import nengo
import nengo.spa as spa

D = 16

model = spa.SPA()
with model:
    model.wm = spa.Buffer(D)
    
    q = nengo.networks.EnsembleArray(n_neurons=50,
            n_ensembles=4)
    
    vocab = model.get_output_vocab('wm')
    
    nengo.Connection(model.wm.state.output,
        q.input, transform=[vocab.parse('DOG').v,
                            vocab.parse('CAT').v,
                            vocab.parse('RAT').v,
                            vocab.parse('COW').v])
                            
    
    e = 0.5
    i = -1

    transform = [[e, i, i, i], 
                 [i, e, i, i], 
                 [i, i, e, i], 
                 [i, i, i, e]]
    def rectified(x):
        if x < 0:
            return 0
        else:
            return x
    q.add_output('rectified', rectified)
    nengo.Connection(q.rectified, q.input, 
                    transform=transform)
                    
    
    