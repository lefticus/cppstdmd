## Keywords

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
    pp-number 'e' sign
    pp-number 'E' sign
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
    other implementation-defined characters
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
    decimal-literal integer-suffix\opt
    octal-literal integer-suffix\opt
    hexadecimal-literal integer-suffix\opt
```

``` bnf
decimal-literal:
    nonzero-digit
    decimal-literal digit
```

``` bnf
octal-literal:
    '0'
    octal-literal octal-digit
```

``` bnf
hexadecimal-literal:
    '0x' hexadecimal-digit
    '0X' hexadecimal-digit
    hexadecimal-literal hexadecimal-digit
```

``` bnf
nonzero-digit: one of
    '1  2  3  4  5  6  7  8  9'
```

``` bnf
octal-digit: one of
    '0  1  2  3  4  5  6  7'
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
    ''' c-char-sequence '''
    u''' c-char-sequence '''
    U''' c-char-sequence '''
    L''' c-char-sequence '''
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
    fractional-constant exponent-part\opt floating-suffix\opt
    digit-sequence exponent-part floating-suffix\opt
```

``` bnf
fractional-constant:
    digit-sequence\terminal ₒₚₜ{.} digit-sequence
    digit-sequence '.'
```

``` bnf
exponent-part:
    'e' signdₒₚₜigit-sequence
    'E' signdₒₚₜigit-sequence
```

``` bnf
sign: one of
    '+  -'
```

``` bnf
digit-sequence:
    digit
    digit-sequence digit
```

``` bnf
floating-suffix: one of
    'f  l  F  L'
```

``` bnf
string-literal:
    encoding-prefix\terminal ₒₚₜ{"} s-char-sequence\terminal ₒₚₜ{"}
    encoding-prefix\terminal ₒₚₜ{R} raw-string
```

``` bnf
encoding-prefix:
  'u8'
  'u'
  'U'
  'L'
```

``` bnf
s-char-sequence:
    s-char
    s-char-sequence s-char
```

``` bnf
raw-string:
    '"' d-char-sequence\terminal ₒₚₜ{(} r-char-sequence\terminal ₒₚₜ{)} d-char-sequence\terminal ₒₚₜ{"}
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
```

``` bnf
user-defined-floating-literal:
    fractional-constant exponent-partuₒₚₜd-suffix
    digit-sequence exponent-part ud-suffix
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
    '::' identifier
    '::' operator-function-id
    '::' literal-operator-id
    '::' template-id
```

``` bnf
nested-name-specifier:
    '::'tₒₚₜype-name '::'
    '::'nₒₚₜamespace-name '::'
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
    '[' lambda-capture\terminal ₒₚₜ{]}
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
    identifier
    '&' identifier
    'this'
```

``` bnf
lambda-declarator:
    '(' parameter-declaration-clause ')' 'mutable'\opt
    \hspace*{  inc}exception-specification\opt attribute-specifier-seq\opt trailing-return-type\opt
```

``` bnf
postfix-expression:
    primary-expression
    postfix-expression '[' expression ']'
    postfix-expression '[' braced-init-list ']'
    postfix-expression '(' expression-list\terminal ₒₚₜ{)}
    simple-type-specifier '(' expression-list\terminal ₒₚₜ{)}
    typename-specifier '(' expression-list\terminal ₒₚₜ{)}
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
    nested-name-specifier\terminal ₒₚₜ{~} type-name
    '~' decltype-specifier
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
    '::'\opt 'new' new-placement\opt new-type-id new-initializer\opt 
    '::'\opt 'new' new-placement\opt '(' type-id ')' new-initializer\opt
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
    '(' expression-list\terminal ₒₚₜ{)}
    braced-init-list
```

``` bnf
delete-expression:
    '::'\terminal ₒₚₜ{delete} cast-expression
    '::'\terminal ₒₚₜ{delete [ ]} cast-expression
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
    shift-expression '\shl' additive-expression
    shift-expression '\shr' additive-expression
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
    exclusive-or-expression '\^{}' and-expression
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
    logical-or-expression '$||$' logical-and-expression
```

``` bnf
conditional-expression:
    logical-or-expression
    logical-or-expression '?' expression ':' assignment-expression
```

``` bnf
assignment-expression:
    conditional-expression
    logical-or-expression assignment-operator initializer-clause
    throw-expression
```

``` bnf
assignment-operator: one of
    '=  *=  /=  %=   +=  -=  \shr=  \shl=  &=  \^{}=  |='
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
```

``` bnf
labeled-statement:
    attribute-specifier-seqiₒₚₜdentifier ':' statement
    attribute-specifier-seq\terminal ₒₚₜ{case} constant-expression ':' statement
    attribute-specifier-seq\terminal ₒₚₜ{default :} statement
```

``` bnf
expression-statement:
    expression\terminal ₒₚₜ{;}
```

``` bnf
compound-statement:
    \terminal{\ statement-seq\terminal ₒₚₜ{\}}
```

``` bnf
statement-seq:
    statement
    statement-seq statement
```

``` bnf
selection-statement:
    'if (' condition ')' statement
    'if (' condition ')' statement 'else' statement
    'switch (' condition ')' statement
```

``` bnf
condition:
    expression
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator '=' initializer-clause
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator braced-init-list
```

``` bnf
iteration-statement:
    'while (' condition ')' statement
    'do' statement 'while (' expression ') ;'
    'for (' for-init-statement condition\terminal ₒₚₜ{;} expression\terminal ₒₚₜ{)} statement
    'for (' for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
for-init-statement:
    expression-statement
    simple-declaration
```

``` bnf
for-range-declaration:
    attribute-specifier-seqdₒₚₜecl-specifier-seq declarator
```

``` bnf
for-range-initializer:
    expression
    braced-init-list
```

``` bnf
jump-statement:
    'break ;'
    'continue ;'
    'return' expression\terminal ₒₚₜ{;}
    'return' braced-init-list ';'
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
    function-definition
    template-declaration
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
alias-declaration:
    'using' identifier attribute-specifier-seq=ₒₚₜ type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seqiₒₚₜnit-declarator-list\terminal ₒₚₜ{;}
    attribute-specifier-seq decl-specifier-seqiₒₚₜnit-declarator-list ';'
```

``` bnf
static_assert-declaration:
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
decl-specifier:
    storage-class-specifier
    type-specifier
    function-specifier
    'friend'
    'typedef'
    'constexpr'
```

``` bnf
decl-specifier-seq:
    decl-specifier attribute-specifier-seq
 ₒₚₜ
    decl-specifier decl-specifier-seq
```

``` bnf
storage-class-specifier:
    'register'
    'static'
    'thread_local'
    'extern'
    'mutable'
```

``` bnf
function-specifier:
    'inline'
    'virtual'
    'explicit'
```

``` bnf
typedef-name:
    identifier
```

``` bnf
type-specifier:
    trailing-type-specifier
    class-specifier
    enum-specifier
```

``` bnf
trailing-type-specifier:
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
trailing-type-specifier-seq:
  trailing-type-specifier attribute-specifier-seq
 ₒₚₜ
  trailing-type-specifier trailing-type-specifier-seq
```

``` bnf
simple-type-specifier:
    nested-name-specifiertₒₚₜype-name
    nested-name-specifier 'template' simple-template-id
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
```

``` bnf
elaborated-type-specifier:
    class-key attribute-specifier-seqnₒₚₜested-name-specifieriₒₚₜdentifier
    class-key nested-name-specifier\terminal ₒₚₜ{template}sₒₚₜimple-template-id
    'enum' nested-name-specifieriₒₚₜdentifier
```

``` bnf
enum-name:
    identifier
```

``` bnf
enum-specifier:
    enum-head \terminal{\ enumerator-list\terminal ₒₚₜ{\}}
    enum-head \terminal{\ enumerator-list \terminal{, \}}
```

``` bnf
enum-head:
    enum-key attribute-specifier-seq\opt identifier\opt enum-base\opt
    enum-key attribute-specifier-seq\opt nested-name-specifier identifier
\hspace*{  inc}enum-base\opt
```

``` bnf
opaque-enum-declaration:
    enum-key attribute-specifier-seqiₒₚₜdentifier enum-base\terminal ₒₚₜ{;}
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
    identifier
```

``` bnf
namespace-name:
        original-namespace-name
        namespace-alias
```

``` bnf
original-namespace-name:
        identifier
```

``` bnf
namespace-definition:
        named-namespace-definition
        unnamed-namespace-definition
```

``` bnf
named-namespace-definition:
        original-namespace-definition
        extension-namespace-definition
```

``` bnf
original-namespace-definition:
        'inline\opt' 'namespace' identifier \terminal{\ namespace-body \terminal{\}}
```

``` bnf
extension-namespace-definition:
        'inline\opt' 'namespace' original-namespace-name \terminal{\ namespace-body \terminal{\}}
```

``` bnf
unnamed-namespace-definition:
        'inline\opt' \terminal{namespace \ namespace-body \terminal{\}}
```

``` bnf
namespace-body:
        declaration-seq\opt
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
    'using typename\opt' nested-name-specifier unqualified-id ';'
    'using ::' unqualified-id ';'
```

``` bnf
using-directive:
    attribute-specifier-seq\terminal ₒₚₜ{using  namespace} nested-name-specifiernₒₚₜamespace-name ';'
```

``` bnf
asm-definition:
    'asm (' string-literal ') ;'
```

``` bnf
linkage-specification:
    'extern' string-literal \terminal{\ declaration-seq\terminal ₒₚₜ{\}}
    \terminal{extern} string-literal declaration
```

``` bnf
attribute-specifier-seq:
  attribute-specifier-seqaₒₚₜttribute-specifier
```

``` bnf
attribute-specifier:
  '[' '[' attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  'alignas (' type-id '...'\terminal ₒₚₜ{)}
  'alignas (' alignment-expression '...'\terminal ₒₚₜ{)}
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
    '(' balanced-token-seq ')'
```

``` bnf
balanced-token-seq:
    balanced-token
 ₒₚₜ
    balanced-token-seq balanced-token
```

``` bnf
balanced-token:
    '(' balanced-token-seq ')'
    '[' balanced-token-seq ']'
    \terminal{\ balanced-token-seq \terminal{\}}
    any *token* other than a parenthesis, a bracket, or a brace
```

## Declarators <a id="gram.decl">[[gram.decl]]</a>

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
    noptr-declarator '[' constant-expression\terminal ₒₚₜ{]} attribute-specifier-seq
 ₒₚₜ
    '(' ptr-declarator ')'
```

``` bnf
parameters-and-qualifiers:
    '(' parameter-declaration-clause ')' attribute-specifier-seq\opt cv-qualifier-seq\opt
\hspace*{  inc}ref-qualifier\opt exception-specification\opt
```

``` bnf
trailing-return-type:
    '->' trailing-type-specifier-seq abstract-declarator\opt
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
    nested-name-specifiercₒₚₜlass-name
```

``` bnf
type-id:
    type-specifier-seq abstract-declarator\opt
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
    noptr-abstract-declarator\terminal ₒₚₜ{[} constant-expressionₒₚₜ ']' attribute-specifier-seq
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
    noptr-abstract-pack-declarator '[' constant-expression\ ₒₚₜ']' attribute-specifier-seq
 ₒₚₜ
    '...'
```

``` bnf
parameter-declaration-clause:
    parameter-declaration-list.ₒₚₜ..
 ₒₚₜ
    parameter-declaration-list ',' ...
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
    attribute-specifier-seqdₒₚₜecl-specifier-seq abstract-declarator\terminal ₒₚₜ{=} initializer-clause
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
    \terminal{\ initializer-list \terminal{,\opt} \terminal{\}}
    \terminal{\ \terminal{\}}
```

## Classes <a id="gram.class">[[gram.class]]</a>

``` bnf
class-name:
    identifier
    simple-template-id
```

``` bnf
class-specifier:
    class-head \terminal{\ member-specification\terminal ₒₚₜ{\}}
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
    attribute-specifier-seqdₒₚₜecl-specifier-seqmₒₚₜember-declarator-list\terminal ₒₚₜ{;}
    function-definition ';\opt'
    using-declaration
    static_assert-declaration
    template-declaration
    alias-declaration
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
    identifieraₒₚₜttribute-specifier-seq\terminal ₒₚₜ{:} constant-expression
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

## Derived classes <a id="gram.derived">[[gram.derived]]</a>

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
    attribute-specifier-seqbₒₚₜase-type-specifier
    attribute-specifier-seq\terminal ₒₚₜ{virtual} access-specifierbₒₚₜase-type-specifier
    attribute-specifier-seqaₒₚₜccess-specifier 'virtual'bₒₚₜase-type-specifier
```

``` bnf
class-or-decltype:
    nested-name-specifiercₒₚₜlass-name
    decltype-specifier
```

``` bnf
base-type-specifier:
    class-or-decltype
```

``` bnf
access-specifier:
    'private'
    'protected'
    'public'
```

## Special member functions <a id="gram.special">[[gram.special]]</a>

``` bnf
conversion-function-id:
    'operator' conversion-type-id
```

``` bnf
conversion-type-id:
    type-specifier-seq conversion-declarator\opt
```

``` bnf
conversion-declarator:
    ptr-operator conversion-declarator\opt
```

``` bnf
ctor-initializer:
    ':' mem-initializer-list
```

``` bnf
mem-initializer-list:
    mem-initializer '...'\opt
    mem-initializer ',' mem-initializer-list '...'\opt
```

``` bnf
mem-initializer:
    mem-initializer-id '(' expression-list\terminal ₒₚₜ{)}
    mem-initializer-id braced-init-list
```

``` bnf
mem-initializer-id:
    class-or-decltype
    identifier
```

## Overloading <a id="gram.over">[[gram.over]]</a>

``` bnf
operator-function-id:
    'operator' operator
```

``` bnf
literal-operator-id:
    'operator' '""' identifier
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
  'class' '...'iₒₚₜdentifier
 ₒₚₜ
  'class' identifier\terminal ₒₚₜ{=} type-id
  'typename' '...'iₒₚₜdentifier
 ₒₚₜ
  'typename' identifier\terminal ₒₚₜ{=} type-id
  'template <' template-parameter-list '> class' '...'iₒₚₜdentifier
 ₒₚₜ
  'template <' template-parameter-list '> class' identifier\terminal ₒₚₜ{=} id-expression
```

``` bnf
simple-template-id:
  template-name '<' template-argument-list\terminal ₒₚₜ{>}
```

``` bnf
template-id:
  simple-template-id
  operator-function-id '<' template-argument-list\terminal ₒₚₜ{>}
  literal-operator-id '<' template-argument-list\terminal ₒₚₜ{>}
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
throw-expression:
    'throw'  assignment-expression\opt
```

``` bnf
exception-specification:
    dynamic-exception-specification
    noexcept-specification
```

``` bnf
dynamic-exception-specification:
    'throw (' type-id-list\terminal ₒₚₜ{)}
```

``` bnf
type-id-list:
    type-id '...'\opt
    type-id-list ',' type-id '...'\opt
```

``` bnf
noexcept-specification:
    'noexcept' '(' constant-expression ')'
    'noexcept'
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
    if-section
    control-line
    text-line
    \# non-directive
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

<!-- Link reference definitions -->
[gram.basic]: #gram.basic
[gram.class]: class.md#gram.class
[gram.cpp]: cpp.md#gram.cpp
[gram.dcl]: dcl.md#gram.dcl
[gram.decl]: #gram.decl
[gram.derived]: class.md#gram.derived
[gram.except]: #gram.except
[gram.expr]: expr.md#gram.expr
[gram.key]: #gram.key
[gram.lex]: #gram.lex
[gram.over]: #gram.over
[gram.special]: #gram.special
[gram.stmt]: #gram.stmt
[gram.temp]: temp.md#gram.temp
