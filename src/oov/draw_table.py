from typing import Dict


def draw_table(raw_table: Dict[str, Dict[str, int]]) -> None:

    lens = {e: len(e) for e in raw_table}
    max_col_size = max([len(e) for e in raw_table])
    joined_header_row = " | ".join([e for e in raw_table])

    print("=" * (len(joined_header_row) + max_col_size))
    print(" " * max_col_size + joined_header_row)
    print("=" * (len(joined_header_row) + max_col_size))

    for k, column in raw_table.items():
        text = k.ljust(max_col_size)
        print(text, end=" ")
        for i, row in column.items():
            text = str(row).rjust(lens[i] - int(len(i) / 2)).ljust(len(i) + 2)
            text = text.replace("0", " ")
            text = text.replace("1", "Y")
            print(text, end=" ")
        print("")
