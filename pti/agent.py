
class Agent:
    def __init__(self, name, initial_state):
        self.id  = name 
        self.x_0 = initial_state   # initial value of the quantity being measured for this particular agent
        self.x_k = self.x_0        # approximated value of the quantity being measured by this agent 
        self.xN_k = {}             # dictionary of all neighbours and their (last communicated) values that the agent is connected to 
                                   # (not the neighbours that are connected to it)
    
    def __str__(self):
        return self.id + ':' + str(self.x_k) 

    def connect(self, neighbour):
        if neighbour.id not in self.xN_k:
            self.xN_k[neighbour.id] = 0

    def communicate(self, neighbour):
        if neighbour.id in self.xN_k:
            self.xN_k[neighbour.id] = neighbour.x_k 

    def update_state(self, measurement):
        self.x_k = self.x_k + self._protocol() + measurement

    def _protocol(self) -> float:
        '''Gradient-based feedback of how much the agent doesn't agree with it's neighbours.'''
        u = 0
        for name, xN_k in self.xN_k.items():
            u = u + (xN_k - self.x_k)
        
        return u

if __name__ == "__main__":
    A = Agent('A', 5)
    B = Agent('B', 6)
    C = Agent('C', 2)

    A.connect(B)
    B.connect(C)
    C.connect(B) # in order for convergence to occur all nodes need to be connected

    iterations = 0

    print(A)
    print(B)
    print(C)
    print('-------')

    while A.x_k != B.x_k or B.x_k != C.x_k:
        A.communicate(B)
        B.communicate(C)
        C.communicate(B)

        A.update_state(0)
        B.update_state(0)
        C.update_state(0)

        iterations = iterations + 1

        print(A)
        print(B)
        print(C)
        print('-------')
    
    print('Iteration count: ' + str(iterations))




