from setuptools import setup

setup(name='serialDevice',
	version='0.2',
	description='Simple class to abstract a device connected to a USB port',
	url='http://github.com/rgmaidana/serialDevice',
	author='Renan Maidana',
	author_email='renanmaidana@gmail.com',
	license='MIT',
	packages=['serialDevice'],
	install_requires=[
		'pyserial',
	],
	zip_safe=False
)
