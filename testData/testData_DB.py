import re
import sqlite3
from pathlib import Path
from typing import List, Tuple

# =========================
# Configuration
# =========================
DB_PATH = Path("testData/CustomerDB.db")
TABLE_NAME = "customers"

# Your 6 entries, one per line, columns separated by '-'
RAW_LINES = [
    "1047 - Chandrakanth Y - 9894582770 - 22/03/1996 - 0 - True",
    "1048 - Chandrakanth M - 9985733456 - 21/03/1994 - 50 - False",
    "1049 - Madhumitha P - 9729379022 - 12/05/2000 - 10 - False",
    "1050 - Sandhiya V - 9894582890 - 18/08/1998 - 17 - False",
    "1051 - Vidhiya M - 9894587110 - 19/05/1990 - 90 - False",
    "1057 - Naveen S - 8897023412 -  17/02/1997 - 0 - True",
]

# =========================
# Helpers: parsing & validation
# =========================

DOB_REGEX = re.compile(r"^[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}$")
DIGITS10 = re.compile(r"^[0-9]{10}$")

def parse_line(line: str) -> Tuple[int, str, str, str, int, int]:
    """
    Parse a single input line with fields separated by '-'.
    Returns a tuple: (id, name, phone, dob, credits, account_locked_int)
    """
    parts = [p.strip() for p in line.split("-")]
    if len(parts) != 6:
        raise ValueError(f"Expected 6 fields separated by '-', got {len(parts)} in: {line}")

    # Unpack and normalize
    id_str, name, phone, dob, credits_str, locked_str = parts

    # ID
    try:
        rec_id = int(id_str)
    except ValueError:
        raise ValueError(f"ID must be an integer: {id_str}")

    # Phone: normalize spaces, ensure exactly 10 digits
    phone_digits = re.sub(r"\s+", "", phone)
    if not DIGITS10.match(phone_digits):
        raise ValueError(f"Phone must be exactly 10 digits: {phone} -> {phone_digits}")

    # DOB: must match dd/mm/yyyy (basic check)
    dob_norm = re.sub(r"\s+", "", dob)
    if not DOB_REGEX.match(dob_norm):
        raise ValueError(f"Date of Birth must be dd/mm/yyyy: {dob}")

    # Credits
    try:
        credits = int(credits_str)
    except ValueError:
        raise ValueError(f"Credits must be an integer: {credits_str}")

    # Account Locked: True/False -> 1/0 (case-insensitive)
    locked_clean = locked_str.strip().lower()
    if locked_clean not in ("true", "false"):
        raise ValueError(f"Account Locked must be True or False: {locked_str}")
    locked_int = 1 if locked_clean == "true" else 0

    return rec_id, name, phone_digits, dob_norm, credits, locked_int


def parse_all(lines: List[str]) -> List[Tuple[int, str, str, str, int, int]]:
    rows = []
    for idx, ln in enumerate(lines, start=1):
        if not ln.strip():
            continue
        try:
            rows.append(parse_line(ln))
        except Exception as e:
            raise ValueError(f"Error in line {idx}: {e}") from e
    return rows


# =========================
# Database setup
# =========================

CREATE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id             INTEGER PRIMARY KEY,                 -- ID [Int]
    name           TEXT NOT NULL,                       -- Name [varchar-like]
    phone_number   TEXT NOT NULL
                   CHECK(length(phone_number) = 10 AND phone_number GLOB '[0-9]*'),
                                                       -- Phone Number [10 digits]
    date_of_birth  TEXT NOT NULL
                   CHECK(date_of_birth GLOB '[0-3][0-9]/[0-1][0-9]/[1-2][0-9][0-9][0-9]'),
                                                       -- Date Of Birth [dd/mm/yyyy]
    credits        INTEGER NOT NULL DEFAULT 0
                   CHECK(credits >= 0),                -- Credits [Int]
    account_locked INTEGER NOT NULL DEFAULT 0
                   CHECK(account_locked IN (0, 1))     -- Account Locked [Boolean 0/1]
);
"""

INSERT_SQL = f"""
INSERT INTO {TABLE_NAME}
(id, name, phone_number, date_of_birth, credits, account_locked)
VALUES (?, ?, ?, ?, ?, ?);
"""

def main():
    # Connect (creates DB file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table
    cur.execute(CREATE_SQL)
    conn.commit()

    # Parse inputs
    rows = parse_all(RAW_LINES)

    # Insert rows
    cur.executemany(INSERT_SQL, rows)
    conn.commit()

    # Read back and display
    print(f"Database created at: {DB_PATH.resolve()}")
    print(f"Table '{TABLE_NAME}' contents:")
    for row in cur.execute(f"SELECT id, name, phone_number, date_of_birth, credits, account_locked FROM {TABLE_NAME} ORDER BY id;"):
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()