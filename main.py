import os
from dotenv import load_dotenv
import telebot
from GNews_API import gnews_api


load_dotenv()
API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(API_KEY)

VALID_COUNTRIES = {
    "ar", "au", "bd", "br", "ca", "cn", "co", "eg", "fr", "de",
    "gr", "hk", "in", "id", "ie", "il", "it", "jp", "my", "mx",
    "nl", "no", "pk", "pe", "ph", "pt", "ro", "ru", "sg", "es",
    "se", "ch", "tw", "tr", "ua", "gb", "us",'ge'
}
def loop(message,result):
    if not result:
        bot.send_message(message, "❌ No articles found matching your criteria.")
        return

    for r in result:
        title = r['title']
        desc = r['description']
        source = r['source']
        url = r['url']
        text = (
            f"📰 {title}\n\n"
            f"📄 {desc}\n\n"
            f"🏢 Source: {source}\n"
            f"🔗 {url} \n"
            f"                  READ MORE"
        )
        bot.send_message(message, text)

# Combined handler for start and help commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Hello! My name is NewsNova. 🤖\n"
        "I am your daily news bot.\n\n"
        "Please use one of the commands below to get the latest news:\n"
        "/general - Global general news\n"
        "/world - International updates\n"
        "/nation - National news\n"
        "/business - Financial and market updates\n"
        "/technology - Tech and gadget reviews\n"
        "/entertainment - Celebrity and movie news\n"
        "/sports - Match updates and scores\n"
        "/science - Space and research discoveries\n"
        "/health - Medical and wellness news"
    )
    bot.reply_to(message, welcome_text)


# Dedicated handler for specific news categories
@bot.message_handler(
    commands=["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"])
def get_news_category(message):
    # Extracts the exact command used (e.g., "sports")
    category = message.text.split()[0].replace('/', '')

    # Placeholder text for the API integration
    bot.reply_to(message, f"you have selected the {category.upper()} category")
    msg=bot.reply_to(message,"Would you like to search for a specific keyword?\n\
    Type YES or NO.")
    bot.register_next_step_handler(msg, ask_keyword,category)

def ask_keyword(message, category,):
    answer=message.text.strip().upper()
    if answer=="YES":
        msg=bot.reply_to(message,"Enter a keyword (example: football, crypto, F1)")
        #msg = bot.reply_to(message,'Enter the country you want to search:\n\nUnited States us\nChina cn\nGermany de\nJapan jp\nIndia in\nUnited Kingdom gb\nFrance fr\nItaly it\nBrazil br\nCanada ca\nRussia ru\nSpain es')
        bot.register_next_step_handler(msg, get_keyword,category)
    elif answer=="NO":
        bot.reply_to(message,f"Fetching the latest {category.upper()} news...")
        result = gnews_api(category)
        loop(message.chat.id, result)
    else:
        msg= bot.reply_to(message,"Please enter yes or no")
        bot.register_next_step_handler(msg, ask_keyword, category)

def get_keyword(message, category):
    keyword=message.text.strip().upper()
    msg = bot.reply_to(message,'Enter the country code you want to search:\n\nUnited States us\nChina cn\nGermany de\nJapan jp\nIndia in\nUnited Kingdom gb\nFrance fr\nItaly it\nBrazil br\nCanada ca\nRussia ru\nSpain es \n general ge')
    bot.register_next_step_handler(msg, get_country, category, keyword)

def get_country(message, category, keyword):
    country=message.text.strip().lower()
    if country == 'ge':
        bot.reply_to(message, f"Fetching the latest general country data")
        bot.reply_to(
            message,
            f"Searching {category.upper()} news for '{keyword}' in {country.upper()}..."
        )
        result = gnews_api(keyword, category, country)
        loop(message.chat.id, result)
    elif country in VALID_COUNTRIES:
        bot.reply_to(message,f"Fetching the latest {country.upper()} news...")
        result = gnews_api(keyword, category, country)
        loop(message.chat.id, result)

    else:
        msg = bot.reply_to(
            message,
            "❌ Invalid country code.\n\n"
            "Please enter a valid country code (e.g. us, gb, jp)."
        )

        bot.register_next_step_handler(msg, get_country, category, keyword)
        return
bot.infinity_polling()
