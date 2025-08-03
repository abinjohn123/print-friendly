#!/usr/bin/env python3
"""
Print Friendly - PDF Color Inverter
Converts greenboard lecture notes to printer-friendly format
"""

import argparse
import sys
from pathlib import Path
from pdf_processor import PDFProcessor
from utils import validate_input_file, validate_output_path, setup_output_directory, check_dependencies

def find_pdf_files(folder_path):
    """Find all PDF files in the given folder"""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Folder does not exist or is not a directory: {folder_path}")
    
    # Use a set to avoid duplicates, then search for PDF files
    pdf_files = set()
    for pattern in ['*.pdf', '*.PDF']:
        pdf_files.update(folder.glob(pattern))
    
    if not pdf_files:
        raise ValueError(f"No PDF files found in folder: {folder_path}")
    
    return sorted([str(pdf) for pdf in pdf_files])

def main():
    # Check dependencies first
    check_dependencies()
    
    parser = argparse.ArgumentParser(
        description="Convert PDF greenboard notes to printer-friendly format"
    )
    
    parser.add_argument(
        "input",
        nargs="+",
        help="Input PDF file(s) to process"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file (for single input) or directory (for multiple inputs)"
    )
    
    parser.add_argument(
        "--output-dir",
        help="Output directory for processed files"
    )
    
    parser.add_argument(
        "--combine-pages",
        action="store_true",
        help="Combine two pages vertically on single A4 sheet"
    )
    
    parser.add_argument(
        "--quality",
        type=int,
        default=200,
        help="DPI for image processing (default: 200)"
    )
    
    args = parser.parse_args()
    
    # Determine if we have folder input or file input(s)
    folder_input = False
    if len(args.input) == 1:
        input_path = Path(args.input[0])
        if input_path.exists() and input_path.is_dir():
            folder_input = True
    
    # Validate arguments based on input type
    if folder_input:
        # Folder input - must use --output-dir
        if not args.output_dir:
            print("Error: When processing a folder, you must specify --output-dir")
            sys.exit(1)
        if args.output:
            print("Error: Cannot use -o with folder input. Use --output-dir instead")
            sys.exit(1)
        
        # Find all PDF files in the folder
        try:
            pdf_files = find_pdf_files(args.input[0])
            print(f"Found {len(pdf_files)} PDF files in folder: {args.input[0]}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        output_dir = Path(args.output_dir)
        setup_output_directory(output_dir)
        
    elif len(args.input) == 1 and args.output and not args.output_dir:
        # Single file processing
        input_file = args.input[0]
        output_file = args.output
    elif args.output_dir:
        # Multiple file batch processing
        output_dir = Path(args.output_dir)
        setup_output_directory(output_dir)
    else:
        print("Error: For single file, use -o. For multiple files or folders, use --output-dir")
        sys.exit(1)
    
    # Process files
    processor = PDFProcessor(quality=args.quality, combine_pages=args.combine_pages)
    
    try:
        if folder_input:
            # Folder batch processing
            for input_file in pdf_files:
                try:
                    validate_input_file(input_file)
                    
                    # Generate output filename
                    input_path = Path(input_file)
                    output_file = output_dir / f"{input_path.stem}_processed.pdf"
                    
                    print(f"Processing {input_file}...")
                    processor.process_pdf(input_file, str(output_file))
                    print(f"Output saved to {output_file}")
                    
                except Exception as e:
                    print(f"Error processing {input_file}: {e}")
                    continue
                    
        elif len(args.input) == 1 and not args.output_dir:
            # Single file processing
            validate_input_file(input_file)
            validate_output_path(output_file)
            
            print(f"Processing {input_file}...")
            processor.process_pdf(input_file, output_file)
            print(f"Output saved to {output_file}")
            
        else:
            # Multiple file batch processing
            for input_file in args.input:
                try:
                    validate_input_file(input_file)
                    
                    # Generate output filename
                    input_path = Path(input_file)
                    output_file = output_dir / f"{input_path.stem}_processed.pdf"
                    
                    print(f"Processing {input_file}...")
                    processor.process_pdf(input_file, str(output_file))
                    print(f"Output saved to {output_file}")
                    
                except Exception as e:
                    print(f"Error processing {input_file}: {e}")
                    continue
                    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()