"""Sensor platform for Entity Janitor."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    ATTR_OBSOLETE_COUNT,
    ATTR_TOTAL_ENTITIES,
    ATTR_LAST_SCAN,
)
from .coordinator import EntityJanitorCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Entity Janitor sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        EntityJanitorSensor(coordinator, "obsolete_count"),
        EntityJanitorSensor(coordinator, "total_entities"),
        EntityJanitorSensor(coordinator, "last_scan"),
    ]

    async_add_entities(sensors)


class EntityJanitorSensor(CoordinatorEntity, SensorEntity):
    """Entity Janitor sensor."""

    def __init__(
        self,
        coordinator: EntityJanitorCoordinator,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"Entity Janitor {sensor_type.replace('_', ' ').title()}"
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self._sensor_type == "obsolete_count":
            return self.coordinator.data.get("orphaned_entities", 0)
        elif self._sensor_type == "total_entities":
            return self.coordinator.data.get("total_entities", 0)
        elif self._sensor_type == "last_scan":
            last_scan = self.coordinator.data.get("last_scan")
            if last_scan:
                # Return datetime object for timestamp device class
                if isinstance(last_scan, str):
                    return dt_util.parse_datetime(last_scan)
                return last_scan
            return None
        return None

    @property
    def device_class(self) -> Optional[SensorDeviceClass]:
        """Return the device class."""
        if self._sensor_type in ["obsolete_count", "total_entities"]:
            return None  # No specific device class for counts
        elif self._sensor_type == "last_scan":
            return SensorDeviceClass.TIMESTAMP
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra state attributes."""
        if self._sensor_type == "orphan_count":
            return {
                "orphaned_entities": [
                    entity["entity_id"] for entity in self.coordinator.orphaned_entities
                ][:50],  # Limit to first 50 to avoid state size limits
                "scan_in_progress": self.coordinator.data.get("scan_in_progress", False),
            }
        elif self._sensor_type == "total_entities":
            return {
                "orphan_percentage": (
                    round(
                        (self.coordinator.data.get("orphaned_entities", 0) / 
                         max(self.coordinator.data.get("total_entities", 1), 1)) * 100, 2
                    )
                )
            }
        return {}

    @property
    def icon(self) -> str:
        """Return the icon for the sensor."""
        if self._sensor_type == "orphan_count":
            return "mdi:delete-sweep"
        elif self._sensor_type == "total_entities":
            return "mdi:counter"
        elif self._sensor_type == "last_scan":
            return "mdi:clock-outline"
        return "mdi:information"

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
