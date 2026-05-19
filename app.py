import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ultra-Premium UPI Standee", page_icon="💎", layout="centered")

# --- UI CUSTOM CSS (Glassmorphism + Futuristic Style) ---
st.markdown("""
    <style>
    /* Global Background - Futuristic Gradient */
    .stApp { 
        background: radial-gradient(circle at 10% 20%, #0c1521, #131d2c, #1a1e2b);
        color: white; 
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    /* Main Card Styling - Semi-Transparent Blurred Glass */
    .main-card {
        background: rgba(255, 255, 255, 0.015);
        padding: 40px; 
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        box-shadow: 0 40px 60px rgba(0,0,0,0.4);
        margin-top: 30px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    h1 { 
        font-weight: 900;
        letter-spacing: -2px;
        background: linear-gradient(to right, #60a5fa, #8b5cf6, #3b82f6); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        margin-bottom: 30px;
    }
    .stImage {
        border-radius: 20px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to get centered coordinates for text safely
def draw_centered_text(draw, canvas_w, y, text, font, fill):
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (canvas_w - text_w) // 2
    draw.text((text_x, y), text, font=font, fill=fill)

def generate_futuristic_card(upi_id, amount, custom_note):
    # Canvas Layout - Large vertical high-res canvas (650x1000)
    w, h = 650, 1000
    card = Image.new('RGB', (w, h), '#ffffff')
    draw = ImageDraw.Draw(card)
    
    # --- STEP 1: FUTURISTIC GLASS BACKGROUND ---
    # Top Header Area - Deep Blue Gradient
    draw.rectangle([0, 0, w, 260], fill='#0c1c3c') 
    
    # Bottom Body Area - Clean White Flat Area for Glass Box
    draw.rectangle([0, 260, w, h], fill='#ffffff')
    
    # --- INTERNAL ROBUST FONT LOADING SYSTEM (Standard Serif & Sans) ---
    try:
        # SCAN FOR PAYMENT के लिए Serif बोल्ड
        font_title = ImageFont.truetype("georgiab.ttf", 46) 
        font_subtitle = ImageFont.truetype("arial.ttf", 26)
        font_label = ImageFont.truetype("arial.ttf", 24)
        font_amount = ImageFont.truetype("arial.ttf", 64)  # Massive Size
        font_upi = ImageFont.truetype("arial.ttf", 30)
        font_footer = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        # फॉन्ट न मिलने पर Linux के लिए Fallback
        try:
            font_title = ImageFont.truetype("LiberationSerif-Bold.ttf", 46)
            font_subtitle = ImageFont.truetype("LiberationSans-Regular.ttf", 26)
            font_label = ImageFont.truetype("LiberationSans-Regular.ttf", 24)
            font_amount = ImageFont.truetype("LiberationSans-Bold.ttf", 64)
            font_upi = ImageFont.truetype("LiberationSans-Regular.ttf", 30)
            font_footer = ImageFont.truetype("LiberationSans-Regular.ttf", 22)
        except IOError:
            # Ultimate built-in fallback
            font_title = font_subtitle = font_label = font_amount = font_upi = font_footer = ImageFont.load_default()

    # 1. Header Texts Drawing
    draw_centered_text(draw, w, 65, "SCAN FOR PAYMENT", font_title, fill="white")
    draw_centered_text(draw, w, 140, "━━━━━━━━━━━━━━━━━━━━━━", font_subtitle, fill="#3b82f6")
    draw_centered_text(draw, w, 180, "USING ANY UPI APP", font_subtitle, fill="#bfdbfe")
    
    # --- STEP 2: GLASSMORPHISM BLUR BOX (Semi-Transparent Blurred Glass Layer) ---
    # इस कांच के बॉक्स के ऊपर सब कुछ तैरता हुआ लगेगा
    glass_w, glass_h = 550, 680
    gx, gy = (w - glass_w) // 2, 280
    
    # Create the glass container layer with blur
    glass_box = Image.new('RGB', (glass_w, glass_h), '#ffffff')
    glass_box_blur = glass_box.filter(ImageFilter.GaussianBlur(12)) # कांच जैसा धुंधला इफेक्ट
    # draw_glass_box = ImageDraw.Draw(glass_box_blur)
    
    # कांच के बॉक्स की आउटलाइन (border)
    # draw_glass_box.rounded_rectangle(
    #     [0, 0, glass_w, glass_h], radius=25, 
    #     outline='#e2e8f0', width=2
    # )
    
    # कांच के बॉक्स को कार्ड पर पेस्ट करें
    card.paste(glass_box_blur, (gx, gy))

    # --- STEP 3: ADVANCED QR CODE (Perfect Balanced Square) ---
    upi_url = f"upi://pay?pa={upi_id}&pn=UPI%20Payment&am={amount}&cu=INR&tn={custom_note}"
    qr = qrcode.QRCode(version=3, box_size=8, border=1) 
    qr.add_data(upi_url)
    qr.make(fit=True)
    # Futuristic dark-navy and blue pattern QR color
    qr_img = qr.make_image(fill_color="#102040", back_color="white").convert('RGB')
    
    qr_w, qr_h = qr_img.size
    bx, by = (w - qr_w) // 2, gy + 40 # Position relative to glass box
    
    # Sleek Border around QR inside Glass Box
    frame_padding = 15
    draw.rounded_rectangle(
        [bx - frame_padding, by - frame_padding, bx + qr_w + frame_padding, by + qr_h + frame_padding], 
        radius=20, 
        outline='#cbd5e1', 
        fill='#cbd5e1',
        width=3
    )
    card.paste(qr_img, (bx, by))
    
    # --- STEP 4: CLEAN ULTRA-PREMIUM PAYMENT DETAILS ---
    content_start_y = by + qr_h + 60
    
    # Label
    draw_centered_text(draw, w, content_start_y, "AMOUNT TO PAY", font_label, fill="#64748b")
    
    # Massive Amount display without currency symbol
    amount_str = f"{float(amount):,.2f}"
    draw_centered_text(draw, w, content_start_y + 45, amount_str, font_amount, fill="#0a0e17")

    # Minimalist Divider Line
    divider_y = content_start_y + 145
    draw.line([(100, divider_y), (500, divider_y)], fill="#e2e8f0", width=3)
    
    # Big UPI ID Text
    upi_label_str = f"UPI ID: {upi_id}"
    draw_centered_text(draw, w, divider_y + 35, upi_label_str, font_upi, fill="#1e293b")
    
    # Optional Note Text (हमेशा व्यवस्थित तरीके से रहेगा)
    note_text = custom_note.strip() if custom_note else ""
    note_label_str = f"Note: {note_text}" if note_text else "Note: N/A"
    draw_centered_text(draw, w, divider_y + 85, note_label_str, font_subtitle, fill="#94a3b8")

    # --- STEP 5: PREVIEW CLEAN FLAT FOOTER ---
    draw.rectangle([0, h-80, w, h], fill='#f1f5f9')
    draw_centered_text(draw, w, h-50, "🔒 SECURE UPI GATEWAY", font_footer, fill="#64748b")
    
    return card

# --- APP UI ---
st.markdown("<h1>💎 Ultra-Premium UPI Standee</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:16px;'>Futuristic glass-effect merchant payment stands.</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    upi_suggestions = ["9696159863.wallet@phonepe", "9696159863@ibl"]
    selected_upi = st.selectbox("Select UPI ID", upi_suggestions)
    custom_upi = st.text_input("Or Enter Custom ID", value=selected_upi)
    final_upi = custom_upi if custom_upi else selected_upi
    
    amount = st.number_input("Amount (INR)", min_value=1.0, value=100.0, step=10.0)
    note = st.text_input("Optional Payment Note (e.g., 'Coffee', 'Service')", value="Service Fee")

    if st.button("✨ Generate Balanced Card View", use_container_width=True):
        final_image = generate_futuristic_card(final_upi, amount, note)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(final_image, use_container_width=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
