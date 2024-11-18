import random

class Agent:
    def __init__(self, name, initial_state, noise=1):
        self.id  = name 
        self.x_0 = initial_state   # initial value of the quantity being measured for this particular agent
        self.x_k = self.x_0        # approximated value of the quantity being measured by this agent 
        self.xN_k = {}             # dictionary of all neighbours and their (last communicated) values that the agent is connected to 
                                   # (not the neighbours that are connected to it)
        self.noise = noise         # measure of how noisy the measurements are
        self.step = 0.4

    def __str__(self):
        return self.id + ':' + str(self.x_k) 

    def connect(self, neighbour):
        if neighbour.id not in self.xN_k:
            self.xN_k[neighbour.id] = 0

    def communicate(self, neighbour):
        if neighbour.id in self.xN_k:
            self.xN_k[neighbour.id] = neighbour.x_k 
        
    def measure(self):
        return random.random() * self.noise + 5

    def update_state(self, measurement):
        measurement = measurement - self.x_k
        self.x_k = self.x_k + self.step * (self._protocol() + measurement)

    def _protocol(self) -> float:
        '''Gradient-based feedback of how much the agent doesn't agree with it's neighbours.'''
        u = 0
        for _, xN_k in self.xN_k.items():
            u = u + (xN_k - self.x_k)
        
        return u
    
    def _protocol1(self) -> float:
        u = 0
        for _, xN_k in self.xN_k.items():
            u = u + xN_k
        
        u = 1/(1+len(self.xN_k.items())) * (self.x_k + u)
        
        return u

if __name__ == "__main__":
    A = Agent('A', 5)
    B = Agent('B', 4)
    C = Agent('C', 6)

    A.connect(B)
    A.connect(C)
    B.connect(A)
    B.connect(C)
    #C.connect(A) # in order for convergence to occur all nodes need to be connected
    C.connect(B)

    iterations = 0

    print(A)
    print(B)
    print(C)
    print('-------')

    while round(A.x_k, 3) != round(B.x_k, 3) or round(B.x_k, 3) != round(C.x_k, 3):
        A.communicate(B)
        A.communicate(C)
        B.communicate(A)
        B.communicate(C)
        # C.communicate(A)
        C.communicate(B)

        A.update_state(5.2)
        B.update_state(5.5)
        C.update_state(4.9)

        iterations = iterations + 1

        print(A)
        print(B)
        print(C)
        print('-------')
    
    print('Iteration count: ' + str(iterations))




