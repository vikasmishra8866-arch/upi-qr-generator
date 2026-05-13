# app.py
import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import base64
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Premium UPI QR Generator",
    page_icon="💳",
    layout="centered"
)

# ---------------------------------------------------
# PREMIUM CSS (Glassmorphism UI)
# ---------------------------------------------------
st.markdown("""
<style>
.stApp{
    background: radial-gradient(circle at top,#172554,#020617 65%);
    color:white;
}
.main-card{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(18px);
    border-radius:28px;
    padding:35px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 20px 60px rgba(0,0,0,0.45);
}
.title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    background: linear-gradient(90deg,#38bdf8,#8b5cf6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:8px;
}
.sub{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:35px;
    font-size:18px;
}
div.stButton > button{
    width:100%;
    border:none;
    border-radius:14px;
    padding:14px;
    font-weight:700;
    font-size:17px;
    color:white;
    background: linear-gradient(90deg,#3b82f6,#a855f7);
}
.footer{
    text-align:center;
    margin-top:40px;
    color:#cbd5e1;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def generate_qr(upi_url):
    qr = qrcode.QRCode(version=1, box_size=15, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")

# ---------------------------------------------------
# PREMIUM STANDY DESIGN (High Quality)
# ---------------------------------------------------
def create_premium_standee(qr_image, amount, merchant_name, upi_id):
    # बड़ी इमेज ताकि फटे नहीं (HD Quality)
    WIDTH, HEIGHT = 1200, 1800
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#f8fafc")
    draw = ImageDraw.Draw(canvas)

    # 1. Top Gradient Header
    header_h = 400
    for i in range(header_h):
        r = 15 + int(i * 0.1)
        g = 23 + int(i * 0.2)
        b = 150 + int(i * 0.3)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b))

    # Header Texts (Manually Drawing to avoid Font errors)
    # SCAN FOR PAYMENT
    draw.text((WIDTH//2 - 400, 100), "SCAN FOR PAYMENT", fill="white", stroke_width=2)
    draw.text((WIDTH//2 - 180, 220), "Secure UPI Payment", fill="#e2e8f0")

    # 2. QR Container with thick blue border
    # Shadow for QR box
    draw.rounded_rectangle([185, 385, 1025, 1225], radius=55, fill="#cbd5e1") # Shadow
    draw.rounded_rectangle([180, 380, 1020, 1220], radius=50, outline="#2563eb", width=12, fill="white")
    
    # Paste QR in center
    qr_res = qr_image.resize((680, 680), Image.Resampling.LANCZOS)
    canvas.paste(qr_res, (260, 470))

    # 3. Amount Badge (Blue Box, Large Yellow Text)
    draw.rounded_rectangle([250, 1260, 950, 1380], radius=35, fill="#1e40af")
    # Amount Text
    amt_text = f"Amount: ₹{amount}"
    draw.text((WIDTH//2 - 250, 1285), amt_text, fill="#facc15")

    # 4. Merchant Details (Large enough to read)
    draw.text((200, 1420), f"Merchant Name: {merchant_name}", fill="#1e293b")
    draw.text((200, 1490), f"UPI ID: {upi_id}", fill="#1e293b")

    # 5. Supported On Section
    draw.line([(150, 1580), (1050, 1580)], fill="#cbd5e1", width=4)
    draw.text((WIDTH//2 - 120, 1555), " SUPPORTED ON ", fill="#1e40af")
    
    # Simple Badges
    apps = ["Google Pay", "PhonePe", "Paytm", "BHIM UPI"]
    start_x = 100
    for app in apps:
        draw.rounded_rectangle([start_x, 1620, start_x + 230, 1700], radius=20, outline="#94a3b8", width=3)
        draw.text((start_x + 30, 1635), app, fill="#475569")
        start_x += 270

    # 6. Final Footer Black Bar
    draw.rectangle([0, 1730, WIDTH, 1800], fill="#0f172a")
    draw.text((WIDTH//2 - 220, 1750), "🛡️ 100% Secure UPI Payment", fill="white")

    return canvas

def get_download_button(canvas):
    buffered = BytesIO()
    canvas.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f"""
    <a href="data:file/png;base64,{img_str}" download="Premium_UPI_QR_Standee.png" style="text-decoration:none;">
        <button style="width:100%; padding:18px; border:none; border-radius:14px; background:linear-gradient(90deg,#22c55e,#10b981); color:white; font-size:20px; font-weight:700; cursor:pointer; margin-top:20px;">
            ⬇ DOWNLOAD HIGH-QUALITY STANDY CARD
        </button>
    </a>
    """
    return href

# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------
st.markdown('<div class="title">Instant UPI QR Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Generate secure payment QR codes instantly</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    upi_options = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Select UPI ID", upi_options)
    
    st.write("### Quick Amount Selection")
    c1,c2,c3,c4 = st.columns(4)
    if c1.button("₹50"): st.session_state.amount = 50
    if c2.button("₹100"): st.session_state.amount = 100
    if c3.button("₹150"): st.session_state.amount = 150
    if c4.button("₹200"): st.session_state.amount = 200
    
    amount = st.number_input("Enter Amount (₹)", min_value=1, step=1, key="amount")
    merchant_name = st.text_input("Merchant Name", value="Payment")

    if st.button("🚀 Generate QR Code"):
        with st.spinner("Designing your High-Quality Standee..."):
            time.sleep(1)
            upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={amount}&cu=INR"
            qr_img = generate_qr(upi_url)
            
            # Create standee
            final_image = create_premium_standee(qr_img, amount, merchant_name, selected_upi)
            
            st.success(f"✅ QR Generated Successfully!")
            st.image(final_image, use_container_width=True)
            st.markdown(get_download_button(final_image), unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 Parivahan Service Fintech</div>', unsafe_allow_html=True)
