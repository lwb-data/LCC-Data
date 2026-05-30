import os
import json
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://w1.anime4up.rest/home8/"
# Your ScrapingAnt API key
SCRAPEANT_API_KEY = "2632547b8ac743e2a892a7f1aa7d311a"

def scrape_anime():
    filename = "movies.json"
    api_url = "https://api.scrapingant.com/v1/general"
    
    # Advanced parameters to bypass tough firewalls (Enabling Browser & Residential Proxy)
    params = {
        "url": TARGET_URL,
        "x-api-key": SCRAPEANT_API_KEY,
        "browser": "true",          # Runs a real hidden browser to bypass detection
        "proxy_type": "residential", # Uses a residential home IP instead of datacenter
        "proxy_country": "ae"        # Route through UAE proxy for better speed/access to Arabic content
    }
    
    try:
        response = requests.get(api_url, params=params, timeout=45)
        
        if response.status_code != 200:
            raise Exception(f"ScrapingAnt Proxy returned status code: {response.status_code}. Detail: {response.text}")
            
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
            raise Exception("Scraper completed but zero items were found. Structure might have changed.")
                
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(anime_list, f, ensure_ascii=False, indent=4)
        print(f"Success: Scraped {len(anime_list)} items via Advanced Residential Browser.")
        
    except Exception as e:
        print(f"Crucial Error during scraping: {str(e)}")
        raise e

if __name__ == "__main__":
    scrape_anime()
