# Grammar summary (informative) <a id="gram" data-annex="true" data-annex-type="informative">[[gram]]</a>

This summary of C++ grammar is intended to be an aid to comprehension.
It is not an exact statement of the language. In particular, the grammar
described here accepts a superset of valid C++ constructs.
Disambiguation rules ([[stmt.ambig]], [[dcl.spec]],
[[class.member.lookup]]) must be applied to distinguish expressions from
declarations. Further, access control, ambiguity, and type rules must be
used to weed out syntactically valid but meaningless constructs.

## Keywords <a id="gram.key">[[gram.key]]</a>

New context-dependent keywords are introduced into a program by
`typedef` [[dcl.typedef]], `namespace` [[namespace.def]], class
[[class]], enumeration [[dcl.enum]], and `template` [[temp]]
declarations.

``` bnf
typedef-name:
    identifier
    simple-template-id
```

``` bnf
namespace-name:
    identifier
    namespace-alias

namespace-alias:
    identifier
```

``` bnf
class-name:
    identifier
    simple-template-id
```

``` bnf
enum-name:
    identifier
```

``` bnf
template-name:
    identifier
```

<!-- Link reference definitions -->
[class]: class.md#class
[class.member.lookup]: class.md#class.member.lookup
[dcl.enum]: dcl.md#dcl.enum
[dcl.spec]: dcl.md#dcl.spec
[dcl.typedef]: dcl.md#dcl.typedef
[gram]: #gram
[gram.key]: #gram.key
[namespace.def]: dcl.md#namespace.def
[stmt.ambig]: stmt.md#stmt.ambig
[temp]: temp.md#temp

## Lexical conventions <a id="gram.lex">[[gram.lex]]</a>

``` bnf
hex-quad:
    hexadecimal-digit hexadecimal-digit hexadecimal-digit hexadecimal-digit
```

``` bnf
universal-character-name:
    '\u' hex-quad
    '\U' hex-quad hex-quad
```

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
    each non-white-space character that cannot be one of the above
```

``` bnf
token:
    identifier
    keyword
    literal
    operator-or-punctuator
```

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

``` bnf
keyword:
    any identifier listed in [[lex.key]]
    *import-keyword*
    *module-keyword*
    *export-keyword*
```

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
    '{ } [ ] ( )'
    '<: :> <% %> ; : ...'
    '? :: . .* -> ->* ~'
    '! + - * / % ^ & |'
    '= += -= *= /= %= ^= &= |='
    '== != < > <= >= <=> && ||'
    '<< >> <<= >>= ++ -- ,'
    'and or xor not bitand bitor compl'
    'and_eq or_eq xor_eq not_eq'
```

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

``` bnf
integer-literal:
    binary-literal ₒₚₜ {integer-suffix}
    octal-literal ₒₚₜ {integer-suffix}
    decimal-literal ₒₚₜ {integer-suffix}
    hexadecimal-literal ₒₚₜ {integer-suffix}
```

``` bnf
binary-literal:
    '0b' binary-digit
    '0B' binary-digit
    binary-literal ₒₚₜ {'''} binary-digit
```

``` bnf
octal-literal:
    '0'
    octal-literal ₒₚₜ {'''} octal-digit
```

``` bnf
decimal-literal:
    nonzero-digit
    decimal-literal ₒₚₜ {'''} digit
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
    hexadecimal-digit-sequence ₒₚₜ {'''} hexadecimal-digit
```

``` bnf
hexadecimal-digit: one of
    '0 1 2 3 4 5 6 7 8 9'
    'a b c d e f'
    'A B C D E F'
```

``` bnf
integer-suffix:
    unsigned-suffix ₒₚₜ {long-suffix} 
    unsigned-suffix ₒₚₜ {long-long-suffix} 
    long-suffix ₒₚₜ {unsigned-suffix} 
    long-long-suffix ₒₚₜ {unsigned-suffix}
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
character-literal:
    ₒₚₜ {encoding-prefix} ''' c-char-sequence '''
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
c-char:
    any member of the basic source character set except the single-quote ''', backslash '\', or new-line character
    escape-sequence
    universal-character-name
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

``` bnf
floating-point-literal:
    decimal-floating-point-literal
    hexadecimal-floating-point-literal
```

``` bnf
decimal-floating-point-literal:
    fractional-constant ₒₚₜ {exponent-part} ₒₚₜ {floating-point-suffix}
    digit-sequence exponent-part ₒₚₜ {floating-point-suffix}
```

``` bnf
hexadecimal-floating-point-literal:
    hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part ₒₚₜ {floating-point-suffix}
    hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part ₒₚₜ {floating-point-suffix}
```

``` bnf
fractional-constant:
    ₒₚₜ {digit-sequence} '.' digit-sequence
    digit-sequence '.'
```

``` bnf
hexadecimal-fractional-constant:
    ₒₚₜ {hexadecimal-digit-sequence} '.' hexadecimal-digit-sequence
    hexadecimal-digit-sequence '.'
```

``` bnf
exponent-part:
    'e' ₒₚₜ {sign} digit-sequence
    'E' ₒₚₜ {sign} digit-sequence
```

``` bnf
binary-exponent-part:
    'p' ₒₚₜ {sign} digit-sequence
    'P' ₒₚₜ {sign} digit-sequence
```

``` bnf
sign: one of
    '+ -'
```

``` bnf
digit-sequence:
    digit
    digit-sequence ₒₚₜ {'''} digit
```

``` bnf
floating-point-suffix: one of
    'f l F L'
```

``` bnf
string-literal:
    ₒₚₜ {encoding-prefix} '"' ₒₚₜ {s-char-sequence} '"'
    ₒₚₜ {encoding-prefix} 'R' raw-string
```

``` bnf
s-char-sequence:
    s-char
    s-char-sequence s-char
```

``` bnf
s-char:
    any member of the basic source character set except the double-quote '"', backslash '\', or new-line character
    escape-sequence
    universal-character-name
```

``` bnf
raw-string:
    '"' ₒₚₜ {d-char-sequence} '(' ₒₚₜ {r-char-sequence} ')' ₒₚₜ {d-char-sequence} '"'
```

``` bnf
r-char-sequence:
    r-char
    r-char-sequence r-char
```

``` bnf
r-char:
    any member of the source character set, except a right parenthesis ')' followed by
       the initial *d-char-sequence* (which may be empty) followed by a double quote '"'.
```

``` bnf
d-char-sequence:
    d-char
    d-char-sequence d-char
```

``` bnf
d-char:
    any member of the basic source character set except:
       space, the left parenthesis '(', the right parenthesis ')', the backslash '\', and the control characters
       representing horizontal tab, vertical tab, form feed, and newline.
```

``` bnf
boolean-literal:
    'false'
    'true'
```

``` bnf
pointer-literal:
    'nullptr'
```

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
    fractional-constant ₒₚₜ {exponent-part} ud-suffix
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


## Basic concepts <a id="gram.basic">[[gram.basic]]</a>

``` bnf
ₒₚₜ {nested-name-specifier} type-name '::' '~' type-name
```

``` bnf
nested-name-specifier unqualified-id
```

``` bnf
class-key ₒₚₜ {attribute-specifier-seq} identifier ';'
```

``` bnf
class-key ₒₚₜ {attribute-specifier-seq} identifier ';'
```

``` bnf
translation-unit:
    ₒₚₜ {declaration-seq}
    ₒₚₜ {global-module-fragment} module-declaration ₒₚₜ {declaration-seq} ₒₚₜ {private-module-fragment}
```


## Expressions <a id="gram.expr">[[gram.expr]]</a>

``` bnf
primary-expression:
    literal
    this
    '(' expression ')'
    id-expression
    lambda-expression
    fold-expression
    requires-expression
```

``` bnf
id-expression:
    unqualified-id
    qualified-id
```

``` bnf
unqualified-id:
    identifier
    operator-function-id
    conversion-function-id
    literal-operator-id
    '~' type-name
    '~' decltype-specifier
    template-id
```

``` bnf
qualified-id:
    nested-name-specifier ₒₚₜ {template} unqualified-id
```

``` bnf
nested-name-specifier:
    '::'
    type-name '::'
    namespace-name '::'
    decltype-specifier '::'
    nested-name-specifier identifier '::'
    nested-name-specifier ₒₚₜ {template} simple-template-id '::'
```

``` bnf
lambda-expression:
    lambda-introducer ₒₚₜ {lambda-declarator} compound-statement
    lambda-introducer '<' template-parameter-list '>' ₒₚₜ {requires-clause} ₒₚₜ {lambda-declarator} compound-statement
```

``` bnf
lambda-introducer:
    '[' ₒₚₜ {lambda-capture} ']'
```

``` bnf
lambda-declarator:
    '(' parameter-declaration-clause ')' ₒₚₜ {decl-specifier-seq}
       ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq} ₒₚₜ {trailing-return-type} ₒₚₜ {requires-clause}
```

``` bnf
lambda-capture:
    capture-default
    capture-list
    capture-default ',' capture-list
```

``` bnf
capture-default:
    '&'
    '='
```

``` bnf
capture-list:
    capture
    capture-list ',' capture
```

``` bnf
capture:
    simple-capture
    init-capture
```

``` bnf
simple-capture:
    identifier ₒₚₜ {'...'}
    '&' identifier ₒₚₜ {'...'}
    this
    '*' 'this'
```

``` bnf
init-capture:
    ₒₚₜ {'...'} identifier initializer
    '&' ₒₚₜ {'...'} identifier initializer
```

``` bnf
fold-expression:
    '(' cast-expression fold-operator '...' ')'
    '(' '...' fold-operator cast-expression ')'
    '(' cast-expression fold-operator '...' fold-operator cast-expression ')'
```

``` bnf
%% Ed. note: character protrusion would misalign operators with leading `-`.

fold-operator: one of
    '+ ' '- ' '* ' '/ ' '% ' '^ ' '& ' '| ' '<< ' '>> '
    '+=' '-=' '*=' '/=' '%=' '^=' '&=' '|=' '<<=' '>>=' '='
    '==' '!=' '< ' '> ' '<=' '>=' '&&' '||' ', ' '.* ' '->*'
```

``` bnf
requires-expression:
    requires ₒₚₜ {requirement-parameter-list} requirement-body
```

``` bnf
requirement-parameter-list:
    '(' ₒₚₜ {parameter-declaration-clause} ')'
```

``` bnf
requirement-body:
    '{' requirement-seq '}'
```

``` bnf
requirement-seq:
    requirement
    requirement-seq requirement
```

``` bnf
requirement:
    simple-requirement
    type-requirement
    compound-requirement
    nested-requirement
```

``` bnf
simple-requirement:
    expression ';'
```

``` bnf
type-requirement:
    typename ₒₚₜ {nested-name-specifier} type-name ';'
```

``` bnf
compound-requirement:
    '{' expression '}' ₒₚₜ {noexcept} ₒₚₜ {return-type-requirement} ';'
```

``` bnf
return-type-requirement:
    '->' type-constraint
```

``` bnf
nested-requirement:
    requires constraint-expression ';'
```

``` bnf
postfix-expression:
    primary-expression
    postfix-expression '[' expr-or-braced-init-list ']'
    postfix-expression '(' ₒₚₜ {expression-list} ')'
    simple-type-specifier '(' ₒₚₜ {expression-list} ')'
    typename-specifier '(' ₒₚₜ {expression-list} ')'
    simple-type-specifier braced-init-list
    typename-specifier braced-init-list
    postfix-expression ₒₚₜ {'.' 'template'} id-expression
    postfix-expression ₒₚₜ {'->' 'template'} id-expression
    postfix-expression '++'
    postfix-expression '-{-}'
    dynamic_cast '<' type-id '>' '(' expression ')'
    static_cast '<' type-id '>' '(' expression ')'
    reinterpret_cast '<' type-id '>' '(' expression ')'
    const_cast '<' type-id '>' '(' expression ')'
    typeid '(' expression ')'
    typeid '(' type-id ')'
```

``` bnf
expression-list:
    initializer-list
```

``` bnf
unary-expression:
    postfix-expression
    unary-operator cast-expression
    '++' cast-expression
    '-{-}' cast-expression
    await-expression
    sizeof unary-expression
    sizeof '(' type-id ')'
    sizeof '...' '(' identifier ')'
    alignof '(' type-id ')'
    noexcept-expression
    new-expression
    delete-expression
```

``` bnf
unary-operator: one of
    '* & + - ! ~'
```

``` bnf
await-expression:
    'co_await' cast-expression
```

``` bnf
noexcept-expression:
  noexcept '(' expression ')'
```

``` bnf
new-expression:
    ₒₚₜ {'::'} new ₒₚₜ {new-placement} new-type-id ₒₚₜ {new-initializer} 
    ₒₚₜ {'::'} new ₒₚₜ {new-placement} '(' type-id ')' ₒₚₜ {new-initializer}
```

``` bnf
new-placement:
    '(' expression-list ')'
```

``` bnf
new-type-id:
    type-specifier-seq ₒₚₜ {new-declarator}
```

``` bnf
new-declarator:
    ptr-operator ₒₚₜ {new-declarator} 
    noptr-new-declarator
```

``` bnf
noptr-new-declarator:
    '[' ₒₚₜ {expression} ']' ₒₚₜ {attribute-specifier-seq}
    noptr-new-declarator '[' constant-expression ']' ₒₚₜ {attribute-specifier-seq}
```

``` bnf
new-initializer:
    '(' ₒₚₜ {expression-list} ')'
    braced-init-list
```

``` bnf
delete-expression:
    ₒₚₜ {'::'} delete cast-expression
    ₒₚₜ {'::'} delete '[' ']' cast-expression
```

``` bnf
cast-expression:
    unary-expression
    '(' type-id ')' cast-expression
```

``` bnf
pm-expression:
    cast-expression
    pm-expression '.*' cast-expression
    pm-expression '->*' cast-expression
```

``` bnf
multiplicative-expression:
    pm-expression
    multiplicative-expression '*' pm-expression
    multiplicative-expression '/' pm-expression
    multiplicative-expression '%' pm-expression
```

``` bnf
additive-expression:
    multiplicative-expression
    additive-expression '+' multiplicative-expression
    additive-expression '-' multiplicative-expression
```

``` bnf
shift-expression:
    additive-expression
    shift-expression '<<' additive-expression
    shift-expression '>>' additive-expression
```

``` bnf
compare-expression:
    shift-expression
    compare-expression '<=>' shift-expression
```

``` bnf
relational-expression:
    compare-expression
    relational-expression '<' compare-expression
    relational-expression '>' compare-expression
    relational-expression '<=' compare-expression
    relational-expression '>=' compare-expression
```

``` bnf
equality-expression:
    relational-expression
    equality-expression '==' relational-expression
    equality-expression '!=' relational-expression
```

``` bnf
and-expression:
    equality-expression
    and-expression '&' equality-expression
```

``` bnf
exclusive-or-expression:
    and-expression
    exclusive-or-expression '^' and-expression
```

``` bnf
inclusive-or-expression:
    exclusive-or-expression
    inclusive-or-expression '|' exclusive-or-expression
```

``` bnf
logical-and-expression:
    inclusive-or-expression
    logical-and-expression '&&' inclusive-or-expression
```

``` bnf
logical-or-expression:
    logical-and-expression
    logical-or-expression '||' logical-and-expression
```

``` bnf
conditional-expression:
    logical-or-expression
    logical-or-expression '?' expression ':' assignment-expression
```

``` bnf
yield-expression:
  'co_yield' assignment-expression
  'co_yield' braced-init-list
```

``` bnf
throw-expression:
    throw ₒₚₜ {assignment-expression}
```

``` bnf
assignment-expression:
    conditional-expression
    yield-expression
    throw-expression
    logical-or-expression assignment-operator initializer-clause
```

``` bnf
assignment-operator: one of
    '= *= /= %= += -= >>= <<= &= ^= |='
```

``` bnf
expression:
    assignment-expression
    expression ',' assignment-expression
```

``` bnf
constant-expression:
    conditional-expression
```


## Statements <a id="gram.stmt">[[gram.stmt]]</a>

``` bnf
statement:
    labeled-statement
    ₒₚₜ {attribute-specifier-seq} expression-statement
    ₒₚₜ {attribute-specifier-seq} compound-statement
    ₒₚₜ {attribute-specifier-seq} selection-statement
    ₒₚₜ {attribute-specifier-seq} iteration-statement
    ₒₚₜ {attribute-specifier-seq} jump-statement
    declaration-statement
    ₒₚₜ {attribute-specifier-seq} try-block

init-statement:
    expression-statement
    simple-declaration

condition:
    expression
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq declarator brace-or-equal-initializer
```

``` bnf
labeled-statement:
    ₒₚₜ {attribute-specifier-seq} identifier ':' statement
    ₒₚₜ {attribute-specifier-seq} case constant-expression ':' statement
    ₒₚₜ {attribute-specifier-seq} default ':' statement
```

``` bnf
expression-statement:
    ₒₚₜ {expression} ';'
```

``` bnf
compound-statement:
    '{' ₒₚₜ {statement-seq} '}'
```

``` bnf
statement-seq:
    statement
    statement-seq statement
```

``` bnf
selection-statement:
    if ₒₚₜ {constexpr} '(' ₒₚₜ {init-statement} condition ')' statement
    if ₒₚₜ {constexpr} '(' ₒₚₜ {init-statement} condition ')' statement else statement
    switch '(' ₒₚₜ {init-statement} condition ')' statement
```

``` bnf
if ₒₚₜ {constexpr} '(' init-statement condition ')' statement
```

``` bnf
'{'
   init-statement
   if ₒₚₜ {constexpr} '(' condition ')' statement
'}'
```

``` bnf
if ₒₚₜ {constexpr} '(' init-statement condition ')' statement else statement
```

``` bnf
'{'
   init-statement
   if ₒₚₜ {constexpr} '(' condition ')' statement else statement
'}'
```

``` bnf
case constant-expression ':'
```

``` bnf
switch '(' init-statement condition ')' statement
```

``` bnf
'{'
   init-statement
   switch '(' condition ')' statement
'}'
```

``` bnf
iteration-statement:
    while '(' condition ')' statement
    do statement while '(' expression ')' ';'
    for '(' init-statement ₒₚₜ {condition} ';' ₒₚₜ {expression} ')' statement
    for '(' ₒₚₜ {init-statement} for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
for-range-declaration:
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq declarator
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq ₒₚₜ {ref-qualifier} '[' identifier-list ']'
```

``` bnf
for-range-initializer:
    expr-or-braced-init-list
```

``` bnf
label ':'
'{'
   if '(' condition ')' '{'
      statement
      goto label ';'
   '}'
'}'
```

``` bnf
for '(' init-statement ₒₚₜ {condition} ';' ₒₚₜ {expression} ')' statement
```

``` bnf
'{'
   init-statement
   while '(' condition ')' '{'
     statement
     expression ';'
   '}'
'}'
```

``` bnf
for '(' ₒₚₜ {init-statement} for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
'{'
   ₒₚₜ {init-statement}
   auto '&&'range '=' for-range-initializer ';'
   auto begin '=' begin-expr ';'
   auto end '=' end-expr ';'
   for '(' ';' begin '!=' end';' '++'begin ')' '{'
     for-range-declaration '=' '*' begin ';'
     statement
   '}'
'}'
```

``` bnf
jump-statement:
    break ';'
    continue ';'
    return ₒₚₜ {expr-or-braced-init-list} ';'
    coroutine-return-statement
    goto identifier ';'
```

``` bnf
coroutine-return-statement:
    'co_return' ₒₚₜ {expr-or-braced-init-list} ';'
```

``` bnf
'{' S';' 'goto' final-suspend';' '}'
```

``` bnf
declaration-statement:
    block-declaration
```


## Declarations <a id="gram.dcl">[[gram.dcl]]</a>

``` bnf
declaration-seq:
    declaration
    declaration-seq declaration
```

``` bnf
declaration:
    block-declaration
    nodeclspec-function-declaration
    function-definition
    template-declaration
    deduction-guide
    explicit-instantiation
    explicit-specialization
    export-declaration
    linkage-specification
    namespace-definition
    empty-declaration
    attribute-declaration
    module-import-declaration
```

``` bnf
block-declaration:
    simple-declaration
    asm-declaration
    namespace-alias-definition
    using-declaration
    using-enum-declaration
    using-directive
    static_assert-declaration
    alias-declaration
    opaque-enum-declaration
```

``` bnf
nodeclspec-function-declaration:
    ₒₚₜ {attribute-specifier-seq} declarator ';'
```

``` bnf
alias-declaration:
    using identifier ₒₚₜ {attribute-specifier-seq} '=' defining-type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seq ₒₚₜ {init-declarator-list} ';'
    attribute-specifier-seq decl-specifier-seq init-declarator-list ';'
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq ₒₚₜ {ref-qualifier} '[' identifier-list ']' initializer ';'
```

``` bnf
static_assert-declaration:
  static_assert '(' constant-expression ')' ';'
  static_assert '(' constant-expression ',' string-literal ')' ';'
```

``` bnf
empty-declaration:
    ';'
```

``` bnf
attribute-declaration:
    attribute-specifier-seq ';'
```

``` bnf
ₒₚₜ {attribute-specifier-seq} ₒₚₜ {decl-specifier-seq} ₒₚₜ {init-declarator-list} ';'
```

``` bnf
decl-specifier:
    storage-class-specifier
    defining-type-specifier
    function-specifier
    friend
    typedef
    constexpr
    consteval
    constinit
    inline
```

``` bnf
decl-specifier-seq:
    decl-specifier ₒₚₜ {attribute-specifier-seq}
    decl-specifier decl-specifier-seq
```

``` bnf
storage-class-specifier:
    static
    thread_local
    extern
    mutable
```

``` bnf
function-specifier:
    virtual
    explicit-specifier
```

``` bnf
explicit-specifier:
    explicit '(' constant-expression ')'
    explicit
```

``` bnf
typedef-name:
    identifier
    simple-template-id
```

``` bnf
type-specifier:
  simple-type-specifier
  elaborated-type-specifier
  typename-specifier
  cv-qualifier
```

``` bnf
type-specifier-seq:
    type-specifier ₒₚₜ {attribute-specifier-seq}
    type-specifier type-specifier-seq
```

``` bnf
defining-type-specifier:
    type-specifier
    class-specifier
    enum-specifier
```

``` bnf
defining-type-specifier-seq:
  defining-type-specifier ₒₚₜ {attribute-specifier-seq}
  defining-type-specifier defining-type-specifier-seq
```

``` bnf
simple-type-specifier:
    ₒₚₜ {nested-name-specifier} type-name
    nested-name-specifier template simple-template-id
    decltype-specifier
    placeholder-type-specifier
    ₒₚₜ {nested-name-specifier} template-name
    char
    char8_t
    char16_t
    char32_t
    wchar_t
    bool
    short
    int
    long
    signed
    unsigned
    float
    double
    void
```

``` bnf
type-name:
    class-name
    enum-name
    typedef-name
```

``` bnf
ₒₚₜ {typename} ₒₚₜ {nested-name-specifier} ₒₚₜ {template} simple-template-id
```

``` bnf
elaborated-type-specifier:
    class-key ₒₚₜ {attribute-specifier-seq} ₒₚₜ {nested-name-specifier} identifier
    class-key simple-template-id
    class-key nested-name-specifier ₒₚₜ {template} simple-template-id
    elaborated-enum-specifier
```

``` bnf
elaborated-enum-specifier:
    enum ₒₚₜ {nested-name-specifier} identifier
```

``` bnf
class-key ₒₚₜ {attribute-specifier-seq} identifier ';'
friend class-key 'ₒₚₜ {::}' identifier ';'
friend class-key 'ₒₚₜ {::}' simple-template-id ';'
friend class-key nested-name-specifier identifier ';'
friend class-key nested-name-specifier ₒₚₜ {template} simple-template-id ';'
```

``` bnf
decltype-specifier:
  decltype '(' expression ')'
```

``` bnf
placeholder-type-specifier:
  ₒₚₜ {type-constraint} auto
  ₒₚₜ {type-constraint} decltype '(' auto ')'
```

``` bnf
init-declarator-list:
    init-declarator
    init-declarator-list ',' init-declarator
```

``` bnf
init-declarator:
    declarator ₒₚₜ {initializer}
    declarator requires-clause
```

``` bnf
declarator:
    ptr-declarator
    noptr-declarator parameters-and-qualifiers trailing-return-type
```

``` bnf
ptr-declarator:
    noptr-declarator
    ptr-operator ptr-declarator
```

``` bnf
noptr-declarator:
    declarator-id ₒₚₜ {attribute-specifier-seq}
    noptr-declarator parameters-and-qualifiers
    noptr-declarator '[' ₒₚₜ {constant-expression} ']' ₒₚₜ {attribute-specifier-seq}
    '(' ptr-declarator ')'
```

``` bnf
parameters-and-qualifiers:
    '(' parameter-declaration-clause ')' ₒₚₜ {cv-qualifier-seq}
       ₒₚₜ {ref-qualifier} ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq}
```

``` bnf
trailing-return-type:
    '->' type-id
```

``` bnf
ptr-operator:
    '*' ₒₚₜ {attribute-specifier-seq} ₒₚₜ {cv-qualifier-seq}
    '&' ₒₚₜ {attribute-specifier-seq}
    '&&' ₒₚₜ {attribute-specifier-seq}
    nested-name-specifier '*' ₒₚₜ {attribute-specifier-seq} ₒₚₜ {cv-qualifier-seq}
```

``` bnf
cv-qualifier-seq:
    cv-qualifier ₒₚₜ {cv-qualifier-seq}
```

``` bnf
cv-qualifier:
    const
    volatile
```

``` bnf
ref-qualifier:
    '&'
    '&&'
```

``` bnf
declarator-id:
    ₒₚₜ {'...'} id-expression
```

``` bnf
type-id:
    type-specifier-seq ₒₚₜ {abstract-declarator}
```

``` bnf
defining-type-id:
    defining-type-specifier-seq ₒₚₜ {abstract-declarator}
```

``` bnf
abstract-declarator:
    ptr-abstract-declarator
    ₒₚₜ {noptr-abstract-declarator} parameters-and-qualifiers trailing-return-type
    abstract-pack-declarator
```

``` bnf
ptr-abstract-declarator:
    noptr-abstract-declarator
    ptr-operator ₒₚₜ {ptr-abstract-declarator}
```

``` bnf
noptr-abstract-declarator:
    ₒₚₜ {noptr-abstract-declarator} parameters-and-qualifiers
    ₒₚₜ {noptr-abstract-declarator} '[' ₒₚₜ {constant-expression} ']' ₒₚₜ {attribute-specifier-seq}
    '(' ptr-abstract-declarator ')'
```

``` bnf
abstract-pack-declarator:
    noptr-abstract-pack-declarator
    ptr-operator abstract-pack-declarator
```

``` bnf
noptr-abstract-pack-declarator:
    noptr-abstract-pack-declarator parameters-and-qualifiers
    noptr-abstract-pack-declarator '[' ₒₚₜ {constant-expression} ']' ₒₚₜ {attribute-specifier-seq}
    '...'
```

``` bnf
'(' 'D1' ')'
```

``` bnf
'*' ₒₚₜ {attribute-specifier-seq} ₒₚₜ {cv-qualifier-seq} 'D1'
```

``` bnf
'&' ₒₚₜ {attribute-specifier-seq} 'D1'
'&&' ₒₚₜ {attribute-specifier-seq} 'D1'
```

``` bnf
nested-name-specifier '*' ₒₚₜ {attribute-specifier-seq} ₒₚₜ {cv-qualifier-seq} 'D1'
```

``` bnf
'D1' '[' ₒₚₜ {constant-expression} ']' ₒₚₜ {attribute-specifier-seq}
```

``` bnf
'D1 [ ]' ₒₚₜ {attribute-specifier-seq}
```

``` bnf
'D1' '(' parameter-declaration-clause ')' ₒₚₜ {cv-qualifier-seq}
   ₒₚₜ {ref-qualifier} ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq}
```

``` bnf
'D1' '(' parameter-declaration-clause ')' ₒₚₜ {cv-qualifier-seq}
   ₒₚₜ {ref-qualifier} ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq} trailing-return-type
```

``` bnf
parameter-declaration-clause:
    ₒₚₜ {parameter-declaration-list} ₒₚₜ {'...'}
    parameter-declaration-list ',' '...'
```

``` bnf
parameter-declaration-list:
    parameter-declaration
    parameter-declaration-list ',' parameter-declaration
```

``` bnf
parameter-declaration:
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq declarator
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq declarator '=' initializer-clause
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq ₒₚₜ {abstract-declarator}
    ₒₚₜ {attribute-specifier-seq} decl-specifier-seq ₒₚₜ {abstract-declarator} '=' initializer-clause
```

``` bnf
initializer:
    brace-or-equal-initializer
    '(' expression-list ')'
```

``` bnf
brace-or-equal-initializer:
    '=' initializer-clause
    braced-init-list
```

``` bnf
initializer-clause:
    assignment-expression
    braced-init-list
```

``` bnf
braced-init-list:
    '{' initializer-list ₒₚₜ {','} '}'
    '{' designated-initializer-list ₒₚₜ {','} '}'
    '{' '}'
```

``` bnf
initializer-list:
    initializer-clause ₒₚₜ {'...'}
    initializer-list ',' initializer-clause ₒₚₜ {'...'}
```

``` bnf
designated-initializer-list:
    designated-initializer-clause
    designated-initializer-list ',' designated-initializer-clause
```

``` bnf
designated-initializer-clause:
    designator brace-or-equal-initializer
```

``` bnf
designator:
    '.' identifier
```

``` bnf
expr-or-braced-init-list:
    expression
    braced-init-list
```

``` bnf
function-definition:
    ₒₚₜ {attribute-specifier-seq} ₒₚₜ {decl-specifier-seq} declarator ₒₚₜ {virt-specifier-seq} function-body
    ₒₚₜ {attribute-specifier-seq} ₒₚₜ {decl-specifier-seq} declarator requires-clause function-body
```

``` bnf
function-body:
    ₒₚₜ {ctor-initializer} compound-statement
    function-try-block
    '=' default ';'
    '=' delete ';'
```

``` bnf
'{'
   *promise-type* promise *promise-constructor-arguments* ';'
% FIXME: promise'.get_return_object()' ';'
% ... except that it's not a discarded-value expression
   'try' '{'
     'co_await' 'promise.initial_suspend()' ';'
     function-body
   '} catch ( ... ) {'
     'if (!initial-await-resume-called)'
       'throw' ';'
     'promise.unhandled_exception()' ';'
   '}'
final-suspend ':'
   'co_await' 'promise.final_suspend()' ';'
'}'
```

``` bnf
ₒₚₜ {attribute-specifier-seq} *S* cv 'A' e ';'
```

``` bnf
ₒₚₜ {attribute-specifier-seq} decl-specifier-seq ₒₚₜ {ref-qualifier} e initializer ';'
```

``` bnf
*S* 'Uᵢ rᵢ =' initializer ';'
```

``` bnf
enum-name:
    identifier
```

``` bnf
enum-specifier:
    enum-head '{' ₒₚₜ {enumerator-list} '}'
    enum-head '{' enumerator-list ',' '}'
```

``` bnf
enum-head:
    enum-key ₒₚₜ {attribute-specifier-seq} ₒₚₜ {enum-head-name} ₒₚₜ {enum-base}
```

``` bnf
enum-head-name:
    ₒₚₜ {nested-name-specifier} identifier
```

``` bnf
opaque-enum-declaration:
    enum-key ₒₚₜ {attribute-specifier-seq} enum-head-name ₒₚₜ {enum-base} ';'
```

``` bnf
enum-key:
    enum
    enum class
    enum struct
```

``` bnf
enum-base:
    ':' type-specifier-seq
```

``` bnf
enumerator-list:
    enumerator-definition
    enumerator-list ',' enumerator-definition
```

``` bnf
enumerator-definition:
    enumerator
    enumerator '=' constant-expression
```

``` bnf
enumerator:
    identifier ₒₚₜ {attribute-specifier-seq}
```

``` bnf
using-enum-declaration:
    'using' elaborated-enum-specifier ';'
```

``` bnf
namespace-name:
        identifier
        namespace-alias
```

``` bnf
namespace-definition:
        named-namespace-definition
        unnamed-namespace-definition
        nested-namespace-definition
```

``` bnf
named-namespace-definition:
        ₒₚₜ {inline} namespace ₒₚₜ {attribute-specifier-seq} identifier '{' namespace-body '}'
```

``` bnf
unnamed-namespace-definition:
        ₒₚₜ {inline} namespace ₒₚₜ {attribute-specifier-seq} '{' namespace-body '}'
```

``` bnf
nested-namespace-definition:
        namespace enclosing-namespace-specifier '::' ₒₚₜ {inline} identifier '{' namespace-body '}'
```

``` bnf
enclosing-namespace-specifier:
        identifier
        enclosing-namespace-specifier '::' ₒₚₜ {inline} identifier
```

``` bnf
namespace-body:
        ₒₚₜ {declaration-seq}
```

``` bnf
ₒₚₜ {inline} namespace unique '{' '/* empty body */' '}'
using namespace unique ';'
namespace unique '{' namespace-body '}'
```

``` bnf
namespace-alias:
        identifier
```

``` bnf
namespace-alias-definition:
        namespace identifier '=' qualified-namespace-specifier ';'
```

``` bnf
qualified-namespace-specifier:
    ₒₚₜ {nested-name-specifier} namespace-name
```

``` bnf
using-directive:
    ₒₚₜ {attribute-specifier-seq} using namespace ₒₚₜ {nested-name-specifier} namespace-name ';'
```

``` bnf
using-declaration:
    using using-declarator-list ';'
```

``` bnf
using-declarator-list:
    using-declarator ₒₚₜ {'...'}
    using-declarator-list ',' using-declarator ₒₚₜ {'...'}
```

``` bnf
using-declarator:
    ₒₚₜ {typename} nested-name-specifier unqualified-id
```

``` bnf
asm-declaration:
    ₒₚₜ {attribute-specifier-seq} asm '(' string-literal ')' ';'
```

``` bnf
linkage-specification:
    extern string-literal '{' ₒₚₜ {declaration-seq} '}'
    extern string-literal declaration
```

``` bnf
attribute-specifier-seq:
  ₒₚₜ {attribute-specifier-seq} attribute-specifier
```

``` bnf
attribute-specifier:
  '[' '[' ₒₚₜ {attribute-using-prefix} attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  alignas '(' type-id ₒₚₜ {'...'} ')'
  alignas '(' constant-expression ₒₚₜ {'...'} ')'
```

``` bnf
attribute-using-prefix:
  using attribute-namespace ':'
```

``` bnf
attribute-list:
  ₒₚₜ {attribute}
  attribute-list ',' ₒₚₜ {attribute}
  attribute '...'
  attribute-list ',' attribute '...'
```

``` bnf
attribute:
    attribute-token ₒₚₜ {attribute-argument-clause}
```

``` bnf
attribute-token:
    identifier
    attribute-scoped-token
```

``` bnf
attribute-scoped-token:
    attribute-namespace '::' identifier
```

``` bnf
attribute-namespace:
    identifier
```

``` bnf
attribute-argument-clause:
    '(' ₒₚₜ {balanced-token-seq} ')'
```

``` bnf
balanced-token-seq:
    balanced-token
    balanced-token-seq balanced-token
```

``` bnf
balanced-token:
    '(' ₒₚₜ {balanced-token-seq} ')'
    '[' ₒₚₜ {balanced-token-seq} ']'
    '{' ₒₚₜ {balanced-token-seq} '}'
    any *token* other than a parenthesis, a bracket, or a brace
```

``` bnf
'(' string-literal ')'
```

``` bnf
'(' string-literal ')'
```


## Classes <a id="gram.class">[[gram.class]]</a>

``` bnf
class-name:
    identifier
    simple-template-id
```

``` bnf
class-specifier:
    class-head '{' ₒₚₜ {member-specification} '}'
```

``` bnf
class-head:
    class-key ₒₚₜ {attribute-specifier-seq} class-head-name ₒₚₜ {class-virt-specifier} ₒₚₜ {base-clause}
    class-key ₒₚₜ {attribute-specifier-seq} ₒₚₜ {base-clause}
```

``` bnf
class-head-name:
    ₒₚₜ {nested-name-specifier} class-name
```

``` bnf
class-virt-specifier:
    final
```

``` bnf
class-key:
    class
    struct
    union
```

``` bnf
member-specification:
    member-declaration ₒₚₜ {member-specification}
    access-specifier ':' ₒₚₜ {member-specification}
```

``` bnf
member-declaration:
    ₒₚₜ {attribute-specifier-seq} ₒₚₜ {decl-specifier-seq} ₒₚₜ {member-declarator-list} ';'
    function-definition
    using-declaration
    using-enum-declaration
    static_assert-declaration
    template-declaration
    explicit-specialization
    deduction-guide
    alias-declaration
    opaque-enum-declaration
    empty-declaration
```

``` bnf
member-declarator-list:
    member-declarator
    member-declarator-list ',' member-declarator
```

``` bnf
member-declarator:
    declarator ₒₚₜ {virt-specifier-seq} ₒₚₜ {pure-specifier}
    declarator requires-clause
    declarator ₒₚₜ {brace-or-equal-initializer}
    ₒₚₜ {identifier} ₒₚₜ {attribute-specifier-seq} ':' constant-expression ₒₚₜ {brace-or-equal-initializer}
```

``` bnf
virt-specifier-seq:
    virt-specifier
    virt-specifier-seq virt-specifier
```

``` bnf
virt-specifier:
    override
    final
```

``` bnf
pure-specifier:
    '=' '0'
```

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq}
```

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq}
```

``` bnf
conversion-function-id:
    operator conversion-type-id
```

``` bnf
conversion-type-id:
    type-specifier-seq ₒₚₜ {conversion-declarator}
```

``` bnf
conversion-declarator:
    ptr-operator ₒₚₜ {conversion-declarator}
```

``` bnf
ₒₚₜ {identifier} ₒₚₜ {attribute-specifier-seq} ':' constant-expression ₒₚₜ {brace-or-equal-initializer}
```

``` bnf
union '{' member-specification '}' ';'
```

``` bnf
base-clause:
    ':' base-specifier-list
```

``` bnf
base-specifier-list:
    base-specifier ₒₚₜ {'...'}
    base-specifier-list ',' base-specifier ₒₚₜ {'...'}
```

``` bnf
base-specifier:
    ₒₚₜ {attribute-specifier-seq} class-or-decltype
    ₒₚₜ {attribute-specifier-seq} virtual ₒₚₜ {access-specifier} class-or-decltype
    ₒₚₜ {attribute-specifier-seq} access-specifier ₒₚₜ {virtual} class-or-decltype
```

``` bnf
class-or-decltype:
    ₒₚₜ {nested-name-specifier} type-name
    nested-name-specifier template simple-template-id
    decltype-specifier
```

``` bnf
access-specifier:
    private
    protected
    public
```

``` bnf
access-specifier ':' ₒₚₜ {member-specification}
```

``` bnf
friend elaborated-type-specifier ';'
friend simple-type-specifier ';'
friend typename-specifier ';'
```

``` bnf
ctor-initializer:
    ':' mem-initializer-list
```

``` bnf
mem-initializer-list:
    mem-initializer ₒₚₜ {'...'}
    mem-initializer-list ',' mem-initializer ₒₚₜ {'...'}
```

``` bnf
mem-initializer:
    mem-initializer-id '(' ₒₚₜ {expression-list} ')'
    mem-initializer-id braced-init-list
```

``` bnf
mem-initializer-id:
    class-or-decltype
    identifier
```


## Overloading <a id="gram.over">[[gram.over]]</a>

``` bnf
postfix-expression '(' ₒₚₜ {expression-list} ')'
```

``` bnf
postfix-expression:
    postfix-expression '.' id-expression
    postfix-expression '->' id-expression
    primary-expression
```

``` bnf
operator conversion-type-id '( )' ₒₚₜ {cv-qualifier-seq} ₒₚₜ {ref-qualifier} ₒₚₜ {noexcept-specifier} ₒₚₜ {attribute-specifier-seq} ';'
```

``` bnf
'R' *call-function* '(' conversion-type-id \ %
'F, P₁ a₁, …, Pₙ aₙ)' '{ return F (a₁, …, aₙ); }'
```

``` bnf
ₒₚₜ {typename} ₒₚₜ {nested-name-specifier} ₒₚₜ {template} simple-template-id
```

``` bnf
operator-function-id:
    operator operator
```

``` bnf
%% Ed. note: character protrusion would misalign various operators.
operator: one of
    'new delete new[] delete[] co_await (\rlap{ )} [\rlap{ ]} -> ->*'
    '~ ! + - * / % ^ &'
    '| = += -= *= /= %= ^= &='
    '|= == != < > <= >= <=> &&'
    '|| << >> <<= >>= ++ -- ,'
```

``` bnf
'+ - * &'
```

``` bnf
'. .* :: ?:'
```

``` bnf
cast-expression '.' operator '@' '('')'
```

``` bnf
operator '@' '(' cast-expression ')'
```

``` bnf
x '.' operator '@' '(' y ')'
```

``` bnf
operator '@' '(' x ',' y ')'
```

``` bnf
postfix-expression '(' ₒₚₜ {expression-list} ')'
```

``` bnf
postfix-expression '.' operator conversion-type-id '('')' '(' ₒₚₜ {expression-list} ')'
```

``` bnf
postfix-expression '.' operator '('')' '(' ₒₚₜ {expression-list} ')'
```

``` bnf
postfix-expression '[' expr-or-braced-init-list ']'
```

``` bnf
postfix-expression . operator '['']' '(' expr-or-braced-init-list ')'
```

``` bnf
postfix-expression '->' ₒₚₜ {template} id-expression
```

``` bnf
'(' postfix-expression . operator '->' '('')' ')' '->' ₒₚₜ {template} id-expression
```

``` bnf
literal-operator-id:
    operator string-literal identifier
    operator user-defined-string-literal
```


## Templates <a id="gram.temp">[[gram.temp]]</a>

``` bnf
template-declaration:
  template-head declaration
  template-head concept-definition
```

``` bnf
template-head:
  template '<' template-parameter-list '>' ₒₚₜ {requires-clause}
```

``` bnf
template-parameter-list:
  template-parameter
  template-parameter-list ',' template-parameter
```

``` bnf
requires-clause:
  requires constraint-logical-or-expression
```

``` bnf
constraint-logical-or-expression:
  constraint-logical-and-expression
  constraint-logical-or-expression '||' constraint-logical-and-expression
```

``` bnf
constraint-logical-and-expression:
  primary-expression
  constraint-logical-and-expression '&&' primary-expression
```

``` bnf
template-parameter:
  type-parameter
  parameter-declaration
```

``` bnf
type-parameter:
  type-parameter-key ₒₚₜ {'...'} ₒₚₜ {identifier}
  type-parameter-key ₒₚₜ {identifier} '=' type-id
  type-constraint ₒₚₜ {'...'} ₒₚₜ {identifier}
  type-constraint ₒₚₜ {identifier} '=' type-id
  template-head type-parameter-key ₒₚₜ {'...'} ₒₚₜ {identifier}
  template-head type-parameter-key ₒₚₜ {identifier} '=' id-expression
```

``` bnf
type-parameter-key:
  class
  typename
```

``` bnf
type-constraint:
  ₒₚₜ {nested-name-specifier} concept-name
  ₒₚₜ {nested-name-specifier} concept-name '<' ₒₚₜ {template-argument-list} '>'
```

``` bnf
simple-template-id:
  template-name '<' ₒₚₜ {template-argument-list} '>'
```

``` bnf
template-id:
  simple-template-id
  operator-function-id '<' ₒₚₜ {template-argument-list} '>'
  literal-operator-id '<' ₒₚₜ {template-argument-list} '>'
```

``` bnf
template-name:
  identifier
```

``` bnf
template-argument-list:
  template-argument ₒₚₜ {'...'}
  template-argument-list ',' template-argument ₒₚₜ {'...'}
```

``` bnf
template-argument:
  constant-expression
  type-id
  id-expression
```

``` bnf
constraint-expression:
    logical-or-expression
```

``` bnf
deduction-guide:
    ₒₚₜ {explicit-specifier} template-name '(' parameter-declaration-clause ')' '->' simple-template-id ';'
```

``` bnf
concept-definition:
  concept concept-name '=' constraint-expression ';'
```

``` bnf
concept-name:
  identifier
```

``` bnf
typename-specifier:
  typename nested-name-specifier identifier
  typename nested-name-specifier 'ₒₚₜ {template}' simple-template-id
```

``` bnf
postfix-expression '(' ₒₚₜ {expression-list} ')'
```

``` bnf
simple-type-specifier '(' ₒₚₜ {expression-list} ')'
ₒₚₜ {'::'} new ₒₚₜ {new-placement} new-type-id ₒₚₜ {new-initializer}
ₒₚₜ {'::'} new ₒₚₜ {new-placement} '(' type-id ')' ₒₚₜ {new-initializer}
dynamic_cast '<' type-id '>' '(' expression ')'
static_cast '<' type-id '>' '(' expression ')'
const_cast '<' type-id '>' '(' expression ')'
reinterpret_cast '<' type-id '>' '(' expression ')'
'(' type-id ')' cast-expression
```

``` bnf
literal
sizeof unary-expression
sizeof '(' type-id ')'
sizeof '...' '(' identifier ')'
alignof '(' type-id ')'
typeid '(' expression ')'
typeid '(' type-id ')'
ₒₚₜ {'::'} delete cast-expression
ₒₚₜ {'::'} delete '[' ']' cast-expression
throw ₒₚₜ {assignment-expression}
noexcept '(' expression ')'
```

``` bnf
sizeof unary-expression
sizeof '(' type-id ')'
typeid '(' expression ')'
typeid '(' type-id ')'
alignof '(' type-id ')'
noexcept '(' expression ')'
```

``` bnf
simple-type-specifier '(' ₒₚₜ {expression-list} ')'
static_cast '<' type-id '>' '(' expression ')'
const_cast '<' type-id '>' '(' expression ')'
reinterpret_cast '<' type-id '>' '(' expression ')'
'(' type-id ')' cast-expression
```

``` bnf
sizeof '...' '(' identifier ')'
fold-expression
```

``` bnf
explicit-instantiation:
  ₒₚₜ {extern} template declaration
```

``` bnf
explicit-specialization:
  template '<' '>' declaration
```


## Preprocessing directives <a id="gram.cpp">[[gram.cpp]]</a>

``` bnf
preprocessing-file:
    ₒₚₜ {group}
    module-file
```

``` bnf
module-file:
    ₒₚₜ {pp-global-module-fragment} pp-module ₒₚₜ {group} ₒₚₜ {pp-private-module-fragment}
```

``` bnf
pp-global-module-fragment:
    module ';' new-line ₒₚₜ {group}
```

``` bnf
pp-private-module-fragment:
    module ':' private ';' new-line ₒₚₜ {group}
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
    '# define ' identifier lparen ₒₚₜ {identifier-list} ')' replacement-list new-line
    '# define ' identifier lparen '... )' replacement-list new-line
    '# define ' identifier lparen identifier-list ', ... )' replacement-list new-line
    '# undef ' identifier new-line
    '# line ' pp-tokens new-line
    '# error ' ₒₚₜ {pp-tokens} new-line
    '# pragma ' ₒₚₜ {pp-tokens} new-line
    '# 'new-line
```

``` bnf
if-section:
    if-group ₒₚₜ {elif-groups} ₒₚₜ {else-group} endif-line
```

``` bnf
if-group:
    '# if ' constant-expression new-line ₒₚₜ {group}
    '# ifdef ' identifier new-line ₒₚₜ {group}
    '# ifndef ' identifier new-line ₒₚₜ {group}
```

``` bnf
elif-groups:
    elif-group
    elif-groups elif-group
```

``` bnf
elif-group:
    '# elif ' constant-expression new-line ₒₚₜ {group}
```

``` bnf
else-group:
    '# else ' new-line ₒₚₜ {group}
```

``` bnf
endif-line:
    '# endif ' new-line
```

``` bnf
text-line:
    ₒₚₜ {pp-tokens} new-line
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
    ₒₚₜ {pp-tokens}
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

``` bnf
'# if ' constant-expression new-line ₒₚₜ {group}
'# elif ' constant-expression new-line ₒₚₜ {group}
```

``` bnf
'# ifdef ' identifier new-line ₒₚₜ {group}
'# ifndef ' identifier new-line ₒₚₜ {group}
```

``` bnf
'# include <' h-char-sequence '>' new-line
```

``` bnf
'# include "' q-char-sequence '"' new-line
```

``` bnf
'# include <' h-char-sequence '>' new-line
```

``` bnf
'# include' pp-tokens new-line
```

``` bnf
'import' header-name ';' new-line
```

``` bnf
pp-module:
    ₒₚₜ {export} module ₒₚₜ {pp-tokens} ';' new-line
```

``` bnf
pp-import:
    ₒₚₜ {export} import header-name ₒₚₜ {pp-tokens} ';' new-line
    ₒₚₜ {export} import header-name-tokens ₒₚₜ {pp-tokens} ';' new-line
    ₒₚₜ {export} import pp-tokens ';' new-line
```

``` bnf
'# define' identifier replacement-list new-line
```

``` bnf
'# define' identifier lparen ₒₚₜ {identifier-list} ')' replacement-list new-line
'# define' identifier lparen '...' ')' replacement-list new-line
'# define' identifier lparen identifier-list ', ...' ')' replacement-list new-line
```

``` bnf
va-opt-replacement:
    '__VA_OPT__ (' ₒₚₜ {pp-tokens} ')'
```

``` bnf
'# undef' identifier new-line
```

``` bnf
'# line' digit-sequence new-line
```

``` bnf
'# line' digit-sequence '"' ₒₚₜ {s-char-sequence} '"' new-line
```

``` bnf
'# line' pp-tokens new-line
```

``` bnf
'# error' ₒₚₜ {pp-tokens} new-line
```

``` bnf
'# pragma' ₒₚₜ {pp-tokens} new-line
```

``` bnf
'#' new-line
```

``` bnf
'_Pragma' '(' string-literal ')'
```


## Exception handling <a id="gram.except">[[gram.except]]</a>

``` bnf
try-block:
    'try' compound-statement handler-seq
```

``` bnf
function-try-block:
    'try' ₒₚₜ {ctor-initializer} compound-statement handler-seq
```

``` bnf
handler-seq:
    handler ₒₚₜ {handler-seq}
```

``` bnf
handler:
    'catch' '(' exception-declaration ')' compound-statement
```

``` bnf
exception-declaration:
    ₒₚₜ {attribute-specifier-seq} type-specifier-seq declarator
    ₒₚₜ {attribute-specifier-seq} type-specifier-seq ₒₚₜ {abstract-declarator}
    '...'
```

``` bnf
noexcept-specifier:
    'noexcept' '(' constant-expression ')'
    'noexcept'
```

<!-- Link reference definitions -->
[gram.lex]: #gram.lex
[gram.basic]: #gram.basic
[gram.expr]: #gram.expr
[gram.stmt]: #gram.stmt
[gram.dcl]: #gram.dcl
[gram.class]: #gram.class
[gram.over]: #gram.over
[gram.temp]: #gram.temp
[gram.cpp]: #gram.cpp
[gram.except]: #gram.except
