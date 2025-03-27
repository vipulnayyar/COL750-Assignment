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
                print(line)
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


            if (i == 0 and j == 0) or (i == size - 1 and j == size - 1):
                continue

            row_elements.append(ms.get_address(i,j))
            print(i,j, ms.get_address(i,j))
            print(ms.get_index(ms.get_address(i,j)))

            if array[i][j] == 'X':
                print(f"Adding negative clause for {i} , {j} ")
                ms.add_clause([-1 * ms.get_address(i,j)])
            #else:
            #    print(f"Adding positive clause for {i} , {j} ")
            #    s.add_clause([get_address(i,j, size)])

            nextright = 0
            nextdown = 0

            if(i == size - 1):
                if array[i][j+1] == '.' or array[i][j+1] == 'G':
                    nextright = 1
                else:
                    nextright = -1

                ms.add_clause([-1 * ms.get_address(i,j), nextright * ms.get_address(i,j+1)])
            
            elif(j == size - 1):

                if array[i+1][j] == '.' or array[i+1][j] == 'G':
                    nextdown = 1
                else:
                    nextdown = -1

                ms.add_clause([-1 * ms.get_address(i,j), nextdown * ms.get_address(i+1,j)])
            else:
                if array[i][j+1] == '.' or array[i][j+1] == 'G':
                    nextright = 1
                else:
                    nextright = -1

                if array[i+1][j] == '.' or array[i+1][j] == 'G':
                    nextdown = 1
                else:
                    nextdown = -1

                ms.add_clause([-1 * ms.get_address(i,j), nextdown * ms.get_address(i+1,j), nextright * ms.get_address(i,j+1) ])
        ms.add_clause(row_elements)
   
    #for j in range(len(array)):
        
               


    # Add Slot constraints : Minimum 1

    result = ms.s.solve()
    if result:
        print("SAT")
        model = ms.s.get_model()

        for var in model:
            if var > 0 :
                print(ms.get_index(var))
    else:
        print("UNSAT")
        print(ms.ss.get_core())

if __name__ == '__main__':
    main()
