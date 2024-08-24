import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def get_editions():
    editions_url = "https://www.olympedia.org/editions"

    try:
        response = requests.get(editions_url, timeout=60)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            dfs = []
            current_title = None
            current_subtitle = None

            for element in soup.find_all(["h2", "h3", "table"]):
                if element.name == "h2":
                    current_title = element.get_text(strip=True)
                elif element.name == "h3":
                    current_subtitle = element.get_text(strip=True)
                elif element.name == "table":
                    df = pd.read_html(StringIO(str(element)))[0]
                    df["title"] = current_title
                    df["subtitle"] = current_subtitle
                    dfs.append(df)

            editions = pd.concat(dfs)
        
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
    except Exception as e:
        print(e)

    editions.to_csv('datalake/bronze/editions.csv',index=False)


if __name__ == "__main__":
    get_editions()
