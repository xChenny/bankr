from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/hello')
    def hello():
        return 'hello world'

    from backend import auth, bankr, jobhuntr
    app.register_blueprint(auth.bp)
    app.register_blueprint(jobhuntr.bp)

    app.add_url_rule('/', endpoint='index')

    return app
