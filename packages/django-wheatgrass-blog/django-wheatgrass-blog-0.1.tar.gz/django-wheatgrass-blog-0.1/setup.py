import pypandoc
from setuptools import find_packages, setup
from pip.req import parse_requirements

# Short description
short_description = (
    'django-wheatgrass-blog is a simple blogging platform '
    'designed for the Django Web Framework.'
)

# Read from README.md
# Convert Markdown to reStructuredText
long_description = pypandoc.convert('README.md', 'rst')

# Import dependencies from requirements.txt
requirements_txt = parse_requirements('requirements.txt', session=False)
dependencies = []
for dependency in requirements_txt:
    dependencies.append(str(dependency.req))

setup(
    name='django-wheatgrass-blog',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=short_description,
    long_description=long_description,
    url='https://github.com/FractionalFunction/django-wheatgrass-blog',
    author='Richie Zhang',
    install_requires=dependencies,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
