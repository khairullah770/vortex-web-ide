import sys
import re

class VortexInterpreter:
    def __init__(self, user_inputs=None):
        self.variables = {}
        self.functions = {}
        self.output = []
        self.input_values = user_inputs or []
        self.input_index = 0

    def interpret_file(self, tokens_file):
        try:
            with open(tokens_file, 'r', encoding='utf-8') as f:
                tokens = self.parse_tokens(f.read())
            self.parse_program(tokens)
            if 'main' in self.functions:
                self.execute_function('main', [])
            else:
                self.output.append('Error: No main() function found')
            return '\n'.join(self.output)
        except Exception as e:
            return f'Runtime Error: {str(e)}'

    def parse_tokens(self, token_text):
        tokens = []
        for line in token_text.strip().split('\n'):
            if not line.strip():
                continue
            match = re.match(r"(\w+)\('(.*)'\) at line (\d+)", line)
            if match:
                token_type, value, line_num = match.groups()
                tokens.append({'type': token_type, 'value': value, 'line': int(line_num)})
        return tokens

    def parse_program(self, tokens):
        i = 0
        while i < len(tokens):
            if tokens[i]['type'] == 'KEYWORD' and tokens[i]['value'] == 'func':
                i = self.parse_function_definition(tokens, i)
            else:
                i += 1

    def parse_function_definition(self, tokens, start):
        i = start + 1
        if i >= len(tokens) or tokens[i]['type'] != 'IDENTIFIER':
            return i
        func_name = tokens[i]['value']
        i += 1
        params = []
        if i < len(tokens) and tokens[i]['type'] == 'LEFT_PAREN':
            i += 1
            while i < len(tokens) and tokens[i]['type'] != 'RIGHT_PAREN':
                if tokens[i]['type'] == 'KEYWORD':
                    i += 1
                if i < len(tokens) and tokens[i]['type'] == 'IDENTIFIER':
                    params.append(tokens[i]['value'])
                    i += 1
                if i < len(tokens) and tokens[i]['type'] == 'COMMA':
                    i += 1
            i += 1
        if i < len(tokens) and tokens[i]['type'] == 'LEFT_BRACE':
            body_start = i
            brace_count = 1
            i += 1
            while i < len(tokens) and brace_count > 0:
                if tokens[i]['type'] == 'LEFT_BRACE':
                    brace_count += 1
                elif tokens[i]['type'] == 'RIGHT_BRACE':
                    brace_count -= 1
                i += 1
            body_end = i
            self.functions[func_name] = {'params': params, 'body': tokens[body_start:body_end]}
        return i

    def execute_function(self, func_name, args):
        if func_name not in self.functions:
            return None
        func = self.functions[func_name]
        old_vars = self.variables.copy()
        for i, param in enumerate(func['params']):
            if i < len(args):
                self.variables[param] = args[i]
        result = self.execute_block(func['body'])
        self.variables = old_vars
        return result

    def execute_block(self, tokens):
        i = 0
        if tokens and tokens[0]['type'] == 'LEFT_BRACE':
            i = 1
        while i < len(tokens):
            if tokens[i]['type'] == 'RIGHT_BRACE':
                break
            if tokens[i]['type'] == 'KEYWORD':
                keyword = tokens[i]['value']
                if keyword == 'out':
                    i = self.execute_out(tokens, i)
                elif keyword == 'in':
                    i = self.execute_in(tokens, i)
                elif keyword in ['num', 'str', 'bool', 'list', 'const']:
                    i = self.execute_declaration(tokens, i)
                else:
                    i += 1
            elif tokens[i]['type'] == 'IDENTIFIER':
                if i + 1 < len(tokens) and tokens[i + 1]['type'] == 'LEFT_PAREN':
                    i = self.execute_function_call(tokens, i)
                else:
                    i = self.execute_assignment(tokens, i)
            else:
                i += 1
        return None

    def execute_out(self, tokens, start):
        i = start + 1
        if i < len(tokens) and tokens[i]['type'] == 'LEFT_PAREN':
            i += 1
            expr_tokens = []
            paren_count = 1
            while i < len(tokens) and paren_count > 0:
                if tokens[i]['type'] == 'LEFT_PAREN':
                    paren_count += 1
                elif tokens[i]['type'] == 'RIGHT_PAREN':
                    paren_count -= 1
                    if paren_count == 0:
                        break
                expr_tokens.append(tokens[i])
                i += 1
            value = self.evaluate_expression(expr_tokens)
            self.output.append(str(value))
            i += 1
            if i < len(tokens) and tokens[i]['type'] == 'SEMICOLON':
                i += 1
        return i

    def execute_in(self, tokens, start):
        i = start + 1
        if i < len(tokens) and tokens[i]['type'] == 'LEFT_PAREN':
            i += 1
            if i < len(tokens) and tokens[i]['type'] == 'IDENTIFIER':
                var_name = tokens[i]['value']
                i += 1
                if self.input_index < len(self.input_values):
                    # Use the provided input value
                    val = self.input_values[self.input_index]
                    self.input_index += 1
                    # Try to convert to number if possible
                    try:
                        self.variables[var_name] = int(val)
                    except ValueError:
                        try:
                            self.variables[var_name] = float(val)
                        except ValueError:
                            self.variables[var_name] = val
                else:
                    # No input provided - signal that input is needed
                    self.output.append(f'[INPUT_NEEDED:{var_name}]')
                    self.variables[var_name] = ''
                i += 1  # skip RIGHT_PAREN
                if i < len(tokens) and tokens[i]['type'] == 'SEMICOLON':
                    i += 1
        return i

    def execute_declaration(self, tokens, start):
        i = start
        if tokens[i]['value'] == 'const':
            i += 1
        i += 1
        if i < len(tokens) and tokens[i]['type'] == 'IDENTIFIER':
            var_name = tokens[i]['value']
            i += 1
            if i < len(tokens) and tokens[i]['type'] == 'OPERATOR' and tokens[i]['value'] == '=':
                i += 1
                expr_tokens = []
                while i < len(tokens) and tokens[i]['type'] != 'SEMICOLON':
                    expr_tokens.append(tokens[i])
                    i += 1
                value = self.evaluate_expression(expr_tokens)
                self.variables[var_name] = value
                if i < len(tokens) and tokens[i]['type'] == 'SEMICOLON':
                    i += 1
            else:
                self.variables[var_name] = ''
                if i < len(tokens) and tokens[i]['type'] == 'SEMICOLON':
                    i += 1
        return i

    def execute_assignment(self, tokens, start):
        var_name = tokens[start]['value']
        i = start + 1
        if i < len(tokens) and tokens[i]['type'] == 'OPERATOR':
            op = tokens[i]['value']
            i += 1
            expr_tokens = []
            while i < len(tokens) and tokens[i]['type'] != 'SEMICOLON':
                expr_tokens.append(tokens[i])
                i += 1
            value = self.evaluate_expression(expr_tokens)
            if op == '=':
                self.variables[var_name] = value
            elif op == '+=':
                self.variables[var_name] = self.variables.get(var_name, 0) + value
            if i < len(tokens) and tokens[i]['type'] == 'SEMICOLON':
                i += 1
        return i

    def execute_function_call(self, tokens, start):
        func_name = tokens[start]['value']
        i = start + 2
        args = []
        arg_tokens = []
        while i < len(tokens) and tokens[i]['type'] != 'RIGHT_PAREN':
            if tokens[i]['type'] == 'COMMA':
                if arg_tokens:
                    args.append(self.evaluate_expression(arg_tokens))
                    arg_tokens = []
                i += 1
            else:
                arg_tokens.append(tokens[i])
                i += 1
        if arg_tokens:
            args.append(self.evaluate_expression(arg_tokens))
        self.execute_function(func_name, args)
        i += 1
        if i < len(tokens) and tokens[i]['type'] == 'SEMICOLON':
            i += 1
        return i

    def evaluate_expression(self, tokens):
        if not tokens:
            return ''
        if len(tokens) == 1:
            token = tokens[0]
            if token['type'] == 'NUMBER_LITERAL':
                return float(token['value']) if '.' in token['value'] else int(token['value'])
            elif token['type'] == 'STRING_LITERAL':
                return token['value'].strip('"')
            elif token['type'] == 'BOOLEAN_LITERAL':
                return token['value'] == 'yes'
            elif token['type'] == 'IDENTIFIER':
                return self.variables.get(token['value'], '')
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token['type'] == 'NUMBER_LITERAL':
                result.append(float(token['value']) if '.' in token['value'] else int(token['value']))
            elif token['type'] == 'STRING_LITERAL':
                result.append(token['value'].strip('"'))
            elif token['type'] == 'BOOLEAN_LITERAL':
                result.append(token['value'] == 'yes')
            elif token['type'] == 'IDENTIFIER':
                result.append(self.variables.get(token['value'], ''))
            elif token['type'] == 'OPERATOR':
                op = token['value']
                if len(result) >= 1 and i + 1 < len(tokens):
                    left = result.pop()
                    i += 1
                    right = None
                    if tokens[i]['type'] == 'NUMBER_LITERAL':
                        right = float(tokens[i]['value']) if '.' in tokens[i]['value'] else int(tokens[i]['value'])
                    elif tokens[i]['type'] == 'STRING_LITERAL':
                        right = tokens[i]['value'].strip('"')
                    elif tokens[i]['type'] == 'IDENTIFIER':
                        right = self.variables.get(tokens[i]['value'], '')
                    if right is not None:
                        if op == '+':
                            if isinstance(left, str) or isinstance(right, str):
                                result.append(str(left) + str(right))
                            else:
                                result.append(left + right)
                        elif op == '-':
                            result.append(left - right)
                        elif op == '*':
                            result.append(left * right)
                        elif op == '/':
                            result.append(left / right if right != 0 else 0)
                        else:
                            result.append(left)
            i += 1
        return result[0] if result else ''


def main():
    if len(sys.argv) < 2:
        print('Usage: python vortex_interpreter.py <tokens_file> [input1] [input2] ...')
        sys.exit(1)
    tokens_file = sys.argv[1]
    # All extra args are user inputs in order
    user_inputs = sys.argv[2:] if len(sys.argv) > 2 else []
    interpreter = VortexInterpreter(user_inputs=user_inputs)
    output = interpreter.interpret_file(tokens_file)
    print(output)


if __name__ == '__main__':
    main()
