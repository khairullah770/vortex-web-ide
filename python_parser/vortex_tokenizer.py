import sys

# Token structure
class Token:
    def __init__(self, token_type, value, line):
        self.type = token_type
        self.value = value
        self.line = line

    def print(self):
        print(f"{self.type}('{self.value}') at line {self.line}")

# Keywords
keywords = {
    "func", "num", "str", "bool", "list", "const", "in", "out",
    "when", "whenelse", "else", "repeat", "cycle", "perform",
    "break", "skip", "select", "case", "default", "give", "try", "catch"
}

# Operators
operators = {
    "==", "!=", ">=", "<=", "=", "+", "-", "*", "/", "->", ".", "++", "--",
    "+=", "-=", "*=", "/=", "<", ">", "%", "&&", "||", "!"
}

# Symbols
symbols = {
    '{', '}', '(', ')', '[', ']', ';', ':', ',', '\''
}

symbol_map = {
    '{': "LEFT_BRACE", '}': "RIGHT_BRACE", '(': "LEFT_PAREN", ')': "RIGHT_PAREN",
    '[': "LEFT_BRACKET", ']': "RIGHT_BRACKET", ';': "SEMICOLON", ':': "COLON",
    ',': "COMMA", '\'': "SINGLE_QUOTE"
}

has_errors = False
in_multiline_comment = False
in_string = False
string_buffer = ""
string_start_line = 0

def tokenize_line(line, line_number):
    global has_errors, in_multiline_comment, in_string, string_buffer, string_start_line
    tokens = []
    i = 0
    n = len(line)

    while i < n:
        if in_multiline_comment:
            end = line.find("*#", i)
            if end != -1:
                in_multiline_comment = False
                i = end + 2
            else:
                return tokens
            continue

        if line[i:i+2] == "#*":
            in_multiline_comment = True
            i += 2
            continue

        if line[i:i+2] == "##":
            break

        if line[i].isspace():
            i += 1
            continue

        if in_string or line[i] == '"':
            if not in_string:
                in_string = True
                string_start_line = line_number
                string_buffer = '"'
                i += 1

            while i < n:
                if line[i] == '\\' and i + 1 < n:
                    string_buffer += line[i:i+2]
                    i += 2
                elif line[i] == '"':
                    string_buffer += '"'
                    tokens.append(Token("STRING_LITERAL", string_buffer, string_start_line))
                    in_string = False
                    i += 1
                    break
                else:
                    string_buffer += line[i]
                    i += 1

            if in_string:
                return tokens
            continue

        if line[i].isdigit():
            j = i
            has_dot = False
            invalid = False
            while j < n and (line[j].isdigit() or line[j] == '.'):
                if line[j] == '.':
                    if has_dot or j + 1 >= n or not line[j + 1].isdigit():
                        invalid = True
                        j += 1
                        break
                    has_dot = True
                j += 1
            number = line[i:j]
            if invalid or (j < n and (line[j].isalpha() or line[j] == '_')):
                tokens.append(Token("ERROR", f"Invalid number literal: '{number}'", line_number))
                has_errors = True
                i = j
            else:
                tokens.append(Token("NUMBER_LITERAL", number, line_number))
                i = j
            continue

        if line[i].isalpha() or line[i] == '_':
            j = i
            while j < n and (line[j].isalnum() or line[j] == '_'):
                j += 1
            word = line[i:j]
            if word in {"yes", "no"}:
                tokens.append(Token("BOOLEAN_LITERAL", word, line_number))
            elif word in keywords:
                tokens.append(Token("KEYWORD", word, line_number))
            else:
                tokens.append(Token("IDENTIFIER", word, line_number))
            i = j
            continue

        matched_op = False
        for length in (3, 2, 1):
            if i + length <= n:
                op = line[i:i+length]
                if op in operators:
                    op_type = "OPERATOR"
                    if op == "&&":
                        op_type = "LOGICAL_AND"
                    elif op == "||":
                        op_type = "LOGICAL_OR"
                    elif op == "!":
                        op_type = "LOGICAL_NOT"
                    tokens.append(Token(op_type, op, line_number))
                    i += length
                    matched_op = True
                    break
        if matched_op:
            continue

        if line[i] in symbols:
            tokens.append(Token(symbol_map[line[i]], line[i], line_number))
            i += 1
            continue

        tokens.append(Token("ERROR", f"Invalid character '{line[i]}'", line_number))
        has_errors = True
        i += 1

    return tokens

def write_tokens_to_file(all_tokens, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as out:
            for token in all_tokens:
                out.write(f"{token.type}('{token.value}') at line {token.line}\n")
        print(f"Tokens saved to: {filename}")
    except IOError:
        print("Error: Could not write token output file.")

def main():
    global in_string, in_multiline_comment, has_errors, string_start_line

    if len(sys.argv) != 2:
        print("Usage: python vortex_tokenizer.py <source_file.vortex>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            all_tokens = []
            line_number = 1

            for line in file:
                tokens = tokenize_line(line.rstrip('\n'), line_number)
                all_tokens.extend(tokens)
                for token in tokens:
                    token.print()
                line_number += 1

        if in_string:
            print(f"Lexical Error: Unterminated string literal starting at line {string_start_line}.")
            has_errors = True

        if in_multiline_comment:
            print("Lexical Error: Unclosed multi-line comment.")
            has_errors = True

        if has_errors:
            print("\nLexical errors detected. See messages above.")
            sys.exit(2)
        else:
            write_tokens_to_file(all_tokens, filename + ".tokens")
            print("\nAll tokens scanned successfully.")
            sys.exit(0)

    except FileNotFoundError:
        print("Error: Cannot open file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
