import pandas as pd
from extract import extract_data

def transform_data(data):
    transformed = []
    for country in data:
        transformed.append({"Name": country.get("name", {}).get("common"),
        "Capital": country.get("capital",[None])[0],
        "Region": country.get("region"),
        "Subregion": country.get("subregion")
        })

    return pd.DataFrame(transformed)

print(transform_data(extract_data()))