import PIL.ImageDraw
import requests
import pandas as pd
from colormap import rgb2hex
import PySimpleGUI as sg
import tkmacosx
import tkinter.ttk as ttk
# from window import Figma_window

code = open("code.txt", 'a')
lines = []

from tkinter import *
window = Tk()

def btnClicked():
    print("hey")


lines.extend(['from tkinter import *','window = Tk()\n','def btnClicked():','    print("hey")'])

def get_color(element):
    el_r = element["fills"][0]["color"]['r'] * 255
    el_g = element["fills"][0]["color"]['g'] * 255
    el_b = element["fills"][0]["color"]['b'] * 255
    hex = rgb2hex(round(el_r), round(el_g), round(el_b))
    return hex

def get_cordinates(element):
    x = int(element["absoluteBoundingBox"]["x"])
    y = int(element["absoluteBoundingBox"]["y"])
    return x,y

def get_dimensions(element):
    height = int(element["absoluteBoundingBox"]["height"])
    width = int(element["absoluteBoundingBox"]["width"])
    return width,height

def get_text_properties(element):
    font = element["style"]["fontPostScriptName"]
    fontSize = element["style"]["fontSize"]
    return font,fontSize

###################### Getting File Data #######################
token = "189541-e5791cc9-4619-411e-b4b1-6b6f7d285d68"
fileId = "8K2eByUz9tLasBT5sOFSzJ"
response = requests.get("https://api.figma.com/v1/files/8K2eByUz9tLasBT5sOFSzJ", headers={"X-FIGMA-TOKEN": token})

with open("js.json",'w') as js:
    js.write(response.text)

data = pd.read_json("js.json")

####################### Accesing Window Properties #######################
fig_window = data["document"]["children"][0]['children'][0]

####################### Getting Window Dimensions #######################
window_cordinates = fig_window["absoluteBoundingBox"]
window_width = int(window_cordinates["width"])
window_height = int(window_cordinates["height"])

####################### Getting Window Background Color #######################
window_color = fig_window["fills"][0]["color"]
window_color_r = window_color['r'] * 255
window_color_g = window_color['g'] * 255
window_color_b = window_color['b'] * 255
window_bg_hex = rgb2hex(round(window_color_r), round(window_color_g), round(window_color_b))

####################### Creating Window #######################

window.geometry(f"{window_width}x{window_height}")
window.configure(bg=window_bg_hex)
canvas = Canvas(window,bg=window_bg_hex,height=window_height,width=window_width,bd=0, highlightthickness=0,relief="ridge")
canvas.pack()
lines.extend([f'\nwindow.geometry("{window_width}x{window_height}")',f'window.configure(bg="{window_bg_hex}")',f'canvas = Canvas(window,bg="{window_bg_hex}",height={window_height},width={window_width},bd=0, highlightthickness=0,relief="ridge")','canvas.pack()'])

####################### Getting Elements inside Window #######################
window_elements = fig_window["children"]

btn_count = 0
for element in window_elements:

    if element["name"] == 'Rectangle':
        rec_width, rec_height = get_dimensions(element)
        x, y = get_cordinates(element)
        element_color = get_color(element)

        canvas.create_rectangle(x, y, x + rec_width, y + rec_height, fill=element_color)

        lines.extend([f'\ncanvas.create_rectangle({x}, {y}, {x} + {rec_width}, {y} + {rec_height}, fill="{element_color}")'])

    elif element["name"] == 'Button':

        rec_width, rec_height = get_dimensions(element)
        x, y = get_cordinates(element)
        element_color = get_color(element["children"][0])
        btn_text = element["children"][len(element["children"]) - 1]["characters"]
        btn_id = element["id"]
        response = requests.get(f"https://api.figma.com/v1/images/8K2eByUz9tLasBT5sOFSzJ?ids={btn_id}",
                                headers={"X-FIGMA-TOKEN": "189543-60e9c4f6-7b8c-4fc1-b682-586c2fb8a0e7"})
        res = requests.get(response.json()["images"][btn_id])

        with open(f"img{btn_count}.png", "wb") as file:
            file.write(res.content)

        img = PhotoImage(file=f"img{btn_count}.png")

        b = Button(image=img, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")
        b.place(x=x, y=y, width=rec_width, height=rec_height)

        lines.extend([f'\nimg{btn_count} = PhotoImage(file=f"img{btn_count}.png")',f'b{btn_count} = Button(image=img{btn_count}, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")',f'b{btn_count}.place(x={x}, y={y}, width={rec_width}, height={rec_height})\n'])
        btn_count += 1

    elif element["type"] == 'TEXT':
        text = element["characters"]
        x,y = get_cordinates(element)
        width,height = get_dimensions(element)
        color = get_color(element)
        font,fontSize = get_text_properties(element)
        x,y = x + (width/2), y + (height/2)
        canvas.create_text(x,y,text=text,fill=color,font=(font,int(fontSize)))
        lines.extend([f'canvas.create_text({x},{y},text="{text}",fill="{color}",font=("{font}",int({fontSize})))'])

# for i in lines:
#     print(i)

window.mainloop()