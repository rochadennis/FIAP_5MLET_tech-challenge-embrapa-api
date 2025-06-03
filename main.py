from fastapi import FastAPI, HTTPException
from scraper import scrape_data
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tech Challenge - Vitivinicultura Embrapa API",
    version="1.0.0",
    description="API para consumo de dados da Embrapa"
)

def handle_scraping_endpoint(opt_value: str):
    """
    Função genérica para chamar o scraper com tratamento de exceções.
    """
    try:
        data = scrape_data(opt_value)
        return {"dados": data}
    except RuntimeError as e:
        logger.error(f"Erro de scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Erro inesperado.")
        raise HTTPException(status_code=500, detail="Erro inesperado no servidor.")

@app.get("/")
async def home():
    return {"mensagem": "API para consumo de dados da Embrapa!"}

@app.get("/producao", tags=["Produção"])
def get_producao():
    return handle_scraping_endpoint("opt_02")

@app.get("/processamento", tags=["Processamento"])
def get_processamento():
    return handle_scraping_endpoint("opt_03")

@app.get("/comercializacao", tags=["Comercialização"])
def get_comercializacao():
    return handle_scraping_endpoint("opt_04")

@app.get("/importacao", tags=["Importação"])
def get_importacao():
    return handle_scraping_endpoint("opt_05")

@app.get("/exportacao", tags=["Exportação"])
def get_exportacao():
    return handle_scraping_endpoint("opt_06")
