import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_data(opt_value):
    """
    Função para extrair dados da tabela da página da Embrapa usando Requests e BeautifulSoup.
    """
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={opt_value}"

    try:
        logger.info(f"Fazendo requisição para a URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Garante que erros de HTTP sejam levantados

        soup = BeautifulSoup(response.content, "html.parser")

        # Encontrar a tabela com a classe "tb_base tb_dados"
        table = soup.find("table", class_="tb_base tb_dados")
        if not table:
            raise RuntimeError("Tabela não encontrada na página.")

        data = []
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            row_data = [col.get_text(strip=True) for col in cols]
            if row_data:
                data.append(row_data)

        logger.info(f"Total de linhas extraídas: {len(data)}")
        return data

    except Exception as e:
        logger.error(f"Erro ao extrair dados: {str(e)}")
        raise RuntimeError("Falha ao extrair dados da página Embrapa.")
