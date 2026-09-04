# Day 4 - Conditions & Loops
**Topics:** `if`, `if-else`, `if-elif-else`, `match`, `while`, `for`, `break`, `continue`, `pass`, Patterns

## 1. if Statement

```python
age = 20

if age >= 18:
    print("Eligible to Vote")
```

**Output:**
```text
Eligible to Vote
```

```python
num = -5

if num < 0:
    print("Negative Number")
```

**Output:**
```text
Negative Number
```

```python
marks = 82

if marks >= 35:
    print("Pass")
```

**Output:**
```text
Pass
```

## 2. if-else

```python
num = 7

if num % 2 == 0:
    print("Even")
else:
    print("Odd")
```

**Output:**
```text
Odd
```

```python
password = "python"

if password == "python":
    print("Login Successful")
else:
    print("Wrong Password")
```

**Output:**
```text
Login Successful
```

```python
a = 25
b = 18

if a > b:
    print(a)
else:
    print(b)
```

**Output:**
```text
25
```

## 3. if-elif-else

```python
marks = 86

if marks >= 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 50:
    print("Grade C")
else:
    print("Fail")
```

**Output:**
```text
Grade B
```

```python
signal = "yellow"

if signal == "red":
    print("Stop")
elif signal == "yellow":
    print("Ready")
elif signal == "green":
    print("Go")
else:
    print("Invalid Signal")
```

**Output:**
```text
Ready
```

```python
day = 4

if day == 1:
    print("Monday")
elif day == 2:
    print("Tuesday")
elif day == 3:
    print("Wednesday")
elif day == 4:
    print("Thursday")
else:
    print("Other Day")
```

**Output:**
```text
Thursday
```

## 4. Nested if

```python
username = "admin"
password = "1234"

if username == "admin":
    if password == "1234":
        print("Login Successful")
    else:
        print("Wrong Password")
else:
    print("Unknown User")
```

**Output:**
```text
Login Successful
```

```python
balance = 5000
amount = 2500

if balance >= amount:
    if amount > 0:
        print("Transaction Successful")
    else:
        print("Invalid Amount")
else:
    print("Insufficient Balance")
```

**Output:**
```text
Transaction Successful
```

## 5. match-case

```python
day = 2

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case _:
        print("Invalid")
```

**Output:**
```text
Tuesday
```

```python
operator = "*"

match operator:
    case "+":
        print(10 + 5)
    case "-":
        print(10 - 5)
    case "*":
        print(10 * 5)
    case "/":
        print(10 / 5)
    case _:
        print("Invalid Operator")
```

**Output:**
```text
50
```

## 6. while Loop

```python
i = 1

while i <= 5:
    print(i)
    i += 1
```

**Output:**
```text
1
2
3
4
5
```

```python
i = 5

while i >= 1:
    print(i)
    i -= 1
```

**Output:**
```text
5
4
3
2
1
```

```python
i = 1
total = 0

while i <= 10:
    total += i
    i += 1

print(total)
```

**Output:**
```text
55
```

```python
n = 7

i = 1
while i <= 10:
    print(f"{n} x {i} = {n*i}")
    i += 1
```

**Output:**
```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

## 7. for Loop

```python
for i in range(5):
    print(i)
```

**Output:**
```text
0
1
2
3
4
```

```python
for i in range(1, 6):
    print(i)
```

**Output:**
```text
1
2
3
4
5
```

```python
for i in range(2, 11, 2):
    print(i)
```

**Output:**
```text
2
4
6
8
10
```

```python
for ch in "Python":
    print(ch)
```

**Output:**
```text
P
y
t
h
o
n
```

```python
fruits = ["Apple", "Mango", "Orange"]

for fruit in fruits:
    print(fruit)
```

**Output:**
```text
Apple
Mango
Orange
```

## 8. Nested Loops

```python
for i in range(3):
    for j in range(3):
        print(i, j)
```

**Output:**
```text
0 0
0 1
0 2
1 0
1 1
1 2
2 0
2 1
2 2
```

```python
for i in range(3):
    for j in range(3):
        print("*", end=" ")
    print()
```

**Output:**
```text
* * * 
* * * 
* * * 
```

## 9. break

```python
for i in range(10):
    if i == 5:
        break
    print(i)
```

**Output:**
```text
0
1
2
3
4
```

```python
for ch in "Python":
    if ch == "h":
        break
    print(ch)
```

**Output:**
```text
P
y
t
```

## 10. continue

```python
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)
```

**Output:**
```text
1
3
5
7
9
```

```python
for ch in "Python":
    if ch == "o":
        continue
    print(ch)
```

**Output:**
```text
P
y
t
h
n
```

## 11. pass

```python
if True:
    pass

print("Program Continues")
```

**Output:**
```text
Program Continues
```

```python
for i in range(5):
    if i == 3:
        pass
    print(i)
```

**Output:**
```text
0
1
2
3
4
```

## 12. Pattern 1 - Left Half Pyramid

```python
for i in range(5):
    for j in range(i + 1):
        print("*", end="")
    print()
```

**Output:**
```text
*
**
***
****
*****
```

## 13. Pattern 2 - Right Half Pyramid

```python
for i in range(5):
    for j in range(5 - i - 1):
        print(" ", end="")
    for j in range(i + 1):
        print("*", end="")
    print()
```

**Output:**
```text
    *
   **
  ***
 ****
*****
```

## 14. Pattern 3 - Full Pyramid

```python
n = 5

for i in range(n):
    for j in range(n - i - 1):
        print(" ", end="")
    for j in range(2 * i + 1):
        print("*", end="")
    print()
```

**Output:**
```text
    *
   ***
  *****
 *******
*********
```

## Practice Questions

1. Check whether a given year is a leap year.
2. Print the multiplication table of a given number using a `for` loop.
3. Print the sum of numbers from `1` to `n` using a `while` loop.
4. Print all odd numbers from `1` to `100`.
5. Print the following pattern:

```
1
12
123
1234
12345
```
