"""Constants for the Water Temperature Uglich integration."""

DOMAIN = "water_temperature"
NAME = "Water Temperature Uglich"
VERSION = "1.0.0"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 30  # minutes

# URLs
BASE_URL = "https://seatemperature.ru/current/russia/uglich-russia-sea-temperature"

# Sensor attributes
ATTR_YESTERDAY_TEMP = "yesterday_temperature"
ATTR_WEEK_AGO_TEMP = "week_ago_temperature"
ATTR_TREND = "trend"
ATTR_AIR_TEMPERATURE = "air_temperature"
ATTR_LAST_UPDATED = "last_updated"
ATTR_LOCATION = "location"

# Default values
DEFAULT_LOCATION = "Углич, Россия" 