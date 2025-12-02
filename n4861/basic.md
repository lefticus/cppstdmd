# Basics <a id="basic">[[basic]]</a>

## Preamble <a id="basic.pre">[[basic.pre]]</a>

[*Note 1*: This Clause presents the basic concepts of the C++ language.
It explains the difference between an object and a name and how they
relate to the value categories for expressions. It introduces the
concepts of a declaration and a definition and presents C++’s notion of
type, scope, linkage, and storage duration. The mechanisms for starting
and terminating a program are discussed. Finally, this Clause presents
the fundamental types of the language and lists the ways of constructing
compound types from these. — *end note*]

[*Note 2*: This Clause does not cover concepts that affect only a
single part of the language. Such concepts are discussed in the relevant
Clauses. — *end note*]

An *entity* is a value, object, reference, structured binding, function,
enumerator, type, class member, bit-field, template, template
specialization, namespace, or pack.

A *name* is a use of an *identifier* [[lex.name]],
*operator-function-id* [[over.oper]], *literal-operator-id*
[[over.literal]], *conversion-function-id* [[class.conv.fct]], or
*template-id* [[temp.names]] that denotes an entity or label (
[[stmt.goto]], [[stmt.label]]).

Every name that denotes an entity is introduced by a *declaration*.
Every name that denotes a label is introduced either by a `goto`
statement [[stmt.goto]] or a *labeled-statement* [[stmt.label]].

A *variable* is introduced by the declaration of a reference other than
a non-static data member or of an object. The variable’s name, if any,
denotes the reference or object.

A *local entity* is a variable with automatic storage duration
[[basic.stc.auto]], a structured binding [[dcl.struct.bind]] whose
corresponding variable is such an entity, or the `*this` object
[[expr.prim.this]].

Some names denote types or templates. In general, whenever a name is
encountered it is necessary to determine whether that name denotes one
of these entities before continuing to parse the program that contains
it. The process that determines this is called *name lookup*
[[basic.lookup]].

Two names are *the same* if

- they are *identifier*s composed of the same character sequence, or
- they are *operator-function-id*s formed with the same operator, or
- they are *conversion-function-id*s formed with the same type, or
- they are *template-id*s that refer to the same class, function, or
  variable [[temp.type]], or
- they are *literal-operator-id*s [[over.literal]] formed with the same
  literal suffix identifier.

A name used in more than one translation unit can potentially refer to
the same entity in these translation units depending on the linkage
[[basic.link]] of the name specified in each translation unit.

## Declarations and definitions <a id="basic.def">[[basic.def]]</a>

A declaration [[dcl.dcl]] may introduce one or more names into a
translation unit or redeclare names introduced by previous declarations.
If so, the declaration specifies the interpretation and semantic
properties of these names. A declaration may also have effects
including:

- a static assertion [[dcl.pre]],
- controlling template instantiation [[temp.explicit]],
- guiding template argument deduction for constructors
  [[temp.deduct.guide]],
- use of attributes [[dcl.attr]], and
- nothing (in the case of an *empty-declaration*).

Each entity declared by a *declaration* is also *defined* by that
declaration unless:

- it declares a function without specifying the function’s body
  [[dcl.fct.def]],
- it contains the `extern` specifier [[dcl.stc]] or a
  *linkage-specification*[^1] [[dcl.link]] and neither an *initializer*
  nor a *function-body*,
- it declares a non-inline static data member in a class definition (
  [[class.mem]], [[class.static]]),
- it declares a static data member outside a class definition and the
  variable was defined within the class with the `constexpr` specifier
  (this usage is deprecated; see [[depr.static.constexpr]]),
- it is introduced by an *elaborated-type-specifier* [[class.name]],
- it is an *opaque-enum-declaration* [[dcl.enum]],
- it is a *template-parameter* [[temp.param]],
- it is a *parameter-declaration* [[dcl.fct]] in a function declarator
  that is not the *declarator* of a *function-definition*,
- it is a `typedef` declaration [[dcl.typedef]],
- it is an *alias-declaration* [[dcl.typedef]],
- it is a *using-declaration* [[namespace.udecl]],
- it is a *deduction-guide* [[temp.deduct.guide]],
- it is a *static_assert-declaration* [[dcl.pre]],
- it is an *attribute-declaration* [[dcl.pre]],
- it is an *empty-declaration* [[dcl.pre]],
- it is a *using-directive* [[namespace.udir]],
- it is a *using-enum-declaration* [[enum.udecl]],
- it is a *template-declaration* [[temp.pre]] whose *template-head* is
  not followed by either a *concept-definition* or a *declaration* that
  defines a function, a class, a variable, or a static data member.
- it is an explicit instantiation declaration [[temp.explicit]], or
- it is an explicit specialization [[temp.expl.spec]] whose
  *declaration* is not a definition.

A declaration is said to be a *definition* of each entity that it
defines.

[*Example 1*:

All but one of the following are definitions:

``` cpp
int a;                          // defines a
extern const int c = 1;         // defines c
int f(int x) { return x+a; }    // defines f and defines x
struct S { int a; int b; };     // defines S, S::a, and S::b
struct X {                      // defines X
  int x;                        // defines non-static data member x
  static int y;                 // declares static data member y
  X(): x(0) { }                 // defines a constructor of X
};
int X::y = 1;                   // defines X::y
enum { up, down };              // defines up and down
namespace N { int d; }          // defines N and N::d
namespace N1 = N;               // defines N1
X anX;                          // defines anX
```

whereas these are just declarations:

``` cpp
extern int a;                   // declares a
extern const int c;             // declares c
int f(int);                     // declares f
struct S;                       // declares S
typedef int Int;                // declares Int
extern X anotherX;              // declares anotherX
using N::d;                     // declares d
```

— *end example*]

[*Note 1*:  In some circumstances, C++ implementations implicitly
define the default constructor [[class.default.ctor]], copy constructor,
move constructor [[class.copy.ctor]], copy assignment operator, move
assignment operator [[class.copy.assign]], or destructor [[class.dtor]]
member functions. — *end note*]

[*Example 2*:

Given

``` cpp
#include <string>

struct C {
  std::string s;                // std::string is the standard library class[string.classes]
};

int main() {
  C a;
  C b = a;
  b = a;
}
```

the implementation will implicitly define functions to make the
definition of `C` equivalent to

``` cpp
struct C {
  std::string s;
  C() : s() { }
  C(const C& x): s(x.s) { }
  C(C&& x): s(static_cast<std::string&&>(x.s)) { }
      //    : s(std::move(x.s)) { }
  C& operator=(const C& x) { s = x.s; return *this; }
  C& operator=(C&& x) { s = static_cast<std::string&&>(x.s); return *this; }
      //                { s = std::move(x.s); return *this; }
  ~C() { }
};
```

— *end example*]

[*Note 2*: A class name can also be implicitly declared by an
*elaborated-type-specifier* [[dcl.type.elab]]. — *end note*]

In the definition of an object, the type of that object shall not be an
incomplete type [[basic.types]], an abstract class type
[[class.abstract]], or a (possibly multi-dimensional) array thereof.

## One-definition rule <a id="basic.def.odr">[[basic.def.odr]]</a>

No translation unit shall contain more than one definition of any
variable, function, class type, enumeration type, template, default
argument for a parameter (for a function in a given scope), or default
template argument.

An expression or conversion is *potentially evaluated* unless it is an
unevaluated operand [[expr.prop]], a subexpression thereof, or a
conversion in an initialization or conversion sequence in such a
context. The set of *potential results* of an expression E is defined as
follows:

- If E is an *id-expression* [[expr.prim.id]], the set contains only E.
- If E is a subscripting operation [[expr.sub]] with an array operand,
  the set contains the potential results of that operand.
- If E is a class member access expression [[expr.ref]] of the form E₁
  `.` \tcode{templateₒₚₜ  E₂ naming a non-static data member, the set
  contains the potential results of E₁.
- If E is a class member access expression naming a static data member,
  the set contains the *id-expression* designating the data member.
- If E is a pointer-to-member expression [[expr.mptr.oper]] of the form
  E₁ `.*` E₂, the set contains the potential results of E₁.
- If E has the form `(E₁)`, the set contains the potential results of
  E₁.
- If E is a glvalue conditional expression [[expr.cond]], the set is the
  union of the sets of potential results of the second and third
  operands.
- If E is a comma expression [[expr.comma]], the set contains the
  potential results of the right operand.
- Otherwise, the set is empty.

[*Note 1*:

This set is a (possibly-empty) set of *id-expression*s, each of which is
either E or a subexpression of E.

[*Example 1*:

In the following example, the set of potential results of the
initializer of `n` contains the first `S::x` subexpression, but not the
second `S::x` subexpression.

``` cpp
struct S { static const int x = 0; };
const int &f(const int &r);
int n = b ? (1, S::x)           // S::x is not odr-used here
          : f(S::x);            // S::x is odr-used here, so a definition is required
```

— *end example*]

— *end note*]

A function is *named by* an expression or conversion as follows:

- A function is named by an expression or conversion if it is the
  selected member of an overload set ([[basic.lookup]], [[over.match]],
  [[over.over]]) in an overload resolution performed as part of forming
  that expression or conversion, unless it is a pure virtual function
  and either the expression is not an *id-expression* naming the
  function with an explicitly qualified name or the expression forms a
  pointer to member [[expr.unary.op]]. \[*Note 2*: This covers taking
  the address of functions ([[conv.func]], [[expr.unary.op]]), calls to
  named functions [[expr.call]], operator overloading [[over]],
  user-defined conversions [[class.conv.fct]], allocation functions for
  *new-expression*s [[expr.new]], as well as non-default initialization
  [[dcl.init]]. A constructor selected to copy or move an object of
  class type is considered to be named by an expression or conversion
  even if the call is actually elided by the implementation
  [[class.copy.elision]]. — *end note*]
- A deallocation function for a class is named by a *new-expression* if
  it is the single matching deallocation function for the allocation
  function selected by overload resolution, as specified in 
  [[expr.new]].
- A deallocation function for a class is named by a *delete-expression*
  if it is the selected usual deallocation function as specified in 
  [[expr.delete]] and  [[class.free]].

A variable `x` whose name appears as a potentially-evaluated expression
E is *odr-used* by E unless

- `x` is a reference that is usable in constant expressions
  [[expr.const]], or
- `x` is a variable of non-reference type that is usable in constant
  expressions and has no mutable subobjects, and E is an element of the
  set of potential results of an expression of non-volatile-qualified
  non-class type to which the lvalue-to-rvalue conversion [[conv.lval]]
  is applied, or
- `x` is a variable of non-reference type, and E is an element of the
  set of potential results of a discarded-value expression [[expr.prop]]
  to which the lvalue-to-rvalue conversion is not applied.

A structured binding is odr-used if it appears as a
potentially-evaluated expression.

`*this` is odr-used if `this` appears as a potentially-evaluated
expression (including as the result of the implicit transformation in
the body of a non-static member function ([[class.mfct.non-static]])).

A virtual member function is odr-used if it is not pure. A function is
odr-used if it is named by a potentially-evaluated expression or
conversion. A non-placement allocation or deallocation function for a
class is odr-used by the definition of a constructor of that class. A
non-placement deallocation function for a class is odr-used by the
definition of the destructor of that class, or by being selected by the
lookup at the point of definition of a virtual destructor
[[class.dtor]].[^2]

An assignment operator function in a class is odr-used by an
implicitly-defined copy-assignment or move-assignment function for
another class as specified in  [[class.copy.assign]]. A constructor for
a class is odr-used as specified in  [[dcl.init]]. A destructor for a
class is odr-used if it is potentially invoked [[class.dtor]].

A local entity [[basic.pre]] is *odr-usable* in a declarative region
[[basic.scope.declarative]] if:

- either the local entity is not `*this`, or an enclosing class or
  non-lambda function parameter scope exists and, if the innermost such
  scope is a function parameter scope, it corresponds to a non-static
  member function, and
- for each intervening declarative region [[basic.scope.declarative]]
  between the point at which the entity is introduced and the region
  (where `*this` is considered to be introduced within the innermost
  enclosing class or non-lambda function definition scope), either:
  - the intervening declarative region is a block scope, or
  - the intervening declarative region is the function parameter scope
    of a *lambda-expression* that has a *simple-capture* naming the
    entity or has a *capture-default*, and the block scope of the
    *lambda-expression* is also an intervening declarative region.

If a local entity is odr-used in a declarative region in which it is not
odr-usable, the program is ill-formed.

[*Example 2*:

``` cpp
void f(int n) {
  [] { n = 1; };                // error: n is not odr-usable due to intervening lambda-expression
  struct A {
    void f() { n = 2; }         // error: n is not odr-usable due to intervening function definition scope
  };
  void g(int = n);              // error: n is not odr-usable due to intervening function parameter scope
  [=](int k = n) {};            // error: n is not odr-usable due to being
                                // outside the block scope of the lambda-expression
  [&] { [n]{ return n; }; };    // OK
}
```

— *end example*]

Every program shall contain exactly one definition of every non-inline
function or variable that is odr-used in that program outside of a
discarded statement [[stmt.if]]; no diagnostic required. The definition
can appear explicitly in the program, it can be found in the standard or
a user-defined library, or (when appropriate) it is implicitly defined
(see  [[class.default.ctor]], [[class.copy.ctor]], [[class.dtor]], and
[[class.copy.assign]]).

[*Example 3*:

``` cpp
auto f() {
  struct A {};
  return A{};
}
decltype(f()) g();
auto x = g();
```

A program containing this translation unit is ill-formed because `g` is
odr-used but not defined, and cannot be defined in any other translation
unit because the local class `A` cannot be named outside this
translation unit.

— *end example*]

A *definition domain* is a *private-module-fragment* or the portion of a
translation unit excluding its *private-module-fragment* (if any). A
definition of an inline function or variable shall be reachable from the
end of every definition domain in which it is odr-used outside of a
discarded statement.

A definition of a class is required to be reachable in every context in
which the class is used in a way that requires the class type to be
complete.

[*Example 4*:

The following complete translation unit is well-formed, even though it
never defines `X`:

``` cpp
struct X;                       // declare X as a struct type
struct X* x1;                   // use X in pointer formation
X* x2;                          // use X in pointer formation
```

— *end example*]

[*Note 3*:

The rules for declarations and expressions describe in which contexts
complete class types are required. A class type `T` must be complete if:

- an object of type `T` is defined [[basic.def]], or
- a non-static class data member of type `T` is declared [[class.mem]],
  or
- `T` is used as the allocated type or array element type in a
  *new-expression* [[expr.new]], or
- an lvalue-to-rvalue conversion is applied to a glvalue referring to an
  object of type `T` [[conv.lval]], or
- an expression is converted (either implicitly or explicitly) to type
  `T` ([[conv]], [[expr.type.conv]], [[expr.dynamic.cast]],
  [[expr.static.cast]], [[expr.cast]]), or
- an expression that is not a null pointer constant, and has type other
  than cv `void*`, is converted to the type pointer to `T` or reference
  to `T` using a standard conversion [[conv]], a `dynamic_cast`
  [[expr.dynamic.cast]] or a `static_cast` [[expr.static.cast]], or
- a class member access operator is applied to an expression of type `T`
  [[expr.ref]], or
- the `typeid` operator [[expr.typeid]] or the `sizeof` operator
  [[expr.sizeof]] is applied to an operand of type `T`, or
- a function with a return type or argument type of type `T` is defined
  [[basic.def]] or called [[expr.call]], or
- a class with a base class of type `T` is defined [[class.derived]], or
- an lvalue of type `T` is assigned to [[expr.ass]], or
- the type `T` is the subject of an `alignof` expression
  [[expr.alignof]], or
- an *exception-declaration* has type `T`, reference to `T`, or pointer
  to `T` [[except.handle]].

— *end note*]

There can be more than one definition of a

- class type [[class]],
- enumeration type [[dcl.enum]],
- inline function or variable [[dcl.inline]],
- templated entity [[temp.pre]],
- default argument for a parameter (for a function in a given scope)
  [[dcl.fct.default]], or
- default template argument [[temp.param]]

in a program provided that each definition appears in a different
translation unit and the definitions satisfy the following requirements.
Given such an entity `D` defined in more than one translation unit, for
all definitions of `D`, or, if `D` is an unnamed enumeration, for all
definitions of `D` that are reachable at any given program point, the
following requirements shall be satisfied.

- Each such definition shall not be attached to a named module
  [[module.unit]].
- Each such definition shall consist of the same sequence of tokens,
  where the definition of a closure type is considered to consist of the
  sequence of tokens of the corresponding *lambda-expression*.
- In each such definition, corresponding names, looked up according to 
  [[basic.lookup]], shall refer to the same entity, after overload
  resolution [[over.match]] and after matching of partial template
  specialization [[temp.over]], except that a name can refer to
  - a non-volatile const object with internal or no linkage if the
    object
    - has the same literal type in all definitions of `D`,
    - is initialized with a constant expression [[expr.const]],
    - is not odr-used in any definition of `D`, and
    - has the same value in all definitions of `D`,

    or
  - a reference with internal or no linkage initialized with a constant
    expression such that the reference refers to the same entity in all
    definitions of `D`.
- In each such definition, except within the default arguments and
  default template arguments of `D`, corresponding *lambda-expression*s
  shall have the same closure type (see below).
- In each such definition, corresponding entities shall have the same
  language linkage.
- In each such definition, the overloaded operators referred to, the
  implicit calls to conversion functions, constructors, operator new
  functions and operator delete functions, shall refer to the same
  function.
- In each such definition, a default argument used by an (implicit or
  explicit) function call or a default template argument used by an
  (implicit or explicit) *template-id* or *simple-template-id* is
  treated as if its token sequence were present in the definition of
  `D`; that is, the default argument or default template argument is
  subject to the requirements described in this paragraph (recursively).
- If `D` is a class with an implicitly-declared constructor (
  [[class.default.ctor]], [[class.copy.ctor]]), it is as if the
  constructor was implicitly defined in every translation unit where it
  is odr-used, and the implicit definition in every translation unit
  shall call the same constructor for a subobject of `D`.
  \[*Example 5*:
  ``` cpp
  // translation unit 1:
  struct X {
    X(int, int);
    X(int, int, int);
  };
  X::X(int, int = 0) { }
  class D {
    X x = 0;
  };
  D d1;                           // X(int, int) called by D()

  // translation unit 2:
  struct X {
    X(int, int);
    X(int, int, int);
  };
  X::X(int, int = 0, int = 0) { }
  class D {
    X x = 0;
  };
  D d2;                           // X(int, int, int) called by D();
                                  // D()'s implicit definition violates the ODR
  ```

  — *end example*]
- If `D` is a class with a defaulted three-way comparison operator
  function [[class.spaceship]], it is as if the operator was implicitly
  defined in every translation unit where it is odr-used, and the
  implicit definition in every translation unit shall call the same
  comparison operators for each subobject of `D`.

If `D` is a template and is defined in more than one translation unit,
then the preceding requirements shall apply both to names from the
template’s enclosing scope used in the template definition
[[temp.nondep]], and also to dependent names at the point of
instantiation [[temp.dep]]. These requirements also apply to
corresponding entities defined within each definition of `D` (including
the closure types of *lambda-expression*s, but excluding entities
defined within default arguments or default template arguments of either
`D` or an entity not defined within `D`). For each such entity and for
`D` itself, the behavior is as if there is a single entity with a single
definition, including in the application of these requirements to other
entities.

[*Note 4*: The entity is still declared in multiple translation units,
and [[basic.link]] still applies to these declarations. In particular,
*lambda-expression*s [[expr.prim.lambda]] appearing in the type of `D`
may result in the different declarations having distinct types, and
*lambda-expression*s appearing in a default argument of `D` may still
denote different types in different translation units. — *end note*]

If these definitions do not satisfy these requirements, then the program
is ill-formed; a diagnostic is required only if the entity is attached
to a named module and a prior definition is reachable at the point where
a later definition occurs.

[*Example 6*:

``` cpp
inline void f(bool cond, void (*p)()) {
  if (cond) f(false, []{});
}
inline void g(bool cond, void (*p)() = []{}) {
  if (cond) g(false);
}
struct X {
  void h(bool cond, void (*p)() = []{}) {
    if (cond) h(false);
  }
};
```

If the definition of `f` appears in multiple translation units, the
behavior of the program is as if there is only one definition of `f`. If
the definition of `g` appears in multiple translation units, the program
is ill-formed (no diagnostic required) because each such definition uses
a default argument that refers to a distinct *lambda-expression* closure
type. The definition of `X` can appear in multiple translation units of
a valid program; the *lambda-expression*s defined within the default
argument of `X::h` within the definition of `X` denote the same closure
type in each translation unit.

— *end example*]

If, at any point in the program, there is more than one reachable
unnamed enumeration definition in the same scope that have the same
first enumerator name and do not have typedef names for linkage purposes
[[dcl.enum]], those unnamed enumeration types shall be the same; no
diagnostic required.

## Scope <a id="basic.scope">[[basic.scope]]</a>

### Declarative regions and scopes <a id="basic.scope.declarative">[[basic.scope.declarative]]</a>

Every name is introduced in some portion of program text called a
*declarative region*, which is the largest part of the program in which
that name is valid, that is, in which that name may be used as an
unqualified name to refer to the same entity. In general, each
particular name is valid only within some possibly discontiguous portion
of program text called its *scope*. To determine the scope of a
declaration, it is sometimes convenient to refer to the *potential
scope* of a declaration. The scope of a declaration is the same as its
potential scope unless the potential scope contains another declaration
of the same name. In that case, the potential scope of the declaration
in the inner (contained) declarative region is excluded from the scope
of the declaration in the outer (containing) declarative region.

[*Example 1*:

In

``` cpp
int j = 24;
int main() {
  int i = j, j;
  j = 42;
}
```

the identifier `j` is declared twice as a name (and used twice). The
declarative region of the first `j` includes the entire example. The
potential scope of the first `j` begins immediately after that `j` and
extends to the end of the program, but its (actual) scope excludes the
text between the `,` and the `}`. The declarative region of the second
declaration of `j` (the `j` immediately before the semicolon) includes
all the text between `{` and `}`, but its potential scope excludes the
declaration of `i`. The scope of the second declaration of `j` is the
same as its potential scope.

— *end example*]

The names declared by a declaration are introduced into the scope in
which the declaration occurs, except that the presence of a `friend`
specifier [[class.friend]], certain uses of the
*elaborated-type-specifier* [[dcl.type.elab]], and *using-directive*s
[[namespace.udir]] alter this general behavior.

Given a set of declarations in a single declarative region, each of
which specifies the same unqualified name,

- they shall all refer to the same entity, or all refer to functions and
  function templates; or
- exactly one declaration shall declare a class name or enumeration name
  that is not a typedef name and the other declarations shall all refer
  to the same variable, non-static data member, or enumerator, or all
  refer to functions and function templates; in this case the class name
  or enumeration name is hidden [[basic.scope.hiding]]. \[*Note 1*: A
  structured binding [[dcl.struct.bind]], namespace name
  [[basic.namespace]], or class template name [[temp.pre]] must be
  unique in its declarative region. — *end note*]

[*Note 2*: These restrictions apply to the declarative region into
which a name is introduced, which is not necessarily the same as the
region in which the declaration occurs. In particular,
*elaborated-type-specifier*s [[dcl.type.elab]] and friend declarations
[[class.friend]] may introduce a (possibly not visible) name into an
enclosing namespace; these restrictions apply to that region. Local
extern declarations [[basic.link]] may introduce a name into the
declarative region where the declaration appears and also introduce a
(possibly not visible) name into an enclosing namespace; these
restrictions apply to both regions. — *end note*]

For a given declarative region *R* and a point *P* outside *R*, the set
of *intervening* declarative regions between *P* and *R* comprises all
declarative regions that are or enclose *R* and do not enclose *P*.

[*Note 3*: The name lookup rules are summarized in 
[[basic.lookup]]. — *end note*]

### Point of declaration <a id="basic.scope.pdecl">[[basic.scope.pdecl]]</a>

The *point of declaration* for a name is immediately after its complete
declarator [[dcl.decl]] and before its *initializer* (if any), except as
noted below.

[*Example 1*:

``` cpp
unsigned char x = 12;
{ unsigned char x = x; }
```

Here, the initialization of the second `x` has undefined behavior,
because the initializer accesses the second `x` outside its lifetime
[[basic.life]].

— *end example*]

[*Note 1*:

A name from an outer scope remains visible up to the point of
declaration of the name that hides it.

[*Example 2*:

``` cpp
const int  i = 2;
{ int  i[i]; }
```

declares a block-scope array of two integers.

— *end example*]

— *end note*]

The point of declaration for a class or class template first declared by
a *class-specifier* is immediately after the *identifier* or
*simple-template-id* (if any) in its *class-head* [[class.pre]]. The
point of declaration for an enumeration is immediately after the
*identifier* (if any) in either its *enum-specifier* [[dcl.enum]] or its
first *opaque-enum-declaration* [[dcl.enum]], whichever comes first. The
point of declaration of an alias or alias template immediately follows
the *defining-type-id* to which the alias refers.

The point of declaration of a *using-declarator* that does not name a
constructor is immediately after the *using-declarator*
[[namespace.udecl]].

The point of declaration for an enumerator is immediately after its
*enumerator-definition*.

[*Example 3*:

``` cpp
const int x = 12;
{ enum { x = x }; }
```

Here, the enumerator `x` is initialized with the value of the constant
`x`, namely 12.

— *end example*]

After the point of declaration of a class member, the member name can be
looked up in the scope of its class.

[*Note 2*:

This is true even if the class is an incomplete class. For example,

``` cpp
struct X {
  enum E { z = 16 };
  int b[X::z];      // OK
};
```

— *end note*]

The point of declaration of a class first declared in an
*elaborated-type-specifier* is as follows:

- for a declaration of the formattribute-specifier-seqₒₚₜ  the
  *identifier* is declared to be a *class-name* in the scope that
  contains the declaration, otherwise
- for an *elaborated-type-specifier* of the form if the
  *elaborated-type-specifier* is used in the *decl-specifier-seq* or
  *parameter-declaration-clause* of a function defined in namespace
  scope, the *identifier* is declared as a *class-name* in the namespace
  that contains the declaration; otherwise, except as a friend
  declaration, the *identifier* is declared in the smallest namespace or
  block scope that contains the declaration. \[*Note 3*: These rules
  also apply within templates. — *end note*] \[*Note 4*: Other forms of
  *elaborated-type-specifier* do not declare a new name, and therefore
  must refer to an existing *type-name*. See  [[basic.lookup.elab]] and 
  [[dcl.type.elab]]. — *end note*]

The point of declaration for an injected-class-name [[class.pre]] is
immediately following the opening brace of the class definition.

The point of declaration for a function-local predefined variable
[[dcl.fct.def.general]] is immediately before the *function-body* of a
function definition.

The point of declaration of a structured binding [[dcl.struct.bind]] is
immediately after the *identifier-list* of the structured binding
declaration.

The point of declaration for the variable or the structured bindings
declared in the *for-range-declaration* of a range-based `for` statement
[[stmt.ranged]] is immediately after the *for-range-initializer*.

The point of declaration for a template parameter is immediately after
its complete *template-parameter*.

[*Example 4*:

``` cpp
typedef unsigned char T;
template<class T
  = T               // lookup finds the typedef name of unsigned char
  , T               // lookup finds the template parameter
    N = 0> struct A { };
```

— *end example*]

[*Note 5*: Friend declarations refer to functions or classes that are
members of the nearest enclosing namespace, but they do not introduce
new names into that namespace [[namespace.memdef]]. Function
declarations at block scope and variable declarations with the `extern`
specifier at block scope refer to declarations that are members of an
enclosing namespace, but they do not introduce new names into that
scope. — *end note*]

[*Note 6*: For point of instantiation of a template, see 
[[temp.point]]. — *end note*]

### Block scope <a id="basic.scope.block">[[basic.scope.block]]</a>

A name declared in a block [[stmt.block]] is local to that block; it has
*block scope*. Its potential scope begins at its point of declaration
[[basic.scope.pdecl]] and ends at the end of its block. A variable
declared at block scope is a *local variable*.

The name declared in an *exception-declaration* is local to the
*handler* and shall not be redeclared in the outermost block of the
*handler*.

Names declared in the *init-statement*, the *for-range-declaration*, and
in the *condition* of `if`, `while`, `for`, and `switch` statements are
local to the `if`, `while`, `for`, or `switch` statement (including the
controlled statement), and shall not be redeclared in a subsequent
condition of that statement nor in the outermost block (or, for the `if`
statement, any of the outermost blocks) of the controlled statement.

[*Example 1*:

``` cpp
if (int x = f()) {
  int x;            // error: redeclaration of x
}
else {
  int x;            // error: redeclaration of x
}
```

— *end example*]

### Function parameter scope <a id="basic.scope.param">[[basic.scope.param]]</a>

A function parameter (including one appearing in a *lambda-declarator*)
or function-local predefined variable [[dcl.fct.def]] has *function
parameter scope*. The potential scope of a parameter or function-local
predefined variable begins at its point of declaration. If the nearest
enclosing function declarator is not the declarator of a function
definition, the potential scope ends at the end of that function
declarator. Otherwise, if the function has a *function-try-block* the
potential scope ends at the end of the last associated handler.
Otherwise the potential scope ends at the end of the outermost block of
the function definition. A parameter name shall not be redeclared in the
outermost block of the function definition nor in the outermost block of
any handler associated with a *function-try-block*.

### Function scope <a id="basic.funscope">[[basic.funscope]]</a>

Labels [[stmt.label]] have *function scope* and may be used anywhere in
the function in which they are declared. Only labels have function
scope.

### Namespace scope <a id="basic.scope.namespace">[[basic.scope.namespace]]</a>

The declarative region of a *namespace-definition* is its
*namespace-body*. Entities declared in a *namespace-body* are said to be
*members* of the namespace, and names introduced by these declarations
into the declarative region of the namespace are said to be *member
names* of the namespace. A namespace member name has namespace scope.
Its potential scope includes its namespace from the name’s point of
declaration [[basic.scope.pdecl]] onwards; and for each
*using-directive* [[namespace.udir]] that nominates the member’s
namespace, the member’s potential scope includes that portion of the
potential scope of the *using-directive* that follows the member’s point
of declaration.

[*Example 1*:

``` cpp
namespace N {
  int i;
  int g(int a) { return a; }
  int j();
  void q();
}
namespace { int l=1; }
// the potential scope of l is from its point of declaration to the end of the translation unit

namespace N {
  int g(char a) {   // overloads N::g(int)
    return l+a;     // l is from unnamed namespace
  }

  int i;            // error: duplicate definition
  int j();          // OK: duplicate function declaration

  int j() {         // OK: definition of N::j()
    return g(i);    // calls N::g(int)
  }
  int q();          // error: different return type
}
```

— *end example*]

If a translation unit Q is imported into a translation unit R
[[module.import]], the potential scope of a name X declared with
namespace scope in Q is extended to include the portion of the
corresponding namespace scope in R following the first
*module-import-declaration* or *module-declaration* in R that imports Q
(directly or indirectly) if

- X does not have internal linkage, and
- X is declared after the *module-declaration* in Q (if any), and
- either X is exported or Q and R are part of the same module.

[*Note 1*:

A *module-import-declaration* imports both the named translation unit(s)
and any modules named by exported *module-import-declaration*s within
them, recursively.

[*Example 2*:

Translation unit #1

``` cpp
export module Q;
export int sq(int i) { return i*i; }
```

Translation unit #2

``` cpp
export module R;
export import Q;
```

Translation unit #3

``` cpp
import R;
int main() { return sq(9); }    // OK: sq from module Q
```

— *end example*]

— *end note*]

A namespace member can also be referred to after the `::` scope
resolution operator [[expr.prim.id.qual]] applied to the name of its
namespace or the name of a namespace which nominates the member’s
namespace in a *using-directive*; see  [[namespace.qual]].

The outermost declarative region of a translation unit is also a
namespace, called the *global namespace*. A name declared in the global
namespace has *global namespace scope* (also called *global scope*). The
potential scope of such a name begins at its point of declaration
[[basic.scope.pdecl]] and ends at the end of the translation unit that
is its declarative region. A name with global namespace scope is said to
be a *global name*.

### Class scope <a id="basic.scope.class">[[basic.scope.class]]</a>

The potential scope of a name declared in a class consists not only of
the declarative region following the name’s point of declaration, but
also of all complete-class contexts [[class.mem]] of that class.

A name `N` used in a class `S` shall refer to the same declaration in
its context and when re-evaluated in the completed scope of `S`. No
diagnostic is required for a violation of this rule.

A name declared within a member function hides a declaration of the same
name whose scope extends to or past the end of the member function’s
class.

The potential scope of a declaration in a class that extends to or past
the end of a class definition also extends to the regions defined by its
member definitions, even if the members are defined lexically outside
the class (this includes static data member definitions, nested class
definitions, and member function definitions, including the member
function body and any portion of the declarator part of such definitions
which follows the *declarator-id*, including a
*parameter-declaration-clause* and any default arguments
[[dcl.fct.default]]).

[*Example 1*:

``` cpp
typedef int  c;
enum { i = 1 };

class X {
  char  v[i];                       // error: i refers to ::i but when reevaluated is X::i
  int  f() { return sizeof(c); }    // OK: X::c
  char  c;
  enum { i = 2 };
};

typedef char*  T;
struct Y {
  T  a;                             // error: T refers to ::T but when reevaluated is Y::T
  typedef long  T;
  T  b;
};

typedef int I;
class D {
  typedef I I;                      // error, even though no reordering involved
};
```

— *end example*]

The name of a class member shall only be used as follows:

- in the scope of its class (as described above) or a class derived
  [[class.derived]] from its class,
- after the `.` operator applied to an expression of the type of its
  class [[expr.ref]] or a class derived from its class,
- after the `->` operator applied to a pointer to an object of its class
  [[expr.ref]] or a class derived from its class,
- after the `::` scope resolution operator [[expr.prim.id.qual]] applied
  to the name of its class or a class derived from its class.

### Enumeration scope <a id="basic.scope.enum">[[basic.scope.enum]]</a>

The name of a scoped enumerator [[dcl.enum]] has *enumeration scope*.
Its potential scope begins at its point of declaration and terminates at
the end of the *enum-specifier*.

### Template parameter scope <a id="basic.scope.temp">[[basic.scope.temp]]</a>

The declarative region of the name of a template parameter of a template
*template-parameter* is the smallest *template-parameter-list* in which
the name was introduced.

The declarative region of the name of a template parameter of a template
is the smallest *template-declaration* in which the name was introduced.
Only template parameter names belong to this declarative region; any
other kind of name introduced by the *declaration* of a
*template-declaration* is instead introduced into the same declarative
region where it would be introduced as a result of a non-template
declaration of the same name.

[*Example 1*:

``` cpp
namespace N {
  template<class T> struct A { };               // #1
  template<class U> void f(U) { }               // #2
  struct B {
    template<class V> friend int g(struct C*);  // #3
  };
}
```

The declarative regions of `T`, `U` and `V` are the
*template-declaration*s on lines \#1, \#2, and \#3, respectively. But
the names `A`, `f`, `g` and `C` all belong to the same declarative
region — namely, the *namespace-body* of `N`. (`g` is still considered
to belong to this declarative region in spite of its being hidden during
qualified and unqualified name lookup.)

— *end example*]

The potential scope of a template parameter name begins at its point of
declaration [[basic.scope.pdecl]] and ends at the end of its declarative
region.

[*Note 1*:

This implies that a *template-parameter* can be used in the declaration
of subsequent *template-parameter*s and their default arguments but
cannot be used in preceding *template-parameter*s or their default
arguments. For example,

``` cpp
template<class T, T* p, class U = T> class X { ... };
template<class T> void f(T* p = new T);
```

This also implies that a *template-parameter* can be used in the
specification of base classes. For example,

``` cpp
template<class T> class X : public Array<T> { ... };
template<class T> class Y : public T { ... };
```

The use of a template parameter as a base class implies that a class
used as a template argument must be defined and not just declared when
the class template is instantiated.

— *end note*]

The declarative region of the name of a template parameter is nested
within the immediately-enclosing declarative region.

[*Note 2*:

As a result, a *template-parameter* hides any entity with the same name
in an enclosing scope [[basic.scope.hiding]].

[*Example 2*:

``` cpp
typedef int N;
template<N X, typename N, template<N Y> class T> struct A;
```

Here, `X` is a non-type template parameter of type `int` and `Y` is a
non-type template parameter of the same type as the second template
parameter of `A`.

— *end example*]

— *end note*]

[*Note 3*: Because the name of a template parameter cannot be
redeclared within its potential scope [[temp.local]], a template
parameter’s scope is often its potential scope. However, it is still
possible for a template parameter name to be hidden; see 
[[temp.local]]. — *end note*]

### Name hiding <a id="basic.scope.hiding">[[basic.scope.hiding]]</a>

A declaration of a name in a nested declarative region hides a
declaration of the same name in an enclosing declarative region; see
[[basic.scope.declarative]] and [[basic.lookup.unqual]].

If a class name [[class.name]] or enumeration name [[dcl.enum]] and a
variable, data member, function, or enumerator are declared in the same
declarative region (in any order) with the same name (excluding
declarations made visible via *using-directive*s
[[basic.lookup.unqual]]), the class or enumeration name is hidden
wherever the variable, data member, function, or enumerator name is
visible.

In a member function definition, the declaration of a name at block
scope hides the declaration of a member of the class with the same name;
see  [[basic.scope.class]]. The declaration of a member in a derived
class [[class.derived]] hides the declaration of a member of a base
class of the same name; see  [[class.member.lookup]].

During the lookup of a name qualified by a namespace name, declarations
that would otherwise be made visible by a *using-directive* can be
hidden by declarations with the same name in the namespace containing
the *using-directive*; see  [[namespace.qual]].

If a name is in scope and is not hidden it is said to be *visible*.

## Name lookup <a id="basic.lookup">[[basic.lookup]]</a>

The name lookup rules apply uniformly to all names (including
*typedef-name*s [[dcl.typedef]], *namespace-name*s [[basic.namespace]],
and *class-name*s [[class.name]]) wherever the grammar allows such names
in the context discussed by a particular rule. Name lookup associates
the use of a name with a set of declarations [[basic.def]] of that name.
If the declarations found by name lookup all denote functions or
function templates, the declarations are said to form an *overload set*.
The declarations found by name lookup shall either all denote the same
entity or form an overload set. Overload resolution ([[over.match]],
[[over.over]]) takes place after name lookup has succeeded. The access
rules [[class.access]] are considered only once name lookup and function
overload resolution (if applicable) have succeeded. Only after name
lookup, function overload resolution (if applicable) and access checking
have succeeded are the semantic properties introduced by the name’s
declaration and its reachable [[module.reach]] redeclarations used
further in expression processing [[expr]].

A name “looked up in the context of an expression” is looked up in the
scope where the expression is found.

The injected-class-name of a class [[class.pre]] is also considered to
be a member of that class for the purposes of name hiding and lookup.

[*Note 1*:  [[basic.link]] discusses linkage issues. The notions of
scope, point of declaration and name hiding are discussed in 
[[basic.scope]]. — *end note*]

### Unqualified name lookup <a id="basic.lookup.unqual">[[basic.lookup.unqual]]</a>

In all the cases listed in  [[basic.lookup.unqual]], the scopes are
searched for a declaration in the order listed in each of the respective
categories; name lookup ends as soon as a declaration is found for the
name. If no declaration is found, the program is ill-formed.

The declarations from the namespace nominated by a *using-directive*
become visible in a namespace enclosing the *using-directive*; see 
[[namespace.udir]]. For the purpose of the unqualified name lookup rules
described in  [[basic.lookup.unqual]], the declarations from the
namespace nominated by the *using-directive* are considered members of
that enclosing namespace.

The lookup for an unqualified name used as the *postfix-expression* of a
function call is described in  [[basic.lookup.argdep]].

[*Note 1*:

For purposes of determining (during parsing) whether an expression is a
*postfix-expression* for a function call, the usual name lookup rules
apply. In some cases a name followed by `<` is treated as a
*template-name* even though name lookup did not find a *template-name*
(see [[temp.names]]). For example,

``` cpp
int h;
void g();
namespace N {
  struct A {};
  template <class T> int f(T);
  template <class T> int g(T);
  template <class T> int h(T);
}

int x = f<N::A>(N::A());        // OK: lookup of f finds nothing, f treated as template name
int y = g<N::A>(N::A());        // OK: lookup of g finds a function, g treated as template name
int z = h<N::A>(N::A());        // error: h< does not begin a template-id
```

The rules in  [[basic.lookup.argdep]] have no effect on the syntactic
interpretation of an expression. For example,

``` cpp
typedef int f;
namespace N {
  struct A {
    friend void f(A &);
    operator int();
    void g(A a) {
      int i = f(a);             // f is the typedef, not the friend function: equivalent to int(a)
    }
  };
}
```

Because the expression is not a function call, the argument-dependent
name lookup [[basic.lookup.argdep]] does not apply and the friend
function `f` is not found.

— *end note*]

A name used in global scope, outside of any function, class or
user-declared namespace, shall be declared before its use in global
scope.

A name used in a user-declared namespace outside of the definition of
any function or class shall be declared before its use in that namespace
or before its use in a namespace enclosing its namespace.

In the definition of a function that is a member of namespace `N`, a
name used after the function’s *declarator-id*[^3] shall be declared
before its use in the block in which it is used or in one of its
enclosing blocks [[stmt.block]] or shall be declared before its use in
namespace `N` or, if `N` is a nested namespace, shall be declared before
its use in one of `N`’s enclosing namespaces.

[*Example 1*:

``` cpp
namespace A {
  namespace N {
    void f();
  }
}
void A::N::f() {
  i = 5;
  // The following scopes are searched for a declaration of i:
  // 1) outermost block scope of A::N::f, before the use of i
  // 2) scope of namespace N
  // 3) scope of namespace A
  // 4) global scope, before the definition of A::N::f
}
```

— *end example*]

A name used in the definition of a class `X` [^4] outside of a
complete-class context [[class.mem]] of `X` shall be declared in one of
the following ways:

- before its use in class `X` or be a member of a base class of `X`
  [[class.member.lookup]], or
- if `X` is a nested class of class `Y` [[class.nest]], before the
  definition of `X` in `Y`, or shall be a member of a base class of `Y`
  (this lookup applies in turn to `Y`’s enclosing classes, starting with
  the innermost enclosing class),[^5] or
- if `X` is a local class [[class.local]] or is a nested class of a
  local class, before the definition of class `X` in a block enclosing
  the definition of class `X`, or
- if `X` is a member of namespace `N`, or is a nested class of a class
  that is a member of `N`, or is a local class or a nested class within
  a local class of a function that is a member of `N`, before the
  definition of class `X` in namespace `N` or in one of `N`’s enclosing
  namespaces.

[*Example 2*:

``` cpp
namespace M {
  class B { };
}
```

``` cpp
namespace N {
  class Y : public M::B {
    class X {
      int a[i];
    };
  };
}

// The following scopes are searched for a declaration of i:
// 1) scope of class N::Y::X, before the use of i
// 2) scope of class N::Y, before the definition of N::Y::X
// 3) scope of N::Y's base class M::B
// 4) scope of namespace N, before the definition of N::Y
// 5) global scope, before the definition of N
```

— *end example*]

[*Note 2*: When looking for a prior declaration of a class or function
introduced by a friend declaration, scopes outside of the innermost
enclosing namespace scope are not considered; see 
[[namespace.memdef]]. — *end note*]

[*Note 3*:  [[basic.scope.class]] further describes the restrictions on
the use of names in a class definition. [[class.nest]] further describes
the restrictions on the use of names in nested class definitions.
[[class.local]] further describes the restrictions on the use of names
in local class definitions. — *end note*]

For the members of a class `X`, a name used in a complete-class context
[[class.mem]] of `X` or in the definition of a class member outside of
the definition of `X`, following the member’s *declarator-id*[^6], shall
be declared in one of the following ways:

- before its use in the block in which it is used or in an enclosing
  block [[stmt.block]], or
- shall be a member of class `X` or be a member of a base class of `X`
  [[class.member.lookup]], or
- if `X` is a nested class of class `Y` [[class.nest]], shall be a
  member of `Y`, or shall be a member of a base class of `Y` (this
  lookup applies in turn to `Y`’s enclosing classes, starting with the
  innermost enclosing class),[^7] or
- if `X` is a local class [[class.local]] or is a nested class of a
  local class, before the definition of class `X` in a block enclosing
  the definition of class `X`, or
- if `X` is a member of namespace `N`, or is a nested class of a class
  that is a member of `N`, or is a local class or a nested class within
  a local class of a function that is a member of `N`, before the use of
  the name, in namespace `N` or in one of `N`’s enclosing namespaces.

[*Example 3*:

``` cpp
class B { };
namespace M {
  namespace N {
    class X : public B {
      void f();
    };
  }
}
void M::N::X::f() {
  i = 16;
}

// The following scopes are searched for a declaration of i:
// 1) outermost block scope of M::N::X::f, before the use of i
// 2) scope of class M::N::X
// 3) scope of M::N::X's base class B
// 4) scope of namespace M::N
// 5) scope of namespace M
// 6) global scope, before the definition of M::N::X::f
```

— *end example*]

[*Note 4*:  [[class.mfct]] and  [[class.static]] further describe the
restrictions on the use of names in member function definitions.
[[class.nest]] further describes the restrictions on the use of names in
the scope of nested classes. [[class.local]] further describes the
restrictions on the use of names in local class
definitions. — *end note*]

Name lookup for a name used in the definition of a friend function
[[class.friend]] defined inline in the class granting friendship shall
proceed as described for lookup in member function definitions. If the
friend function is not defined in the class granting friendship, name
lookup in the friend function definition shall proceed as described for
lookup in namespace member function definitions.

In a friend declaration naming a member function, a name used in the
function declarator and not part of a *template-argument* in the
*declarator-id* is first looked up in the scope of the member function’s
class [[class.member.lookup]]. If it is not found, or if the name is
part of a *template-argument* in the *declarator-id*, the look up is as
described for unqualified names in the definition of the class granting
friendship.

[*Example 4*:

``` cpp
struct A {
  typedef int AT;
  void f1(AT);
  void f2(float);
  template <class T> void f3();
};
struct B {
  typedef char AT;
  typedef float BT;
  friend void A::f1(AT);        // parameter type is A::AT
  friend void A::f2(BT);        // parameter type is B::BT
  friend void A::f3<AT>();      // template argument is B::AT
};
```

— *end example*]

During the lookup for a name used as a default argument
[[dcl.fct.default]] in a function *parameter-declaration-clause* or used
in the *expression* of a *mem-initializer* for a constructor
[[class.base.init]], the function parameter names are visible and hide
the names of entities declared in the block, class or namespace scopes
containing the function declaration.

[*Note 5*:  [[dcl.fct.default]] further describes the restrictions on
the use of names in default arguments. [[class.base.init]] further
describes the restrictions on the use of names in a
*ctor-initializer*. — *end note*]

During the lookup of a name used in the *constant-expression* of an
*enumerator-definition*, previously declared *enumerator*s of the
enumeration are visible and hide the names of entities declared in the
block, class, or namespace scopes containing the *enum-specifier*.

A name used in the definition of a `static` data member of class `X`
[[class.static.data]] (after the *qualified-id* of the static member) is
looked up as if the name was used in a member function of `X`.

[*Note 6*:  [[class.static.data]] further describes the restrictions on
the use of names in the definition of a `static` data
member. — *end note*]

If a variable member of a namespace is defined outside of the scope of
its namespace then any name that appears in the definition of the member
(after the *declarator-id*) is looked up as if the definition of the
member occurred in its namespace.

[*Example 5*:

``` cpp
namespace N {
  int i = 4;
  extern int j;
}

int i = 2;

int N::j = i;       // N::j == 4
```

— *end example*]

A name used in the handler for a *function-try-block* [[except.pre]] is
looked up as if the name was used in the outermost block of the function
definition. In particular, the function parameter names shall not be
redeclared in the *exception-declaration* nor in the outermost block of
a handler for the *function-try-block*. Names declared in the outermost
block of the function definition are not found when looked up in the
scope of a handler for the *function-try-block*.

[*Note 7*: But function parameter names are found. — *end note*]

[*Note 8*: The rules for name lookup in template definitions are
described in  [[temp.res]]. — *end note*]

### Argument-dependent name lookup <a id="basic.lookup.argdep">[[basic.lookup.argdep]]</a>

When the *postfix-expression* in a function call [[expr.call]] is an
*unqualified-id*, other namespaces not considered during the usual
unqualified lookup [[basic.lookup.unqual]] may be searched, and in those
namespaces, namespace-scope friend function or function template
declarations [[class.friend]] not otherwise visible may be found. These
modifications to the search depend on the types of the arguments (and
for template template arguments, the namespace of the template
argument).

[*Example 1*:

``` cpp
namespace N {
  struct S { };
  void f(S);
}

void g() {
  N::S s;
  f(s);             // OK: calls N::f
  (f)(s);           // error: N::f not considered; parentheses prevent argument-dependent lookup
}
```

— *end example*]

For each argument type `T` in the function call, there is a set of zero
or more *associated namespaces* and a set of zero or more *associated
entities* (other than namespaces) to be considered. The sets of
namespaces and entities are determined entirely by the types of the
function arguments (and the namespace of any template template
argument). Typedef names and *using-declaration*s used to specify the
types do not contribute to this set. The sets of namespaces and entities
are determined in the following way:

- If `T` is a fundamental type, its associated sets of namespaces and
  entities are both empty.
- If `T` is a class type (including unions), its associated entities
  are: the class itself; the class of which it is a member, if any; and
  its direct and indirect base classes. Its associated namespaces are
  the innermost enclosing namespaces of its associated entities.
  Furthermore, if `T` is a class template specialization, its associated
  namespaces and entities also include: the namespaces and entities
  associated with the types of the template arguments provided for
  template type parameters (excluding template template parameters); the
  templates used as template template arguments; the namespaces of which
  any template template arguments are members; and the classes of which
  any member templates used as template template arguments are members.
  \[*Note 1*: Non-type template arguments do not contribute to the set
  of associated namespaces. — *end note*]
- If `T` is an enumeration type, its associated namespace is the
  innermost enclosing namespace of its declaration, and its associated
  entities are `T` and, if it is a class member, the member’s class.
- If `T` is a pointer to `U` or an array of `U`, its associated
  namespaces and entities are those associated with `U`.
- If `T` is a function type, its associated namespaces and entities are
  those associated with the function parameter types and those
  associated with the return type.
- If `T` is a pointer to a member function of a class `X`, its
  associated namespaces and entities are those associated with the
  function parameter types and return type, together with those
  associated with `X`.
- If `T` is a pointer to a data member of class `X`, its associated
  namespaces and entities are those associated with the member type
  together with those associated with `X`.

If an associated namespace is an inline namespace [[namespace.def]], its
enclosing namespace is also included in the set. If an associated
namespace directly contains inline namespaces, those inline namespaces
are also included in the set. In addition, if the argument is the name
or address of an overload set, its associated entities and namespaces
are the union of those associated with each of the members of the set,
i.e., the entities and namespaces associated with its parameter types
and return type. Additionally, if the aforementioned overload set is
named with a *template-id*, its associated entities and namespaces also
include those of its type *template-argument*s and its template
*template-argument*s.

Let *X* be the lookup set produced by unqualified lookup
[[basic.lookup.unqual]] and let *Y* be the lookup set produced by
argument dependent lookup (defined as follows). If *X* contains

- a declaration of a class member, or
- a block-scope function declaration that is not a *using-declaration*,
  or
- a declaration that is neither a function nor a function template

then *Y* is empty. Otherwise *Y* is the set of declarations found in the
namespaces associated with the argument types as described below. The
set of declarations found by the lookup of the name is the union of *X*
and *Y*.

[*Note 2*: The namespaces and entities associated with the argument
types can include namespaces and entities already considered by the
ordinary unqualified lookup. — *end note*]

[*Example 2*:

``` cpp
namespace NS {
  class T { };
  void f(T);
  void g(T, int);
}
NS::T parm;
void g(NS::T, float);
int main() {
  f(parm);                      // OK: calls NS::f
  extern void g(NS::T, float);
  g(parm, 1);                   // OK: calls g(NS::T, float)
}
```

— *end example*]

When considering an associated namespace `N`, the lookup is the same as
the lookup performed when `N` is used as a qualifier [[namespace.qual]]
except that:

- Any *using-directive*s in `N` are ignored.
- All names except those of (possibly overloaded) functions and function
  templates are ignored.
- Any namespace-scope friend functions or friend function templates
  [[class.friend]] declared in classes with reachable definitions in the
  set of associated entities are visible within their respective
  namespaces even if they are not visible during an ordinary lookup
  [[namespace.memdef]].
- Any exported declaration `D` in `N` declared within the purview of a
  named module `M` [[module.interface]] is visible if there is an
  associated entity attached to `M` with the same innermost enclosing
  non-inline namespace as `D`.
- If the lookup is for a dependent name ([[temp.dep]],
  [[temp.dep.candidate]]), any declaration `D` in `N` is visible if `D`
  would be visible to qualified name lookup [[namespace.qual]] at any
  point in the instantiation context [[module.context]] of the lookup,
  unless `D` is declared in another translation unit, attached to the
  global module, and is either discarded [[module.global.frag]] or has
  internal linkage.

[*Example 3*:

Translation unit #1

``` cpp
export module M;
namespace R {
  export struct X {};
  export void f(X);
}
namespace S {
  export void f(R::X, R::X);
}
```

Translation unit #2

``` cpp
export module N;
import M;
export R::X make();
namespace R { static int g(X); }
export template<typename T, typename U> void apply(T t, U u) {
  f(t, u);
  g(t);
}
```

Translation unit #3

``` cpp
module Q;
import N;
namespace S {
  struct Z { template<typename T> operator T(); };
}
void test() {
  auto x = make();              // OK, decltype(x) is R::X in module M
  R::f(x);                      // error: R and R::f are not visible here
  f(x);                         // OK, calls R::f from interface of M
  f(x, S::Z());                 // error: S::f in module M not considered
                                // even though S is an associated namespace
  apply(x, S::Z());             // error: S::f is visible in instantiation context, but
                                // R::g has internal linkage and cannot be used outside TU #2
}
```

— *end example*]

### Qualified name lookup <a id="basic.lookup.qual">[[basic.lookup.qual]]</a>

The name of a class or namespace member or enumerator can be referred to
after the `::` scope resolution operator [[expr.prim.id.qual]] applied
to a *nested-name-specifier* that denotes its class, namespace, or
enumeration. If a `::` scope resolution operator in a
*nested-name-specifier* is not preceded by a *decltype-specifier*,
lookup of the name preceding that `::` considers only namespaces, types,
and templates whose specializations are types. If the name found does
not designate a namespace or a class, enumeration, or dependent type,
the program is ill-formed.

[*Example 1*:

``` cpp
class A {
public:
  static int n;
};
int main() {
  int A;
  A::n = 42;        // OK
  A b;              // error: A does not name a type
}
```

— *end example*]

[*Note 1*: Multiply qualified names, such as `N1::N2::N3::n`, can be
used to refer to members of nested classes [[class.nest]] or members of
nested namespaces. — *end note*]

In a declaration in which the *declarator-id* is a *qualified-id*, names
used before the *qualified-id* being declared are looked up in the
defining namespace scope; names following the *qualified-id* are looked
up in the scope of the member’s class or namespace.

[*Example 2*:

``` cpp
class X { };
class C {
  class X { };
  static const int number = 50;
  static X arr[number];
};
X C::arr[number];   // error:
                    // equivalent to ::X C::arr[C::number];
                    // and not to C::X C::arr[C::number];
```

— *end example*]

A name prefixed by the unary scope operator `::` [[expr.prim.id.qual]]
is looked up in global scope, in the translation unit where it is used.
The name shall be declared in global namespace scope or shall be a name
whose declaration is visible in global scope because of a
*using-directive* [[namespace.qual]]. The use of `::` allows a global
name to be referred to even if its identifier has been hidden
[[basic.scope.hiding]].

A name prefixed by a *nested-name-specifier* that nominates an
enumeration type shall represent an *enumerator* of that enumeration.

In a *qualified-id* of the form:

``` bnf
nested-name-specifierₒₚₜ type-name '::' '~' type-name
```

the second *type-name* is looked up in the same scope as the first.

[*Example 3*:

``` cpp
struct C {
  typedef int I;
};
typedef int I1, I2;
extern int* p;
extern int* q;
p->C::I::~I();      // I is looked up in the scope of C
q->I1::~I2();       // I2 is looked up in the scope of the postfix-expression

struct A {
  ~A();
};
typedef A AB;
int main() {
  AB* p;
  p->AB::~AB();     // explicitly calls the destructor for A
}
```

— *end example*]

[*Note 2*:  [[basic.lookup.classref]] describes how name lookup
proceeds after the `.` and `->` operators. — *end note*]

#### Class members <a id="class.qual">[[class.qual]]</a>

If the *nested-name-specifier* of a *qualified-id* nominates a class,
the name specified after the *nested-name-specifier* is looked up in the
scope of the class [[class.member.lookup]], except for the cases listed
below. The name shall represent one or more members of that class or of
one of its base classes [[class.derived]].

[*Note 1*: A class member can be referred to using a *qualified-id* at
any point in its potential scope [[basic.scope.class]]. — *end note*]

The exceptions to the name lookup rule above are the following:

- the lookup for a destructor is as specified in  [[basic.lookup.qual]];
- a *conversion-type-id* of a *conversion-function-id* is looked up in
  the same manner as a *conversion-type-id* in a class member access
  (see  [[basic.lookup.classref]]);
- the names in a *template-argument* of a *template-id* are looked up in
  the context in which the entire *postfix-expression* occurs;
- the lookup for a name specified in a *using-declaration*
  [[namespace.udecl]] also finds class or enumeration names hidden
  within the same scope [[basic.scope.hiding]].

In a lookup in which function names are not ignored[^8] and the
*nested-name-specifier* nominates a class `C`:

- if the name specified after the *nested-name-specifier*, when looked
  up in `C`, is the injected-class-name of `C` [[class.pre]], or
- in a *using-declarator* of a *using-declaration* [[namespace.udecl]]
  that is a *member-declaration*, if the name specified after the
  *nested-name-specifier* is the same as the *identifier* or the
  *simple-template-id*’s *template-name* in the last component of the
  *nested-name-specifier*,

the name is instead considered to name the constructor of class `C`.

[*Note 2*: For example, the constructor is not an acceptable lookup
result in an *elaborated-type-specifier* so the constructor would not be
used in place of the injected-class-name. — *end note*]

Such a constructor name shall be used only in the *declarator-id* of a
declaration that names a constructor or in a *using-declaration*.

[*Example 1*:

``` cpp
struct A { A(); };
struct B: public A { B(); };

A::A() { }
B::B() { }

B::A ba;            // object of type A
A::A a;             // error: A::A is not a type name
struct A::A a2;     // object of type A
```

— *end example*]

A class member name hidden by a name in a nested declarative region or
by the name of a derived class member can still be found if qualified by
the name of its class followed by the `::` operator.

#### Namespace members <a id="namespace.qual">[[namespace.qual]]</a>

If the *nested-name-specifier* of a *qualified-id* nominates a namespace
(including the case where the *nested-name-specifier* is `::`, i.e.,
nominating the global namespace), the name specified after the
*nested-name-specifier* is looked up in the scope of the namespace. The
names in a *template-argument* of a *template-id* are looked up in the
context in which the entire *postfix-expression* occurs.

For a namespace `X` and name `m`, the namespace-qualified lookup set
S(X, m) is defined as follows: Let S'(X, m) be the set of all
declarations of `m` in `X` and the inline namespace set of `X`
[[namespace.def]] whose potential scope [[basic.scope.namespace]] would
include the namespace in which `m` is declared at the location of the
*nested-name-specifier*. If S'(X, m) is not empty, S(X, m) is S'(X, m);
otherwise, S(X, m) is the union of S(Nᵢ, m) for all namespaces Nᵢ
nominated by *using-directive*s in `X` and its inline namespace set.

Given `X::m` (where `X` is a user-declared namespace), or given `::m`
(where X is the global namespace), if S(X, m) is the empty set, the
program is ill-formed. Otherwise, if S(X, m) has exactly one member, or
if the context of the reference is a *using-declaration*
[[namespace.udecl]], S(X, m) is the required set of declarations of `m`.
Otherwise if the use of `m` is not one that allows a unique declaration
to be chosen from S(X, m), the program is ill-formed.

[*Example 1*:

``` cpp
int x;
namespace Y {
  void f(float);
  void h(int);
}

namespace Z {
  void h(double);
}

namespace A {
  using namespace Y;
  void f(int);
  void g(int);
  int i;
}

namespace B {
  using namespace Z;
  void f(char);
  int i;
}

namespace AB {
  using namespace A;
  using namespace B;
  void g();
}

void h()
{
  AB::g();          // g is declared directly in AB, therefore S is { `AB::g()` } and AB::g() is chosen

  AB::f(1);         // f is not declared directly in AB so the rules are applied recursively to A and B;
                    // namespace Y is not searched and Y::f(float) is not considered;
                    // S is { `A::f(int)`, `B::f(char)` } and overload resolution chooses A::f(int)

  AB::f('c');       // as above but resolution chooses B::f(char)

  AB::x++;          // x is not declared directly in AB, and is not declared in A or B, so the rules
                    // are applied recursively to Y and Z, S is { } so the program is ill-formed

  AB::i++;          // i is not declared directly in AB so the rules are applied recursively to A and B,
                    // S is { `A::i`, `B::i` } so the use is ambiguous and the program is ill-formed

  AB::h(16.8);      // h is not declared directly in AB and not declared directly in A or B so the rules
                    // are applied recursively to Y and Z, S is { `Y::h(int)`, `Z::h(double)` } and
                    // overload resolution chooses Z::h(double)
}
```

— *end example*]

[*Note 1*:

The same declaration found more than once is not an ambiguity (because
it is still a unique declaration).

[*Example 2*:

``` cpp
namespace A {
  int a;
}

namespace B {
  using namespace A;
}

namespace C {
  using namespace A;
}

namespace BC {
  using namespace B;
  using namespace C;
}

void f()
{
  BC::a++;          // OK: S is { `A::a`, `A::a` }
}

namespace D {
  using A::a;
}

namespace BD {
  using namespace B;
  using namespace D;
}

void g()
{
  BD::a++;          // OK: S is { `A::a`, `A::a` }
}
```

— *end example*]

— *end note*]

[*Example 3*:

Because each referenced namespace is searched at most once, the
following is well-defined:

``` cpp
namespace B {
  int b;
}

namespace A {
  using namespace B;
  int a;
}

namespace B {
  using namespace A;
}

void f()
{
  A::a++;           // OK: a declared directly in A, S is { `A::a` }
  B::a++;           // OK: both A and B searched (once), S is { `A::a` }
  A::b++;           // OK: both A and B searched (once), S is { `B::b` }
  B::b++;           // OK: b declared directly in B, S is { `B::b` }
}
```

— *end example*]

During the lookup of a qualified namespace member name, if the lookup
finds more than one declaration of the member, and if one declaration
introduces a class name or enumeration name and the other declarations
introduce either the same variable, the same enumerator, or a set of
functions, the non-type name hides the class or enumeration name if and
only if the declarations are from the same namespace; otherwise (the
declarations are from different namespaces), the program is ill-formed.

[*Example 4*:

``` cpp
namespace A {
  struct x { };
  int x;
  int y;
}

namespace B {
  struct y { };
}

namespace C {
  using namespace A;
  using namespace B;
  int i = C::x;     // OK, A::x (of type int)
  int j = C::y;     // ambiguous, A::y or B::y
}
```

— *end example*]

In a declaration for a namespace member in which the *declarator-id* is
a *qualified-id*, given that the *qualified-id* for the namespace member
has the form

``` bnf
nested-name-specifier unqualified-id
```

the *unqualified-id* shall name a member of the namespace designated by
the *nested-name-specifier* or of an element of the inline namespace set
[[namespace.def]] of that namespace.

[*Example 5*:

``` cpp
namespace A {
  namespace B {
    void f1(int);
  }
  using namespace B;
}
void A::f1(int){ }  // error: f1 is not a member of A
```

— *end example*]

However, in such namespace member declarations, the
*nested-name-specifier* may rely on *using-directive*s to implicitly
provide the initial part of the *nested-name-specifier*.

[*Example 6*:

``` cpp
namespace A {
  namespace B {
    void f1(int);
  }
}

namespace C {
  namespace D {
    void f1(int);
  }
}

using namespace A;
using namespace C::D;
void B::f1(int){ }  // OK, defines A::B::f1(int)
```

— *end example*]

### Elaborated type specifiers <a id="basic.lookup.elab">[[basic.lookup.elab]]</a>

An *elaborated-type-specifier* [[dcl.type.elab]] may be used to refer to
a previously declared *class-name* or *enum-name* even though the name
has been hidden by a non-type declaration [[basic.scope.hiding]].

If the *elaborated-type-specifier* has no *nested-name-specifier*, and
unless the *elaborated-type-specifier* appears in a declaration with the
following form:

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
```

the *identifier* is looked up according to  [[basic.lookup.unqual]] but
ignoring any non-type names that have been declared. If the
*elaborated-type-specifier* is introduced by the `enum` keyword and this
lookup does not find a previously declared *type-name*, the
*elaborated-type-specifier* is ill-formed. If the
*elaborated-type-specifier* is introduced by the *class-key* and this
lookup does not find a previously declared *type-name*, or if the
*elaborated-type-specifier* appears in a declaration with the form:

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
```

the *elaborated-type-specifier* is a declaration that introduces the
*class-name* as described in  [[basic.scope.pdecl]].

If the *elaborated-type-specifier* has a *nested-name-specifier*,
qualified name lookup is performed, as described in 
[[basic.lookup.qual]], but ignoring any non-type names that have been
declared. If the name lookup does not find a previously declared
*type-name*, the *elaborated-type-specifier* is ill-formed.

[*Example 1*:

``` cpp
struct Node {
  struct Node* Next;            // OK: Refers to injected-class-name Node
  struct Data* Data;            // OK: Declares type Data at global scope and member Data
};

struct Data {
  struct Node* Node;            // OK: Refers to Node at global scope
  friend struct ::Glob;         // error: Glob is not declared, cannot introduce a qualified type[dcl.type.elab]
  friend struct Glob;           // OK: Refers to (as yet) undeclared Glob at global scope.
  ...
};

struct Base {
  struct Data;                  // OK: Declares nested Data
  struct ::Data*     thatData;  // OK: Refers to ::Data
  struct Base::Data* thisData;  // OK: Refers to nested Data
  friend class ::Data;          // OK: global Data is a friend
  friend class Data;            // OK: nested Data is a friend
  struct Data { ... };    // Defines nested Data
};

struct Data;                    // OK: Redeclares Data at global scope
struct ::Data;                  // error: cannot introduce a qualified type[dcl.type.elab]
struct Base::Data;              // error: cannot introduce a qualified type[dcl.type.elab]
struct Base::Datum;             // error: Datum undefined
struct Base::Data* pBase;       // OK: refers to nested Data
```

— *end example*]

### Class member access <a id="basic.lookup.classref">[[basic.lookup.classref]]</a>

In a class member access expression [[expr.ref]], if the `.` or `->`
token is immediately followed by an *identifier* followed by a `<`, the
identifier must be looked up to determine whether the `<` is the
beginning of a template argument list [[temp.names]] or a less-than
operator. The identifier is first looked up in the class of the object
expression [[class.member.lookup]]. If the identifier is not found, it
is then looked up in the context of the entire *postfix-expression* and
shall name a template whose specializations are types.

If the *id-expression* in a class member access [[expr.ref]] is an
*unqualified-id*, and the type of the object expression is of a class
type `C`, the *unqualified-id* is looked up in the scope of class `C`
[[class.member.lookup]].

If the *unqualified-id* is `~`*type-name*, the *type-name* is looked up
in the context of the entire *postfix-expression*. If the type `T` of
the object expression is of a class type `C`, the *type-name* is also
looked up in the scope of class `C`. At least one of the lookups shall
find a name that refers to cv `T`.

[*Example 1*:

``` cpp
struct A { };

struct B {
  struct A { };
  void f(::A* a);
};

void B::f(::A* a) {
  a->~A();                      // OK: lookup in *a finds the injected-class-name
}
```

— *end example*]

If the *id-expression* in a class member access is a *qualified-id* of
the form

``` cpp
class-name-or-namespace-name::...
```

the `class-name-or-namespace-name` following the `.` or `->` operator is
first looked up in the class of the object expression
[[class.member.lookup]] and the name, if found, is used. Otherwise it is
looked up in the context of the entire *postfix-expression*.

[*Note 1*: See  [[basic.lookup.qual]], which describes the lookup of a
name before `::`, which will only find a type or namespace
name. — *end note*]

If the *qualified-id* has the form

``` cpp
::class-name-or-namespace-name::...
```

the `class-name-or-namespace-name` is looked up in global scope as a
*class-name* or *namespace-name*.

If the *nested-name-specifier* contains a *simple-template-id*
[[temp.names]], the names in its *template-argument*s are looked up in
the context in which the entire *postfix-expression* occurs.

If the *id-expression* is a *conversion-function-id*, its
*conversion-type-id* is first looked up in the class of the object
expression [[class.member.lookup]] and the name, if found, is used.
Otherwise it is looked up in the context of the entire
*postfix-expression*. In each of these lookups, only names that denote
types or templates whose specializations are types are considered.

[*Example 2*:

``` cpp
struct A { };
namespace N {
  struct A {
    void g() { }
    template <class T> operator T();
  };
}

int main() {
  N::A a;
  a.operator A();               // calls N::A::operator N::A
}
```

— *end example*]

### Using-directives and namespace aliases <a id="basic.lookup.udir">[[basic.lookup.udir]]</a>

In a *using-directive* or *namespace-alias-definition*, during the
lookup for a *namespace-name* or for a name in a *nested-name-specifier*
only namespace names are considered.

## Program and linkage <a id="basic.link">[[basic.link]]</a>

A *program* consists of one or more translation units [[lex.separate]]
linked together. A translation unit consists of a sequence of
declarations.

``` bnf
translation-unit:
    declaration-seqₒₚₜ 
    global-module-fragmentₒₚₜ module-declaration declaration-seqₒₚₜ private-module-fragmentₒₚₜ
```

A name is said to have *linkage* when it might denote the same object,
reference, function, type, template, namespace or value as a name
introduced by a declaration in another scope:

- When a name has *external linkage*, the entity it denotes can be
  referred to by names from scopes of other translation units or from
  other scopes of the same translation unit.
- When a name has *module linkage*, the entity it denotes can be
  referred to by names from other scopes of the same module unit
  [[module.unit]] or from scopes of other module units of that same
  module.
- When a name has *internal linkage*, the entity it denotes can be
  referred to by names from other scopes in the same translation unit.
- When a name has *no linkage*, the entity it denotes cannot be referred
  to by names from other scopes.

A name having namespace scope [[basic.scope.namespace]] has internal
linkage if it is the name of

- a variable, variable template, function, or function template that is
  explicitly declared `static`; or
- a non-template variable of non-volatile const-qualified type, unless
  - it is explicitly declared `extern`, or
  - it is inline or exported, or
  - it was previously declared and the prior declaration did not have
    internal linkage; or
- a data member of an anonymous union.

[*Note 1*: An instantiated variable template that has const-qualified
type can have external or module linkage, even if not declared
`extern`. — *end note*]

An unnamed namespace or a namespace declared directly or indirectly
within an unnamed namespace has internal linkage. All other namespaces
have external linkage. A name having namespace scope that has not been
given internal linkage above and that is the name of

- a variable; or
- a function; or
- a named class [[class.pre]], or an unnamed class defined in a typedef
  declaration in which the class has the typedef name for linkage
  purposes [[dcl.typedef]]; or
- a named enumeration [[dcl.enum]], or an unnamed enumeration defined in
  a typedef declaration in which the enumeration has the typedef name
  for linkage purposes [[dcl.typedef]]; or
- an unnamed enumeration that has an enumerator as a name for linkage
  purposes [[dcl.enum]]; or
- a template

has its linkage determined as follows:

- if the enclosing namespace has internal linkage, the name has internal
  linkage;
- otherwise, if the declaration of the name is attached to a named
  module [[module.unit]] and is not exported [[module.interface]], the
  name has module linkage;
- otherwise, the name has external linkage.

In addition, a member function, static data member, a named class or
enumeration of class scope, or an unnamed class or enumeration defined
in a class-scope typedef declaration such that the class or enumeration
has the typedef name for linkage purposes [[dcl.typedef]], has the same
linkage, if any, as the name of the class of which it is a member.

The name of a function declared in block scope and the name of a
variable declared by a block scope `extern` declaration have linkage. If
such a declaration is attached to a named module, the program is
ill-formed. If there is a visible declaration of an entity with linkage,
ignoring entities declared outside the innermost enclosing namespace
scope, such that the block scope declaration would be a (possibly
ill-formed) redeclaration if the two declarations appeared in the same
declarative region, the block scope declaration declares that same
entity and receives the linkage of the previous declaration. If there is
more than one such matching entity, the program is ill-formed.
Otherwise, if no matching entity is found, the block scope entity
receives external linkage. If, within a translation unit, the same
entity is declared with both internal and external linkage, the program
is ill-formed.

[*Example 1*:

``` cpp
static void f();
extern "C" void h();
static int i = 0;               // #1
void g() {
  extern void f();              // internal linkage
  extern void h();              // C language linkage
  int i;                        // #2: i has no linkage
  {
    extern void f();            // internal linkage
    extern int i;               // #3: external linkage, ill-formed
  }
}
```

Without the declaration at line \#2, the declaration at line \#3 would
link with the declaration at line \#1. Because the declaration with
internal linkage is hidden, however, \#3 is given external linkage,
making the program ill-formed.

— *end example*]

When a block scope declaration of an entity with linkage is not found to
refer to some other declaration, then that entity is a member of the
innermost enclosing namespace. However such a declaration does not
introduce the member name in its namespace scope.

[*Example 2*:

``` cpp
namespace X {
  void p() {
    q();                        // error: q not yet declared
    extern void q();            // q is a member of namespace X
  }

  void middle() {
    q();                        // error: q not yet declared
  }

  void q() { ... }        // definition of X::q
}

void q() { ... }          // some other, unrelated q
```

— *end example*]

Names not covered by these rules have no linkage. Moreover, except as
noted, a name declared at block scope [[basic.scope.block]] has no
linkage.

Two names that are the same [[basic.pre]] and that are declared in
different scopes shall denote the same variable, function, type,
template or namespace if

- both names have external or module linkage and are declared in
  declarations attached to the same module, or else both names have
  internal linkage and are declared in the same translation unit; and
- both names refer to members of the same namespace or to members, not
  by inheritance, of the same class; and
- when both names denote functions or function templates, the
  signatures ([[defns.signature]], [[defns.signature.templ]]) are the
  same.

If multiple declarations of the same name with external linkage would
declare the same entity except that they are attached to different
modules, the program is ill-formed; no diagnostic is required.

[*Note 2*: *using-declaration*s, typedef declarations, and
*alias-declaration*s do not declare entities, but merely introduce
synonyms. Similarly, *using-directive*s do not declare entities.
Enumerators do not have linkage, but may serve as the name of an
enumeration with linkage [[dcl.enum]]. — *end note*]

If a declaration would redeclare a reachable declaration attached to a
different module, the program is ill-formed.

[*Example 3*:

\`"decls.h"\`

``` cpp
int f();            // #1, attached to the global module
int g();            // #2, attached to the global module
```

Module interface of \`M\`

``` cpp
module;
#include "decls.h"
export module M;
export using ::f;   // OK: does not declare an entity, exports #1
int g();            // error: matches #2, but attached to M
export int h();     // #3
export int k();     // #4
```

Other translation unit

``` cpp
import M;
static int h();     // error: matches #3
int k();            // error: matches #4
```

— *end example*]

As a consequence of these rules, all declarations of an entity are
attached to the same module; the entity is said to be *attached* to that
module.

After all adjustments of types (during which typedefs [[dcl.typedef]]
are replaced by their definitions), the types specified by all
declarations referring to a given variable or function shall be
identical, except that declarations for an array object can specify
array types that differ by the presence or absence of a major array
bound [[dcl.array]]. A violation of this rule on type identity does not
require a diagnostic.

[*Note 3*: Linkage to non-C++ declarations can be achieved using a
*linkage-specification* [[dcl.link]]. — *end note*]

A declaration D *names* an entity E if

- D contains a *lambda-expression* whose closure type is E,
- E is not a function or function template and D contains an
  *id-expression*, *type-specifier*, *nested-name-specifier*,
  *template-name*, or *concept-name* denoting E, or
- E is a function or function template and D contains an expression that
  names E [[basic.def.odr]] or an *id-expression* that refers to a set
  of overloads that contains E. \[*Note 4*: Non-dependent names in an
  instantiated declaration do not refer to a set of overloads
  [[temp.nondep]]. — *end note*]

A declaration is an *exposure* if it either names a TU-local entity
(defined below), ignoring

- the *function-body* for a non-inline function or function template
  (but not the deduced return type for a (possibly instantiated)
  definition of a function with a declared return type that uses a
  placeholder type [[dcl.spec.auto]]),
- the *initializer* for a variable or variable template (but not the
  variable’s type),
- friend declarations in a class definition, and
- any reference to a non-volatile const object or reference with
  internal or no linkage initialized with a constant expression that is
  not an odr-use [[basic.def.odr]],

or defines a constexpr variable initialized to a TU-local value (defined
below).

[*Note 5*: An inline function template can be an exposure even though
explicit specializations of it might be usable in other translation
units. — *end note*]

An entity is *TU-local* if it is

- a type, function, variable, or template that
  - has a name with internal linkage, or
  - does not have a name with linkage and is declared, or introduced by
    a *lambda-expression*, within the definition of a TU-local entity,
- a type with no name that is defined outside a *class-specifier*,
  function body, or *initializer* or is introduced by a
  *defining-type-specifier* that is used to declare only TU-local
  entities,
- a specialization of a TU-local template,
- a specialization of a template with any TU-local template argument, or
- a specialization of a template whose (possibly instantiated)
  declaration is an exposure. \[*Note 6*: The specialization might have
  been implicitly or explicitly instantiated. — *end note*]

A value or object is *TU-local* if either

- it is, or is a pointer to, a TU-local function or the object
  associated with a TU-local variable,
- it is an object of class or array type and any of its subobjects or
  any of the objects or functions to which its non-static data members
  of reference type refer is TU-local and is usable in constant
  expressions.

If a (possibly instantiated) declaration of, or a deduction guide for, a
non-TU-local entity in a module interface unit (outside the
*private-module-fragment*, if any) or module partition [[module.unit]]
is an exposure, the program is ill-formed. Such a declaration in any
other context is deprecated [[depr.local]].

If a declaration that appears in one translation unit names a TU-local
entity declared in another translation unit that is not a header unit,
the program is ill-formed. A declaration instantiated for a template
specialization [[temp.spec]] appears at the point of instantiation of
the specialization [[temp.point]].

[*Example 4*:

Translation unit #1

``` cpp
export module A;
static void f() {}
inline void it() { f(); }           // error: is an exposure of f
static inline void its() { f(); }   // OK
template<int> void g() { its(); }   // OK
template void g<0>();

decltype(f) *fp;                    // error: f (though not its type) is TU-local
auto &fr = f;                       // OK
constexpr auto &fr2 = fr;           // error: is an exposure of f
constexpr static auto fp2 = fr;     // OK

struct S { void (&ref)(); } s{f};               // OK, value is TU-local
constexpr extern struct W { S &s; } wrap{s};    // OK, value is not TU-local

static auto x = []{f();};           // OK
auto x2 = x;                        // error: the closure type is TU-local
int y = ([]{f();}(),0);             // error: the closure type is not TU-local
int y2 = (x,0);                     // OK

namespace N {
  struct A {};
  void adl(A);
  static void adl(int);
}
void adl(double);

inline void h(auto x) { adl(x); }   // OK, but a specialization might be an exposure
```

Translation unit #2

``` cpp
module A;
void other() {
  g<0>();                           // OK, specialization is explicitly instantiated
  g<1>();                           // error: instantiation uses TU-local its
  h(N::A{});                        // error: overload set contains TU-local N::adl(int)
  h(0);                             // OK, calls adl(double)
  adl(N::A{});                      // OK; N::adl(int) not found, calls N::adl(N::A)
  fr();                             // OK, calls f
  constexpr auto ptr = fr;          // error: fr is not usable in constant expressions here
}
```

— *end example*]

## Memory and objects <a id="basic.memobj">[[basic.memobj]]</a>

### Memory model <a id="intro.memory">[[intro.memory]]</a>

The fundamental storage unit in the C++ memory model is the *byte*. A
byte is at least large enough to contain any member of the basic
execution character set [[lex.charset]] and the eight-bit code units of
the Unicode UTF-8 encoding form and is composed of a contiguous sequence
of bits,[^9] the number of which is *implementation-defined*. The least
significant bit is called the *low-order bit*; the most significant bit
is called the *high-order bit*. The memory available to a C++ program
consists of one or more sequences of contiguous bytes. Every byte has a
unique address.

[*Note 1*: The representation of types is described in 
[[basic.types]]. — *end note*]

A *memory location* is either an object of scalar type or a maximal
sequence of adjacent bit-fields all having nonzero width.

[*Note 2*: Various features of the language, such as references and
virtual functions, might involve additional memory locations that are
not accessible to programs but are managed by the
implementation. — *end note*]

Two or more threads of execution [[intro.multithread]] can access
separate memory locations without interfering with each other.

[*Note 3*: Thus a bit-field and an adjacent non-bit-field are in
separate memory locations, and therefore can be concurrently updated by
two threads of execution without interference. The same applies to two
bit-fields, if one is declared inside a nested struct declaration and
the other is not, or if the two are separated by a zero-length bit-field
declaration, or if they are separated by a non-bit-field declaration. It
is not safe to concurrently update two bit-fields in the same struct if
all fields between them are also bit-fields of nonzero
width. — *end note*]

[*Example 1*:

A class declared as

``` cpp
struct {
  char a;
  int b:5,
  c:11,
  :0,
  d:8;
  struct {int ee:8;} e;
}
```

contains four separate memory locations: The member `a` and bit-fields
`d` and `e.ee` are each separate memory locations, and can be modified
concurrently without interfering with each other. The bit-fields `b` and
`c` together constitute the fourth memory location. The bit-fields `b`
and `c` cannot be concurrently modified, but `b` and `a`, for example,
can be.

— *end example*]

### Object model <a id="intro.object">[[intro.object]]</a>

The constructs in a C++ program create, destroy, refer to, access, and
manipulate objects. An *object* is created by a definition
[[basic.def]], by a *new-expression* [[expr.new]], by an operation that
implicitly creates objects (see below), when implicitly changing the
active member of a union [[class.union]], or when a temporary object is
created ([[conv.rval]], [[class.temporary]]). An object occupies a
region of storage in its period of construction [[class.cdtor]],
throughout its lifetime [[basic.life]], and in its period of destruction
[[class.cdtor]].

[*Note 1*: A function is not an object, regardless of whether or not it
occupies storage in the way that objects do. — *end note*]

The properties of an object are determined when the object is created.
An object can have a name [[basic.pre]]. An object has a storage
duration [[basic.stc]] which influences its lifetime [[basic.life]]. An
object has a type [[basic.types]]. Some objects are polymorphic
[[class.virtual]]; the implementation generates information associated
with each such object that makes it possible to determine that object’s
type during program execution. For other objects, the interpretation of
the values found therein is determined by the type of the *expression*s
[[expr.compound]] used to access them.

Objects can contain other objects, called *subobjects*. A subobject can
be a *member subobject* [[class.mem]], a *base class subobject*
[[class.derived]], or an array element. An object that is not a
subobject of any other object is called a *complete object*. If an
object is created in storage associated with a member subobject or array
element *e* (which may or may not be within its lifetime), the created
object is a subobject of *e*’s containing object if:

- the lifetime of *e*’s containing object has begun and not ended, and
- the storage for the new object exactly overlays the storage location
  associated with *e*, and
- the new object is of the same type as *e* (ignoring cv-qualification).

If a complete object is created [[expr.new]] in storage associated with
another object *e* of type “array of N `unsigned char`” or of type
“array of N `std::byte`” [[cstddef.syn]], that array *provides storage*
for the created object if:

- the lifetime of *e* has begun and not ended, and
- the storage for the new object fits entirely within *e*, and
- there is no smaller array object that satisfies these constraints.

[*Note 2*: If that portion of the array previously provided storage for
another object, the lifetime of that object ends because its storage was
reused [[basic.life]]. — *end note*]

[*Example 1*:

``` cpp
template<typename ...T>
struct AlignedUnion {
  alignas(T...) unsigned char data[max(sizeof(T)...)];
};
int f() {
  AlignedUnion<int, char> au;
  int *p = new (au.data) int;           // OK, au.data provides storage
  char *c = new (au.data) char();       // OK, ends lifetime of *p
  char *d = new (au.data + 1) char();
  return *c + *d;                       // OK
}

struct A { unsigned char a[32]; };
struct B { unsigned char b[16]; };
A a;
B *b = new (a.a + 8) B;                 // a.a provides storage for *b
int *p = new (b->b + 4) int;            // b->b provides storage for *p
                                        // a.a does not provide storage for *p (directly),
                                        // but *p is nested within a (see below)
```

— *end example*]

An object *a* is *nested within* another object *b* if:

- *a* is a subobject of *b*, or
- *b* provides storage for *a*, or
- there exists an object *c* where *a* is nested within *c*, and *c* is
  nested within *b*.

For every object `x`, there is some object called the *complete object
of* `x`, determined as follows:

- If `x` is a complete object, then the complete object of `x` is
  itself.
- Otherwise, the complete object of `x` is the complete object of the
  (unique) object that contains `x`.

If a complete object, a data member [[class.mem]], or an array element
is of class type, its type is considered the *most derived class*, to
distinguish it from the class type of any base class subobject; an
object of a most derived class type or of a non-class type is called a
*most derived object*.

A *potentially-overlapping subobject* is either:

- a base class subobject, or
- a non-static data member declared with the `no_unique_address`
  attribute [[dcl.attr.nouniqueaddr]].

An object has nonzero size if it

- is not a potentially-overlapping subobject, or
- is not of class type, or
- is of a class type with virtual member functions or virtual base
  classes, or
- has subobjects of nonzero size or bit-fields of nonzero length.

Otherwise, if the object is a base class subobject of a standard-layout
class type with no non-static data members, it has zero size. Otherwise,
the circumstances under which the object has zero size are
*implementation-defined*. Unless it is a bit-field [[class.bit]], an
object with nonzero size shall occupy one or more bytes of storage,
including every byte that is occupied in full or in part by any of its
subobjects. An object of trivially copyable or standard-layout type
[[basic.types]] shall occupy contiguous bytes of storage.

Unless an object is a bit-field or a subobject of zero size, the address
of that object is the address of the first byte it occupies. Two objects
with overlapping lifetimes that are not bit-fields may have the same
address if one is nested within the other, or if at least one is a
subobject of zero size and they are of different types; otherwise, they
have distinct addresses and occupy disjoint bytes of storage.[^10]

[*Example 2*:

``` cpp
static const char test1 = 'x';
static const char test2 = 'x';
const bool b = &test1 != &test2;        // always true
```

— *end example*]

The address of a non-bit-field subobject of zero size is the address of
an unspecified byte of storage occupied by the complete object of that
subobject.

Some operations are described as *implicitly creating objects* within a
specified region of storage. For each operation that is specified as
implicitly creating objects, that operation implicitly creates and
starts the lifetime of zero or more objects of implicit-lifetime types
[[basic.types]] in its specified region of storage if doing so would
result in the program having defined behavior. If no such set of objects
would give the program defined behavior, the behavior of the program is
undefined. If multiple such sets of objects would give the program
defined behavior, it is unspecified which such set of objects is
created.

[*Note 3*: Such operations do not start the lifetimes of subobjects of
such objects that are not themselves of implicit-lifetime
types. — *end note*]

Further, after implicitly creating objects within a specified region of
storage, some operations are described as producing a pointer to a
*suitable created object*. These operations select one of the
implicitly-created objects whose address is the address of the start of
the region of storage, and produce a pointer value that points to that
object, if that value would result in the program having defined
behavior. If no such pointer value would give the program defined
behavior, the behavior of the program is undefined. If multiple such
pointer values would give the program defined behavior, it is
unspecified which such pointer value is produced.

[*Example 3*:

``` cpp
#include <cstdlib>
struct X { int a, b; };
X *make_x() {
  // The call to std::malloc implicitly creates an object of type X
  // and its subobjects a and b, and returns a pointer to that X object
  // (or an object that is pointer-interconvertible[basic.compound] with it),
  // in order to give the subsequent class member access operations
  // defined behavior.
  X *p = (X*)std::malloc(sizeof(struct X));
  p->a = 1;
  p->b = 2;
  return p;
}
```

— *end example*]

An operation that begins the lifetime of an array of `char`,
`unsigned char`, or `std::byte` implicitly creates objects within the
region of storage occupied by the array.

[*Note 4*: The array object provides storage for these
objects. — *end note*]

Any implicit or explicit invocation of a function named `operator new`
or `operator new[]` implicitly creates objects in the returned region of
storage and returns a pointer to a suitable created object.

[*Note 5*: Some functions in the C++ standard library implicitly create
objects ([[allocator.traits.members]], [[c.malloc]], [[cstring.syn]],
[[bit.cast]]). — *end note*]

### Lifetime <a id="basic.life">[[basic.life]]</a>

The *lifetime* of an object or reference is a runtime property of the
object or reference. A variable is said to have *vacuous initialization*
if it is default-initialized and, if it is of class type or a (possibly
multi-dimensional) array thereof, that class type has a trivial default
constructor. The lifetime of an object of type `T` begins when:

- storage with the proper alignment and size for type `T` is obtained,
  and
- its initialization (if any) is complete (including vacuous
  initialization) [[dcl.init]],

except that if the object is a union member or subobject thereof, its
lifetime only begins if that union member is the initialized member in
the union ([[dcl.init.aggr]], [[class.base.init]]), or as described in
[[class.union]] and [[class.copy.ctor]], and except as described in
[[allocator.members]]. The lifetime of an object *o* of type `T` ends
when:

- if `T` is a non-class type, the object is destroyed, or
- if `T` is a class type, the destructor call starts, or
- the storage which the object occupies is released, or is reused by an
  object that is not nested within *o* [[intro.object]].

The lifetime of a reference begins when its initialization is complete.
The lifetime of a reference ends as if it were a scalar object requiring
storage.

[*Note 1*:  [[class.base.init]] describes the lifetime of base and
member subobjects. — *end note*]

The properties ascribed to objects and references throughout this
document apply for a given object or reference only during its lifetime.

[*Note 2*: In particular, before the lifetime of an object starts and
after its lifetime ends there are significant restrictions on the use of
the object, as described below, in  [[class.base.init]] and in 
[[class.cdtor]]. Also, the behavior of an object under construction and
destruction might not be the same as the behavior of an object whose
lifetime has started and not ended. [[class.base.init]] and 
[[class.cdtor]] describe the behavior of an object during its periods of
construction and destruction. — *end note*]

A program may end the lifetime of any object by reusing the storage
which the object occupies or by explicitly calling a destructor or
pseudo-destructor [[expr.prim.id.dtor]] for the object. For an object of
a class type, the program is not required to call the destructor
explicitly before the storage which the object occupies is reused or
released; however, if there is no explicit call to the destructor or if
a *delete-expression* [[expr.delete]] is not used to release the
storage, the destructor is not implicitly called and any program that
depends on the side effects produced by the destructor has undefined
behavior.

Before the lifetime of an object has started but after the storage which
the object will occupy has been allocated[^11] or, after the lifetime of
an object has ended and before the storage which the object occupied is
reused or released, any pointer that represents the address of the
storage location where the object will be or was located may be used but
only in limited ways. For an object under construction or destruction,
see  [[class.cdtor]]. Otherwise, such a pointer refers to allocated
storage [[basic.stc.dynamic.allocation]], and using the pointer as if
the pointer were of type `void*` is well-defined. Indirection through
such a pointer is permitted but the resulting lvalue may only be used in
limited ways, as described below. The program has undefined behavior if:

- the object will be or was of a class type with a non-trivial
  destructor and the pointer is used as the operand of a
  *delete-expression*,
- the pointer is used to access a non-static data member or call a
  non-static member function of the object, or
- the pointer is implicitly converted [[conv.ptr]] to a pointer to a
  virtual base class, or
- the pointer is used as the operand of a `static_cast`
  [[expr.static.cast]], except when the conversion is to pointer to
  cv `void`, or to pointer to cv `void` and subsequently to pointer to
  cv `char`, cv `unsigned char`, or cv `std::byte` [[cstddef.syn]], or
- the pointer is used as the operand of a `dynamic_cast`
  [[expr.dynamic.cast]].

[*Example 1*:

``` cpp
#include <cstdlib>

struct B {
  virtual void f();
  void mutate();
  virtual ~B();
};

struct D1 : B { void f(); };
struct D2 : B { void f(); };

void B::mutate() {
  new (this) D2;    // reuses storage --- ends the lifetime of *this
  f();              // undefined behavior
  ... = this;       // OK, this points to valid memory
}

void g() {
  void* p = std::malloc(sizeof(D1) + sizeof(D2));
  B* pb = new (p) D1;
  pb->mutate();
  *pb;              // OK: pb points to valid memory
  void* q = pb;     // OK: pb points to valid memory
  pb->f();          // undefined behavior: lifetime of *pb has ended
}
```

— *end example*]

Similarly, before the lifetime of an object has started but after the
storage which the object will occupy has been allocated or, after the
lifetime of an object has ended and before the storage which the object
occupied is reused or released, any glvalue that refers to the original
object may be used but only in limited ways. For an object under
construction or destruction, see  [[class.cdtor]]. Otherwise, such a
glvalue refers to allocated storage [[basic.stc.dynamic.allocation]],
and using the properties of the glvalue that do not depend on its value
is well-defined. The program has undefined behavior if:

- the glvalue is used to access the object, or
- the glvalue is used to call a non-static member function of the
  object, or
- the glvalue is bound to a reference to a virtual base class
  [[dcl.init.ref]], or
- the glvalue is used as the operand of a `dynamic_cast`
  [[expr.dynamic.cast]] or as the operand of `typeid`.

If, after the lifetime of an object has ended and before the storage
which the object occupied is reused or released, a new object is created
at the storage location which the original object occupied, a pointer
that pointed to the original object, a reference that referred to the
original object, or the name of the original object will automatically
refer to the new object and, once the lifetime of the new object has
started, can be used to manipulate the new object, if the original
object is transparently replaceable (see below) by the new object. An
object o₁ is *transparently replaceable* by an object o₂ if:

- the storage that o₂ occupies exactly overlays the storage that o₁
  occupied, and
- o₁ and o₂ are of the same type (ignoring the top-level cv-qualifiers),
  and
- o₁ is not a complete const object, and
- neither o₁ nor o₂ is a potentially-overlapping subobject
  [[intro.object]], and
- either o₁ and o₂ are both complete objects, or o₁ and o₂ are direct
  subobjects of objects p₁ and p₂, respectively, and p₁ is transparently
  replaceable by p₂.

[*Example 2*:

``` cpp
struct C {
  int i;
  void f();
  const C& operator=( const C& );
};

const C& C::operator=( const C& other) {
  if ( this != &other ) {
    this->~C();                 // lifetime of *this ends
    new (this) C(other);        // new object of type C created
    f();                        // well-defined
  }
  return *this;
}

C c1;
C c2;
c1 = c2;                        // well-defined
c1.f();                         // well-defined; c1 refers to a new object of type C
```

— *end example*]

[*Note 3*: If these conditions are not met, a pointer to the new object
can be obtained from a pointer that represents the address of its
storage by calling `std::launder` [[ptr.launder]]. — *end note*]

If a program ends the lifetime of an object of type `T` with static
[[basic.stc.static]], thread [[basic.stc.thread]], or automatic
[[basic.stc.auto]] storage duration and if `T` has a non-trivial
destructor,[^12] the program must ensure that an object of the original
type occupies that same storage location when the implicit destructor
call takes place; otherwise the behavior of the program is undefined.
This is true even if the block is exited with an exception.

[*Example 3*:

``` cpp
class T { };
struct B {
   ~B();
};

void h() {
   B b;
   new (&b) T;
}                               // undefined behavior at block exit
```

— *end example*]

Creating a new object within the storage that a const complete object
with static, thread, or automatic storage duration occupies, or within
the storage that such a const object used to occupy before its lifetime
ended, results in undefined behavior.

[*Example 4*:

``` cpp
struct B {
  B();
  ~B();
};

const B b;

void h() {
  b.~B();
  new (const_cast<B*>(&b)) const B;     // undefined behavior
}
```

— *end example*]

In this subclause, “before” and “after” refer to the “happens before”
relation [[intro.multithread]].

[*Note 4*: Therefore, undefined behavior results if an object that is
being constructed in one thread is referenced from another thread
without adequate synchronization. — *end note*]

### Indeterminate values <a id="basic.indet">[[basic.indet]]</a>

When storage for an object with automatic or dynamic storage duration is
obtained, the object has an *indeterminate value*, and if no
initialization is performed for the object, that object retains an
indeterminate value until that value is replaced [[expr.ass]].

[*Note 1*: Objects with static or thread storage duration are
zero-initialized, see  [[basic.start.static]]. — *end note*]

If an indeterminate value is produced by an evaluation, the behavior is
undefined except in the following cases:

- If an indeterminate value of unsigned ordinary character type
  [[basic.fundamental]] or `std::byte` type [[cstddef.syn]] is produced
  by the evaluation of:
  - the second or third operand of a conditional expression
    [[expr.cond]],
  - the right operand of a comma expression [[expr.comma]],
  - the operand of a cast or conversion ([[conv.integral]],
    [[expr.type.conv]], [[expr.static.cast]], [[expr.cast]]) to an
    unsigned ordinary character type or `std::byte` type
    [[cstddef.syn]], or
  - a discarded-value expression [[expr.context]],

  then the result of the operation is an indeterminate value.
- If an indeterminate value of unsigned ordinary character type or
  `std::byte` type is produced by the evaluation of the right operand of
  a simple assignment operator [[expr.ass]] whose first operand is an
  lvalue of unsigned ordinary character type or `std::byte` type, an
  indeterminate value replaces the value of the object referred to by
  the left operand.
- If an indeterminate value of unsigned ordinary character type is
  produced by the evaluation of the initialization expression when
  initializing an object of unsigned ordinary character type, that
  object is initialized to an indeterminate value.
- If an indeterminate value of unsigned ordinary character type or
  `std::byte` type is produced by the evaluation of the initialization
  expression when initializing an object of `std::byte` type, that
  object is initialized to an indeterminate value.

[*Example 1*:

``` cpp
int f(bool b) {
  unsigned char c;
  unsigned char d = c;          // OK, d has an indeterminate value
  int e = d;                    // undefined behavior
  return b ? d : 0;             // undefined behavior if b is true
}
```

— *end example*]

### Storage duration <a id="basic.stc">[[basic.stc]]</a>

The *storage duration* is the property of an object that defines the
minimum potential lifetime of the storage containing the object. The
storage duration is determined by the construct used to create the
object and is one of the following:

- static storage duration
- thread storage duration
- automatic storage duration
- dynamic storage duration

Static, thread, and automatic storage durations are associated with
objects introduced by declarations [[basic.def]] and implicitly created
by the implementation [[class.temporary]]. The dynamic storage duration
is associated with objects created by a *new-expression* [[expr.new]].

The storage duration categories apply to references as well.

When the end of the duration of a region of storage is reached, the
values of all pointers representing the address of any part of that
region of storage become invalid pointer values [[basic.compound]].
Indirection through an invalid pointer value and passing an invalid
pointer value to a deallocation function have undefined behavior. Any
other use of an invalid pointer value has *implementation-defined*
behavior.[^13]

#### Static storage duration <a id="basic.stc.static">[[basic.stc.static]]</a>

All variables which do not have dynamic storage duration, do not have
thread storage duration, and are not local have *static storage
duration*. The storage for these entities lasts for the duration of the
program ([[basic.start.static]], [[basic.start.term]]).

If a variable with static storage duration has initialization or a
destructor with side effects, it shall not be eliminated even if it
appears to be unused, except that a class object or its copy/move may be
eliminated as specified in  [[class.copy.elision]].

The keyword `static` can be used to declare a local variable with static
storage duration.

[*Note 1*:  [[stmt.dcl]] describes the initialization of local `static`
variables; [[basic.start.term]] describes the destruction of local
`static` variables. — *end note*]

The keyword `static` applied to a class data member in a class
definition gives the data member static storage duration.

#### Thread storage duration <a id="basic.stc.thread">[[basic.stc.thread]]</a>

All variables declared with the `thread_local` keyword have
*thread storage duration*. The storage for these entities lasts for the
duration of the thread in which they are created. There is a distinct
object or reference per thread, and use of the declared name refers to
the entity associated with the current thread.

[*Note 1*: A variable with thread storage duration is initialized as
specified in  [[basic.start.static]], [[basic.start.dynamic]], and
[[stmt.dcl]] and, if constructed, is destroyed on thread exit
[[basic.start.term]]. — *end note*]

#### Automatic storage duration <a id="basic.stc.auto">[[basic.stc.auto]]</a>

Block-scope variables not explicitly declared `static`, `thread_local`,
or `extern` have *automatic storage duration*. The storage for these
entities lasts until the block in which they are created exits.

[*Note 1*: These variables are initialized and destroyed as described
in  [[stmt.dcl]]. — *end note*]

If a variable with automatic storage duration has initialization or a
destructor with side effects, an implementation shall not destroy it
before the end of its block nor eliminate it as an optimization, even if
it appears to be unused, except that a class object or its copy/move may
be eliminated as specified in  [[class.copy.elision]].

#### Dynamic storage duration <a id="basic.stc.dynamic">[[basic.stc.dynamic]]</a>

Objects can be created dynamically during program execution
[[intro.execution]], using *new-expression*s [[expr.new]], and destroyed
using *delete-expression*s [[expr.delete]]. A C++ implementation
provides access to, and management of, dynamic storage via the global
*allocation functions* `operator new` and `operator
new[]` and the global *deallocation functions* `operator
delete` and `operator delete[]`.

[*Note 1*: The non-allocating forms described in
[[new.delete.placement]] do not perform allocation or
deallocation. — *end note*]

The library provides default definitions for the global allocation and
deallocation functions. Some global allocation and deallocation
functions are replaceable [[new.delete]]. A C++ program shall provide at
most one definition of a replaceable allocation or deallocation
function. Any such function definition replaces the default version
provided in the library [[replacement.functions]]. The following
allocation and deallocation functions [[support.dynamic]] are implicitly
declared in global scope in each translation unit of a program.

``` cpp
[[nodiscard]] void* operator new(std::size_t);
[[nodiscard]] void* operator new(std::size_t, std::align_val_t);

void operator delete(void*) noexcept;
void operator delete(void*, std::size_t) noexcept;
void operator delete(void*, std::align_val_t) noexcept;
void operator delete(void*, std::size_t, std::align_val_t) noexcept;

[[nodiscard]] void* operator new[](std::size_t);
[[nodiscard]] void* operator new[](std::size_t, std::align_val_t);

void operator delete[](void*) noexcept;
void operator delete[](void*, std::size_t) noexcept;
void operator delete[](void*, std::align_val_t) noexcept;
void operator delete[](void*, std::size_t, std::align_val_t) noexcept;
```

These implicit declarations introduce only the function names `operator`
`new`, `operator` `new[]`, `operator` `delete`, and `operator`
`delete[]`.

[*Note 2*: The implicit declarations do not introduce the names `std`,
`std::size_t`, `std::align_val_t`, or any other names that the library
uses to declare these names. Thus, a *new-expression*,
*delete-expression*, or function call that refers to one of these
functions without importing or including the header `<new>` is
well-formed. However, referring to `std` or `std::size_t` or
`std::align_val_t` is ill-formed unless the name has been declared by
importing or including the appropriate header. — *end note*]

Allocation and/or deallocation functions may also be declared and
defined for any class [[class.free]].

If the behavior of an allocation or deallocation function does not
satisfy the semantic constraints specified in 
[[basic.stc.dynamic.allocation]] and 
[[basic.stc.dynamic.deallocation]], the behavior is undefined.

##### Allocation functions <a id="basic.stc.dynamic.allocation">[[basic.stc.dynamic.allocation]]</a>

An allocation function shall be a class member function or a global
function; a program is ill-formed if an allocation function is declared
in a namespace scope other than global scope or declared static in
global scope. The return type shall be `void*`. The first parameter
shall have type `std::size_t` [[support.types]]. The first parameter
shall not have an associated default argument [[dcl.fct.default]]. The
value of the first parameter is interpreted as the requested size of the
allocation. An allocation function can be a function template. Such a
template shall declare its return type and first parameter as specified
above (that is, template parameter types shall not be used in the return
type and first parameter type). Template allocation functions shall have
two or more parameters.

An allocation function attempts to allocate the requested amount of
storage. If it is successful, it returns the address of the start of a
block of storage whose length in bytes is at least as large as the
requested size. The order, contiguity, and initial value of storage
allocated by successive calls to an allocation function are unspecified.
Even if the size of the space requested is zero, the request can fail.
If the request succeeds, the value returned by a replaceable allocation
function is a non-null pointer value [[basic.compound]] `p0` different
from any previously returned value `p1`, unless that value `p1` was
subsequently passed to a replaceable deallocation function. Furthermore,
for the library allocation functions in  [[new.delete.single]] and 
[[new.delete.array]], `p0` represents the address of a block of storage
disjoint from the storage for any other object accessible to the caller.
The effect of indirecting through a pointer returned from a request for
zero size is undefined.[^14]

For an allocation function other than a reserved placement allocation
function [[new.delete.placement]], the pointer returned on a successful
call shall represent the address of storage that is aligned as follows:

- If the allocation function takes an argument of type
  `std::align_val_t`, the storage will have the alignment specified by
  the value of this argument.
- Otherwise, if the allocation function is named `operator new[]`, the
  storage is aligned for any object that does not have new-extended
  alignment [[basic.align]] and is no larger than the requested size.
- Otherwise, the storage is aligned for any object that does not have
  new-extended alignment and is of the requested size.

An allocation function that fails to allocate storage can invoke the
currently installed new-handler function [[new.handler]], if any.

[*Note 3*:  A program-supplied allocation function can obtain the
address of the currently installed `new_handler` using the
`std::get_new_handler` function [[get.new.handler]]. — *end note*]

An allocation function that has a non-throwing exception specification
[[except.spec]] indicates failure by returning a null pointer value. Any
other allocation function never returns a null pointer value and
indicates failure only by throwing an exception [[except.throw]] of a
type that would match a handler [[except.handle]] of type
`std::bad_alloc` [[bad.alloc]].

A global allocation function is only called as the result of a new
expression [[expr.new]], or called directly using the function call
syntax [[expr.call]], or called indirectly to allocate storage for a
coroutine state [[dcl.fct.def.coroutine]], or called indirectly through
calls to the functions in the C++ standard library.

[*Note 4*: In particular, a global allocation function is not called to
allocate storage for objects with static storage duration
[[basic.stc.static]], for objects or references with thread storage
duration [[basic.stc.thread]], for objects of type `std::type_info`
[[expr.typeid]], or for an exception object
[[except.throw]]. — *end note*]

##### Deallocation functions <a id="basic.stc.dynamic.deallocation">[[basic.stc.dynamic.deallocation]]</a>

Deallocation functions shall be class member functions or global
functions; a program is ill-formed if deallocation functions are
declared in a namespace scope other than global scope or declared static
in global scope.

A deallocation function is a *destroying operator delete* if it has at
least two parameters and its second parameter is of type
`std::destroying_delete_t`. A destroying operator delete shall be a
class member function named `operator delete`.

[*Note 5*: Array deletion cannot use a destroying operator
delete. — *end note*]

Each deallocation function shall return `void`. If the function is a
destroying operator delete declared in class type `C`, the type of its
first parameter shall be `C*`; otherwise, the type of its first
parameter shall be `void*`. A deallocation function may have more than
one parameter. A *usual deallocation function* is a deallocation
function whose parameters after the first are

- optionally, a parameter of type `std::destroying_delete_t`, then
- optionally, a parameter of type `std::size_t` [^15], then
- optionally, a parameter of type `std::align_val_t`.

A destroying operator delete shall be a usual deallocation function. A
deallocation function may be an instance of a function template. Neither
the first parameter nor the return type shall depend on a template
parameter. A deallocation function template shall have two or more
function parameters. A template instance is never a usual deallocation
function, regardless of its signature.

If a deallocation function terminates by throwing an exception, the
behavior is undefined. The value of the first argument supplied to a
deallocation function may be a null pointer value; if so, and if the
deallocation function is one supplied in the standard library, the call
has no effect.

If the argument given to a deallocation function in the standard library
is a pointer that is not the null pointer value [[basic.compound]], the
deallocation function shall deallocate the storage referenced by the
pointer, ending the duration of the region of storage.

##### Safely-derived pointers <a id="basic.stc.dynamic.safety">[[basic.stc.dynamic.safety]]</a>

A *traceable pointer object* is

- an object of an object pointer type [[basic.compound]], or
- an object of an integral type that is at least as large as
  `std::intptr_t`, or
- a sequence of elements in an array of narrow character type
  [[basic.fundamental]], where the size and alignment of the sequence
  match those of some object pointer type.

A pointer value is a *safely-derived pointer* to an object with dynamic
storage duration only if the pointer value has an object pointer type
and is one of the following:

- the value returned by a call to the C++ standard library
  implementation of `::operator new(std::{}size_t)` or
  `::operator new(std::size_t, std::align_val_t)` ;[^16]
- the result of taking the address of an object (or one of its
  subobjects) designated by an lvalue resulting from indirection through
  a safely-derived pointer value;
- the result of well-defined pointer arithmetic [[expr.add]] using a
  safely-derived pointer value;
- the result of a well-defined pointer conversion ([[conv.ptr]],
  [[expr.type.conv]], [[expr.static.cast]], [[expr.cast]]) of a
  safely-derived pointer value;
- the result of a `reinterpret_cast` of a safely-derived pointer value;
- the result of a `reinterpret_cast` of an integer representation of a
  safely-derived pointer value;
- the value of an object whose value was copied from a traceable pointer
  object, where at the time of the copy the source object contained a
  copy of a safely-derived pointer value.

An integer value is an *integer representation of a safely-derived
pointer* only if its type is at least as large as `std::intptr_t` and it
is one of the following:

- the result of a `reinterpret_cast` of a safely-derived pointer value;
- the result of a valid conversion of an integer representation of a
  safely-derived pointer value;
- the value of an object whose value was copied from a traceable pointer
  object, where at the time of the copy the source object contained an
  integer representation of a safely-derived pointer value;
- the result of an additive or bitwise operation, one of whose operands
  is an integer representation of a safely-derived pointer value `P`, if
  that result converted by `reinterpret_cast<void*>` would compare equal
  to a safely-derived pointer computable from
  `reinterpret_cast<void*>(P)`.

An implementation may have *relaxed pointer safety*, in which case the
validity of a pointer value does not depend on whether it is a
safely-derived pointer value. Alternatively, an implementation may have
*strict pointer safety*, in which case a pointer value referring to an
object with dynamic storage duration that is not a safely-derived
pointer value is an invalid pointer value unless the referenced complete
object has previously been declared reachable [[util.dynamic.safety]].

[*Note 6*: The effect of using an invalid pointer value (including
passing it to a deallocation function) is undefined, see  [[basic.stc]].
This is true even if the unsafely-derived pointer value might compare
equal to some safely-derived pointer value. — *end note*]

It is *implementation-defined* whether an implementation has relaxed or
strict pointer safety.

#### Duration of subobjects <a id="basic.stc.inherit">[[basic.stc.inherit]]</a>

The storage duration of subobjects and reference members is that of
their complete object [[intro.object]].

### Alignment <a id="basic.align">[[basic.align]]</a>

Object types have *alignment requirements* ([[basic.fundamental]],
[[basic.compound]]) which place restrictions on the addresses at which
an object of that type may be allocated. An *alignment* is an
*implementation-defined* integer value representing the number of bytes
between successive addresses at which a given object can be allocated.
An object type imposes an alignment requirement on every object of that
type; stricter alignment can be requested using the alignment specifier
[[dcl.align]].

A *fundamental alignment* is represented by an alignment less than or
equal to the greatest alignment supported by the implementation in all
contexts, which is equal to `alignof(std::max_align_t)`
[[support.types]]. The alignment required for a type might be different
when it is used as the type of a complete object and when it is used as
the type of a subobject.

[*Example 1*:

``` cpp
struct B { long double d; };
struct D : virtual B { char c; };
```

When `D` is the type of a complete object, it will have a subobject of
type `B`, so it must be aligned appropriately for a `long double`. If
`D` appears as a subobject of another object that also has `B` as a
virtual base class, the `B` subobject might be part of a different
subobject, reducing the alignment requirements on the `D` subobject.

— *end example*]

The result of the `alignof` operator reflects the alignment requirement
of the type in the complete-object case.

An *extended alignment* is represented by an alignment greater than
`alignof(std::max_align_t)`. It is *implementation-defined* whether any
extended alignments are supported and the contexts in which they are
supported [[dcl.align]]. A type having an extended alignment requirement
is an *over-aligned type*.

[*Note 1*: Every over-aligned type is or contains a class type to which
extended alignment applies (possibly through a non-static data
member). — *end note*]

A *new-extended alignment* is represented by an alignment greater than
`__STDCPP_DEFAULT_NEW_ALIGNMENT__` [[cpp.predefined]].

Alignments are represented as values of the type `std::size_t`. Valid
alignments include only those values returned by an `alignof` expression
for the fundamental types plus an additional *implementation-defined*
set of values, which may be empty. Every alignment value shall be a
non-negative integral power of two.

Alignments have an order from *weaker* to *stronger* or *stricter*
alignments. Stricter alignments have larger alignment values. An address
that satisfies an alignment requirement also satisfies any weaker valid
alignment requirement.

The alignment requirement of a complete type can be queried using an
`alignof` expression [[expr.alignof]]. Furthermore, the narrow character
types [[basic.fundamental]] shall have the weakest alignment
requirement.

[*Note 2*: This enables the ordinary character types to be used as the
underlying type for an aligned memory area [[dcl.align]]. — *end note*]

Comparing alignments is meaningful and provides the obvious results:

- Two alignments are equal when their numeric values are equal.
- Two alignments are different when their numeric values are not equal.
- When an alignment is larger than another it represents a stricter
  alignment.

[*Note 3*: The runtime pointer alignment function [[ptr.align]] can be
used to obtain an aligned pointer within a buffer; the aligned-storage
templates in the library [[meta.trans.other]] can be used to obtain
aligned storage. — *end note*]

If a request for a specific extended alignment in a specific context is
not supported by an implementation, the program is ill-formed.

### Temporary objects <a id="class.temporary">[[class.temporary]]</a>

Temporary objects are created

- when a prvalue is converted to an xvalue [[conv.rval]],
- when needed by the implementation to pass or return an object of
  trivially-copyable type (see below), and
- when throwing an exception [[except.throw]]. \[*Note 1*: The lifetime
  of exception objects is described in  [[except.throw]]. — *end note*]

Even when the creation of the temporary object is unevaluated
[[expr.prop]], all the semantic restrictions shall be respected as if
the temporary object had been created and later destroyed.

[*Note 2*: This includes accessibility [[class.access]] and whether it
is deleted, for the constructor selected and for the destructor.
However, in the special case of the operand of a *decltype-specifier*
[[expr.call]], no temporary is introduced, so the foregoing does not
apply to such a prvalue. — *end note*]

The materialization of a temporary object is generally delayed as long
as possible in order to avoid creating unnecessary temporary objects.

[*Note 3*:

Temporary objects are materialized:

- when binding a reference to a prvalue ([[dcl.init.ref]],
  [[expr.type.conv]], [[expr.dynamic.cast]], [[expr.static.cast]],
  [[expr.const.cast]], [[expr.cast]]),
- when performing member access on a class prvalue ([[expr.ref]],
  [[expr.mptr.oper]]),
- when performing an array-to-pointer conversion or subscripting on an
  array prvalue ([[conv.array]], [[expr.sub]]),
- when initializing an object of type `std::initializer_list<T>` from a
  *braced-init-list* [[dcl.init.list]],
- for certain unevaluated operands ([[expr.typeid]], [[expr.sizeof]]),
  and
- when a prvalue that has type other than cv `void` appears as a
  discarded-value expression [[expr.prop]].

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
materialized so that the reference parameter of `X::operator=(const X&)`
can bind to it.

— *end example*]

When an object of class type `X` is passed to or returned from a
function, if `X` has at least one eligible copy or move constructor
[[special]], each such constructor is trivial, and the destructor of `X`
is either trivial or deleted, implementations are permitted to create a
temporary object to hold the function parameter or result object. The
temporary object is constructed from the function argument or return
value, respectively, and the function’s parameter or return object is
initialized as if by using the eligible trivial constructor to copy the
temporary (even if that constructor is inaccessible or would not be
selected by overload resolution to perform a copy or move of the
object).

[*Note 4*: This latitude is granted to allow objects of class type to
be passed to or returned from functions in registers. — *end note*]

When an implementation introduces a temporary object of a class that has
a non-trivial constructor ([[class.default.ctor]],
[[class.copy.ctor]]), it shall ensure that a constructor is called for
the temporary object. Similarly, the destructor shall be called for a
temporary with a non-trivial destructor [[class.dtor]]. Temporary
objects are destroyed as the last step in evaluating the full-expression
[[intro.execution]] that (lexically) contains the point where they were
created. This is true even if that evaluation ends in throwing an
exception. The value computations and side effects of destroying a
temporary object are associated only with the full-expression, not with
any specific subexpression.

There are three contexts in which temporaries are destroyed at a
different point than the end of the full-expression. The first context
is when a default constructor is called to initialize an element of an
array with no corresponding initializer [[dcl.init]]. The second context
is when a copy constructor is called to copy an element of an array
while the entire array is copied ([[expr.prim.lambda.capture]],
[[class.copy.ctor]]). In either case, if the constructor has one or more
default arguments, the destruction of every temporary created in a
default argument is sequenced before the construction of the next array
element, if any.

The third context is when a reference is bound to a temporary
object.[^17] The temporary object to which the reference is bound or the
temporary object that is the complete object of a subobject to which the
reference is bound persists for the lifetime of the reference if the
glvalue to which the reference is bound was obtained through one of the
following:

- a temporary materialization conversion [[conv.rval]],
- `(` *expression* `)`, where *expression* is one of these expressions,
- subscripting [[expr.sub]] of an array operand, where that operand is
  one of these expressions,
- a class member access [[expr.ref]] using the `.` operator where the
  left operand is one of these expressions and the right operand
  designates a non-static data member of non-reference type,
- a pointer-to-member operation [[expr.mptr.oper]] using the `.*`
  operator where the left operand is one of these expressions and the
  right operand is a pointer to data member of non-reference type,
- a
  - `const_cast` [[expr.const.cast]],
  - `static_cast` [[expr.static.cast]],
  - `dynamic_cast` [[expr.dynamic.cast]], or
  - `reinterpret_cast` [[expr.reinterpret.cast]]

  converting, without a user-defined conversion, a glvalue operand that
  is one of these expressions to a glvalue that refers to the object
  designated by the operand, or to its complete object or a subobject
  thereof,
- a conditional expression [[expr.cond]] that is a glvalue where the
  second or third operand is one of these expressions, or
- a comma expression [[expr.comma]] that is a glvalue where the right
  operand is one of these expressions.

[*Example 2*:

``` cpp
template<typename T> using id = T;

int i = 1;
int&& a = id<int[3]>{1, 2, 3}[i];           // temporary array has same lifetime as a
const int& b = static_cast<const int&>(0);  // temporary int has same lifetime as b
int&& c = cond ? id<int[3]>{1, 2, 3}[i] : static_cast<int&&>(0);
                                            // exactly one of the two temporaries is lifetime-extended
```

— *end example*]

[*Note 5*:

An explicit type conversion ([[expr.type.conv]], [[expr.cast]]) is
interpreted as a sequence of elementary casts, covered above.

[*Example 3*:

``` cpp
const int& x = (const int&)1;   // temporary for value 1 has same lifetime as x
```

— *end example*]

— *end note*]

[*Note 6*:

If a temporary object has a reference member initialized by another
temporary object, lifetime extension applies recursively to such a
member’s initializer.

[*Example 4*:

``` cpp
struct S {
  const int& m;
};
const S& s = S{1};              // both S and int temporaries have lifetime of s
```

— *end example*]

— *end note*]

The exceptions to this lifetime rule are:

- A temporary object bound to a reference parameter in a function call
  [[expr.call]] persists until the completion of the full-expression
  containing the call.
- A temporary object bound to a reference element of an aggregate of
  class type initialized from a parenthesized *expression-list*
  [[dcl.init]] persists until the completion of the full-expression
  containing the *expression-list*.
- The lifetime of a temporary bound to the returned value in a function
  `return` statement [[stmt.return]] is not extended; the temporary is
  destroyed at the end of the full-expression in the `return` statement.
- A temporary bound to a reference in a *new-initializer* [[expr.new]]
  persists until the completion of the full-expression containing the
  *new-initializer*.
  \[*Note 7*: This may introduce a dangling reference. — *end note*]
  \[*Example 5*:
  ``` cpp
  struct S { int mi; const std::pair<int,int>& mp; };
  S a { 1, {2,3} };
  S* p = new S{ 1, {2,3} };       // creates dangling reference
  ```

  — *end example*]

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

[*Example 6*:

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

The expression `S(16) + S(23)` creates three temporaries: a first
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

## Types <a id="basic.types">[[basic.types]]</a>

[*Note 1*:  [[basic.types]] and the subclauses thereof impose
requirements on implementations regarding the representation of types.
There are two kinds of types: fundamental types and compound types.
Types describe objects [[intro.object]], references [[dcl.ref]], or
functions [[dcl.fct]]. — *end note*]

For any object (other than a potentially-overlapping subobject) of
trivially copyable type `T`, whether or not the object holds a valid
value of type `T`, the underlying bytes [[intro.memory]] making up the
object can be copied into an array of `char`, `unsigned char`, or
`std::byte` [[cstddef.syn]]. [^18] If the content of that array is
copied back into the object, the object shall subsequently hold its
original value.

[*Example 1*:

``` cpp
constexpr std::size_t N = sizeof(T);
char buf[N];
T obj;                          // obj initialized to its original value
std::memcpy(buf, &obj, N);      // between these two calls to std::memcpy, obj might be modified
std::memcpy(&obj, buf, N);      // at this point, each subobject of obj of scalar type holds its original value
```

— *end example*]

For any trivially copyable type `T`, if two pointers to `T` point to
distinct `T` objects `obj1` and `obj2`, where neither `obj1` nor `obj2`
is a potentially-overlapping subobject, if the underlying bytes
[[intro.memory]] making up `obj1` are copied into `obj2`,[^19] `obj2`
shall subsequently hold the same value as `obj1`.

[*Example 2*:

``` cpp
T* t1p;
T* t2p;
    // provided that t2p points to an initialized object ...
std::memcpy(t1p, t2p, sizeof(T));
    // at this point, every subobject of trivially copyable type in *t1p contains
    // the same value as the corresponding subobject in *t2p
```

— *end example*]

The *object representation* of an object of type `T` is the sequence of
*N* `unsigned char` objects taken up by the object of type `T`, where
*N* equals `sizeof(T)`. The *value representation* of an object of type
`T` is the set of bits that participate in representing a value of type
`T`. Bits in the object representation that are not part of the value
representation are *padding bits*. For trivially copyable types, the
value representation is a set of bits in the object representation that
determines a *value*, which is one discrete element of an
*implementation-defined* set of values.[^20]

A class that has been declared but not defined, an enumeration type in
certain contexts [[dcl.enum]], or an array of unknown bound or of
incomplete element type, is an *incompletely-defined object type*. [^21]
Incompletely-defined object types and cv `void` are *incomplete types*
[[basic.fundamental]]. Objects shall not be defined to have an
incomplete type.

A class type (such as “`class X`”) might be incomplete at one point in a
translation unit and complete later on; the type “`class X`” is the same
type at both points. The declared type of an array object might be an
array of incomplete class type and therefore incomplete; if the class
type is completed later on in the translation unit, the array type
becomes complete; the array type at those two points is the same type.
The declared type of an array object might be an array of unknown bound
and therefore be incomplete at one point in a translation unit and
complete later on; the array types at those two points (“array of
unknown bound of `T`” and “array of `N` `T`”) are different types. The
type of a pointer to array of unknown bound, or of a type defined by a
`typedef` declaration to be an array of unknown bound, cannot be
completed.

[*Example 3*:

``` cpp
class X;                        // X is an incomplete type
extern X* xp;                   // xp is a pointer to an incomplete type
extern int arr[];               // the type of arr is incomplete
typedef int UNKA[];             // UNKA is an incomplete type
UNKA* arrp;                     // arrp is a pointer to an incomplete type
UNKA** arrpp;

void foo() {
  xp++;                         // error: X is incomplete
  arrp++;                       // error: incomplete type
  arrpp++;                      // OK: sizeof UNKA* is known
}

struct X { int i; };            // now X is a complete type
int  arr[10];                   // now the type of arr is complete

X x;
void bar() {
  xp = &x;                      // OK; type is ``pointer to X''
  arrp = &arr;                  // error: different types
  xp++;                         // OK:  X is complete
  arrp++;                       // error: UNKA can't be completed
}
```

— *end example*]

[*Note 2*: The rules for declarations and expressions describe in which
contexts incomplete types are prohibited. — *end note*]

An *object type* is a (possibly cv-qualified) type that is not a
function type, not a reference type, and not cv `void`.

Arithmetic types [[basic.fundamental]], enumeration types, pointer
types, pointer-to-member types [[basic.compound]], `std::nullptr_t`, and
cv-qualified [[basic.type.qualifier]] versions of these types are
collectively called *scalar types*. Scalar types, trivially copyable
class types [[class.prop]], arrays of such types, and cv-qualified
versions of these types are collectively called *trivially copyable
types*. Scalar types, trivial class types [[class.prop]], arrays of such
types and cv-qualified versions of these types are collectively called
*trivial types*. Scalar types, standard-layout class types
[[class.prop]], arrays of such types and cv-qualified versions of these
types are collectively called *standard-layout types*. Scalar types,
implicit-lifetime class types [[class.prop]], array types, and
cv-qualified versions of these types are collectively called
*implicit-lifetime types*.

A type is a *literal type* if it is:

- cv `void`; or
- a scalar type; or
- a reference type; or
- an array of literal type; or
- a possibly cv-qualified class type [[class]] that has all of the
  following properties:
  - it has a constexpr destructor [[dcl.constexpr]],
  - it is either a closure type [[expr.prim.lambda.closure]], an
    aggregate type [[dcl.init.aggr]], or has at least one constexpr
    constructor or constructor template (possibly inherited
    [[namespace.udecl]] from a base class) that is not a copy or move
    constructor,
  - if it is a union, at least one of its non-static data members is of
    non-volatile literal type, and
  - if it is not a union, all of its non-static data members and base
    classes are of non-volatile literal types.

[*Note 3*: A literal type is one for which it might be possible to
create an object within a constant expression. It is not a guarantee
that it is possible to create such an object, nor is it a guarantee that
any object of that type will be usable in a constant
expression. — *end note*]

Two types *cv1* `T1` and *cv2* `T2` are *layout-compatible* types if
`T1` and `T2` are the same type, layout-compatible enumerations
[[dcl.enum]], or layout-compatible standard-layout class types
[[class.mem]].

### Fundamental types <a id="basic.fundamental">[[basic.fundamental]]</a>

There are five *standard signed integer types* : “`signed char`”,
“`short int`”, “`int`”, “`long int`”, and “`long long int`”. In this
list, each type provides at least as much storage as those preceding it
in the list. There may also be *implementation-defined* *extended signed
integer types*. The standard and extended signed integer types are
collectively called *signed integer types*. The range of representable
values for a signed integer type is -2ᴺ⁻¹ to 2ᴺ⁻¹-1 (inclusive), where
*N* is called the *width* of the type.

[*Note 1*: Plain `int`s are intended to have the natural width
suggested by the architecture of the execution environment; the other
signed integer types are provided to meet special needs. — *end note*]

For each of the standard signed integer types, there exists a
corresponding (but different) *standard unsigned integer type*:
“`unsigned char`”, “`unsigned short int`”, “`unsigned int`”,
“`unsigned long int`”, and “`unsigned long long int`”. Likewise, for
each of the extended signed integer types, there exists a corresponding
*extended unsigned integer type*. The standard and extended unsigned
integer types are collectively called *unsigned integer types*. An
unsigned integer type has the same width *N* as the corresponding signed
integer type. The range of representable values for the unsigned type is
0 to 2ᴺ-1 (inclusive); arithmetic for the unsigned type is performed
modulo 2ᴺ.

[*Note 2*: Unsigned arithmetic does not overflow. Overflow for signed
arithmetic yields undefined behavior [[expr.pre]]. — *end note*]

An unsigned integer type has the same object representation, value
representation, and alignment requirements [[basic.align]] as the
corresponding signed integer type. For each value x of a signed integer
type, the value of the corresponding unsigned integer type congruent to
x modulo 2ᴺ has the same value of corresponding bits in its value
representation.[^22]

[*Example 1*: The value -1 of a signed integer type has the same
representation as the largest value of the corresponding unsigned
type. — *end example*]

**Table: Minimum width** <a id="basic.fundamental.width">[basic.fundamental.width]</a>

| Type          | Minimum width $N$ |
| ------------- | ----------------- |
| `signed char` | 8                 |
| `short`       | 16                |
| `int`         | 16                |
| `long`        | 32                |
| `long long`   | 64                |


The width of each signed integer type shall not be less than the values
specified in [[basic.fundamental.width]]. The value representation of a
signed or unsigned integer type comprises N bits, where N is the
respective width. Each set of values for any padding bits
[[basic.types]] in the object representation are alternative
representations of the value specified by the value representation.

[*Note 3*: Padding bits have unspecified value, but cannot cause traps.
In contrast, see ISO C 6.2.6.2. — *end note*]

[*Note 4*: The signed and unsigned integer types satisfy the
constraints given in ISO C 5.2.4.2.1. — *end note*]

Except as specified above, the width of a signed or unsigned integer
type is *implementation-defined*.

Each value x of an unsigned integer type with width N has a unique
representation $x = x_0 2^0 + x_1 2^1 + \ldots + x_{N-1} 2^{N-1}$, where
each coefficient xᵢ is either 0 or 1; this is called the *base-2
representation* of x. The base-2 representation of a value of signed
integer type is the base-2 representation of the congruent value of the
corresponding unsigned integer type. The standard signed integer types
and standard unsigned integer types are collectively called the
*standard integer types*, and the extended signed integer types and
extended unsigned integer types are collectively called the *extended
integer types*.

A fundamental type specified to have a signed or unsigned integer type
as its *underlying type* has the same object representation, value
representation, alignment requirements [[basic.align]], and range of
representable values as the underlying type. Further, each value has the
same representation in both types.

Type `char` is a distinct type that has an *implementation-defined*
choice of “`signed char`” or “`unsigned char`” as its underlying type.
The values of type `char` can represent distinct codes for all members
of the implementation’s basic character set. The three types `char`,
`signed char`, and `unsigned char` are collectively called *ordinary
character types*. The ordinary character types and `char8_t` are
collectively called *narrow character types*. For narrow character
types, each possible bit pattern of the object representation represents
a distinct value.

[*Note 5*: This requirement does not hold for other
types. — *end note*]

[*Note 6*: A bit-field of narrow character type whose width is larger
than the width of that type has padding bits; see
[[basic.types]]. — *end note*]

Type `wchar_t` is a distinct type that has an *implementation-defined*
signed or unsigned integer type as its underlying type. The values of
type `wchar_t` can represent distinct codes for all members of the
largest extended character set specified among the supported locales
[[locale]].

Type `char8_t` denotes a distinct type whose underlying type is
`unsigned char`. Types `char16_t` and `char32_t` denote distinct types
whose underlying types are `uint_least16_t` and `uint_least32_t`,
respectively, in `<cstdint>`.

Type `bool` is a distinct type that has the same object representation,
value representation, and alignment requirements as an
*implementation-defined* unsigned integer type. The values of type
`bool` are `true` and `false`.

[*Note 7*: There are no `signed`, `unsigned`, `short`, or `long bool`
types or values. — *end note*]

Types `bool`, `char`, `wchar_t`, `char8_t`, `char16_t`, `char32_t`, and
the signed and unsigned integer types are collectively called *integral
types*. A synonym for integral type is *integer type*.

[*Note 8*: Enumerations [[dcl.enum]] are not integral; however,
unscoped enumerations can be promoted to integral types as specified in
[[conv.prom]]. — *end note*]

There are three *floating-point types*: `float`, `double`, and
`long double`. The type `double` provides at least as much precision as
`float`, and the type `long double` provides at least as much precision
as `double`. The set of values of the type `float` is a subset of the
set of values of the type `double`; the set of values of the type
`double` is a subset of the set of values of the type `long double`. The
value representation of floating-point types is
*implementation-defined*.

[*Note 9*: This document imposes no requirements on the accuracy of
floating-point operations; see also  [[support.limits]]. — *end note*]

Integral and floating-point types are collectively called *arithmetic*
types. Specializations of the standard library template
`std::numeric_limits` [[support.limits]] shall specify the maximum and
minimum values of each arithmetic type for an implementation.

A type cv `void` is an incomplete type that cannot be completed; such a
type has an empty set of values. It is used as the return type for
functions that do not return a value. Any expression can be explicitly
converted to type cv `void` ([[expr.type.conv]], [[expr.static.cast]],
[[expr.cast]]). An expression of type cv `void` shall be used only as an
expression statement [[stmt.expr]], as an operand of a comma expression
[[expr.comma]], as a second or third operand of `?:` [[expr.cond]], as
the operand of `typeid`, `noexcept`, or `decltype`, as the expression in
a `return` statement [[stmt.return]] for a function with the return type
cv `void`, or as the operand of an explicit conversion to type
cv `void`.

A value of type `std::nullptr_t` is a null pointer constant
[[conv.ptr]]. Such values participate in the pointer and the
pointer-to-member conversions ([[conv.ptr]], [[conv.mem]]).
`sizeof(std::nullptr_t)` shall be equal to `sizeof(void*)`.

The types described in this subclause are called *fundamental types*.

[*Note 10*: Even if the implementation defines two or more fundamental
types to have the same value representation, they are nevertheless
different types. — *end note*]

### Compound types <a id="basic.compound">[[basic.compound]]</a>

Compound types can be constructed in the following ways:

- *arrays* of objects of a given type, [[dcl.array]];
- *functions*, which have parameters of given types and return `void` or
  references or objects of a given type, [[dcl.fct]];
- *pointers* to cv `void` or objects or functions (including static
  members of classes) of a given type, [[dcl.ptr]];
- *references* to objects or functions of a given type, [[dcl.ref]].
  There are two types of references:
  - lvalue reference
  - rvalue reference
- *classes* containing a sequence of objects of various types [[class]],
  a set of types, enumerations and functions for manipulating these
  objects [[class.mfct]], and a set of restrictions on the access to
  these entities [[class.access]];
- *unions*, which are classes capable of containing objects of different
  types at different times, [[class.union]];
- *enumerations*, which comprise a set of named constant values. Each
  distinct enumeration constitutes a different *enumerated type*,
  [[dcl.enum]];
- *pointers to non-static class members*, [^23] which identify members
  of a given type within objects of a given class, [[dcl.mptr]].
  Pointers to data members and pointers to member functions are
  collectively called *pointer-to-member* types.

These methods of constructing types can be applied recursively;
restrictions are mentioned in  [[dcl.meaning]]. Constructing a type such
that the number of bytes in its object representation exceeds the
maximum value representable in the type `std::size_t` [[support.types]]
is ill-formed.

The type of a pointer to cv `void` or a pointer to an object type is
called an *object pointer type*.

[*Note 1*: A pointer to `void` does not have a pointer-to-object type,
however, because `void` is not an object type. — *end note*]

The type of a pointer that can designate a function is called a
*function pointer type*. A pointer to an object of type `T` is referred
to as a “pointer to `T`”.

[*Example 1*: A pointer to an object of type `int` is referred to as
“pointer to `int`” and a pointer to an object of class `X` is called a
“pointer to `X`”. — *end example*]

Except for pointers to static members, text referring to “pointers” does
not apply to pointers to members. Pointers to incomplete types are
allowed although there are restrictions on what can be done with them
[[basic.align]]. Every value of pointer type is one of the following:

- a *pointer to* an object or function (the pointer is said to *point*
  to the object or function), or
- a *pointer past the end of* an object [[expr.add]], or
- the *null pointer value* for that type, or
- an *invalid pointer value*.

A value of a pointer type that is a pointer to or past the end of an
object *represents the address* of the first byte in memory
[[intro.memory]] occupied by the object [^24] or the first byte in
memory after the end of the storage occupied by the object,
respectively.

[*Note 2*: A pointer past the end of an object [[expr.add]] is not
considered to point to an unrelated object of the object’s type that
might be located at that address. A pointer value becomes invalid when
the storage it denotes reaches the end of its storage duration; see
[[basic.stc]]. — *end note*]

For purposes of pointer arithmetic [[expr.add]] and comparison (
[[expr.rel]], [[expr.eq]]), a pointer past the end of the last element
of an array `x` of n elements is considered to be equivalent to a
pointer to a hypothetical array element n of `x` and an object of type
`T` that is not an array element is considered to belong to an array
with one element of type `T`. The value representation of pointer types
is *implementation-defined*. Pointers to layout-compatible types shall
have the same value representation and alignment requirements
[[basic.align]].

[*Note 3*: Pointers to over-aligned types [[basic.align]] have no
special representation, but their range of valid values is restricted by
the extended alignment requirement. — *end note*]

Two objects *a* and *b* are *pointer-interconvertible* if:

- they are the same object, or
- one is a union object and the other is a non-static data member of
  that object [[class.union]], or
- one is a standard-layout class object and the other is the first
  non-static data member of that object, or, if the object has no
  non-static data members, any base class subobject of that object
  [[class.mem]], or
- there exists an object *c* such that *a* and *c* are
  pointer-interconvertible, and *c* and *b* are
  pointer-interconvertible.

If two objects are pointer-interconvertible, then they have the same
address, and it is possible to obtain a pointer to one from a pointer to
the other via a `reinterpret_cast` [[expr.reinterpret.cast]].

[*Note 4*: An array object and its first element are not
pointer-interconvertible, even though they have the same
address. — *end note*]

A pointer to cv `void` can be used to point to objects of unknown type.
Such a pointer shall be able to hold any object pointer. An object of
type cv `void*` shall have the same representation and alignment
requirements as cv `char*`.

### CV-qualifiers <a id="basic.type.qualifier">[[basic.type.qualifier]]</a>

A type mentioned in  [[basic.fundamental]] and  [[basic.compound]] is a
*cv-unqualified type*. Each type which is a cv-unqualified complete or
incomplete object type or is `void` [[basic.types]] has three
corresponding cv-qualified versions of its type: a *const-qualified*
version, a *volatile-qualified* version, and a
*const-volatile-qualified* version. The type of an object
[[intro.object]] includes the *cv-qualifier*s specified in the
*decl-specifier-seq* [[dcl.spec]], *declarator* [[dcl.decl]], *type-id*
[[dcl.name]], or *new-type-id* [[expr.new]] when the object is created.

- A *const object* is an object of type `const T` or a non-mutable
  subobject of a const object.
- A *volatile object* is an object of type `volatile T` or a subobject
  of a volatile object.
- A *const volatile object* is an object of type `const volatile T`, a
  non-mutable subobject of a const volatile object, a const subobject of
  a volatile object, or a non-mutable volatile subobject of a const
  object.

The cv-qualified or cv-unqualified versions of a type are distinct
types; however, they shall have the same representation and alignment
requirements [[basic.align]].[^25]

Except for array types, a compound type [[basic.compound]] is not
cv-qualified by the cv-qualifiers (if any) of the types from which it is
compounded.

An array type whose elements are cv-qualified is also considered to have
the same cv-qualifications as its elements.

[*Note 1*: Cv-qualifiers applied to an array type attach to the
underlying element type, so the notation “cv `T`”, where `T` is an array
type, refers to an array whose elements are so-qualified
[[dcl.array]]. — *end note*]

[*Example 1*:

``` cpp
typedef char CA[5];
typedef const char CC;
CC arr1[5] = { 0 };
const CA arr2 = { 0 };
```

The type of both `arr1` and `arr2` is “array of 5 `const char`”, and the
array type is considered to be const-qualified.

— *end example*]

[*Note 2*: See  [[dcl.fct]] and  [[class.this]] regarding function
types that have *cv-qualifier*s. — *end note*]

There is a partial ordering on cv-qualifiers, so that a type can be said
to be *more cv-qualified* than another. [[basic.type.qualifier.rel]]
shows the relations that constitute this ordering.

**Table: Relations on `const` and `volatile`** <a id="basic.type.qualifier.rel">[basic.type.qualifier.rel]</a>

|                 |     |                  |
| --------------- | --- | ---------------- |
| no cv-qualifier | <   | `const`          |
| no cv-qualifier | <   | `volatile`       |
| no cv-qualifier | <   | `const volatile` |
| `const`         | <   | `const volatile` |
| `volatile`      | <   | `const volatile` |


In this document, the notation cv (or *cv1*, *cv2*, etc.), used in the
description of types, represents an arbitrary set of cv-qualifiers,
i.e., one of {`const`}, {`volatile`}, {`const`, `volatile`}, or the
empty set. For a type cv `T`, the *top-level cv-qualifiers* of that type
are those denoted by cv.

[*Example 2*: The type corresponding to the *type-id* `const int&` has
no top-level cv-qualifiers. The type corresponding to the *type-id*
`volatile int * const` has the top-level cv-qualifier `const`. For a
class type `C`, the type corresponding to the *type-id*
`void (C::* volatile)(int) const` has the top-level cv-qualifier
`volatile`. — *end example*]

### Integer conversion rank <a id="conv.rank">[[conv.rank]]</a>

Every integer type has an *integer conversion rank* defined as follows:

- No two signed integer types other than `char` and `signed
  char` (if `char` is signed) shall have the same rank, even if they
  have the same representation.
- The rank of a signed integer type shall be greater than the rank of
  any signed integer type with a smaller width.
- The rank of `long long int` shall be greater than the rank of
  `long int`, which shall be greater than the rank of `int`, which shall
  be greater than the rank of `short int`, which shall be greater than
  the rank of `signed char`.
- The rank of any unsigned integer type shall equal the rank of the
  corresponding signed integer type.
- The rank of any standard integer type shall be greater than the rank
  of any extended integer type with the same width.
- The rank of `char` shall equal the rank of `signed char` and
  `unsigned char`.
- The rank of `bool` shall be less than the rank of all other standard
  integer types.
- The ranks of `char8_t`, `char16_t`, `char32_t`, and `wchar_t` shall
  equal the ranks of their underlying types [[basic.fundamental]].
- The rank of any extended signed integer type relative to another
  extended signed integer type with the same width is
  *implementation-defined*, but still subject to the other rules for
  determining the integer conversion rank.
- For all integer types `T1`, `T2`, and `T3`, if `T1` has greater rank
  than `T2` and `T2` has greater rank than `T3`, then `T1` shall have
  greater rank than `T3`.

[*Note 1*: The integer conversion rank is used in the definition of the
integral promotions [[conv.prom]] and the usual arithmetic conversions
[[expr.arith.conv]]. — *end note*]

## Program execution <a id="basic.exec">[[basic.exec]]</a>

### Sequential execution <a id="intro.execution">[[intro.execution]]</a>

An instance of each object with automatic storage duration
[[basic.stc.auto]] is associated with each entry into its block. Such an
object exists and retains its last-stored value during the execution of
the block and while the block is suspended (by a call of a function,
suspension of a coroutine [[expr.await]], or receipt of a signal).

A *constituent expression* is defined as follows:

- The constituent expression of an expression is that expression.
- The constituent expressions of a *braced-init-list* or of a (possibly
  parenthesized) *expression-list* are the constituent expressions of
  the elements of the respective list.
- The constituent expressions of a *brace-or-equal-initializer* of the
  form `=` *initializer-clause* are the constituent expressions of the
  *initializer-clause*.

[*Example 1*:

``` cpp
struct A { int x; };
struct B { int y; struct A a; };
B b = { 5, { 1+1 } };
```

The constituent expressions of the *initializer* used for the
initialization of `b` are `5` and `1+1`.

— *end example*]

The *immediate subexpressions* of an expression E are

- the constituent expressions of E’s operands [[expr.prop]],
- any function call that E implicitly invokes,
- if E is a *lambda-expression* [[expr.prim.lambda]], the initialization
  of the entities captured by copy and the constituent expressions of
  the *initializer* of the *init-capture*s,
- if E is a function call [[expr.call]] or implicitly invokes a
  function, the constituent expressions of each default argument
  [[dcl.fct.default]] used in the call, or
- if E creates an aggregate object [[dcl.init.aggr]], the constituent
  expressions of each default member initializer [[class.mem]] used in
  the initialization.

A *subexpression* of an expression E is an immediate subexpression of E
or a subexpression of an immediate subexpression of E.

[*Note 1*: Expressions appearing in the *compound-statement* of a
*lambda-expression* are not subexpressions of the
*lambda-expression*. — *end note*]

A *full-expression* is

- an unevaluated operand [[expr.prop]],
- a *constant-expression* [[expr.const]],
- an immediate invocation [[expr.const]],
- an *init-declarator* [[dcl.decl]] or a *mem-initializer*
  [[class.base.init]], including the constituent expressions of the
  initializer,
- an invocation of a destructor generated at the end of the lifetime of
  an object other than a temporary object [[class.temporary]] whose
  lifetime has not been extended, or
- an expression that is not a subexpression of another expression and
  that is not otherwise part of a full-expression.

If a language construct is defined to produce an implicit call of a
function, a use of the language construct is considered to be an
expression for the purposes of this definition. Conversions applied to
the result of an expression in order to satisfy the requirements of the
language construct in which the expression appears are also considered
to be part of the full-expression. For an initializer, performing the
initialization of the entity (including evaluating default member
initializers of an aggregate) is also considered part of the
full-expression.

[*Example 2*:

``` cpp
struct S {
  S(int i): I(i) { }            // full-expression is initialization of I
  int& v() { return I; }
  ~S() noexcept(false) { }
private:
  int I;
};

S s1(1);                        // full-expression comprises call of S::S(int)
void f() {
  S s2 = 2;                     // full-expression comprises call of S::S(int)
  if (S(3).v())                 // full-expression includes lvalue-to-rvalue and int to bool conversions,
                                // performed before temporary is deleted at end of full-expression
  { }
  bool b = noexcept(S());       // exception specification of destructor of S considered for noexcept

  // full-expression is destruction of s2 at end of block
}
struct B {
  B(S = S(0));
};
B b[2] = { B(), B() };          // full-expression is the entire initialization
                                // including the destruction of temporaries
```

— *end example*]

[*Note 2*: The evaluation of a full-expression can include the
evaluation of subexpressions that are not lexically part of the
full-expression. For example, subexpressions involved in evaluating
default arguments [[dcl.fct.default]] are considered to be created in
the expression that calls the function, not the expression that defines
the default argument. — *end note*]

Reading an object designated by a `volatile` glvalue [[basic.lval]],
modifying an object, calling a library I/O function, or calling a
function that does any of those operations are all *side effects*, which
are changes in the state of the execution environment. *Evaluation* of
an expression (or a subexpression) in general includes both value
computations (including determining the identity of an object for
glvalue evaluation and fetching a value previously assigned to an object
for prvalue evaluation) and initiation of side effects. When a call to a
library I/O function returns or an access through a volatile glvalue is
evaluated the side effect is considered complete, even though some
external actions implied by the call (such as the I/O itself) or by the
`volatile` access may not have completed yet.

*Sequenced before* is an asymmetric, transitive, pair-wise relation
between evaluations executed by a single thread [[intro.multithread]],
which induces a partial order among those evaluations. Given any two
evaluations *A* and *B*, if *A* is sequenced before *B* (or,
equivalently, *B* is *sequenced after* *A*), then the execution of *A*
shall precede the execution of *B*. If *A* is not sequenced before *B*
and *B* is not sequenced before *A*, then *A* and *B* are *unsequenced*.

[*Note 3*: The execution of unsequenced evaluations can
overlap. — *end note*]

Evaluations *A* and *B* are *indeterminately sequenced* when either *A*
is sequenced before *B* or *B* is sequenced before *A*, but it is
unspecified which.

[*Note 4*: Indeterminately sequenced evaluations cannot overlap, but
either could be executed first. — *end note*]

An expression *X* is said to be sequenced before an expression *Y* if
every value computation and every side effect associated with the
expression *X* is sequenced before every value computation and every
side effect associated with the expression *Y*.

Every value computation and side effect associated with a
full-expression is sequenced before every value computation and side
effect associated with the next full-expression to be evaluated.[^26]

Except where noted, evaluations of operands of individual operators and
of subexpressions of individual expressions are unsequenced.

[*Note 5*: In an expression that is evaluated more than once during the
execution of a program, unsequenced and indeterminately sequenced
evaluations of its subexpressions need not be performed consistently in
different evaluations. — *end note*]

The value computations of the operands of an operator are sequenced
before the value computation of the result of the operator. If a side
effect on a memory location [[intro.memory]] is unsequenced relative to
either another side effect on the same memory location or a value
computation using the value of any object in the same memory location,
and they are not potentially concurrent [[intro.multithread]], the
behavior is undefined.

[*Note 6*: The next subclause imposes similar, but more complex
restrictions on potentially concurrent computations. — *end note*]

[*Example 3*:

``` cpp
void g(int i) {
  i = 7, i++, i++;              // i becomes 9

  i = i++ + 1;                  // the value of i is incremented
  i = i++ + i;                  // undefined behavior
  i = i + 1;                    // the value of i is incremented
}
```

— *end example*]

When calling a function (whether or not the function is inline), every
value computation and side effect associated with any argument
expression, or with the postfix expression designating the called
function, is sequenced before execution of every expression or statement
in the body of the called function. For each function invocation *F*,
for every evaluation *A* that occurs within *F* and every evaluation *B*
that does not occur within *F* but is evaluated on the same thread and
as part of the same signal handler (if any), either *A* is sequenced
before *B* or *B* is sequenced before *A*.[^27]

[*Note 7*: If *A* and *B* would not otherwise be sequenced then they
are indeterminately sequenced. — *end note*]

Several contexts in C++ cause evaluation of a function call, even though
no corresponding function call syntax appears in the translation unit.

[*Example 4*: Evaluation of a *new-expression* invokes one or more
allocation and constructor functions; see  [[expr.new]]. For another
example, invocation of a conversion function [[class.conv.fct]] can
arise in contexts in which no function call syntax
appears. — *end example*]

The sequencing constraints on the execution of the called function (as
described above) are features of the function calls as evaluated,
whatever the syntax of the expression that calls the function might be.

If a signal handler is executed as a result of a call to the
`std::raise` function, then the execution of the handler is sequenced
after the invocation of the `std::raise` function and before its return.

[*Note 8*: When a signal is received for another reason, the execution
of the signal handler is usually unsequenced with respect to the rest of
the program. — *end note*]

### Multi-threaded executions and data races <a id="intro.multithread">[[intro.multithread]]</a>

A *thread of execution* (also known as a *thread*) is a single flow of
control within a program, including the initial invocation of a specific
top-level function, and recursively including every function invocation
subsequently executed by the thread.

[*Note 1*: When one thread creates another, the initial call to the
top-level function of the new thread is executed by the new thread, not
by the creating thread. — *end note*]

Every thread in a program can potentially access every object and
function in a program.[^28] Under a hosted implementation, a C++ program
can have more than one thread running concurrently. The execution of
each thread proceeds as defined by the remainder of this document. The
execution of the entire program consists of an execution of all of its
threads.

[*Note 2*: Usually the execution can be viewed as an interleaving of
all its threads. However, some kinds of atomic operations, for example,
allow executions inconsistent with a simple interleaving, as described
below. — *end note*]

Under a freestanding implementation, it is *implementation-defined*
whether a program can have more than one thread of execution.

For a signal handler that is not executed as a result of a call to the
`std::raise` function, it is unspecified which thread of execution
contains the signal handler invocation.

#### Data races <a id="intro.races">[[intro.races]]</a>

The value of an object visible to a thread T at a particular point is
the initial value of the object, a value assigned to the object by T, or
a value assigned to the object by another thread, according to the rules
below.

[*Note 1*: In some cases, there may instead be undefined behavior. Much
of this subclause is motivated by the desire to support atomic
operations with explicit and detailed visibility constraints. However,
it also implicitly supports a simpler view for more restricted
programs. — *end note*]

Two expression evaluations *conflict* if one of them modifies a memory
location [[intro.memory]] and the other one reads or modifies the same
memory location.

The library defines a number of atomic operations [[atomics]] and
operations on mutexes [[thread]] that are specially identified as
synchronization operations. These operations play a special role in
making assignments in one thread visible to another. A synchronization
operation on one or more memory locations is either a consume operation,
an acquire operation, a release operation, or both an acquire and
release operation. A synchronization operation without an associated
memory location is a fence and can be either an acquire fence, a release
fence, or both an acquire and release fence. In addition, there are
relaxed atomic operations, which are not synchronization operations, and
atomic read-modify-write operations, which have special characteristics.

[*Note 2*: For example, a call that acquires a mutex will perform an
acquire operation on the locations comprising the mutex.
Correspondingly, a call that releases the same mutex will perform a
release operation on those same locations. Informally, performing a
release operation on A forces prior side effects on other memory
locations to become visible to other threads that later perform a
consume or an acquire operation on A. “Relaxed” atomic operations are
not synchronization operations even though, like synchronization
operations, they cannot contribute to data races. — *end note*]

All modifications to a particular atomic object M occur in some
particular total order, called the *modification order* of M.

[*Note 3*: There is a separate order for each atomic object. There is
no requirement that these can be combined into a single total order for
all objects. In general this will be impossible since different threads
may observe modifications to different objects in inconsistent
orders. — *end note*]

A *release sequence* headed by a release operation A on an atomic object
M is a maximal contiguous sub-sequence of side effects in the
modification order of M, where the first operation is A, and every
subsequent operation is an atomic read-modify-write operation.

Certain library calls *synchronize with* other library calls performed
by another thread. For example, an atomic store-release synchronizes
with a load-acquire that takes its value from the store
[[atomics.order]].

[*Note 4*: Except in the specified cases, reading a later value does
not necessarily ensure visibility as described below. Such a requirement
would sometimes interfere with efficient implementation. — *end note*]

[*Note 5*: The specifications of the synchronization operations define
when one reads the value written by another. For atomic objects, the
definition is clear. All operations on a given mutex occur in a single
total order. Each mutex acquisition “reads the value written” by the
last mutex release. — *end note*]

An evaluation A *carries a dependency* to an evaluation B if

- the value of A is used as an operand of B, unless:
  - B is an invocation of any specialization of `std::kill_dependency`
    [[atomics.order]], or
  - A is the left operand of a built-in logical (`&&`, see 
    [[expr.log.and]]) or logical (`||`, see  [[expr.log.or]]) operator,
    or
  - A is the left operand of a conditional (`?:`, see  [[expr.cond]])
    operator, or
  - A is the left operand of the built-in comma (`,`) operator
    [[expr.comma]];

  or
- A writes a scalar object or bit-field M, B reads the value written by
  A from M, and A is sequenced before B, or
- for some evaluation X, A carries a dependency to X, and X carries a
  dependency to B.

[*Note 6*: “Carries a dependency to” is a subset of “is sequenced
before”, and is similarly strictly intra-thread. — *end note*]

An evaluation A is *dependency-ordered before* an evaluation B if

- A performs a release operation on an atomic object M, and, in another
  thread, B performs a consume operation on M and reads the value
  written by A, or
- for some evaluation X, A is dependency-ordered before X and X carries
  a dependency to B.

[*Note 7*: The relation “is dependency-ordered before” is analogous to
“synchronizes with”, but uses release/consume in place of
release/acquire. — *end note*]

An evaluation A *inter-thread happens before* an evaluation B if

- A synchronizes with B, or
- A is dependency-ordered before B, or
- for some evaluation X
  - A synchronizes with X and X is sequenced before B, or
  - A is sequenced before X and X inter-thread happens before B, or
  - A inter-thread happens before X and X inter-thread happens before B.

[*Note 8*: The “inter-thread happens before” relation describes
arbitrary concatenations of “sequenced before”, “synchronizes with” and
“dependency-ordered before” relationships, with two exceptions. The
first exception is that a concatenation is not permitted to end with
“dependency-ordered before” followed by “sequenced before”. The reason
for this limitation is that a consume operation participating in a
“dependency-ordered before” relationship provides ordering only with
respect to operations to which this consume operation actually carries a
dependency. The reason that this limitation applies only to the end of
such a concatenation is that any subsequent release operation will
provide the required ordering for a prior consume operation. The second
exception is that a concatenation is not permitted to consist entirely
of “sequenced before”. The reasons for this limitation are (1) to permit
“inter-thread happens before” to be transitively closed and (2) the
“happens before” relation, defined below, provides for relationships
consisting entirely of “sequenced before”. — *end note*]

An evaluation A *happens before* an evaluation B (or, equivalently, B
*happens after* A) if:

- A is sequenced before B, or
- A inter-thread happens before B.

The implementation shall ensure that no program execution demonstrates a
cycle in the “happens before” relation.

[*Note 9*: This cycle would otherwise be possible only through the use
of consume operations. — *end note*]

An evaluation A *simply happens before* an evaluation B if either

- A is sequenced before B, or
- A synchronizes with B, or
- A simply happens before X and X simply happens before B.

[*Note 10*: In the absence of consume operations, the happens before
and simply happens before relations are identical. — *end note*]

An evaluation A *strongly happens before* an evaluation D if, either

- A is sequenced before D, or
- A synchronizes with D, and both A and D are sequentially consistent
  atomic operations [[atomics.order]], or
- there are evaluations B and C such that A is sequenced before B, B
  simply happens before C, and C is sequenced before D, or
- there is an evaluation B such that A strongly happens before B, and B
  strongly happens before D.

[*Note 11*: Informally, if A strongly happens before B, then A appears
to be evaluated before B in all contexts. Strongly happens before
excludes consume operations. — *end note*]

A *visible side effect* A on a scalar object or bit-field M with respect
to a value computation B of M satisfies the conditions:

- A happens before B and
- there is no other side effect X to M such that A happens before X and
  X happens before B.

The value of a non-atomic scalar object or bit-field M, as determined by
evaluation B, shall be the value stored by the visible side effect A.

[*Note 12*: If there is ambiguity about which side effect to a
non-atomic object or bit-field is visible, then the behavior is either
unspecified or undefined. — *end note*]

[*Note 13*: This states that operations on ordinary objects are not
visibly reordered. This is not actually detectable without data races,
but it is necessary to ensure that data races, as defined below, and
with suitable restrictions on the use of atomics, correspond to data
races in a simple interleaved (sequentially consistent)
execution. — *end note*]

The value of an atomic object M, as determined by evaluation B, shall be
the value stored by some side effect A that modifies M, where B does not
happen before A.

[*Note 14*: The set of such side effects is also restricted by the rest
of the rules described here, and in particular, by the coherence
requirements below. — *end note*]

If an operation A that modifies an atomic object M happens before an
operation B that modifies M, then A shall be earlier than B in the
modification order of M.

[*Note 15*: This requirement is known as write-write
coherence. — *end note*]

If a value computation A of an atomic object M happens before a value
computation B of M, and A takes its value from a side effect X on M,
then the value computed by B shall either be the value stored by X or
the value stored by a side effect Y on M, where Y follows X in the
modification order of M.

[*Note 16*: This requirement is known as read-read
coherence. — *end note*]

If a value computation A of an atomic object M happens before an
operation B that modifies M, then A shall take its value from a side
effect X on M, where X precedes B in the modification order of M.

[*Note 17*: This requirement is known as read-write
coherence. — *end note*]

If a side effect X on an atomic object M happens before a value
computation B of M, then the evaluation B shall take its value from X or
from a side effect Y that follows X in the modification order of M.

[*Note 18*: This requirement is known as write-read
coherence. — *end note*]

[*Note 19*: The four preceding coherence requirements effectively
disallow compiler reordering of atomic operations to a single object,
even if both operations are relaxed loads. This effectively makes the
cache coherence guarantee provided by most hardware available to C++
atomic operations. — *end note*]

[*Note 20*: The value observed by a load of an atomic depends on the
“happens before” relation, which depends on the values observed by loads
of atomics. The intended reading is that there must exist an association
of atomic loads with modifications they observe that, together with
suitably chosen modification orders and the “happens before” relation
derived as described above, satisfy the resulting constraints as imposed
here. — *end note*]

Two actions are *potentially concurrent* if

- they are performed by different threads, or
- they are unsequenced, at least one is performed by a signal handler,
  and they are not both performed by the same signal handler invocation.

The execution of a program contains a *data race* if it contains two
potentially concurrent conflicting actions, at least one of which is not
atomic, and neither happens before the other, except for the special
case for signal handlers described below. Any such data race results in
undefined behavior.

[*Note 21*: It can be shown that programs that correctly use mutexes
and `memory_order::seq_cst` operations to prevent all data races and use
no other synchronization operations behave as if the operations executed
by their constituent threads were simply interleaved, with each value
computation of an object being taken from the last side effect on that
object in that interleaving. This is normally referred to as “sequential
consistency”. However, this applies only to data-race-free programs, and
data-race-free programs cannot observe most program transformations that
do not change single-threaded program semantics. In fact, most
single-threaded program transformations continue to be allowed, since
any program that behaves differently as a result must perform an
undefined operation. — *end note*]

Two accesses to the same object of type `volatile std::sig_atomic_t` do
not result in a data race if both occur in the same thread, even if one
or more occurs in a signal handler. For each signal handler invocation,
evaluations performed by the thread invoking a signal handler can be
divided into two groups A and B, such that no evaluations in B happen
before evaluations in A, and the evaluations of such
`volatile std::sig_atomic_t` objects take values as though all
evaluations in A happened before the execution of the signal handler and
the execution of the signal handler happened before all evaluations in
B.

[*Note 22*: Compiler transformations that introduce assignments to a
potentially shared memory location that would not be modified by the
abstract machine are generally precluded by this document, since such an
assignment might overwrite another assignment by a different thread in
cases in which an abstract machine execution would not have encountered
a data race. This includes implementations of data member assignment
that overwrite adjacent members in separate memory locations. Reordering
of atomic loads in cases in which the atomics in question may alias is
also generally precluded, since this may violate the coherence
rules. — *end note*]

[*Note 23*: Transformations that introduce a speculative read of a
potentially shared memory location may not preserve the semantics of the
C++ program as defined in this document, since they potentially
introduce a data race. However, they are typically valid in the context
of an optimizing compiler that targets a specific machine with
well-defined semantics for data races. They would be invalid for a
hypothetical machine that is not tolerant of races or provides hardware
race detection. — *end note*]

#### Forward progress <a id="intro.progress">[[intro.progress]]</a>

The implementation may assume that any thread will eventually do one of
the following:

- terminate,
- make a call to a library I/O function,
- perform an access through a volatile glvalue, or
- perform a synchronization operation or an atomic operation.

[*Note 1*: This is intended to allow compiler transformations such as
removal of empty loops, even when termination cannot be
proven. — *end note*]

Executions of atomic functions that are either defined to be lock-free
[[atomics.flag]] or indicated as lock-free [[atomics.lockfree]] are
*lock-free executions*.

- If there is only one thread that is not blocked [[defns.block]] in a
  standard library function, a lock-free execution in that thread shall
  complete. \[*Note 2*: Concurrently executing threads may prevent
  progress of a lock-free execution. For example, this situation can
  occur with load-locked store-conditional implementations. This
  property is sometimes termed obstruction-free. — *end note*]
- When one or more lock-free executions run concurrently, at least one
  should complete. \[*Note 3*: It is difficult for some implementations
  to provide absolute guarantees to this effect, since repeated and
  particularly inopportune interference from other threads may prevent
  forward progress, e.g., by repeatedly stealing a cache line for
  unrelated purposes between load-locked and store-conditional
  instructions. Implementations should ensure that such effects cannot
  indefinitely delay progress under expected operating conditions, and
  that such anomalies can therefore safely be ignored by programmers.
  Outside this document, this property is sometimes termed
  lock-free. — *end note*]

During the execution of a thread of execution, each of the following is
termed an *execution step*:

- termination of the thread of execution,
- performing an access through a volatile glvalue, or
- completion of a call to a library I/O function, a synchronization
  operation, or an atomic operation.

An invocation of a standard library function that blocks [[defns.block]]
is considered to continuously execute execution steps while waiting for
the condition that it blocks on to be satisfied.

[*Example 1*: A library I/O function that blocks until the I/O
operation is complete can be considered to continuously check whether
the operation is complete. Each such check might consist of one or more
execution steps, for example using observable behavior of the abstract
machine. — *end example*]

[*Note 4*: Because of this and the preceding requirement regarding what
threads of execution have to perform eventually, it follows that no
thread of execution can execute forever without an execution step
occurring. — *end note*]

A thread of execution *makes progress* when an execution step occurs or
a lock-free execution does not complete because there are other
concurrent threads that are not blocked in a standard library function
(see above).

For a thread of execution providing *concurrent forward progress
guarantees*, the implementation ensures that the thread will eventually
make progress for as long as it has not terminated.

[*Note 5*: This is required regardless of whether or not other threads
of executions (if any) have been or are making progress. To eventually
fulfill this requirement means that this will happen in an unspecified
but finite amount of time. — *end note*]

It is *implementation-defined* whether the implementation-created thread
of execution that executes `main` [[basic.start.main]] and the threads
of execution created by `std::thread` [[thread.thread.class]] or
`std::jthread` [[thread.jthread.class]] provide concurrent forward
progress guarantees.

[*Note 6*: General-purpose implementations should provide these
guarantees. — *end note*]

For a thread of execution providing *parallel forward progress
guarantees*, the implementation is not required to ensure that the
thread will eventually make progress if it has not yet executed any
execution step; once this thread has executed a step, it provides
concurrent forward progress guarantees.

[*Note 7*: This does not specify a requirement for when to start this
thread of execution, which will typically be specified by the entity
that creates this thread of execution. For example, a thread of
execution that provides concurrent forward progress guarantees and
executes tasks from a set of tasks in an arbitrary order, one after the
other, satisfies the requirements of parallel forward progress for these
tasks. — *end note*]

For a thread of execution providing *weakly parallel forward progress
guarantees*, the implementation does not ensure that the thread will
eventually make progress.

[*Note 8*: Threads of execution providing weakly parallel forward
progress guarantees cannot be expected to make progress regardless of
whether other threads make progress or not; however, blocking with
forward progress guarantee delegation, as defined below, can be used to
ensure that such threads of execution make progress
eventually. — *end note*]

Concurrent forward progress guarantees are stronger than parallel
forward progress guarantees, which in turn are stronger than weakly
parallel forward progress guarantees.

[*Note 9*: For example, some kinds of synchronization between threads
of execution may only make progress if the respective threads of
execution provide parallel forward progress guarantees, but will fail to
make progress under weakly parallel guarantees. — *end note*]

When a thread of execution P is specified to *block with forward
progress guarantee delegation* on the completion of a set S of threads
of execution, then throughout the whole time of P being blocked on S,
the implementation shall ensure that the forward progress guarantees
provided by at least one thread of execution in S is at least as strong
as P’s forward progress guarantees.

[*Note 10*: It is unspecified which thread or threads of execution in S
are chosen and for which number of execution steps. The strengthening is
not permanent and not necessarily in place for the rest of the lifetime
of the affected thread of execution. As long as P is blocked, the
implementation has to eventually select and potentially strengthen a
thread of execution in S. — *end note*]

Once a thread of execution in S terminates, it is removed from S. Once S
is empty, P is unblocked.

[*Note 11*: A thread of execution B thus can temporarily provide an
effectively stronger forward progress guarantee for a certain amount of
time, due to a second thread of execution A being blocked on it with
forward progress guarantee delegation. In turn, if B then blocks with
forward progress guarantee delegation on C, this may also temporarily
provide a stronger forward progress guarantee to C. — *end note*]

[*Note 12*: If all threads of execution in S finish executing (e.g.,
they terminate and do not use blocking synchronization incorrectly),
then P’s execution of the operation that blocks with forward progress
guarantee delegation will not result in P’s progress guarantee being
effectively weakened. — *end note*]

[*Note 13*: This does not remove any constraints regarding blocking
synchronization for threads of execution providing parallel or weakly
parallel forward progress guarantees because the implementation is not
required to strengthen a particular thread of execution whose too-weak
progress guarantee is preventing overall progress. — *end note*]

An implementation should ensure that the last value (in modification
order) assigned by an atomic or synchronization operation will become
visible to all other threads in a finite period of time.

### Start and termination <a id="basic.start">[[basic.start]]</a>

#### `main` function <a id="basic.start.main">[[basic.start.main]]</a>

A program shall contain a global function called `main` attached to the
global module. Executing a program starts a main thread of execution (
[[intro.multithread]], [[thread.threads]]) in which the `main` function
is invoked, and in which variables of static storage duration might be
initialized [[basic.start.static]] and destroyed [[basic.start.term]].
It is *implementation-defined* whether a program in a freestanding
environment is required to define a `main` function.

[*Note 1*: In a freestanding environment, startup and termination is
*implementation-defined*; startup contains the execution of constructors
for objects of namespace scope with static storage duration; termination
contains the execution of destructors for objects with static storage
duration. — *end note*]

An implementation shall not predefine the `main` function. This function
shall not be overloaded. Its type shall have C++ language linkage and it
shall have a declared return type of type `int`, but otherwise its type
is *implementation-defined*. An implementation shall allow both

- a function of `()` returning `int` and
- a function of `(int`, pointer to pointer to `char)` returning `int`

as the type of `main` [[dcl.fct]]. In the latter form, for purposes of
exposition, the first function parameter is called `argc` and the second
function parameter is called `argv`, where `argc` shall be the number of
arguments passed to the program from the environment in which the
program is run. If `argc` is nonzero these arguments shall be supplied
in `argv[0]` through `argv[argc-1]` as pointers to the initial
characters of null-terminated multibyte strings (NTMBSs)
[[multibyte.strings]] and `argv[0]` shall be the pointer to the initial
character of a NTMBS that represents the name used to invoke the program
or `""`. The value of `argc` shall be non-negative. The value of
`argv[argc]` shall be 0.

[*Note 2*: It is recommended that any further (optional) parameters be
added after `argv`. — *end note*]

The function `main` shall not be used within a program. The linkage
[[basic.link]] of `main` is *implementation-defined*. A program that
defines `main` as deleted or that declares `main` to be `inline`,
`static`, or `constexpr` is ill-formed. The function `main` shall not be
a coroutine [[dcl.fct.def.coroutine]]. The `main` function shall not be
declared with a *linkage-specification* [[dcl.link]]. A program that
declares a variable `main` at global scope, or that declares a function
`main` at global scope attached to a named module, or that declares the
name `main` with C language linkage (in any namespace) is ill-formed.
The name `main` is not otherwise reserved.

[*Example 1*: Member functions, classes, and enumerations can be called
`main`, as can entities in other namespaces. — *end example*]

Terminating the program without leaving the current block (e.g., by
calling the function `std::exit(int)` [[support.start.term]]) does not
destroy any objects with automatic storage duration [[class.dtor]]. If
`std::exit` is called to end a program during the destruction of an
object with static or thread storage duration, the program has undefined
behavior.

A `return` statement [[stmt.return]] in `main` has the effect of leaving
the main function (destroying any objects with automatic storage
duration) and calling `std::exit` with the return value as the argument.
If control flows off the end of the *compound-statement* of `main`, the
effect is equivalent to a `return` with operand `0` (see also
[[except.handle]]).

#### Static initialization <a id="basic.start.static">[[basic.start.static]]</a>

Variables with static storage duration are initialized as a consequence
of program initiation. Variables with thread storage duration are
initialized as a consequence of thread execution. Within each of these
phases of initiation, initialization occurs as follows.

*Constant initialization* is performed if a variable or temporary object
with static or thread storage duration is constant-initialized
[[expr.const]]. If constant initialization is not performed, a variable
with static storage duration [[basic.stc.static]] or thread storage
duration [[basic.stc.thread]] is zero-initialized [[dcl.init]].
Together, zero-initialization and constant initialization are called
*static initialization*; all other initialization is *dynamic
initialization*. All static initialization strongly happens before
[[intro.races]] any dynamic initialization.

[*Note 1*: The dynamic initialization of non-local variables is
described in  [[basic.start.dynamic]]; that of local static variables is
described in  [[stmt.dcl]]. — *end note*]

An implementation is permitted to perform the initialization of a
variable with static or thread storage duration as a static
initialization even if such initialization is not required to be done
statically, provided that

- the dynamic version of the initialization does not change the value of
  any other object of static or thread storage duration prior to its
  initialization, and
- the static version of the initialization produces the same value in
  the initialized variable as would be produced by the dynamic
  initialization if all variables not required to be initialized
  statically were initialized dynamically.

[*Note 2*:

As a consequence, if the initialization of an object `obj1` refers to an
object `obj2` of namespace scope potentially requiring dynamic
initialization and defined later in the same translation unit, it is
unspecified whether the value of `obj2` used will be the value of the
fully initialized `obj2` (because `obj2` was statically initialized) or
will be the value of `obj2` merely zero-initialized. For example,

``` cpp
inline double fd() { return 1.0; }
extern double d1;
double d2 = d1;     // unspecified:
                    // may be statically initialized to 0.0 or
                    // dynamically initialized to 0.0 if d1 is
                    // dynamically initialized, or 1.0 otherwise
double d1 = fd();   // may be initialized statically or dynamically to 1.0
```

— *end note*]

#### Dynamic initialization of non-local variables <a id="basic.start.dynamic">[[basic.start.dynamic]]</a>

Dynamic initialization of a non-local variable with static storage
duration is unordered if the variable is an implicitly or explicitly
instantiated specialization, is partially-ordered if the variable is an
inline variable that is not an implicitly or explicitly instantiated
specialization, and otherwise is ordered.

[*Note 1*: An explicitly specialized non-inline static data member or
variable template specialization has ordered
initialization. — *end note*]

A declaration `D` is *appearance-ordered* before a declaration `E` if

- `D` appears in the same translation unit as `E`, or
- the translation unit containing `E` has an interface dependency on the
  translation unit containing `D`,

in either case prior to `E`.

Dynamic initialization of non-local variables `V` and `W` with static
storage duration are ordered as follows:

- If `V` and `W` have ordered initialization and the definition of `V`
  is appearance-ordered before the definition of `W`, or if `V` has
  partially-ordered initialization, `W` does not have unordered
  initialization, and for every definition `E` of `W` there exists a
  definition `D` of `V` such that `D` is appearance-ordered before `E`,
  then
  - if the program does not start a thread [[intro.multithread]] other
    than the main thread [[basic.start.main]] or `V` and `W` have
    ordered initialization and they are defined in the same translation
    unit, the initialization of `V` is sequenced before the
    initialization of `W`;
  - otherwise, the initialization of `V` strongly happens before the
    initialization of `W`.
- Otherwise, if the program starts a thread other than the main thread
  before either `V` or `W` is initialized, it is unspecified in which
  threads the initializations of `V` and `W` occur; the initializations
  are unsequenced if they occur in the same thread.
- Otherwise, the initializations of `V` and `W` are indeterminately
  sequenced.

[*Note 2*: This definition permits initialization of a sequence of
ordered variables concurrently with another sequence. — *end note*]

A *non-initialization odr-use* is an odr-use [[basic.def.odr]] not
caused directly or indirectly by the initialization of a non-local
static or thread storage duration variable.

It is *implementation-defined* whether the dynamic initialization of a
non-local non-inline variable with static storage duration is sequenced
before the first statement of `main` or is deferred. If it is deferred,
it strongly happens before any non-initialization odr-use of any
non-inline function or non-inline variable defined in the same
translation unit as the variable to be initialized. [^29] It is
*implementation-defined* in which threads and at which points in the
program such deferred dynamic initialization occurs.

[*Note 3*: Such points should be chosen in a way that allows the
programmer to avoid deadlocks. — *end note*]

[*Example 1*:

``` cpp
// - File 1 -
#include "a.h"
#include "b.h"
B b;
A::A(){
  b.Use();
}

// - File 2 -
#include "a.h"
A a;

// - File 3 -
#include "a.h"
#include "b.h"
extern A a;
extern B b;

int main() {
  a.Use();
  b.Use();
}
```

It is *implementation-defined* whether either `a` or `b` is initialized
before `main` is entered or whether the initializations are delayed
until `a` is first odr-used in `main`. In particular, if `a` is
initialized before `main` is entered, it is not guaranteed that `b` will
be initialized before it is odr-used by the initialization of `a`, that
is, before `A::A` is called. If, however, `a` is initialized at some
point after the first statement of `main`, `b` will be initialized prior
to its use in `A::A`.

— *end example*]

It is *implementation-defined* whether the dynamic initialization of a
non-local inline variable with static storage duration is sequenced
before the first statement of `main` or is deferred. If it is deferred,
it strongly happens before any non-initialization odr-use of that
variable. It is *implementation-defined* in which threads and at which
points in the program such deferred dynamic initialization occurs.

It is *implementation-defined* whether the dynamic initialization of a
non-local non-inline variable with thread storage duration is sequenced
before the first statement of the initial function of a thread or is
deferred. If it is deferred, the initialization associated with the
entity for thread *t* is sequenced before the first non-initialization
odr-use by *t* of any non-inline variable with thread storage duration
defined in the same translation unit as the variable to be initialized.
It is *implementation-defined* in which threads and at which points in
the program such deferred dynamic initialization occurs.

If the initialization of a non-local variable with static or thread
storage duration exits via an exception, the function `std::terminate`
is called [[except.terminate]].

#### Termination <a id="basic.start.term">[[basic.start.term]]</a>

Constructed objects [[dcl.init]] with static storage duration are
destroyed and functions registered with `std::atexit` are called as part
of a call to `std::exit` [[support.start.term]]. The call to `std::exit`
is sequenced before the destructions and the registered functions.

[*Note 1*: Returning from `main` invokes `std::exit`
[[basic.start.main]]. — *end note*]

Constructed objects with thread storage duration within a given thread
are destroyed as a result of returning from the initial function of that
thread and as a result of that thread calling `std::exit`. The
destruction of all constructed objects with thread storage duration
within that thread strongly happens before destroying any object with
static storage duration.

If the completion of the constructor or dynamic initialization of an
object with static storage duration strongly happens before that of
another, the completion of the destructor of the second is sequenced
before the initiation of the destructor of the first. If the completion
of the constructor or dynamic initialization of an object with thread
storage duration is sequenced before that of another, the completion of
the destructor of the second is sequenced before the initiation of the
destructor of the first. If an object is initialized statically, the
object is destroyed in the same order as if the object was dynamically
initialized. For an object of array or class type, all subobjects of
that object are destroyed before any block-scope object with static
storage duration initialized during the construction of the subobjects
is destroyed. If the destruction of an object with static or thread
storage duration exits via an exception, the function `std::terminate`
is called [[except.terminate]].

If a function contains a block-scope object of static or thread storage
duration that has been destroyed and the function is called during the
destruction of an object with static or thread storage duration, the
program has undefined behavior if the flow of control passes through the
definition of the previously destroyed block-scope object. Likewise, the
behavior is undefined if the block-scope object is used indirectly
(i.e., through a pointer) after its destruction.

If the completion of the initialization of an object with static storage
duration strongly happens before a call to `std::atexit` (see
`<cstdlib>`, [[support.start.term]]), the call to the function passed to
`std::atexit` is sequenced before the call to the destructor for the
object. If a call to `std::atexit` strongly happens before the
completion of the initialization of an object with static storage
duration, the call to the destructor for the object is sequenced before
the call to the function passed to `std::atexit`. If a call to
`std::atexit` strongly happens before another call to `std::atexit`, the
call to the function passed to the second `std::atexit` call is
sequenced before the call to the function passed to the first
`std::atexit` call.

If there is a use of a standard library object or function not permitted
within signal handlers [[support.runtime]] that does not happen before
[[intro.multithread]] completion of destruction of objects with static
storage duration and execution of `std::atexit` registered functions
[[support.start.term]], the program has undefined behavior.

[*Note 2*: If there is a use of an object with static storage duration
that does not happen before the object’s destruction, the program has
undefined behavior. Terminating every thread before a call to
`std::exit` or the exit from `main` is sufficient, but not necessary, to
satisfy these requirements. These requirements permit thread managers as
static-storage-duration objects. — *end note*]

Calling the function `std::abort()` declared in `<cstdlib>` terminates
the program without executing any destructors and without calling the
functions passed to `std::atexit()` or `std::at_quick_exit()`.

<!-- Link reference definitions -->
[allocator.members]: utilities.md#allocator.members
[allocator.traits.members]: utilities.md#allocator.traits.members
[atomics]: atomics.md#atomics
[atomics.flag]: atomics.md#atomics.flag
[atomics.lockfree]: atomics.md#atomics.lockfree
[atomics.order]: atomics.md#atomics.order
[bad.alloc]: support.md#bad.alloc
[basic]: #basic
[basic.align]: #basic.align
[basic.compound]: #basic.compound
[basic.def]: #basic.def
[basic.def.odr]: #basic.def.odr
[basic.exec]: #basic.exec
[basic.fundamental]: #basic.fundamental
[basic.fundamental.width]: #basic.fundamental.width
[basic.funscope]: #basic.funscope
[basic.indet]: #basic.indet
[basic.life]: #basic.life
[basic.link]: #basic.link
[basic.lookup]: #basic.lookup
[basic.lookup.argdep]: #basic.lookup.argdep
[basic.lookup.classref]: #basic.lookup.classref
[basic.lookup.elab]: #basic.lookup.elab
[basic.lookup.qual]: #basic.lookup.qual
[basic.lookup.udir]: #basic.lookup.udir
[basic.lookup.unqual]: #basic.lookup.unqual
[basic.lval]: expr.md#basic.lval
[basic.memobj]: #basic.memobj
[basic.namespace]: dcl.md#basic.namespace
[basic.pre]: #basic.pre
[basic.scope]: #basic.scope
[basic.scope.block]: #basic.scope.block
[basic.scope.class]: #basic.scope.class
[basic.scope.declarative]: #basic.scope.declarative
[basic.scope.enum]: #basic.scope.enum
[basic.scope.hiding]: #basic.scope.hiding
[basic.scope.namespace]: #basic.scope.namespace
[basic.scope.param]: #basic.scope.param
[basic.scope.pdecl]: #basic.scope.pdecl
[basic.scope.temp]: #basic.scope.temp
[basic.start]: #basic.start
[basic.start.dynamic]: #basic.start.dynamic
[basic.start.main]: #basic.start.main
[basic.start.static]: #basic.start.static
[basic.start.term]: #basic.start.term
[basic.stc]: #basic.stc
[basic.stc.auto]: #basic.stc.auto
[basic.stc.dynamic]: #basic.stc.dynamic
[basic.stc.dynamic.allocation]: #basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: #basic.stc.dynamic.deallocation
[basic.stc.dynamic.safety]: #basic.stc.dynamic.safety
[basic.stc.inherit]: #basic.stc.inherit
[basic.stc.static]: #basic.stc.static
[basic.stc.thread]: #basic.stc.thread
[basic.type.qualifier]: #basic.type.qualifier
[basic.type.qualifier.rel]: #basic.type.qualifier.rel
[basic.types]: #basic.types
[bit.cast]: numerics.md#bit.cast
[c.malloc]: utilities.md#c.malloc
[class]: class.md#class
[class.abstract]: class.md#class.abstract
[class.access]: class.md#class.access
[class.base.init]: class.md#class.base.init
[class.bit]: class.md#class.bit
[class.cdtor]: class.md#class.cdtor
[class.conv.fct]: class.md#class.conv.fct
[class.copy.assign]: class.md#class.copy.assign
[class.copy.ctor]: class.md#class.copy.ctor
[class.copy.elision]: class.md#class.copy.elision
[class.default.ctor]: class.md#class.default.ctor
[class.derived]: class.md#class.derived
[class.dtor]: class.md#class.dtor
[class.free]: class.md#class.free
[class.friend]: class.md#class.friend
[class.local]: class.md#class.local
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.mfct.non-static]: class.md#class.mfct.non-static
[class.name]: class.md#class.name
[class.nest]: class.md#class.nest
[class.pre]: class.md#class.pre
[class.prop]: class.md#class.prop
[class.qual]: #class.qual
[class.spaceship]: class.md#class.spaceship
[class.static]: class.md#class.static
[class.static.data]: class.md#class.static.data
[class.temporary]: #class.temporary
[class.this]: class.md#class.this
[class.union]: class.md#class.union
[class.virtual]: class.md#class.virtual
[conv]: expr.md#conv
[conv.array]: expr.md#conv.array
[conv.func]: expr.md#conv.func
[conv.integral]: expr.md#conv.integral
[conv.lval]: expr.md#conv.lval
[conv.mem]: expr.md#conv.mem
[conv.prom]: expr.md#conv.prom
[conv.ptr]: expr.md#conv.ptr
[conv.rank]: #conv.rank
[conv.rval]: expr.md#conv.rval
[cpp.predefined]: cpp.md#cpp.predefined
[cstddef.syn]: support.md#cstddef.syn
[cstring.syn]: strings.md#cstring.syn
[dcl.align]: dcl.md#dcl.align
[dcl.array]: dcl.md#dcl.array
[dcl.attr]: dcl.md#dcl.attr
[dcl.attr.nouniqueaddr]: dcl.md#dcl.attr.nouniqueaddr
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.decl]: dcl.md#dcl.decl
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.fct.def.coroutine]: dcl.md#dcl.fct.def.coroutine
[dcl.fct.def.general]: dcl.md#dcl.fct.def.general
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.inline]: dcl.md#dcl.inline
[dcl.link]: dcl.md#dcl.link
[dcl.meaning]: dcl.md#dcl.meaning
[dcl.mptr]: dcl.md#dcl.mptr
[dcl.name]: dcl.md#dcl.name
[dcl.pre]: dcl.md#dcl.pre
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[dcl.spec]: dcl.md#dcl.spec
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.stc]: dcl.md#dcl.stc
[dcl.struct.bind]: dcl.md#dcl.struct.bind
[dcl.type.elab]: dcl.md#dcl.type.elab
[dcl.typedef]: dcl.md#dcl.typedef
[defns.block]: intro.md#defns.block
[defns.signature]: intro.md#defns.signature
[defns.signature.templ]: intro.md#defns.signature.templ
[depr.local]: future.md#depr.local
[depr.static.constexpr]: future.md#depr.static.constexpr
[diff.cpp11.basic]: compatibility.md#diff.cpp11.basic
[enum.udecl]: dcl.md#enum.udecl
[except.handle]: except.md#except.handle
[except.pre]: except.md#except.pre
[except.spec]: except.md#except.spec
[except.terminate]: except.md#except.terminate
[except.throw]: except.md#except.throw
[expr]: expr.md#expr
[expr.add]: expr.md#expr.add
[expr.alignof]: expr.md#expr.alignof
[expr.arith.conv]: expr.md#expr.arith.conv
[expr.ass]: expr.md#expr.ass
[expr.await]: expr.md#expr.await
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.comma]: expr.md#expr.comma
[expr.compound]: expr.md#expr.compound
[expr.cond]: expr.md#expr.cond
[expr.const]: expr.md#expr.const
[expr.const.cast]: expr.md#expr.const.cast
[expr.context]: expr.md#expr.context
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.eq]: expr.md#expr.eq
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.new]: expr.md#expr.new
[expr.pre]: expr.md#expr.pre
[expr.prim.id]: expr.md#expr.prim.id
[expr.prim.id.dtor]: expr.md#expr.prim.id.dtor
[expr.prim.id.qual]: expr.md#expr.prim.id.qual
[expr.prim.lambda]: expr.md#expr.prim.lambda
[expr.prim.lambda.capture]: expr.md#expr.prim.lambda.capture
[expr.prim.lambda.closure]: expr.md#expr.prim.lambda.closure
[expr.prim.this]: expr.md#expr.prim.this
[expr.prop]: expr.md#expr.prop
[expr.ref]: expr.md#expr.ref
[expr.reinterpret.cast]: expr.md#expr.reinterpret.cast
[expr.rel]: expr.md#expr.rel
[expr.sizeof]: expr.md#expr.sizeof
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.type.conv]: expr.md#expr.type.conv
[expr.typeid]: expr.md#expr.typeid
[expr.unary.op]: expr.md#expr.unary.op
[get.new.handler]: support.md#get.new.handler
[headers]: library.md#headers
[intro.execution]: #intro.execution
[intro.memory]: #intro.memory
[intro.multithread]: #intro.multithread
[intro.object]: #intro.object
[intro.progress]: #intro.progress
[intro.races]: #intro.races
[lex.charset]: lex.md#lex.charset
[lex.name]: lex.md#lex.name
[lex.separate]: lex.md#lex.separate
[locale]: localization.md#locale
[meta.trans.other]: utilities.md#meta.trans.other
[module.context]: module.md#module.context
[module.global.frag]: module.md#module.global.frag
[module.import]: module.md#module.import
[module.interface]: module.md#module.interface
[module.reach]: module.md#module.reach
[module.unit]: module.md#module.unit
[multibyte.strings]: library.md#multibyte.strings
[namespace.def]: dcl.md#namespace.def
[namespace.memdef]: dcl.md#namespace.memdef
[namespace.qual]: #namespace.qual
[namespace.udecl]: dcl.md#namespace.udecl
[namespace.udir]: dcl.md#namespace.udir
[new.delete]: support.md#new.delete
[new.delete.array]: support.md#new.delete.array
[new.delete.placement]: support.md#new.delete.placement
[new.delete.single]: support.md#new.delete.single
[new.handler]: support.md#new.handler
[over]: over.md#over
[over.literal]: over.md#over.literal
[over.match]: over.md#over.match
[over.oper]: over.md#over.oper
[over.over]: over.md#over.over
[ptr.align]: utilities.md#ptr.align
[ptr.launder]: support.md#ptr.launder
[replacement.functions]: library.md#replacement.functions
[special]: class.md#special
[stmt.block]: stmt.md#stmt.block
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.expr]: stmt.md#stmt.expr
[stmt.goto]: stmt.md#stmt.goto
[stmt.if]: stmt.md#stmt.if
[stmt.label]: stmt.md#stmt.label
[stmt.ranged]: stmt.md#stmt.ranged
[stmt.return]: stmt.md#stmt.return
[support.dynamic]: support.md#support.dynamic
[support.limits]: support.md#support.limits
[support.runtime]: support.md#support.runtime
[support.start.term]: support.md#support.start.term
[support.types]: support.md#support.types
[temp.deduct.guide]: temp.md#temp.deduct.guide
[temp.dep]: temp.md#temp.dep
[temp.dep.candidate]: temp.md#temp.dep.candidate
[temp.expl.spec]: temp.md#temp.expl.spec
[temp.explicit]: temp.md#temp.explicit
[temp.local]: temp.md#temp.local
[temp.names]: temp.md#temp.names
[temp.nondep]: temp.md#temp.nondep
[temp.over]: temp.md#temp.over
[temp.param]: temp.md#temp.param
[temp.point]: temp.md#temp.point
[temp.pre]: temp.md#temp.pre
[temp.res]: temp.md#temp.res
[temp.spec]: temp.md#temp.spec
[temp.type]: temp.md#temp.type
[thread]: thread.md#thread
[thread.jthread.class]: thread.md#thread.jthread.class
[thread.thread.class]: thread.md#thread.thread.class
[thread.threads]: thread.md#thread.threads
[util.dynamic.safety]: utilities.md#util.dynamic.safety

[^1]: Appearing inside the brace-enclosed *declaration-seq* in a
    *linkage-specification* does not affect whether a declaration is a
    definition.

[^2]: An implementation is not required to call allocation and
    deallocation functions from constructors or destructors; however,
    this is a permissible implementation technique.

[^3]: This refers to unqualified names that occur, for instance, in a
    type or default argument in the *parameter-declaration-clause* or
    used in the function body.

[^4]: This refers to unqualified names following the class name; such a
    name may be used in a *base-specifier* or in the
    *member-specification* of the class definition.

[^5]: This lookup applies whether the definition of `X` is nested within
    `Y`’s definition or whether `X`’s definition appears in a namespace
    scope enclosing `Y`’s definition [[class.nest]].

[^6]: That is, an unqualified name that occurs, for instance, in a type
    in the *parameter-declaration-clause* or in the
    *noexcept-specifier*.

[^7]: This lookup applies whether the member function is defined within
    the definition of class `X` or whether the member function is
    defined in a namespace scope enclosing `X`’s definition.

[^8]: Lookups in which function names are ignored include names
    appearing in a *nested-name-specifier*, an
    *elaborated-type-specifier*, or a *base-specifier*.

[^9]: The number of bits in a byte is reported by the macro `CHAR_BIT`
    in the header `<climits>`.

[^10]: Under the “as-if” rule an implementation is allowed to store two
    objects at the same machine address or not store an object at all if
    the program cannot observe the difference [[intro.execution]].

[^11]: For example, before the construction of a global object that is
    initialized via a user-provided constructor [[class.cdtor]].

[^12]: That is, an object for which a destructor will be called
    implicitly—upon exit from the block for an object with automatic
    storage duration, upon exit from the thread for an object with
    thread storage duration, or upon exit from the program for an object
    with static storage duration.

[^13]: Some implementations might define that copying an invalid pointer
    value causes a system-generated runtime fault.

[^14]: The intent is to have `operator new()` implementable by calling
    `std::malloc()` or `std::calloc()`, so the rules are substantially
    the same. C++ differs from C in requiring a zero request to return a
    non-null pointer.

[^15]: The global `operator delete(void*, std::size_t)` precludes use of
    an allocation function `void operator new(std::size_t, std::size_t)`
    as a placement allocation function ([[diff.cpp11.basic]]).

[^16]: This subclause does not impose restrictions on indirection
    through pointers to memory not allocated by `::operator new`. This
    maintains the ability of many C++ implementations to use binary
    libraries and components written in other languages. In particular,
    this applies to C binaries, because indirection through pointers to
    memory allocated by `std::malloc` is not restricted.

[^17]: The same rules apply to initialization of an `initializer_list`
    object [[dcl.init.list]] with its underlying temporary array.

[^18]: By using, for example, the library functions [[headers]]
    `std::memcpy` or `std::memmove`.

[^19]: By using, for example, the library functions [[headers]]
    `std::memcpy` or `std::memmove`.

[^20]: The intent is that the memory model of C++ is compatible with
    that of ISO/IEC 9899 Programming Language C.

[^21]: The size and layout of an instance of an incompletely-defined
    object type is unknown.

[^22]: This is also known as two’s complement representation.

[^23]: Static class members are objects or functions, and pointers to
    them are ordinary pointers to objects or functions.

[^24]: For an object that is not within its lifetime, this is the first
    byte in memory that it will occupy or used to occupy.

[^25]: The same representation and alignment requirements are meant to
    imply interchangeability as arguments to functions, return values
    from functions, and non-static data members of unions.

[^26]: As specified in  [[class.temporary]], after a full-expression is
    evaluated, a sequence of zero or more invocations of destructor
    functions for temporary objects takes place, usually in reverse
    order of the construction of each temporary object.

[^27]: In other words, function executions do not interleave with each
    other.

[^28]: An object with automatic or thread storage duration [[basic.stc]]
    is associated with one specific thread, and can be accessed by a
    different thread only indirectly through a pointer or reference
    [[basic.compound]].

[^29]: A non-local variable with static storage duration having
    initialization with side effects is initialized in this case, even
    if it is not itself odr-used ([[basic.def.odr]],
    [[basic.stc.static]]).
