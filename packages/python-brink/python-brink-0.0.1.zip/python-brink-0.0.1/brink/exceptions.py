
class InvalidTokenException(Exception):
    """ Exception used to indicate invalid JWT tokens """
    pass
    
class ExpiredTokenException(Exception):
    """ Exception used to indicate a JWT token that needs to be renewed """
    pass
    
class BrinkAPIException(Exception):
    """ Exception used to indicate an api request exception """
    pass    