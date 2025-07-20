import streamlit as st
from typing import Any, Dict

def initialize_session_state():
    """
    Initialize session state variables for the application
    """
    # Initialize session state variables if they don't exist
    session_variables = [
        'extracted_text',
        'document_name', 
        'questions_answers',
        'flash_cards',
        'summaries',
        'current_card',
        'show_answer'
    ]
    
    for var in session_variables:
        if var not in st.session_state:
            if var == 'current_card':
                st.session_state[var] = 0
            elif var == 'show_answer':
                st.session_state[var] = False
            else:
                st.session_state[var] = None

def display_error_message(message: str):
    """
    Display a formatted error message
    
    Args:
        message (str): Error message to display
    """
    st.error(f"❌ **Error:** {message}")

def display_success_message(message: str):
    """
    Display a formatted success message
    
    Args:
        message (str): Success message to display
    """
    st.success(f"✅ **Success:** {message}")

def display_warning_message(message: str):
    """
    Display a formatted warning message
    
    Args:
        message (str): Warning message to display
    """
    st.warning(f"⚠️ **Warning:** {message}")

def display_info_message(message: str):
    """
    Display a formatted info message
    
    Args:
        message (str): Info message to display
    """
    st.info(f"ℹ️ **Info:** {message}")

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes = int(size_bytes / 1024.0)
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_openai_response(response_data: Any, expected_type: type = list) -> bool:
    """
    Validate OpenAI API response data
    
    Args:
        response_data (Any): Response data to validate
        expected_type (type): Expected data type
        
    Returns:
        bool: True if valid, False otherwise
    """
    if response_data is None:
        return False
    
    if expected_type == list:
        return isinstance(response_data, list) and len(response_data) > 0
    elif expected_type == dict:
        return isinstance(response_data, dict) and len(response_data) > 0
    else:
        return isinstance(response_data, expected_type)

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length before truncation
        suffix (str): Suffix to add when truncated
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def clean_filename(filename: str) -> str:
    """
    Clean filename for safe file operations
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Cleaned filename
    """
    # Remove or replace invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    cleaned = filename
    
    for char in invalid_chars:
        cleaned = cleaned.replace(char, '_')
    
    # Remove multiple consecutive underscores
    import re
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Remove leading/trailing underscores and whitespace
    cleaned = cleaned.strip('_ ')
    
    return cleaned if cleaned else "study_materials"

def get_question_type_emoji(question_type: str) -> str:
    """
    Get emoji for question type
    
    Args:
        question_type (str): Type of question
        
    Returns:
        str: Corresponding emoji
    """
    emoji_map = {
        'multiple_choice': '🔤',
        'short_answer': '✏️',
        'conceptual': '💭',
        'application': '⚙️',
        'true_false': '✅❌',
        'fill_in_blank': '📝'
    }
    
    return emoji_map.get(question_type, '❓')

def create_progress_indicator(current: int, total: int, label: str = "Progress") -> None:
    """
    Create a progress indicator with label
    
    Args:
        current (int): Current progress value
        total (int): Total progress value
        label (str): Progress label
    """
    if total > 0:
        progress = current / total
        st.progress(progress)
        st.caption(f"{label}: {current}/{total} ({progress:.1%})")
    else:
        st.progress(0)
        st.caption(f"{label}: 0/0")

def count_words(text: str) -> int:
    """
    Count words in text
    
    Args:
        text (str): Text to count words in
        
    Returns:
        int: Word count
    """
    if not text:
        return 0
    
    return len(text.split())

def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Estimate reading time for text
    
    Args:
        text (str): Text to estimate reading time for
        words_per_minute (int): Average reading speed
        
    Returns:
        int: Estimated reading time in minutes
    """
    word_count = count_words(text)
    return max(1, round(word_count / words_per_minute))
