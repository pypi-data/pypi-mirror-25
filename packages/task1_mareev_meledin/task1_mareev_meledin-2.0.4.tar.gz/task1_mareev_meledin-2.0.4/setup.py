from setuptools import setup


# Функция для загрузки подробного описания проекта.
def readme():
    with open('README.rst') as f:
        return f.read()


      # Имя пакета.
setup(name='task1_mareev_meledin',
      # Версия.
      version='2.0.4',
      # Краткое описание пакета.
      description='Workshop 3 course. Autumn 17-18. Exercise 1.',
      # Авторы.
      author='Mareev Gleb and Meledin Stanislav',
      # Контактный email.
      author_email='wowmagic.gm@gmail.com',
      # Лицензия, под которой распространяется пакет.
      license='MIT',
      # packages=['task1_mareev_meledin'],
      # Зависимости от других пакетов.
      install_requires=[
          'numpy',
          'scipy'
      ],
      # Подробное описание проекта.
      long_description=readme(),
      # Добавление в пакет файлов с данными.
      include_package_data=True,
      # Ключевые слова, описывающие пакет.
      keywords='task1 mareev maledin cs msu',
      # Адрес пакета в интернете.
      url='https://github.com/GlebOlegovich/prac-2017-2018/tree/task1-mareev-meledin/submissions/task1/mareev-meledin/task1_mareev_meledin',
      # Категории пакета.
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
      ],
      packages=['task1_mareev_meledin'],
      # Установка пакета в качестве каталога, а не архива.
      zip_safe=False)
