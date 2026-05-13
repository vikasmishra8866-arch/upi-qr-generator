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
    font-size:58px;
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
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# QR GENERATOR
# ---------------------------------------------------

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

# ---------------------------------------------------
# FONT FUNCTION
# ---------------------------------------------------

def get_font(size, bold=False):

    try:

        if bold:
            return ImageFont.truetype("arialbd.ttf", size)

        return ImageFont.truetype("arial.ttf", size)

    except:
        return ImageFont.load_default()

# ---------------------------------------------------
# CREATE PREMIUM QR CARD
# ---------------------------------------------------

def create_premium_card(
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
    # SHADOW
    # ---------------------------------------------------

    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        (55,55,1145,1845),
        radius=45,
        fill=(0,0,0,100)
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(25))

    canvas.paste(shadow, (0,0), shadow)

    # ---------------------------------------------------
    # MAIN CARD
    # ---------------------------------------------------

    draw.rounded_rectangle(
        (40,40,1160,1860),
        radius=45,
        fill="white"
    )

    # ---------------------------------------------------
    # HEADER
    # ---------------------------------------------------

    for i in range(330):

        r = 15 + int(i * 0.2)
        g = 23 + int(i * 0.1)
        b = 80 + int(i * 0.4)

        draw.rectangle(
            (40,40+i,1160,41+i),
            fill=(r,g,b)
        )

    # ---------------------------------------------------
    # HEADER TEXT
    # ---------------------------------------------------

    title_font = get_font(78, True)
    sub_font = get_font(38, False)
    amount_font = get_font(58, True)
    normal_font = get_font(34, False)
    small_font = get_font(28, False)
    badge_font = get_font(28, True)

    draw.text(
        (170,120),
        "SCAN FOR PAYMENT",
        fill="white",
        font=title_font
    )

    draw.text(
        (390,230),
        "Secure UPI Payment",
        fill="#e2e8f0",
        font=sub_font
    )

    # ---------------------------------------------------
    # QR CONTAINER
    # ---------------------------------------------------

    draw.rounded_rectangle(
        (210,380,990,1160),
        radius=40,
        fill="#ffffff",
        outline="#2563eb",
        width=4
    )

    qr_resized = qr_image.resize((620,620))

    canvas.paste(qr_resized, (290,460))

    # ---------------------------------------------------
    # AMOUNT BOX
    # ---------------------------------------------------

    draw.rounded_rectangle(
        (300,1200,900,1290),
        radius=24,
        fill="#1d4ed8"
    )

    draw.text(
        (380,1218),
        f"Amount: ₹{amount}",
        fill="#facc15",
        font=amount_font
    )

    # ---------------------------------------------------
    # MERCHANT DETAILS
    # ---------------------------------------------------

    draw.text(
        (240,1360),
        f"Merchant Name: {merchant_name}",
        fill="#1e293b",
        font=normal_font
    )

    draw.text(
        (240,1435),
        f"UPI ID: {upi_id}",
        fill="#1e293b",
        font=normal_font
    )

    # ---------------------------------------------------
    # DIVIDER
    # ---------------------------------------------------

    draw.line(
        (180,1525,1020,1525),
        fill="#cbd5e1",
        width=3
    )

    draw.text(
        (470,1560),
        "SUPPORTED ON",
        fill="#1d4ed8",
        font=badge_font
    )

    # ---------------------------------------------------
    # PAYMENT BADGES
    # ---------------------------------------------------

    badges = [
        ("Google Pay", 90),
        ("PhonePe", 350),
        ("Paytm", 610),
        ("BHIM", 870)
    ]

    for text, x in badges:

        draw.rounded_rectangle(
            (x,1640,x+220,1725),
            radius=22,
            outline="#2563eb",
            width=3,
            fill="#ffffff"
        )

        draw.text(
            (x+28,1665),
            text,
            fill="#111827",
            font=normal_font
        )

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------

    draw.rectangle(
        (40,1770,1160,1860),
        fill="#0f172a"
    )

    draw.text(
        (320,1795),
        "100% Secure UPI Payment",
        fill="white",
        font=badge_font
    )

    draw.text(
        (345,1835),
        "Generated by Premium QR Generator",
        fill="#cbd5e1",
        font=small_font
    )

    return canvas

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------

def get_download_link(img):

    buffered = BytesIO()

    img.save(
        buffered,
        format="PNG",
        quality=100
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
    padding:16px;
    border:none;
    border-radius:14px;
    background:linear-gradient(90deg,#22c55e,#38bdf8);
    color:white;
    font-size:22px;
    font-weight:700;
    cursor:pointer;
    margin-top:10px;
    ">
    ⬇ Download Premium QR Card
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
        "Merchant Name (Optional)",
        value="Payment"
    )

    if st.button("🚀 Generate QR Code"):

        with st.spinner("Generating Premium QR..."):

            time.sleep(1)

            upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={amount}&cu=INR"

            qr = generate_qr(upi_url)

            premium_card = create_premium_card(
                qr,
                amount,
                merchant_name,
                selected_upi
            )

            st.success(
                f"✅ QR Generated successfully at {time.strftime('%H:%M:%S')}"
            )

            st.image(
                premium_card,
                use_container_width=True
            )

            st.markdown(
                get_download_link(premium_card),
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    '<div class="footer">Secure • Fast • Professional<br>© 2026 Parivahan Service Fintech</div>',
    unsafe_allow_html=True
)
