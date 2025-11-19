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
```

The optional *attribute-specifier-seq* appertains to the respective
statement.

## Labeled statement <a id="stmt.label">[[stmt.label]]</a>

A statement can be labeled.

``` bnf
labeled-statement:
    attribute-specifier-seqiₒₚₜdentifier ':' statement
    attribute-specifier-seq\terminal ₒₚₜ{case} constant-expression ':' statement
    attribute-specifier-seq\terminal ₒₚₜ{default :} statement
```

The optional *attribute-specifier-seq* appertains to the label. An
identifier label declares the identifier. The only use of an identifier
label is as the target of a `goto`. The scope of a label is the function
in which it appears. Labels shall not be redeclared within a function. A
label can be used in a `goto` statement before its definition. Labels
have their own name space and do not interfere with other identifiers.

Case labels and default labels shall occur only in switch statements.

## Expression statement <a id="stmt.expr">[[stmt.expr]]</a>

Expression statements have the form

``` bnf
expression-statement:
    expression\terminal ₒₚₜ{;}
```

The expression is a discarded-value expression (Clause  [[expr]]). All
side effects from an expression statement are completed before the next
statement is executed. An expression statement with the expression
missing is called a null statement. Most statements are expression
statements — usually assignments or function calls. A null statement is
useful to carry a label just before the `}` of a compound statement and
to supply a null body to an iteration statement such as a `while`
statement ([[stmt.while]]).

## Compound statement or block <a id="stmt.block">[[stmt.block]]</a>

So that several statements can be used where one is expected, the
compound statement (also, and equivalently, called “block”) is provided.

``` bnf
compound-statement:
    \terminal{\ statement-seq\terminal ₒₚₜ{\}}
```

``` bnf
statement-seq:
    statement
    statement-seq statement
```

A compound statement defines a block scope ([[basic.scope]]). A
declaration is a *statement* ([[stmt.dcl]]).

## Selection statements <a id="stmt.select">[[stmt.select]]</a>

Selection statements choose one of several flows of control.

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

See  [[dcl.meaning]] for the optional *attribute-specifier-seq* in a
condition. In Clause  [[stmt.stmt]], the term *substatement* refers to
the contained *statement* or *statement*s that appear in the syntax
notation. The substatement in a *selection-statement* (each
substatement, in the `else` form of the `if` statement) implicitly
defines a block scope ([[basic.scope]]). If the substatement in a
selection-statement is a single statement and not a
*compound-statement,* it is as if it was rewritten to be a
compound-statement containing the original substatement.

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

The rules for *condition*s apply both to *selection-statement*s and to
the `for` and `while` statements ([[stmt.iter]]). The *declarator*
shall not specify a function or an array. If the `auto` appears in the ,
the type of the identifier being declared is deduced from the
initializer as described in  [[dcl.spec.auto]].

A name introduced by a declaration in a *condition* (either introduced
by the *type-specifier-seq* or the *declarator* of the condition) is in
scope from its point of declaration until the end of the substatements
controlled by the condition. If the name is re-declared in the outermost
block of a substatement controlled by the condition, the declaration
that re-declares the name is ill-formed.

``` cpp
if (int x = f()) {
  int x;            // ill-formed, redeclaration of x
}
else {
  int x;            // ill-formed, redeclaration of x
}
```

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

### The `if` statement <a id="stmt.if">[[stmt.if]]</a>

If the condition ([[stmt.select]]) yields `true` the first substatement
is executed. If the `else` part of the selection statement is present
and the condition yields `false`, the second substatement is executed.
In the second form of `if` statement (the one including `else`), if the
first substatement is also an `if` statement then that inner `if`
statement shall contain an `else` part.[^1]

### The `switch` statement <a id="stmt.switch">[[stmt.switch]]</a>

The `switch` statement causes control to be transferred to one of
several statements depending on the value of a condition.

The condition shall be of integral type, enumeration type, or of a class
type for which a single non-explicit conversion function to integral or
enumeration type exists ([[class.conv]]). If the condition is of class
type, the condition is converted by calling that conversion function,
and the result of the conversion is used in place of the original
condition for the remainder of this section. Integral promotions are
performed. Any statement within the `switch` statement can be labeled
with one or more case labels as follows:

``` bnf
'case' constant-expression ':'
```

where the *constant-expression* shall be a converted constant
expression ([[expr.const]]) of the promoted type of the switch
condition. No two of the case constants in the same switch shall have
the same value after conversion to the promoted type of the switch
condition.

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
switch, see `break`,  [[stmt.break]]. Usually, the substatement that is
the subject of a switch is compound and `case` and `default` labels
appear on the top-level statements contained within the (compound)
substatement, but this is not required. Declarations can appear in the
substatement of a *switch-statement*.

## Iteration statements <a id="stmt.iter">[[stmt.iter]]</a>

Iteration statements specify looping.

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

See  [[dcl.meaning]] for the optional *attribute-specifier-seq* in a
*for-range-declaration*. A *for-init-statement* ends with a semicolon.

The substatement in an *iteration-statement* implicitly defines a block
scope ([[basic.scope]]) which is entered and exited each time through
the loop.

If the substatement in an iteration-statement is a single statement and
not a *compound-statement,* it is as if it was rewritten to be a
compound-statement containing the original statement.

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

The requirements on *condition*s in iteration statements are described
in  [[stmt.select]].

### The `while` statement <a id="stmt.while">[[stmt.while]]</a>

In the `while` statement the substatement is executed repeatedly until
the value of the condition ([[stmt.select]]) becomes `false`. The test
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

### The `do` statement <a id="stmt.do">[[stmt.do]]</a>

The expression is contextually converted to `bool` (Clause  [[conv]]);
if that conversion is ill-formed, the program is ill-formed.

In the `do` statement the substatement is executed repeatedly until the
value of the expression becomes `false`. The test takes place after each
execution of the statement.

### The `for` statement <a id="stmt.for">[[stmt.for]]</a>

The `for` statement

``` bnf
'for (' for-init-statement condition\terminal ₒₚₜ{;} expression\terminal ₒₚₜ{)} statement
```

is equivalent to

except that names declared in the *for-init-statement* are in the same
declarative-region as those declared in the *condition*, and except that
a `continue` in *statement* (not enclosed in another iteration
statement) will execute *expression* before re-evaluating *condition*.
Thus the first statement specifies initialization for the loop; the
condition ([[stmt.select]]) specifies a test, made before each
iteration, such that the loop is exited when the condition becomes
`false`; the expression often specifies incrementing that is done after
each iteration.

Either or both of the condition and the expression can be omitted. A
missing *condition* makes the implied `while` Clause equivalent to
`while(true)`.

If the *for-init-statement* is a declaration, the scope of the name(s)
declared extends to the end of the *for-statement*.

``` cpp
int i = 42;
int a[10];

for (int i = 0; i < 10; i++)
  a[i] = i;

int j = i;          // j = 42
```

### The range-based `for` statement <a id="stmt.ranged">[[stmt.ranged]]</a>

For a range-based `for` statement of the form

``` bnf
'for (' for-range-declaration : expression ')' statement
```

let *range-init* be equivalent to the *expression* surrounded by
parentheses[^2]

``` bnf
'(' expression ')'
```

and for a range-based `for` statement of the form

``` bnf
'for' '(' for-range-declaration ':' braced-init-list ')' statement
```

let *range-init* be equivalent to the *braced-init-list*. In each case,
a range-based `for` statement is equivalent to

``` cpp
{
  auto && __range = range-init;
  for ( auto __begin = begin-expr,
             __end = end-expr;
        __begin != __end;
        ++__begin ) {
    for-range-declaration = *__begin;
    statement
  }
}
```

where `__range`, `__begin`, and `__end` are variables defined for
exposition only, and `_RangeT` is the type of the *expression*, and
*begin-expr* and *end-expr* are determined as follows:

- if `_RangeT` is an array type, *begin-expr* and *end-expr* are
  `__range` and `__range + __bound`, respectively, where `__bound` is
  the array bound. If `_RangeT` is an array of unknown size or an array
  of incomplete type, the program is ill-formed;
- if `_RangeT` is a class type, the *unqualified-id*s `begin` and `end`
  are looked up in the scope of class `\mbox{_RangeT}` as if by class
  member access lookup ([[basic.lookup.classref]]), and if either (or
  both) finds at least one declaration, *begin-expr* and *end-expr* are
  `__range.begin()` and `__range.end()`, respectively;
- otherwise, *begin-expr* and *end-expr* are `begin(__range)` and
  `end(__range)`, respectively, where `begin` and `end` are looked up
  with argument-dependent lookup ([[basic.lookup.argdep]]). For the
  purposes of this name lookup, namespace `std` is an associated
  namespace.

``` cpp
int array[5] = { 1, 2, 3, 4, 5 };
for (int& x : array)
  x *= 2;
```

In the *decl-specifier-seq* of a *for-range-declaration*, each
*decl-specifier* shall be either a *type-specifier* or `constexpr`.

## Jump statements <a id="stmt.jump">[[stmt.jump]]</a>

Jump statements unconditionally transfer control.

``` bnf
jump-statement:
    'break ;'
    'continue ;'
    'return' expression\terminal ₒₚₜ{;}
    'return' braced-init-list ';'
    'goto' identifier ';'
```

On exit from a scope (however accomplished), objects with automatic
storage duration ([[basic.stc.auto]]) that have been constructed in
that scope are destroyed in the reverse order of their construction. For
temporaries, see  [[class.temporary]]. Transfer out of a loop, out of a
block, or back past an initialized variable with automatic storage
duration involves the destruction of objects with automatic storage
duration that are in scope at the point transferred from but not at the
point transferred to. (See  [[stmt.dcl]] for transfers into blocks).
However, the program can be terminated (by calling `std::exit()` or
`std::abort()` ([[support.start.term]]), for example) without
destroying class objects with automatic storage duration.

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

A return statement with neither an *expression* nor a *braced-init-list*
can be used only in functions that do not return a value, that is, a
function with the return type `void`, a constructor ([[class.ctor]]),
or a destructor ([[class.dtor]]). A return statement with an expression
of non-void type can be used only in functions returning a value; the
value of the expression is returned to the caller of the function. The
value of the expression is implicitly converted to the return type of
the function in which it appears. A return statement can involve the
construction and copy or move of a temporary object (
[[class.temporary]]). A copy or move operation associated with a return
statement may be elided or considered as an rvalue for the purpose of
overload resolution in selecting a constructor ([[class.copy]]). A
return statement with a *braced-init-list* initializes the object or
reference to be returned from the function by copy-list-initialization (
[[dcl.init.list]]) from the specified initializer list.

``` cpp
std::pair<std::string,int> f(const char* p, int x) {
  return {p,x};
}
```

Flowing off the end of a function is equivalent to a `return` with no
value; this results in undefined behavior in a value-returning function.

A return statement with an expression of type `void` can be used only in
functions with a return type of *cv* `void`; the expression is evaluated
just before the function returns to its caller.

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

Variables with automatic storage duration ([[basic.stc.auto]]) are
initialized each time their *declaration-statement* is executed.
Variables with automatic storage duration declared in the block are
destroyed on exit from the block ([[stmt.jump]]).

It is possible to transfer into a block, but not in a way that bypasses
declarations with initialization. A program that jumps[^3] from a point
where a variable with automatic storage duration is not in scope to a
point where it is in scope is ill-formed unless the variable has scalar
type, class type with a trivial default constructor and a trivial
destructor, a cv-qualified version of one of these types, or an array of
one of the preceding types and is declared without an *initializer* (
[[dcl.init]]).

``` cpp
void f() {
  // ...
  goto lx;          // ill-formed: jump into scope of a
  // ...
ly:
  X a = 1;
  // ...
lx:
  goto ly;          // OK, jump implies destructor
                    // call for a followed by construction
                    // again immediately following label ly
}
```

The zero-initialization ([[dcl.init]]) of all block-scope variables
with static storage duration ([[basic.stc.static]]) or thread storage
duration ([[basic.stc.thread]]) is performed before any other
initialization takes place. Constant initialization (
[[basic.start.init]]) of a block-scope entity with static storage
duration, if applicable, is performed before its block is first entered.
An implementation is permitted to perform early initialization of other
block-scope variables with static or thread storage duration under the
same conditions that an implementation is permitted to statically
initialize a variable with static or thread storage duration in
namespace scope ([[basic.start.init]]). Otherwise such a variable is
initialized the first time control passes through its declaration; such
a variable is considered initialized upon the completion of its
initialization. If the initialization exits by throwing an exception,
the initialization is not complete, so it will be tried again the next
time control enters the declaration. If control enters the declaration
concurrently while the variable is being initialized, the concurrent
execution shall wait for completion of the initialization.[^4] If
control re-enters the declaration recursively while the variable is
being initialized, the behavior is undefined.

``` cpp
int foo(int i) {
  static int s = foo(2*i);      // recursive call - undefined
  return i+1;
}
```

The destructor for a block-scope object with static or thread storage
duration will be executed if and only if it was constructed.
[[basic.start.term]] describes the order in which block-scope objects
with static and thread storage duration are destroyed.

## Ambiguity resolution <a id="stmt.ambig">[[stmt.ambig]]</a>

There is an ambiguity in the grammar involving *expression-statement*s
and *declaration*s: An *expression-statement* with a function-style
explicit type conversion ([[expr.type.conv]]) as its leftmost
subexpression can be indistinguishable from a *declaration* where the
first *declarator* starts with a `(`. In those cases the *statement* is
a *declaration*. To disambiguate, the whole *statement* might have to be
examined to determine if it is an *expression-statement* or a
*declaration*. This disambiguates many examples. assuming `T` is a
*simple-type-specifier* ([[dcl.type]]),

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

The remaining cases are *declaration*s.

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

The disambiguation is purely syntactic; that is, the meaning of the
names occurring in such a statement, beyond whether they are
*type-name*s or not, is not generally used in or changed by the
disambiguation. Class templates are instantiated as necessary to
determine if a qualified name is a *type-name*. Disambiguation precedes
parsing, and a statement disambiguated as a declaration may be an
ill-formed declaration. If, during parsing, a name in a template
parameter is bound differently than it would be bound during a trial
parse, the program is ill-formed. No diagnostic is required. This can
occur only when the name is declared earlier in the declaration.

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
  T2(4),                        // T2 will be declared as
  (*(*b)(T2(c)))(int(d));       // a variable of type T1
                                // but this will not allow
                                // the last part of the
                                // declaration to parse
                                // properly since it depends
                                // on T2 being a type-name
}
```

<!-- Link reference definitions -->
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.classref]: basic.md#basic.lookup.classref
[basic.scope]: basic.md#basic.scope
[basic.scope.pdecl]: basic.md#basic.scope.pdecl
[basic.start.init]: basic.md#basic.start.init
[basic.start.term]: basic.md#basic.start.term
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[class.conv]: special.md#class.conv
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.dtor]: special.md#class.dtor
[class.temporary]: special.md#class.temporary
[conv]: conv.md#conv
[dcl.init]: dcl.md#dcl.init
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.meaning]: dcl.md#dcl.meaning
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.type]: dcl.md#dcl.type
[expr]: expr.md#expr
[expr.const]: expr.md#expr.const
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
[stmt.jump]: #stmt.jump
[stmt.label]: #stmt.label
[stmt.ranged]: #stmt.ranged
[stmt.return]: #stmt.return
[stmt.select]: #stmt.select
[stmt.stmt]: #stmt.stmt
[stmt.switch]: #stmt.switch
[stmt.while]: #stmt.while
[support.start.term]: language.md#support.start.term

[^1]: In other words, the `else` is associated with the nearest un-elsed
    `if`.

[^2]: this ensures that a top-level comma operator cannot be
    reinterpreted as a delimiter between *init-declarator*s in the
    declaration of `__range`.

[^3]: The transfer from the condition of a `switch` statement to a
    `case` label is considered a jump in this respect.

[^4]: The implementation must not introduce any deadlock around
    execution of the initializer.
