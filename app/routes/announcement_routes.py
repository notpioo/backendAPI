
from flask import Blueprint, request, jsonify
from app.services.announcement_service import announcement_service

announcement_bp = Blueprint('announcement', __name__)

@announcement_bp.route('/', methods=['GET'])
def get_announcement():
    """Get current announcement"""
    try:
        announcement = announcement_service.get_current_announcement()
        return jsonify({
            'success': True,
            'data': announcement
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@announcement_bp.route('/', methods=['POST'])
def update_announcement():
    """Update announcement"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        
        if not title or not message:
            return jsonify({
                'success': False,
                'error': 'Title and message are required'
            }), 400
        
        success = announcement_service.update_announcement(title, message)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Announcement updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update announcement'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
