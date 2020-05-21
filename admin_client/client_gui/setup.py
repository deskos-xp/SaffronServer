import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SaffronExplorer-NGL",
    version="0.0.3",
    author="Karl Josef Wisdom",
    author_email="k.j.hirner.wisdom@gmail.com",
    description="a tool to access server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deskos-xp/saffronserver",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.6',
    install_requires=[
        'python-dotenv',
        'PyQt5',
        'requests',
        'colored' 
    ]
    )
