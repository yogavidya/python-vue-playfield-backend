import flask
import re
import os
import dotenv
from App import logger

dotenv.load_dotenv()

__accepted_origins=[os.getenv('FLASK_FRONTEND_DEV_SERVER'),
                  os.getenv('FLASK_FRONTEND_PROD_SERVER'),
                  os.getenv('FLASK_FRONTEND_LOCAL_PROD_SERVER')]


def matches_any(s, pattern_list):
  """Check if S matches any of PATTERN_LIST
  Args:
      s ([string]): any text
      pattern_list ([str]): a list of pattern strings

  Returns:
      [boolean]: True if match
  """
  try:
    next(filter(lambda x: x is not None, [re.match(x, s) for x in pattern_list]))
    return True
  except StopIteration:
    return False

def valid_origin():
    """Checks if current request comes from a valid origin
    Returns:
        [boolean]: True if request has Origin header AND origin is in __ACCEPTED_ORIGINS
    """
    logger.debug('app_cors.valid_origin()')
    if 'Origin' in flask.request.headers \
      and matches_any(flask.request.headers['Origin'], __accepted_origins):
        logger.debug(f'returning: {flask.request.headers["Origin"]}')
        return flask.request.headers['Origin']
        logger.debug(f'returning: False')
    return False
  
def preflight_request_response():
  """Returns a prefilled preflight response if current request requires ("OPTIONS")

  Returns:
      [response or None]: a valid preflight response if necessary, else None
  """
  if flask.request.method == 'OPTIONS':
    response = flask.make_response('OK')
    response.headers['Access-Control-Allow-Origin']=valid_origin()
    response.headers['Access-Control-Allow-Headers']=flask.request.headers['Access-Control-Request-Headers']
    response.headers['Access-Control-Allow-Methods']=flask.request.headers['Access-Control-Request-Method']
    response.headers['Vary']=True
    return response
  return None

