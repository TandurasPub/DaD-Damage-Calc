import numpy as np
from scipy.stats import hypergeom 
import matplotlib.pyplot as  plt

import tkinter
from tkinter import ttk

def generate_graph(): 
    castDam = float(book_entry.get())
    add = float(add_entry.get())
    true = float(true_entry.get())
    mpb = float(mpb_entry.get())/100

    MDR = float(MDR_entry.get())/100
    projRes = float(projRes_entry.get())/100
    hsRes = float(hsRes_entry.get())/100
    debuff = float(debuffDurr_entry.get())/100

    headshot = headshot_combobox.get()
    if headshot == "Uh, duh. I'm a gamer": 
        hsMult = (1.5-hsRes)
    else: 
        hsMult = 1

    #quick calcs for mult later 
    funcMDR = (1-MDR)
    funcProjRes = (1-projRes)

    fullRes = funcMDR

    spellDam = 1
    spellScale = 1
    spellBurn = 0
    spellHit = 1
    spellProj = 0
    canHS = 0
    #"Ignite", "Zap", "Magic Missile", "Ice Bolt", "Explosion", "Fireball (Splash)", "Lightning Strike", "Chain Lightning"
    spell = spell_combobox.get()
    
    if spell == "Ignite": 
        spellDam = 5
        spellScale = 0.5
        spellBurn = 1
        spellHit = 1
        canHS = 1
    elif spell == "Zap": 
        spellDam = 20
        spellScale = 1
        spellBurn = 1
        spellHit = 1
    elif spell == "Magic Missile": 
        spellDam = 9
        spellScale = 1
        spellBurn = 0 
        spellHit = 9
        spellProj = 1
    elif spell == "Ice Bolt": 
        spellDam = 30 
        spellScale = 1 
        spellBurn = 0 
        spellHit = 1
        spellProj = 1
    elif spell == "Explosion": 
        spellDam = 25
        spellScale = 1
        spellBurn = 2
        spellHit = 1
        spellProj = 1
    elif spell == "Fireball (Splash)": 
        spellDam = 10
        spellScale = 1
        spellBurn = 2
        spellHit = 1
    elif spell == "Fireball (Direct)": 
        spellDam = 20
        spellScale = 1
        spellBurn = 2
        spellHit = 2
        spellProj = 1
    elif spell == "Lightning Strike":
        spellDam = 30
        spellScale = 1
        spellBurn = 0 
        spellHit = 1
    elif spell == "Chain Lightning": 
        spellDam = 30
        spellScale = 1
        SpellBurn = 0
        spellHit = 1

    if spellProj == 1:
        fullRes = funcMDR*funcProjRes
    else:
        fullRes = funcMDR

    dam = (((spellDam + (castDam * spellScale)) * (1 + (mpb*spellScale))) + (add * spellScale))

    if spellProj == 1 or canHS == 1:
        dam = dam * hsMult

    if spellBurn > 0:
        dam = dam + ((spellBurn + (0.5 * castDam)) * (1+(0.5 * mpb))) + (0.5 * add) 
    
    dam = dam * fullRes
    
    if spell == "Fireball (Direct)":
        dam += ((((10 + castDam) * mpb) + add) * funcMDR)
        

    dam += (true * spellScale)  
    

    if spellBurn > 0: 
        dam += (0.5 * true)

    print("Damage: " + str(dam))

    # String Building
    roundedDam = np.round(dam,decimals=2)
    retStr = "Total Damage: " + str(roundedDam)

    if spell == "Chain Lightning": 
        bounceReduc = 5.0 * (1+mpb) 
        bounceReduc = np.round(bounceReduc, 2)
        retStr = retStr + "\rEach bounce does " + str(bounceReduc) + " less damage" 
    elif spell == "Magic Missile": 
        retStr = "Damage per Missile: " + str(roundedDam)
        retStr = retStr + "\r Total Damage: " + str(np.round(roundedDam * spellHit, 2))
    
    disp = tkinter.Message(frame, text=retStr)
    disp.grid(row=4, column= 1, sticky="news", padx=15, pady=15)
    
window = tkinter.Tk()
window.title("Simple Damage Calc")

frame = tkinter.Frame(window)
frame.pack()

# saving user info 
draw_info_frame = tkinter.LabelFrame(frame, text ="Character Enhancements")
draw_info_frame.grid(row= 0, column= 0)

draw_opp_frame = tkinter.LabelFrame(frame, text="Opponent Info (Enter whole %'s, not decimals)")
draw_opp_frame.grid(row=0, column=1)

MDR_label = tkinter.Label(draw_opp_frame, text="Opponent % MDR:")
MDR_label.grid(row=0, column=0,sticky="w")

projRes_label = tkinter.Label(draw_opp_frame, text="Opponent % Proj Resist:")
projRes_label.grid(row=1, column=0,sticky="w")

hsRes_label = tkinter.Label(draw_opp_frame, text="Opponent % Headshot Resist:")
hsRes_label.grid(row=2, column=0,sticky="w")

debuffDur_label = tkinter.Label(draw_opp_frame, text="Opponent % Debuff Duration:")
debuffDur_label.grid(row=3, column=0,sticky="w")

MDR_entry = tkinter.Entry(draw_opp_frame)
MDR_entry.grid(row=0, column=1)

projRes_entry = tkinter.Entry(draw_opp_frame)
projRes_entry.grid(row=1, column=1)

hsRes_entry = tkinter.Entry(draw_opp_frame)
hsRes_entry.grid(row=2, column=1)

debuffDurr_entry = tkinter.Entry(draw_opp_frame)
debuffDurr_entry.grid(row=3, column=1)

headshot_label = tkinter.Label(draw_opp_frame, text="Headshot")
headshot_combobox = ttk.Combobox(draw_opp_frame, values=["Uh, duh. I'm a gamer", "No"])
headshot_label.grid(row=4, column=0,sticky="w")
headshot_combobox.grid(row=4, column=1)

#Defaults
MDR_entry.insert(0, 0)
projRes_entry.insert(0, 0)
hsRes_entry.insert(0, 0)
debuffDurr_entry.insert(0, 0)
headshot_combobox.insert(0, "No")

#Enhancement input
book_label = tkinter.Label(draw_info_frame, text="Casting Implement Damage:")
book_label.grid(row=0, column=0,sticky="w")

add_label = tkinter.Label(draw_info_frame, text="Additional Magic Damage:")
add_label.grid(row=1, column=0,sticky="w")

true_label = tkinter.Label(draw_info_frame, text="Additional True Magic Damage:")
true_label.grid(row=2, column=0,sticky="w")

mpb_label = tkinter.Label(draw_info_frame, text="Magic Power Bonus %:")
mpb_label.grid(row=3, column=0,sticky="w")

book_entry = tkinter.Entry(draw_info_frame)
book_entry.grid(row=0, column=1)

add_entry = tkinter.Entry(draw_info_frame)
add_entry.grid(row=1, column=1)

true_entry = tkinter.Entry(draw_info_frame)
true_entry.grid(row=2, column=1)

mpb_entry = tkinter.Entry(draw_info_frame)
mpb_entry.grid(row=3, column=1)

spell_label = tkinter.Label(draw_info_frame, text="Spell")
spell_combobox = ttk.Combobox(draw_info_frame, values=["Ignite", "Zap", "Magic Missile", "Ice Bolt", "Explosion", "Fireball (Splash)", "Fireball (Direct)", "Lightning Strike", "Chain Lightning"])
spell_label.grid(row=4, column=0)
spell_combobox.grid(row=4, column=1)

#inserting defaults 
book_entry.insert(0, 5)
add_entry.insert(0, 0)
true_entry.insert(0, 11)
mpb_entry.insert(0, 22)
spell_combobox.insert(0, "Zap")

for widget in draw_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5) 

for widget in draw_opp_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5) 

#button
button = tkinter.Button(frame, text="Calculate", command= generate_graph)
button.grid(row=4, column= 0, sticky="news", padx=20, pady=20)

#display 
disp = tkinter.Message(frame)
disp.grid(row=4, column= 1, sticky="news", padx=20, pady=20)

window.mainloop()
