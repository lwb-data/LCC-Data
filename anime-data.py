import os
import json
import requests
from bs4 import BeautifulSoup

# Switching target to Anime3rb
TARGET_URL = "https://anime3rb.com/"
# Your ScrapingAnt API key
SCRAPEANT_API_KEY = "2632547b8ac743e2a892a7f1aa7d311a"

def scrape_anime():
    filename = "movies.json"
    api_url = "https://api.scrapingant.com/v1/general"
    
    # Advanced rendering options to guarantee zero blocks on the new site
    params = {
        "url": TARGET_URL,
        "x-api-key": SCRAPEANT_API_KEY,
        "browser": "true",          
        "proxy_type": "residential", 
        "proxy_country": "ae"        
    }
    
    try:
        print("⚡ Connecting to Anime3rb via secure residential proxy...")
        response = requests.get(api_url, params=params, timeout=45)
        
        if response.status_code != 200:
            raise Exception(f"ScrapingAnt Proxy returned status code: {response.status_code}. Detail: {response.text}")
            
        soup = BeautifulSoup(response.content, "html.parser")
        anime_list = []
        
        # Mapping Anime3rb card structures for latest episodes and updates
        div_blocks = soup.find_all('div', class_='anime-card') or \
                     soup.find_all('div', class_='latest-episode-card') or \
                     soup.find_all('div', class_='card') or \
                     soup.find_all('a', class_='anime-popup')
                     
        for block in div_blocks:
            # Checking different possible tag positions on Anime3rb layout
            title_element = block.find('h3') or block.find('h2') or block.find('span', class_='title') or block.find('div', class_='title')
            link_element = block if block.name == 'a' else block.find('a')
            img_element = block.find('img')
            
            if title_element and link_element:
                link = link_element.get('href', '').strip()
                title = title_element.text.strip()
                image = img_element.get('src', '').strip() if img_element else ""
                
                # Auto repair links if they are relative paths (e.g., /titles/naruto)
                if link.startswith('/'):
                    link = f"https://anime3rb.com{link}"
                    
                if title and link and link != "https://anime3rb.com/":
                    # Prevent duplicates in the list
                    if not any(item['link'] == link for item in anime_list):
                        anime_list.append({
                            "title": title,
                            "link": link,
                            "image": image
                        })
        
        if not anime_list:
            raise Exception("Scraper completed but zero items were found on Anime3rb. Retrying might be needed.")
                
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(anime_list, f, ensure_ascii=False, indent=4)
        print(f"🎉 Success! Beautifully scraped {len(anime_list)} items from Anime3rb.")
        
    except Exception as e:
        print(f"Crucial Error during scraping: {str(e)}")
        raise e

if __name__ == "__main__":
    scrape_anime()
