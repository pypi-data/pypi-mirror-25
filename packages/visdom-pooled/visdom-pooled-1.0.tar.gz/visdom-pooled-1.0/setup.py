from setuptools import setup

__VERSION__ = "1.0"

setup(
    name="visdom-pooled",
    version=__VERSION__,
    description="Slightly More Efficient Visdom Wrapper",
    url="https://github.com/kaniblu/visdom-pooled",
    author="Kang Min Yoo",
    author_email="k@nib.lu",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    keywords="visdom deeplearning visualization pooled",
    packages=["visdom_pooled"],
    install_requires=[
        "visdom",
        "numpy"
    ]
)
