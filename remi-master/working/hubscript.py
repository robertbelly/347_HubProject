"""
Edit this file for actually
implementing the hub functions
"""


import remi.gui as gui
from remi import start, App
import threading, time
from functionsForExample import myrandomfunction,returntime
import hub_spi as pispi


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)


    def idle(self):
        self.lbl.set_text(str(self.my_thread_result))
        self.sensorlabel.set_text("Sensor value: " + str(self.my_thread_result2))

    def main(self):

        # Make containers
        vertContainer = gui.Widget(width='100%', height=300, layout_orientation=gui.Widget.LAYOUT_VERTICAL, margin='0px auto',
                                         style={'display': 'block', 'overflow': 'auto', 'background-color': '#BEBEBE'})
        vertContainer.style['text-align'] = 'center'

        wid = gui.HBox(width=300, height=150, margin='0px auto')
        wid.style['align-items'] = 'center'
        wid.style['justify-content'] = 'baseline'
        wid.style['font-size'] = '30px'
        wid.style['background-color'] = '#BEBEBE'

        buttonContainer = gui.HBox(width='80%', height=100, margin='0px auto')
        buttonContainer.style['align-items'] = 'baseline'
        buttonContainer.style['justify-content'] = 'space-around'
        buttonContainer.style['background-color'] = '#BEBEBE'
        buttonContainer.style['text-align'] = 'center'

        labelContainer = gui.HBox(width='80%', height=50, margin='0px auto')
        labelContainer.style['align-items'] = 'baseline'
        labelContainer.style['justify-content'] = 'space-around'
        labelContainer.style['background-color'] = '#BEBEBE'
        labelContainer.style['text-align'] = 'center'

        # Components
        #self.img = gui.Image('/res/wildcat.png', height=150, margin='0px auto')

        self.lbl = gui.Label('', width='80%', height=100, margin='0px auto',style="position: absolute")
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

        bt2 = gui.Button('Shut off', width=200, height=50)
        bt2.style['margin'] = 'auto 50px'
        bt2.style['background-color'] = '#9876aa'
        bt2.style['color'] = '#2b2b2b'

        self.sensorlabel = gui.Label('sensor value', width='80%', height=100, margin='0px auto',
                                     style="position: absolute")
        self.sensorlabel.style['margin'] = 'auto'
        self.sensorlabel.style['font-weight'] = 'bold'
        self.sensorlabel.style['color'] = '#000000'

        self.onofflabel = gui.Label('On/Off value', width='80%', height=100, margin='0px auto',
                                    style="position: absolute")
        self.onofflabel.style['margin'] = 'auto'
        self.onofflabel.style['font-weight'] = 'bold'
        self.onofflabel.style['color'] = '#000000'

        current_process = "No current process"
        self.process_label = gui.Label(current_process, width='80%', height=50, margin='0px auto',style="position: absolute")
        labelContainer.append(self.process_label)

        # Containers Code
        wid.append(self.lbl)
        #wid.append(self.img)
        buttonContainer.append(bt)
        buttonContainer.append(bt1)
        buttonContainer.append(bt2)

        vertContainer.append([wid,labelContainer,buttonContainer])

        tb = gui.TabBox(width='100%')
        tb.style['background-color'] = '#BEBEBE'
        tb.add_tab(vertContainer, "Home Screen", None)

        # Actions

        bt.set_on_click_listener(self.sensor_button_pressed, tb)
        bt1.set_on_click_listener(self.onoff_button_pressed, tb)
        bt2.set_on_click_listener(self.shutdown_button)

        # Thread code
        self.thread_alive_flag = True
        self.my_thread_result = 'n/a'
        self.my_thread_result2 = 'n/a'
        t = threading.Thread(target=self.my_algorithm)
        t.start()

        self.COUNTER = 0

        # returning the root widget
        return tb


    # Functions

    def sensor_button_pressed(self, container, tabbox):

        # On button press, create new tab for the module
        self.process_label.set_text("Initiated sensor pairing...")
        self.do_gui_update()
        # Subcontainer for the 'pairing initiated box'
        mainmessageContainer = gui.Widget(width='100%', height=250, layout_orientation=gui.Widget.LAYOUT_VERTICAL, margin='0px auto',
                                         style={'display': 'block', 'overflow': 'auto', 'background-color': '#BEBEBE'})
        mainmessageContainer.style['text-align'] = 'center'
        mainmessageContainer.style['align-items'] = 'center'
        mainmessageContainer.style['justify-content'] = 'space-around'
        mainmessageContainer.style['font-size'] = '20px'

        self.newlabel = gui.Label('Sensor Module', width='60%', height=50, margin='0px auto')#,style="position: absolute")

        buttonBox = gui.HBox(width='80%', height=100, margin='0px auto')
        buttonBox.style['align-items'] = 'center'
        buttonBox.style['justify-content'] = 'space-around'
        buttonBox.style['background-color'] = '#BEBEBE'

        button_ReturnToHome = gui.Button('Return to Home Screen', width=200, height=50)
        button_ReturnToHome.style['margin'] = 'auto 50px'
        button_ReturnToHome.style['background-color'] = '#9876aa'
        button_ReturnToHome.style['color'] = '#2b2b2b'

        labelContainer = gui.HBox(width='80%', height=50, margin='0px auto')
        labelContainer.style['align-items'] = 'baseline'
        labelContainer.style['justify-content'] = 'space-around'
        labelContainer.style['background-color'] = '#BEBEBE'
        labelContainer.style['text-align'] = 'center'
        labelContainer.append(self.sensorlabel)

        button_ReturnToHome.set_on_click_listener(self.on_bt_pressed, tabbox, 0)

        buttonBox.append(button_ReturnToHome)
        mainmessageContainer.append([self.newlabel, labelContainer, buttonBox])

        # Display the result of the pairing
        pairing_return = pispi.init_pairing()
        self.newlabel2 = pairing_return
        if pairing_return:
            self.process_label.set_text("Pairing successful")
            self.COUNTER = self.COUNTER + 1
            tabbox.add_tab(mainmessageContainer, "Sensor Module", None)
        else:
            self.process_label.set_text("Pairing failed")
        self.do_gui_update()
        time.sleep(2)
        self.process_label.set_text("No current process")
        self.do_gui_update()

        t2 = threading.Thread(target=self.my_2algorithm)
        t2.start()
        #self.sensorlabel.set_text(self.my_thread_result2)

    def onoff_button_pressed(self, container, tabbox):

        # On button press, create new tab for the module
        self.process_label.set_text("Initiated On/Off pairing...")
        self.do_gui_update()
        # Subcontainer for the info display box
        mainmessageContainer = gui.Widget(width='100%', height=250, layout_orientation=gui.Widget.LAYOUT_VERTICAL, margin='0px auto',
                                         style={'display': 'block', 'overflow': 'auto', 'background-color': '#BEBEBE'})
        mainmessageContainer.style['text-align'] = 'center'
        mainmessageContainer.style['align-items'] = 'center'
        mainmessageContainer.style['justify-content'] = 'space-around'
        mainmessageContainer.style['font-size'] = '20px'

        self.newlabel = gui.Label('On/Off Module', width='60%', height=150, margin='0px auto')#,style="position: absolute")

        buttonBox = gui.HBox(width='80%', height=100, margin='0px auto')
        buttonBox.style['align-items'] = 'center'
        buttonBox.style['justify-content'] = 'space-around'
        buttonBox.style['background-color'] = '#BEBEBE'

        button_ON = gui.Button('Turn ON', width=200, height=50)
        button_ON.style['margin'] = 'auto 50px'
        button_ON.style['background-color'] = '#9876aa'
        button_ON.style['color'] = '#2b2b2b'

        button_OFF = gui.Button('Turn OFF', width=200, height=50)
        button_OFF.style['margin'] = 'auto 50px'
        button_OFF.style['background-color'] = '#9876aa'
        button_OFF.style['color'] = '#2b2b2b'

        button_ReturnToHome = gui.Button('Return to Home Screen', width=200, height=50)
        button_ReturnToHome.style['margin'] = 'auto 50px'
        button_ReturnToHome.style['background-color'] = '#9876aa'
        button_ReturnToHome.style['color'] = '#2b2b2b'

        labelContainer = gui.HBox(width='80%', height=50, margin='0px auto')
        labelContainer.style['align-items'] = 'baseline'
        labelContainer.style['justify-content'] = 'space-around'
        labelContainer.style['background-color'] = '#BEBEBE'
        labelContainer.style['text-align'] = 'center'
        labelContainer.append(self.sensorlabel)

        button_ReturnToHome.set_on_click_listener(self.on_bt_pressed, tabbox, 0)
        button_ON.set_on_click_listener(self.turn_on_button, 2)
        button_OFF.set_on_click_listener(self.turn_off_button, 2)

        buttonBox.append(button_ON)
        buttonBox.append(button_OFF)
        buttonBox.append(button_ReturnToHome)
        mainmessageContainer.append([self.newlabel, labelContainer, buttonBox])

        # Display the result of the pairing

        pairing_return = pispi.init_pairing()
        self.newlabel2 = pairing_return
        if pairing_return:
            self.process_label.set_text("Pairing successful")
            self.COUNTER = self.COUNTER + 1
            tabbox.add_tab(mainmessageContainer, "On/Off Module", None)
        else:
            self.process_label.set_text("Pairing failed")
        self.do_gui_update()
        time.sleep(2)
        self.process_label.set_text("No current process")
        self.do_gui_update()


    def on_bt_pressed(self, widget, tabbox, tabIndex):
        tabbox.select_by_index(tabIndex)

    def turn_off_button(self, emitter, tabIndex):
        pispi.new_value_set(tabIndex, pispi.CHAR_ONOFF, 0)
        self.onofflabel.set_text("Current status: Off")

    def turn_on_button(self, emitter, tabIndex):
        pispi.new_value_set(tabIndex, pispi.CHAR_ONOFF, 1)
        self.onofflabel.set_text("Current status: On")

    def shutdown_button(self, _):
        self.process_label.set_text("Bye!")
        self.do_gui_update()
        self.close()

    def my_algorithm(self):
        while self.thread_alive_flag:
            self.my_thread_result = returntime()

    def my_2algorithm(self):
        while self.thread_alive_flag:
            self.my_thread_result2 = pispi.read_chars(0)
            self.do_gui_update()

    def start_thread(self):
        self.thread_alive_flag = True
        self.my_thread_result = 'n/a'
        t = threading.Thread(target=self.my_algorithm)
        t.start()


if __name__ == "__main__":
    start(MyApp, debug=True, update_interval=.5)
