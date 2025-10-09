Entities:

- `OpenSourceGuard`
- `CipherExecutorExtended`
- `Metadata`
  - `MetadataLoader`
  - `MetadataDumper`
- `FileRecord`
- `KeyRecord`
- `CryptoGraphicTransactionResult`
- `Finalizers`
  - `PostEncryptionJobManager`
  - `PostDecryptionJobManager` 

---
1. Scenario 1. Encrypt

User :`list[Path]` → `OpenSourceGuard.encrypt`: `list[Path]` →  `CipherExecutorExtended.encrypt_files` : `FileRecord` →  `CipherExecutorExtended.encrypt_file`→  `PostEncryptionJobManager` : `FileRecord` → `MetadataDumper`: `CryptoGraphicTransactionResult`  → `OpenSourceGuard`
