from sqlite3 import Connection
import pytest
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_path():
    return (
        project_root /
        "python-package" /
        "employee_events" /
        "employee_events.db"
        )


def test_db_exists(db_path: Path):
    assert db_path.is_file()
    assert (
        db_path
        == project_root /
        "python-package" /
        "employee_events" /
        "employee_events.db"
    )


@pytest.fixture
def db_conn(db_path: Path):
    from sqlite3 import connect

    return connect(db_path)


@pytest.fixture
def table_names(db_conn: Connection):
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    assert "employee" in table_names


def test_team_table_exists(table_names):
    assert "team" in table_names


def test_employee_events_table_exists(table_names):
    assert "employee_events" in table_names
