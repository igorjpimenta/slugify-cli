# slugify-cli

Python 3 (stdlib-only) CLI that turns text into a URL slug.

**Rules:** lowercase → strip accents (`unicodedata` NFKD) → collapse each run
of non-alphanumerics into one hyphen → trim leading/trailing hyphens.

## Installation

No install step — it's a single script. Get it with either:

```sh
git clone https://github.com/igorjpimenta/slugify-cli
# or
gh repo clone igorjpimenta/slugify-cli
```

Requires Python 3.6+ (stdlib only, no dependencies).

## Running it

```sh
./slugify "Some Text"            # executable wrapper
python3 slugify.py "Some Text"   # same thing
```

Text is passed as arguments (multiple args are joined with spaces)
or piped through stdin:

```sh
echo "Some Text" | ./slugify
```

## Examples

### 1. Arguments are joined, case is folded

```sh
$ python3 slugify.py Hello World
hello-world
```

### 2. Accents are stripped

```sh
$ python3 slugify.py "Café au lait — crème brûlée"
cafe-au-lait-creme-brulee
```

### 3. Repeated / mixed separators collapse into one hyphen

```sh
$ python3 slugify.py "  Hello---World!!  "
hello-world
```

### 4. Stdin input

```sh
$ echo "Über API Gateway 2024" | python3 slugify.py
uber-api-gateway-2024
```

## Exit codes

| Code | Meaning | Trigger |
|---|---|---|
| `0` | Success | A non-empty slug was printed |
| `2` | Input error | No arguments and no stdin data (tty case), or the input contains no alphanumeric characters at all (e.g. `echo '!!!' \| ./slugify`) |

Errors are reported on stderr:

```sh
$ echo '!!!' | python3 slugify.py; echo "exit=$?"
slugify: error: empty slug (input contained no alphanumeric characters)
exit=2
```
