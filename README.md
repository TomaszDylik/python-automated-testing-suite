# Virtual Greenhouse - Automated Testing Suite

**Autor:** Tomasz Dylik  
**Grupa:** 2, Informatyka praktyczna

## Opis projektu

Projekt testow automatycznych dla aplikacji Virtual Greenhouse.
Aplikacja sluzy do zarzadzania wirtualna szklarnia z roslinami.

## Struktura projektu

- `app/` - kod aplikacji Python (logika biznesowa)
- `client/` - frontend React
- `server/` - backend Express/Node.js
- `tests/` - testy automatyczne Python
  - `unit/` - testy jednostkowe
  - `api/` - testy API
  - `bdd/` - testy BDD (Gherkin)
  - `performance/` - testy wydajnosciowe

## Uruchomienie aplikacji

### 1. Baza danych
```bash
docker-compose up -d
```

### 2. Backend
```bash
cd server
npm install
npx prisma db push
npx prisma generate
npm run seed
npm run dev
```

### 3. Frontend
```bash
cd client
npm install
npm run dev
```

## Uruchomienie testow

### Instalacja
```bash
cd tests
pip install -r requirements.txt
```

### Wszystkie testy
```bash
pytest
```

### Testy jednostkowe
```bash
pytest unit/ -m unit -v
```

### Testy API
```bash
pytest api/ -m api -v
```

### Testy BDD
```bash
pytest bdd/ -m bdd -v
```

### Testy wydajnosciowe
```bash
pytest performance/ -m performance -v
```

### Pokrycie kodu
```bash
pytest unit/ --cov=../app --cov-report=html --cov-report=term
```

### Locust (test obciazeniowy)
```bash
cd tests/performance
locust -f locustfile.py --host=http://localhost:3001
```

## Pipelines CI/CD

- `.github/workflows/unit-tests.yml` - testy jednostkowe
- `.github/workflows/api-tests.yml` - testy API
- `.github/workflows/bdd-tests.yml` - testy BDD
- `.github/workflows/performance-tests.yml` - testy wydajnosciowe

## Uzytkownicy testowi

- admin / admin123
- user / user123