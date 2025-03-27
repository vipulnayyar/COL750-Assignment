from pysat.solvers import Solver



class MySolver:

    def __init__(self):
        self.s = Solver()
        self.size = 0

    def add_clause(self, clause):
        print("Adding Clause")
        print(clause)

        self.s.add_clause(clause)

    def get_address(self, i,j):
        return 1 + (i * self.size) + j

    def get_index(self, addr):

        addr = addr - 1

        j = addr % self.size
        i = addr / self.size

        return int(i),int(j)


    def get_input(self):

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

        print(array)
        self.size = len(array)
        return array



def main():

    ms = MySolver()
    array = ms.get_input()
    size = ms.size


    ms.add_clause([ms.get_address(0,0)])
    ms.add_clause([ms.get_address(size - 1, size - 1)])

    for i in range(len(array)):

        row_elements = []
        for j in range(len(array[i])):

            row_elements.append(ms.get_address(i,j))
            if (i == size - 1 and j == size - 1):
                continue

            if array[i][j] == 'X':
                ms.add_clause([-1 * ms.get_address(i,j)])
           
            
            # Add next node constraints
            if(i == size - 1):

                ms.add_clause([-1 * ms.get_address(i,j),  ms.get_address(i,j+1)])
            
            elif(j == size - 1):                
            
                ms.add_clause([-1 * ms.get_address(i,j), ms.get_address(i+1,j)])
            
            else:
    
                ms.add_clause([-1 * ms.get_address(i,j), ms.get_address(i+1,j),  ms.get_address(i,j+1) ])
   
    for k in range(len(array)):
        i = 0
        j = k

        # Min one constraint
        min_one_list = []
        while True:

            if j < 0 or i >= size:
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


    for k in range(1, len(array)):
        i = k
        j = len(array) - 1

        # Min one constraint
        min_one_list = []
        while True:

            if j < 0 or i >= size:
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
        
               



    result = ms.s.solve()
    if result:
        print("*** SAT ***")
        model = ms.s.get_model()

        for var in model:
            if var > 0 :
                print(var , ms.get_index(var))
    else:
        print("*** UNSAT ***")
        print(ms.s.get_core())

if __name__ == '__main__':
    main()
