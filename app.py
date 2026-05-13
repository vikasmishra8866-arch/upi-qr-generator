import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageOps, ImageDraw, ImageFont
import base64
import time

# --- Page Configuration ---
st.set_page_config(page_title="Premium UPI QR Generator", page_icon="💳", layout="centered")

# --- Custom Premium CSS (Glassmorphism & Fintech Theme) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Premium Card Container */
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }

    /* Header Styling */
    .header-text {
        text-align: center;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    
    .subtitle-text {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.5);
        border: none;
        color: white;
    }

    /* Input & Select Box Styling */
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #64748b;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def generate_qr(upi_url):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e293b", back_color="white").convert('RGB')
    return img

def get_image_download_link(img, filename, text):
    # --- Premium Payment Card Configuration ---
    card_w = 600
    card_h = 850
    
    # 1. Create Base Canvas with subtle off-white background
    canvas = Image.new('RGB', (card_w, card_h), '#F8FAFC')
    draw = ImageDraw.Draw(canvas)
    
    # 2. Add Premium Gradient Header (Dark Blue to Navy)
    header_height = 160
    for i in range(header_height):
        r = int(15 + (i * (30 - 15) / header_height))
        g = int(23 + (i * (41 - 23) / header_height))
        b = int(42 + (i * (59 - 42) / header_height))
        draw.line([(0, i), (card_w, i)], fill=(r, g, b))
    
    # 3. Add Header Text
    try:
        draw.text((card_w // 2 - 140, 45), "SCAN FOR PAYMENT", fill="#38BDF8")
        draw.text((card_w // 2 - 80, 95), "Secure UPI Payment", fill="#94A3B8")
    except:
        draw.text((card_w // 2 - 100, 50), "SCAN FOR PAYMENT", fill="white")

    # 4. Create Main QR White Container with Shadow effect
    draw.rectangle([55, 185, 555, 685], fill="#E2E8F0") 
    draw.rectangle([50, 180, 550, 680], fill="white") 
    
    # 5. Process and Paste QR Code
    qr_res = img.resize((400, 400), Image.Resampling.LANCZOS)
    canvas.paste(qr_res, (100, 230))
    
    # 6. Add Payment Info below QR
    amt = st.session_state.get('amount_input', '0.00')
    draw.text((card_w // 2 - 60, 640), f"Amount: ₹{amt}", fill="#1E293B")
    
    # 7. Supported Apps Section
    y_pos = 710
    draw.text((card_w // 2 - 55, y_pos), "SUPPORTED ON", fill="#64748B")
    
    badges = ["GPay", "PhonePe", "Paytm", "BHIM"]
    start_x = 80
    for badge in badges:
        draw.rectangle([start_x, y_pos + 30, start_x + 100, y_pos + 65], fill="#F1F5F9", outline="#CBD5E1")
        draw.text((start_x + 20, y_pos + 40), badge, fill="#475569")
        start_x += 115

    # 8. Footer Section
    draw.line([(100, 800), (500, 800)], fill="#E2E8F0", width=1) 
    footer_text = "100% Secure UPI Payment  •  Fintech Powered"
    draw.text((card_w // 2 - 160, 815), footer_text, fill="#94A3B8")

    # --- Convert to Downloadable Link ---
    buffered = BytesIO()
    canvas.save(buffered, format="PNG", optimize=True, quality=100)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    href = f'''
    <a href="data:file/png;base64,{img_str}" download="{filename}" style="text-decoration:none;">
        <button style="
            width:100%; 
            border-radius:12px; 
            padding:14px; 
            background: linear-gradient(90deg, #10B981, #059669); 
            color:white; 
            border:none; 
            cursor:pointer; 
            font-weight:700;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        ">
            {text}
        </button>
    </a>
    '''
    return href

# --- UI Layout ---
st.markdown('<h1 class="header-text">Instant UPI QR Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Generate secure payment QR codes instantly</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    upi_options = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Select UPI ID", upi_options, help="Choose your pre-configured UPI ID")
    
    st.write("Quick Amount Selection")
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("₹50"): st.session_state.amount_input = 50.0
    if col2.button("₹100"): st.session_state.amount_input = 100.0
    if col3.button("₹150"): st.session_state.amount_input = 150.0
    if col4.button("₹200"): st.session_state.amount_input = 200.0
    
    custom_amount = st.number_input("Enter Amount (₹)", min_value=0.0, step=1.0, key="amount_input")
    merchant_name = st.text_input("Merchant Name (Optional)", value="Payment")

    if st.button("🚀 Generate QR Code"):
        if custom_amount <= 0:
            st.warning("Please enter a valid amount greater than 0.")
        else:
            with st.spinner("Creating your secure QR..."):
                time.sleep(1) 
                
                upi_url = f"upi://pay?pa={selected_upi}&pn={merchant_name}&am={custom_amount}&cu=INR"
                qr_img = generate_qr(upi_url)
                
                st.markdown("---")
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    st.image(qr_img, caption=f"Scan to Pay: ₹{custom_amount:,.2f}", use_container_width=True)
                    
                    st.markdown("""
                        <div style="text-align:center; margin-top:10px;">
                            <span style="color:#94a3b8; font-size:12px;">Supported Apps</span><br>
                            <span style="font-size:20px;">🅿️ 🛄 💳 📱</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.success(f"QR Generated successfully at {time.strftime('%H:%M:%S')}")
                
                st.markdown(get_image_download_link(qr_img, "Premium_UPI_QR.png", "📥 Download Premium QR Card"), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('<p class="footer">Secure • Fast • Professional<br>© 2026 Parivahan Service Fintech</p>', unsafe_allow_html=True)
