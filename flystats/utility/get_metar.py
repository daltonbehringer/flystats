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

        self._flight_cat()

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

        self.wdir = pd.to_numeric(self.wdir, errors = 'coerce')
        self.wspd = pd.to_numeric(self.wspd, errors = 'coerce')
        self.vsby = pd.to_numeric(self.vsby, errors = 'coerce')
        self.wgst = pd.to_numeric(self.wgst, errors = 'coerce')

        # self.skc1 = pd.to_numeric(self.skc1, errors = 'coerce')
        # self.skc2 = pd.to_numeric(self.skc2, errors = 'coerce')
        # self.skc3 = pd.to_numeric(self.skc3, errors = 'coerce')

        self.skl1 = pd.to_numeric(self.skl1, errors = 'coerce')
        self.skl2 = pd.to_numeric(self.skl2, errors = 'coerce')
        self.skl3 = pd.to_numeric(self.skl3, errors = 'coerce') 

    def _flight_cat(self):

        self.ceiling_hgt = np.zeros((len(self.skc1)))

        for i in range(len(self.date)):
            if self.skc1[i] == 'BKN' or self.skc1[i] == 'OVC' or self.skc1[i] == 'VV':
                self.ceiling_hgt[i] = self.skl1[i]
            elif self.skc2[i] == 'BKN' or self.skc2[i] == 'OVC' or self.skc1[i] == 'VV':
                self.ceiling_hgt[i] = self.skl2[i]
            elif self.skc3[i] == 'BKN' or self.skc3[i] == 'OVC' or self.skc1[i] == 'VV':
                self.ceiling_hgt[i] = self.skl3[i]

        self.ceiling_hgt[self.ceiling_hgt == 0.] = np.nan

        self.flight_cat = ['VFR']*len(self.date)

        for i in range(len(self.date)):
            if self.vsby[i] < 1. or self.ceiling_hgt[i] < 500.:
                self.flight_cat.append('LIFR')
            elif self.vsby[i] < 3. or self.ceiling_hgt[i] < 1000.:
                self.flight_cat.append('IFR')
            elif self.vsby[i] <= 5. or self.ceiling_hgt[i] <= 3000.:
                self.flight_cat.append('MVFR')
            else:
                self.flight_cat.append('VFR')

        # return flight_cat


def var_to_dict(standard_name, data, units, long_name):

    d = {}
    d["data"] = data[:]
    d["units"] = units
    d["long_name"] = long_name
    d["standard_name"] = standard_name
    return d

