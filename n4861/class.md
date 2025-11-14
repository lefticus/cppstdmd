# Classes <a id="class">[[class]]</a>

## Preamble <a id="class.pre">[[class.pre]]</a>

A class is a type. Its name becomes a *class-name* [[class.name]] within
its scope.

``` bnf
class-name:
    identifier
    simple-template-id
```

A *class-specifier* or an *elaborated-type-specifier* [[dcl.type.elab]]
is used to make a *class-name*. An object of a class consists of a
(possibly empty) sequence of members and base class objects.

``` bnf
class-specifier:
    class-head \terminal{\ member-specificationₒₚₜ \terminal{\}}
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
    final
```

``` bnf
class-key:
    class
    struct
    union
```

A class declaration where the *class-name* in the *class-head-name* is a
*simple-template-id* shall be an explicit specialization
[[temp.expl.spec]] or a partial specialization [[temp.class.spec]]. A
*class-specifier* whose *class-head* omits the *class-head-name* defines
an unnamed class.

[*Note 1*: An unnamed class thus can’t be `final`. — *end note*]

A *class-name* is inserted into the scope in which it is declared
immediately after the *class-name* is seen. The *class-name* is also
inserted into the scope of the class itself; this is known as the
*injected-class-name*. For purposes of access checking, the
injected-class-name is treated as if it were a public member name. A
*class-specifier* is commonly referred to as a *class
definition*. A class is considered defined after the closing brace of
its *class-specifier* has been seen even though its member functions are
in general not yet defined. The optional *attribute-specifier-seq*
appertains to the class; the attributes in the *attribute-specifier-seq*
are thereafter considered attributes of the class whenever it is named.

If a *class-head-name* contains a *nested-name-specifier*, the
*class-specifier* shall refer to a class that was previously declared
directly in the class or namespace to which the *nested-name-specifier*
refers, or in an element of the inline namespace set [[namespace.def]]
of that namespace (i.e., not merely inherited or introduced by a
*using-declaration*), and the *class-specifier* shall appear in a
namespace enclosing the previous declaration. In such cases, the
*nested-name-specifier* of the *class-head-name* of the definition shall
not begin with a *decltype-specifier*.

[*Note 2*: The *class-key* determines whether the class is a union
[[class.union]] and whether access is public or private by default
[[class.access]]. A union holds the value of at most one data member at
a time. — *end note*]

If a class is marked with the *class-virt-specifier* `final` and it
appears as a *class-or-decltype* in a *base-clause* [[class.derived]],
the program is ill-formed. Whenever a *class-key* is followed by a
*class-head-name*, the *identifier* `final`, and a colon or left brace,
`final` is interpreted as a *class-virt-specifier*.

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

[*Note 3*: Complete objects of class type have nonzero size. Base class
subobjects and members declared with the `no_unique_address` attribute
[[dcl.attr.nouniqueaddr]] are not so constrained. — *end note*]

[*Note 4*: Class objects can be assigned ([[over.ass]],
[[class.copy.assign]]), passed as arguments to functions ([[dcl.init]],
[[class.copy.ctor]]), and returned by functions (except objects of
classes for which copying or moving has been restricted; see 
[[dcl.fct.def.delete]] and [[class.access]]). Other plausible operators,
such as equality comparison, can be defined by the user; see 
[[over.oper]]. — *end note*]

## Properties of classes <a id="class.prop">[[class.prop]]</a>

A *trivially copyable class* is a class:

- that has at least one eligible copy constructor, move constructor,
  copy assignment operator, or move assignment operator ([[special]],
  [[class.copy.ctor]], [[class.copy.assign]]),
- where each eligible copy constructor, move constructor, copy
  assignment operator, and move assignment operator is trivial, and
- that has a trivial, non-deleted destructor [[class.dtor]].

A *trivial class* is a class that is trivially copyable and has one or
more eligible default constructors [[class.default.ctor]], all of which
are trivial.

[*Note 1*: In particular, a trivially copyable or trivial class does
not have virtual functions or virtual base classes. — *end note*]

A class `S` is a *standard-layout class* if it:

- has no non-static data members of type non-standard-layout class (or
  array of such types) or reference,
- has no virtual functions [[class.virtual]] and no virtual base classes
  [[class.mi]],
- has the same access control [[class.access]] for all non-static data
  members,
- has no non-standard-layout base classes,
- has at most one base class subobject of any given type,
- has all non-static data members and bit-fields in the class and its
  base classes first declared in the same class, and
- has no element of the set M(S) of types as a base class, where for any
  type `X`, M(X) is defined as follows.[^1]
  \[*Note 1*: M(X) is the set of the types of all non-base-class
  subobjects that may be at a zero offset in `X`. — *end note*]
  - If `X` is a non-union class type with no (possibly inherited
    [[class.derived]]) non-static data members, the set M(X) is empty.
  - If `X` is a non-union class type with a non-static data member of
    type X₀ that is either of zero size or is the first non-static data
    member of `X` (where said member may be an anonymous union), the set
    M(X) consists of X₀ and the elements of M(X₀).
  - If `X` is a union type, the set M(X) is the union of all M(Uᵢ) and
    the set containing all Uᵢ, where each Uᵢ is the type of the iᵗʰ
    non-static data member of `X`.
  - If `X` is an array type with element type Xₑ, the set M(X) consists
    of Xₑ and the elements of M(Xₑ).
  - If `X` is a non-class, non-array type, the set M(X) is empty.

[*Example 1*:

``` cpp
struct B { int i; };            // standard-layout class
struct C : B { };               // standard-layout class
struct D : C { };               // standard-layout class
struct E : D { char : 4; };     // not a standard-layout class

struct Q {};
struct S : Q { };
struct T : Q { };
struct U : S, T { };            // not a standard-layout class
```

— *end example*]

A *standard-layout struct* is a standard-layout class defined with the
*class-key* `struct` or the *class-key* `class`. A
*standard-layout union* is a standard-layout class defined with the
*class-key* `union`.

[*Note 2*: Standard-layout classes are useful for communicating with
code written in other programming languages. Their layout is specified
in  [[class.mem]]. — *end note*]

[*Example 2*:

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

[*Note 3*: Aggregates of class type are described in 
[[dcl.init.aggr]]. — *end note*]

A class `S` is an *implicit-lifetime class* if it is an aggregate or has
at least one trivial eligible constructor and a trivial, non-deleted
destructor.

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

declare an overloaded [[over]] function `f()` and not simply a single
function `f()` twice. For the same reason,

``` cpp
struct S { int a; };
struct S { int a; };            // error: double definition
```

is ill-formed because it defines `S` twice.

— *end example*]

A class declaration introduces the class name into the scope where it is
declared and hides any class, variable, function, or other declaration
of that name in an enclosing scope [[basic.scope]]. If a class name is
declared in a scope where a variable, function, or enumerator of the
same name is also declared, then when both declarations are in scope,
the class can be referred to only using an *elaborated-type-specifier*
[[basic.lookup.elab]].

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

Declaration of friends is described in  [[class.friend]], operator
functions in  [[over.oper]].

— *end example*]

— *end note*]

[*Note 2*: An *elaborated-type-specifier* [[dcl.type.elab]] can also be
used as a *type-specifier* as part of a declaration. It differs from a
class declaration in that if a class of the elaborated name is in scope
the elaborated name will refer to it. — *end note*]

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

A *simple-template-id* is only a *class-name* if its *template-name*
names a class template.

## Class members <a id="class.mem">[[class.mem]]</a>

``` bnf
member-specification:
    member-declaration member-specificationₒₚₜ
    access-specifier ':' member-specificationₒₚₜ
```

``` bnf
member-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ member-declarator-listₒₚₜ ';'
    function-definition
    using-declaration
    using-enum-declaration
    static_assert-declaration
    template-declaration
    explicit-specialization
    deduction-guide
    alias-declaration
    opaque-enum-declaration
    empty-declaration
```

``` bnf
member-declarator-list:
    member-declarator
    member-declarator-list ',' member-declarator
```

``` bnf
member-declarator:
    declarator virt-specifier-seqₒₚₜ pure-specifierₒₚₜ
    declarator requires-clause
    declarator brace-or-equal-initializerₒₚₜ
    identifierₒₚₜ attribute-specifier-seqₒₚₜ ':' constant-expression brace-or-equal-initializerₒₚₜ
```

``` bnf
virt-specifier-seq:
    virt-specifier
    virt-specifier-seq virt-specifier
```

``` bnf
virt-specifier:
    override
    final
```

``` bnf
pure-specifier:
    '=' '0'
```

The *member-specification* in a class definition declares the full set
of members of the class; no member can be added elsewhere. A *direct
member* of a class `X` is a member of `X` that was first declared within
the *member-specification* of `X`, including anonymous union objects
[[class.union.anon]] and direct members thereof. Members of a class are
data members, member functions [[class.mfct]], nested types,
enumerators, and member templates [[temp.mem]] and specializations
thereof.

[*Note 1*: A specialization of a static data member template is a
static data member. A specialization of a member function template is a
member function. A specialization of a member class template is a nested
class. — *end note*]

A *member-declaration* does not declare new members of the class if it
is

- a friend declaration [[class.friend]],
- a *static_assert-declaration*,
- a *using-declaration* [[namespace.udecl]], or
- an *empty-declaration*.

For any other *member-declaration*, each declared entity that is not an
unnamed bit-field [[class.bit]] is a member of the class, and each such
*member-declaration* shall either declare at least one member name of
the class or declare at least one unnamed bit-field.

A *data member* is a non-function member introduced by a
*member-declarator*. A *member function* is a member that is a function.
Nested types are classes ([[class.name]], [[class.nest]]) and
enumerations [[dcl.enum]] declared in the class and arbitrary types
declared as members by use of a typedef declaration [[dcl.typedef]] or
*alias-declaration*. The enumerators of an unscoped enumeration
[[dcl.enum]] defined in the class are members of the class.

A data member or member function may be declared `static` in its
*member-declaration*, in which case it is a *static member* (see 
[[class.static]]) (a *static data member* [[class.static.data]] or
*static member function* [[class.static.mfct]], respectively) of the
class. Any other data member or member function is a *non-static member*
(a *non-static data member* or *non-static member function* (
[[class.mfct.non-static]]), respectively).

[*Note 2*: A non-static data member of non-reference type is a member
subobject of a class object [[intro.object]]. — *end note*]

A member shall not be declared twice in the *member-specification*,
except that

- a nested class or member class template can be declared and then later
  defined, and
- an enumeration can be introduced with an *opaque-enum-declaration* and
  later redeclared with an *enum-specifier*.

[*Note 3*: A single name can denote several member functions provided
their types are sufficiently different [[over.load]]. — *end note*]

A *complete-class context* of a class is a

- function body [[dcl.fct.def.general]],
- default argument [[dcl.fct.default]],
- *noexcept-specifier* [[except.spec]], or
- default member initializer

within the *member-specification* of the class.

[*Note 4*: A complete-class context of a nested class is also a
complete-class context of any enclosing class, if the nested class is
defined within the *member-specification* of the enclosing
class. — *end note*]

A class is considered a completely-defined object type [[basic.types]]
(or complete type) at the closing `}` of the *class-specifier*. The
class is regarded as complete within its complete-class contexts;
otherwise it is regarded as incomplete within its own class
*member-specification*.

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

In a *member-declarator* for a bit-field, the *constant-expression* is
parsed as the longest sequence of tokens that could syntactically form a
*constant-expression*.

[*Example 2*:

``` cpp
int a;
const int b = 0;
struct S {
  int x1 : 8 = 42;              // OK, "= 42" is brace-or-equal-initializer
  int x2 : 8 { 42 };            // OK, "{ 42 \"} is brace-or-equal-initializer
  int y1 : true ? 8 : a = 42;   // OK, brace-or-equal-initializer is absent
  int y2 : true ? 8 : b = 42;   // error: cannot assign to const int
  int y3 : (true ? 8 : b) = 42; // OK, "= 42" is brace-or-equal-initializer
  int z : 1 || new int { 0 };   // OK, brace-or-equal-initializer is absent
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
after a *class-specifier* or an *enum-specifier* or in a friend
declaration [[class.friend]]. A *pure-specifier* shall be used only in
the declaration of a virtual function [[class.virtual]] that is not a
friend declaration.

The optional *attribute-specifier-seq* in a *member-declaration*
appertains to each of the entities declared by the *member-declarator*s;
it shall not appear if the optional *member-declarator-list* is omitted.

A *virt-specifier-seq* shall contain at most one of each
*virt-specifier*. A *virt-specifier-seq* shall appear only in the first
declaration of a virtual member function [[class.virtual]].

The type of a non-static data member shall not be an incomplete type
[[basic.types]], an abstract class type [[class.abstract]], or a
(possibly multi-dimensional) array thereof.

[*Note 5*: In particular, a class `C` cannot contain a non-static
member of class `C`, but it can contain a pointer or reference to an
object of class `C`. — *end note*]

[*Note 6*: See  [[expr.prim.id]] for restrictions on the use of
non-static data members and non-static member functions. — *end note*]

[*Note 7*: The type of a non-static member function is an ordinary
function type, and the type of a non-static data member is an ordinary
object type. There are no special member function types or data member
types. — *end note*]

[*Example 3*:

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

[*Note 8*:  Non-static data members of a (non-union) class with the
same access control [[class.access]] and non-zero size [[intro.object]]
are allocated so that later members have higher addresses within a class
object. The order of allocation of non-static data members with
different access control is unspecified. Implementation alignment
requirements might cause two adjacent members not to be allocated
immediately after each other; so might requirements for space for
managing virtual functions [[class.virtual]] and virtual base classes
[[class.mi]]. — *end note*]

If `T` is the name of a class, then each of the following shall have a
name different from `T`:

- every static data member of class `T`;
- every member function of class `T` \[*Note 2*: This restriction does
  not apply to constructors, which do not have names
  [[class.ctor]] — *end note*] ;
- every member of class `T` that is itself a type;
- every member template of class `T`;
- every enumerator of every member of class `T` that is an unscoped
  enumerated type; and
- every member of every anonymous union that is a member of class `T`.

In addition, if class `T` has a user-declared constructor
[[class.ctor]], every non-static data member of class `T` shall have a
name different from `T`.

The *common initial sequence* of two standard-layout struct
[[class.prop]] types is the longest sequence of non-static data members
and bit-fields in declaration order, starting with the first such entity
in each of the structs, such that corresponding entities have
layout-compatible types, either both entities are declared with the
`no_unique_address` attribute [[dcl.attr.nouniqueaddr]] or neither is,
and either both entities are bit-fields with the same width or neither
is a bit-field.

[*Example 4*:

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

Two standard-layout struct [[class.prop]] types are
*layout-compatible classes* if their common initial sequence comprises
all members and bit-fields of both classes [[basic.types]].

Two standard-layout unions are layout-compatible if they have the same
number of non-static data members and corresponding non-static data
members (in any order) have layout-compatible types [[basic.types]].

In a standard-layout union with an active member [[class.union]] of
struct type `T1`, it is permitted to read a non-static data member `m`
of another union member of struct type `T2` provided `m` is part of the
common initial sequence of `T1` and `T2`; the behavior is as if the
corresponding member of `T1` were nominated.

[*Example 5*:

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

[*Note 9*: Reading a volatile object through a glvalue of non-volatile
type has undefined behavior [[dcl.type.cv]]. — *end note*]

If a standard-layout class object has any non-static data members, its
address is the same as the address of its first non-static data member
if that member is not a bit-field. Its address is also the same as the
address of each of its base class subobjects.

[*Note 10*: There might therefore be unnamed padding within a
standard-layout struct object inserted by an implementation, but not at
its beginning, as necessary to achieve appropriate
alignment. — *end note*]

[*Note 11*: The object and its first subobject are
pointer-interconvertible ([[basic.compound]],
[[expr.static.cast]]). — *end note*]

### Member functions <a id="class.mfct">[[class.mfct]]</a>

A member function may be defined [[dcl.fct.def]] in its class
definition, in which case it is an inline [[dcl.inline]] member function
if it is attached to the global module, or it may be defined outside of
its class definition if it has already been declared but not defined in
its class definition.

[*Note 1*: A member function is also inline if it is declared `inline`,
`constexpr`, or `consteval`. — *end note*]

A member function definition that appears outside of the class
definition shall appear in a namespace scope enclosing the class
definition. Except for member function definitions that appear outside
of a class definition, and except for explicit specializations of member
functions of class templates and member function templates [[temp.spec]]
appearing outside of the class definition, a member function shall not
be redeclared.

[*Note 2*: There can be at most one definition of a non-inline member
function in a program. There may be more than one inline member function
definition in a program. See  [[basic.def.odr]] and 
[[dcl.inline]]. — *end note*]

[*Note 3*: Member functions of a class have the linkage of the name of
the class. See  [[basic.link]]. — *end note*]

If the definition of a member function is lexically outside its class
definition, the member function name shall be qualified by its class
name using the `::` operator.

[*Note 4*: A name used in a member function definition (that is, in the
*parameter-declaration-clause* including the default arguments
[[dcl.fct.default]] or in the member function body) is looked up as
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

[*Note 5*: A `static` local variable or local type in a member function
always refers to the same entity, whether or not the member function is
inline. — *end note*]

Previously declared member functions may be mentioned in friend
declarations.

Member functions of a local class shall be defined inline in their class
definition, if they are defined at all.

[*Note 6*:

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
type, or for an object of a class derived [[class.derived]] from its
class type, using the class member access syntax ([[expr.ref]],
[[over.match.call]]). A non-static member function may also be called
directly using the function call syntax ([[expr.call]],
[[over.match.call]]) from within its class or a class derived from its
class, or a member thereof, as described below.

If a non-static member function of a class `X` is called for an object
that is not of type `X`, or of a type derived from `X`, the behavior is
undefined.

When an *id-expression* [[expr.prim.id]] that is not part of a class
member access syntax [[expr.ref]] and not used to form a pointer to
member [[expr.unary.op]] is used in a member of class `X` in a context
where `this` can be used [[expr.prim.this]], if name lookup
[[basic.lookup]] resolves the name in the *id-expression* to a
non-static non-type member of some class `C`, and if either the
*id-expression* is potentially evaluated or `C` is `X` or a base class
of `X`, the *id-expression* is transformed into a class member access
expression [[expr.ref]] using `(*this)` [[class.this]] as the
*postfix-expression* to the left of the `.` operator.

[*Note 1*: If `C` is not `X` or a base class of `X`, the class member
access expression is ill-formed. — *end note*]

This transformation does not apply in the template definition context
[[temp.dep.type]].

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
not members of the class `tnode` and should be declared elsewhere.[^2]

— *end example*]

A non-static member function may be declared `const`, `volatile`, or
`const` `volatile`. These *cv-qualifier*s affect the type of the `this`
pointer [[class.this]]. They also affect the function type [[dcl.fct]]
of the member function; a member function declared `const` is a *const
member function*, a member function declared `volatile` is a *volatile
member function* and a member function declared `const` `volatile` is a
*const volatile member function*.

[*Example 2*:

``` cpp
struct X {
  void g() const;
  void h() const volatile;
};
```

`X::g` is a const member function and `X::h` is a const volatile member
function.

— *end example*]

A non-static member function may be declared with a *ref-qualifier*
[[dcl.fct]]; see  [[over.match.funcs]].

A non-static member function may be declared virtual [[class.virtual]]
or pure virtual [[class.abstract]].

#### The `this` pointer <a id="class.this">[[class.this]]</a>

In the body of a non-static [[class.mfct]] member function, the keyword
`this` is a prvalue whose value is a pointer to the object for which the
function is called. The type of `this` in a member function whose type
has a *cv-qualifier-seq* cv and whose class is `X` is “pointer to cv
`X`”.

[*Note 1*: Thus in a const member function, the object for which the
function is called is accessed through a const access
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
in a const member function because `this` is a pointer to `const`; that
is, `*this` has `const` type.

— *end example*]

[*Note 2*: Similarly, `volatile` semantics [[dcl.type.cv]] apply in
volatile member functions when accessing the object and its non-static
data members. — *end note*]

A member function whose type has a *cv-qualifier-seq* cv-qualifiercv1
can be called on an object expression [[expr.ref]] of type
cv-qualifiercv2 `T` only if cv-qualifiercv1 is the same as or more
cv-qualified than cv-qualifiercv2 [[basic.type.qualifier]].

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
non-const member function, that is, `s::g()` is less-qualified than the
object expression `y`.

— *end example*]

[*Note 3*: Constructors and destructors cannot be declared `const`,
`volatile`, or `const` `volatile`. However, these functions can be
invoked to create and destroy objects with cv-qualified types; see 
[[class.ctor]] and  [[class.dtor]]. — *end note*]

### Special member functions <a id="special">[[special]]</a>

Default constructors [[class.default.ctor]], copy constructors, move
constructors [[class.copy.ctor]], copy assignment operators, move
assignment operators [[class.copy.assign]], and prospective destructors
[[class.dtor]] are *special member functions*.

[*Note 1*: The implementation will implicitly declare these member
functions for some class types when the program does not explicitly
declare them. The implementation will implicitly define them if they are
odr-used [[basic.def.odr]] or needed for constant evaluation
[[expr.const]]. — *end note*]

An implicitly-declared special member function is declared at the
closing `}` of the *class-specifier*. Programs shall not define
implicitly-declared special member functions.

Programs may explicitly refer to implicitly-declared special member
functions.

[*Example 1*:

A program may explicitly call or form a pointer to member to an
implicitly-declared special member function.

``` cpp
struct A { };                   // implicitly declared A::operator=
struct B : A {
  B& operator=(const B &);
};
B& B::operator=(const B& s) {
  this->A::operator=(s);        // well-formed
  return *this;
}
```

— *end example*]

[*Note 2*: The special member functions affect the way objects of class
type are created, copied, moved, and destroyed, and how values can be
converted to values of other types. Often such special member functions
are called implicitly. — *end note*]

Special member functions obey the usual access rules [[class.access]].

[*Example 2*: Declaring a constructor protected ensures that only
derived classes and friends can create objects using
it. — *end example*]

Two special member functions are of the same kind if:

- they are both default constructors,
- they are both copy or move constructors with the same first parameter
  type, or
- they are both copy or move assignment operators with the same first
  parameter type and the same *cv-qualifier*s and *ref-qualifier*, if
  any.

An *eligible special member function* is a special member function for
which:

- the function is not deleted,
- the associated constraints [[temp.constr]], if any, are satisfied, and
- no special member function of the same kind is more constrained
  [[temp.constr.order]].

For a class, its non-static data members, its non-virtual direct base
classes, and, if the class is not abstract [[class.abstract]], its
virtual base classes are called its *potentially constructed
subobjects*.

A defaulted special member function is *constexpr-compatible* if the
corresponding implicitly-declared special member function would be a
constexpr function.

### Constructors <a id="class.ctor">[[class.ctor]]</a>

A *constructor* is introduced by a declaration whose *declarator* is a
function declarator [[dcl.fct]] of the form

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

where the *ptr-declarator* consists solely of an *id-expression*, an
optional *attribute-specifier-seq*, and optional surrounding
parentheses, and the *id-expression* has one of the following forms:

- in a *member-declaration* that belongs to the *member-specification*
  of a class or class template but is not a friend declaration
  [[class.friend]], the *id-expression* is the injected-class-name
  [[class.pre]] of the immediately-enclosing entity or
- in a declaration at namespace scope or in a friend declaration, the
  *id-expression* is a *qualified-id* that names a constructor
  [[class.qual]].

Constructors do not have names. In a constructor declaration, each
*decl-specifier* in the optional *decl-specifier-seq* shall be `friend`,
`inline`, `constexpr`, or an *explicit-specifier*.

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
however an explicit type conversion using the functional notation
[[expr.type.conv]] will cause a constructor to be called to initialize
an object.

[*Note 1*: The syntax looks like an explicit call of the
constructor. — *end note*]

[*Example 2*:

``` cpp
complex zz = complex(1,2.3);
cprint( complex(7.8,1.2) );
```

— *end example*]

[*Note 2*: For initialization of objects of class type see 
[[class.init]]. — *end note*]

An object created in this way is unnamed.

[*Note 3*:  [[class.temporary]] describes the lifetime of temporary
objects. — *end note*]

[*Note 4*: Explicit constructor calls do not yield lvalues, see 
[[basic.lval]]. — *end note*]

[*Note 5*:  Some language constructs have special semantics when used
during construction; see  [[class.base.init]] and 
[[class.cdtor]]. — *end note*]

A constructor can be invoked for a `const`, `volatile` or `const`
`volatile` object. `const` and `volatile` semantics [[dcl.type.cv]] are
not applied on an object under construction. They come into effect when
the constructor for the most derived object [[intro.object]] ends.

A `return` statement in the body of a constructor shall not specify a
return value. The address of a constructor shall not be taken.

A constructor shall not be a coroutine.

#### Default constructors <a id="class.default.ctor">[[class.default.ctor]]</a>

A *default constructor* for a class `X` is a constructor of class `X`
for which each parameter that is not a function parameter pack has a
default argument (including the case of a constructor with no
parameters). If there is no user-declared constructor for class `X`, a
non-explicit constructor having no parameters is implicitly declared as
defaulted [[dcl.fct.def]]. An implicitly-declared default constructor is
an inline public member of its class.

A defaulted default constructor for class `X` is defined as deleted if:

- `X` is a union that has a variant member with a non-trivial default
  constructor and no variant member of `X` has a default member
  initializer,
- `X` is a non-union class that has a variant member `M` with a
  non-trivial default constructor and no variant member of the anonymous
  union containing `M` has a default member initializer,
- any non-static data member with no default member initializer
  [[class.mem]] is of reference type,
- any non-variant non-static data member of const-qualified type (or
  array thereof) with no *brace-or-equal-initializer* is not
  const-default-constructible [[dcl.init]],
- `X` is a union and all of its variant members are of const-qualified
  type (or array thereof),
- `X` is a non-union class and all members of any anonymous union member
  are of const-qualified type (or array thereof),
- any potentially constructed subobject, except for a non-static data
  member with a *brace-or-equal-initializer*, has class type `M` (or
  array thereof) and either `M` has no default constructor or overload
  resolution [[over.match]] as applied to find `M`’s corresponding
  constructor results in an ambiguity or in a function that is deleted
  or inaccessible from the defaulted default constructor, or
- any potentially constructed subobject has a type with a destructor
  that is deleted or inaccessible from the defaulted default
  constructor.

A default constructor is *trivial* if it is not user-provided and if:

- its class has no virtual functions [[class.virtual]] and no virtual
  base classes [[class.mi]], and
- no non-static data member of its class has a default member
  initializer [[class.mem]], and
- all the direct base classes of its class have trivial default
  constructors, and
- for all the non-static data members of its class that are of class
  type (or array thereof), each such class has a trivial default
  constructor.

Otherwise, the default constructor is *non-trivial*.

A default constructor that is defaulted and not defined as deleted is
*implicitly defined* when it is odr-used [[basic.def.odr]] to create an
object of its class type [[intro.object]], when it is needed for
constant evaluation [[expr.const]], or when it is explicitly defaulted
after its first declaration. The implicitly-defined default constructor
performs the set of initializations of the class that would be performed
by a user-written default constructor for that class with no
*ctor-initializer* [[class.base.init]] and an empty
*compound-statement*. If that user-written default constructor would be
ill-formed, the program is ill-formed. If that user-written default
constructor would satisfy the requirements of a constexpr constructor
[[dcl.constexpr]], the implicitly-defined default constructor is
`constexpr`. Before the defaulted default constructor for a class is
implicitly defined, all the non-user-provided default constructors for
its base classes and its non-static data members are implicitly defined.

[*Note 1*: An implicitly-declared default constructor has an exception
specification [[except.spec]]. An explicitly-defaulted definition might
have an implicit exception specification, see 
[[dcl.fct.def]]. — *end note*]

Default constructors are called implicitly to create class objects of
static, thread, or automatic storage duration ([[basic.stc.static]],
[[basic.stc.thread]], [[basic.stc.auto]]) defined without an initializer
[[dcl.init]], are called to create class objects of dynamic storage
duration [[basic.stc.dynamic]] created by a *new-expression* in which
the *new-initializer* is omitted [[expr.new]], or are called when the
explicit type conversion syntax [[expr.type.conv]] is used. A program is
ill-formed if the default constructor for an object is implicitly used
and the constructor is not accessible [[class.access]].

[*Note 2*:  [[class.base.init]] describes the order in which
constructors for base classes and non-static data members are called and
describes how arguments can be specified for the calls to these
constructors. — *end note*]

#### Copy/move constructors <a id="class.copy.ctor">[[class.copy.ctor]]</a>

A non-template constructor for class `X` is a copy constructor if its
first parameter is of type `X&`, `const X&`, `volatile X&` or
`const volatile X&`, and either there are no other parameters or else
all other parameters have default arguments [[dcl.fct.default]].

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
all other parameters have default arguments [[dcl.fct.default]].

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
initialize an object of type cv `X`.

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
first parameter is of type cv `X` and either there are no other
parameters or else all other parameters have default arguments. A member
function template is never instantiated to produce such a constructor
signature.

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
defined as defaulted [[dcl.fct.def]]. The latter case is deprecated if
the class has a user-declared copy assignment operator or a
user-declared destructor [[depr.impldec]].

The implicitly-declared copy constructor for a class `X` will have the
form

``` cpp
X::X(const X&)
```

if each potentially constructed subobject of a class type `M` (or array
thereof) has a copy constructor whose first parameter is of type `const`
`M&` or `const` `volatile` `M&`.[^3] Otherwise, the implicitly-declared
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

An implicitly-declared copy/move constructor is an inline public member
of its class. A defaulted copy/move constructor for a class `X` is
defined as deleted [[dcl.fct.def.delete]] if `X` has:

- a potentially constructed subobject type `M` (or array thereof) that
  cannot be copied/moved because overload resolution [[over.match]], as
  applied to find `M`’s corresponding constructor, results in an
  ambiguity or a function that is deleted or inaccessible from the
  defaulted constructor,
- a variant member whose corresponding constructor as selected by
  overload resolution is non-trivial,
- any potentially constructed subobject of a type with a destructor that
  is deleted or inaccessible from the defaulted constructor, or,
- for the copy constructor, a non-static data member of rvalue reference
  type.

[*Note 4*: A defaulted move constructor that is defined as deleted is
ignored by overload resolution ([[over.match]], [[over.over]]). Such a
constructor would otherwise interfere with initialization from an rvalue
which can use the copy constructor instead. — *end note*]

A copy/move constructor for class `X` is trivial if it is not
user-provided and if:

- class `X` has no virtual functions [[class.virtual]] and no virtual
  base classes [[class.mi]], and
- the constructor selected to copy/move each direct base class subobject
  is trivial, and
- for each non-static data member of `X` that is of class type (or array
  thereof), the constructor selected to copy/move that member is
  trivial;

otherwise the copy/move constructor is *non-trivial*.

A copy/move constructor that is defaulted and not defined as deleted is
*implicitly defined* when it is odr-used [[basic.def.odr]], when it is
needed for constant evaluation [[expr.const]], or when it is explicitly
defaulted after its first declaration.

[*Note 5*: The copy/move constructor is implicitly defined even if the
implementation elided its odr-use ([[basic.def.odr]],
[[class.temporary]]). — *end note*]

If the implicitly-defined constructor would satisfy the requirements of
a constexpr constructor [[dcl.constexpr]], the implicitly-defined
constructor is `constexpr`.

Before the defaulted copy/move constructor for a class is implicitly
defined, all non-user-provided copy/move constructors for its
potentially constructed subobjects are implicitly defined.

[*Note 6*: An implicitly-declared copy/move constructor has an implied
exception specification [[except.spec]]. — *end note*]

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
object representation [[basic.types]] of `X`. For each object nested
within [[intro.object]] the object that is the source of the copy, a
corresponding object o nested within the destination is identified (if
the object is a subobject) or created (otherwise), and the lifetime of o
begins before the copy is performed.

### Copy/move assignment operator <a id="class.copy.assign">[[class.copy.assign]]</a>

A user-declared *copy* assignment operator `X::operator=` is a
non-static non-template member function of class `X` with exactly one
parameter of type `X`, `X&`, `const X&`, `volatile X&`, or
`const volatile X&`.[^4]

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
as defaulted [[dcl.fct.def]]. The latter case is deprecated if the class
has a user-declared copy constructor or a user-declared destructor
[[depr.impldec]]. The implicitly-declared copy assignment operator for a
class `X` will have the form

``` cpp
X& X::operator=(const X&)
```

if

- each direct base class `B` of `X` has a copy assignment operator whose
  parameter is of type `const B&`, `const volatile B&`, or `B`, and
- for all the non-static data members of `X` that are of a class type
  `M` (or array thereof), each such class type has a copy assignment
  operator whose parameter is of type `const M&`, `const volatile M&`,
  or `M`.[^5]

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
X& X::operator=(X&&)
```

The implicitly-declared copy/move assignment operator for class `X` has
the return type `X&`; it returns the object for which the assignment
operator is invoked, that is, the object assigned to. An
implicitly-declared copy/move assignment operator is an inline public
member of its class.

A defaulted copy/move assignment operator for class `X` is defined as
deleted if `X` has:

- a variant member with a non-trivial corresponding assignment operator
  and `X` is a union-like class, or
- a non-static data member of `const` non-class type (or array thereof),
  or
- a non-static data member of reference type, or
- a direct non-static data member of class type `M` (or array thereof)
  or a direct base class `M` that cannot be copied/moved because
  overload resolution [[over.match]], as applied to find `M`’s
  corresponding assignment operator, results in an ambiguity or a
  function that is deleted or inaccessible from the defaulted assignment
  operator.

[*Note 6*: A defaulted move assignment operator that is defined as
deleted is ignored by overload resolution ([[over.match]],
[[over.over]]). — *end note*]

Because a copy/move assignment operator is implicitly declared for a
class if not declared by the user, a base class copy/move assignment
operator is always hidden by the corresponding assignment operator of a
derived class [[over.ass]]. A *using-declaration* [[namespace.udecl]]
that brings in from a base class an assignment operator with a parameter
type that could be that of a copy/move assignment operator for the
derived class is not considered an explicit declaration of such an
operator and does not suppress the implicit declaration of the derived
class operator; the operator introduced by the *using-declaration* is
hidden by the implicitly-declared operator in the derived class.

A copy/move assignment operator for class `X` is trivial if it is not
user-provided and if:

- class `X` has no virtual functions [[class.virtual]] and no virtual
  base classes [[class.mi]], and
- the assignment operator selected to copy/move each direct base class
  subobject is trivial, and
- for each non-static data member of `X` that is of class type (or array
  thereof), the assignment operator selected to copy/move that member is
  trivial;

otherwise the copy/move assignment operator is *non-trivial*.

A copy/move assignment operator for a class `X` that is defaulted and
not defined as deleted is *implicitly defined* when it is odr-used
[[basic.def.odr]] (e.g., when it is selected by overload resolution to
assign to an object of its class type), when it is needed for constant
evaluation [[expr.const]], or when it is explicitly defaulted after its
first declaration. The implicitly-defined copy/move assignment operator
is `constexpr` if

- `X` is a literal type, and
- the assignment operator selected to copy/move each direct base class
  subobject is a constexpr function, and
- for each non-static data member of `X` that is of class type (or array
  thereof), the assignment operator selected to copy/move that member is
  a constexpr function.

Before the defaulted copy/move assignment operator for a class is
implicitly defined, all non-user-provided copy/move assignment operators
for its direct base classes and its non-static data members are
implicitly defined.

[*Note 7*: An implicitly-declared copy/move assignment operator has an
implied exception specification [[except.spec]]. — *end note*]

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
the object representation [[basic.types]] of `X`. If the source and
destination of the assignment are not the same object, then for each
object nested within [[intro.object]] the object that is the source of
the copy, a corresponding object o nested within the destination is
created, and the lifetime of o begins before the copy is performed.

### Destructors <a id="class.dtor">[[class.dtor]]</a>

A *prospective destructor* is introduced by a declaration whose
*declarator* is a function declarator [[dcl.fct]] of the form

``` bnf
ptr-declarator '(' parameter-declaration-clause ')' noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

where the *ptr-declarator* consists solely of an *id-expression*, an
optional *attribute-specifier-seq*, and optional surrounding
parentheses, and the *id-expression* has one of the following forms:

- in a *member-declaration* that belongs to the *member-specification*
  of a class or class template but is not a friend declaration
  [[class.friend]], the *id-expression* is `~`*class-name* and the
  *class-name* is the injected-class-name [[class.pre]] of the
  immediately-enclosing entity or
- in a declaration at namespace scope or in a friend declaration, the
  *id-expression* is *nested-name-specifier* `~`*class-name* and the
  *class-name* names the same class as the *nested-name-specifier*.

A prospective destructor shall take no arguments [[dcl.fct]]. Each
*decl-specifier* of the *decl-specifier-seq* of a prospective destructor
declaration (if any) shall be `friend`, `inline`, `virtual`,
`constexpr`, or `consteval`.

If a class has no user-declared prospective destructor, a prospective
destructor is implicitly declared as defaulted [[dcl.fct.def]]. An
implicitly-declared prospective destructor is an inline public member of
its class.

An implicitly-declared prospective destructor for a class `X` will have
the form

``` cpp
~X()
```

At the end of the definition of a class, overload resolution is
performed among the prospective destructors declared in that class with
an empty argument list to select the *destructor* for the class, also
known as the *selected destructor*. The program is ill-formed if
overload resolution fails. Destructor selection does not constitute a
reference to, or odr-use [[basic.def.odr]] of, the selected destructor,
and in particular, the selected destructor may be deleted
[[dcl.fct.def.delete]].

The address of a destructor shall not be taken. A destructor can be
invoked for a `const`, `volatile` or `const` `volatile` object. `const`
and `volatile` semantics [[dcl.type.cv]] are not applied on an object
under destruction. They stop being in effect when the destructor for the
most derived object [[intro.object]] starts.

[*Note 1*: A declaration of a destructor that does not have a
*noexcept-specifier* has the same exception specification as if it had
been implicitly declared [[except.spec]]. — *end note*]

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

A defaulted destructor is a constexpr destructor if it satisfies the
requirements for a constexpr destructor [[dcl.constexpr]].

A destructor that is defaulted and not defined as deleted is
*implicitly defined* when it is odr-used [[basic.def.odr]] or when it is
explicitly defaulted after its first declaration.

Before a defaulted destructor for a class is implicitly defined, all the
non-user-provided destructors for its base classes and its non-static
data members are implicitly defined.

A prospective destructor can be declared `virtual` [[class.virtual]] or
pure `virtual` [[class.abstract]]. If the destructor of a class is
virtual and any objects of that class or any derived class are created
in the program, the destructor shall be defined. If a class has a base
class with a virtual destructor, its destructor (whether user- or
implicitly-declared) is virtual.

[*Note 2*:  Some language constructs have special semantics when used
during destruction; see  [[class.cdtor]]. — *end note*]

After executing the body of the destructor and destroying any objects
with automatic storage duration allocated within the body, a destructor
for class `X` calls the destructors for `X`’s direct non-variant
non-static data members, the destructors for `X`’s non-virtual direct
base classes and, if `X` is the most derived class [[class.base.init]],
its destructor calls the destructors for `X`’s virtual base classes. All
destructors are called as if they were referenced with a qualified name,
that is, ignoring any possible virtual overriding destructors in more
derived classes. Bases and members are destroyed in the reverse order of
the completion of their constructor (see  [[class.base.init]]). A
`return` statement [[stmt.return]] in a destructor might not directly
return to the caller; before transferring control to the caller, the
destructors for the members and bases are called. Destructors for
elements of an array are called in reverse order of their construction
(see  [[class.init]]).

A destructor is invoked implicitly

- for a constructed object with static storage duration
  [[basic.stc.static]] at program termination [[basic.start.term]],
- for a constructed object with thread storage duration
  [[basic.stc.thread]] at thread exit,
- for a constructed object with automatic storage duration
  [[basic.stc.auto]] when the block in which an object is created exits
  [[stmt.dcl]],
- for a constructed temporary object when its lifetime ends (
  [[conv.rval]], [[class.temporary]]).

In each case, the context of the invocation is the context of the
construction of the object. A destructor may also be invoked implicitly
through use of a *delete-expression* [[expr.delete]] for a constructed
object allocated by a *new-expression* [[expr.new]]; the context of the
invocation is the *delete-expression*.

[*Note 3*: An array of class type contains several subobjects for each
of which the destructor is invoked. — *end note*]

A destructor can also be invoked explicitly. A destructor is
*potentially invoked* if it is invoked or as specified in  [[expr.new]],
[[stmt.return]], [[dcl.init.aggr]], [[class.base.init]], and 
[[except.throw]]. A program is ill-formed if a destructor that is
potentially invoked is deleted or not accessible from the context of the
invocation.

At the point of definition of a virtual destructor (including an
implicit definition [[class.dtor]]), the non-array deallocation function
is determined as if for the expression `delete this` appearing in a
non-virtual destructor of the destructor’s class (see  [[expr.delete]]).
If the lookup fails or if the deallocation function has a deleted
definition [[dcl.fct.def]], the program is ill-formed.

[*Note 4*: This assures that a deallocation function corresponding to
the dynamic type of an object is available for the *delete-expression*
[[class.free]]. — *end note*]

In an explicit destructor call, the destructor is specified by a `~`
followed by a *type-name* or *decltype-specifier* that denotes the
destructor’s class type. The invocation of a destructor is subject to
the usual rules for member functions [[class.mfct]]; that is, if the
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
member access operator [[expr.ref]] or a *qualified-id*
[[expr.prim.id.qual]]; in particular, the *unary-expression* `~X()` in a
member function is not an explicit destructor call
[[expr.unary.op]]. — *end note*]

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
whose lifetime has ended [[basic.life]].

[*Example 2*: If the destructor for an object with automatic storage
duration is explicitly invoked, and the block is subsequently left in a
manner that would ordinarily invoke implicit destruction of the object,
the behavior is undefined. — *end example*]

[*Note 8*:

The notation for explicit call of a destructor can be used for any
scalar type name [[expr.prim.id.dtor]]. Allowing this makes it possible
to write code without having to know if a destructor exists for a given
type. For example:

``` cpp
typedef int I;
I* p;
p->I::~I();
```

— *end note*]

A destructor shall not be a coroutine.

### Conversions <a id="class.conv">[[class.conv]]</a>

Type conversions of class objects can be specified by constructors and
by conversion functions. These conversions are called
*user-defined conversions* and are used for implicit type conversions
[[conv]], for initialization [[dcl.init]], and for explicit type
conversions ([[expr.type.conv]], [[expr.cast]], [[expr.static.cast]]).

User-defined conversions are applied only where they are unambiguous (
[[class.member.lookup]], [[class.conv.fct]]). Conversions obey the
access control rules [[class.access]]. Access control is applied after
ambiguity resolution [[basic.lookup]].

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
int b = a;          // error: no viable conversion (a.operator X().operator int() not considered)
int c = X(a);       // OK: a.operator X().operator int()
```

— *end example*]

User-defined conversions are used implicitly only if they are
unambiguous. A conversion function in a derived class does not hide a
conversion function in a base class unless the two functions convert to
the same type. Function overload resolution [[over.match.best]] selects
the best conversion function to perform the conversion.

[*Example 2*:

``` cpp
struct X {
  operator int();
};

struct Y : X {
    operator char();
};

void f(Y& a) {
  if (a) {          // error: ambiguous between X::operator int() and Y::operator char()
  }
}
```

— *end example*]

#### Conversion by constructor <a id="class.conv.ctor">[[class.conv.ctor]]</a>

A constructor that is not explicit [[dcl.fct.spec]] specifies a
conversion from the types of its parameters (if any) to the type of its
class. Such a constructor is called a *converting constructor*.

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
constructors, but does so only where the direct-initialization syntax
[[dcl.init]] or where casts ([[expr.static.cast]], [[expr.cast]]) are
explicitly used; see also  [[over.match.copy]]. A default constructor
may be an explicit constructor; such a constructor will be used to
perform default-initialization or value-initialization [[dcl.init]].

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

A non-explicit copy/move constructor [[class.copy.ctor]] is a converting
constructor.

[*Note 2*: An implicitly-declared copy/move constructor is not an
explicit constructor; it may be called for implicit type
conversions. — *end note*]

#### Conversion functions <a id="class.conv.fct">[[class.conv.fct]]</a>

A member function of a class `X` having no parameters with a name of the
form

``` bnf
conversion-function-id:
    operator conversion-type-id
```

``` bnf
conversion-type-id:
    type-specifier-seq conversion-declaratorₒₚₜ
```

``` bnf
conversion-declarator:
    ptr-operator conversion-declaratorₒₚₜ
```

specifies a conversion from `X` to the type specified by the
*conversion-type-id*. Such functions are called *conversion functions*.
A *decl-specifier* in the *decl-specifier-seq* of a conversion function
(if any) shall be neither a *defining-type-specifier* nor `static`. The
type of the conversion function [[dcl.fct]] is “function taking no
parameter returning *conversion-type-id*”. A conversion function is
never used to convert a (possibly cv-qualified) object to the (possibly
cv-qualified) same object type (or a reference to it), to a (possibly
cv-qualified) base class of that type (or a reference to it), or to
cv `void`.[^6]

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

A conversion function may be explicit [[dcl.fct.spec]], in which case it
is only considered as a user-defined conversion for
direct-initialization [[dcl.init]]. Otherwise, user-defined conversions
are not restricted to use in assignments and initializations.

[*Example 2*:

``` cpp
class Y { };
struct Z {
  explicit operator Y() const;
};

void h(Z z) {
  Y y1(z);          // OK: direct-initialization
  Y y2 = z;         // error: no conversion function candidate for copy-initialization
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

A conversion function template shall not have a deduced return type
[[dcl.spec.auto]].

[*Example 5*:

``` cpp
struct S {
  operator auto() const { return 10; }      // OK
  template<class T>
  operator auto() const { return 1.2; }     // error: conversion function template
};
```

— *end example*]

### Static members <a id="class.static">[[class.static]]</a>

A static member `s` of class `X` may be referred to using the
*qualified-id* expression `X::s`; it is not necessary to use the class
member access syntax [[expr.ref]] to refer to a static member. A static
member may be referred to using the class member access syntax, in which
case the object expression is evaluated.

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
in the scope of a class derived [[class.derived]] from its class; in
this case, the static member is referred to as if a *qualified-id*
expression was used, with the *nested-name-specifier* of the
*qualified-id* naming the class scope from which the static member is
referenced.

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

Static members obey the usual class member access rules
[[class.access]]. When used in the declaration of a class member, the
`static` specifier shall only be used in the member declarations that
appear within the *member-specification* of the class definition.

[*Note 1*: It cannot be specified in member declarations that appear in
namespace scope. — *end note*]

#### Static member functions <a id="class.static.mfct">[[class.static.mfct]]</a>

[*Note 1*: The rules described in  [[class.mfct]] apply to static
member functions. — *end note*]

[*Note 2*: A static member function does not have a `this` pointer
[[class.this]]. — *end note*]

A static member function shall not be `virtual`. There shall not be a
static and a non-static member function with the same name and the same
parameter types [[over.load]]. A static member function shall not be
declared `const`, `volatile`, or `const volatile`.

#### Static data members <a id="class.static.data">[[class.static.data]]</a>

A static data member is not part of the subobjects of a class. If a
static data member is declared `thread_local` there is one copy of the
member per thread. If a static data member is not declared
`thread_local` there is one copy of the data member that is shared by
all the objects of the class.

A static data member shall not be `mutable` [[dcl.stc]]. A static data
member shall not be a direct member [[class.mem]] of an unnamed
[[class.pre]] or local [[class.local]] class or of a (possibly
indirectly) nested class [[class.nest]] thereof.

The declaration of a non-inline static data member in its class
definition is not a definition and may be of an incomplete type other
than cv `void`. The definition for a static data member that is not
defined inline in the class definition shall appear in a namespace scope
enclosing the member’s class definition. In the definition at namespace
scope, the name of the static data member shall be qualified by its
class name using the `::` operator. The *initializer* expression in the
definition of a static data member is in the scope of its class
[[basic.scope.class]].

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
is an *assignment-expression* is a constant expression [[expr.const]].
The member shall still be defined in a namespace scope if it is odr-used
[[basic.def.odr]] in the program and the namespace scope definition
shall not contain an *initializer*. An inline static data member may be
defined in the class definition and may specify a
*brace-or-equal-initializer*. If the member is declared with the
`constexpr` specifier, it may be redeclared in namespace scope with no
initializer (this usage is deprecated; see [[depr.static.constexpr]]).
Declarations of other static data members shall not specify a
*brace-or-equal-initializer*.

[*Note 2*: There is exactly one definition of a static data member that
is odr-used [[basic.def.odr]] in a valid program. — *end note*]

[*Note 3*: Static data members of a class in namespace scope have the
linkage of the name of the class [[basic.link]]. — *end note*]

Static data members are initialized and destroyed exactly like non-local
variables ([[basic.start.static]], [[basic.start.dynamic]],
[[basic.start.term]]).

### Bit-fields <a id="class.bit">[[class.bit]]</a>

A *member-declarator* of the form

``` bnf
identifierₒₚₜ attribute-specifier-seqₒₚₜ ':' constant-expression brace-or-equal-initializerₒₚₜ
```

specifies a bit-field. The optional *attribute-specifier-seq* appertains
to the entity being declared. A bit-field shall not be a static member.
A bit-field shall have integral or enumeration type; the bit-field
semantic property is not part of the type of the class member. The
*constant-expression* shall be an integral constant expression with a
value greater than or equal to zero and is called the *width* of the
bit-field. If the width of a bit-field is larger than the width of the
bit-field’s type (or, in case of an enumeration type, of its underlying
type), the extra bits are padding bits [[basic.types]]. Allocation of
bit-fields within a class object is *implementation-defined*. Alignment
of bit-fields is *implementation-defined*. Bit-fields are packed into
some addressable allocation unit.

[*Note 1*: Bit-fields straddle allocation units on some machines and
not on others. Bit-fields are assigned right-to-left on some machines,
left-to-right on others. — *end note*]

A declaration for a bit-field that omits the *identifier* declares an
*unnamed bit-field*. Unnamed bit-fields are not members and cannot be
initialized. An unnamed bit-field shall not be declared with a
cv-qualified type.

[*Note 2*: An unnamed bit-field is useful for padding to conform to
externally-imposed layouts. — *end note*]

As a special case, an unnamed bit-field with a width of zero specifies
alignment of the next bit-field at an allocation unit boundary. Only
when declaring an unnamed bit-field may the width be zero.

The address-of operator `&` shall not be applied to a bit-field, so
there are no pointers to bit-fields. A non-const reference shall not be
bound to a bit-field [[dcl.init.ref]].

[*Note 3*: If the initializer for a reference of type `const` `T&` is
an lvalue that refers to a bit-field, the reference is bound to a
temporary initialized to hold the value of the bit-field; the reference
is not bound to the bit-field directly. See 
[[dcl.init.ref]]. — *end note*]

If a value of integral type (other than `bool`) is stored into a
bit-field of width N and the value would be representable in a
hypothetical signed or unsigned integer type with width N and the same
signedness as the bit-field’s type, the original value and the value of
the bit-field compare equal. If the value `true` or `false` is stored
into a bit-field of type `bool` of any size (including a one bit
bit-field), the original `bool` value and the value of the bit-field
compare equal. If a value of an enumeration type is stored into a
bit-field of the same type and the width is large enough to hold all the
values of that enumeration type [[dcl.enum]], the original value and the
value of the bit-field compare equal.

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
another is called a *nested class*. The name of a nested class is local
to its enclosing class. The nested class is in the scope of its
enclosing class.

[*Note 1*: See  [[expr.prim.id]] for restrictions on the use of
non-static data members and non-static member functions. — *end note*]

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

Like a member function, a friend function [[class.friend]] defined
within a nested class is in the lexical scope of that class; it obeys
the same rules for name binding as a static member function of that
class [[class.static]], but it has no special access rights to members
of an enclosing class.

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

A *union* is a class defined with the *class-key* `union`.

In a union, a non-static data member is *active* if its name refers to
an object whose lifetime has begun and has not ended [[basic.life]]. At
most one of the non-static data members of an object of union type can
be active at any time, that is, the value of at most one of the
non-static data members can be stored in a union at any time.

[*Note 1*: One special guarantee is made in order to simplify the use
of unions: If a standard-layout union contains several standard-layout
structs that share a common initial sequence [[class.mem]], and if a
non-static data member of an object of this standard-layout union type
is active and is one of the standard-layout structs, it is permitted to
inspect the common initial sequence of any of the standard-layout struct
members; see  [[class.mem]]. — *end note*]

The size of a union is sufficient to contain the largest of its
non-static data members. Each non-static data member is allocated as if
it were the sole member of a non-union class.

[*Note 2*: A union object and its non-static data members are
pointer-interconvertible ([[basic.compound]], [[expr.static.cast]]). As
a consequence, all non-static data members of a union object have the
same address. — *end note*]

A union can have member functions (including constructors and
destructors), but it shall not have virtual [[class.virtual]] functions.
A union shall not have base classes. A union shall not be used as a base
class. If a union contains a non-static data member of reference type
the program is ill-formed.

[*Note 3*: Absent default member initializers [[class.mem]], if any
non-static data member of a union has a non-trivial default constructor
[[class.default.ctor]], copy constructor, move constructor
[[class.copy.ctor]], copy assignment operator, move assignment operator
[[class.copy.assign]], or destructor [[class.dtor]], the corresponding
member function of the union must be user-provided or it will be
implicitly deleted [[dcl.fct.def.delete]] for the union. — *end note*]

[*Example 1*:

Consider the following union:

``` cpp
union U {
  int i;
  float f;
  std::string s;
};
```

Since `std::string` [[string.classes]] declares non-trivial versions of
all of the special member functions, `U` will have an implicitly deleted
default constructor, copy/move constructor, copy/move assignment
operator, and destructor. To use `U`, some or all of these member
functions must be user-provided.

— *end example*]

When the left operand of an assignment operator involves a member access
expression [[expr.ref]] that nominates a union member, it may begin the
lifetime of that union member, as described below. For an expression
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
built-in assignment operator [[expr.ass]] or a trivial assignment
operator [[class.copy.assign]], for each element `X` of S(`E1`), if
modification of `X` would have undefined behavior under  [[basic.life]],
an object of the type of `X` is implicitly created in the nominated
storage; no initialization is performed and the beginning of its
lifetime is sequenced after the value computation of the left and right
operands and before the assignment.

[*Note 4*: This ends the lifetime of the previously-active member of
the union, if any [[basic.life]]. — *end note*]

[*Example 2*:

``` cpp
union A { int x; int y[4]; };
struct B { A a; };
union C { B b; int k; };
int f() {
  C c;                  // does not start lifetime of any union member
  c.b.a.y[3] = 4;       // OK: $S($c.b.a.y[3]$)$ contains c.b and c.b.a.y;
                        // creates objects to hold union members c.b and c.b.a.y
  return c.b.a.y[3];    // OK: c.b.a.y refers to newly created object (see [basic.life])
}

struct X { const int a; int b; };
union Y { X x; int k; };
void g() {
  Y y = { { 1, 2 } };   // OK, y.x is active union member[class.mem]
  int n = y.x.a;
  y.k = 4;              // OK: ends lifetime of y.x, y.k is active member of union
  y.x.b = n;            // undefined behavior: y.x.b modified outside its lifetime,
                        // $S($y.x.b$)$ is empty because X's default constructor is deleted,
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

``` bnf
union \terminal{\ member-specification \terminal{\}} \terminal{;}
```

is called an *anonymous union*; it defines an unnamed type and an
unnamed object of that type called an *anonymous union object*. Each
*member-declaration* in the *member-specification* of an anonymous union
shall either define a non-static data member or be a
*static_assert-declaration*. Nested types, anonymous unions, and
functions shall not be declared within an anonymous union. The names of
the members of an anonymous union shall be distinct from the names of
any other entity in the scope in which the anonymous union is declared.
For the purpose of name lookup, after the anonymous union definition,
the members of the anonymous union are considered to have been defined
in the scope in which the anonymous union is declared.

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
shall not have private or protected members [[class.access]]. An
anonymous union shall not have member functions.

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

[*Note 1*: Initialization of unions with no user-declared constructors
is described in  [[dcl.init.aggr]]. — *end note*]

A *union-like class* is a union or a class that has an anonymous union
as a direct member. A union-like class `X` has a set of
*variant members*. If `X` is a union, a non-static data member of `X`
that is not an anonymous union is a variant member of `X`. In addition,
a non-static data member of an anonymous union that is a member of `X`
is also a variant member of `X`. At most one variant member of a union
may have a default member initializer.

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
called a *local class*. The name of a local class is local to its
enclosing scope. The local class is in the scope of the enclosing scope,
and has the same access to names outside the function as does the
enclosing function.

[*Note 1*: A declaration in a local class cannot odr-use
[[basic.def.odr]] a local entity from an enclosing scope. — *end note*]

[*Example 1*:

``` cpp
int x;
void f() {
  static int s;
  int x;
  const int N = 5;
  extern int q();
  int arr[2];
  auto [y, z] = arr;

  struct local {
    int g() { return x; }       // error: odr-use of non-odr-usable variable x
    int h() { return s; }       // OK
    int k() { return ::x; }     // OK
    int l() { return q(); }     // OK
    int m() { return N; }       // OK: not an odr-use
    int* n() { return &N; }     // error: odr-use of non-odr-usable variable N
    int p() { return y; }       // error: odr-use of non-odr-usable structured binding y
  };
}

local* p = 0;                   // error: local not in scope
```

— *end example*]

An enclosing function has no special access to members of the local
class; it obeys the usual access rules [[class.access]]. Member
functions of a local class shall be defined within their class
definition, if they are defined at all.

If class `X` is a local class a nested class `Y` may be declared in
class `X` and later defined in the definition of class `X` or be later
defined in the same scope as the definition of class `X`. A class nested
within a local class is a local class.

[*Note 2*: A local class cannot have static data members
[[class.static.data]]. — *end note*]

## Derived classes <a id="class.derived">[[class.derived]]</a>

A list of base classes can be specified in a class definition using the
notation:

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
    attribute-specifier-seqₒₚₜ class-or-decltype
    attribute-specifier-seqₒₚₜ virtual access-specifierₒₚₜ class-or-decltype
    attribute-specifier-seqₒₚₜ access-specifier virtualₒₚₜ class-or-decltype
```

``` bnf
class-or-decltype:
    nested-name-specifierₒₚₜ type-name
    nested-name-specifier template simple-template-id
    decltype-specifier
```

``` bnf
access-specifier:
    private
    protected
    public
```

The optional *attribute-specifier-seq* appertains to the
*base-specifier*.

A *class-or-decltype* shall denote a (possibly cv-qualified) class type
that is not an incompletely defined class [[class.mem]]; any
cv-qualifiers are ignored. The class denoted by the *class-or-decltype*
of a *base-specifier* is called a *direct base class* for the class
being defined. During the lookup for a base class name, non-type names
are ignored [[basic.scope.hiding]]. A class `B` is a base class of a
class `D` if it is a direct base class of `D` or a direct base class of
one of `D`’s base classes. A class is an *indirect base class* of
another if it is a base class but not a direct base class. A class is
said to be (directly or indirectly) *derived* from its (direct or
indirect) base classes.

[*Note 1*: See [[class.access]] for the meaning of
*access-specifier*. — *end note*]

Unless redeclared in the derived class, members of a base class are also
considered to be members of the derived class. Members of a base class
other than constructors are said to be *inherited* by the derived class.
Constructors of a base class can also be inherited as described in 
[[namespace.udecl]]. Inherited members can be referred to in expressions
in the same manner as other members of the derived class, unless their
names are hidden or ambiguous [[class.member.lookup]].

[*Note 2*: The scope resolution operator `::` [[expr.prim.id.qual]] can
be used to refer to a direct or indirect base member explicitly. This
allows access to a name that has been redeclared in the derived class. A
derived class can itself serve as a base class subject to access
control; see  [[class.access.base]]. A pointer to a derived class can be
implicitly converted to a pointer to an accessible unambiguous base
class [[conv.ptr]]. An lvalue of a derived class type can be bound to a
reference to an accessible unambiguous base class
[[dcl.init.ref]]. — *end note*]

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

A *base-specifier* followed by an ellipsis is a pack expansion
[[temp.variadic]].

The order in which the base class subobjects are allocated in the most
derived object [[intro.object]] is unspecified.

[*Note 3*:

A derived class and its base class subobjects can be represented by a
directed acyclic graph (DAG) where an arrow means “directly derived
from” (see ). An arrow need not have a physical representation in
memory. A DAG of subobjects is often referred to as a “subobject
lattice”.

— *end note*]

[*Note 4*: Initialization of objects representing base classes can be
specified in constructors; see  [[class.base.init]]. — *end note*]

[*Note 5*: A base class subobject might have a layout [[basic.stc]]
different from the layout of a most derived object of the same type. A
base class subobject might have a polymorphic behavior [[class.cdtor]]
different from the polymorphic behavior of a most derived object of the
same type. A base class subobject may be of zero size [[class]];
however, two subobjects that have the same class type and that belong to
the same most derived object must not be allocated at the same address
[[expr.eq]]. — *end note*]

### Multiple base classes <a id="class.mi">[[class.mi]]</a>

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
specified by the semantics of initialization by constructor
[[class.base.init]], cleanup [[class.dtor]], and storage layout (
[[class.mem]], [[class.access.spec]]). — *end note*]

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
class Y : public X, public X { ... };             // error
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
lattice of the most derived class, the most derived object
[[intro.object]] shall contain a corresponding distinct base class
subobject of that type. For each distinct base class that is specified
virtual, the most derived object shall contain a single base class
subobject of that type.

[*Note 4*:

For an object of class type `C`, each distinct occurrence of a
(non-virtual) base class `L` in the class lattice of `C` corresponds
one-to-one with a distinct `L` subobject within the object of type `C`.
Given the class `C` defined above, an object of class `C` will have two
subobjects of class `L` as shown in .

In such lattices, explicit qualification can be used to specify which
subobject is meant. The body of function `C::f` could refer to the
member `next` of each `L` subobject:

``` cpp
void C::f() { A::next = B::next; }      // well-formed
```

Without the `A::` or `B::` qualifiers, the definition of `C::f` above
would be ill-formed because of ambiguity [[class.member.lookup]].

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
`C` will have one subobject of class `V`, as shown in .

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
`B` and the virtual `B` shared by `X` and `Y`, as shown in .

— *end note*]

### Virtual functions <a id="class.virtual">[[class.virtual]]</a>

A non-static member function is a *virtual function* if it is first
declared with the keyword `virtual` or if it overrides a virtual member
function declared in a base class (see below).[^7]

[*Note 1*: Virtual functions support dynamic binding and
object-oriented programming. — *end note*]

A class that declares or inherits a virtual function is called a
*polymorphic class*.[^8]

If a virtual member function `vf` is declared in a class `Base` and in a
class `Derived`, derived directly or indirectly from `Base`, a member
function `vf` with the same name, parameter-type-list [[dcl.fct]],
cv-qualification, and ref-qualifier (or absence of same) as `Base::vf`
is declared, then `Derived::vf` *overrides*[^9] `Base::vf`. For
convenience we say that any virtual function overrides itself. A virtual
member function `C::vf` of a class object `S` is a *final overrider*
unless the most derived class [[intro.object]] of which `S` is a base
class subobject (if any) declares or inherits another member function
that overrides `vf`. In a derived class, if a virtual member function of
a base class subobject has more than one final overrider the program is
ill-formed.

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
  c.f();            // calls B::f, the final overrider
  c.C::f();         // calls A::f because of the using-declaration
}
```

— *end example*]

[*Example 2*:

``` cpp
struct A { virtual void f(); };
struct B : A { };
struct C : A { void f(); };
struct D : B, C { };            // OK: A::f and C::f are the final overriders
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
  void f() const;   // error: D::f attempts to override final B::f
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
  virtual void f(long) override;        // error: wrong signature overriding B::f
  virtual void f(int) override;         // OK
};
```

— *end example*]

A virtual function shall not have a trailing *requires-clause*
[[dcl.decl]].

[*Example 5*:

``` cpp
struct A {
  virtual void f() requires true;       // error: virtual function cannot be constrained[temp.constr.decl]
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
  or both are rvalue references to classes[^10]
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
by the (statically chosen) overridden function [[expr.call]].

[*Example 6*:

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
  B*  p = bp->vf4();            // calls Derived::vf4() and converts the
                                // result to B*
  Derived*  dp = &d;
  D*  q = dp->vf4();            // calls Derived::vf4() and does not
                                // convert the result to B*
  dp->vf2();                    // error: argument mismatch
}
```

— *end example*]

[*Note 3*: The interpretation of the call of a virtual function depends
on the type of the object for which it is called (the dynamic type),
whereas the interpretation of a call of a non-virtual member function
depends only on the type of the pointer or reference denoting that
object (the static type) [[expr.call]]. — *end note*]

[*Note 4*: The `virtual` specifier implies membership, so a virtual
function cannot be a non-member [[dcl.fct.spec]] function. Nor can a
virtual function be a static member, since a virtual function call
relies on a specific object for determining which function to invoke. A
virtual function declared in one class can be declared a friend (
[[class.friend]]) in another class. — *end note*]

A virtual function declared in a class shall be defined, or declared
pure [[class.abstract]] in that class, or both; no diagnostic is
required [[basic.def.odr]].

[*Example 7*:

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
  dp->f();                      // error: ambiguous
}
```

In class `D` above there are two occurrences of class `A` and hence two
occurrences of the virtual member function `A::f`. The final overrider
of `B1::A::f` is `B1::f` and the final overrider of `B2::A::f` is
`B2::f`.

— *end example*]

[*Example 8*:

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

struct Error : VB1, VB2 {       // error
};

struct Okay : VB1, VB2 {
  void f();
};
```

Both `VB1::f` and `VB2::f` override `A::f` but there is no overrider of
both of them in class `Error`. This example is therefore ill-formed.
Class `Okay` is well-formed, however, because `Okay::f` is a final
overrider.

— *end example*]

[*Example 9*:

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

Explicit qualification with the scope operator [[expr.prim.id.qual]]
suppresses the virtual call mechanism.

[*Example 10*:

``` cpp
class B { public: virtual void f(); };
class D : public B { public: void f(); };

void D::f() { ... B::f(); }
```

Here, the function call in `D::f` really does call `B::f` and not
`D::f`.

— *end example*]

A function with a deleted definition [[dcl.fct.def]] shall not override
a function that does not have a deleted definition. Likewise, a function
that does not have a deleted definition shall not override a function
with a deleted definition.

A `consteval` virtual function shall not override a virtual function
that is not `consteval`. A `consteval` virtual function shall not be
overridden by a virtual function that is not `consteval`.

### Abstract classes <a id="class.abstract">[[class.abstract]]</a>

[*Note 1*: The abstract class mechanism supports the notion of a
general concept, such as a `shape`, of which only more concrete
variants, such as `circle` and `square`, can actually be used. An
abstract class can also be used to define an interface for which derived
classes provide a variety of implementations. — *end note*]

A virtual function is specified as a *pure virtual function* by using a
*pure-specifier* [[class.mem]] in the function declaration in the class
definition.

[*Note 2*: Such a function might be inherited: see
below. — *end note*]

A class is an *abstract class* if it has at least one pure virtual
function.

[*Note 3*: An abstract class can be used only as a base class of some
other class; no objects of an abstract class can be created except as
subobjects of a class derived from it ([[basic.def]],
[[class.mem]]). — *end note*]

A pure virtual function need be defined only if called with, or as if
with [[class.dtor]], the *qualified-id* syntax [[expr.prim.id.qual]].

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

[*Note 4*: A function declaration cannot provide both a
*pure-specifier* and a definition. — *end note*]

[*Example 2*:

``` cpp
struct C {
  virtual void f() = 0 { };     // error
};
```

— *end example*]

[*Note 5*: An abstract class type cannot be used as a parameter or
return type of a function being defined [[dcl.fct]] or called
[[expr.call]], except as specified in [[dcl.type.simple]]. Further, an
abstract class type cannot be used as the type of an explicit type
conversion ([[expr.static.cast]], [[expr.reinterpret.cast]],
[[expr.const.cast]]), because the resulting prvalue would be of abstract
class type [[basic.lval]]. However, pointers and references to abstract
class types can appear in such contexts. — *end note*]

A class is abstract if it contains or inherits at least one pure virtual
function for which the final overrider is pure virtual.

[*Example 3*:

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

[*Note 6*: An abstract class can be derived from a class that is not
abstract, and a pure virtual function may override a virtual function
which is not pure. — *end note*]

Member functions can be called from a constructor (or destructor) of an
abstract class; the effect of making a virtual call [[class.virtual]] to
a pure virtual function directly or indirectly for the object being
created (or destroyed) from such a constructor (or destructor) is
undefined.

## Member name lookup <a id="class.member.lookup">[[class.member.lookup]]</a>

Member name lookup determines the meaning of a name (*id-expression*) in
a class scope [[basic.scope.class]]. Name lookup can result in an
ambiguity, in which case the program is ill-formed. For an
*unqualified-id*, name lookup begins in the class scope of `this`; for a
*qualified-id*, name lookup begins in the scope of the
*nested-name-specifier*. Name lookup takes place before access control (
[[basic.lookup]], [[class.access]]).

The following steps define the result of name lookup for a member name
`f` in a class scope `C`.

The *lookup set* for `f` in `C`, called S(f,C), consists of two
component sets: the *declaration set*, a set of members named `f`; and
the *subobject set*, a set of subobjects where declarations of these
members (possibly including *using-declaration*s) were found. In the
declaration set, *using-declaration*s are replaced by the set of
designated members that are not hidden or overridden by members of the
derived class [[namespace.udecl]], and type declarations (including
injected-class-names) are replaced by the types they designate. S(f,C)
is calculated as follows:

If `C` contains a declaration of the name `f`, the declaration set
contains every declaration of `f` declared in `C` that satisfies the
requirements of the language construct in which the lookup occurs.

[*Note 1*: Looking up a name in an *elaborated-type-specifier*
[[basic.lookup.elab]] or *base-specifier* [[class.derived]], for
instance, ignores all non-type declarations, while looking up a name in
a *nested-name-specifier* [[basic.lookup.qual]] ignores function,
variable, and enumerator declarations. As another example, looking up a
name in a *using-declaration* [[namespace.udecl]] includes the
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
resolution [[over.match]] also takes place before access control.
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
  pd->a++;          // error: ambiguous: two a{s} in D
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

As illustrated in , the names declared in `V` and the left-hand instance
of `W` are hidden by those in `B`, but the names declared in the
right-hand instance of `W` are not hidden at all.

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
  A* pa = &d;       // error: ambiguous: C's A or B's A?
  V* pv = &d;       // OK: only one V subobject
}
```

— *end example*]

[*Note 4*: Even if the result of name lookup is unambiguous, use of a
name found in multiple subobjects might still be ambiguous (
[[conv.mem]], [[expr.ref]], [[class.access.base]]). — *end note*]

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

## Member access control <a id="class.access">[[class.access]]</a>

A member of a class can be

- private; that is, its name can be used only by members and friends of
  the class in which it is declared.
- protected; that is, its name can be used only by members and friends
  of the class in which it is declared, by classes derived from that
  class, and by their friends (see  [[class.protected]]).
- public; that is, its name can be used anywhere without access
  restriction.

A member of a class can also access all the names to which the class has
access. A local class of a member function may access the same names
that the member function itself may access.[^11]

Members of a class defined with the keyword `class` are `private` by
default. Members of a class defined with the keywords `struct` or
`union` are public by default.

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

[*Note 1*: Access control applies to names nominated by friend
declarations [[class.friend]] and *using-declaration*s
[[namespace.udecl]]. — *end note*]

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

[*Note 3*: Access to members and base classes is controlled, not their
visibility [[basic.scope.hiding]]. Names of members are still visible,
and implicit conversions to base classes are still considered, when
those members and base classes are inaccessible. — *end note*]

The interpretation of a given construct is established without regard to
access control. If the interpretation established makes use of
inaccessible member names or base classes, the construct is ill-formed.

All access controls in [[class.access]] affect the ability to access a
class member name from the declaration of a particular entity, including
parts of the declaration preceding the name of the entity being declared
and, if the entity is a class, the definitions of members of the class
appearing outside the class’s *member-specification*.

[*Note 4*: This access also applies to implicit references to
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

The names in a default argument [[dcl.fct.default]] are bound at the
point of declaration, and access is checked at that point rather than at
any points of use of the default argument. Access checking for default
arguments in function templates and in member functions of class
templates is performed as described in  [[temp.inst]].

The names in a default *template-argument* [[temp.param]] have their
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

### Access specifiers <a id="class.access.spec">[[class.access.spec]]</a>

Member declarations can be labeled by an *access-specifier* (
[[class.derived]]):

``` bnf
access-specifier ':' member-specificationₒₚₜ
```

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
data members is specified in  [[expr.rel]]. — *end note*]

When a member is redeclared within its class definition, the access
specified at its redeclaration shall be the same as at its initial
declaration.

[*Example 3*:

``` cpp
struct S {
  class A;
  enum E : int;
private:
  class A { };                  // error: cannot change access
  enum E: int { e0 };           // error: cannot change access
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

### Accessibility of base classes and base class members <a id="class.access.base">[[class.access.base]]</a>

If a class is declared to be a base class [[class.derived]] for another
class using the `public` access specifier, the public members of the
base class are accessible as public members of the derived class and
protected members of the base class are accessible as protected members
of the derived class. If a class is declared to be a base class for
another class using the `protected` access specifier, the public and
protected members of the base class are accessible as protected members
of the derived class. If a class is declared to be a base class for
another class using the `private` access specifier, the public and
protected members of the base class are accessible as private members of
the derived class.[^12]

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
conversions [[conv.ptr]] and explicit casts ([[expr.type.conv]],
[[expr.static.cast]], [[expr.cast]]), a conversion from a pointer to a
derived class to a pointer to an inaccessible base class might be
ill-formed if an implicit conversion is used, but well-formed if an
explicit cast is used. For example,

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
used, or implicit, e.g., when a class member access operator
[[expr.ref]] is used (including cases where an implicit “`this->`” is
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

### Friends <a id="class.friend">[[class.friend]]</a>

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

A friend declaration that does not declare a function shall have one of
the following forms:

``` bnf
friend elaborated-type-specifier ';'
friend simple-type-specifier ';'
friend typename-specifier ';'
```

[*Note 1*: A friend declaration may be the *declaration* in a
*template-declaration* ([[temp.pre]], [[temp.friend]]). — *end note*]

If the type specifier in a `friend` declaration designates a (possibly
cv-qualified) class type, that class is declared as a friend; otherwise,
the friend declaration is ignored.

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
namespace of which it is a member ([[basic.link]],
[[namespace.memdef]]). Otherwise, the function retains its previous
linkage [[dcl.stc]].

When a friend declaration refers to an overloaded name or operator, only
the function specified by the parameter types becomes a friend. A member
function of a class `X` can be a friend of a class `Y`.

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
if the class is a non-local class [[class.local]], the function name is
unqualified, and the function has namespace scope.

[*Example 7*:

``` cpp
class M {
  friend void f() { }           // definition of global f, a friend of M,
                                // not the definition of a member function
};
```

— *end example*]

Such a function is implicitly an inline [[dcl.inline]] function if it is
attached to the global module. A friend function defined in a class is
in the (lexical) scope of the class in which it is defined. A friend
function defined outside the class is not [[basic.lookup.unqual]].

No *storage-class-specifier* shall appear in the *decl-specifier-seq* of
a friend declaration.

A name nominated by a friend declaration shall be accessible in the
scope of the class containing the friend declaration. The meaning of the
friend declaration is the same whether the friend declaration appears in
the private, protected, or public [[class.mem]] portion of the class
*member-specification*.

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

If a friend declaration appears in a local class [[class.local]] and the
name specified is an unqualified name, a prior declaration is looked up
without considering scopes that are outside the innermost enclosing
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
  Z* pz;            // error: no Z is found
}
```

— *end example*]

### Protected member access <a id="class.protected">[[class.protected]]</a>

An additional access check beyond those described earlier in
[[class.access]] is applied when a non-static data member or non-static
member function is a protected member of its naming class
[[class.access.base]].[^13] As described earlier, access to a protected
member is granted because the reference occurs in a friend or member of
some class `C`. If the access is to form a pointer to member
[[expr.unary.op]], the *nested-name-specifier* shall denote `C` or a
class derived from `C`. All other accesses involve a (possibly implicit)
object expression [[expr.ref]]. In this case, the class of the object
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
  pb->i = 1;                    // error
  p1->i = 2;                    // error
  p2->i = 3;                    // OK (access through a D2)
  p2->B::i = 4;                 // OK (access through a D2, even though naming class is B)
  int B::* pmi_B = &B::i;       // error
  int B::* pmi_B2 = &D2::i;     // OK (type of &D2::i is int B::*)
  B::j = 5;                     // error: not a friend of naming class B
  D2::j = 6;                    // OK (because refers to static member)
}

void D2::mem(B* pb, D1* p1) {
  pb->i = 1;                    // error
  p1->i = 2;                    // error
  i = 3;                        // OK (access through this)
  B::i = 4;                     // OK (access through this, qualification ignored)
  int B::* pmi_B = &B::i;       // error
  int B::* pmi_B2 = &D2::i;     // OK
  j = 5;                        // OK (because j refers to static member)
  B::j = 6;                     // OK (because B::j refers to static member)
}

void g(B* pb, D1* p1, D2* p2) {
  pb->i = 1;                    // error
  p1->i = 2;                    // error
  p2->i = 3;                    // error
}
```

— *end example*]

### Access to virtual functions <a id="class.access.virt">[[class.access.virt]]</a>

The access rules [[class.access]] for a virtual function are determined
by its declaration and are not affected by the rules for a function that
later overrides it.

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

### Multiple access <a id="class.paths">[[class.paths]]</a>

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

### Nested classes <a id="class.access.nest">[[class.access.nest]]</a>

A nested class is a member and as such has the same access rights as any
other member. The members of an enclosing class have no special access
to members of a nested class; the usual access rules [[class.access]]
shall be obeyed.

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

complex a(1);                   // initialized by calling complex(double) with argument 1
complex b = a;                  // initialized as a copy of a
complex c = complex(1,2);       // initialized by calling complex(double,double) with arguments 1 and 2
complex d = sqrt(b,c);          // initialized by calling sqrt(complex,complex) with d as its result object
complex e;                      // initialized by calling complex()
complex f = 3;                  // initialized by calling complex(double) with argument 3
complex g = { 1, 2 };           // initialized by calling complex(double, double) with arguments 1 and 2
```

— *end example*]

[*Note 1*:  Overloading of the assignment operator [[over.ass]] has no
effect on initialization. — *end note*]

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
    mem-initializer '...'ₒₚₜ
    mem-initializer-list ',' mem-initializer '...'ₒₚₜ
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
C::C(): A() { }                 // error: which A?
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
constitutes a full-expression [[intro.execution]]. Any expression in a
*mem-initializer* is evaluated as part of the full-expression that
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
  initializer [[class.mem]] and either
  - the constructor’s class is a union [[class.union]], and no other
    variant member of that union is designated by a *mem-initializer-id*
    or
  - the constructor’s class is not a union, and, if the entity is a
    member of an anonymous union, no other member of that union is
    designated by a *mem-initializer-id*,

  the entity is initialized from its default member initializer as
  specified in  [[dcl.init]];
- otherwise, if the entity is an anonymous union or a variant member
  [[class.union.anon]], no initialization is performed;
- otherwise, the entity is default-initialized [[dcl.init]].

[*Note 3*: An abstract class [[class.abstract]] is never a most derived
class, thus its constructors never initialize virtual base classes,
therefore the corresponding *mem-initializer*s may be
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
constructed subobject of class type is potentially invoked
[[class.dtor]].

[*Note 5*: This provision ensures that destructors can be called for
fully-constructed subobjects in case an exception is thrown
[[except.ctor]]. — *end note*]

In a non-delegating constructor, initialization proceeds in the
following order:

- First, and only for the constructor of the most derived class
  [[intro.object]], virtual base classes are initialized in the order
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
under construction can be the operand of the `typeid` operator
[[expr.typeid]] or of a `dynamic_cast` [[expr.dynamic.cast]]. However,
if these operations are performed in a *ctor-initializer* (or in a
function called directly or indirectly from a *ctor-initializer*) before
all the *mem-initializer*s for base classes have completed, the program
has undefined behavior.

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
  B() : A(f()),     // undefined behavior: calls member function but base A not yet initialized
  j(f()) { }        // well-defined: bases are all initialized
};

class C {
public:
  C(int);
};

class D : public B, C {
  int i;
public:
  D() : C(f()),     // undefined behavior: calls member function but base C not yet initialized
  i(f()) { }        // well-defined: bases are all initialized
};
```

— *end example*]

[*Note 8*:  [[class.cdtor]] describes the result of virtual function
calls, `typeid` and `dynamic_cast`s during construction for the
well-defined cases; that is, describes the polymorphic behavior of an
object under construction. — *end note*]

A *mem-initializer* followed by an ellipsis is a pack expansion
[[temp.variadic]] that initializes the base classes specified by a pack
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
different type `D` (that is, when the constructor was inherited
[[namespace.udecl]]), initialization proceeds as if a defaulted default
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

D1 d1(0);           // error: ambiguous
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

### Construction and destruction <a id="class.cdtor">[[class.cdtor]]</a>

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
int* p1 = &bobj.a;                      // undefined behavior: refers to base class member
int* p2 = &bobj.y.i;                    // undefined behavior: refers to member's member

A* pa = &bobj;                          // undefined behavior: upcast to a base class type
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

During the construction of an object, if the value of the object or any
of its subobjects is accessed through a glvalue that is not obtained,
directly or indirectly, from the constructor’s `this` pointer, the value
of the object or subobject thus obtained is unspecified.

[*Example 2*:

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

[*Example 3*:

``` cpp
struct A { };
struct B : virtual A { };
struct C : B { };
struct D : virtual A { D(A*); };
struct X { X(A*); };

struct E : C, D, X {
  E() : D(this),    // undefined behavior: upcast from E* to A* might use path E* → D* → A*
                    // but D is not constructed

                    // ``D((C*)this)'' would be defined: E* → C* is defined because E() has started,
                    // and C* → A* is defined because C is fully constructed

  X(this) {}        // defined: upon construction of X, C/B/D/A sublattice is fully constructed
};
```

— *end example*]

Member functions, including virtual functions [[class.virtual]], can be
called during construction or destruction [[class.base.init]]. When a
virtual function is called directly or indirectly from a constructor or
from a destructor, including during the construction or destruction of
the class’s non-static data members, and the object to which the call
applies is the object (call it `x`) under construction or destruction,
the function called is the final overrider in the constructor’s or
destructor’s class and not one overriding it in a more-derived class. If
the virtual function call uses an explicit class member access
[[expr.ref]] and the object expression refers to the complete object of
`x` or one of that object’s base class subobjects but not `x` or one of
its base class subobjects, the behavior is undefined.

[*Example 4*:

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
  a->f();           // undefined behavior: a's type not a base of B
}
```

— *end example*]

The `typeid` operator [[expr.typeid]] can be used during construction or
destruction [[class.base.init]]. When `typeid` is used in a constructor
(including the *mem-initializer* or default member initializer
[[class.mem]] for a non-static data member) or in a destructor, or used
in a function called (directly or indirectly) from a constructor or
destructor, if the operand of `typeid` refers to the object under
construction or destruction, `typeid` yields the `std::type_info` object
representing the constructor or destructor’s class. If the operand of
`typeid` refers to the object under construction or destruction and the
static type of the operand is neither the constructor or destructor’s
class nor one of its bases, the behavior is undefined.

`dynamic_cast`s [[expr.dynamic.cast]] can be used during construction or
destruction [[class.base.init]]. When a `dynamic_cast` is used in a
constructor (including the *mem-initializer* or default member
initializer for a non-static data member) or in a destructor, or used in
a function called (directly or indirectly) from a constructor or
destructor, if the operand of the `dynamic_cast` refers to the object
under construction or destruction, this object is considered to be a
most derived object that has the type of the constructor or destructor’s
class. If the operand of the `dynamic_cast` refers to the object under
construction or destruction and the static type of the operand is not a
pointer to or object of the constructor or destructor’s own class or one
of its bases, the `dynamic_cast` results in undefined behavior.

[*Example 5*:

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
  dynamic_cast<B*>(a);          // undefined behavior: a has type A*, A not a base of B
}
```

— *end example*]

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
optimization.[^14] This elision of copy/move operations, called *copy
elision*, is permitted in the following circumstances (which may be
combined to eliminate multiple copies):

- in a `return` statement in a function with a class return type, when
  the *expression* is the name of a non-volatile object with automatic
  storage duration (other than a function parameter or a variable
  introduced by the *exception-declaration* of a *handler*
  [[except.handle]]) with the same type (ignoring cv-qualification) as
  the function return type, the copy/move operation can be omitted by
  constructing the object directly into the function call’s return
  object
- in a *throw-expression* [[expr.throw]], when the operand is the name
  of a non-volatile object with automatic storage duration (other than a
  function or catch-clause parameter) whose scope does not extend beyond
  the end of the innermost enclosing *try-block* (if there is one), the
  copy/move operation can be omitted by constructing the object directly
  into the exception object
- in a coroutine [[dcl.fct.def.coroutine]], a copy of a coroutine
  parameter can be omitted and references to that copy replaced with
  references to the corresponding parameter if the meaning of the
  program will be unchanged except for the execution of a constructor
  and destructor for the parameter copy object
- when the *exception-declaration* of an exception handler
  [[except.pre]] declares an object of the same type (except for
  cv-qualification) as the exception object [[except.throw]], the copy
  operation can be omitted by treating the *exception-declaration* as an
  alias for the exception object if the meaning of the program will be
  unchanged except for the execution of constructors and destructors for
  the object declared by the *exception-declaration*. \[*Note 3*: There
  cannot be a move from the exception object because it is always an
  lvalue. — *end note*]

Copy elision is not permitted where an expression is evaluated in a
context requiring a constant expression [[expr.const]] and in constant
initialization [[basic.start.static]].

[*Note 1*: Copy elision might be performed if the same expression is
evaluated in another context. — *end note*]

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
  A loc;
  return loc;
}

constexpr A a;          // well-formed, a.p points to a
constexpr A b = g();    // error: b.p would be dangling[expr.const]

void h() {
  A c = g();            // well-formed, c.p may point to c or to an ephemeral temporary
}
```

Here the criteria for elision can eliminate the copying of the object
`t` with automatic storage duration into the result object for the
function call `f()`, which is the global object `t2`. Effectively, the
construction of the local object `t` can be viewed as directly
initializing the global object `t2`, and that object’s destruction will
occur at program exit. Adding a move constructor to `Thing` has the same
effect, but it is the move construction from the object with automatic
storage duration to `t2` that is elided.

— *end example*]

An *implicitly movable entity* is a variable of automatic storage
duration that is either a non-volatile object or an rvalue reference to
a non-volatile object type. In the following copy-initialization
contexts, a move operation might be used instead of a copy operation:

- If the *expression* in a `return` [[stmt.return]] or `co_return`
  [[stmt.return.coroutine]] statement is a (possibly parenthesized)
  *id-expression* that names an implicitly movable entity declared in
  the body or *parameter-declaration-clause* of the innermost enclosing
  function or *lambda-expression*, or
- if the operand of a *throw-expression* [[expr.throw]] is a (possibly
  parenthesized) *id-expression* that names an implicitly movable entity
  whose scope does not extend beyond the *compound-statement* of the
  innermost *try-block* or *function-try-block* (if any) whose
  *compound-statement* or *ctor-initializer* encloses the
  *throw-expression*,

overload resolution to select the constructor for the copy or the
`return_value` overload to call is first performed as if the expression
or operand were an rvalue. If the first overload resolution fails or was
not performed, overload resolution is performed again, considering the
expression or operand as an lvalue.

[*Note 2*: This two-stage overload resolution must be performed
regardless of whether copy elision will occur. It determines the
constructor or the `return_value` overload to be called if elision is
not performed, and the selected constructor or `return_value` overload
must be accessible even if the call is elided. — *end note*]

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

[*Example 3*:

``` cpp
template<class T> void g(const T&);

template<class T> void f() {
  T x;
  try {
    T y;
    try { g(x); }
    catch (...) {
      if (/*...*/)
        throw x;        // does not move
      throw y;          // moves
    }
    g(y);
  } catch(...) {
    g(x);
    g(y);               // error: y is not in scope
  }
}
```

— *end example*]

## Comparisons <a id="class.compare">[[class.compare]]</a>

### Defaulted comparison operator functions <a id="class.compare.default">[[class.compare.default]]</a>

A defaulted comparison operator function [[over.binary]] for some class
`C` shall be a non-template function that is

- a non-static const non-volatile member of `C` having one parameter of
  type `const C&` and either no *ref-qualifier* or the *ref-qualifier*
  `&`, or
- a friend of `C` having either two parameters of type `const C&` or two
  parameters of type `C`.

A comparison operator function for class `C` that is defaulted on its
first declaration and is not defined as deleted is *implicitly defined*
when it is odr-used or needed for constant evaluation. Name lookups in
the defaulted definition of a comparison operator function are performed
from a context equivalent to its *function-body*. A definition of a
comparison operator as defaulted that appears in a class shall be the
first declaration of that function.

A defaulted `<=>` or `==` operator function for class `C` is defined as
deleted if any non-static data member of `C` is of reference type or `C`
has variant members [[class.union.anon]].

A binary operator expression `a @ b` is *usable* if either

- `a` or `b` is of class or enumeration type and overload resolution
  [[over.match]] as applied to `a @ b` results in a usable candidate, or
- neither `a` nor `b` is of class or enumeration type and `a @ b` is a
  valid expression.

A defaulted comparison function is *constexpr-compatible* if it
satisfies the requirements for a constexpr function [[dcl.constexpr]]
and no overload resolution performed when determining whether to delete
the function results in a usable candidate that is a non-constexpr
function.

[*Note 1*:

This includes the overload resolutions performed:

- for an `operator<=>` whose return type is not `auto`, when determining
  whether a synthesized three-way comparison is defined,
- for an `operator<=>` whose return type is `auto` or for an
  `operator==`, for a comparison between an element of the expanded list
  of subobjects and itself, or
- for a secondary comparison operator `@`, for the expression `x @ y`.

— *end note*]

If the *member-specification* does not explicitly declare any member or
friend named `operator==`, an `==` operator function is declared
implicitly for each three-way comparison operator function defined as
defaulted in the *member-specification*, with the same access and
*function-definition* and in the same class scope as the respective
three-way comparison operator function, except that the return type is
replaced with `bool` and the *declarator-id* is replaced with
`operator==`.

[*Note 2*: Such an implicitly-declared `==` operator for a class `X` is
defined as defaulted in the definition of `X` and has the same
*parameter-declaration-clause* and trailing *requires-clause* as the
respective three-way comparison operator. It is declared with `friend`,
`virtual`, `constexpr`, or `consteval` if the three-way comparison
operator function is so declared. If the three-way comparison operator
function has no *noexcept-specifier*, the implicitly-declared `==`
operator function has an implicit exception specification
[[except.spec]] that may differ from the implicit exception
specification of the three-way comparison operator
function. — *end note*]

[*Example 1*:

``` cpp
template<typename T> struct X {
  friend constexpr std::partial_ordering operator<=>(X, X) requires (sizeof(T) != 1) = default;
  // implicitly declares: friend constexpr bool operator==(X, X) requires (sizeof(T) != 1) = default;

  [[nodiscard]] virtual std::strong_ordering operator<=>(const X&) const = default;
  // implicitly declares: [[nodiscard]] virtual bool operator==(const X&) const = default;
};
```

— *end example*]

[*Note 3*: The `==` operator function is declared implicitly even if
the defaulted three-way comparison operator function is defined as
deleted. — *end note*]

The direct base class subobjects of `C`, in the order of their
declaration in the *base-specifier-list* of `C`, followed by the
non-static data members of `C`, in the order of their declaration in the
*member-specification* of `C`, form a list of subobjects. In that list,
any subobject of array type is recursively expanded to the sequence of
its elements, in the order of increasing subscript. Let `xᵢ` be an
lvalue denoting the iᵗʰ element in the expanded list of subobjects for
an object `x` (of length n), where `xᵢ` is formed by a sequence of
derived-to-base conversions [[over.best.ics]], class member access
expressions [[expr.ref]], and array subscript expressions [[expr.sub]]
applied to `x`.

### Equality operator <a id="class.eq">[[class.eq]]</a>

A defaulted equality operator function [[over.binary]] shall have a
declared return type `bool`.

A defaulted `==` operator function for a class `C` is defined as deleted
unless, for each `xᵢ` in the expanded list of subobjects for an object
`x` of type `C`, `xᵢ`` == ``xᵢ` is usable [[class.compare.default]].

The return value `V` of a defaulted `==` operator function with
parameters `x` and `y` is determined by comparing corresponding elements
`xᵢ` and `yᵢ` in the expanded lists of subobjects for `x` and `y` (in
increasing index order) until the first index i where `xᵢ`` == ``yᵢ`
yields a result value which, when contextually converted to `bool`,
yields `false`. If no such index exists, `V` is `true`. Otherwise, `V`
is `false`.

[*Example 1*:

``` cpp
struct D {
  int i;
  friend bool operator==(const D& x, const D& y) = default;
                                                // OK, returns x.i == y.i
};
```

— *end example*]

### Three-way comparison <a id="class.spaceship">[[class.spaceship]]</a>

The *synthesized three-way comparison* of type `R` [[cmp.categories]] of
glvalues `a` and `b` of the same type is defined as follows:

- If `a <=> b` is usable [[class.compare.default]],
  `static_cast<R>(a <=> b)`.
- Otherwise, if overload resolution for `a <=> b` is performed and finds
  at least one viable candidate, the synthesized three-way comparison is
  not defined.
- Otherwise, if `R` is not a comparison category type, or either the
  expression `a == b` or the expression `a < b` is not usable, the
  synthesized three-way comparison is not defined.
- Otherwise, if `R` is `strong_ordering`, then
  ``` cpp
  a == b ? strong_ordering::equal :
  a < b  ? strong_ordering::less :
           strong_ordering::greater
  ```
- Otherwise, if `R` is `weak_ordering`, then
  ``` cpp
  a == b ? weak_ordering::equivalent :
  a < b  ? weak_ordering::less :
           weak_ordering::greater
  ```
- Otherwise (when `R` is `partial_ordering`),
  ``` cpp
  a == b ? partial_ordering::equivalent :
  a < b  ? partial_ordering::less :
  b < a  ? partial_ordering::greater :
           partial_ordering::unordered
  ```

[*Note 1*: A synthesized three-way comparison may be ill-formed if
overload resolution finds usable candidates that do not otherwise meet
the requirements implied by the defined expression. — *end note*]

Let `R` be the declared return type of a defaulted three-way comparison
operator function, and let `xᵢ` be the elements of the expanded list of
subobjects for an object `x` of type `C`.

- If `R` is `auto`, then let cv{}_i~`Rᵢ` be the type of the expression
  `xᵢ`` <=> ``xᵢ`. The operator function is defined as deleted if that
  expression is not usable or if `Rᵢ` is not a comparison category type
  [[cmp.categories.pre]] for any i. The return type is deduced as the
  common comparison type (see below) of `R₀`, `R₁`, …, `R_n-1`.
- Otherwise, `R` shall not contain a placeholder type. If the
  synthesized three-way comparison of type `R` between any objects `xᵢ`
  and `xᵢ` is not defined, the operator function is defined as deleted.

The return value `V` of type `R` of the defaulted three-way comparison
operator function with parameters `x` and `y` of the same type is
determined by comparing corresponding elements `xᵢ` and `yᵢ` in the
expanded lists of subobjects for `x` and `y` (in increasing index order)
until the first index i where the synthesized three-way comparison of
type `R` between `xᵢ` and `yᵢ` yields a result value `vᵢ` where
`vᵢ` \mathrel{`!=`} 0, contextually converted to `bool`, yields `true`;
`V` is a copy of `vᵢ`. If no such index exists, `V` is
`static_cast<R>(std::strong_ordering::equal)`.

The *common comparison type* `U` of a possibly-empty list of n
comparison category types `T₀`, `T₁`, …, `T_n-1` is defined as follows:

- If at least one `Tᵢ` is `std::partial_ordering`, `U` is
  `std::partial_ordering` [[cmp.partialord]].
- Otherwise, if at least one `Tᵢ` is `std::weak_ordering`, `U` is
  `std::weak_ordering` [[cmp.weakord]].
- Otherwise, `U` is `std::strong_ordering` [[cmp.strongord]].
  \[*Note 4*: In particular, this is the result when n is
  0. — *end note*]

### Secondary comparison operators <a id="class.compare.secondary">[[class.compare.secondary]]</a>

A *secondary comparison operator* is a relational operator [[expr.rel]]
or the `!=` operator. A defaulted operator function [[over.binary]] for
a secondary comparison operator `@` shall have a declared return type
`bool`.

The operator function with parameters `x` and `y` is defined as deleted
if

- overload resolution [[over.match]], as applied to `x @ y`, does not
  result in a usable candidate, or
- the candidate selected by overload resolution is not a rewritten
  candidate.

Otherwise, the operator function yields `x @ y`. The defaulted operator
function is not considered as a candidate in the overload resolution for
the `@` operator.

[*Example 1*:

``` cpp
struct HasNoLessThan { };

struct C {
  friend HasNoLessThan operator<=>(const C&, const C&);
  bool operator<(const C&) const = default;             // OK, function is deleted
};
```

— *end example*]

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
  new D1;           // error: ::operator new(std::size_t) hidden
}
```

— *end example*]

When an object is deleted with a *delete-expression* [[expr.delete]], a
deallocation function (`operator delete()` for non-array objects or
`operator delete[]()` for arrays) is (implicitly) called to reclaim the
storage occupied by the object [[basic.stc.dynamic.deallocation]].

Class-specific deallocation function lookup is a part of general
deallocation function lookup [[expr.delete]] and occurs as follows. If
the *delete-expression* is used to deallocate a class object whose
static type has a virtual destructor, the deallocation function is the
one selected at the point of definition of the dynamic type’s virtual
destructor [[class.dtor]].[^15] Otherwise, if the *delete-expression* is
used to deallocate an object of class `T` or array thereof, the
deallocation function’s name is looked up in the scope of `T`. If this
lookup fails to find the name, general deallocation function lookup
[[expr.delete]] continues. If the result of the lookup is ambiguous or
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
of the object if the destructor is virtual, the effect is the same in
that case. For example,

``` cpp
struct B {
  virtual ~B();
  void operator delete(void*, std::size_t);
};

struct D : B {
  void operator delete(void*);
};

struct E : B {
  void log_deletion();
  void operator delete(E *p, std::destroying_delete_t) {
    p->log_deletion();
    p->~E();
    ::operator delete(p);
  }
};

void f() {
  B* bp = new D;
  delete bp;        // 1: uses D::operator delete(void*)
  bp = new E;
  delete bp;        // 2: uses E::operator delete(E*, std::destroying_delete_t)
}
```

Here, storage for the object of class `D` is deallocated by
`D::operator delete()`, and the object of class `E` is destroyed and its
storage is deallocated by `E::operator delete()`, due to the virtual
destructor.

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
`B::operator delete()` had been private, the delete expression would
have been ill-formed. — *end example*]

[*Note 3*: If a deallocation function has no explicit
*noexcept-specifier*, it has a non-throwing exception specification
[[except.spec]]. — *end note*]

<!-- Link reference definitions -->
[basic.compound]: basic.md#basic.compound
[basic.def]: basic.md#basic.def
[basic.def.odr]: basic.md#basic.def.odr
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.elab]: basic.md#basic.lookup.elab
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.lval]: expr.md#basic.lval
[basic.scope]: basic.md#basic.scope
[basic.scope.class]: basic.md#basic.scope.class
[basic.scope.hiding]: basic.md#basic.scope.hiding
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.static]: basic.md#basic.start.static
[basic.start.term]: basic.md#basic.start.term
[basic.stc]: basic.md#basic.stc
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[class]: #class
[class.abstract]: #class.abstract
[class.access]: #class.access
[class.access.base]: #class.access.base
[class.access.nest]: #class.access.nest
[class.access.spec]: #class.access.spec
[class.access.virt]: #class.access.virt
[class.base.init]: #class.base.init
[class.bit]: #class.bit
[class.cdtor]: #class.cdtor
[class.compare]: #class.compare
[class.compare.default]: #class.compare.default
[class.compare.secondary]: #class.compare.secondary
[class.conv]: #class.conv
[class.conv.ctor]: #class.conv.ctor
[class.conv.fct]: #class.conv.fct
[class.copy.assign]: #class.copy.assign
[class.copy.ctor]: #class.copy.ctor
[class.copy.elision]: #class.copy.elision
[class.ctor]: #class.ctor
[class.default.ctor]: #class.default.ctor
[class.derived]: #class.derived
[class.dtor]: #class.dtor
[class.eq]: #class.eq
[class.expl.init]: #class.expl.init
[class.free]: #class.free
[class.friend]: #class.friend
[class.inhctor.init]: #class.inhctor.init
[class.init]: #class.init
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
[class.pre]: #class.pre
[class.prop]: #class.prop
[class.protected]: #class.protected
[class.qual]: basic.md#class.qual
[class.spaceship]: #class.spaceship
[class.static]: #class.static
[class.static.data]: #class.static.data
[class.static.mfct]: #class.static.mfct
[class.temporary]: basic.md#class.temporary
[class.this]: #class.this
[class.union]: #class.union
[class.union.anon]: #class.union.anon
[class.virtual]: #class.virtual
[cmp.categories]: support.md#cmp.categories
[cmp.categories.pre]: support.md#cmp.categories.pre
[cmp.partialord]: support.md#cmp.partialord
[cmp.strongord]: support.md#cmp.strongord
[cmp.weakord]: support.md#cmp.weakord
[conv]: expr.md#conv
[conv.mem]: expr.md#conv.mem
[conv.ptr]: expr.md#conv.ptr
[conv.rval]: expr.md#conv.rval
[dcl.array]: dcl.md#dcl.array
[dcl.attr.nouniqueaddr]: dcl.md#dcl.attr.nouniqueaddr
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.decl]: dcl.md#dcl.decl
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.fct.def.coroutine]: dcl.md#dcl.fct.def.coroutine
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.fct.def.general]: dcl.md#dcl.fct.def.general
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.fct.spec]: dcl.md#dcl.fct.spec
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.inline]: dcl.md#dcl.inline
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.stc]: dcl.md#dcl.stc
[dcl.type.cv]: dcl.md#dcl.type.cv
[dcl.type.elab]: dcl.md#dcl.type.elab
[dcl.type.simple]: dcl.md#dcl.type.simple
[dcl.typedef]: dcl.md#dcl.typedef
[depr.impldec]: future.md#depr.impldec
[depr.static.constexpr]: future.md#depr.static.constexpr
[diff.class]: compatibility.md#diff.class
[except.ctor]: except.md#except.ctor
[except.handle]: except.md#except.handle
[except.pre]: except.md#except.pre
[except.spec]: except.md#except.spec
[except.throw]: except.md#except.throw
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.const]: expr.md#expr.const
[expr.const.cast]: expr.md#expr.const.cast
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.eq]: expr.md#expr.eq
[expr.new]: expr.md#expr.new
[expr.prim.id]: expr.md#expr.prim.id
[expr.prim.id.dtor]: expr.md#expr.prim.id.dtor
[expr.prim.id.qual]: expr.md#expr.prim.id.qual
[expr.prim.this]: expr.md#expr.prim.this
[expr.ref]: expr.md#expr.ref
[expr.reinterpret.cast]: expr.md#expr.reinterpret.cast
[expr.rel]: expr.md#expr.rel
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.throw]: expr.md#expr.throw
[expr.type.conv]: expr.md#expr.type.conv
[expr.typeid]: expr.md#expr.typeid
[expr.unary.op]: expr.md#expr.unary.op
[intro.execution]: basic.md#intro.execution
[intro.object]: basic.md#intro.object
[namespace.def]: dcl.md#namespace.def
[namespace.memdef]: dcl.md#namespace.memdef
[namespace.udecl]: dcl.md#namespace.udecl
[over]: over.md#over
[over.ass]: over.md#over.ass
[over.best.ics]: over.md#over.best.ics
[over.binary]: over.md#over.binary
[over.ics.ref]: over.md#over.ics.ref
[over.load]: over.md#over.load
[over.match]: over.md#over.match
[over.match.best]: over.md#over.match.best
[over.match.call]: over.md#over.match.call
[over.match.copy]: over.md#over.match.copy
[over.match.funcs]: over.md#over.match.funcs
[over.oper]: over.md#over.oper
[over.over]: over.md#over.over
[special]: #special
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.return]: stmt.md#stmt.return
[stmt.return.coroutine]: stmt.md#stmt.return.coroutine
[string.classes]: strings.md#string.classes
[temp.arg]: temp.md#temp.arg
[temp.class.spec]: temp.md#temp.class.spec
[temp.constr]: temp.md#temp.constr
[temp.constr.order]: temp.md#temp.constr.order
[temp.dep.type]: temp.md#temp.dep.type
[temp.expl.spec]: temp.md#temp.expl.spec
[temp.friend]: temp.md#temp.friend
[temp.inst]: temp.md#temp.inst
[temp.mem]: temp.md#temp.mem
[temp.param]: temp.md#temp.param
[temp.pre]: temp.md#temp.pre
[temp.spec]: temp.md#temp.spec
[temp.variadic]: temp.md#temp.variadic

[^1]: This ensures that two subobjects that have the same class type and
    that belong to the same most derived object are not allocated at the
    same address [[expr.eq]].

[^2]: See, for example, `<cstring>`.

[^3]: This implies that the reference parameter of the
    implicitly-declared copy constructor cannot bind to a `volatile`
    lvalue; see  [[diff.class]].

[^4]: Because a template assignment operator or an assignment operator
    taking an rvalue reference parameter is never a copy assignment
    operator, the presence of such an assignment operator does not
    suppress the implicit declaration of a copy assignment operator.
    Such assignment operators participate in overload resolution with
    other assignment operators, including copy assignment operators,
    and, if selected, will be used to assign an object.

[^5]: This implies that the reference parameter of the
    implicitly-declared copy assignment operator cannot bind to a
    `volatile` lvalue; see  [[diff.class]].

[^6]: These conversions are considered as standard conversions for the
    purposes of overload resolution ([[over.best.ics]],
    [[over.ics.ref]]) and therefore initialization [[dcl.init]] and
    explicit casts [[expr.static.cast]]. A conversion to `void` does not
    invoke any conversion function [[expr.static.cast]]. Even though
    never directly called to perform a conversion, such conversion
    functions can be declared and can potentially be reached through a
    call to a virtual conversion function in a base class.

[^7]: The use of the `virtual` specifier in the declaration of an
    overriding function is valid but redundant (has empty semantics).

[^8]: If all virtual functions are immediate functions, the class is
    still polymorphic even though its internal representation might not
    otherwise require any additions for that polymorphic behavior.

[^9]: A function with the same name but a different parameter list
    [[over]] as a virtual function is not necessarily virtual and does
    not override. Access control [[class.access]] is not considered in
    determining overriding.

[^10]: Multi-level pointers to classes or references to multi-level
    pointers to classes are not allowed.

[^11]: Access permissions are thus transitive and cumulative to nested
    and local classes.

[^12]: As specified previously in [[class.access]], private members of a
    base class remain inaccessible even to derived classes unless friend
    declarations within the base class definition are used to grant
    access explicitly.

[^13]: This additional check does not apply to other members, e.g.,
    static data members or enumerator member constants.

[^14]: Because only one object is destroyed instead of two, and one
    copy/move constructor is not executed, there is still one object
    destroyed for each one constructed.

[^15]: A similar provision is not needed for the array version of
    `operator` `delete` because  [[expr.delete]] requires that in this
    situation, the static type of the object to be deleted be the same
    as its dynamic type.
