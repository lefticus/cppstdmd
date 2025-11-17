# Classes <a id="class">[[class]]</a>

A class is a type. Its name becomes a *class-name* ([[class.name]])
within its scope.

``` bnf
class-name:
    identifier
    simple-template-id
```

*Class-specifier*s and *elaborated-type-specifier*s ([[dcl.type.elab]])
are used to make *class-name*s. An object of a class consists of a
(possibly empty) sequence of members and base class objects.

``` bnf
class-specifier:
    class-head \terminal{\ member-specificationₒₚₜ \terminal{\}}
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

A *class-specifier* whose *class-head* omits the *class-head-name*
defines an unnamed class.

[*Note 1*: An unnamed class thus can’t be `final`. — *end note*]

A *class-name* is inserted into the scope in which it is declared
immediately after the *class-name* is seen. The *class-name* is also
inserted into the scope of the class itself; this is known as the
*injected-class-name*. For purposes of access checking, the
injected-class-name is treated as if it were a public member name. A
*class-specifier* is commonly referred to as a class definition. A class
is considered defined after the closing brace of its *class-specifier*
has been seen even though its member functions are in general not yet
defined. The optional *attribute-specifier-seq* appertains to the class;
the attributes in the *attribute-specifier-seq* are thereafter
considered attributes of the class whenever it is named.

If a class is marked with the *class-virt-specifier* `final` and it
appears as a *class-or-decltype* in a *base-clause* (Clause 
[[class.derived]]), the program is ill-formed. Whenever a *class-key* is
followed by a *class-head-name*, the *identifier* `final`, and a colon
or left brace, `final` is interpreted as a *class-virt-specifier*.

[*Example 1*:

``` cpp
struct A;
struct A final {};      // OK: definition of struct A,
                        // not value-initialization of variable final

struct X {
 struct C { constexpr operator int() { return 5; } };
 struct B final : C{};  // OK: definition of nested class B,
                        // not declaration of a bit-field member final
};
```

— *end example*]

Complete objects and member subobjects of class type shall have nonzero
size.[^1]

[*Note 2*: Class objects can be assigned, passed as arguments to
functions, and returned by functions (except objects of classes for
which copying or moving has been restricted; see  [[class.copy]]). Other
plausible operators, such as equality comparison, can be defined by the
user; see  [[over.oper]]. — *end note*]

A *union* is a class defined with the *class-key* `union`; it holds at
most one data member at a time ([[class.union]]).

[*Note 3*: Aggregates of class type are described in 
[[dcl.init.aggr]]. — *end note*]

A *trivially copyable class* is a class:

- where each copy constructor, move constructor, copy assignment
  operator, and move assignment operator ([[class.copy]], [[over.ass]])
  is either deleted or trivial,
- that has at least one non-deleted copy constructor, move constructor,
  copy assignment operator, or move assignment operator, and
- that has a trivial, non-deleted destructor ([[class.dtor]]).

A *trivial class* is a class that is trivially copyable and has one or
more default constructors ([[class.ctor]]), all of which are either
trivial or deleted and at least one of which is not deleted.

[*Note 4*: In particular, a trivially copyable or trivial class does
not have virtual functions or virtual base classes. — *end note*]

A class `S` is a *standard-layout class* if it:

- has no non-static data members of type non-standard-layout class (or
  array of such types) or reference,
- has no virtual functions ([[class.virtual]]) and no virtual base
  classes ([[class.mi]]),
- has the same access control (Clause  [[class.access]]) for all
  non-static data members,
- has no non-standard-layout base classes,
- has at most one base class subobject of any given type,
- has all non-static data members and bit-fields in the class and its
  base classes first declared in the same class, and
- has no element of the set M(S) of types (defined below) as a base
  class.[^2]

M(X) is defined as follows:

- If `X` is a non-union class type with no (possibly inherited (Clause 
  [[class.derived]])) non-static data members, the set M(X) is empty.
- If `X` is a non-union class type whose first non-static data member
  has type X₀ (where said member may be an anonymous union), the set
  M(X) consists of X₀ and the elements of M(X₀).
- If `X` is a union type, the set M(X) is the union of all M(Uᵢ) and the
  set containing all Uᵢ, where each Uᵢ is the type of the ith non-static
  data member of `X`.
- If `X` is an array type with element type Xₑ, the set M(X) consists of
  Xₑ and the elements of M(Xₑ).
- If `X` is a non-class, non-array type, the set M(X) is empty.

[*Note 5*: M(X) is the set of the types of all non-base-class
subobjects that are guaranteed in a standard-layout class to be at a
zero offset in `X`. — *end note*]

[*Example 2*:

``` cpp
   struct B { int i; };         // standard-layout class
   struct C : B { };            // standard-layout class
   struct D : C { };            // standard-layout class
   struct E : D { char : 4; };  // not a standard-layout class

   struct Q {};
   struct S : Q { };
   struct T : Q { };
   struct U : S, T { };         // not a standard-layout class
```

— *end example*]

A *standard-layout struct* is a standard-layout class defined with the
*class-key* `struct` or the *class-key* `class`. A *standard-layout
union* is a standard-layout class defined with the *class-key* `union`.

[*Note 6*: Standard-layout classes are useful for communicating with
code written in other programming languages. Their layout is specified
in  [[class.mem]]. — *end note*]

A *POD struct*[^3] is a non-union class that is both a trivial class and
a standard-layout class, and has no non-static data members of type
non-POD struct, non-POD union (or array of such types). Similarly, a
*POD union* is a union that is both a trivial class and a
standard-layout class, and has no non-static data members of type
non-POD struct, non-POD union (or array of such types). A *POD class* is
a class that is either a POD struct or a POD union.

[*Example 3*:

``` cpp
struct N {          // neither trivial nor standard-layout
  int i;
  int j;
  virtual ~N();
};

struct T {          // trivial but not standard-layout
  int i;
private:
  int j;
};

struct SL {         // standard-layout but not trivial
  int i;
  int j;
  ~SL();
};

struct POD {        // both trivial and standard-layout
  int i;
  int j;
};
```

— *end example*]

If a *class-head-name* contains a *nested-name-specifier*, the
*class-specifier* shall refer to a class that was previously declared
directly in the class or namespace to which the *nested-name-specifier*
refers, or in an element of the inline namespace set (
[[namespace.def]]) of that namespace (i.e., not merely inherited or
introduced by a *using-declaration*), and the *class-specifier* shall
appear in a namespace enclosing the previous declaration. In such cases,
the *nested-name-specifier* of the *class-head-name* of the definition
shall not begin with a *decltype-specifier*.

## Class names <a id="class.name">[[class.name]]</a>

A class definition introduces a new type.

[*Example 1*:

``` cpp
struct X { int a; };
struct Y { int a; };
X a1;
Y a2;
int a3;
```

declares three variables of three different types. This implies that

``` cpp
a1 = a2;                        // error: Y assigned to X
a1 = a3;                        // error: int assigned to X
```

are type mismatches, and that

``` cpp
int f(X);
int f(Y);
```

declare an overloaded (Clause  [[over]]) function `f()` and not simply a
single function `f()` twice. For the same reason,

``` cpp
struct S { int a; };
struct S { int a; };            // error, double definition
```

is ill-formed because it defines `S` twice.

— *end example*]

A class declaration introduces the class name into the scope where it is
declared and hides any class, variable, function, or other declaration
of that name in an enclosing scope ([[basic.scope]]). If a class name
is declared in a scope where a variable, function, or enumerator of the
same name is also declared, then when both declarations are in scope,
the class can be referred to only using an *elaborated-type-specifier* (
[[basic.lookup.elab]]).

[*Example 2*:

``` cpp
struct stat {
  // ...
};

stat gstat;                     // use plain stat to define variable

int stat(struct stat*);         // redeclare stat as function

void f() {
  struct stat* ps;              // struct prefix needed to name struct stat
  stat(ps);                     // call stat()
}
```

— *end example*]

A *declaration* consisting solely of *class-key* *identifier*`;` is
either a redeclaration of the name in the current scope or a forward
declaration of the identifier as a class name. It introduces the class
name into the current scope.

[*Example 3*:

``` cpp
struct s { int a; };

void g() {
  struct s;                     // hide global struct s with a block-scope declaration
  s* p;                         // refer to local struct s
  struct s { char* p; };        // define local struct s
  struct s;                     // redeclaration, has no effect
}
```

— *end example*]

[*Note 1*:

Such declarations allow definition of classes that refer to each other.

[*Example 4*:

``` cpp
class Vector;

class Matrix {
  // ...
  friend Vector operator*(const Matrix&, const Vector&);
};

class Vector {
  // ...
  friend Vector operator*(const Matrix&, const Vector&);
};
```

Declaration of `friend`s is described in  [[class.friend]], operator
functions in  [[over.oper]].

— *end example*]

— *end note*]

[*Note 2*: An *elaborated-type-specifier* ([[dcl.type.elab]]) can also
be used as a *type-specifier* as part of a declaration. It differs from
a class declaration in that if a class of the elaborated name is in
scope the elaborated name will refer to it. — *end note*]

[*Example 5*:

``` cpp
struct s { int a; };

void g(int s) {
  struct s* p = new struct s;   // global s
  p->a = s;                     // parameter s
}
```

— *end example*]

[*Note 3*:

The declaration of a class name takes effect immediately after the
*identifier* is seen in the class definition or
*elaborated-type-specifier*. For example,

``` cpp
class A * A;
```

first specifies `A` to be the name of a class and then redefines it as
the name of a pointer to an object of that class. This means that the
elaborated form `class` `A` must be used to refer to the class. Such
artistry with names can be confusing and is best avoided.

— *end note*]

A *typedef-name* ([[dcl.typedef]]) that names a class type, or a
cv-qualified version thereof, is also a *class-name*. If a
*typedef-name* that names a cv-qualified class type is used where a
*class-name* is required, the cv-qualifiers are ignored. A
*typedef-name* shall not be used as the *identifier* in a *class-head*.

## Class members <a id="class.mem">[[class.mem]]</a>

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

The *member-specification* in a class definition declares the full set
of members of the class; no member can be added elsewhere. A *direct
member* of a class `X` is a member of `X` that was first declared within
the *member-specification* of `X`, including anonymous union objects (
[[class.union.anon]]) and direct members thereof. Members of a class are
data members, member functions ([[class.mfct]]), nested types,
enumerators, and member templates ([[temp.mem]]) and specializations
thereof.

[*Note 1*: A specialization of a static data member template is a
static data member. A specialization of a member function template is a
member function. A specialization of a member class template is a nested
class. — *end note*]

A *member-declaration* does not declare new members of the class if it
is

- a friend declaration ([[class.friend]]),
- a *static_assert-declaration*,
- a *using-declaration* ([[namespace.udecl]]), or
- an *empty-declaration*.

For any other *member-declaration*, each declared entity that is not an
unnamed bit-field ([[class.bit]]) is a member of the class, and each
such *member-declaration* shall either declare at least one member name
of the class or declare at least one unnamed bit-field.

A *data member* is a non-function member introduced by a
*member-declarator*. A *member function* is a member that is a function.
Nested types are classes ([[class.name]],  [[class.nest]]) and
enumerations ([[dcl.enum]]) declared in the class and arbitrary types
declared as members by use of a typedef declaration ([[dcl.typedef]])
or *alias-declaration*. The enumerators of an unscoped enumeration (
[[dcl.enum]]) defined in the class are members of the class.

A data member or member function may be declared `static` in its
*member-declaration*, in which case it is a *static member* (see 
[[class.static]]) (a *static data member* ([[class.static.data]]) or
*static member function* ([[class.static.mfct]]), respectively) of the
class. Any other data member or member function is a *non-static member*
(a *non-static data member* or *non-static member function* (
[[class.mfct.non-static]]), respectively).

[*Note 2*: A non-static data member of non-reference type is a member
subobject of a class object ([[intro.object]]). — *end note*]

A member shall not be declared twice in the *member-specification*,
except that

- a nested class or member class template can be declared and then later
  defined, and
- an enumeration can be introduced with an *opaque-enum-declaration* and
  later redeclared with an *enum-specifier*.

[*Note 3*: A single name can denote several member functions provided
their types are sufficiently different (Clause 
[[over]]). — *end note*]

A class is considered a completely-defined object type (
[[basic.types]]) (or complete type) at the closing `}` of the
*class-specifier*. Within the class *member-specification*, the class is
regarded as complete within function bodies, default arguments,
*noexcept-specifier*s, and default member initializers (including such
things in nested classes). Otherwise it is regarded as incomplete within
its own class *member-specification*.

In a *member-declarator*, an `=` immediately following the *declarator*
is interpreted as introducing a *pure-specifier* if the *declarator-id*
has function type, otherwise it is interpreted as introducing a
*brace-or-equal-initializer*.

[*Example 1*:

``` cpp
struct S {
  using T = void();
  T * p = 0;        // OK: brace-or-equal-initializer
  virtual T f = 0;  // OK: pure-specifier
};
```

— *end example*]

A *brace-or-equal-initializer* shall appear only in the declaration of a
data member. (For static data members, see  [[class.static.data]]; for
non-static data members, see  [[class.base.init]] and 
[[dcl.init.aggr]]). A *brace-or-equal-initializer* for a non-static data
member specifies a *default member initializer* for the member, and
shall not directly or indirectly cause the implicit definition of a
defaulted default constructor for the enclosing class or the exception
specification of that constructor.

A member shall not be declared with the `extern`
*storage-class-specifier*. Within a class definition, a member shall not
be declared with the `thread_local` *storage-class-specifier* unless
also declared `static`.

The *decl-specifier-seq* may be omitted in constructor, destructor, and
conversion function declarations only; when declaring another kind of
member the *decl-specifier-seq* shall contain a *type-specifier* that is
not a *cv-qualifier*. The *member-declarator-list* can be omitted only
after a *class-specifier* or an *enum-specifier* or in a `friend`
declaration ([[class.friend]]). A *pure-specifier* shall be used only
in the declaration of a virtual function ([[class.virtual]]) that is
not a `friend` declaration.

The optional *attribute-specifier-seq* in a *member-declaration*
appertains to each of the entities declared by the *member-declarator*s;
it shall not appear if the optional *member-declarator-list* is omitted.

A *virt-specifier-seq* shall contain at most one of each
*virt-specifier*. A *virt-specifier-seq* shall appear only in the
declaration of a virtual member function ([[class.virtual]]).

Non-static data members shall not have incomplete types. In particular,
a class `C` shall not contain a non-static member of class `C`, but it
can contain a pointer or reference to an object of class `C`.

[*Note 4*: See  [[expr.prim]] for restrictions on the use of non-static
data members and non-static member functions. — *end note*]

[*Note 5*: The type of a non-static member function is an ordinary
function type, and the type of a non-static data member is an ordinary
object type. There are no special member function types or data member
types. — *end note*]

[*Example 2*:

A simple example of a class definition is

``` cpp
struct tnode {
  char tword[20];
  int count;
  tnode* left;
  tnode* right;
};
```

which contains an array of twenty characters, an integer, and two
pointers to objects of the same type. Once this definition has been
given, the declaration

``` cpp
tnode s, *sp;
```

declares `s` to be a `tnode` and `sp` to be a pointer to a `tnode`. With
these declarations, `sp->count` refers to the `count` member of the
object to which `sp` points; `s.left` refers to the `left` subtree
pointer of the object `s`; and `s.right->tword[0]` refers to the initial
character of the `tword` member of the `right` subtree of `s`.

— *end example*]

Non-static data members of a (non-union) class with the same access
control (Clause  [[class.access]]) are allocated so that later members
have higher addresses within a class object. The order of allocation of
non-static data members with different access control is unspecified
(Clause  [[class.access]]). Implementation alignment requirements might
cause two adjacent members not to be allocated immediately after each
other; so might requirements for space for managing virtual functions (
[[class.virtual]]) and virtual base classes ([[class.mi]]).

If `T` is the name of a class, then each of the following shall have a
name different from `T`:

- every static data member of class `T`;
- every member function of class `T` \[*Note 1*: This restriction does
  not apply to constructors, which do not have names (
  [[class.ctor]]) — *end note*] ;
- every member of class `T` that is itself a type;
- every member template of class `T`;
- every enumerator of every member of class `T` that is an unscoped
  enumerated type; and
- every member of every anonymous union that is a member of class `T`.

In addition, if class `T` has a user-declared constructor (
[[class.ctor]]), every non-static data member of class `T` shall have a
name different from `T`.

The *common initial sequence* of two standard-layout struct (Clause 
[[class]]) types is the longest sequence of non-static data members and
bit-fields in declaration order, starting with the first such entity in
each of the structs, such that corresponding entities have
layout-compatible types and either neither entity is a bit-field or both
are bit-fields with the same width.

[*Example 3*:

``` cpp
  struct A { int a; char b; };
  struct B { const int b1; volatile char b2; };
  struct C { int c; unsigned : 0; char b; };
  struct D { int d; char b : 4; };
  struct E { unsigned int e; char b; };
```

The common initial sequence of `A` and `B` comprises all members of
either class. The common initial sequence of `A` and `C` and of `A` and
`D` comprises the first member in each case. The common initial sequence
of `A` and `E` is empty.

— *end example*]

Two standard-layout struct (Clause  [[class]]) types are
*layout-compatible classes* if their common initial sequence comprises
all members and bit-fields of both classes ([[basic.types]]).

Two standard-layout unions are layout-compatible if they have the same
number of non-static data members and corresponding non-static data
members (in any order) have layout-compatible types ([[basic.types]]).

In a standard-layout union with an active member ([[class.union]]) of
struct type `T1`, it is permitted to read a non-static data member `m`
of another union member of struct type `T2` provided `m` is part of the
common initial sequence of `T1` and `T2`; the behavior is as if the
corresponding member of `T1` were nominated.

[*Example 4*:

``` cpp
struct T1 { int a, b; };
struct T2 { int c; double d; };
union U { T1 t1; T2 t2; };
int f() {
  U u = { { 1, 2 } };   // active member is t1
  return u.t2.c;        // OK, as if u.t1.a were nominated
}
```

— *end example*]

[*Note 6*: Reading a volatile object through a non-volatile glvalue has
undefined behavior ([[dcl.type.cv]]). — *end note*]

If a standard-layout class object has any non-static data members, its
address is the same as the address of its first non-static data member.
Otherwise, its address is the same as the address of its first base
class subobject (if any).

[*Note 7*: There might therefore be unnamed padding within a
standard-layout struct object, but not at its beginning, as necessary to
achieve appropriate alignment. — *end note*]

[*Note 8*: The object and its first subobject are
pointer-interconvertible ([[basic.compound]],
[[expr.static.cast]]). — *end note*]

### Member functions <a id="class.mfct">[[class.mfct]]</a>

A member function may be defined ([[dcl.fct.def]]) in its class
definition, in which case it is an *inline* member function (
[[dcl.inline]]), or it may be defined outside of its class definition if
it has already been declared but not defined in its class definition. A
member function definition that appears outside of the class definition
shall appear in a namespace scope enclosing the class definition. Except
for member function definitions that appear outside of a class
definition, and except for explicit specializations of member functions
of class templates and member function templates ([[temp.spec]])
appearing outside of the class definition, a member function shall not
be redeclared.

An inline member function (whether static or non-static) may also be
defined outside of its class definition provided either its declaration
in the class definition or its definition outside of the class
definition declares the function as `inline` or `constexpr`.

[*Note 1*: Member functions of a class in namespace scope have the
linkage of that class. Member functions of a local class (
[[class.local]]) have no linkage. See  [[basic.link]]. — *end note*]

[*Note 2*: There can be at most one definition of a non-inline member
function in a program. There may be more than one `inline` member
function definition in a program. See  [[basic.def.odr]] and 
[[dcl.inline]]. — *end note*]

If the definition of a member function is lexically outside its class
definition, the member function name shall be qualified by its class
name using the `::` operator.

[*Note 3*: A name used in a member function definition (that is, in the
*parameter-declaration-clause* including the default arguments (
[[dcl.fct.default]]) or in the member function body) is looked up as
described in  [[basic.lookup]]. — *end note*]

[*Example 1*:

``` cpp
struct X {
  typedef int T;
  static T count;
  void f(T);
};
void X::f(T t = count) { }
```

The member function `f` of class `X` is defined in global scope; the
notation `X::f` specifies that the function `f` is a member of class `X`
and in the scope of class `X`. In the function definition, the parameter
type `T` refers to the typedef member `T` declared in class `X` and the
default argument `count` refers to the static data member `count`
declared in class `X`.

— *end example*]

[*Note 4*: A `static` local variable or local type in a member function
always refers to the same entity, whether or not the member function is
`inline`. — *end note*]

Previously declared member functions may be mentioned in `friend`
declarations.

Member functions of a local class shall be defined inline in their class
definition, if they are defined at all.

[*Note 5*:

A member function can be declared (but not defined) using a typedef for
a function type. The resulting member function has exactly the same type
as it would have if the function declarator were provided explicitly,
see  [[dcl.fct]]. For example,

``` cpp
typedef void fv();
typedef void fvc() const;
struct S {
  fv memfunc1;      // equivalent to: void memfunc1();
  void memfunc2();
  fvc memfunc3;     // equivalent to: void memfunc3() const;
};
fv  S::* pmfv1 = &S::memfunc1;
fv  S::* pmfv2 = &S::memfunc2;
fvc S::* pmfv3 = &S::memfunc3;
```

Also see  [[temp.arg]].

— *end note*]

### Non-static member functions <a id="class.mfct.non-static">[[class.mfct.non-static]]</a>

A non-static member function may be called for an object of its class
type, or for an object of a class derived (Clause  [[class.derived]])
from its class type, using the class member access syntax (
[[expr.ref]],  [[over.match.call]]). A non-static member function may
also be called directly using the function call syntax ([[expr.call]], 
[[over.match.call]]) from within the body of a member function of its
class or of a class derived from its class.

If a non-static member function of a class `X` is called for an object
that is not of type `X`, or of a type derived from `X`, the behavior is
undefined.

When an *id-expression* ([[expr.prim]]) that is not part of a class
member access syntax ([[expr.ref]]) and not used to form a pointer to
member ([[expr.unary.op]]) is used in a member of class `X` in a
context where `this` can be used ([[expr.prim.this]]), if name lookup (
[[basic.lookup]]) resolves the name in the *id-expression* to a
non-static non-type member of some class `C`, and if either the
*id-expression* is potentially evaluated or `C` is `X` or a base class
of `X`, the *id-expression* is transformed into a class member access
expression ([[expr.ref]]) using `(*this)` ([[class.this]]) as the
*postfix-expression* to the left of the `.` operator.

[*Note 1*: If `C` is not `X` or a base class of `X`, the class member
access expression is ill-formed. — *end note*]

Similarly during name lookup, when an *unqualified-id* ([[expr.prim]])
used in the definition of a member function for class `X` resolves to a
static member, an enumerator or a nested type of class `X` or of a base
class of `X`, the *unqualified-id* is transformed into a
*qualified-id* ([[expr.prim]]) in which the *nested-name-specifier*
names the class of the member function. These transformations do not
apply in the template definition context ([[temp.dep.type]]).

[*Example 1*:

``` cpp
struct tnode {
  char tword[20];
  int count;
  tnode* left;
  tnode* right;
  void set(const char*, tnode* l, tnode* r);
};

void tnode::set(const char* w, tnode* l, tnode* r) {
  count = strlen(w)+1;
  if (sizeof(tword)<=count)
      perror("tnode string too long");
  strcpy(tword,w);
  left = l;
  right = r;
}

void f(tnode n1, tnode n2) {
  n1.set("abc",&n2,0);
  n2.set("def",0,0);
}
```

In the body of the member function `tnode::set`, the member names
`tword`, `count`, `left`, and `right` refer to members of the object for
which the function is called. Thus, in the call `n1.set("abc",&n2,0)`,
`tword` refers to `n1.tword`, and in the call `n2.set("def",0,0)`, it
refers to `n2.tword`. The functions `strlen`, `perror`, and `strcpy` are
not members of the class `tnode` and should be declared elsewhere.[^4]

— *end example*]

A non-static member function may be declared `const`, `volatile`, or
`const` `volatile`. These *cv-qualifier*s affect the type of the `this`
pointer ([[class.this]]). They also affect the function type (
[[dcl.fct]]) of the member function; a member function declared `const`
is a *const* member function, a member function declared `volatile` is a
*volatile* member function and a member function declared `const`
`volatile` is a *const volatile* member function.

[*Example 2*:

``` cpp
struct X {
  void g() const;
  void h() const volatile;
};
```

`X::g` is a `const` member function and `X::h` is a `const` `volatile`
member function.

— *end example*]

A non-static member function may be declared with a *ref-qualifier* (
[[dcl.fct]]); see  [[over.match.funcs]].

A non-static member function may be declared *virtual* (
[[class.virtual]]) or *pure virtual* ([[class.abstract]]).

#### The `this` pointer <a id="class.this">[[class.this]]</a>

In the body of a non-static ([[class.mfct]]) member function, the
keyword `this` is a prvalue expression whose value is the address of the
object for which the function is called. The type of `this` in a member
function of a class `X` is `X*`. If the member function is declared
`const`, the type of `this` is `const` `X*`, if the member function is
declared `volatile`, the type of `this` is `volatile` `X*`, and if the
member function is declared `const` `volatile`, the type of `this` is
`const` `volatile` `X*`.

[*Note 1*: Thus in a `const` member function, the object for which the
function is called is accessed through a `const` access
path. — *end note*]

[*Example 1*:

``` cpp
struct s {
  int a;
  int f() const;
  int g() { return a++; }
  int h() const { return a++; } // error
};

int s::f() const { return a; }
```

The `a++` in the body of `s::h` is ill-formed because it tries to modify
(a part of) the object for which `s::h()` is called. This is not allowed
in a `const` member function because `this` is a pointer to `const`;
that is, `*this` has `const` type.

— *end example*]

Similarly, `volatile` semantics ([[dcl.type.cv]]) apply in `volatile`
member functions when accessing the object and its non-static data
members.

A cv-qualified member function can be called on an object-expression (
[[expr.ref]]) only if the object-expression is as cv-qualified or
less-cv-qualified than the member function.

[*Example 2*:

``` cpp
void k(s& x, const s& y) {
  x.f();
  x.g();
  y.f();
  y.g();                        // error
}
```

The call `y.g()` is ill-formed because `y` is `const` and `s::g()` is a
non-`const` member function, that is, `s::g()` is less-qualified than
the object-expression `y`.

— *end example*]

Constructors ([[class.ctor]]) and destructors ([[class.dtor]]) shall
not be declared `const`, `volatile` or `const` `volatile`.

[*Note 2*: However, these functions can be invoked to create and
destroy objects with cv-qualified types, see  [[class.ctor]] and 
[[class.dtor]]. — *end note*]

### Static members <a id="class.static">[[class.static]]</a>

A static member `s` of class `X` may be referred to using the
*qualified-id* expression `X::s`; it is not necessary to use the class
member access syntax ([[expr.ref]]) to refer to a static member. A
static member may be referred to using the class member access syntax,
in which case the object expression is evaluated.

[*Example 1*:

``` cpp
struct process {
  static void reschedule();
};
process& g();

void f() {
  process::reschedule();        // OK: no object necessary
  g().reschedule();             // g() is called
}
```

— *end example*]

A static member may be referred to directly in the scope of its class or
in the scope of a class derived (Clause  [[class.derived]]) from its
class; in this case, the static member is referred to as if a
*qualified-id* expression was used, with the *nested-name-specifier* of
the *qualified-id* naming the class scope from which the static member
is referenced.

[*Example 2*:

``` cpp
int g();
struct X {
  static int g();
};
struct Y : X {
  static int i;
};
int Y::i = g();                 // equivalent to Y::g();
```

— *end example*]

If an *unqualified-id* ([[expr.prim]]) is used in the definition of a
static member following the member’s *declarator-id*, and name lookup (
[[basic.lookup.unqual]]) finds that the *unqualified-id* refers to a
static member, enumerator, or nested type of the member’s class (or of a
base class of the member’s class), the *unqualified-id* is transformed
into a *qualified-id* expression in which the *nested-name-specifier*
names the class scope from which the member is referenced.

[*Note 1*: See  [[expr.prim]] for restrictions on the use of non-static
data members and non-static member functions. — *end note*]

Static members obey the usual class member access rules (Clause 
[[class.access]]). When used in the declaration of a class member, the
`static` specifier shall only be used in the member declarations that
appear within the *member-specification* of the class definition.

[*Note 2*: It cannot be specified in member declarations that appear in
namespace scope. — *end note*]

#### Static member functions <a id="class.static.mfct">[[class.static.mfct]]</a>

[*Note 1*: The rules described in  [[class.mfct]] apply to static
member functions. — *end note*]

[*Note 2*: A static member function does not have a `this` pointer (
[[class.this]]). — *end note*]

A static member function shall not be `virtual`. There shall not be a
static and a non-static member function with the same name and the same
parameter types ([[over.load]]). A static member function shall not be
declared `const`, `volatile`, or `const volatile`.

#### Static data members <a id="class.static.data">[[class.static.data]]</a>

A static data member is not part of the subobjects of a class. If a
static data member is declared `thread_local` there is one copy of the
member per thread. If a static data member is not declared
`thread_local` there is one copy of the data member that is shared by
all the objects of the class.

The declaration of a non-inline static data member in its class
definition is not a definition and may be of an incomplete type other
than cv `void`. The definition for a static data member that is not
defined inline in the class definition shall appear in a namespace scope
enclosing the member’s class definition. In the definition at namespace
scope, the name of the static data member shall be qualified by its
class name using the `::` operator. The *initializer* expression in the
definition of a static data member is in the scope of its class (
[[basic.scope.class]]).

[*Example 1*:

``` cpp
class process {
  static process* run_chain;
  static process* running;
};

process* process::running = get_main();
process* process::run_chain = running;
```

The static data member `run_chain` of class `process` is defined in
global scope; the notation `process::run_chain` specifies that the
member `run_chain` is a member of class `process` and in the scope of
class `process`. In the static data member definition, the *initializer*
expression refers to the static data member `running` of class
`process`.

— *end example*]

[*Note 1*:

Once the static data member has been defined, it exists even if no
objects of its class have been created.

[*Example 2*:

In the example above, `run_chain` and `running` exist even if no objects
of class `process` are created by the program.

— *end example*]

— *end note*]

If a non-volatile non-inline `const` static data member is of integral
or enumeration type, its declaration in the class definition can specify
a *brace-or-equal-initializer* in which every *initializer-clause* that
is an *assignment-expression* is a constant expression (
[[expr.const]]). The member shall still be defined in a namespace scope
if it is odr-used ([[basic.def.odr]]) in the program and the namespace
scope definition shall not contain an *initializer*. An inline static
data member may be defined in the class definition and may specify a
*brace-or-equal-initializer*. If the member is declared with the
`constexpr` specifier, it may be redeclared in namespace scope with no
initializer (this usage is deprecated; see [[depr.static_constexpr]]).
Declarations of other static data members shall not specify a
*brace-or-equal-initializer*.

[*Note 2*: There shall be exactly one definition of a static data
member that is odr-used ([[basic.def.odr]]) in a program; no diagnostic
is required. — *end note*]

Unnamed classes and classes contained directly or indirectly within
unnamed classes shall not contain static data members.

[*Note 3*: Static data members of a class in namespace scope have the
linkage of that class ([[basic.link]]). A local class cannot have
static data members ([[class.local]]). — *end note*]

Static data members are initialized and destroyed exactly like non-local
variables ([[basic.start.static]], [[basic.start.dynamic]],
[[basic.start.term]]).

A static data member shall not be `mutable` ([[dcl.stc]]).

### Bit-fields <a id="class.bit">[[class.bit]]</a>

A *member-declarator* of the form

specifies a bit-field; its length is set off from the bit-field name by
a colon. The optional *attribute-specifier-seq* appertains to the entity
being declared. The bit-field attribute is not part of the type of the
class member. The *constant-expression* shall be an integral constant
expression with a value greater than or equal to zero. The value of the
integral constant expression may be larger than the number of bits in
the object representation ([[basic.types]]) of the bit-field’s type; in
such cases the extra bits are used as padding bits and do not
participate in the value representation ([[basic.types]]) of the
bit-field. Allocation of bit-fields within a class object is
*implementation-defined*. Alignment of bit-fields is
*implementation-defined*. Bit-fields are packed into some addressable
allocation unit.

[*Note 1*: Bit-fields straddle allocation units on some machines and
not on others. Bit-fields are assigned right-to-left on some machines,
left-to-right on others. — *end note*]

A declaration for a bit-field that omits the *identifier* declares an
*unnamed bit-field*. Unnamed bit-fields are not members and cannot be
initialized.

[*Note 2*: An unnamed bit-field is useful for padding to conform to
externally-imposed layouts. — *end note*]

As a special case, an unnamed bit-field with a width of zero specifies
alignment of the next bit-field at an allocation unit boundary. Only
when declaring an unnamed bit-field may the value of the
*constant-expression* be equal to zero.

A bit-field shall not be a static member. A bit-field shall have
integral or enumeration type ([[basic.fundamental]]). A `bool` value
can successfully be stored in a bit-field of any nonzero size. The
address-of operator `&` shall not be applied to a bit-field, so there
are no pointers to bit-fields. A non-const reference shall not be bound
to a bit-field ([[dcl.init.ref]]).

[*Note 3*: If the initializer for a reference of type `const` `T&` is
an lvalue that refers to a bit-field, the reference is bound to a
temporary initialized to hold the value of the bit-field; the reference
is not bound to the bit-field directly. See 
[[dcl.init.ref]]. — *end note*]

If the value `true` or `false` is stored into a bit-field of type `bool`
of any size (including a one bit bit-field), the original `bool` value
and the value of the bit-field shall compare equal. If the value of an
enumerator is stored into a bit-field of the same enumeration type and
the number of bits in the bit-field is large enough to hold all the
values of that enumeration type ([[dcl.enum]]), the original enumerator
value and the value of the bit-field shall compare equal.

[*Example 1*:

``` cpp
enum BOOL { FALSE=0, TRUE=1 };
struct A {
  BOOL b:1;
};
A a;
void f() {
  a.b = TRUE;
  if (a.b == TRUE)              // yields true
    { ... }
}
```

— *end example*]

### Nested class declarations <a id="class.nest">[[class.nest]]</a>

A class can be declared within another class. A class declared within
another is called a *nested* class. The name of a nested class is local
to its enclosing class. The nested class is in the scope of its
enclosing class.

[*Note 1*: See  [[expr.prim]] for restrictions on the use of non-static
data members and non-static member functions. — *end note*]

[*Example 1*:

``` cpp
int x;
int y;

struct enclose {
  int x;
  static int s;

  struct inner {
    void f(int i) {
      int a = sizeof(x);        // OK: operand of sizeof is an unevaluated operand
      x = i;                    // error: assign to enclose::x
      s = i;                    // OK: assign to enclose::s
      ::x = i;                  // OK: assign to global x
      y = i;                    // OK: assign to global y
    }
    void g(enclose* p, int i) {
      p->x = i;                 // OK: assign to enclose::x
    }
  };
};

inner* p = 0;                   // error: inner not in scope
```

— *end example*]

Member functions and static data members of a nested class can be
defined in a namespace scope enclosing the definition of their class.

[*Example 2*:

``` cpp
struct enclose {
  struct inner {
    static int x;
    void f(int i);
  };
};

int enclose::inner::x = 1;

void enclose::inner::f(int i) { ... }
```

— *end example*]

If class `X` is defined in a namespace scope, a nested class `Y` may be
declared in class `X` and later defined in the definition of class `X`
or be later defined in a namespace scope enclosing the definition of
class `X`.

[*Example 3*:

``` cpp
class E {
  class I1;                     // forward declaration of nested class
  class I2;
  class I1 { };                 // definition of nested class
};
class E::I2 { };                // definition of nested class
```

— *end example*]

Like a member function, a friend function ([[class.friend]]) defined
within a nested class is in the lexical scope of that class; it obeys
the same rules for name binding as a static member function of that
class ([[class.static]]), but it has no special access rights to
members of an enclosing class.

### Nested type names <a id="class.nested.type">[[class.nested.type]]</a>

Type names obey exactly the same scope rules as other names. In
particular, type names defined within a class definition cannot be used
outside their class without qualification.

[*Example 1*:

``` cpp
struct X {
  typedef int I;
  class Y { ... };
  I a;
};

I b;                            // error
Y c;                            // error
X::Y d;                         // OK
X::I e;                         // OK
```

— *end example*]

## Unions <a id="class.union">[[class.union]]</a>

In a union, a non-static data member is *active* if its name refers to
an object whose lifetime has begun and has not ended ([[basic.life]]).
At most one of the non-static data members of an object of union type
can be active at any time, that is, the value of at most one of the
non-static data members can be stored in a union at any time.

[*Note 1*: One special guarantee is made in order to simplify the use
of unions: If a standard-layout union contains several standard-layout
structs that share a common initial sequence ([[class.mem]]), and if a
non-static data member of an object of this standard-layout union type
is active and is one of the standard-layout structs, it is permitted to
inspect the common initial sequence of any of the standard-layout struct
members; see  [[class.mem]]. — *end note*]

The size of a union is sufficient to contain the largest of its
non-static data members. Each non-static data member is allocated as if
it were the sole member of a struct.

[*Note 2*: A union object and its non-static data members are
pointer-interconvertible ([[basic.compound]], [[expr.static.cast]]). As
a consequence, all non-static data members of a union object have the
same address. — *end note*]

A union can have member functions (including constructors and
destructors), but it shall not have virtual ([[class.virtual]])
functions. A union shall not have base classes. A union shall not be
used as a base class. If a union contains a non-static data member of
reference type the program is ill-formed.

[*Note 3*: Absent default member initializers ([[class.mem]]), if any
non-static data member of a union has a non-trivial default
constructor ([[class.ctor]]), copy constructor ([[class.copy]]), move
constructor ([[class.copy]]), copy assignment operator (
[[class.copy]]), move assignment operator ([[class.copy]]), or
destructor ([[class.dtor]]), the corresponding member function of the
union must be user-provided or it will be implicitly deleted (
[[dcl.fct.def.delete]]) for the union. — *end note*]

[*Example 1*:

Consider the following union:

``` cpp
union U {
  int i;
  float f;
  std::string s;
};
```

Since `std::string` ([[string.classes]]) declares non-trivial versions
of all of the special member functions, `U` will have an implicitly
deleted default constructor, copy/move constructor, copy/move assignment
operator, and destructor. To use `U`, some or all of these member
functions must be user-provided.

— *end example*]

When the left operand of an assignment operator involves a member access
expression ([[expr.ref]]) that nominates a union member, it may begin
the lifetime of that union member, as described below. For an expression
`E`, define the set S(E) of subexpressions of `E` as follows:

- If `E` is of the form `A.B`, S(E) contains the elements of S(A), and
  also contains `A.B` if `B` names a union member of a non-class,
  non-array type, or of a class type with a trivial default constructor
  that is not deleted, or an array of such types.
- If `E` is of the form `A[B]` and is interpreted as a built-in array
  subscripting operator, S(E) is S(A) if `A` is of array type, S(B) if
  `B` is of array type, and empty otherwise.
- Otherwise, S(E) is empty.

In an assignment expression of the form `E1 = E2` that uses either the
built-in assignment operator ([[expr.ass]]) or a trivial assignment
operator ([[class.copy]]), for each element `X` of S(`E1`), if
modification of `X` would have undefined behavior under  [[basic.life]],
an object of the type of `X` is implicitly created in the nominated
storage; no initialization is performed and the beginning of its
lifetime is sequenced after the value computation of the left and right
operands and before the assignment.

[*Note 4*: This ends the lifetime of the previously-active member of
the union, if any ([[basic.life]]). — *end note*]

[*Example 2*:

``` cpp
union A { int x; int y[4]; };
struct B { A a; };
union C { B b; int k; };
int f() {
  C c;                  // does not start lifetime of any union member
  c.b.a.y[3] = 4;       // OK: S(c.b.a.y[3]) contains c.b and c.b.a.y;
                        // creates objects to hold union members c.b and c.b.a.y
  return c.b.a.y[3];    // OK: c.b.a.y refers to newly created object (see [basic.life])
}

struct X { const int a; int b; };
union Y { X x; int k; };
void g() {
  Y y = { { 1, 2 } };   // OK, y.x is active union member ([class.mem])
  int n = y.x.a;
  y.k = 4;              // OK: ends lifetime of y.x, y.k is active member of union
  y.x.b = n;            // undefined behavior: y.x.b modified outside its lifetime,
                        // S(y.x.b) is empty because X's default constructor is deleted,
                        // so union member y.x's lifetime does not implicitly start
}
```

— *end example*]

[*Note 5*: In general, one must use explicit destructor calls and
placement *new-expression* to change the active member of a
union. — *end note*]

[*Example 3*:

Consider an object `u` of a `union` type `U` having non-static data
members `m` of type `M` and `n` of type `N`. If `M` has a non-trivial
destructor and `N` has a non-trivial constructor (for instance, if they
declare or inherit virtual functions), the active member of `u` can be
safely switched from `m` to `n` using the destructor and placement
*new-expression* as follows:

``` cpp
u.m.~M();
new (&u.n) N;
```

— *end example*]

### Anonymous unions <a id="class.union.anon">[[class.union.anon]]</a>

A union of the form

is called an *anonymous union*; it defines an unnamed type and an
unnamed object of that type called an *anonymous union object*. Each
*member-declaration* in the *member-specification* of an anonymous union
shall either define a non-static data member or be a
*static_assert-declaration*.

[*Note 1*: Nested types, anonymous unions, and functions cannot be
declared within an anonymous union. — *end note*]

The names of the members of an anonymous union shall be distinct from
the names of any other entity in the scope in which the anonymous union
is declared. For the purpose of name lookup, after the anonymous union
definition, the members of the anonymous union are considered to have
been defined in the scope in which the anonymous union is declared.

[*Example 1*:

``` cpp
void f() {
  union { int a; const char* p; };
  a = 1;
  p = "Jennifer";
}
```

Here `a` and `p` are used like ordinary (non-member) variables, but
since they are union members they have the same address.

— *end example*]

Anonymous unions declared in a named namespace or in the global
namespace shall be declared `static`. Anonymous unions declared at block
scope shall be declared with any storage class allowed for a block-scope
variable, or with no storage class. A storage class is not allowed in a
declaration of an anonymous union in a class scope. An anonymous union
shall not have `private` or `protected` members (Clause 
[[class.access]]). An anonymous union shall not have member functions.

A union for which objects, pointers, or references are declared is not
an anonymous union.

[*Example 2*:

``` cpp
void f() {
  union { int aa; char* p; } obj, *ptr = &obj;
  aa = 1;           // error
  ptr->aa = 1;      // OK
}
```

The assignment to plain `aa` is ill-formed since the member name is not
visible outside the union, and even if it were visible, it is not
associated with any particular object.

— *end example*]

[*Note 2*: Initialization of unions with no user-declared constructors
is described in  [[dcl.init.aggr]]. — *end note*]

A *union-like class* is a union or a class that has an anonymous union
as a direct member. A union-like class `X` has a set of *variant
members*. If `X` is a union, a non-static data member of `X` that is not
an anonymous union is a variant member of `X`. In addition, a non-static
data member of an anonymous union that is a member of `X` is also a
variant member of `X`. At most one variant member of a union may have a
default member initializer.

[*Example 3*:

``` cpp
union U {
  int x = 0;
  union {
    int k;
  };
  union {
    int z;
    int y = 1;      // error: initialization for second variant member of U
  };
};
```

— *end example*]

## Local class declarations <a id="class.local">[[class.local]]</a>

A class can be declared within a function definition; such a class is
called a *local* class. The name of a local class is local to its
enclosing scope. The local class is in the scope of the enclosing scope,
and has the same access to names outside the function as does the
enclosing function. Declarations in a local class shall not odr-use (
[[basic.def.odr]]) a variable with automatic storage duration from an
enclosing scope.

[*Example 1*:

``` cpp
int x;
void f() {
  static int s;
  int x;
  const int N = 5;
  extern int q();

  struct local {
    int g() { return x; }       // error: odr-use of automatic variable x
    int h() { return s; }       // OK
    int k() { return ::x; }     // OK
    int l() { return q(); }     // OK
    int m() { return N; }       // OK: not an odr-use
    int* n() { return &N; }     // error: odr-use of automatic variable N
  };
}

local* p = 0;                   // error: local not in scope
```

— *end example*]

An enclosing function has no special access to members of the local
class; it obeys the usual access rules (Clause  [[class.access]]).
Member functions of a local class shall be defined within their class
definition, if they are defined at all.

If class `X` is a local class a nested class `Y` may be declared in
class `X` and later defined in the definition of class `X` or be later
defined in the same scope as the definition of class `X`. A class nested
within a local class is a local class.

A local class shall not have static data members.

# Derived classes <a id="class.derived">[[class.derived]]</a>

A list of base classes can be specified in a class definition using the
notation:

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

The optional *attribute-specifier-seq* appertains to the
*base-specifier*.

A *class-or-decltype* shall denote a class type that is not an
incompletely defined class (Clause  [[class]]). The class denoted by the
*class-or-decltype* of a *base-specifier* is called a *direct base
class* for the class being defined. During the lookup for a base class
name, non-type names are ignored ([[basic.scope.hiding]]). If the name
found is not a *class-name*, the program is ill-formed. A class `B` is a
base class of a class `D` if it is a direct base class of `D` or a
direct base class of one of `D`’s base classes. A class is an *indirect*
base class of another if it is a base class but not a direct base class.
A class is said to be (directly or indirectly) *derived* from its
(direct or indirect) base classes.

[*Note 1*: See Clause  [[class.access]] for the meaning of
*access-specifier*. — *end note*]

Unless redeclared in the derived class, members of a base class are also
considered to be members of the derived class. Members of a base class
other than constructors are said to be *inherited* by the derived class.
Constructors of a base class can also be inherited as described in 
[[namespace.udecl]]. Inherited members can be referred to in expressions
in the same manner as other members of the derived class, unless their
names are hidden or ambiguous ([[class.member.lookup]]).

[*Note 2*: The scope resolution operator `::` ([[expr.prim]]) can be
used to refer to a direct or indirect base member explicitly. This
allows access to a name that has been redeclared in the derived class. A
derived class can itself serve as a base class subject to access
control; see  [[class.access.base]]. A pointer to a derived class can be
implicitly converted to a pointer to an accessible unambiguous base
class ([[conv.ptr]]). An lvalue of a derived class type can be bound to
a reference to an accessible unambiguous base class (
[[dcl.init.ref]]). — *end note*]

The *base-specifier-list* specifies the type of the *base class
subobjects* contained in an object of the derived class type.

[*Example 1*:

``` cpp
struct Base {
  int a, b, c;
};
```

``` cpp
struct Derived : Base {
  int b;
};
```

``` cpp
struct Derived2 : Derived {
  int c;
};
```

Here, an object of class `Derived2` will have a subobject of class
`Derived` which in turn will have a subobject of class `Base`.

— *end example*]

A *base-specifier* followed by an ellipsis is a pack expansion (
[[temp.variadic]]).

The order in which the base class subobjects are allocated in the most
derived object ([[intro.object]]) is unspecified.

[*Note 3*:

A derived class and its base class subobjects can be represented by a
directed acyclic graph (DAG) where an arrow means “directly derived
from”. An arrow need not have a physical representation in memory. A DAG
of subobjects is often referred to as a “subobject lattice”.

— *end note*]

[*Note 4*: Initialization of objects representing base classes can be
specified in constructors; see  [[class.base.init]]. — *end note*]

[*Note 5*: A base class subobject might have a layout ([[basic.stc]])
different from the layout of a most derived object of the same type. A
base class subobject might have a polymorphic behavior (
[[class.cdtor]]) different from the polymorphic behavior of a most
derived object of the same type. A base class subobject may be of zero
size (Clause  [[class]]); however, two subobjects that have the same
class type and that belong to the same most derived object must not be
allocated at the same address ([[expr.eq]]). — *end note*]

## Multiple base classes <a id="class.mi">[[class.mi]]</a>

A class can be derived from any number of base classes.

[*Note 1*: The use of more than one direct base class is often called
multiple inheritance. — *end note*]

[*Example 1*:

``` cpp
class A { ... };
class B { ... };
class C { ... };
class D : public A, public B, public C { ... };
```

— *end example*]

[*Note 2*: The order of derivation is not significant except as
specified by the semantics of initialization by constructor (
[[class.base.init]]), cleanup ([[class.dtor]]), and storage layout (
[[class.mem]],  [[class.access.spec]]). — *end note*]

A class shall not be specified as a direct base class of a derived class
more than once.

[*Note 3*: A class can be an indirect base class more than once and can
be a direct and an indirect base class. There are limited things that
can be done with such a class. The non-static data members and member
functions of the direct base class cannot be referred to in the scope of
the derived class. However, the static members, enumerations and types
can be unambiguously referred to. — *end note*]

[*Example 2*:

``` cpp
class X { ... };
class Y : public X, public X { ... };             // ill-formed
```

``` cpp
class L { public: int next;  ... };
class A : public L { ... };
class B : public L { ... };
class C : public A, public B { void f(); ... };   // well-formed
class D : public A, public L { void f(); ... };   // well-formed
```

— *end example*]

A base class specifier that does not contain the keyword `virtual`
specifies a *non-virtual base class*. A base class specifier that
contains the keyword `virtual` specifies a *virtual base class*. For
each distinct occurrence of a non-virtual base class in the class
lattice of the most derived class, the most derived object (
[[intro.object]]) shall contain a corresponding distinct base class
subobject of that type. For each distinct base class that is specified
virtual, the most derived object shall contain a single base class
subobject of that type.

[*Note 4*:

For an object of class type `C`, each distinct occurrence of a
(non-virtual) base class `L` in the class lattice of `C` corresponds
one-to-one with a distinct `L` subobject within the object of type `C`.
Given the class `C` defined above, an object of class `C` will have two
subobjects of class `L` as shown in Figure  [[fig:nonvirt]].

In such lattices, explicit qualification can be used to specify which
subobject is meant. The body of function `C::f` could refer to the
member `next` of each `L` subobject:

``` cpp
void C::f() { A::next = B::next; }      // well-formed
```

Without the `A::` or `B::` qualifiers, the definition of `C::f` above
would be ill-formed because of ambiguity ([[class.member.lookup]]).

— *end note*]

[*Note 5*:

In contrast, consider the case with a virtual base class:

``` cpp
class V { ... };
class A : virtual public V { ... };
class B : virtual public V { ... };
class C : public A, public B { ... };
```

For an object `c` of class type `C`, a single subobject of type `V` is
shared by every base class subobject of `c` that has a `virtual` base
class of type `V`. Given the class `C` defined above, an object of class
`C` will have one subobject of class `V`, as shown in Figure 
[[fig:virt]].

— *end note*]

[*Note 6*:

A class can have both virtual and non-virtual base classes of a given
type.

``` cpp
class B { ... };
class X : virtual public B { ... };
class Y : virtual public B { ... };
class Z : public B { ... };
class AA : public X, public Y, public Z { ... };
```

For an object of class `AA`, all `virtual` occurrences of base class `B`
in the class lattice of `AA` correspond to a single `B` subobject within
the object of type `AA`, and every other occurrence of a (non-virtual)
base class `B` in the class lattice of `AA` corresponds one-to-one with
a distinct `B` subobject within the object of type `AA`. Given the class
`AA` defined above, class `AA` has two subobjects of class `B`: `Z`’s
`B` and the virtual `B` shared by `X` and `Y`, as shown in Figure 
[[fig:virtnonvirt]].

— *end note*]

## Member name lookup <a id="class.member.lookup">[[class.member.lookup]]</a>

Member name lookup determines the meaning of a name (*id-expression*) in
a class scope ([[basic.scope.class]]). Name lookup can result in an
*ambiguity*, in which case the program is ill-formed. For an
*id-expression*, name lookup begins in the class scope of `this`; for a
*qualified-id*, name lookup begins in the scope of the
*nested-name-specifier*. Name lookup takes place before access control (
[[basic.lookup]], Clause  [[class.access]]).

The following steps define the result of name lookup for a member name
`f` in a class scope `C`.

The *lookup set* for `f` in `C`, called S(f,C), consists of two
component sets: the *declaration set*, a set of members named `f`; and
the *subobject set*, a set of subobjects where declarations of these
members (possibly including *using-declaration*s) were found. In the
declaration set, *using-declaration*s are replaced by the set of
designated members that are not hidden or overridden by members of the
derived class ([[namespace.udecl]]), and type declarations (including
injected-class-names) are replaced by the types they designate. S(f,C)
is calculated as follows:

If `C` contains a declaration of the name `f`, the declaration set
contains every declaration of `f` declared in `C` that satisfies the
requirements of the language construct in which the lookup occurs.

[*Note 1*: Looking up a name in an *elaborated-type-specifier* (
[[basic.lookup.elab]]) or *base-specifier* (Clause  [[class.derived]]),
for instance, ignores all non-type declarations, while looking up a name
in a *nested-name-specifier* ([[basic.lookup.qual]]) ignores function,
variable, and enumerator declarations. As another example, looking up a
name in a *using-declaration* ([[namespace.udecl]]) includes the
declaration of a class or enumeration that would ordinarily be hidden by
another declaration of that name in the same scope. — *end note*]

If the resulting declaration set is not empty, the subobject set
contains `C` itself, and calculation is complete.

Otherwise (i.e., `C` does not contain a declaration of `f` or the
resulting declaration set is empty), S(f,C) is initially empty. If `C`
has base classes, calculate the lookup set for `f` in each direct base
class subobject Bᵢ, and merge each such lookup set S(f,Bᵢ) in turn into
S(f,C).

The following steps define the result of merging lookup set S(f,Bᵢ) into
the intermediate S(f,C):

- If each of the subobject members of S(f,Bᵢ) is a base class subobject
  of at least one of the subobject members of S(f,C), or if S(f,Bᵢ) is
  empty, S(f,C) is unchanged and the merge is complete. Conversely, if
  each of the subobject members of S(f,C) is a base class subobject of
  at least one of the subobject members of S(f,Bᵢ), or if S(f,C) is
  empty, the new S(f,C) is a copy of S(f,Bᵢ).
- Otherwise, if the declaration sets of S(f,Bᵢ) and S(f,C) differ, the
  merge is ambiguous: the new S(f,C) is a lookup set with an invalid
  declaration set and the union of the subobject sets. In subsequent
  merges, an invalid declaration set is considered different from any
  other.
- Otherwise, the new S(f,C) is a lookup set with the shared set of
  declarations and the union of the subobject sets.

The result of name lookup for `f` in `C` is the declaration set of
S(f,C). If it is an invalid set, the program is ill-formed.

[*Example 1*:

``` cpp
struct A { int x; };                    // S(x,A) = { { A::x }, { A } }
struct B { float x; };                  // S(x,B) = { { B::x }, { B } }
struct C: public A, public B { };       // S(x,C) = { invalid, { A in C, B in C } }
struct D: public virtual C { };         // S(x,D) = S(x,C)
struct E: public virtual C { char x; }; // S(x,E) = { { E::x }, { E } }
struct F: public D, public E { };       // S(x,F) = S(x,E)
int main() {
  F f;
  f.x = 0;                              // OK, lookup finds E::x
}
```

S(x,F) is unambiguous because the `A` and `B` base class subobjects of
`D` are also base class subobjects of `E`, so S(x,D) is discarded in the
first merge step.

— *end example*]

If the name of an overloaded function is unambiguously found, overload
resolution ([[over.match]]) also takes place before access control.
Ambiguities can often be resolved by qualifying a name with its class
name.

[*Example 2*:

``` cpp
struct A {
  int f();
};
```

``` cpp
struct B {
  int f();
};
```

``` cpp
struct C : A, B {
  int f() { return A::f() + B::f(); }
};
```

— *end example*]

[*Note 2*: A static member, a nested type or an enumerator defined in a
base class `T` can unambiguously be found even if an object has more
than one base class subobject of type `T`. Two base class subobjects
share the non-static member subobjects of their common virtual base
classes. — *end note*]

[*Example 3*:

``` cpp
struct V {
  int v;
};
struct A {
  int a;
  static int   s;
  enum { e };
};
struct B : A, virtual V { };
struct C : A, virtual V { };
struct D : B, C { };

void f(D* pd) {
  pd->v++;          // OK: only one v (virtual)
  pd->s++;          // OK: only one s (static)
  int i = pd->e;    // OK: only one e (enumerator)
  pd->a++;          // error, ambiguous: two a{s} in D
}
```

— *end example*]

[*Note 3*:  When virtual base classes are used, a hidden declaration
can be reached along a path through the subobject lattice that does not
pass through the hiding declaration. This is not an ambiguity. The
identical use with non-virtual base classes is an ambiguity; in that
case there is no unique instance of the name that hides all the
others. — *end note*]

[*Example 4*:

``` cpp
struct V { int f();  int x; };
struct W { int g();  int y; };
struct B : virtual V, W {
  int f();  int x;
  int g();  int y;
};
struct C : virtual V, W { };

struct D : B, C { void glorp(); };
```

The names declared in `V` and the left-hand instance of `W` are hidden
by those in `B`, but the names declared in the right-hand instance of
`W` are not hidden at all.

``` cpp
void D::glorp() {
  x++;              // OK: B::x hides V::x
  f();              // OK: B::f() hides V::f()
  y++;              // error: B::y and C's W::y
  g();              // error: B::g() and C's W::g()
}
```

— *end example*]

An explicit or implicit conversion from a pointer to or an expression
designating an object of a derived class to a pointer or reference to
one of its base classes shall unambiguously refer to a unique object
representing the base class.

[*Example 5*:

``` cpp
struct V { };
struct A { };
struct B : A, virtual V { };
struct C : A, virtual V { };
struct D : B, C { };

void g() {
  D d;
  B* pb = &d;
  A* pa = &d;       // error, ambiguous: C's A or B's A?
  V* pv = &d;       // OK: only one V subobject
}
```

— *end example*]

[*Note 4*: Even if the result of name lookup is unambiguous, use of a
name found in multiple subobjects might still be ambiguous (
[[conv.mem]],  [[expr.ref]], [[class.access.base]]). — *end note*]

[*Example 6*:

``` cpp
struct B1 {
  void f();
  static void f(int);
  int i;
};
struct B2 {
  void f(double);
};
struct I1: B1 { };
struct I2: B1 { };

struct D: I1, I2, B2 {
  using B1::f;
  using B2::f;
  void g() {
    f();                        // Ambiguous conversion of this
    f(0);                       // Unambiguous (static)
    f(0.0);                     // Unambiguous (only one B2)
    int B1::* mpB1 = &D::i;     // Unambiguous
    int D::* mpD = &D::i;       // Ambiguous conversion
  }
};
```

— *end example*]

## Virtual functions <a id="class.virtual">[[class.virtual]]</a>

[*Note 1*: Virtual functions support dynamic binding and
object-oriented programming. — *end note*]

A class that declares or inherits a virtual function is called a
*polymorphic class*.

If a virtual member function `vf` is declared in a class `Base` and in a
class `Derived`, derived directly or indirectly from `Base`, a member
function `vf` with the same name, parameter-type-list ([[dcl.fct]]),
cv-qualification, and ref-qualifier (or absence of same) as `Base::vf`
is declared, then `Derived::vf` is also virtual (whether or not it is so
declared) and it *overrides*[^5] `Base::vf`. For convenience we say that
any virtual function overrides itself. A virtual member function `C::vf`
of a class object `S` is a *final overrider* unless the most derived
class ([[intro.object]]) of which `S` is a base class subobject (if
any) declares or inherits another member function that overrides `vf`.
In a derived class, if a virtual member function of a base class
subobject has more than one final overrider the program is ill-formed.

[*Example 1*:

``` cpp
struct A {
  virtual void f();
};
struct B : virtual A {
  virtual void f();
};
struct C : B , virtual A {
  using A::f;
};

void foo() {
  C c;
  c.f();              // calls B::f, the final overrider
  c.C::f();           // calls A::f because of the using-declaration
}
```

— *end example*]

[*Example 2*:

``` cpp
struct A { virtual void f(); };
struct B : A { };
struct C : A { void f(); };
struct D : B, C { };  // OK: A::f and C::f are the final overriders
                      // for the B and C subobjects, respectively
```

— *end example*]

[*Note 2*:

A virtual member function does not have to be visible to be overridden,
for example,

``` cpp
struct B {
  virtual void f();
};
struct D : B {
  void f(int);
};
struct D2 : D {
  void f();
};
```

the function `f(int)` in class `D` hides the virtual function `f()` in
its base class `B`; `D::f(int)` is not a virtual function. However,
`f()` declared in class `D2` has the same name and the same parameter
list as `B::f()`, and therefore is a virtual function that overrides the
function `B::f()` even though `B::f()` is not visible in class `D2`.

— *end note*]

If a virtual function `f` in some class `B` is marked with the
*virt-specifier* `final` and in a class `D` derived from `B` a function
`D::f` overrides `B::f`, the program is ill-formed.

[*Example 3*:

``` cpp
struct B {
  virtual void f() const final;
};

struct D : B {
  void f() const;     // error: D::f attempts to override final B::f
};
```

— *end example*]

If a virtual function is marked with the *virt-specifier* `override` and
does not override a member function of a base class, the program is
ill-formed.

[*Example 4*:

``` cpp
struct B {
  virtual void f(int);
};

struct D : B {
  virtual void f(long) override;  // error: wrong signature overriding B::f
  virtual void f(int) override;   // OK
};
```

— *end example*]

Even though destructors are not inherited, a destructor in a derived
class overrides a base class destructor declared virtual; see 
[[class.dtor]] and  [[class.free]].

The return type of an overriding function shall be either identical to
the return type of the overridden function or *covariant* with the
classes of the functions. If a function `D::f` overrides a function
`B::f`, the return types of the functions are covariant if they satisfy
the following criteria:

- both are pointers to classes, both are lvalue references to classes,
  or both are rvalue references to classes[^6]
- the class in the return type of `B::f` is the same class as the class
  in the return type of `D::f`, or is an unambiguous and accessible
  direct or indirect base class of the class in the return type of
  `D::f`
- both pointers or references have the same cv-qualification and the
  class type in the return type of `D::f` has the same cv-qualification
  as or less cv-qualification than the class type in the return type of
  `B::f`.

If the class type in the covariant return type of `D::f` differs from
that of `B::f`, the class type in the return type of `D::f` shall be
complete at the point of declaration of `D::f` or shall be the class
type `D`. When the overriding function is called as the final overrider
of the overridden function, its result is converted to the type returned
by the (statically chosen) overridden function ([[expr.call]]).

[*Example 5*:

``` cpp
class B { };
class D : private B { friend class Derived; };
struct Base {
  virtual void vf1();
  virtual void vf2();
  virtual void vf3();
  virtual B*   vf4();
  virtual B*   vf5();
  void f();
};

struct No_good : public Base {
  D*  vf4();        // error: B (base class of D) inaccessible
};

class A;
struct Derived : public Base {
    void vf1();     // virtual and overrides Base::vf1()
    void vf2(int);  // not virtual, hides Base::vf2()
    char vf3();     // error: invalid difference in return type only
    D*   vf4();     // OK: returns pointer to derived class
    A*   vf5();     // error: returns pointer to incomplete class
    void f();
};

void g() {
  Derived d;
  Base* bp = &d;                // standard conversion:
                                // Derived* to Base*
  bp->vf1();                    // calls Derived::vf1()
  bp->vf2();                    // calls Base::vf2()
  bp->f();                      // calls Base::f() (not virtual)
  B*  p = bp->vf4();            // calls Derived::pf() and converts the
                                // result to B*
  Derived*  dp = &d;
  D*  q = dp->vf4();            // calls Derived::pf() and does not
                                // convert the result to B*
  dp->vf2();                    // ill-formed: argument mismatch
}
```

— *end example*]

[*Note 3*: The interpretation of the call of a virtual function depends
on the type of the object for which it is called (the dynamic type),
whereas the interpretation of a call of a non-virtual member function
depends only on the type of the pointer or reference denoting that
object (the static type) ([[expr.call]]). — *end note*]

[*Note 4*: The `virtual` specifier implies membership, so a virtual
function cannot be a non-member ([[dcl.fct.spec]]) function. Nor can a
virtual function be a static member, since a virtual function call
relies on a specific object for determining which function to invoke. A
virtual function declared in one class can be declared a `friend` in
another class. — *end note*]

A virtual function declared in a class shall be defined, or declared
pure ([[class.abstract]]) in that class, or both; no diagnostic is
required ([[basic.def.odr]]).

[*Example 6*:

Here are some uses of virtual functions with multiple base classes:

``` cpp
struct A {
  virtual void f();
};

struct B1 : A {                 // note non-virtual derivation
  void f();
};

struct B2 : A {
  void f();
};

struct D : B1, B2 {             // D has two separate A subobjects
};

void foo() {
  D   d;
//   A*  ap = &d;                  // would be ill-formed: ambiguous
  B1*  b1p = &d;
  A*   ap = b1p;
  D*   dp = &d;
  ap->f();                      // calls D::B1::f
  dp->f();                      // ill-formed: ambiguous
}
```

In class `D` above there are two occurrences of class `A` and hence two
occurrences of the virtual member function `A::f`. The final overrider
of `B1::A::f` is `B1::f` and the final overrider of `B2::A::f` is
`B2::f`.

— *end example*]

[*Example 7*:

The following example shows a function that does not have a unique final
overrider:

``` cpp
struct A {
  virtual void f();
};

struct VB1 : virtual A {        // note virtual derivation
  void f();
};

struct VB2 : virtual A {
  void f();
};

struct Error : VB1, VB2 {       // ill-formed
};

struct Okay : VB1, VB2 {
  void f();
};
```

Both `VB1::f` and `VB2::f` override `A::f` but there is no overrider of
both of them in class `Error`. This example is therefore ill-formed.
Class `Okay` is well formed, however, because `Okay::f` is a final
overrider.

— *end example*]

[*Example 8*:

The following example uses the well-formed classes from above.

``` cpp
struct VB1a : virtual A {       // does not declare f
};

struct Da : VB1a, VB2 {
};

void foe() {
  VB1a*  vb1ap = new Da;
  vb1ap->f();                   // calls VB2::f
}
```

— *end example*]

Explicit qualification with the scope operator ([[expr.prim]])
suppresses the virtual call mechanism.

[*Example 9*:

``` cpp
class B { public: virtual void f(); };
class D : public B { public: void f(); };

void D::f() { ... B::f(); }
```

Here, the function call in `D::f` really does call `B::f` and not
`D::f`.

— *end example*]

A function with a deleted definition ([[dcl.fct.def]]) shall not
override a function that does not have a deleted definition. Likewise, a
function that does not have a deleted definition shall not override a
function with a deleted definition.

## Abstract classes <a id="class.abstract">[[class.abstract]]</a>

[*Note 1*: The abstract class mechanism supports the notion of a
general concept, such as a `shape`, of which only more concrete
variants, such as `circle` and `square`, can actually be used. An
abstract class can also be used to define an interface for which derived
classes provide a variety of implementations. — *end note*]

An *abstract class* is a class that can be used only as a base class of
some other class; no objects of an abstract class can be created except
as subobjects of a class derived from it. A class is abstract if it has
at least one *pure virtual function*.

[*Note 2*: Such a function might be inherited: see
below. — *end note*]

A virtual function is specified *pure* by using a *pure-specifier* (
[[class.mem]]) in the function declaration in the class definition. A
pure virtual function need be defined only if called with, or as if
with ([[class.dtor]]), the *qualified-id* syntax ([[expr.prim]]).

[*Example 1*:

``` cpp
class point { ... };
class shape {                   // abstract class
  point center;
public:
  point where() { return center; }
  void move(point p) { center=p; draw(); }
  virtual void rotate(int) = 0; // pure virtual
  virtual void draw() = 0;      // pure virtual
};
```

— *end example*]

[*Note 3*: A function declaration cannot provide both a
*pure-specifier* and a definition — *end note*]

[*Example 2*:

``` cpp
struct C {
  virtual void f() = 0 { };     // ill-formed
};
```

— *end example*]

An abstract class shall not be used as a parameter type, as a function
return type, or as the type of an explicit conversion. Pointers and
references to an abstract class can be declared.

[*Example 3*:

``` cpp
shape x;                        // error: object of abstract class
shape* p;                       // OK
shape f();                      // error
void g(shape);                  // error
shape& h(shape&);               // OK
```

— *end example*]

A class is abstract if it contains or inherits at least one pure virtual
function for which the final overrider is pure virtual.

[*Example 4*:

``` cpp
class ab_circle : public shape {
  int radius;
public:
  void rotate(int) { }
  // ab_circle::draw() is a pure virtual
};
```

Since `shape::draw()` is a pure virtual function `ab_circle::draw()` is
a pure virtual by default. The alternative declaration,

``` cpp
class circle : public shape {
  int radius;
public:
  void rotate(int) { }
  void draw();                  // a definition is required somewhere
};
```

would make class `circle` non-abstract and a definition of
`circle::draw()` must be provided.

— *end example*]

[*Note 4*: An abstract class can be derived from a class that is not
abstract, and a pure virtual function may override a virtual function
which is not pure. — *end note*]

Member functions can be called from a constructor (or destructor) of an
abstract class; the effect of making a virtual call ([[class.virtual]])
to a pure virtual function directly or indirectly for the object being
created (or destroyed) from such a constructor (or destructor) is
undefined.

# Member access control <a id="class.access">[[class.access]]</a>

A member of a class can be

- `private`; that is, its name can be used only by members and friends
  of the class in which it is declared.
- `protected`; that is, its name can be used only by members and friends
  of the class in which it is declared, by classes derived from that
  class, and by their friends (see  [[class.protected]]).
- `public`; that is, its name can be used anywhere without access
  restriction.

A member of a class can also access all the names to which the class has
access. A local class of a member function may access the same names
that the member function itself may access.[^7]

Members of a class defined with the keyword `class` are `private` by
default. Members of a class defined with the keywords `struct` or
`union` are `public` by default.

[*Example 1*:

``` cpp
class X {
  int a;            // X::a is private by default
};

struct S {
  int a;            // S::a is public by default
};
```

— *end example*]

Access control is applied uniformly to all names, whether the names are
referred to from declarations or expressions.

[*Note 1*: Access control applies to names nominated by `friend`
declarations ([[class.friend]]) and *using-declaration*s (
[[namespace.udecl]]). — *end note*]

In the case of overloaded function names, access control is applied to
the function selected by overload resolution.

[*Note 2*:

Because access control applies to names, if access control is applied to
a typedef name, only the accessibility of the typedef name itself is
considered. The accessibility of the entity referred to by the typedef
is not considered. For example,

``` cpp
class A {
  class B { };
public:
  typedef B BB;
};

void f() {
  A::BB x;          // OK, typedef name A::BB is public
  A::B y;           // access error, A::B is private
}
```

— *end note*]

It should be noted that it is *access* to members and base classes that
is controlled, not their *visibility*. Names of members are still
visible, and implicit conversions to base classes are still considered,
when those members and base classes are inaccessible. The interpretation
of a given construct is established without regard to access control. If
the interpretation established makes use of inaccessible member names or
base classes, the construct is ill-formed.

All access controls in Clause  [[class.access]] affect the ability to
access a class member name from the declaration of a particular entity,
including parts of the declaration preceding the name of the entity
being declared and, if the entity is a class, the definitions of members
of the class appearing outside the class’s *member-specification*.

[*Note 3*: This access also applies to implicit references to
constructors, conversion functions, and destructors. — *end note*]

[*Example 2*:

``` cpp
class A {
  typedef int I;    // private member
  I f();
  friend I g(I);
  static I x;
  template<int> struct Q;
  template<int> friend struct R;
protected:
    struct B { };
};

A::I A::f() { return 0; }
A::I g(A::I p = A::x);
A::I g(A::I p) { return 0; }
A::I A::x = 0;
template<A::I> struct A::Q { };
template<A::I> struct R { };

struct D: A::B, A { };
```

Here, all the uses of `A::I` are well-formed because `A::f`, `A::x`, and
`A::Q` are members of class `A` and `g` and `R` are friends of class
`A`. This implies, for example, that access checking on the first use of
`A::I` must be deferred until it is determined that this use of `A::I`
is as the return type of a member of class `A`. Similarly, the use of
`A::B` as a *base-specifier* is well-formed because `D` is derived from
`A`, so checking of *base-specifier*s must be deferred until the entire
*base-specifier-list* has been seen.

— *end example*]

The names in a default argument ([[dcl.fct.default]]) are bound at the
point of declaration, and access is checked at that point rather than at
any points of use of the default argument. Access checking for default
arguments in function templates and in member functions of class
templates is performed as described in  [[temp.inst]].

The names in a default *template-argument* ([[temp.param]]) have their
access checked in the context in which they appear rather than at any
points of use of the default *template-argument*.

[*Example 3*:

``` cpp
class B { };
template <class T> class C {
protected:
  typedef T TT;
};

template <class U, class V = typename U::TT>
class D : public U { };

D <C<B> >* d;       // access error, C::TT is protected
```

— *end example*]

## Access specifiers <a id="class.access.spec">[[class.access.spec]]</a>

Member declarations can be labeled by an *access-specifier* (Clause 
[[class.derived]]):

An *access-specifier* specifies the access rules for members following
it until the end of the class or until another *access-specifier* is
encountered.

[*Example 1*:

``` cpp
class X {
  int a;            // X::a is private by default: class used
public:
  int b;            // X::b is public
  int c;            // X::c is public
};
```

— *end example*]

Any number of access specifiers is allowed and no particular order is
required.

[*Example 2*:

``` cpp
struct S {
  int a;            // S::a is public by default: struct used
protected:
  int b;            // S::b is protected
private:
  int c;            // S::c is private
public:
  int d;            // S::d is public
};
```

— *end example*]

[*Note 1*: The effect of access control on the order of allocation of
data members is described in  [[class.mem]]. — *end note*]

When a member is redeclared within its class definition, the access
specified at its redeclaration shall be the same as at its initial
declaration.

[*Example 3*:

``` cpp
struct S {
  class A;
  enum E : int;
private:
  class A { };        // error: cannot change access
  enum E: int { e0 }; // error: cannot change access
};
```

— *end example*]

[*Note 2*: In a derived class, the lookup of a base class name will
find the injected-class-name instead of the name of the base class in
the scope in which it was declared. The injected-class-name might be
less accessible than the name of the base class in the scope in which it
was declared. — *end note*]

[*Example 4*:

``` cpp
class A { };
class B : private A { };
class C : public B {
  A* p;             // error: injected-class-name A is inaccessible
  ::A* q;           // OK
};
```

— *end example*]

## Accessibility of base classes and base class members <a id="class.access.base">[[class.access.base]]</a>

If a class is declared to be a base class (Clause  [[class.derived]])
for another class using the `public` access specifier, the `public`
members of the base class are accessible as `public` members of the
derived class and `protected` members of the base class are accessible
as `protected` members of the derived class. If a class is declared to
be a base class for another class using the `protected` access
specifier, the `public` and `protected` members of the base class are
accessible as `protected` members of the derived class. If a class is
declared to be a base class for another class using the `private` access
specifier, the `public` and `protected` members of the base class are
accessible as `private` members of the derived class[^8].

In the absence of an *access-specifier* for a base class, `public` is
assumed when the derived class is defined with the *class-key* `struct`
and `private` is assumed when the class is defined with the *class-key*
`class`.

[*Example 1*:

``` cpp
class B { ... };
class D1 : private B { ... };
class D2 : public B { ... };
class D3 : B { ... };             // B private by default
struct D4 : public B { ... };
struct D5 : private B { ... };
struct D6 : B { ... };            // B public by default
class D7 : protected B { ... };
struct D8 : protected B { ... };
```

Here `B` is a public base of `D2`, `D4`, and `D6`, a private base of
`D1`, `D3`, and `D5`, and a protected base of `D7` and `D8`.

— *end example*]

[*Note 1*:

A member of a private base class might be inaccessible as an inherited
member name, but accessible directly. Because of the rules on pointer
conversions ([[conv.ptr]]) and explicit casts ([[expr.cast]]), a
conversion from a pointer to a derived class to a pointer to an
inaccessible base class might be ill-formed if an implicit conversion is
used, but well-formed if an explicit cast is used. For example,

``` cpp
class B {
public:
  int mi;                       // non-static member
  static int si;                // static member
};
class D : private B {
};
class DD : public D {
  void f();
};

void DD::f() {
  mi = 3;                       // error: mi is private in D
  si = 3;                       // error: si is private in D
  ::B  b;
  b.mi = 3;                     // OK (b.mi is different from this->mi)
  b.si = 3;                     // OK (b.si is different from this->si)
  ::B::si = 3;                  // OK
  ::B* bp1 = this;              // error: B is a private base class
  ::B* bp2 = (::B*)this;        // OK with cast
  bp2->mi = 3;                  // OK: access through a pointer to B.
}
```

— *end note*]

A base class `B` of `N` is *accessible* at *R*, if

- an invented public member of `B` would be a public member of `N`, or
- *R* occurs in a member or friend of class `N`, and an invented public
  member of `B` would be a private or protected member of `N`, or
- *R* occurs in a member or friend of a class `P` derived from `N`, and
  an invented public member of `B` would be a private or protected
  member of `P`, or
- there exists a class `S` such that `B` is a base class of `S`
  accessible at *R* and `S` is a base class of `N` accessible at *R*.

[*Example 2*:

``` cpp
class B {
public:
  int m;
};

class S: private B {
  friend class N;
};

class N: private S {
  void f() {
    B* p = this;    // OK because class S satisfies the fourth condition above: B is a base class of N
                    // accessible in f() because B is an accessible base class of S and S is an accessible
                    // base class of N.
  }
};
```

— *end example*]

If a base class is accessible, one can implicitly convert a pointer to a
derived class to a pointer to that base class ([[conv.ptr]],
[[conv.mem]]).

[*Note 2*: It follows that members and friends of a class `X` can
implicitly convert an `X*` to a pointer to a private or protected
immediate base class of `X`. — *end note*]

The access to a member is affected by the class in which the member is
named. This naming class is the class in which the member name was
looked up and found.

[*Note 3*: This class can be explicit, e.g., when a *qualified-id* is
used, or implicit, e.g., when a class member access operator (
[[expr.ref]]) is used (including cases where an implicit “`this->`” is
added). If both a class member access operator and a *qualified-id* are
used to name the member (as in `p->T::m`), the class naming the member
is the class denoted by the *nested-name-specifier* of the
*qualified-id* (that is, `T`). — *end note*]

A member `m` is accessible at the point *R* when named in class `N` if

- `m` as a member of `N` is public, or
- `m` as a member of `N` is private, and *R* occurs in a member or
  friend of class `N`, or
- `m` as a member of `N` is protected, and *R* occurs in a member or
  friend of class `N`, or in a member of a class `P` derived from `N`,
  where `m` as a member of `P` is public, private, or protected, or
- there exists a base class `B` of `N` that is accessible at *R*, and
  `m` is accessible at *R* when named in class `B`.
  \[*Example 1*:
  ``` cpp
  class B;
  class A {
  private:
    int i;
    friend void f(B*);
  };
  class B : public A { };
  void f(B* p) {
    p->i = 1;         // OK: B* can be implicitly converted to A*, and f has access to i in A
  }
  ```

  — *end example*]

If a class member access operator, including an implicit “`this->`”, is
used to access a non-static data member or non-static member function,
the reference is ill-formed if the left operand (considered as a pointer
in the “`.`” operator case) cannot be implicitly converted to a pointer
to the naming class of the right operand.

[*Note 4*: This requirement is in addition to the requirement that the
member be accessible as named. — *end note*]

## Friends <a id="class.friend">[[class.friend]]</a>

A friend of a class is a function or class that is given permission to
use the private and protected member names from the class. A class
specifies its friends, if any, by way of friend declarations. Such
declarations give special access rights to the friends, but they do not
make the nominated friends members of the befriending class.

[*Example 1*:

The following example illustrates the differences between members and
friends:

``` cpp
class X {
  int a;
  friend void friend_set(X*, int);
public:
  void member_set(int);
};

void friend_set(X* p, int i) { p->a = i; }
void X::member_set(int i) { a = i; }

void f() {
  X obj;
  friend_set(&obj,10);
  obj.member_set(10);
}
```

— *end example*]

Declaring a class to be a friend implies that the names of private and
protected members from the class granting friendship can be accessed in
the *base-specifier*s and member declarations of the befriended class.

[*Example 2*:

``` cpp
class A {
  class B { };
  friend class X;
};

struct X : A::B {               // OK: A::B accessible to friend
  A::B mx;                      // OK: A::B accessible to member of friend
  class Y {
    A::B my;                    // OK: A::B accessible to nested member of friend
  };
};
```

— *end example*]

[*Example 3*:

``` cpp
class X {
  enum { a=100 };
  friend class Y;
};

class Y {
  int v[X::a];                  // OK, Y is a friend of X
};

class Z {
  int v[X::a];                  // error: X::a is private
};
```

— *end example*]

A class shall not be defined in a friend declaration.

[*Example 4*:

``` cpp
class A {
  friend class B { };           // error: cannot define class in friend declaration
};
```

— *end example*]

A `friend` declaration that does not declare a function shall have one
of the following forms:

``` bnf
'friend' elaborated-type-specifier ';'
'friend' simple-type-specifier ';'
'friend' typename-specifier ';'
```

[*Note 1*: A `friend` declaration may be the *declaration* in a
*template-declaration* (Clause  [[temp]],
[[temp.friend]]). — *end note*]

If the type specifier in a `friend` declaration designates a (possibly
cv-qualified) class type, that class is declared as a friend; otherwise,
the `friend` declaration is ignored.

[*Example 5*:

``` cpp
class C;
typedef C Ct;

class X1 {
  friend C;                     // OK: class C is a friend
};

class X2 {
  friend Ct;                    // OK: class C is a friend
  friend D;                     // error: no type-name D in scope
  friend class D;               // OK: elaborated-type-specifier declares new class
};

template <typename T> class R {
  friend T;
};

R<C> rc;                        // class C is a friend of R<C>
R<int> Ri;                      // OK: "friend int;" is ignored
```

— *end example*]

A function first declared in a friend declaration has the linkage of the
namespace of which it is a member ([[basic.link]]). Otherwise, the
function retains its previous linkage ([[dcl.stc]]).

When a `friend` declaration refers to an overloaded name or operator,
only the function specified by the parameter types becomes a friend. A
member function of a class `X` can be a friend of a class `Y`.

[*Example 6*:

``` cpp
class Y {
  friend char* X::foo(int);
  friend X::X(char);            // constructors can be friends
  friend X::~X();               // destructors can be friends
};
```

— *end example*]

A function can be defined in a friend declaration of a class if and only
if the class is a non-local class ([[class.local]]), the function name
is unqualified, and the function has namespace scope.

[*Example 7*:

``` cpp
class M {
  friend void f() { }           // definition of global f, a friend of M,
                                // not the definition of a member function
};
```

— *end example*]

Such a function is implicitly an inline function ([[dcl.inline]]). A
`friend` function defined in a class is in the (lexical) scope of the
class in which it is defined. A friend function defined outside the
class is not ([[basic.lookup.unqual]]).

No *storage-class-specifier* shall appear in the *decl-specifier-seq* of
a friend declaration.

A name nominated by a friend declaration shall be accessible in the
scope of the class containing the friend declaration. The meaning of the
friend declaration is the same whether the friend declaration appears in
the `private`, `protected` or `public` ([[class.mem]]) portion of the
class *member-specification*.

Friendship is neither inherited nor transitive.

[*Example 8*:

``` cpp
class A {
  friend class B;
  int a;
};

class B {
  friend class C;
};

class C  {
  void f(A* p) {
    p->a++;         // error: C is not a friend of A despite being a friend of a friend
  }
};

class D : public B  {
  void f(A* p) {
    p->a++;         // error: D is not a friend of A despite being derived from a friend
  }
};
```

— *end example*]

If a friend declaration appears in a local class ([[class.local]]) and
the name specified is an unqualified name, a prior declaration is looked
up without considering scopes that are outside the innermost enclosing
non-class scope. For a friend function declaration, if there is no prior
declaration, the program is ill-formed. For a friend class declaration,
if there is no prior declaration, the class that is specified belongs to
the innermost enclosing non-class scope, but if it is subsequently
referenced, its name is not found by name lookup until a matching
declaration is provided in the innermost enclosing non-class scope.

[*Example 9*:

``` cpp
class X;
void a();
void f() {
  class Y;
  extern void b();
  class A {
  friend class X;   // OK, but X is a local class, not ::X
  friend class Y;   // OK
  friend class Z;   // OK, introduces local class Z
  friend void a();  // error, ::a is not considered
  friend void b();  // OK
  friend void c();  // error
  };
  X* px;            // OK, but ::X is found
  Z* pz;            // error, no Z is found
}
```

— *end example*]

## Protected member access <a id="class.protected">[[class.protected]]</a>

An additional access check beyond those described earlier in Clause 
[[class.access]] is applied when a non-static data member or non-static
member function is a protected member of its naming class (
[[class.access.base]])[^9] As described earlier, access to a protected
member is granted because the reference occurs in a friend or member of
some class `C`. If the access is to form a pointer to member (
[[expr.unary.op]]), the *nested-name-specifier* shall denote `C` or a
class derived from `C`. All other accesses involve a (possibly implicit)
object expression ([[expr.ref]]). In this case, the class of the object
expression shall be `C` or a class derived from `C`.

[*Example 1*:

``` cpp
class B {
protected:
  int i;
  static int j;
};

class D1 : public B {
};

class D2 : public B {
  friend void fr(B*,D1*,D2*);
  void mem(B*,D1*);
};

void fr(B* pb, D1* p1, D2* p2) {
  pb->i = 1;                    // ill-formed
  p1->i = 2;                    // ill-formed
  p2->i = 3;                    // OK (access through a D2)
  p2->B::i = 4;                 // OK (access through a D2, even though naming class is B)
  int B::* pmi_B = &B::i;       // ill-formed
  int B::* pmi_B2 = &D2::i;     // OK (type of &D2::i is int B::*)
  B::j = 5;                     // ill-formed (not a friend of naming class B)
  D2::j = 6;                    // OK (because refers to static member)
}

void D2::mem(B* pb, D1* p1) {
  pb->i = 1;                    // ill-formed
  p1->i = 2;                    // ill-formed
  i = 3;                        // OK (access through this)
  B::i = 4;                     // OK (access through this, qualification ignored)
  int B::* pmi_B = &B::i;       // ill-formed
  int B::* pmi_B2 = &D2::i;     // OK
  j = 5;                        // OK (because j refers to static member)
  B::j = 6;                     // OK (because B::j refers to static member)
}

void g(B* pb, D1* p1, D2* p2) {
  pb->i = 1;                    // ill-formed
  p1->i = 2;                    // ill-formed
  p2->i = 3;                    // ill-formed
}
```

— *end example*]

## Access to virtual functions <a id="class.access.virt">[[class.access.virt]]</a>

The access rules (Clause  [[class.access]]) for a virtual function are
determined by its declaration and are not affected by the rules for a
function that later overrides it.

[*Example 1*:

``` cpp
class B {
public:
  virtual int f();
};

class D : public B {
private:
  int f();
};

void f() {
  D d;
  B* pb = &d;
  D* pd = &d;

  pb->f();                      // OK: B::f() is public, D::f() is invoked
  pd->f();                      // error: D::f() is private
}
```

— *end example*]

Access is checked at the call point using the type of the expression
used to denote the object for which the member function is called (`B*`
in the example above). The access of the member function in the class in
which it was defined (`D` in the example above) is in general not known.

## Multiple access <a id="class.paths">[[class.paths]]</a>

If a name can be reached by several paths through a multiple inheritance
graph, the access is that of the path that gives most access.

[*Example 1*:

``` cpp
class W { public: void f(); };
class A : private virtual W { };
class B : public virtual W { };
class C : public A, public B {
  void f() { W::f(); }          // OK
};
```

Since `W::f()` is available to `C::f()` along the public path through
`B`, access is allowed.

— *end example*]

## Nested classes <a id="class.access.nest">[[class.access.nest]]</a>

A nested class is a member and as such has the same access rights as any
other member. The members of an enclosing class have no special access
to members of a nested class; the usual access rules (Clause 
[[class.access]]) shall be obeyed.

[*Example 1*:

``` cpp
class E {
  int x;
  class B { };

  class I {
    B b;                        // OK: E::I can access E::B
    int y;
    void f(E* p, int i) {
      p->x = i;                 // OK: E::I can access E::x
    }
  };

  int g(I* p) {
    return p->y;                // error: I::y is private
  }
};
```

— *end example*]

<!-- Link reference definitions -->
[basic.compound]: basic.md#basic.compound
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.elab]: basic.md#basic.lookup.elab
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.scope]: basic.md#basic.scope
[basic.scope.class]: basic.md#basic.scope.class
[basic.scope.hiding]: basic.md#basic.scope.hiding
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.static]: basic.md#basic.start.static
[basic.start.term]: basic.md#basic.start.term
[basic.stc]: basic.md#basic.stc
[basic.types]: basic.md#basic.types
[c.strings]: strings.md#c.strings
[class]: #class
[class.abstract]: #class.abstract
[class.access]: #class.access
[class.access.base]: #class.access.base
[class.access.nest]: #class.access.nest
[class.access.spec]: #class.access.spec
[class.access.virt]: #class.access.virt
[class.base.init]: special.md#class.base.init
[class.bit]: #class.bit
[class.cdtor]: special.md#class.cdtor
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.derived]: #class.derived
[class.dtor]: special.md#class.dtor
[class.free]: special.md#class.free
[class.friend]: #class.friend
[class.local]: #class.local
[class.mem]: #class.mem
[class.member.lookup]: #class.member.lookup
[class.mfct]: #class.mfct
[class.mfct.non-static]: #class.mfct.non-static
[class.mi]: #class.mi
[class.name]: #class.name
[class.nest]: #class.nest
[class.nested.type]: #class.nested.type
[class.paths]: #class.paths
[class.protected]: #class.protected
[class.static]: #class.static
[class.static.data]: #class.static.data
[class.static.mfct]: #class.static.mfct
[class.this]: #class.this
[class.union]: #class.union
[class.union.anon]: #class.union.anon
[class.virtual]: #class.virtual
[conv.mem]: conv.md#conv.mem
[conv.ptr]: conv.md#conv.ptr
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.fct.spec]: dcl.md#dcl.fct.spec
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.inline]: dcl.md#dcl.inline
[dcl.stc]: dcl.md#dcl.stc
[dcl.type.cv]: dcl.md#dcl.type.cv
[dcl.type.elab]: dcl.md#dcl.type.elab
[dcl.typedef]: dcl.md#dcl.typedef
[depr.static_constexpr]: future.md#depr.static_constexpr
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.const]: expr.md#expr.const
[expr.eq]: expr.md#expr.eq
[expr.prim]: expr.md#expr.prim
[expr.prim.this]: expr.md#expr.prim.this
[expr.ref]: expr.md#expr.ref
[expr.static.cast]: expr.md#expr.static.cast
[expr.unary.op]: expr.md#expr.unary.op
[fig:nonvirt]: #fig:nonvirt
[fig:virt]: #fig:virt
[fig:virtnonvirt]: #fig:virtnonvirt
[intro.object]: intro.md#intro.object
[namespace.def]: dcl.md#namespace.def
[namespace.udecl]: dcl.md#namespace.udecl
[over]: over.md#over
[over.ass]: over.md#over.ass
[over.load]: over.md#over.load
[over.match]: over.md#over.match
[over.match.call]: over.md#over.match.call
[over.match.funcs]: over.md#over.match.funcs
[over.oper]: over.md#over.oper
[string.classes]: strings.md#string.classes
[temp]: temp.md#temp
[temp.arg]: temp.md#temp.arg
[temp.dep.type]: temp.md#temp.dep.type
[temp.friend]: temp.md#temp.friend
[temp.inst]: temp.md#temp.inst
[temp.mem]: temp.md#temp.mem
[temp.param]: temp.md#temp.param
[temp.spec]: temp.md#temp.spec
[temp.variadic]: temp.md#temp.variadic

[^1]: Base class subobjects are not so constrained.

[^2]: This ensures that two subobjects that have the same class type and
    that belong to the same most derived object are not allocated at the
    same address ([[expr.eq]]).

[^3]: The acronym POD stands for “plain old data”.

[^4]: See, for example, `<cstring>` ([[c.strings]]).

[^5]: A function with the same name but a different parameter list
    (Clause  [[over]]) as a virtual function is not necessarily virtual
    and does not override. The use of the `virtual` specifier in the
    declaration of an overriding function is legal but redundant (has
    empty semantics). Access control (Clause  [[class.access]]) is not
    considered in determining overriding.

[^6]: Multi-level pointers to classes or references to multi-level
    pointers to classes are not allowed.

[^7]: Access permissions are thus transitive and cumulative to nested
    and local classes.

[^8]: As specified previously in Clause  [[class.access]], private
    members of a base class remain inaccessible even to derived classes
    unless `friend` declarations within the base class definition are
    used to grant access explicitly.

[^9]: This additional check does not apply to other members, e.g.,
    static data members or enumerator member constants.
