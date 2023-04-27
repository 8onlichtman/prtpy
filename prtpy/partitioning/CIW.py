import heapq
from heapq import heappush
from typing import List
from prtpy import Binner, BinsArray, BinnerKeepingContents
import logging

from ESS import ESS
from Horowitz_And_Sahni import Horowitz_Sahni
from karmarkar_karp_sy import kk

class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


def Tree_insert(node: Tree, S: list, S_2: list) -> Tree:
    if not S:
        return node
    if node is None:
        node = Tree
        node.data = S[0]
    if S[0] in S_2:
        S.pop(0)
        node.left = Tree
        return Tree_insert(node.left, S, S_2)
    else:
        S.pop(0)
        node.right = Tree
        return Tree_insert(node.right, S, S_2)




def Cached_Iterative_Weakening(binner: Binner, k: int, S: List[any], m: int) -> BinsArray:
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
    S.sort(reverse=True)
    ub = int(sum(S) / k)
    logging.debug("ub = %d ", ub)
    maximum = list(kk(BinnerKeepingContents(), k, S))
    maximum = int(maximum[0][len(maximum[0])-1])
    minimum = sum(S) - (k - 1) * (maximum - 1)
    logging.debug("maximum = %d, minimum = %d", maximum, minimum)
    while maximum > ub:
        counter = 0
        min_heap = []
        heapq.heapify(min_heap)
        max_heap = []
        heapq.heapify(max_heap)                  #We will use minus to make it a max heap
        cardinality_tree = []
        for i in range (len(S)):
            cardinality_tree.append(None)
        logging.debug("cardinality_tree:")
        logging.debug(cardinality_tree)
        next_sum = minimum
        while True:
            next = ESS(S, next_sum, maximum)  # ESS returns the smallest subset between next_sum and maximum
            logging.debug("next:")
            logging.debug(next)
            if next is None:
                break
            next_sum = sum(next)
            if next_sum < ub:
                heappush(min_heap, next_sum)
                next_sum = next_sum + 1
            else:
                heappush(max_heap, -next_sum)
                next_sum = next_sum + 1
                counter = counter + 1
            if counter == m:
                break
        maximum = -min(max_heap)
        minimum = sum(S) - (k - 1) * maximum
        logging.debug("maximum = %d, minimum = %d", maximum, minimum)
        while True:
            logging.debug("in while")
            next = ESS(S, next_sum, maximum)  # ESS returns the smallest subset between next_sum and maximum
            if next is None:
                break
            next_sum = sum(next)
            heapq.heappush(max_heap, -next_sum)
            heapq.heappop(max_heap)
            maximum = -min(max_heap)
            minimum = sum(S) - (k - 1) * maximum
            next_sum = next_sum + 1
        subset_sums = list(max_heap)
        for i in range(len(subset_sums)):
            subset_sums[i] = -subset_sums[i]
        subset_sums.sort(reverse=True)
        logging.debug("subset_sums:")
        logging.debug(subset_sums)
        for subset_sum in subset_sums:
            S_1 = Horowitz_Sahni(S, subset_sum)  # Find the subset that matches the sum
            ub = sum(S_1)
            lb = sum(S) - (k - 1) * ub
            for subset_sum2 in subset_sums:
                S_2 = Horowitz_Sahni(S, subset_sum2)
                logging.debug("S_2:")
                logging.debug(S_2)
                if (sum(S_2) >= lb and sum(S_2) <= ub):
                    cardinality_tree[len(S_2)] = Tree_insert(cardinality_tree[len(S_2)], S, S_2)
            logging.debug("cardinality_tree:")
            logging.debug(cardinality_tree)
            Search(S, [S_1], cardinality_tree, 1)
        m = 2 * m

    return None


def Search(S: List[int], current_allocation: List[any], cardinality_tree: List[Tree], card: int):
    if card < len(cardinality_tree):
        union = []
        for i in range(len(current_allocation)):
            for j in range(len(current_allocation[i])):
                union.append(current_allocation[i][j])
        union.sort(reverse=True)
        is_full_allocation = True
        if len(S) == len(union):
            for i in range(len(S)):
                if S[i] != union[i]:
                    is_full_allocation = False
            if is_full_allocation:
                return current_allocation
        else:
            S_R = {}
            S_pointer = 0
            union_pointer = 0
            is_possible_allocation = True
            while is_possible_allocation and S_pointer < len(S) and union_pointer < len(union):
                if S[S_pointer] == union[union_pointer]:
                    S_pointer += 1
                    union_pointer += 1
                elif S[S_pointer] < union[union_pointer]:
                    is_possible_allocation = False
                else:
                    S_R.append(S[S_pointer])
                    S_pointer += 1
        t = {}
        if cardinality_tree[card] is not None:
            Tree_search(S, current_allocation, S_R, cardinality_tree[card], card, t)
        Search(S, current_allocation, cardinality_tree, card+1)


def Tree_search(S: List[int], current_allocation: List[any], S_R: List[int], cardinality_tree: List[Tree], card: int,
                t: List[int]):
    tree = cardinality_tree[card]
    if cardinality_tree[card].data in S_R:
        if cardinality_tree[card].left is None:
            t.append(cardinality_tree[card].data)
            current_allocation.append(t)
            Search(S, current_allocation, cardinality_tree, card)
        else:
            Tree_search(S, current_allocation, S_R, cardinality_tree[card].right, t)
            t.append(cardinality_tree[card].data)
            Tree_search(S, current_allocation, S_R, cardinality_tree[card].left, t)
    elif cardinality_tree[card].right is not None:
        Tree_search(S, current_allocation, S_R, cardinality_tree[card].right, t)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Cached_Iterative_Weakening(BinnerKeepingContents(), 3, [127, 125, 122, 105, 87, 75, 68, 64, 30, 22], 6)
