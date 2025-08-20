from pytest_bdd import scenarios

from step_defs.ui_steps import *  # type:ignore
from step_defs.api_steps import *  # type:ignore

scenarios(
    "../features/ui-tests.feature",
    "../features/api-tests.feature",
)
