# 🎬 Vortex Web IDE - Demo Guide

This guide walks you through using the Vortex Web IDE with step-by-step instructions.

---

## 🖥️ Interface Overview

### Main Components

```
┌─────────────────────────────────────────────────────────────┐
│  🌀 Vortex Programming Language    [Compile] [Tokenize] [Clear]│
├──────────┬──────────────────────────────────────────────────┤
│          │  📝 Code Editor                                  │
│ Examples │  ┌────────────────────────────────────────────┐ │
│ Sidebar  │  │ func main() {                              │ │
│          │  │     out("Hello, Vortex!");                 │ │
│ • Hello  │  │     num x = 10;                            │ │
│ • Vars   │  │     out(x);                                │ │
│ • Loops  │  │ }                                          │ │
│ • Funcs  │  └────────────────────────────────────────────┘ │
│ • Lists  │                                                  │
│ • ...    │  ┌────────────────────────────────────────────┐ │
│          │  │ [Result] [Tokens] [Parse Tree]             │ │
│ Quick    │  ├────────────────────────────────────────────┤ │
│ Guide    │  │ ✓ Compilation Successful!                  │ │
│          │  │   Your code has been compiled with no      │ │
│          │  │   errors.                                  │ │
│          │  └────────────────────────────────────────────┘ │
└──────────┴──────────────────────────────────────────────────┘
```

---

## 📖 Step-by-Step Tutorial

### Demo 1: Hello World

**Step 1: Load the Example**
1. Look at the left sidebar
2. Click on "Hello World" example
3. Code appears in the editor:
   ```vortex
   func main() {
       out("Hello, Vortex!");
   }
   ```

**Step 2: Compile**
1. Click the green **"Compile & Run"** button
2. Wait for compilation (< 1 second)
3. See success message in Result tab

**Step 3: View Tokens**
1. Click the **"Tokens"** tab
2. See the generated tokens:
   ```
   KEYWORD('func') at line 1
   IDENTIFIER('main') at line 1
   LEFT_PAREN('(') at line 1
   RIGHT_PAREN(')') at line 1
   LEFT_BRACE('{') at line 1
   KEYWORD('out') at line 2
   LEFT_PAREN('(') at line 2
   STRING_LITERAL('"Hello, Vortex!"') at line 2
   RIGHT_PAREN(')') at line 2
   SEMICOLON(';') at line 2
   RIGHT_BRACE('}') at line 3
   ```

**Step 4: View Parse Tree**
1. Click the **"Parse Tree"** tab
2. See parsing results:
   ```
   Parsing started...
   Parsing finished.
   No syntax errors detected.
   ```

---

### Demo 2: Variables and Types

**Step 1: Load Example**
Click "Variables & Types" in sidebar

**Code:**
```vortex
func main() {
    num age = 25;
    str name = "Ali";
    bool isActive = yes;
    const num PI = 3.14;
    
    out("Name: " + name);
    out("Age: " + age);
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ All variable declarations recognized
- ✅ Type keywords (num, str, bool, const) tokenized
- ✅ String concatenation parsed correctly
- ✅ No syntax errors

**Learning Points:**
- Vortex has 4 basic types: num, str, bool, list
- Use `const` for constants
- Boolean values are `yes` and `no` (not true/false)

---

### Demo 3: Conditionals

**Step 1: Load Example**
Click "Conditionals" in sidebar

**Code:**
```vortex
func checkValue(num x) {
    when (x > 5) {
        out("High");
    }
    whenelse (x > 2) {
        out("Medium");
    }
    else {
        out("Low");
    }
}

func main() {
    checkValue(7);
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ `when` keyword (like `if`)
- ✅ `whenelse` keyword (like `elif`)
- ✅ `else` keyword
- ✅ Nested blocks parsed correctly

**Learning Points:**
- Vortex uses `when` instead of `if`
- Use `whenelse` for else-if conditions
- Conditions must be in parentheses

---

### Demo 4: Loops

**Step 1: Load Example**
Click "Loops" in sidebar

**Code:**
```vortex
func main() {
    ## Repeat loop (for loop)
    repeat (num i = 0; i < 5; i += 1) {
        out(i);
    }
    
    ## Cycle loop (while loop)
    num x = 0;
    cycle (x < 3) {
        out(x);
        x += 1;
    }
    
    ## Perform-cycle (do-while)
    num y = 3;
    perform {
        out(y);
        y -= 1;
    } cycle (y > 0);
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ Three types of loops recognized
- ✅ Comments (##) ignored properly
- ✅ Loop syntax validated

**Learning Points:**
- `repeat` = for loop
- `cycle` = while loop
- `perform...cycle` = do-while loop
- Comments start with `##`

---

### Demo 5: Functions

**Step 1: Load Example**
Click "Functions" in sidebar

**Code:**
```vortex
func add(num a, num b) -> num {
    give a + b;
}

func greet(str name = "Guest") {
    out("Hello, " + name);
}

func main() {
    num result = add(5, 3);
    out(result);
    
    greet("Ali");
    greet();
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ Function with return type (`-> num`)
- ✅ Default parameters (`name = "Guest"`)
- ✅ `give` keyword (like `return`)
- ✅ Function calls with and without arguments

**Learning Points:**
- Use `->` to specify return type
- Use `give` to return values
- Default parameters are supported
- Functions must be defined before `main()`

---

### Demo 6: Lists

**Step 1: Load Example**
Click "Lists" in sidebar

**Code:**
```vortex
func main() {
    list nums = [1, 2, 3, 4, 5];
    list names = ["Ali", "Sara", "Ahmed"];
    
    out(nums[0]);
    out(names[1]);
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ List declarations
- ✅ Array indexing with `[0]`
- ✅ Mixed content types

**Learning Points:**
- Lists use square brackets `[]`
- Access elements with index `[0]`
- Lists can contain numbers or strings

---

### Demo 7: Objects

**Step 1: Load Example**
Click "Objects" in sidebar

**Code:**
```vortex
func main() {
    list people = [
        {str name -> "Ali", num age -> 22},
        {str name -> "Sara", num age -> 23},
        {str name -> "Ahmed", num age -> 25}
    ];
    
    out("People list created");
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ Object syntax with `{}`
- ✅ Property syntax: `type name -> value`
- ✅ List of objects

**Learning Points:**
- Objects use curly braces `{}`
- Properties need type declarations
- Use `->` (not `=` or `=>`) for property values
- Can create lists of objects

---

### Demo 8: Error Handling

**Step 1: Load Example**
Click "Error Handling" in sidebar

**Code:**
```vortex
func main() {
    try {
        num x = 5 / 0;
        out(x);
    } catch (err) {
        out("Error occurred!");
    }
}
```

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
- ✅ `try` block recognized
- ✅ `catch` block with error variable
- ✅ Exception handling syntax validated

**Learning Points:**
- Use `try-catch` for error handling
- Catch block needs error variable name
- Similar to Java/JavaScript syntax

---

### Demo 9: Intentional Error

**Step 1: Write Bad Code**
Type this in the editor:
```vortex
func main() {
    num x = 10
    out(x);
}
```
(Notice: missing semicolon after `num x = 10`)

**Step 2: Compile**
Click "Compile & Run"

**What You'll See:**
```
❌ Compilation Failed
Expected SEMICOLON, found KEYWORD('out') at line 3
```

**Step 3: Fix the Error**
Add semicolon:
```vortex
func main() {
    num x = 10;
    out(x);
}
```

**Step 4: Recompile**
Click "Compile & Run" again
✅ Success!

**Learning Points:**
- Error messages show line numbers
- Clear indication of what's expected
- Easy to fix and retry

---

## 🎯 Advanced Features Demo

### Demo 10: Complex Nested Program

**Code:**
```vortex
func factorial(num n) -> num {
    when (n <= 1) {
        give 1;
    }
    give n * factorial(n - 1);
}

func main() {
    num result = factorial(5);
    out("Factorial: " + result);
    
    repeat (num i = 1; i <= 5; i += 1) {
        when (i == 3) {
            skip;
        }
        out("Number: " + i);
    }
}
```

**Features Demonstrated:**
- ✅ Recursive functions
- ✅ Nested conditionals
- ✅ Loop with skip statement
- ✅ String concatenation
- ✅ Multiple function definitions

---

## 🔍 Exploring Tokens

### Understanding Token Output

When you click "Tokenize Only" or view the Tokens tab, you see:

```
KEYWORD('func') at line 1
IDENTIFIER('main') at line 1
LEFT_PAREN('(') at line 1
RIGHT_PAREN(')') at line 1
LEFT_BRACE('{') at line 1
...
```

**Token Types:**
- `KEYWORD` - Reserved words (func, num, when, etc.)
- `IDENTIFIER` - Variable/function names
- `NUMBER_LITERAL` - Numbers (10, 3.14)
- `STRING_LITERAL` - Strings ("Hello")
- `BOOLEAN_LITERAL` - yes/no
- `OPERATOR` - +, -, *, /, =, etc.
- `LEFT_BRACE`, `RIGHT_BRACE` - { }
- `LEFT_PAREN`, `RIGHT_PAREN` - ( )
- `LEFT_BRACKET`, `RIGHT_BRACKET` - [ ]
- `SEMICOLON`, `COLON`, `COMMA` - ; : ,

---

## 🎨 UI Features

### Button Functions

**🟢 Compile & Run**
- Full compilation (tokenization + parsing)
- Shows all results
- Best for checking complete code

**🔵 Tokenize Only**
- Shows only tokens
- Faster than full compile
- Good for learning tokenization

**🔴 Clear**
- Clears the editor
- Resets all output
- Confirms before clearing

### Tab Navigation

**Result Tab**
- Shows compilation status
- Success or error messages
- Compilation details

**Tokens Tab**
- Lists all generated tokens
- Shows token types and line numbers
- Useful for understanding lexical analysis

**Parse Tree Tab**
- Shows parsing output
- Syntax validation results
- Error messages if any

---

## 💡 Tips & Tricks

### 1. Quick Testing
- Use examples as templates
- Modify small parts to experiment
- Compile frequently to catch errors early

### 2. Learning Tokens
- Click "Tokenize Only" to see just tokens
- Compare token output with your code
- Understand how code becomes tokens

### 3. Understanding Errors
- Read error messages carefully
- Note the line number
- Check for missing semicolons, brackets

### 4. Keyboard Shortcuts
- `Ctrl+A` - Select all
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo

### 5. Code Organization
- Define functions before main()
- Use comments (##) to organize
- Keep consistent indentation

---

## 🎓 Learning Path

### Beginner (Start Here)
1. Hello World
2. Variables & Types
3. Input/Output
4. Conditionals

### Intermediate
5. Loops
6. Functions
7. Lists
8. Select-Case

### Advanced
9. Objects
10. Error Handling
11. Complex nested structures
12. Recursive functions

---

## 🐛 Common Mistakes

### 1. Missing Semicolon
```vortex
❌ num x = 10
✅ num x = 10;
```

### 2. Wrong Boolean Values
```vortex
❌ bool flag = true;
✅ bool flag = yes;
```

### 3. Wrong Conditional Keyword
```vortex
❌ if (x > 5) { }
✅ when (x > 5) { }
```

### 4. Wrong Return Keyword
```vortex
❌ return x + y;
✅ give x + y;
```

### 5. Wrong Object Syntax
```vortex
❌ {name: "Ali"}
❌ {name => "Ali"}
✅ {str name -> "Ali"}
```

---

## 🎬 Demo Scenarios

### Scenario 1: Teaching a Class
1. Open IDE on projector
2. Start with Hello World
3. Show token generation
4. Explain each token type
5. Progress through examples
6. Introduce errors intentionally
7. Show how to fix them

### Scenario 2: Self-Learning
1. Read QUICK_START.md
2. Try each example in order
3. Modify examples slightly
4. Create your own programs
5. Experiment with errors
6. Read VORTEX_ANALYSIS.md for details

### Scenario 3: Code Review
1. Write a program
2. Compile and check tokens
3. Verify parse tree
4. Share URL with others on network
5. Discuss code structure

---

## 📱 Mobile Usage

The IDE works on mobile devices!

**Tips for Mobile:**
- Use landscape mode for better view
- Tap examples to load them
- Pinch to zoom if needed
- Use on-screen keyboard
- Buttons are touch-friendly

---

## 🌐 Network Sharing

**Share with Others:**
1. Find your IP address
2. Share: `http://YOUR_IP:5000`
3. Others can access on same network
4. Great for classroom settings

**Example:**
```
Your computer: 192.168.1.100
Share URL: http://192.168.1.100:5000
```

---

## 🎉 Conclusion

You now know how to:
- ✅ Use the Vortex Web IDE
- ✅ Write Vortex programs
- ✅ Compile and view results
- ✅ Understand tokens and parsing
- ✅ Fix common errors
- ✅ Explore all language features

**Next Steps:**
1. Try all examples
2. Create your own programs
3. Read VORTEX_ANALYSIS.md
4. Share with friends
5. Experiment and learn!

---

**Happy Coding with Vortex! 🌀**

Need help? Check:
- `QUICK_START.md` - Quick setup
- `SETUP_GUIDE.md` - Detailed guide
- `VORTEX_ANALYSIS.md` - Language reference
