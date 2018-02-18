#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import json
import sys

if(len(sys.argv) != 2 or int(sys.argv[1]) not in range(1960,2017)):
	print("Usage: ")
	print("$crunch year")
	sys.exit()

data = {}

ignore = ["WLD", "TEA", "LMY", "IBT", "SAS", "LTE", "EAS", "IDA", "UMC", "IBD", "EAR", "EAP", "LMC", "MIC", "TSA"]

def plot(year):
	key	= []
	gdp	= []
	le	= []
	pop	= []
	color	= []
	for country in data[year].keys():

		if country in ignore:
			continue

		key.append(country)
		gdp.append(data[year][country]['gdp'])
		le.append(data[year][country]['le'])
		p = data[year][country]['pop']/1000000
		
		pop.append(p)
		color.append(data[year][country]['color'])

	plt.scatter(gdp, le, s=pop, alpha=0.8, color=color)
	plt.xscale('log')
	plt.ylim(40,90)
	plt.show()

def loadData(context, fileName):
	global data

	jsonData = open(fileName, 'r')
	jsonData = json.load(jsonData)

	for record in jsonData['Root']['data']['record']:
		key = record['field'][0]['-key']
		name = record['field'][0]['#text']
		if name == 'India':
			color = 'red'
		elif name == 'China':
			color = 'green'
		else:
			color = 'blue'
		year = record['field'][2]['#text']
	
		try:
			val = float(record['field'][3]['#text'])
		except KeyError:
			val = -1

		if year not in data:
			data[str(year)] = {}
		if key not in data[str(year)]:
			data[str(year)][str(key)] = {}

		data[str(year)][str(key)]['name'] = name
		data[str(year)][str(key)][context] = val
		data[str(year)][str(key)]['color'] = color
	

loadData('pop', 'pop.json') #load population data
loadData('gdp', 'gdp.json') #load gdp data
loadData('le', 'le.json')   #load life expectancy data


plot(sys.argv[1])

