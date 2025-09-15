import json
import logging
import os
from typing import Optional

from google import genai
from google.genai import types

class GeminiService:
    def __init__(self):
        self._initialize_client()
        self.model = "gemini-2.5-flash"
    
    def _initialize_client(self):
        """Initialize or reinitialize the Gemini client"""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        self.client = genai.Client(api_key=api_key)
    
    def reload_api_key(self):
        """Reload API key from environment and reinitialize client"""
        try:
            self._initialize_client()
            return True
        except Exception as e:
            logging.error(f"Failed to reload API key: {e}")
            return False
        
        # Academic context prompt for consistent responses
        self.system_prompt = """
        Anda adalah asisten virtual akademik kampus yang membantu mahasiswa dengan informasi umum, akademik, dan pembelajaran. 
        
        Aturan penting:
        1. PRIORITASKAN informasi dari konteks pengetahuan yang disediakan
        2. Jika ada informasi spesifik di konteks pengetahuan, gunakan informasi tersebut sebagai jawaban utama
        3. PAHAMI maksud pertanyaan meskipun disampaikan dengan cara yang berbeda:
           - "siapa nama rektor" = "kamu tau ga nama rektor" = "nama rektor siapa"
           - "universitas prabumulih" = "kampus prabumulih" = "perguruan tinggi prabumulih"
        4. Hanya jawab pertanyaan yang berkaitan dengan:
           - Informasi umum tentang kampus dan pendidikan
           - Materi pembelajaran dan akademik
           - Prosedur dan kebijakan kampus
           - Panduan belajar dan tips akademik
        
        5. Jika pertanyaan di luar topik akademik, sopan menolak dan arahkan kembali ke topik akademik
        6. Gunakan bahasa Indonesia yang natural dan ramah
        7. Berikan jawaban yang informatif dan membantu
        8. Jika tidak ada informasi di konteks pengetahuan dan tidak yakin, sampaikan bahwa perlu konfirmasi lebih lanjut
        
        Selalu jawab dengan nada yang supportif dan mendorong pembelajaran.
        """
    
    def generate_response(self, user_message: str, knowledge_context: str = "") -> dict:
        """
        Generate response using Gemini AI with academic context
        """
        try:
            # Ensure client is initialized with current API key
            if not hasattr(self, 'client') or not self.client:
                self._initialize_client()
            # Combine system prompt, knowledge context, and user message
            if knowledge_context:
                full_prompt = f"""
                {self.system_prompt}
                
                KONTEKS PENGETAHUAN SPESIFIK (GUNAKAN INI SEBAGAI PRIORITAS UTAMA):
                {knowledge_context}
                
                Pertanyaan mahasiswa: {user_message}
                
                Instruksi: Gunakan informasi dari konteks pengetahuan di atas untuk menjawab pertanyaan. Jika konteks pengetahuan mengandung jawaban yang relevan, berikan jawaban berdasarkan informasi tersebut. Jawab dalam bahasa Indonesia dengan ramah dan informatif.
                """
            else:
                full_prompt = f"""
                {self.system_prompt}
                
                Pertanyaan mahasiswa: {user_message}
                
                Catatan: Tidak ada konteks pengetahuan spesifik yang ditemukan untuk pertanyaan ini. Berikan jawaban umum yang membantu atau arahkan untuk mendapatkan informasi lebih lanjut.
                """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt
            )
            
            if response.text:
                return {
                    "success": True,
                    "response": response.text,
                    "source": "gemini-ai"
                }
            else:
                return {
                    "success": False,
                    "response": "Maaf, saya tidak dapat memproses pertanyaan Anda saat ini. Silakan coba lagi.",
                    "error": "Empty response from AI"
                }
                
        except Exception as e:
            logging.error(f"Gemini API error: {e}")
            return {
                "success": False,
                "response": "Maaf, terjadi kesalahan sistem. Silakan coba lagi dalam beberapa saat.",
                "error": str(e)
            }
    
    def check_academic_relevance(self, message: str) -> bool:
        """
        Check if the message is academically relevant using AI
        """
        try:
            relevance_prompt = f"""
            Tentukan apakah pertanyaan berikut relevan dengan topik akademik, pendidikan, atau kampus.
            
            Pertanyaan: "{message}"
            
            Jawab hanya dengan "YA" jika relevan dengan akademik/pendidikan/kampus, atau "TIDAK" jika tidak relevan.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=relevance_prompt
            )
            
            if response.text:
                return response.text.strip().upper() == "YA"
            return False
            
        except Exception as e:
            logging.error(f"Academic relevance check error: {e}")
            # Default to allowing the question if check fails
            return True

# Global instance
gemini_service = GeminiService()