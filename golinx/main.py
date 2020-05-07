import os

from absl import app
from absl import flags
import flask

from golinx.controllers import link
from golinx.models import db


FLAGS = flags.FLAGS
flags.DEFINE_string('host', None, 'IP address on which to listen.')
flags.DEFINE_integer('port', 5000, 'Port on which to listen.')
flags.DEFINE_boolean('debug', True, 'Whether to operate in debug mode.')
flags.DEFINE_boolean('init_db', False, 'Whether to initialize SQLite.')


def create_app(config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'golinx.sqlite'),
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

    app.register_blueprint(link.create_blueprint())

    return app


def main(argv):
    del argv  # Unused.

    app = create_app()
    
    if FLAGS.init_db:
        with app.app_context():
            db.init_db()

    app.run(host=FLAGS.host, port=FLAGS.port, debug=FLAGS.debug)


if __name__ == '__main__':
    app.run(main)

