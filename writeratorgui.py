#!/usr/bin/env python3

# Copyright 2012 Bill Tyros
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
import tkinter.messagebox as mb

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.createTopMenu()
    
    def createTopMenu(self):
        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top["menu"] = self.menuBar
    
        self.FileMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="File", menu=self.FileMenu)
        self.FileMenu.add_cascade(label="Save")
        self.FileMenu.add_cascade(label="Exit")
        
        self.HelpMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label="Help", menu=self.HelpMenu)
        self.HelpMenu.add_cascade(label="How-To", command=self.popUpHowTo())
        self.HelpMenu.add_cascade(label="About", command=self.popUpAbout())
    
    def popUpAbout(self):
        mb.showinfo("About", "Writerator coded by Bill Tyros.")
    
    def popUpHowTo(self):
        mb.showinfo("How-To", "Click on buttons and things happen")
        

def main():
    root = tk.Tk()
    app = Application(master=root)
    
    app.master.title("Writerator")

    app.mainloop()


if __name__== "__main__":
    main()