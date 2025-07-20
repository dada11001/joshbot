from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, darkblue, darkgreen, red
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any
import streamlit as st

class PDFExporter:
    """
    Handles PDF export functionality for study materials
    Creates formatted PDFs containing questions, flash cards, and summaries
    """
    
    def __init__(self):
        # Get standard styles
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles for the PDF"""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=darkgreen,
            fontName='Helvetica-Bold'
        )
        
        # Question style
        self.question_style = ParagraphStyle(
            'Question',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        # Answer style
        self.answer_style = ParagraphStyle(
            'Answer',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=20,
            fontName='Helvetica'
        )
        
        # Flash card term style
        self.flashcard_term_style = ParagraphStyle(
            'FlashcardTerm',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=darkblue
        )
        
        # Flash card definition style
        self.flashcard_def_style = ParagraphStyle(
            'FlashcardDefinition',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            leftIndent=15,
            fontName='Helvetica'
        )
    
    def create_study_materials_pdf(self, export_data: Dict[str, Any]) -> BytesIO:
        """
        Create a comprehensive PDF with all study materials
        
        Args:
            export_data (Dict): Dictionary containing study materials data
            
        Returns:
            BytesIO: PDF file buffer
        """
        buffer = BytesIO()
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build PDF content
            story = []
            
            # Add title page
            self._add_title_page(story, export_data['document_name'])
            
            # Add questions and answers section
            if export_data.get('questions_answers'):
                self._add_questions_section(story, export_data['questions_answers'])
            
            # Add flash cards section
            if export_data.get('flash_cards'):
                self._add_flashcards_section(story, export_data['flash_cards'])
            
            # Add summaries section
            if export_data.get('summaries'):
                self._add_summaries_section(story, export_data['summaries'])
            
            # Build the PDF
            doc.build(story)
            buffer.seek(0)
            
        except Exception as e:
            st.error(f"Error creating PDF: {str(e)}")
            raise
        
        return buffer
    
    def _add_title_page(self, story: List, document_name: str):
        """Add title page to the PDF"""
        
        # Main title
        title = Paragraph("StudyAI - Engineering Study Materials", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        # Document name
        doc_title = Paragraph(f"Generated from: {document_name}", self.styles['Heading2'])
        story.append(doc_title)
        story.append(Spacer(1, 0.3*inch))
        
        # Generation date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"Generated on: {date_str}", self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 0.5*inch))
        
        # Description
        description = Paragraph(
            "This document contains comprehensive study materials including questions & answers, "
            "flash cards, and summaries generated specifically for engineering students.",
            self.styles['Normal']
        )
        story.append(description)
        
        # Add page break
        story.append(PageBreak())
    
    def _add_questions_section(self, story: List, questions_answers: List[Dict]):
        """Add questions and answers section to the PDF"""
        
        # Section header
        header = Paragraph("Questions & Answers", self.section_style)
        story.append(header)
        story.append(Spacer(1, 0.2*inch))
        
        for i, qa in enumerate(questions_answers, 1):
            # Question number and type
            q_header = f"Question {i} ({qa.get('type', 'Unknown').replace('_', ' ').title()})"
            story.append(Paragraph(q_header, self.question_style))
            
            # Question text
            story.append(Paragraph(f"Q: {qa['question']}", self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Multiple choice options
            if qa.get('type') == 'multiple_choice' and qa.get('options'):
                for j, option in enumerate(qa['options'], 1):
                    option_para = Paragraph(f"{j}. {option}", self.answer_style)
                    story.append(option_para)
                story.append(Spacer(1, 0.1*inch))
            
            # Answer
            story.append(Paragraph(f"<b>Answer:</b> {qa['answer']}", self.answer_style))
            
            # Explanation
            if qa.get('explanation'):
                story.append(Paragraph(f"<b>Explanation:</b> {qa['explanation']}", self.answer_style))
            
            story.append(Spacer(1, 0.2*inch))
        
        story.append(PageBreak())
    
    def _add_flashcards_section(self, story: List, flash_cards: List[Dict]):
        """Add flash cards section to the PDF"""
        
        # Section header
        header = Paragraph("Flash Cards", self.section_style)
        story.append(header)
        story.append(Spacer(1, 0.2*inch))
        
        # Description
        description = Paragraph(
            "Use these flash cards to test your knowledge of key terms and concepts.",
            self.styles['Normal']
        )
        story.append(description)
        story.append(Spacer(1, 0.2*inch))
        
        for i, card in enumerate(flash_cards, 1):
            # Card number
            card_header = Paragraph(f"Flash Card {i}", self.styles['Heading3'])
            story.append(card_header)
            
            # Term
            story.append(Paragraph(f"<b>Term/Concept:</b> {card['term']}", self.flashcard_term_style))
            
            # Definition
            story.append(Paragraph(f"<b>Definition:</b> {card['definition']}", self.flashcard_def_style))
            
            # Additional explanation
            if card.get('explanation'):
                story.append(Paragraph(f"<b>Additional Context:</b> {card['explanation']}", self.flashcard_def_style))
            
            story.append(Spacer(1, 0.15*inch))
        
        story.append(PageBreak())
    
    def _add_summaries_section(self, story: List, summaries: Dict[str, str]):
        """Add summaries section to the PDF"""
        
        # Section header
        header = Paragraph("Summaries & Key Information", self.section_style)
        story.append(header)
        story.append(Spacer(1, 0.2*inch))
        
        # Key concepts
        if summaries.get('key_concepts'):
            subheader = Paragraph("Key Concepts", self.styles['Heading3'])
            story.append(subheader)
            story.append(Paragraph(summaries['key_concepts'], self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Main summary
        if summaries.get('main_summary'):
            subheader = Paragraph("Main Summary", self.styles['Heading3'])
            story.append(subheader)
            story.append(Paragraph(summaries['main_summary'], self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Engineering applications
        if summaries.get('engineering_applications'):
            subheader = Paragraph("Engineering Applications", self.styles['Heading3'])
            story.append(subheader)
            story.append(Paragraph(summaries['engineering_applications'], self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Important formulas
        if summaries.get('formulas') and summaries['formulas'].strip():
            subheader = Paragraph("Important Formulas & Equations", self.styles['Heading3'])
            story.append(subheader)
            story.append(Paragraph(summaries['formulas'], self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    def create_individual_section_pdf(self, section_type: str, data: Any, document_name: str) -> BytesIO:
        """
        Create PDF for individual section (questions, flashcards, or summaries)
        
        Args:
            section_type (str): Type of section ('questions', 'flashcards', 'summaries')
            data (Any): Section data
            document_name (str): Original document name
            
        Returns:
            BytesIO: PDF file buffer
        """
        buffer = BytesIO()
        
        try:
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            story = []
            
            # Add title
            title = Paragraph(f"StudyAI - {section_type.title()}", self.title_style)
            story.append(title)
            story.append(Spacer(1, 0.3*inch))
            
            # Add document info
            doc_info = Paragraph(f"From: {document_name}", self.styles['Normal'])
            story.append(doc_info)
            story.append(Spacer(1, 0.3*inch))
            
            # Add content based on section type
            if section_type == 'questions' and isinstance(data, list):
                self._add_questions_section(story, data)
            elif section_type == 'flashcards' and isinstance(data, list):
                self._add_flashcards_section(story, data)
            elif section_type == 'summaries' and isinstance(data, dict):
                self._add_summaries_section(story, data)
            
            doc.build(story)
            buffer.seek(0)
            
        except Exception as e:
            st.error(f"Error creating {section_type} PDF: {str(e)}")
            raise
        
        return buffer
