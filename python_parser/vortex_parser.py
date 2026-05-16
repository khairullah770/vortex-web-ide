# Updated VortexLang parser with list of objects support and -> validation
import sys

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __str__(self):
        return f"{self.type}('{self.value}') at line {self.line}"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None
        self.errors = []

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def expect(self, type_, value=None):
        if self.current and self.current.type == type_ and (value is None or self.current.value == value):
            self.advance()
            return True
        line = self.current.line if self.current else 'EOF'
        found = f"{self.current.type}('{self.current.value}')" if self.current else 'EOF'
        expected = f"{type_}" + (f"('{value}')" if value else "")
        self.errors.append(f"Expected {expected}, found {found} at line {line}")
        return False

    def parse(self):
        self.parse_program()
        return self.errors

    def parse_program(self):
        while self.current:
            if self.current.type == "KEYWORD" and self.current.value == "func":
                self.parse_func_decl()
            elif self.current.type == "KEYWORD" and self.current.value in ("num", "str", "bool", "list", "const"):
                self.parse_var_decl()
            else:
                self.errors.append(f"Unexpected token at global scope: {self.current}")
                self.advance()

    def parse_func_decl(self):
        self.expect("KEYWORD", "func")
        self.expect("IDENTIFIER")
        self.expect("LEFT_PAREN")
        self.parse_param_list()
        self.expect("RIGHT_PAREN")
        if self.current and self.current.type == "OPERATOR" and self.current.value == "->":
            self.advance()
            self.expect("KEYWORD")
        self.parse_block()

    def parse_param_list(self):
        while self.current and self.current.type == "KEYWORD":
            self.advance()
            self.expect("IDENTIFIER")
            if self.current and self.current.type == "OPERATOR" and self.current.value == "=":
                self.advance()
                self.parse_expr()
            if self.current and self.current.type == "COMMA":
                self.advance()

    def parse_block(self):
        self.expect("LEFT_BRACE")
        while self.current and self.current.type != "RIGHT_BRACE":
            self.parse_statement()
        self.expect("RIGHT_BRACE")

    def parse_statement(self):
        if not self.current:
            return

        kw = self.current.value if self.current.type == "KEYWORD" else None
        if kw in ("num", "str", "bool", "list", "const"):
            self.parse_var_decl()
        elif kw == "in":
            self.parse_input()
        elif kw == "out":
            self.parse_output()
        elif kw == "give":
            self.advance()
            self.parse_expr()
            self.expect("SEMICOLON")
        elif kw == "when":
            self.parse_when()
        elif kw == "repeat":
            self.parse_repeat()
        elif kw == "cycle":
            self.parse_cycle()
        elif kw == "perform":
            self.parse_perform_cycle()
        elif kw in ("break", "skip"):
            self.advance()
            self.expect("SEMICOLON")
        elif kw == "select":
            self.parse_select()
        elif kw == "try":
            self.parse_try_catch()
        elif self.current.type == "IDENTIFIER":
            self.parse_assignment_or_call()
            self.expect("SEMICOLON")
        else:
            self.errors.append(f"Unexpected token: {self.current}")
            self.advance()

    def parse_var_decl(self):
        if self.current.value == "const":
            self.advance()
        if self.current.type == "KEYWORD":
            self.advance()
        self.expect("IDENTIFIER")
        # Initializer is optional: allow  str name;  as well as  str name = expr;
        if self.current and self.current.type == "OPERATOR" and self.current.value == "=":
            self.advance()
            self.parse_expr()
        self.expect("SEMICOLON")

    def parse_input(self):
        self.advance()
        self.expect("LEFT_PAREN")
        self.expect("IDENTIFIER")
        self.expect("RIGHT_PAREN")
        self.expect("SEMICOLON")

    def parse_output(self):
        self.advance()
        self.expect("LEFT_PAREN")
        self.parse_expr()
        self.expect("RIGHT_PAREN")
        self.expect("SEMICOLON")

    def parse_assignment_or_call(self):
        self.advance()
        if self.current and self.current.type == "LEFT_BRACKET":
            self.advance()
            self.parse_expr()
            self.expect("RIGHT_BRACKET")
        if self.current and self.current.type == "OPERATOR":
            self.advance()
            self.parse_expr()
        elif self.current and self.current.type == "LEFT_PAREN":
            self.advance()
            if self.current and self.current.type != "RIGHT_PAREN":
                self.parse_expr()
                while self.current and self.current.type == "COMMA":
                    self.advance()
                    self.parse_expr()
            self.expect("RIGHT_PAREN")

    def parse_when(self):
        self.expect("KEYWORD", "when")
        self.expect("LEFT_PAREN")
        self.parse_expr()
        self.expect("RIGHT_PAREN")
        self.parse_block()
        while self.current and self.current.value == "whenelse":
            self.advance()
            self.expect("LEFT_PAREN")
            self.parse_expr()
            self.expect("RIGHT_PAREN")
            self.parse_block()
        if self.current and self.current.value == "else":
            self.advance()
            self.parse_block()

    def parse_repeat(self):
        self.advance()
        self.expect("LEFT_PAREN")
        self.parse_var_decl()
        self.parse_expr()
        self.expect("SEMICOLON")
        self.parse_assignment_or_call()
        self.expect("RIGHT_PAREN")
        self.parse_block()

    def parse_cycle(self):
        self.advance()
        self.expect("LEFT_PAREN")
        self.parse_expr()
        self.expect("RIGHT_PAREN")
        self.parse_block()

    def parse_perform_cycle(self):
        self.advance()
        self.parse_block()
        self.expect("KEYWORD", "cycle")
        self.expect("LEFT_PAREN")
        self.parse_expr()
        self.expect("RIGHT_PAREN")
        self.expect("SEMICOLON")

    def parse_select(self):
        self.advance()
        self.expect("LEFT_PAREN")
        self.parse_expr()
        self.expect("RIGHT_PAREN")
        self.expect("LEFT_BRACE")
        while self.current and self.current.value == "case":
            self.advance()
            self.parse_expr()
            self.expect("COLON")
            while self.current and not (self.current.value in ("case", "default") or self.current.type == "RIGHT_BRACE"):
                self.parse_statement()
        if self.current and self.current.value == "default":
            self.advance()
            self.expect("COLON")
            while self.current and self.current.type != "RIGHT_BRACE":
                self.parse_statement()
        self.expect("RIGHT_BRACE")

    def parse_try_catch(self):
        self.advance()
        self.parse_block()
        self.expect("KEYWORD", "catch")
        self.expect("LEFT_PAREN")
        self.expect("IDENTIFIER")
        self.expect("RIGHT_PAREN")
        self.parse_block()

    def parse_expr(self):
        expect_operand = True
        while self.current and self.current.type not in ("SEMICOLON", "COMMA", "RIGHT_PAREN", "RIGHT_BRACE"):
            if expect_operand:
                if self.current.type in ("IDENTIFIER", "NUMBER_LITERAL", "STRING_LITERAL", "BOOLEAN_LITERAL"):
                    self.advance()
                elif self.current.type == "LEFT_PAREN":
                    self.advance()
                    self.parse_expr()
                    self.expect("RIGHT_PAREN")
                elif self.current.type == "LEFT_BRACKET":
                    self.advance()
                    if self.current.type != "RIGHT_BRACKET":
                        self.parse_expr()
                        while self.current and self.current.type == "COMMA":
                            self.advance()
                            self.parse_expr()
                    self.expect("RIGHT_BRACKET")
                elif self.current.type == "LEFT_BRACE":
                    self.parse_object()
                else:
                    self.errors.append(f"Expected expression operand, found {self.current} at line {self.current.line}")
                    self.advance()
                expect_operand = False
            else:
                if self.current.type == "OPERATOR":
                    self.advance()
                    expect_operand = True
                else:
                    break

        if expect_operand:
            self.errors.append(f"Incomplete expression: expected operand at line {self.current.line if self.current else 'EOF'}")

    def parse_object(self):
        self.expect("LEFT_BRACE")
        while self.current and self.current.type != "RIGHT_BRACE":
            if self.current.type in ("KEYWORD", "IDENTIFIER"):
                self.advance()
                if self.current and self.current.type == "OPERATOR" and self.current.value == "=":
                    if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == "OPERATOR" and self.tokens[self.pos + 1].value == ">":
                        self.errors.append(f"Invalid operator '=>' used instead of '->' at line {self.current.line}")
                        self.advance()  # Skip '='
                        self.advance()  # Skip '>'
                        continue
                if self.current and self.current.type == "OPERATOR":
                    if self.current.value != "->":
                        self.errors.append(
                            f"Expected OPERATOR('->'), found OPERATOR('{self.current.value}') at line {self.current.line}"
                        )
                        self.advance()
                    else:
                        self.advance()
                else:
                    self.errors.append(f"Expected OPERATOR('->'), found {self.current} at line {self.current.line if self.current else 'EOF'}")
                self.parse_expr()
                if self.current and self.current.type == "COMMA":
                    self.advance()
            else:
                self.advance()
        self.expect("RIGHT_BRACE")


def main():
    if len(sys.argv) != 2:
        print("Usage: python vortex_parser.py <tokens_file>")
        return

    with open(sys.argv[1]) as f:
        tokens = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                part1, part2 = line.split(" at line ")
                type_, val = part1.split("(", 1)
                val = val.rstrip(")")
                if val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                tokens.append(Token(type_, val, int(part2)))
            except Exception as e:
                print(f"Error parsing token line: {line} -> {e}")

    parser = Parser(tokens)
    print("Parsing started...")
    errors = parser.parse()
    print("Parsing finished.\n")

    if errors:
        print("Syntax errors found:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("No syntax errors detected.")

if __name__ == "__main__":
    main()
