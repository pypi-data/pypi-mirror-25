from bottle import (
    Bottle, request, response, redirect, static_file, SimpleTemplate
)
import sys
import os
import shutil
import json
import requests
import traceback
import io
import wsgiref.util
try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError
from schul_cloud_resources_server_tests.tests.fixtures import StoppableWSGIRefServerAdapter
if "" in sys.path:
    sys.path.append(".")
from schul_cloud_search_tests.search_tests import run_request_tests, run_response_tests

ENDPOINT_STOP = "/stop"
ENDPOINT_CODE = ["/code", "/code/", "/code/<path:path>", "/code<ending:re:\\.zip>"]
REDIRECT_TO = "http://localhost:8080"
APPLICATION = "schul_cloud_search_tests"
HERE = os.path.dirname(__file__)
LISTING_TEMPLATE = SimpleTemplate(
"""
% import os
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>{{ APPLICATION }}</h1>
    <p>
      You can view the updated source code on
      <a href="https://github.com/schul-cloud/schul_cloud_search_tests">GitHub</a>, create issues and get in touch with the developers.
      You can find the currently running version below.
      You can <a href="/code.zip">download the currently running version of the service</a>.
    </p>
    <ul>
    % for dirpath, dirnames, filenames in os.walk(here):
      % assert dirpath.startswith(here)
      % dirpath = dirpath[len(here):]
      % dirpath = dirpath.replace("\\\\", "/")
      % for filename in filenames:
        % if filename.endswith(".pyc"):
          % continue
        % end
        % file = dirpath + "/" + filename
        <li>
          <a href="/code{{ file }}">{{ file }}</a>
        </li>      
      % end
    % end
    </ul>
    <p>
    </p>
  </body>
</html>
""")

error_code_to_name = {
  400: "Bad Request",
  404: "Not Found",
  409: "Conflict",
  500: "Internal Server Error"
}

def create_error_response(status, errors, server_url, answer=None, secret=""):
    """Return the formatted pytest errors, jsonapi compatible.
    
    - status is the status code of the response
    - errors is a list of errors
    - server_url is the url of this server
    - answer is optional and the reponse the proxy got from
      the server to test
    - secret is a secret to include in the response to verify this
      response came from this proxy.
    """
    response.status = status
    error_text = error_code_to_name[status]
    code = "http://" + request.headers["host"] + "/code"
    result = {
      "errors":[
        {
          "status": str(status),
          "title": error_text,
          "detail": "The request or response contained some errors.",
          "meta": {
            "url": server_url,
            "response": answer,
            "proxy": "http://" + request.headers.get("host", "??") + request.path + "?" + request.query_string
          }
        }
      ] + errors,
      "jsonapi": {
        "version": "1.0",
        "meta": {
          "name": "schul_cloud/schul_cloud_search_tests", 
          "source": code,
          "description":
            "These are the tests for the search engines.",
          "secret": secret
        }
      }
    }
    return json.dumps(result, indent="  ").encode("UTF-8")


def jsonapi_error(error, code, target_url, secret=""):
    """Return an error as json"""
    ty, err, tb = type(error.exception), error.exception, getattr(error, "traceback", None)
    if err:
        meta = {"traceback": tb}
        errors = [{
            "status": str(code), 
            "title": error_code_to_name[code],
            "detail": ty.__name__ + ": " + str(err),
            "meta": meta
        }]
    else:
        errors = []
    response.headers["Content-Type"] = "application/vnd.api+json"
    return create_error_response(code, errors, get_server_url(target_url), secret=secret)


def get_server_url(target_url):
    """Return the url on the server."""
    if request.query_string:
        return target_url + "?" + request.query_string
    else:
        return target_url

def print_curl_command(target_url):
    """Print a curl command which would be the equivalent of this request."""
    target = get_server_url(target_url)
    headers = ""
    for header, value in get_request_headers().items():
        headers += " -H '{}: {}'".format(header, value)
    print("curl -i{headers} '{target}'".format(target=target, headers=headers))


def get_request_headers():
    """Return the headers which should be used for the request to the server."""
    headers = {}
    for header, header_value in request.headers.items():
        if header.lower() not in ["content-type", "content-length"] and not wsgiref.util.is_hop_by_hop(header):
            headers[header] = header_value
    return headers

def get_response_headers(response):
    """Return the headers which can be passed to the response.
    
    This removed hop hop headers
    """
    headers = {}
    for header, value in response.headers.items():
        if not wsgiref.util.is_hop_by_hop(header):
            headers[header] = value
    return headers

def check_response(target_url, secret=""):
    """Test the request and the response to the search engine.
    
    - target_url is the url to request
    - secret is the secret to inlcude in the response to make sure the
      response is from the tests.
    """
    print_curl_command(target_url)
    server_url = get_server_url(target_url)
    client_errors = run_request_tests(server_url)
    return_error = (400 if client_errors else 409)
    answer = requests.get(server_url, headers=get_request_headers())
    server_errors = run_response_tests(server_url, answer)
    try:
        result = answer.json()
    except (JSONDecodeError):
        result = None
    all_errors = []
    if client_errors and answer.status_code != 400:
        all_errors += client_errors
    if server_errors:
        all_errors += server_errors
    if all_errors:
        return create_error_response(return_error, all_errors, server_url, result,
                                     secret=secret)
    assert result is not None, "The tests take care that there is a result."
    response.status = answer.status_code
    response.headers.update(get_response_headers(answer))
    return json.dumps(result).encode("UTF-8")


def get_code(path=None, ending=None):
    """Return a directory listing or a static file.
    
    Serve "/code", "/code/*" and "/code.zip"
    
    - path is None or a path to a file to view
    - ending is either None or ".zip"
    """
    if ending is not None:
        assert ending == ".zip"
        redirect("/code/{}.zip".format(APPLICATION))
    if path == APPLICATION + ".zip":
        # Download the source of this application."""
        # from http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python#6511788
        zip_path = (shutil.make_archive("/tmp/" + APPLICATION, "zip", HERE))
        return static_file(zip_path, root="/")
    if path is None:
        path = "/"
    if path.endswith("/"):
        # return a listing
        allowed = ["/", "tests/", "search_tests/"]
        assert path in allowed, "Path \"{}\" should be in {}".format(path, allowed)
        return LISTING_TEMPLATE.render(here=HERE, APPLICATION=APPLICATION)
    return static_file(path, root=HERE)


def get_app(endpoint="/", target_url="http://localhost:8080", secret=""):
    """Return a bottle app that tests the request and the response."""
    app = Bottle()
    app.get(endpoint, callback=lambda: check_response(target_url, secret=secret))
    for code_endpoint in ENDPOINT_CODE:
        app.get(code_endpoint, callback=get_code)
    for code in [404, 500]:
       app.error(code)(lambda error, code=code: jsonapi_error(error, code, target_url, secret=secret))
    return app


def run(app, host="0.0.0.0", port=8081):
    """Run a stoppable bottle app."""
    server = StoppableWSGIRefServerAdapter(host=host, port=port)
    app.get(ENDPOINT_STOP, callback=lambda: server.shutdown(blocking=False))
    app.run(debug=True, server=server)


def main(host="0.0.0.0", port=8081, endpoint="/", target_url="http://localhost:8080"):
    """Start the server."""
    app = get_app(endpoint=endpoint, target_url=target_url)
    run(app, host=host, port=port)


__all__ = ["main", "run", "get_app"]

if __name__ == "__main__":
    kw = {"host": "0.0.0.0"}
    kw["target_url"] = (sys.argv[1] if len(sys.argv) >= 2 else "http://localhost:8080/v1/search")
    kw["port"] = (int(sys.argv[2]) if len(sys.argv) >= 3 else 8081) 
    kw["endpoint"] = (sys.argv[3] if len(sys.argv) >= 4 else "/v1/search")
    print("Forwarding traffic from http://{host}:{port}{endpoint} to {target_url}".format(**kw))
    main(**kw)
