from setuptools import setup

setup(name='SkitterCrawler',
      version='0.0.1',
      description='Generic packages with Crawlers for OSNs',
      url='https://github.com/manoelhortaribeiro/SkitterCrawler',
      download_url='https://github.com/manoelhortaribeiro/SkitterCrawler',
      author='Manoel Horta Ribeiro',
      author_email='manoelhortaribeiro@gmail.com',
      license='MIT',
      packages=['SkitterCrawler'],
      keywords='Online social network crawler utilities',
      install_requires=['sqlalchemy', 'SkitterSchema', 'tweepy', 'numpy'],
      entry_points={
            'console_scripts': ['rw_crawler=SkitterCrawler.random_walk_crawler:_random_walk_crawler']
      },
      include_package_data=True,
      zip_safe=False)
