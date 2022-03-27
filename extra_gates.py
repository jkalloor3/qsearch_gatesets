import qsearch
from qsearch.gates import *

# from IBM
SQISW = np.array([[1,0,0,0],
                  [0,1/np.sqrt(2), 1j/np.sqrt(2),0],
                  [0,1j/np.sqrt(2),1/np.sqrt(2),0],
                  [0,0,0,1]],
                  dtype='complex128')

# CRZ = # from IBM
# SQISW = np.array([[1,0,0,0],
#                   [0,1/np.sqrt(2), 1j/np.sqrt(2),0],
#                   [0,1j/np.sqrt(2),1/np.sqrt(2),0],
#                   [0,0,0,1]],
#                   dtype='complex128')

# from IONQ
MS = np.array([[1,0,0,-1j],
               [0,1,-1j,0],
               [0,-1j,1,0],
               [-1j,0,0,1]],
               dtype='complex128') / np.sqrt(2)

class SQISWGate(Gate):
    def __init__(self):
        self.num_inputs = 0
        self.qudits = 2

    def __eq__(self, other):
        return type(self) == type(other)

    def matrix(self, v):
        return SQISW

    def assemble(self, v, i=0):
        return [("gate", "SQISW", (), (i, i+1))]

    def __repr__(self):
        return "SQISWGate()"

class MSGate(Gate):
    def __init__(self):
        self.num_inputs = 0
        self.qudits = 2

    def __eq__(self, other):
        return type(self) == type(other)

    def matrix(self, v):
        return MS

    def assemble(self, v, i=0):
        return [("gate", "MS", (), (i, i+1))]

    def __repr__(self):
        return "MSGate()"

class RXXGate(Gate):
    def __init__(self):
        self.d = 2
        self.qudits = 2
        self.num_inputs = 1

    def assemble(self, v, i=0):
        return [("gate", "XX", (v[0]), (i, i+1))]

    def __repr__(self):
        return "RXXGate()"

    def __eq__(self, other):
        return type(self) == type(other)

    def matrix(self, v):
        return native_from_object(self).matrix(np.array(v, dtype='float64'))

    def mat_jac(self, v):
        return native_from_object(self).mat_jac(v)

class CRZGate(Gate):
    def __init__(self):
        self.d = 2
        self.qudits = 2
        self.num_inputs = 1

    def assemble(self, v, i=0):
        return [("gate", "CRZ", (v[0]), (i, i+1))]

    def __repr__(self):
        return "CRZGate()"

    def __eq__(self, other):
        return type(self) == type(other)

    def matrix(self, v):
        return native_from_object(self).matrix(np.array(v, dtype='float64'))

    def mat_jac(self, v):
        return native_from_object(self).mat_jac(v)
