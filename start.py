# !/usr/bin/python3  

from tkinter import *
from tkinter import messagebox
import csv, os
from yahoo_fin import options as options
import yfinance as yf
from datetime import date
from datetime import *
import sqlite3
from dateutil import parser
from tkinter.ttk import Progressbar
from threading import Event

conn = sqlite3.connect('CSP.db')
c = conn.cursor()

def GetPutData(Ticker, Expiry):
  
  dictionary = options.get_puts(Ticker,Expiry)
  

  
  ##Contract Name
  ##Last Trade Date
  ##Strike
  ##Last Price
  ##Bid
  ##Ask
  ##Change
  ##% Change
  ##Volume
  ##Open Interest
  ##Implied Volatility

  

  x=0
  line = ''
  returnVal = ''
  items=dictionary.items()

  while x<len(dictionary):
      line = str(x) + '|' + Ticker + '|'
      for code,value in dictionary.items():
        line += str(value[x]) + "|"
      x+=1
      line = line[:-1]
      returnVal += line + '\n'
  return returnVal
def get_value(item):
    info = item.strip().split(':')
    val = info[1].strip().split(',')
    return val[0].strip()


def dataInsert():
        cspdata = open("cspData.txt","wt")
        with open('TickerLog.txt', 'rt') as tickerFile:
            for symbol in tickerFile:
                symbol = symbol.replace('\n','')
                dates = options.get_expiration_dates(symbol)
                for date in dates:
                    #print(date)
                    #print (str(date - datetime.today()))
                    try:
                        cspdata.write(GetPutData(symbol,date))
                    except:
                        print("failed to write to csp data file")
        tickerFile.close()
        
        winner = 0.0
        with open("cspData.txt", 'r') as f:
            conn.execute("delete from Options;")
            for line in f:
                data = line.split("|")

                #begin DTE calculations because yahoo_fin doesnt know that somehoh
                #calculate DTE from the expiry in contract name EX: F220114P00010000
                st = data[2]
                
                newst = st.replace(data[1], '')
                #print(newst)

                st2 = newst[0:6]

                #print(st2)

                y = '20' + st2[0:2]
                m = st2[2:4]
                d = st2[4:6]

                #print ("y: "+y )
                #print ("m: "+m )
                #print ("d: "+d )
                
                #print(data[2])

                dt = y + "-" + m + "-" + d

                
                
                stdate = datetime.strptime(dt, '%Y-%m-%d')
                

                adte = stdate.date() - datetime.today().date()
                s = str(adte)
                spl = s.split(" ")
                dte = spl[0]
                #print(dte)
                

                if ( (float(data[5])/float(data[4]))/int(dte) > winner):
                  winner1 = data[2]
                  winnerName = winner1[0:7] + " " + data[4] + " put for "+data[5]+"$" 
                  
                  winner = (float(data[5])/float(data[4]))/int(dte)
            print(winnerName)

                
              
                
                
        

        f.close()    
        return winnerName 

        


  
def calculate():
    
    q = dataInsert()
    Label(text=q).pack(side=RIGHT,padx=5,pady=3) 

    
    
    
def quitWin():
    res = messagebox.askyesno('prompt', 'Calculations can take up to 5 minutes. Do you still want to calculate?') 
    if res == False:
        messagebox.showinfo('countdown', 'calculation canceled')
        root.destroy()
        

    elif res == True:
        pass
        messagebox.showerror('error', 'dont cancel even if page stops responding')
        calculate()
        
    else:
        messagebox.showerror('error', 'something went wrong!')  
    
    
    
    

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.output()

    def output(self):
        Label(text='Insert Tickers:').pack(side=LEFT,padx=5,pady=5)
        self.e = Entry(root, width=10)
        self.e.pack(side=LEFT,padx=5,pady=5)

        self.b = Button(root, text='Submit', command=self.writeToFile)
        self.b.pack(side=LEFT,padx=5,pady=5)
        self.b2 = Button(root, text='Clear File', command=self.clearFile)
        self.b2.pack(side=LEFT,padx=2.5,pady=5)

    
    def writeToFile(self):
        with open('TickerLog.txt', 'a', newline = '') as f:
            w=csv.writer(f)
            w.writerow([self.e.get().upper()])
        self.e.delete(0, END)

    def clearFile(self):
        os.remove("TickerLog.txt") 
        print("file removed")

    
            
       
           


    
        

if __name__ == "__main__":
    root=Tk()
    root.title("Miles CSP Calculator")
    root.geometry('1000x100')
    calc = Button(root, text='Finished', command=quitWin)
    calc.pack(side=RIGHT,padx=5,pady=5)
    app=App(master=root)
    app.mainloop()
    root.mainloop()










'''
win = Tk()

win.geometry("750x250")
def get_content():
   #Get the content of Entry Widget
   print(entry.get())

def nextPage():
    win.destroy()
    import page2
    '''
