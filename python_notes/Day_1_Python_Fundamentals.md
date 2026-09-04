# Day 1 – Python Programming Fundamentals

## Agenda
1. What is Programming?
2. Programming Languages
3. Compiled vs Interpreted Languages
4. Python Architecture
5. Installing Python
6. Virtual Environment
7. Installing JupyterLab
8. First Program
9. Understanding Functions

# before all what are subjects we have in whole cse with ai&ml

| Subject                                          | Main Core Concepts                                                                                                                                                    |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Computer Organization and Architecture (COA)** | CPU, ALU, Registers, Instruction Set Architecture (ISA), Number Systems, Memory Hierarchy, Cache Memory, Pipelining, Input/Output Organization, Assembly Language     |
| **Operating Systems (OS)**                       | Processes, Threads, CPU Scheduling, Process Synchronization, Deadlocks, Memory Management, Virtual Memory, File Systems, System Calls, Operating System Architecture  |
| **Theory of Computation (TOC)**                  | Finite Automata, Regular Expressions, Context-Free Grammar (CFG), Pushdown Automata (PDA), Turing Machines, Decidability, Computability                               |
| **Compiler Design (CD)**                         | Lexical Analysis, Syntax Analysis (Parsing), Semantic Analysis, Intermediate Code Generation, Code Optimization, Target Code Generation, Symbol Table, Error Handling |
| **Computer Networks (CN)**                       | OSI Model, TCP/IP Model, IP Addressing, Routing, Switching, DNS, HTTP/HTTPS, TCP, UDP, Network Security                                                               |
| **Database Management Systems (DBMS)**           | Database Design, ER Model, Relational Model, SQL, Normalization, Transactions, ACID Properties, Indexing, Joins, Concurrency Control, Recovery                        |

---

## What is Programming?

Programming is the process of giving instructions to a computer to solve a problem.

## Programming Languages
- Low-level
- High-level

Examples: C, C++, Java, Python, JavaScript

## Compiled vs Interpreted

Compiled: C, C++, Go

Interpreted: Python, JavaScript

Python compiles to bytecode and runs on the Python Virtual Machine (PVM).

## Python Execution Flow

Python Code (.py) → Bytecode (.pyc) → Python Virtual Machine → Output

- python -m py_compile tyu.py
- find . -name "tyu*.pyc"

For a Python virtual environment (`.venv`), the main folders are:

| Folder/File    | Purpose                                                                                                                                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bin/**       | Contains the executables for the virtual environment, such as `python`, `pip`, `jupyter`, and the activation scripts (`activate`, `Activate.ps1`). This is the folder you use most often.                      |
| **lib/**       | Stores the installed Python packages (`site-packages`) and the Python standard library files used by the virtual environment.                                                                                  |
| **include/**   | Contains C/C++ header files needed when compiling Python extensions or native modules. Usually empty unless building packages with C extensions.                                                               |
| **etc/**       | Stores configuration files for some installed tools. For example, Jupyter configuration may be placed here.                                                                                                    |
| **share/**     | Contains shared resources such as documentation, icons, schemas, templates, localization files, and Jupyter assets.                                                                                            |
| **lib64/**     | On 64-bit Linux, this usually points to `lib/` (often as a symbolic link). It exists for compatibility with software expecting a `lib64` directory.                                                            |
| **pyvenv.cfg** | The configuration file for the virtual environment. It records information such as the base Python installation, whether system packages are available, and the Python version used to create the environment. |

Inside **`bin/`**, you'll commonly see:

| File            | Purpose                                                 |
| --------------- | ------------------------------------------------------- |
| `python`        | Python interpreter for this virtual environment.        |
| `pip`           | Installs and manages Python packages.                   |
| `activate`      | Activates the virtual environment in Bash/Zsh.          |
| `Activate.ps1`  | Activates the virtual environment in PowerShell.        |
| `activate.fish` | Activation script for the Fish shell.                   |
| `activate.csh`  | Activation script for C Shell (`csh`/`tcsh`).           |
| `jupyter`       | Starts Jupyter.                                         |
| `jupyter-lab`   | Starts JupyterLab.                                      |
| `ipython`       | Starts the enhanced interactive Python shell (IPython). |

A simple way to explain it to students is:

```text
.venv/
├── bin/          → Programs & commands
├── lib/          → Installed Python libraries
├── include/      → C/C++ header files
├── etc/          → Configuration files
├── share/        → Shared resources
├── lib64/        → 64-bit library link
└── pyvenv.cfg    → Virtual environment configuration
```

This mental model is usually enough for beginners.

---

| Command                 | Purpose                             |
| ----------------------- | ----------------------------------- |
| `pwd`                   | Show the current working directory. |
| `ls`                    | List all files and folders.         |
| `cd folder_name`        | Change to another directory.        |
| `mkdir folder_name`     | Create a new folder.                |
| `touch file.py`         | Create an empty file (Linux/macOS). |
| `cp source destination` | Copy a file or folder.              |
| `mv old_name new_name`  | Move or rename a file/folder.       |
| `rm file.py`            | Delete a file.                      |
| `clear`                 | Clear the terminal screen.          |
| `history`               | Show previously executed commands.  |

---

Use these steps for **Windows**.

---

## Step 1: Download Python

* Open your browser.
* Go to **[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)**
* Click **Download Python 3.x.x**.

---

## Step 2: Run the Installer

Double-click the downloaded `.exe` file.

### Very Important

Before clicking **Install Now**, check:

✅ **Add Python to PATH**

This allows you to run Python from Command Prompt.

Then click:

**Install Now**

Wait until installation completes.

---

## Step 3: Verify Installation

Open **Command Prompt** (`Win + R` → `cmd`).

Run:

```cmd
python --version
```

Example:

```text
Python 3.14.0
```

Also verify `pip`:

```cmd
pip --version
```

Example:

```text
pip 25.x.x
```

---

## Step 4: Create a Project Folder

```cmd
mkdir PythonCourse
cd PythonCourse
```

---

## Step 5: Create a Virtual Environment

```cmd
python -m venv .venv
```

You should now see:

```text
PythonCourse
│
├── .venv
```

---

## Step 6: Activate the Virtual Environment

### Command Prompt

```cmd
.venv\Scripts\activate
```

### PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

If successful, you'll see:

```text
(.venv) C:\Users\YourName\PythonCourse>
```

---

## Step 7: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

---

## Step 8: Install Jupyter

```cmd
pip install jupyterlab notebook ipykernel
```

---

## Step 9: Register the Environment

```cmd
python -m ipykernel install --user --name=.venv --display-name="Python (.venv)"
```

---

## Step 10: Start JupyterLab

```cmd
jupyter lab
```

Your browser will automatically open JupyterLab.

---

## Step 11: Create Your First Notebook

* Click **Python (.venv)**.
* Rename the notebook.
* Start writing Python code.

---

## Step 12: Close Everything

Stop Jupyter:

Press:

```text
Ctrl + C
```

Then deactivate the virtual environment:

```cmd
deactivate
```

---

### Folder Structure

```text
PythonCourse/
│
├── .venv/
│   ├── Scripts/
│   ├── Lib/
│   ├── Include/
│   └── pyvenv.cfg
│
└── your_file.py
```

This workflow is the standard setup used for Python development on Windows.

---

## Useful Jupyter Shortcuts
- Shift+Enter : Run Cell
- Tab : Auto Complete
- Shift+Tab : Function Signature
- function? : Documentation
- function?? : Source (if available)

```python
print('Hello, World!')
```

## Understanding Functions
For every function ask:
1. Input?
2. Logic?
3. Output?

```python
name='Python'
print(len(name))
print(type(len(name)))
```

## Homework
- Install Python
- Install Jupyter
- Create a virtual environment
- Run your first notebook
- Practice print(), len(), type()
