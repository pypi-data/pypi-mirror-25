"""
Request is a request
"""

import json


def dejsonify(request):
    json_content = request.content.read()
    if json_content:
        content = json.loads(json_content)
    else:
        content = {}
    return content


def jsonify(request, data):
    request.responseHeaders.addRawHeader("content-type", "application/json")
    return json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
