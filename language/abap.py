""" ABAP module """
from language.abstract_language import AbstractLanguage
from artifact.artifact import Artifact
from pattern.design_pattern import \
    PAT_CACHED_DATA, PAT_LAZY_INITIALIZATION, PAT_MULTITON, PAT_NULL, DesignPattern


class Abap(AbstractLanguage):
    """ ABAP language """

    _FILE_EXTENSION = ".abap"

    def __init__(self):
        super().__init__()
        self._pattern = DesignPattern(PAT_NULL)

    def get_artifacts(self, pattern: DesignPattern) -> []:
        self._pattern = pattern

        if self._pattern.name == PAT_NULL:
            raise Exception("No pattern assigned")
        if self._pattern.name == PAT_CACHED_DATA:
            return self._get_artifacts_of_cached_data()
        if self._pattern.name == PAT_LAZY_INITIALIZATION:
            return self._get_artifacts_of_lazy_initialization()
        if self._pattern.name == PAT_MULTITON:
            return self._get_artifacts_of_multiton()
        raise Exception("Unsupported pattern: " + self._pattern.name)

    def _get_artifacts_of_cached_data(self) -> []:

        method_name = self._pattern.properties["method_name"].lower()
        entered_type = self._pattern.properties["type_name"].lower()
        type_name = entered_type + "_dict"
        key_type_name = entered_type + "_key_dict"
        fld_type_name = entered_type + "_fld_dict"
        table_type_name = entered_type + "_list"
        variable = self._pattern.properties["variable"].lower()
        itab_name = variable + "s"
        field_symbol = "<" + variable + ">"
        work_area = variable
        static = self._pattern.properties["scope"].lower() == "static"

        if "exception" in self._pattern.properties:
            exception = self._pattern.properties["exception"]
        else:
            exception = ""

        art = Artifact()
        art.name = method_name
        art.file_name = art.name + Abap._FILE_EXTENSION

        art.content.append("##TODO. \" Move this type to the class header")
        art.content.append("  TYPES: BEGIN OF " + key_type_name + ",")
        for key in self._pattern.properties["keys"]:
            art.content.append("           " + key["name"] + " TYPE " + key["type"] + ",")
        art.content.append("         END OF " + key_type_name + ".")
        art.content.append("")
        art.content.append("  TYPES: BEGIN OF " + fld_type_name + ",")
        for fld in self._pattern.properties["fields"]:
            art.content.append("           " + fld["name"] + " TYPE " + fld["type"] + ",")
        art.content.append("         END OF " + fld_type_name + ".")
        art.content.append("")
        art.content.append("  TYPES: BEGIN OF " + type_name + ",")
        art.content.append("           key TYPE " + key_type_name + ",")
        art.content.append("           fld TYPE " + fld_type_name + ",")
        if exception != "":
            art.content.append("           cx  TYPE REF TO cx_no_entry_in_table,")
        art.content.append("         END OF " + type_name + ",")
        art.content.append("")

        tt_line = "         " + table_type_name + " TYPE HASHED TABLE OF " + type_name
        tt_line += " WITH UNIQUE KEY primary_key COMPONENTS key."
        art.content.append(tt_line)
        art.content.append("")

        art.content.append("##TODO. \" Move this data definition to the class header")
        data_line = "  "
        if static:
            data_line = "CLASS-"
        data_line += "DATA " + itab_name + " TYPE " + table_type_name + "."
        art.content.append(data_line)

        art.content.append("")
        art.content.append("##TODO. \" Move this method definition to the class header")
        meth_line = "    "
        if static:
            meth_line = "CLASS-"
        meth_line += "METHODS " + method_name
        art.content.append(meth_line)
        art.content.append("  IMPORTING !key TYPE " + key_type_name)
        ret_line = "  RETURNING VALUE(fld) TYPE " + fld_type_name
        if exception == "":
            art.content.append(ret_line + ".")
        else:
            art.content.append(ret_line)
            art.content.append("  RAISING   " + exception + ".")

        art.content.append("")
        art.content.append("##TODO. \" Move this method implementation to the class body")
        art.content.append("  METHOD " + art.name.lower() + ".")
        art.content.append("    ASSIGN me->" + itab_name + "[")
        art.content.append("        KEY primary_key COMPONENTS key = key")
        art.content.append("      ] TO FIELD-SYMBOL(" + field_symbol + ").")
        art.content.append("    IF sy-subrc <> 0.")
        art.content.append("      DATA(" + work_area + ") = VALUE " + type_name + "( key = key ).")
        art.content.append("")
        if exception != "":
            art.content.append("      TRY.")

        fill_line = "          ##TODO. \" Fill " + work_area + "-FLD here"
        if exception != "":
            fill_line += " and raise " + exception + " if needed"
        art.content.append(fill_line)

        if exception != "":
            art.content.append("        CATCH " + exception + " INTO " + work_area + "-cx ##NO_HANDLER.") # pylint: disable=C0301
            art.content.append("      ENDTRY.")

        art.content.append("")
        art.content.append("      INSERT " + work_area + " INTO TABLE me->" + itab_name + " ASSIGNING " + field_symbol + ".")
        art.content.append("    ENDIF.")
        art.content.append("")
        if exception != "":
            art.content.append("    IF " + field_symbol + "-cx IS NOT INITIAL.")
            art.content.append("      RAISE EXCEPTION " + field_symbol + "-cx.")
            art.content.append("    ENDIF.")
            art.content.append("")
        art.content.append("    fld = " + field_symbol + "-fld.")

        art.content.append("  ENDMETHOD.")

        return [art]

    def _get_artifacts_of_lazy_initialization(self) -> []:
        method_name = self._pattern.properties["method_name"].lower()
        static = self._pattern.properties["scope"].lower() == "static"
        variable = self._pattern.properties["variable"].lower()
        type_name = self._pattern.properties["type_name"].lower()
        flag = variable + "_read"

        if "exception" in self._pattern.properties:
            exception = self._pattern.properties["exception"]
        else:
            exception = ""

        art = Artifact()
        art.name = method_name
        art.file_name = art.name + Abap._FILE_EXTENSION

        art.content.append("##TODO. \" Move data definitions to class header")
        data_line = "    "
        if static:
            data_line += "CLASS-"
        data_line += "DATA: "
        art.content.append(data_line)
        art.content.append("      " + variable + " TYPE " + type_name + ",")
        art.content.append("      " + flag + " TYPE abap_bool.")
        art.content.append("")

        art.content.append("##TODO. \" Move method definition to class header")
        method_line = "    "
        if static:
            method_line += "CLASS-"
        method_line += "METHODS " + method_name
        if exception != "":
            method_line += " RAISING " + exception
        method_line += "."
        art.content.append(method_line)
        art.content.append("")

        art.content.append("##TODO. \" Move method to class body")
        art.content.append("  METHOD " + method_name + ".")
        art.content.append("    CHECK " + flag + " = abap_false.")
        art.content.append("")
        todo_line = "    ##TODO. \" Fill " + variable
        if exception != "":
            todo_line += " and raise " + exception + " if needed"
        art.content.append(todo_line)
        art.content.append("")
        art.content.append("    " + flag + " = abap_true.")
        art.content.append("  ENDMETHOD.")

        return [art]

    def _get_artifacts_of_multiton(self) -> []:

        ##############################
        # Initialization
        ##############################

        art = Artifact()
        art.name = self._pattern.properties["class_name"]
        art.description = self._pattern.properties["class_description"]
        art.file_name = art.name + Abap._FILE_EXTENSION

        ##############################
        # Class definition
        ##############################

        art.content.append("CLASS " + art.name + " DEFINITION PUBLIC FINAL CREATE PRIVATE.")
        art.content.append("")
        art.content.append("  PUBLIC SECTION.")
        art.content.append("    TYPES: BEGIN OF key_dict,")
        for key in self._pattern.properties["keys"]:
            art.content.append("             " + key["name"].lower() + " TYPE " + key["type"].lower() + ",")
        art.content.append("           END OF key_dict.")
        art.content.append("")
        art.content.append("    DATA def TYPE " + self._pattern.properties["master_table"].lower() + " READ-ONLY.")
        art.content.append("")
        art.content.append("    CLASS-METHODS get_instance")
        art.content.append("      IMPORTING !key TYPE key_dict")
        art.content.append("      RETURNING VALUE(obj) TYPE REF TO " + art.name.lower())
        art.content.append("      RAISING   cx_no_entry_in_table.")
        art.content.append("")
        art.content.append("  PROTECTED SECTION.")
        art.content.append("")
        art.content.append("  PRIVATE SECTION.")
        art.content.append("    TYPES: BEGIN OF multiton_dict,")
        art.content.append("             key TYPE key_dict,")
        art.content.append("             obj TYPE REF TO " + art.name.lower() + ",")
        art.content.append("             cx  TYPE REF TO cx_no_entry_in_table,")
        art.content.append("           END OF multiton_dict,")
        art.content.append("")
        art.content.append("           multiton_set TYPE HASHED TABLE OF multiton_dict")
        art.content.append("                        WITH UNIQUE KEY primary_key COMPONENTS key.")
        art.content.append("")
        art.content.append("    CONSTANTS: BEGIN OF table,")
        art.content.append("                 def TYPE tabname VALUE '" + self._pattern.properties["master_table"].upper() + "',")
        art.content.append("               END OF table.")
        art.content.append("")
        art.content.append("    CLASS-DATA multitons TYPE multiton_set.")
        art.content.append("")
        art.content.append("    METHODS constructor")
        art.content.append("      IMPORTING !key TYPE key_dict")
        art.content.append("      RAISING   cx_no_entry_in_table.")
        art.content.append("ENDCLASS.")
        art.content.append("")

        ##############################
        # Class implementation
        ##############################

        art.content.append("CLASS " + art.name + " IMPLEMENTATION.")
        art.content.append("  METHOD constructor.")
        art.content.append("    SELECT SINGLE *")
        art.content.append("           FROM " + self._pattern.properties["master_table"].lower())


        pos = 0
        for key in self._pattern.properties["keys"]:
            if pos == 0:
                line = "           WHERE "
            else:
                line = "                 "
            line += key["name"].lower() + " = @key-" + key["name"].lower()
            pos += 1
            if pos < len(self._pattern.properties["keys"]):
                line += " AND"
            art.content.append(line)

        art.content.append("           INTO CORRESPONDING FIELDS OF @me->def.")
        art.content.append("")
        art.content.append("    IF sy-subrc <> 0.")
        art.content.append("      RAISE EXCEPTION TYPE cx_no_entry_in_table")
        art.content.append("        EXPORTING")
        art.content.append("          table_name = CONV #( table-def )")
        entry_name = ""
        for key in self._pattern.properties["keys"]:
            if entry_name != "":
                entry_name += " "
            entry_name += "{ key-" + key["name"].lower() + " }"
        art.content.append("          entry_name = |" + entry_name + "|.")
        art.content.append("    ENDIF.")
        art.content.append("  ENDMETHOD.")
        art.content.append("")
        art.content.append("")
        art.content.append("  METHOD get_instance.")
        art.content.append("    ASSIGN multitons[ KEY primary_key COMPONENTS key = key")
        art.content.append("                    ] TO FIELD-SYMBOL(<multiton>).")
        art.content.append("    IF sy-subrc <> 0.")
        art.content.append("      DATA(multiton) = VALUE multiton_dict( key = key ).")
        art.content.append("")
        art.content.append("      TRY.")
        art.content.append("          multiton-obj = NEW #( multiton-key ).")
        art.content.append("        CATCH cx_no_entry_in_table INTO multiton-cx ##NO_HANDLER.")
        art.content.append("      ENDTRY.")
        art.content.append("")
        art.content.append("      INSERT multiton INTO TABLE multitons ASSIGNING <multiton>.")
        art.content.append("    ENDIF.")
        art.content.append("")
        art.content.append("    IF <multiton>-cx IS NOT INITIAL.")
        art.content.append("      RAISE EXCEPTION <multiton>-cx.")
        art.content.append("    ENDIF.")
        art.content.append("")
        art.content.append("    obj = <multiton>-obj.")
        art.content.append("  ENDMETHOD.")
        art.content.append("ENDCLASS.")

        ##############################
        # Closure
        ##############################

        return [art]
