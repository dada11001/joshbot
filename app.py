import streamlit as st
import os
from io import BytesIO
import tempfile

from document_processor import DocumentProcessor
from content_generator import ContentGenerator
from pdf_exporter import PDFExporter
from utils import initialize_session_state, display_error_message, display_success_message

#Page configuration
st.set_page_config( page_title="StudyAI - Engineering Study Assistant", page_icon="\ud83d\udcda", layout="wide", initial_sidebar_state="expanded" )

def main():
    # Main title
    st.title("\ud83d\udcda StudyAI - Engineering Study Assistant")
st.markdown("Transform your engineering documents into comprehensive study materials")

# Sidebar navigation using radio (cleaner UX)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "📂 Sections",
    ["📄 Upload Document", "❓ Questions & Answers", "🗂️ Flash Cards", "📝 Summaries", "📊 Export Materials"]
)

# Initialize processors
doc_processor = DocumentProcessor()
content_generator = ContentGenerator()
pdf_exporter = PDFExporter()

if page == "📄 Upload Document":
    upload_document_page(doc_processor, content_generator)
elif page == "❓ Questions & Answers":
    questions_answers_page()
elif page == "🗂️ Flash Cards":
    flash_cards_page()
elif page == "📝 Summaries":
    summaries_page()
elif page == "📊 Export Materials":
    export_materials_page(pdf_exporter)

def upload_document_page(doc_processor, content_generator): st.header("\ud83d\udcc4 Upload Your Study Document")

# AI Provider is fixed to Gemini
st.info("**AI Provider:** 🆓 Google Gemini (Free)")

# OCR Setting
use_ocr = st.checkbox(
    "Extract text from images",
    value=True,
    help="Enable OCR to extract text from images, diagrams, and scanned content in PDFs"
)
doc_processor.use_ocr = use_ocr

# File uploader
uploaded_file = st.file_uploader(
    "Choose a PDF or DOC file",
    type=['pdf', 'doc', 'docx'],
    help="Upload your engineering documents (textbooks, notes, papers) to generate study materials"
)

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Process button
    if st.button("🔄 Process Document", type="primary"):
        try:
            processing_message = "Processing document and generating study materials..."
            if use_ocr and uploaded_file.name.lower().endswith('.pdf'):
                processing_message += " (Including image text extraction)"

            with st.spinner(processing_message):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name

                extracted_text = doc_processor.extract_text(tmp_file_path)

                if not extracted_text.strip():
                    st.error("❌ No text could be extracted. Check the file integrity.")
                    return

                st.session_state.extracted_text = extracted_text
                st.session_state.document_name = uploaded_file.name

                progress_bar = st.progress(0)
                progress_bar.progress(25)
                st.session_state.questions_answers = content_generator.generate_questions_answers(extracted_text)
                progress_bar.progress(50)
                st.session_state.flash_cards = content_generator.generate_flash_cards(extracted_text)
                progress_bar.progress(75)
                st.session_state.summaries = content_generator.generate_summaries(extracted_text)
                progress_bar.progress(100)

                os.unlink(tmp_file_path)

                display_success_message("🎉 Document processed successfully! Navigate to other sections to view study materials.")

        except Exception as e:
            display_error_message(f"Error processing document: {str(e)}")

if hasattr(st.session_state, 'document_name'):
    st.info(f"📄 Current Document: **{st.session_state.document_name}**")
    if st.button("🗑️ Clear Document"):
        for key in ['extracted_text', 'document_name', 'questions_answers', 'flash_cards', 'summaries']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def questions_answers_page(): st.header("❓ Questions & Answers") if not hasattr(st.session_state, 'questions_answers'): st.warning("⚠️ Please upload and process a document first.") return if not st.session_state.questions_answers: st.error("❌ No questions were generated.") return st.success(f"📚 Generated from: {st.session_state.document_name}") for i, qa in enumerate(st.session_state.questions_answers, 1): with st.expander(f"Question {i}: {qa['question'][:100]}..."): st.markdown(f"Question Type: {qa['type']}") st.markdown(f"Question: {qa['question']}") if qa['type'] == 'multiple_choice' and 'options' in qa: for j, option in enumerate(qa['options'], 1): st.markdown(f"{j}. {option}") st.markdown(f"Answer: {qa['answer']}") if 'explanation' in qa: st.markdown(f"Explanation: {qa['explanation']}")

def flash_cards_page(): st.header("🗂️ Flash Cards") if not hasattr(st.session_state, 'flash_cards'): st.warning("⚠️ Please upload and process a document first.") return if not st.session_state.flash_cards: st.error("❌ No flash cards were generated.") return st.success(f"📚 Generated from: {st.session_state.document_name}") if 'current_card' not in st.session_state: st.session_state.current_card = 0 total_cards = len(st.session_state.flash_cards) current_card = st.session_state.current_card card = st.session_state.flash_cards[current_card] if 'show_answer' not in st.session_state: st.session_state.show_answer = False if not st.session_state.show_answer: st.markdown("### 📝 Term/Concept") st.info(card['term']) if st.button("🔄 Flip Card", key="flip_to_answer"): st.session_state.show_answer = True st.rerun() else: st.markdown("### 💡 Definition/Explanation") st.success(card['definition']) if 'explanation' in card and card['explanation']: st.markdown("### 📖 Additional Context") st.markdown(card['explanation']) if st.button("🔄 Flip Card", key="flip_to_term"): st.session_state.show_answer = False st.rerun() col1, col2, col3 = st.columns([1, 2, 1]) with col1: if current_card > 0: if st.button("⬅️ Previous"): st.session_state.current_card -= 1 st.session_state.show_answer = False st.rerun() with col3: if current_card < total_cards - 1: if st.button("Next ➡️"): st.session_state.current_card += 1 st.session_state.show_answer = False st.rerun() st.progress((current_card + 1) / total_cards)

def summaries_page(): st.header("📝 Summaries") if not hasattr(st.session_state, 'summaries'): st.warning("⚠️ Please upload and process a document first.") return if not st.session_state.summaries: st.error("❌ No summaries were generated.") return st.success(f"📚 Generated from: {st.session_state.document_name}") summaries = st.session_state.summaries if 'key_concepts' in summaries: with st.expander("🔑 Key Concepts", expanded=True): st.markdown(summaries['key_concepts']) if 'main_summary' in summaries: with st.expander("📄 Main Summary", expanded=True): st.markdown(summaries['main_summary']) if 'engineering_applications' in summaries: with st.expander("⚙️ Engineering Applications"): st.markdown(summaries['engineering_applications']) if 'formulas' in summaries and summaries['formulas']: with st.expander("📐 Important Formulas & Equations"): st.markdown(summaries['formulas'])

def export_materials_page(pdf_exporter): st.header("📊 Export Study Materials") if not hasattr(st.session_state, 'document_name'): st.warning("⚠️ Please upload and process a document first.") return st.success(f"📚 Ready to export materials for: {st.session_state.document_name}") st.subheader("Select Materials to Export") export_questions = st.checkbox("❓ Questions & Answers", value=True) export_flashcards = st.checkbox("🗂️ Flash Cards", value=True) export_summaries = st.checkbox("📝 Summaries", value=True) if not any([export_questions, export_flashcards, export_summaries]): st.warning("⚠️ Please select at least one type of material to export.") return if st.button("📥 Generate PDF Export", type="primary"): try: with st.spinner("Generating PDF export..."): export_data = { 'document_name': st.session_state.document_name, 'questions_answers': st.session_state.questions_answers if export_questions else [], 'flash_cards': st.session_state.flash_cards if export_flashcards else [], 'summaries': st.session_state.summaries if export_summaries else {} } pdf_buffer = pdf_exporter.create_study_materials_pdf(export_data) st.download_button( label="📥 Download Study Materials PDF", data=pdf_buffer.getvalue(), file_name=f"study_materials_{st.session_state.document_name.replace('.', '_')}.pdf", mime="application/pdf", type="primary" ) display_success_message("🎉 PDF export generated successfully!") except Exception as e: display_error_message(f"Error generating PDF export: {str(e)}") st.divider() st.subheader("📈 Study Materials Overview") col1, col2, col3 = st.columns(3) with col1: st.metric("Questions Generated", len(st.session_state.get('questions_answers', []))) with col2: st.metric("Flash Cards Created", len(st.session_state.get('flash_cards', []))) with col3: st.metric("Summary Sections", len(st.session_state.get('summaries', {})))

if name == "main": main()

