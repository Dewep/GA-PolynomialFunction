import plotly
import plotly.graph_objs as go

tab_x = list()
tab_y = list()

with open("data.in") as input_file:
    for line in input_file:
        line = line.strip()
        numbers = line.split()
        if len(numbers) == 2:
            tab_x.append(float(numbers[0]))
            tab_y.append(float(numbers[1]))
            #target[float(numbers[0])] = float(numbers[1])

trace = go.Scatter(
    x = tab_x,
    y = tab_y
)

data = [trace]

plotly.offline.plot(data, filename='compare-results')
