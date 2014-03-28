#!/usr/bin/env python
# Filename: gui.py
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import review_test

class Proximity:
        def __init__(self, master):
                self.master = master
                self.master.wm_title("Proximity Based Sentiment Analysis")
                self.frame = tk.Frame(self.master)
                var1 = StringVar()
                lb1 = Label(self.master, textvariable=var1,font = "Verdana 14 bold")
                var1.set("\nEnter your review here...\n")
                lb1.pack()
                txt = Text(self.master)
                txt.pack(expand=YES, fill=BOTH)
                Label(self.master,text="\nChoose your method:\n",font = "Verdana 12 bold").pack()
                v = IntVar()
                Radiobutton(master, text="Without Phrase Analysis", variable=v, value=0).pack(anchor=CENTER , padx=10)
                Radiobutton(master, text="With Phrase Analysis", variable=v, value=1).pack(anchor=CENTER, padx=10)
                Label(self.master,text="\n").pack()
                about = "Proximity Based Sentiment Analysis : \n\n\tThis is based on the concept of proximity of words within a review."\
                        "The basic idea is as follows. Imagine what happens when people write. When a person starts writing positively"\
                        "about a topic or subject they continue with this positive trend for a period of time. Later he/she will use"\
                        "inflexion words like 'however' and then start writing negatively about the topic. In a paragraph people don't"\
                        "repeatedly write one positive and one negative word together.\n\tTypically segments of a written text"\
                        "(e.g. paragraphs or sentences) capture a concept or trend of thought over a short period of time. Such trends"\
                        "could fluctuate as we move along the written document. The average distance between positive-oriented "\
                        "(negative-oriented) words is expected to be small for segments bearing positive (negative) sentiments. Consequently,"\
                        "we expect that the average distance between positive-oriented (negative-oriented) words is expected to be relatively"\
                        "large for segments bearing negative (positive) sentiments.\n\n\nCreated By :\nAjith S\nAmit Praseed\nDeepu Raj R\n"\
                        "Nidhin Balakrishnan\n\nDepartment of Computer Science,\nCollege Of Engineering ,Trivandrum.\n"
                self.button1 = tk.Button(self.frame, text = 'About', width = 25, command = lambda: tkMessageBox.showinfo("About", about))
                self.button1.pack( side =LEFT , padx=10)
                self.button2 = tk.Button(self.frame, text = 'Submit the review', width = 25, command = lambda: self.analysis(txt.get(1.0, END),v.get()),font = "Verdana 12 bold", relief=RAISED)
                self.button2.pack( side =LEFT , padx=10 )
                self.button2 = tk.Button(self.frame, text = 'Close', width = 25, command = lambda: self.master.destroy())
                self.button2.pack( side =LEFT , padx=10 )
                self.frame.pack()
                Label(self.master,text="\n\nCopyright : Ajith S , Amit Praseed , Deepu Raj R , Nidhin Balakrishnan\nAll Rights Reserved. \n").pack()

        def analysis(self, stringvar,isphrase):
                fid=open('samplereview.txt', 'w')
                fid.write(stringvar)
                fid.close()
                value = review_test.review_test(isphrase)
                if value==1:
                        var="Review is Positive"
                else:
                        var="Review is Negative"
                tkMessageBox.showinfo("Result", var)
      	
def main():
	root = tk.Tk()
	app = Proximity(root)
	root.mainloop()

if __name__ == '__main__':
	main()
