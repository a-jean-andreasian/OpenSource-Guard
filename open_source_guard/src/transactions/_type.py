from typing import Union, Type

EncryptionTransaction = object()
DecryptionTransaction = object()

TransactionType = Type[Union[EncryptionTransaction, DecryptionTransaction]]
