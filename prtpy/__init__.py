import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()

import prtpy.outputtypes as out
import prtpy.objectives as obj
from prtpy.bins import Bins, BinsKeepingContents, BinsKeepingSums

from prtpy.packing import pack
from prtpy.partitioning import partition



class partitioning:
    from prtpy.partitioning.complete_greedy import anytime as cg
    from prtpy.partitioning.complete_greedy import anytime as complete_greedy

    from prtpy.partitioning.dp import optimal as dp
    from prtpy.partitioning.dp import optimal as dynamic_programming

    from prtpy.partitioning.ilp import optimal as ilp
    from prtpy.partitioning.ilp import optimal as integer_programming

    from prtpy.partitioning.greedy import greedy
    from prtpy.partitioning.greedy import greedy as lpt
    from prtpy.partitioning.greedy import greedy as longest_processing_time

    from prtpy.partitioning.roundrobin import roundrobin
    from prtpy.partitioning.multifit import multifit as multifit

    # Samuel & Jonathan modules
    from prtpy.partitioning.kk_sy import kk as kk_sy
    from prtpy.partitioning.ckk_sy import best_ckk_partition as ckk_sy
    from prtpy.partitioning.snp import snp

    # Eli Belkind module
    from prtpy.partitioning.cbldm import cbldm

    # Kfir Goldfarb modules
    from prtpy.partitioning.kk import kk
    from prtpy.partitioning.ckk import ckk
    from prtpy.partitioning.rnp import rnp
    from prtpy.partitioning.irnp import irnp

partitioning.complete_greedy.__name__ = "complete-greedy"
partitioning.ilp.__name__ = "integer-programming"
partitioning.dp.__name__ = "dynamic-programming"
partitioning.kk.__name__ = "karmarkar-karp"
partitioning.ckk.__name__ = "complete-karmarkar-karp"
partitioning.kk_sy.__name__ = "karmarkar-karp-sy"
partitioning.ckk_sy.__name__ = "complete-karmarkar-karp-sy"
partitioning.rnp.__name__ = "recursive-number-partitioning"
partitioning.irnp.__name__ = "improved-recursive-number-partitioning"
partitioning.snp.__name__ = "sequential-number-partitioning"

class packing:
    from prtpy.packing.first_fit import online as first_fit, decreasing as first_fit_decreasing
    from prtpy.packing.first_fit import online as ff, decreasing as ffd


class covering:
    from prtpy.packing.greedy_covering import decreasing as decreasing
    from prtpy.packing.cflz_covering import twothirds as twothirds
    from prtpy.packing.cflz_covering import threequarters as threequarters

# class exact:  # Algorithms that return the exact optimal partition
#     from prtpy.complete_greedy import optimal as cg
#     from prtpy.complete_greedy import optimal as complete_greedy
#     from prtpy.dp import optimal as dp
#     from prtpy.dp import optimal as dynamic_programming
#     from prtpy.ilp import optimal as ilp
#     from prtpy.ilp import optimal as integer_programming


# class approx:  # Algorithms that return an approximately-optimal partition
#     from prtpy.greedy import greedy
#     from prtpy.first_fit import online as first_fit, decreasing as first_fit_decreasing
#     from prtpy.first_fit import online as ff, decreasing as ffd
