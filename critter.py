import nengo

model = nengo.Network()
with model:
    target_command = nengo.Node([0,0])
    target = nengo.Ensemble(100, 2)
    nengo.Connection(target_command, target)
    
    motor = nengo.Ensemble(100, 2)
    

    position = nengo.Ensemble(600, 2, radius=5)
    
    tau = 0.1
    nengo.Connection(position, position, synapse=tau)
    nengo.Connection(motor, position, transform=tau)
    
    starting_dir = nengo.Ensemble(200, 2)
    nengo.Connection(position, starting_dir, transform=-1)
    
    scared_stim = nengo.Node([0])
    scared = nengo.Ensemble(50, 1)
    nengo.Connection(scared_stim, scared)
    
    select_target = nengo.Ensemble(500, dimensions=3)
    nengo.Connection(target, select_target[:2])
    
    def convert_scared(x):
        return 1-x
    nengo.Connection(scared, select_target[2], function=convert_scared)
    
    def do_select_target(state):
        x, y, select = state
        return [x*(select), y*(select)]
    nengo.Connection(select_target, motor, function=do_select_target)
        
        
    select_runaway = nengo.Ensemble(500, 3)
    nengo.Connection(starting_dir, select_runaway[:2])
    nengo.Connection(scared, select_runaway[2])
    
    def do_select_runaway(state):
        x, y, select = state
        return [x*select, y*select]
    nengo.Connection(select_runaway, motor, function=do_select_runaway)
    
    
    
    