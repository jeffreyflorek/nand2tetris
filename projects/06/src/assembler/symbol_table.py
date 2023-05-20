#!/usr/bin/env python3


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_entry(self, symbol, address):
        self.symbols[symbol] = address

    def contains(self, symbol):
        return symbol in self.symbols

    def get_address(self, symbol):
        if symbol in self.symbols:
            return self.symbols[symbol]
        else:
            raise KeyError("Symbol not found: " + symbol)
