import setuptools

setuptools.setup(
    name="yaml_backed_structs",
    version="0.1.0",
    url="https://github.com/dcdanko/YamlBackedPyStructs",

    author="David C. Danko",
    author_email="dcdanko@gmail.com",

    description="Basic python data structures backed by a human editable yaml file",
    long_description=open('README.rst').read(),

    packages=['yaml_backed_structs'],

    install_requires=['PyYAML==3.12'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
