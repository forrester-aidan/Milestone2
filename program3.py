from typing import List, Tuple


def program3(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 3
    
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

    max_sum = [0, []]
    def backtrack(index, curr, curr_sum, k):
        nonlocal max_sum
        if index >= n:
            if max_sum[0] < curr_sum:
                max_sum[0], max_sum[1] = curr_sum, curr.copy()
            return
        
        # Take current index
        curr.append(values[index])
        backtrack(index + k, curr, curr_sum + values[index], k)

        # Pop previous and skip current index
        curr.pop()
        backtrack(index + 1, curr, curr_sum, k)
        return
    backtrack(0, [], 0, k)

    return tuple(max_sum)


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program3(n, k, values)

    print(m)
    for i in indices:
        print(i)