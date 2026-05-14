import streamlit as st
import qrcode
from PIL import Image
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
        /* Main Background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #ffffff;
        }

        /* Glassmorphism Card Effect */
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
        }

        /* Typography */
        h1 {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            background: -webkit-linear-gradient(#fff, #a5a5a5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 5px !important;
        }
        
        .sub-heading {
            text-align: center;
            color: #b0b0b0;
            font-size: 1.1rem;
            margin-bottom: 40px;
        }

        /* Input Styling */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
            background-color: rgba(255, 255, 255, 0.07) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }

        /* Button Styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(142, 84, 233, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(142, 84, 233, 0.5);
            color: white;
        }

        /* QR Display Card */
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

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #666;
            font-size: 0.8rem;
            letter-spacing: 1px;
        }
        
        /* Preset Buttons Row */
        .preset-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- APP LAYOUT ---
st.markdown("<h1>Premium UPI QR Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-heading'>Generate stylish UPI payment QR codes instantly</p>", unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # UPI ID Section
    upi_suggestions = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox(
        "Enter or Select UPI ID",
        options=upi_suggestions,
        index=0,
        help="Select a predefined UPI ID or type your own",
        placeholder="Type your UPI ID...",
    )
    
    # Manual Override (if user types custom)
    custom_upi = st.text_input("Or type custom UPI ID manually", value=selected_upi)
    final_upi = custom_upi if custom_upi else selected_upi

    st.write("---")

    # Amount Section
    st.markdown("<b>Select or Enter Amount (INR)</b>", unsafe_allow_html=True)
    
    # Preset Buttons Logic
    col1, col2, col3, col4 = st.columns(4)
    preset_amt = None
    if col1.button("₹50"): preset_amt = 50
    if col2.button("₹100"): preset_amt = 100
    if col3.button("₹150"): preset_amt = 150
    if col4.button("₹200"): preset_amt = 200

    # Amount Input
    if preset_amt:
        amount = st.number_input("Enter Amount", min_value=1.0, value=float(preset_amt), step=1.0)
    else:
        amount = st.number_input("Enter Amount", min_value=1.0, value=1.0, step=1.0)

    # Generate Button
    generate_btn = st.button("✨ Generate Premium QR")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- QR GENERATION LOGIC ---
if generate_btn:
    if not final_upi:
        st.error("Please enter a valid UPI ID")
    else:
        # Create UPI URL
        # upi://pay?pa=address@upi&pn=Name&am=100&cu=INR
        upi_url = f"upi://pay?pa={final_upi}&pn=UPI%20Payment&am={amount}&cu=INR"
        
        # QR Generation
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        img_qr = qr.make_image(fill_color="#000000", back_color="#ffffff").convert('RGB')
        
        # Save to buffer for Streamlit
        buf = io.BytesIO()
        img_qr.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Display Card
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <div class="qr-display-container" style="width: 350px; border: 2px solid #8E54E9;">
                    <p style="font-weight: 600; margin-bottom: 15px; color: #333;">Scan and Pay using any UPI App</p>
        """, unsafe_allow_html=True)
        
        st.image(byte_im, width=280)
        
        st.markdown(f"""
                    <div style="margin-top: 15px;">
                        <h2 style="color: #1a1a1a; margin: 0; font-size: 1.8rem;">₹{amount:,.2f}</h2>
                        <div class="upi-badge">{final_upi}</div>
                    </div>
                    <div style="display: flex; justify-content: space-around; align-items: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #eee;">
                        <img src="https://img.icons8.com/color/48/000000/google-pay-india.png" width="30"/>
                        <img src="https://img.icons8.com/color/48/000000/phonepe.png" width="30"/>
                        <img src="https://img.icons8.com/color/48/000000/paytm.png" width="30"/>
                        <img src="https://img.icons8.com/fluency/48/000000/bhim.png" width="30"/>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        col_down1, col_down2 = st.columns(2)
        with col_down1:
            st.download_button(
                label="📥 Download QR",
                data=byte_im,
                file_name="upi_qr_payment.png",
                mime="image/png"
            )
        with col_down2:
            if st.button("📋 Copy UPI ID"):
                st.write(f"ID: `{final_upi}` copied to clipboard (Simulated)")
                st.success("Copied!")

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        <p>🔒 Secure UPI Payments • Verified NPCI Format</p>
    </div>
""", unsafe_allow_html=True)
