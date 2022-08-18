#from chatbot import CB
from flask import Flask, render_template, request
import pickle, random, json
import requests
app = Flask(__name__)



@app.route("/chatbot")
def home():
    return render_template("index.html")

#@app.route("/get")
#def get_bot_response():
#   userText = request.args.get('msg')
#   return str(CB.get_response(userText))

@app.route("/get")
def get_bot_response():
   userText = request.args.get('msg')
   #model = pickle.load(open("NaiveModel","rb"))
   #tf = pickle.load(open("tf","rb"))
   #response_tag = model.predict(make_me_ready(userText,tf))
   print(userText)
   data = json.dumps({"sender": "Rasa","message": userText})
   print(data)
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
   #res = requests.post(' https://rasa-deployment-aakash.herokuapp.com/webhooks/rest/webhook', data= data,headers = headers)
   print(res)
   # testing
   #return "Sorry"
   res = res.json()
   print(res)
   val = ""
   if res !=[]:
        for i in res:
            print(i.keys())
            try:
                val = val + " " + i['text']
            except:
                val+="\n"
                continue
        #val = res[0]['text']
        #print(val)

        return val 
   return "Sorry,I did't understand that."

if __name__ == "__main__":
    app.run(debug = True)