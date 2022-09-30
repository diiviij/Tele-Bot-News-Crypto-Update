import os
import time
import telebot
from telebot import types
from tracker import get_prices
from pytube import YouTube


#from pytube import YouTube


my_secret = os.environ['Token']

TOKEN = my_secret
knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'crypto'       : 'Gives you Information about the Top Crypto \n',
    'help'        : 'Gives you information about the available commands \n',
    'NIMCET'      : 'Free NIMCET study Material  \n',
    '/type bye '  : 'To End the Chat '
    #'/Type yt-download' : 'To Download YT Videos for Free \n'
    
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('Previous Year paper', 'English','Computer','Reasoning')

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        #bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid,"Please use /NIMCET command & PDF will take time to load so be Calm")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        bot.send_message(cid, "Please click /help to know the commands")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['NIMCET'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your option now", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/NIMCET" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == 'Previous Year paper':  # send the appropriate image based on the reply to the "/getImage" command
      
        bot.send_document(cid, open('MATHS/2010.pdf', 'rb'))  
          
        bot.send_document(cid, open('MATHS/2013.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/2015.pdf', 'rb')) 
        bot.send_document(cid, open('MATHS/2016.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/2017.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/2018.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/DPP_Maths.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/DU_MCA.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/JNU_MCA.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/JNU_MCA_Answers.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/MCA_Apsirants.pdf', 'rb'))  
        bot.send_document(cid, open('MATHS/nimcet_2019_question_paper_with_answer_key.pdf', 'rb'))  
        bot.send_message(cid, "Use /help to go back to menu")
        userStep[cid] = 0  # reset the users step back to 0

    elif text =='English':

        bot.send_document(cid, open('english/HighSchool.pdf', 'rb'))
        bot.send_message(cid,"Use /NIMCET to go back to menu")
        userStep[cid] = 0

    elif text == 'Computer':
        bot.send_document(cid, open('computer/Logic Gates.pdf', 'rb'))
        bot.send_document(cid, open('computer/Kmap.pdf', 'rb'))
        bot.send_document(cid, open('computer/Computer Awareness.pdf', 'rb'))
        bot.send_document(cid, open('computer/BooleanAlgebra.pdf', 'rb'))
        bot.send_message(cid,"Use /NIMCET to go back to menu ")

        userStep[cid] = 0 
    
    elif text == 'Reasoning':
        bot.send_message(cid,"Coming Soon \n Use /NIMCET to go back to menu")
        userStep[cid] = 0 
    

    else:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")

@bot.message_handler(func=lambda message: message.text.lower() == "bye")
def command_text_byee(m):
    bot.send_message(m.chat.id, "Bye Have a Great Future !!")


@bot.message_handler(commands=['crypto'])
def crypto_price(m):
    cid = m.chat.id
    message=""
    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"
        
    bot.send_message(cid, message)



@bot.message_handler(func=lambda message: message.text.lower() == "btc")
def btc_price(m):
      cid = m.chat.id
      btcpr2 = get_prices()
      for i in btcpr2:
        coin = btcpr2[i]["coin"]
        price = btcpr2[i]["price"]
        change_day = btcpr2[i]["change_day"]
        change_hour = btcpr2[i]["change_hour"]
        message = f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: #{change_day:.3f}%\n\n"
        
        if coin == 'BTC':
              break

      bot.send_message(cid, message)

@bot.message_handler(func=lambda message: message.text.lower() == "wrx")
def btc_price(m):
      cid = m.chat.id
      btcpr2 = get_prices()
      for i in btcpr2:
        coin = btcpr2[i]["coin"]
        price = btcpr2[i]["price"]
        change_day = btcpr2[i]["change_day"]
        change_hour = btcpr2[i]["change_hour"]
        message = f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: #{change_day:.3f}%\n\n"
        
        if coin == 'WRX':
              break

      bot.send_message(cid, message)
@bot.message_handler(func=lambda message: message.text.lower() == "bnb")
def btc_price(m):
      cid = m.chat.id
      btcpr2 = get_prices()
      for i in btcpr2:
        coin = btcpr2[i]["coin"]
        price = btcpr2[i]["price"]
        change_day = btcpr2[i]["change_day"]
        change_hour = btcpr2[i]["change_hour"]
        message = f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: #{change_day:.3f}%\n\n"
        
        if coin == 'BNB':
              break

      bot.send_message(cid, message)

@bot.message_handler(func=lambda message: message.text.lower() == "group")
def btc_price(m):
      cid = m.chat.id
      bot.send_message(cid, "t.me/nimcet_mca_2022")

@bot.message_handler(func=lambda message: message.text.lower() == "invites")
def links(m):
      cid = m.chat.id
      bot.send_message(cid, "t.me/supernimcetgroup")





@bot.message_handler(func=lambda message: message.text.lower() == "yt")
def command_help(m):
    cid = m.chat.id
    bot.send_message(m.chat.id,"Please send the Url of the video")
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def ytube_download(m):
        bot.send_message(m.chat.id, "Please Wait,Video on the way")
        link = m.text
        yt = YouTube(link)
        print("Title: ",yt.title)
        yt.streams.first().download()
        os.rename(yt.streams.first().default_filename, 'download.mp4')
        bot.send_message(m.chat.id, "Video on the way")
        bot.send_document(cid, open('download.mp4', 'rb'))

    bot.send_message(cid, m.text)







@bot.message_handler(func=lambda message: message.text.lower() == "ok")
def bye_message(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "Bye Have a Gret Day !")
  

  
bot.set_update_listener(listener)
bot.infinity_polling()