import heapq
from pickle import TRUE
from typing import List
from prtpy import Binner, BinsArray, BinnerKeepingContents

from ESS import ESS
from Horowitz_And_Sahni import Horowitz_Sahni
from karmarkar_karp_sy import kk


class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

cardinality = []

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
    S.sort(reverse=TRUE)
    ub = int(sum(S) / k)
    solution = kk(BinnerKeepingContents(), k, S)
    maximum = max(binner.sums(kk(BinnerKeepingContents(), k, S)))
    minimum = sum(S) - (k-1)*(maximum-1)
    while (solution > ub):
        counter = 0
        min_heap = []
        heapq.heapify(min_heap)
        max_heap = []
        heapq.heapify(max_heap)
        while True:
            next_sum = minimum
            next = ESS(S,next_sum,maximum) #ESS returns the smallest subset between next_sum and maximum
            if next is None:
                break
            next_sum = sum(next.__iter__())
            if next_sum < ub:
                min_heap.add(next_sum)
            if next_sum >= ub:
                max_heap.add(next_sum)
                counter = counter+1
            if counter == m:
                break
        maximum = max(max_heap)
        minimum = sum(S) - (k - 1) * maximum
        while True:
            next = ESS(S, next_sum, maximum)  # ESS returns the smallest subset between next_sum and maximum
            if next is None:
                break
            next_sum = sum(next.__iter__())
            max_heap.add(next_sum)
            max_heap.pop(maximum)
            maximum = max(max_heap)
            minimum = sum(S) - (k - 1) * maximum
        subset_sums= list(max_heap)
        for subset_sum in subset_sums:
            S_1 = Horowitz_Sahni(S, subset_sum)       # Find the subset that matches the sum
            ub = sum(S_1)
            lb = sum(S) - (k-1) * ub
            for subset_sum2 in subset_sums:
                S_2 = Horowitz_Sahni(S, subset_sum2)
                if (sum(S_2) >= lb and sum(S_2) <= ub):
                    current = cardinality[len(S_2)]
                    for i in range (len(S)):
                        if current.data is None:
                            current.data = S[i]
                        if S[i] in S_2:
                            current = current.left
                        else:
                            current = current.right
                    Tree_search(S,{S_1},cardinality,1)
        m = 2*m


    return {}


def Tree_search (S: List[int], current_allocation: List[any],cardinality:List[Tree], card: int):
    union = {}
    for i in range (len(current_allocation)):
        for j in range (len(current_allocation[i])):
            union.add = current_allocation[i][j]
    union.sort(reverse=TRUE)
    is_full_allocation = True
    if len(S) == len(union):
        for i in range (len(S)):
            if S[i] != union[i]:
                is_full_allocation = False
        if is_full_allocation == True:
            return current_allocation
    S_R = {}
    counter = 0
    for i in range (len(S)):
        


    if cardinality[card] != None:


    return 0

if __name__ == '__main__':
    Cached_Iterative_Weakening(BinnerKeepingContents(), 3, [127, 125, 122, 105, 87, 75, 68, 64, 30, 22], 6)
