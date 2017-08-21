di = {((0,0), 'exit'): 5, ((1,1), 'left'):3, ((2,2), 'right'):7}
state_actions = [((0,0), 'exit'), ((1,1), 'left'), ((2,2), 'right')]
values = [di.get(state_action) for state_action in state_actions]
print di
print state_actions
print values

return_action = state_actions[values.index(max(values))][1]
print return_action
