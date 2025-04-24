"""Nox sessions."""

import tempfile
from pathlib import Path

import nox
import nox_poetry
from nox_poetry.sessions import Session

package = "imgvisint"
# nox.options.sessions = "formatter", "linter", "mypy", "pytype", "tests"
locations = "tests", "noxfile.py", "models"


@nox_poetry.session(python="3.11")
def formatter(session: Session) -> None:
    """Run ruff code formatter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)


@nox_poetry.session(python="3.11")
def pytest(session: Session) -> None:
    """Run tests with pytest."""
    session.install(".", "pytest", "pytest-cov")

    session.run(
        "pytest",
        "-v",
        "--cov=models",
        "--cov-report=term-missing",
        *session.posargs,
        "tests",
    )


@nox_poetry.session(python=["3.11"])
def linter(session: Session) -> None:
    """Lint using ruff."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", "--fix", *args)


@nox_poetry.session(python="3.11")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@nox_poetry.session(python=["3.11"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.install(".", "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox_poetry.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")
