# Basic concepts <a id="basic">[[basic]]</a>

[*Note 1*: This Clause presents the basic concepts of the C++language.
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

An *entity* is a value, object, reference, function, enumerator, type,
class member, bit-field, template, template specialization, namespace,
or parameter pack.

A *name* is a use of an *identifier* ([[lex.name]]),
*operator-function-id* ([[over.oper]]), *literal-operator-id* (
[[over.literal]]), *conversion-function-id* ([[class.conv.fct]]), or
*template-id* ([[temp.names]]) that denotes an entity or label (
[[stmt.goto]], [[stmt.label]]).

Every name that denotes an entity is introduced by a *declaration*.
Every name that denotes a label is introduced either by a `goto`
statement ([[stmt.goto]]) or a *labeled-statement* ([[stmt.label]]).

A *variable* is introduced by the declaration of a reference other than
a non-static data member or of an object. The variable’s name, if any,
denotes the reference or object.

Some names denote types or templates. In general, whenever a name is
encountered it is necessary to determine whether that name denotes one
of these entities before continuing to parse the program that contains
it. The process that determines this is called *name lookup* (
[[basic.lookup]]).

Two names are *the same* if

- they are *identifier*s composed of the same character sequence, or
- they are *operator-function-id*s formed with the same operator, or
- they are *conversion-function-id*s formed with the same type, or
- they are *template-id*s that refer to the same class, function, or
  variable ([[temp.type]]), or
- they are the names of literal operators ([[over.literal]]) formed
  with the same literal suffix identifier.

A name used in more than one translation unit can potentially refer to
the same entity in these translation units depending on the linkage (
[[basic.link]]) of the name specified in each translation unit.

## Declarations and definitions <a id="basic.def">[[basic.def]]</a>

A declaration (Clause  [[dcl.dcl]]) may introduce one or more names into
a translation unit or redeclare names introduced by previous
declarations. If so, the declaration specifies the interpretation and
attributes of these names. A declaration may also have effects
including:

- a static assertion (Clause  [[dcl.dcl]]),
- controlling template instantiation ([[temp.explicit]]),
- guiding template argument deduction for constructors (
  [[temp.deduct.guide]]),
- use of attributes (Clause  [[dcl.dcl]]), and
- nothing (in the case of an *empty-declaration*).

A declaration is a *definition* unless

- it declares a function without specifying the function’s body (
  [[dcl.fct.def]]),
- it contains the `extern` specifier ([[dcl.stc]]) or a
  *linkage-specification*[^1] ([[dcl.link]]) and neither an
  *initializer* nor a *function-body*,
- it declares a non-inline static data member in a class definition (
  [[class.mem]],  [[class.static]]),
- it declares a static data member outside a class definition and the
  variable was defined within the class with the `constexpr` specifier
  (this usage is deprecated; see [[depr.static_constexpr]]),
- it is a class name declaration ([[class.name]]),
- it is an *opaque-enum-declaration* ([[dcl.enum]]),
- it is a *template-parameter* ([[temp.param]]),
- it is a *parameter-declaration* ([[dcl.fct]]) in a function
  declarator that is not the *declarator* of a *function-definition*,
- it is a `typedef` declaration ([[dcl.typedef]]),
- it is an *alias-declaration* ([[dcl.typedef]]),
- it is a *using-declaration* ([[namespace.udecl]]),
- it is a *deduction-guide* ([[temp.deduct.guide]]),
- it is a *static_assert-declaration* (Clause  [[dcl.dcl]]),
- it is an *attribute-declaration* (Clause  [[dcl.dcl]]),
- it is an *empty-declaration* (Clause  [[dcl.dcl]]),
- it is a *using-directive* ([[namespace.udir]]),
- it is an explicit instantiation declaration ([[temp.explicit]]), or
- it is an explicit specialization ([[temp.expl.spec]]) whose
  *declaration* is not a definition.

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

[*Note 1*:  In some circumstances, C++implementations implicitly define
the default constructor ([[class.ctor]]), copy constructor (
[[class.copy]]), move constructor ([[class.copy]]), copy assignment
operator ([[class.copy]]), move assignment operator ([[class.copy]]),
or destructor ([[class.dtor]]) member functions. — *end note*]

[*Example 2*:

Given

``` cpp
#include <string>

struct C {
  std::string s;              // std::string is the standard library class (Clause~[strings])
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
    // : s(std::move(x.s)) { }
  C& operator=(const C& x) { s = x.s; return *this; }
  C& operator=(C&& x) { s = static_cast<std::string&&>(x.s); return *this; }
    // { s = std::move(x.s); return *this; }
  ~C() { }
};
```

— *end example*]

[*Note 2*: A class name can also be implicitly declared by an
*elaborated-type-specifier* ([[dcl.type.elab]]). — *end note*]

A program is ill-formed if the definition of any object gives the object
an incomplete type ([[basic.types]]).

## One-definition rule <a id="basic.def.odr">[[basic.def.odr]]</a>

No translation unit shall contain more than one definition of any
variable, function, class type, enumeration type, or template.

An expression is *potentially evaluated* unless it is an unevaluated
operand (Clause  [[expr]]) or a subexpression thereof. The set of
*potential results* of an expression `e` is defined as follows:

- If `e` is an *id-expression* ([[expr.prim.id]]), the set contains
  only `e`.
- If `e` is a subscripting operation ([[expr.sub]]) with an array
  operand, the set contains the potential results of that operand.
- If `e` is a class member access expression ([[expr.ref]]), the set
  contains the potential results of the object expression.
- If `e` is a pointer-to-member expression ([[expr.mptr.oper]]) whose
  second operand is a constant expression, the set contains the
  potential results of the object expression.
- If `e` has the form `(e1)`, the set contains the potential results of
  `e1`.
- If `e` is a glvalue conditional expression ([[expr.cond]]), the set
  is the union of the sets of potential results of the second and third
  operands.
- If `e` is a comma expression ([[expr.comma]]), the set contains the
  potential results of the right operand.
- Otherwise, the set is empty.

[*Note 1*:

This set is a (possibly-empty) set of *id-expression*s, each of which is
either `e` or a subexpression of `e`.

[*Example 1*:

In the following example, the set of potential results of the
initializer of `n` contains the first `S::x` subexpression, but not the
second `S::x` subexpression.

``` cpp
struct S { static const int x = 0; };
const int &f(const int &r);
int n = b ? (1, S::x)  // S::x is not odr-used here
          : f(S::x);   // S::x is odr-used here, so a definition is required
```

— *end example*]

— *end note*]

A variable `x` whose name appears as a potentially-evaluated expression
`ex` is *odr-used* by `ex` unless applying the lvalue-to-rvalue
conversion ([[conv.lval]]) to `x` yields a constant expression (
[[expr.const]]) that does not invoke any non-trivial functions and, if
`x` is an object, `ex` is an element of the set of potential results of
an expression `e`, where either the lvalue-to-rvalue conversion (
[[conv.lval]]) is applied to `e`, or `e` is a discarded-value
expression (Clause [[expr]]). `this` is odr-used if it appears as a
potentially-evaluated expression (including as the result of the
implicit transformation in the body of a non-static member function (
[[class.mfct.non-static]])). A virtual member function is odr-used if it
is not pure. A function whose name appears as a potentially-evaluated
expression is odr-used if it is the unique lookup result or the selected
member of a set of overloaded functions ([[basic.lookup]],
[[over.match]], [[over.over]]), unless it is a pure virtual function and
either its name is not explicitly qualified or the expression forms a
pointer to member ([[expr.unary.op]]).

[*Note 2*: This covers calls to named functions ([[expr.call]]),
operator overloading (Clause  [[over]]), user-defined conversions (
[[class.conv.fct]]), allocation functions for placement
*new-expression*s ([[expr.new]]), as well as non-default
initialization ([[dcl.init]]). A constructor selected to copy or move
an object of class type is odr-used even if the call is actually elided
by the implementation ([[class.copy]]). — *end note*]

An allocation or deallocation function for a class is odr-used by a
*new-expression* appearing in a potentially-evaluated expression as
specified in  [[expr.new]] and  [[class.free]]. A deallocation function
for a class is odr-used by a delete expression appearing in a
potentially-evaluated expression as specified in  [[expr.delete]] and 
[[class.free]]. A non-placement allocation or deallocation function for
a class is odr-used by the definition of a constructor of that class. A
non-placement deallocation function for a class is odr-used by the
definition of the destructor of that class, or by being selected by the
lookup at the point of definition of a virtual destructor (
[[class.dtor]]).[^2] An assignment operator function in a class is
odr-used by an implicitly-defined copy-assignment or move-assignment
function for another class as specified in  [[class.copy]]. A
constructor for a class is odr-used as specified in  [[dcl.init]]. A
destructor for a class is odr-used if it is potentially invoked (
[[class.dtor]]).

Every program shall contain exactly one definition of every non-inline
function or variable that is odr-used in that program outside of a
discarded statement ([[stmt.if]]); no diagnostic required. The
definition can appear explicitly in the program, it can be found in the
standard or a user-defined library, or (when appropriate) it is
implicitly defined (see  [[class.ctor]], [[class.dtor]] and
[[class.copy]]). An inline function or variable shall be defined in
every translation unit in which it is odr-used outside of a discarded
statement.

Exactly one definition of a class is required in a translation unit if
the class is used in a way that requires the class type to be complete.

[*Example 2*:

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

- an object of type `T` is defined ([[basic.def]]), or
- a non-static class data member of type `T` is declared (
  [[class.mem]]), or
- `T` is used as the allocated type or array element type in a
  *new-expression* ([[expr.new]]), or
- an lvalue-to-rvalue conversion is applied to a glvalue referring to an
  object of type `T` ([[conv.lval]]), or
- an expression is converted (either implicitly or explicitly) to type
  `T` (Clause  [[conv]], [[expr.type.conv]], [[expr.dynamic.cast]],
  [[expr.static.cast]], [[expr.cast]]), or
- an expression that is not a null pointer constant, and has type other
  than cv `void*`, is converted to the type pointer to `T` or reference
  to `T` using a standard conversion (Clause  [[conv]]), a
  `dynamic_cast` ([[expr.dynamic.cast]]) or a `static_cast` (
  [[expr.static.cast]]), or
- a class member access operator is applied to an expression of type
  `T` ([[expr.ref]]), or
- the `typeid` operator ([[expr.typeid]]) or the `sizeof` operator (
  [[expr.sizeof]]) is applied to an operand of type `T`, or
- a function with a return type or argument type of type `T` is
  defined ([[basic.def]]) or called ([[expr.call]]), or
- a class with a base class of type `T` is defined (Clause 
  [[class.derived]]), or
- an lvalue of type `T` is assigned to ([[expr.ass]]), or
- the type `T` is the subject of an `alignof` expression (
  [[expr.alignof]]), or
- an *exception-declaration* has type `T`, reference to `T`, or pointer
  to `T` ([[except.handle]]).

— *end note*]

There can be more than one definition of a class type (Clause 
[[class]]), enumeration type ([[dcl.enum]]), inline function with
external linkage ([[dcl.inline]]), inline variable with external
linkage ([[dcl.inline]]), class template (Clause  [[temp]]), non-static
function template ([[temp.fct]]), static data member of a class
template ([[temp.static]]), member function of a class template (
[[temp.mem.func]]), or template specialization for which some template
parameters are not specified ([[temp.spec]], [[temp.class.spec]]) in a
program provided that each definition appears in a different translation
unit, and provided the definitions satisfy the following requirements.
Given such an entity named `D` defined in more than one translation
unit, then

- each definition of `D` shall consist of the same sequence of tokens;
  and
- in each definition of `D`, corresponding names, looked up according
  to  [[basic.lookup]], shall refer to an entity defined within the
  definition of `D`, or shall refer to the same entity, after overload
  resolution ([[over.match]]) and after matching of partial template
  specialization ([[temp.over]]), except that a name can refer to
  - a non-volatile `const` object with internal or no linkage if the
    object
    - has the same literal type in all definitions of `D`,
    - is initialized with a constant expression ([[expr.const]]),
    - is not odr-used in any definition of `D`, and
    - has the same value in all definitions of `D`,

    or
  - a reference with internal or no linkage initialized with a constant
    expression such that the reference refers to the same entity in all
    definitions of `D`;

  and
- in each definition of `D`, corresponding entities shall have the same
  language linkage; and
- in each definition of `D`, the overloaded operators referred to, the
  implicit calls to conversion functions, constructors, operator new
  functions and operator delete functions, shall refer to the same
  function, or to a function defined within the definition of `D`; and
- in each definition of `D`, a default argument used by an (implicit or
  explicit) function call is treated as if its token sequence were
  present in the definition of `D`; that is, the default argument is
  subject to the requirements described in this paragraph (and, if the
  default argument has subexpressions with default arguments, this
  requirement applies recursively).[^3]
- if `D` is a class with an implicitly-declared constructor (
  [[class.ctor]]), it is as if the constructor was implicitly defined in
  every translation unit where it is odr-used, and the implicit
  definition in every translation unit shall call the same constructor
  for a subobject of `D`.
  \[*Example 3*:
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

If `D` is a template and is defined in more than one translation unit,
then the preceding requirements shall apply both to names from the
template’s enclosing scope used in the template definition (
[[temp.nondep]]), and also to dependent names at the point of
instantiation ([[temp.dep]]). If the definitions of `D` satisfy all
these requirements, then the behavior is as if there were a single
definition of `D`. If the definitions of `D` do not satisfy these
requirements, then the behavior is undefined.

## Scope <a id="basic.scope">[[basic.scope]]</a>

### Declarative regions and scopes <a id="basic.scope.declarative">[[basic.scope.declarative]]</a>

Every name is introduced in some portion of program text called a
*declarative region*, which is the largest part of the program in which
that name is *valid*, that is, in which that name may be used as an
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
specifier ([[class.friend]]), certain uses of the
*elaborated-type-specifier* ([[dcl.type.elab]]), and
*using-directive*s ([[namespace.udir]]) alter this general behavior.

Given a set of declarations in a single declarative region, each of
which specifies the same unqualified name,

- they shall all refer to the same entity, or all refer to functions and
  function templates; or
- exactly one declaration shall declare a class name or enumeration name
  that is not a typedef name and the other declarations shall all refer
  to the same variable, non-static data member, or enumerator, or all
  refer to functions and function templates; in this case the class name
  or enumeration name is hidden ([[basic.scope.hiding]]). \[*Note 1*: A
  namespace name or a class template name must be unique in its
  declarative region ([[namespace.alias]], Clause 
  [[temp]]). — *end note*]

[*Note 2*: These restrictions apply to the declarative region into
which a name is introduced, which is not necessarily the same as the
region in which the declaration occurs. In particular,
*elaborated-type-specifier*s ([[dcl.type.elab]]) and friend
declarations ([[class.friend]]) may introduce a (possibly not visible)
name into an enclosing namespace; these restrictions apply to that
region. Local extern declarations ([[basic.link]]) may introduce a name
into the declarative region where the declaration appears and also
introduce a (possibly not visible) name into an enclosing namespace;
these restrictions apply to both regions. — *end note*]

[*Note 3*: The name lookup rules are summarized in 
[[basic.lookup]]. — *end note*]

### Point of declaration <a id="basic.scope.pdecl">[[basic.scope.pdecl]]</a>

The *point of declaration* for a name is immediately after its complete
declarator (Clause  [[dcl.decl]]) and before its *initializer* (if any),
except as noted below.

[*Example 1*:

``` cpp
unsigned char x = 12;
{ unsigned char x = x; }
```

Here the second `x` is initialized with its own (indeterminate) value.

— *end example*]

[*Note 1*:

a name from an outer scope remains visible up to the point of
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
*simple-template-id* (if any) in its *class-head* (Clause  [[class]]).
The point of declaration for an enumeration is immediately after the
*identifier* (if any) in either its *enum-specifier* ([[dcl.enum]]) or
its first *opaque-enum-declaration* ([[dcl.enum]]), whichever comes
first. The point of declaration of an alias or alias template
immediately follows the *type-id* to which the alias refers.

The point of declaration of a *using-declarator* that does not name a
constructor is immediately after the *using-declarator* (
[[namespace.udecl]]).

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

- for a declaration of the form the *identifier* is declared to be a
  *class-name* in the scope that contains the declaration, otherwise
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

The point of declaration for an *injected-class-name* (Clause 
[[class]]) is immediately following the opening brace of the class
definition.

The point of declaration for a function-local predefined variable (
[[dcl.fct.def]]) is immediately before the *function-body* of a function
definition.

The point of declaration for a template parameter is immediately after
its complete *template-parameter*.

[*Example 4*:

``` cpp
typedef unsigned char T;
template<class T
  = T     // lookup finds the typedef name of unsigned char
  , T     // lookup finds the template parameter
    N = 0> struct A { };
```

— *end example*]

[*Note 5*: Friend declarations refer to functions or classes that are
members of the nearest enclosing namespace, but they do not introduce
new names into that namespace ([[namespace.memdef]]). Function
declarations at block scope and variable declarations with the `extern`
specifier at block scope refer to declarations that are members of an
enclosing namespace, but they do not introduce new names into that
scope. — *end note*]

[*Note 6*: For point of instantiation of a template, see 
[[temp.point]]. — *end note*]

### Block scope <a id="basic.scope.block">[[basic.scope.block]]</a>

A name declared in a block ([[stmt.block]]) is local to that block; it
has *block scope*. Its potential scope begins at its point of
declaration ([[basic.scope.pdecl]]) and ends at the end of its block. A
variable declared at block scope is a *local variable*.

The potential scope of a function parameter name (including one
appearing in a *lambda-declarator*) or of a function-local predefined
variable in a function definition ([[dcl.fct.def]]) begins at its point
of declaration. If the function has a *function-try-block* the potential
scope of a parameter or of a function-local predefined variable ends at
the end of the last associated handler, otherwise it ends at the end of
the outermost block of the function definition. A parameter name shall
not be redeclared in the outermost block of the function definition nor
in the outermost block of any handler associated with a
*function-try-block*.

The name declared in an *exception-declaration* is local to the
*handler* and shall not be redeclared in the outermost block of the
*handler*.

Names declared in the *init-statement*, the *for-range-declaration*, and
in the *condition* of `if`, `while`, `for`, and `switch` statements are
local to the `if`, `while`, `for`, or `switch` statement (including the
controlled statement), and shall not be redeclared in a subsequent
condition of that statement nor in the outermost block (or, for the `if`
statement, any of the outermost blocks) of the controlled statement;
see  [[stmt.select]].

### Function prototype scope <a id="basic.scope.proto">[[basic.scope.proto]]</a>

In a function declaration, or in any function declarator except the
declarator of a function definition ([[dcl.fct.def]]), names of
parameters (if supplied) have function prototype scope, which terminates
at the end of the nearest enclosing function declarator.

### Function scope <a id="basic.funscope">[[basic.funscope]]</a>

Labels ([[stmt.label]]) have *function scope* and may be used anywhere
in the function in which they are declared. Only labels have function
scope.

### Namespace scope <a id="basic.scope.namespace">[[basic.scope.namespace]]</a>

The declarative region of a *namespace-definition* is its
*namespace-body*. Entities declared in a *namespace-body* are said to be
*members* of the namespace, and names introduced by these declarations
into the declarative region of the namespace are said to be *member
names* of the namespace. A namespace member name has namespace scope.
Its potential scope includes its namespace from the name’s point of
declaration ([[basic.scope.pdecl]]) onwards; and for each
*using-directive* ([[namespace.udir]]) that nominates the member’s
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

A namespace member can also be referred to after the `::` scope
resolution operator ([[expr.prim]]) applied to the name of its
namespace or the name of a namespace which nominates the member’s
namespace in a *using-directive*; see  [[namespace.qual]].

The outermost declarative region of a translation unit is also a
namespace, called the *global namespace*. A name declared in the global
namespace has *global namespace scope* (also called *global scope*). The
potential scope of such a name begins at its point of declaration (
[[basic.scope.pdecl]]) and ends at the end of the translation unit that
is its declarative region. A name with global namespace scope is said to
be a *global name*.

### Class scope <a id="basic.scope.class">[[basic.scope.class]]</a>

The potential scope of a name declared in a class consists not only of
the declarative region following the name’s point of declaration, but
also of all function bodies, default arguments, *noexcept-specifier*s,
and *brace-or-equal-initializer*s of non-static data members in that
class (including such things in nested classes).

A name `N` used in a class `S` shall refer to the same declaration in
its context and when re-evaluated in the completed scope of `S`. No
diagnostic is required for a violation of this rule.

A name declared within a member function hides a declaration of the same
name whose scope extends to or past the end of the member function’s
class.

The potential scope of a declaration that extends to or past the end of
a class definition also extends to the regions defined by its member
definitions, even if the members are defined lexically outside the class
(this includes static data member definitions, nested class definitions,
and member function definitions, including the member function body and
any portion of the declarator part of such definitions which follows the
*declarator-id*, including a *parameter-declaration-clause* and any
default arguments ([[dcl.fct.default]])).

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
  (Clause  [[class.derived]]) from its class,
- after the `.` operator applied to an expression of the type of its
  class ([[expr.ref]]) or a class derived from its class,
- after the `->` operator applied to a pointer to an object of its
  class ([[expr.ref]]) or a class derived from its class,
- after the `::` scope resolution operator ([[expr.prim]]) applied to
  the name of its class or a class derived from its class.

### Enumeration scope <a id="basic.scope.enum">[[basic.scope.enum]]</a>

The name of a scoped enumerator ([[dcl.enum]]) has *enumeration scope*.
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
declaration ([[basic.scope.pdecl]]) and ends at the end of its
declarative region.

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
in an enclosing scope ([[basic.scope.hiding]]).

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
redeclared within its potential scope ([[temp.local]]), a template
parameter’s scope is often its potential scope. However, it is still
possible for a template parameter name to be hidden; see 
[[temp.local]]. — *end note*]

### Name hiding <a id="basic.scope.hiding">[[basic.scope.hiding]]</a>

A name can be hidden by an explicit declaration of that same name in a
nested declarative region or derived class ([[class.member.lookup]]).

A class name ([[class.name]]) or enumeration name ([[dcl.enum]]) can
be hidden by the name of a variable, data member, function, or
enumerator declared in the same scope. If a class or enumeration name
and a variable, data member, function, or enumerator are declared in the
same scope (in any order) with the same name, the class or enumeration
name is hidden wherever the variable, data member, function, or
enumerator name is visible.

In a member function definition, the declaration of a name at block
scope hides the declaration of a member of the class with the same name;
see  [[basic.scope.class]]. The declaration of a member in a derived
class (Clause  [[class.derived]]) hides the declaration of a member of a
base class of the same name; see  [[class.member.lookup]].

During the lookup of a name qualified by a namespace name, declarations
that would otherwise be made visible by a *using-directive* can be
hidden by declarations with the same name in the namespace containing
the *using-directive*; see  [[namespace.qual]].

If a name is in scope and is not hidden it is said to be *visible*.

## Name lookup <a id="basic.lookup">[[basic.lookup]]</a>

The name lookup rules apply uniformly to all names (including
*typedef-name*s ([[dcl.typedef]]), *namespace-name*s (
[[basic.namespace]]), and *class-name*s ([[class.name]])) wherever the
grammar allows such names in the context discussed by a particular rule.
Name lookup associates the use of a name with a set of declarations (
[[basic.def]]) of that name. The declarations found by name lookup shall
either all declare the same entity or shall all declare functions; in
the latter case, the declarations are said to form a set of overloaded
functions ([[over.load]]). Overload resolution ([[over.match]]) takes
place after name lookup has succeeded. The access rules (Clause 
[[class.access]]) are considered only once name lookup and function
overload resolution (if applicable) have succeeded. Only after name
lookup, function overload resolution (if applicable) and access checking
have succeeded are the attributes introduced by the name’s declaration
used further in expression processing (Clause  [[expr]]).

A name “looked up in the context of an expression” is looked up as an
unqualified name in the scope where the expression is found.

The injected-class-name of a class (Clause  [[class]]) is also
considered to be a member of that class for the purposes of name hiding
and lookup.

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
apply. The rules in  [[basic.lookup.argdep]] have no effect on the
syntactic interpretation of an expression. For example,

``` cpp
typedef int f;
namespace N {
  struct A {
    friend void f(A &);
    operator int();
    void g(A a) {
      int i = f(a);  // f is the typedef, not the friend function: equivalent to int(a)
    }
  };
}
```

Because the expression is not a function call, the argument-dependent
name lookup ([[basic.lookup.argdep]]) does not apply and the friend
function `f` is not found.

— *end note*]

A name used in global scope, outside of any function, class or
user-declared namespace, shall be declared before its use in global
scope.

A name used in a user-declared namespace outside of the definition of
any function or class shall be declared before its use in that namespace
or before its use in a namespace enclosing its namespace.

In the definition of a function that is a member of namespace `N`, a
name used after the function’s *declarator-id*[^4] shall be declared
before its use in the block in which it is used or in one of its
enclosing blocks ([[stmt.block]]) or shall be declared before its use
in namespace `N` or, if `N` is a nested namespace, shall be declared
before its use in one of `N`’s enclosing namespaces.

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

A name used in the definition of a class `X` outside of a member
function body, default argument, *noexcept-specifier*,
*brace-or-equal-initializer* of a non-static data member, or nested
class definition[^5] shall be declared in one of the following ways:

- before its use in class `X` or be a member of a base class of `X` (
  [[class.member.lookup]]), or
- if `X` is a nested class of class `Y` ([[class.nest]]), before the
  definition of `X` in `Y`, or shall be a member of a base class of `Y`
  (this lookup applies in turn to `Y`’s enclosing classes, starting with
  the innermost enclosing class),[^6] or
- if `X` is a local class ([[class.local]]) or is a nested class of a
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
introduced by a `friend` declaration, scopes outside of the innermost
enclosing namespace scope are not considered; see 
[[namespace.memdef]]. — *end note*]

[*Note 3*:  [[basic.scope.class]] further describes the restrictions on
the use of names in a class definition. [[class.nest]] further describes
the restrictions on the use of names in nested class definitions.
[[class.local]] further describes the restrictions on the use of names
in local class definitions. — *end note*]

For the members of a class `X`, a name used in a member function body,
in a default argument, in a *noexcept-specifier*, in the
*brace-or-equal-initializer* of a non-static data member (
[[class.mem]]), or in the definition of a class member outside of the
definition of `X`, following the member’s *declarator-id*[^7], shall be
declared in one of the following ways:

- before its use in the block in which it is used or in an enclosing
  block ([[stmt.block]]), or
- shall be a member of class `X` or be a member of a base class of `X` (
  [[class.member.lookup]]), or
- if `X` is a nested class of class `Y` ([[class.nest]]), shall be a
  member of `Y`, or shall be a member of a base class of `Y` (this
  lookup applies in turn to `Y`’s enclosing classes, starting with the
  innermost enclosing class),[^8] or
- if `X` is a local class ([[class.local]]) or is a nested class of a
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

Name lookup for a name used in the definition of a `friend` function (
[[class.friend]]) defined inline in the class granting friendship shall
proceed as described for lookup in member function definitions. If the
`friend` function is not defined in the class granting friendship, name
lookup in the `friend` function definition shall proceed as described
for lookup in namespace member function definitions.

In a `friend` declaration naming a member function, a name used in the
function declarator and not part of a *template-argument* in the
*declarator-id* is first looked up in the scope of the member function’s
class ([[class.member.lookup]]). If it is not found, or if the name is
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
  friend void A::f1(AT);      // parameter type is A::AT
  friend void A::f2(BT);      // parameter type is B::BT
  friend void A::f3<AT>();    // template argument is B::AT
};
```

— *end example*]

During the lookup for a name used as a default argument (
[[dcl.fct.default]]) in a function *parameter-declaration-clause* or
used in the *expression* of a *mem-initializer* for a constructor (
[[class.base.init]]), the function parameter names are visible and hide
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

A name used in the definition of a `static` data member of class `X` (
[[class.static.data]]) (after the *qualified-id* of the static member)
is looked up as if the name was used in a member function of `X`.

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

A name used in the handler for a *function-try-block* (Clause 
[[except]]) is looked up as if the name was used in the outermost block
of the function definition. In particular, the function parameter names
shall not be redeclared in the *exception-declaration* nor in the
outermost block of a handler for the *function-try-block*. Names
declared in the outermost block of the function definition are not found
when looked up in the scope of a handler for the *function-try-block*.

[*Note 7*: But function parameter names are found. — *end note*]

[*Note 8*: The rules for name lookup in template definitions are
described in  [[temp.res]]. — *end note*]

### Argument-dependent name lookup <a id="basic.lookup.argdep">[[basic.lookup.argdep]]</a>

When the *postfix-expression* in a function call ([[expr.call]]) is an
*unqualified-id*, other namespaces not considered during the usual
unqualified lookup ([[basic.lookup.unqual]]) may be searched, and in
those namespaces, namespace-scope friend function or function template
declarations ([[class.friend]]) not otherwise visible may be found.
These modifications to the search depend on the types of the arguments
(and for template template arguments, the namespace of the template
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
classes* to be considered. The sets of namespaces and classes are
determined entirely by the types of the function arguments (and the
namespace of any template template argument). Typedef names and
*using-declaration*s used to specify the types do not contribute to this
set. The sets of namespaces and classes are determined in the following
way:

- If `T` is a fundamental type, its associated sets of namespaces and
  classes are both empty.
- If `T` is a class type (including unions), its associated classes are:
  the class itself; the class of which it is a member, if any; and its
  direct and indirect base classes. Its associated namespaces are the
  innermost enclosing namespaces of its associated classes. Furthermore,
  if `T` is a class template specialization, its associated namespaces
  and classes also include: the namespaces and classes associated with
  the types of the template arguments provided for template type
  parameters (excluding template template parameters); the namespaces of
  which any template template arguments are members; and the classes of
  which any member templates used as template template arguments are
  members. \[*Note 1*: Non-type template arguments do not contribute to
  the set of associated namespaces. — *end note*]
- If `T` is an enumeration type, its associated namespace is the
  innermost enclosing namespace of its declaration. If it is a class
  member, its associated class is the member’s class; else it has no
  associated class.
- If `T` is a pointer to `U` or an array of `U`, its associated
  namespaces and classes are those associated with `U`.
- If `T` is a function type, its associated namespaces and classes are
  those associated with the function parameter types and those
  associated with the return type.
- If `T` is a pointer to a member function of a class `X`, its
  associated namespaces and classes are those associated with the
  function parameter types and return type, together with those
  associated with `X`.
- If `T` is a pointer to a data member of class `X`, its associated
  namespaces and classes are those associated with the member type
  together with those associated with `X`.

If an associated namespace is an inline namespace ([[namespace.def]]),
its enclosing namespace is also included in the set. If an associated
namespace directly contains inline namespaces, those inline namespaces
are also included in the set. In addition, if the argument is the name
or address of a set of overloaded functions and/or function templates,
its associated classes and namespaces are the union of those associated
with each of the members of the set, i.e., the classes and namespaces
associated with its parameter types and return type. Additionally, if
the aforementioned set of overloaded functions is named with a
*template-id*, its associated classes and namespaces also include those
of its type *template-argument*s and its template *template-argument*s.

Let *X* be the lookup set produced by unqualified lookup (
[[basic.lookup.unqual]]) and let *Y* be the lookup set produced by
argument dependent lookup (defined as follows). If *X* contains

- a declaration of a class member, or
- a block-scope function declaration that is not a *using-declaration*,
  or
- a declaration that is neither a function nor a function template

then *Y* is empty. Otherwise *Y* is the set of declarations found in the
namespaces associated with the argument types as described below. The
set of declarations found by the lookup of the name is the union of *X*
and *Y*.

[*Note 2*: The namespaces and classes associated with the argument
types can include namespaces and classes already considered by the
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

When considering an associated namespace, the lookup is the same as the
lookup performed when the associated namespace is used as a qualifier (
[[namespace.qual]]) except that:

- Any *using-directive*s in the associated namespace are ignored.
- Any namespace-scope friend functions or friend function templates
  declared in associated classes are visible within their respective
  namespaces even if they are not visible during an ordinary lookup (
  [[class.friend]]).
- All names except those of (possibly overloaded) functions and function
  templates are ignored.

### Qualified name lookup <a id="basic.lookup.qual">[[basic.lookup.qual]]</a>

The name of a class or namespace member or enumerator can be referred to
after the `::` scope resolution operator ([[expr.prim]]) applied to a
*nested-name-specifier* that denotes its class, namespace, or
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
  A b;              // ill-formed: A does not name a type
}
```

— *end example*]

[*Note 1*: Multiply qualified names, such as `N1::N2::N3::n`, can be
used to refer to members of nested classes ([[class.nest]]) or members
of nested namespaces. — *end note*]

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
X C::arr[number];   // ill-formed:
                    // equivalent to ::X C::arr[C::number];
                    // and not to C::X C::arr[C::number];
```

— *end example*]

A name prefixed by the unary scope operator `::` ([[expr.prim]]) is
looked up in global scope, in the translation unit where it is used. The
name shall be declared in global namespace scope or shall be a name
whose declaration is visible in global scope because of a
*using-directive* ([[namespace.qual]]). The use of `::` allows a global
name to be referred to even if its identifier has been hidden (
[[basic.scope.hiding]]).

A name prefixed by a *nested-name-specifier* that nominates an
enumeration type shall represent an *enumerator* of that enumeration.

If a *pseudo-destructor-name* ([[expr.pseudo]]) contains a
*nested-name-specifier*, the *type-name*s are looked up as types in the
scope designated by the *nested-name-specifier*. Similarly, in a
*qualified-id* of the form:

``` bnf
nested-name-specifierₒₚₜ class-name '::' '~' class-name
```

the second *class-name* is looked up in the same scope as the first.

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
scope of the class ([[class.member.lookup]]), except for the cases
listed below. The name shall represent one or more members of that class
or of one of its base classes (Clause  [[class.derived]]).

[*Note 1*: A class member can be referred to using a *qualified-id* at
any point in its potential scope (
[[basic.scope.class]]). — *end note*]

The exceptions to the name lookup rule above are the following:

- the lookup for a destructor is as specified in  [[basic.lookup.qual]];
- a *conversion-type-id* of a *conversion-function-id* is looked up in
  the same manner as a *conversion-type-id* in a class member access
  (see  [[basic.lookup.classref]]);
- the names in a *template-argument* of a *template-id* are looked up in
  the context in which the entire *postfix-expression* occurs.
- the lookup for a name specified in a *using-declaration* (
  [[namespace.udecl]]) also finds class or enumeration names hidden
  within the same scope ([[basic.scope.hiding]]).

In a lookup in which function names are not ignored[^9] and the
*nested-name-specifier* nominates a class `C`:

- if the name specified after the *nested-name-specifier*, when looked
  up in `C`, is the injected-class-name of `C` (Clause  [[class]]), or
- in a *using-declarator* of a *using-declaration* (
  [[namespace.udecl]]) that is a *member-declaration*, if the name
  specified after the *nested-name-specifier* is the same as the
  *identifier* or the *simple-template-id*’s *template-name* in the last
  component of the *nested-name-specifier*,

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
A::A a;             // error, A::A is not a type name
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
declarations of `m` in `X` and the inline namespace set of `X` (
[[namespace.def]]). If S'(X, m) is not empty, S(X, m) is S'(X, m);
otherwise, S(X, m) is the union of S(Nᵢ, m) for all namespaces Nᵢ
nominated by *using-directive*s in `X` and its inline namespace set.

Given `X::m` (where `X` is a user-declared namespace), or given `::m`
(where X is the global namespace), if S(X, m) is the empty set, the
program is ill-formed. Otherwise, if S(X, m) has exactly one member, or
if the context of the reference is a *using-declaration* (
[[namespace.udecl]]), S(X, m) is the required set of declarations of
`m`. Otherwise if the use of `m` is not one that allows a unique
declaration to be chosen from S(X, m), the program is ill-formed.

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
either introduce the same variable, the same enumerator or a set of
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
the *nested-name-specifier* or of an element of the inline namespace
set ([[namespace.def]]) of that namespace.

[*Example 5*:

``` cpp
namespace A {
  namespace B {
    void f1(int);
  }
  using namespace B;
}
void A::f1(int){ }  // ill-formed, f1 is not a member of A
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

An *elaborated-type-specifier* ([[dcl.type.elab]]) may be used to refer
to a previously declared *class-name* or *enum-name* even though the
name has been hidden by a non-type declaration (
[[basic.scope.hiding]]).

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
  struct Node* Next;            // OK: Refers to Node at global scope
  struct Data* Data;            // OK: Declares type Data
                                // at global scope and member Data
};

struct Data {
  struct Node* Node;            // OK: Refers to Node at global scope
  friend struct ::Glob;         // error: Glob is not declared, cannot introduce a qualified type~([dcl.type.elab])
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
struct ::Data;                  // error: cannot introduce a qualified type~([dcl.type.elab])
struct Base::Data;              // error: cannot introduce a qualified type~([dcl.type.elab])
struct Base::Datum;             // error: Datum undefined
struct Base::Data* pBase;       // OK: refers to nested Data
```

— *end example*]

### Class member access <a id="basic.lookup.classref">[[basic.lookup.classref]]</a>

In a class member access expression ([[expr.ref]]), if the `.` or `->`
token is immediately followed by an *identifier* followed by a `<`, the
identifier must be looked up to determine whether the `<` is the
beginning of a template argument list ([[temp.names]]) or a less-than
operator. The identifier is first looked up in the class of the object
expression. If the identifier is not found, it is then looked up in the
context of the entire *postfix-expression* and shall name a class
template.

If the *id-expression* in a class member access ([[expr.ref]]) is an
*unqualified-id*, and the type of the object expression is of a class
type `C`, the *unqualified-id* is looked up in the scope of class `C`.
For a pseudo-destructor call ([[expr.pseudo]]), the *unqualified-id* is
looked up in the context of the complete *postfix-expression*.

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

the *class-name-or-namespace-name* following the `.` or `->` operator is
first looked up in the class of the object expression and the name, if
found, is used. Otherwise it is looked up in the context of the entire
*postfix-expression*.

[*Note 1*: See  [[basic.lookup.qual]], which describes the lookup of a
name before `::`, which will only find a type or namespace
name. — *end note*]

If the *qualified-id* has the form

``` cpp
::class-name-or-namespace-name::...
```

the *class-name-or-namespace-name* is looked up in global scope as a
*class-name* or *namespace-name*.

If the *nested-name-specifier* contains a *simple-template-id* (
[[temp.names]]), the names in its *template-argument*s are looked up in
the context in which the entire *postfix-expression* occurs.

If the *id-expression* is a *conversion-function-id*, its
*conversion-type-id* is first looked up in the class of the object
expression and the name, if found, is used. Otherwise it is looked up in
the context of the entire *postfix-expression*. In each of these
lookups, only names that denote types or templates whose specializations
are types are considered.

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

A *program* consists of one or more *translation units* (Clause 
[[lex]]) linked together. A translation unit consists of a sequence of
declarations.

``` bnf
translation-unit:
    declaration-seqₒₚₜ
```

A name is said to have *linkage* when it might denote the same object,
reference, function, type, template, namespace or value as a name
introduced by a declaration in another scope:

- When a name has *external linkage*, the entity it denotes can be
  referred to by names from scopes of other translation units or from
  other scopes of the same translation unit.
- When a name has *internal linkage*, the entity it denotes can be
  referred to by names from other scopes in the same translation unit.
- When a name has *no linkage*, the entity it denotes cannot be referred
  to by names from other scopes.

A name having namespace scope ([[basic.scope.namespace]]) has internal
linkage if it is the name of

- a variable, function or function template that is explicitly declared
  `static`; or,
- a non-inline variable of non-volatile const-qualified type that is
  neither explicitly declared `extern` nor previously declared to have
  external linkage; or
- a data member of an anonymous union.

An unnamed namespace or a namespace declared directly or indirectly
within an unnamed namespace has internal linkage. All other namespaces
have external linkage. A name having namespace scope that has not been
given internal linkage above has the same linkage as the enclosing
namespace if it is the name of

- a variable; or
- a function; or
- a named class (Clause  [[class]]), or an unnamed class defined in a
  typedef declaration in which the class has the typedef name for
  linkage purposes ([[dcl.typedef]]); or
- a named enumeration ([[dcl.enum]]), or an unnamed enumeration defined
  in a typedef declaration in which the enumeration has the typedef name
  for linkage purposes ([[dcl.typedef]]); or
- a template.

In addition, a member function, static data member, a named class or
enumeration of class scope, or an unnamed class or enumeration defined
in a class-scope typedef declaration such that the class or enumeration
has the typedef name for linkage purposes ([[dcl.typedef]]), has the
same linkage, if any, as the name of the class of which it is a member.

The name of a function declared in block scope and the name of a
variable declared by a block scope `extern` declaration have linkage. If
there is a visible declaration of an entity with linkage having the same
name and type, ignoring entities declared outside the innermost
enclosing namespace scope, the block scope declaration declares that
same entity and receives the linkage of the previous declaration. If
there is more than one such matching entity, the program is ill-formed.
Otherwise, if no matching entity is found, the block scope entity
receives external linkage. If, within a translation unit, the same
entity is declared with both internal and external linkage, the program
is ill-formed.

[*Example 1*:

``` cpp
static void f();
static int i = 0;               // #1
void g() {
  extern void f();              // internal linkage
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
noted, a name declared at block scope ([[basic.scope.block]]) has no
linkage. A type is said to have linkage if and only if:

- it is a class or enumeration type that is named (or has a name for
  linkage purposes ([[dcl.typedef]])) and the name has linkage; or
- it is an unnamed class or unnamed enumeration that is a member of a
  class with linkage; or
- it is a specialization of a class template (Clause  [[temp]])[^10]; or
- it is a fundamental type ([[basic.fundamental]]); or
- it is a compound type ([[basic.compound]]) other than a class or
  enumeration, compounded exclusively from types that have linkage; or
- it is a cv-qualified ([[basic.type.qualifier]]) version of a type
  that has linkage.

A type without linkage shall not be used as the type of a variable or
function with external linkage unless

- the entity has C language linkage ([[dcl.link]]), or
- the entity is declared within an unnamed namespace (
  [[namespace.def]]), or
- the entity is not odr-used ([[basic.def.odr]]) or is defined in the
  same translation unit.

[*Note 1*: In other words, a type without linkage contains a class or
enumeration that cannot be named outside its translation unit. An entity
with external linkage declared using such a type could not correspond to
any other entity in another translation unit of the program and thus
must be defined in the translation unit if it is odr-used. Also note
that classes with linkage may contain members whose types do not have
linkage, and that typedef names are ignored in the determination of
whether a type has linkage. — *end note*]

[*Example 3*:

``` cpp
template <class T> struct B {
  void g(T) { }
  void h(T);
  friend void i(B, T) { }
};

void f() {
  struct A { int x; };  // no linkage
  A a = { 1 };
  B<A> ba;              // declares B<A>::g(A) and B<A>::h(A)
  ba.g(a);              // OK
  ba.h(a);              // error: B<A>::h(A) not defined in the translation unit
  i(ba, a);             // OK
}
```

— *end example*]

Two names that are the same (Clause  [[basic]]) and that are declared in
different scopes shall denote the same variable, function, type,
template or namespace if

- both names have external linkage or else both names have internal
  linkage and are declared in the same translation unit; and
- both names refer to members of the same namespace or to members, not
  by inheritance, of the same class; and
- when both names denote functions, the parameter-type-lists of the
  functions ([[dcl.fct]]) are identical; and
- when both names denote function templates, the signatures (
  [[temp.over.link]]) are the same.

After all adjustments of types (during which typedefs ([[dcl.typedef]])
are replaced by their definitions), the types specified by all
declarations referring to a given variable or function shall be
identical, except that declarations for an array object can specify
array types that differ by the presence or absence of a major array
bound ([[dcl.array]]). A violation of this rule on type identity does
not require a diagnostic.

[*Note 2*: Linkage to non-C++declarations can be achieved using a
*linkage-specification* ([[dcl.link]]). — *end note*]

## Start and termination <a id="basic.start">[[basic.start]]</a>

### `main` function <a id="basic.start.main">[[basic.start.main]]</a>

A program shall contain a global function called `main`. Executing a
program starts a main thread of execution ([[intro.multithread]],
[[thread.threads]]) in which the `main` function is invoked, and in
which variables of static storage duration might be initialized (
[[basic.start.static]]) and destroyed ([[basic.start.term]]). It is
*implementation-defined* whether a program in a freestanding environment
is required to define a `main` function.

[*Note 1*: In a freestanding environment, start-up and termination is
*implementation-defined*; start-up contains the execution of
constructors for objects of namespace scope with static storage
duration; termination contains the execution of destructors for objects
with static storage duration. — *end note*]

An implementation shall not predefine the `main` function. This function
shall not be overloaded. Its type shall have C++language linkage and it
shall have a declared return type of type `int`, but otherwise its type
is *implementation-defined*. An implementation shall allow both

- a function of `()` returning `int` and
- a function of `(int`, pointer to pointer to `char)` returning `int`

as the type of `main` ([[dcl.fct]]). In the latter form, for purposes
of exposition, the first function parameter is called `argc` and the
second function parameter is called `argv`, where `argc` shall be the
number of arguments passed to the program from the environment in which
the program is run. If `argc` is nonzero these arguments shall be
supplied in `argv[0]` through `argv[argc-1]` as pointers to the initial
characters of null-terminated multibyte strings (NTMBS s) (
[[multibyte.strings]]) and `argv[0]` shall be the pointer to the initial
character of a NTMBSthat represents the name used to invoke the program
or `""`. The value of `argc` shall be non-negative. The value of
`argv[argc]` shall be 0.

[*Note 2*: It is recommended that any further (optional) parameters be
added after `argv`. — *end note*]

The function `main` shall not be used within a program. The linkage (
[[basic.link]]) of `main` is *implementation-defined*. A program that
defines `main` as deleted or that declares `main` to be `inline`,
`static`, or `constexpr` is ill-formed. The `main` function shall not be
declared with a *linkage-specification* ([[dcl.link]]). A program that
declares a variable `main` at global scope or that declares the name
`main` with C language linkage (in any namespace) is ill-formed. The
name `main` is not otherwise reserved.

[*Example 1*: Member functions, classes, and enumerations can be called
`main`, as can entities in other namespaces. — *end example*]

Terminating the program without leaving the current block (e.g., by
calling the function `std::exit(int)` ([[support.start.term]])) does
not destroy any objects with automatic storage duration (
[[class.dtor]]). If `std::exit` is called to end a program during the
destruction of an object with static or thread storage duration, the
program has undefined behavior.

A return statement in `main` has the effect of leaving the main function
(destroying any objects with automatic storage duration) and calling
`std::exit` with the return value as the argument. If control flows off
the end of the *compound-statement* of `main`, the effect is equivalent
to a `return` with operand `0` (see also [[except.handle]]).

### Static initialization <a id="basic.start.static">[[basic.start.static]]</a>

Variables with static storage duration are initialized as a consequence
of program initiation. Variables with thread storage duration are
initialized as a consequence of thread execution. Within each of these
phases of initiation, initialization occurs as follows.

A *constant initializer* for a variable or temporary object `o` is an
initializer whose full-expression is a constant expression, except that
if `o` is an object, such an initializer may also invoke constexpr
constructors for `o` and its subobjects even if those objects are of
non-literal class types.

[*Note 1*: Such a class may have a non-trivial
destructor. — *end note*]

*Constant initialization* is performed if a variable or temporary object
with static or thread storage duration is initialized by a constant
initializer for the entity. If constant initialization is not performed,
a variable with static storage duration ([[basic.stc.static]]) or
thread storage duration ([[basic.stc.thread]]) is zero-initialized (
[[dcl.init]]). Together, zero-initialization and constant initialization
are called *static initialization*; all other initialization is *dynamic
initialization*. All static initialization strongly happens before (
[[intro.races]]) any dynamic initialization.

[*Note 2*: The dynamic initialization of non-local variables is
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

[*Note 3*:

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

### Dynamic initialization of non-local variables <a id="basic.start.dynamic">[[basic.start.dynamic]]</a>

Dynamic initialization of a non-local variable with static storage
duration is unordered if the variable is an implicitly or explicitly
instantiated specialization, is partially-ordered if the variable is an
inline variable that is not an implicitly or explicitly instantiated
specialization, and otherwise is ordered.

[*Note 1*: An explicitly specialized non-inline static data member or
variable template specialization has ordered
initialization. — *end note*]

Dynamic initialization of non-local variables `V` and `W` with static
storage duration are ordered as follows:

- If `V` and `W` have ordered initialization and `V` is defined before
  `W` within a single translation unit, the initialization of `V` is
  sequenced before the initialization of `W`.
- If `V` has partially-ordered initialization, `W` does not have
  unordered initialization, and `V` is defined before `W` in every
  translation unit in which `W` is defined, then
  - if the program starts a thread ([[intro.multithread]]) other than
    the main thread ([[basic.start.main]]), the initialization of `V`
    strongly happens before the initialization of `W`;
  - otherwise, the initialization of `V` is sequenced before the
    initialization of `W`.
- Otherwise, if the program starts a thread other than the main thread
  before either `V` or `W` is initialized, it is unspecified in which
  threads the initializations of `V` and `W` occur; the initializations
  are unsequenced if they occur in the same thread.
- Otherwise, the initializations of `V` and `W` are indeterminately
  sequenced.

[*Note 2*: This definition permits initialization of a sequence of
ordered variables concurrently with another sequence. — *end note*]

A *non-initialization odr-use* is an odr-use ([[basic.def.odr]]) not
caused directly or indirectly by the initialization of a non-local
static or thread storage duration variable.

It is *implementation-defined* whether the dynamic initialization of a
non-local non-inline variable with static storage duration is sequenced
before the first statement of `main` or is deferred. If it is deferred,
it strongly happens before any non-initialization odr-use of any
non-inline function or non-inline variable defined in the same
translation unit as the variable to be initialized. [^11] It is
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
storage duration exits via an exception, `std::terminate` is called (
[[except.terminate]]).

### Termination <a id="basic.start.term">[[basic.start.term]]</a>

Destructors ([[class.dtor]]) for initialized objects (that is, objects
whose lifetime ([[basic.life]]) has begun) with static storage
duration, and functions registered with `std::atexit`, are called as
part of a call to `std::exit` ([[support.start.term]]). The call to
`std::exit` is sequenced before the invocations of the destructors and
the registered functions.

[*Note 1*: Returning from `main` invokes `std::exit` (
[[basic.start.main]]). — *end note*]

Destructors for initialized objects with thread storage duration within
a given thread are called as a result of returning from the initial
function of that thread and as a result of that thread calling
`std::exit`. The completions of the destructors for all initialized
objects with thread storage duration within that thread strongly happen
before the initiation of the destructors of any object with static
storage duration.

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
storage duration exits via an exception, `std::terminate` is called (
[[except.terminate]]).

If a function contains a block-scope object of static or thread storage
duration that has been destroyed and the function is called during the
destruction of an object with static or thread storage duration, the
program has undefined behavior if the flow of control passes through the
definition of the previously destroyed block-scope object. Likewise, the
behavior is undefined if the block-scope object is used indirectly
(i.e., through a pointer) after its destruction.

If the completion of the initialization of an object with static storage
duration strongly happens before a call to `std::atexit` (see
`<cstdlib>`,  [[support.start.term]]), the call to the function passed
to `std::atexit` is sequenced before the call to the destructor for the
object. If a call to `std::atexit` strongly happens before the
completion of the initialization of an object with static storage
duration, the call to the destructor for the object is sequenced before
the call to the function passed to `std::atexit`. If a call to
`std::atexit` strongly happens before another call to `std::atexit`, the
call to the function passed to the second `std::atexit` call is
sequenced before the call to the function passed to the first
`std::atexit` call.

If there is a use of a standard library object or function not permitted
within signal handlers ([[support.runtime]]) that does not happen
before ([[intro.multithread]]) completion of destruction of objects
with static storage duration and execution of `std::atexit` registered
functions ([[support.start.term]]), the program has undefined behavior.

[*Note 2*: If there is a use of an object with static storage duration
that does not happen before the object’s destruction, the program has
undefined behavior. Terminating every thread before a call to
`std::exit` or the exit from `main` is sufficient, but not necessary, to
satisfy these requirements. These requirements permit thread managers as
static-storage-duration objects. — *end note*]

Calling the function `std::abort()` declared in `<cstdlib>` terminates
the program without executing any destructors and without calling the
functions passed to `std::atexit()` or `std::at_quick_exit()`.

## Storage duration <a id="basic.stc">[[basic.stc]]</a>

The *storage duration* is the property of an object that defines the
minimum potential lifetime of the storage containing the object. The
storage duration is determined by the construct used to create the
object and is one of the following:

- static storage duration
- thread storage duration
- automatic storage duration
- dynamic storage duration

Static, thread, and automatic storage durations are associated with
objects introduced by declarations ([[basic.def]]) and implicitly
created by the implementation ([[class.temporary]]). The dynamic
storage duration is associated with objects created by a
*new-expression* ([[expr.new]]).

The storage duration categories apply to references as well.

When the end of the duration of a region of storage is reached, the
values of all pointers representing the address of any part of that
region of storage become invalid pointer values ([[basic.compound]]).
Indirection through an invalid pointer value and passing an invalid
pointer value to a deallocation function have undefined behavior. Any
other use of an invalid pointer value has *implementation-defined*
behavior.[^12]

### Static storage duration <a id="basic.stc.static">[[basic.stc.static]]</a>

All variables which do not have dynamic storage duration, do not have
thread storage duration, and are not local have *static storage
duration*. The storage for these entities shall last for the duration of
the program ([[basic.start.static]], [[basic.start.term]]).

If a variable with static storage duration has initialization or a
destructor with side effects, it shall not be eliminated even if it
appears to be unused, except that a class object or its copy/move may be
eliminated as specified in  [[class.copy]].

The keyword `static` can be used to declare a local variable with static
storage duration.

[*Note 1*:  [[stmt.dcl]] describes the initialization of local `static`
variables; [[basic.start.term]] describes the destruction of local
`static` variables. — *end note*]

The keyword `static` applied to a class data member in a class
definition gives the data member static storage duration.

### Thread storage duration <a id="basic.stc.thread">[[basic.stc.thread]]</a>

All variables declared with the `thread_local` keyword have *thread
storage duration*. The storage for these entities shall last for the
duration of the thread in which they are created. There is a distinct
object or reference per thread, and use of the declared name refers to
the entity associated with the current thread.

A variable with thread storage duration shall be initialized before its
first odr-use ([[basic.def.odr]]) and, if constructed, shall be
destroyed on thread exit.

### Automatic storage duration <a id="basic.stc.auto">[[basic.stc.auto]]</a>

Block-scope variables not explicitly declared `static`, `thread_local`,
or `extern` have *automatic storage duration*. The storage for these
entities lasts until the block in which they are created exits.

[*Note 1*: These variables are initialized and destroyed as described
in  [[stmt.dcl]]. — *end note*]

If a variable with automatic storage duration has initialization or a
destructor with side effects, an implementation shall not destroy it
before the end of its block nor eliminate it as an optimization, even if
it appears to be unused, except that a class object or its copy/move may
be eliminated as specified in  [[class.copy]].

### Dynamic storage duration <a id="basic.stc.dynamic">[[basic.stc.dynamic]]</a>

Objects can be created dynamically during program execution (
[[intro.execution]]), using *new-expression*s ([[expr.new]]), and
destroyed using *delete-expression*s ([[expr.delete]]). A
C++implementation provides access to, and management of, dynamic storage
via the global *allocation functions* `operator new` and `operator
new[]` and the global *deallocation functions* `operator
delete` and `operator delete[]`.

[*Note 1*: The non-allocating forms described in
[[new.delete.placement]] do not perform allocation or
deallocation. — *end note*]

The library provides default definitions for the global allocation and
deallocation functions. Some global allocation and deallocation
functions are replaceable ([[new.delete]]). A C++program shall provide
at most one definition of a replaceable allocation or deallocation
function. Any such function definition replaces the default version
provided in the library ([[replacement.functions]]). The following
allocation and deallocation functions ([[support.dynamic]]) are
implicitly declared in global scope in each translation unit of a
program.

``` cpp
void* operator new(std::size_t);
void* operator new(std::size_t, std::align_val_t);

void operator delete(void*) noexcept;
void operator delete(void*, std::size_t) noexcept;
void operator delete(void*, std::align_val_t) noexcept;
void operator delete(void*, std::size_t, std::align_val_t) noexcept;

void* operator new[](std::size_t);
void* operator new[](std::size_t, std::align_val_t);

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
*delete-expression* or function call that refers to one of these
functions without including the header `<new>` is well-formed. However,
referring to `std` or `std::size_t` or `std::align_val_t` is ill-formed
unless the name has been declared by including the appropriate
header. — *end note*]

Allocation and/or deallocation functions may also be declared and
defined for any class ([[class.free]]).

Any allocation and/or deallocation functions defined in a C++program,
including the default versions in the library, shall conform to the
semantics specified in  [[basic.stc.dynamic.allocation]] and 
[[basic.stc.dynamic.deallocation]].

#### Allocation functions <a id="basic.stc.dynamic.allocation">[[basic.stc.dynamic.allocation]]</a>

An allocation function shall be a class member function or a global
function; a program is ill-formed if an allocation function is declared
in a namespace scope other than global scope or declared static in
global scope. The return type shall be `void*`. The first parameter
shall have type `std::size_t` ([[support.types]]). The first parameter
shall not have an associated default argument ([[dcl.fct.default]]).
The value of the first parameter shall be interpreted as the requested
size of the allocation. An allocation function can be a function
template. Such a template shall declare its return type and first
parameter as specified above (that is, template parameter types shall
not be used in the return type and first parameter type). Template
allocation functions shall have two or more parameters.

The allocation function attempts to allocate the requested amount of
storage. If it is successful, it shall return the address of the start
of a block of storage whose length in bytes shall be at least as large
as the requested size. There are no constraints on the contents of the
allocated storage on return from the allocation function. The order,
contiguity, and initial value of storage allocated by successive calls
to an allocation function are unspecified. The pointer returned shall be
suitably aligned so that it can be converted to a pointer to any
suitable complete object type ([[new.delete.single]]) and then used to
access the object or array in the storage allocated (until the storage
is explicitly deallocated by a call to a corresponding deallocation
function). Even if the size of the space requested is zero, the request
can fail. If the request succeeds, the value returned shall be a
non-null pointer value ([[conv.ptr]]) `p0` different from any
previously returned value `p1`, unless that value `p1` was subsequently
passed to an `operator` `delete`. Furthermore, for the library
allocation functions in  [[new.delete.single]] and 
[[new.delete.array]], `p0` shall represent the address of a block of
storage disjoint from the storage for any other object accessible to the
caller. The effect of indirecting through a pointer returned as a
request for zero size is undefined.[^13]

An allocation function that fails to allocate storage can invoke the
currently installed new-handler function ([[new.handler]]), if any.

[*Note 1*:  A program-supplied allocation function can obtain the
address of the currently installed `new_handler` using the
`std::get_new_handler` function ([[set.new.handler]]). — *end note*]

If an allocation function that has a non-throwing exception
specification ([[except.spec]]) fails to allocate storage, it shall
return a null pointer. Any other allocation function that fails to
allocate storage shall indicate failure only by throwing an exception (
[[except.throw]]) of a type that would match a handler (
[[except.handle]]) of type `std::bad_alloc` ([[bad.alloc]]).

A global allocation function is only called as the result of a new
expression ([[expr.new]]), or called directly using the function call
syntax ([[expr.call]]), or called indirectly through calls to the
functions in the C++standard library.

[*Note 2*: In particular, a global allocation function is not called to
allocate storage for objects with static storage duration (
[[basic.stc.static]]), for objects or references with thread storage
duration ([[basic.stc.thread]]), for objects of type `std::type_info` (
[[expr.typeid]]), or for an exception object (
[[except.throw]]). — *end note*]

#### Deallocation functions <a id="basic.stc.dynamic.deallocation">[[basic.stc.dynamic.deallocation]]</a>

Deallocation functions shall be class member functions or global
functions; a program is ill-formed if deallocation functions are
declared in a namespace scope other than global scope or declared static
in global scope.

Each deallocation function shall return `void` and its first parameter
shall be `void*`. A deallocation function may have more than one
parameter. A *usual deallocation function* is a deallocation function
that has:

- exactly one parameter; or
- exactly two parameters, the type of the second being either
  `std::align_val_t` or `std::size_t` [^14]; or
- exactly three parameters, the type of the second being `std::size_t`
  and the type of the third being `std::align_val_t`.

A deallocation function may be an instance of a function template.
Neither the first parameter nor the return type shall depend on a
template parameter.

[*Note 1*: That is, a deallocation function template shall have a first
parameter of type `void*` and a return type of `void` (as specified
above). — *end note*]

A deallocation function template shall have two or more function
parameters. A template instance is never a usual deallocation function,
regardless of its signature.

If a deallocation function terminates by throwing an exception, the
behavior is undefined. The value of the first argument supplied to a
deallocation function may be a null pointer value; if so, and if the
deallocation function is one supplied in the standard library, the call
has no effect.

If the argument given to a deallocation function in the standard library
is a pointer that is not the null pointer value ([[conv.ptr]]), the
deallocation function shall deallocate the storage referenced by the
pointer, ending the duration of the region of storage.

#### Safely-derived pointers <a id="basic.stc.dynamic.safety">[[basic.stc.dynamic.safety]]</a>

A *traceable pointer object* is

- an object of an object pointer type ([[basic.compound]]), or
- an object of an integral type that is at least as large as
  `std::intptr_t`, or
- a sequence of elements in an array of narrow character type (
  [[basic.fundamental]]), where the size and alignment of the sequence
  match those of some object pointer type.

A pointer value is a *safely-derived pointer* to a dynamic object only
if it has an object pointer type and it is one of the following:

- the value returned by a call to the C++standard library implementation
  of `::operator new(std::{}size_t)` or
  `::operator new(std::size_t, std::align_val_t)` ;[^15]
- the result of taking the address of an object (or one of its
  subobjects) designated by an lvalue resulting from indirection through
  a safely-derived pointer value;
- the result of well-defined pointer arithmetic ([[expr.add]]) using a
  safely-derived pointer value;
- the result of a well-defined pointer conversion ([[conv.ptr]], 
  [[expr.cast]]) of a safely-derived pointer value;
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
object has previously been declared reachable (
[[util.dynamic.safety]]).

[*Note 1*: The effect of using an invalid pointer value (including
passing it to a deallocation function) is undefined, see 
[[basic.stc.dynamic.deallocation]]. This is true even if the
unsafely-derived pointer value might compare equal to some
safely-derived pointer value. — *end note*]

It is *implementation-defined* whether an implementation has relaxed or
strict pointer safety.

### Duration of subobjects <a id="basic.stc.inherit">[[basic.stc.inherit]]</a>

The storage duration of subobjects and reference members is that of
their complete object ([[intro.object]]).

## Object lifetime <a id="basic.life">[[basic.life]]</a>

The *lifetime* of an object or reference is a runtime property of the
object or reference. An object is said to have *non-vacuous
initialization* if it is of a class or aggregate type and it or one of
its subobjects is initialized by a constructor other than a trivial
default constructor.

[*Note 1*: Initialization by a trivial copy/move constructor is
non-vacuous initialization. — *end note*]

The lifetime of an object of type `T` begins when:

- storage with the proper alignment and size for type `T` is obtained,
  and
- if the object has non-vacuous initialization, its initialization is
  complete,

except that if the object is a union member or subobject thereof, its
lifetime only begins if that union member is the initialized member in
the union ([[dcl.init.aggr]], [[class.base.init]]), or as described in
[[class.union]]. The lifetime of an object *o* of type `T` ends when:

- if `T` is a class type with a non-trivial destructor (
  [[class.dtor]]), the destructor call starts, or
- the storage which the object occupies is released, or is reused by an
  object that is not nested within *o* ([[intro.object]]).

The lifetime of a reference begins when its initialization is complete.
The lifetime of a reference ends as if it were a scalar object.

[*Note 2*:  [[class.base.init]] describes the lifetime of base and
member subobjects. — *end note*]

The properties ascribed to objects and references throughout this
International Standard apply for a given object or reference only during
its lifetime.

[*Note 3*: In particular, before the lifetime of an object starts and
after its lifetime ends there are significant restrictions on the use of
the object, as described below, in  [[class.base.init]] and in 
[[class.cdtor]]. Also, the behavior of an object under construction and
destruction might not be the same as the behavior of an object whose
lifetime has started and not ended. [[class.base.init]] and 
[[class.cdtor]] describe the behavior of objects during the construction
and destruction phases. — *end note*]

A program may end the lifetime of any object by reusing the storage
which the object occupies or by explicitly calling the destructor for an
object of a class type with a non-trivial destructor. For an object of a
class type with a non-trivial destructor, the program is not required to
call the destructor explicitly before the storage which the object
occupies is reused or released; however, if there is no explicit call to
the destructor or if a *delete-expression* ([[expr.delete]]) is not
used to release the storage, the destructor shall not be implicitly
called and any program that depends on the side effects produced by the
destructor has undefined behavior.

Before the lifetime of an object has started but after the storage which
the object will occupy has been allocated[^16] or, after the lifetime of
an object has ended and before the storage which the object occupied is
reused or released, any pointer that represents the address of the
storage location where the object will be or was located may be used but
only in limited ways. For an object under construction or destruction,
see  [[class.cdtor]]. Otherwise, such a pointer refers to allocated
storage ([[basic.stc.dynamic.deallocation]]), and using the pointer as
if the pointer were of type `void*`, is well-defined. Indirection
through such a pointer is permitted but the resulting lvalue may only be
used in limited ways, as described below. The program has undefined
behavior if:

- the object will be or was of a class type with a non-trivial
  destructor and the pointer is used as the operand of a
  *delete-expression*,
- the pointer is used to access a non-static data member or call a
  non-static member function of the object, or
- the pointer is implicitly converted ([[conv.ptr]]) to a pointer to a
  virtual base class, or
- the pointer is used as the operand of a `static_cast` (
  [[expr.static.cast]]), except when the conversion is to pointer to
  cv `void`, or to pointer to cv `void` and subsequently to pointer to
  cv `char`, cv `unsigned char`, or cv `std::byte` ([[cstddef.syn]]),
  or
- the pointer is used as the operand of a `dynamic_cast` (
  [[expr.dynamic.cast]]).

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
  pb->f();          // undefined behavior, lifetime of *pb has ended
}
```

— *end example*]

Similarly, before the lifetime of an object has started but after the
storage which the object will occupy has been allocated or, after the
lifetime of an object has ended and before the storage which the object
occupied is reused or released, any glvalue that refers to the original
object may be used but only in limited ways. For an object under
construction or destruction, see  [[class.cdtor]]. Otherwise, such a
glvalue refers to allocated storage (
[[basic.stc.dynamic.deallocation]]), and using the properties of the
glvalue that do not depend on its value is well-defined. The program has
undefined behavior if:

- the glvalue is used to access the object, or
- the glvalue is used to call a non-static member function of the
  object, or
- the glvalue is bound to a reference to a virtual base class (
  [[dcl.init.ref]]), or
- the glvalue is used as the operand of a `dynamic_cast` (
  [[expr.dynamic.cast]]) or as the operand of `typeid`.

If, after the lifetime of an object has ended and before the storage
which the object occupied is reused or released, a new object is created
at the storage location which the original object occupied, a pointer
that pointed to the original object, a reference that referred to the
original object, or the name of the original object will automatically
refer to the new object and, once the lifetime of the new object has
started, can be used to manipulate the new object, if:

- the storage for the new object exactly overlays the storage location
  which the original object occupied, and
- the new object is of the same type as the original object (ignoring
  the top-level cv-qualifiers), and
- the type of the original object is not const-qualified, and, if a
  class type, does not contain any non-static data member whose type is
  const-qualified or a reference type, and
- the original object was a most derived object ([[intro.object]]) of
  type `T` and the new object is a most derived object of type `T` (that
  is, they are not base class subobjects).

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

[*Note 4*: If these conditions are not met, a pointer to the new object
can be obtained from a pointer that represents the address of its
storage by calling `std::launder` ([[support.dynamic]]). — *end note*]

If a program ends the lifetime of an object of type `T` with static (
[[basic.stc.static]]), thread ([[basic.stc.thread]]), or automatic (
[[basic.stc.auto]]) storage duration and if `T` has a non-trivial
destructor,[^17] the program must ensure that an object of the original
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

Creating a new object within the storage that a `const` complete object
with static, thread, or automatic storage duration occupies, or within
the storage that such a `const` object used to occupy before its
lifetime ended, results in undefined behavior.

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

In this section, “before” and “after” refer to the “happens before”
relation ([[intro.multithread]]).

[*Note 5*: Therefore, undefined behavior results if an object that is
being constructed in one thread is referenced from another thread
without adequate synchronization. — *end note*]

## Types <a id="basic.types">[[basic.types]]</a>

[*Note 1*:  [[basic.types]] and the subclauses thereof impose
requirements on implementations regarding the representation of types.
There are two kinds of types: fundamental types and compound types.
Types describe objects ([[intro.object]]), references ([[dcl.ref]]),
or functions ([[dcl.fct]]). — *end note*]

For any object (other than a base-class subobject) of trivially copyable
type `T`, whether or not the object holds a valid value of type `T`, the
underlying bytes ([[intro.memory]]) making up the object can be copied
into an array of `char`, `unsigned char`, or `std::byte` (
[[cstddef.syn]]). [^18] If the content of that array is copied back into
the object, the object shall subsequently hold its original value.

[*Example 1*:

``` cpp
#define N sizeof(T)
char buf[N];
T obj;                          // obj initialized to its original value
std::memcpy(buf, &obj, N);      // between these two calls to std::memcpy, obj might be modified
std::memcpy(&obj, buf, N);      // at this point, each subobject of obj of scalar type holds its original value
```

— *end example*]

For any trivially copyable type `T`, if two pointers to `T` point to
distinct `T` objects `obj1` and `obj2`, where neither `obj1` nor `obj2`
is a base-class subobject, if the underlying bytes ([[intro.memory]])
making up `obj1` are copied into `obj2`,[^19] `obj2` shall subsequently
hold the same value as `obj1`.

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
*N* equals `sizeof(T)`. The *value representation* of an object is the
set of bits that hold the value of type `T`. For trivially copyable
types, the value representation is a set of bits in the object
representation that determines a *value*, which is one discrete element
of an *implementation-defined* set of values.[^20]

A class that has been declared but not defined, an enumeration type in
certain contexts ([[dcl.enum]]), or an array of unknown bound or of
incomplete element type, is an *incompletely-defined object type*. [^21]
Incompletely-defined object types and cv `void` are *incomplete types* (
[[basic.fundamental]]). Objects shall not be defined to have an
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
  xp++;                         // ill-formed: X is incomplete
  arrp++;                       // ill-formed: incomplete type
  arrpp++;                      // OK: sizeof UNKA* is known
}

struct X { int i; };            // now X is a complete type
int  arr[10];                   // now the type of arr is complete

X x;
void bar() {
  xp = &x;                      // OK; type is ``pointer to X''
  arrp = &arr;                  // ill-formed: different types
  xp++;                         // OK:  X is complete
  arrp++;                       // ill-formed: UNKA can't be completed
}
```

— *end example*]

[*Note 2*: The rules for declarations and expressions describe in which
contexts incomplete types are prohibited. — *end note*]

An *object type* is a (possibly cv-qualified) type that is not a
function type, not a reference type, and not cv `void`.

Arithmetic types ([[basic.fundamental]]), enumeration types, pointer
types, pointer to member types ([[basic.compound]]), `std::nullptr_t`,
and cv-qualified ([[basic.type.qualifier]]) versions of these types are
collectively called *scalar types*. Scalar types, POD classes (Clause 
[[class]]), arrays of such types and cv-qualified versions of these
types are collectively called *POD types*. Cv-unqualified scalar types,
trivially copyable class types (Clause  [[class]]), arrays of such
types, and cv-qualified versions of these types are collectively called
*trivially copyable types*. Scalar types, trivial class types (Clause 
[[class]]), arrays of such types and cv-qualified versions of these
types are collectively called *trivial types*. Scalar types,
standard-layout class types (Clause  [[class]]), arrays of such types
and cv-qualified versions of these types are collectively called
*standard-layout types*.

A type is a *literal type* if it is:

- possibly cv-qualified `void`; or
- a scalar type; or
- a reference type; or
- an array of literal type; or
- a possibly cv-qualified class type (Clause  [[class]]) that has all of
  the following properties:
  - it has a trivial destructor,
  - it is either a closure type ([[expr.prim.lambda.closure]]), an
    aggregate type ([[dcl.init.aggr]]), or has at least one constexpr
    constructor or constructor template (possibly inherited (
    [[namespace.udecl]]) from a base class) that is not a copy or move
    constructor,
  - if it is a union, at least one of its non-static data members is of
    non-volatile literal type, and
  - if it is not a union, all of its non-static data members and base
    classes are of non-volatile literal types.

[*Note 3*: A literal type is one for which it might be possible to
create an object within a constant expression. It is not a guarantee
that it is possible to create such an object, nor is it a guarantee that
any object of that type will usable in a constant
expression. — *end note*]

Two types *cv1* `T1` and *cv2* `T2` are *layout-compatible* types if
`T1` and `T2` are the same type, layout-compatible enumerations (
[[dcl.enum]]), or layout-compatible standard-layout class types (
[[class.mem]]).

### Fundamental types <a id="basic.fundamental">[[basic.fundamental]]</a>

Objects declared as characters (`char`) shall be large enough to store
any member of the implementation’s basic character set. If a character
from this set is stored in a character object, the integral value of
that character object is equal to the value of the single character
literal form of that character. It is *implementation-defined* whether a
`char` object can hold negative values. Characters can be explicitly
declared `unsigned` or `signed`. Plain `char`, `signed char`, and
`unsigned char` are three distinct types, collectively called *narrow
character types*. A `char`, a `signed char`, and an `unsigned char`
occupy the same amount of storage and have the same alignment
requirements ([[basic.align]]); that is, they have the same object
representation. For narrow character types, all bits of the object
representation participate in the value representation.

[*Note 1*: A bit-field of narrow character type whose length is larger
than the number of bits in the object representation of that type has
padding bits; see  [[class.bit]]. — *end note*]

For unsigned narrow character types, each possible bit pattern of the
value representation represents a distinct number. These requirements do
not hold for other types. In any particular implementation, a plain
`char` object can take on either the same values as a `signed char` or
an `unsigned
char`; which one is *implementation-defined*. For each value *i* of type
`unsigned char` in the range 0 to 255 inclusive, there exists a value
*j* of type `char` such that the result of an integral conversion (
[[conv.integral]]) from *i* to `char` is *j*, and the result of an
integral conversion from *j* to `unsigned char` is *i*.

There are five *standard signed integer types* : “`signed char`”,
“`short int`”, “`int`”, “`long int`”, and “`long long int`”. In this
list, each type provides at least as much storage as those preceding it
in the list. There may also be *implementation-defined* *extended signed
integer types*. The standard and extended signed integer types are
collectively called *signed integer types*. Plain `int`s have the
natural size suggested by the architecture of the execution environment
[^22]; the other signed integer types are provided to meet special
needs.

For each of the standard signed integer types, there exists a
corresponding (but different) *standard unsigned integer type*:
“`unsigned char`”, “`unsigned short int`”, “`unsigned int`”,
“`unsigned long int`”, and “`unsigned long long int`”, each of which
occupies the same amount of storage and has the same alignment
requirements ([[basic.align]]) as the corresponding signed integer
type[^23]; that is, each signed integer type has the same object
representation as its corresponding unsigned integer type. Likewise, for
each of the extended signed integer types there exists a corresponding
*extended unsigned integer type* with the same amount of storage and
alignment requirements. The standard and extended unsigned integer types
are collectively called *unsigned integer types*. The range of
non-negative values of a signed integer type is a subrange of the
corresponding unsigned integer type, the representation of the same
value in each of the two types is the same, and the value representation
of each corresponding signed/unsigned type shall be the same. The
standard signed integer types and standard unsigned integer types are
collectively called the *standard integer types*, and the extended
signed integer types and extended unsigned integer types are
collectively called the *extended integer types*. The signed and
unsigned integer types shall satisfy the constraints given in the C
standard, section 5.2.4.2.1.

Unsigned integers shall obey the laws of arithmetic modulo 2ⁿ where n is
the number of bits in the value representation of that particular size
of integer.[^24]

Type `wchar_t` is a distinct type whose values can represent distinct
codes for all members of the largest extended character set specified
among the supported locales ([[locale]]). Type `wchar_t` shall have the
same size, signedness, and alignment requirements ([[basic.align]]) as
one of the other integral types, called its *underlying type*. Types
`char16_t` and `char32_t` denote distinct types with the same size,
signedness, and alignment as `uint_least16_t` and `uint_least32_t`,
respectively, in `<cstdint>`, called the underlying types.

Values of type `bool` are either `true` or `false`.[^25]

[*Note 2*: There are no `signed`, `unsigned`, `short`, or `long bool`
types or values. — *end note*]

Values of type `bool` participate in integral promotions (
[[conv.prom]]).

Types `bool`, `char`, `char16_t`, `char32_t`, `wchar_t`, and the signed
and unsigned integer types are collectively called *integral*
types.[^26] A synonym for integral type is *integer type*. The
representations of integral types shall define values by use of a pure
binary numeration system.[^27]

[*Example 1*: This International Standard permits two’s complement,
ones’ complement and signed magnitude representations for integral
types. — *end example*]

There are three *floating-point* types: `float`, `double`, and
`long double`. The type `double` provides at least as much precision as
`float`, and the type `long double` provides at least as much precision
as `double`. The set of values of the type `float` is a subset of the
set of values of the type `double`; the set of values of the type
`double` is a subset of the set of values of the type `long double`. The
value representation of floating-point types is
*implementation-defined*.

[*Note 3*: This International Standard imposes no requirements on the
accuracy of floating-point operations; see also 
[[support.limits]]. — *end note*]

Integral and floating types are collectively called *arithmetic* types.
Specializations of the standard library template `std::numeric_limits` (
[[support.limits]]) shall specify the maximum and minimum values of each
arithmetic type for an implementation.

A type cv `void` is an incomplete type that cannot be completed; such a
type has an empty set of values. It is used as the return type for
functions that do not return a value. Any expression can be explicitly
converted to type cv `void` ([[expr.cast]]). An expression of type
cv `void` shall be used only as an expression statement (
[[stmt.expr]]), as an operand of a comma expression ([[expr.comma]]),
as a second or third operand of `?:` ([[expr.cond]]), as the operand of
`typeid`, `noexcept`, or `decltype`, as the expression in a return
statement ([[stmt.return]]) for a function with the return type
cv `void`, or as the operand of an explicit conversion to type
cv `void`.

A value of type `std::nullptr_t` is a null pointer constant (
[[conv.ptr]]). Such values participate in the pointer and the pointer to
member conversions ([[conv.ptr]], [[conv.mem]]).
`sizeof(std::nullptr_t)` shall be equal to `sizeof(void*)`.

[*Note 4*: Even if the implementation defines two or more basic types
to have the same value representation, they are nevertheless different
types. — *end note*]

### Compound types <a id="basic.compound">[[basic.compound]]</a>

Compound types can be constructed in the following ways:

- *arrays* of objects of a given type,  [[dcl.array]];
- *functions*, which have parameters of given types and return `void` or
  references or objects of a given type,  [[dcl.fct]];
- *pointers* to cv `void` or objects or functions (including static
  members of classes) of a given type,  [[dcl.ptr]];
- *references* to objects or functions of a given type,  [[dcl.ref]].
  There are two types of references:
  - *lvalue reference*
  - *rvalue reference*
- *classes* containing a sequence of objects of various types (Clause 
  [[class]]), a set of types, enumerations and functions for
  manipulating these objects ([[class.mfct]]), and a set of
  restrictions on the access to these entities (Clause 
  [[class.access]]);
- *unions*, which are classes capable of containing objects of different
  types at different times,  [[class.union]];
- *enumerations*, which comprise a set of named constant values. Each
  distinct enumeration constitutes a different *enumerated type*, 
  [[dcl.enum]];
- *pointers to non-static class members*, [^28] which identify members
  of a given type within objects of a given class,  [[dcl.mptr]].

These methods of constructing types can be applied recursively;
restrictions are mentioned in  [[dcl.ptr]], [[dcl.array]], [[dcl.fct]],
and  [[dcl.ref]]. Constructing a type such that the number of bytes in
its object representation exceeds the maximum value representable in the
type `std::size_t` ([[support.types]]) is ill-formed.

The type of a pointer to cv `void` or a pointer to an object type is
called an *object pointer type*.

[*Note 1*: A pointer to `void` does not have a pointer-to-object type,
however, because `void` is not an object type. — *end note*]

The type of a pointer that can designate a function is called a
*function pointer type*. A pointer to objects of type `T` is referred to
as a “pointer to `T`”.

[*Example 1*: A pointer to an object of type `int` is referred to as
“pointer to `int`” and a pointer to an object of class `X` is called a
“pointer to `X`”. — *end example*]

Except for pointers to static members, text referring to “pointers” does
not apply to pointers to members. Pointers to incomplete types are
allowed although there are restrictions on what can be done with them (
[[basic.align]]). Every value of pointer type is one of the following:

- a *pointer to* an object or function (the pointer is said to *point*
  to the object or function), or
- a *pointer past the end of* an object ([[expr.add]]), or
- the *null pointer value* ([[conv.ptr]]) for that type, or
- an *invalid pointer value*.

A value of a pointer type that is a pointer to or past the end of an
object *represents the address* of the first byte in memory (
[[intro.memory]]) occupied by the object [^29] or the first byte in
memory after the end of the storage occupied by the object,
respectively.

[*Note 2*: A pointer past the end of an object ([[expr.add]]) is not
considered to point to an unrelated object of the object’s type that
might be located at that address. A pointer value becomes invalid when
the storage it denotes reaches the end of its storage duration; see
[[basic.stc]]. — *end note*]

For purposes of pointer arithmetic ([[expr.add]]) and comparison (
[[expr.rel]], [[expr.eq]]), a pointer past the end of the last element
of an array `x` of n elements is considered to be equivalent to a
pointer to a hypothetical element `x[n]`. The value representation of
pointer types is *implementation-defined*. Pointers to layout-compatible
types shall have the same value representation and alignment
requirements ([[basic.align]]).

[*Note 3*: Pointers to over-aligned types ([[basic.align]]) have no
special representation, but their range of valid values is restricted by
the extended alignment requirement. — *end note*]

Two objects *a* and *b* are *pointer-interconvertible* if:

- they are the same object, or
- one is a standard-layout union object and the other is a non-static
  data member of that object ([[class.union]]), or
- one is a standard-layout class object and the other is the first
  non-static data member of that object, or, if the object has no
  non-static data members, the first base class subobject of that
  object ([[class.mem]]), or
- there exists an object *c* such that *a* and *c* are
  pointer-interconvertible, and *c* and *b* are
  pointer-interconvertible.

If two objects are pointer-interconvertible, then they have the same
address, and it is possible to obtain a pointer to one from a pointer to
the other via a `reinterpret_cast` ([[expr.reinterpret.cast]]).

[*Note 4*: An array object and its first element are not
pointer-interconvertible, even though they have the same
address. — *end note*]

A pointer to cv-qualified ([[basic.type.qualifier]]) or cv-unqualified
`void` can be used to point to objects of unknown type. Such a pointer
shall be able to hold any object pointer. An object of type cv `void*`
shall have the same representation and alignment requirements as
cv `char*`.

### CV-qualifiers <a id="basic.type.qualifier">[[basic.type.qualifier]]</a>

A type mentioned in  [[basic.fundamental]] and  [[basic.compound]] is a
*cv-unqualified type*. Each type which is a cv-unqualified complete or
incomplete object type or is `void` ([[basic.types]]) has three
corresponding cv-qualified versions of its type: a *const-qualified*
version, a *volatile-qualified* version, and a
*const-volatile-qualified* version. The type of an object (
[[intro.object]]) includes the *cv-qualifier*s specified in the
*decl-specifier-seq* ([[dcl.spec]]), *declarator* (Clause 
[[dcl.decl]]), *type-id* ([[dcl.name]]), or *new-type-id* (
[[expr.new]]) when the object is created.

- A *const object* is an object of type `const T` or a non-mutable
  subobject of such an object.
- A *volatile object* is an object of type `volatile T`, a subobject of
  such an object, or a mutable subobject of a const volatile object.
- A *const volatile object* is an object of type `const volatile T`, a
  non-mutable subobject of such an object, a const subobject of a
  volatile object, or a non-mutable volatile subobject of a const
  object.

The cv-qualified or cv-unqualified versions of a type are distinct
types; however, they shall have the same representation and alignment
requirements ([[basic.align]]).[^30]

A compound type ([[basic.compound]]) is not cv-qualified by the
cv-qualifiers (if any) of the types from which it is compounded. Any
cv-qualifiers applied to an array type affect the array element type (
[[dcl.array]]).

See  [[dcl.fct]] and  [[class.this]] regarding function types that have
*cv-qualifier*s.

There is a partial ordering on cv-qualifiers, so that a type can be said
to be *more cv-qualified* than another. Table 
[[tab:relations.on.const.and.volatile]] shows the relations that
constitute this ordering.

**Table: Relations on `const` and `volatile`** <a id="tab:relations.on.const.and.volatile">[tab:relations.on.const.and.volatile]</a>

|                 |     |                  |
| --------------- | --- | ---------------- |
| no cv-qualifier | <   | `const`          |
| no cv-qualifier | <   | `volatile`       |
| no cv-qualifier | <   | `const volatile` |
| `const`         | <   | `const volatile` |
| `volatile`      | <   | `const volatile` |


In this International Standard, the notation cv (or *cv1*, *cv2*, etc.),
used in the description of types, represents an arbitrary set of
cv-qualifiers, i.e., one of {`const`}, {`volatile`}, {`const`,
`volatile`}, or the empty set. For a type cv `T`, the *top-level
cv-qualifiers* of that type are those denoted by cv.

[*Example 1*: The type corresponding to the *type-id* `const int&` has
no top-level cv-qualifiers. The type corresponding to the *type-id*
`volatile int * const` has the top-level cv-qualifier `const`. For a
class type `C`, the type corresponding to the *type-id*
`void (C::* volatile)(int) const` has the top-level cv-qualifier
`volatile`. — *end example*]

Cv-qualifiers applied to an array type attach to the underlying element
type, so the notation “cv `T`”, where `T` is an array type, refers to an
array whose elements are so-qualified. An array type whose elements are
cv-qualified is also considered to have the same cv-qualifications as
its elements.

[*Example 2*:

``` cpp
typedef char CA[5];
typedef const char CC;
CC arr1[5] = { 0 };
const CA arr2 = { 0 };
```

The type of both `arr1` and `arr2` is “array of 5 `const char`”, and the
array type is considered to be const-qualified.

— *end example*]

## Lvalues and rvalues <a id="basic.lval">[[basic.lval]]</a>

Expressions are categorized according to the taxonomy in Figure 
[[fig:categories]].

<a id="fig:categories"></a>

![Expression category taxonomy \[fig:categories\]](images/valuecategories.svg)

- A *glvalue* is an expression whose evaluation determines the identity
  of an object, bit-field, or function.
- A *prvalue* is an expression whose evaluation initializes an object or
  a bit-field, or computes the value of the operand of an operator, as
  specified by the context in which it appears.
- An *xvalue* is a glvalue that denotes an object or bit-field whose
  resources can be reused (usually because it is near the end of its
  lifetime). \[*Example 1*: Certain kinds of expressions involving
  rvalue references ([[dcl.ref]]) yield xvalues, such as a call to a
  function whose return type is an rvalue reference or a cast to an
  rvalue reference type. — *end example*]
- An *lvalue* is a glvalue that is not an xvalue.
- An *rvalue* is a prvalue or an xvalue.

[*Note 1*: Historically, lvalues and rvalues were so-called because
they could appear on the left- and right-hand side of an assignment
(although this is no longer generally true); glvalues are “generalized”
lvalues, prvalues are “pure” rvalues, and xvalues are “eXpiring”
lvalues. Despite their names, these terms classify expressions, not
values. — *end note*]

Every expression belongs to exactly one of the fundamental
classifications in this taxonomy: lvalue, xvalue, or prvalue. This
property of an expression is called its *value category*.

[*Note 2*: The discussion of each built-in operator in Clause  [[expr]]
indicates the category of the value it yields and the value categories
of the operands it expects. For example, the built-in assignment
operators expect that the left operand is an lvalue and that the right
operand is a prvalue and yield an lvalue as the result. User-defined
operators are functions, and the categories of values they expect and
yield are determined by their parameter and return types. — *end note*]

The *result* of a prvalue is the value that the expression stores into
its context. A prvalue whose result is the value *V* is sometimes said
to have or name the value *V*. The *result object* of a prvalue is the
object initialized by the prvalue; a prvalue that is used to compute the
value of an operand of an operator or that has type cv `void` has no
result object.

[*Note 3*: Except when the prvalue is the operand of a
*decltype-specifier*, a prvalue of class or array type always has a
result object. For a discarded prvalue, a temporary object is
materialized; see Clause  [[expr]]. — *end note*]

The *result* of a glvalue is the entity denoted by the expression.

[*Note 4*: Whenever a glvalue appears in a context where a prvalue is
expected, the glvalue is converted to a prvalue; see  [[conv.lval]],
[[conv.array]], and  [[conv.func]]. An attempt to bind an rvalue
reference to an lvalue is not such a context; see 
[[dcl.init.ref]]. — *end note*]

[*Note 5*: There are no prvalue bit-fields; if a bit-field is converted
to a prvalue ([[conv.lval]]), a prvalue of the type of the bit-field is
created, which might then be promoted ([[conv.prom]]). — *end note*]

[*Note 6*: Whenever a prvalue appears in a context where a glvalue is
expected, the prvalue is converted to an xvalue; see 
[[conv.rval]]. — *end note*]

The discussion of reference initialization in  [[dcl.init.ref]] and of
temporaries in  [[class.temporary]] indicates the behavior of lvalues
and rvalues in other significant contexts.

Unless otherwise indicated ([[expr.call]]), a prvalue shall always have
complete type or the `void` type. A glvalue shall not have type
cv `void`.

[*Note 7*: A glvalue may have complete or incomplete non-`void` type.
Class and array prvalues can have cv-qualified types; other prvalues
always have cv-unqualified types. See Clause  [[expr]]. — *end note*]

An lvalue is *modifiable* unless its type is const-qualified or is a
function type.

[*Note 8*: A program that attempts to modify an object through a
nonmodifiable lvalue expression or through an rvalue expression is
ill-formed ([[expr.ass]], [[expr.post.incr]],
[[expr.pre.incr]]). — *end note*]

If a program attempts to access the stored value of an object through a
glvalue of other than one of the following types the behavior is
undefined:[^31]

- the dynamic type of the object,
- a cv-qualified version of the dynamic type of the object,
- a type similar (as defined in  [[conv.qual]]) to the dynamic type of
  the object,
- a type that is the signed or unsigned type corresponding to the
  dynamic type of the object,
- a type that is the signed or unsigned type corresponding to a
  cv-qualified version of the dynamic type of the object,
- an aggregate or union type that includes one of the aforementioned
  types among its elements or non-static data members (including,
  recursively, an element or non-static data member of a subaggregate or
  contained union),
- a type that is a (possibly cv-qualified) base class type of the
  dynamic type of the object,
- a `char`, `unsigned char`, or `std::byte` type.

## Alignment <a id="basic.align">[[basic.align]]</a>

Object types have *alignment requirements* ([[basic.fundamental]], 
[[basic.compound]]) which place restrictions on the addresses at which
an object of that type may be allocated. An *alignment* is an
*implementation-defined* integer value representing the number of bytes
between successive addresses at which a given object can be allocated.
An object type imposes an alignment requirement on every object of that
type; stricter alignment can be requested using the alignment
specifier ([[dcl.align]]).

A *fundamental alignment* is represented by an alignment less than or
equal to the greatest alignment supported by the implementation in all
contexts, which is equal to `alignof(std::max_align_t)` (
[[support.types]]). The alignment required for a type might be different
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
supported ([[dcl.align]]). A type having an extended alignment
requirement is an *over-aligned type*.

[*Note 1*: Every over-aligned type is or contains a class type to which
extended alignment applies (possibly through a non-static data
member). — *end note*]

A *new-extended alignment* is represented by an alignment greater than
`__STDCPP_DEFAULT_NEW_ALIGNMENT__` ([[cpp.predefined]]).

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
`alignof` expression ([[expr.alignof]]). Furthermore, the narrow
character types ([[basic.fundamental]]) shall have the weakest
alignment requirement.

[*Note 2*: This enables the narrow character types to be used as the
underlying type for an aligned memory area (
[[dcl.align]]). — *end note*]

Comparing alignments is meaningful and provides the obvious results:

- Two alignments are equal when their numeric values are equal.
- Two alignments are different when their numeric values are not equal.
- When an alignment is larger than another it represents a stricter
  alignment.

[*Note 3*: The runtime pointer alignment function ([[ptr.align]]) can
be used to obtain an aligned pointer within a buffer; the
aligned-storage templates in the library ([[meta.trans.other]]) can be
used to obtain aligned storage. — *end note*]

If a request for a specific extended alignment in a specific context is
not supported by an implementation, the program is ill-formed.

<!-- Link reference definitions -->
[bad.alloc]: language.md#bad.alloc
[basic]: #basic
[basic.align]: #basic.align
[basic.compound]: #basic.compound
[basic.def]: #basic.def
[basic.def.odr]: #basic.def.odr
[basic.fundamental]: #basic.fundamental
[basic.funscope]: #basic.funscope
[basic.life]: #basic.life
[basic.link]: #basic.link
[basic.lookup]: #basic.lookup
[basic.lookup.argdep]: #basic.lookup.argdep
[basic.lookup.classref]: #basic.lookup.classref
[basic.lookup.elab]: #basic.lookup.elab
[basic.lookup.qual]: #basic.lookup.qual
[basic.lookup.udir]: #basic.lookup.udir
[basic.lookup.unqual]: #basic.lookup.unqual
[basic.lval]: #basic.lval
[basic.namespace]: dcl.md#basic.namespace
[basic.scope]: #basic.scope
[basic.scope.block]: #basic.scope.block
[basic.scope.class]: #basic.scope.class
[basic.scope.declarative]: #basic.scope.declarative
[basic.scope.enum]: #basic.scope.enum
[basic.scope.hiding]: #basic.scope.hiding
[basic.scope.namespace]: #basic.scope.namespace
[basic.scope.pdecl]: #basic.scope.pdecl
[basic.scope.proto]: #basic.scope.proto
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
[basic.types]: #basic.types
[class]: class.md#class
[class.access]: class.md#class.access
[class.base.init]: special.md#class.base.init
[class.bit]: class.md#class.bit
[class.cdtor]: special.md#class.cdtor
[class.conv.fct]: special.md#class.conv.fct
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.derived]: class.md#class.derived
[class.dtor]: special.md#class.dtor
[class.free]: special.md#class.free
[class.friend]: class.md#class.friend
[class.local]: class.md#class.local
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.mfct.non-static]: class.md#class.mfct.non-static
[class.name]: class.md#class.name
[class.nest]: class.md#class.nest
[class.qual]: #class.qual
[class.static]: class.md#class.static
[class.static.data]: class.md#class.static.data
[class.temporary]: special.md#class.temporary
[class.this]: class.md#class.this
[class.union]: class.md#class.union
[conv]: conv.md#conv
[conv.array]: conv.md#conv.array
[conv.func]: conv.md#conv.func
[conv.integral]: conv.md#conv.integral
[conv.lval]: conv.md#conv.lval
[conv.mem]: conv.md#conv.mem
[conv.prom]: conv.md#conv.prom
[conv.ptr]: conv.md#conv.ptr
[conv.qual]: conv.md#conv.qual
[conv.rval]: conv.md#conv.rval
[cpp.predefined]: cpp.md#cpp.predefined
[cstddef.syn]: language.md#cstddef.syn
[dcl.align]: dcl.md#dcl.align
[dcl.array]: dcl.md#dcl.array
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.decl]: dcl.md#dcl.decl
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init]: dcl.md#dcl.init
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.init.ref]: dcl.md#dcl.init.ref
[dcl.inline]: dcl.md#dcl.inline
[dcl.link]: dcl.md#dcl.link
[dcl.mptr]: dcl.md#dcl.mptr
[dcl.name]: dcl.md#dcl.name
[dcl.ptr]: dcl.md#dcl.ptr
[dcl.ref]: dcl.md#dcl.ref
[dcl.spec]: dcl.md#dcl.spec
[dcl.stc]: dcl.md#dcl.stc
[dcl.type.elab]: dcl.md#dcl.type.elab
[dcl.type.simple]: dcl.md#dcl.type.simple
[dcl.typedef]: dcl.md#dcl.typedef
[depr.static_constexpr]: future.md#depr.static_constexpr
[diff.cpp11.basic]: compatibility.md#diff.cpp11.basic
[except]: except.md#except
[except.handle]: except.md#except.handle
[except.spec]: except.md#except.spec
[except.terminate]: except.md#except.terminate
[except.throw]: except.md#except.throw
[expr]: expr.md#expr
[expr.add]: expr.md#expr.add
[expr.alignof]: expr.md#expr.alignof
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.comma]: expr.md#expr.comma
[expr.cond]: expr.md#expr.cond
[expr.const]: expr.md#expr.const
[expr.delete]: expr.md#expr.delete
[expr.dynamic.cast]: expr.md#expr.dynamic.cast
[expr.eq]: expr.md#expr.eq
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.new]: expr.md#expr.new
[expr.post.incr]: expr.md#expr.post.incr
[expr.pre.incr]: expr.md#expr.pre.incr
[expr.prim]: expr.md#expr.prim
[expr.prim.id]: expr.md#expr.prim.id
[expr.prim.lambda.closure]: expr.md#expr.prim.lambda.closure
[expr.pseudo]: expr.md#expr.pseudo
[expr.ref]: expr.md#expr.ref
[expr.reinterpret.cast]: expr.md#expr.reinterpret.cast
[expr.rel]: expr.md#expr.rel
[expr.sizeof]: expr.md#expr.sizeof
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.type.conv]: expr.md#expr.type.conv
[expr.typeid]: expr.md#expr.typeid
[expr.unary.op]: expr.md#expr.unary.op
[fig:categories]: #fig:categories
[headers]: library.md#headers
[intro.execution]: intro.md#intro.execution
[intro.memory]: intro.md#intro.memory
[intro.multithread]: intro.md#intro.multithread
[intro.object]: intro.md#intro.object
[intro.races]: intro.md#intro.races
[lex]: lex.md#lex
[lex.name]: lex.md#lex.name
[locale]: localization.md#locale
[meta.trans.other]: utilities.md#meta.trans.other
[multibyte.strings]: library.md#multibyte.strings
[namespace.alias]: dcl.md#namespace.alias
[namespace.def]: dcl.md#namespace.def
[namespace.memdef]: dcl.md#namespace.memdef
[namespace.qual]: #namespace.qual
[namespace.udecl]: dcl.md#namespace.udecl
[namespace.udir]: dcl.md#namespace.udir
[new.delete]: language.md#new.delete
[new.delete.array]: language.md#new.delete.array
[new.delete.placement]: language.md#new.delete.placement
[new.delete.single]: language.md#new.delete.single
[new.handler]: language.md#new.handler
[over]: over.md#over
[over.literal]: over.md#over.literal
[over.load]: over.md#over.load
[over.match]: over.md#over.match
[over.oper]: over.md#over.oper
[over.over]: over.md#over.over
[ptr.align]: utilities.md#ptr.align
[replacement.functions]: library.md#replacement.functions
[set.new.handler]: language.md#set.new.handler
[stmt.block]: stmt.md#stmt.block
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.expr]: stmt.md#stmt.expr
[stmt.goto]: stmt.md#stmt.goto
[stmt.if]: stmt.md#stmt.if
[stmt.label]: stmt.md#stmt.label
[stmt.return]: stmt.md#stmt.return
[stmt.select]: stmt.md#stmt.select
[support.dynamic]: language.md#support.dynamic
[support.limits]: language.md#support.limits
[support.runtime]: language.md#support.runtime
[support.start.term]: language.md#support.start.term
[support.types]: language.md#support.types
[tab:relations.on.const.and.volatile]: #tab:relations.on.const.and.volatile
[temp]: temp.md#temp
[temp.class.spec]: temp.md#temp.class.spec
[temp.deduct.guide]: temp.md#temp.deduct.guide
[temp.dep]: temp.md#temp.dep
[temp.expl.spec]: temp.md#temp.expl.spec
[temp.explicit]: temp.md#temp.explicit
[temp.fct]: temp.md#temp.fct
[temp.local]: temp.md#temp.local
[temp.mem.func]: temp.md#temp.mem.func
[temp.names]: temp.md#temp.names
[temp.nondep]: temp.md#temp.nondep
[temp.over]: temp.md#temp.over
[temp.over.link]: temp.md#temp.over.link
[temp.param]: temp.md#temp.param
[temp.point]: temp.md#temp.point
[temp.res]: temp.md#temp.res
[temp.spec]: temp.md#temp.spec
[temp.static]: temp.md#temp.static
[temp.type]: temp.md#temp.type
[thread.threads]: thread.md#thread.threads
[util.dynamic.safety]: utilities.md#util.dynamic.safety

[^1]: Appearing inside the braced-enclosed *declaration-seq* in a
    *linkage-specification* does not affect whether a declaration is a
    definition.

[^2]: An implementation is not required to call allocation and
    deallocation functions from constructors or destructors; however,
    this is a permissible implementation technique.

[^3]:  [[dcl.fct.default]] describes how default argument names are
    looked up.

[^4]: This refers to unqualified names that occur, for instance, in a
    type or default argument in the *parameter-declaration-clause* or
    used in the function body.

[^5]: This refers to unqualified names following the class name; such a
    name may be used in the *base-clause* or may be used in the class
    definition.

[^6]: This lookup applies whether the definition of `X` is nested within
    `Y`’s definition or whether `X`’s definition appears in a namespace
    scope enclosing `Y`’s definition ([[class.nest]]).

[^7]: That is, an unqualified name that occurs, for instance, in a type
    in the *parameter-declaration-clause* or in the
    *noexcept-specifier*.

[^8]: This lookup applies whether the member function is defined within
    the definition of class `X` or whether the member function is
    defined in a namespace scope enclosing `X`’s definition.

[^9]: Lookups in which function names are ignored include names
    appearing in a *nested-name-specifier*, an
    *elaborated-type-specifier*, or a *base-specifier*.

[^10]: A class template has the linkage of the innermost enclosing class
    or namespace in which it is declared.

[^11]: A non-local variable with static storage duration having
    initialization with side effects is initialized in this case, even
    if it is not itself odr-used ([[basic.def.odr]], 
    [[basic.stc.static]]).

[^12]: Some implementations might define that copying an invalid pointer
    value causes a system-generated runtime fault.

[^13]: The intent is to have `operator new()` implementable by calling
    `std::malloc()` or `std::calloc()`, so the rules are substantially
    the same. C++differs from C in requiring a zero request to return a
    non-null pointer.

[^14]: The global `operator delete(void*, std::size_t)` precludes use of
    an allocation function `void operator new(std::size_t, std::size_t)`
    as a placement allocation function ([[diff.cpp11.basic]]).

[^15]: This section does not impose restrictions on indirection through
    pointers to memory not allocated by `::operator new`. This maintains
    the ability of many C++implementations to use binary libraries and
    components written in other languages. In particular, this applies
    to C binaries, because indirection through pointers to memory
    allocated by `std::malloc` is not restricted.

[^16]: For example, before the construction of a global object of
    non-POD class type ([[class.cdtor]]).

[^17]: That is, an object for which a destructor will be called
    implicitly—upon exit from the block for an object with automatic
    storage duration, upon exit from the thread for an object with
    thread storage duration, or upon exit from the program for an object
    with static storage duration.

[^18]: By using, for example, the library functions ([[headers]])
    `std::memcpy` or `std::memmove`.

[^19]: By using, for example, the library functions ([[headers]])
    `std::memcpy` or `std::memmove`.

[^20]: The intent is that the memory model of C++is compatible with that
    of ISO/IEC 9899 Programming Language C.

[^21]: The size and layout of an instance of an incompletely-defined
    object type is unknown.

[^22]: `int` must also be large enough to contain any value in the range
    \[`INT_MIN`, `INT_MAX`\], as defined in the header `<climits>`.

[^23]: See  [[dcl.type.simple]] regarding the correspondence between
    types and the sequences of *type-specifier*s that designate them.

[^24]: This implies that unsigned arithmetic does not overflow because a
    result that cannot be represented by the resulting unsigned integer
    type is reduced modulo the number that is one greater than the
    largest value that can be represented by the resulting unsigned
    integer type.

[^25]: Using a `bool` value in ways described by this International
    Standard as “undefined”, such as by examining the value of an
    uninitialized automatic object, might cause it to behave as if it is
    neither `true` nor `false`.

[^26]: Therefore, enumerations ([[dcl.enum]]) are not integral;
    however, enumerations can be promoted to integral types as specified
    in  [[conv.prom]].

[^27]: A positional representation for integers that uses the binary
    digits 0 and 1, in which the values represented by successive bits
    are additive, begin with 1, and are multiplied by successive
    integral power of 2, except perhaps for the bit with the highest
    position. (Adapted from the *American National Dictionary for
    Information Processing Systems*.)

[^28]: Static class members are objects or functions, and pointers to
    them are ordinary pointers to objects or functions.

[^29]: For an object that is not within its lifetime, this is the first
    byte in memory that it will occupy or used to occupy.

[^30]: The same representation and alignment requirements are meant to
    imply interchangeability as arguments to functions, return values
    from functions, and non-static data members of unions.

[^31]: The intent of this list is to specify those circumstances in
    which an object may or may not be aliased.
