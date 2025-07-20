#!/usr/bin/env python3
"""
Example usage of StudyAI Standalone
"""

from studyai_standalone import StudyAIStandalone
import os

def example_usage():
    """Example of how to use StudyAI programmatically"""
    
    # Create a test document
    test_content = """
    Engineering Mechanics: Statics
    
    Chapter 2: Force Vectors
    
    A force is a vector quantity that tends to cause acceleration of a body.
    Forces are characterized by their magnitude, direction, and point of application.
    
    Key Concepts:
    1. Scalar and Vector Quantities
    2. Vector Operations
    3. Force Resultants
    4. Equilibrium of Particles
    
    The resultant of a system of forces is the single force that produces
    the same effect as the original system of forces.
    """
    
    # Write test document
    with open('test_mechanics.txt', 'w') as f:
        f.write(test_content)
    
    # Initialize StudyAI
    studyai = StudyAIStandalone(use_ocr=True, provider='auto')
    
    # Process the document
    try:
        print("Processing test document...")
        text_content = studyai.process_document('test_mechanics.txt')
        
        # Generate study materials
        materials = studyai.generate_study_materials(text_content)
        
        # Save to files
        studyai.save_to_json('mechanics_study_materials.json')
        studyai.save_to_pdf('mechanics_study_materials.pdf')
        
        # Print summary
        studyai.print_summary()
        
        # Clean up
        os.remove('test_mechanics.txt')
        
        print("\nExample completed successfully!")
        print("Generated files:")
        print("- mechanics_study_materials.json")
        print("- mechanics_study_materials.pdf")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_usage()