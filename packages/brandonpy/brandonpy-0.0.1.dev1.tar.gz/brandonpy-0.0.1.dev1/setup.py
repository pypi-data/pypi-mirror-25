from setuptools import setup, find_packages

setup(
	name="brandonpy",
	version="0.0.1.dev1",
	description="A sample Python project",
	long_description=None,
	url= "https://github.com/byu-dml/brandonpy",
	author="Brandon Schoenfeld",
	author_email="bsjchoenfeld@byu.edu",
	license="MIT",
	classifiers=[
		"Programming Language :: Python :: 3.5",
	],
	keywords="brandon brandonpy sample test",
	packages=find_packages(),
	install_requires=["tqdm"],
	python_requires="~=3.5",
)
