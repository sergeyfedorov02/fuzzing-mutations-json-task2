class JsonParseError(Exception):
    pass


class JsonParser:
    def __init__(self, source):
        self.source = source
        self.position = 0

    def parse(self):
        result = self.parse_value()
        self.skip_whitespace()
        if self.position < len(self.source):
            raise JsonParseError("Unexpected characters at end of input.")
        return result

    def parse_value(self):
        self.skip_whitespace()
        if self.peek() == '{':
            return self.parse_object()
        elif self.peek() == '[':
            return self.parse_array()
        elif self.peek() == '"':
            return self.parse_string()
        elif self.peek() in '0123456789-':
            return self.parse_number()
        elif self.source.startswith('true', self.position):
            self.position += 4
            return True
        elif self.source.startswith('false', self.position):
            self.position += 5
            return False
        elif self.source.startswith('null', self.position):
            self.position += 4
            return None
        else:
            raise JsonParseError("Invalid value.")

    def parse_object(self):
        self.expect('{')
        members = {}
        while True:
            self.skip_whitespace()
            if self.peek() == '}':
                break
            key = self.parse_string()
            self.skip_whitespace()
            self.expect(':')
            value = self.parse_value()
            members[key] = value
            self.skip_whitespace()
            if self.peek() == '}':
                break
            self.expect(',')
        self.expect('}')
        return members

    def parse_array(self):
        self.expect('[')
        elements = []
        while True:
            self.skip_whitespace()
            if self.peek() == ']':
                break
            elements.append(self.parse_value())
            self.skip_whitespace()
            if self.peek() == ']':
                break
            self.expect(',')
        self.expect(']')
        return elements

    def parse_string(self):
        self.expect('"')
        start = self.position
        while True:
            if self.position >= len(self.source):
                raise JsonParseError("Unterminated string.")
            char = self.source[self.position]
            if char == '"':
                break
            self.position += 1
        value = self.source[start:self.position]
        self.position += 1  # skip the closing '\\"'
        return value

    def parse_number(self):
        start = self.position

        if self.peek() == '-':
            self.position += 1  # Обработка знака

        while self.peek() in '0123456789':
            self.position += 1  # Считываем целую часть

        if self.peek() == '.':  # has decimal
            self.position += 1  # Считываем точку
            while self.peek() in '0123456789':
                self.position += 1  # Считываем дробную часть

        if self.peek() in 'eE':  # has exponent
            self.position += 1  # Считываем 'e' или 'E'
            if self.peek() in '+-':
                self.position += 1  # Считываем знак экспоненты
            while self.peek() in '0123456789':
                self.position += 1  # Считываем экспоненту

        num_str = self.source[start:self.position]  # Получаем полное значение числа

        try:
            return float(num_str)  # Преобразуем строку в число
        except ValueError:
            raise JsonParseError("Invalid number format.")

    def parse_int(self):
        if self.peek() == '0':
            self.position += 1
        else:
            if self.peek() not in '123456789':
                raise JsonParseError("Invalid integer format.")
            while self.peek() in '0123456789':
                self.position += 1

    def parse_fraction(self):
        if not self.peek().isdigit():
            raise JsonParseError("Invalid fraction format.")
        while self.peek().isdigit():
            self.position += 1

    def expect(self, char):
        if self.peek() != char:
            raise JsonParseError(f"Expected '{char}', found '{self.peek()}'.")
        self.position += 1

    def peek(self):
        self.skip_whitespace()
        return self.source[self.position] if self.position < len(self.source) else None

    def skip_whitespace(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1


def loads(input_json):
    parser = JsonParser(input_json)
    parser_res = parser.parse()
    return parser_res


# Пример использования
if __name__ == "__main__":
    json_data1 = '{"name": "John", "age": 30, "city": "New York", "is_student": false, "courses": ["Math", "Science"]}'
    json_data2 = '{ "@-": [ 0e+08 ] }'
    json_data3 = '[ { "": [ { "WU": "" } ], "": null }, "X", [ 10.821 ] ]'
    result = loads(json_data3)
    print(result)