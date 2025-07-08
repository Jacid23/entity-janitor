"""Button platform for Entity Janitor."""
import logging
from typing import Any
from datetime import datetime

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory, DeviceInfo

from .const import DOMAIN
from .coordinator import EntityJanitorCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Entity Janitor button platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    buttons = [
        EntityJanitorButton(coordinator, "scan_obsolete"),
        EntityJanitorButton(coordinator, "test_cleanup"),
        EntityJanitorButton(coordinator, "backup_obsolete"),
        EntityJanitorTemplateButton(coordinator, "quick_scan"),
        EntityJanitorTemplateButton(coordinator, "full_cleanup"),
        EntityJanitorTemplateButton(coordinator, "export_report"),
        EntityJanitorTemplateButton(coordinator, "reset_stats"),
    ]

    async_add_entities(buttons)


class EntityJanitorButton(CoordinatorEntity, ButtonEntity):
    """Entity Janitor button."""

    def __init__(
        self,
        coordinator: EntityJanitorCoordinator,
        button_type: str,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._button_type = button_type
        self._attr_name = f"Entity Janitor {button_type.replace('_', ' ').title()}"
        self._attr_unique_id = f"{DOMAIN}_{button_type}"

    async def async_press(self) -> None:
        """Handle the button press."""
        if self._button_type == "scan_obsolete":
            await self.coordinator.async_scan_for_obsolete()
        elif self._button_type == "test_cleanup":
            await self.coordinator.async_clean_obsolete(dry_run=True)
        elif self._button_type == "backup_obsolete":
            if self.coordinator.obsolete_entities:
                await self.coordinator.async_backup_entities(
                    self.coordinator.obsolete_entities
                )
            else:
                _LOGGER.warning("No obsolete entities to backup")

    @property
    def icon(self) -> str:
        """Return the icon for the button."""
        if self._button_type == "scan_obsolete":
            return "mdi:magnify"
        elif self._button_type == "test_cleanup":
            return "mdi:play-outline"
        elif self._button_type == "backup_obsolete":
            return "mdi:content-save"
        return "mdi:button-pointer"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the Entity Janitor device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name="Entity Janitor",
            manufacturer="Custom Integration",
            model="Entity Management System",
            sw_version="1.0.4",
            suggested_area="System",
        )


class EntityJanitorTemplateButton(CoordinatorEntity, ButtonEntity):
    """Entity Janitor template button for user-facing actions."""

    def __init__(
        self,
        coordinator: EntityJanitorCoordinator,
        button_type: str,
    ) -> None:
        """Initialize the template button."""
        super().__init__(coordinator)
        self._button_type = button_type
        self._attr_name = f"Entity Janitor {self._get_display_name()}"
        self._attr_unique_id = f"{DOMAIN}_template_{button_type}"
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the Entity Janitor device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name="Entity Janitor",
            manufacturer="Custom Integration",
            model="Entity Management System",
            sw_version="1.0.4",
            suggested_area="System",
        )

    def _get_display_name(self) -> str:
        """Get the display name for the button."""
        names = {
            "quick_scan": "Quick Scan",
            "full_cleanup": "Full Cleanup",
            "export_report": "Export Report",
            "reset_stats": "Reset Statistics",
        }
        return names.get(self._button_type, self._button_type.replace("_", " ").title())

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info(f"Template button pressed: {self._button_type}")

        if self._button_type == "quick_scan":
            await self._quick_scan()
        elif self._button_type == "full_cleanup":
            await self._full_cleanup()
        elif self._button_type == "export_report":
            await self._export_report()
        elif self._button_type == "reset_stats":
            await self._reset_stats()

    async def _quick_scan(self) -> None:
        """Perform a quick scan for obsolete entities."""
        _LOGGER.info("Starting quick scan for obsolete entities")
        await self.coordinator.async_scan_for_obsolete()

        # Fire event similar to ESPHome pattern
        self.hass.bus.async_fire(
            "entity_janitor_quick_scan_complete",
            {"entity_id": self.entity_id, "obsolete_count": len(self.coordinator.obsolete_entities)},
        )

    async def _full_cleanup(self) -> None:
        """Perform full cleanup with backup."""
        _LOGGER.info("Starting full cleanup with backup")

        # Check if dry run mode is enabled
        dry_run = self.coordinator.config_entry.options.get("dry_run_mode", False)
        backup_enabled = self.coordinator.config_entry.options.get("backup_before_clean", True)

        if backup_enabled and self.coordinator.obsolete_entities and not dry_run:
            await self.coordinator.async_backup_entities(self.coordinator.obsolete_entities)

        await self.coordinator.async_clean_obsolete(dry_run=dry_run)

        # Fire event
        self.hass.bus.async_fire(
            "entity_janitor_full_cleanup_complete",
            {"entity_id": self.entity_id, "dry_run": dry_run},
        )

    async def _export_report(self) -> None:
        """Export a report of obsolete entities."""
        _LOGGER.info("Exporting obsolete entities report")

        if not self.coordinator.obsolete_entities:
            _LOGGER.warning("No obsolete entities to export")
            return

        import json
        from datetime import datetime

        report = {
            "timestamp": datetime.now().isoformat(),
            "obsolete_count": len(self.coordinator.obsolete_entities),
            "entities": [
                {
                    "entity_id": entity_data["entity_id"],
                    "domain": entity_data["entity_id"].split(".")[0],
                    "name": entity_data.get("name", "Unknown"),
                    "last_seen": entity_data.get("created_at", "Unknown"),
                    "reason": entity_data.get("reason", "Unknown"),
                    "platform": entity_data.get("platform", "Unknown"),
                }
                for entity_data in self.coordinator.obsolete_entities
            ],
        }

        # Save to file in Home Assistant config directory
        file_path = self.hass.config.path(
            f"entity_janitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        try:
            with open(file_path, "w") as f:
                json.dump(report, f, indent=2)
            _LOGGER.info(f"Report exported to {file_path}")
        except Exception as e:
            _LOGGER.error(f"Failed to export report: {e}")

    async def _reset_stats(self) -> None:
        """Reset statistics and clear cached data."""
        _LOGGER.info("Resetting Entity Janitor statistics")

        # Clear obsolete entities cache
        self.coordinator.obsolete_entities.clear()

        # Reset last scan time
        self.coordinator.last_scan = None

        # Request refresh
        await self.coordinator.async_request_refresh()

        # Fire event
        self.hass.bus.async_fire(
            "entity_janitor_stats_reset",
            {"entity_id": self.entity_id},
        )

    @property
    def icon(self) -> str:
        """Return the icon for the button."""
        icons = {
            "quick_scan": "mdi:magnify-scan",
            "full_cleanup": "mdi:delete-sweep",
            "export_report": "mdi:file-export",
            "reset_stats": "mdi:refresh",
        }
        return icons.get(self._button_type, "mdi:button-pointer")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "button_type": self._button_type,
            "description": self._get_description(),
            "last_pressed": getattr(self, "_last_pressed", None),
        }

    def _get_description(self) -> str:
        """Get description for the button."""
        descriptions = {
            "quick_scan": "Quickly scan for obsolete entities",
            "full_cleanup": "Perform full cleanup with backup (respects dry run mode)",
            "export_report": "Export detailed report of obsolete entities",
            "reset_stats": "Reset statistics and clear cached data",
        }
        return descriptions.get(self._button_type, "")
