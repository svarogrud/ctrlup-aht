# ControlUP - Automation Home Test

## Setup

1. Create a Python virtual environment:
   ```sh
   bash create_venv.sh
   ```
   Or manually:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Test Scenarios and Steps definitions

- Test Scenarios are written in Gherkin format
- The test scenarios are located in the `features` directory.
- Each scenario is defined in a `.feature` file.
- The step definitions are implemented in the `step_defs` directory, which contains Python files that map Gherkin steps
  to Python functions.
- Use tags to filter scenarios when running tests. For example, to run only scenarios tagged with `@smoke`:
  ```sh
  pytest -m smoke
  ```
- `tests.py` module glues the feature files and step definitions together, allowing you to run all tests in one go.

## Running Tests

- To run all tests with pytest:
  ```sh
  pytest tests.py
  ```

- Alternatively, you can use the Makefile:
  ```sh
  make run_test
  ```

- Test configuration is managed in `pytest.ini`.

## Reporting

- Use allure for reporting - add the `--alluredir` option to pytest:
  ```sh
  pytest tests.py --alluredir=/tmp/allure-results
  ```
- To generate the report, run:
  ```sh
  allure serve /tmp/allure-results
  ```
- Alternatively, you can use the Makefile:
  ```sh
  make serve_reports
  ```
