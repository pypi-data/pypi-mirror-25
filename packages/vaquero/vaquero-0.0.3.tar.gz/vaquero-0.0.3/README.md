[![Build Status](https://travis-ci.org/jbn/vaquero.svg?branch=master)](https://travis-ci.org/jbn/vaquero)
[![Coverage Status](https://coveralls.io/repos/github/jbn/vaquero/badge.svg?branch=master)](https://coveralls.io/github/jbn/vaquero?branch=master)


# What is Vaquero?

<div align="center">
    <img src="logo.png" alt="Vaquero logo" />
    <!-- art by https://www.fiverr.com/calum_mcghee -->
</div>

## TL;DR

It's a library for iterative and interactive data wrangling at
laptop-scale. If you spend a lot of time in a
[Jupyter notebook](http://jupyter.org/), trying to clean dirty, raw
data, it's probably useful.

It would be nice if it were possible to write data cleaning code
correctly. But, the people who pay you to do data analysis don't do
data analysis and don't understand how dangerous dirty data are, so you
rarely get the luxury of feeling secure with what you extract. Vaquero
tries to find a balance between "business" demands and good hygiene.
Borrowing from Larry Wall, it tries "to make the easy things easy, and 
the hard things possible." In this context, "hard things" refers to
those wonderfully fun situations where, you write some code that you
know will break in the future but you have no time to fix it; then,
three months later, it breaks and you have no idea what your code does.

See also: [On Disappearing Code](https://medium.com/@generativist/on-disappearing-code-7fa2494203aa)

## An Example

It's easier to get a sense of "why" by looking at a notebook.

- [Notebook for the common usage pattern](https://github.com/jbn/vaquero/blob/master/demo/Module_Demo.ipynb)
- [Notebook for inline pipelines](https://github.com/jbn/vaquero/blob/master/demo/Inline_Demo.ipynb)

## Expecting Exceptions

Vaquero *expects* exceptions, making them pretty unexceptional. But,
Python's exception handling is cheap, so that's fine (i.e. EAFP -- 
Easier to ask for forgiveness than permission). Plus, with dirty
data, you know it will probably fail for some records. During
development, rather than halting each time, vaquero continues on its
merry way, up to some failure limit. For each failure, the library
logs the exception, including the name of the file *and* the arguments
which resulted in a failure.

After you have processed all the documents, you can then inspect the
errors. This helps you scan for error patterns, rather than programming
by the coincidence of the first error raised. Moreover, since you the
offending function and its arguments, it is easy to update the new
function, ensuring it passes with the prior bad example. Vaquero reloads
the pipeline for you. (Or, at least tries to, because reloading is
tricky.)

## Modules as Pipelines

> Namespaces are one honking great idea -- let's do more of those!

Programmers use namespaces everywhere to organize their code. Yet, when
writing data cleaning code, everything ends up in a big file with lots
of poorly-named functions. Think: `from hellishlib import *`. The
perfectionist in me says, "this is awful, and I should write it
properly, as a full library with lots of unit tests!" But, for
"perfectionists with deadlines," that's not possible.

Furthermore, the single-file-of-functions pattern emerges not only
because of time constraints; it's a reflection of the problem! ELT
code is **inherently** tightly-coupled. Code that extracts this variable
probably depends on that one which in turn also depends on some other
one. This leads to a tree of transformations, encapsulated by function
calls.

Recognizing this, `vaquero` doesn't try to move you away from
collecting all your ELT code in a single file. It's going to happen
anyway. Instead, it makes it safer with some conventions.

1. A module represents a single encapsulated pipeline. It should
process a well-defined document.
2. The function definition order is meaningful. Functions at the top
of the file execute before those above them. Again, it's a pipeline.
3. As per pythonic convention, functions prefixed with `_` are private.
Here, that means, the pipeline constructor ignores it when compiling
the pipeline. This gives you nice helper functions.
4. You're probably not going to use unit tests -- you don't have time.
But, since it's a module, pepper it with assertions. And, using
the `_`-prefix, you can actually write namespaced tests
(e.g. `_my_test()`), and immediately call them in the module.
(I actually write a lot of my code with `unittest` in the pipeline
module and it gets called right before the module fully imports.)
Then, when you break something, you can't even start pipeline
processing. It fails fast. (You can deviate from this pattern -- but,
in general, don't.)

## Installation

```sh
pip install vaquero
```

## Tips

### The `f(src, dst)` Pattern

For most of my pipelines, I tend to write functions that look like,

```python
def f(src_d, dst_d):
    dst_d['age'] = int(src_d['AGE1'])
```

Coming from functional languages, I'd prefer immutable objects. But,
in Python, that tends to be painfully slow. This pattern represents a
compromise that usually works well. On the one side (`dst_d`) you have
already processed elements; on the other, the raw data.  


### Hidden field pattern

- Assume you are processing a pipeline with a dict destination document.
  Use '_key_name' fields for intermediary results in a document. You can
  delete them at the end of the pipeline (easily, via
  `vaquero.transformations.remove_private_keys`), but in the interim,
  you'll see these fields on failure.

## Disclaimer

I have this big monstrous library called vaquero on my computer. It's a
collection of lots of functions I've written over (entirely too) many
data munging projects. I use it often, and keep telling myself "once I
find the time, I'll release it!" And, that never happens. It's too big
to clean up in a way that makes me comfortable. Instead, I'll be
releasing little bits of code in a ad-hoc, just-in-time fashion. When
I absolutely need some feature of the big library going forward, I'll
extract it and put it here.

That makes me wildly uncomfortable, but...I'm starving for time.

In any case, library-user beware. Things will break.
