UBelt is a "utility belt" of commonly needed utility and helper functions. It is a migration of the most useful parts of `utool`   (https://github.com/Erotemic/utool) into a minimal and standalone module.

The `utool` library contains a number of useful utility functions, however a number of these are too specific or not well documented. The goal of this migration is to slowly port over the most re-usable parts of `utool` into a stable package.

In addition to utility functions `utool` also contains a custom doctest   harness and code introspection and auto-generation features. This port will contain a rewrite of the doctest harness. Some of the code introspection features will be ported, but most   auto-generation abilities will be ported into a new module that depends on   `ubelt`.

