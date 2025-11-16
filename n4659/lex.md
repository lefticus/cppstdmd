# Lexical conventions <a id="lex">[[lex]]</a>

## Separate translation <a id="lex.separate">[[lex.separate]]</a>

The text of the program is kept in units called *source files* in this
International Standard. A source file together with all the headers (
[[headers]]) and source files included ([[cpp.include]]) via the
preprocessing directive `#include`, less any source lines skipped by any
of the conditional inclusion ([[cpp.cond]]) preprocessing directives,
is called a *translation unit*.

[*Note 1*: A C++program need not all be translated at the same
time. — *end note*]

[*Note 2*: Previously translated translation units and instantiation
units can be preserved individually or in libraries. The separate
translation units of a program communicate ([[basic.link]]) by (for
example) calls to functions whose identifiers have external linkage,
manipulation of objects whose identifiers have external linkage, or
manipulation of data files. Translation units can be separately
translated and then later linked to produce an executable program (
[[basic.link]]). — *end note*]

## Phases of translation <a id="lex.phases">[[lex.phases]]</a>

The precedence among the syntax rules of translation is specified by the
following phases.[^1]

1.  Physical source file characters are mapped, in an
    *implementation-defined* manner, to the basic source character set
    (introducing new-line characters for end-of-line indicators) if
    necessary. The set of physical source file characters accepted is
    *implementation-defined*. Any source file character not in the basic
    source character set ([[lex.charset]]) is replaced by the
    *universal-character-name* that designates that character. An
    implementation may use any internal encoding, so long as an actual
    extended character encountered in the source file, and the same
    extended character expressed in the source file as a
    *universal-character-name* (e.g., using the `\uXXXX` notation), are
    handled equivalently except where this replacement is reverted (
    [[lex.pptoken]]) in a raw string literal.
2.  Each instance of a backslash character (\\ immediately followed by a
    new-line character is deleted, splicing physical source lines to
    form logical source lines. Only the last backslash on any physical
    source line shall be eligible for being part of such a splice.
    Except for splices reverted in a raw string literal, if a splice
    results in a character sequence that matches the syntax of a
    *universal-character-name*, the behavior is undefined. A source file
    that is not empty and that does not end in a new-line character, or
    that ends in a new-line character immediately preceded by a
    backslash character before any such splicing takes place, shall be
    processed as if an additional new-line character were appended to
    the file.
3.  The source file is decomposed into preprocessing tokens (
    [[lex.pptoken]]) and sequences of white-space characters (including
    comments). A source file shall not end in a partial preprocessing
    token or in a partial comment.[^2] Each comment is replaced by one
    space character. New-line characters are retained. Whether each
    nonempty sequence of white-space characters other than new-line is
    retained or replaced by one space character is unspecified. The
    process of dividing a source file’s characters into preprocessing
    tokens is context-dependent. \[*Example 1*: see the handling of `<`
    within a `#include` preprocessing directive. — *end example*]
4.  Preprocessing directives are executed, macro invocations are
    expanded, and `_Pragma` unary operator expressions are executed. If
    a character sequence that matches the syntax of a
    *universal-character-name* is produced by token concatenation (
    [[cpp.concat]]), the behavior is undefined. A `#include`
    preprocessing directive causes the named header or source file to be
    processed from phase 1 through phase 4, recursively. All
    preprocessing directives are then deleted.
5.  Each source character set member in a character literal or a string
    literal, as well as each escape sequence and
    *universal-character-name* in a character literal or a non-raw
    string literal, is converted to the corresponding member of the
    execution character set ([[lex.ccon]], [[lex.string]]); if there is
    no corresponding member, it is converted to an
    *implementation-defined* member other than the null (wide)
    character.[^3]
6.  Adjacent string literal tokens are concatenated.
7.  White-space characters separating tokens are no longer significant.
    Each preprocessing token is converted into a token ([[lex.token]]).
    The resulting tokens are syntactically and semantically analyzed and
    translated as a translation unit. \[*Note 1*: The process of
    analyzing and translating the tokens may occasionally result in one
    token being replaced by a sequence of other tokens (
    [[temp.names]]). — *end note*] \[*Note 2*: Source files,
    translation units and translated translation units need not
    necessarily be stored as files, nor need there be any one-to-one
    correspondence between these entities and any external
    representation. The description is conceptual only, and does not
    specify any particular implementation. — *end note*]
8.  Translated translation units and instantiation units are combined as
    follows: \[*Note 3*: Some or all of these may be supplied from a
    library. — *end note*] Each translated translation unit is examined
    to produce a list of required instantiations. \[*Note 4*: This may
    include instantiations which have been explicitly requested (
    [[temp.explicit]]). — *end note*] The definitions of the required
    templates are located. It is *implementation-defined* whether the
    source of the translation units containing these definitions is
    required to be available. \[*Note 5*: An implementation could encode
    sufficient information into the translated translation unit so as to
    ensure the source is not required here. — *end note*] All the
    required instantiations are performed to produce *instantiation
    units*. \[*Note 6*: These are similar to translated translation
    units, but contain no references to uninstantiated templates and no
    template definitions. — *end note*] The program is ill-formed if
    any instantiation fails.
9.  All external entity references are resolved. Library components are
    linked to satisfy external references to entities not defined in the
    current translation. All such translator output is collected into a
    program image which contains information needed for execution in its
    execution environment.

## Character sets <a id="lex.charset">[[lex.charset]]</a>

The *basic source character set* consists of 96 characters: the space
character, the control characters representing horizontal tab, vertical
tab, form feed, and new-line, plus the following 91 graphical
characters:[^4]

``` cpp
a b c d e f g h i j k l m n o p q r s t u v w x y z
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
0 1 2 3 4 5 6 7 8 9
_ { } [ ] # ( ) < > % : ; . ? * + - / ^ & | ~ ! = , \" '
```

The *universal-character-name* construct provides a way to name other
characters.

``` bnf
hex-quad:
    hexadecimal-digit hexadecimal-digit hexadecimal-digit hexadecimal-digit
```

``` bnf
universal-character-name:
    '\u' hex-quad
    '\U' hex-quad hex-quad
```

The character designated by the *universal-character-name* `\UNNNNNNNN`
is that character whose character short name in ISO/IEC 10646 is
`NNNNNNNN`; the character designated by the *universal-character-name*
`\uNNNN` is that character whose character short name in ISO/IEC 10646
is `0000NNNN`. If the hexadecimal value for a *universal-character-name*
corresponds to a surrogate code point (in the range 0xD800–0xDFFF,
inclusive), the program is ill-formed. Additionally, if the hexadecimal
value for a *universal-character-name* outside the *c-char-sequence*,
*s-char-sequence*, or *r-char-sequence* of a character or string literal
corresponds to a control character (in either of the ranges 0x00–0x1F or
0x7F–0x9F, both inclusive) or to a character in the basic source
character set, the program is ill-formed.[^5]

The *basic execution character set* and the
*basic execution wide-character set* shall each contain all the members
of the basic source character set, plus control characters representing
alert, backspace, and carriage return, plus a *null character*
(respectively, *null wide character*), whose value is 0. For each basic
execution character set, the values of the members shall be non-negative
and distinct from one another. In both the source and execution basic
character sets, the value of each character after `0` in the above list
of decimal digits shall be one greater than the value of the previous.
The *execution character set* and the *execution wide-character set* are
*implementation-defined* supersets of the basic execution character set
and the basic execution wide-character set, respectively. The values of
the members of the execution character sets and the sets of additional
members are locale-specific.

## Preprocessing tokens <a id="lex.pptoken">[[lex.pptoken]]</a>

``` bnf
preprocessing-token:
    header-name
    identifier
    pp-number
    character-literal
    user-defined-character-literal
    string-literal
    user-defined-string-literal
    preprocessing-op-or-punc
    each non-white-space character that cannot be one of the above
```

Each preprocessing token that is converted to a token ([[lex.token]])
shall have the lexical form of a keyword, an identifier, a literal, an
operator, or a punctuator.

A preprocessing token is the minimal lexical element of the language in
translation phases 3 through 6. The categories of preprocessing token
are: header names, identifiers, preprocessing numbers, character
literals (including user-defined character literals), string literals
(including user-defined string literals), preprocessing operators and
punctuators, and single non-white-space characters that do not lexically
match the other preprocessing token categories. If a `'` or a `"`
character matches the last category, the behavior is undefined.
Preprocessing tokens can be separated by white space; this consists of
comments ([[lex.comment]]), or white-space characters (space,
horizontal tab, new-line, vertical tab, and form-feed), or both. As
described in Clause  [[cpp]], in certain circumstances during
translation phase 4, white space (or the absence thereof) serves as more
than preprocessing token separation. White space can appear within a
preprocessing token only as part of a header name or between the
quotation characters in a character literal or string literal.

If the input stream has been parsed into preprocessing tokens up to a
given character:

- If the next character begins a sequence of characters that could be
  the prefix and initial double quote of a raw string literal, such as
  `R"`, the next preprocessing token shall be a raw string literal.
  Between the initial and final double quote characters of the raw
  string, any transformations performed in phases 1 and 2
  (*universal-character-name*s and line splicing) are reverted; this
  reversion shall apply before any *d-char*, *r-char*, or delimiting
  parenthesis is identified. The raw string literal is defined as the
  shortest sequence of characters that matches the raw-string pattern
- Otherwise, if the next three characters are `<::` and the subsequent
  character is neither `:` nor `>`, the `<` is treated as a
  preprocessing token by itself and not as the first character of the
  alternative token `<:`.
- Otherwise, the next preprocessing token is the longest sequence of
  characters that could constitute a preprocessing token, even if that
  would cause further lexical analysis to fail, except that a
  *header-name* ([[lex.header]]) is only formed within a `#include`
  directive ([[cpp.include]]).

[*Example 1*:

``` cpp
#define R "x"
const char* s = R"y";           // ill-formed raw string, not "x" "y"
```

— *end example*]

[*Example 2*: The program fragment `0xe+foo` is parsed as a
preprocessing number token (one that is not a valid floating or integer
literal token), even though a parse as three preprocessing tokens `0xe`,
`+`, and `foo` might produce a valid expression (for example, if `foo`
were a macro defined as `1`). Similarly, the program fragment `1E1` is
parsed as a preprocessing number (one that is a valid floating literal
token), whether or not `E` is a macro name. — *end example*]

[*Example 3*: The program fragment `x+++++y` is parsed as `x
++ ++ + y`, which, if `x` and `y` have integral types, violates a
constraint on increment operators, even though the parse `x ++ + ++ y`
might yield a correct expression. — *end example*]

## Alternative tokens <a id="lex.digraph">[[lex.digraph]]</a>

Alternative token representations are provided for some operators and
punctuators.[^6]

In all respects of the language, each alternative token behaves the
same, respectively, as its primary token, except for its spelling.[^7]
The set of alternative tokens is defined in Table 
[[tab:alternative.tokens]].

## Tokens <a id="lex.token">[[lex.token]]</a>

``` bnf
token:
    identifier
    keyword
    literal
    operator
    punctuator
```

There are five kinds of tokens: identifiers, keywords, literals,[^8]
operators, and other separators. Blanks, horizontal and vertical tabs,
newlines, formfeeds, and comments (collectively, “white space”), as
described below, are ignored except as they serve to separate tokens.

[*Note 1*: Some white space is required to separate otherwise adjacent
identifiers, keywords, numeric literals, and alternative tokens
containing alphabetic characters. — *end note*]

## Comments <a id="lex.comment">[[lex.comment]]</a>

The characters `/*` start a comment, which terminates with the
characters `*/`. These comments do not nest. The characters `//` start a
comment, which terminates immediately before the next new-line
character. If there is a form-feed or a vertical-tab character in such a
comment, only white-space characters shall appear between it and the
new-line that terminates the comment; no diagnostic is required.

[*Note 1*: The comment characters `//`, `/*`, and `*/` have no special
meaning within a `//` comment and are treated just like other
characters. Similarly, the comment characters `//` and `/*` have no
special meaning within a `/*` comment. — *end note*]

## Header names <a id="lex.header">[[lex.header]]</a>

``` bnf
header-name:
    '<' h-char-sequence '>'
    '"' q-char-sequence '"'
```

``` bnf
h-char-sequence:
    h-char
    h-char-sequence h-char
```

``` bnf
h-char:
    any member of the source character set except new-line and '>'
```

``` bnf
q-char-sequence:
    q-char
    q-char-sequence q-char
```

``` bnf
q-char:
    any member of the source character set except new-line and '"'
```

[*Note 1*: Header name preprocessing tokens only appear within a
`#include` preprocessing directive (see 
[[lex.pptoken]]). — *end note*]

The sequences in both forms of *header-name*s are mapped in an
*implementation-defined* manner to headers or to external source file
names as specified in  [[cpp.include]].

The appearance of either of the characters `'` or `\` or of either of
the character sequences `/*` or `//` in a *q-char-sequence* or an
*h-char-sequence* is conditionally-supported with
*implementation-defined* semantics, as is the appearance of the
character `"` in an *h-char-sequence*.[^9]

## Preprocessing numbers <a id="lex.ppnumber">[[lex.ppnumber]]</a>

``` bnf
pp-number:
    digit
    '.' digit
    pp-number digit
    pp-number identifier-nondigit
    pp-number ''' digit
    pp-number ''' nondigit
    pp-number 'e' sign
    pp-number 'E' sign
    pp-number 'p' sign
    pp-number 'P' sign
    pp-number '.'
```

Preprocessing number tokens lexically include all integer literal
tokens ([[lex.icon]]) and all floating literal tokens ([[lex.fcon]]).

A preprocessing number does not have a type or a value; it acquires both
after a successful conversion to an integer literal token or a floating
literal token.

## Identifiers <a id="lex.name">[[lex.name]]</a>

``` bnf
identifier:
    identifier-nondigit
    identifier identifier-nondigit
    identifier digit
```

``` bnf
identifier-nondigit:
    nondigit
    universal-character-name
```

``` bnf
nondigit: one of
    'a b c d e f g h i j k l m'
    'n o p q r s t u v w x y z'
    'A B C D E F G H I J K L M'
    'N O P Q R S T U V W X Y Z _'
```

``` bnf
digit: one of
    '0 1 2 3 4 5 6 7 8 9'
```

An identifier is an arbitrarily long sequence of letters and digits.
Each *universal-character-name* in an identifier shall designate a
character whose encoding in ISO 10646 falls into one of the ranges
specified in Table  [[tab:charname.allowed]]. The initial element shall
not be a *universal-character-name* designating a character whose
encoding falls into one of the ranges specified in Table 
[[tab:charname.disallowed]]. Upper- and lower-case letters are
different. All characters are significant.[^10]

**Table: Ranges of characters allowed**

|               |               |               |               |               |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `00A8`        | `00AA`        | `00AD`        | `00AF`        | `00B2-00B5`   |
| `00B7-00BA`   | `00BC-00BE`   | `00C0-00D6`   | `00D8-00F6`   | `00F8-00FF`   |
| `0100-167F`   | `1681-180D`   | `180F-1FFF`   |               |               |
| `200B-200D`   | `202A-202E`   | `203F-2040`   | `2054`        | `2060-206F`   |
| `2070-218F`   | `2460-24FF`   | `2776-2793`   | `2C00-2DFF`   | `2E80-2FFF`   |
| `3004-3007`   | `3021-302F`   | `3031-D7FF`   |               |               |
| `F900-FD3D`   | `FD40-FDCF`   | `FDF0-FE44`   | `FE47-FFFD`   |               |
| `10000-1FFFD` | `20000-2FFFD` | `30000-3FFFD` | `40000-4FFFD` | `50000-5FFFD` |
| `60000-6FFFD` | `70000-7FFFD` | `80000-8FFFD` | `90000-9FFFD` | `A0000-AFFFD` |
| `B0000-BFFFD` | `C0000-CFFFD` | `D0000-DFFFD` | `E0000-EFFFD` |               |


**Table: Ranges of characters disallowed initially (combining characters)**

|             |                                                |             |             |
| ----------- | ---------------------------------------------- | ----------- | ----------- |
| `0300-036F` | % FIXME: Unicode v7 adds 1AB0-1AFF `1DC0-1DFF` | `20D0-20FF` | `FE20-FE2F` |


The identifiers in Table  [[tab:identifiers.special]] have a special
meaning when appearing in a certain context. When referred to in the
grammar, these identifiers are used explicitly rather than using the
*identifier* grammar production. Unless otherwise specified, any
ambiguity as to whether a given *identifier* has a special meaning is
resolved to interpret the token as a regular *identifier*.

**Table: Identifiers with special meaning**

|            |         |
| ---------- | ------- |
| `override` | `final` |


In addition, some identifiers are reserved for use by C++
implementations and shall not be used otherwise; no diagnostic is
required.

- Each identifier that contains a double underscore `__` or begins with
  an underscore followed by an uppercase letter is reserved to the
  implementation for any use.
- Each identifier that begins with an underscore is reserved to the
  implementation for use as a name in the global namespace.

## Keywords <a id="lex.key">[[lex.key]]</a>

The identifiers shown in Table  [[tab:keywords]] are reserved for use as
keywords (that is, they are unconditionally treated as keywords in phase
7) except in an *attribute-token* ([[dcl.attr.grammar]]):

**Table: Keywords**

|              |                |             |                    |            |
| ------------ | -------------- | ----------- | ------------------ | ---------- |
| `alignas`    | `continue`     | `friend`    | `register`         | `true`     |
| `alignof`    | `decltype`     | `goto`      | `reinterpret_cast` | `try`      |
| `asm`        | `default`      | `if`        | `return`           | `typedef`  |
| `auto`       | `delete`       | `inline`    | `short`            | `typeid`   |
| `bool`       | `do`           | `int`       | `signed`           | `typename` |
| `break`      | `double`       | `long`      | `sizeof`           | `union`    |
| `case`       | `dynamic_cast` | `mutable`   | `static`           | `unsigned` |
| `catch`      | `else`         | `namespace` | `static_assert`    | `using`    |
| `char`       | `enum`         | `new`       | `static_cast`      | `virtual`  |
| `char16_t`   | `explicit`     | `noexcept`  | `struct`           | `void`     |
| `char32_t`   | `export`       | `nullptr`   | `switch`           | `volatile` |
| `class`      | `extern`       | `operator`  | `template`         | `wchar_t`  |
| `const`      | `false`        | `private`   | `this`             | `while`    |
| `constexpr`  | `float`        | `protected` | `thread_local`     |            |
| `const_cast` | `for`          | `public`    | `throw`            |            |


[*Note 1*: The `export` and `register` keywords are unused but are
reserved for future use. — *end note*]

Furthermore, the alternative representations shown in Table 
[[tab:alternative.representations]] for certain operators and
punctuators ([[lex.digraph]]) are reserved and shall not be used
otherwise:

**Table: Alternative representations**

|          |          |          |         |          |       |
| -------- | -------- | -------- | ------- | -------- | ----- |
| `and`    | `and_eq` | `bitand` | `bitor` | `compl`  | `not` |
| `not_eq` | `or`     | `or_eq`  | `xor`   | `xor_eq` |       |

## Operators and punctuators <a id="lex.operators">[[lex.operators]]</a>

The lexical representation of C++programs includes a number of
preprocessing tokens which are used in the syntax of the preprocessor or
are converted into tokens for operators and punctuators:

Each *preprocessing-op-or-punc* is converted to a single token in
translation phase 7 ([[lex.phases]]).

## Literals <a id="lex.literal">[[lex.literal]]</a>

### Kinds of literals <a id="lex.literal.kinds">[[lex.literal.kinds]]</a>

There are several kinds of literals.[^11]

``` bnf
literal:
    integer-literal
    character-literal
    floating-literal
    string-literal
    boolean-literal
    pointer-literal
    user-defined-literal
```

### Integer literals <a id="lex.icon">[[lex.icon]]</a>

``` bnf
integer-literal:
    binary-literal integer-suffix\opt
    octal-literal integer-suffix\opt
    decimal-literal integer-suffix\opt
    hexadecimal-literal integer-suffix\opt
```

``` bnf
binary-literal:
    '0b' binary-digit
    '0B' binary-digit
    binary-literal '''bₒₚₜinary-digit
```

``` bnf
octal-literal:
    '0'
    octal-literal '''oₒₚₜctal-digit
```

``` bnf
decimal-literal:
    nonzero-digit
    decimal-literal '''dₒₚₜigit
```

``` bnf
hexadecimal-literal:
    hexadecimal-prefix hexadecimal-digit-sequence
```

``` bnf
binary-digit:
    '0'
    '1'
```

``` bnf
octal-digit: one of
    '0  1  2  3  4  5  6  7'
```

``` bnf
nonzero-digit: one of
    '1  2  3  4  5  6  7  8  9'
```

``` bnf
hexadecimal-prefix: one of
    '0x  0X'
```

``` bnf
hexadecimal-digit-sequence:
    hexadecimal-digit
    hexadecimal-digit-sequence '''hₒₚₜexadecimal-digit
```

``` bnf
hexadecimal-digit: one of
    '0  1  2  3  4  5  6  7  8  9'
    'a  b  c  d  e  f'
    'A  B  C  D  E  F'
```

``` bnf
integer-suffix:
    unsigned-suffix long-suffix\opt 
    unsigned-suffix long-long-suffix\opt 
    long-suffix unsigned-suffix\opt 
    long-long-suffix unsigned-suffix\opt
```

``` bnf
unsigned-suffix: one of
    'u  U'
```

``` bnf
long-suffix: one of
    'l  L'
```

``` bnf
long-long-suffix: one of
    'll  LL'
```

An *integer literal* is a sequence of digits that has no period or
exponent part, with optional separating single quotes that are ignored
when determining its value. An integer literal may have a prefix that
specifies its base and a suffix that specifies its type. The lexically
first digit of the sequence of digits is the most significant. A
*binary integer literal* (base two) begins with `0b` or `0B` and
consists of a sequence of binary digits. An *octal integer literal*
(base eight) begins with the digit `0` and consists of a sequence of
octal digits.[^12] A *decimal integer literal* (base ten) begins with a
digit other than `0` and consists of a sequence of decimal digits. A
*hexadecimal integer literal* (base sixteen) begins with `0x` or `0X`
and consists of a sequence of hexadecimal digits, which include the
decimal digits and the letters `a` through `f` and `A` through `F` with
decimal values ten through fifteen.

[*Example 1*: The number twelve can be written `12`, `014`, `0XC`, or
`0b1100`. The integer literals `1048576`, `1'048'576`, `0X100000`,
`0x10'0000`, and `0'004'000'000` all have the same
value. — *end example*]

The type of an integer literal is the first of the corresponding list in
Table  [[tab:lex.type.integer.literal]] in which its value can be
represented.

**Table: Types of integer literals**

|                  |                          |                          |
| ---------------- | ------------------------ | ------------------------ |
| none             | `int`                    | `int`                    |
|                  | `long int`               | `unsigned int`           |
|                  | `long long int`          | `long int`               |
|                  |                          | `unsigned long int`      |
|                  |                          | `long long int`          |
|                  |                          | `unsigned long long int` |
| `u` or `U`       | `unsigned int`           | `unsigned int`           |
|                  | `unsigned long int`      | `unsigned long int`      |
|                  | `unsigned long long int` | `unsigned long long int` |
| `l` or `L`       | `long int`               | `long int`               |
|                  | `long long int`          | `unsigned long int`      |
|                  |                          | `long long int`          |
|                  |                          | `unsigned long long int` |
| Both `u` or `U`  | `unsigned long int`      | `unsigned long int`      |
| and `l` or `L`   | `unsigned long long int` | `unsigned long long int` |
| `ll` or `LL`     | `long long int`          | `long long int`          |
|                  |                          | `unsigned long long int` |
| Both `u` or `U`  | `unsigned long long int` | `unsigned long long int` |
| and `ll` or `LL` |                          |                          |


If an integer literal cannot be represented by any type in its list and
an extended integer type ([[basic.fundamental]]) can represent its
value, it may have that extended integer type. If all of the types in
the list for the integer literal are signed, the extended integer type
shall be signed. If all of the types in the list for the integer literal
are unsigned, the extended integer type shall be unsigned. If the list
contains both signed and unsigned types, the extended integer type may
be signed or unsigned. A program is ill-formed if one of its translation
units contains an integer literal that cannot be represented by any of
the allowed types.

### Character literals <a id="lex.ccon">[[lex.ccon]]</a>

``` bnf
character-literal:
    encoding-prefixₒₚₜ ''' c-char-sequence '''
```

``` bnf
encoding-prefix: one of
    'u8' 'u' 'U' 'L'
```

``` bnf
c-char-sequence:
    c-char
    c-char-sequence c-char
```

``` bnf
escape-sequence:
    simple-escape-sequence
    octal-escape-sequence
    hexadecimal-escape-sequence
```

``` bnf
simple-escape-sequence: one of
    '\'' '\"' '\?' '\\'
    '\a' '\b' '\f' '\n' '\r' '\t' '\v'
```

``` bnf
octal-escape-sequence:
    '\' octal-digit
    '\' octal-digit octal-digit
    '\' octal-digit octal-digit octal-digit
```

``` bnf
hexadecimal-escape-sequence:
    '\x' hexadecimal-digit
    hexadecimal-escape-sequence hexadecimal-digit
```

A character literal is one or more characters enclosed in single quotes,
as in `'x'`, optionally preceded by `u8`, `u`, `U`, or `L`, as in
`u8'w'`, `u'x'`, `U'y'`, or `L'z'`, respectively.

A character literal that does not begin with `u8`, `u`, `U`, or `L` is
an *ordinary character literal*. An ordinary character literal that
contains a single *c-char* representable in the execution character set
has type `char`, with value equal to the numerical value of the encoding
of the *c-char* in the execution character set. An ordinary character
literal that contains more than one *c-char* is a
*multicharacter literal*. A multicharacter literal, or an ordinary
character literal containing a single *c-char* not representable in the
execution character set, is conditionally-supported, has type `int`, and
has an *implementation-defined* value.

A character literal that begins with `u8`, such as `u8'w'`, is a
character literal of type `char`, known as a *UTF-8 character literal*.
The value of a UTF-8 character literal is equal to its ISO 10646 code
point value, provided that the code point value is representable with a
single UTF-8 code unit (that is, provided it is in the C0 Controls and
Basic Latin Unicode block). If the value is not representable with a
single UTF-8 code unit, the program is ill-formed. A UTF-8 character
literal containing multiple *c-char*s is ill-formed.

A character literal that begins with the letter `u`, such as `u'x'`, is
a character literal of type `char16_t`. The value of a `char16_t`
character literal containing a single *c-char* is equal to its ISO 10646
code point value, provided that the code point is representable with a
single 16-bit code unit. (That is, provided it is a basic multi-lingual
plane code point.) If the value is not representable within 16 bits, the
program is ill-formed. A `char16_t` character literal containing
multiple *c-char*s is ill-formed.

A character literal that begins with the letter `U`, such as `U'y'`, is
a character literal of type `char32_t`. The value of a `char32_t`
character literal containing a single *c-char* is equal to its ISO 10646
code point value. A `char32_t` character literal containing multiple
*c-char*s is ill-formed.

A character literal that begins with the letter `L`, such as `L'z'`, is
a *wide-character literal*. A wide-character literal has type
`wchar_t`.[^13] The value of a wide-character literal containing a
single *c-char* has value equal to the numerical value of the encoding
of the *c-char* in the execution wide-character set, unless the *c-char*
has no representation in the execution wide-character set, in which case
the value is *implementation-defined*.

[*Note 1*: The type `wchar_t` is able to represent all members of the
execution wide-character set (see 
[[basic.fundamental]]). — *end note*]

The value of a wide-character literal containing multiple *c-char*s is
*implementation-defined*.

Certain non-graphic characters, the single quote `'`, the double quote
`"`, the question mark `?`,[^14] and the backslash `\`, can be
represented according to Table  [[tab:escape.sequences]]. The double
quote `"` and the question mark `?`, can be represented as themselves or
by the escape sequences `\"` and `\?` respectively, but the single quote
`'` and the backslash `\` shall be represented by the escape sequences
`\'` and `\\` respectively. Escape sequences in which the character
following the backslash is not listed in Table  [[tab:escape.sequences]]
are conditionally-supported, with *implementation-defined* semantics. An
escape sequence specifies a single character.

**Table: Escape sequences**

|                 |                |                    |
| --------------- | -------------- | ------------------ |
| new-line        | NL(LF)         | `\n`               |
| horizontal tab  | HT             | `\t`               |
| vertical tab    | VT             | `\v`               |
| backspace       | BS             | `\b`               |
| carriage return | CR             | `\r`               |
| form feed       | FF             | `\f`               |
| alert           | BEL            | `\a`               |
| backslash       | \              | ``                 |
| question mark   | ?              | `\?`               |
| single quote    | `'`            | `\'`               |
| double quote    | `"`            | `\"`               |
| octal number    | \numconst{ooo} | `numconst{ooo}`    |
| hex number      | \numconst{hhh} | `\x\numconst{hhh}` |


The escape `\\numconst{ooo}` consists of the backslash followed by one,
two, or three octal digits that are taken to specify the value of the
desired character. The escape `\x\numconst{hhh}` consists of the
backslash followed by `x` followed by one or more hexadecimal digits
that are taken to specify the value of the desired character. There is
no limit to the number of digits in a hexadecimal sequence. A sequence
of octal or hexadecimal digits is terminated by the first character that
is not an octal digit or a hexadecimal digit, respectively. The value of
a character literal is *implementation-defined* if it falls outside of
the *implementation-defined* range defined for `char` (for character
literals with no prefix) or `wchar_t` (for character literals prefixed
by `L`).

[*Note 2*: If the value of a character literal prefixed by `u`, `u8`,
or `U` is outside the range defined for its type, the program is
ill-formed. — *end note*]

A *universal-character-name* is translated to the encoding, in the
appropriate execution character set, of the character named. If there is
no such encoding, the *universal-character-name* is translated to an
*implementation-defined* encoding.

[*Note 3*: In translation phase 1, a *universal-character-name* is
introduced whenever an actual extended character is encountered in the
source text. Therefore, all extended characters are described in terms
of *universal-character-name*s. However, the actual compiler
implementation may use its own native character set, so long as the same
results are obtained. — *end note*]

### Floating literals <a id="lex.fcon">[[lex.fcon]]</a>

``` bnf
floating-literal:
    decimal-floating-literal
    hexadecimal-floating-literal
```

``` bnf
decimal-floating-literal:
    fractional-constant exponent-part\opt floating-suffix\opt
    digit-sequence exponent-part floating-suffix\opt
```

``` bnf
hexadecimal-floating-literal:
    hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part floating-suffix\opt
    hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part floating-suffix\opt
```

``` bnf
fractional-constant:
    digit-sequenceₒₚₜ '.' digit-sequence
    digit-sequence '.'
```

``` bnf
hexadecimal-fractional-constant:
    hexadecimal-digit-sequenceₒₚₜ '.' hexadecimal-digit-sequence
    hexadecimal-digit-sequence '.'
```

``` bnf
exponent-part:
    'e' signdₒₚₜigit-sequence
    'E' signdₒₚₜigit-sequence
```

``` bnf
binary-exponent-part:
    'p' signdₒₚₜigit-sequence
    'P' signdₒₚₜigit-sequence
```

``` bnf
sign: one of
    '+  -'
```

``` bnf
digit-sequence:
    digit
    digit-sequence '''dₒₚₜigit
```

``` bnf
floating-suffix: one of
    'f  l  F  L'
```

A floating literal consists of an optional prefix specifying a base, an
integer part, a radix point, a fraction part, an `e`, `E`, `p` or `P`,
an optionally signed integer exponent, and an optional type suffix. The
integer and fraction parts both consist of a sequence of decimal (base
ten) digits if there is no prefix, or hexadecimal (base sixteen) digits
if the prefix is `0x` or `0X`. The floating literal is a
*decimal floating literal* in the former case and a
*hexadecimal floating literal* in the latter case. Optional separating
single quotes in a *digit-sequence* or *hexadecimal-digit-sequence* are
ignored when determining its value.

[*Example 1*: The floating literals `1.602'176'565e-19` and
`1.602176565e-19` have the same value. — *end example*]

Either the integer part or the fraction part (not both) can be omitted.
Either the radix point or the letter `e` or `E` and the exponent (not
both) can be omitted from a decimal floating literal. The radix point
(but not the exponent) can be omitted from a hexadecimal floating
literal. The integer part, the optional radix point, and the optional
fraction part, form the *significand* of the floating literal. In a
decimal floating literal, the exponent, if present, indicates the power
of 10 by which the significand is to be scaled. In a hexadecimal
floating literal, the exponent indicates the power of 2 by which the
significand is to be scaled.

[*Example 2*: The floating literals `49.625` and `0xC.68p+2` have the
same value. — *end example*]

If the scaled value is in the range of representable values for its
type, the result is the scaled value if representable, else the larger
or smaller representable value nearest the scaled value, chosen in an
*implementation-defined* manner. The type of a floating literal is
`double` unless explicitly specified by a suffix. The suffixes `f` and
`F` specify `float`, the suffixes `l` and `L` specify `long` `double`.
If the scaled value is not in the range of representable values for its
type, the program is ill-formed.

### String literals <a id="lex.string">[[lex.string]]</a>

``` bnf
string-literal:
    encoding-prefixₒₚₜ '"' s-char-sequenceₒₚₜ '"'
    encoding-prefixₒₚₜ 'R' raw-string
```

``` bnf
s-char-sequence:
    s-char
    s-char-sequence s-char
```

``` bnf
raw-string:
    '"' d-char-sequenceₒₚₜ '(' r-char-sequenceₒₚₜ ')' d-char-sequenceₒₚₜ '"'
```

``` bnf
r-char-sequence:
    r-char
    r-char-sequence r-char
```

``` bnf
d-char-sequence:
    d-char
    d-char-sequence d-char
```

A *string-literal* is a sequence of characters (as defined in 
[[lex.ccon]]) surrounded by double quotes, optionally prefixed by `R`,
`u8`, `u8R`, `u`, `uR`, `U`, `UR`, `L`, or `LR`, as in `"..."`,
`R"(...)"`, `u8"..."`, `u8R"**(...)**"`, `u"..."`, `uR"*~(...)*~"`,
`U"..."`, `UR"zzz(...)zzz"`, `L"..."`, or `LR"(...)"`, respectively.

A *string-literal* that has an `R` in the prefix is a *raw string
literal*. The *d-char-sequence* serves as a delimiter. The terminating
*d-char-sequence* of a *raw-string* is the same sequence of characters
as the initial *d-char-sequence*. A *d-char-sequence* shall consist of
at most 16 characters.

[*Note 1*: The characters `'('` and `')'` are permitted in a
*raw-string*. Thus, `R"delimiter((a|b))delimiter"` is equivalent to
`"(a|b)"`. — *end note*]

[*Note 2*:

A source-file new-line in a raw string literal results in a new-line in
the resulting execution string literal. Assuming no whitespace at the
beginning of lines in the following example, the assert will succeed:

``` cpp
const char* p = R"(a\
b
c)";
assert(std::strcmp(p, "a\\\nb\nc") == 0);
```

— *end note*]

[*Example 1*:

The raw string

``` cpp
R"a(
)\
a"
)a"
```

is equivalent to `"\n)\\\na\"\n"`. The raw string

``` cpp
R"(??)"
```

is equivalent to `"\?\?"`. The raw string

``` cpp
R"#(
)??="
)#"
```

is equivalent to `"\n)\?\?=\"\n"`.

— *end example*]

After translation phase 6, a *string-literal* that does not begin with
an *encoding-prefix* is an *ordinary string literal*, and is initialized
with the given characters.

A *string-literal* that begins with `u8`, such as `u8"asdf"`, is a
*UTF-8 string literal*.

Ordinary string literals and UTF-8 string literals are also referred to
as narrow string literals. A narrow string literal has type “array of
*n* `const char`”, where *n* is the size of the string as defined below,
and has static storage duration ([[basic.stc]]).

For a UTF-8 string literal, each successive element of the object
representation ([[basic.types]]) has the value of the corresponding
code unit of the UTF-8 encoding of the string.

A *string-literal* that begins with `u`, such as `u"asdf"`, is a
`char16_t` string literal. A `char16_t` string literal has type “array
of *n* `const char16_t`”, where *n* is the size of the string as defined
below; it is initialized with the given characters. A single *c-char*
may produce more than one `char16_t` character in the form of surrogate
pairs.

A *string-literal* that begins with `U`, such as `U"asdf"`, is a
`char32_t` string literal. A `char32_t` string literal has type “array
of *n* `const char32_t`”, where *n* is the size of the string as defined
below; it is initialized with the given characters.

A *string-literal* that begins with `L`, such as `L"asdf"`, is a *wide
string literal*. A wide string literal has type “array of *n* `const
wchar_t`”, where *n* is the size of the string as defined below; it is
initialized with the given characters.

In translation phase 6 ([[lex.phases]]), adjacent *string-literal*s are
concatenated. If both *string-literal*s have the same *encoding-prefix*,
the resulting concatenated string literal has that *encoding-prefix*. If
one *string-literal* has no *encoding-prefix*, it is treated as a
*string-literal* of the same *encoding-prefix* as the other operand. If
a UTF-8 string literal token is adjacent to a wide string literal token,
the program is ill-formed. Any other concatenations are
conditionally-supported with *implementation-defined* behavior.

[*Note 3*: This concatenation is an interpretation, not a conversion.
Because the interpretation happens in translation phase 6 (after each
character from a string literal has been translated into a value from
the appropriate character set), a *string-literal*’s initial rawness has
no effect on the interpretation or well-formedness of the
concatenation. — *end note*]

Table  [[tab:lex.string.concat]] has some examples of valid
concatenations.

**Table: String literal concatenations**

|                            |       |                            |       |                            |       |
| -------------------------- | ----- | -------------------------- | ----- | -------------------------- | ----- |
| *[spans 2 columns]* Source | Means | *[spans 2 columns]* Source | Means | *[spans 2 columns]* Source | Means |
| `u"a"`                     | `u"b"` | `u"ab"`                    | `U"a"` | `U"b"`                     | `U"ab"` | `L"a"` | `L"b"` | `L"ab"` |
| `u"a"`                     | `"b"` | `u"ab"`                    | `U"a"` | `"b"`                      | `U"ab"` | `L"a"` | `"b"` | `L"ab"` |
| `"a"`                      | `u"b"` | `u"ab"`                    | `"a"` | `U"b"`                     | `U"ab"` | `"a"` | `L"b"` | `L"ab"` |


Characters in concatenated strings are kept distinct.

[*Example 2*:

``` cpp
"\xA" "B"
```

contains the two characters `'\xA'` and `'B'` after concatenation (and
not the single hexadecimal character `'\xAB'`).

— *end example*]

After any necessary concatenation, in translation phase 7 (
[[lex.phases]]), `'\0'` is appended to every string literal so that
programs that scan a string can find its end.

Escape sequences and *universal-character-name*s in non-raw string
literals have the same meaning as in character literals ([[lex.ccon]]),
except that the single quote `'` is representable either by itself or by
the escape sequence `\'`, and the double quote `"` shall be preceded by
a `\`, and except that a *universal-character-name* in a `char16_t`
string literal may yield a surrogate pair. In a narrow string literal, a
*universal-character-name* may map to more than one `char` element due
to *multibyte encoding*. The size of a `char32_t` or wide string literal
is the total number of escape sequences, *universal-character-name*s,
and other characters, plus one for the terminating `U'\0'` or `L'\0'`.
The size of a `char16_t` string literal is the total number of escape
sequences, *universal-character-name*s, and other characters, plus one
for each character requiring a surrogate pair, plus one for the
terminating `u'\0'`.

[*Note 4*: The size of a `char16_t` string literal is the number of
code units, not the number of characters. — *end note*]

Within `char32_t` and `char16_t` string literals, any
*universal-character-name*s shall be within the range `0x0` to
`0x10FFFF`. The size of a narrow string literal is the total number of
escape sequences and other characters, plus at least one for the
multibyte encoding of each *universal-character-name*, plus one for the
terminating `'\0'`.

Evaluating a *string-literal* results in a string literal object with
static storage duration, initialized from the given characters as
specified above. Whether all string literals are distinct (that is, are
stored in nonoverlapping objects) and whether successive evaluations of
a *string-literal* yield the same or a different object is unspecified.

[*Note 5*:  The effect of attempting to modify a string literal is
undefined. — *end note*]

### Boolean literals <a id="lex.bool">[[lex.bool]]</a>

``` bnf
boolean-literal:
    'false'
    'true'
```

The Boolean literals are the keywords `false` and `true`. Such literals
are prvalues and have type `bool`.

### Pointer literals <a id="lex.nullptr">[[lex.nullptr]]</a>

``` bnf
pointer-literal:
    'nullptr'
```

The pointer literal is the keyword `nullptr`. It is a prvalue of type
`std::nullptr_t`.

[*Note 1*: `std::nullptr_t` is a distinct type that is neither a
pointer type nor a pointer to member type; rather, a prvalue of this
type is a null pointer constant and can be converted to a null pointer
value or null member pointer value. See  [[conv.ptr]] and 
[[conv.mem]]. — *end note*]

### User-defined literals <a id="lex.ext">[[lex.ext]]</a>

``` bnf
user-defined-literal:
    user-defined-integer-literal
    user-defined-floating-literal
    user-defined-string-literal
    user-defined-character-literal
```

``` bnf
user-defined-integer-literal:
    decimal-literal ud-suffix
    octal-literal ud-suffix
    hexadecimal-literal ud-suffix
    binary-literal ud-suffix
```

``` bnf
user-defined-floating-literal:
    fractional-constant exponent-partuₒₚₜd-suffix
    digit-sequence exponent-part ud-suffix
    hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part ud-suffix
    hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part ud-suffix
```

``` bnf
user-defined-string-literal:
    string-literal ud-suffix
```

``` bnf
user-defined-character-literal:
    character-literal ud-suffix
```

``` bnf
ud-suffix:
    identifier
```

If a token matches both *user-defined-literal* and another *literal*
kind, it is treated as the latter.

[*Example 1*:

`123_km`

is a *user-defined-literal*, but `12LL` is an *integer-literal*.

— *end example*]

The syntactic non-terminal preceding the *ud-suffix* in a
*user-defined-literal* is taken to be the longest sequence of characters
that could match that non-terminal.

A *user-defined-literal* is treated as a call to a literal operator or
literal operator template ([[over.literal]]). To determine the form of
this call for a given *user-defined-literal* *L* with *ud-suffix* *X*,
the *literal-operator-id* whose literal suffix identifier is *X* is
looked up in the context of *L* using the rules for unqualified name
lookup ([[basic.lookup.unqual]]). Let *S* be the set of declarations
found by this lookup. *S* shall not be empty.

If *L* is a *user-defined-integer-literal*, let *n* be the literal
without its *ud-suffix*. If *S* contains a literal operator with
parameter type `unsigned long long`, the literal *L* is treated as a
call of the form

``` cpp
operator "" X(nULL)
```

Otherwise, *S* shall contain a raw literal operator or a literal
operator template ([[over.literal]]) but not both. If *S* contains a
raw literal operator, the literal *L* is treated as a call of the form

``` cpp
operator "" X("n{"})
```

Otherwise (*S* contains a literal operator template), *L* is treated as
a call of the form

``` cpp
operator "" X<'c₁', 'c₂', ... 'cₖ'>()
```

where *n* is the source character sequence c₁c_2...cₖ.

[*Note 1*: The sequence c₁c_2...cₖ can only contain characters from the
basic source character set. — *end note*]

If *L* is a *user-defined-floating-literal*, let *f* be the literal
without its *ud-suffix*. If *S* contains a literal operator with
parameter type `long double`, the literal *L* is treated as a call of
the form

``` cpp
operator "" X(fL)
```

Otherwise, *S* shall contain a raw literal operator or a literal
operator template ([[over.literal]]) but not both. If *S* contains a
raw literal operator, the *literal* *L* is treated as a call of the form

``` cpp
operator "" X("f{"})
```

Otherwise (*S* contains a literal operator template), *L* is treated as
a call of the form

``` cpp
operator "" X<'c₁', 'c₂', ... 'cₖ'>()
```

where *f* is the source character sequence c₁c_2...cₖ.

[*Note 2*: The sequence c₁c_2...cₖ can only contain characters from the
basic source character set. — *end note*]

If *L* is a *user-defined-string-literal*, let *str* be the literal
without its *ud-suffix* and let *len* be the number of code units in
*str* (i.e., its length excluding the terminating null character). The
literal *L* is treated as a call of the form

``` cpp
operator "" X(str, len)
```

If *L* is a *user-defined-character-literal*, let *ch* be the literal
without its *ud-suffix*. *S* shall contain a literal operator (
[[over.literal]]) whose only parameter has the type of *ch* and the
literal *L* is treated as a call of the form

``` cpp
operator "" X(ch)
```

[*Example 2*:

``` cpp
long double operator "" _w(long double);
std::string operator "" _w(const char16_t*, std::size_t);
unsigned operator "" _w(const char*);
int main() {
  1.2_w;      // calls operator "" _w(1.2L)
  u"one"_w;   // calls operator "" _w(u"one", 3)
  12_w;       // calls operator "" _w("12")
  "two"_w;    // error: no applicable literal operator
}
```

— *end example*]

In translation phase 6 ([[lex.phases]]), adjacent string literals are
concatenated and *user-defined-string-literal*s are considered string
literals for that purpose. During concatenation, *ud-suffix*es are
removed and ignored and the concatenation process occurs as described
in  [[lex.string]]. At the end of phase 6, if a string literal is the
result of a concatenation involving at least one
*user-defined-string-literal*, all the participating
*user-defined-string-literal*s shall have the same *ud-suffix* and that
suffix is applied to the result of the concatenation.

[*Example 3*:

``` cpp
int main() {
  L"A" "B" "C"_x; // OK: same as L"ABC"_x
  "P"_x "Q" "R"_y;// error: two different ud-suffix{es}
}
```

— *end example*]

<!-- Link reference definitions -->
[basic.fundamental]: basic.md#basic.fundamental
[basic.link]: basic.md#basic.link
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.stc]: basic.md#basic.stc
[basic.types]: basic.md#basic.types
[conv.mem]: conv.md#conv.mem
[conv.ptr]: conv.md#conv.ptr
[cpp]: cpp.md#cpp
[cpp.concat]: cpp.md#cpp.concat
[cpp.cond]: cpp.md#cpp.cond
[cpp.include]: cpp.md#cpp.include
[cpp.stringize]: cpp.md#cpp.stringize
[dcl.attr.grammar]: dcl.md#dcl.attr.grammar
[headers]: library.md#headers
[lex]: #lex
[lex.bool]: #lex.bool
[lex.ccon]: #lex.ccon
[lex.charset]: #lex.charset
[lex.comment]: #lex.comment
[lex.digraph]: #lex.digraph
[lex.ext]: #lex.ext
[lex.fcon]: #lex.fcon
[lex.header]: #lex.header
[lex.icon]: #lex.icon
[lex.key]: #lex.key
[lex.literal]: #lex.literal
[lex.literal.kinds]: #lex.literal.kinds
[lex.name]: #lex.name
[lex.nullptr]: #lex.nullptr
[lex.operators]: #lex.operators
[lex.phases]: #lex.phases
[lex.ppnumber]: #lex.ppnumber
[lex.pptoken]: #lex.pptoken
[lex.separate]: #lex.separate
[lex.string]: #lex.string
[lex.token]: #lex.token
[over.literal]: over.md#over.literal
[tab:alternative.representations]: #tab:alternative.representations
[tab:alternative.tokens]: #tab:alternative.tokens
[tab:charname.allowed]: #tab:charname.allowed
[tab:charname.disallowed]: #tab:charname.disallowed
[tab:escape.sequences]: #tab:escape.sequences
[tab:identifiers.special]: #tab:identifiers.special
[tab:keywords]: #tab:keywords
[tab:lex.string.concat]: #tab:lex.string.concat
[tab:lex.type.integer.literal]: #tab:lex.type.integer.literal
[temp.explicit]: temp.md#temp.explicit
[temp.names]: temp.md#temp.names

[^1]: Implementations must behave as if these separate phases occur,
    although in practice different phases might be folded together.

[^2]: A partial preprocessing token would arise from a source file
    ending in the first portion of a multi-character token that requires
    a terminating sequence of characters, such as a *header-name* that
    is missing the closing `"` or `>`. A partial comment would arise
    from a source file ending with an unclosed `/*` comment.

[^3]: An implementation need not convert all non-corresponding source
    characters to the same execution character.

[^4]: The glyphs for the members of the basic source character set are
    intended to identify characters from the subset of ISO/IEC 10646
    which corresponds to the ASCII character set. However, because the
    mapping from source file characters to the source character set
    (described in translation phase 1) is specified as
    *implementation-defined*, an implementation is required to document
    how the basic source characters are represented in source files.

[^5]: A sequence of characters resembling a *universal-character-name*
    in an *r-char-sequence* ([[lex.string]]) does not form a
    *universal-character-name*.

[^6]:  These include “digraphs” and additional reserved words. The term
    “digraph” (token consisting of two characters) is not perfectly
    descriptive, since one of the alternative preprocessing-tokens is
    `%:%:` and of course several primary tokens contain two characters.
    Nonetheless, those alternative tokens that aren’t lexical keywords
    are colloquially known as “digraphs”.

[^7]: Thus the “stringized” values ([[cpp.stringize]]) of `[` and `<:`
    will be different, maintaining the source spelling, but the tokens
    can otherwise be freely interchanged.

[^8]: Literals include strings and character and numeric literals.

[^9]: Thus, a sequence of characters that resembles an escape sequence
    might result in an error, be interpreted as the character
    corresponding to the escape sequence, or have a completely different
    meaning, depending on the implementation.

[^10]: On systems in which linkers cannot accept extended characters, an
    encoding of the *universal-character-name* may be used in forming
    valid external identifiers. For example, some otherwise unused
    character or sequence of characters may be used to encode the `\u`
    in a *universal-character-name*. Extended characters may produce a
    long external identifier, but C++does not place a translation limit
    on significant characters for external identifiers. In C++, upper-
    and lower-case letters are considered different for all identifiers,
    including external identifiers.

[^11]: The term “literal” generally designates, in this International
    Standard, those tokens that are called “constants” in ISO C.

[^12]: The digits `8` and `9` are not octal digits.

[^13]: They are intended for character sets where a character does not
    fit into a single byte.

[^14]: Using an escape sequence for a question mark is supported for
    compatibility with ISO C++14and ISO C.
