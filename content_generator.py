import json
import os
from typing import List, Dict, Any
from openai import OpenAI
import streamlit as st
import google.generativeai as genai
from anthropic import Anthropic
import requests

class ContentGenerator:
    """
    Generates study materials using multiple AI providers for unlimited usage
    Supports OpenAI, Google Gemini, Anthropic Claude, and local models
    """
    
    def __init__(self):
        self.available_providers = []
        self.clients = {}
        
        # Initialize all available AI providers
        self._initialize_providers()
        
        # Set default provider
        self.current_provider = self._get_best_available_provider()
    
    def _initialize_providers(self):
        """Initialize all available AI providers"""
        
        # Google Gemini (Free with generous limits)
        gemini_key = os.getenv("GOOGLE_API_KEY", "")
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                self.clients['gemini'] = genai.GenerativeModel('gemini-1.5-flash')
                self.available_providers.append('gemini')
            except Exception as e:
                st.warning(f"Could not initialize Google Gemini: {str(e)}")
        
        # Anthropic Claude
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        if anthropic_key:
            try:
                self.clients['claude'] = Anthropic(api_key=anthropic_key)
                self.available_providers.append('claude')
            except Exception as e:
                st.warning(f"Could not initialize Anthropic Claude: {str(e)}")
        
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key:
            try:
                self.clients['openai'] = OpenAI(api_key=openai_key)
                self.available_providers.append('openai')
            except Exception as e:
                st.warning(f"Could not initialize OpenAI: {str(e)}")
        
        # Local/Free alternatives (if no API keys available)
        if not self.available_providers:
            self.available_providers.append('local')
            st.info("💡 No API keys found. Using local processing mode with limited functionality.")
    
    def _get_best_available_provider(self):
        """Get the best available provider based on usage limits and capabilities"""
        # Priority: Gemini (free with high limits) > Claude > OpenAI > Local
        priority_order = ['gemini', 'claude', 'openai', 'local']
        
        for provider in priority_order:
            if provider in self.available_providers:
                return provider
        
        return 'local'
    
    def get_provider_info(self):
        """Get information about available providers"""
        provider_info = {
            'gemini': '🆓 Google Gemini - Free with generous limits',
            'claude': '💰 Anthropic Claude - Pay-per-use',
            'openai': '💰 OpenAI GPT-4 - Pay-per-use',
            'local': '🔧 Local processing - Limited functionality'
        }
        
        return {
            'current': provider_info.get(self.current_provider, 'Unknown'),
            'available': [provider_info[p] for p in self.available_providers]
        }
    
    def _generate_with_provider(self, prompt: str, provider: str = None) -> str:
        """Generate content using the specified or current provider"""
        if provider is None:
            provider = self.current_provider
        
        try:
            if provider == 'gemini' and 'gemini' in self.clients:
                response = self.clients['gemini'].generate_content(prompt)
                return response.text
            
            elif provider == 'claude' and 'claude' in self.clients:
                response = self.clients['claude'].messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif provider == 'openai' and 'openai' in self.clients:
                response = self.clients['openai'].chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000
                )
                return response.choices[0].message.content or ""
            
            elif provider == 'local':
                return self._generate_local_content(prompt)
            
            else:
                raise Exception(f"Provider {provider} not available")
        
        except Exception as e:
            st.error(f"Error with {provider}: {str(e)}")
            # Try fallback to next available provider
            remaining_providers = [p for p in self.available_providers if p != provider]
            if remaining_providers:
                st.info(f"Trying fallback provider: {remaining_providers[0]}")
                return self._generate_with_provider(prompt, remaining_providers[0])
            else:
                return ""
    
    def _generate_local_content(self, prompt: str) -> str:
        """Generate basic content using local/template-based approach"""
        if "questions" in prompt.lower():
            return self._create_template_questions()
        elif "flash" in prompt.lower():
            return self._create_template_flashcards()
        elif "summar" in prompt.lower():
            return self._create_template_summary()
        else:
            return ""
    
    def _create_template_questions(self) -> str:
        """Create template questions when no AI provider is available"""
        return json.dumps([
            {
                "type": "conceptual",
                "question": "What are the main concepts covered in this document?",
                "answer": "Please review the document to identify key concepts.",
                "explanation": "This is a template question. Please add API keys for AI-generated content."
            },
            {
                "type": "application",
                "question": "How can the concepts in this document be applied in engineering practice?",
                "answer": "Consider practical applications based on the document content.",
                "explanation": "This is a template question. Please add API keys for AI-generated content."
            }
        ])
    
    def _create_template_flashcards(self) -> str:
        """Create template flashcards when no AI provider is available"""
        return json.dumps([
            {
                "term": "Key Concept 1",
                "definition": "Please review the document to identify key terms and definitions.",
                "explanation": "This is a template flashcard. Please add API keys for AI-generated content."
            },
            {
                "term": "Key Concept 2", 
                "definition": "Please review the document to identify key terms and definitions.",
                "explanation": "This is a template flashcard. Please add API keys for AI-generated content."
            }
        ])
    
    def _create_template_summary(self) -> str:
        """Create template summary when no AI provider is available"""
        return json.dumps({
            "key_concepts": "• Please add API keys to generate AI-powered summaries\n• Template mode provides basic structure only",
            "main_summary": "This is a template summary. To get AI-generated summaries with detailed analysis, please add API keys for Google Gemini (free), Anthropic Claude, or OpenAI.",
            "engineering_applications": "Please add API keys to generate specific engineering applications.",
            "formulas": "Please add API keys to extract and explain mathematical formulas."
        })

    def generate_questions_answers(self, text: str) -> List[Dict[str, Any]]:
        """
        Generate comprehensive questions and answers from document text
        
        Args:
            text (str): Extracted document text
            
        Returns:
            List[Dict]: List of question-answer pairs with explanations
        """
        if not self.available_providers:
            return []
        
        try:
            prompt = f"""You are an expert engineering educator. Based on the following text, generate comprehensive study questions for engineering students.

Create a variety of question types:
1. Multiple choice questions (4 options each)
2. Short answer questions  
3. Conceptual questions
4. Application-based questions

Focus on:
- Key engineering concepts and principles
- Mathematical formulas and derivations
- Practical applications
- Problem-solving approaches
- Critical thinking aspects

For each question, provide:
- Question type
- The question itself
- Options (for multiple choice)
- Correct answer
- Detailed explanation

Generate 8-12 questions total. Return the response as a JSON array with this format:
[
    {{
        "type": "multiple_choice" | "short_answer" | "conceptual" | "application",
        "question": "Question text here",
        "options": ["A", "B", "C", "D"] (only for multiple choice),
        "answer": "Correct answer",
        "explanation": "Detailed explanation"
    }}
]

Document text:
{text[:8000]}"""
            
            content = self._generate_with_provider(prompt)
            if not content:
                return []
            
            # Try to parse as JSON
            try:
                result = json.loads(content)
            except:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    return []
            
            # Ensure we have a list of questions
            if isinstance(result, dict) and 'questions' in result:
                return result['questions']
            elif isinstance(result, list):
                return result
            else:
                return []
                
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return []
    
    def generate_flash_cards(self, text: str) -> List[Dict[str, str]]:
        """
        Generate flash cards with key terms and definitions
        
        Args:
            text (str): Extracted document text
            
        Returns:
            List[Dict]: List of flash card term-definition pairs
        """
        if not self.available_providers:
            return []
        
        try:
            prompt = f"""You are an expert engineering educator. Based on the following text, create comprehensive flash cards for engineering students.

Focus on:
- Key engineering terms and definitions
- Important concepts and principles
- Mathematical formulas and their meanings
- Units and measurements
- Process descriptions
- Technical terminology

For each flash card, provide:
- Term/concept (front of card)
- Clear, concise definition (back of card)
- Additional explanation or context if needed

Create 10-15 flash cards. Return the response as a JSON array with this format:
[
    {{
        "term": "Term or concept name",
        "definition": "Clear, concise definition",
        "explanation": "Additional context or example (optional)"
    }}
]

Document text:
{text[:8000]}"""
            
            content = self._generate_with_provider(prompt)
            if not content:
                return []
            
            # Try to parse as JSON
            try:
                result = json.loads(content)
            except:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    return []
            
            # Ensure we have a list of flash cards
            if isinstance(result, dict) and 'flashcards' in result:
                return result['flashcards']
            elif isinstance(result, dict) and 'cards' in result:
                return result['cards']
            elif isinstance(result, list):
                return result
            else:
                return []
                
        except Exception as e:
            st.error(f"Error generating flash cards: {str(e)}")
            return []
    
    def generate_summaries(self, text: str) -> Dict[str, str]:
        """
        Generate comprehensive summaries and key points
        
        Args:
            text (str): Extracted document text
            
        Returns:
            Dict: Different types of summaries and key information
        """
        if not self.available_providers:
            return {}
        
        try:
            prompt = f"""You are an expert engineering educator. Based on the following text, create comprehensive summaries for engineering students.

Create the following sections:
1. Key Concepts: Main engineering concepts and principles (bullet points)
2. Main Summary: Overall summary of the document content
3. Engineering Applications: Real-world applications and use cases
4. Formulas: Important formulas, equations, or mathematical relationships (if any)

Focus on:
- Essential engineering principles
- Practical applications
- Problem-solving approaches
- Industry relevance
- Mathematical relationships

Return the response as a JSON object with this format:
{{
    "key_concepts": "• Key concept 1\n• Key concept 2\n...",
    "main_summary": "Comprehensive summary of main content",
    "engineering_applications": "Real-world applications and use cases",
    "formulas": "Important formulas and equations (if applicable)"
}}

Document text:
{text[:10000]}"""
            
            content = self._generate_with_provider(prompt)
            if not content:
                return {}
            
            # Try to parse as JSON
            try:
                result = json.loads(content)
            except:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    return {}
            
            return result if isinstance(result, dict) else {}
                
        except Exception as e:
            st.error(f"Error generating summaries: {str(e)}")
            return {}
    
    def _chunk_text(self, text: str, chunk_size: int = 8000) -> List[str]:
        """
        Split large text into manageable chunks for API processing
        
        Args:
            text (str): Text to chunk
            chunk_size (int): Maximum size of each chunk
            
        Returns:
            List[str]: List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_length = word_length
                else:
                    # Word is too long, split it
                    chunks.append(word[:chunk_size])
                    current_chunk = [word[chunk_size:]] if len(word) > chunk_size else []
                    current_length = len(current_chunk[0]) if current_chunk else 0
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
