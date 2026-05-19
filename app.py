import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
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

# Helper function to get centered coordinates for text
def draw_centered_text(draw, canvas_w, y, text, font, fill):
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        text_x = (canvas_w - text_w) // 2
        draw.text((text_x, y), text, font=font, fill=fill)
        return text_h
    except:
        font_default = ImageFont.load_default()
        draw.text((canvas_w // 2 - 50, y), text, font=font_default, fill=fill)
        return 15

def generate_premium_card(upi_id, amount, custom_note):
    w, h = 600, 850
    card = Image.new('RGB', (w, h), '#ffffff')
    draw = ImageDraw.Draw(card)
    
    header_h = 220
    draw.rectangle([0, 0, w, header_h], fill='#1e3a8a')
    draw.rectangle([0, header_h-10, w, header_h], fill='#3b82f6')
    
    font_default = ImageFont.load_default()

    draw_centered_text(draw, w, 55, "SCAN FOR PAYMENT", font_default, fill="white")
    draw_centered_text(draw, w, 95, "━━━━━━━━━━━━━━━━━━━━━━", font_default, fill="#3b82f6")
    draw_centered_text(draw, w, 125, "USING ANY UPI APP", font_default, fill="#bfdbfe")
    
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR&tn={custom_note}"
    qr = qrcode.QRCode(version=3, box_size=10, border=1)
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, 270
    
    frame_padding = 10
    draw.rounded_rectangle(
        [bx - frame_padding, by - frame_padding, bx + qr_w + frame_padding, by + qr_h + frame_padding], 
        radius=14, 
        outline='#e2e8f0', 
        width=2
    )
    
    card.paste(qr_img, (bx, by))
    
    content_start_y = by + qr_h + 50
    draw_centered_text(draw, w, content_start_y, "AMOUNT TO PAY", font_default, fill="#64748b")
    
    amount_str = f"INR {float(amount):,.2f}"
    amount_y = content_start_y + 45
    
    for offset_x, offset_y in [(0, 0), (1, 0), (0, 1), (1, 1), (2,1)]:
        draw.text(((w - 100) // 2 + offset_x, amount_y + offset_y), amount_str, font=font_default, fill="#0a0e17")

    divider_y = content_start_y + 110
    draw.line([(120, divider_y), (480, divider_y)], fill="#e2e8f0", width=2)
    
    upi_label_str = f"UPI ID: {upi_id}"
    draw_centered_text(draw, w, divider_y + 35, upi_label_str, font_default, fill="#334155")
    
    if custom_note and custom_note.strip() != "":
        note_label_str = f"Note: {custom_note}"
        draw_centered_text(draw, w, divider_y + 75, note_label_str, font_default, fill="#94a3b8")

    draw.rectangle([0, h-70, w, h], fill='#f1f5f9')
    draw_centered_text(draw, w, h-45, "SECURE UPI GATEWAY", font_default, fill="#94a3b8")
    
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
