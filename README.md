# programmingLanguages
Repo for the programming languages class winter 2020  
Members : 
  - gavendanoc
  - DIEG055
  - saduquebe

### Test

This guide follows the recommended project structure for testing given [here](https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure) 

#### How to use ?
This repo uses a python library called `unittest`, which allows testing as a command line tool. This [site](https://realpython.com/python-testing/) offers an introduction, but you can always check the [docs](https://docs.python.org/3/library/unittest.html).  

Running lexical analyzer 
```shell
$ cd src
$ python3 lexical.py
```

Running syntactic analyzer 
```shell
$ cd src
$ python3 main.py
```

##### Examples

For checking all test:
```shell
$ cd code
$ python3 -m unittest
```

For checking a single set of tests, in this case characters:
```shell
$ cd code
$ python3 -m unittest tests.testlexical.testCharacters
```

Another example,  running test over a single test set
```shell
$ cd code
$ python3 -m unittest tests.testsyntax.testExamples
```

You can also check a whole section, for running all the syntax tests do : 
```shell
$ cd code
$ python3 -m unittest discover tests.testsyntax
```
