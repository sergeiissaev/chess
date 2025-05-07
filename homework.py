import heapq
import random
from io import StringIO
from random import randint
from typing import List

import numpy as np


class Solution:

    def maxMeetingRooms(self, logs, N) -> int:
        rank = [1] * N
        parent = [i for i in range(N)]
        def find(n):
            if parent[n] != n:
                return find(parent[n])
            return n

        def union(a, b, n):
            parent_a = find(a)
            parent_b = find(b)
            if parent_a != parent_b:
                n -= 1
                if rank[parent_a] > rank[parent_b]:
                    rank[parent_a] += rank[parent_b]
                    parent[parent_b] = a
                else:
                    rank[parent_b] += rank[parent_a]
                    parent[parent_a] = b
            return n




        logs = sorted(logs)
        for log in logs:
            time, p1, p2 = log
            N = union(p1, p2, N)
            if N == 1: return time

        return -1


#print("".join(a for a in np.random.choice([".", "R", "L", ".", "."], random.randint(1, 10))))
print([random.randint(1, 2) for _ in range(3)])
sol = Solution()
logs =  [
    [1, 0, 1],
    [2, 1, 2],
    [3, 2, 3],
    [4, 3, 4],
    [5, 4, 0]
]
N = 5
print(sol.maxMeetingRooms(logs=logs, N=N))