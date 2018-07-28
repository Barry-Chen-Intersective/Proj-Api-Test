import myModule.awsS3Actions, myModule.tools, myModule.decorators, myModule.constants


@myModule.decorators.jsonHttpResponse
def testSuitesHandler(event, context):
    testDataDir = "api-test-data"
    testSuitesFile = "testSuites.json"
    if event["queryStringParameters"] is not None:
        if "testSuite" in event["queryStringParameters"] and len(event["queryStringParameters"]["testSuite"].strip()) > 0:
            testSuitesFile = event["queryStringParameters"]["testSuite"]
    s3Actions = myModule.awsS3Actions.awsS3Actions()
    testSuitesFile = "{}/{}".format(testDataDir, testSuitesFile)
    statusMessage, testSuites = s3Actions.getS3JsonObject(testSuitesFile)
    results = []

    if statusMessage != myModule.constants.SUCCESS:
        return {"status" : statusMessage, "data" : results}
    
    for oneTest in testSuites["data"]:
        testId = oneTest["id"]
        message, testData = s3Actions.getS3JsonObject("{}/data/{}_{}.json".format(testDataDir ,testId, oneTest["params"]))
        if message != myModule.constants.SUCCESS:
            results.append({"id" : str(testId), "params" : str(oneTest["params"]), "expected_result_file" : str(oneTest["expected_result"]), "message" : message})
            continue
        requestUrl = "{}/{}.json".format(oneTest["domain"], oneTest["id"])
        result = myModule.tools.fireRequest(requestUrl, testData["headers"], testData["parameters"], testData["method"])
        message, expectedResult = s3Actions.getS3JsonObject("{}/data/{}_expected_result_{}.json".format(testDataDir, testId, oneTest["expected_result"]))
        if message != myModule.constants.SUCCESS:
            results.append({"id" : str(testId), "params" : str(oneTest["params"]), "expected_result_file" : str(oneTest["expected_result"]), "message" : message})
            continue
        message = myModule.constants.OK
        if myModule.tools.jsonLoads(result.text) != expectedResult:
            message = myModule.constants.FAIL
        results.append({"id" : str(testId), "params" : str(oneTest["params"]), "expected_result_file" : str(oneTest["expected_result"]), "message" : message})
    return {"status" : statusMessage, "data" : results}

@myModule.decorators.jsonHttpResponse
def handler(event, context):
    myHeaders = {
        "timelineid" : "587",
        "appkey" : "b11e7c189b",
        "apikey" : "6bcfa5a817f3e9ba7130"
    }
    myParams = {
        "model" : "project",
        "model_id" : "556"
    }

    response = myModule.tools.fireRequest("https://sandbox.practera.com/api/v2/motivations/progress/list.json", myHeaders, myParams, "get")
    return response.text