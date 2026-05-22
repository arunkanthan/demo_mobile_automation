# Quick start and development commands

.PHONY: help setup install clean test test-ios test-android test-smoke test-regression test-bdd allure-report

help:
	@echo "Mobile Automation Framework - Available Commands"
	@echo "================================================"
	@echo "make setup              - Initial setup (venv + dependencies)"
	@echo "make install            - Install dependencies only"
	@echo "make clean              - Clean test artifacts and cache"
	@echo "make test               - Run all tests"
	@echo "make test-ios           - Run iOS tests only"
	@echo "make test-android       - Run Android tests only"
	@echo "make test-smoke         - Run smoke tests"
	@echo "make test-regression    - Run regression tests"
	@echo "make test-bdd           - Run BDD feature tests"
	@echo "make allure-report      - Generate and serve Allure report"
	@echo "make appium-start       - Start Appium server"
	@echo "make lint               - Run code quality checks"

setup: 
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	cp .env.example .env
	@echo "Setup complete! Edit .env file with your device configuration"

install:
	pip install -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf reports/allure-results
	rm -rf reports/screenshots
	rm -rf reports/logs
	@echo "Cleanup complete"

test:
	pytest -v --alluredir=reports/allure-results

test-ios:
	pytest -v --platform=ios --alluredir=reports/allure-results

test-android:
	pytest -v --platform=android --alluredir=reports/allure-results

test-smoke:
	pytest -m smoke -v --alluredir=reports/allure-results

test-regression:
	pytest -m regression -v --alluredir=reports/allure-results

test-bdd:
	pytest features/ -v --alluredir=reports/allure-results

allure-report: test
	allure serve reports/allure-results

appium-start:
	appium


android-setup:
	@echo "Running Android SDK + AVD setup helper"
	./scripts/android_setup.sh


android-emulator-start:
	@echo "Start emulator: pass optional AVD name, default 'test_avd'"
	$(ANDROID_SDK_ROOT)/emulator/emulator -avd ${AVD_NAME:-test_avd} &

lint:
	@echo "Running code quality checks..."
	pylint steps/ pages/ config/ utils/ --disable=all --enable=E,F 2>/dev/null || true

.DEFAULT_GOAL := help
