from language.abstract_language import AbstractLanguage
from artifact.artifact import Artifact
from pattern.design_pattern import *


class Abap(AbstractLanguage):

    _FILE_EXTENSION = ".txt"

    def __init__(self):
        self._pattern = DesignPattern(PAT_NULL)

    def get_artifacts(self, pattern: DesignPattern) -> []:
        self._pattern = pattern

        if self._pattern.name == PAT_NULL:
            raise Exception("No pattern assigned")
        elif self._pattern.name == PAT_MULTITON:
            return self._get_artifacts_of_multiton()
        else:
            raise Exception("Unsupported pattern: " + self._pattern.name)

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

        art.content.append("CLASS " + art.name + " DEFINITION CREATE PRIVATE.")
        art.content.append("")
        art.content.append("  PUBLIC SECTION.")
        art.content.append("")
        art.content.append("    TYPES:")
        art.content.append("      BEGIN OF t_key,")
        for key in self._pattern.properties["keys"]:
            art.content.append("        " + key["name"].lower() + " TYPE " + key["type"].lower() + ",")
        art.content.append("      END OF t_key.")
        art.content.append("")
        art.content.append("    DATA gs_def TYPE " + self._pattern.properties["master_table"].lower() + " READ-ONLY.")
        art.content.append("")
        art.content.append("    CLASS-METHODS:")
        art.content.append("      get_instance")
        art.content.append("        IMPORTING !is_key TYPE t_key")
        art.content.append("        RETURNING VALUE(ro_obj) TYPE REF TO " + art.name.lower())
        art.content.append("        RAISING   cx_no_entry_in_table.")
        art.content.append("")
        art.content.append("  PROTECTED SECTION.")
        art.content.append("")
        art.content.append("  PRIVATE SECTION.")
        art.content.append("")
        art.content.append("    TYPES:")
        art.content.append("      BEGIN OF t_multiton,")
        art.content.append("        key TYPE t_key,")
        art.content.append("        obj TYPE REF TO " + art.name.lower() + ",")
        art.content.append("        cx  TYPE REF TO cx_no_entry_in_table,")
        art.content.append("      END OF t_multiton,")
        art.content.append("")
        art.content.append("      tt_multiton")
        art.content.append("        TYPE HASHED TABLE OF t_multiton")
        art.content.append("        WITH UNIQUE KEY primary_key COMPONENTS key.")
        art.content.append("")
        art.content.append("    CONSTANTS:")
        art.content.append("      BEGIN OF c_tabname,")
        art.content.append("        def TYPE tabname VALUE '" + self._pattern.properties["master_table"].upper() + "',")
        art.content.append("      END OF c_tabname.")
        art.content.append("")
        art.content.append("    CLASS-DATA gt_multiton TYPE tt_multiton.")
        art.content.append("")
        art.content.append("    METHODS:")
        art.content.append("      constructor")
        art.content.append("        IMPORTING !is_key TYPE t_key")
        art.content.append("        RAISING   cx_no_entry_in_table.")
        art.content.append("")
        art.content.append("ENDCLASS.")
        art.content.append("")

        ##############################
        # Class implementation
        ##############################

        art.content.append("CLASS " + art.name + " IMPLEMENTATION.")
        art.content.append("")
        art.content.append("  METHOD constructor.")
        art.content.append("")
        art.content.append("    SELECT SINGLE *")
        art.content.append("      FROM " + self._pattern.properties["master_table"].lower())
        art.content.append("      WHERE")

        pos = 0
        for key in self._pattern.properties["keys"]:
            line = "        " + key["name"].lower() + " EQ @is_key-" + key["name"].lower()
            pos += 1
            if pos < len(self._pattern.properties["keys"]):
                line += " AND"
            art.content.append(line)

        art.content.append("      INTO CORRESPONDING FIELDS OF @gs_def.")
        art.content.append("")
        art.content.append("    IF sy-subrc NE 0.")
        art.content.append("      RAISE EXCEPTION TYPE cx_no_entry_in_table")
        art.content.append("        EXPORTING")
        art.content.append("          table_name = c_tabname-def")
        entry_name = ""
        for key in self._pattern.properties["keys"]:
            if entry_name != "":
                entry_name += " "
            entry_name += "{ iv_" + key["name"].lower() + " }"
        art.content.append("          entry_name = |" + entry_name + "|.")
        art.content.append("    ENDIF.")
        art.content.append("")
        art.content.append("  ENDMETHOD.")
        art.content.append("")
        art.content.append("  METHOD get_instance.")
        art.content.append("")
        art.content.append("    ASSIGN gt_multiton[ ")
        art.content.append("        KEY primary_key COMPONENTS key = is_key")
        art.content.append("      ] TO FIELD-SYMBOL(<ls_multiton>).")
        art.content.append("")
        art.content.append("    IF sy-subrc NE 0.")
        art.content.append("      DATA(ls_multiton) = VALUE t_multiton( key = is_key ).")
        art.content.append("")
        art.content.append("      TRY.")
        art.content.append("          ls_multiton-obj = NEW #( ls_multiton-key ).")
        art.content.append("        CATCH cx_no_entry_in_table INTO ls_multiton-cx ##NO_HANDLER.")
        art.content.append("      ENDTRY.")
        art.content.append("")
        art.content.append("      INSERT ls_multiton INTO TABLE gt_multiton ASSIGNING <ls_multiton>.")
        art.content.append("    ENDIF.")
        art.content.append("")
        art.content.append("    IF <ls_multiton>-cx IS NOT INITIAL.")
        art.content.append("      RAISE EXCEPTION <ls_multiton>-cx.")
        art.content.append("    ENDIF.")
        art.content.append("")
        art.content.append("    ro_obj = <ls_multiton>-obj.")
        art.content.append("")
        art.content.append("  ENDMETHOD.")
        art.content.append("")
        art.content.append("ENDCLASS.")

        ##############################
        # Closure
        ##############################

        return [art]

