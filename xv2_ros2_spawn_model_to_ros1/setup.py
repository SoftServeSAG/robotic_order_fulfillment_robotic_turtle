from setuptools import setup

package_name = 'xv2_ros2_spawn_model_to_ros1'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Yuriy Fedyuk',
    author_email='yfedi@softserveinc.com',
    maintainer='Yuriy Fedyuk',
    maintainer_email='yfedi@softserveinc.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='A simple ROS2 Python package',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
	        'spawn = xv2_ros2_spawn_model_to_ros1.spawn_model:spawn'
        ],
    },
)