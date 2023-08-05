click_ is a framework to simplify writing composable commands for
command-line tools. This package extends the click_ functionality
by adding support for commands that use configuration files.

.. _click: https://click.pocoo.org/

EXAMPLE:

A configuration file, like:

.. code-block:: INI

    # -- FILE: foo.ini
    [foo]
    flag = yes
    name = Alice and Bob
    numbers = 1 4 9 16 25
    filenames = foo/xxx.txt
        bar/baz/zzz.txt

    [person.alice]
    name = Alice
    birthyear = 1995

    [person.bob]
    name = Bob
    birthyear = 2001

can be processed with:

.. code-block:: python

    # EXAMPLE:
    # -- FILE: example_command_with_configfile.py (ALL PARTS: simplified)
    from click_configfile import ConfigFileReader, Param, SectionSchema
    from click_configfile import matches_section
    import click

    class ConfigSectionSchema(object):
        """Describes all config sections of this configuration file."""

        @matches_section("foo")
        class Foo(SectionSchema):
            name    = Param(type=str)
            flag    = Param(type=bool, default=True)
            numbers = Param(type=int, multiple=True)
            filenames = Param(type=click.Path(), multiple=True)

        @matches_section("person.*")   # Matches multiple sections
        class Person(SectionSchema):
            name      = Param(type=str)
            birthyear = Param(type=click.IntRange(1990, 2100))


    class ConfigFileProcessor(ConfigFileReader):
        config_files = ["foo.ini", "foo.cfg"]
        config_section_schemas = [
            ConfigSectionSchema.Foo,     # PRIMARY SCHEMA
            ConfigSectionSchema.Person,
        ]

        # -- SIMPLIFIED STORAGE-SCHEMA:
        #   section:person.*        -> storage:person.*
        #   section:person.alice    -> storage:person.alice
        #   section:person.bob      -> storage:person.bob

        # -- ALTERNATIVES: Override ConfigFileReader methods:
        #  * process_config_section(config_section, storage)
        #  * get_storage_name_for(section_name)
        #  * get_storage_for(section_name, storage)


    # -- COMMAND:
    CONTEXT_SETTINGS = dict(default_map=ConfigFileProcessor.read_config())

    @click.command(context_settings=CONTEXT_SETTINGS)
    @click.option("-n", "--number", "numbers", type=int, multiple=True)
    @click.pass_context
    def command_with_config(ctx, numbers):
        # -- ACCESS ADDITIONAL DATA FROM CONFIG FILES: Using ctx.default_map
        for person_data_key in ctx.default_map.keys():
            if not person_data_key.startswith("person."):
                continue
            person_data = ctx.default_map[person_data_key]
            process_person_data(person_data)    # as dict.


