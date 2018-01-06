from util.json import from_json
import tokens


def read_tokens():
    tokens_file = open('tokens/tokens.json', 'r')
    json = from_json(tokens_file.read())
    tokens_file.close()
    tokens.flickr_api_key = json[u'flickr_api_key']
    tokens.google_api_key = json[u'google_api_key']

