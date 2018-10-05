[![CircleCI](https://circleci.com/gh/fgkinus/Fast-Food-Fast/tree/develop.svg?style=svg)](https://circleci.com/gh/fgkinus/Fast-Food-Fast/tree/develop)
[![Coverage Status](https://coveralls.io/repos/github/fgkinus/Fast-Food-Fast/badge.svg?branch=develop)](https://coveralls.io/github/fgkinus/Fast-Food-Fast?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/18d0d4be1372bb91b7c4/maintainability)](https://codeclimate.com/github/fgkinus/Fast-Food-Fast/maintainability)

# Fast-Food-Fast
Get your fast food really fast

# Description
A restaurant fast food delivery service. The Flask application is supposed to be a platform to manage orders for Admins
 and make orders for normal user.

## Documentation
The API endpoints exposed by the application are:

| CRUD   	| ENDPOINT                    	| DESCRIPTION                         	| PROTECTED 	| ROLE  	|
|--------	|-----------------------------	|-------------------------------------	|-----------	|-------	|
| POST   	| /api/v2/auth/login          	| start new session                   	| NO        	|       	|
| POST   	| /api/v2/auth/signup         	| register new users                 	| NO        	|       	|
| GET    	| /api/v2/auth/profile        	| get profile for authenticated user  	| YES       	| BOTH  	|
| PUT    	| /api/v2/auth/profile        	| edit user details                   	| YES       	| BOTH  	|
| POST   	| /api/v2/auth/register-admin 	| Add new Admin User                  	| YES       	| ADMIN 	|
| POST   	| /api/v2/menu/               	| Add new Menu Item                   	| YES       	| ADMIN 	|
| GET    	| /api/v2/menu/               	| List all Menu Items                 	| NO        	|       	|
| DELETE 	| /api/v2/menu/{item_id}      	| Delete a menu item                  	| YES       	| ADMIN 	|
| GET    	| /api/v2/menu/{item_id}      	| Fetch a specific Menu Item          	| NO        	|       	|
| PUT    	| /api/v2/menu/{item_id}      	| edit user details                   	| YES       	| ADMIN 	|
| POST   	| /api/v2/orders/             	| Add new order                       	| YES       	| USER  	|
| GET    	| /api/v2/orders/             	| list all orders                     	| YES       	| ADMIN 	|
| GET    	| /api/v2/orders/history      	| list all authenticate users' orders 	| YES       	| USER  	|
| GET    	| /api/v2/orders/response     	| list the possible responses         	| YES       	| ADMIN 	|
| PUT    	| /api/v2/orders/{oder_id}    	| Add/edit a response to an order     	| YES       	| ADMIN 	|
| DELETE 	| /api/v2/orders/{oder_id}    	| Remove orders                       	| YES       	| USER  	|
| GET    	| /api/v2/orders/{oder_id}    	| Fetch a specific order Item         	| YES       	| ADMIN 	|
| PATCH  	| /api/v2/orders/{oder_id}    	| edit order details                  	| YES       	| USER  	|



## Setup
### Dependencies
Python

### Getting Started

To run this project,first clone the repository and  install the requirements

1. install `virtualenv`
`pip install virtualev`
2. create a local environment
`virtualenv <name>`
3. activate virtual environment


   **cmd** :`venv\Scripts\activate.bat`
   
   **Linux** : `source venv/bin/activate`
   
 4. install the dependencies

`pip install -r requirements.txt`

Then create an environment configuration file in the root __.env__. in the environmenet file add:

```
APP_SETTINGS = 'development' 
SECRET = '<YOUR SECRET KEY GOES HERE>' 
DATABASE_URL = '<The DB url to your POSTGRES Database>'
TEST_DATABASE_URL = '<The DB url to your TEST POSTGRES Database>'
```

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
py.test 
```

## Deployment
### API
https://fast-food-really-fast.herokuapp.com/
### UI
https://fgkinus.github.io/Fast-Food-Fast/

