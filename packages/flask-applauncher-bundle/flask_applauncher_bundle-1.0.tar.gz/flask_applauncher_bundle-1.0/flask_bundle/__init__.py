from flask.json import JSONEncoder
import zope.event
import inject
from flask import Flask
import datetime
import threading
import applauncher.kernel


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


# Just for inject an array as ApiBlueprints
class ApiBlueprints(object):
    pass


class RestApiBundle(object):
    def __init__(self):
        self.config_mapping = {
            "flask": {
                "use_debugger": False,
                "port": 3003,
                "host": "0.0.0.0"
            }
        }

        self.blueprints = []
        self.injection_bindings = {
            ApiBlueprints: self.blueprints
        }

        zope.event.subscribers.append(self.kernel_ready)

    @inject.params(config=applauncher.kernel.Configuration)
    def start_sever(self, config):
        app = Flask("FlaskServer")
        app.json_encoder = CustomJSONEncoder

        for blueprint in self.blueprints:
            app.register_blueprint(blueprint)

        c = config.flask
        app.run(use_debugger=c.use_debugger, port=c.port, host=c.host)

    def kernel_ready(self, event):
        if isinstance(event, applauncher.kernel.KernelReadyEvent):
            t = threading.Thread(target=self.start_sever)
            t.start()


