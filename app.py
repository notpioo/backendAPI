import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.routes.admin_routes import admin_bp
from app.routes.chat_routes import chat_bp
from app.routes.knowledge_routes import knowledge_bp
from app.routes.announcement_routes import announcement_bp
from app.config.firebase_config import initialize_firebase

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

    # Configure Flask
    app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'default-secret-key')
    app.config['JSON_AS_ASCII'] = False  # Support Indonesian characters

    # Enable CORS for all routes
    CORS(app)

    # Initialize Firebase
    try:
        initialize_firebase()
        print("✅ Firebase initialized successfully")
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(announcement_bp, url_prefix='/api/announcement')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)