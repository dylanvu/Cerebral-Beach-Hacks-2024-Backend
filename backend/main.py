from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import chat
from sanitizer import Email, run_cleaning_pipeline
from test_data.eml_data import *


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/prompt/")
async def clean_email(email: Email):
    return run_cleaning_pipeline(email)


@app.post("/analyze-local/")
async def analyze_email_local(path: str):
    try:
        with open(path, "r") as f:
            eml = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    llm_input = run_cleaning_pipeline(eml)
    print(llm_input)
    return chat(llm_input)


@app.post("/analyze/")
async def analyze_email(email: Email):
    try:
        llm_input = run_cleaning_pipeline(email.eml)
        print(llm_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return chat(llm_input)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)


# to run this, run "fastapi dev main.py"
# served at http://127.0.0.1:8000
