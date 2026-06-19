import ast
import builtins as builtins_module
def find_undefined_variables(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    defined = set()
    used = set()

    builtins = set(dir(builtins_module))

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined.add(target.id)

        if isinstance(node, ast.FunctionDef):
            defined.add(node.name)
            for arg in node.args.args:
                defined.add(arg.arg)

        if isinstance(node, ast.ClassDef):
            defined.add(node.name)

        if isinstance(node, ast.Import):
            for alias in node.names:
                defined.add(alias.asname or alias.name.split(".")[0])

        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                defined.add(alias.asname or alias.name)

        if isinstance(node, ast.For):
            if isinstance(node.target, ast.Name):
                defined.add(node.target.id)

        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            for generator in node.generators:
                if isinstance(generator.target, ast.Name):
                    defined.add(generator.target.id)

        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)

    undefined = [name for name in used if name not in defined and name not in builtins]

    return undefined

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