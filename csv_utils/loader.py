import pandas as pd

def load_csv_with_fallback(self, filepath):
     encodings = ["latin1", "utf-8", "utf-8-sig", "cp1252", "utf-16"]
     for enc in encodings:
         try:
             df = pd.read_csv(filepath, encoding=enc, on_bad_lines='skip')
             print(f"CSV loaded with encoding: {enc}")
             return df
         except Exception as e:
             print(f"Failed with encoding {enc}: {e}")
     raise ValueError("Failed to load CSV with known encodings.")