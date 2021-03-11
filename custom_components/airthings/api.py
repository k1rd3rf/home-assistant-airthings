import logging
from asyncio import run_coroutine_threadsafe
from datetime import timezone, datetime
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from homeassistant.util import Throttle
from oauthlib.oauth2 import TokenExpiredError
from requests import Response
from requests_oauthlib import OAuth2Session as RequestOAuth2Session
from urllib.parse import urlencode

from homeassistant import config_entries, core
from .const import API_URL, SCAN_INTERVAL, DOMAIN, CONF_ORGANIZATION_ID

_LOGGER = logging.getLogger(__name__)


class AirthingsError(Exception):
    pass


class AirthingsApi:
    def __init__(
            self,
            hass: core.HomeAssistant,
            config_entry: config_entries.ConfigEntry,
            implementation: config_entry_oauth2_flow.AbstractOAuth2Implementation,
    ):
        self.hass = hass
        self.config_entry = config_entry
        self.session = OAuth2Session(hass, config_entry, implementation)
        self._oauth = RequestOAuth2Session(token=self.session.token)
        self.organization_id = hass.data[DOMAIN].get(CONF_ORGANIZATION_ID, None)
        self.locations = []
        self.devices = []

    def _refresh_tokens(self) -> dict:
        """Refresh and return new tokens using Home Assistant OAuth2 session."""
        run_coroutine_threadsafe(
            self.session.async_ensure_token_valid(), self.hass.loop
        ).result()

        return self.session.token

    def _request(self, method: str, path: str, **kwargs) -> Response:
        """Make a request."""
        parameters = urlencode({'organizationId': self.organization_id}) \
            if self.organization_id is not None else ""
        url = f"{API_URL}/{path}?%s" % parameters
        try:
            return getattr(self._oauth, method)(url, **kwargs)
        except TokenExpiredError:
            _LOGGER.warning("Token expired.")
            self._oauth.token = self._refresh_tokens()

            return getattr(self._oauth, method)(url, **kwargs)

    def _get(self, endpoint):
        """Get data as dictionary from an endpoint."""
        res = self._request("get", endpoint)
        if not res.content:
            return {}
        try:
            res = res.json()
        except ValueError:
            raise ValueError("Cannot parse {} as JSON".format(res))
        if "error" in res:
            raise AirthingsError(res["error"])
        return res

    def _get_locations(self):
        """Return a list of `AirthingsLocation` instances for all location."""
        data = self._get("/locations")
        if "locations" not in data:
            _LOGGER.error("Did not find locations")
            raise AirthingsError(data)
        return [AirthingsLocation(d, self) for d in data["locations"]]

    def update_locations(self):
        self.locations = self._get_locations()

    def get_location_devices(self, location):
        data = self._get("/locations/{}".format(location.location_id))
        if "devices" not in data:
            _LOGGER.error("Did not find devices on location_id %s", location.id)
            raise AirthingsError(data)

        devices = dict()
        for d in data["devices"]:
            device = AirthingsDevice(d, location)
            devices[device.device_id] = device
        return devices

    def get_location_samples(self, location_id: str):
        data = self._get("/locations/{}/latest-samples".format(location_id))
        if "devices" not in data:
            _LOGGER.error("Did not find devices on location_id %s", location_id)
            raise AirthingsError(data)

        _LOGGER.debug("Received latest samples for location (%s): %s", location_id,
                      data["devices"])
        samples = dict()
        for d in data["devices"]:
            device_id = d.get('id')
            samples[device_id] = d.get('data', dict())

        return samples


class AirthingsLocation:
    def __init__(self, data, api: AirthingsApi):
        self._id = data.get('id')
        self._samples = dict()
        self._api = api
        self.name = data.get('name')
        self.labels = data.get('labels', dict())
        self.devices = dict()

    def initialize(self):
        self.devices = self._api.get_location_devices(self)
        self.update_devices()

    @Throttle(SCAN_INTERVAL)
    def update_devices(self):
        self._samples = self._api.get_location_samples(self.location_id)
        for d_id in self._samples:
            samples = self._samples.get(d_id)
            if d_id not in self.devices:
                _LOGGER.warning("Device not created for %s, but got data: %s", d_id,
                                samples)
                continue
            self.devices.get(d_id).data = samples

    @property
    def location_id(self):
        return self._id

    def __repr__(self):
        return "AirthingsLocation(id={}, name={}, labels={}, devices={})".format(
            self._id,
            self.name,
            self.labels,
            self.devices,
        )


class AirthingsDevice:
    def __init__(self, data, location: AirthingsLocation):
        self._id = data.get('id')
        self._segment = AirthingsDeviceSegment(data.get('segment'))
        self._location = location
        self._data = dict()
        self.device_type = data.get('deviceType', 'UNKNOWN')

    def __repr__(self):
        return "AirthingsDevice(id={}, type={}, name={}, location={}, data={})".format(
            self._id,
            self.device_type,
            self.name,
            self.location_name,
            self.data,
        )

    @property
    def device_id(self):
        return self._id

    @property
    def name(self):
        return self._segment.name

    @property
    def location_name(self):
        return self._location.name

    @property
    def last_synced(self):
        d = self._data.get('time', None)
        return datetime.fromtimestamp(d, timezone.utc).isoformat() \
            if d is not None else None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data=None):
        if data is None:
            data = dict()
        self._data = data

    def update_location(self):
        self._location.update_devices()


class AirthingsDeviceSegment:
    def __init__(self, data):
        self._id = data.get('id')
        self.name = data.get('name')

    def __repr__(self):
        return "AirthingsDeviceSegment(id={}, name='{}')".format(
            self._id,
            self.name,
        )
