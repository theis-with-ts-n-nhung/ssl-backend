import uvicorn
from dotenv import load_dotenv
load_dotenv()


def run():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8001, reload=True)