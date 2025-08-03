"""
PDF Processing Module
Handles PDF-to-image conversion and image-to-PDF creation
"""

from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path
import tempfile
import os
from image_processor import ImageProcessor

class PDFProcessor:
    def __init__(self, quality=200, combine_pages=False):
        self.quality = quality
        self.combine_pages = combine_pages
        self.image_processor = ImageProcessor(dpi=quality)
    
    def pdf_to_images(self, pdf_path):
        """Convert PDF pages to PIL images"""
        try:
            images = convert_from_path(
                pdf_path, 
                dpi=self.quality,
                fmt='RGB'
            )
            return images
        except Exception as e:
            raise Exception(f"Failed to convert PDF to images: {str(e)}")
    
    def images_to_pdf(self, images, output_path):
        """Convert list of PIL images to PDF"""
        if not images:
            raise ValueError("No images provided for PDF creation")
        
        try:
            # Ensure all images are in RGB mode
            rgb_images = []
            for img in images:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                rgb_images.append(img)
            
            # Save as PDF
            rgb_images[0].save(
                output_path,
                save_all=True,
                append_images=rgb_images[1:] if len(rgb_images) > 1 else [],
                format='PDF',
                resolution=self.quality
            )
            
        except Exception as e:
            raise Exception(f"Failed to create PDF from images: {str(e)}")
    
    def process_pdf(self, input_path, output_path):
        """Main processing function"""
        print(f"Converting PDF to images...")
        images = self.pdf_to_images(input_path)
        print(f"Found {len(images)} pages")
        
        print("Inverting colors...")
        processed_images = []
        for i, image in enumerate(images):
            print(f"Processing page {i+1}/{len(images)}")
            inverted = self.image_processor.invert_colors(image)
            processed_images.append(inverted)
        
        if self.combine_pages and len(processed_images) > 1:
            print("Combining pages...")
            combined_images = self.image_processor.combine_pages(processed_images)
            processed_images = combined_images
        
        print("Adding text overlays...")
        final_images = []
        total_pages = len(processed_images)
        for i, image in enumerate(processed_images):
            page_num = i + 1
            with_text = self.image_processor.add_text_overlay(
                image, output_path, page_num, total_pages
            )
            final_images.append(with_text)
        
        print("Creating output PDF...")
        self.images_to_pdf(final_images, output_path)
        print("Processing complete!")