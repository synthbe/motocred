import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe
from google.cloud import storage
from datetime import timedelta
from typing import Any

def read_sheet(credentials: Any, sheet_url: str, page: str) -> pd.DataFrame:
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet(page)
    df = get_as_dataframe(worksheet, evaluate_formulas=True)

    return df

def read_audio_link(bucket_name: str, blob_name: str, expiration_minutes: int=10) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
        response_disposition="inline"  # for audio playback
    )

    return url
