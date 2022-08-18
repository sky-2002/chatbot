# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
import random
# importing required modules
import requests, json
import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer


#download_model(model='bert-squad_1.1',dir='./models')

class ActionVideo(Action):
    def name(self) -> Text:
        return "action_video"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:
        video_urls = ["https://www.youtube.com/watch?v=bW_8EYHcsMI",
        "https://www.youtube.com/watch?v=01lBDjMD1f8",
        "https://www.youtube.com/watch?v=a-kvfaYOlkM",
        "https://www.youtube.com/watch?v=x_Zw45b8ngs"]
        dispatcher.utter_message("Playing your video....")
        webbrowser.open_new(random.choice(video_urls))
        return []

class ActionValidateAge(Action):
    def name(self) -> Text:
        return "action_validate_age"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:
        print("Age related action called")
        #dispatcher.utter_message("Validating age, please wait...")

        #age = tracker.latest_messsage["entities"]
        print("Reached line before age")
        #age = tracker.latest_messsage.text
        #age =  tracker.latest_message['entities']#.get('value')
        print("----------------------------------------------------")
        print(tracker.latest_message)
        print("----------------------------------------------------")
        age =  tracker.latest_message['entities'][0]['value']
        #dispatcher.utter_message(f"Your age is {age}.\n \n")
        result = f"Your age is {age}."
        if int(age)>=18:
            result+=f"As your age is 18 or above, you are eligible to open account."
            #dispatcher.utter_message()
        else:
            result+=f"Sorry..., you must be at least 18 years old to open an account."
            #dispatcher.utter_message()
        dispatcher.utter_message(result)
        return []

savings = {"Messi":20000,"Krishna":30000,"Jason":70000}
class ActionTransferMoney(Action):
    def name(self) -> Text:
        return "action_transfer_money"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:
        print("Transfer money action called.")
        print("----------------------------------------------------")
        print(tracker.latest_message)
        print("----------------------------------------------------")

        print(savings)

        payer =  tracker.get_slot("name")
        payee = tracker.get_slot("payee")
        amount = int(tracker.get_slot("amount"))

        result = ""
        if payer not in savings.keys():
            result+=f"Sorry...You need to have an account to transfer money."
        elif payee not in savings.keys():
            result+="Couldn't process request. Payee needs to have an account in our bank, sorry."
        elif amount>savings[payer]:
            result+="Sorry...You do not have enough money to transfer, need a loan?"
        else:
            print(f"Initial balance of {payer}",savings[payer])
            print(f"Initial balance of {payee}",savings[payee])
            savings[payer]-=amount
            savings[payee]+=amount
            print(f"Final balance of {payer}",savings[payer])
            print(f"Final balance of {payee}",savings[payee])
            result+=f"An amount of {amount} has been sent to {payee}. Your balance is {savings[payer]}. Thank you for using our service."
        dispatcher.utter_message(result)
        return []



class ActionFindATM(Action):
    def name(self) -> Text:
        return "action_find_atm"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:

        # Python program to get a set of
        # places according to your search
        # query using Google Places API
        print("ATM action called")
        # enter your api key here
        api_key = ''

        # url variable store url
        url = ""
        # The text string on which to search
        query = "ATM"

        # get method of requests module
        # return response object
        r = requests.get(url + 'query=' + query +
                                '&key=' + api_key)
        
        # json method of response object convert
        # json format data into python format data
        x = r.json()
        print(x)
        # now x contains list of nested dictionaries
        # we know dictionary contain key value pair
        # store the value of result key in variable y
        y = x['results']

        # keep looping upto length of y
        for i in range(len(y)):
            
            # Print value corresponding to the
            # 'name' key at the ith index of y
            print(y[i]['name'])

bank = '''
A fixed deposit, also known as an FD, is an investment instrument offered by banks, as well as non-banking financial companies (NBFC) to their customers to help them save money. With an FD account, you can invest a sizeable amount of money at a predetermined rate of interest for a fixed period. At the end of the tenure, you receive the lump sum, along with an interest, which is a good money-saving plan. Banks offers different rates of interest for a fixed deposit account.
You can choose a fixed deposit for a period ranging from minimum 7-14 days to maximum 10 years. This is why an FD is sometimes called a term deposit. When you open a fixed deposit account at a specific interest rate, it is guaranteed, for the rate of interest remains the same, irrespective of any changes, which happen due to market fluctuations.Hence it is secured.
The interest you earn is either paid at maturity or on periodic basis depending on your choice. You are not allowed to withdraw the money before the maturity. If you want to, you have to pay a penalty.
The returns of a fixed deposit are guaranteed. You will get the same return agreed at the time of opening an FD. This is not the case with market-led investments, which offers returns based on the fluctuations of interest rates in the market. You will receive the same interest that was agreed to you, even if the interest rates fall. This makes the fixed deposit more secured than any other investments.
The interest rate on a fixed deposit varies depending on the term you choose. However, the rate of interest is fixed. If you want to know the current FD interest rates, you can visit the IDFC FIRST Bank website
'''

car = '''
For salaried individuals(can be employees 
of private limited companies or public sector),the
minimum age of applicant should be 21 years at the time of 
applying and not more than 60 at the end of tenure, and the
minimum earning should be Rs.3,00,000 per anum.

For self employed individuals or business people, you can apply if
age is 21 or above at time of application, not above 60 at end of tenure and minimum income should be 
Rs.3,00,000 per anum.
'''

docs ='''
You need any one of Valid passport, driving licence,
voter ID card, Aadhar card. For income proof, you can
submit latest salary slip as Form number 16. You also
need to submit bank statement of past 6 months.If you 
are a self employed insividual, you also need ITR as 
proof of income. For address proof, you need any one of
telephone bill, electricity bill.
'''

car2 = '''
For people who are salaried, which includes employees of private and public sector, are eligible for loan.
Also, the applicant must be above 21 years of age at the time of applying, and not older than 60 years of 
age at end of tenure. Also, the individual should have had a job for at least 2 years with minimum 1 year 
with current employer. The minimum income should be Rs. 3,00,000 per year and should have a telephone.
For business people, the minimum age is 21 and no older than 65 at the end of tenure. Should be doing business
for at least 2 years. Income should be atleast Rs. 3,00,000 per annum.
'''

health_suraksha = '''
Health suraksha is a health insurance scheme which not only covers hospitalization costs but also
pre and post medication expenses.
It has a wide coverage in a way that you can choose an individual Health Suraksha scheme or a Family Floater health insurance policy according to your
requirements and the coverage is optimal and comes at an affordable price.
You can opt for a HDFC ERGO Health Suraksha policy that runs for a time period of 
one or two years (With Life time renewability).
HDFC ERGO Health Suraksha will provide for at the cost of a health check up if you have 
completed 4 years without making a claim.
You can avail of the Income Tax benefits under Section 80D of the Income Tax Act.  
As per section 80D, a taxpayer can deduct tax on premium paid towards medical insurance 
for self, spouse, parents and dependent children.
'''

car_insurance = '''
The policy covers loss or damage caused to your vehicle by any one of the events from 
Accident by external means, Burglary, housebreaking or theft , Fire, explosion, self ignition, lightning,
Terrorism, riots, strikes, malicious acts, Transit by road, rail, inland waterways, air or lift,
Earthquake, flood, storm, landslide or rockslide. The policy would also cover any legal liability 
arising out of injury to or death of a third party and property damage of a third party in case of 
an accident involving your vehicle.The policy also provides compulsory personal accident cover for 
owner-driver for an amount of Rs. 2 lakh in case of accidental death and permanent total disability.
'''

pin_reset = '''
If you are at the ATM and realise “I forgot my ATM Card PIN number” after putting your card inside the machine, do not worry.
Choose Forgot PIN or Regenerate ATM PIN option on the menu. 
You would be redirected to a screen to enter your registered mobile number, 
which triggers an OTP to that number. Enter the OTP on the screen, 
and you would be redirected to choose another PIN. The reset through this mechanism happens immediately, 
and you can withdraw cash once it resets.
'''

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
def corrected(answer):
  corrected_answer = ''

  for word in answer.split():
      
      #If it's a subword token
      if word[0:2] == '##':
          corrected_answer += word[2:]
      else:
          corrected_answer += ' ' + word
  return corrected_answer

def giveAnswer(question,paragraph):
  
  encoding = tokenizer.encode_plus(text=question,text_pair=paragraph)#, add_special=True)
  
  inputs = encoding['input_ids']  #Token embeddings
  
  sentence_embedding = encoding['token_type_ids']  #Segment embeddings
  tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens
  
  outputs = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]))
  start_index = torch.argmax(outputs.start_logits)

  end_index = torch.argmax(outputs.end_logits)

  answer = ' '.join(tokens[start_index:end_index+1])
  return corrected(answer)


class ActionFixedDepositInfo(Action):
    def name(self) -> Text:
        return "action_fixed_deposit_info"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:

        query = tracker.latest_message['text']
        print(query)

        ans = giveAnswer(query,bank)
        #prediction = cdqa_pipeline.predict(query)
        dispatcher.utter_message(ans)
        return []

class ActionCarLoanEligibility(Action):
    def name(self) -> Text:
        return "action_car_loan_eligibility"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:

        query = tracker.latest_message['text']
        print(query)

        ans = giveAnswer(query,car)
        dispatcher.utter_message(ans)
        return []

class ActionCarLoanDocs(Action):
    def name(self) -> Text:
        return "action_car_loan_docs"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:

        query = tracker.latest_message['text']
        print(query)

        ans = giveAnswer(query,docs)
        dispatcher.utter_message(ans)
        return []

class ActionCarInsuranceInfo(Action):
    def name(self) -> Text:
        return "action_car_insurance_info"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:

        query = tracker.latest_message['text']
        print(query)

        ans = giveAnswer(query,car_insurance)
        dispatcher.utter_message(ans)
        return []

class ActionHealthInsurance(Action):
    def name(self) -> Text:
        return "action_health_insurance"

    async def run(
        self,dispatcher,
        tracker:Tracker,
        domain:"DomainDict")-> List[Dict[Text, Any]]:

        query = tracker.latest_message['text']
        print(query)

        ans = giveAnswer(query,health_suraksha)
        dispatcher.utter_message(ans)
        return []
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []