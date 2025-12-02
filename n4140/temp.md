# Templates <a id="temp">[[temp]]</a>

A *template* defines a family of classes or functions or an alias for a
family of types.

``` bnf
template-declaration:
  'template <' template-parameter-list '>' declaration
```

``` bnf
template-parameter-list:
  template-parameter
  template-parameter-list ',' template-parameter
```

The `>` token following the of a may be the product of replacing a
`>{>}` token by two consecutive `>` tokens ([[temp.names]]).

The *declaration* in a *template-declaration* shall

- declare or define a function, a class, or a variable, or
- define a member function, a member class, a member enumeration, or a
  static data member of a class template or of a class nested within a
  class template, or
- define a member template of a class or class template, or
- be an *alias-declaration*.

A *template-declaration* is a *declaration*. A *template-declaration* is
also a definition if its *declaration* defines a function, a class, a
variable, or a static data member. A declaration introduced by a
template declaration of a variable is a *variable template*. A variable
template at class scope is a *static data member template*.

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
   constexpr pauli<T> sigma1 = { { 0, 1 }, { 1, 0 } };
  template<class T>
   constexpr pauli<T> sigma2 = { { 0, -1i }, { 1i, 0 } };
  template<class T>
   constexpr pauli<T> sigma3 = { { 1, 0 }, { 0, -1 } };
};
```

A *template-declaration* can appear only as a namespace scope or class
scope declaration. In a function template declaration, the last
component of the *declarator-id* shall not be a *template-id*. That last
component may be an *identifier*, an *operator-function-id*, a
*conversion-function-id*, or a *literal-operator-id*. In a class
template declaration, if the class name is a *simple-template-id*, the
declaration declares a class template partial specialization (
[[temp.class.spec]]).

In a *template-declaration*, explicit specialization, or explicit
instantiation the *init-declarator-list* in the declaration shall
contain at most one declarator. When such a declaration is used to
declare a class template, no declarator is permitted.

A template name has linkage ([[basic.link]]). A non-member function
template can have internal linkage; any other template name shall have
external linkage. Specializations (explicit or implicit) of a template
that has internal linkage are distinct from all specializations in other
translation units. A template, a template explicit specialization (
[[temp.expl.spec]]), and a class template partial specialization shall
not have C linkage. Use of a linkage specification other than C or C++
with any of these constructs is conditionally-supported, with
*implementation-defined* semantics. Template definitions shall obey the
one definition rule ([[basic.def.odr]]). Default arguments for function
templates and for member functions of class templates are considered
definitions for the purpose of template instantiation ([[temp.decls]])
and must also obey the one definition rule.

A class template shall not have the same name as any other template,
class, function, variable, enumeration, enumerator, namespace, or type
in the same scope ([[basic.scope]]), except as specified in (
[[temp.class.spec]]). Except that a function template can be overloaded
either by non-template functions ([[dcl.fct]]) with the same name or by
other function templates with the same name ([[temp.over]]), a template
name declared in namespace scope or in class scope shall be unique in
that scope.

A function template, member function of a class template, variable
template, or static data member of a class template shall be defined in
every translation unit in which it is implicitly instantiated (
[[temp.inst]]) unless the corresponding specialization is explicitly
instantiated ([[temp.explicit]]) in some translation unit; no
diagnostic is required.

## Template parameters <a id="temp.param">[[temp.param]]</a>

The syntax for *template-parameter*s is:

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

The `>` token following the of a may be the product of replacing a
`>{>}` token by two consecutive `>` tokens ([[temp.names]]).

There is no semantic difference between `class` and `typename` in a
*template-parameter*. `typename` followed by an *unqualified-id* names a
template type parameter. `typename` followed by a *qualified-id* denotes
the type in a non-type [^1] *parameter-declaration*. A storage class
shall not be specified in a *template-parameter* declaration. Types
shall not be defined in a *template-parameter* declaration. A template
parameter may be a class template. For example,

``` cpp
template<class T> class myarray { /* ... */ };

template<class K, class V, template<class T> class C = myarray>
class Map {
  C<K> key;
  C<V> value;
};
```

A *type-parameter* whose identifier does not follow an ellipsis defines
its *identifier* to be a *typedef-name* (if declared with `class` or
`typename`) or *template-name* (if declared with `template`) in the
scope of the template declaration. Because of the name lookup rules, a
*template-parameter* that could be interpreted as either a non-type
*template-parameter* or a *type-parameter* (because its *identifier* is
the name of an already existing class) is taken as a *type-parameter*.
For example,

``` cpp
class T { /* ... */ };
int i;

template<class T, T i> void f(T t) {
  T t1 = i;         // template-parameters T and i
  ::T t2 = ::i;     // global namespace members T and i
}
```

Here, the template `f` has a *type-parameter* called `T`, rather than an
unnamed non-type *template-parameter* of class `T`.

A non-type *template-parameter* shall have one of the following
(optionally *cv-qualified*) types:

- integral or enumeration type,
- pointer to object or pointer to function,
- lvalue reference to object or lvalue reference to function,
- pointer to member,
- `std::nullptr_t`.

Other types are disallowed either explicitly below or implicitly by the
rules governing the form of *template-argument*s ([[temp.arg]]). The
top-level *cv-qualifiers* on the *template-parameter* are ignored when
determining its type.

A non-type non-reference *template-parameter* is a prvalue. It shall not
be assigned to or in any other way have its value changed. A non-type
non-reference *template-parameter* cannot have its address taken. When a
non-type non-reference *template-parameter* is used as an initializer
for a reference, a temporary is always used.

``` cpp
template<const X& x, int i> void f() {
  i++;                          // error: change of template-parameter value

  &x;                           // OK
  &i;                           // error: address of non-reference template-parameter

  int& ri = i;                  // error: non-const reference bound to temporary
  const int& cri = i;           // OK: const reference bound to temporary
}
```

A non-type *template-parameter* shall not be declared to have floating
point, class, or void type.

``` cpp
template<double d> class X;     // error
template<double* pd> class Y;   // OK
template<double& rd> class Z;   // OK
```

A non-type *template-parameter* of type “array of `T`” or “function
returning `T`” is adjusted to be of type “pointer to `T`” or “pointer to
function returning `T`”, respectively.

``` cpp
template<int* a>   struct R { /* ... */ };
template<int b[5]> struct S { /* ... */ };
int p;
R<&p> w;                        // OK
S<&p> x;                        // OK due to parameter adjustment
int v[5];
R<v> y;                         // OK due to implicit argument conversion
S<v> z;                         // OK due to both adjustment and conversion
```

A *default template-argument* is a *template-argument* ([[temp.arg]])
specified after `=` in a *template-parameter*. A default
*template-argument* may be specified for any kind of
*template-parameter* (type, non-type, template) that is not a template
parameter pack ([[temp.variadic]]). A default *template-argument* may
be specified in a template declaration. A default *template-argument*
shall not be specified in the *template-parameter-list*s of the
definition of a member of a class template that appears outside of the
member’s class. A default *template-argument* shall not be specified in
a friend class template declaration. If a friend function template
declaration specifies a default *template-argument*, that declaration
shall be a definition and shall be the only declaration of the function
template in the translation unit.

The set of default *template-argument*s available for use with a
template declaration or definition is obtained by merging the default
arguments from the definition (if in scope) and all declarations in
scope in the same way default function arguments are (
[[dcl.fct.default]]).

``` cpp
template<class T1, class T2 = int> class A;
template<class T1 = int, class T2> class A;
```

is equivalent to

``` cpp
template<class T1 = int, class T2 = int> class A;
```

If a *template-parameter* of a class template or alias template has a
default *template-argument*, each subsequent *template-parameter* shall
either have a default *template-argument* supplied or be a template
parameter pack. If a *template-parameter* of a primary class template or
alias template is a template parameter pack, it shall be the last
*template-parameter*. A template parameter pack of a function template
shall not be followed by another template parameter unless that template
parameter can be deduced from the *parameter-type-list* of the function
template or has a default argument ([[temp.deduct]]).

``` cpp
template<class T1 = int, class T2> class B;   // error

// U can be neither deduced from the parameter-type-list nor specified
template<class... T, class... U> void f() { } // error
template<class... T, class U> void g() { }    // error
```

A *template-parameter* shall not be given default arguments by two
different declarations in the same scope.

``` cpp
template<class T = int> class X;
template<class T = int> class X { /*... */ }; // error
```

When parsing a default *template-argument* for a non-type
*template-parameter*, the first non-nested `>` is taken as the end of
the *template-parameter-list* rather than a greater-than operator.

``` cpp
template<int i = 3 > 4 >        // syntax error
class X { /* ... */ };

template<int i = (3 > 4) >      // OK
class Y { /* ... */ };
```

A *template-parameter* of a template *template-parameter* is permitted
to have a default *template-argument*. When such default arguments are
specified, they apply to the template *template-parameter* in the scope
of the template *template-parameter*.

``` cpp
template <class T = float> struct B {};
template <template <class TT = float> class T> struct A {
  inline void f();
  inline void g();
};
template <template <class TT> class T> void A<T>::f() {
  T<> t;            // error - TT has no default template argument
}
template <template <class TT = char> class T> void A<T>::g() {
    T<> t;          // OK - T<char>
}
```

If a *template-parameter* is a *type-parameter* with an ellipsis prior
to its optional *identifier* or is a *parameter-declaration* that
declares a parameter pack ([[dcl.fct]]), then the *template-parameter*
is a template parameter pack ([[temp.variadic]]). A template parameter
pack that is a *parameter-declaration* whose type contains one or more
unexpanded parameter packs is a pack expansion. Similarly, a template
parameter pack that is a *type-parameter* with a
*template-parameter-list* containing one or more unexpanded parameter
packs is a pack expansion. A template parameter pack that is a pack
expansion shall not expand a parameter pack declared in the same
*template-parameter-list*.

``` cpp
template <class... Types> class Tuple;                // Types is a template type parameter pack
                                                      // but not a pack expansion
template <class T, int... Dims> struct multi_array;   // Dims is a non-type template parameter pack
                                                      // but not a pack expansion
template<class... T> struct value_holder {
  template<T... Values> struct apply { };             // Values is a non-type template parameter pack
                                                      // and a pack expansion
};
template<class... T, T... Values> struct static_array;// error: Values expands template type parameter
                                                      // pack T within the same template parameter list
```

## Names of template specializations <a id="temp.names">[[temp.names]]</a>

A template specialization ([[temp.spec]]) can be referred to by a
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

The name lookup rules ([[basic.lookup]]) are used to associate the use
of a name with a template declaration; that is, to identify a name as a
*template-name*.

For a *template-name* to be explicitly qualified by the template
arguments, the name must be known to refer to a template.

After name lookup ([[basic.lookup]]) finds that a name is a
*template-name* or that an *operator-function-id* or a
*literal-operator-id* refers to a set of overloaded functions any member
of which is a function template, if this is followed by a `<`, the `<`
is always taken as the delimiter of a *template-argument-list* and never
as the less-than operator. When parsing a *template-argument-list*, the
first non-nested `>`[^2] is taken as the ending delimiter rather than a
greater-than operator. Similarly, the first non-nested `>{>}` is treated
as two consecutive but distinct `>` tokens, the first of which is taken
as the end of the and completes the . The second `>` token produced by
this replacement rule may terminate an enclosing construct or it may be
part of a different construct (e.g. a cast).

``` cpp
template<int i> class X { /* ... */ }

X< 1>2 > x1;                        // syntax error
X<(1>2)> x2;                        // OK

template<class T> class Y { /* ... */ }
Y<X<1>> x3;                         // OK, same as Y<X<1> > x3;
Y<X<6>>1>> x4;                      // syntax error
Y<X<(6>>1)>> x5;                    // OK
```

When the name of a member template specialization appears after `.` or
`->` in a *postfix-expression* or after a *nested-name-specifier* in a
*qualified-id*, and the object expression of the *postfix-expression* is
type-dependent or the *nested-name-specifier* in the *qualified-id*
refers to a dependent type, but the name is not a member of the current
instantiation ([[temp.dep.type]]), the member template name must be
prefixed by the keyword `template`. Otherwise the name is assumed to
name a non-template.

``` cpp
struct X {
  template<std::size_t> X* alloc();
  template<std::size_t> static X* adjust();
};
template<class T> void f(T* p) {
  T* p1 = p->alloc<200>();          // ill-formed: < means less than
  T* p2 = p->template alloc<200>(); // OK: < starts template argument list
  T::adjust<100>();                 // ill-formed: < means less than
  T::template adjust<100>();        // OK: < starts template argument list
}
```

A name prefixed by the keyword `template` shall be a *template-id* or
the name shall refer to a class template. The keyword `template` may not
be applied to non-template members of class templates. As is the case
with the `typename` prefix, the `template` prefix is allowed in cases
where it is not strictly necessary; i.e., when the
*nested-name-specifier* or the expression on the left of the `->` or `.`
is not dependent on a *template-parameter*, or the use does not appear
in the scope of a template.

``` cpp
template <class T> struct A {
  void f(int);
  template <class U> void f(U);
};

template <class T> void f(T t) {
  A<T> a;
  a.template f<>(t);                // OK: calls template
  a.template f(t);                  // error: not a template-id
}

template <class T> struct B {
  template <class T2> struct C { };
};

// OK: T::template C names a class template:
template <class T, template <class X> class TT = T::template C> struct D { };
D<B<int> > db;
```

A *simple-template-id* that names a class template specialization is a
*class-name* (Clause  [[class]]).

A *template-id* that names an alias template specialization is a
*type-name*.

## Template arguments <a id="temp.arg">[[temp.arg]]</a>

There are three forms of *template-argument*, corresponding to the three
forms of *template-parameter*: type, non-type and template. The type and
form of each *template-argument* specified in a *template-id* shall
match the type and form specified for the corresponding parameter
declared by the template in its *template-parameter-list*. When the
parameter declared by the template is a template parameter pack (
[[temp.variadic]]), it will correspond to zero or more
*template-argument*s.

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
typedef std::complex<double> dcomplex;  // std::complex is a standard
                                        // library template
Array<dcomplex> v2(30);
Array<dcomplex> v3(40);

void bar() {
  v1[3] = 7;
  v2[3] = v3.elem(4) = dcomplex(7,8);
}
```

In a *template-argument*, an ambiguity between a *type-id* and an
expression is resolved to a *type-id*, regardless of the form of the
corresponding *template-parameter*.[^3]

``` cpp
template<class T> void f();
template<int I> void f();

void g() {
  f<int()>();       // int() is a type-id: call the first f()
}
```

The name of a *template-argument* shall be accessible at the point where
it is used as a *template-argument*. If the name of the
*template-argument* is accessible at the point where it is used as a
*template-argument*, there is no further access restriction in the
resulting instantiation where the corresponding *template-parameter*
name is used.

``` cpp
template<class T> class X {
  static T t;
};

class Y {
private:
  struct S { /* ... */ };
  X<S> x;           // OK: S is accessible
                    // X<Y::S> has a static member of type Y::S
                    // OK: even though Y::S is private
};

X<Y::S> y;          // error: S not accessible
```

For a *template-argument* that is a class type or a class template, the
template definition has no special access rights to the members of the
*template-argument*.

``` cpp
template <template <class TT> class T> class A {
  typename T<int>::S s;
};

template <class U> class B {
private:
  struct S { /* ... */ };
};

A<B> b;             // ill-formed: A has no access to B::S
```

When template argument packs or default *template-argument*s are used, a
*template-argument* list can be empty. In that case the empty `<>`
brackets shall still be used as the *template-argument-list.*

``` cpp
template<class T = char> class String;
String<>* p;                    // OK: String<char>
String* q;                      // syntax error
template<class ... Elements> class Tuple;
Tuple<>* t;                     // OK: Elements is empty
Tuple* u;                       // syntax error
```

An explicit destructor call ([[class.dtor]]) for an object that has a
type that is a class template specialization may explicitly specify the
*template-argument*s.

``` cpp
template<class T> struct A {
  ~A();
};
void f(A<int>* p, A<int>* q) {
  p->A<int>::~A();              // OK: destructor call
  q->A<int>::~A<int>();         // OK: destructor call
}
```

If the use of a *template-argument* gives rise to an ill-formed
construct in the instantiation of a template specialization, the program
is ill-formed.

When the template in a *template-id* is an overloaded function template,
both non-template functions in the overload set and function templates
in the overload set for which the *template-argument*s do not match the
*template-parameter*s are ignored. If none of the function templates
have matching *template-parameter*s, the program is ill-formed.

A *template-argument* followed by an ellipsis is a pack expansion (
[[temp.variadic]]).

### Template type arguments <a id="temp.arg.type">[[temp.arg.type]]</a>

A *template-argument* for a *template-parameter* which is a type shall
be a *type-id*.

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

A template type argument may be an incomplete type ([[basic.types]]).

If a declaration acquires a function type through a type dependent on a
*template-parameter* and this causes a declaration that does not use the
syntactic form of a function declarator to have function type, the
program is ill-formed.

``` cpp
template<class T> struct A {
  static T t;
};
typedef int function();
A<function> a;                  // ill-formed: would declare A<function>::t
                                // as a static member function
```

### Template non-type arguments <a id="temp.arg.nontype">[[temp.arg.nontype]]</a>

A *template-argument* for a non-type, non-template *template-parameter*
shall be one of:

- for a non-type *template-parameter* of integral or enumeration type, a
  converted constant expression ([[expr.const]]) of the type of the
  *template-parameter*; or
- the name of a non-type *template-parameter*; or
- a constant expression ([[expr.const]]) that designates the address of
  a complete object with static storage duration and external or
  internal linkage or a function with external or internal linkage,
  including function templates and function *template-id*s but excluding
  non-static class members, expressed (ignoring parentheses) as `&`
  *id-expression*, where the *id-expression* is the name of an object or
  function, except that the `&` may be omitted if the name refers to a
  function or array and shall be omitted if the corresponding
  *template-parameter* is a reference; or
- a constant expression that evaluates to a null pointer value (
  [[conv.ptr]]); or
- a constant expression that evaluates to a null member pointer value (
  [[conv.mem]]); or
- a pointer to member expressed as described in  [[expr.unary.op]]; or
- a constant expression of type `std::nullptr_t`.

A string literal ([[lex.string]]) does not satisfy the requirements of
any of these categories and thus is not an acceptable
*template-argument*.

``` cpp
template<class T, const char* p> class X {
  /* ... */
};

X<int, "Studebaker"> x1;        // error: string literal as template-argument

const char p[] = "Vivisectionist";
X<int,p> x2;                    // OK
```

Addresses of array elements and names or addresses of non-static class
members are not acceptable *template-argument*s.

``` cpp
template<int* p> class X { };

int a[10];
struct S { int m; static int s; } s;

X<&a[2]> x3;                    // error: address of array element
X<&s.m> x4;                     // error: address of non-static member
X<&s.s> x5;                     // error: &S::s must be used
X<&S::s> x6;                    // OK: address of static member
```

Temporaries, unnamed lvalues, and named lvalues with no linkage are not
acceptable *template-argument*s when the corresponding
*template-parameter* has reference type.

``` cpp
template<const int& CRI> struct B { /* ... */ };

B<1> b2;                        // error: temporary would be required for template argument

int c = 1;
B<c> b1;                        // OK
```

The following conversions are performed on each expression used as a
non-type *template-argument*. If a non-type *template-argument* cannot
be converted to the type of the corresponding *template-parameter* then
the program is ill-formed.

- For a non-type *template-parameter* of integral or enumeration type,
  conversions permitted in a converted constant expression (
  [[expr.const]]) are applied.
- for a non-type *template-parameter* of type pointer to object,
  qualification conversions ([[conv.qual]]) and the array-to-pointer
  conversion ([[conv.array]]) are applied; if the *template-argument*
  is of type `std::nullptr_t`, the null pointer conversion (
  [[conv.ptr]]) is applied. In particular, neither the null pointer
  conversion for a zero-valued integer literal ([[conv.ptr]]) nor the
  derived-to-base conversion ([[conv.ptr]]) are applied. Although `0`
  is a valid *template-argument* for a non-type *template-parameter* of
  integral type, it is not a valid *template-argument* for a non-type
  *template-parameter* of pointer type. However, both `(int*)0` and
  `nullptr` are valid *template-argument*s for a non-type
  *template-parameter* of type “pointer to int.”
- For a non-type *template-parameter* of type reference to object, no
  conversions apply. The type referred to by the reference may be more
  cv-qualified than the (otherwise identical) type of the
  *template-argument*. The *template-parameter* is bound directly to the
  *template-argument*, which shall be an lvalue.
- For a non-type *template-parameter* of type pointer to function, the
  function-to-pointer conversion ([[conv.func]]) is applied; if the
  *template-argument* is of type `std::nullptr_t`, the null pointer
  conversion ([[conv.ptr]]) is applied. If the *template-argument*
  represents a set of overloaded functions (or a pointer to such), the
  matching function is selected from the set ([[over.over]]).
- For a non-type *template-parameter* of type reference to function, no
  conversions apply. If the *template-argument* represents a set of
  overloaded functions, the matching function is selected from the set (
  [[over.over]]).
- For a non-type *template-parameter* of type pointer to member
  function, if the *template-argument* is of type `std::nullptr_t`, the
  null member pointer conversion ([[conv.mem]]) is applied; otherwise,
  no conversions apply. If the *template-argument* represents a set of
  overloaded member functions, the matching member function is selected
  from the set ([[over.over]]).
- For a non-type *template-parameter* of type pointer to data member,
  qualification conversions ([[conv.qual]]) are applied; if the
  *template-argument* is of type `std::nullptr_t`, the null member
  pointer conversion ([[conv.mem]]) is applied.

``` cpp
template<const int* pci> struct X { /* ... */ };
int ai[10];
X<ai> xi;                       // array to pointer and qualification conversions

struct Y { /* ... */ };
template<const Y& b> struct Z { /* ... */ };
Y y;
Z<y> z;                         // no conversion, but note extra cv-qualification

template<int (&pa)[5]> struct W { /* ... */ };
int b[5];
W<b> w;                         // no conversion

void f(char);
void f(int);

template<void (*pf)(int)> struct A { /* ... */ };

A<&f> a;                        // selects f(int)
```

### Template template arguments <a id="temp.arg.template">[[temp.arg.template]]</a>

A *template-argument* for a template *template-parameter* shall be the
name of a class template or an alias template, expressed as
*id-expression*. When the *template-argument* names a class template,
only primary class templates are considered when matching the template
template argument with the corresponding parameter; partial
specializations are not considered even if their parameter lists match
that of the template template parameter.

Any partial specializations ([[temp.class.spec]]) associated with the
primary class template or primary variable template are considered when
a specialization based on the template *template-parameter* is
instantiated. If a specialization is not visible at the point of
instantiation, and it would have been selected had it been visible, the
program is ill-formed; no diagnostic is required.

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
C<A> c;                         // V<int> within C<A> uses the primary template,
                                // so c.y.x has type int
                                // V<int*> within C<A> uses the partial specialization,
                                // so c.z.x has type long
```

A *template-argument* matches a template *template-parameter* (call it
`P`) when each of the template parameters in the
*template-parameter-list* of the *template-argument*’s corresponding
class template or alias template (call it `A`) matches the corresponding
template parameter in the *template-parameter-list* of `P`. Two template
parameters match if they are of the same kind (type, non-type,
template), for non-type *template-parameter*s, their types are
equivalent ([[temp.over.link]]), and for template
*template-parameter*s, each of their corresponding *template-parameter*s
matches, recursively. When `P`’s *template-parameter-list* contains a
template parameter pack ([[temp.variadic]]), the template parameter
pack will match zero or more template parameters or template parameter
packs in the *template-parameter-list* of `A` with the same type and
form as the template parameter pack in `P` (ignoring whether those
template parameters are template parameter packs).

``` cpp
template<class T> class A { /* ... */ };
template<class T, class U = T> class B { /* ... */ };
template <class ... Types> class C { /* ... */ };

template<template<class> class P> class X { /* ... */ };
template<template<class ...> class Q> class Y { /* ... */ };

X<A> xa;            // OK
X<B> xb;            // ill-formed: default arguments for the parameters of a template argument are ignored
X<C> xc;            // ill-formed: a template parameter pack does not match a template parameter

Y<A> ya;            // OK
Y<B> yb;            // OK
Y<C> yc;            // OK
```

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

## Type equivalence <a id="temp.type">[[temp.type]]</a>

Two *template-id*s refer to the same class, function, or variable if

- their *template-name*s, *operator-function-id*s, or
  *literal-operator-id*s refer to the same template and
- their corresponding type *template-argument*s are the same type and
- their corresponding non-type template arguments of integral or
  enumeration type have identical values and
- their corresponding non-type *template-argument*s of pointer type
  refer to the same external object or function or are both the null
  pointer value and
- their corresponding non-type *template-argument*s of pointer-to-member
  type refer to the same class member or are both the null member
  pointer value and
- their corresponding non-type *template-argument*s of reference type
  refer to the same external object or function and
- their corresponding template *template-argument*s refer to the same
  template.

``` cpp
template<class E, int size> class buffer { /* ... */ };
buffer<char,2*512> x;
buffer<char,1024> y;
```

declares `x` and `y` to be of the same type, and

``` cpp
template<class T, void(*err_fct)()> class list { /* ... */ };
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

If an expression e involves a template parameter, `decltype(e)` denotes
a unique dependent type. Two such *decltype-specifier*s refer to the
same type only if their *expression*s are equivalent (
[[temp.over.link]]). however, it may be aliased, e.g., by a
*typedef-name*.

## Template declarations <a id="temp.decls">[[temp.decls]]</a>

A *template-id*, that is, the *template-name* followed by a
*template-argument-list* shall not be specified in the declaration of a
primary template declaration.

``` cpp
template<class T1, class T2, int I> class A<T1, T2, I> { };     // error
template<class T1, int I> void sort<T1, I>(T1 data[I]);         // error
```

However, this syntax is allowed in class template partial
specializations ([[temp.class.spec]]).

For purposes of name lookup and instantiation, default arguments and
*exception-specification*s of function templates and default arguments
and *exception-specification*s of member functions of class templates
are considered definitions; each default argument or
*exception-specification* is a separate definition which is unrelated to
the function template definition or to any other default arguments or
*exception-specification*s.

Because an *alias-declaration* cannot declare a *template-id*, it is not
possible to partially or explicitly specialize an alias template.

### Class templates <a id="temp.class">[[temp.class]]</a>

A class *template* defines the layout and operations for an unbounded
set of related types. a single class template `List` might provide a
common definition for list of `int`, list of `float`, and list of
pointers to `Shape`s.

An array class template might be declared like this:

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

The prefix `template` `<class` `T>` specifies that a template is being
declared and that a *type-name* `T` will be used in the declaration. In
other words, `Array` is a parameterized type with `T` as its parameter.

When a member function, a member class, a member enumeration, a static
data member or a member template of a class template is defined outside
of the class template definition, the member definition is defined as a
template definition in which the *template-parameter*s are those of the
class template. The names of the template parameters used in the
definition of the member may be different from the template parameter
names used in the class template definition. The template argument list
following the class template name in the member definition shall name
the parameters in the same order as the one used in the template
parameter list of the member. Each template parameter pack shall be
expanded with an ellipsis in the template argument list.

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

template<class ... Types> void B<Types ...>::f3() { }    // OK
template<class ... Types> void B<Types>::f4() { }        // error
```

In a redeclaration, partial specialization, explicit specialization or
explicit instantiation of a class template, the *class-key* shall agree
in kind with the original class template declaration (
[[dcl.type.elab]]).

#### Member functions of class templates <a id="temp.mem.func">[[temp.mem.func]]</a>

A member function of a class template may be defined outside of the
class template definition in which it is declared.

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

declares three function templates. The subscript function might be
defined like this:

``` cpp
template<class T> T& Array<T>::operator[](int i) {
  if (i<0 || sz<=i) error("Array: range error");
  return v[i];
}
```

The *template-argument*s for a member function of a class template are
determined by the *template-argument*s of the type of the object for
which the member function is called. the *template-argument* for
`Array<T> :: operator [] ()` will be determined by the `Array` to which
the subscripting operation is applied.

``` cpp
Array<int> v1(20);
Array<dcomplex> v2(30);

v1[3] = 7;                      // Array<int>::operator[]()
v2[3] = dcomplex(7,8);          // Array<dcomplex>::operator[]()
```

#### Member classes of class templates <a id="temp.mem.class">[[temp.mem.class]]</a>

A member class of a class template may be defined outside the class
template definition in which it is declared. The member class must be
defined before its first use that requires an instantiation (
[[temp.inst]]). For example,

``` cpp
template<class T> struct A {
  class B;
};
A<int>::B* b1;                  // OK: requires A to be defined but not A::B
template<class T> class A<T>::B { };
A<int>::B  b2;                  // OK: requires A::B to be defined
```

#### Static data members of class templates <a id="temp.static">[[temp.static]]</a>

A definition for a static data member or static data member template may
be provided in a namespace scope enclosing the definition of the static
member’s class template.

``` cpp
template<class T> class X {
  static T s;
};
template<class T> T X<T>::s = 0;

struct limits {
  template<class T>
    static const T min;           // declaration
};

template<class T>
  const T limits::min = { };      // definition
```

An explicit specialization of a static data member declared as an array
of unknown bound can have a different bound from its definition, if any.

``` cpp
template <class T> struct A {
  static int i[];
};
template <class T> int A<T>::i[4];    // 4 elements
template <> int A<int>::i[] = { 1 };  // OK: 1 element
```

#### Enumeration members of class templates <a id="temp.mem.enum">[[temp.mem.enum]]</a>

An enumeration member of a class template may be defined outside the
class template definition.

``` cpp
template<class T> struct A {
  enum E : T;
};
A<int> a;
template<class T> enum A<T>::E : T { e1, e2 };
A<int>::E e = A<int>::e1;
```

### Member templates <a id="temp.mem">[[temp.mem]]</a>

A template can be declared within a class or class template; such a
template is called a member template. A member template can be defined
within or outside its class definition or class template definition. A
member template of a class template that is defined outside of its class
template definition shall be specified with the *template-parameter*s of
the class template followed by the *template-parameter*s of the member
template.

``` cpp
template<class T> struct string {
  template<class T2> int compare(const T2&);
  template<class T2> string(const string<T2>& s) { /* ... */ }
};

template<class T> template<class T2> int string<T>::compare(const T2& s) {
}
```

A local class of non-closure type shall not have member templates.
Access control rules (Clause  [[class.access]]) apply to member template
names. A destructor shall not be a member template. A non-template
member function ([[dcl.fct]]) with a given name and type and a member
function template of the same name, which could be used to generate a
specialization of the same type, can both be declared in a class. When
both exist, a use of that name and type refers to the non-template
member unless an explicit template argument list is supplied.

``` cpp
template <class T> struct A {
  void f(int);
  template <class T2> void f(T2);
};

template <> void A<int>::f(int) { }                     // non-template member function
template <> template <> void A<int>::f<>(int) { }       // member function template specialization

int main() {
  A<char> ac;
  ac.f(1);          // non-template
  ac.f('c');        // template
  ac.f<>(1);        // template
}
```

A member function template shall not be virtual.

``` cpp
template <class T> struct AA {
  template <class C> virtual void g(C);   // error
  virtual void f();                       // OK
};
```

A specialization of a member function template does not override a
virtual function from a base class.

``` cpp
class B {
  virtual void f(int);
};

class D : public B {
  template <class T> void f(T); // does not override B::f(int)
  void f(int i) { f<>(i); }     // overriding function that calls
                                // the template instantiation
};
```

A specialization of a conversion function template is referenced in the
same way as a non-template conversion function that converts to the same
type.

``` cpp
struct A {
  template <class T> operator T*();
};
template <class T> A::operator T*(){ return 0; }
template <> A::operator char*(){ return 0; }    // specialization
template A::operator void*();                   // explicit instantiation

int main() {
  A a;
  int* ip;
  ip = a.operator int*();       // explicit call to template operator
                                // A::operator int*()
}
```

Because the explicit template argument list follows the function
template name, and because conversion member function templates and
constructor member function templates are called without using a
function name, there is no way to provide an explicit template argument
list for these function templates.

A specialization of a conversion function template is not found by name
lookup. Instead, any conversion function templates visible in the
context of the use are considered. For each such operator, if argument
deduction succeeds ([[temp.deduct.conv]]), the resulting specialization
is used as if found by name lookup.

A *using-declaration* in a derived class cannot refer to a
specialization of a conversion function template in a base class.

Overload resolution ([[over.ics.rank]]) and partial ordering (
[[temp.func.order]]) are used to select the best conversion function
among multiple specializations of conversion function templates and/or
non-template conversion functions.

### Variadic templates <a id="temp.variadic">[[temp.variadic]]</a>

A *template parameter pack* is a template parameter that accepts zero or
more template arguments.

``` cpp
template<class ... Types> struct Tuple { };

Tuple<> t0;                     // Types contains no arguments
Tuple<int> t1;                  // Types contains one argument: int
Tuple<int, float> t2;           // Types contains two arguments: int and float
Tuple<0> error;                 // error: 0 is not a type
```

A *function parameter pack* is a function parameter that accepts zero or
more function arguments.

``` cpp
template<class ... Types> void f(Types ... args);

f();                // OK: args contains no arguments
f(1);               // OK: args contains one argument: int
f(2, 1.0);          // OK: args contains two arguments: int and double
```

A *parameter pack* is either a template parameter pack or a function
parameter pack.

A *pack expansion* consists of a *pattern* and an ellipsis, the
instantiation of which produces zero or more instantiations of the
pattern in a list (described below). The form of the pattern depends on
the context in which the expansion occurs. Pack expansions can occur in
the following contexts:

- In a function parameter pack ([[dcl.fct]]); the pattern is the
  *parameter-declaration* without the ellipsis.
- In a template parameter pack that is a pack expansion (
  [[temp.param]]):
  - if the template parameter pack is a *parameter-declaration*; the
    pattern is the *parameter-declaration* without the ellipsis;
  - if the template parameter pack is a *type-parameter* with a
    *template-parameter-list*; the pattern is the corresponding
    *type-parameter* without the ellipsis.
- In an *initializer-list* ([[dcl.init]]); the pattern is an
  *initializer-clause*.
- In a *base-specifier-list* (Clause  [[class.derived]]); the pattern is
  a *base-specifier*.
- In a *mem-initializer-list* ([[class.base.init]]) for a
  *mem-initializer* whose *mem-initializer-id* denotes a base class; the
  pattern is the *mem-initializer*.
- In a *template-argument-list* ([[temp.arg]]); the pattern is a
  *template-argument*.
- In a *dynamic-exception-specification* ([[except.spec]]); the pattern
  is a *type-id*.
- In an *attribute-list* ([[dcl.attr.grammar]]); the pattern is an
  *attribute*.
- In an *alignment-specifier* ([[dcl.align]]); the pattern is the
  *alignment-specifier* without the ellipsis.
- In a *capture-list* ([[expr.prim.lambda]]); the pattern is a
  *capture*.
- In a `sizeof...` expression ([[expr.sizeof]]); the pattern is an
  *identifier*.

For the purpose of determining whether a parameter pack satisfies a rule
regarding entities other than parameter packs, the parameter pack is
considered to be the entity that would result from an instantiation of
the pattern in which it appears.

``` cpp
template<class ... Types> void f(Types ... rest);
template<class ... Types> void g(Types ... rest) {
  f(&rest ...);     // ``&rest ...'' is a pack expansion; ``&rest'' is its pattern
}
```

A parameter pack whose name appears within the pattern of a pack
expansion is expanded by that pack expansion. An appearance of the name
of a parameter pack is only expanded by the innermost enclosing pack
expansion. The pattern of a pack expansion shall name one or more
parameter packs that are not expanded by a nested pack expansion; such
parameter packs are called *unexpanded* parameter packs in the pattern.
All of the parameter packs expanded by a pack expansion shall have the
same number of arguments specified. An appearance of a name of a
parameter pack that is not expanded is ill-formed.

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
  void g(Args ... args) {               // OK: Args is expanded by the function parameter pack args
    f(const_cast<const Args*>(&args)...); // OK: ``Args'' and ``args'' are expanded
    f(5 ...);                             // error: pattern does not contain any parameter packs
    f(args);                              // error: parameter pack ``args'' is not expanded
    f(h(args ...) + args ...);            // OK: first ``args'' expanded within h, second
                                          // ``args'' expanded within f
  }
```

The instantiation of a pack expansion that is not a `sizeof...`
expression produces a list
$\mathtt{E}_1, \mathtt{E}_2, ..., \mathtt{E}_N$, where N is the number
of elements in the pack expansion parameters. Each Eᵢ is generated by
instantiating the pattern and replacing each pack expansion parameter
with its ith element. Such an element, in the context of the
instantiation, is interpreted as follows:

- if the pack is a template parameter pack, the element is a template
  parameter ([[temp.param]]) of the corresponding kind (type or
  non-type) designating the type or value from the template argument;
  otherwise,
- if the pack is a function parameter pack, the element is an
  *id-expression* designating the function parameter that resulted from
  the instantiation of the pattern where the pack is declared.

All of the Eᵢ become elements in the enclosing list. The variety of list
varies with the context: *expression-list*, *base-specifier-list*,
*template-argument-list*, etc. When N is zero, the instantiation of the
expansion produces an empty list. Such an instantiation does not alter
the syntactic interpretation of the enclosing construct, even in cases
where omitting the list entirely would otherwise be ill-formed or would
result in an ambiguity in the grammar.

``` cpp
template<class... T> struct X : T... { };
template<class... T> void f(T... values) {
  X<T...> x(values...);
}

template void f<>();  // OK: X<> has no base classes
                      // x is a variable of type X<> that is value-initialized
```

The instantiation of a `sizeof...` expression ([[expr.sizeof]])
produces an integral constant containing the number of elements in the
parameter pack it expands.

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
  template ([[temp.deduct.decl]]), otherwise,
- the name shall be an *unqualified-id* that declares (or redeclares) a
  non-template function.

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

A friend template may be declared within a class or class template. A
friend function template may be defined within a class or class
template, but a friend class template may not be defined in a class or
class template. In these cases, all specializations of the friend class
or friend function template are friends of the class or class template
granting friendship.

``` cpp
class A {
  template<class T> friend class B;                 // OK
  template<class T> friend void f(T){ /* ... */ }  // OK
};
```

A template friend declaration specifies that all specializations of that
template, whether they are implicitly instantiated ([[temp.inst]]),
partially specialized ([[temp.class.spec]]) or explicitly specialized (
[[temp.expl.spec]]), are friends of the class containing the template
friend declaration.

``` cpp
class X {
  template<class T> friend struct A;
  class Y { };
};

template<class T> struct A { X::Y ab; };            // OK
template<class T> struct A<T*> { X::Y ab; };        // OK
```

When a function is defined in a friend function declaration in a class
template, the function is instantiated when the function is odr-used (
[[basic.def.odr]]). The same restrictions on multiple declarations and
definitions that apply to non-template function declarations and
definitions also apply to these implicit definitions.

A member of a class template may be declared to be a friend of a
non-template class. In this case, the corresponding member of every
specialization of the class template is a friend of the class granting
friendship. For explicit specializations the corresponding member is the
member (if any) that has the same name, kind (type, function, class
template, or function template), template parameters, and signature as
the member of the class template instantiation that would otherwise have
been generated.

``` cpp
template<class T> struct A {
  struct B { };
  void f();
  struct D {
    void g();
  };
};
template<> struct A<int> {
  struct B { };
  int f();
  struct D {
    void g();
  };
};

class C {
  template<class T> friend struct A<T>::B;    // grants friendship to A<int>::B even though
                                              // it is not a specialization of A<T>::B
  template<class T> friend void A<T>::f();    // does not grant friendship to A<int>::f()
                                              // because its return type does not match
  template<class T> friend void A<T>::D::g(); // does not grant friendship to A<int>::D::g()
                                              // because A<int>::D is not a specialization of A<T>::D
};
```

A friend declaration may first declare a member of an enclosing
namespace scope ([[temp.inject]]).

A friend template shall not be declared in a local class.

Friend declarations shall not declare partial specializations.

``` cpp
template<class T> class A { };
class X {
  template<class T> friend class A<T*>; // error
};
```

When a friend declaration refers to a specialization of a function
template, the function parameter declarations shall not include default
arguments, nor shall the inline specifier be used in such a declaration.

### Class template partial specializations <a id="temp.class.spec">[[temp.class.spec]]</a>

A *primary* class template declaration is one in which the class
template name is an identifier. A template declaration in which the
class template name is a *simple-template-id* is a *partial
specialization* of the class template named in the *simple-template-id*.
A partial specialization of a class template provides an alternative
definition of the template that is used instead of the primary
definition when the arguments in a specialization match those given in
the partial specialization ([[temp.class.spec.match]]). The primary
template shall be declared before any specializations of that template.
A partial specialization shall be declared before the first use of a
class template specialization that would make use of the partial
specialization as the result of an implicit or explicit instantiation in
every translation unit in which such a use occurs; no diagnostic is
required.

Each class template partial specialization is a distinct template and
definitions shall be provided for the members of a template partial
specialization ([[temp.class.spec.mfunc]]).

``` cpp
template<class T1, class T2, int I> class A             { };    // #1
template<class T, int I>            class A<T, T*, I>   { };    // #2
template<class T1, class T2, int I> class A<T1*, T2, I> { };    // #3
template<class T>                   class A<int, T*, 5> { };    // #4
template<class T1, class T2, int I> class A<T1, T2*, I> { };    // #5
```

The first declaration declares the primary (unspecialized) class
template. The second and subsequent declarations declare partial
specializations of the primary template.

The template parameters are specified in the angle bracket enclosed list
that immediately follows the keyword `template`. For partial
specializations, the template argument list is explicitly written
immediately following the class template name. For primary templates,
this list is implicitly described by the template parameter list.
Specifically, the order of the template arguments is the sequence in
which they appear in the template parameter list. the template argument
list for the primary template in the example above is `<T1,` `T2,` `I>`.
The template argument list shall not be specified in the primary
template declaration. For example,

``` cpp
template<class T1, class T2, int I> class A<T1, T2, I>  { };    // error
```

A class template partial specialization may be declared or redeclared in
any namespace scope in which its definition may be defined (
[[temp.class]] and  [[temp.mem]]).

``` cpp
template<class T> struct A {
  struct C {
    template<class T2> struct B { };
  };
};

// partial specialization of A<T>::C::B<T2>
template<class T> template<class T2>
  struct A<T>::C::B<T2*> { };

A<short>::C::B<int*> absip;     // uses partial specialization
```

Partial specialization declarations themselves are not found by name
lookup. Rather, when the primary template name is used, any
previously-declared partial specializations of the primary template are
also considered. One consequence is that a *using-declaration* which
refers to a class template does not restrict the set of partial
specializations which may be found through the *using-declaration*.

``` cpp
namespace N {
  template<class T1, class T2> class A { };         // primary template
}

using N::A;                             // refers to the primary template

namespace N {
  template<class T> class A<T, T*> { }; // partial specialization
}

A<int,int*> a;                  // uses the partial specialization, which is found through
                                // the using declaration which refers to the primary template
```

A non-type argument is non-specialized if it is the name of a non-type
parameter. All other non-type arguments are specialized.

Within the argument list of a class template partial specialization, the
following restrictions apply:

- A partially specialized non-type argument expression shall not involve
  a template parameter of the partial specialization except when the
  argument expression is a simple *identifier*.
  ``` cpp
  template <int I, int J> struct A {};
  template <int I> struct A<I+5, I*2> {}; // error

  template <int I, int J> struct B {};
  template <int I> struct B<I, I> {};     // OK
  ```
- The type of a template parameter corresponding to a specialized
  non-type argument shall not be dependent on a parameter of the
  specialization.
  ``` cpp
  template <class T, T t> struct C {};
  template <class T> struct C<T, 1>;                  // error

  template< int X, int (*array_ptr)[X] > class A {};
  int array[5];
  template< int X > class A<X,&array> { };            // error
  ```
- The argument list of the specialization shall not be identical to the
  implicit argument list of the primary template.
- The specialization shall be more specialized than the primary
  template ([[temp.class.order]]).
- The template parameter list of a specialization shall not contain
  default template argument values.[^4]
- An argument shall not contain an unexpanded parameter pack. If an
  argument is a pack expansion ([[temp.variadic]]), it shall be the
  last argument in the template argument list.

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
  rules ([[temp.class.order]]) are used to determine whether one of the
  specializations is more specialized than the others. If none of the
  specializations is more specialized than all of the other matching
  specializations, then the use of the class template is ambiguous and
  the program is ill-formed.
- If no matches are found, the instantiation is generated from the
  primary template.

A partial specialization matches a given actual template argument list
if the template arguments of the partial specialization can be deduced
from the actual template argument list ([[temp.deduct]]).

``` cpp
A<int, int, 1>   a1;            // uses #1
A<int, int*, 1>  a2;            // uses #2, T is int, I is 1
A<int, char*, 5> a3;            // uses #4, T is char
A<int, char*, 1> a4;            // uses #5, T1 is int, T2 is char, I is 1
A<int*, int*, 2> a5;            // ambiguous: matches #3 and #5
```

A non-type template argument can also be deduced from the value of an
actual template argument of a non-type parameter of the primary
template. the declaration of `a2` above.

In a type name that refers to a class template specialization, (e.g.,
`A<int, int, 1>`) the argument list shall match the template parameter
list of the primary template. The template arguments of a specialization
are deduced from the arguments of the primary template.

#### Partial ordering of class template specializations <a id="temp.class.order">[[temp.class.order]]</a>

For two class template partial specializations, the first is at least as
specialized as the second if, given the following rewrite to two
function templates, the first function template is at least as
specialized as the second according to the ordering rules for function
templates ([[temp.func.order]]):

- the first function template has the same template parameters as the
  first partial specialization and has a single function parameter whose
  type is a class template specialization with the template arguments of
  the first partial specialization, and
- the second function template has the same template parameters as the
  second partial specialization and has a single function parameter
  whose type is a class template specialization with the template
  arguments of the second partial specialization.

``` cpp
template<int I, int J, class T> class X { };
template<int I, int J>          class X<I, J, int> { }; // #1
template<int I>                 class X<I, I, int> { }; // #2

template<int I, int J> void f(X<I, J, int>);            // A
template<int I>        void f(X<I, I, int>);            // B
```

The partial specialization `#2` is more specialized than the partial
specialization `#1` because the function template `B` is more
specialized than the function template `A` according to the ordering
rules for function templates.

#### Members of class template specializations <a id="temp.class.spec.mfunc">[[temp.class.spec.mfunc]]</a>

The template parameter list of a member of a class template partial
specialization shall match the template parameter list of the class
template partial specialization. The template argument list of a member
of a class template partial specialization shall match the template
argument list of the class template partial specialization. A class
template specialization is a distinct template. The members of the class
template partial specialization are unrelated to the members of the
primary template. Class template partial specialization members that are
used in a way that requires a definition shall be defined; the
definitions of members of the primary template are never used as
definitions for members of a class template partial specialization. An
explicit specialization of a member of a class template partial
specialization is declared in the same way as an explicit specialization
of the primary template.

``` cpp
// primary template
template<class T, int I> struct A {
  void f();
};

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
  a0.f();                       // OK, uses definition of primary template's member
  a2.g();                       // OK, uses definition of
                                // partial specialization's member
  a2.h();                       // OK, uses definition of
                                // explicit specialization's member
  a2.f();                       // ill-formed, no definition of f for A<T,2>
                                // the primary template is not used here
}
```

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

``` cpp
template<class T> struct A {
  template<class T2> struct B {};                     // #1
  template<class T2> struct B<T2*> {};                // #2
};

template<> template<class T2> struct A<short>::B {};  // #3

A<char>::B<int*>  abcip;  // uses #2
A<short>::B<int*> absip;  // uses #3
A<char>::B<int>  abci;    // uses #1
```

### Function templates <a id="temp.fct">[[temp.fct]]</a>

A function template defines an unbounded set of related functions. a
family of sort functions might be declared like this:

``` cpp
template<class T> class Array { };
template<class T> void sort(Array<T>&);
```

A function template can be overloaded with other function templates and
with non-template functions ([[dcl.fct]]). A non-template function is
not related to a function template (i.e., it is never considered to be a
specialization), even if it has the same name and type as a potentially
generated function template specialization.[^5]

#### Function template overloading <a id="temp.over.link">[[temp.over.link]]</a>

It is possible to overload function templates so that two different
function template specializations have the same type.

``` cpp
// file1.c
template<class T>
  void f(T*);
void g(int* p) {
  f(p); // calls f<int>(int*)
}
```

``` cpp
// file2.c
template<class T>
  void f(T);
void h(int* p) {
  f(p); // calls f<int*>(int*)
}
```

Such specializations are distinct functions and do not violate the one
definition rule ([[basic.def.odr]]).

The signature of a function template is defined in  [[intro.defs]]. The
names of the template parameters are significant only for establishing
the relationship between the template parameters and the rest of the
signature. Two distinct function templates may have identical function
return types and function parameter lists, even if overload resolution
alone cannot distinguish them.

``` cpp
template<class T> void f();
template<int I> void f();       // OK: overloads the first template
                                // distinguishable with an explicit template argument list
```

When an expression that references a template parameter is used in the
function parameter list or the return type in the declaration of a
function template, the expression that references the template parameter
is part of the signature of the function template. This is necessary to
permit a declaration of a function template in one translation unit to
be linked with another declaration of the function template in another
translation unit and, conversely, to ensure that function templates that
are intended to be distinct are not linked with one another.

``` cpp
template <int I, int J> A<I+J> f(A<I>, A<J>);   // #1
template <int K, int L> A<K+L> f(A<K>, A<L>);   // same as #1
template <int I, int J> A<I-J> f(A<I>, A<J>);   // different from #1
```

Most expressions that use template parameters use non-type template
parameters, but it is possible for an expression to reference a type
parameter. For example, a template type parameter can be used in the
`sizeof` operator.

Two expressions involving template parameters are considered
*equivalent* if two function definitions containing the expressions
would satisfy the one definition rule ([[basic.def.odr]]), except that
the tokens used to name the template parameters may differ as long as a
token used to name a template parameter in one expression is replaced by
another token that names the same template parameter in the other
expression. For determining whether two dependent names ([[temp.dep]])
are equivalent, only the name itself is considered, not the result of
name lookup in the context of the template. If multiple declarations of
the same function template differ in the result of this name lookup, the
result for the first declaration is used.

``` cpp
template <int I, int J> void f(A<I+J>);         // #1
template <int K, int L> void f(A<K+L>);         // same as #1

template <class T> decltype(g(T())) h();
int g(int);
template <class T> decltype(g(T())) h()         // redeclaration of h() uses the earlier lookup
  { return g(T()); }                            // ...although the lookup here does find g(int)
int i = h<int>();                               // template argument substitution fails; g(int)
                                                // was not in scope at the first declaration of h()
```

Two expressions involving template parameters that are not equivalent
are *functionally equivalent* if, for any given set of template
arguments, the evaluation of the expression results in the same value.

Two function templates are *equivalent* if they are declared in the same
scope, have the same name, have identical template parameter lists, and
have return types and parameter lists that are equivalent using the
rules described above to compare expressions involving template
parameters. Two function templates are *functionally equivalent* if they
are equivalent except that one or more expressions that involve template
parameters in the return types and parameter lists are functionally
equivalent using the rules described above to compare expressions
involving template parameters. If a program contains declarations of
function templates that are functionally equivalent but not equivalent,
the program is ill-formed; no diagnostic is required.

This rule guarantees that equivalent declarations will be linked with
one another, while not requiring implementations to use heroic efforts
to guarantee that functionally equivalent declarations will be treated
as distinct. For example, the last two declarations are functionally
equivalent and would cause a program to be ill-formed:

``` cpp
// Guaranteed to be the same
template <int I> void f(A<I>, A<I+10>);
template <int I> void f(A<I>, A<I+10>);

// Guaranteed to be different
template <int I> void f(A<I>, A<I+10>);
template <int I> void f(A<I>, A<I+11>);

// Ill-formed, no diagnostic required
template <int I> void f(A<I>, A<I+10>);
template <int I> void f(A<I>, A<I+1+2+3+4>);
```

#### Partial ordering of function templates <a id="temp.func.order">[[temp.func.order]]</a>

If a function template is overloaded, the use of a function template
specialization might be ambiguous because template argument deduction (
[[temp.deduct]]) may associate the function template specialization with
more than one function template declaration. *Partial ordering* of
overloaded function template declarations is used in the following
contexts to select the function template to which a function template
specialization refers:

- during overload resolution for a call to a function template
  specialization ([[over.match.best]]);
- when the address of a function template specialization is taken;
- when a placement operator delete that is a function template
  specialization is selected to match a placement operator new (
  [[basic.stc.dynamic.deallocation]], [[expr.new]]);
- when a friend function declaration ([[temp.friend]]), an explicit
  instantiation ([[temp.explicit]]) or an explicit specialization (
  [[temp.expl.spec]]) refers to a function template specialization.

Partial ordering selects which of two function templates is more
specialized than the other by transforming each template in turn (see
next paragraph) and performing template argument deduction using the
function type. The deduction process determines whether one of the
templates is more specialized than the other. If so, the more
specialized template is the one chosen by the partial ordering process.

To produce the transformed template, for each type, non-type, or
template template parameter (including template parameter packs (
[[temp.variadic]]) thereof) synthesize a unique type, value, or class
template respectively and substitute it for each occurrence of that
parameter in the function type of the template. If only one of the
function templates is a non-static member of some class `A`, that
function template is considered to have a new first parameter inserted
in its function parameter list. Given cv as the cv-qualifiers of the
function template (if any), the new parameter is of type “rvalue
reference to cv `A`” if the optional *ref-qualifier* of the function
template is `&&`, or of type “lvalue reference to cv `A`” otherwise.
This allows a non-static member to be ordered with respect to a
nonmember function and for the results to be equivalent to the ordering
of two equivalent nonmembers.

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
  b * a;                                            // calls #1a
}
```

Using the transformed function template’s function type, perform type
deduction against the other template as described in 
[[temp.deduct.partial]].

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
  g(x);             // Ambiguous: g(T) or g(T&)
  A<int> z;
  h(z);             // overload resolution selects h(A<T>&)
  const A<int> z2;
  h(z2);            // h(const T&) is called because h(A<T>&) is not callable
}
```

Since partial ordering in a call context considers only parameters for
which there are explicit call arguments, some parameters are ignored
(namely, function parameter packs, parameters with default arguments,
and ellipsis parameters).

``` cpp
template<class T> void f(T);            // #1
template<class T> void f(T*, int=1);    // #2
template<class T> void g(T);            // #3
template<class T> void g(T*, ...);      // #4
```

``` cpp
int main() {
  int* ip;
  f(ip);            // calls #2
  g(ip);            // calls #4
}
```

``` cpp
template<class T, class U> struct A { };

template<class T, class U> void f(U, A<U, T>* p = 0); // #1
template<         class U> void f(U, A<U, U>* p = 0); // #2
template<class T         > void g(T, T = T());        // #3
template<class T, class... U> void g(T, U ...);       // #4

void h() {
  f<int>(42, (A<int, int>*)0);                        // calls #2
  f<int>(42);                                         // error: ambiguous
  g(42);                                              // error: ambiguous
}
```

``` cpp
template<class T, class... U> void f(T, U...);        // #1
template<class T            > void f(T);              // #2
template<class T, class... U> void g(T*, U...);       // #3
template<class T            > void g(T);              // #4

void h(int i) {
  f(&i);                                              // error: ambiguous
  g(&i);                                              // OK: calls #3
}
```

### Alias templates <a id="temp.alias">[[temp.alias]]</a>

A *template-declaration* in which the *declaration* is an
*alias-declaration* (Clause  [[dcl.dcl]]) declares the *identifier* to
be a *alias template*. An alias template is a name for a family of
types. The name of the alias template is a *template-name*.

When a *template-id* refers to the specialization of an alias template,
it is equivalent to the associated type obtained by substitution of its
*template-argument*s for the *template-parameter*s in the *type-id* of
the alias template. An alias template name is never deduced.

``` cpp
template<class T> struct Alloc { /* ... */ };
template<class T> using Vec = vector<T, Alloc<T>>;
Vec<int> v;         // same as vector<int, Alloc<int>{> v;}

template<class T>
  void process(Vec<T>& v)
  { /* ... */ }

template<class T>
  void process(vector<T, Alloc<T>>& w)
  { /* ... */ }     // error: redefinition

template<template<class> class TT>
  void f(TT<int>);

f(v);               // error: Vec not deduced

template<template<class,class> class TT>
  void g(TT<int, Alloc<int>>);
g(v);               // OK: TT = vector
```

The *type-id* in an alias template declaration shall not refer to the
alias template being declared. The type produced by an alias template
specialization shall not directly or indirectly make use of that
specialization.

``` cpp
template <class T> struct A;
template <class T> using B = typename A<T>::U;
template <class T> struct A {
  typedef B<T> U;
};
B<short> b;         // error: instantiation of B<short> uses own type via A<short>::U
```

## Name resolution <a id="temp.res">[[temp.res]]</a>

Three kinds of names can be used within a template definition:

- The name of the template itself, and names declared within the
  template itself.
- Names dependent on a *template-parameter* ([[temp.dep]]).
- Names from scopes which are visible within the template definition.

A name used in a template declaration or definition and that is
dependent on a *template-parameter* is assumed not to name a type unless
the applicable name lookup finds a type name or the name is qualified by
the keyword `typename`.

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
    T::A* a7;                   // T::A is not a type name:
                                // multiply T::A by a7; ill-formed,
                                // no visible declaration of a7
    B* a8;                      // B is not a type name:
                                // multiply B by a8; ill-formed,
                                // no visible declarations of B and a8
  }
};
```

When a is intended to refer to a type that is not a member of the
current instantiation ([[temp.dep.type]]) and its refers to a dependent
type, it shall be prefixed by the keyword `typename`, forming a . If the
*qualified-id* in a *typename-specifier* does not denote a type, the
program is ill-formed.

``` bnf
typename-specifier:
  'typename' nested-name-specifier identifier
  'typename' nested-name-specifier 'template'ₒₚₜ simple-template-id
```

If a specialization of a template is instantiated for a set of
*template-argument*s such that the *qualified-id* prefixed by `typename`
does not denote a type, the specialization is ill-formed. The usual
qualified name lookup ([[basic.lookup.qual]]) is used to find the
*qualified-id* even in the presence of `typename`.

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

A qualified name used as the name in a *mem-initializer-id*, a
*base-specifier*, or an *elaborated-type-specifier* is implicitly
assumed to name a type, without the use of the `typename` keyword. In a
*nested-name-specifier* that immediately contains a
*nested-name-specifier* that depends on a template parameter, the
*identifier* or *simple-template-id* is implicitly assumed to name a
type, without the use of the `typename` keyword. The `typename` keyword
is not permitted by the syntax of these constructs.

If, for a given set of template arguments, a specialization of a
template is instantiated that refers to a *qualified-id* that denotes a
type, and the *qualified-id* refers to a member of an unknown
specialization, the *qualified-id* shall either be prefixed by
`typename` or shall be used in a context in which it implicitly names a
type as described above.

``` cpp
template <class T> void f(int i) {
  T::x * i;         // T::x must not be a type
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

Within the definition of a class template or within the definition of a
member of a class template following the *declarator-id*, the keyword
`typename` is not required when referring to the name of a previously
declared member of the class template that declares a type. such names
can be found using unqualified name lookup ([[basic.lookup.unqual]]),
class member lookup ([[class.qual]]) into the current instantiation (
[[temp.dep.type]]), or class member access expression lookup (
[[basic.lookup.classref]]) when the type of the object expression is the
current instantiation ([[temp.dep.expr]]).

``` cpp
template<class T> struct A {
  typedef int B;
  B b;              // OK, no typename required
};
```

Knowing which names are type names allows the syntax of every template
to be checked. No diagnostic shall be issued for a template for which a
valid specialization can be generated. If no valid specialization can be
generated for a template, and that template is not instantiated, the
template is ill-formed, no diagnostic required. If every valid
specialization of a variadic template requires an empty template
parameter pack, the template is ill-formed, no diagnostic required. If a
type used in a non-dependent name is incomplete at the point at which a
template is defined but is complete at the point at which an
instantiation is done, and if the completeness of that type affects
whether or not the program is well-formed or affects the semantics of
the program, the program is ill-formed; no diagnostic is required. If a
template is instantiated, errors will be diagnosed according to the
other rules in this Standard. Exactly when these errors are diagnosed is
a quality of implementation issue.

``` cpp
int j;
template<class T> class X {
  void f(T t, int i, char* p) {
    t = i;          // diagnosed if X::f is instantiated
                    // and the assignment to t is an error
    p = i;          // may be diagnosed even if X::f is
                    // not instantiated
    p = j;          // may be diagnosed even if X::f is
                    // not instantiated
  }
  void g(T t) {
    +;              // may be diagnosed even if X::g is
                    // not instantiated
  }
};

template<class... T> struct A {
  void operator++(int, T... t);                 // error: too many parameters
};
template<class... T> union X : T... { };        // error: union with base class
template<class... T> struct A : T...,  T... { };// error: duplicate base class
```

When looking for the declaration of a name used in a template
definition, the usual lookup rules ([[basic.lookup.unqual]],
[[basic.lookup.argdep]]) are used for non-dependent names. The lookup of
names dependent on the template parameters is postponed until the actual
template argument is known ([[temp.dep]]).

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

in the example, `i` is the local variable `i` declared in `printall`,
`cnt` is the member `cnt` declared in `Set`, and `cout` is the standard
output stream declared in `iostream`. However, not every declaration can
be found this way; the resolution of some names must be postponed until
the actual *template-argument*s are known. For example, even though the
name `operator<<` is known within the definition of `printall()` and a
declaration of it can be found in `<iostream>`, the actual declaration
of `operator<<` needed to print `p[i]` cannot be known until it is known
what type `T` is ([[temp.dep]]).

If a name does not depend on a *template-parameter* (as defined in 
[[temp.dep]]), a declaration (or set of declarations) for that name
shall be in scope at the point where the name appears in the template
definition; the name is bound to the declaration (or declarations) found
at that point and this binding is not affected by declarations that are
visible at the point of instantiation.

``` cpp
void f(char);

template<class T> void g(T t) {
  f(1);             // f(char)
  f(T(1));          // dependent
  f(t);             // dependent
  dd++;             // not dependent
                    // error: declaration for dd not found
}

enum E { e };
void f(E);

double dd;
void h() {
  g(e);             // will cause one call of f(char) followed
                    // by two calls of f(E)
  g('a');           // will cause three calls of f(char)
}
```

For purposes of name lookup, default arguments and
*exception-specification*s of function templates and default arguments
and *exception-specification*s of member functions of class templates
are considered definitions ([[temp.decls]]).

### Locally declared names <a id="temp.local">[[temp.local]]</a>

Like normal (non-template) classes, class templates have an
injected-class-name (Clause  [[class]]). The injected-class-name can be
used as a *template-name* or a *type-name*. When it is used with a
*template-argument-list*, as a *template-argument* for a template
*template-parameter*, or as the final identifier in the
*elaborated-type-specifier* of a friend class template declaration, it
refers to the class template itself. Otherwise, it is equivalent to the
*template-name* followed by the *template-parameter*s of the class
template enclosed in `<>`.

Within the scope of a class template specialization or partial
specialization, when the injected-class-name is used as a *type-name*,
it is equivalent to the *template-name* followed by the
*template-argument*s of the class template specialization or partial
specialization enclosed in `<>`.

``` cpp
template<template<class> class T> class A { };
template<class T> class Y;
template<> class Y<int> {
  Y* p;                               // meaning Y<int>
  Y<char>* q;                         // meaning Y<char>
  A<Y>* a;                            // meaning A<::Y>
  class B {
    template<class> friend class Y;   // meaning ::Y
  };
};
```

The injected-class-name of a class template or class template
specialization can be used either as a *template-name* or a *type-name*
wherever it is in scope.

``` cpp
template <class T> struct Base {
  Base* p;
};

template <class T> struct Derived: public Base<T> {
  typename Derived::Base* p;    // meaning Derived::Base<T>
};

template<class T, template<class> class U = T::template Base> struct Third { };
Third<Base<int> > t;            // OK: default argument uses injected-class-name as a template
```

A lookup that finds an injected-class-name ([[class.member.lookup]])
can result in an ambiguity in certain cases (for example, if it is found
in more than one base class). If all of the injected-class-names that
are found refer to specializations of the same class template, and if
the name is used as a *template-name*, the reference refers to the class
template itself and not a specialization thereof, and is not ambiguous.

``` cpp
template <class T> struct Base { };
template <class T> struct Derived: Base<int>, Base<char> {
  typename Derived::Base b;             // error: ambiguous
  typename Derived::Base<double> d;     // OK
};
```

When the normal name of the template (i.e., the name from the enclosing
scope, not the injected-class-name) is used, it always refers to the
class template itself and not a specialization of the template.

``` cpp
template<class T> class X {
  X* p;             // meaning X<T>
  X<T>* p2;
  X<int>* p3;
  ::X* p4;          // error: missing template argument list
                    // ::X does not refer to the injected-class-name
};
```

A *template-parameter* shall not be redeclared within its scope
(including nested scopes). A *template-parameter* shall not have the
same name as the template name.

``` cpp
template<class T, int i> class Y {
  int T;            // error: template-parameter redeclared
  void f() {
    char T;         // error: template-parameter redeclared
  }
};

template<class X> class X;      // error: template-parameter redeclared
```

In the definition of a member of a class template that appears outside
of the class template definition, the name of a member of the class
template hides the name of a *template-parameter* of any enclosing class
templates (but not a *template-parameter* of the member if the member is
a class or function template).

``` cpp
template<class T> struct A {
  struct B { /* ... */ }
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

In the definition of a member of a class template that appears outside
of the namespace containing the class template definition, the name of a
*template-parameter* hides the name of a member of this namespace.

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

In the definition of a class template or in the definition of a member
of such a template that appears outside of the template definition, for
each base class which does not depend on a *template-parameter* (
[[temp.dep]]), if the name of the base class or the name of a member of
the base class is the same as the name of a *template-parameter*, the
base class name or member name hides the *template-parameter* name (
[[basic.scope.hiding]]).

``` cpp
struct A {
  struct B { /* ... */ };
  int a;
  int Y;
};

template<class B, class a> struct X : A {
  B b;              // A's B
  a b;              // error: A's a isn't a type name
};
```

### Dependent names <a id="temp.dep">[[temp.dep]]</a>

Inside a template, some constructs have semantics which may differ from
one instantiation to another. Such a construct *depends* on the template
parameters. In particular, types and expressions may depend on the type
and/or value of template parameters (as determined by the template
arguments) and this determines the context for name lookup for certain
names. Expressions may be *type-dependent* (on the type of a template
parameter) or *value-dependent* (on the value of a non-type template
parameter). In an expression of the form:

where the *postfix-expression* is an *unqualified-id*, the
*unqualified-id* denotes a *dependent name* if

- any of the expressions in the *expression-list* is a pack expansion (
  [[temp.variadic]]),
- any of the expressions in the *expression-list* is a type-dependent
  expression ([[temp.dep.expr]]), or
- if the *unqualified-id* is a *template-id* in which any of the
  template arguments depends on a template parameter.

If an operand of an operator is a type-dependent expression, the
operator also denotes a dependent name. Such names are unbound and are
looked up at the point of the template instantiation ([[temp.point]])
in both the context of the template definition and the context of the
point of instantiation.

``` cpp
template<class T> struct X : B<T> {
  typename T::A* pa;
  void f(B<T>* pb) {
    static int i = B<T>::i;
    pb->j++;
  }
};
```

the base class name `B<T>`, the type name `T::A`, the names `B<T>::i`
and `pb->j` explicitly depend on the *template-parameter*.

In the definition of a class or class template, if a base class depends
on a *template-parameter*, the base class scope is not examined during
unqualified name lookup either at the point of definition of the class
template or member or during an instantiation of the class template or
member.

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

``` cpp
struct A {
  struct B { /* ... */ };
  int a;
  int Y;
};

int a;

template<class T> struct Y : T {
  struct B { /* ... */ };
  B b;                          // The B defined in Y
  void f(int i) { a = i; }      // ::a
  Y* p;                         // Y<T>
};

Y<A> ya;
```

The members `A::B`, `A::a`, and `A::Y` of the template argument `A` do
not affect the binding of names in `Y<A>`.

#### Dependent types <a id="temp.dep.type">[[temp.dep.type]]</a>

A name refers to the *current instantiation* if it is

- in the definition of a class template, a nested class of a class
  template, a member of a class template, or a member of a nested class
  of a class template, the injected-class-name (Clause  [[class]]) of
  the class template or nested class,
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
  (or an equivalent template alias specialization). If the *n*th
  template parameter is a parameter pack, the *n*th template argument is
  a pack expansion ([[temp.variadic]]) whose pattern is the name of the
  parameter pack.

The template argument list of a primary template is a template argument
list in which the *n*th template argument has the value of the *n*th
template parameter of the class template. If the *n*th template
parameter is a template parameter pack ([[temp.variadic]]), the *n*th
template argument is a pack expansion ([[temp.variadic]]) whose pattern
is the name of the template parameter pack.

A template argument that is equivalent to a template parameter (i.e.,
has the same constant value or the same type as the template parameter)
can be used in place of that template parameter in a reference to the
current instantiation. In the case of a non-type template argument, the
argument must have been given the value of the template parameter and
not an expression in which the template parameter appears as a
subexpression.

``` cpp
template <class T> class A {
  A* p1;                        // A is the current instantiation
  A<T>* p2;                     // A<T> is the current instantiation
  A<T*> p3;                     // A<T*> is not the current instantiation
  ::A<T>* p4;                   // ::A<T> is the current instantiation
  class B {
    B* p1;                      // B is the current instantiation
    A<T>::B* p2;                // A<T>::B is the current instantiation
    typename A<T*>::B* p3;      // A<T*>::B is not the
                                // current instantiation
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
  B<my_T1, T2, my_I>* b3;       // refers to the current instantiation
  B<my_T1, T2, my_I2>* b4;      // not the current instantiation
  B<my_T1, T2, my_I3>* b5;      // refers to the current instantiation
};
```

A name is a *member of the current instantiation* if it is

- An unqualified name that, when looked up, refers to at least one
  member of a class that is the current instantiation or a non-dependent
  base class thereof. This can only occur when looking up a name in a
  scope enclosed by the definition of a class template.
- A *qualified-id* in which the *nested-name-specifier* refers to the
  current instantiation and that, when looked up, refers to at least one
  member of a class that is the current instantiation or a non-dependent
  base class thereof. if no such member is found, and the current
  instantiation has any dependent base classes, then the *qualified-id*
  is a member of an unknown specialization; see below.
- An *id-expression* denoting the member in a class member access
  expression ([[expr.ref]]) for which the type of the object expression
  is the current instantiation, and the *id-expression*, when looked
  up ([[basic.lookup.classref]]), refers to at least one member of a
  class that is the current instantiation or a non-dependent base class
  thereof. if no such member is found, and the current instantiation has
  any dependent base classes, then the *id-expression* is a member of an
  unknown specialization; see below.

``` cpp
template <class T> class A {
  static const int i = 5;
  int n1[i];        // i refers to a member of the current instantiation
  int n2[A::i];     // A::i refers to a member of the current instantiation
  int n3[A<T>::i];  // A<T>::i refers to a member of the current instantiation
  int f();
};

template <class T> int A<T>::f() {
  return i;         // i refers to a member of the current instantiation
}
```

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
  expression ([[expr.ref]]) in which either
  - the type of the object expression is the current instantiation, the
    current instantiation has at least one dependent base class, and
    name lookup of the *id-expression* does not find a member of a class
    that is the current instantiation or a non-dependent base class
    thereof; or
  - the type of the object expression is dependent and is not the
    current instantiation.

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

``` cpp
template<class T> class A {
  typedef int type;
  void f() {
    A<T>::type i;           // OK: refers to a member of the current instantiation
    typename A<T>::other j; // error: neither a member of the current instantiation nor
                            // a member of an unknown specialization
  }
};
```

If, for a given set of template arguments, a specialization of a
template is instantiated that refers to a member of the current
instantiation with a *qualified-id* or class member access expression,
the name in the *qualified-id* or class member access expression is
looked up in the template instantiation context. If the result of this
lookup differs from the result of name lookup in the template definition
context, name lookup is ambiguous. the result of name lookup differs
only when the member of the current instantiation was found in a
non-dependent base class of the current instantiation and a member with
the same name is also introduced by the substitution for a dependent
base class of the current instantiation.

A type is dependent if it is

- a template parameter,
- a member of an unknown specialization,
- a nested class or enumeration that is a dependent member of the
  current instantiation,
- a cv-qualified type where the cv-unqualified type is dependent,
- a compound type constructed from any dependent type,
- an array type constructed from any dependent type or whose size is
  specified by a constant expression that is value-dependent,
- a *simple-template-id* in which either the template name is a template
  parameter or any of the template arguments is a dependent type or an
  expression that is type-dependent or value-dependent, or
- denoted by `decltype(`*expression*`)`, where *expression* is
  type-dependent ([[temp.dep.expr]]).

Because typedefs do not introduce new types, but instead simply refer to
other types, a name that refers to a typedef that is a member of the
current instantiation is dependent only if the type referred to is
dependent.

#### Type-dependent expressions <a id="temp.dep.expr">[[temp.dep.expr]]</a>

Except as described below, an expression is type-dependent if any
subexpression is type-dependent.

`this`

is type-dependent if the class type of the enclosing member function is
dependent ([[temp.dep.type]]).

An *id-expression* is type-dependent if it contains

- an *identifier* associated by name lookup with one or more
  declarations declared with a dependent type,
- an *identifier* associated by name lookup with one or more
  declarations of member functions of the current instantiation declared
  with a return type that contains a placeholder type (
  [[dcl.spec.auto]]),
- a *template-id* that is dependent,
- a *conversion-function-id* that specifies a dependent type, or
- a *nested-name-specifier* or a *qualified-id* that names a member of
  an unknown specialization;

or if it names a dependent member of the current instantiation that is a
static data member of type “array of unknown bound of `T`” for some
`T` ([[temp.static]]). Expressions of the following forms are
type-dependent only if the type specified by the *type-id*,
*simple-type-specifier* or *new-type-id* is dependent, even if any
subexpression is type-dependent:

Expressions of the following forms are never type-dependent (because the
type of the expression cannot be dependent):

For the standard library macro `offsetof`, see  [[support.types]].

A class member access expression ([[expr.ref]]) is type-dependent if
the expression refers to a member of the current instantiation and the
type of the referenced member is dependent, or the class member access
expression refers to a member of an unknown specialization. In an
expression of the form `x.y` or `xp->y` the type of the expression is
usually the type of the member `y` of the class of `x` (or the class
pointed to by `xp`). However, if `x` or `xp` refers to a dependent type
that is not the current instantiation, the type of `y` is always
dependent. If `x` or `xp` refers to a non-dependent type or refers to
the current instantiation, the type of `y` is the type of the class
member access expression.

#### Value-dependent expressions <a id="temp.dep.constexpr">[[temp.dep.constexpr]]</a>

Except as described below, a constant expression is value-dependent if
any subexpression is value-dependent.

An *id-expression* is value-dependent if:

- it is a name declared with a dependent type,
- it is the name of a non-type template parameter,
- it names a member of an unknown specialization,
- it names a static data member that is a dependent member of the
  current instantiation and is not initialized in a *member-declarator*,
- it names a static member function that is a dependent member of the
  current instantiation, or
- it is a constant with literal type and is initialized with an
  expression that is value-dependent.

Expressions of the following form are value-dependent if the
*unary-expression* or *expression* is type-dependent or the *type-id* is
dependent:

For the standard library macro `offsetof`, see  [[support.types]].

Expressions of the following form are value-dependent if either the
*type-id* or *simple-type-specifier* is dependent or the *expression* or
*cast-expression* is value-dependent:

Expressions of the following form are value-dependent:

An expression of the form `&`*qualified-id* where the *qualified-id*
names a dependent member of the current instantiation is
value-dependent.

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

``` cpp
void g(double);
void h();

template<class T> class Z {
public:
  void f() {
    g(1);           // calls g(double)
    h++;            // ill-formed: cannot increment function;
                    // this could be diagnosed either here or
                    // at the point of instantiation
  }
};

void g(int);        // not in scope at the point of the template
                    // definition, not considered for the call g(1)
```

### Dependent name resolution <a id="temp.dep.res">[[temp.dep.res]]</a>

In resolving dependent names, names from the following sources are
considered:

- Declarations that are visible at the point of definition of the
  template.
- Declarations from namespaces associated with the types of the function
  arguments both from the instantiation context ([[temp.point]]) and
  from the definition context.

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

For an *exception-specification* of a function template specialization
or specialization of a member function of a class template, if the
*exception-specification* is implicitly instantiated because it is
needed by another template specialization and the context that requires
it depends on a template parameter, the point of instantiation of the
*exception-specification* is the point of instantiation of the
specialization that requires it. Otherwise, the point of instantiation
for such an *exception-specification* immediately follows the namespace
scope declaration or definition that requires the
*exception-specification*.

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

The instantiation context of an expression that depends on the template
arguments is the set of declarations with external linkage declared
prior to the point of instantiation of the template specialization in
the same translation unit.

A specialization for a function template, a member function template, or
of a member function or static data member of a class template may have
multiple points of instantiations within a translation unit, and in
addition to the points of instantiation described above, for any such
specialization that has a point of instantiation within the translation
unit, the end of the translation unit is also considered a point of
instantiation. A specialization for a class template has at most one
point of instantiation within a translation unit. A specialization for
any template may have points of instantiation in multiple translation
units. If two different points of instantiation give a template
specialization different meanings according to the one definition rule (
[[basic.def.odr]]), the program is ill-formed, no diagnostic required.

#### Candidate functions <a id="temp.dep.candidate">[[temp.dep.candidate]]</a>

For a function call where the *postfix-expression* is a dependent name,
the candidate functions are found using the usual lookup rules (
[[basic.lookup.unqual]], [[basic.lookup.argdep]]) except that:

- For the part of the lookup using unqualified name lookup (
  [[basic.lookup.unqual]]), only function declarations from the template
  definition context are found.
- For the part of the lookup using associated namespaces (
  [[basic.lookup.argdep]]), only function declarations found in either
  the template definition context or the template instantiation context
  are found.

If the call would be ill-formed or would find a better match had the
lookup within the associated namespaces considered all the function
declarations with external linkage introduced in those namespaces in all
translation units, not just considering those declarations found in the
template definition and template instantiation contexts, then the
program has undefined behavior.

### Friend names declared within a class template <a id="temp.inject">[[temp.inject]]</a>

Friend classes or functions can be declared within a class template.
When a template is instantiated, the names of its friends are treated as
if the specialization had been explicitly declared at its point of
instantiation.

As with non-template classes, the names of namespace-scope friend
functions of a class template specialization are not visible during an
ordinary lookup unless explicitly declared at namespace scope (
[[class.friend]]). Such names may be found under the rules for
associated classes ([[basic.lookup.argdep]]).[^6]

``` cpp
template<typename T> struct number {
  number(int);
  friend number gcd(number x, number y) { return 0; };
};

void g() {
  number<double> a(3), b(4);
  a = gcd(a,b);     // finds gcd because number<double> is an
                    // associated class, making gcd visible
                    // in its namespace (global scope)
  b = gcd(3,4);     // ill-formed; gcd is not visible
}
```

## Template instantiation and specialization <a id="temp.spec">[[temp.spec]]</a>

The act of instantiating a function, a class, a member of a class
template or a member template is referred to as *template
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
instantiated member class.

An explicit specialization may be declared for a function template, a
class template, a member of a class template or a member template. An
explicit specialization declaration is introduced by `template<>`. In an
explicit specialization declaration for a class template, a member of a
class template or a class member template, the name of the class that is
explicitly specialized shall be a *simple-template-id*. In the explicit
specialization declaration for a function template or a member function
template, the name of the function or member function explicitly
specialized may be a *template-id*.

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

An instantiated template specialization can be either implicitly
instantiated ([[temp.inst]]) for a given argument list or be explicitly
instantiated ([[temp.explicit]]). A specialization is a class,
function, or class member that is either instantiated or explicitly
specialized ([[temp.expl.spec]]).

For a given template and a given set of *template-argument*s,

- an explicit instantiation definition shall appear at most once in a
  program,
- an explicit specialization shall be defined at most once in a program
  (according to  [[basic.def.odr]]), and
- both an explicit instantiation and a declaration of an explicit
  specialization shall not appear in a program unless the explicit
  instantiation follows a declaration of the explicit specialization.

An implementation is not required to diagnose a violation of this rule.

Each class template specialization instantiated from a template has its
own copy of any static members.

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

### Implicit instantiation <a id="temp.inst">[[temp.inst]]</a>

Unless a class template specialization has been explicitly
instantiated ([[temp.explicit]]) or explicitly specialized (
[[temp.expl.spec]]), the class template specialization is implicitly
instantiated when the specialization is referenced in a context that
requires a completely-defined object type or when the completeness of
the class type affects the semantics of the program. The implicit
instantiation of a class template specialization causes the implicit
instantiation of the declarations, but not of the definitions, default
arguments, or *exception-specification*s of the class member functions,
member classes, scoped member enumerations, static data members and
member templates; and it causes the implicit instantiation of the
definitions of unscoped member enumerations and member anonymous unions.
However, for the purpose of determining whether an instantiated
redeclaration of a member is valid according to  [[class.mem]], a
declaration that corresponds to a definition in the template is
considered to be a definition.

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

Unless a member of a class template or a member template has been
explicitly instantiated or explicitly specialized, the specialization of
the member is implicitly instantiated when the specialization is
referenced in a context that requires the member definition to exist; in
particular, the initialization (and any associated side-effects) of a
static data member does not occur unless the static data member is
itself used in a way that requires the definition of the static data
member to exist.

Unless a function template specialization has been explicitly
instantiated or explicitly specialized, the function template
specialization is implicitly instantiated when the specialization is
referenced in a context that requires a function definition to exist.
Unless a call is to a function template explicit specialization or to a
member function of an explicitly specialized class template, a default
argument for a function template or a member function of a class
template is implicitly instantiated when the function is called in a
context that requires the value of the default argument.

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

Unless a variable template specialization has been explicitly
instantiated or explicitly specialized, the variable template
specialization is implicitly instantiated when the specialization is
used. A default template argument for a variable template is implicitly
instantiated when the variable template is referenced in a context that
requires the value of the default argument.

A class template specialization is implicitly instantiated if the class
type is used in a context that requires a completely-defined object type
or if the completeness of the class type might affect the semantics of
the program. In particular, if the semantics of an expression depend on
the member or base class lists of a class template specialization, the
class template specialization is implicitly generated. For instance,
deleting a pointer to class type depends on whether or not the class
declares a destructor, and conversion between pointer to class types
depends on the inheritance relationship between the two classes
involved.

``` cpp
template<class T> class B { /* ... */ };
template<class T> class D : public B<T> { /* ... */ };

void f(void*);
void f(B<int>*);

void g(D<int>* p, D<char>* pp, D<double>* ppp) {
  f(p);             // instantiation of D<int> required: call f(B<int>*)
  B<char>* q = pp;  // instantiation of D<char> required:
                    // convert D<char>* to B<char>*
  delete ppp;       // instantiation of D<double> required
}
```

If the overload resolution process can determine the correct function to
call without instantiating a class template definition, it is
unspecified whether that instantiation actually takes place.

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

If an implicit instantiation of a class template specialization is
required and the template is declared but not defined, the program is
ill-formed.

``` cpp
template<class T> class X;

X<char> ch;         // error: definition of X required
```

The implicit instantiation of a class template does not cause any static
data members of that class to be implicitly instantiated.

If a function template or a member function template specialization is
used in a way that involves overload resolution, a declaration of the
specialization is implicitly instantiated ([[temp.over]]).

An implementation shall not implicitly instantiate a function template,
a variable template, a member template, a non-virtual member function, a
member class, or a static data member of a class template that does not
require instantiation. It is unspecified whether or not an
implementation implicitly instantiates a virtual member function of a
class template if the virtual member function would not otherwise be
instantiated. The use of a template specialization in a default argument
shall not cause the template to be implicitly instantiated except that a
class template may be instantiated where its complete type is needed to
determine the correctness of the default argument. The use of a default
argument in a function call causes specializations in the default
argument to be implicitly instantiated.

Implicitly instantiated class, function, and variable template
specializations are placed in the namespace where the template is
defined. Implicitly instantiated specializations for members of a class
template are placed in the namespace where the enclosing class template
is defined. Implicitly instantiated member templates are placed in the
namespace where the enclosing class or class template is defined.

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

a call of `lt.get()` from `Map<const char*,int>::get()` would place
`List<int>::get()` in the namespace `N` rather than in the global
namespace.

If a function template `f` is called in a way that requires a default
argument to be used, the dependent names are looked up, the semantics
constraints are checked, and the instantiation of any template used in
the default argument is done as if the default argument had been an
initializer used in a function template specialization with the same
scope, the same template parameters and the same access as that of the
function template `f` used at that point, except that the scope in which
a closure type is declared ([[expr.prim.lambda]]) – and therefore its
associated namespaces – remain as determined from the context of the
definition for the default argument. This analysis is called *default
argument instantiation*. The instantiated default argument is then used
as the argument of `f`.

Each default argument is instantiated independently.

``` cpp
template<class T> void f(T x, T y = ydef(T()), T z = zdef(T()));

class  A { };

A zdef(A);

void g(A a, A b, A c) {
  f(a, b, c);       // no default argument instantiation
  f(a, b);          // default argument z = zdef(T()) instantiated
  f(a);             // ill-formed; ydef is not declared
}
```

The *exception-specification* of a function template specialization is
not instantiated along with the function declaration; it is instantiated
when needed ([[except.spec]]). If such an *exception-specification* is
needed but has not yet been instantiated, the dependent names are looked
up, the semantics constraints are checked, and the instantiation of any
template used in the *exception-specification* is done as if it were
being done as part of instantiating the declaration of the
specialization at that point.

[[temp.point]] defines the point of instantiation of a template
specialization.

There is an implementation-defined quantity that specifies the limit on
the total depth of recursive instantiations, which could involve more
than one template. The result of an infinite recursion in instantiation
is undefined.

``` cpp
template<class T> class X {
  X<T>* p;          // OK
  X<T*> a;          // implicit generation of X<T> requires
                    // the implicit instantiation of X<T*> which requires
                    // the implicit instantiation of X<T**> which ...
};
```

### Explicit instantiation <a id="temp.explicit">[[temp.explicit]]</a>

A class, function, variable, or member template specialization can be
explicitly instantiated from its template. A member function, member
class or static data member of a class template can be explicitly
instantiated from the member definition associated with its class
template. An explicit instantiation of a function template or member
function of a class template shall not use the `inline` or `constexpr`
specifiers.

The syntax for explicit instantiation is:

``` bnf
explicit-instantiation:
  'extern'ₒₚₜ 'template' declaration
```

There are two forms of explicit instantiation: an explicit instantiation
definition and an explicit instantiation declaration. An explicit
instantiation declaration begins with the `extern` keyword.

If the explicit instantiation is for a class or member class, the
*elaborated-type-specifier* in the *declaration* shall include a
*simple-template-id*. If the explicit instantiation is for a function or
member function, the *unqualified-id* in the *declaration* shall be
either a *template-id* or, where all template arguments can be deduced,
a *template-name* or *operator-function-id*. The declaration may declare
a *qualified-id*, in which case the *unqualified-id* of the
*qualified-id* must be a *template-id*. If the explicit instantiation is
for a member function, a member class or a static data member of a class
template specialization, the name of the class template specialization
in the *qualified-id* for the member name shall be a
*simple-template-id*. If the explicit instantiation is for a variable,
the *unqualified-id* in the declaration shall be a *template-id*. An
explicit instantiation shall appear in an enclosing namespace of its
template. If the name declared in the explicit instantiation is an
unqualified name, the explicit instantiation shall appear in the
namespace where its template is declared or, if that namespace is
inline ([[namespace.def]]), any namespace from its enclosing namespace
set. Regarding qualified names in declarators, see  [[dcl.meaning]].

``` cpp
template<class T> class Array { void mf(); };
template class Array<char>;
template void Array<int>::mf();

template<class T> void sort(Array<T>& v) { /* ... */ }
template void sort(Array<char>&);       // argument is deduced here

namespace N {
  template<class T> void f(T&) { }
}
template void N::f<int>(int&);
```

A declaration of a function template, a variable template, a member
function or static data member of a class template, or a member function
template of a class or class template shall precede an explicit
instantiation of that entity. A definition of a class template, a member
class of a class template, or a member class template of a class or
class template shall precede an explicit instantiation of that entity
unless the explicit instantiation is preceded by an explicit
specialization of the entity with the same template arguments. If the
*declaration* of the explicit instantiation names an implicitly-declared
special member function (Clause  [[special]]), the program is
ill-formed.

For a given set of template arguments, if an explicit instantiation of a
template appears after a declaration of an explicit specialization for
that template, the explicit instantiation has no effect. Otherwise, for
an explicit instantiation definition the definition of a function
template, a variable template, a member function template, or a member
function or static data member of a class template shall be present in
every translation unit in which it is explicitly instantiated.

An explicit instantiation of a class, function template, or variable
template specialization is placed in the namespace in which the template
is defined. An explicit instantiation for a member of a class template
is placed in the namespace where the enclosing class template is
defined. An explicit instantiation for a member template is placed in
the namespace where the enclosing class or class template is defined.

``` cpp
namespace N {
  template<class T> class Y { void mf() { } };
}

template class Y<int>;                  // error: class template Y not visible
                                        // in the global namespace

using N::Y;
template class Y<int>;                  // error: explicit instantiation outside of the
                                        // namespace of the template

template class N::Y<char*>;             // OK: explicit instantiation in namespace N
template void N::Y<double>::mf();       // OK: explicit instantiation
                                        // in namespace N
```

A trailing *template-argument* can be left unspecified in an explicit
instantiation of a function template specialization or of a member
function template specialization provided it can be deduced from the
type of a function parameter ([[temp.deduct]]).

``` cpp
template<class T> class Array { /* ... */ };
template<class T> void sort(Array<T>& v) { /* ... */ }

// instantiate sort(Array<int>&) - template-argument deduced
template void sort<>(Array<int>&);
```

An explicit instantiation that names a class template specialization is
also an explicit instantiation of the same kind (declaration or
definition) of each of its members (not including members inherited from
base classes and members that are templates) that has not been
previously explicitly specialized in the translation unit containing the
explicit instantiation, except as described below. In addition, it will
typically be an explicit instantiation of certain
implementation-dependent data about the class.

An explicit instantiation definition that names a class template
specialization explicitly instantiates the class template specialization
and is an explicit instantiation definition of only those members that
have been defined at the point of instantiation.

Except for inline functions, declarations with types deduced from their
initializer or return value ([[dcl.spec.auto]]), `const` variables of
literal types, variables of reference types, and class template
specializations, explicit instantiation declarations have the effect of
suppressing the implicit instantiation of the entity to which they
refer. The intent is that an inline function that is the subject of an
explicit instantiation declaration will still be implicitly instantiated
when odr-used ([[basic.def.odr]]) so that the body can be considered
for inlining, but that no out-of-line copy of the inline function would
be generated in the translation unit.

If an entity is the subject of both an explicit instantiation
declaration and an explicit instantiation definition in the same
translation unit, the definition shall follow the declaration. An entity
that is the subject of an explicit instantiation declaration and that is
also used in a way that would otherwise cause an implicit
instantiation ([[temp.inst]]) in the translation unit shall be the
subject of an explicit instantiation definition somewhere in the
program; otherwise the program is ill-formed, no diagnostic required.
This rule does apply to inline functions even though an explicit
instantiation declaration of such an entity has no other normative
effect. This is needed to ensure that if the address of an inline
function is taken in a translation unit in which the implementation
chose to suppress the out-of-line body, another translation unit will
supply the body. An explicit instantiation declaration shall not name a
specialization of a template with internal linkage.

The usual access checking rules do not apply to names used to specify
explicit instantiations. In particular, the template arguments and names
used in the function declarator (including parameter types, return types
and exception specifications) may be private types or objects which
would normally not be accessible and the template may be a member
template or member function which would not normally be accessible.

An explicit instantiation does not constitute a use of a default
argument, so default argument instantiation is not done.

``` cpp
char* p = 0;
template<class T> T g(T x = &p) { return x; }
template int g<int>(int);       // OK even though &p isn't an int.
```

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
  'template < >' declaration
```

``` cpp
template<class T> class stream;

template<> class stream<char> { /* ... */ };

template<class T> class Array { /* ... */ };
template<class T> void sort(Array<T>& v) { /* ... */ }

template<> void sort<char*>(Array<char*>&) ;
```

Given these declarations, `stream<char>` will be used as the definition
of streams of `char`s; other streams will be handled by class template
specializations instantiated from the class template. Similarly,
`sort<char*>` will be used as the sort function for arguments of type
`Array<char*>`; other `Array` types will be sorted by functions
generated from the template.

An explicit specialization shall be declared in a namespace enclosing
the specialized template. An explicit specialization whose
*declarator-id* is not qualified shall be declared in the nearest
enclosing namespace of the template, or, if the namespace is inline (
[[namespace.def]]), any namespace from its enclosing namespace set. Such
a declaration may also be a definition. If the declaration is not a
definition, the specialization may be defined later (
[[namespace.memdef]]).

A declaration of a function template, class template, or variable
template being explicitly specialized shall precede the declaration of
the explicit specialization. A declaration, but not a definition of the
template is required. The definition of a class or class template shall
precede the declaration of an explicit specialization for a member
template of the class or class template.

``` cpp
template<> class X<int> { /* ... */ };          // error: X not a template

template<class T> class X;

template<> class X<char*> { /* ... */ };        // OK: X is a template
```

A member function, a member function template, a member class, a member
enumeration, a member class template, a static data member, or a static
data member template of a class template may be explicitly specialized
for a class specialization that is implicitly instantiated; in this
case, the definition of the class template shall precede the explicit
specialization for the member of the class template. If such an explicit
specialization for the member of a class template names an
implicitly-declared special member function (Clause  [[special]]), the
program is ill-formed.

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

// template<> not used for a member of an
// explicitly specialized class template
void A<int>::f(int) { /* ... */ }

template<> struct A<char>::B {
  void f();
};
// template<> also not used when defining a member of
// an explicitly specialized member class
void A<char>::B::f() { /* ... */ }

template<> template<class U> struct A<char>::C {
  void f();
};
// template<> is used when defining a member of an explicitly
// specialized member class template specialized as a class template
template<>
template<class U> void A<char>::C<U>::f() { /* ... */ }

template<> struct A<short>::B {
  void f();
};
template<> void A<short>::B::f() { /* ... */ }  // error: template<> not permitted

template<> template<class U> struct A<short>::C {
  void f();
};
template<class U> void A<short>::C<U>::f() { /* ... */ }  // error: template<> required
```

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

``` cpp
class String { };
template<class T> class Array { /* ... */ };
template<class T> void sort(Array<T>& v) { /* ... */ }

void f(Array<String>& v) {
  sort(v);          // use primary template
                    // sort(Array<T>&), T is String
}

template<> void sort<String>(Array<String>& v); // error: specialization
                                                // after use of primary template
template<> void sort<>(Array<char*>& v);        // OK: sort<char*> not yet used
template<class T> struct A {
  enum E : T;
  enum class S : T;
};
template<> enum A<int>::E : int { eint };         // OK
template<> enum class A<int>::S : int { sint };   // OK
template<class T> enum A<T>::E : T { eT };
template<class T> enum class A<T>::S : T { sT };
template<> enum A<char>::E : char { echar };       // ill-formed, A<char>::E was instantiated
                                                   // when A<char> was instantiated
template<> enum class A<char>::S : char { schar }; // OK
```

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

``` cpp
namespace N {
  template<class T> class X { /* ... */ };
  template<class T> class Y { /* ... */ };

  template<> class X<int> { /* ... */ };          // OK: specialization
                                                // in same namespace
  template<> class Y<double>;                   // forward declare intent to
                                                // specialize for double
}

template<> class N::Y<double> { /* ... */ };      // OK: specialization
                                                // in enclosing namespace
template<> class N::Y<short> { /* ... */ };       // OK: specialization
                                                // in enclosing namespace
```

A *simple-template-id* that names a class template explicit
specialization that has been declared but not defined can be used
exactly like the names of other incompletely-defined classes (
[[basic.types]]).

``` cpp
template<class T> class X;      // X is a class template
template<> class X<int>;

X<int>* p;                      // OK: pointer to declared class X<int>
X<int> x;                       // error: object of incomplete class X<int>
```

A trailing *template-argument* can be left unspecified in the
*template-id* naming an explicit function template specialization
provided it can be deduced from the function argument type.

``` cpp
template<class T> class Array { /* ... */ };
template<class T> void sort(Array<T>& v);

// explicit specialization for sort(Array<int>&)
// with deduced template-argument of type int
template<> void sort(Array<int>&);
```

A function with the same name as a template and a type that exactly
matches that of a template specialization is not an explicit
specialization ([[temp.fct]]).

An explicit specialization of a function template is inline only if it
is declared with the `inline` specifier or defined as deleted, and
independently of whether its function template is inline.

``` cpp
template<class T> void f(T) { /* ... */ }
template<class T> inline T g(T) { /* ... */ }

template<> inline void f<>(int) { /* ... */ }   // OK: inline
template<> int g<>(int) { /* ... */ }           // OK: not inline
```

An explicit specialization of a static data member of a template or an
explicit specialization of a static data member template is a definition
if the declaration includes an initializer; otherwise, it is a
declaration. The definition of a static data member of a template that
requires default initialization must use a *braced-init-list*:

``` cpp
template<> X Q<int>::x;         // declaration
template<> X Q<int>::x ();      // error: declares a function
template<> X Q<int>::x { };     // definition
```

A member or a member template of a class template may be explicitly
specialized for a given implicit instantiation of the class template,
even if the member or member template is defined in the class template
definition. An explicit specialization of a member or member template is
specified using the syntax for explicit specialization.

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

//member template specialization
template<> template<>
  void A<int>::g1(int, char);           // X1 deduced as char
template<> template<>
  void A<int>::g2<char>(int, char);     // X2 specified as char

// member specialization even if defined in class definition
template<> void A<int>::h(int) { }
```

A member or a member template may be nested within many enclosing class
templates. In an explicit specialization for such a member, the member
declaration shall be preceded by a `template<>` for each enclosing class
template that is explicitly specialized.

``` cpp
template<class T1> class A {
  template<class T2> class B {
    void mf();
  };
};
template<> template<> class A<int>::B<double>;
template<> template<> void A<char>::B<char>::mf();
```

In an explicit specialization declaration for a member of a class
template or a member template that appears in namespace scope, the
member template and some of its enclosing class templates may remain
unspecialized, except that the declaration shall not explicitly
specialize a class member template if its enclosing class templates are
not explicitly specialized as well. In such explicit specialization
declaration, the keyword `template` followed by a
*template-parameter-list* shall be provided instead of the `template<>`
preceding the explicit specialization declaration of the member. The
types of the *template-parameters* in the *template-parameter-list*
shall be the same as those specified in the primary template definition.

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
  void A<Y>::B<double>::mf2() { }       // ill-formed; B<double> is specialized but
                                        // its enclosing class template A is not
```

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
  specialization belongs is implicitly instantiated. Default function
  arguments may be specified in the declaration or definition of a
  member function of a class template specialization that is explicitly
  specialized.

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

### Explicit template argument specification <a id="temp.arg.explicit">[[temp.arg.explicit]]</a>

Template arguments can be specified when referring to a function
template specialization by qualifying the function template name with
the list of *template-argument*s in the same way as *template-argument*s
are specified in uses of a class template specialization.

``` cpp
template<class T> void sort(Array<T>& v);
void f(Array<dcomplex>& cv, Array<int>& ci) {
  sort<dcomplex>(cv);           // sort(Array<dcomplex>&)
  sort<int>(ci);                // sort(Array<int>&)
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

A template argument list may be specified when referring to a
specialization of a function template

- when a function is called,
- when the address of a function is taken, when a function initializes a
  reference to function, or when a pointer to member function is formed,
- in an explicit specialization,
- in an explicit instantiation, or
- in a friend declaration.

Trailing template arguments that can be deduced ([[temp.deduct]]) or
obtained from default *template-argument*s may be omitted from the list
of explicit *template-argument*s. A trailing template parameter pack (
[[temp.variadic]]) not otherwise deduced will be deduced to an empty
sequence of template arguments. If all of the template arguments can be
deduced, they may all be omitted; in this case, the empty template
argument list `<>` itself may also be omitted. In contexts where
deduction is done and fails, or in contexts where deduction is not done,
if a template argument list is specified and it, along with any default
template arguments, identifies a single function template
specialization, then the *template-id* is an lvalue for the function
template specialization.

``` cpp
template<class X, class Y> X f(Y);
template<class X, class Y, class ... Z> X g(Y);
void h() {
  int i = f<int>(5.6);          // Y is deduced to be double
  int j = f(5.6);               // ill-formed: X cannot be deduced
  f<void>(f<int, bool>);        // Y for outer f deduced to be
                                // int (*)(bool)
  f<void>(f<int>);              // ill-formed: f<int> does not denote a
                                // single function template specialization
  int k = g<int>(5.6);          // Y is deduced to be double, Z is deduced to an empty sequence
  f<void>(g<int, bool>);        // Y for outer f is deduced to be
                                // int (*)(bool), Z is deduced to an empty sequence
}
```

An empty template argument list can be used to indicate that a given use
refers to a specialization of a function template even when a
non-template function ([[dcl.fct]]) is visible that would otherwise be
used. For example:

``` cpp
template <class T> int f(T);    // #1
int f(int);                     // #2
int k = f(1);                   // uses #2
int l = f<>(1);                 // uses #1
```

Template arguments that are present shall be specified in the
declaration order of their corresponding *template-parameter*s. The
template argument list shall not specify more *template-argument*s than
there are corresponding *template-parameter*s unless one of the
*template-parameter*s is a template parameter pack.

``` cpp
template<class X, class Y, class Z> X f(Y,Z);
template<class ... Args> void f2();
void g() {
  f<int,const char*,double>("aa",3.0);
  f<int,const char*>("aa",3.0);       // Z is deduced to be double
  f<int>("aa",3.0);             // Y is deduced to be const char*, and
                                // Z is deduced to be double
  f("aa",3.0);                  // error: X cannot be deduced
  f2<char, short, int, long>(); // OK
}
```

Implicit conversions (Clause  [[conv]]) will be performed on a function
argument to convert it to the type of the corresponding function
parameter if the parameter type contains no *template-parameter*s that
participate in template argument deduction. Template parameters do not
participate in template argument deduction if they are explicitly
specified. For example,

``` cpp
template<class T> void f(T);

class Complex {
  Complex(double);
};

void g() {
  f<Complex>(1);                // OK, means f<Complex>(Complex(1))
}
```

Because the explicit template argument list follows the function
template name, and because conversion member function templates and
constructor member function templates are called without using a
function name, there is no way to provide an explicit template argument
list for these function templates.

For simple function names, argument dependent lookup (
[[basic.lookup.argdep]]) applies even when the function name is not
visible within the scope of the call. This is because the call still has
the syntactic form of a function call ([[basic.lookup.unqual]]). But
when a function template with explicit template arguments is used, the
call does not have the correct syntactic form unless there is a function
template with that name visible at the point of the call. If no such
name is visible, the call is not syntactically well-formed and
argument-dependent lookup does not apply. If some such name is visible,
argument dependent lookup applies and additional function templates may
be found in other namespaces.

``` cpp
namespace A {
  struct B { };
  template<int X> void f(B);
}
namespace C {
  template<class T> void f(T t);
}
void g(A::B b) {
  f<3>(b);                      // ill-formed: not a function call
  A::f<3>(b);                   // well-formed
  C::f<3>(b);                   // ill-formed; argument dependent lookup
                                // applies only to unqualified names
  using C::f;
  f<3>(b);                      // well-formed because C::f is visible; then
                                // A::f is found by argument dependent lookup
}
```

Template argument deduction can extend the sequence of template
arguments corresponding to a template parameter pack, even when the
sequence contains explicitly specified template arguments.

``` cpp
template<class ... Types> void f(Types ... values);

void g() {
  f<int*, float*>(0, 0, 0);     // Types is deduced to the sequence int*, float*, int
}
```

### Template argument deduction <a id="temp.deduct">[[temp.deduct]]</a>

When a function template specialization is referenced, all of the
template arguments shall have values. The values can be explicitly
specified or, in some cases, be deduced from the use or obtained from
default *template-argument*s.

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

When an explicit template argument list is specified, the template
arguments must be compatible with the template parameter list and must
result in a valid function type as described below; otherwise type
deduction fails. Specifically, the following steps are performed when
evaluating an explicitly specified template argument list with respect
to a given function template:

- The specified template arguments must match the template parameters in
  kind (i.e., type, non-type, template). There must not be more
  arguments than there are parameters unless at least one parameter is a
  template parameter pack, and there shall be an argument for each
  non-pack parameter. Otherwise, type deduction fails.
- Non-type arguments must match the types of the corresponding non-type
  template parameters, or must be convertible to the types of the
  corresponding non-type parameters as specified in 
  [[temp.arg.nontype]], otherwise type deduction fails.
- The specified template argument values are substituted for the
  corresponding template parameters as specified below.

After this substitution is performed, the function parameter type
adjustments described in  [[dcl.fct]] are performed. A parameter type of
“`void ()(const int, int[5])`” becomes “`void(*)(int,int*)`”. A
top-level qualifier in a function parameter declaration does not affect
the function type but still affects the type of the function parameter
variable within the function.

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

`f<int>(1)` and `f<const int>(1)` call distinct functions even though
both of the functions called have the same function type.

The resulting substituted and adjusted function type is used as the type
of the function template for template argument deduction. If a template
argument has not been deduced and its corresponding template parameter
has a default argument, the template argument is determined by
substituting the template arguments determined for preceding template
parameters into the default argument. If the substitution results in an
invalid type, as described above, type deduction fails.

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

When all template arguments have been deduced or obtained from default
template arguments, all uses of template parameters in the template
parameter list of the template and the function type are replaced with
the corresponding deduced or default argument values. If the
substitution results in an invalid type, as described above, type
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
causes deduction to fail is encountered. The equivalent substitution in
exception specifications is done only when the *exception-specification*
is instantiated, at which point a program is ill-formed if the
substitution results in an invalid type or expression.

``` cpp
template <class T> struct A { using X = typename T::X; };
template <class T> typename T::X f(typename A<T>::X);
template <class T> void f(...) { }
template <class T> auto g(typename A<T>::X) -> typename T::X;
template <class T> void g(...) { }

void h() {
  f<int>(0); // OK, substituting return type causes deduction to fail
  g<int>(0); // error, substituting parameter type instantiates A<int>
}
```

If a substitution results in an invalid type or expression, type
deduction fails. An invalid type or expression is one that would be
ill-formed, with a diagnostic required, if written using the substituted
arguments. If no diagnostic is required, the program is still
ill-formed. Access checking is done as part of the substitution process.
Only invalid types and expressions in the immediate context of the
function type and its template parameter types can result in a deduction
failure. The evaluation of the substituted types and expressions can
result in side effects such as the instantiation of class template
specializations and/or function template specializations, the generation
of implicitly-defined functions, etc. Such side effects are not in the
“immediate context” and can result in the program being ill-formed.

``` cpp
struct X { };
struct Y {
  Y(X){}
};

template <class T> auto f(T t1, T t2) -> decltype(t1 + t2); // #1
X f(Y, Y);  // #2

X x1, x2;
X x3 = f(x1, x2);  // deduction fails on #1 (cannot add X+X), calls #2
```

Type deduction may fail for the following reasons:

- Attempting to instantiate a pack expansion containing multiple
  parameter packs of differing lengths.
- Attempting to create an array with an element type that is `void`, a
  function type, a reference type, or an abstract class type, or
  attempting to create an array with a size that is zero or negative.
  ``` cpp
  template <class T> int f(T[5]);
  int I = f<int>(0);
  int j = f<void>(0);             // invalid array
  ```
- Attempting to use a type that is not a class or enumeration type in a
  qualified name.
  ``` cpp
  template <class T> int f(typename T::B*);
  int i = f<int>(0);
  ```
- Attempting to use a type in a *nested-name-specifier* of a
  *qualified-id* when that type does not contain the specified member,
  or
  - the specified member is not a type where a type is required, or
  - the specified member is not a template where a template is required,
    or
  - the specified member is not a non-type where a non-type is required.

  ``` cpp
  template <int I> struct X { };
  template <template <class T> class> struct Z { };
  template <class T> void f(typename T::Y*){}
  template <class T> void g(X<T::N>*){}
  template <class T> void h(Z<T::template TT>*){}
  struct A {};
  struct B { int Y; };
  struct C {
    typedef int N;
  };
  struct D {
    typedef int TT;
  };

  int main() {
    // Deduction fails in each of these cases:
    f<A>(0);  // A does not contain a member Y
    f<B>(0);  // The Y member of B is not a type
    g<C>(0);  // The N member of C is not a non-type
    h<D>(0);  // The TT member of D is not a template
  }
  ```
- Attempting to create a pointer to reference type.
- Attempting to create a reference to `void`.
- Attempting to create “pointer to member of `T`” when `T` is not a
  class type.
  ``` cpp
  template <class T> int f(int T::*);
  int i = f<int>(0);
  ```
- Attempting to give an invalid type to a non-type template parameter.
  ``` cpp
  template <class T, T> struct S {};
  template <class T> int f(S<T, T()>*);
  struct X {};
  int i0 = f<X>(0);
  ```
- Attempting to perform an invalid conversion in either a template
  argument expression, or an expression used in the function
  declaration.
  ``` cpp
  template <class T, T*> int f(int);
  int i2 = f<int,1>(0);           // can't conv 1 to int*
  ```
- Attempting to create a function type in which a parameter has a type
  of `void`, or in which the return type is a function type or array
  type.
- Attempting to create a function type in which a parameter type or the
  return type is an abstract class type ([[class.abstract]]).

Except as described above, the use of an invalid value shall not cause
type deduction to fail. In the following example 1000 is converted to
`signed char` and results in an implementation-defined value as
specified in ([[conv.integral]]). In other words, both templates are
considered even though 1000, when converted to `signed char`, results in
an implementation-defined value.

``` cpp
template <int> int f(int);
template <signed char> int f(int);
int i1 = f<1>(0);               // ambiguous
int i2 = f<1000>(0);            // ambiguous
```

#### Deducing template arguments from a function call <a id="temp.deduct.call">[[temp.deduct.call]]</a>

Template argument deduction is done by comparing each function template
parameter type (call it `P`) with the type of the corresponding argument
of the call (call it `A`) as described below. If removing references and
cv-qualifiers from `P` gives `std::initializer_list<P^\prime>` for some
`P^\prime` and the argument is an initializer list ([[dcl.init.list]]),
then deduction is performed instead for each element of the initializer
list, taking `P^\prime` as a function template parameter type and the
initializer element as its argument. Otherwise, an initializer list
argument causes the parameter to be considered a non-deduced context (
[[temp.deduct.type]]).

``` cpp
template<class T> void f(std::initializer_list<T>);
f({1,2,3});                 // T deduced to int
f({1,"asdf"});              // error: T deduced to both int and const char*

template<class T> void g(T);
g({1,2,3});                 // error: no argument deduced for T
```

For a function parameter pack that occurs at the end of the
*parameter-declaration-list*, the type `A` of each remaining argument of
the call is compared with the type `P` of the *declarator-id* of the
function parameter pack. Each comparison deduces template arguments for
subsequent positions in the template parameter packs expanded by the
function parameter pack. When a function parameter pack appears in a
non-deduced context ([[temp.deduct.type]]), the type of that parameter
pack is never deduced.

``` cpp
template<class ... Types> void f(Types& ...);
template<class T1, class ... Types> void g(T1, Types ...);
template<class T1, class ... Types> void g1(Types ..., T1);

void h(int x, float& y) {
  const int z = x;
  f(x, y, z);                  // Types is deduced to int, float, const int
  g(x, y, z);                  // T1 is deduced to int; Types is deduced to float, int
  g1(x, y, z);                 // error: Types is not deduced
  g1<int, int, int>(x, y, z);  // OK, no deduction occurs

}
```

If `P` is not a reference type:

- If `A` is an array type, the pointer type produced by the
  array-to-pointer standard conversion ([[conv.array]]) is used in
  place of `A` for type deduction; otherwise,
- If `A` is a function type, the pointer type produced by the
  function-to-pointer standard conversion ([[conv.func]]) is used in
  place of `A` for type deduction; otherwise,
- If `A` is a cv-qualified type, the top level cv-qualifiers of `A`’s
  type are ignored for type deduction.

If `P` is a cv-qualified type, the top level cv-qualifiers of `P`’s type
are ignored for type deduction. If `P` is a reference type, the type
referred to by `P` is used for type deduction. If `P` is an rvalue
reference to a cv-unqualified template parameter and the argument is an
lvalue, the type “lvalue reference to `A`” is used in place of `A` for
type deduction.

``` cpp
template <class T> int f(T&&);
template <class T> int g(const T&&);
int i;
int n1 = f(i);                  // calls f<int&>(int&)
int n2 = f(0);                  // calls f<int>(int&&)
int n3 = g(i);                  // error: would call g<int>(const int&&), which
                                // would bind an rvalue reference to an lvalue
```

In general, the deduction process attempts to find template argument
values that will make the deduced `A` identical to `A` (after the type
`A` is transformed as described above). However, there are three cases
that allow a difference:

- If the original `P` is a reference type, the deduced `A` (i.e., the
  type referred to by the reference) can be more cv-qualified than the
  transformed `A`.
- The transformed `A` can be another pointer or pointer to member type
  that can be converted to the deduced `A` via a qualification
  conversion ([[conv.qual]]).
- If `P` is a class and `P` has the form *simple-template-id*, then the
  transformed `A` can be a derived class of the deduced `A`. Likewise,
  if `P` is a pointer to a class of the form *simple-template-id*, the
  transformed `A` can be a pointer to a derived class pointed to by the
  deduced `A`.

as specified in  [[temp.arg.explicit]], implicit conversions will be
performed on a function argument to convert it to the type of the
corresponding function parameter if the parameter contains no
*template-parameter*s that participate in template argument deduction.
Such conversions are also allowed, in addition to the ones described in
the preceding list.

These alternatives are considered only if type deduction would otherwise
fail. If they yield more than one possible deduced `A`, the type
deduction fails. If a *template-parameter* is not used in any of the
function parameters of a function template, or is used only in a
non-deduced context, its corresponding *template-argument* cannot be
deduced from a function call and the *template-argument* must be
explicitly specified.

When P is a function type, pointer to function type, or pointer to
member function type:

- If the argument is an overload set containing one or more function
  templates, the parameter is treated as a non-deduced context.
- If the argument is an overload set (not containing function
  templates), trial argument deduction is attempted using each of the
  members of the set. If deduction succeeds for only one of the overload
  set members, that member is used as the argument value for the
  deduction. If deduction succeeds for more than one member of the
  overload set the parameter is treated as a non-deduced context.
  ``` cpp
  // Only one function of an overload set matches the call so the function
  // parameter is a deduced context.
  template <class T> int f(T (*p)(T));
  int g(int);
  int g(char);
  int i = f(g);       // calls f(int (*)(int))
  ```

  ``` cpp
  // Ambiguous deduction causes the second function parameter to be a
  // non-deduced context.
  template <class T> int f(T, T (*p)(T));
  int g(int);
  char g(char);
  int i = f(1, g);    // calls f(int, int (*)(int))
  ```

  ``` cpp
  // The overload set contains a template, causing the second function
  // parameter to be a non-deduced context.
  template <class T> int f(T, T (*p)(T));
  char g(char);
  template <class T> T g(T);
  int i = f(1, g);    // calls f(int, int (*)(int))
  ```

#### Deducing template arguments taking the address of a function template <a id="temp.deduct.funcaddr">[[temp.deduct.funcaddr]]</a>

Template arguments can be deduced from the type specified when taking
the address of an overloaded function ([[over.over]]). The function
template’s function type and the specified type are used as the types of
`P` and `A`, and the deduction is done as described in 
[[temp.deduct.type]].

A placeholder type ([[dcl.spec.auto]]) in the return type of a function
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
transformations of `P` in the remainder of this section.

If `A` is not a reference type:

- If `P` is an array type, the pointer type produced by the
  array-to-pointer standard conversion ([[conv.array]]) is used in
  place of `P` for type deduction; otherwise,
- If `P` is a function type, the pointer type produced by the
  function-to-pointer standard conversion ([[conv.func]]) is used in
  place of `P` for type deduction; otherwise,
- If `P` is a cv-qualified type, the top level cv-qualifiers of `P`’s
  type are ignored for type deduction.

If `A` is a cv-qualified type, the top level cv-qualifiers of `A`’s type
are ignored for type deduction. If `A` is a reference type, the type
referred to by `A` is used for type deduction.

In general, the deduction process attempts to find template argument
values that will make the deduced `A` identical to `A`. However, there
are two cases that allow a difference:

- If the original `A` is a reference type, `A` can be more cv-qualified
  than the deduced `A` (i.e., the type referred to by the reference)
- The deduced `A` can be another pointer or pointer to member type that
  can be converted to `A` via a qualification conversion.

These alternatives are considered only if type deduction would otherwise
fail. If they yield more than one possible deduced `A`, the type
deduction fails.

When the deduction process requires a qualification conversion for a
pointer or pointer to member type as described above, the following
process is used to determine the deduced template argument values:

If `A` is a type

and `P` is a type

The cv-unqualified `T1` and `T2` are used as the types of `A` and `P`
respectively for type deduction.

``` cpp
struct A {
  template <class T> operator T***();
};
A a;
const int * const * const * p1 = a;     // T is deduced as int, not const int
```

#### Deducing template arguments during partial ordering <a id="temp.deduct.partial">[[temp.deduct.partial]]</a>

Template argument deduction is done by comparing certain types
associated with the two function templates being compared.

Two sets of types are used to determine the partial ordering. For each
of the templates involved there is the original function type and the
transformed function type. The creation of the transformed type is
described in  [[temp.func.order]]. The deduction process uses the
transformed type as the argument template and the original type of the
other template as the parameter template. This process is done twice for
each type involved in the partial ordering comparison: once using the
transformed template-1 as the argument template and template-2 as the
parameter template and again using the transformed template-2 as the
argument template and template-1 as the parameter template.

The types used to determine the ordering depend on the context in which
the partial ordering is done:

- In the context of a function call, the types used are those function
  parameter types for which the function call has arguments.[^7]
- In the context of a call to a conversion function, the return types of
  the conversion function templates are used.
- In other contexts ([[temp.func.order]]) the function template’s
  function type is used.

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

If `A` was transformed from a function parameter pack and `P` is not a
parameter pack, type deduction fails. Otherwise, using the resulting
types `P` and `A`, the deduction is then done as described in 
[[temp.deduct.type]]. If `P` is a function parameter pack, the type `A`
of each remaining parameter type of the argument template is compared
with the type `P` of the *declarator-id* of the function parameter pack.
Each comparison deduces template arguments for subsequent positions in
the template parameter packs expanded by the function parameter pack. If
deduction succeeds for a given type, the type from the argument template
is considered to be at least as specialized as the type from the
parameter template.

``` cpp
template<class... Args>           void f(Args... args);           // #1
template<class T1, class... Args> void f(T1 a1, Args... args);    // #2
template<class T1, class T2>      void f(T1 a1, T2 a2);           // #3

f();                  // calls #1
f(1, 2, 3);           // calls #2
f(1, 2);              // calls #3; non-variadic template #3 is more
                      // specialized than the variadic templates #1 and #2
```

If, for a given type, deduction succeeds in both directions (i.e., the
types are identical after the transformations above) and both `P` and
`A` were reference types (before being replaced with the type referred
to above):

- if the type from the argument template was an lvalue reference and the
  type from the parameter template was not, the argument type is
  considered to be more specialized than the other; otherwise,
- if the type from the argument template is more cv-qualified than the
  type from the parameter template (as described above), the argument
  type is considered to be more specialized than the other; otherwise,
- neither type is more specialized than the other.

If for each type being considered a given template is at least as
specialized for all types and more specialized for some set of types and
the other template is not more specialized for any types or is not at
least as specialized for any types, then the given template is more
specialized than the other template. Otherwise, neither template is more
specialized than the other.

In most cases, all template parameters must have values in order for
deduction to succeed, but for partial ordering purposes a template
parameter may remain without a value provided it is not used in the
types being used for partial ordering. A template parameter used in a
non-deduced context is considered used.

``` cpp
template <class T> T f(int);        // #1
template <class T, class U> T f(U); // #2
void g() {
  f<int>(1);        // calls #1
}
```

Partial ordering of function templates containing template parameter
packs is independent of the number of deduced arguments for those
template parameter packs.

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
deduction fails.

A given type `P` can be composed from a number of other types,
templates, and non-type values:

- A function type includes the types of each of the function parameters
  and the return type.
- A pointer to member type includes the type of the class object pointed
  to and the type of the member pointed to.
- A type that is a specialization of a class template (e.g., `A<int>`)
  includes the types, templates, and non-type values referenced by the
  template argument list of the specialization.
- An array type includes the array element type and the value of the
  array bound.

In most cases, the types, templates, and non-type values that are used
to compose `P` participate in template argument deduction. That is, they
may be used to determine the value of a template argument, and the value
so determined must be consistent with the values determined elsewhere.
In certain contexts, however, the value does not participate in type
deduction, but instead uses the values of template arguments that were
either deduced elsewhere or explicitly specified. If a template
parameter is used only in non-deduced contexts and is not explicitly
specified, template argument deduction fails.

The non-deduced contexts are:

- The *nested-name-specifier* of a type that was specified using a
  *qualified-id*.
- The *expression* of a *decltype-specifier*.
- A non-type template argument or an array bound in which a
  subexpression references a template parameter.
- A template parameter used in the parameter type of a function
  parameter that has a default argument that is being used in the call
  for which argument deduction is being done.
- A function parameter for which argument deduction cannot be done
  because the associated function argument is a function, or a set of
  overloaded functions ([[over.over]]), and one or more of the
  following apply:
  - more than one function matches the function parameter type
    (resulting in an ambiguous deduction), or
  - no function matches the function parameter type, or
  - the set of functions supplied as an argument contains one or more
    function templates.
- A function parameter for which the associated argument is an
  initializer list ([[dcl.init.list]]) but the parameter does not have
  `std::initializer_list` or reference to possibly cv-qualified
  `std::initializer_list` type.
  ``` cpp
  template<class T> void g(T);
  g({1,2,3});                 // error: no argument deduced for T
  ```
- A function parameter pack that does not occur at the end of the
  *parameter-declaration-list*.

When a type name is specified in a way that includes a non-deduced
context, all of the types that comprise that type name are also
non-deduced. However, a compound type can include both deduced and
non-deduced types. If a type is specified as `A<T>::B<T2>`, both `T` and
`T2` are non-deduced. Likewise, if a type is specified as
`A<I+J>::X<T>`, `I`, `J`, and `T` are non-deduced. If a type is
specified as `void` `f(typename` `A<T>::B,` `A<T>)`, the `T` in
`A<T>::B` is non-deduced but the `T` in `A<T>` is deduced.

Here is an example in which different parameter/argument pairs produce
inconsistent template argument deductions:

``` cpp
template<class T> void f(T x, T y) { /* ... */ }
struct A { /* ... */ };
struct B : A { /* ... */ };
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

A template type argument `T`, a template template argument `TT` or a
template non-type argument `i` can be deduced if `P` and `A` have one of
the following forms:

``` cpp
T
cv-list T
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

where `(T)` represents a *parameter-type-list* where at least one
parameter type contains a `T`, and `()` represents a
*parameter-type-list* where no parameter type contains a `T`. Similarly,
`<T>` represents template argument lists where at least one argument
contains a `T`, `<i>` represents template argument lists where at least
one argument contains an `i` and `<>` represents template argument lists
where no argument contains a `T` or an `i`.

If `P` has a form that contains `<T>` or `<i>`, then each argument Pᵢ of
the respective template argument list `P` is compared with the
corresponding argument Aᵢ of the corresponding template argument list of
`A`. If the template argument list of `P` contains a pack expansion that
is not the last template argument, the entire template argument list is
a non-deduced context. If `Pᵢ` is a pack expansion, then the pattern of
`Pᵢ` is compared with each remaining argument in the template argument
list of `A`. Each comparison deduces template arguments for subsequent
positions in the template parameter packs expanded by `Pᵢ`. During
partial ordering ([[temp.deduct.partial]]), if `Aᵢ` was originally a
pack expansion:

- if `P` does not contain a template argument corresponding to `Aᵢ` then
  `Aᵢ` is ignored;
- otherwise, if `Pᵢ` is not a pack expansion, template argument
  deduction fails.

``` cpp
template<class T1, class... Z> class S;                               // #1
template<class T1, class... Z> class S<T1, const Z&...> { };          // #2
template<class T1, class T2>   class S<T1, const T2&> { };            // #3
S<int, const int&> s;         // both #2 and #3 match; #3 is more specialized

template<class T, class... U>            struct A { };                // #1
template<class T1, class T2, class... U> struct A<T1, T2*, U...> { }; // #2
template<class T1, class T2>             struct A<T1, T2> { };        // #3
template struct A<int, int*>; // selects #2
```

Similarly, if `P` has a form that contains `(T)`, then each parameter
type `Pᵢ` of the respective *parameter-type-list* of `P` is compared
with the corresponding parameter type `Aᵢ` of the corresponding
*parameter-type-list* of `A`. If `P` and `A` are function types that
originated from deduction when taking the address of a function
template ([[temp.deduct.funcaddr]]) or when deducing template arguments
from a function declaration ([[temp.deduct.decl]]) and `Pᵢ` and `Aᵢ`
are parameters of the top-level *parameter-type-list* of `P` and `A`,
respectively, `Pᵢ` is adjusted if it is an rvalue reference to a
cv-unqualified template parameter and `Aᵢ` is an lvalue reference, in
which case the type of `Pᵢ` is changed to be the template parameter type
(i.e., `T&&` is changed to simply `T`). As a result, when `Pᵢ` is `T&&`
and `Aᵢ` is `X&`, the adjusted `Pᵢ` will be `T`, causing `T` to be
deduced as `X&`.

``` cpp
template <class T> void f(T&&);
template <> void f(int&) { }  // #1
template <> void f(int&&) { } // #2
void g(int i) {
  f(i);                       // calls f<int&>(int&), i.e., #1
  f(0);                       // calls f<int>(int&&), i.e., #2
}
```

If the *parameter-declaration* corresponding to `Pᵢ` is a function
parameter pack, then the type of its *declarator-id* is compared with
each remaining parameter type in the *parameter-type-list* of `A`. Each
comparison deduces template arguments for subsequent positions in the
template parameter packs expanded by the function parameter pack. During
partial ordering ([[temp.deduct.partial]]), if `Aᵢ` was originally a
function parameter pack:

- if `P` does not contain a function parameter type corresponding to
  `Aᵢ` then `Aᵢ` is ignored;
- otherwise, if `Pᵢ` is not a function parameter pack, template argument
  deduction fails.

``` cpp
template<class T, class... U> void f(T*, U...) { }    // #1
template<class T>             void f(T) { }           // #2
template void f(int*);      // selects #1
```

These forms can be used in the same way as `T` is for further
composition of types.

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

Template arguments cannot be deduced from function arguments involving
constructs other than the ones specified above.

A template type argument cannot be deduced from the type of a non-type
*template-argument*.

``` cpp
template<class T, T i> void f(double a[10][i]);
int v[10][20];
f(v);               // error: argument for template-parameter T cannot be deduced
```

Except for reference and pointer types, a major array bound is not part
of a function parameter type and cannot be deduced from an argument:

``` cpp
template<int i> void f1(int a[10][i]);
template<int i> void f2(int a[i][20]);
template<int i> void f3(int (&a)[i][20]);

void g() {
  int v[10][20];
  f1(v);            // OK: i deduced to be 20
  f1<20>(v);        // OK
  f2(v);            // error: cannot deduce template-argument i
  f2<10>(v);        // OK
  f3(v);            // OK: i deduced to be 10
}
```

If, in the declaration of a function template with a non-type template
parameter, the non-type template parameter is used in a subexpression in
the function parameter list, the expression is a non-deduced context as
specified above.

``` cpp
template <int i> class A { /* ... */ };
template <int i> void g(A<i+1>);
template <int i> void f(A<i>, A<i+1>);
void k() {
  A<1> a1;
  A<2> a2;
  g(a1);            // error: deduction fails for expression i+1
  g<0>(a1);         // OK
  f(a1, a2);        // OK
}
```

Template parameters do not participate in template argument deduction if
they are used only in non-deduced contexts. For example,

``` cpp
template<int i, typename T>
T deduce(typename A<T>::X x,    // T is not deduced here
  T t,                          // but T is deduced here
  typename B<i>::Y y);          // i is not deduced here
A<int> a;
B<77>  b;

int    x = deduce<77>(a.xm, 62, b.ym);
// T is deduced to be int, a.xm must be convertible to
// A<int>::X
// i is explicitly specified to be 77, b.ym must be convertible
// to B<77>::Y
```

If `P` has a form that contains `<i>`, and if the type of the
corresponding value of `A` differs from the type of `i`, deduction
fails. If `P` has a form that contains `[i]`, and if the type of `i` is
not an integral type, deduction fails.[^8]

``` cpp
template<int i> class A { /* ... */ };
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

A *template-argument* can be deduced from a function, pointer to
function, or pointer to member function type.

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

A template *type-parameter* cannot be deduced from the type of a
function default argument.

``` cpp
template <class T> void f(T = 5, T = 7);
void g() {
  f(1);             // OK: call f<int>(1,7)
  f();              // error: cannot deduce T
  f<int>();         // OK: call f<int>(5,7)
}
```

The *template-argument* corresponding to a template *template-parameter*
is deduced from the type of the *template-argument* of a class template
specialization used in the argument list of a function call.

``` cpp
template <template <class T> class X> struct A { };
template <template <class T> class X> void f(A<X>) { }
template<class T> struct B { };
A<B> ab;
f(ab);              // calls f(A<B>)
```

Template argument deduction involving parameter packs (
[[temp.variadic]]) can deduce zero or more arguments for each parameter
pack.

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

#### Deducing template arguments from a function declaration <a id="temp.deduct.decl">[[temp.deduct.decl]]</a>

In a declaration whose *declarator-id* refers to a specialization of a
function template, template argument deduction is performed to identify
the specialization to which the declaration refers. Specifically, this
is done for explicit instantiations ([[temp.explicit]]), explicit
specializations ([[temp.expl.spec]]), and certain friend declarations (
[[temp.friend]]). This is also done to determine whether a deallocation
function template specialization matches a placement `operator new` (
[[basic.stc.dynamic.deallocation]],  [[expr.new]]). In all these cases,
`P` is the type of the function template being considered as a potential
match and `A` is either the function type from the declaration or the
type of the deallocation function that would match the placement
`operator new` as described in  [[expr.new]]. The deduction is done as
described in  [[temp.deduct.type]].

If, for the set of function templates so considered, there is either no
match or more than one match after partial ordering has been
considered ([[temp.func.order]]), deduction fails and, in the
declaration cases, the program is ill-formed.

### Overload resolution <a id="temp.over">[[temp.over]]</a>

A function template can be overloaded either by (non-template) functions
of its name or by (other) function templates of the same name. When a
call to that name is written (explicitly, or implicitly using the
operator notation), template argument deduction ([[temp.deduct]]) and
checking of any explicit template arguments ([[temp.arg]]) are
performed for each function template to find the template argument
values (if any) that can be used with that function template to
instantiate a function template specialization that can be invoked with
the call arguments. For each function template, if the argument
deduction and checking succeeds, the *template-argument*s (deduced
and/or explicit) are used to synthesize the declaration of a single
function template specialization which is added to the candidate
functions set to be used in overload resolution. If, for a given
function template, argument deduction fails, no such function is added
to the set of candidate functions for that template. The complete set of
candidate functions includes all the synthesized declarations and all of
the non-template overloaded functions of the same name. The synthesized
declarations are treated like any other functions in the remainder of
overload resolution, except as explicitly noted in 
[[over.match.best]].[^9]

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

Here is an example involving conversions on a function argument involved
in *template-argument* deduction:

``` cpp
template<class T> struct B { /* ... */ };
template<class T> struct D : public B<T> { /* ... */ };
template<class T> void f(B<T>&);

void g(B<int>& bi, D<int>& di) {
  f(bi);            // f(bi)
  f(di);            // f((B<int>&)di)
}
```

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

Only the signature of a function template specialization is needed to
enter the specialization in a set of candidate functions. Therefore only
the function template declaration is needed to resolve a call for which
a template specialization is a candidate.

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

<!-- Link reference definitions -->
[basic.def.odr]: basic.md#basic.def.odr
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.classref]: basic.md#basic.lookup.classref
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope]: basic.md#basic.scope
[basic.scope.hiding]: basic.md#basic.scope.hiding
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.types]: basic.md#basic.types
[class]: class.md#class
[class.abstract]: class.md#class.abstract
[class.access]: class.md#class.access
[class.base.init]: special.md#class.base.init
[class.derived]: class.md#class.derived
[class.dtor]: special.md#class.dtor
[class.friend]: class.md#class.friend
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.qual]: basic.md#class.qual
[conv]: conv.md#conv
[conv.array]: conv.md#conv.array
[conv.func]: conv.md#conv.func
[conv.integral]: conv.md#conv.integral
[conv.mem]: conv.md#conv.mem
[conv.ptr]: conv.md#conv.ptr
[conv.qual]: conv.md#conv.qual
[dcl.align]: dcl.md#dcl.align
[dcl.attr.grammar]: dcl.md#dcl.attr.grammar
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.meaning]: dcl.md#dcl.meaning
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.type.elab]: dcl.md#dcl.type.elab
[except.spec]: except.md#except.spec
[expr.const]: expr.md#expr.const
[expr.new]: expr.md#expr.new
[expr.prim.lambda]: expr.md#expr.prim.lambda
[expr.ref]: expr.md#expr.ref
[expr.sizeof]: expr.md#expr.sizeof
[expr.unary.op]: expr.md#expr.unary.op
[intro.defs]: intro.md#intro.defs
[lex.string]: lex.md#lex.string
[namespace.def]: dcl.md#namespace.def
[namespace.memdef]: dcl.md#namespace.memdef
[over.ics.rank]: over.md#over.ics.rank
[over.match.best]: over.md#over.match.best
[over.match.conv]: over.md#over.match.conv
[over.match.ref]: over.md#over.match.ref
[over.over]: over.md#over.over
[special]: special.md#special
[support.types]: language.md#support.types
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
[temp.decls]: #temp.decls
[temp.deduct]: #temp.deduct
[temp.deduct.call]: #temp.deduct.call
[temp.deduct.conv]: #temp.deduct.conv
[temp.deduct.decl]: #temp.deduct.decl
[temp.deduct.funcaddr]: #temp.deduct.funcaddr
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

[^4]: There is no way in which they could be used.

[^5]: That is, declarations of non-template functions do not merely
    guide overload resolution of function template specializations with
    the same name. If such a non-template function is odr-used (
    [[basic.def.odr]]) in a program, it must be defined; it will not be
    implicitly instantiated using the function template definition.

[^6]: Friend declarations do not introduce new names into any scope,
    either when the template is declared or when it is instantiated.

[^7]: Default arguments are not considered to be arguments in this
    context; they only become arguments after a function has been
    selected.

[^8]: Although the *template-argument* corresponding to a
    *template-parameter* of type `bool` may be deduced from an array
    bound, the resulting value will always be `true` because the array
    bound will be non-zero.

[^9]: The parameters of function template specializations contain no
    template parameter types. The set of conversions allowed on deduced
    arguments is limited, because the argument deduction process
    produces function templates with parameters that either match the
    call arguments exactly or differ only in ways that can be bridged by
    the allowed limited conversions. Non-deduced arguments allow the
    full range of conversions. Note also that  [[over.match.best]]
    specifies that a non-template function will be given preference over
    a template specialization if the two functions are otherwise equally
    good candidates for an overload match.
