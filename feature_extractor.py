import ast

def extract_features(code):

    try:
        tree = ast.parse(code)
        syntax_error = 0

    except SyntaxError:
        return {
            "loops": 0,
            "functions": 0,
            "ifs": 0,
            "imports": 0,
            "try_blocks": 0,
            "lines": len(code.splitlines()),
            "syntax_error": 1
        }

    num_loops = sum(
        isinstance(node, (ast.For, ast.While))
        for node in ast.walk(tree)
    )

    num_functions = sum(
        isinstance(node, ast.FunctionDef)
        for node in ast.walk(tree)
    )

    num_ifs = sum(
        isinstance(node, ast.If)
        for node in ast.walk(tree)
    )

    num_imports = sum(
        isinstance(node, (ast.Import, ast.ImportFrom))
        for node in ast.walk(tree)
    )

    num_try = sum(
        isinstance(node, ast.Try)
        for node in ast.walk(tree)
    )

    return {
        "loops": num_loops,
        "functions": num_functions,
        "ifs": num_ifs,
        "imports": num_imports,
        "try_blocks": num_try,
        "lines": len(code.splitlines()),
        "syntax_error": syntax_error
    }