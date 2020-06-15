""" Labeled text are module """
import tkinter
from config.constants import GUI_CELL_WIDTH


class LabeledTextarea:
    """ Labeled text are class """

    _LINE_FEED = "\r\n"

    def __init__(self,
                 parent: tkinter.Toplevel,
                 label_text: str,
                 text_value,
                 x_pos: int,
                 y_pos: int):
        self._parent = parent
        self._label = tkinter.Label(parent, text=label_text)
        self._label.place(x=x_pos, y=y_pos)
        self._text_box = tkinter.Text(parent, height=10)
        self._text_box.place(x=x_pos + GUI_CELL_WIDTH, y=y_pos)

        if isinstance(text_value, str):
            self.set_value(text_value)
        elif isinstance(text_value, list):
            string_value = ""
            for val in text_value:
                string_value += val
            self.set_value(string_value)

    def disable(self):
        """ Disables control """
        self._text_box.configure(state="disabled")

    def get_value(self):
        """ Returns value in text area """
        return self._text_box.get("1.0", tkinter.END)

    def set_value(self, value: str):
        """ Sets value in text area """
        self._text_box.insert(tkinter.INSERT, value)
        self._parent.update()
