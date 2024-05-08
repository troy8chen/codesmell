"""
This class structure is inspired by this article on StackOverflow.com:
https://stackoverflow.com/questions/43166571/getting-all-the-nodes-from-python-ast-that-correspond-to-a-particular-variable-w
"""
import ast


class LongParameterListDetector(ast.NodeVisitor):
    def __init__(self, allowance=3):
        self.allowance = allowance
        self.parameter_counts = []
        self.source_code = ""

    def visit_FunctionDef(self, node):
        """
        Override ast.NodeVisitor's default traversal definition:
        the goal is to count the parameters in the classifier, and ignore
        parameter "self"
        """
        num_parameters = len(
            [arg for arg in node.args.args if arg.arg != 'self'])
        self.parameter_counts.append(
            (node.name, num_parameters, num_parameters > self.allowance))
        self.generic_visit(node)

    def analyze_file(self, file_path):
        """
        Access the Python file that needs to check if it is long parameter list
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.source_code = file.read()
            self.visit(ast.parse(self.source_code, file_path))
        except (FileNotFoundError, SyntaxError) as error_message:
            print(f"Error occurs accessing the file in {file_path}: "
                  f"{error_message}")
        return self.parameter_counts

    def print_parameter_counts(self):
        """
        Print out the analyzed result
        """
        report_lines = []
        for method_name, num_params, has_long_param_list in \
                self.parameter_counts:
            status = "has a long parameter list, count >" \
                if has_long_param_list \
                else "within acceptable parameter count, count <="
            report_line = f"- {method_name} function has {num_params} " \
                          f"parameters: {status} {self.allowance}"
            report_lines.append(report_line)
        return "\n".join(report_lines)
