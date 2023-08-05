from setuptools import setup, find_packages
import os

HERE = os.path.abspath(os.path.dirname(__file__))
def get_long_description():
    dirs = [ HERE ]
    if os.getenv("TRAVIS"):
        dirs.append(os.getenv("TRAVIS_BUILD_DIR"))

    long_description = ""

    for d in dirs:
        rst_readme = os.path.join(d, "README.rst")
        if not os.path.exists(rst_readme):
            continue

        with open(rst_readme) as fp:
            long_description = fp.read()
            return long_description

    return long_description

long_description = get_long_description()

version = '0.3'
setup(
    name="wordvecspace",
    version=version,
    description="A high performance pure python module that helps in"
                " loading and performing operations on word vector spaces"
                " created using Google's Word2vec tool.",
    long_description=long_description,
    keywords='wordvecspace',
    author='Deep Compute, LLC',
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/wordvecspace",
    download_url="https://github.com/deep-compute/wordvecspace/tarball/%s" % version,
    license='MIT License',
    install_requires=[
        'numpy',
        'pandas',
        'numba',
    ],
    extras_require={
        'cuda': ['pycuda', 'scikit-cuda'],
    },
    package_dir={'wordvecspace': 'wordvecspace'},
    packages=find_packages('.'),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite='test.suite'
)
