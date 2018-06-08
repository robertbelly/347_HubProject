
import remi.gui as gui
from remi import start, App
import os
from pathlib import Path

class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)


    def idle(self):
        #idle loop, you can place here custom code
        # avoid to use infinite iterations, it would stop gui update
        pass


    def main(self):
        #creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, height=200, style={'margin':'0px auto'})

        my_file = Path("/res/wildcat.png")
        if my_file.is_file():
            texttoprint = "True"
        else: texttoprint = "False"

        self.img = gui.Image('/res/wildcat.png', height=100, margin='0px auto')
        self.lbl = gui.Label(texttoprint)

        main_container.append(self.img)
        main_container.append(self.lbl)

        # returning the root widget
        return main_container


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='127.0.0.1', port=8081, host_name=None, start_browser=True, username=None, password=None)
