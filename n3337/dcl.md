# Declarations <a id="dcl.dcl">[[dcl.dcl]]</a>

Declarations generally specify how names are to be interpreted.
Declarations have the form

``` bnf
declaration-seq:
    declaration
    declaration-seq declaration
```

``` bnf
declaration:
    block-declaration
    function-definition
    template-declaration
    explicit-instantiation
    explicit-specialization
    linkage-specification
    namespace-definition
    empty-declaration
    attribute-declaration
```

``` bnf
block-declaration:
    simple-declaration
    asm-definition
    namespace-alias-definition
    using-declaration
    using-directive
    static_assert-declaration
    alias-declaration
    opaque-enum-declaration
```

``` bnf
alias-declaration:
    'using' identifier attribute-specifier-seqₒₚₜ = type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seqₒₚₜ init-declarator-listₒₚₜ ';'
    attribute-specifier-seq decl-specifier-seqₒₚₜ init-declarator-list ';'
```

``` bnf
static_assert-declaration:
  'static_assert' '(' constant-expression ',' string-literal ')' ';'
```

``` bnf
empty-declaration:
    ';'
```

``` bnf
attribute-declaration:
    attribute-specifier-seq ';'
```

*asm-definition*s are described in  [[dcl.asm]], and
*linkage-specification*s are described in  [[dcl.link]].
*Function-definition*s are described in  [[dcl.fct.def]] and
*template-declaration*s are described in Clause  [[temp]].
*Namespace-definition*s are described in  [[namespace.def]],
*using-declaration*s are described in  [[namespace.udecl]] and
*using-directive*s are described in  [[namespace.udir]].

The *simple-declaration*

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ init-declarator-listₒₚₜ ';'
```

is divided into three parts. Attributes are described in  [[dcl.attr]].
*decl-specifier*s, the principal components of a *decl-specifier-seq*,
are described in  [[dcl.spec]]. *declarator*s, the components of an
*init-declarator-list*, are described in Clause  [[dcl.decl]]. The
*attribute-specifier-seq* in a *simple-declaration* appertains to each
of the entities declared by the *declarator*s of the
*init-declarator-list*. In the declaration for an entity, attributes
appertaining to that entity may appear at the start of the declaration
and after the *declarator-id* for that declaration.

``` cpp
[[noreturn]] void f [[noreturn]] (); // OK
```

Except where otherwise specified, the meaning of an
*attribute-declaration* is *implementation-defined*.

A declaration occurs in a scope ([[basic.scope]]); the scope rules are
summarized in  [[basic.lookup]]. A declaration that declares a function
or defines a class, namespace, template, or function also has one or
more scopes nested within it. These nested scopes, in turn, can have
declarations nested within them. Unless otherwise stated, utterances in
Clause  [[dcl.dcl]] about components in, of, or contained by a
declaration or subcomponent thereof refer only to those components of
the declaration that are *not* nested within scopes nested within the
declaration.

In a *simple-declaration*, the optional *init-declarator-list* can be
omitted only when declaring a class (Clause  [[class]]) or enumeration (
[[dcl.enum]]), that is, when the *decl-specifier-seq* contains either a
*class-specifier*, an *elaborated-type-specifier* with a *class-key* (
[[class.name]]), or an *enum-specifier*. In these cases and whenever a
*class-specifier* or *enum-specifier* is present in the
*decl-specifier-seq*, the identifiers in these specifiers are among the
names being declared by the declaration (as *class-names*, *enum-names*,
or *enumerators*, depending on the syntax). In such cases, and except
for the declaration of an unnamed bit-field ([[class.bit]]), the
*decl-specifier-seq* shall introduce one or more names into the program,
or shall redeclare a name introduced by a previous declaration.

``` cpp
enum { };           // ill-formed
typedef class { };  //  ill-formed
```

In a *static_assert-declaration* the *constant-expression* shall be a
constant expression ([[expr.const]]) that can be contextually converted
to `bool` (Clause  [[conv]]). If the value of the expression when so
converted is `true`, the declaration has no effect. Otherwise, the
program is ill-formed, and the resulting diagnostic message (
[[intro.compliance]]) shall include the text of the *string-literal*,
except that characters not in the basic source character set (
[[lex.charset]]) are not required to appear in the diagnostic message.

``` cpp
static_assert(sizeof(long) >= 8, "64-bit code generation required for this library.");
```

An *empty-declaration* has no effect.

Each *init-declarator* in the *init-declarator-list* contains exactly
one *declarator-id*, which is the name declared by that
*init-declarator* and hence one of the names declared by the
declaration. The *type-specifiers* ([[dcl.type]]) in the
*decl-specifier-seq* and the recursive *declarator* structure of the
*init-declarator* describe a type ([[dcl.meaning]]), which is then
associated with the name being declared by the *init-declarator*.

If the *decl-specifier-seq* contains the `typedef` specifier, the
declaration is called a *typedef declaration* and the name of each
*init-declarator* is declared to be a *typedef-name*, synonymous with
its associated type ([[dcl.typedef]]). If the *decl-specifier-seq*
contains no `typedef` specifier, the declaration is called a *function
declaration* if the type associated with the name is a function type (
[[dcl.fct]]) and an *object declaration* otherwise.

Syntactic components beyond those found in the general form of
declaration are added to a function declaration to make a
*function-definition*. An object declaration, however, is also a
definition unless it contains the `extern` specifier and has no
initializer ([[basic.def]]). A definition causes the appropriate amount
of storage to be reserved and any appropriate initialization (
[[dcl.init]]) to be done.

Only in function declarations for constructors, destructors, and type
conversions can the *decl-specifier-seq* be omitted.[^1]

## Specifiers <a id="dcl.spec">[[dcl.spec]]</a>

The specifiers that can be used in a declaration are

``` bnf
decl-specifier:
    storage-class-specifier
    type-specifier
    function-specifier
    'friend'
    'typedef'
    'constexpr'
```

``` bnf
decl-specifier-seq:
    decl-specifier attribute-specifier-seqₒₚₜ 
    decl-specifier decl-specifier-seq
```

The optional *attribute-specifier-seq* in a *decl-specifier-seq*
appertains to the type determined by the preceding *decl-specifier*s (
[[dcl.meaning]]). The *attribute-specifier-seq* affects the type only
for the declaration it appears in, not other declarations involving the
same type.

If a *type-name* is encountered while parsing a *decl-specifier-seq*, it
is interpreted as part of the *decl-specifier-seq* if and only if there
is no previous *type-specifier* other than a *cv-qualifier* in the
*decl-specifier-seq*. The sequence shall be self-consistent as described
below.

``` cpp
typedef char* Pc;
static Pc;                      // error: name missing
```

Here, the declaration `static` `Pc` is ill-formed because no name was
specified for the static variable of type `Pc`. To get a variable called
`Pc`, a *type-specifier* (other than `const` or `volatile`) has to be
present to indicate that the *typedef-name* `Pc` is the name being
(re)declared, rather than being part of the *decl-specifier* sequence.
For another example,

``` cpp
void f(const Pc);               // void f(char* const) (not const char*)
void g(const int Pc);           // void g(const int)
```

Since `signed`, `unsigned`, `long`, and `short` by default imply `int`,
a *type-name* appearing after one of those specifiers is treated as the
name being (re)declared.

``` cpp
void h(unsigned Pc);            // void h(unsigned int)
void k(unsigned int Pc);        // void k(unsigned int)
```

### Storage class specifiers <a id="dcl.stc">[[dcl.stc]]</a>

The storage class specifiers are

``` bnf
storage-class-specifier:
    'register'
    'static'
    'thread_local'
    'extern'
    'mutable'
```

At most one *storage-class-specifier* shall appear in a given
*decl-specifier-seq*, except that `thread_local` may appear with
`static` or `extern`. If `thread_local` appears in any declaration of a
variable it shall be present in all declarations of that entity. If a
*storage-class-specifier* appears in a *decl-specifier-seq*, there can
be no `typedef` specifier in the same *decl-specifier-seq* and the
*init-declarator-list* of the declaration shall not be empty (except for
an anonymous union declared in a named namespace or in the global
namespace, which shall be declared `static` ([[class.union]])). The
*storage-class-specifier* applies to the name declared by each
*init-declarator* in the list and not to any names declared by other
specifiers. A *storage-class-specifier* shall not be specified in an
explicit specialization ([[temp.expl.spec]]) or an explicit
instantiation ([[temp.explicit]]) directive.

The `register` specifier shall be applied only to names of variables
declared in a block ([[stmt.block]]) or to function parameters (
[[dcl.fct.def]]). It specifies that the named variable has automatic
storage duration ([[basic.stc.auto]]). A variable declared without a
*storage-class-specifier* at block scope or declared as a function
parameter has automatic storage duration by default.

A `register` specifier is a hint to the implementation that the variable
so declared will be heavily used. The hint can be ignored and in most
implementations it will be ignored if the address of the variable is
taken. This use is deprecated (see  [[depr.register]]).

The `thread_local` specifier indicates that the named entity has thread
storage duration ([[basic.stc.thread]]). It shall be applied only to
the names of variables of namespace or block scope and to the names of
static data members. When `thread_local` is applied to a variable of
block scope the *storage-class-specifier* `static` is implied if it does
not appear explicitly.

The `static` specifier can be applied only to names of variables and
functions and to anonymous unions ([[class.union]]). There can be no
`static` function declarations within a block, nor any `static` function
parameters. A `static` specifier used in the declaration of a variable
declares the variable to have static storage duration (
[[basic.stc.static]]), unless accompanied by the `thread_local`
specifier, which declares the variable to have thread storage duration (
[[basic.stc.thread]]). A `static` specifier can be used in declarations
of class members;  [[class.static]] describes its effect. For the
linkage of a name declared with a `static` specifier, see 
[[basic.link]].

The `extern` specifier can be applied only to the names of variables and
functions. The `extern` specifier cannot be used in the declaration of
class members or function parameters. For the linkage of a name declared
with an `extern` specifier, see  [[basic.link]]. The `extern` keyword
can also be used in s and s, but it is not a in such contexts.

A name declared in a namespace scope without a *storage-class-specifier*
has external linkage unless it has internal linkage because of a
previous declaration and provided it is not declared `const`. Objects
declared `const` and not explicitly declared `extern` have internal
linkage.

The linkages implied by successive declarations for a given entity shall
agree. That is, within a given scope, each declaration declaring the
same variable name or the same overloading of a function name shall
imply the same linkage. Each function in a given set of overloaded
functions can have a different linkage, however.

``` cpp
static char* f();               // f() has internal linkage
char* f()                       // f() still has internal linkage
  { /* ... */ }

char* g();                      // g() has external linkage
static char* g()                // error: inconsistent linkage
  { /* ... */ }

void h();
inline void h();                // external linkage

inline void l();
void l();                       // external linkage

inline void m();
extern void m();                // external linkage

static void n();
inline void n();                // internal linkage

static int a;                   // a has internal linkage
int a;                          // error: two definitions

static int b;                   // b has internal linkage
extern int b;                   // b still has internal linkage

int c;                          // c has external linkage
static int c;                   // error: inconsistent linkage

extern int d;                   // d has external linkage
static int d;                   // error: inconsistent linkage
```

The name of a declared but undefined class can be used in an `extern`
declaration. Such a declaration can only be used in ways that do not
require a complete class type.

``` cpp
struct S;
extern S a;
extern S f();
extern void g(S);

void h() {
  g(a);                         // error: S is incomplete
  f();                          // error: S is incomplete
}
```

The `mutable` specifier can be applied only to names of class data
members ([[class.mem]]) and cannot be applied to names declared `const`
or `static`, and cannot be applied to reference members.

``` cpp
class X {
  mutable const int* p;         // OK
  mutable int* const q;         // ill-formed
};
```

The `mutable` specifier on a class data member nullifies a `const`
specifier applied to the containing class object and permits
modification of the mutable class member even though the rest of the
object is `const` ([[dcl.type.cv]]).

### Function specifiers <a id="dcl.fct.spec">[[dcl.fct.spec]]</a>

can be used only in function declarations.

``` bnf
function-specifier:
    'inline'
    'virtual'
    'explicit'
```

A function declaration ([[dcl.fct]],  [[class.mfct]], [[class.friend]])
with an `inline` specifier declares an *inline function*. The inline
specifier indicates to the implementation that inline substitution of
the function body at the point of call is to be preferred to the usual
function call mechanism. An implementation is not required to perform
this inline substitution at the point of call; however, even if this
inline substitution is omitted, the other rules for inline functions
defined by  [[dcl.fct.spec]] shall still be respected.

A function defined within a class definition is an inline function. The
`inline` specifier shall not appear on a block scope function
declaration.[^2] If the `inline` specifier is used in a friend
declaration, that declaration shall be a definition or the function
shall have previously been declared inline.

An inline function shall be defined in every translation unit in which
it is odr-used and shall have exactly the same definition in every
case ([[basic.def.odr]]). A call to the inline function may be
encountered before its definition appears in the translation unit. If
the definition of a function appears in a translation unit before its
first declaration as inline, the program is ill-formed. If a function
with external linkage is declared inline in one translation unit, it
shall be declared inline in all translation units in which it appears;
no diagnostic is required. An `inline` function with external linkage
shall have the same address in all translation units. A `static` local
variable in an `extern` `inline` function always refers to the same
object. A string literal in the body of an `extern` `inline` function is
the same object in different translation units. A string literal
appearing in a default argument is not in the body of an inline function
merely because the expression is used in a function call from that
inline function. A type defined within the body of an `extern inline`
function is the same type in every translation unit.

The `virtual` specifier shall be used only in the initial declaration of
a non-static class member function; see  [[class.virtual]].

The `explicit` specifier shall be used only in the declaration of a
constructor or conversion function within its class definition; see 
[[class.conv.ctor]] and  [[class.conv.fct]].

### The `typedef` specifier <a id="dcl.typedef">[[dcl.typedef]]</a>

Declarations containing the *decl-specifier* `typedef` declare
identifiers that can be used later for naming fundamental (
[[basic.fundamental]]) or compound ([[basic.compound]]) types. The
`typedef` specifier shall not be combined in a *decl-specifier-seq* with
any other kind of specifier except a *type-specifier,* and it shall not
be used in the *decl-specifier-seq* of a *parameter-declaration* (
[[dcl.fct]]) nor in the *decl-specifier-seq* of a
*function-definition* ([[dcl.fct.def]]).

``` bnf
typedef-name:
    identifier
```

A name declared with the `typedef` specifier becomes a *typedef-name*.
Within the scope of its declaration, a *typedef-name* is syntactically
equivalent to a keyword and names the type associated with the
identifier in the way described in Clause  [[dcl.decl]]. A
*typedef-name* is thus a synonym for another type. A *typedef-name* does
not introduce a new type the way a class declaration ([[class.name]])
or enum declaration does. after

``` cpp
typedef int MILES, *KLICKSP;
```

the constructions

``` cpp
MILES distance;
extern KLICKSP metricp;
```

are all correct declarations; the type of `distance` is `int` and that
of `metricp` is “pointer to `int`.”

A *typedef-name* can also be introduced by an *alias-declaration*. The
*identifier* following the `using` keyword becomes a *typedef-name* and
the optional *attribute-specifier-seq* following the *identifier*
appertains to that *typedef-name*. It has the same semantics as if it
were introduced by the `typedef` specifier. In particular, it does not
define a new type and it shall not appear in the *type-id*.

``` cpp
using handler_t = void (*)(int);
extern handler_t ignore;
extern void (*ignore)(int);         // redeclare ignore
using cell = pair<void*, cell*>;    // ill-formed
```

In a given non-class scope, a `typedef` specifier can be used to
redefine the name of any type declared in that scope to refer to the
type to which it already refers.

``` cpp
typedef struct s { /* ... */ } s;
typedef int I;
typedef int I;
typedef I I;
```

In a given class scope, a `typedef` specifier can be used to redefine
any *class-name* declared in that scope that is not also a
*typedef-name* to refer to the type to which it already refers.

``` cpp
struct S {
  typedef struct A { } A;       // OK
  typedef struct B B;           // OK
  typedef A A;                  // error
};
```

If a `typedef` specifier is used to redefine in a given scope an entity
that can be referenced using an *elaborated-type-specifier*, the entity
can continue to be referenced by an *elaborated-type-specifier* or as an
enumeration or class name in an enumeration or class definition
respectively.

``` cpp
struct S;
typedef struct S S;
int main() {
  struct S* p;                  // OK
}
struct S { };                   // OK
```

In a given scope, a `typedef` specifier shall not be used to redefine
the name of any type declared in that scope to refer to a different
type.

``` cpp
class complex { /* ... */ };
typedef int complex;            // error: redefinition
```

Similarly, in a given scope, a class or enumeration shall not be
declared with the same name as a *typedef-name* that is declared in that
scope and refers to a type other than the class or enumeration itself.

``` cpp
typedef int complex;
class complex { /* ... */ };   // error: redefinition
```

A *typedef-name* that names a class type, or a cv-qualified version
thereof, is also a *class-name* ([[class.name]]). If a *typedef-name*
is used to identify the subject of an *elaborated-type-specifier* (
[[dcl.type.elab]]), a class definition (Clause  [[class]]), a
constructor declaration ([[class.ctor]]), or a destructor declaration (
[[class.dtor]]), the program is ill-formed.

``` cpp
struct S {
  S();
  ~S();
};

typedef struct S T;

S a = T();                      // OK
struct T * p;                   // error
```

If the typedef declaration defines an unnamed class (or enum), the first
*typedef-name* declared by the declaration to be that class type (or
enum type) is used to denote the class type (or enum type) for linkage
purposes only ([[basic.link]]).

``` cpp
typedef struct { } *ps, S;      // S is the class name for linkage purposes
```

### The `friend` specifier <a id="dcl.friend">[[dcl.friend]]</a>

The `friend` specifier is used to specify access to class members; see 
[[class.friend]].

### The `constexpr` specifier <a id="dcl.constexpr">[[dcl.constexpr]]</a>

The `constexpr` specifier shall be applied only to the definition of a
variable, the declaration of a function or function template, or the
declaration of a static data member of a literal type (
[[basic.types]]). If any declaration of a function or function template
has `constexpr` specifier, then all its declarations shall contain the
`constexpr` specifier. An explicit specialization can differ from the
template declaration with respect to the `constexpr` specifier. Function
parameters cannot be declared `constexpr`.

``` cpp
constexpr int square(int x);    // OK: declaration
constexpr int bufsz = 1024;     // OK: definition
constexpr struct pixel {        // error: pixel is a type
  int x;
  int y;
  constexpr pixel(int);         // OK: declaration
};
constexpr pixel::pixel(int a)
  : x(square(a)), y(square(a))  // OK: definition
  { }
constexpr pixel small(2);       // error: square not defined, so small(2)
                                // not constant~([expr.const]) so constexpr not satisfied

constexpr int square(int x) {   // OK: definition
  return x * x;
}
constexpr pixel large(4);       // OK: square defined
int next(constexpr int x) {     // error: not for parameters
     return x + 1;
}
extern constexpr int memsz;     // error: not a definition
```

A `constexpr` specifier used in the declaration of a function that is
not a constructor declares that function to be a *constexpr function*.
Similarly, a `constexpr` specifier used in a constructor declaration
declares that constructor to be a *constexpr constructor*. `constexpr`
functions and `constexpr` constructors are implicitly `inline` (
[[dcl.fct.spec]]).

The definition of a `constexpr` function shall satisfy the following
constraints:

- it shall not be virtual ([[class.virtual]]);
- its return type shall be a literal type;
- each of its parameter types shall be a literal type;
- its *function-body* shall be `= delete`, `= default`, or a
  *compound-statement* that contains only
  - null statements,

  - 

  - `typedef` declarations and *alias-declaration*s that do not define
    classes or enumerations,

  - *using-declaration*s,

  - *using-directive*s,

  - and exactly one return statement;
- every constructor call and implicit conversion used in initializing
  the return value ([[stmt.return]],  [[dcl.init]]) shall be one of
  those allowed in a constant expression ([[expr.const]]).

``` cpp
constexpr int square(int x)
  { return x * x; }             // OK
constexpr long long_max()
  { return 2147483647; }        // OK
constexpr int abs(int x)
  { return x < 0 ? -x : x; }    // OK
constexpr void f(int x)         // error: return type is void
  { /* ... */ }
constexpr int prev(int x)
  { return --x; }               // error: use of decrement
constexpr int g(int x, int n) { // error: body not just ``return expr''
  int r = 1;
  while (--n > 0) r *= x;
  return r;
}
```

In a definition of a `constexpr` constructor, each of the parameter
types shall be a literal type. In addition, either its *function-body*
shall be `= delete` or `= default` or it shall satisfy the following
constraints:

- the class shall not have any virtual base classes;
- its *function-body* shall not be a *function-try-block*;
- the *compound-statement* of its *function-body* shall contain only
  - null statements,

  - 

  - `typedef` declarations and *alias-declaration*s that do not define
    classes or enumerations,

  - *using-declaration*s,

  - and *using-directive*s;
- every non-static data member and base class sub-object shall be
  initialized ([[class.base.init]]);
- every constructor involved in initializing non-static data members and
  base class sub-objects shall be a `constexpr` constructor;
- every *assignment-expression* that is an *initializer-clause*
  appearing directly or indirectly within a *brace-or-equal-initializer*
  for a non-static data member that is not named by a
  *mem-initializer-id* shall be a constant expression; and
- every implicit conversion used in converting a constructor argument to
  the corresponding parameter type and converting a full-expression to
  the corresponding member type shall be one of those allowed in a
  constant expression.

``` cpp
struct Length {
  explicit constexpr Length(int i = 0) : val(i) { }
private:
    int val;
};
```

*Function invocation substitution* for a call of a `constexpr` function
or of a `constexpr` constructor means implicitly converting each
argument to the corresponding parameter type as if by
copy-initialization,[^3] substituting that converted expression for each
use of the corresponding parameter in the *function-body*, and, for
`constexpr` functions, implicitly converting the resulting returned
expression or *braced-init-list* to the return type of the function as
if by copy-initialization. Such substitution does not change the
meaning.

``` cpp
constexpr int f(void *) { return 0; }
constexpr int f(...) { return 1; }
constexpr int g1() { return f(0); }         // calls f(void *)
constexpr int g2(int n) { return f(n); }    // calls f(...) even for n == 0
constexpr int g3(int n) { return f(n*0); }  // calls f(...)

namespace N {
  constexpr int c = 5;
  constexpr int h() { return c; }
}
constexpr int c = 0;
constexpr int g4() { return N::h(); }       // value is 5, c is not looked up again after the substitution
```

For a `constexpr` function, if no function argument values exist such
that the function invocation substitution would produce a constant
expression ([[expr.const]]), the program is ill-formed; no diagnostic
required. For a `constexpr` constructor, if no argument values exist
such that after function invocation substitution, every constructor call
and full-expression in the *mem-initializer*s would be a constant
expression (including conversions), the program is ill-formed; no
diagnostic required.

``` cpp
constexpr int f(bool b)
  { return b ? throw 0 : 0; }               // OK
constexpr int f() { throw 0; }              // ill-formed, no diagnostic required

struct B {
  constexpr B(int x) : i(0) { }             // x is unused
  int i;
};

int global;

struct D : B {
  constexpr D() : B(global) { }             // ill-formed, no diagnostic required
                                            // lvalue-to-rvalue conversion on non-constant global
};
```

If the instantiated template specialization of a `constexpr` function
template or member function of a class template would fail to satisfy
the requirements for a `constexpr` function or `constexpr` constructor,
that specialization is not a `constexpr` function or `constexpr`
constructor. If the function is a member function it will still be
`const` as described below. If no specialization of the template would
yield a `constexpr` function or `constexpr` constructor, the program is
ill-formed; no diagnostic required.

A call to a `constexpr` function produces the same result as a call to
an equivalent non-`constexpr` function in all respects except that a
call to a `constexpr` function can appear in a constant expression.

A `constexpr` specifier for a non-static member function that is not a
constructor declares that member function to be `const` (
[[class.mfct.non-static]]). The `constexpr` specifier has no other
effect on the function type. The keyword `const` is ignored if it
appears in the *cv-qualifier-seq* of the function declarator of the
declaration of such a member function. The class of which that function
is a member shall be a literal type ([[basic.types]]).

``` cpp
class debug_flag {
public:
  explicit debug_flag(bool);
  constexpr bool is_on();       // error: debug_flag not
                                // literal type
private:
  bool flag;
};
constexpr int bar(int x, int y) // OK
    { return x + y + x*y; }
// ...
int bar(int x, int y)           // error: redefinition of bar
    { return x * 2 + 3 * y; }
```

A `constexpr` specifier used in an object declaration declares the
object as `const`. Such an object shall have literal type and shall be
initialized. If it is initialized by a constructor call, that call shall
be a constant expression ([[expr.const]]). Otherwise, or if a
`constexpr` specifier is used in a reference declaration, every
full-expression that appears in its initializer shall be a constant
expression. Each implicit conversion used in converting the initializer
expressions and each constructor call used for the initialization shall
be one of those allowed in a constant expression ([[expr.const]]).

``` cpp
struct pixel {
  int x, y;
};
constexpr pixel ur = { 1294, 1024 };// OK
constexpr pixel origin;             // error: initializer missing
```

### Type specifiers <a id="dcl.type">[[dcl.type]]</a>

The type-specifiers are

``` bnf
type-specifier:
    trailing-type-specifier
    class-specifier
    enum-specifier
```

``` bnf
trailing-type-specifier:
  simple-type-specifier
  elaborated-type-specifier
  typename-specifier
  cv-qualifier
```

``` bnf
type-specifier-seq:
    type-specifier attribute-specifier-seqₒₚₜ 
    type-specifier type-specifier-seq
```

``` bnf
trailing-type-specifier-seq:
  trailing-type-specifier attribute-specifier-seqₒₚₜ 
  trailing-type-specifier trailing-type-specifier-seq
```

The optional *attribute-specifier-seq* in a *type-specifier-seq* or a
*trailing-type-specifier-seq* appertains to the type denoted by the
preceding *type-specifier*s ([[dcl.meaning]]). The
*attribute-specifier-seq* affects the type only for the declaration it
appears in, not other declarations involving the same type.

As a general rule, at most one *type-specifier* is allowed in the
complete *decl-specifier-seq* of a *declaration* or in a
*type-specifier-seq* or *trailing-type-specifier-seq*. The only
exceptions to this rule are the following:

- `const` can be combined with any type specifier except itself.
- `volatile` can be combined with any type specifier except itself.
- `signed` or `unsigned` can be combined with `char`, `long`, `short`,
  or `int`.
- `short` or `long` can be combined with `int`.
- `long` can be combined with `double`.
- `long` can be combined with `long`.

At least one *type-specifier* that is not a *cv-qualifier* is required
in a declaration unless it declares a constructor, destructor or
conversion function.[^4] A *type-specifier-seq* shall not define a class
or enumeration unless it appears in the *type-id* of an
*alias-declaration* ([[dcl.typedef]]) that is not the *declaration* of
a *template-declaration*.

*enum-specifier*s, *class-specifier*s, and *typename-specifier*s are
discussed in [[dcl.enum]], [[class]], and [[temp.res]], respectively.
The remaining *type-specifier*s are discussed in the rest of this
section.

#### The *cv-qualifiers* <a id="dcl.type.cv">[[dcl.type.cv]]</a>

There are two *cv-qualifiers*, `const` and `volatile`. If a
*cv-qualifier* appears in a *decl-specifier-seq*, the
*init-declarator-list* of the declaration shall not be empty.
[[basic.type.qualifier]] and [[dcl.fct]] describe how cv-qualifiers
affect object and function types. Redundant cv-qualifications are
ignored. For example, these could be introduced by typedefs.

Declaring a variable `const` can affect its linkage ([[dcl.stc]]) and
its usability in constant expressions ([[expr.const]]). As described
in  [[dcl.init]], the definition of an object or subobject of
const-qualified type must specify an initializer or be subject to
default-initialization.

A pointer or reference to a cv-qualified type need not actually point or
refer to a cv-qualified object, but it is treated as if it does; a
const-qualified access path cannot be used to modify an object even if
the object referenced is a non-const object and can be modified through
some other access path. Cv-qualifiers are supported by the type system
so that they cannot be subverted without casting ([[expr.const.cast]]).

Except that any class member declared `mutable` ([[dcl.stc]]) can be
modified, any attempt to modify a `const` object during its lifetime (
[[basic.life]]) results in undefined behavior.

``` cpp
const int ci = 3;               // cv-qualified (initialized as required)
ci = 4;                         // ill-formed: attempt to modify const

int i = 2;                      // not cv-qualified
const int* cip;                 // pointer to const int
cip = &i;                       // OK: cv-qualified access path to unqualified
*cip = 4;                       // ill-formed: attempt to modify through ptr to const

int* ip;
ip = const_cast<int*>(cip);     // cast needed to convert const int* to int*
*ip = 4;                        // defined: *ip points to i, a non-const object

const int* ciq = new const int (3);     // initialized as required
int* iq = const_cast<int*>(ciq);        // cast required
*iq = 4;                                // undefined: modifies a const object
```

For another example

``` cpp
struct X {
  mutable int i;
  int j;
};
struct Y {
  X x;
  Y();
};

const Y y;
y.x.i++;                        // well-formed: mutable member can be modified
y.x.j++;                        // ill-formed: const-qualified member modified
Y* p = const_cast<Y*>(&y);      // cast away const-ness of y
p->x.i = 99;                    // well-formed: mutable member can be modified
p->x.j = 99;                    // undefined: modifies a const member
```

If an attempt is made to refer to an object defined with a
volatile-qualified type through the use of a glvalue with a
non-volatile-qualified type, the program behavior is undefined.

`volatile` is a hint to the implementation to avoid aggressive
optimization involving the object because the value of the object might
be changed by means undetectable by an implementation. See 
[[intro.execution]] for detailed semantics. In general, the semantics of
`volatile` are intended to be the same in C++as they are in C.

#### Simple type specifiers <a id="dcl.type.simple">[[dcl.type.simple]]</a>

The simple type specifiers are

``` bnf
simple-type-specifier:
    nested-name-specifierₒₚₜ type-name
    nested-name-specifier 'template' simple-template-id
    'char'
    'char16_t'
    'char32_t'
    'wchar_t'
    'bool'
    'short'
    'int'
    'long'
    'signed'
    'unsigned'
    'float'
    'double'
    'void'
    'auto'
    decltype-specifier
```

``` bnf
type-name:
    class-name
    enum-name
    typedef-name
    simple-template-id
```

``` bnf
decltype-specifier:
  'decltype' '(' expression ')'
```

The `auto` specifier is a placeholder for a type to be deduced (
[[dcl.spec.auto]]). The other *simple-type-specifier*s specify either a
previously-declared user-defined type or one of the fundamental types (
[[basic.fundamental]]). Table  [[tab:simple.type.specifiers]] summarizes
the valid combinations of *simple-type-specifier*s and the types they
specify.

**Table: *simple-type-specifier*{s} and the types they specify** <a id="tab:simple.type.specifiers">[tab:simple.type.specifiers]</a>

|                        |                                        |
| ---------------------- | -------------------------------------- |
| *type-name*            | the type named                         |
| *simple-template-id*   | the type as defined in~ [[temp.names]] |
| char                   | ``char''                               |
| unsigned char          | ``unsigned char''                      |
| signed char            | ``signed char''                        |
| char16_t               | ``char16_t''                           |
| char32_t               | ``char32_t''                           |
| bool                   | ``bool''                               |
| unsigned               | ``unsigned int''                       |
| unsigned int           | ``unsigned int''                       |
| signed                 | ``int''                                |
| signed int             | ``int''                                |
| int                    | ``int''                                |
| unsigned short int     | ``unsigned short int''                 |
| unsigned short         | ``unsigned short int''                 |
| unsigned long int      | ``unsigned long int''                  |
| unsigned long          | ``unsigned long int''                  |
| unsigned long long int | ``unsigned long long int''             |
| unsigned long long     | ``unsigned long long int''             |
| signed long int        | ``long int''                           |
| signed long            | ``long int''                           |
| signed long long int   | ``long long int''                      |
| signed long long       | ``long long int''                      |
| long long int          | ``long long int''                      |
| long long              | ``long long int''                      |
| long int               | ``long int''                           |
| long                   | ``long int''                           |
| signed short int       | ``short int''                          |
| signed short           | ``short int''                          |
| short int              | ``short int''                          |
| short                  | ``short int''                          |
| wchar_t                | ``wchar_t''                            |
| float                  | ``float''                              |
| double                 | ``double''                             |
| long double            | ``long double''                        |
| void                   | ``void''                               |
| auto                   | placeholder for a type to be deduced   |
| decltype(*expression*) | the type as defined below              |


When multiple *simple-type-specifiers* are allowed, they can be freely
intermixed with other *decl-specifiers* in any order. It is
implementation-defined whether objects of `char` type and certain
bit-fields ([[class.bit]]) are represented as signed or unsigned
quantities. The `signed` specifier forces `char` objects and bit-fields
to be signed; it is redundant in other contexts.

The type denoted by `decltype(e)` is defined as follows:

- if `e` is an unparenthesized *id-expression* or an unparenthesized
  class member access ([[expr.ref]]), `decltype(e)` is the type of the
  entity named by `e`. If there is no such entity, or if `e` names a set
  of overloaded functions, the program is ill-formed;
- otherwise, if `e` is an xvalue, `decltype(e)` is `T&&`, where `T` is
  the type of `e`;
- otherwise, if `e` is an lvalue, `decltype(e)` is `T&`, where `T` is
  the type of `e`;
- otherwise, `decltype(e)` is the type of `e`.

The operand of the `decltype` specifier is an unevaluated operand
(Clause  [[expr]]).

``` cpp
const int&& foo();
int i;
struct A { double x; };
const A* a = new A();
decltype(foo()) x1 = i;         // type is const int&&
decltype(i) x2;                 // type is int
decltype(a->x) x3;              // type is double
decltype((a->x)) x4 = x3;       // type is const double&
```

in the case where the operand of a *decltype-specifier* is a function
call and the return type of the function is a class type, a special
rule ([[expr.call]]) ensures that the return type is not required to be
complete (as it would be if the call appeared in a sub-expression or
outside of a *decltype-specifier*). In this context, the common purpose
of writing the expression is merely to refer to its type. In that sense,
a *decltype-specifier* is analogous to a use of a *typedef-name*, so the
usual reasons for requiring a complete type do not apply. In particular,
it is not necessary to allocate storage for a temporary object or to
enforce the semantic constraints associated with invoking the type’s
destructor.

``` cpp
template<class T> struct A { ~A() = delete; };
template<class T> auto h()
  -> A<T>;
template<class T> auto i(T)     // identity
  -> T;
template<class T> auto f(T)     // #1
  -> decltype(i(h<T>()));       // forces completion of A<T> and implicitly uses
                                // A<T>::~A() for the temporary introduced by the
                                // use of h(). (A temporary is not introduced
                                // as a result of the use of i().)
template<class T> auto f(T)     // #2
  -> void;
auto g() -> void {
  f(42);                        // OK: calls #2. (#1 is not a viable candidate: type
                                // deduction fails~([temp.deduct]) because A<int>::~{A()}
                                // is implicitly used in its decltype-specifier)
}
template<class T> auto q(T)
  -> decltype((h<T>()));        // does not force completion of A<T>; A<T>::~A() is
                                // not implicitly used within the context of this decltype-specifier
void r() {
  q(42);                        // Error: deduction against q succeeds, so overload resolution
                                // selects the specialization ``q(T) -> decltype((h<T>())) [with T=int]''.
                                // The return type is A<int>, so a temporary is introduced and its
                                // destructor is used, so the program is ill-formed.
}
```

#### Elaborated type specifiers <a id="dcl.type.elab">[[dcl.type.elab]]</a>

``` bnf
elaborated-type-specifier:
    class-key attribute-specifier-seqₒₚₜ nested-name-specifierₒₚₜ identifier
    class-key nested-name-specifierₒₚₜ 'template'ₒₚₜ simple-template-id
    'enum' nested-name-specifierₒₚₜ identifier
```

An *attribute-specifier-seq* shall not appear in an
*elaborated-type-specifier* unless the latter is the sole constituent of
a declaration. If an *elaborated-type-specifier* is the sole constituent
of a declaration, the declaration is ill-formed unless it is an explicit
specialization ([[temp.expl.spec]]), an explicit instantiation (
[[temp.explicit]]) or it has one of the following forms:

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
'friend' class-key '::ₒₚₜ ' identifier ';'
'friend' class-key '::ₒₚₜ ' simple-template-id ';'
'friend' class-key nested-name-specifier identifier ';'
'friend' class-key nested-name-specifier 'templateₒₚₜ ' simple-template-id ';'
```

In the first case, the *attribute-specifier-seq*, if any, appertains to
the class being declared; the attributes in the
*attribute-specifier-seq* are thereafter considered attributes of the
class whenever it is named.

[[basic.lookup.elab]] describes how name lookup proceeds for the
*identifier* in an *elaborated-type-specifier*. If the *identifier*
resolves to a *class-name* or *enum-name*, the
*elaborated-type-specifier* introduces it into the declaration the same
way a *simple-type-specifier* introduces its *type-name*. If the
*identifier* resolves to a *typedef-name* or the *simple-template-id*
resolves to an alias template specialization, the
*elaborated-type-specifier* is ill-formed. This implies that, within a
class template with a template *type-parameter* `T`, the declaration

``` cpp
friend class T;
```

is ill-formed. However, the similar declaration `friend T;` is allowed (
[[class.friend]]).

The *class-key* or `enum` keyword present in the
*elaborated-type-specifier* shall agree in kind with the declaration to
which the name in the *elaborated-type-specifier* refers. This rule also
applies to the form of *elaborated-type-specifier* that declares a
*class-name* or `friend` class since it can be construed as referring to
the definition of the class. Thus, in any *elaborated-type-specifier*,
the `enum` keyword shall be used to refer to an enumeration (
[[dcl.enum]]), the `union` *class-key* shall be used to refer to a union
(Clause  [[class]]), and either the `class` or `struct` *class-key*
shall be used to refer to a class (Clause  [[class]]) declared using the
`class` or `struct` *class-key*.

``` cpp
enum class E { a, b };
enum E x = E::a;                // OK
```

#### `auto` specifier <a id="dcl.spec.auto">[[dcl.spec.auto]]</a>

The `auto` *type-specifier* signifies that the type of a variable being
declared shall be deduced from its initializer or that a function
declarator shall include a *trailing-return-type*.

The `auto` *type-specifier* may appear with a function declarator with a
*trailing-return-type* ([[dcl.fct]]) in any context where such a
declarator is valid.

Otherwise, the type of the variable is deduced from its initializer. The
name of the variable being declared shall not appear in the initializer
expression. This use of `auto` is allowed when declaring variables in a
block ([[stmt.block]]), in namespace scope (
[[basic.scope.namespace]]), and in a  ([[stmt.for]]). `auto` shall
appear as one of the *decl-specifier*s in the *decl-specifier-seq* and
the *decl-specifier-seq* shall be followed by one or more
*init-declarator*s, each of which shall have a non-empty *initializer*.

``` cpp
auto x = 5;                 // OK: x has type int
const auto *v = &x, u = 6;  // OK: v has type const int*, u has type const int
static auto y = 0.0;        // OK: y has type double
auto int r;                 // error: auto is not a storage-class-specifier
```

The `auto` can also be used in declaring a variable in the of a
selection statement ([[stmt.select]]) or an iteration statement (
[[stmt.iter]]), in the in the or of a  ([[expr.new]]), in a
*for-range-declaration*, and in declaring a static data member with a
*brace-or-equal-initializer* that appears within the of a class
definition ([[class.static.data]]).

A program that uses `auto` in a context not explicitly allowed in this
section is ill-formed.

Once the type of a has been determined according to  [[dcl.meaning]],
the type of the declared variable using the is determined from the type
of its initializer using the rules for template argument deduction. Let
`T` be the type that has been determined for a variable identifier `d`.
Obtain `P` from `T` by replacing the occurrences of `auto` with either a
new invented type template parameter `U` or, if the initializer is a
*braced-init-list* ([[dcl.init.list]]), with
`std::initializer_list<U>`. The type deduced for the variable `d` is
then the deduced `A` determined using the rules of template argument
deduction from a function call ([[temp.deduct.call]]), where `P` is a
function template parameter type and the initializer for `d` is the
corresponding argument. If the deduction fails, the declaration is
ill-formed.

``` cpp
auto x1 = { 1, 2 };         // decltype(x1) is std::initializer_list<int>
auto x2 = { 1, 2.0 };       // error: cannot deduce element type
```

If the list of declarators contains more than one declarator, the type
of each declared variable is determined as described above. If the type
deduced for the template parameter `U` is not the same in each
deduction, the program is ill-formed.

``` cpp
const auto &i = expr;
```

The type of `i` is the deduced type of the parameter `u` in the call
`f(expr)` of the following invented function template:

``` cpp
template <class U> void f(const U& u);
```

## Enumeration declarations <a id="dcl.enum">[[dcl.enum]]</a>

An enumeration is a distinct type ([[basic.compound]]) with named
constants. Its name becomes an *enum-name*, within its scope.

``` bnf
enum-name:
    identifier
```

``` bnf
enum-specifier:
    enum-head '{' enumerator-listₒₚₜ '}'
    enum-head '{' enumerator-list ', }'
```

``` bnf
enum-head:
    enum-key attribute-specifier-seqₒₚₜ identifierₒₚₜ enum-baseₒₚₜ 
    enum-key attribute-specifier-seqₒₚₜ nested-name-specifier identifier
\hspace*{ inc}enum-baseₒₚₜ
```

``` bnf
opaque-enum-declaration:
    enum-key attribute-specifier-seqₒₚₜ identifier enum-baseₒₚₜ ';'
```

``` bnf
enum-key:
    'enum'
    'enum class'
    'enum struct'
```

``` bnf
enum-base:
    ':' type-specifier-seq
```

``` bnf
enumerator-list:
    enumerator-definition
    enumerator-list ',' enumerator-definition
```

``` bnf
enumerator-definition:
    enumerator
    enumerator '=' constant-expression
```

``` bnf
enumerator:
    identifier
```

The optional *attribute-specifier-seq* in the *enum-head* and the
*opaque-enum-declaration* appertains to the enumeration; the attributes
in that *attribute-specifier-seq* are thereafter considered attributes
of the enumeration whenever it is named.

The enumeration type declared with an *enum-key* of only `enum` is an
unscoped enumeration, and its *enumerator*s are *unscoped enumerators*.
The *enum-key*s `enum class` and `enum struct` are semantically
equivalent; an enumeration type declared with one of these is a *scoped
enumeration*, and its *enumerator*s are *scoped enumerators*. The
optional *identifier* shall not be omitted in the declaration of a
scoped enumeration. The *type-specifier-seq* of an *enum-base* shall
name an integral type; any cv-qualification is ignored. An
*opaque-enum-declaration* declaring an unscoped enumeration shall not
omit the *enum-base*. The identifiers in an *enumerator-list* are
declared as constants, and can appear wherever constants are required.
An *enumerator-definition* with `=` gives the associated *enumerator*
the value indicated by the *constant-expression*. If the first
*enumerator* has no *initializer*, the value of the corresponding
constant is zero. An *enumerator-definition* without an *initializer*
gives the *enumerator* the value obtained by increasing the value of the
previous *enumerator* by one.

``` cpp
enum { a, b, c=0 };
enum { d, e, f=e+2 };
```

defines `a`, `c`, and `d` to be zero, `b` and `e` to be `1`, and `f` to
be `3`.

An *opaque-enum-declaration* is either a redeclaration of an enumeration
in the current scope or a declaration of a new enumeration. An
enumeration declared by an *opaque-enum-declaration* has fixed
underlying type and is a complete type. The list of enumerators can be
provided in a later redeclaration with an *enum-specifier*. A scoped
enumeration shall not be later redeclared as unscoped or with a
different underlying type. An unscoped enumeration shall not be later
redeclared as scoped and each redeclaration shall include an *enum-base*
specifying the same underlying type as in the original declaration.

If the *enum-key* is followed by a *nested-name-specifier*, the
*enum-specifier* shall refer to an enumeration that was previously
declared directly in the class or namespace to which the
*nested-name-specifier* refers (i.e., neither inherited nor introduced
by a *using-declaration*), and the *enum-specifier* shall appear in a
namespace enclosing the previous declaration.

Each enumeration defines a type that is different from all other types.
Each enumeration also has an underlying type. The underlying type can be
explicitly specified using *enum-base*; if not explicitly specified, the
underlying type of a scoped enumeration type is `int`. In these cases,
the underlying type is said to be *fixed*. Following the closing brace
of an *enum-specifier*, each enumerator has the type of its enumeration.
If the underlying type is fixed, the type of each *enumerator* prior to
the closing brace is the underlying type and the *constant-expression*
in the *enumerator-definition* shall be a converted constant expression
of the underlying type ([[expr.const]]); if the initializing value of
an *enumerator* cannot be represented by the underlying type, the
program is ill-formed. If the underlying type is not fixed, the type of
each enumerator is the type of its initializing value:

- If an initializer is specified for an enumerator, the initializing
  value has the same type as the expression and the
  *constant-expression* shall be an integral constant expression (
  [[expr.const]]).
- If no initializer is specified for the first enumerator, the
  initializing value has an unspecified integral type.
- Otherwise the type of the initializing value is the same as the type
  of the initializing value of the preceding enumerator unless the
  incremented value is not representable in that type, in which case the
  type is an unspecified integral type sufficient to contain the
  incremented value. If no such type exists, the program is ill-formed.

For an enumeration whose underlying type is not fixed, the underlying
type is an integral type that can represent all the enumerator values
defined in the enumeration. If no integral type can represent all the
enumerator values, the enumeration is ill-formed. It is
*implementation-defined* which integral type is used as the underlying
type except that the underlying type shall not be larger than `int`
unless the value of an enumerator cannot fit in an `int` or
`unsigned int`. If the *enumerator-list* is empty, the underlying type
is as if the enumeration had a single enumerator with value 0.

For an enumeration whose underlying type is fixed, the values of the
enumeration are the values of the underlying type. Otherwise, for an
enumeration where eₘin is the smallest enumerator and eₘax is the
largest, the values of the enumeration are the values in the range bₘᵢₙ
to bₘₐₓ, defined as follows: Let K be 1 for a two’s complement
representation and 0 for a one’s complement or sign-magnitude
representation. bₘₐₓ is the smallest value greater than or equal to
max(|eₘᵢₙ| - K, |eₘₐₓ|) and equal to $2^M-1$, where M is a non-negative
integer. bₘᵢₙ is zero if eₘᵢₙ is non-negative and -(bₘₐₓ+K) otherwise.
The size of the smallest bit-field large enough to hold all the values
of the enumeration type is max(M,1) if bₘᵢₙ is zero and M+1 otherwise.
It is possible to define an enumeration that has values not defined by
any of its enumerators. If the *enumerator-list* is empty, the values of
the enumeration are as if the enumeration had a single enumerator with
value 0.[^5]

Two enumeration types are layout-compatible if they have the same
*underlying type*.

The value of an enumerator or an object of an unscoped enumeration type
is converted to an integer by integral promotion ([[conv.prom]]).

``` cpp
enum color { red, yellow, green=20, blue };
  color col = red;
  color* cp = &col;
  if (*cp == blue)              // ...
```

makes `color` a type describing various colors, and then declares `col`
as an object of that type, and `cp` as a pointer to an object of that
type. The possible values of an object of type `color` are `red`,
`yellow`, `green`, `blue`; these values can be converted to the integral
values `0`, `1`, `20`, and `21`. Since enumerations are distinct types,
objects of type `color` can be assigned only values of type `color`.

``` cpp
color c = 1;                    // error: type mismatch,
                                // no conversion from int to color

int i = yellow;                 // OK: yellow converted to integral value 1
                                // integral promotion
```

Note that this implicit `enum` to `int` conversion is not provided for a
scoped enumeration:

``` cpp
enum class Col { red, yellow, green };
int x = Col::red;               // error: no Col to int conversion
Col y = Col::red;
if (y) { }                      // error: no Col to bool conversion
```

Each *enum-name* and each unscoped *enumerator* is declared in the scope
that immediately contains the *enum-specifier*. Each scoped *enumerator*
is declared in the scope of the enumeration. These names obey the scope
rules defined for all names in ([[basic.scope]]) and (
[[basic.lookup]]).

``` cpp
enum direction { left='l', right='r' };

void g()  {
  direction d;                  // OK
  d = left;                     // OK
  d = direction::right;         // OK
}

enum class altitude { high='h', low='l' };

void h()  {
  altitude a;                   // OK
  a = high;                     // error: high not in scope
  a = altitude::low;            // OK
}
```

An enumerator declared in class scope can be referred to using the class
member access operators (`::`, `.` (dot) and `->` (arrow)), see 
[[expr.ref]].

``` cpp
struct X {
  enum direction { left='l', right='r' };
  int f(int i) { return i==left ? 0 : i==right ? 1 : 2; }
};

void g(X* p) {
  direction d;                  // error: direction not in scope
  int i;
  i = p->f(left);               // error: left not in scope
  i = p->f(X::right);           // OK
  i = p->f(p->left);            // OK
  // ...
}
```

## Namespaces <a id="basic.namespace">[[basic.namespace]]</a>

A namespace is an optionally-named declarative region. The name of a
namespace can be used to access entities declared in that namespace;
that is, the members of the namespace. Unlike other declarative regions,
the definition of a namespace can be split over several parts of one or
more translation units.

The outermost declarative region of a translation unit is a namespace;
see  [[basic.scope.namespace]].

### Namespace definition <a id="namespace.def">[[namespace.def]]</a>

The grammar for a *namespace-definition* is

``` bnf
namespace-name:
        original-namespace-name
        namespace-alias
```

``` bnf
original-namespace-name:
        identifier
```

``` bnf
namespace-definition:
        named-namespace-definition
        unnamed-namespace-definition
```

``` bnf
named-namespace-definition:
        original-namespace-definition
        extension-namespace-definition
```

``` bnf
original-namespace-definition:
        'inlineₒₚₜ ' 'namespace' identifier '{' namespace-body '}'
```

``` bnf
extension-namespace-definition:
        'inlineₒₚₜ ' 'namespace' original-namespace-name '{' namespace-body '}'
```

``` bnf
unnamed-namespace-definition:
        'inlineₒₚₜ ' 'namespace {' namespace-body '}'
```

``` bnf
namespace-body:
        declaration-seqₒₚₜ
```

The *identifier* in an *original-namespace-definition* shall not have
been previously defined in the declarative region in which the
*original-namespace-definition* appears. The *identifier* in an
*original-namespace-definition* is the name of the namespace.
Subsequently in that declarative region, it is treated as an
*original-namespace-name*.

The *original-namespace-name* in an *extension-namespace-definition*
shall have previously been defined in an *original-namespace-definition*
in the same declarative region.

Every *namespace-definition* shall appear in the global scope or in a
namespace scope ([[basic.scope.namespace]]).

Because a *namespace-definition* contains *declaration*s in its
*namespace-body* and a *namespace-definition* is itself a *declaration*,
it follows that *namespace-definitions* can be nested.

``` cpp
namespace Outer {
  int i;
  namespace Inner {
    void f() { i++; }           // Outer::i
    int i;
    void g() { i++; }           // Inner::i
  }
}
```

The *enclosing namespaces* of a declaration are those namespaces in
which the declaration lexically appears, except for a redeclaration of a
namespace member outside its original namespace (e.g., a definition as
specified in  [[namespace.memdef]]). Such a redeclaration has the same
enclosing namespaces as the original declaration.

``` cpp
namespace Q {
  namespace V {
    void f();   // enclosing namespaces are the global namespace, Q, and Q::V
    class C { void m(); };
  }
  void V::f() { // enclosing namespaces are the global namespace, Q, and Q::V
    extern void h();  // ... so this declares Q::V::h
  }
  void V::C::m() { // enclosing namespaces are the global namespace, Q, and Q::V
  }
}
```

If the optional initial `inline` keyword appears in a
*namespace-definition* for a particular namespace, that namespace is
declared to be an *inline namespace*. The `inline` keyword may be used
on an *extension-namespace-definition* only if it was previously used on
the *original-namespace-definition* for that namespace.

Members of an inline namespace can be used in most respects as though
they were members of the enclosing namespace. Specifically, the inline
namespace and its enclosing namespace are both added to the set of
associated namespaces used in argument-dependent lookup (
[[basic.lookup.argdep]]) whenever one of them is, and a
*using-directive* ([[namespace.udir]]) that names the inline namespace
is implicitly inserted into the enclosing namespace as for an unnamed
namespace ([[namespace.unnamed]]). Furthermore, each member of the
inline namespace can subsequently be explicitly instantiated (
[[temp.explicit]]) or explicitly specialized ([[temp.expl.spec]]) as
though it were a member of the enclosing namespace. Finally, looking up
a name in the enclosing namespace via explicit qualification (
[[namespace.qual]]) will include members of the inline namespace brought
in by the *using-directive* even if there are declarations of that name
in the enclosing namespace.

These properties are transitive: if a namespace `N` contains an inline
namespace `M`, which in turn contains an inline namespace `O`, then the
members of `O` can be used as though they were members of `M` or `N`.
The *inline namespace set* of `N` is the transitive closure of all
inline namespaces in `N`. The *enclosing namespace set* of `O` is the
set of namespaces consisting of the innermost non-inline namespace
enclosing an inline namespace `O`, together with any intervening inline
namespaces.

#### Unnamed namespaces <a id="namespace.unnamed">[[namespace.unnamed]]</a>

An *unnamed-namespace-definition* behaves as if it were replaced by

``` bnf
'inline'ₒₚₜ 'namespace' \uniquens '{ /* empty body */ }'
'using namespace' \uniquens ';'
'namespace' \uniquens '{' namespace-body '}'
```

where `inline` appears if and only if it appears in the
*unnamed-namespace-definition*, all occurrences of in a translation unit
are replaced by the same identifier, and this identifier differs from
all other identifiers in the entire program.[^6]

``` cpp
namespace { int i; }            // \uniquens ::i
void f() { i++; }               // \uniquens ::i++

namespace A {
  namespace {
    int i;                      // A:: \uniquens ::i
    int j;                      // A:: \uniquens ::j
  }
  void g() { i++; }             // A:: \uniquens ::i++
}

using namespace A;
void h() {
  i++;                          // error: \uniquens ::i or A:: \uniquens ::i
  A::i++;                       // A:: \uniquens ::i
  j++;                          // A:: \uniquens ::j
}
```

#### Namespace member definitions <a id="namespace.memdef">[[namespace.memdef]]</a>

Members (including explicit specializations of templates (
[[temp.expl.spec]])) of a namespace can be defined within that
namespace.

``` cpp
namespace X {
  void f() { /* ... */ }
}
```

Members of a named namespace can also be defined outside that namespace
by explicit qualification ([[namespace.qual]]) of the name being
defined, provided that the entity being defined was already declared in
the namespace and the definition appears after the point of declaration
in a namespace that encloses the declaration’s namespace.

``` cpp
namespace Q {
  namespace V {
    void f();
  }
  void V::f() { /* ... */ }     // OK
  void V::g() { /* ... */ }     // error: g() is not yet a member of V
  namespace V {
    void g();
  }
}

namespace R {
  void Q::V::g() { /* ... */ }  // error: R doesn't enclose Q
}
```

Every name first declared in a namespace is a member of that namespace.
If a `friend` declaration in a non-local class first declares a class or
function[^7] the friend class or function is a member of the innermost
enclosing namespace. The name of the friend is not found by unqualified
lookup ([[basic.lookup.unqual]]) or by qualified lookup (
[[basic.lookup.qual]]) until a matching declaration is provided in that
namespace scope (either before or after the class definition granting
friendship). If a friend function is called, its name may be found by
the name lookup that considers functions from namespaces and classes
associated with the types of the function arguments (
[[basic.lookup.argdep]]). If the name in a `friend` declaration is
neither qualified nor a *template-id* and the declaration is a function
or an *elaborated-type-specifier*, the lookup to determine whether the
entity has been previously declared shall not consider any scopes
outside the innermost enclosing namespace. The other forms of `friend`
declarations cannot declare a new member of the innermost enclosing
namespace and thus follow the usual lookup rules.

``` cpp
// Assume f and g have not yet been defined.
void h(int);
template <class T> void f2(T);
namespace A {
  class X {
    friend void f(X);           // A::f(X) is a friend
    class Y {
      friend void g();          // A::g is a friend
      friend void h(int);       // A::h is a friend
                                // ::h not considered
      friend void f2<>(int);    // ::f2<>(int) is a friend
    };
  };

  // A::f, A::g and A::h are not visible here
  X x;
  void g() { f(x); }            // definition of A::g
  void f(X) { /* ... */}       // definition of A::f
  void h(int) { /* ... */ }    // definition of A::h
  // A::f, A::g and A::h are visible here and known to be friends
}

using A::x;

void h() {
  A::f(x);
  A::X::f(x);                   // error: f is not a member of A::X
  A::X::Y::g();                 // error: g is not a member of A::X::Y
}
```

### Namespace alias <a id="namespace.alias">[[namespace.alias]]</a>

A *namespace-alias-definition* declares an alternate name for a
namespace according to the following grammar:

``` bnf
namespace-alias:
        identifier
```

``` bnf
namespace-alias-definition:
        'namespace' identifier '=' qualified-namespace-specifier ';'
```

``` bnf
qualified-namespace-specifier:
    nested-name-specifierₒₚₜ namespace-name
```

The *identifier* in a *namespace-alias-definition* is a synonym for the
name of the namespace denoted by the *qualified-namespace-specifier* and
becomes a *namespace-alias*. When looking up a *namespace-name* in a
*namespace-alias-definition*, only namespace names are considered, see 
[[basic.lookup.udir]].

In a declarative region, a *namespace-alias-definition* can be used to
redefine a *namespace-alias* declared in that declarative region to
refer only to the namespace to which it already refers. the following
declarations are well-formed:

``` cpp
namespace Company_with_very_long_name { /* ... */ }
namespace CWVLN = Company_with_very_long_name;
namespace CWVLN = Company_with_very_long_name;          // OK: duplicate
namespace CWVLN = CWVLN;
```

A *namespace-name* or *namespace-alias* shall not be declared as the
name of any other entity in the same declarative region. A
*namespace-name* defined at global scope shall not be declared as the
name of any other entity in any global scope of the program. No
diagnostic is required for a violation of this rule by declarations in
different translation units.

### The `using` declaration <a id="namespace.udecl">[[namespace.udecl]]</a>

A *using-declaration* introduces a name into the declarative region in
which the *using-declaration* appears.

``` bnf
using-declaration:
    'using typenameₒₚₜ ' nested-name-specifier unqualified-id ';'
    'using ::' unqualified-id ';'
```

The member name specified in a *using-declaration* is declared in the
declarative region in which the *using-declaration* appears. Only the
specified name is so declared; specifying an enumeration name in a
*using-declaration* does not declare its enumerators in the
*using-declaration*’s declarative region. If a *using-declaration* names
a constructor ([[class.qual]]), it implicitly declares a set of
constructors in the class in which the *using-declaration* appears (
[[class.inhctor]]); otherwise the name specified in a
*using-declaration* is a synonym for the name of some entity declared
elsewhere.

Every *using-declaration* is a *declaration* and a *member-declaration*
and so can be used in a class definition.

``` cpp
struct B {
  void f(char);
  void g(char);
  enum E { e };
  union { int x; };
};

struct D : B {
  using B::f;
  void f(int) { f('c'); }       // calls B::f(char)
  void g(int) { g('c'); }       // recursively calls D::g(int)
};
```

In a *using-declaration* used as a *member-declaration*, the
*nested-name-specifier* shall name a base class of the class being
defined. If such a *using-declaration* names a constructor, the
*nested-name-specifier* shall name a direct base class of the class
being defined; otherwise it introduces the set of declarations found by
member name lookup ([[class.member.lookup]],  [[class.qual]]).

``` cpp
class C {
  int g();
};

class D2 : public B {
  using B::f;                   // OK: B is a base of D2
  using B::e;                   // OK: e is an enumerator of base B
  using B::x;                   // OK: x is a union member of base B
  using C::g;                   // error: C isn't a base of D2
};
```

Since destructors do not have names, a *using-declaration* cannot refer
to a destructor for a base class. Since specializations of member
templates for conversion functions are not found by name lookup, they
are not considered when a *using-declaration* specifies a conversion
function ([[temp.mem]]). If an assignment operator brought from a base
class into a derived class scope has the signature of a copy/move
assignment operator for the derived class ([[class.copy]]), the
*using-declaration* does not by itself suppress the implicit declaration
of the derived class assignment operator; the copy/move assignment
operator from the base class is hidden or overridden by the
implicitly-declared copy/move assignment operator of the derived class,
as described below.

A *using-declaration* shall not name a *template-id*.

``` cpp
struct A {
  template <class T> void f(T);
  template <class T> struct X { };
};
struct B : A {
  using A::f<double>;           // ill-formed
  using A::X<int>;              // ill-formed
};
```

A *using-declaration* shall not name a namespace.

A *using-declaration* shall not name a scoped enumerator.

A *using-declaration* for a class member shall be a
*member-declaration*.

``` cpp
struct X {
  int i;
  static int s;
};

void f() {
  using X::i;       // error: X::i is a class member
                    // and this is not a member declaration.
  using X::s;       // error: X::s is a class member
                    // and this is not a member declaration.
}
```

Members declared by a *using-declaration* can be referred to by explicit
qualification just like other member names ([[namespace.qual]]). In a
*using-declaration*, a prefix `::` refers to the global namespace.

``` cpp
void f();

namespace A {
  void g();
}

namespace X {
  using ::f;        // global f
  using A::g;       // A's g
}

void h()
{
  X::f();           // calls ::f
  X::g();           // calls A::g
}
```

A *using-declaration* is a *declaration* and can therefore be used
repeatedly where (and only where) multiple declarations are allowed.

``` cpp
namespace A {
  int i;
}

namespace A1 {
  using A::i;
  using A::i;       // OK: double declaration
}

void f() {
  using A::i;
  using A::i;       // error: double declaration
}

struct B {
  int i;
};

struct X : B {
  using B::i;
  using B::i;       // error: double member declaration
};
```

The entity declared by a *using-declaration* shall be known in the
context using it according to its definition at the point of the
*using-declaration*. Definitions added to the namespace after the
*using-declaration* are not considered when a use of the name is made.

``` cpp
namespace A {
  void f(int);
}

using A::f;         // f is a synonym for A::f;
                    // that is, for A::f(int).
namespace A {
  void f(char);
}

void foo() {
  f('a');           // calls f(int),
}                   // even though f(char) exists.

void bar() {
  using A::f;       // f is a synonym for A::f;
                    // that is, for A::f(int) and A::f(char).
  f('a');           // calls f(char)
}
```

Partial specializations of class templates are found by looking up the
primary class template and then considering all partial specializations
of that template. If a *using-declaration* names a class template,
partial specializations introduced after the *using-declaration* are
effectively visible because the primary template is visible (
[[temp.class.spec]]).

Since a *using-declaration* is a declaration, the restrictions on
declarations of the same name in the same declarative region (
[[basic.scope]]) also apply to *using-declaration*s.

``` cpp
namespace A {
  int x;
}

namespace B {
  int i;
  struct g { };
  struct x { };
  void f(int);
  void f(double);
  void g(char);     // OK: hides struct g
}

void func() {
  int i;
  using B::i;       // error: i declared twice
  void f(char);
  using B::f;       // OK: each f is a function
  f(3.5);           // calls B::f(double)
  using B::g;
  g('a');           // calls B::g(char)
  struct g g1;      // g1 has class type B::g
  using B::x;
  using A::x;       // OK: hides struct B::x
  x = 99;           // assigns to A::x
  struct x x1;      // x1 has class type B::x
}
```

If a function declaration in namespace scope or block scope has the same
name and the same parameter types as a function introduced by a
*using-declaration*, and the declarations do not declare the same
function, the program is ill-formed. Two *using-declaration*s may
introduce functions with the same name and the same parameter types. If,
for a call to an unqualified function name, function overload resolution
selects the functions introduced by such *using-declaration*s, the
function call is ill-formed.

``` cpp
namespace B {
  void f(int);
  void f(double);
}
namespace C {
  void f(int);
  void f(double);
  void f(char);
}

void h() {
  using B::f;       // B::f(int) and B::f(double)
  using C::f;       // C::f(int), C::f(double), and C::f(char)
  f('h');           // calls C::f(char)
  f(1);             // error: ambiguous: B::f(int) or C::f(int)?
  void f(int);      // error: f(int) conflicts with C::f(int) and B::f(int)
}
```

When a *using-declaration* brings names from a base class into a derived
class scope, member functions and member function templates in the
derived class override and/or hide member functions and member function
templates with the same name, parameter-type-list ([[dcl.fct]]),
cv-qualification, and *ref-qualifier* (if any) in a base class (rather
than conflicting). For *using-declarations* that name a constructor,
see  [[class.inhctor]].

``` cpp
struct B {
  virtual void f(int);
  virtual void f(char);
  void g(int);
  void h(int);
};

struct D : B {
  using B::f;
  void f(int);      // OK: D::f(int) overrides B::f(int);

  using B::g;
  void g(char);     // OK

  using B::h;
  void h(int);      // OK: D::h(int) hides B::h(int)
};

void k(D* p)
{
  p->f(1);          // calls D::f(int)
  p->f('a');        // calls B::f(char)
  p->g(1);          // calls B::g(int)
  p->g('a');        // calls D::g(char)
}
```

For the purpose of overload resolution, the functions which are
introduced by a *using-declaration* into a derived class will be treated
as though they were members of the derived class. In particular, the
implicit `this` parameter shall be treated as if it were a pointer to
the derived class rather than to the base class. This has no effect on
the type of the function, and in all other respects the function remains
a member of the base class.

The access rules for inheriting constructors are specified in 
[[class.inhctor]]; otherwise all instances of the name mentioned in a
*using-declaration* shall be accessible. In particular, if a derived
class uses a *using-declaration* to access a member of a base class, the
member name shall be accessible. If the name is that of an overloaded
member function, then all functions named shall be accessible. The base
class members mentioned by a *using-declaration* shall be visible in the
scope of at least one of the direct base classes of the class where the
*using-declaration* is specified. Because a *using-declaration*
designates a base class member (and not a member subobject or a member
function of a base class subobject), a *using-declaration* cannot be
used to resolve inherited member ambiguities. For example,

``` cpp
struct A { int x(); };
struct B : A { };
struct C : A {
  using A::x;
  int x(int);
};

struct D : B, C {
  using C::x;
  int x(double);
};
int f(D* d) {
  return d->x();    // ambiguous: B::x or C::x
}
```

The alias created by the *using-declaration* has the usual accessibility
for a *member-declaration*. A *using-declaration* that names a
constructor does not create aliases; see  [[class.inhctor]] for the
pertinent accessibility rules.

``` cpp
class A {
private:
    void f(char);
public:
    void f(int);
protected:
    void g();
};

class B : public A {
  using A::f;       // error: A::f(char) is inaccessible
public:
  using A::g;       // B::g is a public synonym for A::g
};
```

If a *using-declaration* uses the keyword `typename` and specifies a
dependent name ([[temp.dep]]), the name introduced by the
*using-declaration* is treated as a *typedef-name* ([[dcl.typedef]]).

### Using directive <a id="namespace.udir">[[namespace.udir]]</a>

``` bnf
using-directive:
    attribute-specifier-seqₒₚₜ 'using namespace' nested-name-specifierₒₚₜ namespace-name ';'
```

A *using-directive* shall not appear in class scope, but may appear in
namespace scope or in block scope. When looking up a *namespace-name* in
a *using-directive*, only namespace names are considered, see 
[[basic.lookup.udir]]. The optional *attribute-specifier-seq* appertains
to the *using-directive*.

A *using-directive* specifies that the names in the nominated namespace
can be used in the scope in which the *using-directive* appears after
the *using-directive*. During unqualified name lookup (
[[basic.lookup.unqual]]), the names appear as if they were declared in
the nearest enclosing namespace which contains both the
*using-directive* and the nominated namespace. In this context,
“contains” means “contains directly or indirectly”.

A *using-directive* does not add any members to the declarative region
in which it appears.

``` cpp
namespace A {
  int i;
  namespace B {
    namespace C {
      int i;
    }
    using namespace A::B::C;
    void f1() {
      i = 5;        // OK, C::i visible in B and hides A::i
    }
  }
  namespace D {
    using namespace B;
    using namespace C;
    void f2() {
      i = 5;        // ambiguous, B::C::i or A::i?
    }
  }
  void f3() {
    i = 5;          // uses A::i
  }
}
void f4() {
  i = 5;            // ill-formed; neither i is visible
}
```

For unqualified lookup ([[basic.lookup.unqual]]), the *using-directive*
is transitive: if a scope contains a *using-directive* that nominates a
second namespace that itself contains *using-directive*s, the effect is
as if the *using-directive*s from the second namespace also appeared in
the first. For qualified lookup, see  [[namespace.qual]].

``` cpp
namespace M {
  int i;
}

namespace N {
  int i;
  using namespace M;
}

void f() {
  using namespace N;
  i = 7;            // error: both M::i and N::i are visible
}
```

For another example,

``` cpp
namespace A {
  int i;
}
namespace B {
  int i;
  int j;
  namespace C {
    namespace D {
      using namespace A;
      int j;
      int k;
      int a = i;    // B::i hides A::i
    }
    using namespace D;
    int k = 89;     // no problem yet
    int l = k;      // ambiguous: C::k or D::k
    int m = i;      // B::i hides A::i
    int n = j;      // D::j hides B::j
  }
}
```

If a namespace is extended by an *extension-namespace-definition* after
a *using-directive* for that namespace is given, the additional members
of the extended namespace and the members of namespaces nominated by
*using-directive*s in the *extension-namespace-definition* can be used
after the *extension-namespace-definition*.

If name lookup finds a declaration for a name in two different
namespaces, and the declarations do not declare the same entity and do
not declare functions, the use of the name is ill-formed. In particular,
the name of a variable, function or enumerator does not hide the name of
a class or enumeration declared in a different namespace. For example,

``` cpp
namespace A {
  class X { };
  extern "C"   int g();
  extern "C++" int h();
}
namespace B {
  void X(int);
  extern "C"   int g();
  extern "C++" int h(int);
}
using namespace A;
using namespace B;

void f() {
  X(1);             // error: name X found in two namespaces
  g();              // okay: name g refers to the same entity
  h();              // okay: overload resolution selects A::h
}
```

During overload resolution, all functions from the transitive search are
considered for argument matching. The set of declarations found by the
transitive search is unordered. In particular, the order in which
namespaces were considered and the relationships among the namespaces
implied by the *using-directive*s do not cause preference to be given to
any of the declarations found by the search. An ambiguity exists if the
best match finds two functions with the same signature, even if one is
in a namespace reachable through *using-directive*s in the namespace of
the other.[^8]

``` cpp
namespace D {
  int d1;
  void f(char);
}
using namespace D;

int d1;             // OK: no conflict with D::d1

namespace E {
  int e;
  void f(int);
}

namespace D {       // namespace extension
  int d2;
  using namespace E;
  void f(int);
}

void f() {
  d1++;             // error: ambiguous ::d1 or D::d1?
  ::d1++;           // OK
  D::d1++;          // OK
  d2++;             // OK: D::d2
  e++;              // OK: E::e
  f(1);             // error: ambiguous: D::f(int) or E::f(int)?
  f('a');           // OK: D::f(char)
}
```

## The `asm` declaration <a id="dcl.asm">[[dcl.asm]]</a>

An `asm` declaration has the form

``` bnf
asm-definition:
    'asm (' string-literal ') ;'
```

The `asm` declaration is conditionally-supported; its meaning is
*implementation-defined*. Typically it is used to pass information
through the implementation to an assembler.

## Linkage specifications <a id="dcl.link">[[dcl.link]]</a>

All function types, function names with external linkage, and variable
names with external linkage have a *language linkage*. Some of the
properties associated with an entity with language linkage are specific
to each implementation and are not described here. For example, a
particular language linkage may be associated with a particular form of
representing names of objects and functions with external linkage, or
with a particular calling convention, etc. The default language linkage
of all function types, function names, and variable names is C++language
linkage. Two function types with different language linkages are
distinct types even if they are otherwise identical.

Linkage ([[basic.link]]) between C++and non-C++code fragments can be
achieved using a *linkage-specification*:

``` bnf
linkage-specification:
    'extern' string-literal '{' declaration-seqₒₚₜ '}'
    'extern' string-literal declaration
```

The *string-literal* indicates the required language linkage. This
International Standard specifies the semantics for the *string-literal*s
`"C"` and `"C++"`. Use of a *string-literal* other than `"C"` or `"C++"`
is conditionally-supported, with *implementation-defined* semantics.
Therefore, a linkage-specification with a *string-literal* that is
unknown to the implementation requires a diagnostic. It is recommended
that the spelling of the *string-literal* be taken from the document
defining that language. For example, `Ada` (not `ADA`) and `Fortran` or
`FORTRAN`, depending on the vintage.

Every implementation shall provide for linkage to functions written in
the C programming language, `"C"`, and linkage to C++functions, `"C++"`.

``` cpp
complex sqrt(complex);          // C++linkage by default
extern "C" {
  double sqrt(double);          // C linkage
}
```

Linkage specifications nest. When linkage specifications nest, the
innermost one determines the language linkage. A linkage specification
does not establish a scope. A *linkage-specification* shall occur only
in namespace scope ([[basic.scope]]). In a *linkage-specification*, the
specified language linkage applies to the function types of all function
declarators, function names with external linkage, and variable names
with external linkage declared within the *linkage-specification*.

``` cpp
extern "C" void f1(void(*pf)(int));
                                // the name f1 and its function type have C language
                                // linkage; pf is a pointer to a C function
extern "C" typedef void FUNC();
FUNC f2;                        // the name f2 has \Cpp language linkage and the
                                // function's type has C language linkage
extern "C" FUNC f3;             // the name of function f3 and the function's type
                                // have C language linkage
void (*pf2)(FUNC*);             // the name of the variable pf2 has \Cpp linkage and
                                // the type of pf2 is pointer to \Cpp function that
                                // takes one parameter of type pointer to C function
extern "C" {
  static void f4();             // the name of the function f4 has
                                // internal linkage (not C language
                                // linkage) and the function's type
                                // has C language linkage.
}

extern "C" void f5() {
  extern void f4();             // OK: Name linkage (internal)
                                // and function type linkage (C
                                // language linkage) gotten from
                                // previous declaration.
}

extern void f4();               // OK: Name linkage (internal)
                                // and function type linkage (C
                                // language linkage) gotten from
                                // previous declaration.
}

void f6() {
  extern void f4();             // OK: Name linkage (internal)
                                // and function type linkage (C
                                // language linkage) gotten from
                                // previous declaration.
}
```

A C language linkage is ignored in determining the language linkage of
the names of class members and the function type of class member
functions.

``` cpp
extern "C" typedef void FUNC_c();
class C {
   void mf1(FUNC_c*);           // the name of the function mf1 and the member
                                // function's type have C++language linkage; the
                                // parameter has type pointer to C function
   FUNC_c mf2;                  // the name of the function mf2 and the member
                                // function's type have C++language linkage
   static FUNC_c* q;            // the name of the data member q has C++language
                                // linkage and the data member's type is pointer to
                                // C function
};

extern "C" {
  class X {
  void mf();                    // the name of the function mf and the member
                                // function's type have C++language linkage
  void mf2(void(*)());          // the name of the function mf2 has C++language
                                // linkage; the parameter has type pointer to
                                // C function
  };
}
```

If two declarations declare functions with the same name and
*parameter-type-list* ([[dcl.fct]]) to be members of the same namespace
or declare objects with the same name to be members of the same
namespace and the declarations give the names different language
linkages, the program is ill-formed; no diagnostic is required if the
declarations appear in different translation units. Except for functions
with C++linkage, a function declaration without a linkage specification
shall not precede the first linkage specification for that function. A
function can be declared without a linkage specification after an
explicit linkage specification has been seen; the linkage explicitly
specified in the earlier declaration is not affected by such a function
declaration.

At most one function with a particular name can have C language linkage.
Two declarations for a function with C language linkage with the same
function name (ignoring the namespace names that qualify it) that appear
in different namespace scopes refer to the same function. Two
declarations for a variable with C language linkage with the same name
(ignoring the namespace names that qualify it) that appear in different
namespace scopes refer to the same variable. An entity with C language
linkage shall not be declared with the same name as an entity in global
scope, unless both declarations denote the same entity; no diagnostic is
required if the declarations appear in different translation units. A
variable with C language linkage shall not be declared with the same
name as a function with C language linkage (ignoring the namespace names
that qualify the respective names); no diagnostic is required if the
declarations appear in different translation units. Only one definition
for an entity with a given name with C language linkage may appear in
the program (see  [[basic.def.odr]]); this implies that such an entity
must not be defined in more than one namespace scope.

``` cpp
int x;
namespace A {
  extern "C" int f();
  extern "C" int g() { return 1; }
  extern "C" int h();
  extern "C" int x();               // ill-formed: same name as global-space object x
}

namespace B {
  extern "C" int f();               // A::f and B::f refer to the same function
  extern "C" int g() { return 1; }  // ill-formed, the function g
                                    // with C language linkage has two definitions
}

int A::f() { return 98; }           //definition for the function f with C language linkage
extern "C" int h() { return 97; }   // definition for the function h with C language linkage
                                    // A::h and ::h refer to the same function
```

A declaration directly contained in a *linkage-specification* is treated
as if it contains the `extern` specifier ([[dcl.stc]]) for the purpose
of determining the linkage of the declared name and whether it is a
definition. Such a declaration shall not specify a storage class.

``` cpp
extern "C" double f();
static double f();                  // error
extern "C" int i;                   // declaration
extern "C" {
  int i;                            // definition
}
extern "C" static void g();         // error
```

Because the language linkage is part of a function type, when a pointer
to C function (for example) is dereferenced, the function to which it
refers is considered a C function.

Linkage from C++to objects defined in other languages and to objects
defined in C++from other languages is implementation-defined and
language-dependent. Only where the object layout strategies of two
language implementations are similar enough can such linkage be
achieved.

## Attributes <a id="dcl.attr">[[dcl.attr]]</a>

### Attribute syntax and semantics <a id="dcl.attr.grammar">[[dcl.attr.grammar]]</a>

Attributes specify additional information for various source constructs
such as types, variables, names, blocks, or translation units.

``` bnf
attribute-specifier-seq:
  attribute-specifier-seqₒₚₜ attribute-specifier
```

``` bnf
attribute-specifier:
  '[' '[' attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  'alignas (' type-id '...'ₒₚₜ ')'
  'alignas (' alignment-expression '...'ₒₚₜ ')'
```

``` bnf
attribute-list:
  attributeₒₚₜ 
  attribute-list ',' attributeₒₚₜ 
  attribute '...'
  attribute-list ',' attribute '...'
```

``` bnf
attribute:
    attribute-token attribute-argument-clauseₒₚₜ
```

``` bnf
attribute-token:
    identifier
    attribute-scoped-token
```

``` bnf
attribute-scoped-token:
    attribute-namespace '::' identifier
```

``` bnf
attribute-namespace:
    identifier
```

``` bnf
attribute-argument-clause:
    '(' balanced-token-seq ')'
```

``` bnf
balanced-token-seq:
    balanced-tokenₒₚₜ 
    balanced-token-seq balanced-token
```

``` bnf
balanced-token:
    '(' balanced-token-seq ')'
    '[' balanced-token-seq ']'
    '{' balanced-token-seq '}'
    any *token* other than a parenthesis, a bracket, or a brace
```

For each individual attribute, the form of the *balanced-token-seq* will
be specified.

In an *attribute-list*, an ellipsis may appear only if that
*attribute*’s specification permits it. An *attribute* followed by an
ellipsis is a pack expansion ([[temp.variadic]]). An
*attribute-specifier* that contains no *attribute*s has no effect. The
order in which the *attribute-tokens* appear in an *attribute-list* is
not significant. If a keyword ([[lex.key]]) or an alternative token (
[[lex.digraph]]) that satisfies the syntactic requirements of an
*identifier* ([[lex.name]]) is contained in an *attribute-token*, it is
considered an identifier. No name lookup ([[basic.lookup]]) is
performed on any of the identifiers contained in an *attribute-token*.
The *attribute-token* determines additional requirements on the
*attribute-argument-clause* (if any). The use of an
*attribute-scoped-token* is conditionally-supported, with
*implementation-defined* behavior. Each implementation should choose a
distinctive name for the *attribute-namespace* in an
*attribute-scoped-token*.

Each *attribute-specifier-seq* is said to *appertain* to some entity or
statement, identified by the syntactic context where it appears (Clause 
[[stmt.stmt]], Clause  [[dcl.dcl]], Clause  [[dcl.decl]]). If an
*attribute-specifier-seq* that appertains to some entity or statement
contains an *attribute* that is not allowed to apply to that entity or
statement, the program is ill-formed. If an *attribute-specifier-seq*
appertains to a friend declaration ([[class.friend]]), that declaration
shall be a definition. No *attribute-specifier-seq* shall appertain to
an explicit instantiation ([[temp.explicit]]).

For an *attribute-token* not specified in this International Standard,
the behavior is *implementation-defined*.

Two consecutive left square bracket tokens shall appear only when
introducing an *attribute-specifier*. If two consecutive left square
brackets appear where an *attribute-specifier* is not allowed, the
program is ill formed even if the brackets match an alternative grammar
production.

``` cpp
int p[10];
void f() {
  int x = 42, y[5];
  int(p[[x] { return x; }()]);  // error: malformed attribute on a nested
                                // declarator-id and not a function-style cast of
                                // an element of p.
  y[[] { return 2; }()] = 2;    // error even though attributes are not allowed
                                // in this context.
}
```

### Alignment specifier <a id="dcl.align">[[dcl.align]]</a>

An *alignment-specifier* may be applied to a variable or to a class data
member, but it shall not be applied to a bit-field, a function
parameter, the formal parameter of a catch clause ([[except.handle]]),
or a variable declared with the `register` storage class specifier. An
*alignment-specifier* may also be applied to the declaration of a class
or enumeration type. An *alignment-specifier* with an ellipsis is a pack
expansion ([[temp.variadic]]).

When the *alignment-specifier* is of the form `alignas(`
*assignment-expression* `)`:

- the *assignment-expression* shall be an integral constant expression
- if the constant expression evaluates to a fundamental alignment, the
  alignment requirement of the declared entity shall be the specified
  fundamental alignment
- if the constant expression evaluates to an extended alignment and the
  implementation supports that alignment in the context of the
  declaration, the alignment of the declared entity shall be that
  alignment
- if the constant expression evaluates to an extended alignment and the
  implementation does not support that alignment in the context of the
  declaration, the program is ill-formed
- if the constant expression evaluates to zero, the alignment specifier
  shall have no effect
- otherwise, the program is ill-formed.

When the *alignment-specifier* is of the form `alignas(` *type-id* `)`,
it shall have the same effect as `alignas({}alignof(`*type-id*`))` (
[[expr.alignof]]).

When multiple *alignment-specifier*s are specified for an entity, the
alignment requirement shall be set to the strictest specified alignment.

The combined effect of all *alignment-specifier*s in a declaration shall
not specify an alignment that is less strict than the alignment that
would be required for the entity being declared if all
*alignment-specifier*s were omitted (including those in other
declarations).

If the defining declaration of an entity has an *alignment-specifier*,
any non-defining declaration of that entity shall either specify
equivalent alignment or have no *alignment-specifier*. Conversely, if
any declaration of an entity has an *alignment-specifier*, every
defining declaration of that entity shall specify an equivalent
alignment. No diagnostic is required if declarations of an entity have
different *alignment-specifier*s in different translation units.

``` cpp
// Translation unit #1:
struct S { int x; } s, p = &s;

// Translation unit #2:
struct alignas(16) S;           // error: definition of S lacks alignment; no
extern S* p;                    // diagnostic required
```

An aligned buffer with an alignment requirement of `A` and holding `N`
elements of type `T` other than `char`, `signed char`, or
`unsigned char` can be declared as:

``` cpp
alignas(T) alignas(A) T buffer[N];
```

Specifying `alignas(T)` ensures that the final requested alignment will
not be weaker than `alignof(T)`, and therefore the program will not be
ill-formed.

``` cpp
alignas(double) void f();                         // error: alignment applied to function
alignas(double) unsigned char c[sizeof(double)];  // array of characters, suitably aligned for a double
extern unsigned char c[sizeof(double)];           // no alignas necessary
alignas(float)
  extern unsigned char c[sizeof(double)];         // error: different alignment in declaration
```

### Noreturn attribute <a id="dcl.attr.noreturn">[[dcl.attr.noreturn]]</a>

The *attribute-token* `noreturn` specifies that a function does not
return. It shall appear at most once in each *attribute-list* and no
*attribute-argument-clause* shall be present. The attribute may be
applied to the *declarator-id* in a function declaration. The first
declaration of a function shall specify the `noreturn` attribute if any
declaration of that function specifies the `noreturn` attribute. If a
function is declared with the `noreturn` attribute in one translation
unit and the same function is declared without the `noreturn` attribute
in another translation unit, the program is ill-formed; no diagnostic
required.

If a function `f` is called where `f` was previously declared with the
`noreturn` attribute and `f` eventually returns, the behavior is
undefined. The function may terminate by throwing an exception.
Implementations are encouraged to issue a warning if a function marked
`[[noreturn]]` might return.

``` cpp
[[ noreturn ]] void f() {
  throw "error";        // OK
}

[[ noreturn ]] void q(int i) { // behavior is undefined if called with an argument <= 0
  if (i > 0)
    throw "positive";
}
```

### Carries dependency attribute <a id="dcl.attr.depend">[[dcl.attr.depend]]</a>

The *attribute-token* `carries_dependency` specifies dependency
propagation into and out of functions. It shall appear at most once in
each *attribute-list* and no *attribute-argument-clause* shall be
present. The attribute may be applied to the *declarator-id* of a
*parameter-declaration* in a function declaration or lambda, in which
case it specifies that the initialization of the parameter carries a
dependency to ([[intro.multithread]]) each lvalue-to-rvalue
conversion ([[conv.lval]]) of that object. The attribute may also be
applied to the *declarator-id* of a function declaration, in which case
it specifies that the return value, if any, carries a dependency to the
evaluation of the function call expression.

The first declaration of a function shall specify the
`carries_dependency` attribute for its *declarator-id* if any
declaration of the function specifies the `carries_dependency`
attribute. Furthermore, the first declaration of a function shall
specify the `carries_dependency` attribute for a parameter if any
declaration of that function specifies the `carries_dependency`
attribute for that parameter. If a function or one of its parameters is
declared with the `carries_dependency` attribute in its first
declaration in one translation unit and the same function or one of its
parameters is declared without the `carries_dependency` attribute in its
first declaration in another translation unit, the program is
ill-formed; no diagnostic required.

The `carries_dependency` attribute does not change the meaning of the
program, but may result in generation of more efficient code.

``` cpp
/* Translation unit A. */

struct foo { int* a; int* b; };
std::atomic<struct foo *> foo_head[10];
int foo_array[10][10];

[[carries_dependency]] struct foo* f(int i) {
  return foo_head[i].load(memory_order_consume);
}

[[carries_dependency]] int g(int* x, int* y) {
  return kill_dependency(foo_array[*x][*y]);
}

/* Translation unit B. */

[[carries_dependency]] struct foo* f(int i);
[[carries_dependency]] int* g(int* x, int* y);

int c = 3;

void h(int i) {
  struct foo* p;

  p = f(i);
  do_something_with(g(&c, p->a));
  do_something_with(g(p->a, &c));
}
```

The `carries_dependency` attribute on function `f` means that the return
value carries a dependency out of `f`, so that the implementation need
not constrain ordering upon return from `f`. Implementations of `f` and
its caller may choose to preserve dependencies instead of emitting
hardware memory ordering instructions (a.k.a. fences).

Function `g`’s second argument has a `carries_dependency` attribute, but
its first argument does not. Therefore, function `h`’s first call to `g`
carries a dependency into `g`, but its second call does not. The
implementation might need to insert a fence prior to the second call to
`g`.

# Declarators <a id="dcl.decl">[[dcl.decl]]</a>

A declarator declares a single variable, function, or type, within a
declaration. The *init-declarator-list* appearing in a declaration is a
comma-separated sequence of declarators, each of which can have an
initializer.

``` bnf
init-declarator-list:
    init-declarator
    init-declarator-list ',' init-declarator
```

``` bnf
init-declarator:
    declarator initializerₒₚₜ
```

The three components of a *simple-declaration* are the attributes (
[[dcl.attr]]), the specifiers (*decl-specifier-seq*; [[dcl.spec]]) and
the declarators (*init-declarator-list*). The specifiers indicate the
type, storage class or other properties of the entities being declared.
The declarators specify the names of these entities and (optionally)
modify the type of the specifiers with operators such as `*` (pointer
to) and `()` (function returning). Initial values can also be specified
in a declarator; initializers are discussed in  [[dcl.init]] and 
[[class.init]].

Each *init-declarator* in a declaration is analyzed separately as if it
was in a declaration by itself.[^9]

Declarators have the syntax

``` bnf
declarator:
    ptr-declarator
    noptr-declarator parameters-and-qualifiers trailing-return-type
```

``` bnf
ptr-declarator:
    noptr-declarator
    ptr-operator ptr-declarator
```

``` bnf
noptr-declarator:
    declarator-id attribute-specifier-seqₒₚₜ 
    noptr-declarator parameters-and-qualifiers
    noptr-declarator '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ 
    '(' ptr-declarator ')'
```

``` bnf
parameters-and-qualifiers:
    '(' parameter-declaration-clause ')' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 
\hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ
```

``` bnf
trailing-return-type:
    '->' trailing-type-specifier-seq abstract-declaratorₒₚₜ
```

``` bnf
ptr-operator:
    '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 
    '&' attribute-specifier-seqₒₚₜ 
    '&&' attribute-specifier-seqₒₚₜ 
    nested-name-specifier '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ
```

``` bnf
cv-qualifier-seq:
    cv-qualifier cv-qualifier-seqₒₚₜ
```

``` bnf
cv-qualifier:
    'const'
    'volatile'
```

``` bnf
ref-qualifier:
    '&'
    '&&'
```

``` bnf
declarator-id:
    '...'ₒₚₜ id-expression
    nested-name-specifierₒₚₜ class-name
```

A *class-name* has special meaning in a declaration of the class of that
name and when qualified by that name using the scope resolution operator
`::` ([[expr.prim]], [[class.ctor]], [[class.dtor]]).

The optional *attribute-specifier-seq* in a *trailing-return-type*
appertains to the indicated return type. The *type-id* in a
*trailing-return-type* includes the longest possible sequence of
*abstract-declarator*s. This resolves the ambiguous binding of array and
function declarators.

``` cpp
auto f()->int(*)[4];  // function returning a pointer to array[4] of int
                      // not function returning array[4] of pointer to int
```

## Type names <a id="dcl.name">[[dcl.name]]</a>

To specify type conversions explicitly, and as an argument of `sizeof`,
`alignof`, `new`, or `typeid`, the name of a type shall be specified.
This can be done with a *type-id*, which is syntactically a declaration
for a variable or function of that type that omits the name of the
entity.

``` bnf
type-id:
    type-specifier-seq abstract-declaratorₒₚₜ
```

``` bnf
abstract-declarator:
    ptr-abstract-declarator
    noptr-abstract-declaratorₒₚₜ parameters-and-qualifiers trailing-return-type
    abstract-pack-declarator
```

``` bnf
ptr-abstract-declarator:
    noptr-abstract-declarator
    ptr-operator ptr-abstract-declaratorₒₚₜ
```

``` bnf
noptr-abstract-declarator:
    noptr-abstract-declaratorₒₚₜ parameters-and-qualifiers
    noptr-abstract-declaratorₒₚₜ '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ 
    '(' ptr-abstract-declarator ')'
```

``` bnf
abstract-pack-declarator:
    noptr-abstract-pack-declarator
    ptr-operator abstract-pack-declarator
```

``` bnf
noptr-abstract-pack-declarator:
    noptr-abstract-pack-declarator parameters-and-qualifiers
    noptr-abstract-pack-declarator '[' constant-expressionₒₚₜ \ ']' attribute-specifier-seqₒₚₜ 
    '...'
```

It is possible to identify uniquely the location in the
*abstract-declarator* where the identifier would appear if the
construction were a declarator in a declaration. The named type is then
the same as the type of the hypothetical identifier.

``` cpp
int                 // int i
int *               // int *pi
int *[3]            // int *p[3]
int (*)[3]          // int (*p3i)[3]
int *()             // int *f()
int (*)(double)     // int (*pf)(double)
```

name respectively the types “`int`,” “pointer to `int`,” “array of 3
pointers to `int`,” “pointer to array of 3 `int`,” “function of (no
parameters) returning pointer to `int`,” and “pointer to a function of
(`double`) returning `int`.”

A type can also be named (often more easily) by using a *typedef* (
[[dcl.typedef]]).

## Ambiguity resolution <a id="dcl.ambig.res">[[dcl.ambig.res]]</a>

The ambiguity arising from the similarity between a function-style cast
and a declaration mentioned in  [[stmt.ambig]] can also occur in the
context of a declaration. In that context, the choice is between a
function declaration with a redundant set of parentheses around a
parameter name and an object declaration with a function-style cast as
the initializer. Just as for the ambiguities mentioned in 
[[stmt.ambig]], the resolution is to consider any construct that could
possibly be a declaration a declaration. A declaration can be explicitly
disambiguated by a nonfunction-style cast, by an `=` to indicate
initialization or by removing the redundant parentheses around the
parameter name.

``` cpp
struct S {
  S(int);
};

void foo(double a) {
  S w(int(a));      // function declaration
  S x(int());       // function declaration
  S y((int)a);      // object declaration
  S z = int(a);     // object declaration
}
```

The ambiguity arising from the similarity between a function-style cast
and a *type-id* can occur in different contexts. The ambiguity appears
as a choice between a function-style cast expression and a declaration
of a type. The resolution is that any construct that could possibly be a
*type-id* in its syntactic context shall be considered a *type-id*.

``` cpp
#include <cstddef>
char *p;
void *operator new(std::size_t, int);
void foo()  {
  const int x = 63;
  new (int(*p)) int;            // new-placement expression
  new (int(*[x]));              // new type-id
}
```

For another example,

``` cpp
template <class T>
struct S {
  T *p;
};
S<int()> x;                     // type-id
S<int(1)> y;                    // expression (ill-formed)
```

For another example,

``` cpp
void foo() {
  sizeof(int(1));               // expression
  sizeof(int());                // type-id (ill-formed)
}
```

For another example,

``` cpp
void foo() {
  (int(1));                     // expression
  (int())1;                     // type-id (ill-formed)
}
```

Another ambiguity arises in a *parameter-declaration-clause* of a
function declaration, or in a *type-id* that is the operand of a
`sizeof` or `typeid` operator, when a *type-name* is nested in
parentheses. In this case, the choice is between the declaration of a
parameter of type pointer to function and the declaration of a parameter
with redundant parentheses around the *declarator-id*. The resolution is
to consider the *type-name* as a *simple-type-specifier* rather than a
*declarator-id*.

``` cpp
class C { };
void f(int(C)) { }              // void f(int(*fp)(C c)) { }
                                // not: void f(int C);

int g(C);

void foo() {
  f(1);                         // error: cannot convert 1 to function pointer
  f(g);                         // OK
}
```

For another example,

``` cpp
class C { };
void h(int *(C[10]));           // void h(int *(*_fp)(C _parm[10]));
                                // not: void h(int *C[10]);
```

## Meaning of declarators <a id="dcl.meaning">[[dcl.meaning]]</a>

A list of declarators appears after an optional (Clause  [[dcl.dcl]])
*decl-specifier-seq* ([[dcl.spec]]). Each declarator contains exactly
one *declarator-id*; it names the identifier that is declared. An
*unqualified-id* occurring in a *declarator-id* shall be a simple
*identifier* except for the declaration of some special functions (
[[class.conv]], [[class.dtor]], [[over.oper]]) and for the declaration
of template specializations or partial specializations ([[temp.spec]]).
A *declarator-id* shall not be qualified except for the definition of a
member function ([[class.mfct]]) or static data member (
[[class.static]]) outside of its class, the definition or explicit
instantiation of a function or variable member of a namespace outside of
its namespace, or the definition of an explicit specialization outside
of its namespace, or the declaration of a friend function that is a
member of another class or namespace ([[class.friend]]). When the
*declarator-id* is qualified, the declaration shall refer to a
previously declared member of the class or namespace to which the
qualifier refers (or, in the case of a namespace, of an element of the
inline namespace set of that namespace ([[namespace.def]])) or to a
specialization thereof; the member shall not merely have been introduced
by a *using-declaration* in the scope of the class or namespace
nominated by the *nested-name-specifier* of the *declarator-id*. The
*nested-name-specifier* of a qualified *declarator-id* shall not begin
with a *decltype-specifier*. If the qualifier is the global `::` scope
resolution operator, the *declarator-id* refers to a name declared in
the global namespace scope. The optional *attribute-specifier-seq*
following a *declarator-id* appertains to the entity that is declared.

A `static`, `thread_local`, `extern`, `register`, `mutable`, `friend`,
`inline`, `virtual`, or `typedef` specifier applies directly to each
*declarator-id* in an *init-declarator-list*; the type specified for
each *declarator-id* depends on both the *decl-specifier-seq* and its
*declarator*.

Thus, a declaration of a particular identifier has the form

``` cpp
T D
```

where `T` is of the form *attribute-specifier-seqₒₚₜ *
*decl-specifier-seq* and `D` is a declarator. Following is a recursive
procedure for determining the type specified for the contained
*declarator-id* by such a declaration.

First, the *decl-specifier-seq* determines a type. In a declaration

``` cpp
T D
```

the *decl-specifier-seq* `T` determines the type `T`. in the declaration

``` cpp
int unsigned i;
```

the type specifiers `int` `unsigned` determine the type “`unsigned int`”
([[dcl.type.simple]]).

In a declaration *attribute-specifier-seqₒₚₜ * `T` `D` where `D` is an
unadorned identifier the type of this identifier is “`T`”.

In a declaration `T` `D` where `D` has the form

``` bnf
( D1 )
```

the type of the contained *declarator-id* is the same as that of the
contained *declarator-id* in the declaration

``` cpp
T D1
```

Parentheses do not alter the type of the embedded *declarator-id*, but
they can alter the binding of complex declarators.

### Pointers <a id="dcl.ptr">[[dcl.ptr]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
'*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 'D1'
```

and the type of the identifier in the declaration `T` `D1` is “ `T`,”
then the type of the identifier of `D` is “ pointer to `T`.” The
*cv-qualifier*s apply to the pointer and not to the object pointed to.
Similarly, the optional *attribute-specifier-seq* (
[[dcl.attr.grammar]]) appertains to the pointer and not to the object
pointed to.

the declarations

``` cpp
const int ci = 10, *pc = &ci, *const cpc = pc, **ppc;
int i, *p, *const cp = &i;
```

declare `ci`, a constant integer; `pc`, a pointer to a constant integer;
`cpc`, a constant pointer to a constant integer; `ppc`, a pointer to a
pointer to a constant integer; `i`, an integer; `p`, a pointer to
integer; and `cp`, a constant pointer to integer. The value of `ci`,
`cpc`, and `cp` cannot be changed after initialization. The value of
`pc` can be changed, and so can the object pointed to by `cp`. Examples
of some correct operations are

``` cpp
i = ci;
*cp = ci;
pc++;
pc = cpc;
pc = p;
ppc = &pc;
```

Examples of ill-formed operations are

``` cpp
ci = 1;             // error
ci++;               // error
*pc = 2;            // error
cp = &ci;           // error
cpc++;              // error
p = pc;             // error
ppc = &p;           // error
```

Each is unacceptable because it would either change the value of an
object declared `const` or allow it to be changed through a
cv-unqualified pointer later, for example:

``` cpp
*ppc = &ci;         // OK, but would make p point to ci ...
                    // ... because of previous error
*p = 5;             // clobber ci
```

See also  [[expr.ass]] and  [[dcl.init]].

There are no pointers to references; see  [[dcl.ref]]. Since the address
of a bit-field ([[class.bit]]) cannot be taken, a pointer can never
point to a bit-field.

### References <a id="dcl.ref">[[dcl.ref]]</a>

In a declaration `T` `D` where `D` has either of the forms

``` bnf
'&' attribute-specifier-seqₒₚₜ 'D1'
'&&' attribute-specifier-seqₒₚₜ 'D1'
```

and the type of the identifier in the declaration `T` `D1` is “ `T`,”
then the type of the identifier of `D` is “ reference to `T`.” The
optional *attribute-specifier-seq* appertains to the reference type.
Cv-qualified references are ill-formed except when the cv-qualifiers are
introduced through the use of a typedef ([[dcl.typedef]]) or of a
template type argument ([[temp.arg]]), in which case the cv-qualifiers
are ignored.

``` cpp
typedef int& A;
const A aref = 3;   // ill-formed; lvalue reference to non-const initialized with rvalue
```

The type of `aref` is “lvalue reference to `int`”, not “lvalue reference
to `const int`”. A reference can be thought of as a name of an object. A
declarator that specifies the type “reference to *cv* `void`” is
ill-formed.

A reference type that is declared using `&` is called an *lvalue
reference*, and a reference type that is declared using `&&` is called
an *rvalue reference*. Lvalue references and rvalue references are
distinct types. Except where explicitly noted, they are semantically
equivalent and commonly referred to as references.

``` cpp
void f(double& a) { a += 3.14; }
// ...
double d = 0;
f(d);
```

declares `a` to be a reference parameter of `f` so the call `f(d)` will
add `3.14` to `d`.

``` cpp
int v[20];
// ...
int& g(int i) { return v[i]; }
// ...
g(3) = 7;
```

declares the function `g()` to return a reference to an integer so
`g(3)=7` will assign `7` to the fourth element of the array `v`. For
another example,

``` cpp
struct link {
  link* next;
};

link* first;

void h(link*& p) {  // p is a reference to pointer
  p->next = first;
  first = p;
  p = 0;
}

void k() {
   link* q = new link;
   h(q);
}
```

declares `p` to be a reference to a pointer to `link` so `h(q)` will
leave `q` with the value zero. See also  [[dcl.init.ref]].

It is unspecified whether or not a reference requires storage (
[[basic.stc]]).

There shall be no references to references, no arrays of references, and
no pointers to references. The declaration of a reference shall contain
an *initializer* ([[dcl.init.ref]]) except when the declaration
contains an explicit `extern` specifier ([[dcl.stc]]), is a class
member ([[class.mem]]) declaration within a class definition, or is the
declaration of a parameter or a return type ([[dcl.fct]]); see 
[[basic.def]]. A reference shall be initialized to refer to a valid
object or function. in particular, a null reference cannot exist in a
well-defined program, because the only way to create such a reference
would be to bind it to the “object” obtained by dereferencing a null
pointer, which causes undefined behavior. As described in 
[[class.bit]], a reference cannot be bound directly to a bit-field.

If a typedef ([[dcl.typedef]]), a type *template-parameter* (
[[temp.arg.type]]), or a *decltype-specifier* ([[dcl.type.simple]])
denotes a type `TR` that is a reference to a type `T`, an attempt to
create the type “lvalue reference to cv `TR`” creates the type “lvalue
reference to `T`”, while an attempt to create the type “rvalue reference
to cv `TR`” creates the type `TR`.

``` cpp
int i;
typedef int& LRI;
typedef int&& RRI;

LRI& r1 = i;                    // r1 has the type int&
const LRI& r2 = i;              // r2 has the type int&
const LRI&& r3 = i;             // r3 has the type int&

RRI& r4 = i;                    // r4 has the type int&
RRI&& r5 = 5;                   // r5 has the type int&&

decltype(r2)& r6 = i;           // r6 has the type int&
decltype(r2)&& r7 = i;          // r7 has the type int&
```

### Pointers to members <a id="dcl.mptr">[[dcl.mptr]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
nested-name-specifier '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ D1
```

and the *nested-name-specifier* denotes a class, and the type of the
identifier in the declaration `T` `D1` is “ `T`”, then the type of the
identifier of `D` is “ pointer to member of class of type `T`”. The
optional *attribute-specifier-seq* ([[dcl.attr.grammar]]) appertains to
the pointer-to-member.

``` cpp
struct X {
  void f(int);
  int a;
};
struct Y;

int X::* pmi = &X::a;
void (X::* pmf)(int) = &X::f;
double X::* pmd;
char Y::* pmc;
```

declares `pmi`, `pmf`, `pmd` and `pmc` to be a pointer to a member of
`X` of type `int`, a pointer to a member of `X` of type `void(int)`, a
pointer to a member of `X` of type `double` and a pointer to a member of
`Y` of type `char` respectively. The declaration of `pmd` is well-formed
even though `X` has no members of type `double`. Similarly, the
declaration of `pmc` is well-formed even though `Y` is an incomplete
type. `pmi` and `pmf` can be used like this:

``` cpp
X obj;
// ...
obj.*pmi = 7;       // assign 7 to an integer
                    // member of obj
(obj.*pmf)(7);      // call a function member of obj
                    // with the argument 7
```

A pointer to member shall not point to a static member of a class (
[[class.static]]), a member with reference type, or “*cv* `void`.”

See also  [[expr.unary]] and  [[expr.mptr.oper]]. The type “pointer to
member” is distinct from the type “pointer”, that is, a pointer to
member is declared only by the pointer to member declarator syntax, and
never by the pointer declarator syntax. There is no
“reference-to-member” type in C++.

### Arrays <a id="dcl.array">[[dcl.array]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
'D1 [' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ
```

and the type of the identifier in the declaration `T` `D1` is
“*derived-declarator-type-list* `T`”, then the type of the identifier of
`D` is an array type; if the type of the identifier of `D` contains the
`auto` , the program is ill-formed. `T` is called the array *element
type*; this type shall not be a reference type, the (possibly
cv-qualified) type `void`, a function type or an abstract class type. If
the *constant-expression* ([[expr.const]]) is present, it shall be an
integral constant expression and its value shall be greater than zero.
The constant expression specifies the *bound* of (number of elements in)
the array. If the value of the constant expression is `N`, the array has
`N` elements numbered `0` to `N-1`, and the type of the identifier of
`D` is “ array of `N` `T`”. An object of array type contains a
contiguously allocated non-empty set of `N` subobjects of type `T`.
Except as noted below, if the constant expression is omitted, the type
of the identifier of `D` is “ array of unknown bound of `T`”, an
incomplete object type. The type “ array of `N` `T`” is a different type
from the type “ array of unknown bound of `T`”, see  [[basic.types]].
Any type of the form “ array of `N` `T`” is adjusted to “array of `N`
`T`”, and similarly for “array of unknown bound of `T`”. The optional
*attribute-specifier-seq* appertains to the array.

``` cpp
typedef int A[5], AA[2][3];
typedef const A CA;             // type is ``array of 5 const int''
typedef const AA CAA;           // type is ``array of 2 array of 3 const int''
```

An “array of `N` `T`” has cv-qualified type; see 
[[basic.type.qualifier]].

An array can be constructed from one of the fundamental types (except
`void`), from a pointer, from a pointer to member, from a class, from an
enumeration type, or from another array.

When several “array of” specifications are adjacent, a multidimensional
array is created; only the first of the constant expressions that
specify the bounds of the arrays may be omitted. In addition to
declarations in which an incomplete object type is allowed, an array
bound may be omitted in some cases in the declaration of a function
parameter ([[dcl.fct]]). An array bound may also be omitted when the
declarator is followed by an *initializer* ([[dcl.init]]). In this case
the bound is calculated from the number of initial elements (say, `N`)
supplied ([[dcl.init.aggr]]), and the type of the identifier of `D` is
“array of `N` `T`.” Furthermore, if there is a preceding declaration of
the entity in the same scope in which the bound was specified, an
omitted array bound is taken to be the same as in that earlier
declaration, and similarly for the definition of a static data member of
a class.

``` cpp
float fa[17], *afp[17];
```

declares an array of `float` numbers and an array of pointers to `float`
numbers. For another example,

``` cpp
static int x3d[3][5][7];
```

declares a static three-dimensional array of integers, with rank
3 × 5 × 7. In complete detail, `x3d` is an array of three items; each
item is an array of five arrays; each of the latter arrays is an array
of seven integers. Any of the expressions `x3d`, `x3d[i]`, `x3d[i][j]`,
`x3d[i][j][k]` can reasonably appear in an expression. Finally,

``` cpp
extern int x[10];
struct S {
  static int y[10];
};

int x[];                      // OK: bound is 10
int S::y[];                   // OK: bound is 10

void f() {
  extern int x[];
  int i = sizeof(x);          // error: incomplete object type
}
```

conversions affecting expressions of array type are described in 
[[conv.array]]. Objects of array types cannot be modified, see 
[[basic.lval]].

Except where it has been declared for a class ([[over.sub]]), the
subscript operator `[]` is interpreted in such a way that `E1[E2]` is
identical to `*((E1)+(E2))`. Because of the conversion rules that apply
to `+`, if `E1` is an array and `E2` an integer, then `E1[E2]` refers to
the `E2`-th member of `E1`. Therefore, despite its asymmetric
appearance, subscripting is a commutative operation.

A consistent rule is followed for multidimensional arrays. If `E` is an
*n*-dimensional array of rank i × j × … × k, then `E` appearing in an
expression that is subject to the array-to-pointer conversion (
[[conv.array]]) is converted to a pointer to an (n-1)-dimensional array
with rank j × … × k. If the `*` operator, either explicitly or
implicitly as a result of subscripting, is applied to this pointer, the
result is the pointed-to (n-1)-dimensional array, which itself is
immediately converted into a pointer.

consider

``` cpp
int x[3][5];
```

Here `x` is a 3 × 5 array of integers. When `x` appears in an
expression, it is converted to a pointer to (the first of three)
five-membered arrays of integers. In the expression `x[i]` which is
equivalent to `*(x+i)`, `x` is first converted to a pointer as
described; then `x+i` is converted to the type of `x`, which involves
multiplying `i` by the length of the object to which the pointer points,
namely five integer objects. The results are added and indirection
applied to yield an array (of five integers), which in turn is converted
to a pointer to the first of the integers. If there is another subscript
the same argument applies again; this time the result is an integer.

It follows from all this that arrays in C++are stored row-wise (last
subscript varies fastest) and that the first subscript in the
declaration helps determine the amount of storage consumed by an array
but plays no other part in subscript calculations.

### Functions <a id="dcl.fct">[[dcl.fct]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
\hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ
```

and the type of the contained *declarator-id* in the declaration `T`
`D1` is “*derived-declarator-type-list* `T`”, the type of the
*declarator-id* in `D` is “ function of ( ) returning `T`”. The optional
*attribute-specifier-seq* appertains to the function type.

In a declaration `T` `D` where `D` has the form

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
\hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-type
```

and the type of the contained *declarator-id* in the declaration `T`
`D1` is “*derived-declarator-type-list* `T`”, `T` shall be the single
*type-specifier* `auto`. The type of the *declarator-id* in `D` is
“*derived-declarator-type-list* function of
(*parameter-declaration-clause*) *cv-qualifier-seq*ₒₚₜ
*ref-qualifier*ₒₚₜ returning *trailing-return-type*”. The optional
*attribute-specifier-seq* appertains to the function type.

A type of either form is a *function type*.[^10]

``` bnf
parameter-declaration-clause:
    parameter-declaration-listₒₚₜ ...ₒₚₜ 
    parameter-declaration-list ',' ...
```

``` bnf
parameter-declaration-list:
    parameter-declaration
    parameter-declaration-list ',' parameter-declaration
```

``` bnf
parameter-declaration:
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator
    attribute-specifier-seqₒₚₜ decl-specifier-seq declarator '=' initializer-clause
    attribute-specifier-seqₒₚₜ decl-specifier-seq abstract-declaratorₒₚₜ 
    attribute-specifier-seqₒₚₜ decl-specifier-seq abstract-declaratorₒₚₜ '=' initializer-clause
```

The optional *attribute-specifier-seq* in a *parameter-declaration*
appertains to the parameter.

The *parameter-declaration-clause* determines the arguments that can be
specified, and their processing, when the function is called. the
*parameter-declaration-clause* is used to convert the arguments
specified on the function call; see  [[expr.call]]. If the
*parameter-declaration-clause* is empty, the function takes no
arguments. The parameter list `(void)` is equivalent to the empty
parameter list. Except for this special case, `void` shall not be a
parameter type (though types derived from `void`, such as `void*`, can).
If the *parameter-declaration-clause* terminates with an ellipsis or a
function parameter pack ([[temp.variadic]]), the number of arguments
shall be equal to or greater than the number of parameters that do not
have a default argument and are not function parameter packs. Where
syntactically correct and where “” is not part of an
*abstract-declarator*, “” is synonymous with “”. the declaration

``` cpp
int printf(const char*, ...);
```

declares a function that can be called with varying numbers and types of
arguments.

``` cpp
printf("hello world");
printf("a=%d b=%d", a, b);
```

However, the first argument must be of a type that can be converted to a
`const` `char*` The standard header `<cstdarg>` contains a mechanism for
accessing arguments passed using the ellipsis (see  [[expr.call]] and 
[[support.runtime]]).

A single name can be used for several different functions in a single
scope; this is function overloading (Clause  [[over]]). All declarations
for a function shall agree exactly in both the return type and the
parameter-type-list. The type of a function is determined using the
following rules. The type of each parameter (including function
parameter packs) is determined from its own *decl-specifier-seq* and
*declarator*. After determining the type of each parameter, any
parameter of type “array of `T`” or “function returning `T`” is adjusted
to be “pointer to `T`” or “pointer to function returning `T`,”
respectively. After producing the list of parameter types, any top-level
*cv-qualifier*s modifying a parameter type are deleted when forming the
function type. The resulting list of transformed parameter types and the
presence or absence of the ellipsis or a function parameter pack is the
function’s *parameter-type-list*. This transformation does not affect
the types of the parameters. For example,
`int(*)(const int p, decltype(p)*)` and `int(*)(int, const int*)` are
identical types.

A *cv-qualifier-seq* or a *ref-qualifier* shall only be part of:

- the function type for a non-static member function,
- the function type to which a pointer to member refers,
- the top-level function type of a function typedef declaration or
  *alias-declaration*,
- the *type-id* in the default argument of a *type-parameter* (
  [[temp.param]]), or
- the *type-id* of a *template-argument* for a *type-parameter* (
  [[temp.names]]).

The effect of a *cv-qualifier-seq* in a function declarator is not the
same as adding cv-qualification on top of the function type. In the
latter case, the cv-qualifiers are ignored. a function type that has a
*cv-qualifier-seq* is not a cv-qualified type; there are no cv-qualified
function types.

``` cpp
typedef void F();
struct S {
  const F f;        // OK: equivalent to: void f();
};
```

The return type, the parameter-type-list, the *ref-qualifier*, and the
*cv-qualifier-seq*, but not the default arguments ([[dcl.fct.default]])
or the exception specification ([[except.spec]]), are part of the
function type. Function types are checked during the assignments and
initializations of pointers to functions, references to functions, and
pointers to member functions.

the declaration

``` cpp
int fseek(FILE*, long, int);
```

declares a function taking three arguments of the specified types, and
returning `int` ([[dcl.type]]).

If the type of a parameter includes a type of the form “pointer to array
of unknown bound of `T`” or “reference to array of unknown bound of
`T`,” the program is ill-formed.[^11] Functions shall not have a return
type of type array or function, although they may have a return type of
type pointer or reference to such things. There shall be no arrays of
functions, although there can be arrays of pointers to functions.

Types shall not be defined in return or parameter types. The type of a
parameter or the return type for a function definition shall not be an
incomplete class type (possibly cv-qualified) unless the function
definition is nested within the *member-specification* for that class
(including definitions in nested classes defined within the class).

A typedef of function type may be used to declare a function but shall
not be used to define a function ([[dcl.fct.def]]).

``` cpp
typedef void F();
F  fv;              // OK: equivalent to void fv();
F  fv { }           // ill-formed
void fv() { }       // OK: definition of fv
```

A typedef of a function type whose declarator includes a
*cv-qualifier-seq* shall be used only to declare the function type for a
non-static member function, to declare the function type to which a
pointer to member refers, or to declare the top-level function type of
another function typedef declaration.

``` cpp
typedef int FIC(int) const;
FIC f;              // ill-formed: does not declare a member function
struct S {
  FIC f;            // OK
};
FIC S::*pm = &S::f; // OK
```

An identifier can optionally be provided as a parameter name; if present
in a function definition ([[dcl.fct.def]]), it names a parameter
(sometimes called “formal argument”). In particular, parameter names are
also optional in function definitions and names used for a parameter in
different declarations and the definition of a function need not be the
same. If a parameter name is present in a function declaration that is
not a definition, it cannot be used outside of its function declarator
because that is the extent of its potential scope (
[[basic.scope.proto]]).

the declaration

``` cpp
int i,
    *pi,
    f(),
    *fpi(int),
    (*pif)(const char*, const char*),
    (*fpif(int))(int);
```

declares an integer `i`, a pointer `pi` to an integer, a function `f`
taking no arguments and returning an integer, a function `fpi` taking an
integer argument and returning a pointer to an integer, a pointer `pif`
to a function which takes two pointers to constant characters and
returns an integer, a function `fpif` taking an integer argument and
returning a pointer to a function that takes an integer argument and
returns an integer. It is especially useful to compare `fpi` and `pif`.
The binding of `*fpi(int)` is `*(fpi(int))`, so the declaration
suggests, and the same construction in an expression requires, the
calling of a function `fpi`, and then using indirection through the
(pointer) result to yield an integer. In the declarator
`(*pif)(const char*, const char*)`, the extra parentheses are necessary
to indicate that indirection through a pointer to a function yields a
function, which is then called. Typedefs and *trailing-return-type*s are
sometimes convenient when the return type of a function is complex. For
example, the function `fpif` above could have been declared

``` cpp
typedef int  IFUNC(int);
IFUNC*  fpif(int);
```

or

``` cpp
auto fpif(int)->int(*)(int)
```

A *trailing-return-type* is most useful for a type that would be more
complicated to specify before the *declarator-id*:

``` cpp
template <class T, class U> auto add(T t, U u) -> decltype(t + u);
```

rather than

``` cpp
template <class T, class U> decltype((*(T*)0) + (*(U*)0)) add(T t, U u);
```

A *declarator-id* or *abstract-declarator* containing an ellipsis shall
only be used in a *parameter-declaration*. Such a
*parameter-declaration* is a parameter pack ([[temp.variadic]]). When
it is part of a *parameter-declaration-clause*, the parameter pack is a
function parameter pack ([[temp.variadic]]). Otherwise, the
*parameter-declaration* is part of a *template-parameter-list* and the
parameter pack is a template parameter pack; see  [[temp.param]]. A
function parameter pack is a pack expansion ([[temp.variadic]]).

``` cpp
template<typename... T> void f(T (* ...t)(int, int));

int add(int, int);
float subtract(int, int);

void g() {
  f(add, subtract);
}
```

There is a syntactic ambiguity when an ellipsis occurs at the end of a
*parameter-declaration-clause* without a preceding comma. In this case,
the ellipsis is parsed as part of the *abstract-declarator* if the type
of the parameter names a template parameter pack that has not been
expanded; otherwise, it is parsed as part of the
*parameter-declaration-clause*.[^12]

### Default arguments <a id="dcl.fct.default">[[dcl.fct.default]]</a>

If an *initializer-clause* is specified in a *parameter-declaration*
this *initializer-clause* is used as a default argument. Default
arguments will be used in calls where trailing arguments are missing.

the declaration

``` cpp
void point(int = 3, int = 4);
```

declares a function that can be called with zero, one, or two arguments
of type `int`. It can be called in any of these ways:

``` cpp
point(1,2);  point(1);  point();
```

The last two calls are equivalent to `point(1,4)` and `point(3,4)`,
respectively.

A default argument shall be specified only in the
*parameter-declaration-clause* of a function declaration or in a
*template-parameter* ([[temp.param]]); in the latter case, the
*initializer-clause* shall be an *assignment-expression*. A default
argument shall not be specified for a parameter pack. If it is specified
in a *parameter-declaration-clause*, it shall not occur within a
*declarator* or *abstract-declarator* of a *parameter-declaration*.[^13]

For non-template functions, default arguments can be added in later
declarations of a function in the same scope. Declarations in different
scopes have completely distinct sets of default arguments. That is,
declarations in inner scopes do not acquire default arguments from
declarations in outer scopes, and vice versa. In a given function
declaration, each parameter subsequent to a parameter with a default
argument shall have a default argument supplied in this or a previous
declaration or shall be a function parameter pack. A default argument
shall not be redefined by a later declaration (not even to the same
value).

``` cpp
void g(int = 0, ...);           // OK, ellipsis is not a parameter so it can follow
                                // a parameter with a default argument
void f(int, int);
void f(int, int = 7);
void h() {
  f(3);                         // OK, calls f(3, 7)
  void f(int = 1, int);         // error: does not use default
                                // from surrounding scope
}
void m() {
  void f(int, int);             // has no defaults
  f(4);                         // error: wrong number of arguments
  void f(int, int = 5);         // OK
  f(4);                         // OK, calls f(4, 5);
  void f(int, int = 5);         // error: cannot redefine, even to
                                // same value
}
void n() {
  f(6);                         // OK, calls f(6, 7)
}
```

For a given inline function defined in different translation units, the
accumulated sets of default arguments at the end of the translation
units shall be the same; see  [[basic.def.odr]]. If a friend declaration
specifies a default argument expression, that declaration shall be a
definition and shall be the only declaration of the function or function
template in the translation unit.

A default argument is implicitly converted (Clause  [[conv]]) to the
parameter type. The default argument has the same semantic constraints
as the initializer in a declaration of a variable of the parameter type,
using the copy-initialization semantics ([[dcl.init]]). The names in
the default argument are bound, and the semantic constraints are
checked, at the point where the default argument appears. Name lookup
and checking of semantic constraints for default arguments in function
templates and in member functions of class templates are performed as
described in  [[temp.inst]]. in the following code, `g` will be called
with the value `f(2)`:

``` cpp
int a = 1;
int f(int);
int g(int x = f(a));            // default argument: f(::a)

void h() {
  a = 2;
  {
  int a = 3;
  g();                          // g(f(::a))
  }
}
```

In member function declarations, names in default arguments are looked
up as described in  [[basic.lookup.unqual]]. Access checking applies to
names in default arguments as described in Clause  [[class.access]].

Except for member functions of class templates, the default arguments in
a member function definition that appears outside of the class
definition are added to the set of default arguments provided by the
member function declaration in the class definition. Default arguments
for a member function of a class template shall be specified on the
initial declaration of the member function within the class template.

``` cpp
class C {
  void f(int i = 3);
  void g(int i, int j = 99);
};

void C::f(int i = 3) {          // error: default argument already
}                               // specified in class scope
void C::g(int i = 88, int j) {  // in this translation unit,
}                               // C::g can be called with no argument
```

Local variables shall not be used in a default argument.

``` cpp
void f() {
  int i;
  extern void g(int x = i);     //error
  // ...
}
```

The keyword `this` shall not be used in a default argument of a member
function.

``` cpp
class A {
  void f(A* p = this) { }       // error
};
```

Default arguments are evaluated each time the function is called. The
order of evaluation of function arguments is unspecified. Consequently,
parameters of a function shall not be used in a default argument, even
if they are not evaluated. Parameters of a function declared before a
default argument are in scope and can hide namespace and class member
names.

``` cpp
int a;
int f(int a, int b = a);            // error: parameter a
                                    // used as default argument
typedef int I;
int g(float I, int b = I(2));       // error: parameter I found
int h(int a, int b = sizeof(a));    // error, parameter a used
                                    // in default argument
```

Similarly, a non-static member shall not be used in a default argument,
even if it is not evaluated, unless it appears as the *id-expression* of
a class member access expression ([[expr.ref]]) or unless it is used to
form a pointer to member ([[expr.unary.op]]). the declaration of
`X::mem1()` in the following example is ill-formed because no object is
supplied for the non-static member `X::a` used as an initializer.

``` cpp
int b;
class X {
  int a;
  int mem1(int i = a);          // error: non-static member a
                                // used as default argument
  int mem2(int i = b);          // OK;  use X::b
  static int b;
};
```

The declaration of `X::mem2()` is meaningful, however, since no object
is needed to access the static member `X::b`. Classes, objects, and
members are described in Clause  [[class]]. A default argument is not
part of the type of a function.

``` cpp
int f(int = 0);

void h() {
  int j = f(1);
  int k = f();                  // OK, means f(0)
}

int (*p1)(int) = &f;
int (*p2)() = &f;               // error: type mismatch
```

When a declaration of a function is introduced by way of a
*using-declaration* ([[namespace.udecl]]), any default argument
information associated with the declaration is made known as well. If
the function is redeclared thereafter in the namespace with additional
default arguments, the additional arguments are also known at any point
following the redeclaration where the *using-declaration* is in scope.

A virtual function call ([[class.virtual]]) uses the default arguments
in the declaration of the virtual function determined by the static type
of the pointer or reference denoting the object. An overriding function
in a derived class does not acquire default arguments from the function
it overrides.

``` cpp
struct A {
  virtual void f(int a = 7);
};
struct B : public A {
  void f(int a);
};
void m() {
  B* pb = new B;
  A* pa = pb;
  pa->f();          // OK, calls pa->B::f(7)
  pb->f();          // error: wrong number of arguments for B::f()
}
```

## Function definitions <a id="dcl.fct.def">[[dcl.fct.def]]</a>

### In general <a id="dcl.fct.def.general">[[dcl.fct.def.general]]</a>

Function definitions have the form

``` bnf
function-definition:
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator virt-specifier-seqₒₚₜ function-body
```

``` bnf
function-body:
    ctor-initializerₒₚₜ compound-statement
    function-try-block
    '= default ;'
    '= delete ;'
```

Any informal reference to the body of a function should be interpreted
as a reference to the non-terminal *function-body*. The optional
*attribute-specifier-seq* in a *function-definition* appertains to the
function. A *virt-specifier-seq* can be part of a *function-definition*
only if it is a *member-declaration* ([[class.mem]]).

The *declarator* in a *function-definition* shall have the form

``` bnf
'D1 (' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ 
   
    \hspace*{ inc}ref-qualifierₒₚₜ exception-specificationₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-typeₒₚₜ
```

as described in  [[dcl.fct]]. A function shall be defined only in
namespace or class scope.

a simple example of a complete function definition is

``` cpp
int max(int a, int b, int c) {
  int m = (a > b) ? a : b;
  return (m > c) ? m : c;
}
```

Here `int` is the *decl-specifier-seq*; `max(int` `a,` `int` `b,` `int`
`c)` is the *declarator*; `{ /* ... */ }` is the *function-body*.

A *ctor-initializer* is used only in a constructor; see  [[class.ctor]]
and  [[class.init]].

A *cv-qualifier-seq* or a *ref-qualifier* (or both) can be part of a
non-static member function declaration, non-static member function
definition, or pointer to member function only ([[dcl.fct]]); see 
[[class.this]].

Unused parameters need not be named. For example,

``` cpp
void print(int a, int) {
  std::printf("a = %d\n",a);
}
```

In the *function-body*, a *function-local predefined variable* denotes a
block-scope object of static storage duration that is implicitly defined
(see  [[basic.scope.local]]).

The function-local predefined variable `__func__` is defined as if a
definition of the form

``` cpp
static const char __func__[] = "function-name";
```

had been provided, where *function-name* is an *implementation-defined*
string. It is unspecified whether such a variable has an address
distinct from that of any other object in the program.[^14]

``` cpp
struct S {
  S() : s(__func__) { }             // OK
  const char *s;
};
void f(const char * s = __func__);  // error: __func__ is undeclared
```

### Explicitly-defaulted functions <a id="dcl.fct.def.default">[[dcl.fct.def.default]]</a>

A function definition of the form:

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator ' = default ;'
```

is called an *explicitly-defaulted* definition. A function that is
explicitly defaulted shall

- be a special member function,
- have the same declared function type (except for possibly differing
  *ref-qualifier*s and except that in the case of a copy constructor or
  copy assignment operator, the parameter type may be “reference to
  non-const `T`”, where `T` is the name of the member function’s class)
  as if it had been implicitly declared, and
- not have default arguments.

An explicitly-defaulted function may be declared `constexpr` only if it
would have been implicitly declared as `constexpr`, and may have an
explicit *exception-specification* only if it is compatible (
[[except.spec]]) with the *exception-specification* on the implicit
declaration. If a function is explicitly defaulted on its first
declaration,

- it is implicitly considered to be `constexpr` if the implicit
  declaration would be,
- it is implicitly considered to have the same *exception-specification*
  as if it had been implicitly declared ([[except.spec]]), and
- in the case of a copy constructor, move constructor, copy assignment
  operator, or move assignment operator, it shall have the same
  parameter type as if it had been implicitly declared.

``` cpp
struct S {
  constexpr S() = default;                  // ill-formed: implicit S() is not constexpr
  S(int a = 0) = default;                   // ill-formed: default argument
  void operator=(const S&) = default;       // ill-formed: non-matching return type
  ~S() throw(int) = default;                // ill-formed: exception specification does not match
private:
  int i;
  S(S&);                                    // OK: private copy constructor
};
S::S(S&) = default;                         // OK: defines copy constructor
```

Explicitly-defaulted functions and implicitly-declared functions are
collectively called *defaulted* functions, and the implementation shall
provide implicit definitions for them ([[class.ctor]] [[class.dtor]],
[[class.copy]]), which might mean defining them as deleted. A special
member function is *user-provided* if it is user-declared and not
explicitly defaulted or deleted on its first declaration. A
user-provided explicitly-defaulted function (i.e., explicitly defaulted
after its first declaration) is defined at the point where it is
explicitly defaulted; if such a function is implicitly defined as
deleted, the program is ill-formed. Declaring a function as defaulted
after its first declaration can provide efficient execution and concise
definition while enabling a stable binary interface to an evolving code
base.

``` cpp
struct trivial {
  trivial() = default;
  trivial(const trivial&) = default;
  trivial(trivial&&) = default;
  trivial& operator=(const trivial&) = default;
  trivial& operator=(trivial&&) = default;
  ~trivial() = default;
};

struct nontrivial1 {
  nontrivial1();
};
nontrivial1::nontrivial1() = default;           // not first declaration
```

### Deleted definitions <a id="dcl.fct.def.delete">[[dcl.fct.def.delete]]</a>

A function definition of the form:

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator ' = delete ;'
```

is called a *deleted definition*. A function with a deleted definition
is also called a *deleted function*.

A program that refers to a deleted function implicitly or explicitly,
other than to declare it, is ill-formed. This includes calling the
function implicitly or explicitly and forming a pointer or
pointer-to-member to the function. It applies even for references in
expressions that are not potentially-evaluated. If a function is
overloaded, it is referenced only if the function is selected by
overload resolution.

One can enforce non-default initialization and non-integral
initialization with

``` cpp
struct onlydouble {
  onlydouble() = delete;              // OK, but redundant
  onlydouble(std::intmax_t) = delete;
  onlydouble(double);
};
```

One can prevent use of a class in certain `new` expressions by using
deleted definitions of a user-declared `operator new` for that class.

``` cpp
struct sometype {
  void *operator new(std::size_t) = delete;
  void *operator new[](std::size_t) = delete;
};
sometype *p = new sometype;     // error, deleted class operator new
sometype *q = new sometype[3];  // error, deleted class operator new[]
```

One can make a class uncopyable, i.e. move-only, by using deleted
definitions of the copy constructor and copy assignment operator, and
then providing defaulted definitions of the move constructor and move
assignment operator.

``` cpp
struct moveonly {
  moveonly() = default;
  moveonly(const moveonly&) = delete;
  moveonly(moveonly&&) = default;
  moveonly& operator=(const moveonly&) = delete;
  moveonly& operator=(moveonly&&) = default;
  ~moveonly() = default;
};
moveonly *p;
moveonly q(*p); // error, deleted copy constructor
```

A deleted function is implicitly inline. The one-definition rule (
[[basic.def.odr]]) applies to deleted definitions. A deleted definition
of a function shall be the first declaration of the function or, for an
explicit specialization of a function template, the first declaration of
that specialization.

``` cpp
struct sometype {
  sometype();
};
sometype::sometype() = delete;      // ill-formed; not first declaration
```

## Initializers <a id="dcl.init">[[dcl.init]]</a>

A declarator can specify an initial value for the identifier being
declared. The identifier designates a variable being initialized. The
process of initialization described in the remainder of  [[dcl.init]]
applies also to initializations specified by other syntactic contexts,
such as the initialization of function parameters with argument
expressions ([[expr.call]]) or the initialization of return values (
[[stmt.return]]).

``` bnf
initializer:
    brace-or-equal-initializer
    '(' expression-list ')'
```

``` bnf
brace-or-equal-initializer:
    '=' initializer-clause
    braced-init-list
```

``` bnf
initializer-clause:
    assignment-expression
    braced-init-list
```

``` bnf
initializer-list:
    initializer-clause '...'ₒₚₜ 
    initializer-list ',' initializer-clause '...'ₒₚₜ
```

``` bnf
braced-init-list:
    '{' initializer-list ',ₒₚₜ ' '}'
    '{' '}'
```

Except for objects declared with the `constexpr` specifier, for which
see  [[dcl.constexpr]], an *initializer* in the definition of a variable
can consist of arbitrary expressions involving literals and previously
declared variables and functions, regardless of the variable’s storage
duration.

``` cpp
int f(int);
int a = 2;
int b = f(a);
int c(b);
```

Default arguments are more restricted; see  [[dcl.fct.default]].

The order of initialization of variables with static storage duration is
described in  [[basic.start]] and  [[stmt.dcl]].

To *zero-initialize* an object or reference of type `T` means:

- if `T` is a scalar type ([[basic.types]]), the object is set to the
  value `0` (zero), taken as an integral constant expression, converted
  to `T`;[^15]
- if `T` is a (possibly cv-qualified) non-union class type, each
  non-static data member and each base-class subobject is
  zero-initialized and padding is initialized to zero bits;
- if `T` is a (possibly cv-qualified) union type, the object’s first
  non-static named data member is zero-initialized and padding is
  initialized to zero bits;
- if `T` is an array type, each element is zero-initialized;
- if `T` is a reference type, no initialization is performed.

To *default-initialize* an object of type `T` means:

- if `T` is a (possibly cv-qualified) class type (Clause  [[class]]),
  the default constructor for `T` is called (and the initialization is
  ill-formed if `T` has no accessible default constructor);
- if `T` is an array type, each element is default-initialized;
- otherwise, no initialization is performed.

If a program calls for the default initialization of an object of a
const-qualified type `T`, `T` shall be a class type with a user-provided
default constructor.

To *value-initialize* an object of type `T` means:

- if `T` is a (possibly cv-qualified) class type (Clause  [[class]])
  with a user-provided constructor ([[class.ctor]]), then the default
  constructor for `T` is called (and the initialization is ill-formed if
  `T` has no accessible default constructor);
- if `T` is a (possibly cv-qualified) non-union class type without a
  user-provided constructor, then the object is zero-initialized and, if
  `T`’s implicitly-declared default constructor is non-trivial, that
  constructor is called.
- if `T` is an array type, then each element is value-initialized;
- otherwise, the object is zero-initialized.

An object that is value-initialized is deemed to be constructed and thus
subject to provisions of this International Standard applying to
“constructed” objects, objects “for which the constructor has
completed,” etc., even if no constructor is invoked for the object’s
initialization.

A program that calls for default-initialization or value-initialization
of an entity of reference type is ill-formed.

Every object of static storage duration is zero-initialized at program
startup before any other initialization takes place. In some cases,
additional initialization is done later.

An object whose initializer is an empty set of parentheses, i.e., `()`,
shall be value-initialized.

Since `()` is not permitted by the syntax for *initializer*,

``` cpp
X a();
```

is not the declaration of an object of class `X`, but the declaration of
a function taking no argument and returning an `X`. The form `()` is
permitted in certain other initialization contexts ([[expr.new]],
[[expr.type.conv]], [[class.base.init]]).

If no initializer is specified for an object, the object is
default-initialized; if no initialization is performed, an object with
automatic or dynamic storage duration has indeterminate value. Objects
with static or thread storage duration are zero-initialized, see 
[[basic.start.init]].

An initializer for a static member is in the scope of the member’s
class.

``` cpp
int a;

struct X {
  static int a;
  static int b;
};

int X::a = 1;
int X::b = a;       // X::b = X::a
```

The form of initialization (using parentheses or `=`) is generally
insignificant, but does matter when the initializer or the entity being
initialized has a class type; see below. If the entity being initialized
does not have class type, the *expression-list* in a parenthesized
initializer shall be a single expression.

The initialization that occurs in the form

``` cpp
T x = a;
```

as well as in argument passing, function return, throwing an exception (
[[except.throw]]), handling an exception ([[except.handle]]), and
aggregate member initialization ([[dcl.init.aggr]]) is called
*copy-initialization*. Copy-initialization may invoke a move (
[[class.copy]]).

The initialization that occurs in the forms

``` cpp
T x(a);
T x{a};
```

as well as in `new` expressions ([[expr.new]]), `static_cast`
expressions ([[expr.static.cast]]), functional notation type
conversions ([[expr.type.conv]]), and base and member initializers (
[[class.base.init]]) is called *direct-initialization*.

The semantics of initializers are as follows. The *destination type* is
the type of the object or reference being initialized and the *source
type* is the type of the initializer expression. If the initializer is
not a single (possibly parenthesized) expression, the source type is not
defined.

- If the initializer is a (non-parenthesized) *braced-init-list*, the
  object or reference is list-initialized ([[dcl.init.list]]).
- If the destination type is a reference type, see  [[dcl.init.ref]].
- If the destination type is an array of characters, an array of
  `char16_t`, an array of `char32_t`, or an array of `wchar_t`, and the
  initializer is a string literal, see  [[dcl.init.string]].
- If the initializer is `()`, the object is value-initialized.
- Otherwise, if the destination type is an array, the program is
  ill-formed.
- If the destination type is a (possibly cv-qualified) class type:
  - If the initialization is direct-initialization, or if it is
    copy-initialization where the cv-unqualified version of the source
    type is the same class as, or a derived class of, the class of the
    destination, constructors are considered. The applicable
    constructors are enumerated ([[over.match.ctor]]), and the best one
    is chosen through overload resolution ([[over.match]]). The
    constructor so selected is called to initialize the object, with the
    initializer expression or *expression-list* as its argument(s). If
    no constructor applies, or the overload resolution is ambiguous, the
    initialization is ill-formed.
  - Otherwise (i.e., for the remaining copy-initialization cases),
    user-defined conversion sequences that can convert from the source
    type to the destination type or (when a conversion function is used)
    to a derived class thereof are enumerated as described in 
    [[over.match.copy]], and the best one is chosen through overload
    resolution ([[over.match]]). If the conversion cannot be done or is
    ambiguous, the initialization is ill-formed. The function selected
    is called with the initializer expression as its argument; if the
    function is a constructor, the call initializes a temporary of the
    cv-unqualified version of the destination type. The temporary is a
    prvalue. The result of the call (which is the temporary for the
    constructor case) is then used to direct-initialize, according to
    the rules above, the object that is the destination of the
    copy-initialization. In certain cases, an implementation is
    permitted to eliminate the copying inherent in this
    direct-initialization by constructing the intermediate result
    directly into the object being initialized; see 
    [[class.temporary]], [[class.copy]].
- Otherwise, if the source type is a (possibly cv-qualified) class type,
  conversion functions are considered. The applicable conversion
  functions are enumerated ([[over.match.conv]]), and the best one is
  chosen through overload resolution ([[over.match]]). The user-defined
  conversion so selected is called to convert the initializer expression
  into the object being initialized. If the conversion cannot be done or
  is ambiguous, the initialization is ill-formed.
- Otherwise, the initial value of the object being initialized is the
  (possibly converted) value of the initializer expression. Standard
  conversions (Clause  [[conv]]) will be used, if necessary, to convert
  the initializer expression to the cv-unqualified version of the
  destination type; no user-defined conversions are considered. If the
  conversion cannot be done, the initialization is ill-formed. An
  expression of type “ `T`” can initialize an object of type “ `T`”
  independently of the cv-qualifiers and .
  ``` cpp
  int a;
  const int b = a;
  int c = b;
  ```

An *initializer-clause* followed by an ellipsis is a pack expansion (
[[temp.variadic]]).

### Aggregates <a id="dcl.init.aggr">[[dcl.init.aggr]]</a>

An *aggregate* is an array or a class (Clause  [[class]]) with no
user-provided constructors ([[class.ctor]]), no
*brace-or-equal-initializer*s for non-static data members (
[[class.mem]]), no private or protected non-static data members (Clause 
[[class.access]]), no base classes (Clause  [[class.derived]]), and no
virtual functions ([[class.virtual]]).

When an aggregate is initialized by an initializer list, as specified
in  [[dcl.init.list]], the elements of the initializer list are taken as
initializers for the members of the aggregate, in increasing subscript
or member order. Each member is copy-initialized from the corresponding
*initializer-clause*. If the *initializer-clause* is an expression and a
narrowing conversion ([[dcl.init.list]]) is required to convert the
expression, the program is ill-formed. If an *initializer-clause* is
itself an initializer list, the member is list-initialized, which will
result in a recursive application of the rules in this section if the
member is an aggregate.

``` cpp
struct A {
  int x;
  struct B {
    int i;
    int j;
  } b;
} a = { 1, { 2, 3 } };
```

initializes `a.x` with 1, `a.b.i` with 2, `a.b.j` with 3.

An aggregate that is a class can also be initialized with a single
expression not enclosed in braces, as described in  [[dcl.init]].

An array of unknown size initialized with a brace-enclosed
*initializer-list* containing `n` *initializer-clause*s, where `n` shall
be greater than zero, is defined as having `n` elements (
[[dcl.array]]).

``` cpp
int x[] = { 1, 3, 5 };
```

declares and initializes `x` as a one-dimensional array that has three
elements since no size was specified and there are three initializers.
An empty initializer list `{}` shall not be used as the
*initializer-clause * for an array of unknown bound.[^16]

Static data members and anonymous bit-fields are not considered members
of the class for purposes of aggregate initialization.

``` cpp
struct A {
  int i;
  static int s;
  int j;
  int :17;
  int k;
} a = { 1, 2, 3 };
```

Here, the second initializer 2 initializes `a.j` and not the static data
member `A::s`, and the third initializer 3 initializes `a.k` and not the
anonymous bit-field before it.

An *initializer-list* is ill-formed if the number of
*initializer-clause*s exceeds the number of members or elements to
initialize.

``` cpp
char cv[4] = { 'a', 's', 'd', 'f', 0 };     // error
```

is ill-formed.

If there are fewer *initializer-clause*s in the list than there are
members in the aggregate, then each member not explicitly initialized
shall be initialized from an empty initializer list (
[[dcl.init.list]]).

``` cpp
struct S { int a; const char* b; int c; };
S ss = { 1, "asdf" };
```

initializes `ss.a` with 1, `ss.b` with `"asdf"`, and `ss.c` with the
value of an expression of the form `int()`, that is, `0`.

If an aggregate class `C` contains a subaggregate member `m` that has no
members for purposes of aggregate initialization, the
*initializer-clause* for `m` shall not be omitted from an
*initializer-list* for an object of type `C` unless the
*initializer-clause*s for all members of `C` following `m` are also
omitted.

``` cpp
struct S { } s;
struct A {
  S s1;
  int i1;
  S s2;
  int i2;
  S s3;
  int i3;
} a = {
  { },      // Required initialization
  0,
  s,        // Required initialization
  0
};          // Initialization not required for A::s3 because A::i3 is also not initialized
```

If an incomplete or empty *initializer-list* leaves a member of
reference type uninitialized, the program is ill-formed.

When initializing a multi-dimensional array, the *initializer-clause*s
initialize the elements with the last (rightmost) index of the array
varying the fastest ([[dcl.array]]).

``` cpp
int x[2][2] = { 3, 1, 4, 2 };
```

initializes `x[0][0]` to `3`, `x[0][1]` to `1`, `x[1][0]` to `4`, and
`x[1][1]` to `2`. On the other hand,

``` cpp
float y[4][3] = {
  { 1 }, { 2 }, { 3 }, { 4 }
};
```

initializes the first column of `y` (regarded as a two-dimensional
array) and leaves the rest zero.

In a declaration of the form

``` cpp
T x = { a };
```

braces can be elided in an *initializer-list* as follows.[^17] If the
*initializer-list* begins with a left brace, then the succeeding
comma-separated list of *initializer-clause*s initializes the members of
a subaggregate; it is erroneous for there to be more
*initializer-clause*s than members. If, however, the *initializer-list*
for a subaggregate does not begin with a left brace, then only enough
*initializer-clause*s from the list are taken to initialize the members
of the subaggregate; any remaining *initializer-clause*s are left to
initialize the next member of the aggregate of which the current
subaggregate is a member.

``` cpp
float y[4][3] = {
  { 1, 3, 5 },
  { 2, 4, 6 },
  { 3, 5, 7 },
};
```

is a completely-braced initialization: 1, 3, and 5 initialize the first
row of the array `y[0]`, namely `y[0][0]`, `y[0][1]`, and `y[0][2]`.
Likewise the next two lines initialize `y[1]` and `y[2]`. The
initializer ends early and therefore `y[3]`s elements are initialized as
if explicitly initialized with an expression of the form `float()`, that
is, are initialized with `0.0`. In the following example, braces in the
*initializer-list* are elided; however the *initializer-list* has the
same effect as the completely-braced *initializer-list* of the above
example,

``` cpp
float y[4][3] = {
  1, 3, 5, 2, 4, 6, 3, 5, 7
};
```

The initializer for `y` begins with a left brace, but the one for `y[0]`
does not, therefore three elements from the list are used. Likewise the
next three are taken successively for `y[1]` and `y[2]`.

All implicit type conversions (Clause  [[conv]]) are considered when
initializing the aggregate member with an *assignment-expression*. If
the *assignment-expression* can initialize a member, the member is
initialized. Otherwise, if the member is itself a subaggregate, brace
elision is assumed and the *assignment-expression* is considered for the
initialization of the first member of the subaggregate. As specified
above, brace elision cannot apply to subaggregates with no members for
purposes of aggregate initialization; an *initializer-clause* for the
entire subobject is required.

``` cpp
struct A {
  int i;
  operator int();
};
struct B {
  A a1, a2;
  int z;
};
A a;
B b = { 4, a, a };
```

Braces are elided around the *initializer-clause* for `b.a1.i`. `b.a1.i`
is initialized with 4, `b.a2` is initialized with `a`, `b.z` is
initialized with whatever `a.operator int()` returns.

An aggregate array or an aggregate class may contain members of a class
type with a user-provided constructor ([[class.ctor]]). Initialization
of these aggregate objects is described in  [[class.expl.init]].

Whether the initialization of aggregates with static storage duration is
static or dynamic is specified in  [[basic.start.init]] and 
[[stmt.dcl]].

When a union is initialized with a brace-enclosed initializer, the
braces shall only contain an *initializer-clause* for the first
non-static data member of the union.

``` cpp
union u { int a; const char* b; };
u a = { 1 };
u b = a;
u c = 1;                        // error
u d = { 0, "asdf" };            // error
u e = { "asdf" };               // error
```

As described above, the braces around the *initializer-clause* for a
union member can be omitted if the union is a member of another
aggregate.

### Character arrays <a id="dcl.init.string">[[dcl.init.string]]</a>

A `char` array (whether plain `char`, `signed` `char`, or `unsigned`
`char`), `char16_t` array, `char32_t` array, or `wchar_t` array can be
initialized by a narrow character literal, `char16_t` string literal,
`char32_t` string literal, or wide string literal, respectively, or by
an appropriately-typed string literal enclosed in braces. Successive
characters of the value of the string literal initialize the elements of
the array.

``` cpp
char msg[] = "Syntax error on line %s\n";
```

shows a character array whose members are initialized with a
*string-literal*. Note that because `'\n'` is a single character and
because a trailing `'\0'` is appended, `sizeof(msg)` is `25`.

There shall not be more initializers than there are array elements.

``` cpp
char cv[4] = "asdf";            // error
```

is ill-formed since there is no space for the implied trailing `'\0'`.

If there are fewer initializers than there are array elements, each
element not explicitly initialized shall be zero-initialized (
[[dcl.init]]).

### References <a id="dcl.init.ref">[[dcl.init.ref]]</a>

A variable declared to be a `T&` or `T&&`, that is, “reference to type
`T`” ([[dcl.ref]]), shall be initialized by an object, or function, of
type `T` or by an object that can be converted into a `T`.

``` cpp
int g(int);
void f() {
  int i;
  int& r = i;                   // r refers to i
  r = 1;                        // the value of i becomes 1
  int* p = &r;                  // p points to i
  int& rr = r;                  // rr refers to what r refers to, that is, to i
  int (&rg)(int) = g;           // rg refers to the function g
  rg(i);                        // calls function g
  int a[3];
  int (&ra)[3] = a;             // ra refers to the array a
  ra[1] = i;                    // modifies a[1]
}
```

A reference cannot be changed to refer to another object after
initialization. Note that initialization of a reference is treated very
differently from assignment to it. Argument passing ([[expr.call]]) and
function value return ([[stmt.return]]) are initializations.

The initializer can be omitted for a reference only in a parameter
declaration ([[dcl.fct]]), in the declaration of a function return
type, in the declaration of a class member within its class definition (
[[class.mem]]), and where the `extern` specifier is explicitly used.

``` cpp
int& r1;                        // error: initializer missing
extern int& r2;                 // OK
```

Given types “ `T1`” and “ `T2`,” “ `T1`” is to “ `T2`” if `T1` is the
same type as `T2`, or `T1` is a base class of `T2`. “ `T1`” is with “
`T2`” if `T1` is reference-related to `T2` and *cv1* is the same
cv-qualification as, or greater cv-qualification than, *cv2*. For
purposes of overload resolution, cases for which *cv1* is greater
cv-qualification than *cv2* are identified as
*reference-compatible with added qualification* (see 
[[over.ics.rank]]). In all cases where the reference-related or
reference-compatible relationship of two types is used to establish the
validity of a reference binding, and `T1` is a base class of `T2`, a
program that necessitates such a binding is ill-formed if `T1` is an
inaccessible (Clause  [[class.access]]) or ambiguous (
[[class.member.lookup]]) base class of `T2`.

A reference to type “*cv1* `T1`” is initialized by an expression of type
“*cv2* `T2`” as follows:

- If the reference is an lvalue reference and the initializer expression
  - is an lvalue (but is not a bit-field), and “ `T1`” is
    reference-compatible with “ `T2`,” or
  - has a class type (i.e., `T2` is a class type), where `T1` is not
    reference-related to `T2`, and can be implicitly converted to an
    lvalue of type “ `T3`,” where “ `T1`” is reference-compatible with “
    `T3`”[^18] (this conversion is selected by enumerating the
    applicable conversion functions ([[over.match.ref]]) and choosing
    the best one through overload resolution ([[over.match]])),

  then the reference is bound to the initializer expression lvalue in
  the first case and to the lvalue result of the conversion in the
  second case (or, in either case, to the appropriate base class
  subobject of the object). The usual lvalue-to-rvalue ([[conv.lval]]),
  array-to-pointer ([[conv.array]]), and function-to-pointer (
  [[conv.func]]) standard conversions are not needed, and therefore are
  suppressed, when such direct bindings to lvalues are done.
  ``` cpp
  double d = 2.0;
  double& rd = d;                 // rd refers to d
  const double& rcd = d;          // rcd refers to d

  struct A { };
  struct B : A { operator int&(); } b;
  A& ra = b;                      // ra refers to A subobject in b
  const A& rca = b;               // rca refers to A subobject in b
  int& ir = B();                  // ir refers to the result of B::operator int&
  ```
- Otherwise, the reference shall be an lvalue reference to a
  non-volatile const type (i.e., *cv1* shall be `const`), or the
  reference shall be an rvalue reference.
  ``` cpp
  double& rd2 = 2.0;              // error: not an lvalue and reference not const
  int  i = 2;
  double& rd3 = i;                // error: type mismatch and reference not const
  ```

  - If the initializer expression
    - is an xvalue, class prvalue, array prvalue or function lvalue and
      “*cv1* `T1`” is reference-compatible with “*cv2* `T2`”, or
    - has a class type (i.e., `T2` is a class type), where `T1` is not
      reference-related to `T2`, and can be implicitly converted to an
      xvalue, class prvalue, or function lvalue of type “*cv3* `T3`”,
      where “*cv1* `T1`” is reference-compatible with “*cv3* `T3`”,

    then the reference is bound to the value of the initializer
    expression in the first case and to the result of the conversion in
    the second case (or, in either case, to an appropriate base class
    subobject). In the second case, if the reference is an rvalue
    reference and the second standard conversion sequence of the
    user-defined conversion sequence includes an lvalue-to-rvalue
    conversion, the program is ill-formed.
    ``` cpp
    struct A { };
    struct B : A { } b;
    extern B f();
    const A& rca2 = f();                // bound to the A subobject of the B rvalue.
    A&& rra = f();                      // same as above
    struct X {
      operator B();
      operator int&();
    } x;
    const A& r = x;                     // bound to the A subobject of the result of the conversion
    int i2 = 42;
    int&& rri = static_cast<int&&>(i2); // bound directly to i2
    B&& rrb = x;                        // bound directly to the result of operator B
    int&& rri2 = X();                   // error: lvalue-to-rvalue conversion applied to the
                                        // result of operator int&
    ```
  - Otherwise, a temporary of type “ `T1`” is created and initialized
    from the initializer expression using the rules for a non-reference
    copy-initialization ([[dcl.init]]). The reference is then bound to
    the temporary. If `T1` is reference-related to `T2`, *cv1* shall be
    the same cv-qualification as, or greater cv-qualification than,
    *cv2*. If `T1` is reference-related to `T2` and the reference is an
    rvalue reference, the initializer expression shall not be an lvalue.
    ``` cpp
    const double& rcd2 = 2;         // rcd2 refers to temporary with value 2.0
    double&& rrd = 2;               // rrd refers to temporary with value 2.0
    const volatile int cvi = 1;
    const int& r2 = cvi;            // error: type qualifiers dropped
    double d2 = 1.0;
    double&& rrd2 = d2;             // error: copying lvalue of related type
    int i3 = 2;
    double&& rrd3 = i3;             // rrd3 refers to temporary with value 2.0
    ```

In all cases except the last (i.e., creating and initializing a
temporary from the initializer expression), the reference is said to
*bind directly* to the initializer expression.

[[class.temporary]] describes the lifetime of temporaries bound to
references.

### List-initialization <a id="dcl.init.list">[[dcl.init.list]]</a>

*List-initialization* is initialization of an object or reference from a
*braced-init-list*. Such an initializer is called an *initializer list*,
and the comma-separated *initializer-clause*s of the list are called the
*elements* of the initializer list. An initializer list may be empty.
List-initialization can occur in direct-initialization or
copy-initialization contexts; list-initialization in a
direct-initialization context is called *direct-list-initialization* and
list-initialization in a copy-initialization context is called
*copy-list-initialization*. List-initialization can be used

- as the initializer in a variable definition ([[dcl.init]])
- as the initializer in a new expression ([[expr.new]])
- in a return statement ([[stmt.return]])
- as a function argument ([[expr.call]])
- as a subscript ([[expr.sub]])
- as an argument to a constructor invocation ([[dcl.init]], 
  [[expr.type.conv]])
- as an initializer for a non-static data member ([[class.mem]])
- in a *mem-initializer* ([[class.base.init]])
- on the right-hand side of an assignment ([[expr.ass]])

``` cpp
int a = {1};
std::complex<double> z{1,2};
new std::vector<std::string>{"once", "upon", "a", "time"};  // 4 string elements
f( {"Nicholas","Annemarie"} );  // pass list of two elements
return { "Norah" };             // return list of one element
int* e {};                      // initialization to zero / null pointer
x = double{1};                  // explicitly construct a double
std::map<std::string,int> anim = { {"bear",4}, {"cassowary",2}, {"tiger",7} };
```

A constructor is an *initializer-list constructor* if its first
parameter is of type `std::initializer_list<E>` or reference to possibly
cv-qualified `std::initializer_list<E>` for some type `E`, and either
there are no other parameters or else all other parameters have default
arguments ([[dcl.fct.default]]). Initializer-list constructors are
favored over other constructors in list-initialization (
[[over.match.list]]).The template `std::initializer_list` is not
predefined; if the header `<initializer_list>` is not included prior to
a use of `std::initializer_list` — even an implicit use in which the
type is not named ([[dcl.spec.auto]]) — the program is ill-formed.

List-initialization of an object or reference of type `T` is defined as
follows:

- If the initializer list has no elements and `T` is a class type with a
  default constructor, the object is value-initialized.
- Otherwise, if `T` is an aggregate, aggregate initialization is
  performed ([[dcl.init.aggr]]).
  ``` cpp
  double ad[] = { 1, 2.0 };           // OK
  int ai[] = { 1, 2.0 };              // error: narrowing

  struct S2 {
    int m1;
    double m2, m3;
  };
  S2 s21 = { 1, 2, 3.0 };             // OK
  S2 s22 { 1.0, 2, 3 };               // error: narrowing
  S2 s23 { };                         // OK: default to 0,0,0
  ```
- Otherwise, if `T` is a specialization of `std::initializer_list<E>`,
  an `initializer_list` object is constructed as described below and
  used to initialize the object according to the rules for
  initialization of an object from a class of the same type (
  [[dcl.init]]).
- Otherwise, if `T` is a class type, constructors are considered. The
  applicable constructors are enumerated and the best one is chosen
  through overload resolution ([[over.match]],  [[over.match.list]]).
  If a narrowing conversion (see below) is required to convert any of
  the arguments, the program is ill-formed.
  ``` cpp
  struct S {
    S(std::initializer_list<double>); // #1
    S(std::initializer_list<int>);    // #2
    S();                              // #3
    // ...
  };
  S s1 = { 1.0, 2.0, 3.0 };           // invoke #1
  S s2 = { 1, 2, 3 };                 // invoke #2
  S s3 = { };                         // invoke #3
  ```

  ``` cpp
  struct Map {
    Map(std::initializer_list<std::pair<std::string,int>>);
  };
  Map ship = {{"Sophie",14}, {"Surprise",28}};
  ```

  ``` cpp
  struct S {
    // no initializer-list constructors
    S(int, double, double);           // #1
    S();                              // #2
    // ...
  };
  S s1 = { 1, 2, 3.0 };               // OK: invoke #1
  S s2 { 1.0, 2, 3 };                 // error: narrowing
  S s3 { };                           // OK: invoke #2
  ```
- Otherwise, if `T` is a reference type, a prvalue temporary of the type
  referenced by `T` is list-initialized, and the reference is bound to
  that temporary. As usual, the binding will fail and the program is
  ill-formed if the reference type is an lvalue reference to a non-const
  type.
  ``` cpp
  struct S {
    S(std::initializer_list<double>); // #1
    S(const std::string&);            // #2
    // ...
  };
  const S& r1 = { 1, 2, 3.0 };        // OK: invoke #1
  const S& r2 { "Spinach" };          // OK: invoke #2
  S& r3 = { 1, 2, 3 };                // error: initializer is not an lvalue
  const int& i1 = { 1 };              // OK
  const int& i2 = { 1.1 };            // error: narrowing
  const int (&iar)[2] = { 1, 2 };     // OK: iar is bound to temporary array
  ```
- Otherwise, if the initializer list has a single element, the object or
  reference is initialized from that element; if a narrowing conversion
  (see below) is required to convert the element to `T`, the program is
  ill-formed.
  ``` cpp
  int x1 {2};                         // OK
  int x2 {2.0};                       // error: narrowing
  ```
- Otherwise, if the initializer list has no elements, the object is
  value-initialized.
  ``` cpp
  int** pp {};                        // initialized to null pointer
  ```
- Otherwise, the program is ill-formed.
  ``` cpp
  struct A { int i; int j; };
  A a1 { 1, 2 };                      // aggregate initialization
  A a2 { 1.2 };                       // error: narrowing
  struct B {
    B(std::initializer_list<int>);
  };
  B b1 { 1, 2 };                      // creates initializer_list<int> and calls constructor
  B b2 { 1, 2.0 };                    // error: narrowing
  struct C {
    C(int i, double j);
  };
  C c1 = { 1, 2.2 };                  // calls constructor with arguments (1, 2.2)
  C c2 = { 1.1, 2 };                  // error: narrowing

  int j { 1 };                        // initialize to 1
  int k { };                          // initialize to 0
  ```

Within the *initializer-list* of a *braced-init-list*, the
*initializer-clause*s, including any that result from pack expansions (
[[temp.variadic]]), are evaluated in the order in which they appear.
That is, every value computation and side effect associated with a given
*initializer-clause* is sequenced before every value computation and
side effect associated with any *initializer-clause* that follows it in
the comma-separated list of the *initializer-list*. This evaluation
ordering holds regardless of the semantics of the initialization; for
example, it applies when the elements of the *initializer-list* are
interpreted as arguments of a constructor call, even though ordinarily
there are no sequencing constraints on the arguments of a call.

An object of type `std::initializer_list<E>` is constructed from an
initializer list as if the implementation allocated an array of N
elements of type `E`, where N is the number of elements in the
initializer list. Each element of that array is copy-initialized with
the corresponding element of the initializer list, and the
`std::initializer_list<E>` object is constructed to refer to that array.
If a narrowing conversion is required to initialize any of the elements,
the program is ill-formed.

``` cpp
struct X {
  X(std::initializer_list<double> v);
};
X x{ 1,2,3 };
```

The initialization will be implemented in a way roughly equivalent to
this:

``` cpp
double __a[3] = {double{1}, double{2}, double{3}};
X x(std::initializer_list<double>(__a, __a+3));
```

assuming that the implementation can construct an `initializer_list`
object with a pair of pointers.

The lifetime of the array is the same as that of the `initializer_list`
object.

``` cpp
typedef std::complex<double> cmplx;
std::vector<cmplx> v1 = { 1, 2, 3 };

void f() {
  std::vector<cmplx> v2{ 1, 2, 3 };
  std::initializer_list<int> i3 = { 1, 2, 3 };
}
```

For `v1` and `v2`, the `initializer_list` object and array created for
`{ 1, 2, 3 }` have full-expression lifetime. For `i3`, the
`initializer_list` object and array have automatic lifetime. The
implementation is free to allocate the array in read-only memory if an
explicit array with the same initializer could be so allocated.

A *narrowing conversion* is an implicit conversion

- from a floating-point type to an integer type, or
- from `long double` to `double` or `float`, or from `double` to
  `float`, except where the source is a constant expression and the
  actual value after conversion is within the range of values that can
  be represented (even if it cannot be represented exactly), or
- from an integer type or unscoped enumeration type to a floating-point
  type, except where the source is a constant expression and the actual
  value after conversion will fit into the target type and will produce
  the original value when converted back to the original type, or
- from an integer type or unscoped enumeration type to an integer type
  that cannot represent all the values of the original type, except
  where the source is a constant expression and the actual value after
  conversion will fit into the target type and will produce the original
  value when converted back to the original type.

As indicated above, such conversions are not allowed at the top level in
list-initializations.

``` cpp
int x = 999;              // x is not a constant expression
const int y = 999;
const int z = 99;
char c1 = x;              // OK, though it might narrow (in this case, it does narrow)
char c2{x};               // error: might narrow
char c3{y};               // error: narrows (assuming char is 8 bits)
char c4{z};               // OK: no narrowing needed
unsigned char uc1 = {5};  // OK: no narrowing needed
unsigned char uc2 = {-1}; // error: narrows
unsigned int ui1 = {-1};  // error: narrows
signed int si1 =
  { (unsigned int)-1 };   // error: narrows
int ii = {2.0};           // error: narrows
float f1 { x };           // error: might narrow
float f2 { 7 };           // OK: 7 can be exactly represented as a float
int f(int);
int a[] =
  { 2, f(2), f(2.0) };    // OK: the double-to-int conversion is not at the top level
```

<!-- Link reference definitions -->
[basic.compound]: basic.md#basic.compound
[basic.def]: basic.md#basic.def
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.elab]: basic.md#basic.lookup.elab
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.udir]: basic.md#basic.lookup.udir
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.lval]: basic.md#basic.lval
[basic.namespace]: #basic.namespace
[basic.scope]: basic.md#basic.scope
[basic.scope.local]: basic.md#basic.scope.local
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.scope.proto]: basic.md#basic.scope.proto
[basic.start]: basic.md#basic.start
[basic.start.init]: basic.md#basic.start.init
[basic.stc]: basic.md#basic.stc
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[class]: class.md#class
[class.access]: class.md#class.access
[class.base.init]: special.md#class.base.init
[class.bit]: class.md#class.bit
[class.conv]: special.md#class.conv
[class.conv.ctor]: special.md#class.conv.ctor
[class.conv.fct]: special.md#class.conv.fct
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.derived]: class.md#class.derived
[class.dtor]: special.md#class.dtor
[class.expl.init]: special.md#class.expl.init
[class.friend]: class.md#class.friend
[class.inhctor]: special.md#class.inhctor
[class.init]: special.md#class.init
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.mfct.non-static]: class.md#class.mfct.non-static
[class.name]: class.md#class.name
[class.qual]: basic.md#class.qual
[class.static]: class.md#class.static
[class.static.data]: class.md#class.static.data
[class.temporary]: special.md#class.temporary
[class.this]: class.md#class.this
[class.union]: class.md#class.union
[class.virtual]: class.md#class.virtual
[conv]: conv.md#conv
[conv.array]: conv.md#conv.array
[conv.func]: conv.md#conv.func
[conv.lval]: conv.md#conv.lval
[conv.prom]: conv.md#conv.prom
[conv.ptr]: conv.md#conv.ptr
[dcl.align]: #dcl.align
[dcl.ambig.res]: #dcl.ambig.res
[dcl.array]: #dcl.array
[dcl.asm]: #dcl.asm
[dcl.attr]: #dcl.attr
[dcl.attr.depend]: #dcl.attr.depend
[dcl.attr.grammar]: #dcl.attr.grammar
[dcl.attr.noreturn]: #dcl.attr.noreturn
[dcl.constexpr]: #dcl.constexpr
[dcl.dcl]: #dcl.dcl
[dcl.decl]: #dcl.decl
[dcl.enum]: #dcl.enum
[dcl.fct]: #dcl.fct
[dcl.fct.def]: #dcl.fct.def
[dcl.fct.def.default]: #dcl.fct.def.default
[dcl.fct.def.delete]: #dcl.fct.def.delete
[dcl.fct.def.general]: #dcl.fct.def.general
[dcl.fct.default]: #dcl.fct.default
[dcl.fct.spec]: #dcl.fct.spec
[dcl.friend]: #dcl.friend
[dcl.init]: #dcl.init
[dcl.init.aggr]: #dcl.init.aggr
[dcl.init.list]: #dcl.init.list
[dcl.init.ref]: #dcl.init.ref
[dcl.init.string]: #dcl.init.string
[dcl.link]: #dcl.link
[dcl.meaning]: #dcl.meaning
[dcl.mptr]: #dcl.mptr
[dcl.name]: #dcl.name
[dcl.ptr]: #dcl.ptr
[dcl.ref]: #dcl.ref
[dcl.spec]: #dcl.spec
[dcl.spec.auto]: #dcl.spec.auto
[dcl.stc]: #dcl.stc
[dcl.type]: #dcl.type
[dcl.type.cv]: #dcl.type.cv
[dcl.type.elab]: #dcl.type.elab
[dcl.type.simple]: #dcl.type.simple
[dcl.typedef]: #dcl.typedef
[depr.register]: future.md#depr.register
[except.handle]: except.md#except.handle
[except.spec]: except.md#except.spec
[except.throw]: except.md#except.throw
[expr]: expr.md#expr
[expr.alignof]: expr.md#expr.alignof
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.const.cast]: expr.md#expr.const.cast
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.new]: expr.md#expr.new
[expr.prim]: expr.md#expr.prim
[expr.ref]: expr.md#expr.ref
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.type.conv]: expr.md#expr.type.conv
[expr.unary]: expr.md#expr.unary
[expr.unary.op]: expr.md#expr.unary.op
[global.names]: library.md#global.names
[intro.compliance]: intro.md#intro.compliance
[intro.execution]: intro.md#intro.execution
[intro.multithread]: intro.md#intro.multithread
[lex.charset]: lex.md#lex.charset
[lex.digraph]: lex.md#lex.digraph
[lex.key]: lex.md#lex.key
[lex.name]: lex.md#lex.name
[namespace.alias]: #namespace.alias
[namespace.def]: #namespace.def
[namespace.memdef]: #namespace.memdef
[namespace.qual]: basic.md#namespace.qual
[namespace.udecl]: #namespace.udecl
[namespace.udir]: #namespace.udir
[namespace.unnamed]: #namespace.unnamed
[over]: over.md#over
[over.ics.rank]: over.md#over.ics.rank
[over.match]: over.md#over.match
[over.match.conv]: over.md#over.match.conv
[over.match.copy]: over.md#over.match.copy
[over.match.ctor]: over.md#over.match.ctor
[over.match.list]: over.md#over.match.list
[over.match.ref]: over.md#over.match.ref
[over.oper]: over.md#over.oper
[over.sub]: over.md#over.sub
[stmt.ambig]: stmt.md#stmt.ambig
[stmt.block]: stmt.md#stmt.block
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.for]: stmt.md#stmt.for
[stmt.iter]: stmt.md#stmt.iter
[stmt.return]: stmt.md#stmt.return
[stmt.select]: stmt.md#stmt.select
[stmt.stmt]: stmt.md#stmt.stmt
[support.runtime]: language.md#support.runtime
[tab:simple.type.specifiers]: #tab:simple.type.specifiers
[temp]: temp.md#temp
[temp.arg]: temp.md#temp.arg
[temp.arg.type]: temp.md#temp.arg.type
[temp.class.spec]: temp.md#temp.class.spec
[temp.deduct.call]: temp.md#temp.deduct.call
[temp.dep]: temp.md#temp.dep
[temp.expl.spec]: temp.md#temp.expl.spec
[temp.explicit]: temp.md#temp.explicit
[temp.inst]: temp.md#temp.inst
[temp.mem]: temp.md#temp.mem
[temp.names]: temp.md#temp.names
[temp.param]: temp.md#temp.param
[temp.res]: temp.md#temp.res
[temp.spec]: temp.md#temp.spec
[temp.variadic]: temp.md#temp.variadic

[^1]: The “implicit int” rule of C is no longer supported.

[^2]: The inline keyword has no effect on the linkage of a function.

[^3]: The resulting converted value will include an lvalue-to-rvalue
    conversion ([[conv.lval]]) if the corresponding copy-initialization
    requires one.

[^4]: There is no special provision for a *decl-specifier-seq* that
    lacks a *type-specifier* or that has a *type-specifier* that only
    specifies *cv-qualifier*s. The “implicit int” rule of C is no longer
    supported.

[^5]: This set of values is used to define promotion and conversion
    semantics for the enumeration type. It does not preclude an
    expression of enumeration type from having a value that falls
    outside this range.

[^6]: Although entities in an unnamed namespace might have external
    linkage, they are effectively qualified by a name unique to their
    translation unit and therefore can never be seen from any other
    translation unit.

[^7]: this implies that the name of the class or function is
    unqualified.

[^8]: During name lookup in a class hierarchy, some ambiguities may be
    resolved by considering whether one member hides the other along
    some paths ([[class.member.lookup]]). There is no such
    disambiguation when considering the set of names found as a result
    of following *using-directive*s.

[^9]: A declaration with several declarators is usually equivalent to
    the corresponding sequence of declarations each with a single
    declarator. That is

    `T  D1, D2, ... Dn;`

    is usually equivalent to

    `T  D1; T D2; ... T Dn;`

    where `T` is a *decl-specifier-seq* and each `Di` is an
    *init-declarator*. An exception occurs when a name introduced by one
    of the *declarator*s hides a type name used by the
    *decl-specifiers*, so that when the same *decl-specifiers* are used
    in a subsequent declaration, they do not have the same meaning, as
    in

    `struct S { ... };`  
    `S S, T; \textrm{// declare two instances of \tcode{struct S}}`

    which is not equivalent to

    `struct S { ... };`  
    `S S;`  
    `S T; \textrm{// error}`

    Another exception occurs when `T` is `auto` ([[dcl.spec.auto]]),
    for example:

    `auto i = 1, j = 2.0; \textrm{// error: deduced types for \tcode{i} and \tcode{j} do not match}`  
    as opposed to  
    `auto i = 1;    \textrm{// OK: \tcode{i} deduced to have type \tcode{int}}`  
    `auto j = 2.0;  \textrm{// OK: \tcode{j} deduced to have type \tcode{double}}`

[^10]: As indicated by syntax, cv-qualifiers are a significant component
    in function return types.

[^11]: This excludes parameters of type “ `T2`” where `T2` is “pointer
    to array of unknown bound of `T`” and where means any sequence of
    “pointer to” and “array of” derived declarator types. This exclusion
    applies to the parameters of the function, and if a parameter is a
    pointer to function or pointer to member function then to its
    parameters also, etc.

[^12]: One can explicitly disambiguate the parse either by introducing a
    comma (so the ellipsis will be parsed as part of the
    *parameter-declaration-clause*) or by introducing a name for the
    parameter (so the ellipsis will be parsed as part of the
    *declarator-id*).

[^13]: This means that default arguments cannot appear, for example, in
    declarations of pointers to functions, references to functions, or
    `typedef` declarations.

[^14]: Implementations are permitted to provide additional predefined
    variables with names that are reserved to the implementation (
    [[global.names]]). If a predefined variable is not odr-used (
    [[basic.def.odr]]), its string value need not be present in the
    program image.

[^15]: As specified in  [[conv.ptr]], converting an integral constant
    expression whose value is `0` to a pointer type results in a null
    pointer value.

[^16]: The syntax provides for empty *initializer-list*s, but
    nonetheless C++does not have zero length arrays.

[^17]: Braces cannot be elided in other uses of list-initialization.

[^18]: This requires a conversion function ([[class.conv.fct]])
    returning a reference type.
