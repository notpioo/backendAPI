from flask import Blueprint, request, jsonify
from app.services.gemini_service import gemini_service
from app.services.knowledge_service import knowledge_service

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/message', methods=['POST'])
def process_message():
    """Process chat message from Flutter app"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data['message']
        
        # Check if message is academically relevant
        if not gemini_service.check_academic_relevance(user_message):
            return jsonify({
                'success': True,
                'response': 'Maaf, saya hanya dapat membantu dengan pertanyaan yang berkaitan dengan akademik, pembelajaran, dan informasi kampus. Silakan ajukan pertanyaan seputar topik tersebut.',
                'source': 'filter'
            })
        
        # Search for relevant knowledge in database
        knowledge_context = knowledge_service.search_knowledge(user_message)
        
        # Generate response using Gemini
        ai_response = gemini_service.generate_response(user_message, knowledge_context)
        
        return jsonify(ai_response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'response': 'Maaf, terjadi kesalahan sistem. Silakan coba lagi.',
            'error': str(e)
        }), 500

@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'chatbot-api',
        'message': 'API is running successfully'
    })