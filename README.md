# WORKSHOP B3 2017 - GetWatuAsk

## Dev Server preparation

### Linux packages
- sudo apt-get install python3
- sudo apt-get install python3-venv
- python3 -m venv .venv

### Setup environment
- source .venv/bin/activate
- pip install -U pip
- pip install -r requirements.txt

### Launch app (dev)
- export FLASK_APP=app/app.py
- flask run --reload

## Work with Heroku
In a terminal:

- To connect to heroku with your account
`heroku login`
- To copy the project from heroku to your computer in the current folder
`heroku git:clone -a getwatuask`
- To Get the current content of the project from heroku
`git pull heroku master`
- To send your work to heroku (**make sure your work is valid before**)
`git push heroku master`

### Postgresql setup

- Create the database:
`heroku addons:create heroku-postgresql:hobby-dev`
- Test the newly created database in interactive mode:
`heroku pg:psql`
- Exit the interactive mod with
`\q`
- 
`heroku config`


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
- Domain provider: Heroku
- Versionning: Heroku CLI (integrated git)
- Web server: GUnicorn
- Database: SQLITE --> Technically impossible to user
- Database: Postgresql
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
Procfile
README.md
requirements.txt
snapat.db
```
