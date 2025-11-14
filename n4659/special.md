# Special member functions <a id="special">[[special]]</a>

The default constructor ([[class.ctor]]), copy constructor and copy
assignment operator ([[class.copy]]), move constructor and move
assignment operator ([[class.copy]]), and destructor ([[class.dtor]])
are *special member functions*.

[*Note 1*: The implementation will implicitly declare these member
functions for some class types when the program does not explicitly
declare them. The implementation will implicitly define them if they are
odr-used ([[basic.def.odr]]). See  [[class.ctor]], [[class.dtor]] and 
[[class.copy]]. — *end note*]

An implicitly-declared special member function is declared at the
closing `}` of the *class-specifier*. Programs shall not define
implicitly-declared special member functions.

Programs may explicitly refer to implicitly-declared special member
functions.

[*Example 1*:

A program may explicitly call, take the address of, or form a pointer to
member to an implicitly-declared special member function.

``` cpp
struct A { };                   // implicitly declared A::operator=
struct B : A {
  B& operator=(const B &);
};
B& B::operator=(const B& s) {
  this->A::operator=(s);        // well formed
  return *this;
}
```

— *end example*]

[*Note 2*: The special member functions affect the way objects of class
type are created, copied, moved, and destroyed, and how values can be
converted to values of other types. Often such special member functions
are called implicitly. — *end note*]

Special member functions obey the usual access rules (Clause 
[[class.access]]).

[*Example 2*: Declaring a constructor `protected` ensures that only
derived classes and friends can create objects using
it. — *end example*]

For a class, its non-static data members, its non-virtual direct base
classes, and, if the class is not abstract ([[class.abstract]]), its
virtual base classes are called its *potentially constructed
subobjects*.

## Constructors <a id="class.ctor">[[class.ctor]]</a>

Constructors do not have names. In a declaration of a constructor, the
*declarator* is a function declarator ([[dcl.fct]]) of the form

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' noexcept-specifier\opt attribute-specifier-seq\opt
```

where the *ptr-declarator* consists solely of an *id-expression*, an
optional *attribute-specifier-seq*, and optional surrounding
parentheses, and the *id-expression* has one of the following forms:

- in a *member-declaration* that belongs to the *member-specification*
  of a class but is not a friend declaration ([[class.friend]]), the
  *id-expression* is the injected-class-name (Clause  [[class]]) of the
  immediately-enclosing class;
- in a *member-declaration* that belongs to the *member-specification*
  of a class template but is not a friend declaration, the
  *id-expression* is a *class-name* that names the current
  instantiation ([[temp.dep.type]]) of the immediately-enclosing class
  template; or
- in a declaration at namespace scope or in a friend declaration, the
  *id-expression* is a *qualified-id* that names a constructor (
  [[class.qual]]).

The *class-name* shall not be a *typedef-name*. In a constructor
declaration, each *decl-specifier* in the optional *decl-specifier-seq*
shall be `friend`, `inline`, `explicit`, or `constexpr`.

[*Example 1*:

``` cpp
struct S {
  S();              // declares the constructor
};

S::S() { }          // defines the constructor
```

— *end example*]

A constructor is used to initialize objects of its class type. Because
constructors do not have names, they are never found during name lookup;
however an explicit type conversion using the functional notation (
[[expr.type.conv]]) will cause a constructor to be called to initialize
an object.

[*Note 1*: For initialization of objects of class type see 
[[class.init]]. — *end note*]

A constructor can be invoked for a `const`, `volatile` or `const`
`volatile` object. `const` and `volatile` semantics ([[dcl.type.cv]])
are not applied on an object under construction. They come into effect
when the constructor for the most derived object ([[intro.object]])
ends.

A *default* constructor for a class `X` is a constructor of class `X`
for which each parameter that is not a function parameter pack has a
default argument (including the case of a constructor with no
parameters). If there is no user-declared constructor for class `X`, a
non-explicit constructor having no parameters is implicitly declared as
defaulted ([[dcl.fct.def]]). An implicitly-declared default constructor
is an `inline` `public` member of its class.

A defaulted default constructor for class `X` is defined as deleted if:

- `X` is a union that has a variant member with a non-trivial default
  constructor and no variant member of `X` has a default member
  initializer,
- `X` is a non-union class that has a variant member `M` with a
  non-trivial default constructor and no variant member of the anonymous
  union containing `M` has a default member initializer,
- any non-static data member with no default member initializer (
  [[class.mem]]) is of reference type,
- any non-variant non-static data member of const-qualified type (or
  array thereof) with no *brace-or-equal-initializer* does not have a
  user-provided default constructor,
- `X` is a union and all of its variant members are of const-qualified
  type (or array thereof),
- `X` is a non-union class and all members of any anonymous union member
  are of const-qualified type (or array thereof),
- any potentially constructed subobject, except for a non-static data
  member with a *brace-or-equal-initializer*, has class type `M` (or
  array thereof) and either `M` has no default constructor or overload
  resolution ([[over.match]]) as applied to find `M`’s corresponding
  constructor results in an ambiguity or in a function that is deleted
  or inaccessible from the defaulted default constructor, or
- any potentially constructed subobject has a type with a destructor
  that is deleted or inaccessible from the defaulted default
  constructor.

A default constructor is *trivial* if it is not user-provided and if:

- its class has no virtual functions ([[class.virtual]]) and no virtual
  base classes ([[class.mi]]), and
- no non-static data member of its class has a default member
  initializer ([[class.mem]]), and
- all the direct base classes of its class have trivial default
  constructors, and
- for all the non-static data members of its class that are of class
  type (or array thereof), each such class has a trivial default
  constructor.

Otherwise, the default constructor is *non-trivial*.

A default constructor that is defaulted and not defined as deleted is
*implicitly defined* when it is odr-used ([[basic.def.odr]]) to create
an object of its class type ([[intro.object]]) or when it is explicitly
defaulted after its first declaration. The implicitly-defined default
constructor performs the set of initializations of the class that would
be performed by a user-written default constructor for that class with
no *ctor-initializer* ([[class.base.init]]) and an empty
*compound-statement*. If that user-written default constructor would be
ill-formed, the program is ill-formed. If that user-written default
constructor would satisfy the requirements of a constexpr constructor (
[[dcl.constexpr]]), the implicitly-defined default constructor is
`constexpr`. Before the defaulted default constructor for a class is
implicitly defined, all the non-user-provided default constructors for
its base classes and its non-static data members shall have been
implicitly defined.

[*Note 2*: An implicitly-declared default constructor has an exception
specification ([[except.spec]]). An explicitly-defaulted definition
might have an implicit exception specification, see 
[[dcl.fct.def]]. — *end note*]

Default constructors are called implicitly to create class objects of
static, thread, or automatic storage duration ([[basic.stc.static]],
[[basic.stc.thread]], [[basic.stc.auto]]) defined without an
initializer ([[dcl.init]]), are called to create class objects of
dynamic storage duration ([[basic.stc.dynamic]]) created by a
*new-expression* in which the *new-initializer* is omitted (
[[expr.new]]), or are called when the explicit type conversion syntax (
[[expr.type.conv]]) is used. A program is ill-formed if the default
constructor for an object is implicitly used and the constructor is not
accessible (Clause  [[class.access]]).

[*Note 3*:  [[class.base.init]] describes the order in which
constructors for base classes and non-static data members are called and
describes how arguments can be specified for the calls to these
constructors. — *end note*]

A `return` statement in the body of a constructor shall not specify a
return value. The address of a constructor shall not be taken.

A functional notation type conversion ([[expr.type.conv]]) can be used
to create new objects of its type.

[*Note 4*: The syntax looks like an explicit call of the
constructor. — *end note*]

[*Example 2*:

``` cpp
complex zz = complex(1,2.3);
cprint( complex(7.8,1.2) );
```

— *end example*]

An object created in this way is unnamed.

[*Note 5*:  [[class.temporary]] describes the lifetime of temporary
objects. — *end note*]

[*Note 6*: Explicit constructor calls do not yield lvalues, see 
[[basic.lval]]. — *end note*]

[*Note 7*:  Some language constructs have special semantics when used
during construction; see  [[class.base.init]] and 
[[class.cdtor]]. — *end note*]

During the construction of an object, if the value of the object or any
of its subobjects is accessed through a glvalue that is not obtained,
directly or indirectly, from the constructor’s `this` pointer, the value
of the object or subobject thus obtained is unspecified.

[*Example 3*:

``` cpp
struct C;
void no_opt(C*);

struct C {
  int c;
  C() : c(0) { no_opt(this); }
};

const C cobj;

void no_opt(C* cptr) {
  int i = cobj.c * 100;         // value of cobj.c is unspecified
  cptr->c = 1;
  cout << cobj.c * 100          // value of cobj.c is unspecified
       << '\n';
}

extern struct D d;
struct D {
  D(int a) : a(a), b(d.a) {}
  int a, b;
};
D d = D(1);                     // value of d.b is unspecified
```

— *end example*]

## Temporary objects <a id="class.temporary">[[class.temporary]]</a>

Temporary objects are created

- when a prvalue is materialized so that it can be used as a glvalue (
  [[conv.rval]]),
- when needed by the implementation to pass or return an object of
  trivially-copyable type (see below), and
- when throwing an exception ([[except.throw]]). \[*Note 1*: The
  lifetime of exception objects is described in 
  [[except.throw]]. — *end note*]

Even when the creation of the temporary object is unevaluated (Clause 
[[expr]]), all the semantic restrictions shall be respected as if the
temporary object had been created and later destroyed.

[*Note 1*: This includes accessibility (Clause  [[class.access]]) and
whether it is deleted, for the constructor selected and for the
destructor. However, in the special case of the operand of a
*decltype-specifier* ([[expr.call]]), no temporary is introduced, so
the foregoing does not apply to such a prvalue. — *end note*]

The materialization of a temporary object is generally delayed as long
as possible in order to avoid creating unnecessary temporary objects.

[*Note 2*:

Temporary objects are materialized:

- when binding a reference to a prvalue ([[dcl.init.ref]],
  [[expr.type.conv]], [[expr.dynamic.cast]], [[expr.static.cast]],
  [[expr.const.cast]], [[expr.cast]]),
- when performing member access on a class prvalue ([[expr.ref]],
  [[expr.mptr.oper]]),
- when performing an array-to-pointer conversion or subscripting on an
  array prvalue ([[conv.array]], [[expr.sub]]),
- when initializing an object of type `std::initializer_list<T>` from a
  *braced-init-list* ([[dcl.init.list]]),
- for certain unevaluated operands ([[expr.typeid]], [[expr.sizeof]]),
  and
- when a prvalue appears as a discarded-value expression (Clause 
  [[expr]]).

— *end note*]

[*Example 1*:

Consider the following code:

``` cpp
class X {
public:
  X(int);
  X(const X&);
  X& operator=(const X&);
  ~X();
};

class Y {
public:
  Y(int);
  Y(Y&&);
  ~Y();
};

X f(X);
Y g(Y);

void h() {
  X a(1);
  X b = f(X(2));
  Y c = g(Y(3));
  a = f(a);
}
```

`X(2)` is constructed in the space used to hold `f()`’s argument and
`Y(3)` is constructed in the space used to hold `g()`’s argument.
Likewise, `f()`’s result is constructed directly in `b` and `g()`’s
result is constructed directly in `c`. On the other hand, the expression
`a = f(a)` requires a temporary for the result of `f(a)`, which is
materialized so that the reference parameter of `A::operator=(const A&)`
can bind to it.

— *end example*]

When an object of class type `X` is passed to or returned from a
function, if each copy constructor, move constructor, and destructor of
`X` is either trivial or deleted, and `X` has at least one non-deleted
copy or move constructor, implementations are permitted to create a
temporary object to hold the function parameter or result object. The
temporary object is constructed from the function argument or return
value, respectively, and the function’s parameter or return object is
initialized as if by using the non-deleted trivial constructor to copy
the temporary (even if that constructor is inaccessible or would not be
selected by overload resolution to perform a copy or move of the
object).

[*Note 3*: This latitude is granted to allow objects of class type to
be passed to or returned from functions in registers. — *end note*]

When an implementation introduces a temporary object of a class that has
a non-trivial constructor ([[class.ctor]], [[class.copy]]), it shall
ensure that a constructor is called for the temporary object. Similarly,
the destructor shall be called for a temporary with a non-trivial
destructor ([[class.dtor]]). Temporary objects are destroyed as the
last step in evaluating the full-expression ([[intro.execution]]) that
(lexically) contains the point where they were created. This is true
even if that evaluation ends in throwing an exception. The value
computations and side effects of destroying a temporary object are
associated only with the full-expression, not with any specific
subexpression.

There are three contexts in which temporaries are destroyed at a
different point than the end of the full-expression. The first context
is when a default constructor is called to initialize an element of an
array with no corresponding initializer ([[dcl.init]]). The second
context is when a copy constructor is called to copy an element of an
array while the entire array is copied ([[expr.prim.lambda.capture]], 
[[class.copy]]). In either case, if the constructor has one or more
default arguments, the destruction of every temporary created in a
default argument is sequenced before the construction of the next array
element, if any.

The third context is when a reference is bound to a temporary.[^1] The
temporary to which the reference is bound or the temporary that is the
complete object of a subobject to which the reference is bound persists
for the lifetime of the reference except:

- A temporary object bound to a reference parameter in a function call (
  [[expr.call]]) persists until the completion of the full-expression
  containing the call.
- The lifetime of a temporary bound to the returned value in a function
  return statement ([[stmt.return]]) is not extended; the temporary is
  destroyed at the end of the full-expression in the return statement.
- A temporary bound to a reference in a *new-initializer* (
  [[expr.new]]) persists until the completion of the full-expression
  containing the *new-initializer*.
  \[*Example 1*:
  ``` cpp
  struct S { int mi; const std::pair<int,int>& mp; };
  S a { 1, {2,3} };
  S* p = new S{ 1, {2,3} };   // Creates dangling reference
  ```

  — *end example*]
  \[*Note 2*: This may introduce a dangling reference, and
  implementations are encouraged to issue a warning in such a
  case. — *end note*]

The destruction of a temporary whose lifetime is not extended by being
bound to a reference is sequenced before the destruction of every
temporary which is constructed earlier in the same full-expression. If
the lifetime of two or more temporaries to which references are bound
ends at the same point, these temporaries are destroyed at that point in
the reverse order of the completion of their construction. In addition,
the destruction of temporaries bound to references shall take into
account the ordering of destruction of objects with static, thread, or
automatic storage duration ([[basic.stc.static]], [[basic.stc.thread]],
[[basic.stc.auto]]); that is, if `obj1` is an object with the same
storage duration as the temporary and created before the temporary is
created the temporary shall be destroyed before `obj1` is destroyed; if
`obj2` is an object with the same storage duration as the temporary and
created after the temporary is created the temporary shall be destroyed
after `obj2` is destroyed.

[*Example 2*:

``` cpp
struct S {
  S();
  S(int);
  friend S operator+(const S&, const S&);
  ~S();
};
S obj1;
const S& cr = S(16)+S(23);
S obj2;
```

the expression `S(16) + S(23)` creates three temporaries: a first
temporary `T1` to hold the result of the expression `S(16)`, a second
temporary `T2` to hold the result of the expression `S(23)`, and a third
temporary `T3` to hold the result of the addition of these two
expressions. The temporary `T3` is then bound to the reference `cr`. It
is unspecified whether `T1` or `T2` is created first. On an
implementation where `T1` is created before `T2`, `T2` shall be
destroyed before `T1`. The temporaries `T1` and `T2` are bound to the
reference parameters of `operator+`; these temporaries are destroyed at
the end of the full-expression containing the call to `operator+`. The
temporary `T3` bound to the reference `cr` is destroyed at the end of
`cr`’s lifetime, that is, at the end of the program. In addition, the
order in which `T3` is destroyed takes into account the destruction
order of other objects with static storage duration. That is, because
`obj1` is constructed before `T3`, and `T3` is constructed before
`obj2`, `obj2` shall be destroyed before `T3`, and `T3` shall be
destroyed before `obj1`.

— *end example*]

## Conversions <a id="class.conv">[[class.conv]]</a>

Type conversions of class objects can be specified by constructors and
by conversion functions. These conversions are called *user-defined
conversions* and are used for implicit type conversions (Clause 
[[conv]]), for initialization ([[dcl.init]]), and for explicit type
conversions ([[expr.cast]], [[expr.static.cast]]).

User-defined conversions are applied only where they are unambiguous (
[[class.member.lookup]], [[class.conv.fct]]). Conversions obey the
access control rules (Clause  [[class.access]]). Access control is
applied after ambiguity resolution ([[basic.lookup]]).

[*Note 1*: See  [[over.match]] for a discussion of the use of
conversions in function calls as well as examples below. — *end note*]

At most one user-defined conversion (constructor or conversion function)
is implicitly applied to a single value.

[*Example 1*:

``` cpp
struct X {
  operator int();
};

struct Y {
  operator X();
};

Y a;
int b = a;          // error, a.operator X().operator int() not tried
int c = X(a);       // OK: a.operator X().operator int()
```

— *end example*]

User-defined conversions are used implicitly only if they are
unambiguous. A conversion function in a derived class does not hide a
conversion function in a base class unless the two functions convert to
the same type. Function overload resolution ([[over.match.best]])
selects the best conversion function to perform the conversion.

[*Example 2*:

``` cpp
struct X {
  operator int();
};

struct Y : X {
    operator char();
};

void f(Y& a) {
  if (a) {          // ill-formed: X::operator int() or Y::operator char()
  }
}
```

— *end example*]

### Conversion by constructor <a id="class.conv.ctor">[[class.conv.ctor]]</a>

A constructor declared without the *function-specifier* `explicit`
specifies a conversion from the types of its parameters (if any) to the
type of its class. Such a constructor is called a *converting
constructor*.

[*Example 1*:

``` cpp
struct X {
    X(int);
    X(const char*, int =0);
    X(int, int);
};

void f(X arg) {
  X a = 1;          // a = X(1)
  X b = "Jessie";   // b = X("Jessie",0)
  a = 2;            // a = X(2)
  f(3);             // f(X(3))
  f({1, 2});        // f(X(1,2))
}
```

— *end example*]

[*Note 1*:

An explicit constructor constructs objects just like non-explicit
constructors, but does so only where the direct-initialization syntax (
[[dcl.init]]) or where casts ([[expr.static.cast]], [[expr.cast]]) are
explicitly used; see also  [[over.match.copy]]. A default constructor
may be an explicit constructor; such a constructor will be used to
perform default-initialization or value-initialization ([[dcl.init]]).

[*Example 2*:

``` cpp
struct Z {
  explicit Z();
  explicit Z(int);
  explicit Z(int, int);
};

Z a;                            // OK: default-initialization performed
Z b{};                          // OK: direct initialization syntax used
Z c = {};                       // error: copy-list-initialization
Z a1 = 1;                       // error: no implicit conversion
Z a3 = Z(1);                    // OK: direct initialization syntax used
Z a2(1);                        // OK: direct initialization syntax used
Z* p = new Z(1);                // OK: direct initialization syntax used
Z a4 = (Z)1;                    // OK: explicit cast used
Z a5 = static_cast<Z>(1);       // OK: explicit cast used
Z a6 = { 3, 4 };                // error: no implicit conversion
```

— *end example*]

— *end note*]

A non-explicit copy/move constructor ([[class.copy]]) is a converting
constructor.

[*Note 2*: An implicitly-declared copy/move constructor is not an
explicit constructor; it may be called for implicit type
conversions. — *end note*]

### Conversion functions <a id="class.conv.fct">[[class.conv.fct]]</a>

A member function of a class `X` having no parameters with a name of the
form

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

specifies a conversion from `X` to the type specified by the
*conversion-type-id*. Such functions are called *conversion functions*.
A *decl-specifier* in the *decl-specifier-seq* of a conversion function
(if any) shall be neither a *defining-type-specifier* nor `static`. The
type of the conversion function ([[dcl.fct]]) is “function taking no
parameter returning *conversion-type-id*”. A conversion function is
never used to convert a (possibly cv-qualified) object to the (possibly
cv-qualified) same object type (or a reference to it), to a (possibly
cv-qualified) base class of that type (or a reference to it), or to
(possibly cv-qualified) void.[^2]

[*Example 1*:

``` cpp
struct X {
  operator int();
  operator auto() -> short;     // error: trailing return type
};

void f(X a) {
  int i = int(a);
  i = (int)a;
  i = a;
}
```

In all three cases the value assigned will be converted by
`X::operator int()`.

— *end example*]

A conversion function may be explicit ([[dcl.fct.spec]]), in which case
it is only considered as a user-defined conversion for
direct-initialization ([[dcl.init]]). Otherwise, user-defined
conversions are not restricted to use in assignments and
initializations.

[*Example 2*:

``` cpp
class Y { };
struct Z {
  explicit operator Y() const;
};

void h(Z z) {
  Y y1(z);          // OK: direct-initialization
  Y y2 = z;         // ill-formed: copy-initialization
  Y y3 = (Y)z;      // OK: cast notation
}

void g(X a, X b) {
  int i = (a) ? 1+a : 0;
  int j = (a&&b) ? a+b : i;
  if (a) {
  }
}
```

— *end example*]

The *conversion-type-id* shall not represent a function type nor an
array type. The *conversion-type-id* in a *conversion-function-id* is
the longest sequence of tokens that could possibly form a
*conversion-type-id*.

[*Note 1*:

This prevents ambiguities between the declarator operator `*` and its
expression counterparts.

[*Example 3*:

``` cpp
&ac.operator int*i; // syntax error:
                    // parsed as: &(ac.operator int *)i
                    // not as: &(ac.operator int)*i
```

The `*` is the pointer declarator and not the multiplication operator.

— *end example*]

This rule also prevents ambiguities for attributes.

[*Example 4*:

``` cpp
operator int [[noreturn]] ();   // error: noreturn attribute applied to a type
```

— *end example*]

— *end note*]

Conversion functions are inherited.

Conversion functions can be virtual.

A conversion function template shall not have a deduced return type (
[[dcl.spec.auto]]).

[*Example 5*:

``` cpp
struct S {
  operator auto() const { return 10; }      // OK
  template<class T>
  operator auto() const { return 1.2; }     // error: conversion function template
};
```

— *end example*]

## Destructors <a id="class.dtor">[[class.dtor]]</a>

In a declaration of a destructor, the *declarator* is a function
declarator ([[dcl.fct]]) of the form

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' noexcept-specifier\opt attribute-specifier-seq\opt
```

where the *ptr-declarator* consists solely of an *id-expression*, an
optional *attribute-specifier-seq*, and optional surrounding
parentheses, and the *id-expression* has one of the following forms:

- in a *member-declaration* that belongs to the *member-specification*
  of a class but is not a friend declaration ([[class.friend]]), the
  *id-expression* is `~`*class-name* and the *class-name* is the
  injected-class-name (Clause  [[class]]) of the immediately-enclosing
  class;
- in a *member-declaration* that belongs to the *member-specification*
  of a class template but is not a friend declaration, the
  *id-expression* is `~`*class-name* and the *class-name* names the
  current instantiation ([[temp.dep.type]]) of the
  immediately-enclosing class template; or
- in a declaration at namespace scope or in a friend declaration, the
  *id-expression* is *nested-name-specifier* `~`*class-name* and the
  *class-name* names the same class as the *nested-name-specifier*.

The *class-name* shall not be a *typedef-name*. A destructor shall take
no arguments ([[dcl.fct]]). Each *decl-specifier* of the
*decl-specifier-seq* of a destructor declaration (if any) shall be
`friend`, `inline`, or `virtual`.

A destructor is used to destroy objects of its class type. The address
of a destructor shall not be taken. A destructor can be invoked for a
`const`, `volatile` or `const` `volatile` object. `const` and `volatile`
semantics ([[dcl.type.cv]]) are not applied on an object under
destruction. They stop being in effect when the destructor for the most
derived object ([[intro.object]]) starts.

[*Note 1*: A declaration of a destructor that does not have a
*noexcept-specifier* has the same exception specification as if had been
implicitly declared ([[except.spec]]). — *end note*]

If a class has no user-declared destructor, a destructor is implicitly
declared as defaulted ([[dcl.fct.def]]). An implicitly-declared
destructor is an `inline` `public` member of its class.

A defaulted destructor for a class `X` is defined as deleted if:

- `X` is a union-like class that has a variant member with a non-trivial
  destructor,
- any potentially constructed subobject has class type `M` (or array
  thereof) and `M` has a deleted destructor or a destructor that is
  inaccessible from the defaulted destructor,
- or, for a virtual destructor, lookup of the non-array deallocation
  function results in an ambiguity or in a function that is deleted or
  inaccessible from the defaulted destructor.

A destructor is trivial if it is not user-provided and if:

- the destructor is not `virtual`,
- all of the direct base classes of its class have trivial destructors,
  and
- for all of the non-static data members of its class that are of class
  type (or array thereof), each such class has a trivial destructor.

Otherwise, the destructor is *non-trivial*.

A destructor that is defaulted and not defined as deleted is *implicitly
defined* when it is odr-used ([[basic.def.odr]]) or when it is
explicitly defaulted after its first declaration.

Before the defaulted destructor for a class is implicitly defined, all
the non-user-provided destructors for its base classes and its
non-static data members shall have been implicitly defined.

After executing the body of the destructor and destroying any automatic
objects allocated within the body, a destructor for class `X` calls the
destructors for `X`’s direct non-variant non-static data members, the
destructors for `X`’s non-virtual direct base classes and, if `X` is the
type of the most derived class ([[class.base.init]]), its destructor
calls the destructors for `X`’s virtual base classes. All destructors
are called as if they were referenced with a qualified name, that is,
ignoring any possible virtual overriding destructors in more derived
classes. Bases and members are destroyed in the reverse order of the
completion of their constructor (see  [[class.base.init]]). A `return`
statement ([[stmt.return]]) in a destructor might not directly return
to the caller; before transferring control to the caller, the
destructors for the members and bases are called. Destructors for
elements of an array are called in reverse order of their construction
(see  [[class.init]]).

A destructor can be declared `virtual` ([[class.virtual]]) or pure
`virtual` ([[class.abstract]]); if any objects of that class or any
derived class are created in the program, the destructor shall be
defined. If a class has a base class with a virtual destructor, its
destructor (whether user- or implicitly-declared) is virtual.

[*Note 2*:  Some language constructs have special semantics when used
during destruction; see  [[class.cdtor]]. — *end note*]

A destructor is invoked implicitly

- for a constructed object with static storage duration (
  [[basic.stc.static]]) at program termination ([[basic.start.term]]),
- for a constructed object with thread storage duration (
  [[basic.stc.thread]]) at thread exit,
- for a constructed object with automatic storage duration (
  [[basic.stc.auto]]) when the block in which an object is created
  exits ([[stmt.dcl]]),
- for a constructed temporary object when its lifetime ends (
  [[conv.rval]], [[class.temporary]]).

In each case, the context of the invocation is the context of the
construction of the object. A destructor is also invoked implicitly
through use of a *delete-expression* ([[expr.delete]]) for a
constructed object allocated by a *new-expression* ([[expr.new]]); the
context of the invocation is the *delete-expression*.

[*Note 3*: An array of class type contains several subobjects for each
of which the destructor is invoked. — *end note*]

A destructor can also be invoked explicitly. A destructor is
*potentially invoked* if it is invoked or as specified in  [[expr.new]],
[[class.base.init]], and  [[except.throw]]. A program is ill-formed if a
destructor that is potentially invoked is deleted or not accessible from
the context of the invocation.

At the point of definition of a virtual destructor (including an
implicit definition ([[class.copy]])), the non-array deallocation
function is determined as if for the expression `delete this` appearing
in a non-virtual destructor of the destructor’s class (see 
[[expr.delete]]). If the lookup fails or if the deallocation function
has a deleted definition ([[dcl.fct.def]]), the program is ill-formed.

[*Note 4*: This assures that a deallocation function corresponding to
the dynamic type of an object is available for the *delete-expression* (
[[class.free]]). — *end note*]

In an explicit destructor call, the destructor is specified by a `~`
followed by a *type-name* or *decltype-specifier* that denotes the
destructor’s class type. The invocation of a destructor is subject to
the usual rules for member functions ([[class.mfct]]); that is, if the
object is not of the destructor’s class type and not of a class derived
from the destructor’s class type (including when the destructor is
invoked via a null pointer value), the program has undefined behavior.

[*Note 5*: Invoking `delete` on a null pointer does not call the
destructor; see [[expr.delete]]. — *end note*]

[*Example 1*:

``` cpp
struct B {
  virtual ~B() { }
};
struct D : B {
  ~D() { }
};

D D_object;
typedef B B_alias;
B* B_ptr = &D_object;

void f() {
  D_object.B::~B();             // calls B's destructor
  B_ptr->~B();                  // calls D's destructor
  B_ptr->~B_alias();            // calls D's destructor
  B_ptr->B_alias::~B();         // calls B's destructor
  B_ptr->B_alias::~B_alias();   // calls B's destructor
}
```

— *end example*]

[*Note 6*: An explicit destructor call must always be written using a
member access operator ([[expr.ref]]) or a *qualified-id* (
[[expr.prim]]); in particular, the *unary-expression* `~X()` in a member
function is not an explicit destructor call (
[[expr.unary.op]]). — *end note*]

[*Note 7*:

Explicit calls of destructors are rarely needed. One use of such calls
is for objects placed at specific addresses using a placement
*new-expression*. Such use of explicit placement and destruction of
objects can be necessary to cope with dedicated hardware resources and
for writing memory management facilities. For example,

``` cpp
void* operator new(std::size_t, void* p) { return p; }
struct X {
  X(int);
  ~X();
};
void f(X* p);

void g() {                      // rare, specialized use:
  char* buf = new char[sizeof(X)];
  X* p = new(buf) X(222);       // use buf[] and initialize
  f(p);
  p->X::~X();                   // cleanup
}
```

— *end note*]

Once a destructor is invoked for an object, the object no longer exists;
the behavior is undefined if the destructor is invoked for an object
whose lifetime has ended ([[basic.life]]).

[*Example 2*: If the destructor for an automatic object is explicitly
invoked, and the block is subsequently left in a manner that would
ordinarily invoke implicit destruction of the object, the behavior is
undefined. — *end example*]

[*Note 8*:

The notation for explicit call of a destructor can be used for any
scalar type name ([[expr.pseudo]]). Allowing this makes it possible to
write code without having to know if a destructor exists for a given
type. For example:

``` cpp
typedef int I;
I* p;
p->I::~I();
```

— *end note*]

## Free store <a id="class.free">[[class.free]]</a>

Any allocation function for a class `T` is a static member (even if not
explicitly declared `static`).

[*Example 1*:

``` cpp
class Arena;
struct B {
  void* operator new(std::size_t, Arena*);
};
struct D1 : B {
};

Arena*  ap;
void foo(int i) {
  new (ap) D1;      // calls B::operator new(std::size_t, Arena*)
  new D1[i];        // calls ::operator new[](std::size_t)
  new D1;           // ill-formed: ::operator new(std::size_t) hidden
}
```

— *end example*]

When an object is deleted with a *delete-expression* ([[expr.delete]]),
a deallocation function (`operator delete()` for non-array objects or
`operator delete[]()` for arrays) is (implicitly) called to reclaim the
storage occupied by the object ([[basic.stc.dynamic.deallocation]]).

Class-specific deallocation function lookup is a part of general
deallocation function lookup ([[expr.delete]]) and occurs as follows.
If the *delete-expression* is used to deallocate a class object whose
static type has a virtual destructor, the deallocation function is the
one selected at the point of definition of the dynamic type’s virtual
destructor ([[class.dtor]]).[^3] Otherwise, if the *delete-expression*
is used to deallocate an object of class `T` or array thereof, the
static and dynamic types of the object shall be identical and the
deallocation function’s name is looked up in the scope of `T`. If this
lookup fails to find the name, general deallocation function lookup (
[[expr.delete]]) continues. If the result of the lookup is ambiguous or
inaccessible, or if the lookup selects a placement deallocation
function, the program is ill-formed.

Any deallocation function for a class `X` is a static member (even if
not explicitly declared `static`).

[*Example 2*:

``` cpp
class X {
  void operator delete(void*);
  void operator delete[](void*, std::size_t);
};

class Y {
  void operator delete(void*, std::size_t);
  void operator delete[](void*);
};
```

— *end example*]

Since member allocation and deallocation functions are `static` they
cannot be virtual.

[*Note 1*:

However, when the *cast-expression* of a *delete-expression* refers to
an object of class type, because the deallocation function actually
called is looked up in the scope of the class that is the dynamic type
of the object, if the destructor is virtual, the effect is the same. For
example,

``` cpp
struct B {
  virtual ~B();
  void operator delete(void*, std::size_t);
};

struct D : B {
  void operator delete(void*);
};

void f() {
  B* bp = new D;
  delete bp;        // 1: uses D::operator delete(void*)
}
```

Here, storage for the non-array object of class `D` is deallocated by
`D::operator delete()`, due to the virtual destructor.

— *end note*]

[*Note 2*:

Virtual destructors have no effect on the deallocation function actually
called when the *cast-expression* of a *delete-expression* refers to an
array of objects of class type. For example,

``` cpp
struct B {
  virtual ~B();
  void operator delete[](void*, std::size_t);
};

struct D : B {
  void operator delete[](void*, std::size_t);
};

void f(int i) {
  D* dp = new D[i];
  delete [] dp;     // uses D::operator delete[](void*, std::size_t)
  B* bp = new D[i];
  delete[] bp;      // undefined behavior
}
```

— *end note*]

Access to the deallocation function is checked statically. Hence, even
though a different one might actually be executed, the statically
visible deallocation function is required to be accessible.

[*Example 3*: For the call on line “// 1” above, if
`B::operator delete()` had been `private`, the delete expression would
have been ill-formed. — *end example*]

[*Note 3*: If a deallocation function has no explicit
*noexcept-specifier*, it has a non-throwing exception specification (
[[except.spec]]). — *end note*]

## Initialization <a id="class.init">[[class.init]]</a>

When no initializer is specified for an object of (possibly
cv-qualified) class type (or array thereof), or the initializer has the
form `()`, the object is initialized as specified in  [[dcl.init]].

An object of class type (or array thereof) can be explicitly
initialized; see  [[class.expl.init]] and  [[class.base.init]].

When an array of class objects is initialized (either explicitly or
implicitly) and the elements are initialized by constructor, the
constructor shall be called for each element of the array, following the
subscript order; see  [[dcl.array]].

[*Note 1*: Destructors for the array elements are called in reverse
order of their construction. — *end note*]

### Explicit initialization <a id="class.expl.init">[[class.expl.init]]</a>

An object of class type can be initialized with a parenthesized
*expression-list*, where the *expression-list* is construed as an
argument list for a constructor that is called to initialize the object.
Alternatively, a single *assignment-expression* can be specified as an
*initializer* using the `=` form of initialization. Either
direct-initialization semantics or copy-initialization semantics apply;
see  [[dcl.init]].

[*Example 1*:

``` cpp
struct complex {
  complex();
  complex(double);
  complex(double,double);
};

complex sqrt(complex,complex);

complex a(1);                   // initialize by a call of complex(double)
complex b = a;                  // initialize by a copy of a
complex c = complex(1,2);       // construct complex(1,2) using complex(double,double),
                                // copy/move it into c
complex d = sqrt(b,c);          // call sqrt(complex,complex) and copy/move the result into d
complex e;                      // initialize by a call of complex()
complex f = 3;                  // construct complex(3) using complex(double), copy/move it into f
complex g = { 1, 2 };           // initialize by a call of complex(double, double)
```

— *end example*]

[*Note 1*:  Overloading of the assignment operator ([[over.ass]]) has
no effect on initialization. — *end note*]

An object of class type can also be initialized by a *braced-init-list*.
List-initialization semantics apply; see  [[dcl.init]] and 
[[dcl.init.list]].

[*Example 2*:

``` cpp
complex v[6] = { 1, complex(1,2), complex(), 2 };
```

Here, `complex::complex(double)` is called for the initialization of
`v[0]` and `v[3]`, `complex::complex({}double, double)` is called for
the initialization of `v[1]`, `complex::complex()` is called for the
initialization `v[2]`, `v[4]`, and `v[5]`. For another example,

``` cpp
struct X {
  int i;
  float f;
  complex c;
} x = { 99, 88.8, 77.7 };
```

Here, `x.i` is initialized with 99, `x.f` is initialized with 88.8, and
`complex::complex(double)` is called for the initialization of `x.c`.

— *end example*]

[*Note 2*: Braces can be elided in the *initializer-list* for any
aggregate, even if the aggregate has members of a class type with
user-defined type conversions; see  [[dcl.init.aggr]]. — *end note*]

[*Note 3*: If `T` is a class type with no default constructor, any
declaration of an object of type `T` (or array thereof) is ill-formed if
no *initializer* is explicitly specified (see  [[class.init]] and 
[[dcl.init]]). — *end note*]

[*Note 4*:  The order in which objects with static or thread storage
duration are initialized is described in  [[basic.start.dynamic]] and 
[[stmt.dcl]]. — *end note*]

### Initializing bases and members <a id="class.base.init">[[class.base.init]]</a>

In the definition of a constructor for a class, initializers for direct
and virtual base class subobjects and non-static data members can be
specified by a *ctor-initializer*, which has the form

``` bnf
ctor-initializer:
    ':' mem-initializer-list
```

``` bnf
mem-initializer-list:
    mem-initializer '...'\opt
    mem-initializer-list ',' mem-initializer '...'\opt
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

In a *mem-initializer-id* an initial unqualified *identifier* is looked
up in the scope of the constructor’s class and, if not found in that
scope, it is looked up in the scope containing the constructor’s
definition.

[*Note 1*: If the constructor’s class contains a member with the same
name as a direct or virtual base class of the class, a
*mem-initializer-id* naming the member or base class and composed of a
single identifier refers to the class member. A *mem-initializer-id* for
the hidden base class may be specified using a qualified
name. — *end note*]

Unless the *mem-initializer-id* names the constructor’s class, a
non-static data member of the constructor’s class, or a direct or
virtual base of that class, the *mem-initializer* is ill-formed.

A *mem-initializer-list* can initialize a base class using any
*class-or-decltype* that denotes that base class type.

[*Example 1*:

``` cpp
struct A { A(); };
typedef A global_A;
struct B { };
struct C: public A, public B { C(); };
C::C(): global_A() { }          // mem-initializer for base A
```

— *end example*]

If a *mem-initializer-id* is ambiguous because it designates both a
direct non-virtual base class and an inherited virtual base class, the
*mem-initializer* is ill-formed.

[*Example 2*:

``` cpp
struct A { A(); };
struct B: public virtual A { };
struct C: public A, public B { C(); };
C::C(): A() { }                 // ill-formed: which A?
```

— *end example*]

A *ctor-initializer* may initialize a variant member of the
constructor’s class. If a *ctor-initializer* specifies more than one
*mem-initializer* for the same member or for the same base class, the
*ctor-initializer* is ill-formed.

A *mem-initializer-list* can delegate to another constructor of the
constructor’s class using any *class-or-decltype* that denotes the
constructor’s class itself. If a *mem-initializer-id* designates the
constructor’s class, it shall be the only *mem-initializer*; the
constructor is a *delegating constructor*, and the constructor selected
by the *mem-initializer* is the *target constructor*. The target
constructor is selected by overload resolution. Once the target
constructor returns, the body of the delegating constructor is executed.
If a constructor delegates to itself directly or indirectly, the program
is ill-formed, no diagnostic required.

[*Example 3*:

``` cpp
struct C {
  C( int ) { }                  // #1: non-delegating constructor
  C(): C(42) { }                // #2: delegates to #1
  C( char c ) : C(42.0) { }     // #3: ill-formed due to recursion with #4
  C( double d ) : C('a') { }    // #4: ill-formed due to recursion with #3
};
```

— *end example*]

The *expression-list* or *braced-init-list* in a *mem-initializer* is
used to initialize the designated subobject (or, in the case of a
delegating constructor, the complete class object) according to the
initialization rules of  [[dcl.init]] for direct-initialization.

[*Example 4*:

``` cpp
struct B1 { B1(int); ... };
struct B2 { B2(int); ... };
struct D : B1, B2 {
  D(int);
  B1 b;
  const int c;
};

D::D(int a) : B2(a+1), B1(a+2), c(a+3), b(a+4) { ... }
D d(10);
```

— *end example*]

[*Note 2*: The initialization performed by each *mem-initializer*
constitutes a full-expression ([[intro.execution]]). Any expression in
a *mem-initializer* is evaluated as part of the full-expression that
performs the initialization. — *end note*]

A *mem-initializer* where the *mem-initializer-id* denotes a virtual
base class is ignored during execution of a constructor of any class
that is not the most derived class.

A temporary expression bound to a reference member in a
*mem-initializer* is ill-formed.

[*Example 5*:

``` cpp
struct A {
  A() : v(42) { }   // error
  const int& v;
};
```

— *end example*]

In a non-delegating constructor, if a given potentially constructed
subobject is not designated by a *mem-initializer-id* (including the
case where there is no *mem-initializer-list* because the constructor
has no *ctor-initializer*), then

- if the entity is a non-static data member that has a default member
  initializer ([[class.mem]]) and either
  - the constructor’s class is a union ([[class.union]]), and no other
    variant member of that union is designated by a *mem-initializer-id*
    or
  - the constructor’s class is not a union, and, if the entity is a
    member of an anonymous union, no other member of that union is
    designated by a *mem-initializer-id*,

  the entity is initialized from its default member initializer as
  specified in  [[dcl.init]];
- otherwise, if the entity is an anonymous union or a variant member (
  [[class.union.anon]]), no initialization is performed;
- otherwise, the entity is default-initialized ([[dcl.init]]).

[*Note 3*: An abstract class ([[class.abstract]]) is never a most
derived class, thus its constructors never initialize virtual base
classes, therefore the corresponding *mem-initializer*s may be
omitted. — *end note*]

An attempt to initialize more than one non-static data member of a union
renders the program ill-formed.

[*Note 4*: After the call to a constructor for class `X` for an object
with automatic or dynamic storage duration has completed, if the
constructor was not invoked as part of value-initialization and a member
of `X` is neither initialized nor given a value during execution of the
*compound-statement* of the body of the constructor, the member has an
indeterminate value. — *end note*]

[*Example 6*:

``` cpp
struct A {
  A();
};

struct B {
  B(int);
};

struct C {
  C() { }               // initializes members as follows:
  A a;                  // OK: calls A::A()
  const B b;            // error: B has no default constructor
  int i;                // OK: i has indeterminate value
  int j = 5;            // OK: j has the value 5
};
```

— *end example*]

If a given non-static data member has both a default member initializer
and a *mem-initializer*, the initialization specified by the
*mem-initializer* is performed, and the non-static data member’s default
member initializer is ignored.

[*Example 7*:

Given

``` cpp
struct A {
  int i = /* some integer expression with side effects */ ;
  A(int arg) : i(arg) { }
  // ...
};
```

the `A(int)` constructor will simply initialize `i` to the value of
`arg`, and the side effects in `i`’s default member initializer will not
take place.

— *end example*]

A temporary expression bound to a reference member from a default member
initializer is ill-formed.

[*Example 8*:

``` cpp
struct A {
  A() = default;        // OK
  A(int v) : v(v) { }   // OK
  const int& v = 42;    // OK
};
A a1;                   // error: ill-formed binding of temporary to reference
A a2(1);                // OK, unfortunately
```

— *end example*]

In a non-delegating constructor, the destructor for each potentially
constructed subobject of class type is potentially invoked (
[[class.dtor]]).

[*Note 5*: This provision ensures that destructors can be called for
fully-constructed subobjects in case an exception is thrown (
[[except.ctor]]). — *end note*]

In a non-delegating constructor, initialization proceeds in the
following order:

- First, and only for the constructor of the most derived class (
  [[intro.object]]), virtual base classes are initialized in the order
  they appear on a depth-first left-to-right traversal of the directed
  acyclic graph of base classes, where “left-to-right” is the order of
  appearance of the base classes in the derived class
  *base-specifier-list*.
- Then, direct base classes are initialized in declaration order as they
  appear in the *base-specifier-list* (regardless of the order of the
  *mem-initializer*s).
- Then, non-static data members are initialized in the order they were
  declared in the class definition (again regardless of the order of the
  *mem-initializer*s).
- Finally, the *compound-statement* of the constructor body is executed.

[*Note 6*: The declaration order is mandated to ensure that base and
member subobjects are destroyed in the reverse order of
initialization. — *end note*]

[*Example 9*:

``` cpp
struct V {
  V();
  V(int);
};

struct A : virtual V {
  A();
  A(int);
};

struct B : virtual V {
  B();
  B(int);
};

struct C : A, B, virtual V {
  C();
  C(int);
};

A::A(int i) : V(i) { ... }
B::B(int i) { ... }
C::C(int i) { ... }

V v(1);             // use V(int)
A a(2);             // use V(int)
B b(3);             // use V()
C c(4);             // use V()
```

— *end example*]

Names in the *expression-list* or *braced-init-list* of a
*mem-initializer* are evaluated in the scope of the constructor for
which the *mem-initializer* is specified.

[*Example 10*:

``` cpp
class X {
  int a;
  int b;
  int i;
  int j;
public:
  const int& r;
  X(int i): r(a), b(i), i(i), j(this->i) { }
};
```

initializes `X::r` to refer to `X::a`, initializes `X::b` with the value
of the constructor parameter `i`, initializes `X::i` with the value of
the constructor parameter `i`, and initializes `X::j` with the value of
`X::i`; this takes place each time an object of class `X` is created.

— *end example*]

[*Note 7*: Because the *mem-initializer* are evaluated in the scope of
the constructor, the `this` pointer can be used in the *expression-list*
of a *mem-initializer* to refer to the object being
initialized. — *end note*]

Member functions (including virtual member functions, [[class.virtual]])
can be called for an object under construction. Similarly, an object
under construction can be the operand of the `typeid` operator (
[[expr.typeid]]) or of a `dynamic_cast` ([[expr.dynamic.cast]]).
However, if these operations are performed in a *ctor-initializer* (or
in a function called directly or indirectly from a *ctor-initializer*)
before all the *mem-initializer*s for base classes have completed, the
program has undefined behavior.

[*Example 11*:

``` cpp
class A {
public:
  A(int);
};

class B : public A {
  int j;
public:
  int f();
  B() : A(f()),     // undefined: calls member function but base A not yet initialized
  j(f()) { }        // well-defined: bases are all initialized
};

class C {
public:
  C(int);
};

class D : public B, C {
  int i;
public:
  D() : C(f()),     // undefined: calls member function but base C not yet initialized
  i(f()) { }        // well-defined: bases are all initialized
};
```

— *end example*]

[*Note 8*:  [[class.cdtor]] describes the result of virtual function
calls, `typeid` and `dynamic_cast`s during construction for the
well-defined cases; that is, describes the *polymorphic behavior* of an
object under construction. — *end note*]

A *mem-initializer* followed by an ellipsis is a pack expansion (
[[temp.variadic]]) that initializes the base classes specified by a pack
expansion in the *base-specifier-list* for the class.

[*Example 12*:

``` cpp
template<class... Mixins>
class X : public Mixins... {
public:
  X(const Mixins&... mixins) : Mixins(mixins)... { }
};
```

— *end example*]

### Initialization by inherited constructor <a id="class.inhctor.init">[[class.inhctor.init]]</a>

When a constructor for type `B` is invoked to initialize an object of a
different type `D` (that is, when the constructor was inherited (
[[namespace.udecl]])), initialization proceeds as if a defaulted default
constructor were used to initialize the `D` object and each base class
subobject from which the constructor was inherited, except that the `B`
subobject is initialized by the invocation of the inherited constructor.
The complete initialization is considered to be a single function call;
in particular, the initialization of the inherited constructor’s
parameters is sequenced before the initialization of any part of the `D`
object.

[*Example 1*:

``` cpp
struct B1 {
  B1(int, ...) { }
};

struct B2 {
  B2(double) { }
};

int get();

struct D1 : B1 {
  using B1::B1;     // inherits B1(int, ...)
  int x;
  int y = get();
};

void test() {
  D1 d(2, 3, 4);    // OK: B1 is initialized by calling B1(2, 3, 4),
                    // then d.x is default-initialized (no initialization is performed),
                    // then d.y is initialized by calling get()
  D1 e;             // error: D1 has a deleted default constructor
}

struct D2 : B2 {
  using B2::B2;
  B1 b;
};

D2 f(1.0);          // error: B1 has a deleted default constructor

struct W { W(int); };
struct X : virtual W { using W::W; X() = delete; };
struct Y : X { using X::X; };
struct Z : Y, virtual W { using Y::Y; };
Z z(0);             // OK: initialization of Y does not invoke default constructor of X

template<class T> struct Log : T {
  using T::T;       // inherits all constructors from class T
  ~Log() { std::clog << "Destroying wrapper" << std::endl; }
};
```

Class template `Log` wraps any class and forwards all of its
constructors, while writing a message to the standard log whenever an
object of class `Log` is destroyed.

— *end example*]

If the constructor was inherited from multiple base class subobjects of
type `B`, the program is ill-formed.

[*Example 2*:

``` cpp
struct A { A(int); };
struct B : A { using A::A; };

struct C1 : B { using B::B; };
struct C2 : B { using B::B; };

struct D1 : C1, C2 {
  using C1::C1;
  using C2::C2;
};

struct V1 : virtual B { using B::B; };
struct V2 : virtual B { using B::B; };

struct D2 : V1, V2 {
  using V1::V1;
  using V2::V2;
};

D1 d1(0);           // ill-formed: ambiguous
D2 d2(0);           // OK: initializes virtual B base class, which initializes the A base class
                    // then initializes the V1 and V2 base classes as if by a defaulted default constructor

struct M { M(); M(int); };
struct N : M { using M::M; };
struct O : M {};
struct P : N, O { using N::N; using O::O; };
P p(0);             // OK: use M(0) to initialize N's base class,
                    // use M() to initialize O's base class
```

— *end example*]

When an object is initialized by an inherited constructor,
initialization of the object is complete when the initialization of all
subobjects is complete.

## Construction and destruction <a id="class.cdtor">[[class.cdtor]]</a>

For an object with a non-trivial constructor, referring to any
non-static member or base class of the object before the constructor
begins execution results in undefined behavior. For an object with a
non-trivial destructor, referring to any non-static member or base class
of the object after the destructor finishes execution results in
undefined behavior.

[*Example 1*:

``` cpp
struct X { int i; };
struct Y : X { Y(); };                  // non-trivial
struct A { int a; };
struct B : public A { int j; Y y; };    // non-trivial

extern B bobj;
B* pb = &bobj;                          // OK
int* p1 = &bobj.a;                      // undefined, refers to base class member
int* p2 = &bobj.y.i;                    // undefined, refers to member's member

A* pa = &bobj;                          // undefined, upcast to a base class type
B bobj;                                 // definition of bobj

extern X xobj;
int* p3 = &xobj.i;                      // OK, X is a trivial class
X xobj;
```

For another example,

``` cpp
struct W { int j; };
struct X : public virtual W { };
struct Y {
  int* p;
  X x;
  Y() : p(&x.j) {   // undefined, x is not yet constructed
    }
};
```

— *end example*]

To explicitly or implicitly convert a pointer (a glvalue) referring to
an object of class `X` to a pointer (reference) to a direct or indirect
base class `B` of `X`, the construction of `X` and the construction of
all of its direct or indirect bases that directly or indirectly derive
from `B` shall have started and the destruction of these classes shall
not have completed, otherwise the conversion results in undefined
behavior. To form a pointer to (or access the value of) a direct
non-static member of an object `obj`, the construction of `obj` shall
have started and its destruction shall not have completed, otherwise the
computation of the pointer value (or accessing the member value) results
in undefined behavior.

[*Example 2*:

``` cpp
struct A { };
struct B : virtual A { };
struct C : B { };
struct D : virtual A { D(A*); };
struct X { X(A*); };

struct E : C, D, X {
  E() : D(this),    // undefined: upcast from E* to A* might use path E* → D* → A*
                    // but D is not constructed

                    // ``D((C*)this)'' would be defined: E* → C* is defined because E() has started,
                    // and C* → A* is defined because C is fully constructed

  X(this) {}        // defined: upon construction of X, C/B/D/A sublattice is fully constructed
};
```

— *end example*]

Member functions, including virtual functions ([[class.virtual]]), can
be called during construction or destruction ([[class.base.init]]).
When a virtual function is called directly or indirectly from a
constructor or from a destructor, including during the construction or
destruction of the class’s non-static data members, and the object to
which the call applies is the object (call it `x`) under construction or
destruction, the function called is the final overrider in the
constructor’s or destructor’s class and not one overriding it in a
more-derived class. If the virtual function call uses an explicit class
member access ([[expr.ref]]) and the object expression refers to the
complete object of `x` or one of that object’s base class subobjects but
not `x` or one of its base class subobjects, the behavior is undefined.

[*Example 3*:

``` cpp
struct V {
  virtual void f();
  virtual void g();
};

struct A : virtual V {
  virtual void f();
};

struct B : virtual V {
  virtual void g();
  B(V*, A*);
};

struct D : A, B {
  virtual void f();
  virtual void g();
  D() : B((A*)this, this) { }
};

B::B(V* v, A* a) {
  f();              // calls V::f, not A::f
  g();              // calls B::g, not D::g
  v->g();           // v is base of B, the call is well-defined, calls B::g
  a->f();           // undefined behavior, a's type not a base of B
}
```

— *end example*]

The `typeid` operator ([[expr.typeid]]) can be used during construction
or destruction ([[class.base.init]]). When `typeid` is used in a
constructor (including the *mem-initializer* or default member
initializer ([[class.mem]]) for a non-static data member) or in a
destructor, or used in a function called (directly or indirectly) from a
constructor or destructor, if the operand of `typeid` refers to the
object under construction or destruction, `typeid` yields the
`std::type_info` object representing the constructor or destructor’s
class. If the operand of `typeid` refers to the object under
construction or destruction and the static type of the operand is
neither the constructor or destructor’s class nor one of its bases, the
behavior is undefined.

`dynamic_cast`s ([[expr.dynamic.cast]]) can be used during construction
or destruction ([[class.base.init]]). When a `dynamic_cast` is used in
a constructor (including the *mem-initializer* or default member
initializer for a non-static data member) or in a destructor, or used in
a function called (directly or indirectly) from a constructor or
destructor, if the operand of the `dynamic_cast` refers to the object
under construction or destruction, this object is considered to be a
most derived object that has the type of the constructor or destructor’s
class. If the operand of the `dynamic_cast` refers to the object under
construction or destruction and the static type of the operand is not a
pointer to or object of the constructor or destructor’s own class or one
of its bases, the `dynamic_cast` results in undefined behavior.

[*Example 4*:

``` cpp
struct V {
  virtual void f();
};

struct A : virtual V { };

struct B : virtual V {
  B(V*, A*);
};

struct D : A, B {
  D() : B((A*)this, this) { }
};

B::B(V* v, A* a) {
  typeid(*this);                // type_info for B
  typeid(*v);                   // well-defined: *v has type V, a base of B yields type_info for B
  typeid(*a);                   // undefined behavior: type A not a base of B
  dynamic_cast<B*>(v);          // well-defined: v of type V*, V base of B results in B*
  dynamic_cast<B*>(a);          // undefined behavior, a has type A*, A not a base of B
}
```

— *end example*]

## Copying and moving class objects <a id="class.copy">[[class.copy]]</a>

A class object can be copied or moved in two ways: by initialization (
[[class.ctor]], [[dcl.init]]), including for function argument passing (
[[expr.call]]) and for function value return ([[stmt.return]]); and by
assignment ([[expr.ass]]). Conceptually, these two operations are
implemented by a copy/move constructor ([[class.ctor]]) and copy/move
assignment operator ([[over.ass]]).

A program is ill-formed if the copy/move constructor or the copy/move
assignment operator for an object is implicitly odr-used and the special
member function is not accessible (Clause  [[class.access]]).

[*Note 1*: Copying/moving one object into another using the copy/move
constructor or the copy/move assignment operator does not change the
layout or size of either object. — *end note*]

### Copy/move constructors <a id="class.copy.ctor">[[class.copy.ctor]]</a>

A non-template constructor for class `X` is a copy constructor if its
first parameter is of type `X&`, `const X&`, `volatile X&` or
`const volatile X&`, and either there are no other parameters or else
all other parameters have default arguments ([[dcl.fct.default]]).

[*Example 1*:

`X::X(const X&)`

and `X::X(X&,int=1)` are copy constructors.

``` cpp
struct X {
  X(int);
  X(const X&, int = 1);
};
X a(1);             // calls X(int);
X b(a, 0);          // calls X(const X&, int);
X c = b;            // calls X(const X&, int);
```

— *end example*]

A non-template constructor for class `X` is a move constructor if its
first parameter is of type `X&&`, `const X&&`, `volatile X&&`, or
`const volatile X&&`, and either there are no other parameters or else
all other parameters have default arguments ([[dcl.fct.default]]).

[*Example 2*:

`Y::Y(Y&&)` is a move constructor.

``` cpp
struct Y {
  Y(const Y&);
  Y(Y&&);
};
extern Y f(int);
Y d(f(1));          // calls Y(Y&&)
Y e = d;            // calls Y(const Y&)
```

— *end example*]

[*Note 1*:

All forms of copy/move constructor may be declared for a class.

[*Example 3*:

``` cpp
struct X {
  X(const X&);
  X(X&);            // OK
  X(X&&);
  X(const X&&);     // OK, but possibly not sensible
};
```

— *end example*]

— *end note*]

[*Note 2*:

If a class `X` only has a copy constructor with a parameter of type
`X&`, an initializer of type `const` `X` or `volatile` `X` cannot
initialize an object of type (possibly cv-qualified) `X`.

[*Example 4*:

``` cpp
struct X {
  X();              // default constructor
  X(X&);            // copy constructor with a non-const parameter
};
const X cx;
X x = cx;           // error: X::X(X&) cannot copy cx into x
```

— *end example*]

— *end note*]

A declaration of a constructor for a class `X` is ill-formed if its
first parameter is of type (optionally cv-qualified) `X` and either
there are no other parameters or else all other parameters have default
arguments. A member function template is never instantiated to produce
such a constructor signature.

[*Example 5*:

``` cpp
struct S {
  template<typename T> S(T);
  S();
};

S g;

void h() {
  S a(g);           // does not instantiate the member template to produce S::S<S>(S);
                    // uses the implicitly declared copy constructor
}
```

— *end example*]

If the class definition does not explicitly declare a copy constructor,
a non-explicit one is declared *implicitly*. If the class definition
declares a move constructor or move assignment operator, the implicitly
declared copy constructor is defined as deleted; otherwise, it is
defined as defaulted ([[dcl.fct.def]]). The latter case is deprecated
if the class has a user-declared copy assignment operator or a
user-declared destructor.

The implicitly-declared copy constructor for a class `X` will have the
form

``` cpp
X::X(const X&)
```

if each potentially constructed subobject of a class type `M` (or array
thereof) has a copy constructor whose first parameter is of type `const`
`M&` or `const` `volatile` `M&`.[^4] Otherwise, the implicitly-declared
copy constructor will have the form

``` cpp
X::X(X&)
```

If the definition of a class `X` does not explicitly declare a move
constructor, a non-explicit one will be implicitly declared as defaulted
if and only if

- `X` does not have a user-declared copy constructor,
- `X` does not have a user-declared copy assignment operator,
- `X` does not have a user-declared move assignment operator, and
- `X` does not have a user-declared destructor.

[*Note 3*: When the move constructor is not implicitly declared or
explicitly supplied, expressions that otherwise would have invoked the
move constructor may instead invoke a copy constructor. — *end note*]

The implicitly-declared move constructor for class `X` will have the
form

``` cpp
X::X(X&&)
```

An implicitly-declared copy/move constructor is an `inline` `public`
member of its class. A defaulted copy/move constructor for a class `X`
is defined as deleted ([[dcl.fct.def.delete]]) if `X` has:

- a variant member with a non-trivial corresponding constructor and `X`
  is a union-like class,
- a potentially constructed subobject type `M` (or array thereof) that
  cannot be copied/moved because overload resolution ([[over.match]]),
  as applied to find `M`’s corresponding constructor, results in an
  ambiguity or a function that is deleted or inaccessible from the
  defaulted constructor,
- any potentially constructed subobject of a type with a destructor that
  is deleted or inaccessible from the defaulted constructor, or,
- for the copy constructor, a non-static data member of rvalue reference
  type.

A defaulted move constructor that is defined as deleted is ignored by
overload resolution ([[over.match]], [[over.over]]).

[*Note 4*: A deleted move constructor would otherwise interfere with
initialization from an rvalue which can use the copy constructor
instead. — *end note*]

A copy/move constructor for class `X` is trivial if it is not
user-provided and if:

- class `X` has no virtual functions ([[class.virtual]]) and no virtual
  base classes ([[class.mi]]), and
- the constructor selected to copy/move each direct base class subobject
  is trivial, and
- for each non-static data member of `X` that is of class type (or array
  thereof), the constructor selected to copy/move that member is
  trivial;

otherwise the copy/move constructor is *non-trivial*.

A copy/move constructor that is defaulted and not defined as deleted is
*implicitly defined* if it is odr-used ([[basic.def.odr]]) or when it
is explicitly defaulted after its first declaration.

[*Note 5*: The copy/move constructor is implicitly defined even if the
implementation elided its odr-use ([[basic.def.odr]],
[[class.temporary]]). — *end note*]

If the implicitly-defined constructor would satisfy the requirements of
a constexpr constructor ([[dcl.constexpr]]), the implicitly-defined
constructor is `constexpr`.

Before the defaulted copy/move constructor for a class is implicitly
defined, all non-user-provided copy/move constructors for its
potentially constructed subobjects shall have been implicitly defined.

[*Note 6*: An implicitly-declared copy/move constructor has an implied
exception specification ([[except.spec]]). — *end note*]

The implicitly-defined copy/move constructor for a non-union class `X`
performs a memberwise copy/move of its bases and members.

[*Note 7*: Default member initializers of non-static data members are
ignored. See also the example in  [[class.base.init]]. — *end note*]

The order of initialization is the same as the order of initialization
of bases and members in a user-defined constructor (see 
[[class.base.init]]). Let `x` be either the parameter of the constructor
or, for the move constructor, an xvalue referring to the parameter. Each
base or non-static data member is copied/moved in the manner appropriate
to its type:

- if the member is an array, each element is direct-initialized with the
  corresponding subobject of `x`;
- if a member `m` has rvalue reference type `T&&`, it is
  direct-initialized with `static_cast<T&&>(x.m)`;
- otherwise, the base or member is direct-initialized with the
  corresponding base or member of `x`.

Virtual base class subobjects shall be initialized only once by the
implicitly-defined copy/move constructor (see  [[class.base.init]]).

The implicitly-defined copy/move constructor for a union `X` copies the
object representation ([[basic.types]]) of `X`.

### Copy/move assignment operator <a id="class.copy.assign">[[class.copy.assign]]</a>

A user-declared *copy* assignment operator `X::operator=` is a
non-static non-template member function of class `X` with exactly one
parameter of type `X`, `X&`, `const` `X&`, `volatile` `X&` or `const`
`volatile` `X&`.[^5]

[*Note 1*: An overloaded assignment operator must be declared to have
only one parameter; see  [[over.ass]]. — *end note*]

[*Note 2*: More than one form of copy assignment operator may be
declared for a class. — *end note*]

[*Note 3*:

If a class `X` only has a copy assignment operator with a parameter of
type `X&`, an expression of type const `X` cannot be assigned to an
object of type `X`.

[*Example 1*:

``` cpp
struct X {
  X();
  X& operator=(X&);
};
const X cx;
X x;
void f() {
  x = cx;           // error: X::operator=(X&) cannot assign cx into x
}
```

— *end example*]

— *end note*]

If the class definition does not explicitly declare a copy assignment
operator, one is declared *implicitly*. If the class definition declares
a move constructor or move assignment operator, the implicitly declared
copy assignment operator is defined as deleted; otherwise, it is defined
as defaulted ([[dcl.fct.def]]). The latter case is deprecated if the
class has a user-declared copy constructor or a user-declared
destructor. The implicitly-declared copy assignment operator for a class
`X` will have the form

``` cpp
X& X::operator=(const X&)
```

if

- each direct base class `B` of `X` has a copy assignment operator whose
  parameter is of type `const` `B&`, `const` `volatile` `B&` or `B`, and
- for all the non-static data members of `X` that are of a class type
  `M` (or array thereof), each such class type has a copy assignment
  operator whose parameter is of type `const` `M&`, `const` `volatile`
  `M&` or `M`.[^6]

Otherwise, the implicitly-declared copy assignment operator will have
the form

``` cpp
X& X::operator=(X&)
```

A user-declared move assignment operator `X::operator=` is a non-static
non-template member function of class `X` with exactly one parameter of
type `X&&`, `const X&&`, `volatile X&&`, or `const volatile X&&`.

[*Note 4*: An overloaded assignment operator must be declared to have
only one parameter; see  [[over.ass]]. — *end note*]

[*Note 5*: More than one form of move assignment operator may be
declared for a class. — *end note*]

If the definition of a class `X` does not explicitly declare a move
assignment operator, one will be implicitly declared as defaulted if and
only if

- `X` does not have a user-declared copy constructor,
- `X` does not have a user-declared move constructor,
- `X` does not have a user-declared copy assignment operator, and
- `X` does not have a user-declared destructor.

[*Example 2*:

The class definition

``` cpp
struct S {
  int a;
  S& operator=(const S&) = default;
};
```

will not have a default move assignment operator implicitly declared
because the copy assignment operator has been user-declared. The move
assignment operator may be explicitly defaulted.

``` cpp
struct S {
  int a;
  S& operator=(const S&) = default;
  S& operator=(S&&) = default;
};
```

— *end example*]

The implicitly-declared move assignment operator for a class `X` will
have the form

``` cpp
X& X::operator=(X&&);
```

The implicitly-declared copy/move assignment operator for class `X` has
the return type `X&`; it returns the object for which the assignment
operator is invoked, that is, the object assigned to. An
implicitly-declared copy/move assignment operator is an `inline`
`public` member of its class.

A defaulted copy/move assignment operator for class `X` is defined as
deleted if `X` has:

- a variant member with a non-trivial corresponding assignment operator
  and `X` is a union-like class, or
- a non-static data member of `const` non-class type (or array thereof),
  or
- a non-static data member of reference type, or
- a direct non-static data member of class type `M` (or array thereof)
  or a direct base class `M` that cannot be copied/moved because
  overload resolution ([[over.match]]), as applied to find `M`’s
  corresponding assignment operator, results in an ambiguity or a
  function that is deleted or inaccessible from the defaulted assignment
  operator.

A defaulted move assignment operator that is defined as deleted is
ignored by overload resolution ([[over.match]], [[over.over]]).

Because a copy/move assignment operator is implicitly declared for a
class if not declared by the user, a base class copy/move assignment
operator is always hidden by the corresponding assignment operator of a
derived class ([[over.ass]]). A *using-declaration* (
[[namespace.udecl]]) that brings in from a base class an assignment
operator with a parameter type that could be that of a copy/move
assignment operator for the derived class is not considered an explicit
declaration of such an operator and does not suppress the implicit
declaration of the derived class operator; the operator introduced by
the *using-declaration* is hidden by the implicitly-declared operator in
the derived class.

A copy/move assignment operator for class `X` is trivial if it is not
user-provided and if:

- class `X` has no virtual functions ([[class.virtual]]) and no virtual
  base classes ([[class.mi]]), and
- the assignment operator selected to copy/move each direct base class
  subobject is trivial, and
- for each non-static data member of `X` that is of class type (or array
  thereof), the assignment operator selected to copy/move that member is
  trivial;

otherwise the copy/move assignment operator is *non-trivial*.

A copy/move assignment operator for a class `X` that is defaulted and
not defined as deleted is *implicitly defined* when it is odr-used (
[[basic.def.odr]]) (e.g., when it is selected by overload resolution to
assign to an object of its class type) or when it is explicitly
defaulted after its first declaration. The implicitly-defined copy/move
assignment operator is `constexpr` if

- `X` is a literal type, and
- the assignment operator selected to copy/move each direct base class
  subobject is a constexpr function, and
- for each non-static data member of `X` that is of class type (or array
  thereof), the assignment operator selected to copy/move that member is
  a constexpr function.

Before the defaulted copy/move assignment operator for a class is
implicitly defined, all non-user-provided copy/move assignment operators
for its direct base classes and its non-static data members shall have
been implicitly defined.

[*Note 6*: An implicitly-declared copy/move assignment operator has an
implied exception specification ([[except.spec]]). — *end note*]

The implicitly-defined copy/move assignment operator for a non-union
class `X` performs memberwise copy/move assignment of its subobjects.
The direct base classes of `X` are assigned first, in the order of their
declaration in the *base-specifier-list*, and then the immediate
non-static data members of `X` are assigned, in the order in which they
were declared in the class definition. Let `x` be either the parameter
of the function or, for the move operator, an xvalue referring to the
parameter. Each subobject is assigned in the manner appropriate to its
type:

- if the subobject is of class type, as if by a call to `operator=` with
  the subobject as the object expression and the corresponding subobject
  of `x` as a single function argument (as if by explicit qualification;
  that is, ignoring any possible virtual overriding functions in more
  derived classes);
- if the subobject is an array, each element is assigned, in the manner
  appropriate to the element type;
- if the subobject is of scalar type, the built-in assignment operator
  is used.

It is unspecified whether subobjects representing virtual base classes
are assigned more than once by the implicitly-defined copy/move
assignment operator.

[*Example 3*:

``` cpp
struct V { };
struct A : virtual V { };
struct B : virtual V { };
struct C : B, A { };
```

It is unspecified whether the virtual base class subobject `V` is
assigned twice by the implicitly-defined copy/move assignment operator
for `C`.

— *end example*]

The implicitly-defined copy assignment operator for a union `X` copies
the object representation ([[basic.types]]) of `X`.

### Copy/move elision <a id="class.copy.elision">[[class.copy.elision]]</a>

When certain criteria are met, an implementation is allowed to omit the
copy/move construction of a class object, even if the constructor
selected for the copy/move operation and/or the destructor for the
object have side effects. In such cases, the implementation treats the
source and target of the omitted copy/move operation as simply two
different ways of referring to the same object. If the first parameter
of the selected constructor is an rvalue reference to the object’s type,
the destruction of that object occurs when the target would have been
destroyed; otherwise, the destruction occurs at the later of the times
when the two objects would have been destroyed without the
optimization.[^7] This elision of copy/move operations, called *copy
elision*, is permitted in the following circumstances (which may be
combined to eliminate multiple copies):

- in a `return` statement in a function with a class return type, when
  the *expression* is the name of a non-volatile automatic object (other
  than a function parameter or a variable introduced by the
  *exception-declaration* of a *handler* ([[except.handle]])) with the
  same type (ignoring cv-qualification) as the function return type, the
  copy/move operation can be omitted by constructing the automatic
  object directly into the function call’s return object
- in a *throw-expression* ([[expr.throw]]), when the operand is the
  name of a non-volatile automatic object (other than a function or
  catch-clause parameter) whose scope does not extend beyond the end of
  the innermost enclosing *try-block* (if there is one), the copy/move
  operation from the operand to the exception object ([[except.throw]])
  can be omitted by constructing the automatic object directly into the
  exception object
- when the *exception-declaration* of an exception handler (Clause 
  [[except]]) declares an object of the same type (except for
  cv-qualification) as the exception object ([[except.throw]]), the
  copy operation can be omitted by treating the *exception-declaration*
  as an alias for the exception object if the meaning of the program
  will be unchanged except for the execution of constructors and
  destructors for the object declared by the *exception-declaration*.
  \[*Note 3*: There cannot be a move from the exception object because
  it is always an lvalue. — *end note*]

Copy elision is required where an expression is evaluated in a context
requiring a constant expression ([[expr.const]]) and in constant
initialization ([[basic.start.static]]).

[*Note 1*: Copy elision might not be performed if the same expression
is evaluated in another context. — *end note*]

[*Example 1*:

``` cpp
class Thing {
public:
  Thing();
  ~Thing();
  Thing(const Thing&);
};

Thing f() {
  Thing t;
  return t;
}

Thing t2 = f();

struct A {
  void *p;
  constexpr A(): p(this) {}
};

constexpr A g() {
  A a;
  return a;
}

constexpr A a;          // well-formed, a.p points to a
constexpr A b = g();    // well-formed, b.p points to b

void g() {
  A c = g();            // well-formed, c.p may point to c or to an ephemeral temporary
}
```

Here the criteria for elision can eliminate the copying of the local
automatic object `t` into the result object for the function call `f()`,
which is the global object `t2`. Effectively, the construction of the
local object `t` can be viewed as directly initializing the global
object `t2`, and that object’s destruction will occur at program exit.
Adding a move constructor to `Thing` has the same effect, but it is the
move construction from the local automatic object to `t2` that is
elided.

— *end example*]

In the following copy-initialization contexts, a move operation might be
used instead of a copy operation:

- If the *expression* in a `return` statement ([[stmt.return]]) is a
  (possibly parenthesized) *id-expression* that names an object with
  automatic storage duration declared in the body or
  *parameter-declaration-clause* of the innermost enclosing function or
  *lambda-expression*, or
- if the operand of a *throw-expression* ([[expr.throw]]) is the name
  of a non-volatile automatic object (other than a function or
  catch-clause parameter) whose scope does not extend beyond the end of
  the innermost enclosing *try-block* (if there is one),

overload resolution to select the constructor for the copy is first
performed as if the object were designated by an rvalue. If the first
overload resolution fails or was not performed, or if the type of the
first parameter of the selected constructor is not an rvalue reference
to the object’s type (possibly cv-qualified), overload resolution is
performed again, considering the object as an lvalue.

[*Note 2*: This two-stage overload resolution must be performed
regardless of whether copy elision will occur. It determines the
constructor to be called if elision is not performed, and the selected
constructor must be accessible even if the call is
elided. — *end note*]

[*Example 2*:

``` cpp
class Thing {
public:
  Thing();
  ~Thing();
  Thing(Thing&&);
private:
  Thing(const Thing&);
};

Thing f(bool b) {
  Thing t;
  if (b)
    throw t;            // OK: Thing(Thing&&) used (or elided) to throw t
  return t;             // OK: Thing(Thing&&) used (or elided) to return t
}

Thing t2 = f(false);    // OK: no extra copy/move performed, t2 constructed by call to f

struct Weird {
  Weird();
  Weird(Weird&);
};

Weird g() {
  Weird w;
  return w;             // OK: first overload resolution fails, second overload resolution selects Weird(Weird&)
}
```

— *end example*]

<!-- Section link definitions -->
[class.base.init]: #class.base.init
[class.cdtor]: #class.cdtor
[class.conv]: #class.conv
[class.conv.ctor]: #class.conv.ctor
[class.conv.fct]: #class.conv.fct
[class.copy]: #class.copy
[class.copy.assign]: #class.copy.assign
[class.copy.ctor]: #class.copy.ctor
[class.copy.elision]: #class.copy.elision
[class.ctor]: #class.ctor
[class.dtor]: #class.dtor
[class.expl.init]: #class.expl.init
[class.free]: #class.free
[class.inhctor.init]: #class.inhctor.init
[class.init]: #class.init
[class.temporary]: #class.temporary
[special]: #special

<!-- Link reference definitions -->
[basic.def.odr]: basic.md#basic.def.odr
[basic.life]: basic.md#basic.life
[basic.lookup]: basic.md#basic.lookup
[basic.lval]: basic.md#basic.lval
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.static]: basic.md#basic.start.static
[basic.start.term]: basic.md#basic.start.term
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[basic.types]: basic.md#basic.types
[class]: class.md#class
[class.abstract]: class.md#class.abstract
[class.access]: class.md#class.access
[class.base.init]: #class.base.init
[class.cdtor]: #class.cdtor
[class.conv.fct]: #class.conv.fct
[class.copy]: #class.copy
[class.ctor]: #class.ctor
[class.dtor]: #class.dtor
[class.expl.init]: #class.expl.init
[class.free]: #class.free
[class.friend]: class.md#class.friend
[class.init]: #class.init
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.mi]: class.md#class.mi
[class.qual]: basic.md#class.qual
[class.temporary]: #class.temporary
[class.union]: class.md#class.union
[class.union.anon]: class.md#class.union.anon
[class.virtual]: class.md#class.virtual
[conv]: conv.md#conv
[conv.array]: conv.md#conv.array
[conv.rval]: conv.md#conv.rval
[dcl.array]: dcl.md#dcl.array
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.fct.spec]: dcl.md#dcl.fct.spec
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.type.cv]: dcl.md#dcl.type.cv
[diff.special]: compatibility.md#diff.special
[except]: except.md#except
[except.ctor]: except.md#except.ctor
[except.handle]: except.md#except.handle
[except.spec]: except.md#except.spec
[except.throw]: except.md#except.throw
[expr]: expr.md#expr
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.const]: expr.md#expr.const
[expr.const.cast]: expr.md#expr.const.cast
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.new]: expr.md#expr.new
[expr.prim]: expr.md#expr.prim
[expr.prim.lambda.capture]: expr.md#expr.prim.lambda.capture
[expr.pseudo]: expr.md#expr.pseudo
[expr.ref]: expr.md#expr.ref
[expr.sizeof]: expr.md#expr.sizeof
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.throw]: expr.md#expr.throw
[expr.type.conv]: expr.md#expr.type.conv
[expr.typeid]: expr.md#expr.typeid
[expr.unary.op]: expr.md#expr.unary.op
[intro.execution]: intro.md#intro.execution
[intro.object]: intro.md#intro.object
[namespace.udecl]: dcl.md#namespace.udecl
[over.ass]: over.md#over.ass
[over.best.ics]: over.md#over.best.ics
[over.ics.ref]: over.md#over.ics.ref
[over.match]: over.md#over.match
[over.match.best]: over.md#over.match.best
[over.match.copy]: over.md#over.match.copy
[over.over]: over.md#over.over
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.return]: stmt.md#stmt.return
[temp.dep.type]: temp.md#temp.dep.type
[temp.variadic]: temp.md#temp.variadic

[^1]: The same rules apply to initialization of an `initializer_list`
    object ([[dcl.init.list]]) with its underlying temporary array.

[^2]: These conversions are considered as standard conversions for the
    purposes of overload resolution ([[over.best.ics]],
    [[over.ics.ref]]) and therefore initialization ([[dcl.init]]) and
    explicit casts ([[expr.static.cast]]). A conversion to `void` does
    not invoke any conversion function ([[expr.static.cast]]). Even
    though never directly called to perform a conversion, such
    conversion functions can be declared and can potentially be reached
    through a call to a virtual conversion function in a base class.

[^3]: A similar provision is not needed for the array version of
    `operator` `delete` because  [[expr.delete]] requires that in this
    situation, the static type of the object to be deleted be the same
    as its dynamic type.

[^4]: This implies that the reference parameter of the
    implicitly-declared copy constructor cannot bind to a `volatile`
    lvalue; see  [[diff.special]].

[^5]: Because a template assignment operator or an assignment operator
    taking an rvalue reference parameter is never a copy assignment
    operator, the presence of such an assignment operator does not
    suppress the implicit declaration of a copy assignment operator.
    Such assignment operators participate in overload resolution with
    other assignment operators, including copy assignment operators,
    and, if selected, will be used to assign an object.

[^6]: This implies that the reference parameter of the
    implicitly-declared copy assignment operator cannot bind to a
    `volatile` lvalue; see  [[diff.special]].

[^7]: Because only one object is destroyed instead of two, and one
    copy/move constructor is not executed, there is still one object
    destroyed for each one constructed.
