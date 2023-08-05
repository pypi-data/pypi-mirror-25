# SeppelSHARK Smother
### Description
SeppelSHARK Smother is a fork and massivly reduced version of [Smother](https://github.com/ChrisBeaumont/smother). After
the installation, it provides one plug-in for [nose](https://github.com/nose-devs/nose) and a second plugin for [py.test](https://github.com/pytest-dev/pytest). After you have called any
of these test programs with your tests, a .seppelsmother file is generated, which can then be used as input for the
TestCoverageLoader of the SeppelSHARK framework. This file includes coverage information based on each test method
that is executed.

### Build
From within the directory call
```bash
python setup.py install
```

### Test
From within the directory call
```bash
make test
```

### Use
You can just call your tests like always, but just including one/two more command line options.
- For nose call: 
```bash
nosetests --with-seppelsmother --seppelsmother-package=<root_of_project_to_track> <path_to_tests>
```

- For pytest call: 
```bash
py.test --seppelsmother=<root_of_project_to_track> <path_to_tests>
```