import unittest

from QueryParser import query_parser
from Contracts.QueryNodes import AndNode, HedgeNode, NotNode, OrNode, TermNode
from Errors.QueryError.query_error import QueryError

class QueryParserApiTests(unittest.TestCase):
    def assertIsTerm(self, node, expected_term):
        self.assertIsInstance(node, TermNode)
        self.assertEqual(node.term, expected_term)

    def test_parse_single_term(self):
        ast = query_parser.parse("apple")
        self.assertIsTerm(ast, "apple")

    def test_parse_or_has_lower_precedence_than_and(self):
        ast = query_parser.parse("apple OR banana AND cherry")

        self.assertIsInstance(ast, OrNode)
        self.assertIsTerm(ast.left, "apple")
        self.assertIsInstance(ast.right, AndNode)
        self.assertIsTerm(ast.right.left, "banana")
        self.assertIsTerm(ast.right.right, "cherry")

    def test_parse_parentheses_override_precedence(self):
        ast = query_parser.parse("( apple OR banana ) AND cherry")

        self.assertIsInstance(ast, AndNode)
        self.assertIsInstance(ast.left, OrNode)
        self.assertIsTerm(ast.left.left, "apple")
        self.assertIsTerm(ast.left.right, "banana")
        self.assertIsTerm(ast.right, "cherry")

    def test_parse_not_binds_tightly(self):
        ast = query_parser.parse("NOT apple AND banana")

        self.assertIsInstance(ast, AndNode)
        self.assertIsInstance(ast.left, NotNode)
        self.assertIsTerm(ast.left.child, "apple")
        self.assertIsTerm(ast.right, "banana")

    def test_parse_hedge_wraps_unary_expression(self):
        ast = query_parser.parse("VERY apple")

        self.assertIsInstance(ast, HedgeNode)
        self.assertEqual(ast.hedge_keyword, "VERY")
        self.assertIsTerm(ast.child, "apple")

    def test_parse_hedge_and_not_chain_right_associatively(self):
        ast = query_parser.parse("VERY NOT apple")

        self.assertIsInstance(ast, HedgeNode)
        self.assertEqual(ast.hedge_keyword, "VERY")
        self.assertIsInstance(ast.child, NotNode)
        self.assertIsTerm(ast.child.child, "apple")

    def test_parse_nested_parentheses(self):
        ast = query_parser.parse("(   apple AND(banana OR NOT cherry))")

        self.assertIsInstance(ast, AndNode)
        self.assertIsTerm(ast.left, "apple")
        self.assertIsInstance(ast.right, OrNode)
        self.assertIsTerm(ast.right.left, "banana")
        self.assertIsInstance(ast.right.right, NotNode)
        self.assertIsTerm(ast.right.right.child, "cherry")

    def test_parse_raises_for_missing_operator_between_terms(self):
        with self.assertRaises(QueryError):
            query_parser.parse("apple banana")

    def test_parse_raises_for_unclosed_parenthesis(self):
        with self.assertRaises(QueryError):
            query_parser.parse("( apple AND banana")

    def test_parse_raises_for_uppercase_term_token(self):
        with self.assertRaises(QueryError):
            query_parser.parse("APPLE")


if __name__ == "__main__":
    unittest.main()
