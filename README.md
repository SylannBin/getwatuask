# WORKSHOP B3 2017 - GetWatuAsk

## Setup

### Linux
- $ sudo apt-get install python3
- $ sudo apt-get install python3-venv
- $ pip install -U pip
- $ python3 -m venv .venv
- $ source .venv/bin/activate
- $ pip install -r requirements.txt
- $ export FLASK_APP=app/app.py

### Windows
First use installer for python3, then in cmd.exe:
- pip install -U pip
- pip install virtualenv
- python -m virtualenv .venv
- .venv/Scripts/activate
- pip install -r requirements.txt
- SET FLASK_APP=app/app.py

### Mac
- brew install python
- pip3 install virtualenv
- python3 -m virtualenv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- export FLASK_APP=app/app.py

## Launch app (dev)
- flask run --reload

## Postgresql setup
Get postgresql
Get pgadmin (GUI for postgresql)

- Create a new role with super user rights and prompt for password
`psql createuser -P -s -e <UserName>`
- Create a new database:
`psql -c "createdb snapat"`
- Test the newly created database in interactive mode:
`psql snapat`
- Exit the interactive mod with
`\q`
- Dump a database
`pg_dump snapat > filename.sql`
- Import a dumpfile into an existing database
`psql snapat < filename.sql`

## Routes:
- /
- /login `GET` `POST`
- /logout
- /needs
- /client/<client_id>/<need_id>/<qr_code_salt>
- /needs/view/<need_id>
- /needs/edit/<need_id> `GET` `POST`
- /needs/new `GET` `POST`

## Language choices
We had to change of Domain provider and database during the development, due to technical and skill limitations.

- 1st Domain provider: Heroku
- 2nd Domain provider: Always data
- finally: No Domain provider :(

- 1st: Versionning: Heroku CLI (integrated git)
- 2nd: Github

- Web server: GUnicorn
- finally: Local Flask server

- 1st Database: SQLITE
- 2nd Database: Postgresql

- Server-side scripts: Python3 (+ Micro framework Flask)
- Template rendering: Jinja2
- Client-side scripts: Javascript, Jquery

## Folder Organisation
```
.venv/
app/
    static/
        css/
        js/
        img/
    templates/
        *.html
    *.py
.gitignore
README.md
requirements.txt
```
