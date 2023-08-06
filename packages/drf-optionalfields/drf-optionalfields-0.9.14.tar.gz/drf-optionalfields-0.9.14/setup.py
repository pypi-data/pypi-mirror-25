from setuptools import setup


classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Intended Audience :: Developers",
    "Framework :: Django",
]

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="drf-optionalfields",
    version="0.9.14",
    description="Fine tuning for serialized fields",
    long_description=long_description,
    packages=["drf_optionalfields"],
    author="Petros G. Sideris",
    author_email="pgsideris@gmail.com",
    license="MIT",
    url="https://github.com/sideris/drf-optionalfields",
    classifiers=classifiers,
    extras_require={
        "dev": [
            "pytest", "pytest-cov", "pytest-django", "coveralls",
            "django", "djangorestframework", "mock_django",
            "setuptools", "wheel",
        ]
    },
)
