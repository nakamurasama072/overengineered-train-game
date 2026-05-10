# overengineered-train-game

Translations in other languages of this file can be viewed here:

[中文（简体）](./docs/README-zh_CN.md) | [中文（繁體）](./docs/README-zh_TW.md) | [日本語](./docs/README-ja_JP.md)

## A Cautionary Tale of Java-Style Python

This repository contains a Python implementation of the *Ticket to Ride* board game. However, it is **NOT** intended as a working, exemplary project. Instead, it serves as an **educational warning** against blindly transplanting Java design patterns into Python.

The code is extremely over‑engineered, hard to read, and stuffed with unnecessary abstractions. You will find command patterns for simple actions, strategy patterns for card effects that could be a one‑line conditional, factory patterns creating objects that could be written directly, and a deep inheritance hierarchy that makes following the data flow nearly impossible. What should have been a few hundred lines of clean Python code ended up as thousands of lines spread across dozens of files, all because every problem looked like a nail for the Java OOP hammer.

This project perfectly demonstrates how writing Python as if it were Java leads to bloated, unmaintainable academic garbage. It is a live museum of anti‑patterns.

## Who Wrote This Mess?

**I did NOT made this design of software architecture.**

The majority of this codebase was created by two of my teammates during a past assignment (or sprint). They are genuinely excellent Java developers — their OOP course in the University taught them object‑oriented programming very well. Too well, perhaps.

Unfortunately, they applied every single Java OOP habit directly to Python. Every action needed a class. Every variation needed an abstract interface. Every collection needed its own subclass. And they kept “adding improvements” — more patterns, more abstractions, more files — until the project became an unreadable Leviathan. **I watched in horror as a simple card game grew tentacles.**

## The Purpose of This Repository

This repository exists for one reason only: **to show you what NOT to do**.

- **DO NOT** write Python as if it is Java.

- **DO NOT** create a class for everything.

- **DO NOT** blindly apply design patterns without asking whether they are needed.

- **DO NOT** sacrifice readability for architectural purity.

If you are a student learning object‑oriented programming, this is the perfect example of how not to apply what you have learned. Study this code, learn to recognize the warning signs, and avoid making the same mistakes.

## Disclaimer

This repository has **no intention** of defaming, attacking, or insulting any individual, team, or educational institution. I mean no offense to anyone — least of all my two teammates, who are skilled developers working with the tools they were taught. The code is shared solely as a **negative** example for learning or researching purposes. All lessons here are lessons about code, not about people.

## Repository Policy

This repository exists **only for education and warning**. Therefore, **I will NOT accept any issues or pull requests regarding the code**. However, it is perfectly fine to use it for personal study or research.

Please, **DO NOT** try to “fix” it and bother me — that would completely miss the point. The code is broken by design to serve as a warning. If you want to see a correct implementation, please **look elsewhere** or **ask GenAI (ChatGPT, Claude, Gemini, Mistral AI, DeepSeek, GLM, MiniMax, etc.) for advice**. If you want to argue about design choices... then congratulations, you have already understood the lesson.

## Final Words

Look at the directory structure. Count the files. Ask yourself: does a *Ticket to Ride* clone really need an `actions` folder, an `effects` folder, a `comps` folder, a `deck` folder, a `utils` folder, and a `ui` folder with duplicated files? Does drawing a card really need a command class? Does a card effect really need a strategy pattern?

The answer, of course, is **NO**.

And that is exactly why this repository exists.

