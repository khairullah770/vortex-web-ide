# Vortex Web IDE - Complete Setup Guide

This guide will help you set up and run the Vortex Programming Language Web IDE on your system.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.7+** installed ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package manager - usually comes with Python)
- **Git** (optional, for cloning repositories)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Verify Directory Structure

Your directory structure should look like this:

```
parent-folder/
├── Vortex-Programming-Language/
│   └── python_parser/
│       ├── vortex_tokenizer.py
│       └── vortex_parser.py
└── vortex-web-ide/
    ├── app.py
    ├── templates/
    └── requirements.txt
```

### Step 2: Install Dependencies

**Windows:**
```bash
cd vortex-web-ide
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd vortex-web-ide
pip3 install -r requirements.txt
```

### Step 3: Run the Application

**Windows:**
```bash
start.bat
```
Or manually:
```bash
python app.py
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```
Or manually:
```bash
python3 app.py
```

### Step 4: Open in Browser

Navigate to: **http://localhost:5000**

---

## 🔧 Detailed Installation

### Option 1: Using Startup Scripts (Recommended)

#### Windows
1. Double-click `start.bat`
2. The script will:
   - Check Python installation
   - Install dependencies
   - Start the server
3. Browser will show the IDE at `http://localhost:5000`

#### macOS/Linux
1. Open terminal in `vortex-web-ide` directory
2. Make script executable:
   ```bash
   chmod +x start.sh
   ```
3. Run the script:
   ```bash
   ./start.sh
   ```
4. Open browser at `http://localhost:5000`

### Option 2: Manual Installation

1. **Install Python Dependencies:**
   ```bash
   pip install Flask==3.0.0 Werkzeug==3.0.1
   ```

2. **Verify Vortex Parser Location:**
   ```bash
   # From vortex-web-ide directory
   ls ../Vortex-Programming-Language/python_parser/
   ```
   Should show: `vortex_tokenizer.py` and `vortex_parser.py`

3. **Start the Server:**
   ```bash
   python app.py
   ```

4. **Access the IDE:**
   Open `http://localhost:5000` in your browser

### Option 3: Using Docker

1. **Build the Docker image:**
   ```bash
   docker-compose build
   ```

2. **Run the container:**
   ```bash
   docker-compose up
   ```

3. **Access the IDE:**
   Open `http://localhost:5000` in your browser

4. **Stop the container:**
   ```bash
   docker-compose down
   ```

---

## 🌐 Network Access

### Access from Other Devices on Your Network

1. **Find your IP address:**

   **Windows:**
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address"

   **macOS/Linux:**
   ```bash
   ifconfig
   # or
   hostname -I
   ```

2. **Access from other devices:**
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

### Change Port

Edit `app.py` and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

---

## 🎯 Using the IDE

### 1. Writing Code

- Type directly in the code editor
- Use syntax highlighting for better readability
- Code is auto-saved in the browser

### 2. Loading Examples

- Click any example in the left sidebar
- Examples cover all Vortex language features
- Modify examples to learn

### 3. Compiling Code

**Compile & Run Button:**
- Performs full compilation (tokenization + parsing)
- Shows success/error messages
- Displays tokens and parse tree

**Tokenize Only Button:**
- Shows only lexical analysis
- Useful for understanding token generation
- Faster than full compilation

**Clear Button:**
- Clears the editor
- Resets all output panels

### 4. Viewing Results

Switch between tabs:
- **Result**: Compilation status and errors
- **Tokens**: All generated tokens with line numbers
- **Parse Tree**: Syntax validation results

---

## 🐛 Troubleshooting

### Problem: "Module 'flask' not found"

**Solution:**
```bash
pip install Flask
# or
pip3 install Flask
```

### Problem: "Port 5000 already in use"

**Solution 1 - Kill the process:**

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Solution 2 - Use different port:**
Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Problem: "Vortex parser not found"

**Solution:**
Ensure directory structure is correct:
```
parent-folder/
├── Vortex-Programming-Language/
│   └── python_parser/
└── vortex-web-ide/
```

If different, update the path in `app.py`:
```python
VORTEX_PARSER_DIR = Path(__file__).parent.parent / "Vortex-Programming-Language" / "python_parser"
```

### Problem: "Permission denied" on Linux/macOS

**Solution:**
```bash
chmod +x start.sh
```

### Problem: Browser shows "Connection refused"

**Solution:**
1. Check if server is running
2. Verify the URL: `http://localhost:5000`
3. Check firewall settings
4. Try `http://127.0.0.1:5000`

### Problem: Code doesn't compile

**Solution:**
1. Check Vortex syntax in examples
2. Look at error messages in Result tab
3. Verify all statements end with `;`
4. Check bracket matching `{ }`, `( )`, `[ ]`

---

## 🔒 Security Considerations

### For Local Use
- Default configuration is safe for local development
- Server binds to `0.0.0.0` (all interfaces)

### For Public Deployment
1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Add authentication** (if needed)

3. **Use HTTPS** with a reverse proxy (nginx/Apache)

4. **Set up firewall rules**

5. **Disable debug mode** in `app.py`:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

---

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 1 GHz processor
- **RAM**: 512 MB
- **Storage**: 100 MB free space
- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distro)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Recommended Requirements
- **CPU**: 2 GHz dual-core processor
- **RAM**: 2 GB
- **Storage**: 500 MB free space
- **Browser**: Latest version of Chrome, Firefox, or Edge

---

## 🎓 Learning Resources

### Vortex Language Syntax

**Basic Program:**
```vortex
func main() {
    out("Hello, Vortex!");
}
```

**Variables:**
```vortex
num age = 25;
str name = "Ali";
bool isActive = yes;
const num PI = 3.14;
```

**Functions:**
```vortex
func add(num a, num b) -> num {
    give a + b;
}
```

**Conditionals:**
```vortex
when (x > 5) {
    out("High");
}
whenelse (x > 2) {
    out("Medium");
}
else {
    out("Low");
}
```

**Loops:**
```vortex
repeat (num i = 0; i < 5; i += 1) {
    out(i);
}
```

### Documentation
- See `VORTEX_ANALYSIS.md` for complete language reference
- Check examples in the IDE sidebar
- Read the original repository README

---

## 🚀 Advanced Configuration

### Custom Themes

Edit `templates/index.html` and change CodeMirror theme:
```javascript
const editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
    theme: 'dracula',  // Change from 'monokai' to other themes
    // ... other options
});
```

Available themes: monokai, dracula, material, solarized, etc.

### Add More Examples

Edit `app.py` and add to the `get_examples()` function:
```python
'my_example': {
    'name': 'My Example',
    'code': '''func main() {
    out("My custom example");
}'''
}
```

### Increase Timeout

Edit `app.py` and change timeout value:
```python
subprocess.run(
    [...],
    timeout=10  # Change from 5 to 10 seconds
)
```

---

## 📞 Support

### Getting Help

1. **Check this guide** for common issues
2. **Review error messages** in the Result tab
3. **Check browser console** (F12) for JavaScript errors
4. **Verify Python version**: `python --version`
5. **Check Flask installation**: `pip show Flask`

### Reporting Issues

When reporting issues, include:
- Operating system and version
- Python version
- Error messages (full text)
- Steps to reproduce
- Browser and version

---

## 🎉 Success Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Directory structure correct
- [ ] Server starts without errors
- [ ] Browser opens at `http://localhost:5000`
- [ ] Can load examples
- [ ] Can compile code
- [ ] Can see tokens and parse results

---

## 📝 Next Steps

1. **Try all examples** to understand Vortex syntax
2. **Write your own programs** using the language features
3. **Experiment with errors** to understand error messages
4. **Share with others** on your network
5. **Customize the IDE** to your preferences

---

**Happy Coding with Vortex! 🌀**

For more information, visit the [Vortex Programming Language Repository](https://github.com/khairullah770/Vortex-Programming-Language)
