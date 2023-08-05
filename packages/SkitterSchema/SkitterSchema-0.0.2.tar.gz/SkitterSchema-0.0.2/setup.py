from setuptools import setup

setup(name='SkitterSchema',
      version='0.0.2',
      description='OSN schema for online social networks.',
      url='https://github.com/manoelhortaribeiro/SkitterSchema',
      download_url='https://github.com/manoelhortaribeiro/annotated_bibliography/dist/annotated_bibliography-0.1.tar.gz',
      author='Manoel Horta Ribeiro',
      author_email='manoelhortaribeiro@gmail.com',
      license='MIT',
      packages=['SkitterSchema'],
      keywords='ORM schema online social network',
      install_requires=['sqlalchemy'],
      include_package_data=True,
      zip_safe=False)
