#!/usr/bin/env python
import plotly as py
import plotly.graph_objs as go

def accuracy(algo_accuracy):
	data = []
	rgb_codes = ['rgb(49,130,189)','rgb(51,0,0)','rgb(107, 107, 107)']
	for (algo,rgb_code) in zip(algo_accuracy,rgb_codes):
		trace = go.Bar(
				x =algo_accuracy[algo].keys(),
				y = algo_accuracy[algo].values(),
				name=algo,
				#text = algo_accuracy[algo].values(),
				marker=dict(
					color=rgb_code
					)
				)
		data.append(trace)
	layout = go.Layout(
			title = 'Accuracy of algorithms trained on different fractions of data',
			titlefont=dict(
				size=25,
				color='#7f7f7f'
				),
			bargap=0.15,
			bargroupgap=0.1,
			barmode='group',
			xaxis=dict(
				title = 'Training data fraction',
				titlefont=dict(
					size=18,
					color='#7f7f7f'
					)
				),
			yaxis=dict(
				title= 'Accuracy',
				titlefont=dict(
					size=18,
					color='#7f7f7f'
					)
				)
			)
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.offline.plot(fig, filename='accuracy')

def ms_cost(algo_ms_cost):
	data = []
	for algo in algo_ms_cost:
		trace = go.Scatter(
				x = algo_ms_cost[algo].keys(),
				y = algo_ms_cost[algo].values(),
				name=algo
				)
		data.append(trace)
	layout = go.Layout(
			title='Misclassification cost for different training samples using different algorithms',
			titlefont=dict(
				size=25,
				color='#7f7f7f'
				),
			xaxis=dict(
				title = 'Training data fraction',
				titlefont=dict(
					size=18,
					color='#7f7f7f'
					)
				),
			yaxis=dict(
				title = 'Missclassification cost',
				titlefont=dict(
					size=18,
					color='#7f7f7f'
					)
				)
			)
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.offline.plot(fig, filename='ms_cost')

def cc_benefit(algo_cc_benefit):
	data = []
	for algo in algo_cc_benefit:
		trace = go.Scatter(
				x = algo_cc_benefit[algo].keys(),
				y = algo_cc_benefit[algo].values(),
				name=algo
				)
		data.append(trace)
	layout = go.Layout(
			title='Correct classification benefit for different training samples using different algorithms',
			titlefont=dict(
				size=25,
				color='#7f7f7f'
				),
			xaxis=dict(
				title = 'Training data fraction',
				titlefont=dict(
					size=18,
					color='#7f7f7f'
					)
				),
			yaxis=dict(
				title = 'Correct classification cost',
				titlefont=dict(
					size=18,
					color='#7f7f7f'
					)
				)
			)
	fig = go.Figure(data=data, layout=layout)
	plot_url = py.offline.plot(fig, filename='cc_benefit')
