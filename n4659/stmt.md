# Statements <a id="stmt.stmt">[[stmt.stmt]]</a>

Except as indicated, statements are executed in sequence.

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

The optional *attribute-specifier-seq* appertains to the respective
statement.

The rules for *condition*s apply both to *selection-statement*s and to
the `for` and `while` statements ( [[stmt.iter]]). The *declarator*
shall not specify a function or an array. The *decl-specifier-seq* shall
not define a class or enumeration. If the `auto` *type-specifier*
appears in the *decl-specifier-seq*, the type of the identifier being
declared is deduced from the initializer as described in 
[[dcl.spec.auto]].

A name introduced by a declaration in a *condition* (either introduced
by the *decl-specifier-seq* or the *declarator* of the condition) is in
scope from its point of declaration until the end of the substatements
controlled by the condition. If the name is redeclared in the outermost
block of a substatement controlled by the condition, the declaration
that redeclares the name is ill-formed.

[*Example 1*:

``` cpp
if (int x = f()) {
  int x;            // ill-formed, redeclaration of x
}
else {
  int x;            // ill-formed, redeclaration of x
}
```

— *end example*]

The value of a *condition* that is an initialized declaration in a
statement other than a `switch` statement is the value of the declared
variable contextually converted to `bool` (Clause  [[conv]]). If that
conversion is ill-formed, the program is ill-formed. The value of a
*condition* that is an initialized declaration in a `switch` statement
is the value of the declared variable if it has integral or enumeration
type, or of that variable implicitly converted to integral or
enumeration type otherwise. The value of a *condition* that is an
expression is the value of the expression, contextually converted to
`bool` for statements other than `switch`; if that conversion is
ill-formed, the program is ill-formed. The value of the condition will
be referred to as simply “the condition” where the usage is unambiguous.

If a *condition* can be syntactically resolved as either an expression
or the declaration of a block-scope name, it is interpreted as a
declaration.

In the *decl-specifier-seq* of a *condition*, each *decl-specifier*
shall be either a *type-specifier* or `constexpr`.

## Labeled statement <a id="stmt.label">[[stmt.label]]</a>

A statement can be labeled.

``` bnf
labeled-statement:
    attribute-specifier-seqiₒₚₜdentifier ':' statement
    attribute-specifier-seqₒₚₜ 'case' constant-expression ':' statement
    attribute-specifier-seqₒₚₜ 'default :' statement
```

The optional *attribute-specifier-seq* appertains to the label. An
*identifier label* declares the identifier. The only use of an
identifier label is as the target of a `goto`. The scope of a label is
the function in which it appears. Labels shall not be redeclared within
a function. A label can be used in a `goto` statement before its
declaration. Labels have their own name space and do not interfere with
other identifiers.

[*Note 1*: A label may have the same name as another declaration in the
same scope or a *template-parameter* from an enclosing scope.
Unqualified name lookup ( [[basic.lookup.unqual]]) ignores
labels. — *end note*]

Case labels and default labels shall occur only in switch statements.

## Expression statement <a id="stmt.expr">[[stmt.expr]]</a>

Expression statements have the form

``` bnf
expression-statement:
    expressionₒₚₜ ';'
```

The expression is a discarded-value expression (Clause  [[expr]]). All
side effects from an expression statement are completed before the next
statement is executed. An expression statement with the expression
missing is called a *null statement*.

[*Note 1*: Most statements are expression statements — usually
assignments or function calls. A null statement is useful to carry a
label just before the `}` of a compound statement and to supply a null
body to an iteration statement such as a `while` statement (
[[stmt.while]]). — *end note*]

## Compound statement or block <a id="stmt.block">[[stmt.block]]</a>

So that several statements can be used where one is expected, the
compound statement (also, and equivalently, called “block”) is provided.

``` bnf
compound-statement:
    \terminal{\ statement-seqₒₚₜ \terminal{\}}
```

``` bnf
statement-seq:
    statement
    statement-seq statement
```

A compound statement defines a block scope ( [[basic.scope]]).

[*Note 1*: A declaration is a *statement* (
[[stmt.dcl]]). — *end note*]

## Selection statements <a id="stmt.select">[[stmt.select]]</a>

Selection statements choose one of several flows of control.

``` bnf
selection-statement:
    'if constexpr(ₒₚₜ' init-statementcₒₚₜondition ')' statement
    'if constexpr(ₒₚₜ' init-statementcₒₚₜondition ')' statement 'else' statement
    'switch (' init-statementcₒₚₜondition ')' statement
```

See  [[dcl.meaning]] for the optional *attribute-specifier-seq* in a
condition.

[*Note 1*: An *init-statement* ends with a semicolon. — *end note*]

In Clause  [[stmt.stmt]], the term *substatement* refers to the
contained *statement* or *statement*s that appear in the syntax
notation. The substatement in a *selection-statement* (each
substatement, in the `else` form of the `if` statement) implicitly
defines a block scope ( [[basic.scope]]). If the substatement in a
selection-statement is a single statement and not a
*compound-statement*, it is as if it was rewritten to be a
compound-statement containing the original substatement.

[*Example 1*:

``` cpp
if (x)
  int i;
```

can be equivalently rewritten as

``` cpp
if (x) {
  int i;
}
```

Thus after the `if` statement, `i` is no longer in scope.

— *end example*]

### The `if` statement <a id="stmt.if">[[stmt.if]]</a>

If the condition ( [[stmt.select]]) yields `true` the first substatement
is executed. If the `else` part of the selection statement is present
and the condition yields `false`, the second substatement is executed.
If the first substatement is reached via a label, the condition is not
evaluated and the second substatement is not executed. In the second
form of `if` statement (the one including `else`), if the first
substatement is also an `if` statement then that inner `if` statement
shall contain an `else` part.[^1]

If the `if` statement is of the form `if constexpr`, the value of the
condition shall be a contextually converted constant expression of type
`bool` ( [[expr.const]]); this form is called a *constexpr if*
statement. If the value of the converted condition is `false`, the first
substatement is a *discarded statement*, otherwise the second
substatement, if present, is a discarded statement. During the
instantation of an enclosing templated entity (Clause  [[temp]]), if the
condition is not value-dependent after its instantiation, the discarded
substatement (if any) is not instantiated.

[*Note 1*: Odr-uses ( [[basic.def.odr]]) in a discarded statement do
not require an entity to be defined. — *end note*]

A `case` or `default` label appearing within such an `if` statement
shall be associated with a `switch` statement ( [[stmt.switch]]) within
the same `if` statement. A label ( [[stmt.label]]) declared in a
substatement of a constexpr if statement shall only be referred to by a
statement ( [[stmt.goto]]) in the same substatement.

[*Example 1*:

``` cpp
template<typename T, typename ... Rest> void g(T&& p, Rest&& ...rs) {
  // ... handle p

  if constexpr (sizeof...(rs) > 0)
    g(rs...);       // never instantiated with an empty argument list
}

extern int x;       // no definition of x required

int f() {
  if constexpr (true)
    return 0;
  else if (x)
    return x;
  else
    return -x;
}
```

— *end example*]

An `if` statement of the form

``` bnf
'if constexpr(ₒₚₜ' init-statement condition ')' statement
```

is equivalent to

and an `if` statement of the form

``` bnf
'if constexpr(ₒₚₜ' init-statement condition ')' statement 'else' statement
```

is equivalent to

except that names declared in the *init-statement* are in the same
declarative region as those declared in the *condition*.

### The `switch` statement <a id="stmt.switch">[[stmt.switch]]</a>

The `switch` statement causes control to be transferred to one of
several statements depending on the value of a condition.

The condition shall be of integral type, enumeration type, or class
type. If of class type, the condition is contextually implicitly
converted (Clause  [[conv]]) to an integral or enumeration type. If the
(possibly converted) type is subject to integral promotions (
[[conv.prom]]), the condition is converted to the promoted type. Any
statement within the `switch` statement can be labeled with one or more
case labels as follows:

``` bnf
'case' constant-expression ':'
```

where the *constant-expression* shall be a converted constant
expression ( [[expr.const]]) of the adjusted type of the switch
condition. No two of the case constants in the same switch shall have
the same value after conversion.

There shall be at most one label of the form

``` cpp
default :
```

within a `switch` statement.

Switch statements can be nested; a `case` or `default` label is
associated with the smallest switch enclosing it.

When the `switch` statement is executed, its condition is evaluated and
compared with each case constant. If one of the case constants is equal
to the value of the condition, control is passed to the statement
following the matched case label. If no case constant matches the
condition, and if there is a `default` label, control passes to the
statement labeled by the default label. If no case matches and if there
is no `default` then none of the statements in the switch is executed.

`case` and `default` labels in themselves do not alter the flow of
control, which continues unimpeded across such labels. To exit from a
switch, see `break`,  [[stmt.break]].

[*Note 1*: Usually, the substatement that is the subject of a switch is
compound and `case` and `default` labels appear on the top-level
statements contained within the (compound) substatement, but this is not
required. Declarations can appear in the substatement of a `switch`
statement. — *end note*]

A `switch` statement of the form

``` bnf
'switch (' init-statement condition ')' statement
```

is equivalent to

except that names declared in the *init-statement* are in the same
declarative region as those declared in the *condition*.

## Iteration statements <a id="stmt.iter">[[stmt.iter]]</a>

Iteration statements specify looping.

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

See  [[dcl.meaning]] for the optional *attribute-specifier-seq* in a
*for-range-declaration*.

[*Note 1*: An *init-statement* ends with a semicolon. — *end note*]

The substatement in an *iteration-statement* implicitly defines a block
scope ( [[basic.scope]]) which is entered and exited each time through
the loop.

If the substatement in an iteration-statement is a single statement and
not a *compound-statement*, it is as if it was rewritten to be a
compound-statement containing the original statement.

[*Example 1*:

``` cpp
while (--x >= 0)
  int i;
```

can be equivalently rewritten as

``` cpp
while (--x >= 0) {
  int i;
}
```

Thus after the `while` statement, `i` is no longer in scope.

— *end example*]

If a name introduced in an *init-statement* or *for-range-declaration*
is redeclared in the outermost block of the substatement, the program is
ill-formed.

[*Example 2*:

``` cpp
void f() {
  for (int i = 0; i < 10; ++i)
    int i = 0;          // error: redeclaration
  for (int i : { 1, 2, 3 })
    int i = 1;          // error: redeclaration
}
```

— *end example*]

### The `while` statement <a id="stmt.while">[[stmt.while]]</a>

In the `while` statement the substatement is executed repeatedly until
the value of the condition ( [[stmt.select]]) becomes `false`. The test
takes place before each execution of the substatement.

When the condition of a `while` statement is a declaration, the scope of
the variable that is declared extends from its point of declaration (
[[basic.scope.pdecl]]) to the end of the `while` *statement*. A `while`
statement of the form

``` cpp
while (T t = x) statement
```

is equivalent to

``` cpp
label:
{                   // start of condition scope
  T t = x;
  if (t) {
    statement
    goto label;
  }
}                   // end of condition scope
```

The variable created in a condition is destroyed and created with each
iteration of the loop.

[*Example 1*:

``` cpp
struct A {
  int val;
  A(int i) : val(i) { }
  ~A() { }
  operator bool() { return val != 0; }
};
int i = 1;
while (A a = i) {
  // ...
  i = 0;
}
```

In the while-loop, the constructor and destructor are each called twice,
once for the condition that succeeds and once for the condition that
fails.

— *end example*]

### The `do` statement <a id="stmt.do">[[stmt.do]]</a>

The expression is contextually converted to `bool` (Clause  [[conv]]);
if that conversion is ill-formed, the program is ill-formed.

In the `do` statement the substatement is executed repeatedly until the
value of the expression becomes `false`. The test takes place after each
execution of the statement.

### The `for` statement <a id="stmt.for">[[stmt.for]]</a>

The `for` statement

``` bnf
'for (' init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
```

is equivalent to

except that names declared in the *init-statement* are in the same
declarative region as those declared in the *condition*, and except that
a `continue` in *statement* (not enclosed in another iteration
statement) will execute *expression* before re-evaluating *condition*.

[*Note 1*: Thus the first statement specifies initialization for the
loop; the condition ( [[stmt.select]]) specifies a test, sequenced
before each iteration, such that the loop is exited when the condition
becomes `false`; the expression often specifies incrementing that is
sequenced after each iteration. — *end note*]

Either or both of the *condition* and the *expression* can be omitted. A
missing *condition* makes the implied `while` clause equivalent to
`while(true)`.

If the *init-statement* is a declaration, the scope of the name(s)
declared extends to the end of the `for` statement.

[*Example 1*:

``` cpp
int i = 42;
int a[10];

for (int i = 0; i < 10; i++)
  a[i] = i;

int j = i;          // j = 42
```

— *end example*]

### The range-based `for` statement <a id="stmt.ranged">[[stmt.ranged]]</a>

The range-based `for` statement

``` bnf
'for (' for-range-declaration ':' for-range-initializer ')' statement
```

is equivalent to

where

- if the *for-range-initializer* is an *expression*, it is regarded as
  if it were surrounded by parentheses (so that a comma operator cannot
  be reinterpreted as delimiting two *init-declarator*s);
- `__range`, `__begin`, and `__end` are variables defined for exposition
  only; and
- *begin-expr* and *end-expr* are determined as follows:
  - if the *for-range-initializer* is an expression of array type `R`,
    *begin-expr* and *end-expr* are `__range` and `__range + __bound`,
    respectively, where `__bound` is the array bound. If `R` is an array
    of unknown bound or an array of incomplete type, the program is
    ill-formed;
  - if the *for-range-initializer* is an expression of class type `C`,
    the *unqualified-id*s `begin` and `end` are looked up in the scope
    of `C` as if by class member access lookup (
    [[basic.lookup.classref]]), and if either (or both) finds at least
    one declaration, *begin-expr* and *end-expr* are `__range.begin()`
    and `__range.end()`, respectively;
  - otherwise, *begin-expr* and *end-expr* are `begin(__range)` and
    `end(__range)`, respectively, where `begin` and `end` are looked up
    in the associated namespaces ( [[basic.lookup.argdep]]).
    \[*Note 1*: Ordinary unqualified lookup ( [[basic.lookup.unqual]])
    is not performed. — *end note*]

[*Example 1*:

``` cpp
int array[5] = { 1, 2, 3, 4, 5 };
for (int& x : array)
  x *= 2;
```

— *end example*]

In the *decl-specifier-seq* of a *for-range-declaration*, each
*decl-specifier* shall be either a *type-specifier* or `constexpr`. The
*decl-specifier-seq* shall not define a class or enumeration.

## Jump statements <a id="stmt.jump">[[stmt.jump]]</a>

Jump statements unconditionally transfer control.

``` bnf
jump-statement:
    'break ;'
    'continue ;'
    'return' expr-or-braced-init-listₒₚₜ ';'
    'goto' identifier ';'
```

On exit from a scope (however accomplished), objects with automatic
storage duration ( [[basic.stc.auto]]) that have been constructed in
that scope are destroyed in the reverse order of their construction.

[*Note 1*: For temporaries, see  [[class.temporary]]. — *end note*]

Transfer out of a loop, out of a block, or back past an initialized
variable with automatic storage duration involves the destruction of
objects with automatic storage duration that are in scope at the point
transferred from but not at the point transferred to. (See  [[stmt.dcl]]
for transfers into blocks).

[*Note 2*: However, the program can be terminated (by calling
`std::exit()` or `std::abort()` ( [[support.start.term]]), for example)
without destroying class objects with automatic storage
duration. — *end note*]

### The `break` statement <a id="stmt.break">[[stmt.break]]</a>

The `break` statement shall occur only in an *iteration-statement* or a
`switch` statement and causes termination of the smallest enclosing
*iteration-statement* or `switch` statement; control passes to the
statement following the terminated statement, if any.

### The `continue` statement <a id="stmt.cont">[[stmt.cont]]</a>

The `continue` statement shall occur only in an *iteration-statement*
and causes control to pass to the loop-continuation portion of the
smallest enclosing *iteration-statement*, that is, to the end of the
loop. More precisely, in each of the statements

``` cpp
while (foo) {
  {
    // ...
  }
contin: ;
}
```

``` cpp
do {
  {
    // ...
  }
contin: ;
} while (foo);
```

``` cpp
for (;;) {
  {
    // ...
  }
contin: ;
}
```

a `continue` not contained in an enclosed iteration statement is
equivalent to `goto` `contin`.

### The `return` statement <a id="stmt.return">[[stmt.return]]</a>

A function returns to its caller by the `return` statement.

The *expr-or-braced-init-list* of a return statement is called its
operand. A return statement with no operand shall be used only in a
function whose return type is cv `void`, a constructor (
[[class.ctor]]), or a destructor ( [[class.dtor]]). A return statement
with an operand of type `void` shall be used only in a function whose
return type is cv `void`. A return statement with any other operand
shall be used only in a function whose return type is not cv `void`; the
return statement initializes the glvalue result or prvalue result object
of the (explicit or implicit) function call by copy-initialization (
[[dcl.init]]) from the operand.

[*Note 1*: A return statement can involve an invocation of a
constructor to perform a copy or move of the operand if it is not a
prvalue or if its type differs from the return type of the function. A
copy operation associated with a return statement may be elided or
converted to a move operation if an automatic storage duration variable
is returned ( [[class.copy]]). — *end note*]

[*Example 1*:

``` cpp
std::pair<std::string,int> f(const char* p, int x) {
  return {p,x};
}
```

— *end example*]

Flowing off the end of a constructor, a destructor, or a function with a
cv `void` return type is equivalent to a `return` with no operand.
Otherwise, flowing off the end of a function other than `main` (
[[basic.start.main]]) results in undefined behavior.

The copy-initialization of the result of the call is sequenced before
the destruction of temporaries at the end of the full-expression
established by the operand of the return statement, which, in turn, is
sequenced before the destruction of local variables ( [[stmt.jump]]) of
the block enclosing the return statement.

### The `goto` statement <a id="stmt.goto">[[stmt.goto]]</a>

The `goto` statement unconditionally transfers control to the statement
labeled by the identifier. The identifier shall be a label (
[[stmt.label]]) located in the current function.

## Declaration statement <a id="stmt.dcl">[[stmt.dcl]]</a>

A declaration statement introduces one or more new identifiers into a
block; it has the form

``` bnf
declaration-statement:
    block-declaration
```

If an identifier introduced by a declaration was previously declared in
an outer block, the outer declaration is hidden for the remainder of the
block, after which it resumes its force.

Variables with automatic storage duration ( [[basic.stc.auto]]) are
initialized each time their *declaration-statement* is executed.
Variables with automatic storage duration declared in the block are
destroyed on exit from the block ( [[stmt.jump]]).

It is possible to transfer into a block, but not in a way that bypasses
declarations with initialization. A program that jumps[^2] from a point
where a variable with automatic storage duration is not in scope to a
point where it is in scope is ill-formed unless the variable has scalar
type, class type with a trivial default constructor and a trivial
destructor, a cv-qualified version of one of these types, or an array of
one of the preceding types and is declared without an *initializer* (
[[dcl.init]]).

[*Example 1*:

``` cpp
void f() {
  // ...
  goto lx;          // ill-formed: jump into scope of a
  // ...
ly:
  X a = 1;
  // ...
lx:
  goto ly;          // OK, jump implies destructor call for a followed by
                    // construction again immediately following label ly
}
```

— *end example*]

Dynamic initialization of a block-scope variable with static storage
duration ( [[basic.stc.static]]) or thread storage duration (
[[basic.stc.thread]]) is performed the first time control passes through
its declaration; such a variable is considered initialized upon the
completion of its initialization. If the initialization exits by
throwing an exception, the initialization is not complete, so it will be
tried again the next time control enters the declaration. If control
enters the declaration concurrently while the variable is being
initialized, the concurrent execution shall wait for completion of the
initialization.[^3] If control re-enters the declaration recursively
while the variable is being initialized, the behavior is undefined.

[*Example 2*:

``` cpp
int foo(int i) {
  static int s = foo(2*i);      // recursive call - undefined
  return i+1;
}
```

— *end example*]

The destructor for a block-scope object with static or thread storage
duration will be executed if and only if it was constructed.

[*Note 1*:  [[basic.start.term]] describes the order in which
block-scope objects with static and thread storage duration are
destroyed. — *end note*]

## Ambiguity resolution <a id="stmt.ambig">[[stmt.ambig]]</a>

There is an ambiguity in the grammar involving *expression-statement*s
and *declaration*s: An *expression-statement* with a function-style
explicit type conversion ( [[expr.type.conv]]) as its leftmost
subexpression can be indistinguishable from a *declaration* where the
first *declarator* starts with a `(`. In those cases the *statement* is
a *declaration*.

[*Note 1*:

If the *statement* cannot syntactically be a *declaration*, there is no
ambiguity, so this rule does not apply. The whole *statement* might need
to be examined to determine whether this is the case. This resolves the
meaning of many examples.

[*Example 1*:

Assuming `T` is a *simple-type-specifier* ( [[dcl.type]]),

``` cpp
T(a)->m = 7;        // expression-statement
T(a)++;             // expression-statement
T(a,5)<<c;          // expression-statement

T(*d)(int);         //  declaration
T(e)[5];            //  declaration
T(f) = { 1, 2 };    //  declaration
T(*g)(double(3));   //  declaration
```

In the last example above, `g`, which is a pointer to `T`, is
initialized to `double(3)`. This is of course ill-formed for semantic
reasons, but that does not affect the syntactic analysis.

— *end example*]

The remaining cases are *declaration*s.

[*Example 2*:

``` cpp
class T {
  // ...
public:
  T();
  T(int);
  T(int, int);
};
T(a);               //  declaration
T(*b)();            //  declaration
T(c)=7;             //  declaration
T(d),e,f=3;         //  declaration
extern int h;
T(g)(h,2);          //  declaration
```

— *end example*]

— *end note*]

The disambiguation is purely syntactic; that is, the meaning of the
names occurring in such a statement, beyond whether they are
*type-name*s or not, is not generally used in or changed by the
disambiguation. Class templates are instantiated as necessary to
determine if a qualified name is a *type-name*. Disambiguation precedes
parsing, and a statement disambiguated as a declaration may be an
ill-formed declaration. If, during parsing, a name in a template
parameter is bound differently than it would be bound during a trial
parse, the program is ill-formed. No diagnostic is required.

[*Note 2*: This can occur only when the name is declared earlier in the
declaration. — *end note*]

[*Example 3*:

``` cpp
struct T1 {
  T1 operator()(int x) { return T1(x); }
  int operator=(int x) { return x; }
  T1(int) { }
};
struct T2 { T2(int){ } };
int a, (*(*b)(T2))(int), c, d;

void f() {
  // disambiguation requires this to be parsed as a declaration:
  T1(a) = 3,
  T2(4),                        // T2 will be declared as a variable of type T1, but this will not
  (*(*b)(T2(c)))(int(d));       // allow the last part of the declaration to parse properly,
                                // since it depends on T2 being a type-name
}
```

— *end example*]

<!-- Section link definitions -->
[stmt.ambig]: #stmt.ambig
[stmt.block]: #stmt.block
[stmt.break]: #stmt.break
[stmt.cont]: #stmt.cont
[stmt.dcl]: #stmt.dcl
[stmt.do]: #stmt.do
[stmt.expr]: #stmt.expr
[stmt.for]: #stmt.for
[stmt.goto]: #stmt.goto
[stmt.if]: #stmt.if
[stmt.iter]: #stmt.iter
[stmt.jump]: #stmt.jump
[stmt.label]: #stmt.label
[stmt.ranged]: #stmt.ranged
[stmt.return]: #stmt.return
[stmt.select]: #stmt.select
[stmt.stmt]: #stmt.stmt
[stmt.switch]: #stmt.switch
[stmt.while]: #stmt.while

<!-- Link reference definitions -->
[basic.def.odr]: basic.md#basic.def.odr
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.classref]: basic.md#basic.lookup.classref
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope]: basic.md#basic.scope
[basic.scope.pdecl]: basic.md#basic.scope.pdecl
[basic.start.main]: basic.md#basic.start.main
[basic.start.term]: basic.md#basic.start.term
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.dtor]: special.md#class.dtor
[class.temporary]: special.md#class.temporary
[conv]: conv.md#conv
[conv.prom]: conv.md#conv.prom
[dcl.init]: dcl.md#dcl.init
[dcl.meaning]: dcl.md#dcl.meaning
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.type]: dcl.md#dcl.type
[expr]: expr.md#expr
[expr.const]: expr.md#expr.const
[expr.type.conv]: expr.md#expr.type.conv
[stmt.break]: #stmt.break
[stmt.dcl]: #stmt.dcl
[stmt.goto]: #stmt.goto
[stmt.iter]: #stmt.iter
[stmt.jump]: #stmt.jump
[stmt.label]: #stmt.label
[stmt.select]: #stmt.select
[stmt.stmt]: #stmt.stmt
[stmt.switch]: #stmt.switch
[stmt.while]: #stmt.while
[support.start.term]: language.md#support.start.term
[temp]: temp.md#temp

[^1]: In other words, the `else` is associated with the nearest un-elsed
    `if`.

[^2]: The transfer from the condition of a `switch` statement to a
    `case` label is considered a jump in this respect.

[^3]: The implementation must not introduce any deadlock around
    execution of the initializer. Deadlocks might still be caused by the
    program logic; the implementation need only avoid deadlocks due to
    its own synchronization operations.
