.PHONY: run_all_tests
run_all_tests: ## (Run all tests)
	pytest tests.py --alluredir=/tmp/allure-results --log-level=INFO --cfg=local


.PHONY: run_smoke_test
run_smoke_test: ## (Run tests marked with "control-up" and "smoke" tags)
	pytest tests.py -m="control-up and smoke" --alluredir=/tmp/allure-results --log-level=INFO --cfg=local


.PHONY: run_control_up_tests
run_control_up_tests: ## (Run tests marked with "control-up" tag)
	pytest tests.py -m="control-up" --alluredir=/tmp/allure-results --log-level=INFO --cfg=local


.PHONY: run_test_on_se_grid
run_test_on_se_grid: ## (Run tests marked with "control-up" tag in parallel)
	pytest tests.py -m="control-up" --alluredir=/tmp/allure-results --log-level=INFO --cfg=se_grid -n=2


.PHONY: serve_reports
serve_reports: ## (Serve allure reports)
	# Allure should be installed and available in PATH
	allure serve /tmp/allure-results
