import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Premium UPI Card Generator", page_icon="💳", layout="centered")

# --- UI CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; }
    .main-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    h1 { text-align: center; background: linear-gradient(to right, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

def generate_premium_card(upi_id, amount):
    # Canvas Settings (Gradient Background)
    w, h = 600, 850
    card = Image.new('RGB', (w, h), '#f8f9fa')
    draw = ImageDraw.Draw(card)
    
    # Draw Header Gradient area
    draw.rectangle([0, 0, w, 180], fill='#0052D4') # Royal Blue Theme
    
    # Generate QR Code
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR"
    qr = qrcode.QRCode(version=1, box_size=12, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Create Shadow Box for QR
    shadow_offset = 8
    qr_box_size = qr_img.size[0] + 40
    bx, by = (w - qr_box_size) // 2, 220
    
    # Draw Shadow
    draw.rounded_rectangle([bx+shadow_offset, by+shadow_offset, bx+qr_box_size+shadow_offset, by+qr_box_size+shadow_offset], 
                           radius=20, fill='#d1d1d1')
    # Draw White Box
    draw.rounded_rectangle([bx, by, bx+qr_box_size, by+qr_box_size], radius=20, fill='white')
    
    # Paste QR
    card.paste(qr_img, (bx + 20, by + 20))
    
    # Text Rendering
    try:
        # Note: Default fonts used for compatibility
        font_main = ImageFont.load_default() 
    except:
        font_main = ImageFont.load_default()

    # Header Text
    draw.text((w//2 - 90, 50), "SCAN AND PAY", fill="white")
    draw.text((w//2 - 80, 80), "USING ANY UPI APP", fill="#a1c4fd")
    
    # Amount & ID
    draw.text((w//2 - 50, by + qr_box_size + 40), f"AMOUNT: ₹{amount}", fill="black")
    draw.text((w//2 - 100, by + qr_box_size + 80), f"UPI ID: {upi_id}", fill="#555555")
    
    # Footer Decoration
    draw.rectangle([0, h-80, w, h], fill='#eeeeee')
    draw.text((w//2 - 60, h-50), "SECURE GATEWAY", fill="#999999")
    
    return card

# --- APP UI ---
st.markdown("<h1>Premium UPI QR Card</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    upi_suggestions = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Select UPI ID", upi_suggestions)
    custom_upi = st.text_input("Or Enter Custom ID", value=selected_upi)
    final_upi = custom_upi if custom_upi else selected_upi
    
    amount = st.number_input("Amount (INR)", min_value=1.0, value=100.0)
    
    if st.button("🚀 Generate Best Design Card"):
        final_image = generate_premium_card(final_upi, amount)
        
        # Display
        buf = io.BytesIO()
        final_image.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Your Premium UPI Card", width=400)
        
        # Download
        st.download_button(
            label="📥 Download Premium Image",
            data=buf.getvalue(),
            file_name=f"UPI_Card_{amount}.png",
            mime="image/png"
        )
    st.markdown('</div>', unsafe_allow_html=True)
