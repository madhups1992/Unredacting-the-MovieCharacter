from setuptools import setup, find_packages

setup(
	name='project1_phase2',
	version='1.0',
	author='Madhu',
	authour_email='madhumitha.pachapalayam.sivasalapathy-1@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
