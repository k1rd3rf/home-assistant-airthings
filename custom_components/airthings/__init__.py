import asyncio
import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.config_entry_oauth2_flow import LocalOAuth2Implementation, \
    async_get_config_entry_implementation
from homeassistant.util import Throttle
from requests import HTTPError

from .api import AirthingsApi
from .config_flow import OAuth2FlowHandler
from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, SCAN_INTERVAL, \
    CONF_ORGANIZATION_ID

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Optional(CONF_ORGANIZATION_ID): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data[DOMAIN] = {
        CONF_ORGANIZATION_ID: config[DOMAIN].get(CONF_ORGANIZATION_ID)
    }

    if DOMAIN not in config:
        return True

    implementation = LocalOAuth2Implementation(hass,
                                               DOMAIN,
                                               config[DOMAIN][CONF_CLIENT_ID],
                                               config[DOMAIN][CONF_CLIENT_SECRET],
                                               OAUTH2_AUTHORIZE,
                                               OAUTH2_TOKEN
                                               )
    OAuth2FlowHandler.async_register_implementation(hass, implementation)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    implementation = await async_get_config_entry_implementation(hass, entry)
    hass.data[DOMAIN][entry.entry_id] = AirthingsApi(hass, entry, implementation)

    await initialize_locations(hass, entry)

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


@Throttle(SCAN_INTERVAL)
async def initialize_locations(hass, entry):
    """Update all the devices."""
    a_api = hass.data[DOMAIN][entry.entry_id]
    try:
        await hass.async_add_executor_job(a_api.update_locations)
        for location in a_api.locations:
            await hass.async_add_executor_job(location.initialize)
    except HTTPError as err:
        _LOGGER.warning("Cannot update devices: %s", err.response.status_code)
