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
# PREMIUM CSS
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
    font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# QR GENERATOR
# ---------------------------------------------------

def generate_qr(upi_url):

    qr = qrcode.QRCode(
        version=1,
        box_size=15,
        border=2
    )

    qr.add_data(upi_url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    return qr_img

# ---------------------------------------------------
# FONT LOADER
# ---------------------------------------------------

def get_font(size, bold=False):

    try:

        if bold:
            return ImageFont.truetype("arialbd.ttf", size)

        return ImageFont.truetype("arial.ttf", size)

    except:
        return ImageFont.load_default()

# ---------------------------------------------------
# PREMIUM STANDEE
# ---------------------------------------------------

def create_premium_standee(
    qr_image,
    amount,
    merchant_name,
    upi_id
):

    WIDTH = 1200
    HEIGHT = 1900

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#eef2ff")
    draw = ImageDraw.Draw(canvas)

    # ---------------------------------------------------
    # MAIN CARD
    # ---------------------------------------------------

    draw.rounded_rectangle(
        [40,40,1160,1860],
        radius=45,
        fill="white"
    )

    # ---------------------------------------------------
    # HEADER GRADIENT
    # ---------------------------------------------------

    for i in range(340):

        r = 10 + int(i * 0.15)
        g = 20 + int(i * 0.08)
        b = 120 + int(i * 0.35)

        draw.line(
            [(40,40+i),(1160,40+i)],
            fill=(r,g,b),
            width=1
        )

    # ---------------------------------------------------
    # FONTS
    # ---------------------------------------------------

    title_font = get_font(76, True)
    sub_font = get_font(38)
    amount_font = get_font(56, True)
    detail_font = get_font(34, True)
    footer_font = get_font(30, True)
    small_font = get_font(24)

    # ---------------------------------------------------
    # TOP DESIGN
    # ---------------------------------------------------

    draw.line((320,140,450,140), fill="white", width=4)
    draw.line((750,140,880,140), fill="white", width=4)

    draw.ellipse((560,95,640,175), fill="#22c55e")

    draw.text(
        (590,110),
        "✓",
        fill="white",
        font=detail_font
    )

    draw.text(
        (180,190),
        "SCAN FOR PAYMENT",
        fill="white",
        font=title_font
    )

    draw.text(
        (405,295),
        "Secure UPI Payment",
        fill="#e2e8f0",
        font=sub_font
    )

    draw.line((280,315,390,315), fill="white", width=3)
    draw.line((810,315,920,315), fill="white", width=3)

    # ---------------------------------------------------
    # QR SHADOW
    # ---------------------------------------------------

    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        [200,420,1000,1220],
        radius=40,
        fill=(0,0,0,70)
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(18))

    canvas.paste(shadow, (0,0), shadow)

    # ---------------------------------------------------
    # QR BOX
    # ---------------------------------------------------

    draw.rounded_rectangle(
        [190,410,1010,1230],
        radius=40,
        fill="white",
        outline="#2563eb",
        width=5
    )

    qr_resized = qr_image.resize((620,620))

    canvas.paste(qr_resized, (290,500))

    # ---------------------------------------------------
    # AMOUNT BOX
    # ---------------------------------------------------

    draw.rounded_rectangle(
        [320,1270,880,1365],
        radius=25,
        fill="#1d4ed8"
    )

    draw.text(
        (390,1290),
        f"Amount: ₹{amount}",
        fill="#facc15",
        font=amount_font
    )

    # ---------------------------------------------------
    # MERCHANT DETAILS
    # ---------------------------------------------------

    draw.ellipse((220,1425,265,1470), outline="#2563eb", width=3)

    draw.text(
        (290,1425),
        f"Merchant Name: {merchant_name}",
        fill="#1e293b",
        font=detail_font
    )

    draw.ellipse((220,1510,265,1555), outline="#2563eb", width=3)

    draw.text(
        (290,1510),
        f"UPI ID: {upi_id}",
        fill="#1e293b",
        font=detail_font
    )

    # ---------------------------------------------------
    # DIVIDER
    # ---------------------------------------------------

    draw.line(
        (150,1615,1050,1615),
        fill="#cbd5e1",
        width=3
    )

    draw.text(
        (455,1565),
        "SUPPORTED ON",
        fill="#1d4ed8",
        font=footer_font
    )

    # ---------------------------------------------------
    # PAYMENT BADGES
    # ---------------------------------------------------

    apps = [
        ("Google Pay", 90),
        ("PhonePe", 360),
        ("Paytm", 630),
        ("BHIM", 900)
    ]

    for app, x in apps:

        draw.rounded_rectangle(
            [x,1660,x+220,1745],
            radius=20,
            outline="#2563eb",
            width=3,
            fill="white"
        )

        draw.text(
            (x+30,1687),
            app,
            fill="#1e293b",
            font=detail_font
        )

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------

    draw.rectangle(
        [40,1780,1160,1860],
        fill="#08122e"
    )

    draw.text(
        (330,1800),
        "100% Secure UPI Payment",
        fill="white",
        font=footer_font
    )

    draw.text(
        (360,1840),
        "Generated by Premium QR Generator",
        fill="#cbd5e1",
        font=small_font
    )

    return canvas

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------

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
    background:linear-gradient(90deg,#22c55e,#38bdf8);
    color:white;
    font-size:20px;
    font-weight:700;
    cursor:pointer;
    margin-top:20px;
    ">
    ⬇ DOWNLOAD HIGH QUALITY QR
    </button>

    </a>
    """

    return href

# ---------------------------------------------------
# UI
# ---------------------------------------------------

st.markdown(
    '<div class="title">Instant UPI QR Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">Generate secure payment QR codes instantly</div>',
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

    if st.button("🚀 Generate QR Code"):

        with st.spinner("Generating Premium QR..."):

            time.sleep(1)

            upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={amount}&cu=INR"

            qr_img = generate_qr(upi_url)

            final_image = create_premium_standee(
                qr_img,
                amount,
                merchant_name,
                selected_upi
            )

            st.success("✅ QR Generated Successfully!")

            st.image(
                final_image,
                use_container_width=True
            )

            st.markdown(
                get_download_button(final_image),
                unsafe_allow_html=True
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    '<div class="footer">© 2026 Parivahan Service Fintech</div>',
    unsafe_allow_html=True
)
