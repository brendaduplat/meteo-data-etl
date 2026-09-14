import requests
import json
from pathlib import Path
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url: str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as erro:
        logging.error(f"Erro {erro} na requisição")
        raise

    output_path = "data/weather_data.json"
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info("Arquivo salvo com sucesso.")
    return data