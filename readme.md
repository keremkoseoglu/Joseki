# Joseki

Joseki is a simple code generator to help with class generation, based on design patterns. Basically; you select your
language & design pattern, change the JSON configuration and hit "Generate" to get the class source code.

## Adding a new class

* Add a new file to the package **language**
* Add a new language class derived from **abstract_language.AbstractLanguage**
* Implement support for desired patterns
* Modify **language/factory.py** to support the new language

## Adding a new pattern

* Implement the new pattern into **pattern/design_pattern.py**
* Edit the languages under **language** to add support for the new pattern

## Trivia

Joseki refers to a studied and standardized sequence of moves in game of Go in the opening phase of a game. Just like
design patterns in the opening phase of a project.