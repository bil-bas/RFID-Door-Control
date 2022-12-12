from __future__ import absolute_import, print_function, division, unicode_literals

from Tkinter import *
import ConfigParser
import requests
from DoorInterfaceNoDb import DoorInterface
import RPi.GPIO as GPIO
import binascii


class CardGui:

    def __init__(self, path):
        self.config = ConfigParser.ConfigParser()
        self.config_path = path
        self.config.read(path)
        self.tk = Tk()
        self.tk.title("LAMM RFID")
        self.tk.geometry("250x600")
        self.url = self.config.get('fetch', 'endpoint')
        self.door = self.config.get('main', 'door')
        self.key = self.config.get('fetch', 'api_key')
        self.cards = []
        self.dialog = None
        self._interface = None

    def run(self):
        self.init()
        self.tk.after(100, self.fetch_data)
        self.tk.mainloop()

    def init(self):
        self.label_title()
        self.button_refresh()
        self.listbox_cards()
        self.button_write()
        self.button_read()

    def label_title(self):
        title = Label(self.tk, text="Select a Card/Fob to Write")
        title.pack()

    def fetch_data(self):
        r = requests.get(self.url, params={'door': self.door, 'key': self.key}, verify=False)
        data = r.json()
        self.cards = data['allowed_card']
        self.list_var.set(tuple(c["user_name"] for c in self.cards))

    def callback_refresh(self):
        print("Refreshing!")
        self.fetch_data()

    def button_refresh(self):
        button = Button(self.tk, text="Refresh", command=self.callback_refresh)
        button.pack()

    def callback_write(self):
        print("Writing")
        card = self.current_card
        print("Writing Card for ", self.describe_card(card))
        self.msg_box("Notice", "Place Card/Fob on RFID writer", False)
        self.tk.after(100, self.background_write)

    def describe_card(self, card):
        return card['user_name'] + "User: " + str(card["user_id"]) + "Card: " + card["card_key"]

    @property
    def current_card(self):
        card_index = self.list_view.index(ACTIVE)
        return self.cards[card_index]

    @property
    def interface(self):
        if self._interface is None:
            self._interface = DoorInterface(self.config_path)
            self._interface.print_reader_version()
        return self._interface

    def background_write(self):
        uid = self.interface.read_card_id()
        if uid is None:
            self.tk.after(100, self.background_write)
            return

        print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        
        if self.interface.set_key(uid):
            print("Set new card key")
        else:
            print("Card key already set")
            
        uid = self.interface.read_card_id()  
       
        print("Writing card for", self.describe_card(self.current_card))
        if self.interface.set_id(uid, self.curent_card['card_key']):
            self.msg_box("Success", "Wrote id correctly")
        else:
            self.msg_box("Warning", "Failed to write card?!?!")

    def button_write(self):
        self.write_button = Button(self.tk, text="Write", command=self.callback_write, state=DISABLED)
        self.write_button.pack()

    def button_read(self):
        button = Button(self.tk, text="Read", command=self.callback_read)
        button.pack()

    def callback_read(self):
        print("reading")
        self.msg_box("Notice", "Place Card/Fob on RFID reader", False)
        self.tk.after(100, self.background_read)

    def background_read(self):
        uid = self.interface.read_card_id()
        if uid is None:
            self.tk.after(100, self.background_read)
            return

        print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))

        id = self.interface.get_id(uid)
        card_key = binascii.hexlify(id)
        for card in self.cards:
            if card["card_key"] == card_key:
                print("Card for ", self.describe_card(card))
                self.msg_box("Success", "Card is for " + card["user_name"])
                return

        self.msg_box("Success", "Card is not set for a recognised user")
    
    def listbox_cards(self):
        self.list_var = StringVar()
        self.list_view = Listbox(self.tk, listvariable=self.list_var)
        self.list_view.pack(expand=True, fill="both", padx=(16, 16), pady=(16, 16))
        self.list_view.bind("<<ListboxSelect>>", self.list_item_selected)

    def list_item_selected(self, event):
        self.write_button["state"] = NORMAL

    def msg_box(self, title, msg, show_button=True):
        self.close_msg_box()
       
        self.dialog = Toplevel(self.tk)
        self.dialog.grab_set()
        self.dialog.title(title)
        Label(self.dialog, text=msg).pack()
        if show_button:
            Button(self.dialog, text="Dismiss", command=self.close_msg_box).pack()
            
    def close_msg_box(self):
        if self.dialog is not None:
            try:
                self.dialog.destroy()
            except Exception as ex:
                print(ex)
            self.dialog = None
