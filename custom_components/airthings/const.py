from datetime import timedelta

from homeassistant.const import PERCENTAGE, TEMP_CELSIUS, \
    CONCENTRATION_PARTS_PER_MILLION, \
    CONCENTRATION_PARTS_PER_BILLION, PRESSURE_MBAR, DEVICE_CLASS_HUMIDITY, \
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_PRESSURE, DEVICE_CLASS_ILLUMINANCE, \
    DEVICE_CLASS_TIMESTAMP, VOLUME_CUBIC_METERS

DOMAIN = 'airthings'
MANUFACTURER = "Airthings"
OAUTH2_AUTHORIZE = "https://accounts.airthings.com/authorize"
OAUTH2_TOKEN = "https://accounts-api.airthings.com/v1/token"
API_URL = "https://ext-api.airthings.com/v1"
SCAN_INTERVAL = timedelta(minutes=5)
CONF_ORGANIZATION_ID = "organization_id"


class AirthingsSensorType:
    def __init__(self, name, icon, field, unit=None, device_class=None):
        self.name = name
        self.unit = unit
        self.icon = icon
        self.device_class = device_class
        self.field = field


SENSOR_TYPES = dict(
    humidity=AirthingsSensorType('Humidity', "mdi:water-percent", 'humidity',
                                 PERCENTAGE, DEVICE_CLASS_HUMIDITY),
    temp=AirthingsSensorType('Temperature', "mdi:thermometer", 'temp', TEMP_CELSIUS,
                             DEVICE_CLASS_TEMPERATURE),
    co2=AirthingsSensorType('CO2', "mdi:molecule-co2", 'co2',
                            CONCENTRATION_PARTS_PER_MILLION),
    voc=AirthingsSensorType('TVOC', "mdi:chemical-weapon", 'voc',
                            CONCENTRATION_PARTS_PER_BILLION),
    pressure=AirthingsSensorType('Pressure', "mdi:gauge", 'pressure', PRESSURE_MBAR,
                                 DEVICE_CLASS_PRESSURE),
    light=AirthingsSensorType('Light level', "mdi:white-balance-sunny", 'light',
                              PERCENTAGE, DEVICE_CLASS_ILLUMINANCE),
    radonShortTermAvg=AirthingsSensorType('Radon Short term average', "mdi:atom",
                                          'radonShortTermAvg',
                                          f"Bq/{VOLUME_CUBIC_METERS} 24h avg"),
    mold=AirthingsSensorType('Mold risk indicator', 'mdi:mushroom-outline', 'mold', '/ 10'),
    virusRisk=AirthingsSensorType('Virus risk indicator', 'mdi:virus-outline', 'virusRisk', '/ 10'),
    time=AirthingsSensorType('Last synced', "mdi:clock", 'time',
                             device_class=DEVICE_CLASS_TIMESTAMP),
)


def get_airthings_sensor_type(field_name):
    return SENSOR_TYPES[field_name] \
        if field_name in SENSOR_TYPES \
        else AirthingsSensorType(field_name, "mdi:unknown", field_name)
