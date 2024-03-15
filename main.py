from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from ResumeTools import does_resume_have_live_links
import os
import shutil


app=FastAPI()

@app.get('/')
def home():
    return {'Message':"Welcome to resume filtering App to the /check_live_links POST route to acess the feature"}


@app.post("/check_live_links")
async def check_live_links(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            shutil.copyfileobj(file.file, temp_pdf)

        # Check if the PDF has live links
        result = does_resume_have_live_links(temp_pdf.name)

        # # Remove the temporary file
        temp_pdf_path = temp_pdf.name
        temp_pdf.close()
        os.unlink(temp_pdf_path)

        return JSONResponse(content={"has_live_links": result})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


import uvicorn
uvicorn.run(app)