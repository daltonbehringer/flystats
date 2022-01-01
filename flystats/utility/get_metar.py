import pandas as pd
import numpy as np

'''
NOTES
'''

def read_metar(filename):

    data = _reader(filename)
    return data

class _reader(object):

    def __init__(self, filename):

        self.filename = filename

        data = pd.read_csv(filename)
        
        # t = pd.Series([val.time() for val in pd.to_datetime(data.Time)])
        self.site = data.station
        self.date = pd.to_datetime(data.valid)
        self.metar = data.metar

        self._prep_data()

    def _prep_data(self):
    
        self.fields = {}

        self.fields["site"] = var_to_dict(
            "ICAO", np.ma.array(self.site), " ", "Station Identifier"
        )
        self.fields["date"] = var_to_dict(
            "date", np.ma.array(self.date), "M/D/Y", "Seeding Aircraft Date",
        )
        self.fields["metar"] = var_to_dict(
            "metar", np.ma.array(self.metar), " ", "Raw METAR (5-min obs)",
 		)

def var_to_dict(standard_name, data, units, long_name):

    d = {}
    d["data"] = data[:]
    d["units"] = units
    d["long_name"] = long_name
    d["standard_name"] = standard_name
    return d