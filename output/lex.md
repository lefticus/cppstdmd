---
current_file: lex
label_index_file: converted/cppstdmd/output/cpp_std_labels.lua
---

# Lexical conventions <a id="lex">[[lex]]</a>

## Separate translation <a id="lex.separate">[[lex.separate]]</a>

The text of the program is kept in units called *source files* in this
document. A source file together with all the headers [[headers]] and
source files included [[cpp.include]] via the preprocessing directive
`#include`, less any source lines skipped by any of the conditional
inclusion [[cpp.cond]] preprocessing directives, is called a
*preprocessing translation unit*.

\[*Note 1*: A C++ program need not all be translated at the same
time. — *end note*\]

\[*Note 2*: Previously translated translation units and instantiation
units can be preserved individually or in libraries. The separate
translation units of a program communicate [[basic.link]] by (for
example) calls to functions whose identifiers have external or module
linkage, manipulation of objects whose identifiers have external or
module linkage, or manipulation of data files. Translation units can be
separately translated and then later linked to produce an executable
program [[basic.link]]. — *end note*\]

## Phases of translation <a id="lex.phases">[[lex.phases]]</a>

The precedence among the syntax rules of translation is specified by the
following phases.

1.   An implementation shall support input files that are a sequence of
    UTF-8 code units (UTF-8 files). It may also support an
    *implementation-defined* set of other kinds of input files, and, if
    so, the kind of an input file is determined in an
    *implementation-defined* manner that includes a means of designating
    input files as UTF-8 files, independent of their content.

    \[*Note 1*: In other words, recognizing the is not
    sufficient. — *end note*\]

    If an input file is determined to be a UTF-8 file, then it shall be
    a well-formed UTF-8 code unit sequence and it is decoded to produce
    a sequence of Unicode scalar values. A sequence of translation
    character set elements is then formed by mapping each Unicode scalar
    value to the corresponding translation character set element. In the
    resulting sequence, each pair of characters in the input sequence
    consisting of followed by , as well as each not immediately followed
    by a , is replaced by a single new-line character.

    For any other kind of input file supported by the implementation,
    characters are mapped, in an *implementation-defined* manner, to a
    sequence of translation character set elements [[lex.charset]],
    representing end-of-line indicators as new-line characters.

2.   If the first translation character is , it is deleted. Each
    sequence of a backslash character (\\ immediately followed by zero
    or more whitespace characters other than new-line followed by a
    new-line character is deleted, splicing physical source lines to
    form logical source lines. Only the last backslash on any physical
    source line shall be eligible for being part of such a splice.
    Except for splices reverted in a raw string literal, if a splice
    results in a character sequence that matches the syntax of a
    *universal-character-name*, the behavior is undefined. A source file
    that is not empty and that does not end in a new-line character, or
    that ends in a splice, shall be processed as if an additional
    new-line character were appended to the file.

3.  The source file is decomposed into preprocessing tokens
    [[lex.pptoken]] and sequences of whitespace characters (including
    comments). A source file shall not end in a partial preprocessing
    token or in a partial comment.

    Each comment is replaced by one space character. New-line characters
    are retained. Whether each nonempty sequence of whitespace
    characters other than new-line is retained or replaced by one space
    character is unspecified. As characters from the source file are
    consumed to form the next preprocessing token (i.e., not being
    consumed as part of a comment or other forms of whitespace), except
    when matching a *c-char-sequence*, *s-char-sequence*,
    *r-char-sequence*, *h-char-sequence*, or *q-char-sequence*,
    *universal-character-name*s are recognized and replaced by the
    designated element of the translation character set. The process of
    dividing a source file’s characters into preprocessing tokens is
    context-dependent.

    \[*Example 1*: See the handling of `<` within a `#include`
    preprocessing directive. — *end example*\]

4.  Preprocessing directives are executed, macro invocations are
    expanded, and `_Pragma` unary operator expressions are executed. A
    `#include` preprocessing directive causes the named header or source
    file to be processed from phase 1 through phase 4, recursively. All
    preprocessing directives are then deleted.

5.  For a sequence of two or more adjacent *string-literal* tokens, a
    common *encoding-prefix* is determined as specified in
    [[lex.string]]. Each such *string-literal* token is then considered
    to have that common *encoding-prefix*.

6.  Adjacent *string-literal* tokens are concatenated [[lex.string]].

7.  Whitespace characters separating tokens are no longer significant.
    Each preprocessing token is converted into a token [[lex.token]].
    The resulting tokens constitute a *translation unit* and are
    syntactically and semantically analyzed and translated.

    \[*Note 2*: The process of analyzing and translating the tokens can
    occasionally result in one token being replaced by a sequence of
    other tokens [[temp.names]]. — *end note*\]

    It is *implementation-defined* whether the sources for module units
    and header units on which the current translation unit has an
    interface dependency [[module.unit]], [[module.import]] are required
    to be available.

    \[*Note 3*: Source files, translation units and translated
    translation units need not necessarily be stored as files, nor need
    there be any one-to-one correspondence between these entities and
    any external representation. The description is conceptual only, and
    does not specify any particular implementation. — *end note*\]

8.  Translated translation units and instantiation units are combined as
    follows:

    \[*Note 4*: Some or all of these can be supplied from a
    library. — *end note*\]

    Each translated translation unit is examined to produce a list of
    required instantiations.

    \[*Note 5*: This can include instantiations which have been
    explicitly requested [[temp.explicit]]. — *end note*\]

    The definitions of the required templates are located. It is
    *implementation-defined* whether the source of the translation units
    containing these definitions is required to be available.

    \[*Note 6*: An implementation can choose to encode sufficient
    information into the translated translation unit so as to ensure the
    source is not required here. — *end note*\]

    All the required instantiations are performed to produce
    *instantiation units*.

    \[*Note 7*: These are similar to translated translation units, but
    contain no references to uninstantiated templates and no template
    definitions. — *end note*\]

    The program is ill-formed if any instantiation fails.

9.  All external entity references are resolved. Library components are
    linked to satisfy external references to entities not defined in the
    current translation. All such translator output is collected into a
    program image which contains information needed for execution in its
    execution environment.

## Character sets <a id="lex.charset">[[lex.charset]]</a>

The *translation character set* consists of the following elements:

- each abstract character assigned a code point in the Unicode
  codespace, and

- a distinct character for each Unicode scalar value not assigned to an
  abstract character.

\[*Note 1*: Unicode code points are integers in the range [0, 10FFFF]
(hexadecimal). A surrogate code point is a value in the range
[D800, DFFF] (hexadecimal). A Unicode scalar value is any code point
that is not a surrogate code point. — *end note*\]

The *basic character set* is a subset of the translation character set,
consisting of 96 characters as specified in [[lex.charset.basic]].

\[*Note 2*: Unicode short names are given only as a means to identifying
the character; the numerical value has no other meaning in this
context. — *end note*\]

**Table: Basic character set**

|  |  |
| --- | --- |
| `U+0009` | \uname{character tabulation} |
| `U+000b` | \uname{line tabulation} |
| `U+000c` | \uname{form feed} |
| `U+0020` | \uname{space} |
| `U+000a` | \uname{line feed} | new-line |
| `U+0021` | \uname{exclamation mark} | `!` |
| `U+0022` | \uname{quotation mark} | `"` |
| `U+0023` | \uname{number sign} | `\#` |
| `U+0025` | \uname{percent sign} | `\%` |
| `U+0026` | \uname{ampersand} | `\&` |
| `U+0027` | \uname{apostrophe} | `'` |
| `U+0028` | \uname{left parenthesis} | `(` |
| `U+0029` | \uname{right parenthesis} | `)` |
| `U+002a` | \uname{asterisk} | `*` |
| `U+002b` | \uname{plus sign} | `+` |
| `U+002c` | \uname{comma} | `,` |
| `U+002d` | \uname{hyphen-minus} | `-` |
| `U+002e` | \uname{full stop} | `.` |
| `U+002f` | \uname{solidus} | `/` |
| `U+0030` .. `U+0039` | \uname{digit zero .. nine} | `0 1 2 3 4 5 6 7 8 9` |
| `U+003a` | \uname{colon} | `:` |
| `U+003b` | \uname{semicolon} | `;` |
| `U+003c` | \uname{less-than sign} | `<` |
| `U+003d` | \uname{equals sign} | `=` |
| `U+003e` | \uname{greater-than sign} | `>` |
| `U+003f` | \uname{question mark} | `?` |
| `U+0041` .. `U+005a` | \uname{latin capital letter a .. z} | `A B C D E F G H I J K L M` |
|  |  | `N O P Q R S T U V W X Y Z` |
| `U+005b` | \uname{left square bracket} | `[` |
| `U+005c` | \uname{reverse solidus} | `\` |
| `U+005d` | \uname{right square bracket} | `]` |
| `U+005e` | \uname{circumflex accent} | `\caret` |
| `U+005f` | \uname{low line} | `_` |
| `U+0061` .. `U+007a` | \uname{latin small letter a .. z} | `a b c d e f g h i j k l m` |
|  |  | `n o p q r s t u v w x y z` |
| `U+007b` | \uname{left curly bracket} | \texttt{\{} |
| `U+007c` | \uname{vertical line} | `|` |
| `U+007d` | \uname{right curly bracket} | `\`} |
| `U+007e` | \uname{tilde} | `\textasciitilde` |
The *universal-character-name* construct provides a way to name other
characters.

``` bnf
n-char: one of
     any member of the translation character set except the \unicode{007d{right curly bracket} or new-line character}
```

``` bnf
n-char-sequence:
    n-char
    n-char-sequence n-char
```

``` bnf
named-universal-character:
    '\ N{' n-char-sequence '$'}
```

``` bnf
hex-quad:
    hexadecimal-digit hexadecimal-digit hexadecimal-digit hexadecimal-digit
```

``` bnf
simple-hexadecimal-digit-sequence:
    hexadecimal-digit
    simple-hexadecimal-digit-sequence hexadecimal-digit
```

``` bnf
universal-character-name:
    '\ u' hex-quad
    '\ U' hex-quad hex-quad
    '\ u{' simple-hexadecimal-digit-sequence '$'}
    named-universal-character
```

A *universal-character-name* of the form `\ u` *hex-quad*, `\ U`
*hex-quad* *hex-quad*, or `\ u\{simple-hexadecimal-digit-sequence\}`
designates the character in the translation character set whose Unicode
scalar value is the hexadecimal number represented by the sequence of
*hexadecimal-digit*s in the *universal-character-name*. The program is
ill-formed if that number is not a Unicode scalar value.

A *universal-character-name* that is a *named-universal-character*
designates the corresponding character in the Unicode Standard (chapter
4.8 Name) if the *n-char-sequence* is equal to its character name or to
one of its character name aliases of type “control”, “correction”, or
“alternate”; otherwise, the program is ill-formed.

\[*Note 3*: These aliases are listed in the Unicode Character Database’s
`NameAliases.txt`. None of these names or aliases have leading or
trailing spaces. — *end note*\]

If a *universal-character-name* outside the *c-char-sequence*,
*s-char-sequence*, or *r-char-sequence* of a *character-literal* or
*string-literal* (in either case, including within a
*user-defined-literal*) corresponds to a control character or to a
character in the basic character set, the program is ill-formed.

\[*Note 4*: A sequence of characters resembling a
*universal-character-name* in an *r-char-sequence* [[lex.string]] does
not form a *universal-character-name*. — *end note*\]

The *basic literal character set* consists of all characters of the
basic character set, plus the control characters specified in
[[lex.charset.literal]].

**Table: Additional control characters in the basic literal character set**

|  |  |
| --- | --- |
| `U+0000` | \uname{null} |
| `U+0007` | \uname{alert} |
| `U+0008` | \uname{backspace} |
| `U+000d` | \uname{carriage return} |
A *code unit* is an integer value of character type
[[basic.fundamental]]. Characters in a *character-literal* other than a
multicharacter or non-encodable character literal or in a
*string-literal* are encoded as a sequence of one or more code units, as
determined by the *encoding-prefix* [[lex.ccon]], [[lex.string]]; this
is termed the respective *literal encoding*. The
*ordinary literal encoding* is the encoding applied to an ordinary
character or string literal. The *wide literal encoding* is the encoding
applied to a wide character or string literal.

A literal encoding or a locale-specific encoding of one of the execution
character sets [[character.seq]] encodes each element of the basic
literal character set as a single code unit with non-negative value,
distinct from the code unit for any other such element.

\[*Note 5*: A character not in the basic literal character set can be
encoded with more than one code unit; the value of such a code unit can
be the same as that of a code unit for an element of the basic literal
character set. — *end note*\]

The character is encoded as the value `0`. No other element of the
translation character set is encoded with a code unit of value `0`. The
code unit value of each decimal digit character after the digit `0`
(`U+0030`) shall be one greater than the value of the previous. The
ordinary and wide literal encodings are otherwise
*implementation-defined*. For a UTF-8, UTF-16, or UTF-32 literal, the
Unicode scalar value corresponding to each character of the translation
character set is encoded as specified in the Unicode Standard for the
respective Unicode encoding form.

## Preprocessing tokens <a id="lex.pptoken">[[lex.pptoken]]</a>

``` bnf
preprocessing-token:
    header-name
    import-keyword
    module-keyword
    export-keyword
    identifier
    pp-number
    character-literal
    user-defined-character-literal
    string-literal
    user-defined-string-literal
    preprocessing-op-or-punc
    each non-whitespace character that cannot be one of the above
```

Each preprocessing token that is converted to a token [[lex.token]]
shall have the lexical form of a keyword, an identifier, a literal, or
an operator or punctuator.

A preprocessing token is the minimal lexical element of the language in
translation phases 3 through 6. In this document, glyphs are used to
identify elements of the basic character set [[lex.charset]]. The
categories of preprocessing token are: header names, placeholder tokens
produced by preprocessing `import` and `module` directives
(*import-keyword*, *module-keyword*, and *export-keyword*), identifiers,
preprocessing numbers, character literals (including user-defined
character literals), string literals (including user-defined string
literals), preprocessing operators and punctuators, and single
non-whitespace characters that do not lexically match the other
preprocessing token categories. If a or a character matches the last
category, the behavior is undefined. If any character not in the basic
character set matches the last category, the program is ill-formed.
Preprocessing tokens can be separated by whitespace; this consists of
comments [[lex.comment]], or whitespace characters (, , new-line, , and
), or both. As described in [[cpp]], in certain circumstances during
translation phase 4, whitespace (or the absence thereof) serves as more
than preprocessing token separation. Whitespace can appear within a
preprocessing token only as part of a header name or between the
quotation characters in a character literal or string literal.

If the input stream has been parsed into preprocessing tokens up to a
given character:

-  If the next character begins a sequence of characters that could be
  the prefix and initial double quote of a raw string literal, such as
  `R"`, the next preprocessing token shall be a raw string literal.
  Between the initial and final double quote characters of the raw
  string, any transformations performed in phase 2 (line splicing) are
  reverted; this reversion shall apply before any *d-char*, *r-char*, or
  delimiting parenthesis is identified. The raw string literal is
  defined as the shortest sequence of characters that matches the
  raw-string pattern

  ``` bnf
  encoding-prefix_opt 'R' raw-string
  ```

- Otherwise, if the next three characters are `<::` and the subsequent
  character is neither `:` nor `>`, the `<` is treated as a
  preprocessing token by itself and not as the first character of the
  alternative token `<:`.

- Otherwise, the next preprocessing token is the longest sequence of
  characters that could constitute a preprocessing token, even if that
  would cause further lexical analysis to fail, except that a
  *header-name* [[lex.header]] is only formed

  - after the `include` or `import` preprocessing token in an `#include`
    [[cpp.include]] or `import` [[cpp.import]] directive, or

  - within a *has-include-expression*.

\[*Example 1*:

``` cpp
#define R "x"
const char* s = R"y";           // ill-formed raw string, not "x" "y"
```

— *end example*\]

The *import-keyword* is produced by processing an `import` directive
[[cpp.import]], the *module-keyword* is produced by preprocessing a
`module` directive [[cpp.module]], and the *export-keyword* is produced
by preprocessing either of the previous two directives.

\[*Note 1*: None has any observable spelling. — *end note*\]

\[*Example 2*: The program fragment `0xe+foo` is parsed as a
preprocessing number token (one that is not a valid *integer-literal* or
*floating-point-literal* token), even though a parse as three
preprocessing tokens `0xe`, `+`, and `foo` can produce a valid
expression (for example, if `foo` is a macro defined as `1`). Similarly,
the program fragment `1E1` is parsed as a preprocessing number (one that
is a valid *floating-point-literal* token), whether or not `E` is a
macro name. — *end example*\]

\[*Example 3*: The program fragment `x+++++y` is parsed as `x
++ ++ + y`, which, if `x` and `y` have integral types, violates a
constraint on increment operators, even though the parse `x ++ + ++ y`
can yield a correct expression. — *end example*\]

## Alternative tokens <a id="lex.digraph">[[lex.digraph]]</a>

Alternative token representations are provided for some operators and
punctuators.

In all respects of the language, each alternative token behaves the
same, respectively, as its primary token, except for its spelling.

The set of alternative tokens is defined in [[lex.digraph]].

## Tokens <a id="lex.token">[[lex.token]]</a>

``` bnf
token:
    identifier
    keyword
    literal
    operator-or-punctuator
```

There are five kinds of tokens: identifiers, keywords, literals,

operators, and other separators. Blanks, horizontal and vertical tabs,
newlines, formfeeds, and comments (collectively, “whitespace”), as
described below, are ignored except as they serve to separate tokens.

\[*Note 1*: Some whitespace is required to separate otherwise adjacent
identifiers, keywords, numeric literals, and alternative tokens
containing alphabetic characters. — *end note*\]

## Comments <a id="lex.comment">[[lex.comment]]</a>

The characters `/*` start a comment, which terminates with the
characters `*/`. These comments do not nest. The characters `//` start a
comment, which terminates immediately before the next new-line
character. If there is a form-feed or a vertical-tab character in such a
comment, only whitespace characters shall appear between it and the
new-line that terminates the comment; no diagnostic is required.

\[*Note 1*: The comment characters `//`, `/*`, and `*/` have no special
meaning within a `//` comment and are treated just like other
characters. Similarly, the comment characters `//` and `/*` have no
special meaning within a `/*` comment. — *end note*\]

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
    any member of the translation character set except new-line and \unicode{003e{greater-than sign}}
```

``` bnf
q-char-sequence:
    q-char
    q-char-sequence q-char
```

``` bnf
q-char:
    any member of the translation character set except new-line and \unicode{0022{quotation mark}}
```

\[*Note 1*: Header name preprocessing tokens only appear within a
`#include` preprocessing directive, a `__has_include` preprocessing
expression, or after certain occurrences of an `import` token (see 
[[lex.pptoken]]). — *end note*\]

The sequences in both forms of *header-name* are mapped in an
*implementation-defined* manner to headers or to external source file
names as specified in  [[cpp.include]].

The appearance of either of the characters `'` or `\` or of either of
the character sequences `/*` or `//` in a *q-char-sequence* or an
*h-char-sequence* is conditionally-supported with
*implementation-defined* semantics, as is the appearance of the
character `"` in an *h-char-sequence*.

## Preprocessing numbers <a id="lex.ppnumber">[[lex.ppnumber]]</a>

``` bnf
pp-number:
    digit
    '.' digit
    pp-number identifier-continue
    pp-number ''' digit
    pp-number ''' nondigit
    pp-number 'e' sign
    pp-number 'E' sign
    pp-number 'p' sign
    pp-number 'P' sign
    pp-number '.'
```

Preprocessing number tokens lexically include all *integer-literal*
tokens [[lex.icon]] and all *floating-point-literal* tokens
[[lex.fcon]].

A preprocessing number does not have a type or a value; it acquires both
after a successful conversion to an *integer-literal* token or a
*floating-point-literal* token.

## Identifiers <a id="lex.name">[[lex.name]]</a>

``` bnf
identifier:
    identifier-start
    identifier identifier-continue
```

``` bnf
identifier-start:
    nondigit
    an element of the translation character set with the Unicode property XID_Start
```

``` bnf
identifier-continue:
    digit
    nondigit
    an element of the translation character set with the Unicode property XID_Continue
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

\[*Note 1*:

The character properties XID_Start and XID_Continue are Derived Core
Properties as described by of the Unicode Standard.

— *end note*\]

The program is ill-formed if an *identifier* does not conform to
Normalization Form C as specified in the Unicode Standard.

\[*Note 2*: Identifiers are case-sensitive. — *end note*\]

\[*Note 3*: In translation phase 4, *identifier* also includes those
*preprocessing-token*s [[lex.pptoken]] differentiated as keywords
[[lex.key]] in the later translation phase 7
[[lex.token]]. — *end note*\]

The identifiers in [[lex.name.special]] have a special meaning when
appearing in a certain context. When referred to in the grammar, these
identifiers are used explicitly rather than using the *identifier*
grammar production. Unless otherwise specified, any ambiguity as to
whether a given *identifier* has a special meaning is resolved to
interpret the token as a regular *identifier*.

In addition, some identifiers appearing as a *token* or
*preprocessing-token* are reserved for use by C++ implementations and
shall not be used otherwise; no diagnostic is required.

- Each identifier that contains a double underscore `\unun` or begins
  with an underscore followed by an uppercase letter is reserved to the
  implementation for any use.

- Each identifier that begins with an underscore is reserved to the
  implementation for use as a name in the global namespace.

## Keywords <a id="lex.key">[[lex.key]]</a>

``` bnf
keyword:
    any identifier listed in \tref{lex.key}
    *import-keyword*
    *module-keyword*
    *export-keyword*
```

The identifiers shown in [[lex.key]] are reserved for use as keywords
(that is, they are unconditionally treated as keywords in phase 7)
except in an *attribute-token* [[dcl.attr.grammar]].

\[*Note 1*: The `register` keyword is unused but is reserved for future
use. — *end note*\]

Furthermore, the alternative representations shown in
[[lex.key.digraph]] for certain operators and punctuators
[[lex.digraph]] are reserved and shall not be used otherwise.

**Table: Alternative representations**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| `and` | `and_eq` | `bitand` | `bitor` | `compl` | `not` |
| `not_eq` | `or` | `or_eq` | `xor` | `xor_eq` |

## Operators and punctuators <a id="lex.operators">[[lex.operators]]</a>

The lexical representation of C++ programs includes a number of
preprocessing tokens that are used in the syntax of the preprocessor or
are converted into tokens for operators and punctuators:

``` bnf
preprocessing-op-or-punc:
    preprocessing-operator
    operator-or-punctuator
```

``` bnf
%% Ed. note: character protrusion would misalign various operators.
preprocessing-operator: one of
    '#        ##       %:       %:%:'
```

``` bnf
operator-or-punctuator: one of
    '{        $'        [        ]        (        )}
    '<:       :>       <%       %>       ;        :        ...'
    '?        ::       .        .*       ->       ->*      \~'
    '!        +        -        *        /        %        \caret{'        \&        |}
    '=        +=       -=       *=       /=       %=       \caret{'=       \&=       |=}
    '==       !=       <        >        <=       >=       <=>      &&       ||'
    '<<       >>       <<=      >>=      ++       --       ,'
    '\texttt{and'      \texttt{or}       \texttt{xor}      \texttt{not}      \texttt{bitand}   \texttt{bitor}    \texttt{compl}}
    '\texttt{and_eq'   \texttt{or_eq}    \texttt{xor_eq}   \texttt{not_eq}}
```

Each *operator-or-punctuator* is converted to a single token in
translation phase 7 [[lex.phases]].

## Literals <a id="lex.literal">[[lex.literal]]</a>

### Kinds of literals <a id="lex.literal.kinds">[[lex.literal.kinds]]</a>

There are several kinds of literals.

``` bnf
literal:
    integer-literal
    character-literal
    floating-point-literal
    string-literal
    boolean-literal
    pointer-literal
    user-defined-literal
```

\[*Note 1*: When appearing as an *expression*, a literal has a type and
a value category [[expr.prim.literal]]. — *end note*\]

### Integer literals <a id="lex.icon">[[lex.icon]]</a>

``` bnf
integer-literal:
    binary-literal integer-suffix_opt
    octal-literal integer-suffix_opt
    decimal-literal integer-suffix_opt
    hexadecimal-literal integer-suffix_opt
```

``` bnf
binary-literal:
    '0b' binary-digit
    '0B' binary-digit
    binary-literal ''_opt' binary-digit
```

``` bnf
octal-literal:
    '0'
    octal-literal ''_opt' octal-digit
```

``` bnf
decimal-literal:
    nonzero-digit
    decimal-literal ''_opt' digit
```

``` bnf
hexadecimal-literal:
    hexadecimal-prefix hexadecimal-digit-sequence
```

``` bnf
binary-digit: one of
    '0  1'
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
    hexadecimal-digit-sequence ''_opt' hexadecimal-digit
```

``` bnf
hexadecimal-digit: one of
    '0  1  2  3  4  5  6  7  8  9'
    'a  b  c  d  e  f'
    'A  B  C  D  E  F'
```

``` bnf
integer-suffix:
    unsigned-suffix long-suffix_opt 
    unsigned-suffix long-long-suffix_opt 
    unsigned-suffix size-suffix_opt 
    long-suffix unsigned-suffix_opt 
    long-long-suffix unsigned-suffix_opt 
    size-suffix unsigned-suffix_opt
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

``` bnf
size-suffix: one of
   'z  Z'
```

In an *integer-literal*, the sequence of *binary-digit*s,
*octal-digit*s, *digit*s, or *hexadecimal-digit*s is interpreted as a
base N integer as shown in table [[lex.icon.base]]; the lexically first
digit of the sequence of digits is the most significant.

\[*Note 1*: The prefix and any optional separating single quotes are
ignored when determining the value. — *end note*\]

The *hexadecimal-digit*s `a` through `f` and `A` through `F` have
decimal values ten through fifteen.

\[*Example 1*: The number twelve can be written `12`, `014`, `0XC`, or
`0b1100`. The *integer-literal*s `1048576`, `1'048'576`, `0X100000`,
`0x10'0000`, and `0'004'000'000` all have the same
value. — *end example*\]

The type of an *integer-literal* is the first type in the list in
[[lex.icon.type]] corresponding to its optional *integer-suffix* in
which its value can be represented.

**Table: Types of *integer-literal*s**

|  |  |  |
| --- | --- | --- |
| none | `int` | `int` |
|  | `long int` | `unsigned int` |
|  | `long long int` | `long int` |
|  |  | `unsigned long int` |
|  |  | `long long int` |
|  |  | `unsigned long long int` |
| `u` or `U` | `unsigned int` | `unsigned int` |
|  | `unsigned long int` | `unsigned long int` |
|  | `unsigned long long int` | `unsigned long long int` |
| `l` or `L` | `long int` | `long int` |
|  | `long long int` | `unsigned long int` |
|  |  | `long long int` |
|  |  | `unsigned long long int` |
| Both `u` or `U` | `unsigned long int` | `unsigned long int` |
| and `l` or `L` | `unsigned long long int` | `unsigned long long int` |
| `ll` or `LL` | `long long int` | `long long int` |
|  |  | `unsigned long long int` |
| Both `u` or `U` | `unsigned long long int` | `unsigned long long int` |
| and `ll` or `LL` |  |
| `z` or `Z` | the signed integer type corresponding | the signed integer type |
|  | \qquad to `std::size_t` [[support.types.layout]] | \qquad corresponding to `std::size_t` |
|  |  | `std::size_t` |
| Both `u` or `U` | `std::size_t` | `std::size_t` |
| and `z` or `Z` |  |
If an *integer-literal* cannot be represented by any type in its list
and an extended integer type [[basic.fundamental]] can represent its
value, it may have that extended integer type. If all of the types in
the list for the *integer-literal* are signed, the extended integer type
shall be signed. If all of the types in the list for the
*integer-literal* are unsigned, the extended integer type shall be
unsigned. If the list contains both signed and unsigned types, the
extended integer type may be signed or unsigned. A program is ill-formed
if one of its translation units contains an *integer-literal* that
cannot be represented by any of the allowed types.

### Character literals <a id="lex.ccon">[[lex.ccon]]</a>

``` bnf
character-literal:
    encoding-prefix_opt ''' c-char-sequence '''
```

``` bnf
encoding-prefix: one of
    'u8'\quad'u'\quad'U'\quad'L'
```

``` bnf
c-char-sequence:
    c-char
    c-char-sequence c-char
```

``` bnf
c-char:
    basic-c-char
    escape-sequence
    universal-character-name
```

``` bnf
basic-c-char:
    any member of the translation character set except the \unicode{0027{apostrophe},}
      \unicode{005c{reverse solidus}, or new-line character}
```

``` bnf
escape-sequence:
    simple-escape-sequence
    numeric-escape-sequence
    conditional-escape-sequence
```

``` bnf
simple-escape-sequence:
    '$' simple-escape-sequence-char
```

``` bnf
simple-escape-sequence-char: one of
    ''  "  ?  \ a  b  f  n  r  t  v'
```

``` bnf
numeric-escape-sequence:
    octal-escape-sequence
    hexadecimal-escape-sequence
```

``` bnf
simple-octal-digit-sequence:
    octal-digit
    simple-octal-digit-sequence octal-digit
```

``` bnf
octal-escape-sequence:
    '$' octal-digit
    '$' octal-digit octal-digit
    '$' octal-digit octal-digit octal-digit
    '\ o{' simple-octal-digit-sequence '$'}
```

``` bnf
hexadecimal-escape-sequence:
    '\ x' simple-hexadecimal-digit-sequence
    '\ x{' simple-hexadecimal-digit-sequence '$'}
```

``` bnf
conditional-escape-sequence:
    '$' conditional-escape-sequence-char
```

``` bnf
conditional-escape-sequence-char:
    any member of the basic character set that is not an octal-digit, a simple-escape-sequence-char, or the characters 'N, \terminal{o', 'u', 'U', or 'x'}
```

A *non-encodable character literal* is a *character-literal* whose
*c-char-sequence* consists of a single *c-char* that is not a
*numeric-escape-sequence* and that specifies a character that either
lacks representation in the literal’s associated character encoding or
that cannot be encoded as a single code unit. A *multicharacter literal*
is a *character-literal* whose *c-char-sequence* consists of more than
one *c-char*. The *encoding-prefix* of a non-encodable character literal
or a multicharacter literal shall be absent. Such *character-literal*s
are conditionally-supported.

The kind of a *character-literal*, its type, and its associated
character encoding [[lex.charset]] are determined by its
*encoding-prefix* and its *c-char-sequence* as defined by
[[lex.ccon.literal]]. The special cases for non-encodable character
literals and multicharacter literals take precedence over the base kind.

\[*Note 1*: The associated character encoding for ordinary character
literals determines encodability, but does not determine the value of
non-encodable ordinary character literals or ordinary multicharacter
literals. The examples in [[lex.ccon.literal]] for non-encodable
ordinary character literals assume that the specified character lacks
representation in the ordinary literal encoding or that encoding the
character would require more than one code unit. — *end note*\]

**Table: Character literals**

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| none | \defnx{ordinary character literal}{literal!character!ordinary} | `char` | ordinary | `'v'` |
| `L` | \defnx{wide character literal}{literal!character!wide} | `wchar_t` | wide literal | `L'w'` |
|  |  |  | encoding |
| `u8` | \defnx{UTF-8 character literal}{literal!character!UTF-8} | `char8_t` | UTF-8 | `u8'x'` |
| `u` | \defnx{UTF-16 character literal}{literal!character!UTF-16} | `char16_t` | UTF-16 | `u'y'` |
| `U` | \defnx{UTF-32 character literal}{literal!character!UTF-32} | `char32_t` | UTF-32 | `U'z'` |
In translation phase 4, the value of a *character-literal* is determined
using the range of representable values of the *character-literal*’s
type in translation phase 7. A non-encodable character literal or a
multicharacter literal has an *implementation-defined* value. The value
of any other kind of *character-literal* is determined as follows:

- A *character-literal* with a *c-char-sequence* consisting of a single
  *basic-c-char*, *simple-escape-sequence*, or
  *universal-character-name* is the code unit value of the specified
  character as encoded in the literal’s associated character encoding.

  \[*Note 8*: If the specified character lacks representation in the
  literal’s associated character encoding or if it cannot be encoded as
  a single code unit, then the literal is a non-encodable character
  literal. — *end note*\]

- A *character-literal* with a *c-char-sequence* consisting of a single
  *numeric-escape-sequence* has a value as follows:

  - Let v be the integer value represented by the octal number
    comprising the sequence of *octal-digit* in an
    *octal-escape-sequence* or by the hexadecimal number comprising the
    sequence of *hexadecimal-digit* in a *hexadecimal-escape-sequence*.

  - If v does not exceed the range of representable values of the
    *character-literal*’s type, then the value is v.

  - Otherwise, if the *character-literal*’s *encoding-prefix* is absent
    or `L`, and v does not exceed the range of representable values of
    the corresponding unsigned type for the underlying type of the
    *character-literal*’s type, then the value is the unique value of
    the *character-literal*’s type `T` that is congruent to v modulo
    $2^N$, where N is the width of `T`.

  - Otherwise, the *character-literal* is ill-formed.

- A *character-literal* with a *c-char-sequence* consisting of a single
  *conditional-escape-sequence* is conditionally-supported and has an
  *implementation-defined* value.

The character specified by a *simple-escape-sequence* is specified in
[[lex.ccon.esc]].

\[*Note 2*: Using an escape sequence for a question mark is supported
for compatibility with ISO C++14 and ISO C. — *end note*\]

**Table: Simple escape sequences**

|  |  |  |
| --- | --- | --- |
| `U+000a` | \uname{line feed} | `\ n` |
| `U+0009` | \uname{character tabulation} | `\ t` |
| `U+000b` | \uname{line tabulation} | `\ v` |
| `U+0008` | \uname{backspace} | `\ b` |
| `U+000d` | \uname{carriage return} | `\ r` |
| `U+000c` | \uname{form feed} | `\ f` |
| `U+0007` | \uname{alert} | `\ a` |
| `U+005c` | \uname{reverse solidus} | `` |
| `U+003f` | \uname{question mark} | `\ ?` |
| `U+0027` | \uname{apostrophe} | `\ '` |
| `U+0022` | \uname{quotation mark} | `\ "` |

### Floating-point literals <a id="lex.fcon">[[lex.fcon]]</a>

``` bnf
floating-point-literal:
    decimal-floating-point-literal
    hexadecimal-floating-point-literal
```

``` bnf
decimal-floating-point-literal:
    fractional-constant exponent-part_opt floating-point-suffix_opt
    digit-sequence exponent-part floating-point-suffix_opt
```

``` bnf
hexadecimal-floating-point-literal:
    hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part floating-point-suffix_opt
    hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part floating-point-suffix_opt
```

``` bnf
fractional-constant:
    digit-sequence_opt '.' digit-sequence
    digit-sequence '.'
```

``` bnf
hexadecimal-fractional-constant:
    hexadecimal-digit-sequence_opt '.' hexadecimal-digit-sequence
    hexadecimal-digit-sequence '.'
```

``` bnf
exponent-part:
    'e' sign_opt digit-sequence
    'E' sign_opt digit-sequence
```

``` bnf
binary-exponent-part:
    'p' sign_opt digit-sequence
    'P' sign_opt digit-sequence
```

``` bnf
sign: one of
    '+  -'
```

``` bnf
digit-sequence:
    digit
    digit-sequence ''_opt' digit
```

``` bnf
floating-point-suffix: one of
    'f  l  f16  f32  f64  f128  bf16  F  L  F16  F32  F64  F128  BF16'
```

The type of a *floating-point-literal*
[[basic.fundamental]], [[basic.extended.fp]] is determined by its
*floating-point-suffix* as specified in [[lex.fcon.type]].

\[*Note 1*: The floating-point suffixes `f16`, `f32`, `f64`, `f128`,
`bf16`, `F16`, `F32`, `F64`, `F128`, and `BF16` are
conditionally-supported. See [[basic.extended.fp]]. — *end note*\]

The *significand* of a *floating-point-literal* is the
*fractional-constant* or *digit-sequence* of a
*decimal-floating-point-literal* or the
*hexadecimal-fractional-constant* or *hexadecimal-digit-sequence* of a
*hexadecimal-floating-point-literal*. In the significand, the sequence
of *digit*s or *hexadecimal-digit*s and optional period are interpreted
as a base N real number s, where N is 10 for a
*decimal-floating-point-literal* and 16 for a
*hexadecimal-floating-point-literal*.

\[*Note 2*: Any optional separating single quotes are ignored when
determining the value. — *end note*\]

If an *exponent-part* or *binary-exponent-part* is present, the exponent
e of the *floating-point-literal* is the result of interpreting the
sequence of an optional *sign* and the *digit*s as a base 10 integer.
Otherwise, the exponent e is 0. The scaled value of the literal is
$s \times 10^e$ for a *decimal-floating-point-literal* and
$s \times 2^e$ for a *hexadecimal-floating-point-literal*.

\[*Example 1*: The *floating-point-literal* `49.625` and `0xC.68p+2`
have the same value. The *floating-point-literal* `1.602'176'565e-19`
and `1.602176565e-19` have the same value. — *end example*\]

If the scaled value is not in the range of representable values for its
type, the program is ill-formed. Otherwise, the value of a
*floating-point-literal* is the scaled value if representable, else the
larger or smaller representable value nearest the scaled value, chosen
in an *implementation-defined* manner.

### String literals <a id="lex.string">[[lex.string]]</a>

``` bnf
string-literal:
    encoding-prefix_opt '"' s-char-sequence_opt '"'
    encoding-prefix_opt 'R' raw-string
```

``` bnf
s-char-sequence:
    s-char
    s-char-sequence s-char
```

``` bnf
s-char:
    basic-s-char
    escape-sequence
    universal-character-name
```

``` bnf
basic-s-char:
    any member of the translation character set except the \unicode{0022{quotation mark},}
      \unicode{005c{reverse solidus}, or new-line character}
```

``` bnf
raw-string:
    '"' d-char-sequence_opt '(' r-char-sequence_opt ')' d-char-sequence_opt '"'
```

``` bnf
r-char-sequence:
    r-char
    r-char-sequence r-char
```

``` bnf
r-char:
    any member of the translation character set, except a \unicode{0029{right parenthesis} followed by}
      the initial *d-char-sequence* (which may be empty) followed by a \unicode{0022{quotation mark}}
```

``` bnf
d-char-sequence:
    d-char
    d-char-sequence d-char
```

``` bnf
d-char:
    any member of the basic character set except:
      \unicode{0020{space}, ({left parenthesis}, ){right parenthesis}, \{reverse solidus},}
      \unicode{0009{character tabulation}, {line tabulation}, {form feed}, and new-line}
```

The kind of a *string-literal*, its type, and its associated character
encoding [[lex.charset]] are determined by its encoding prefix and
sequence of *s-char*s or *r-char*s as defined by [[lex.string.literal]]
where n is the number of encoded code units as described below.

**Table: String literals**

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| none | \defnx{ordinary string literal}{literal!string!ordinary} | array of $n$\newline `const char` | ordinary literal encoding | `"ordinary string"`\newline `R"(ordinary raw string)"` |
| `L` | \defnx{wide string literal}{literal!string!wide} | array of $n$\newline `const wchar_t` | wide literal\newline encoding | `L"wide string"`\newline `LR"w(wide raw string)w"` |
| `u8` | \defnx{UTF-8 string literal}{literal!string!UTF-8} | array of $n$\newline `const char8_t` | UTF-8 | `u8"UTF-8 string"`\newline `u8R"x(UTF-8 raw string)x"` |
| `u` | \defnx{UTF-16 string literal}{literal!string!UTF-16} | array of $n$\newline `const char16_t` | UTF-16 | `u"UTF-16 string"`\newline `uR"y(UTF-16 raw string)y"` |
| `U` | \defnx{UTF-32 string literal}{literal!string!UTF-32} | array of $n$\newline `const char32_t` | UTF-32 | `U"UTF-32 string"`\newline `UR"z(UTF-32 raw string)z"` |
A *string-literal* that has an `R` in the prefix is a
*raw string literal*. The *d-char-sequence* serves as a delimiter. The
terminating *d-char-sequence* of a *raw-string* is the same sequence of
characters as the initial *d-char-sequence*. A *d-char-sequence* shall
consist of at most 16 characters.

\[*Note 1*: The characters `'('` and `')'` are permitted in a
*raw-string*. Thus, `R"delimiter((a|b))delimiter"` is equivalent to
`"(a|b)"`. — *end note*\]

\[*Note 2*:

A source-file new-line in a raw string literal results in a new-line in
the resulting execution string literal. Assuming no whitespace at the
beginning of lines in the following example, the assert will succeed:

``` cpp
const char* p = R"(a\
b
c)";
assert(std::strcmp(p, "a\\\nb\nc") == 0);
```

— *end note*\]

\[*Example 1*:

The raw string

``` cpp
R"a(
)\
a"
)a"
```

is equivalent to `"\ n)\ \ \ na\"\ n"`. The raw string

``` cpp
R"(x = "\"y\"")"
```

is equivalent to `"x = \ "\\\ "y\\\ "\ ""`.

— *end example*\]

Ordinary string literals and UTF-8 string literals are also referred to
as narrow string literals.

The common *encoding-prefix* for a sequence of adjacent
*string-literal*s is determined pairwise as follows: If two
*string-literal* have the same *encoding-prefix*, the common
*encoding-prefix* is that *encoding-prefix*. If one *string-literal* has
no *encoding-prefix*, the common *encoding-prefix* is that of the other
*string-literal*. Any other combinations are ill-formed.

\[*Note 3*: A *string-literal*’s rawness has no effect on the
determination of the common *encoding-prefix*. — *end note*\]

In translation phase 6 [[lex.phases]], adjacent *string-literal*s are
concatenated. The lexical structure and grouping of the contents of the
individual *string-literal*s is retained.

\[*Example 2*:

``` cpp
"\xA" "B"
```

represents the code unit `'\ xA'` and the character `'B'` after
concatenation (and not the single code unit `'\ xAB'`). Similarly,

``` cpp
R"(\u00)" "41"
```

represents six characters, starting with a backslash and ending with the
digit `1` (and not the single character `'A'` specified by a
*universal-character-name*).

[[lex.string.concat]] has some examples of valid concatenations.

— *end example*\]

**Table: String literal concatenations**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| \multicolumn{2}{|c}{Source} | Means | \multicolumn{2}{c}{Source} | Means | \multicolumn{2}{c}{Source} | Means |
| `u"a"` | `u"b"` | `u"ab"` | `U"a"` | `U"b"` | `U"ab"` | `L"a"` | `L"b"` | `L"ab"` |
| `u"a"` | `"b"` | `u"ab"` | `U"a"` | `"b"` | `U"ab"` | `L"a"` | `"b"` | `L"ab"` |
| `"a"` | `u"b"` | `u"ab"` | `"a"` | `U"b"` | `U"ab"` | `"a"` | `L"b"` | `L"ab"` |
Evaluating a *string-literal* results in a string literal object with
static storage duration [[basic.stc]]. Whether all *string-literal*s are
distinct (that is, are stored in nonoverlapping objects) and whether
successive evaluations of a *string-literal* yield the same or a
different object is unspecified.

\[*Note 4*:  The effect of attempting to modify a string literal object
is undefined. — *end note*\]

String literal objects are initialized with the sequence of code unit
values corresponding to the *string-literal*’s sequence of *s-char*s
(originally from non-raw string literals) and *r-char*s (originally from
raw string literals), plus a terminating character, in order as follows:

- The sequence of characters denoted by each contiguous sequence of
  *basic-s-char*s, *r-char*s, *simple-escape-sequence*s [[lex.ccon]],
  and *universal-character-name*s [[lex.charset]] is encoded to a code
  unit sequence using the *string-literal*’s associated character
  encoding. If a character lacks representation in the associated
  character encoding, then the *string-literal* is
  conditionally-supported and an *implementation-defined* code unit
  sequence is encoded.

  \[*Note 9*: No character lacks representation in any Unicode encoding
  form. — *end note*\]

  When encoding a stateful character encoding, implementations should
  encode the first such sequence beginning with the initial encoding
  state and encode subsequent sequences beginning with the final
  encoding state of the prior sequence.

  \[*Note 10*: The encoded code unit sequence can differ from the
  sequence of code units that would be obtained by encoding each
  character independently. — *end note*\]

- Each *numeric-escape-sequence* [[lex.ccon]] contributes a single code
  unit with a value as follows:

  - Let v be the integer value represented by the octal number
    comprising the sequence of *octal-digit* in an
    *octal-escape-sequence* or by the hexadecimal number comprising the
    sequence of *hexadecimal-digit* in a *hexadecimal-escape-sequence*.

  - If v does not exceed the range of representable values of the
    *string-literal*’s array element type, then the value is v.

  - Otherwise, if the *string-literal*’s *encoding-prefix* is absent or
    `L`, and v does not exceed the range of representable values of the
    corresponding unsigned type for the underlying type of the
    *string-literal*’s array element type, then the value is the unique
    value of the *string-literal*’s array element type `T` that is
    congruent to v modulo $2^N$, where N is the width of `T`.

  - Otherwise, the *string-literal* is ill-formed.

  When encoding a stateful character encoding, these sequences should
  have no effect on encoding state.

- Each *conditional-escape-sequence* [[lex.ccon]] contributes an
  *implementation-defined* code unit sequence. When encoding a stateful
  character encoding, it is *implementation-defined* what effect these
  sequences have on encoding state.

### Boolean literals <a id="lex.bool">[[lex.bool]]</a>

``` bnf
boolean-literal:
    'false'
    'true'
```

The Boolean literals are the keywords `false` and `true`. Such literals
have type `bool`.

### Pointer literals <a id="lex.nullptr">[[lex.nullptr]]</a>

``` bnf
pointer-literal:
    'nullptr'
```

The pointer literal is the keyword `nullptr`. It has type
`std::nullptr_t`.

\[*Note 1*: `std::nullptr_t` is a distinct type that is neither a
pointer type nor a pointer-to-member type; rather, a prvalue of this
type is a null pointer constant and can be converted to a null pointer
value or null member pointer value. See  [[conv.ptr]] and 
[[conv.mem]]. — *end note*\]

### User-defined literals <a id="lex.ext">[[lex.ext]]</a>

``` bnf
user-defined-literal:
    user-defined-integer-literal
    user-defined-floating-point-literal
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
user-defined-floating-point-literal:
    fractional-constant exponent-part_opt ud-suffix
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

\[*Example 1*:

`123_km`

is a *user-defined-literal*, but `12LL` is an *integer-literal*.

— *end example*\]

The syntactic non-terminal preceding the *ud-suffix* in a
*user-defined-literal* is taken to be the longest sequence of characters
that could match that non-terminal.

A *user-defined-literal* is treated as a call to a literal operator or
literal operator template [[over.literal]]. To determine the form of
this call for a given *user-defined-literal* *L* with *ud-suffix* *X*,
first let *S* be the set of declarations found by unqualified lookup for
the *literal-operator-id* whose literal suffix identifier is *X*
[[basic.lookup.unqual]]. *S* shall not be empty.

If *L* is a *user-defined-integer-literal*, let *n* be the literal
without its *ud-suffix*. If *S* contains a literal operator with
parameter type `unsigned long long`, the literal *L* is treated as a
call of the form

``` cpp
operator ""X(nULL)
```

Otherwise, *S* shall contain a raw literal operator or a numeric literal
operator template [[over.literal]] but not both. If *S* contains a raw
literal operator, the literal *L* is treated as a call of the form

``` cpp
operator ""X("n")
```

Otherwise (*S* contains a numeric literal operator template), *L* is
treated as a call of the form

``` cpp
operator ""X<'$c_1$', '$c_2$', ... '$c_k$'>()
```

where *n* is the source character sequence c₁c₂...cₖ.

\[*Note 1*: The sequence c₁c₂...cₖ can only contain characters from the
basic character set. — *end note*\]

If *L* is a *user-defined-floating-point-literal*, let *f* be the
literal without its *ud-suffix*. If *S* contains a literal operator with
parameter type `long double`, the literal *L* is treated as a call of
the form

``` cpp
operator ""X(fL)
```

Otherwise, *S* shall contain a raw literal operator or a numeric literal
operator template [[over.literal]] but not both. If *S* contains a raw
literal operator, the *literal* *L* is treated as a call of the form

``` cpp
operator ""X("f")
```

Otherwise (*S* contains a numeric literal operator template), *L* is
treated as a call of the form

``` cpp
operator ""X<'$c_1$', '$c_2$', ... '$c_k$'>()
```

where *f* is the source character sequence c₁c₂...cₖ.

\[*Note 2*: The sequence c₁c₂...cₖ can only contain characters from the
basic character set. — *end note*\]

If *L* is a *user-defined-string-literal*, let *str* be the literal
without its *ud-suffix* and let *len* be the number of code units in
*str* (i.e., its length excluding the terminating null character). If
*S* contains a literal operator template with a non-type template
parameter for which *str* is a well-formed *template-argument*, the
literal *L* is treated as a call of the form

``` cpp
operator ""X<str{}>()
```

Otherwise, the literal *L* is treated as a call of the form

``` cpp
operator ""X(str{}, len{})
```

If *L* is a *user-defined-character-literal*, let *ch* be the literal
without its *ud-suffix*. *S* shall contain a literal operator
[[over.literal]] whose only parameter has the type of *ch* and the
literal *L* is treated as a call of the form

``` cpp
operator ""X(ch{})
```

\[*Example 2*:

``` cpp
long double operator ""_w(long double);
std::string operator ""_w(const char16_t*, std::size_t);
unsigned operator ""_w(const char*);
int main() {
  1.2_w;            // calls operator ""_w(1.2L)
  u"one"_w;         // calls operator ""_w(u"one", 3)
  12_w;             // calls operator ""_w("12")
  "two"_w;          // error: no applicable literal operator
}
```

— *end example*\]

In translation phase 6 [[lex.phases]], adjacent *string-literal*s are
concatenated and *user-defined-string-literal* are considered
*string-literal*s for that purpose. During concatenation, *ud-suffix*
are removed and ignored and the concatenation process occurs as
described in  [[lex.string]]. At the end of phase 6, if a
*string-literal* is the result of a concatenation involving at least one
*user-defined-string-literal*, all the participating
*user-defined-string-literal* shall have the same *ud-suffix* and that
suffix is applied to the result of the concatenation.

\[*Example 3*:

``` cpp
int main() {
  L"A" "B" "C"_x;   // OK, same as L"ABC"_x
  "P"_x "Q" "R"_y;  // error: two different ud-suffix{es}
}
```

— *end example*\]

<!-- Section link definitions -->
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

<!-- Link reference definitions -->
[basic.extended.fp]: basic.md#basic.extended.fp
[basic.fundamental]: basic.md#basic.fundamental
[basic.link]: basic.md#basic.link
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.stc]: basic.md#basic.stc
[character.seq]: library.md#character.seq
[conv.mem]: expr.md#conv.mem
[conv.ptr]: expr.md#conv.ptr
[cpp]: cpp.md#cpp
[cpp.cond]: cpp.md#cpp.cond
[cpp.import]: cpp.md#cpp.import
[cpp.include]: cpp.md#cpp.include
[cpp.module]: cpp.md#cpp.module
[cpp.stringize]: cpp.md#cpp.stringize
[dcl.attr.grammar]: dcl.md#dcl.attr.grammar
[expr.prim.literal]: expr.md#expr.prim.literal
[headers]: library.md#headers
[lex.ccon]: #lex.ccon
[lex.ccon.esc]: #lex.ccon.esc
[lex.ccon.literal]: #lex.ccon.literal
[lex.charset]: #lex.charset
[lex.charset.basic]: #lex.charset.basic
[lex.charset.literal]: #lex.charset.literal
[lex.comment]: #lex.comment
[lex.digraph]: #lex.digraph
[lex.fcon]: #lex.fcon
[lex.fcon.type]: #lex.fcon.type
[lex.header]: #lex.header
[lex.icon]: #lex.icon
[lex.icon.base]: #lex.icon.base
[lex.icon.type]: #lex.icon.type
[lex.key]: #lex.key
[lex.key.digraph]: #lex.key.digraph
[lex.name.special]: #lex.name.special
[lex.phases]: #lex.phases
[lex.pptoken]: #lex.pptoken
[lex.string]: #lex.string
[lex.string.concat]: #lex.string.concat
[lex.string.literal]: #lex.string.literal
[lex.token]: #lex.token
[module.import]: module.md#module.import
[module.unit]: module.md#module.unit
[over.literal]: over.md#over.literal
[support.types.layout]: support.md#support.types.layout
[temp.explicit]: temp.md#temp.explicit
[temp.names]: temp.md#temp.names
