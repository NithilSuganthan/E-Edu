"""
Certificate Image Generator
Generates certificate images by overlaying student details on a course template.
Uses Pillow to place text at admin-configured X/Y positions.
"""
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.conf import settings


# Path to the bundled font
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
FONT_PATH = os.path.join(FONT_DIR, 'Inter.ttf')


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_certificate_image(certificate, course_config):
    """
    Generate a certificate image with student details overlaid on the course template.
    
    Args:
        certificate: Certificate model instance (with student_name, course, issue_date, certificate_id)
        course_config: CertificationCourse model instance (with template and position fields)
    
    Returns:
        str: Filename of the generated image, or None if no template configured.
    """
    if not course_config.certificate_template:
        return None

    # Load the template image
    template_path = course_config.certificate_template.path
    img = Image.open(template_path).convert('RGBA')
    
    # Create a transparent overlay for text
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Parse colors
    name_color = hex_to_rgb(course_config.name_color)
    detail_color = hex_to_rgb(course_config.detail_color)

    # Load fonts
    def load_font(font_filename, size):
        try:
            path = os.path.join(FONT_DIR, font_filename)
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            return ImageFont.load_default()

    name_font = load_font(course_config.font_family, course_config.name_font_size)
    detail_font = load_font(course_config.detail_font_family, course_config.detail_font_size)

    # --- Draw Student Name (center-aligned) ---
    student_name = certificate.student_name
    name_bbox = draw.textbbox((0, 0), student_name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = course_config.name_position_x - (name_width // 2)
    # Add 10px offset to match editor's padding/visual alignment
    draw.text(
        (name_x, course_config.name_position_y + 10),
        student_name,
        font=name_font,
        fill=name_color
    )

    # --- Draw Course Name (center-aligned) ---
    course_name = course_config.name
    course_bbox = draw.textbbox((0, 0), course_name, font=detail_font)
    course_width = course_bbox[2] - course_bbox[0]
    course_x = course_config.course_position_x - (course_width // 2)
    draw.text(
        (course_x, course_config.course_position_y + 10),
        course_name,
        font=detail_font,
        fill=detail_color
    )

    # --- Draw Issue Date (center-aligned) ---
    date_str = certificate.issue_date.strftime('%B %d, %Y')
    date_bbox = draw.textbbox((0, 0), date_str, font=detail_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = course_config.date_position_x - (date_width // 2)
    draw.text(
        (date_x, course_config.date_position_y + 10),
        date_str,
        font=detail_font,
        fill=detail_color
    )

    # --- Draw Certificate ID (center-aligned) ---
    cert_id = certificate.certificate_id
    certid_bbox = draw.textbbox((0, 0), cert_id, font=detail_font)
    certid_width = certid_bbox[2] - certid_bbox[0]
    certid_x = course_config.certid_position_x - (certid_width // 2)
    draw.text(
        (certid_x, course_config.certid_position_y + 10),
        cert_id,
        font=detail_font,
        fill=detail_color
    )

    # Composite text layer onto template
    result = Image.alpha_composite(img, txt_layer)
    # Convert to RGB for JPEG/PNG saving
    result = result.convert('RGB')

    # Save to bytes
    buffer = BytesIO()
    result.save(buffer, format='PNG', quality=95)
    buffer.seek(0)

    # Generate filename
    filename = f"{certificate.certificate_id}.png"

    # Save to the certificate's image field
    certificate.certificate_image.save(
        filename,
        ContentFile(buffer.read()),
        save=False  # Don't trigger another save() — caller handles it
    )

    return filename
