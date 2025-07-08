"""Config flow for Entity Janitor integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_AUTO_SCAN,
    CONF_SCAN_INTERVAL,
    CONF_AUTO_CLEAN,
    CONF_BACKUP_BEFORE_CLEAN,
    CONF_EXCLUDED_DOMAINS,
    CONF_EXCLUDED_ENTITIES,
    CONF_MINIMUM_AGE_DAYS,
    CONF_DRY_RUN,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_MINIMUM_AGE_DAYS,
    DEFAULT_EXCLUDED_DOMAINS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_AUTO_SCAN, default=False): bool,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=15, max=1440)
        ),
        vol.Optional(CONF_AUTO_CLEAN, default=False): bool,
        vol.Optional(CONF_BACKUP_BEFORE_CLEAN, default=True): bool,
        vol.Optional(CONF_MINIMUM_AGE_DAYS, default=DEFAULT_MINIMUM_AGE_DAYS): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=365)
        ),
        vol.Optional(CONF_DRY_RUN, default=True): bool,
    }
)


@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Entity Janitor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLLING

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Check if already configured
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
            
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        # Validate that auto_clean is not enabled without backup
        if user_input.get(CONF_AUTO_CLEAN) and not user_input.get(CONF_BACKUP_BEFORE_CLEAN):
            errors["base"] = "auto_clean_requires_backup"

        if errors:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA,
                errors=errors,
            )

        return self.async_create_entry(
            title="Entity Janitor",
            data={},
            options=user_input,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Entity Janitor options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_AUTO_SCAN,
                    default=self.config_entry.options.get(CONF_AUTO_SCAN, False),
                ): bool,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=15, max=1440)),
                vol.Optional(
                    CONF_AUTO_CLEAN,
                    default=self.config_entry.options.get(CONF_AUTO_CLEAN, False),
                ): bool,
                vol.Optional(
                    CONF_BACKUP_BEFORE_CLEAN,
                    default=self.config_entry.options.get(CONF_BACKUP_BEFORE_CLEAN, True),
                ): bool,
                vol.Optional(
                    CONF_MINIMUM_AGE_DAYS,
                    default=self.config_entry.options.get(CONF_MINIMUM_AGE_DAYS, DEFAULT_MINIMUM_AGE_DAYS),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=365)),
                vol.Optional(
                    CONF_DRY_RUN,
                    default=self.config_entry.options.get(CONF_DRY_RUN, True),
                ): bool,
                vol.Optional(
                    CONF_EXCLUDED_DOMAINS,
                    default=self.config_entry.options.get(CONF_EXCLUDED_DOMAINS, DEFAULT_EXCLUDED_DOMAINS),
                ): cv.multi_select([
                    "automation", "script", "scene", "zone", "person", "device_tracker",
                    "persistent_notification", "input_boolean", "input_text", "input_number",
                    "input_select", "input_datetime", "timer", "counter", "weather",
                    "sun", "group", "media_player", "light", "switch", "sensor",
                    "binary_sensor", "camera", "climate", "cover", "fan", "lock",
                    "alarm_control_panel", "vacuum", "water_heater", "humidifier",
                    "remote", "select", "siren", "button", "number", "text"
                ]),
                vol.Optional(
                    CONF_EXCLUDED_ENTITIES,
                    default=self.config_entry.options.get(CONF_EXCLUDED_ENTITIES, []),
                ): cv.multi_select([]),  # This would be dynamically populated
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )
