from flask import Flask, request, Response
from flask_restful import Resource, Api
from collections import defaultdict
from heapq import *
from json import dumps
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def processRequest():
   if request.method == 'GET':    
        return Response("", status=200)
   elif request.method == 'POST':
       try:
           content = request.get_json()
           validateInputJson(content)
           out = dijkstra(content['corridors'], content['start'], content['end'])
           outJson = processDijkstraOutput(out)
           return Response(outJson, status=200, mimetype='application/json')
       except Exception as e:
           return Response(createErrorJson(str(e)), status=200, mimetype='application/json')
   elif request.method == 'HEAD':
       return

def createErrorJson(msg):
    return json.dumps(ErrorResult(None, None, msg), default=default) 

def validateInputJson(inJson):
    if inJson.get('corridors') == None :
        raise ValueError('Json does not contain proper keys.')
    if inJson.get('start') == None :
        raise ValueError('Json does not contain proper keys.')
    if inJson.get('end') == None :
        raise ValueError('Json does not contain proper keys.')
    if inJson.get('rooms') == None :
        raise ValueError('Json does not contain proper keys.')
    if(len(inJson.get('rooms')) != len(set(inJson.get('rooms')))):
        raise ValueError('More than one occurence of a room in room list.')
    if inJson['start'] not in inJson['rooms'] :
        raise ValueError('Start room not in rooms.')
    if inJson['end'] not in inJson['rooms'] :
        raise ValueError('Start room not in rooms.')
    for tuple in inJson['corridors']:
        if(tuple[0] == tuple[1]):
            raise ValueError('Invalid circular corridor.')
        for room in tuple:
            if room not in inJson['rooms'] :
                raise ValueError('Invalid room in corridors.')
    return

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r in edges:
        g[l].append((1,r))
        g[r].append((1,l))

    q, seen = [(0,f,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))
    raise ValueError('No solution found')

def default(o):
    return o._asdict()

def processDijkstraOutput(dOut):
    dOut = dOut[1]
    solution = []
    length = 0
    while dOut:
        length += 1
        solution.append(dOut[0])
        dOut = dOut[1]
    solution = list(reversed(solution))
    res = Result(solution, length, 'OK')
    return json.dumps(res, default=default)

class Result:
    def __init__(self, solution, length, status):
        self.solution = solution
        self.status = status
        self.length = length

    def _asdict(self):
        return self.__dict__

class ErrorResult:
    def __init__(self, solution, length, error):
        self.solution = solution
        self.error = error
        self.length = length

    def _asdict(self):
        return self.__dict__

if __name__ == '__main__':
     app.run(port=5000)