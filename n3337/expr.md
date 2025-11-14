# Expressions <a id="expr">[[expr]]</a>

Clause  [[expr]] defines the syntax, order of evaluation, and meaning of
expressions.[^1] An expression is a sequence of operators and operands
that specifies a computation. An expression can result in a value and
can cause side effects.

Operators can be overloaded, that is, given meaning when applied to
expressions of class type (Clause [[class]]) or enumeration type (
[[dcl.enum]]). Uses of overloaded operators are transformed into
function calls as described in  [[over.oper]]. Overloaded operators obey
the rules for syntax specified in Clause  [[expr]], but the requirements
of operand type, value category, and evaluation order are replaced by
the rules for function call. Relations between operators, such as `++a`
meaning `a+=1`, are not guaranteed for overloaded operators (
[[over.oper]]), and are not guaranteed for operands of type `bool`.

Clause  [[expr]] defines the effects of operators when applied to types
for which they have not been overloaded. Operator overloading shall not
modify the rules for the *built-in operators*, that is, for operators
applied to types for which they are defined by this Standard. However,
these built-in operators participate in overload resolution, and as part
of that process user-defined conversions will be considered where
necessary to convert the operands to types appropriate for the built-in
operator. If a built-in operator is selected, such conversions will be
applied to the operands before the operation is considered further
according to the rules in Clause  [[expr]]; see  [[over.match.oper]], 
[[over.built]].

If during the evaluation of an expression, the result is not
mathematically defined or not in the range of representable values for
its type, the behavior is undefined. most existing implementations of
C++ignore integer overflows. Treatment of division by zero, forming a
remainder using a zero divisor, and all floating point exceptions vary
among machines, and is usually adjustable by a library function.

If an expression initially has the type “reference to `T`” (
[[dcl.ref]],  [[dcl.init.ref]]), the type is adjusted to `T` prior to
any further analysis. The expression designates the object or function
denoted by the reference, and the expression is an lvalue or an xvalue,
depending on the expression.

An expression is an xvalue if it is:

- the result of calling a function, whether implicitly or explicitly,
  whose return type is an rvalue reference to object type,
- a cast to an rvalue reference to object type,
- a class member access expression designating a non-static data member
  of non-reference type in which the object expression is an xvalue, or
- a `.*` pointer-to-member expression in which the first operand is an
  xvalue and the second operand is a pointer to data member.

In general, the effect of this rule is that named rvalue references are
treated as lvalues and unnamed rvalue references to objects are treated
as xvalues; rvalue references to functions are treated as lvalues
whether named or not.

``` cpp
struct A {
  int m;
};
A&& operator+(A, A);
A&& f();

A a;
A&& ar = static_cast<A&&>(a);
```

The expressions `f()`, `f().m`, `static_cast<A&&>(a)`, and `a + a` are
xvalues. The expression `ar` is an lvalue.

In some contexts, *unevaluated operands* appear ([[expr.typeid]],
[[expr.sizeof]], [[expr.unary.noexcept]], [[dcl.type.simple]]). An
unevaluated operand is not evaluated. In an unevaluated operand, a
non-static class member may be named ([[expr.prim]]) and naming of
objects or functions does not, by itself, require that a definition be
provided ([[basic.def.odr]]).

Whenever a glvalue expression appears as an operand of an operator that
expects a prvalue for that operand, the lvalue-to-rvalue (
[[conv.lval]]), array-to-pointer ([[conv.array]]), or
function-to-pointer ([[conv.func]]) standard conversions are applied to
convert the expression to a prvalue. because cv-qualifiers are removed
from the type of an expression of non-class type when the expression is
converted to a prvalue, an lvalue expression of type `const int` can,
for example, be used where a prvalue expression of type `int` is
required.

Many binary operators that expect operands of arithmetic or enumeration
type cause conversions and yield result types in a similar way. The
purpose is to yield a common type, which is also the type of the result.
This pattern is called the *usual arithmetic conversions*, which are
defined as follows:

- If either operand is of scoped enumeration type ([[dcl.enum]]), no
  conversions are performed; if the other operand does not have the same
  type, the expression is ill-formed.
- If either operand is of type `long` `double`, the other shall be
  converted to `long` `double`.
- Otherwise, if either operand is `double`, the other shall be converted
  to `double`.
- Otherwise, if either operand is `float`, the other shall be converted
  to `float`.
- Otherwise, the integral promotions ([[conv.prom]]) shall be performed
  on both operands.[^2] Then the following rules shall be applied to the
  promoted operands:
  - If both operands have the same type, no further conversion is
    needed.
  - Otherwise, if both operands have signed integer types or both have
    unsigned integer types, the operand with the type of lesser integer
    conversion rank shall be converted to the type of the operand with
    greater rank.
  - Otherwise, if the operand that has unsigned integer type has rank
    greater than or equal to the rank of the type of the other operand,
    the operand with signed integer type shall be converted to the type
    of the operand with unsigned integer type.
  - Otherwise, if the type of the operand with signed integer type can
    represent all of the values of the type of the operand with unsigned
    integer type, the operand with unsigned integer type shall be
    converted to the type of the operand with signed integer type.
  - Otherwise, both operands shall be converted to the unsigned integer
    type corresponding to the type of the operand with signed integer
    type.

In some contexts, an expression only appears for its side effects. Such
an expression is called a *discarded-value expression*. The expression
is evaluated and its value is discarded. The array-to-pointer (
[[conv.array]]) and function-to-pointer ([[conv.func]]) standard
conversions are not applied. The lvalue-to-rvalue conversion (
[[conv.lval]]) is applied only if the expression is an lvalue of
volatile-qualified type and it has one of the following forms:

- *id-expression* ([[expr.prim.general]]),
- subscripting ([[expr.sub]]),
- class member access ([[expr.ref]]),
- indirection ([[expr.unary.op]]),
- pointer-to-member operation ([[expr.mptr.oper]]),
- conditional expression ([[expr.cond]]) where both the second and the
  third operands are one of the above, or
- comma expression ([[expr.comma]]) where the right operand is one of
  the above.

The values of the floating operands and the results of floating
expressions may be represented in greater precision and range than that
required by the type; the types are not changed thereby.[^3]

## Primary expressions <a id="expr.prim">[[expr.prim]]</a>

### General <a id="expr.prim.general">[[expr.prim.general]]</a>

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

A *literal* is a primary expression. Its type depends on its form (
[[lex.literal]]). A string literal is an lvalue; all other literals are
prvalues.

The keyword `this` names a pointer to the object for which a non-static
member function ([[class.this]]) is invoked or a non-static data
member’s initializer ([[class.mem]]) is evaluated.

If a declaration declares a member function or member function template
of a class `X`, the expression `this` is a prvalue of type “pointer to
*cv-qualifier-seq* `X`” between the optional *cv-qualifer-seq* and the
end of the *function-definition*, *member-declarator*, or *declarator*.
It shall not appear before the optional *cv-qualifier-seq* and it shall
not appear within the declaration of a static member function (although
its type and value category are defined within a static member function
as they are within a non-static member function). this is because
declaration matching does not occur until the complete declarator is
known. Unlike the object expression in other contexts, `*this` is not
required to be of complete type for purposes of class member access (
[[expr.ref]]) outside the member function body. only class members
declared prior to the declaration are visible.

``` cpp
struct A {
  char g();
  template<class T> auto f(T t) -> decltype(t + g())
    { return t + g(); }
};
template auto A::f(int t) -> decltype(t + g());
```

Otherwise, if a *member-declarator* declares a non-static data member (
[[class.mem]]) of a class `X`, the expression `this` is a prvalue of
type “pointer to `X`” within the optional *brace-or-equal-initializer*.
It shall not appear elsewhere in the *member-declarator*.

The expression `this` shall not appear in any other context.

``` cpp
class Outer {
  int a[sizeof(*this)];               // error: not inside a member function
  unsigned int sz = sizeof(*this);    // OK: in brace-or-equal-initializer

  void f() {
    int b[sizeof(*this)];             // OK

    struct Inner {
      int c[sizeof(*this)];           // error: not inside a member function of Inner
    };
  }
};
```

A parenthesized expression is a primary expression whose type and value
are identical to those of the enclosed expression. The presence of
parentheses does not affect whether the expression is an lvalue. The
parenthesized expression can be used in exactly the same contexts as
those where the enclosed expression can be used, and with the same
meaning, except as otherwise indicated.

An *id-expression* is a restricted form of a *primary-expression*. an
*id-expression* can appear after `.` and `->` operators ([[expr.ref]]).

An *identifier* is an *id-expression* provided it has been suitably
declared (Clause  [[dcl.dcl]]). for *operator-function-id*s, see 
[[over.oper]]; for *conversion-function-id*s, see  [[class.conv.fct]];
for *literal-operator-id*s, see  [[over.literal]]; for *template-id*s,
see  [[temp.names]]. A *class-name* or *decltype-specifier* prefixed by
`~` denotes a destructor; see  [[class.dtor]]. Within the definition of
a non-static member function, an *identifier* that names a non-static
member is transformed to a class member access expression (
[[class.mfct.non-static]]). The type of the expression is the type of
the *identifier*. The result is the entity denoted by the identifier.
The result is an lvalue if the entity is a function, variable, or data
member and a prvalue otherwise.

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

A *nested-name-specifier* that denotes a class, optionally followed by
the keyword `template` ([[temp.names]]), and then followed by the name
of a member of either that class ([[class.mem]]) or one of its base
classes (Clause  [[class.derived]]), is a *qualified-id*; 
[[class.qual]] describes name lookup for class members that appear in
*qualified-ids*. The result is the member. The type of the result is the
type of the member. The result is an lvalue if the member is a static
member function or a data member and a prvalue otherwise. a class member
can be referred to using a *qualified-id* at any point in its potential
scope ([[basic.scope.class]]). Where *class-name* `::` *class-name* is
used, and the two *class-name*s refer to the same class, this notation
names the constructor ([[class.ctor]]). Where *class-name* `::~`
*class-name* is used, the two *class-name*s shall refer to the same
class; this notation names the destructor ([[class.dtor]]). The form
*\textasciitilde* *decltype-specifier* also denotes the destructor, but
it shall not be used as the *unqualified-id* in a *qualified-id*. a
*typedef-name* that names a class is a *class-name* ([[class.name]]).

A `::`, or a *nested-name-specifier* that names a namespace (
[[basic.namespace]]), in either case followed by the name of a member of
that namespace (or the name of a member of a namespace made visible by a
*using-directive*) is a *qualified-id*;  [[namespace.qual]] describes
name lookup for namespace members that appear in *qualified-ids*. The
result is the member. The type of the result is the type of the member.
The result is an lvalue if the member is a function or a variable and a
prvalue otherwise.

A *nested-name-specifier* that denotes an enumeration ([[dcl.enum]]),
followed by the name of an enumerator of that enumeration, is a
*qualified-id* that refers to the enumerator. The result is the
enumerator. The type of the result is the type of the enumeration. The
result is a prvalue.

In a *qualified-id*, if the *unqualified-id* is a
*conversion-function-id*, its *conversion-type-id* shall denote the same
type in both the context in which the entire *qualified-id* occurs and
in the context of the class denoted by the *nested-name-specifier*.

An *id-expression* that denotes a non-static data member or non-static
member function of a class can only be used:

- as part of a class member access ([[expr.ref]]) in which the object
  expression refers to the member’s class[^4] or a class derived from
  that class, or
- to form a pointer to member ([[expr.unary.op]]), or
- in a *mem-initializer* for a constructor for that class or for a class
  derived from that class ([[class.base.init]]), or
- in a *brace-or-equal-initializer* for a non-static data member of that
  class or of a class derived from that class ([[class.base.init]]), or
- if that *id-expression* denotes a non-static data member and it
  appears in an unevaluated operand.
  ``` cpp
  struct S {
    int m;
  };
  int i = sizeof(S::m);           // OK
  int j = sizeof(S::m + 42);      // OK
  ```

### Lambda expressions <a id="expr.prim.lambda">[[expr.prim.lambda]]</a>

Lambda expressions provide a concise way to create simple function
objects.

``` cpp
#include <algorithm>
#include <cmath>
void abssort(float *x, unsigned N) {
  std::sort(x, x + N,
    [](float a, float b) {
      return std::abs(a) < std::abs(b);
    });
}
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

The evaluation of a *lambda-expression* results in a prvalue temporary (
[[class.temporary]]). This temporary is called the *closure object*. A
*lambda-expression* shall not appear in an unevaluated operand (Clause 
[[expr]]). A closure object behaves like a function object (
[[function.objects]]).

The type of the *lambda-expression* (which is also the type of the
closure object) is a unique, unnamed non-union class type — called the
*closure type* — whose properties are described below. This class type
is not an aggregate ([[dcl.init.aggr]]). The closure type is declared
in the smallest block scope, class scope, or namespace scope that
contains the corresponding *lambda-expression*. This determines the set
of namespaces and classes associated with the closure type (
[[basic.lookup.argdep]]). The parameter types of a *lambda-declarator*
do not affect these associated namespaces and classes. An implementation
may define the closure type differently from what is described below
provided this does not alter the observable behavior of the program
other than by changing:

- the size and/or alignment of the closure type,
- whether the closure type is trivially copyable (Clause  [[class]]),
- whether the closure type is a standard-layout class (Clause 
  [[class]]), or
- whether the closure type is a POD class (Clause  [[class]]).

An implementation shall not add members of rvalue reference type to the
closure type.

If a *lambda-expression* does not include a *lambda-declarator*, it is
as if the *lambda-declarator* were `()`. If a *lambda-expression* does
not include a *trailing-return-type*, it is as if the
*trailing-return-type* denotes the following type:

- if the *compound-statement* is of the form\begin{ncbnf}
  \terminal{\\attribute-specifier-seq\terminal ₒₚₜ{return} expression \terminal{;} \terminal{\\}
  \end{ncbnf} the type of the returned expression after lvalue-to-rvalue
  conversion ([[conv.lval]]), array-to-pointer conversion (
  [[conv.array]]), and function-to-pointer conversion ([[conv.func]]);
- otherwise, `void`.

``` cpp
auto x1 = [](int i){ return i; }; // OK: return type is int
auto x2 = []{ return { 1, 2 }; }; // error: the return type is void (a
                                  // braced-init-list is not an expression)
```

The closure type for a *lambda-expression* has a public `inline`
function call operator ([[over.call]]) whose parameters and return type
are described by the *lambda-expression*’s
*parameter-declaration-clause* and *trailing-return-type* respectively.
This function call operator is declared `const` (
[[class.mfct.non-static]]) if and only if the *lambda-expression*’s
*parameter-declaration-clause* is not followed by `mutable`. It is
neither virtual nor declared `volatile`. Default arguments (
[[dcl.fct.default]]) shall not be specified in the
*parameter-declaration-clause* of a *lambda-declarator*. Any
*exception-specification* specified on a *lambda-expression* applies to
the corresponding function call operator. An *attribute-specifier-seq*
in a *lambda-declarator* appertains to the type of the corresponding
function call operator. Names referenced in the *lambda-declarator* are
looked up in the context in which the *lambda-expression* appears.

The closure type for a *lambda-expression* with no *lambda-capture* has
a public non-virtual non-explicit const conversion function to pointer
to function having the same parameter and return types as the closure
type’s function call operator. The value returned by this conversion
function shall be the address of a function that, when invoked, has the
same effect as invoking the closure type’s function call operator.

The *lambda-expression*’s *compound-statement* yields the
*function-body* ([[dcl.fct.def]]) of the function call operator, but
for purposes of name lookup ([[basic.lookup]]), determining the type
and value of `this` ([[class.this]]) and transforming *id-expression*s
referring to non-static class members into class member access
expressions using `(*this)` ([[class.mfct.non-static]]), the
*compound-statement* is considered in the context of the
*lambda-expression*.

``` cpp
struct S1 {
  int x, y;
  int operator()(int);
  void f() {
    [=]()->int {
      return operator()(this->x + y); // equivalent to S1::operator()(this->x + (*this).y)
                                      // this has type S1*
    };
  }
};
```

If a *lambda-capture* includes a *capture-default* that is `&`, the
identifiers in the *lambda-capture* shall not be preceded by `&`. If a
*lambda-capture* includes a *capture-default* that is `=`, the
*lambda-capture* shall not contain `this` and each identifier it
contains shall be preceded by `&`. An identifier or `this` shall not
appear more than once in a *lambda-capture*.

``` cpp
struct S2 { void f(int i); };
void S2::f(int i) {
  [&, i]{ };    // OK
  [&, &i]{ };   // error: i preceded by & when & is the default
  [=, this]{ }; // error: this when = is the default
  [i, i]{ };    // error: i repeated
}
```

A *lambda-expression* whose smallest enclosing scope is a block scope (
[[basic.scope.local]]) is a *local lambda expression*; any other
*lambda-expression* shall not have a *capture-list* in its
*lambda-introducer*. The *reaching scope* of a local lambda expression
is the set of enclosing scopes up to and including the innermost
enclosing function and its parameters. This reaching scope includes any
intervening *lambda-expression*s.

The *identifiers* in a *capture-list* are looked up using the usual
rules for unqualified name lookup ([[basic.lookup.unqual]]); each such
lookup shall find a variable with automatic storage duration declared in
the reaching scope of the local lambda expression. An entity (i.e. a
variable or `this`) is said to be *explicitly captured* if it appears in
the *lambda-expression*’s *capture-list*.

If a *lambda-expression* has an associated *capture-default* and its
*compound-statement* odr-uses ([[basic.def.odr]]) `this` or a variable
with automatic storage duration and the odr-used entity is not
explicitly captured, then the odr-used entity is said to be *implicitly
captured*; such entities shall be declared within the reaching scope of
the lambda expression. The implicit capture of an entity by a nested
*lambda-expression* can cause its implicit capture by the containing
*lambda-expression* (see below). Implicit odr-uses of `this` can result
in implicit capture.

An entity is *captured* if it is captured explicitly or implicitly. An
entity captured by a *lambda-expression* is odr-used (
[[basic.def.odr]]) in the scope containing the *lambda-expression*. If
`this` is captured by a local lambda expression, its nearest enclosing
function shall be a non-static member function. If a *lambda-expression*
odr-uses ([[basic.def.odr]]) `this` or a variable with automatic
storage duration from its reaching scope, that entity shall be captured
by the *lambda-expression*. If a *lambda-expression* captures an entity
and that entity is not defined or captured in the immediately enclosing
lambda expression or function, the program is ill-formed.

``` cpp
void f1(int i) {
  int const N = 20;
  auto m1 = [=]{
    int const M = 30;
    auto m2 = [i]{
      int x[N][M];              // OK: N and M are not odr-used
      x[0][0] = i;              // OK: i is explicitly captured by m2
                                // and implicitly captured by m1
    };
  };
  struct s1 {
    int f;
    void work(int n) {
      int m = n*n;
      int j = 40;
      auto m3 = [this,m] {
        auto m4 = [&,j] {       // error: j not captured by m3
          int x = n;            // error: n implicitly captured by m4
                                // but not captured by m3
          x += m;               // OK: m implicitly captured by m4
                                // and explicitly captured by m3
          x += i;               // error: i is outside of the reaching scope
          x += f;               // OK: this captured implicitly by m4
                                // and explicitly by m3
        };
      };
    }
  };
}
```

A *lambda-expression* appearing in a default argument shall not
implicitly or explicitly capture any entity.

``` cpp
void f2() {
  int i = 1;
  void g1(int = ([i]{ return i; })());        // ill-formed
  void g2(int = ([i]{ return 0; })());        // ill-formed
  void g3(int = ([=]{ return i; })());        // ill-formed
  void g4(int = ([=]{ return 0; })());        // OK
  void g5(int = ([]{ return sizeof i; })());  // OK
}
```

An entity is *captured by copy* if it is implicitly captured and the
*capture-default* is `=` or if it is explicitly captured with a capture
that does not include an `&`. For each entity captured by copy, an
unnamed non-static data member is declared in the closure type. The
declaration order of these members is unspecified. The type of such a
data member is the type of the corresponding captured entity if the
entity is not a reference to an object, or the referenced type
otherwise. If the captured entity is a reference to a function, the
corresponding data member is also a reference to a function.

An entity is *captured by reference* if it is implicitly or explicitly
captured but not captured by copy. It is unspecified whether additional
unnamed non-static data members are declared in the closure type for
entities captured by reference.

If a *lambda-expression* `m2` captures an entity and that entity is
captured by an immediately enclosing *lambda-expression* `m1`, then
`m2`’s capture is transformed as follows:

- if `m1` captures the entity by copy, `m2` captures the corresponding
  non-static data member of `m1`’s closure type;
- if `m1` captures the entity by reference, `m2` captures the same
  entity captured by `m1`.

the nested lambda expressions and invocations below will output
`123234`.

``` cpp
int a = 1, b = 1, c = 1;
auto m1 = [a, &b, &c]() mutable {
  auto m2 = [a, b, &c]() mutable {
    std::cout << a << b << c;
    a = 4; b = 4; c = 4;
  };
  a = 3; b = 3; c = 3;
  m2();
};
a = 2; b = 2; c = 2;
m1();
std::cout << a << b << c;
```

Every *id-expression* that is an odr-use ([[basic.def.odr]]) of an
entity captured by copy is transformed into an access to the
corresponding unnamed data member of the closure type. An
*id-expression* that is not an odr-use refers to the original entity,
never to a member of the closure type. Furthermore, such an
*id-expression* does not cause the implicit capture of the entity. If
`this` is captured, each odr-use of `this` is transformed into an access
to the corresponding unnamed data member of the closure type, cast (
[[expr.cast]]) to the type of `this`. The cast ensures that the
transformed expression is a prvalue.

``` cpp
void f(const int*);
void g() {
  const int N = 10;
  [=] {
    int arr[N];             // OK: not an odr-use, refers to automatic variable
    f(&N);                  // OK: causes N to be captured; &N points to the
                            // corresponding member of the closure type
  }
}
```

Every occurrence of `decltype((x))` where `x` is a possibly
parenthesized *id-expression* that names an entity of automatic storage
duration is treated as if `x` were transformed into an access to a
corresponding data member of the closure type that would have been
declared if `x` were an odr-use of the denoted entity.

``` cpp
void f3() {
  float x, &r = x;
  [=] {                     // x and r are not captured (appearance in a decltype operand is not an odr-use)
    decltype(x) y1;         // y1 has type float
    decltype((x)) y2 = y1;  // y2 has type float const& because this lambda
                            // is not mutable and x is an lvalue
    decltype(r) r1 = y1;    // r1 has type float& (transformation not considered)
    decltype((r)) r2 = y2;  // r2 has type float const&
  };
}
```

The closure type associated with a *lambda-expression* has a deleted (
[[dcl.fct.def.delete]]) default constructor and a deleted copy
assignment operator. It has an implicitly-declared copy constructor (
[[class.copy]]) and may have an implicitly-declared move constructor (
[[class.copy]]). The copy/move constructor is implicitly defined in the
same way as any other implicitly declared copy/move constructor would be
implicitly defined.

The closure type associated with a *lambda-expression* has an
implicitly-declared destructor ([[class.dtor]]).

When the *lambda-expression* is evaluated, the entities that are
captured by copy are used to direct-initialize each corresponding
non-static data member of the resulting closure object. (For array
members, the array elements are direct-initialized in increasing
subscript order.) These initializations are performed in the
(unspecified) order in which the non-static data members are declared.
This ensures that the destructions will occur in the reverse order of
the constructions.

If an entity is implicitly or explicitly captured by reference, invoking
the function call operator of the corresponding *lambda-expression*
after the lifetime of the entity has ended is likely to result in
undefined behavior.

A *capture* followed by an ellipsis is a pack expansion (
[[temp.variadic]]).

``` cpp
template<class... Args>
void f(Args... args) {
  auto lm = [&, args...] { return g(args...); };
  lm();
}
```

## Postfix expressions <a id="expr.post">[[expr.post]]</a>

Postfix expressions group left-to-right.

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

The `>` token following the in a `dynamic_cast`, `static_cast`,
`reinterpret_cast`, or `const_cast` may be the product of replacing a
`>{>}` token by two consecutive `>` tokens ([[temp.names]]).

### Subscripting <a id="expr.sub">[[expr.sub]]</a>

A postfix expression followed by an expression in square brackets is a
postfix expression. One of the expressions shall have the type “pointer
to `T`” and the other shall have unscoped enumeration or integral type.
The result is an lvalue of type “`T`.” The type “`T`” shall be a
completely-defined object type.[^5] The expression `E1[E2]` is identical
(by definition) to `*((E1)+(E2))` see  [[expr.unary]] and  [[expr.add]]
for details of `*` and `+` and  [[dcl.array]] for details of arrays.

A *braced-init-list* shall not be used with the built-in subscript
operator.

### Function call <a id="expr.call">[[expr.call]]</a>

There are two kinds of function call: ordinary function call and member
function[^6] ([[class.mfct]]) call. A function call is a postfix
expression followed by parentheses containing a possibly empty,
comma-separated list of expressions which constitute the arguments to
the function. For an ordinary function call, the postfix expression
shall be either an lvalue that refers to a function (in which case the
function-to-pointer standard conversion ([[conv.func]]) is suppressed
on the postfix expression), or it shall have pointer to function type.
Calling a function through an expression whose function type has a
language linkage that is different from the language linkage of the
function type of the called function’s definition is undefined (
[[dcl.link]]). For a member function call, the postfix expression shall
be an implicit ([[class.mfct.non-static]],  [[class.static]]) or
explicit class member access ([[expr.ref]]) whose *id-expression* is a
function member name, or a pointer-to-member expression (
[[expr.mptr.oper]]) selecting a function member; the call is as a member
of the class object referred to by the object expression. In the case of
an implicit class member access, the implied object is the one pointed
to by `this`. a member function call of the form `f()` is interpreted as
`(*this).f()` (see  [[class.mfct.non-static]]). If a function or member
function name is used, the name can be overloaded (Clause  [[over]]), in
which case the appropriate function shall be selected according to the
rules in  [[over.match]]. If the selected function is non-virtual, or if
the *id-expression* in the class member access expression is a
*qualified-id*, that function is called. Otherwise, its final
overrider ([[class.virtual]]) in the dynamic type of the object
expression is called. the dynamic type is the type of the object
referred to by the current value of the object expression.
[[class.cdtor]] describes the behavior of virtual function calls when
the object expression refers to an object under construction or
destruction.

If a function or member function name is used, and name lookup (
[[basic.lookup]]) does not find a declaration of that name, the program
is ill-formed. No function is implicitly declared by such a call.

If the *postfix-expression* designates a destructor ([[class.dtor]]),
the type of the function call expression is `void`; otherwise, the type
of the function call expression is the return type of the statically
chosen function (i.e., ignoring the `virtual` keyword), even if the type
of the function actually called is different. This type shall be an
object type, a reference type or the type `void`.

When a function is called, each parameter ([[dcl.fct]]) shall be
initialized ([[dcl.init]],  [[class.copy]],  [[class.ctor]]) with its
corresponding argument. Such initializations are indeterminately
sequenced with respect to each other ([[intro.execution]]) If the
function is a non-static member function, the `this` parameter of the
function ([[class.this]]) shall be initialized with a pointer to the
object of the call, converted as if by an explicit type conversion (
[[expr.cast]]). There is no access or ambiguity checking on this
conversion; the access checking and disambiguation are done as part of
the (possibly implicit) class member access operator. See 
[[class.member.lookup]],  [[class.access.base]], and  [[expr.ref]]. When
a function is called, the parameters that have object type shall have
completely-defined object type. this still allows a parameter to be a
pointer or reference to an incomplete class type. However, it prevents a
passed-by-value parameter to have an incomplete class type. During the
initialization of a parameter, an implementation may avoid the
construction of extra temporaries by combining the conversions on the
associated argument and/or the construction of temporaries with the
initialization of the parameter (see  [[class.temporary]]). The lifetime
of a parameter ends when the function in which it is defined returns.
The initialization and destruction of each parameter occurs within the
context of the calling function. the access of the constructor,
conversion functions or destructor is checked at the point of call in
the calling function. If a constructor or destructor for a function
parameter throws an exception, the search for a handler starts in the
scope of the calling function; in particular, if the function called has
a *function-try-block* (Clause  [[except]]) with a handler that could
handle the exception, this handler is not considered. The value of a
function call is the value returned by the called function except in a
virtual function call if the return type of the final overrider is
different from the return type of the statically chosen function, the
value returned from the final overrider is converted to the return type
of the statically chosen function.

a function can change the values of its non-const parameters, but these
changes cannot affect the values of the arguments except where a
parameter is of a reference type ([[dcl.ref]]); if the reference is to
a const-qualified type, `const_cast` is required to be used to cast away
the constness in order to modify the argument’s value. Where a parameter
is of `const` reference type a temporary object is introduced if
needed ([[dcl.type]],  [[lex.literal]],  [[lex.string]], 
[[dcl.array]],  [[class.temporary]]). In addition, it is possible to
modify the values of nonconstant objects through pointer parameters.

A function can be declared to accept fewer arguments (by declaring
default arguments ([[dcl.fct.default]])) or more arguments (by using
the ellipsis, `...`, or a function parameter pack ([[dcl.fct]])) than
the number of parameters in the function definition ([[dcl.fct.def]]).
this implies that, except where the ellipsis (`...`) or a function
parameter pack is used, a parameter is available for each argument.

When there is no parameter for a given argument, the argument is passed
in such a way that the receiving function can obtain the value of the
argument by invoking `va_arg` ([[support.runtime]]). This paragraph
does not apply to arguments passed to a function parameter pack.
Function parameter packs are expanded during template instantiation (
[[temp.variadic]]), thus each such argument has a corresponding
parameter when a function template specialization is actually called.
The lvalue-to-rvalue ([[conv.lval]]), array-to-pointer (
[[conv.array]]), and function-to-pointer ([[conv.func]]) standard
conversions are performed on the argument expression. An argument that
has (possibly cv-qualified) type `std::nullptr_t` is converted to type
`void*` ([[conv.ptr]]). After these conversions, if the argument does
not have arithmetic, enumeration, pointer, pointer to member, or class
type, the program is ill-formed. Passing a potentially-evaluated
argument of class type (Clause  [[class]]) having a non-trivial copy
constructor, a non-trivial move constructor, or a non-trivial
destructor, with no corresponding parameter, is conditionally-supported
with *implementation-defined* semantics. If the argument has integral or
enumeration type that is subject to the integral promotions (
[[conv.prom]]), or a floating point type that is subject to the floating
point promotion ([[conv.fpprom]]), the value of the argument is
converted to the promoted type before the call. These promotions are
referred to as the *default argument promotions*.

The evaluations of the postfix expression and of the argument
expressions are all unsequenced relative to one another. All side
effects of argument expression evaluations are sequenced before the
function is entered (see  [[intro.execution]]).

Recursive calls are permitted, except to the function named `main` (
[[basic.start.main]]).

A function call is an lvalue if the result type is an lvalue reference
type or an rvalue reference to function type, an xvalue if the result
type is an rvalue reference to object type, and a prvalue otherwise.

If a function call is a prvalue of object type:

- if the function call is either
  - the operand of a *decltype-specifier* or
  - the right operand of a comma operator that is the operand of a
    *decltype-specifier*,

  a temporary object is not introduced for the prvalue. The type of the
  prvalue may be incomplete. as a result, storage is not allocated for
  the prvalue and it is not destroyed; thus, a class type is not
  instantiated as a result of being the type of a function call in this
  context. This is true regardless of whether the expression uses
  function call notation or operator notation ([[over.match.oper]]).
  unlike the rule for a *decltype-specifier* that considers whether an
  *id-expression* is parenthesized ([[dcl.type.simple]]), parentheses
  have no special meaning in this context.
- otherwise, the type of the prvalue shall be complete.

### Explicit type conversion (functional notation) <a id="expr.type.conv">[[expr.type.conv]]</a>

A *simple-type-specifier* ([[dcl.type.simple]]) or
*typename-specifier* ([[temp.res]]) followed by a parenthesized
*expression-list* constructs a value of the specified type given the
expression list. If the expression list is a single expression, the type
conversion expression is equivalent (in definedness, and if defined in
meaning) to the corresponding cast expression ([[expr.cast]]). If the
type specified is a class type, the class type shall be complete. If the
expression list specifies more than a single value, the type shall be a
class with a suitably declared constructor ([[dcl.init]], 
[[class.ctor]]), and the expression `T(x1, x2, ...)` is equivalent in
effect to the declaration `T t(x1, x2, ...);` for some invented
temporary variable `t`, with the result being the value of `t` as a
prvalue.

The expression `T()`, where `T` is a *simple-type-specifier* or
*typename-specifier* for a non-array complete object type or the
(possibly cv-qualified) `void` type, creates a prvalue of the specified
type,which is value-initialized ([[dcl.init]]; no initialization is
done for the `void()` case). if `T` is a non-class type that is
cv-qualified, the *cv-qualifier*s are ignored when determining the type
of the resulting prvalue ([[basic.lval]]).

Similarly, a *simple-type-specifier* or *typename-specifier* followed by
a *braced-init-list* creates a temporary object of the specified type
direct-list-initialized ([[dcl.init.list]]) with the specified
*braced-init-list*, and its value is that temporary object as a prvalue.

### Pseudo destructor call <a id="expr.pseudo">[[expr.pseudo]]</a>

The use of a *pseudo-destructor-name* after a dot `.` or arrow `->`
operator represents the destructor for the non-class type denoted by
*type-name* or *decltype-specifier*. The result shall only be used as
the operand for the function call operator `()`, and the result of such
a call has type `void`. The only effect is the evaluation of the
*postfix-expression* before the dot or arrow.

The left-hand side of the dot operator shall be of scalar type. The
left-hand side of the arrow operator shall be of pointer to scalar type.
This scalar type is the object type. The cv-qualifiercv-unqualified
versions of the object type and of the type designated by the
*pseudo-destructor-name* shall be the same type. Furthermore, the two
*type-name*s in a *pseudo-destructor-name* of the form

``` bnf
nested-name-specifiertₒₚₜype-name ':: ~' type-name
```

shall designate the same scalar type.

### Class member access <a id="expr.ref">[[expr.ref]]</a>

A postfix expression followed by a dot `.` or an arrow `->`, optionally
followed by the keyword `template` ([[temp.names]]), and then followed
by an *id-expression*, is a postfix expression. The postfix expression
before the dot or arrow is evaluated;[^7] the result of that evaluation,
together with the *id-expression*, determines the result of the entire
postfix expression.

For the first option (dot) the first expression shall have complete
class type. For the second option (arrow) the first expression shall
have pointer to complete class type. The expression `E1->E2` is
converted to the equivalent form `(*(E1)).E2`; the remainder of
[[expr.ref]] will address only the first option (dot).[^8] In either
case, the *id-expression* shall name a member of the class or of one of
its base classes. because the name of a class is inserted in its class
scope (Clause  [[class]]), the name of a class is also considered a
nested member of that class. [[basic.lookup.classref]] describes how
names are looked up after the `.` and `->` operators.

Abbreviating *postfix-expression.id-expression* as `E1.E2`, `E1` is
called the *object expression*. The type and value category of `E1.E2`
are determined as follows. In the remainder of  [[expr.ref]],
cv-qualifiercq represents either `const` or the absence of `const` and
cv-qualifiervq represents either `volatile` or the absence of
`volatile`. cv-qualifiercv represents an arbitrary set of cv-qualifiers,
as defined in  [[basic.type.qualifier]].

If `E2` is declared to have type “reference to `T`,” then `E1.E2` is an
lvalue; the type of `E1.E2` is `T`. Otherwise, one of the following
rules applies.

- If `E2` is a static data member and the type of `E2` is `T`, then
  `E1.E2` is an lvalue; the expression designates the named member of
  the class. The type of `E1.E2` is `T`.
- If `E2` is a non-static data member and the type of `E1` is
  “cv-qualifiercq1 vq1 `X`”, and the type of `E2` is “cv-qualifiercq2
  vq2 `T`”, the expression designates the named member of the object
  designated by the first expression. If `E1` is an lvalue, then `E1.E2`
  is an lvalue; if `E1` is an xvalue, then `E1.E2` is an xvalue;
  otherwise, it is a prvalue. Let the notation cv-qualifiervq12 stand
  for the “union” of cv-qualifiervq1 and cv-qualifiervq2; that is, if
  cv-qualifiervq1 or cv-qualifiervq2 is `volatile`, then
  cv-qualifiervq12 is `volatile`. Similarly, let the notation
  cv-qualifiercq12 stand for the “union” of cv-qualifiercq1 and
  cv-qualifiercq2; that is, if cv-qualifiercq1 or cv-qualifiercq2 is
  `const`, then cv-qualifiercq12 is `const`. If `E2` is declared to be a
  `mutable` member, then the type of `E1.E2` is “cv-qualifiervq12 `T`”.
  If `E2` is not declared to be a `mutable` member, then the type of
  `E1.E2` is “cv-qualifiercq12 cv-qualifiervq12 `T`”.
- If `E2` is a (possibly overloaded) member function, function overload
  resolution ([[over.match]]) is used to determine whether `E1.E2`
  refers to a static or a non-static member function.
  - If it refers to a static member function and the type of `E2` is
    “function of parameter-type-list returning `T`”, then `E1.E2` is an
    lvalue; the expression designates the static member function. The
    type of `E1.E2` is the same type as that of `E2`, namely “function
    of parameter-type-list returning `T`”.
  - Otherwise, if `E1.E2` refers to a non-static member function and the
    type of `E2` is “function of parameter-type-list cv-qualifiercv
    *ref-qualifier\opt* returning `T`”, then `E1.E2` is a prvalue. The
    expression designates a non-static member function. The expression
    can be used only as the left-hand operand of a member function
    call ([[class.mfct]]). Any redundant set of parentheses surrounding
    the expression is ignored ([[expr.prim]]). The type of `E1.E2` is
    “function of parameter-type-list cv-qualifiercv returning `T`”.
- If `E2` is a nested type, the expression `E1.E2` is ill-formed.
- If `E2` is a member enumerator and the type of `E2` is `T`, the
  expression `E1.E2` is a prvalue. The type of `E1.E2` is `T`.

If `E2` is a non-static data member or a non-static member function, the
program is ill-formed if the class of which `E2` is directly a member is
an ambiguous base ([[class.member.lookup]]) of the naming class (
[[class.access.base]]) of `E2`. The program is also ill-formed if the
naming class is an ambiguous base of the class type of the object
expression; see  [[class.access.base]].

### Increment and decrement <a id="expr.post.incr">[[expr.post.incr]]</a>

The value of a postfix `++` expression is the value of its operand. the
value obtained is a copy of the original value The operand shall be a
modifiable lvalue. The type of the operand shall be an arithmetic type
or a pointer to a complete object type. The value of the operand object
is modified by adding `1` to it, unless the object is of type `bool`, in
which case it is set to `true`. this use is deprecated, see Annex 
[[depr]]. The value computation of the `++` expression is sequenced
before the modification of the operand object. With respect to an
indeterminately-sequenced function call, the operation of postfix `++`
is a single evaluation. Therefore, a function call shall not intervene
between the lvalue-to-rvalue conversion and the side effect associated
with any single postfix ++ operator. The result is a prvalue. The type
of the result is the cv-unqualified version of the type of the operand.
See also  [[expr.add]] and  [[expr.ass]].

The operand of postfix `\dcr` is decremented analogously to the postfix
`++` operator, except that the operand shall not be of type `bool`. For
prefix increment and decrement, see  [[expr.pre.incr]].

### Dynamic cast <a id="expr.dynamic.cast">[[expr.dynamic.cast]]</a>

The result of the expression `dynamic_cast<T>(v)` is the result of
converting the expression `v` to type `T`. `T` shall be a pointer or
reference to a complete class type, or “pointer to cv-qualifiercv
`void`.” The `dynamic_cast` operator shall not cast away constness (
[[expr.const.cast]]).

If `T` is a pointer type, `v` shall be a prvalue of a pointer to
complete class type, and the result is a prvalue of type `T`. If `T` is
an lvalue reference type, `v` shall be an lvalue of a complete class
type, and the result is an lvalue of the type referred to by `T`. If `T`
is an rvalue reference type, `v` shall be an expression having a
complete class type, and the result is an xvalue of the type referred to
by `T`.

If the type of `v` is the same as `T`, or it is the same as `T` except
that the class object type in `T` is more cv-qualified than the class
object type in `v`, the result is `v` (converted if necessary).

If the value of `v` is a null pointer value in the pointer case, the
result is the null pointer value of type `T`.

If `T` is “pointer to cv-qualifiercv1 `B`” and `v` has type “pointer to
cv-qualifiercv2 `D`” such that `B` is a base class of `D`, the result is
a pointer to the unique `B` subobject of the `D` object pointed to by
`v`. Similarly, if `T` is “reference to cv-qualifiercv1 `B`” and `v` has
type cv-qualifiercv2 `D` such that `B` is a base class of `D`, the
result is the unique `B` subobject of the `D` object referred to by `v`.
[^9] The result is an lvalue if `T` is an lvalue reference, or an xvalue
if `T` is an rvalue reference. In both the pointer and reference cases,
the program is ill-formed if cv-qualifiercv2 has greater
cv-qualification than cv-qualifiercv1 or if `B` is an inaccessible or
ambiguous base class of `D`.

``` cpp
struct B { };
struct D : B { };
void foo(D* dp) {
  B*  bp = dynamic_cast<B*>(dp);    // equivalent to B* bp = dp;
}
```

Otherwise, `v` shall be a pointer to or an lvalue of a polymorphic
type ([[class.virtual]]).

If `T` is “pointer to cv-qualifiercv `void`,” then the result is a
pointer to the most derived object pointed to by `v`. Otherwise, a
run-time check is applied to see if the object pointed or referred to by
`v` can be converted to the type pointed or referred to by `T`.

If `C` is the class type to which `T` points or refers, the run-time
check logically executes as follows:

- If, in the most derived object pointed (referred) to by `v`, `v`
  points (refers) to a `public` base class subobject of a `C` object,
  and if only one object of type `C` is derived from the subobject
  pointed (referred) to by `v` the result points (refers) to that `C`
  object.
- Otherwise, if `v` points (refers) to a `public` base class subobject
  of the most derived object, and the type of the most derived object
  has a base class, of type `C`, that is unambiguous and `public`, the
  result points (refers) to the `C` subobject of the most derived
  object.
- Otherwise, the run-time check *fails*.

The value of a failed cast to pointer type is the null pointer value of
the required result type. A failed cast to reference type throws
`std::bad_cast` ([[bad.cast]]).

``` cpp
class A { virtual void f(); };
class B { virtual void g(); };
class D : public virtual A, private B { };
void g() {
  D   d;
  B*  bp = (B*)&d;                  // cast needed to break protection
  A*  ap = &d;                      // public derivation, no cast needed
  D&  dr = dynamic_cast<D&>(*bp);   // fails
  ap = dynamic_cast<A*>(bp);        // fails
  bp = dynamic_cast<B*>(ap);        // fails
  ap = dynamic_cast<A*>(&d);        // succeeds
  bp = dynamic_cast<B*>(&d);        // ill-formed (not a run-time check)
}

class E : public D, public B { };
class F : public E, public D { };
void h() {
  F   f;
  A*  ap  = &f;                     // succeeds: finds unique A
  D*  dp  = dynamic_cast<D*>(ap);   // fails: yields 0
                                    // f has two D subobjects
  E*  ep  = (E*)ap;                 // ill-formed: cast from virtual base
  E*  ep1 = dynamic_cast<E*>(ap);   // succeeds
}
```

[[class.cdtor]] describes the behavior of a `dynamic_cast` applied to an
object under construction or destruction.

### Type identification <a id="expr.typeid">[[expr.typeid]]</a>

The result of a `typeid` expression is an lvalue of static type `const`
`std::type_info` ([[type.info]]) and dynamic type `const`
`std::type_info` or `const` *name* where *name* is an
*implementation-defined* class publicly derived from `std :: type_info`
which preserves the behavior described in  [[type.info]].[^10] The
lifetime of the object referred to by the lvalue extends to the end of
the program. Whether or not the destructor is called for the
`std::type_info` object at the end of the program is unspecified.

When `typeid` is applied to a glvalue expression whose type is a
polymorphic class type ([[class.virtual]]), the result refers to a
`std::type_info` object representing the type of the most derived
object ([[intro.object]]) (that is, the dynamic type) to which the
glvalue refers. If the glvalue expression is obtained by applying the
unary `*` operator to a pointer[^11] and the pointer is a null pointer
value ([[conv.ptr]]), the `typeid` expression throws the
`std::bad_typeid` exception ([[bad.typeid]]).

When `typeid` is applied to an expression other than a glvalue of a
polymorphic class type, the result refers to a `std::type_info` object
representing the static type of the expression. Lvalue-to-rvalue (
[[conv.lval]]), array-to-pointer ([[conv.array]]), and
function-to-pointer ([[conv.func]]) conversions are not applied to the
expression. If the type of the expression is a class type, the class
shall be completely-defined. The expression is an unevaluated operand
(Clause  [[expr]]).

When `typeid` is applied to a *type-id*, the result refers to a
`std::type_info` object representing the type of the *type-id*. If the
type of the *type-id* is a reference to a possibly
cv-qualifiercv-qualified type, the result of the `typeid` expression
refers to a `std::type_info` object representing the
cv-qualifiercv-unqualified referenced type. If the type of the *type-id*
is a class type or a reference to a class type, the class shall be
completely-defined.

The top-level cv-qualifiers of the glvalue expression or the *type-id*
that is the operand of `typeid` are always ignored.

``` cpp
class D { /* ... */ };
D d1;
const D d2;

typeid(d1) == typeid(d2);       // yields true
typeid(D)  == typeid(const D);  // yields true
typeid(D)  == typeid(d2);       // yields true
typeid(D)  == typeid(const D&); // yields true
```

If the header `<typeinfo>` ([[type.info]]) is not included prior to a
use of `typeid`, the program is ill-formed.

[[class.cdtor]] describes the behavior of `typeid` applied to an object
under construction or destruction.

### Static cast <a id="expr.static.cast">[[expr.static.cast]]</a>

The result of the expression `static_cast<T>(v)` is the result of
converting the expression `v` to type `T`. If `T` is an lvalue reference
type or an rvalue reference to function type, the result is an lvalue;
if `T` is an rvalue reference to object type, the result is an xvalue;
otherwise, the result is a prvalue. The `static_cast` operator shall not
cast away constness ([[expr.const.cast]]).

An lvalue of type “cv-qualifiercv1 `B`,” where `B` is a class type, can
be cast to type “reference to cv-qualifiercv2 `D`,” where `D` is a class
derived (Clause  [[class.derived]]) from `B`, if a valid standard
conversion from “pointer to `D`” to “pointer to `B`” exists (
[[conv.ptr]]), cv-qualifiercv2 is the same cv-qualification as, or
greater cv-qualification than, cv-qualifiercv1, and `B` is neither a
virtual base class of `D` nor a base class of a virtual base class of
`D`. The result has type “cv-qualifiercv2 `D`.” An xvalue of type
“cv-qualifiercv1 `B`” may be cast to type “rvalue reference to
cv-qualifiercv2 `D`” with the same constraints as for an lvalue of type
“cv-qualifiercv1 `B`.” If the object of type “cv-qualifiercv1 `B`” is
actually a subobject of an object of type `D`, the result refers to the
enclosing object of type `D`. Otherwise, the result of the cast is
undefined.

``` cpp
struct B { };
struct D : public B { };
D d;
B &br = d;

static_cast<D&>(br);            // produces lvalue to the original d object
```

A glvalue of type “cv-qualifiercv1 `T1`” can be cast to type “rvalue
reference to cv-qualifiercv2 `T2`” if “cv-qualifiercv2 `T2`” is
reference-compatible with “cv-qualifiercv1 `T1`” ([[dcl.init.ref]]).
The result refers to the object or the specified base class subobject
thereof. If `T2` is an inaccessible (Clause  [[class.access]]) or
ambiguous ([[class.member.lookup]]) base class of `T1`, a program that
necessitates such a cast is ill-formed.

Otherwise, an expression `e` can be explicitly converted to a type `T`
using a `static_cast` of the form `static_cast<T>(e)` if the declaration
`T t(e);` is well-formed, for some invented temporary variable `t` (
[[dcl.init]]). The effect of such an explicit conversion is the same as
performing the declaration and initialization and then using the
temporary variable as the result of the conversion. The expression `e`
is used as a glvalue if and only if the initialization uses it as a
glvalue.

Otherwise, the `static_cast` shall perform one of the conversions listed
below. No other conversion shall be performed explicitly using a
`static_cast`.

Any expression can be explicitly converted to type cv `void`, in which
case it becomes a discarded-value expression (Clause  [[expr]]).
however, if the value is in a temporary object ([[class.temporary]]),
the destructor for that object is not executed until the usual time, and
the value of the object is preserved for the purpose of executing the
destructor.

The inverse of any standard conversion sequence (Clause  [[conv]]) not
containing an lvalue-to-rvalue ([[conv.lval]]), array-to-pointer (
[[conv.array]]), function-to-pointer ([[conv.func]]), null pointer (
[[conv.ptr]]), null member pointer ([[conv.mem]]), or boolean (
[[conv.bool]]) conversion, can be performed explicitly using
`static_cast`. A program is ill-formed if it uses `static_cast` to
perform the inverse of an ill-formed standard conversion sequence.

``` cpp
struct B { };
struct D : private B { };
void f() {
  static_cast<D*>((B*)0);               // Error: B is a private base of D.
  static_cast<int B::*>((int D::*)0);   // Error: B is a private base of D.
}
```

The lvalue-to-rvalue ([[conv.lval]]), array-to-pointer (
[[conv.array]]), and function-to-pointer ([[conv.func]]) conversions
are applied to the operand. Such a `static_cast` is subject to the
restriction that the explicit conversion does not cast away constness (
[[expr.const.cast]]), and the following additional rules for specific
cases:

A value of a scoped enumeration type ([[dcl.enum]]) can be explicitly
converted to an integral type. The value is unchanged if the original
value can be represented by the specified type. Otherwise, the resulting
value is unspecified. A value of a scoped enumeration type can also be
explicitly converted to a floating-point type; the result is the same as
that of converting from the original value to the floating-point type.

A value of integral or enumeration type can be explicitly converted to
an enumeration type. The value is unchanged if the original value is
within the range of the enumeration values ([[dcl.enum]]). Otherwise,
the resulting value is unspecified (and might not be in that range). A
value of floating-point type can also be converted to an enumeration
type. The resulting value is the same as converting the original value
to the underlying type of the enumeration ([[conv.fpint]]), and
subsequently to the enumeration type.

A prvalue of type “pointer to cv-qualifiercv1 `B`,” where `B` is a class
type, can be converted to a prvalue of type “pointer to cv-qualifiercv2
`D`,” where `D` is a class derived (Clause  [[class.derived]]) from `B`,
if a valid standard conversion from “pointer to `D`” to “pointer to `B`”
exists ([[conv.ptr]]), cv-qualifiercv2 is the same cv-qualification as,
or greater cv-qualification than, cv-qualifiercv1, and `B` is neither a
virtual base class of `D` nor a base class of a virtual base class of
`D`. The null pointer value ([[conv.ptr]]) is converted to the null
pointer value of the destination type. If the prvalue of type “pointer
to cv-qualifiercv1 `B`” points to a `B` that is actually a subobject of
an object of type `D`, the resulting pointer points to the enclosing
object of type `D`. Otherwise, the result of the cast is undefined.

A prvalue of type “pointer to member of `D` of type cv-qualifiercv1 `T`”
can be converted to a prvalue of type “pointer to member of `B`” of type
cv-qualifiercv2 `T`, where `B` is a base class (Clause 
[[class.derived]]) of `D`, if a valid standard conversion from “pointer
to member of `B` of type `T`” to “pointer to member of `D` of type `T`”
exists ([[conv.mem]]), and cv-qualifiercv2 is the same cv-qualification
as, or greater cv-qualification than, cv-qualifiercv1.[^12] The null
member pointer value ([[conv.mem]]) is converted to the null member
pointer value of the destination type. If class `B` contains the
original member, or is a base or derived class of the class containing
the original member, the resulting pointer to member points to the
original member. Otherwise, the result of the cast is undefined.
although class `B` need not contain the original member, the dynamic
type of the object on which the pointer to member is dereferenced must
contain the original member; see  [[expr.mptr.oper]].

A prvalue of type “pointer to cv-qualifiercv1 `void`” can be converted
to a prvalue of type “pointer to cv-qualifiercv2 `T`,” where `T` is an
object type and cv-qualifiercv2 is the same cv-qualification as, or
greater cv-qualification than, cv-qualifiercv1. The null pointer value
is converted to the null pointer value of the destination type. A value
of type pointer to object converted to “pointer to cv-qualifiercv
`void`” and back, possibly with different cv-qualification, shall have
its original value.

``` cpp
T* p1 = new T;
const T* p2 = static_cast<const T*>(static_cast<void*>(p1));
bool b = p1 == p2;  // b will have the value true.
```

### Reinterpret cast <a id="expr.reinterpret.cast">[[expr.reinterpret.cast]]</a>

The result of the expression `reinterpret_cast<T>(v)` is the result of
converting the expression `v` to type `T`. If `T` is an lvalue reference
type or an rvalue reference to function type, the result is an lvalue;
if `T` is an rvalue reference to object type, the result is an xvalue;
otherwise, the result is a prvalue and the lvalue-to-rvalue (
[[conv.lval]]), array-to-pointer ([[conv.array]]), and
function-to-pointer ([[conv.func]]) standard conversions are performed
on the expression `v`. Conversions that can be performed explicitly
using `reinterpret_cast` are listed below. No other conversion can be
performed explicitly using `reinterpret_cast`.

The `reinterpret_cast` operator shall not cast away constness (
[[expr.const.cast]]). An expression of integral, enumeration, pointer,
or pointer-to-member type can be explicitly converted to its own type;
such a cast yields the value of its operand.

The mapping performed by `reinterpret_cast` might, or might not, produce
a representation different from the original value.

A pointer can be explicitly converted to any integral type large enough
to hold it. The mapping function is implementation-defined. It is
intended to be unsurprising to those who know the addressing structure
of the underlying machine. A value of type `std::nullptr_t` can be
converted to an integral type; the conversion has the same meaning and
validity as a conversion of `(void*)0` to the integral type. A
`reinterpret_cast` cannot be used to convert a value of any type to the
type `std::nullptr_t`.

A value of integral type or enumeration type can be explicitly converted
to a pointer. A pointer converted to an integer of sufficient size (if
any such exists on the implementation) and back to the same pointer type
will have its original value; mappings between pointers and integers are
otherwise *implementation-defined*. Except as described in
[[basic.stc.dynamic.safety]], the result of such a conversion will not
be a safely-derived pointer value.

A function pointer can be explicitly converted to a function pointer of
a different type. The effect of calling a function through a pointer to
a function type ([[dcl.fct]]) that is not the same as the type used in
the definition of the function is undefined. Except that converting a
prvalue of type “pointer to `T1`” to the type “pointer to `T2`” (where
`T1` and `T2` are function types) and back to its original type yields
the original pointer value, the result of such a pointer conversion is
unspecified. see also  [[conv.ptr]] for more details of pointer
conversions.

An object pointer can be explicitly converted to an object pointer of a
different type.[^13] When a prvalue `v` of type “pointer to `T1`” is
converted to the type “pointer to cv `T2`”, the result is
`static_cast<cv\ T2*>(static_cast<cv\
void*>(v))` if both `T1` and `T2` are standard-layout types (
[[basic.types]]) and the alignment requirements of `T2` are no stricter
than those of `T1`, or if either type is `void`. Converting a prvalue of
type “pointer to `T1`” to the type “pointer to `T2`” (where `T1` and
`T2` are object types and where the alignment requirements of `T2` are
no stricter than those of `T1`) and back to its original type yields the
original pointer value. The result of any other such pointer conversion
is unspecified.

Converting a function pointer to an object pointer type or vice versa is
conditionally-supported. The meaning of such a conversion is
*implementation-defined*, except that if an implementation supports
conversions in both directions, converting a prvalue of one type to the
other type and back, possibly with different cv-qualification, shall
yield the original pointer value.

The null pointer value ([[conv.ptr]]) is converted to the null pointer
value of the destination type. A null pointer constant of type
`std::nullptr_t` cannot be converted to a pointer type, and a null
pointer constant of integral type is not necessarily converted to a null
pointer value.

A prvalue of type “pointer to member of `X` of type `T1`” can be
explicitly converted to a prvalue of a different type “pointer to member
of `Y` of type `T2`” if `T1` and `T2` are both function types or both
object types.[^14] The null member pointer value ([[conv.mem]]) is
converted to the null member pointer value of the destination type. The
result of this conversion is unspecified, except in the following cases:

- converting a prvalue of type “pointer to member function” to a
  different pointer to member function type and back to its original
  type yields the original pointer to member value.
- converting a prvalue of type “pointer to data member of `X` of type
  `T1`” to the type “pointer to data member of `Y` of type `T2`” (where
  the alignment requirements of `T2` are no stricter than those of `T1`)
  and back to its original type yields the original pointer to member
  value.

An lvalue expression of type `T1` can be cast to the type “reference to
`T2`” if an expression of type “pointer to `T1`” can be explicitly
converted to the type “pointer to `T2`” using a `reinterpret_cast`. That
is, a reference cast `reinterpret_cast<T&>(x)` has the same effect as
the conversion `*reinterpret_cast<T*>(&x)` with the built-in `&` and `*`
operators (and similarly for `reinterpret_cast<T&&>(x)`). The result
refers to the same object as the source lvalue, but with a different
type. The result is an lvalue for an lvalue reference type or an rvalue
reference to function type and an xvalue for an rvalue reference to
object type. No temporary is created, no copy is made, and
constructors ([[class.ctor]]) or conversion functions ([[class.conv]])
are not called.[^15]

### Const cast <a id="expr.const.cast">[[expr.const.cast]]</a>

The result of the expression `const_cast<T>(v)` is of type `T`. If `T`
is an lvalue reference to object type, the result is an lvalue; if `T`
is an rvalue reference to object type, the result is an xvalue;
otherwise, the result is a prvalue and the lvalue-to-rvalue (
[[conv.lval]]), array-to-pointer ([[conv.array]]), and
function-to-pointer ([[conv.func]]) standard conversions are performed
on the expression `v`. Conversions that can be performed explicitly
using `const_cast` are listed below. No other conversion shall be
performed explicitly using `const_cast`.

Subject to the restrictions in this section, an expression may be cast
to its own type using a `const_cast` operator.

For two pointer types `T1` and `T2` where

and

where `T` is any object type or the `void` type and where
$\mathit{cv}_{1,k}$ and $\mathit{cv}_{2,k}$ may be different
cv-qualifications, a prvalue of type `T1` may be explicitly converted to
the type `T2` using a `const_cast`. The result of a pointer `const_cast`
refers to the original object.

For two object types `T1` and `T2`, if a pointer to `T1` can be
explicitly converted to the type “pointer to `T2`” using a `const_cast`,
then the following conversions can also be made:

- an lvalue of type `T1` can be explicitly converted to an lvalue of
  type `T2` using the cast `const_cast<T2&>`;
- a glvalue of type `T1` can be explicitly converted to an xvalue of
  type `T2` using the cast `const_cast<T2&&>`; and
- if `T1` is a class type, a prvalue of type `T1` can be explicitly
  converted to an xvalue of type `T2` using the cast `const_cast<T2&&>`.

The result of a reference `const_cast` refers to the original object.

For a `const_cast` involving pointers to data members, multi-level
pointers to data members and multi-level mixed pointers and pointers to
data members ([[conv.qual]]), the rules for `const_cast` are the same
as those used for pointers; the “member” aspect of a pointer to member
is ignored when determining where the cv-qualifiers are added or removed
by the `const_cast`. The result of a pointer to data member `const_cast`
refers to the same member as the original (uncast) pointer to data
member.

A null pointer value ([[conv.ptr]]) is converted to the null pointer
value of the destination type. The null member pointer value (
[[conv.mem]]) is converted to the null member pointer value of the
destination type.

Depending on the type of the object, a write operation through the
pointer, lvalue or pointer to data member resulting from a `const_cast`
that casts away a const-qualifier[^16] may produce undefined behavior (
[[dcl.type.cv]]).

The following rules define the process known as *casting away
constness*. In these rules `Tn ` and `Xn ` represent types. For two
pointer types:

casting from `X1` to `X2` casts away constness if, for a non-pointer
type `T` there does not exist an implicit conversion (Clause  [[conv]])
from:

to

Casting from an lvalue of type `T1` to an lvalue of type `T2` using an
lvalue reference cast or casting from an expression of type `T1` to an
xvalue of type `T2` using an rvalue reference cast casts away constness
if a cast from a prvalue of type “pointer to `T1`” to the type “pointer
to `T2`” casts away constness.

Casting from a prvalue of type “pointer to data member of `X` of type
`T1`” to the type “pointer to data member of `Y` of type `T2`” casts
away constness if a cast from a prvalue of type “pointer to `T1`” to the
type “pointer to `T2`” casts away constness.

For multi-level pointer to members and multi-level mixed pointers and
pointer to members ([[conv.qual]]), the “member” aspect of a pointer to
member level is ignored when determining if a `const` cv-qualifier has
been cast away.

some conversions which involve only changes in cv-qualification cannot
be done using `const_cast.` For instance, conversions between pointers
to functions are not covered because such conversions lead to values
whose use causes undefined behavior. For the same reasons, conversions
between pointers to member functions, and in particular, the conversion
from a pointer to a const member function to a pointer to a non-const
member function, are not covered.

## Unary expressions <a id="expr.unary">[[expr.unary]]</a>

Expressions with unary operators group right-to-left.

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

### Unary operators <a id="expr.unary.op">[[expr.unary.op]]</a>

The unary `*` operator performs *indirection*: the expression to which
it is applied shall be a pointer to an object type, or a pointer to a
function type and the result is an lvalue referring to the object or
function to which the expression points. If the type of the expression
is “pointer to `T`,” the type of the result is “`T`.” a pointer to an
incomplete type (other than cv-qualifiercv `void`) can be dereferenced.
The lvalue thus obtained can be used in limited ways (to initialize a
reference, for example); this lvalue must not be converted to a prvalue,
see  [[conv.lval]].

The result of each of the following unary operators is a prvalue.

The result of the unary `&` operator is a pointer to its operand. The
operand shall be an lvalue or a *qualified-id*. If the operand is a
*qualified-id* naming a non-static member `m` of some class `C` with
type `T`, the result has type “pointer to member of class `C` of type
`T`” and is a prvalue designating `C::m`. Otherwise, if the type of the
expression is `T`, the result has type “pointer to `T`” and is a prvalue
that is the address of the designated object ([[intro.memory]]) or a
pointer to the designated function. In particular, the address of an
object of type “cv `T`” is “pointer to cv `T`”, with the same
cv-qualification.

``` cpp
struct A { int i; };
struct B : A { };
... &B::i ...       // has type int A::*
```

a pointer to member formed from a `mutable` non-static data member (
[[dcl.stc]]) does not reflect the `mutable` specifier associated with
the non-static data member.

A pointer to member is only formed when an explicit `&` is used and its
operand is a *qualified-id* not enclosed in parentheses. that is, the
expression `&(qualified-id)`, where the *qualified-id* is enclosed in
parentheses, does not form an expression of type “pointer to member.”
Neither does `qualified-id`, because there is no implicit conversion
from a *qualified-id* for a non-static member function to the type
“pointer to member function” as there is from an lvalue of function type
to the type “pointer to function” ([[conv.func]]). Nor is
`&unqualified-id` a pointer to member, even within the scope of the
*unqualified-id*’s class.

The address of an object of incomplete type can be taken, but if the
complete type of that object is a class type that declares `operator&()`
as a member function, then the behavior is undefined (and no diagnostic
is required). The operand of `&` shall not be a bit-field.

The address of an overloaded function (Clause  [[over]]) can be taken
only in a context that uniquely determines which version of the
overloaded function is referred to (see  [[over.over]]). since the
context might determine whether the operand is a static or non-static
member function, the context can also affect whether the expression has
type “pointer to function” or “pointer to member function.”

The operand of the unary `+` operator shall have arithmetic, unscoped
enumeration, or pointer type and the result is the value of the
argument. Integral promotion is performed on integral or enumeration
operands. The type of the result is the type of the promoted operand.

The operand of the unary `-` operator shall have arithmetic or unscoped
enumeration type and the result is the negation of its operand. Integral
promotion is performed on integral or enumeration operands. The negative
of an unsigned quantity is computed by subtracting its value from 2ⁿ,
where n is the number of bits in the promoted operand. The type of the
result is the type of the promoted operand.

The operand of the logical negation operator `!` is contextually
converted to `bool` (Clause  [[conv]]); its value is `true` if the
converted operand is `false` and `false` otherwise. The type of the
result is `bool`.

The operand of `~` shall have integral or unscoped enumeration type; the
result is the one’s complement of its operand. Integral promotions are
performed. The type of the result is the type of the promoted operand.
There is an ambiguity in the *unary-expression* `~X()`, where `X` is a
*class-name* or *decltype-specifier*. The ambiguity is resolved in favor
of treating `~` as a unary complement rather than treating `~X` as
referring to a destructor.

### Increment and decrement <a id="expr.pre.incr">[[expr.pre.incr]]</a>

The operand of prefix `++` is modified by adding `1`, or set to `true`
if it is `bool` (this use is deprecated). The operand shall be a
modifiable lvalue. The type of the operand shall be an arithmetic type
or a pointer to a completely-defined object type. The result is the
updated operand; it is an lvalue, and it is a bit-field if the operand
is a bit-field. If `x` is not of type `bool`, the expression `++x` is
equivalent to `x+=1` See the discussions of addition ([[expr.add]]) and
assignment operators ([[expr.ass]]) for information on conversions.

The operand of prefix `\dcr` is modified by subtracting `1`. The operand
shall not be of type `bool`. The requirements on the operand of prefix
`\dcr` and the properties of its result are otherwise the same as those
of prefix `++`. For postfix increment and decrement, see 
[[expr.post.incr]].

### Sizeof <a id="expr.sizeof">[[expr.sizeof]]</a>

The `sizeof` operator yields the number of bytes in the object
representation of its operand. The operand is either an expression,
which is an unevaluated operand (Clause  [[expr]]), or a parenthesized
*type-id*. The `sizeof` operator shall not be applied to an expression
that has function or incomplete type, to an enumeration type whose
underlying type is not fixed before all its enumerators have been
declared, to the parenthesized name of such types, or to an lvalue that
designates a bit-field. `sizeof(char)`, `sizeof(signed char)` and
`sizeof(unsigned char)` are `1`. The result of `sizeof` applied to any
other fundamental type ([[basic.fundamental]]) is
*implementation-defined*. in particular, `sizeof(bool)`,
`sizeof(char16_t)`, `sizeof(char32_t)`, and `sizeof(wchar_t)` are
implementation-defined.[^17] See  [[intro.memory]] for the definition of
*byte* and  [[basic.types]] for the definition of *object
representation*.

When applied to a reference or a reference type, the result is the size
of the referenced type. When applied to a class, the result is the
number of bytes in an object of that class including any padding
required for placing objects of that type in an array. The size of a
most derived class shall be greater than zero ([[intro.object]]). The
result of applying `sizeof` to a base class subobject is the size of the
base class type.[^18] When applied to an array, the result is the total
number of bytes in the array. This implies that the size of an array of
*n* elements is *n* times the size of an element.

The `sizeof` operator can be applied to a pointer to a function, but
shall not be applied directly to a function.

The lvalue-to-rvalue ([[conv.lval]]), array-to-pointer (
[[conv.array]]), and function-to-pointer ([[conv.func]]) standard
conversions are not applied to the operand of `sizeof`.

The identifier in a `sizeof...` expression shall name a parameter pack.
The `sizeof...` operator yields the number of arguments provided for the
parameter pack *identifier*. A `sizeof...` expression is a pack
expansion ([[temp.variadic]]).

``` cpp
template<class... Types>
struct count {
  static const std::size_t value = sizeof...(Types);
};
```

The result of `sizeof` and `sizeof...` is a constant of type
`std::size_t`. `std::size_t` is defined in the standard header
`<cstddef>` ([[support.types]]).

### New <a id="expr.new">[[expr.new]]</a>

The *new-expression* attempts to create an object of the *type-id* (
[[dcl.name]]) or *new-type-id* to which it is applied. The type of that
object is the *allocated type*. This type shall be a complete object
type, but not an abstract class type or array thereof (
[[intro.object]],  [[basic.types]],  [[class.abstract]]). It is
*implementation-defined* whether over-aligned types are supported (
[[basic.align]]). because references are not objects, references cannot
be created by *new-expression*s. the *type-id* may be a cv-qualified
type, in which case the object created by the *new-expression* has a
cv-qualified type.

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

Entities created by a *new-expression* have dynamic storage duration (
[[basic.stc.dynamic]]). the lifetime of such an entity is not
necessarily restricted to the scope in which it is created. If the
entity is a non-array object, the *new-expression* returns a pointer to
the object created. If it is an array, the *new-expression* returns a
pointer to the initial element of the array.

If the `auto` appears in the of a or of a , the shall contain a of the
form

``` bnf
'(' assignment-expression ')'
```

The allocated type is deduced from the as follows: Let `e` be the
*assignment-expression* in the and `T` be the or of the , then the
allocated type is the type deduced for the variable `x` in the invented
declaration ([[dcl.spec.auto]]):

``` cpp
T x(e);
```

``` cpp
new auto(1);                    // allocated type is int
auto x = new auto('a');         // allocated type is char, x is of type char*
```

The *new-type-id* in a *new-expression* is the longest possible sequence
of *new-declarator*s. this prevents ambiguities between the declarator
operators `&`, `&&`, `*`, and `[]` and their expression counterparts.

``` cpp
new int * i;                    // syntax error: parsed as (new int*) i, not as (new int)*i
```

The `*` is the pointer declarator and not the multiplication operator.

parentheses in a *new-type-id* of a *new-expression* can have surprising
effects.

``` cpp
new int(*[10])();               // error
```

is ill-formed because the binding is

``` cpp
(new int) (*[10])();            // error
```

Instead, the explicitly parenthesized version of the `new` operator can
be used to create objects of compound types ([[basic.compound]]):

``` cpp
new (int (*[10])());
```

allocates an array of `10` pointers to functions (taking no argument and
returning `int`.

When the allocated object is an array (that is, the
*noptr-new-declarator* syntax is used or the *new-type-id* or *type-id*
denotes an array type), the *new-expression* yields a pointer to the
initial element (if any) of the array. both `new int` and `new int[10]`
have type `int*` and the type of `new int[i][10]` is `int (*)[10]` The
*attribute-specifier-seq* in a *noptr-new-declarator* appertains to the
associated array type.

Every *constant-expression* in a *noptr-new-declarator* shall be an
integral constant expression ([[expr.const]]) and evaluate to a
strictly positive value. The *expression* in a *noptr-new-declarator*
shall be of integral type, unscoped enumeration type, or a class type
for which a single non-explicit conversion function to integral or
unscoped enumeration type exists ([[class.conv]]). If the expression is
of class type, the expression is converted by calling that conversion
function, and the result of the conversion is used in place of the
original expression. given the definition `int n = 42`,
`new float[n][5]` is well-formed (because `n` is the *expression* of a
*noptr-new-declarator*), but `new float[5][n]` is ill-formed (because
`n` is not a constant expression).

When the value of the *expression* in a *noptr-new-declarator* is zero,
the allocation function is called to allocate an array with no elements.
If the value of that *expression* is less than zero or such that the
size of the allocated object would exceed the implementation-defined
limit, or if the *new-initializer* is a *braced-init-list* for which the
number of *initializer-clause*s exceeds the number of elements to
initialize, no storage is obtained and the *new-expression* terminates
by throwing an exception of a type that would match a handler (
[[except.handle]]) of type `std::bad_array_new_length` (
[[new.badlength]]).

A *new-expression* obtains storage for the object by calling an
*allocation function* ([[basic.stc.dynamic.allocation]]). If the
*new-expression* terminates by throwing an exception, it may release
storage by calling a deallocation function (
[[basic.stc.dynamic.deallocation]]). If the allocated type is a
non-array type, the allocation function’s name is `operator new` and the
deallocation function’s name is `operator delete`. If the allocated type
is an array type, the allocation function’s name is `operator new[]` and
the deallocation function’s name is `operator delete[]`. an
implementation shall provide default definitions for the global
allocation functions ([[basic.stc.dynamic]],  [[new.delete.single]], 
[[new.delete.array]]). A C++program can provide alternative definitions
of these functions ([[replacement.functions]]) and/or class-specific
versions ([[class.free]]).

If the *new-expression* begins with a unary `::` operator, the
allocation function’s name is looked up in the global scope. Otherwise,
if the allocated type is a class type `T` or array thereof, the
allocation function’s name is looked up in the scope of `T`. If this
lookup fails to find the name, or if the allocated type is not a class
type, the allocation function’s name is looked up in the global scope.

A *new-expression* passes the amount of space requested to the
allocation function as the first argument of type `std::size_t`. That
argument shall be no less than the size of the object being created; it
may be greater than the size of the object being created only if the
object is an array. For arrays of `char` and `unsigned char`, the
difference between the result of the *new-expression* and the address
returned by the allocation function shall be an integral multiple of the
strictest fundamental alignment requirement ([[basic.align]]) of any
object type whose size is no greater than the size of the array being
created. Because allocation functions are assumed to return pointers to
storage that is appropriately aligned for objects of any type with
fundamental alignment, this constraint on array allocation overhead
permits the common idiom of allocating character arrays into which
objects of other types will later be placed.

The *new-placement* syntax is used to supply additional arguments to an
allocation function. If used, overload resolution is performed on a
function call created by assembling an argument list consisting of the
amount of space requested (the first argument) and the expressions in
the *new-placement* part of the *new-expression* (the second and
succeeding arguments). The first of these arguments has type
`std::size_t` and the remaining arguments have the corresponding types
of the expressions in the *new-placement*.

- `new T` results in a call of `operator
  new(sizeof(T))`,
- `new(2,f) T` results in a call of `operator
  new(sizeof(T),2,f)`,
- `new T[5]` results in a call of `operator
  new[](sizeof(T)*5+x)`, and
- `new(2,f) T[5]` results in a call of `operator
  new[](sizeof(T)*5+y,2,f)`.

Here, `x` and `y` are non-negative unspecified values representing array
allocation overhead; the result of the *new-expression* will be offset
by this amount from the value returned by `operator new[]`. This
overhead may be applied in all array *new-expression*s, including those
referencing the library function `operator new[](std::size_t, void*)`
and other placement allocation functions. The amount of overhead may
vary from one invocation of `new` to another.

unless an allocation function is declared with a non-throwing
*exception-specification* ([[except.spec]]), it indicates failure to
allocate storage by throwing a `std::bad_alloc` exception (Clause 
[[except]],  [[bad.alloc]]); it returns a non-null pointer otherwise. If
the allocation function is declared with a non-throwing
*exception-specification*, it returns null to indicate failure to
allocate storage and a non-null pointer otherwise. If the allocation
function returns null, initialization shall not be done, the
deallocation function shall not be called, and the value of the
*new-expression* shall be null.

when the allocation function returns a value other than null, it must be
a pointer to a block of storage in which space for the object has been
reserved. The block of storage is assumed to be appropriately aligned
and of the requested size. The address of the created object will not
necessarily be the same as that of the block if the object is an array.

A *new-expression* that creates an object of type `T` initializes that
object as follows:

- If the *new-initializer* is omitted, the object is
  default-initialized ([[dcl.init]]); if no initialization is
  performed, the object has indeterminate value.
- Otherwise, the *new-initializer* is interpreted according to the
  initialization rules of  [[dcl.init]] for direct-initialization.

The invocation of the allocation function is indeterminately sequenced
with respect to the evaluations of expressions in the *new-initializer*.
Initialization of the allocated object is sequenced before the value
computation of the *new-expression*. It is unspecified whether
expressions in the *new-initializer* are evaluated if the allocation
function returns the null pointer or exits using an exception.

If the *new-expression* creates an object or an array of objects of
class type, access and ambiguity control are done for the allocation
function, the deallocation function ([[class.free]]), and the
constructor ([[class.ctor]]). If the new expression creates an array of
objects of class type, access and ambiguity control are done for the
destructor ([[class.dtor]]).

If any part of the object initialization described above[^19] terminates
by throwing an exception and a suitable deallocation function can be
found, the deallocation function is called to free the memory in which
the object was being constructed, after which the exception continues to
propagate in the context of the *new-expression*. If no unambiguous
matching deallocation function can be found, propagating the exception
does not cause the object’s memory to be freed. This is appropriate when
the called allocation function does not allocate memory; otherwise, it
is likely to result in a memory leak.

If the *new-expression* begins with a unary `::` operator, the
deallocation function’s name is looked up in the global scope.
Otherwise, if the allocated type is a class type `T` or an array
thereof, the deallocation function’s name is looked up in the scope of
`T`. If this lookup fails to find the name, or if the allocated type is
not a class type or array thereof, the deallocation function’s name is
looked up in the global scope.

A declaration of a placement deallocation function matches the
declaration of a placement allocation function if it has the same number
of parameters and, after parameter transformations ([[dcl.fct]]), all
parameter types except the first are identical. Any non-placement
deallocation function matches a non-placement allocation function. If
the lookup finds a single matching deallocation function, that function
will be called; otherwise, no deallocation function will be called. If
the lookup finds the two-parameter form of a usual deallocation
function ([[basic.stc.dynamic.deallocation]]) and that function,
considered as a placement deallocation function, would have been
selected as a match for the allocation function, the program is
ill-formed.

``` cpp
struct S {
  // Placement allocation function:
  static void* operator new(std::size_t, std::size_t);

  // Usual (non-placement) deallocation function:
  static void operator delete(void*, std::size_t);
};

S* p = new (0) S;   // ill-formed: non-placement deallocation function matches
                    // placement allocation function
```

If a *new-expression* calls a deallocation function, it passes the value
returned from the allocation function call as the first argument of type
`void*`. If a placement deallocation function is called, it is passed
the same additional arguments as were passed to the placement allocation
function, that is, the same arguments as those specified with the
*new-placement* syntax. If the implementation is allowed to make a copy
of any argument as part of the call to the allocation function, it is
allowed to make a copy (of the same original value) as part of the call
to the deallocation function or to reuse the copy made as part of the
call to the allocation function. If the copy is elided in one place, it
need not be elided in the other.

### Delete <a id="expr.delete">[[expr.delete]]</a>

The *delete-expression* operator destroys a most derived object (
[[intro.object]]) or array created by a *new-expression*.

``` bnf
delete-expression:
    '::'\terminal ₒₚₜ{delete} cast-expression
    '::'\terminal ₒₚₜ{delete [ ]} cast-expression
```

The first alternative is for non-array objects, and the second is for
arrays. Whenever the `delete` keyword is immediately followed by empty
square brackets, it shall be interpreted as the second alternative.[^20]
The operand shall have a pointer to object type, or a class type having
a single non-explicit conversion function ([[class.conv.fct]]) to a
pointer to object type. The result has type `void`.[^21]

If the operand has a class type, the operand is converted to a pointer
type by calling the above-mentioned conversion function, and the
converted operand is used in place of the original operand for the
remainder of this section. In the first alternative (*delete object*),
the value of the operand of `delete` may be a null pointer value, a
pointer to a non-array object created by a previous *new-expression*, or
a pointer to a subobject ([[intro.object]]) representing a base class
of such an object (Clause  [[class.derived]]). If not, the behavior is
undefined. In the second alternative (*delete array*), the value of the
operand of `delete` may be a null pointer value or a pointer value that
resulted from a previous array *new-expression*.[^22] If not, the
behavior is undefined. this means that the syntax of the
*delete-expression* must match the type of the object allocated by
`new`, not the syntax of the *new-expression*. a pointer to a `const`
type can be the operand of a *delete-expression*; it is not necessary to
cast away the constness ([[expr.const.cast]]) of the pointer expression
before it is used as the operand of the *delete-expression*.

In the first alternative (*delete object*), if the static type of the
object to be deleted is different from its dynamic type, the static type
shall be a base class of the dynamic type of the object to be deleted
and the static type shall have a virtual destructor or the behavior is
undefined. In the second alternative (*delete array*) if the dynamic
type of the object to be deleted differs from its static type, the
behavior is undefined.

The *cast-expression* in a *delete-expression* shall be evaluated
exactly once.

If the object being deleted has incomplete class type at the point of
deletion and the complete class has a non-trivial destructor or a
deallocation function, the behavior is undefined.

If the value of the operand of the *delete-expression* is not a null
pointer value, the *delete-expression* will invoke the destructor (if
any) for the object or the elements of the array being deleted. In the
case of an array, the elements will be destroyed in order of decreasing
address (that is, in reverse order of the completion of their
constructor; see  [[class.base.init]]).

If the value of the operand of the *delete-expression* is not a null
pointer value, the *delete-expression* will call a *deallocation
function* ([[basic.stc.dynamic.deallocation]]). Otherwise, it is
unspecified whether the deallocation function will be called. The
deallocation function is called regardless of whether the destructor for
the object or some element of the array throws an exception.

An implementation provides default definitions of the global
deallocation functions `operator delete()` for non-arrays (
[[new.delete.single]]) and `operator delete[]()` for arrays (
[[new.delete.array]]). A C++ program can provide alternative definitions
of these functions ([[replacement.functions]]), and/or class-specific
versions ([[class.free]]).

When the keyword `delete` in a *delete-expression* is preceded by the
unary `::` operator, the global deallocation function is used to
deallocate the storage.

Access and ambiguity control are done for both the deallocation function
and the destructor ([[class.dtor]],  [[class.free]]).

### Alignof <a id="expr.alignof">[[expr.alignof]]</a>

An `alignof` expression yields the alignment requirement of its operand
type. The operand shall be a *type-id* representing a complete object
type or an array thereof or a reference to a complete object type.

The result is an integral constant of type `std::size_t`.

When `alignof` is applied to a reference type, the result shall be the
alignment of the referenced type. When `alignof` is applied to an array
type, the result shall be the alignment of the element type.

### `noexcept` operator <a id="expr.unary.noexcept">[[expr.unary.noexcept]]</a>

The `noexcept` operator determines whether the evaluation of its
operand, which is an unevaluated operand (Clause  [[expr]]), can throw
an exception ([[except.throw]]).

``` bnf
noexcept-expression:
  'noexcept' '(' expression ')'
```

The result of the `noexcept` operator is a constant of type `bool` and
is an rvalue.

The result of the `noexcept` operator is `false` if in a
potentially-evaluated context the *expression* would contain

- a potentially evaluated call[^23] to a function, member function,
  function pointer, or member function pointer that does not have a
  non-throwing *exception-specification* ([[except.spec]]), unless the
  call is a constant expression ([[expr.const]]),
- a potentially evaluated *throw-expression* ([[except.throw]]),
- a potentially evaluated `dynamic_cast` expression
  `dynamic_cast<T>(v)`, where `T` is a reference type, that requires a
  run-time check ([[expr.dynamic.cast]]), or
- a potentially evaluated `typeid` expression ([[expr.typeid]]) applied
  to a glvalue expression whose type is a polymorphic class type (
  [[class.virtual]]).

Otherwise, the result is `true`.

## Explicit type conversion (cast notation) <a id="expr.cast">[[expr.cast]]</a>

The result of the expression `(T)` *cast-expression* is of type `T`. The
result is an lvalue if `T` is an lvalue reference type or an rvalue
reference to function type and an xvalue if `T` is an rvalue reference
to object type; otherwise the result is a prvalue. if `T` is a non-class
type that is *cv-qualified*, the *cv-qualifiers* are ignored when
determining the type of the resulting prvalue; see  [[basic.lval]].

An explicit type conversion can be expressed using functional notation (
[[expr.type.conv]]), a type conversion operator (`dynamic_cast`,
`static_cast`, `reinterpret_cast`, `const_cast`), or the *cast*
notation.

``` bnf
cast-expression:
    unary-expression
    '(' type-id ')' cast-expression
```

Any type conversion not mentioned below and not explicitly defined by
the user ([[class.conv]]) is ill-formed.

The conversions performed by

- a `const_cast` ([[expr.const.cast]]),
- a `static_cast` ([[expr.static.cast]]),
- a `static_cast` followed by a `const_cast`,
- a `reinterpret_cast` ([[expr.reinterpret.cast]]), or
- a `reinterpret_cast` followed by a `const_cast`,

can be performed using the cast notation of explicit type conversion.
The same semantic restrictions and behaviors apply, with the exception
that in performing a `static_cast` in the following situations the
conversion is valid even if the base class is inaccessible:

- a pointer to an object of derived class type or an lvalue or rvalue of
  derived class type may be explicitly converted to a pointer or
  reference to an unambiguous base class type, respectively;
- a pointer to member of derived class type may be explicitly converted
  to a pointer to member of an unambiguous non-virtual base class type;
- a pointer to an object of an unambiguous non-virtual base class type,
  a glvalue of an unambiguous non-virtual base class type, or a pointer
  to member of an unambiguous non-virtual base class type may be
  explicitly converted to a pointer, a reference, or a pointer to member
  of a derived class type, respectively.

If a conversion can be interpreted in more than one of the ways listed
above, the interpretation that appears first in the list is used, even
if a cast resulting from that interpretation is ill-formed. If a
conversion can be interpreted in more than one way as a `static_cast`
followed by a `const_cast`, the conversion is ill-formed.

``` cpp
struct A { };
struct I1 : A { };
struct I2 : A { };
struct D : I1, I2 { };
A *foo( D *p ) {
  return (A*)( p ); // ill-formed static_cast interpretation
}
```

The operand of a cast using the cast notation can be a prvalue of type
“pointer to incomplete class type”. The destination type of a cast using
the cast notation can be “pointer to incomplete class type”. If both the
operand and destination types are class types and one or both are
incomplete, it is unspecified whether the `static_cast` or the
`reinterpret_cast` interpretation is used, even if there is an
inheritance relationship between the two classes. For example, if the
classes were defined later in the translation unit, a multi-pass
compiler would be permitted to interpret a cast between pointers to the
classes as if the class types were complete at the point of the cast.

## Pointer-to-member operators <a id="expr.mptr.oper">[[expr.mptr.oper]]</a>

The pointer-to-member operators `->*` and `.*` group left-to-right.

``` bnf
pm-expression:
    cast-expression
    pm-expression '.*' cast-expression
    pm-expression '->*' cast-expression
```

The binary operator `.*` binds its second operand, which shall be of
type “pointer to member of `T`” (where `T` is a completely-defined class
type) to its first operand, which shall be of class `T` or of a class of
which `T` is an unambiguous and accessible base class. The result is an
object or a function of the type specified by the second operand.

The binary operator `->*` binds its second operand, which shall be of
type “pointer to member of `T`” (where `T` is a completely-defined class
type) to its first operand, which shall be of type “pointer to `T`” or
“pointer to a class of which `T` is an unambiguous and accessible base
class.” The expression `E1->*E2` is converted into the equivalent form
`(*(E1)).*E2`.

Abbreviating *pm-expression*`.*`*cast-expression* as `E1.*E2`, `E1` is
called the *object expression*. If the dynamic type of `E1` does not
contain the member to which `E2` refers, the behavior is undefined.

The restrictions on cv-qualifiercv-qualification, and the manner in
which the cv-qualifiercv-qualifiers of the operands are combined to
produce the cv-qualifiercv-qualifiers of the result, are the same as the
rules for `E1.E2` given in  [[expr.ref]]. it is not possible to use a
pointer to member that refers to a `mutable` member to modify a `const`
class object. For example,

``` cpp
struct S {
  S() : i(0) { }
  mutable int i;
};
void f()
{
const S cs;
int S::* pm = &S::i;            // pm refers to mutable member S::i
cs.*pm = 88;                    // ill-formed: cs is a const object
}
```

If the result of `.*` or `->*` is a function, then that result can be
used only as the operand for the function call operator `()`.

``` cpp
(ptr_to_obj->*ptr_to_mfct)(10);
```

calls the member function denoted by `ptr_to_mfct` for the object
pointed to by `ptr_to_obj`. In a `.*` expression whose object expression
is an rvalue, the program is ill-formed if the second operand is a
pointer to member function with *ref-qualifier* `&`. In a `.*`
expression whose object expression is an lvalue, the program is
ill-formed if the second operand is a pointer to member function with
*ref-qualifier* `&&`. The result of a `.*` expression whose second
operand is a pointer to a data member is of the same value category (
[[basic.lval]]) as its first operand. The result of a `.*` expression
whose second operand is a pointer to a member function is a prvalue. If
the second operand is the null pointer to member value ([[conv.mem]]),
the behavior is undefined.

## Multiplicative operators <a id="expr.mul">[[expr.mul]]</a>

The multiplicative operators `*`, `/`, and `%` group left-to-right.

``` bnf
multiplicative-expression:
    pm-expression
    multiplicative-expression '*' pm-expression
    multiplicative-expression '/' pm-expression
    multiplicative-expression '%' pm-expression
```

The operands of `*` and `/` shall have arithmetic or unscoped
enumeration type; the operands of `%` shall have integral or unscoped
enumeration type. The usual arithmetic conversions are performed on the
operands and determine the type of the result.

The binary `*` operator indicates multiplication.

The binary `/` operator yields the quotient, and the binary `%` operator
yields the remainder from the division of the first expression by the
second. If the second operand of `/` or `%` is zero the behavior is
undefined. For integral operands the `/` operator yields the algebraic
quotient with any fractional part discarded;[^24] if the quotient `a/b`
is representable in the type of the result, `(a/b)*b + a%b` is equal to
`a`.

## Additive operators <a id="expr.add">[[expr.add]]</a>

The additive operators `+` and `-` group left-to-right. The usual
arithmetic conversions are performed for operands of arithmetic or
enumeration type.

``` bnf
additive-expression:
    multiplicative-expression
    additive-expression '+' multiplicative-expression
    additive-expression '-' multiplicative-expression
```

For addition, either both operands shall have arithmetic or unscoped
enumeration type, or one operand shall be a pointer to a
completely-defined object type and the other shall have integral or
unscoped enumeration type.

For subtraction, one of the following shall hold:

- both operands have arithmetic or unscoped enumeration type; or
- both operands are pointers to cv-qualified or cv-unqualified versions
  of the same completely-defined object type; or
- the left operand is a pointer to a completely-defined object type and
  the right operand has integral or unscoped enumeration type.

The result of the binary `+` operator is the sum of the operands. The
result of the binary `-` operator is the difference resulting from the
subtraction of the second operand from the first.

For the purposes of these operators, a pointer to a nonarray object
behaves the same as a pointer to the first element of an array of length
one with the type of the object as its element type.

When an expression that has integral type is added to or subtracted from
a pointer, the result has the type of the pointer operand. If the
pointer operand points to an element of an array object, and the array
is large enough, the result points to an element offset from the
original element such that the difference of the subscripts of the
resulting and original array elements equals the integral expression. In
other words, if the expression `P` points to the i-th element of an
array object, the expressions `(P)+N` (equivalently, `N+(P)`) and
`(P)-N` (where `N` has the value n) point to, respectively, the i+n-th
and i-n-th elements of the array object, provided they exist. Moreover,
if the expression `P` points to the last element of an array object, the
expression `(P)+1` points one past the last element of the array object,
and if the expression `Q` points one past the last element of an array
object, the expression `(Q)-1` points to the last element of the array
object. If both the pointer operand and the result point to elements of
the same array object, or one past the last element of the array object,
the evaluation shall not produce an overflow; otherwise, the behavior is
undefined.

When two pointers to elements of the same array object are subtracted,
the result is the difference of the subscripts of the two array
elements. The type of the result is an *implementation-defined* signed
integral type; this type shall be the same type that is defined as
`std::ptrdiff_t` in the `<cstddef>` header ([[support.types]]). As with
any other arithmetic overflow, if the result does not fit in the space
provided, the behavior is undefined. In other words, if the expressions
`P` and `Q` point to, respectively, the i-th and j-th elements of an
array object, the expression `(P)-(Q)` has the value i-j provided the
value fits in an object of type `std::ptrdiff_t`. Moreover, if the
expression `P` points either to an element of an array object or one
past the last element of an array object, and the expression `Q` points
to the last element of the same array object, the expression
`((Q)+1)-(P)` has the same value as `((Q)-(P))+1` and as
`-((P)-((Q)+1))`, and has the value zero if the expression `P` points
one past the last element of the array object, even though the
expression `(Q)+1` does not point to an element of the array object.
Unless both pointers point to elements of the same array object, or one
past the last element of the array object, the behavior is
undefined.[^25]

If the value 0 is added to or subtracted from a pointer value, the
result compares equal to the original pointer value. If two pointers
point to the same object or both point one past the end of the same
array or both are null, and the two pointers are subtracted, the result
compares equal to the value 0 converted to the type `std::ptrdiff_t`.

## Shift operators <a id="expr.shift">[[expr.shift]]</a>

The shift operators `\shl` and `\shr` group left-to-right.

``` bnf
shift-expression:
    additive-expression
    shift-expression '\shl' additive-expression
    shift-expression '\shr' additive-expression
```

The operands shall be of integral or unscoped enumeration type and
integral promotions are performed. The type of the result is that of the
promoted left operand. The behavior is undefined if the right operand is
negative, or greater than or equal to the length in bits of the promoted
left operand.

The value of `E1 \shl\ E2` is `E1` left-shifted `E2` bit positions;
vacated bits are zero-filled. If `E1` has an unsigned type, the value of
the result is $\mathrm{E1}\times2^\mathrm{E2}$, reduced modulo one more
than the maximum value representable in the result type. Otherwise, if
`E1` has a signed type and non-negative value, and
$\mathrm{E1}\times2^\mathrm{E2}$ is representable in the result type,
then that is the resulting value; otherwise, the behavior is undefined.

The value of `E1 \shr\ E2` is `E1` right-shifted `E2` bit positions. If
`E1` has an unsigned type or if `E1` has a signed type and a
non-negative value, the value of the result is the integral part of the
quotient of $\mathrm{E1}/2^\mathrm{E2}$. If `E1` has a signed type and a
negative value, the resulting value is *implementation-defined*.

## Relational operators <a id="expr.rel">[[expr.rel]]</a>

The relational operators group left-to-right. `a<b<c` means `(a<b)<c`
and *not* `(a<b)&&(b<c)`.

``` bnf
relational-expression:
    shift-expression
    relational-expression '<' shift-expression
    relational-expression '>' shift-expression
    relational-expression '<=' shift-expression
    relational-expression '>=' shift-expression
```

The operands shall have arithmetic, enumeration, or pointer type, or
type `std::nullptr_t`. The operators `<` (less than), `>` (greater
than), `<=` (less than or equal to), and `>=` (greater than or equal to)
all yield `false` or `true`. The type of the result is `bool`.

The usual arithmetic conversions are performed on operands of arithmetic
or enumeration type. Pointer conversions ([[conv.ptr]]) and
qualification conversions ([[conv.qual]]) are performed on pointer
operands (or on a pointer operand and a null pointer constant, or on two
null pointer constants, at least one of which is non-integral) to bring
them to their *composite pointer type*. If one operand is a null pointer
constant, the composite pointer type is `std::nullptr_t` if the other
operand is also a null pointer constant or, if the other operand is a
pointer, the type of the other operand. Otherwise, if one of the
operands has type “pointer to cv-qualifiercv1 `void`,” then the other
has type “pointer to cv-qualifiercv2 *T*” and the composite pointer type
is “pointer to cv-qualifiercv12 `void`,” where cv-qualifiercv12 is the
union of cv-qualifiercv1 and cv-qualifiercv2. Otherwise, the composite
pointer type is a pointer type similar ([[conv.qual]]) to the type of
one of the operands, with a cv-qualification signature ([[conv.qual]])
that is the union of the cv-qualification signatures of the operand
types. this implies that any pointer can be compared to a null pointer
constant and that any object pointer can be compared to a pointer to
(possibly cv-qualified) `void`.

``` cpp
void *p;
const int *q;
int **pi;
const int *const *pci;
void ct() {
  p <= q;           // Both converted to const void* before comparison
  pi <= pci;        // Both converted to const int *const * before comparison
}
```

Pointers to objects or functions of the same type (after pointer
conversions) can be compared, with a result defined as follows:

- If two pointers `p` and `q` of the same type point to the same object
  or function, or both point one past the end of the same array, or are
  both null, then `p<=q` and `p>=q` both yield `true` and `p<q` and
  `p>q` both yield `false`.
- If two pointers `p` and `q` of the same type point to different
  objects that are not members of the same object or elements of the
  same array or to different functions, or if only one of them is null,
  the results of `p<q`, `p>q`, `p<=q`, and `p>=q` are unspecified.
- If two pointers point to non-static data members of the same object,
  or to subobjects or array elements of such members, recursively, the
  pointer to the later declared member compares greater provided the two
  members have the same access control (Clause  [[class.access]]) and
  provided their class is not a union.
- If two pointers point to non-static data members of the same object
  with different access control (Clause  [[class.access]]) the result is
  unspecified.
- If two pointers point to non-static data members of the same union
  object, they compare equal (after conversion to `void*`, if
  necessary). If two pointers point to elements of the same array or one
  beyond the end of the array, the pointer to the object with the higher
  subscript compares higher.
- Other pointer comparisons are unspecified.

Pointers to `void` (after pointer conversions) can be compared, with a
result defined as follows: If both pointers represent the same address
or are both the null pointer value, the result is `true` if the operator
is `<=` or `>=` and `false` otherwise; otherwise the result is
unspecified.

If two operands of type `std::nullptr_t` are compared, the result is
`true` if the operator is `<=` or `>=`, and `false` otherwise.

If both operands (after conversions) are of arithmetic or enumeration
type, each of the operators shall yield `true` if the specified
relationship is true and `false` if it is false.

## Equality operators <a id="expr.eq">[[expr.eq]]</a>

``` bnf
equality-expression:
    relational-expression
    equality-expression '==' relational-expression
    equality-expression '!=' relational-expression
```

The `==` (equal to) and the `!=` (not equal to) operators have the same
semantic restrictions, conversions, and result type as the relational
operators except for their lower precedence and truth-value result.
`a<b == c<d` is `true` whenever `a<b` and `c<d` have the same
truth-value. Pointers of the same type (after pointer conversions) can
be compared for equality. Two pointers of the same type compare equal if
and only if they are both null, both point to the same function, or both
represent the same address ([[basic.compound]]).

In addition, pointers to members can be compared, or a pointer to member
and a null pointer constant. Pointer to member conversions (
[[conv.mem]]) and qualification conversions ([[conv.qual]]) are
performed to bring them to a common type. If one operand is a null
pointer constant, the common type is the type of the other operand.
Otherwise, the common type is a pointer to member type similar (
[[conv.qual]]) to the type of one of the operands, with a
cv-qualification signature ([[conv.qual]]) that is the union of the
cv-qualification signatures of the operand types. this implies that any
pointer to member can be compared to a null pointer constant. If both
operands are null, they compare equal. Otherwise if only one is null,
they compare unequal. Otherwise if either is a pointer to a virtual
member function, the result is unspecified. Otherwise they compare equal
if and only if they would refer to the same member of the same most
derived object ([[intro.object]]) or the same subobject if they were
dereferenced with a hypothetical object of the associated class type.

``` cpp
struct B {
  int f();
};
struct L : B { };
struct R : B { };
struct D : L, R { };

int (B::*pb)() = &B::f;
int (L::*pl)() = pb;
int (R::*pr)() = pb;
int (D::*pdl)() = pl;
int (D::*pdr)() = pr;
bool x = (pdl == pdr);          // false
```

If two operands of type `std::nullptr_t` are compared, the result is
`true` if the operator is `==`, and `false` otherwise.

Each of the operators shall yield `true` if the specified relationship
is true and `false` if it is false.

## Bitwise AND operator <a id="expr.bit.and">[[expr.bit.and]]</a>

``` bnf
and-expression:
    equality-expression
    and-expression '&' equality-expression
```

The usual arithmetic conversions are performed; the result is the
bitwise function of the operands. The operator applies only to integral
or unscoped enumeration operands.

## Bitwise exclusive OR operator <a id="expr.xor">[[expr.xor]]</a>

``` bnf
exclusive-or-expression:
    and-expression
    exclusive-or-expression '\^{}' and-expression
```

The usual arithmetic conversions are performed; the result is the
bitwise exclusive function of the operands. The operator applies only to
integral or unscoped enumeration operands.

## Bitwise inclusive OR operator <a id="expr.or">[[expr.or]]</a>

``` bnf
inclusive-or-expression:
    exclusive-or-expression
    inclusive-or-expression '|' exclusive-or-expression
```

The usual arithmetic conversions are performed; the result is the
bitwise inclusive function of its operands. The operator applies only to
integral or unscoped enumeration operands.

## Logical AND operator <a id="expr.log.and">[[expr.log.and]]</a>

``` bnf
logical-and-expression:
    inclusive-or-expression
    logical-and-expression '&&' inclusive-or-expression
```

The `&&` operator groups left-to-right. The operands are both
contextually converted to type `bool` (Clause  [[conv]]). The result is
`true` if both operands are `true` and `false` otherwise. Unlike `&`,
`&&` guarantees left-to-right evaluation: the second operand is not
evaluated if the first operand is `false`.

The result is a `bool`. If the second expression is evaluated, every
value computation and side effect associated with the first expression
is sequenced before every value computation and side effect associated
with the second expression.

## Logical OR operator <a id="expr.log.or">[[expr.log.or]]</a>

``` bnf
logical-or-expression:
    logical-and-expression
    logical-or-expression '$||$' logical-and-expression
```

The `||` operator groups left-to-right. The operands are both
contextually converted to `bool` (Clause  [[conv]]). It returns `true`
if either of its operands is `true`, and `false` otherwise. Unlike `|`,
`||` guarantees left-to-right evaluation; moreover, the second operand
is not evaluated if the first operand evaluates to `true`.

The result is a `bool`. If the second expression is evaluated, every
value computation and side effect associated with the first expression
is sequenced before every value computation and side effect associated
with the second expression.

## Conditional operator <a id="expr.cond">[[expr.cond]]</a>

``` bnf
conditional-expression:
    logical-or-expression
    logical-or-expression '?' expression ':' assignment-expression
```

Conditional expressions group right-to-left. The first expression is
contextually converted to `bool` (Clause  [[conv]]). It is evaluated and
if it is `true`, the result of the conditional expression is the value
of the second expression, otherwise that of the third expression. Only
one of the second and third expressions is evaluated. Every value
computation and side effect associated with the first expression is
sequenced before every value computation and side effect associated with
the second or third expression.

If either the second or the third operand has type `void`, then the
lvalue-to-rvalue ([[conv.lval]]), array-to-pointer ([[conv.array]]),
and function-to-pointer ([[conv.func]]) standard conversions are
performed on the second and third operands, and one of the following
shall hold:

- The second or the third operand (but not both) is a
  *throw-expression* ([[except.throw]]); the result is of the type of
  the other and is a prvalue.
- Both the second and the third operands have type `void`; the result is
  of type `void` and is a prvalue. This includes the case where both
  operands are *throw-expression*s.

Otherwise, if the second and third operand have different types and
either has (possibly cv-qualified) class type, or if both are glvalues
of the same value category and the same type except for
cv-qualification, an attempt is made to convert each of those operands
to the type of the other. The process for determining whether an operand
expression `E1` of type `T1` can be converted to match an operand
expression `E2` of type `T2` is defined as follows:

- If `E2` is an lvalue: `E1` can be converted to match `E2` if `E1` can
  be implicitly converted (Clause  [[conv]]) to the type “lvalue
  reference to `T2`”, subject to the constraint that in the conversion
  the reference must bind directly ([[dcl.init.ref]]) to an lvalue.
- If `E2` is an xvalue: `E1` can be converted to match `E2` if `E1` can
  be implicitly converted to the type “rvalue reference to `T2`”,
  subject to the constraint that the reference must bind directly.
- If `E2` is an rvalue or if neither of the conversions above can be
  done and at least one of the operands has (possibly cv-qualified)
  class type:
  - if `E1` and `E2` have class type, and the underlying class types are
    the same or one is a base class of the other: `E1` can be converted
    to match `E2` if the class of `T2` is the same type as, or a base
    class of, the class of `T1`, and the cv-qualification of `T2` is the
    same cv-qualification as, or a greater cv-qualification than, the
    cv-qualification of `T1`. If the conversion is applied, `E1` is
    changed to a prvalue of type `T2` by copy-initializing a temporary
    of type `T2` from `E1` and using that temporary as the converted
    operand.
  - Otherwise (i.e., if `E1` or `E2` has a nonclass type, or if they
    both have class types but the underlying classes are not either the
    same or one a base class of the other): `E1` can be converted to
    match `E2` if `E1` can be implicitly converted to the type that
    expression `E2` would have if `E2` were converted to a prvalue (or
    the type it has, if `E2` is a prvalue).

  Using this process, it is determined whether the second operand can be
  converted to match the third operand, and whether the third operand
  can be converted to match the second operand. If both can be
  converted, or one can be converted but the conversion is ambiguous,
  the program is ill-formed. If neither can be converted, the operands
  are left unchanged and further checking is performed as described
  below. If exactly one conversion is possible, that conversion is
  applied to the chosen operand and the converted operand is used in
  place of the original operand for the remainder of this section.

If the second and third operands are glvalues of the same value category
and have the same type, the result is of that type and value category
and it is a bit-field if the second or the third operand is a bit-field,
or if both are bit-fields.

Otherwise, the result is a prvalue. If the second and third operands do
not have the same type, and either has (possibly cv-qualified) class
type, overload resolution is used to determine the conversions (if any)
to be applied to the operands ([[over.match.oper]],  [[over.built]]).
If the overload resolution fails, the program is ill-formed. Otherwise,
the conversions thus determined are applied, and the converted operands
are used in place of the original operands for the remainder of this
section.

Lvalue-to-rvalue ([[conv.lval]]), array-to-pointer ([[conv.array]]),
and function-to-pointer ([[conv.func]]) standard conversions are
performed on the second and third operands. After those conversions, one
of the following shall hold:

- The second and third operands have the same type; the result is of
  that type. If the operands have class type, the result is a prvalue
  temporary of the result type, which is copy-initialized from either
  the second operand or the third operand depending on the value of the
  first operand.
- The second and third operands have arithmetic or enumeration type; the
  usual arithmetic conversions are performed to bring them to a common
  type, and the result is of that type.
- The second and third operands have pointer type, or one has pointer
  type and the other is a null pointer constant, or both are null
  pointer constants, at least one of which is non-integral; pointer
  conversions ([[conv.ptr]]) and qualification conversions (
  [[conv.qual]]) are performed to bring them to their composite pointer
  type ([[expr.rel]]). The result is of the composite pointer type.
- The second and third operands have pointer to member type, or one has
  pointer to member type and the other is a null pointer constant;
  pointer to member conversions ([[conv.mem]]) and qualification
  conversions ([[conv.qual]]) are performed to bring them to a common
  type, whose cv-qualification shall match the cv-qualification of
  either the second or the third operand. The result is of the common
  type.

## Assignment and compound assignment operators <a id="expr.ass">[[expr.ass]]</a>

The assignment operator (`=`) and the compound assignment operators all
group right-to-left. All require a modifiable lvalue as their left
operand and return an lvalue referring to the left operand. The result
in all cases is a bit-field if the left operand is a bit-field. In all
cases, the assignment is sequenced after the value computation of the
right and left operands, and before the value computation of the
assignment expression. With respect to an indeterminately-sequenced
function call, the operation of a compound assignment is a single
evaluation. Therefore, a function call shall not intervene between the
lvalue-to-rvalue conversion and the side effect associated with any
single compound assignment operator.

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

In simple assignment (`=`), the value of the expression replaces that of
the object referred to by the left operand.

If the left operand is not of class type, the expression is implicitly
converted (Clause  [[conv]]) to the cv-unqualified type of the left
operand.

If the left operand is of class type, the class shall be complete.
Assignment to objects of a class is defined by the copy/move assignment
operator ([[class.copy]],  [[over.ass]]).

For class objects, assignment is not in general the same as
initialization ([[dcl.init]],  [[class.ctor]],  [[class.init]], 
[[class.copy]]).

When the left operand of an assignment operator denotes a reference to
`T`, the operation assigns to the object of type `T` denoted by the
reference.

The behavior of an expression of the form `E1` *op*`=` `E2` is
equivalent to `E1 = E1` *op* `E2` except that `E1` is evaluated only
once. In `+=` and `-=`, `E1` shall either have arithmetic type or be a
pointer to a possibly cv-qualified completely-defined object type. In
all other cases, `E1` shall have arithmetic type.

If the value being stored in an object is accessed from another object
that overlaps in any way the storage of the first object, then the
overlap shall be exact and the two objects shall have the same type,
otherwise the behavior is undefined. This restriction applies to the
relationship between the left and right sides of the assignment
operation; it is not a statement about how the target of the assignment
may be aliased in general. See  [[basic.lval]].

A *braced-init-list* may appear on the right-hand side of

- an assignment to a scalar, in which case the initializer list shall
  have at most a single element. The meaning of `x={v}`, where `T` is
  the scalar type of the expression `x`, is that of `x=T(v)` except that
  no narrowing conversion ([[dcl.init.list]]) is allowed. The meaning
  of `x={}` is `x=T()`.
- an assignment defined by a user-defined assignment operator, in which
  case the initializer list is passed as the argument to the operator
  function.

``` cpp
complex<double> z;
z = { 1,2 };              // meaning z.operator=({1,2\)}
z += { 1, 2 };            // meaning z.operator+=({1,2\)}
int a, b;
a = b = { 1 };            // meaning a=b=1;
a = { 1 } = b;            // syntax error
```

## Comma operator <a id="expr.comma">[[expr.comma]]</a>

The comma operator groups left-to-right.

``` bnf
expression:
    assignment-expression
    expression ',' assignment-expression
```

A pair of expressions separated by a comma is evaluated left-to-right;
the left expression is a discarded-value expression (Clause 
[[expr]]).[^26] Every value computation and side effect associated with
the left expression is sequenced before every value computation and side
effect associated with the right expression. The type and value of the
result are the type and value of the right operand; the result is of the
same value category as its right operand, and is a bit-field if its
right operand is a glvalue and a bit-field.

In contexts where comma is given a special meaning, in lists of
arguments to functions ([[expr.call]]) and lists of initializers (
[[dcl.init]]) the comma operator as described in Clause  [[expr]] can
appear only in parentheses.

``` cpp
f(a, (t=3, t+2), c);
```

has three arguments, the second of which has the value `5`.

## Constant expressions <a id="expr.const">[[expr.const]]</a>

Certain contexts require expressions that satisfy additional
requirements as detailed in this sub-clause; other contexts have
different semantics depending on whether or not an expression satisfies
these requirements. Expressions that satisfy these requirements are
called *constant expressions*. Constant expressions can be evaluated
during translation.

``` bnf
constant-expression:
    conditional-expression
```

A *conditional-expression* is a *core constant expression* unless it
involves one of the following as a potentially evaluated subexpression (
[[basic.def.odr]]), but subexpressions of logical AND (
[[expr.log.and]]), logical OR ([[expr.log.or]]), and conditional (
[[expr.cond]]) operations that are not evaluated are not considered An
overloaded operator invokes a function.:

- `this` ([[expr.prim]]) unless it appears as the *postfix-expression*
  in a class member access expression, including the result of the
  implicit transformation in the body of a non-static member function (
  [[class.mfct.non-static]]);
- an invocation of a function other than a `constexpr` constructor for a
  literal class or a `constexpr` function Overload resolution (
  [[over.match]]) is applied as usual ;
- an invocation of an undefined `constexpr` function or an undefined
  `constexpr` constructor outside the definition of a `constexpr`
  function or a `constexpr` constructor;
- an invocation of a `constexpr` function with arguments that, when
  substituted by function invocation substitution ([[dcl.constexpr]]),
  do not produce a constant expression;
  ``` cpp
  constexpr const int* addr(const int& ir) { return &ir; }  // OK
  static const int x = 5;
  constexpr const int* xp = addr(x);  // OK: (const int*)&(const int&)x is an
                                      // address constant expression
  constexpr const int* tp = addr(5);  // error, initializer for constexpr variable not a constant
                                      // expression; (const int*)&(const int&)5 is not a constant
                                      // expression because it takes the address of a temporary
  ```
- an invocation of a `constexpr` constructor with arguments that, when
  substituted by function invocation substitution ([[dcl.constexpr]]),
  do not produce all constant expressions for the constructor calls and
  full-expressions in the *mem-initializer*s;
  ``` cpp
  int x;                              // not constant
  struct A {
    constexpr A(bool b) : m(b?42:x) { }
    int m;
  };
  constexpr int v = A(true).m;        // OK: constructor call initializes
                                      // m with the value 42 after substitution
  constexpr int w = A(false).m;       // error: initializer for m is
                                      // x, which is non-constant
  ```
- an invocation of a `constexpr` function or a `constexpr` constructor
  that would exceed the implementation-defined recursion limits (see
  Annex  [[implimits]]);
- a result that is not mathematically defined or not in the range of
  representable values for its type;
- a *lambda-expression* ([[expr.prim.lambda]]);
- an lvalue-to-rvalue conversion ([[conv.lval]]) unless it is applied
  to
  - a glvalue of integral or enumeration type that refers to a
    non-volatile const object with a preceding initialization,
    initialized with a constant expression, or
  - a glvalue of literal type that refers to a non-volatile object
    defined with `constexpr`, or that refers to a sub-object of such an
    object, or
  - a glvalue of literal type that refers to a non-volatile temporary
    object whose lifetime has not ended, initialized with a constant
    expression;
- an lvalue-to-rvalue conversion ([[conv.lval]]) that is applied to a
  glvalue that refers to a non-active member of a union or a subobject
  thereof;
- an *id-expression* that refers to a variable or data member of
  reference type unless the reference has a preceding initialization,
  initialized with a constant expression;
- a dynamic cast ([[expr.dynamic.cast]]);
- a `reinterpret_cast` ([[expr.reinterpret.cast]]);
- a pseudo-destructor call ([[expr.pseudo]]);
- increment or decrement operations ([[expr.post.incr]],
  [[expr.pre.incr]]);
- a typeid expression ([[expr.typeid]]) whose operand is of a
  polymorphic class type;
- a *new-expression* ([[expr.new]]);
- a *delete-expression* ([[expr.delete]]);
- a subtraction ([[expr.add]]) where both operands are pointers;
- a relational ([[expr.rel]]) or equality ([[expr.eq]]) operator where
  the result is unspecified;
- an assignment or a compound assignment ([[expr.ass]]); or
- a *throw-expression* ([[except.throw]]).

A *literal constant expression* is a prvalue core constant expression of
literal type, but not pointer type. An *integral constant expression* is
a literal constant expression of integral or unscoped enumeration type.
Such expressions may be used as array bounds ([[dcl.array]],
[[expr.new]]), as bit-field lengths ([[class.bit]]), as enumerator
initializers if the underlying type is not fixed ([[dcl.enum]]), as
null pointer constants ([[conv.ptr]]), and as alignments (
[[dcl.align]]). A *converted constant expression* of type `T` is a
literal constant expression, implicitly converted to type `T`, where the
implicit conversion (if any) is permitted in a literal constant
expression and the implicit conversion sequence contains only
user-defined conversions, lvalue-to-rvalue conversions ([[conv.lval]]),
integral promotions ([[conv.prom]]), and integral conversions (
[[conv.integral]]) other than narrowing conversions (
[[dcl.init.list]]). such expressions may be used as case expressions (
[[stmt.switch]]), as enumerator initializers if the underlying type is
fixed ([[dcl.enum]]), and as integral or enumeration non-type template
arguments ([[temp.arg]]). A *reference constant expression* is an
lvalue core constant expression that designates an object with static
storage duration or a function. An *address constant expression* is a
prvalue core constant expression of pointer type that evaluates to the
address of an object with static storage duration, to the address of a
function, or to a null pointer value, or a prvalue core constant
expression of type `std::nullptr_t`. Collectively, literal constant
expressions, reference constant expressions, and address constant
expressions are called *constant expressions*.

Although in some contexts constant expressions must be evaluated during
program translation, others may be evaluated during program execution.
Since this International Standard imposes no restrictions on the
accuracy of floating-point operations, it is unspecified whether the
evaluation of a floating-point expression during translation yields the
same result as the evaluation of the same expression (or the same
operations on the same values) during program execution.[^27]

``` cpp
bool f() {
    char array[1 + int(1 + 0.2 - 0.1 - 0.1)];  // Must be evaluated during translation
    int size = 1 + int(1 + 0.2 - 0.1 - 0.1);   // May be evaluated at runtime
    return sizeof(array) == size;
}
```

It is unspecified whether the value of `f()` will be `true` or `false`.

If an expression of literal class type is used in a context where an
integral constant expression is required, then that class type shall
have a single non-explicit conversion function to an integral or
unscoped enumeration type and that conversion function shall be
`constexpr`.

``` cpp
struct A {
  constexpr A(int i) : val(i) { }
  constexpr operator int() { return val; }
  constexpr operator long() { return 43; }
private:
  int val;
};
template<int> struct X { };
constexpr A a = 42;
X<a> x;             // OK: unique conversion to int
int ary[a];         // error: ambiguous conversion
```

<!-- Link reference definitions -->
[bad.alloc]: language.md#bad.alloc
[bad.cast]: language.md#bad.cast
[bad.typeid]: language.md#bad.typeid
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.classref]: basic.md#basic.lookup.classref
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.lval]: basic.md#basic.lval
[basic.namespace]: dcl.md#basic.namespace
[basic.scope.class]: basic.md#basic.scope.class
[basic.scope.local]: basic.md#basic.scope.local
[basic.start.main]: basic.md#basic.start.main
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[class]: class.md#class
[class.abstract]: class.md#class.abstract
[class.access]: class.md#class.access
[class.access.base]: class.md#class.access.base
[class.base.init]: special.md#class.base.init
[class.bit]: class.md#class.bit
[class.cdtor]: special.md#class.cdtor
[class.conv]: special.md#class.conv
[class.conv.fct]: special.md#class.conv.fct
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.derived]: class.md#class.derived
[class.dtor]: special.md#class.dtor
[class.free]: special.md#class.free
[class.init]: special.md#class.init
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.mfct.non-static]: class.md#class.mfct.non-static
[class.name]: class.md#class.name
[class.qual]: basic.md#class.qual
[class.static]: class.md#class.static
[class.temporary]: special.md#class.temporary
[class.this]: class.md#class.this
[class.virtual]: class.md#class.virtual
[conv]: conv.md#conv
[conv.array]: conv.md#conv.array
[conv.bool]: conv.md#conv.bool
[conv.fpint]: conv.md#conv.fpint
[conv.fpprom]: conv.md#conv.fpprom
[conv.func]: conv.md#conv.func
[conv.integral]: conv.md#conv.integral
[conv.lval]: conv.md#conv.lval
[conv.mem]: conv.md#conv.mem
[conv.prom]: conv.md#conv.prom
[conv.ptr]: conv.md#conv.ptr
[conv.qual]: conv.md#conv.qual
[dcl.align]: dcl.md#dcl.align
[dcl.array]: dcl.md#dcl.array
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.link]: dcl.md#dcl.link
[dcl.name]: dcl.md#dcl.name
[dcl.ref]: dcl.md#dcl.ref
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.stc]: dcl.md#dcl.stc
[dcl.type]: dcl.md#dcl.type
[dcl.type.cv]: dcl.md#dcl.type.cv
[dcl.type.simple]: dcl.md#dcl.type.simple
[depr]: #depr
[except]: except.md#except
[except.handle]: except.md#except.handle
[except.spec]: except.md#except.spec
[except.throw]: except.md#except.throw
[expr]: #expr
[expr.add]: #expr.add
[expr.alignof]: #expr.alignof
[expr.ass]: #expr.ass
[expr.bit.and]: #expr.bit.and
[expr.call]: #expr.call
[expr.cast]: #expr.cast
[expr.comma]: #expr.comma
[expr.cond]: #expr.cond
[expr.const]: #expr.const
[expr.const.cast]: #expr.const.cast
[expr.delete]: #expr.delete
[expr.dynamic.cast]: #expr.dynamic.cast
[expr.eq]: #expr.eq
[expr.log.and]: #expr.log.and
[expr.log.or]: #expr.log.or
[expr.mptr.oper]: #expr.mptr.oper
[expr.mul]: #expr.mul
[expr.new]: #expr.new
[expr.or]: #expr.or
[expr.post]: #expr.post
[expr.post.incr]: #expr.post.incr
[expr.pre.incr]: #expr.pre.incr
[expr.prim]: #expr.prim
[expr.prim.general]: #expr.prim.general
[expr.prim.lambda]: #expr.prim.lambda
[expr.pseudo]: #expr.pseudo
[expr.ref]: #expr.ref
[expr.reinterpret.cast]: #expr.reinterpret.cast
[expr.rel]: #expr.rel
[expr.shift]: #expr.shift
[expr.sizeof]: #expr.sizeof
[expr.static.cast]: #expr.static.cast
[expr.sub]: #expr.sub
[expr.type.conv]: #expr.type.conv
[expr.typeid]: #expr.typeid
[expr.unary]: #expr.unary
[expr.unary.noexcept]: #expr.unary.noexcept
[expr.unary.op]: #expr.unary.op
[expr.xor]: #expr.xor
[function.objects]: utilities.md#function.objects
[implimits]: #implimits
[intro.execution]: intro.md#intro.execution
[intro.memory]: intro.md#intro.memory
[intro.object]: intro.md#intro.object
[lex.literal]: lex.md#lex.literal
[lex.string]: lex.md#lex.string
[namespace.qual]: basic.md#namespace.qual
[new.badlength]: language.md#new.badlength
[new.delete.array]: language.md#new.delete.array
[new.delete.single]: language.md#new.delete.single
[over]: over.md#over
[over.ass]: over.md#over.ass
[over.built]: over.md#over.built
[over.call]: over.md#over.call
[over.literal]: over.md#over.literal
[over.match]: over.md#over.match
[over.match.oper]: over.md#over.match.oper
[over.oper]: over.md#over.oper
[over.over]: over.md#over.over
[replacement.functions]: library.md#replacement.functions
[stmt.switch]: stmt.md#stmt.switch
[support.runtime]: language.md#support.runtime
[support.types]: language.md#support.types
[temp.arg]: temp.md#temp.arg
[temp.names]: temp.md#temp.names
[temp.res]: temp.md#temp.res
[temp.variadic]: temp.md#temp.variadic
[type.info]: language.md#type.info

[^1]: The precedence of operators is not directly specified, but it can
    be derived from the syntax.

[^2]: As a consequence, operands of type `bool`, `char16_t`, `char32_t`,
    `wchar_t`, or an enumerated type are converted to some integral
    type.

[^3]: The cast and assignment operators must still perform their
    specific conversions as described in  [[expr.cast]], 
    [[expr.static.cast]] and  [[expr.ass]].

[^4]: This also applies when the object expression is an implicit
    `(*this)` ([[class.mfct.non-static]]).

[^5]: This is true even if the subscript operator is used in the
    following common idiom: `&x[0]`.

[^6]: A static member function ([[class.static]]) is an ordinary
    function.

[^7]: If the class member access expression is evaluated, the
    subexpression evaluation happens even if the result is unnecessary
    to determine the value of the entire postfix expression, for example
    if the *id-expression* denotes a static member.

[^8]: Note that `(*(E1))` is an lvalue.

[^9]: The most derived object ([[intro.object]]) pointed or referred to
    by `v` can contain other `B` objects as base classes, but these are
    ignored.

[^10]: The recommended name for such a class is `extended_type_info`.

[^11]: If `p` is an expression of pointer type, then `*p`, `(*p)`,
    `*(p)`, `((*p))`, `*((p))`, and so on all meet this requirement.

[^12]: Function types (including those used in pointer to member
    function types) are never cv-qualified; see  [[dcl.fct]].

[^13]: The types may have different cv-qualifiers, subject to the
    overall restriction that a `reinterpret_cast` cannot cast away
    constness.

[^14]: `T1` and `T2` may have different cv-qualifiers, subject to the
    overall restriction that a `reinterpret_cast` cannot cast away
    constness.

[^15]: This is sometimes referred to as a *type pun*.

[^16]: `const_cast`

    is not limited to conversions that cast away a const-qualifier.

[^17]: `sizeof(bool)` is not required to be `1`.

[^18]: The actual size of a base class subobject may be less than the
    result of applying `sizeof` to the subobject, due to virtual base
    classes and less strict padding requirements on base class
    subobjects.

[^19]: This may include evaluating a *new-initializer* and/or calling a
    constructor.

[^20]: A lambda expression with a *lambda-introducer* that consists of
    empty square brackets can follow the `delete` keyword if the lambda
    expression is enclosed in parentheses.

[^21]: This implies that an object cannot be deleted using a pointer of
    type `void*` because `void` is not an object type.

[^22]: For non-zero-length arrays, this is the same as a pointer to the
    first element of the array created by that *new-expression*.
    Zero-length arrays do not have a first element.

[^23]: This includes implicit calls such as the call to an allocation
    function in a *new-expression*.

[^24]: This is often called truncation towards zero.

[^25]: Another way to approach pointer arithmetic is first to convert
    the pointer(s) to character pointer(s): In this scheme the integral
    value of the expression added to or subtracted from the converted
    pointer is first multiplied by the size of the object originally
    pointed to, and the resulting pointer is converted back to the
    original type. For pointer subtraction, the result of the difference
    between the character pointers is similarly divided by the size of
    the object originally pointed to.

    When viewed in this way, an implementation need only provide one
    extra byte (which might overlap another object in the program) just
    after the end of the object in order to satisfy the “one past the
    last element” requirements.

[^26]: However, an invocation of an overloaded comma operator is an
    ordinary function call; hence, the evaluations of its argument
    expressions are unsequenced relative to one another (see
    [[intro.execution]]).

[^27]: Nonetheless, implementations are encouraged to provide consistent
    results, irrespective of whether the evaluation was actually
    performed during translation or during program execution.
