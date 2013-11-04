
from setuptools import find_packages

setup_args = dict(
      name             = 'pyatompaw',
      version          = '1.3.0',
      description      = "A python interface for atompaw.",
     #long_description = long_description,
      author           = "Gabriel Antonius",
      author_email     = "gabriel.antonius@gmail.com",
     #url              = url,
     #license          = license,
     #platforms        = platforms,
     #keywords         = keywords,
     #install_requires = install_requires,
      packages         = find_packages(),
     #scripts          = my_scripts
      )


if __name__ == "__main__":
    from setuptools import setup
    setup(**setup_args)

