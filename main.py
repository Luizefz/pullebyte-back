from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def extract_url_json():
    url = 'https://superplacar.com.br/'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        try:
            if response.status_code == 200:
                document = response.text
                match = re.search(r'var\s+urlJson\s*=\s*\"([^"]*)\"', document)
                if match:
                    return match.group(1)
        except Exception as e:
            return str(e)

async def fetch_match_data():
    url = await extract_url_json()
    if url:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                decoded_data = json.loads(response.text)
                matches = decoded_data['campeonatos']
                return matches
    return None

@app.get("/matches-data")
async def get_api_data():
    data = await fetch_match_data()
    return data

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")