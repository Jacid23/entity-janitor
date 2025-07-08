"""Switch platform for Entity Janitor."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory, DeviceInfo

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
        EntityJanitorTemplateSwitch(coordinator, "backup_before_clean"),
        EntityJanitorTemplateSwitch(coordinator, "dry_run_mode"),
        EntityJanitorTemplateSwitch(coordinator, "notifications_enabled"),
        EntityJanitorTemplateSwitch(coordinator, "detailed_logging"),
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
        self._attr_entity_category = EntityCategory.CONFIG

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

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the Entity Janitor device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name="Entity Janitor",
            manufacturer="Custom Integration",
            model="Entity Management System",
            sw_version="1.0.4",
            configuration_url="/local/entity_janitor/icon.svg",
            suggested_area="System",
        )


class EntityJanitorTemplateSwitch(CoordinatorEntity, SwitchEntity):
    """Entity Janitor template switch for user-facing controls."""

    def __init__(
        self,
        coordinator: EntityJanitorCoordinator,
        switch_type: str,
    ) -> None:
        """Initialize the template switch."""
        super().__init__(coordinator)
        self._switch_type = switch_type
        self._attr_name = f"Entity Janitor {self._get_display_name()}"
        self._attr_unique_id = f"{DOMAIN}_template_{switch_type}"
        self._attr_entity_category = EntityCategory.CONFIG
        self._state = self._get_initial_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the Entity Janitor device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name="Entity Janitor",
            manufacturer="Custom Integration",
            model="Entity Management System",
            sw_version="1.0.4",
            configuration_url="/local/entity_janitor/icon.svg",
            suggested_area="System",
        )

    def _get_display_name(self) -> str:
        """Get the display name for the switch."""
        names = {
            "backup_before_clean": "Backup Before Clean",
            "dry_run_mode": "Dry Run Mode",
            "notifications_enabled": "Notifications",
            "detailed_logging": "Detailed Logging",
        }
        return names.get(self._switch_type, self._switch_type.replace("_", " ").title())

    def _get_initial_state(self) -> bool:
        """Get the initial state from config or defaults."""
        defaults = {
            "backup_before_clean": True,
            "dry_run_mode": False,
            "notifications_enabled": True,
            "detailed_logging": False,
        }
        return self.coordinator.config_entry.options.get(
            self._switch_type, defaults.get(self._switch_type, False)
        )

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._state = True
        options = dict(self.coordinator.config_entry.options)
        options[self._switch_type] = True
        
        self.hass.config_entries.async_update_entry(
            self.coordinator.config_entry, options=options
        )
        self.async_write_ha_state()
        
        # Trigger specific actions based on switch type
        await self._handle_switch_action(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self._state = False
        options = dict(self.coordinator.config_entry.options)
        options[self._switch_type] = False
        
        self.hass.config_entries.async_update_entry(
            self.coordinator.config_entry, options=options
        )
        self.async_write_ha_state()
        
        # Trigger specific actions based on switch type
        await self._handle_switch_action(False)

    async def _handle_switch_action(self, state: bool) -> None:
        """Handle switch-specific actions when toggled."""
        if self._switch_type == "detailed_logging":
            # Update logging level
            logger = logging.getLogger(__name__.split('.')[0])
            logger.setLevel(logging.DEBUG if state else logging.INFO)
            _LOGGER.info(f"Detailed logging {'enabled' if state else 'disabled'}")
        elif self._switch_type == "notifications_enabled":
            _LOGGER.info(f"Notifications {'enabled' if state else 'disabled'}")
        elif self._switch_type == "backup_before_clean":
            _LOGGER.info(f"Backup before clean {'enabled' if state else 'disabled'}")
        elif self._switch_type == "dry_run_mode":
            _LOGGER.info(f"Dry run mode {'enabled' if state else 'disabled'}")

    @property
    def icon(self) -> str:
        """Return the icon for the switch."""
        icons = {
            "backup_before_clean": "mdi:content-save-cog",
            "dry_run_mode": "mdi:test-tube",
            "notifications_enabled": "mdi:bell-ring",
            "detailed_logging": "mdi:text-box-search",
        }
        return icons.get(self._switch_type, "mdi:toggle-switch")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "switch_type": self._switch_type,
            "description": self._get_description(),
        }

    def _get_description(self) -> str:
        """Get description for the switch."""
        descriptions = {
            "backup_before_clean": "Automatically backup entities before cleaning",
            "dry_run_mode": "Test cleanup operations without actually removing entities",
            "notifications_enabled": "Send notifications when obsolete entities are found",
            "detailed_logging": "Enable detailed logging for troubleshooting",
        }
        return descriptions.get(self._switch_type, "")
