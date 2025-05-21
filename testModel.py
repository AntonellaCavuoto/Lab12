from model.model import Model

myModel = Model()

(myModel.buildGraph("France", 2015))
print(myModel.getPath(5))
