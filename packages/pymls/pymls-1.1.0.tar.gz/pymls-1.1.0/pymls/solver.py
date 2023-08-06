#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# solver.py
#
# This file is part of pymls, a software distributed under the MIT license.
# For any question, please contact one of the authors cited below.
#
# Copyright (c) 2017
# 	Olivier Dazel <olivier.dazel@univ-lemans.fr>
# 	Mathieu Gaborit <gaborit@kth.se>
# 	Peter Göransson <pege@kth.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

import numpy as np
from numpy.lib.scimath import sqrt

from pymls.analysis import Analysis
from pymls.interface.utils import generic_interface
from pymls.layers import generic_layer
import pymls.backing as backing
from pymls.media import Air


class IncompleteDefinitionError(Exception):

    def __init__(self, msg='The definition is incomplete and no analysis can be performed'):
        super().__init__(msg)


class Solver(object):
    """
    Stores a system to solve and parameters for the analysis.
    Performs analysis and gives back raw unmodified/cleaned results.

    All post-processing should be done *out* of this class
    """

    def __init__(self, media=None, analyses=None, layers=None, backing=None):
        self.media = media if media is not None else []
        self.layers = layers if layers is not None else []
        self.backing = backing
        if type(analyses) == Analysis:
            self.analyses = [analyses]
        elif type(analyses) == list:
            self.analyses = analyses
        else:
            self.analyses = []

        self.resultset = []

    def check_is_complete(self):
        """ Checks that all the required data has been provided. """
        # not empty layer list
        if not self.layers:
            raise IncompleteDefinitionError("Empty layer list")

        # if media are missing, grab them from the layers list
        missing_media = {l.medium for l in self.layers} - set(self.media)
        self.media += list(missing_media)

        if not self.backing in [backing.transmission, backing.rigid]:
            raise IncompleteDefinitionError('No backing provided')

        return True

    def solve(self, frequencies=None, angles=0):
        self.check_is_complete()

        if frequencies is not None:
            self.analyses.append(Analysis('auto', frequencies, angles))

        for a in self.analyses:
            result = {
                'name': a.name,
                'f': [],
                'angle': [],
                'R': [],
                'T': [],
            }
            for f, angle in a:
                (R, T) = self.__solve_one_frequency(f, angle)
                result['f'].append(f)
                result['angle'].append(angle)
                result['R'].append(R)
                if T is not None:
                    result['T'].append(T)
            self.resultset.append(result)

        return self.resultset

    def __solve_one_frequency(self, frequency, theta_inc):

        omega = frequency*2*np.pi

        for m in self.media:
            m.update_frequency(omega)

        # compute k_x
        k_x = omega/Air.c*np.sin(theta_inc*np.pi/180)

        # load the backing vector to initiate recursion
        Omega_plus = self.backing(omega, k_x)

        # goes backward (from last to first layer) and compute successive
        # Omega_plus/minus
        back_prop = np.eye(1)
        for invertedi_L, L in enumerate(self.layers[::-1]):

            i_L = len(self.layers)-invertedi_L-1

            if invertedi_L == 0:  # right-most layer
                interface_func = generic_interface(L.medium, Air)
            else:
                interface_func = generic_interface(
                    L.medium,
                    self.layers[i_L+1].medium
                )

            if interface_func is not None:
                (Omega_moins, tau) = interface_func(Omega_plus)
            else:
                Omega_moins = Omega_plus
                tau = np.eye(len(Omega_moins))

            layer_func = generic_layer(L.medium)
            (Omega_plus, xi) = layer_func(Omega_moins, omega, k_x, L.medium, L.thickness)

            if self.backing == backing.transmission:
                back_prop = back_prop.dot(tau).dot(xi)

        # last interface
        interface_func = generic_interface(Air, self.layers[0].medium)
        if interface_func is not None:
            (Omega_moins, tau) = interface_func(Omega_plus)

        else:
            Omega_moins = Omega_plus
            tau = np.eye(len(Omega_moins))

        if self.backing == backing.transmission:
            back_prop = back_prop.dot(tau)

        # Solve for the first layer
        k_air = omega*sqrt(Air.rho/Air.K)
        k_z = sqrt(k_air**2-k_x**2)
        u_z = 1j*k_z/(Air.rho*omega**2)

        Omega_0_fluid = np.matrix([
            [-u_z],
            [-1]
        ])
        S_fluid = np.matrix([
            [-u_z],
            [1]
        ])

        temp = np.array([
            [Omega_moins[0,0], Omega_0_fluid[0,0]],
            [Omega_moins[1,0], Omega_0_fluid[1,0]]
        ])
        X = np.linalg.inv(temp).dot(S_fluid)

        reflx_coefficient = X[1,0]
        X_0_moins = X[0,0]

        if self.backing == backing.transmission:
            trans_coefficient = back_prop*X_0_moins
            trans_coefficient = trans_coefficient[0,0]
        else:
            trans_coefficient = None

        return (reflx_coefficient, trans_coefficient)
