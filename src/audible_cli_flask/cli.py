import logging

import click
from audible import Client
from flask import Flask
from flask.cli import FlaskGroup, ScriptInfo
from flask_restful import Api, Resource, request


logger = logging.getLogger("audible_cli.cmds.cmd_flask")

audible_cli_session = None
audible_cli_client = None


class RESTapp(Resource):

    @staticmethod
    def get(path=""):
        args = request.args
        r = audible_cli_client._request("GET", path, params=args)
        return r

    @staticmethod
    def post(path=""):
        json_body = request.get_json()
        r = audible_cli_client._request("POST", path, json=json_body)
        return r

    @staticmethod
    def put(path=""):
        json_body = request.get_json()
        r = audible_cli_client._request("PUT", path, json=json_body)
        return r

    @staticmethod
    def delete(path=""):
        r = audible_cli_client._request("DELETE", path)
        return r


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(RESTapp, '/', '/<path:path>')
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
