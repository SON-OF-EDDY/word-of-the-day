import telebot
from telebot import formatting
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import pytz

################################################################################################################
##TELEGRAM STUFF
API_KEY = '6704201341:AAH2mHL9u_gvsCU0CWfkahmu8771KQwRXkI'
CHAT_ID = '-1001702148514'
#CHAT_ID = '5289262606'
bot = telebot.TeleBot(API_KEY)
################################################################################################################
def escape_special_characters(input_text):
    special_characters = ['_', '[', ']', '(', ')', '~', '`', '>',
'#', '+', '-', '=', '|', '{', '}', '.', '!' ]
    for char in special_characters:
        input_text = input_text.replace(char, f'\\{char}')
    return input_text


def find_synoymns(word_to_find):

    array_of_synoymns = []

    try:
        url = f"https://www.thesaurus.com/browse/{word_to_find}"

        response = requests.get(url=url)

        soup = BeautifulSoup(response.text, 'html.parser')

        actual_synoymns_box = soup.find(class_="LhpJmDktqk95S2vWg1JZ")

        get_list_elements = soup.find_all('a', class_='KmScG4NplKj_3H5E3oA_')

        for element in get_list_elements:
            array_of_synoymns.append(element.text)

        return array_of_synoymns

    except:
        pass
    return array_of_synoymns

def send_scheduled_message():

    important_info = word_scrape()

    actual_word = important_info[0]
    definition = important_info[1][0]
    definition_audio = generate_audio(definition, actual_word)
    example_one = important_info[1][1]
    example_two = important_info[1][2]
    did_you_know_section = important_info[2]
    synonyms_list = find_synoymns(actual_word)
    try:
        synonyms_long_string = ", ".join(synonyms_list)
    except:
        synonyms_long_string = 'None found'

    bold_part = formatting.mbold("Word of the Day")
    regular_part = f"{actual_word}"
    mixed_text = bold_part + ": " + regular_part

    # Send message without using message variable
    bot.send_message(chat_id=CHAT_ID,
                     text=f'''
    {escape_special_characters(mixed_text)}
    ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Definition")
    regular_part = f"{definition}"
    mixed_text = bold_part + ": " + regular_part

    # Send message without using message variable
    bot.send_message(chat_id=CHAT_ID,
                     text=f'''
    {escape_special_characters(mixed_text)}
        ''', parse_mode='MarkdownV2')

    script_dir = os.path.dirname(__file__)

    # Replace 'example.mp3' with the actual name of your audio file
    audio_filename = 'word_of_the_day.mp3'

    # Construct the full path to the audio file
    audio_path = os.path.join(script_dir, audio_filename)

    audio = open(audio_path, 'rb')

    # Send audio without using message variable
    bot.send_audio(chat_id=CHAT_ID, audio=audio)

    audio.close()

    bold_part = formatting.mbold("Synonymns")
    regular_part = f"{synonyms_long_string}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(chat_id=CHAT_ID,text=
                     f'''
        {escape_special_characters(mixed_text)}
        ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Example One")
    regular_part = f"{example_one}"
    mixed_text = bold_part + ": " + regular_part

    # Send message without using message variable
    bot.send_message(chat_id=CHAT_ID,
                     text=f'''
    {escape_special_characters(mixed_text)}
        ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Example Two")
    regular_part = f"{example_two}"
    mixed_text = bold_part + ": " + regular_part

    # Send message without using message variable
    bot.send_message(chat_id=CHAT_ID,
                     text=f'''
    {escape_special_characters(mixed_text)}
        ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Did you know?")
    regular_part = f"{did_you_know_section}"
    mixed_text = bold_part + ": " + regular_part

    # Send message without using message variable
    bot.send_message(chat_id=CHAT_ID,
                     text=f'''
    {escape_special_characters(mixed_text)}
        ''', parse_mode='MarkdownV2')

@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):

    # SCHEDULER SECTION
    scheduler = BackgroundScheduler()

    # Set the start time for 21:50 Moscow time
    start_time = datetime.now(pytz.timezone('Europe/Moscow'))
    start_time = start_time.replace(hour=12, minute=0, second=0, microsecond=0)

    # Set the interval to 24 hours
    interval = 24


    trigger = IntervalTrigger(hours=interval, start_date=start_time, timezone=pytz.timezone('Europe/Moscow'))
    scheduler.add_job(send_scheduled_message, trigger=trigger)
    scheduler.start()

    # KEYBOARD MARKUP/BUTTONS SECTION
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
    definition = important_info[1][0]
    definition_audio = generate_audio(definition,actual_word)
    example_one = important_info[1][1]
    example_two = important_info[1][2]
    did_you_know_section = important_info[2]
    synonyms_list = find_synoymns(actual_word)
    try:
        synonyms_long_string = ", ".join(synonyms_list)
    except:
        synonyms_long_string = 'None found'

    bold_part = formatting.mbold("Word of the Day")
    regular_part = f"{actual_word}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(message.chat.id,
               f'''
{escape_special_characters(mixed_text)}
''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Definition")
    regular_part = f"{definition}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(message.chat.id,
                     f'''
{escape_special_characters(mixed_text)}
    ''', parse_mode='MarkdownV2')

    script_dir = os.path.dirname(__file__)

    # Replace 'example.mp3' with the actual name of your audio file
    audio_filename = 'word_of_the_day.mp3'

    # Construct the full path to the audio file
    audio_path = os.path.join(script_dir, audio_filename)
    audio = open(audio_path, 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()

    bold_part = formatting.mbold("Synonymns")
    regular_part = f"{synonyms_long_string}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(message.chat.id,
                     f'''
    {escape_special_characters(mixed_text)}
    ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Example One")
    regular_part = f"{example_one}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(message.chat.id,
                     f'''
{escape_special_characters(mixed_text)}
    ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Example Two")
    regular_part = f"{example_two}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(message.chat.id,
                     f'''
{escape_special_characters(mixed_text)}
    ''', parse_mode='MarkdownV2')

    bold_part = formatting.mbold("Did you know?")
    regular_part = f"{did_you_know_section}"
    mixed_text = bold_part + ": " + regular_part
    bot.send_message(message.chat.id,
                     f'''
{escape_special_characters(mixed_text)}
    ''', parse_mode='MarkdownV2')

def generate_audio(input_text,word_of_the_day):
    audio = gTTS(text=input_text, lang="en", slow=False)
    audio.save("word_of_the_day.mp3")

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