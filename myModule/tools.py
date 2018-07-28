import json, requests


def fireRequest(requestUrl, myHeaders, myParams, method):
    if method == "get":
        return requests.get(url = requestUrl, headers = myHeaders, params = myParams)
    elif method == "post":
        return requests.post(url = requestUrl, data = myParams, headers = myHeaders)
    elif method == "post-json":
        myHeaders["content-type"] = "application/json"
        return requests.post(url = requestUrl, data = json.dumps(myParams), headers = myHeaders)
    else:
        return None

def jsonLoad(contentStr):
    return json.load(contentStr)

def jsonLoads(rawStr):
    return json.loads(rawStr)

def jsonDumps(rawObject):
    return json.dumps(rawObject)