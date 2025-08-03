# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Print Friendly - PDF Processing Utility

## Project Overview

Create a Python utility that processes PDF files containing greenboard lecture notes (screenshots from a tablet), inverts the colors to make them printer-friendly (dark text on light background), and optionally combines two pages into one A4 page to save paper.

## Core Requirements (MVP)

1. **Extract images from PDF pages** - Each PDF page contains a screenshot that needs to be extracted
2. **Invert colors** - Convert greenboard (light text on dark background) to printer-friendly format (dark text on light background)
3. **Auto-crop black bars** - Remove thick black bars that appear at top/bottom after color inversion
4. **Add text overlays** - Display output filename and page numbers at bottom right of each page
5. **Save as new PDF** - Output the processed images as a new PDF file

## Nice-to-Have Features

1. **Page combining** - Stitch two processed images vertically on a single A4 page (portrait orientation)
2. **Batch processing** - Handle multiple PDF files at once
3. **Quality preservation** - Maintain image quality during processing

## Technical Requirements

### Python Libraries to Use

- `PyPDF2` or `pypdf` - For PDF manipulation
- `pdf2image` - To convert PDF pages to images
- `Pillow (PIL)` - For image processing, color inversion, and text overlays
- `reportlab` - To create new PDFs with processed images
- `numpy` - For advanced image analysis and auto-cropping

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Note: pdf2image requires poppler-utils
# Windows: Install poppler-utils via conda or download binaries
# Linux: sudo apt-get install poppler-utils  
# Mac: brew install poppler
```

## Common Commands

```bash
# Run the main utility
python main.py input.pdf -o output.pdf

# Run with page combining
python main.py input.pdf -o output.pdf --combine-pages

# Batch processing
python main.py *.pdf --output-dir processed/

# Test the utility (once tests are implemented)
python -m pytest tests/
```

## Implementation Steps

### Step 1: PDF to Images

- Use `pdf2image` to convert each PDF page to an image
- Handle different page sizes gracefully
- Maintain original resolution

### Step 2: Color Inversion

- Use PIL's `ImageOps.invert()` for simple inversion
- Consider more sophisticated inversion that preserves readability:
  - Convert to grayscale if needed
  - Apply threshold adjustments for better contrast
  - Handle edge cases where simple inversion doesn't work well

### Step 3: Image to PDF

- For MVP: One inverted image per PDF page
- For enhancement: Combine two images vertically on A4 pages

## Architecture

The utility follows a modular architecture:

- **main.py**: CLI interface using argparse, orchestrates the processing pipeline
- **pdf_processor.py**: Handles PDF-to-image conversion and image-to-PDF creation using pdf2image and PIL
- **image_processor.py**: Core color inversion logic and image processing operations  
- **utils.py**: Shared utilities for file validation, error handling, and path operations

The processing pipeline: PDF → Images → Color Inversion → Auto-Crop → Page Combining (optional) → Text Overlays → Output PDF

## Key Implementation Details

### Key Technical Considerations

### Error Handling

- Check if input files exist and are valid PDFs
- Handle corrupted or password-protected PDFs gracefully
- Validate output paths before processing
- Provide clear error messages

### Performance Considerations

- Process pages in batches for large PDFs
- Consider multi-threading for batch file processing
- Keep memory usage in check when handling high-resolution images

## Sample Code Snippet (to get started)

```python
from pdf2image import convert_from_path
from PIL import Image, ImageOps
import os

def invert_pdf_colors(input_pdf_path, output_pdf_path):
    # Convert PDF to images
    images = convert_from_path(input_pdf_path)

    # Process each image
    inverted_images = []
    for img in images:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Invert colors
        inverted = ImageOps.invert(img)
        inverted_images.append(inverted)

    # Save as PDF
    if inverted_images:
        inverted_images[0].save(
            output_pdf_path,
            save_all=True,
            append_images=inverted_images[1:]
        )
```

## Implementation Notes

- Use `ImageOps.invert()` for basic color inversion, with automatic black bar cropping afterward
- Auto-crop functionality uses numpy array analysis to detect and remove black bars from top/bottom
- For page combining, resize images proportionally to fit two on a single A4 page (portrait orientation)
- Text overlays show output filename and page numbers with semi-transparent backgrounds for readability
- Handle different input PDF page sizes gracefully by normalizing dimensions
- Maintain image quality while optimizing file size for printer-friendly output
- The utility should work with greenboard screenshots (light text on dark background) commonly found in lecture notes

## Current Features

✅ **Core Features Implemented:**
- PDF to image conversion with configurable DPI
- Color inversion with contrast/brightness enhancement
- Automatic black bar cropping after inversion
- Text overlays with filename and page numbers
- Page combining (two pages per A4 sheet)
- Batch processing support
- Cross-platform font detection for text overlays

✅ **Processing Pipeline:**
1. Extract images from PDF pages
2. Invert colors for printer-friendly output
3. Auto-crop black bars from top/bottom edges
4. Optionally combine two pages vertically on A4
5. Add text overlays (filename + page numbers)
6. Generate final PDF with processed images
