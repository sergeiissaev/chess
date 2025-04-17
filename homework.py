import heapq
from io import StringIO
from random import randint
from typing import List

import pandas as pd
import requests


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


def read_csv_data(url: str) -> pd.DataFrame:
    """ Helper function to read the data from the Google Drive URL """
    df_list = pd.read_html(url, encoding='utf-8', header=0)
    df = df_list[0]
    df["x-coordinate"] = df["x-coordinate"].astype("int")
    df["y-coordinate"] = df["y-coordinate"].astype("int")
    return df


def decode_message(url: str) -> None:
    """ Main function to read the table and print the hidden message """
    df = read_csv_data(url=url)
    grid_width = df['x-coordinate'].max()
    grid_length = df['y-coordinate'].max()
    grid = [[' ' for _ in range(grid_width + 1)] for _ in range(grid_length + 1)]
    data = df[["Character", "x-coordinate", "y-coordinate"]].values
    for char, x, y in data:
        grid[y][x] = char
    for row in reversed(grid):
        print(''.join(row))


decode_message(url='https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub?output=csv')
df = read_csv_data(url='https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub?output=csv')

url_response = requests.get('https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub')
url_response.raise_for_status()
url_text = url_response.text
row_start_text = '</span></p></td></tr><tr class="c2"><td class="c0" colspan="1" rowspan="1"><p class="c3"><span class="c1">'
url_text_split_rows = url_text.split(row_start_text)
for row in range(2, len(url_text_split_rows)):
    text = url_text_split_rows[row]
    #<span class="c3">


df = pd.DataFrame(StringIO(url_response.text))
print(df)
