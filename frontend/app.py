import streamlit as st
import requests
from PIL import Image
import os
import base64

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Ornament AI Classifier",
    page_icon="💎",
    layout="centered"
)

# ------------------ ORIGINAL CSS (UNCHANGED) ------------------
st.markdown("""
<style>

/* ===== BASE ===== */
body {
    background-color: #f4f6fb;
    color: #1f2937;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 16px;
}

/* ===== HEADER ===== */
.header {
    text-align: center;
    padding: 22px 0;
}
.header-title {
    font-size: 42px;
    font-weight: 800;
    color: #1e40af;              /* Royal blue (bright, not black) */
    letter-spacing: 0.5px;
}

.header-subtitle {
    font-size: 17px;
    font-weight: 600;
    color: #475569;              /* Slate blue-gray (clearly visible) */
    margin-top: 6px;
}



/* ===== INFO BOX ===== */
.info-box {
    background: #ffffff;
    padding: 18px;
    border-radius: 12px;
    margin-top: 18px;
    border-left: 6px solid #1e40af;
}

/* ===== SECTION ===== */
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #1e40af;
}
.section-text {
    font-size: 15px;
    color: #1f2937;
    line-height: 1.6;
}
.section-list {
    font-size: 15px;
    color: #374151;
    line-height: 1.6;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #1e40af !important;
    color: white !important;
    font-weight: 700;
    height: 44px;
    border-radius: 8px;
}

/* ===== RESULT ===== */
.result-card {
    background: #f8fafc;
    border: 1px solid #cbd5f5;
    border-radius: 12px;
    padding: 18px;
    margin-top: 18px;
    text-align: center;
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #64748b;
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
    This application classifies an uploaded ornament image into one of
    <b>17 traditional Indian ornament categories</b> using a
    <b>Vision Transformer (ViT-B/16)</b>.
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

# ------------------ ORNAMENT DATA ------------------
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

# ------------------ FIXED HORIZONTAL GALLERY (ONLY CHANGE) ------------------
st.markdown("""
<div class="info-box">
  <div class="section-title">✨ Supported Ornament Categories (17)</div>
</div>
""", unsafe_allow_html=True)

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

gallery_html = "<div style='display:flex;flex-wrap:nowrap;overflow-x:auto;gap:18px;padding:14px;'>"

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

# ------------------ PREDICTION ------------------
st.markdown("<div class='info-box'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔮 Predict Ornament</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload ornament image (JPG / PNG / JPEG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, width=300)

    if st.button("Predict Ornament"):
        with st.spinner("Analyzing image..."):
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                files={"file": uploaded_file.getvalue()},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                st.markdown(f"""
                <div class="result-card">
                    <b>Prediction:</b> {result['prediction']}<br>
                    <b>Confidence:</b> {round(result.get('confidence',0)*100,2)}%
                </div>
                """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
© Ornament Classification Project • Built with FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)
