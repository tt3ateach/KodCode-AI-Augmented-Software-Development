"""Check is_valid_israeli_id() in israeli_id.py against numbers whose answer is known.

    python check_id.py
"""

from israeli_id import is_valid_israeli_id

# Valid numbers satisfy the official check-digit rule; the others don't, or aren't numbers at all.
CASES = {
    "123456782": True,
    "039337423": True,
    "39337423": True,     # leading zero left out
    "000000018": True,
    "123456789": False,   # wrong check digit
    "12345678": False,
    "12a456782": False,
    "1234567890": False,  # too long
    "": False,
}

failures = 0
for number, expected in CASES.items():
    got = bool(is_valid_israeli_id(number))
    mark = "ok  " if got == expected else "FAIL"
    failures += got != expected
    print(f"{mark} {number!r:14} expected {expected!s:5}  got {got}")
print("\nAll correct." if not failures else f"\n{failures} of {len(CASES)} wrong.")
