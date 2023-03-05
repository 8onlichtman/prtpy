from Horowitz_And_Sahni import Horowitz_Sahni


def ESS (S: list, minimum: int, maximum: int):
    for i in range(minimum, maximum):
        if sum(Horowitz_Sahni(S, i)) == i:     #There exists a bin with sum i
            return Horowitz_Sahni(S, i)
    return None                                #There is no bin with sum between minimum and maximum
