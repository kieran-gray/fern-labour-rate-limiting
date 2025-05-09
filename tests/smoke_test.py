from fern_labour_package_template.example import DomainEvent


def can_instantiate_classes() -> None:
    DomainEvent.create(data={"test": "test"})
    print("Can instantiate all classes")


if __name__ == "__main__":
    can_instantiate_classes()
