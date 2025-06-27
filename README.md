# Water Temperature - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/futuro135/water_temperature_hacs.svg)](https://github.com/futuro135/water_temperature_hacs/releases)
[![License](https://img.shields.io/github/license/futuro135/water_temperature_hacs.svg)](LICENSE)

Универсальная интеграция для Home Assistant, которая получает актуальную температуру воды для любого города с сайта [seatemperature.ru](https://seatemperature.ru). Поддерживает все города России и мира, представленные на сайте.

## Возможности

- 🌍 **Поддержка любого города** - настройка через URL с сайта seatemperature.ru
- 🌡️ **Текущая температура воды** - основной сенсор с температурой воды
- 📊 **Дополнительные атрибуты**:
  - Температура воды вчера
  - Температура воды неделю назад
  - Тенденция изменения температуры
  - Температура воздуха
  - Время последнего обновления данных
  - Автоматическое определение местоположения
- ⚙️ **Настраиваемый интервал обновления** (от 5 до 1440 минут)
- 🔄 **Асинхронное обновление данных**
- 🎯 **Полная интеграция с Home Assistant**
- 🏷️ **Автоматическое именование сенсоров** по названию города

## Установка через HACS

### Способ 1: Автоматическая установка (рекомендуется)

1. Убедитесь, что у вас установлен [HACS](https://hacs.xyz/)
2. Перейдите в HACS → Integrations
3. Нажмите на три точки в правом верхнем углу → Custom repositories
4. Добавьте URL этого репозитория: `https://github.com/futuro135/water_temperature_hacs`
5. Выберите категорию "Integration"
6. Найдите "Water Temperature Uglich" в списке и установите
7. Перезапустите Home Assistant

### Способ 2: Ручная установка

1. Скачайте папку `custom_components/water_temperature`
2. Скопируйте её в директорию `custom_components` вашего Home Assistant
3. Перезапустите Home Assistant

## Настройка

1. Перейдите в Settings → Devices & Services
2. Нажмите "Add Integration"
3. Найдите "Water Temperature"
4. Заполните настройки:
   - **City URL**: URL страницы города с сайта seatemperature.ru (например: `https://seatemperature.ru/current/russia/uglich-russia-sea-temperature`)
   - **City Name**: Название города (например: "Углич")
   - **Update interval**: Интервал обновления в минутах (по умолчанию 30)
5. Нажмите "Submit"

### Как найти URL города

1. Перейдите на [seatemperature.ru](https://seatemperature.ru)
2. Найдите ваш город через поиск или карту
3. Скопируйте URL страницы города
4. Вставьте его в поле "City URL" при настройке интеграции

**Примеры URL:**
- Углич: `https://seatemperature.ru/current/russia/uglich-russia-sea-temperature`
- Сочи: `https://seatemperature.ru/current/russia/sochi-krasnodarskiy-russia-sea-temperature`
- Анапа: `https://seatemperature.ru/current/russia/anapa-krasnodarskiy-russia-sea-temperature`

📋 **Больше примеров URL**: См. файл [CITIES_EXAMPLES.md](CITIES_EXAMPLES.md) для полного списка популярных городов России и мира.

📝 **История изменений**: См. файл [CHANGELOG.md](CHANGELOG.md) для подробной информации о всех обновлениях.

## Использование

После установки и настройки в Home Assistant появится сенсор:

- **Сенсор**: `sensor.water_temperature_[город]` (например: `sensor.water_temperature_углич`)
- **Атрибуты**:
  - `yesterday_temperature` - температура вчера
  - `week_ago_temperature` - температура неделю назад
  - `trend` - тенденция изменения
  - `air_temperature` - температура воздуха
  - `last_updated` - время последнего обновления
  - `location` - автоматически определенное местоположение

### Пример использования в автоматизации

```yaml
automation:
  - alias: "Уведомление о температуре воды"
    trigger:
      - platform: numeric_state
        entity_id: sensor.water_temperature_углич  # замените на ваш город
        above: 20
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Температура воды поднялась выше 20°C: {{ states('sensor.water_temperature_углич') }}°C"
```

### Пример карточки в Lovelace

```yaml
type: entities
title: Температура воды  # название будет автоматически подставлено
entities:
  - entity: sensor.water_temperature_углич  # замените на ваш город
    name: Текущая температура
    icon: mdi:thermometer-water
  - type: attribute
    entity: sensor.water_temperature_углич
    attribute: yesterday_temperature
    name: Вчера
    suffix: "°C"
  - type: attribute
    entity: sensor.water_temperature_углич
    attribute: week_ago_temperature
    name: Неделю назад
    suffix: "°C"
  - type: attribute
    entity: sensor.water_temperature_углич
    attribute: trend
    name: Тенденция
  - type: attribute
    entity: sensor.water_temperature_углич
    attribute: air_temperature
    name: Температура воздуха
    suffix: "°C"
```

## Поддержка

Если у вас возникли проблемы или есть предложения по улучшению, создайте [issue](https://github.com/futuro135/water_temperature_hacs/issues) в этом репозитории.

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## Благодарности

- Сайт [seatemperature.ru](https://seatemperature.ru/) за предоставление данных о температуре воды
- Сообщество Home Assistant за отличную платформу автоматизации дома 