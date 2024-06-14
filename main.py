from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx
import re
import json

app = FastAPI()
dados_times = [{"nome":"Brasil","escudoUrl":"https://escudosfc.com.br/images/cbf2.jpg"},{"nome":"Athletico Paranaense ","escudoUrl":"https://escudosfc.com.br/images/atlpr.png"},{"nome":"Atletico Goianiense","escudoUrl":"https://escudosfc.com.br/images/atlego.png"},{"nome":"Atlético Mineiro","escudoUrl":"https://escudosfc.com.br/images/atletico.png"},{"nome":"Bahia","escudoUrl":"https://escudosfc.com.br/images/bahia.png"},{"nome":"Botafogo","escudoUrl":"https://escudosfc.com.br/images/botafogo.gif"},{"nome":"Corinthians","escudoUrl":"https://escudosfc.com.br/images/corinthians.png"},{"nome":"Criciúma","escudoUrl":"https://escudosfc.com.br/images/criciuma.png"},{"nome":"Cruzeiro","escudoUrl":"https://escudosfc.com.br/images/cruzeiro.png"},{"nome":"Cuiabá","escudoUrl":"https://escudosfc.com.br/images/cuiaba_mt.png"},{"nome":"Flamengo","escudoUrl":"https://escudosfc.com.br/images/fla.png"},{"nome":"Fluminense","escudoUrl":"https://escudosfc.com.br/images/fluminense.png"},{"nome":"Fortaleza","escudoUrl":"https://escudosfc.com.br/images/fortaleza.png"},{"nome":"Grêmio","escudoUrl":"https://escudosfc.com.br/images/gremio.png"},{"nome":"Internacional","escudoUrl":"https://escudosfc.com.br/images/interrs.png"},{"nome":"Juventude","escudoUrl":"https://escudosfc.com.br/images/juventude.png"},{"nome":"Palmeiras","escudoUrl":"https://escudosfc.com.br/images/palmeiras.png"},{"nome":"Bragantino","escudoUrl":"https://escudosfc.com.br/images/bragantino.png"},{"nome":"São Paulo","escudoUrl":"https://escudosfc.com.br/images/saopaulo.png"},{"nome":"Vasco da Gama ","escudoUrl":"https://escudosfc.com.br/images/vasco.png"},{"nome":"Vitoria","escudoUrl":"https://escudosfc.com.br/images/vitoria.png"},{"nome":"Amazonas","escudoUrl":"https://escudosfc.com.br/images/amazonas_fc_am.png"},{"nome":"América-MG","escudoUrl":"https://escudosfc.com.br/images/ammg.png"},{"nome":"Avaí","escudoUrl":"https://escudosfc.com.br/images/avai.gif"},{"nome":"Botafogo","escudoUrl":"https://escudosfc.com.br/images/botasp.png"},{"nome":"Brusque","escudoUrl":"https://escudosfc.com.br/images/brusque.gif"},{"nome":"Ceará","escudoUrl":"https://escudosfc.com.br/images/ceara.png"},{"nome":"Chapecoense","escudoUrl":"https://escudosfc.com.br/images/chapeco.png"},{"nome":"Coritiba","escudoUrl":"https://escudosfc.com.br/images/coritiba.png"},{"nome":"CRB","escudoUrl":"https://escudosfc.com.br/images/crb.gif"},{"nome":"Goiás","escudoUrl":"https://escudosfc.com.br/images/goias.png"},{"nome":"Grêmio Novorizontino","escudoUrl":"https://escudosfc.com.br/images/novorizontino_novo.jpg"},{"nome":"Guarani","escudoUrl":"https://escudosfc.com.br/images/guarani.gif"},{"nome":"Ituano","escudoUrl":"https://escudosfc.com.br/images/ituano.png"},{"nome":"Mirassol","escudoUrl":"https://escudosfc.com.br/images/mirassol.jpg"},{"nome":"Operário","escudoUrl":"https://escudosfc.com.br/images/operario_pr.png"},{"nome":"Paysandu","escudoUrl":"https://escudosfc.com.br/images/paysandu_pa.png"},{"nome":"Ponte Preta ","escudoUrl":"https://escudosfc.com.br/images/pontepreta.gif"},{"nome":"Santos","escudoUrl":"https://escudosfc.com.br/images/santos.png"},{"nome":"Sport","escudoUrl":"https://escudosfc.com.br/images/sport.gif"},{"nome":"Vila Nova","escudoUrl":"https://escudosfc.com.br/images/vilanova.png"},{"nome":"ABC","escudoUrl":"https://escudosfc.com.br/images/abc.jpg"},{"nome":"Aparecidense","escudoUrl":"https://escudosfc.com.br/images/aparecidense_go.png"},{"nome":"Atlético São João Del-Rey ","escudoUrl":"https://escudosfc.com.br/images/aletico_del_rey_mg.png"},{"nome":"Botafogo-PB","escudoUrl":"https://escudosfc.com.br/images/botapb.png"},{"nome":"Caxias","escudoUrl":"https://escudosfc.com.br/images/caxias.gif"},{"nome":"Confiança","escudoUrl":"https://escudosfc.com.br/images/confianca_se.png"},{"nome":"CSA","escudoUrl":"https://escudosfc.com.br/images/csa.png"},{"nome":"Ferroviária","escudoUrl":"https://escudosfc.com.br/images/ferroviaria.png"},{"nome":"Ferroviário","escudoUrl":"https://escudosfc.com.br/images/ferroviario.gif"},{"nome":"Figueirense","escudoUrl":"https://escudosfc.com.br/images/figue.gif"},{"nome":"Floresta","escudoUrl":"https://escudosfc.com.br/images/floresta_ce.png"},{"nome":"Londrina","escudoUrl":"https://escudosfc.com.br/images/londrina_pr.png"},{"nome":"Náutico","escudoUrl":"https://escudosfc.com.br/images/nautico.png"},{"nome":"Remo","escudoUrl":"https://escudosfc.com.br/images/remo.png"},{"nome":"Sampaio Correa","escudoUrl":"https://escudosfc.com.br/images/sampaio.png"},{"nome":"São Bernardo ","escudoUrl":"https://escudosfc.com.br/images/sao_bernarndo_sp.png"},{"nome":"  São José","escudoUrl":"https://escudosfc.com.br/images/saojose_rs.png"},{"nome":"Tombense","escudoUrl":"https://escudosfc.com.br/images/tombense_mg.png"},{"nome":"Volta Redonda","escudoUrl":"https://escudosfc.com.br/images/volta.png"},{"nome":"Ypiranga","escudoUrl":"https://escudosfc.com.br/images/ypiranga_rs.png"},{"nome":"Porto Velho","escudoUrl":"https://escudosfc.com.br/images/porto_velho_ro.png"},{"nome":"Humaitá","escudoUrl":"https://escudosfc.com.br/images/humaita_ac.png"},{"nome":"Manauara","escudoUrl":"https://escudosfc.com.br/images/manauara_am.png"},{"nome":"Manaus","escudoUrl":"https://escudosfc.com.br/images/manaus_fc.png"},{"nome":"Princesa","escudoUrl":"https://escudosfc.com.br/images/princesa_am.png"},{"nome":"Rio Branco","escudoUrl":"https://escudosfc.com.br/images/riobranco_ac.jpg"},{"nome":"São Raimundo ","escudoUrl":"https://escudosfc.com.br/images/saoraimundo_rr.jpg"},{"nome":"Trem","escudoUrl":"https://escudosfc.com.br/images/trem_ap.jpg"},{"nome":"Águia Marabá ","escudoUrl":"https://escudosfc.com.br/images/aguia_pa.png"},{"nome":"Altos","escudoUrl":"https://escudosfc.com.br/images/altos_pi.png"},{"nome":"Cametá","escudoUrl":"https://escudosfc.com.br/images/cameta_pa.png"},{"nome":"Fluminense","escudoUrl":"https://escudosfc.com.br/images/fluminense_pi.png"},{"nome":"Maranhão","escudoUrl":"https://escudosfc.com.br/images/maranhao.png"},{"nome":"Moto Club-MA","escudoUrl":"https://escudosfc.com.br/images/moto.jpg"},{"nome":"River","escudoUrl":"https://escudosfc.com.br/images/river_pi.png"},{"nome":"Tocantinópolis","escudoUrl":"https://escudosfc.com.br/images/tocantinopolis.png"},{"nome":"America","escudoUrl":"https://escudosfc.com.br/images/america.png"},{"nome":"Atlético Cearense","escudoUrl":"https://escudosfc.com.br/images/uniclinic.jpg"},{"nome":"Iguatu","escudoUrl":"https://escudosfc.com.br/images/iguatu_ce.png"},{"nome":"Maracanã","escudoUrl":"https://escudosfc.com.br/images/maracanau.png"},{"nome":"Potiguar","escudoUrl":"https://escudosfc.com.br/images/potiguar_rn.png"},{"nome":"Santa Cruz ","escudoUrl":"https://escudosfc.com.br/images/santa_cruz_natal_rn.png"},{"nome":"Sousa","escudoUrl":"https://escudosfc.com.br/images/sousa_pb3.png"},{"nome":"Treze","escudoUrl":"https://escudosfc.com.br/images/treze.jpg"},{"nome":"ASA","escudoUrl":"https://escudosfc.com.br/images/asa_al.png"},{"nome":"CSE","escudoUrl":"https://escudosfc.com.br/images/cse_al.png"},{"nome":"Itabaiana","escudoUrl":"https://escudosfc.com.br/images/itabaiana.gif"},{"nome":"Jacuipense","escudoUrl":"https://escudosfc.com.br/images/jacuipense_ba.jpg"},{"nome":"Juazeirense","escudoUrl":"https://escudosfc.com.br/images/juazeirense_ba.png"},{"nome":"Petrolina","escudoUrl":"https://escudosfc.com.br/images/petrolina.png"},{"nome":"Retrô","escudoUrl":"https://escudosfc.com.br/images/retro_pe.png"},{"nome":"Sergipe","escudoUrl":"https://escudosfc.com.br/images/sergipe.png"},{"nome":"Anápolis","escudoUrl":"https://escudosfc.com.br/images/anapolis.png"},{"nome":"Brasiliense","escudoUrl":"https://escudosfc.com.br/images/brasiliense.png"},{"nome":"Capital","escudoUrl":"https://escudosfc.com.br/images/capital_to.png"},{"nome":"CRAC","escudoUrl":"https://escudosfc.com.br/images/crac_go.png"},{"nome":"Iporá","escudoUrl":"https://escudosfc.com.br/images/ipora_go.png"},{"nome":"Mixto","escudoUrl":"https://escudosfc.com.br/images/mixto.gif"},{"nome":"Real Brasília","escudoUrl":"https://escudosfc.com.br/images/real_df.png"},{"nome":"União Rondonópolis","escudoUrl":"https://escudosfc.com.br/images/rondonopolis.jpg"},{"nome":"Audax","escudoUrl":"https://escudosfc.com.br/images/audax_rj.png"},{"nome":"Democrata","escudoUrl":"https://escudosfc.com.br/images/democrata_sl.png"},{"nome":"Ipatinga","escudoUrl":"https://escudosfc.com.br/images/ipatinga.gif"},{"nome":"Itabuna","escudoUrl":"https://escudosfc.com.br/images/itabuna.png"},{"nome":"Nova Iguaçu ","escudoUrl":"https://escudosfc.com.br/images/novaiguacu_rj.jpg"},{"nome":"Portuguesa","escudoUrl":"https://escudosfc.com.br/images/portuguesa_rj.png"},{"nome":"Real Noroeste","escudoUrl":"https://escudosfc.com.br/images/real_noroeste_es.png"},{"nome":"Serra","escudoUrl":"https://escudosfc.com.br/images/serra.png"},{"nome":"Água Santa","escudoUrl":"https://escudosfc.com.br/images/agua_santa_sp.png"},{"nome":"Costa Rica","escudoUrl":"https://escudosfc.com.br/images/costa_rica_rs.gif"},{"nome":"Internacional Limeira","escudoUrl":"https://escudosfc.com.br/images/intl.png"},{"nome":"Maringá","escudoUrl":"https://escudosfc.com.br/images/gremio_maringa.png"},{"nome":"Patrocinense","escudoUrl":"https://escudosfc.com.br/images/patrocinensenovo_mg.png"},{"nome":"Pouso Alegre","escudoUrl":"https://escudosfc.com.br/images/pouso_alegre_mg.png"},{"nome":"Santo André","escudoUrl":"https://escudosfc.com.br/images/santo_andre.png"},{"nome":"São José","escudoUrl":"https://escudosfc.com.br/images/sao_jose.png"},{"nome":"Avenida","escudoUrl":"https://escudosfc.com.br/images/avenida_rs.png"},{"nome":"Barra","escudoUrl":"https://escudosfc.com.br/images/barra_sc.png"},{"nome":"Brasil-RS","escudoUrl":"https://escudosfc.com.br/images/gebrasil.gif"},{"nome":"Cascavel","escudoUrl":"https://escudosfc.com.br/images/fc_cascavel_pr.png"},{"nome":"Cianorte","escudoUrl":"https://escudosfc.com.br/images/cianorte.jpg"},{"nome":"Concórdia","escudoUrl":"https://escudosfc.com.br/images/concordia_atletico_clube_sc.jpg"},{"nome":"Hercílio Luz","escudoUrl":"https://escudosfc.com.br/images/hercilio_luz_sc.png"},{"nome":"Novo Hamburgo","escudoUrl":"https://escudosfc.com.br/images/novohamburgo.png"}]

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

@app.get("/times")
async def get_times():
    return dados_times