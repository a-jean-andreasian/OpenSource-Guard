# OpenSource Guard

---
## Table of content

- Introduction
  - [What problem does this tool solve?](#what-problem-does-this-tool-solve)
  - [What does this tool protect you from?](#what-does-this-tool-protect-you-from)
  - [Manifesto](#manifesto)
- In detail
  - [How it works?](#how-it-works)
  - [Usage notes](#usage-notes)
  - [The benefits of this tool](#the-benefits-of-this-tool)
    - [Little intro on used algorithms](#little-intro-on-these-algorithms)
- Usage
  - [Usage flow](#usage-flow)


---

## What problem does this tool solve?

- We are living times that anything public means it's not yours anymore.
- Anyone can grab your code, laugh at the licence, then reuse, repurpose, republish as their own, feed it to
  AI crawlers.
- Most “open-source protection” advice is utopian: blocklists, licenses, code etiquette.
- In reality, as in life the majority doesn't respect the rules but respect the gun.

TLDR: **This tool gives you hand-on protection for your open-source projects from code stealers.**

---

## What does this tool protect you from?

- AI crawlers.
- Those who will violate the license anyway.
- Individuals who modify the code and re-license it as their own.
- Other unwanted steals.

---

## Manifesto
1. No, _"not everything open-source is free to use. And if you think otherwise, then keep your code private."_
2. This is indeed the mentality of a typical scammer: unintelligent, selfish, greedy and ignorant. The one this tool opposes.

---

## How it works?

**The core idea** is in encoding the important and critical files of your open source code.

- E.g. abstraction layers, parts with heavy business logic, settings, file with constants, etc.

---

## Usage notes

- Use different keys in different parts of the program.
- Do not store the keys anywhere in the project, even encoded.
- Yes you can additionally obfuscate your code as well.
  - This actually depends on your preferences.

---

## The benefits of this tool

- It provides 2 in 1 choice. You can choose any of **AES-256 GCM** and **ChaCha20-Poly1305**.
- Moreover, it doesn't enforce you to encode all files with one algorithm.
- Moreover, you can rencode already encoded files with another algorithm, as many times as you want.

---

## Little intro on these algorithms

- **AES-256 GCM**: Industry standard, very secure, fast, and has built-in authentication (detects tampering). Perfect
  for encrypting source files.
- **ChaCha20-Poly1305**: Very fast, especially on mobile or low-power devices, and secure. A good alternative to AES if
  you want portability and performance.

---

## Usage flow

1. Encrypt the important files.
2. Save the keys somewhere handy, or directly save the keys to the deployment environment as variables (if available).
3. Upload the project to GitHub.


- Alternatively, you can have an automatic job to decrypt the project files (on startup).

---
