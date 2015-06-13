import nengo
import nengo.spa as spa

D = 16

model = spa.SPA()
with model:
    model.visual = spa.Buffer(D)
    model.speech = spa.Buffer(D)
    model.hand = spa.Buffer(D)
    
    model.combined = spa.Buffer(D)
    
    model.verb = spa.Memory(D, synapse=0.1)
    model.noun = spa.Memory(D, synapse=0.1)
    
    vocab = model.get_output_vocab('visual')
    vocab.add('ALL_NOUNS', vocab.parse('HELLO+GOODBYE').v)
    vocab.add('ALL_VERBS', vocab.parse('SAY+WRITE').v)
    actions = spa.Actions(
        'dot(visual, ALL_VERBS) --> combined=visual*VERB',
        'dot(visual, ALL_NOUNS) --> combined=visual*NOUN',
        'dot(combined, SAY*VERB) - '
            'dot(visual, ALL_VERBS+ALL_NOUNS) '
            '--> speech=combined*~NOUN',
        'dot(combined, WRITE*VERB) '
            '-dot(visual, ALL_VERBS+ALL_NOUNS) '
            '--> hand=combined*~NOUN',
        )
        
    model.bg = spa.BasalGanglia(actions)
    model.thal = spa.Thalamus(model.bg)
    
    cortical_actions = spa.Actions(
        'combined = verb*VERB',
        'combined = noun*NOUN',
    )
    
    model.cortical = spa.Cortical(cortical_actions)
    
    