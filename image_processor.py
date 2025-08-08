"""
Image Processing Module
Handles color inversion and image manipulation operations
"""

from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont
import math
import numpy as np
import os

class ImageProcessor:
    def __init__(self, dpi=200):
        # A4 dimensions in inches: 8.27 x 11.69
        self.dpi = dpi
        self.a4_width = int(8.27 * dpi)   # A4 width at specified DPI
        self.a4_height = int(11.69 * dpi)  # A4 height at specified DPI
    
    def smart_crop_content(self, image, mode='content_detection', brightness_threshold=30, variation_threshold=20, min_height_ratio=0.4, margin=5):
        """
        Unified cropping function that can handle both content detection and black bar removal
        
        Args:
            image: PIL Image to crop
            mode: 'content_detection' (for lecture area) or 'black_bar_removal' (post-inversion)
            brightness_threshold: For black bar removal - pixels brighter than this are content
            variation_threshold: For content detection - std dev above this indicates content
            min_height_ratio: Minimum height to preserve as ratio of original
            margin: Pixels to add around detected content
        
        Returns:
            Crop box tuple (left, top, right, bottom) or cropped image based on context
        """
        # Convert to grayscale for analysis
        if image.mode != 'L':
            gray = image.convert('L')
        else:
            gray = image
        
        img_array = np.array(gray)
        height, width = img_array.shape
        
        top_content = 0
        bottom_content = height
        
        if mode == 'content_detection':
            # Use standard deviation to find content vs uniform areas (white bars)
            for y in range(height):
                row = img_array[y, :]
                if np.std(row) > variation_threshold:
                    top_content = y
                    break
            
            for y in range(height - 1, -1, -1):
                row = img_array[y, :]
                if np.std(row) > variation_threshold:
                    bottom_content = y + 1
                    break
                    
        elif mode == 'black_bar_removal':
            # Use mean brightness to find content vs dark areas (black bars)
            for y in range(height):
                row_avg = np.mean(img_array[y, :])
                if row_avg > brightness_threshold:
                    top_content = max(0, y - margin)
                    break
            
            for y in range(height - 1, -1, -1):
                row_avg = np.mean(img_array[y, :])
                if row_avg > brightness_threshold:
                    bottom_content = min(height, y + margin)
                    break
        
        # Ensure minimum height preservation
        min_height = int(height * min_height_ratio)
        content_height = bottom_content - top_content
        
        if content_height < min_height:
            center_y = height // 2
            top_content = max(0, center_y - min_height // 2)
            bottom_content = min(height, center_y + min_height // 2)
        
        # For black bar removal, only crop if significant bars found (20+ pixels)
        if mode == 'black_bar_removal' and top_content <= 20 and (height - bottom_content) <= 20:
            return image  # Return original if no significant bars found
        
        # Return cropped image
        return image.crop((0, top_content, width, bottom_content))

    def is_image_dark(self, image, threshold=0.7):
        """
        Check if image is dark enough to warrant color inversion
        Returns True if a portion of the lecture area is dark (determined by threshold)
        """
        lecture_area = self.smart_crop_content(image, mode='content_detection')
        
        # Convert to grayscale for analysis
        if lecture_area.mode != 'L':
            gray = lecture_area.convert('L')
        else:
            gray = lecture_area
        
        # Convert to numpy array
        img_array = np.array(gray)
        
        # Calculate percentage of dark pixels (below 128 on 0-255 scale)
        dark_pixels = np.sum(img_array < 128)
        total_pixels = img_array.size
        dark_percentage = dark_pixels / total_pixels
        
        return dark_percentage >= threshold

    def invert_colors(self, image):
        """
        Invert image colors with enhanced processing for greenboard notes
        Only performs inversion if 70% or more of the image is dark
        """
        try:
            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Check if image is dark enough to warrant inversion
            if not self.is_image_dark(image):
                return image  # Return original image if not dark enough
            
            # Basic color inversion
            inverted = ImageOps.invert(image)
            
            # Auto-crop black bars that appear after inversion
            cropped = self.smart_crop_content(inverted, mode='black_bar_removal')
            
            # Enhance contrast for better readability
            enhancer = ImageEnhance.Contrast(cropped)
            enhanced = enhancer.enhance(1.2)  # Increase contrast by 20%
            
            # Slightly adjust brightness
            brightness_enhancer = ImageEnhance.Brightness(enhanced)
            result = brightness_enhancer.enhance(0.95)  # Slightly reduce brightness
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to invert image colors: {str(e)}")
    
    def resize_to_fit(self, image, target_width, target_height, maintain_aspect=True):
        """
        Resize image to fit within target dimensions while maintaining aspect ratio
        """
        if not maintain_aspect:
            return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Calculate scaling factor to fit within target dimensions
        width_ratio = target_width / image.width
        height_ratio = target_height / image.height
        scale_factor = min(width_ratio, height_ratio)
        
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    
    def combine_pages(self, images):
        """
        Combine pairs of images vertically on A4 pages
        """
        if len(images) < 2:
            return images
        
        combined_images = []
        
        # Process images in pairs
        for i in range(0, len(images), 2):
            if i + 1 < len(images):
                # Two images to combine
                img1 = images[i]
                img2 = images[i + 1]
            else:
                # Odd number of images, last one goes alone on A4 page
                single_img = self.resize_to_fit(images[i], self.a4_width - 80, self.a4_height - 80)
                a4_canvas = Image.new('RGB', (self.a4_width, self.a4_height), 'white')
                x = (self.a4_width - single_img.width) // 2
                y = (self.a4_height - single_img.height) // 2
                a4_canvas.paste(single_img, (x, y))
                combined_images.append(a4_canvas)
                break
            
            # Calculate available space for each image (with margins)
            margin = 40
            available_width = self.a4_width - (2 * margin)
            available_height_per_image = (self.a4_height - (3 * margin)) // 2  # 3 margins: top, middle, bottom
            
            # Resize both images to fit their allocated space
            resized_img1 = self.resize_to_fit(img1, available_width, available_height_per_image)
            resized_img2 = self.resize_to_fit(img2, available_width, available_height_per_image)
            
            # Create A4 canvas with white background
            a4_canvas = Image.new('RGB', (self.a4_width, self.a4_height), 'white')
            
            # Position first image (top half)
            x1 = (self.a4_width - resized_img1.width) // 2
            y1 = margin
            a4_canvas.paste(resized_img1, (x1, y1))
            
            # Position second image (bottom half)
            x2 = (self.a4_width - resized_img2.width) // 2
            y2 = margin + available_height_per_image + margin  # Start after first image + margin
            a4_canvas.paste(resized_img2, (x2, y2))
            
            combined_images.append(a4_canvas)
        
        return combined_images
    
    def optimize_for_printing(self, image):
        """
        Optimize image for printing by adjusting quality and compression
        """
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Ensure reasonable DPI for printing
        return image
    
    def add_text_overlay(self, image, filename, page_num, total_pages):
        """
        Add filename and page number overlay to bottom right of image
        """
        # Create a copy to avoid modifying original
        img_with_text = image.copy()
        draw = ImageDraw.Draw(img_with_text)
        
        # Extract just the filename without path and extension
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        
        # Create text strings
        filename_text = f"{base_filename}"
        page_text = f"Page {page_num}/{total_pages}"
        
        # Try to use a system font, fallback to default
        font_size = max(12, int(image.height * 0.015))  # Scale with image size
        try:
            # Try common system fonts
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf", 
                "/System/Library/Fonts/Arial.ttf",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Linux
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text dimensions and positions
        filename_bbox = draw.textbbox((0, 0), filename_text, font=font)
        page_bbox = draw.textbbox((0, 0), page_text, font=font)
        
        filename_width = filename_bbox[2] - filename_bbox[0]
        filename_height = filename_bbox[3] - filename_bbox[1]
        page_width = page_bbox[2] - page_bbox[0]
        page_height = page_bbox[3] - page_bbox[1]
        
        # Position at bottom right with margins
        margin = 20
        x_filename = image.width - filename_width - margin
        y_filename = image.height - filename_height - page_height - margin - 5  # Above page number
        
        x_page = image.width - page_width - margin
        y_page = image.height - page_height - margin
        
        # Add semi-transparent background rectangles for better readability
        padding = 5
        
        # Background for filename
        filename_bg = [
            x_filename - padding,
            y_filename - padding,
            x_filename + filename_width + padding,
            y_filename + filename_height + padding
        ]
        
        # Background for page number
        page_bg = [
            x_page - padding,
            y_page - padding,
            x_page + page_width + padding,
            y_page + page_height + padding
        ]
        
        # Draw semi-transparent backgrounds
        draw.rectangle(filename_bg, fill=(255, 255, 255, 200))
        draw.rectangle(page_bg, fill=(255, 255, 255, 200))
        
        # Draw text
        draw.text((x_filename, y_filename), filename_text, font=font, fill=(0, 0, 0))
        draw.text((x_page, y_page), page_text, font=font, fill=(0, 0, 0))
        
        return img_with_text