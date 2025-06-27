"""Constants for the Water Temperature Uglich integration."""

DOMAIN = "water_temperature"
NAME = "Water Temperature"
VERSION = "1.1.0"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"
CONF_CITY_URL = "city_url"
CONF_CITY_NAME = "city_name"
DEFAULT_UPDATE_INTERVAL = 30  # minutes

# URLs
DEFAULT_URL = "https://seatemperature.ru/current/russia/uglich-russia-sea-temperature"
DEFAULT_CITY_NAME = "Углич"

# Sensor attributes
ATTR_YESTERDAY_TEMP = "yesterday_temperature"
ATTR_WEEK_AGO_TEMP = "week_ago_temperature"
ATTR_TREND = "trend"
ATTR_AIR_TEMPERATURE = "air_temperature"
ATTR_LAST_UPDATED = "last_updated"
ATTR_LOCATION = "location"

# URL validation
SEATEMPERATURE_DOMAIN = "seatemperature.ru" 