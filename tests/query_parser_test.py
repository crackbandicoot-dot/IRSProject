import pytest

from QueryParser import query_parser
from Contracts.QueryNodes import AndNode, HedgeNode, NotNode, OrNode, TermNode
from Errors.QueryError.query_error import QueryError

def assert_is_term(node: TermNode, expected_term: str) -> None:
    assert isinstance(node, TermNode)
    assert node.term == expected_term

def test_parse_single_term() -> None:
    ast = query_parser.parse("apple")
    import typing
    assert_is_term(typing.cast(TermNode, ast), "apple")

def test_parse_or_has_lower_precedence_than_and() -> None:
    ast = query_parser.parse("apple OR banana AND cherry")
    import typing

    assert isinstance(ast, OrNode)
    ast = typing.cast(OrNode, ast)
    assert_is_term(typing.cast(TermNode, ast.left), "apple")
    assert isinstance(ast.right, AndNode)
    right = typing.cast(AndNode, ast.right)
    assert_is_term(typing.cast(TermNode, right.left), "banana")
    assert_is_term(typing.cast(TermNode, right.right), "cherry")

def test_parse_parentheses_override_precedence() -> None:
    ast = query_parser.parse("( apple OR banana ) AND cherry")
    import typing

    assert isinstance(ast, AndNode)
    ast = typing.cast(AndNode, ast)
    assert isinstance(ast.left, OrNode)
    left = typing.cast(OrNode, ast.left)
    assert_is_term(typing.cast(TermNode, left.left), "apple")
    assert_is_term(typing.cast(TermNode, left.right), "banana")
    assert_is_term(typing.cast(TermNode, ast.right), "cherry")

def test_parse_not_binds_tightly() -> None:
    ast = query_parser.parse("NOT apple AND banana")
    import typing

    assert isinstance(ast, AndNode)
    ast = typing.cast(AndNode, ast)
    assert isinstance(ast.left, NotNode)
    left = typing.cast(NotNode, ast.left)
    assert_is_term(typing.cast(TermNode, left.child), "apple")
    assert_is_term(typing.cast(TermNode, ast.right), "banana")

def test_parse_hedge_wraps_unary_expression() -> None:
    ast = query_parser.parse("VERY apple")
    import typing

    assert isinstance(ast, HedgeNode)
    ast = typing.cast(HedgeNode, ast)
    assert ast.hedge_keyword == "VERY"
    assert_is_term(typing.cast(TermNode, ast.child), "apple")

def test_parse_hedge_and_not_chain_right_associatively() -> None:
    ast = query_parser.parse("VERY NOT apple")
    import typing

    assert isinstance(ast, HedgeNode)
    ast = typing.cast(HedgeNode, ast)
    assert ast.hedge_keyword == "VERY"
    assert isinstance(ast.child, NotNode)
    child = typing.cast(NotNode, ast.child)
    assert_is_term(typing.cast(TermNode, child.child), "apple")

def test_parse_nested_parentheses() -> None:
    ast = query_parser.parse("(   apple AND(banana OR NOT cherry))")
    import typing

    assert isinstance(ast, AndNode)
    ast = typing.cast(AndNode, ast)
    assert_is_term(typing.cast(TermNode, ast.left), "apple")
    assert isinstance(ast.right, OrNode)
    right = typing.cast(OrNode, ast.right)
    assert_is_term(typing.cast(TermNode, right.left), "banana")
    assert isinstance(right.right, NotNode)
    right_right = typing.cast(NotNode, right.right)
    assert_is_term(typing.cast(TermNode, right_right.child), "cherry")

def test_parse_raises_for_missing_operator_between_terms() -> None:
    with pytest.raises(QueryError):
        query_parser.parse("apple banana")

def test_parse_raises_for_unclosed_parenthesis() -> None:
    with pytest.raises(QueryError):
        query_parser.parse("( apple AND banana")

def test_parse_raises_for_uppercase_term_token() -> None:
    with pytest.raises(QueryError):
        query_parser.parse("APPLE")

