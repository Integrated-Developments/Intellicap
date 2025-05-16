### ---------- TornBot Alpha 0.1 ---------- ###
import json, jsonify
import datetime as dt, time as T
import os, sys
import webbrowser, requests as rq
import pyautogui as pyat
import threading as TH, subprocess as sub
import random, string

## ----- Globals ----- ##
# Path and Data #
_dir = 0
exe = 0
usr_dat = {}
sys_dat = {}
tmp_dat = {}
USER = 0
key = 0
items = {}
str_gen = {
    "count" : 0,
    "result" : "",
    "strings" : {}
}
act_cntr = 0
path = 0

# Urls #  https://api.torn.com/ market/ ?selections=lookup &key=mdHz0qLMvoYFQhLJ
api = "https://api.torn.com/"
stat = "https://tornstats.com"
torn = "https://www.torn.com/"
yata = "https://yata.yt"

## ----- Useful Functions ----- ##
def prints (*args) :
    for txt in args :
        print (txt)
        print ("")
    T.sleep (1)

def Timer (x, direction, randomize=bool) :
    if direction == 1 : ## Counts from 0 to x ##
        if randomize is True :
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
                    T.sleep (1)
            if f > 0 :
                T.sleep (f)
        elif randomize is False :
            z = 0
            while x > 0 :
                z += 1
                prints (z)
                x -= 1
                T.sleep (1)
    elif direction == 0 : ## Counts from x to 0 ##
        if randomize is True:
            partial_w = random.uniform(0.001, 0.999)
            deviation = (x * 1.367)
            diff_w = (deviation - x)
            diff = (diff_w + partial_w)
            max = (x + diff)
            min = (x - diff)
            if min < 1:
                partial = (x / 4.364)
                min = (x + partial)
            tot_diff = (max - min)
            if tot_diff <= 3:
                max += 2.539
            choice = random.uniform(min, max)
            w = int(choice)
            f = (choice - w)
            for i in range(w, 0, -1):
                print(f"{i}sec...")
                T.sleep(1)
            if f > 0:
                T.sleep(f)
        elif randomize is False:
            while x > 0:
                print(x)
                x -= 1
                T.sleep(1)

def Thread_Start (command, console=bool) : #if no console script = User Function, if Console Script = directory loaction of a py script
    global act_cntr, str_gen
    if not console :
        act_cntr += 1
        act = TH.Thread(target=command)
        act.daemon = True
        act.start()
    else :
        sub.Popen(['python', f'{command}.py'], creationflags=sub.CREATE_NEW_CONSOLE)

def Generate_String (char=int, debug=None) :
    global str_gen
    str_gen['result'] = ""
    for i in range (char) :
        str_gen['result'] += random.choice(string.ascii_letters + string.digits)
    str_gen["count"] += 1
    var_name = (f"str{str_gen['count']}")
    format = {var_name:str_gen['result']}
    var = str_gen['strings'].update(format)
    if debug is not None :    
        prints (f"For trouble shooting...", f"str_gen : {str_gen}", f"Var_Name : {var_name}", f"Format : {format}")
    with open (f"{_dir}/dev/str_gen.json", 'w') as file :
        json.dump (str_gen, file, indent=4, sort_keys=True)
    return (f"{str_gen['result']}")

## ----- Bot Data Gathering ----- ##
def Get_Data () :
    global _dir, exe, usr_dat, sys_dat, key, USER, tmp_dat
    print ("")
    if getattr(sys, 'frozen', False) :
            _dir = os.path.dirname(sys.executable)
            exe = True
            prints ("exe = True")
    else:
            _dir = os.path.dirname(os.path.abspath(__file__))
            exe = False
            prints ("exe = False")
    with open (f"{_dir}/data/console/sys.json", 'r') as file :
        raw = json.load (file)
        prints (json.dumps(raw, indent=4))
        sys_dat = raw['sys_dat']
        usr_dat = raw['usr_dat']
        USER = sys_dat['static']['USER']
        key = usr_dat[USER]['_key']
        tmp_dat = raw['tmp_dat']

def img (file, x=None) :
    global path, _dir
    if x == "web" :
        path = os.path.join(_dir, "images", "pc", "web", f"{file}.PNG")
    return path

def Save (data=None) :
    if data == "usr" or data == "tmp" or data == "tmp" :
        path = (f"{_dir}/console/sys.json")
        with open (path, 'w') as file :
            user_dat = {
                "sys_dat" : sys_dat,
                "usr_dat" : usr_dat,
                "tmp_dat" : tmp_dat
            }
            json.dump (user_dat, file, indent=4, sort_keys=True) 

def Item_List (up=bool) :
    global items
    file = (f"{_dir}/data/console/itemslist.json")
    while True :
        if os.path.isfile(file):
            with open (f"{_dir}/data/console/itemslist.json", 'r') as file :
                dat = json.load (file)
                items = dat['items']
            if up is None :
                prints(f"The file '{file}' exists.", "Imported Data", "Starting Bot")
                break
            elif up is not None :
                prints(f"The file '{file}' exists.", "Imported Data", "Checking for Updates")
        raw_rq = rq.get (f"{api}torn/?selections=items&key={key}")
        raw = raw_rq.json()
        if up is True :
            prints ("updating coming soon", "Starting Bot")
            break
        else :
            list = {}
            for item_id, details in raw.items() :
                list = {
                    "info" : {
                        "descrip": details["description"],
                        "image": details["image"],
                        "name" : details["name"],
                        "require": details["requirement"],
                        "type": details["type"],
                        "weapon_type": details["weapon_type"],
                    },
                    "trader" : {
                        "circulation": { 
                            "current" : details["circulation"],
                            "circ_1d" : "",
                            "circ_2d" : "",
                            "circ_3d" : "",
                            "circ_5d" : "",
                            "circ_1w" : "",
                            "circ_2w" : "",
                            "circ_1m" : ""
                        },
                        "logs" : {
                            "" : {}
                        },
                        "stats" : {
                            "avg_buy" : 0,
                            "avg_sell" : 0,
                            "bought" : [0,0], # [{number of items}{total spent}]
                            "inventory" : 0, # amount in inventory
                            "sold" : [0,0], # [{number sold}{gross return}]
                        },
                        "trade" : {
                            "market" : [0,0],
                            "bulk" : [[0,0],[0,0]], # [[buy:{amt},{multi("Xstr")specific(int)}],[sell:{amnt},{multi}]]
                            "profit" : 0,
                        },
                        "value": {
                            "current" : details["buy_price"],
                            "value_12" : [0,0,0], # [{avg},{high},{low}] 
                            "value_24" : [0,0,0],
                            "value_1w" : [0,0,0],
                            "value_2w" : [0,0,0],
                            "value_1m" : [0,0,0]
                        }
                    },
                }
                if details["effect"] :
                    list["info"]["effect"] = details["effect"]
                items[item_id] = list
            prints (items)
            with open (f'{_dir}/data/itemslist.json', 'w') as file :
                json.dump ({"items" : items}, file, indent=4)
                prints ("Items List Created")
                break

def TMP (key) :
    raw = rq.get(f"{api}user/?selections=bars,refills,cooldowns,money&key={key}")
    resp = raw.json()
    tmp_dat['happy']['max'] = resp['happy']['maximum']
    tmp_dat['happy']['current'] = resp['happy']['current']
    tmp_dat['happy']['ttf'] = resp['happy']['fulltime']
    tmp_dat['happy']['tick'] = [resp['happy']['increment'], resp['happy']['interval']]
    tmp_dat['health']['max'] = resp['life']['maximum']
    tmp_dat['health']['current'] = resp['life']['current']
    tmp_dat['health']['ttf'] = resp['life']['fulltime']
    tmp_dat['health']['tick'] = [resp['life']['increment'], resp['life']['interval']]
    tmp_dat['energy']['max'] = resp['energy']['maximum']
    tmp_dat['energy']['current'] = resp['energy']['current']
    tmp_dat['energy']['ttf'] = resp['energy']['fulltime']
    tmp_dat['energy']['refill'] = resp['refills']['energy_refill_used']
    tmp_dat['energy']['tick'] = [resp['energy']['increment'], resp['energy']['interval']]
    tmp_dat['nerve']['max'] = resp['nerve']['maximum']
    tmp_dat['nerve']['current'] = resp['nerve']['current']
    tmp_dat['nerve']['ttf'] = resp['nerve']['fulltime']
    tmp_dat['nerve']['refill'] = resp['refills']['nerve_refill_used']
    tmp_dat['nerve']['tick'] = [resp['nerve']['increment'], resp['nerve']['interval']]
    tmp_dat['chain']['hits'] = [resp['chain']['current'], resp['chain']['modifier']]
    tmp_dat['chain']['timer'] = resp['chain']['timeout']
    tmp_dat['chain']['cooloff'] = resp['chain']['cooldown']
    tmp_dat['health']['drugs'] = resp['cooldowns']['drug']
    tmp_dat['health']['booster'] = resp['cooldowns']['booster']
    tmp_dat['health']['medical'] = resp['cooldowns']['medical']
    tmp_dat['money']['onhand'] = resp['money_onhand']
    tmp_dat['money']['points'] = resp['points']
    tmp_dat['money']['cayman'] = resp['cayman_bank']
    tmp_dat['money']['vault'] = resp['vault_amount']
    tmp_dat['money']['company'] = resp['company_funds']
    tmp_dat['money']['bank'] = [resp['city_bank']['amount'],resp['city_bank']['time_left']]
    tmp_dat['money']['networth'] = resp['daily_networth']
    raw = rq.get(f"{api}market/?selections=pointsmarket&key={key}")
    resp = raw.json()
    tmp_dat['p_market'] = resp['pointsmarket']
    with open (f'{_dir}/data/console/sys.json', 'w') as file :
        temp_data = {
            "sys_dat" : sys_dat, 
            "usr_dat" : usr_dat,
            "tmp_dat" : tmp_dat
        }
        parse = json.dump (temp_data, file, indent=4, sort_keys=True)
## ----------- FUCK FINBAR ---------------##
def hosp () :
     while True :
        raw = rq.get('https://api.torn.com/user/3299722?selections=&key=mdHz0qLMvoYFQhLJ')
        finbar = raw.json()
        if finbar['status']['state'] == "okay" :
            webbrowser.open ("https://www.torn.com/profiles.php?XID=3299722")

### ---------- Script Execution ---------- ###
def TornBot () :
    Get_Data ()
    Item_List (up=True)
    commit = usr_dat[USER]['settings']['crimes']['commit']
    if commit == "false" :
        return ()
    else :
        global key
        if commit[0] == "forgery" :
            TMP (key=key)
            calc = (tmp_dat['nerve']['current'] / 5)
            if calc >= 1 : 
                webbrowser.open ("https://www.torn.com/loader.php?sid=crimes#/forgery")
                while True :
                    txt = img("forgery",x="web")
                    forgery = (f"{txt}")
                    prints (forgery)
                    loaded = pyat.locateOnScreen(forgery, confidence=(0.8))
                    if loaded is not None :
                        break
                    else :
                        pass
            while True :
                if calc >= 1 :
                    plates = img("forgery_lic_pla", x="web")
                    started = pyat.locateOnScreen(plates, confidence=(0.8))
                    if started is None :
                        start = img("forgery_begin_project", x="web")
                        begin = pyat.locateOnScreen(start, confidence=(0.8))
                        if begin is not None :
                            move = pyat.moveTo(begin)
                            click = pyat.click ()
                    actions = ["forgery_lic_pla_rub", "forgery_lic_pla_drill", "forgery_lic_pla_paint", "forgery_lic_pla_dry", "forgery_lic_pla_cut"]
                    result = ["forgery_success", "forgery_fail"]
                    for path in actions :
                        imges = img(path, x="web")
                        act = pyat.locateOnScreen(imges, confidence=(0.8))
                        if act is not None :
                            pyat.moveTo (act)
                            pyat.click ()
                            calc -= 1
                            tmp_dat['nerve']['current'] -= 5
                            tmp_dat['nerve']['ttf'] += (5 * tmp_dat['nerve']['tick'][0] * tmp_dat['nerve']['tick'][1])
                if calc < 1 :
                    if tmp_dat['nerve']['refill'] == "false" :
                        # use refill
                        pass
                    if tmp_dat['health']['booster'] <= 86400 :
                        # use beer/can
                        pass

##### ---------- RUN ---------- #####
TornBot () 