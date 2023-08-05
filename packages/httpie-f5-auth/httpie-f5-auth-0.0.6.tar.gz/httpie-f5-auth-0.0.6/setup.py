from setuptools import setup

setup(
    name='httpie-f5-auth',
    description='F5 BIG-IQ Auth plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.0.6',
    author='Ivan Mecimore',
    author_email='imecimore@gmail.com',
    license='MIT',
    url='https://github.com/imecimore/httpie-f5-auth',
    download_url='https://github.com/imecimore/httpie-f5-auth',
    py_modules=['httpie_f5_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_f5_auth = httpie_f5_auth:F5AuthPlugin'
        ]
    },
    install_requires=[
        'httpie',
        'requests',
        'requests-f5auth'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
