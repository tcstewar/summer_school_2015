import nengo
import nengo.spa as spa

D = 64
model = spa.SPA(seed=1)
with model:
    model.vision = spa.Buffer(D)
    model.sentence = spa.Memory(D, synapse=0.1)
    model.hand = spa.Buffer(D)
    model.speech = spa.Buffer(D)
    
    actions = spa.Actions(
        'dot(vision, WRITE+SAY) --> sentence=vision*VERB*0.5',
        'dot(vision, ONE+TWO+THREE) --> sentence=vision*NOUN*0.5',
        'dot(sentence, WRITE*VERB)-dot(vision, ONE+TWO+THREE+WRITE+SAY)  --> hand=sentence*~NOUN',
        'dot(sentence, SAY*VERB)-dot(vision, ONE+TWO+THREE+WRITE+SAY) --> speech=sentence*~NOUN',
        )
        
    model.bg = spa.BasalGanglia(actions)
    model.thal = spa.Thalamus(model.bg)
