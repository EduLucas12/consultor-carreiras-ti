"""Compatibilidade do Experta com Python >= 3.10.

O Experta (última versão publicada) ainda faz ``collections.Mapping``,
``collections.Callable`` etc. Esses nomes foram REMOVIDOS do módulo
``collections`` no Python 3.10 (ficaram só em ``collections.abc``).

Sem este "remendo" (shim), ``import experta`` quebra com:

    AttributeError: module 'collections' has no attribute 'Mapping'

IMPORTANTE: este módulo precisa ser importado ANTES de ``import experta``.
"""

import collections
import collections.abc

for _nome in (
    "Mapping",
    "MutableMapping",
    "Sequence",
    "Iterable",
    "Callable",
    "Hashable",
    "Set",
    "MutableSet",
):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))
