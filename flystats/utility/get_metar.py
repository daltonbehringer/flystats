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
        
        self.site = data.station
        self.date = pd.to_datetime(data.valid)
        self.wdir = data.drct
        self.wspd = data.sknt
        self.vsby = data.vsby
        self.wgst = data.gust
        self.skc1 = data.skyc1
        self.skc2 = data.skyc2
        self.skc3 = data.skyc3
        self.skl1 = data.skyl1
        self.skl2 = data.skyl2
        self.skl3 = data.skyl3

        self._prep_data()

    def _prep_data(self):
    
        self.fields = {}

        self.fields["site"] = var_to_dict(
            "ICAO", np.ma.array(self.site), " ", "Station Identifier"
        )
        self.fields["date"] = var_to_dict(
            "date", np.ma.array(self.date), " ", "Observation Date (UTC)",
        )
        self.fields["wdir"] = var_to_dict(
            "wdir", np.ma.array(self.wdir), "deg", "Wind Direction",
 		)
        self.fields["wspd"] = var_to_dict(
            "wspd", np.ma.array(self.wspd), "kts", "Wind Speed",
        )
        self.fields["vsby"] = var_to_dict(
            "vsby", np.ma.array(self.vsby), "statute miles", "Visibility",
        )
        self.fields["wgst"] = var_to_dict(
            "wgst", np.ma.array(self.wgst), "kts", "Wind Gust",
        )
        self.fields["skc1"] = var_to_dict(
            "skc1", np.ma.array(self.skc1), " ", "Sky Cover 1",
        )
        self.fields["skc2"] = var_to_dict(
            "skc2", np.ma.array(self.skc2), " ", "Sky Cover 2",
        )
        self.fields["skc3"] = var_to_dict(
            "skc3", np.ma.array(self.skc3), " ", "Sky Cover 3",
        )
        self.fields["skl1"] = var_to_dict(
            "skl1", np.ma.array(self.skl1), "100 feet", "Sky Cover Level 1",
        )
        self.fields["skl2"] = var_to_dict(
            "skl2", np.ma.array(self.skl2), "100 feet", "Sky Cover Level 2",
        )
        self.fields["skl3"] = var_to_dict(
            "skl3", np.ma.array(self.skl3), "100 feet", "Sky Cover Level 3",
        )



def var_to_dict(standard_name, data, units, long_name):

    d = {}
    d["data"] = data[:]
    d["units"] = units
    d["long_name"] = long_name
    d["standard_name"] = standard_name
    return d

