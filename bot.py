import telebot
from telebot.types import Message,ReplyKeyboardMarkup, KeyboardButton
import requests
from bs4 import BeautifulSoup
#######################################################################
# TELEGRAM STUFF
API_KEY = '6704201341:AAH2mHL9u_gvsCU0CWfkahmu8771KQwRXkI'
bot = telebot.TeleBot(API_KEY)

##################################################################################################################
@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):

    markup_reply = ReplyKeyboardMarkup(resize_keyboard=True)

    word_of_the_day_button = KeyboardButton(text='Word of the Day!')

    row1 = [word_of_the_day_button]

    markup_reply.add(*row1)

    msg = bot.send_message(message.chat.id,
                           "Improve your English with a random interesting word each day!",
                           reply_markup=markup_reply
                           )

@bot.message_handler(content_types=['text'])
def handle_start_response(message):

    important_info = word_scrape()

    actual_word = important_info[0]
    defintion = important_info[1][0]
    example_one = important_info[1][1]
    example_two = important_info[1][2]
    did_you_know_section = important_info[2]

    bot.send_message(message.chat.id,
               f'''
Word of the Day: {actual_word}

Definition: {defintion}

Example One: {example_one}

Example Two: {example_two}

Did you know?: {did_you_know_section}
''')


def word_scrape():

    output = ['Null','Null','Null']

    try:
        url = f"https://www.merriam-webster.com/word-of-the-day"

        response = requests.get(url=url)

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with class "<h2 class="word-header-txt">glower</h2>"
        actual_word = soup.find(class_="word-header-txt").text

        wod_definition_div = soup.find('div', class_='wod-definition-container')

        all_p_tags = wod_definition_div.find_all('p')

        meaning_and_examples = [all_p_tags[0].text,all_p_tags[1].text,all_p_tags[3].text]

        did_you_know_section = soup.find(class_="did-you-know-wrapper")

        did_you_know_section_content = did_you_know_section.find('p').text

        output = [actual_word,meaning_and_examples,did_you_know_section_content]

    except:
        pass
    return output

bot.polling()



