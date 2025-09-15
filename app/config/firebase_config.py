import firebase_admin
from firebase_admin import credentials, db
import os
import json

def initialize_firebase():
    """Initialize Firebase Admin SDK with service account key"""
    try:
        # Initialize with default credentials if not already initialized
        if not firebase_admin._apps:
            # Check if Firebase credentials are available
            project_id = os.getenv('FIREBASE_PROJECT_ID')
            private_key = os.getenv('FIREBASE_PRIVATE_KEY')
            client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
            
            if project_id and private_key and client_email:
                # Use real Firebase credentials
                cred_dict = {
                    "type": "service_account",
                    "project_id": project_id,
                    "private_key": private_key.replace('\\n', '\n'),  # Fix newlines
                    "client_email": client_email,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "universe_domain": "googleapis.com"
                }
                
                cred = credentials.Certificate(cred_dict)
                # Try different Firebase regions
                database_urls = [
                    f'https://{project_id}-default-rtdb.asia-southeast1.firebasedatabase.app',
                    f'https://{project_id}-default-rtdb.firebaseio.com',
                    f'https://{project_id}-default-rtdb.europe-west1.firebasedatabase.app'
                ]
                
                database_url = database_urls[0]  # Default to Asia Southeast
                firebase_admin.initialize_app(cred, {
                    'databaseURL': database_url
                })
                
                print("✅ Firebase connected successfully to real database!")
                return True
            else:
                print("⚠️  Using mock Firebase service for development")
                print("   Add FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, and FIREBASE_CLIENT_EMAIL to use real Firebase")
                return True
            
        return True
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        print("⚠️  Falling back to mock database")
        return False

class MockDatabase:
    """Mock database for development"""
    def __init__(self):
        self.data = {
            'knowledge': {}
        }
    
    def child(self, path):
        return MockDatabaseRef(self.data, path)

class MockDatabaseRef:
    """Mock database reference"""
    def __init__(self, data, path):
        self.data = data
        self.path = path
        self.keys = path.split('/') if path else []
    
    def child(self, child_path):
        new_path = f"{self.path}/{child_path}" if self.path else child_path
        return MockDatabaseRef(self.data, new_path)
    
    def get(self):
        current = self.data
        for key in self.keys:
            if key in current:
                current = current[key]
            else:
                return None
        return current
    
    def push(self):
        import uuid
        new_id = str(uuid.uuid4())[:8]
        return MockPushRef(self.data, self.keys, new_id)
    
    def set(self, value):
        current = self.data
        for key in self.keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        if self.keys:
            current[self.keys[-1]] = value
    
    def update(self, value):
        current = self.data
        for key in self.keys:
            if key not in current:
                current[key] = {}
            current = current[key]
        current.update(value)
    
    def delete(self):
        if len(self.keys) > 0:
            current = self.data
            for key in self.keys[:-1]:
                if key in current:
                    current = current[key]
                else:
                    return
            if self.keys[-1] in current:
                del current[self.keys[-1]]

class MockPushRef:
    def __init__(self, data, parent_keys, new_id):
        self.data = data
        self.parent_keys = parent_keys
        self.new_id = new_id
    
    def set(self, value):
        current = self.data
        for key in self.parent_keys:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[self.new_id] = value

# Global mock database instance
_mock_db = MockDatabase()

def get_db():
    """Get Firebase Realtime Database reference"""
    # Check if we have real Firebase connection
    project_id = os.getenv('FIREBASE_PROJECT_ID')
    private_key = os.getenv('FIREBASE_PRIVATE_KEY')
    client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
    
    # Debug credentials
    print(f"🔍 Debug credentials: project_id={bool(project_id)}, private_key={bool(private_key)}, client_email={bool(client_email)}")
    print(f"🔍 Firebase apps initialized: {bool(firebase_admin._apps)}")
    
    if project_id and private_key and client_email and firebase_admin._apps:
        try:
            print("🔥 Using REAL Firebase database!")
            return db.reference()  # Real Firebase database
        except Exception as e:
            print(f"❌ Error getting Firebase DB: {e}, falling back to mock")
            return _mock_db
    else:
        print("⚠️ Using mock database - Firebase credentials not complete")
        if not project_id:
            print("   Missing FIREBASE_PROJECT_ID")
        if not private_key:
            print("   Missing FIREBASE_PRIVATE_KEY")
        if not client_email:
            print("   Missing FIREBASE_CLIENT_EMAIL")
        if not firebase_admin._apps:
            print("   Firebase not initialized")
        return _mock_db  # Mock database for development