"""
This class is refined by adopting method from these sources:
- Roy, Chanchal K., and James R. Cordy. "A survey on software clone detection research."
  Queen's School of Computing TR, 2007. This work provides a comprehensive overview
  of detection techniques and tools, which has informed the CloneDetector's
  approach to identifying similar code patterns.

- Falke, Raimar, Pierre Frenzel, and Rainer Koschke. "Clone Detection Using Abstract Syntax Suffix Trees."
  University of Bremen, Germany, 2006. This paper's discussion on leveraging abstract syntax trees
  for clone detection has inspired the method of tokenization and comparison used in this implementation.

- Levandowsky, Michael, and David Winter. "Distance between sets." Nature 234.5323 (1971): 34-35.
  The conceptual understanding of set similarity and the application of the Jaccard index
  as discussed in this paper underpin the CloneDetector's algorithm for assessing code similarity.
"""
import itertools
import ast
import astor
from typing import Dict, Tuple, Set, List


class CloneDetector(ast.NodeVisitor):
    def __init__(self, similarity_threshold=0.75):
        self.similarity_threshold = similarity_threshold
        self.function_info: Dict[str, Tuple[ast.FunctionDef, Set[str]]] = {}
        self.duplicates: List[Tuple[str, str, float]] = []
        self.source_code = ""
        self.ast_tree = None
        self.red = None  # RedBaron instance

    def tokenize_ast(self, node) -> Set[str]:
        tokens = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Str):
                tokens.add('STR')
            elif isinstance(child, ast.Num):
                tokens.add('NUM')
            elif isinstance(child, ast.Name):
                tokens.add(f"VAR:{child.id}")
            elif isinstance(child, (ast.Assign, ast.AugAssign)):
                tokens.add('ASSIGN')
            elif isinstance(child, (ast.For, ast.While)):
                tokens.add('LOOP')
            elif isinstance(child, ast.If):
                tokens.add('IF_STMT')
            # Add other types as needed
        return tokens

    def jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union) if union else 1.0

    def visit_FunctionDef(self, node):
        #start_lineno = node.lineno - 1
        #end_lineno = node.end_lineno
        #function_source = "\n".join(self.source_code.splitlines()[start_lineno:end_lineno])
        # Syntactic tokenization
        syntactic_tokens = self.tokenize_ast(node)
        self.function_info[node.name] = (node, syntactic_tokens)
        self.generic_visit(node)

    def find_duplicates(self):
        for (name1, (node1, tokens1)), (name2, (node2, tokens2)) in itertools.combinations(self.function_info.items(), 2):
            # Calculate syntactic similarity
            syntactic_similarity = self.jaccard_similarity(tokens1, tokens2)
            if syntactic_similarity >= self.similarity_threshold:
                self.duplicates.append((name1, name2, syntactic_similarity))
                # For simplicity, refactor the first function to call the second one
                self.refactor_duplicate(node1, name2)

    def refactor_duplicate(self, func_node, new_func_name):
        # Create a call to the new function
        new_call = ast.Call(func=ast.Name(id=new_func_name, ctx=ast.Load()),
                            args=[], keywords=[])

        # Optionally, handle function arguments
        # Assuming the new function has the same arguments as the original function
        new_call.args = [ast.Name(id=arg.arg, ctx=ast.Load()) for arg in
                         func_node.args.args]

        # Optionally, handle return statement
        # Assuming the original function contains a single return statement
        return_stmts = [stmt for stmt in func_node.body if
                        isinstance(stmt, ast.Return)]
        if return_stmts:
            # If the original function has a return statement, replace it with the new function call
            return_value = return_stmts[0].value
            new_return_stmt = ast.Return(value=new_call)
            func_node.body = [new_return_stmt]
        else:
            # If the original function does not have a return statement, add the new function call as the last statement
            new_return_stmt = ast.Expr(value=new_call)
            func_node.body.append(new_return_stmt)

    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.source_code = file.read()
            self.ast_tree = ast.parse(self.source_code, file_path)
            self.visit(self.ast_tree)
            self.find_duplicates()
        except FileNotFoundError:
            print(f"Cannot locate the file: {file_path}")
        except SyntaxError as error_message:
            print(f"Syntax error detected in {file_path}: {error_message}")

    def print_duplicates(self):
        if not self.duplicates:
            return "No duplicated code detected."

        report_lines = [
            f"Duplicated code detected with syntactic similarity over {self.similarity_threshold}:"
        ]

        for name1, name2, syntactic_similarity in self.duplicates:
            report_lines.append(
                f"{name1} and {name2} have syntactic similarity of {syntactic_similarity:.2f}."
            )

        return "\n".join(report_lines)

    def save_refactored_code(self, file_path):
        if self.ast_tree:
            refactored_code = astor.to_source(self.ast_tree)
            with open(file_path, 'w') as file:
                file.write(refactored_code)
            print(f"Refactored code saved to: {file_path}")
        else:
            print("No AST tree to refactor.")
