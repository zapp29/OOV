"""Implements a presentation layer for OOV."""
import subprocess
from itertools import islice
from typing import Dict


def terminal_line_lenght() -> int:  # pragma: nocover
    """Checks what is current users terminal size."""
    tput = subprocess.Popen(["tput", "cols"], stdout=subprocess.PIPE)
    return int(tput.communicate()[0].strip())


def build_table(raw_table: Dict[str, Dict[str, int]]) -> None:
    """Prepare a table for printing.

    If the table is bigger than screen width, split it into chunks.
    """
    lens = {e: len(e) for e in raw_table}
    max_col_size = max([len(e) for e in raw_table])
    max_line_length = int(0.9 * (terminal_line_lenght() - max_col_size))

    joined_header_row = ""
    joined_header_row_dry_run = ""
    chunk_start = 0
    chunk_end = 0
    for i, e in enumerate(raw_table):
        joined_header_row_dry_run = joined_header_row
        if joined_header_row_dry_run != "":
            joined_header_row_dry_run += " | "
        joined_header_row_dry_run += e
        if len(joined_header_row_dry_run) > max_line_length:
            chunk_end = i
            table_chunk = dict(islice(raw_table.items(), chunk_start, chunk_end))
            draw_table_chunk(table_chunk, lens, max_col_size)
            chunk_start = i
            joined_header_row = ""
        else:
            joined_header_row = joined_header_row_dry_run
    chunk_start = chunk_end
    chunk_end = i
    table_chunk = dict(islice(raw_table.items(), chunk_start, chunk_end))
    draw_table_chunk(table_chunk, lens, max_col_size)
    return


def draw_table_chunk(raw_table: Dict[str, Dict[str, int]], lens, max_col_size) -> None:
    """Render a given chunk of a table."""
    cols = list(raw_table)
    rows = list(raw_table[list(raw_table)[0]])
    joined_header_row = " | ".join([e for e in raw_table])

    print("=" * (len(joined_header_row) + max_col_size))
    print(" " * max_col_size + joined_header_row)
    print("=" * (len(joined_header_row) + max_col_size))

    for row in rows:
        text = row.ljust(max_col_size)
        print(text, end=" ")
        for col in cols:
            l_col = len(col)

            try:
                cell = raw_table[col][row]
            except KeyError:
                cell = "N/A"
            text = str(cell).rjust(lens[col] - int(l_col / 2)).ljust(l_col + 2)
            text = text.replace("0", " ")
            text = text.replace("1", "Y")
            print(text, end=" ")
        print("")
    return
