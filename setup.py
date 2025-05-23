from setuptools import setup

setup(
    name='qr-code-generator',
    version='1.0',
    author="Amon Felbermayer",
    author_email="amon.felbermayer@nesto-software.de",
    description="A tool which generates beautiful nesto-branded qr-codes.",
    license="Closed",
    url="https://gitlab.nesto.app/nesto-software/pos-adapter-v2/qr-code-generator",
    package_dir={"": "src"},
    py_modules=["qr_code_generator", "entrypoint"],
    scripts=["src/entrypoint.py"],
    install_requires=[
        'qrcode',
        'PIL'
    ],
)
