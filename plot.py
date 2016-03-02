import plotly
import plotly.graph_objs as go

tab_x = list()
tab_y = list()
tab_x2 = list()
tab_y2 = list()

best = [-0.0000015230981995981592, 5000.000000176404, 4.999999998293433, -61.99999999999368, 0.9999999999999908, -0.0009999999999999955]
best = [0.0, 5000.0, 5.0, -62.0, 1.0, -0.001]

def compute_value(coefs, x):
    return coefs[0] + coefs[1] * x + coefs[2] * x * x + coefs[3] * x * x * x + coefs[4] * x * x * x * x + coefs[5] * x * x * x * x * x

with open("data.in") as input_file:
    for line in input_file:
        line = line.strip()
        numbers = line.split()
        if len(numbers) == 2:
            tab_x.append(float(numbers[0]))
            tab_y.append(float(numbers[1]))

for index in range(len(tab_x)):
    tab_x2.append(tab_x[index])
    value_y = compute_value(best, tab_x[index])
    tab_y2.append(value_y)
    diff = abs(value_y - tab_y[index])
    if diff > 0.0001:
        print(tab_x[index], value_y, tab_y[index])

plotly.offline.plot([go.Scatter(x=tab_x, y=tab_y), go.Scatter(x=tab_x2, y=tab_y2)], filename='compare-results-tmp.html')
