# ---------------------------------------------------
# PREMIUM STANDY DESIGN (EXACT PREMIUM STYLE)
# REPLACE ONLY THIS FUNCTION
# ---------------------------------------------------

def create_premium_standee(qr_image, amount, merchant_name, upi_id):

    WIDTH, HEIGHT = 1200, 1800

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#f3f6fb")
    draw = ImageDraw.Draw(canvas)

    # ---------------------------------------------------
    # FONTS
    # ---------------------------------------------------

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 72)
        sub_font = ImageFont.truetype("arial.ttf", 36)
        amount_font = ImageFont.truetype("arialbd.ttf", 54)
        details_font = ImageFont.truetype("arial.ttf", 34)
        footer_font = ImageFont.truetype("arialbd.ttf", 30)
        small_font = ImageFont.truetype("arial.ttf", 24)

    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        amount_font = ImageFont.load_default()
        details_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # ---------------------------------------------------
    # MAIN WHITE CARD
    # ---------------------------------------------------

    draw.rounded_rectangle(
        [40, 40, 1160, 1760],
        radius=40,
        fill="white"
    )

    # ---------------------------------------------------
    # PREMIUM HEADER
    # ---------------------------------------------------

    for i in range(320):

        r = 15 + int(i * 0.15)
        g = 30 + int(i * 0.08)
        b = 120 + int(i * 0.35)

        draw.line(
            [(40, 40 + i), (1160, 40 + i)],
            fill=(r, g, b),
            width=1
        )

    # Rounded top header
    draw.rounded_rectangle(
        [40, 40, 1160, 360],
        radius=40,
        outline=None
    )

    # Decorative lines
    draw.line([(340, 140), (470, 140)], fill="white", width=4)
    draw.line([(730, 140), (860, 140)], fill="white", width=4)

    # Shield icon circle
    draw.ellipse((565, 95, 635, 165), fill="#22c55e")
    draw.text((587, 112), "✓", fill="white", font=details_font)

    # Main Heading
    draw.text(
        (210, 180),
        "SCAN FOR PAYMENT",
        fill="white",
        font=title_font
    )

    # Subtitle
    draw.text(
        (410, 285),
        "Secure UPI Payment",
        fill="#e2e8f0",
        font=sub_font
    )

    # Decorative lines subtitle
    draw.line([(280, 305), (380, 305)], fill="white", width=3)
    draw.line([(820, 305), (920, 305)], fill="white", width=3)

    # ---------------------------------------------------
    # QR SHADOW
    # ---------------------------------------------------

    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        [200, 420, 1000, 1220],
        radius=45,
        fill=(0,0,0,70)
    )

    shadow = shadow.filter(ImageFilter.GaussianBlur(20))

    canvas.paste(shadow, (0,0), shadow)

    # ---------------------------------------------------
    # QR BOX
    # ---------------------------------------------------

    draw.rounded_rectangle(
        [190, 410, 1010, 1230],
        radius=45,
        fill="white",
        outline="#2563eb",
        width=5
    )

    # QR Resize
    qr_res = qr_image.resize((620, 620), Image.Resampling.LANCZOS)

    canvas.paste(qr_res, (290, 500))

    # ---------------------------------------------------
    # AMOUNT BOX
    # ---------------------------------------------------

    draw.rounded_rectangle(
        [320, 1270, 880, 1365],
        radius=28,
        fill="#1d4ed8"
    )

    amount_text = f"Amount: ₹{amount}"

    draw.text(
        (390, 1292),
        amount_text,
        fill="#facc15",
        font=amount_font
    )

    # ---------------------------------------------------
    # MERCHANT DETAILS
    # ---------------------------------------------------

    # Merchant icon circle
    draw.ellipse((220, 1420, 265, 1465), outline="#2563eb", width=3)

    draw.text(
        (290, 1422),
        f"Merchant Name: {merchant_name}",
        fill="#1e293b",
        font=details_font
    )

    # UPI icon circle
    draw.ellipse((220, 1500, 265, 1545), outline="#2563eb", width=3)

    draw.text(
        (290, 1502),
        f"UPI ID: {upi_id}",
        fill="#1e293b",
        font=details_font
    )

    # ---------------------------------------------------
    # DIVIDER
    # ---------------------------------------------------

    draw.line(
        [(150, 1610), (1050, 1610)],
        fill="#cbd5e1",
        width=3
    )

    draw.text(
        (470, 1570),
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
            [x, 1660, x + 220, 1745],
            radius=22,
            fill="white",
            outline="#2563eb",
            width=3
        )

        draw.text(
            (x + 35, 1688),
            app,
            fill="#1e293b",
            font=details_font
        )

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------

    for i in range(120):

        draw.line(
            [(40, 1760 + i), (1160, 1760 + i)],
            fill=(5, 20, 60 + i),
            width=1
        )

    draw.text(
        (350, 1790),
        "100% Secure UPI Payment",
        fill="white",
        font=footer_font
    )

    draw.text(
        (380, 1840),
        "Generated by Premium QR Generator",
        fill="#e2e8f0",
        font=small_font
    )

    return canvas
