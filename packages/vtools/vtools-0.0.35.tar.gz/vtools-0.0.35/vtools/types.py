from typing import Union, List, Tuple, NewType
from numpy import ndarray
from .vcontours import vContour, vContours
from .colors import vColor
# from .vimg import vImg

# contour_list_type will accept either lists of type ndarray or vcontour,
# as well as vContours (which is a list subclass)
contour_list_type = Union[List[Union[List[ndarray], vContour]], vContours]

# color_type will accept either Tuples of three integers or a vColor class object
color_type = Union[Tuple[int], vColor]

# check_odd is a type pertaining to the vImg private class _isOdd that handles
# cases when the user incorrectly passes an even number for a value of k
check_odd = Union[Tuple[int, int], int]

# Checks if type numpy.ndarray or None
nd_or_none = Union[ndarray, None]

# Checks if type tuple or None
tuple_or_none = Union[tuple, None]

# Checks if type tuple[int] or None
intuple_or_none = Union[Tuple[int], None]

# Checks if image type (numpy.ndarray or vImg)
# image_type = Union[ndarray, vImg]

# Checks if variable is of type string or None
str_or_none = Union[str, None]
