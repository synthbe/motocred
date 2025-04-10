from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

sheet_wallet = os.getenv("SHEET_WALLET") # Contains customer name and selling date and selling code as bmp op
sheet_selling = os.getenv("SHEET_SELLING") # Contains selling code and customer name
sheet_parcels = os.getenv("SHEET_PARCELS") # Contains selling code and parc deadline
