from distutils.core import setup
import setuptools
setup(name='elem',
      packages=['elem'],
      install_requires=['requests', 'GitPython'],
      version='0.0.2',
      description='Tool to correlate published CVE\'s against Enterprise Linux against known exploits.',
      author='Kenneth Evensen',
      author_email='kevensen@redhat.com',
      license='Apache 2.0',
      url='https://github.com/fedoraredteam/elem',
      download_url='https://github.com/fedoraredteam/elem/archive/0.0.2.zip',
      keywords=['cve', 'exploit', 'linux'],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2.7',
      ],
      package_data={'elem': ['exploits/*']},
      scripts=['bin/elem'],
      platforms=['Linux'])
