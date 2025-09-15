from flask import Blueprint, request, jsonify
from app.services.knowledge_service import knowledge_service

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('/', methods=['GET'])
def get_all_knowledge():
    """Get all knowledge entries"""
    try:
        knowledge_list = knowledge_service.get_all_knowledge()
        return jsonify({
            'success': True,
            'data': knowledge_list,
            'total': len(knowledge_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['GET'])
def get_knowledge(knowledge_id):
    """Get single knowledge entry"""
    try:
        knowledge_item = knowledge_service.get_knowledge_by_id(knowledge_id)
        if knowledge_item:
            return jsonify({
                'success': True,
                'knowledge': knowledge_item
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Knowledge not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/', methods=['POST'])
def add_knowledge():
    """Add new knowledge entry"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data or 'answer' not in data:
            return jsonify({
                'success': False,
                'error': 'Question and answer are required'
            }), 400
        
        success = knowledge_service.add_knowledge(
            question=data['question'],
            answer=data['answer'],
            category=data.get('category', 'general'),
            keywords=data.get('keywords', '')
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Knowledge added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add knowledge'}), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['PUT'])
def update_knowledge(knowledge_id):
    """Update existing knowledge entry"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data or 'answer' not in data:
            return jsonify({
                'success': False,
                'error': 'Question and answer are required'
            }), 400
        
        success = knowledge_service.update_knowledge(
            knowledge_id=knowledge_id,
            question=data['question'],
            answer=data['answer'],
            category=data.get('category', 'general'),
            keywords=data.get('keywords', '')
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Knowledge updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update knowledge'}), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['DELETE'])
def delete_knowledge(knowledge_id):
    """Delete knowledge entry"""
    try:
        success = knowledge_service.delete_knowledge(knowledge_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Knowledge deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete knowledge'}), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/stats', methods=['GET'])
def get_knowledge_stats():
    """Get knowledge statistics"""
    try:
        stats = knowledge_service.get_knowledge_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500