# Statements <a id="stmt.stmt">[[stmt.stmt]]</a>

## Preamble <a id="stmt.pre">[[stmt.pre]]</a>

Except as indicated, statements are executed in sequence.

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

The optional *attribute-specifier-seq* appertains to the respective
statement.

A *substatement* of a *statement* is one of the following:

- for a *labeled-statement*, its *statement*,
- for a *compound-statement*, any *statement* of its *statement-seq*,
- for a *selection-statement*, any of its *statement*s or
  *compound-statement*s (but not its *init-statement*), or
- for an *iteration-statement*, its *statement* (but not an
  *init-statement*).

[*Note 1*: The *compound-statement* of a *lambda-expression* is not a
substatement of the *statement* (if any) in which the
*lambda-expression* lexically appears. — *end note*]

A *statement* `S1` *encloses* a *statement* `S2` if

- `S2` is a substatement of `S1`,
- `S1` is a *selection-statement* or *iteration-statement* and `S2` is
  the *init-statement* of `S1`,
- `S1` is a *try-block* and `S2` is its *compound-statement* or any of
  the *compound-statement*s of its *handler*s, or
- `S1` encloses a statement `S3` and `S3` encloses `S2`.

A statement `S1` is *enclosed by* a statement `S2` if `S2` encloses
`S1`.

The rules for *condition*s apply both to *selection-statement*s
[[stmt.select]] and to the `for` and `while` statements [[stmt.iter]]. A
*condition* that is not an *expression* is a declaration [[dcl.dcl]].
The *declarator* shall not specify a function or an array. The
*decl-specifier-seq* shall not define a class or enumeration. If the
`auto` *type-specifier* appears in the *decl-specifier-seq*, the type of
the identifier being declared is deduced from the initializer as
described in  [[dcl.spec.auto]].

The value of a *condition* that is an initialized declaration in a
statement other than a `switch` statement is the value of the declared
variable contextually converted to `bool` [[conv]]. If that conversion
is ill-formed, the program is ill-formed. The value of a *condition*
that is an expression is the value of the expression, contextually
converted to `bool` for statements other than `switch`; if that
conversion is ill-formed, the program is ill-formed. The value of the
condition will be referred to as simply “the condition” where the usage
is unambiguous.

If a *condition* can be syntactically resolved as either an expression
or a declaration, it is interpreted as the latter.

In the *decl-specifier-seq* of a *condition*, each *decl-specifier*
shall be either a *type-specifier* or `constexpr`.

## Label <a id="stmt.label">[[stmt.label]]</a>

A label can be added to a statement or used anywhere in a
*compound-statement*.

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

The optional *attribute-specifier-seq* appertains to the label. The only
use of a label with an *identifier* is as the target of a `goto`. No two
labels in a function shall have the same *identifier*. A label can be
used in a `goto` statement before its introduction.

A *labeled-statement* whose *label* is a `case` or `default` label shall
be enclosed by [[stmt.pre]] a `switch` statement [[stmt.switch]].

A *control-flow-limited statement* is a statement `S` for which:

- a `case` or `default` label appearing within `S` shall be associated
  with a `switch` statement [[stmt.switch]] within `S`, and
- a label declared in `S` shall only be referred to by a statement
  [[stmt.goto]] in `S`.

## Expression statement <a id="stmt.expr">[[stmt.expr]]</a>

Expression statements have the form

``` bnf
expression-statement:
    expressionₒₚₜ ';'
```

The expression is a discarded-value expression [[expr.context]]. All
side effects from an expression statement are completed before the next
statement is executed. An expression statement with the expression
missing is called a *null statement*.

[*Note 1*: Most statements are expression statements — usually
assignments or function calls. A null statement is useful to supply a
null body to an iteration statement such as a `while` statement
[[stmt.while]]. — *end note*]

## Compound statement or block <a id="stmt.block">[[stmt.block]]</a>

A *compound statement* (also known as a block) groups a sequence of
statements into a single statement.

``` bnf
compound-statement:
    \terminal{\ statement-seqₒₚₜ label-seqₒₚₜ \terminal{\}}
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

A label at the end of a *compound-statement* is treated as if it were
followed by a null statement.

[*Note 1*: A compound statement defines a block scope [[basic.scope]].
A declaration is a *statement* [[stmt.dcl]]. — *end note*]

## Selection statements <a id="stmt.select">[[stmt.select]]</a>

### General <a id="stmt.select.general">[[stmt.select.general]]</a>

Selection statements choose one of several flows of control.

``` bnf
selection-statement:
    if constexprₒₚₜ '(' init-statementₒₚₜ condition ')' statement
    if constexprₒₚₜ '(' init-statementₒₚₜ condition ')' statement else statement
    if '!'ₒₚₜ consteval compound-statement
    if '!'ₒₚₜ consteval compound-statement else statement
    switch '(' init-statementₒₚₜ condition ')' statement
```

See  [[dcl.meaning]] for the optional *attribute-specifier-seq* in a
condition.

[*Note 1*: An *init-statement* ends with a semicolon. — *end note*]

[*Note 2*: Each *selection-statement* and each substatement of a
*selection-statement* has a block scope
[[basic.scope.block]]. — *end note*]

### The `if` statement <a id="stmt.if">[[stmt.if]]</a>

If the condition [[stmt.pre]] yields `true` the first substatement is
executed. If the `else` part of the selection statement is present and
the condition yields `false`, the second substatement is executed. If
the first substatement is reached via a label, the condition is not
evaluated and the second substatement is not executed. In the second
form of `if` statement (the one including `else`), if the first
substatement is also an `if` statement then that inner `if` statement
shall contain an `else` part.[^1]

If the `if` statement is of the form `if constexpr`, the value of the
condition is contextually converted to `bool` and the converted
expression shall be a constant expression [[expr.const]]; this form is
called a *constexpr if* statement. If the value of the converted
condition is `false`, the first substatement is a *discarded statement*,
otherwise the second substatement, if present, is a discarded statement.
During the instantiation of an enclosing templated entity [[temp.pre]],
if the condition is not value-dependent after its instantiation, the
discarded substatement (if any) is not instantiated. Each substatement
of a constexpr if statement is a control-flow-limited statement
[[stmt.label]].

[*Example 1*:

``` cpp
if constexpr (sizeof(int[2])) {}        // OK, narrowing allowed
```

— *end example*]

[*Note 1*: Odr-uses [[term.odr.use]] in a discarded statement do not
require an entity to be defined. — *end note*]

[*Example 2*:

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
if constexprₒₚₜ '(' init-statement condition ')' statement
```

is equivalent to

``` bnf
'{'
   init-statement
   if constexprₒₚₜ '(' condition ')' statement
'}'
```

and an `if` statement of the form

``` bnf
if constexprₒₚₜ '(' init-statement condition ')' statement else statement
```

is equivalent to

``` bnf
'{'
   init-statement
   if constexprₒₚₜ '(' condition ')' statement else statement
'}'
```

except that the *init-statement* is in the same scope as the
*condition*.

An `if` statement of the form `if consteval` is called a
*consteval if statement*. The *statement*, if any, in a consteval if
statement shall be a *compound-statement*.

[*Example 3*:

``` cpp
constexpr void f(bool b) {
  if (true)
    if consteval { }
    else ;              // error: not a compound-statement; else not associated with outer if
}
```

— *end example*]

If a consteval if statement is evaluated in a context that is manifestly
constant-evaluated [[expr.const]], the first substatement is executed.

[*Note 2*: The first substatement is an immediate function
context. — *end note*]

Otherwise, if the `else` part of the selection statement is present,
then the second substatement is executed. Each substatement of a
consteval if statement is a control-flow-limited statement
[[stmt.label]].

An `if` statement of the form

``` bnf
if '!' consteval compound-statement
```

is not itself a consteval if statement, but is equivalent to the
consteval if statement

``` bnf
if consteval \terminal{\ \terminal{\}} else compound-statement
```

An `if` statement of the form

``` bnf
if '!' consteval compound-statement₁ else statement₂
```

is not itself a consteval if statement, but is equivalent to the
consteval if statement

``` bnf
if consteval statement₂ else compound-statement₁
```

### The `switch` statement <a id="stmt.switch">[[stmt.switch]]</a>

The `switch` statement causes control to be transferred to one of
several statements depending on the value of a condition.

The value of a *condition* that is an initialized declaration is the
value of the declared variable, or the value of the *expression*
otherwise. The value of the condition shall be of integral type,
enumeration type, or class type. If of class type, the condition is
contextually implicitly converted [[conv]] to an integral or enumeration
type. If the (possibly converted) type is subject to integral promotions
[[conv.prom]], the condition is converted to the promoted type. Any
statement within the `switch` statement can be labeled with one or more
case labels as follows:

``` bnf
case constant-expression ':'
```

where the *constant-expression* shall be a converted constant expression
[[expr.const]] of the adjusted type of the switch condition. No two of
the case constants in the same switch shall have the same value after
conversion.

There shall be at most one label of the form

``` cpp
default :
```

within a `switch` statement.

Switch statements can be nested; a `case` or `default` label is
associated with the smallest switch enclosing it.

When the `switch` statement is executed, its condition is evaluated. If
one of the case constants has the same value as the condition, control
is passed to the statement following the matched case label. If no case
constant matches the condition, and if there is a `default` label,
control passes to the statement labeled by the default label. If no case
matches and if there is no `default` then none of the statements in the
switch is executed.

`case` and `default` labels in themselves do not alter the flow of
control, which continues unimpeded across such labels. To exit from a
switch, see `break`, [[stmt.break]].

[*Note 1*: Usually, the substatement that is the subject of a switch is
compound and `case` and `default` labels appear on the top-level
statements contained within the (compound) substatement, but this is not
required. Declarations can appear in the substatement of a `switch`
statement. — *end note*]

A `switch` statement of the form

``` bnf
switch '(' init-statement condition ')' statement
```

is equivalent to

``` bnf
'{'
   init-statement
   switch '(' condition ')' statement
'}'
```

except that the *init-statement* is in the same scope as the
*condition*.

## Iteration statements <a id="stmt.iter">[[stmt.iter]]</a>

### General <a id="stmt.iter.general">[[stmt.iter.general]]</a>

Iteration statements specify looping.

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

See  [[dcl.meaning]] for the optional *attribute-specifier-seq* in a
*for-range-declaration*.

[*Note 1*: An *init-statement* ends with a semicolon. — *end note*]

The substatement in an *iteration-statement* implicitly defines a block
scope [[basic.scope]] which is entered and exited each time through the
loop. If the substatement in an *iteration-statement* is a single
statement and not a *compound-statement*, it is as if it was rewritten
to be a *compound-statement* containing the original statement.

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

### The `while` statement <a id="stmt.while">[[stmt.while]]</a>

In the `while` statement the substatement is executed repeatedly until
the value of the condition [[stmt.pre]] becomes `false`. The test takes
place before each execution of the substatement.

A `while` statement is equivalent to

``` bnf
label ':'
'{'
   if '(' condition ')' '{'
      statement
      goto label ';'
   '}'
'}'
```

[*Note 1*:

The variable created in the condition is destroyed and created with each
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

— *end note*]

### The `do` statement <a id="stmt.do">[[stmt.do]]</a>

The expression is contextually converted to `bool` [[conv]]; if that
conversion is ill-formed, the program is ill-formed.

In the `do` statement the substatement is executed repeatedly until the
value of the expression becomes `false`. The test takes place after each
execution of the statement.

### The `for` statement <a id="stmt.for">[[stmt.for]]</a>

The `for` statement

``` bnf
for '(' init-statement conditionₒₚₜ ';' expressionₒₚₜ ')' statement
```

is equivalent to

``` bnf
'{'
   init-statement
   while '(' condition ')' '{'
     statement
     expression ';'
   '}'
'}'
```

except that the *init-statement* is in the same scope as the
*condition*, and except that a `continue` in *statement* (not enclosed
in another iteration statement) will execute *expression* before
re-evaluating *condition*.

[*Note 1*: Thus the first statement specifies initialization for the
loop; the condition [[stmt.pre]] specifies a test, sequenced before each
iteration, such that the loop is exited when the condition becomes
`false`; the expression often specifies incrementing that is sequenced
after each iteration. — *end note*]

Either or both of the *condition* and the *expression* can be omitted. A
missing *condition* makes the implied `while` clause equivalent to
`while(true)`.

### The range-based `for` statement <a id="stmt.ranged">[[stmt.ranged]]</a>

The range-based `for` statement

``` bnf
for '(' init-statementₒₚₜ for-range-declaration ':' for-range-initializer ')' statement
```

is equivalent to

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

where

- if the *for-range-initializer* is an *expression*, it is regarded as
  if it were surrounded by parentheses (so that a comma operator cannot
  be reinterpreted as delimiting two *init-declarator*s);
- *`range`*, *`begin`*, and *`end`* are variables defined for exposition
  only; and
- *`begin-expr`* and *`end-expr`* are determined as follows:
  - if the *for-range-initializer* is an expression of array type `R`,
    *`begin-expr`* and *`end-expr`* are *`range`* and *`range`* `+` `N`,
    respectively, where `N` is the array bound. If `R` is an array of
    unknown bound or an array of incomplete type, the program is
    ill-formed;
  - if the *for-range-initializer* is an expression of class type `C`,
    and searches in the scope of `C` [[class.member.lookup]] for the
    names `begin` and `end` each find at least one declaration,
    *`begin-expr`* and *`end-expr`* are `range.begin()` and
    `range.end()`, respectively;
  - otherwise, *`begin-expr`* and *`end-expr`* are `begin(range)` and
    `end(range)`, respectively, where `begin` and `end` undergo
    argument-dependent lookup [[basic.lookup.argdep]].
    \[*Note 1*: Ordinary unqualified lookup [[basic.lookup.unqual]] is
    not performed. — *end note*]

[*Example 1*:

``` cpp
int array[5] = { 1, 2, 3, 4, 5 };
for (int& x : array)
  x *= 2;
```

— *end example*]

[*Note 1*: The lifetime of some temporaries in the
*for-range-initializer* is extended to cover the entire loop
[[class.temporary]]. — *end note*]

[*Example 2*:

``` cpp
using T = std::list<int>;
const T& f1(const T& t) { return t; }
const T& f2(T t)        { return t; }
T g();

void foo() {
  for (auto e : f1(g())) {}     // OK, lifetime of return value of g() extended
  for (auto e : f2(g())) {}     // undefined behavior
}
```

— *end example*]

In the *decl-specifier-seq* of a *for-range-declaration*, each
*decl-specifier* shall be either a *type-specifier* or `constexpr`. The
*decl-specifier-seq* shall not define a class or enumeration.

## Jump statements <a id="stmt.jump">[[stmt.jump]]</a>

### General <a id="stmt.jump.general">[[stmt.jump.general]]</a>

Jump statements unconditionally transfer control.

``` bnf
jump-statement:
    break ';'
    continue ';'
    return expr-or-braced-init-listₒₚₜ ';'
    coroutine-return-statement
    goto identifier ';'
```

[*Note 1*: On exit from a scope (however accomplished), objects with
automatic storage duration [[basic.stc.auto]] that have been constructed
in that scope are destroyed in the reverse order of their construction.
For temporaries, see  [[class.temporary]]. However, the program can be
terminated (by calling `std::exit()` or `std::abort()`
[[support.start.term]], for example) without destroying objects with
automatic storage duration. — *end note*]

[*Note 2*: A suspension of a coroutine [[expr.await]] is not considered
to be an exit from a scope. — *end note*]

### The `break` statement <a id="stmt.break">[[stmt.break]]</a>

A `break` statement shall be enclosed by [[stmt.pre]] an
*iteration-statement* [[stmt.iter]] or a `switch` statement
[[stmt.switch]]. The `break` statement causes termination of the
smallest such enclosing statement; control passes to the statement
following the terminated statement, if any.

### The `continue` statement <a id="stmt.cont">[[stmt.cont]]</a>

A `continue` statement shall be enclosed by [[stmt.pre]] an
*iteration-statement* [[stmt.iter]]. The `continue` statement causes
control to pass to the loop-continuation portion of the smallest such
enclosing statement, that is, to the end of the loop. More precisely, in
each of the statements

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
equivalent to `goto` *`contin`*.

### The `return` statement <a id="stmt.return">[[stmt.return]]</a>

A function returns to its caller by the `return` statement.

The *expr-or-braced-init-list* of a `return` statement is called its
operand. A `return` statement with no operand shall be used only in a
function whose return type is cv `void`, a constructor [[class.ctor]],
or a destructor [[class.dtor]]. A `return` statement with an operand of
type `void` shall be used only in a function that has a cv `void` return
type. A `return` statement with any other operand shall be used only in
a function that has a return type other than cv `void`; the `return`
statement initializes the returned reference or prvalue result object of
the (explicit or implicit) function call by copy-initialization
[[dcl.init]] from the operand.

[*Note 1*: A constructor or destructor does not have a return
type. — *end note*]

[*Note 2*: A `return` statement can involve an invocation of a
constructor to perform a copy or move of the operand if it is not a
prvalue or if its type differs from the return type of the function. A
copy operation associated with a `return` statement can be elided or
converted to a move operation if an automatic storage duration variable
is returned [[class.copy.elision]]. — *end note*]

The destructor for the result object is potentially invoked
[[class.dtor]], [[except.ctor]].

[*Example 1*:

``` cpp
class A {
  ~A() {}
};
A f() { return A(); }   // error: destructor of A is private (even though it is never invoked)
```

— *end example*]

Flowing off the end of a constructor, a destructor, or a non-coroutine
function with a cv `void` return type is equivalent to a `return` with
no operand. Otherwise, flowing off the end of a function that is neither
`main` [[basic.start.main]] nor a coroutine [[dcl.fct.def.coroutine]]
results in undefined behavior.

The copy-initialization of the result of the call is sequenced before
the destruction of temporaries at the end of the full-expression
established by the operand of the `return` statement, which, in turn, is
sequenced before the destruction of local variables [[stmt.jump]] of the
block enclosing the `return` statement.

### The `co_return` statement <a id="stmt.return.coroutine">[[stmt.return.coroutine]]</a>

``` bnf
coroutine-return-statement:
    'co_return' expr-or-braced-init-listₒₚₜ ';'
```

A coroutine returns to its caller or resumer [[dcl.fct.def.coroutine]]
by the `co_return` statement or when suspended [[expr.await]]. A
coroutine shall not enclose a `return` statement [[stmt.return]].

[*Note 1*: For this determination, it is irrelevant whether the
`return` statement is enclosed by a discarded statement
[[stmt.if]]. — *end note*]

The *expr-or-braced-init-list* of a `co_return` statement is called its
operand. Let *p* be an lvalue naming the coroutine promise object
[[dcl.fct.def.coroutine]]. A `co_return` statement is equivalent to:

``` bnf
\terminal{\ S\terminal{;} \terminal{goto} final-suspend\terminal{;} \terminal{\}}
```

where *`final-suspend`* is the exposition-only label defined in
[[dcl.fct.def.coroutine]] and *S* is defined as follows:

- If the operand is a *braced-init-list* or an expression of non-`void`
  type, *S* is *p*`.return_value(`*expr-or-braced-init-list*`)`. The
  expression *S* shall be a prvalue of type `void`.
- Otherwise, *S* is the *compound-statement* `{` *expression*ₒₚₜ `;`
  *p*`.return_void()``; }`. The expression *p*`.return_void()` shall be
  a prvalue of type `void`.

If *p*`.return_void()` is a valid expression, flowing off the end of a
coroutine’s *function-body* is equivalent to a `co_return` with no
operand; otherwise flowing off the end of a coroutine’s *function-body*
results in undefined behavior.

### The `goto` statement <a id="stmt.goto">[[stmt.goto]]</a>

The `goto` statement unconditionally transfers control to the statement
labeled by the identifier. The identifier shall be a label
[[stmt.label]] located in the current function.

## Declaration statement <a id="stmt.dcl">[[stmt.dcl]]</a>

A declaration statement introduces one or more new names into a block;
it has the form

``` bnf
declaration-statement:
    block-declaration
```

[*Note 1*: If an identifier introduced by a declaration was previously
declared in an outer block, the outer declaration is hidden for the
remainder of the block [[basic.lookup.unqual]], after which it resumes
its force. — *end note*]

A variable with automatic storage duration [[basic.stc.auto]] is
*active* everywhere in the scope to which it belongs after its
*init-declarator*. Upon each transfer of control (including sequential
execution of statements) within a function from point P to point Q, all
variables with automatic storage duration that are active at P and not
at Q are destroyed in the reverse order of their construction. Then, all
variables with automatic storage duration that are active at Q but not
at P are initialized in declaration order; unless all such variables
have vacuous initialization [[basic.life]], the transfer of control
shall not be a jump.[^2]

When a *declaration-statement* is executed, P and Q are the points
immediately before and after it; when a function returns, Q is after its
body.

[*Example 1*:

``` cpp
void f() {
  // ...
  goto lx;          // error: jump into scope of a
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

Dynamic initialization of a block variable with static storage duration
[[basic.stc.static]] or thread storage duration [[basic.stc.thread]] is
performed the first time control passes through its declaration; such a
variable is considered initialized upon the completion of its
initialization. If the initialization exits by throwing an exception,
the initialization is not complete, so it will be tried again the next
time control enters the declaration. If control enters the declaration
concurrently while the variable is being initialized, the concurrent
execution shall wait for completion of the initialization.

[*Note 2*: A conforming implementation cannot introduce any deadlock
around execution of the initializer. Deadlocks might still be caused by
the program logic; the implementation need only avoid deadlocks due to
its own synchronization operations. — *end note*]

If control re-enters the declaration recursively while the variable is
being initialized, the behavior is undefined.

[*Example 2*:

``` cpp
int foo(int i) {
  static int s = foo(2*i);      // undefined behavior: recursive call
  return i+1;
}
```

— *end example*]

An object associated with a block variable with static or thread storage
duration will be destroyed if and only if it was constructed.

[*Note 3*:  [[basic.start.term]] describes the order in which such
objects are destroyed. — *end note*]

## Ambiguity resolution <a id="stmt.ambig">[[stmt.ambig]]</a>

There is an ambiguity in the grammar involving *expression-statement*s
and *declaration*s: An *expression-statement* with a function-style
explicit type conversion [[expr.type.conv]] as its leftmost
subexpression can be indistinguishable from a *declaration* where the
first *declarator* starts with a `(`. In those cases the *statement* is
a *declaration*.

[*Note 1*:

If the *statement* cannot syntactically be a *declaration*, there is no
ambiguity, so this rule does not apply. In some cases, the whole
*statement* needs to be examined to determine whether this is the case.
This resolves the meaning of many examples.

[*Example 1*:

Assuming `T` is a *simple-type-specifier* [[dcl.type]],

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
ill-formed declaration. If, during parsing, lookup finds that a name in
a template argument is bound to (part of) the declaration being parsed,
the program is ill-formed. No diagnostic is required.

[*Example 3*:

``` cpp
struct T1 {
  T1 operator()(int x) { return T1(x); }
  int operator=(int x) { return x; }
  T1(int) { }
};
struct T2 { T2(int) { } };
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

<!-- Link reference definitions -->
[basic.life]: basic.md#basic.life
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope]: basic.md#basic.scope
[basic.scope.block]: basic.md#basic.scope.block
[basic.start.main]: basic.md#basic.start.main
[basic.start.term]: basic.md#basic.start.term
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[class.copy.elision]: class.md#class.copy.elision
[class.ctor]: class.md#class.ctor
[class.dtor]: class.md#class.dtor
[class.member.lookup]: basic.md#class.member.lookup
[class.temporary]: basic.md#class.temporary
[conv]: expr.md#conv
[conv.prom]: expr.md#conv.prom
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.fct.def.coroutine]: dcl.md#dcl.fct.def.coroutine
[dcl.init]: dcl.md#dcl.init
[dcl.meaning]: dcl.md#dcl.meaning
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.type]: dcl.md#dcl.type
[except.ctor]: except.md#except.ctor
[expr.await]: expr.md#expr.await
[expr.const]: expr.md#expr.const
[expr.context]: expr.md#expr.context
[expr.type.conv]: expr.md#expr.type.conv
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
[stmt.iter.general]: #stmt.iter.general
[stmt.jump]: #stmt.jump
[stmt.jump.general]: #stmt.jump.general
[stmt.label]: #stmt.label
[stmt.pre]: #stmt.pre
[stmt.ranged]: #stmt.ranged
[stmt.return]: #stmt.return
[stmt.return.coroutine]: #stmt.return.coroutine
[stmt.select]: #stmt.select
[stmt.select.general]: #stmt.select.general
[stmt.stmt]: #stmt.stmt
[stmt.switch]: #stmt.switch
[stmt.while]: #stmt.while
[support.start.term]: support.md#support.start.term
[temp.pre]: temp.md#temp.pre
[term.odr.use]: basic.md#term.odr.use

[^1]: In other words, the `else` is associated with the nearest un-elsed
    `if`.

[^2]: The transfer from the condition of a `switch` statement to a
    `case` label is considered a jump in this respect.
