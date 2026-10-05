from collections import deque

from Weapons import Weapons


def get_weapons():
    """ที่เก็บข้อมูลอาวุธทั้งหมด 21 ชิ้น (คืนค่าเป็น list ของวัตถุ Weapons)"""
    return [
        Weapons("M4",      25, 100, 200, 30, 2.5, 3.5, 85, 30, "Assault Rifle"),
        Weapons("AK47",    30,  80, 180, 30, 3.0, 4.0, 75, 50, "Assault Rifle"),
        Weapons("SCAR-L",  28,  90, 200, 30, 2.6, 3.5, 88, 35, "Assault Rifle"),
        Weapons("M416",    26,  95, 210, 30, 2.4, 3.6, 87, 28, "Assault Rifle"),
        Weapons("Groza",   32,  85, 190, 30, 2.8, 4.1, 80, 45, "Assault Rifle"),
        Weapons("AWM",    100,  10, 500,  5, 4.0, 6.0, 95, 20, "Sniper"),
        Weapons("Kar98k",  80,  12, 400,  5, 3.5, 5.0, 90, 40, "Sniper"),
        Weapons("M24",     85,  15, 450,  5, 3.2, 5.5, 92, 35, "Sniper"),
        Weapons("MP5",     20, 120, 100, 30, 2.0, 2.5, 80, 25, "SMG"),
        Weapons("UMP45",   22, 110, 120, 30, 2.2, 2.7, 82, 30, "SMG"),
        Weapons("Vector",  18, 150,  80, 33, 1.8, 2.0, 78, 35, "SMG"),
        Weapons("UZI",     16, 140,  70, 25, 1.9, 1.9, 74, 38, "SMG"),
        Weapons("P90",     19, 135,  90, 50, 2.6, 2.6, 81, 27, "SMG"),
        Weapons("Mini14",  45,  40, 300, 20, 2.7, 4.0, 89, 32, "DMR"),
        Weapons("SKS",     50,  35, 320, 10, 2.9, 4.2, 86, 36, "DMR"),
        Weapons("Mk14",    52,  45, 330, 20, 3.1, 5.0, 88, 42, "DMR"),
        Weapons("S12K",    60,  30,  40, 10, 3.4, 4.5, 60, 55, "Shotgun"),
        Weapons("S686",    75,  20,  35,  2, 2.2, 3.8, 58, 60, "Shotgun"),
        Weapons("M249",    24, 110, 230, 100, 6.0, 8.0, 70, 48, "LMG"),
        Weapons("DP-28",   27,  70, 220, 47, 4.5, 6.5, 72, 44, "LMG"),
        Weapons("Tommy",   21, 100, 110, 30, 2.3, 4.2, 76, 33, "SMG"),
    ]


# ---------------------------------------------------------------
# โครงสร้างข้อมูลสำหรับเก็บและนำออกมาใช้ : Stack และ Queue
# ---------------------------------------------------------------

class Stack:
    """LIFO : เข้าทีหลัง ออกก่อน -> ใช้เก็บประวัติเพื่อ Undo"""

    def __init__(self):
        self._data = []

    def push(self, x):
        self._data.append(x)

    def pop(self):
        return self._data.pop()

    def is_empty(self):
        return not self._data

    def __len__(self):
        return len(self._data)


class Queue:
    """FIFO : เข้าก่อน ออกก่อน -> ใช้เป็นคิวอาวุธที่เลือกไว้"""

    def __init__(self):
        self._data = deque()

    def enqueue(self, x):
        self._data.append(x)

    def dequeue(self):
        return self._data.popleft()

    def is_empty(self):
        return not self._data

    def items(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)
