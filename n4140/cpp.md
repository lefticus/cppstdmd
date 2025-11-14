# Preprocessing directives <a id="cpp">[[cpp]]</a>

A *preprocessing directive* consists of a sequence of preprocessing
tokens that satisfies the following constraints: The first token in the
sequence is a `#` preprocessing token that (at the start of translation
phase 4) is either the first character in the source file (optionally
after white space containing no new-line characters) or that follows
white space containing at least one new-line character. The last token
in the sequence is the first new-line character that follows the first
token in the sequence.[^1] A new-line character ends the preprocessing
directive even if it occurs within what would otherwise be an invocation
of a function-like macro.

``` bnf
preprocessing-file:
    group\opt
```

``` bnf
group:
    group-part
    group group-part
```

``` bnf
group-part:
    if-section
    control-line
    text-line
    '#' non-directive
```

``` bnf
if-section:
    if-group elif-groupseₒₚₜlse-groupeₒₚₜndif-line
```

``` bnf
elif-groups:
    elif-group
    elif-groups elif-group
```

``` bnf
text-line:
    pp-tokensₒₚₜ new-line
```

``` bnf
non-directive:
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
    pp-tokens\opt
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

A text line shall not begin with a `#` preprocessing token. A
non-directive shall not begin with any of the directive names appearing
in the syntax.

When in a group that is skipped ([[cpp.cond]]), the directive syntax is
relaxed to allow any sequence of preprocessing tokens to occur between
the directive name and the following new-line character.

The only white-space characters that shall appear between preprocessing
tokens within a preprocessing directive (from just after the introducing
`#` preprocessing token through just before the terminating new-line
character) are space and horizontal-tab (including spaces that have
replaced comments or possibly other white-space characters in
translation phase 3).

The implementation can process and skip sections of source files
conditionally, include other source files, and replace macros. These
capabilities are called *preprocessing*, because conceptually they occur
before translation of the resulting translation unit.

The preprocessing tokens within a preprocessing directive are not
subject to macro expansion unless otherwise stated.

In:

``` cpp
#define EMPTY
EMPTY   #   include <file.h>
```

the sequence of preprocessing tokens on the second line is *not* a
preprocessing directive, because it does not begin with a \# at the
start of translation phase 4, even though it will do so after the macro
`EMPTY` has been replaced.

## Conditional inclusion <a id="cpp.cond">[[cpp.cond]]</a>

The expression that controls conditional inclusion shall be an integral
constant expression except that identifiers (including those lexically
identical to keywords) are interpreted as described below[^2] and it may
contain unary operator expressions of the form

``` bnf
'defined' identifier
```

or

``` bnf
'defined (' identifier ')'
```

which evaluate to `1` if the identifier is currently defined as a macro
name (that is, if it is predefined or if it has been the subject of a
`#define` preprocessing directive without an intervening `#undef`
directive with the same subject identifier), `0` if it is not.

Each preprocessing token that remains (in the list of preprocessing
tokens that will become the controlling expression) after all macro
replacements have occurred shall be in the lexical form of a token (
[[lex.token]]).

Preprocessing directives of the forms

check whether the controlling constant expression evaluates to nonzero.

Prior to evaluation, macro invocations in the list of preprocessing
tokens that will become the controlling constant expression are replaced
(except for those macro names modified by the `defined` unary operator),
just as in normal text. If the token `defined` is generated as a result
of this replacement process or use of the `defined` unary operator does
not match one of the two specified forms prior to macro replacement, the
behavior is undefined. After all replacements due to macro expansion and
the `defined` unary operator have been performed, all remaining
identifiers and keywords[^3], except for `true` and `false`, are
replaced with the pp-number `0`, and then each preprocessing token is
converted into a token. The resulting tokens comprise the controlling
constant expression which is evaluated according to the rules of 
[[expr.const]] using arithmetic that has at least the ranges specified
in  [[support.limits]]. For the purposes of this token conversion and
evaluation all signed and unsigned integer types act as if they have the
same representation as, respectively, `intmax_t` or `uintmax_t` (
[[cstdint]]).[^4] This includes interpreting character literals, which
may involve converting escape sequences into execution character set
members. Whether the numeric value for these character literals matches
the value obtained when an identical character literal occurs in an
expression (other than within a `#if` or `#elif` directive) is
*implementation-defined*.[^5] Also, whether a single-character character
literal may have a negative value is *implementation-defined*. Each
subexpression with type `bool` is subjected to integral promotion before
processing continues.

Preprocessing directives of the forms

check whether the identifier is or is not currently defined as a macro
name. Their conditions are equivalent to `#if` `defined` *identifier*
and `#if` `!defined` *identifier* respectively.

Each directive’s condition is checked in order. If it evaluates to false
(zero), the group that it controls is skipped: directives are processed
only through the name that determines the directive in order to keep
track of the level of nested conditionals; the rest of the directives’
preprocessing tokens are ignored, as are the other preprocessing tokens
in the group. Only the first group whose control condition evaluates to
true (nonzero) is processed. If none of the conditions evaluates to
true, and there is a `#else` directive, the group controlled by the
`#else` is processed; lacking a `#else` directive, all the groups until
the `#endif` are skipped.[^6]

## Source file inclusion <a id="cpp.include">[[cpp.include]]</a>

A `#include` directive shall identify a header or source file that can
be processed by the implementation.

A preprocessing directive of the form

``` bnf
'# include <'h-char-sequence'>' new-line
```

searches a sequence of *implementation-defined* places for a header
identified uniquely by the specified sequence between the `<` and `>`
delimiters, and causes the replacement of that directive by the entire
contents of the header. How the places are specified or the header
identified is *implementation-defined*.

A preprocessing directive of the form

``` bnf
'# include "'q-char-sequence'"' new-line
```

causes the replacement of that directive by the entire contents of the
source file identified by the specified sequence between the `"`
delimiters. The named source file is searched for in an
*implementation-defined* manner. If this search is not supported, or if
the search fails, the directive is reprocessed as if it read

``` bnf
'# include <'h-char-sequence'>' new-line
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
two previous forms, the behavior is undefined.[^7] The method by which a
sequence of preprocessing tokens between a `<` and a `>` preprocessing
token pair or a pair of `"` characters is combined into a single header
name preprocessing token is *implementation-defined*.

The implementation shall provide unique mappings for sequences
consisting of one or more *nondigit*s or *digit*s ([[lex.name]])
followed by a period (`.`) and a single *nondigit*. The first character
shall not be a *digit*. The implementation may ignore distinctions of
alphabetical case.

A `#include` preprocessing directive may appear in a source file that
has been read because of a `#include` directive in another file, up to
an *implementation-defined* nesting limit.

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

This illustrates macro-replaced `#include` directives:

``` cpp
#if VERSION == 1
    #define INCFILE  "vers1.h"
#elif VERSION == 2
    #define INCFILE  "vers2.h"   // and so on
#else
    #define INCFILE  "versN.h"
#endif
#include INCFILE
```

## Macro replacement <a id="cpp.replace">[[cpp.replace]]</a>

Two replacement lists are identical if and only if the preprocessing
tokens in both have the same number, ordering, spelling, and white-space
separation, where all white-space separations are considered identical.

An identifier currently defined as an *object-like* macro may be
redefined by another `#define` preprocessing directive provided that the
second definition is an object-like macro definition and the two
replacement lists are identical, otherwise the program is ill-formed.
Likewise, an identifier currently defined as a *function-like* macro may
be redefined by another `#define` preprocessing directive provided that
the second definition is a function-like macro definition that has the
same number and spelling of parameters, and the two replacement lists
are identical, otherwise the program is ill-formed.

There shall be white-space between the identifier and the replacement
list in the definition of an object-like macro.

If the identifier-list in the macro definition does not end with an
ellipsis, the number of arguments (including those arguments consisting
of no preprocessing tokens) in an invocation of a function-like macro
shall equal the number of parameters in the macro definition. Otherwise,
there shall be more arguments in the invocation than there are
parameters in the macro definition (excluding the `...`). There shall
exist a `)` preprocessing token that terminates the invocation.

The identifier `__VA_ARGS__` shall occur only in the replacement-list of
a function-like macro that uses the ellipsis notation in the parameters.

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
the macro name[^8] to be replaced by the replacement list of
preprocessing tokens that constitute the remainder of the directive.[^9]
The replacement list is then rescanned for more macro names as specified
below.

A preprocessing directive of the form

``` bnf
'# define' identifier lparen identifier-list\terminal ₒₚₜ{)} replacement-list new-line
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
act as preprocessing directives,[^10] the behavior is undefined.

If there is a `...` immediately preceding the `)` in the function-like
macro definition, then the trailing arguments, including any separating
comma preprocessing tokens, are merged to form a single item: the
*variable arguments*. The number of arguments so combined is such that,
following merger, the number of arguments is one more than the number of
parameters in the macro definition (excluding the `...`).

### Argument substitution <a id="cpp.subst">[[cpp.subst]]</a>

After the arguments for the invocation of a function-like macro have
been identified, argument substitution takes place. A parameter in the
replacement list, unless preceded by a `#` or `##` preprocessing token
or followed by a `##` preprocessing token (see below), is replaced by
the corresponding argument after all macros contained therein have been
expanded. Before being substituted, each argument’s preprocessing tokens
are completely macro replaced as if they formed the rest of the
preprocessing file; no other preprocessing tokens are available.

An identifier `__VA_ARGS__` that occurs in the replacement list shall be
treated as if it were a parameter, and the variable arguments shall form
the preprocessing tokens used to replace it.

### The `#` operator <a id="cpp.stringize">[[cpp.stringize]]</a>

Each `#` preprocessing token in the replacement list for a function-like
macro shall be followed by a parameter as the next preprocessing token
in the replacement list.

A *character string literal* is a *string-literal* with no prefix. If,
in the replacement list, a parameter is immediately preceded by a `#`
preprocessing token, both are replaced by a single character string
literal preprocessing token that contains the spelling of the
preprocessing token sequence for the corresponding argument. Each
occurrence of white space between the argument’s preprocessing tokens
becomes a single space character in the character string literal. White
space before the first preprocessing token and after the last
preprocessing token comprising the argument is deleted. Otherwise, the
original spelling of each preprocessing token in the argument is
retained in the character string literal, except for special handling
for producing the spelling of string literals and character literals: a
`\` character is inserted before each `"` and `\` character of a
character literal or string literal (including the delimiting `"`
characters). If the replacement that results is not a valid character
string literal, the behavior is undefined. The character string literal
corresponding to an empty argument is `""`. The order of evaluation of
`#` and `##` operators is unspecified.

### The `##` operator <a id="cpp.concat">[[cpp.concat]]</a>

A `##` preprocessing token shall not occur at the beginning or at the
end of a replacement list for either form of macro definition.

If, in the replacement list of a function-like macro, a parameter is
immediately preceded or followed by a `##` preprocessing token, the
parameter is replaced by the corresponding argument’s preprocessing
token sequence; however, if an argument consists of no preprocessing
tokens, the parameter is replaced by a placemarker preprocessing token
instead.[^11]

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

In the following fragment:

``` cpp
#define hash_hash # ## #
#define mkstr(a) # a
#define in_between(a) mkstr(a)
#define join(c, d) in_between(c hash_hash d)
char p[] = join(x, y);          // equivalent to
                                // char p[] = "x ## y";
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

### Rescanning and further replacement <a id="cpp.rescan">[[cpp.rescan]]</a>

After all parameters in the replacement list have been substituted and
`#` and `##` processing has taken place, all placemarker preprocessing
tokens are removed. Then the resulting preprocessing token sequence is
rescanned, along with all subsequent preprocessing tokens of the source
file, for more macro names to replace.

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

The simplest use of this facility is to define a “manifest constant,” as
in

``` cpp
#define TABSIZE 100
int table[TABSIZE];
```

The following defines a function-like macro whose value is the maximum
of its arguments. It has the advantages of working for any compatible
types of the arguments and of generating in-line code without the
overhead of function calling. It has the disadvantages of evaluating one
or the other of its arguments a second time (including side effects) and
generating more code than a function if invoked several times. It also
cannot have its address taken, as it has none.

``` cpp
#define max(a, b) ((a) > (b) ? (a) : (b))
```

The parentheses ensure that the arguments and the resulting expression
are bound properly.

To illustrate the rules for redefinition and reexamination, the sequence

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

To illustrate the rules for creating character string literals and
concatenating tokens, the sequence

``` cpp
#define str(s)      # s
#define xstr(s)     str(s)
#define debug(s, t) printf("x" # s "= %d, x" # t "= %s", \               x ## s, x ## t)
#define INCFILE(n)  vers ## n
#define glue(a, b)  a ## b
#define xglue(a, b) glue(a, b)
#define HIGHLOW     "hello"
#define LOW         LOW ", world"

debug(1, 2);
fputs(str(strncmp("abc\0d", "abc", '\4')  // this goes away
    == 0) str(: \@n), s);
#include xstr(INCFILE(2).h)
glue(HIGH, LOW);
xglue(HIGH, LOW)
```

results in

``` cpp
printf("x" "1" "= %d, x" "2" "= %s", x1, x2);
fputs("strncmp(\"abc\\0d\", \"abc\", '\\4') == 0" ": \@n", s);
#include "vers2.h"    (after macro replacement, before file access)
"hello";
"hello" ", world"
```

or, after concatenation of the character string literals,

``` cpp
printf("x1= %d, x2= %s", x1, x2);
fputs("strncmp(\"abc\\0d\", \"abc\", '\\4') == 0: \@n", s);
#include "vers2.h"    (after macro replacement, before file access)
"hello";
"hello, world"
```

Space around the `#` and `##` tokens in the macro definition is
optional.

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

To demonstrate the redefinition rules, the following sequence is valid.

``` cpp
#define OBJ_LIKE      (1-1)
#define OBJ_LIKE      /* white space */ (1-1) /* other */
#define FUNC_LIKE(a)   ( a )
#define FUNC_LIKE( a )(     /* note the white space */ \                a /* other stuff on this line
                  */ )
```

But the following redefinitions are invalid:

``` cpp
#define OBJ_LIKE    (0)      // different token sequence
#define OBJ_LIKE    (1 - 1)  // different white space
#define FUNC_LIKE(b) ( a )   // different parameter usage
#define FUNC_LIKE(b) ( b )   // different parameter spelling
```

Finally, to show the variable argument list macro facilities:

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

## Line control <a id="cpp.line">[[cpp.line]]</a>

The string literal of a `#line` directive, if present, shall be a
character string literal.

The *line number* of the current source line is one greater than the
number of new-line characters read or introduced in translation phase
1 ([[lex.phases]]) while processing the source file to the current
token.

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
'# line' digit-sequence '"' s-char-sequence\terminal ₒₚₜ{"} new-line
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
'# error' pp-tokensnₒₚₜew-line
```

causes the implementation to produce a diagnostic message that includes
the specified sequence of preprocessing tokens, and renders the program
ill-formed.

## Pragma directive <a id="cpp.pragma">[[cpp.pragma]]</a>

A preprocessing directive of the form

``` bnf
'# pragma' pp-tokensnₒₚₜew-line
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

- **`\texttt{__cplusplus}`**

The name ` __cplusplus` is defined to the value `202302L` when compiling
a C++translation unit.[^12]

- **`__DATE__`**

The date of translation of the source file: a character string literal
of the form `"Mmm dd yyyy"`, where the names of the months are the same
as those generated by the `asctime` function, and the first character of
`dd` is a space character if the value is less than 10. If the date of
translation is not available, an *implementation-defined* valid date
shall be supplied.

- **`__FILE__`**

The presumed name of the current source file (a character string
literal).[^13]

- **`__LINE__`**

The presumed line number (within the current source file) of the current
source line (an integer literal).

 

- **`__STDC_HOSTED__`**

The integer literal `1` if the implementation is a hosted implementation
or the integer literal `0` if it is not.

- **`__TIME__`**

The time of translation of the source file: a character string literal
of the form `"hh:mm:ss"` as in the time generated by the `asctime`
function. If the time of translation is not available, an
*implementation-defined* valid time shall be supplied.

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
the short identifier of that character. The *Unicode required set*
consists of all the characters that are defined by ISO/IEC 10646, along
with all amendments and technical corrigenda as of the specified year
and month.

- **`__STDCPP_STRICT_POINTER_SAFETY__`**

Defined, and has the value integer literal 1, if and only if the
implementation has strict pointer safety (
[[basic.stc.dynamic.safety]]).

- **`__STDCPP_THREADS__`**

Defined, and has the value integer literal 1, if and only if a program
can have more than one thread of execution ([[intro.multithread]]).

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

is processed as follows: The string literal is *destringized* by
deleting the `L` prefix, if present, deleting the leading and trailing
double-quotes, replacing each escape sequence `\"` by a double-quote,
and replacing each escape sequence `\\` by a single backslash. The
resulting sequence of characters is processed through translation phase
3 to produce preprocessing tokens that are executed as if they were the
*pp-tokens* in a pragma directive. The original four preprocessing
tokens in the unary operator expression are removed.

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

<!-- Link reference definitions -->
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[cpp]: #cpp
[cpp.concat]: #cpp.concat
[cpp.cond]: #cpp.cond
[cpp.error]: #cpp.error
[cpp.include]: #cpp.include
[cpp.line]: #cpp.line
[cpp.null]: #cpp.null
[cpp.pragma]: #cpp.pragma
[cpp.pragma.op]: #cpp.pragma.op
[cpp.predefined]: #cpp.predefined
[cpp.replace]: #cpp.replace
[cpp.rescan]: #cpp.rescan
[cpp.scope]: #cpp.scope
[cpp.stringize]: #cpp.stringize
[cpp.subst]: #cpp.subst
[cstdint]: language.md#cstdint
[expr.const]: expr.md#expr.const
[intro.multithread]: intro.md#intro.multithread
[lex.digraph]: lex.md#lex.digraph
[lex.name]: lex.md#lex.name
[lex.phases]: lex.md#lex.phases
[lex.token]: lex.md#lex.token
[support.limits]: language.md#support.limits

[^1]: Thus, preprocessing directives are commonly called “lines.” These
    “lines” have no other syntactic significance, as all white space is
    equivalent except in certain situations during preprocessing (see
    the `#` character string literal creation operator in 
    [[cpp.stringize]], for example).

[^2]: Because the controlling constant expression is evaluated during
    translation phase 4, all identifiers either are or are not macro
    names — there simply are no keywords, enumeration constants, etc.

[^3]: An alternative token ([[lex.digraph]]) is not an identifier, even
    when its spelling consists entirely of letters and underscores.
    Therefore it is not subject to this replacement.

[^4]: Thus on an implementation where `std::numeric_limits<int>::max()`
    is `0x7FFF` and `std::numeric_limits<unsigned int>::max()` is
    `0xFFFF`, the integer literal `0x8000` is signed and positive within
    a `#if` expression even though it is unsigned in translation phase
    7 ([[lex.phases]]).

[^5]: Thus, the constant expression in the following `#if` directive and
    `if` statement is not guaranteed to evaluate to the same value in
    these two contexts.

[^6]: As indicated by the syntax, a preprocessing token shall not follow
    a `#else` or `#endif` directive before the terminating new-line
    character. However, comments may appear anywhere in a source file,
    including within a preprocessing directive.

[^7]: Note that adjacent string literals are not concatenated into a
    single string literal (see the translation phases in 
    [[lex.phases]]); thus, an expansion that results in two string
    literals is an invalid directive.

[^8]: Since, by macro-replacement time, all character literals and
    string literals are preprocessing tokens, not sequences possibly
    containing identifier-like subsequences (see [[lex.phases]],
    translation phases), they are never scanned for macro names or
    parameters.

[^9]: An alternative token ([[lex.digraph]]) is not an identifier, even
    when its spelling consists entirely of letters and underscores.
    Therefore it is not possible to define a macro whose name is the
    same as that of an alternative token.

[^10]: Despite the name, a non-directive is a preprocessing directive.

[^11]: Placemarker preprocessing tokens do not appear in the syntax
    because they are temporary entities that exist only within
    translation phase 4.

[^12]: It is intended that future versions of this standard will replace
    the value of this macro with a greater value. Non-conforming
    compilers should use a value with at most five decimal digits.

[^13]: The presumed source file name and line number can be changed by
    the `#line` directive.
