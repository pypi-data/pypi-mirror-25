Python Brink API Wrapper
========================

Install the Python Package
-------------------------

::

    $ pip install python-brink


Using the API
--------------

1. Login to the api to receive a jwt token that can be used in future requests without the need to reauthenticate

.. code-block:: python

    from brink.client import BrinkAPI
    from brink.exceptions import BrinkAPIException

    api = BrinkAPI()

    try: 
       # Login to the api via username and password
       access = api.login( 'username', 'password' )
       
    except BrinkApiException, e:
    
       # Login error
       exit()

    jwt_token = access['jwt_token']
    
    # After logging in using the api.login() method, the token is already set so additional
    # requests can be handled correctly
    flights = api.getFlights()
    
2. If you already have a jwt token prepared, you can use it when creating the api instance and bypass logging in.

.. code-block:: python

    from brink.client import BrinkAPI
    
    token='eyJ0eXAiOiJKV1QiLCJhbGc...'
    api = BrinkAPI(token)
    
    # Get flights
    flights = api.getFlights()
    
    # Get details for a specific flights
    flight = api.getFlight(10)
    
    # Get data points for a specific flight
    params = { 'page': 1, 'per_page': 50 }
    flight_data = api.getFlightData(10,params)