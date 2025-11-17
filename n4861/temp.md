# Templates <a id="temp">[[temp]]</a>

## Preamble <a id="temp.pre">[[temp.pre]]</a>

A *template* defines a family of classes, functions, or variables, an
alias for a family of types, or a concept.

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

[*Note 1*: The `>` token following the *template-parameter-list* of a
*template-declaration* may be the product of replacing a `>{>}` token by
two consecutive `>` tokens [[temp.names]]. — *end note*]

The *declaration* in a *template-declaration* (if any) shall

- declare or define a function, a class, or a variable, or
- define a member function, a member class, a member enumeration, or a
  static data member of a class template or of a class nested within a
  class template, or
- define a member template of a class or class template, or
- be a *deduction-guide*, or
- be an *alias-declaration*.

A *template-declaration* is a *declaration*. A declaration introduced by
a template declaration of a variable is a *variable template*. A
variable template at class scope is a *static data member template*.

[*Example 1*:

``` cpp
template<class T>
  constexpr T pi = T(3.1415926535897932385L);
template<class T>
  T circular_area(T r) {
    return pi<T> * r * r;
  }
struct matrix_constants {
  template<class T>
    using pauli = hermitian_matrix<T, 2>;
  template<class T>
    constexpr static pauli<T> sigma1 = { { 0, 1 }, { 1, 0 } };
  template<class T>
    constexpr static pauli<T> sigma2 = { { 0, -1i }, { 1i, 0 } };
  template<class T>
    constexpr static pauli<T> sigma3 = { { 1, 0 }, { 0, -1 } };
};
```

— *end example*]

A *template-declaration* can appear only as a namespace scope or class
scope declaration. Its *declaration* shall not be an
*export-declaration*. In a function template declaration, the last
component of the *declarator-id* shall not be a *template-id*.

[*Note 2*: That last component may be an *identifier*, an
*operator-function-id*, a *conversion-function-id*, or a
*literal-operator-id*. In a class template declaration, if the class
name is a *simple-template-id*, the declaration declares a class
template partial specialization [[temp.class.spec]]. — *end note*]

In a *template-declaration*, explicit specialization, or explicit
instantiation the *init-declarator-list* in the declaration shall
contain at most one declarator. When such a declaration is used to
declare a class template, no declarator is permitted.

A template name has linkage [[basic.link]]. Specializations (explicit or
implicit) of a template that has internal linkage are distinct from all
specializations in other translation units. A template, a template
explicit specialization [[temp.expl.spec]], and a class template partial
specialization shall not have C linkage. Use of a linkage specification
other than `"C"` or `"C++"` with any of these constructs is
conditionally-supported, with *implementation-defined* semantics.
Template definitions shall obey the one-definition rule
[[basic.def.odr]].

[*Note 3*: Default arguments for function templates and for member
functions of class templates are considered definitions for the purpose
of template instantiation [[temp.decls]] and must also obey the
one-definition rule. — *end note*]

A class template shall not have the same name as any other template,
class, function, variable, enumeration, enumerator, namespace, or type
in the same scope [[basic.scope]], except as specified in 
[[temp.class.spec]]. Except that a function template can be overloaded
either by non-template functions [[dcl.fct]] with the same name or by
other function templates with the same name [[temp.over]], a template
name declared in namespace scope or in class scope shall be unique in
that scope.

An entity is *templated* if it is

- a template,
- an entity defined [[basic.def]] or created [[class.temporary]] in a
  templated entity,
- a member of a templated entity,
- an enumerator for an enumeration that is a templated entity, or
- the closure type of a *lambda-expression* [[expr.prim.lambda.closure]]
  appearing in the declaration of a templated entity.

[*Note 4*: A local class, a local variable, or a friend function
defined in a templated entity is a templated entity. — *end note*]

A *template-declaration* is written in terms of its template parameters.
The optional *requires-clause* following a *template-parameter-list*
allows the specification of constraints [[temp.constr.decl]] on template
arguments [[temp.arg]]. The *requires-clause* introduces the
*constraint-expression* that results from interpreting the
*constraint-logical-or-expression* as a *constraint-expression*. The
*constraint-logical-or-expression* of a *requires-clause* is an
unevaluated operand [[expr.context]].

[*Note 5*:

The expression in a *requires-clause* uses a restricted grammar to avoid
ambiguities. Parentheses can be used to specify arbitrary expressions in
a *requires-clause*.

[*Example 2*:

``` cpp
template<int N> requires N == sizeof new unsigned short
int f();            // error: parentheses required around == expression
```

— *end example*]

— *end note*]

A definition of a function template, member function of a class
template, variable template, or static data member of a class template
shall be reachable from the end of every definition domain
[[basic.def.odr]] in which it is implicitly instantiated [[temp.inst]]
unless the corresponding specialization is explicitly instantiated
[[temp.explicit]] in some translation unit; no diagnostic is required.

## Template parameters <a id="temp.param">[[temp.param]]</a>

The syntax for *template-parameter*s is:

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

[*Note 1*: The `>` token following the *template-parameter-list* of a
*type-parameter* may be the product of replacing a `>{>}` token by two
consecutive `>` tokens [[temp.names]]. — *end note*]

There is no semantic difference between `class` and `typename` in a
*type-parameter-key*. `typename` followed by an *unqualified-id* names a
template type parameter. `typename` followed by a *qualified-id* denotes
the type in a non-type [^1] *parameter-declaration*. A
*template-parameter* of the form `class` *identifier* is a
*type-parameter*.

[*Example 1*:

``` cpp
class T { ... };
int i;

template<class T, T i> void f(T t) {
  T t1 = i;         // template-parameters T and i
  ::T t2 = ::i;     // global namespace members T and i
}
```

Here, the template `f` has a *type-parameter* called `T`, rather than an
unnamed non-type *template-parameter* of class `T`.

— *end example*]

A storage class shall not be specified in a *template-parameter*
declaration. Types shall not be defined in a *template-parameter*
declaration.

A *type-parameter* whose identifier does not follow an ellipsis defines
its *identifier* to be a *typedef-name* (if declared without `template`)
or *template-name* (if declared with `template`) in the scope of the
template declaration.

[*Note 2*:

A template argument may be a class template or alias template. For
example,

``` cpp
template<class T> class myarray { ... };

template<class K, class V, template<class T> class C = myarray>
class Map {
  C<K> key;
  C<V> value;
};
```

— *end note*]

A *type-constraint* `Q` that designates a concept `C` can be used to
constrain a contextually-determined type or template type parameter pack
`T` with a *constraint-expression* `E` defined as follows. If `Q` is of
the form `C<A_1, \cdots, A_n>`, then let `E'` be
`C<T, A_1, \cdots, A_n>`. Otherwise, let `E'` be `C<T>`. If `T` is not a
pack, then `E` is `E'`, otherwise `E` is `(E' && ...)`. This
*constraint-expression* `E` is called the *immediately-declared
constraint* of `Q` for `T`. The concept designated by a
*type-constraint* shall be a type concept [[temp.concept]].

A *type-parameter* that starts with a *type-constraint* introduces the
immediately-declared constraint of the *type-constraint* for the
parameter.

[*Example 2*:

``` cpp
template<typename T> concept C1 = true;
template<typename... Ts> concept C2 = true;
template<typename T, typename U> concept C3 = true;

template<C1 T> struct s1;               // associates C1<T>
template<C1... T> struct s2;            // associates (C1<T> && ...)
template<C2... T> struct s3;            // associates (C2<T> && ...)
template<C3<int> T> struct s4;          // associates C3<T, int>
template<C3<int>... T> struct s5;       // associates (C3<T, int> && ...)
```

— *end example*]

A non-type *template-parameter* shall have one of the following
(possibly cv-qualified) types:

- a structural type (see below),
- a type that contains a placeholder type [[dcl.spec.auto]], or
- a placeholder for a deduced class type [[dcl.type.class.deduct]].

The top-level *cv-qualifier*s on the *template-parameter* are ignored
when determining its type.

A *structural type* is one of the following:

- a scalar type, or
- an lvalue reference type, or
- a literal class type with the following properties:
  - all base classes and non-static data members are public and
    non-mutable and
  - the types of all bases classes and non-static data members are
    structural types or (possibly multi-dimensional) array thereof.

An *id-expression* naming a non-type *template-parameter* of class type
`T` denotes a static storage duration object of type `const T`, known as
a *template parameter object*, whose value is that of the corresponding
template argument after it has been converted to the type of the
*template-parameter*. All such template parameters in the program of the
same type with the same value denote the same template parameter object.
A template parameter object shall have constant destruction
[[expr.const]].

[*Note 3*: If an *id-expression* names a non-type non-reference
*template-parameter*, then it is a prvalue if it has non-class type.
Otherwise, if it is of class type `T`, it is an lvalue and has type
`const T` [[expr.prim.id.unqual]]. — *end note*]

[*Example 3*:

``` cpp
using X = int;
struct A {};
template<const X& x, int i, A a> void f() {
  i++;                          // error: change of template-parameter value

  &x;                           // OK
  &i;                           // error: address of non-reference template-parameter
  &a;                           // OK
  int& ri = i;                  // error: non-const reference bound to temporary
  const int& cri = i;           // OK: const reference bound to temporary
  const A& ra = a;              // OK: const reference bound to a template parameter object
}
```

— *end example*]

[*Note 4*:

A non-type *template-parameter* cannot be declared to have type cv
`void`.

[*Example 4*:

``` cpp
template<void v> class X;       // error
template<void* pv> class Y;     // OK
```

— *end example*]

— *end note*]

A non-type *template-parameter* of type “array of `T`” or of function
type `T` is adjusted to be of type “pointer to `T`”.

[*Example 5*:

``` cpp
template<int* a>   struct R { ... };
template<int b[5]> struct S { ... };
int p;
R<&p> w;                        // OK
S<&p> x;                        // OK due to parameter adjustment
int v[5];
R<v> y;                         // OK due to implicit argument conversion
S<v> z;                         // OK due to both adjustment and conversion
```

— *end example*]

A non-type template parameter declared with a type that contains a
placeholder type with a *type-constraint* introduces the
immediately-declared constraint of the *type-constraint* for the
invented type corresponding to the placeholder [[dcl.fct]].

A *default template-argument* is a *template-argument* [[temp.arg]]
specified after `=` in a *template-parameter*. A default
*template-argument* may be specified for any kind of
*template-parameter* (type, non-type, template) that is not a template
parameter pack [[temp.variadic]]. A default *template-argument* may be
specified in a template declaration. A default *template-argument* shall
not be specified in the *template-parameter-list*s of the definition of
a member of a class template that appears outside of the member’s class.
A default *template-argument* shall not be specified in a friend class
template declaration. If a friend function template declaration
specifies a default *template-argument*, that declaration shall be a
definition and shall be the only declaration of the function template in
the translation unit.

The set of default *template-argument*s available for use is obtained by
merging the default arguments from all prior declarations of the
template in the same way default function arguments are
[[dcl.fct.default]].

[*Example 6*:

``` cpp
template<class T1, class T2 = int> class A;
template<class T1 = int, class T2> class A;
```

is equivalent to

``` cpp
template<class T1 = int, class T2 = int> class A;
```

— *end example*]

If a *template-parameter* of a class template, variable template, or
alias template has a default *template-argument*, each subsequent
*template-parameter* shall either have a default *template-argument*
supplied or be a template parameter pack. If a *template-parameter* of a
primary class template, primary variable template, or alias template is
a template parameter pack, it shall be the last *template-parameter*. A
template parameter pack of a function template shall not be followed by
another template parameter unless that template parameter can be deduced
from the parameter-type-list [[dcl.fct]] of the function template or has
a default argument [[temp.deduct]]. A template parameter of a deduction
guide template [[temp.deduct.guide]] that does not have a default
argument shall be deducible from the parameter-type-list of the
deduction guide template.

[*Example 7*:

``` cpp
template<class T1 = int, class T2> class B;     // error

// U can be neither deduced from the parameter-type-list nor specified
template<class... T, class... U> void f() { }   // error
template<class... T, class U> void g() { }      // error
```

— *end example*]

A *template-parameter* shall not be given default arguments by two
different declarations in the same scope.

[*Example 8*:

``` cpp
template<class T = int> class X;
template<class T = int> class X { ... };  // error
```

— *end example*]

When parsing a default *template-argument* for a non-type
*template-parameter*, the first non-nested `>` is taken as the end of
the *template-parameter-list* rather than a greater-than operator.

[*Example 9*:

``` cpp
template<int i = 3 > 4 >        // syntax error
class X { ... };

template<int i = (3 > 4) >      // OK
class Y { ... };
```

— *end example*]

A *template-parameter* of a template *template-parameter* is permitted
to have a default *template-argument*. When such default arguments are
specified, they apply to the template *template-parameter* in the scope
of the template *template-parameter*.

[*Example 10*:

``` cpp
template <template <class TT = float> class T> struct A {
  inline void f();
  inline void g();
};
template <template <class TT> class T> void A<T>::f() {
  T<> t;            // error: TT has no default template argument
}
template <template <class TT = char> class T> void A<T>::g() {
  T<> t;            // OK, T<char>
}
```

— *end example*]

If a *template-parameter* is a *type-parameter* with an ellipsis prior
to its optional *identifier* or is a *parameter-declaration* that
declares a pack [[dcl.fct]], then the *template-parameter* is a template
parameter pack [[temp.variadic]]. A template parameter pack that is a
*parameter-declaration* whose type contains one or more unexpanded packs
is a pack expansion. Similarly, a template parameter pack that is a
*type-parameter* with a *template-parameter-list* containing one or more
unexpanded packs is a pack expansion. A type parameter pack with a
*type-constraint* that contains an unexpanded parameter pack is a pack
expansion. A template parameter pack that is a pack expansion shall not
expand a template parameter pack declared in the same
*template-parameter-list*.

[*Example 11*:

``` cpp
template <class... Types>                       // Types is a template type parameter pack
   class Tuple;                                 // but not a pack expansion

template <class T, int... Dims>                 // Dims is a non-type template parameter pack
   struct multi_array;                          // but not a pack expansion

template <class... T>
  struct value_holder {
    template <T... Values> struct apply { };    // Values is a non-type template parameter pack
  };                                            // and a pack expansion

template <class... T, T... Values>              // error: Values expands template type parameter
  struct static_array;                          // pack T within the same template parameter list
```

— *end example*]

## Names of template specializations <a id="temp.names">[[temp.names]]</a>

A template specialization [[temp.spec]] can be referred to by a
*template-id*:

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

[*Note 1*: The name lookup rules [[basic.lookup]] are used to associate
the use of a name with a template declaration; that is, to identify a
name as a *template-name*. — *end note*]

For a *template-name* to be explicitly qualified by the template
arguments, the name must be considered to refer to a template.

[*Note 2*: Whether a name actually refers to a template cannot be known
in some cases until after argument dependent lookup is done
[[basic.lookup.argdep]]. — *end note*]

A name is considered to refer to a template if name lookup finds a
*template-name* or an overload set that contains a function template. A
name is also considered to refer to a template if it is an
*unqualified-id* followed by a `<` and name lookup either finds one or
more functions or finds nothing.

When a name is considered to be a *template-name*, and it is followed by
a `<`, the `<` is always taken as the delimiter of a
*template-argument-list* and never as the less-than operator. When
parsing a *template-argument-list*, the first non-nested `>`[^2] is
taken as the ending delimiter rather than a greater-than operator.
Similarly, the first non-nested `>{>}` is treated as two consecutive but
distinct `>` tokens, the first of which is taken as the end of the
*template-argument-list* and completes the *template-id*.

[*Note 3*: The second `>` token produced by this replacement rule may
terminate an enclosing *template-id* construct or it may be part of a
different construct (e.g., a cast). — *end note*]

[*Example 1*:

``` cpp
template<int i> class X { ... };

X< 1>2 > x1;                            // syntax error
X<(1>2)> x2;                            // OK

template<class T> class Y { ... };
Y<X<1>> x3;                             // OK, same as Y<X<1> > x3;
Y<X<6>>1>> x4;                          // syntax error
Y<X<(6>>1)>> x5;                        // OK
```

— *end example*]

The keyword `template` is said to appear at the top level in a
*qualified-id* if it appears outside of a *template-argument-list* or
*decltype-specifier*. In a *qualified-id* of a *declarator-id* or in a
*qualified-id* formed by a *class-head-name* [[class.pre]] or
*enum-head-name* [[dcl.enum]], the keyword `template` shall not appear
at the top level. In a *qualified-id* used as the name in a
*typename-specifier* [[temp.res]], *elaborated-type-specifier*
[[dcl.type.elab]], *using-declaration* [[namespace.udecl]], or
*class-or-decltype* [[class.derived]], an optional keyword `template`
appearing at the top level is ignored. In these contexts, a `<` token is
always assumed to introduce a *template-argument-list*. In all other
contexts, when naming a template specialization of a member of an
unknown specialization [[temp.dep.type]], the member template name shall
be prefixed by the keyword `template`.

[*Example 2*:

``` cpp
struct X {
  template<std::size_t> X* alloc();
  template<std::size_t> static X* adjust();
};
template<class T> void f(T* p) {
  T* p1 = p->alloc<200>();              // error: < means less than
  T* p2 = p->template alloc<200>();     // OK: < starts template argument list
  T::adjust<100>();                     // error: < means less than
  T::template adjust<100>();            // OK: < starts template argument list
}
```

— *end example*]

A name prefixed by the keyword `template` shall be a *template-id* or
the name shall refer to a class template or an alias template.

[*Note 4*: The keyword `template` may not be applied to non-template
members of class templates. — *end note*]

[*Note 5*: As is the case with the `typename` prefix, the `template`
prefix is allowed in cases where it is not strictly necessary; i.e.,
when the *nested-name-specifier* or the expression on the left of the
`->` or `.` is not dependent on a *template-parameter*, or the use does
not appear in the scope of a template. — *end note*]

[*Example 3*:

``` cpp
template <class T> struct A {
  void f(int);
  template <class U> void f(U);
};

template <class T> void f(T t) {
  A<T> a;
  a.template f<>(t);                    // OK: calls template
  a.template f(t);                      // error: not a template-id
}

template <class T> struct B {
  template <class T2> struct C { };
};

// OK: T::template C names a class template:
template <class T, template <class X> class TT = T::template C> struct D { };
D<B<int> > db;
```

— *end example*]

A *template-id* is *valid* if

- there are at most as many arguments as there are parameters or a
  parameter is a template parameter pack [[temp.variadic]],
- there is an argument for each non-deducible non-pack parameter that
  does not have a default *template-argument*,
- each *template-argument* matches the corresponding
  *template-parameter* [[temp.arg]],
- substitution of each template argument into the following template
  parameters (if any) succeeds, and
- if the *template-id* is non-dependent, the associated constraints are
  satisfied as specified in the next paragraph.

A *simple-template-id* shall be valid unless it names a function
template specialization [[temp.deduct]].

[*Example 4*:

``` cpp
template<class T, T::type n = 0> class X;
struct S {
  using type = int;
};
using T1 = X<S, int, int>;      // error: too many arguments
using T2 = X<>;                 // error: no default argument for first template parameter
using T3 = X<1>;                // error: value 1 does not match type-parameter
using T4 = X<int>;              // error: substitution failure for second template parameter
using T5 = X<S>;                // OK
```

— *end example*]

When the *template-name* of a *simple-template-id* names a constrained
non-function template or a constrained template *template-parameter*,
but not a member template that is a member of an unknown specialization
[[temp.res]], and all *template-argument*s in the *simple-template-id*
are non-dependent [[temp.dep.temp]], the associated constraints
[[temp.constr.decl]] of the constrained template shall be satisfied
[[temp.constr.constr]].

[*Example 5*:

``` cpp
template<typename T> concept C1 = sizeof(T) != sizeof(int);

template<C1 T> struct S1 { };
template<C1 T> using Ptr = T*;

S1<int>* p;                         // error: constraints not satisfied
Ptr<int> p;                         // error: constraints not satisfied

template<typename T>
struct S2 { Ptr<int> x; };          // ill-formed, no diagnostic required

template<typename T>
struct S3 { Ptr<T> x; };            // OK, satisfaction is not required

S3<int> x;                          // error: constraints not satisfied

template<template<C1 T> class X>
struct S4 {
  X<int> x;                         // ill-formed, no diagnostic required
};

template<typename T> concept C2 = sizeof(T) == 1;

template<C2 T> struct S { };

template struct S<char[2]>;         // error: constraints not satisfied
template<> struct S<char[2]> { };   // error: constraints not satisfied
```

— *end example*]

A *concept-id* is a *simple-template-id* where the *template-name* is a
*concept-name*. A concept-id is a prvalue of type `bool`, and does not
name a template specialization. A concept-id evaluates to `true` if the
concept’s normalized *constraint-expression* [[temp.constr.decl]] is
satisfied [[temp.constr.constr]] by the specified template arguments and
`false` otherwise.

[*Note 6*: Since a *constraint-expression* is an unevaluated operand, a
concept-id appearing in a *constraint-expression* is not evaluated
except as necessary to determine whether the normalized constraints are
satisfied. — *end note*]

[*Example 6*:

``` cpp
template<typename T> concept C = true;
static_assert(C<int>);      // OK
```

— *end example*]

## Template arguments <a id="temp.arg">[[temp.arg]]</a>

There are three forms of *template-argument*, corresponding to the three
forms of *template-parameter*: type, non-type and template. The type and
form of each *template-argument* specified in a *template-id* shall
match the type and form specified for the corresponding parameter
declared by the template in its *template-parameter-list*. When the
parameter declared by the template is a template parameter pack
[[temp.variadic]], it will correspond to zero or more
*template-argument*s.

[*Example 1*:

``` cpp
template<class T> class Array {
  T* v;
  int sz;
public:
  explicit Array(int);
  T& operator[](int);
  T& elem(int i) { return v[i]; }
};

Array<int> v1(20);
typedef std::complex<double> dcomplex;  // std::complex is a standard library template
Array<dcomplex> v2(30);
Array<dcomplex> v3(40);

void bar() {
  v1[3] = 7;
  v2[3] = v3.elem(4) = dcomplex(7,8);
}
```

— *end example*]

In a *template-argument*, an ambiguity between a *type-id* and an
expression is resolved to a *type-id*, regardless of the form of the
corresponding *template-parameter*.[^3]

[*Example 2*:

``` cpp
template<class T> void f();
template<int I> void f();

void g() {
  f<int()>();       // int() is a type-id: call the first f()
}
```

— *end example*]

The name of a *template-argument* shall be accessible at the point where
it is used as a *template-argument*.

[*Note 1*: If the name of the *template-argument* is accessible at the
point where it is used as a *template-argument*, there is no further
access restriction in the resulting instantiation where the
corresponding *template-parameter* name is used. — *end note*]

[*Example 3*:

``` cpp
template<class T> class X {
  static T t;
};

class Y {
private:
  struct S { ... };
  X<S> x;           // OK: S is accessible
                    // X<Y::S> has a static member of type Y::S
                    // OK: even though Y::S is private
};

X<Y::S> y;          // error: S not accessible
```

— *end example*]

For a *template-argument* that is a class type or a class template, the
template definition has no special access rights to the members of the
*template-argument*.

[*Example 4*:

``` cpp
template <template <class TT> class T> class A {
  typename T<int>::S s;
};

template <class U> class B {
private:
  struct S { ... };
};

A<B> b;             // error: A has no access to B::S
```

— *end example*]

When template argument packs or default *template-argument*s are used, a
*template-argument* list can be empty. In that case the empty `<>`
brackets shall still be used as the *template-argument-list*.

[*Example 5*:

``` cpp
template<class T = char> class String;
String<>* p;                    // OK: String<char>
String* q;                      // syntax error
template<class ... Elements> class Tuple;
Tuple<>* t;                     // OK: Elements is empty
Tuple* u;                       // syntax error
```

— *end example*]

An explicit destructor call [[class.dtor]] for an object that has a type
that is a class template specialization may explicitly specify the
*template-argument*s.

[*Example 6*:

``` cpp
template<class T> struct A {
  ~A();
};
void f(A<int>* p, A<int>* q) {
  p->A<int>::~A();              // OK: destructor call
  q->A<int>::~A<int>();         // OK: destructor call
}
```

— *end example*]

If the use of a *template-argument* gives rise to an ill-formed
construct in the instantiation of a template specialization, the program
is ill-formed.

When name lookup for the name in a *template-id* finds an overload set,
both non-template functions in the overload set and function templates
in the overload set for which the *template-argument*s do not match the
*template-parameter*s are ignored. If none of the function templates
have matching *template-parameter*s, the program is ill-formed.

When a *simple-template-id* does not name a function, a default
*template-argument* is implicitly instantiated [[temp.inst]] when the
value of that default argument is needed.

[*Example 7*:

``` cpp
template<typename T, typename U = int> struct S { };
S<bool>* p;         // the type of p is S<bool, int>*
```

The default argument for `U` is instantiated to form the type
`S<bool, int>*`.

— *end example*]

A *template-argument* followed by an ellipsis is a pack expansion
[[temp.variadic]].

### Template type arguments <a id="temp.arg.type">[[temp.arg.type]]</a>

A *template-argument* for a *template-parameter* which is a type shall
be a *type-id*.

[*Example 1*:

``` cpp
template <class T> class X { };
template <class T> void f(T t) { }
struct { } unnamed_obj;

void f() {
  struct A { };
  enum { e1 };
  typedef struct { } B;
  B b;
  X<A> x1;          // OK
  X<A*> x2;         // OK
  X<B> x3;          // OK
  f(e1);            // OK
  f(unnamed_obj);   // OK
  f(b);             // OK
}
```

— *end example*]

[*Note 1*: A template type argument may be an incomplete type
[[basic.types]]. — *end note*]

### Template non-type arguments <a id="temp.arg.nontype">[[temp.arg.nontype]]</a>

If the type `T` of a *template-parameter* [[temp.param]] contains a
placeholder type [[dcl.spec.auto]] or a placeholder for a deduced class
type [[dcl.type.class.deduct]], the type of the parameter is the type
deduced for the variable `x` in the invented declaration

``` cpp
T x = \grammartermnc{template-argument} ;
```

If a deduced parameter type is not permitted for a *template-parameter*
declaration [[temp.param]], the program is ill-formed.

A *template-argument* for a non-type *template-parameter* shall be a
converted constant expression [[expr.const]] of the type of the
*template-parameter*.

[*Note 1*: If the *template-argument* is an overload set (or the
address of such, including forming a pointer-to-member), the matching
function is selected from the set [[over.over]]. — *end note*]

For a non-type *template-parameter* of reference or pointer type, or for
each non-static data member of reference or pointer type in a non-type
*template-parameter* of class type or subobject thereof, the reference
or pointer value shall not refer to or be the address of (respectively):

- a temporary object [[class.temporary]],
- a string literal object [[lex.string]],
- the result of a `typeid` expression [[expr.typeid]],
- a predefined `__func__` variable [[dcl.fct.def.general]], or
- a subobject [[intro.object]] of one of the above.

[*Example 1*:

``` cpp
template<const int* pci> struct X { ... };
int ai[10];
X<ai> xi;                       // array to pointer and qualification conversions

struct Y { ... };
template<const Y& b> struct Z { ... };
Y y;
Z<y> z;                         // no conversion, but note extra cv-qualification

template<int (&pa)[5]> struct W { ... };
int b[5];
W<b> w;                         // no conversion

void f(char);
void f(int);

template<void (*pf)(int)> struct A { ... };

A<&f> a;                        // selects f(int)

template<auto n> struct B { ... };
B<5> b1;                        // OK, template parameter type is int
B<'a'> b2;                      // OK, template parameter type is char
B<2.5> b3;                      // OK, template parameter type is double
B<void(0)> b4;                  // error: template parameter type cannot be void
```

— *end example*]

[*Note 2*:

A *string-literal* [[lex.string]] is not an acceptable
*template-argument* for a *template-parameter* of non-class type.

[*Example 2*:

``` cpp
template<class T, T p> class X {
  ...
};

X<const char*, "Studebaker"> x; // error: string literal object as template-argument
X<const char*, "Knope" + 1> x2; // error: subobject of string literal object as template-argument

const char p[] = "Vivisectionist";
X<const char*, p> y;            // OK

struct A {
  constexpr A(const char*) {}
};

X<A, "Pyrophoricity"> z;        // OK, string-literal is a constructor argument to A
```

— *end example*]

— *end note*]

[*Note 3*:

A temporary object is not an acceptable *template-argument* when the
corresponding *template-parameter* has reference type.

[*Example 3*:

``` cpp
template<const int& CRI> struct B { ... };

B<1> b1;                        // error: temporary would be required for template argument

int c = 1;
B<c> b2;                        // OK

struct X { int n; };
struct Y { const int &r; };
template<Y y> struct C { ... };
C<Y{X{1}.n}> c;                 // error: subobject of temporary object used to initialize
                                // reference member of template parameter
```

— *end example*]

— *end note*]

### Template template arguments <a id="temp.arg.template">[[temp.arg.template]]</a>

A *template-argument* for a template *template-parameter* shall be the
name of a class template or an alias template, expressed as
*id-expression*. When the *template-argument* names a class template,
only primary class templates are considered when matching the template
template argument with the corresponding parameter; partial
specializations are not considered even if their parameter lists match
that of the template template parameter.

Any partial specializations [[temp.class.spec]] associated with the
primary class template or primary variable template are considered when
a specialization based on the template *template-parameter* is
instantiated. If a specialization is not visible at the point of
instantiation, and it would have been selected had it been visible, the
program is ill-formed, no diagnostic required.

[*Example 1*:

``` cpp
template<class T> class A {     // primary template
  int x;
};
template<class T> class A<T*> { // partial specialization
  long x;
};
template<template<class U> class V> class C {
  V<int>  y;
  V<int*> z;
};
C<A> c;             // V<int> within C<A> uses the primary template, so c.y.x has type int
                    // V<int*> within C<A> uses the partial specialization, so c.z.x has type long
```

— *end example*]

A *template-argument* matches a template *template-parameter* `P` when
`P` is at least as specialized as the *template-argument* `A`. In this
comparison, if `P` is unconstrained, the constraints on `A` are not
considered. If `P` contains a template parameter pack, then `A` also
matches `P` if each of `A`’s template parameters matches the
corresponding template parameter in the *template-head* of `P`. Two
template parameters match if they are of the same kind (type, non-type,
template), for non-type *template-parameter*s, their types are
equivalent [[temp.over.link]], and for template *template-parameter*s,
each of their corresponding *template-parameter*s matches, recursively.
When `P`’s *template-head* contains a template parameter pack
[[temp.variadic]], the template parameter pack will match zero or more
template parameters or template parameter packs in the *template-head*
of `A` with the same type and form as the template parameter pack in `P`
(ignoring whether those template parameters are template parameter
packs).

[*Example 2*:

``` cpp
template<class T> class A { ... };
template<class T, class U = T> class B { ... };
template<class ... Types> class C { ... };
template<auto n> class D { ... };
template<template<class> class P> class X { ... };
template<template<class ...> class Q> class Y { ... };
template<template<int> class R> class Z { ... };

X<A> xa;            // OK
X<B> xb;            // OK
X<C> xc;            // OK
Y<A> ya;            // OK
Y<B> yb;            // OK
Y<C> yc;            // OK
Z<D> zd;            // OK
```

— *end example*]

[*Example 3*:

``` cpp
template <class T> struct eval;

template <template <class, class...> class TT, class T1, class... Rest>
struct eval<TT<T1, Rest...>> { };

template <class T1> struct A;
template <class T1, class T2> struct B;
template <int N> struct C;
template <class T1, int N> struct D;
template <class T1, class T2, int N = 17> struct E;

eval<A<int>> eA;                // OK: matches partial specialization of eval
eval<B<int, float>> eB;         // OK: matches partial specialization of eval
eval<C<17>> eC;                 // error: C does not match TT in partial specialization
eval<D<int, 17>> eD;            // error: D does not match TT in partial specialization
eval<E<int, float>> eE;         // error: E does not match TT in partial specialization
```

— *end example*]

[*Example 4*:

``` cpp
template<typename T> concept C = requires (T t) { t.f(); };
template<typename T> concept D = C<T> && requires (T t) { t.g(); };

template<template<C> class P> struct S { };

template<C> struct X { };
template<D> struct Y { };
template<typename T> struct Z { };

S<X> s1;            // OK, X and P have equivalent constraints
S<Y> s2;            // error: P is not at least as specialized as Y
S<Z> s3;            // OK, P is at least as specialized as Z
```

— *end example*]

A template *template-parameter* `P` is at least as specialized as a
template *template-argument* `A` if, given the following rewrite to two
function templates, the function template corresponding to `P` is at
least as specialized as the function template corresponding to `A`
according to the partial ordering rules for function templates
[[temp.func.order]]. Given an invented class template `X` with the
*template-head* of `A` (including default arguments and
*requires-clause*, if any):

- Each of the two function templates has the same template parameters
  and *requires-clause* (if any), respectively, as `P` or `A`.
- Each function template has a single function parameter whose type is a
  specialization of `X` with template arguments corresponding to the
  template parameters from the respective function template where, for
  each template parameter `PP` in the *template-head* of the function
  template, a corresponding template argument `AA` is formed. If `PP`
  declares a template parameter pack, then `AA` is the pack expansion
  `PP...` [[temp.variadic]]; otherwise, `AA` is the *id-expression*
  `PP`.

If the rewrite produces an invalid type, then `P` is not at least as
specialized as `A`.

## Template constraints <a id="temp.constr">[[temp.constr]]</a>

[*Note 1*: This subclause defines the meaning of constraints on
template arguments. The abstract syntax and satisfaction rules are
defined in [[temp.constr.constr]]. Constraints are associated with
declarations in [[temp.constr.decl]]. Declarations are partially ordered
by their associated constraints [[temp.constr.order]]. — *end note*]

### Constraints <a id="temp.constr.constr">[[temp.constr.constr]]</a>

A *constraint* is a sequence of logical operations and operands that
specifies requirements on template arguments. The operands of a logical
operation are constraints. There are three different kinds of
constraints:

- conjunctions [[temp.constr.op]],
- disjunctions [[temp.constr.op]], and
- atomic constraints [[temp.constr.atomic]].

In order for a constrained template to be instantiated [[temp.spec]],
its associated constraints [[temp.constr.decl]] shall be satisfied as
described in the following subclauses.

[*Note 1*: Forming the name of a specialization of a class template, a
variable template, or an alias template [[temp.names]] requires the
satisfaction of its constraints. Overload resolution
[[over.match.viable]] requires the satisfaction of constraints on
functions and function templates. — *end note*]

#### Logical operations <a id="temp.constr.op">[[temp.constr.op]]</a>

There are two binary logical operations on constraints: conjunction and
disjunction.

[*Note 1*: These logical operations have no corresponding C++ syntax.
For the purpose of exposition, conjunction is spelled using the symbol ∧
and disjunction is spelled using the symbol ∨. The operands of these
operations are called the left and right operands. In the constraint
A ∧ B, A is the left operand, and B is the right operand. — *end note*]

A *conjunction* is a constraint taking two operands. To determine if a
conjunction is *satisfied*, the satisfaction of the first operand is
checked. If that is not satisfied, the conjunction is not satisfied.
Otherwise, the conjunction is satisfied if and only if the second
operand is satisfied.

A *disjunction* is a constraint taking two operands. To determine if a
disjunction is *satisfied*, the satisfaction of the first operand is
checked. If that is satisfied, the disjunction is satisfied. Otherwise,
the disjunction is satisfied if and only if the second operand is
satisfied.

[*Example 1*:

``` cpp
template<typename T>
  constexpr bool get_value() { return T::value; }

template<typename T>
  requires (sizeof(T) > 1) && (get_value<T>())
    void f(T);      // has associated constraint sizeof(T) > 1 ∧ get_value<T>()

void f(int);

f('a'); // OK: calls f(int)
```

In the satisfaction of the associated constraints [[temp.constr.decl]]
of `f`, the constraint `sizeof(char) > 1` is not satisfied; the second
operand is not checked for satisfaction.

— *end example*]

[*Note 2*:

A logical negation expression [[expr.unary.op]] is an atomic constraint;
the negation operator is not treated as a logical operation on
constraints. As a result, distinct negation *constraint-expression*s
that are equivalent under  [[temp.over.link]] do not subsume one another
under  [[temp.constr.order]]. Furthermore, if substitution to determine
whether an atomic constraint is satisfied [[temp.constr.atomic]]
encounters a substitution failure, the constraint is not satisfied,
regardless of the presence of a negation operator.

[*Example 2*:

``` cpp
template <class T> concept sad = false;

template <class T> int f1(T) requires (!sad<T>);
template <class T> int f1(T) requires (!sad<T>) && true;
int i1 = f1(42);        // ambiguous, !sad<T> atomic constraint expressions[temp.constr.atomic]
                        // are not formed from the same expression

template <class T> concept not_sad = !sad<T>;
template <class T> int f2(T) requires not_sad<T>;
template <class T> int f2(T) requires not_sad<T> && true;
int i2 = f2(42);        // OK, !sad<T> atomic constraint expressions both come from not_sad

template <class T> int f3(T) requires (!sad<typename T::type>);
int i3 = f3(42);        // error: associated constraints not satisfied due to substitution failure

template <class T> concept sad_nested_type = sad<typename T::type>;
template <class T> int f4(T) requires (!sad_nested_type<T>);
int i4 = f4(42);        // OK, substitution failure contained within sad_nested_type
```

Here, `requires (!sad<typename T::type>)` requires that there is a
nested `type` that is not `sad`, whereas
`requires (!sad_nested_type<T>)` requires that there is no `sad` nested
`type`.

— *end example*]

— *end note*]

#### Atomic constraints <a id="temp.constr.atomic">[[temp.constr.atomic]]</a>

An *atomic constraint* is formed from an expression `E` and a mapping
from the template parameters that appear within `E` to template
arguments that are formed via substitution during constraint
normalization in the declaration of a constrained entity (and,
therefore, can involve the unsubstituted template parameters of the
constrained entity), called the *parameter mapping*
[[temp.constr.decl]].

[*Note 1*: Atomic constraints are formed by constraint normalization
[[temp.constr.normal]]. `E` is never a logical expression
[[expr.log.and]] nor a logical expression
[[expr.log.or]]. — *end note*]

Two atomic constraints, e₁ and e₂, are *identical* if they are formed
from the same appearance of the same *expression* and if, given a
hypothetical template A whose *template-parameter-list* consists of
*template-parameter*s corresponding and equivalent [[temp.over.link]] to
those mapped by the parameter mappings of the expression, a
*template-id* naming A whose *template-argument*s are the targets of the
parameter mapping of e₁ is the same [[temp.type]] as a *template-id*
naming A whose *template-argument*s are the targets of the parameter
mapping of e₂.

[*Note 2*:

The comparison of parameter mappings of atomic constraints operates in a
manner similar to that of declaration matching with alias template
substitution [[temp.alias]].

[*Example 1*:

``` cpp
template <unsigned N> constexpr bool Atomic = true;
template <unsigned N> concept C = Atomic<N>;
template <unsigned N> concept Add1 = C<N + 1>;
template <unsigned N> concept AddOne = C<N + 1>;
template <unsigned M> void f()
  requires Add1<2 * M>;
template <unsigned M> int f()
  requires AddOne<2 * M> && true;

int x = f<0>();     // OK, the atomic constraints from concept C in both fs are Atomic<N>
                    // with mapping similar to `N` ↦ `2 * M + 1`

template <unsigned N> struct WrapN;
template <unsigned N> using Add1Ty = WrapN<N + 1>;
template <unsigned N> using AddOneTy = WrapN<N + 1>;
template <unsigned M> void g(Add1Ty<2 * M> *);
template <unsigned M> void g(AddOneTy<2 * M> *);

void h() {
  g<0>(nullptr);    // OK, there is only one g
}
```

— *end example*]

This similarity includes the situation where a program is ill-formed, no
diagnostic required, when the meaning of the program depends on whether
two constructs are equivalent, and they are functionally equivalent but
not equivalent.

[*Example 2*:

``` cpp
template <unsigned N> void f2()
  requires Add1<2 * N>;
template <unsigned N> int f2()
  requires Add1<N * 2> && true;
void h2() {
  f2<0>();          // ill-formed, no diagnostic required:
                    // requires determination of subsumption between atomic constraints that are
                    // functionally equivalent but not equivalent
}
```

— *end example*]

— *end note*]

To determine if an atomic constraint is *satisfied*, the parameter
mapping and template arguments are first substituted into its
expression. If substitution results in an invalid type or expression,
the constraint is not satisfied. Otherwise, the lvalue-to-rvalue
conversion [[conv.lval]] is performed if necessary, and `E` shall be a
constant expression of type `bool`. The constraint is satisfied if and
only if evaluation of `E` results in `true`. If, at different points in
the program, the satisfaction result is different for identical atomic
constraints and template arguments, the program is ill-formed, no
diagnostic required.

[*Example 3*:

``` cpp
template<typename T> concept C =
  sizeof(T) == 4 && !true;      // requires atomic constraints sizeof(T) == 4 and !true

template<typename T> struct S {
  constexpr operator bool() const { return true; }
};

template<typename T> requires (S<T>{})
void f(T);                      // #1
void f(int);                    // #2

void g() {
  f(0);                         // error: expression S<int>{} does not have type bool
}                               // while checking satisfaction of deduced arguments of #1;
                                // call is ill-formed even though #2 is a better match
```

— *end example*]

### Constrained declarations <a id="temp.constr.decl">[[temp.constr.decl]]</a>

A template declaration [[temp.pre]] or templated function declaration
[[dcl.fct]] can be constrained by the use of a *requires-clause*. This
allows the specification of constraints for that declaration as an
expression:

``` bnf
constraint-expression:
    logical-or-expression
```

Constraints can also be associated with a declaration through the use of
*type-constraint*s in a *template-parameter-list* or
parameter-type-list. Each of these forms introduces additional
*constraint-expression*s that are used to constrain the declaration.

A declaration’s *associated constraints* are defined as follows:

- If there are no introduced *constraint-expression*s, the declaration
  has no associated constraints.
- Otherwise, if there is a single introduced *constraint-expression*,
  the associated constraints are the normal form [[temp.constr.normal]]
  of that expression.
- Otherwise, the associated constraints are the normal form of a logical
  expression [[expr.log.and]] whose operands are in the following order:
  - the *constraint-expression* introduced by each *type-constraint*
    [[temp.param]] in the declaration’s *template-parameter-list*, in
    order of appearance, and
  - the *constraint-expression* introduced by a *requires-clause*
    following a *template-parameter-list* [[temp.pre]], and
  - the *constraint-expression* introduced by each *type-constraint* in
    the parameter-type-list of a function declaration, and
  - the *constraint-expression* introduced by a trailing
    *requires-clause* [[dcl.decl]] of a function declaration
    [[dcl.fct]].

The formation of the associated constraints establishes the order in
which constraints are instantiated when checking for satisfaction
[[temp.constr.constr]].

[*Example 1*:

``` cpp
template<typename T> concept C = true;

template<C T> void f1(T);
template<typename T> requires C<T> void f2(T);
template<typename T> void f3(T) requires C<T>;
```

The functions `f1`, `f2`, and `f3` have the associated constraint
`C<T>`.

``` cpp
template<typename T> concept C1 = true;
template<typename T> concept C2 = sizeof(T) > 0;

template<C1 T> void f4(T) requires C2<T>;
template<typename T> requires C1<T> && C2<T> void f5(T);
```

The associated constraints of `f4` and `f5` are `C1<T> ∧ C2<T>`.

``` cpp
template<C1 T> requires C2<T> void f6();
template<C2 T> requires C1<T> void f7();
```

The associated constraints of `f6` are `C1<T> ∧ C2<T>`, and those of
`f7` are `C2<T> ∧ C1<T>`.

— *end example*]

When determining whether a given introduced *constraint-expression* C₁
of a declaration in an instantiated specialization of a templated class
is equivalent [[temp.over.link]] to the corresponding
*constraint-expression* C₂ of a declaration outside the class body, C₁
is instantiated. If the instantiation results in an invalid expression,
the *constraint-expression*s are not equivalent.

[*Note 1*: This can happen when determining which member template is
specialized by an explicit specialization declaration. — *end note*]

[*Example 2*:

``` cpp
template <class T> concept C = true;
template <class T> struct A {
  template <class U> U f(U) requires C<typename T::type>;   // #1
  template <class U> U f(U) requires C<T>;                  // #2
};

template <> template <class U>
U A<int>::f(U u) requires C<int> { return u; }              // OK, specializes #2
```

Substituting `int` for `T` in `C<typename T::type>` produces an invalid
expression, so the specialization does not match \#1. Substituting `int`
for `T` in `C<T>` produces `C<int>`, which is equivalent to the
*constraint-expression* for the specialization, so it does match \#2.

— *end example*]

### Constraint normalization <a id="temp.constr.normal">[[temp.constr.normal]]</a>

The *normal form* of an *expression* `E` is a constraint
[[temp.constr.constr]] that is defined as follows:

- The normal form of an expression `( E )` is the normal form of `E`.
- The normal form of an expression `E1 || E2` is the disjunction
  [[temp.constr.op]] of the normal forms of `E1` and `E2`.
- The normal form of an expression `E1 && E2` is the conjunction of the
  normal forms of `E1` and `E2`.
- The normal form of a concept-id `C<A_1, A_2, ..., A_n>` is the normal
  form of the *constraint-expression* of `C`, after substituting
  `A_1, A_2, ..., A_n` for `C`'s respective template parameters in the
  parameter mappings in each atomic constraint. If any such substitution
  results in an invalid type or expression, the program is ill-formed;
  no diagnostic is required.
  \[*Example 1*:
  ``` cpp
  template<typename T> concept A = T::value || true;
  template<typename U> concept B = A<U*>;
  template<typename V> concept C = B<V&>;
  ```

  Normalization of `B`'s *constraint-expression* is valid and results in
  `T::value` (with the mapping `T` ↦ `U*`) ∨ `true` (with an empty
  mapping), despite the expression `T::value` being ill-formed for a
  pointer type `T`. Normalization of `C`'s *constraint-expression*
  results in the program being ill-formed, because it would form the
  invalid type `V&*` in the parameter mapping.
  — *end example*]
- The normal form of any other expression `E` is the atomic constraint
  whose expression is `E` and whose parameter mapping is the identity
  mapping.

The process of obtaining the normal form of a *constraint-expression* is
called *normalization*.

[*Note 1*: Normalization of *constraint-expression*s is performed when
determining the associated constraints [[temp.constr.constr]] of a
declaration and when evaluating the value of an *id-expression* that
names a concept specialization [[expr.prim.id]]. — *end note*]

[*Example 1*:

``` cpp
template<typename T> concept C1 = sizeof(T) == 1;
template<typename T> concept C2 = C1<T> && 1 == 2;
template<typename T> concept C3 = requires { typename T::type; };
template<typename T> concept C4 = requires (T x) { ++x; }

template<C2 U> void f1(U);      // #1
template<C3 U> void f2(U);      // #2
template<C4 U> void f3(U);      // #3
```

The associated constraints of \#1 are `sizeof(T) == 1` (with mapping
`T` ↦ `U`) ∧ `1 == 2`.  
The associated constraints of \#2 are `requires { typename T::type; }`
(with mapping `T` ↦ `U`).  
The associated constraints of \#3 are `requires (T x) { ++x; }` (with
mapping `T` ↦ `U`).

— *end example*]

### Partial ordering by constraints <a id="temp.constr.order">[[temp.constr.order]]</a>

A constraint P *subsumes* a constraint Q if and only if, for every
disjunctive clause Pᵢ in the disjunctive normal form[^4] of P, Pᵢ
subsumes every conjunctive clause Qⱼ in the conjunctive normal form[^5]
of Q, where

- a disjunctive clause Pᵢ subsumes a conjunctive clause Qⱼ if and only
  if there exists an atomic constraint Pᵢₐ in Pᵢ for which there exists
  an atomic constraint $Q_{jb}$ in Qⱼ such that Pᵢₐ subsumes $Q_{jb}$,
  and
- an atomic constraint A subsumes another atomic constraint B if and
  only if A and B are identical using the rules described in
  [[temp.constr.atomic]].

[*Example 1*: Let A and B be atomic constraints [[temp.constr.atomic]].
The constraint A ∧ B subsumes A, but A does not subsume A ∧ B. The
constraint A subsumes A ∨ B, but A ∨ B does not subsume A. Also note
that every constraint subsumes itself. — *end example*]

[*Note 1*:

The subsumption relation defines a partial ordering on constraints. This
partial ordering is used to determine

- the best viable candidate of non-template functions
  [[over.match.best]],
- the address of a non-template function [[over.over]],
- the matching of template template arguments [[temp.arg.template]],
- the partial ordering of class template specializations
  [[temp.class.order]], and
- the partial ordering of function templates [[temp.func.order]].

— *end note*]

A declaration `D1` is *at least as constrained* as a declaration `D2` if

- `D1` and `D2` are both constrained declarations and `D1`’s associated
  constraints subsume those of `D2`; or
- `D2` has no associated constraints.

A declaration `D1` is *more constrained* than another declaration `D2`
when `D1` is at least as constrained as `D2`, and `D2` is not at least
as constrained as `D1`.

[*Example 2*:

``` cpp
template<typename T> concept C1 = requires(T t) { --t; };
template<typename T> concept C2 = C1<T> && requires(T t) { *t; };

template<C1 T> void f(T);       // #1
template<C2 T> void f(T);       // #2
template<typename T> void g(T); // #3
template<C1 T> void g(T);       // #4

f(0);                           // selects #1
f((int*)0);                     // selects #2
g(true);                        // selects #3 because C1<bool> is not satisfied
g(0);                           // selects #4
```

— *end example*]

## Type equivalence <a id="temp.type">[[temp.type]]</a>

Two *template-id*s are the same if

- their *template-name*s, *operator-function-id*s, or
  *literal-operator-id*s refer to the same template, and
- their corresponding type *template-argument*s are the same type, and
- their corresponding non-type *template-argument*s are
  template-argument-equivalent (see below) after conversion to the type
  of the *template-parameter*, and
- their corresponding template *template-argument*s refer to the same
  template.

Two *template-id*s that are the same refer to the same class, function,
or variable.

Two values are *template-argument-equivalent* if they are of the same
type and

- they are of integral type and their values are the same, or
- they are of floating-point type and their values are identical, or
- they are of type `std::nullptr_t`, or
- they are of enumeration type and their values are the same, [^6] or
- they are of pointer type and they have the same pointer value, or
- they are of pointer-to-member type and they refer to the same class
  member or are both the null member pointer value, or
- they are of reference type and they refer to the same object or
  function, or
- they are of array type and their corresponding elements are
  template-argument-equivalent, [^7] or
- they are of union type and either they both have no active member or
  they have the same active member and their active members are
  template-argument-equivalent, or
- they are of class type and their corresponding direct subobjects and
  reference members are template-argument-equivalent.

[*Example 1*:

``` cpp
template<class E, int size> class buffer { ... };
buffer<char,2*512> x;
buffer<char,1024> y;
```

declares `x` and `y` to be of the same type, and

``` cpp
template<class T, void(*err_fct)()> class list { ... };
list<int,&error_handler1> x1;
list<int,&error_handler2> x2;
list<int,&error_handler2> x3;
list<char,&error_handler2> x4;
```

declares `x2` and `x3` to be of the same type. Their type differs from
the types of `x1` and `x4`.

``` cpp
template<class T> struct X { };
template<class> struct Y { };
template<class T> using Z = Y<T>;
X<Y<int> > y;
X<Z<int> > z;
```

declares `y` and `z` to be of the same type.

— *end example*]

If an expression e is type-dependent [[temp.dep.expr]], `decltype(e)`
denotes a unique dependent type. Two such *decltype-specifier*s refer to
the same type only if their *expression*s are equivalent
[[temp.over.link]].

[*Note 1*: However, such a type may be aliased, e.g., by a
*typedef-name*. — *end note*]

## Template declarations <a id="temp.decls">[[temp.decls]]</a>

A *template-id*, that is, the *template-name* followed by a
*template-argument-list* shall not be specified in the declaration of a
primary template declaration.

[*Example 1*:

``` cpp
template<class T1, class T2, int I> class A<T1, T2, I> { };     // error
template<class T1, int I> void sort<T1, I>(T1 data[I]);         // error
```

— *end example*]

[*Note 1*: However, this syntax is allowed in class template partial
specializations [[temp.class.spec]]. — *end note*]

For purposes of name lookup and instantiation, default arguments,
*type-constraint*s, *requires-clause*s [[temp.pre]], and
*noexcept-specifier*s of function templates and of member functions of
class templates are considered definitions; each default argument,
*type-constraint*, *requires-clause*, or *noexcept-specifier* is a
separate definition which is unrelated to the templated function
definition or to any other default arguments *type-constraint*s,
*requires-clause*s, or *noexcept-specifier*s. For the purpose of
instantiation, the substatements of a constexpr if statement [[stmt.if]]
are considered definitions.

Because an *alias-declaration* cannot declare a *template-id*, it is not
possible to partially or explicitly specialize an alias template.

### Class templates <a id="temp.class">[[temp.class]]</a>

A *class template* defines the layout and operations for an unbounded
set of related types.

[*Example 1*:

A single class template `List` might provide an unbounded set of class
definitions: one class `List<T>` for every type `T`, each describing a
linked list of elements of type `T`. Similarly, a class template `Array`
describing a contiguous, dynamic array might be defined like this:

``` cpp
template<class T> class Array {
  T* v;
  int sz;
public:
  explicit Array(int);
  T& operator[](int);
  T& elem(int i) { return v[i]; }
};
```

The prefix `template<class T>` specifies that a template is being
declared and that a *type-name* `T` may be used in the declaration. In
other words, `Array` is a parameterized type with `T` as its parameter.

— *end example*]

When a member function, a member class, a member enumeration, a static
data member or a member template of a class template is defined outside
of the class template definition, the member definition is defined as a
template definition in which the *template-head* is equivalent to that
of the class template [[temp.over.link]]. The names of the template
parameters used in the definition of the member may be different from
the template parameter names used in the class template definition. The
template argument list following the class template name in the member
definition shall name the parameters in the same order as the one used
in the template parameter list of the member. Each template parameter
pack shall be expanded with an ellipsis in the template argument list.

[*Example 2*:

``` cpp
template<class T1, class T2> struct A {
  void f1();
  void f2();
};

template<class T2, class T1> void A<T2,T1>::f1() { }    // OK
template<class T2, class T1> void A<T1,T2>::f2() { }    // error
```

``` cpp
template<class ... Types> struct B {
  void f3();
  void f4();
};

template<class ... Types> void B<Types ...>::f3() { }   // OK
template<class ... Types> void B<Types>::f4() { }       // error
```

``` cpp
template<typename T> concept C = true;
template<typename T> concept D = true;

template<C T> struct S {
  void f();
  void g();
  void h();
  template<D U> struct Inner;
};

template<C A> void S<A>::f() { }        // OK: template-head{s} match
template<typename T> void S<T>::g() { } // error: no matching declaration for S<T>

template<typename T> requires C<T>      // ill-formed, no diagnostic required: template-head{s} are
void S<T>::h() { }                      // functionally equivalent but not equivalent

template<C X> template<D Y>
struct S<X>::Inner { };                 // OK
```

— *end example*]

In a redeclaration, partial specialization, explicit specialization or
explicit instantiation of a class template, the *class-key* shall agree
in kind with the original class template declaration [[dcl.type.elab]].

#### Member functions of class templates <a id="temp.mem.func">[[temp.mem.func]]</a>

A member function of a class template may be defined outside of the
class template definition in which it is declared.

[*Example 1*:

``` cpp
template<class T> class Array {
  T* v;
  int sz;
public:
  explicit Array(int);
  T& operator[](int);
  T& elem(int i) { return v[i]; }
};
```

declares three member functions of a class template. The subscript
function might be defined like this:

``` cpp
template<class T> T& Array<T>::operator[](int i) {
  if (i<0 || sz<=i) error("Array: range error");
  return v[i];
}
```

A constrained member function can be defined out of line:

``` cpp
template<typename T> concept C = requires {
  typename T::type;
};

template<typename T> struct S {
  void f() requires C<T>;
  void g() requires C<T>;
};

template<typename T>
  void S<T>::f() requires C<T> { }      // OK
template<typename T>
  void S<T>::g() { }                    // error: no matching function in S<T>
```

— *end example*]

The *template-argument*s for a member function of a class template are
determined by the *template-argument*s of the type of the object for
which the member function is called.

[*Example 2*:

The *template-argument* for `Array<T>::operator[]` will be determined by
the `Array` to which the subscripting operation is applied.

``` cpp
Array<int> v1(20);
Array<dcomplex> v2(30);

v1[3] = 7;                              // Array<int>::operator[]
v2[3] = dcomplex(7,8);                  // Array<dcomplex>::operator[]
```

— *end example*]

#### Deduction guides <a id="temp.deduct.guide">[[temp.deduct.guide]]</a>

Deduction guides are used when a *template-name* appears as a type
specifier for a deduced class type [[dcl.type.class.deduct]]. Deduction
guides are not found by name lookup. Instead, when performing class
template argument deduction [[over.match.class.deduct]], any deduction
guides declared for the class template are considered.

``` bnf
deduction-guide:
    explicit-specifierₒₚₜ template-name '(' parameter-declaration-clause ')' '->' simple-template-id ';'
```

[*Example 1*:

``` cpp
template<class T, class D = int>
struct S {
  T data;
};
template<class U>
S(U) -> S<typename U::type>;

struct A {
  using type = short;
  operator type();
};
S x{A()};           // x is of type S<short, int>
```

— *end example*]

The same restrictions apply to the *parameter-declaration-clause* of a
deduction guide as in a function declaration [[dcl.fct]]. The
*simple-template-id* shall name a class template specialization. The
*template-name* shall be the same *identifier* as the *template-name* of
the *simple-template-id*. A *deduction-guide* shall be declared in the
same scope as the corresponding class template and, for a member class
template, with the same access. Two deduction guide declarations in the
same translation unit for the same class template shall not have
equivalent *parameter-declaration-clause*s.

#### Member classes of class templates <a id="temp.mem.class">[[temp.mem.class]]</a>

A member class of a class template may be defined outside the class
template definition in which it is declared.

[*Note 1*:

The member class must be defined before its first use that requires an
instantiation [[temp.inst]]. For example,

``` cpp
template<class T> struct A {
  class B;
};
A<int>::B* b1;                          // OK: requires A to be defined but not A::B
template<class T> class A<T>::B { };
A<int>::B  b2;                          // OK: requires A::B to be defined
```

— *end note*]

#### Static data members of class templates <a id="temp.static">[[temp.static]]</a>

A definition for a static data member or static data member template may
be provided in a namespace scope enclosing the definition of the static
member’s class template.

[*Example 1*:

``` cpp
template<class T> class X {
  static T s;
};
template<class T> T X<T>::s = 0;

struct limits {
  template<class T>
    static const T min;                 // declaration
};

template<class T>
  const T limits::min = { };            // definition
```

— *end example*]

An explicit specialization of a static data member declared as an array
of unknown bound can have a different bound from its definition, if any.

[*Example 2*:

``` cpp
template <class T> struct A {
  static int i[];
};
template <class T> int A<T>::i[4];      // 4 elements
template <> int A<int>::i[] = { 1 };    // OK: 1 element
```

— *end example*]

#### Enumeration members of class templates <a id="temp.mem.enum">[[temp.mem.enum]]</a>

An enumeration member of a class template may be defined outside the
class template definition.

[*Example 1*:

``` cpp
template<class T> struct A {
  enum E : T;
};
A<int> a;
template<class T> enum A<T>::E : T { e1, e2 };
A<int>::E e = A<int>::e1;
```

— *end example*]

### Member templates <a id="temp.mem">[[temp.mem]]</a>

A template can be declared within a class or class template; such a
template is called a member template. A member template can be defined
within or outside its class definition or class template definition. A
member template of a class template that is defined outside of its class
template definition shall be specified with a *template-head* equivalent
to that of the class template followed by a *template-head* equivalent
to that of the member template [[temp.over.link]].

[*Example 1*:

``` cpp
template<class T> struct string {
  template<class T2> int compare(const T2&);
  template<class T2> string(const string<T2>& s) { ... }
};

template<class T> template<class T2> int string<T>::compare(const T2& s) {
}
```

— *end example*]

[*Example 2*:

``` cpp
template<typename T> concept C1 = true;
template<typename T> concept C2 = sizeof(T) <= 4;

template<C1 T> struct S {
  template<C2 U> void f(U);
  template<C2 U> void g(U);
};

template<C1 T> template<C2 U>
void S<T>::f(U) { }             // OK
template<C1 T> template<typename U>
void S<T>::g(U) { }             // error: no matching function in S<T>
```

— *end example*]

A local class of non-closure type shall not have member templates.
Access control rules [[class.access]] apply to member template names. A
destructor shall not be a member template. A non-template member
function [[dcl.fct]] with a given name and type and a member function
template of the same name, which could be used to generate a
specialization of the same type, can both be declared in a class. When
both exist, a use of that name and type refers to the non-template
member unless an explicit template argument list is supplied.

[*Example 3*:

``` cpp
template <class T> struct A {
  void f(int);
  template <class T2> void f(T2);
};

template <> void A<int>::f(int) { }                 // non-template member function
template <> template <> void A<int>::f<>(int) { }   // member function template specialization

int main() {
  A<char> ac;
  ac.f(1);                                          // non-template
  ac.f('c');                                        // template
  ac.f<>(1);                                        // template
}
```

— *end example*]

A member function template shall not be virtual.

[*Example 4*:

``` cpp
template <class T> struct AA {
  template <class C> virtual void g(C);             // error
  virtual void f();                                 // OK
};
```

— *end example*]

A specialization of a member function template does not override a
virtual function from a base class.

[*Example 5*:

``` cpp
class B {
  virtual void f(int);
};

class D : public B {
  template <class T> void f(T); // does not override B::f(int)
  void f(int i) { f<>(i); }     // overriding function that calls the template instantiation
};
```

— *end example*]

A specialization of a conversion function template is referenced in the
same way as a non-template conversion function that converts to the same
type.

[*Example 6*:

``` cpp
struct A {
  template <class T> operator T*();
};
template <class T> A::operator T*(){ return 0; }
template <> A::operator char*(){ return 0; }        // specialization
template A::operator void*();                       // explicit instantiation

int main() {
  A a;
  int* ip;
  ip = a.operator int*();       // explicit call to template operator A::operator int*()
}
```

— *end example*]

[*Note 1*: There is no syntax to form a *template-id* [[temp.names]] by
providing an explicit template argument list [[temp.arg.explicit]] for a
conversion function template [[class.conv.fct]]. — *end note*]

A specialization of a conversion function template is not found by name
lookup. Instead, any conversion function templates visible in the
context of the use are considered. For each such operator, if argument
deduction succeeds [[temp.deduct.conv]], the resulting specialization is
used as if found by name lookup.

A *using-declaration* in a derived class cannot refer to a
specialization of a conversion function template in a base class.

Overload resolution [[over.ics.rank]] and partial ordering
[[temp.func.order]] are used to select the best conversion function
among multiple specializations of conversion function templates and/or
non-template conversion functions.

### Variadic templates <a id="temp.variadic">[[temp.variadic]]</a>

A *template parameter pack* is a template parameter that accepts zero or
more template arguments.

[*Example 1*:

``` cpp
template<class ... Types> struct Tuple { };

Tuple<> t0;                     // Types contains no arguments
Tuple<int> t1;                  // Types contains one argument: int
Tuple<int, float> t2;           // Types contains two arguments: int and float
Tuple<0> error;                 // error: 0 is not a type
```

— *end example*]

A *function parameter pack* is a function parameter that accepts zero or
more function arguments.

[*Example 2*:

``` cpp
template<class ... Types> void f(Types ... args);

f();                            // args contains no arguments
f(1);                           // args contains one argument: int
f(2, 1.0);                      // args contains two arguments: int and double
```

— *end example*]

An **init-capture* pack* is a lambda capture that introduces an
*init-capture* for each of the elements in the pack expansion of its
*initializer*.

[*Example 3*:

``` cpp
template <typename... Args>
void foo(Args... args) {
    [...xs=args]{
        bar(xs...);             // xs is an init-capture pack
    };
}

foo();                          // xs contains zero init-captures
foo(1);                         // xs contains one init-capture
```

— *end example*]

A *pack* is a template parameter pack, a function parameter pack, or an
*init-capture* pack. The number of elements of a template parameter pack
or a function parameter pack is the number of arguments provided for the
parameter pack. The number of elements of an *init-capture* pack is the
number of elements in the pack expansion of its *initializer*.

A *pack expansion* consists of a *pattern* and an ellipsis, the
instantiation of which produces zero or more instantiations of the
pattern in a list (described below). The form of the pattern depends on
the context in which the expansion occurs. Pack expansions can occur in
the following contexts:

- In a function parameter pack [[dcl.fct]]; the pattern is the
  *parameter-declaration* without the ellipsis.
- In a *using-declaration* [[namespace.udecl]]; the pattern is a
  *using-declarator*.
- In a template parameter pack that is a pack expansion [[temp.param]]:
  - if the template parameter pack is a *parameter-declaration*; the
    pattern is the *parameter-declaration* without the ellipsis;
  - if the template parameter pack is a *type-parameter*; the pattern is
    the corresponding *type-parameter* without the ellipsis.
- In an *initializer-list* [[dcl.init]]; the pattern is an
  *initializer-clause*.
- In a *base-specifier-list* [[class.derived]]; the pattern is a
  *base-specifier*.
- In a *mem-initializer-list* [[class.base.init]] for a
  *mem-initializer* whose *mem-initializer-id* denotes a base class; the
  pattern is the *mem-initializer*.
- In a *template-argument-list* [[temp.arg]]; the pattern is a
  *template-argument*.
- In an *attribute-list* [[dcl.attr.grammar]]; the pattern is an
  *attribute*.
- In an *alignment-specifier* [[dcl.align]]; the pattern is the
  *alignment-specifier* without the ellipsis.
- In a *capture-list* [[expr.prim.lambda.capture]]; the pattern is the
  *capture* without the ellipsis.
- In a `sizeof...` expression [[expr.sizeof]]; the pattern is an
  *identifier*.
- In a *fold-expression* [[expr.prim.fold]]; the pattern is the
  *cast-expression* that contains an unexpanded pack.

[*Example 4*:

``` cpp
template<class ... Types> void f(Types ... rest);
template<class ... Types> void g(Types ... rest) {
  f(&rest ...);     // ``&rest ...'' is a pack expansion; ``&rest'' is its pattern
}
```

— *end example*]

For the purpose of determining whether a pack satisfies a rule regarding
entities other than packs, the pack is considered to be the entity that
would result from an instantiation of the pattern in which it appears.

A pack whose name appears within the pattern of a pack expansion is
expanded by that pack expansion. An appearance of the name of a pack is
only expanded by the innermost enclosing pack expansion. The pattern of
a pack expansion shall name one or more packs that are not expanded by a
nested pack expansion; such packs are called *unexpanded packs* in the
pattern. All of the packs expanded by a pack expansion shall have the
same number of arguments specified. An appearance of a name of a pack
that is not expanded is ill-formed.

[*Example 5*:

``` cpp
template<typename...> struct Tuple {};
template<typename T1, typename T2> struct Pair {};

template<class ... Args1> struct zip {
  template<class ... Args2> struct with {
    typedef Tuple<Pair<Args1, Args2> ... > type;
  };
};

typedef zip<short, int>::with<unsigned short, unsigned>::type T1;
    // T1 is Tuple<Pair<short, unsigned short>, Pair<int, unsigned>{>}
typedef zip<short>::with<unsigned short, unsigned>::type T2;
    // error: different number of arguments specified for Args1 and Args2

template<class ... Args>
  void g(Args ... args) {                   // OK: Args is expanded by the function parameter pack args
    f(const_cast<const Args*>(&args)...);   // OK: ``Args'' and ``args'' are expanded
    f(5 ...);                               // error: pattern does not contain any packs
    f(args);                                // error: pack ``args'' is not expanded
    f(h(args ...) + args ...);              // OK: first ``args'' expanded within h,
                                            // second ``args'' expanded within f
  }
```

— *end example*]

The instantiation of a pack expansion that is neither a `sizeof...`
expression nor a *fold-expression* produces a list of elements E₁, E₂,
⋯, $\mathtt{E}_N$, where N is the number of elements in the pack
expansion parameters. Each Eᵢ is generated by instantiating the pattern
and replacing each pack expansion parameter with its iᵗʰ element. Such
an element, in the context of the instantiation, is interpreted as
follows:

- if the pack is a template parameter pack, the element is a template
  parameter [[temp.param]] of the corresponding kind (type or non-type)
  designating the iᵗʰ corresponding type or value template argument;
- if the pack is a function parameter pack, the element is an
  *id-expression* designating the iᵗʰ function parameter that resulted
  from instantiation of the function parameter pack declaration;
  otherwise
- if the pack is an *init-capture* pack, the element is an
  *id-expression* designating the variable introduced by the iᵗʰ
  *init-capture* that resulted from instantiation of the *init-capture*
  pack.

All of the Eᵢ become items in the enclosing list.

[*Note 1*: The variety of list varies with the context:
*expression-list*, *base-specifier-list*, *template-argument-list*,
etc. — *end note*]

When N is zero, the instantiation of the expansion produces an empty
list. Such an instantiation does not alter the syntactic interpretation
of the enclosing construct, even in cases where omitting the list
entirely would otherwise be ill-formed or would result in an ambiguity
in the grammar.

[*Example 6*:

``` cpp
template<class... T> struct X : T... { };
template<class... T> void f(T... values) {
  X<T...> x(values...);
}

template void f<>();    // OK: X<> has no base classes
                        // x is a variable of type X<> that is value-initialized
```

— *end example*]

The instantiation of a `sizeof...` expression [[expr.sizeof]] produces
an integral constant containing the number of elements in the pack it
expands.

The instantiation of a *fold-expression* produces:

- `((`E₁ *op* E₂`)` *op* ⋯`)` *op* $\mathtt{E}_N$ for a unary left fold,
- E₁ *op* `(`⋯ *op* `(`$\mathtt{E}_{N-1}$ *op* $\mathtt{E}_N$`))` for a
  unary right fold,
- `(((`E *op* E₁`)` *op* E₂`)` *op* ⋯`)` *op* $\mathtt{E}_N$ for a
  binary left fold, and
- E₁ *op* `(`⋯ *op* `(`$\mathtt{E}_{N-1}$ *op* `(`$\mathtt{E}_{N}$ *op*
  E`)))` for a binary right fold.

In each case, *op* is the *fold-operator*, N is the number of elements
in the pack expansion parameters, and each Eᵢ is generated by
instantiating the pattern and replacing each pack expansion parameter
with its iᵗʰ element. For a binary fold-expression, E is generated by
instantiating the *cast-expression* that did not contain an unexpanded
pack.

[*Example 7*:

``` cpp
template<typename ...Args>
  bool all(Args ...args) { return (... && args); }

bool b = all(true, true, true, false);
```

Within the instantiation of `all`, the returned expression expands to
`((true && true) && true) && false`, which evaluates to `false`.

— *end example*]

If N is zero for a unary fold-expression, the value of the expression is
shown in [[temp.fold.empty]]; if the operator is not listed in
[[temp.fold.empty]], the instantiation is ill-formed.

**Table: Value of folding empty sequences**

| Operator | Value when pack is empty |
| -------- | ------------------------ |
| `&&`     | `true`                   |
| `||`     | `false`                  |
| `,`      | `void()`                 |


### Friends <a id="temp.friend">[[temp.friend]]</a>

A friend of a class or class template can be a function template or
class template, a specialization of a function template or class
template, or a non-template function or class. For a friend function
declaration that is not a template declaration:

- if the name of the friend is a qualified or unqualified *template-id*,
  the friend declaration refers to a specialization of a function
  template, otherwise,
- if the name of the friend is a *qualified-id* and a matching
  non-template function is found in the specified class or namespace,
  the friend declaration refers to that function, otherwise,
- if the name of the friend is a *qualified-id* and a matching function
  template is found in the specified class or namespace, the friend
  declaration refers to the deduced specialization of that function
  template [[temp.deduct.decl]], otherwise,
- the name shall be an *unqualified-id* that declares (or redeclares) a
  non-template function.

[*Example 1*:

``` cpp
template<class T> class task;
template<class T> task<T>* preempt(task<T>*);

template<class T> class task {
  friend void next_time();
  friend void process(task<T>*);
  friend task<T>* preempt<T>(task<T>*);
  template<class C> friend int func(C);

  friend class task<int>;
  template<class P> friend class frd;
};
```

Here, each specialization of the `task` class template has the function
`next_time` as a friend; because `process` does not have explicit
*template-argument*s, each specialization of the `task` class template
has an appropriately typed function `process` as a friend, and this
friend is not a function template specialization; because the friend
`preempt` has an explicit *template-argument* `T`, each specialization
of the `task` class template has the appropriate specialization of the
function template `preempt` as a friend; and each specialization of the
`task` class template has all specializations of the function template
`func` as friends. Similarly, each specialization of the `task` class
template has the class template specialization `task<int>` as a friend,
and has all specializations of the class template `frd` as friends.

— *end example*]

A friend template may be declared within a class or class template. A
friend function template may be defined within a class or class
template, but a friend class template may not be defined in a class or
class template. In these cases, all specializations of the friend class
or friend function template are friends of the class or class template
granting friendship.

[*Example 2*:

``` cpp
class A {
  template<class T> friend class B;                 // OK
  template<class T> friend void f(T){ ... }   // OK
};
```

— *end example*]

A template friend declaration specifies that all specializations of that
template, whether they are implicitly instantiated [[temp.inst]],
partially specialized [[temp.class.spec]] or explicitly specialized
[[temp.expl.spec]], are friends of the class containing the template
friend declaration.

[*Example 3*:

``` cpp
class X {
  template<class T> friend struct A;
  class Y { };
};

template<class T> struct A { X::Y ab; };            // OK
template<class T> struct A<T*> { X::Y ab; };        // OK
```

— *end example*]

A template friend declaration may declare a member of a dependent type
to be a friend. The friend declaration shall declare a function or
specify a type with an *elaborated-type-specifier*, in either case with
a *nested-name-specifier* ending with a *simple-template-id*, *C*, whose
*template-name* names a class template. The template parameters of the
template friend declaration shall be deducible from *C* (
[[temp.deduct.type]]). In this case, a member of a specialization *S* of
the class template is a friend of the class granting friendship if
deduction of the template parameters of *C* from *S* succeeds, and
substituting the deduced template arguments into the friend declaration
produces a declaration that would be a valid redeclaration of the member
of the specialization.

[*Example 4*:

``` cpp
template<class T> struct A {
  struct B { };
  void f();
  struct D {
    void g();
  };
  T h();
  template<T U> T i();
};
template<> struct A<int> {
  struct B { };
  int f();
  struct D {
    void g();
  };
  template<int U> int i();
};
template<> struct A<float*> {
  int *h();
};

class C {
  template<class T> friend struct A<T>::B;      // grants friendship to A<int>::B even though
                                                // it is not a specialization of A<T>::B
  template<class T> friend void A<T>::f();      // does not grant friendship to A<int>::f()
                                                // because its return type does not match
  template<class T> friend void A<T>::D::g();   // error: A<T>::D does not end with a simple-template-id
  template<class T> friend int *A<T*>::h();     // grants friendship to A<int*>::h() and A<float*>::h()
  template<class T> template<T U>               // grants friendship to instantiations of A<T>::i() and
    friend T A<T>::i();                         // to A<int>::i(), and thereby to all specializations
};                                              // of those function templates
```

— *end example*]

[*Note 1*: A friend declaration may first declare a member of an
enclosing namespace scope [[temp.inject]]. — *end note*]

A friend template shall not be declared in a local class.

Friend declarations shall not declare partial specializations.

[*Example 5*:

``` cpp
template<class T> class A { };
class X {
  template<class T> friend class A<T*>;         // error
};
```

— *end example*]

When a friend declaration refers to a specialization of a function
template, the function parameter declarations shall not include default
arguments, nor shall the `inline`, `constexpr`, or `consteval`
specifiers be used in such a declaration.

A non-template friend declaration with a *requires-clause* shall be a
definition. A friend function template with a constraint that depends on
a template parameter from an enclosing template shall be a definition.
Such a constrained friend function or function template declaration does
not declare the same function or function template as a declaration in
any other scope.

### Class template partial specializations <a id="temp.class.spec">[[temp.class.spec]]</a>

A *primary class template* declaration is one in which the class
template name is an identifier. A template declaration in which the
class template name is a *simple-template-id* is a *partial
specialization* of the class template named in the *simple-template-id*.
A partial specialization of a class template provides an alternative
definition of the template that is used instead of the primary
definition when the arguments in a specialization match those given in
the partial specialization [[temp.class.spec.match]]. The primary
template shall be declared before any specializations of that template.
A partial specialization shall be declared before the first use of a
class template specialization that would make use of the partial
specialization as the result of an implicit or explicit instantiation in
every translation unit in which such a use occurs; no diagnostic is
required.

Each class template partial specialization is a distinct template and
definitions shall be provided for the members of a template partial
specialization [[temp.class.spec.mfunc]].

[*Example 1*:

``` cpp
template<class T1, class T2, int I> class A             { };
template<class T, int I>            class A<T, T*, I>   { };
template<class T1, class T2, int I> class A<T1*, T2, I> { };
template<class T>                   class A<int, T*, 5> { };
template<class T1, class T2, int I> class A<T1, T2*, I> { };
```

The first declaration declares the primary (unspecialized) class
template. The second and subsequent declarations declare partial
specializations of the primary template.

— *end example*]

A class template partial specialization may be constrained [[temp.pre]].

[*Example 2*:

``` cpp
template<typename T> concept C = true;

template<typename T> struct X { };
template<typename T> struct X<T*> { };          // #1
template<C T> struct X<T> { };                  // #2
```

Both partial specializations are more specialized than the primary
template. \#1 is more specialized because the deduction of its template
arguments from the template argument list of the class template
specialization succeeds, while the reverse does not. \#2 is more
specialized because the template arguments are equivalent, but the
partial specialization is more constrained [[temp.constr.order]].

— *end example*]

The template parameters are specified in the angle bracket enclosed list
that immediately follows the keyword `template`. For partial
specializations, the template argument list is explicitly written
immediately following the class template name. For primary templates,
this list is implicitly described by the template parameter list.
Specifically, the order of the template arguments is the sequence in
which they appear in the template parameter list.

[*Example 3*: The template argument list for the primary template in
the example above is `<T1,` `T2,` `I>`. — *end example*]

[*Note 1*:

The template argument list cannot be specified in the primary template
declaration. For example,

``` cpp
template<class T1, class T2, int I>
class A<T1, T2, I> { };                         // error
```

— *end note*]

A class template partial specialization may be declared in any scope in
which the corresponding primary template may be defined (
[[namespace.memdef]], [[class.mem]], [[temp.mem]]).

[*Example 4*:

``` cpp
template<class T> struct A {
  struct C {
    template<class T2> struct B { };
    template<class T2> struct B<T2**> { };      // partial specialization #1
  };
};

// partial specialization of A<T>::C::B<T2>
template<class T> template<class T2>
  struct A<T>::C::B<T2*> { };                   // #2

A<short>::C::B<int*> absip;                     // uses partial specialization #2
```

— *end example*]

Partial specialization declarations themselves are not found by name
lookup. Rather, when the primary template name is used, any
previously-declared partial specializations of the primary template are
also considered. One consequence is that a *using-declaration* which
refers to a class template does not restrict the set of partial
specializations which may be found through the *using-declaration*.

[*Example 5*:

``` cpp
namespace N {
  template<class T1, class T2> class A { };     // primary template
}

using N::A;                                     // refers to the primary template

namespace N {
  template<class T> class A<T, T*> { };         // partial specialization
}

A<int,int*> a;      // uses the partial specialization, which is found through the using-declaration
                    // which refers to the primary template
```

— *end example*]

A non-type argument is non-specialized if it is the name of a non-type
parameter. All other non-type arguments are specialized.

Within the argument list of a class template partial specialization, the
following restrictions apply:

- The type of a template parameter corresponding to a specialized
  non-type argument shall not be dependent on a parameter of the
  specialization.
  \[*Example 4*:
  ``` cpp
  template <class T, T t> struct C {};
  template <class T> struct C<T, 1>;              // error

  template< int X, int (*array_ptr)[X] > class A {};
  int array[5];
  template< int X > class A<X,&array> { };        // error
  ```

  — *end example*]
- The specialization shall be more specialized than the primary template
  [[temp.class.order]].
- The template parameter list of a specialization shall not contain
  default template argument values.[^8]
- An argument shall not contain an unexpanded pack. If an argument is a
  pack expansion [[temp.variadic]], it shall be the last argument in the
  template argument list.

The usual access checking rules do not apply to non-dependent names used
to specify template arguments of the *simple-template-id* of the partial
specialization.

[*Note 2*: The template arguments may be private types or objects that
would normally not be accessible. Dependent names cannot be checked when
declaring the partial specialization, but will be checked when
substituting into the partial specialization. — *end note*]

#### Matching of class template partial specializations <a id="temp.class.spec.match">[[temp.class.spec.match]]</a>

When a class template is used in a context that requires an
instantiation of the class, it is necessary to determine whether the
instantiation is to be generated using the primary template or one of
the partial specializations. This is done by matching the template
arguments of the class template specialization with the template
argument lists of the partial specializations.

- If exactly one matching specialization is found, the instantiation is
  generated from that specialization.
- If more than one matching specialization is found, the partial order
  rules [[temp.class.order]] are used to determine whether one of the
  specializations is more specialized than the others. If none of the
  specializations is more specialized than all of the other matching
  specializations, then the use of the class template is ambiguous and
  the program is ill-formed.
- If no matches are found, the instantiation is generated from the
  primary template.

A partial specialization matches a given actual template argument list
if the template arguments of the partial specialization can be deduced
from the actual template argument list [[temp.deduct]], and the deduced
template arguments satisfy the associated constraints of the partial
specialization, if any [[temp.constr.decl]].

[*Example 1*:

``` cpp
template<class T1, class T2, int I> class A             { };    // #1
template<class T, int I>            class A<T, T*, I>   { };    // #2
template<class T1, class T2, int I> class A<T1*, T2, I> { };    // #3
template<class T>                   class A<int, T*, 5> { };    // #4
template<class T1, class T2, int I> class A<T1, T2*, I> { };    // #5

A<int, int, 1>   a1;                    // uses #1
A<int, int*, 1>  a2;                    // uses #2, T is int, I is 1
A<int, char*, 5> a3;                    // uses #4, T is char
A<int, char*, 1> a4;                    // uses #5, T1 is int, T2 is char, I is 1
A<int*, int*, 2> a5;                    // ambiguous: matches #3 and #5
```

— *end example*]

[*Example 2*:

``` cpp
template<typename T> concept C = requires (T t) { t.f(); };

template<typename T> struct S { };      // #1
template<C T> struct S<T> { };          // #2

struct Arg { void f(); };

S<int> s1;                              // uses #1; the constraints of #2 are not satisfied
S<Arg> s2;                              // uses #2; both constraints are satisfied but #2 is more specialized
```

— *end example*]

If the template arguments of a partial specialization cannot be deduced
because of the structure of its *template-parameter-list* and the
*template-id*, the program is ill-formed.

[*Example 3*:

``` cpp
template <int I, int J> struct A {};
template <int I> struct A<I+5, I*2> {};     // error

template <int I> struct A<I, I> {};         // OK

template <int I, int J, int K> struct B {};
template <int I> struct B<I, I*2, 2> {};    // OK
```

— *end example*]

In a type name that refers to a class template specialization, (e.g.,
`A<int, int, 1>`) the argument list shall match the template parameter
list of the primary template. The template arguments of a specialization
are deduced from the arguments of the primary template.

#### Partial ordering of class template specializations <a id="temp.class.order">[[temp.class.order]]</a>

For two class template partial specializations, the first is *more
specialized* than the second if, given the following rewrite to two
function templates, the first function template is more specialized than
the second according to the ordering rules for function templates
[[temp.func.order]]:

- Each of the two function templates has the same template parameters
  and associated constraints [[temp.constr.decl]] as the corresponding
  partial specialization.
- Each function template has a single function parameter whose type is a
  class template specialization where the template arguments are the
  corresponding template parameters from the function template for each
  template argument in the *template-argument-list* of the
  *simple-template-id* of the partial specialization.

[*Example 1*:

``` cpp
template<int I, int J, class T> class X { };
template<int I, int J>          class X<I, J, int> { };         // #1
template<int I>                 class X<I, I, int> { };         // #2

template<int I0, int J0> void f(X<I0, J0, int>);                // A
template<int I0>         void f(X<I0, I0, int>);                // B

template <auto v>    class Y { };
template <auto* p>   class Y<p> { };                            // #3
template <auto** pp> class Y<pp> { };                           // #4

template <auto* p0>   void g(Y<p0>);                            // C
template <auto** pp0> void g(Y<pp0>);                           // D
```

According to the ordering rules for function templates, the function
template *B* is more specialized than the function template *A* and the
function template *D* is more specialized than the function template
*C*. Therefore, the partial specialization \#2 is more specialized than
the partial specialization \#1 and the partial specialization \#4 is
more specialized than the partial specialization \#3.

— *end example*]

[*Example 2*:

``` cpp
template<typename T> concept C = requires (T t) { t.f(); };
template<typename T> concept D = C<T> && requires (T t) { t.f(); };

template<typename T> class S { };
template<C T> class S<T> { };   // #1
template<D T> class S<T> { };   // #2

template<C T> void f(S<T>);     // A
template<D T> void f(S<T>);     // B
```

The partial specialization \#2 is more specialized than \#1 because `B`
is more specialized than `A`.

— *end example*]

#### Members of class template specializations <a id="temp.class.spec.mfunc">[[temp.class.spec.mfunc]]</a>

The template parameter list of a member of a class template partial
specialization shall match the template parameter list of the class
template partial specialization. The template argument list of a member
of a class template partial specialization shall match the template
argument list of the class template partial specialization. A class
template partial specialization is a distinct template. The members of
the class template partial specialization are unrelated to the members
of the primary template. Class template partial specialization members
that are used in a way that requires a definition shall be defined; the
definitions of members of the primary template are never used as
definitions for members of a class template partial specialization. An
explicit specialization of a member of a class template partial
specialization is declared in the same way as an explicit specialization
of the primary template.

[*Example 1*:

``` cpp
// primary class template
template<class T, int I> struct A {
  void f();
};

// member of primary class template
template<class T, int I> void A<T,I>::f() { }

// class template partial specialization
template<class T> struct A<T,2> {
  void f();
  void g();
  void h();
};

// member of class template partial specialization
template<class T> void A<T,2>::g() { }

// explicit specialization
template<> void A<char,2>::h() { }

int main() {
  A<char,0> a0;
  A<char,2> a2;
  a0.f();           // OK, uses definition of primary template's member
  a2.g();           // OK, uses definition of partial specialization's member
  a2.h();           // OK, uses definition of explicit specialization's member
  a2.f();           // error: no definition of f for A<T,2>; the primary template is not used here
}
```

— *end example*]

If a member template of a class template is partially specialized, the
member template partial specializations are member templates of the
enclosing class template; if the enclosing class template is
instantiated ([[temp.inst]], [[temp.explicit]]), a declaration for
every member template partial specialization is also instantiated as
part of creating the members of the class template specialization. If
the primary member template is explicitly specialized for a given
(implicit) specialization of the enclosing class template, the partial
specializations of the member template are ignored for this
specialization of the enclosing class template. If a partial
specialization of the member template is explicitly specialized for a
given (implicit) specialization of the enclosing class template, the
primary member template and its other partial specializations are still
considered for this specialization of the enclosing class template.

[*Example 2*:

``` cpp
template<class T> struct A {
  template<class T2> struct B {};                               // #1
  template<class T2> struct B<T2*> {};                          // #2
};

template<> template<class T2> struct A<short>::B {};            // #3

A<char>::B<int*>  abcip;                                        // uses #2
A<short>::B<int*> absip;                                        // uses #3
A<char>::B<int>  abci;                                          // uses #1
```

— *end example*]

### Function templates <a id="temp.fct">[[temp.fct]]</a>

A function template defines an unbounded set of related functions.

[*Example 1*:

A family of sort functions might be declared like this:

``` cpp
template<class T> class Array { };
template<class T> void sort(Array<T>&);
```

— *end example*]

A function template can be overloaded with other function templates and
with non-template functions [[dcl.fct]]. A non-template function is not
related to a function template (i.e., it is never considered to be a
specialization), even if it has the same name and type as a potentially
generated function template specialization.[^9]

#### Function template overloading <a id="temp.over.link">[[temp.over.link]]</a>

It is possible to overload function templates so that two different
function template specializations have the same type.

[*Example 1*:

``` cpp
// translation unit 1:
template<class T>
  void f(T*);
void g(int* p) {
  f(p); // calls f<int>(int*)
}
```

``` cpp
// translation unit 2:
template<class T>
  void f(T);
void h(int* p) {
  f(p); // calls f<int*>(int*)
}
```

— *end example*]

Such specializations are distinct functions and do not violate the
one-definition rule [[basic.def.odr]].

The signature of a function template is defined in [[intro.defs]]. The
names of the template parameters are significant only for establishing
the relationship between the template parameters and the rest of the
signature.

[*Note 1*:

Two distinct function templates may have identical function return types
and function parameter lists, even if overload resolution alone cannot
distinguish them.

``` cpp
template<class T> void f();
template<int I> void f();       // OK: overloads the first template
                                // distinguishable with an explicit template argument list
```

— *end note*]

When an expression that references a template parameter is used in the
function parameter list or the return type in the declaration of a
function template, the expression that references the template parameter
is part of the signature of the function template. This is necessary to
permit a declaration of a function template in one translation unit to
be linked with another declaration of the function template in another
translation unit and, conversely, to ensure that function templates that
are intended to be distinct are not linked with one another.

[*Example 2*:

``` cpp
template <int I, int J> A<I+J> f(A<I>, A<J>);   // #1
template <int K, int L> A<K+L> f(A<K>, A<L>);   // same as #1
template <int I, int J> A<I-J> f(A<I>, A<J>);   // different from #1
```

— *end example*]

[*Note 2*: Most expressions that use template parameters use non-type
template parameters, but it is possible for an expression to reference a
type parameter. For example, a template type parameter can be used in
the `sizeof` operator. — *end note*]

Two expressions involving template parameters are considered
*equivalent* if two function definitions containing the expressions
would satisfy the one-definition rule [[basic.def.odr]], except that the
tokens used to name the template parameters may differ as long as a
token used to name a template parameter in one expression is replaced by
another token that names the same template parameter in the other
expression. Two unevaluated operands that do not involve template
parameters are considered equivalent if two function definitions
containing the expressions would satisfy the one-definition rule, except
that the tokens used to name types and declarations may differ as long
as they name the same entities, and the tokens used to form concept-ids
may differ as long as the two *template-id*s are the same [[temp.type]].

[*Note 3*: For instance, `A<42>` and `A<40+2>` name the same
type. — *end note*]

Two *lambda-expression*s are never considered equivalent.

[*Note 4*: The intent is to avoid *lambda-expression*s appearing in the
signature of a function template with external linkage. — *end note*]

For determining whether two dependent names [[temp.dep]] are equivalent,
only the name itself is considered, not the result of name lookup in the
context of the template. If multiple declarations of the same function
template differ in the result of this name lookup, the result for the
first declaration is used.

[*Example 3*:

``` cpp
template <int I, int J> void f(A<I+J>);         // #1
template <int K, int L> void f(A<K+L>);         // same as #1

template <class T> decltype(g(T())) h();
int g(int);
template <class T> decltype(g(T())) h()         // redeclaration of h() uses the earlier lookup…
  { return g(T()); }                            // …{} although the lookup here does find g(int)
int i = h<int>();                               // template argument substitution fails; g(int)
                                                // was not in scope at the first declaration of h()

// ill-formed, no diagnostic required: the two expressions are functionally equivalent but not equivalent
template <int N> void foo(const char (*s)[([]{}, N)]);
template <int N> void foo(const char (*s)[([]{}, N)]);

// two different declarations because the non-dependent portions are not considered equivalent
template <class T> void spam(decltype([]{}) (*s)[sizeof(T)]);
template <class T> void spam(decltype([]{}) (*s)[sizeof(T)]);
```

— *end example*]

Two potentially-evaluated expressions involving template parameters that
are not equivalent are *functionally equivalent* if, for any given set
of template arguments, the evaluation of the expression results in the
same value. Two unevaluated operands that are not equivalent are
functionally equivalent if, for any given set of template arguments, the
expressions perform the same operations in the same order with the same
entities.

[*Note 5*: For instance, one could have redundant
parentheses. — *end note*]

Two *template-head*s are *equivalent* if their
*template-parameter-list*s have the same length, corresponding
*template-parameter*s are equivalent and are both declared with
*type-constraint*s that are equivalent if either *template-parameter* is
declared with a *type-constraint*, and if either *template-head* has a
*requires-clause*, they both have *requires-clause*s and the
corresponding *constraint-expression*s are equivalent. Two
*template-parameter*s are *equivalent* under the following conditions:

- they declare template parameters of the same kind,
- if either declares a template parameter pack, they both do,
- if they declare non-type template parameters, they have equivalent
  types ignoring the use of *type-constraint*s for placeholder types,
  and
- if they declare template template parameters, their template
  parameters are equivalent.

When determining whether types or *type-constraint*s are equivalent, the
rules above are used to compare expressions involving template
parameters. Two *template-head*s are *functionally equivalent* if they
accept and are satisfied by [[temp.constr.constr]] the same set of
template argument lists.

Two function templates are *equivalent* if they are declared in the same
scope, have the same name, have equivalent *template-head*s, and have
return types, parameter lists, and trailing *requires-clause*s (if any)
that are equivalent using the rules described above to compare
expressions involving template parameters. Two function templates are
*functionally equivalent* if they are declared in the same scope, have
the same name, accept and are satisfied by the same set of template
argument lists, and have return types and parameter lists that are
functionally equivalent using the rules described above to compare
expressions involving template parameters. If the validity or meaning of
the program depends on whether two constructs are equivalent, and they
are functionally equivalent but not equivalent, the program is
ill-formed, no diagnostic required.

[*Note 6*:

This rule guarantees that equivalent declarations will be linked with
one another, while not requiring implementations to use heroic efforts
to guarantee that functionally equivalent declarations will be treated
as distinct. For example, the last two declarations are functionally
equivalent and would cause a program to be ill-formed:

``` cpp
// guaranteed to be the same
template <int I> void f(A<I>, A<I+10>);
template <int I> void f(A<I>, A<I+10>);

// guaranteed to be different
template <int I> void f(A<I>, A<I+10>);
template <int I> void f(A<I>, A<I+11>);

// ill-formed, no diagnostic required
template <int I> void f(A<I>, A<I+10>);
template <int I> void f(A<I>, A<I+1+2+3+4>);
```

— *end note*]

#### Partial ordering of function templates <a id="temp.func.order">[[temp.func.order]]</a>

If a function template is overloaded, the use of a function template
specialization might be ambiguous because template argument deduction
[[temp.deduct]] may associate the function template specialization with
more than one function template declaration. *Partial ordering* of
overloaded function template declarations is used in the following
contexts to select the function template to which a function template
specialization refers:

- during overload resolution for a call to a function template
  specialization [[over.match.best]];
- when the address of a function template specialization is taken;
- when a placement operator delete that is a function template
  specialization is selected to match a placement operator new (
  [[basic.stc.dynamic.deallocation]], [[expr.new]]);
- when a friend function declaration [[temp.friend]], an explicit
  instantiation [[temp.explicit]] or an explicit specialization
  [[temp.expl.spec]] refers to a function template specialization.

Partial ordering selects which of two function templates is more
specialized than the other by transforming each template in turn (see
next paragraph) and performing template argument deduction using the
function type. The deduction process determines whether one of the
templates is more specialized than the other. If so, the more
specialized template is the one chosen by the partial ordering process.
If both deductions succeed, the partial ordering selects the more
constrained template (if one exists) as determined below.

To produce the transformed template, for each type, non-type, or
template template parameter (including template parameter packs
[[temp.variadic]] thereof) synthesize a unique type, value, or class
template respectively and substitute it for each occurrence of that
parameter in the function type of the template.

[*Note 1*: The type replacing the placeholder in the type of the value
synthesized for a non-type template parameter is also a unique
synthesized type. — *end note*]

Each function template M that is a member function is considered to have
a new first parameter of type X(M), described below, inserted in its
function parameter list. If exactly one of the function templates was
considered by overload resolution via a rewritten candidate
[[over.match.oper]] with a reversed order of parameters, then the order
of the function parameters in its transformed template is reversed. For
a function template M with cv-qualifiers cv that is a member of a class
A:

- The type X(M) is “rvalue reference to cv A” if the optional
  *ref-qualifier* of M is `&&` or if M has no *ref-qualifier* and the
  positionally-corresponding parameter of the other transformed template
  has rvalue reference type; if this determination depends recursively
  upon whether X(M) is an rvalue reference type, it is not considered to
  have rvalue reference type.
- Otherwise, X(M) is “lvalue reference to cv A”.

[*Note 2*: This allows a non-static member to be ordered with respect
to a non-member function and for the results to be equivalent to the
ordering of two equivalent non-members. — *end note*]

[*Example 1*:

``` cpp
struct A { };
template<class T> struct B {
  template<class R> int operator*(R&);              // #1
};

template<class T, class R> int operator*(T&, R&);   // #2

// The declaration of B::operator* is transformed into the equivalent of
// template<class R> int operator*(B<A>&, R&);\quad\quad\quad// #1a

int main() {
  A a;
  B<A> b;
  b * a;                                            // calls #1
}
```

— *end example*]

Using the transformed function template’s function type, perform type
deduction against the other template as described in 
[[temp.deduct.partial]].

[*Example 2*:

``` cpp
template<class T> struct A { A(); };

template<class T> void f(T);
template<class T> void f(T*);
template<class T> void f(const T*);

template<class T> void g(T);
template<class T> void g(T&);

template<class T> void h(const T&);
template<class T> void h(A<T>&);

void m() {
  const int* p;
  f(p);             // f(const T*) is more specialized than f(T) or f(T*)
  float x;
  g(x);             // ambiguous: g(T) or g(T&)
  A<int> z;
  h(z);             // overload resolution selects h(A<T>&)
  const A<int> z2;
  h(z2);            // h(const T&) is called because h(A<T>&) is not callable
}
```

— *end example*]

[*Note 3*:

Since, in a call context, such type deduction considers only parameters
for which there are explicit call arguments, some parameters are ignored
(namely, function parameter packs, parameters with default arguments,
and ellipsis parameters).

[*Example 3*:

``` cpp
template<class T> void f(T);                            // #1
template<class T> void f(T*, int=1);                    // #2
template<class T> void g(T);                            // #3
template<class T> void g(T*, ...);                      // #4
```

``` cpp
int main() {
  int* ip;
  f(ip);                                                // calls #2
  g(ip);                                                // calls #4
}
```

— *end example*]

[*Example 4*:

``` cpp
template<class T, class U> struct A { };

template<class T, class U> void f(U, A<U, T>* p = 0);   // #1
template<         class U> void f(U, A<U, U>* p = 0);   // #2
template<class T         > void g(T, T = T());          // #3
template<class T, class... U> void g(T, U ...);         // #4

void h() {
  f<int>(42, (A<int, int>*)0);                          // calls #2
  f<int>(42);                                           // error: ambiguous
  g(42);                                                // error: ambiguous
}
```

— *end example*]

[*Example 5*:

``` cpp
template<class T, class... U> void f(T, U...);          // #1
template<class T            > void f(T);                // #2
template<class T, class... U> void g(T*, U...);         // #3
template<class T            > void g(T);                // #4

void h(int i) {
  f(&i);                                                // OK: calls #2
  g(&i);                                                // OK: calls #3
}
```

— *end example*]

— *end note*]

If deduction against the other template succeeds for both transformed
templates, constraints can be considered as follows:

- If their *template-parameter-list*s (possibly including
  *template-parameter*s invented for an abbreviated function template
  [[dcl.fct]]) or function parameter lists differ in length, neither
  template is more specialized than the other.
- Otherwise:
  - If exactly one of the templates was considered by overload
    resolution via a rewritten candidate with reversed order of
    parameters:
    - If, for either template, some of the template parameters are not
      deducible from their function parameters, neither template is more
      specialized than the other.
    - If there is either no reordering or more than one reordering of
      the associated *template-parameter-list* such that
      - the corresponding *template-parameter*s of the
        *template-parameter-list*s are equivalent and
      - the function parameters that positionally correspond between the
        two templates are of the same type,

      neither template is more specialized than the other.
  - Otherwise, if the corresponding *template-parameter*s of the
    *template-parameter-list*s are not equivalent [[temp.over.link]] or
    if the function parameters that positionally correspond between the
    two templates are not of the same type, neither template is more
    specialized than the other.
- Otherwise, if the context in which the partial ordering is done is
  that of a call to a conversion function and the return types of the
  templates are not the same, then neither template is more specialized
  than the other.
- Otherwise, if one template is more constrained than the other
  [[temp.constr.order]], the more constrained template is more
  specialized than the other.
- Otherwise, neither template is more specialized than the other.

[*Example 6*:

``` cpp
template <typename> constexpr bool True = true;
template <typename T> concept C = True<T>;

void f(C auto &, auto &) = delete;
template <C Q> void f(Q &, C auto &);

void g(struct A *ap, struct B *bp) {
  f(*ap, *bp);                  // OK: Can use different methods to produce template parameters
}

template <typename T, typename U> struct X {};

template <typename T, C U, typename V> bool operator==(X<T, U>, V) = delete;
template <C T, C U, C V>               bool operator==(T, X<U, V>);

void h() {
  X<void *, int>{} == 0;        // OK: Correspondence of [T, U, V] and [U, V, T]
}
```

— *end example*]

### Alias templates <a id="temp.alias">[[temp.alias]]</a>

A *template-declaration* in which the *declaration* is an
*alias-declaration* [[dcl.pre]] declares the *identifier* to be an
*alias template*. An alias template is a name for a family of types. The
name of the alias template is a *template-name*.

When a *template-id* refers to the specialization of an alias template,
it is equivalent to the associated type obtained by substitution of its
*template-argument*s for the *template-parameter*s in the
*defining-type-id* of the alias template.

[*Note 1*: An alias template name is never deduced. — *end note*]

[*Example 1*:

``` cpp
template<class T> struct Alloc { ... };
template<class T> using Vec = vector<T, Alloc<T>>;
Vec<int> v;         // same as vector<int, Alloc<int>{> v;}

template<class T>
  void process(Vec<T>& v)
  { ... }

template<class T>
  void process(vector<T, Alloc<T>>& w)
  { ... }     // error: redefinition

template<template<class> class TT>
  void f(TT<int>);

f(v);               // error: Vec not deduced

template<template<class,class> class TT>
  void g(TT<int, Alloc<int>>);
g(v);               // OK: TT = vector
```

— *end example*]

However, if the *template-id* is dependent, subsequent template argument
substitution still applies to the *template-id*.

[*Example 2*:

``` cpp
template<typename...> using void_t = void;
template<typename T> void_t<typename T::foo> f();
f<int>();           // error: int does not have a nested type foo
```

— *end example*]

The *defining-type-id* in an alias template declaration shall not refer
to the alias template being declared. The type produced by an alias
template specialization shall not directly or indirectly make use of
that specialization.

[*Example 3*:

``` cpp
template <class T> struct A;
template <class T> using B = typename A<T>::U;
template <class T> struct A {
  typedef B<T> U;
};
B<short> b;         // error: instantiation of B<short> uses own type via A<short>::U
```

— *end example*]

The type of a *lambda-expression* appearing in an alias template
declaration is different between instantiations of that template, even
when the *lambda-expression* is not dependent.

[*Example 4*:

``` cpp
template <class T>
  using A = decltype([] { });   // A<int> and A<char> refer to different closure types
```

— *end example*]

### Concept definitions <a id="temp.concept">[[temp.concept]]</a>

A *concept* is a template that defines constraints on its template
arguments.

``` bnf
concept-definition:
  concept concept-name '=' constraint-expression ';'
```

``` bnf
concept-name:
  identifier
```

A *concept-definition* declares a concept. Its *identifier* becomes a
*concept-name* referring to that concept within its scope.

[*Example 1*:

``` cpp
template<typename T>
concept C = requires(T x) {
  { x == x } -> std::convertible_to<bool>;
};

template<typename T>
  requires C<T>     // C constrains f1(T) in constraint-expression
T f1(T x) { return x; }

template<C T>       // C, as a type-constraint, constrains f2(T)
T f2(T x) { return x; }
```

— *end example*]

A *concept-definition* shall appear at namespace scope
[[basic.scope.namespace]].

A concept shall not have associated constraints [[temp.constr.decl]].

A concept is not instantiated [[temp.spec]].

[*Note 1*: A concept-id [[temp.names]] is evaluated as an expression. A
concept cannot be explicitly instantiated [[temp.explicit]], explicitly
specialized [[temp.expl.spec]], or partially specialized. — *end note*]

The *constraint-expression* of a *concept-definition* is an unevaluated
operand [[expr.context]].

The first declared template parameter of a concept definition is its
*prototype parameter*. A *type concept* is a concept whose prototype
parameter is a type *template-parameter*.

## Name resolution <a id="temp.res">[[temp.res]]</a>

Three kinds of names can be used within a template definition:

- The name of the template itself, and names declared within the
  template itself.
- Names dependent on a *template-parameter* [[temp.dep]].
- Names from scopes which are visible within the template definition.

A name used in a template declaration or definition and that is
dependent on a *template-parameter* is assumed not to name a type unless
the applicable name lookup finds a type name or the name is qualified by
the keyword `typename`.

[*Example 1*:

``` cpp
// no B declared here

class X;

template<class T> class Y {
  class Z;                      // forward declaration of member class

  void f() {
    X* a1;                      // declare pointer to X
    T* a2;                      // declare pointer to T
    Y* a3;                      // declare pointer to Y<T>
    Z* a4;                      // declare pointer to Z
    typedef typename T::A TA;
    TA* a5;                     // declare pointer to T's A
    typename T::A* a6;          // declare pointer to T's A
    T::A* a7;                   // error: no visible declaration of a7
                                // T::A is not a type name; multiplication of T::A by a7
    B* a8;                      // error: no visible declarations of B and a8
                                // B is not a type name; multiplication of B by a8
  }
};
```

— *end example*]

``` bnf
typename-specifier:
  typename nested-name-specifier identifier
  typename nested-name-specifier 'templateₒₚₜ' simple-template-id
```

A *typename-specifier* denotes the type or class template denoted by the
*simple-type-specifier* [[dcl.type.simple]] formed by omitting the
keyword `typename`. The usual qualified name lookup
[[basic.lookup.qual]] is used to find the *qualified-id* even in the
presence of `typename`.

[*Example 2*:

``` cpp
struct A {
  struct X { };
  int X;
};
struct B {
  struct X { };
};
template<class T> void f(T t) {
  typename T::X x;
}
void foo() {
  A a;
  B b;
  f(b);             // OK: T::X refers to B::X
  f(a);             // error: T::X refers to the data member A::X not the struct A::X
}
```

— *end example*]

A qualified name used as the name in a *class-or-decltype*
[[class.derived]] or an *elaborated-type-specifier* is implicitly
assumed to name a type, without the use of the `typename` keyword. In a
*nested-name-specifier* that immediately contains a
*nested-name-specifier* that depends on a template parameter, the
*identifier* or *simple-template-id* is implicitly assumed to name a
type, without the use of the `typename` keyword.

[*Note 1*: The `typename` keyword is not permitted by the syntax of
these constructs. — *end note*]

A *qualified-id* is assumed to name a type if

- it is a qualified name in a type-id-only context (see below), or
- it is a *decl-specifier* of the *decl-specifier-seq* of a
  - *simple-declaration* or a *function-definition* in namespace scope,
  - *member-declaration*,
  - *parameter-declaration* in a *member-declaration* [^10], unless that
    *parameter-declaration* appears in a default argument,
  - *parameter-declaration* in a *declarator* of a function or function
    template declaration whose *declarator-id* is qualified, unless that
    *parameter-declaration* appears in a default argument,
  - *parameter-declaration* in a *lambda-declarator* or
    *requirement-parameter-list*, unless that *parameter-declaration*
    appears in a default argument, or
  - *parameter-declaration* of a (non-type) *template-parameter*.

A qualified name is said to be in a *type-id-only context* if it appears
in a *type-id*, *new-type-id*, or *defining-type-id* and the smallest
enclosing *type-id*, *new-type-id*, or *defining-type-id* is a
*new-type-id*, *defining-type-id*, *trailing-return-type*, default
argument of a *type-parameter* of a template, or *type-id* of a
`static_cast`, `const_cast`, `reinterpret_cast`, or `dynamic_cast`.

[*Example 3*:

``` cpp
template<class T> T::R f();             // OK, return type of a function declaration at global scope
template<class T> void f(T::R);         // ill-formed, no diagnostic required: attempt to declare
                                        // a void variable template
template<class T> struct S {
  using Ptr = PtrTraits<T>::Ptr;        // OK, in a defining-type-id
  T::R f(T::P p) {                      // OK, class scope
    return static_cast<T::R>(p);        // OK, type-id of a static_cast
  }
  auto g() -> S<T*>::Ptr;               // OK, trailing-return-type
};
template<typename T> void f() {
  void (*pf)(T::X);                     // variable pf of type void* initialized with T::X
  void g(T::X);                         // error: T::X at block scope does not denote a type
                                        // (attempt to declare a void variable)
}
```

— *end example*]

A *qualified-id* that refers to a member of an unknown specialization,
that is not prefixed by `typename`, and that is not otherwise assumed to
name a type (see above) denotes a non-type.

[*Example 4*:

``` cpp
template <class T> void f(int i) {
  T::x * i;         // expression, not the declaration of a variable i
}

struct Foo {
  typedef int x;
};

struct Bar {
  static int const x = 5;
};

int main() {
  f<Bar>(1);        // OK
  f<Foo>(1);        // error: Foo::x is a type
}
```

— *end example*]

Within the definition of a class template or within the definition of a
member of a class template following the *declarator-id*, the keyword
`typename` is not required when referring to a member of the current
instantiation [[temp.dep.type]].

[*Example 5*:

``` cpp
template<class T> struct A {
  typedef int B;
  B b;              // OK, no typename required
};
```

— *end example*]

The validity of a template may be checked prior to any instantiation.

[*Note 2*: Knowing which names are type names allows the syntax of
every template to be checked in this way. — *end note*]

The program is ill-formed, no diagnostic required, if:

- no valid specialization can be generated for a template or a
  substatement of a constexpr if statement [[stmt.if]] within a template
  and the template is not instantiated, or
- no substitution of template arguments into a *type-constraint* or
  *requires-clause* would result in a valid expression, or
- every valid specialization of a variadic template requires an empty
  template parameter pack, or
- a hypothetical instantiation of a template immediately following its
  definition would be ill-formed due to a construct that does not depend
  on a template parameter, or
- the interpretation of such a construct in the hypothetical
  instantiation is different from the interpretation of the
  corresponding construct in any actual instantiation of the template.
  \[*Note 1*:
  This can happen in situations including the following:
  - a type used in a non-dependent name is incomplete at the point at
    which a template is defined but is complete at the point at which an
    instantiation is performed, or
  - lookup for a name in the template definition found a
    *using-declaration*, but the lookup in the corresponding scope in
    the instantiation does not find any declarations because the
    *using-declaration* was a pack expansion and the corresponding pack
    is empty, or
  - an instantiation uses a default argument or default template
    argument that had not been defined at the point at which the
    template was defined, or
  - constant expression evaluation [[expr.const]] within the template
    instantiation uses
    - the value of a const object of integral or unscoped enumeration
      type or
    - the value of a `constexpr` object or
    - the value of a reference or
    - the definition of a constexpr function,

    and that entity was not defined when the template was defined, or
  - a class template specialization or variable template specialization
    that is specified by a non-dependent *simple-template-id* is used by
    the template, and either it is instantiated from a partial
    specialization that was not defined when the template was defined or
    it names an explicit specialization that was not declared when the
    template was defined.

  — *end note*]

Otherwise, no diagnostic shall be issued for a template for which a
valid specialization can be generated.

[*Note 3*: If a template is instantiated, errors will be diagnosed
according to the other rules in this document. Exactly when these errors
are diagnosed is a quality of implementation issue. — *end note*]

[*Example 6*:

``` cpp
int j;
template<class T> class X {
  void f(T t, int i, char* p) {
    t = i;          // diagnosed if X::f is instantiated, and the assignment to t is an error
    p = i;          // may be diagnosed even if X::f is not instantiated
    p = j;          // may be diagnosed even if X::f is not instantiated
  }
  void g(T t) {
    +;              // may be diagnosed even if X::g is not instantiated
  }
};

template<class... T> struct A {
  void operator++(int, T... t);                     // error: too many parameters
};
template<class... T> union X : T... { };            // error: union with base class
template<class... T> struct A : T...,  T... { };    // error: duplicate base class
```

— *end example*]

When looking for the declaration of a name used in a template
definition, the usual lookup rules ([[basic.lookup.unqual]],
[[basic.lookup.argdep]]) are used for non-dependent names. The lookup of
names dependent on the template parameters is postponed until the actual
template argument is known [[temp.dep]].

[*Example 7*:

``` cpp
#include <iostream>
using namespace std;

template<class T> class Set {
  T* p;
  int cnt;
public:
  Set();
  Set<T>(const Set<T>&);
  void printall() {
    for (int i = 0; i<cnt; i++)
      cout << p[i] << '\n';
  }
};
```

In the example, `i` is the local variable `i` declared in `printall`,
`cnt` is the member `cnt` declared in `Set`, and `cout` is the standard
output stream declared in `iostream`. However, not every declaration can
be found this way; the resolution of some names must be postponed until
the actual *template-argument*s are known. For example, even though the
name `operator<<` is known within the definition of `printall()` and a
declaration of it can be found in `<iostream>`, the actual declaration
of `operator<<` needed to print `p[i]` cannot be known until it is known
what type `T` is [[temp.dep]].

— *end example*]

If a name does not depend on a *template-parameter* (as defined in 
[[temp.dep]]), a declaration (or set of declarations) for that name
shall be in scope at the point where the name appears in the template
definition; the name is bound to the declaration (or declarations) found
at that point and this binding is not affected by declarations that are
visible at the point of instantiation.

[*Example 8*:

``` cpp
void f(char);

template<class T> void g(T t) {
  f(1);             // f(char)
  f(T(1));          // dependent
  f(t);             // dependent
  dd++;             // not dependent; error: declaration for dd not found
}

enum E { e };
void f(E);

double dd;
void h() {
  g(e);             // will cause one call of f(char) followed by two calls of f(E)
  g('a');           // will cause three calls of f(char)
}
```

— *end example*]

[*Note 4*: For purposes of name lookup, default arguments and
*noexcept-specifier*s of function templates and default arguments and
*noexcept-specifier*s of member functions of class templates are
considered definitions [[temp.decls]]. — *end note*]

### Locally declared names <a id="temp.local">[[temp.local]]</a>

Like normal (non-template) classes, class templates have an
injected-class-name [[class.pre]]. The injected-class-name can be used
as a *template-name* or a *type-name*. When it is used with a
*template-argument-list*, as a *template-argument* for a template
*template-parameter*, or as the final identifier in the
*elaborated-type-specifier* of a friend class template declaration, it
is a *template-name* that refers to the class template itself.
Otherwise, it is a *type-name* equivalent to the *template-name*
followed by the *template-parameter*s of the class template enclosed in
`<>`.

Within the scope of a class template specialization or partial
specialization, when the injected-class-name is used as a *type-name*,
it is equivalent to the *template-name* followed by the
*template-argument*s of the class template specialization or partial
specialization enclosed in `<>`.

[*Example 1*:

``` cpp
template<template<class> class T> class A { };
template<class T> class Y;
template<> class Y<int> {
  Y* p;                                 // meaning Y<int>
  Y<char>* q;                           // meaning Y<char>
  A<Y>* a;                              // meaning A<::Y>
  class B {
    template<class> friend class Y;     // meaning ::Y
  };
};
```

— *end example*]

The injected-class-name of a class template or class template
specialization can be used as either a *template-name* or a *type-name*
wherever it is in scope.

[*Example 2*:

``` cpp
template <class T> struct Base {
  Base* p;
};

template <class T> struct Derived: public Base<T> {
  typename Derived::Base* p;            // meaning Derived::Base<T>
};

template<class T, template<class> class U = T::template Base> struct Third { };
Third<Derived<int> > t;                 // OK: default argument uses injected-class-name as a template
```

— *end example*]

A lookup that finds an injected-class-name [[class.member.lookup]] can
result in an ambiguity in certain cases (for example, if it is found in
more than one base class). If all of the injected-class-names that are
found refer to specializations of the same class template, and if the
name is used as a *template-name*, the reference refers to the class
template itself and not a specialization thereof, and is not ambiguous.

[*Example 3*:

``` cpp
template <class T> struct Base { };
template <class T> struct Derived: Base<int>, Base<char> {
  typename Derived::Base b;             // error: ambiguous
  typename Derived::Base<double> d;     // OK
};
```

— *end example*]

When the normal name of the template (i.e., the name from the enclosing
scope, not the injected-class-name) is used, it always refers to the
class template itself and not a specialization of the template.

[*Example 4*:

``` cpp
template<class T> class X {
  X* p;                                 // meaning X<T>
  X<T>* p2;
  X<int>* p3;
  ::X* p4;                              // error: missing template argument list
                                        // ::X does not refer to the injected-class-name
};
```

— *end example*]

The name of a *template-parameter* shall not be redeclared within its
scope (including nested scopes). A *template-parameter* shall not have
the same name as the template name.

[*Example 5*:

``` cpp
template<class T, int i> class Y {
  int T;                                // error: template-parameter redeclared
  void f() {
    char T;                             // error: template-parameter redeclared
  }
};

template<class X> class X;              // error: template-parameter redeclared
```

— *end example*]

In the definition of a member of a class template that appears outside
of the class template definition, the name of a member of the class
template hides the name of a *template-parameter* of any enclosing class
templates (but not a *template-parameter* of the member if the member is
a class or function template).

[*Example 6*:

``` cpp
template<class T> struct A {
  struct B { ... };
  typedef void C;
  void f();
  template<class U> void g(U);
};

template<class B> void A<B>::f() {
  B b;              // A's B, not the template parameter
}

template<class B> template<class C> void A<B>::g(C) {
  B b;              // A's B, not the template parameter
  C c;              // the template parameter C, not A's C
}
```

— *end example*]

In the definition of a member of a class template that appears outside
of the namespace containing the class template definition, the name of a
*template-parameter* hides the name of a member of this namespace.

[*Example 7*:

``` cpp
namespace N {
  class C { };
  template<class T> class B {
    void f(T);
  };
}
template<class C> void N::B<C>::f(C) {
  C b;              // C is the template parameter, not N::C
}
```

— *end example*]

In the definition of a class template or in the definition of a member
of such a template that appears outside of the template definition, for
each non-dependent base class [[temp.dep.type]], if the name of the base
class or the name of a member of the base class is the same as the name
of a *template-parameter*, the base class name or member name hides the
*template-parameter* name [[basic.scope.hiding]].

[*Example 8*:

``` cpp
struct A {
  struct B { ... };
  int a;
  int Y;
};

template<class B, class a> struct X : A {
  B b;              // A's B
  a b;              // error: A's a isn't a type name
};
```

— *end example*]

### Dependent names <a id="temp.dep">[[temp.dep]]</a>

Inside a template, some constructs have semantics which may differ from
one instantiation to another. Such a construct *depends* on the template
parameters. In particular, types and expressions may depend on the type
and/or value of template parameters (as determined by the template
arguments) and this determines the context for name lookup for certain
names. An expression may be *type-dependent* (that is, its type may
depend on a template parameter) or *value-dependent* (that is, its value
when evaluated as a constant expression [[expr.const]] may depend on a
template parameter) as described in this subclause.

In an expression of the form:

``` bnf
postfix-expression '(' expression-listₒₚₜ ')'
```

where the *postfix-expression* is an *unqualified-id*, the
*unqualified-id* denotes a *dependent name* if

- any of the expressions in the *expression-list* is a pack expansion
  [[temp.variadic]],
- any of the expressions or *braced-init-list*s in the *expression-list*
  is type-dependent [[temp.dep.expr]], or
- the *unqualified-id* is a *template-id* in which any of the template
  arguments depends on a template parameter.

If an operand of an operator is a type-dependent expression, the
operator also denotes a dependent name.

[*Note 1*: Such names are unbound and are looked up at the point of the
template instantiation [[temp.point]] in both the context of the
template definition and the context of the point of instantiation
[[temp.dep.candidate]]. — *end note*]

[*Example 1*:

``` cpp
template<class T> struct X : B<T> {
  typename T::A* pa;
  void f(B<T>* pb) {
    static int i = B<T>::i;
    pb->j++;
  }
};
```

The base class name `B<T>`, the type name `T::A`, the names `B<T>::i`
and `pb->j` explicitly depend on the *template-parameter*.

— *end example*]

In the definition of a class or class template, the scope of a dependent
base class [[temp.dep.type]] is not examined during unqualified name
lookup either at the point of definition of the class template or member
or during an instantiation of the class template or member.

[*Example 2*:

``` cpp
typedef double A;
template<class T> class B {
  typedef int A;
};
template<class T> struct X : B<T> {
  A a;              // a has type double
};
```

The type name `A` in the definition of `X<T>` binds to the typedef name
defined in the global namespace scope, not to the typedef name defined
in the base class `B<T>`.

— *end example*]

[*Example 3*:

``` cpp
struct A {
  struct B { ... };
  int a;
  int Y;
};

int a;

template<class T> struct Y : T {
  struct B { ... };
  B b;                          // The B defined in Y
  void f(int i) { a = i; }      // ::a
  Y* p;                         // Y<T>
};

Y<A> ya;
```

The members `A::B`, `A::a`, and `A::Y` of the template argument `A` do
not affect the binding of names in `Y<A>`.

— *end example*]

#### Dependent types <a id="temp.dep.type">[[temp.dep.type]]</a>

A name refers to the *current instantiation* if it is

- in the definition of a class template, a nested class of a class
  template, a member of a class template, or a member of a nested class
  of a class template, the injected-class-name [[class.pre]] of the
  class template or nested class,
- in the definition of a primary class template or a member of a primary
  class template, the name of the class template followed by the
  template argument list of the primary template (as described below)
  enclosed in `<>` (or an equivalent template alias specialization),
- in the definition of a nested class of a class template, the name of
  the nested class referenced as a member of the current instantiation,
  or
- in the definition of a partial specialization or a member of a partial
  specialization, the name of the class template followed by the
  template argument list of the partial specialization enclosed in `<>`
  (or an equivalent template alias specialization). If the nᵗʰ template
  parameter is a template parameter pack, the nᵗʰ template argument is a
  pack expansion [[temp.variadic]] whose pattern is the name of the
  template parameter pack.

The template argument list of a primary template is a template argument
list in which the nᵗʰ template argument has the value of the nᵗʰ
template parameter of the class template. If the nᵗʰ template parameter
is a template parameter pack [[temp.variadic]], the nᵗʰ template
argument is a pack expansion [[temp.variadic]] whose pattern is the name
of the template parameter pack.

A template argument that is equivalent to a template parameter can be
used in place of that template parameter in a reference to the current
instantiation. For a template *type-parameter*, a template argument is
equivalent to a template parameter if it denotes the same type. For a
non-type template parameter, a template argument is equivalent to a
template parameter if it is an *identifier* that names a variable that
is equivalent to the template parameter. A variable is equivalent to a
template parameter if

- it has the same type as the template parameter (ignoring
  cv-qualification) and
- its initializer consists of a single *identifier* that names the
  template parameter or, recursively, such a variable.

[*Note 1*: Using a parenthesized variable name breaks the
equivalence. — *end note*]

[*Example 1*:

``` cpp
template <class T> class A {
  A* p1;                        // A is the current instantiation
  A<T>* p2;                     // A<T> is the current instantiation
  A<T*> p3;                     // A<T*> is not the current instantiation
  ::A<T>* p4;                   // ::A<T> is the current instantiation
  class B {
    B* p1;                      // B is the current instantiation
    A<T>::B* p2;                // A<T>::B is the current instantiation
    typename A<T*>::B* p3;      // A<T*>::B is not the current instantiation
  };
};

template <class T> class A<T*> {
  A<T*>* p1;                    // A<T*> is the current instantiation
  A<T>* p2;                     // A<T> is not the current instantiation
};

template <class T1, class T2, int I> struct B {
  B<T1, T2, I>* b1;             // refers to the current instantiation
  B<T2, T1, I>* b2;             // not the current instantiation
  typedef T1 my_T1;
  static const int my_I = I;
  static const int my_I2 = I+0;
  static const int my_I3 = my_I;
  static const long my_I4 = I;
  static const int my_I5 = (I);
  B<my_T1, T2, my_I>* b3;       // refers to the current instantiation
  B<my_T1, T2, my_I2>* b4;      // not the current instantiation
  B<my_T1, T2, my_I3>* b5;      // refers to the current instantiation
  B<my_T1, T2, my_I4>* b6;      // not the current instantiation
  B<my_T1, T2, my_I5>* b7;      // not the current instantiation
};
```

— *end example*]

A *dependent base class* is a base class that is a dependent type and is
not the current instantiation.

[*Note 2*:

A base class can be the current instantiation in the case of a nested
class naming an enclosing class as a base.

[*Example 2*:

``` cpp
template<class T> struct A {
  typedef int M;
  struct B {
    typedef void M;
    struct C;
  };
};

template<class T> struct A<T>::B::C : A<T> {
  M m;                          // OK, A<T>::M
};
```

— *end example*]

— *end note*]

A name is a *member of the current instantiation* if it is

- An unqualified name that, when looked up, refers to at least one
  member of a class that is the current instantiation or a non-dependent
  base class thereof. \[*Note 2*: This can only occur when looking up a
  name in a scope enclosed by the definition of a class
  template. — *end note*]
- A *qualified-id* in which the *nested-name-specifier* refers to the
  current instantiation and that, when looked up, refers to at least one
  member of a class that is the current instantiation or a non-dependent
  base class thereof. \[*Note 3*: If no such member is found, and the
  current instantiation has any dependent base classes, then the
  *qualified-id* is a member of an unknown specialization; see
  below. — *end note*]
- An *id-expression* denoting the member in a class member access
  expression [[expr.ref]] for which the type of the object expression is
  the current instantiation, and the *id-expression*, when looked up
  [[basic.lookup.classref]], refers to at least one member of a class
  that is the current instantiation or a non-dependent base class
  thereof. \[*Note 4*: If no such member is found, and the current
  instantiation has any dependent base classes, then the *id-expression*
  is a member of an unknown specialization; see below. — *end note*]

[*Example 3*:

``` cpp
template <class T> class A {
  static const int i = 5;
  int n1[i];                    // i refers to a member of the current instantiation
  int n2[A::i];                 // A::i refers to a member of the current instantiation
  int n3[A<T>::i];              // A<T>::i refers to a member of the current instantiation
  int f();
};

template <class T> int A<T>::f() {
  return i;                     // i refers to a member of the current instantiation
}
```

— *end example*]

A name is a *dependent member of the current instantiation* if it is a
member of the current instantiation that, when looked up, refers to at
least one member of a class that is the current instantiation.

A name is a *member of an unknown specialization* if it is

- A *qualified-id* in which the *nested-name-specifier* names a
  dependent type that is not the current instantiation.
- A *qualified-id* in which the *nested-name-specifier* refers to the
  current instantiation, the current instantiation has at least one
  dependent base class, and name lookup of the *qualified-id* does not
  find any member of a class that is the current instantiation or a
  non-dependent base class thereof.
- An *id-expression* denoting the member in a class member access
  expression [[expr.ref]] in which either
  - the type of the object expression is the current instantiation, the
    current instantiation has at least one dependent base class, and
    name lookup of the *id-expression* does not find a member of a class
    that is the current instantiation or a non-dependent base class
    thereof; or
  - the type of the object expression is not the current instantiation
    and the object expression is type-dependent.

If a *qualified-id* in which the *nested-name-specifier* refers to the
current instantiation is not a member of the current instantiation or a
member of an unknown specialization, the program is ill-formed even if
the template containing the *qualified-id* is not instantiated; no
diagnostic required. Similarly, if the *id-expression* in a class member
access expression for which the type of the object expression is the
current instantiation does not refer to a member of the current
instantiation or a member of an unknown specialization, the program is
ill-formed even if the template containing the member access expression
is not instantiated; no diagnostic required.

[*Example 4*:

``` cpp
template<class T> class A {
  typedef int type;
  void f() {
    A<T>::type i;               // OK: refers to a member of the current instantiation
    typename A<T>::other j;     // error: neither a member of the current instantiation nor
                                // a member of an unknown specialization
  }
};
```

— *end example*]

If, for a given set of template arguments, a specialization of a
template is instantiated that refers to a member of the current
instantiation with a *qualified-id* or class member access expression,
the name in the *qualified-id* or class member access expression is
looked up in the template instantiation context. If the result of this
lookup differs from the result of name lookup in the template definition
context, name lookup is ambiguous.

[*Example 5*:

``` cpp
struct A {
  int m;
};

struct B {
  int m;
};

template<typename T>
struct C : A, T {
  int f() { return this->m; }   // finds A::m in the template definition context
  int g() { return m; }         // finds A::m in the template definition context
};

template int C<B>::f();         // error: finds both A::m and B::m
template int C<B>::g();         // OK: transformation to class member access syntax
                                // does not occur in the template definition context; see~[class.mfct.non-static]
```

— *end example*]

A type is dependent if it is

- a template parameter,
- a member of an unknown specialization,
- a nested class or enumeration that is a dependent member of the
  current instantiation,
- a cv-qualified type where the cv-unqualified type is dependent,
- a compound type constructed from any dependent type,
- an array type whose element type is dependent or whose bound (if any)
  is value-dependent,
- a function type whose exception specification is value-dependent,
- denoted by a *simple-template-id* in which either the template name is
  a template parameter or any of the template arguments is a dependent
  type or an expression that is type-dependent or value-dependent or is
  a pack expansion \[*Note 5*: This includes an injected-class-name
  [[class.pre]] of a class template used without a
  *template-argument-list*. — *end note*] , or
- denoted by `decltype(`*expression*`)`, where *expression* is
  type-dependent [[temp.dep.expr]].

[*Note 3*: Because typedefs do not introduce new types, but instead
simply refer to other types, a name that refers to a typedef that is a
member of the current instantiation is dependent only if the type
referred to is dependent. — *end note*]

#### Type-dependent expressions <a id="temp.dep.expr">[[temp.dep.expr]]</a>

Except as described below, an expression is type-dependent if any
subexpression is type-dependent.

`this`

is type-dependent if the class type of the enclosing member function is
dependent [[temp.dep.type]].

An *id-expression* is type-dependent if it is not a concept-id and it
contains

- an *identifier* associated by name lookup with one or more
  declarations declared with a dependent type,
- an *identifier* associated by name lookup with a non-type
  *template-parameter* declared with a type that contains a placeholder
  type [[dcl.spec.auto]],
- an *identifier* associated by name lookup with a variable declared
  with a type that contains a placeholder type [[dcl.spec.auto]] where
  the initializer is type-dependent,
- an *identifier* associated by name lookup with one or more
  declarations of member functions of the current instantiation declared
  with a return type that contains a placeholder type,
- an *identifier* associated by name lookup with a structured binding
  declaration [[dcl.struct.bind]] whose *brace-or-equal-initializer* is
  type-dependent,
- the *identifier* `__func__` [[dcl.fct.def.general]], where any
  enclosing function is a template, a member of a class template, or a
  generic lambda,
- a *template-id* that is dependent,
- a *conversion-function-id* that specifies a dependent type, or
- a *nested-name-specifier* or a *qualified-id* that names a member of
  an unknown specialization;

or if it names a dependent member of the current instantiation that is a
static data member of type “array of unknown bound of `T`” for some `T`
[[temp.static]]. Expressions of the following forms are type-dependent
only if the type specified by the *type-id*, *simple-type-specifier* or
*new-type-id* is dependent, even if any subexpression is type-dependent:

``` bnf
simple-type-specifier '(' expression-listₒₚₜ ')'
'::'ₒₚₜ new new-placementₒₚₜ new-type-id new-initializerₒₚₜ
'::'ₒₚₜ new new-placementₒₚₜ '(' type-id ')' new-initializerₒₚₜ
dynamic_cast '<' type-id '>' '(' expression ')'
static_cast '<' type-id '>' '(' expression ')'
const_cast '<' type-id '>' '(' expression ')'
reinterpret_cast '<' type-id '>' '(' expression ')'
'(' type-id ')' cast-expression
```

Expressions of the following forms are never type-dependent (because the
type of the expression cannot be dependent):

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

[*Note 1*: For the standard library macro `offsetof`, see 
[[support.types]]. — *end note*]

A class member access expression [[expr.ref]] is type-dependent if the
expression refers to a member of the current instantiation and the type
of the referenced member is dependent, or the class member access
expression refers to a member of an unknown specialization.

[*Note 2*: In an expression of the form `x.y` or `xp->y` the type of
the expression is usually the type of the member `y` of the class of `x`
(or the class pointed to by `xp`). However, if `x` or `xp` refers to a
dependent type that is not the current instantiation, the type of `y` is
always dependent. If `x` or `xp` refers to a non-dependent type or
refers to the current instantiation, the type of `y` is the type of the
class member access expression. — *end note*]

A *braced-init-list* is type-dependent if any element is type-dependent
or is a pack expansion.

A *fold-expression* is type-dependent.

#### Value-dependent expressions <a id="temp.dep.constexpr">[[temp.dep.constexpr]]</a>

Except as described below, an expression used in a context where a
constant expression is required is value-dependent if any subexpression
is value-dependent.

An *id-expression* is value-dependent if:

- it is a concept-id and any of its arguments are dependent,
- it is type-dependent,
- it is the name of a non-type template parameter,
- it names a static data member that is a dependent member of the
  current instantiation and is not initialized in a *member-declarator*,
- it names a static member function that is a dependent member of the
  current instantiation, or
- it names a potentially-constant variable [[expr.const]] that is
  initialized with an expression that is value-dependent.

Expressions of the following form are value-dependent if the
*unary-expression* or *expression* is type-dependent or the *type-id* is
dependent:

``` bnf
sizeof unary-expression
sizeof '(' type-id ')'
typeid '(' expression ')'
typeid '(' type-id ')'
alignof '(' type-id ')'
noexcept '(' expression ')'
```

[*Note 1*: For the standard library macro `offsetof`, see 
[[support.types]]. — *end note*]

Expressions of the following form are value-dependent if either the
*type-id* or *simple-type-specifier* is dependent or the *expression* or
*cast-expression* is value-dependent:

``` bnf
simple-type-specifier '(' expression-listₒₚₜ ')'
static_cast '<' type-id '>' '(' expression ')'
const_cast '<' type-id '>' '(' expression ')'
reinterpret_cast '<' type-id '>' '(' expression ')'
'(' type-id ')' cast-expression
```

Expressions of the following form are value-dependent:

``` bnf
sizeof '...' '(' identifier ')'
fold-expression
```

An expression of the form `&`*qualified-id* where the *qualified-id*
names a dependent member of the current instantiation is
value-dependent. An expression of the form `&`*cast-expression* is also
value-dependent if evaluating *cast-expression* as a core constant
expression [[expr.const]] succeeds and the result of the evaluation
refers to a templated entity that is an object with static or thread
storage duration or a member function.

#### Dependent template arguments <a id="temp.dep.temp">[[temp.dep.temp]]</a>

A type *template-argument* is dependent if the type it specifies is
dependent.

A non-type *template-argument* is dependent if its type is dependent or
the constant expression it specifies is value-dependent.

Furthermore, a non-type *template-argument* is dependent if the
corresponding non-type *template-parameter* is of reference or pointer
type and the *template-argument* designates or points to a member of the
current instantiation or a member of a dependent type.

A template *template-argument* is dependent if it names a
*template-parameter* or is a *qualified-id* that refers to a member of
an unknown specialization.

### Non-dependent names <a id="temp.nondep">[[temp.nondep]]</a>

Non-dependent names used in a template definition are found using the
usual name lookup and bound at the point they are used.

[*Example 1*:

``` cpp
void g(double);
void h();

template<class T> class Z {
public:
  void f() {
    g(1);           // calls g(double)
    h++;            // ill-formed: cannot increment function; this could be diagnosed
                    // either here or at the point of instantiation
  }
};

void g(int);        // not in scope at the point of the template definition, not considered for the call g(1)
```

— *end example*]

### Dependent name resolution <a id="temp.dep.res">[[temp.dep.res]]</a>

#### Point of instantiation <a id="temp.point">[[temp.point]]</a>

For a function template specialization, a member function template
specialization, or a specialization for a member function or static data
member of a class template, if the specialization is implicitly
instantiated because it is referenced from within another template
specialization and the context from which it is referenced depends on a
template parameter, the point of instantiation of the specialization is
the point of instantiation of the enclosing specialization. Otherwise,
the point of instantiation for such a specialization immediately follows
the namespace scope declaration or definition that refers to the
specialization.

If a function template or member function of a class template is called
in a way which uses the definition of a default argument of that
function template or member function, the point of instantiation of the
default argument is the point of instantiation of the function template
or member function specialization.

For a *noexcept-specifier* of a function template specialization or
specialization of a member function of a class template, if the
*noexcept-specifier* is implicitly instantiated because it is needed by
another template specialization and the context that requires it depends
on a template parameter, the point of instantiation of the
*noexcept-specifier* is the point of instantiation of the specialization
that requires it. Otherwise, the point of instantiation for such a
*noexcept-specifier* immediately follows the namespace scope declaration
or definition that requires the *noexcept-specifier*.

For a class template specialization, a class member template
specialization, or a specialization for a class member of a class
template, if the specialization is implicitly instantiated because it is
referenced from within another template specialization, if the context
from which the specialization is referenced depends on a template
parameter, and if the specialization is not instantiated previous to the
instantiation of the enclosing template, the point of instantiation is
immediately before the point of instantiation of the enclosing template.
Otherwise, the point of instantiation for such a specialization
immediately precedes the namespace scope declaration or definition that
refers to the specialization.

If a virtual function is implicitly instantiated, its point of
instantiation is immediately following the point of instantiation of its
enclosing class template specialization.

An explicit instantiation definition is an instantiation point for the
specialization or specializations specified by the explicit
instantiation.

A specialization for a function template, a member function template, or
of a member function or static data member of a class template may have
multiple points of instantiations within a translation unit, and in
addition to the points of instantiation described above,

- for any such specialization that has a point of instantiation within
  the *declaration-seq* of the *translation-unit*, prior to the
  *private-module-fragment* (if any), the point after the
  *declaration-seq* of the *translation-unit* is also considered a point
  of instantiation, and
- for any such specialization that has a point of instantiation within
  the *private-module-fragment*, the end of the translation unit is also
  considered a point of instantiation.

A specialization for a class template has at most one point of
instantiation within a translation unit. A specialization for any
template may have points of instantiation in multiple translation units.
If two different points of instantiation give a template specialization
different meanings according to the one-definition rule
[[basic.def.odr]], the program is ill-formed, no diagnostic required.

#### Candidate functions <a id="temp.dep.candidate">[[temp.dep.candidate]]</a>

For a function call where the *postfix-expression* is a dependent name,
the candidate functions are found using the usual lookup rules from the
template definition context ([[basic.lookup.unqual]],
[[basic.lookup.argdep]]).

[*Note 1*: For the part of the lookup using associated namespaces
[[basic.lookup.argdep]], function declarations found in the template
instantiation context are found by this lookup, as described in
[[basic.lookup.argdep]]. — *end note*]

If the call would be ill-formed or would find a better match had the
lookup within the associated namespaces considered all the function
declarations with external linkage introduced in those namespaces in all
translation units, not just considering those declarations found in the
template definition and template instantiation contexts, then the
program has undefined behavior.

[*Example 1*:

Source file \`"X.h"\`

``` cpp
namespace Q {
  struct X { };
}
```

Source file \`"G.h"\`

``` cpp
namespace Q {
  void g_impl(X, X);
}
```

Module interface unit of \`M1\`

``` cpp
module;
#include "X.h"
#include "G.h"
export module M1;
export template<typename T>
void g(T t) {
  g_impl(t, Q::X{ });   // ADL in definition context finds Q::g_impl, g_impl not discarded
}
```

Module interface unit of \`M2\`

``` cpp
module;
#include "X.h"
export module M2;
import M1;
void h(Q::X x) {
   g(x);                // OK
}
```

— *end example*]

[*Example 2*:

Module interface unit of \`Std\`

``` cpp
export module Std;
export template<typename Iter>
void indirect_swap(Iter lhs, Iter rhs)
{
  swap(*lhs, *rhs);     // swap not found by unqualified lookup, can be found only via ADL
}
```

Module interface unit of \`M\`

``` cpp
export module M;
import Std;

struct S { /* ...*/ };
void swap(S&, S&);      // #1

void f(S* p, S* q)
{
  indirect_swap(p, q);  // finds #1 via ADL in instantiation context
}
```

— *end example*]

[*Example 3*:

Source file \`"X.h"\`

``` cpp
struct X { /* ... */ };
X operator+(X, X);
```

Module interface unit of \`F\`

``` cpp
export module F;
export template<typename T>
void f(T t) {
  t + t;
}
```

Module interface unit of \`M\`

``` cpp
module;
#include "X.h"
export module M;
import F;
void g(X x) {
  f(x);             // OK: instantiates f from F,
                    // operator+ is visible in instantiation context
}
```

— *end example*]

[*Example 4*:

Module interface unit of \`A\`

``` cpp
export module A;
export template<typename T>
void f(T t) {
  cat(t, t);            // #1
  dog(t, t);            // #2
}
```

Module interface unit of \`B\`

``` cpp
export module B;
import A;
export template<typename T, typename U>
void g(T t, U u) {
  f(t);
}
```

Source file \`"foo.h"\`, not an importable header

``` cpp
struct foo {
  friend int cat(foo, foo);
};
int dog(foo, foo);
```

Module interface unit of \`C1\`

``` cpp
module;
#include "foo.h"        // dog not referenced, discarded
export module C1;
import B;
export template<typename T>
void h(T t) {
  g(foo{ }, t);
}
```

Translation unit

``` cpp
import C1;
void i() {
   h(0);                // error: dog not found at #2
}
```

Importable header \`"bar.h"\`

``` cpp
struct bar {
  friend int cat(bar, bar);
};
int dog(bar, bar);
```

Module interface unit of \`C2\`

``` cpp
module;
#include "bar.h"        // imports header unit "bar.h"
export module C2;
import B;
export template<typename T>
void j(T t) {
  g(bar{ }, t);
}
```

Translation unit

``` cpp
import C2;
void k() {
   j(0);                // OK, dog found in instantiation context:
                        // visible at end of module interface unit of C2
}
```

— *end example*]

### Friend names declared within a class template <a id="temp.inject">[[temp.inject]]</a>

Friend classes or functions can be declared within a class template.
When a template is instantiated, the names of its friends are treated as
if the specialization had been explicitly declared at its point of
instantiation.

As with non-template classes, the names of namespace-scope friend
functions of a class template specialization are not visible during an
ordinary lookup unless explicitly declared at namespace scope
[[class.friend]]. Such names may be found under the rules for associated
classes [[basic.lookup.argdep]].[^11]

[*Example 1*:

``` cpp
template<typename T> struct number {
  number(int);
  friend number gcd(number x, number y) { return 0; };
};

void g() {
  number<double> a(3), b(4);
  a = gcd(a,b);     // finds gcd because number<double> is an associated class,
                    // making gcd visible in its namespace (global scope)
  b = gcd(3,4);     // error: gcd is not visible
}
```

— *end example*]

## Template instantiation and specialization <a id="temp.spec">[[temp.spec]]</a>

The act of instantiating a function, a variable, a class, a member of a
class template, or a member template is referred to as *template
instantiation*.

A function instantiated from a function template is called an
instantiated function. A class instantiated from a class template is
called an instantiated class. A member function, a member class, a
member enumeration, or a static data member of a class template
instantiated from the member definition of the class template is called,
respectively, an instantiated member function, member class, member
enumeration, or static data member. A member function instantiated from
a member function template is called an instantiated member function. A
member class instantiated from a member class template is called an
instantiated member class. A variable instantiated from a variable
template is called an instantiated variable. A static data member
instantiated from a static data member template is called an
instantiated static data member.

An explicit specialization may be declared for a function template, a
variable template, a class template, a member of a class template, or a
member template. An explicit specialization declaration is introduced by
`template<>`. In an explicit specialization declaration for a variable
template, a class template, a member of a class template or a class
member template, the name of the variable or class that is explicitly
specialized shall be a *simple-template-id*. In the explicit
specialization declaration for a function template or a member function
template, the name of the function or member function explicitly
specialized may be a *template-id*.

[*Example 1*:

``` cpp
template<class T = int> struct A {
  static int x;
};
template<class U> void g(U) { }

template<> struct A<double> { };        // specialize for T == double
template<> struct A<> { };              // specialize for T == int
template<> void g(char) { }             // specialize for U == char
                                        // U is deduced from the parameter type
template<> void g<int>(int) { }         // specialize for U == int
template<> int A<char>::x = 0;          // specialize for T == char

template<class T = int> struct B {
  static int x;
};
template<> int B<>::x = 1;              // specialize for T == int
```

— *end example*]

An instantiated template specialization can be either implicitly
instantiated [[temp.inst]] for a given argument list or be explicitly
instantiated [[temp.explicit]]. A *specialization* is a class, variable,
function, or class member that is either instantiated [[temp.inst]] from
a templated entity or is an explicit specialization [[temp.expl.spec]]
of a templated entity.

For a given template and a given set of *template-argument*s,

- an explicit instantiation definition shall appear at most once in a
  program,
- an explicit specialization shall be defined at most once in a program,
  as specified in [[basic.def.odr]], and
- both an explicit instantiation and a declaration of an explicit
  specialization shall not appear in a program unless the explicit
  instantiation follows a declaration of the explicit specialization.

An implementation is not required to diagnose a violation of this rule.

The usual access checking rules do not apply to names in a declaration
of an explicit instantiation or explicit specialization, with the
exception of names appearing in a function body, default argument,
base-clause, member-specification, enumerator-list, or static data
member or variable template initializer.

[*Note 1*: In particular, the template arguments and names used in the
function declarator (including parameter types, return types and
exception specifications) may be private types or objects that would
normally not be accessible. — *end note*]

Each class template specialization instantiated from a template has its
own copy of any static members.

[*Example 2*:

``` cpp
template<class T> class X {
  static T s;
};
template<class T> T X<T>::s = 0;
X<int> aa;
X<char*> bb;
```

`X<int>`

has a static member `s` of type `int` and `X<char*>` has a static member
`s` of type `char*`.

— *end example*]

If a function declaration acquired its function type through a dependent
type [[temp.dep.type]] without using the syntactic form of a function
declarator, the program is ill-formed.

[*Example 3*:

``` cpp
template<class T> struct A {
  static T t;
};
typedef int function();
A<function> a;      // error: would declare A<function>::t as a static member function
```

— *end example*]

### Implicit instantiation <a id="temp.inst">[[temp.inst]]</a>

A template specialization E is a *declared specialization* if there is a
reachable explicit instantiation definition [[temp.explicit]] or
explicit specialization declaration [[temp.expl.spec]] for E, or if
there is a reachable explicit instantiation declaration for E and E is
not

- an inline function,
- declared with a type deduced from its initializer or return value
  [[dcl.spec.auto]],
- a potentially-constant variable [[expr.const]], or
- a specialization of a templated class.

[*Note 1*: An implicit instantiation in an importing translation unit
cannot use names with internal linkage from an imported translation unit
[[basic.link]]. — *end note*]

Unless a class template specialization is a declared specialization, the
class template specialization is implicitly instantiated when the
specialization is referenced in a context that requires a
completely-defined object type or when the completeness of the class
type affects the semantics of the program.

[*Note 2*: In particular, if the semantics of an expression depend on
the member or base class lists of a class template specialization, the
class template specialization is implicitly generated. For instance,
deleting a pointer to class type depends on whether or not the class
declares a destructor, and a conversion between pointers to class type
depends on the inheritance relationship between the two classes
involved. — *end note*]

[*Example 1*:

``` cpp
template<class T> class B { ... };
template<class T> class D : public B<T> { ... };

void f(void*);
void f(B<int>*);

void g(D<int>* p, D<char>* pp, D<double>* ppp) {
  f(p);             // instantiation of D<int> required: call f(B<int>*)
  B<char>* q = pp;  // instantiation of D<char> required: convert D<char>* to B<char>*
  delete ppp;       // instantiation of D<double> required
}
```

— *end example*]

If a class template has been declared, but not defined, at the point of
instantiation [[temp.point]], the instantiation yields an incomplete
class type [[basic.types]].

[*Example 2*:

``` cpp
template<class T> class X;
X<char> ch;         // error: incomplete type X<char>
```

— *end example*]

[*Note 3*: Within a template declaration, a local class [[class.local]]
or enumeration and the members of a local class are never considered to
be entities that can be separately instantiated (this includes their
default arguments, *noexcept-specifier*s, and non-static data member
initializers, if any, but not their *type-constraint*s or
*requires-clause*s). As a result, the dependent names are looked up, the
semantic constraints are checked, and any templates used are
instantiated as part of the instantiation of the entity within which the
local class or enumeration is declared. — *end note*]

The implicit instantiation of a class template specialization causes

- the implicit instantiation of the declarations, but not of the
  definitions, of the non-deleted class member functions, member
  classes, scoped member enumerations, static data members, member
  templates, and friends; and
- the implicit instantiation of the definitions of deleted member
  functions, unscoped member enumerations, and member anonymous unions.

The implicit instantiation of a class template specialization does not
cause the implicit instantiation of default arguments or
*noexcept-specifier*s of the class member functions.

[*Example 3*:

``` cpp
template<class T>
struct C {
  void f() { T x; }
  void g() = delete;
};
C<void> c;                      // OK, definition of C<void>::f is not instantiated at this point
template<> void C<int>::g() { } // error: redefinition of C<int>::g
```

— *end example*]

However, for the purpose of determining whether an instantiated
redeclaration is valid according to  [[basic.def.odr]] and
[[class.mem]], a declaration that corresponds to a definition in the
template is considered to be a definition.

[*Example 4*:

``` cpp
template<class T, class U>
struct Outer {
  template<class X, class Y> struct Inner;
  template<class Y> struct Inner<T, Y>;         // #1a
  template<class Y> struct Inner<T, Y> { };     // #1b; OK: valid redeclaration of #1a
  template<class Y> struct Inner<U, Y> { };     // #2
};

Outer<int, int> outer;                          // error at #2
```

`Outer<int, int>::Inner<int, Y>` is redeclared at \#1b. (It is not
defined but noted as being associated with a definition in
`Outer<T, U>`.) \#2 is also a redeclaration of \#1a. It is noted as
associated with a definition, so it is an invalid redeclaration of the
same partial specialization.

``` cpp
template<typename T> struct Friendly {
  template<typename U> friend int f(U) { return sizeof(T); }
};
Friendly<char> fc;
Friendly<float> ff;                             // error: produces second definition of f(U)
```

— *end example*]

Unless a member of a class template or a member template is a declared
specialization, the specialization of the member is implicitly
instantiated when the specialization is referenced in a context that
requires the member definition to exist or if the existence of the
definition of the member affects the semantics of the program; in
particular, the initialization (and any associated side effects) of a
static data member does not occur unless the static data member is
itself used in a way that requires the definition of the static data
member to exist.

Unless a function template specialization is a declared specialization,
the function template specialization is implicitly instantiated when the
specialization is referenced in a context that requires a function
definition to exist or if the existence of the definition affects the
semantics of the program. A function whose declaration was instantiated
from a friend function definition is implicitly instantiated when it is
referenced in a context that requires a function definition to exist or
if the existence of the definition affects the semantics of the program.
Unless a call is to a function template explicit specialization or to a
member function of an explicitly specialized class template, a default
argument for a function template or a member function of a class
template is implicitly instantiated when the function is called in a
context that requires the value of the default argument.

[*Note 4*: An inline function that is the subject of an explicit
instantiation declaration is not a declared specialization; the intent
is that it still be implicitly instantiated when odr-used
[[basic.def.odr]] so that the body can be considered for inlining, but
that no out-of-line copy of it be generated in the translation
unit. — *end note*]

[*Example 5*:

``` cpp
template<class T> struct Z {
  void f();
  void g();
};

void h() {
  Z<int> a;         // instantiation of class Z<int> required
  Z<char>* p;       // instantiation of class Z<char> not required
  Z<double>* q;     // instantiation of class Z<double> not required

  a.f();            // instantiation of Z<int>::f() required
  p->g();           // instantiation of class Z<char> required, and
                    // instantiation of Z<char>::g() required
}
```

Nothing in this example requires `class` `Z<double>`, `Z<int>::g()`, or
`Z<char>::f()` to be implicitly instantiated.

— *end example*]

Unless a variable template specialization is a declared specialization,
the variable template specialization is implicitly instantiated when it
is referenced in a context that requires a variable definition to exist
or if the existence of the definition affects the semantics of the
program. A default template argument for a variable template is
implicitly instantiated when the variable template is referenced in a
context that requires the value of the default argument.

The existence of a definition of a variable or function is considered to
affect the semantics of the program if the variable or function is
needed for constant evaluation by an expression [[expr.const]], even if
constant evaluation of the expression is not required or if constant
expression evaluation does not use the definition.

[*Example 6*:

``` cpp
template<typename T> constexpr int f() { return T::value; }
template<bool B, typename T> void g(decltype(B ? f<T>() : 0));
template<bool B, typename T> void g(...);
template<bool B, typename T> void h(decltype(int{B ? f<T>() : 0}));
template<bool B, typename T> void h(...);
void x() {
  g<false, int>(0); // OK, B ? f<T>() :\ 0 is not potentially constant evaluated
  h<false, int>(0); // error, instantiates f<int> even though B evaluates to false and
                    // list-initialization of int from int cannot be narrowing
}
```

— *end example*]

If the function selected by overload resolution [[over.match]] can be
determined without instantiating a class template definition, it is
unspecified whether that instantiation actually takes place.

[*Example 7*:

``` cpp
template <class T> struct S {
  operator int();
};

void f(int);
void f(S<int>&);
void f(S<float>);

void g(S<int>& sr) {
  f(sr);            // instantiation of S<int> allowed but not required
                    // instantiation of S<float> allowed but not required
};
```

— *end example*]

If a function template or a member function template specialization is
used in a way that involves overload resolution, a declaration of the
specialization is implicitly instantiated [[temp.over]].

An implementation shall not implicitly instantiate a function template,
a variable template, a member template, a non-virtual member function, a
member class, a static data member of a class template, or a
substatement of a constexpr if statement [[stmt.if]], unless such
instantiation is required.

[*Note 5*: The instantiation of a generic lambda does not require
instantiation of substatements of a constexpr if statement within its
*compound-statement* unless the call operator template is
instantiated. — *end note*]

It is unspecified whether or not an implementation implicitly
instantiates a virtual member function of a class template if the
virtual member function would not otherwise be instantiated. The use of
a template specialization in a default argument shall not cause the
template to be implicitly instantiated except that a class template may
be instantiated where its complete type is needed to determine the
correctness of the default argument. The use of a default argument in a
function call causes specializations in the default argument to be
implicitly instantiated.

Implicitly instantiated class, function, and variable template
specializations are placed in the namespace where the template is
defined. Implicitly instantiated specializations for members of a class
template are placed in the namespace where the enclosing class template
is defined. Implicitly instantiated member templates are placed in the
namespace where the enclosing class or class template is defined.

[*Example 8*:

``` cpp
namespace N {
  template<class T> class List {
  public:
    T* get();
  };
}

template<class K, class V> class Map {
public:
  N::List<V> lt;
  V get(K);
};

void g(Map<const char*,int>& m) {
  int i = m.get("Nicholas");
}
```

A call of `lt.get()` from `Map<const char*,int>::get()` would place
`List<int>::get()` in the namespace `N` rather than in the global
namespace.

— *end example*]

If a function template `f` is called in a way that requires a default
argument to be used, the dependent names are looked up, the semantics
constraints are checked, and the instantiation of any template used in
the default argument is done as if the default argument had been an
initializer used in a function template specialization with the same
scope, the same template parameters and the same access as that of the
function template `f` used at that point, except that the scope in which
a closure type is declared [[expr.prim.lambda.closure]] – and therefore
its associated namespaces – remain as determined from the context of the
definition for the default argument. This analysis is called *default
argument instantiation*. The instantiated default argument is then used
as the argument of `f`.

Each default argument is instantiated independently.

[*Example 9*:

``` cpp
template<class T> void f(T x, T y = ydef(T()), T z = zdef(T()));

class  A { };

A zdef(A);

void g(A a, A b, A c) {
  f(a, b, c);       // no default argument instantiation
  f(a, b);          // default argument z = zdef(T()) instantiated
  f(a);             // error: ydef is not declared
}
```

— *end example*]

The *noexcept-specifier* of a function template specialization is not
instantiated along with the function declaration; it is instantiated
when needed [[except.spec]]. If such an *noexcept-specifier* is needed
but has not yet been instantiated, the dependent names are looked up,
the semantics constraints are checked, and the instantiation of any
template used in the *noexcept-specifier* is done as if it were being
done as part of instantiating the declaration of the specialization at
that point.

[*Note 6*:  [[temp.point]] defines the point of instantiation of a
template specialization. — *end note*]

There is an *implementation-defined* quantity that specifies the limit
on the total depth of recursive instantiations [[implimits]], which
could involve more than one template. The result of an infinite
recursion in instantiation is undefined.

[*Example 10*:

``` cpp
template<class T> class X {
  X<T>* p;          // OK
  X<T*> a;          // implicit generation of X<T> requires
                    // the implicit instantiation of X<T*> which requires
                    // the implicit instantiation of X<T**> which …
};
```

— *end example*]

The *type-constraint*s and *requires-clause* of a template
specialization or member function are not instantiated along with the
specialization or function itself, even for a member function of a local
class; substitution into the atomic constraints formed from them is
instead performed as specified in [[temp.constr.decl]] and
[[temp.constr.atomic]] when determining whether the constraints are
satisfied or as specified in [[temp.constr.decl]] when comparing
declarations.

[*Note 7*: The satisfaction of constraints is determined during
template argument deduction [[temp.deduct]] and overload resolution
[[over.match]]. — *end note*]

[*Example 11*:

``` cpp
template<typename T> concept C = sizeof(T) > 2;
template<typename T> concept D = C<T> && sizeof(T) > 4;

template<typename T> struct S {
  S() requires C<T> { }         // #1
  S() requires D<T> { }         // #2
};

S<char> s1;                     // error: no matching constructor
S<char[8]> s2;                  // OK, calls #2
```

When `S<char>` is instantiated, both constructors are part of the
specialization. Their constraints are not satisfied, and they suppress
the implicit declaration of a default constructor for `S<char>`
[[class.default.ctor]], so there is no viable constructor for `s1`.

— *end example*]

[*Example 12*:

``` cpp
template<typename T> struct S1 {
  template<typename U>
    requires false
  struct Inner1;                // ill-formed, no diagnostic required
};

template<typename T> struct S2 {
  template<typename U>
    requires (sizeof(T[-(int)sizeof(T)]) > 1)
  struct Inner2;                // ill-formed, no diagnostic required
};
```

The class `S1<T>::Inner1` is ill-formed, no diagnostic required, because
it has no valid specializations. `S2` is ill-formed, no diagnostic
required, since no substitution into the constraints of its `Inner2`
template would result in a valid expression.

— *end example*]

### Explicit instantiation <a id="temp.explicit">[[temp.explicit]]</a>

A class, function, variable, or member template specialization can be
explicitly instantiated from its template. A member function, member
class or static data member of a class template can be explicitly
instantiated from the member definition associated with its class
template.

The syntax for explicit instantiation is:

``` bnf
explicit-instantiation:
  externₒₚₜ template declaration
```

There are two forms of explicit instantiation: an explicit instantiation
definition and an explicit instantiation declaration. An explicit
instantiation declaration begins with the `extern` keyword.

An explicit instantiation shall not use a *storage-class-specifier*
[[dcl.stc]] other than `thread_local`. An explicit instantiation of a
function template, member function of a class template, or variable
template shall not use the `inline`, `constexpr`, or `consteval`
specifiers. No *attribute-specifier-seq* [[dcl.attr.grammar]] shall
appertain to an explicit instantiation.

If the explicit instantiation is for a class or member class, the
*elaborated-type-specifier* in the *declaration* shall include a
*simple-template-id*; otherwise, the *declaration* shall be a
*simple-declaration* whose *init-declarator-list* comprises a single
*init-declarator* that does not have an *initializer*. If the explicit
instantiation is for a function or member function, the *unqualified-id*
in the *declarator* shall be either a *template-id* or, where all
template arguments can be deduced, a *template-name* or
*operator-function-id*.

[*Note 1*: The declaration may declare a *qualified-id*, in which case
the *unqualified-id* of the *qualified-id* must be a
*template-id*. — *end note*]

If the explicit instantiation is for a member function, a member class
or a static data member of a class template specialization, the name of
the class template specialization in the *qualified-id* for the member
name shall be a *simple-template-id*. If the explicit instantiation is
for a variable template specialization, the *unqualified-id* in the
*declarator* shall be a *simple-template-id*. An explicit instantiation
shall appear in an enclosing namespace of its template. If the name
declared in the explicit instantiation is an unqualified name, the
explicit instantiation shall appear in the namespace where its template
is declared or, if that namespace is inline [[namespace.def]], any
namespace from its enclosing namespace set.

[*Note 2*: Regarding qualified names in declarators, see 
[[dcl.meaning]]. — *end note*]

[*Example 1*:

``` cpp
template<class T> class Array { void mf(); };
template class Array<char>;
template void Array<int>::mf();

template<class T> void sort(Array<T>& v) { ... }
template void sort(Array<char>&);       // argument is deduced here

namespace N {
  template<class T> void f(T&) { }
}
template void N::f<int>(int&);
```

— *end example*]

A declaration of a function template, a variable template, a member
function or static data member of a class template, or a member function
template of a class or class template shall precede an explicit
instantiation of that entity. A definition of a class template, a member
class of a class template, or a member class template of a class or
class template shall precede an explicit instantiation of that entity
unless the explicit instantiation is preceded by an explicit
specialization of the entity with the same template arguments. If the
*declaration* of the explicit instantiation names an implicitly-declared
special member function [[special]], the program is ill-formed.

The *declaration* in an *explicit-instantiation* and the *declaration*
produced by the corresponding substitution into the templated function,
variable, or class are two declarations of the same entity.

[*Note 3*:

These declarations are required to have matching types as specified in 
[[basic.link]], except as specified in  [[except.spec]].

[*Example 2*:

``` cpp
template<typename T> T var = {};
template float var<float>;      // OK, instantiated variable has type float
template int var<int[16]>[];    // OK, absence of major array bound is permitted
template int *var<int>;         // error: instantiated variable has type int

template<typename T> auto av = T();
template int av<int>;           // OK, variable with type int can be redeclared with type auto

template<typename T> auto f() {}
template void f<int>();         // error: function with deduced return type
                                // redeclared with non-deduced return type[dcl.spec.auto]
```

— *end example*]

— *end note*]

Despite its syntactic form, the *declaration* in an
*explicit-instantiation* for a variable is not itself a definition and
does not conflict with the definition instantiated by an explicit
instantiation definition for that variable.

For a given set of template arguments, if an explicit instantiation of a
template appears after a declaration of an explicit specialization for
that template, the explicit instantiation has no effect. Otherwise, for
an explicit instantiation definition, the definition of a function
template, a variable template, a member function template, or a member
function or static data member of a class template shall be present in
every translation unit in which it is explicitly instantiated.

An explicit instantiation of a class, function template, or variable
template specialization is placed in the namespace in which the template
is defined. An explicit instantiation for a member of a class template
is placed in the namespace where the enclosing class template is
defined. An explicit instantiation for a member template is placed in
the namespace where the enclosing class or class template is defined.

[*Example 3*:

``` cpp
namespace N {
  template<class T> class Y { void mf() { } };
}

template class Y<int>;          // error: class template Y not visible in the global namespace

using N::Y;
template class Y<int>;          // error: explicit instantiation outside of the namespace of the template

template class N::Y<char*>;             // OK: explicit instantiation in namespace N
template void N::Y<double>::mf();       // OK: explicit instantiation in namespace N
```

— *end example*]

A trailing *template-argument* can be left unspecified in an explicit
instantiation of a function template specialization or of a member
function template specialization provided it can be deduced from the
type of a function parameter [[temp.deduct]].

[*Example 4*:

``` cpp
template<class T> class Array { ... };
template<class T> void sort(Array<T>& v) { ... }

// instantiate sort(Array<int>&) -- template-argument deduced
template void sort<>(Array<int>&);
```

— *end example*]

[*Note 4*: An explicit instantiation of a constrained template is
required to satisfy that template’s associated constraints
[[temp.constr.decl]]. The satisfaction of constraints is determined when
forming the template name of an explicit instantiation in which all
template arguments are specified [[temp.names]], or, for explicit
instantiations of function templates, during template argument deduction
[[temp.deduct.decl]] when one or more trailing template arguments are
left unspecified. — *end note*]

An explicit instantiation that names a class template specialization is
also an explicit instantiation of the same kind (declaration or
definition) of each of its members (not including members inherited from
base classes and members that are templates) that has not been
previously explicitly specialized in the translation unit containing the
explicit instantiation, provided that the associated constraints, if
any, of that member are satisfied by the template arguments of the
explicit instantiation ([[temp.constr.decl]], [[temp.constr.constr]]),
except as described below.

[*Note 5*: In addition, it will typically be an explicit instantiation
of certain implementation-dependent data about the class. — *end note*]

An explicit instantiation definition that names a class template
specialization explicitly instantiates the class template specialization
and is an explicit instantiation definition of only those members that
have been defined at the point of instantiation.

An explicit instantiation of a prospective destructor [[class.dtor]]
shall name the selected destructor of the class.

If an entity is the subject of both an explicit instantiation
declaration and an explicit instantiation definition in the same
translation unit, the definition shall follow the declaration. An entity
that is the subject of an explicit instantiation declaration and that is
also used in a way that would otherwise cause an implicit instantiation
[[temp.inst]] in the translation unit shall be the subject of an
explicit instantiation definition somewhere in the program; otherwise
the program is ill-formed, no diagnostic required.

[*Note 6*: This rule does apply to inline functions even though an
explicit instantiation declaration of such an entity has no other
normative effect. This is needed to ensure that if the address of an
inline function is taken in a translation unit in which the
implementation chose to suppress the out-of-line body, another
translation unit will supply the body. — *end note*]

An explicit instantiation declaration shall not name a specialization of
a template with internal linkage.

An explicit instantiation does not constitute a use of a default
argument, so default argument instantiation is not done.

[*Example 5*:

``` cpp
char* p = 0;
template<class T> T g(T x = &p) { return x; }
template int g<int>(int);       // OK even though &p isn't an int.
```

— *end example*]

### Explicit specialization <a id="temp.expl.spec">[[temp.expl.spec]]</a>

An explicit specialization of any of the following:

- function template
- class template
- variable template
- member function of a class template
- static data member of a class template
- member class of a class template
- member enumeration of a class template
- member class template of a class or class template
- member function template of a class or class template

can be declared by a declaration introduced by `template<>`; that is:

``` bnf
explicit-specialization:
  template '<' '>' declaration
```

[*Example 1*:

``` cpp
template<class T> class stream;

template<> class stream<char> { ... };

template<class T> class Array { ... };
template<class T> void sort(Array<T>& v) { ... }

template<> void sort<char*>(Array<char*>&);
```

Given these declarations, `stream<char>` will be used as the definition
of streams of `char`s; other streams will be handled by class template
specializations instantiated from the class template. Similarly,
`sort<char*>` will be used as the sort function for arguments of type
`Array<char*>`; other `Array` types will be sorted by functions
generated from the template.

— *end example*]

An explicit specialization shall not use a *storage-class-specifier*
[[dcl.stc]] other than `thread_local`.

An explicit specialization may be declared in any scope in which the
corresponding primary template may be defined ([[namespace.memdef]],
[[class.mem]], [[temp.mem]]).

A declaration of a function template, class template, or variable
template being explicitly specialized shall precede the declaration of
the explicit specialization.

[*Note 1*: A declaration, but not a definition of the template is
required. — *end note*]

The definition of a class or class template shall precede the
declaration of an explicit specialization for a member template of the
class or class template.

[*Example 2*:

``` cpp
template<> class X<int> { ... };          // error: X not a template

template<class T> class X;

template<> class X<char*> { ... };        // OK: X is a template
```

— *end example*]

A member function, a member function template, a member class, a member
enumeration, a member class template, a static data member, or a static
data member template of a class template may be explicitly specialized
for a class specialization that is implicitly instantiated; in this
case, the definition of the class template shall precede the explicit
specialization for the member of the class template. If such an explicit
specialization for the member of a class template names an
implicitly-declared special member function [[special]], the program is
ill-formed.

A member of an explicitly specialized class is not implicitly
instantiated from the member declaration of the class template; instead,
the member of the class template specialization shall itself be
explicitly defined if its definition is required. In this case, the
definition of the class template explicit specialization shall be in
scope at the point at which the member is defined. The definition of an
explicitly specialized class is unrelated to the definition of a
generated specialization. That is, its members need not have the same
names, types, etc. as the members of a generated specialization. Members
of an explicitly specialized class template are defined in the same
manner as members of normal classes, and not using the `template<>`
syntax. The same is true when defining a member of an explicitly
specialized member class. However, `template<>` is used in defining a
member of an explicitly specialized member class template that is
specialized as a class template.

[*Example 3*:

``` cpp
template<class T> struct A {
  struct B { };
  template<class U> struct C { };
};

template<> struct A<int> {
  void f(int);
};

void h() {
  A<int> a;
  a.f(16);          // A<int>::f must be defined somewhere
}

// template<> not used for a member of an explicitly specialized class template
void A<int>::f(int) { ... }

template<> struct A<char>::B {
  void f();
};
// template<> also not used when defining a member of an explicitly specialized member class
void A<char>::B::f() { ... }

template<> template<class U> struct A<char>::C {
  void f();
};
// template<> is used when defining a member of an explicitly specialized member class template
// specialized as a class template
template<>
template<class U> void A<char>::C<U>::f() { ... }

template<> struct A<short>::B {
  void f();
};
template<> void A<short>::B::f() { ... }              // error: template<> not permitted

template<> template<class U> struct A<short>::C {
  void f();
};
template<class U> void A<short>::C<U>::f() { ... }    // error: template<> required
```

— *end example*]

If a template, a member template or a member of a class template is
explicitly specialized then that specialization shall be declared before
the first use of that specialization that would cause an implicit
instantiation to take place, in every translation unit in which such a
use occurs; no diagnostic is required. If the program does not provide a
definition for an explicit specialization and either the specialization
is used in a way that would cause an implicit instantiation to take
place or the member is a virtual member function, the program is
ill-formed, no diagnostic required. An implicit instantiation is never
generated for an explicit specialization that is declared but not
defined.

[*Example 4*:

``` cpp
class String { };
template<class T> class Array { ... };
template<class T> void sort(Array<T>& v) { ... }

void f(Array<String>& v) {
  sort(v);          // use primary template sort(Array<T>&), T is String
}

template<> void sort<String>(Array<String>& v);     // error: specialization after use of primary template
template<> void sort<>(Array<char*>& v);            // OK: sort<char*> not yet used
template<class T> struct A {
  enum E : T;
  enum class S : T;
};
template<> enum A<int>::E : int { eint };           // OK
template<> enum class A<int>::S : int { sint };     // OK
template<class T> enum A<T>::E : T { eT };
template<class T> enum class A<T>::S : T { sT };
template<> enum A<char>::E : char { echar };        // error: A<char>::E was instantiated
                                                    // when A<char> was instantiated
template<> enum class A<char>::S : char { schar };  // OK
```

— *end example*]

The placement of explicit specialization declarations for function
templates, class templates, variable templates, member functions of
class templates, static data members of class templates, member classes
of class templates, member enumerations of class templates, member class
templates of class templates, member function templates of class
templates, static data member templates of class templates, member
functions of member templates of class templates, member functions of
member templates of non-template classes, static data member templates
of non-template classes, member function templates of member classes of
class templates, etc., and the placement of partial specialization
declarations of class templates, variable templates, member class
templates of non-template classes, static data member templates of
non-template classes, member class templates of class templates, etc.,
can affect whether a program is well-formed according to the relative
positioning of the explicit specialization declarations and their points
of instantiation in the translation unit as specified above and below.
When writing a specialization, be careful about its location; or to make
it compile will be such a trial as to kindle its self-immolation.

A template explicit specialization is in the scope of the namespace in
which the template was defined.

[*Example 5*:

``` cpp
namespace N {
  template<class T> class X { ... };
  template<class T> class Y { ... };

  template<> class X<int> { ... };        // OK: specialization in same namespace
  template<> class Y<double>;                   // forward-declare intent to specialize for double
}

template<> class N::Y<double> { ... };    // OK: specialization in enclosing namespace
template<> class N::Y<short> { ... };     // OK: specialization in enclosing namespace
```

— *end example*]

A *simple-template-id* that names a class template explicit
specialization that has been declared but not defined can be used
exactly like the names of other incompletely-defined classes
[[basic.types]].

[*Example 6*:

``` cpp
template<class T> class X;                      // X is a class template
template<> class X<int>;

X<int>* p;                                      // OK: pointer to declared class X<int>
X<int> x;                                       // error: object of incomplete class X<int>
```

— *end example*]

A trailing *template-argument* can be left unspecified in the
*template-id* naming an explicit function template specialization
provided it can be deduced from the function argument type.

[*Example 7*:

``` cpp
template<class T> class Array { ... };
template<class T> void sort(Array<T>& v);

// explicit specialization for sort(Array<int>&)
// with deduced template-argument of type int
template<> void sort(Array<int>&);
```

— *end example*]

[*Note 2*: An explicit specialization of a constrained template is
required to satisfy that template’s associated constraints
[[temp.constr.decl]]. The satisfaction of constraints is determined when
forming the template name of an explicit specialization in which all
template arguments are specified [[temp.names]], or, for explicit
specializations of function templates, during template argument
deduction [[temp.deduct.decl]] when one or more trailing template
arguments are left unspecified. — *end note*]

A function with the same name as a template and a type that exactly
matches that of a template specialization is not an explicit
specialization [[temp.fct]].

Whether an explicit specialization of a function or variable template is
inline, constexpr, or an immediate function is determined by the
explicit specialization and is independent of those properties of the
template.

[*Example 8*:

``` cpp
template<class T> void f(T) { ... }
template<class T> inline T g(T) { ... }

template<> inline void f<>(int) { ... }   // OK: inline
template<> int g<>(int) { ... }           // OK: not inline
```

— *end example*]

An explicit specialization of a static data member of a template or an
explicit specialization of a static data member template is a definition
if the declaration includes an initializer; otherwise, it is a
declaration.

[*Note 3*:

The definition of a static data member of a template that requires
default-initialization must use a *braced-init-list*:

``` cpp
template<> X Q<int>::x;                         // declaration
template<> X Q<int>::x ();                      // error: declares a function
template<> X Q<int>::x { };                     // definition
```

— *end note*]

A member or a member template of a class template may be explicitly
specialized for a given implicit instantiation of the class template,
even if the member or member template is defined in the class template
definition. An explicit specialization of a member or member template is
specified using the syntax for explicit specialization.

[*Example 9*:

``` cpp
template<class T> struct A {
  void f(T);
  template<class X1> void g1(T, X1);
  template<class X2> void g2(T, X2);
  void h(T) { }
};

// specialization
template<> void A<int>::f(int);

// out of class member template definition
template<class T> template<class X1> void A<T>::g1(T, X1) { }

// member template specialization
template<> template<class X1> void A<int>::g1(int, X1);

// member template specialization
template<> template<>
  void A<int>::g1(int, char);           // X1 deduced as char
template<> template<>
  void A<int>::g2<char>(int, char);     // X2 specified as char

// member specialization even if defined in class definition
template<> void A<int>::h(int) { }
```

— *end example*]

A member or a member template may be nested within many enclosing class
templates. In an explicit specialization for such a member, the member
declaration shall be preceded by a `template<>` for each enclosing class
template that is explicitly specialized.

[*Example 10*:

``` cpp
template<class T1> class A {
  template<class T2> class B {
    void mf();
  };
};
template<> template<> class A<int>::B<double>;
template<> template<> void A<char>::B<char>::mf();
```

— *end example*]

In an explicit specialization declaration for a member of a class
template or a member template that appears in namespace scope, the
member template and some of its enclosing class templates may remain
unspecialized, except that the declaration shall not explicitly
specialize a class member template if its enclosing class templates are
not explicitly specialized as well. In such an explicit specialization
declaration, the keyword `template` followed by a
*template-parameter-list* shall be provided instead of the `template<>`
preceding the explicit specialization declaration of the member. The
types of the *template-parameter*s in the *template-parameter-list*
shall be the same as those specified in the primary template definition.

[*Example 11*:

``` cpp
template <class T1> class A {
  template<class T2> class B {
    template<class T3> void mf1(T3);
    void mf2();
  };
};
template <> template <class X>
  class A<int>::B {
      template <class T> void mf1(T);
  };
template <> template <> template<class T>
  void A<int>::B<double>::mf1(T t) { }
template <class Y> template <>
  void A<Y>::B<double>::mf2() { }       // error: B<double> is specialized but
                                        // its enclosing class template A is not
```

— *end example*]

A specialization of a member function template, member class template,
or static data member template of a non-specialized class template is
itself a template.

An explicit specialization declaration shall not be a friend
declaration.

Default function arguments shall not be specified in a declaration or a
definition for one of the following explicit specializations:

- the explicit specialization of a function template;
- the explicit specialization of a member function template;
- the explicit specialization of a member function of a class template
  where the class template specialization to which the member function
  specialization belongs is implicitly instantiated. \[*Note 6*: Default
  function arguments may be specified in the declaration or definition
  of a member function of a class template specialization that is
  explicitly specialized. — *end note*]

## Function template specializations <a id="temp.fct.spec">[[temp.fct.spec]]</a>

A function instantiated from a function template is called a function
template specialization; so is an explicit specialization of a function
template. Template arguments can be explicitly specified when naming the
function template specialization, deduced from the context (e.g.,
deduced from the function arguments in a call to the function template
specialization, see  [[temp.deduct]]), or obtained from default template
arguments.

Each function template specialization instantiated from a template has
its own copy of any static variable.

[*Example 1*:

``` cpp
template<class T> void f(T* p) {
  static T s;
};

void g(int a, char* b) {
  f(&a);            // calls f<int>(int*)
  f(&b);            // calls f<char*>(char**)
}
```

Here `f<int>(int*)` has a static variable `s` of type `int` and
`f<char*>(char**)` has a static variable `s` of type `char*`.

— *end example*]

### Explicit template argument specification <a id="temp.arg.explicit">[[temp.arg.explicit]]</a>

Template arguments can be specified when referring to a function
template specialization that is not a specialization of a constructor
template by qualifying the function template name with the list of
*template-argument*s in the same way as *template-argument*s are
specified in uses of a class template specialization.

[*Example 1*:

``` cpp
template<class T> void sort(Array<T>& v);
void f(Array<dcomplex>& cv, Array<int>& ci) {
  sort<dcomplex>(cv);                   // sort(Array<dcomplex>&)
  sort<int>(ci);                        // sort(Array<int>&)
}
```

and

``` cpp
template<class U, class V> U convert(V v);

void g(double d) {
  int i = convert<int,double>(d);       // int convert(double)
  char c = convert<char,double>(d);     // char convert(double)
}
```

— *end example*]

Template arguments shall not be specified when referring to a
specialization of a constructor template ([[class.ctor]],
[[class.qual]]).

A template argument list may be specified when referring to a
specialization of a function template

- when a function is called,
- when the address of a function is taken, when a function initializes a
  reference to function, or when a pointer to member function is formed,
- in an explicit specialization,
- in an explicit instantiation, or
- in a friend declaration.

Trailing template arguments that can be deduced [[temp.deduct]] or
obtained from default *template-argument*s may be omitted from the list
of explicit *template-argument*s. A trailing template parameter pack
[[temp.variadic]] not otherwise deduced will be deduced as an empty
sequence of template arguments. If all of the template arguments can be
deduced, they may all be omitted; in this case, the empty template
argument list `<>` itself may also be omitted. In contexts where
deduction is done and fails, or in contexts where deduction is not done,
if a template argument list is specified and it, along with any default
template arguments, identifies a single function template
specialization, then the *template-id* is an lvalue for the function
template specialization.

[*Example 2*:

``` cpp
template<class X, class Y> X f(Y);
template<class X, class Y, class ... Z> X g(Y);
void h() {
  int i = f<int>(5.6);          // Y deduced as double
  int j = f(5.6);               // error: X cannot be deduced
  f<void>(f<int, bool>);        // Y for outer f deduced as int (*)(bool)
  f<void>(f<int>);              // error: f<int> does not denote a single function template specialization
  int k = g<int>(5.6);          // Y deduced as double; Z deduced as an empty sequence
  f<void>(g<int, bool>);        // Y for outer f deduced as int (*)(bool),
                                // Z deduced as an empty sequence
}
```

— *end example*]

[*Note 1*:

An empty template argument list can be used to indicate that a given use
refers to a specialization of a function template even when a
non-template function [[dcl.fct]] is visible that would otherwise be
used. For example:

``` cpp
template <class T> int f(T);    // #1
int f(int);                     // #2
int k = f(1);                   // uses #2
int l = f<>(1);                 // uses #1
```

— *end note*]

Template arguments that are present shall be specified in the
declaration order of their corresponding *template-parameter*s. The
template argument list shall not specify more *template-argument*s than
there are corresponding *template-parameter*s unless one of the
*template-parameter*s is a template parameter pack.

[*Example 3*:

``` cpp
template<class X, class Y, class Z> X f(Y,Z);
template<class ... Args> void f2();
void g() {
  f<int,const char*,double>("aa",3.0);
  f<int,const char*>("aa",3.0); // Z deduced as double
  f<int>("aa",3.0);             // Y deduced as const char*; Z deduced as double
  f("aa",3.0);                  // error: X cannot be deduced
  f2<char, short, int, long>(); // OK
}
```

— *end example*]

Implicit conversions [[conv]] will be performed on a function argument
to convert it to the type of the corresponding function parameter if the
parameter type contains no *template-parameter*s that participate in
template argument deduction.

[*Note 2*:

Template parameters do not participate in template argument deduction if
they are explicitly specified. For example,

``` cpp
template<class T> void f(T);

class Complex {
  Complex(double);
};

void g() {
  f<Complex>(1);    // OK, means f<Complex>(Complex(1))
}
```

— *end note*]

[*Note 3*: Because the explicit template argument list follows the
function template name, and because constructor templates [[class.ctor]]
are named without using a function name [[class.qual]], there is no way
to provide an explicit template argument list for these function
templates. — *end note*]

Template argument deduction can extend the sequence of template
arguments corresponding to a template parameter pack, even when the
sequence contains explicitly specified template arguments.

[*Example 4*:

``` cpp
template<class ... Types> void f(Types ... values);

void g() {
  f<int*, float*>(0, 0, 0);     // Types deduced as the sequence int*, float*, int
}
```

— *end example*]

### Template argument deduction <a id="temp.deduct">[[temp.deduct]]</a>

When a function template specialization is referenced, all of the
template arguments shall have values. The values can be explicitly
specified or, in some cases, be deduced from the use or obtained from
default *template-argument*s.

[*Example 1*:

``` cpp
void f(Array<dcomplex>& cv, Array<int>& ci) {
  sort(cv);                     // calls sort(Array<dcomplex>&)
  sort(ci);                     // calls sort(Array<int>&)
}
```

and

``` cpp
void g(double d) {
  int i = convert<int>(d);      // calls convert<int,double>(double)
  int c = convert<char>(d);     // calls convert<char,double>(double)
}
```

— *end example*]

When an explicit template argument list is specified, if the given
*template-id* is not valid [[temp.names]], type deduction fails.
Otherwise, the specified template argument values are substituted for
the corresponding template parameters as specified below.

After this substitution is performed, the function parameter type
adjustments described in  [[dcl.fct]] are performed.

[*Example 2*: A parameter type of “`void (const int, int[5])`” becomes
“`void(*)(int,int*)`”. — *end example*]

[*Note 1*: A top-level qualifier in a function parameter declaration
does not affect the function type but still affects the type of the
function parameter variable within the function. — *end note*]

[*Example 3*:

``` cpp
template <class T> void f(T t);
template <class X> void g(const X x);
template <class Z> void h(Z, Z*);

int main() {
  // #1: function type is f(int), t is non const
  f<int>(1);

  // #2: function type is f(int), t is const
  f<const int>(1);

  // #3: function type is g(int), x is const
  g<int>(1);

  // #4: function type is g(int), x is const
  g<const int>(1);

  // #5: function type is h(int, const int*)
  h<const int>(1,0);
}
```

— *end example*]

[*Note 2*: `f<int>(1)` and `f<const int>(1)` call distinct functions
even though both of the functions called have the same function
type. — *end note*]

The resulting substituted and adjusted function type is used as the type
of the function template for template argument deduction. If a template
argument has not been deduced and its corresponding template parameter
has a default argument, the template argument is determined by
substituting the template arguments determined for preceding template
parameters into the default argument. If the substitution results in an
invalid type, as described above, type deduction fails.

[*Example 4*:

``` cpp
template <class T, class U = double>
void f(T t = 0, U u = 0);

void g() {
  f(1, 'c');        // f<int,char>(1,'c')
  f(1);             // f<int,double>(1,0)
  f();              // error: T cannot be deduced
  f<int>();         // f<int,double>(0,0)
  f<int,char>();    // f<int,char>(0,0)
}
```

— *end example*]

When all template arguments have been deduced or obtained from default
template arguments, all uses of template parameters in the template
parameter list of the template and the function type are replaced with
the corresponding deduced or default argument values. If the
substitution results in an invalid type, as described above, type
deduction fails. If the function template has associated constraints
[[temp.constr.decl]], those constraints are checked for satisfaction
[[temp.constr.constr]]. If the constraints are not satisfied, type
deduction fails.

At certain points in the template argument deduction process it is
necessary to take a function type that makes use of template parameters
and replace those template parameters with the corresponding template
arguments. This is done at the beginning of template argument deduction
when any explicitly specified template arguments are substituted into
the function type, and again at the end of template argument deduction
when any template arguments that were deduced or obtained from default
arguments are substituted.

The substitution occurs in all types and expressions that are used in
the function type and in template parameter declarations. The
expressions include not only constant expressions such as those that
appear in array bounds or as nontype template arguments but also general
expressions (i.e., non-constant expressions) inside `sizeof`,
`decltype`, and other contexts that allow non-constant expressions. The
substitution proceeds in lexical order and stops when a condition that
causes deduction to fail is encountered. If substitution into different
declarations of the same function template would cause template
instantiations to occur in a different order or not at all, the program
is ill-formed; no diagnostic required.

[*Note 3*: The equivalent substitution in exception specifications is
done only when the *noexcept-specifier* is instantiated, at which point
a program is ill-formed if the substitution results in an invalid type
or expression. — *end note*]

[*Example 5*:

``` cpp
template <class T> struct A { using X = typename T::X; };
template <class T> typename T::X f(typename A<T>::X);
template <class T> void f(...) { }
template <class T> auto g(typename A<T>::X) -> typename T::X;
template <class T> void g(...) { }
template <class T> typename T::X h(typename A<T>::X);
template <class T> auto h(typename A<T>::X) -> typename T::X;   // redeclaration
template <class T> void h(...) { }

void x() {
  f<int>(0);        // OK, substituting return type causes deduction to fail
  g<int>(0);        // error, substituting parameter type instantiates A<int>
  h<int>(0);        // ill-formed, no diagnostic required
}
```

— *end example*]

If a substitution results in an invalid type or expression, type
deduction fails. An invalid type or expression is one that would be
ill-formed, with a diagnostic required, if written using the substituted
arguments.

[*Note 4*: If no diagnostic is required, the program is still
ill-formed. Access checking is done as part of the substitution
process. — *end note*]

Only invalid types and expressions in the immediate context of the
function type, its template parameter types, and its
*explicit-specifier* can result in a deduction failure.

[*Note 5*: The substitution into types and expressions can result in
effects such as the instantiation of class template specializations
and/or function template specializations, the generation of
implicitly-defined functions, etc. Such effects are not in the
“immediate context” and can result in the program being
ill-formed. — *end note*]

A *lambda-expression* appearing in a function type or a template
parameter is not considered part of the immediate context for the
purposes of template argument deduction.

[*Note 6*:

The intent is to avoid requiring implementations to deal with
substitution failure involving arbitrary statements.

[*Example 6*:

``` cpp
template <class T>
  auto f(T) -> decltype([]() { T::invalid; } ());
void f(...);
f(0);               // error: invalid expression not part of the immediate context

template <class T, std::size_t = sizeof([]() { T::invalid; })>
  void g(T);
void g(...);
g(0);               // error: invalid expression not part of the immediate context

template <class T>
  auto h(T) -> decltype([x = T::invalid]() { });
void h(...);
h(0);               // error: invalid expression not part of the immediate context

template <class T>
  auto i(T) -> decltype([]() -> typename T::invalid { });
void i(...);
i(0);               // error: invalid expression not part of the immediate context

template <class T>
  auto j(T t) -> decltype([](auto x) -> decltype(x.invalid) { } (t));   // #1
void j(...);                                                            // #2
j(0);               // deduction fails on #1, calls #2
```

— *end example*]

— *end note*]

[*Example 7*:

``` cpp
struct X { };
struct Y {
  Y(X){}
};

template <class T> auto f(T t1, T t2) -> decltype(t1 + t2);     // #1
X f(Y, Y);                                                      // #2

X x1, x2;
X x3 = f(x1, x2);   // deduction fails on #1 (cannot add X+X), calls #2
```

— *end example*]

[*Note 7*:

Type deduction may fail for the following reasons:

- Attempting to instantiate a pack expansion containing multiple packs
  of differing lengths.
- Attempting to create an array with an element type that is `void`, a
  function type, or a reference type, or attempting to create an array
  with a size that is zero or negative.
- Attempting to use a type that is not a class or enumeration type in a
  qualified name.
- Attempting to use a type in a *nested-name-specifier* of a
  *qualified-id* when that type does not contain the specified member,
  or
  - the specified member is not a type where a type is required, or
  - the specified member is not a template where a template is required,
    or
  - the specified member is not a non-type where a non-type is required.

  \[*Example 1*: \_\_CODEBLOCK_3\_\_ — *end example*]
- Attempting to create a pointer to reference type.
- Attempting to create a reference to `void`.
- Attempting to create “pointer to member of `T`” when `T` is not a
  class type.
- Attempting to give an invalid type to a non-type template parameter.
- Attempting to perform an invalid conversion in either a template
  argument expression, or an expression used in the function
  declaration.
- Attempting to create a function type in which a parameter has a type
  of `void`, or in which the return type is a function type or array
  type.

— *end note*]

[*Example 8*:

In the following example, assuming a `signed char` cannot represent the
value 1000, a narrowing conversion [[dcl.init.list]] would be required
to convert the *template-argument* of type `int` to `signed char`,
therefore substitution fails for the second template
[[temp.arg.nontype]].

``` cpp
template <int> int f(int);
template <signed char> int f(int);
int i1 = f<1000>(0);            // OK
int i2 = f<1>(0);               // ambiguous; not narrowing
```

— *end example*]

#### Deducing template arguments from a function call <a id="temp.deduct.call">[[temp.deduct.call]]</a>

Template argument deduction is done by comparing each function template
parameter type (call it `P`) that contains *template-parameter*s that
participate in template argument deduction with the type of the
corresponding argument of the call (call it `A`) as described below. If
removing references and cv-qualifiers from `P` gives
`std::initializer_list<P^{\prime}>` or `P`'`[N]` for some `P`' and `N`
and the argument is a non-empty initializer list [[dcl.init.list]], then
deduction is performed instead for each element of the initializer list
independently, taking `P`' as separate function template parameter types
`P`'_i and the iᵗʰ initializer element as the corresponding argument. In
the `P`'`[N]` case, if `N` is a non-type template parameter, `N` is
deduced from the length of the initializer list. Otherwise, an
initializer list argument causes the parameter to be considered a
non-deduced context [[temp.deduct.type]].

[*Example 1*:

``` cpp
template<class T> void f(std::initializer_list<T>);
f({1,2,3});                     // T deduced as int
f({1,"asdf"});                  // error: T deduced as both int and const char*

template<class T> void g(T);
g({1,2,3});                     // error: no argument deduced for T

template<class T, int N> void h(T const(&)[N]);
h({1,2,3});                     // T deduced as int; N deduced as 3

template<class T> void j(T const(&)[3]);
j({42});                        // T deduced as int; array bound not considered

struct Aggr { int i; int j; };
template<int N> void k(Aggr const(&)[N]);
k({1,2,3});                     // error: deduction fails, no conversion from int to Aggr
k({{1},{2},{3}});               // OK, N deduced as 3

template<int M, int N> void m(int const(&)[M][N]);
m({{1,2},{3,4}});               // M and N both deduced as 2

template<class T, int N> void n(T const(&)[N], T);
n({{1},{2},{3}},Aggr());        // OK, T is Aggr, N is 3

template<typename T, int N> void o(T (* const (&)[N])(T)) { }
int f1(int);
int f4(int);
char f4(char);
o({ &f1, &f4 });                                // OK, T deduced as int from first element, nothing
                                                // deduced from second element, N deduced as 2
o({ &f1, static_cast<char(*)(char)>(&f4) });    // error: conflicting deductions for T
```

— *end example*]

For a function parameter pack that occurs at the end of the
*parameter-declaration-list*, deduction is performed for each remaining
argument of the call, taking the type `P` of the *declarator-id* of the
function parameter pack as the corresponding function template parameter
type. Each deduction deduces template arguments for subsequent positions
in the template parameter packs expanded by the function parameter pack.
When a function parameter pack appears in a non-deduced context
[[temp.deduct.type]], the type of that pack is never deduced.

[*Example 2*:

``` cpp
template<class ... Types> void f(Types& ...);
template<class T1, class ... Types> void g(T1, Types ...);
template<class T1, class ... Types> void g1(Types ..., T1);

void h(int x, float& y) {
  const int z = x;
  f(x, y, z);                   // Types deduced as int, float, const int
  g(x, y, z);                   // T1 deduced as int; Types deduced as float, int
  g1(x, y, z);                  // error: Types is not deduced
  g1<int, int, int>(x, y, z);   // OK, no deduction occurs
}
```

— *end example*]

If `P` is not a reference type:

- If `A` is an array type, the pointer type produced by the
  array-to-pointer standard conversion [[conv.array]] is used in place
  of `A` for type deduction; otherwise,
- If `A` is a function type, the pointer type produced by the
  function-to-pointer standard conversion [[conv.func]] is used in place
  of `A` for type deduction; otherwise,
- If `A` is a cv-qualified type, the top-level cv-qualifiers of `A`’s
  type are ignored for type deduction.

If `P` is a cv-qualified type, the top-level cv-qualifiers of `P`’s type
are ignored for type deduction. If `P` is a reference type, the type
referred to by `P` is used for type deduction.

[*Example 3*:

``` cpp
template<class T> int f(const T&);
int n1 = f(5);                  // calls f<int>(const int&)
const int i = 0;
int n2 = f(i);                  // calls f<int>(const int&)
template <class T> int g(volatile T&);
int n3 = g(i);                  // calls g<const int>(const volatile int&)
```

— *end example*]

A *forwarding reference* is an rvalue reference to a cv-unqualified
template parameter that does not represent a template parameter of a
class template (during class template argument deduction
[[over.match.class.deduct]]). If `P` is a forwarding reference and the
argument is an lvalue, the type “lvalue reference to `A`” is used in
place of `A` for type deduction.

[*Example 4*:

``` cpp
template <class T> int f(T&& heisenreference);
template <class T> int g(const T&&);
int i;
int n1 = f(i);                  // calls f<int&>(int&)
int n2 = f(0);                  // calls f<int>(int&&)
int n3 = g(i);                  // error: would call g<int>(const int&&), which
                                // would bind an rvalue reference to an lvalue

template <class T> struct A {
  template <class U>
    A(T&&, U&&, int*);          // #1: T&& is not a forwarding reference.
                                // U&& is a forwarding reference.
  A(T&&, int*);                 // #2
};

template <class T> A(T&&, int*) -> A<T>;    // #3: T&& is a forwarding reference.

int *ip;
A a{i, 0, ip};                  // error: cannot deduce from #1
A a0{0, 0, ip};                 // uses #1 to deduce A<int> and #1 to initialize
A a2{i, ip};                    // uses #3 to deduce A<int&> and #2 to initialize
```

— *end example*]

In general, the deduction process attempts to find template argument
values that will make the deduced `A` identical to `A` (after the type
`A` is transformed as described above). However, there are three cases
that allow a difference:

- If the original `P` is a reference type, the deduced `A` (i.e., the
  type referred to by the reference) can be more cv-qualified than the
  transformed `A`.
- The transformed `A` can be another pointer or pointer-to-member type
  that can be converted to the deduced `A` via a function pointer
  conversion [[conv.fctptr]] and/or qualification conversion
  [[conv.qual]].
- If `P` is a class and `P` has the form *simple-template-id*, then the
  transformed `A` can be a derived class `D` of the deduced `A`.
  Likewise, if `P` is a pointer to a class of the form
  *simple-template-id*, the transformed `A` can be a pointer to a
  derived class `D` pointed to by the deduced `A`. However, if there is
  a class `C` that is a (direct or indirect) base class of `D` and
  derived (directly or indirectly) from a class `B` and that would be a
  valid deduced `A`, the deduced `A` cannot be `B` or pointer to `B`,
  respectively.
  \[*Example 5*:
  ``` cpp
  template <typename... T> struct X;
  template <> struct X<> {};
  template <typename T, typename... Ts>
    struct X<T, Ts...> : X<Ts...> {};
  struct D : X<int> {};

  template <typename... T>
  int f(const X<T...>&);
  int x = f(D());     // calls f<int>, not f<>
                      // B is X<>, C is X<int>
  ```

  — *end example*]

These alternatives are considered only if type deduction would otherwise
fail. If they yield more than one possible deduced `A`, the type
deduction fails.

[*Note 1*: If a *template-parameter* is not used in any of the function
parameters of a function template, or is used only in a non-deduced
context, its corresponding *template-argument* cannot be deduced from a
function call and the *template-argument* must be explicitly
specified. — *end note*]

When `P` is a function type, function pointer type, or
pointer-to-member-function type:

- If the argument is an overload set containing one or more function
  templates, the parameter is treated as a non-deduced context.
- If the argument is an overload set (not containing function
  templates), trial argument deduction is attempted using each of the
  members of the set. If deduction succeeds for only one of the overload
  set members, that member is used as the argument value for the
  deduction. If deduction succeeds for more than one member of the
  overload set the parameter is treated as a non-deduced context.

[*Example 5*:

``` cpp
// Only one function of an overload set matches the call so the function parameter is a deduced context.
template <class T> int f(T (*p)(T));
int g(int);
int g(char);
int i = f(g);       // calls f(int (*)(int))
```

— *end example*]

[*Example 6*:

``` cpp
// Ambiguous deduction causes the second function parameter to be a non-deduced context.
template <class T> int f(T, T (*p)(T));
int g(int);
char g(char);
int i = f(1, g);    // calls f(int, int (*)(int))
```

— *end example*]

[*Example 7*:

``` cpp
// The overload set contains a template, causing the second function parameter to be a non-deduced context.
template <class T> int f(T, T (*p)(T));
char g(char);
template <class T> T g(T);
int i = f(1, g);    // calls f(int, int (*)(int))
```

— *end example*]

If deduction succeeds for all parameters that contain
*template-parameter*s that participate in template argument deduction,
and all template arguments are explicitly specified, deduced, or
obtained from default template arguments, remaining parameters are then
compared with the corresponding arguments. For each remaining parameter
`P` with a type that was non-dependent before substitution of any
explicitly-specified template arguments, if the corresponding argument
`A` cannot be implicitly converted to `P`, deduction fails.

[*Note 2*: Parameters with dependent types in which no
*template-parameter*s participate in template argument deduction, and
parameters that became non-dependent due to substitution of
explicitly-specified template arguments, will be checked during overload
resolution. — *end note*]

[*Example 8*:

``` cpp
template <class T> struct Z {
  typedef typename T::x xx;
};
template <class T> typename Z<T>::xx f(void *, T);      // #1
template <class T> void f(int, T);                      // #2
struct A {} a;
int main() {
  f(1, a);          // OK, deduction fails for #1 because there is no conversion from int to void*
}
```

— *end example*]

#### Deducing template arguments taking the address of a function template <a id="temp.deduct.funcaddr">[[temp.deduct.funcaddr]]</a>

Template arguments can be deduced from the type specified when taking
the address of an overloaded function [[over.over]]. If there is a
target, the function template’s function type and the target type are
used as the types of `P` and `A`, and the deduction is done as described
in  [[temp.deduct.type]]. Otherwise, deduction is performed with empty
sets of types P and A.

A placeholder type [[dcl.spec.auto]] in the return type of a function
template is a non-deduced context. If template argument deduction
succeeds for such a function, the return type is determined from
instantiation of the function body.

#### Deducing conversion function template arguments <a id="temp.deduct.conv">[[temp.deduct.conv]]</a>

Template argument deduction is done by comparing the return type of the
conversion function template (call it `P`) with the type that is
required as the result of the conversion (call it `A`; see 
[[dcl.init]], [[over.match.conv]], and [[over.match.ref]] for the
determination of that type) as described in  [[temp.deduct.type]].

If `P` is a reference type, the type referred to by `P` is used in place
of `P` for type deduction and for any further references to or
transformations of `P` in the remainder of this subclause.

If `A` is not a reference type:

- If `P` is an array type, the pointer type produced by the
  array-to-pointer standard conversion [[conv.array]] is used in place
  of `P` for type deduction; otherwise,
- If `P` is a function type, the pointer type produced by the
  function-to-pointer standard conversion [[conv.func]] is used in place
  of `P` for type deduction; otherwise,
- If `P` is a cv-qualified type, the top-level cv-qualifiers of `P`’s
  type are ignored for type deduction.

If `A` is a cv-qualified type, the top-level cv-qualifiers of `A`’s type
are ignored for type deduction. If `A` is a reference type, the type
referred to by `A` is used for type deduction.

In general, the deduction process attempts to find template argument
values that will make the deduced `A` identical to `A`. However, there
are four cases that allow a difference:

- If the original `A` is a reference type, `A` can be more cv-qualified
  than the deduced `A` (i.e., the type referred to by the reference).
- If the original `A` is a function pointer type, `A` can be “pointer to
  function” even if the deduced `A` is “pointer to `noexcept` function”.
- If the original `A` is a pointer-to-member-function type, `A` can be
  “pointer to member of type function” even if the deduced `A` is
  “pointer to member of type `noexcept` function”.
- The deduced `A` can be another pointer or pointer-to-member type that
  can be converted to `A` via a qualification conversion.

These alternatives are considered only if type deduction would otherwise
fail. If they yield more than one possible deduced `A`, the type
deduction fails.

#### Deducing template arguments during partial ordering <a id="temp.deduct.partial">[[temp.deduct.partial]]</a>

Template argument deduction is done by comparing certain types
associated with the two function templates being compared.

Two sets of types are used to determine the partial ordering. For each
of the templates involved there is the original function type and the
transformed function type.

[*Note 1*: The creation of the transformed type is described in 
[[temp.func.order]]. — *end note*]

The deduction process uses the transformed type as the argument template
and the original type of the other template as the parameter template.
This process is done twice for each type involved in the partial
ordering comparison: once using the transformed template-1 as the
argument template and template-2 as the parameter template and again
using the transformed template-2 as the argument template and template-1
as the parameter template.

The types used to determine the ordering depend on the context in which
the partial ordering is done:

- In the context of a function call, the types used are those function
  parameter types for which the function call has arguments.[^12]
- In the context of a call to a conversion function, the return types of
  the conversion function templates are used.
- In other contexts [[temp.func.order]] the function template’s function
  type is used.

Each type nominated above from the parameter template and the
corresponding type from the argument template are used as the types of
`P` and `A`.

Before the partial ordering is done, certain transformations are
performed on the types used for partial ordering:

- If `P` is a reference type, `P` is replaced by the type referred to.
- If `A` is a reference type, `A` is replaced by the type referred to.

If both `P` and `A` were reference types (before being replaced with the
type referred to above), determine which of the two types (if any) is
more cv-qualified than the other; otherwise the types are considered to
be equally cv-qualified for partial ordering purposes. The result of
this determination will be used below.

Remove any top-level cv-qualifiers:

- If `P` is a cv-qualified type, `P` is replaced by the cv-unqualified
  version of `P`.
- If `A` is a cv-qualified type, `A` is replaced by the cv-unqualified
  version of `A`.

Using the resulting types `P` and `A`, the deduction is then done as
described in  [[temp.deduct.type]]. If `P` is a function parameter pack,
the type `A` of each remaining parameter type of the argument template
is compared with the type `P` of the *declarator-id* of the function
parameter pack. Each comparison deduces template arguments for
subsequent positions in the template parameter packs expanded by the
function parameter pack. Similarly, if `A` was transformed from a
function parameter pack, it is compared with each remaining parameter
type of the parameter template. If deduction succeeds for a given type,
the type from the argument template is considered to be at least as
specialized as the type from the parameter template.

[*Example 1*:

``` cpp
template<class... Args>           void f(Args... args);         // #1
template<class T1, class... Args> void f(T1 a1, Args... args);  // #2
template<class T1, class T2>      void f(T1 a1, T2 a2);         // #3

f();                // calls #1
f(1, 2, 3);         // calls #2
f(1, 2);            // calls #3; non-variadic template #3 is more specialized
                    // than the variadic templates #1 and #2
```

— *end example*]

If, for a given type, the types are identical after the transformations
above and both `P` and `A` were reference types (before being replaced
with the type referred to above):

- if the type from the argument template was an lvalue reference and the
  type from the parameter template was not, the parameter type is not
  considered to be at least as specialized as the argument type;
  otherwise,
- if the type from the argument template is more cv-qualified than the
  type from the parameter template (as described above), the parameter
  type is not considered to be at least as specialized as the argument
  type.

Function template `F` is *at least as specialized as* function template
`G` if, for each pair of types used to determine the ordering, the type
from `F` is at least as specialized as the type from `G`. `F` is *more
specialized than* `G` if `F` is at least as specialized as `G` and `G`
is not at least as specialized as `F`.

If, after considering the above, function template `F` is at least as
specialized as function template `G` and vice-versa, and if `G` has a
trailing function parameter pack for which `F` does not have a
corresponding parameter, and if `F` does not have a trailing function
parameter pack, then `F` is more specialized than `G`.

In most cases, deduction fails if not all template parameters have
values, but for partial ordering purposes a template parameter may
remain without a value provided it is not used in the types being used
for partial ordering.

[*Note 2*: A template parameter used in a non-deduced context is
considered used. — *end note*]

[*Example 2*:

``` cpp
template <class T> T f(int);            // #1
template <class T, class U> T f(U);     // #2
void g() {
  f<int>(1);                            // calls #1
}
```

— *end example*]

[*Note 3*: Partial ordering of function templates containing template
parameter packs is independent of the number of deduced arguments for
those template parameter packs. — *end note*]

[*Example 3*:

``` cpp
template<class ...> struct Tuple { };
template<class ... Types> void g(Tuple<Types ...>);                 // #1
template<class T1, class ... Types> void g(Tuple<T1, Types ...>);   // #2
template<class T1, class ... Types> void g(Tuple<T1, Types& ...>);  // #3

g(Tuple<>());                   // calls #1
g(Tuple<int, float>());         // calls #2
g(Tuple<int, float&>());        // calls #3
g(Tuple<int>());                // calls #3
```

— *end example*]

#### Deducing template arguments from a type <a id="temp.deduct.type">[[temp.deduct.type]]</a>

Template arguments can be deduced in several different contexts, but in
each case a type that is specified in terms of template parameters (call
it `P`) is compared with an actual type (call it `A`), and an attempt is
made to find template argument values (a type for a type parameter, a
value for a non-type parameter, or a template for a template parameter)
that will make `P`, after substitution of the deduced values (call it
the deduced `A`), compatible with `A`.

In some cases, the deduction is done using a single set of types `P` and
`A`, in other cases, there will be a set of corresponding types `P` and
`A`. Type deduction is done independently for each `P/A` pair, and the
deduced template argument values are then combined. If type deduction
cannot be done for any `P/A` pair, or if for any pair the deduction
leads to more than one possible set of deduced values, or if different
pairs yield different deduced values, or if any template argument
remains neither deduced nor explicitly specified, template argument
deduction fails. The type of a type parameter is only deduced from an
array bound if it is not otherwise deduced.

A given type `P` can be composed from a number of other types,
templates, and non-type values:

- A function type includes the types of each of the function parameters
  and the return type.
- A pointer-to-member type includes the type of the class object pointed
  to and the type of the member pointed to.
- A type that is a specialization of a class template (e.g., `A<int>`)
  includes the types, templates, and non-type values referenced by the
  template argument list of the specialization.
- An array type includes the array element type and the value of the
  array bound.

In most cases, the types, templates, and non-type values that are used
to compose `P` participate in template argument deduction. That is, they
may be used to determine the value of a template argument, and template
argument deduction fails if the value so determined is not consistent
with the values determined elsewhere. In certain contexts, however, the
value does not participate in type deduction, but instead uses the
values of template arguments that were either deduced elsewhere or
explicitly specified. If a template parameter is used only in
non-deduced contexts and is not explicitly specified, template argument
deduction fails.

[*Note 1*: Under [[temp.deduct.call]], if `P` contains no
*template-parameter*s that appear in deduced contexts, no deduction is
done, so `P` and `A` need not have the same form. — *end note*]

The non-deduced contexts are:

- The *nested-name-specifier* of a type that was specified using a
  *qualified-id*.
- The *expression* of a *decltype-specifier*.
- A non-type template argument or an array bound in which a
  subexpression references a template parameter.
- A template parameter used in the parameter type of a function
  parameter that has a default argument that is being used in the call
  for which argument deduction is being done.
- A function parameter for which the associated argument is an overload
  set [[over.over]], and one or more of the following apply:
  - more than one function matches the function parameter type
    (resulting in an ambiguous deduction), or
  - no function matches the function parameter type, or
  - the overload set supplied as an argument contains one or more
    function templates.
- A function parameter for which the associated argument is an
  initializer list [[dcl.init.list]] but the parameter does not have a
  type for which deduction from an initializer list is specified
  [[temp.deduct.call]].
  \[*Example 6*:
  ``` cpp
  template<class T> void g(T);
  g({1,2,3});                 // error: no argument deduced for T
  ```

  — *end example*]
- A function parameter pack that does not occur at the end of the
  *parameter-declaration-list*.

When a type name is specified in a way that includes a non-deduced
context, all of the types that comprise that type name are also
non-deduced. However, a compound type can include both deduced and
non-deduced types.

[*Example 1*: If a type is specified as `A<T>::B<T2>`, both `T` and
`T2` are non-deduced. Likewise, if a type is specified as
`A<I+J>::X<T>`, `I`, `J`, and `T` are non-deduced. If a type is
specified as `void` `f(typename` `A<T>::B,` `A<T>)`, the `T` in
`A<T>::B` is non-deduced but the `T` in `A<T>` is
deduced. — *end example*]

[*Example 2*:

Here is an example in which different parameter/argument pairs produce
inconsistent template argument deductions:

``` cpp
template<class T> void f(T x, T y) { ... }
struct A { ... };
struct B : A { ... };
void g(A a, B b) {
  f(a,b);           // error: T could be A or B
  f(b,a);           // error: T could be A or B
  f(a,a);           // OK: T is A
  f(b,b);           // OK: T is B
}
```

Here is an example where two template arguments are deduced from a
single function parameter/argument pair. This can lead to conflicts that
cause type deduction to fail:

``` cpp
template <class T, class U> void f(  T (*)( T, U, U )  );

int g1( int, float, float);
char g2( int, float, float);
int g3( int, char, float);

void r() {
  f(g1);            // OK: T is int and U is float
  f(g2);            // error: T could be char or int
  f(g3);            // error: U could be char or float
}
```

Here is an example where a qualification conversion applies between the
argument type on the function call and the deduced template argument
type:

``` cpp
template<class T> void f(const T*) { }
int* p;
void s() {
  f(p);             // f(const int*)
}
```

Here is an example where the template argument is used to instantiate a
derived class type of the corresponding function parameter type:

``` cpp
template <class T> struct B { };
template <class T> struct D : public B<T> {};
struct D2 : public B<int> {};
template <class T> void f(B<T>&){}
void t() {
  D<int> d;
  D2     d2;
  f(d);             // calls f(B<int>&)
  f(d2);            // calls f(B<int>&)
}
```

— *end example*]

A template type argument `T`, a template template argument `TT` or a
template non-type argument `i` can be deduced if `P` and `A` have one of
the following forms:

``` cpp
T
cv T
T*
T&
T&&
T[integer-constant]
template-name<T>  (where template-name refers to a class template)
type(T)
T()
T(T)
T type::*
type T::*
T T::*
T (type::*)()
type (T::*)()
type (type::*)(T)
type (T::*)(T)
T (type::*)(T)
T (T::*)()
T (T::*)(T)
type[i]
template-name<i>  (where template-name refers to a class template)
TT<T>
TT<i>
TT<>
```

where `(T)` represents a parameter-type-list [[dcl.fct]] where at least
one parameter type contains a `T`, and `()` represents a
parameter-type-list where no parameter type contains a `T`. Similarly,
`<T>` represents template argument lists where at least one argument
contains a `T`, `<i>` represents template argument lists where at least
one argument contains an `i` and `<>` represents template argument lists
where no argument contains a `T` or an `i`.

If `P` has a form that contains `<T>` or `<i>`, then each argument Pᵢ of
the respective template argument list of `P` is compared with the
corresponding argument Aᵢ of the corresponding template argument list of
`A`. If the template argument list of `P` contains a pack expansion that
is not the last template argument, the entire template argument list is
a non-deduced context. If `Pᵢ` is a pack expansion, then the pattern of
`Pᵢ` is compared with each remaining argument in the template argument
list of `A`. Each comparison deduces template arguments for subsequent
positions in the template parameter packs expanded by `Pᵢ`. During
partial ordering [[temp.deduct.partial]], if `Aᵢ` was originally a pack
expansion:

- if `P` does not contain a template argument corresponding to `Aᵢ` then
  `Aᵢ` is ignored;
- otherwise, if `Pᵢ` is not a pack expansion, template argument
  deduction fails.

[*Example 3*:

``` cpp
template<class T1, class... Z> class S;                                 // #1
template<class T1, class... Z> class S<T1, const Z&...> { };            // #2
template<class T1, class T2>   class S<T1, const T2&> { };              // #3
S<int, const int&> s;           // both #2 and #3 match; #3 is more specialized

template<class T, class... U>            struct A { };                  // #1
template<class T1, class T2, class... U> struct A<T1, T2*, U...> { };   // #2
template<class T1, class T2>             struct A<T1, T2> { };          // #3
template struct A<int, int*>;   // selects #2
```

— *end example*]

Similarly, if `P` has a form that contains `(T)`, then each parameter
type `Pᵢ` of the respective parameter-type-list [[dcl.fct]] of `P` is
compared with the corresponding parameter type `Aᵢ` of the corresponding
parameter-type-list of `A`. If `P` and `A` are function types that
originated from deduction when taking the address of a function template
[[temp.deduct.funcaddr]] or when deducing template arguments from a
function declaration [[temp.deduct.decl]] and `Pᵢ` and `Aᵢ` are
parameters of the top-level parameter-type-list of `P` and `A`,
respectively, `Pᵢ` is adjusted if it is a forwarding reference
[[temp.deduct.call]] and `Aᵢ` is an lvalue reference, in which case the
type of `Pᵢ` is changed to be the template parameter type (i.e., `T&&`
is changed to simply `T`).

[*Note 2*: As a result, when `Pᵢ` is `T&&` and `Aᵢ` is `X&`, the
adjusted `Pᵢ` will be `T`, causing `T` to be deduced as
`X&`. — *end note*]

[*Example 4*:

``` cpp
template <class T> void f(T&&);
template <> void f(int&) { }    // #1
template <> void f(int&&) { }   // #2
void g(int i) {
  f(i);                         // calls f<int&>(int&), i.e., #1
  f(0);                         // calls f<int>(int&&), i.e., #2
}
```

— *end example*]

If the *parameter-declaration* corresponding to `Pᵢ` is a function
parameter pack, then the type of its *declarator-id* is compared with
each remaining parameter type in the parameter-type-list of `A`. Each
comparison deduces template arguments for subsequent positions in the
template parameter packs expanded by the function parameter pack. During
partial ordering [[temp.deduct.partial]], if `Aᵢ` was originally a
function parameter pack:

- if `P` does not contain a function parameter type corresponding to
  `Aᵢ` then `Aᵢ` is ignored;
- otherwise, if `Pᵢ` is not a function parameter pack, template argument
  deduction fails.

[*Example 5*:

``` cpp
template<class T, class... U> void f(T*, U...) { }  // #1
template<class T>             void f(T) { }         // #2
template void f(int*);                              // selects #1
```

— *end example*]

These forms can be used in the same way as `T` is for further
composition of types.

[*Example 6*:

``` cpp
X<int> (*)(char[6])
```

is of the form

``` cpp
template-name<T> (*)(type[i])
```

which is a variant of

``` cpp
type (*)(T)
```

where type is `X<int>` and `T` is `char[6]`.

— *end example*]

Template arguments cannot be deduced from function arguments involving
constructs other than the ones specified above.

When the value of the argument corresponding to a non-type template
parameter `P` that is declared with a dependent type is deduced from an
expression, the template parameters in the type of `P` are deduced from
the type of the value.

[*Example 7*:

``` cpp
template<long n> struct A { };

template<typename T> struct C;
template<typename T, T n> struct C<A<n>> {
  using Q = T;
};

using R = long;
using R = C<A<2>>::Q;           // OK; T was deduced as long from the
                                // template argument value in the type A<2>
```

— *end example*]

The type of `N` in the type `T[N]` is `std::size_t`.

[*Example 8*:

``` cpp
template<typename T> struct S;
template<typename T, T n> struct S<int[n]> {
  using Q = T;
};

using V = decltype(sizeof 0);
using V = S<int[42]>::Q;        // OK; T was deduced as std::size_t from the type int[42]
```

— *end example*]

[*Example 9*:

``` cpp
template<class T, T i> void f(int (&a)[i]);
int v[10];
void g() {
  f(v);                         // OK: T is std::size_t
}
```

— *end example*]

[*Note 3*:

Except for reference and pointer types, a major array bound is not part
of a function parameter type and cannot be deduced from an argument:

``` cpp
template<int i> void f1(int a[10][i]);
template<int i> void f2(int a[i][20]);
template<int i> void f3(int (&a)[i][20]);

void g() {
  int v[10][20];
  f1(v);                        // OK: i deduced as 20
  f1<20>(v);                    // OK
  f2(v);                        // error: cannot deduce template-argument i
  f2<10>(v);                    // OK
  f3(v);                        // OK: i deduced as 10
}
```

— *end note*]

[*Note 4*:

If, in the declaration of a function template with a non-type template
parameter, the non-type template parameter is used in a subexpression in
the function parameter list, the expression is a non-deduced context as
specified above.

[*Example 10*:

``` cpp
template <int i> class A { ... };
template <int i> void g(A<i+1>);
template <int i> void f(A<i>, A<i+1>);
void k() {
  A<1> a1;
  A<2> a2;
  g(a1);                        // error: deduction fails for expression i+1
  g<0>(a1);                     // OK
  f(a1, a2);                    // OK
}
```

— *end example*]

— *end note*]

[*Note 5*:

Template parameters do not participate in template argument deduction if
they are used only in non-deduced contexts. For example,

``` cpp
template<int i, typename T>
T deduce(typename A<T>::X x,    // T is not deduced here
         T t,                   // but T is deduced here
         typename B<i>::Y y);   // i is not deduced here
A<int> a;
B<77>  b;

int    x = deduce<77>(a.xm, 62, b.ym);
// T deduced as int; a.xm must be convertible to A<int>::X
// i is explicitly specified to be 77; b.ym must be convertible to B<77>::Y
```

— *end note*]

If `P` has a form that contains `<i>`, and if the type of `i` differs
from the type of the corresponding template parameter of the template
named by the enclosing *simple-template-id*, deduction fails. If `P` has
a form that contains `[i]`, and if the type of `i` is not an integral
type, deduction fails.[^13]

[*Example 11*:

``` cpp
template<int i> class A { ... };
template<short s> void f(A<s>);
void k1() {
  A<1> a;
  f(a);             // error: deduction fails for conversion from int to short
  f<1>(a);          // OK
}

template<const short cs> class B { };
template<short s> void g(B<s>);
void k2() {
  B<1> b;
  g(b);             // OK: cv-qualifiers are ignored on template parameter types
}
```

— *end example*]

A *template-argument* can be deduced from a function, pointer to
function, or pointer-to-member-function type.

[*Example 12*:

``` cpp
template<class T> void f(void(*)(T,int));
template<class T> void foo(T,int);
void g(int,int);
void g(char,int);

void h(int,int,int);
void h(char,int);
int m() {
  f(&g);            // error: ambiguous
  f(&h);            // OK: void h(char,int) is a unique match
  f(&foo);          // error: type deduction fails because foo is a template
}
```

— *end example*]

A template *type-parameter* cannot be deduced from the type of a
function default argument.

[*Example 13*:

``` cpp
template <class T> void f(T = 5, T = 7);
void g() {
  f(1);             // OK: call f<int>(1,7)
  f();              // error: cannot deduce T
  f<int>();         // OK: call f<int>(5,7)
}
```

— *end example*]

The *template-argument* corresponding to a template *template-parameter*
is deduced from the type of the *template-argument* of a class template
specialization used in the argument list of a function call.

[*Example 14*:

``` cpp
template <template <class T> class X> struct A { };
template <template <class T> class X> void f(A<X>) { }
template<class T> struct B { };
A<B> ab;
f(ab);              // calls f(A<B>)
```

— *end example*]

[*Note 6*: Template argument deduction involving parameter packs
[[temp.variadic]] can deduce zero or more arguments for each parameter
pack. — *end note*]

[*Example 15*:

``` cpp
template<class> struct X { };
template<class R, class ... ArgTypes> struct X<R(int, ArgTypes ...)> { };
template<class ... Types> struct Y { };
template<class T, class ... Types> struct Y<T, Types& ...> { };

template<class ... Types> int f(void (*)(Types ...));
void g(int, float);

X<int> x1;                      // uses primary template
X<int(int, float, double)> x2;  // uses partial specialization; ArgTypes contains float, double
X<int(float, int)> x3;          // uses primary template
Y<> y1;                         // use primary template; Types is empty
Y<int&, float&, double&> y2;    // uses partial specialization; T is int&, Types contains float, double
Y<int, float, double> y3;       // uses primary template; Types contains int, float, double
int fv = f(g);                  // OK; Types contains int, float
```

— *end example*]

#### Deducing template arguments from a function declaration <a id="temp.deduct.decl">[[temp.deduct.decl]]</a>

In a declaration whose *declarator-id* refers to a specialization of a
function template, template argument deduction is performed to identify
the specialization to which the declaration refers. Specifically, this
is done for explicit instantiations [[temp.explicit]], explicit
specializations [[temp.expl.spec]], and certain friend declarations
[[temp.friend]]. This is also done to determine whether a deallocation
function template specialization matches a placement `operator new` (
[[basic.stc.dynamic.deallocation]], [[expr.new]]). In all these cases,
`P` is the type of the function template being considered as a potential
match and `A` is either the function type from the declaration or the
type of the deallocation function that would match the placement
`operator new` as described in  [[expr.new]]. The deduction is done as
described in  [[temp.deduct.type]].

If, for the set of function templates so considered, there is either no
match or more than one match after partial ordering has been considered
[[temp.func.order]], deduction fails and, in the declaration cases, the
program is ill-formed.

### Overload resolution <a id="temp.over">[[temp.over]]</a>

When a call to the name of a function or function template is written
(explicitly, or implicitly using the operator notation), template
argument deduction [[temp.deduct]] and checking of any explicit template
arguments [[temp.arg]] are performed for each function template to find
the template argument values (if any) that can be used with that
function template to instantiate a function template specialization that
can be invoked with the call arguments. For each function template, if
the argument deduction and checking succeeds, the *template-argument*s
(deduced and/or explicit) are used to synthesize the declaration of a
single function template specialization which is added to the candidate
functions set to be used in overload resolution. If, for a given
function template, argument deduction fails or the synthesized function
template specialization would be ill-formed, no such function is added
to the set of candidate functions for that template. The complete set of
candidate functions includes all the synthesized declarations and all of
the non-template overloaded functions of the same name. The synthesized
declarations are treated like any other functions in the remainder of
overload resolution, except as explicitly noted in 
[[over.match.best]].[^14]

[*Example 1*:

``` cpp
template<class T> T max(T a, T b) { return a>b?a:b; }

void f(int a, int b, char c, char d) {
  int m1 = max(a,b);            // max(int a, int b)
  char m2 = max(c,d);           // max(char a, char b)
  int m3 = max(a,c);            // error: cannot generate max(int,char)
}
```

Adding the non-template function

``` cpp
int max(int,int);
```

to the example above would resolve the third call, by providing a
function that could be called for `max(a,c)` after using the standard
conversion of `char` to `int` for `c`.

— *end example*]

[*Example 2*:

Here is an example involving conversions on a function argument involved
in *template-argument* deduction:

``` cpp
template<class T> struct B { ... };
template<class T> struct D : public B<T> { ... };
template<class T> void f(B<T>&);

void g(B<int>& bi, D<int>& di) {
  f(bi);            // f(bi)
  f(di);            // f((B<int>&)di)
}
```

— *end example*]

[*Example 3*:

Here is an example involving conversions on a function argument not
involved in *template-parameter* deduction:

``` cpp
template<class T> void f(T*,int);       // #1
template<class T> void f(T,char);       // #2

void h(int* pi, int i, char c) {
  f(pi,i);          // #1: f<int>(pi,i)
  f(pi,c);          // #2: f<int*>(pi,c)

  f(i,c);           // #2: f<int>(i,c);
  f(i,i);           // #2: f<int>(i,char(i))
}
```

— *end example*]

Only the signature of a function template specialization is needed to
enter the specialization in a set of candidate functions. Therefore only
the function template declaration is needed to resolve a call for which
a template specialization is a candidate.

[*Example 4*:

``` cpp
template<class T> void f(T);    // declaration

void g() {
  f("Annemarie");               // call of f<const char*>
}
```

The call of `f` is well-formed even if the template `f` is only declared
and not defined at the point of the call. The program will be ill-formed
unless a specialization for `f<const char*>`, either implicitly or
explicitly generated, is present in some translation unit.

— *end example*]

<!-- Link reference definitions -->
[basic.def]: basic.md#basic.def
[basic.def.odr]: basic.md#basic.def.odr
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.classref]: basic.md#basic.lookup.classref
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope]: basic.md#basic.scope
[basic.scope.hiding]: basic.md#basic.scope.hiding
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.types]: basic.md#basic.types
[class.access]: class.md#class.access
[class.base.init]: class.md#class.base.init
[class.conv.fct]: class.md#class.conv.fct
[class.ctor]: class.md#class.ctor
[class.default.ctor]: class.md#class.default.ctor
[class.derived]: class.md#class.derived
[class.dtor]: class.md#class.dtor
[class.friend]: class.md#class.friend
[class.local]: class.md#class.local
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.pre]: class.md#class.pre
[class.qual]: basic.md#class.qual
[class.temporary]: basic.md#class.temporary
[conv]: expr.md#conv
[conv.array]: expr.md#conv.array
[conv.fctptr]: expr.md#conv.fctptr
[conv.func]: expr.md#conv.func
[conv.lval]: expr.md#conv.lval
[conv.qual]: expr.md#conv.qual
[dcl.align]: dcl.md#dcl.align
[dcl.attr.grammar]: dcl.md#dcl.attr.grammar
[dcl.decl]: dcl.md#dcl.decl
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def.general]: dcl.md#dcl.fct.def.general
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.meaning]: dcl.md#dcl.meaning
[dcl.pre]: dcl.md#dcl.pre
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.stc]: dcl.md#dcl.stc
[dcl.struct.bind]: dcl.md#dcl.struct.bind
[dcl.type.class.deduct]: dcl.md#dcl.type.class.deduct
[dcl.type.elab]: dcl.md#dcl.type.elab
[dcl.type.simple]: dcl.md#dcl.type.simple
[except.spec]: except.md#except.spec
[expr.const]: expr.md#expr.const
[expr.context]: expr.md#expr.context
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.new]: expr.md#expr.new
[expr.prim.fold]: expr.md#expr.prim.fold
[expr.prim.id]: expr.md#expr.prim.id
[expr.prim.id.unqual]: expr.md#expr.prim.id.unqual
[expr.prim.lambda.capture]: expr.md#expr.prim.lambda.capture
[expr.prim.lambda.closure]: expr.md#expr.prim.lambda.closure
[expr.ref]: expr.md#expr.ref
[expr.sizeof]: expr.md#expr.sizeof
[expr.typeid]: expr.md#expr.typeid
[expr.unary.op]: expr.md#expr.unary.op
[implimits]: #implimits
[intro.defs]: intro.md#intro.defs
[intro.object]: basic.md#intro.object
[lex.string]: lex.md#lex.string
[namespace.def]: dcl.md#namespace.def
[namespace.memdef]: dcl.md#namespace.memdef
[namespace.udecl]: dcl.md#namespace.udecl
[over.ics.rank]: over.md#over.ics.rank
[over.match]: over.md#over.match
[over.match.best]: over.md#over.match.best
[over.match.class.deduct]: over.md#over.match.class.deduct
[over.match.conv]: over.md#over.match.conv
[over.match.oper]: over.md#over.match.oper
[over.match.ref]: over.md#over.match.ref
[over.match.viable]: over.md#over.match.viable
[over.over]: over.md#over.over
[special]: class.md#special
[stmt.if]: stmt.md#stmt.if
[support.types]: support.md#support.types
[temp]: #temp
[temp.alias]: #temp.alias
[temp.arg]: #temp.arg
[temp.arg.explicit]: #temp.arg.explicit
[temp.arg.nontype]: #temp.arg.nontype
[temp.arg.template]: #temp.arg.template
[temp.arg.type]: #temp.arg.type
[temp.class]: #temp.class
[temp.class.order]: #temp.class.order
[temp.class.spec]: #temp.class.spec
[temp.class.spec.match]: #temp.class.spec.match
[temp.class.spec.mfunc]: #temp.class.spec.mfunc
[temp.concept]: #temp.concept
[temp.constr]: #temp.constr
[temp.constr.atomic]: #temp.constr.atomic
[temp.constr.constr]: #temp.constr.constr
[temp.constr.decl]: #temp.constr.decl
[temp.constr.normal]: #temp.constr.normal
[temp.constr.op]: #temp.constr.op
[temp.constr.order]: #temp.constr.order
[temp.decls]: #temp.decls
[temp.deduct]: #temp.deduct
[temp.deduct.call]: #temp.deduct.call
[temp.deduct.conv]: #temp.deduct.conv
[temp.deduct.decl]: #temp.deduct.decl
[temp.deduct.funcaddr]: #temp.deduct.funcaddr
[temp.deduct.guide]: #temp.deduct.guide
[temp.deduct.partial]: #temp.deduct.partial
[temp.deduct.type]: #temp.deduct.type
[temp.dep]: #temp.dep
[temp.dep.candidate]: #temp.dep.candidate
[temp.dep.constexpr]: #temp.dep.constexpr
[temp.dep.expr]: #temp.dep.expr
[temp.dep.res]: #temp.dep.res
[temp.dep.temp]: #temp.dep.temp
[temp.dep.type]: #temp.dep.type
[temp.expl.spec]: #temp.expl.spec
[temp.explicit]: #temp.explicit
[temp.fct]: #temp.fct
[temp.fct.spec]: #temp.fct.spec
[temp.fold.empty]: #temp.fold.empty
[temp.friend]: #temp.friend
[temp.func.order]: #temp.func.order
[temp.inject]: #temp.inject
[temp.inst]: #temp.inst
[temp.local]: #temp.local
[temp.mem]: #temp.mem
[temp.mem.class]: #temp.mem.class
[temp.mem.enum]: #temp.mem.enum
[temp.mem.func]: #temp.mem.func
[temp.names]: #temp.names
[temp.nondep]: #temp.nondep
[temp.over]: #temp.over
[temp.over.link]: #temp.over.link
[temp.param]: #temp.param
[temp.point]: #temp.point
[temp.pre]: #temp.pre
[temp.res]: #temp.res
[temp.spec]: #temp.spec
[temp.static]: #temp.static
[temp.type]: #temp.type
[temp.variadic]: #temp.variadic

[^1]: Since template *template-parameter*s and template
    *template-argument*s are treated as types for descriptive purposes,
    the terms *non-type parameter* and *non-type argument* are used to
    refer to non-type, non-template parameters and arguments.

[^2]: A `>` that encloses the *type-id* of a `dynamic_cast`,
    `static_cast`, `reinterpret_cast` or `const_cast`, or which encloses
    the *template-argument*s of a subsequent *template-id*, is
    considered nested for the purpose of this description.

[^3]: There is no such ambiguity in a default *template-argument*
    because the form of the *template-parameter* determines the
    allowable forms of the *template-argument*.

[^4]: A constraint is in disjunctive normal form when it is a
    disjunction of clauses where each clause is a conjunction of atomic
    constraints.

    \[*Example 2*: For atomic constraints A, B, and C, the disjunctive
    normal form of the constraint A ∧ (B ∨ C) is (A ∧ B) ∨ (A ∧ C). Its
    disjunctive clauses are (A ∧ B) and (A ∧ C). — *end example*]

[^5]: A constraint is in conjunctive normal form when it is a
    conjunction of clauses where each clause is a disjunction of atomic
    constraints.

    \[*Example 3*: For atomic constraints A, B, and C, the constraint
    A ∧ (B ∨ C) is in conjunctive normal form. Its conjunctive clauses
    are A and (B ∨ C). — *end example*]

[^6]: The identity of enumerators is not preserved.

[^7]: An array as a *template-parameter* decays to a pointer.

[^8]: There is no way in which they could be used.

[^9]: That is, declarations of non-template functions do not merely
    guide overload resolution of function template specializations with
    the same name. If such a non-template function is odr-used
    [[basic.def.odr]] in a program, it must be defined; it will not be
    implicitly instantiated using the function template definition.

[^10]: This includes friend function declarations.

[^11]: Friend declarations do not introduce new names into any scope,
    either when the template is declared or when it is instantiated.

[^12]: Default arguments are not considered to be arguments in this
    context; they only become arguments after a function has been
    selected.

[^13]: Although the *template-argument* corresponding to a
    *template-parameter* of type `bool` may be deduced from an array
    bound, the resulting value will always be `true` because the array
    bound will be nonzero.

[^14]: The parameters of function template specializations contain no
    template parameter types. The set of conversions allowed on deduced
    arguments is limited, because the argument deduction process
    produces function templates with parameters that either match the
    call arguments exactly or differ only in ways that can be bridged by
    the allowed limited conversions. Non-deduced arguments allow the
    full range of conversions. Note also that  [[over.match.best]]
    specifies that a non-template function will be given preference over
    a template specialization if the two functions are otherwise equally
    good candidates for an overload match.
