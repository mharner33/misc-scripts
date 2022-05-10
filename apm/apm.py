"""
    Script to generate a series of spans using the Datadog APM tracer installed on the localhost
"""
import requests
import time
import json
from random import randint

# Change these if you are not using localhost
apmURL = 'http://localhost:8126/v0.3/traces'

# These will identify the service information
serviceName = "test_service"
resourceName = "/home"
traceType = "web"

traceId = randint(10000000,99999999)
spanId = randint(10000000,99999999)
parentId = 0

# Set the initial start time for the first span
startTime = int(time.time_ns())
time.sleep(1)

# Total number of spans to create (including parent trace)
spanNum = int(input("Enter the number of spans to create: "))

for i in range(0,spanNum):
    if i == 0:
        spanName = "trace_1"
    else:
        spanName = "span_" + str(i)

    duration = int(time.time_ns()) - startTime

    payload = [[{
            "duration": duration,
            "name": spanName,
            "resource": resourceName,
            "service": serviceName,
            "span_id": spanId,
            "start": startTime,
            "trace_id": traceId, 
            "type": traceType,
            "parent_id": parentId
            }]] 

    try: 
        r = requests.put(apmURL,json=payload)
    except ConnectionError:
        print("Connection error %n",r.status_code)

    parentId = spanId
    spanId = spanId + 10

    # Get start time for next span and delay for some amount
    startTime = int(time.time_ns())
    time.sleep(randint(1,5)) 
