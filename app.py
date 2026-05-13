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
    transition:0.3s;
}
div.stButton > button:hover{
    transform:translateY(-2px);
}
.footer{
    text-align:center;
    margin-top:40px;
    color:#cbd5e1;
    font-size:16px;
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

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

# ---------------------------------------------------
# PREMIUM STANDY DESIGN (Matching your Screenshot)
# ---------------------------------------------------
def create_premium_standee(qr_image, amount, merchant_name, upi_id):
    WIDTH, HEIGHT = 1200, 1800
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#f8fafc")
    draw = ImageDraw.Draw(canvas)

    # 1. Gradient Header
    header_h = 350
    for i in range(header_h):
        r = 15 + int(i * 0.1)
        g = 23 + int(i * 0.2)
        b = 150 + int(i * 0.3)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b))

    # Header Texts
    font_title = get_font(85, True)
    font_sub = get_font(45)
    draw.text((WIDTH//2 - 420, 80), "SCAN FOR PAYMENT", fill="white", font=font_title)
    draw.text((WIDTH//2 - 180, 190), "Secure UPI Payment", fill="#e2e8f0", font=font_sub)

    # 2. QR Box with Blue Border
    draw.rounded_rectangle([180, 380, 1020, 1220], radius=50, outline="#2563eb", width=8, fill="white")
    qr_res = qr_image.resize((650, 650), Image.Resampling.LANCZOS)
    canvas.paste(qr_res, (275, 475))

    # 3. Amount Badge (Blue Box, Yellow Text)
    draw.rounded_rectangle([300, 1260, 900, 1370], radius=30, fill="#1e40af")
    font_amt = get_font(65, True)
    draw.text((WIDTH//2 - 240, 1280), f"Amount: ₹{amount}", fill="#facc15", font=font_amt)

    # 4. Details
    font_det = get_font(42)
    draw.text((220, 1420), f"Merchant Name: {merchant_name}", fill="#1e293b", font=font_det)
    draw.text((220, 1485), f"UPI ID: {upi_id}", fill="#1e293b", font=font_det)

    # 5. Supported Apps
    draw.line([(150, 1560), (1050, 1560)], fill="#cbd5e1", width=3)
    draw.text((WIDTH//2 - 130, 1540), " SUPPORTED ON ", fill="#64748b", font=get_font(30, True))
    
    apps = ["Google Pay", "PhonePe", "Paytm", "BHIM"]
    start_x = 100
    for app in apps:
        draw.rounded_rectangle([start_x, 1600, start_x + 230, 1670], radius=20, outline="#94a3b8", width=2)
        draw.text((start_x + 40, 1615), app, fill="#475569", font=get_font(35))
        start_x += 270

    # 6. Bottom Black Bar
    draw.rectangle([0, 1720, WIDTH, 1800], fill="#0f172a")
    draw.text((WIDTH//2 - 200, 1745), "🛡️ 100% Secure UPI Payment", fill="white", font=get_font(35))

    return canvas

def get_download_button(canvas):
    buffered = BytesIO()
    canvas.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f"""
    <a href="data:file/png;base64,{img_str}" download="Premium_UPI_QR.png" style="text-decoration:none;">
        <button style="width:100%; padding:18px; border:none; border-radius:14px; background:linear-gradient(90deg,#22c55e,#10b981); color:white; font-size:20px; font-weight:700; cursor:pointer; margin-top:20px; box-shadow: 0 10px 20px rgba(34,197,94,0.3);">
            📥 Download Premium Standee Card
        </button>
    </a>
    """
    return href

# ---------------------------------------------------
# MAIN UI
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
        with st.spinner("Designing your Premium Standee..."):
            time.sleep(1)
            upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={amount}&cu=INR"
            qr_img = generate_qr(upi_url)
            
            # Create the standee using live data
            standee_card = create_premium_standee(qr_img, amount, merchant_name, selected_upi)
            
            st.success(f"✅ QR Generated for ₹{amount}")
            st.image(standee_card, use_container_width=True)
            
            # Download Button with high-res image
            st.markdown(get_download_button(standee_card), unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown('<div class="footer">Secure • Fast • Professional<br>© 2026 Parivahan Service Fintech</div>', unsafe_allow_html=True)
