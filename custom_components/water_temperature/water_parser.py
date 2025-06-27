"""Water temperature parser for Home Assistant integration."""
import aiohttp
import asyncio
import re
import logging
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup

from .const import DEFAULT_URL

_LOGGER = logging.getLogger(__name__)


class WaterTemperatureParser:
    """Parser for water temperature data."""

    def __init__(self, url: Optional[str] = None):
        """Initialize the parser."""
        self.url = url or DEFAULT_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def get_temperature(self) -> Optional[float]:
        """Get current water temperature (synchronous version for compatibility)."""
        try:
            import requests
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self._parse_temperature(response.text)
        except Exception as e:
            _LOGGER.error("Error fetching temperature: %s", e)
            return None

    async def async_get_temperature(self) -> Optional[float]:
        """Get current water temperature asynchronously."""
        try:
            async with aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    text = await response.text()
                    return self._parse_temperature(text)
        except Exception as e:
            _LOGGER.error("Error fetching temperature: %s", e)
            return None

    async def async_get_detailed_info(self) -> Optional[Dict[str, Any]]:
        """Get detailed water temperature information asynchronously."""
        try:
            async with aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    text = await response.text()
                    return self._parse_detailed_info(text)
        except Exception as e:
            _LOGGER.error("Error fetching detailed info: %s", e)
            return None

    def _parse_temperature(self, text: str) -> Optional[float]:
        """Parse temperature from HTML text."""
        try:
            soup = BeautifulSoup(text, 'html.parser')
            
            # Try different parsing strategies
            temp_element = soup.find('h3', class_='temperature-now')
            if temp_element:
                temp_text = temp_element.get_text(strip=True)
                temp_match = re.search(r'(\d+\.?\d*)°C', temp_text)
                if temp_match:
                    return float(temp_match.group(1))
            
            # Alternative parsing
            text_content = soup.get_text()
            
            # Search for temperature patterns
            temp_patterns = [
                r'температура воды.*?составляет\s+(\d+\.?\d*)°C',
                r'Температура воды.*?(\d+\.?\d*)°C',
                r'прямо сейчас.*?(\d+\.?\d*)°C',
                r'данные обновлены.*?(\d+\.?\d*)°C'
            ]
            
            for pattern in temp_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    return float(match.group(1))
            
            # Find all temperatures and return the first reasonable one
            all_temps = re.findall(r'(\d+\.?\d*)°C', text_content)
            if all_temps:
                for temp in all_temps:
                    temp_val = float(temp)
                    if 0 <= temp_val <= 40:  # Reasonable range for water temperature
                        return temp_val
            
            return None
            
        except Exception as e:
            _LOGGER.error("Error parsing temperature: %s", e)
            return None

    def _parse_detailed_info(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse detailed information from HTML text."""
        try:
            soup = BeautifulSoup(text, 'html.parser')
            text_content = soup.get_text()
            
            # Try to extract location from page title or content
            location = self._extract_location(soup, text_content)
            
            info = {
                'current_temperature': None,
                'yesterday_temperature': None,
                'week_ago_temperature': None,
                'trend': None,
                'air_temperature': None,
                'last_updated': None,
                'location': location
            }
            
            # Current temperature
            current_temp = self._parse_temperature(text)
            if current_temp:
                info['current_temperature'] = current_temp
            
            # Yesterday temperature
            yesterday_match = re.search(r'вчера:\s*(\d+\.?\d*)°C', text_content, re.IGNORECASE)
            if yesterday_match:
                info['yesterday_temperature'] = float(yesterday_match.group(1))
            
            # Week ago temperature
            week_match = re.search(r'неделю назад:\s*(\d+\.?\d*)°C', text_content, re.IGNORECASE)
            if week_match:
                info['week_ago_temperature'] = float(week_match.group(1))
            
            # Trend
            trend_match = re.search(r'Тенденция:\s*([а-яё\s]+)', text_content, re.IGNORECASE)
            if trend_match:
                info['trend'] = trend_match.group(1).strip()
            
            # Air temperature
            air_temp_match = re.search(r'температура воздуха.*?достигнет\s+(\d+)°C', text_content, re.IGNORECASE)
            if air_temp_match:
                info['air_temperature'] = int(air_temp_match.group(1))
            
            # Last updated
            updated_match = re.search(r'данные обновлены\s+(\d+)\s+минут назад', text_content, re.IGNORECASE)
            if updated_match:
                info['last_updated'] = f"{updated_match.group(1)} минут назад"
            
            return info
            
        except Exception as e:
            _LOGGER.error("Error parsing detailed info: %s", e)
            return None

    def _extract_location(self, soup: BeautifulSoup, text_content: str) -> str:
        """Extract location from page content."""
        try:
            # Try to get location from title
            title = soup.find('title')
            if title:
                title_text = title.get_text()
                # Look for patterns like "Температура воды в Городе"
                location_match = re.search(r'в\s+([А-Яа-яё\s\-]+?)\s+в', title_text)
                if location_match:
                    return location_match.group(1).strip()
                
                # Alternative pattern
                location_match = re.search(r'Температура.*?в\s+([А-Яа-яё\s\-]+)', title_text)
                if location_match:
                    city = location_match.group(1).strip()
                    # Clean up common suffixes
                    city = re.sub(r'\s+(в\s+.*|сегодня|сейчас).*$', '', city, flags=re.IGNORECASE)
                    return city
            
            # Try to get location from h1 or h2 headers
            for header_tag in ['h1', 'h2']:
                header = soup.find(header_tag)
                if header:
                    header_text = header.get_text()
                    # Look for city name in header
                    location_match = re.search(r'в\s+([А-Яа-яё\s\-]+)', header_text)
                    if location_match:
                        city = location_match.group(1).strip()
                        # Clean up
                        city = re.sub(r'\s+(сегодня|сейчас).*$', '', city, flags=re.IGNORECASE)
                        return city
            
            # Try to extract from URL
            if 'russia' in self.url:
                url_parts = self.url.split('/')
                for part in url_parts:
                    if '-russia-' in part or '-krasnodarskiy-' in part:
                        city_part = part.split('-')[0]
                        if city_part and len(city_part) > 2:
                            return city_part.replace('-', ' ').title()
            
            # Fallback - try to find city name in text
            city_patterns = [
                r'([А-Яа-яё]+),\s*Россия',
                r'в\s+городе\s+([А-Яа-яё]+)',
                r'Температура\s+воды\s+в\s+([А-Яа-яё\s]+?)\s+составляет'
            ]
            
            for pattern in city_patterns:
                match = re.search(pattern, text_content)
                if match:
                    city = match.group(1).strip()
                    # Clean up common suffixes
                    city = re.sub(r'\s+(в\s+.*|сегодня|сейчас).*$', '', city, flags=re.IGNORECASE)
                    return city
            
            return "Неизвестное местоположение"
            
        except Exception as e:
            _LOGGER.error("Error extracting location: %s", e)
            return "Неизвестное местоположение" 