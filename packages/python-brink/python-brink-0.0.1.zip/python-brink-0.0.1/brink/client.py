from .exceptions import InvalidTokenException, ExpiredTokenException, BrinkAPIException
import requests, base64, json, time

class BrinkAPI(object):
    """ The main brink api wrapper
    """
    
    apibase = 'http://api.joinbrink.com'
    apinamespace = 'v1'
    token = None
    
    def __init__(self, token=None):
        """ Init """
        self.token = token
        
    def setToken(self, token):
        """ Set the authorization token 
        
        Arguments:
            token (str):        The authorization token
        """
        self.validateToken( )
        self.token = token
        
    def getTokenData(self):
        """ Validate a JWT token 
        
        Arguments:
            token (str):        The JWT token
            
        Returns:
            dict                The decoded JWT token
        """
        
        if not isinstance(self.token, str):
            raise InvalidTokenException('Token must be provided as a string value to the constructor or via the setToken() method')
            
        header, body, signature = self.token.split('.')
        
        if not all( (header,body,signature) ):
            raise InvalidTokenException('Token is not a valid JWT token')
        
        data = json.loads( str( base64.b64decode( body + '=' ), 'utf-8' ) )
        
        if 'exp' not in data:
            raise InvalidTokenException('Unable to determine the token expiration')
            
        if time.time() >= data['exp']:
            raise ExpiredTokenException('Token has expired.')
        
        return data
    
    def login(self, username, password):
        """ Get a new JWT token
        
        Arguments:
            username (str):         The username
            password (str):         The password
            
        Returns:
            str
        """
        
        payload = {
            'username': username,
            'password': password
        }
        
        response = self.request('post', '/login', payload, auth=False)
        self.token = response['jwt_token']
        return response
        
    def getFlights(self):
        """ Get a list of recent flights """
        return self.request( 'get', '/flights' )
        
    def getFlight(self, flight_id):
        """ Get the details of a specific flight 
        
        Arguments:
            flight_id (int):            The flight id
        """
        return self.request( 'get', '/flights/' + str(flight_id) );
        
    def createFlight(self, flight_details):
        """ Create a new flight 
        
        Arguments:
            flight_details (dict):          The dictionary containing the flight details
        """
        return self.request( 'put', '/flights', flight_details )
        
    def getFlightData(self, flight_id, params={}):
        """ Get the data for a specific flight 
        
        Arguments:
            flight_id (int):            The flight id
            params (dict):              The request parameters (page, per_page)
        """
        return self.request( 'post', '/flights/' + str(flight_id) + '/data', params )
        
    def createFlightData(self, flight_id, data):
        """ Create a data point for a flight
        
        Arguments:
            flight_id (int):            The flight id
            data (dict):                The data point attributes
        """
        return self.request( 'put', '/flights/' + str(flight_id) + '/data', data )
        
    def request(self, method, endpoint, payload=None, headers={}, auth=True):
        """ Make an api request """
        
        if auth:
            headers.update({'Authorization': 'JWT ' + self.token})
            
        callback = getattr(requests, method)
        response = callback(self.apibase + '/' + self.apinamespace + endpoint, json=payload, headers=headers)

        data = response.json()
        
        if 'error' in data:
            raise BrinkAPIException( data['error'] )
        
        return data
        
