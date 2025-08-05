# Print Friendly - PDF Processing Utility

A Python utility that processes PDF files containing greenboard lecture notes (screenshots from tablets), converting them to printer-friendly format.

## What It Does

Transform dark greenboard screenshots into clean, printer-friendly documents by:

- **Color Inversion**: Converts light text on dark backgrounds to dark text on light backgrounds
- **Page Combining**: Optionally combines two pages vertically on a single A4 sheet to save paper
- **Text Overlays**: Adds filename and page numbers to bottom right of each page

## Examples

Raw & Processed files are available in the [Examples](https://github.com/abinjohn123/print-friendly/tree/master/examples) folder

## Perfect For

- **Students/Educators**: Converting tablet lecture notes for printing
- **Anybody else :)**: Processing dark-background PDFs for better printing

## Requirements

- Python 3.7+
- Dependencies: PyPDF2, pdf2image, Pillow, reportlab, numpy
- System: poppler-utils for PDF processing

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

**Note**: `pdf2image` requires poppler-utils:

- **Windows**: Install via conda or download binaries
- **Linux**: `sudo apt-get install poppler-utils`
- **macOS**: `brew install poppler`

### Usage Examples

```bash
# Process single file
python main.py lecture.pdf -o lecture_processed.pdf

# Process with page combining (two pages per sheet)
python main.py lecture.pdf -o lecture_processed.pdf --combine-pages

# Process entire folder
python main.py input_folder/ --output-dir processed/

# Batch process with page combining and custom quality
python main.py input_folder/ --output-dir processed/ --combine-pages --quality 300
```

## Features

### Core Processing Pipeline

1. **PDF to Images**: Extract high-quality images from PDF pages
2. **Color Inversion**: Convert greenboard colors with contrast enhancement
3. **Auto-Crop**: Remove vertical black bars using edge detection
4. **Page Combining** (optional): Fit two pages on single A4 sheet
5. **Text Overlays**: Add output filename and page numbers for reference
6. **PDF Generation**: Create final printer-friendly PDF

## Command Line Options

```
python main.py INPUT [INPUT ...] [OPTIONS]

Arguments:
  INPUT                 Input PDF file or folder to process

Options:
  -o, --output          Output PDF file (for single file processing)
  --output-dir          Output directory (for folder processing)
  --combine-pages       Combine two pages vertically on single A4 sheet
  --quality             DPI for image processing (default: 200)
  -h, --help           Show help message
```

## Input Types

| Input Type     | Required Flag  | Example                                          |
| -------------- | -------------- | ------------------------------------------------ |
| Single file    | `-o`           | `python main.py file.pdf -o output.pdf`          |
| Multiple files | `--output-dir` | `python main.py *.pdf --output-dir processed/`   |
| Folder         | `--output-dir` | `python main.py folder/ --output-dir processed/` |
