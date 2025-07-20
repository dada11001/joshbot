#!/usr/bin/env python3
"""
StudyAI Standalone - Engineering Study Assistant
A command-line version of StudyAI that processes documents and generates study materials
without requiring Streamlit.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from document_processor import DocumentProcessor
from content_generator import ContentGenerator
from pdf_exporter import PDFExporter

class StudyAIStandalone:
    def __init__(self, use_ocr: bool = True, provider: str = 'auto'):
        """
        Initialize StudyAI Standalone
        
        Args:
            use_ocr (bool): Enable OCR for image text extraction
            provider (str): AI provider ('gemini', 'claude', 'openai', 'local', 'auto')
        """
        self.doc_processor = DocumentProcessor()
        self.content_generator = ContentGenerator()
        self.pdf_exporter = PDFExporter()
        self.use_ocr = use_ocr
        
        # Set AI provider if specified
        if provider != 'auto' and provider in self.content_generator.available_providers:
            self.content_generator.current_provider = provider
        
        self.study_materials = {
            'questions': [],
            'flashcards': [],
            'summaries': []
        }
    
    def process_document(self, file_path: str) -> str:
        """
        Process a document and extract text content
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            str: Extracted text content
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Processing document: {file_path}")
        
        # Extract text from document
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.txt':
            # Handle text files directly
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        else:
            text_content = self.doc_processor.extract_text(file_path)
        
        if not text_content.strip():
            raise ValueError("No text content extracted from the document")
        
        print(f"Extracted {len(text_content)} characters of text")
        return text_content
    
    def generate_study_materials(self, text_content: str) -> Dict:
        """
        Generate all study materials from text content
        
        Args:
            text_content (str): Document text content
            
        Returns:
            Dict: Generated study materials
        """
        print(f"Generating study materials using {self.content_generator.current_provider}...")
        
        # Generate questions
        print("Generating questions...")
        questions = self.content_generator.generate_questions_answers(text_content)
        self.study_materials['questions'] = questions
        
        # Generate flashcards
        print("Generating flashcards...")
        flashcards = self.content_generator.generate_flash_cards(text_content)
        self.study_materials['flashcards'] = flashcards
        
        # Generate summaries
        print("Generating summaries...")
        summaries = self.content_generator.generate_summaries(text_content)
        self.study_materials['summaries'] = summaries
        
        return self.study_materials
    
    def save_to_json(self, output_path: str) -> None:
        """
        Save study materials to JSON file
        
        Args:
            output_path (str): Path to save JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.study_materials, f, indent=2, ensure_ascii=False)
        print(f"Study materials saved to: {output_path}")
    
    def save_to_pdf(self, output_path: str) -> None:
        """
        Save study materials to PDF file
        
        Args:
            output_path (str): Path to save PDF file
        """
        export_data = {
            'document_name': 'Study Materials',
            'questions_answers': self.study_materials['questions'],
            'flash_cards': self.study_materials['flashcards'],
            'summaries': self.study_materials['summaries']
        }
        pdf_buffer = self.pdf_exporter.create_study_materials_pdf(export_data)
        
        with open(output_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        print(f"Study materials PDF saved to: {output_path}")
    
    def print_summary(self) -> None:
        """Print a summary of generated materials"""
        print("\n" + "="*60)
        print("STUDY MATERIALS GENERATED")
        print("="*60)
        
        # Questions summary
        if self.study_materials['questions']:
            print(f"\n📝 QUESTIONS ({len(self.study_materials['questions'])} total)")
            for i, q in enumerate(self.study_materials['questions'][:3], 1):
                print(f"  {i}. {q.get('question', 'N/A')[:80]}...")
            if len(self.study_materials['questions']) > 3:
                print(f"  ... and {len(self.study_materials['questions']) - 3} more")
        
        # Flashcards summary
        if self.study_materials['flashcards']:
            print(f"\n🗂️ FLASHCARDS ({len(self.study_materials['flashcards'])} total)")
            for i, fc in enumerate(self.study_materials['flashcards'][:3], 1):
                print(f"  {i}. {fc.get('front', 'N/A')[:50]}...")
            if len(self.study_materials['flashcards']) > 3:
                print(f"  ... and {len(self.study_materials['flashcards']) - 3} more")
        
        # Summaries
        if self.study_materials['summaries']:
            print(f"\n📚 SUMMARIES ({len(self.study_materials['summaries'])} total)")
            for i, summary in enumerate(self.study_materials['summaries'][:2], 1):
                title = summary.get('title', f'Summary {i}')
                content = summary.get('content', 'N/A')[:100]
                print(f"  {i}. {title}: {content}...")
        
        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="StudyAI Standalone - Generate study materials from documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python studyai_standalone.py document.pdf
  python studyai_standalone.py document.pdf --output-json materials.json
  python studyai_standalone.py document.pdf --output-pdf materials.pdf
  python studyai_standalone.py document.pdf --no-ocr --provider gemini
  python studyai_standalone.py document.pdf --output-json materials.json --output-pdf materials.pdf
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the input document (PDF, DOC, or DOCX)'
    )
    
    parser.add_argument(
        '--output-json',
        help='Save study materials to JSON file'
    )
    
    parser.add_argument(
        '--output-pdf',
        help='Save study materials to PDF file'
    )
    
    parser.add_argument(
        '--no-ocr',
        action='store_true',
        help='Disable OCR for image text extraction'
    )
    
    parser.add_argument(
        '--provider',
        choices=['gemini', 'claude', 'openai', 'local', 'auto'],
        default='auto',
        help='AI provider to use (default: auto)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress messages'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize StudyAI
        studyai = StudyAIStandalone(
            use_ocr=not args.no_ocr,
            provider=args.provider
        )
        
        # Process document
        text_content = studyai.process_document(args.input_file)
        
        # Generate study materials
        materials = studyai.generate_study_materials(text_content)
        
        # Save outputs
        if args.output_json:
            studyai.save_to_json(args.output_json)
        
        if args.output_pdf:
            studyai.save_to_pdf(args.output_pdf)
        
        # Print summary unless quiet mode
        if not args.quiet:
            studyai.print_summary()
        
        # If no output files specified, create default ones
        if not args.output_json and not args.output_pdf:
            base_name = Path(args.input_file).stem
            default_json = f"{base_name}_study_materials.json"
            default_pdf = f"{base_name}_study_materials.pdf"
            
            studyai.save_to_json(default_json)
            studyai.save_to_pdf(default_pdf)
        
        print(f"\n✅ StudyAI processing completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()