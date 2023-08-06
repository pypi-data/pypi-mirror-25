from distutils.core import setup
setup(
  name = 'pwmlight',
  packages = ['pwmlight'], # this must be the same as the name above
  version = '0.1',
  description = 'Controls for PWM controlled Finder dimmer (0-10V)',
  author = 'Max van Rooijen',
  author_email = 'max@triangle1.net',
  url = 'https://github.com/elmexdechileen/pwmlight', # use the URL to the github repo
  download_url = 'https://github.com/elmexdechileen/pwmlight/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['pwm', 'home automation', 'hass'], # arbitrary keywords
  classifiers = []
)
