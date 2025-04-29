#OCR MODULE TO EXTRACT TEXT FROM IMAGE SCREENSHOTS
#USES AZURE COMPUTER VISION FOR OCR

import os
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from msrest.authentication import CognitiveServicesCredentials
from azure.core.credentials import AzureKeyCredential
from PIL import Image


#Setup Azure Computer Vision Instance:
load_dotenv()
AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")
AZURE_OCR_CREDENTIALS = AzureKeyCredential(os.getenv("AZURE_OCR_KEY"))
cv_client = ImageAnalysisClient(
    endpoint=AZURE_OCR_ENDPOINT, credential=AZURE_OCR_CREDENTIALS
)

#Text Extraction Function:
def extract_text(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            image_stream = f.read()
            ocr_result = cv_client.analyze(image_data=image_stream, visual_features=["read"])
            #Process OCR result into readable content:
            lines = []
            for block in ocr_result.read.blocks:
                for line in block.lines:
                    lines.append(line.text)
            final_result = "\n".join(lines)
            return final_result
    except Exception as e:
        return f'OCR ERROR: {str(e)}'
        

    