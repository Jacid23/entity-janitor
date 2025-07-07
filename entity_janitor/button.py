"""Button platform for Entity Janitor."""
import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
        EntityJanitorButton(coordinator, "scan_orphans"),
        EntityJanitorButton(coordinator, "clean_orphans_dry_run"),
        EntityJanitorButton(coordinator, "backup_orphans"),
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
        if self._button_type == "scan_orphans":
            await self.coordinator.async_scan_for_orphans()
        elif self._button_type == "clean_orphans_dry_run":
            await self.coordinator.async_clean_orphans(dry_run=True)
        elif self._button_type == "backup_orphans":
            if self.coordinator.orphaned_entities:
                await self.coordinator.async_backup_entities(
                    self.coordinator.orphaned_entities
                )
            else:
                _LOGGER.warning("No orphaned entities to backup")

    @property
    def icon(self) -> str:
        """Return the icon for the button."""
        if self._button_type == "scan_orphans":
            return "mdi:magnify"
        elif self._button_type == "clean_orphans_dry_run":
            return "mdi:play-outline"
        elif self._button_type == "backup_orphans":
            return "mdi:content-save"
        return "mdi:button-pointer"
