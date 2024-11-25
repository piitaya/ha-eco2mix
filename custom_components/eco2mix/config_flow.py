"""Config flow for éCO2mix integration."""
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import UnitOfTime

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    SENSOR_TYPES,
    DEFAULT_SENSORS,
)

class Eco2mixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for éCO2mix."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        # Prevent multiple instances
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # Build sensors selection schema
        sensors_schema = {
            vol.Optional(sensor_id, default=sensor_id in DEFAULT_SENSORS): bool
            for sensor_id in SENSOR_TYPES
        }
        
        data_schema = vol.Schema({
            vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.All(
                vol.Coerce(int),
                vol.Range(min=MIN_SCAN_INTERVAL)
            ),
            **sensors_schema
        })

        if user_input is not None:
            # Extract selected sensors
            selected_sensors = [
                sensor_id for sensor_id in SENSOR_TYPES 
                if user_input.get(sensor_id, False)
            ]
            
            # Prepare configuration data
            data = {
                "scan_interval": user_input["scan_interval"],
                "sensors": selected_sensors
            }
            
            return self.async_create_entry(title="éCO2mix", data=data)

        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return Eco2mixOptionsFlow(config_entry)

class Eco2mixOptionsFlow(config_entries.OptionsFlow):
    """Config flow options handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle options flow."""
        if user_input is not None:
            # Extract selected sensors
            selected_sensors = [
                sensor_id for sensor_id in SENSOR_TYPES 
                if user_input.get(sensor_id, False)
            ]
            
            return self.async_create_entry(
                title="", 
                data={
                    "scan_interval": user_input["scan_interval"],
                    "sensors": selected_sensors
                }
            )

        # Prepare current selections
        current_sensors = self.config_entry.data.get("sensors", [])
        
        # Build sensors schema
        sensors_schema = {
            vol.Optional(sensor_id, default=sensor_id in current_sensors): bool
            for sensor_id in SENSOR_TYPES
        }

        options_schema = vol.Schema({
            vol.Required(
                "scan_interval",
                default=self.config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL),
            ): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL)),
            **sensors_schema
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema
        )
