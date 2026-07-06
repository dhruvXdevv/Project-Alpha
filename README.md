# Project Alpha

Scientific quantitative research and trading platform built with Clean Architecture and Domain-Driven Design (DDD).

Owned and maintained by **dhruvXdevv**.

---

## Vision

Project Alpha aims to provide a robust, production-grade, highly scalable system for executing scientific quantitative research and algorithmic trading. By enforcing strict separation of concerns, inward dependency flows, and high test coverage, Project Alpha ensures that research strategies can transition seamlessly and safely from historical backtesting to live execution markets.

---

## Repository Structure

The project uses a Python `src`-layout structure to isolate code under development from the testing runtime:

```text
project-alpha/
├── .github/
│   └── workflows/          # CI/CD Workflows (GitHub Actions)
├── docs/                   # ADRs, Architecture, Research, Meeting notes
├── experiments/            # Exploratory research and Jupyter notebooks
├── scripts/                # Operations, seeding, and management scripts
├── storage/                # Ingested datasets and output persistence
├── tests/                  # Unit, integration, and E2E tests
├── verification/           # Verification schemas and formal methods
└── src/
    └── alpha/              # Root package namespace
        ├── core/           # Configuration, exceptions, registries
        ├── models/         # Pure domain entities and invariants
        ├── services/       # Core service layer orchestration
        ├── strategy/       # Trading strategy interfaces
        ├── backtest/       # Historical simulator engine
        ├── analytics/      # Performance metric computation
        ├── execution/      # Infrastructure adapters (Broker/API)
        ├── risk/           # Pre- and post-trade risk gates
        ├── features/       # Feature store and engineering
        └── utils/          # Logging, math, and time helpers
```

---

## Development Setup

### Prerequisites

* Python 3.12 or newer
* Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dhruvXdevv/Project-Alpha.git
   cd Project-Alpha
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   * **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
   * **Linux/macOS**: `source .venv/bin/activate`

4. Install the package and development dependencies in editable mode:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

---

## Engineering Standards

1. **Clean Architecture**: Outward packages (infrastructure adapters like `execution`) must depend exclusively on inner packages (`models`, `services`, `strategy`). Dependency inversion must be used at all boundaries.
2. **Type Safety**: All production code must be fully type-hinted and satisfy `mypy` strict checks.
3. **Coding Standards**: Enforced by Ruff and Black.
   * Max Line Length: 100 characters.
   * Imports sorting: Enforced automatically.
4. **Validation**: Use Pydantic for input parsing, data models, and setting configurations.

---

## Branching Strategy & Versioning

* **Branching Strategy**: 
  * Use `main` directly during the foundation stage.
  * Introduce `develop` and `feature/*` branches after the foundation stage is complete.
* **Versioning Policy**: Follows Semantic Versioning (SemVer) `MAJOR.MINOR.PATCH` pattern.

---

## Project Status & Roadmap

### Current Status
* **Phase**: Milestone 0 (M0) — Project initialization and tooling configuration.
* **Release**: `0.0.1`

### Roadmap
* **Sprint 0 (Current)**: Project structure, dependencies, toolchain, and quality gate configurations (Completed).
* **Sprint 0.5**: CI/CD pipeline improvements, testing infrastructure validation, and test setup.
* **Sprint 1**: Core domain models, feature extraction pipelines, and data ingestion service integration.
* **Sprint 2**: Strategy executor interfaces, backtesting simulation engine, and basic analytics framework.
* **Future Milestones**: Live brokerage adapters, real-time risk checks, and web visualization dashboards.


---

## How to Run Quality Checks

Run the verification toolchain locally using the following commands:

### Code Formatting (Black)
Checks code formatting:
```bash
black --check src/ tests/
```
Auto-format code:
```bash
black src/ tests/
```

### Linting (Ruff)
Run linters and import organization:
```bash
ruff check src/ tests/
```

### Static Type Checks (Mypy)
Run type analysis in strict mode:
```bash
mypy src/
```

### Run Tests (Pytest)
Run the test suite:
```bash
pytest
```

### Run Pre-commit Hooks manually
Run all checks on staged changes:
```bash
pre-commit run --all-files
```
