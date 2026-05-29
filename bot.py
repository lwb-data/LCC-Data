import telebot
import requests

TOKEN = "8859232723:AAE7Y4mNxn0Mq2tnaCQZmDdBQcknXNy-zSI"
JSON_RAW_URL = "https://raw.githubusercontent.com/lwb-data/LCC-Data/main/movies.json"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'fetch', 'help'])
def get_anime_list(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = requests.get(JSON_RAW_URL, timeout=10)
        
        if response.status_code == 200:
            anime_data = response.json()
            if not anime_data:
                bot.reply_to(message, "Welcome! No new anime updates available right now.")
                return
            
            text_response = "Welcome! Here are the Latest Anime Updates 🎬:\n\n"
            for index, anime in enumerate(anime_data[:10], 1):
                title = anime.get('title', 'No Title')
                link = anime.get('link', '#')
                text_response += f"{index}. {title}\n🔗 Link: {link}\n\n"
            
            bot.reply_to(message, text_response)
        else:
            bot.reply_to(message, f"Welcome! Failed to fetch data. Error code: {response.status_code}")
            
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
