from app.config.firebase_config import get_db
from typing import List, Dict, Optional
import uuid
from datetime import datetime

class KnowledgeService:
    def __init__(self):
        pass  # Don't store db_ref in init, get it fresh each time
    
    def get_db_ref(self):
        return get_db()
    
    def get_all_knowledge(self) -> List[Dict]:
        """Get all knowledge entries from Firebase"""
        try:
            knowledge_ref = self.get_db_ref().child('knowledge')
            knowledge_data = knowledge_ref.get()
            
            if knowledge_data and isinstance(knowledge_data, dict):
                knowledge_list = []
                for key, value in knowledge_data.items():
                    if isinstance(value, dict):
                        value['id'] = key
                        knowledge_list.append(value)
                return knowledge_list
            return []
            
        except Exception as e:
            print(f"Error getting knowledge: {e}")
            return []
    
    def get_knowledge_by_id(self, knowledge_id: str) -> Optional[Dict]:
        """Get single knowledge entry by ID"""
        try:
            knowledge_ref = self.get_db_ref().child('knowledge').child(knowledge_id)
            knowledge_data = knowledge_ref.get()
            
            if knowledge_data and isinstance(knowledge_data, dict):
                knowledge_data['id'] = knowledge_id
                return knowledge_data
            return None
            
        except Exception as e:
            print(f"Error getting knowledge by ID: {e}")
            return None
    
    def search_knowledge(self, query: str) -> str:
        """Search for relevant knowledge based on query with improved semantic matching"""
        try:
            knowledge_list = self.get_all_knowledge()
            relevant_context = []
            
            query_lower = query.lower()
            query_words = query_lower.split()
            
            print(f"🔍 Searching for: '{query}' in {len(knowledge_list)} knowledge entries")
            
            # Define synonyms and related terms for better matching
            synonyms = {
                'rektor': ['kepala', 'pimpinan', 'pemimpin', 'direktur', 'ketua'],
                'universitas': ['kampus', 'perguruan tinggi', 'univ', 'pt'],
                'prabumulih': ['prabumullih', 'prabumullih'],
                'nama': ['siapa', 'namanya', 'identitas'],
                'tau': ['tahu', 'kenal', 'mengetahui'],
                'dari': ['di', 'pada', 'untuk'],
                'adalah': ['yaitu', 'ialah', 'merupakan']
            }
            
            # Normalize query by expanding with synonyms
            expanded_query_words = set(query_words)
            for word in query_words:
                if word in synonyms:
                    expanded_query_words.update(synonyms[word])
            
            # Remove common stop words that don't add meaning
            stop_words = {'yang', 'adalah', 'dan', 'atau', 'di', 'ke', 'dari', 'untuk', 'dengan', 
                         'pada', 'dalam', 'ini', 'itu', 'ya', 'sih', 'kah', 'ga', 'tidak', 'bukan',
                         'kan', 'dong', 'kok', 'gimana', 'bagaimana', 'apa', 'kapan', 'dimana'}
            
            meaningful_words = [word for word in expanded_query_words if word not in stop_words and len(word) > 2]
            
            print(f"🔍 Expanded search terms: {meaningful_words}")
            
            for item in knowledge_list:
                question = item.get('question', '').lower()
                answer = item.get('answer', '').lower()
                keywords = item.get('keywords', '').lower()
                category = item.get('category', '').lower()
                
                # Combine all searchable text
                all_text = f"{question} {answer} {keywords} {category}"
                
                # Check for exact phrase match first
                if query_lower in all_text:
                    relevant_context.append({
                        'content': f"Q: {item.get('question', '')}\nA: {item.get('answer', '')}",
                        'score': 100,
                        'match_type': 'exact'
                    })
                    print(f"✅ Exact match found: {item.get('question', '')[:50]}...")
                    continue
                
                # Calculate semantic similarity score
                match_score = 0
                matches_found = []
                
                for word in meaningful_words:
                    # Direct word match
                    if word in all_text:
                        match_score += 2
                        matches_found.append(word)
                    # Partial word match (for typos or variations)
                    else:
                        for text_word in all_text.split():
                            if len(word) > 3 and len(text_word) > 3:
                                # Check for partial matches (like "prabumulih" vs "prabumullih")
                                if (word in text_word or text_word in word or 
                                    self._calculate_similarity(word, text_word) > 0.7):
                                    match_score += 1
                                    matches_found.append(f"{word}~{text_word}")
                
                # Calculate final score based on meaningful word matches
                if len(meaningful_words) > 0:
                    final_score = (match_score / len(meaningful_words)) * 100
                    
                    # Lower threshold for better recall
                    if final_score >= 30:  # Reduced from 50% to 30%
                        relevant_context.append({
                            'content': f"Q: {item.get('question', '')}\nA: {item.get('answer', '')}",
                            'score': final_score,
                            'match_type': 'semantic',
                            'matches': matches_found
                        })
                        print(f"🎯 Semantic match found: {item.get('question', '')[:50]}... (score: {final_score:.1f}%, matches: {matches_found})")
            
            # Sort by score (highest first)
            relevant_context.sort(key=lambda x: x['score'], reverse=True)
            
            # Return top 3 matches
            result_content = []
            for item in relevant_context[:3]:
                result_content.append(item['content'])
            
            result = "\n\n".join(result_content)
            print(f"📋 Found {len(relevant_context)} matches, returning {min(3, len(relevant_context))}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error searching knowledge: {e}")
            return ""
    
    def _calculate_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity between two words using simple character overlap"""
        if not word1 or not word2:
            return 0.0
        
        # Simple character-based similarity
        set1 = set(word1.lower())
        set2 = set(word2.lower())
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def add_knowledge(self, question: str, answer: str, category: str = "general", keywords: str = "") -> bool:
        """Add new knowledge entry"""
        try:
            db_ref = self.get_db_ref()
            knowledge_ref = db_ref.child('knowledge')
            new_entry = {
                'question': question,
                'answer': answer,
                'category': category,
                'keywords': keywords,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Debug logging
            print(f"🔥 Adding knowledge to database type: {type(db_ref)}")
            print(f"🔥 Database reference: {db_ref}")
            
            knowledge_ref.push().set(new_entry)
            print(f"✅ Knowledge added successfully: {question[:50]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error adding knowledge: {e}")
            return False
    
    def update_knowledge(self, knowledge_id: str, question: str, answer: str, category: str = "general", keywords: str = "") -> bool:
        """Update existing knowledge entry"""
        try:
            knowledge_ref = self.get_db_ref().child('knowledge').child(knowledge_id)
            updated_entry = {
                'question': question,
                'answer': answer,
                'category': category,
                'keywords': keywords,
                'updated_at': datetime.now().isoformat()
            }
            
            knowledge_ref.update(updated_entry)
            return True
            
        except Exception as e:
            print(f"Error updating knowledge: {e}")
            return False
    
    def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete knowledge entry"""
        try:
            knowledge_ref = self.get_db_ref().child('knowledge').child(knowledge_id)
            knowledge_ref.delete()
            return True
            
        except Exception as e:
            print(f"Error deleting knowledge: {e}")
            return False
    
    def get_knowledge_stats(self) -> Dict:
        """Get knowledge statistics"""
        try:
            knowledge_list = self.get_all_knowledge()
            total_knowledge = len(knowledge_list)
            
            # Count by category
            categories = {}
            for item in knowledge_list:
                category = item.get('category', 'general')
                categories[category] = categories.get(category, 0) + 1
            
            return {
                'total_knowledge': total_knowledge,
                'categories': categories
            }
            
        except Exception as e:
            print(f"Error getting knowledge stats: {e}")
            return {'total_knowledge': 0, 'categories': {}}

# Global instance
knowledge_service = KnowledgeService()