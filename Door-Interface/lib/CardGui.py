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
        self.url = self.config.get('fetch', 'endpoint')
        self.door = self.config.get('main', 'door')
        self.key = self.config.get('fetch', 'api_key')
        self.cards = []
        self.dialog = None

    def run(self):
        self.init()
        self.fetch_data()
        self.tk.mainloop()

    def init(self):
        self.label_title()
        self.button_refresh()
        self.listbox_cards()
        self.button_write()
        self.button_flash()

    def label_title(self):
        title = Label(self.tk, text="Select a Card to Write")
        title.pack()

    def fetch_data(self):
        r = requests.get(self.url, params = {'door': self.door, 'key': self.key}, verify=False)
        data = r.json()
        self.cards = data['allowed_card']
        self.load_cards()

    def callback_refresh(self):
        print "Refreshing!"

        self.fetch_data()

    def button_refresh(self):
        button = Button(self.tk, text="Refresh", command=self.callback_refresh)
        button.pack()

    def callback_write(self):
        print "Writing"

        card_index = self.list_view.index(ACTIVE)
        if card_index is None:
            self.msg_box("Warning", "Select an ID first")
            return

        card = self.cards[card_index]
        print "Writing Card for", card['user_name']

        interface = DoorInterface(self.config_path)
        interface.print_reader_version()

        self.msg_box("Notice", "Place Card on reader", False)

        uid = None
        while uid is None:
            uid = interface.read_card_id()

            if uid is not None:
                print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))
                if interface.read_id_block(uid):
                    print "Writing card with new key"
                    if interface.set_id(uid, card['card_key']):
                        self.msg_box("Success", "Wrote id correctly")
                    else:
                        self.msg_box("Warning", "Failed to write card?!?!")
                else:
                    self.msg_box("Warning", "Possible new card, flash new first")

    def callback_flash(self):
        interface = DoorInterface(self.config_path)
        interface.print_reader_version()

        self.msg_box("Notice", "Place Card on reader", False)

        uid = None
        while uid is None:
            uid = interface.read_card_id()

            if uid is not None:
                print 'Found card with UID: 0x{0}'.format(binascii.hexlify(uid))
                if interface.set_key(uid):
                    self.msg_box("Success", "Set new key")
                else:
                    self.msg_box("Warning", "failed to set key, non-blank card?")

    def button_write(self):
        button = Button(self.tk, text="Write", command=self.callback_write)
        button.pack()

    def button_flash(self):
        button = Button(self.tk, text="Flash Key", command=self.callback_flash)
        button.pack()

    def load_cards(self):
        self.list_view.delete(0, END)
        for item in self.cards:
            self.list_view.insert(END, item['user_name'])

    def listbox_cards(self):
        self.list_view = Listbox(self.tk)
        self.list_view.pack()

    def msg_box(self, title, msg, show_button=True):
        self.close_msg_box()
        
        self.dialog = Toplevel()
        self.dialog.title(title)
        Label(self.dialog, text=msg).pack()
        if show_button:
            Button(self.dialog, text="Dismiss", command=self.close_msg_box).pack()
            
    def close_msg_box():
        if self.dialog is not None:
            try:
                self.dialog.close()
            except:
                pass
            self.dialog = None
