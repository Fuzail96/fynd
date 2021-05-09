# Fynd Task For IMDB API Development.


## Prerequisites:

- Python 3.8 or higher

## Clone the project

```
git clone https://github.com/Fuzail96/fynd.git
```

## Run local

### create and activate virtual environment 

 works for linux only
```
 virtualenv env
 source env/bin/activate
```
for other os please refer to the python virual environment [docs](https://docs.python.org/3.6/tutorial/venv.html)

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
python3 manage.py runserver
```

### Run tests

```
python3 manage.py test
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs/
```

### Deployment on Heroku

For deployment on heroku refer [this](https://simpleisbetterthancomplex.com/tutorial/2016/08/09/how-to-deploy-django-applications-on-heroku.html) article