# coding=utf8


from setuptools import setup

setup(name='qiniuFolderSync',
      version='0.0.1',
      description='Sync local folder to qiniu bucket',
      url='https://github.com/ipconfiger/qiniuFolderSync',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='MIT License',
      packages=['qiniuFolderSync'],
      install_requires=[
          'click',
          'result2',
      ],
      entry_points={
        'console_scripts': ['qnsync=qiniuFolderSync.main:main'],
      },
      zip_safe=False)
