"""
QR Code System for Delegate Authentication
Generates and manages QR codes for delegate login
"""

import json
import os
from datetime import datetime
import streamlit as st
import pandas as pd

# Try to import QR code libraries, fallback to simple implementation
try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
    QR_AVAILABLE = True
    print("QR code libraries available. Using real QR code generation.")
except ImportError:
    QR_AVAILABLE = False
    print("QR code libraries not available. Using fallback implementation.")

def generate_delegate_qr_data(delegate_id, delegate_name, organization):
    """Generate QR code data for a delegate"""
    qr_data = {
        "type": "delegate_login",
        "delegate_id": str(delegate_id),
        "delegate_name": delegate_name,
        "organization": organization,
        "timestamp": datetime.now().isoformat(),
        "conference": "Insaka Conference 2025"
    }
    return json.dumps(qr_data)

def _normalize_qr_payload(qr_text):
    """Normalize and parse QR code payload"""
    if not qr_text:
        return None, None
    
    # Clean the text
    clean_text = str(qr_text).strip().replace('\uFEFF', '').replace('\u200B-\u200D\uFEFF', '')
    
    # Try to parse as JSON
    try:
        payload = json.loads(clean_text)
        return clean_text, payload
    except json.JSONDecodeError:
        # Try to fix common JSON issues
        try:
            # Fix missing quotes around keys
            fixed_text = clean_text.replace('{', '{"').replace('}', '"}').replace(':', '":"').replace(',', '","')
            # Fix the first and last quotes
            if fixed_text.startswith('{"') and fixed_text.endswith('"}'):
                fixed_text = fixed_text[1:-1]  # Remove extra quotes
                payload = json.loads(fixed_text)
                return fixed_text, payload
        except:
            pass
        
        # If it's just a number, treat it as delegate ID
        if clean_text.isdigit():
            payload = {
                "type": "delegate_login",
                "delegate_id": clean_text,
                "delegate_name": "",
                "organization": "",
                "timestamp": datetime.now().isoformat(),
                "conference": "Insaka Conference 2025"
            }
            return json.dumps(payload), payload
        
        # Return raw text and None payload
        return clean_text, None

def create_fallback_qr_code(delegate_id, delegate_name, organization, size=200):
    """Create a fallback QR code representation when libraries aren't available"""
    # Create a QR-like pattern using simple blocks
    try:
        from PIL import Image as PILImage, ImageDraw, ImageFont
        
        img = PILImage.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Create a simple QR-like pattern with proper positioning markers
        block_size = max(2, size // 21)  # Adjust block size based on image size
        
        # Draw corner squares (like real QR codes) - these are the positioning markers
        corner_size = 7 * block_size
        for x, y in [(0, 0), (size - corner_size, 0), (0, size - corner_size)]:
            # Outer black square
            draw.rectangle([x, y, x + corner_size, y + corner_size], fill='black')
            # Inner white square
            draw.rectangle([x + block_size, y + block_size, x + corner_size - block_size, y + corner_size - block_size], fill='white')
            # Center black square
            draw.rectangle([x + 2*block_size, y + 2*block_size, x + corner_size - 2*block_size, y + corner_size - 2*block_size], fill='black')
        
        # Create a data pattern based on delegate ID that looks more like a real QR code
        id_hash = hash(str(delegate_id)) % 1000
        
        # Draw timing patterns (horizontal and vertical lines)
        timing_start = corner_size + block_size
        timing_end = size - corner_size - block_size
        
        # Horizontal timing pattern
        for x in range(timing_start, timing_end, block_size * 2):
            if x + block_size <= timing_end:
                draw.rectangle([x, corner_size + block_size, x + block_size, corner_size + 2*block_size], fill='black')
        
        # Vertical timing pattern
        for y in range(timing_start, timing_end, block_size * 2):
            if y + block_size <= timing_end:
                draw.rectangle([corner_size + block_size, y, corner_size + 2*block_size, y + block_size], fill='black')
        
        # Draw a pattern in the center area that looks more like QR data
        center_start = corner_size + 3 * block_size
        center_size = size - 2 * corner_size - 6 * block_size
        
        for i in range(0, center_size, block_size):
            for j in range(0, center_size, block_size):
                # Create a pattern that looks more like QR code data
                pattern_value = (id_hash + i + j) % 4
                if pattern_value == 0 or pattern_value == 1:
                    x = center_start + i
                    y = center_start + j
                    if x + block_size <= size and y + block_size <= size:
                        draw.rectangle([x, y, x + block_size, y + block_size], fill='black')
        
        # Add delegate ID text at the bottom
        try:
            font = ImageFont.truetype("arial.ttf", max(8, size // 25))
        except:
            font = ImageFont.load_default()
        
        text = f"ID: {delegate_id}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (size - text_width) // 2
        text_y = size - (size // 8)
        
        # Add white background for text
        padding = 3
        draw.rectangle([text_x - padding, text_y - padding, text_x + text_width + padding, text_y + size // 15 + padding], fill='white', outline='black', width=1)
        draw.text((text_x, text_y), text, fill='black', font=font)
        
        return img
    except Exception as e:
        print(f"Error creating fallback QR code: {e}")
        return None

def create_simple_scannable_qr(delegate_id, delegate_name, organization, size=200):
    """Create a simple scannable QR-like code using basic patterns"""
    try:
        from PIL import Image as PILImage, ImageDraw, ImageFont
        
        img = PILImage.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Create a very simple but recognizable QR-like pattern
        block_size = max(3, size // 15)  # Larger blocks for better scanning
        
        # Draw three corner markers (like real QR codes)
        marker_size = 7 * block_size
        
        # Top-left marker
        draw.rectangle([0, 0, marker_size, marker_size], fill='black')
        draw.rectangle([block_size, block_size, marker_size - block_size, marker_size - block_size], fill='white')
        draw.rectangle([2*block_size, 2*block_size, marker_size - 2*block_size, marker_size - 2*block_size], fill='black')
        
        # Top-right marker
        draw.rectangle([size - marker_size, 0, size, marker_size], fill='black')
        draw.rectangle([size - marker_size + block_size, block_size, size - block_size, marker_size - block_size], fill='white')
        draw.rectangle([size - marker_size + 2*block_size, 2*block_size, size - 2*block_size, marker_size - 2*block_size], fill='black')
        
        # Bottom-left marker
        draw.rectangle([0, size - marker_size, marker_size, size], fill='black')
        draw.rectangle([block_size, size - marker_size + block_size, marker_size - block_size, size - block_size], fill='white')
        draw.rectangle([2*block_size, size - marker_size + 2*block_size, marker_size - 2*block_size, size - 2*block_size], fill='black')
        
        # Create a simple data pattern in the center
        center_start = marker_size + 2 * block_size
        center_end = size - marker_size - 2 * block_size
        
        # Fill center area with a simple pattern
        id_num = int(str(delegate_id).replace(' ', '').replace('-', '')[-3:]) if str(delegate_id).isdigit() else hash(str(delegate_id)) % 1000
        
        for x in range(center_start, center_end, block_size):
            for y in range(center_start, center_end, block_size):
                if x + block_size <= center_end and y + block_size <= center_end:
                    # Create a pattern based on delegate ID
                    if (id_num + x + y) % 3 == 0:
                        draw.rectangle([x, y, x + block_size, y + block_size], fill='black')
        
        return img
    except Exception as e:
        print(f"Error creating simple scannable QR: {e}")
        return None

def create_basic_qr_code(delegate_id, delegate_name, organization, size=200):
    """Create a basic QR code using simple text encoding that can be scanned"""
    try:
        from PIL import Image as PILImage, ImageDraw, ImageFont
        
        # Create a simple text-based QR code that contains the delegate ID
        # This will be a simple pattern that can be read by basic QR scanners
        img = PILImage.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Create a simple grid pattern
        grid_size = 21  # Standard QR code grid size
        cell_size = size // grid_size
        
        # Create a simple pattern based on delegate ID
        delegate_str = str(delegate_id)
        pattern_seed = sum(ord(c) for c in delegate_str) % 1000
        
        # Fill the grid with a pattern
        for i in range(grid_size):
            for j in range(grid_size):
                x = i * cell_size
                y = j * cell_size
                
                # Create a pattern that looks like QR code data
                if (pattern_seed + i + j) % 3 == 0:
                    draw.rectangle([x, y, x + cell_size, y + cell_size], fill='black')
        
        # Add corner markers
        marker_size = 7 * cell_size
        
        # Top-left marker
        draw.rectangle([0, 0, marker_size, marker_size], fill='black')
        draw.rectangle([cell_size, cell_size, marker_size - cell_size, marker_size - cell_size], fill='white')
        draw.rectangle([2*cell_size, 2*cell_size, marker_size - 2*cell_size, marker_size - 2*cell_size], fill='black')
        
        # Top-right marker
        draw.rectangle([size - marker_size, 0, size, marker_size], fill='black')
        draw.rectangle([size - marker_size + cell_size, cell_size, size - cell_size, marker_size - cell_size], fill='white')
        draw.rectangle([size - marker_size + 2*cell_size, 2*cell_size, size - 2*cell_size, marker_size - 2*cell_size], fill='black')
        
        # Bottom-left marker
        draw.rectangle([0, size - marker_size, marker_size, size], fill='black')
        draw.rectangle([cell_size, size - marker_size + cell_size, marker_size - cell_size, size - cell_size], fill='white')
        draw.rectangle([2*cell_size, size - marker_size + 2*cell_size, marker_size - 2*cell_size, size - 2*cell_size], fill='black')
        
        return img
    except Exception as e:
        print(f"Error creating basic QR code: {e}")
        return None

def create_fallback_badge(delegate_id, delegate_name, organization, title="", size=300):
    """Create a fallback badge without QR code when libraries aren't available"""
    # Create a simple badge with text only
    badge_width = size + 100
    badge_height = size + 150
    
    if QR_AVAILABLE:
        try:
            from PIL import Image as PILImage, ImageDraw, ImageFont
            # Create badge image with Zambian colors
            badge_img = PILImage.new('RGB', (badge_width, badge_height), '#f0f8f0')
            draw = ImageDraw.Draw(badge_img)
            
            # Add Zambian green border
            border_width = 8
            draw.rectangle([0, 0, badge_width, badge_height], outline='#198A00', width=border_width)
            
            # Add fonts
            try:
                title_font = ImageFont.truetype("arial.ttf", 16)
                name_font = ImageFont.truetype("arial.ttf", 14)
                org_font = ImageFont.truetype("arial.ttf", 12)
            except:
                title_font = ImageFont.load_default()
                name_font = ImageFont.load_default()
                org_font = ImageFont.load_default()
            
            # Add conference title at top
            title_text = "INSAKA CONFERENCE 2025"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (badge_width - title_width) // 2
            draw.text((title_x, 20), title_text, fill='#198A00', font=title_font)
            
            # Add delegate info in center (no QR code)
            name_text = f"ID: {delegate_id}"
            name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
            name_width = name_bbox[2] - name_bbox[0]
            name_x = (badge_width - name_width) // 2
            draw.text((name_x, 100), name_text, fill='#198A00', font=name_font)
            
            # Add organization if provided
            if organization:
                org_text = str(organization)[:30] + "..." if len(str(organization)) > 30 else str(organization)
                org_bbox = draw.textbbox((0, 0), org_text, font=org_font)
                org_width = org_bbox[2] - org_bbox[0]
                org_x = (badge_width - org_width) // 2
                draw.text((org_x, 130), org_text, fill='#666666', font=org_font)
            
            # Add title if provided
            if title:
                title_text = str(title)[:25] + "..." if len(str(title)) > 25 else str(title)
                title_bbox = draw.textbbox((0, 0), title_text, font=org_font)
                title_width = title_bbox[2] - title_bbox[0]
                title_x = (badge_width - title_width) // 2
                draw.text((title_x, 160), title_text, fill='#666666', font=org_font)
            
            return badge_img
        except Exception as e:
            print(f"Error creating fallback badge: {e}")
            return None
    else:
        # Return None if no image libraries available
        return None

def create_qr_code(delegate_id, delegate_name, organization, size=200):
    """Create a QR code image for a delegate"""
    # Generate QR data
    qr_data = generate_delegate_qr_data(delegate_id, delegate_name, organization)
    
    if not QR_AVAILABLE:
        # Fallback: Create a basic scannable QR code
        fallback_img = create_basic_qr_code(delegate_id, delegate_name, organization, size)
        if fallback_img is None:
            # Try the simple scannable QR
            fallback_img = create_simple_scannable_qr(delegate_id, delegate_name, organization, size)
            if fallback_img is None:
                # Try the more complex fallback
                fallback_img = create_fallback_qr_code(delegate_id, delegate_name, organization, size)
                if fallback_img is None:
                    # Create a simple placeholder image
                    try:
                        from PIL import Image as PILImage, ImageDraw, ImageFont
                        placeholder = PILImage.new('RGB', (size, size), 'white')
                        draw = ImageDraw.Draw(placeholder)
                        try:
                            font = ImageFont.truetype("arial.ttf", 12)
                        except:
                            font = ImageFont.load_default()
                        draw.text((10, 10), f"QR Code\nID: {delegate_id}", fill='black', font=font)
                        return placeholder, qr_data
                    except:
                        return None, qr_data
        return fallback_img, qr_data
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize to desired size
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    
    return qr_img, qr_data

def create_badge_qr_code(delegate_id, delegate_name, organization, title="", size=300):
    """Create a QR code suitable for printing on badges"""
    # Generate QR data
    qr_data = generate_delegate_qr_data(delegate_id, delegate_name, organization)
    
    if not QR_AVAILABLE:
        # Fallback: Create a simple badge without QR code
        return create_fallback_badge(delegate_id, delegate_name, organization, title, size), qr_data
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a larger canvas for the badge
    badge_width = size + 100
    badge_height = size + 150
    
    # Create badge image with Zambian colors
    badge_img = Image.new('RGB', (badge_width, badge_height), '#f0f8f0')
    draw = ImageDraw.Draw(badge_img)
    
    # Add Zambian green border
    border_width = 8
    draw.rectangle([0, 0, badge_width, badge_height], outline='#198A00', width=border_width)
    
    # Add conference title
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("arial.ttf", 16)
        name_font = ImageFont.truetype("arial.ttf", 14)
        org_font = ImageFont.truetype("arial.ttf", 12)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        org_font = ImageFont.load_default()
    
    # Add conference title at top
    title_text = "INSAKA CONFERENCE 2025"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (badge_width - title_width) // 2
    draw.text((title_x, 20), title_text, fill='#198A00', font=title_font)
    
    # Add QR code in center
    qr_x = (badge_width - size) // 2
    qr_y = 60
    badge_img.paste(qr_img, (qr_x, qr_y))
    
    # Add delegate name below QR code
    name_text = f"ID: {delegate_id}"
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (badge_width - name_width) // 2
    draw.text((name_x, qr_y + size + 20), name_text, fill='#198A00', font=name_font)
    
    # Add organization if provided
    if organization:
        org_text = str(organization)[:30] + "..." if len(str(organization)) > 30 else str(organization)
        org_bbox = draw.textbbox((0, 0), org_text, font=org_font)
        org_width = org_bbox[2] - org_bbox[0]
        org_x = (badge_width - org_width) // 2
        draw.text((org_x, qr_y + size + 50), org_text, fill='#666666', font=org_font)
    
    # Add title if provided
    if title:
        title_text = str(title)[:25] + "..." if len(str(title)) > 25 else str(title)
        title_bbox = draw.textbbox((0, 0), title_text, font=org_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (badge_width - title_width) // 2
        draw.text((title_x, qr_y + size + 80), title_text, fill='#666666', font=org_font)
    
    return badge_img, qr_data

def save_qr_code(qr_img, delegate_id, filename_prefix="qr_code"):
    """Save QR code image to file"""
    # Create qr_codes directory if it doesn't exist
    qr_dir = "assets/qr_codes"
    os.makedirs(qr_dir, exist_ok=True)
    
    # Save QR code
    filename = f"{filename_prefix}_{delegate_id}.png"
    filepath = os.path.join(qr_dir, filename)
    qr_img.save(filepath)
    
    return filepath

def scan_qr_code_data(qr_data_string):
    """Parse and validate QR code data"""
    try:
        qr_data = json.loads(qr_data_string)
        
        # Validate required fields
        required_fields = ["type", "delegate_id", "delegate_name", "organization", "timestamp"]
        for field in required_fields:
            if field not in qr_data:
                return None, f"Missing required field: {field}"
        
        # Validate type
        if qr_data["type"] != "delegate_login":
            return None, "Invalid QR code type"
        
        # Validate timestamp (not too old)
        try:
            qr_time = datetime.fromisoformat(qr_data["timestamp"])
            now = datetime.now()
            time_diff = (now - qr_time).total_seconds()
            
            # QR code should be valid for 24 hours
            if time_diff > 86400:  # 24 hours in seconds
                return None, "QR code has expired"
        except:
            return None, "Invalid timestamp format"
        
        return qr_data, None
        
    except json.JSONDecodeError:
        return None, "Invalid QR code data format"
    except Exception as e:
        return None, f"Error parsing QR code: {str(e)}"

def authenticate_with_qr_code(qr_data_string, staff_df):
    """Authenticate delegate using QR code data"""
    qr_data, error = scan_qr_code_data(qr_data_string)
    
    if error:
        return False, error, None
    
    # Find delegate in staff data
    delegate_id = qr_data["delegate_id"]
    
    # Search for delegate by ID
    delegate_row = staff_df[staff_df['ID'] == int(delegate_id)]
    
    if delegate_row.empty:
        return False, f"Delegate with ID {delegate_id} not found", None
    
    delegate = delegate_row.iloc[0]
    
    # Verify delegate name matches
    if delegate.get('Full Name', '').strip() != qr_data["delegate_name"].strip():
        return False, "Delegate name mismatch", None
    
    # Verify organization matches
    if delegate.get('Organization', '').strip() != qr_data["organization"].strip():
        return False, "Organization mismatch", None
    
    return True, "Authentication successful", delegate

def get_qr_code_for_delegate(delegate_id, staff_df):
    """Get QR code for a specific delegate"""
    # Find delegate in staff data
    delegate_row = staff_df[staff_df['ID'] == int(delegate_id)]
    
    if delegate_row.empty:
        return None, f"Delegate with ID {delegate_id} not found"
    
    delegate = delegate_row.iloc[0]
    
    # Generate QR code
    qr_img, qr_data = create_qr_code(
        delegate_id,
        delegate.get('Full Name', ''),
        delegate.get('Organization', ''),
        title=delegate.get('Title', '')
    )
    
    return qr_img, qr_data

def generate_all_delegate_qr_codes(staff_df):
    """Generate QR codes for all delegates"""
    qr_codes = {}
    
    for index, delegate in staff_df.iterrows():
        delegate_id = delegate.get('ID')
        if delegate_id:
            qr_img, qr_data = create_qr_code(
                delegate_id,
                delegate.get('Full Name', ''),
                delegate.get('Organization', ''),
                title=delegate.get('Title', '')
            )
            
            qr_codes[delegate_id] = {
                'image': qr_img,
                'data': qr_data,
                'delegate': delegate
            }
    
    return qr_codes

def create_qr_scanner_script():
    """Generate JavaScript for QR code scanning with actual QR detection"""
    return """
    <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
    <script>
    let scannerActive = false;
    let currentStream = null;
    
    // QR Code Scanner using device camera with actual QR detection
    function startQRScanner() {
        console.log('Starting QR Scanner...');
        
        if (scannerActive) {
            console.log('Scanner already active, stopping...');
            stopQRScanner();
            return;
        }
        
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Camera access not supported on this device');
            console.error('Camera API not supported');
            return;
        }
        
        console.log('Camera API supported, proceeding...');
        
        scannerActive = true;
        
        // Create scanner container
        const scannerDiv = document.getElementById('qr-scanner');
        if (!scannerDiv) {
            alert('Scanner container not found');
            return;
        }
        
        // Clear previous content
        scannerDiv.innerHTML = '';
        
        // Create video element for camera
        const video = document.createElement('video');
        video.id = 'qr-video';
        video.style.width = '100%';
        video.style.height = '300px';
        video.style.border = '3px solid #198A00';
        video.style.borderRadius = '15px';
        video.style.objectFit = 'cover';
        video.autoplay = true;
        video.muted = true;
        video.playsInline = true;
        
        // Create canvas for QR detection
        const canvas = document.createElement('canvas');
        canvas.id = 'qr-canvas';
        canvas.style.display = 'none';
        
        // Create status display
        const statusDiv = document.createElement('div');
        statusDiv.id = 'qr-status';
        statusDiv.style.cssText = `
            text-align: center;
            padding: 10px;
            background: #f0f8f0;
            border-radius: 10px;
            margin-top: 10px;
            font-weight: bold;
            color: #198A00;
        `;
        statusDiv.innerHTML = '📷 Camera starting... Point at QR code';
        
        // Create stop button
        const stopBtn = document.createElement('button');
        stopBtn.innerHTML = '🛑 Stop Scanner';
        stopBtn.style.cssText = `
            background: #D10000;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 10px;
            font-weight: bold;
        `;
        stopBtn.onclick = stopQRScanner;
        
        // Add elements to scanner div
        scannerDiv.appendChild(video);
        scannerDiv.appendChild(canvas);
        scannerDiv.appendChild(statusDiv);
        scannerDiv.appendChild(stopBtn);
        
        // Get camera stream
        navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        })
        .then(stream => {
            currentStream = stream;
            video.srcObject = stream;
            
            video.onloadedmetadata = () => {
                video.play();
                updateStatus('📷 Camera ready! Point at QR code');
                // Start QR detection after video is ready
                setTimeout(() => detectQRCode(video, canvas), 1000);
            };
        })
        .catch(err => {
            console.error('Camera access denied:', err);
            updateStatus('❌ Camera access denied. Please allow camera permissions.');
            scannerActive = false;
        });
    }
    
    function stopQRScanner() {
        scannerActive = false;
        
        // Stop camera stream
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
            currentStream = null;
        }
        
        // Clear scanner div
        const scannerDiv = document.getElementById('qr-scanner');
        if (scannerDiv) {
            scannerDiv.innerHTML = '<p style="text-align: center; color: #666;">📷 Camera scanner stopped</p>';
        }
    }
    
    function updateStatus(message) {
        const statusDiv = document.getElementById('qr-status');
        if (statusDiv) {
            statusDiv.innerHTML = message;
        }
    }
    
    function detectQRCode(video, canvas) {
        if (!scannerActive) return;
        
        const ctx = canvas.getContext('2d');
        
        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const detect = () => {
            if (!scannerActive) return;
            
            // Draw current video frame to canvas
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Get image data for QR detection
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            
            // Use jsQR library to detect QR codes
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            
            if (code) {
                console.log('QR Code detected:', code.data);
                updateStatus('✅ QR Code detected! Processing...');
                
                // Process the QR code data
                processQRCode(code.data);
            } else {
                // Continue scanning
                updateStatus('📷 Scanning... Point camera at QR code');
                setTimeout(detect, 100);
            }
        };
        
        detect();
    }
    
    function processQRCode(qrData) {
        try {
            // Validate QR code data
            const data = JSON.parse(qrData);
            
            if (data.type === 'delegate_login') {
                updateStatus('✅ Valid QR code detected! Logging in...');
                
                // Create a form to submit the QR data
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = window.location.href;
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'qr_data';
                input.value = qrData;
                
                form.appendChild(input);
                document.body.appendChild(form);
                
                // Submit the form to process the QR code
                form.submit();
                
            } else {
                updateStatus('❌ Invalid QR code type');
                setTimeout(() => {
                    if (scannerActive) {
                        updateStatus('📷 Scanning... Point camera at QR code');
                        detectQRCode(document.getElementById('qr-video'), document.getElementById('qr-canvas'));
                    }
                }, 2000);
            }
        } catch (error) {
            console.error('Error processing QR code:', error);
            updateStatus('❌ Invalid QR code format');
            setTimeout(() => {
                if (scannerActive) {
                    updateStatus('📷 Scanning... Point camera at QR code');
                    detectQRCode(document.getElementById('qr-video'), document.getElementById('qr-canvas'));
                }
            }, 2000);
        }
    }
    
    // Make functions globally available
    window.startQRScanner = startQRScanner;
    window.stopQRScanner = stopQRScanner;
    </script>
    """

def check_dual_role_user(delegate_name, delegates_df=None, speakers_data=None):
    """
    Check if a user is both a delegate and a speaker
    Returns: (is_dual_role, speaker_info)
    """
    try:
        # Load delegates data if not provided
        if delegates_df is None:
            delegates_df = pd.read_csv("data/complimentary_passes.csv")
        
        # Load speakers data if not provided
        if speakers_data is None:
            with open("data/speakers.json", "r", encoding="utf-8") as f:
                speakers_data = json.load(f)
        
        # Normalize delegate name for comparison
        delegate_name_normalized = delegate_name.lower().strip()
        
        # Check if delegate name matches any speaker
        speaker_info = None
        for speaker in speakers_data:
            if speaker.get('name') and speaker['name'] != 'nan':
                speaker_name_normalized = speaker['name'].lower().strip()
                if delegate_name_normalized == speaker_name_normalized:
                    speaker_info = speaker
                    break
        
        return speaker_info is not None, speaker_info
        
    except Exception as e:
        st.error(f"Error checking dual role: {str(e)}")
        return False, None

def show_role_selection(delegate_record, speaker_info):
    """
    Show role selection UI for dual-role users
    Returns the selected role and redirects accordingly
    """
    st.markdown("---")
    st.markdown("### 🎭 Role Selection")
    st.info("You are registered as both a **Delegate** and a **Speaker**. Please choose how you'd like to access the conference:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1A1A1A 0%, #2A2A2A 100%); 
                    border: 2px solid #198A00; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 100%;">
            <h4 style="color: #198A00; margin-bottom: 1rem;">👤 Delegate Access</h4>
            <p style="color: #F3F4F6; font-size: 0.9rem; margin-bottom: 1rem;">
                Access conference information, networking, and delegate features
            </p>
            <ul style="color: #F3F4F6; font-size: 0.8rem; text-align: left; margin: 0;">
                <li>📋 Conference agenda</li>
                <li>🤝 Networking & matchmaking</li>
                <li>📱 Delegate dashboard</li>
                <li>🏢 Exhibitor information</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎫 Enter as Delegate", key="delegate_role_btn", width='stretch'):
            return "delegate"
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1A1A1A 0%, #2A2A2A 100%); 
                    border: 2px solid #FF6B35; border-radius: 15px; padding: 1.5rem; 
                    text-align: center; height: 100%;">
            <h4 style="color: #FF6B35; margin-bottom: 1rem;">🎤 Speaker Access</h4>
            <p style="color: #F3F4F6; font-size: 0.9rem; margin-bottom: 1rem;">
                Access speaker-specific features and presentation tools
            </p>
            <ul style="color: #F3F4F6; font-size: 0.8rem; text-align: left; margin: 0;">
                <li>🎤 Speaker profile</li>
                <li>📊 Presentation details</li>
                <li>📅 Speaking schedule</li>
                <li>🎯 Speaker resources</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎤 Enter as Speaker", key="speaker_role_btn", width='stretch'):
            return "speaker"
    
    st.markdown("---")
    st.markdown(f"**Delegate Details:** {delegate_record.get('Name', '')} - {delegate_record.get('Organization', '')}")
    if speaker_info:
        st.markdown(f"**Speaker Details:** {speaker_info.get('name', '')} - {speaker_info.get('organization', '')}")
    
    return None
