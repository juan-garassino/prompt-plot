# Makefile for PromptPlot v3.0

PYTHON := python3
PACKAGE := promptplot
TESTS := tests

.PHONY: help install dev test test-ci studio-check check prints-export lint format clean

help:
	@echo "PromptPlot v3.0"
	@echo ""
	@echo "  install    Install package"
	@echo "  dev        Install with dev dependencies"
	@echo "  test       Run tests"
	@echo "  test-ci    Tests, minus the one known pre-existing failure"
	@echo "  studio-check  Re-render every studio piece and compare against the baseline"
	@echo "  check      test-ci + studio-check — run this before you call it done"
	@echo "  prints-export  Published plates -> build/prints/ catalog + assets -> gs://garassino-ai-prints"
	@echo "  lint       Run ruff linter"
	@echo "  format     Format code with black"
	@echo "  clean      Remove build artifacts"

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev,viz]"

test:
	$(PYTHON) -m pytest $(TESTS)/ -v

test-ci:
	$(PYTHON) -m pytest $(TESTS)/ -q \
		--deselect $(TESTS)/test_refinement.py::test_batch_refinement_prefers_improved_result

# The studio pieces live OUTSIDE the package and no test imports them, so the
# suite can be green while an engine edit has silently changed an approved
# plate. This is the only thing that catches that.
studio-check:
	$(PYTHON) scripts/studio_regression.py

check: test-ci studio-check

# Juan's publish verdicts -> catalog.json + content-addressed assets -> the
# public bucket the portfolio site reads. Re-runs render only what is new.
prints-export:
	uv run python scripts/prints_export.py --push

lint:
	$(PYTHON) -m ruff check $(PACKAGE)/

format:
	$(PYTHON) -m black $(PACKAGE)/ $(TESTS)/
	$(PYTHON) -m isort $(PACKAGE)/ $(TESTS)/

clean:
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage coverage.xml test-results/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
