# ==
# conftest.py
# Shared pytest fixtures for the Seamark Project 2 test suite
# ==
#
# Same idea as Project 1's conftest.py — work out the project root
# once and hand every test the folders it needs. Project 2's layout
# is flatter than Project 1's (raw_data/cleaned_data/outputs sit
# directly under the project root instead of inside a Stage1_Analytics
# folder), so the paths below are shorter, but the purpose is the same.

from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def project_root():
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def raw_data_dir(project_root):
    return project_root / "raw_data"


@pytest.fixture(scope="session")
def cleaned_data_dir(project_root):
    return project_root / "cleaned_data"


@pytest.fixture(scope="session")
def outputs_dir(project_root):
    return project_root / "outputs"
