from setuptools import setup

with open('moxel_python_driver/VERSION', 'r') as f:
    version = f.read()
    version = version.replace('\n', '')

setup(name='moxel-python-driver',
      version=version,
      description='python driver for moxel models',
      # url='www.moxel.ai',
      author='moxel',
      author_email='support@moxel.ai',
      license='MIT',
      zip_safe=False,
      packages=['moxel_python_driver'],
      include_package_data=True,
      package_data={'moxel_python_driver': ['moxel_python_driver/VERSION'] },
      entry_points={
          "console_scripts": [
              "moxel-python-driver = moxel_python_driver.driver:main",
          ]
      }
)
