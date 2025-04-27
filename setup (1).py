from setuptools import setup, find_packages

setup(
    name="arabic-library",
    version="9.3",
    description="مكتبة Python شاملة للمطورين الناطقين بالعربية",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="فريق المكتبة العربية",
    author_email="support@arabic-library.org",
    url="https://github.com/arabic-library/arabic-library",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "sqlalchemy>=1.4.0",
        "aiosqlite>=0.17.0",
        "asyncpg>=0.27.0",
        "motor>=3.0.0",
        "pyjwt>=2.4.0",
        "cryptography>=38.0.0",
        "asyncssh>=2.12.0",
        "click>=8.1.0",
        "websockets>=10.0",
        "aioredis>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "مكتبة = arabic_library:مكتبة"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)