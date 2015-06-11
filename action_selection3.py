import nengo
import nengo.spa as spa

D = 16

model = spa.SPA()
with model:
    model.wm = spa.Buffer(D)
    
    vocab = model.get_output_vocab('wm')

    bg = nengo.networks.BasalGanglia(4)

    
    nengo.Connection(model.wm.state.output,
        bg.input, transform=[vocab.parse('DOG').v,
                            vocab.parse('CAT').v,
                            vocab.parse('RAT').v,
                            vocab.parse('COW').v])
                            
    thal = nengo.networks.EnsembleArray(n_neurons=50, 
                    n_ensembles=4, 
                    encoders=nengo.dists.Choice([[1]]),
                    intercepts=nengo.dists.Uniform(0.3,0.9))
                    
    import numpy as np
    nengo.Connection(thal.output, thal.input,
                transform=(np.eye(4)-1))
    
    bias = nengo.Node([1,1,1,1])
    nengo.Connection(bias, thal.input)
    nengo.Connection(bg.output, thal.input)
    
    
    
    