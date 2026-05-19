import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request

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

# --- FUNCTION TO DOWNLOAD PREMIUM FONT ---
@st.cache_data
def get_premium_font():
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bslnt%2Cwght%5D.ttf"
        font_path = "Inter-Bold.ttf"
        urllib.request.urlretrieve(font_url, font_path)
        return font_path
    except Exception as e:
        return None

# Helper function to get centered coordinates for text with custom fonts
def draw_centered_text(draw, canvas_w, y, text, font, fill):
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (canvas_w - text_w) // 2
    draw.text((text_x, y), text, font=font, fill=fill)

def generate_premium_card(upi_id, amount, custom_note):
    # Canvas Layout Definition (600x950 for extra breathing room for large text)
    w, h = 600, 950
    card = Image.new('RGB', (w, h), '#ffffff')
    draw = ImageDraw.Draw(card)
    
    # Extra large header area to cover big fonts
    header_h = 260
    draw.rectangle([0, 0, w, header_h], fill='#1e3a8a') # Deep Blue
    draw.rectangle([0, header_h-15, w, header_h], fill='#3b82f6') # Light Blue Accent
    
    # Loading Fonts with Mega Sizes
    font_file = get_premium_font()
    
    if font_file:
        font_title = ImageFont.truetype(font_file, 46)       # "SCAN FOR PAYMENT" (Super Big)
        font_subtitle = ImageFont.truetype(font_file, 26)    # "USING ANY UPI APP" (Clear & Bold)
        font_label = ImageFont.truetype(font_file, 24)       # "AMOUNT TO PAY" (Highly Readable)
        font_amount = ImageFont.truetype(font_file, 64)      # "INR 100.00" (Massive & Bold)
        font_upi = ImageFont.truetype(font_file, 28)         # UPI ID (Clear Text)
        font_footer = ImageFont.truetype(font_file, 22)      # Secure Gateway Text (Readable)
    else:
        font_title = font_subtitle = font_label = font_amount = font_upi = font_footer = ImageFont.load_default()

    # 1. Drawing Huge Header Texts (Adjusted Y-coordinates to avoid crowding)
    draw_centered_text(draw, w, 55, "SCAN FOR PAYMENT", font_title, fill="white")
    draw_centered_text(draw, w, 125, "━━━━━━━━━━━━━━━━━━━━━━", font_subtitle, fill="#3b82f6")
    draw_centered_text(draw, w, 165, "USING ANY UPI APP", font_subtitle, fill="#bfdbfe")
    
    # 2. Balanced QR Code Generation (Slightly more compact for text space)
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR&tn={custom_note}"
    qr = qrcode.QRCode(version=3, box_size=8, border=1) 
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, 310 # Pushed slightly down
    
    # Dynamic Frame Around QR
    frame_padding = 12
    draw.rounded_rectangle(
        [bx - frame_padding, by - frame_padding, bx + qr_w + frame_padding, by + qr_h + frame_padding], 
        radius=16, 
        outline='#e2e8f0', 
        width=3
    )
    card.paste(qr_img, (bx, by))
    
    # 3. Content Layout (Below QR Section) - Huge Sizes
    content_start_y = by + qr_h + 60
    
    # Label: "AMOUNT TO PAY"
    draw_centered_text(draw, w, content_start_y, "AMOUNT TO PAY", font_label, fill="#64748b")
    
    # Massive Amount Display
    amount_str = f"INR {float(amount):,.2f}"
    draw_centered_text(draw, w, content_start_y + 45, amount_str, font_amount, fill="#0a0e17")

    # Clean Divider Line
    divider_y = content_start_y + 145
    draw.line([(100, divider_y), (500, divider_y)], fill="#e2e8f0", width=3)
    
    # Big UPI ID Text
    upi_label_str = f"UPI ID: {upi_id}"
    draw_centered_text(draw, w, divider_y + 35, upi_label_str, font_upi, fill="#1e293b")
    
    # Optional Note Text
    if custom_note and custom_note.strip() != "":
        note_label_str = f"Note: {custom_note}"
        draw_centered_text(draw, w, divider_y + 85, note_label_str, font_subtitle, fill="#94a3b8")

    # 4. Clean Flat Big Footer
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
