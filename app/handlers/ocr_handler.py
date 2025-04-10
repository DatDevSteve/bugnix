import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from msrest.authentication import CognitiveServicesCredentials
from azure.core.credentials import AzureKeyCredential
from PIL import Image
import io 

#credentials loading:
load_dotenv()
AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")
AZURE_OCR_CREDENTIALS = AzureKeyCredential(os.getenv("AZURE_OCR_KEY"))

#computer vision client:
cv_client = ImageAnalysisClient(
    endpoint=AZURE_OCR_ENDPOINT, credential=AZURE_OCR_CREDENTIALS
)
hardcodeImage = "app/handlers/ocr_sample_inputs/sample_traceback_error.png" #hardcode for testing
def extract_text(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            image_stream = f.read()
            ocr_result = cv_client.analyze(image_data=image_stream, visual_features=["read"])
            #process ocr result into human readable
            lines = []
            for block in ocr_result.read.blocks:
                for line in block.lines:
                    lines.append(line.text)
            final_result = "\n".join(lines)
            #print(final_result) # for hardcode testing
            return final_result
    except Exception as e:
        return f'OCR ERROR: {str(e)}'
    
#extract_text("hi") #for hardcode testing
    

    