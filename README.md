[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Master workflow](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-dependency-injection/actions/workflows/master.yml)

# py-dependency-injection

A dependency injection library for Python.

## Features

- Dependency Container
- Dependency Scopes
- Constructor Injection
- Method Injection
- Tags
- Factory registration
- Instance registration

## Python Compatibility

This library is compatible with the following Python versions:

- 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

## Installation

```bash
$ pip install py-dependency-injection
```

## Usage

The following examples demonstrates how to use the library.

### Getting default container

```python
dependency_container = DependencyContainer.get_instance()
```

### Getting more containers

```python
another_container = DependencyContainer.get_instance(name="another_container")
third_container = DependencyContainer.get_instance(name="third_container")
```

### Register with one of three available scopes

```python
dependency_container.register_transient(Fruit, Apple)
dependency_container.register_scoped(Beverage, Cream)
dependency_container.register_singleton(Vehicle, Car)
```

### Register with constructor arguments

```python
dependency_container.register_transient(
    Fruit,
    Apple,
    constructor_args={"brand": "Gala", "price": 5.00}
)
```

### Register with factory

```python
class CarFactory:
    @classmethod
    def create(cls, color: str, mileage: int) -> Car:
        return Car(color=color, mileage=mileage)

def create_car(color: str, mileage: int) -> Car:
    return Car(color=color, mileage=mileage)

dependency_container.register_factory(Vehicle, CarFactory.create, factory_args={"color": "red", "mileage": 3800})
dependency_container.register_factory(Vehicle, create_car, factory_args={"color": "red", "mileage": 3800})
dependency_container.register_factory(Vehicle, lambda: Car(color="red", mileage=3800))
```

### Register instance

```python
instance = Car(color="red", mileage=3800)
dependency_container.register_instance(Vehicle, instance)
```

### Register with tags

```python
dependency_container.register_transient(Fruit, Apple, tags={Eatable, Delicious})
dependency_container.register_scoped(Beverage, Cream, tags={Eatable})
dependency_container.register_singleton(Vehicle, Car, tags={Driveable, Comfortable})
```

### Resolve dependencies

```python
transient_dependency = dependency_container.resolve(Fruit)
scoped_dependency = dependency_container.resolve(Beverage, scope_name="dinner")
singleton_dependency = dependency_container.resolve(Vehicle)
```

### Resolve dependencies with tags

```python
tagged_dependencies = dependency_container.resolve_all(tags={Eatable, Delicious})
```

### Constructor injection

```python
class Place:
    def __init__(
        self,
        fruit: Fruit,
        beverage: Beverage,
        vehicle: Vehicle
    ):
        self.fruit = fruit
        self.beverage = beverage
        self.vehicle = vehicle

dependency_container = DependencyContainer.get_instance()

dependency_container.register_transient(Place)
dependency_container.register_transient(Fruit, Apple)
dependency_container.register_scoped(Beverage, Cream)
dependency_container.register_singleton(Vehicle, Car)

place = dependency_container.resolve(Place)

place.fruit.eat()
place.beverage.drink()
place.vehicle.drive()
```

### Method injection

```python
class Place:

    @classmethod
    @inject()
    def do_it(cls, fruit: Fruit, beverage: Beverage, vehicle: Vehicle):
        fruit.eat()
        beverage.drink()
        vehicle.drive()

    @staticmethod
    @inject()
    def do_it_again(fruit: Fruit, beverage: Beverage, vehicle: Vehicle):
        fruit.eat()
        beverage.drink()
        vehicle.drive()

    @staticmethod
    @inject(container_name="another_container", scope_name="another_scope")
    def do_it_with_another_container_and_scope(fruit: Fruit, beverage: Beverage, vehicle: Vehicle):
        fruit.eat()
        beverage.drink()
        vehicle.drive()
```

## Documentation

For the latest documentation, visit [readthedocs](https://py-dependency-injection.readthedocs.io/en/latest/).

## Contribution

To contribute, create a pull request on the develop branch following the [git flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.

## Release Notes

### [1.0.0-alpha.6](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.6) (2024-03-23)

- Factory Registration: Added support for registering dependencies using factory functions for dynamic instantiation.
- Instance Registration: Enabled registering existing instances as dependencies.
- Tag-based Registration and Resolution: Introduced the ability to register and resolve dependencies using tags for flexible dependency management.

### [1.0.0-alpha.5](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.5) (2024-03-03)

- **Critical Package Integrity Fix**: This release addresses a critical issue that affected the packaging of the Python library in all previous alpha releases (1.0.0-alpha.1 to 1.0.0-alpha.4). The problem involved missing source files in the distribution, rendering the library incomplete and non-functional. Users are strongly advised to upgrade to version 1.0.0-alpha.5 to ensure the correct functioning of the library. All previous alpha releases are affected by this issue.

### [1.0.0-alpha.4](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.4) (2024-03-02)

- Constructor Arguments: Support for constructor arguments added to dependency registration.

### [1.0.0-alpha.3](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.3) (2024-03-02)

- **Breaking Change**: Starting from this version, the `@inject` decorator can only be used on static class methods and class methods. It can't be used on instance methods anymore.
- Documentation Update: The documentation has been updated to reflect the new restriction on the usage of the decorator.

### [1.0.0-alpha.2](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.2) (2024-02-27)

- Python Version Support: Added support for Python versions 3.7, 3.9, 3.10, 3.11, and 3.12.
- New Feature: Method Injection with Decorator: Introduced a new feature allowing method injection using the @inject decorator. Dependencies can now be injected into an instance method, providing more flexibility in managing dependencies within class instance methods.
- New Feature: Multiple Containers: Enhanced the library to support multiple containers. Users can now create and manage multiple dependency containers, enabling better organization and separation of dependencies for different components or modules.
- Documentation Update: Expanded and improved the documentation to include details about the newly added method injection feature and additional usage examples. Users can refer to the latest documentation at readthedocs for comprehensive guidance.

### [1.0.0-alpha.1](https://github.com/runemalm/py-dependency-injection/releases/tag/v1.0.0-alpha.1) (2024-02-25)

- Initial alpha release.
- Added Dependency Container: The library includes a dependency container for managing object dependencies.
- Added Constructor Injection: Users can leverage constructor injection for cleaner and more modular code.
- Added Dependency Scopes: Define and manage the lifecycle of dependencies with support for different scopes.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.
