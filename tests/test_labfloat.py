import pytest
import numpy
import itertools
from math import sqrt
import labfis

dx = 1e-10


def labfloat_iterative(vardic, exp):
    resulterror = 0

    for var in vardic.keys():
        exec(var + "=" + "{0:.16f}".format(vardic[var][0]))

    for var in vardic.keys():
        var_value = vardic[var][0]
        var_error = vardic[var][1]

        exec(var + "=" + "{0:.16f}".format(var_value) +
             "+" + "{0:.16f}".format(dx))
        dph = eval(exp)

        exec(var + "=" + "{0:.16f}".format(var_value))
        dpn = eval(exp)

        derivative = (dph - dpn)/dx
        resulterror += (derivative * var_error) ** 2
    return sqrt(resulterror)


def labfloat_calc(vardic, exp):
    for var in vardic.keys():
        exec(var + "=" +
             "labfis.labfloat({0:.16f},{1:.16f})".format(*vardic[var]))
    result = eval(exp)
    return result.uncertainty


rng = numpy.random.default_rng()

operations = ["*", "/", "+", "-", "**"]

vals = {
    "a": (rng.random(), rng.random()),
    "b": (rng.random(), rng.random()),
    "c": (rng.random(), rng.random()),
    "d": (rng.random(), rng.random()),
    "e": (rng.random(), rng.random())
}


def test_labfloat_expressions():
    print(vals)
    var = list(vals.keys())
    opers = itertools.combinations_with_replacement(operations, len(var)-1)
    for exp in opers:
        expression = ""
        for i in range(len(exp)):
            if i == len(exp)-1:
                expression += var[i]+exp[i]+var[i+1]
            else:
                expression += var[i]+exp[i]

        result1 = labfloat_iterative(vals, expression)
        result2 = labfloat_calc(vals, expression)

        print(expression)
        print(result1, result2)
        print(round(result1), round(result2))

        assert round(result2) == round(result1)
