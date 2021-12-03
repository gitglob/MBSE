# -*- coding: utf-8 -*-

import tkinter as tk

''' DEFAULT VALUES FOR THE SIMULATION

TIME_TO_RUN     = 3600*24*1 # 1 day
SENSOR_DISTANCE = 0 # 15 meters => 3 blocks
SENSOR_PERIOD   = 600 # seconds (5mins)
SENSOR_STATIC   = True
SAVE_PLOTS      = True
DEBUG           = False

'''

class GUI:

    def __init__(self, master, canvas):
        self.master = master
        self.frame = tk.Frame(self.master, bg='black')
        self.startButton = tk.Button(self.master, text='START the Simulation', padx=10, pady=10,
                                     command=self.start_simulation, font=('Helvetica', 10, 'bold'))

        self.quitButton = tk.Button(self.master, text='QUIT', padx=10, pady=10,
                                    command=self.close_windows, font=('Helvetica', 10, 'bold'))

        self.parameters_button = tk.Button(self.master, text='Set Parameters', padx=10, pady=10,
                                           command=self.set_parameters,  font=('Helvetica', 10, 'bold'))

        self.canvas = canvas
        self.startButton_window = self.canvas.create_window(
            360, 645, window=self.startButton)
        self.parameters_window = self.canvas.create_window(
            510, 645, window=self.parameters_button)
        self.quitButton_window = self.canvas.create_window(
            605, 645, window=self.quitButton)

        self.days = 1
        self.sensors_distance = 8
        self.sensors_period = 900
        self.sensors_movement = True  # True = 'static'
        self.save_plots = False
        self.debug = False
        self.frame.pack()


#%%     ##################### PARAMETERS #####################
    def set_parameters(self):

        self.parameters = tk.Toplevel()
        parameters = self.parameters
        parameters.title("Simulation Parameters")
        parameters.geometry("450x350")
        button = tk.Button(parameters, text="THE PARAMETERS ARE SET !!", command=self.close_windows_parameters,
                           padx=10, pady=10, bd=5, font=('Helvetica', 18, 'bold'))
        button.grid(row=10, column=1)

        #%%     SAVE PLOTS

        self.save_plots2 = tk.BooleanVar()
        self.s_p = tk.Checkbutton(parameters, text='Save Plots of the Simulation', variable=self.save_plots2,
                                  onvalue=True, offvalue=False, command=self.get_check_value_save_plots)
        self.s_p.grid(row=1, column=1, sticky="nw")

        #%%     SENSORS MOVEMENT

        self.sensors_movement2 = tk.BooleanVar()
        self.s_m = tk.Checkbutton(parameters, text='Sensors Movement', variable=self.sensors_movement2,
                                  onvalue=True, offvalue=False, command=self.get_check_value_sensors_movement)
        self.s_m.grid(row=2, column=1, sticky="nw",  pady=5)

        #%%     DEBUG

        self.debug2 = tk.BooleanVar()
        self.d = tk.Checkbutton(parameters, text='Debug', variable=self.debug2,
                                onvalue=True, offvalue=False, command=self.set_debug)
        self.d.grid(row=3, column=1, sticky="nw",  pady=5)

        #%%     DAYS OF SIMULATION

        self.e = tk.Entry(self.parameters, width=5, font=('Helvetica', 18, 'bold'),
                          textvariable=tk.IntVar())
        self.e.grid(row=5, column=1, sticky="nw", padx=5, pady=5)

        button1 = tk.Button(
            self.parameters, text="Set the Days for the Simulation", command=self.set_days)
        button1.grid(row=5, column=1, sticky="ne", padx=5, pady=5)

        #%%    SENSORS PERIOD

        self.e2 = tk.Entry(self.parameters, width=5, font=('Helvetica', 18, 'bold'),
                           textvariable=tk.IntVar())
        self.e2.grid(row=6, column=1, sticky="nw", padx=5, pady=5)

        button2 = tk.Button(
            self.parameters, text="Set the Sensors Sampling Period in Secs", command=self.set_sensors_period)
        button2.grid(row=6, column=1, sticky="e", padx=5, pady=5)

        #%%     SENSORS DISTANCE

        self.e1 = tk.Entry(self.parameters, width=5, font=('Helvetica', 18, 'bold'),
                           textvariable=tk.IntVar())
        self.e1.grid(row=7, column=1, sticky="nw", padx=5,  pady=5)

        button2 = tk.Button(
            self.parameters, text="Set the Distance of the Sensors in Blocks", command=self.set_sensors_distance)
        button2.grid(row=7, column=1, sticky="e", padx=5, pady=5)

        parameters.mainloop()

        #%%     FUNCTIONS FOR THE GUI

    def get_check_value_sensors_movement(self):
        self.sensors_movement = self.sensors_movement2.get()
        #print('na malaka')

    def get_check_value_save_plots(self):
        self.save_plots = self.save_plots2.get()

    def set_days(self):  # THIS IS FOR THE SET DAYS BUTTON IN PARAMETERS
        self.days = self.e.get()

    def set_sensors_distance(self):
        self.sensors_distance = self.e1.get()

    def set_sensors_period(self):
        self.sensors_period = self.e2.get()

    def set_debug(self):
        self.debug = self.debug2.get()

    def close_windows_parameters(self):  # THIS IS FOR THE PARAMETERS BUTTON
        self.parameters.destroy()

    def close_windows(self):  # THIS IS FOR THE QUIT BUTTON
        self.days = 0
        self.master.destroy()

    def start_simulation(self):  # THIS IS FOR THE SET DAYS BUTTON

        if int(self.days) != 0:
            self.master.destroy()


#%% #############  NOT USED OBJECTS  ###############

class Parameters():
    def __init__(self):
        super().__init__(self)

        self.geometry('300x100')
        self.title('Toplevel Window')

        button2 = tk.Button(self, text='Close', command=self.destroy)
        button2.pack()

    def close_windows(self, master):
        # e = tk.Entry(root)
        # e.pack()
        e = tk.Entry(master, width=50)
        e.pack()
        self.master.destroy()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Start(self.newWindow)

    def on_button_press(entry):
        on_button_press.value = entry.get()
        entry.quit()


class Quit:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', padx=60, pady=40,
                                    command=self.close_windows, bg='red', fg='black', bd=5, font=('Helvetica', 18, 'bold'))
        self.quitButton.pack(side=tk.RIGHT)
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
