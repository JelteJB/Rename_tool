''' 
Tool to rename Pdf's to a 00000_FirstName_LastName_code.pdf format


Copyright © 2024 Steven de windt - Version 2.1
Permission is hereby granted, free of charge, 
to any person obtaining a copy of this software and 
associated documentation files (the “Software”), to 
deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom 
the Software is furnished to do so, subject to the 
following conditions:
The above copyright notice and this permission notice
shall be included in all copies or substantial portion
s of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


# Import

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import re
import glob
import os


# Classes

class Status(Tk):
    '''Class to keep track of a session'''

    def __init__(self):
        self._location=None
        self._current=None
        self._results = None
        self._length=None
        self._correct=False

    def new_folder(self,location):
        '''Get files from a new folder'''
        self._location=location
        self._current=0

        # Get all pdf's at location
        self._results = glob.glob(location+"/*.pdf")

        # Checking if files are already in the 000000_*_*_*.pdf format
        self._results_left=[f for f in self._results if re.match('\D{6}',f.split('\\')[-1])]
        self._length=len(self._results)
        self._length_left=len(self._results_left)
        if self._length >0:
            self.finished=False
        else:
            self.finished=True
        if self._length == self._length_left:
            self._newfolder=True
        else:
            self._newfolder=False

    def new_document(self):
        '''Prepare a new pdf to be renamed and set timer'''
        self.current_file=self._results[self._current]
        name=os.path.split(self.current_file)
        filename=os.path.splitext(name[-1])
        self.current_file_name=filename[0]
        
        self._current+=1
        
        self._check_finished()
        
    def _check_finished(self):
        '''check if all documents were done'''
        check = self._length if self._newfolder else self._length_left
        if self._current == check:
            # Done
            self.finished=True
        
    def set_correct(self,bool):
        '''Set the flag whether you can start renaming'''
        self._correct=bool

    def skipoldfiles(self):
        '''Remove the files with \d{6} from the list of files'''
        progressbar_incr=self._length-self._length_left
        self._results=self._results_left
        if self._length_left ==0:
            self.finished=True
        
        progress.step(progressbar_incr*100/self._length)

    def runfullfolder(self):
        '''Force the full folder to be done'''
        self._newfolder=True

    def get_location(self):
        '''Get _location internal veriable'''
        return self._location


## Functions
         
def callback(event):
    '''Handling keypresses in the Entry fields'''
    # After 1 ms call `_callback`
    # That is to make sure that tkinter has handled the keyboard press
    root.after(1, _callback)

def set_birthday(bool):
    '''Change color of birthday entry'''
    if bool:
        date_name_entry.config(foreground='black')
    else:
        date_name_entry.config(foreground='red')

def _callback():
    '''Update the new name dynamically'''

    # Create name like Birthday_FirstName_Lastname_Endcode.pdf
    # Add additional names like Name1-Name2-Name3
    firstname=first_name_entry.get().strip().capitalize().replace(" ","-")
    lastname=Last_name_entry.get().strip().capitalize().replace(" ","-")
    birthday=date_name_entry.get().strip()
    end_code=end_code_entry.get().strip().replace(" ","_")
    
    # Birthday Sanity Check
    if not birthday.isdigit():
        set_birthday(False)
        return

    # Correct dates that are too short or too long
    # 1112     -> 01/01/12 
    # 11212    -> 01/12/12 (so NOT as 11/02/12!)
    # 01012012 -> 01/01/12

    match len(birthday):
        case 8:
            # 01012012 -> 01/01/12
            date_name_entry.delete(4,6)
            birthday=birthday[0:4]+birthday[6:8]
        case 7:
            # 1012012 -> 01/01/12 (so NOT as 10/12/12! or 10/01/12!)
            date_name_entry.delete(3,5)
            birthday='0'+birthday[0:3]+birthday[5:7]
        case 6:
            pass # correct
        case 5:
             # 11212    -> 01/12/12 (so NOT as 11/02/12!)
            date_name_entry.insert(0,'0')
            birthday='0'+birthday
        case 4:
            # 1112     -> 01/01/12 
            date_name_entry.insert(0,'0')
            date_name_entry.insert(2,'0')
            birthday='0'+birthday[0:1]+'0'+birthday[1:]
        case 0:
            # Empty field
            return
        case _:
            # Incorrect birthday filled
            set_birthday(False)
            return

    #Sanity checks on day and month
    if int(birthday[0:2])>31 or int(birthday[2:4])>12:
        set_birthday(False)
        return
    
    set_birthday(True)
    birthday=birthday[4:6]+birthday[2:4]+birthday[0:2]
    if firstname and lastname and birthday:
        new_name_entry.delete(0,END)
        new_name_entry.insert(0,birthday+"_"+firstname+"_"+lastname+"_"+end_code)

def get_endcode(name):
    '''Extract the endcode (starting with a digit) from the original filename'''
    # find Endcode
    b= re.search('\d',name)
    try:
        loc=b.span()[0]
        return name[loc:]
    except:
        return '' # No endcode in this file


def rename_event(event):
    '''Accept pressing enter to safe results'''    
    if myStatus._correct:
        rename()

def rename():
    '''Rename the file to the new name including handling some potential problems'''
    newname=new_name_entry.get()
    oldname=old_name_entry.get()
    location=myStatus.get_location()
    
    if not (newname==oldname):
        if os.path.isfile(location+"/"+newname+".pdf"):
            if not messagebox.askokcancel("Duplicate name","Chosen filename already exists, renaming will overwrite old file.", icon='warning'):
                return
            else:
                '''Remove file to be overwritten to prevent rename to fail'''
                os.remove(location+"/"+newname+".pdf")
        try:
            os.rename(location+"/"+oldname+".pdf",location+"/"+newname+".pdf")
            
        except:
            '''In Case file is removed during session'''
            messagebox.showerror("Rename Failed","Cannot access file anymore, reload the folder!")
            change_folder()
            return
            
    if myStatus.finished:
        non_left()
    else:
        load_document()
    progress.step(100/myStatus._length)

def license():
    '''Show lisence as mentioned above in source code'''
    messagebox.showinfo("MIT Open Source License", "Copyright © 2024 Steven de windt - Version 2.1\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")


def clear(input,info=None,state_after="normal"):
    '''Reset field to be empty for next document or session'''
    input.configure(state="normal")
    input.delete(0,END)
    if info:
        input.insert(0,info)
    input.configure(state=state_after)

def non_left(bool=True):
    '''Final situation, no documents left in folder to handle'''
    clear(old_name_entry,None,'readonly')
    clear(first_name_entry)
    clear(Last_name_entry)
    clear(date_name_entry)
    clear(new_name_entry)
    clear(end_code_entry)
    Change_name_button.configure(state='disable')
    myStatus.set_correct(False)
    if bool:
        messagebox.showinfo("Completed", "All Files in this folder are converted.\nPlease select a new folder")
    else:
        messagebox.showinfo("Empty Folder", "There are no PDF's in this folder to convert.\nPlease select a new folder")
    progress_int.set(0)

def load_document():
    '''Load new pdf document in OS and reset the entries'''
    myStatus.new_document()
    try:
        os.startfile(myStatus.current_file)
    except:
        '''In Case file is removed during session'''
        messagebox.showerror("Opening Failed","Cannot open file, reload the folder!")
        change_folder()
        return
    
    clear(old_name_entry,myStatus.current_file_name,'readonly')
    clear(first_name_entry)
    clear(Last_name_entry)
    clear(date_name_entry)
    set_birthday(True)
    clear(new_name_entry,myStatus.current_file_name)
    clear(end_code_entry,get_endcode(myStatus.current_file_name))
    
def change_folder():
    '''
    Ask user for new folder and set everything
    Included possibility to skip files that are already set corrrect
    '''
    file_path = filedialog.askdirectory()
    progress_int.set(0)
    folder_entry.configure(state="normal")
    folder_entry.delete(0,END)
    folder_entry.insert(0,file_path)
    folder_entry.configure(state="readonly")
    myStatus.new_folder(file_path)

    if not myStatus._newfolder:
        if messagebox.askyesno("Converted files detected!", "Some files in this folder already start with 6 digits!\nDo you want to skip these files?"):
            myStatus.skipoldfiles()
        else:
            myStatus.runfullfolder()

    if myStatus.finished:
        non_left(False)
        return
    load_document()
    Change_name_button.configure(state='normal')
    myStatus.set_correct(True)


'''__main__'''
## Create the main tkinter window
root = Tk()
root.title("Steven's rename tool - v2.1")
root.geometry('400x420')

##Variables
input_width=40
myStatus=Status()

## Create labels and entry fields for each input

#License button
License = Button(root,text="License",command=license)
License.pack()

#Folder Entry box (Readonly)
folder = Label(root, text="Folder:")
folder.pack()
folder_entry = Entry(state="readonly",width=input_width)
folder_entry.pack()

#Change folder button
folder_button = Button(root, text="Change folder",command=change_folder)
folder_button.pack()

#Progress bar
progress_int=IntVar()
progress = Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate',variable=[progress_int]) 
progress.pack()

#Old name entry box (Readonly)
old_name_label = Label(root, text="Current name:")
old_name_label.pack()
old_name_entry = Entry(state=DISABLED,width=input_width)
old_name_entry.pack(pady=10,padx=input_width)

#Birthday Entry box
#Entry is checked for sanity 
date_name = Label(root, text="Birthday (ddmmyy):")
date_name.pack()
date_name_entry = Entry(root,width=input_width)
date_name_entry.pack()

#First name Entry Box
first_name_label = Label(root, text="First Name:")
first_name_label.pack()
first_name_entry = Entry(root,width=input_width)
first_name_entry.pack()

#Last name Entry Box
Last_name_label = Label(root, text="Last Name:")
Last_name_label.pack()
Last_name_entry = Entry(root,width=input_width)
Last_name_entry.pack()

#End code Entry Box
#Gets generated automatically, but can be changed if needed
end_code_label = Label(root, text="End-code:")
end_code_label.pack()
end_code_entry = Entry(width=input_width)
end_code_entry.pack()

#New name Entry Box
#Gets generated automatically, but can be changed if needed
new_name_label = Label(root, text="New name:")
new_name_label.pack()
new_name_entry = Entry(width=input_width)
new_name_entry.pack()

#Binding keypresses to a new-name generation
date_name_entry.bind("<Tab>",callback)
first_name_entry.bind("<Key>",callback)
Last_name_entry.bind("<Key>",callback)
end_code_entry.bind("<Key>",callback)

#Rename document button
Change_name_button = Button(root, text="Rename",command=rename,state="disabled")
Change_name_button.pack()

#Bind Enter press to the rename button
root.bind("<Return>",rename_event)

## Looping TKInter
root.mainloop()