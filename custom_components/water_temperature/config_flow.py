"""Config flow for Water Temperature integration."""
import logging
import voluptuous as vol
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN, 
    NAME, 
    CONF_UPDATE_INTERVAL, 
    CONF_CITY_URL, 
    CONF_CITY_NAME,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_URL,
    DEFAULT_CITY_NAME,
    SEATEMPERATURE_DOMAIN
)
from .water_parser import WaterTemperatureParser

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_CITY_URL, default=DEFAULT_URL): str,
    vol.Required(CONF_CITY_NAME, default=DEFAULT_CITY_NAME): str,
    vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(
        vol.Coerce(int), vol.Range(min=5, max=1440)
    ),
})


async def validate_input(hass: HomeAssistant, data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the user input allows us to connect."""
    
    # Validate URL
    city_url = data.get(CONF_CITY_URL, "")
    city_name = data.get(CONF_CITY_NAME, "")
    
    if not city_url:
        raise InvalidURL
    
    # Check if URL is from seatemperature.ru
    parsed_url = urlparse(city_url)
    if SEATEMPERATURE_DOMAIN not in parsed_url.netloc:
        raise InvalidURL
    
    # Test the connection
    parser = WaterTemperatureParser(city_url)
    
    try:
        temperature = await hass.async_add_executor_job(parser.get_temperature)
        if temperature is None:
            raise CannotConnect
    except Exception:
        raise CannotConnect
    
    return {"title": f"{NAME} - {city_name}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Water Temperature Uglich."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidURL:
                errors["base"] = "invalid_url"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidURL(HomeAssistantError):
    """Error to indicate invalid URL."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth.""" 