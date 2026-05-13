# app.py

import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import base64
import time

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Premium UPI QR Generator",
    page_icon="💳",
    layout="centered"
)

# -----------------------------------
# PREMIUM CSS
# -----------------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
    color:white;
}

.main-card{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    border-radius:24px;
    padding:32px;
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 20px 50px rgba(0,0,0,0.4);
}

.header{
    text-align:center;
    font-size:42px;
    font-weight:800;
    background: linear-gradient(90deg,#38bdf8,#818cf8);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:5px;
}

.sub{
    text-align:center;
    color:#94a3b8;
    margin-bottom:30px;
}

div.stButton > button{
    width:100%;
    border:none;
    border-radius:14px;
    padding:12px;
    font-weight:700;
    color:white;
    background: linear-gradient(90deg,#0ea5e9,#6366f1);
    transition:0.3s;
}

div.stButton > button:hover{
    transform:translateY(-2px);
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#94a3b8;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# QR GENERATION
# -----------------------------------
def generate_qr(upi_url):

    qr = qrcode.QRCode(
        version=1,
        box_size=14,
        border=2
    )

    qr.add_data(upi_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#111827",
        back_color="white"
    ).convert("RGB")

    return img


# -----------------------------------
# PREMIUM QR CARD
# -----------------------------------
def create_premium_qr_card(
    qr_img,
    amount,
    merchant_name,
    upi_id
):

    width = 900
    height = 1500

    # MAIN BACKGROUND
    bg = Image.new("RGB", (width, height), "#eef2ff")
    draw = ImageDraw.Draw(bg)

    # CARD
    card_margin = 40

    card = Image.new(
        "RGBA",
        (width - 80, height - 80),
        (255,255,255,255)
    )

    # SHADOW
    shadow = Image.new(
        "RGBA",
        (width - 40, height - 40),
        (0,0,0,0)
    )

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        (10,10,width-130,height-130),
        radius=40,
        fill=(0,0,0,90)
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(18))

    bg.paste(shadow,(10,20),shadow)

    # MAIN CARD
    card_draw = ImageDraw.Draw(card)

    card_draw.rounded_rectangle(
        (0,0,width-80,height-80),
        radius=45,
        fill="white"
    )

    bg.paste(card,(40,40))

    # HEADER GRADIENT
    header_height = 240

    for i in range(header_height):
        color = (
            int(15 + i * 0.2),
            int(23 + i * 0.1),
            int(42 + i * 0.4)
        )

        draw.rectangle(
            [(40,40+i),(width-40,40+i+1)],
            fill=color
        )

    # HEADER ROUND FIX
    draw.rounded_rectangle(
        (40,40,width-40,300),
        radius=45,
        outline=None
    )

    # FONTS
    try:
        title_font = ImageFont.truetype("arial.ttf", 52)
        sub_font = ImageFont.truetype("arial.ttf", 28)
        amount_font = ImageFont.truetype("arial.ttf", 44)
        small_font = ImageFont.truetype("arial.ttf", 24)
        brand_font = ImageFont.truetype("arial.ttf", 26)

    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        amount_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    # HEADER TEXT
    draw.text(
        (170,100),
        "SCAN FOR PAYMENT",
        fill="white",
        font=title_font
    )

    draw.text(
        (300,180),
        "Secure UPI Payment",
        fill="#cbd5e1",
        font=sub_font
    )

    # QR CONTAINER
    qr_box_x = 140
    qr_box_y = 360
    qr_box_size = 620

    draw.rounded_rectangle(
        (
            qr_box_x,
            qr_box_y,
            qr_box_x + qr_box_size,
            qr_box_y + qr_box_size
        ),
        radius=35,
        fill="#f8fafc",
        outline="#dbeafe",
        width=5
    )

    # QR IMAGE
    qr_resized = qr_img.resize((520,520))

    bg.paste(
        qr_resized,
        (190,410)
    )

    # AMOUNT
    draw.text(
        (310,1020),
        f"Amount: ₹{amount}",
        fill="#111827",
        font=amount_font
    )

    # MERCHANT
    draw.text(
        (230,1090),
        f"Merchant: {merchant_name}",
        fill="#475569",
        font=sub_font
    )

    # UPI ID
    draw.text(
        (180,1145),
        f"UPI ID: {upi_id}",
        fill="#64748b",
        font=small_font
    )

    # DIVIDER
    draw.line(
        (120,1200,780,1200),
        fill="#e2e8f0",
        width=3
    )

    # SUPPORTED TEXT
    draw.text(
        (315,1235),
        "SUPPORTED ON",
        fill="#475569",
        font=sub_font
    )

    # APP BADGES
    badges = [
        "Google Pay",
        "PhonePe",
        "Paytm",
        "BHIM"
    ]

    start_x = 95
    y = 1310

    for badge in badges:

        draw.rounded_rectangle(
            (start_x,y,start_x+160,y+55),
            radius=18,
            fill="#eff6ff",
            outline="#bfdbfe",
            width=2
        )

        draw.text(
            (start_x+18,y+15),
            badge,
            fill="#1e293b",
            font=brand_font
        )

        start_x += 180

    # FOOTER
    draw.text(
        (260,1410),
        "100% Secure UPI Payment",
        fill="#0f172a",
        font=sub_font
    )

    draw.text(
        (250,1450),
        "Generated by Premium QR Generator",
        fill="#64748b",
        font=small_font
    )

    return bg


# -----------------------------------
# DOWNLOAD BUTTON
# -----------------------------------
def get_download_link(img):

    buffered = BytesIO()

    img.save(
        buffered,
        format="PNG"
    )

    img_str = base64.b64encode(
        buffered.getvalue()
    ).decode()

    href = f'''
    <a href="data:file/png;base64,{img_str}"
    download="Premium_UPI_QR.png"
    style="text-decoration:none;">

    <button style="
    width:100%;
    background:linear-gradient(90deg,#10b981,#059669);
    color:white;
    border:none;
    padding:14px;
    border-radius:14px;
    font-weight:700;
    font-size:16px;
    cursor:pointer;
    ">
    📥 Download Premium QR
    </button>

    </a>
    '''

    return href


# -----------------------------------
# UI
# -----------------------------------
st.markdown(
    '<div class="header">Instant UPI QR Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">Generate secure premium payment QR instantly</div>',
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

    st.write("### Quick Amount")

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
        "Enter Amount",
        min_value=1,
        step=1,
        key="amount"
    )

    merchant_name = st.text_input(
        "Merchant Name",
        value="Payment"
    )

    if st.button("🚀 Generate Premium QR"):

        if amount <= 0:

            st.warning(
                "Please enter valid amount."
            )

        else:

            with st.spinner(
                "Generating Premium QR..."
            ):

                time.sleep(1)

                upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={amount}&cu=INR"

                qr_img = generate_qr(upi_url)

                premium_card = create_premium_qr_card(
                    qr_img,
                    amount,
                    merchant_name,
                    selected_upi
                )

                st.image(
                    premium_card,
                    use_container_width=True
                )

                st.success(
                    f"Premium QR Generated Successfully • {time.strftime('%H:%M:%S')}"
                )

                st.markdown(
                    get_download_link(premium_card),
                    unsafe_allow_html=True
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown(
    '<div class="footer">Secure • Fast • Professional</div>',
    unsafe_allow_html=True
)
