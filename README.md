# python-class-attribute-lookup
Why your choice of variable names can slow down your program - a deep dive into Python

This is the repository for my blog post [Why your choice of variable names can slow down your program - a deep dive into Python](https://styfenschaer.github.io/Why-your-choice-of-variable-names-can-slow-down-your-program-a-deep-dive-into-Python/).
Everything needed to reproduce the results in the article is included in this repository.
The only dependencies are numpy and matplotlib. 
You will have to build the C extension module yourself (make sure you have a C compiler installed). You can type the following command in the path of this directory. 

```bash
python setup.py build_ext --inplace
```

After the build process is complete, you can use the module as you would any other Python module. The module named `hashmod` is used in the file `hash_collison.py`.