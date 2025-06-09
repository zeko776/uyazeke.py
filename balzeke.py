import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}


def eval_expr(expr: str):
    """Evaluate a simple arithmetic expression safely."""
    tree = ast.parse(expr, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):  # for Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant")
        if isinstance(node, ast.Num):  # for Python <3.8
            return node.n
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in OPS:
                return OPS[op_type](_eval(node.left), _eval(node.right))
            raise ValueError(f"Unsupported operator: {op_type}")
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -_eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return _eval(node.operand)
            raise ValueError("Unsupported unary operator")
        raise ValueError(f"Unsupported expression: {type(node)}")

    return _eval(tree.body)


def main():
    print("Basit Hesap Makinesi. Cikmak icin 'q' yazin.")
    while True:
        expr = input("Islem > ").strip()
        if expr.lower() in {"q", "quit", "exit"}:
            break
        if not expr:
            continue
        try:
            result = eval_expr(expr)
        except Exception as exc:
            print("Hata:", exc)
        else:
            print("Sonuc:", result)


if __name__ == "__main__":
    main()
