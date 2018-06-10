"""
Edit this file for actually
implementing the hub functions
"""


import remi.gui as gui
from remi import start, App
import threading, time
from functionsForExample import myrandomfunction,returntime
#import hub_spi.py as pispi


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)


    def idle(self):
        self.lbl.set_text(str(self.my_thread_result))


    def main(self):

        # Make containers
        vertContainer = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_VERTICAL, margin='0px auto',
                                         style={'display': 'block', 'overflow': 'auto', 'background-color': '#BEBEBE'})
        vertContainer.style['text-align'] = 'center'

        wid = gui.HBox(width=300, height=200, margin='20px auto')
        wid.style['align-items'] = 'center'
        wid.style['justify-content'] = 'space-around'
        wid.style['font-size'] = '30px'
        wid.style['background-color'] = '#BEBEBE'

        buttonContainer = gui.HBox(width='80%', height=200, margin='0px auto')
        buttonContainer.style['align-items'] = 'baseline'
        buttonContainer.style['justify-content'] = 'space-around'
        buttonContainer.style['background-color'] = '#BEBEBE'

        # Components
        self.img = gui.Image('/res/wildcat.png', height=150, margin='0px auto')

        self.lbl = gui.Label('', width='80%', height=150, margin='0px auto',style="position: absolute")
        self.lbl.style['margin'] = 'auto'
        self.lbl.style['font-weight'] = 'bold'
        self.lbl.style['color'] = '#000000'

        bt = gui.Button('Add Sensor Module', width=200, height=50)
        bt.style['margin'] = 'auto 50px'
        bt.style['background-color'] = '#9876aa'
        bt.style['color'] = '#2b2b2b'

        bt1 = gui.Button('Add On/Off Module', width=200, height=50)
        bt1.style['margin'] = 'auto 50px'
        bt1.style['background-color'] = '#9876aa'
        bt1.style['color'] = '#2b2b2b'

        bt2 = gui.Button('Button 3', width=200, height=50)
        bt2.style['margin'] = 'auto 50px'
        bt2.style['background-color'] = '#9876aa'
        bt2.style['color'] = '#2b2b2b'


        # Containers Code
        wid.append(self.lbl)
        wid.append(self.img)
        buttonContainer.append(bt)
        buttonContainer.append(bt1)
        buttonContainer.append(bt2)

        tb = gui.TabBox(width='100%')
        tb.style['background-color'] = '#BEBEBE'
        tb.add_tab([wid,buttonContainer], "Home Screen", None)

        vertContainer.append(tb)


        # Actions

        bt.set_on_click_listener(self.on_button_pressed, tb)

        # Thread code
        self.thread_alive_flag = True
        self.my_thread_result = 'n/a'
        t = threading.Thread(target=self.my_algorithm)
        t.start()

        # returning the root widget
        return vertContainer


    # Functions

    def on_button_pressed(self, container, tabbox):

        # On button press, create new tab for the module

        self.newlabel = gui.Label('Pairing initiated', width='80%', height=150, margin='0px auto',style="position: absolute")
        tabbox.add_tab(self.newlabel, "new tab", None)
        # container.append(self.newlabel)
        # self.newlabel2 = gui.Label('Test', width='80%', height=150, margin='0px auto',style="position: absolute")

        # Display the result of the pairing
        pairing_return = pispi.init_pairing()
        self.newlabel2 = pairing_return
        self.newlabel = gui.Label('', width='80%', height=150, margin='0px auto',
                                  style="position: absolute")
        container.append(self.newlabel)
        container.append(self.newlabel2)
        self.my_thread_result = pairing_return


    def my_algorithm(self):
        while self.thread_alive_flag:
            self.my_thread_result = returntime()

    def start_thread(self):
        return

if __name__ == "__main__":
    start(MyApp, debug=True, update_interval=.5)
