"""
Use this file for testing functionality
of the various things
"""

import remi.gui as gui
from remi import start, App
import threading, time
from functionsForExample import myrandomfunction, returntime


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)


    def idle(self):
        self.lbl.set_text('Thread result:  ' + str(self.my_thread_result))


    def main(self):
        # margin 0px auto allows to center the app to the screen

        horizontalContainer = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_VERTICAL, margin='0px auto',
                                         style={'display': 'block', 'overflow': 'auto', 'background-color': '#b6b6b6'})


        wid = gui.VBox(width=300, height=200, margin='0px auto')


        self.lbl = gui.Label('Thread result:', width='80%', height='50%')
        self.lbl.style['margin'] = 'auto'

        self.lbl1 = gui.Label('bottom text')
        self.lbl1.style['margin'] = 'auto'

        bt = gui.Button('Start algorithm', width=200, height=30)
        bt.style['margin'] = 'auto 50px'
        bt.style['background-color'] = 'red'

        bt1 = gui.Button('Stop algorithm', width=200, height=30)
        bt1.style['margin'] = 'auto 50px'
        bt1.style['background-color'] = 'red'

        bt2 = gui.Button('Stop algorithm', width=200, height=30)
        bt2.style['margin'] = 'auto 50px'
        bt2.style['background-color'] = 'red'

        wid.append(self.lbl)
        wid.append(bt)
        wid.append(bt1)
        wid.append(bt2)
        wid.append(self.lbl1)

        self.thread_alive_flag = False
        self.my_thread_result = "Not started yet"

        bt.set_on_click_listener(self.on_button_pressed)
        bt1.set_on_click_listener(self.off_button_pressed)
        bt2.set_on_click_listener(self.add_field)

        horizontalContainer.append([wid])

        # returning the root widget
        return horizontalContainer

    def my_algorithm(self):
        but = gui.Button('new button', width=200, height=30)
        while self.thread_alive_flag:
            self.my_thread_result = myrandomfunction()

    def start_thread(self):
        t = threading.Thread(target=self.my_algorithm)
        t.start()

    def on_button_pressed(self, emitter):
        self.thread_alive_flag = True
        var = self.thread_alive_flag
        self.lbl1.set_text(str(var))
        self.start_thread()

    def off_button_pressed(self, emitter):
        self.thread_alive_flag = False
        var = self.thread_alive_flag
        self.lbl1.set_text(str(var))
        self.my_thread_result = "Turned off"

    def add_field(self, container):
        newbutton = gui.Button('New button!', width=200, height=30)
        newbutton.style['margin'] = 'auto 50px'
        newbutton.style['background-color'] = 'blue'
        container.append(newbutton)


if __name__ == "__main__":
    start(MyApp, debug=True, update_interval=1)
