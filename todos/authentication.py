from rest_framework import authentication, exceptions


# Hardcoded credentials for this version
API_KEY = "buildy-api-key-2026"
API_SECRET = "buildy-secret-2026"


class APIKeyUser:
    """
    Simple user object for API key authentication.
    Doesn't use Django's user model.
    """
    def __init__(self):
        self.is_authenticated = True
    
    @property
    def is_anonymous(self):
        return False


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom API key authentication using X-API-Key and X-API-Secret headers.
    
    Clients must include both headers in their requests:
    - X-API-Key: buildy-api-key-2026
    - X-API-Secret: buildy-secret-2026
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using API key and secret headers.
        
        Returns:
            tuple: (user, auth) where user is an APIKeyUser instance
        
        Raises:
            AuthenticationFailed: If credentials are missing or invalid
        """
        api_key = request.headers.get('X-API-Key')
        api_secret = request.headers.get('X-API-Secret')
        
        # Check if headers are present
        if not api_key:
            raise exceptions.AuthenticationFailed('X-API-Key header is required')
        
        if not api_secret:
            raise exceptions.AuthenticationFailed('X-API-Secret header is required')
        
        # Validate credentials
        if api_key != API_KEY:
            raise exceptions.AuthenticationFailed('Invalid API key')
        
        if api_secret != API_SECRET:
            raise exceptions.AuthenticationFailed('Invalid API secret')
        
        # Return APIKeyUser instance as the user
        return (APIKeyUser(), {'api_key': api_key, 'api_secret': api_secret})
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the WWW-Authenticate header
        in a 401 Unauthenticated response.
        
        This method is required to return 401 instead of 403 for failed authentication.
        """
        return 'X-API-Key'

