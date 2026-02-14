# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

CFP Generator - A tool for building conference "Call for Papers" submissions and related messaging.

## Status

This is a new Python project. No code has been written yet.

## Development Setup

This project uses Python. When setting up:
- Create a virtual environment (`.venv/`)
- Use `pyproject.toml` for project configuration and dependencies
- Consider using `uv` or `poetry` for dependency management

## Commands

- **Install dependencies**: `pip install -e .` or `pip install streamlit`
- **Run Streamlit app**: `streamlit run app.py`
- **Run CLI version**: `python cfp_generator.py` or `cfp-generator`
- **Run tests**: `pytest test_cfp_generator.py`
- **Lint**: `ruff check .`
- **Type check**: `mypy .`

## Architecture (to be updated)

Document the high-level architecture here as the codebase develops.
