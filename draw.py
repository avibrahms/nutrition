from utils import read_nutrients, read_personal_info
from chart import chart
from spider import spider
from graph import graph


info = read_personal_info('/Users/avi/Documents/personal code/nutrients/info.txt')
data = read_nutrients('/Users/avi/Documents/personal code/nutrients/nutrients.csv')
graph(info, data)
chart(info, data)
spider(info, data)