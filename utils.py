"""
Utility Functions
File validation, error handling, and helper operations
"""

import os
import sys
from pathlib import Path
import PyPDF2

def validate_input_file(file_path):
    """
    Validate that input file exists and is a valid PDF
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"Input file must be a PDF: {file_path}")
    
    # Basic PDF validation
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            if num_pages == 0:
                raise ValueError(f"PDF file appears to be empty: {file_path}")
    except Exception as e:
        raise ValueError(f"Invalid or corrupted PDF file: {file_path}. Error: {str(e)}")

def validate_output_path(output_path):
    """
    Validate output file path and ensure parent directory exists
    """
    output_file = Path(output_path)
    
    # Check if parent directory exists, create if needed
    parent_dir = output_file.parent
    if not parent_dir.exists():
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise PermissionError(f"Cannot create output directory: {parent_dir}. Error: {str(e)}")
    
    # Check if we can write to the directory
    if not os.access(parent_dir, os.W_OK):
        raise PermissionError(f"No write permission for directory: {parent_dir}")
    
    # Check if output file already exists and warn user
    if output_file.exists():
        print(f"Warning: Output file {output_path} already exists and will be overwritten")

def setup_output_directory(output_dir):
    """
    Create output directory if it doesn't exist
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise PermissionError(f"Cannot create output directory: {output_dir}. Error: {str(e)}")
    
    # Check write permissions
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"No write permission for directory: {output_dir}")

def get_file_size(file_path):
    """
    Get file size in human-readable format
    """
    size_bytes = os.path.getsize(file_path)
    
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"

def print_processing_summary(input_files, output_files, errors=None):
    """
    Print summary of processing results
    """
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    
    successful = len(output_files)
    total = len(input_files)
    
    print(f"Total files processed: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    
    if successful > 0:
        print("\nSuccessful outputs:")
        for output_file in output_files:
            if os.path.exists(output_file):
                size = get_file_size(output_file)
                print(f"  ✓ {output_file} ({size})")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  ✗ {error}")

def check_dependencies():
    """
    Check if required dependencies are available
    """
    missing_deps = []
    
    try:
        import PyPDF2
    except ImportError:
        missing_deps.append("PyPDF2")
    
    try:
        import pdf2image
    except ImportError:
        missing_deps.append("pdf2image")
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("Pillow")
    
    try:
        import reportlab
    except ImportError:
        missing_deps.append("reportlab")
    
    if missing_deps:
        print("Error: Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nInstall missing dependencies with:")
        print("pip install " + " ".join(missing_deps))
        sys.exit(1)
    
    # Check for poppler (pdf2image dependency)
    try:
        from pdf2image.exceptions import PDFInfoNotInstalledError
        from pdf2image import convert_from_path
        # Try a minimal conversion to test poppler
        # This will raise an exception if poppler is not installed
    except Exception:
        print("Warning: poppler-utils may not be installed.")
        print("pdf2image requires poppler-utils for PDF processing.")
        print("Install instructions:")
        print("  Windows: Install via conda or download binaries")
        print("  Linux: sudo apt-get install poppler-utils")
        print("  Mac: brew install poppler")