from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Alive & Kicking"}

@app.get("/helloworld")
async def say_helloworld():
    return {"message": "Hello World"}

@app.post("/readpdf")
async def receive_pdf(file: UploadFile = File(...)):
    # print(f"Received file: {file.filename}")

    # Read file content into memory
    file_content = await file.read()

    # Load it into PyMuPDF from memory
    doc = fitz.open(stream=file_content, filetype="pdf")

    # Extract text from all pages
    full_text = ''.join(page.get_text() for page in doc)

    return {
        "filename": file.filename,
        "text": full_text
    }
