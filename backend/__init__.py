from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'hello world'

    from backend import auth
    app.register_blueprint(auth.bp)

    app.add_url_rule('/', endpoint='index')

    return app
