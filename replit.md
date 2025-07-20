# StudyAI - Engineering Study Assistant

## Overview

StudyAI is a Streamlit-based web application designed to help engineering students transform their study documents into comprehensive learning materials. The application processes uploaded PDF and DOC/DOCX files, extracting text content and using OpenAI's GPT-4o model to generate study questions, flash cards, and summaries. It also provides PDF export functionality for all generated materials.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **UI Pattern**: Multi-page application with sidebar navigation
- **State Management**: Streamlit's built-in session state for maintaining data across page interactions
- **Layout**: Wide layout with expandable sidebar for navigation

### Backend Architecture
- **Modular Design**: Separated into distinct processing modules:
  - Document processing (text extraction)
  - Content generation (AI-powered study material creation)
  - PDF export (formatted output generation)
  - Utilities (session management and UI helpers)
- **API Integration**: Direct integration with OpenAI API for content generation
- **File Processing**: Local file handling for document uploads and processing

## Key Components

### 1. Document Processor (`document_processor.py`)
- **Purpose**: Handles text extraction from uploaded documents including images within PDFs
- **Supported Formats**: PDF (.pdf), Word documents (.doc, .docx)
- **Libraries**: 
  - PyMuPDF (primary) and PyPDF2 (fallback) for PDF processing
  - python-docx for Word documents
  - Tesseract OCR and PyTesseract for image text extraction
  - Pillow (PIL) for image processing
- **Features**:
  - Advanced PDF text extraction with OCR support
  - Extracts text from images, diagrams, and scanned content in PDFs
  - User-configurable OCR toggle
  - Fallback mechanisms for robust document processing
- **Error Handling**: Comprehensive exception handling for file processing and OCR failures

### 2. Content Generator (`content_generator.py`)
- **Purpose**: AI-powered generation of study materials with unlimited usage options
- **AI Providers**: 
  - **Google Gemini** (primary, free with generous limits)
  - **Anthropic Claude** (pay-per-use)
  - **OpenAI GPT-4o** (pay-per-use) 
  - **Local processing** (basic templates when no API keys available)
- **Content Types**: 
  - Multiple choice questions
  - Short answer questions
  - Conceptual questions
  - Application-based questions
  - Flash cards
  - Summaries
- **Features**:
  - Multi-provider support for unlimited usage
  - Automatic fallback between providers
  - Smart provider selection based on availability and cost
  - Template-based local processing as backup
- **API Management**: Handles multiple API key configurations and provider switching

### 3. PDF Exporter (`pdf_exporter.py`)
- **Purpose**: Creates formatted PDF exports of generated study materials
- **Library**: ReportLab for PDF generation
- **Features**: Custom styling, multi-page documents, tables, and formatted layouts
- **Output**: Professional-looking study materials ready for printing or digital use

### 4. Main Application (`app.py`)
- **Purpose**: Orchestrates the entire application flow
- **Navigation**: Multi-page interface with sections for:
  - Document upload
  - Questions & answers
  - Flash cards
  - Summaries
  - Export materials

### 5. Standalone Version (`studyai_standalone.py`)
- **Purpose**: Command-line version for automation and integration
- **Features**:
  - Full command-line interface with argument parsing
  - Programmatic API for custom applications
  - Support for PDF, DOC, DOCX, and TXT files
  - JSON and PDF output formats
  - Multi-provider AI support with automatic selection
  - Batch processing capabilities
- **Usage Examples**:
  - `python studyai_standalone.py document.pdf`
  - `python studyai_standalone.py document.pdf --provider gemini --output-pdf study_guide.pdf`
  - Integration into other Python applications

### 6. Utilities (`utils.py`)
- **Purpose**: Common functionality and session state management
- **Features**: Error/success message formatting, session variable initialization

## Data Flow

1. **Document Upload**: User uploads PDF or Word document through Streamlit interface
2. **Text Extraction**: Document processor extracts raw text content from uploaded file
3. **Content Generation**: OpenAI API processes extracted text to generate study materials
4. **Session Storage**: Generated content stored in Streamlit session state for persistence
5. **Material Display**: Users can navigate between different types of generated content
6. **Export**: PDF exporter creates downloadable study materials

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **OpenAI**: AI content generation via GPT-4o
- **PyMuPDF**: Advanced PDF processing and text extraction
- **PyPDF2**: Fallback PDF text extraction
- **python-docx**: Word document processing
- **ReportLab**: PDF generation and formatting
- **Tesseract/PyTesseract**: OCR for image text extraction
- **Pillow (PIL)**: Image processing and manipulation

### API Dependencies
- **Google Gemini API**: Free tier with generous limits, set as environment variable `GOOGLE_API_KEY` (recommended)
- **Anthropic Claude API**: Pay-per-use, set as environment variable `ANTHROPIC_API_KEY`
- **OpenAI API**: Pay-per-use, set as environment variable `OPENAI_API_KEY`
- **Fallback**: Local template-based processing when no API keys are available
- **Models**: Gemini-1.5-flash, Claude-3-haiku, GPT-4o respectively

## Recent Changes

### July 20, 2025
- **Added Standalone Version**: Created `studyai_standalone.py` for command-line usage and integration
- **Multi-Format Support**: Enhanced document processing to support PDF, DOC, DOCX, and TXT files
- **Command-Line Interface**: Full CLI with argument parsing, provider selection, and output control
- **Programmatic API**: Standalone version can be imported and used in other Python applications
- **Batch Processing**: Supports automated processing of multiple documents
- **Enhanced AI Integration**: Confirmed Google Gemini API working with unlimited free usage

## Deployment Strategy

### Web Application (Streamlit)
- **Environment Setup**: Python-based application suitable for various deployment platforms
- **API Configuration**: Google Gemini API key set as environment variable for unlimited usage
- **Dependencies**: Managed through standard Python package management
- **Layout**: Wide page layout optimized for document processing workflows
- **Session Management**: Session state ensures data persistence during user interactions

### Standalone Application
- **Command-Line Tool**: Direct execution with `python studyai_standalone.py`
- **Programmatic Integration**: Import as module for custom applications
- **Automation Ready**: Supports batch processing and scripting
- **Cross-Platform**: Works on any system with Python and required dependencies

### File Handling
- **Temporary Processing**: Uploaded documents processed in memory
- **Multiple Formats**: PDF (with OCR), DOC, DOCX, TXT support
- **PDF Generation**: In-memory PDF creation for downloads
- **No Persistent Storage**: All content exists in session state or returned directly

### Security Considerations
- **API Key Management**: Environment variables for secure key storage
- **File Type Validation**: Processing limited to supported document types
- **Error Handling**: Comprehensive error management prevents information exposure
- **Multi-Provider Fallback**: Automatic fallback between AI providers ensures reliability