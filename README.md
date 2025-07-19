# Project Setup Instructions

## 📦 Prerequisites

### Backend
- **PostgreSQL** 17.5  
  [Download PostgreSQL](https://www.postgresql.org/download/)
- **Poetry**  
  [Install Poetry](https://python-poetry.org/docs/#installation)
- **Python** 3.13.5  
  [Download Python](https://www.python.org/downloads/)

### Frontend
- **Node.js** v22.17.1  
  [Download Node.js](https://nodejs.org/en/download)

---

## 🚀 Setup Instructions

### 🔧 Backend (`./backend`)

1. **Start PostgreSQL**, and update the `.db.env` file with the appropriate database credentials.  

2. **Verify Python version**
```bash
  python --version
```
3. Install dependencies using poetry 
```bash
poetry install
```
4. Run Alembic to initialize the database
```bash
poetry run alembic upgrade head
```
5. Start server
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

###  Frontend (`./frontend`)

1. **Make sure node is properly installed and correct version
```bash
node --version
```
2. **Install dependencies**
```bash
npm install
```
3. **Run locally**
```bash
npm run dev
```

### 🔐 Default Login Credentials
Username: chiefaiuser@chiefai.com

Password: Test123!

