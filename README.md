# Vortex Programming Language - Web IDE

A modern, interactive web-based IDE for writing, compiling, and running Vortex programming language code.

## 🌟 Features

- **Code Editor**: Syntax-highlighted code editor powered by CodeMirror
- **Real-time Compilation**: Tokenize and parse Vortex code instantly
- **Multiple Views**: 
  - Result view showing compilation status
  - Tokens view displaying lexical analysis
  - Parse Tree view showing syntactic analysis
- **Example Programs**: Pre-loaded examples covering all Vortex features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Error Reporting**: Clear error messages with line numbers

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
vortex-web-ide/
├── app.py                  # Flask backend server
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main web interface
└── README.md              # This file
```

## 🎯 Usage

### Writing Code

1. Use the code editor to write your Vortex program
2. Or select an example from the sidebar to get started

### Compiling

- **Compile & Run**: Full compilation (tokenization + parsing)
- **Tokenize Only**: View just the lexical analysis
- **Clear**: Reset the editor

### Viewing Results

Switch between tabs to see:
- **Result**: Compilation success/failure status
- **Tokens**: List of all tokens generated
- **Parse Tree**: Parsing output and syntax validation

## 🔧 API Endpoints

### `GET /`
Returns the main web interface

### `POST /compile`
Compiles Vortex code

**Request:**
```json
{
  "code": "func main() { out(\"Hello\"); }"
}
```

**Response:**
```json
{
  "success": true,
  "stage": "complete",
  "tokens": "KEYWORD('func') at line 1\n...",
  "parseResult": "Parsing started...\nNo syntax errors detected.",
  "message": "Compilation successful!"
}
```

### `GET /examples`
Returns all example programs

**Response:**
```json
{
  "hello_world": {
    "name": "Hello World",
    "code": "func main() { ... }"
  },
  ...
}
```

## 🎨 Features Showcase

### Supported Vortex Features

1. ✅ Function definitions with return types
2. ✅ Default parameters
3. ✅ Variable declarations (num, str, bool, list, const)
4. ✅ Input/Output operations
5. ✅ Conditional statements (when/whenelse/else)
6. ✅ Loops (repeat, cycle, perform-cycle)
7. ✅ Control flow (break, skip)
8. ✅ Switch statements (select-case-default)
9. ✅ Error handling (try-catch)
10. ✅ Lists and objects
11. ✅ Nested structures

## 🛠️ Development

### Running in Development Mode

```bash
python app.py
```

The server will start on `http://localhost:5000` with debug mode enabled.

### Customization

- **Port**: Change `port=5000` in `app.py`
- **Theme**: Modify CodeMirror theme in `index.html`
- **Examples**: Add more examples in the `/examples` endpoint

## 🔒 Security Notes

- Code execution is sandboxed (tokenization and parsing only)
- No actual code execution on the server
- Timeout protection (5 seconds max)
- Temporary files are automatically cleaned up

## 📝 Example Programs Included

1. **Hello World** - Basic output
2. **Variables & Types** - Data type declarations
3. **Conditionals** - when/whenelse/else statements
4. **Loops** - repeat, cycle, perform-cycle
5. **Functions** - Function definitions and calls
6. **Lists** - List operations
7. **Objects** - Object handling
8. **Select-Case** - Switch statements
9. **Error Handling** - try-catch blocks
10. **Complex Example** - Advanced features

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py or kill the process using port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Vortex Parser Not Found
Ensure the `Vortex-Programming-Language` directory is in the parent directory of `vortex-web-ide`.

## 🚀 Deployment

### Local Network Access

```bash
python app.py
# Access from other devices: http://YOUR_IP:5000
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📄 License

This project is part of the Vortex Programming Language educational initiative.

## 👥 Authors

- Khairullah
- Qasim

## 🔗 Links

- [Vortex Language Repository](https://github.com/khairullah770/Vortex-Programming-Language)
- [Documentation](../VORTEX_ANALYSIS.md)

## 🎓 Educational Purpose

This IDE is designed for:
- Learning compiler design concepts
- Understanding lexical and syntactic analysis
- Experimenting with custom programming languages
- Teaching programming language theory

---

**Enjoy coding in Vortex! 🌀**
