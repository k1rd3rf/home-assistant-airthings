from datetime import timedelta

from homeassistant.const import UNIT_PERCENTAGE, TEMP_CELSIUS, \
    CONCENTRATION_PARTS_PER_MILLION, \
    CONCENTRATION_PARTS_PER_BILLION, PRESSURE_MBAR, VOLUME_CUBIC_METERS, \
    DEVICE_CLASS_HUMIDITY, \
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_PRESSURE, DEVICE_CLASS_ILLUMINANCE, \
    DEVICE_CLASS_TIMESTAMP

DOMAIN = 'airthings'
MANUFACTURER = "Airthings"
OAUTH2_AUTHORIZE = "https://accounts.airthings.com/authorize"
OAUTH2_TOKEN = "https://accounts-api.airthings.com/v1/token"
API_URL = "https://ext-api.airthings.com/v1"
SCAN_INTERVAL = timedelta(minutes=5)
CONF_ORGANIZATION_ID = "organization_id"


class AirthingsSensorType:
    def __init__(self, name, icon, unit=None, device_class=None):
        self.name = name
        self.unit = unit
        self.icon = icon
        self.device_class = device_class


SENSOR_TYPES = dict(
    humidity=AirthingsSensorType('Humidity', "mdi:water-percent", UNIT_PERCENTAGE,
                                 DEVICE_CLASS_HUMIDITY),
    temp=AirthingsSensorType('Temperature', "mdi:thermometer", TEMP_CELSIUS,
                             DEVICE_CLASS_TEMPERATURE),
    co2=AirthingsSensorType('CO2', "mdi:molecule-co2",
                            CONCENTRATION_PARTS_PER_MILLION),
    voc=AirthingsSensorType('TVOC', "mdi:chemical-weapon",
                            CONCENTRATION_PARTS_PER_BILLION),
    pressure=AirthingsSensorType('Pressure', "mdi:gauge", PRESSURE_MBAR,
                                 DEVICE_CLASS_PRESSURE),
    radonShortTermAvg=AirthingsSensorType('Radon Short term average', "mdi:atom",
                                          f"Bq/{VOLUME_CUBIC_METERS} 24h avg"),
    light=AirthingsSensorType('Light level', "mdi:white-balance-sunny", UNIT_PERCENTAGE,
                              DEVICE_CLASS_ILLUMINANCE),
    time=AirthingsSensorType('Last synced', "mdi:clock",
                             device_class=DEVICE_CLASS_TIMESTAMP),
)
