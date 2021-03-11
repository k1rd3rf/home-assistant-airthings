from datetime import timedelta

from homeassistant.const import PERCENTAGE, TEMP_CELSIUS, \
    CONCENTRATION_PARTS_PER_MILLION, \
    CONCENTRATION_PARTS_PER_BILLION, PRESSURE_MBAR, DEVICE_CLASS_HUMIDITY, \
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_PRESSURE, DEVICE_CLASS_ILLUMINANCE, \
    DEVICE_CLASS_TIMESTAMP, VOLUME_CUBIC_METERS

DOMAIN = "airthings"
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
    humidity=AirthingsSensorType(
        name="Humidity",
        icon="mdi:water-percent",
        field="humidity",
        unit=PERCENTAGE,
        device_class=DEVICE_CLASS_HUMIDITY,
    ),
    temp=AirthingsSensorType(
        name="Temperature",
        icon="mdi:thermometer",
        field="temp",
        unit=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    co2=AirthingsSensorType(
        name="CO2",
        icon="mdi:molecule-co2",
        field="co2",
        unit=CONCENTRATION_PARTS_PER_MILLION,
    ),
    voc=AirthingsSensorType(
        name="VOC",
        icon="mdi:chemical-weapon",
        field="voc",
        unit=CONCENTRATION_PARTS_PER_BILLION,
    ),
    pressure=AirthingsSensorType(
        name="Pressure",
        icon="mdi:gauge",
        field="pressure",
        unit=PRESSURE_MBAR,
        device_class=DEVICE_CLASS_PRESSURE,
    ),
    light=AirthingsSensorType(
        name="Light level",
        icon="mdi:white-balance-sunny",
        field="light",
        unit=PERCENTAGE,
        device_class=DEVICE_CLASS_ILLUMINANCE,
    ),
    radonShortTermAvg=AirthingsSensorType(
        name="Radon Short term average",
        icon="mdi:atom",
        field="radonShortTermAvg",
        unit=f"Bq/{VOLUME_CUBIC_METERS} 24h avg",
    ),
    mold=AirthingsSensorType(
        name="Mold risk indicator",
        icon="mdi:mushroom-outline",
        field="mold",
        unit="/ 10",
    ),
    virusRisk=AirthingsSensorType(
        name="Virus risk indicator",
        icon="mdi:virus-outline",
        field="virusRisk",
        unit="/ 10",
    ),
    time=AirthingsSensorType(
        name="Last synced",
        icon="mdi:clock",
        field="time",
        device_class=DEVICE_CLASS_TIMESTAMP,
    ),
)


def get_airthings_sensor_type(field_name):
    return SENSOR_TYPES[field_name] \
        if field_name in SENSOR_TYPES \
        else AirthingsSensorType(field_name, "mdi:unknown", field_name)
