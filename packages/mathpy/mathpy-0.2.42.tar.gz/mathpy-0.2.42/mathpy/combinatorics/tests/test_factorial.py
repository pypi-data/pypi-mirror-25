from decimal import Decimal

import numpy as np

from mathpy.combinatorics.factorial import factorial, stirling, stirlingln, ramanujan, risingfactorial, fallingfactorial


def test_factorial():
    n = (1, 3, 5, 10, 20, 50)
    expected = (1, 6, 120, 3628800, 2432902008176640000,
                3.0414093201713378043612608166064768844377641568960511 * 10 ** 64)

    for i in np.arange(len(n)):
        np.testing.assert_almost_equal(factorial(n[i]), expected[i])

    np.testing.assert_equal(factorial(1.3), 1)

def test_stirling():
    n = (20, 50)
    expected = (2432902008176640000, 3.0414093201713378043612608166064768844377641568960511 * 10 ** 64)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(stirling(n[i]), expected[i], significant=2)

    np.testing.assert_approx_equal(stirling(20.2), 2432902008176640000, significant=4)
    np.testing.assert_equal(stirling(101),
                            Decimal(
                                '9425941375484441766154427626962023412731338508679429017126502107398244141692683257618988743840289379351580791761758353462970394328480399039328305880791995383808'))

def test_stirlingln():
    n = (20, 50)
    expected = (2432902008176640000, 3.0414093201713378043612608166064768844377641568960511 * 10 ** 64)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(stirlingln(n[i]), expected[i], significant=2)

    np.testing.assert_approx_equal(stirlingln(20.2), 2432902008176640000, significant=4)
    np.testing.assert_equal(stirlingln(101), Decimal('9.425947753602083039772910909E+159'))

def test_ramanujan():
    n = (5, 10, 20, 50)
    expected = (66.921730613329601, 1708821.083575075, 9.6539471162564851 * 10 ** 17, 9.6097693773772344 * 10 ** 63)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(ramanujan(n[i]), expected[i], significant=5)

    np.testing.assert_approx_equal(ramanujan(10.2), 1708821.083575075)
    np.testing.assert_equal(ramanujan(101),
                            Decimal(
                                '2499240341003369060059203655791547023073667383219135335894841710407780745990003555804972466765967094125622407449036446479870610367396703593274368075898682343424'))

def test_fallingfactorial():
    x = (3, 5, 10, 15)
    n = (2, 3, 5, 10)

    expected = (6, 60, 30240, 10897286400)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(fallingfactorial(x[i], n[i]), expected[i], significant=2)

    np.testing.assert_almost_equal(fallingfactorial(10, 5.2), 30240)
    np.testing.assert_almost_equal(fallingfactorial(10.2, 5), 30240)
    np.testing.assert_almost_equal(fallingfactorial(5, -4), 0.0083333333333333332)

    np.testing.assert_string_equal(fallingfactorial('x', -4), '1 /x*(x - 1)*(x - 2)*(x - 3)')
    np.testing.assert_string_equal(fallingfactorial('x', 2), 'x*(x - 1)')
    np.testing.assert_string_equal(fallingfactorial('a', 4), 'a*(a - 1)*(a - 2)*(a - 3)')

def test_risingfactorial():
    x = (3, 5, 10, 15)
    n = (2, 3, 5, 10)

    expected = (12, 210, 240240, 7117005772800)

    for i in np.arange(len(n)):
        np.testing.assert_approx_equal(risingfactorial(x[i], n[i]), expected[i], significant=2)

    np.testing.assert_almost_equal(risingfactorial(10, 6.2), 3603600)
    np.testing.assert_almost_equal(risingfactorial(10.2, 6), 3603600)
    np.testing.assert_almost_equal(risingfactorial(5, -4), 0.00059523809523809529)

    np.testing.assert_string_equal(risingfactorial('x', 4), 'x*(x + 1)*(x + 2)*(x + 3)')
    np.testing.assert_string_equal(risingfactorial('a', 4), 'a*(a + 1)*(a + 2)*(a + 3)')
    np.testing.assert_string_equal(risingfactorial('x', -4), '1 /x*(x + 1)*(x + 2)*(x + 3)')
