from pysat.solvers import Solver
from pysat.card import ITotalizer
from pysat.card import CardEnc , EncType
import argparse



class MySolver:

    def __init__(self, array):
        self.s = Solver(name='glucose3')
        self.size = len(array)
        self.array = array

    def add_clause(self, clause):
        #print("Adding Clause")
        #print(clause)

        self.s.add_clause(clause)

    def get_address(self, i,j):
        return 1 + (i * self.size) + j

    def get_index(self, addr):

        addr = addr - 1

        j = addr % self.size
        i = addr / self.size

        return int(i),int(j)


    
    def get_all_empty_slots(self):

        result = []
        for i in range(len(self.array)):
            for j in range(len(self.array)):
                if self.array[i][j] != 'X':
                    result.append(self.get_address(i,j))
        return result

    def solve(self, assumptions = None):

        # Solving
        if assumptions is not None:
            result = self.s.solve(assumptions = assumptions)
        else:
            result = self.s.solve()

        if result:
            print("*** SAT ***")
            model = self.s.get_model()

            node_list = []
            print("Points in path obtained are as below : ")
            print("Row-Column Index  | Encoded Address")
            for var in model:
                if var > 0 and var <= (self.size * self.size) :
                    print( str(self.get_index(var)) + "                   " + str(var) )
                    node_list.append(self.get_index(var))

            print("\nOutput Path(marked by *)\n")
            for i in range(len(self.array)):
                for j in range(len(self.array)):
                    if (i,j) in node_list:
                        print("*", end='')
                    else:
                        print(self.array[i][j], end='')
                    print("  ", end = '')
                print("")
            print("\n")
        else:
            print("*** UNSAT ***")
            #print(self.s.get_core())

def solve_one_shot(array = None, solve=True):
    if array is None:
        print("Error : Array is None")
        return
    
    ms = MySolver(array=array)


    # Adding Start and Goal field
    ms.add_clause([ms.get_address(0,0)])
    ms.add_clause([ms.get_address(ms.size - 1, ms.size - 1)])

    # Adding next node constraints
    for i in range(len(array)):

        #row_elements = []
        for j in range(len(array[i])):

            #row_elements.append(ms.get_address(i,j))
            if (i == ms.size - 1 and j == ms.size - 1):
                continue

            if array[i][j] == 'X':
                ms.add_clause([-1 * ms.get_address(i,j)])
           
            
            # Add next node constraints
            if(i == ms.size - 1):

                ms.add_clause([-1 * ms.get_address(i,j),  ms.get_address(i,j+1)])
            
            elif(j == ms.size - 1):                
            
                ms.add_clause([-1 * ms.get_address(i,j), ms.get_address(i+1,j)])
            
            else:

                ms.add_clause([-1 * ms.get_address(i,j), ms.get_address(i+1,j),  ms.get_address(i,j+1) ])
    
     # Adding diagonal part 1 constraints
    for j in range(1, len(array)):
        i = 0
        
        # Min one constraint
        min_one_list = []
        while True:

            if j < 0 or i >= ms.size:
                break 
            min_one_list.append(ms.get_address(i,j))
            i += 1
            j -= 1
        
        if len(min_one_list) >= 1:
            ms.add_clause(min_one_list)


        # Atmost one constraint
        for i in range(len(min_one_list)):
            for j in range(i+1, len(min_one_list)):
                ms.add_clause([-1 * min_one_list[i], -1 * min_one_list[j]])


    # Adding diagonal part 2 constraints
    for i in range(1, len(array)-1):
        
        j = len(array) - 1

        # Min one constraint
        min_one_list = []
        while True:

            if j < 0 or i >= ms.size:
                break 

            min_one_list.append(ms.get_address(i,j))
            i += 1
            j -= 1
        
        if len(min_one_list) >= 1:
            ms.add_clause(min_one_list)

        #Atmost one constraint
        for i in range(len(min_one_list)):
            for j in range(i+1, len(min_one_list)):
                ms.add_clause([-1 * min_one_list[i], -1 * min_one_list[j]])
        

    if solve is False:
        return ms
    
    ms.solve()

    


def solve_incrementally(array=None):
    
    ms = solve_one_shot(array=array, solve=False)
    #print("Number of lits = " + str(len(ms.get_all_empty_slots())))
    
    t = ITotalizer(lits=ms.get_all_empty_slots(), ubound=1, top_id = (ms.size*ms.size))

    for clause in t.cnf.clauses:
            ms.add_clause(clause)

   
    for bound in range(2, (2*ms.size) + 2):
        print("\n--- Running with at most number of steps = " + str(bound-1) + " ---")
        
        t.increase(ubound=bound)        
        
        for clause in t.cnf.clauses[-t.nof_new:]:
            ms.add_clause(clause)

        ms.solve(assumptions=[-1 * t.rhs[bound]])






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
