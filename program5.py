from typing import List, Tuple

def program5(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Θ(n) DP for the general vault problem.
    dp[i] = max(dp[i-1], values[i] + dp[i-(k+1)])
    We also track choices to reconstruct the picked indices.
    """
    if n == 0:
        return 0, []

    dp = [0] * n          # dp[i] = best total using vaults up to i
    take = [False] * n    # take[i] = True if we pick vault i in an optimal solution

    for i in range(n):
        take_val = values[i] + (dp[i - (k + 1)] if i - (k + 1) >= 0 else 0)
        skip_val = dp[i - 1] if i - 1 >= 0 else 0

        if take_val > skip_val:
            dp[i] = take_val
            take[i] = True
        else:
            dp[i] = skip_val
            take[i] = False

    # Reconstruct indices (1-indexed, increasing)
    indices = []
    i = n - 1
    while i >= 0:
        if take[i]:
            indices.append(i + 1)   # store 1-indexed
            i -= (k + 1)            # skip k neighbors to the left
        else:
            i -= 1
    indices.reverse()

    return dp[n - 1], indices


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    total, indices = program5(n, k, values)

    print(total)
    for idx in indices:
        print(idx)