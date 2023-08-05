from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='slideseg',
      version='1.1',
      description='segments whole slide images into usable image chips and masks for deep learning',
      long_description=readme(),
      url='https://github.com/btcrabb/SlideSeg',
      author='bcrabb',
      author_email='brendancrabb8388@pointloma.edu',
      packages=['slideseg'],
      scripts=['bin/slideseg-run'],
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7'],
      install_requires=[
          'numpy',
          'tqdm',
          'openslide-python',
          'opencv-python',
          'pexif',
      ],
      zip_safe=False,
      include_package_data=True)