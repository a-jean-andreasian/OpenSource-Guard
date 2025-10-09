from typing import Type, Union

EncryptionTransaction = object()
DecryptionTransaction = object()

TransactionType = Type[Union[EncryptionTransaction, DecryptionTransaction]]
