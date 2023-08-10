import argparse
import logging
import os
from flask import Flask
from routes import routes
from routes.polling_funcs import Polling


def start_server():
    app = Flask(__name__, static_url_path='/polling', static_folder='static')
    app.register_blueprint(routes, url_prefix='/polling')
    app.run(debug=False, host="0.0.0.0", port=int(args.port))


def main(args):
    Polling(str(args.config))
    if not os.path.exists('/var/log/polling/'):
        os.makedirs('/var/log/polling/')
    logger = logging.getLogger('polling_app')
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    file_handler=logging.FileHandler(args.log_file,'a+')
    file_handler.setLevel(logging.INFO)
    file_formatter=logging.Formatter(
        "{'timestamp':'%(asctime)s', 'appname': 'polling_app', \
        'level': '%(levelname)s', %(message)s}"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(ch)
    start_server()

print("Loading Polling app")
parser = argparse.ArgumentParser(description="polling trigger service")
parser.add_argument('-p', '--port', type=int,
                    default=7883, help="port to start flask app server")
parser.add_argument('-c', '--config', type=str,
                    default=str(os.path.abspath(os.path.dirname(__file__))+'/config.json'), help="config file location")
parser.add_argument('-l', '--log_file', type=str,
                    default='/var/log/polling/polling.log', help="log file location")
args = parser.parse_args()

main(args)