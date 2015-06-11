import nengo

model = nengo.Network('Basal Ganglia')
with model:
    mm = 1
    mp = 1
    me = 1
    mg = 1
    ws = 1
    wt = 1
    wm = 1
    wg = 1
    wp = 0.9
    we = 0.3
    e = 0.2
    ep = -0.25
    ee = -0.2
    eg = -0.2
    le = 0.2
    lg = 0.2
    tau_ampa = 0.002
    tau_gaba = 0.008
    N = 50
    D = 4
    model.config[nengo.Ensemble].radius = 1.5
    model.config[nengo.Ensemble].encoders = nengo.dists.Choice([[1]])
    
    strD1 = nengo.networks.EnsembleArray(N, D, label="StrD1", 
                intercepts=nengo.dists.Uniform(e, 1))
    strD2 = nengo.networks.EnsembleArray(N, D, label="StrD2", 
                intercepts=nengo.dists.Uniform(e, 1))
    stn = nengo.networks.EnsembleArray(N, D, label="STN", 
                intercepts=nengo.dists.Uniform(ep, 1))
    gpi = nengo.networks.EnsembleArray(N, D, label="GPi", 
                intercepts=nengo.dists.Uniform(eg, 1))
    gpe = nengo.networks.EnsembleArray(N, D, label="GPe", 
                intercepts=nengo.dists.Uniform(ee, 1))

    input = nengo.Node([0]*D, label="input")
    output = nengo.Node(label="output", size_in=D)

    # spread the input to StrD1, StrD2, and STN
    nengo.Connection(input, strD1.input, synapse=None,
                     transform=ws * (1 + lg))
    nengo.Connection(input, strD2.input, synapse=None,
                     transform=ws * (1 - le))
    nengo.Connection(input, stn.input, synapse=None,
                     transform=wt)    
                     
    # connect the striatum to the GPi and GPe (inhibitory)
    def func_str(x):
        if x < e:
            return 0
        return mm * (x - e)
    strD1.add_output('func', func_str)
    import numpy
    nengo.Connection(strD1.func,
                     gpi.input, synapse=tau_gaba,
                     transform=-numpy.eye(D) * wm)
    strD2.add_output('func', func_str)
    nengo.Connection(strD2.func,
                     gpe.input, synapse=tau_gaba,
                     transform=-numpy.eye(D) * wm)                     
    def func_stn(x):
        if x < ep:
            return 0
        return mp * (x - ep)
                     
    # connect the STN to GPi and GPe (broad and excitatory)
    tr = wp * numpy.ones((D, D))
    stn.add_output('func', func_stn)
    nengo.Connection(stn.func, gpi.input,
                     transform=tr, synapse=tau_ampa)
    nengo.Connection(stn.func, gpe.input,
                     transform=tr, synapse=tau_ampa)

    def func_gpe(x):
        if x < ee:
            return 0
        return me * (x - ee)

    # connect the GPe to GPi and STN (inhibitory)
    gpe.add_output('func', func_gpe)
    nengo.Connection(gpe.func, gpi.input, synapse=tau_gaba,
                     transform=-we)
    nengo.Connection(gpe.func, stn.input, synapse=tau_gaba,
                     transform=-wg)

    def func_gpi(x):
        if x < eg:
            return 0
        return mg * (x - eg)
    # connect GPi to output (inhibitory)
    gpi.add_output('func', func_gpi)
    nengo.Connection(gpi.func, output)