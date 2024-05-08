from fastapi import FastAPI, Response
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
                matches = json.loads(response.text)
                return matches
    return None

@app.get("/matches-data")
async def get_api_data():
    data = await fetch_match_data()
    return data

@app.get("/get_escudo_image/{team_id}")
async def get_escudo_image(team_id):
    async with httpx.AsyncClient() as client:
        url = f"https://arquivos.admsuperplacar.com.br/img_{team_id}_48.png"
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.RequestError as e:
            return {"error": f"Erro ao buscar a imagem: {e}"}
    
    return Response(content=response.content, media_type="image/png")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")