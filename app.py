from flask import Flask, render_template, request, jsonify
import sys
import os
import re
import tempfile
import subprocess
from pathlib import Path

app = Flask(__name__)

# Works both locally and on any cloud server
BASE_DIR = Path(__file__).parent.resolve()
VORTEX_PARSER_DIR = BASE_DIR / "python_parser"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile_code():
    """Tokenize, parse, and run Vortex code. Accepts optional user_inputs list."""
    try:
        data = request.json
        code = data.get('code', '')
        user_inputs = data.get('user_inputs', [])   # list of strings from the browser

        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'})

        # Write source to a temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vortex',
                                         delete=False, encoding='utf-8') as f:
            f.write(code)
            vortex_file = f.name

        tokens_file = vortex_file + '.tokens'

        try:
            # ── Step 1: Tokenize ──────────────────────────────────────────
            tokenizer_path = VORTEX_PARSER_DIR / "vortex_tokenizer.py"
            tok = subprocess.run(
                [sys.executable, str(tokenizer_path), vortex_file],
                capture_output=True, text=True, timeout=5,
                encoding='utf-8', errors='replace'
            )

            if tok.returncode != 0:
                return jsonify({
                    'success': False,
                    'stage': 'tokenization',
                    'error': tok.stdout + tok.stderr,
                    'tokens': None,
                    'parseResult': None
                })

            with open(tokens_file, 'r', encoding='utf-8') as f:
                tokens_text = f.read()

            # ── Step 2: Parse ─────────────────────────────────────────────
            parser_path = VORTEX_PARSER_DIR / "vortex_parser.py"
            parse = subprocess.run(
                [sys.executable, str(parser_path), tokens_file],
                capture_output=True, text=True, timeout=5,
                encoding='utf-8', errors='replace'
            )
            parse_output = parse.stdout + parse.stderr
            success = "No syntax errors detected" in parse_output

            # ── Step 3: Interpret ─────────────────────────────────────────
            execution_output = None
            needs_input = []      # variable names still waiting for input

            if success:
                interpreter_path = VORTEX_PARSER_DIR / "vortex_interpreter.py"
                cmd = [sys.executable, str(interpreter_path), tokens_file] + \
                      [str(v) for v in user_inputs]
                try:
                    interp = subprocess.run(
                        cmd,
                        capture_output=True, text=True, timeout=10,
                        encoding='utf-8', errors='replace'
                    )
                    raw = interp.stdout + interp.stderr

                    # Detect which variables still need input
                    needs_input = re.findall(r'\[INPUT_NEEDED:(\w+)\]', raw)

                    # Clean the markers out of the visible output
                    clean = re.sub(r'\[INPUT_NEEDED:\w+\]\n?', '', raw).strip()
                    execution_output = clean

                except subprocess.TimeoutExpired:
                    execution_output = "Execution timeout"
                except Exception as e:
                    execution_output = f"Execution error: {str(e)}"

            # Clean up
            os.unlink(vortex_file)
            if os.path.exists(tokens_file):
                os.unlink(tokens_file)

            return jsonify({
                'success': success,
                'stage': 'complete',
                'tokens': tokens_text,
                'parseResult': parse_output,
                'executionOutput': execution_output,
                'needsInput': needs_input,   # e.g. ["name", "age"]
                'message': 'OK' if success else 'Compilation failed'
            })

        except subprocess.TimeoutExpired:
            return jsonify({'success': False, 'error': 'Compilation timeout'})
        except Exception as e:
            return jsonify({'success': False, 'error': f'Compilation error: {str(e)}'})

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})


@app.route('/examples', methods=['GET'])
def get_examples():
    examples = {
        'hello_world': {
            'name': 'Hello World',
            'code': 'func main() {\n    out("Hello, Vortex!");\n}'
        },
        'variables': {
            'name': 'Variables & Types',
            'code': '''func main() {
    num age = 25;
    str name = "Ali";
    bool isActive = yes;
    const num PI = 3.14;

    out("Name: " + name);
    out("Age: " + age);
}'''
        },
        'input_output': {
            'name': 'Input & Output',
            'code': '''func main() {
    out("What is your name?");
    str name;
    in(name);

    out("How old are you?");
    num age;
    in(age);

    out("Hello, " + name + "!");
    out("You are " + age + " years old.");
}'''
        },
        'functions': {
            'name': 'Functions',
            'code': '''func add(num a, num b) -> num {
    give a + b;
}

func greet(str name) {
    out("Hello, " + name + "!");
}

func main() {
    num result = add(10, 5);
    out("10 + 5 = " + result);
    greet("Ali");
}'''
        },

    }
    return jsonify(examples)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
