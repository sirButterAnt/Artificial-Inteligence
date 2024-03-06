
import random

dictionary = {1 : 0.2, 1.25 : 0.3, 1.50:0.3, 1.75:0.2}

states = {i: [0] for i in range(101)}

stateTransition = {i: {} for i in range(101)}

optimalPolicy =  {}
for state in stateTransition:
    for probability in dictionary:
        roundedNumber = round(state*probability)
        if roundedNumber > 100:
            roundedNumber = 100
        if roundedNumber in stateTransition[state]:
            stateTransition[state][roundedNumber] = stateTransition[state][roundedNumber] +dictionary[probability]
        else :
            stateTransition[state][roundedNumber] = dictionary[probability]


def iterationEnder(dict):
    boolean = False

    for state in dict:
        if dict[state][-1] != dict[state][-2]:
            boolean = True
    return boolean

def valueIteration(numberOfIteration):
    numberOfIteration = 1
    boolean = True
    while boolean:
        for state in states:
            optimalUtility = 0
            for action in range(state + 1):
                actionUtility = action
                for nextYear in stateTransition[state-action]:
                    actionUtility += 0.9 * states[nextYear][numberOfIteration-1] *  stateTransition[state-action][nextYear]
                if actionUtility > optimalUtility:
                    optimalUtility = actionUtility
                    optimalPolicy[state] = action 
            states[state].append(optimalUtility)   
            print(f"Utility of {state} = {optimalUtility}")     
        boolean = iterationEnder(states)
        numberOfIteration += 1


valueIteration(2)

print(optimalPolicy)


def calculate_state_transitions(dictionary, max_state=100):
 
    state_transition = {i: {} for i in range(max_state + 1)}
    for state in state_transition:
        for probability, prob_value in dictionary.items():
            next_state = min(round(state * probability), max_state)
            state_transition[state][next_state] = state_transition[state].get(next_state, 0) + prob_value
    return state_transition
 

#policyIteration-----------------------------------------------------------------
def policyIteration(states, state_transition, discount_factor=0.9, threshold=0.01):
 
    is_converged = False
    while not is_converged:
        is_converged = True
        for state in states:
            max_utility = -100
            best_action = None
            for action in range(state + 1):
                utility = action  # Immediate reward
                for next_state, prob in state_transition[state - action].items():
                    utility += discount_factor * prob * max(states[next_state].values())  # Future reward
                if utility > max_utility:
                    max_utility = utility
                    best_action = action
           
            if abs(states[state][best_action] - max_utility) > threshold:
                is_converged = False
                states[state][best_action] = max_utility
    return states
 #I didnt print policy iterations every iterations
print("policy iteration")
dictionary = {1: 0.2, 1.25: 0.3, 1.50: 0.3, 1.75: 0.2}
states = {i: {j: 0 for j in range(i + 1)} for i in range(101)}
 
 
state_transition = calculate_state_transitions(dictionary)
 
 
best_actions = policyIteration(states, state_transition)
 
 
optimal_actions = {state: max(actions, key=actions.get) for state, actions in best_actions.items()}
print(optimal_actions)

