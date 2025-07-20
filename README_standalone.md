# StudyAI Standalone

A command-line version of StudyAI that processes documents and generates study materials without requiring Streamlit.

## Quick Start

### Command Line Usage

```bash
# Basic usage
python studyai_standalone.py document.pdf

# Save to specific files
python studyai_standalone.py document.pdf --output-json materials.json --output-pdf materials.pdf

# Use specific AI provider
python studyai_standalone.py document.pdf --provider gemini

# Disable OCR for faster processing
python studyai_standalone.py document.pdf --no-ocr

# Quiet mode (minimal output)
python studyai_standalone.py document.pdf --quiet
```

### Programmatic Usage

```python
from studyai_standalone import StudyAIStandalone

# Initialize
studyai = StudyAIStandalone(use_ocr=True, provider='gemini')

# Process document
text_content = studyai.process_document('my_document.pdf')

# Generate study materials
materials = studyai.generate_study_materials(text_content)

# Save outputs
studyai.save_to_json('study_materials.json')
studyai.save_to_pdf('study_materials.pdf')

# Print summary
studyai.print_summary()
```

## Features

- **Document Processing**: PDF, DOC, DOCX support
- **OCR Support**: Extract text from images in PDFs
- **Multi-AI Providers**: Google Gemini (free), Claude, OpenAI, Local mode
- **Multiple Output Formats**: JSON and PDF export
- **Command Line Interface**: Easy automation and scripting
- **Programmatic API**: Integrate into your own applications

## AI Providers

1. **Google Gemini** (Recommended - Free)
   - Generous free limits
   - High quality results
   - No API costs

2. **Anthropic Claude** (Pay-per-use)
   - Excellent for complex analysis
   - Requires ANTHROPIC_API_KEY

3. **OpenAI GPT-4** (Pay-per-use)
   - Industry standard
   - Requires OPENAI_API_KEY

4. **Local Mode** (Fallback)
   - Basic templates
   - No internet required
   - Limited functionality

## Environment Variables

Set these environment variables to enable AI providers:

```bash
export GOOGLE_API_KEY="your_gemini_api_key"      # For Google Gemini
export ANTHROPIC_API_KEY="your_claude_api_key"   # For Claude
export OPENAI_API_KEY="your_openai_api_key"      # For OpenAI
```

## Output Formats

### JSON Output
Contains structured data with questions, flashcards, and summaries that can be processed by other applications.

### PDF Output
Professional formatted study materials ready for printing or digital use.

## Examples

### Process Engineering Textbook
```bash
python studyai_standalone.py engineering_textbook.pdf --provider gemini --output-pdf study_guide.pdf
```

### Batch Process Multiple Documents
```bash
for file in *.pdf; do
    python studyai_standalone.py "$file" --provider gemini --quiet
done
```

### Integration with Other Tools
```python
import subprocess
import json

# Process document
result = subprocess.run([
    'python', 'studyai_standalone.py', 
    'document.pdf', 
    '--output-json', 'temp.json',
    '--quiet'
], capture_output=True, text=True)

# Load generated materials
with open('temp.json') as f:
    materials = json.load(f)

# Use materials in your application
for question in materials['questions']:
    print(f"Q: {question['question']}")
    print(f"A: {question['answer']}")
```

## Requirements

All dependencies are included in the main project:
- document_processor.py
- content_generator.py  
- pdf_exporter.py
- Required Python packages (see pyproject.toml)

## Error Handling

The standalone version includes comprehensive error handling:
- File not found errors
- Empty document detection
- AI provider failures with automatic fallback
- Network connectivity issues
- Invalid file format detection