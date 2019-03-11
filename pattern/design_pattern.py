

PAT_MULTITON = "Multiton"
PAT_NULL = "Null"
ALL_PATTERNS = [PAT_MULTITON]


class DesignPattern:

    def __init__(self, name: str):
        self.name = name
        self.properties = dict()
        self._initialize_properties()

    def _initialize_properties(self):
        if self.name == PAT_MULTITON:
            self.properties = {
                "class_name": "ZCL_CLASS",
                "class_description": "My class",
                "master_table": "ZTABLE",
                "keys": [
                    {
                        "name": "field1",
                        "type": "type1"
                    }
                ]
            }
        elif self.name == PAT_NULL:
            self.properties = {
                "class_name": "ZCL_CLASS",
                "class_description": "My class"
            }
        else:
            raise Exception("Unknown pattern: " + self.name)
