'''
A Sinbad plug-in for JSON-based data sources
'''


import json
from sinbad.plugin_base import *
from sinbad.util import collapse_dicts, normalize_keys

class JSON_Infer(Base_Infer):
    
    def matched_by(self, path):
        path = path.lower()
        if path.endswith("json"): return True
        for ptrn in [".json", "=json", ".geojson", "=geojson", "/json", "/geojson"]:   # , ".json.gz", ".json.zip"]:
            if ptrn in path: return True
        return False


class JSON_Data_Factory(Base_Data_Factory):
    
    def load_data(self, fp):
        return normalize_keys(collapse_dicts(json.loads(fp.read().decode(),
                                                        parse_int = str,
                                                        parse_float = str)))

