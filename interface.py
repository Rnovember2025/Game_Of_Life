from tkinter import *
from tkinter import ttk
from time import time as get_time

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Game of Life")
        self.root.columnconfigure(0,weight=0)
        self.root.columnconfigure(1,weight=1)
        self.root.rowconfigure(13,weight=1)

        ttk.Button(self.root,text="Quit",command=self.close).grid(column=0,row=0,sticky=(N,W))

        ttk.Button(self.root,text="Add Edit",command=self._done_editing).grid(column=0,row=1,sticky=(N,W),pady=(5,0))

        ttk.Button(self.root,text="Clear Edit",command=self._undo_edit).grid(column=0,row=2,sticky=(N,W))

        ttk.Button(self.root,text="Reset Cells",command=self._reset).grid(column=0,row=3,sticky=(N,W),pady=(5,0))

        ttk.Button(self.root,text="New State",command=self._new_state).grid(column=0,row=4,sticky=(N,W))

        self.run_button = ttk.Button(self.root,text="Run",command=self._run)
        self.run_button.grid(column=0,row=5,sticky=(N,W),pady=(5,0))

        self.check_box_var = BooleanVar(self.root,value=0)
        ttk.Checkbutton(self.root,text="Step Mode",command=self._single_step,
                        variable=self.check_box_var).grid(column=0,row=6,sticky=(N,W))

        ttk.Label(self.root, text='Speed\n(1 = Fast!)').grid(column=0,row=7,sticky=(N,W),pady=(15,0))

        self.sim_speed_var = StringVar(self.root,value=20)
        self.sim_speed_box = ttk.Spinbox(self.root,from_=1,to=100,width=7,
                                           textvariable=self.sim_speed_var)
        self.sim_speed_box.state(['readonly'])
        self.sim_speed_box.grid(column=0,row=8,sticky=(N,E))

        ttk.Label(self.root, text='Scale').grid(column=0,row=9,sticky=(N,W),pady=(15,0))

        self.scale_var = DoubleVar(value=5)
        self.scale_select = ttk.Combobox(self.root, width=8, textvariable=self.scale_var)
        self.scale_select['values'] = (15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,.5,.1,.05,.01,.001,.0001)
        self.scale_select.state(['readonly'])
        self.scale_select.grid(column=0,row=10,sticky=(N,E))

        ttk.Button(self.root,text='Help',command=self._help_window)\
            .grid(column=0,row=13,sticky=(S,W))

        self.frame_rate_var = StringVar(self.root,value="FPS: 0")
        ttk.Label(self.root, textvariable=self.frame_rate_var).grid(column=0,row=14,sticky=(S,W))
        
        self.canvas_frame = Frame(self.root)
        self.canvas_frame["borderwidth"] = 3
        self.canvas_frame["relief"] = 'sunken'
        self.canvas_frame.grid(column=1,row=0,rowspan=15,sticky=(N,S,E,W))
        self.canvas_frame.columnconfigure(0,weight=1)
        self.canvas_frame.rowconfigure(0,weight=1)

        self.canvas = Canvas(self.canvas_frame,height=500,width=500,background='black')
        self.canvas.grid(sticky=(N,S,E,W))
        self.canvas.configure(xscrollincrement=1,yscrollincrement=1)
        
        self.canvas.scan_mark(0,0)
        self.canvas.scan_dragto(250,250,gain=1)

        self.cross_hairs = (self.canvas.create_line(0,-5,0,5,fill='red'),
                            self.canvas.create_line(-5,0,5,0,fill='red'))
        self.center = (0,0)

        self._bind_events()

        # internal variables
        self._scale = 5
        self._sim_speed = 20
        self._single_step = False
        self._simulation_running = False
        self._reset = False
        self._new_state = False
        self._done_edit = False
        self._last_time = get_time()
        self._edited_cells = []

    def get_edited_cells(self):
        if self._done_edit:
            edited_cells = self._edited_cells[:]
            self._edited_cells.clear()
            self._done_edit = False
            self.canvas.itemconfigure('edit',fill='white',
                                      outline='white',tags=('almost_all','perm'))
            return edited_cells
        else: return []
        
    def draw(self, state): 
        self.canvas.delete('perm')
        for cell in state:
            x1 = cell[0]*self._scale
            y1 = cell[1]*self._scale
            self.canvas.create_rectangle(x1,y1,x1+self._scale,y1+self._scale,fill='white',
                                         outline='white',tags=('almost_all','perm'))

    def update_framerate(self,other_data=''):
        current_time = get_time()
        elapsed_time = current_time - self._last_time
        self.frame_rate_var.set(f"FPS: {int(1/elapsed_time)}\n{other_data}")
        self._last_time = current_time

    def is_simulation_running(self):
        if self._reset:
            self._reset = False
            return 2
        elif self._new_state:
            self._new_state = False
            return 3
        elif self._single_step:
            running = self._simulation_running
            self._simulation_running = False
            return running
        else:
            return self._simulation_running

    def schedule(self,function,time=None):
        if time:
            self.root.after(time,function)
        else:
            self.root.after(self._sim_speed,function)

    def loop(self):
        self.root.mainloop()
        
    def close(self,var=1):
        self.root.destroy()
        self.root.quit()

    def _bind_events(self):
        self.root.bind("<q>",func=self.close)
        self.root.bind("<Escape>",func=self.close)
        self.root.bind("<Control-r>",func=self._run)
        self.root.bind("<Control-x>",func=self._reset)
        self.root.bind("<Control-z>",func=self._undo_edit)
        self.root.bind("<Control-s>",func=self._single_step)
        self.root.bind("<Control-n>",func=self._new_state)
        
        self.canvas.bind("<Button-1>",func=self._start_drag)
        self.canvas.bind("<B1-Motion>",func=self._drag)
        #self.canvas.bind("<Button-2>",func=self._recenter)
        self.canvas.bind("<Button-3>",func=self._edit)
        self.canvas.bind("<B3-Motion>",func=self._edit)
        self.canvas.bind("<Shift-Button-3>",func=self._done_editing)

        self.scale_select.bind("<<ComboboxSelected>>", self._update_scale)
        self.sim_speed_box.bind("<<Increment>>", self._update_sim_speed)
        self.sim_speed_box.bind("<<Decrement>>", self._update_sim_speed)

    def _edit(self,event):
        s = self._scale
        x = int((self.canvas.canvasx(event.x)/s))
        y = int((self.canvas.canvasy(event.y)/s))

        if not (x,y) in self._edited_cells:
            self._edited_cells.append((x,y))
            self.canvas.create_rectangle(x*s,y*s,x*s+s,y*s+s,
                                         fill='yellow',outline='yellow',
                                         tags=('almost_all','edit'))

    def _done_editing(self,event=None):
        self._done_edit = True

    def _undo_edit(self,event=None):
        self._edited_cells.clear()
        self.canvas.delete('edit')
                
    def _run(self,event=None):
        if self._single_step:
            self._simulation_running = True
        else:
            self._simulation_running = not self._simulation_running
            if self._simulation_running:
                self.run_button["text"] = "Pause"
            else:
                self.run_button["text"] = "Run"

    def _update_scale(self,event=None):
        new_scale = self.scale_var.get()
        self.canvas.scale('almost_all',self.center[0],self.center[1],
                          new_scale/self._scale,new_scale/self._scale)
        self._scale = new_scale

    def _update_sim_speed(self, event=None):
        speed = self.sim_speed_var.get()
        if speed.isdigit():
            if 1 <= int(speed) <= 100:
                self._sim_speed = int(speed)
                return
        
        self._sim_speed = 20

##    def _recenter(self,event):
##        x = self.canvas.canvasx(event.x)
##        y = self.canvas.canvasy(event.y)
##        self.canvas.coords(self.cross_hairs[0], x, y-5, x, y+5)
##        self.canvas.coords(self.cross_hairs[1], x-5, y, x+5, y)
##
##        self.center = (x,y)
##        self._update_scale()

    def _start_drag(self,event):
        self.canvas.scan_mark(event.x,event.y)

    def _drag(self,event):
        self.canvas.scan_dragto(event.x,event.y,gain=1)

    def _single_step(self,event=None):
        if self._single_step:
            self._single_step = False
            self.check_box_var.set(False)
            self._simulation_running = True
            self._run()
        else:
            self._single_step = True
            self.check_box_var.set(True)
            self.run_button["text"] = "Single Step"
            self._simulation_running = False

    def _reset(self,event=None):
        self._reset = True

    def _new_state(self,event=None):
        self._new_state = True

    def _help_window(self,event=None):
        help_win = Toplevel(self.root)
        help_win.title('HELP')
        ttk.Label(help_win, text=\
"""Keyboard Shortcuts:
 * Esc (or q): Quit Program
 * Control Z: Clear Edit
 * Control X: Reset Cells
 * Control N: New State
 * Control R: Run or Step Simulation
 * Control S: Toggle Single Step


Mouse Controls:
 * Left Click & Drag: Move Around
 * Right Click & Drag: Add Cells
 * Shift Right Click: Add Edited
    Cells to Simulation
 * Scroll on Speed Box: Change Speed
 * Scroll on Scale Box: Change Scale
""").grid(padx=5)
        ttk.Button(help_win,text='OK',command=help_win.destroy).grid(pady=(0,5))
