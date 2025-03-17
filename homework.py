import heapq
from random import randint
from typing import List


class Solution:

    def maxMeetingRooms(self, rooms) -> int:
        rooms = sorted(rooms)
        max_rooms = 0
        current_rooms = 0
        end_time_heap = []
        for r_s, r_e in rooms:
            while end_time_heap and end_time_heap[0] <= r_s:
                heapq.heappop(end_time_heap)
                current_rooms -= 1

            current_rooms += 1
            max_rooms = max(max_rooms, current_rooms)
            heapq.heappush(end_time_heap, r_e)

        return max_rooms


#[[0, 30],[5, 10],[15, 20]]

end_time_heap = [20, 30]
curr = 2, max=2
