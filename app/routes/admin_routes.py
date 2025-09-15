import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.services.knowledge_service import knowledge_service
from app.services.announcement_service import announcement_service

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    try:
        stats = knowledge_service.get_knowledge_stats()
        announcement = announcement_service.get_current_announcement()
        return render_template('dashboard.html', stats=stats, announcement=announcement)
    except Exception as e:
        return render_template('dashboard.html', stats={'total_knowledge': 0, 'categories': {}}, announcement={'title': 'Announcement', 'message': 'No announcement available'})

@admin_bp.route('/knowledge')
def knowledge_management():
    """Knowledge management page"""
    try:
        knowledge_list = knowledge_service.get_all_knowledge()
        return render_template('knowledge.html', knowledge_list=knowledge_list)
    except Exception as e:
        return render_template('knowledge.html', knowledge_list=[])

@admin_bp.route('/testing')
def chatbot_testing():
    """Chatbot testing page"""
    return render_template('testing.html')

@admin_bp.route('/models')
def models():
    """Models management page"""
    return render_template('models.html')

@admin_bp.route('/announcement')
def announcement():
    """Announcement management page"""
    return render_template('announcement.html')

@admin_bp.route('/api-docs')
def api_docs():
    """API documentation page"""
    return render_template('api_docs.html')

@admin_bp.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

@admin_bp.route('/api/models/current-api-key')
def get_current_api_key():
    """Get current GEMINI API key"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            return jsonify({
                "success": True,
                "api_key": api_key
            })
        else:
            return jsonify({
                "success": False,
                "message": "No API key configured",
                "api_key": ""
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "api_key": ""
        }), 500

@admin_bp.route('/api/models/update-api-key', methods=['POST'])
def update_api_key():
    """Update GEMINI API key"""
    try:
        data = request.get_json()
        new_api_key = data.get('api_key', '').strip()
        
        if not new_api_key:
            return jsonify({
                "success": False,
                "message": "API key cannot be empty"
            }), 400
        
        # Validate API key format (basic validation)
        if not new_api_key.startswith('AIza') or len(new_api_key) < 30:
            return jsonify({
                "success": False,
                "message": "Invalid API key format. GEMINI API keys should start with 'AIza'"
            }), 400
        
        # Update environment variable (note: this is temporary in runtime)
        os.environ["GEMINI_API_KEY"] = new_api_key
        
        # Test the API key by trying to initialize the service
        try:
            from app.services.gemini_service import GeminiService
            test_service = GeminiService()
            # You could add a simple test call here if needed
            
            return jsonify({
                "success": True,
                "message": "API key updated successfully"
            })
            
        except Exception as api_error:
            return jsonify({
                "success": False,
                "message": f"API key validation failed: {str(api_error)}"
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500