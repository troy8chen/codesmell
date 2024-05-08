"""
This class structure is inspired by this article on StackOverflow.com:
https://stackoverflow.com/questions/43166571/getting-all-the-nodes-from-python-ast-that-correspond-to-a-particular-variable-w
"""
import ast


class LongMethodDetector(ast.NodeVisitor):
    def __init__(self, line_limit=15):
        self.line_limit = line_limit
        self.long_methods = []
        self.source_code = ""

    def get_function_length(self, node):
        """
        Obtain the length by excluding whitespace lines
        """
        lines = self.source_code.splitlines()[
                         node.lineno - 1:node.end_lineno]
        return sum(1 for line in lines if line.strip())

    def visit_FunctionDef(self, node):
        """
        Override default ast.NodeVsitor's FunctionDef:
        To determine if a method is lengthy we calculate its length
        """
        length = self.get_function_length(node)
        is_long_method = length > self.line_limit
        self.long_methods.append((node.name, length, is_long_method))
        self.generic_visit(node)

    def read_file(self, file_path):
        """
        To read and interpret the provided Python file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.source_code = file.read()
            self.visit(ast.parse(self.source_code, file_path))
        except FileNotFoundError:
            print(f"Can not locate the file: {file_path}")
        except SyntaxError as error_message:
            print(f"Syntax error detected in {file_path}: {error_message}")
        return self.long_methods

    def print_long_methods(self):
        """
        Prepare a report, on methods that surpass the specified line limit
        """
        report_lines = []
        for method_name, length, is_long_method in self.long_methods:
            status = "long method, LOC >" if is_long_method \
                else "within line limit LOC <"
            report_line = f"- {method_name} function has {length} " \
                          f"lines: {status} {self.line_limit}"
            report_lines.append(report_line)
        return "\n".join(report_lines)
