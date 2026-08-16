PAGE_SIZE = 1024
PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
SEGMENT_TABLE = {0: (1000, 400), 1: (2200, 300), 2: (500, 150)}


def translate_paged(address):
    page = address // PAGE_SIZE
    offset = address % PAGE_SIZE
    if page not in PAGE_TABLE:
        return f"{address}: PAGE FAULT (page {page} is not in PAGE_TABLE)"
    physical = PAGE_TABLE[page] * PAGE_SIZE + offset
    return f"{address}: physical address {physical} (page {page}, offset {offset})"


def translate_segmented(segment, offset):
    if segment not in SEGMENT_TABLE:
        return f"({segment}, {offset}): SEGMENTATION FAULT (unknown segment)"
    base, limit = SEGMENT_TABLE[segment]
    if offset >= limit:
        return f"({segment}, {offset}): SEGMENTATION FAULT (offset {offset} >= limit {limit})"
    return f"({segment}, {offset}): physical address {base + offset}"


if __name__ == "__main__":
    for address in (260, 1500, 3000, 5000):
        print(translate_paged(address))
    for pair in ((0, 150), (1, 350), (2, 100)):
        print(translate_segmented(*pair))
