from bottle import get, run, response, request
import json
from schul_cloud_resources_api_v1.schema import get_schemas

JSONAPI = {
            "version": "1.0",
            "meta": {
                "name": "schul_cloud/schul_cloud_search_tests", 
                "source": 
                    "https://github.com/schul_cloud/schul_cloud_search_tests",
                "description":
                    "These are the tests for the search engines.",
            }
        }

def api_error(status, title, description):
    response.status = status
    result = {
      "errors":[
        {
          "status": str(status),
          "title": title,
          "detail": description
        }
      ],
      "jsonapi": JSONAPI
    }
    return json.dumps(result)

@get("/<path:path>")
def get(path):
    """Return a search response."""
    response.headers["Content-Type"] = "application/vnd.api+json"
    if request.headers["Accept"] not in ["application/vnd.api+json", "application/*", "*/*"]:
        return api_error(406, "Not Acceptable", "Accept should be application/vnd.api+json.")
    if not "Q" in request.query or len(request.query) >= 2:
        return api_error(400, "Bad Request", "I do not understand other parameters than Q.")
    response.set_header("Content-Type", "application/vnd.api+json")
    self_href = "http://" + request.headers.get("host", "localhost") + "?" + request.query_string
    example_resources = get_schemas()["resource"].get_valid_examples()
    resources = [{"type":"resource","attributes":data,"id":str(i)}
                 for i, data in enumerate(example_resources)]
    count = len(resources)
    limit = 10
    if count > limit:
        count = limit
        resources = resources[:count]
    result = {
        "jsonapi": JSONAPI,
        "links" : {
            "self": {
                 "href": self_href,
                 "meta": {
                    "limit": limit,
                    "offset": 0,
                    "count": count
                 }
            },
            "first": self_href,
            "last": (self_href if count else None),
            "prev": None,
            "next": None,
        },
        "data": resources
    }
    return json.dumps(result)

if __name__ == "__main__":
    run(reload=True, port=8080)
