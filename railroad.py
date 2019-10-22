import heapq, random, math, time
from heapq import heappop
from math import pi, acos, sin, cos
from tkinter import *


def calc_edge_cost(y1, x1, y2, x2):
   #
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees

   # if (and only if) the input is strings
   # use the following conversions

   y1 = float(y1)
   x1 = float(x1)
   y2 = float(y2)
   x2 = float(x2)
   #
   R = 3958.76  # miles = 6371 km
   #
   y1 *= pi / 180.0
   x1 *= pi / 180.0
   y2 *= pi / 180.0
   x2 *= pi / 180.0
   #
   # approximate great circle distance with law of cosines
   #
   try:
      return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R
   except:
      return 0
   #


# NodeLocations, NodeToCity, CityToNode, Neighbors, EdgeCost
# Node: (lat, long) or (y, x), node: city, city: node, node: neighbors, (n1, n2): cost
def make_graph(nodes="rrNodes.txt", node_city="rrNodeCity.txt", edges="rrEdges.txt"):
   nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
   map = {}  # have screen coordinate for each node location

   for line in open(nodes, 'r').read().splitlines():
      node, y, x = line.split()
      nodeLoc[node] = (y, x)
   for line in open(node_city, 'r').read().splitlines():
      node, *city = line.split()
      nodeToCity[node] = ' '.join(city)
      cityToNode[' '.join(city)] = node
   for line in open(edges, 'r').read().splitlines():
      node, child = line.split()
      if node not in neighbors:
         neighbors[node] = set()
      if child not in neighbors:
         neighbors[child] = set()
      neighbors[node].add(child)
      neighbors[child].add(node)
      y1, x1 = nodeLoc[node]
      y2, x2 = nodeLoc[child]
      edgeCost[(node, child)] = calc_edge_cost(y1, x1, y2, x2)
      edgeCost[(child, node)] = calc_edge_cost(y2, x2, y1, x1)

   # Un-comment after you fill the nodeLoc dictionary.
   for node in nodeLoc:  # checks each
      lat = float(nodeLoc[node][0])  # gets latitude
      long = float(nodeLoc[node][1])  # gets long
      modlat = (lat - 10) / 60  # scales to 0-1
      modlong = (long + 130) / 70  # scales to 0-1
      map[node] = [modlat * 800, modlong * 1200]  # scales to fit 800 1200
   return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]


# Return the direct distance from node1 to node2
# Use calc_edge_cost function.
def dist_heuristic(n1, n2, graph):
   # Your code goes here
   y1, x1 = graph[0][n1]
   y2, x2 = graph[0][n2]
   return calc_edge_cost(y1, x1, y2, x2)
   # pass


# Create a city path.
# Visit each node in the path. If the node has the city name, add the city name to the path.
# Example: ['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
def display_path(path, graph):
   # Your code goes here
   retPath = []
   for id in path:
      if id in graph:
         retPath.append(graph[id])
      else:
         retPath.append(id)
   return retPath
   # pass


def drawLine(canvas, y1, x1, y2, x2, col):
   x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
   canvas.create_line(x1, 800 - y1, x2, 800 - y2, fill=col)


# Draw the final shortest path.
# Use drawLine function.
def draw_final_path(ROOT, canvas, path, graph, col='red'):
   # Your code goes here
   for i in range(len(path) - 1):
      y1, x1 = graph[5][path[i][0]]
      y2, x2 = graph[5][path[i + 1][0]]
      drawLine(canvas, y1, x1, y2, x2, col)
   # ROOT.update()
   # pass


def draw_all_edges(ROOT, canvas, graph):
   ROOT.geometry("1200x800")  # sets geometry
   canvas.pack(fill=BOTH, expand=1)  # sets fill expand
   for n1, n2 in graph[4]:  # graph[4] keys are edge set
      drawLine(canvas, *graph[5][n1], *graph[5][n2], 'black')  # graph[5] is map dict
   ROOT.update()


def a_star(start, goal, graph):
   # Your code goes here
   ROOT = Tk()
   ROOT.title("aStar")
   canvas = Canvas(ROOT, background='white')
   draw_all_edges(ROOT, canvas, graph)
   startTime = time.time()
   if start == goal:
      return start, 0
   openSet = [(dist_heuristic(start, goal, graph), start, 0, [(start, 0)], start)]
   closedSet = {}
   counter = 1
   while openSet:
      counter+=1
      ROOT.update()
      openSet.sort()
      f, parent, distanceTo, path, location = openSet.pop(0)
      if location in closedSet:
         drawLine(canvas, graph[5][location][0], graph[5][location][1], graph[5][parent][0], graph[5][parent][1],'blue')
         continue
      closedSet[location] = distanceTo
      drawLine(canvas, graph[5][location][0], graph[5][location][1], graph[5][parent][0], graph[5][parent][1], 'blue')
      if location==goal:
         #for est, par, pathlen, nodes, location in openSet:
         #   draw_final_path(ROOT, canvas, nodes, graph, 'green')
         totalDist = distanceTo
         draw_final_path(ROOT, canvas, path, graph)
         ROOT.update()
         return path, totalDist
      for nbr in graph[3][location]:
         parToChild = calc_edge_cost(graph[0][nbr][0], graph[0][nbr][1], graph[0][location][0], graph[0][location][1])
         '''if nbr == goal:
            #for f, distanceTo, path, location in openSet:
            #   draw_final_path(ROOT, canvas, path, graph, 'green')
            # print(parentSet)
            totalDist = distanceTo + calc_edge_cost(graph[0][nbr][0], graph[0][nbr][1], graph[0][location][0],
                                                    graph[0][location][1])
            # find path
            path.append((nbr, parToChild))
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.update()
            return path, totalDist'''
         # dToEnd = calc_edge_cost(graph[0][goal][0], graph[0][goal][1], graph[0][nbr][0], graph[0][nbr][1])
         dToEnd = dist_heuristic(goal, nbr, graph)

         newF = dToEnd + parToChild + distanceTo
         openSet.append((newF, location, distanceTo + parToChild, path + [(nbr, parToChild)], nbr))

         drawLine(canvas, graph[5][location][0], graph[5][location][1], graph[5][nbr][0], graph[5][nbr][1], 'green')
         #ROOT.update()#comment out to draw closedSet at end
   return None

def main():
   # find start, goal
   graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")

   cur_time = time.time()
   start = ''
   end = ''
   args = sys.argv[1:]
   for loc in args:
      if start not in graph[2]:
         if start!='':
            start+=' '
         start+=loc
         continue
      if end not in graph[2]:
         if end!='':
            end+= ' '
         end+=loc
   path, cost = a_star(graph[2][start], graph[2][end], graph)
   if path != None:
      display_path(path, graph)
   else:
      print("No Path Found.")
   for node in path:
      if node[0] in graph[1]:
         print(str(graph[1][node[0]]) + '     ' + str(node[1]) + ' miles')
      else:
         print(str(node[0]) + '     ' + str(node[1]) + ' miles')
   print('Total stations: ' + str(len(path)-1))
   print('Total Distance: ', cost,  ' miles')
   #print('duration: ', (time.time() - cur_time))
   print()
   mainloop()  # Let TK windows stay still


main()

''' Sample output
The number of explored nodes of A star: 7692
The whole path: ['3700421', '3700258', '3700257', '3700142', '3700422', '3700001', '3700235', '3700234', '3700330', '3700329', '3700002', '3700356', '3700355', '3700357', '3700197', '3700198', '0000529', '4500042', '4500270', '4500231', '4500069', '4500023', '4500233', '4500094', '4500095', '4500096', '4500097', '4500234', '4500225', '4500104', '4500082', '4500164', '4500015', '4500181', '4500167', '0000533', '1300133', '1300197', '1300132', '1300146', '1300198', '1300204', '1300208', '1300087', '1300279', '1300088', '1300369', '1300459', '1300458', '1300090', '1300460', '1300107', '1300210', '1300398', '1300099', '0000031', '0100343', '0100342', '0100341', '0100084', '0100340', '0100276', '0100339', '0100338', '0100324', '0100344', '0100508', '0100273', '0100329', '0100272', '0100303', '0100090', '0100430', '0100429', '0100435', '0100240', '0100239', '0100018', '0100138', '0100139', '0100088', '0100289', '0100569', '0100222', '0100224', '0100227', '0100188', '0100256', '0100101', '0100134', '0100038', '0100317', '0100319', '0100157', '0100253', '0100316', '0100198', '0100030', '0100465', '0100472', '0100028', '0100200', '0100293', '0100104', '0000462', '2800033', '2800152', '2800032', '2800150', '2800031', '2800108', '2800247', '2800191', '2800156', '2800169', '2800001', '2800162', '2800163', '2800164', '2800125', '2800030', '2800028', '0000419', '2200078', '2200143', '2200039', '2200274', '2200379', '2200080', '2200273', '2200205', '2200112', '2200037', '2200076', '2200277', '2200074', '2200322', '2200320', '2200035', '2200212', '2200218', '2200248', '2200036', '2200211', '2200209', '2200208', '2200265', '2200073', '2200312', '2200314', '0000143', '4801029', '4801030', '4800307', '4801033', '4801031', '4801171', '4800227', '4800306', '4800901', '4801289', '4800309', '4800416', '4800531', '4801183', '4800786', '4801181', '4800365', '4801180', '4800530', '4801168', '4800785', '4800096', '4800478', '4800097', '4800107', '4800106', '4800100', '4800586', '4800099', '4801026', '4800058', '4800842', '4800843', '4800467', '4800646', '4800056', '4800645', '4800456', '4800048', '4800455', '4801124', '4800778', '4800046', '4800853', '4800852', '4800045', '4801244', '4800681', '4800738', '4800291', '4800362', '4800363', '4800539', '4800295', '4800288', '4800540', '4800634', '4800554', '4801293', '4801292', '4800549', '4801294', '4800292', '4801290', '4800283', '4800702', '4800754', '4800281', '4800755', '4800756', '4800294', '4800550', '4800552', '4800553', '4800624', '4800823', '4801012', '4800536', '4800751', '4801307', '4801295', '4800743', '4800300', '4800746', '4800749', '4800516', '4801299', '0000588', '3500100', '3500044', '3500086', '3500106', '3500137', '3500015', '3500143', '3500041', '3500024', '0000310', '0400107', '0400029', '0400098', '0400105', '0400097', '0400030', '0400031', '0400033', '0400034', '0400036', '0400111', '0400110', '0400118', '0400037', '0400108', '0400120', '0400119', '0400103', '0400026', '0400079', '0400134', '0400072', '0400099', '0400044', '0400045', '0400135', '0400080', '0400048', '0400112', '0400092', '0400053', '0400060', '0000146', '0600798', '0600648', '0600758', '0600796', '0600039', '0600646', '0600797', '0600747', '0600516', '0600750', '0600584', '0600746', '0600585', '0600586', '0600042', '0600770', '0600434', '0600689', '0600464', '0600688', '0600384', '0600588', '0600460', '0600408', '0600799', '0600402', '0600766', '0600686', '0600079', '0600080', '0600085', '0600685', '0600084', '0600751', '0600322', '0600427', '0600316']
The length of the whole path 319
['Charlotte', 'Dallas', 'Tucson', 'Los Angeles']
A star Path Cost: 2419.9700735372285
A star duration: 6.368658781051636 '''


