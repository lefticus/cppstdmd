# Lexical conventions <a id="lex">[[lex]]</a>

## Separate translation <a id="lex.separate">[[lex.separate]]</a>

The text of the program is kept in units called *source files* in this
document. A source file together with all the headers [[headers]] and
source files included [[cpp.include]] via the preprocessing directive
`#include`, less any source lines skipped by any of the conditional
inclusion [[cpp.cond]] preprocessing directives, as modified by the
implementation-defined behavior of any
conditionally-supported-directives [[cpp.pre]] and pragmas
[[cpp.pragma]], if any, is called a *preprocessing translation unit*.

[*Note 1*: A C++ program need not all be translated at the same time.
Translation units can be separately translated and then later linked to
produce an executable program [[basic.link]]. — *end note*]

## Phases of translation <a id="lex.phases">[[lex.phases]]</a>

The precedence among the syntax rules of translation is specified by the
following phases.[^1]

1.  An implementation shall support input files that are a sequence of
    UTF-8 code units (UTF-8 files). It may also support an
    *implementation-defined* set of other kinds of input files, and, if
    so, the kind of an input file is determined in an
    *implementation-defined* manner that includes a means of designating
    input files as UTF-8 files, independent of their content.
    \[*Note 1*: In other words, recognizing the U+feff (byte order mark)
    is not sufficient. — *end note*] If an input file is determined to
    be a UTF-8 file, then it shall be a well-formed UTF-8 code unit
    sequence and it is decoded to produce a sequence of Unicode[^2]
    scalar values. A sequence of translation character set elements
    [[lex.charset]] is then formed by mapping each Unicode scalar value
    to the corresponding translation character set element. In the
    resulting sequence, each pair of characters in the input sequence
    consisting of U+000d (carriage return) followed by
    U+000a (line feed), as well as each U+000d (carriage return) not
    immediately followed by a U+000a (line feed), is replaced by a
    single new-line character. For any other kind of input file
    supported by the implementation, characters are mapped, in an
    *implementation-defined* manner, to a sequence of translation
    character set elements, representing end-of-line indicators as
    new-line characters.
2.  If the first translation character is U+feff (byte order mark), it
    is deleted. Each sequence comprising a backslash character (\\
    immediately followed by zero or more whitespace characters other
    than new-line followed by a new-line character is deleted, splicing
    physical source lines to form *logical source lines*. Only the last
    backslash on any physical source line shall be eligible for being
    part of such a splice. \[*Note 2*: Line splicing can form a
    *universal-character-name* [[lex.charset]]. — *end note*] A source
    file that is not empty and that (after splicing) does not end in a
    new-line character shall be processed as if an additional new-line
    character were appended to the file.
3.  The source file is decomposed into preprocessing tokens
    [[lex.pptoken]] and sequences of whitespace characters (including
    comments). A source file shall not end in a partial preprocessing
    token or in a partial comment.[^3] Each comment [[lex.comment]] is
    replaced by one U+0020 (space) character. New-line characters are
    retained. Whether each nonempty sequence of whitespace characters
    other than new-line is retained or replaced by one U+0020 (space)
    character is unspecified. As characters from the source file are
    consumed to form the next preprocessing token (i.e., not being
    consumed as part of a comment or other forms of whitespace), except
    when matching a *c-char-sequence*, *s-char-sequence*,
    *r-char-sequence*, *h-char-sequence*, or *q-char-sequence*,
    *universal-character-name*s are recognized [[lex.universal.char]]
    and replaced by the designated element of the translation character
    set [[lex.charset]]. The process of dividing a source file’s
    characters into preprocessing tokens is context-dependent.
    \[*Example 1*: See the handling of `<` within a `#include`
    preprocessing directive
    [[lex.header]], [[cpp.include]]. — *end example*]
4.  The source file is analyzed as a *preprocessing-file* [[cpp.pre]].
    Preprocessing directives [[cpp]] are executed, macro invocations are
    expanded [[cpp.replace]], and `_Pragma` unary operator expressions
    are executed [[cpp.pragma.op]]. A `#include` preprocessing directive
    [[cpp.include]] causes the named header or source file to be
    processed from phase 1 through phase 4, recursively. All
    preprocessing directives are then deleted. Whitespace characters
    separating preprocessing tokens are no longer significant.
5.  For a sequence of two or more adjacent *string-literal*
    preprocessing tokens, a common *encoding-prefix* is determined as
    specified in [[lex.string]]. Each such *string-literal*
    preprocessing token is then considered to have that common
    *encoding-prefix*.
6.  Adjacent *string-literal* preprocessing tokens are concatenated
    [[lex.string]].
7.  Each preprocessing token is converted into a token [[lex.token]].
    The resulting tokens constitute a *translation unit* and are
    syntactically and semantically analyzed as a *translation-unit*
    [[basic.link]] and translated.
    \[*Note 3*: The process of analyzing and translating the tokens can
    occasionally result in one token being replaced by a sequence of
    other tokens [[temp.names]]. — *end note*]
    It is *implementation-defined* whether the sources for module units
    and header units on which the current translation unit has an
    interface dependency [[module.unit]], [[module.import]] are required
    to be available.
    \[*Note 4*: Source files, translation units and translated
    translation units need not necessarily be stored as files, nor need
    there be any one-to-one correspondence between these entities and
    any external representation. The description is conceptual only, and
    does not specify any particular implementation. — *end note*]
    \[*Note 5*: Previously translated translation units can be preserved
    individually or in libraries. The separate translation units of a
    program communicate [[basic.link]] by (for example) calls to
    functions whose names have external or module linkage, manipulation
    of variables whose names have external or module linkage, or
    manipulation of data files. — *end note*]
    While the tokens constituting translation units are being analyzed
    and translated, required instantiations are performed.
    \[*Note 6*: This can include instantiations which have been
    explicitly requested [[temp.explicit]]. — *end note*]
    The contexts from which instantiations may be performed are
    determined by their respective points of instantiation
    [[temp.point]].
    \[*Note 7*: Other requirements in this document can further
    constrain the context from which an instantiation can be performed.
    For example, a constexpr function template specialization might have
    a point of instantiation at the end of a translation unit, but its
    use in certain constant expressions could require that it be
    instantiated at an earlier point [[temp.inst]]. — *end note*]
    Each instantiation results in new program constructs. The program is
    ill-formed if any instantiation fails.
    During the analysis and translation of tokens, certain expressions
    are evaluated [[expr.const]]. Constructs appearing at a program
    point P are analyzed in a context where each side effect of
    evaluating an expression E as a full-expression is complete if and
    only if
    - E is the expression corresponding to a
      *consteval-block-declaration* [[dcl.pre]], and
    - either that *consteval-block-declaration* or the template
      definition from which it is instantiated is reachable from
      [[module.reach]]
      - P, or
      - the point immediately following the *class-specifier* of the
        outermost class for which P is in a complete-class context
        [[class.mem.general]].

    \[*Example 2*:
    ``` cpp
    class S {
      class Incomplete;

      class Inner {
        void fn() {
          /* p₁ */ Incomplete i;    // OK
        }
      }; /* p₂ */

      consteval {
        define_aggregate(^^Incomplete, {});
      }
    }; /* p₃ */
    ```

    Constructs at p₁ are analyzed in a context where the side effect of
    the call to `define_aggregate` is evaluated because
    - E is the expression corresponding to a consteval block, and
    - p₁ is in a complete-class context of `S` and the consteval block
      is reachable from p₃.

    — *end example*]
8.  Translated translation units are combined, and all external entity
    references are resolved. Library components are linked to satisfy
    external references to entities not defined in the current
    translation. All such translator output is collected into a program
    image which contains information needed for execution in its
    execution environment.

## Characters <a id="lex.char">[[lex.char]]</a>

### Character sets <a id="lex.charset">[[lex.charset]]</a>

The *translation character set* consists of the following elements:

- each abstract character assigned a code point in the Unicode codespace
  as specified in the Unicode Standard, and
- a distinct character for each Unicode scalar value not assigned to an
  abstract character.

[*Note 1*: Unicode code points are integers in the range [0, 10FFFF]
(hexadecimal). A surrogate code point is a value in the range
[D800, DFFF] (hexadecimal). A Unicode scalar value is any code point
that is not a surrogate code point. — *end note*]

The *basic character set* is a subset of the translation character set,
consisting of 99 characters as specified in [[lex.charset.basic]].

[*Note 2*: Unicode short names are given only as a means to identifying
the character; the numerical value has no other meaning in this
context. — *end note*]

**Table: Basic character set** <a id="lex.charset.basic">[lex.charset.basic]</a>

| character            |                             | glyph                       |
| -------------------- | --------------------------- | --------------------------- |
| `U+0009`             | character tabulation        |                             |
| `U+000b`             | line tabulation             |                             |
| `U+000c`             | form feed                   |                             |
| `U+0020`             | space                       |                             |
| `U+000a`             | line feed                   | new-line                    |
| `U+0021`             | exclamation mark            | `!`                         |
| `U+0022`             | quotation mark              | `"`                         |
| `U+0023`             | number sign                 | `#`                         |
| `U+0024`             | dollar sign                 | `$`                         |
| `U+0025`             | percent sign                | `%`                         |
| `U+0026`             | ampersand                   | `&`                         |
| `U+0027`             | apostrophe                  | `'`                         |
| `U+0028`             | left parenthesis            | `(`                         |
| `U+0029`             | right parenthesis           | `)`                         |
| `U+002a`             | asterisk                    | `*`                         |
| `U+002b`             | plus sign                   | `+`                         |
| `U+002c`             | comma                       | `,`                         |
| `U+002d`             | hyphen-minus                | `-`                         |
| `U+002e`             | full stop                   | `.`                         |
| `U+002f`             | solidus                     | `/`                         |
| `U+0030` .. `U+0039` | digit zero .. nine          | `0 1 2 3 4 5 6 7 8 9`       |
| `U+003a`             | colon                       | `:`                         |
| `U+003b`             | semicolon                   | `;`                         |
| `U+003c`             | less-than sign              | `<`                         |
| `U+003d`             | equals sign                 | `=`                         |
| `U+003e`             | greater-than sign           | `>`                         |
| `U+003f`             | question mark               | `?`                         |
| }                    |
| `U+0041` .. `U+005a` | latin capital letter a .. z | `A B C D E F G H I J K L M` |
|                      |                             | `N O P Q R S T U V W X Y Z` |
| `U+005b`             | left square bracket         | `[`                         |
| `U+005c`             | reverse solidus             | \texttt{\}                  |
| `U+005d`             | right square bracket        | `]`                         |
| `U+005e`             | circumflex accent           | `^`                         |
| `U+005f`             | low line                    | `_`                         |
| `U+0060`             | grave accent                | `\`                         |
| `U+0061` .. `U+007a` | latin small letter a .. z   | `a b c d e f g h i j k l m` |
|                      |                             | `n o p q r s t u v w x y z` |
| `U+007b`             | left curly bracket          | \texttt{\                   |
| `U+007c`             | vertical line               | `|`                         |
| `U+007d`             | right curly bracket         | `}`                         |
| `U+007e`             | tilde                       | `~`                         |


The *basic literal character set* consists of all characters of the
basic character set, plus the control characters specified in
[[lex.charset.literal]].

**Table: Additional control characters in the basic literal character set** <a id="lex.charset.literal">[lex.charset.literal]</a>

|          |                 |
| -------- | --------------- |
| `U+0000` | null            |
| `U+0007` | alert           |
| `U+0008` | backspace       |
| `U+000d` | carriage return |


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

[*Note 3*: A character not in the basic literal character set can be
encoded with more than one code unit; the value of such a code unit can
be the same as that of a code unit for an element of the basic literal
character set. — *end note*]

The U+0000 (null) character is encoded as the value `0`. No other
element of the translation character set is encoded with a code unit of
value `0`. The code unit value of each decimal digit character after the
digit `0` (`U+0030`) shall be one greater than the value of the
previous. The ordinary and wide literal encodings are otherwise
*implementation-defined*. For a UTF-8, UTF-16, or UTF-32 literal, the
implementation shall encode the Unicode scalar value corresponding to
each character of the translation character set as specified in the
Unicode Standard for the respective Unicode encoding form.

### Universal character names <a id="lex.universal.char">[[lex.universal.char]]</a>

``` bnf
n-char:
     any member of the translation character set except the U+007d (right curly bracket) or new-line character
```

``` bnf
n-char-sequence:
    n-char n-char-sequenceₒₚₜ
```

``` bnf
named-universal-character:
    '\N{' n-char-sequence '}'
```

``` bnf
hex-quad:
    hexadecimal-digit hexadecimal-digit hexadecimal-digit hexadecimal-digit
```

``` bnf
simple-hexadecimal-digit-sequence:
    hexadecimal-digit simple-hexadecimal-digit-sequenceₒₚₜ
```

``` bnf
universal-character-name:
    '\u' hex-quad
    '\U' hex-quad hex-quad
    '\u{' simple-hexadecimal-digit-sequence '}'
    named-universal-character
```

The *universal-character-name* construct provides a way to name any
element in the translation character set using just the basic character
set. If a *universal-character-name* outside the *c-char-sequence*,
*s-char-sequence*, or *r-char-sequence* of a *character-literal* or
*string-literal* (in either case, including within a
*user-defined-literal*) corresponds to a control character or to a
character in the basic character set, the program is ill-formed.

[*Note 1*: A sequence of characters resembling a
*universal-character-name* in an *r-char-sequence* [[lex.string]] does
not form a *universal-character-name*. — *end note*]

A *universal-character-name* of the form `\u` *hex-quad*, `\U`
*hex-quad* *hex-quad*, or `\u{simple-hexadecimal-digit-sequence}`
designates the character in the translation character set whose Unicode
scalar value is the hexadecimal number represented by the sequence of
*hexadecimal-digit*s in the *universal-character-name*. The program is
ill-formed if that number is not a Unicode scalar value.

A *universal-character-name* that is a *named-universal-character*
designates the corresponding character in the Unicode Standard (chapter
4.8 Name) if the *n-char-sequence* is equal to its character name or to
one of its character name aliases of type “control”, “correction”, or
“alternate”; otherwise, the program is ill-formed.

[*Note 2*: These aliases are listed in the Unicode Character Database’s
`NameAliases.txt`. None of these names or aliases have leading or
trailing spaces. — *end note*]

## Comments <a id="lex.comment">[[lex.comment]]</a>

The characters `/*` start a comment, which terminates with the
characters `*/`. These comments do not nest. The characters `//` start a
comment, which terminates immediately before the next new-line
character.

[*Note 1*: The comment characters `//`, `/*`, and `*/` have no special
meaning within a `//` comment and are treated just like other
characters. Similarly, the comment characters `//` and `/*` have no
special meaning within a `/*` comment. — *end note*]

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
preprocessing token categories. If a U+0027 (apostrophe), a
U+0022 (quotation mark), or any character not in the basic character set
matches the last category, the program is ill-formed. Preprocessing
tokens can be separated by whitespace; this consists of comments
[[lex.comment]], or whitespace characters (U+0020 (space),
U+0009 (character tabulation), new-line, U+000b (line tabulation), and
U+000c (form feed)), or both. As described in [[cpp]], in certain
circumstances during translation phase 4, whitespace (or the absence
thereof) serves as more than preprocessing token separation. Whitespace
can appear within a preprocessing token only as part of a header name or
between the quotation characters in a character literal or string
literal.

Each preprocessing token that is converted to a token [[lex.token]]
shall have the lexical form of a keyword, an identifier, a literal, or
an operator or punctuator.

The *import-keyword* is produced by processing an `import` directive
[[cpp.import]], the *module-keyword* is produced by preprocessing a
`module` directive [[cpp.module]], and the *export-keyword* is produced
by preprocessing either of the previous two directives.

[*Note 1*: None has any observable spelling. — *end note*]

If the input stream has been parsed into preprocessing tokens up to a
given character:

- If the next character begins a sequence of characters that could be
  the prefix and initial double quote of a raw string literal, such as
  `R"`, the next preprocessing token shall be a raw string literal.
  Between the initial and final double quote characters of the raw
  string, any transformations performed in phase 2 (line splicing) are
  reverted; this reversion shall apply before any *d-char*, *r-char*, or
  delimiting parenthesis is identified. The raw string literal is
  defined as the shortest sequence of characters that matches the
  raw-string pattern
  ``` bnf
  encoding-prefixₒₚₜ 'R' raw-string
  ```
- Otherwise, if the next three characters are `<::` and the subsequent
  character is neither `:` nor `>`, the `<` is treated as a
  preprocessing token by itself and not as the first character of the
  alternative token `<:`.
- Otherwise, if the next three characters are `[::` and the subsequent
  character is not `:`, or if the next three characters are `[:>`, the
  `[` is treated as a preprocessing token by itself and not as the first
  character of the preprocessing token `[:`. \[*Note 2*: The tokens `[:`
  and `:]` cannot be composed from digraphs. — *end note*]
- Otherwise, the next preprocessing token is the longest sequence of
  characters that could constitute a preprocessing token, even if that
  would cause further lexical analysis to fail, except that
  - a *string-literal* token is never formed when a *header-name* token
    can be formed, and
  - a *header-name* [[lex.header]] is only formed
    - immediately after the `include`, `embed`, or `import`
      preprocessing token in a `#include` [[cpp.include]], `#embed`
      [[cpp.embed]], or `import` [[cpp.import]] directive, respectively,
      or
    - immediately after a preprocessing token sequence of
      `__has_include` or `__has_embed` immediately followed by `(` in a
      `#if`, `#elif`, or `#embed` directive [[cpp.cond]], [[cpp.embed]].

[*Example 1*:

``` cpp
#define R "x"
const char* s = R"y";           // ill-formed raw string, not "x" "y"
```

— *end example*]

[*Example 2*: The program fragment `0xe+foo` is parsed as a
preprocessing number token (one that is not a valid *integer-literal* or
*floating-point-literal* token), even though a parse as three
preprocessing tokens `0xe`, `+`, and `foo` can produce a valid
expression (for example, if `foo` is a macro defined as `1`). Similarly,
the program fragment `1E1` is parsed as a preprocessing number (one that
is a valid *floating-point-literal* token), whether or not `E` is a
macro name. — *end example*]

[*Example 3*: The program fragment `x+++++y` is parsed as `x
++ ++ + y`, which, if `x` and `y` have integral types, violates a
constraint on increment operators, even though the parse `x ++ + ++ y`
can yield a correct expression. — *end example*]

## Header names <a id="lex.header">[[lex.header]]</a>

``` bnf
header-name:
    '<' h-char-sequence '>'
    '"' q-char-sequence '"'
```

``` bnf
h-char-sequence:
    h-char h-char-sequenceₒₚₜ
```

``` bnf
h-char:
    any member of the translation character set except new-line and U+003e (greater-than sign)
```

``` bnf
q-char-sequence:
    q-char q-char-sequenceₒₚₜ
```

``` bnf
q-char:
    any member of the translation character set except new-line and U+0022 (quotation mark)
```

The sequences in both forms of *header-name*s are mapped in an
*implementation-defined* manner to headers or to external source file
names as specified in  [[cpp.include]].

[*Note 1*: Header name preprocessing tokens appear only within a
`#include` preprocessing directive, a `__has_include` preprocessing
expression, or after certain occurrences of an `import` token (see 
[[lex.pptoken]]). — *end note*]

The appearance of either of the characters `'` or `\` or of either of
the character sequences `/*` or `//` in a *q-char-sequence* or an
*h-char-sequence* is conditionally-supported with
*implementation-defined* semantics, as is the appearance of the
character `"` in an *h-char-sequence*.

[*Note 2*: Thus, a sequence of characters that resembles an escape
sequence can result in an error, be interpreted as the character
corresponding to the escape sequence, or have a completely different
meaning, depending on the implementation. — *end note*]

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
    '# ## %: %:%:'
```

``` bnf
operator-or-punctuator: one of
    '{ } [ ] ( ) [: :]'
    '<% %> <: :> ; : ...'
    '? :: . .* -> ->* ^^ ~'
    '! + - * / % ^ & |'
    '= += -= *= /= %= ^= &= |='
    '== != < > <= >= <=> && ||'
    '<< >> <<= >>= ++ -- ,'
    'and or xor not bitand bitor compl'
    'and_eq or_eq xor_eq not_eq'
```

Each *operator-or-punctuator* is converted to a single token in
translation phase 7 [[lex.phases]].

## Alternative tokens <a id="lex.digraph">[[lex.digraph]]</a>

Alternative token representations are provided for some operators and
punctuators.[^4]

In all respects of the language, each alternative token behaves the
same, respectively, as its primary token, except for its spelling.[^5]

The set of alternative tokens is defined in [[lex.digraph]].

## Tokens <a id="lex.token">[[lex.token]]</a>

``` bnf
token:
    identifier
    keyword
    literal
    operator-or-punctuator
```

There are five kinds of tokens: identifiers, keywords, literals,[^6]

operators, and other separators. Comments and the characters
U+0020 (space), U+0009 (character tabulation), U+000b (line tabulation),
U+000c (form feed), and new-line (collectively, “whitespace”), as
described below, are ignored except as they serve to separate tokens.

[*Note 1*: Whitespace can separate otherwise adjacent identifiers,
keywords, numeric literals, and alternative tokens containing alphabetic
characters. — *end note*]

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

[*Note 1*:

The character properties XID_Start and XID_Continue are described by UAX
\#44 of the Unicode Standard.[^7]

— *end note*]

The program is ill-formed if an *identifier* does not conform to
Normalization Form C as specified in the Unicode Standard.

[*Note 2*: Identifiers are case-sensitive. — *end note*]

[*Note 3*:  [[uaxid]] compares the requirements of UAX \#31 of the
Unicode Standard with the C++ rules for identifiers. — *end note*]

[*Note 4*: In translation phase 4, *identifier* also includes those
*preprocessing-token*s [[lex.pptoken]] differentiated as keywords
[[lex.key]] in the later translation phase 7
[[lex.token]]. — *end note*]

The identifiers in [[lex.name.special]] have a special meaning when
appearing in a certain context. When referred to in the grammar, these
identifiers are used explicitly rather than using the *identifier*
grammar production. Unless otherwise specified, any ambiguity as to
whether a given *identifier* has a special meaning is resolved to
interpret the token as a regular *identifier*.

In addition, some identifiers appearing as a *token* or
*preprocessing-token* are reserved for use by C++ implementations and
shall not be used otherwise; no diagnostic is required.

- Each identifier that contains a double underscore `__` or begins with
  an underscore followed by an uppercase letter, other than those
  specified in this document (for example, `__cplusplus`
  [[cpp.predefined]]), is reserved to the implementation for any use.
- Each identifier that begins with an underscore is reserved to the
  implementation for use as a name in the global namespace.

## Keywords <a id="lex.key">[[lex.key]]</a>

``` bnf
keyword:
    any identifier listed in [[lex.key]]
    *import-keyword*
    *module-keyword*
    *export-keyword*
```

The identifiers shown in [[lex.key]] are reserved for use as keywords
(that is, they are unconditionally treated as keywords in phase 7)
except in an *attribute-token* [[dcl.attr.grammar]].

[*Note 1*: The `register` keyword is unused but is reserved for future
use. — *end note*]

Furthermore, the alternative representations shown in
[[lex.key.digraph]] for certain operators and punctuators
[[lex.digraph]] are reserved and shall not be used otherwise.

**Table: Alternative representations** <a id="lex.key.digraph">[lex.key.digraph]</a>

|          |          |          |         |          |       |
| -------- | -------- | -------- | ------- | -------- | ----- |
| `and`    | `and_eq` | `bitand` | `bitor` | `compl`  | `not` |
| `not_eq` | `or`     | `or_eq`  | `xor`   | `xor_eq` |       |

## Literals <a id="lex.literal">[[lex.literal]]</a>

### Kinds of literals <a id="lex.literal.kinds">[[lex.literal.kinds]]</a>

There are several kinds of literals.[^8]

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

[*Note 1*: When appearing as an *expression*, a literal has a type and
a value category [[expr.prim.literal]]. — *end note*]

### Integer literals <a id="lex.icon">[[lex.icon]]</a>

``` bnf
integer-literal:
    binary-literal integer-suffixₒₚₜ 
    octal-literal integer-suffixₒₚₜ 
    decimal-literal integer-suffixₒₚₜ 
    hexadecimal-literal integer-suffixₒₚₜ
```

``` bnf
binary-literal:
    '0b' binary-digit
    '0B' binary-digit
    binary-literal '''ₒₚₜ binary-digit
```

``` bnf
octal-literal:
    '0'
    octal-literal '''ₒₚₜ octal-digit
```

``` bnf
decimal-literal:
    nonzero-digit
    decimal-literal '''ₒₚₜ digit
```

``` bnf
hexadecimal-literal:
    hexadecimal-prefix hexadecimal-digit-sequence
```

``` bnf
binary-digit: one of
    '0 1'
```

``` bnf
octal-digit: one of
    '0 1 2 3 4 5 6 7'
```

``` bnf
nonzero-digit: one of
    '1 2 3 4 5 6 7 8 9'
```

``` bnf
hexadecimal-prefix: one of
    '0x 0X'
```

``` bnf
hexadecimal-digit-sequence:
    hexadecimal-digit
    hexadecimal-digit-sequence '''ₒₚₜ hexadecimal-digit
```

``` bnf
hexadecimal-digit: one of
    '0 1 2 3 4 5 6 7 8 9'
    'a b c d e f'
    'A B C D E F'
```

``` bnf
integer-suffix:
    unsigned-suffix long-suffixₒₚₜ 
    unsigned-suffix long-long-suffixₒₚₜ 
    unsigned-suffix size-suffixₒₚₜ 
    long-suffix unsigned-suffixₒₚₜ 
    long-long-suffix unsigned-suffixₒₚₜ 
    size-suffix unsigned-suffixₒₚₜ
```

``` bnf
unsigned-suffix: one of
    'u U'
```

``` bnf
long-suffix: one of
    'l L'
```

``` bnf
long-long-suffix: one of
    'll LL'
```

``` bnf
size-suffix: one of
   'z Z'
```

In an *integer-literal*, the sequence of *binary-digit*s,
*octal-digit*s, *digit*s, or *hexadecimal-digit*s is interpreted as a
base N integer as shown in [[lex.icon.base]]; the lexically first digit
of the sequence of digits is the most significant.

[*Note 1*: The prefix and any optional separating single quotes are
ignored when determining the value. — *end note*]

**Table: Base of *integer-literal*{s}** <a id="lex.icon.base">[lex.icon.base]</a>

| Kind of *integer-literal* | base $N$ |
| ------------------------- | -------- |
| *binary-literal*          | 2        |
| *octal-literal*           | 8        |
| *decimal-literal*         | 10       |
| *hexadecimal-literal*     | 16       |


The *hexadecimal-digit*s `a` through `f` and `A` through `F` have
decimal values ten through fifteen.

[*Example 1*: The number twelve can be written `12`, `014`, `0XC`, or
`0b1100`. The *integer-literal*s `1048576`, `1'048'576`, `0X100000`,
`0x10'0000`, and `0'004'000'000` all have the same
value. — *end example*]

The type of an *integer-literal* is the first type in the list in
[[lex.icon.type]] corresponding to its optional *integer-suffix* in
which its value can be represented.

**Table: Types of *integer-literal*s** <a id="lex.icon.type">[lex.icon.type]</a>

| *integer-suffix* | *decimal-literal*                         | *integer-literal* other than *decimal-literal* |
| ---------------- | ----------------------------------------- | ---------------------------------------------- |
| none             | `int`                                     | `int`                                          |
|                  | `long int`                                | `unsigned int`                                 |
|                  | `long long int`                           | `long int`                                     |
|                  |                                           | `unsigned long int`                            |
|                  |                                           | `long long int`                                |
|                  |                                           | `unsigned long long int`                       |
| `u` or `U`       | `unsigned int`                            | `unsigned int`                                 |
|                  | `unsigned long int`                       | `unsigned long int`                            |
|                  | `unsigned long long int`                  | `unsigned long long int`                       |
| `l` or `L`       | `long int`                                | `long int`                                     |
|                  | `long long int`                           | `unsigned long int`                            |
|                  |                                           | `long long int`                                |
|                  |                                           | `unsigned long long int`                       |
| Both `u` or `U`  | `unsigned long int`                       | `unsigned long int`                            |
| and `l` or `L`   | `unsigned long long int`                  | `unsigned long long int`                       |
| `ll` or `LL`     | `long long int`                           | `long long int`                                |
|                  |                                           | `unsigned long long int`                       |
| Both `u` or `U`  | `unsigned long long int`                  | `unsigned long long int`                       |
| and `ll` or `LL` |                                           |                                                |
| `z` or `Z`       | the signed integer type corresponding     | the signed integer type                        |
|                  | to `std::size_t` [[support.types.layout]] | corresponding to `std::size_t`                 |
|                  |                                           | `std::size_t`                                  |
| Both `u` or `U`  | `std::size_t`                             | `std::size_t`                                  |
| and `z` or `Z`   |                                           |                                                |


Except for *integer-literal*s containing a *size-suffix*, if the value
of an *integer-literal* cannot be represented by any type in its list
and an extended integer type [[basic.fundamental]] can represent its
value, it may have that extended integer type. If all of the types in
the list for the *integer-literal* are signed, the extended integer type
is signed. If all of the types in the list for the *integer-literal* are
unsigned, the extended integer type is unsigned. If the list contains
both signed and unsigned types, the extended integer type may be signed
or unsigned. If an *integer-literal* cannot be represented by any of the
allowed types, the program is ill-formed.

[*Note 2*: An *integer-literal* with a `z` or `Z` suffix is ill-formed
if it cannot be represented by `std::size_t`. — *end note*]

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
    c-char c-char-sequenceₒₚₜ
```

``` bnf
c-char:
    basic-c-char
    escape-sequence
    universal-character-name
```

``` bnf
basic-c-char:
    any member of the translation character set except the U+0027 (apostrophe),
      U+005c (reverse solidus), or new-line character
```

``` bnf
escape-sequence:
    simple-escape-sequence
    numeric-escape-sequence
    conditional-escape-sequence
```

``` bnf
simple-escape-sequence:
    '\' simple-escape-sequence-char
```

``` bnf
simple-escape-sequence-char: one of
    '' " ? \ a b f n r t v'
```

``` bnf
numeric-escape-sequence:
    octal-escape-sequence
    hexadecimal-escape-sequence
```

``` bnf
simple-octal-digit-sequence:
    octal-digit simple-octal-digit-sequenceₒₚₜ
```

``` bnf
octal-escape-sequence:
    '\' octal-digit
    '\' octal-digit octal-digit
    '\' octal-digit octal-digit octal-digit
    '\o{' simple-octal-digit-sequence '}'
```

``` bnf
hexadecimal-escape-sequence:
    '\x' simple-hexadecimal-digit-sequence
    '\x{' simple-hexadecimal-digit-sequence '}'
```

``` bnf
conditional-escape-sequence:
    '\' conditional-escape-sequence-char
```

``` bnf
conditional-escape-sequence-char:
    any member of the basic character set that is not an octal-digit, a simple-escape-sequence-char, or the characters 'N', 'o', 'u', 'U', or 'x'
```

A *multicharacter literal* is a *character-literal* whose
*c-char-sequence* consists of more than one *c-char*. A multicharacter
literal shall not have an *encoding-prefix*. If a multicharacter literal
contains a *c-char* that is not encodable as a single code unit in the
ordinary literal encoding, the program is ill-formed. Multicharacter
literals are conditionally-supported.

The kind of a *character-literal*, its type, and its associated
character encoding [[lex.charset]] are determined by its
*encoding-prefix* and its *c-char-sequence* as defined by
[[lex.ccon.literal]].

**Table: Character literals** <a id="lex.ccon.literal">[lex.ccon.literal]</a>

| Encoding | Kind | Type | Associated char- | prefix | \chdr | \chdr | acter encoding |     |
| -------- | ---- | ---- | ---------------- | ------ | ----- | ----- | -------------- | --- |
| none     | ordinary character literal | `char` | ordinary literal | `'v'`  |
| `L`      | wide character literal | `wchar_t` | wide literal     | `L'w'` |
|          |      |      | encoding         |        |
| `u8`     | UTF-8 character literal | `char8_t` | UTF-8            | `u8'x'` |
| `u`      | UTF-16 character literal | `char16_t` | UTF-16           | `u'y'` |
| `U`      | UTF-32 character literal | `char32_t` | UTF-32           | `U'z'` |


In translation phase 4, the value of a *character-literal* is determined
using the range of representable values of the *character-literal*’s
type in translation phase 7. A multicharacter literal has an
*implementation-defined* value. The value of any other kind of
*character-literal* is determined as follows:

- A *character-literal* with a *c-char-sequence* consisting of a single
  *basic-c-char*, *simple-escape-sequence*, or
  *universal-character-name* is the code unit value of the specified
  character as encoded in the literal’s associated character encoding.
  If the specified character lacks representation in the literal’s
  associated character encoding or if it cannot be encoded as a single
  code unit, then the program is ill-formed.
- A *character-literal* with a *c-char-sequence* consisting of a single
  *numeric-escape-sequence* has a value as follows:
  - Let v be the integer value represented by the octal number
    comprising the sequence of *octal-digit*s in an
    *octal-escape-sequence* or by the hexadecimal number comprising the
    sequence of *hexadecimal-digit*s in a *hexadecimal-escape-sequence*.
  - If v does not exceed the range of representable values of the
    *character-literal*’s type, then the value is v.
  - Otherwise, if the *character-literal*’s *encoding-prefix* is absent
    or `L`, and v does not exceed the range of representable values of
    the corresponding unsigned type for the underlying type of the
    *character-literal*’s type, then the value is the unique value of
    the *character-literal*’s type `T` that is congruent to v modulo 2ᴺ,
    where N is the width of `T`.
  - Otherwise, the program is ill-formed.
- A *character-literal* with a *c-char-sequence* consisting of a single
  *conditional-escape-sequence* is conditionally-supported and has an
  *implementation-defined* value.

The character specified by a *simple-escape-sequence* is specified in
[[lex.ccon.esc]].

[*Note 1*: Using an escape sequence for a question mark is supported
for compatibility with C++14 and C. — *end note*]

**Table: Simple escape sequences** <a id="lex.ccon.esc">[lex.ccon.esc]</a>

| character |                      | *simple-escape-sequence* |
| --------- | -------------------- | ------------------------ |
| `U+000a`  | line feed            | `\n`                     |
| `U+0009`  | character tabulation | `\t`                     |
| `U+000b`  | line tabulation      | `\v`                     |
| `U+0008`  | backspace            | `\b`                     |
| `U+000d`  | carriage return      | `\r`                     |
| `U+000c`  | form feed            | `\f`                     |
| `U+0007`  | alert                | `\a`                     |
| `U+005c`  | reverse solidus      | ``                       |
| `U+003f`  | question mark        | `\?`                     |
| `U+0027`  | apostrophe           | `\'`                     |
| `U+0022`  | quotation mark       | `\"`                     |


### Floating-point literals <a id="lex.fcon">[[lex.fcon]]</a>

``` bnf
floating-point-literal:
    decimal-floating-point-literal
    hexadecimal-floating-point-literal
```

``` bnf
decimal-floating-point-literal:
    fractional-constant exponent-partₒₚₜ floating-point-suffixₒₚₜ 
    digit-sequence exponent-part floating-point-suffixₒₚₜ
```

``` bnf
hexadecimal-floating-point-literal:
    hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part floating-point-suffixₒₚₜ 
    hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part floating-point-suffixₒₚₜ
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
    'e' signₒₚₜ digit-sequence
    'E' signₒₚₜ digit-sequence
```

``` bnf
binary-exponent-part:
    'p' signₒₚₜ digit-sequence
    'P' signₒₚₜ digit-sequence
```

``` bnf
sign: one of
    '+ -'
```

``` bnf
digit-sequence:
    digit
    digit-sequence '''ₒₚₜ digit
```

``` bnf
floating-point-suffix: one of
    'f l f16 f32 f64 f128 bf16 F L F16 F32 F64 F128 BF16'
```

The type of a *floating-point-literal*
[[basic.fundamental]], [[basic.extended.fp]] is determined by its
*floating-point-suffix* as specified in [[lex.fcon.type]].

[*Note 1*: The floating-point suffixes `f16`, `f32`, `f64`, `f128`,
`bf16`, `F16`, `F32`, `F64`, `F128`, and `BF16` are
conditionally-supported. See [[basic.extended.fp]]. — *end note*]

**Table: Types of *floating-point-literal*{s}** <a id="lex.fcon.type">[lex.fcon.type]</a>

| *floating-point-suffix* | type              |
| ----------------------- | ----------------- |
| none                    | `double`          |
| `f` or `F`              | `float`           |
| `l` or `L`              | `long` `double`   |
| `f16` or `F16`          | `std::float16_t`  |
| `f32` or `F32`          | `std::float32_t`  |
| `f64` or `F64`          | `std::float64_t`  |
| `f128` or `F128`        | `std::float128_t` |
| `bf16` or `BF16`        | `std::bfloat16_t` |


The *significand* of a *floating-point-literal* is the
*fractional-constant* or *digit-sequence* of a
*decimal-floating-point-literal* or the
*hexadecimal-fractional-constant* or *hexadecimal-digit-sequence* of a
*hexadecimal-floating-point-literal*. In the significand, the sequence
of *digit*s or *hexadecimal-digit*s and optional period are interpreted
as a base N real number s, where N is 10 for a
*decimal-floating-point-literal* and 16 for a
*hexadecimal-floating-point-literal*.

[*Note 2*: Any optional separating single quotes are ignored when
determining the value. — *end note*]

If an *exponent-part* or *binary-exponent-part* is present, the exponent
e of the *floating-point-literal* is the result of interpreting the
sequence of an optional *sign* and the *digit*s as a base 10 integer.
Otherwise, the exponent e is 0. The scaled value of the literal is
s × 10ᵉ for a *decimal-floating-point-literal* and s × 2ᵉ for a
*hexadecimal-floating-point-literal*.

[*Example 1*: The *floating-point-literal*s `49.625` and `0xC.68p+2`
have the same value. The *floating-point-literal*s `1.602'176'565e-19`
and `1.602176565e-19` have the same value. — *end example*]

If the scaled value is not in the range of representable values for its
type, the program is ill-formed. Otherwise, the value of a
*floating-point-literal* is the scaled value if representable, else the
larger or smaller representable value nearest the scaled value, chosen
in an *implementation-defined* manner.

### String literals <a id="lex.string">[[lex.string]]</a>

``` bnf
string-literal:
    encoding-prefixₒₚₜ '"' s-char-sequenceₒₚₜ '"'
    encoding-prefixₒₚₜ 'R' raw-string
```

``` bnf
s-char-sequence:
    s-char s-char-sequenceₒₚₜ
```

``` bnf
s-char:
    basic-s-char
    escape-sequence
    universal-character-name
```

``` bnf
basic-s-char:
    any member of the translation character set except the U+0022 (quotation mark),
      U+005c (reverse solidus), or new-line character
```

``` bnf
raw-string:
    '"' d-char-sequenceₒₚₜ '(' r-char-sequenceₒₚₜ ')' d-char-sequenceₒₚₜ '"'
```

``` bnf
r-char-sequence:
    r-char r-char-sequenceₒₚₜ
```

``` bnf
r-char:
    any member of the translation character set, except a U+0029 (right parenthesis) followed by
       the initial *d-char-sequence* (which may be empty) followed by a U+0022 (quotation mark)
```

``` bnf
d-char-sequence:
    d-char d-char-sequenceₒₚₜ
```

``` bnf
d-char:
    any member of the basic character set except:
      U+0020 (space), U+0028 (left parenthesis), U+0029 (right parenthesis), U+005c (reverse solidus),
      U+0009 (character tabulation), U+000b (line tabulation), U+000c (form feed), and new-line
```

The kind of a *string-literal*, its type, and its associated character
encoding [[lex.charset]] are determined by its encoding prefix and
sequence of *s-char*s or *r-char*s as defined by [[lex.string.literal]]
where n is the number of encoded code units that would result from an
evaluation of the *string-literal* (see below).

**Table: String literals** <a id="lex.string.literal">[lex.string.literal]</a>

| Enco- | Kind | Type | Associated | ding | \chdr | \chdr | character | prefix | \chdr | \chdr | encoding | \rhdr |
| ----- | ---- | ---- | ---------- | ---- | ----- | ----- | --------- | ------ | ----- | ----- | -------- | ----- |
| none  | ordinary string literal | array of $n$ `const char` | ordinary literal encoding | `"ordinary string"` `R"(ordinary raw string)"` |
| `L`   | wide string literal | array of $n$ `const wchar_t` | wide literal encoding | `L"wide string"` `LR"w(wide raw string)w"` |
| `u8`  | UTF-8 string literal | array of $n$ `const char8_t` | UTF-8      | `u8"UTF-8 string"` `u8R"x(UTF-8 raw string)x"` |
| `u`   | UTF-16 string literal | array of $n$ `const char16_t` | UTF-16     | `u"UTF-16 string"` `uR"y(UTF-16 raw string)y"` |
| `U`   | UTF-32 string literal | array of $n$ `const char32_t` | UTF-32     | `U"UTF-32 string"` `UR"z(UTF-32 raw string)z"` |


A *string-literal* that has an `R` in the prefix is a *raw string
literal*. The *d-char-sequence* serves as a delimiter. The terminating
*d-char-sequence* of a *raw-string* is the same sequence of characters
as the initial *d-char-sequence*. A *d-char-sequence* shall consist of
at most 16 characters.

[*Note 1*: The characters `'('` and `')'` can appear in a *raw-string*.
Thus, `R"delimiter((a|b))delimiter"` is equivalent to
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
R"(x = "\"y\"")"
```

is equivalent to `"x = \"\\\"y\\\"\""`.

— *end example*]

Ordinary string literals and UTF-8 string literals are also referred to
as *narrow string literals*.

The *string-literal*s in any sequence of adjacent *string-literal*s
shall have at most one unique *encoding-prefix* among them. The common
*encoding-prefix* of the sequence is that *encoding-prefix*, if any.

[*Note 3*: A *string-literal*’s rawness has no effect on the
determination of the common *encoding-prefix*. — *end note*]

In translation phase 6 [[lex.phases]], adjacent *string-literal*s are
concatenated. The lexical structure and grouping of the contents of the
individual *string-literal*s is retained.

[*Example 2*:

``` cpp
"\xA" "B"
```

represents the code unit `'\xA'` and the character `'B'` after
concatenation (and not the single code unit `'\xAB'`). Similarly,

``` cpp
R"(\u00)" "41"
```

represents six characters, starting with a backslash and ending with the
digit `1` (and not the single character `'A'` specified by a
*universal-character-name*).

[[lex.string.concat]] has some examples of valid concatenations.

— *end example*]

**Table: String literal concatenations** <a id="lex.string.concat">[lex.string.concat]</a>

|                            |       |                            |       |                            |       |
| -------------------------- | ----- | -------------------------- | ----- | -------------------------- | ----- |
| *[spans 2 columns]* Source | Means | *[spans 2 columns]* Source | Means | *[spans 2 columns]* Source | Means |
| `u"a"`                     | `u"b"` | `u"ab"`                    | `U"a"` | `U"b"`                     | `U"ab"` | `L"a"` | `L"b"` | `L"ab"` |
| `u"a"`                     | `"b"` | `u"ab"`                    | `U"a"` | `"b"`                      | `U"ab"` | `L"a"` | `"b"` | `L"ab"` |
| `"a"`                      | `u"b"` | `u"ab"`                    | `"a"` | `U"b"`                     | `U"ab"` | `"a"` | `L"b"` | `L"ab"` |


Evaluating a *string-literal* results in a string literal object with
static storage duration [[basic.stc]].

[*Note 4*: String literal objects are potentially non-unique
[[intro.object]]. Whether successive evaluations of a *string-literal*
yield the same or a different object is unspecified. — *end note*]

[*Note 5*:  The effect of attempting to modify a string literal object
is undefined. — *end note*]

String literal objects are initialized with the sequence of code unit
values corresponding to the *string-literal*’s sequence of *s-char*s
(originally from non-raw string literals) and *r-char*s (originally from
raw string literals), plus a terminating U+0000 (null) character, in
order as follows:

- The sequence of characters denoted by each contiguous sequence of
  *basic-s-char*s, *r-char*s, *simple-escape-sequence*s [[lex.ccon]],
  and *universal-character-name*s [[lex.charset]] is encoded to a code
  unit sequence using the *string-literal*’s associated character
  encoding. If a character lacks representation in the associated
  character encoding, then the program is ill-formed. \[*Note 6*: No
  character lacks representation in any Unicode encoding
  form. — *end note*] When encoding a stateful character encoding,
  implementations should encode the first such sequence beginning with
  the initial encoding state and encode subsequent sequences beginning
  with the final encoding state of the prior sequence. \[*Note 7*: The
  encoded code unit sequence can differ from the sequence of code units
  that would be obtained by encoding each character
  independently. — *end note*]
- Each *numeric-escape-sequence* [[lex.ccon]] contributes a single code
  unit with a value as follows:
  - Let v be the integer value represented by the octal number
    comprising the sequence of *octal-digit*s in an
    *octal-escape-sequence* or by the hexadecimal number comprising the
    sequence of *hexadecimal-digit*s in a *hexadecimal-escape-sequence*.
  - If v does not exceed the range of representable values of the
    *string-literal*’s array element type, then the value is v.
  - Otherwise, if the *string-literal*’s *encoding-prefix* is absent or
    `L`, and v does not exceed the range of representable values of the
    corresponding unsigned type for the underlying type of the
    *string-literal*’s array element type, then the value is the unique
    value of the *string-literal*’s array element type `T` that is
    congruent to v modulo 2ᴺ, where N is the width of `T`.
  - Otherwise, the program is ill-formed.

  When encoding a stateful character encoding, these sequences should
  have no effect on encoding state.
- Each *conditional-escape-sequence* [[lex.ccon]] contributes an
  *implementation-defined* code unit sequence. When encoding a stateful
  character encoding, it is *implementation-defined* what effect these
  sequences have on encoding state.

### Unevaluated strings <a id="lex.string.uneval">[[lex.string.uneval]]</a>

``` bnf
unevaluated-string:
    string-literal
```

An *unevaluated-string* shall have no *encoding-prefix*.

Each *universal-character-name* and each *simple-escape-sequence* in an
*unevaluated-string* is replaced by the member of the translation
character set it denotes. An *unevaluated-string* that contains a
*numeric-escape-sequence* or a *conditional-escape-sequence* is
ill-formed.

An *unevaluated-string* is never evaluated and its interpretation
depends on the context in which it appears.

### Boolean literals <a id="lex.bool">[[lex.bool]]</a>

``` bnf
boolean-literal:
    false
    true
```

The Boolean literals are the keywords `false` and `true`. Such literals
have type `bool`.

### Pointer literals <a id="lex.nullptr">[[lex.nullptr]]</a>

``` bnf
pointer-literal:
    nullptr
```

The pointer literal is the keyword `nullptr`. It has type
`std::nullptr_t`.

[*Note 1*: `std::nullptr_t` is a distinct type that is neither a
pointer type nor a pointer-to-member type; rather, a prvalue of this
type is a null pointer constant and can be converted to a null pointer
value or null member pointer value. See  [[conv.ptr]] and 
[[conv.mem]]. — *end note*]

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
    fractional-constant exponent-partₒₚₜ ud-suffix
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
operator ""X<'c₁', 'c₂', ... 'cₖ'>()
```

where *n* is the source character sequence c₁c₂...cₖ.

[*Note 1*: The sequence c₁c₂...cₖ can only contain characters from the
basic character set. — *end note*]

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
operator ""X<'c₁', 'c₂', ... 'cₖ'>()
```

where *f* is the source character sequence c₁c₂...cₖ.

[*Note 2*: The sequence c₁c₂...cₖ can only contain characters from the
basic character set. — *end note*]

If *L* is a *user-defined-string-literal*, let *str* be the literal
without its *ud-suffix* and let *len* be the number of code units in
*str* (i.e., its length excluding the terminating null character). If
*S* contains a literal operator template with a constant template
parameter for which *str* is a well-formed *template-argument*, the
literal *L* is treated as a call of the form

``` cpp
operator ""X<str>()
```

Otherwise, the literal *L* is treated as a call of the form

``` cpp
operator ""X(str, len)
```

If *L* is a *user-defined-character-literal*, let *ch* be the literal
without its *ud-suffix*. *S* shall contain a literal operator
[[over.literal]] whose only parameter has the type of *ch* and the
literal *L* is treated as a call of the form

``` cpp
operator ""X(ch)
```

[*Example 2*:

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

— *end example*]

In translation phase 6 [[lex.phases]], adjacent *string-literal*s are
concatenated and *user-defined-string-literal*s are considered
*string-literal*s for that purpose. During concatenation, *ud-suffix*es
are removed and ignored and the concatenation process occurs as
described in  [[lex.string]]. At the end of phase 6, if a
*string-literal* is the result of a concatenation involving at least one
*user-defined-string-literal*, all the participating
*user-defined-string-literal*s shall have the same *ud-suffix* and that
suffix is applied to the result of the concatenation.

[*Example 3*:

``` cpp
int main() {
  L"A" "B" "C"_x;   // OK, same as L"ABC"_x
  "P"_x "Q" "R"_y;  // error: two different ud-suffix{es}
}
```

— *end example*]

<!-- Link reference definitions -->
[basic.extended.fp]: basic.md#basic.extended.fp
[basic.fundamental]: basic.md#basic.fundamental
[basic.link]: basic.md#basic.link
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.stc]: basic.md#basic.stc
[character.seq]: library.md#character.seq
[class.mem.general]: class.md#class.mem.general
[conv.mem]: expr.md#conv.mem
[conv.ptr]: expr.md#conv.ptr
[cpp]: cpp.md#cpp
[cpp.cond]: cpp.md#cpp.cond
[cpp.embed]: cpp.md#cpp.embed
[cpp.import]: cpp.md#cpp.import
[cpp.include]: cpp.md#cpp.include
[cpp.module]: cpp.md#cpp.module
[cpp.pragma]: cpp.md#cpp.pragma
[cpp.pragma.op]: cpp.md#cpp.pragma.op
[cpp.pre]: cpp.md#cpp.pre
[cpp.predefined]: cpp.md#cpp.predefined
[cpp.replace]: cpp.md#cpp.replace
[cpp.stringize]: cpp.md#cpp.stringize
[dcl.attr.grammar]: dcl.md#dcl.attr.grammar
[dcl.pre]: dcl.md#dcl.pre
[expr.const]: expr.md#expr.const
[expr.prim.literal]: expr.md#expr.prim.literal
[headers]: library.md#headers
[intro.object]: basic.md#intro.object
[lex]: #lex
[lex.bool]: #lex.bool
[lex.ccon]: #lex.ccon
[lex.ccon.esc]: #lex.ccon.esc
[lex.ccon.literal]: #lex.ccon.literal
[lex.char]: #lex.char
[lex.charset]: #lex.charset
[lex.charset.basic]: #lex.charset.basic
[lex.charset.literal]: #lex.charset.literal
[lex.comment]: #lex.comment
[lex.digraph]: #lex.digraph
[lex.ext]: #lex.ext
[lex.fcon]: #lex.fcon
[lex.fcon.type]: #lex.fcon.type
[lex.header]: #lex.header
[lex.icon]: #lex.icon
[lex.icon.base]: #lex.icon.base
[lex.icon.type]: #lex.icon.type
[lex.key]: #lex.key
[lex.key.digraph]: #lex.key.digraph
[lex.literal]: #lex.literal
[lex.literal.kinds]: #lex.literal.kinds
[lex.name]: #lex.name
[lex.name.special]: #lex.name.special
[lex.nullptr]: #lex.nullptr
[lex.operators]: #lex.operators
[lex.phases]: #lex.phases
[lex.ppnumber]: #lex.ppnumber
[lex.pptoken]: #lex.pptoken
[lex.separate]: #lex.separate
[lex.string]: #lex.string
[lex.string.concat]: #lex.string.concat
[lex.string.literal]: #lex.string.literal
[lex.string.uneval]: #lex.string.uneval
[lex.token]: #lex.token
[lex.universal.char]: #lex.universal.char
[module.import]: module.md#module.import
[module.reach]: module.md#module.reach
[module.unit]: module.md#module.unit
[over.literal]: over.md#over.literal
[support.types.layout]: support.md#support.types.layout
[temp.explicit]: temp.md#temp.explicit
[temp.inst]: temp.md#temp.inst
[temp.names]: temp.md#temp.names
[temp.point]: temp.md#temp.point
[uaxid]: uax31.md#uaxid

[^1]: Implementations behave as if these separate phases occur, although
    in practice different phases can be folded together.

[^2]: Unicode® is a registered trademark of Unicode, Inc. This
    information is given for the convenience of users of this document
    and does not constitute an endorsement by ISO or IEC of this
    product.

[^3]: A partial preprocessing token would arise from a source file
    ending in the first portion of a multi-character token that requires
    a terminating sequence of characters, such as a *header-name* that
    is missing the closing `"` or `>`. A partial comment would arise
    from a source file ending with an unclosed `/*` comment.

[^4]:  These include “digraphs” and additional reserved words. The term
    “digraph” (token consisting of two characters) is not perfectly
    descriptive, since one of the alternative *preprocessing-token*s is
    `%:%:` and of course several primary tokens contain two characters.
    Nonetheless, those alternative tokens that aren’t lexical keywords
    are colloquially known as “digraphs”.

[^5]: Thus the “stringized” values [[cpp.stringize]] of `[` and `<:`
    will be different, maintaining the source spelling, but the tokens
    can otherwise be freely interchanged.

[^6]: Literals include strings and character and numeric literals.

[^7]: On systems in which linkers cannot accept extended characters, an
    encoding of the \*universal-character-name\* can be used in forming
    valid external identifiers. For example, some otherwise unused
    character or sequence of characters can be used to encode the `̆` in
    a \*universal-character-name\*. Extended characters can produce a
    long external identifier, but C++ does not place a translation limit
    on significant characters for external identifiers.

[^8]: The term “literal” generally designates, in this document, those
    tokens that are called “constants” in C.
