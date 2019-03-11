from config.constants import *
import tkinter
import tkinter.ttk


class LabeledCombobox:

    def __init__(self, parent: tkinter.Toplevel, label_text: str, combo_values: [], x_pos: int, y_pos: int, width=0):
        self._label = tkinter.Label(parent, text=label_text)
        self._label.place(x=x_pos, y=y_pos)
        self._selected_value = tkinter.StringVar()

        if width > 0:
            self._combobox = tkinter.ttk.Combobox(parent, textvariable=self._selected_value, width=50)
        else:
            self._combobox = tkinter.ttk.Combobox(parent, textvariable=self._selected_value)

        self._combobox.config(values=combo_values)
        self._combobox.place(x=x_pos + GUI_CELL_WIDTH, y=y_pos)

    def get_selected_value(self) -> str:
        return self._selected_value.get()

    def set_selected_value(self, value: str):
        self._selected_value.set(value)
