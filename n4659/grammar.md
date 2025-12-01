# Grammar summary (informative) <a id="gram" data-annex="true" data-annex-type="informative">[[gram]]</a>

This summary of C++ grammar is intended to be an aid to comprehension.
It is not an exact statement of the language. In particular, the grammar
described here accepts a superset of valid C++ constructs.
Disambiguation rules ([[stmt.ambig]], [[dcl.spec]],
[[class.member.lookup]]) must be applied to distinguish expressions from
declarations. Further, access control, ambiguity, and type rules must be
used to weed out syntactically valid but meaningless constructs.

## Keywords <a id="gram.key">[[gram.key]]</a>

New context-dependent keywords are introduced into a program by
`typedef` ([[dcl.typedef]]), `namespace` ([[namespace.def]]),
class (Clause [[class]]), enumeration ([[dcl.enum]]), and
`template` (Clause [[temp]]) declarations.

``` bnf
typedef-name:
    identifier
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

Note that a *typedef-name* naming a class is also a *class-name* (
[[class.name]]).

<!-- Link reference definitions -->
[class]: class.md#class
[class.member.lookup]: class.md#class.member.lookup
[class.name]: class.md#class.name
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
    operator
    punctuator
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
literal:
    integer-literal
    character-literal
    floating-literal
    string-literal
    boolean-literal
    pointer-literal
    user-defined-literal
```

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


## Basic concepts <a id="gram.basic">[[gram.basic]]</a>

``` bnf
nested-name-specifiercₒₚₜlass-name '::' '~' class-name
```

``` bnf
nested-name-specifier unqualified-id
```

``` bnf
class-key attribute-specifier-seqiₒₚₜdentifier ';'
```

``` bnf
class-key attribute-specifier-seqiₒₚₜdentifier ';'
```

``` bnf
translation-unit:
    declaration-seq\opt
```


## Expressions <a id="gram.expr">[[gram.expr]]</a>

``` bnf
primary-expression:
    literal
    'this'
    '(' expression ')'
    id-expression
    lambda-expression
    fold-expression
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
    '~' class-name
    '~' decltype-specifier
    template-id
```

``` bnf
qualified-id:
    nested-name-specifier 'template'uₒₚₜnqualified-id
```

``` bnf
nested-name-specifier:
    '::'
    type-name '::'
    namespace-name '::'
    decltype-specifier '::'
    nested-name-specifier identifier '::'
    nested-name-specifier 'template'sₒₚₜimple-template-id '::'
```

``` bnf
lambda-expression:
    lambda-introducer lambda-declaratorcₒₚₜompound-statement
```

``` bnf
lambda-introducer:
    '[' lambda-captureₒₚₜ ']'
```

``` bnf
lambda-declarator:
    '(' parameter-declaration-clause ')' decl-specifier-seq\opt
    \hspace*{  inc}noexcept-specifier\opt attribute-specifier-seq\opt trailing-return-type\opt
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
    capture '...\opt'
    capture-list ',' capture '...\opt'
```

``` bnf
capture:
    simple-capture
    init-capture
```

``` bnf
simple-capture:
    identifier
    '&' identifier
    'this'
    '* this'
```

``` bnf
init-capture:
    identifier initializer
    '&' identifier initializer
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
    '==' '!=' '< ' '> ' '<=' '>=' '&&' '||' ',  ' '.* ' '->*'
```

``` bnf
postfix-expression:
    primary-expression
    postfix-expression '[' expr-or-braced-init-list ']'
    postfix-expression '(' expression-listₒₚₜ ')'
    simple-type-specifier '(' expression-listₒₚₜ ')'
    typename-specifier '(' expression-listₒₚₜ ')'
    simple-type-specifier braced-init-list
    typename-specifier braced-init-list
    postfix-expression '. template'iₒₚₜd-expression
    postfix-expression '-> template'iₒₚₜd-expression
    postfix-expression '.' pseudo-destructor-name
    postfix-expression '->' pseudo-destructor-name
    postfix-expression '++'
    postfix-expression '-{-}'
    'dynamic_cast <' type-id '> (' expression ')'
    'static_cast <' type-id '> (' expression ')'
    'reinterpret_cast <' type-id '> (' expression ')'
    'const_cast <' type-id '> (' expression ')'
    'typeid (' expression ')'
    'typeid (' type-id ')'
```

``` bnf
expression-list:
    initializer-list
```

``` bnf
pseudo-destructor-name:
    nested-name-specifiertₒₚₜype-name ':: ~' type-name
    nested-name-specifier 'template' simple-template-id ':: ~' type-name
    '~' type-name
    '~' decltype-specifier
```

``` bnf
nested-name-specifiertₒₚₜype-name ':: ~' type-name
```

``` bnf
unary-expression:
    postfix-expression
    '++' cast-expression
    '-{-}' cast-expression
    unary-operator cast-expression
    'sizeof' unary-expression
    'sizeof (' type-id ')'
    'sizeof ...' '(' identifier ')'
    'alignof (' type-id ')'
    noexcept-expression
    new-expression
    delete-expression
```

``` bnf
unary-operator: one of
    '*  &  +  -  !  ~'
```

``` bnf
new-expression:
    '::'\opt{} 'new' new-placement\opt new-type-id new-initializer\opt 
    '::'\opt{} 'new' new-placement\opt{} '(' type-id ')' new-initializer\opt
```

``` bnf
new-placement:
    '(' expression-list ')'
```

``` bnf
new-type-id:
    type-specifier-seq new-declarator\opt
```

``` bnf
new-declarator:
    ptr-operator new-declarator
 ₒₚₜ
    noptr-new-declarator
```

``` bnf
noptr-new-declarator:
    '[' expression ']' attribute-specifier-seq\opt
    noptr-new-declarator '[' constant-expression ']' attribute-specifier-seq\opt
```

``` bnf
new-initializer:
    '(' expression-listₒₚₜ ')'
    braced-init-list
```

``` bnf
delete-expression:
    '::'ₒₚₜ 'delete' cast-expression
    '::'ₒₚₜ 'delete [ ]' cast-expression
```

``` bnf
noexcept-expression:
  'noexcept' '(' expression ')'
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
relational-expression:
    shift-expression
    relational-expression '<' shift-expression
    relational-expression '>' shift-expression
    relational-expression '<=' shift-expression
    relational-expression '>=' shift-expression
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
throw-expression:
    'throw'  assignment-expression\opt
```

``` bnf
assignment-expression:
    conditional-expression
    logical-or-expression assignment-operator initializer-clause
    throw-expression
```

``` bnf
assignment-operator: one of
    '=  *=  /=  %=   +=  -=  >>=  <<=  &=  ^=  |='
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
    attribute-specifier-seqeₒₚₜxpression-statement
    attribute-specifier-seqcₒₚₜompound-statement
    attribute-specifier-seqsₒₚₜelection-statement
    attribute-specifier-seqiₒₚₜteration-statement
    attribute-specifier-seqjₒₚₜump-statement
    declaration-statement
    attribute-specifier-seqtₒₚₜry-block

init-statement:
    expression-statement
    simple-declaration

condition:
    expression
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator brace-or-equal-initializer
```

``` bnf
labeled-statement:
    attribute-specifier-seqiₒₚₜdentifier ':' statement
    attribute-specifier-seqₒₚₜ 'case' constant-expression ':' statement
    attribute-specifier-seqₒₚₜ 'default :' statement
```

``` bnf
expression-statement:
    expressionₒₚₜ ';'
```

``` bnf
compound-statement:
    '{' statement-seqₒₚₜ '}'
```

``` bnf
statement-seq:
    statement
    statement-seq statement
```

``` bnf
selection-statement:
    'if constexpr(ₒₚₜ' init-statementcₒₚₜondition ')' statement
    'if constexpr(ₒₚₜ' init-statementcₒₚₜondition ')' statement 'else' statement
    'switch (' init-statementcₒₚₜondition ')' statement
```

``` bnf
'if constexpr(ₒₚₜ' init-statement condition ')' statement
```

``` bnf
'if constexpr(ₒₚₜ' init-statement condition ')' statement 'else' statement
```

``` bnf
'case' constant-expression ':'
```

``` bnf
'switch (' init-statement condition ')' statement
```

``` bnf
iteration-statement:
    'while (' condition ')' statement
    'do' statement 'while (' expression ') ;'
    'for (' init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
    'for (' for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
for-range-declaration:
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator
    attribute-specifier-seqdₒₚₜecl-specifier-seq ref-qualifierₒₚₜ '[' identifier-list ']'
```

``` bnf
for-range-initializer:
    expr-or-braced-init-list
```

``` bnf
'for (' init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
```

``` bnf
'for (' for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
jump-statement:
    'break ;'
    'continue ;'
    'return' expr-or-braced-init-listₒₚₜ ';'
    'goto' identifier ';'
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
    linkage-specification
    namespace-definition
    empty-declaration
    attribute-declaration
```

``` bnf
block-declaration:
    simple-declaration
    asm-definition
    namespace-alias-definition
    using-declaration
    using-directive
    static_assert-declaration
    alias-declaration
    opaque-enum-declaration
```

``` bnf
nodeclspec-function-declaration:
    attribute-specifier-seqdₒₚₜeclarator ';'
```

``` bnf
alias-declaration:
    'using' identifier attribute-specifier-seqₒₚₜ '=' defining-type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seq init-declarator-listₒₚₜ ';'
    attribute-specifier-seq decl-specifier-seq init-declarator-list ';'
    attribute-specifier-seqdₒₚₜecl-specifier-seq ref-qualifierₒₚₜ '[' identifier-list ']' initializer ';'
```

``` bnf
static_assert-declaration:
  'static_assert' '(' constant-expression ')' ';'
  'static_assert' '(' constant-expression ',' string-literal ')' ';'
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
attribute-specifier-seqdₒₚₜecl-specifier-seqiₒₚₜnit-declarator-listₒₚₜ ';'
```

``` bnf
decl-specifier:
    storage-class-specifier
    defining-type-specifier
    function-specifier
    'friend'
    'typedef'
    'constexpr'
    'inline'
```

``` bnf
decl-specifier-seq:
    decl-specifier attribute-specifier-seq
 ₒₚₜ
    decl-specifier decl-specifier-seq
```

``` bnf
storage-class-specifier:
    'static'
    'thread_local'
    'extern'
    'mutable'
```

``` bnf
function-specifier:
    'virtual'
    'explicit'
```

``` bnf
typedef-name:
    identifier
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
    type-specifier attribute-specifier-seq
 ₒₚₜ
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
  defining-type-specifier attribute-specifier-seq
 ₒₚₜ
  defining-type-specifier defining-type-specifier-seq
```

``` bnf
simple-type-specifier:
    nested-name-specifiertₒₚₜype-name
    nested-name-specifier 'template' simple-template-id
    nested-name-specifiertₒₚₜemplate-name
    'char'
    'char16_t'
    'char32_t'
    'wchar_t'
    'bool'
    'short'
    'int'
    'long'
    'signed'
    'unsigned'
    'float'
    'double'
    'void'
    'auto'
    decltype-specifier
```

``` bnf
type-name:
    class-name
    enum-name
    typedef-name
    simple-template-id
```

``` bnf
decltype-specifier:
  'decltype' '(' expression ')'
  'decltype' '(' 'auto' ')'
```

``` bnf
elaborated-type-specifier:
    class-key attribute-specifier-seqnₒₚₜested-name-specifieriₒₚₜdentifier
    class-key simple-template-id
    class-key nested-name-specifier 'template'sₒₚₜimple-template-id
    'enum' nested-name-specifieriₒₚₜdentifier
```

``` bnf
class-key attribute-specifier-seqiₒₚₜdentifier ';'
'friend' class-key '::\opt' identifier ';'
'friend' class-key '::\opt' simple-template-id ';'
'friend' class-key nested-name-specifier identifier ';'
'friend' class-key nested-name-specifier 'template\opt' simple-template-id ';'
```

``` bnf
enum-name:
    identifier
```

``` bnf
enum-specifier:
    enum-head '{' enumerator-listₒₚₜ '}'
    enum-head '{' enumerator-list ', }'
```

``` bnf
enum-head:
    enum-key attribute-specifier-seq\opt enum-head-name\opt enum-base\opt
```

``` bnf
enum-head-name:
    nested-name-specifieriₒₚₜdentifier
```

``` bnf
opaque-enum-declaration:
    enum-key attribute-specifier-seqnₒₚₜested-name-specifieriₒₚₜdentifier enum-baseₒₚₜ ';'
```

``` bnf
enum-key:
    'enum'
    'enum class'
    'enum struct'
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
    identifier attribute-specifier-seq\opt
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
        'inline\opt' 'namespace' attribute-specifier-seqiₒₚₜdentifier '{' namespace-body '}'
```

``` bnf
unnamed-namespace-definition:
        'inline\opt' 'namespace' attribute-specifier-seqₒₚₜ '{' namespace-body '}'
```

``` bnf
nested-namespace-definition:
        'namespace' enclosing-namespace-specifier '::' identifier '{' namespace-body '}'
```

``` bnf
enclosing-namespace-specifier:
        identifier
        enclosing-namespace-specifier '::' identifier
```

``` bnf
namespace-body:
        declaration-seq\opt
```

``` bnf
'inline'ₒₚₜ 'namespace' '\uniquens' '{ /* empty body */ }'
'using namespace' '\uniquens' ';'
'namespace' '\uniquens' '{' namespace-body '}'
```

``` bnf
namespace-alias:
        identifier
```

``` bnf
namespace-alias-definition:
        'namespace' identifier '=' qualified-namespace-specifier ';'
```

``` bnf
qualified-namespace-specifier:
    nested-name-specifiernₒₚₜamespace-name
```

``` bnf
using-declaration:
    'using' using-declarator-list ';'
```

``` bnf
using-declarator-list:
    using-declarator '...'\opt
    using-declarator-list ',' using-declarator '...'\opt
```

``` bnf
using-declarator:
    'typename\opt' nested-name-specifier unqualified-id
```

``` bnf
using-directive:
    attribute-specifier-seqₒₚₜ 'using  namespace' nested-name-specifiernₒₚₜamespace-name ';'
```

``` bnf
asm-definition:
    attribute-specifier-seqₒₚₜ 'asm (' string-literal ') ;'
```

``` bnf
linkage-specification:
    'extern' string-literal '{' declaration-seqₒₚₜ '}'
    'extern' string-literal declaration
```

``` bnf
attribute-specifier-seq:
  attribute-specifier-seqaₒₚₜttribute-specifier
```

``` bnf
attribute-specifier:
  '[' '[' attribute-using-prefixₒₚₜ attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  'alignas (' type-id '...'ₒₚₜ ')'
  'alignas (' constant-expression '...'ₒₚₜ ')'
```

``` bnf
attribute-using-prefix:
  'using' attribute-namespace ':'
```

``` bnf
attribute-list:
  attribute
 ₒₚₜ
  attribute-list ',' attribute
 ₒₚₜ
  attribute '...'
  attribute-list ',' attribute '...'
```

``` bnf
attribute:
    attribute-token attribute-argument-clause\opt
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
init-declarator-list:
    init-declarator
    init-declarator-list ',' init-declarator
```

``` bnf
init-declarator:
    declarator initializer\opt
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
    declarator-id attribute-specifier-seq
 ₒₚₜ
    noptr-declarator parameters-and-qualifiers
    noptr-declarator '[' constant-expressionₒₚₜ ']' attribute-specifier-seq
 ₒₚₜ
    '(' ptr-declarator ')'
```

``` bnf
parameters-and-qualifiers:
    '(' parameter-declaration-clause ')' cv-qualifier-seq\opt
\hspace*{  inc}ref-qualifier\opt noexcept-specifier\opt attribute-specifier-seq\opt
```

``` bnf
trailing-return-type:
    '->' type-id
```

``` bnf
ptr-operator:
    '*' attribute-specifier-seq\opt cv-qualifier-seq\opt
    '&' attribute-specifier-seq\opt
    '&&' attribute-specifier-seq\opt
    nested-name-specifier '*' attribute-specifier-seq\opt cv-qualifier-seq\opt
```

``` bnf
cv-qualifier-seq:
    cv-qualifier cv-qualifier-seq\opt
```

``` bnf
cv-qualifier:
    'const'
    'volatile'
```

``` bnf
ref-qualifier:
    '&'
    '&&'
```

``` bnf
declarator-id:
    '...'iₒₚₜd-expression
```

``` bnf
type-id:
    type-specifier-seq abstract-declarator\opt
```

``` bnf
defining-type-id:
    defining-type-specifier-seq abstract-declarator\opt
```

``` bnf
abstract-declarator:
    ptr-abstract-declarator
    noptr-abstract-declaratorpₒₚₜarameters-and-qualifiers trailing-return-type
    abstract-pack-declarator
```

``` bnf
ptr-abstract-declarator:
    noptr-abstract-declarator
    ptr-operator ptr-abstract-declarator\opt
```

``` bnf
noptr-abstract-declarator:
    noptr-abstract-declaratorpₒₚₜarameters-and-qualifiers
    noptr-abstract-declaratorₒₚₜ '[' constant-expressionₒₚₜ ']' attribute-specifier-seq
 ₒₚₜ
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
    noptr-abstract-pack-declarator '[' constant-expressionₒₚₜ ']' attribute-specifier-seq
 ₒₚₜ
    '...'
```

``` bnf
'(' 'D1' ')'
```

``` bnf
'*' attribute-specifier-seqcₒₚₜv-qualifier-seqₒₚₜ 'D1'
```

``` bnf
'&' attribute-specifier-seqₒₚₜ 'D1'
'&&' attribute-specifier-seqₒₚₜ 'D1'
```

``` bnf
nested-name-specifier '*' attribute-specifier-seqcₒₚₜv-qualifier-seqₒₚₜ 'D1'
```

``` bnf
'D1 [' constant-expression\opt{} ']' attribute-specifier-seq\opt
```

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seq\opt
\hspace*{  inc}ref-qualifier\opt noexcept-specifier\opt attribute-specifier-seq\opt
```

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seq
 ₒₚₜ
\hspace*{  inc}ref-qualifiernₒₚₜoexcept-specifieraₒₚₜttribute-specifier-seqtₒₚₜrailing-return-type
```

``` bnf
parameter-declaration-clause:
    parameter-declaration-listₒₚₜ '...'
 ₒₚₜ
    parameter-declaration-list ', ...'
```

``` bnf
parameter-declaration-list:
    parameter-declaration
    parameter-declaration-list ',' parameter-declaration
```

``` bnf
parameter-declaration:
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator '=' initializer-clause
    attribute-specifier-seqdₒₚₜecl-specifier-seq abstract-declarator
 ₒₚₜ
    attribute-specifier-seqdₒₚₜecl-specifier-seq abstract-declaratorₒₚₜ '=' initializer-clause
```

``` bnf
function-definition:
    attribute-specifier-seqdₒₚₜecl-specifier-seqdₒₚₜeclarator virt-specifier-seqfₒₚₜunction-body
```

``` bnf
function-body:
    ctor-initializercₒₚₜompound-statement
    function-try-block
    '= default ;'
    '= delete ;'
```

``` bnf
attribute-specifier-seqdₒₚₜecl-specifier-seqdₒₚₜeclarator virt-specifier-seqₒₚₜ ' = default ;'
```

``` bnf
attribute-specifier-seqdₒₚₜecl-specifier-seqdₒₚₜeclarator virt-specifier-seqₒₚₜ ' = delete ;'
```

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seq ref-qualifierₒₚₜ 'e' initializer ';'
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
initializer-list:
    initializer-clause '...'\opt
    initializer-list ',' initializer-clause '...'\opt
```

``` bnf
braced-init-list:
    '{' initializer-list ',\opt' '}'
    '{' '}'
```

``` bnf
expr-or-braced-init-list:
    expression
    braced-init-list
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
    class-key attribute-specifier-seq\opt class-head-name class-virt-specifier\opt base-clause\opt
    class-key attribute-specifier-seq\opt base-clause\opt
```

``` bnf
class-head-name:
    nested-name-specifiercₒₚₜlass-name
```

``` bnf
class-virt-specifier:
    'final'
```

``` bnf
class-key:
    'class'
    'struct'
    'union'
```

``` bnf
member-specification:
    member-declaration member-specification\opt
    access-specifier ':' member-specification\opt
```

``` bnf
member-declaration:
    attribute-specifier-seqdₒₚₜecl-specifier-seqmₒₚₜember-declarator-listₒₚₜ ';'
    function-definition
    using-declaration
    static_assert-declaration
    template-declaration
    deduction-guide
    alias-declaration
    empty-declaration
```

``` bnf
member-declarator-list:
    member-declarator
    member-declarator-list ',' member-declarator
```

``` bnf
member-declarator:
    declarator virt-specifier-seqpₒₚₜure-specifier
 ₒₚₜ
    declarator brace-or-equal-initializer
 ₒₚₜ
    identifieraₒₚₜttribute-specifier-seqₒₚₜ ':' constant-expression
```

``` bnf
virt-specifier-seq:
    virt-specifier
    virt-specifier-seq virt-specifier
```

``` bnf
virt-specifier:
    'override'
    'final'
```

``` bnf
pure-specifier:
    '= 0'
```

``` bnf
base-clause:
    ':' base-specifier-list
```

``` bnf
base-specifier-list:
    base-specifier '...'\opt
    base-specifier-list ',' base-specifier '...'\opt
```

``` bnf
base-specifier:
    attribute-specifier-seqcₒₚₜlass-or-decltype
    attribute-specifier-seqₒₚₜ 'virtual' access-specifiercₒₚₜlass-or-decltype
    attribute-specifier-seqaₒₚₜccess-specifier 'virtual'cₒₚₜlass-or-decltype
```

``` bnf
class-or-decltype:
    nested-name-specifiercₒₚₜlass-name
    nested-name-specifier 'template' simple-template-id
    decltype-specifier
```

``` bnf
access-specifier:
    'private'
    'protected'
    'public'
```

``` bnf
'friend' elaborated-type-specifier ';'
'friend' simple-type-specifier ';'
'friend' typename-specifier ';'
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
'operator' conversion-type-id '( )' cv-qualifier ref-qualifiernₒₚₜoexcept-specifieraₒₚₜttribute-specifier-seqₒₚₜ ';'
```

``` bnf
'R' call-function '(' conversion-type-id \ %
'F, P₁ a₁, …, Pₙ aₙ)' '{ return F (a₁, …, aₙ); }'
```

``` bnf
operator-function-id:
    'operator' operator
```

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

``` bnf
postfix-expression '[' expr-or-braced-init-list ']'
```

``` bnf
postfix-expression '->' 'template\opt' id-expression\\
postfix-expression '->' pseudo-destructor-name
```

``` bnf
literal-operator-id:
    'operator' string-literal identifier
    'operator' user-defined-string-literal
```


## Templates <a id="gram.temp">[[gram.temp]]</a>

``` bnf
template-declaration:
  'template <' template-parameter-list '>' declaration
```

``` bnf
template-parameter-list:
  template-parameter
  template-parameter-list ',' template-parameter
```

``` bnf
template-parameter:
  type-parameter
  parameter-declaration
```

``` bnf
type-parameter:
  type-parameter-key '...'iₒₚₜdentifier
 ₒₚₜ
  type-parameter-key identifierₒₚₜ '=' type-id
  'template <' template-parameter-list '>' type-parameter-key '...'iₒₚₜdentifier
 ₒₚₜ
  'template <' template-parameter-list '>' type-parameter-key identifierₒₚₜ '=' id-expression
```

``` bnf
type-parameter-key:
  'class'
  'typename'
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
  template-argument '...'\opt
  template-argument-list ',' template-argument '...'\opt
```

``` bnf
template-argument:
  constant-expression
  type-id
  id-expression
```

``` bnf
typename-specifier:
  'typename' nested-name-specifier identifier
  'typename' nested-name-specifier 'template\opt' simple-template-id
```

``` bnf
explicit-instantiation:
  'extern\opt' 'template' declaration
```

``` bnf
explicit-specialization:
  'template < >' declaration
```

``` bnf
deduction-guide:
    'explicit'ₒₚₜ template-name '(' parameter-declaration-clause ') ->' simple-template-id ';'
```


## Preprocessing directives <a id="gram.cpp">[[gram.cpp]]</a>

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
    control-line
    if-section
    text-line
    '#' conditionally-supported-directive
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
    pp-tokensnₒₚₜew-line
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
has-include-expression:
    '__has_include ( <' h-char-sequence '> )'
    '__has_include ( "' q-char-sequence '" )'
    '__has_include ('   string-literal  ')'
    '__has_include ( <' h-pp-tokens     '> )'
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
'# define' identifier replacement-list new-line
```

``` bnf
'# define' identifier lparen identifier-listₒₚₜ ')' replacement-list new-line
'# define' identifier lparen '...' ')' replacement-list new-line
'# define' identifier lparen identifier-list ', ...' ')' replacement-list new-line
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
'# error' pp-tokensnₒₚₜew-line
```

``` bnf
'# pragma' pp-tokensnₒₚₜew-line
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
    'try' ctor-initializercₒₚₜompound-statement handler-seq
```

``` bnf
handler-seq:
    handler handler-seq\opt
```

``` bnf
handler:
    'catch (' exception-declaration ')' compound-statement
```

``` bnf
exception-declaration:
    attribute-specifier-seqtₒₚₜype-specifier-seq declarator
    attribute-specifier-seqtₒₚₜype-specifier-seq abstract-declarator
 ₒₚₜ
    '...'
```

``` bnf
noexcept-specifier:
    'noexcept' '(' constant-expression ')'
    'noexcept'
    'throw' '(' ')'
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
