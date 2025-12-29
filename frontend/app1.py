import streamlit as st
import requests
from PIL import Image
import os
import base64
import urllib.parse

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Ornament AI Classifier",
    page_icon="💎",
    layout="centered"
)

# ------------------ CSS ------------------
st.markdown("""
<style>

/* ===== BASE ===== */
body {
    background-color: #f4f6fb;
    color: #0f172a;
    font-family: "Segoe UI", Arial, sans-serif;
}

/* ===== HEADER ===== */
.header {
    text-align: center;
    padding: 22px 0;
}
.header-title {
    font-size: 42px;
    font-weight: 800;
    color: #1e40af;
}
.header-subtitle {
    font-size: 17px;
    font-weight: 600;
    color: #475569;
}

/* ===== INFO BOX (FIXED VISIBILITY) ===== */
.info-box {
    background: #f8fafc;
    padding: 18px;
    border-radius: 12px;
    margin-top: 18px;
    border-left: 6px solid #1e40af;
    color: #0f172a;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 6px;
}

.section-text {
    font-size: 15px;
    color: #0f172a;
    line-height: 1.6;
}

.section-list {
    font-size: 15px;
    color: #1f2937;
    line-height: 1.7;
}

/* ===== HORIZONTAL SCROLL GALLERY ===== */
.scroll-container {
    display: flex;
    flex-wrap: nowrap;
    gap: 18px;
    overflow-x: auto;
    padding: 14px 6px;
    width: 100%;
}
.scroll-container::-webkit-scrollbar {
    height: 8px;
}
.scroll-container::-webkit-scrollbar-thumb {
    background: #c7d2fe;
    border-radius: 4px;
}

/* ===== MAIN CARD ===== */
.main-card {
    background: #ffffff;
    padding: 24px;
    border-radius: 14px;
    margin-top: 24px;
    border: 1px solid #e5e7eb;
}

/* ===== RESULT ===== */
.result-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 18px;
    margin-top: 18px;
    text-align: center;
}
.prediction {
    font-size: 24px;
    font-weight: 800;
    color: #166534;
}
.confidence {
    font-size: 15px;
    color: #14532d;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #1e40af !important;
    color: #ffffff !important;
    font-weight: 700;
    height: 44px;
    border-radius: 8px;
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #475569;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<div class="header">
    <div class="header-title">💎 Ornament AI Classifier</div>
    <div class="header-subtitle">
        Vision Transformer based identification of traditional Indian ornaments
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------ INFO SECTIONS ------------------
st.markdown("""
<div class="info-box">
  <div class="section-title">📌 About the System</div>
  <div class="section-text">
    Classifies an uploaded ornament image into one of
    <b>17 traditional Indian ornament categories</b>
    using a <b>Vision Transformer (ViT-B/16)</b>.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
  <div class="section-title">🧠 Model & Technology</div>
  <div class="section-list">
    • Vision Transformer (ViT-B/16)<br>
    • PyTorch Deep Learning Framework<br>
    • FastAPI Backend<br>
    • Streamlit Frontend
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
  <div class="section-title">🧪 How to Use</div>
  <div class="section-list">
    1. Upload a clear ornament image<br>
    2. Click <b>Predict Ornament</b><br>
    3. View predicted class and confidence
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------ ORNAMENT LIST ------------------
ornaments = [
    ("Bajuband", "bajuband.jpg"),
    ("Bakuli Haar", "bakuli_haar.jpg"),
    ("Bugadi", "bugadi.jpg"),
    ("Chinchpeti", "chinchpeti.jpg"),
    ("Jodvi", "jodvi.jpg"),
    ("Kambarpatta", "kambarpatta.jpg"),
    ("Kolhapuri Saaj", "kolhapuri_saaj.jpg"),
    ("Kudya", "kudya.jpeg"),
    ("Laxmi Haar", "laxmi_haar.jpeg"),
    ("Mangalsutra", "mangalsutra.jpg"),
    ("Mohan Mala", "mohan_mala.jpg"),
    ("Nath", "nath.jpeg"),
    ("Patlya", "patlya.jpeg"),
    ("Surya Haar", "surya_haar.jpeg"),
    ("Tanmani", "tanmani.jpg"),
    ("Thushi", "thushi.jpg"),
    ("Tode", "tode.jpg"),
]

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ------------------ GALLERY ------------------
st.markdown("""
<div class="info-box">
  <div class="section-title">✨ Supported Ornament Categories (17)</div>
</div>
""", unsafe_allow_html=True)

gallery_html = "<div class='scroll-container'>"

for name, img_file in ornaments:
    img_path = os.path.join("assets", "ornaments", img_file)
    if os.path.exists(img_path):
        img_b64 = img_to_base64(img_path)
        gallery_html += (
            "<div style='min-width:160px;border:1px solid #e5e7eb;"
            "border-radius:12px;padding:10px;text-align:center;background:white;'>"
            f"<img src='data:image/jpeg;base64,{img_b64}' "
            "style='width:140px;height:140px;object-fit:contain;'/>"
            "<div style='font-size:13px;color:#475569;margin-top:6px;'>(Ornament Type)</div>"
            f"<div style='font-size:17px;font-weight:700;color:#1e40af;'>{name}</div>"
            "</div>"
        )

gallery_html += "</div>"
st.markdown(gallery_html, unsafe_allow_html=True)

# ------------------ ORNAMENT INFO ------------------
ornament_info = {
    "Bajuband": {
        "description": "Bajuband is a traditional armlet worn on the upper arm, often associated with royal and bridal attire.",
        "region": "Maharashtra, Rajasthan",
        "occasion": "Weddings, festivals"
    },
    "Bakuli Haar": {
        "description": "Bakuli Haar is a floral-inspired gold necklace resembling jasmine buds, symbolizing purity and elegance.",
        "region": "Maharashtra",
        "occasion": "Traditional ceremonies, weddings"
    },
    "Bugadi": {
        "description": "Bugadi is a distinctive ear ornament worn on the upper cartilage of the ear, common in rural traditions.",
        "region": "Maharashtra, Karnataka",
        "occasion": "Daily traditional wear, festivals"
    },
    "Chinchpeti": {
        "description": "Chinchpeti is a pearl choker necklace that sits close to the neck and is a staple of Maharashtrian bridal jewelry.",
        "region": "Maharashtra",
        "occasion": "Weddings"
    },
    "Jodvi": {
        "description": "Jodvi are toe rings traditionally worn by married women, symbolizing marital status.",
        "region": "Across India",
        "occasion": "Daily wear after marriage"
    },
    "Kambarpatta": {
        "description": "Kambarpatta is an ornate waist belt worn with sarees, often richly decorated with gold motifs.",
        "region": "Maharashtra, Karnataka",
        "occasion": "Weddings, classical dance"
    },
    "Kolhapuri Saaj": {
        "description": "Kolhapuri Saaj is a heavy traditional necklace featuring multiple symbolic pendants.",
        "region": "Kolhapur, Maharashtra",
        "occasion": "Weddings, religious ceremonies"
    },
    "Kudya": {
        "description": "Kudya are traditional ear studs often made of pearls or gemstones, worn daily.",
        "region": "Maharashtra",
        "occasion": "Daily traditional wear"
    },
    "Laxmi Haar": {
        "description": "Laxmi Haar is a long necklace featuring Goddess Laxmi motifs, symbolizing wealth and prosperity.",
        "region": "Maharashtra, South India",
        "occasion": "Weddings, festivals"
    },
    "Mangalsutra": {
        "description": "Mangalsutra is a sacred black-beaded necklace worn by married women as a symbol of marriage.",
        "region": "Across India",
        "occasion": "Daily wear after marriage"
    },
    "Mohan Mala": {
        "description": "Mohan Mala is a long necklace made of closely spaced gold beads, giving a regal appearance.",
        "region": "Maharashtra",
        "occasion": "Weddings, festive occasions"
    },
    "Nath": {
        "description": "Nath is a traditional nose ring, often pearl-studded, and an important part of bridal jewelry.",
        "region": "Maharashtra, North India",
        "occasion": "Weddings, festivals"
    },
    "Patlya": {
        "description": "Patlya are flat, broad gold bangles usually worn in pairs, symbolizing prosperity.",
        "region": "Maharashtra",
        "occasion": "Weddings, daily traditional wear"
    },
    "Surya Haar": {
        "description": "Surya Haar is a necklace featuring a sun-shaped pendant, representing energy and power.",
        "region": "Maharashtra",
        "occasion": "Festivals, weddings"
    },
    "Tanmani": {
        "description": "Tanmani is a pearl choker necklace with a central pendant, known for its delicate craftsmanship.",
        "region": "Maharashtra",
        "occasion": "Weddings, traditional functions"
    },
    "Thushi": {
        "description": "Thushi is a tightly strung choker made of gold beads, a hallmark of Maharashtrian jewelry.",
        "region": "Maharashtra",
        "occasion": "Weddings"
    },
    "Tode": {
        "description": "Tode are heavy, intricately carved bangles traditionally worn by brides.",
        "region": "Maharashtra",
        "occasion": "Weddings"
    }
}


def google_links(name):
    q = urllib.parse.quote(f"{name} traditional indian ornament")
    return {
        "search": f"https://www.google.com/search?q={q}",
        "images": f"https://www.google.com/search?tbm=isch&q={q}",
        "shopping": f"https://www.google.com/search?tbm=shop&q={q}",
    }

# ------------------ PREDICTION ------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload ornament image (JPG / PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width=320)

    if st.button("🔮 Predict Ornament"):
        with st.spinner("Analyzing image..."):
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                files={"file": uploaded_file.getvalue()},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                pred = result["prediction"]
                conf = result.get("confidence", 0)

                st.markdown(f"""
                <div class="result-card">
                    <div class="prediction">{pred}</div>
                    <div class="confidence">Confidence: {round(conf*100,2)}%</div>
                </div>
                """, unsafe_allow_html=True)

                info = ornament_info.get(pred)
                links = google_links(pred)

                st.markdown("### 📖 Ornament Information")
                if info:
                    st.markdown(f"""
                    **Description:** {info['description']}  
                    **Region:** {info['region']}  
                    **Occasion:** {info['occasion']}
                    """)
                else:
                    st.info("Detailed information will be added soon.")

                st.markdown("### 🔎 Explore More")
                st.markdown(f"""
                - 🌐 [Google Search]({links['search']})
                - 🖼️ [Image Results]({links['images']})
                - 🛍️ [Shopping Results]({links['shopping']})
                """)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
© Ornament Classification Project • Built with FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)
