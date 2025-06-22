.. note::

    This library is currently in the release candidate stage.
    The public API is considered stable and is undergoing final validation before the 1.0.0 release.

py-dependency-injection
=======================

A dependency injection library for Python — inspired by the built-in DI system in ASP.NET Core.

Overview
--------

`py-dependency-injection` provides a lightweight and extensible way to manage dependencies in Python applications. It promotes constructor injection, supports scoped lifetimes, and encourages clean architecture through explicit configuration and testable design.

This library is well-suited for both standalone use in Python applications and as a foundation for frameworks or tools that require structured dependency management.

Key Advantages
--------------

- **Familiar model** – Inspired by ASP.NET Core’s DI system
- **Scoped lifetimes** – Support for `singleton`, `scoped`, and `transient` registrations
- **Explicit injection** – Promotes clarity over magic
- **Test-friendly** – Designed for container isolation and overrides
- **Minimalistic** – Easy to use, extend, and integrate

You can find the source code for `py-dependency-injection` in our `GitHub repository <https://github.com/runemalm/py-dependency-injection>`_.

.. userguide-docs:
.. toctree::
  :maxdepth: 1
  :caption: User Guide

  userguide

.. examples-docs:
.. toctree::
  :maxdepth: 1
  :caption: Examples

  examples

.. releases-docs:
.. toctree::
  :maxdepth: 1
  :caption: Releases

  releases

You can find the source code for `py-dependency-injection` in our `GitHub repository <https://github.com/runemalm/py-dependency-injection>`_.
