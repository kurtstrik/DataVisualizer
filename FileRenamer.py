import tkinter
import re, sys, os, operator
from datetime import *


win = tkinter.Tk()
win.geometry('400x50')
pathinput = tkinter.Label(text="Bitte Ordnerpfad eingeben")

button = tkinter.Button(win, text='Durchsuchen')

browse = tkinter.Entry(win)
pathinput.pack(anchor='nw')
browse.place(in_=pathinput, rely='1.0', width=300)
button.place(in_=browse, relx='1.0')

win.mainloop()

path = "E:/Peli Best/ClipsTest"
old = ""
new = ""
#files = os.listdir(path)

alldates = []
count = 1


"""for x in files: # iterate each file in path folder
    y = re.search("\[{1}.+\]{1}",x) #search for 1x[  1+ a-z OR 0-9   1x] pattern 
    
    if y is None:
        print("None")
    else:
        z = y.string[(y.span()[0]+1):(y.span()[1])-1].split("-") # .span() returns start/end index of matching pattern, string[x:y] gets substring, split seperates into tuples by seperating sign
        day = z[0]
        month = z[1]
        year = z[2] 
        datum = date(int(year),int(month),int(day))
        name = y.string[y.span()[1]:]    

        data = {"index":1, "datum":datum, "name":name}
        alldates.append(data) """
        
#        print(y.string)
        #newtuple = (day, month, year)
        #datum = "-".join(newtuple)
        #datum = "["+datum+"]" 
        #u = y.string.replace(y.group(), datum) # switch old date with new date format
        #os.rename(path+"/"+y.string, path+"/"+u) # finally rename given old filename with new one

"""
alldates.sort(key=operator.itemgetter('datum'))

print("--------------------------------")
counter = 1
for d in range(len(alldates)):
    temp = alldates[d].get("datum")
    alldates[d]["index"]= counter
    #print(str(counter)+" "+temp.strftime("[%d-%m-%Y]")+d.get("name"))    
    counter+=1
    #format(counter, '02d')


for e in alldates:
    temp = e.get("datum")
    print(str(e.get("index"))+" "+temp.strftime("[%d-%m-%Y]")+e.get("name"))"""

# TODO: rename files according to date

"""for j in files:
    for i in alldates:
        info = i.get("datum").strftime("[%d-%m-%Y]")+i.get("name")
        if(j == info):
            outstring = str(i.get("index"))+" "+info
            os.rename(path+"/"+j, path+"/"+outstring)     """   
