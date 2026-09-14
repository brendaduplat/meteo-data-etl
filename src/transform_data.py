import pandas as pd
import json 
from pathlib import Path 
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / "data" / "weather_data.json"
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds",                  
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_df(path_name: Path) -> pd.DataFrame:
    logging.info("Criando o DataFrame..")
    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    
    with open(path, "r") as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info("\n DataFrame criado com %s linha(s).", len(df))
    return df

def normalize_weather_data(df: pd.DataFrame) -> pd.DataFrame:

    df_weather = pd.json_normalize(df["weather"].apply(lambda x: x[0]))
    df_weather = df_weather.rename(columns={col: f"weather_{col}" for col in df_weather.columns})

    df = pd.concat([df, df_weather], axis=1)
    logging.info("\n Coluna 'weather' normalizada - %s colunas", len(df.columns))
    return df

def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info("\n→ Removendo colunas: %s", columns_name)
    df = df.drop(columns=columns_name, errors="ignore")
    return df

def rename_columns(df: pd.DataFrame, columns_name: dict[str, str]) -> pd.DataFrame:
    logging.info("\n→ Renomeando %s colunas...", len(columns_name))
    df = df.rename(columns=columns_name)
    logging.info("✓ Colunas renomeadas")
    return df

def normalize_datetime(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info("\n→ Convertendo colunas para datetime: %s", columns_name)
    for name in columns_name:
        df[name] = pd.to_datetime(df[name], unit="s", utc=True).dt.tz_convert("America/Sao_Paulo")
    logging.info("✓ Colunas convertidas para datetime\n") 
    return df 

def all_data_transformations():
    logging.info("\n Iniciando transformações..")
    df = create_df(path_name)
    df = normalize_weather_data(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime(df, columns_to_normalize_datetime)
    logging.info("Transformações concluídas\n")
    return df