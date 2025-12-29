from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import io

from torchvision.models import vit_b_16

app = FastAPI()

# CORS (for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ MODEL LOADING ------------------

NUM_CLASSES = 17

try:
    model = vit_b_16(weights=None)

    # EXACT training head (single Linear at index 1)
    model.heads = nn.Sequential(
        nn.Identity(),
        nn.Linear(768, NUM_CLASSES)
    )

    state_dict = torch.load("vit_ornament_model.pth", map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    print("✅ Model loaded successfully")

except Exception as e:
    print("❌ Model loading failed:", e)
    model = None
    
# ------------------ IMAGE PREPROCESSING ------------------
# IMPORTANT: ViT normalization
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ------------------ CLASS LABELS ------------------

classes = [
    'Bajuband',
    'Bakuli Haar',
    'Bugadi',
    'Chinchpeti',
    'Jodvi',
    'Kambarpatta',
    'Kolhapuri Saaj',
    'Kudya',
    'Laxmi Haar',
    'Mangalsutra',
    'Mohan Mala',
    'Nath',
    'Patlya',
    'Surya Haar',
    'Tanmani',
    'Thushi',
    'Tode'
]

# ------------------ API ------------------

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model not loaded"}

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)
        predicted = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted].item()

    return {
        "prediction": classes[predicted],
        "confidence": round(confidence, 4)
    }
