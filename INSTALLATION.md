# Инструкции по установке и развертыванию

## 🚀 Развертывание на GitHub

### 1. Создание репозитория

1. Создайте новый репозиторий на GitHub с именем `water-temperature-hacs`
2. Склонируйте его локально:
```bash
git clone https://github.com/futuro135/water_temperature_hacs.git
cd water_temperature_hacs
```

### 2. Загрузка файлов

Скопируйте все файлы из папки `water_temperature_hacs` в корень вашего репозитория:

```
water_temperature_hacs/
├── custom_components/
│   └── water_temperature/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── sensor.py
│       ├── strings.json
│       └── water_parser.py
├── hacs.json
├── README.md
├── LICENSE
├── .gitignore
└── INSTALLATION.md
```

### 3. Обновление ссылок

Обновите следующие файлы, заменив `yourusername` на ваш GitHub username:

**manifest.json**:
```json
{
  "documentation": "https://github.com/yourusername/water-temperature-hacs",
  "issue_tracker": "https://github.com/yourusername/water-temperature-hacs/issues",
  "codeowners": ["@yourusername"]
}
```

**README.md**:
- Обновите все ссылки с `yourusername` на ваш username
- Обновите badges в начале файла

### 4. Коммит и пуш

```bash
git add .
git commit -m "Initial commit: Water Temperature Uglich HACS integration"
git push origin main
```

### 5. Создание релиза

1. Перейдите в ваш репозиторий на GitHub
2. Нажмите "Releases" → "Create a new release"
3. Тег версии: `v1.0.0`
4. Название релиза: `Water Temperature v1.0.0`
5. Описание: краткое описание функций
6. Нажмите "Publish release"

## 📦 Установка через HACS

### Для пользователей

1. **Добавление custom repository**:
   - Откройте HACS в Home Assistant
   - Перейдите в Integrations
   - Нажмите три точки → Custom repositories
   - URL: `https://github.com/futuro135/water_temperature_hacs`
   - Category: Integration
   - Нажмите Add

2. **Установка**:
   - Найдите "Water Temperature" в списке
   - Нажмите Install
   - Перезапустите Home Assistant

3. **Настройка**:
   - Settings → Devices & Services
   - Add Integration
   - Найдите "Water Temperature"
   - Настройте интервал обновления

## 🧪 Тестирование

### Локальное тестирование

Если у вас есть локальная установка Home Assistant для разработки:

1. Скопируйте папку `custom_components/water_temperature` в `custom_components/` вашей установки HA
2. Перезапустите Home Assistant
3. Добавьте интеграцию через UI

### Проверка парсера

Можете протестировать парсер отдельно:

```python
import asyncio
from custom_components.water_temperature.water_parser import WaterTemperatureParser

async def test_parser():
    parser = WaterTemperatureParser()
    
    # Тест синхронного метода
    temp = parser.get_temperature()
    print(f"Синхронная температура: {temp}°C")
    
    # Тест асинхронного метода
    temp_async = await parser.async_get_temperature()
    print(f"Асинхронная температура: {temp_async}°C")
    
    # Тест подробной информации
    info = await parser.async_get_detailed_info()
    print(f"Подробная информация: {info}")

# Запуск теста
asyncio.run(test_parser())
```

## 🔧 Обслуживание

### Обновление версии

1. Обновите версию в `manifest.json`
2. Обновите версию в `const.py`
3. Создайте новый релиз на GitHub

### Мониторинг ошибок

Следите за логами Home Assistant:
```
Settings → System → Logs
```

Ищите сообщения с префиксом `custom_components.water_temperature`

## 📋 Checklist для публикации

- [ ] Все файлы созданы и находятся в правильных местах
- [ ] Обновлены все ссылки на ваш GitHub username
- [ ] Создан репозиторий на GitHub
- [ ] Загружены все файлы
- [ ] Создан первый релиз
- [ ] Протестирована установка через HACS
- [ ] Проверена работа интеграции в Home Assistant
- [ ] README.md содержит актуальную информацию
- [ ] Лицензия MIT добавлена

## 🆘 Troubleshooting

### Проблема: Интеграция не появляется в HACS
- Проверьте правильность URL репозитория
- Убедитесь, что файл `hacs.json` находится в корне репозитория
- Проверьте, что создан хотя бы один релиз

### Проблема: Ошибка при установке
- Проверьте логи Home Assistant
- Убедитесь, что все зависимости указаны в `manifest.json`
- Проверьте синтаксис всех Python файлов

### Проблема: Сенсор не обновляется
- Проверьте доступность сайта seatemperature.ru
- Увеличьте интервал обновления
- Проверьте логи на наличие ошибок парсинга 