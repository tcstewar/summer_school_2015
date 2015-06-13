import nengo
import nengo.spa as spa

D = 16

model = spa.SPA()
with model:
    model.vision = spa.Buffer(D)
    model.motor = spa.Buffer(D)
    
    actions = spa.Actions(
        '0 --> motor = A',
        '0 --> motor = B',
        '0.5 --> motor = UNKNOWN',
        )
    
    model.bg = spa.BasalGanglia(actions)
    model.thal = spa.Thalamus(model.bg)
    
    target = nengo.Node([0, 0])
    
    error = nengo.networks.EnsembleArray(50, 2)
    
    stop_learning = nengo.Node([0])
    
    for i in range(1):
        nengo.Connection(stop_learning, error.ensembles[i].neurons,
                    transform=[[-10]]*50)
        nengo.Connection(target[i], error.ensembles[i])
        nengo.Connection(model.bg.strD1.ensembles[i], error.ensembles[i],
                            transform=-1)
    
        conn = nengo.Connection(model.vision.state.ensembles[0], 
                    model.bg.strD1.ensembles[i], function=lambda x: 0)
        error_conn = nengo.Connection(error.ensembles[i], model.bg.strD1.ensembles[i],
                            modulatory=True)
        conn.learning_rule_type=nengo.PES(error_conn)
        conn.learning_rule_type.learning_rate *= 0.1
    