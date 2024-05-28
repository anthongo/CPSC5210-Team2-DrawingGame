$Env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/dribbbl"
$Env:auth0_domain = "dev-ahjkm0k5e1e7ik74.us.auth0.com"
$Env:client_id = "SHtECfwsr1cV0DznVVyoValV7QBkxAbf"
$Env:client_secret = "hClEGpfL_qxQz2ZAP6Ss2hZHMifHMkwkDjYv30pcFEjlqdq2ruuQXBNDCQABnqBp"

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

scoop install git

scoop install postgresql
$Env:PGPASSWORD = postgres
createdb -h localhost -p 5432 -U postgres dribbbl
psql -d dribbbl -h localhost -U postgres -f schema.sql

scoop install python
pip install pipenv
pipenv install
pipenv install --dev

scoop install nodejs
npm install
npm install --dev

Start-Process "" pipenv run python app.py
pipenv run pytest --cov=app --cov=db --cov-report=term