"""
Produce an optimal partition by solving an integer linear program (ILP).

Programmer: Erel Segal-Halevi, Eitan Lichtman
Since: 2022-02

Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
"""

from typing import List, Callable, Any
from numbers import Number
from prtpy import objectives as obj, outputtypes as out, Binner, printbins
from math import inf

import mip


def optimal(
    binner: Binner, numbins: int, items: List[any], relative_values: List[any] = None,
    copies=1,
    time_limit=inf,
    verbose=0
):
    """
    Produce a partition that minimizes the given objective, by solving an integer linear program (ILP).

    :param numbins: number of bins.
    :param items: list of items.
    :param valueof: a function that maps an item from the list `items` to a number representing its value.
    :param copies: how many copies there are of each item. Default: 1.
    :param time_limit: stop the computation after this number of seconds have passed.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums
    >>> optimal(BinnerKeepingSums(), 2, [11.1,11,11,11,22],[0.1,0.9])
    array([11. , 55.1])
    >>> optimal(BinnerKeepingSums(), 2, [11,11,11,11,22])
    array([33., 33.])

    >>> optimal(BinnerKeepingSums(), 5, [2,2,5,5,5,5,9])
    array([5., 5., 7., 7., 9.])
    >>> optimal(BinnerKeepingSums(), 3, [1,1,1,1])
    array([1., 1., 2.])
    >>> optimal(BinnerKeepingSums(), 3, [1,1,1,1,1])
    array([1., 2., 2.])

    The following examples are based on:
        Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.
    >>> walter_numbers = [46, 39, 27, 26, 16, 13, 10]
    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers))
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0

    >>> printbins(optimal(BinnerKeepingContents(), 3, walter_numbers))
    Bin #0: [39, 16], sum=55.0
    Bin #1: [46, 13], sum=59.0
    Bin #2: [27, 26, 10], sum=63.0

    >>> optimal(BinnerKeepingSums(), 3, walter_numbers)
    array([55., 59., 63.])



    """
    ibins = range(numbins)
    items = list(items)
    iitems = range(len(items))
    if isinstance(copies, Number):
        copies = {iitem: copies for iitem in iitems}

    model = mip.Model("partition")
    counts: dict = {
        iitem: [model.add_var(var_type=mip.INTEGER) for ibin in ibins]
        for iitem in iitems
    }  # counts[i][j] is a variable that represents how many times item i appears in bin j.

    bin_sums = [
        sum([counts[iitem][ibin] * binner.valueof(items[iitem]) for iitem in iitems])
        for ibin in ibins
    ]

    if relative_values:
        z_js = [
            bin_sums[ibin] - sum(items) * relative_values[ibin]
            for ibin in ibins
        ]
    else:
        z_js = [
            bin_sums[ibin] - sum(items) / len(ibins)
            for ibin in ibins
        ]

    t_js = [
        model.add_var(var_type=mip.INTEGER) for ibin in ibins
    ]


    model.objective = mip.minimize(
        0.5 * sum(t_js)
    )

    # Construct the list of constraints:
    t_js_greater_than_z_js = [t_js[ibin] >= z_js[ibin] for ibin in ibins]
    t_js_greater_than_minus_z_js = [t_js[ibin] >= -z_js[ibin] for ibin in ibins]
    counts_are_non_negative = [counts[iitem][ibin] >= 0 for ibin in ibins for iitem in iitems]
    each_item_in_one_bin = [
        sum([counts[iitem][ibin] for ibin in ibins]) == copies[iitem] for iitem in iitems
    ]
    constraints = t_js_greater_than_z_js + t_js_greater_than_minus_z_js + counts_are_non_negative + each_item_in_one_bin
    for constraint in constraints: model += constraint

    # Solve the ILP:
    model.verbose = verbose
    status = model.optimize(max_seconds=time_limit)
    if status != mip.OptimizationStatus.OPTIMAL:
        raise ValueError(f"Problem status is not optimal - it is {status}.")

    # Construct the output:
    output = binner.new_bins(numbins)
    for ibin in ibins:
        for iitem in iitems:
            count_item_in_bin = int(counts[iitem][ibin].x)
            for _ in range(count_item_in_bin):
                binner.add_item_to_bin(output, items[iitem], ibin)
    binner.sort_by_ascending_sum(output)
    return output


if __name__ == "__main__":
    import doctest, logging
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} tests".format(failures, tests))


    import pandas as pd

    df = pd.read_csv('tables.csv')

    numbins = 0
    relative_values = []
    values = []
    for i in range (len(df.values)):
        if (str(df.values[i][11]) != "nan"):
            numbins = numbins + 1
            relative_values.append(float((df.values[i][11])[:-1]))

    for i in range(len(df.values)):
        values.append(int(df.values[i][3].replace(',', '')))
    import time
    start = time.time()

    from prtpy import BinnerKeepingContents, BinnerKeepingSums
    printbins(optimal(BinnerKeepingSums(), numbins, values, relative_values))

    end = time.time()
    print(end - start)
