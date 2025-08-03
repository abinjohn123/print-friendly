"""
Image Processing Module
Handles color inversion and image manipulation operations
"""

from PIL import Image, ImageOps, ImageEnhance
import math

class ImageProcessor:
    def __init__(self, dpi=200):
        # A4 dimensions in inches: 8.27 x 11.69
        self.dpi = dpi
        self.a4_width = int(8.27 * dpi)   # A4 width at specified DPI
        self.a4_height = int(11.69 * dpi)  # A4 height at specified DPI
    
    def invert_colors(self, image):
        """
        Invert image colors with enhanced processing for greenboard notes
        """
        try:
            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Basic color inversion
            inverted = ImageOps.invert(image)
            
            # Enhance contrast for better readability
            enhancer = ImageEnhance.Contrast(inverted)
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