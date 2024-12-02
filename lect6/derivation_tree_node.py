class DerivationTreeNode:
    def __init__(self, value, children):
        self.value = value
        self.children = children if children is not None else []

    def get_value(self):
        return self.value

    def get_children(self):
        return self.children

    def all_terminals(self):
        if not self.get_children():
            return self.get_value()

        result = []
        for child in self.get_children():
            result.append(child.all_terminals())

        return ''.join(result)

    def deep_copy(self):
        # Рекурсивно копируем каждого ребенка
        copied_children = [child.deep_copy() for child in self.children]
        # Возвращаем новый экземпляр DerivationTreeNode с копированным значением и детьми
        return DerivationTreeNode(self.value, copied_children)

    def __str__(self):
        return f"DerivationTreeNode{{value='{self.value}', children={self.children}}}"