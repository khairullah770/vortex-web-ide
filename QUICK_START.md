# 🚀 Vortex Web IDE - Quick Start

Get up and running in 2 minutes!

---

## ⚡ Super Quick Start

### Windows Users

1. **Open Command Prompt** in the `vortex-web-ide` folder
2. **Run:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
3. **Open browser:** http://localhost:5000

### Mac/Linux Users

1. **Open Terminal** in the `vortex-web-ide` folder
2. **Run:**
   ```bash
   pip3 install -r requirements.txt
   python3 app.py
   ```
3. **Open browser:** http://localhost:5000

---

## 📁 Before You Start

Make sure your folders look like this:

```
📁 Your Project Folder
├── 📁 Vortex-Programming-Language
│   └── 📁 python_parser
│       ├── vortex_tokenizer.py
│       └── vortex_parser.py
└── 📁 vortex-web-ide
    ├── app.py
    ├── requirements.txt
    └── 📁 templates
```

---

## 🎯 First Time Setup

### Step 1: Install Python
- Download from: https://www.python.org/downloads/
- Version 3.7 or higher
- ✅ Check "Add Python to PATH" during installation

### Step 2: Install Dependencies
```bash
cd vortex-web-ide
pip install -r requirements.txt
```

### Step 3: Start Server
```bash
python app.py
```

### Step 4: Open Browser
Go to: **http://localhost:5000**

---

## 🎨 Using the IDE

### 1️⃣ Write Code
- Type in the editor
- Or click an example from the sidebar

### 2️⃣ Compile
- Click **"Compile & Run"** button
- See results in the tabs below

### 3️⃣ View Results
- **Result Tab**: Success or error messages
- **Tokens Tab**: Lexical analysis
- **Parse Tree Tab**: Syntax validation

---

## 📝 Your First Program

Try this:

```vortex
func main() {
    out("Hello, Vortex!");
    
    num x = 10;
    num y = 20;
    num sum = x + y;
    
    out("Sum: " + sum);
}
```

Click **"Compile & Run"** and see the magic! ✨

---

## 🆘 Common Issues

### "Module not found"
```bash
pip install Flask
```

### "Port already in use"
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### "Parser not found"
Check that `Vortex-Programming-Language` folder is next to `vortex-web-ide`

---

## 🎓 Learn More

- **Full Setup Guide**: See `SETUP_GUIDE.md`
- **Language Reference**: See `../VORTEX_ANALYSIS.md`
- **Examples**: Click examples in the IDE sidebar

---

## 🌟 Features

✅ Syntax-highlighted editor
✅ Real-time compilation
✅ Token visualization
✅ Parse tree display
✅ 10+ example programs
✅ Error reporting with line numbers
✅ Responsive design
✅ No installation of Vortex compiler needed!

---

**That's it! Start coding in Vortex! 🌀**

Need help? Check `SETUP_GUIDE.md` for detailed instructions.
