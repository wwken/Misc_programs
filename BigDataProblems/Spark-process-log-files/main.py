import pandas as pd

def extractLine(x):
    #extract the date without the second first
    startBracketPos = x.index('[')
    endBracketPos = x.index(']')
    dateTimeStr = x[startBracketPos+1:endBracketPos]
    dateTimeStr = dateTimeStr.split(' ')[0]
    dateTimeStrWithoutSecond = dateTimeStr[0:dateTimeStr.rfind(':')]

    # now extract the status code
    nx = x[endBracketPos+1:]
    nx = nx[nx.index('"') + 1:]
    nx = nx[nx.index('"') + 1:].strip()
    statusCode = nx.split(' ')[0].strip()

    return {'status': statusCode, 'time': dateTimeStrWithoutSecond}

data = pd.read_csv('sample.log', sep="\n", header=None)

data = data[0].map(lambda x: extractLine(x))


data = pd.DataFrame(data.values.tolist())
data.columns = ['status', 'time']

g = data.groupby(['status', 'time'])

for entry in g.groups:
    print "Status and time: {}, count: {}".format(entry, len(g.groups[entry]))


