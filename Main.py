import csv
import json
import codecs
import collections
from collections import defaultdict
from mtranslate import translate
import sys
from mtranslate import translate
import uuid
import io

csvReader = csv.reader(codecs.open('C:/Users/MyLaptop/Desktop/orders.csv', 'rU', 'utf-16'))
csvReader1 = csv.reader(open('C:/Users/MyLaptop/Desktop/intents.csv',encoding="utf8"))
Intent_List=list(csvReader1)
AllData=list(csvReader)

listAlphabet:list=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','u','v','x','w','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','W','Y','Z']
def washString(list_string:str , intT:int ,intR:int):
            InputText = list_string
            InputText = InputText.replace('\\', ',')
            if intT==1:
                InputText = InputText.replace ('t', ' ')
            InputText = InputText.replace(':', ' ')
            if intR==1:

                InputText = InputText.replace(']', ' ')
                InputText = InputText.replace('[', ' ')
            else:
                InputText = InputText.replace (']', '')
                InputText = InputText.replace ('[', '')
                InputText = InputText.replace(' ','')

            InputText = InputText.replace('\'', ' ')
            InputText = InputText.replace(',', ' ')

            return InputText

def washList(list_str:list):
    return_list:list=[]
    for item in list_str:
        return_list.append(washString(str(item),1,1))
    return return_list

def intentWasher(intent_washer:str):
    string_changer=intent_washer
    string_changer = string_changer.replace ('[', '')
    string_changer = string_changer.replace (']', '')
    string_changer = string_changer.replace ('\'', '')
    string_changer = string_changer.replace (' ', '')
    return string_changer

def returnIntent(Intent_List:list , AllData:list):
    y: int = 0
    counter_item: int = 0
    Container: list = []
    Hash = defaultdict (list)
    string_changer: str

    for item in Intent_List:


        counter_item = 0
        Container = []

        for jtem in AllData:
            counter_item = counter_item + 1

            if str (jtem).count (intentWasher(str(item))) != 0:
                Container.append (counter_item - 1)

        Hash[intentWasher(str(item))] = Container
    return Hash

def returnIntentSet(AllData:list , Intent_List:list , Intent:str):
    nthlist: list
    newset = set ()
    nthlist=returnIntent(Intent_List,AllData)[Intent]


    Lastlist:list=[]
    for item in nthlist:
      Lastlist.append(AllData[int(item)])
    for item in washList(Lastlist):
      for jtem in str(item).split():
           #if str(jtem).find(',')==False:
                newset.add(jtem)
    return newset



def To_Json_Usersays(intentList):
    tempList:list=[]
    Tarifkon:str=""
    for item in intentList:
        Tarifkon = washString (str (item), 0, 0)

        Tarifkon=Tarifkon.replace(' ','')

        info = {

            'id' : str(uuid.uuid4()),
            'data':[{'text':Tarifkon,
            'userDefined': False}],
            'isTemplate': False,
            'count':0 ,
            'updated': 1531528884
        }
        #print(str(info))
        tempList.append(info)

    return tempList


def To_Json_Intent_data(intentString:str):
        info:dict()={}
        info = {
             'name': intentString,
             'auto': True,
             'contexts': [],
             'id' : str(uuid.uuid4()),
             'responses':[],
             'priority' : 500000,
             'webhookUsed': False,
             'webhookForSlotFilling': False,
             'lastUpdate': 1531528884,
             'fallbackIntent': False,
             'events': []
             }
        return info


def Csv_to_Json(AllData:list  , Intent_List:list):
    StringCon:str=""
    for item in Intent_List:



        #print(returnIntentSet(AllData,Intent_List,'carwash'))
        if (washString(str(item),0,0)).__len__()>3 & (washString(str(item),0,0)).find('?')!=True :

             f1 = open (washString(str(item),0,0).replace(' ',''), 'a+')  # open file in append mode
             g1 = open (washString(str(item),0,0).replace(' ',''),'w')
             with io.open (washString(str(item),0,0).replace(' ',''), "w", encoding="utf-8") as g1:
                 g1.write(str(To_Json_Intent_data(washString(str(item),0,0).replace(' ',''))))
             StringCon = washString(str(item),0,0).replace(' ','')+"_usersays_en"

             f2 = open (StringCon, 'a+')  # open file in append mode
             g2 = open (StringCon, 'w')
             with io.open (StringCon, "w", encoding="utf-8") as g2:

                  g2.write (str(To_Json_Usersays(returnIntentSet(AllData,Intent_List,washString(str(item),0,0).replace(' ','')))))
             f1.close()
             f2.close()
             g1.close()
             g2.close()
#print(translate(str(returnIntentSet(AllData,Intent_List,'decorationTazinat'))))
Csv_to_Json(AllData,Intent_List)
#for item in Intent_List[4]:
 #  print(To_Json_Usersays(returnIntentSet(AllData,Intent_List,washString(str(item),0,0).replace(' ',''))))
