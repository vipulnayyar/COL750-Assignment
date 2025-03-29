from z3 import *
import argparse



def solve_incrementally(array):

    pass

def solve_one_shot(array):

    GraphNode = Datatype('GraphNode')
    GraphNode.declare('data', ('row', IntSort()), ('col', IntSort()), ('rightnext', GraphNode), ('bottomnext', GraphNode))
    GraphNode.declare('nil')
    GraphNode = GraphNode.create()

    row_index = GraphNode.row
    col_index = GraphNode.col
    next_right = GraphNode.rightnext
    next_bottom = GraphNode.bottomnext



    graph_nodes = [ [ Const(f'graph_node_{i}_{j}', GraphNode) for j in range(len(array)) ] for i in range(len(array)) ]


    ms = Solver()

    for i in range(len(array)):
        for j in range(len(array)):
            
            if array[i][j] == 'X':
                
                ms.add(graph_nodes[i][j] == GraphNode.nil)
                #print(i,j,GraphNode.nil)

            else:

                if j == len(array) - 1 or array[i][j+1] == 'X':
                    right_neighbor = GraphNode.nil
                else:
                    right_neighbor = graph_nodes[i][j+1]

                if i == len(array) - 1 or array[i+1][j] == 'X':
                    bottom_neighbor = GraphNode.nil
                else:
                    bottom_neighbor = graph_nodes[i+1][j]    

                #print(i,j,right_neighbor, bottom_neighbor)
                ms.add(graph_nodes[i][j] == GraphNode.data(i,j,right_neighbor, bottom_neighbor))                           


    graph_path = [ Const(f'graph_path_{i}', GraphNode) for i in range(2*len(array) -1) ]

    ms.add(graph_path[0] == graph_nodes[0][0])
    ms.add(graph_path[-1] == graph_nodes[-1][-1])
       

    for i in range(len(graph_path) - 1):
        ms.add(Or(graph_path[i+1] == next_right(graph_path[i]),
                  graph_path[i+1] == next_bottom(graph_path[i])
                  ))
        
    for i in range(len(graph_path)):
        ms.add(graph_path[i] != GraphNode.nil)



    result = ms.check()

    if result == sat:
        m = ms.model()
        print("*** SAT ***")

        for i in range(len(graph_nodes)):
            for j in range(len(graph_nodes)):
                #print(m.eval(graph_nodes[i][j]))
                pass

        print("Points in path obtained are as below : ")
        print("Row-Column Index ")
        result_path = []
        for i in range(len(graph_path)):
            #print(i,m.eval(graph_path[i]))
            result_path.append(((m.eval(row_index(graph_path[i]))), m.eval(col_index(graph_path[i]))))
            print(m.eval(row_index(graph_path[i])), m.eval(col_index(graph_path[i])) )
            
        #print(result_path)    
        print("\nOutput Path(marked by *)\n")
        for i in range(len(array)):
            for j in range(len(array)):
                if (i,j) in result_path:
                    print("*", end='')
                else:
                    print(array[i][j], end='')
                print("  ", end = '')
            print("")

        print("\n")


    else:
        print("*** UNSAT ***")


def get_input():

    array = []
        
    while True:
        try:
            line = input()
            #print(line)
        except:
            break

        if '.' in line or 'X' in line or 'G' in line or 'S' in line:
            array.append(list(line))
        else:
            break

    print("\nInput Array : \n")
    for i in range(len(array)):
        for j in range(len(array)):
            print(array[i][j], end='')
            print("  ", end = '')
        print("")

    print("\n\n")
    return array

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--incremental", action="store_true",
                    help="run incrementally")
    args = parser.parse_args()

    input_array = get_input()

    if args.incremental:
        solve_incrementally(array=input_array)
    else:
        solve_one_shot(array=input_array)





if __name__ == '__main__':
    main()