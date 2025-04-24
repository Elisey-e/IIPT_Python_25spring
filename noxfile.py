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


"""Working"""
# @nox_poetry.session(python="3.11")
# def safety(session: Session) -> None:
#     """Scan dependencies for insecure packages."""
#     with tempfile.TemporaryDirectory() as d, (Path(d) / "requirements.txt").open("w") as reqs:
#         # Генерируем requirements.txt, включая только main-зависимости
#         session.run(
#             "poetry",
#             "run",  # Запускаем через poetry run, чтобы использовать текущее окружение
#             "pip",
#             "freeze",
#             "--exclude-editable",  # Исключаем editable-пакеты (если есть)
#             external=True,
#             stdout=reqs,  # Перенаправляем вывод в файл
#         )
#         session.install("safety")
#         session.run("safety", "scan", f"--file={reqs.name}", "--full-report")


"""Working"""
# @nox_poetry.session(python="3.11")
# def pytype(session: Session) -> None:
#     """Type-check using pytype."""
#     args = session.posargs or ["--disable=import-error", *locations]
#     session.install("pytype")
#     session.run("pytype", *args)


# @nox_poetry.session(python=["3.11"])
# def tests(session: Session) -> None:
#     """Run the test suite."""
#     args = session.posargs or ["--cov", "-m", "not e2e"]
#     session.run("poetry", "install", "--only=main", external=True)
#     session.install("coverage[toml]", "pytest", "pytest-cov", "pytest-mock")
#     session.run("pytest", *args)


# @nox_poetry.session(python=["3.11"])
# def typeguard(session: Session) -> None:
#     """Runtime type checking using Typeguard."""
#     args = session.posargs or ["-m", "not e2e"]
#     session.run("poetry", "install", "--only=main", external=True)
#     session.install("pytest", "pytest-mock", "typeguard")
#     session.run("pytest", f"--typeguard-packages={package}", *args)


# @nox_poetry.session(python=["3.11"])
# def xdoctest(session: Session) -> None:
#     """Run examples with xdoctest."""
#     args = session.posargs or ["all"]
#     session.run("poetry", "install", "--only=main", external=True)
#     session.install("xdoctest")
#     session.run("python", "-m", "xdoctest", package, *args)


@nox_poetry.session(python="3.11")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox_poetry.session(python="3.11")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")
