"""Switch platform for Entity Janitor."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_AUTO_SCAN, CONF_AUTO_CLEAN
from .coordinator import EntityJanitorCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Entity Janitor switch platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    switches = [
        EntityJanitorSwitch(coordinator, "auto_scan"),
        EntityJanitorSwitch(coordinator, "auto_clean"),
    ]

    async_add_entities(switches)


class EntityJanitorSwitch(CoordinatorEntity, SwitchEntity):
    """Entity Janitor switch."""

    def __init__(
        self,
        coordinator: EntityJanitorCoordinator,
        switch_type: str,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._switch_type = switch_type
        self._attr_name = f"Entity Janitor {switch_type.replace('_', ' ').title()}"
        self._attr_unique_id = f"{DOMAIN}_{switch_type}"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        if self._switch_type == "auto_scan":
            return self.coordinator.config_entry.options.get(CONF_AUTO_SCAN, False)
        elif self._switch_type == "auto_clean":
            return self.coordinator.config_entry.options.get(CONF_AUTO_CLEAN, False)
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        options = dict(self.coordinator.config_entry.options)
        
        if self._switch_type == "auto_scan":
            options[CONF_AUTO_SCAN] = True
        elif self._switch_type == "auto_clean":
            options[CONF_AUTO_CLEAN] = True
        
        self.hass.config_entries.async_update_entry(
            self.coordinator.config_entry, options=options
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        options = dict(self.coordinator.config_entry.options)
        
        if self._switch_type == "auto_scan":
            options[CONF_AUTO_SCAN] = False
        elif self._switch_type == "auto_clean":
            options[CONF_AUTO_CLEAN] = False
        
        self.hass.config_entries.async_update_entry(
            self.coordinator.config_entry, options=options
        )
        await self.coordinator.async_request_refresh()

    @property
    def icon(self) -> str:
        """Return the icon for the switch."""
        if self._switch_type == "auto_scan":
            return "mdi:magnify-scan"
        elif self._switch_type == "auto_clean":
            return "mdi:delete-sweep"
        return "mdi:toggle-switch"
