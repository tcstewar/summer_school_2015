import nengo
import nengo.spa as spa

D = 16

model = spa.SPA()
with model:
    model.color = spa.Buffer(D)
    model.shape = spa.Buffer(D)
    model.wm = spa.Buffer(D)
    cconv = nengo.networks.CircularConvolution(
        n_neurons=200, dimensions=D)
    nengo.Connection(model.color.state.output,
        cconv.A)
    nengo.Connection(model.shape.state.output,
        cconv.B)
        
    nengo.Connection(cconv.output, model.wm.state.input,
            transform=0.1)
    
    nengo.Connection(model.wm.state.output,
                        model.wm.state.input, synapse=0.1)
                        
                        
    model.query = spa.Buffer(D)          
    
    model.result = spa.Buffer(D)
    
    deconv = nengo.networks.CircularConvolution(
        n_neurons=200, dimensions=D, invert_b=True)
    deconv.label = 'deconv'
    
    nengo.Connection(model.wm.state.output,
            deconv.A)
    nengo.Connection(model.query.state.output,
            deconv.B)
    nengo.Connection(deconv.output, 
            model.result.state.input)
    
    vocab = model.get_output_vocab('result')
    subvocab = vocab.create_subset(['SQR', 'BLUE', 
                                    'RED', 'TRI'])
    
    model.cleanup = spa.AssociativeMemory(subvocab)
         
    model.clean_result = spa.Buffer(D)
    nengo.Connection(model.result.state.output,
        model.cleanup.input)
    nengo.Connection(model.cleanup.output,
        model.clean_result.state.input)
