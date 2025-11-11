from typing import List, Tuple


def program4B(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4B
    
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

    opt = [(0, [])] * n # DP table to store previous small subproblems

    for i in range(n): # For every value in original array
        max_sum = 0
        max_indices = []
    
        # Traverse previous small subproblems
        # If we're starting with the first index, this gets skipped always
        # If the max_sum (our greatest sum of previous values) is less than the currently processed previous max sum:
        #     Update max_sum, and grab a copy of the indexes that made that vault sum
        for j in range(0, i - k): 
            if max_sum < opt[j][0]:
                max_sum = opt[j][0]
                max_indices = opt[j][1].copy()

        # Decide on what to add in our optimal array
        # If the optimal solution to the previous subproblem is greater than our current result: 
        #     Choose to store those values at opt[i] since they are the better solution
        # Otherwise, add take the current vault, add the vaults value to the max_sum and index to max_indices.
        #     Store this at opt[i]
        res = 0
        if i > 0 and opt[i - 1][0] >= values[i] + max_sum:
            res = (opt[i - 1][0], opt[i - 1][1])
        else:
            max_indices.append(i)
            res = (values[i] + max_sum, max_indices)

        opt[i] = (res[0], res[1])

    # The optimal value will be present at the last index in the array, along with the 0-indexed indices
    return opt[n - 1][0], [val + 1 for val in opt[n - 1][1]] # replace with your code


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program4B(n, k, values)

    print(m)
    for i in indices:
        print(i)
