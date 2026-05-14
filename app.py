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
    font-size:18px;
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
    transition:0.3s;
}

div.stButton > button:hover{
    transform:translateY(-2px);
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#cbd5e1;
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

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    return img

# =====================================================
# FONT LOADER
# =====================================================

def get_font(size, bold=False):

    try:

        if bold:
            return ImageFont.truetype("arialbd.ttf", size)

        return ImageFont.truetype("arial.ttf", size)

    except:
        return ImageFont.load_default()

# =====================================================
# PREMIUM DOWNLOAD IMAGE
# =====================================================

def create_premium_qr_card(
    qr_img,
    amount,
    merchant_name,
    upi_id
):

    WIDTH = 1300
    HEIGHT = 1900

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#eef4ff")
    draw = ImageDraw.Draw(canvas)

    # -------------------------------------------------
    # SHADOW
    # -------------------------------------------------

    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        [70,70,1230,1830],
        radius=50,
        fill=(0,0,0,80)
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(25))

    canvas.paste(shadow, (0,0), shadow)

    # -------------------------------------------------
    # MAIN CARD
    # -------------------------------------------------

    draw.rounded_rectangle(
        [50,50,1210,1810],
        radius=45,
        fill="white"
    )

    # -------------------------------------------------
    # HEADER GRADIENT
    # -------------------------------------------------

    for i in range(360):

        r = 20 + int(i * 0.10)
        g = 40 + int(i * 0.05)
        b = 130 + int(i * 0.25)

        draw.line(
            [(50,50+i),(1210,50+i)],
            fill=(r,g,b),
            width=1
        )

    # -------------------------------------------------
    # FONTS
    # -------------------------------------------------

    title_font = get_font(82, True)
    subtitle_font = get_font(40, False)
    instruction_font = get_font(42, True)
    amount_font = get_font(60, True)
    detail_font = get_font(38, True)
    small_font = get_font(28, False)
    footer_font = get_font(34, True)

    # -------------------------------------------------
    # HEADER DESIGN
    # -------------------------------------------------

    draw.line((300,150,470,150), fill="white", width=5)
    draw.line((790,150,960,150), fill="white", width=5)

    draw.ellipse((595,100,665,170), fill="#22c55e")

    draw.text(
        (620,112),
        "✓",
        fill="white",
        font=detail_font
    )

    # -------------------------------------------------
    # HEADER TEXT
    # -------------------------------------------------

    draw.text(
        (170,190),
        "SCAN FOR PAYMENT",
        fill="white",
        font=title_font
    )

    draw.text(
        (420,295),
        "Secure UPI Payment",
        fill="#e2e8f0",
        font=subtitle_font
    )

    # -------------------------------------------------
    # QR INSTRUCTION TEXT
    # -------------------------------------------------

    draw.text(
        (250,390),
        "Scan and Pay using any UPI App",
        fill="#ffffff",
        font=instruction_font
    )

    # -------------------------------------------------
    # QR BOX SHADOW
    # -------------------------------------------------

    qr_shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))

    qr_shadow_draw = ImageDraw.Draw(qr_shadow)

    qr_shadow_draw.rounded_rectangle(
        [220,460,1080,1320],
        radius=45,
        fill=(0,0,0,60)
    )

    qr_shadow = qr_shadow.filter(ImageFilter.GaussianBlur(18))

    canvas.paste(qr_shadow, (0,0), qr_shadow)

    # -------------------------------------------------
    # QR BOX
    # -------------------------------------------------

    draw.rounded_rectangle(
        [210,450,1070,1310],
        radius=45,
        fill="white",
        outline="#2563eb",
        width=5
    )

    # -------------------------------------------------
    # QR IMAGE
    # -------------------------------------------------

    qr_resized = qr_img.resize((680,680))

    canvas.paste(qr_resized, (310,540))

    # -------------------------------------------------
    # AMOUNT BOX
    # -------------------------------------------------

    draw.rounded_rectangle(
        [340,1360,920,1460],
        radius=28,
        fill="#1d4ed8"
    )

    draw.text(
        (420,1385),
        f"Amount : ₹{amount}",
        fill="#facc15",
        font=amount_font
    )

    # -------------------------------------------------
    # MERCHANT DETAILS
    # -------------------------------------------------

    draw.text(
        (220,1530),
        f"Merchant Name : {merchant_name}",
        fill="#1e293b",
        font=detail_font
    )

    draw.text(
        (220,1605),
        f"UPI ID : {upi_id}",
        fill="#1e293b",
        font=detail_font
    )

    # -------------------------------------------------
    # SUPPORTED TEXT
    # -------------------------------------------------

    draw.line(
        (150,1690,1110,1690),
        fill="#cbd5e1",
        width=3
    )

    draw.text(
        (500,1650),
        "SUPPORTED ON",
        fill="#2563eb",
        font=footer_font
    )

    # -------------------------------------------------
    # PAYMENT BADGES
    # -------------------------------------------------

    apps = [
        ("Google Pay", 120),
        ("PhonePe", 390),
        ("Paytm", 660),
        ("BHIM", 930)
    ]

    for app, x in apps:

        draw.rounded_rectangle(
            [x,1730,x+220,1810],
            radius=20,
            fill="white",
            outline="#2563eb",
            width=3
        )

        draw.text(
            (x+30,1755),
            app,
            fill="#1e293b",
            font=small_font
        )

    return canvas

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

def get_download_button(img):

    buffered = BytesIO()

    img.save(
        buffered,
        format="PNG"
    )

    img_str = base64.b64encode(
        buffered.getvalue()
    ).decode()

    href = f"""
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

    return href

# =====================================================
# UI
# =====================================================

st.markdown(
    '<div class="title">Instant UPI QR Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">Generate Secure Payment QR Instantly</div>',
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

            final_image = create_premium_qr_card(
                qr_img,
                amount,
                merchant_name,
                selected_upi
            )

            st.success("✅ Premium QR Generated Successfully!")

            st.image(
                final_image,
                use_container_width=True
            )

            st.markdown(
                get_download_button(final_image),
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
