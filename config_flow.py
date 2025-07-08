"""Config flow for Entity Janitor integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class EntityJanitorConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Entity Janitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.info("Entity Janitor config flow started")
        
        if self._async_current_entries():
            _LOGGER.info("Entity Janitor already configured, aborting")
            return self.async_abort(reason="single_instance_allowed")
            
        if user_input is not None:
            _LOGGER.info("Creating Entity Janitor config entry")
            return self.async_create_entry(
                title="Entity Janitor",
                data={},
            )

        _LOGGER.info("Showing Entity Janitor config form")
        return self.async_show_form(
            step_id="user",
        )
