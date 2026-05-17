from flask import Flask, render_template, request, jsonify
import sys
import os
import re
import io
from pathlib import Path

app = Flask(__name__)

# Add python_parser to path so we can import directly (no subprocess needed)
BASE_DIR = Path(__file__).parent.resolve()
PARSER_DIR = str(BASE_DIR / "python_parser")
if PARSER_DIR not in sys.path:
    sys.path.insert(0, PARSER_DIR)

import vortex_tokenizer as tokenizer_mod
import vortex_parser   as parser_mod
import vortex_interpreter as interp_mod


# ── helpers ──────────────────────────────────────────────────────────────────

def run_tokenizer(code: str):
    """
    Tokenize Vortex source code.
    Returns (tokens_list, tokens_text, error_message)
    """
    # Reset global state in tokenizer
    tokenizer_mod.has_errors = False
    tokenizer_mod.in_multiline_comment = False
    tokenizer_mod.in_string = False
    tokenizer_mod.string_buffer = ""
    tokenizer_mod.string_start_line = 0

    all_tokens = []
    lines = code.split('\n')
    for line_number, line in enumerate(lines, start=1):
        toks = tokenizer_mod.tokenize_line(line.rstrip('\n'), line_number)
        all_tokens.extend(toks)

    # Check for unclosed string / comment
    errors = []
    if tokenizer_mod.in_string:
        errors.append(f"Lexical Error: Unterminated string literal starting at line {tokenizer_mod.string_start_line}.")
    if tokenizer_mod.in_multiline_comment:
        errors.append("Lexical Error: Unclosed multi-line comment.")
    if tokenizer_mod.has_errors:
        error_tokens = [t for t in all_tokens if t.type == 'ERROR']
        for et in error_tokens:
            errors.append(f"Lexical Error at line {et.line}: {et.value}")

    if errors:
        return None, None, '\n'.join(errors)

    # Build tokens text (same format as the .tokens file)
    tokens_text = '\n'.join(
        f"{t.type}('{t.value}') at line {t.line}" for t in all_tokens
    )
    return all_tokens, tokens_text, None


def run_parser(tokens_text: str):
    """
    Parse a tokens string.
    Returns (success, parse_output)
    """
    tokens = []
    for line in tokens_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            part1, part2 = line.split(" at line ")
            type_, val = part1.split("(", 1)
            val = val.rstrip(")")
            if val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            tokens.append(parser_mod.Token(type_, val, int(part2)))
        except Exception:
            pass

    parser = parser_mod.Parser(tokens)
    errors = parser.parse()

    if errors:
        output = "Parsing started...\nParsing finished.\n\nSyntax errors found:\n"
        output += '\n'.join(f"  - {e}" for e in errors)
        return False, output
    else:
        return True, "Parsing started...\nParsing finished.\n\nNo syntax errors detected."


def run_interpreter(tokens_text: str, user_inputs: list):
    """
    Interpret a tokens string with given user inputs.
    Returns (output, needs_input_list)
    """
    interpreter = interp_mod.VortexInterpreter(user_inputs=user_inputs)

    # Feed tokens directly instead of reading a file
    tokens = interpreter.parse_tokens(tokens_text)
    interpreter.parse_program(tokens)

    if 'main' in interpreter.functions:
        interpreter.execute_function('main', [])
    else:
        interpreter.output.append('Error: No main() function found')

    raw = '\n'.join(interpreter.output)
    needs_input = re.findall(r'\[INPUT_NEEDED:(\w+)\]', raw)
    clean = re.sub(r'\[INPUT_NEEDED:\w+\]\n?', '', raw).strip()
    return clean, needs_input


# ── routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        data = request.json
        code = data.get('code', '')
        user_inputs = data.get('user_inputs', [])

        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'})

        # Step 1: Tokenize
        _, tokens_text, tok_error = run_tokenizer(code)
        if tok_error:
            return jsonify({
                'success': False,
                'stage': 'tokenization',
                'error': tok_error,
                'tokens': None,
                'parseResult': None
            })

        # Step 2: Parse
        success, parse_output = run_parser(tokens_text)

        # Step 3: Interpret
        execution_output = None
        needs_input = []
        if success:
            try:
                execution_output, needs_input = run_interpreter(tokens_text, user_inputs)
            except Exception as e:
                execution_output = f"Runtime Error: {str(e)}"

        return jsonify({
            'success': success,
            'stage': 'complete',
            'tokens': tokens_text,
            'parseResult': parse_output,
            'executionOutput': execution_output,
            'needsInput': needs_input,
            'message': 'OK' if success else 'Compilation failed'
        })

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
