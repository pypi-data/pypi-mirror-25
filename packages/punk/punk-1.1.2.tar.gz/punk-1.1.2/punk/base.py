from abc import ABC, abstractmethod


class PrimitiveBase(ABC):
    """
    A base class for all TA1 primitives.
    """


class DataCleaningPrimitiveBase(PrimitiveBase):
    
    def __init__(self):
        """ Initializes the featurization primitive.
        All primitives should specify all the hyper-parameters that can be set 
        at the class level in their ``__init__`` as explicit keyword arguments 
        (no ``*args`` or ``**kwargs``). Available hyper-parameters should be 
        specified in primitive’s D3M annotation.
        """
        self._out_type = None

    @property
    def out_type(self):
        """ This definition of this object allows the primitive to define and
        return an arbitrary structure, which is essential for primitives that
        are augmenting, transforming, and annotating data.

        Returns
        -------
        {
            'type': 'dict',
            'definition': {
                'my_property_1': {
                    'type': 'dict',
                    'my_sub_property_1': {
                        'type': 'label[]'
                    }
                }
            }
        }

        Defines a data structure such as: 

        {
            'my_property_1': {
                'my_sub_property_1': ['a','b','c']
            }
        }

        When the primitive returns a matrix, the keys refer to column positions.
        For example:

        {
            'type': 'matrix',
            'definition': {
                0: {
                    'type': 'label[]'
                },
                1: {
                    'type': 'dict[]',
                    'my_sub_property_1': {
                        'type': 'integer'
                    }
                }
            }
        }

        This would define a data structure such as:

        [
            [
                'a',
                'b',
                'c'
            ],
            [
                {'my_sub_property_1': 1},
                {'my_sub_property_1': 2},
                {'my_sub_property_1': 3}
            ]
        ]

        All sub property definition should conform to the allowed `fit` model
        intype.
        """
        return self._out_type


    @abstractmethod
    def fit(self, intype, data):
        """ Takes input data of the specified type and performs any computation
        required for transformation.

        Parameters
        ----------
        intype : array-like
            A matrix specifying the format of the input data.

            Possible intype formats are:
            "float" : float

            "integer" : integer

            "text" : str
                Document (longer text)

            "label" : string
                1-2 word category label

            "dateTime" : datetime or str
                Python datetime object, or dateTime-formatted string

            "location" : str
                Represents a real-world location

            "coordinatePair" : str
                Latitude, longitude pair, e.g. "10.27,-30.45"

            "matrix" : array-like
                Numpy.ndarray or list.

            "dataset": array-like
                Tabular data structure, where the first row is a list of
                column headers

            Each primitive should specify applicable input data formats in its
            documentation and primitive annotation. The intype property can be
            arbitrarily complex, including nested structures. 
            For example: 

            ["matrix, [""label", "dateTime", ["float","float"]]]

            Would correspond to the structure:

            [
                ["green", "2017-01-01", [1.25,3.5]],
                ["blue", "2017-02-01", [3.25,5.5]]
            ]

        data : array-like
            The input in the specified format. 
        """


    @abstractmethod
    def transform(self, data=None):
        """ Performs the transformation and returns the transformed data.

        Parameters
        ----------
        data : array-like
            optional argument, used in cases where the original input data was
            used to train model, and transformation will now be performed on a
            new set of data

        Returns
        -------
        transformed_data : array-like
        """


    def staged_fit(self, intype, data):
        """ An iterative version of ``fit`` which yields at each internal
        iteration, for example, after every batch of training. This allows
        incremental monitoring and evaluation of the training process. When a
        fit generator yields, it should be possible to call methods on the
        instance and operate on current state of the model (at the time of
        yielding), including pickling the instance.
        """
        yield self.fit(self, intype, data)


    def staged_transform(self, data=None):
        """ An iterative version of ``transform`` which yields at each internal
        iteration. At every iteration, returned value should be of the same shape
        as the return value for ``transform``, but some elements might be
        missing.
        """
        yield self.transform(data=data)
