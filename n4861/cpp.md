# Preprocessing directives <a id="cpp">[[cpp]]</a>

## Preamble <a id="cpp.pre">[[cpp.pre]]</a>

``` bnf
preprocessing-file:
    groupₒₚₜ
    module-file
```

``` bnf
module-file:
    pp-global-module-fragmentₒₚₜ pp-module groupₒₚₜ pp-private-module-fragmentₒₚₜ
```

``` bnf
pp-global-module-fragment:
    module ';' new-line groupₒₚₜ
```

``` bnf
pp-private-module-fragment:
    module ':' private ';' new-line groupₒₚₜ
```

``` bnf
group:
    group-part
    group group-part
```

``` bnf
group-part:
    control-line
    if-section
    text-line
    '#' conditionally-supported-directive
```

``` bnf
control-line:
    '# include' pp-tokens new-line
    pp-import
    '# define ' identifier replacement-list new-line
    '# define ' identifier lparen identifier-listₒₚₜ ')' replacement-list new-line
    '# define ' identifier lparen '... )' replacement-list new-line
    '# define ' identifier lparen identifier-list ', ... )' replacement-list new-line
    '# undef  ' identifier new-line
    '# line   ' pp-tokens new-line
    '# error  ' pp-tokensₒₚₜ new-line
    '# pragma ' pp-tokensₒₚₜ new-line
    '# 'new-line
```

``` bnf
if-section:
    if-group elif-groupsₒₚₜ else-groupₒₚₜ endif-line
```

``` bnf
if-group:
    '# if     ' constant-expression new-line groupₒₚₜ
    '# ifdef  ' identifier new-line groupₒₚₜ
    '# ifndef ' identifier new-line groupₒₚₜ
```

``` bnf
elif-groups:
    elif-group
    elif-groups elif-group
```

``` bnf
elif-group:
    '# elif   ' constant-expression new-line groupₒₚₜ
```

``` bnf
else-group:
    '# else   ' new-line groupₒₚₜ
```

``` bnf
endif-line:
    '# endif  ' new-line
```

``` bnf
text-line:
    pp-tokensₒₚₜ new-line
```

``` bnf
conditionally-supported-directive:
    pp-tokens new-line
```

``` bnf
lparen:
    a '(' character not immediately preceded by white-space
```

``` bnf
identifier-list:
    identifier
    identifier-list ',' identifier
```

``` bnf
replacement-list:
    pp-tokensₒₚₜ
```

``` bnf
pp-tokens:
    preprocessing-token
    pp-tokens preprocessing-token
```

``` bnf
new-line:
    the new-line character
```

A *preprocessing directive* consists of a sequence of preprocessing
tokens that satisfies the following constraints: At the start of
translation phase 4, the first token in the sequence, referred to as a
*directive-introducing token*, begins with the first character in the
source file (optionally after white space containing no new-line
characters) or follows white space containing at least one new-line
character, and is

- a `#` preprocessing token, or
- an `import` preprocessing token immediately followed on the same
  logical line by a *header-name*, `<`, *identifier*, *string-literal*,
  or `:` preprocessing token, or
- a `module` preprocessing token immediately followed on the same
  logical line by an *identifier*, `:`, or `;` preprocessing token, or
- an `export` preprocessing token immediately followed on the same
  logical line by one of the two preceding forms.

The last token in the sequence is the first token within the sequence
that is immediately followed by whitespace containing a new-line
character. [^1]

[*Note 1*: A new-line character ends the preprocessing directive even
if it occurs within what would otherwise be an invocation of a
function-like macro. — *end note*]

[*Example 1*:

``` cpp
#                       // preprocessing directive
module ;                // preprocessing directive
export module leftpad;  // preprocessing directive
import <string>;        // preprocessing directive
export import "squee";  // preprocessing directive
import rightpad;        // preprocessing directive
import :part;           // preprocessing directive

module                  // not a preprocessing directive
;                       // not a preprocessing directive

export                  // not a preprocessing directive
import                  // not a preprocessing directive
foo;                    // not a preprocessing directive

export                  // not a preprocessing directive
import foo;             // preprocessing directive (ill-formed at phase 7)

import ::               // not a preprocessing directive
import ->               // not a preprocessing directive
```

— *end example*]

A sequence of preprocessing tokens is only a *text-line* if it does not
begin with a directive-introducing token. A sequence of preprocessing
tokens is only a *conditionally-supported-directive* if it does not
begin with any of the directive names appearing after a `#` in the
syntax. A *conditionally-supported-directive* is conditionally-supported
with *implementation-defined* semantics.

At the start of phase 4 of translation, the *group* of a
*pp-global-module-fragment* shall contain neither a *text-line* nor a
*pp-import*.

When in a group that is skipped [[cpp.cond]], the directive syntax is
relaxed to allow any sequence of preprocessing tokens to occur between
the directive name and the following new-line character.

The only white-space characters that shall appear between preprocessing
tokens within a preprocessing directive (from just after the
directive-introducing token through just before the terminating new-line
character) are space and horizontal-tab (including spaces that have
replaced comments or possibly other white-space characters in
translation phase 3).

The implementation can process and skip sections of source files
conditionally, include other source files, import macros from header
units, and replace macros. These capabilities are called
*preprocessing*, because conceptually they occur before translation of
the resulting translation unit.

The preprocessing tokens within a preprocessing directive are not
subject to macro expansion unless otherwise stated.

[*Example 2*:

In:

``` cpp
#define EMPTY
EMPTY   #   include <file.h>
```

the sequence of preprocessing tokens on the second line is *not* a
preprocessing directive, because it does not begin with a `#` at the
start of translation phase 4, even though it will do so after the macro
`EMPTY` has been replaced.

— *end example*]

## Conditional inclusion <a id="cpp.cond">[[cpp.cond]]</a>

``` bnf
defined-macro-expression:
    'defined' identifier
    'defined (' identifier ')'
```

``` bnf
h-preprocessing-token:
    any *preprocessing-token* other than '>'
```

``` bnf
h-pp-tokens:
    h-preprocessing-token
    h-pp-tokens h-preprocessing-token
```

``` bnf
header-name-tokens:
    string-literal
    '<' h-pp-tokens '>'
```

``` bnf
has-include-expression:
    '__has_include' '(' header-name ')'
    '__has_include' '(' header-name-tokens ')'
```

``` bnf
has-attribute-expression:
    '__has_cpp_attribute (' pp-tokens ')'
```

The expression that controls conditional inclusion shall be an integral
constant expression except that identifiers (including those lexically
identical to keywords) are interpreted as described below[^2] and it may
contain zero or more *defined-macro-expression*s and/or
*has-include-expression*s and/or *has-attribute-expression*s as unary
operator expressions.

A *defined-macro-expression* evaluates to `1` if the identifier is
currently defined as a macro name (that is, if it is predefined or if it
has one or more active macro definitions [[cpp.import]], for example
because it has been the subject of a `#define` preprocessing directive
without an intervening `#undef` directive with the same subject
identifier), `0` if it is not.

The second form of *has-include-expression* is considered only if the
first form does not match, in which case the preprocessing tokens are
processed just as in normal text.

The header or source file identified by the parenthesized preprocessing
token sequence in each contained *has-include-expression* is searched
for as if that preprocessing token sequence were the *pp-tokens* in a
`#include` directive, except that no further macro expansion is
performed. If such a directive would not satisfy the syntactic
requirements of a `#include` directive, the program is ill-formed. The
*has-include-expression* evaluates to `1` if the search for the source
file succeeds, and to `0` if the search fails.

Each *has-attribute-expression* is replaced by a non-zero *pp-number*
matching the form of an *integer-literal* if the implementation supports
an attribute with the name specified by interpreting the *pp-tokens*,
after macro expansion, as an *attribute-token*, and by `0` otherwise.
The program is ill-formed if the *pp-tokens* do not match the form of an
*attribute-token*.

For an attribute specified in this document, the value of the
*has-attribute-expression* is given by [[cpp.cond.ha]]. For other
attributes recognized by the implementation, the value is
*implementation-defined*.

[*Note 1*: It is expected that the availability of an attribute can be
detected by any non-zero result. — *end note*]

**Table: __has_cpp_attribute values**

| Attribute            | Value     |
| -------------------- | --------- |
| `carries_dependency` | `200809L` |
| `deprecated`         | `201309L` |
| `fallthrough`        | `201603L` |
| `likely`             | `201803L` |
| `maybe_unused`       | `201603L` |
| `no_unique_address`  | `201803L` |
| `nodiscard`          | `201907L` |
| `noreturn`           | `200809L` |
| `unlikely`           | `201803L` |


The `#ifdef` and `#ifndef` directives, and the `defined` conditional
inclusion operator, shall treat `__has_include` and
`__has_cpp_attribute` as if they were the names of defined macros. The
identifiers `__has_include` and `__has_cpp_attribute` shall not appear
in any context not mentioned in this subclause.

Each preprocessing token that remains (in the list of preprocessing
tokens that will become the controlling expression) after all macro
replacements have occurred shall be in the lexical form of a token
[[lex.token]].

Preprocessing directives of the forms

``` bnf
'# if     ' constant-expression new-line groupₒₚₜ
'# elif   ' constant-expression new-line groupₒₚₜ
```

check whether the controlling constant expression evaluates to nonzero.

Prior to evaluation, macro invocations in the list of preprocessing
tokens that will become the controlling constant expression are replaced
(except for those macro names modified by the `defined` unary operator),
just as in normal text. If the token `defined` is generated as a result
of this replacement process or use of the `defined` unary operator does
not match one of the two specified forms prior to macro replacement, the
behavior is undefined.

After all replacements due to macro expansion and evaluations of
*defined-macro-expression*s, *has-include-expression*s, and
*has-attribute-expression*s have been performed, all remaining
identifiers and keywords, except for `true` and `false`, are replaced
with the *pp-number* `0`, and then each preprocessing token is converted
into a token.

[*Note 2*: An alternative token [[lex.digraph]] is not an identifier,
even when its spelling consists entirely of letters and underscores.
Therefore it is not subject to this replacement. — *end note*]

The resulting tokens comprise the controlling constant expression which
is evaluated according to the rules of  [[expr.const]] using arithmetic
that has at least the ranges specified in  [[support.limits]]. For the
purposes of this token conversion and evaluation all signed and unsigned
integer types act as if they have the same representation as,
respectively, `intmax_t` or `uintmax_t` [[cstdint]].

[*Note 3*: Thus on an implementation where
`std::numeric_limits<int>::max()` is `0x7FFF` and
`std::numeric_limits<unsigned int>::max()` is `0xFFFF`, the integer
literal `0x8000` is signed and positive within a `#if` expression even
though it is unsigned in translation phase 7
[[lex.phases]]. — *end note*]

This includes interpreting *character-literal*s, which may involve
converting escape sequences into execution character set members.
Whether the numeric value for these *character-literal*s matches the
value obtained when an identical *character-literal* occurs in an
expression (other than within a `#if` or `#elif` directive) is
*implementation-defined*.

[*Note 4*:

Thus, the constant expression in the following `#if` directive and `if`
statement [[stmt.if]] is not guaranteed to evaluate to the same value in
these two contexts:

``` cpp
#if 'z' - 'a' == 25
if ('z' - 'a' == 25)
```

— *end note*]

Also, whether a single-character *character-literal* may have a negative
value is *implementation-defined*. Each subexpression with type `bool`
is subjected to integral promotion before processing continues.

Preprocessing directives of the forms

``` bnf
'# ifdef  ' identifier new-line groupₒₚₜ
'# ifndef ' identifier new-line groupₒₚₜ
```

check whether the identifier is or is not currently defined as a macro
name. Their conditions are equivalent to `#if` `defined` *identifier*
and `#if` `!defined` *identifier* respectively.

Each directive’s condition is checked in order. If it evaluates to false
(zero), the group that it controls is skipped: directives are processed
only through the name that determines the directive in order to keep
track of the level of nested conditionals; the rest of the directives’
preprocessing tokens are ignored, as are the other preprocessing tokens
in the group. Only the first group whose control condition evaluates to
true (nonzero) is processed; any following groups are skipped and their
controlling directives are processed as if they were in a group that is
skipped. If none of the conditions evaluates to true, and there is a
`#else` directive, the group controlled by the `#else` is processed;
lacking a `#else` directive, all the groups until the `#endif` are
skipped.[^3]

[*Example 1*:

This demonstrates a way to include a library `optional` facility only if
it is available:

``` cpp
#if __has_include(<optional>)
#  include <optional>
#  if __cpp_lib_optional >= 201603
#    define have_optional 1
#  endif
#elif __has_include(<experimental/optional>)
#  include <experimental/optional>
#  if __cpp_lib_experimental_optional >= 201411
#    define have_optional 1
#    define experimental_optional 1
#  endif
#endif
#ifndef have_optional
#  define have_optional 0
#endif
```

— *end example*]

[*Example 2*:

This demonstrates a way to use the attribute `[[acme::deprecated]]` only
if it is available.

``` cpp
#if __has_cpp_attribute(acme::deprecated)
#  define ATTR_DEPRECATED(msg) [[acme::deprecated(msg)]]
#else
#  define ATTR_DEPRECATED(msg) [[deprecated(msg)]]
#endif
ATTR_DEPRECATED("This function is deprecated") void anvil();
```

— *end example*]

## Source file inclusion <a id="cpp.include">[[cpp.include]]</a>

A `#include` directive shall identify a header or source file that can
be processed by the implementation.

A preprocessing directive of the form

``` bnf
'# include <' h-char-sequence '>' new-line
```

searches a sequence of *implementation-defined* places for a header
identified uniquely by the specified sequence between the `<` and `>`
delimiters, and causes the replacement of that directive by the entire
contents of the header. How the places are specified or the header
identified is *implementation-defined*.

A preprocessing directive of the form

``` bnf
'# include "' q-char-sequence '"' new-line
```

causes the replacement of that directive by the entire contents of the
source file identified by the specified sequence between the `"`
delimiters. The named source file is searched for in an
*implementation-defined* manner. If this search is not supported, or if
the search fails, the directive is reprocessed as if it read

``` bnf
'# include <' h-char-sequence '>' new-line
```

with the identical contained sequence (including `>` characters, if any)
from the original directive.

A preprocessing directive of the form

``` bnf
'# include' pp-tokens new-line
```

(that does not match one of the two previous forms) is permitted. The
preprocessing tokens after `include` in the directive are processed just
as in normal text (i.e., each identifier currently defined as a macro
name is replaced by its replacement list of preprocessing tokens). If
the directive resulting after all replacements does not match one of the
two previous forms, the behavior is undefined.[^4] The method by which a
sequence of preprocessing tokens between a `<` and a `>` preprocessing
token pair or a pair of `"` characters is combined into a single header
name preprocessing token is *implementation-defined*.

The implementation shall provide unique mappings for sequences
consisting of one or more *nondigit*s or *digit*s [[lex.name]] followed
by a period (`.`) and a single *nondigit*. The first character shall not
be a *digit*. The implementation may ignore distinctions of alphabetical
case.

A `#include` preprocessing directive may appear in a source file that
has been read because of a `#include` directive in another file, up to
an *implementation-defined* nesting limit.

If the header identified by the *header-name* denotes an importable
header [[module.import]], it is *implementation-defined* whether the
`#include` preprocessing directive is instead replaced by an `import`
directive [[cpp.import]] of the form

``` bnf
'import' header-name ';' new-line
```

[*Note 1*:

Although an implementation may provide a mechanism for making arbitrary
source files available to the `< >` search, in general programmers
should use the `< >` form for headers provided with the implementation,
and the `" "` form for sources outside the control of the
implementation. For instance:

``` cpp
#include <stdio.h>
#include <unistd.h>
#include "usefullib.h"
#include "myprog.h"
```

— *end note*]

[*Example 1*:

This illustrates macro-replaced `#include` directives:

``` cpp
#if VERSION == 1
    #define INCFILE  "vers1.h"
#elif VERSION == 2
    #define INCFILE  "vers2.h"  // and so on
#else
    #define INCFILE  "versN.h"
#endif
#include INCFILE
```

— *end example*]

## Module directive <a id="cpp.module">[[cpp.module]]</a>

``` bnf
pp-module:
    exportₒₚₜ module pp-tokensₒₚₜ ';' new-line
```

A *pp-module* shall not appear in a context where `module` or (if it is
the first token of the *pp-module*) `export` is an identifier defined as
an object-like macro.

Any preprocessing tokens after the `module` preprocessing token in the
`module` directive are processed just as in normal text.

[*Note 1*: Each identifier currently defined as a macro name is
replaced by its replacement list of preprocessing tokens. — *end note*]

The `module` and `export` (if it exists) preprocessing tokens are
replaced by the *module-keyword* and *export-keyword* preprocessing
tokens respectively.

[*Note 2*: This makes the line no longer a directive so it is not
removed at the end of phase 4. — *end note*]

## Header unit importation <a id="cpp.import">[[cpp.import]]</a>

``` bnf
pp-import:
    exportₒₚₜ import header-name pp-tokensₒₚₜ ';' new-line
    exportₒₚₜ import header-name-tokens pp-tokensₒₚₜ ';' new-line
    exportₒₚₜ import pp-tokens ';' new-line
```

A *pp-import* shall not appear in a context where `import` or (if it is
the first token of the *pp-import*) `export` is an identifier defined as
an object-like macro.

The preprocessing tokens after the `import` preprocessing token in the
`import` *control-line* are processed just as in normal text (i.e., each
identifier currently defined as a macro name is replaced by its
replacement list of preprocessing tokens). An `import` directive
matching the first two forms of a *pp-import* instructs the preprocessor
to import macros from the header unit [[module.import]] denoted by the
*header-name*. The *point of macro import* for the first two forms of
*pp-import* is immediately after the *new-line* terminating the
*pp-import*. The last form of *pp-import* is only considered if the
first two forms did not match.

If a *pp-import* is produced by source file inclusion (including by the
rewrite produced when a `#include` directive names an importable header)
while processing the *group* of a *module-file*, the program is
ill-formed.

In all three forms of *pp-import*, the `import` and `export` (if it
exists) preprocessing tokens are replaced by the *import-keyword* and
*export-keyword* preprocessing tokens respectively.

[*Note 1*: This makes the line no longer a directive so it is not
removed at the end of phase 4. — *end note*]

Additionally, in the second form of *pp-import*, a *header-name* token
is formed as if the *header-name-tokens* were the *pp-tokens* of a
`#include` directive. The *header-name-tokens* are replaced by the
*header-name* token.

[*Note 2*: This ensures that imports are treated consistently by the
preprocessor and later phases of translation. — *end note*]

Each `#define` directive encountered when preprocessing each translation
unit in a program results in a distinct *macro definition*.

[*Note 3*: A predefined macro name [[cpp.predefined]] is not introduced
by a `#define` directive. Implementations providing mechanisms to
predefine additional macros are encouraged to not treat them as being
introduced by a `#define` directive. — *end note*]

Importing macros from a header unit makes macro definitions from a
translation unit visible in other translation units. Each macro
definition has at most one point of definition in each translation unit
and at most one point of undefinition, as follows:

- The *point of definition* of a macro definition within a translation
  unit is the point at which its `#define` directive occurs (in the
  translation unit containing the `#define` directive), or, if the macro
  name is not lexically identical to a keyword [[lex.key]] or to the
  *identifier*s `module` or `import`, the first point of macro import of
  a translation unit containing a point of definition for the macro
  definition, if any (in any other translation unit).
- The *point of undefinition* of a macro definition within a translation
  unit is the first point at which a `#undef` directive naming the macro
  occurs after its point of definition, or the first point of macro
  import of a translation unit containing a point of undefinition for
  the macro definition, whichever (if any) occurs first.

A macro directive is *active* at a source location if it has a point of
definition in that translation unit preceding the location, and does not
have a point of undefinition in that translation unit preceding the
location.

If a macro would be replaced or redefined, and multiple macro
definitions are active for that macro name, the active macro definitions
shall all be valid redefinitions of the same macro [[cpp.replace]].

[*Note 4*: The relative order of *pp-import*s has no bearing on whether
a particular macro definition is active. — *end note*]

[*Example 1*:

Importable header \`"a.h"\`

``` cpp
#define X 123   // #1
#define Y 45    // #2
#define Z a     // #3
#undef X        // point of undefinition of #1 in "a.h"
```

Importable header \`"b.h"\`

``` cpp
import "a.h";   // point of definition of #1, #2, and #3, point of undefinition of #1 in "b.h"
#define X 456   // OK, #1 is not active
#define Y 6     // error: #2 is active
```

Importable header \`"c.h"\`

``` cpp
#define Y 45    // #4
#define Z c     // #5
```

Importable header \`"d.h"\`

``` cpp
import "a.h";   // point of definition of #1, #2, and #3, point of undefinition of #1 in "d.h"
import "c.h";   // point of definition of #4 and #5 in "d.h"
int a = Y;      // OK, active macro definitions #2 and #4 are valid redefinitions
int c = Z;      // error: active macro definitions #3 and #5 are not valid redefinitions of Z
```

— *end example*]

## Macro replacement <a id="cpp.replace">[[cpp.replace]]</a>

Two replacement lists are identical if and only if the preprocessing
tokens in both have the same number, ordering, spelling, and white-space
separation, where all white-space separations are considered identical.

An identifier currently defined as an object-like macro (see below) may
be redefined by another `#define` preprocessing directive provided that
the second definition is an object-like macro definition and the two
replacement lists are identical, otherwise the program is ill-formed.
Likewise, an identifier currently defined as a function-like macro (see
below) may be redefined by another `#define` preprocessing directive
provided that the second definition is a function-like macro definition
that has the same number and spelling of parameters, and the two
replacement lists are identical, otherwise the program is ill-formed.

[*Example 1*:

The following sequence is valid:

``` cpp
#define OBJ_LIKE      (1-1)
#define OBJ_LIKE      /* white space */ (1-1) /* other */
#define FUNC_LIKE(a)   ( a )
#define FUNC_LIKE( a )(     /* note the white space */ \
                a /* other stuff on this line
                  */ )
```

But the following redefinitions are invalid:

``` cpp
#define OBJ_LIKE    (0)         // different token sequence
#define OBJ_LIKE    (1 - 1)     // different white space
#define FUNC_LIKE(b) ( a )      // different parameter usage
#define FUNC_LIKE(b) ( b )      // different parameter spelling
```

— *end example*]

There shall be white-space between the identifier and the replacement
list in the definition of an object-like macro.

If the *identifier-list* in the macro definition does not end with an
ellipsis, the number of arguments (including those arguments consisting
of no preprocessing tokens) in an invocation of a function-like macro
shall equal the number of parameters in the macro definition. Otherwise,
there shall be at least as many arguments in the invocation as there are
parameters in the macro definition (excluding the `...`). There shall
exist a `)` preprocessing token that terminates the invocation.

The identifiers `__VA_ARGS__` and `__VA_OPT__` shall occur only in the
*replacement-list* of a function-like macro that uses the ellipsis
notation in the parameters.

A parameter identifier in a function-like macro shall be uniquely
declared within its scope.

The identifier immediately following the `define` is called the *macro
name*. There is one name space for macro names. Any white-space
characters preceding or following the replacement list of preprocessing
tokens are not considered part of the replacement list for either form
of macro.

If a `#` preprocessing token, followed by an identifier, occurs
lexically at the point at which a preprocessing directive could begin,
the identifier is not subject to macro replacement.

A preprocessing directive of the form

``` bnf
'# define' identifier replacement-list new-line
```

defines an *object-like macro* that causes each subsequent instance of
the macro name[^5] to be replaced by the replacement list of
preprocessing tokens that constitute the remainder of the directive.[^6]
The replacement list is then rescanned for more macro names as specified
below.

[*Example 2*:

The simplest use of this facility is to define a “manifest constant”, as
in

``` cpp
#define TABSIZE 100
int table[TABSIZE];
```

— *end example*]

A preprocessing directive of the form

``` bnf
'# define' identifier lparen identifier-listₒₚₜ ')' replacement-list new-line
'# define' identifier lparen '...' ')' replacement-list new-line
'# define' identifier lparen identifier-list ', ...' ')' replacement-list new-line
```

defines a *function-like macro* with parameters, whose use is similar
syntactically to a function call. The parameters are specified by the
optional list of identifiers, whose scope extends from their declaration
in the identifier list until the new-line character that terminates the
`#define` preprocessing directive. Each subsequent instance of the
function-like macro name followed by a `(` as the next preprocessing
token introduces the sequence of preprocessing tokens that is replaced
by the replacement list in the definition (an invocation of the macro).
The replaced sequence of preprocessing tokens is terminated by the
matching `)` preprocessing token, skipping intervening matched pairs of
left and right parenthesis preprocessing tokens. Within the sequence of
preprocessing tokens making up an invocation of a function-like macro,
new-line is considered a normal white-space character.

The sequence of preprocessing tokens bounded by the outside-most
matching parentheses forms the list of arguments for the function-like
macro. The individual arguments within the list are separated by comma
preprocessing tokens, but comma preprocessing tokens between matching
inner parentheses do not separate arguments. If there are sequences of
preprocessing tokens within the list of arguments that would otherwise
act as preprocessing directives,[^7] the behavior is undefined.

[*Example 3*:

The following defines a function-like macro whose value is the maximum
of its arguments. It has the disadvantages of evaluating one or the
other of its arguments a second time (including side effects) and
generating more code than a function if invoked several times. It also
cannot have its address taken, as it has none.

``` cpp
#define max(a, b) ((a) > (b) ? (a) : (b))
```

The parentheses ensure that the arguments and the resulting expression
are bound properly.

— *end example*]

If there is a `...` immediately preceding the `)` in the function-like
macro definition, then the trailing arguments (if any), including any
separating comma preprocessing tokens, are merged to form a single item:
the *variable arguments*. The number of arguments so combined is such
that, following merger, the number of arguments is either equal to or
one more than the number of parameters in the macro definition
(excluding the `...`).

### Argument substitution <a id="cpp.subst">[[cpp.subst]]</a>

``` bnf
va-opt-replacement:
    '__VA_OPT__ (' pp-tokensₒₚₜ ')'
```

After the arguments for the invocation of a function-like macro have
been identified, argument substitution takes place. For each parameter
in the replacement list that is neither preceded by a `#` or `##`
preprocessing token nor followed by a `##` preprocessing token, the
preprocessing tokens naming the parameter are replaced by a token
sequence determined as follows:

- If the parameter is of the form *va-opt-replacement*, the replacement
  preprocessing tokens are the preprocessing token sequence for the
  corresponding argument, as specified below.
- Otherwise, the replacement preprocessing tokens are the preprocessing
  tokens of corresponding argument after all macros contained therein
  have been expanded. The argument’s preprocessing tokens are completely
  macro replaced before being substituted as if they formed the rest of
  the preprocessing file with no other preprocessing tokens being
  available.

[*Example 1*:

``` cpp
#define LPAREN() (
#define G(Q) 42
#define F(R, X, ...)  __VA_OPT__(G R X) )
int x = F(LPAREN(), 0, <:-);    // replaced by int x = 42;
```

— *end example*]

An identifier `__VA_ARGS__` that occurs in the replacement list shall be
treated as if it were a parameter, and the variable arguments shall form
the preprocessing tokens used to replace it.

[*Example 2*:

``` cpp
#define debug(...) fprintf(stderr, __VA_ARGS__)
#define showlist(...) puts(#__VA_ARGS__)
#define report(test, ...) ((test) ? puts(#test) : printf(__VA_ARGS__))
debug("Flag");
debug("X = %d\n", x);
showlist(The first, second, and third items.);
report(x>y, "x is %d but y is %d", x, y);
```

results in

``` cpp
fprintf(stderr, "Flag");
fprintf(stderr, "X = %d\n", x);
puts("The first, second, and third items.");
((x>y) ? puts("x>y") : printf("x is %d but y is %d", x, y));
```

— *end example*]

The identifier `__VA_OPT__` shall always occur as part of the
preprocessing token sequence *va-opt-replacement*; its closing `)` is
determined by skipping intervening pairs of matching left and right
parentheses in its *pp-tokens*. The *pp-tokens* of a
*va-opt-replacement* shall not contain `__VA_OPT__`. If the *pp-tokens*
would be ill-formed as the replacement list of the current function-like
macro, the program is ill-formed. A *va-opt-replacement* is treated as
if it were a parameter, and the preprocessing token sequence for the
corresponding argument is defined as follows. If the substitution of
`__VA_ARGS__` as neither an operand of `#` nor `##` consists of no
preprocessing tokens, the argument consists of a single placemarker
preprocessing token ([[cpp.concat]], [[cpp.rescan]]). Otherwise, the
argument consists of the results of the expansion of the contained
*pp-tokens* as the replacement list of the current function-like macro
before removal of placemarker tokens, rescanning, and further
replacement.

[*Note 1*: The placemarker tokens are removed before stringization
[[cpp.stringize]], and can be removed by rescanning and further
replacement [[cpp.rescan]]. — *end note*]

[*Example 3*:

``` cpp
#define F(...)           f(0 __VA_OPT__(,) __VA_ARGS__)
#define G(X, ...)        f(0, X __VA_OPT__(,) __VA_ARGS__)
#define SDEF(sname, ...) S sname __VA_OPT__(= { __VA_ARGS__ })
#define EMP

F(a, b, c)          // replaced by f(0, a, b, c)
F()                 // replaced by f(0)
F(EMP)              // replaced by f(0)

G(a, b, c)          // replaced by f(0, a, b, c)
G(a, )              // replaced by f(0, a)
G(a)                // replaced by f(0, a)

SDEF(foo);          // replaced by S foo;
SDEF(bar, 1, 2);    // replaced by S bar = { 1, 2 }

#define H1(X, ...) X __VA_OPT__(##) __VA_ARGS__ // error: ## may not appear at
                                                // the beginning of a replacement list[cpp.concat]

#define H2(X, Y, ...) __VA_OPT__(X ## Y,) __VA_ARGS__
H2(a, b, c, d)      // replaced by ab, c, d

#define H3(X, ...) #__VA_OPT__(X##X X##X)
H3(, 0)             // replaced by ""

#define H4(X, ...) __VA_OPT__(a X ## X) ## b
H4(, 1)             // replaced by a b

#define H5A(...) __VA_OPT__()/**/__VA_OPT__()
#define H5B(X) a ## X ## b
#define H5C(X) H5B(X)
H5C(H5A())          // replaced by ab
```

— *end example*]

### The `#` operator <a id="cpp.stringize">[[cpp.stringize]]</a>

Each `#` preprocessing token in the replacement list for a function-like
macro shall be followed by a parameter as the next preprocessing token
in the replacement list.

A *character string literal* is a *string-literal* with no prefix. If,
in the replacement list, a parameter is immediately preceded by a `#`
preprocessing token, both are replaced by a single character string
literal preprocessing token that contains the spelling of the
preprocessing token sequence for the corresponding argument (excluding
placemarker tokens). Let the *stringizing argument* be the preprocessing
token sequence for the corresponding argument with placemarker tokens
removed. Each occurrence of white space between the stringizing
argument’s preprocessing tokens becomes a single space character in the
character string literal. White space before the first preprocessing
token and after the last preprocessing token comprising the stringizing
argument is deleted. Otherwise, the original spelling of each
preprocessing token in the stringizing argument is retained in the
character string literal, except for special handling for producing the
spelling of *string-literal*s and *character-literal*s: a `\` character
is inserted before each `"` and `\` character of a *character-literal*
or *string-literal* (including the delimiting `"` characters). If the
replacement that results is not a valid character string literal, the
behavior is undefined. The character string literal corresponding to an
empty stringizing argument is `""`. The order of evaluation of `#` and
`##` operators is unspecified.

### The `##` operator <a id="cpp.concat">[[cpp.concat]]</a>

A `##` preprocessing token shall not occur at the beginning or at the
end of a replacement list for either form of macro definition.

If, in the replacement list of a function-like macro, a parameter is
immediately preceded or followed by a `##` preprocessing token, the
parameter is replaced by the corresponding argument’s preprocessing
token sequence; however, if an argument consists of no preprocessing
tokens, the parameter is replaced by a placemarker preprocessing token
instead.[^8]

For both object-like and function-like macro invocations, before the
replacement list is reexamined for more macro names to replace, each
instance of a `##` preprocessing token in the replacement list (not from
an argument) is deleted and the preceding preprocessing token is
concatenated with the following preprocessing token. Placemarker
preprocessing tokens are handled specially: concatenation of two
placemarkers results in a single placemarker preprocessing token, and
concatenation of a placemarker with a non-placemarker preprocessing
token results in the non-placemarker preprocessing token. If the result
is not a valid preprocessing token, the behavior is undefined. The
resulting token is available for further macro replacement. The order of
evaluation of `##` operators is unspecified.

[*Example 1*:

The sequence

``` cpp
#define str(s)      # s
#define xstr(s)     str(s)
#define debug(s, t) printf("x" # s "= %d, x" # t "= %s", \
               x ## s, x ## t)
#define INCFILE(n)  vers ## n
#define glue(a, b)  a ## b
#define xglue(a, b) glue(a, b)
#define HIGHLOW     "hello"
#define LOW         LOW ", world"

debug(1, 2);
fputs(str(strncmp("abc\0d", "abc", '\4')        // this goes away
    == 0) str(: \@n), s);
#include xstr(INCFILE(2).h)
glue(HIGH, LOW);
xglue(HIGH, LOW)
```

results in

``` cpp
printf("x" "1" "= %d, x" "2" "= %s", x1, x2);
fputs("strncmp(\"abc\\0d\", \"abc\", '\\4') == 0" ": \@n", s);
#include "vers2.h"      (after macro replacement, before file access)
"hello";
"hello" ", world"
```

or, after concatenation of the character string literals,

``` cpp
printf("x1= %d, x2= %s", x1, x2);
fputs("strncmp(\"abc\\0d\", \"abc\", '\\4') == 0: \@n", s);
#include "vers2.h"      (after macro replacement, before file access)
"hello";
"hello, world"
```

Space around the `#` and `##` tokens in the macro definition is
optional.

— *end example*]

[*Example 2*:

In the following fragment:

``` cpp
#define hash_hash # ## #
#define mkstr(a) # a
#define in_between(a) mkstr(a)
#define join(c, d) in_between(c hash_hash d)
char p[] = join(x, y);          // equivalent to char p[] = "x ## y";
```

The expansion produces, at various stages:

``` cpp
join(x, y)
in_between(x hash_hash y)
in_between(x ## y)
mkstr(x ## y)
"x ## y"
```

In other words, expanding `hash_hash` produces a new token, consisting
of two adjacent sharp signs, but this new token is not the `##`
operator.

— *end example*]

[*Example 3*:

To illustrate the rules for placemarker preprocessing tokens, the
sequence

``` cpp
#define t(x,y,z) x ## y ## z
int j[] = { t(1,2,3), t(,4,5), t(6,,7), t(8,9,),
  t(10,,), t(,11,), t(,,12), t(,,) };
```

results in

``` cpp
int j[] = { 123, 45, 67, 89,
  10, 11, 12, };
```

— *end example*]

### Rescanning and further replacement <a id="cpp.rescan">[[cpp.rescan]]</a>

After all parameters in the replacement list have been substituted and
`#` and `##` processing has taken place, all placemarker preprocessing
tokens are removed. Then the resulting preprocessing token sequence is
rescanned, along with all subsequent preprocessing tokens of the source
file, for more macro names to replace.

[*Example 1*:

The sequence

``` cpp
#define x       3
#define f(a)    f(x * (a))
#undef  x
#define x       2
#define g       f
#define z       z[0]
#define h       g(~
#define m(a)    a(w)
#define w       0,1
#define t(a)    a
#define p()     int
#define q(x)    x
#define r(x,y)  x ## y
#define str(x)  # x

f(y+1) + f(f(z)) % t(t(g)(0) + t)(1);
g(x+(3,4)-w) | h 5) & m
    (f)^m(m);
p() i[q()] = { q(1), r(2,3), r(4,), r(,5), r(,) };
char c[2][6] = { str(hello), str() };
```

results in

``` cpp
f(2 * (y+1)) + f(2 * (f(2 * (z[0])))) % f(2 * (0)) + t(1);
f(2 * (2+(3,4)-0,1)) | f(2 * (~ 5)) & f(2 * (0,1))^m(0,1);
int i[] = { 1, 23, 4, 5, };
char c[2][6] = { "hello", "" };
```

— *end example*]

If the name of the macro being replaced is found during this scan of the
replacement list (not including the rest of the source file’s
preprocessing tokens), it is not replaced. Furthermore, if any nested
replacements encounter the name of the macro being replaced, it is not
replaced. These nonreplaced macro name preprocessing tokens are no
longer available for further replacement even if they are later
(re)examined in contexts in which that macro name preprocessing token
would otherwise have been replaced.

The resulting completely macro-replaced preprocessing token sequence is
not processed as a preprocessing directive even if it resembles one, but
all pragma unary operator expressions within it are then processed as
specified in  [[cpp.pragma.op]] below.

### Scope of macro definitions <a id="cpp.scope">[[cpp.scope]]</a>

A macro definition lasts (independent of block structure) until a
corresponding `#undef` directive is encountered or (if none is
encountered) until the end of the translation unit. Macro definitions
have no significance after translation phase 4.

A preprocessing directive of the form

``` bnf
'# undef' identifier new-line
```

causes the specified identifier no longer to be defined as a macro name.
It is ignored if the specified identifier is not currently defined as a
macro name.

## Line control <a id="cpp.line">[[cpp.line]]</a>

The *string-literal* of a `#line` directive, if present, shall be a
character string literal.

The *line number* of the current source line is one greater than the
number of new-line characters read or introduced in translation phase 1
[[lex.phases]] while processing the source file to the current token.

A preprocessing directive of the form

``` bnf
'# line' digit-sequence new-line
```

causes the implementation to behave as if the following sequence of
source lines begins with a source line that has a line number as
specified by the digit sequence (interpreted as a decimal integer). If
the digit sequence specifies zero or a number greater than 2147483647,
the behavior is undefined.

A preprocessing directive of the form

``` bnf
'# line' digit-sequence '"' s-char-sequenceₒₚₜ '"' new-line
```

sets the presumed line number similarly and changes the presumed name of
the source file to be the contents of the character string literal.

A preprocessing directive of the form

``` bnf
'# line' pp-tokens new-line
```

(that does not match one of the two previous forms) is permitted. The
preprocessing tokens after `line` on the directive are processed just as
in normal text (each identifier currently defined as a macro name is
replaced by its replacement list of preprocessing tokens). If the
directive resulting after all replacements does not match one of the two
previous forms, the behavior is undefined; otherwise, the result is
processed as appropriate.

## Error directive <a id="cpp.error">[[cpp.error]]</a>

A preprocessing directive of the form

``` bnf
'# error' pp-tokensₒₚₜ new-line
```

causes the implementation to produce a diagnostic message that includes
the specified sequence of preprocessing tokens, and renders the program
ill-formed.

## Pragma directive <a id="cpp.pragma">[[cpp.pragma]]</a>

A preprocessing directive of the form

``` bnf
'# pragma' pp-tokensₒₚₜ new-line
```

causes the implementation to behave in an *implementation-defined*
manner. The behavior might cause translation to fail or cause the
translator or the resulting program to behave in a non-conforming
manner. Any pragma that is not recognized by the implementation is
ignored.

## Null directive <a id="cpp.null">[[cpp.null]]</a>

A preprocessing directive of the form

``` bnf
'#' new-line
```

has no effect.

## Predefined macro names <a id="cpp.predefined">[[cpp.predefined]]</a>

The following macro names shall be defined by the implementation:

- **`__cplusplus`**

The integer literal `202302L`.

[*Note 1*: It is intended that future versions of this International
Standard will replace the value of this macro with a greater
value. — *end note*]

- **`__DATE__`**

The date of translation of the source file: a character string literal
of the form `"Mmm dd yyyy"`, where the names of the months are the same
as those generated by the `asctime` function, and the first character of
`dd` is a space character if the value is less than 10. If the date of
translation is not available, an *implementation-defined* valid date
shall be supplied.

- **`__FILE__`**

The presumed name of the current source file (a character string
literal). [^9]

- **`__LINE__`**

The presumed line number (within the current source file) of the current
source line (an integer literal). [^10]

- **`__STDC_HOSTED__`**

The integer literal `1` if the implementation is a hosted implementation
or the integer literal `0` if it is not.

- **`__STDCPP_DEFAULT_NEW_ALIGNMENT__`**

An integer literal of type `std::size_t` whose value is the alignment
guaranteed by a call to `operator new(std::size_t)` or
`operator new[](std::size_t)`.

[*Note 2*: Larger alignments will be passed to
`operator new(std::size_t, std::align_val_t)`, etc.
[[expr.new]]. — *end note*]

- **`__TIME__`**

The time of translation of the source file: a character string literal
of the form `"hh:mm:ss"` as in the time generated by the `asctime`
function. If the time of translation is not available, an
*implementation-defined* valid time shall be supplied.

- **The names listed in [[cpp.predefined.ft]].**

The macros defined in [[cpp.predefined.ft]] shall be defined to the
corresponding integer literal.

[*Note 3*: Future versions of this International Standard might replace
the values of these macros with greater values. — *end note*]

**Table: Feature-test macros**

| Macro name                              | Value     |
| --------------------------------------- | --------- |
| `__cpp_aggregate_bases`                 | `201603L` |
| `__cpp_aggregate_nsdmi`                 | `201304L` |
| `__cpp_aggregate_paren_init`            | `201902L` |
| `__cpp_alias_templates`                 | `200704L` |
| `__cpp_aligned_new`                     | `201606L` |
| `__cpp_attributes`                      | `200809L` |
| `__cpp_binary_literals`                 | `201304L` |
| `__cpp_capture_star_this`               | `201603L` |
| `__cpp_char8_t`                         | `201811L` |
| `__cpp_concepts`                        | `201907L` |
| `__cpp_conditional_explicit`            | `201806L` |
| `__cpp_constexpr`                       | `201907L` |
| `__cpp_constexpr_dynamic_alloc`         | `201907L` |
| `__cpp_constexpr_in_decltype`           | `201711L` |
| `__cpp_consteval`                       | `201811L` |
| `__cpp_constinit`                       | `201907L` |
| `__cpp_decltype`                        | `200707L` |
| `__cpp_decltype_auto`                   | `201304L` |
| `__cpp_deduction_guides`                | `201907L` |
| `__cpp_delegating_constructors`         | `200604L` |
| `__cpp_designated_initializers`         | `201707L` |
| `__cpp_enumerator_attributes`           | `201411L` |
| `__cpp_fold_expressions`                | `201603L` |
| `__cpp_generic_lambdas`                 | `201707L` |
| `__cpp_guaranteed_copy_elision`         | `201606L` |
| `__cpp_hex_float`                       | `201603L` |
| `__cpp_if_constexpr`                    | `201606L` |
| `__cpp_impl_coroutine`                  | `201902L` |
| `__cpp_impl_destroying_delete`          | `201806L` |
| `__cpp_impl_three_way_comparison`       | `201907L` |
| `__cpp_inheriting_constructors`         | `201511L` |
| `__cpp_init_captures`                   | `201803L` |
| `__cpp_initializer_lists`               | `200806L` |
| `__cpp_inline_variables`                | `201606L` |
| `__cpp_lambdas`                         | `200907L` |
| `__cpp_modules`                         | `201907L` |
| `__cpp_namespace_attributes`            | `201411L` |
| `__cpp_noexcept_function_type`          | `201510L` |
| `__cpp_nontype_template_args`           | `201911L` |
| `__cpp_nontype_template_parameter_auto` | `201606L` |
| `__cpp_nsdmi`                           | `200809L` |
| `__cpp_range_based_for`                 | `201603L` |
| `__cpp_raw_strings`                     | `200710L` |
| `__cpp_ref_qualifiers`                  | `200710L` |
| `__cpp_return_type_deduction`           | `201304L` |
| `__cpp_rvalue_references`               | `200610L` |
| `__cpp_sized_deallocation`              | `201309L` |
| `__cpp_static_assert`                   | `201411L` |
| `__cpp_structured_bindings`             | `201606L` |
| `__cpp_template_template_args`          | `201611L` |
| `__cpp_threadsafe_static_init`          | `200806L` |
| `__cpp_unicode_characters`              | `200704L` |
| `__cpp_unicode_literals`                | `200710L` |
| `__cpp_user_defined_literals`           | `200809L` |
| `__cpp_using_enum`                      | `201907L` |
| `__cpp_variable_templates`              | `201304L` |
| `__cpp_variadic_templates`              | `200704L` |
| `__cpp_variadic_using`                  | `201611L` |


The following macro names are conditionally defined by the
implementation:

- **`__STDC__`**

Whether \_\_STDC\_\_ is predefined and if so, what its value is, are
*implementation-defined*.

- **`__STDC_MB_MIGHT_NEQ_WC__`**

The integer literal `1`, intended to indicate that, in the encoding for
`wchar_t`, a member of the basic character set need not have a code
value equal to its value when used as the lone character in an ordinary
character literal.

- **`__STDC_VERSION__`**

Whether \_\_STDC_VERSION\_\_ is predefined and if so, what its value is,
are *implementation-defined*.

- **`__STDC_ISO_10646__`**

An integer literal of the form `yyyymmL` (for example, `199712L`). If
this symbol is defined, then every character in the Unicode required
set, when stored in an object of type `wchar_t`, has the same value as
the code point of that character. The *Unicode required set* consists of
all the characters that are defined by ISO/IEC 10646, along with all
amendments and technical corrigenda as of the specified year and month.

- **`__STDCPP_STRICT_POINTER_SAFETY__`**

Defined, and has the value integer literal 1, if and only if the
implementation has strict pointer safety
[[basic.stc.dynamic.safety]].

- **`__STDCPP_THREADS__`**

Defined, and has the value integer literal 1, if and only if a program
can have more than one thread of execution [[intro.multithread]].

The values of the predefined macros (except for `__FILE__` and
`__LINE__`) remain constant throughout the translation unit.

If any of the pre-defined macro names in this subclause, or the
identifier `defined`, is the subject of a `#define` or a `#undef`
preprocessing directive, the behavior is undefined. Any other predefined
macro names shall begin with a leading underscore followed by an
uppercase letter or a second underscore.

## Pragma operator <a id="cpp.pragma.op">[[cpp.pragma.op]]</a>

A unary operator expression of the form:

``` bnf
'_Pragma' '(' string-literal ')'
```

is processed as follows: The *string-literal* is *destringized* by
deleting the `L` prefix, if present, deleting the leading and trailing
double-quotes, replacing each escape sequence `\"` by a double-quote,
and replacing each escape sequence `\\` by a single backslash. The
resulting sequence of characters is processed through translation phase
3 to produce preprocessing tokens that are executed as if they were the
*pp-tokens* in a pragma directive. The original four preprocessing
tokens in the unary operator expression are removed.

[*Example 1*:

``` cpp
#pragma listing on "..\listing.dir"
```

can also be expressed as:

``` cpp
_Pragma ( "listing on \"..\\listing.dir\"" )
```

The latter form is processed in the same way whether it appears
literally as shown, or results from macro replacement, as in:

``` cpp
#define LISTING(x) PRAGMA(listing on #x)
#define PRAGMA(x) _Pragma(#x)

LISTING( ..\listing.dir )
```

— *end example*]

<!-- Link reference definitions -->
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[cpp]: #cpp
[cpp.concat]: #cpp.concat
[cpp.cond]: #cpp.cond
[cpp.cond.ha]: #cpp.cond.ha
[cpp.error]: #cpp.error
[cpp.import]: #cpp.import
[cpp.include]: #cpp.include
[cpp.line]: #cpp.line
[cpp.module]: #cpp.module
[cpp.null]: #cpp.null
[cpp.pragma]: #cpp.pragma
[cpp.pragma.op]: #cpp.pragma.op
[cpp.pre]: #cpp.pre
[cpp.predefined]: #cpp.predefined
[cpp.predefined.ft]: #cpp.predefined.ft
[cpp.replace]: #cpp.replace
[cpp.rescan]: #cpp.rescan
[cpp.scope]: #cpp.scope
[cpp.stringize]: #cpp.stringize
[cpp.subst]: #cpp.subst
[cstdint]: support.md#cstdint
[expr.const]: expr.md#expr.const
[expr.new]: expr.md#expr.new
[intro.multithread]: basic.md#intro.multithread
[lex.digraph]: lex.md#lex.digraph
[lex.key]: lex.md#lex.key
[lex.name]: lex.md#lex.name
[lex.phases]: lex.md#lex.phases
[lex.token]: lex.md#lex.token
[module.import]: module.md#module.import
[stmt.if]: stmt.md#stmt.if
[support.limits]: support.md#support.limits

[^1]: Thus, preprocessing directives are commonly called “lines”. These
    “lines” have no other syntactic significance, as all white space is
    equivalent except in certain situations during preprocessing (see
    the `#` character string literal creation operator in 
    [[cpp.stringize]], for example).

[^2]: Because the controlling constant expression is evaluated during
    translation phase 4, all identifiers either are or are not macro
    names — there simply are no keywords, enumeration constants, etc.

[^3]: As indicated by the syntax, a preprocessing token shall not follow
    a `#else` or `#endif` directive before the terminating new-line
    character. However, comments may appear anywhere in a source file,
    including within a preprocessing directive.

[^4]: Note that adjacent *string-literal*s are not concatenated into a
    single *string-literal* (see the translation phases in 
    [[lex.phases]]); thus, an expansion that results in two
    *string-literal*s is an invalid directive.

[^5]: Since, by macro-replacement time, all *character-literal*s and
    *string-literal*s are preprocessing tokens, not sequences possibly
    containing identifier-like subsequences (see [[lex.phases]],
    translation phases), they are never scanned for macro names or
    parameters.

[^6]: An alternative token [[lex.digraph]] is not an identifier, even
    when its spelling consists entirely of letters and underscores.
    Therefore it is not possible to define a macro whose name is the
    same as that of an alternative token.

[^7]: A *conditionally-supported-directive* is a preprocessing directive
    regardless of whether the implementation supports it.

[^8]: Placemarker preprocessing tokens do not appear in the syntax
    because they are temporary entities that exist only within
    translation phase 4.

[^9]: The presumed source file name can be changed by the `#line`
    directive.

[^10]: The presumed line number can be changed by the `#line` directive.
