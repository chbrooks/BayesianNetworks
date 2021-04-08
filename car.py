from pomegranate import *

# function builds the cat starts network
# an already-baked pomegranate.BayesianNetwork
def buildFirstGraph() :
    battery = DiscreteDistribution({'True': 0.5, 'False': 0.5})
    gas = DiscreteDistribution({'True': 0.5, 'False': 0.5})

    radio = ConditionalProbabilityTable(
        [['True', 'True', 0.85],  # battery true, radio true
         ['True', 'False', 0.15],  # battery true, radio false
         ['False', 'True', 0.0],  # batter false, radio true
         ['False', 'False', 1.0]], [battery])

    ignition = ConditionalProbabilityTable(
        [['True', 'True', 0.95],  # battery true, ignition true
         ['True', 'False', 0.05],  # battery true, ignition false
         ['False', 'True', 0.0],
         ['False', 'False', 1.0]], [battery])

    starts = ConditionalProbabilityTable(
        [['True', 'True', 'True', 0.99],  # ignition true, gas true, starts true
         ['True', 'True', 'False', 0.01],
         ['True', 'False', 'True', 0.0],  # no gas
         ['True', 'False', 'False', 1.0],
         ['False', 'True', 'True', 0.0],  # no ignition
         ['False', 'True', 'False', 1.0],
         ['False', 'False', 'True', 0.0],
         ['False', 'False', 'False', 1.0]  # no ignition, no gas
         ], [ignition, gas])

    moves = ConditionalProbabilityTable(
        [['True', 'True', 0.95],
         ['True', 'False', 0.05],
         ['False', 'True', 0.0],
         ['False', 'False', 1.0]], [starts])

    state_0 = State(battery, name="Battery")
    state_1 = State(gas, name="Gas")
    state_2 = State(radio, name="Radio")
    state_3 = State(ignition, name="Ignition")
    state_4 = State(starts, name="Starts")
    state_5 = State(moves, name="Moves")

    network = BayesianNetwork("Battery")
    network.add_nodes(state_0, state_1, state_2, state_3, state_4, state_5)

    network.add_edge(state_0, state_2)
    network.add_edge(state_0, state_3)
    network.add_edge(state_1, state_4)
    network.add_edge(state_3, state_4)
    network.add_edge(state_4, state_5)

    network.bake()
    return network
