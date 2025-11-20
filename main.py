from graph import GraphMatrix, GraphList
from algorithms import kosaraju_matrix, kosaraju_list

graph_matrix = GraphMatrix()
graph_matrix.generate(200, 0.1)
output, time = kosaraju_matrix(graph_matrix)
print(output)
print(time)

graph_list = graph_matrix.transform_to_list()
output, time = kosaraju_list(graph_list)
print(output)
print(time)