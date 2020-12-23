"""
Hang Zhang et al. "`ResNeSt: Split-Attention Networks
<https://arxiv.org/abs/2004.08955>`_"
"""
from .encoder_decoder import Encoder
from .blocks import ResNeStBlock

class ResNeSt(Encoder):
    """ Base ResNeSt architecture. """
    @classmethod
    def default_config(cls):
        config = super().default_config()

        config['initial_block'] += dict(layout='cnap', filters=64, kernel_size=1, bias=False, padding='same',
                                        pool_size=3, pool_strides=2)

        config['body/encoder/num_stages'] = 4
        config['body/encoder/order'] = ['skip', 'block']
        config['body/encoder/blocks'] += dict(base=ResNeStBlock, layout='S', attention='sac',
                                              filters=[64, 128, 256, 512],
                                              n_reps=[1, 1, 1, 1], radix=2, cardinality=1)

        config['head'] += dict(layout='Vdf', dropout_rate=.4)

        config['loss'] = 'ce'
        return config



class ResNeSt18(ResNeSt):
    """ ResNeSt-18 architecture. """
    @classmethod
    def default_config(cls):
        config = super().default_config()
        config['body/encoder/blocks/n_reps'] = [2, 2, 2, 2]
        return config

class ResNeSt34(ResNeSt):
    """ ResNeSt-34 architecture. """
    @classmethod
    def default_config(cls):
        config = super().default_config()
        config['body/encoder/blocks/n_reps'] = [3, 4, 6, 3]
        return config
