# slugify-cli

Python 3 stdlib-only CLI that turns text into a URL slug.

Rules: lowercase → strip accents (`unicodedata` NFKD) → collapse each run
of non-alphanumerics into one hyphen → trim leading/trailing hyphens.

## Usage

```sh
python3 slugify.py "Hello, World!"        # -> hello-world
python3 slugify.py Café au lait           # -> cafe-au-lait
echo "Hello World" | python3 slugify.py   # -> hello-world
./slugify "Hello World"                   # -> hello-world (wrapper)
```

Text can be passed as arguments (joined with spaces) or via stdin.
An input that produces an empty slug exits `2` with an error message.

## Examples

| Input | Slug |
|---|---|
| `Hello, World!` | `hello-world` |
| `Café au lait — crème brûlée` | `cafe-au-lait-creme-brulee` |
| `  Hello---World!!  ` | `hello-world` |
