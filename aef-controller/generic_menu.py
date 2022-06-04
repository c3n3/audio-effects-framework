# Import module
import json
from textwrap import fill
import tkinter as tk
from turtle import title
from local_interface import LocalInterface

controller = LocalInterface()


controller.init()

# Create object
root = tk.Tk()
  
# Adjust size
root.geometry( "400x400" )

# Dropdown menu options
# commands = {
#     'type1': {
#         'command0': {'input_type':'button', 'id': '1'},
#         'command1': {'input_type': 'button', 'id': '1'}
#     },
#     'type2': {
#         'command2': {'input_type': 'encoder', 'id': '1'}
#     },
#     'presets': {
#         'test': {'id': '1', 'input_type': 'button', 'path': '../temp/'},
#         'another.txt': {'id': '1', 'input_type': 'button', 'path': '../temp/'}
#     },
#     'type3': {
#         'TEST1': {'input_type': 'button', 'id': '4'},
#         'TEST2': {'input_type': 'button', 'id': '5'}
#     },
#     'type4': {
#         'TEST3': {'input_type': 'encoder', 'id': '1'}
#     }
# }

inputData = controller.getInputs()

buttons = {}

def getName(arr, name):
    for x in arr:
        if x["name"] == name:
            return x

for b in inputData:
    buttons[b["name"]] = tk.StringVar()

def buttonChange(*args):
    var = args[0]
    val = args[1]
    print(args)


#encoder delete function
def changeButton(button, value):
    def sub_function():
        controller.update(button, value)
        print("Changing '" + button + "' to '" + value + "'")
    return sub_function

def sync(*args):
    createButtons(bottom, controller.getCommnds())

def createButtons(parent, commands):
    i = 0
    j = 0
    for w in parent.winfo_children():
        w.destroy()
    for button in buttons.keys():
        # Create Dropdown menu
        # Create Label
        frame = tk.Frame(
                master=parent,
                relief=tk.RAISED,
                borderwidth=1
        )
        frame.grid(row=j, column=i, sticky="news")
        menuButton = tk.Menubutton(frame, text=button, underline=0)
        menuButton.pack(expand=True, fill="both", side=tk.BOTTOM)
        menu = tk.Menu(menuButton)
        for type in commands.keys():
            count = 0
            commandMenu = tk.Menu(menu, tearoff=0)
            for command in commands[type].keys():
                if (commands[type][command]["input_type"] == getName(inputData, button)["type"]):
                    commandMenu.add_command(label=command, command=changeButton(button, command))
                    count += 1
            if (count != 0):
                menu.add_cascade(label=type, menu=commandMenu)
        menuButton.config(menu=menu)
        parent.columnconfigure(i, weight=1)
        i += 1
        if (i == 1):
            parent.rowconfigure(j, weight=1)
            i = 0
            j += 1

# top = tk.Frame(
#         master=root,
#         relief=tk.RAISED,
#         borderwidth=1
# )
# top.pack(row=0, column=0)
# root.rowconfigure(0, weight=0)



scLeft = tk.Scrollbar(root)
scLeft.pack( side = tk.LEFT, fill = tk.Y )

mylist = tk.Listbox(root, yscrollcommand = scLeft.set )
for line in range(100):
   mylist.insert(tk.END, "This is line number " + str(line))

mylist.pack( side = tk.LEFT, fill = tk.BOTH )
scLeft.config( command = mylist.yview )


scrollbar = tk.Scrollbar(root)
scrollbar.pack( side = tk.RIGHT, fill = tk.Y )

mylist = tk.Listbox(root, yscrollcommand = scrollbar.set )
for line in range(50):
   mylist.insert(tk.END, "This is " + str(line))

mylist.pack( side = tk.LEFT, fill = tk.BOTH )
scrollbar.config( command = mylist.yview )


# bottom = tk.Scrollbar(
#         master=root,
#         relief=tk.RAISED,
#         borderwidth=1
# )

# bottom.grid(row=1, column=0)
# root.rowconfigure(1, weight=1)

# createButtons(bottom)

for b in buttons.keys():
    buttons[b].set("None")
    buttons[b].trace("w", buttonChange)

# datatype of menu text
clicked = tk.StringVar()

 
# initial menu text
clicked.set( "Monday" )

i = 0
j = 0

# sync()

# Execute tkinter
root.mainloop()

controller.close()
