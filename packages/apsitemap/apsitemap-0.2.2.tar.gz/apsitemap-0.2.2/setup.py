from setuptools import setup, find_packages

install_requires = [
    "requests",
    "pyquery",
    "docopt",
    "colorama",
    "pytest",
]

setup(
    name='apsitemap',
    version='0.2.2',
    packages=find_packages(),
    scripts=[
        "./bin/apsitemap"
    ],
    url='https://github.com/gamelife1314/sitemap',
    license='MIT',
    author='Gamelife',
    author_email='fudenglong1417@gmail.com',
    description='python3 website sitemap generator tool!',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.5",
    ],
    platforms=["all"],
    tests_require=["pytest"],
)
