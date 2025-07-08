"""Data update coordinator for Entity Janitor."""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_MINIMUM_AGE_DAYS,
    CONF_EXCLUDED_DOMAINS,
    CONF_EXCLUDED_ENTITIES,
    DEFAULT_MINIMUM_AGE_DAYS,
    DEFAULT_EXCLUDED_DOMAINS,
)

_LOGGER = logging.getLogger(__name__)


class EntityJanitorCoordinator(DataUpdateCoordinator):
    """Coordinator for Entity Janitor data updates."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )
        self.config_entry = config_entry
        self.hass = hass
        self._orphaned_entities: List[Dict[str, Any]] = []
        self._last_scan: Optional[datetime] = None
        self._scan_in_progress = False

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from API endpoint."""
        try:
            # Get current entity and device registries
            entity_registry = async_get_entity_registry(self.hass)
            device_registry = async_get_device_registry(self.hass)

            total_entities = len(entity_registry.entities)
            orphaned_count = len(self._orphaned_entities)

            return {
                "total_entities": total_entities,
                "orphaned_entities": orphaned_count,
                "last_scan": self._last_scan,
                "scan_in_progress": self._scan_in_progress,
            }
        except Exception as ex:
            raise UpdateFailed(f"Error communicating with API: {ex}") from ex

    async def async_scan_for_orphans(self, *args) -> List[Dict[str, Any]]:
        """Scan for orphaned entities."""
        if self._scan_in_progress:
            _LOGGER.warning("Scan already in progress, skipping")
            return self._orphaned_entities

        _LOGGER.info("Starting orphaned entity scan")
        self._scan_in_progress = True
        
        try:
            entity_registry = async_get_entity_registry(self.hass)
            device_registry = async_get_device_registry(self.hass)
            
            # Get configuration
            minimum_age_days = self.config_entry.options.get(
                CONF_MINIMUM_AGE_DAYS, DEFAULT_MINIMUM_AGE_DAYS
            )
            excluded_domains = self.config_entry.options.get(
                CONF_EXCLUDED_DOMAINS, DEFAULT_EXCLUDED_DOMAINS
            )
            excluded_entities = self.config_entry.options.get(
                CONF_EXCLUDED_ENTITIES, []
            )

            cutoff_date = dt_util.utcnow() - timedelta(days=minimum_age_days)
            orphaned_entities = []

            for entity_id, entity in entity_registry.entities.items():
                # Skip if entity is in excluded domains
                domain = entity_id.split(".")[0]
                if domain in excluded_domains:
                    continue

                # Skip if entity is explicitly excluded
                if entity_id in excluded_entities:
                    continue

                # Check if entity is orphaned
                is_orphaned = False
                reason = ""

                # Check if device exists but is orphaned
                if entity.device_id:
                    device = device_registry.devices.get(entity.device_id)
                    if not device:
                        is_orphaned = True
                        reason = "Device not found"
                    elif not device.config_entries:
                        is_orphaned = True
                        reason = "Device has no config entries"
                    elif not any(
                        entry_id in self.hass.config_entries.async_entries()
                        for entry_id in device.config_entries
                    ):
                        is_orphaned = True
                        reason = "Device config entries not loaded"

                # Check if config entry exists
                elif entity.config_entry_id:
                    config_entry = self.hass.config_entries.async_get_entry(
                        entity.config_entry_id
                    )
                    if not config_entry:
                        is_orphaned = True
                        reason = "Config entry not found"
                    elif config_entry.state.name != "loaded":
                        is_orphaned = True
                        reason = f"Config entry state: {config_entry.state.name}"

                # Check if entity is old enough
                if is_orphaned and entity.created_at:
                    if entity.created_at > cutoff_date:
                        continue  # Too new, skip

                # Check if entity actually exists in Home Assistant
                if is_orphaned:
                    state = self.hass.states.get(entity_id)
                    if state is not None:
                        # Entity has state, might not be orphaned
                        continue

                if is_orphaned:
                    orphaned_entities.append({
                        "entity_id": entity_id,
                        "domain": domain,
                        "platform": entity.platform,
                        "device_id": entity.device_id,
                        "config_entry_id": entity.config_entry_id,
                        "created_at": entity.created_at.isoformat() if entity.created_at else None,
                        "reason": reason,
                        "name": entity.name or entity.original_name,
                        "unique_id": entity.unique_id,
                    })

            self._orphaned_entities = orphaned_entities
            self._last_scan = dt_util.utcnow()
            
            _LOGGER.info(f"Scan completed. Found {len(orphaned_entities)} orphaned entities")
            
            # Fire event
            self.hass.bus.fire(
                "entity_janitor_orphans_found",
                {
                    "orphan_count": len(orphaned_entities),
                    "total_entities": len(entity_registry.entities),
                }
            )

            return orphaned_entities

        except Exception as ex:
            _LOGGER.error(f"Error during orphan scan: {ex}")
            raise
        finally:
            self._scan_in_progress = False
            await self.async_update_listeners()

    async def async_clean_orphans(
        self, 
        entity_ids: Optional[List[str]] = None,
        dry_run: bool = True,
        backup_before_clean: bool = True
    ) -> Dict[str, Any]:
        """Clean orphaned entities."""
        _LOGGER.info(f"Starting orphan cleanup (dry_run={dry_run})")
        
        # If no specific entities provided, use all orphaned entities
        if entity_ids is None:
            if not self._orphaned_entities:
                await self.async_scan_for_orphans()
            entities_to_clean = self._orphaned_entities
        else:
            entities_to_clean = [
                entity for entity in self._orphaned_entities
                if entity["entity_id"] in entity_ids
            ]

        if not entities_to_clean:
            return {"cleaned_count": 0, "skipped_count": 0, "backup_file": None}

        backup_file = None
        if backup_before_clean and not dry_run:
            backup_file = await self.async_backup_entities(entities_to_clean)

        cleaned_count = 0
        skipped_count = 0
        
        if not dry_run:
            entity_registry = async_get_entity_registry(self.hass)
            
            for entity_data in entities_to_clean:
                entity_id = entity_data["entity_id"]
                try:
                    if entity_id in entity_registry.entities:
                        entity_registry.async_remove(entity_id)
                        cleaned_count += 1
                        _LOGGER.info(f"Removed orphaned entity: {entity_id}")
                    else:
                        skipped_count += 1
                        _LOGGER.warning(f"Entity not found in registry: {entity_id}")
                except Exception as ex:
                    _LOGGER.error(f"Error removing entity {entity_id}: {ex}")
                    skipped_count += 1

            # Update our internal list
            remaining_entities = [
                entity for entity in self._orphaned_entities
                if entity["entity_id"] not in [e["entity_id"] for e in entities_to_clean]
            ]
            self._orphaned_entities = remaining_entities

            # Fire event
            self.hass.bus.fire(
                "entity_janitor_cleanup_complete",
                {
                    "cleaned_count": cleaned_count,
                    "skipped_count": skipped_count,
                    "backup_file": backup_file,
                }
            )

        result = {
            "cleaned_count": cleaned_count if not dry_run else 0,
            "skipped_count": skipped_count,
            "backup_file": backup_file,
            "dry_run": dry_run,
            "would_clean": len(entities_to_clean) if dry_run else 0,
        }

        _LOGGER.info(f"Cleanup completed: {result}")
        return result

    async def async_backup_entities(
        self, entities: List[Dict[str, Any]]
    ) -> str:
        """Backup entities to a file."""
        timestamp = dt_util.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_file = f"entity_janitor_backup_{timestamp}.json"
        backup_path = self.hass.config.path(backup_file)

        backup_data = {
            "timestamp": timestamp,
            "entities": entities,
            "total_count": len(entities),
        }

        try:
            with open(backup_path, "w", encoding="utf-8") as file:
                json.dump(backup_data, file, indent=2, ensure_ascii=False)
            
            _LOGGER.info(f"Backed up {len(entities)} entities to {backup_file}")
            return backup_file
        except Exception as ex:
            _LOGGER.error(f"Error creating backup: {ex}")
            raise

    @property
    def orphaned_entities(self) -> List[Dict[str, Any]]:
        """Return list of orphaned entities."""
        return self._orphaned_entities

    @property
    def last_scan(self) -> Optional[datetime]:
        """Return last scan time."""
        return self._last_scan
