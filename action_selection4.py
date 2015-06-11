import nengo
import nengo.spa as spa

D = 16

model = spa.SPA()
with model:
    model.wm = spa.Memory(D)
    model.vision = spa.Buffer(D)
    model.speech = spa.Buffer(D)
    
    actions = spa.Actions(
        'dot(DOG,wm) --> speech=BARK',
        'dot(CAT,wm) --> speech=MEOW',
        'dot(RAT,wm) --> speech=SQUEAK',
        'dot(COW,wm) + dot(vision,FARM) - 1 --> speech=MOO',
        )
        
    actions2 = spa.Actions(
        'dot(vision, A+B+C+D+E)*1.4 --> wm=vision',
        'dot(wm, A)*0.8 --> wm=B',
        'dot(wm, B)*0.8 --> wm=C',
        'dot(wm, C)*0.8 --> wm=D',
        'dot(wm, D)*0.8 --> wm=E',
        'dot(wm, E)*0.8 --> wm=A',
    )
        
        
    model.bg = spa.BasalGanglia(actions2)
    model.thal = spa.Thalamus(model.bg)
        
    