# from ChatGPT

def preprocess_list_indexing(expr, local_vars):
    local_vars = dict(local_vars)  # 원본 locals 훼손 방지

    pattern = r"\b([A-Za-z_]\w*)\[(\d+)\]"

    def replace(match):
        name = match.group(1)      # TPSL
        index = int(match.group(2)) # 0

        if name not in local_vars:
            raise NameError(f"{name} 변수가 locals에 없음")

        value = local_vars[name][index]

        new_name = f"{name}_{index}"
        local_vars[new_name] = value

        return new_name

    new_expr = re.sub(pattern, replace, expr)

    return new_expr, local_vars

class _if:
    def __init__(self, condition):
        self.condition = condition

    def __getitem__(self, expr_pair):
        frame = inspect.currentframe().f_back
        local_vars = frame.f_locals

        parts = expr_pair.split(",", 1)

        if len(parts) != 2:
            raise ValueError("형식: 'expr1, expr2' 이어야 함")

        true_expr, false_expr = map(str.strip, parts)

        cond = self.condition() if callable(self.condition) else self.condition
        selected = true_expr if cond else false_expr

        selected, local_vars = preprocess_list_indexing(selected, local_vars)

        return sympify(selected, locals=local_vars)
