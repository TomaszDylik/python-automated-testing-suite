# Automated Testing Suite

Python automated tests for Virtual Greenhouse application.

## Setup

```bash
cd tests
pip install -r requirements.txt
```

## Run Tests

All tests:
```bash
pytest
```

Unit tests:
```bash
pytest unit/ -m unit
```

API tests:
```bash
pytest api/ -m api
```

BDD tests:
```bash
pytest bdd/ -m bdd
```

Performance tests:
```bash
pytest performance/ -m performance
```

## Code Coverage

```bash
pytest unit/ --cov=../app --cov-report=html
```

## Locust Load Test

```bash
cd performance
locust -f locustfile.py --host=http://localhost:3001
```

## Reports

HTML report: `reports/report.html`
Coverage report: `htmlcov/index.html