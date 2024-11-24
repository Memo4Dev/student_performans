
import pandas as pd
import numpy as np
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained Pipeline
model = load_model("student_performance_api")

# Create input model with type annotations
class StudentPerformanceInput(BaseModel):
    Age: float
    Gender: float
    Ethnicity: float
    ParentalEducation: float
    StudyTimeWeekly: float
    Absences: float
    Tutoring: float
    ParentalSupport: float
    Extracurricular: float
    Sports: float
    Music: float
    Volunteering: float

# Create output model
class StudentPerformanceOutput(BaseModel):
    prediction: int

# Helper function to convert numpy types to native Python types
def convert_numpy_types(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# Define predict function
@app.post("/predict", response_model=StudentPerformanceOutput)
async def predict(request: Request):
    try:
        # Log incoming request details
        body = await request.json()
        logger.info(f"Received data: {body}")

        # Validate input data
        try:
            input_data = StudentPerformanceInput(**body)
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            return JSONResponse(
                status_code=422, 
                content={"detail": str(e)}
            )

        # Convert data to DataFrame
        data_df = pd.DataFrame([input_data.model_dump()])
        logger.info(f"DataFrame: {data_df}")

        # Make prediction
        predictions = predict_model(model, data=data_df)
        logger.info(f"Predictions: {predictions}")

        # Extract prediction and convert to native Python type
        prediction = int(predictions["prediction_label"].iloc[0])
        logger.info(f"Final Prediction: {prediction}")

        # Return prediction
        return {"prediction": prediction}

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
