#!/bin/sh

mkdir -p "reports/flake8_report"
mkdir -p "reports/allure"
flake8 --config ./tests/.flake8
pytest
allure generate reports/allure -o reports/generated --single-file --clean
