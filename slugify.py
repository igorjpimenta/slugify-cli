"""slugify: turn text into a URL slug.

Rules (stdlib only):
  - lowercase
  - strip accents via unicodedata (NFKD + drop combining marks)
  - collapse any run of non-alphanumerics into one hyphen
  - trim leading/trailing hyphens

CLI usage:
  python3 slugify.py "Hello World"
  python3 slugify.py Hello World        # args are joined with spaces
  echo "Hello World" | python3 slugify.py
  ./slugify "Hello World"               # executable wrapper (same dir)
"""

import re
import sys
import unicodedata


def slugify(text: str) -> str:
    """Convert *text* to a URL slug."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(
        ch for ch in normalized if not unicodedata.combining(ch)
    )
    lowered = ascii_text.lower()
    slugged = re.sub(r"[^a-z0-9]+", "-", lowered)
    return slugged.strip("-")


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args:
        text = " ".join(args)
    elif sys.stdin.isatty():
        print(
            "slugify: error: no input provided "
            "(pass text as arguments or via stdin)",
            file=sys.stderr,
        )
        return 2
    else:
        text = sys.stdin.read()
    result = slugify(text)
    if not result:
        print(
            "slugify: error: empty slug "
            "(input contained no alphanumeric characters)",
            file=sys.stderr,
        )
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
