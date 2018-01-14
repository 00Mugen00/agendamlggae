from tokens.read import read_tokens

google_api_key = None
flickr_api_key = None
jwt_token = None
google_oauth_decorator = None

read.read_tokens()

# Must be here because needs the declaration of jwt_token to be happened when importing
from tokens.jwt_funcs import create_jwt_token, decode_jwt_token, get_user_from_token
