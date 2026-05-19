import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Premium UPI Card Generator", page_icon="💳", layout="centered")

# --- UI CUSTOM CSS ---
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

# Helper function to get centered coordinates for text safely
def draw_centered_text(draw, canvas_w, y, text, font, fill):
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (canvas_w - text_w) // 2
    draw.text((text_x, y), text, font=font, fill=fill)

def generate_premium_card(upi_id, amount, custom_note):
    # Canvas Layout - Large vertical high-res canvas (600x950)
    w, h = 600, 950
    card = Image.new('RGB', (w, h), '#ffffff')
    draw = ImageDraw.Draw(card)
    
    # Header Area
    header_h = 260
    draw.rectangle([0, 0, w, header_h], fill='#1e3a8a') # Deep Blue
    draw.rectangle([0, header_h-15, w, header_h], fill='#3b82f6') # Light Blue Stripe
    
    # --- INTERNAL ROBUST FONT LOADING SYSTEM ---
    try:
        # SCAN FOR PAYMENT के लिए एक क्लासी/यूनिक Serif फॉन्ट (Georgia)
        font_title = ImageFont.truetype("georgiab.ttf", 44) 
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_label = ImageFont.truetype("arial.ttf", 22)
        font_amount = ImageFont.truetype("arial.ttf", 52)  # Size slightly reduced for premium look
        font_upi = ImageFont.truetype("arial.ttf", 28)
        font_footer = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        try:
            # Linux/Streamlit Cloud Fallback font
            font_title = ImageFont.truetype("LiberationSerif-Bold.ttf", 44)
            font_subtitle = ImageFont.truetype("LiberationSans-Regular.ttf", 24)
            font_label = ImageFont.truetype("LiberationSans-Regular.ttf", 22)
            font_amount = ImageFont.truetype("LiberationSans-Bold.ttf", 52)
            font_upi = ImageFont.truetype("LiberationSans-Regular.ttf", 28)
            font_footer = ImageFont.truetype("LiberationSans-Regular.ttf", 20)
        except IOError:
            # Ultimate Fallback using PIL's built-in scalable font system
            font_title = ImageFont.load_default(size=44)
            font_subtitle = ImageFont.load_default(size=24)
            font_label = ImageFont.load_default(size=22)
            font_amount = ImageFont.load_default(size=52)
            font_upi = ImageFont.load_default(size=28)
            font_footer = ImageFont.load_default(size=20)

    # 1. Header Texts Drawing
    draw_centered_text(draw, w, 65, "SCAN FOR PAYMENT", font_title, fill="white")
    draw_centered_text(draw, w, 130, "━━━━━━━━━━━━━━━━━━━━━━", font_subtitle, fill="#3b82f6")
    draw_centered_text(draw, w, 170, "USING ANY UPI APP", font_subtitle, fill="#bfdbfe")
    
    # 2. QR Code Generation (Perfect Balanced Square)
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR&tn={custom_note}"
    qr = qrcode.QRCode(version=3, box_size=8, border=1) 
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, 310
    
    # --- PREMIUM QR SHADOW EFFECT ---
    shadow_padding = 15
    for offset in range(5, 0, -1):
        draw.rounded_rectangle(
            [bx - shadow_padding + offset, by - shadow_padding + offset, 
             bx + qr_w + shadow_padding + offset, by + qr_h + shadow_padding + offset], 
            radius=18, 
            fill="#e2e8f0"  
        )

    # Modern Rounded Frame Around QR
    frame_padding = 15
    draw.rounded_rectangle(
        [bx - frame_padding, by - frame_padding, bx + qr_w + frame_padding, by + qr_h + frame_padding], 
        radius=18, 
        outline='#ffffff',  
        fill='#ffffff',
        width=3
    )
    card.paste(qr_img, (bx, by))
    
    # 3. Bottom Details Section
    content_start_y = by + qr_h + 65
    
    # Label
    draw_centered_text(draw, w, content_start_y, "AMOUNT TO PAY", font_label, fill="#64748b")
    
    # ONLY AMOUNT DISPLAY (NO SYMBOLS)
    amount_str = f"{float(amount):,.2f}"
    draw_centered_text(draw, w, content_start_y + 45, amount_str, font_amount, fill="#0a0e17")

    # Divider Elegant Line
    divider_y = content_start_y + 145
    draw.line([(100, divider_y), (500, divider_y)], fill="#e2e8f0", width=3)
    
    # UPI ID Text
    upi_label_str = f"UPI ID: {upi_id}"
    draw_centered_text(draw, w, divider_y + 35, upi_label_str, font_upi, fill="#1e293b")
    
    # --- LIVE OPTIONAL PAYMENT NOTE AREA ---
    note_text = custom_note.strip() if custom_note else ""
    note_label_str = f"Note: {note_text}" if note_text else "Note: N/A"
    draw_centered_text(draw, w, divider_y + 85, note_label_str, font_subtitle, fill="#94a3b8")

    # 4. Premium Flat Footer
    draw.rectangle([0, h-80, w, h], fill='#f1f5f9')
    draw_centered_text(draw, w, h-50, "🔒 SECURE UPI GATEWAY", font_footer, fill="#64748b")
    
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
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(final_image, use_container_width=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
