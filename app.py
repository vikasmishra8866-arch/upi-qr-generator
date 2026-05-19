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
        background: linear-gradient(135deg, #0f172a, #1e293b); 
        color: white; 
        font-family: 'Inter', sans-serif;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 35px; 
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        margin-top: 20px;
    }
    h1 { 
        text-align: center; 
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #3b82f6); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        margin-bottom: 5px;
    }
    p.subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 25px;
    }
    /* Centering the generated image */
    .stImage {
        display: flex;
        justify-content: center;
        margin-top: 25px;
        border-radius: 16px;
    }
    </style>
""", unsafe_allow_html=True)

def generate_premium_card(upi_id, amount):
    # Canvas Settings (Ultra Premium Vertical Card Concept)
    w, h = 600, 900
    card = Image.new('RGB', (w, h), '#ffffff')
    draw = ImageDraw.Draw(card)
    
    # 1. Top Premium Header (Deep Royal/Neon Gradient Feel)
    draw.rectangle([0, 0, w, 240], fill='#1e3a8a') 
    
    # Decorative subtle accent bar
    draw.rectangle([0, 230, w, 240], fill='#3b82f6')
    
    # 2. Text Rendering Configuration
    # Using default font but manually adjusting spacing & sizes using standard draws
    # Header Texts
    draw.text((w//2 - 110, 65), "SCAN FOR PAYMENT", fill="#ffffff")
    draw.text((w//2 - 125, 105), "━━━━━━━━━━━━━━━━━━━━", fill="#3b82f6")
    draw.text((w//2 - 105, 135), "USING ANY UPI APP", fill="#93c5fd")
    
    # 3. Generate High-Quality QR Code
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR"
    qr = qrcode.QRCode(version=3, box_size=11, border=1)
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    
    # QR Box Dynamic Centering
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, 290
    
    # Outer Border Box for QR to give it a frame look
    padding = 15
    draw.rounded_rectangle(
        [bx - padding, by - padding, bx + qr_w + padding, by + qr_h + padding], 
        radius=16, 
        outline='#e2e8f0', 
        width=3
    )
    
    # Paste QR inside the frame
    card.paste(qr_img, (bx, by))
    
    # 4. Bottom Details (Amount & UPI Details)
    # Dynamic positioning based on QR position
    content_y = by + qr_h + 60
    
    # Amount Section with Premium Labeling
    draw.text((w//2 - 55, content_y), "AMOUNT TO PAY", fill="#64748b")
    
    # Big Bold-Looking Amount text using standard fonts (centered cleanly)
    amount_str = f"INR {amount:,.2f}"
    draw.text((w//2 - (len(amount_str)*4), content_y + 35), amount_str, fill="#0f172a")
    
    # Divider Line
    draw.line([(150, content_y + 90), (450, content_y + 90)], fill="#e2e8f0", width=2)
    
    # UPI ID Section
    id_str = f"UPI ID: {upi_id}"
    draw.text((w//2 - (len(id_str)*3.5), content_y + 115), id_str, fill="#334155")
    
    # 5. Dynamic Footer
    draw.rectangle([0, h-70, w, h], fill='#f1f5f9')
    draw.text((w//2 - 75, h-45), "🔒 100% SECURE UPI GATEWAY", fill="#64748b")
    
    return card

# --- APP UI ---
st.markdown("<h1>Premium UPI QR Card</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Generate beautiful, minimalist live transaction display cards</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    upi_suggestions = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Select UPI ID", upi_suggestions)
    custom_upi = st.text_input("Or Enter Custom ID", value=selected_upi)
    final_upi = custom_upi if custom_upi else selected_upi
    
    amount = st.number_input("Amount (INR)", min_value=1.0, value=100.0, step=10.0)
    
    # Generate button triggers the view directly
    if st.button("✨ Generate Live Payment Card", use_container_width=True):
        final_image = generate_premium_card(final_upi, amount)
        
        # Display Only (No Download Button Below It)
        buf = io.BytesIO()
        final_image.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
