[![Build Status](https://travis-ci.org/fgkinus/Fast-Food-Fast.svg?branch=feature%2Forders)](https://travis-ci.org/fgkinus/Fast-Food-Fast)
[![Coverage Status](https://coveralls.io/repos/github/fgkinus/Fast-Food-Fast/badge.svg?branch=feature%2Forders)](https://coveralls.io/github/fgkinus/Fast-Food-Fast?branch=feature%2Forders)
# Fast-Food-Fast
A restaurant fast food delivery service

To run this project,first install the requirements


`pip install -t requirements.txt`

Then create an environment configuration file __.env__. in the environmenet file add:

`APP_SETTINGS = 'development' `

or alternatively consider the other development scopes in as specified in `config.py`.

to test the application use `py.test` and make sure that __pytest.ini__ contains all environment variables 
in the __.env__ file eg.


`
[pytest]
env = 
    APP_SETTINGS = 'testing'
    SECRET ='''
` 

####find the application on heroku at : 
https://fast-food-really-fast.herokuapp.com/

