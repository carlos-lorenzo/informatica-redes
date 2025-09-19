from __future__ import annotations
from dataclasses import dataclass, field

# Dictionary of supported operators, ordered by BIDMAS precedence.
# Each operator is mapped to its corresponding Python function.
OPERATORS: dict[str, callable] = {
    "^": lambda x, y: x ** y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "%": lambda x, y: x % y,
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
    "s": lambda x, y: x - y,
}
# Reverse the order so higher precedence operators are found first in parsing.
OPERATORS = dict(reversed(list(OPERATORS.items())))


@dataclass
class Node:
    """
    Represents a node in the expression tree.

    Each node can be either:
    - a numeric value (leaf node)
    - an operator with child nodes (internal node)
    """
    expression: str = field(default="0")
    parent_node: Node = field(default=None)

    value: float = field(default=0, init=False)
    is_numeric: bool = field(default=False, init=False)
    operator: str = field(default="", init=False)
    operation: callable = field(default=None, init=False)
    children: tuple[Node] = field(default_factory=tuple, init=False)

    def __post_init__(self) -> None:
        """
        Initialize the node by determining if it's numeric or an operator node.
        """
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
        """
        String representation for debugging.
        """
        if self.children:
            return f"<Node: {self.operator.center(3).join([child.expression for child in self.children])}>"
        return f"<Leaf Node: {self.expression}>"

    @staticmethod
    def contained_operator(expression: str) -> str:
        """
        Returns the first operator found in the expression, or empty string if none.
        """
        for operator, _ in OPERATORS.items():
            if operator in expression:
                return operator
        return ""

    def set_operator(self, operator: str) -> None:
        """
        Set the operator and its corresponding function for this node.
        """
        if not operator in OPERATORS.keys():
            raise NameError(f"\"{operator}\" operator not defined")
        self.operator = operator
        self.operation = OPERATORS.get(operator)

    def collapse(self) -> None:
        """
        Collapse this node by evaluating its operation on its children.
        Converts the node into a numeric leaf node.
        """
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
    """
    Calculator class that builds and evaluates an expression tree.
    """
    nodes: list[Node] = field(default_factory=list, init=False)

    def __getitem__(self, key) -> Node:
        return self.nodes[key]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __delitem__(self, key):
        del self.nodes[key]

    def __repr__(self) -> str:
        """
        String representation of the expression tree.
        """
        def traverse(node: Node) -> str:
            if not node.children:
                return f"{node}"
            children = [traverse(child) for child in node.children]
            return f"{node.expression} (\n{', '.join(children)}\n)"
        return traverse(self.root)

    @property
    def root(self) -> Node:
        """
        Returns the root node of the expression tree.
        """
        return self.nodes[0]

    def propagate_single_node(self, prev_node: Node) -> Node:
        """
        Splits a node's expression into child nodes if it contains an operator.
        """
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
        """
        Recursively propagate the tree, splitting nodes into children as needed.
        """
        def traverse(node: Node):
            if not node.children:
                self.propagate_single_node(node)
            for child in node.children:
                traverse(child)
            return node
        return traverse(self.root)

    def collapse_tree(self):
        """
        Recursively collapse the tree, evaluating all operations bottom-up.
        """
        def collapse_node(node):
            if node.children:
                for child in node.children:
                    collapse_node(child)
                node.collapse()
        collapse_node(self.root)
        # After collapsing, keep only the root node
        self.nodes = [self.root]

    @property
    def _result(self) -> float:
        """
        Returns the result of the evaluated expression.
        """
        if not self.root.value:
            self.propagate_tree()
            self.collapse_tree()
        return self.root.value

    def evaluate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression and return the result as a string.
        """
        self.nodes.append(Node(expression))
        self.propagate_single_node(self.nodes[0])
        output = f"{expression} = {self._result}"
        self.nodes = []
        return output


def main() -> None:
    """
    Main loop for the calculator program.
    Prompts the user for expressions and prints results.
    """
    calculator = Calculator()
    expression = "hola rafa"
    while expression[0].lower() != "f":
        expression = input("Enter expression to be evaluated: ")
        print(f"{calculator.evaluate(expression)}\n")
    return


if __name__ == "__main__":
    main()
