"""Helper: load the stage files (their names contain "-", so a normal
"import" line cannot be used)."""

import importlib.util
import os


def load_module(file_name):
    """Load a python file that sits in the same folder as this one."""

    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, file_name)

    module_name = os.path.splitext(file_name)[0].replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
