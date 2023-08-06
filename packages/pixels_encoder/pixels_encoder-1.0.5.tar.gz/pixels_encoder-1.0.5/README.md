# PIXELS ENCODER
Encode image pixels info into json file

# USAGE

To show help run ` pixels_encoder -h `.

To encode image info ` pixels_encoder -i /path/to/image.png -o /optional/path/to/output.json `.

To encode folder full of images ` pixels_encoder -f /path/to/folder/with/images -o /optional/path/to/output_folder `.

# BUILDING
To upload package to PyPI:
- put `.pypirc` file in your home folder with the following content:

```cfg
 [distutils]
 index-servers=pypi

 [pypi]
 repository=https://pypi.python.org/pypi
 username=your_username # 'wall-e' for AppCraft account
 password=your_password
```

- run `chmod 600 ~/.pypirc`
- upload the package to PyPI by running `python setup.py sdist upload -r pypi`

If you don't want to create `.pypirc` file, you can use [TWINE](https://pypi.python.org/pypi/twine).
