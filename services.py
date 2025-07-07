"""Services for Entity Janitor integration."""
import logging
from typing import Any, Dict, List

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    SERVICE_SCAN_ORPHANS,
    SERVICE_CLEAN_ORPHANS,
    SERVICE_BACKUP_ENTITIES,
    SERVICE_RESTORE_ENTITIES,
)
from .coordinator import EntityJanitorCoordinator

_LOGGER = logging.getLogger(__name__)

SERVICE_SCAN_ORPHANS_SCHEMA = vol.Schema({})

SERVICE_CLEAN_ORPHANS_SCHEMA = vol.Schema({
    vol.Optional("entity_ids", default=[]): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional("dry_run", default=True): bool,
    vol.Optional("backup_before_clean", default=True): bool,
})

SERVICE_BACKUP_ENTITIES_SCHEMA = vol.Schema({
    vol.Optional("entity_ids", default=[]): vol.All(cv.ensure_list, [cv.string]),
})

SERVICE_RESTORE_ENTITIES_SCHEMA = vol.Schema({
    vol.Required("backup_file"): cv.string,
})


async def async_setup_services(hass: HomeAssistant, coordinator: EntityJanitorCoordinator) -> None:
    """Set up services for Entity Janitor."""
    
    async def handle_scan_orphans(call: ServiceCall) -> None:
        """Handle scan orphans service call."""
        try:
            orphans = await coordinator.async_scan_for_orphans()
            _LOGGER.info(f"Scan service completed. Found {len(orphans)} orphaned entities")
        except Exception as ex:
            _LOGGER.error(f"Error in scan service: {ex}")
            raise

    async def handle_clean_orphans(call: ServiceCall) -> None:
        """Handle clean orphans service call."""
        entity_ids = call.data.get("entity_ids", [])
        dry_run = call.data.get("dry_run", True)
        backup_before_clean = call.data.get("backup_before_clean", True)
        
        try:
            result = await coordinator.async_clean_orphans(
                entity_ids=entity_ids if entity_ids else None,
                dry_run=dry_run,
                backup_before_clean=backup_before_clean
            )
            _LOGGER.info(f"Clean service completed: {result}")
        except Exception as ex:
            _LOGGER.error(f"Error in clean service: {ex}")
            raise

    async def handle_backup_entities(call: ServiceCall) -> None:
        """Handle backup entities service call."""
        entity_ids = call.data.get("entity_ids", [])
        
        try:
            if entity_ids:
                # Backup specific entities
                entities_to_backup = [
                    entity for entity in coordinator.orphaned_entities
                    if entity["entity_id"] in entity_ids
                ]
            else:
                # Backup all orphaned entities
                entities_to_backup = coordinator.orphaned_entities
            
            if entities_to_backup:
                backup_file = await coordinator.async_backup_entities(entities_to_backup)
                _LOGGER.info(f"Backup service completed: {backup_file}")
            else:
                _LOGGER.warning("No entities to backup")
        except Exception as ex:
            _LOGGER.error(f"Error in backup service: {ex}")
            raise

    async def handle_restore_entities(call: ServiceCall) -> None:
        """Handle restore entities service call."""
        backup_file = call.data.get("backup_file")
        
        try:
            # TODO: Implement restore functionality
            _LOGGER.warning("Restore functionality not yet implemented")
        except Exception as ex:
            _LOGGER.error(f"Error in restore service: {ex}")
            raise

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SCAN_ORPHANS,
        handle_scan_orphans,
        schema=SERVICE_SCAN_ORPHANS_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CLEAN_ORPHANS,
        handle_clean_orphans,
        schema=SERVICE_CLEAN_ORPHANS_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_BACKUP_ENTITIES,
        handle_backup_entities,
        schema=SERVICE_BACKUP_ENTITIES_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESTORE_ENTITIES,
        handle_restore_entities,
        schema=SERVICE_RESTORE_ENTITIES_SCHEMA,
    )
