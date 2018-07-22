__author__ = 'giacomov'

from astromodels.core.tree import Node
from astromodels.core.parameter import Parameter


class Polarization(Node):

    def __init__(self, type='linear'):

        assert type in ['linear', 'stokes'], 'polarization must be linear or stokes'

        self._polarization_type = type


        Node.__init__(self, 'polarization')


    @staticmethod
    def _get_parameter_from_input(number_or_parameter, minimum, maximum, what, desc):

        # Try to transform it to float, if it works than we transform it to a parameter

        try:

            number_or_parameter = float(number_or_parameter)

        except TypeError:

            assert isinstance(number_or_parameter, Parameter), "%s must be either a number or a " \
                                                               "parameter instance" % what

            # So this is a Parameter instance already. Enforce that it has the right maximum and minimum

            parameter = number_or_parameter

            assert parameter.min_value == minimum, "%s must have a minimum of %s" % (what, minimum)
            assert parameter.max_value == maximum, "%s must have a maximum of %s" % (what, maximum)

        else:

            # This was a float. Enforce that it has a legal value

            assert minimum <= number_or_parameter <= maximum, "%s cannot have a value of %s, " \
                                                              "it must be %s <= %s <= %s" % (what, number_or_parameter,
                                                                                             minimum, what, maximum)

            parameter = Parameter(what, number_or_parameter,
                                  desc=desc, min_value=minimum, max_value=maximum, unit='deg', free=False)

        return parameter


class LinearPolarization(Polarization):

    def __init__(self, degree, angle):
        """
        Linear parameterization of polarization

        :param degree: The polarization degree
        :param angle: The polarization angle
        """
        super(LinearPolarization, self).__init__(type='linear')

        degree = self._get_parameter_from_input(degree, 0, 100, 'degree', 'Polarization degree')

        angle = self._get_parameter_from_input(angle, 0, 180, 'angle', 'Polarization angle')

        self._add_child(degree)
        self._add_child(angle)


class StokesPolarization(Polarization):

    def __init__(self, I, Q, U, V):
        """
        Stokes parameterization of polarization

        :param I:
        :param Q:
        :param U:
        :param V:
        """
        super(StokesPolarization, self).__init__(type='stokes')

        # get the parameters set up

        I = self._get_parameter_from_input(I, 0, 1, 'I', 'Stokes I')
        Q = self._get_parameter_from_input(Q, 0, 1, 'Q', 'Stokes Q')
        U = self._get_parameter_from_input(U, 0, 1, 'U', 'Stokes U')
        V = self._get_parameter_from_input(V, 0, 1, 'V', 'Stokes V')

        # add the children

        self._add_child(I)
        self._add_child(Q)
        self._add_child(U)
        self._add_child(V)


