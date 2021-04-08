## this example shows how to use pomegranate to set up the Bayesian network representing
## the burglary/alarm example seen in class.

from pomegranate import *

def buildAlarmGraph() :
    burglary = DiscreteDistribution( { 'True' : 0.001, 'False' : 0.999 } )
    earthquake = DiscreteDistribution({'True': 0.002, 'False': 0.998})
    alarm = ConditionalProbabilityTable(
        [["True", "True", "True", 0.95],
         ["True", "True", "False", 0.05],
         ["True", "False", "True", 0.94],
        ["True", "False", "False", 0.06],
         ["False", "True", "False", 0.71],
        ["False", "True", "True", 0.29],
        ["False", "False", "True", 0.001],
         ["False", "False", "False", 0.999]], [burglary, earthquake]
    )
    johnCalls = ConditionalProbabilityTable(
        [["True", "True", 0.90],
         ["True", "False", 0.1],
        ["False", "True", 0.05],
        ["False", "False", 0.95]], [alarm]
    )
    maryCalls = ConditionalProbabilityTable(
        [["True", "True", 0.70],
         ["True", "False", 0.30],
        ["False", "True", 0.01],
         ["False", "False", 0.99]], [alarm]
    )
    s1 = State(burglary, name="burglary")
    s2 = State(earthquake, name="earthquake")
    s3 = State(alarm, name="alarm")
    s4 = State(johnCalls, name="johnCalls")
    s5 = State(maryCalls, name="maryCalls")

    network = BayesianNetwork("alarm network")
    network.add_nodes(s1,s2,s3,s4,s5)
    network.add_edge(s1,s3)
    network.add_edge(s2,s3)
    network.add_edge(s3,s4)
    network.add_edge(s3,s5)
    network.bake()
    return network

if __name__ == '__main__':
    net = buildAlarmGraph()
    observations = {"alarm": "False", "earthquake": "False"}
    beliefs = map(str, net.predict_proba(observations))
    print("\n".join("{}\t\t{}".format(state.name, belief) for state, belief in zip(net.states, beliefs)))

