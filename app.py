# app.py

import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import base64
import time

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Premium UPI QR Generator",
    page_icon="💳",
    layout="centered"
)

# =====================================================
# PREMIUM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background: radial-gradient(circle at top,#1e3a8a,#020617 70%);
    color:white;
}

.main-card{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(18px);
    border-radius:30px;
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
    font-size:20px;
}

div.stButton > button{
    width:100%;
    border:none;
    border-radius:14px;
    padding:15px;
    font-size:18px;
    font-weight:700;
    color:white;
    background: linear-gradient(90deg,#2563eb,#9333ea);
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#cbd5e1;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# QR GENERATOR
# =====================================================

def generate_qr(upi_url):

    qr = qrcode.QRCode(
        version=1,
        box_size=18,
        border=2
    )

    qr.add_data(upi_url)
    qr.make(fit=True)

    return qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

# =====================================================
# FONT LOADER
# =====================================================

def get_font(size, bold=False):

    font_paths = []

    if bold:

        font_paths = [
            "DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        ]

    else:

        font_paths = [
            "DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
        ]

    for path in font_paths:

        try:
            return ImageFont.truetype(path, size)
        except:
            continue

    return ImageFont.load_default()

# =====================================================
# PREMIUM QR IMAGE
# =====================================================

def create_premium_qr(
    qr_img,
    amount,
    merchant_name,
    upi_id
):

    WIDTH = 1400
    HEIGHT = 2100

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#edf4ff")
    draw = ImageDraw.Draw(canvas)

    # =================================================
    # MAIN CARD
    # =================================================

    draw.rounded_rectangle(
        [60,60,1340,2020],
        radius=55,
        fill="white"
    )

    # =================================================
    # HEADER GRADIENT
    # =================================================

    for i in range(430):

        r = 25 + int(i * 0.08)
        g = 35 + int(i * 0.04)
        b = 140 + int(i * 0.20)

        draw.line(
            [(60,60+i),(1340,60+i)],
            fill=(r,g,b),
            width=1
        )

    # =================================================
    # FONTS
    # =================================================

    title_font = get_font(110, True)
    sub_font = get_font(56, False)
    instruction_font = get_font(62, True)
    amount_font = get_font(78, True)
    detail_font = get_font(52, True)
    badge_font = get_font(38, True)
    footer_font = get_font(46, True)
    small_font = get_font(34, False)

    # =================================================
    # HEADER DESIGN
    # =================================================

    draw.line((320,170,500,170), fill="white", width=5)
    draw.line((900,170,1080,170), fill="white", width=5)

    draw.ellipse((640,120,720,200), fill="#22c55e")

    draw.text(
        (667,130),
        "✓",
        fill="white",
        font=detail_font
    )

    # =================================================
    # MAIN TEXT
    # =================================================

    draw.text(
        (120,220),
        "SCAN FOR PAYMENT",
        fill="white",
        font=title_font
    )

    draw.text(
        (430,355),
        "Secure UPI Payment",
        fill="#e2e8f0",
        font=sub_font
    )

    draw.text(
        (180,470),
        "Scan and Pay using any UPI App",
        fill="white",
        font=instruction_font
    )

    # =================================================
    # QR SHADOW
    # =================================================

    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        [250,560,1150,1460],
        radius=50,
        fill=(0,0,0,70)
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(22))

    canvas.paste(shadow, (0,0), shadow)

    # =================================================
    # QR BOX
    # =================================================

    draw.rounded_rectangle(
        [240,550,1140,1450],
        radius=50,
        fill="white",
        outline="#2563eb",
        width=6
    )

    # =================================================
    # QR IMAGE
    # =================================================

    qr_resized = qr_img.resize((720,720))

    canvas.paste(qr_resized, (340,640))

    # =================================================
    # AMOUNT BOX
    # =================================================

    draw.rounded_rectangle(
        [360,1510,1040,1620],
        radius=30,
        fill="#1d4ed8"
    )

    draw.text(
        (400,1530),
        f"Amount : ₹{amount}",
        fill="#facc15",
        font=amount_font
    )

    # =================================================
    # DETAILS
    # =================================================

    draw.text(
        (180,1710),
        f"Merchant Name : {merchant_name}",
        fill="#1e293b",
        font=detail_font
    )

    draw.text(
        (180,1795),
        f"UPI ID : {upi_id}",
        fill="#1e293b",
        font=detail_font
    )

    # =================================================
    # SUPPORTED SECTION
    # =================================================

    draw.line(
        (150,1885,1250,1885),
        fill="#cbd5e1",
        width=3
    )

    draw.text(
        (470,1825),
        "SUPPORTED ON",
        fill="#2563eb",
        font=footer_font
    )

    # =================================================
    # BADGES
    # =================================================

    apps = [
        ("Google Pay", 120),
        ("PhonePe", 420),
        ("Paytm", 720),
        ("BHIM", 1020)
    ]

    for app, x in apps:

        draw.rounded_rectangle(
            [x,1920,x+240,2010],
            radius=20,
            fill="white",
            outline="#2563eb",
            width=3
        )

        draw.text(
            (x+20,1942),
            app,
            fill="#1e293b",
            font=badge_font
        )

    return canvas

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

def get_download_button(img):

    buffered = BytesIO()

    img.save(buffered, format="PNG")

    img_str = base64.b64encode(
        buffered.getvalue()
    ).decode()

    return f"""
    <a href="data:file/png;base64,{img_str}"
    download="Premium_UPI_QR.png"
    style="text-decoration:none;">

    <button style="
    width:100%;
    padding:18px;
    border:none;
    border-radius:14px;
    background:linear-gradient(90deg,#22c55e,#06b6d4);
    color:white;
    font-size:22px;
    font-weight:700;
    cursor:pointer;
    margin-top:20px;
    ">
    ⬇ DOWNLOAD PREMIUM QR
    </button>

    </a>
    """

# =====================================================
# UI
# =====================================================

st.markdown(
    '<div class="title">Instant UPI QR Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">Generate Secure Premium UPI QR Instantly</div>',
    unsafe_allow_html=True
)

with st.container():

    st.markdown(
        '<div class="main-card">',
        unsafe_allow_html=True
    )

    upi_options = [
        "9696159863.wallet@phonepe",
        "9696159863@ibl"
    ]

    selected_upi = st.selectbox(
        "Select UPI ID",
        upi_options
    )

    st.write("### Quick Amount Selection")

    c1,c2,c3,c4 = st.columns(4)

    if c1.button("₹50"):
        st.session_state.amount = 50

    if c2.button("₹100"):
        st.session_state.amount = 100

    if c3.button("₹150"):
        st.session_state.amount = 150

    if c4.button("₹200"):
        st.session_state.amount = 200

    amount = st.number_input(
        "Enter Amount (₹)",
        min_value=1,
        step=1,
        key="amount"
    )

    merchant_name = st.text_input(
        "Merchant Name",
        value="Payment"
    )

    if st.button("🚀 Generate Premium QR"):

        with st.spinner("Creating Premium QR..."):

            time.sleep(1)

            upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={amount}&cu=INR"

            qr_img = generate_qr(upi_url)

            final_img = create_premium_qr(
                qr_img,
                amount,
                merchant_name,
                selected_upi
            )

            st.success("✅ Premium QR Generated Successfully!")

            st.image(
                final_img,
                use_container_width=True
            )

            st.markdown(
                get_download_button(final_img),
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    '<div class="footer">© 2026 Premium UPI QR Generator</div>',
    unsafe_allow_html=True
)
