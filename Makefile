.PHONY: run_tests
run_tests: ## (Run tests)
	pytest tests.py -m="control-up" --alluredir=/tmp/allure-results --log-level=INFO

.PHONY: serve_reports
serve_reports: ## (Serve allure reports)
	allure serve /tmp/allure-results