1. Install Python

* Download from https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe
* **Check**: ✅ "Add Python to PATH"
* Click **Install Now**

2. Open Command Prompt (or PowerShell)

3. Go to your project
1. create a folder in the desktop and go to inside folder
2. oepn folder in **Command Prompt:**.


4. Create a virtual environment

```cmd
python -m venv .venv
```

5. Activate it


```cmd
.venv\Scripts\activate
```


6. Install Jupyter

```cmd
pip install -U pip jupyterlab notebook ipykernel
```

7. Register the environment as a Jupyter kernel

```cmd
python -m ipykernel install --user --name=.venv --display-name="Python (.venv)"
```

8. Open JupyterLab

```cmd
jupyter lab
```

9. Create a notebook

* Click **Python (.venv)**
* Start coding.

---

```python
for i in range(3):
    print(i)
```

**Output:**
```text
0
1
2
```

You can structure the demo in about 20–30 minutes like this.

**1. Introduction (2–3 min)**

> Python is a very easy language to learn because it provides many built-in functions that solve common problems for us. Instead of writing everything from scratch, we use these functions effectively.

> A function is simply a reusable piece of code. To understand any function, you only need to know three things:
>
> * What input does it take?
> * What does it do?
> * What output does it return?
>
> Once you understand these three, you can learn almost any Python function.

Example:

```python
name = "python"

print(len(name))
```

Ask:

* Input? → `"python"`
* Function? → `len()`
* Output? → `6`

Then say:

> Today we'll learn loops, one of the most useful concepts in programming.

---

```python
len("Python")          # str
len([1, 2, 3])         # list
len((1, 2, 3))         # tuple
len({"a": 1, "b": 2})  # dict
len({1, 2, 3})         # set
len(range(10))         # range
```

```python
type(len("python"))
```

**Output:**
```text
int
```



**2. Why loops? (2 min)**

Without loops:

```python
print("Tree")
print("Tree")
print("Tree")
print("Tree")
print("Tree")
```

With a loop:

```python
for i in range(5):
    print("Tree")
```

Ask:

> Which one is easier?

---

**3. For Loop (10 min)**

Simple loop

```python
for i in range(5):
    print(i)
```

Output

```
0
1
2
3
4
```

Explain:

* `range(5)` gives numbers from 0 to 4.

---

Different types of `range()`

```python
for i in range(1, 6):
    print(i)
```

Output

```
1
2
3
4
5
```

---

Step value

```python
for i in range(2, 11, 2):
    print(i)
```

Output

```
2
4
6
8
10
```

---

Reverse loop

```python
for i in range(10, 0, -1):
    print(i)
```

Output

```
10
9
8
7
6
5
4
3
2
1
```

---

Loop through a string

```python
tree = "Mango"

for letter in tree:
    print(letter)
```

---

Loop through a list

```python
fruits = ["Apple", "Mango", "Orange"]

for fruit in fruits:
    print(fruit)
```

---

Nested loop

```python
for i in range(3):
    for j in range(2):
        print(i, j)
```

---

**4. While Loop (8 min)**

Basic

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

Explain:

> A `for` loop usually repeats a known number of times. A `while` loop repeats until a condition becomes false.

---

Infinite loop

```python
while True:
    print("Running...")
```

Explain:

> This never stops unless we use `break` or interrupt the program.

---

User input

```python
password = ""

while password != "python":
    password = input("Enter password: ")

print("Correct!")
```

---

**5. Loop Control Statements (Very Important)**

`break`

```python
for i in range(10):
    if i == 5:
        break
    print(i)
```

Stops the loop immediately.

---

`continue`

```python
for i in range(6):
    if i == 3:
        continue
    print(i)
```

Skips only one iteration.


---

**6. Quick Comparison**

| for                            | while                        |
| ------------------------------ | ---------------------------- |
| Known number of iterations     | Unknown number of iterations |
| Uses `range()`, lists, strings | Uses a condition             |
| Simpler                        | More flexible                |

---

**7. Practice Questions**

1.

```python
Print numbers from 1 to 20.
```

2.

```python
Print even numbers from 2 to 20.
```

3.

```python
Print your name 10 times.
```

4.

```python
Print all characters of "Python".
```

5.

```python
Count from 10 to 1.
```

6.

```python
Keep asking for a password until the user enters "admin".
```

---

**Closing (1 min)**

> Today you learned how to repeat work automatically using loops. Almost every real-world Python program uses loops, whether you're processing files, reading data, building AI models, or creating web applications. Mastering loops is one of the biggest steps toward becoming a Python programmer.
