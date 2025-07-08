"""
Entity Janitor - Home Assistant Custom Integration
Automatically detects and manages obsolete entities in Home Assistant.
"""
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers import device_registry as dr
from homeassistant.const import Platform

from .const import DOMAIN, PLATFORMS
from .coordinator import EntityJanitorCoordinator
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Entity Janitor integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Entity Janitor from a config entry."""
    _LOGGER.info("Setting up Entity Janitor integration")
    
    coordinator = EntityJanitorCoordinator(hass, entry)
    
    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    _LOGGER.info("Coordinator stored in hass.data")
    
    # Initial data fetch
    try:
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info("Coordinator first refresh completed")
    except Exception as ex:
        _LOGGER.error(f"Failed to initialize coordinator: {ex}")
        return False
    
    # Register device with icon
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name="Entity Janitor",
        manufacturer="Custom Integration",
        model="Entity Management System",
        sw_version="1.0.4",
        suggested_area="System",
    )
    _LOGGER.info("Device registered")
    
    # Setup platforms
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        _LOGGER.info("Platforms setup completed")
    except Exception as ex:
        _LOGGER.error(f"Failed to setup platforms: {ex}")
        return False
    
    # Setup services
    try:
        await async_setup_services(hass, coordinator)
        _LOGGER.info("Services setup completed")
    except Exception as ex:
        _LOGGER.error(f"Failed to setup services: {ex}")
        return False
    
    # Setup periodic scanning if enabled
    if entry.options.get("auto_scan", False):
        async_track_time_interval(
            hass, coordinator.async_scan_for_obsolete, SCAN_INTERVAL
        )
        _LOGGER.info("Periodic scanning enabled")
    
    _LOGGER.info("Entity Janitor integration setup completed successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
