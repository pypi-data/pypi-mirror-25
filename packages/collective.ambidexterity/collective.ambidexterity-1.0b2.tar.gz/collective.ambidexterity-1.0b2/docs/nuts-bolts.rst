==============================================================================
collective.ambidexterity - Nuts and Bolts
==============================================================================

This is currently a set of explorations of the idea of doing Dexterity views, validators, vocabularies and defaults TTW via scripts in portal_resources.
It's at proof-of-concept stage.
If it works, we can build a plone.app.theming style UI to edit the portal_resources/ambidexterity space.

The general idea is that we will be able to use Dexterity XML to specify a schema like::

    <schema>
      <field name="test_integer_field" type="zope.schema.Int">
        <description/>
        <required>False</required>
        <defaultFactory>collective.ambidexterity.default</defaultFactory>
        <title>Test Integer Field</title>
      </field>
      <field name="test_string_field"
        type="zope.schema.TextLine"
        form:validator="collective.ambidexterity.validate"
      >
        <description/>
        <required>False</required>
        <defaultFactory>collective.ambidexterity.default</defaultFactory>
        <title>Test String Field</title>
      </field>
      <field name="test_choice_field" type="zope.schema.Choice">
        <description/>
        <required>False</required>
        <title>Test Choice Field</title>
        <source>collective.ambidexterity.vocabulary</source>
      </field>
    </schema>

For the Dexterity type "my_simple_type" and we would get::

    portal_resources/ambidexterity/my_simple_type/test_integer_field/default.py
    portal_resources/ambidexterity/my_simple_type/test_string_field/default.py
    portal_resources/ambidexterity/my_simple_type/test_string_field/validate.py
    portal_resources/ambidexterity/my_simple_type/test_choice_field/vocabulary.py

automatically called as appropriate.

The scripts from portal_resources/ambidexterity are executed as untrusted Python.

Defaults
--------

The script is given one value (other than standard builtins):
"context" -- which is either the creation folder if the item is being
added or the item if being edited.

The vocabulary should be assigned to "default" in the script
and should be of the type required by the field.

Vocabularies
------------

The script is given one value (other than standard builtins):
"context" -- which is either the creation folder if the item is being
added or the item if being edited.

The vocabulary should be assigned to "vocabulary" in the script.
It should be a list of values or a list of items (value, title).

Validators
----------

The script is given two values (other than standard builtins):

    * "context" -- which is either the creation folder if the item is being
      added or the item if being edited.

    * "value" -- the field value submitted for validation.

If the validator script determines the value is invalid, it should do
one of the following:

    * print an error message using Python's "print"; or,

    * assign an error message to a variable named "error_message".

If the value is valid, do not do either of the above.
The absence of an error message is taken to mean all is OK.

Views
-----

If a view.pt template file is placed at portal_resources/ambidexterity/content_type/view.portal_type as a text file, it will be usable at @@ambidexterityview.

You may also set other template files and traverse to them at URLs like @@ambidexterityview/custom_file.js.
No matter the extension, they will be handled as page templates.
