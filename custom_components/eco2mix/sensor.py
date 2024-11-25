"""Support for éCO2mix sensors."""
from datetime import datetime
import logging
from typing import Any
import pytz

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    UnitOfPower,
    PERCENTAGE,
)

from .const import (
    DOMAIN, 
    SENSOR_TYPES,
    RENEWABLE_SOURCES,
    LOW_CARBON_SOURCES,
)
from .coordinator import Eco2mixDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the éCO2mix sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Get selected sensors from config
    selected_sensors = config_entry.data.get("sensors", [])
    
    sensors = []
    for sensor_type, (name, icon) in SENSOR_TYPES.items():
        # Skip if sensor not selected
        if sensor_type not in selected_sensors:
            continue
            
        if sensor_type == "last_update":
            sensors.append(
                Eco2mixLastUpdateSensor(coordinator, sensor_type, name, icon)
            )
        elif sensor_type.endswith("_percentage"):
            sensors.append(
                Eco2mixPercentageSensor(coordinator, sensor_type, name, icon)
            )
        elif sensor_type in ["pumping", "import", "export", "total_production"]:
            sensors.append(
                Eco2mixPowerSensor(coordinator, sensor_type, name, icon)
            )
        elif sensor_type in ["renewable", "low_carbon"]:
            sensors.append(
                Eco2mixAggregateSensor(coordinator, sensor_type, name, icon)
            )
        else:
            sensors.append(
                Eco2mixPowerSensor(coordinator, sensor_type, name, icon)
            )

    async_add_entities(sensors)

class Eco2mixBaseSensor(CoordinatorEntity[Eco2mixDataUpdateCoordinator], SensorEntity):
    """Base class for éCO2mix sensors."""

    def __init__(self, coordinator, sensor_type, name, icon):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"eco2mix_{sensor_type}"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, "eco2mix_device")},
            "name": "éCO2mix",
            "manufacturer": "LFPoulain",
            "model": "Integration Eco2Mix RTE via open data ODRE",
            "sw_version": "1.0.0",
        }

class Eco2mixPowerSensor(Eco2mixBaseSensor):
    """Sensor for power values (in kW)."""

    def __init__(self, coordinator, sensor_type, name, icon):
        """Initialize the power sensor."""
        super().__init__(coordinator, sensor_type, name, icon)
        self._attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        try:
            value = self.coordinator.data[self._sensor_type]
            return round(value, 2) if value is not None else None
        except (KeyError, TypeError):
            return None

class Eco2mixPercentageSensor(Eco2mixBaseSensor):
    """Sensor for percentage values."""

    def __init__(self, coordinator, sensor_type, name, icon):
        """Initialize the percentage sensor."""
        super().__init__(coordinator, sensor_type, name, icon)
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        try:
            value = self.coordinator.data[self._sensor_type]
            return round(value, 1) if value is not None else None
        except (KeyError, TypeError):
            return None

class Eco2mixLastUpdateSensor(Eco2mixBaseSensor):
    """Sensor for last update timestamp."""

    def __init__(self, coordinator, sensor_type, name, icon):
        """Initialize the timestamp sensor."""
        super().__init__(coordinator, sensor_type, name, icon)
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_state_class = None
        self._attr_native_unit_of_measurement = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        try:
            timestamp_str = self.coordinator.data["timestamp"]
            return datetime.fromisoformat(timestamp_str)
        except (KeyError, TypeError, ValueError):
            return None

class Eco2mixAggregateSensor(Eco2mixPowerSensor):
    """Sensor for aggregated renewable or low carbon production."""

    @property
    def native_value(self) -> StateType:
        """Return the total production for renewable or low carbon sources."""
        try:
            value = self.coordinator.data[self._sensor_type]
            return round(value, 2) if value is not None else None
        except (KeyError, TypeError):
            return None
