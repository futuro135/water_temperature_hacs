"""Sensor platform for Water Temperature Uglich integration."""
import logging
from datetime import timedelta
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DOMAIN,
    NAME,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    ATTR_YESTERDAY_TEMP,
    ATTR_WEEK_AGO_TEMP,
    ATTR_TREND,
    ATTR_AIR_TEMPERATURE,
    ATTR_LAST_UPDATED,
    ATTR_LOCATION,
)
from .water_parser import WaterTemperatureParser

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    update_interval = config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    
    coordinator = WaterTemperatureCoordinator(hass, update_interval)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([WaterTemperatureSensor(coordinator, config_entry)], True)


class WaterTemperatureCoordinator(DataUpdateCoordinator):
    """Class to manage fetching water temperature data."""

    def __init__(self, hass: HomeAssistant, update_interval: int) -> None:
        """Initialize the coordinator."""
        self.parser = WaterTemperatureParser()
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via library."""
        try:
            data = await self.parser.async_get_detailed_info()
            if data is None:
                raise UpdateFailed("Failed to fetch water temperature data")
            return data
        except Exception as exception:
            raise UpdateFailed(f"Error communicating with API: {exception}")


class WaterTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Water Temperature sensor."""

    def __init__(
        self,
        coordinator: WaterTemperatureCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Water Temperature Uglich"
        self._attr_unique_id = f"{DOMAIN}_water_temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer-water"

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, "water_temperature_uglich")},
            "name": NAME,
            "manufacturer": "Custom",
            "model": "Water Temperature Parser",
            "sw_version": "1.0.0",
        }

    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("current_temperature")
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        data = self.coordinator.data
        attributes = {}
        
        if data.get("yesterday_temperature") is not None:
            attributes[ATTR_YESTERDAY_TEMP] = data["yesterday_temperature"]
        
        if data.get("week_ago_temperature") is not None:
            attributes[ATTR_WEEK_AGO_TEMP] = data["week_ago_temperature"]
        
        if data.get("trend"):
            attributes[ATTR_TREND] = data["trend"]
        
        if data.get("air_temperature") is not None:
            attributes[ATTR_AIR_TEMPERATURE] = data["air_temperature"]
        
        if data.get("last_updated"):
            attributes[ATTR_LAST_UPDATED] = data["last_updated"]
        
        if data.get("location"):
            attributes[ATTR_LOCATION] = data["location"]
        
        return attributes

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None 