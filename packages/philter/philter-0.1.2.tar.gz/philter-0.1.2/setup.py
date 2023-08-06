from setuptools import setup

setup(
    name='philter',    # This is the name of your PyPI-package.
    version='0.1.2',  # Update the version number for new releases
    packages=['philter'],
    #include_package_data=True,
    package_data={'philter': ['whitelist.pkl'],
    },
    entry_points={
        'console_scripts': [
            'philter = philter.phi_reducer:main',
            'philter-annotation = philter.annotation:main',
            'philter-eval = philter.eval:main']
            },
        # The name of your scipt, and also the command you'll be using for calling it
    zip_safe = False,
    install_requires=[
          'nltk',
          'spacy'
      ],
    author='UCSF-ICHS',
    author_email='beaunorgeot@gmail.com'
)
