from setuptools import setup, find_packages


setup(
    name="punk",

    version="1.1.0",

    description="Primitives for Uncovering New Knowledge.",
    long_description="Machine Learning pipeline elements.",

    url="https://github.com/NewKnowledge/punk",

    author="New Knowledge",
    author_email="support@newknowledge.io",

    license="MIT",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.6",

        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],

    keywords="TA1 primitive, feature selection, novelty detection",


    packages=find_packages(exclude=['tests']),

    install_requires=["numpy", "scikit-learn", "scipy", "python-dateutil"],

    entry_points = {
        'd3m.primitives': [
            'distil.PCAFeatures = punk.feature_selection.pca:PCAFeatures',
            'distil.RFFeatures = punk.feature_selection.rf:RFFeatures',
            'distil.Heteroscedasticity = punk.novelty_detection.heteroscedasticity:HeteroscedasticityTest',
            'distil.AggregateByCategory = punk.aggregator.aggregateByCategory:AggregateByCategory',
            'distil.AggregateByDateTime = punk.aggregator.aggregateByDateTime:AggregateByDateTime',
            'distil.AggregateByNumericRange = punk.aggregator.aggregateByNumericRange:AggregateByNumericRange',
            'distil.CleanDates = punk.preppy.cleanDates:CleanDates',
            'distil.CleanNumbers = punk.preppy.cleanNumbers:CleanNumbers',
            'distil.CleanStrings = punk.preppy.cleanStrings:CleanStrings'
        ],
    },

)
