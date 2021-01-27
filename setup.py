from setuptools import setup

setup(
name = 'WateringApp',
package = ['WateringApp'],
include_package_data = True,
install_requieres=[
'flask',
'flask_alchemy',
'flask_user',
''
],
)
