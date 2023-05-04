import telebot
# Model Code
import random
import json

import torch

from model import NeuralNet
from custom_nltk_funcs import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "DumpData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Divy"
# This is Bot Code

TOKEN = '6114741193:AAGnO5oQnTrfl1PnrugmVMkqrrewq-xQG3g'

#Init the  bot with token
bot = telebot.TeleBot(TOKEN)

#To catch the message you need to use this decorator. 
@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, """\n 'You will be Blessed when you come in and blessed when you go out ....DEU 28:6' \n \n\n Welcome to Diviseema Polytechnic College \n\n Hi {}""".format(message.chat.username))
    
@bot.message_handler(commands=['about','About','ABOUT'])
def send_hello(message):
    bot.reply_to(message, """-------❓ About us -----------/nA second home where every student looks forward to finding his or her own Identity is A College Campus. Diviseema Polytechnic is approved by AICTE. College is affording an abundant supply of resources, facilities, and significantly, opportunities for its students to identify themselves.

Diviseema Polytechnic is located in Ramachandrapuram, which is just 35 km from machilipatnam, it presents a scholastic and pollution-free atmosphere surrounded by trees and more greenery land and impressive infrastructure embraces the campus of Diviseema Polytechnic.

The campus is very well equipped with all the facilities, which are the major requirements of any student like a cafeteria and hostel, state-of-the-art laboratories, and seminar halls. Over square feet of instructional space with spacious classrooms, well-equipped laboratories, a Library and Computer Center, and much more are accommodated at the campus.

Diviseema Polytechnic is gaining more reputation because of its continuous efforts in improving the facilities and infrastructure, to reach every individual student to learn, invent, examine, and apply their knowledge. Apart from making the students learn from qualified and efficient staff, Students will also be blessed with an opportunity to express and explore their knowledge.""") 

@bot.message_handler(commands=['help','Help','HELP'])
def send_hello(message):
    bot.reply_to(message, """...............ℹ️ Help Dialog .....\n /help => for this message\n/latestnews => Updated News of College/n/features => features of Diviseema \n /contact => Contact Details \n  /principal => details of Principal \n /developers => Developer 's of Divipolybot  /chairman => chairman note and details of Chairman \n /hods => department heads \n """) 

@bot.message_handler(commands=['latestnews'])
def send_hello(message):
    bot.reply_to(message, """............📰 divi news .........\n[latest news] => Science fest on Feb 25-27 \n
    => Republic day on Jan 26 was built great cultural activities on that day\n\n
    => Sankranthi was one of the great festivals and very cultural to all the Indians, on that day they create our cultural activities like Rangoli, etc.,\n""") 

   
@bot.message_handler(commands=['contact'])
def send_hello(message):
    bot.send_message(message.chat.id, """........📞 contact us .........\noffice:9246451977(or) 8179311821\n Website : Diviseemapolytechinc.org \n Youtube : @diviseemapolytechnic""")
    
@bot.message_handler(commands=['courses'])
def send_hello(message):
    bot.reply_to(message, """..............Courses we offer ..............\n 1.Computer Science Engineering (/CME)\n
    2. Electronics Communication Engineering (/ECE)\n
    3. Electrical Electronics Engineering (/EEE)\n
    4. Mechanical Engineering (/DME)\n
    5. Civil Engineering (/DCE)\n
    6. Artificial Intelligence and Machine Learning \n
    7. Computer Science and Engg(ARTIFICIAL INTELLIGENCE)\n
    8. Communiction and Computer Networking\n""")

@bot.message_handler(commands=['ECE','ece','Ece'])
def send_msg(message):
    bot.send_message(message.chat.id,"""
    Department of Diploma in Electronics & Communication Engineering:
As Electronics and Communication Lab has below listed equipments for the students to have more exposure to the practical aspects of the subject:

➡️ Digital Electronics Lab.
➡️ Micro controller Lab.
➡️ Basic electronics Lab.
➡️ Analog Communication Lab.
➡️ Electronic Measurement Lab.
➡️ Power Electronic Lab (Common).
The intension for setting up the department for Electronics and Communication Engineering was to transform students into industry specific professionals. The option of attending training sessions and seminars conducted by experts of the related industries would be other added advantage that the ECE wing provides to the students. The department allows students to do research and is accomplished by understanding it through various lab sessions being held under the supervision of experienced lab assistants helping them to gain more exposure on the subject.""")

@bot.message_handler(commands=['CME','cme','Cme'])
def send_msg(message):
    bot.send_message(message.chat.id,"""Department of Diploma in Computer Engineering:
The Computer department has latest versions of the computers and software along with user friendly accessories. As count of the students for the course are more in number, the management have setup two labs named "Computer Lab-I" and "Computer Lab-II" to make it more comfortable for practicing lab practical of the academics.

The main goal of the Computer department is to give more exposure on latest technology and software that are adopted by corporate companies. As the IT sector offers more jobs for computer graduates every year, the department wants to secure 100% placement by offering different training sessions on communication and soft skills along with technical aspects by hiring experts. The Computer Engineering wing has great track record for 100% placement and still maintains it. The year planner includes hosting different technology events and seminars for students to build leadership qualities and expose to newer things of the IT arena.""")

@bot.message_handler(commands=['EEE','eee','Eee'])
def send_msg(message):
    bot.send_message(message.chat.id,"""The department is well known for its equipments that are setup in the Lab and list of the same are mentioned below:

➡️ Electrical machines Lab.
➡️ Power Electronics Lab (Common).
➡️ Industrial Automation Lab.
➡️ Electrical Wiring Lab.
The main motto of the department is to achieve 100% placement for the students by organizing on job training sessions under the supervision of experts of the Industry. The state-of-art structure of the Electrical Lab is of top class, which enables to accommodate more students to have practical exposure under one roof. Apart from private jobs, the wing allows you to motivate to crack public sector jobs offered in the Electrical Engineering arena.""")

@bot.message_handler(commands=['DME','dme','Dme'])
def send_msg(message):
    bot.send_message(message.chat.id,"""
    Department of Diploma in Mechanical Engineering:
The management ensured to have well equipped Mechanical instruments for the lab to provide more practical exposure for the students of the college. The list of equipments includes:

➡️ Work Shop.
➡️ Foundry & forging Lab.
➡️ Welding Lab.
➡️ Machine Shop.
➡️ FM & Hydraulics Lab.
➡️ Servicing Maintenance Lab.
➡️ Material Testing Lab.
➡️ Heat Engines & R & A/C Lab.
➡️ Fuels Lab.
The aim of the Mechanical department is to meet the requirements of the students based on the needs. The other responsibilities of the wing are to organize different workshops and also conduct seminars by inviting experts of the industry to give more exposure to the students related to the platform. Apart from the technical aspects, they also provide training sessions on soft skills to ensure that students are groomed to have great qualities built in them that include quality, attitude, commitment and integrity.""")

@bot.message_handler(commands=['DCE','dce','Dce'])
def send_msg(message):
    bot.send_message(message.chat.id,"""
    Department of Diploma in Civil Engineering:
"Surveying Lab" is one of the well equipped instruments of the Civil Engineering Department of the college and are planning to come up few more in short period of time. As scope for Civil Engineers are increasing every year, the department gave the opportunity to students for knowing more about the subject through various seminars and workshops conducted by industry experts. The Civil Engineering wing also aimed to achieve 100% placement for each year and succeeded in doing that. Apart from opportunities, they also act a mentor for resolving the issues that students come across through their academics.

The department also provides field work training especially for Civil Engineers to gain exposure of the issues that they come across, which would certainly help students to work with ease once they are recruited in a company.""")


@bot.message_handler(commands=['hods','hod','Hod'])
def send_hello(message):
    bot.reply_to(message, """.......................\n 1. Mr . Ravi Teja(Btech)(Computer Science Engineering (/CME) \n
    2. Mrs . Vasanthi (Btech)(Electronics Communication Engineering)(/ECE)\n
    3. Mr . Ramana (Btech)(VicePrincipal)(Electrical Electronics Engineering (/EEE))\n
    4. Mr . Ravi Teja(btech)(Mechanical Engineering (/DME))\n
    5. Mr . Heeram Das (btech)(Civil Engineering )(/DCE)\n)
    6. Mrs . Kalpana (btech)(Artificial Intelligence and Machine Learning (/DCAIE))\n
    7. Mr . Ravi Teja (Btech)(Computer Science and Engg(ARTIFICIAL INTELLIGENCE)(DCAIE)\n
    8. Mrs . Sowmya (Btech)(Communiction and Computer Networking(/DCCN))\n""")

@bot.message_handler(commands=['developers'])
def send_hello(message):
    bot.reply_to(message, """1.Rohith Yarramala ('Team Lead')👨‍💻.\n
    2.Khamshiq Tadikonda \n
    3.Harish Vemuri\n
    4.BL Kumar \n
    5.Parishudha Babu Vaddi \n
    6.Atchyuth Kumar Puppala \n
    7.Rohith Krishna Kanth Sriram \n""")

@bot.message_handler(commands=['features'])
def send_hello(message):
    bot.reply_to(message, """*Friendly Faculty  \n **Prayer Cell \n **Extra Large Ground \n **Departmental Labs \n **Own Web site \n ****And Many More  """)


@bot.message_handler(content_types=['text'])
def send_text(message):
    msgtxt = message.text.lower()
    # Main Code
    sentence = tokenize(msgtxt)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                bot.send_message(message.chat.id,"{}".format(random.choice(intent['responses'])))
    elif "hod" in msgtxt:
      bot.send_message(message.chat.id, """.......................\n 1. Mr . Ravi Teja(Btech)(Computer Science Engineering (/CME) \n
    2. Mrs . Vasanthi (Btech)(Electronics Communication Engineering)(/ECE)\n
    3. Mr . Ramana (Btech)(VicePrincipal)(Electrical Electronics Engineering (/EEE))\n
    4. Mr . Ravi Teja(btech)(Mechanical Engineering (/DME))\n
    5. Mr . Heeram Das (btech)(Civil Engineering )(/DCE)\n)
    6. Mrs . Kalpana (btech)(Artificial Intelligence and Machine Learning (/DCAIE))\n
    7. Mr . Ravi Teja (Btech)(Computer Science and Engg(ARTIFICIAL INTELLIGENCE)(DCAIE)\n
    8. Mrs . Sowmya (Btech)(Communiction and Computer Networking(/DCCN))\n""")
    elif "course" in msgtxt:
        bot.send_message(message.chat.id, """..............Courses we offer ..............\n 1.Computer Science Engineering (/CME)\n
    2. Electronics Communication Engineering (/ECE)\n
    3. Electrical Electronics Engineering (/EEE)\n
    4. Mechanical Engineering (/DME)\n
    5. Civil Engineering (/DCE)\n
    6. Artificial Intelligence and Machine Learning \n
    7. Computer Science and Engg(ARTIFICIAL INTELLIGENCE)\n
    8. Communiction and Computer Networking\n""")
    else:
        bot.send_message(message.chat.id,"I do not understand...")
    # end credits
bot.infinity_polling()