from flask import url_for, Flask, request,render_template
import google.generativeai as genai
import json
import os


API_KEY='AIzaSyD6V7UQ9_AgMhiH76t2o9td3bAPXFfrhb0'
genai.configure(api_key=API_KEY)

generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 9000,
  "stop_sequences": [
    "be safe ",
  ],
}


safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

#################################
# Define the initial data structure
initial_data = {
    "conversation": {
        "messages": []
    }
}
with open('conversation.json', 'w') as file:
    json.dump(initial_data, file)


# upload the conversation history from the json file, if it doesn't exist create it, and set the permissions to read and write only for the owner so that the file is not accessible by others
def get_history():
  try:
    File=open('conversation.json','r')
  except:
    File=open('conversation.json','w')
    File.write(json.dumps({'conversation':{'messages':[]}}))
    File.close()
    os.chmod('conversation.json', 0o600)
    File=open('conversation.json','r')
  conversation=json.load(File)
  File.close()
  return conversation['conversation']['messages']


#initialize the conversation history and the welcome message from welcome.txt
H=get_history()
msg="Salut! Je suis un bot spécialisé dans l'assistance pour l'auto-formation en science des données. Comment puis-je vous être utile aujourd'hui?"



#initialize the model (classic way)
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

#initialize the chat with the history (the first message should always be from the user not the model)

  
Chat=model.start_chat(history=H)
#prompt=open('prompt.txt','r') # read the prompt from the file and send it to the model so he can get the context of the conversation
#inst=prompt.read()
#prompt.close()

#Chat.send_message(inst)

app = Flask(__name__)  # create an app instance

# create a route for the web app
@app.route("/")
def index():
    bot_img=url_for('static', filename='hat.png')
    usr_img=url_for('static', filename='user.png')
    return render_template('index.html',bot_img=bot_img,usr_img=usr_img,history= [{'role':'model','parts':[msg]}]+H)


# create a route for the chat app so that the user can send a message to the model
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    global H
    
    return get_chat_response(input,H)



def get_chat_response(question,history=H,chat=None):
    if chat is None:
      global Chat
      chat=globals()['Chat']

    prompt = f"""Vous êtes un bot serviable et amical qui répond aux questions sur l'auto-formation dans le domaine des données.
        Assurez-vous de répondre en phrases complètes. et reponse complete, ne répondez pas avec des réponses longues.
        QUESTION : '{question}'

        ANSWER:
        """
    respone = chat.send_message(prompt)
    r=respone.text
    r=r.replace('*',' ')
    
    H.append({'role':'user','parts':[question]})
    
    H.append({'role':'model','parts':[r]})
    File=open('conversation.json','w')
    json_data=json.dumps({'conversation':{'messages':H}})
    File.write(json_data)

    return  r





if __name__=='__main__':  # on running python app.py
    app.run()  # run the flask app
