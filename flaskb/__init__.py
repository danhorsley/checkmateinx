from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    # Enable CORS for all routes, allowing any origin in Replit environment
    CORS(app)

    # Register blueprints
    from .chess_api import chess_bp
    app.register_blueprint(chess_bp)

    @app.route('/api/hello', methods=['GET'])
    def hello():
        app.logger.info('Received request to /api/hello endpoint')
        return jsonify({"message": "Hello from Flask Backend!"})

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
