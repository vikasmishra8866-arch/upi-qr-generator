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
    """गूगल के सर्वर से सीधे एक प्रीमियम और बोल्ड फोंट डाउनलोड करने के लिए"""
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
    text_h = text_bbox[3] - text_bbox[1]
    text_x = (canvas_w - text_w) // 2
    draw.text((text_x, y), text, font=font, fill=fill)
    return text_h

def generate_premium_card(upi_id, amount, custom_note):
    # 1. Canvas Dimensions (Optimized Standard Premium Standee Size)
    w, h = 600, 900
    card = Image.new('RGB', (w, h), '#ffffff')
    draw = ImageDraw.Draw(card)
    
    # Header Background
    header_h = 240
    draw.rectangle([0, 0, w, header_h], fill='#1e3a8a') # Deep Blue
    draw.rectangle([0, header_h-12, w, header_h], fill='#3b82f6') # Light Blue Stripe
    
    # 2. Loading Fonts dynamically with Specific Sizes
    font_file = get_premium_font()
    
    if font_file:
        font_title = ImageFont.truetype(font_file, 34)       # "SCAN FOR PAYMENT"
        font_subtitle = ImageFont.truetype(font_file, 20)    # "USING ANY UPI APP"
        font_label = ImageFont.truetype(font_file, 18)       # "AMOUNT TO PAY"
        font_amount = ImageFont.truetype(font_file, 48)      # "INR 100.00" (Big & Bold)
        font_upi = ImageFont.truetype(font_file, 22)         # UPI ID
        font_footer = ImageFont.truetype(font_file, 16)      # Secure Gateway Text
    else:
        # Fallback to defaults if download fails (will use built-in scale)
        font_title = font_subtitle = font_label = font_amount = font_upi = font_footer = ImageFont.load_default()

    # 3. Drawing Big Header Texts
    draw_centered_text(draw, w, 65, "SCAN FOR PAYMENT", font_title, fill="white")
    draw_centered_text(draw, w, 125, "━━━━━━━━━━━━━━━━━━━━━━", font_subtitle, fill="#3b82f6")
    draw_centered_text(draw, w, 160, "USING ANY UPI APP", font_subtitle, fill="#bfdbfe")
    
    # 4. Balanced QR Code Generation
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR&tn={custom_note}"
    qr = qrcode.QRCode(version=3, box_size=9, border=1) # Perfect Balanced QR Size
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, 290
    
    # Sleek Border around QR
    frame_padding = 12
    draw.rounded_rectangle(
        [bx - frame_padding, by - frame_padding, bx + qr_w + frame_padding, by + qr_h + frame_padding], 
        radius=16, 
        outline='#e2e8f0', 
        width=3
    )
    card.paste(qr_img, (bx, by))
    
    # 5. Content Layout (Below QR Section)
    content_start_y = by + qr_h + 50
    
    # Label: "AMOUNT TO PAY"
    draw_centered_text(draw, w, content_start_y, "AMOUNT TO PAY", font_label, fill="#64748b")
    
    # Big Premium Amount Display
    amount_str = f"INR {float(amount):,.2f}"
    draw_centered_text(draw, w, content_start_y + 35, amount_str, font_amount, fill="#0a0e17")

    # Divider Minimal Line
    divider_y = content_start_y + 115
    draw.line([(120, divider_y), (480, divider_y)], fill="#e2e8f0", width=2)
    
    # UPI ID Details
    upi_label_str = f"UPI ID: {upi_id}"
    draw_centered_text(draw, w, divider_y + 30, upi_label_str, font_upi, fill="#1e293b")
    
    # Optional Note
    if custom_note and custom_note.strip() != "":
        note_label_str = f"Note: {custom_note}"
        draw_centered_text(draw, w, divider_y + 70, note_label_str, font_subtitle, fill="#94a3b8")

    # 6. Clean and Flat Footer
    draw.rectangle([0, h-70, w, h], fill='#f1f5f9')
    draw_centered_text(draw, w, h-45, "🔒 SECURE UPI GATEWAY", font_footer, fill="#94a3b8")
    
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
