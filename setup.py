from cx_Freeze import setup, Executable

include_files = [('resources/metacardtypes.json', 'resources/metacardtypes.json'),
                 # ('resources/user.properties', 'resources/user.properties'),
                 ('resources/wordsEn.txt', 'resources/wordsEn.txt'),
                 ('DDFLoadTest.py', 'DDFLoadTest.py')]

setup(
    name="DDF Load Test",
    version="0.1",
    description="A DDF Load test tool using locustio.",
    options={
        'build_exe': {
            'packages': ['encodings', 'asyncio', 'jinja2', 'flask'],
            'include_files': include_files
        },
    },
    executables=[Executable("DDFLoadTest.py")]
)
