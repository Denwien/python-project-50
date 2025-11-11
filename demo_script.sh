#!/bin/bash

# Проверка и установка необходимых пакетов
if ! command -v pip &> /dev/null; then
    echo "pip не найден. Устанавливаем pip..."
    apt update && apt install -y python3-pip
fi

# Обновляем pip
pip install --upgrade pip

# Установка зависимостей проекта
pip install pytest pytest-cov pyyaml

# Запуск Python
python3 --version

# Запуск тестов с покрытием
pytest --cov=gendiff tests/

