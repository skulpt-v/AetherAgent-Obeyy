import ast
import operator


class Calculator:
    """Güvenli matematiksel işlem motoru."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression: str) -> float:
        """Matematiksel ifadeyi güvenli şekilde hesaplar."""

        if not expression or not expression.strip():
            raise ValueError("İfade boş olamaz.")

        try:
            tree = ast.parse(
                expression,
                mode="eval"
            )

            return self._evaluate(tree.body)

        except ZeroDivisionError:
            raise ValueError("Sıfıra bölme yapılamaz.")

        except Exception as error:
            raise ValueError(
                f"Geçersiz matematiksel ifade: {error}"
            )

    def _evaluate(self, node):
        """AST düğümünü güvenli şekilde değerlendirir."""

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Sadece sayılar kullanılabilir.")

        if isinstance(node, ast.BinOp):
            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Bu işlem desteklenmiyor."
                )

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operator_function(left, right)

        if isinstance(node, ast.UnaryOp):
            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Bu işlem desteklenmiyor."
                )

            operand = self._evaluate(node.operand)

            return operator_function(operand)

        raise ValueError(
            "Geçersiz veya desteklenmeyen ifade."
        )

