"""
Entity Janitor - Home Assistant Custom Integration
Automatically detects and manages orphaned entities in Home Assistant.
"""
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
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
    coordinator = EntityJanitorCoordinator(hass, entry)
    
    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Initial data fetch
    await coordinator.async_config_entry_first_refresh()
    
    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Setup services
    await async_setup_services(hass, coordinator)
    
    # Setup periodic scanning if enabled
    if entry.options.get("auto_scan", False):
        async_track_time_interval(
            hass, coordinator.async_scan_for_orphans, SCAN_INTERVAL
        )
    
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
