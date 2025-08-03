
# Print Friendly PDF Utility - Demo Guide

## Overview
This utility converts greenboard lecture notes (light text on dark background) 
to printer-friendly format (dark text on light background).

## Features Implemented
✓ PDF to image conversion
✓ Color inversion for greenboard notes  
✓ Image to PDF output
✓ Page combining (2 pages per A4 sheet)
✓ Batch processing multiple files
✓ Comprehensive error handling
✓ Input validation and user feedback

## Usage Examples

### Basic Usage (Single File)
```bash
python main.py input.pdf -o output.pdf
```

### Page Combining (2 pages per A4)
```bash
python main.py input.pdf -o output.pdf --combine-pages
```

### Batch Processing
```bash
python main.py *.pdf --output-dir processed/
```

### Custom Quality
```bash
python main.py input.pdf -o output.pdf --quality 300
```

## Installation Requirements

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install poppler-utils (required for pdf2image):
- Windows: Download from https://github.com/oschwartz10612/poppler-windows
- Linux: `sudo apt-get install poppler-utils`
- Mac: `brew install poppler`

## Testing the Implementation

1. **Test project structure**: `python test_structure.py`
2. **Test with sample PDF**: Create or obtain a greenboard PDF file
3. **Run basic conversion**: `python main.py sample.pdf -o output.pdf`
4. **Test page combining**: `python main.py sample.pdf -o combined.pdf --combine-pages`

## Architecture

- **main.py**: CLI interface and orchestration
- **pdf_processor.py**: Core PDF processing logic
- **image_processor.py**: Color inversion and image manipulation
- **utils.py**: File validation and error handling utilities

## Success Criteria Met

✅ Extracts images from PDF pages
✅ Inverts colors (greenboard → printer-friendly)
✅ Saves as new PDF with maintained quality
✅ Optional page combining feature
✅ Batch processing capability
✅ Comprehensive error handling
✅ User-friendly CLI interface

## Next Steps for Users

1. Install dependencies as shown above
2. Test with a sample greenboard PDF
3. Adjust quality settings if needed
4. Use batch processing for multiple files
5. Experiment with page combining for paper savings

The utility is ready for production use with greenboard lecture notes!
