from ANNarchy.core.Projection import Projection
from ANNarchy.core.Synapse import Synapse
import ANNarchy.core.Global as Global

import numpy as np



###############################
### Shared synapse for report()
###############################
class SharedSynapse(Synapse):
    # For reporting
    _instantiated = []
    def __init__(self, psp, operation):
        Synapse.__init__(self, 
            psp=psp, operation=operation,
            name="Shared Weight", 
            description="Weight shared over all synapses of the projection."
        )
        # For reporting
        self._instantiated.append(True)


###############################
### Shared projection
###############################
class Convolution2D(Projection):
    """
    Projection class implementing a 2D convolution.
    """
    def __init__(self, pre, post, target, psp="w * pre.r", operation="sum"):
        # Create the description, but it will not be used for generation
        Projection.__init__(
            self,
            pre,
            post,
            target,
            synapse = SharedSynapse(psp=psp, operation=operation)
        )
        self._omp_config['psp_schedule'] = 'schedule(dynamic)'
        if not Global.config["paradigm"] == "openmp":
            Global._error('SharedProjection: Weight sharing is only implemented for the OpenMP paradigm.')

        if not pre.neuron_type.type == 'rate':
            Global._error('SharedProjection: Weight sharing is only implemented for rate-coded populations.')