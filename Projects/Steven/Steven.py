
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import re
import glob
import os

class Status(Tk):

    def __init__(self):
        self._location=None
        self._current=None
        self._results = None
        self._length=None

    def new_folder(self,location):
        self._location=location
        self._current=0
        self._results = glob.glob(location+"/*.pdf")
        self._length=len(self._results)
        
        if self._length >0:
            self.finished=False
        else:
            self.finished=True

    def new_document(self):
        
        self.current_file=self._results[self._current]
        name=os.path.split(self.current_file)
        filename=os.path.splitext(name[-1])
        self.current_file_name=filename[0]
        os.startfile(self.current_file)
        self._current+=1
        
        if self._current==self._length:
            # Done
            self.finished=True


def callback(event):
    # After 1 ms call `_callback`
    # That is to make sure that tkinter has handled the keyboard press
    root.after(1, _callback)

def _callback():
    # The `-1` is there because when you have `text_widget.get(..., "end")`
    # It adds a "\n" character at then end
    firstname=first_name_entry.get().strip().replace(" ","-")
    lastname=Last_name_entry.get().strip().replace(" ","-")
    geboorte=date_name_entry.get().strip()
    end_code=end_code_entry.get().strip().replace(" ","_")
    
    if not (len(geboorte)==6):
       date_name_entry.config(foreground='red')
    else:
        date_name_entry.config(foreground='black')
        geboorte=geboorte[4:6]+geboorte[2:4]+geboorte[0:2]
        if firstname and lastname and geboorte:
            new_name_entry.delete(0,END)
            new_name_entry.insert(0,geboorte+"_"+firstname+"_"+lastname+"_"+end_code)

def get_endcode(name):
    # find Endcode
    b= re.search('\d',name)
    loc=b.span()[0]
    return name[loc:]
def rename_event(event):
    if Change_name_button['state']=='normal':
        rename()

def rename():
    newname=new_name_entry.get()
    oldname=old_name_entry.get()
    location=myStatus._location
    if not (newname==oldname):
        os.rename(location+"/"+oldname+".pdf",location+"/"+newname+".pdf")
    if myStatus.finished:
        non_left()
    else:
        load_document()

def license():
    messagebox.showinfo("MIT Open Source License", "Copyright 2024 Steven de windt\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")


def clear(input,info=None,state_after="normal"):
    input.configure(state="normal")
    input.delete(0,END)
    if info:
        input.insert(0,info)
    input.configure(state=state_after)

def non_left():
    clear(old_name_entry,None,'readonly')
    clear(first_name_entry)
    clear(Last_name_entry)
    clear(date_name_entry)
    clear(new_name_entry)
    clear(end_code_entry)
    Change_name_button.configure(state='disable')
    messagebox.showinfo("Completed", "All Files in this folder are converted.\nPlease select a new folder")

def load_document():
    myStatus.new_document()
    clear(old_name_entry,myStatus.current_file_name,'readonly')
    clear(first_name_entry)
    clear(Last_name_entry)
    clear(date_name_entry)
    date_name_entry.config(foreground='black')
    clear(new_name_entry,myStatus.current_file_name)
    clear(end_code_entry,get_endcode(myStatus.current_file_name))

def change_folder():
    file_path = filedialog.askdirectory()
    folder_entry.configure(state="normal")
    folder_entry.delete(0,END)
    folder_entry.insert(0,file_path)
    folder_entry.configure(state="readonly")
    myStatus.new_folder(file_path)
    if myStatus.finished:
        non_left()
        return
    load_document()
    Change_name_button.configure(state='normal')

    


# Create the main tkinter window
root = Tk()
root.title("Steven's rename tool")
root.geometry('400x400')
input_width=40

License = Button(root,text="License",command=license)
License.pack()

# Create labels and entry fields for each input
folder = Label(root, text="Folder:")
folder.pack()


folder_entry = Entry(state="readonly",width=input_width)

folder_entry.pack()
folder_entry.insert(0,"dcdd")
folder_button = Button(root, text="Change folder",command=change_folder)
folder_button.pack()

old_name_label = Label(root, text="Current name:")
old_name_label.pack()
old_name_entry = Entry(state=DISABLED,width=input_width)
old_name_entry.pack(pady=10,padx=input_width)



date_name = Label(root, text="Geboorte datum (ddmmyy):")
date_name.pack()
date_name_entry = Entry(root,width=input_width)
date_name_entry.pack()

first_name_label = Label(root, text="First Name:")
first_name_label.pack()
first_name_entry = Entry(root,width=input_width)
first_name_entry.pack()
print(first_name_entry)
Last_name_label = Label(root, text="Last Name:")
Last_name_label.pack()
Last_name_entry = Entry(root,width=input_width)
Last_name_entry.pack()




end_code_label = Label(root, text="End-code:")
end_code_label.pack()
end_code_entry = Entry(width=input_width)
end_code_entry.pack()
#end_code_entry.insert(0,oldname[loc_end_code:])


new_name_label = Label(root, text="New name:")
new_name_label.pack()
new_name_entry = Entry(width=input_width)
new_name_entry.pack()
#new_name_entry.insert(0,mystr2.get())


date_name_entry.bind("<Tab>",callback)
first_name_entry.bind("<Key>",callback)
Last_name_entry.bind("<Key>",callback)
end_code_entry.bind("<Key>",callback)



Change_name_button = Button(root, text="Rename",command=rename,state="disabled")
Change_name_button.bind("<Enter>")
Change_name_button.pack()
myStatus=Status()


root.bind("<Return>",rename_event)
root.mainloop()