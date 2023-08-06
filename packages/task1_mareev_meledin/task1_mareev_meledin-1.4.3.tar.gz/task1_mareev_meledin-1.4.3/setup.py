from setuptools import setup


# Функция для загрузки подробного описания проекта.
def readme():
    with open('README.md') as f:
        return f.read()


      # Имя пакета.
setup(name='task1_mareev_meledin',
      # Версия.
      version='1.4.3',
      # Краткое описание пакета.
      description='Workshop 3 course. Autumn 17-18. Exercise 1.',
      # Авторы.
      author='Mareev Gleb and Meledin Stanislav',
      # Контактный email.
      author_email='wowmagic.gm@gmail.com',
      # Лицензия, под которой распространяется пакет.
      license='MIT',
      packages=['task1_mareev_meledin'],
      # Зависимости от других пакетов.
      install_requires=[
          'numpy',
          'scipy'
      ],
      # Подробное описание проекта.
      long_description=readme(),
      include_package_data=True,
      zip_safe=False)
