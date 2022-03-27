# Import module
from textwrap import fill
import tkinter as tk
from turtle import title
from server import BluetoothServer

server = BluetoothServer()

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

buttons = {
    "B1": tk.StringVar(),
    "B2": tk.StringVar(),
    "B3":  tk.StringVar(),
    "B4":  tk.StringVar(),
    "B5":  tk.StringVar(),
    "B6":  tk.StringVar(),
    "B7":  tk.StringVar(),
    "B8":  tk.StringVar()
}

def buttonChange(*args):
    var = args[0]
    val = args[1]
    print(args)


#encoder delete function
def changeButton(button, value):
    def sub_function():
        server.updateCommand(button, value)
        print("Changeing '" + button + "' to '" + value + "'")
    return sub_function

def sync(*args):
    server.sync()
    createButtons(bottom, server.commands)

def connect():
    print("Connecting to ", bluetoothValue.get())
    server.connect(BluetoothServer.devices[bluetoothValue.get()])

def setBluetooth(value):
    def subFunction():
        bluetoothValue.set(value)
    return subFunction

def refresh():
    BluetoothServer.lookUpNearbyBluetoothDevices()
    bluetoothMenu["menu"].delete(0, "end")
    for key in BluetoothServer.devices:
        bluetoothMenu["menu"].add_command(label=key, command=setBluetooth(key))

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
        menuButton.pack(expand=True, fill="both")
        menu = tk.Menu(menuButton)
        for type in commands.keys():
            commandMenu = tk.Menu(menu, tearoff=0)
            for command in commands[type].keys():
                commandMenu.add_command(label=command, command=changeButton(button, command))
            menu.add_cascade(label=type, menu=commandMenu)
        menuButton.config(menu=menu)
        parent.columnconfigure(i, weight=1)
        i += 1
        if (i == 4):
            parent.rowconfigure(j, weight=1)
            i = 0
            j += 1

top = tk.Frame(
        master=root,
        relief=tk.RAISED,
        borderwidth=1
)
top.grid(row=0, column=0)
root.rowconfigure(0, weight=0)

button = tk.Button(top, command=sync, text="Sync")
button.pack(side=tk.LEFT)


button = tk.Button(top, command=connect, text="Connect")
button.pack(side=tk.RIGHT)

button = tk.Button(top, command=refresh, text="Refresh")
button.pack(side=tk.RIGHT)


devs = ["think", "Caden"]

bluetoothValue = tk.StringVar(value="Select")
bluetoothMenu = tk.OptionMenu(top, bluetoothValue, *devs)
bluetoothMenu.pack(side=tk.RIGHT)


bottom = tk.Frame(
        master=root,
        relief=tk.RAISED,
        borderwidth=1
)
bottom.grid(row=1, column=0)
root.rowconfigure(1, weight=1)

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





# Execute tkinter
root.mainloop()

server.close()
