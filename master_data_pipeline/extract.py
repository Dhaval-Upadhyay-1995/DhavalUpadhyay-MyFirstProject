import requests 

def extract_data():
    url= "https://restcountries.com/v3.1/all"
    response=requests.get(url)
    if response.status_code==200:
        print("Extraction is successful")
        return response.json()
    else:
        raise Exception( f"API Call Failed: {response.status_code}")
    
l=extract_data()
print(len(l))

# print(extract_data)
    
# df=pd.read_json(extract_data())
# print(df.head())