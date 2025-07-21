import json
import os
from typing import List, Dict, Any
import streamlit as st
import google.generativeai as genai

class ContentGenerator:
    """
    Generates study materials exclusively using Google Gemini AI for unlimited usage.
    """
    
    def __init__(self):
        self.available_providers = []
        self.clients = {}
        
        # Initialize Google Gemini AI provider
        self._initialize_providers()
        
        # Set default provider (which will be Gemini if successfully initialized)
        self.current_provider = self._get_best_available_provider()
        if not self.current_provider:
            st.error("No AI provider could be initialized. Please ensure your GEMINI_API_KEY environment variable is correctly set.")
    
    def _initialize_providers(self):
        """Initialize Google Gemini AI provider."""
        
        # Google Gemini (Free with generous limits)
        # It is highly recommended to set your Gemini API key as an environment variable
        # named 'GEMINI_API_KEY'.
        # Example: In your terminal, before running the app:
        # export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
        # The key you provided in the original code, "AIzaSyBVdVRliKttOoto-FnfiQPkmEvlK96TXyM",
        # should be the VALUE of your GEMINI_API_KEY environment variable.
        gemini_key = os.getenv("GEMINI_API_KEY") 
        
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                self.clients['gemini'] = genai.GenerativeModel('gemini-1.5-flash')
                self.available_providers.append('gemini')
            except Exception as e:
                st.error(f"Could not initialize Google Gemini: {str(e)}. "
                         f"Please ensure your GEMINI_API_KEY is valid and has access.")
        else:
            st.warning("GEMINI_API_KEY environment variable not found. Google Gemini AI will not be available.")
    
    def _get_best_available_provider(self):
        """Get the best available provider (Gemini is the only option)."""
        if 'gemini' in self.available_providers:
            return 'gemini'
        return None # Indicate no provider is available
    
    def get_provider_info(self):
        """Get information about the available provider (Gemini only)."""
        provider_info = {
            'gemini': '🆓 Google Gemini - Free with generous limits'
        }
        
        current_provider_display = provider_info.get(self.current_provider, 'No AI provider available')
        available_list = [provider_info[p] for p in self.available_providers if p in provider_info]
        
        return {
            'current': current_provider_display,
            'available': available_list
        }
    
    def _generate_with_provider(self, prompt: str, provider: str = None) -> str:
        """Generate content using the specified or current provider (Gemini only)."""
        if provider is None:
            provider = self.current_provider
        
        if provider != 'gemini' or 'gemini' not in self.clients:
            st.error(f"Gemini provider not available or selected. Current provider: {self.current_provider}. "
                     "No content will be generated.")
            return ""
            
        try:
            response = self.clients['gemini'].generate_content(prompt)
            return response.text
        
        except Exception as e:
            st.error(f"Error with Gemini AI generation: {str(e)}")
            return ""
    
    def generate_questions_answers(self, text: str) -> List[Dict[str, Any]]:
        """
        Generates comprehensive questions and answers from document text using Gemini.
        
        Args:
            text (str): Extracted document text
            
        Returns:
            List[Dict]: List of question-answer pairs with explanations
        """
        if not self.current_provider: # Check if Gemini was successfully initialized
            st.warning("No AI provider available to generate questions.")
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
            except json.JSONDecodeError:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        st.error("Failed to parse JSON even after regex extraction for questions.")
                        return []
                else:
                    st.error("No valid JSON array found in the Gemini response for questions.")
                    return []
            
            # Ensure we have a list of questions
            if isinstance(result, dict) and 'questions' in result:
                return result['questions']
            elif isinstance(result, list):
                return result
            else:
                st.error("Gemini response for questions is not in the expected list format.")
                return []
                
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return []
    
    def generate_flash_cards(self, text: str) -> List[Dict[str, str]]:
        """
        Generates flash cards with key terms and definitions using Gemini.
        
        Args:
            text (str): Extracted document text
            
        Returns:
            List[Dict]: List of flash card term-definition pairs
        """
        if not self.current_provider: # Check if Gemini was successfully initialized
            st.warning("No AI provider available to generate flash cards.")
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
            except json.JSONDecodeError:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        st.error("Failed to parse JSON even after regex extraction for flash cards.")
                        return []
                else:
                    st.error("No valid JSON array found in the Gemini response for flash cards.")
                    return []
            
            # Ensure we have a list of flash cards
            if isinstance(result, dict) and 'flashcards' in result:
                return result['flashcards']
            elif isinstance(result, dict) and 'cards' in result: # Handle alternative keys from AI
                return result['cards']
            elif isinstance(result, list):
                return result
            else:
                st.error("Gemini response for flash cards is not in the expected list format.")
                return []
                
        except Exception as e:
            st.error(f"Error generating flash cards: {str(e)}")
            return []
    
    def generate_summaries(self, text: str) -> Dict[str, str]:
        """
        Generates comprehensive summaries and key points using Gemini.
        
        Args:
            text (str): Extracted document text
            
        Returns:
            Dict: Different types of summaries and key information
        """
        if not self.current_provider: # Check if Gemini was successfully initialized
            st.warning("No AI provider available to generate summaries.")
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
    "key_concepts": "• Key concept 1\\n• Key concept 2\\n...",
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
            except json.JSONDecodeError:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        st.error("Failed to parse JSON even after regex extraction for summaries.")
                        return {}
                else:
                    st.error("No valid JSON object found in the Gemini response for summaries.")
                    return {}
            
            return result if isinstance(result, dict) else {}
                
        except Exception as e:
            st.error(f"Error generating summaries: {str(e)}")
            return {}
    
    def _chunk_text(self, text: str, chunk_size: int = 8000) -> List[str]:
        """
        Split large text into manageable chunks for API processing.
        This method is kept for potential future use or if Gemini's
        context window changes or smaller models are used.
        The current generation prompts already limit input text size.
        
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
                    # If a single word is larger than chunk_size, split it
                    # This is a rare edge case for natural language but handled for robustness.
                    chunks.append(word[:chunk_size])
                    current_chunk = [word[chunk_size:]] if len(word) > chunk_size else []
                    current_length = len(current_chunk[0]) if current_chunk else 0
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
