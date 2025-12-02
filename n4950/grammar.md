# Grammar summary (informative) <a id="gram" data-annex="true" data-annex-type="informative">[[gram]]</a>

## General <a id="gram.general">[[gram.general]]</a>

This summary of C++ grammar is intended to be an aid to comprehension.
It is not an exact statement of the language. In particular, the grammar
described here accepts a superset of valid C++ constructs.
Disambiguation rules
[[stmt.ambig]], [[dcl.spec]], [[class.member.lookup]] are applied to
distinguish expressions from declarations. Further, access control,
ambiguity, and type rules are used to weed out syntactically valid but
meaningless constructs.

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
```

``` bnf
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
[class.member.lookup]: basic.md#class.member.lookup
[dcl.enum]: dcl.md#dcl.enum
[dcl.spec]: dcl.md#dcl.spec
[dcl.typedef]: dcl.md#dcl.typedef
[gram]: #gram
[gram.general]: #gram.general
[gram.key]: #gram.key
[namespace.def]: dcl.md#namespace.def
[stmt.ambig]: stmt.md#stmt.ambig
[temp]: temp.md#temp

## Lexical conventions <a id="gram.lex">[[gram.lex]]</a>

``` bnf
n-char: one of
     any member of the translation character set except the U+007d (right curly bracket) or new-line character
```

``` bnf
n-char-sequence:
    n-char
    n-char-sequence n-char
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
    hexadecimal-digit
    simple-hexadecimal-digit-sequence hexadecimal-digit
```

``` bnf
universal-character-name:
    '\u' hex-quad
    '\U' hex-quad hex-quad
    '\u{' simple-hexadecimal-digit-sequence '}'
    named-universal-character
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
    each non-whitespace character that cannot be one of the above
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
    any member of the translation character set except new-line and U+003e (greater-than sign)
```

``` bnf
q-char-sequence:
    q-char
    q-char-sequence q-char
```

``` bnf
q-char:
    any member of the translation character set except new-line and U+0022 (quotation mark)
```

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
    octal-digit
    simple-octal-digit-sequence octal-digit
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
    r-char
    r-char-sequence r-char
```

``` bnf
r-char:
    any member of the translation character set, except a U+0029 (right parenthesis) followed by
       the initial *d-char-sequence* (which may be empty) followed by a U+0022 (quotation mark)
```

``` bnf
d-char-sequence:
    d-char
    d-char-sequence d-char
```

``` bnf
d-char:
    any member of the basic character set except:
      U+0020 (space), U+0028 (left parenthesis), U+0029 (right parenthesis), U+005c (reverse solidus),
      U+0009 (character tabulation), U+000b (line tabulation), U+000c (form feed), and new-line
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


## Basic concepts <a id="gram.basic">[[gram.basic]]</a>

``` bnf
translation-unit:
    declaration-seqₒₚₜ 
    global-module-fragmentₒₚₜ module-declaration declaration-seqₒₚₜ private-module-fragmentₒₚₜ
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
    nested-name-specifier templateₒₚₜ unqualified-id
```

``` bnf
nested-name-specifier:
    '::'
    type-name '::'
    namespace-name '::'
    decltype-specifier '::'
    nested-name-specifier identifier '::'
    nested-name-specifier templateₒₚₜ simple-template-id '::'
```

``` bnf
lambda-expression:
    lambda-introducer attribute-specifier-seqₒₚₜ lambda-declarator compound-statement
    lambda-introducer '<' template-parameter-list '>' requires-clauseₒₚₜ attribute-specifier-seqₒₚₜ 
       lambda-declarator compound-statement
```

``` bnf
lambda-introducer:
    '[' lambda-captureₒₚₜ ']'
```

``` bnf
lambda-declarator:
    lambda-specifier-seq noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-typeₒₚₜ 
    noexcept-specifier attribute-specifier-seqₒₚₜ trailing-return-typeₒₚₜ 
    trailing-return-typeₒₚₜ 
    '(' parameter-declaration-clause ')' lambda-specifier-seqₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ 
       trailing-return-typeₒₚₜ requires-clauseₒₚₜ
```

``` bnf
lambda-specifier:
    consteval
    constexpr
    mutable
    static
```

``` bnf
lambda-specifier-seq:
    lambda-specifier
    lambda-specifier lambda-specifier-seq
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
    identifier '...'ₒₚₜ 
    '&' identifier '...'ₒₚₜ 
    this
    '*' 'this'
```

``` bnf
init-capture:
    '...'ₒₚₜ identifier initializer
    '&' '...'ₒₚₜ identifier initializer
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
    requires requirement-parameter-listₒₚₜ requirement-body
```

``` bnf
requirement-parameter-list:
    '(' parameter-declaration-clause ')'
```

``` bnf
requirement-body:
    '{' requirement-seq '}'
```

``` bnf
requirement-seq:
    requirement
    requirement requirement-seq
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
    typename nested-name-specifierₒₚₜ type-name ';'
```

``` bnf
compound-requirement:
    '{' expression '}' noexceptₒₚₜ return-type-requirementₒₚₜ ';'
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
    postfix-expression '[' expression-listₒₚₜ ']'
    postfix-expression '(' expression-listₒₚₜ ')'
    simple-type-specifier '(' expression-listₒₚₜ ')'
    typename-specifier '(' expression-listₒₚₜ ')'
    simple-type-specifier braced-init-list
    typename-specifier braced-init-list
    postfix-expression '.' 'template'ₒₚₜ id-expression
    postfix-expression '->' 'template'ₒₚₜ id-expression
    postfix-expression '++'
    postfix-expression '--'
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
%% Ed. note: character protrusion would misalign operators.

unary-expression:
    postfix-expression
    unary-operator cast-expression
    '++' cast-expression
    '--' cast-expression
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
%% Ed. note: character protrusion would misalign operators.

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
    '::'ₒₚₜ new new-placementₒₚₜ new-type-id new-initializerₒₚₜ 
    '::'ₒₚₜ new new-placementₒₚₜ '(' type-id ')' new-initializerₒₚₜ
```

``` bnf
new-placement:
    '(' expression-list ')'
```

``` bnf
new-type-id:
    type-specifier-seq new-declaratorₒₚₜ
```

``` bnf
new-declarator:
    ptr-operator new-declaratorₒₚₜ 
    noptr-new-declarator
```

``` bnf
noptr-new-declarator:
    '[' expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ 
    noptr-new-declarator '[' constant-expression ']' attribute-specifier-seqₒₚₜ
```

``` bnf
new-initializer:
    '(' expression-listₒₚₜ ')'
    braced-init-list
```

``` bnf
delete-expression:
    '::'ₒₚₜ delete cast-expression
    '::'ₒₚₜ delete '[' ']' cast-expression
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
    throw assignment-expressionₒₚₜ
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
    attribute-specifier-seqₒₚₜ expression-statement
    attribute-specifier-seqₒₚₜ compound-statement
    attribute-specifier-seqₒₚₜ selection-statement
    attribute-specifier-seqₒₚₜ iteration-statement
    attribute-specifier-seqₒₚₜ jump-statement
    declaration-statement
    attribute-specifier-seqₒₚₜ try-block
```

``` bnf
init-statement:
    expression-statement
    simple-declaration
    alias-declaration
```

``` bnf
condition:
    expression
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator brace-or-equal-initializer
```

``` bnf
label:
    attribute-specifier-seqₒₚₜ identifier ':'
    attribute-specifier-seqₒₚₜ case constant-expression ':'
    attribute-specifier-seqₒₚₜ default ':'
```

``` bnf
labeled-statement:
    label statement
```

``` bnf
expression-statement:
    expressionₒₚₜ ';'
```

``` bnf
compound-statement:
    '{' statement-seqₒₚₜ label-seqₒₚₜ '}'
```

``` bnf
statement-seq:
    statement
    statement-seq statement
```

``` bnf
label-seq:
    label
    label-seq label
```

``` bnf
selection-statement:
    if constexprₒₚₜ '(' init-statementₒₚₜ condition ')' statement
    if constexprₒₚₜ '(' init-statementₒₚₜ condition ')' statement else statement
    if '!'ₒₚₜ consteval compound-statement
    if '!'ₒₚₜ consteval compound-statement else statement
    switch '(' init-statementₒₚₜ condition ')' statement
```

``` bnf
if constexprₒₚₜ '(' init-statement condition ')' statement
```

``` bnf
'{'
   init-statement
   if constexprₒₚₜ '(' condition ')' statement
'}'
```

``` bnf
if constexprₒₚₜ '(' init-statement condition ')' statement else statement
```

``` bnf
'{'
   init-statement
   if constexprₒₚₜ '(' condition ')' statement else statement
'}'
```

``` bnf
if '!' consteval compound-statement
```

``` bnf
if consteval '{' '}' else compound-statement
```

``` bnf
if '!' consteval compound-statement₁ else statement₂
```

``` bnf
if consteval statement₂ else compound-statement₁
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
    for '(' init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
    for '(' init-statementₒₚₜ for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
for-range-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator
    attribute-specifier-seqₒₚₜ decl-specifier-seq ref-qualifierₒₚₜ '[' identifier-list ']'
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
for '(' init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
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
for '(' init-statementₒₚₜ for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
'{'
   init-statementₒₚₜ 
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
    return expr-or-braced-init-listₒₚₜ ';'
    coroutine-return-statement
    goto identifier ';'
```

``` bnf
coroutine-return-statement:
    'co_return' expr-or-braced-init-listₒₚₜ ';'
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
    name-declaration
    special-declaration
```

``` bnf
name-declaration:
    block-declaration
    nodeclspec-function-declaration
    function-definition
    template-declaration
    deduction-guide
    linkage-specification
    namespace-definition
    empty-declaration
    attribute-declaration
    module-import-declaration
```

``` bnf
special-declaration:
    explicit-instantiation
    explicit-specialization
    export-declaration
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
    attribute-specifier-seqₒₚₜ declarator ';'
```

``` bnf
alias-declaration:
    using identifier attribute-specifier-seqₒₚₜ '=' defining-type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seq init-declarator-listₒₚₜ ';'
    attribute-specifier-seq decl-specifier-seq init-declarator-list ';'
    attribute-specifier-seqₒₚₜ decl-specifier-seq ref-qualifierₒₚₜ '[' identifier-list ']' initializer ';'
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
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ init-declarator-listₒₚₜ ';'
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
    decl-specifier attribute-specifier-seqₒₚₜ 
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
    type-specifier attribute-specifier-seqₒₚₜ 
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
  defining-type-specifier attribute-specifier-seqₒₚₜ 
  defining-type-specifier defining-type-specifier-seq
```

``` bnf
simple-type-specifier:
    nested-name-specifierₒₚₜ type-name
    nested-name-specifier template simple-template-id
    decltype-specifier
    placeholder-type-specifier
    nested-name-specifierₒₚₜ template-name
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
typenameₒₚₜ nested-name-specifierₒₚₜ templateₒₚₜ simple-template-id
```

``` bnf
elaborated-type-specifier:
    class-key attribute-specifier-seqₒₚₜ nested-name-specifierₒₚₜ identifier
    class-key simple-template-id
    class-key nested-name-specifier templateₒₚₜ simple-template-id
    enum nested-name-specifierₒₚₜ identifier
```

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
class-key attribute-specifier-seqₒₚₜ simple-template-id ';'
```

``` bnf
friend class-key nested-name-specifierₒₚₜ identifier ';'
friend class-key simple-template-id ';'
friend class-key nested-name-specifier templateₒₚₜ simple-template-id ';'
```

``` bnf
decltype-specifier:
  decltype '(' expression ')'
```

``` bnf
placeholder-type-specifier:
  type-constraintₒₚₜ auto
  type-constraintₒₚₜ decltype '(' auto ')'
```

``` bnf
init-declarator-list:
    init-declarator
    init-declarator-list ',' init-declarator
```

``` bnf
init-declarator:
    declarator initializerₒₚₜ 
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
    declarator-id attribute-specifier-seqₒₚₜ 
    noptr-declarator parameters-and-qualifiers
    noptr-declarator '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ 
    '(' ptr-declarator ')'
```

``` bnf
parameters-and-qualifiers:
    '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
      ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
trailing-return-type:
    '->' type-id
```

``` bnf
ptr-operator:
    '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 
    '&' attribute-specifier-seqₒₚₜ 
    '&&' attribute-specifier-seqₒₚₜ 
    nested-name-specifier '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ
```

``` bnf
cv-qualifier-seq:
    cv-qualifier cv-qualifier-seqₒₚₜ
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
    '...'ₒₚₜ id-expression
```

``` bnf
type-id:
    type-specifier-seq abstract-declaratorₒₚₜ
```

``` bnf
defining-type-id:
    defining-type-specifier-seq abstract-declaratorₒₚₜ
```

``` bnf
abstract-declarator:
    ptr-abstract-declarator
    noptr-abstract-declaratorₒₚₜ parameters-and-qualifiers trailing-return-type
    abstract-pack-declarator
```

``` bnf
ptr-abstract-declarator:
    noptr-abstract-declarator
    ptr-operator ptr-abstract-declaratorₒₚₜ
```

``` bnf
noptr-abstract-declarator:
    noptr-abstract-declaratorₒₚₜ parameters-and-qualifiers
    noptr-abstract-declaratorₒₚₜ '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ 
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
    noptr-abstract-pack-declarator '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ 
    '...'
```

``` bnf
'(' 'D1' ')'
```

``` bnf
'*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 'D1'
```

``` bnf
'&' attribute-specifier-seqₒₚₜ 'D1'
'&&' attribute-specifier-seqₒₚₜ 'D1'
```

``` bnf
nested-name-specifier '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 'D1'
```

``` bnf
'D1' '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ
```

``` bnf
'D1 [ ]' attribute-specifier-seqₒₚₜ
```

``` bnf
'D1' '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
  ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
'D1' '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
  ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-type
```

``` bnf
parameter-declaration-clause:
    parameter-declaration-listₒₚₜ '...'ₒₚₜ 
    parameter-declaration-list ',' '...'
```

``` bnf
parameter-declaration-list:
    parameter-declaration
    parameter-declaration-list ',' parameter-declaration
```

``` bnf
parameter-declaration:
    attribute-specifier-seqₒₚₜ thisₒₚₜ decl-specifier-seq declarator
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator '=' initializer-clause
    attribute-specifier-seqₒₚₜ thisₒₚₜ decl-specifier-seq abstract-declaratorₒₚₜ 
    attribute-specifier-seqₒₚₜ decl-specifier-seq abstract-declaratorₒₚₜ '=' initializer-clause
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
    '{' initializer-list ','ₒₚₜ '}'
    '{' designated-initializer-list ','ₒₚₜ '}'
    '{' '}'
```

``` bnf
initializer-list:
    initializer-clause '...'ₒₚₜ 
    initializer-list ',' initializer-clause '...'ₒₚₜ
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
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator virt-specifier-seqₒₚₜ function-body
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator requires-clause function-body
```

``` bnf
function-body:
    ctor-initializerₒₚₜ compound-statement
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
attribute-specifier-seqₒₚₜ *S* cv 'A' e ';'
```

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seq ref-qualifierₒₚₜ e initializer ';'
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
    enum-head '{' enumerator-listₒₚₜ '}'
    enum-head '{' enumerator-list ',' '}'
```

``` bnf
enum-head:
    enum-key attribute-specifier-seqₒₚₜ enum-head-nameₒₚₜ enum-baseₒₚₜ
```

``` bnf
enum-head-name:
    nested-name-specifierₒₚₜ identifier
```

``` bnf
opaque-enum-declaration:
    enum-key attribute-specifier-seqₒₚₜ enum-head-name enum-baseₒₚₜ ';'
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
    identifier attribute-specifier-seqₒₚₜ
```

``` bnf
using-enum-declaration:
    using enum using-enum-declarator ';'
```

``` bnf
using-enum-declarator:
    nested-name-specifierₒₚₜ identifier
    nested-name-specifierₒₚₜ simple-template-id
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
        inlineₒₚₜ namespace attribute-specifier-seqₒₚₜ identifier '{' namespace-body '}'
```

``` bnf
unnamed-namespace-definition:
        inlineₒₚₜ namespace attribute-specifier-seqₒₚₜ '{' namespace-body '}'
```

``` bnf
nested-namespace-definition:
        namespace enclosing-namespace-specifier '::' inlineₒₚₜ identifier '{' namespace-body '}'
```

``` bnf
enclosing-namespace-specifier:
        identifier
        enclosing-namespace-specifier '::' inlineₒₚₜ identifier
```

``` bnf
namespace-body:
        declaration-seqₒₚₜ
```

``` bnf
inlineₒₚₜ namespace unique '{' '/* empty body */' '}'
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
    nested-name-specifierₒₚₜ namespace-name
```

``` bnf
using-directive:
    attribute-specifier-seqₒₚₜ using namespace nested-name-specifierₒₚₜ namespace-name ';'
```

``` bnf
using-declaration:
    using using-declarator-list ';'
```

``` bnf
using-declarator-list:
    using-declarator '...'ₒₚₜ 
    using-declarator-list ',' using-declarator '...'ₒₚₜ
```

``` bnf
using-declarator:
    typenameₒₚₜ nested-name-specifier unqualified-id
```

``` bnf
asm-declaration:
    attribute-specifier-seqₒₚₜ asm '(' string-literal ')' ';'
```

``` bnf
linkage-specification:
    extern string-literal '{' declaration-seqₒₚₜ '}'
    extern string-literal name-declaration
```

``` bnf
attribute-specifier-seq:
  attribute-specifier-seqₒₚₜ attribute-specifier
```

``` bnf
attribute-specifier:
  '[' '[' attribute-using-prefixₒₚₜ attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  alignas '(' type-id '...'ₒₚₜ ')'
  alignas '(' constant-expression '...'ₒₚₜ ')'
```

``` bnf
attribute-using-prefix:
  using attribute-namespace ':'
```

``` bnf
attribute-list:
  attributeₒₚₜ 
  attribute-list ',' attributeₒₚₜ 
  attribute '...'
  attribute-list ',' attribute '...'
```

``` bnf
attribute:
    attribute-token attribute-argument-clauseₒₚₜ
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
    '(' balanced-token-seqₒₚₜ ')'
```

``` bnf
balanced-token-seq:
    balanced-token
    balanced-token-seq balanced-token
```

``` bnf
balanced-token:
    '(' balanced-token-seqₒₚₜ ')'
    '[' balanced-token-seqₒₚₜ ']'
    '{' balanced-token-seqₒₚₜ '}'
    any *token* other than a parenthesis, a bracket, or a brace
```

``` bnf
'(' conditional-expression ')'
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
    class-head '{' member-specificationₒₚₜ '}'
```

``` bnf
class-head:
    class-key attribute-specifier-seqₒₚₜ class-head-name class-virt-specifierₒₚₜ base-clauseₒₚₜ 
    class-key attribute-specifier-seqₒₚₜ base-clauseₒₚₜ
```

``` bnf
class-head-name:
    nested-name-specifierₒₚₜ class-name
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
    member-declaration member-specificationₒₚₜ 
    access-specifier ':' member-specificationₒₚₜ
```

``` bnf
member-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ member-declarator-listₒₚₜ ';'
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
    declarator virt-specifier-seqₒₚₜ pure-specifierₒₚₜ 
    declarator requires-clause
    declarator brace-or-equal-initializerₒₚₜ 
    identifierₒₚₜ attribute-specifier-seqₒₚₜ ':' constant-expression brace-or-equal-initializerₒₚₜ
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
ptr-declarator '(' parameter-declaration-clause ')' noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
conversion-function-id:
    operator conversion-type-id
```

``` bnf
conversion-type-id:
    type-specifier-seq conversion-declaratorₒₚₜ
```

``` bnf
conversion-declarator:
    ptr-operator conversion-declaratorₒₚₜ
```

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
   ref-qualifier-seqₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
identifierₒₚₜ attribute-specifier-seqₒₚₜ ':' constant-expression brace-or-equal-initializerₒₚₜ
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
    base-specifier '...'ₒₚₜ 
    base-specifier-list ',' base-specifier '...'ₒₚₜ
```

``` bnf
base-specifier:
    attribute-specifier-seqₒₚₜ class-or-decltype
    attribute-specifier-seqₒₚₜ virtual access-specifierₒₚₜ class-or-decltype
    attribute-specifier-seqₒₚₜ access-specifier virtualₒₚₜ class-or-decltype
```

``` bnf
class-or-decltype:
    nested-name-specifierₒₚₜ type-name
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
access-specifier ':' member-specificationₒₚₜ
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
    mem-initializer '...'ₒₚₜ 
    mem-initializer-list ',' mem-initializer '...'ₒₚₜ
```

``` bnf
mem-initializer:
    mem-initializer-id '(' expression-listₒₚₜ ')'
    mem-initializer-id braced-init-list
```

``` bnf
mem-initializer-id:
    class-or-decltype
    identifier
```


## Overloading <a id="gram.over">[[gram.over]]</a>

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

``` bnf
postfix-expression:
    postfix-expression '.' id-expression
    postfix-expression '->' id-expression
    primary-expression
```

``` bnf
operator conversion-type-id '( )' cv-qualifier-seqₒₚₜ ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ ';'
```

``` bnf
'R' *call-function* '(' conversion-type-id \ %
'F, P₁ a₁, …, Pₙ aₙ)' '{ return F (a₁, …, aₙ); }'
```

``` bnf
typenameₒₚₜ nested-name-specifierₒₚₜ templateₒₚₜ simple-template-id
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
postfix-expression '(' expression-listₒₚₜ ')'
```

``` bnf
e '(' expression-listₒₚₜ ')'
```

``` bnf
postfix-expression '.' operator '('')' '(' expression-listₒₚₜ ')'
```

``` bnf
postfix-expression '[' expression-listₒₚₜ ']'
```

``` bnf
postfix-expression . operator '['']' '(' expression-listₒₚₜ ')'
```

``` bnf
postfix-expression '->' templateₒₚₜ id-expression
```

``` bnf
'(' postfix-expression . operator '->' '('')' ')' '->' templateₒₚₜ id-expression
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
  template '<' template-parameter-list '>' requires-clauseₒₚₜ
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
  type-parameter-key '...'ₒₚₜ identifierₒₚₜ 
  type-parameter-key identifierₒₚₜ '=' type-id
  type-constraint '...'ₒₚₜ identifierₒₚₜ 
  type-constraint identifierₒₚₜ '=' type-id
  template-head type-parameter-key '...'ₒₚₜ identifierₒₚₜ 
  template-head type-parameter-key identifierₒₚₜ '=' id-expression
```

``` bnf
type-parameter-key:
  class
  typename
```

``` bnf
type-constraint:
  nested-name-specifierₒₚₜ concept-name
  nested-name-specifierₒₚₜ concept-name '<' template-argument-listₒₚₜ '>'
```

``` bnf
simple-template-id:
  template-name '<' template-argument-listₒₚₜ '>'
```

``` bnf
template-id:
  simple-template-id
  operator-function-id '<' template-argument-listₒₚₜ '>'
  literal-operator-id '<' template-argument-listₒₚₜ '>'
```

``` bnf
template-name:
  identifier
```

``` bnf
template-argument-list:
  template-argument '...'ₒₚₜ 
  template-argument-list ',' template-argument '...'ₒₚₜ
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
    explicit-specifierₒₚₜ template-name '(' parameter-declaration-clause ')' '->' simple-template-id ';'
```

``` bnf
concept-definition:
  concept concept-name attribute-specifier-seqₒₚₜ '=' constraint-expression ';'
```

``` bnf
concept-name:
  identifier
```

``` bnf
typename-specifier:
  typename nested-name-specifier identifier
  typename nested-name-specifier 'templateₒₚₜ ' simple-template-id
```

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

``` bnf
simple-type-specifier '(' expression-listₒₚₜ ')'
simple-type-specifier braced-init-list
typename-specifier '(' expression-listₒₚₜ ')'
typename-specifier braced-init-list
'::'ₒₚₜ new new-placementₒₚₜ new-type-id new-initializerₒₚₜ 
'::'ₒₚₜ new new-placementₒₚₜ '(' type-id ')' new-initializerₒₚₜ 
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
'::'ₒₚₜ delete cast-expression
'::'ₒₚₜ delete '[' ']' cast-expression
throw assignment-expressionₒₚₜ 
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
simple-type-specifier '(' expression-listₒₚₜ ')'
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
  externₒₚₜ template declaration
```

``` bnf
explicit-specialization:
  template '<' '>' declaration
```


## Preprocessing directives <a id="gram.cpp">[[gram.cpp]]</a>

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
    '# undef ' identifier new-line
    '# line ' pp-tokens new-line
    '# error ' pp-tokensₒₚₜ new-line
    '# warning' pp-tokensₒₚₜ new-line
    '# pragma ' pp-tokensₒₚₜ new-line
    '# 'new-line
```

``` bnf
if-section:
    if-group elif-groupsₒₚₜ else-groupₒₚₜ endif-line
```

``` bnf
if-group:
    '# if ' constant-expression new-line groupₒₚₜ 
    '# ifdef ' identifier new-line groupₒₚₜ 
    '# ifndef ' identifier new-line groupₒₚₜ
```

``` bnf
elif-groups:
    elif-group
    elif-groups elif-group
```

``` bnf
elif-group:
    '# elif ' constant-expression new-line groupₒₚₜ 
    '# elifdef ' identifier new-line groupₒₚₜ 
    '# elifndef' identifier new-line groupₒₚₜ
```

``` bnf
else-group:
    '# else ' new-line groupₒₚₜ
```

``` bnf
endif-line:
    '# endif ' new-line
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
    a '(' character not immediately preceded by whitespace
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
'# if ' constant-expression new-line groupₒₚₜ 
'# elif ' constant-expression new-line groupₒₚₜ
```

``` bnf
'# ifdef ' identifier new-line groupₒₚₜ 
'# ifndef ' identifier new-line groupₒₚₜ 
'# elifdef ' identifier new-line groupₒₚₜ 
'# elifndef' identifier new-line groupₒₚₜ
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
    exportₒₚₜ module pp-tokensₒₚₜ ';' new-line
```

``` bnf
pp-import:
    exportₒₚₜ import header-name pp-tokensₒₚₜ ';' new-line
    exportₒₚₜ import header-name-tokens pp-tokensₒₚₜ ';' new-line
    exportₒₚₜ import pp-tokens ';' new-line
```

``` bnf
'# define' identifier replacement-list new-line
```

``` bnf
'# define' identifier lparen identifier-listₒₚₜ ')' replacement-list new-line
'# define' identifier lparen '...' ')' replacement-list new-line
'# define' identifier lparen identifier-list ', ...' ')' replacement-list new-line
```

``` bnf
va-opt-replacement:
    '__VA_OPT__ (' pp-tokensₒₚₜ ')'
```

``` bnf
'# undef' identifier new-line
```

``` bnf
'# line' digit-sequence new-line
```

``` bnf
'# line' digit-sequence '"' s-char-sequenceₒₚₜ '"' new-line
```

``` bnf
'# line' pp-tokens new-line
```

``` bnf
'# error' pp-tokensₒₚₜ new-line
'# warning' pp-tokensₒₚₜ new-line
```

``` bnf
'# pragma' pp-tokensₒₚₜ new-line
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
    try compound-statement handler-seq
```

``` bnf
function-try-block:
    try ctor-initializerₒₚₜ compound-statement handler-seq
```

``` bnf
handler-seq:
    handler handler-seqₒₚₜ
```

``` bnf
handler:
    catch '(' exception-declaration ')' compound-statement
```

``` bnf
exception-declaration:
    attribute-specifier-seqₒₚₜ type-specifier-seq declarator
    attribute-specifier-seqₒₚₜ type-specifier-seq abstract-declaratorₒₚₜ 
    '...'
```

``` bnf
noexcept-specifier:
    noexcept '(' constant-expression ')'
    noexcept
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
