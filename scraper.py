from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

def scrape_data(opt_value):
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    options = Options()
    options.add_argument("--headless")
    # Executa em modo headless (sem abrir janela do navegador)

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        logger.info(f"Acessando a URL: {url}")

        # Encontra o botão e clica na aba correspondente
        btn = driver.find_element(By.XPATH, f"//button[@value='{opt_value}']")
        logger.info(f"Clicando na aba com value='{opt_value}'")
        btn.click()
        
        # Espera o carregamento da tabela
        wait = WebDriverWait(driver, 10)
        #Localizar a tabela com os dados para extração
        table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'tb_base tb_dados')]")))
        logger.info("Tabela encontrada, extraindo dados...")

        data = []
        # Extrai dados da tabela
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text.strip() for col in cols]
            if row_data:
                data.append(row_data)

        return data

    except Exception as e:
        logger.error(f"Erro ao fazer scraping: {str(e)}")
        raise RuntimeError("Falha ao extrair dados da página Embrapa.")
    
    finally:
        if driver:
            driver.quit()
            logger.info("Navegador encerrado.")
