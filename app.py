import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# --- PAGE CONFIG ---
# Setting the page width to a narrower, card-like aspect
st.set_page_config(page_title="Premium UPI Card Generator", page_icon="💳", layout="centered")

# --- UI CUSTOM CSS ---
# Deep gradient background, premium blur, and specific font weights for Streamlit UI
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(135deg, #0a0e17, #131b2c); 
        color: white; 
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 35px; 
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        margin-top: 25px;
        max-width: 550px;
        margin-left: auto;
        margin-right: auto;
    }
    h1 { 
        text-align: center; 
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #1d4ed8); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        margin-bottom: 25px;
    }
    .stImage {
        border-radius: 20px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to get centered coordinates for text
def draw_centered_text(draw, canvas_w, y, text, font, fill):
    try:
        text_w, text_h = draw.textsize(text, font=font)
        text_x = (canvas_w - text_w) // 2
        draw.text((text_x, y), text, font=font, fill=fill)
        return text_h
    except: # Fallback for newer PIL version
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        text_x = (canvas_w - text_w) // 2
        draw.text((text_x, y), text, font=font, fill=fill)
        return text_h

def generate_premium_card(upi_id, amount, custom_note):
    # 1. Canvas Settings (Premium Vertical Card Ratio 3:4)
    # Card Dimensions: Smaller than before for a more compact card feel
    w, h = 600, 850
    card = Image.new('RGB', (w, h), '#ffffff') # Clean white card body
    draw = ImageDraw.Draw(card)
    
    # 2. Premium Header Section (Rich deep blue)
    header_h = 220
    draw.rectangle([0, 0, w, header_h], fill='#1e3a8a') # Deep Royal Blue
    
    # Accent line
    draw.rectangle([0, header_h-10, w, header_h], fill='#3b82f6')
    
    # 3. Text Styling (Font & Size Configuration)
    try:
        # Adjust paths based on your system, or leave empty to use default
        # Common locations on Windows: C:\Windows\Fonts\arial.ttf
        font_main = ImageFont.load_default()
        font_amount = ImageFont.load_default()
        font_id = ImageFont.load_default()
    except:
        font_main = ImageFont.load_default()
        font_amount = ImageFont.load_default()
        font_id = ImageFont.load_default()

    # For PIL's default font to simulate bigger sizes, we have to draw more often or upscale.
    # In a real environment, you should use real .ttf files with ImageFont.truetype.
    # To make default font look bigger, we'll draw it twice slightly offset to simulate weight.
    
    def draw_bold_default(d, x, y, text, font, fill):
        for offset_x, offset_y in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            d.text((x + offset_x, y + offset_y), text, font=font, fill=fill)

    # Header Texts (Significantly Bigger & Premium)
    draw_centered_text(draw, w, 55, "SCAN FOR PAYMENT", font_main, fill="white")
    draw_centered_text(draw, w, 95, "━━━━━━━━━━━━━━━━━━━━━━", font_main, fill="#3b82f6")
    draw_centered_text(draw, w, 125, "USING ANY UPI APP", font_main, fill="#bfdbfe")
    
    # 4. Generate Balanced & Smaller QR Code
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR&tn={custom_note}"
    # Changed version for better density and reduced box_size
    qr = qrcode.QRCode(version=3, box_size=10, border=1)
    qr.add_data(upi_url)
    qr.make(fit=True)
    # Modern dark-navy QR color, slightly smaller
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    
    # QR Box dynamic position and size
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, 270 # Positioned more centrally
    
    # Cleaner, thinner dynamic frame for QR
    frame_padding = 10
    draw.rounded_rectangle(
        [bx - frame_padding, by - frame_padding, bx + qr_w + frame_padding, by + qr_h + frame_padding], 
        radius=14, 
        outline='#e2e8f0', 
        width=2
    )
    
    # Paste QR inside the clean white card body
    card.paste(qr_img, (bx, by))
    
    # 5. Bottom Details (Amount, UPI ID, and Note)
    # Dynamically position based on QR size
    content_start_y = by + qr_h + 50
    
    # Label for Amount
    draw_centered_text(draw, w, content_start_y, "AMOUNT TO PAY", font_id, fill="#64748b")
    
    # Premium Bigger Amount Display (Centered)
    # Simulation of bold font
    amount_str = f"INR {float(amount):,.2f}"
    # We will simulate bigger size by positioning carefully
    d_bbox = draw.textbbox((0, 0), amount_str, font=font_amount)
    d_w = d_bbox[2] - d_bbox[0]
    amount_x = (w - d_w) // 2
    amount_y = content_start_y + 45
    for offset_x, offset_y in [(0, 0), (1, 0), (0, 1), (1, 1), (2,1)]: # Ultra bold sim
        draw.text((amount_x + offset_x, amount_y + offset_y), amount_str, font=font_amount, fill="#0a0e17")

    # Divider Line
    divider_y = content_start_y + 110
    draw.line([(120, divider_y), (480, divider_y)], fill="#e2e8f0", width=2)
    
    # UPI ID Section (Slightly bigger and clearer)
    upi_label_str = f"UPI ID: {upi_id}"
    draw_centered_text(draw, w, divider_y + 35, upi_label_str, font_id, fill="#334155")
    
    # Optional Note Section
    if custom_note and custom_note.strip() != "":
        note_label_str = f"Note: {custom_note}"
        draw_centered_text(draw, w, divider_y + 75, note_label_str, font_id, fill="#94a3b8")

    # 6. Clean, Less Decorative Footer
    # Clean flat footer for modern standee look
    draw.rectangle([0, h-70, w, h], fill='#f1f5f9')
    draw_centered_text(draw, w, h-45, "🛡️ SECURE UPI GATEWAY", font_id, fill="#94a3b8")
    
    return card

# --- APP UI ---
st.markdown("<h1>Premium Payment Standee</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    upi_suggestions = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Select UPI ID", upi_suggestions)
    custom_upi = st.text_input("Or Enter Custom ID", value=selected_upi)
    final_upi = custom_upi if custom_upi else selected_upi
    
    amount = st.number_input("Amount (INR)", min_value=1.0, value=100.0, step=10.0)
    
    note = st.text_input("Optional Payment Note (e.g., 'Coffee', 'Service')", value="Service Fee")

    if st.button("✨ Generate Balanced Card View", use_container_width=True):
        final_image = generate_premium_card(final_upi, amount, note)
        
        # Centering the image in the Streamlit view
        # We don't save it to a buffer, just show it directly
        img_container = st.container()
        with img_container:
            # Center the generated card, and make it smaller in view
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image(final_image, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
