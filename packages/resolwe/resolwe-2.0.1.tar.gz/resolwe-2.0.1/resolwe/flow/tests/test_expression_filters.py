# pylint: disable=missing-docstring
from __future__ import absolute_import, division, print_function, unicode_literals

from resolwe.flow.expression_engines import EvaluationError
from resolwe.flow.managers import manager
from resolwe.flow.models import Data, DescriptorSchema, Process, Storage
from resolwe.test import TestCase


class ProcessFieldsTagsTest(TestCase):

    def test_templatetags(self):
        input_process = Process.objects.create(
            name='Input process',
            contributor=self.contributor,
            type='data:test:inputobject:',
            output_schema=[
                {'name': 'test_file', 'type': 'basic:file:'},
            ],
            run={
                'language': 'bash',
                'program': """
mkdir -p path/to
touch path/to/file.txt
re-save-file test_file path/to/file.txt
"""
            }
        )
        descriptor_schema = DescriptorSchema.objects.create(
            name='Test schema',
            slug='test-schema',
            contributor=self.contributor,
            schema=[
                {'name': 'descriptions', 'required': False, 'group': [
                    {'name': 'text', 'type': 'basic:string:'},
                ]}
            ]

        )

        input_data = Data.objects.create(
            name='Input Data object',
            contributor=self.contributor,
            process=input_process,
            descriptor_schema=descriptor_schema,
            descriptor={'descriptions': {'text': 'This is test Data object.'}}
        )

        manager.communicate(verbosity=0)

        process = Process.objects.create(
            name='Test template tags',
            requirements={'expression-engine': 'jinja'},
            contributor=self.contributor,
            type='test:data:templatetags:',
            input_schema=[
                {'name': 'input_data', 'type': 'data:test:inputobject:'},
                {'name': 'input_data_list', 'type': 'list:data:test:inputobject:'},
                {'name': 'spacy', 'type': 'basic:string:'},
            ],
            output_schema=[
                {'name': 'name', 'type': 'basic:string:'},
                {'name': 'id', 'type': 'basic:integer:'},
                {'name': 'type', 'type': 'basic:string:'},
                {'name': 'basename', 'type': 'basic:string:'},
                {'name': 'subtype', 'type': 'basic:string:'},
                {'name': 'yesno', 'type': 'basic:string:'},
                {'name': 'datalookup', 'type': 'basic:integer:'},
                {'name': 'file_url', 'type': 'basic:string:'},
                {'name': 'unsafe', 'type': 'basic:string:'},
                {'name': 'safe', 'type': 'basic:string:'},
                {'name': 'description_text', 'type': 'basic:string:'},
                {'name': 'description_full', 'type': 'basic:json:'},
                {'name': 'list_description_text', 'type': 'basic:string:'},
                {'name': 'list_description_full', 'type': 'basic:json:'},
            ],
            run={
                'language': 'bash',
                'program': """
re-save name {{ input_data | name }}
re-save id {{ input_data | id }}
re-save type {{ input_data | type }}
re-save basename {{ '/foo/bar/moo' | basename }}
re-save subtype {{ 'data:test:inputobject:' | subtype('data:') }}
re-save yesno {{ true | yesno('yes', 'no') }}
re-save datalookup {{ 'input-data-object' | data_by_slug }}
re-save file_url {{ input_data.test_file | get_url }}
re-save unsafe {{ spacy }}
re-save description_text {{ input_data | descriptor('descriptions.text') }}
re-save description_full {{ input_data | descriptor }}
re-save list_description_text {{ input_data_list[0] | descriptor('descriptions.text') }}
re-save list_description_full {{ input_data_list[0] | descriptor }}

function save-safe() {
    re-save safe $1
}
save-safe {{ spacy | safe }}
"""
            }

        )
        data = Data.objects.create(
            name='Data object',
            contributor=self.contributor,
            process=process,
            input={
                'input_data': input_data.pk,
                'input_data_list': [input_data.pk],
                'spacy': 'this has \'some\' spaces',
            },
        )

        manager.communicate(verbosity=0)

        data.refresh_from_db()

        self.assertEqual(data.output['name'], input_data.name)
        self.assertEqual(data.output['id'], input_data.pk)
        self.assertEqual(data.output['type'], input_process.type)
        self.assertEqual(data.output['basename'], 'moo')
        self.assertEqual(data.output['subtype'], 'True')
        self.assertEqual(data.output['yesno'], 'yes')
        self.assertEqual(data.output['datalookup'], input_data.pk)
        self.assertEqual(data.output['file_url'], 'localhost/data/{}/path/to/file.txt'.format(input_data.pk))
        self.assertEqual(data.output['unsafe'], 'this has \'some\' spaces')
        self.assertEqual(data.output['safe'], 'this')
        self.assertEqual(data.output['description_text'], 'This is test Data object.')
        self.assertEqual(data.output['list_description_text'], 'This is test Data object.')

        storage = Storage.objects.get(pk=data.output['description_full'])
        self.assertEqual(storage.json, {'descriptions': {'text': 'This is test Data object.'}})

        storage = Storage.objects.get(pk=data.output['list_description_full'])
        self.assertEqual(storage.json, {'descriptions': {'text': 'This is test Data object.'}})


class ExpressionEngineTest(TestCase):

    def test_jinja_engine(self):
        engine = manager.get_expression_engine('jinja')
        block = engine.evaluate_block('Hello {{ world }}', {'world': 'cruel world'})
        self.assertEqual(block, 'Hello cruel world')
        block = engine.evaluate_block('Hello {% if world %}world{% endif %}', {'world': True})
        self.assertEqual(block, 'Hello world')

        with self.assertRaises(EvaluationError):
            engine.evaluate_block('Hello {% bar')

        expression = engine.evaluate_inline('world', {'world': 'cruel world'})
        self.assertEqual(expression, 'cruel world')
        expression = engine.evaluate_inline('world', {'world': True})
        self.assertEqual(expression, True)
        expression = engine.evaluate_inline('world | yesno("yes", "no")', {'world': False})
        self.assertEqual(expression, 'no')
        expression = engine.evaluate_inline('[1, 2, 3, world]', {'world': 4})
        self.assertEqual(expression, [1, 2, 3, 4])
        expression = engine.evaluate_inline('a.b.c.d', {})
        self.assertEqual(expression, None)
        expression = engine.evaluate_inline('a.b.c().d', {})
        self.assertEqual(expression, None)
        expression = engine.evaluate_inline('a.b.0.d', {'a': {'b': [{'d': 'Hello world'}]}})
        self.assertEqual(expression, 'Hello world')
        expression = engine.evaluate_inline('a.b.0.d', {})
        self.assertEqual(expression, None)

        # Test that propagation of undefined values works.
        expression = engine.evaluate_inline('foo.bar | name | default("bar")', {})
        self.assertEqual(expression, 'bar')
        expression = engine.evaluate_inline('foo.bar | id | default("bar")', {})
        self.assertEqual(expression, 'bar')
        expression = engine.evaluate_inline('foo.bar | type | default("bar")', {})
        self.assertEqual(expression, 'bar')
        expression = engine.evaluate_inline('foo.bar | basename | default("bar")', {})
        self.assertEqual(expression, 'bar')

        # Ensure that filter decorations are correctly copied when decorating filters to
        # automatically propagate undefined values on exceptions.
        expression = engine.evaluate_inline('foo | join(" ")', {'foo': ['a', 'b', 'c']})
        self.assertEqual(expression, 'a b c')
