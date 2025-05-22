from classes.environment import ENV
import gspread
from typing import Dict
import pandas as pd

class Sheets:
    creds = ENV.sheets["token"]
    sheets = ENV.sheets["sheets"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    def __init__(self):
        self.gc = gc = gspread.oauth_from_dict(
            {"installed": Sheets.creds}, scopes=Sheets.scopes)
        self.client = gc[0]
        self.spreadsheets: Dict[str: gspread.spreadsheet.Spreadsheet] = {}

    def get_spreadsheet(self, sheet: str):
        try:
            sheet_obj = self.client.open_by_url(Sheets.sheets[sheet])
        except Exception:
            return None

        self.spreadsheets[sheet] = sheet_obj
        return sheet_obj

    def get_sheet_from_spreadsheet(self, spreadsheet: str, worksheet_index: int, convert_to_pandas=True):
        spread_sheet = self.spreadsheets.get(spreadsheet, None)
        if not spread_sheet:
            spread_sheet = self.get_spreadsheet(spreadsheet)
            if not spread_sheet:
                print(f"spread sheet: {spreadsheet}, Not found")
                return None
        try:
            worksheet = spread_sheet.get_worksheet(worksheet_index)
        except Exception:
            print(f"could not get worksheet index {worksheet_index} from spreadsheet {spreadsheet}")
            return None

        if not convert_to_pandas:
            return worksheet

        try:
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)
            return df
        except Exception:
            print("unable to convert worksheet to dataframe. Returning worksheet object instead")
            return worksheet
