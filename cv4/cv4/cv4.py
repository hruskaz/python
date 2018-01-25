import json
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
from bokeh.models.glyphs import Wedge
from bokeh.plotting import figure, show
from numpy import pi
import numpy
from bokeh.io import curdoc, show

parties=[]
json = json.loads(open('election.json', encoding='utf-8').read())
lowParties = {'name': 'Other',
		 'share': 0,
		 'number': 0,
		 'votes': 0,
		 'color': '#d1f442',
		 'short': 'Other'}
parties.append(lowParties)
for item in json:
    party = {}
    if item['share'] < 1:
        parties[0]['share']+=item['share']
        parties[0]['votes']+=item['votes']
    else:
        party['name']=item['name']
        party['share']=item['share']
        party['number']=item['number']
        party['votes']=item['votes']
        if 'color' in item.keys():
            party['color']=item['color']
        else:
            party['color']="#b3de69"
        if 'short' in item.keys():
            party['short']=item['short']
        else:
            party['short']=item['name']
        parties.append(party)
        party=dict()

datasource = ColumnDataSource(dict(
	names = [party['name'] for party in parties],
	shares=[party['share'] for party in parties],
	numbers=[party['number'] for party in parties],
	votes=[party['votes'] for party in parties],
	colors=[party['color'] for party in parties],
	shorts=[party['short'] for party in parties],
	length=range(len(parties)),
	width=[0.7 for x in range(len(parties)) ]
	))

begins = []
ends=[]
wbr=[float("{0:.2f}".format((party['share']*3.6)*pi/180)) for party in parties]
cursor=0
for i in range(0,len(wbr)):
	begins.append(cursor+wbr[i])
	cursor+=wbr[i]
for item in begins:
	if begins.index(item)==0:
		continue;
	else:
		ends.append(item)
ends.append(begins[0])
wgs=ColumnDataSource(data={
	'starts': begins,
	'ends': ends,
	'color': [party['color'] for party in parties],
	'label': [party['short'] for party in parties]
	})

chart = figure()
chart.vbar( x = 'length', top = 'votes', width = 'width', fill_color='colors', legend='shorts', source=datasource)
show(chart)
chart = figure()
chart.wedge(x=0,y=0,radius=1,start_angle='starts',end_angle='ends',color='color',legend='label',source=wgs)
show(chart)

