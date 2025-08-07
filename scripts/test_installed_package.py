from dependency_injection.container import DependencyContainer


class Foo:
    pass


def main():
    container = DependencyContainer.get_instance()
    container.register_singleton(Foo)
    resolved = container.resolve(Foo)

    if not isinstance(resolved, Foo):
        raise Exception("❌ Resolution failed")

    print("✅ py-dependency-injection works!")


if __name__ == "__main__":
    main()
