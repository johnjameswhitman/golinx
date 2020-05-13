import os
from typing import Any, Dict

from absl import app
from absl import flags
import flask

from golinx.controllers import link_controller
from golinx.models import db


FLAGS = flags.FLAGS
flags.DEFINE_string('host', '0.0.0.0', 'IP address on which to listen.')
flags.DEFINE_integer('port', 5000, 'Port on which to listen.')
flags.DEFINE_string('database_path', None, 'File holding sqlite database.')
flags.DEFINE_boolean('debug', True, 'Whether to operate in debug mode.')
flags.DEFINE_boolean('init_db', False, 'Whether to initialize SQLite.')


def create_app(database_path: str = None, config: Dict[str, Any] = None):
    # create and configure the app

    app = flask.Flask(__name__, instance_relative_config=True)

    if not database_path:
        database_path = os.path.join(app.instance_path, 'golinx.sqlite')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=database_path,
    )

    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(link_controller.LinkController.as_blueprint())

    return app


def main(argv):
    del argv  # Unused.

    app = create_app(FLAGS.database_path)

    if FLAGS.init_db:
        with app.app_context():
            db.init_db()

    print(app.url_map)
    print(flask.__file__)
    app.run(host=FLAGS.host, port=FLAGS.port, debug=FLAGS.debug)

if __name__ == '__main__':
    app.run(main)
