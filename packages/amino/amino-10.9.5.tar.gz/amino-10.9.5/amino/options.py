import os

import amino


class EnvOption:

    def __init__(self, name: str) -> None:
        self.name = name

    def __bool__(self) -> bool:
        return self.name in os.environ

    @property
    def value(self) -> 'amino.Maybe[str]':
        return amino.env[self.name]

    def __str__(self) -> str:
        value = self.value.map(lambda a: f'={a}') | ' is unset'
        return f'{self.name}{value}'

development = EnvOption('AMINO_DEVELOPMENT')
integration_test = EnvOption('AMINO_INTEGRATION')
anon_debug = EnvOption('AMINO_ANON_DEBUG')

__all__ = ('development', 'integration_test', 'anon_debug')
