from typing import List, Tuple


def program1(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 1
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    """
    ############################
    # Add you code here
    ############################

    #edge cases
    if n == 0:
        return 0, []
    
    if n == 1:
        return values[0], [1]
    
    picked_vaults = []

    i = n - 1
    total_value = 0
    while i >= 0:
        picked_vaults.append(i)
        total_value += values[i]
        i = i - k - 1

    picked_vaults.reverse()
    picked_vaults_ind = [ind + 1 for ind in picked_vaults]


    return total_value, picked_vaults_ind


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program1(n, k, values)

    print(m)
    for i in indices:
        print(i)