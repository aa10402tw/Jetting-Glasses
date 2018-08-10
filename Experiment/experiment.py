import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import numpy as np
import time

finger2num = {'index_1': 0, 'index_2': 1, 'index_3': 2,
              'middle_1': 3, 'middle_2': 4, 'middle_3': 5,
              'ring_1': 6, 'ring_2': 7, 'ring_3': 8,
              'little_1': 9, 'little_2': 10, 'little_3': 11}
num2finger = {v: k for k, v in finger2num.items()}


'''
Procedure :
Start -> Exp -> end

Start : Greeting & Enter User Name 

Exp : 
    1. Put hand on table 
    2. User decide to Start
    3. Show Image, User execute and decide to commit
    4. Loop to 1. until enough round  

End : Say GoodBye

'''

NUM_BLOCK = 3
NUM_TRIAL = 12
Debug_Mode = True


class ExperimentApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.has_haptic = False
        self.user_name = ''
        self.order = np.array([i for i in range(12)])
        self.idx = 0
        self._frame = None
        self.geometry("1000x500")
        self.switch_frame(StartPage)
        self.num_block = 0

    def block_begin(self, block):
        self.state = 'experiment_block_' + str(block)
        self.order = np.random.permutation(self.order)
        print('order in block %i :' % block, self.order)
        self.idx = 0

    def get_finger_num(self):
        return self.order[self.idx]

    def next_finger(self):
        self.idx += 1
        if(self.idx >= len(self.order)):
            self.num_block += 1
            self.block_begin(self.num_block + 1)
            if(self.num_block < NUM_BLOCK):
                self.switch_frame(ExperimentPage)
            else:
                self.switch_frame(ExitPage)
            return -1
        return self.idx

    def commit_user_name(self, textBox, haptic):
        self.user_name = textBox.get("1.0", "end-1c")
        print('user_name :', self.user_name)
        self.switch_frame(ExperimentPage)
        self.block_begin(1)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame.frame
        self._frame.place(relx=.5, rely=.5, anchor='c')


class StartPage(tk.Frame):
    def __init__(self, master):
        self.frame = tk.Frame(width=1000, height=500, colormap="new")
        self.frame_info = tk.Label(self.frame, text='請輸入姓名(英文)', font=("Monospace", 20))
        self.textBox_user_name = tk.Text(self.frame, height=1, width=20, font=("Monospace", 20))

        self.buttonCommit_no_haptic = tk.Button(self.frame, height=1, width=10, text="no haptic", font=("Monospace", 20),
                                                command=lambda: master.commit_user_name(self.textBox_user_name, haptic=False))
        self.buttonCommit_haptic = tk.Button(self.frame, height=1, width=10, text="haptic", font=("Monospace", 20),
                                             command=lambda: master.commit_user_name(self.textBox_user_name, haptic=True))
        self.frame_info.place(relx=.5, rely=.4, anchor='c')
        self.textBox_user_name.place(relx=.5, rely=.5, anchor='c')
        self.buttonCommit_no_haptic.place(relx=.4, rely=.6, anchor='c')
        self.buttonCommit_haptic.place(relx=.6, rely=.6, anchor='c')


class ExperimentPage(tk.Frame):

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(width=1000, height=500, colormap="new")
        self.exper_intro_title = tk.Label(self.frame, text="實驗介紹", font=("Monospace", 20))
        self.exper_intro = tk.Label(self.frame, text="本實驗....", font=("Monospace", 20))
        self.ready_instruction = tk.Label(self.frame, text="請將雙手平放於桌上", font=("Monospace", 20))
        self.ready_button = tk.Button(self.frame, text='準備開始', font=("Monospace", 20),
                                      command=lambda: self.start());
        self.img_label = tk.Label(self.frame)
        self.exper_start_label = tk.Label(self.frame, font=("Monospace", 20))
        self.exper_instruction = tk.Label(self.frame, text="藍點為目標", font=("Monospace", 20))

        self.commit_button = tk.Button(self.frame, text='確定', font=("Monospace", 20),
                                       command=lambda: self.commit());
        self.start_time = 0
        self.commit_time = 0
        self.completion_time = 0

        self.finger_pos = [(376, 95), (364, 171), (346, 270),
                           (241, 62), (245, 148), (247, 157),
                           (149, 90), (154, 172), (166, 280),
                           (38, 210), (63, 263), (87, 327)]

        self.debug_info = ''
        self.debug_label = tk.Label(self.frame, font=("Monospace", 20), borderwidth=2, relief="solid")

        if(master.num_block == 0):
            self.exp_intro()
        else:
            self.take_break()

    def get_debug_info(self):
        self.debug_info = "block : %i/%i\ntrial : %i/%i\ntime : %.2f s" % (self.master.num_block, NUM_BLOCK, self.master.idx, 12, self.completion_time)
        return self.debug_info

    def exp_intro(self):
        self.exper_intro_title.place(relx=.5, rely=.1, anchor='c')
        self.exper_intro.place(relx=.5, rely=.3, anchor='c')
        self.ready_button.place(relx=.5, rely=.8, anchor='c')

        if(Debug_Mode):
            self.debug_label['text'] = '(intro)\n ' + self.get_debug_info()
            self.debug_label.place(relx=.05, rely=.05, anchor='nw')

    def take_break(self):

        self.exper_intro_title.place_forget()
        self.exper_intro.place_forget()

        self.commit_button.place_forget()
        self.img_label.place_forget()
        self.exper_instruction.place_forget()
        self.ready_button.place(relx=.5, rely=.8, anchor='c')

        if(Debug_Mode):
            self.debug_label['text'] = '(break)\n' + self.get_debug_info()
            self.debug_label.place(relx=.05, rely=.05, anchor='nw')

    def commit(self):
        self.commit_time = time.time()
        self.completion_time = self.commit_time - self.start_time
        f = self.master.get_finger_num()
        print("finish [%i] %i, %s (%.2f s)" % (self.master.idx, f, num2finger[f], self.completion_time))
        c = self.master.next_finger()
        if(c != -1):
            self.take_break()

    def start(self):
        self.exper_intro_title.place_forget()
        self.exper_intro.place_forget()
        self.ready_instruction.place_forget()
        self.start_time = time.time()
        img = Image.open("right_hand.JPG")
        draw = ImageDraw.Draw(img)
        point_size = 10

        f = self.master.get_finger_num()

        pos = self.finger_pos[f][0] - point_size, self.finger_pos[f][1] - point_size, self.finger_pos[f][0] + point_size, self.finger_pos[f][1] + point_size
        draw.ellipse(pos, fill='blue', outline='blue')
        img = img.resize((300, 400), Image.ANTIALIAS)
        self.hand_img = ImageTk.PhotoImage(img)
        self.img_label = tk.Label(self.frame, image=self.hand_img)
        self.img_label.place(relx=.5, rely=.5, anchor='c')
        self.exper_instruction.place(relx=.8, rely=.5, anchor='c')
        self.commit_button.place(relx=.8, rely=.8, anchor='c')

        if(Debug_Mode):
            self.debug_label['text'] = '(start)\n' + self.get_debug_info()
            self.debug_label.place(relx=.05, rely=.05, anchor='nw')


class ExitPage(tk.Frame):
    def __init__(self, master):
        self.frame = tk.Frame(width=1000, height=500, bg="green", colormap="new")
        self.master = master

        self.exit_label = tk.Label(self.frame, text="88888")
        self.exit_label.place(relx=.5, rely=.5, anchor='c')


if __name__ == "__main__":
    app = ExperimentApp()
    app.mainloop()
