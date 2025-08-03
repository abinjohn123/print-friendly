#!/usr/bin/env python3
"""
Print Friendly - PDF Color Inverter
Converts greenboard lecture notes to printer-friendly format
"""

import argparse
import sys
import os
from pathlib import Path
from pdf_processor import PDFProcessor
from utils import validate_input_file, validate_output_path, setup_output_directory, check_dependencies

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
    
    # Validate arguments
    if len(args.input) == 1 and args.output and not args.output_dir:
        # Single file processing
        input_file = args.input[0]
        output_file = args.output
    elif args.output_dir:
        # Batch processing
        output_dir = Path(args.output_dir)
        setup_output_directory(output_dir)
    else:
        print("Error: For single file, use -o. For multiple files, use --output-dir")
        sys.exit(1)
    
    # Process files
    processor = PDFProcessor(quality=args.quality, combine_pages=args.combine_pages)
    
    try:
        if len(args.input) == 1 and not args.output_dir:
            # Single file processing
            validate_input_file(input_file)
            validate_output_path(output_file)
            
            print(f"Processing {input_file}...")
            processor.process_pdf(input_file, output_file)
            print(f"Output saved to {output_file}")
            
        else:
            # Batch processing
            for input_file in args.input:
                try:
                    validate_input_file(input_file)
                    
                    # Generate output filename
                    input_path = Path(input_file)
                    output_file = output_dir / f"{input_path.stem}_inverted.pdf"
                    
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