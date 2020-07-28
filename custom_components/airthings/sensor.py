import logging
from typing import Optional

from homeassistant.helpers.entity import Entity

from .api import AirthingsDevice
from .const import DOMAIN, SENSOR_TYPES, MANUFACTURER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Airthings sensors."""

    def get_entities():
        """Get a list of entities."""
        hc_api = hass.data[DOMAIN][config_entry.entry_id]

        entities = []
        for location in hc_api.locations:
            for d_id in location.devices:
                device = location.devices.get(d_id)
                for f in device.data:
                    if f not in SENSOR_TYPES:
                        _LOGGER.warning("Field %s not represented in sensor types for device %s", f, d_id)
                        continue
                    entities += [AirthingsSensor(device, f)]

        return entities

    async_add_entities(await hass.async_add_executor_job(get_entities), True)


class AirthingsSensor(Entity):
    def __init__(self, device: AirthingsDevice, sensor_type: str) -> None:
        """Initialize the entity."""
        self._device = device
        self._sensor_type = sensor_type
        self._device_name = f"{self._device.location_name} {self._device.name}"
        self._name = f"{MANUFACTURER} {self._device_name} {SENSOR_TYPES.get(sensor_type).name}"

    @property
    def state(self):
        """Return data for the specific sensor on the device."""
        value = self._device.data.get(self._sensor_type, None)
        return SENSOR_TYPES[self._sensor_type].transform(value)

    @property
    def available(self):
        """Return true if the sensor is available."""
        return self.state is not None

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        """Return the name of the node (used for Entity_ID)."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id base on the id returned by Airthings and the sensor."""
        return f"{self._device.device_id}-{self._sensor_type}"

    @property
    def device_info(self):
        """Return info about the device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device_name,
            "manufacturer": f"{MANUFACTURER}",
            "model": self._device.device_type,
        }

    @property
    def unit_of_measurement(self) -> Optional[str]:
        return SENSOR_TYPES[self._sensor_type].unit

    @property
    def icon(self) -> Optional[str]:
        return SENSOR_TYPES[self._sensor_type].icon

    @property
    def device_class(self) -> Optional[str]:
        return SENSOR_TYPES[self._sensor_type].device_class

    def update(self):
        """Update the entity."""
        self._device.update_location()
