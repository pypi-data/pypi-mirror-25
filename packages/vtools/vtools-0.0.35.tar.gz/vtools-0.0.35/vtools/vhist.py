""" the vhist module contains the definition of the vHist class. vHist is a class to
simplify the display of different kind of histograms. Meant to be used in conjunction
with the vImg class. By adding a single 3-tuple bool parameter (RGB) to indicate which
channels are active in the histogram, we can automatically calculate what type of histogram
to show information for. Therefore, initialization and show functionality may be standardized.
"""


import numpy as np
from matplotlib import pyplot as plt
# from typing import Tuple
# from .types import color_type, nd_or_none
# from itertools import compress
# from .vtools import eprint


####################################################################################################
######################################### Histogram Class ##########################################

class vHist(np.ndarray):
    """ vHist is a class to simplify the display of different kind of histograms. Meant to be used in conjunction
    with the vImg class. By adding a single 3-tuple bool parameter (RGB) to indicate which channels are active
    in the histogram, we can automatically calculate what type of histogram to show information for. Therefore,
    initialization and show functionality may be standardized.


    hist   : This is the image that we want to compute a histogram for. Wrap it as a list: [vHists] .
    channels : A list of indexes, where we specify the index of the channel we want to compute a histogram for.
               To compute a histogram of a grayscale image, the list would be [0] . To compute a histogram for all
               three red, green, and blue channels, the channels list would be [0, 1, 2] .
    mask     : Remember learning about masks in Section 1.4.8? Well, here we can supply a mask. If a mask is
               provided, a histogram will be computed for masked pixels only. If we do not have a mask or do not
               want to apply one, we can just provide a value  of None .
    histSize : This is the number of bins we want to use when computing a histogram. Again, this is a list, one
               for each channel we are computing a histogram for. The bin sizes do not all have to be the same.
               Here is an example of 32 bins for each channel: [32, 32, 32] .
    ranges   : The range of possible pixel values. Normally, this is [0, 256] (this is not a typo — the ending
               range of the cv2.calcHist  function is non-inclusive so you’ll want to provide a value of 256 rather
than 255) for each channel, but if you are using a color space other than RGB [such as HSV],
               the ranges might be different.)
    """

    _cDict = {'b': 'Blue', 'g': 'Green', 'r': 'Red',
              'L': 'Luminance', 'A': 'Alpha', 'B': 'Beta',
              'h': 'Hue', 's': 'Saturation', 'v': 'Value', 'k': 'Grayscale'}

    ####################################################################################################
    ####################################### vHist Dunder Methods #######################################

    def __new__(cls, hist, img_name: str, color_space: str = 'BGR', hist_type: str = '1D',
                channels=(False,) * 3):
        # Init assert statements. Make sure basic class parameter requirements are met.

        assert type is not None, "None check failed for type parameter."

        assert len(channels) == 3 and isinstance(channels, tuple), "Must provide a 3-tuple with True or False " \
            "elements for each value. True if that channel is included in calculated histogram, False if not."
        # Here is the meat for subclassed numpy ndarray types, this casts a new instance of
        # the passed parameter hist.
        assert issubclass(type(hist), np.ndarray), "[-] Error: hist must be subclass of ndarray."
        obj = np.asarray(hist).view(cls)
        obj.__image_name = img_name
        obj.__color_space = color_space
        obj.__type = hist_type
        obj.__channels = channels

        return obj

    # classmethod for alternative creation (beta)
    @classmethod
    def fromMultiHist(cls):
        # to be implemented later
        pass

    def __array_finalize__(self, obj):
        """ this is where we initialize most of the variables for the vHist class, due to the way
            numpy n-dimensional arrays work.
        """
        if obj is None: return
        self.__image_name = getattr(obj, '__image_name', None)
        self.__type = getattr(obj, '__type', None)
        self.__channels = getattr(obj, '__channels', (False, False, False))
        active_chans = sum(1 for e in self.channels if e is True)
        self.xlimit = (0, self.shape[0])
        self.shown = False

    def __array_wrap__(self, out_arr, context=None):
        """__array_wrap__ gets called at the end of numpy ufuncs and
        other numpy functions, to allow a subclass to set the type of
        the return value and update attributes and metadata"""
        out_arr.__image_name = self.__image_name
        out_arr.__type = self.type
        out_arr.__channels = self.channels
        out_arr.__image_name = self.image_name
        out_arr._multi = self._multi
        out_arr.shown = self.shown

        return np.ndarray.__array_wrap__(self, out_arr, context)

    def __eq__(self, other):
        return True if np.array_equal(self, other) else False

    def __truediv__(self, other):
        return super().__truediv__(self, other).view(vHist)

    ####################################################################################################
    ######################################### vHist Properties #########################################

    @property
    def image_name(self):
        return self.__image_name

    @image_name.setter
    def image_name(self, img_name: str):
        self.__image_name = img_name

    @property
    def channels(self):
        return self.__channels

    @channels.setter
    def channels(self, chans):
        if issubclass(type(chans), tuple) and len(chans) == 3 and all(type(e) == bool for e in chans):
            self.__channels = chans
        else:
            raise ValueError(f"[-] Fatal Error: Expected 3-tuple of bools, got ({type(chans)}).")

    @property
    def color_space(self):
        return self.__color_space

    @color_space.setter
    def color_space(self, cspace: str):
        cspace = cspace.upper()
        if cspace == 'RGB':
            self.__color_space = cspace[::-1]
        elif cspace in ('BGR', 'HSV', 'LAB'):
            self.__color_space = cspace
        else:
            raise ValueError(f"[-] Fatal Error: Expected 'RGB', 'BGR', 'HSV', or 'LAB' (case insensitive)")

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, str_type: str):
        str_type = str_type.upper()
        TYPES = ('1D', '2D', '3D')
        if str_type in TYPES:
            self.__type = str_type
        else:
            raise ValueError(f"[-] Fatal Error: Expected '1D', '2D', or '3D', got {str_type}.")

    @property
    def bins(self):
        return self.shape[0]

    @property
    def xlimit(self):
        return self.__xlimit

    @xlimit.setter
    def xlimit(self, x_limit):
        if all(type(e) == int for e in x_limit):
            self.__xlimit = x_limit
        else:
            raise ValueError(f"[-] Fatal Error: x_limit argument must be an iterable made up of only int")

    ####################################################################################################
    ###################################### vHist Display Methods #######################################

    def show(self, title='', append: tuple = tuple(), x_title: str = '', y_title: str = '', legend: bool = True):
        """ The show method of the vHist class invokes the display (using matplotlib) of the histogram it
        represents. Since we handle black and white, RGB histograms, HSV histograms, and two dimensional
        color bar histograms, the function must use the type and color_space properties in order to determine
        the type of display to use. By default, flat histograms use a line plot and 2-D histograms use a
        colorbar plot.

        :param title   :
        :param append  :
        :param x_title :
        :param y_title :
        :return:
        """

        # Check if hist was shown before, if so, proceed with same arguments
        if self.shown is True:
            title, append, x_title, y_title, legend = self._show_cache
        else:
            # Create a cache of the first provided parameters to show function so you can repeat previous views easily
            self._show_cache = (title, append, x_title, y_title, legend)

        self._multi = len(append) > 0

        # If attempting to show a three dimensional histogram
        if self.type == '3D':
            # Print an error and return
            raise ValueError("[-] Error: 3D Histogram has no current visualization method.")

        # Determine color from self.color_space
        color_space = self.color_space.lower() if self.color_space != 'LAB' else 'LAB'

        # color_dict is used to quickly determine which color channel corresponds with the appended data
        # from vImg.histogram(display=True)
        color_dict = {
                      (True, True, True): color_space,
                      (True, True, False): color_space[:3],
                      (True, False, True): color_space[::2],
                      (True, False, False): color_space[0],
                      (False, True, True): color_space[1:],
                      (False, True, False): color_space[1],
                      (False, False, True): color_space[2],
                      (False, False, False): 'k'
        }

        # If the histogram is flattened (or '1D' as used here) we need to create a line graph histogram
        if self.type == '1D':
            if not self._multi:
                # Flat grayscale display code:
                fig, ax = plt.subplots()
                fig.suptitle(title)
                ax.set_xlabel(x_title)
                ax.set_ylabel(y_title)
                ax.set_xlim(self.xlimit)
                color = color_dict[self.channels][0]
                ax.plot(self, color, label=f"{self._cDict[color]} channel")
            else:
                # Flat color histogram at least one channel
                fig, ax = plt.subplots()
                fig.suptitle(title)
                ax.set_xlabel(x_title)
                ax.set_ylabel(y_title)
                color = color_dict[self.channels][0]
                ax.plot(self, color, label=f"{self._cDict[color]} channel")
                max_bin = self.bins
                for add_clr, add_hist in append:
                    ax.plot(add_hist, add_clr, label=f"{self._cDict[add_clr]} channel")
                    if add_hist.shape[0] > max_bin:
                        max_bin = add_hist.shape[0]
                ax.set_xlim(self.xlimit)

            if legend:
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles, labels)

        if self.type == '2D':
            pass

        self.shown = True

