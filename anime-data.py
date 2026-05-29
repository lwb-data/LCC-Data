import os
import json
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://w1.anime4up.rest/home8/"

def scrape_anime():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
    }
    filename = "movies.json"
    
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        
        if response.status_code != 200:
            raise Exception(f"Target website returned status code: {response.status_code}")
            
        soup = BeautifulSoup(response.content, "html.parser")
        anime_list = []
        
        div_blocks = soup.find_all('div', class_='anime-card-container') or \
                     soup.find_all('div', class_='col-md-2') or \
                     soup.find_all('div', class_='anime-card')
        
        for block in div_blocks:
            title_element = block.find('h3') or block.find('a') or block.find('div', class_='anime-card-title')
            link_element = block.find('a')
            img_element = block.find('img')
            
            if title_element and link_element:
                link = link_element.get('href', '').strip()
                title = title_element.text.strip()
                image = img_element.get('src', '').strip() if img_element else ""
                
                if title and link:
                    anime_list.append({
                        "title": title,
                        "link": link,
                        "image": image
                    })
        
        if not anime_list:
            raise Exception("Scraper finished but zero items were found. HTML structure might have changed!")
                
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(anime_list, f, ensure_ascii=False, indent=4)
        print(f"Success: Scraped {len(anime_list)} items.")
        
    except Exception as e:
        print(f"Crucial Error during scraping: {str(e)}")
        raise e

if __name__ == "__main__":
    scrape_anime()
