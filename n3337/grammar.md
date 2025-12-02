# Grammar summary (informative) <a id="gram" data-annex="true" data-annex-type="informative">[[gram]]</a>

## Keywords <a id="gram.key">[[gram.key]]</a>

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
%
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
    decimal-literal integer-suffixₒₚₜ 
    octal-literal integer-suffixₒₚₜ 
    hexadecimal-literal integer-suffixₒₚₜ
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
    '1 2 3 4 5 6 7 8 9'
```

``` bnf
octal-digit: one of
    '0 1 2 3 4 5 6 7'
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
    long-suffix unsigned-suffixₒₚₜ 
    long-long-suffix unsigned-suffixₒₚₜ
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
    fractional-constant exponent-partₒₚₜ floating-suffixₒₚₜ 
    digit-sequence exponent-part floating-suffixₒₚₜ
```

``` bnf
fractional-constant:
    digit-sequenceₒₚₜ '.' digit-sequence
    digit-sequence '.'
```

``` bnf
exponent-part:
    'e' signₒₚₜ digit-sequence
    'E' signₒₚₜ digit-sequence
```

``` bnf
sign: one of
    '+ -'
```

``` bnf
digit-sequence:
    digit
    digit-sequence digit
```

``` bnf
floating-suffix: one of
    'f l F L'
```

``` bnf
string-literal:
    encoding-prefixₒₚₜ '"' s-char-sequenceₒₚₜ '"'
    encoding-prefixₒₚₜ 'R' raw-string
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
```

``` bnf
user-defined-floating-literal:
    fractional-constant exponent-partₒₚₜ ud-suffix
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
nested-name-specifierₒₚₜ class-name '::' '~' class-name
```

``` bnf
nested-name-specifier unqualified-id
```

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
```

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
```

``` bnf
translation-unit:
    declaration-seqₒₚₜ
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
    nested-name-specifier 'template'ₒₚₜ unqualified-id
    '::' identifier
    '::' operator-function-id
    '::' literal-operator-id
    '::' template-id
```

``` bnf
nested-name-specifier:
    '::'ₒₚₜ type-name '::'
    '::'ₒₚₜ namespace-name '::'
    decltype-specifier '::'
    nested-name-specifier identifier '::'
    nested-name-specifier 'template'ₒₚₜ simple-template-id '::'
```

``` bnf
lambda-expression:
    lambda-introducer lambda-declaratorₒₚₜ compound-statement
```

``` bnf
lambda-introducer:
    '[' lambda-captureₒₚₜ ']'
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
    capture '...'ₒₚₜ 
    capture-list ',' capture '...'ₒₚₜ
```

``` bnf
capture:
    identifier
    '&' identifier
    'this'
```

``` bnf
lambda-declarator:
    '(' parameter-declaration-clause ')' 'mutable'ₒₚₜ 
    \hspace*{ inc}exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-typeₒₚₜ
```

``` bnf
postfix-expression:
    primary-expression
    postfix-expression '[' expression ']'
    postfix-expression '[' braced-init-list ']'
    postfix-expression '(' expression-listₒₚₜ ')'
    simple-type-specifier '(' expression-listₒₚₜ ')'
    typename-specifier '(' expression-listₒₚₜ ')'
    simple-type-specifier braced-init-list
    typename-specifier braced-init-list
    postfix-expression '. template'ₒₚₜ id-expression
    postfix-expression '-> template'ₒₚₜ id-expression
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
    nested-name-specifierₒₚₜ type-name ':: ~' type-name
    nested-name-specifier 'template' simple-template-id ':: ~' type-name
    nested-name-specifierₒₚₜ '~' type-name
    '~' decltype-specifier
```

``` bnf
nested-name-specifierₒₚₜ type-name ':: ~' type-name
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
    '* & + - ! ~'
```

``` bnf
new-expression:
    '::'ₒₚₜ 'new' new-placementₒₚₜ new-type-id new-initializerₒₚₜ 
    '::'ₒₚₜ 'new' new-placementₒₚₜ '(' type-id ')' new-initializerₒₚₜ
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
    '[' expression ']' attribute-specifier-seqₒₚₜ 
    noptr-new-declarator '[' constant-expression ']' attribute-specifier-seqₒₚₜ
```

``` bnf
new-initializer:
    '(' expression-listₒₚₜ ')'
    braced-init-list
```

``` bnf
'(' assignment-expression ')'
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
    exclusive-or-expression '\^' and-expression
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
assignment-expression:
    conditional-expression
    logical-or-expression assignment-operator initializer-clause
    throw-expression
```

``` bnf
assignment-operator: one of
    '= *= /= %= += -= \shr= \shl= &= \^= |='
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
labeled-statement:
    attribute-specifier-seqₒₚₜ identifier ':' statement
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
    'if (' condition ')' statement
    'if (' condition ')' statement 'else' statement
    'switch (' condition ')' statement
```

``` bnf
condition:
    expression
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator '=' initializer-clause
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator braced-init-list
```

``` bnf
'case' constant-expression ':'
```

``` bnf
iteration-statement:
    'while (' condition ')' statement
    'do' statement 'while (' expression ') ;'
    'for (' for-init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
    'for (' for-range-declaration ':' for-range-initializer ')' statement
```

``` bnf
for-init-statement:
    expression-statement
    simple-declaration
```

``` bnf
for-range-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator
```

``` bnf
for-range-initializer:
    expression
    braced-init-list
```

``` bnf
'for (' for-init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
```

``` bnf
'for (' for-range-declaration : expression ')' statement
```

``` bnf
'(' expression ')'
```

``` bnf
'for' '(' for-range-declaration ':' braced-init-list ')' statement
```

``` bnf
jump-statement:
    'break ;'
    'continue ;'
    'return' expressionₒₚₜ ';'
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
    'using' identifier attribute-specifier-seqₒₚₜ = type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seqₒₚₜ init-declarator-listₒₚₜ ';'
    attribute-specifier-seq decl-specifier-seqₒₚₜ init-declarator-list ';'
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
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ init-declarator-listₒₚₜ ';'
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
    decl-specifier attribute-specifier-seqₒₚₜ 
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
    type-specifier attribute-specifier-seqₒₚₜ 
    type-specifier type-specifier-seq
```

``` bnf
trailing-type-specifier-seq:
  trailing-type-specifier attribute-specifier-seqₒₚₜ 
  trailing-type-specifier trailing-type-specifier-seq
```

``` bnf
simple-type-specifier:
    nested-name-specifierₒₚₜ type-name
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
    class-key attribute-specifier-seqₒₚₜ nested-name-specifierₒₚₜ identifier
    class-key nested-name-specifierₒₚₜ 'template'ₒₚₜ simple-template-id
    'enum' nested-name-specifierₒₚₜ identifier
```

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
'friend' class-key '::'ₒₚₜ identifier ';'
'friend' class-key '::'ₒₚₜ simple-template-id ';'
'friend' class-key nested-name-specifier identifier ';'
'friend' class-key nested-name-specifier 'template'ₒₚₜ simple-template-id ';'
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
    enum-key attribute-specifier-seqₒₚₜ identifierₒₚₜ enum-baseₒₚₜ 
    enum-key attribute-specifier-seqₒₚₜ nested-name-specifier identifier
\hspace*{ inc}enum-baseₒₚₜ
```

``` bnf
opaque-enum-declaration:
    enum-key attribute-specifier-seqₒₚₜ identifier enum-baseₒₚₜ ';'
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
        'inline'ₒₚₜ 'namespace' identifier '{' namespace-body '}'
```

``` bnf
extension-namespace-definition:
        'inline'ₒₚₜ 'namespace' original-namespace-name '{' namespace-body '}'
```

``` bnf
unnamed-namespace-definition:
        'inline'ₒₚₜ 'namespace {' namespace-body '}'
```

``` bnf
namespace-body:
        declaration-seqₒₚₜ
```

``` bnf
'inline'ₒₚₜ 'namespace' \uniquens '{ /* empty body */ }'
'using namespace' \uniquens ';'
'namespace' \uniquens '{' namespace-body '}'
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
    nested-name-specifierₒₚₜ namespace-name
```

``` bnf
using-declaration:
    'using typename'ₒₚₜ nested-name-specifier unqualified-id ';'
    'using ::' unqualified-id ';'
```

``` bnf
using-directive:
    attribute-specifier-seqₒₚₜ 'using namespace' nested-name-specifierₒₚₜ namespace-name ';'
```

``` bnf
asm-definition:
    'asm (' string-literal ') ;'
```

``` bnf
linkage-specification:
    'extern' string-literal '{' declaration-seqₒₚₜ '}'
    'extern' string-literal declaration
```

``` bnf
attribute-specifier-seq:
  attribute-specifier-seqₒₚₜ attribute-specifier
```

``` bnf
attribute-specifier:
  '[' '[' attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  'alignas (' type-id '...'ₒₚₜ ')'
  'alignas (' alignment-expression '...'ₒₚₜ ')'
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
    '(' balanced-token-seq ')'
```

``` bnf
balanced-token-seq:
    balanced-tokenₒₚₜ 
    balanced-token-seq balanced-token
```

``` bnf
balanced-token:
    '(' balanced-token-seq ')'
    '[' balanced-token-seq ']'
    '{' balanced-token-seq '}'
    any *token* other than a parenthesis, a bracket, or a brace
```

``` bnf
init-declarator-list:
    init-declarator
    init-declarator-list ',' init-declarator
```

``` bnf
init-declarator:
    declarator initializerₒₚₜ
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
    '(' parameter-declaration-clause ')' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 
\hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ
```

``` bnf
trailing-return-type:
    '->' trailing-type-specifier-seq abstract-declaratorₒₚₜ
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
    '...'ₒₚₜ id-expression
    nested-name-specifierₒₚₜ class-name
```

``` bnf
type-id:
    type-specifier-seq abstract-declaratorₒₚₜ
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
( D1 )
```

``` bnf
'*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 'D1'
```

``` bnf
'&' attribute-specifier-seqₒₚₜ 'D1'
'&&' attribute-specifier-seqₒₚₜ 'D1'
```

``` bnf
nested-name-specifier '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ D1
```

``` bnf
'D1 [' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ
```

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
\hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
\hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-type
```

``` bnf
parameter-declaration-clause:
    parameter-declaration-listₒₚₜ ...ₒₚₜ 
    parameter-declaration-list ',' ...
```

``` bnf
parameter-declaration-list:
    parameter-declaration
    parameter-declaration-list ',' parameter-declaration
```

``` bnf
parameter-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator '=' initializer-clause
    attribute-specifier-seqₒₚₜ decl-specifier-seq abstract-declaratorₒₚₜ 
    attribute-specifier-seqₒₚₜ decl-specifier-seq abstract-declaratorₒₚₜ '=' initializer-clause
```

``` bnf
function-definition:
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator virt-specifier-seqₒₚₜ function-body
```

``` bnf
function-body:
    ctor-initializerₒₚₜ compound-statement
    function-try-block
    '= default ;'
    '= delete ;'
```

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
   
    \hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-typeₒₚₜ
```

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator ' = default ;'
```

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator ' = delete ;'
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
    initializer-clause '...'ₒₚₜ 
    initializer-list ',' initializer-clause '...'ₒₚₜ
```

``` bnf
braced-init-list:
    '{' initializer-list ','ₒₚₜ '}'
    '{' '}'
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
    member-declaration member-specificationₒₚₜ 
    access-specifier ':' member-specificationₒₚₜ
```

``` bnf
member-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ member-declarator-listₒₚₜ ';'
    function-definition ';'ₒₚₜ 
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
    declarator virt-specifier-seqₒₚₜ pure-specifierₒₚₜ 
    declarator brace-or-equal-initializerₒₚₜ 
    identifierₒₚₜ attribute-specifier-seqₒₚₜ ':' constant-expression
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
    base-specifier '...'ₒₚₜ 
    base-specifier-list ',' base-specifier '...'ₒₚₜ
```

``` bnf
base-specifier:
    attribute-specifier-seqₒₚₜ base-type-specifier
    attribute-specifier-seqₒₚₜ 'virtual' access-specifierₒₚₜ base-type-specifier
    attribute-specifier-seqₒₚₜ access-specifier 'virtual'ₒₚₜ base-type-specifier
```

``` bnf
class-or-decltype:
    nested-name-specifierₒₚₜ class-name
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
'operator' conversion-type-id '( )' attribute-specifier-seqₒₚₜ cv-qualifier ';'
```

``` bnf
'R' call-function '(' conversion-type-id 'F, P1 a1, ... ,Pn an)' '{ return F (a1,... ,an); }'
```

``` bnf
operator-function-id:
    'operator' operator
```

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

``` bnf
postfix-expression '[' expression ']'
```

``` bnf
postfix-expression '[' braced-init-list ']'
```

``` bnf
postfix-expression '->' 'template'ₒₚₜ id-expression\\
postfix-expression '->' pseudo-destructor-name
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
  'class' '...'ₒₚₜ identifierₒₚₜ 
  'class' identifierₒₚₜ '=' type-id
  'typename' '...'ₒₚₜ identifierₒₚₜ 
  'typename' identifierₒₚₜ '=' type-id
  'template <' template-parameter-list '> class' '...'ₒₚₜ identifierₒₚₜ 
  'template <' template-parameter-list '> class' identifierₒₚₜ '=' id-expression
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
typename-specifier:
  'typename' nested-name-specifier identifier
  'typename' nested-name-specifier 'template'ₒₚₜ simple-template-id
```

``` bnf
explicit-instantiation:
  'extern'ₒₚₜ 'template' declaration
```

``` bnf
explicit-specialization:
  'template < >' declaration
```


## Preprocessing directives <a id="gram.cpp">[[gram.cpp]]</a>

``` bnf
preprocessing-file:
    groupₒₚₜ
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
    if-group elif-groupsₒₚₜ else-groupₒₚₜ endif-line
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
'defined' identifier
```

``` bnf
'defined (' identifier ')'
```

``` bnf
'# include <'h-char-sequence'>' new-line
```

``` bnf
'# include "'q-char-sequence'"' new-line
```

``` bnf
'# include <'h-char-sequence'>' new-line
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
'# error' pp-tokensₒₚₜ new-line
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
    'try' compound-statement handler-seq
```

``` bnf
function-try-block:
    'try' ctor-initializerₒₚₜ compound-statement handler-seq
```

``` bnf
handler-seq:
    handler handler-seqₒₚₜ
```

``` bnf
handler:
    'catch (' exception-declaration ')' compound-statement
```

``` bnf
exception-declaration:
    attribute-specifier-seqₒₚₜ type-specifier-seq declarator
    attribute-specifier-seqₒₚₜ type-specifier-seq abstract-declaratorₒₚₜ 
    '...'
```

``` bnf
throw-expression:
    'throw' assignment-expressionₒₚₜ
```

``` bnf
exception-specification:
    dynamic-exception-specification
    noexcept-specification
```

``` bnf
dynamic-exception-specification:
    'throw (' type-id-listₒₚₜ ')'
```

``` bnf
type-id-list:
    type-id '...'ₒₚₜ 
    type-id-list ',' type-id '...'ₒₚₜ
```

``` bnf
noexcept-specification:
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
