import tkinter as tk
from PIL import ImageTk, Image
import numpy as np


class ExperimentApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state = 'get_user_name'
        self.user_name = ''
        self.order = np.array([i for i in range(12)])
        self._frame = None
        self.geometry("1000x500")
        self.switch_frame(StartPage)

    def trial_begin(self, trial):
        self.state = 'experiment_trial_' + str(trial)
        self.order = np.random.permutation(self.order)
        print('order in trial %i :' % trial, self.order)

    def commit_user_name(self, textBox):
        self.user_name = textBox.get("1.0", "end-1c")
        print('user_name :', self.user_name)
        self.switch_frame(ExperimentPage)
        self.trial_begin(1)

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
        self.buttonCommit = tk.Button(self.frame, height=1, width=10, text="確認", font=("Monospace", 20),
                                      command=lambda: master.commit_user_name(self.textBox_user_name))
        self.frame_info.place(relx=.5, rely=.4, anchor='c')
        self.textBox_user_name.place(relx=.5, rely=.5, anchor='c')
        self.buttonCommit.place(relx=.5, rely=.6, anchor='c')


class ExperimentPage(tk.Frame):

    def __init__(self, master):
        self.start_countDown = False
        self.frame = tk.Frame(width=1000, height=500, bg="yellow", colormap="new")
        self.exper_intro_title = tk.Label(self.frame, text="實驗介紹", font=("Monospace", 20))
        self.exper_intro = tk.Label(self.frame, text="本實驗....", font=("Monospace", 20))
        self.ready_button = tk.Button(self.frame, text='準備開始', font=("Monospace", 20),
                                      command=lambda: self.get_ready(3000));
        self.exper_start_label = tk.Label(self.frame, font=("Monospace", 20))
        self.exper_intro_title.place(relx=.5, rely=.1, anchor='c')
        self.exper_intro.place(relx=.5, rely=.3, anchor='c')
        self.ready_button.place(relx=.5, rely=.8, anchor='c')
        self.hand_img = ImageTk.PhotoImage(Image.open("right_hand.JPG"))

    def get_ready(self, ms=3000):

        if (ms <= 0):
            self.start()
            return
        self.exper_intro_title.place_forget()
        self.exper_intro.place_forget()
        self.ready_button.place_forget()
        text = '實驗開始於 %i 秒' % (ms // 1000),
        self.exper_start_label['text'] = text
        self.exper_start_label.place(relx=.5, rely=.8, anchor='c')
        self.frame.after(1000, lambda: self.get_ready(ms - 1000))

    def start(self):
        print('start')
        self.exper_start_label.place_forget()
        img_label = tk.Label(self.frame, image=self.hand_img)
        img_label.place(relx=.5, rely=.8, anchor='c')


class ExitPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        start_label = tk.Label(self, text="This is the start page")
        page_1_button = tk.Button(self, text="Open page one",
                                  command=lambda: master.switch_frame(PageOne))
        page_2_button = tk.Button(self, text="Open page two",
                                  command=lambda: master.switch_frame(PageTwo))
        start_label.pack(side="top", fill="x", pady=10)
        page_1_button.pack()
        page_2_button.pack()


if __name__ == "__main__":
    app = ExperimentApp()
    app.mainloop()
