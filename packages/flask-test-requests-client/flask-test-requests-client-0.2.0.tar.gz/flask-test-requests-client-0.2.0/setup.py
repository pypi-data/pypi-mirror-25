from setuptools import setup

setup(
    name='flask-test-requests-client',
    version='0.2.0',
    description='A Flask test client which replicates the requests interface.',
    url='http://github.com/jwg4/flask-test-requests-client',
    author='Jack Grahl',
    author_email='jack.grahl@gmail.com',
    license='MIT',
    packages=['frtc'],
    zip_safe=False,
    install_requires=['chardet', 'requests'],
    test_suite="tests",
    tests_require=["flask", "requests"]
)
