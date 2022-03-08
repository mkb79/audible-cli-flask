import json
import logging

import click
from audible import Client
from flask import Flask
from flask.cli import FlaskGroup, ScriptInfo
from flask_restful import Api, Resource, request


logger = logging.getLogger("audible_cli.cmds.cmd_flask")

audible_cli_session = None
audible_cli_client = None


def convert_response_content(resp):
    try:
        return resp.json()
    except json.JSONDecodeError:
        return {"reason_phrase": resp.reason_phrase, "message": resp.text}


def make_api_request(method, path, **kwargs):
    url = audible_cli_client._prepare_api_path(path)

    params = request.args
    if params:
        kwargs["params"] = params

    json_body = request.get_json()
    if json_body is not None:
        kwargs["json"] = json_body

    resp = audible_cli_client.session.request(method, url, **kwargs)
    
    json_resp = convert_response_content(resp)
    status_code = resp.status_code

    headers = {}
    ignore_headers = (
        "content-length", "date", "content-type", "transfer-encoding"
    )
    for k, v in resp.headers.items():
        if k not in ignore_headers:
            headers[k] = v

    return json_resp, status_code, headers


class AudibleAPI(Resource):

    @staticmethod
    def get(path=""):
        return make_api_request("GET", path)

    @staticmethod
    def post(path=""):
        return make_api_request("POST", path)

    @staticmethod
    def put(path=""):
        return make_api_request("PUT", path)

    @staticmethod
    def delete(path=""):
        return make_api_request("DELETE", path)


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(AudibleAPI, '/', '/<path:path>')
    return app


@click.group(
    "flask-server",
    cls=FlaskGroup,
    create_app=create_app,
    load_dotenv=False
)
@click.pass_context
def cli(ctx):
    """Using Flask to make request to the API"""

    # There can only be one `obj` in ctx. FlaskGroup needs his ScriptInfo
    # The audible_cli.session obj must be keep for further purposes
    global audible_cli_session
    global audible_cli_client
    audible_cli_session = ctx.obj
    audible_cli_client = Client(auth=audible_cli_session.auth)
    obj = ScriptInfo(
        create_app=create_app,
        set_debug_flag=ctx.command.set_debug_flag
    )
    ctx.obj = obj
