import sys, os, time, subprocess, json, atexit
 
import Tkinter, tkFileDialog
class Theapp(Tkinter.Tk):
    def __init__(self,parent):
 
        with open('config.json') as data_file:
            cfg_data = json.load(data_file)
        self.cfg_data = cfg_data 
 
        with open(cfg_data[0]['commandsf']) as data_file:
            commands = json.load(data_file)
        self.commands = commands 
 
 
        atexit.register(self.on_exit)

        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
		
    def on_exit(self):
 
        self.cfg_data[0]['workingd'] = self.cwd.get()
 
 
        print "self.cwd.get(): %s"%(self.cwd.get())
        print "self.cfg_data: %s"%(self.cfg_data)
 
        with open('config.json', 'w') as f:
            json.dump(self.cfg_data, f)
 
    def execute_cmd(self, rnum):

        commandstring = self.cmd_entries[rnum].get()
        cwdpath = self.cwd.get()
        outstr = subprocess.check_call(commandstring, cwd=cwdpath, shell=True)
        print outstr
 
 
    ## http://stackoverflow.com/a/16777523/601770   
    def bclick(self, rnum):
        def click():            
            self.execute_cmd(rnum)
        return click
 
 
 
    def browse2cwd(self):   

        tkFileDiaOpt4Dir = {}
        tkFileDiaOpt4Dir['initialdir'] = self.cwd.get()
        tkFileDiaOpt4Dir['mustexist'] = False
        tkFileDiaOpt4Dir['parent'] = self
        tkFileDiaOpt4Dir['title'] = 'Browse to set CWD.'
 
        self.cwd.set( tkFileDialog.askdirectory(**tkFileDiaOpt4Dir) )
 
        print "browse2cwd:  self.cwd.get(): %s"%(self.cwd.get())
 
    def initialize(self):
        self.cwd = Tkinter.StringVar()
        self.cwd.set(self.cfg_data[0]['workingd'])
        self.grid()
 
        ### gui elements
		
		
		
        ## browse to working directory
        label = Tkinter.Label(self, text="Working Directory", fg="#111")
        label.grid(column=0,row=0,columnspan=3,sticky='W')
 
        self.cwd_entry = Tkinter.Entry(self, width=80, textvariable=self.cwd)
        self.cwd_entry.grid(column=0,row=1,columnspan=2, sticky='W')
 
        b = Tkinter.Button(self,text=u"Browse", command=self.browse2cwd,width=8,cursor="crosshair")
        b.grid(column=2,row=1,padx=10,pady=4) 
 
        toprowscount = 2
 
 
        ## command row elements len == len(MyCommands.commands)
        self.buttons = []
        self.cmd_entries = []
        for rnum, cmd in enumerate(self.commands):
 
            label = Tkinter.Label(self, anchor="w",text=cmd['label'], fg="#111")
            label.grid(column=0,row=rnum+toprowscount,sticky='EW')
 
            self.cmd_entries.append( Tkinter.Entry(self, width=60) )
            self.cmd_entries[-1].grid(column=1,row=rnum+toprowscount,sticky='EW'); self.cmd_entries[-1].insert(0, (cmd['cmd']+' '+ cmd['args']))
 
            b = Tkinter.Button(self,text=u"Task %s"%(rnum), command=self.bclick(rnum),width=8,cursor="crosshair")
            b.grid(column=2,row=rnum+toprowscount,padx=10,pady=4) 
 
            self.buttons.append(b)
 
        ## Finish up
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
 
 
 
 
if __name__ == "__main__":
	app = Theapp(None)
	
app.title('Gulp GUI')
app.iconbitmap('gulp.ico')
app.mainloop()