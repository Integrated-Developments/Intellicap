
# PC Automation #
import pyautogui as py
import keyboard
import random

# Data #
import json
import os
import sys
from PIL import ImageGrab as IG

# Networking #
import requests as rq
import webbrowser
import threading as th

# Time #
import datetime as dt
import time as tm

## ----- Variables ----- ##
# Json Importing #
users_data = {}
system_data = {}
serv_dat = {}

# Directing #
urls = {}
dir = 0

# TEMP #
temp_dat = {
    "bars" : {
        "Tct" : 0,
        "happy" : {
            "now" : 0,
            "max" : 0,
            "fill" : 0
        },
        "life" : {
            "now" : 0,
            "max" : 0,
            "fill" : 0
        },
        "energy" : {
            "now" : 0,
            "max" : 0,
            "fill" : 0,
            "ref" : 0
        },
        "nerve" : {
            "now" : 0,
            "max" : 0,
            "fill" : 0,
            "ref" : 0
        },
        "cooldowns" : {
            "drug" : 0,
            "medical" : 0,
            "booster" : 0
        },
        "icons" : {
            "none" : "none"
        }
    },
    "faction" : {
        "info" : {
            "id" : 0,
            "pnts" : 0,
            "mem_bal" : 0,
            "fac_bal" : 0
        },
        "armory" : {
            "weapon" : {
                "R" : 1000,
                "Acq" : 0,
                "Value" : 0
            },
            "armor" : {
                "R" : 1412,
                "Acq" : 0,
                "Value" : 0
            },
            "medical" : {
                "R" : 3067,
                "Acq" : 0,
                "Value" : 0
            },
            "temps" : {
                "R" : 3067,
                "Acq" : 0,
                "Value" : 0
            },
            "drugs" : {
                "R" : 6662,
                "Acq" : 0,
                "Value" : 0
            },
            "boost" : {
                "R" : 6662,
                "Acq" : 0,
                "Value" : 0
            },
            "points" : {
                "R" : 15773,
                "Acq" : 0,
                "Value" : 0
            },
            "lab" : {
                "R" : 105027,
                "Acq" : 0,
                "Value" : 0
            }
        },
        "oc" : {
            "none" : 0
        },
        "chain" : {
            "now" : 0,
            "max" : 0,
            "drop" : 0
        }
    },
    "company" : {
        "info" : {
            "id" : 0,
            "funds" : 0,
            "pop" : 0,
            "eff" : 0,
            "env" : 0,
            "train" : 0,
            "ads" : 0,
            "val" : 0
        },
        "emp" : {
            "1" : {
                "info" : {
                    "name" : 0,
                    "act" : 0,
                    "pos" : 0,
                    "days" : 0,
                    "wage" : 0,
                    "state" : 0
                },
                "stats" : {
                    "man" : 0,
                    "man_inc" : 0,
                    "int" : 0,
                    "int_inc" : 0,
                    "end" : 0,
                    "end_inc" : 0
                },
                "eff" : {
                    "work_stat" : 0,
                    "set_in" : 0,
                    "dir_edu" : 0,
                    "manage" : 0,
                    "addict" : 0,
                    "tot" : 0,
                    "spec" : 0
                }
            }
        },
        "stock" : {
            "tealight" : {},
            "dinner" : {},
            "pillar" : {},
            "scented" : {},
            "holder" : {}
        },
        "upgrades" : {
            "comp_size" : {},
            "staffroom" : {},
            "storage" : {},
            "startup" : 500000
        }
    }
}

## ----- Json Data Importing and Path Sorting ----- ##
# Base Directory #
if getattr(sys, 'frozen', False):
    dir = os.path.dirname(sys.executable)
else:
    dir = os.path.dirname(os.path.abspath(__file__))

# All System Data #
with open (f'{dir}/data/sys.json', 'r') as file :
    sys_dat_raw = json.load(file)
    system_data = sys_dat_raw['System']
    urls = system_data['Static']['URL']

# All Users Data #
with open (f'{dir}/data/user.json', 'r') as file :
    user_dat_raw = json.load(file)
    users_data = user_dat_raw['Users']

## ----- USER CLASS ----- ##
class User ( ) :
    def __init__(self, username, password, urls):
        self.username = username
        self.password = password
        self.url = urls
        self.KEY = users_data[self.username]['Account']['Key']
        self.data = {}
        self.set = {}

        if self.authenticate():
            self.import_data()
            self.sort_temp_data()
        else:
            raise ValueError("Invalid username or password")

    def authenticate(self):
        user_data = users_data.get(self.username)
        if user_data and users_data[self.username]['Account']['Pass'] == self.password:
            return True
        return False

    def import_data(self):
        ## ----- JSON DATA "STATIC"----- ##
        self.data['Account'] = users_data[self.username]['Account']
        self.data['Static'] = users_data[self.username]['Static']
        self.data['Market'] = users_data[self.username]['Market']
        self.set['Settings'] = users_data[self.username]['Settings']
        ## ----- SERVICE KEY FILTERING ----- ##
        services = users_data[self.username]['Account']['Service'].keys()
        if services is not None :
            for serv in services :
                if serv == "Torn_Tools" :
                    self.KEY_TOOL = users_data[self.username]['Account']['Service']['Torn_Tools']['Key']
                if serv == "Torn_Stats" :
                    self.KEY_STAT = users_data[self.username]['Account']['Service']['Torn_Stats']['Torn_Key']
                    self.KEY_STAT_API = users_data[self.username]['Account']['Service']['Torn_Stats']['Stat_Key']
                if serv == "Torn_Exchange" :
                    self.KEY_TEX = users_data[self.username]['Account']['Service']['Torn_Exchange']['Key']
                if serv == "Arson_Ware_House" :
                    self.KEY_AWH = users_data[self.username]['Account']['Service']['Arson_Ware_House']['Torn_Key']
                    self.KEY_AWH_API = users_data[self.username]['Account']['Service']['Arson_Ware_House']['AWH_Key']
                if serv == "Yata" :
                    self.KEY_YATA = users_data[self.username]['Account']['Service']['Yata']['key']
        elif services is None :
            prints ("No Services Registerd")
            prints ("Passing")

    def sort_temp_data(self):
        raw_temp = {}
        calls = [f"{self.url['API_T']}/user/?selections=bars,cooldowns,crimes,refills,icons&key={self.KEY}", f"{self.url['API_T']}/company/?selections=stock,detailed,employees&key={self.KEY}", f"{self.url['API_YATA']}/faction/members/?key=<{self.KEY_YATA}>", f"{self.url['API_T']}/faction/?selections=crimes,currency&key={self.KEY}"]
        for itm in calls :
            try:
                dat_raw = rq.get(itm)
                dat = dat_raw.json()
                raw_temp.update(dat)
            except ValueError as e:
                prints (e)
        prints (json.dumps(raw_temp, indent=4))

    def display_data(self):
        print(f"User: {self.username}")
        print(f"Displaying User Data Coming Soon")

## ----- User Functioning ----- ##
# Bot Initiation #
def signin (data) :
    autolog = system_data['Settings'].get("Auto_Login")
    if autolog in users_data.keys() :
        prints ("Auto-Login...")
        username = autolog
        password = users_data[username]['Account']['Pass']
    elif autolog not in users_data.keys() :
        username = input("Enter Username: ")
        password = input("Enter Password: ")
    try:
        urls = system_data['Static']['URL']
        user = User(username, password, urls)
        prints ("Sign in Successful")
        TornBot_Coms (user)
    except ValueError as e:
        prints (e)

def TornBot_Coms (user) :
    prints ("type h for a list of available commands")
    while True :
        com = input (f"{user.username}/Torn_Bot/Command? : ").lower()
        coms = "main"
        print ("")
        reg_com = system_data['Coms']['main'].keys()
        if com == "train" :
            prints ("Training Thread")
        if com == "chain" :
            prints ("Chaining Thread")
        if com == "crimes" :
            Crimes (user)
        if com == "fly" :
            prints ("Traveling Threading")
        if com == "market" :
            prints ("Market Scripting")
        if com == "faction" :
            prints ("Faction Scripting")
        if com == "company" :
            Company (user)
        if com == "sys" :
            prints ("System Settings Coming Soon")
        if com == "set" :
            prints ("User Setting Coming Soon")
        if com == "h" :
            help (coms=coms)
        if com == "ex" :
            break
        elif com not in reg_com :
            prints (f"{com}, is not a Vaild Command...", f"Type h for a List of Available Commands")

# Help Function #
def help (coms=None) :
    dict = {}
    dict = system_data['Coms'].get(coms)
    prints (f"{json.dumps(dict, indent=4)}")

# Useful #
def prints (txt) :
    print (txt)
    print ("")

def tmr (x) :
    prints (f"Waiting {x}s")
    while x > 0 :
        prints (x)
        x -= 1
        tm.sleep (1)

def Rtmr (x) :
    partial_w = random.uniform(0.001, 0.999)
    deviation = (x * 1.367)
    diff_w = (deviation - x)
    diff = (diff_w + partial_w)
    max = (x + diff)
    min = (x - diff)
    if min < 1 :
        partial = (x / 4.364)
        min = (x + partial)
    tot_diff = (max - min)
    if tot_diff <= 3 :
        max += 2.539
    choice = random.uniform(min, max)
    w = int(choice)
    f = (choice - w)
    for i in range(1, w +1) :
        if i <= 59 :
            prints (f"{i}sec...")
            tm.sleep (1)
    if f > 0 :
        tm.sleep (f)

def web (url) :
    webbrowser.open (url)
    tmr (5)

def img (sort) :
    img = (f"{dir}/images/{sort}.png")

def cur_move (sort) :
    img = (f"{dir}/images/{sort}.png")
    found = py.locateOnScreen (img, confidence=(0.8))
    if found is not None :
        py.moveTo (found)

## ----- SCRIPTING ----- ##
# Company #
def Company (user) :
    while True :
        com = input (f"{user.username}/Torn_Bot/Company/Command? : ").lower()
        coms = "company"
        reg_com = system_data['Coms']['company'].keys()
        if com == "run" :
            pass # Start The Thread #
        if com == "set" :
            pass # Adjust Company Thread Settings #
        if com == "h" :
            help (coms=coms)
        if com == "ex" :
            break

# Crimes #
def Crimes (user) :
    while True :
        com = input (f"{user.username}/Torn_Bot/Crimes/Command? : ").lower()
        coms = "crimes"
        reg_com = system_data['Coms']['crimes'].keys()
        if com == "run" :
            Sort_Act_Crimes (user)
        if com == "set" :
            pass # Adjust Company Thread Settings #
        if com == "h" :
            help (coms=coms)
        if com == "ex" :
            break

def Sort_Act_Crimes (user) :
    prints ("Running Crimes Thread Action")
    prints ("Committing Crimes...")
    Rtmr (3)
    main = user.data['Settings']['Crimes']['Main']
    sub = user.data['Crimes']['Sub']
    act_dat = {},
    act_dat['regen'] = (user.Account['Nerve_Max'] * 300)
    if main == "forgery" :
        if sub == "lisc_plate" :
            Forg_Lisc_Plt_Thread (user, data=act_dat)

def Forg_Lisc_Plt_Thread (user, data=None) :
    web (f"{urls['URL_Crime']}{users_data.Settings['Main']}")
    act_buttons = ['draft', 'sign', 'print', 'cut', 'cover']
    step = None
    for action in act_buttons :
        path = f"crimes_forgery_{action}"
        project = py.locateOnScreen (f"{img (path)}", confidence=(0.8))
        if project is not None :
            step = action
        if project is None :
            step = "begin"
    if step is not None :
        while True :
            if step == "begin" :
                cur_move (f"crimes_forgery_{step}")
            if step == "draft" :
                pass
            if step == "sign" :
                pass
            if step == "print" :
                pass
            if step == "cut" :
                pass
            if step == "cover" :
                pass
    elif step is None :
        prints ("System Error")


# Training #
def Train (user) :
    while True :
        com = input (f"{user.username}/TornBot/Training/Command? :").lower()

def Script ( ) :
    prints ("Bot Loading...")
    Rtmr (5)
    signin (data=users_data)

Script ( )