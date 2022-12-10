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
        self.tk.geometry("250x600")
        self.url = self.config.get('fetch', 'endpoint')
        self.door = self.config.get('main', 'door')
        self.key = self.config.get('fetch', 'api_key')
        self.cards = []
        self.dialog = None
     
    def run(self):
        self.init()
        self.tk.after(100, self.fetch_data)
        self.tk.mainloop()

    def init(self):
        self.label_title()
        self.button_refresh()
        self.listbox_cards()
        self.button_write()

    def label_title(self):
        title = Label(self.tk, text="Select a Card/Fob to Write")
        title.pack()

    def fetch_data(self):
        r = requests.get(self.url, params = {'door': self.door, 'key': self.key}, verify=False)
        data = r.json()
        self.cards = data['allowed_card']
        self.list_var.set(tuple(c["user_name"] for c in self.cards))

    def callback_refresh(self):
        print "Refreshing!"
        self.fetch_data()

    def button_refresh(self):
        button = Button(self.tk, text="Refresh", command=self.callback_refresh)
        button.pack()

    def callback_write(self):
        print "Writing"

        card_index = self.list_view.index(ACTIVE)
        self.card = self.cards[card_index]
        print "Writing Card for {}, User: {}, Card: {}".format(card['user_name'], self.card["user_id"], self.card["card_key"])
        self.msg_box("Notice", "Place Card/Fob on reader", False)
        self.tk.after(100, self.background_write)
    
    def background_write(self):
        interface = DoorInterface(self.config_path)
        interface.print_reader_version()
        
        uid = interface.read_card_id()
        if uud is None:
            self.tk.after(100, self.background_write)
            return

        print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))
        
        if interface.set_key(uid):
            print "Set new card key"
        else:
            print "Card key already set"
            
        if interface.read_id_block(uid):
            print "Writing card with new user id"
            if interface.set_id(uid, card['card_key']):
                self.msg_box("Success", "Wrote id correctly")
            else:
                self.msg_box("Warning", "Failed to write card?!?!")
        else:
            self.msg_box("Warning", "Possible new card, flash new first")        

    def button_write(self):
        button = Button(self.tk, text="Write", command=self.callback_write, state=DISABLED)
        button.pack()
    
    def listbox_cards(self):
        self.list_var = StringVar()
        self.list_view = Listbox(self.tk, listvariable=self.list_var)
        self.list_view.pack(expand=True, fill="both", padx=(16, 16), pady=(16, 16))
        self.list_view.bind("<<ListboxSelect>>", lambda: self.button_write["state"] = NORMAL)

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
                print ex
            self.dialog = None
