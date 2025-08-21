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
- IDEs such as PyCharm and VSCode automatically recognize Gherkin syntax and provide clickable links from steps in feature files to their corresponding step definitions, simplifying navigation and development.

## Configurations
- Configuration settings are stored in the `config` directory.
- The `config.py` file contains the main configuration settings for the tests.
- You can modify the configuration settings as needed, such as changing:
  - browser screen_resolution
  - global timeout
  - services URLs
  - authentication credentials
  - etc.

NOTE: `se_grid.yml` is used for running UI tests in parallel across multiple browsers and devices using Selenium Grid(local or in the cloud).


## Running Tests

- To run all tests with pytest:
  ```sh
  pytest tests.py
  ```
  or using the Makefile:
  ```sh
  make run_all_test
  ```

- Additionally, you can run tests with specific tags:
  ```sh
  pytest tests.py -m="control-up and smoke"
  ```
  or using the Makefile:
  ```sh
  make run_smoke_test
  ```

- to run tests in parallel `pytest-xdist` plugin is used:
  ```sh
  pytest -n auto tests.py
  ```

Output example:
```sh
(.pyvenv) ctrlup-aht ➜ git:(develop) ➜ pytest -n auto tests.py
============================ test session starts ============================
platform darwin -- Python 3.13.7, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/svarogrud/Projects/ctrlup-aht
configfile: pytest.ini
plugins: allure-pytest-bdd-2.15.0, xdist-3.8.0, bdd-8.1.0
10 workers [5 items]      
scheduling tests via LoadScheduling

tests.py::test_verify_distance_between_airports 
tests.py::test_verify_airport_count 
tests.py::test_verify_specific_airports 
tests.py::test_add_item_to_cart 
tests.py::test_verify_inventory_items 
[gw2] [ 20%] PASSED tests.py::test_verify_distance_between_airports 
[gw0] [ 40%] PASSED tests.py::test_verify_airport_count 
[gw1] [ 60%] PASSED tests.py::test_verify_specific_airports 
[gw4] [ 80%] PASSED tests.py::test_add_item_to_cart 
[gw3] [100%] PASSED tests.py::test_verify_inventory_items 

============================ 5 passed in 6.02s ============================
```

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
  
Note: allure tool must be installed on your system. You can install it using Homebrew on macOS:
  ```sh
  brew install allure
  ```
  or using apt on Ubuntu:
  ```sh
  apt-get install allure
  ```
