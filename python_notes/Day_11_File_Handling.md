# Day 11 – File Handling

**Duration:** 50–60 Minutes

### Learning Outcomes
- Understand **why** programs need files (persistent storage beyond memory).
- **Open, read, write, append and close** files correctly.
- Know **all file modes** (`r`, `w`, `a`, `x`, `+`, `b`, `t`) and when to use each.
- Use the **`with` context manager** for safe, automatic file closing.
- Navigate a file with **`seek()`** and **`tell()`**.
- Read and write **CSV** and **JSON** files.

## 0. Safe Workspace (Setup)

The examples below create small sample files. To keep your course folder clean, this notebook
switches into a **temporary directory** first — every file we create lands there, not in your
project. Run this cell once before the rest.

```python
import os, tempfile

WORKDIR = tempfile.mkdtemp(prefix="day11_files_")
os.chdir(WORKDIR)
print("All files in this notebook are created inside:")
print(WORKDIR)
```

**Output:**
```text
All files in this notebook are created inside:
/tmp/day11_files_yuryou5x
```

## 1. What is File Handling?

Variables live in **RAM** and vanish when the program ends. A **file** stores data on **disk**,
so it survives after the program stops. **File handling** is the process of creating, reading,
updating and deleting files from a program.

### Why do we need files?
- **Persistence** — keep data (settings, logs, results) after the program closes.
- **Large data** — data too big to keep in memory can be streamed from disk.
- **Sharing** — exchange data with other programs (CSV, JSON, logs).
- **Records** — save reports, exports and backups.

## 2. Types of Files

| Type | Contents | Examples | Open mode |
|---|---|---|---|
| **Text file** | Human-readable characters (encoded, e.g. UTF-8) | `.txt`, `.csv`, `.py`, `.json`, `.html` | `"t"` (default) |
| **Binary file** | Raw bytes (not human-readable) | `.jpg`, `.png`, `.mp3`, `.exe`, `.pdf` | `"b"` |

**Key Notes:**
- Text mode reads/writes **`str`**; binary mode reads/writes **`bytes`**.
- Text mode handles line-ending and encoding conversions; binary mode does not.
- Default is **text mode** (`"t"`), so `"r"` means `"rt"`.

## 3. The File Handling Workflow

```text
  +--------+     +------------------+     +---------+
  |  OPEN  | --> | READ / WRITE /   | --> |  CLOSE  |
  | open() |     | APPEND (process) |     | close() |
  +--------+     +------------------+     +---------+

  Open a file  ->  do your work  ->  release the file
```

**Key Notes:**
- Always **close** a file (or better, use `with`) so data is flushed to disk and the OS handle
  is released.
- Forgetting to close can lose un-written data or lock the file.

## 4. The `open()` Function

`open()` connects your program to a file and returns a **file object** you read/write through.

**Syntax**
```python
file_object = open(filename, mode="r", encoding=None)
```

- `filename` — path to the file (relative or absolute).
- `mode` — how to open it (see next section). Default `"r"`.
- `encoding` — text encoding, use `"utf-8"` for text files.

**Key Notes:**
- For text files always prefer `encoding="utf-8"` to avoid platform surprises.
- `open()` in write/append mode **creates** the file if it does not exist.

```python
# Create a file, then confirm open() returns a file object
f = open("hello.txt", "w", encoding="utf-8")
f.write("Hello, files!")
f.close()

f = open("hello.txt", "r", encoding="utf-8")
print(type(f))       # <class '_io.TextIOWrapper'>
print(f.read())
f.close()
```

**Output:**
```text
<class '_io.TextIOWrapper'>
Hello, files!
```

## 5. File Modes (Neatly Categorized)

### Core access modes
| Mode | Name | If file exists | If missing | Cursor | Can read? | Can write? |
|---|---|---|---|---|---|---|
| `"r"` | Read | opens | **error** | start | ✅ | ❌ |
| `"w"` | Write | **erases** it | creates | start | ❌ | ✅ |
| `"a"` | Append | keeps it | creates | **end** | ❌ | ✅ (at end) |
| `"x"` | Exclusive create | **error** | creates | start | ❌ | ✅ |

### Update variants (add `+` for read **and** write)
| Mode | Meaning |
|---|---|
| `"r+"` | Read + write, file must exist, no truncation |
| `"w+"` | Read + write, **truncates** existing file |
| `"a+"` | Read + append, cursor at end for writing |

### Text vs binary (combine with the above)
| Suffix | Meaning |
|---|---|
| `"t"` | Text mode (default) — works with `str` |
| `"b"` | Binary mode — works with `bytes` (e.g. `"rb"`, `"wb"`) |

**Memory aid:** `r`ead, `w`rite (wipe!), `a`ppend, e`x`clusive.

```python
# w = write (creates / overwrites), r = read
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("first version")

# w again OVERWRITES the whole file
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("second version")

with open("demo.txt", "r", encoding="utf-8") as f:
    print(f.read())   # only 'second version' remains
```

**Output:**
```text
second version
```

## 6. Reading From a File

Python offers three read methods — pick by how much you need at once.

**Functions:** `read()`, `readline()`, `readlines()`

**Input:** optional size (number of characters) for `read`/`readline`.

**Output:**
- `read()` → the **whole file** as one string (or `read(n)` → first `n` chars).
- `readline()` → the **next single line** (including its `\n`).
- `readlines()` → a **list** of all lines.

```python
# Prepare a multi-line file
with open("poem.txt", "w", encoding="utf-8") as f:
    f.write("Roses are red\n")
    f.write("Violets are blue\n")
    f.write("Python is sweet\n")

# read() -> entire file as one string
with open("poem.txt", "r", encoding="utf-8") as f:
    print(repr(f.read()))
```

**Output:**
```text
'Roses are red\nViolets are blue\nPython is sweet\n'
```

```python
# readline() -> one line at a time
with open("poem.txt", "r", encoding="utf-8") as f:
    print(f.readline().strip())   # line 1
    print(f.readline().strip())   # line 2

# readlines() -> list of all lines
with open("poem.txt", "r", encoding="utf-8") as f:
    print(f.readlines())
```

**Output:**
```text
Roses are red
Violets are blue
['Roses are red\n', 'Violets are blue\n', 'Python is sweet\n']
```

## 7. Looping Over a File (Best Practice)

The cleanest, most memory-friendly way to read a file is to **iterate the file object directly**.
It reads one line at a time — safe even for very large files.

```python
with open("poem.txt", "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        print(line_no, line.strip())   # strip() removes the trailing newline
```

**Output:**
```text
1 Roses are red
2 Violets are blue
3 Python is sweet
```

## 8. Writing to a File

**Functions:** `write()`, `writelines()`

**Input:** a string (`write`) or a list of strings (`writelines`).

**Output:** `write()` returns the number of characters written; `writelines()` returns `None`.

**Key Notes:**
- `write()` does **not** add newlines — add `\n` yourself.
- `writelines()` also does **not** add newlines between items.
- Mode `"w"` **overwrites** the whole file (see the warning below).

```python
# write() a few lines (note the explicit \n)
with open("names.txt", "w", encoding="utf-8") as f:
    n = f.write("Alice\n")
    f.write("Bob\n")
    print("characters written on line 1:", n)

# writelines() with a list
lines = ["Ravi\n", "Sita\n", "Gita\n"]
with open("names.txt", "a", encoding="utf-8") as f:  # append, keep existing
    f.writelines(lines)

with open("names.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

**Output:**
```text
characters written on line 1: 6
Alice
Bob
Ravi
Sita
Gita
```

## 9. Appending vs Overwriting

- `"w"` — **wipes** the file first, then writes. Use for a fresh file.
- `"a"` — keeps existing content and writes at the **end**. Use for logs/records.

```python
# Append mode keeps adding without erasing
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("event 1\n")

with open("log.txt", "a", encoding="utf-8") as f:
    f.write("event 2\n")
    f.write("event 3\n")

with open("log.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

**Output:**
```text
event 1
event 2
event 3
```

## 10. Closing Files — and Why It Matters

```python
f = open("data.txt", "w")
f.write("hello")
f.close()          # flushes buffer to disk + releases the OS handle
```

**Why closing matters:**
- Writes are **buffered**; data may not hit disk until `close()` (or flush).
- Open handles are a limited OS resource — leaking them can crash long-running programs.
- On some systems the file stays **locked** until closed.

➡️ The reliable fix is to let Python close it for you with a **context manager** (next section).

## 11. The `with` Context Manager (Recommended)

A **context manager** guarantees the file is closed automatically — even if an error happens
inside the block. This is the standard, professional way to handle files.

**Syntax**
```python
with open(filename, mode) as f:
    # use f here
    ...
# f is automatically closed here (no explicit close needed)
```

**Key Notes:**
- No need to call `close()` — it happens on block exit.
- Safe against exceptions: the file still closes.
- You can open multiple files in one `with` (comma-separated).

```python
# with handles closing for you
with open("greet.txt", "w", encoding="utf-8") as f:
    f.write("written safely")

# Confirm the file is closed after the block
print("closed after block?", f.closed)   # True

# Open two files at once (read from one, write to another)
with open("greet.txt", "r", encoding="utf-8") as src, \
     open("copy.txt", "w", encoding="utf-8") as dst:
    dst.write(src.read())

with open("copy.txt", "r", encoding="utf-8") as f:
    print("copy contains:", f.read())
```

**Output:**
```text
closed after block? True
copy contains: written safely
```

## 12. The File Cursor — `seek()` and `tell()`

A file has a **cursor** (current position, in bytes). Reading/writing moves it.

**Functions:** `tell()`, `seek(offset)`

- `tell()` → current cursor position.
- `seek(0)` → jump back to the **start** (e.g. to re-read a file).

```python
with open("poem.txt", "r", encoding="utf-8") as f:
    print("start position:", f.tell())     # 0
    first = f.readline()
    print("after 1 line :", f.tell())       # moved forward
    f.seek(0)                                # rewind to the beginning
    print("after seek(0):", f.tell())        # 0 again
    print("re-read line 1:", f.readline().strip())
```

**Output:**
```text
start position: 0
after 1 line : 14
after seek(0): 0
re-read line 1: Roses are red
```

## 13. File Methods — Quick Reference (Grouped)

| Group | Methods | Purpose |
|---|---|---|
| **Read** | `read()`, `readline()`, `readlines()` | Pull content out |
| **Write** | `write()`, `writelines()` | Put content in |
| **Navigate** | `seek()`, `tell()` | Move / report cursor |
| **Maintain** | `flush()`, `close()` | Force-save / release |
| **Info** | `.name`, `.mode`, `.closed` | Metadata attributes |

```python
f = open("poem.txt", "r", encoding="utf-8")
print("name  :", f.name)
print("mode  :", f.mode)
print("closed:", f.closed)
f.close()
print("closed:", f.closed)
```

**Output:**
```text
name  : poem.txt
mode  : r
closed: False
closed: True
```

## 14. Checking & Removing Files (`os` module)

Before opening in read mode it is safe to check a file exists. The `os` / `os.path` module helps.

**Functions:** `os.path.exists()`, `os.path.getsize()`, `os.remove()`, `os.rename()`

```python
import os

print("poem.txt exists?", os.path.exists("poem.txt"))
print("size (bytes)    :", os.path.getsize("poem.txt"))

# Rename then remove a throwaway file
with open("temp.txt", "w") as f:
    f.write("delete me")
os.rename("temp.txt", "temp2.txt")
os.remove("temp2.txt")
print("temp2.txt exists after remove?", os.path.exists("temp2.txt"))
```

**Output:**
```text
poem.txt exists? True
size (bytes)    : 47
temp2.txt exists after remove? False
```

## 15. Working With CSV Files

**CSV** (Comma-Separated Values) is the standard for tabular data (spreadsheets, exports). Use the
built-in **`csv`** module instead of splitting strings by hand (it handles commas inside quotes,
newlines, etc.).

**Key Notes:**
- Open CSV files with `newline=""` to avoid blank rows on some systems.
- `csv.writer` writes rows; `csv.reader` reads rows as lists; `csv.DictReader` reads rows as dicts.

```python
import csv

# Write a CSV
with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "marks"])      # header
    writer.writerows([["Alice", 95], ["Bob", 82], ["Ravi", 88]])

# Read it back as rows
with open("students.csv", "r", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        print(row)
```

**Output:**
```text
['name', 'marks']
['Alice', '95']
['Bob', '82']
['Ravi', '88']
```

```python
import csv
# DictReader gives each row as a dictionary keyed by the header
with open("students.csv", "r", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], "->", row["marks"])
```

**Output:**
```text
Alice -> 95
Bob -> 82
Ravi -> 88
```

## 16. Working With JSON Files

**JSON** stores structured data (dicts/lists) as text — the format of most web APIs and config
files. Use the built-in **`json`** module.

**Functions:** `json.dump()` / `json.load()` (files), `json.dumps()` / `json.loads()` (strings)

**Key Notes:**
- `dump`/`load` work with **files**; `dumps`/`loads` (the `s` = string) work with **strings**.
- JSON keys are always strings; Python `dict`/`list` map cleanly to JSON objects/arrays.

```python
import json

data = {"name": "Alice", "marks": [95, 82, 88], "passed": True}

# Write a dict to a JSON file
with open("student.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Read it back into a Python dict
with open("student.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(type(loaded), loaded)
print("average:", sum(loaded["marks"]) / len(loaded["marks"]))
```

**Output:**
```text
<class 'dict'> {'name': 'Alice', 'marks': [95, 82, 88], 'passed': True}
average: 88.33333333333333
```

## 17. Common Mistakes

**1. Opening in `"w"` when you meant `"a"`** — `"w"` silently erases the whole file.

**2. Forgetting to close (without `with`)** — data may not be saved; use `with`.

**3. Reading a file that isn't there in `"r"` mode** — raises `FileNotFoundError`.
```python
# Guard it:
import os
if os.path.exists("maybe.txt"):
    with open("maybe.txt") as f:
        ...
```

**4. Forgetting `\n`** — `write()` does not add line breaks; lines run together.

**5. Reading twice without rewinding** — after `read()`, the cursor is at the end; call
`seek(0)` to read again.

**6. Wrong data type in binary mode** — `"wb"` needs `bytes`, not `str`.

```python
# The safe pattern for the "file might not exist" mistake
import os
target = "maybe.txt"
if os.path.exists(target):
    with open(target) as f:
        print(f.read())
else:
    print(f"'{target}' not found - skipping safely")
```

**Output:**
```text
'maybe.txt' not found - skipping safely
```

## 18. Mini Practical Examples

Real tasks you can do with the tools above.

```python
# 1) Count lines, words and characters in a file (like the Unix 'wc' command)
with open("poem.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
words = text.split()
print("lines     :", len(lines))
print("words     :", len(words))
print("characters:", len(text))
```

**Output:**
```text
lines     : 3
words     : 9
characters: 47
```

```python
# 2) Copy a file
with open("poem.txt", "r", encoding="utf-8") as src, \
     open("poem_backup.txt", "w", encoding="utf-8") as dst:
    dst.write(src.read())

with open("poem_backup.txt", "r", encoding="utf-8") as f:
    print("backup has", len(f.readlines()), "lines")
```

**Output:**
```text
backup has 3 lines
```

```python
# 3) Word frequency from a file
with open("poem.txt", "r", encoding="utf-8") as f:
    words = f.read().lower().split()

freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
print(freq)
```

**Output:**
```text
{'roses': 1, 'are': 2, 'red': 1, 'violets': 1, 'blue': 1, 'python': 1, 'is': 1, 'sweet': 1}
```

```python
# 4) Append log entries, then read them back
def log_event(msg):
    with open("app.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log_event("server started")
log_event("user logged in")
log_event("server stopped")

with open("app.log", "r", encoding="utf-8") as f:
    print(f.read())
```

**Output:**
```text
server started
user logged in
server stopped
```

## 19. Summary

- Files give **persistent** storage on disk; `open()` returns a **file object**.
- Modes: **`r`** read, **`w`** overwrite, **`a`** append, **`x`** exclusive-create; add `+` for
  read+write, `b` for binary.
- Read with `read()` / `readline()` / `readlines()`, or just **loop over the file**.
- Write with `write()` / `writelines()` (add your own `\n`).
- Always prefer the **`with` context manager** — it closes the file automatically and safely.
- `seek()` / `tell()` move and report the cursor.
- Use the **`csv`** and **`json`** modules for structured data.

## 20. Practice Questions

1. Write a program that creates `notes.txt` and writes three lines to it.
2. Read a file and print it line by line with line numbers.
3. Count the number of words in a text file.
4. Copy the contents of one file into another.
5. Append a new line to an existing file without erasing it.
6. Count how many times a given word appears in a file.
7. Read a file, then use `seek(0)` to read it a second time.
8. Write a list of dictionaries to a CSV file and read it back with `DictReader`.
9. Save a Python dictionary to a JSON file and load it again.
10. Write a function `safe_read(path)` that returns the file text, or `"File not found"` if it doesn't exist.
