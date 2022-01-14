import csv
from scipy import stats
from numpy import arctanh

class Locations:
    locations = []

    def __init__(self, file_name):
        reader = csv.reader(open(file_name, 'rb'))
        
        # Ignore column names
        next(reader)

        # Proper id numbering with array indices
        self.locations.append({'coor': (None, None)})
        for line in reader:
            tempLoc = {}
            lat, _long = line[1], line[2]
            tempLoc['coor'] = (lat, _long)
            self.locations.append(tempLoc)
        

loc = Locations('longtitude_latitude2.5.csv')

def Z(x, y):
    (r, p) = stats.pearsonr(x, y)
    r_prime = arctanh(r)
    s_r = 1/(sqrt(len(x)-3))
    return (r_prime - p)/s_r
    
def SAOLA(data, label):
    markov_blanket = set()
    
    F = data.predictive_features
    C = label
    feature_set_past = data.S_t_past
    
    for f in F:
        is_valid = True
        if abs(Z(feature, c)) < 1.96:
            continue
        for y in feature_set_past:
            if abs(Z(y, C)) > abs(Z(f,C)) and abs(Z(f, y)) >= 1.96:
                is_valid = false
                break
            if abs(Z(f, C)) > abs(Z(y, C)) and abs(Z(f, y)) >= 1.96:
                feature_set_past.remove(y)
                
        if is_valid:
            markov_blanket = feature_set_past | f
        
    return markov_blanket

import pandas as pd
class Feature_Reader:
    file_ext = '.csv'
    base_dir = './raw_data/'
    
    PW = 'pw' # Preciptable water
    T850 = 't850' # 850hPa Temperature
    U300 = 'u300' # 300 hPa Zonal Wind
    U850 = 'u850' # 850 hPa Zonal Wind
    V300 = 'v300' # 300 hPa Meridional Wind
    V850 = 'v850' # 850 hPa Meridional Wind
    Z1000 = 'z1000' # Z1000 hPa Geopotential Height
    Z300 = 'z300' # Z300 hPa Geopotential Height
    Z500 = 'z500' # Z500 hPa Geopotential Height
    
    def make_file_path(self,feature, year):
        return self.base_dir+feature+'_'+year+self.file_ext
    
    def get(self, feature, year):
        print pd.read_csv(self.make_file_path(feature, str(year)), sep=',').values
        
reader = Feature_Reader()
reader.get(reader.Z500, 2010)

