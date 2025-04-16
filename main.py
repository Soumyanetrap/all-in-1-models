from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io

from services.groq import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Alive & Kicking"}

@app.get("/helloworld")
async def say_helloworld():
    return {"message": "Hello World"}

@app.post("/readpdf")
async def receive_pdf(file: UploadFile = File(...)):
    file_content = await file.read()

    pdf_file = io.BytesIO(file_content)

    full_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if (text := page.extract_text()):
                full_text += text + "\n"
                
    pdf_data = chat(full_text)

    return {
        "filename": file.filename,
        **pdf_data
    }
