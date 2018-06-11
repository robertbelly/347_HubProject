import remi.gui as gui
from remi import start, App
from threading import Timer
import os


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def idle(self):
        self.counter.set_text('Running Time: ' + str(self.count))

    def main(self):
        # the margin 0px auto centers the main container
        verticalContainer = gui.Widget(width=540, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px',
                                         style={'display': 'block', 'overflow': 'auto'})


        subContainerLeft = gui.Widget(width=320, style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        self.img = gui.Image('/Users/robertbell/PycharmProjects/347Hub/remi-master/working/res/wildcat.png', height=100, margin='10px')
        self.img.set_on_click_listener(self.on_img_clicked)


        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Widget(
            style={'width': '220px', 'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        self.count = 0
        self.counter = gui.Label('', width=200, height=30, margin='10px')

        self.lbl = gui.Label('This is a LABEL!', width=200, height=30, margin='10px')

        self.bt = gui.Button('Press me!', width=200, height=30, margin='10px')
        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self.on_button_pressed)

        self.txt = gui.TextInput(width=200, height=30, margin='10px')
        self.txt.set_text(os.path.join(os.path.dirname(os.path.abspath(__file__))))
        self.txt.set_on_change_listener(self.on_text_area_change)

        self.date = gui.Date('2015-04-13', width=200, height=20, margin='10px')
        self.date.set_on_change_listener(self.date_changed)

        # appending a widget to another, the first argument is a string key
        subContainerRight.append(
            [self.counter, self.lbl, self.bt, self.txt])
        # use a defined key as we replace this widget later
        fdownloader = gui.FileDownloader('download test', '../remi/res/logo.png', width=200, height=30, margin='10px')
        subContainerRight.append(fdownloader, key='file_downloader')
        subContainerRight.append(
            [self.date])
        self.subContainerRight = subContainerRight

        subContainerLeft.append([self.img])

        horizontalContainer.append([subContainerLeft, subContainerRight])

        verticalContainer.append([horizontalContainer])

        # kick of regular display of counter
        self.display_counter()

        # returning the root widget
        return verticalContainer

    def display_counter(self):
        self.count += 1
        Timer(1, self.display_counter).start()

    def menu_dialog_clicked(self, widget):
        self.dialog = gui.GenericDialog(title='Dialog Box', message='Click Ok to transfer content to main page',
                                        width='500px')
        self.dtextinput = gui.TextInput(width=200, height=30)
        self.dtextinput.set_value('Initial Text')
        self.dialog.add_field_with_label('dtextinput', 'Text Input', self.dtextinput)

        self.dcheck = gui.CheckBox(False, width=200, height=30)
        self.dialog.add_field_with_label('dcheck', 'Label Checkbox', self.dcheck)
        values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        self.dialog.add_field_with_label('dlistView', 'Listview', self.dlistView)

        self.ddropdown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                    width=200, height=20)
        self.dialog.add_field_with_label('ddropdown', 'Dropdown', self.ddropdown)

        self.dspinbox = gui.SpinBox(min=0, max=5000, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dspinbox', 'Spinbox', self.dspinbox)

        self.dslider = gui.Slider(10, 0, 100, 5, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dslider', 'Slider', self.dslider)

        self.dcolor = gui.ColorPicker(width=200, height=20)
        self.dcolor.set_value('#ffff00')
        self.dialog.add_field_with_label('dcolor', 'Colour Picker', self.dcolor)

        self.ddate = gui.Date(width=200, height=20)
        self.ddate.set_value('2000-01-01')
        self.dialog.add_field_with_label('ddate', 'Date', self.ddate)

        self.dialog.set_on_confirm_dialog_listener(self.dialog_confirm)
        self.dialog.show(self)

    def dialog_confirm(self, widget):
        result = self.dialog.get_field('dtextinput').get_value()
        self.txt.set_value(result)

        result = self.dialog.get_field('ddropdown').get_value()
        self.dropDown.select_by_value(result)

        result = self.dialog.get_field('dspinbox').get_value()
        self.spin.set_value(result)

        result = self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

        result = self.dialog.get_field('dcolor').get_value()
        self.colorPicker.set_value(result)

        result = self.dialog.get_field('ddate').get_value()
        self.date.set_value(result)

        result = self.dialog.get_field('dlistView').get_value()
        self.listView.select_by_value(result)

    # listener function
    def on_img_clicked(self, widget):
        self.lbl.set_text('Image clicked!')

    def on_table_row_click(self, table, row, item):
        self.lbl.set_text('Table Item clicked: ' + item.get_text())

    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed! ')
        self.bt.set_text('Hi!')

    def on_text_area_change(self, widget, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, widget, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def on_check_change(self, widget, newValue):
        self.lbl.set_text('CheckBox changed, new value: ' + str(newValue))

    def open_input_dialog(self, widget):
        self.inputDialog = gui.InputDialog('Input Dialog', 'Your name?',
                                           initial_value='type here',
                                           width=500, height=160)
        self.inputDialog.set_on_confirm_value_listener(
            self.on_input_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, widget, value):
        self.lbl.set_text('Hello ' + value)

    def open_fileselection_dialog(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.set_on_confirm_value_listener(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_fileselection_dialog_confirm(self, widget, filelist):
        # a list() of filenames and folders is returned
        self.lbl.set_text('Selected files: %s' % ','.join(filelist))
        if len(filelist):
            f = filelist[0]
            # replace the last download link
            fdownloader = gui.FileDownloader("download selected", f, width=200, height=30)
            self.subContainerRight.append(fdownloader, key='file_downloader')

    def list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        self.lbl.set_text('List selection: ' + self.listView.children[selected_item_key].get_text())

    def drop_down_changed(self, widget, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, widget, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, widget, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, widget, value):
        self.lbl.set_text('New date value: ' + value)

    def menu_save_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save')

    def menu_saveas_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save As')

    def menu_open_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Open')

    def menu_view_clicked(self, widget):
        self.lbl.set_text('Menu clicked: View')

    def fileupload_on_success(self, widget, filename):
        self.lbl.set_text('File upload success: ' + filename)

    def fileupload_on_failed(self, widget, filename):
        self.lbl.set_text('File upload failed: ' + filename)


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    import ssl

    # start(MyApp, debug=True, address='0.0.0.0', start_browser=True, multiple_instance=True)