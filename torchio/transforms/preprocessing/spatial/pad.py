from typing import Union, Tuple, Callable
import SimpleITK as sitk
from .bounds_transform import BoundsTransform, TypeBounds


class Pad(BoundsTransform):
    """Pad an image.

    Args:
        padding: Tuple
            :math:`(D_{ini}, D_{fin}, H_{ini}, H_{fin}, W_{ini}, W_{fin})`
            defining the number of values padded to the edges of each axis.
            If only three values :math:`(D, H, W)` are provided, then
            :math:`D_{ini} = D_{fin} = D`,
            :math:`H_{ini} = H_{fin} = H` and
            :math:`W_{ini} = W_{fin} = W`.
            If only one value :math:`N` is provided, then
            :math:`D_{ini} = D_{fin} = H_{ini} = H_{fin} = W_{ini} = W_{fin} = N`.
        padding_mode:
            Type of padding. Default is ``constant``. Should be one of:

            - ``constant`` Pads with a constant value (specified in :attr:`padding_fill`).

            - ``reflect`` Pads with reflection of image without repeating the last value on the edge.

            - ``edge`` Pads with the last value at the edge of the image.

            - ``replicate`` Same as ``edge``.

            - ``circular`` Pads with the wrap of the vector along the axis. The first values are used to pad the end and the end values are used to pad the beginning.

            - ``wrap`` Same as ``circular``.


        fill: Value for constant fill. Default is ``0``. This value is only
            used when :attr:`padding_mode` is ``constant``.

        verbose:

    """

    PADDING_FUNCTIONS = {
        'constant': sitk.ConstantPad,
        'reflect': sitk.MirrorPad,
        'replicate': sitk.ZeroFluxNeumannPad,
        'edge': sitk.ZeroFluxNeumannPad,
        'circular': sitk.WrapPad,
    }

    def __init__(
            self,
            padding: TypeBounds,
            padding_mode: str = 'constant',
            fill: float = None,
            verbose: bool = False,
            ):
        """
        padding_mode can be 'constant', 'reflect', 'replicate' or 'circular'.
        See https://pytorch.org/docs/stable/nn.functional.html#pad for more
        information about this transform.
        """
        super().__init__(padding, verbose=verbose)
        self.padding_mode = self.parse_padding_mode(padding_mode)
        self.fill = fill

    @classmethod
    def parse_padding_mode(cls, padding_mode):
        if padding_mode in cls.PADDING_FUNCTIONS:
            return padding_mode
        else:
            message = (
                f'Padding mode "{self.padding_mode}" not valid.'
                f' Valid options are {list(self.PADDING_FUNCTIONS.keys())}'
            )
            raise KeyError(message)

    @property
    def bounds_function(self) -> Callable:
        return self.PADDING_FUNCTIONS[self.padding_mode]
