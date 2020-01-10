from setuptools import setup, find_packages

#with open('README.md') as f:
#    long_description = f.read()

setup(
    name='testdb',
    version='0.1.0',
    author='Ilja Everilä',
    author_email='saarni@gmail.com',
    maintainer='Ilja Everilä',
    maintainer_email='saarni@gmail.com',
    description='Test tool for various DBMS, and SQLAlchemy',
    #long_description=long_description,
    #long_description_content_type='text/markdown',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'sqlalchemy',
    ],
    extras_require={
        'postgres': [
            'docker',
            'psycopg2-binary'
        ],
        'mysql': [
            'docker',
            'pymysql',
            'mysql-connector-python',
            'mysqlclient'
        ],
        'mssql': [
            'docker',
            'pymssql',
            'python-tds',
            'pyodbc'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Linux',
    ],
)
