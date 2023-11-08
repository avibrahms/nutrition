from utils import read_nutrients, read_personal_info
# from chart import chart
# from spider import spider
from graph import graph
import os
from constants import *

data = read_nutrients(data_file_path)
info = read_personal_info(info_file_path)
# chart(info, data)
# spider(info, data)
graph(info, data)