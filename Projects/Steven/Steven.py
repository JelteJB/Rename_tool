''' 

Copyright 2024 Steven de windt
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

from tkinter import *
from tkinter.ttk import *
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
        self._correct=False

    def new_folder(self,location):
        self._location=location
        self._current=0
        self._results = glob.glob(location+"/*.pdf")
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
        
        self.current_file=self._results[self._current]
        name=os.path.split(self.current_file)
        filename=os.path.splitext(name[-1])
        self.current_file_name=filename[0]
        os.startfile(self.current_file)
        self._current+=1
        
        self._check_finished()
        
    def _check_finished(self):
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
        self._newfolder=True

    def get_location(self):
        return self._location
       
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
    if len(geboorte)==5:
        date_name_entry.insert(0,'0')
        geboorte='0'+geboorte
    elif len(geboorte)==4:
        date_name_entry.insert(0,'0')
        date_name_entry.insert(2,'0')
        geboorte='0'+geboorte[0:1]+'0'+geboorte[1:]

    if not (len(geboorte)==6):
       date_name_entry.config(foreground='red')       
    elif int(geboorte[0:2])>31 or int(geboorte[2:4])>12:
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
    try:
        loc=b.span()[0]
        return name[loc:]
    except:
        return ''


def rename_event(event):    
    if myStatus._correct:
        rename()

def rename():
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
            messagebox.showerror("Rename Failed","Cannot access file anymore, reload the folder!")
            change_folder()
            return
            
    if myStatus.finished:
        non_left()
    else:
        load_document()
    progress.step(100/myStatus._length)

def license():
    messagebox.showinfo("MIT Open Source License", "Copyright 2024 Steven de windt\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")


def clear(input,info=None,state_after="normal"):
    input.configure(state="normal")
    input.delete(0,END)
    if info:
        input.insert(0,info)
    input.configure(state=state_after)

def non_left(bool=True):
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

    
    


# Create the main tkinter window
root = Tk()
root.title("Steven's rename tool")
root.geometry('400x420')
input_width=40

License = Button(root,text="License",command=license)
License.pack()

# Create labels and entry fields for each input
folder = Label(root, text="Folder:")
folder.pack()
folder_entry = Entry(state="readonly",width=input_width)
folder_entry.pack()

folder_button = Button(root, text="Change folder",command=change_folder)
folder_button.pack()

progress_int=IntVar()
progress = Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate',variable=[progress_int]) 
progress.pack()
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
Change_name_button.pack()
myStatus=Status()


root.bind("<Return>",rename_event)
root.mainloop()