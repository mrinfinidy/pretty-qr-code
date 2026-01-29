from setuptools import setup

setup(
    name='pretty-qr-code',
    version='1.0',
    author="afkdev8",
    author_email="mail@afkdev8.com",
    description="A tool which generates pretty QR codes.",
    license="MIT",
    url="https://github.com/mrinfinidy/pretty-qr-code",
    package_dir={"": "src"},
    py_modules=["qr_code_generator", "entrypoint", "const"],
    install_requires=[
        'qrcode',
        'pillow'
    ],
    entry_points={
        'console_scripts': [
            'qrcode-pretty = entrypoint:main',
        ]
    },
)
