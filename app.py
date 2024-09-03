import tensorflow as tf
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the model
model = tf.keras.models.load_model('palm_disease_detection_model.keras')
print("Model loaded successfully!")

# Image dimensions
img_height, img_width = 224, 224

# Class indices (should match your trained model's classes)
class_indices = {
    'Brown Spots': 0,
    'Healthy': 1,
    'White Scale': 2,
    # Add all your classes here
}

def predict_image(image: Image.Image):
    """Process the image and return the predicted class."""
    # Resize the image
    img = image.resize((img_height, img_width))
    
    # Convert image to array
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image

    # Predict
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions[0])
    class_label = list(class_indices.keys())[class_idx]

    return class_label

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """Endpoint to predict the disease from the uploaded image."""
    try:
        # Load the image from the uploaded file
        image = Image.open(file.file)
        class_label = predict_image(image)
        
        return JSONResponse(content={"predicted_class": class_label})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# To run the server, use: uvicorn script_name:app --reload
