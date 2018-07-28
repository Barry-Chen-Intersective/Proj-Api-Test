import functools, json


def decorator(d):
	def _d(fn): return functools.update_wrapper(d(fn),fn)
	functools.update_wrapper(_d,d)
	return _d

@decorator
def jsonHttpResponse(f):
    def _f(*args):
        responseBody = {
            "data" : f(*args)
        }
        responseObj = {
            "statusCode": 200,
            "body" : json.dumps(responseBody),
            "headers": {
                    'Content-Type': 'application/json'
                    }
                }
        return responseObj
    return _f