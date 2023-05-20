import pytest
from assembler.symbol_table import SymbolTable


@pytest.mark.parametrize(
    "symbol, address",
    [
        ("test", 0),
        ("this", 10),
    ],
)
def test_add_entry(symbol, address):
    symtab = SymbolTable()
    symtab.add_entry(symbol, address)
    assert symtab.symbols.get(symbol) == address


@pytest.mark.parametrize(
    "symbol, result",
    [
        ("test", True),
        ("this", False),
    ],
)
def test_contains(symbol, result):
    symtab = SymbolTable()
    symtab.add_entry("test", 10)
    assert symtab.contains(symbol) == result


@pytest.mark.parametrize(
    "symbol, address",
    [
        ("test", 0),
        ("this", 10),
    ],
)
def test_get_address(symbol, address):
    symtab = SymbolTable()
    symtab.add_entry(symbol, address)
    assert symtab.get_address(symbol) == address
