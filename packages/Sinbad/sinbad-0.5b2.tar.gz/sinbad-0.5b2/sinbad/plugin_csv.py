'''
A Sinbad plug-in for CSV-based data sources (supports TSV also)
'''

import csv
import io

from sinbad.plugin_base import *


class CSV_Infer(Base_Infer):
    
    def __init__(self, delim = None):
        super().__init__()
        if delim: self.options['delimiter'] = delim
    
    def matched_by(self, path):
        path = path.lower()
        if path.endswith("csv"): return True
        for ptrn in [".csv", "=csv", "/csv"]:
            if ptrn in path: return True
        
        is_tsv = False
        if path.endswith("tsv"): is_tsv = True
        for ptrn in [".tsv", "=csv"]:
            if ptrn in path: is_tsv = True
        if is_tsv:
            self.options['delimiter'] = '\t'
            return True
        
        return False



class CSV_Data_Factory(Base_Data_Factory):
    
    def __init__(self):
        super().__init__()
        self.field_names = None
        self.delimiter = None
        self.skip_rows = 0
    
    
    def load_data(self, fp, encoding = None):
        if encoding: str_data = fp.read().decode(encoding)
        else: str_data = fp.read().decode()
        
        if str_data.startswith('\ufeff'):  # BOM, if already decoded as utf8
            str_data = str_data.lstrip('\ufeff')
        str_data = str_data.replace('\r', '\n')
        
        sample = str_data[:10000]
        snuffy = csv.Sniffer()
        if not snuffy.has_header(sample) and not self.field_names:
            # see how many columns there are and provide auto-numbered names
            if self.delimiter: rdr = csv.reader(io.StringIO(str_data), delimiter=self.delimiter)
            else: rdr = csv.reader(io.StringIO(str_data))
            self.field_names = [ self.__fix_heading(i, '') for i in range(len(rdr.__next__())) ]
            
        if not self.delimiter: self.delimiter = snuffy.sniff(sample).delimiter
    
        sfp = io.StringIO(str_data)
        if self.delimiter:
            data = csv.DictReader(sfp, fieldnames = self.field_names, delimiter = self.delimiter, restkey='_extra_', restval='')

        if data.fieldnames:
            data.fieldnames = [ self.__fix_heading(i, n) for i, n in enumerate(data.fieldnames)]
        
        self.field_names = data.fieldnames
            
        stuff = [x for x in data]
        if isinstance(stuff, list) and len(stuff) == 1:
            return stuff[0]
        else:
            return stuff[self.skip_rows:]
        
        
    def get_options(self):
        return [ "header", "delimiter", "skiprows" ]
# TODO: skiprows, quote options
    
    
    def get_option(self, name):
        if name == "header" and self.field_names:
            return ",".join(self.field_names)
        elif name == "delimiter" and self.delimiter:
            return self.delimiter
        elif name == "skip_rows":
            return self.skip_rows
        else:
            return None


    def set_option(self, name, value):
        if name == "header":   # value could be a list or a string of comma-separated column names
            if isinstance(value, str):
                values = value.split(",")
            self.field_names = [v.strip().strip("\"'").strip() for v in values]
        elif name == "delimiter":
            self.delimiter = value
        elif name == "skiprows":
            self.skip_rows = int(value)
    
    
    def __fix_heading(self, i, s):
        '''Strip trailing whitespace, and then provide names for any unnamed columns'''
        s = s.strip()
        if s == '':
            s = '_col_{}'.format(i)
        if s[0].isdigit():      # normalize to identifier naming rules because jsonpath_rw is picky
            s = '_' + s
        return s
        
