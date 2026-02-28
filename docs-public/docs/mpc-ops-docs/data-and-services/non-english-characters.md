# Representing Non-English Characters

Contributions with names that employ diacritic marks (accents, umlauts, etc.) are advised not to use special control codes (e.g., 8-bit ASCII) to represent these characters, as they frequently do not survive transmission via e-mail.

Use of the scheme below will ensure that any special characters required in your item/report will survive transmission via e-mail. The scheme is that used by the TeX typesetting system. The examples below can be extrapolated to other letters as necessary. Use of the curly brackets in some cases as indicated below is important.

## Character Representations

| Character | Description | ASCII Representation |
|-----------|-------------|---------------------|
| e with grave accent | Small e, grave accent | `` \`e `` |
| e with acute accent | Small e, acute accent | `\'e` |
| e with circumflex | Small e, circumflex accent | `\^e` |
| U with diaeresis | Capital U, diaeresis or umlaut | `\"U` |
| a with tilde | Small a, tilde | `\~a` |
| C with cedilla | Capital C, cedilla | `\c{C}` |
| r with hacek | Small r, hacek | `\v{r}` |
| AE ligature (capital) | Capital Norwegian diphthong | `{\AE}` |
| ae ligature (small) | Small Norwegian diphthong | `{\ae}` |
| O with stroke (capital) | Capital Norwegian O-slash | `{\O}` |
| o with stroke (small) | Small Norwegian O-slash | `{\o}` |
| A with ring (capital) | Capital Norwegian aa | `{\AA}` |
| a with ring (small) | Small Norwegian aa | `{\aa}` |
| L with stroke (capital) | Capital Polish L | `\L` |
| l with stroke (small) | Small Polish l | `\l` |
| Z with dot above (capital) | Capital Polish Z | `\.Z` |
| z with dot above (small) | Small Polish z | `\.z` |

!!! note
    When the accented character is *i*, the dot is usually replaced by the accent. The dotless i is represented using `{\i}`, so an i with an acute accent is written as `\'{\\i}`.

## Examples

| Word | ASCII Representation |
|------|---------------------|
| echelle | `\'echelle` |
| Angstrom | `{\AA}ngstr\"om` |
| Besancon | `Besan\c{c}on` |
| Pajdusakova | `Pajdu\v{s}\'akov\'a` |
