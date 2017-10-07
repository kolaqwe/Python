__author__ = 'Kola'
import pandas as pd
import os
from spyre import server
import matplotlib.pyplot as plt
import json
import pylab
from matplotlib import mlab

import sys

if (sys.version_info > (3, 0)):
     import urllib as urllib2
else:
     import urllib2

print(urllib2)

id_list = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 9, 10, 1, 3, 2, 4, 12]

Param_list = ["VCI", "TCI", "VHI"]

os.chdir('VHI/')
path = os.getcwd()


def download_files(path):
    for id in id_list:
        if id < 10:
            id = '0'+str(id)
        url="http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R"+str(id)+".txt"
        vhi_url = urllib2.urlopen(url)
        out = open('vhi_id_'+str(id)+'.csv', 'wb')
        out.write(vhi_url.read())
        out.close()
        print ("VHI"+str(id)+" is downloaded...")



class PlotData(server.App):
    title = "Geo data analysis"

    inputs = [{"input_type": 'dropdown',
               "label": 'Choose parameter',
               "options": [{"label": "VCI", "value": Param_list[0]},
                           {"label": "TCI", "value": Param_list[1]},
                           {"label": "VHI", "value": Param_list[2]}],
               "variable_name": 'sort',
               "action_id": "plot"},

              {"input_type": 'dropdown',
               "label": 'Choose province',
               "options": [{"label": "Vinnytsya", "value": id_list[0]},
                           {"label": "Volyn", "value": id_list[1]},
                           {"label": "Dnipropetrovs'k", "value": id_list[2]},
                           {"label": "Donets'k", "value": id_list[3]},
                           {"label": "Zhytomyr", "value": id_list[4]},
                           {"label": "Transcarpathia", "value": id_list[5]},
                           {"label": "Zaporizhzhya", "value": id_list[6]},
                           {"label": "Ivano-Frankivs'k", "value": id_list[7]},
                           {"label": "Kiev", "value": id_list[8]},
                           {"label": "Kirovohrad", "value": id_list[9]},
                           {"label": " Luhans'k", "value": id_list[10]},
                           {"label": "L'viv", "value": id_list[11]},
                           {"label": "Mykolayiv", "value": id_list[12]},
                           {"label": "Odessa", "value": id_list[13]},
                           {"label": "Poltava", "value": id_list[14]},
                           {"label": "Rivne", "value": id_list[15]},
                           {"label": "Sumy", "value": id_list[16]},
                           {"label": "Ternopil'", "value": id_list[17]},
                           {"label": "Kharkiv", "value": id_list[18]},
                           {"label": "Kherson", "value": id_list[19]},
                           {"label": "Khmel'nyts'kyy", "value": id_list[20]},
                           {"label": "Cherkasy", "value": id_list[21]},
                           {"label": "Chernivtsi", "value": id_list[22]},
                           {"label": "Chernihiv", "value": id_list[23]},
                           {"label": "Crimea", "value": id_list[24]},
                           {"label": "Kiev City", "value": id_list[25]}],
               "variable_name": 'province',
               "action_id": "update_data"},

              {"input_type": "text",
                "label": "week start analysis",
                "variable_name": 'week_start',
                "value": 1,
                "action_id": "update_data"},

              {"input_type": "text",
                "label": "week end analysis",
                "variable_name": 'week_end',
                "value": 16,
                "action_id": "update_data"},

              {"input_type": "text",
                "label": "year for analysis",
                "variable_name": 'year',
                "value": 1996,
                "action_id": "plot"}]
    tabs = ["Plot", "Table"]

    outputs = [{"output_type": "plot",
                "output_id": "plot",
                "control_id": "update_data",
                "tab": "Plot",
                "on_page_load": True },

               {"output_type": "table",
                 "output_id": "update_data",
                 "control_id": "update_data",
                 "tab": "Table",
                 "on_page_load": True}]

    def getData(self, params):
        province = int(params['province'])
        param = str(params['sort'])
        min_week = int(params['week_start'])
        max_week = int(params['week_end'])
        year = int(params['year'])
        if int(province)< 10:
            province = '0'+str(province)
        for file in os.listdir(path):
            if file.startswith('vhi_id_'+str(province)):
                df = pd.read_csv(file, index_col=False, header=1)
                a = df[df['week']>=min_week]
                b = a[df['week']<=max_week]
                c = b[df['year']==year]
                d = c[df[param]>0]
                return d

    def getPlot(self, params):
        param = str(params['sort'])
        df = self.getData(params)
        x = df[[param]]
        y = df['week']
        plt = x.plot(y)
        fig = plt.get_figure()
        return fig


app = PlotData()
app.launch(port=9094)
