import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Premium UPI QR Generator",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS FOR PREMIUM UI ---
def local_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #ffffff;
        }
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
        }
        h1 {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            background: -webkit-linear-gradient(#fff, #a5a5a5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        .sub-heading { text-align: center; color: #b0b0b0; font-size: 1.1rem; margin-bottom: 40px; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
            background-color: rgba(255, 255, 255, 0.07) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 12px;
            font-weight: 600;
        }
        .qr-display-container {
            background: white;
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            color: #1a1a1a;
            margin-top: 20px;
        }
        .upi-badge {
            display: inline-block;
            background: #f0f0f0;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #666;
            margin-top: 10px;
        }
        .footer { text-align: center; margin-top: 50px; color: #666; font-size: 0.8rem; }
        </style>
    """, unsafe_allow_html=True)

local_css()

st.markdown("<h1>Premium UPI QR Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-heading'>Generate stylish UPI payment QR codes instantly</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    upi_suggestions = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Enter or Select UPI ID", options=upi_suggestions)
    custom_upi = st.text_input("Or type custom UPI ID manually", value=selected_upi)
    final_upi = custom_upi if custom_upi else selected_upi

    st.write("---")
    st.markdown("<b>Select or Enter Amount (INR)</b>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    if 'amt' not in st.session_state:
        st.session_state.amt = 1.0

    if col1.button("₹50"): st.session_state.amt = 50.0
    if col2.button("₹100"): st.session_state.amt = 100.0
    if col3.button("₹150"): st.session_state.amt = 150.0
    if col4.button("₹200"): st.session_state.amt = 200.0

    amount = st.number_input("Enter Amount", min_value=1.0, value=st.session_state.amt, key="amount_input")
    generate_btn = st.button("✨ Generate Premium QR")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn:
    if final_upi:
        upi_url = f"upi://pay?pa={final_upi}&pn=UPI%20Payment&am={amount}&cu=INR"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(upi_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # --- PILLOW: INCREASED TEXT SIZE FOR DOWNLOAD ---
        q_w, q_h = qr_img.size
        c_w = q_w + 100
        c_h = q_h + 200 # Space for larger text
        canvas = Image.new('RGB', (c_w, c_h), 'white')
        draw = ImageDraw.Draw(canvas)
        
        # Text to be drawn
        header_text = "SCAN AND PAY ANY UPI APP"
        footer_text = f"Amount: ₹{amount}"
        
        # Note: Streamlit Cloud/Github usually has a default font. 
        # Using a simple trick to simulate "bold/large" without external .ttf files
        def draw_bold_text(draw, position, text, fill="black"):
            x, y = position
            draw.text((x, y), text, fill=fill)
            draw.text((x+1, y), text, fill=fill) # Offset for boldness

        # Paste QR Code
        canvas.paste(qr_img, (50, 100))
        
        # Draw Larger Labels (Centered)
        draw_bold_text(draw, (c_w//2 - 100, 40), header_text)
        draw_bold_text(draw, (c_w//2 - 60, c_h - 60), footer_text)

        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # UI Display
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <div class="qr-display-container" style="width: 350px; border: 2px solid #8E54E9;">
                    <p style="font-weight: 600; margin-bottom: 10px;">Scan and Pay using any UPI App</p>
        """, unsafe_allow_html=True)
        st.image(byte_im, width=280)
        st.markdown(f"""
                    <div style="margin-top: 10px;">
                        <h2 style="color: #1a1a1a; margin: 0;">₹{amount:,.2f}</h2>
                        <div class="upi-badge">{final_upi}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Download QR",
            data=byte_im,
            file_name=f"UPI_QR_{amount}.png",
            mime="image/png"
        )

st.markdown('<div class="footer"><p>🔒 Secure UPI Payments</p></div>', unsafe_allow_html=True)
