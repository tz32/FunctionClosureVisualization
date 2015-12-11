import graphviz as gv;
import functools;
import inspect;


##### Closure Examples #####
# Closure example 1
def add_k(k):

    def plut():
        return 'mars'
    def outer(j):

        def hello(world):
            return 'world'
        def sum(n):
            print(l)
            hello(23)
            plut()
            return k + n
        return sum
    return outer(4)


# This is taken from the getclosurevars function from the inspect module
# This was done just for simplification, reducing the amount of overhead
# from imports, and the globals, builtins, and unbound variables also returned
# from the getclosurevars function were not necessary
def get_nonlocal_vars(func):

    if (inspect.isfunction(func)):

        code = func.__code__
    
        # Nonlocal references are named in co_freevars and resolved
        # by looking them up in __closure__ by positional index

        variablelist = ''
        for var in func.__code__.co_varnames:
            if variablelist == '':
                variablelist = variablelist + var
            else:
                variablelist = variablelist + '\l' + var
        if localvariables != '':
            localvariables.append((func.__name__, variablelist))


        if func.__closure__ is None:
            nonlocal_vars = {}
        else:
            nonlocal_vars = {
                var : cell.cell_contents
                for var, cell in zip(code.co_freevars, func.__closure__)
           }

        for key, value in nonlocal_vars.items():
            if value not in foundfunctions:
                if inspect.isfunction(value):
                    
                    foundfunctions.append(value)
                    get_nonlocal_vars(value)

        return nonlocal_vars

# Converts the function type to a string description containing the scopes of the
# function. Then, using substrings and string matching, the function pulls out
# the scope ordering and places it into head and tail arrays. 
def get_edges(key, value):

    tempValue = str(value)
    if "function" in tempValue and key not in nameList:
        end = tempValue.find('.')
        tail = tempValue[10: end]
        if tempValue[10: end] not in nameList:
            nameList.append(tempValue[10: end])

        start = 0;
        cont = True

        while (cont):
            start = start + 1
            end = tempValue[start:].find('.') + start
            start = end
            end = tempValue[start+1:].find('.') + start
            if tempValue[start+1: end+1] not in nameList and tempValue[start+1: end+1] != '' and tempValue[start+1: end+1] != '<locals>':
                nameList.append(tempValue[start+1: end+1])
                tails.append(tail)
                heads.append(tempValue[start+1: end+1])
                tail = tempValue[start+1: end+1]

            if (end < start):
                cont = False

        end = tempValue[start+1:].find(' ') + start
        if tempValue[start+1: end+1] not in nameList and tempValue[start+1: end+1] != '' and tempValue[start+1: end+1] != '<locals>':
            nameList.append(tempValue[start+1: end+1])
            nameList.append(tempValue[start+1: end+1])
            tails.append(tail)
            heads.append(tempValue[start+1: end+1])
            tail = tempValue[start+1: end+1]

    else:
        #Deal with nonfunction variables
        pass

foundfunctions = []
localvariables = []

currentfunc = add_k
nonlocals = get_nonlocal_vars(add_k)

currentfunc = add_k(3)
nonlocals = get_nonlocal_vars(add_k(3))

nameList = []
heads = []
tails = []

for key, value in nonlocals.items():
    get_edges(key, value)

##### Graphviz Code
graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')



def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph


# Build the lists for vertices and edges
vertices = []
edges = []

variablescope = []

for function, variable in localvariables:
    variablescope.append(function)

print(variablescope)

for name in nameList:
    
    if (name in variablescope):

        for function, variable in localvariables:
            if (function == name):
            #print("1", name)
                vertices.append((name, {'label': '&lambda; ' + name + '\l\l ' + variable}))

    else: #elif (function not in variablescope):
        print("2", name)
        vertices.append((name, {'label': '&lambda; ' + name + '\l\l'}))
i = 0
for head in heads:
    edges.append((head, tails[i]))
    i = i + 1

# Build the graph from the edges and nodes
g6 = add_edges(add_nodes(digraph(), vertices), edges)


# Apply styles to the graph. This allows for the class diagram appearance
styles = {
    'graph': {
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Arial',
        'shape': 'record',
        'fontcolor': 'blue',
        'fontsize': '14',
    },
    'edges': {
        'style': 'solid',
        'color': 'black',
        'arrowhead': 'odot',
        'fontsize': '26',
    }
}

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) #or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) #or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) #or {}
    )
    return graph


##### Generate the image of the graph and display it to a browser
g6 = apply_styles(g6, styles)
g6.render('img/g6', view = 'true')
