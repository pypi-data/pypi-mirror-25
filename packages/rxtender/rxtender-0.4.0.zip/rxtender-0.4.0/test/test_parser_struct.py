from unittest import TestCase

from rxtender.rxtender import parse_idl

class ParserStructTestCase(TestCase):

    def test_struct(self):
        rxt = '''struct Foo {
            field1: u32;
            field2: i32;
        }'''
        expected_ast = [{
            'stream': None,
            'struct': {
                'identifier': 'Foo',
                'field': [{
                    'identifier': 'field1',
                    'type': 'u32'
                },{
                    'identifier': 'field2',
                    'type': 'i32'
                }]
            }
        }]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_all_types(self):
        rxt = '''struct Foo {
            field1: u32;
            field2: i32;
            field3: u64;
            field4: i64;
            field5: bool;
            field6: double;
            field7: string;
        }'''
        expected_ast = [{
            'stream': None,
            'struct': {
                'identifier': 'Foo',
                'field': [{
                    'identifier': 'field1',
                    'type': 'u32'
                },{
                    'identifier': 'field2',
                    'type': 'i32'
                },{
                    'identifier': 'field3',
                    'type': 'u64'
                },{
                    'identifier': 'field4',
                    'type': 'i64'
                },{
                    'identifier': 'field5',
                    'type': 'bool'
                },{
                    'identifier': 'field6',
                    'type': 'double'
                },{
                    'identifier': 'field7',
                    'type': 'string'
                }]
            }
        }]
        ast = parse_idl(rxt)
        self.assertEqual(expected_ast, ast)

    def test_invalid_type(self):
        rxt = '''struct Foo {
            field1: u32;
            field2: something;
        }'''
        ast = parse_idl(rxt)
        self.assertEqual(None, ast)
