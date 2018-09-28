[![Build Status](https://travis-ci.org/fgkinus/Fast-Food-Fast.svg?branch=feature%2Forders)](https://travis-ci.org/fgkinus/Fast-Food-Fast)
[![Coverage Status](https://coveralls.io/repos/github/fgkinus/Fast-Food-Fast/badge.svg?branch=feature%2Forders)](https://coveralls.io/github/fgkinus/Fast-Food-Fast?branch=feature%2Forders)
# Fast-Food-Fast
Get your fast food really fast

# Description
A restaurant fast food delivery service. The Flask application is supposed to be a platform to manage orders for Admins
 and make orders for normal user.

## Documentation
The API endpoints exposed by the application are:
![API endpoints](https://screenshotscdn.firefoxusercontent.com/images/9a8cfbd5-175c-42cd-8642-b6e99ce131bd.png)

## Setup
### Dependencies
Python

### Getting Started

To run this project,first clone the repository and  install the requirements


`pip install -t requirements.txt`

Then create an environment configuration file in the root __.env__. in the environmenet file add:

`APP_SETTINGS = 'development' `
`SECRET = '<YOUR SECRET KEY GOES HERE>' `
`DATABASE_URL = '<The DB url to your POSTGRES Database>' `

or alternatively consider the other development scopes in as specified in `config.py`.

to test the application use `py.test` and make sure that __pytest.ini__ contains all environment variables 
in the __.env__ file eg.


```
[pytest]
env = 
    APP_SETTINGS = 'testing'
    SECRET =''
```

### Run The Service
 ```
cd \repo
python run.py
or
flask run
```
## Testing
```
py.test tests/
```

## Deployment
### API
https://fast-food-really-fast.herokuapp.com/
### UI
https://fgkinus.github.io/Fast-Food-Fast/

