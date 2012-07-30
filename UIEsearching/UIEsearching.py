#!/usr/bin/env python
import os
import Esearching as e
import gtk

from string import join
from time import sleep

class Settings():
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, title, width, height):
        # Drawing window
        self.window = gtk.Window()
        self.window.set_resizable(True)
        self.window.set_title(title)
        self.window.set_default_size(width, height)
        self.window.set_border_width(10)
        self.window.connect('delete_event', self.delete_event)

        box = gtk.VBox(False, 5)
        self.window.add(box)
        box.show()

        # For textview
        box1 = gtk.VBox(False, 5)
        box.pack_start(box1, True, True, 0)

        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview = gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        self.sw.add(self.textview)
        box1.pack_start(self.sw, True, True, 0)

        # For settings
        box2 = gtk.VBox(False, 5)
        box.pack_start(box2, False, False, 0)

        self.fixed = gtk.Fixed()
        self.label = gtk.Label('Search UI Element:')

        self.app_label = gtk.Label('Application Name:')
        self.app_entry = gtk.Entry()
        self.app_entry.set_max_length(20)

        self.ele_label = gtk.Label('Element Name:')
        self.ele_entry = gtk.Entry()
        self.ele_entry.set_max_length(20)

        self.ctrl_label = gtk.Label('Control Name:')
        store = gtk.ListStore(str)
        self.ctrl_combo = gtk.ComboBoxEntry(store)
        self.ctrl_combo.insert_text(0, "application")
        self.ctrl_combo.insert_text(1, "push button")
        self.ctrl_combo.insert_text(2, "label")
        self.ctrl_combo.insert_text(3, "menu")
        self.ctrl_combo.insert_text(4, "menu item")
        self.ctrl_combo.insert_text(5, "dialog")
        self.ctrl_combo.insert_text(6, "text")
        self.ctrl_combo.insert_text(7, "tool bar")
        self.ctrl_combo.insert_text(8, "combo box")
        self.ctrl_combo.insert_text(9, "radio button")
        self.ctrl_combo.insert_text(10, "frame")
        self.ctrl_combo.insert_text(11, "tool bar")
        self.ctrl_combo.set_active(0)

        self.find_label = gtk.Label('Find Type:')
        self.findall_radio = gtk.RadioButton(None, 'findAll')
        self.find_radio = gtk.RadioButton(self.findall_radio, 'find')

        self.child_label = gtk.Label('Show Children:')
        self.no_radio = gtk.RadioButton(None, 'No')
        self.yes_radio = gtk.RadioButton(self.no_radio, 'Yes')
        store = gtk.ListStore(str)
        self.child_combo = gtk.ComboBox(store)
        cell = gtk.CellRendererText()
        self.child_combo.pack_start(cell, True)
        self.child_combo.add_attribute(cell, 'text', 0)
        self.child_combo.insert_text(0, "0")
        self.child_combo.insert_text(1, "1")
        self.child_combo.insert_text(2, "2")
        self.child_combo.set_active(0)

        self.fixed.put(self.label, 20, 20)
        self.fixed.put(self.app_label, 20, 60)
        self.fixed.put(self.app_entry, 140, 60)
        self.fixed.put(self.ele_label, 20, 100)
        self.fixed.put(self.ele_entry, 140, 100)
        self.fixed.put(self.ctrl_label, 20, 140)
        self.fixed.put(self.ctrl_combo, 140, 140)
        self.fixed.put(self.find_label, 20, 180)
        self.fixed.put(self.findall_radio, 140, 180)
        self.fixed.put(self.find_radio, 240, 180)
        self.fixed.put(self.child_label, 20, 220)
        self.fixed.put(self.no_radio, 140, 220)
        self.fixed.put(self.yes_radio, 240, 220)
        self.fixed.put(self.child_combo, 320, 220)
        box2.pack_start(self.fixed)

        # For Buttons
        layout = gtk.Layout()

        self.button1 = gtk.Button('Search')
        self.button2 = gtk.Button('Quit')
        self.button3 = gtk.Button('Help')
        self.button4  = gtk.Button('Preferences')

        self.button1.connect('clicked', self.OnButton1, 'Search')
        self.button2.connect('clicked', self.OnButton2, 'Quit')
        self.button3.connect('clicked', self.OnButton3, 'Help')
        self.button4.connect('clicked', self.OnButton4, 'Preferences')

        layout.put(self.button1, 400, 20)
        layout.put(self.button2, 460, 20)
        layout.put(self.button3, 500, 20)
        layout.put(self.button4, 20, 20)
        box.pack_start(layout)

        self.window.show_all()

    def argument_set(self):
        # Searching variables
        self.appname = self.app_entry.get_text()
        if len(self.appname) == 0:
            self.appname = None

        if not self.findall_radio.get_active():
            self.findtype = 'find' 
        else:
            self.findtype = 'findAll' 
          
        self.ctrl_active = self.ctrl_combo.get_active()
        self.ctrlname = self.ctrl_combo.get_model()[self.ctrl_active][0]

        self.elementname = self.ele_entry.get_text()
        if len(self.elementname) == 0:
            self.elementname = None

        if self.no_radio.get_active():
            self.list_children = None
        elif self.yes_radio.get_active():
            self.child_active = self.child_combo.get_active()
            self.list_children = int(self.child_combo.get_model()[self.child_active][0])

        return  self.findtype, self.appname, self.ctrlname, self.elementname, self.list_children

    def OnButton1(self, widget, data):
        self.argument_set()

        s = e.Searching(self.findtype, self.appname, self.ctrlname, self.elementname, self.list_children)
        info = s.run()

        if not info:
            self.textbuffer.set_text("UIEsearching: Nothing found! Try again!")
        else:
            self.textbuffer.set_text('\r\n'.join(map(str,info)))

    def OnButton2(self, widget, data):
        self.delete_event(self.window, None)

    def OnButton3(self, widget, data):
        # Draw window to show README
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Help")
        window.set_default_size(600, 600)
        window.set_border_width(10)

        vbox = gtk.VBox()
        window.add(vbox)

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        textview.set_editable(False)
        textbuffer = textview.get_buffer()
        sw.add(textview)

        info = open('README', 'r')
        if info:
            string = info.read()
            textbuffer.set_text(string)
            info.close()

        vbox.pack_start(sw)
        window.show_all() 

    def OnButton4(self, widget, data):
        dialog = gtk.Dialog(title="Preferences",
                                 flags=gtk.DIALOG_MODAL)
        # Accessibility status setup
        hbox = gtk.HBox()
        dialog.vbox.pack_start(hbox)

        label = gtk.Label('accessibility status: ')
        hbox.pack_start(label, False, False, 0)
        label1 = gtk.Label('')
        hbox.pack_start(label1, False, False, 10)
        acc_button = gtk.Button('Enabled')
        hbox.pack_start(acc_button, True, True, 10)

        acc_status = e.acc_status()
        label1.set_label(acc_status)
        if acc_status == 'true':
            acc_button.set_sensitive(False)

        def OnAccButton(widget, data):
            e.acc_active('true')

            if e.acc_status() == 'true':
                label1.set_label('true')
                acc_button.set_sensitive(False)

        acc_button.connect('clicked', OnAccButton, 'Enabled')

        # at-spi-registryd process setup
        hbox1 = gtk.HBox()
        dialog.vbox.pack_start(hbox1)

        label = gtk.Label('at-spi-registryd process: ')
        hbox1.pack_start(label, False, False, 0)
        label2 = gtk.Label('')
        hbox1.pack_start(label2, False, False, 10)
        spi_button = gtk.Button('Enabled')
        hbox1.pack_start(spi_button, True, True, 10)

        spi_status = e.spi_status()
        label2.set_label(spi_status)
        if spi_status == 'running':
            spi_button.set_sensitive(False)

        def OnSpiButton(widget, data):
            e.spi_active()

            if e.spi_status() == 'running':
                label2.set_label('running')
                spi_button.set_sensitive(False)

        spi_button.connect('clicked', OnSpiButton, 'Enabled')

        dialog.add_button("Close", gtk.RESPONSE_CLOSE)
        dialog.set_border_width(20)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    Settings('UI Element Searching', 600, 480)    
    gtk.main()
