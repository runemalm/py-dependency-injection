import pickle

from unit_test.unit_test_case import UnitTestCase

from dependency_injection.serialization import RegistrationSerializer
from dependency_injection.registration import Registration
from dependency_injection.scope import Scope


class Vehicle:
    pass


class Car:
    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle


class TestRegistrationSerializer(UnitTestCase):
    def test_serialize_and_deserialize(self):
        # arrange
        registrations = {
            Vehicle: Registration(
                dependency=Vehicle,
                implementation=Car,
                scope=Scope.TRANSIENT,
                tags={"example_tag"},
                constructor_args={"vehicle": Vehicle()},
                factory=None,
                factory_args={},
            )
        }

        # act
        serialized = RegistrationSerializer.serialize(registrations)
        deserialized = RegistrationSerializer.deserialize(serialized)

        # assert
        self.assertEqual(deserialized.keys(), registrations.keys())
        self.assertEqual(
            deserialized[Vehicle].dependency, registrations[Vehicle].dependency
        )
        self.assertEqual(
            deserialized[Vehicle].implementation, registrations[Vehicle].implementation
        )
        self.assertEqual(deserialized[Vehicle].scope, registrations[Vehicle].scope)
        self.assertEqual(deserialized[Vehicle].tags, registrations[Vehicle].tags)
        self.assertEqual(
            deserialized[Vehicle].constructor_args.keys(),
            registrations[Vehicle].constructor_args.keys(),
        )
        self.assertEqual(deserialized[Vehicle].factory, registrations[Vehicle].factory)
        self.assertEqual(
            deserialized[Vehicle].factory_args, registrations[Vehicle].factory_args
        )

    def test_deserialize_invalid_data(self):
        # arrange
        invalid_data = b"not a valid pickle"

        # act & assert
        with self.assertRaises(pickle.UnpicklingError):
            RegistrationSerializer.deserialize(invalid_data)
