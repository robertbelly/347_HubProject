import remi.gui as gui
from remi import start, App


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):

        vertContainer = gui.Widget(width='80%', layout_orientation=gui.Widget.LAYOUT_VERTICAL, margin='0px auto',
                                   style={'display': 'block', 'overflow': 'auto', 'background-color': '#BEBEBE'})
        vertContainer.style['text-align'] = 'center'
        vertContainer.style['align-items'] = 'center'
        vertContainer.style['justify-content'] = 'center'

        wid = gui.VBox(width=300, height=200, margin='0px auto')
        self.lbl1 = gui.Label('bottom text')
        self.lbl1.style['margin'] = 'auto'
        wid.append(self.lbl1)

        self.img = gui.Image('/res/wildcat.png', height=150, margin='0px auto')

        b1 = gui.Button('Add new tab', width=200, height=30)
        b2 = gui.Button('Show third tab', width=200, height=30)
        b3 = gui.Button('Show first tab', width=200, height=30)

        tb = gui.TabBox(width='100%')
        tb.add_tab([b1,b2], 'First', None)


        b1.set_on_click_listener(self.on_bt1_pressed, tb, 0)
        b2.set_on_click_listener(self.on_bt2_pressed, tb, 0)

        vertContainer.append(tb)

        return vertContainer

    def on_bt1_pressed(self, widget, tabbox, refWidgetTab):
        self.newlbl = gui.Label("new tab")
        tabbox.add_tab(self.newlbl, "new tab", None)

    def on_bt2_pressed(self, widget, tabbox, refWidgetTab):
        tabbox.close()

if __name__ == "__main__":
    start(MyApp, title="Tab Demo", standalone=False)