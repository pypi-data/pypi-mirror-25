from setuptools import setup

setup(
  name = 'simple-telegrambot',
  packages = ['simple-telegrambot'], 
  version = '1.0.1',
  description = 'A simple Telegram bot which sends and receive messages',
  author = 'Usman Mahmood',
  author_email = 'um@blackhole.com',
  url = 'https://github.com/umahmood/simple-telegrambot',
  download_url = 'https://github.com/umahmood/simple-telegrambot/archive/1.0.0.tar.gz', 
  keywords = ['bot', 'telegram'], 
  install_requires=['requests>=2.18.4'],
)
