import re

from .spec import TokenSpecification, Token, CODE_TOKEN_TYPES, EOF


def tokenize(code, skip_newline=False):
    line_count = code.count("\n") + 1
    eof = Token(EOF, value="", line=line_count, column=len(code))

    token_iter = tokenize_generator(code, skip_newline)
    current_token = next(token_iter, eof)
    code_token = None
    tokens = []
    code_tokens = []
    text_tokens = []

    while current_token != eof:
        if (
            current_token.line == eof.line
            and current_token.column == eof.column
            and current_token.value == ""
        ):
            break

        if current_token.type in CODE_TOKEN_TYPES:
            if code_tokens and current_token.type == code_tokens[-1].type:
                code_tokens.pop()
                code_token = None
            else:
                code_token = current_token
                code_tokens.append(current_token)
                tokens.append(code_token)

            current_token = next(token_iter, eof)

        while current_token != eof and (
            current_token.type == "TEXT"
            or current_token.type == "SPACE"
            or code_token is not None
        ):
            text_tokens.append(current_token)
            current_token = next(token_iter, eof)
            if code_token is not None and current_token.type == code_token.type:
                code_token = None

        if text_tokens:
            concat_text = [t.value for t in text_tokens]
            concat_text_token = Token(
                "TEXT",
                value="".join(concat_text),
                line=text_tokens[0].line,
                column=text_tokens[0].column,
            )
            text_tokens = []
            tokens.append(concat_text_token)

        if current_token != eof:
            tokens.append(current_token)

        current_token = next(token_iter, eof)

    tokens.append(eof)

    return tokens


def tokenize_generator(code, skip_newline=False):
    tok_regex = "|".join(
        "(?P<%s>%s)%s" % token_spec.value for token_spec in list(TokenSpecification)
    )

    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        token_type = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if token_type == "NEWLINE":
            line_start = mo.end()
            line_num += 1
            if skip_newline:
                continue
        yield Token(token_type, value, line_num, column)
