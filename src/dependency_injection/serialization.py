import pickle

from typing import Dict, Type

from dependency_injection.registration import Registration


class RegistrationSerializer:
    @staticmethod
    def serialize(registrations) -> bytes:
        return pickle.dumps(registrations)

    @staticmethod
    def deserialize(serialized_state) -> Dict[Type, Registration]:
        return pickle.loads(serialized_state)
