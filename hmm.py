## example HMM

from pomegranate import *

## my cat has three states: grumpy, happy, and hungry.  I want to figure out her moods
##  using a HMM. 
## When she's grumpy, she meows with P=0.4, is silent with P=0.5, and purrs with P=0.1
grumpyDist=DiscreteDistribution({'meow': 0.4, 'silent':0.5, 'purr':0.1})
## When she's happy, she meows with P=0.2, is silent with P=0.3, and purrs with P=0.5
happyDist=DiscreteDistribution({'meow': 0.2, 'silent':0.3, 'purr':0.5})
## When she's hungry, she meows with P=0.6, is silent with P=0.2, and purrs with P=0.2
hungryDist=DiscreteDistribution({'meow': 0.6, 'silent':0.2, 'purr':0.2})

## let's make a state for each mood
grumpy = State(grumpyDist,name='grumpy')
happy = State(happyDist, name='happy')
hungry = State(happyDist, name='hungry')

model = HiddenMarkovModel()
model.add_states(grumpy, happy, hungry)

## let's assume my cat starts out happy with P=0.5, and hungry with P=0.5
model.add_transition(model.start, happy, 0.5)
model.add_transition(model.start, hungry, 0.5)

## when she's happy, she stays happy with P=0.5, gets grumpy with P=0.1, and hungry with P=0.4
model.add_transition(happy, happy, 0.5)
model.add_transition(happy, grumpy, 0.1)
model.add_transition(happy, hungry, 0.4)

## when she's hungry, she stays hungry with P=0.3, gets grumpy with P=0.6, and gets happy (fed) withP=0.1
model.add_transition(hungry, hungry, 0.3)
model.add_transition(hungry, grumpy, 0.6)
model.add_transition(hungry, happy, 0.1)

## when she's grumpy, she stays grumpy with  P=0.3, switches back to hungry with P=0.1, and gets happy (fed) with P=0.6
model.add_transition(grumpy, grumpy, 0.3)
model.add_transition(grumpy, hungry, 0.1)
model.add_transition(grumpy, happy, 0.6)

model.bake()

## let's generate a random sequence of observations.
    
obs=model.sample(length=50)

## now let's predict the sequence of states that generated these observations.

model.predict(obs)

##  these ids are annoying. Let's see the state names.

[model.states[a].name for a in model.predict(obs)]

