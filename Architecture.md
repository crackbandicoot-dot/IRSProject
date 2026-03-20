# Architecture

## Style: Modular Monolith, Unix Philosophy

Each module does **one thing**. Modules know nothing about each other — they only know the data shapes they receive and return. The pipeline in `main.py` is the only place that composes them.

This mirrors the Unix philosophy: small, focused tools chained together. Swapping or replacing one stage does not touch any other.

## The Pipeline Contract

```
raw string  →  [UI]  →  [QueryParser]  →  [IndexHandler]  →  [SearchEngine]  →  [ResultsEnricher]  →  [UI]
```

Each arrow is a plain Python value. No shared state, no direct imports between modules.

## Module Structure Convention

Every module follows the same two-file pattern:

```
ModuleName/
├── module_name.py     ← public interface (module-level functions)
└── ModuleName.py      ← implementation class
```

- **`module_name.py`** is the only file the rest of the system imports. It instantiates whatever it needs at module level and exposes one or a few plain functions.
- **`ModuleName.py`** contains the class with the full implementation. It is an internal detail of the module.

This mirrors how Unix tools expose a single command, not their internals.

## Adding a New Module

1. Create the directory and the two files:
   ```
   NewModule/
   ├── new_module.py
   └── NewModule.py
   ```

2. `NewModule.py` — implement the class:
   ```python
   class NewModule:
       def __init__(self): ...
       def process(self, input): ...
   ```

3. `new_module.py` — expose a clean function:
   ```python
   from .NewModule import NewModule
   _instance = NewModule()
   def process(input):
       return _instance.process(input)
   ```

4. Wire it into `main.py`:
   ```python
   from NewModule import new_module
   result = new_module.process(previous_result)
   ```

That is the entire extension point. Nothing else changes.

## Adding a New Data Contract

Contracts live in `Contracts/` and are shared data shapes (dataclasses, ABCs). A module may define its own output contract there if another module needs to consume it.

```
Contracts/
└── NewOutput/
    ├── __init__.py       ← re-exports the class
    └── NewOutput.py      ← dataclass or ABC
```

Contracts have no logic. They are pure structure.

## Rules

- A module must not import from another module. Only `main.py` composes modules.
- A module's class file is private. Only the module's `module_name.py` is public.
- Communication between stages happens through values, not shared state.
- New behavior means a new module or a new class inside an existing module — not changes spread across multiple modules.
