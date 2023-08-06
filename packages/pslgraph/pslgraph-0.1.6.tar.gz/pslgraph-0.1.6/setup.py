import setuptools

setuptools.setup(
    name = 'pslgraph',

    version = '0.1.6',

    description = 'A PSL TA1 primitive for D3M',
    long_description = 'A PSL TA1 primitive for D3M',

    # The project's main homepage.
    url = 'https://gitlab.datadrivendiscovery.org/dhartnett/psl',

    entry_points={
        'd3m.primitives': [
            'pslgraph = pslgraph.pslgraphprimitive:PSLGraphPrimitive',
        ],
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python :: 3.6',
    ],

    packages = setuptools.find_packages(exclude = ['contrib', 'docs', 'tests']),

    include_package_data = True,

    package_data = {
        'pslgraph.psl-cli': [
            'psl-cli-CANARY.jar',
            'unified.data',
            'unified.psl'
        ]
    },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = ['gevent', 'networkx', 'pandas'],

    python_requires = '>=3.6',
)
