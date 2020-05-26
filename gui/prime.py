""" GUI entry point """
import json
import tkinter
import tkinter.ttk
from gui.labeled_combobox import LabeledCombobox
from gui.labeled_textarea import LabeledTextarea
from language import factory as lang_factory
from config.constants import GUI_CELL_HEIGHT
from pattern import design_pattern


class Prime:
    """ Primary window """

    _WINDOW_WIDTH = 800
    _WINDOW_HEIGHT = 300

    def __init__(self):
        # Initialization
        self._design_pattern = design_pattern.DesignPattern(design_pattern.PAT_NULL)
        cell_y = 0

        # Main window
        self._root = tkinter.Tk()
        self._root.title("Joseki")
        self._root.geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Language selection
        self._languages = lang_factory.get_all_languages()
        self._language_combo_val = []
        self._build_language_combo_values()
        self._language_combo = LabeledCombobox(
            self._root,
            "Language",
            self._language_combo_val,
            0,
            cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Pattern selection
        self._patterns = LabeledCombobox(
            self._root,
            "Pattern",
            design_pattern.ALL_PATTERNS,
            0,
            cell_y)
        cell_y += GUI_CELL_HEIGHT

        pattern_button = tkinter.Button(self._root, text="Configure", command=self._config_pattern)
        pattern_button.place(x=0, y=cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Config
        self._notes = LabeledTextarea(self._root, "Config", "", 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Generate
        gen_button = tkinter.Button(self._root, text="Generate", command=self._generate)
        gen_button.place(x=0, y=cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Start GUI
        self._root.mainloop()

    def _build_language_combo_values(self):
        for name in self._languages:
            self._language_combo_val.append(name)

    def _config_pattern(self):
        selected_pattern = self._patterns.get_selected_value()
        self._design_pattern = design_pattern.DesignPattern(selected_pattern)
        props = str(self._design_pattern.properties)
        props = props.replace("'", "\"")
        self._notes.set_value(props)

    def _generate(self):
        self._design_pattern.properties = json.loads(self._notes.get_value())
        lang = lang_factory.get_lang_obj(self._language_combo.get_selected_value())
        arts = lang.get_artifacts(self._design_pattern)
        for art in arts:
            art.save_to_disk()
