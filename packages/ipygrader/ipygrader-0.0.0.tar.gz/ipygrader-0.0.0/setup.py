from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='ipygrader',
      version='0.0.0',
      description='Jupyter notebooks gradding using VPL and Moodle',
      long_description='A tool for creating and gradding assignments in the Jupyter Notebook using the Virtual Programming Lab plugging and Moodle',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Education',
        'License :: Free For Educational Use',
        'Topic :: Education :: Testing',
        'Framework :: Jupyter'
      ],
      keywords='Jupyter Moodle Gradding',
      url='http://github.com/jdvelasq/ipygrader',
      author='Juan D. Velasquez',
      author_email='jdvelasq@unal.edu.co',
      license='MIT',
      packages=['ipygrader'],
      include_package_data=True,
      zip_safe=False)
