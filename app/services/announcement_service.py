
from datetime import datetime
from app.config.firebase_config import get_db

class AnnouncementService:
    def __init__(self):
        self.db_ref = None
    
    def get_db_ref(self):
        """Get database reference"""
        if self.db_ref is None:
            self.db_ref = get_db()
        return self.db_ref
    
    def get_current_announcement(self):
        """Get current announcement"""
        try:
            db_ref = self.get_db_ref()
            announcement_ref = db_ref.child('announcement')
            data = announcement_ref.get()
            
            if data:
                return {
                    'title': data.get('title', 'No Title'),
                    'message': data.get('message', 'No Message'),
                    'updated_at': data.get('updated_at', '')
                }
            else:
                return {
                    'title': 'Knowledge Base Update',
                    'message': "We've updated the chatbot's knowledge base with the latest information. Please review the changes and provide feedback.",
                    'updated_at': ''
                }
                
        except Exception as e:
            print(f"❌ Error getting announcement: {e}")
            return {
                'title': 'Knowledge Base Update',
                'message': "We've updated the chatbot's knowledge base with the latest information. Please review the changes and provide feedback.",
                'updated_at': ''
            }
    
    def update_announcement(self, title: str, message: str) -> bool:
        """Update announcement"""
        try:
            db_ref = self.get_db_ref()
            announcement_ref = db_ref.child('announcement')
            
            announcement_data = {
                'title': title,
                'message': message,
                'updated_at': datetime.now().isoformat()
            }
            
            announcement_ref.set(announcement_data)
            print(f"✅ Announcement updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating announcement: {e}")
            return False

# Global instance
announcement_service = AnnouncementService()
