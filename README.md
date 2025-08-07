[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: David Runemalm](https://img.shields.io/badge/Author-David%20Runemalm-blue)](https://www.davidrunemalm.com)
[![Python Versions](https://img.shields.io/pypi/pyversions/py-dependency-injection)](https://pypi.org/project/py-dependency-injection/)
[![Master workflow](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)
[![PyPI version](https://badge.fury.io/py/py-dependency-injection.svg)](https://pypi.org/project/py-dependency-injection/)
![Downloads](https://pepy.tech/badge/py-dependency-injection)
![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

# py-dependency-injection

A dependency injection library for Python.

## Why py-dependency-injection?

`py-dependency-injection` is inspired by the built-in dependency injection system in **ASP.NET Core**. It provides a lightweight and extensible way to manage dependencies in Python applications. By promoting constructor injection and supporting scoped lifetimes, it encourages clean architecture and makes testable, maintainable code the default.

This library is implemented in **pure Python** and has **no runtime dependencies**.

## Features

- **Scoped Registrations:** Define the lifetime of your dependencies as transient, scoped, or singleton.
- **Constructor Injection:** Automatically resolve and inject dependencies when creating instances.
- **Method Injection:** Inject dependencies into methods using a simple decorator.
- **Factory Functions:** Register factory functions, classes, or lambdas to create dependencies.
- **Instance Registration:** Register existing instances as dependencies.
- **Tag-Based Registration and Resolution:** Organize and resolve dependencies based on tags.
- **Multiple Containers:** Support for using multiple dependency containers.

## Compatibility

This library requires **Python 3.9 or later**.

It is tested and compatible with:

- Python 3.9, 3.10, 3.11, 3.12, 3.13

## Installation

```bash
$ pip install py-dependency-injection
```

## Quick Start

Here's a quick example to get you started:

```python
from dependency_injection.container import DependencyContainer

# Define an abstract payment gateway interface
class PaymentGateway:
    def charge(self, amount: int, currency: str):
        raise NotImplementedError()

# A concrete implementation using Stripe
class StripeGateway(PaymentGateway):
    def charge(self, amount: int, currency: str):
        print(f"Charging {amount} {currency} using Stripe...")

# A service that depends on the payment gateway
class CheckoutService:
    def __init__(self, gateway: PaymentGateway):
        self._gateway = gateway

    def checkout(self):
        self._gateway.charge(2000, "USD")  # e.g. $20.00

# Get the default dependency container
container = DependencyContainer.get_instance()

# Register StripeGateway as a singleton (shared for the app's lifetime)
container.register_singleton(PaymentGateway, StripeGateway)

# Register CheckoutService as transient (new instance per resolve)
container.register_transient(CheckoutService)

# Resolve and use the service
checkout = container.resolve(CheckoutService)
checkout.checkout()
```

## Documentation

For more advanced usage and examples, please visit our [readthedocs](https://py-dependency-injection.readthedocs.io/en/latest/) page.

## License

`py-dependency-injection` is released under the MIT license — a permissive license that allows commercial use, modification, distribution, and private use.
See [LICENSE](LICENSE) for full details.

## Source Code

You can find the source code for `py-dependency-injection` on [GitHub](https://github.com/runemalm/py-dependency-injection).

## Release Notes

### Latest: [1.0.0-rc.2](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-rc.2) (2025-08-07)

- **License Change**: Switched from GPL-3.0 to MIT to support broader adoption and commercial use.
- **Toolchange**: Migrated from `pipenv` to `Poetry`.
- **Dropped Python 3.7 & 3.8 support** – Both versions are EOL and increasingly unsupported by modern tooling.

➡️ Full changelog: [GitHub Releases](https://github.com/runemalm/py-dependency-injection/releases)
