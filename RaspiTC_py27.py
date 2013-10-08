#!/usr/bin/python
'''        
Created on Sep 25, 2013

@author: matthassel

This app provides a gui session to a backend of xfreerpd. 
'''

from Tkinter import *
from PIL import Image, ImageTk
import os, ConfigParser, tkMessageBox

class App:
    def __init__(self, master):
        image = Frame(master)
        image.grid(row=1, columnspan=4, sticky=E+W+N+S)
        frame = Frame(master)
        frame.grid(row=2, columnspan=4, sticky=E+W+N+S)
        status = Frame(master)
        status.grid(row=3, columnspan=4, stick=E+W+N+S)
        
        #Logo Display Image Setup
        self.image = Image.open("/home/pi/RaspiPyThinClient/raspirdp.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        self.my_photo = Label(image, image=self.photo)
        self.my_photo.grid(stick=E+W+N+S)
        
        #hostname label
        self.hostname = Label(frame, text="Hostname:")
        self.hostname.grid(row=0, column=0, stick=W)
        #hostname entry
        self.hostname_entry = Entry(frame, width=58, relief=SUNKEN, bg="white")
        self.hostname_entry.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.hostname_entry.focus()
        
                
        self.username =  Label(frame, text="Username:")
        self.username.grid(row=2,column=0,stick=W)
        
        self.username_entry = Entry(frame, relief=SUNKEN, bg="white")
        self.username_entry.grid(row=2, column=0, sticky=E, pady=0)
        
        self.password = Label(frame, text="Password:")
        self.password.grid(row=3, column=0, stick=W)
               
        self.password_entry = Entry(frame, show="*", relief=SUNKEN, bg="white")
        self.password_entry.grid(row=3, column=0, sticky=E, pady=0)
        
        self.help = Label(frame, text="RDP Permissions Required")
        self.help.grid(row=5, column=0, sticky=W)
        
        self.about = Button(frame, text="About", command=self.about,
                            width=10)
        self.about.grid(row=2, column=1)
        
        self.connect = Button(frame, text="Connect",
                              command=self.session_connect,
                              width=10)
        self.connect.grid(row=3, column=1)
        
        self.cancel = Button(frame, text="Cancel", fg="red",
                             command=self.session_cancel,
                             width=10)
        self.cancel.grid(row=4, column=1)
        
        self.status = StatusBar(status)
        self.status.pack(fill=X)
        
    def window_preferences(self, w=300, h=200, title=None):
        # get screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # set root window title
        root.title(title)
        root.resizable(0, 0)
    
    def close_handler(self):
        self.session_cancel()
        self.clear_entry()
        pass
        
    def about(self):
        message = """
        Raspi RDP Client
        Version: 1.0
        Support: fedusrlive@yahoo.com
        
        ***RDP Permissions Required.***
        """
        tkMessageBox.showinfo("Raspi RDP Client - About", message)
                        
    def session_connect(self):
        hostname = self.hostname_entry.get()
        if hostname == "admin":
            self.enable_mouse()
            return
        if hostname == "prod":
            self.disable_mouse()
            return
        username = self.username_entry.get()
        password = self.password_entry.get()
        if hostname == "" or username == "" or password == "":
            tkMessageBox.showerror("Invalid Entry", "Check session info and try again.")
            return
        self.rdpSession = rdpSession()
        self.rdpSession.rdpconnect(hostname, username, password)
        #self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        pass    
    
    def session_cancel(self):
        self.clear_entry()
        
    def quit(self):
       self.root.destroy()
       
    def disable_mouse(self):
        os.system("bash /home/pi/RaspiPyThinClient/mouse_map on")
        self.clear_entry()
        
    def enable_mouse(self):
        os.system("bash /home/pi/RaspiPyThinClient/mouse_map off")
        self.clear_entry()
        
    def clear_entry(self):
        string = "Cleared"
        self.hostname_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.status.set("%s", string)
        
class StatusBar(Frame):

        def __init__(self, master):
            Frame.__init__(self, master)
            self.label = Label(self, bd=1, relief=FLAT, anchor=W)
            self.label.pack(fill=X)
    
        def set(self, format, *args):
            self.label.config(text=format % args)
            self.label.update_idletasks()
    
        def clear(self):
            self.label.config(text="")
            self.label.update_idletasks()
            
class rdpSession:
    """Setup the environment to connect to a RDP session"""
    
    def __init__(self):     
        self.config = ConfigParser.ConfigParser()
        self.config.read('/home/pi/RaspiPyThinClient/RaspiTC_config.ini')
        self.RDPBinary = self.config.get("DEFAULT", "RDPBinary")
        self.RDPDomain = self.config.get("DEFAULT", "RDPDomain")
        self.RDPDomainFlags = self.config.get("DEFAULT", "RDPDomainFlags")
        self.RDPUserFlags = self.config.get("DEFAULT", "RDPUserFlags")
        self.RDPPasswordFlags = self.config.get("DEFAULT", "RDPPasswordFlags")
        self.RDPResolutionFlags = self.config.get("DEFAULT", "RDPResolutionFlags")
        self.RDPSoundRedirectFlags = self.config.get("DEFAULT", "RDPSoundRedirectFlags")
        self.RDPHostnameFlags = self.config.get("DEFAULT", "RDPHostnameFlags")
        self.RDPDefaultFlags = self.config.get("DEFAULT", "RDPDefaulfFlags")
    
    def makecommand(self, hostname="", username="", password=""):
        #self.hostname = self.RDPHostnameFlags + ' ' + hostname + ' '
        self.hostname = hostname
        self.username = self.RDPUserFlags + ' ' + username + ' '
        self.password = self.RDPPasswordFlags + ' ' + password + ' '
        self.ignore = self.RDPDefaultFlags + ' '
        self.domain = self.RDPDomainFlags + ' ' + self.RDPDomain + ' '
        self.binary = self.RDPBinary + ' '
        self.flags = self.RDPSoundRedirectFlags + ' '
        self.resolution = self.RDPResolutionFlags + ' '
        self.commandline = self.binary + self.flags + self.resolution + \
        self.ignore + self.domain + self.username + self.password + self.hostname
        return self.commandline
        
        
    def rdpconnect(self, hostname, username, password):
        call = self.makecommand(hostname, username, password)
        #print(call)
        os.system(call)     
        
        
root = Tk()
root.update_idletasks()
app = App(root)
app.window_preferences(w=482, h=220, title="Raspi RDP Client")
root.protocol("WM_DELETE_WINDOW", app.close_handler) # used so the app cannot be closed.
root.mainloop()