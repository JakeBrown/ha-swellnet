"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import requests
import logging
import re
from datetime import datetime


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([ExampleSensor()])


class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Middleton"
    _attr_native_unit_of_measurement = "out of 10"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            html_page = requests.get("https://www.swellnet.com/reports/australia/south-australia/middleton").text
            pattern = '(?<=<span class="field-content">)([1-9]|10)(?=\/10)'
            score = re.search(pattern, html_page).group(0)
            d = datetime.now()
        except:
            logging.exception("Error getting weather")
            score = "NA"
        self._attr_native_value = score
