from __future__ import annotations
from dataclasses import dataclass, field


# Ordered according to BIDMAS
OPERATORS: dict[str, callable] = {
    "^": lambda x, y: x ** y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "%": lambda x, y: x % y,
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
}

OPERATORS = dict(reversed(list(OPERATORS.items())))


@dataclass
class Node:
    expression: str = field(default="0")
    parent_node: Node = field(default=None)

    value: float = field(default=0, init=False)
    is_numeric: bool = field(default=False, init=False)
    operator: str = field(default="", init=False)
    operation: callable = field(default=None, init=False)
    children: tuple[Node] = field(default_factory=tuple, init=False)

    def __post_init__(self) -> None:
        self.operator = self.contained_operator(self.expression)
        self.operation = OPERATORS.get(self.operator)
        try:
            self.value = float(self.expression)

            self.is_numeric = True
        except ValueError:
            self.is_numeric = False
        except Exception as e:
            raise e

    def __repr__(self) -> str:
        if self.children:
            return f"<Node: {self.operator.center(3).join([child.expression for child in self.children])}>"

        return f"<Leaf Node: {self.expression}>"

    @staticmethod
    def contained_operator(expression: str) -> str:
        for operator, _ in OPERATORS.items():
            if operator in expression:
                return operator

        return ""

    def set_operator(self, operator: str) -> None:
        if not operator in OPERATORS.keys():
            raise NameError(f"\"{operator}\" operator not defined")

        self.operator = operator
        self.operation = OPERATORS.get(operator)

    def collapse(self) -> None:
        try:
            self.value = self.operation(
                *[child.value for child in self.children])
            self.expression = str(self.value)
            self.children = ()
            self.is_numeric = True
            self.operator = ""
            self.operation = None
        except ZeroDivisionError:
            print("Zero division encountered, ignoring...")
            self.value = 0
            self.expression = "0"
            self.children = ()
            self.is_numeric = True
            self.operator = ""
            self.operation = None


@dataclass
class Calculator:
    nodes: list[Node] = field(default_factory=list, init=False)

    def __getitem__(self, key) -> Node:
        return self.nodes[key]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __delitem__(self, key):
        del self.nodes[key]

    def __repr__(self) -> str:
        def traverse(node: Node) -> str:
            if not node.children:
                return f"{node}"
            children = [traverse(child) for child in node.children]
            return f"{node.expression} (\n{', '.join(children)}\n)"

        return traverse(self.root)

    @property
    def root(self) -> Node:
        return self.nodes[0]

    def propagate_single_node(self, prev_node: Node) -> Node:
        expression = prev_node.expression
        if prev_node.operator:
            operator_index = expression.index(prev_node.operator)
            side_a: str = expression[:operator_index]
            side_b: str = expression[operator_index+1:]

            new_node_a = Node(side_a, prev_node)
            new_node_b = Node(side_b, prev_node)
            prev_node.children = (new_node_a, new_node_b)

            self.nodes.append(new_node_a)
            self.nodes.append(new_node_b)

            return prev_node

    def propagate_tree(self) -> None:
        def traverse(node: Node):
            if not node.children:
                self.propagate_single_node(node)
                # After propagating, node now has children (if it was an operator)

            for child in node.children:
                traverse(child)
            return node

        return traverse(self.root)

    def collapse_tree(self):
        def collapse_node(node):
            if node.children:
                for child in node.children:
                    collapse_node(child)
                node.collapse()
        collapse_node(self.root)
        # Once its done set root as its only node
        self.nodes = [self.root]

    @property
    def _result(self) -> float:
        if not self.root.value:
            self.propagate_tree()
            self.collapse_tree()
        return self.root.value

    def evaluate(self, expression: str) -> float:
        self.nodes.append(Node(expression))
        self.propagate_single_node(self.nodes[0])
        output = f"{expression} = {self._result}"
        self.nodes = []
        return output


def main() -> None:
    calculator = Calculator()
    expression = "hola rafa"
    while expression[0].lower() != "f":
        expression = input("Enter expression to be evaluated: ")
        print(f"{calculator.evaluate(expression)}\n")
    return


if __name__ == "__main__":
    main()
