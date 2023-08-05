from unittest import TestCase

from rxtender.rxtender import parse_idl

class ParserStreamTestCase(TestCase):

    def test_no_arg_stream(self):
        rxt = 'stream Foo() -> Stream<BarItem, FooError>;'
        expected_ast = [{

            'stream': {
                'arg': [],
                'identifier': 'Foo',
                'item_identifier': 'BarItem',
                'error_identifier': 'FooError'
            },
            'struct': None,
        }]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_single_arg_stream(self):
        rxt = 'stream Foo(one: i32) -> Stream<BarItem, FooError>;'
        expected_ast = [{
            'struct': None,
            'stream': {
                'arg': [{
                    'identifier': 'one',
                    'type': 'i32'
                }],
                'identifier': 'Foo',
                'item_identifier': 'BarItem',
                'error_identifier': 'FooError'
            }
        }]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_multi_arg_stream(self):
        rxt = 'stream Foo(one: i32, two: i32, three: i32) -> Stream<BarItem,FooError>;'
        expected_ast = [{
            'struct': None,
            'stream': {
                'arg': [{
                    'identifier': 'one',
                    'type': 'i32'
                }, {
                    'identifier': 'two',
                    'type': 'i32'
                },{
                    'identifier': 'three',
                    'type': 'i32'
                }],
                'identifier': 'Foo',
                'item_identifier': 'BarItem',
                'error_identifier': 'FooError'
            }
        }]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_two_streams(self):
        rxt = '''stream Foo(one: i32) -> Stream<FooItem, FooError>;
            stream Bar(one: i32) -> Stream<BarItem, BarError>;
        '''
        expected_ast = [{
            'struct': None,
            'stream': {
                'arg': [{
                    'identifier': 'one',
                    'type': 'i32'
                }],
                'identifier': 'Foo',
                'item_identifier': 'FooItem',
                'error_identifier': 'FooError'
            }
        },
        {
            'struct': None,
            'stream': {
                'arg': [{
                    'identifier': 'one',
                    'type': 'i32'
                }],
                'identifier': 'Bar',
                'item_identifier': 'BarItem',
                'error_identifier': 'BarError'
            }
        }]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)
