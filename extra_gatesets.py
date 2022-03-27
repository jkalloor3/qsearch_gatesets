import qsearch
from qsearch.gates import *
from qsearch.gatesets import *
from extra_gates import *
from qsrs import native_from_object

# gates stated in the abstract:
# CNOT
# sqrtCNOT
# iSWAP
# sqrtiSWAP
# Molmer-Sorensen
# XX (parameterized)
# CRz (parameterized)

# qutrits:
# CNOT
# CSUM


class QubitLinear(Gateset):
    def __init__(self, single_gate=U3Gate(), single_alt=None, double_gate=CNOTGate(), enable_find3=False):
        self.single_gate = single_gate
        self.single_alt = single_gate if single_alt is None else single_alt
        self.double_gate = double_gate
        self.d = 2

    def initial_layer(self, n):
        return fill_row(self.single_gate, n)

    def search_layers(self, n):
        return linear_topology(self.double_gate, self.single_gate, n, self.d, single_alt=self.single_alt)

    def branching_factor(self, qudits):
        return qudits-1

    def successors(self, circ, qudits=None):
        return super().successors(circ, qudits)
        if qudits is None:
            qudits = int(np.log(circ.matrix([0]*circ.num_inputs).shape[0])/np.log(self.d))

        skip_index = None if not enable_find3 else find_last_3_cnots_linear(circ)

        return [(circ.appending(layer[0]), layer[1]) for layer in linear_topology(self.double_gate, self.single_gate, qudits, self.d, single_alt=self.single_alt, skip_index=skip_index)]


class QubitDuoLinear(Gateset):
    def __init__(self, single_gate=U3Gate(), single_alt=None, double_gate=CNOTGate(), duo_gate=ISwapGate()):
        self.single_gate = single_gate
        self.single_alt = single_gate if single_alt is None else single_alt
        self.two_gate = double_gate
        self.two_duo = duo_gate
        self.d = 2

    def initial_layer(self, n):
        return fill_row(self.single_gate, n)

    def search_layers(self, n):
        return linear_topology(self.two_gate, self.single_gate, n, self.d, single_alt=self.single_alt) + linear_topology(self.two_duo, self.single_gate, n, self.d)



demo_gatesets = []

# constant gates
# demo_gatesets.append(("CRZ", QubitLinear(double_gate=CRZGate(), enable_find3=True)))
# demo_gatesets.append(("XX", QubitLinear(double_gate=RXXGate(), enable_find3=True)))
# demo_gatesets.append(("MS", QubitLinear(double_gate=MSGate(), enable_find3=True)))
demo_gatesets.append(("ISWAP", QubitISwapLinear()))
demo_gatesets.append(("CNOT", QubitCNOTLinear()))
demo_gatesets.append(("sqrt(CNOT)", QubitLinear(double_gate=CNOTRootGate())))
demo_gatesets.append(("sqrt(ISWAP)", QubitLinear(double_gate=SQISWGate(), enable_find3=True)))

duo_gatesets = []
duo_gatesets.append(("CNOT_ISWAP", QubitDuoLinear(duo_gate=ISwapGate(), single_alt=XZXZGate())))
duo_gatesets.append(("CNOT_sqrt(ISWAP)", QubitDuoLinear(duo_gate=SQISWGate(), single_alt=XZXZGate())))

qutrit_gatesets = []
qutrit_gatesets.append(("qtCNOT", QutritCNOTLinear()))
#qutrit_gatesets.append(("qt_CSUM", QutritCSUMLinear()))
# varialbe gates
#demo_gatesets.append(("XX", QubitLinear(double_gate=RXXGate())))

# akel uses ring topology
# continuously parameterized cphase
# google uses "fswap"?
