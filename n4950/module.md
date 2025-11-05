# Modules <a id="module">[[module]]</a>

## Module units and purviews <a id="module.unit">[[module.unit]]</a>

``` bnf
module-declaration:
    [export-keyword] module-keyword module-name [module-partition] [attribute-specifier-seq] ';'
```

``` bnf
module-name:
    [module-name-qualifier] identifier
```

``` bnf
module-partition:
    ':' [module-name-qualifier] identifier
```

``` bnf
module-name-qualifier:
    identifier '.'
    module-name-qualifier identifier '.'
```

A *module unit* is a translation unit that contains a
*module-declaration*. A *named module* is the collection of module units
with the same *module-name*. The identifiers `module` and `import` shall
not appear as *identifier*s in a *module-name* or *module-partition*.
All *module-name*s either beginning with an *identifier* consisting of
`std` followed by zero or more *digit*s or containing a reserved
identifier [[lex.name]] are reserved and shall not be specified in a
*module-declaration*; no diagnostic is required. If any *identifier* in
a reserved *module-name* is a reserved identifier, the module name is
reserved for use by C++ implementations; otherwise it is reserved for
future standardization. The optional *attribute-specifier-seq*
appertains to the *module-declaration*.

A *module interface unit* is a module unit whose *module-declaration*
starts with *export-keyword*; any other module unit is a
*module implementation unit*. A named module shall contain exactly one
module interface unit with no *module-partition*, known as the
*primary module interface unit* of the module; no diagnostic is
required.

A *module partition* is a module unit whose *module-declaration*
contains a *module-partition*. A named module shall not contain multiple
module partitions with the same *module-partition*. All module
partitions of a module that are module interface units shall be directly
or indirectly exported by the primary module interface unit
[[module.import]]. No diagnostic is required for a violation of these
rules.

\[*Note 1*: Module partitions can be imported only by other module units
in the same module. The division of a module into module units is not
visible outside the module. — *end note*\]

\[*Example 1*:

``` cpp
**Translation unit #1**

export module A;
export import :Foo;
export int baz();
```

``` cpp
**Translation unit #2**

export module A:Foo;
import :Internals;
export int foo() { return 2 * (bar() + 1); }
```

``` cpp
**Translation unit #3**

module A:Internals;
int bar();
```

``` cpp
**Translation unit #4**

module A;
import :Internals;
int bar() { return baz() - 10; }
int baz() { return 30; }
```

Module `A` contains four translation units:

- a primary module interface unit,
- a module partition `A:Foo`, which is a module interface unit forming
  part of the interface of module `A`,
- a module partition `A:Internals`, which does not contribute to the
  external interface of module `A`, and
- a module implementation unit providing a definition of `bar` and
  `baz`, which cannot be imported because it does not have a partition
  name.

— *end example*\]

A *module unit purview* is the sequence of *token*s starting at the
*module-declaration* and extending to the end of the translation unit.
The *purview* of a named module `M` is the set of module unit purviews
of `M`’s module units.

The *global module* is the collection of all *global-module-fragment*s
and all translation units that are not module units. Declarations
appearing in such a context are said to be in the *purview* of the
global module.

\[*Note 2*: The global module has no name, no module interface unit, and
is not introduced by any *module-declaration*. — *end note*\]

A *module* is either a named module or the global module. A declaration
is *attached* to a module as follows:

- If the declaration is a non-dependent friend declaration that
  nominates a function with a *declarator-id* that is a *qualified-id*
  or *template-id* or that nominates a class other than with an
  *elaborated-type-specifier* with neither a *nested-name-specifier* nor
  a *simple-template-id*, it is attached to the module to which the
  friend is attached [[basic.link]].
- Otherwise, if the declaration
  - is a *namespace-definition* with external linkage or
  - appears within a *linkage-specification* [[dcl.link]]

  it is attached to the global module.
- Otherwise, the declaration is attached to the module in whose purview
  it appears.

A *module-declaration* that contains neither an *export-keyword* nor a
*module-partition* implicitly imports the primary module interface unit
of the module as if by a *module-import-declaration*.

\[*Example 2*:

``` cpp
**Translation unit #1**

module B:Y;                     // does not implicitly import B
int y();
```

``` cpp
**Translation unit #2**

export module B;
import :Y;                      // OK, does not create interface dependency cycle
int n = y();
```

``` cpp
**Translation unit #3**

module B:X1;                    // does not implicitly import B
int &a = n;                     // error: n not visible here
```

``` cpp
**Translation unit #4**

module B:X2;                    // does not implicitly import B
import B;
int &b = n;                     // OK
```

``` cpp
**Translation unit #5**

module B;                       // implicitly imports B
int &c = n;                     // OK
```

— *end example*\]

## Export declaration <a id="module.interface">[[module.interface]]</a>

``` bnf
export-declaration:
    export name-declaration
    export '{' [declaration-seq] '}'
    export-keyword module-import-declaration
```

An *export-declaration* shall inhabit a namespace scope and appear in
the purview of a module interface unit. An *export-declaration* shall
not appear directly or indirectly within an unnamed namespace or a
*private-module-fragment*. An *export-declaration* has the declarative
effects of its *name-declaration*, *declaration-seq* (if any), or
*module-import-declaration*. The *name-declaration* of an
*export-declaration* shall not declare a partial specialization
[[temp.decls.general]]. The *declaration-seq* of an *export-declaration*
shall not contain an *export-declaration* or
*module-import-declaration*.

\[*Note 1*: An *export-declaration* does not establish a
scope. — *end note*\]

A declaration is *exported* if it is declared within an
*export-declaration* and inhabits a namespace scope or it is

- a *namespace-definition* that contains an exported declaration, or
- a declaration within a header unit [[module.import]] that introduces
  at least one name.

If an exported declaration is not within a header unit, it shall not
declare a name with internal linkage.

\[*Example 1*:

``` cpp
**Source file `"a.h"`**

export int x;
```

``` cpp
**Translation unit #1**

module;
#include "a.h"                  // error: declaration of x is not in the
                                // purview of a module interface unit
export module M;
export namespace {}             // error: namespace has internal linkage
namespace {
  export int a2;                // error: export of name with internal linkage
}
export static int b;            // error: b explicitly declared static
export int f();                 // OK
export namespace N { }          // OK
export using namespace N;       // OK
```

— *end example*\]

If an exported declaration is a *using-declaration* [[namespace.udecl]]
and is not within a header unit, all entities to which all of the
*using-declarator*s ultimately refer (if any) shall have been introduced
with a name having external linkage.

\[*Example 2*:

``` cpp
**Source file `"b.h"`**

int f();
```

``` cpp
**Importable header `"c.h"`**

int g();
```

``` cpp
**Translation unit #1**

export module X;
export int h();
```

``` cpp
**Translation unit #2**

module;
#include "b.h"
export module M;
import "c.h";
import X;
export using ::f, ::g, ::h;     // OK
struct S;
export using ::S;               // error: S has module linkage
namespace N {
  export int h();
  static int h(int);            // #1
}
export using N::h;              // error: #1 has internal linkage
```

— *end example*\]

\[*Note 2*:

These constraints do not apply to type names introduced by `typedef`
declarations and *alias-declaration*s.

— *end note*\]

A redeclaration of an entity X is implicitly exported if X was
introduced by an exported declaration; otherwise it shall not be
exported.

\[*Example 3*:

``` cpp
export module M;
struct S { int n; };
typedef S S;
export typedef S S;             // OK, does not redeclare an entity
export struct S;                // error: exported declaration follows non-exported declaration
```

— *end example*\]

\[*Note 3*: Names introduced by exported declarations have either
external linkage or no linkage; see [[basic.link]]. Namespace-scope
declarations exported by a module can be found by name lookup in any
translation unit importing that module [[basic.lookup]]. Class and
enumeration member names can be found by name lookup in any context in
which a definition of the type is reachable. — *end note*\]

\[*Example 4*:

``` cpp
**Interface unit of `M`**

export module M;
export struct X {
  static void f();
  struct Y { };
};

namespace {
  struct S { };
}
export void f(S);               // OK
struct T { };
export T id(T);                 // OK

export struct A;                // A exported as incomplete

export auto rootFinder(double a) {
  return [=](double x) { return (x + a/x)/2; };
}

export const int n = 5;         // OK, n has external linkage
```

``` cpp
**Implementation unit of `M`**

module M;
struct A {
  int value;
};
```

``` cpp
**Main program**

import M;
int main() {
  X::f();                       // OK, X is exported and definition of X is reachable
  X::Y y;                       // OK, X::Y is exported as a complete type
  auto f = rootFinder(2);       // OK
  return A{45}.value;           // error: A is incomplete
}
```

— *end example*\]

\[*Note 4*:

Declarations in an exported *namespace-definition* or in an exported
*linkage-specification* [[dcl.link]] are exported and subject to the
rules of exported declarations.

— *end note*\]

## Import declaration <a id="module.import">[[module.import]]</a>

``` bnf
module-import-declaration:
    import-keyword module-name [attribute-specifier-seq] ';'
    import-keyword module-partition [attribute-specifier-seq] ';'
    import-keyword header-name [attribute-specifier-seq] ';'
```

A *module-import-declaration* shall inhabit the global namespace scope.
In a module unit, all *module-import-declaration*s and
*export-declaration*s exporting *module-import-declaration*s shall
appear before all other *declaration*s in the *declaration-seq* of the
*translation-unit* and of the *private-module-fragment* (if any). The
optional *attribute-specifier-seq* appertains to the
*module-import-declaration*.

A *module-import-declaration* *imports* a set of translation units
determined as described below.

\[*Note 1*: Namespace-scope declarations exported by the imported
translation units can be found by name lookup [[basic.lookup]] in the
importing translation unit and declarations within the imported
translation units become reachable [[module.reach]] in the importing
translation unit after the import declaration. — *end note*\]

A *module-import-declaration* that specifies a *module-name* `M` imports
all module interface units of `M`.

A *module-import-declaration* that specifies a *module-partition* shall
only appear after the *module-declaration* in a module unit of some
module `M`. Such a declaration imports the so-named module partition of
`M`.

A *module-import-declaration* that specifies a *header-name* `H` imports
a synthesized *header unit*, which is a translation unit formed by
applying phases 1 to 7 of translation [[lex.phases]] to the source file
or header nominated by `H`, which shall not contain a
*module-declaration*.

\[*Note 2*: All declarations within a header unit are implicitly
exported [[module.interface]], and are attached to the global module
[[module.unit]]. — *end note*\]

An *importable header* is a member of an *implementation-defined* set of
headers that includes all importable C++ library headers [[headers]].
`H` shall identify an importable header. Given two such
*module-import-declaration*s:

- if their *header-name*s identify different headers or source files
  [[cpp.include]], they import distinct header units;
- otherwise, if they appear in the same translation unit, they import
  the same header unit;
- otherwise, it is unspecified whether they import the same header unit.
  \[*Note 1*: It is therefore possible that multiple copies exist of
  entities declared with internal linkage in an importable
  header. — *end note*\]

\[*Note 3*: A *module-import-declaration* nominating a *header-name* is
also recognized by the preprocessor, and results in macros defined at
the end of phase 4 of translation of the header unit being made visible
as described in [[cpp.import]]. Any other *module-import-declaration*
does not make macros visible. — *end note*\]

A declaration of a name with internal linkage is permitted within a
header unit despite all declarations being implicitly exported
[[module.interface]].

\[*Note 4*: A definition that appears in multiple translation units
cannot in general refer to such names [[basic.def.odr]]. — *end note*\]

A header unit shall not contain a definition of a non-inline function or
variable whose name has external linkage.

When a *module-import-declaration* imports a translation unit T, it also
imports all translation units imported by exported
*module-import-declaration*s in T; such translation units are said to be
*exported* by T. Additionally, when a *module-import-declaration* in a
module unit of some module M imports another module unit U of M, it also
imports all translation units imported by non-exported
*module-import-declaration*s in the module unit purview of U.

These rules can in turn lead to the importation of yet more translation
units.

\[*Note 5*: Such indirect importation does not make macros available,
because a translation unit is a sequence of tokens in translation phase
7 [[lex.phases]]. Macros can be made available by directly importing
header units as described in [[cpp.import]]. — *end note*\]

A module implementation unit shall not be exported.

\[*Example 1*:

``` cpp
**Translation unit #1**

module M:Part;
```

``` cpp
**Translation unit #2**

export module M;
export import :Part;    // error: exported partition :Part is an implementation unit
```

— *end example*\]

A module implementation unit of a module `M` that is not a module
partition shall not contain a *module-import-declaration* nominating
`M`.

\[*Example 2*:

``` cpp
module M;
import M;               // error: cannot import M in its own unit
```

— *end example*\]

A translation unit has an *interface dependency* on a translation unit
`U` if it contains a declaration (possibly a *module-declaration*) that
imports `U` or if it has an interface dependency on a translation unit
that has an interface dependency on `U`. A translation unit shall not
have an interface dependency on itself.

\[*Example 3*:

``` cpp
**Interface unit of `M1`**

export module M1;
import M2;
```

``` cpp
**Interface unit of `M2`**

export module M2;
import M3;
```

``` cpp
**Interface unit of `M3`**

export module M3;
import M1;              // error: cyclic interface dependency M3 → M1 → M2 → M3
```

— *end example*\]

## Global module fragment <a id="module.global.frag">[[module.global.frag]]</a>

``` bnf
global-module-fragment:
    module-keyword ';' [declaration-seq]
```

\[*Note 1*: Prior to phase 4 of translation, only preprocessing
directives can appear in the *declaration-seq*
[[cpp.pre]]. — *end note*\]

A *global-module-fragment* specifies the contents of the
*global module fragment* for a module unit. The global module fragment
can be used to provide declarations that are attached to the global
module and usable within the module unit.

A declaration D is *decl-reachable* from a declaration S in the same
translation unit if:

- D does not declare a function or function template and S contains an
  *id-expression*, *namespace-name*, *type-name*, *template-name*, or
  *concept-name* naming D, or
- D declares a function or function template that is named by an
  expression [[basic.def.odr]] appearing in S, or
- S contains a dependent call `E` [[temp.dep]] and D is found by any
  name lookup performed for an expression synthesized from `E` by
  replacing each type-dependent argument or operand with a value of a
  placeholder type with no associated namespaces or entities, or
  \[*Note 2*: This includes the lookup for `operator==` performed when
  considering rewriting an `!=` expression, the lookup for `operator<=>`
  performed when considering rewriting a relational comparison, and the
  lookup for `operator!=` when considering whether an `operator==` is a
  rewrite target. — *end note*\]
- S contains an expression that takes the address of an overload set
  [[over.over]] that contains D and for which the target type is
  dependent, or
- there exists a declaration M that is not a *namespace-definition* for
  which M is decl-reachable from S and either
  - D is decl-reachable from M, or
  - D redeclares the entity declared by M or M redeclares the entity
    declared by D, and D neither is a friend declaration nor inhabits a
    block scope, or
  - D declares a namespace N and M is a member of N, or
  - one of M and D declares a class or class template C and the other
    declares a member or friend of C, or
  - one of D and M declares an enumeration E and the other declares an
    enumerator of E, or
  - D declares a function or variable and M is declared in D,
    or
  - one of M and D declares a template and the other declares a partial
    or explicit specialization or an implicit or explicit instantiation
    of that template, or
  - one of M and D declares a class or enumeration type and the other
    introduces a typedef name for linkage purposes for that type.

In this determination, it is unspecified

- whether a reference to an *alias-declaration*, `typedef` declaration,
  *using-declaration*, or *namespace-alias-definition* is replaced by
  the declarations they name prior to this determination,
- whether a *simple-template-id* that does not denote a dependent type
  and whose *template-name* names an alias template is replaced by its
  denoted type prior to this determination,
- whether a *decltype-specifier* that does not denote a dependent type
  is replaced by its denoted type prior to this determination, and
- whether a non-value-dependent constant expression is replaced by the
  result of constant evaluation prior to this determination.

A declaration `D` in a global module fragment of a module unit is
*discarded* if `D` is not decl-reachable from any *declaration* in the
*declaration-seq* of the *translation-unit*.

\[*Note 2*: A discarded declaration is neither reachable nor visible to
name lookup outside the module unit, nor in template instantiations
whose points of instantiation [[temp.point]] are outside the module
unit, even when the instantiation context [[module.context]] includes
the module unit. — *end note*\]

\[*Example 1*:

``` cpp
const int size = 2;
int ary1[size];                 // unspecified whether size is decl-reachable from ary1
constexpr int identity(int x) { return x; }
int ary2[identity(2)];          // unspecified whether identity is decl-reachable from ary2

template<typename> struct S;
template<typename, int> struct S2;
constexpr int g(int);

template<typename T, int N>
S<S2<T, g(N)>> f();             // S, S2, g, and :: are decl-reachable from f

template<int N>
void h() noexcept(g(N) == N);   // g and :: are decl-reachable from h
```

— *end example*\]

\[*Example 2*:

``` cpp
**Source file `"foo.h"`**

namespace N {
  struct X {};
  int d();
  int e();
  inline int f(X, int = d()) { return e(); }
  int g(X);
  int h(X);
}
```

``` cpp
**Module `M` interface**

module;
#include "foo.h"
export module M;
template<typename T> int use_f() {
  N::X x;                       // N::X, N, and :: are decl-reachable from use_f
  return f(x, 123);             // N::f is decl-reachable from use_f,
                                // N::e is indirectly decl-reachable from use_f
                                //   because it is decl-reachable from N::f, and
                                // N::d is decl-reachable from use_f
                                //   because it is decl-reachable from N::f
                                //   even though it is not used in this call
}
template<typename T> int use_g() {
  N::X x;                       // N::X, N, and :: are decl-reachable from use_g
  return g((T(), x));           // N::g is not decl-reachable from use_g
}
template<typename T> int use_h() {
  N::X x;                       // N::X, N, and :: are decl-reachable from use_h
  return h((T(), x));           // N::h is not decl-reachable from use_h, but
                                // N::h is decl-reachable from use_h<int>
}
int k = use_h<int>();
  // use_h<int> is decl-reachable from k, so
  // N::h is decl-reachable from k
```

``` cpp
**Module `M` implementation**

module M;
int a = use_f<int>();           // OK
int b = use_g<int>();           // error: no viable function for call to g;
                                // g is not decl-reachable from purview of
                                // module M's interface, so is discarded
int c = use_h<int>();           // OK
```

— *end example*\]

## Private module fragment <a id="module.private.frag">[[module.private.frag]]</a>

``` bnf
private-module-fragment:
    module-keyword ':' private ';' [declaration-seq]
```

A *private-module-fragment* shall appear only in a primary module
interface unit [[module.unit]]. A module unit with a
*private-module-fragment* shall be the only module unit of its module;
no diagnostic is required.

\[*Note 1*:

A *private-module-fragment* ends the portion of the module interface
unit that can affect the behavior of other translation units. A
*private-module-fragment* allows a module to be represented as a single
translation unit without making all of the contents of the module
reachable to importers. The presence of a *private-module-fragment*
affects:

- the point by which the definition of an inline function or variable is
  required [[dcl.inline]],
- the point by which the definition of an exported function with a
  placeholder return type is required [[dcl.spec.auto]],
- whether a declaration is required not to be an exposure
  [[basic.link]],
- where definitions for inline functions and templates must appear
  [[basic.def.odr]], [[dcl.inline]], [[temp.pre]],
- the instantiation contexts of templates instantiated before it
  [[module.context]], and
- the reachability of declarations within it [[module.reach]].

— *end note*\]

\[*Example 1*:

``` cpp
export module A;
export inline void fn_e();      // error: exported inline function fn_e not defined
                                // before private module fragment
inline void fn_m();             // error: non-exported inline function fn_m not defined
static void fn_s();
export struct X;
export void g(X *x) {
  fn_s();                       // OK, call to static function in same translation unit
}
export X *factory();            // OK

module :private;
struct X {};                    // definition not reachable from importers of A
X *factory() {
  return new X ();
}
void fn_e() {}
void fn_m() {}
void fn_s() {}
```

— *end example*\]

## Instantiation context <a id="module.context">[[module.context]]</a>

The *instantiation context* is a set of points within the program that
determines which declarations are found by argument-dependent name
lookup [[basic.lookup.argdep]] and which are reachable [[module.reach]]
in the context of a particular declaration or template instantiation.

During the implicit definition of a defaulted function
[[special]], [[class.compare.default]], the instantiation context is the
union of the instantiation context from the definition of the class and
the instantiation context of the program construct that resulted in the
implicit definition of the defaulted function.

During the implicit instantiation of a template whose point of
instantiation is specified as that of an enclosing specialization
[[temp.point]], the instantiation context is the union of the
instantiation context of the enclosing specialization and, if the
template is defined in a module interface unit of a module M and the
point of instantiation is not in a module interface unit of M, the point
at the end of the *declaration-seq* of the primary module interface unit
of M (prior to the *private-module-fragment*, if any).

During the implicit instantiation of a template that is implicitly
instantiated because it is referenced from within the implicit
definition of a defaulted function, the instantiation context is the
instantiation context of the defaulted function.

During the instantiation of any other template specialization, the
instantiation context comprises the point of instantiation of the
template.

In any other case, the instantiation context at a point within the
program comprises that point.

\[*Example 1*:

``` cpp
**Translation unit #1**

export module stuff;
export template<typename T, typename U> void foo(T, U u) { auto v = u; }
export template<typename T, typename U> void bar(T, U u) { auto v = *u; }
```

``` cpp
**Translation unit #2**

export module M1;
import "defn.h";        // provides struct X {}
import stuff;
export template<typename T> void f(T t) {
  X x;
  foo(t, x);
}
```

``` cpp
**Translation unit #3**

export module M2;
import "decl.h";        // provides struct X; (not a definition)
import stuff;
export template<typename T> void g(T t) {
  X *x;
  bar(t, x);
}
```

``` cpp
**Translation unit #4**

import M1;
import M2;
void test() {
  f(0);
  g(0);
}
```

The call to `f(0)` is valid; the instantiation context of `foo<int, X>`
comprises

- the point at the end of translation unit \#1,
- the point at the end of translation unit \#2, and
- the point of the call to `f(0)`,

so the definition of `X` is reachable [[module.reach]].

It is unspecified whether the call to `g(0)` is valid: the instantiation
context of `bar<int, X>` comprises

- the point at the end of translation unit \#1,
- the point at the end of translation unit \#3, and
- the point of the call to `g(0)`,

so the definition of `X` need not be reachable, as described in
[[module.reach]].

— *end example*\]

## Reachability <a id="module.reach">[[module.reach]]</a>

A translation unit U is *necessarily reachable* from a point P if U is a
module interface unit on which the translation unit containing P has an
interface dependency, or the translation unit containing P imports U, in
either case prior to P [[module.import]].

\[*Note 1*: While module interface units are reachable even when they
are only transitively imported via a non-exported import declaration,
namespace-scope names from such module interface units are not found by
name lookup [[basic.lookup]]. — *end note*\]

All translation units that are necessarily reachable are *reachable*.
Additional translation units on which the point within the program has
an interface dependency may be considered reachable, but it is
unspecified which are and under what circumstances.

\[*Note 2*: It is advisable to avoid depending on the reachability of
any additional translation units in programs intending to be
portable. — *end note*\]

A declaration D is *reachable from* a point P if

- D appears prior to P in the same translation unit, or
- D is not discarded [[module.global.frag]], appears in a translation
  unit that is reachable from P, and does not appear within a
  *private-module-fragment*.

A declaration is *reachable* if it is reachable from any point in the
instantiation context [[module.context]].

\[*Note 3*: Whether a declaration is exported has no bearing on whether
it is reachable. — *end note*\]

The accumulated properties of all reachable declarations of an entity
within a context determine the behavior of the entity within that
context.

\[*Note 4*:

These reachable semantic properties include type completeness, type
definitions, initializers, default arguments of functions or template
declarations, attributes, names bound, etc. Since default arguments are
evaluated in the context of the call expression, the reachable semantic
properties of the corresponding parameter types apply in that context.

— *end note*\]

\[*Note 5*: Declarations of an entity can be reachable even where they
cannot be found by name lookup. — *end note*\]

\[*Example 1*:

``` cpp
**Translation unit #1**

export module A;
struct X {};
export using Y = X;
```

``` cpp
**Translation unit #2**

import A;
Y y;                // OK, definition of X is reachable
X x;                // error: X not visible to unqualified lookup
```

— *end example*\]

<!-- Section link definitions -->
[module]: #module
[module.context]: #module.context
[module.global.frag]: #module.global.frag
[module.import]: #module.import
[module.interface]: #module.interface
[module.private.frag]: #module.private.frag
[module.reach]: #module.reach
[module.unit]: #module.unit

<!-- Link reference definitions -->
[basic.def.odr]: basic.md#basic.def.odr
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[class.compare.default]: class.md#class.compare.default
[cpp.import]: cpp.md#cpp.import
[cpp.include]: cpp.md#cpp.include
[cpp.pre]: cpp.md#cpp.pre
[dcl.inline]: dcl.md#dcl.inline
[dcl.link]: dcl.md#dcl.link
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[headers]: library.md#headers
[lex.name]: lex.md#lex.name
[lex.phases]: lex.md#lex.phases
[module.context]: #module.context
[module.global.frag]: #module.global.frag
[module.import]: #module.import
[module.interface]: #module.interface
[module.reach]: #module.reach
[module.unit]: #module.unit
[namespace.udecl]: dcl.md#namespace.udecl
[over.over]: over.md#over.over
[special]: class.md#special
[temp.decls.general]: temp.md#temp.decls.general
[temp.dep]: temp.md#temp.dep
[temp.point]: temp.md#temp.point
[temp.pre]: temp.md#temp.pre
