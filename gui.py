#!/usr/bin/python
#Shivam and Stefan CSUA Hackathon
#11/4/16 @ UC Berkeley
#Gradus

from tkinter import *
import pickle
from music import main
root = Tk()
root.title("Gradus")

#Main Variables
duration = ['1', '1/2', '1/4', '1/8', '1/16']
duration_dict = {0: 1, 1: 2, 2: 4, 3: 8, 4: 16}
pitch = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
pitch_dict = {0:'c', 1:'d', 2:'e', 3:'f', 4:'g', 5:'a', 6:'b'}
octave = [str(x) for x in range(1, 11)]
ext_pitch = ['Natural', 'Sharp', 'Flat']
f = open('working.txt', 'w')
finalList = []


def onNext():
    note = []
    args = [listDuration, listPitch, listOctave, listExt_Pitch]
    for x in args:
        note.append(int(x.curselection()[0]))
    note[0] = duration_dict[note[0]]
    note[1] = pitch_dict[note[1]]
    note[2] += 1
    finalList.append(note)
    return note

def exit():
    with open('working.pcl', 'wb') as f:
        pickle.dump(finalList, f)
    f.close()
    root.destroy()
    main()


#Build GUI
label = Message(root, text="Welcome to Gradus")
listDuration, listPitch, listOctave, listExt_Pitch = Listbox(root, exportselection=0), Listbox(root, exportselection=0), Listbox(root, exportselection=0), Listbox(root, exportselection=0)

for key in duration:
    listDuration.insert(END, key)
for item in pitch:
    listPitch.insert(END, item)
for item in octave:
    listOctave.insert(END, item)
for item in ext_pitch:
    listExt_Pitch.insert(END, item)

next = Button(root, text="Next", command=onNext)
end = Button(root, text = "Finished", command=exit)

#onNext(listDuration, listPitch, listOctave, listExt_Pitch)
#Add all elements to GUI
label.pack()
listDuration.pack(side=LEFT)
listPitch.pack(side=LEFT)
listOctave.pack(side=LEFT)
listExt_Pitch.pack(side=LEFT)
next.pack(side=LEFT)
end.pack(side=BOTTOM)
root.mainloop()
