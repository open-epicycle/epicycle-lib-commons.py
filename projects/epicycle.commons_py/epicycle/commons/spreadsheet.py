def read_spread_sheet(file_name, config):
    input = file(file_name, "rb").read().decode('utf-8')    
    data = [x.split("\t") for x in input.split("\n") if x]

    return SpreadSheet(data, config)
    
def write_spread_sheet(file_name, spread_sheet):
    cells = spread_sheet.get_row_data()

#    for x in cells:
#        for y in x:
#            print repr(y)
#            unicode(y)
    
    #data_lines = [[unicode(y if y is not None else u"!!!!NONE!!!!").strip().replace('"', '""') for y in x] for x in cells]
    data_lines = [u"\t".join([(unicode(y) if y is not None else u"!!!!NONE!!!!").strip().replace('"', '""') for y in x]) for x in cells]
    
    data = u"\n".join(data_lines)
    bin_data = data.encode("utf-8")
    f = open(file_name, "wb")
    f.write(bin_data)
    f.close()

class SpreadSheet(object):
    def __init__(self, data, config):
        self._rows = [SpreadSheetRow(config, x) for x in data]
        self._config = config
    
    def get_row_data(self):
        return [x.get_row_data() for x in self._rows]
    
    def rows(self):
        return self._rows
    
    def append(self, row):
        self._rows.append(row)
    
    def __len__(self):
        return len(self._rows)
    
    def __getitem__(self, key):
        return self._rows[key]

def _find_index(config, name):
    return self._config.index(name)

class SpreadSheetRow(object):
    def __init__(self, config, data=None):
        if data:
            self.__dict__["_data"] = data
        else:
            self.__dict__["_data"] = [""] * len(config)
        self.__dict__["_config"] = config

    def get_row_data(self):
        return self._data
    
    def _find_index(self, name):
        return self._config.index(name)    
    
    def set(self, name, value):
        self._data[self._find_index(name)] = value
        
    def get(self, name):
        return self._data[self._find_index(name)]
        
    def __setattr__(self, name, value):
        self.set(name, value)
        
    def __getattr__(self, name):
        return self.get(name)

