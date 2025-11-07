from typing import List, Tuple


def program4A(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4A
    
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

    memo = [-1] * n # Stores previous computations, include sum and vaults used
    res = tuple() # Stores max result as tuple

    if n == 0:
        return 0, []

    def backtrack(i):
        nonlocal memo
        nonlocal res
        if i >= n:
            return 0

        take, indices = values[i], []
        for j in range(0, i - k): # Loop through all previous computations to find max
            if memo[j] != -1:
                prev = memo[j]
                if values[i] + prev[0] > take: # Update the current take of values
                    take = values[i] + prev[0]
                    indices = prev[1].copy()
        
        indices.append(i)
        curr = (take, indices)

        if not res or res[0] < take:  # Update max, that way we dont have to iterate at the end
            res = curr

        memo[i] = curr    # Store optimal sum at the current index for further computations
        backtrack(i + 1)  # Process the next index
        return
    
    backtrack(0)
    return res[0], [val + 1 for val in res[1]] 

if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program4A(n, k, values)

    print(m)
    for i in indices:
        print(i)