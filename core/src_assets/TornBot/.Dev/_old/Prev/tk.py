import requests
import json
import webbrowser
import time
import sys, os
import tkinter as tk
from tkinter import font
from pathlib import Path

root = tk.Tk()
root.title ("Torn Bot : Alpha 0.1")
root.resizable (False, False)
width = 500
height = 500
xco = 25
yco = 20
root.geometry (f"{width}x{height}+{xco}+{yco}")

# ----- Counters and Variables ----- #
# Frame Switching #
market = 0
fly = 0
chain = 0
gym = 0

# Button Closing #
si = 0
tr = 0
lbl_item = 0
itm = 0
sub = 0
entry = 0

# Index Starters 
Items = {}
IDS = {}
User = {}

# ----- User Functions ----- #
def Timer (int) :
    data = range(int, 0, -1)
    for value in data :
        print (value)
        
# ----- Path Sorting ----- #
def Get_Image (image_filename, images_directory = r'images/gui') :
    if getattr (sys, 'frozen', False) :
        bundle_dir = sys.MEIPASS
    else :
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    Image_Path = os.path.join(bundle_dir, images_directory, image_filename)
    return Image_Path
    
def Get_DataIT (data_name, data_directory = r'data') :
    global Items
    if getattr (sys, 'frozen', False) :
        bundle_dir = sys.MEIPASS
    else :
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    Data_Path = os.path.join(bundle_dir, data_directory, data_name)
    with open(Data_Path, 'r') as file:
        Data = json.load(file)
        Items = Data
        
def Get_DataID (data_name, data_directory = r'data') :
    global IDS
    if getattr (sys, 'frozen', False) :
        bundle_dir = sys.MEIPASS
    else :
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    Data_Path = os.path.join(bundle_dir, data_directory, data_name)
    with open(Data_Path, 'r') as file:
        Data = json.load(file)
        IDS = Data
    
def Get_DataUs (data_name, data_directory = r'data') :
    global User
    if getattr (sys, 'frozen', False) :
        bundle_dir = sys.MEIPASS
    else :
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    Data_Path = os.path.join(bundle_dir, data_directory, data_name)
    with open(Data_Path, 'r') as file:
        Data = json.load(file)
        User = Data
        
Get_DataIT ("Items_List.json")
Get_DataID ("IDS.json")
Get_DataUs ("user.json")

# ----- Fonts and Color Creation ----- #
Standard_Font = font.Font (family = "courier new", size = 10, weight = "bold")
Button_Font = font.Font (family = "Helvetica", size = 10, slant = "italic")
BButton_Font = font.Font (family = "Helvetica", size = 12, slant = "italic", weight = "bold")
StatsLable_Font = font.Font (family = "courier new", size = 12, slant = "italic")
BStatsLable_Font = font.Font (family = "courier new", size = 10, weight = "bold", slant = "italic")
Counter_Font = font.Font (family = "courier", size = 10, weight = "bold", slant = "italic")
BigCounter_Font = font.Font (family = "courier", size = 15, weight = "bold")
tb = (f"                            ")

# ----- Pages and Frames ----- #
def Page_Main ( ) :
    Main_Page.tkraise ( )
    
# Main Page Functions #
def Close_Buttons ( ) :
    while True :
        global si
        global tr
        global lbl_item
        global sub
        global entry
        global itm
        S_Items_Button["bg"] = "white"
        Trader_Button["bg"] = "white"
        Items_Button["bg"] = "white"
        S_Items_Button.config(relief="raised")
        Trader_Button.config(relief="raised")
        Items_Button.config(relief="raised")
        si = 0
        tr = 0
        if lbl_item  == 0 :
            MP_BGC.update ( )
            break
        else :
            lbl_item.destroy ( )
            MK_BG.delete (itm)
            sub.destroy ( )
            MP_BGC.update ( )
            break        
    
def Close_Market ( ) :
    global market
    if market == 1 :
        Close_Buttons ( )
        MARKET.lower ( )
        market -= 1
        Market["bg"] = "white"
        Market.config (relief="raised")
        MP_BGC.update ( )
            
def Close_Fly ( ) :
    global fly
    if fly == 1 :
        Close_Buttons ( )
        FLY.lower ( )
        fly -= 1
        Fly["bg"] = "white"
        Fly.config (relief="raised")
        MP_BGC.update ( )
            
def Close_Chain ( ) :
    global chain
    if chain == 1 :
        Close_Buttons ( )
        CHAIN.lower ( )
        chain -= 1
        Chain["bg"] = "white"
        Chain.config (relief="raised")
        MP_BGC.update ( )
        
def Close_Gym ( ) :
    global gym
    if gym == 1 :
        Close_Buttons ( )
        GYM.lower ( )
        gym -= 1
        Gym["bg"] = "white"
        Gym.config (relief="raised")
        MP_BGC.update ( )
    
def Optin_Market ( ) :
    global market
    while True :
        Close_Fly ( )
        Close_Chain ( )
        Close_Gym ( )
        if market == 0 :
            market += 1
            Market["bg"] = "gray"
            Market.config (relief = "sunken")
            MP_BGC.create_window (35, 95, width = 430, height = 45, window = MARKET, anchor = "nw")
            MARKET.lift ( )
            MP_BGC.update ( )
            break
        else :
            Close_Market ( )
            break
    
def Option_Fly ( ) :
    global fly
    while True :
        Close_Market ( )
        Close_Chain ( )
        Close_Gym ( )
        if fly == 0 :
            fly += 1
            Fly["bg"] = "gray"
            Fly.config (relief = "sunken")
            MP_BGC.create_window (35, 95, width = 430, height = 45, window = FLY, anchor = "nw")
            FLY.lift ( )
            MP_BGC.update ( )
            break
        else :
            Close_Fly ( )
            break
    
def Option_Chain ( ) :
    global chain
    while True :
        Close_Market ( )
        Close_Fly ( )
        Close_Gym ( )
        if chain == 0 :
            chain += 1
            Chain["bg"] = "gray"
            Chain.config (relief = "sunken")
            MP_BGC.create_window (35, 95, width = 430, height = 45, window = CHAIN, anchor = "nw")
            CHAIN.lift ( )
            MP_BGC.update ( )
            break
        else :
            Close_Chain ( )
            break
            
def Option_Gym ( ) :
    global gym
    while True :
        Close_Market ( )
        Close_Fly ( )
        Close_Chain ( )
        if gym == 0 :
            gym += 1
            Gym["bg"] = "gray"
            Gym.config (relief = "sunken")
            MP_BGC.create_window (35, 95, width = 430, height = 45, window = GYM, anchor = "nw")
            GYM.lift ( )
            MP_BGC.update ( )
            break
        else :
            Close_Gym ( )
            break
            
def Show_Items ( ) :
    pass
    
def Search_Submit ( ) :
    while True :
        itm = entry.get()
        dat = itm.lower()
        itm = (f"{dat}")
        sub["bg"] = "gray"
        sub.config (relief = "sunken")
        MP_BGC.update ( )
        if itm in Items.keys() :
            entry.delete (0, 'end')
            tag = {f"{itm}" : {
                "ID :" : f"{Items[itm]}"
                }
            }
            dat = json.dumps (tag, indent=4)
            UP (f"{dat}")
            break
        if itm in IDS.keys() :
            entry.delete (0, 'end')
            tag = {f"{itm}" : {
                "Item" : f"{IDS[itm]}"
                }
            }
            dat = json.dumps (tag, indent=4)
            UP (f"{dat}")
            break
        else :
            sub["bg"] = "white"
            sub.config (relief = "raised")
            MP_BGC.update ( )
            entry.delete (0, 'end')
            UP (f"{itm} is not an Item!")
            break
    
def Search_Item ( ) :
    global si
    global lbl_item
    global entry
    global sub
    global itm
    while True :
        if si == 0 :
            si += 1
            S_Items_Button["bg"] = "gray"
            S_Items_Button.config (relief = "sunken")
            MARKET.lower()
            MP_BGC.create_window (35, 95, width = 430, height = 70, window = MARKET, anchor = "nw")
            lbl_item = tk.Label (MARKET, text = "Item", font = Standard_Font)
            MK_BG.create_window (40, 50, window = lbl_item)
            entry = tk.Entry (MARKET, width = 37, font = Standard_Font)
            itm = MK_BG.create_window (210, 50, window = entry)
            sub = tk.Button (MARKET, text = "Submit", command = Search_Submit)
            MK_BG.create_window (385, 50, window = sub)
            MARKET.lift ( )
            MP_BGC.update ( )
            break
        if si == 1 :
            si -= 1
            S_Items_Button["bg"] = "white"
            S_Items_Button.config (relief = "raised")
            MARKET.lower ( )
            MP_BGC.create_window (35, 95, width = 430, height = 45, window = MARKET, anchor = "nw")
            lbl_item.destroy ( )
            entry.destroy ( )
            sub.destroy ( )
            MARKET.lift ( )
            MP_BGC.update ( )
            break
            
def UP (txt) :
    key = (f"{txt}")
    action_box.insert (tk.END, f"{key}")
    action_box.insert (tk.END, "")
    root.update_idletasks ( )
    root.update ( )
    action_box.see (tk.END)
    root.after (100, lambda : action_box.see (tk.END))
    time.sleep (0.5)
   
# ----- Main Page Set-Up ----- #
Main_Page = tk.Frame (root, width = 500, height = 500)
MP_BGI = tk.PhotoImage (file = Get_Image ('Torn.png') )
MP_BGC = tk.Canvas (Main_Page, width = 500, height = 500)
MP_BGC.pack (fill = "both", expand = True)
MP_BGC.create_image (0, 0, image = MP_BGI, anchor = "nw")
lbl_bx = tk.Frame (Main_Page, width = 100, height = 20)
lbl = tk.Label (lbl_bx, text = "Select Option :", font = BigCounter_Font, fg = "red")
lbl.pack ()
MP_BGC.create_window (150, 30, window = lbl_bx)
Settings = tk.Button (Main_Page, text = "Settings", font = Button_Font, width = 15)
MP_BGC.create_window (350, 30, window = Settings)

# Option Market Box #
Market = tk.Button (Main_Page, text = "Market", width = 10, font = Button_Font, command = Optin_Market)
MP_BGC.create_window (100, 80, window = Market)
MARKET = tk.Frame (Main_Page, highlightthickness = 0, borderwidth = 0)
MK_BG = tk.Canvas (MARKET)
MK_BGI = tk.PhotoImage (file = Get_Image ('Torn.png') )
MK_BG.pack (fill = "both", expand = True)
MK_BG.create_image (0, 0, image = MK_BGI, anchor = "nw")
S_Items_Button = tk.Button (MARKET, text = "Search", width = 10, command = Search_Item)
MK_BG.create_window (50, 10, window = S_Items_Button, anchor = "nw")
Trader_Button = tk.Button (MARKET, text = "Trader", width = 10)
MK_BG.create_window (185, 10, window = Trader_Button, anchor = "nw")
Items_Button = tk.Button (MARKET, text = "Items", width = 10, command = Show_Items)
MK_BG.create_window (320, 10, window = Items_Button, anchor = "nw")

# Option Fly Box #
Fly = tk.Button (Main_Page, text = "Fly", width = 10, font = Button_Font, command = Option_Fly)
MP_BGC.create_window (200, 80, window = Fly)
FLY = tk.Frame (Main_Page, highlightthickness = 0, borderwidth = 0)
FL_BG = tk.Canvas (FLY)
FL_BGI = tk.PhotoImage (file = Get_Image ('Torn.png') )
FL_BG.pack (fill = "both", expand = True)
FL_BG.create_image (0, 0, image = FL_BGI, anchor = "nw")
Button1 = tk.Button (FLY, text = "Fbutton", width = 10)
FL_BG.create_window (50, 10, window = Button1, anchor = "nw")
Button2 = tk.Button (FLY, text = "Fbutton", width = 10)
FL_BG.create_window (185, 10, window = Button2, anchor = "nw")
Button3 = tk.Button (FLY, text = "Fbutton", width = 10)
FL_BG.create_window (320, 10, window = Button3, anchor = "nw")

# Option Chain Box #
Chain = tk.Button (Main_Page, text = "Chain", width = 10, font = Button_Font, command = Option_Chain)
MP_BGC.create_window (300, 80, window = Chain)
CHAIN = tk.Frame (Main_Page, highlightthickness = 0, borderwidth = 0)
CH_BG = tk.Canvas (CHAIN)
CH_BGI = tk.PhotoImage (file = Get_Image ('Torn.png') )
CH_BG.pack (fill = "both", expand = True)
CH_BG.create_image (0, 0, image = CH_BGI, anchor = "nw")
Button1 = tk.Button (CHAIN, text = "Cbutton", width = 10)
CH_BG.create_window (50, 10, window = Button1, anchor = "nw")
Button2 = tk.Button (CHAIN, text = "Cbutton", width = 10)
CH_BG.create_window (185, 10, window = Button2, anchor = "nw")
Button3 = tk.Button (CHAIN, text = "Cbutton", width = 10)
CH_BG.create_window (320, 10, window = Button3, anchor = "nw")

# Option Gym Box #
Gym = tk.Button (Main_Page, text = "Gym", width = 10, font = Button_Font, command = Option_Gym)
MP_BGC.create_window (400, 80, window = Gym)
GYM = tk.Frame (Main_Page, highlightthickness = 0, borderwidth = 0)
GY_BG = tk.Canvas (GYM)
GY_BGI = tk.PhotoImage (file = Get_Image ('Torn.png') )
GY_BG.pack (fill = "both", expand = True)
GY_BG.create_image (0, 0, image = CH_BGI, anchor = "nw")
Button1 = tk.Button (GYM, text = "Gbutton", width = 10)
GY_BG.create_window (50, 10, window = Button1, anchor = "nw")
Button2 = tk.Button (GYM, text = "Gbutton", width = 10)
GY_BG.create_window (185, 10, window = Button2, anchor = "nw")
Button3 = tk.Button (GYM, text = "Gbutton", width = 10)
GY_BG.create_window (320, 10, window = Button3, anchor = "nw")

# Action Box #
action_scroll = tk.Scrollbar (Main_Page, orient = "vertical")
Action_Scroll = MP_BGC.create_window (400, 346, window = action_scroll, height = 292)
action_box = tk.Listbox (Main_Page, height = 18, width = 50, state = "normal", yscrollcommand = action_scroll.set, bg = "black", fg = "green")
Action_Box = MP_BGC.create_window (90, 200, window = action_box, anchor = "nw")
action_scroll.config (command = action_box.yview)

# ----- Start Admin ----- #
# Start the Main Page #
Main_Page.grid (row = 0, column = 0)
UP (f"{tb}Welcome to Torn Bot Beta :")
Page_Main ( )       
root.mainloop()