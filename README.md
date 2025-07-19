Backend Server Requirements:
Prequisites installed:
Backend
- Postgresql 17.5 (https://www.postgresql.org/download/)
- poetry (https://python-poetry.org/docs/#installation)
- python 3.13.5 (https://www.python.org/downloads/)

Frontend
- Nodejs v22.17.1 (https://nodejs.org/en/download)

Setup:

Backend (./backend)
1.) Run postgresql and modify .db.env file to match connection credentials (defaults - port: 5433, username: postgres, password: postgres)
2.) Ensure python is installed and correct version
`python --version`
3.) Install dependencies using poetry
`poetry install`
4.) Run alembic to initialize database 
`poetry run alembic upgrade head` 
5.) Run the server locally
`poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload` 

Frontend (./frontend)
1.) Make sure node is properly installed and correct version
`node --version`
2.) Install dependencies
`npm install`
3.) Run locally
`npm run dev`

Default login to the application:
Username: chiefaiuser@chiefai.com
Password: Test123!
