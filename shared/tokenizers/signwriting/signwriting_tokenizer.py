import re
from itertools import chain
from typing import List

from shared.signwriting.signwriting import fsw_to_sign, SignSymbol
from shared.tokenizers.base_tokenizer import BaseTokenizer


class SignWritingTokenizer(BaseTokenizer):

    def __init__(self, starting_index=None):
        super().__init__(tokens=self.tokens(), starting_index=starting_index)

    def tokens(self):
        box_symbols = ["B", "L", "M", "R"]

        base_symbols = ["S" + hex(i)[2:] + hex(j)[2:] for i in range(0x10, 0x38 + 1) for j in range(0x0, 0xf + 1)]
        base_symbols.remove("S38c")
        base_symbols.remove("S38d")
        base_symbols.remove("S38e")
        base_symbols.remove("S38f")

        rows = ["r" + hex(j)[2:] for j in range(0x0, 0xf + 1)]
        cols = ["c0", "c1", "c2", "c3", "c4", "c5"]

        positions = ["p" + str(p) for p in range(250, 750)]

        return list(chain.from_iterable([box_symbols, base_symbols, rows, cols, positions]))

    def tokenize_symbol(self, symbol: SignSymbol):
        if symbol["symbol"] in ["B", "L", "M", "R"]:
            yield symbol["symbol"]
        else:
            yield symbol["symbol"][:4]  # Break symbol down
            num = int(symbol["symbol"][4:], 16)
            yield "c" + hex(num // 0x10)[2:]
            yield "r" + hex(num % 0x10)[2:]

        yield "p" + str(symbol["position"][0])
        yield "p" + str(symbol["position"][1])

    def text_to_tokens(self, fsw: str) -> List[str]:
        signs = [fsw_to_sign(f) for f in fsw.split(" ")]
        for sign in signs:
            yield from self.tokenize_symbol(sign["box"])
            for symbol in sign["symbols"]:
                yield from self.tokenize_symbol(symbol)

    def tokens_to_text(self, tokens: List[str]) -> str:
        tokenized = " ".join(tokens)
        tokenized = re.sub(r'p(\d*) p(\d*)', r'\1x\2', tokenized)
        tokenized = re.sub(r'c(\d)\d? r(.)', r'\1\2', tokenized)
        tokenized = re.sub(r'c(\d)\d?', r'\1 0', tokenized)
        tokenized = re.sub(r'r(.)', r'0\1', tokenized)

        tokenized = tokenized.replace(' ', '')
        tokenized = re.sub(r'(\d)M', r'\1 M', tokenized)

        return tokenized


if __name__ == "__main__":
    tokenizer = SignWritingTokenizer()
    print(tokenizer.tokens_to_text(
        "M p500 p500 S203 r0 p492 p438 S192 r0 p492 p475 S119 r0 p486 p500 S1f0 c0 r0 p478 p540 S14a r0 p492 p565".split(
            " ")))
