import os
import json
import requests
from bs4 import BeautifulSoup

# Direct target URL
TARGET_URL = "https://anime3rb.com/"

def scrape_anime():
    filename = "movies.json"
    
    # Real browser headers to bypass basic server filters
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0"
    }
    
    try:
        print("⚡ Connecting directly to Anime3rb...")
        response = requests.get(TARGET_URL, headers=headers, timeout=20)
        
        if response.status_code != 200:
            raise Exception(f"Website returned status code: {response.status_code}")
            
        soup = BeautifulSoup(response.content, "html.parser")
        anime_list = []
        
        # Comprehensive search for anime entries based on Anime3rb's actual architecture
        # It looks for cards, latest episodes, and anchor tags containing links
        div_blocks = soup.find_all('div', class_='anime-card') or \
                     soup.find_all('div', class_='latest-episode-card') or \
                     soup.find_all('div', class_='card') or \
                     soup.find_all('div', class_='col-12')
                     
        for block in div_blocks:
            title_element = block.find('h3') or block.find('h2') or block.find('h5') or block.find('span', class_='title')
            link_element = block if block.name == 'a' else block.find('a')
            img_element = block.find('img')
            
            if title_element and link_element:
                link = link_element.get('href', '').strip()
                title = title_element.text.strip()
                image = img_element.get('src', '').strip() if img_element else ""
                
                # Auto-repair relative URLs
                if link.startswith('/'):
                    link = f"https://anime3rb.com{link}"
                    
                if title and link and link != "https://anime3rb.com/":
                    if not any(item['link'] == link for item in anime_list):
                        anime_list.append({
                            "title": title,
                            "link": link,
                            "image": image
                        })
        
        if not anime_list:
            raise Exception("Scraper connected successfully but failed to parse HTML structure. The tags might be different.")
                
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(anime_list, f, ensure_ascii=False, indent=4)
        print(f"🎉 Success! Beautifully extracted {len(anime_list)} items directly.")
        
    except Exception as e:
        print(f"Crucial Error during scraping: {str(e)}")
        raise e

if __name__ == "__main__":
    scrape_anime()
