from typing import List
from prtpy import Binner, BinsArray



def Cached_Iterative_Weakening (binner: Binner, k: int, S: List[any], m: int) -> BinsArray:
    """
    "Cached Iterative Weakening for Optimal Multi-Way Number Partitioning", by Ethan L. Schreiber and Richard E. Korf (2014), https://ojs.aaai.org/index.php/AAAI/article/view/9122/8981
    "Cached Iterative Weakening" algorithm finds a partition of the numbers from S into k bins in which the largest sum is minimal.
    programmers: Eitan Lichtman and Shilo Ben Natan.

    >>> from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins
    >>> printbins(Cached_Iterative_Weakening(BinnerKeepingContents(), 3, [127, 125, 122, 105, 87, 75, 68, 64, 30, 22],6))
    Bin #0: [125, 64, 22], sum=211.0
    Bin #1: [127, 75], sum=202.0
    Bin #2: [122, 87], sum=209.0
    Bin #3: [105, 68, 30], sum=203.0



    """
    return {}


def Tree_search (card: int, current_allocation: List[any], S: List[any]):
    return 0