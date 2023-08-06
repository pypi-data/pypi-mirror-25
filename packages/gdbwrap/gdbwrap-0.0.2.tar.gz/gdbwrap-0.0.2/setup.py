import setuptools

setuptools.setup(
        name='gdbwrap',
        version='0.0.2',
        packages=setuptools.find_packages(),
        description='Wrapper for graph database queries.',
        url='https://github.com/danielcouch/gdbwrap',
        author='Daniel Couch',
        author_email='danielcouch1864@gmail.com',
        install_requires=['gremlinpython', 'neo4j-driver'],
        license='MIT')
