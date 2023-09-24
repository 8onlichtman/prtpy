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
import mosek
import mip
import gurobipy

def optimal(
    binner: Binner, numbins: int, items: List[any], relative_values: List[any] = None,
    copies=1,
    time_limit=inf,
    verbose=0,
    solver_name = mip.GRB,  # passed to MIP. See https://docs.python-mip.com/en/latest/quickstart.html#creating-models
    model_filename = None,
    solution_filename = None,
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
    >>> optimal(BinnerKeepingSums(), 2, [11.1,11,11,11,22],[0.9,0.1])
    array([55.1, 11. ])
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

    >>> from prtpy import partition
    >>> partition(algorithm=optimal, numbins=3, items=[1, 2, 3], copies=[2, 1, 4])
    [[2, 3], [1, 1, 3], [3, 3]]

    """
    ibins = range(numbins)
    items = list(items)
    iitems = range(len(items))
    if isinstance(copies, Number):
        copies = {iitem: copies for iitem in iitems}
    model = mip.Model(name = '', solver_name=solver_name)
    counts: dict = {
        iitem: [model.add_var(var_type=mip.INTEGER) for ibin in ibins]
        for iitem in iitems
    }  # counts[i][j] is a variable that represents how many times item i appears in bin j.

    bin_sums = [
        sum([counts[iitem][ibin] * binner.valueof(items[iitem]) for iitem in iitems])
        for ibin in ibins
    ]

    sum_items = 0
    if not copies:
        sum_items = sum(items)
    else:
        for i in range (len(items)):
            sum_items = sum_items + items[i] * copies[i]

    if relative_values:
        z_js = [
            bin_sums[ibin] - sum_items * relative_values[ibin]
            for ibin in ibins
        ]
    else:
        z_js = [
            bin_sums[ibin] - sum_items / len(ibins)
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
    constraints = each_item_in_one_bin + t_js_greater_than_z_js + t_js_greater_than_minus_z_js + counts_are_non_negative
    for constraint in constraints: model += constraint

    # Solve the ILP:
    model.lp_method = verbose
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
    if not relative_values:
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
            relative_values.append(float((df.values[i][11])[:-1])/100)
            #relative_values.append(round(float((df.values[i][11])[:-1]) / 100, 4))

    for i in range(len(df.values)):
        values.append(int(df.values[i][3].replace(',', '')))
    import time
    start = time.time()

    print(len(df.values))
    print(len(values))
    print(numbins)
    print(values)
    print(sum(values))
    print(relative_values)

    import numpy as np, numpy.random

    rv = np.random.dirichlet(np.ones(5), size=1).tolist()
    new_rv = [round(elem, 4) for elem in rv[0]]
    print(rv[0])
    print(sum(rv[0]))
    print(new_rv)



    count_values = dict()
    for num in values:
        count_values.setdefault(num, 0)
        count_values[num] += 1
    print(count_values)

    items = list()
    copies = list()
    for key in count_values.keys():
        items.append(key)
        copies.append(count_values[key])

    print(items)
    print(copies)
    print(len(items))
    print(len(copies))


    from prtpy import BinnerKeepingContents, BinnerKeepingSums
    printbins(optimal(BinnerKeepingContents(), numbins, items=items, relative_values=relative_values, copies=copies))


    '''sum_bins = optimal(BinnerKeepingSums(), numbins, items=items, relative_values= relative_values, copies=copies)
    print(sum(sum_bins))
    print(sum_bins)
    dist_from_avg = 0
    for i in range (len(sum_bins)):
        dist_from_avg = dist_from_avg + max(0, (sum_bins[i] - sum(sum_bins) * relative_values[i]))
    print(dist_from_avg)'''


    end = time.time()
    print(end - start);
