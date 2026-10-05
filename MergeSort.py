class MergeSorter:
    """เรียงลำดับด้วย Merge Sort (stable, O(n log n))"""

    @staticmethod
    def sort(items, attr, ascending=True):
        """เรียงรายการวัตถุตามคุณสมบัติ attr แล้วคืนลิสต์ใหม่ (ไม่แก้ลิสต์เดิม)"""
        if len(items) <= 1:
            return list(items)
        mid = len(items) // 2
        left = MergeSorter.sort(items[:mid], attr, ascending)
        right = MergeSorter.sort(items[mid:], attr, ascending)
        return MergeSorter._merge(left, right, attr, ascending)

    @staticmethod
    def _merge(left, right, attr, ascending):
        result, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            a, b = getattr(left[i], attr), getattr(right[j], attr)
            if (a <= b) if ascending else (a >= b):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class Searcher:
    """การค้นหาข้อมูล : Linear Search และ Binary Search"""

    @staticmethod
    def linear_search(items, attr, text):
        """ไล่ดูทีละตัว ค้นข้อความบางส่วนได้ ไม่ต้องเรียงก่อน  O(n)"""
        text = text.strip().lower()
        return [w for w in items if text in str(getattr(w, attr)).lower()]

    @staticmethod
    def binary_search(sorted_items, attr, target):
        """แบ่งครึ่งช่วงค้นหาทีละรอบ ต้องเรียงน้อย→มากตาม attr ก่อน  O(log n)
        คืนรายการทุกตัวที่ค่าตรงกับ target"""
        lo, hi = 0, len(sorted_items) - 1
        found = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            v = getattr(sorted_items[mid], attr)
            if v == target:
                found = mid
                break
            if v < target:
                lo = mid + 1
            else:
                hi = mid - 1
        if found == -1:
            return []
        left = right = found                      # ขยายหาค่าที่ซ้ำกันซ้าย-ขวา
        while left > 0 and getattr(sorted_items[left - 1], attr) == target:
            left -= 1
        while right < len(sorted_items) - 1 and getattr(sorted_items[right + 1], attr) == target:
            right += 1
        return sorted_items[left:right + 1]

    @staticmethod
    def parse_value(items, attr, text):
        """แปลงข้อความที่พิมพ์ให้เป็นชนิดเดียวกับข้อมูล (ตัวเลข/ข้อความ)"""
        text = text.strip()
        if attr in ("name", "type"):
            for w in items:                       # ไม่สนตัวพิมพ์เล็ก-ใหญ่
                if str(getattr(w, attr)).lower() == text.lower():
                    return getattr(w, attr)
            return text
        return float(text) if "." in text else int(text)
