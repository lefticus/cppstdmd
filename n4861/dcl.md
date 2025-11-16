# Declarations <a id="dcl.dcl">[[dcl.dcl]]</a>

## Preamble <a id="dcl.pre">[[dcl.pre]]</a>

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
    nodeclspec-function-declaration
    function-definition
    template-declaration
    deduction-guide
    explicit-instantiation
    explicit-specialization
    export-declaration
    linkage-specification
    namespace-definition
    empty-declaration
    attribute-declaration
    module-import-declaration
```

``` bnf
block-declaration:
    simple-declaration
    asm-declaration
    namespace-alias-definition
    using-declaration
    using-enum-declaration
    using-directive
    static_assert-declaration
    alias-declaration
    opaque-enum-declaration
```

``` bnf
nodeclspec-function-declaration:
    attribute-specifier-seqₒₚₜ declarator ';'
```

``` bnf
alias-declaration:
    using identifier attribute-specifier-seqₒₚₜ '=' defining-type-id ';'
```

``` bnf
simple-declaration:
    decl-specifier-seq init-declarator-listₒₚₜ ';'
    attribute-specifier-seq decl-specifier-seq init-declarator-list ';'
    attribute-specifier-seqₒₚₜ decl-specifier-seq ref-qualifierₒₚₜ '[' identifier-list ']' initializer ';'
```

``` bnf
static_assert-declaration:
  static_assert '(' constant-expression ')' ';'
  static_assert '(' constant-expression ',' string-literal ')' ';'
```

``` bnf
empty-declaration:
    ';'
```

``` bnf
attribute-declaration:
    attribute-specifier-seq ';'
```

[*Note 1*: *asm-declaration*s are described in  [[dcl.asm]], and
*linkage-specification*s are described in  [[dcl.link]];
*function-definition*s are described in  [[dcl.fct.def]] and
*template-declaration*s and *deduction-guide*s are described in
[[temp.deduct.guide]]; *namespace-definition*s are described in 
[[namespace.def]], *using-declaration*s are described in 
[[namespace.udecl]] and *using-directive*s are described in 
[[namespace.udir]]. — *end note*]

A *simple-declaration* or *nodeclspec-function-declaration* of the form

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ init-declarator-listₒₚₜ ';'
```

is divided into three parts. Attributes are described in  [[dcl.attr]].
*decl-specifier*s, the principal components of a *decl-specifier-seq*,
are described in  [[dcl.spec]]. *declarator*s, the components of an
*init-declarator-list*, are described in [[dcl.decl]]. The
*attribute-specifier-seq* appertains to each of the entities declared by
the *declarator*s of the *init-declarator-list*.

[*Note 2*: In the declaration for an entity, attributes appertaining to
that entity may appear at the start of the declaration and after the
*declarator-id* for that declaration. — *end note*]

[*Example 1*:

``` cpp
[[noreturn]] void f [[noreturn]] ();    // OK
```

— *end example*]

Except where otherwise specified, the meaning of an
*attribute-declaration* is *implementation-defined*.

A declaration occurs in a scope [[basic.scope]]; the scope rules are
summarized in  [[basic.lookup]]. A declaration that declares a function
or defines a class, namespace, template, or function also has one or
more scopes nested within it. These nested scopes, in turn, can have
declarations nested within them. Unless otherwise stated, utterances in
[[dcl.dcl]] about components in, of, or contained by a declaration or
subcomponent thereof refer only to those components of the declaration
that are *not* nested within scopes nested within the declaration.

In a *simple-declaration*, the optional *init-declarator-list* can be
omitted only when declaring a class [[class]] or enumeration
[[dcl.enum]], that is, when the *decl-specifier-seq* contains either a
*class-specifier*, an *elaborated-type-specifier* with a *class-key*
[[class.name]], or an *enum-specifier*. In these cases and whenever a
*class-specifier* or *enum-specifier* is present in the
*decl-specifier-seq*, the identifiers in these specifiers are among the
names being declared by the declaration (as *class-name*s, *enum-name*s,
or *enumerator*s, depending on the syntax). In such cases, the
*decl-specifier-seq* shall introduce one or more names into the program,
or shall redeclare a name introduced by a previous declaration.

[*Example 2*:

``` cpp
enum { };           // error
typedef class { };  // error
```

— *end example*]

In a *static_assert-declaration*, the *constant-expression* shall be a
contextually converted constant expression of type `bool`
[[expr.const]]. If the value of the expression when so converted is
`true`, the declaration has no effect. Otherwise, the program is
ill-formed, and the resulting diagnostic message [[intro.compliance]]
shall include the text of the *string-literal*, if one is supplied,
except that characters not in the basic source character set
[[lex.charset]] are not required to appear in the diagnostic message.

[*Example 3*:

``` cpp
static_assert(sizeof(int) == sizeof(void*), "wrong pointer size");
```

— *end example*]

An *empty-declaration* has no effect.

A *simple-declaration* with an *identifier-list* is called a *structured
binding declaration* [[dcl.struct.bind]]. If the *decl-specifier-seq*
contains any *decl-specifier* other than `static`, `thread_local`,
`auto` [[dcl.spec.auto]], or *cv-qualifier*s, the program is ill-formed.
The *initializer* shall be of the form “`=` *assignment-expression*”, of
the form “`{` *assignment-expression* `}`”, or of the form “`(`
*assignment-expression* `)`”, where the *assignment-expression* is of
array or non-union class type.

Each *init-declarator* in the *init-declarator-list* contains exactly
one *declarator-id*, which is the name declared by that
*init-declarator* and hence one of the names declared by the
declaration. The *defining-type-specifier*s [[dcl.type]] in the
*decl-specifier-seq* and the recursive *declarator* structure of the
*init-declarator* describe a type [[dcl.meaning]], which is then
associated with the name being declared by the *init-declarator*.

If the *decl-specifier-seq* contains the `typedef` specifier, the
declaration is called a *typedef declaration* and the name of each
*init-declarator* is declared to be a *typedef-name*, synonymous with
its associated type [[dcl.typedef]]. If the *decl-specifier-seq*
contains no `typedef` specifier, the declaration is called a
*function declaration* if the type associated with the name is a
function type [[dcl.fct]] and an *object declaration* otherwise.

Syntactic components beyond those found in the general form of
declaration are added to a function declaration to make a
*function-definition*. An object declaration, however, is also a
definition unless it contains the `extern` specifier and has no
initializer [[basic.def]]. An object definition causes storage of
appropriate size and alignment to be reserved and any appropriate
initialization [[dcl.init]] to be done.

A *nodeclspec-function-declaration* shall declare a constructor,
destructor, or conversion function.

[*Note 3*: A *nodeclspec-function-declaration* can only be used in a
*template-declaration* [[temp.pre]], *explicit-instantiation*
[[temp.explicit]], or *explicit-specialization*
[[temp.expl.spec]]. — *end note*]

## Specifiers <a id="dcl.spec">[[dcl.spec]]</a>

The specifiers that can be used in a declaration are

``` bnf
decl-specifier:
    storage-class-specifier
    defining-type-specifier
    function-specifier
    friend
    typedef
    constexpr
    consteval
    constinit
    inline
```

``` bnf
decl-specifier-seq:
    decl-specifier attribute-specifier-seqₒₚₜ
    decl-specifier decl-specifier-seq
```

The optional *attribute-specifier-seq* in a *decl-specifier-seq*
appertains to the type determined by the preceding *decl-specifier*s
[[dcl.meaning]]. The *attribute-specifier-seq* affects the type only for
the declaration it appears in, not other declarations involving the same
type.

Each *decl-specifier* shall appear at most once in a complete
*decl-specifier-seq*, except that `long` may appear twice. At most one
of the `constexpr`, `consteval`, and `constinit` keywords shall appear
in a *decl-specifier-seq*.

If a *type-name* is encountered while parsing a *decl-specifier-seq*, it
is interpreted as part of the *decl-specifier-seq* if and only if there
is no previous *defining-type-specifier* other than a *cv-qualifier* in
the *decl-specifier-seq*. The sequence shall be self-consistent as
described below.

[*Example 1*:

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

— *end example*]

[*Note 1*:

Since `signed`, `unsigned`, `long`, and `short` by default imply `int`,
a *type-name* appearing after one of those specifiers is treated as the
name being (re)declared.

[*Example 2*:

``` cpp
void h(unsigned Pc);            // void h(unsigned int)
void k(unsigned int Pc);        // void k(unsigned int)
```

— *end example*]

— *end note*]

### Storage class specifiers <a id="dcl.stc">[[dcl.stc]]</a>

The storage class specifiers are

``` bnf
storage-class-specifier:
    static
    thread_local
    extern
    mutable
```

At most one *storage-class-specifier* shall appear in a given
*decl-specifier-seq*, except that `thread_local` may appear with
`static` or `extern`. If `thread_local` appears in any declaration of a
variable it shall be present in all declarations of that entity. If a
*storage-class-specifier* appears in a *decl-specifier-seq*, there can
be no `typedef` specifier in the same *decl-specifier-seq* and the
*init-declarator-list* or *member-declarator-list* of the declaration
shall not be empty (except for an anonymous union declared in a named
namespace or in the global namespace, which shall be declared `static`
[[class.union.anon]]). The *storage-class-specifier* applies to the name
declared by each *init-declarator* in the list and not to any names
declared by other specifiers.

[*Note 1*: See [[temp.expl.spec]] and [[temp.explicit]] for
restrictions in explicit specializations and explicit instantiations,
respectively. — *end note*]

[*Note 2*: A variable declared without a *storage-class-specifier* at
block scope or declared as a function parameter has automatic storage
duration by default [[basic.stc.auto]]. — *end note*]

The `thread_local` specifier indicates that the named entity has thread
storage duration [[basic.stc.thread]]. It shall be applied only to the
declaration of a variable of namespace or block scope, to a structured
binding declaration [[dcl.struct.bind]], or to the declaration of a
static data member. When `thread_local` is applied to a variable of
block scope the *storage-class-specifier* `static` is implied if no
other *storage-class-specifier* appears in the *decl-specifier-seq*.

The `static` specifier shall be applied only to the declaration of a
variable or function, to a structured binding declaration
[[dcl.struct.bind]], or to the declaration of an anonymous union
[[class.union.anon]]. There can be no `static` function declarations
within a block, nor any `static` function parameters. A `static`
specifier used in the declaration of a variable declares the variable to
have static storage duration [[basic.stc.static]], unless accompanied by
the `thread_local` specifier, which declares the variable to have thread
storage duration [[basic.stc.thread]]. A `static` specifier can be used
in declarations of class members;  [[class.static]] describes its
effect. For the linkage of a name declared with a `static` specifier,
see  [[basic.link]].

The `extern` specifier shall be applied only to the declaration of a
variable or function. The `extern` specifier shall not be used in the
declaration of a class member or function parameter. For the linkage of
a name declared with an `extern` specifier, see  [[basic.link]].

[*Note 3*: The `extern` keyword can also be used in
*explicit-instantiation*s and *linkage-specification*s, but it is not a
*storage-class-specifier* in such contexts. — *end note*]

The linkages implied by successive declarations for a given entity shall
agree. That is, within a given scope, each declaration declaring the
same variable name or the same overloading of a function name shall
imply the same linkage.

[*Example 1*:

``` cpp
static char* f();               // f() has internal linkage
char* f()                       // f() still has internal linkage
  { ... }

char* g();                      // g() has external linkage
static char* g()                // error: inconsistent linkage
  { ... }

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

— *end example*]

The name of a declared but undefined class can be used in an `extern`
declaration. Such a declaration can only be used in ways that do not
require a complete class type.

[*Example 2*:

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

— *end example*]

The `mutable` specifier shall appear only in the declaration of a
non-static data member [[class.mem]] whose type is neither
const-qualified nor a reference type.

[*Example 3*:

``` cpp
class X {
  mutable const int* p;         // OK
  mutable int* const q;         // error
};
```

— *end example*]

[*Note 4*: The `mutable` specifier on a class data member nullifies a
`const` specifier applied to the containing class object and permits
modification of the mutable class member even though the rest of the
object is const ([[basic.type.qualifier]],
[[dcl.type.cv]]). — *end note*]

### Function specifiers <a id="dcl.fct.spec">[[dcl.fct.spec]]</a>

A *function-specifier* can be used only in a function declaration.

``` bnf
function-specifier:
    virtual
    explicit-specifier
```

``` bnf
explicit-specifier:
    explicit '(' constant-expression ')'
    explicit
```

The `virtual` specifier shall be used only in the initial declaration of
a non-static class member function; see  [[class.virtual]].

An *explicit-specifier* shall be used only in the declaration of a
constructor or conversion function within its class definition; see 
[[class.conv.ctor]] and  [[class.conv.fct]].

In an *explicit-specifier*, the *constant-expression*, if supplied,
shall be a contextually converted constant expression of type `bool`
[[expr.const]]. The *explicit-specifier* `explicit` without a
*constant-expression* is equivalent to the *explicit-specifier*
`explicit(true)`. If the constant expression evaluates to `true`, the
function is explicit. Otherwise, the function is not explicit. A `(`
token that follows `explicit` is parsed as part of the
*explicit-specifier*.

### The `typedef` specifier <a id="dcl.typedef">[[dcl.typedef]]</a>

Declarations containing the *decl-specifier* `typedef` declare
identifiers that can be used later for naming fundamental
[[basic.fundamental]] or compound [[basic.compound]] types. The
`typedef` specifier shall not be combined in a *decl-specifier-seq* with
any other kind of specifier except a *defining-type-specifier*, and it
shall not be used in the *decl-specifier-seq* of a
*parameter-declaration* [[dcl.fct]] nor in the *decl-specifier-seq* of a
*function-definition* [[dcl.fct.def]]. If a `typedef` specifier appears
in a declaration without a *declarator*, the program is ill-formed.

``` bnf
typedef-name:
    identifier
    simple-template-id
```

A name declared with the `typedef` specifier becomes a *typedef-name*. A
*typedef-name* names the type associated with the *identifier*
[[dcl.decl]] or *simple-template-id* [[temp.pre]]; a *typedef-name* is
thus a synonym for another type. A *typedef-name* does not introduce a
new type the way a class declaration [[class.name]] or enum declaration
[[dcl.enum]] does.

[*Example 1*:

After

``` cpp
typedef int MILES, *KLICKSP;
```

the constructions

``` cpp
MILES distance;
extern KLICKSP metricp;
```

are all correct declarations; the type of `distance` is `int` and that
of `metricp` is “pointer to `int`”.

— *end example*]

A *typedef-name* can also be introduced by an *alias-declaration*. The
*identifier* following the `using` keyword becomes a *typedef-name* and
the optional *attribute-specifier-seq* following the *identifier*
appertains to that *typedef-name*. Such a *typedef-name* has the same
semantics as if it were introduced by the `typedef` specifier. In
particular, it does not define a new type.

[*Example 2*:

``` cpp
using handler_t = void (*)(int);
extern handler_t ignore;
extern void (*ignore)(int);         // redeclare ignore
using cell = pair<void*, cell*>;    // error
```

— *end example*]

The *defining-type-specifier-seq* of the *defining-type-id* shall not
define a class or enumeration if the *alias-declaration* is the
*declaration* of a *template-declaration*.

In a given non-class scope, a `typedef` specifier can be used to
redeclare the name of any type declared in that scope to refer to the
type to which it already refers.

[*Example 3*:

``` cpp
typedef struct s { ... } s;
typedef int I;
typedef int I;
typedef I I;
```

— *end example*]

In a given class scope, a `typedef` specifier can be used to redeclare
any *class-name* declared in that scope that is not also a
*typedef-name* to refer to the type to which it already refers.

[*Example 4*:

``` cpp
struct S {
  typedef struct A { } A;       // OK
  typedef struct B B;           // OK
  typedef A A;                  // error
};
```

— *end example*]

If a `typedef` specifier is used to redeclare in a given scope an entity
that can be referenced using an *elaborated-type-specifier*, the entity
can continue to be referenced by an *elaborated-type-specifier* or as an
enumeration or class name in an enumeration or class definition
respectively.

[*Example 5*:

``` cpp
struct S;
typedef struct S S;
int main() {
  struct S* p;                  // OK
}
struct S { };                   // OK
```

— *end example*]

In a given scope, a `typedef` specifier shall not be used to redeclare
the name of any type declared in that scope to refer to a different
type.

[*Example 6*:

``` cpp
class complex { ... };
typedef int complex;            // error: redefinition
```

— *end example*]

Similarly, in a given scope, a class or enumeration shall not be
declared with the same name as a *typedef-name* that is declared in that
scope and refers to a type other than the class or enumeration itself.

[*Example 7*:

``` cpp
typedef int complex;
class complex { ... };    // error: redefinition
```

— *end example*]

A *simple-template-id* is only a *typedef-name* if its *template-name*
names an alias template or a template *template-parameter*.

[*Note 1*: A *simple-template-id* that names a class template
specialization is a *class-name* [[class.name]]. If a *typedef-name* is
used to identify the subject of an *elaborated-type-specifier*
[[dcl.type.elab]], a class definition [[class]], a constructor
declaration [[class.ctor]], or a destructor declaration [[class.dtor]],
the program is ill-formed. — *end note*]

[*Example 8*:

``` cpp
struct S {
  S();
  ~S();
};

typedef struct S T;

S a = T();                      // OK
struct T * p;                   // error
```

— *end example*]

If the typedef declaration defines an unnamed class or enumeration, the
first *typedef-name* declared by the declaration to be that type is used
to denote the type for linkage purposes only [[basic.link]].

[*Note 2*: A typedef declaration involving a *lambda-expression* does
not itself define the associated closure type, and so the closure type
is not given a name for linkage purposes. — *end note*]

[*Example 9*:

``` cpp
typedef struct { } *ps, S;      // S is the class name for linkage purposes
typedef decltype([]{}) C;       // the closure type has no name for linkage purposes
```

— *end example*]

An unnamed class with a typedef name for linkage purposes shall not

- declare any members other than non-static data members, member
  enumerations, or member classes,
- have any base classes or default member initializers, or
- contain a *lambda-expression*,

and all member classes shall also satisfy these requirements
(recursively).

[*Example 10*:

``` cpp
typedef struct {
  int f() {}
} X;                            // error: struct with typedef name for linkage has member functions
```

— *end example*]

### The `friend` specifier <a id="dcl.friend">[[dcl.friend]]</a>

The `friend` specifier is used to specify access to class members; see 
[[class.friend]].

### The `constexpr` and `consteval` specifiers <a id="dcl.constexpr">[[dcl.constexpr]]</a>

The `constexpr` specifier shall be applied only to the definition of a
variable or variable template or the declaration of a function or
function template. The `consteval` specifier shall be applied only to
the declaration of a function or function template. A function or static
data member declared with the `constexpr` or `consteval` specifier is
implicitly an inline function or variable [[dcl.inline]]. If any
declaration of a function or function template has a `constexpr` or
`consteval` specifier, then all its declarations shall contain the same
specifier.

[*Note 1*: An explicit specialization can differ from the template
declaration with respect to the `constexpr` or `consteval`
specifier. — *end note*]

[*Note 2*: Function parameters cannot be declared
`constexpr`. — *end note*]

[*Example 1*:

``` cpp
constexpr void square(int &x);  // OK: declaration
constexpr int bufsz = 1024;     // OK: definition
constexpr struct pixel {        // error: pixel is a type
  int x;
  int y;
  constexpr pixel(int);         // OK: declaration
};
constexpr pixel::pixel(int a)
  : x(a), y(x)                  // OK: definition
  { square(x); }
constexpr pixel small(2);       // error: square not defined, so small(2)
                                // not constant[expr.const] so constexpr not satisfied

constexpr void square(int &x) { // OK: definition
  x *= x;
}
constexpr pixel large(4);       // OK: square defined
int next(constexpr int x) {     // error: not for parameters
     return x + 1;
}
extern constexpr int memsz;     // error: not a definition
```

— *end example*]

A `constexpr` or `consteval` specifier used in the declaration of a
function declares that function to be a *constexpr function*. A function
or constructor declared with the `consteval` specifier is called an
*immediate function*. A destructor, an allocation function, or a
deallocation function shall not be declared with the `consteval`
specifier.

The definition of a constexpr function shall satisfy the following
requirements:

- its return type (if any) shall be a literal type;
- each of its parameter types shall be a literal type;
- it shall not be a coroutine [[dcl.fct.def.coroutine]];
- if the function is a constructor or destructor, its class shall not
  have any virtual base classes;
- its *function-body* shall not enclose [[stmt.pre]]
  - a `goto` statement,
  - an identifier label [[stmt.label]],
  - a definition of a variable of non-literal type or of static or
    thread storage duration.

  \[*Note 1*: A *function-body* that is `= delete` or `= default`
  encloses none of the above. — *end note*]

[*Example 2*:

``` cpp
constexpr int square(int x)
  { return x * x; }             // OK
constexpr long long_max()
  { return 2147483647; }        // OK
constexpr int abs(int x) {
  if (x < 0)
    x = -x;
  return x;                     // OK
}
constexpr int first(int n) {
  static int value = n;         // error: variable has static storage duration
  return value;
}
constexpr int uninit() {
  struct { int a; } s;
  return s.a;                   // error: uninitialized read of s.a
}
constexpr int prev(int x)
  { return --x; }               // OK
constexpr int g(int x, int n) { // OK
  int r = 1;
  while (--n > 0) r *= x;
  return r;
}
```

— *end example*]

The definition of a constexpr constructor whose *function-body* is not
`= delete` shall additionally satisfy the following requirements:

- for a non-delegating constructor, every constructor selected to
  initialize non-static data members and base class subobjects shall be
  a constexpr constructor;
- for a delegating constructor, the target constructor shall be a
  constexpr constructor.

[*Example 3*:

``` cpp
struct Length {
  constexpr explicit Length(int i = 0) : val(i) { }
private:
  int val;
};
```

— *end example*]

The definition of a constexpr destructor whose *function-body* is not
`= delete` shall additionally satisfy the following requirement:

- for every subobject of class type or (possibly multi-dimensional)
  array thereof, that class type shall have a constexpr destructor.

For a constexpr function or constexpr constructor that is neither
defaulted nor a template, if no argument values exist such that an
invocation of the function or constructor could be an evaluated
subexpression of a core constant expression [[expr.const]], or, for a
constructor, an evaluated subexpression of the initialization
full-expression of some constant-initialized object
[[basic.start.static]], the program is ill-formed, no diagnostic
required.

[*Example 4*:

``` cpp
constexpr int f(bool b)
  { return b ? throw 0 : 0; }           // OK
constexpr int f() { return f(true); }   // ill-formed, no diagnostic required

struct B {
  constexpr B(int x) : i(0) { }         // x is unused
  int i;
};

int global;

struct D : B {
  constexpr D() : B(global) { }         // ill-formed, no diagnostic required
                                        // lvalue-to-rvalue conversion on non-constant global
};
```

— *end example*]

If the instantiated template specialization of a constexpr function
template or member function of a class template would fail to satisfy
the requirements for a constexpr function, that specialization is still
a constexpr function, even though a call to such a function cannot
appear in a constant expression. If no specialization of the template
would satisfy the requirements for a constexpr function when considered
as a non-template function, the template is ill-formed, no diagnostic
required.

An invocation of a constexpr function in a given context produces the
same result as an invocation of an equivalent non-constexpr function in
the same context in all respects except that

- an invocation of a constexpr function can appear in a constant
  expression [[expr.const]] and
- copy elision is not performed in a constant expression
  [[class.copy.elision]].

[*Note 3*: Declaring a function constexpr can change whether an
expression is a constant expression. This can indirectly cause calls to
`std::is_constant_evaluated` within an invocation of the function to
produce a different value. — *end note*]

The `constexpr` and `consteval` specifiers have no effect on the type of
a constexpr function.

[*Example 5*:

``` cpp
constexpr int bar(int x, int y)         // OK
    { return x + y + x*y; }
// ...
int bar(int x, int y)                   // error: redefinition of bar
    { return x * 2 + 3 * y; }
```

— *end example*]

A `constexpr` specifier used in an object declaration declares the
object as const. Such an object shall have literal type and shall be
initialized. In any `constexpr` variable declaration, the
full-expression of the initialization shall be a constant expression
[[expr.const]]. A `constexpr` variable shall have constant destruction.

[*Example 6*:

``` cpp
struct pixel {
  int x, y;
};
constexpr pixel ur = { 1294, 1024 };    // OK
constexpr pixel origin;                 // error: initializer missing
```

— *end example*]

### The `constinit` specifier <a id="dcl.constinit">[[dcl.constinit]]</a>

The `constinit` specifier shall be applied only to a declaration of a
variable with static or thread storage duration. If the specifier is
applied to any declaration of a variable, it shall be applied to the
initializing declaration. No diagnostic is required if no `constinit`
declaration is reachable at the point of the initializing declaration.

If a variable declared with the `constinit` specifier has dynamic
initialization [[basic.start.dynamic]], the program is ill-formed.

[*Note 1*: The `constinit` specifier ensures that the variable is
initialized during static initialization
[[basic.start.static]]. — *end note*]

[*Example 1*:

``` cpp
const char * g() { return "dynamic initialization"; }
constexpr const char * f(bool p) { return p ? "constant initializer" : g(); }
constinit const char * c = f(true);     // OK
constinit const char * d = f(false);    // error
```

— *end example*]

### The `inline` specifier <a id="dcl.inline">[[dcl.inline]]</a>

The `inline` specifier shall be applied only to the declaration of a
variable or function.

A function declaration ([[dcl.fct]], [[class.mfct]], [[class.friend]])
with an `inline` specifier declares an *inline function*. The inline
specifier indicates to the implementation that inline substitution of
the function body at the point of call is to be preferred to the usual
function call mechanism. An implementation is not required to perform
this inline substitution at the point of call; however, even if this
inline substitution is omitted, the other rules for inline functions
specified in this subclause shall still be respected.

[*Note 1*: The `inline` keyword has no effect on the linkage of a
function. In certain cases, an inline function cannot use names with
internal linkage; see  [[basic.link]]. — *end note*]

A variable declaration with an `inline` specifier declares an
*inline variable*.

The `inline` specifier shall not appear on a block scope declaration or
on the declaration of a function parameter. If the `inline` specifier is
used in a friend function declaration, that declaration shall be a
definition or the function shall have previously been declared inline.

If a definition of a function or variable is reachable at the point of
its first declaration as inline, the program is ill-formed. If a
function or variable with external or module linkage is declared inline
in one definition domain, an inline declaration of it shall be reachable
from the end of every definition domain in which it is declared; no
diagnostic is required.

[*Note 2*: A call to an inline function or a use of an inline variable
may be encountered before its definition becomes reachable in a
translation unit. — *end note*]

[*Note 3*: An inline function or variable with external or module
linkage has the same address in all translation units. A `static` local
variable in an inline function with external or module linkage always
refers to the same object. A type defined within the body of an inline
function with external or module linkage is the same type in every
translation unit. — *end note*]

If an inline function or variable that is attached to a named module is
declared in a definition domain, it shall be defined in that domain.

[*Note 4*: A constexpr function [[dcl.constexpr]] is implicitly inline.
In the global module, a function defined within a class definition is
implicitly inline ([[class.mfct]], [[class.friend]]). — *end note*]

### Type specifiers <a id="dcl.type">[[dcl.type]]</a>

The type-specifiers are

``` bnf
type-specifier:
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
defining-type-specifier:
    type-specifier
    class-specifier
    enum-specifier
```

``` bnf
defining-type-specifier-seq:
  defining-type-specifier attribute-specifier-seqₒₚₜ
  defining-type-specifier defining-type-specifier-seq
```

The optional *attribute-specifier-seq* in a *type-specifier-seq* or a
*defining-type-specifier-seq* appertains to the type denoted by the
preceding *type-specifier*s or *defining-type-specifier*s
[[dcl.meaning]]. The *attribute-specifier-seq* affects the type only for
the declaration it appears in, not other declarations involving the same
type.

As a general rule, at most one *defining-type-specifier* is allowed in
the complete *decl-specifier-seq* of a *declaration* or in a
*defining-type-specifier-seq*, and at most one *type-specifier* is
allowed in a *type-specifier-seq*. The only exceptions to this rule are
the following:

- `const` can be combined with any type specifier except itself.
- `volatile` can be combined with any type specifier except itself.
- `signed` or `unsigned` can be combined with `char`, `long`, `short`,
  or `int`.
- `short` or `long` can be combined with `int`.
- `long` can be combined with `double`.
- `long` can be combined with `long`.

Except in a declaration of a constructor, destructor, or conversion
function, at least one *defining-type-specifier* that is not a
*cv-qualifier* shall appear in a complete *type-specifier-seq* or a
complete *decl-specifier-seq*.[^1]

[*Note 1*: *enum-specifier*s, *class-specifier*s, and
*typename-specifier*s are discussed in [[dcl.enum]], [[class]], and
[[temp.res]], respectively. The remaining *type-specifier*s are
discussed in the rest of this subclause. — *end note*]

#### The  <a id="dcl.type.cv">[[dcl.type.cv]]</a>

There are two *cv-qualifier*s, `const` and `volatile`. Each
*cv-qualifier* shall appear at most once in a *cv-qualifier-seq*. If a
*cv-qualifier* appears in a *decl-specifier-seq*, the
*init-declarator-list* or *member-declarator-list* of the declaration
shall not be empty.

[*Note 1*:  [[basic.type.qualifier]] and [[dcl.fct]] describe how
cv-qualifiers affect object and function types. — *end note*]

Redundant cv-qualifications are ignored.

[*Note 2*: For example, these could be introduced by
typedefs. — *end note*]

[*Note 3*: Declaring a variable `const` can affect its linkage
[[dcl.stc]] and its usability in constant expressions [[expr.const]]. As
described in  [[dcl.init]], the definition of an object or subobject of
const-qualified type must specify an initializer or be subject to
default-initialization. — *end note*]

A pointer or reference to a cv-qualified type need not actually point or
refer to a cv-qualified object, but it is treated as if it does; a
const-qualified access path cannot be used to modify an object even if
the object referenced is a non-const object and can be modified through
some other access path.

[*Note 4*: Cv-qualifiers are supported by the type system so that they
cannot be subverted without casting [[expr.const.cast]]. — *end note*]

Any attempt to modify ([[expr.ass]], [[expr.post.incr]],
[[expr.pre.incr]]) a const object [[basic.type.qualifier]] during its
lifetime [[basic.life]] results in undefined behavior.

[*Example 1*:

``` cpp
const int ci = 3;                       // cv-qualified (initialized as required)
ci = 4;                                 // error: attempt to modify const

int i = 2;                              // not cv-qualified
const int* cip;                         // pointer to const int
cip = &i;                               // OK: cv-qualified access path to unqualified
*cip = 4;                               // error: attempt to modify through ptr to const

int* ip;
ip = const_cast<int*>(cip);             // cast needed to convert const int* to int*
*ip = 4;                                // defined: *ip points to i, a non-const object

const int* ciq = new const int (3);     // initialized as required
int* iq = const_cast<int*>(ciq);        // cast required
*iq = 4;                                // undefined behavior: modifies a const object
```

For another example,

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
y.x.i++;                                // well-formed: mutable member can be modified
y.x.j++;                                // error: const-qualified member modified
Y* p = const_cast<Y*>(&y);              // cast away const-ness of y
p->x.i = 99;                            // well-formed: mutable member can be modified
p->x.j = 99;                            // undefined behavior: modifies a const subobject
```

— *end example*]

The semantics of an access through a volatile glvalue are
*implementation-defined*. If an attempt is made to access an object
defined with a volatile-qualified type through the use of a non-volatile
glvalue, the behavior is undefined.

[*Note 5*: `volatile` is a hint to the implementation to avoid
aggressive optimization involving the object because the value of the
object might be changed by means undetectable by an implementation.
Furthermore, for some implementations, `volatile` might indicate that
special hardware instructions are required to access the object. See 
[[intro.execution]] for detailed semantics. In general, the semantics of
`volatile` are intended to be the same in C++ as they are in
C. — *end note*]

#### Simple type specifiers <a id="dcl.type.simple">[[dcl.type.simple]]</a>

The simple type specifiers are

``` bnf
simple-type-specifier:
    nested-name-specifierₒₚₜ type-name
    nested-name-specifier template simple-template-id
    decltype-specifier
    placeholder-type-specifier
    nested-name-specifierₒₚₜ template-name
    char
    char8_t
    char16_t
    char32_t
    wchar_t
    bool
    short
    int
    long
    signed
    unsigned
    float
    double
    void
```

``` bnf
type-name:
    class-name
    enum-name
    typedef-name
```

A *placeholder-type-specifier* is a placeholder for a type to be deduced
[[dcl.spec.auto]]. A *type-specifier* of the form `typename`ₒₚₜ
*nested-name-specifier*ₒₚₜ *template-name* is a placeholder for a
deduced class type [[dcl.type.class.deduct]]. The
*nested-name-specifier*, if any, shall be non-dependent and the
*template-name* shall name a deducible template. A *deducible template*
is either a class template or is an alias template whose
*defining-type-id* is of the form

``` bnf
typenameₒₚₜ nested-name-specifierₒₚₜ templateₒₚₜ simple-template-id
```

where the *nested-name-specifier* (if any) is non-dependent and the
*template-name* of the *simple-template-id* names a deducible template.

[*Note 1*: An injected-class-name is never interpreted as a
*template-name* in contexts where class template argument deduction
would be performed [[temp.local]]. — *end note*]

The other *simple-type-specifier*s specify either a previously-declared
type, a type determined from an expression, or one of the fundamental
types [[basic.fundamental]]. [[dcl.type.simple]] summarizes the valid
combinations of *simple-type-specifier*s and the types they specify.

**Table: *simple-type-specifier*{s} and the types they specify**

| Specifier(s)                 | Type                                              |
| ---------------------------- | ------------------------------------------------- |
| *type-name*                  | the type named                                    |
| *simple-template-id*         | the type as defined in~ [[temp.names]]            |
| *decltype-specifier*         | the type as defined in~ [[dcl.type.decltype]]     |
| *placeholder-type-specifier* | the type as defined in~ [[dcl.spec.auto]]         |
| *template-name*              | the type as defined in~ [[dcl.type.class.deduct]] |
| `char`                       | ```char`''                                        |
| `unsigned char`              | ```unsigned char`''                               |
| `signed char`                | ```signed char`''                                 |
| `char8_t`                    | ```char8_t`''                                     |
| `char16_t`                   | ```char16_t`''                                    |
| `char32_t`                   | ```char32_t`''                                    |
| `bool`                       | ```bool`''                                        |
| `unsigned`                   | ```unsigned int`''                                |
| `unsigned int`               | ```unsigned int`''                                |
| `signed`                     | ```int`''                                         |
| `signed int`                 | ```int`''                                         |
| `int`                        | ```int`''                                         |
| `unsigned short int`         | ```unsigned short int`''                          |
| `unsigned short`             | ```unsigned short int`''                          |
| `unsigned long int`          | ```unsigned long int`''                           |
| `unsigned long`              | ```unsigned long int`''                           |
| `unsigned long long int`     | ```unsigned long long int`''                      |
| `unsigned long long`         | ```unsigned long long int`''                      |
| `signed long int`            | ```long int`''                                    |
| `signed long`                | ```long int`''                                    |
| `signed long long int`       | ```long long int`''                               |
| `signed long long`           | ```long long int`''                               |
| `long long int`              | ```long long int`''                               |
| `long long`                  | ```long long int`''                               |
| `long int`                   | ```long int`''                                    |
| `long`                       | ```long int`''                                    |
| `signed short int`           | ```short int`''                                   |
| `signed short`               | ```short int`''                                   |
| `short int`                  | ```short int`''                                   |
| `short`                      | ```short int`''                                   |
| `wchar_t`                    | ```wchar_t`''                                     |
| `float`                      | ```float`''                                       |
| `double`                     | ```double`''                                      |
| `long double`                | ```long double`''                                 |
| `void`                       | ```void`''                                        |


When multiple *simple-type-specifier*s are allowed, they can be freely
intermixed with other *decl-specifier*s in any order.

[*Note 2*: It is *implementation-defined* whether objects of `char`
type are represented as signed or unsigned quantities. The `signed`
specifier forces `char` objects to be signed; it is redundant in other
contexts. — *end note*]

#### Elaborated type specifiers <a id="dcl.type.elab">[[dcl.type.elab]]</a>

``` bnf
elaborated-type-specifier:
    class-key attribute-specifier-seqₒₚₜ nested-name-specifierₒₚₜ identifier
    class-key simple-template-id
    class-key nested-name-specifier templateₒₚₜ simple-template-id
    elaborated-enum-specifier
```

``` bnf
elaborated-enum-specifier:
    enum nested-name-specifierₒₚₜ identifier
```

An *attribute-specifier-seq* shall not appear in an
*elaborated-type-specifier* unless the latter is the sole constituent of
a declaration. If an *elaborated-type-specifier* is the sole constituent
of a declaration, the declaration is ill-formed unless it is an explicit
specialization [[temp.expl.spec]], an explicit instantiation
[[temp.explicit]] or it has one of the following forms:

``` bnf
class-key attribute-specifier-seqₒₚₜ identifier ';'
friend class-key '::ₒₚₜ' identifier ';'
friend class-key '::ₒₚₜ' simple-template-id ';'
friend class-key nested-name-specifier identifier ';'
friend class-key nested-name-specifier templateₒₚₜ simple-template-id ';'
```

In the first case, the *attribute-specifier-seq*, if any, appertains to
the class being declared; the attributes in the
*attribute-specifier-seq* are thereafter considered attributes of the
class whenever it is named.

[*Note 1*:  [[basic.lookup.elab]] describes how name lookup proceeds
for the *identifier* in an *elaborated-type-specifier*. — *end note*]

If the *identifier* or *simple-template-id* resolves to a *class-name*
or *enum-name*, the *elaborated-type-specifier* introduces it into the
declaration the same way a *simple-type-specifier* introduces its
*type-name* [[dcl.type.simple]]. If the *identifier* or
*simple-template-id* resolves to a *typedef-name* ([[dcl.typedef]],
[[temp.names]]), the *elaborated-type-specifier* is ill-formed.

[*Note 2*:

This implies that, within a class template with a template
*type-parameter* `T`, the declaration

``` cpp
friend class T;
```

is ill-formed. However, the similar declaration `friend T;` is allowed
[[class.friend]].

— *end note*]

The *class-key* or `enum` keyword present in the
*elaborated-type-specifier* shall agree in kind with the declaration to
which the name in the *elaborated-type-specifier* refers. This rule also
applies to the form of *elaborated-type-specifier* that declares a
*class-name* or friend class since it can be construed as referring to
the definition of the class. Thus, in any *elaborated-type-specifier*,
the `enum` keyword shall be used to refer to an enumeration
[[dcl.enum]], the `union` *class-key* shall be used to refer to a union
[[class.union]], and either the `class` or `struct` *class-key* shall be
used to refer to a non-union class [[class.pre]].

[*Example 1*:

``` cpp
enum class E { a, b };
enum E x = E::a;                // OK
struct S { } s;
class S* p = &s;                // OK
```

— *end example*]

#### Decltype specifiers <a id="dcl.type.decltype">[[dcl.type.decltype]]</a>

``` bnf
decltype-specifier:
  decltype '(' expression ')'
```

For an expression E, the type denoted by `decltype(E)` is defined as
follows:

- if E is an unparenthesized *id-expression* naming a structured binding
  [[dcl.struct.bind]], `decltype(E)` is the referenced type as given in
  the specification of the structured binding declaration;
- otherwise, if E is an unparenthesized *id-expression* naming a
  non-type *template-parameter* [[temp.param]], `decltype(E)` is the
  type of the *template-parameter* after performing any necessary type
  deduction ([[dcl.spec.auto]], [[dcl.type.class.deduct]]);
- otherwise, if E is an unparenthesized *id-expression* or an
  unparenthesized class member access [[expr.ref]], `decltype(E)` is the
  type of the entity named by E. If there is no such entity, or if E
  names a set of overloaded functions, the program is ill-formed;
- otherwise, if E is an xvalue, `decltype(E)` is `T&&`, where `T` is the
  type of E;
- otherwise, if E is an lvalue, `decltype(E)` is `T&`, where `T` is the
  type of E;
- otherwise, `decltype(E)` is the type of E.

The operand of the `decltype` specifier is an unevaluated operand
[[expr.prop]].

[*Example 1*:

``` cpp
const int&& foo();
int i;
struct A { double x; };
const A* a = new A();
decltype(foo()) x1 = 17;        // type is const int&&
decltype(i) x2;                 // type is int
decltype(a->x) x3;              // type is double
decltype((a->x)) x4 = x3;       // type is const double&
```

— *end example*]

[*Note 1*: The rules for determining types involving `decltype(auto)`
are specified in  [[dcl.spec.auto]]. — *end note*]

If the operand of a *decltype-specifier* is a prvalue and is not a
(possibly parenthesized) immediate invocation [[expr.const]], the
temporary materialization conversion is not applied [[conv.rval]] and no
result object is provided for the prvalue. The type of the prvalue may
be incomplete or an abstract class type.

[*Note 2*: As a result, storage is not allocated for the prvalue and it
is not destroyed. Thus, a class type is not instantiated as a result of
being the type of a function call in this context. In this context, the
common purpose of writing the expression is merely to refer to its type.
In that sense, a *decltype-specifier* is analogous to a use of a
*typedef-name*, so the usual reasons for requiring a complete type do
not apply. In particular, it is not necessary to allocate storage for a
temporary object or to enforce the semantic constraints associated with
invoking the type’s destructor. — *end note*]

[*Note 3*: Unlike the preceding rule, parentheses have no special
meaning in this context. — *end note*]

[*Example 2*:

``` cpp
template<class T> struct A { ~A() = delete; };
template<class T> auto h()
  -> A<T>;
template<class T> auto i(T)     // identity
  -> T;
template<class T> auto f(T)     // #1
  -> decltype(i(h<T>()));       // forces completion of A<T> and implicitly uses A<T>::~A()
                                // for the temporary introduced by the use of h().
                                // (A temporary is not introduced as a result of the use of i().)
template<class T> auto f(T)     // #2
  -> void;
auto g() -> void {
  f(42);                        // OK: calls #2. (#1 is not a viable candidate: type deduction
                                // fails[temp.deduct] because A<int>::~A() is implicitly used in its
                                // decltype-specifier)
}
template<class T> auto q(T)
  -> decltype((h<T>()));        // does not force completion of A<T>; A<T>::~A() is not implicitly
                                // used within the context of this decltype-specifier
void r() {
  q(42);                        // error: deduction against q succeeds, so overload resolution selects
                                // the specialization ``q(T) -> decltype((h<T>()))'' with T=int;
                                // the return type is A<int>, so a temporary is introduced and its
                                // destructor is used, so the program is ill-formed
}
```

— *end example*]

#### Placeholder type specifiers <a id="dcl.spec.auto">[[dcl.spec.auto]]</a>

``` bnf
placeholder-type-specifier:
  type-constraintₒₚₜ auto
  type-constraintₒₚₜ decltype '(' auto ')'
```

A *placeholder-type-specifier* designates a placeholder type that will
be replaced later by deduction from an initializer.

A *placeholder-type-specifier* of the form *type-constraint*ₒₚₜ `auto`
can be used as a *decl-specifier* of the *decl-specifier-seq* of a
*parameter-declaration* of a function declaration or *lambda-expression*
and, if it is not the `auto` *type-specifier* introducing a
*trailing-return-type* (see below), is a *generic parameter type
placeholder* of the function declaration or *lambda-expression*.

[*Note 1*: Having a generic parameter type placeholder signifies that
the function is an abbreviated function template [[dcl.fct]] or the
lambda is a generic lambda [[expr.prim.lambda]]. — *end note*]

The placeholder type can appear with a function declarator in the
*decl-specifier-seq*, *type-specifier-seq*, *conversion-function-id*, or
*trailing-return-type*, in any context where such a declarator is valid.
If the function declarator includes a *trailing-return-type*
[[dcl.fct]], that *trailing-return-type* specifies the declared return
type of the function. Otherwise, the function declarator shall declare a
function. If the declared return type of the function contains a
placeholder type, the return type of the function is deduced from
non-discarded `return` statements, if any, in the body of the function
[[stmt.if]].

The type of a variable declared using a placeholder type is deduced from
its initializer. This use is allowed in an initializing declaration
[[dcl.init]] of a variable. The placeholder type shall appear as one of
the *decl-specifier*s in the *decl-specifier-seq* and the
*decl-specifier-seq* shall be followed by one or more *declarator*s,
each of which shall be followed by a non-empty *initializer*. In an
*initializer* of the form

``` cpp
( expression-list )
```

the *expression-list* shall be a single *assignment-expression*.

[*Example 1*:

``` cpp
auto x = 5;                     // OK: x has type int
const auto *v = &x, u = 6;      // OK: v has type const int*, u has type const int
static auto y = 0.0;            // OK: y has type double
auto int r;                     // error: auto is not a storage-class-specifier
auto f() -> int;                // OK: f returns int
auto g() { return 0.0; }        // OK: g returns double
auto h();                       // OK: h's return type will be deduced when it is defined
```

— *end example*]

The `auto` *type-specifier* can also be used to introduce a structured
binding declaration [[dcl.struct.bind]].

A placeholder type can also be used in the *type-specifier-seq* in the
*new-type-id* or *type-id* of a *new-expression* [[expr.new]] and as a
*decl-specifier* of the *parameter-declaration*'s *decl-specifier-seq*
in a *template-parameter* [[temp.param]].

A program that uses a placeholder type in a context not explicitly
allowed in this subclause is ill-formed.

If the *init-declarator-list* contains more than one *init-declarator*,
they shall all form declarations of variables. The type of each declared
variable is determined by placeholder type deduction
[[dcl.type.auto.deduct]], and if the type that replaces the placeholder
type is not the same in each deduction, the program is ill-formed.

[*Example 2*:

``` cpp
auto x = 5, *y = &x;            // OK: auto is int
auto a = 5, b = { 1, 2 };       // error: different types for auto
```

— *end example*]

If a function with a declared return type that contains a placeholder
type has multiple non-discarded `return` statements, the return type is
deduced for each such `return` statement. If the type deduced is not the
same in each deduction, the program is ill-formed.

If a function with a declared return type that uses a placeholder type
has no non-discarded `return` statements, the return type is deduced as
though from a `return` statement with no operand at the closing brace of
the function body.

[*Example 3*:

``` cpp
auto  f() { }                   // OK, return type is void
auto* g() { }                   // error: cannot deduce auto* from void()
```

— *end example*]

An exported function with a declared return type that uses a placeholder
type shall be defined in the translation unit containing its exported
declaration, outside the *private-module-fragment* (if any).

[*Note 2*: The deduced return type cannot have a name with internal
linkage [[basic.link]]. — *end note*]

If the name of an entity with an undeduced placeholder type appears in
an expression, the program is ill-formed. Once a non-discarded `return`
statement has been seen in a function, however, the return type deduced
from that statement can be used in the rest of the function, including
in other `return` statements.

[*Example 4*:

``` cpp
auto n = n;                     // error: n's initializer refers to n
auto f();
void g() { &f; }                // error: f's return type is unknown
auto sum(int i) {
  if (i == 1)
    return i;                   // sum's return type is int
  else
    return sum(i-1)+i;          // OK, sum's return type has been deduced
}
```

— *end example*]

Return type deduction for a templated entity that is a function or
function template with a placeholder in its declared type occurs when
the definition is instantiated even if the function body contains a
`return` statement with a non-type-dependent operand.

[*Note 3*: Therefore, any use of a specialization of the function
template will cause an implicit instantiation. Any errors that arise
from this instantiation are not in the immediate context of the function
type and can result in the program being ill-formed
[[temp.deduct]]. — *end note*]

[*Example 5*:

``` cpp
template <class T> auto f(T t) { return t; }    // return type deduced at instantiation time
typedef decltype(f(1)) fint_t;                  // instantiates f<int> to deduce return type
template<class T> auto f(T* t) { return *t; }
void g() { int (*p)(int*) = &f; }               // instantiates both fs to determine return types,
                                                // chooses second
```

— *end example*]

Redeclarations or specializations of a function or function template
with a declared return type that uses a placeholder type shall also use
that placeholder, not a deduced type. Similarly, redeclarations or
specializations of a function or function template with a declared
return type that does not use a placeholder type shall not use a
placeholder.

[*Example 6*:

``` cpp
auto f();
auto f() { return 42; }                         // return type is int
auto f();                                       // OK
int f();                                        // error: cannot be overloaded with auto f()
decltype(auto) f();                             // error: auto and decltype(auto) don't match

template <typename T> auto g(T t) { return t; } // #1
template auto g(int);                           // OK, return type is int
template char g(char);                          // error: no matching template
template<> auto g(double);                      // OK, forward declaration with unknown return type

template <class T> T g(T t) { return t; }       // OK, not functionally equivalent to #1
template char g(char);                          // OK, now there is a matching template
template auto g(float);                         // still matches #1

void h() { return g(42); }                      // error: ambiguous

template <typename T> struct A {
  friend T frf(T);
};
auto frf(int i) { return i; }                   // not a friend of A<int>
extern int v;
auto v = 17;                                    // OK, redeclares v
struct S {
  static int i;
};
auto S::i = 23;                                 // OK
```

— *end example*]

A function declared with a return type that uses a placeholder type
shall not be `virtual` [[class.virtual]].

A function declared with a return type that uses a placeholder type
shall not be a coroutine [[dcl.fct.def.coroutine]].

An explicit instantiation declaration [[temp.explicit]] does not cause
the instantiation of an entity declared using a placeholder type, but it
also does not prevent that entity from being instantiated as needed to
determine its type.

[*Example 7*:

``` cpp
template <typename T> auto f(T t) { return t; }
extern template auto f(int);    // does not instantiate f<int>
int (*p)(int) = f;              // instantiates f<int> to determine its return type, but an explicit
                                // instantiation definition is still required somewhere in the program
```

— *end example*]

##### Placeholder type deduction <a id="dcl.type.auto.deduct">[[dcl.type.auto.deduct]]</a>

*Placeholder type deduction*

is the process by which a type containing a placeholder type is replaced
by a deduced type.

A type `T` containing a placeholder type, and a corresponding
initializer E, are determined as follows:

- for a non-discarded `return` statement that occurs in a function
  declared with a return type that contains a placeholder type, `T` is
  the declared return type and E is the operand of the `return`
  statement. If the `return` statement has no operand, then E is
  `void()`;
- for a variable declared with a type that contains a placeholder type,
  `T` is the declared type of the variable and E is the initializer. If
  the initialization is direct-list-initialization, the initializer
  shall be a *braced-init-list* containing only a single
  *assignment-expression* and E is the *assignment-expression*;
- for a non-type template parameter declared with a type that contains a
  placeholder type, `T` is the declared type of the non-type template
  parameter and E is the corresponding template argument.

In the case of a `return` statement with no operand or with an operand
of type `void`, `T` shall be either *type-constraint*ₒₚₜ
`decltype(auto)` or cv *type-constraint*ₒₚₜ `auto`.

If the deduction is for a `return` statement and E is a
*braced-init-list* [[dcl.init.list]], the program is ill-formed.

If the *placeholder-type-specifier* is of the form *type-constraint*ₒₚₜ
`auto`, the deduced type T' replacing `T` is determined using the rules
for template argument deduction. Obtain `P` from `T` by replacing the
occurrences of *type-constraint*ₒₚₜ `auto` either with a new invented
type template parameter `U` or, if the initialization is
copy-list-initialization, with `std::initializer_list<U>`. Deduce a
value for `U` using the rules of template argument deduction from a
function call [[temp.deduct.call]], where `P` is a function template
parameter type and the corresponding argument is E. If the deduction
fails, the declaration is ill-formed. Otherwise, T' is obtained by
substituting the deduced `U` into `P`.

[*Example 8*:

``` cpp
auto x1 = { 1, 2 };             // decltype(x1) is std::initializer_list<int>
auto x2 = { 1, 2.0 };           // error: cannot deduce element type
auto x3{ 1, 2 };                // error: not a single element
auto x4 = { 3 };                // decltype(x4) is std::initializer_list<int>
auto x5{ 3 };                   // decltype(x5) is int
```

— *end example*]

[*Example 9*:

``` cpp
const auto &i = expr;
```

The type of `i` is the deduced type of the parameter `u` in the call
`f(expr)` of the following invented function template:

``` cpp
template <class U> void f(const U& u);
```

— *end example*]

If the *placeholder-type-specifier* is of the form *type-constraint*ₒₚₜ
`decltype(auto)`, `T` shall be the placeholder alone. The type deduced
for `T` is determined as described in  [[dcl.type.simple]], as though E
had been the operand of the `decltype`.

[*Example 10*:

``` cpp
int i;
int&& f();
auto           x2a(i);          // decltype(x2a) is int
decltype(auto) x2d(i);          // decltype(x2d) is int
auto           x3a = i;         // decltype(x3a) is int
decltype(auto) x3d = i;         // decltype(x3d) is int
auto           x4a = (i);       // decltype(x4a) is int
decltype(auto) x4d = (i);       // decltype(x4d) is int&
auto           x5a = f();       // decltype(x5a) is int
decltype(auto) x5d = f();       // decltype(x5d) is int&&
auto           x6a = { 1, 2 };  // decltype(x6a) is std::initializer_list<int>
decltype(auto) x6d = { 1, 2 };  // error: { 1, 2 } is not an expression
auto          *x7a = &i;        // decltype(x7a) is int*
decltype(auto)*x7d = &i;        // error: declared type is not plain decltype(auto)
```

— *end example*]

For a *placeholder-type-specifier* with a *type-constraint*, the
immediately-declared constraint [[temp.param]] of the *type-constraint*
for the type deduced for the placeholder shall be satisfied.

#### Deduced class template specialization types <a id="dcl.type.class.deduct">[[dcl.type.class.deduct]]</a>

If a placeholder for a deduced class type appears as a *decl-specifier*
in the *decl-specifier-seq* of an initializing declaration [[dcl.init]]
of a variable, the declared type of the variable shall be cv `T`, where
`T` is the placeholder.

[*Example 1*:

``` cpp
template <class ...T> struct A {
  A(T...) {}
};
A x[29]{};          // error: no declarator operators allowed
const A& y{};       // error: no declarator operators allowed
```

— *end example*]

The placeholder is replaced by the return type of the function selected
by overload resolution for class template deduction
[[over.match.class.deduct]]. If the *decl-specifier-seq* is followed by
an *init-declarator-list* or *member-declarator-list* containing more
than one *declarator*, the type that replaces the placeholder shall be
the same in each deduction.

A placeholder for a deduced class type can also be used in the
*type-specifier-seq* in the *new-type-id* or *type-id* of a
*new-expression* [[expr.new]], as the *simple-type-specifier* in an
explicit type conversion (functional notation) [[expr.type.conv]], or as
the *type-specifier* in the *parameter-declaration* of a
*template-parameter* [[temp.param]]. A placeholder for a deduced class
type shall not appear in any other context.

[*Example 2*:

``` cpp
template<class T> struct container {
    container(T t) {}
    template<class Iter> container(Iter beg, Iter end);
};
template<class Iter>
container(Iter b, Iter e) -> container<typename std::iterator_traits<Iter>::value_type>;
std::vector<double> v = { ... };

container c(7);                         // OK, deduces int for T
auto d = container(v.begin(), v.end()); // OK, deduces double for T
container e{5, 6};                      // error: int is not an iterator
```

— *end example*]

## Declarators <a id="dcl.decl">[[dcl.decl]]</a>

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
    declarator requires-clause
```

The three components of a *simple-declaration* are the attributes
[[dcl.attr]], the specifiers (*decl-specifier-seq*; [[dcl.spec]]) and
the declarators (*init-declarator-list*). The specifiers indicate the
type, storage class or other properties of the entities being declared.
The declarators specify the names of these entities and (optionally)
modify the type of the specifiers with operators such as `*` (pointer
to) and `()` (function returning). Initial values can also be specified
in a declarator; initializers are discussed in  [[dcl.init]] and 
[[class.init]].

Each *init-declarator* in a declaration is analyzed separately as if it
was in a declaration by itself.

[*Note 1*:

A declaration with several declarators is usually equivalent to the
corresponding sequence of declarations each with a single declarator.
That is

``` cpp
T D1, D2, ... Dn;
```

is usually equivalent to

``` cpp
T D1; T D2; ... T Dn;
```

where `T` is a *decl-specifier-seq* and each `Di` is an
*init-declarator*. One exception is when a name introduced by one of the
*declarator*s hides a type name used by the *decl-specifier*s, so that
when the same *decl-specifier*s are used in a subsequent declaration,
they do not have the same meaning, as in

``` cpp
struct S { ... };
S S, T;                 // declare two instances of struct S
```

which is not equivalent to

``` cpp
struct S { ... };
S S;
S T;                    // error
```

Another exception is when `T` is `auto` [[dcl.spec.auto]], for example:

``` cpp
auto i = 1, j = 2.0;    // error: deduced types for i and j do not match
```

as opposed to

``` cpp
auto i = 1;             // OK: i deduced to have type int
auto j = 2.0;           // OK: j deduced to have type double
```

— *end note*]

The optional *requires-clause* [[temp.pre]] in an *init-declarator* or
*member-declarator* shall be present only if the declarator declares a
templated function [[dcl.fct]]. When present after a declarator, the
*requires-clause* is called the *trailing \*requires-clause\**. The
trailing *requires-clause* introduces the *constraint-expression* that
results from interpreting its *constraint-logical-or-expression* as a
*constraint-expression*.

[*Example 1*:

``` cpp
void f1(int a) requires true;               // error: non-templated function
template<typename T>
  auto f2(T a) -> bool requires true;       // OK
template<typename T>
  auto f3(T a) requires true -> bool;       // error: requires-clause precedes trailing-return-type
void (*pf)() requires true;                 // error: constraint on a variable
void g(int (*)() requires true);            // error: constraint on a parameter-declaration

auto* p = new void(*)(char) requires true;  // error: not a function declaration
```

— *end example*]

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
    '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ
       ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

``` bnf
trailing-return-type:
    '->' type-id
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
    const
    volatile
```

``` bnf
ref-qualifier:
    '&'
    '&&'
```

``` bnf
declarator-id:
    '...'ₒₚₜ id-expression
```

### Type names <a id="dcl.name">[[dcl.name]]</a>

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
defining-type-id:
    defining-type-specifier-seq abstract-declaratorₒₚₜ
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
    noptr-abstract-pack-declarator '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ
    '...'
```

It is possible to identify uniquely the location in the
*abstract-declarator* where the identifier would appear if the
construction were a declarator in a declaration. The named type is then
the same as the type of the hypothetical identifier.

[*Example 1*:

``` cpp
int                 // int i
int *               // int *pi
int *[3]            // int *p[3]
int (*)[3]          // int (*p3i)[3]
int *()             // int *f()
int (*)(double)     // int (*pf)(double)
```

name respectively the types “`int`”, “pointer to `int`”, “array of 3
pointers to `int`”, “pointer to array of 3 `int`”, “function of (no
parameters) returning pointer to `int`”, and “pointer to a function of
(`double`) returning `int`”.

— *end example*]

A type can also be named (often more easily) by using a `typedef`
[[dcl.typedef]].

### Ambiguity resolution <a id="dcl.ambig.res">[[dcl.ambig.res]]</a>

The ambiguity arising from the similarity between a function-style cast
and a declaration mentioned in  [[stmt.ambig]] can also occur in the
context of a declaration. In that context, the choice is between a
function declaration with a redundant set of parentheses around a
parameter name and an object declaration with a function-style cast as
the initializer. Just as for the ambiguities mentioned in 
[[stmt.ambig]], the resolution is to consider any construct that could
possibly be a declaration a declaration.

[*Note 1*: A declaration can be explicitly disambiguated by adding
parentheses around the argument. The ambiguity can be avoided by use of
copy-initialization or list-initialization syntax, or by use of a
non-function-style cast. — *end note*]

[*Example 1*:

``` cpp
struct S {
  S(int);
};

void foo(double a) {
  S w(int(a));                  // function declaration
  S x(int());                   // function declaration
  S y((int(a)));                // object declaration
  S y((int)a);                  // object declaration
  S z = int(a);                 // object declaration
}
```

— *end example*]

An ambiguity can arise from the similarity between a function-style cast
and a *type-id*. The resolution is that any construct that could
possibly be a *type-id* in its syntactic context shall be considered a
*type-id*.

[*Example 2*:

``` cpp
template <class T> struct X {};
template <int N> struct Y {};
X<int()> a;                     // type-id
X<int(1)> b;                    // expression (ill-formed)
Y<int()> c;                     // type-id (ill-formed)
Y<int(1)> d;                    // expression

void foo(signed char a) {
  sizeof(int());                // type-id (ill-formed)
  sizeof(int(a));               // expression
  sizeof(int(unsigned(a)));     // type-id (ill-formed)

  (int())+1;                    // type-id (ill-formed)
  (int(a))+1;                   // expression
  (int(unsigned(a)))+1;         // type-id (ill-formed)
}
```

— *end example*]

Another ambiguity arises in a *parameter-declaration-clause* when a
*type-name* is nested in parentheses. In this case, the choice is
between the declaration of a parameter of type pointer to function and
the declaration of a parameter with redundant parentheses around the
*declarator-id*. The resolution is to consider the *type-name* as a
*simple-type-specifier* rather than a *declarator-id*.

[*Example 3*:

``` cpp
class C { };
void f(int(C)) { }              // void f(int(*fp)(C c)) { }
                                // not: void f(int C) { }

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

— *end example*]

### Meaning of declarators <a id="dcl.meaning">[[dcl.meaning]]</a>

A declarator contains exactly one *declarator-id*; it names the
identifier that is declared. An *unqualified-id* occurring in a
*declarator-id* shall be a simple *identifier* except for the
declaration of some special functions ([[class.ctor]], [[class.conv]],
[[class.dtor]], [[over.oper]]) and for the declaration of template
specializations or partial specializations [[temp.spec]]. When the
*declarator-id* is qualified, the declaration shall refer to a
previously declared member of the class or namespace to which the
qualifier refers (or, in the case of a namespace, of an element of the
inline namespace set of that namespace [[namespace.def]]) or to a
specialization thereof; the member shall not merely have been introduced
by a *using-declaration* in the scope of the class or namespace
nominated by the *nested-name-specifier* of the *declarator-id*. The
*nested-name-specifier* of a qualified *declarator-id* shall not begin
with a *decltype-specifier*.

[*Note 1*: If the qualifier is the global `::` scope resolution
operator, the *declarator-id* refers to a name declared in the global
namespace scope. — *end note*]

The optional *attribute-specifier-seq* following a *declarator-id*
appertains to the entity that is declared.

A `static`, `thread_local`, `extern`, `mutable`, `friend`, `inline`,
`virtual`, `constexpr`, or `typedef` specifier or an
*explicit-specifier* applies directly to each *declarator-id* in an
*init-declarator-list* or *member-declarator-list*; the type specified
for each *declarator-id* depends on both the *decl-specifier-seq* and
its *declarator*.

Thus, a declaration of a particular identifier has the form

``` cpp
T D
```

where `T` is of the form *attribute-specifier-seq*ₒₚₜ
*decl-specifier-seq* and `D` is a declarator. Following is a recursive
procedure for determining the type specified for the contained
*declarator-id* by such a declaration.

First, the *decl-specifier-seq* determines a type. In a declaration

``` cpp
T D
```

the *decl-specifier-seq* `T` determines the type `T`.

[*Example 1*:

In the declaration

``` cpp
int unsigned i;
```

the type specifiers `int` `unsigned` determine the type “`unsigned int`”
[[dcl.type.simple]].

— *end example*]

In a declaration *attribute-specifier-seq*ₒₚₜ `T` `D` where `D` is an
unadorned identifier the type of this identifier is “`T`”.

In a declaration `T` `D` where `D` has the form

``` bnf
'(' 'D1' ')'
```

the type of the contained *declarator-id* is the same as that of the
contained *declarator-id* in the declaration

``` cpp
T D1
```

Parentheses do not alter the type of the embedded *declarator-id*, but
they can alter the binding of complex declarators.

#### Pointers <a id="dcl.ptr">[[dcl.ptr]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
'*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 'D1'
```

and the type of the identifier in the declaration `T` `D1` is
“*derived-declarator-type-list* `T`”, then the type of the identifier of
`D` is “*derived-declarator-type-list* *cv-qualifier-seq* pointer to
`T`”. The *cv-qualifier*s apply to the pointer and not to the object
pointed to. Similarly, the optional *attribute-specifier-seq*
[[dcl.attr.grammar]] appertains to the pointer and not to the object
pointed to.

[*Example 1*:

The declarations

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
*ppc = &ci;         // OK, but would make p point to ci because of previous error
*p = 5;             // clobber ci
```

— *end example*]

See also  [[expr.ass]] and  [[dcl.init]].

[*Note 1*: Forming a pointer to reference type is ill-formed; see 
[[dcl.ref]]. Forming a function pointer type is ill-formed if the
function type has *cv-qualifier*s or a *ref-qualifier*; see 
[[dcl.fct]]. Since the address of a bit-field [[class.bit]] cannot be
taken, a pointer can never point to a bit-field. — *end note*]

#### References <a id="dcl.ref">[[dcl.ref]]</a>

In a declaration `T` `D` where `D` has either of the forms

``` bnf
'&' attribute-specifier-seqₒₚₜ 'D1'
'&&' attribute-specifier-seqₒₚₜ 'D1'
```

and the type of the identifier in the declaration `T` `D1` is
“*derived-declarator-type-list* `T`”, then the type of the identifier of
`D` is “*derived-declarator-type-list* reference to `T`”. The optional
*attribute-specifier-seq* appertains to the reference type. Cv-qualified
references are ill-formed except when the cv-qualifiers are introduced
through the use of a *typedef-name* ([[dcl.typedef]], [[temp.param]])
or *decltype-specifier* [[dcl.type.simple]], in which case the
cv-qualifiers are ignored.

[*Example 1*:

``` cpp
typedef int& A;
const A aref = 3;   // error: lvalue reference to non-const initialized with rvalue
```

The type of `aref` is “lvalue reference to `int`”, not “lvalue reference
to `const int`”.

— *end example*]

[*Note 1*: A reference can be thought of as a name of an
object. — *end note*]

A declarator that specifies the type “reference to cv `void`” is
ill-formed.

A reference type that is declared using `&` is called an *lvalue
reference*, and a reference type that is declared using `&&` is called
an *rvalue reference*. Lvalue references and rvalue references are
distinct types. Except where explicitly noted, they are semantically
equivalent and commonly referred to as references.

[*Example 2*:

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

— *end example*]

It is unspecified whether or not a reference requires storage
[[basic.stc]].

There shall be no references to references, no arrays of references, and
no pointers to references. The declaration of a reference shall contain
an *initializer* [[dcl.init.ref]] except when the declaration contains
an explicit `extern` specifier [[dcl.stc]], is a class member
[[class.mem]] declaration within a class definition, or is the
declaration of a parameter or a return type [[dcl.fct]]; see 
[[basic.def]]. A reference shall be initialized to refer to a valid
object or function.

[*Note 2*:  In particular, a null reference cannot exist in a
well-defined program, because the only way to create such a reference
would be to bind it to the “object” obtained by indirection through a
null pointer, which causes undefined behavior. As described in 
[[class.bit]], a reference cannot be bound directly to a
bit-field. — *end note*]

If a *typedef-name* ([[dcl.typedef]], [[temp.param]]) or a
*decltype-specifier* [[dcl.type.simple]] denotes a type `TR` that is a
reference to a type `T`, an attempt to create the type “lvalue reference
to cv `TR`” creates the type “lvalue reference to `T`”, while an attempt
to create the type “rvalue reference to cv `TR`” creates the type `TR`.

[*Note 3*: This rule is known as reference collapsing. — *end note*]

[*Example 3*:

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

— *end example*]

[*Note 4*: Forming a reference to function type is ill-formed if the
function type has *cv-qualifier*s or a *ref-qualifier*; see 
[[dcl.fct]]. — *end note*]

#### Pointers to members <a id="dcl.mptr">[[dcl.mptr]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
nested-name-specifier '*' attribute-specifier-seqₒₚₜ cv-qualifier-seqₒₚₜ 'D1'
```

and the *nested-name-specifier* denotes a class, and the type of the
identifier in the declaration `T` `D1` is
“*derived-declarator-type-list* `T`”, then the type of the identifier of
`D` is “*derived-declarator-type-list* *cv-qualifier-seq* pointer to
member of class *nested-name-specifier* of type `T`”. The optional
*attribute-specifier-seq* [[dcl.attr.grammar]] appertains to the
pointer-to-member.

[*Example 1*:

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
obj.*pmi = 7;       // assign 7 to an integer member of obj
(obj.*pmf)(7);      // call a function member of obj with the argument 7
```

— *end example*]

A pointer to member shall not point to a static member of a class
[[class.static]], a member with reference type, or “cv `void`”.

[*Note 1*: See also  [[expr.unary]] and  [[expr.mptr.oper]]. The type
“pointer to member” is distinct from the type “pointer”, that is, a
pointer to member is declared only by the pointer-to-member declarator
syntax, and never by the pointer declarator syntax. There is no
“reference-to-member” type in C++. — *end note*]

#### Arrays <a id="dcl.array">[[dcl.array]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
'D1' '[' constant-expressionₒₚₜ ']' attribute-specifier-seqₒₚₜ
```

and the type of the contained *declarator-id* in the declaration `T`
`D1` is “*derived-declarator-type-list* `T`”, the type of the
*declarator-id* in `D` is “*derived-declarator-type-list* array of `N`
`T`”. The *constant-expression* shall be a converted constant expression
of type `std::size_t` [[expr.const]]. Its value `N` specifies the
*array bound*, i.e., the number of elements in the array; `N` shall be
greater than zero.

In a declaration `T` `D` where `D` has the form

``` bnf
'D1 [ ]' attribute-specifier-seqₒₚₜ
```

and the type of the contained *declarator-id* in the declaration `T`
`D1` is “*derived-declarator-type-list* `T`”, the type of the
*declarator-id* in `D` is “*derived-declarator-type-list* array of
unknown bound of `T`”, except as specified below.

A type of the form “array of `N` `U`” or “array of unknown bound of `U`”
is an *array type*. The optional *attribute-specifier-seq* appertains to
the array type.

`U` is called the array *element type*; this type shall not be a
placeholder type [[dcl.spec.auto]], a reference type, a function type,
an array of unknown bound, or cv `void`.

[*Note 1*: An array can be constructed from one of the fundamental
types (except `void`), from a pointer, from a pointer to member, from a
class, from an enumeration type, or from an array of known
bound. — *end note*]

[*Example 1*:

``` cpp
float fa[17], *afp[17];
```

declares an array of `float` numbers and an array of pointers to `float`
numbers.

— *end example*]

Any type of the form “*cv-qualifier-seq* array of `N` `U`” is adjusted
to “array of `N` *cv-qualifier-seq* `U`”, and similarly for “array of
unknown bound of `U`”.

[*Example 2*:

``` cpp
typedef int A[5], AA[2][3];
typedef const A CA;             // type is ``array of 5 const int''
typedef const AA CAA;           // type is ``array of 2 array of 3 const int''
```

— *end example*]

[*Note 2*: An “array of `N` *cv-qualifier-seq* `U`” has cv-qualified
type; see  [[basic.type.qualifier]]. — *end note*]

An object of type “array of `N` `U`” contains a contiguously allocated
non-empty set of `N` subobjects of type `U`, known as the *elements* of
the array, and numbered `0` to `N-1`.

In addition to declarations in which an incomplete object type is
allowed, an array bound may be omitted in some cases in the declaration
of a function parameter [[dcl.fct]]. An array bound may also be omitted
when an object (but not a non-static data member) of array type is
initialized and the declarator is followed by an initializer (
[[dcl.init]], [[class.mem]], [[expr.type.conv]], [[expr.new]]). In these
cases, the array bound is calculated from the number of initial elements
(say, `N`) supplied [[dcl.init.aggr]], and the type of the array is
“array of `N` `U`”.

Furthermore, if there is a preceding declaration of the entity in the
same scope in which the bound was specified, an omitted array bound is
taken to be the same as in that earlier declaration, and similarly for
the definition of a static data member of a class.

[*Example 3*:

``` cpp
extern int x[10];
struct S {
  static int y[10];
};

int x[];                // OK: bound is 10
int S::y[];             // OK: bound is 10

void f() {
  extern int x[];
  int i = sizeof(x);    // error: incomplete object type
}
```

— *end example*]

[*Note 3*:

When several “array of” specifications are adjacent, a multidimensional
array type is created; only the first of the constant expressions that
specify the bounds of the arrays may be omitted.

[*Example 4*:

``` cpp
int x3d[3][5][7];
```

declares an array of three elements, each of which is an array of five
elements, each of which is an array of seven integers. The overall array
can be viewed as a three-dimensional array of integers, with rank
3 × 5 × 7. Any of the expressions `x3d`, `x3d[i]`, `x3d[i][j]`,
`x3d[i][j][k]` can reasonably appear in an expression. The expression
`x3d[i]` is equivalent to `*(x3d + i)`; in that expression, `x3d` is
subject to the array-to-pointer conversion [[conv.array]] and is first
converted to a pointer to a 2-dimensional array with rank 5 × 7 that
points to the first element of `x3d`. Then `i` is added, which on
typical implementations involves multiplying `i` by the length of the
object to which the pointer points, which is `sizeof(int)`× 5 × 7. The
result of the addition and indirection is an lvalue denoting the
`i`^\text{th} array element of `x3d` (an array of five arrays of seven
integers). If there is another subscript, the same argument applies
again, so `x3d[i][j]` is an lvalue denoting the `j`^\text{th} array
element of the `i`^\text{th} array element of `x3d` (an array of seven
integers), and `x3d[i][j][k]` is an lvalue denoting the `k`^\text{th}
array element of the `j`^\text{th} array element of the `i`^\text{th}
array element of `x3d` (an integer).

— *end example*]

The first subscript in the declaration helps determine the amount of
storage consumed by an array but plays no other part in subscript
calculations.

— *end note*]

[*Note 4*: Conversions affecting expressions of array type are
described in  [[conv.array]]. — *end note*]

[*Note 5*: The subscript operator can be overloaded for a class
[[over.sub]]. For the operator’s built-in meaning, see
[[expr.sub]]. — *end note*]

#### Functions <a id="dcl.fct">[[dcl.fct]]</a>

In a declaration `T` `D` where `D` has the form

``` bnf
'D1' '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ
   ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ
```

and the type of the contained *declarator-id* in the declaration `T`
`D1` is “*derived-declarator-type-list* `T`”, the type of the
*declarator-id* in `D` is “*derived-declarator-type-list* `noexcept`ₒₚₜ
function of parameter-type-list *cv-qualifier-seq*ₒₚₜ *ref-qualifier*ₒₚₜ
returning `T`”, where

- the parameter-type-list is derived from the
  *parameter-declaration-clause* as described below and
- the optional `noexcept` is present if and only if the exception
  specification [[except.spec]] is non-throwing.

The optional *attribute-specifier-seq* appertains to the function type.

In a declaration `T` `D` where `D` has the form

``` bnf
'D1' '(' parameter-declaration-clause ')' cv-qualifier-seqₒₚₜ
   ref-qualifierₒₚₜ noexcept-specifierₒₚₜ attribute-specifier-seqₒₚₜ trailing-return-type
```

and the type of the contained *declarator-id* in the declaration `T`
`D1` is “*derived-declarator-type-list* `T`”, `T` shall be the single
*type-specifier* `auto`. The type of the *declarator-id* in `D` is
“*derived-declarator-type-list* `noexcept`ₒₚₜ function of
parameter-type-list *cv-qualifier-seq*ₒₚₜ *ref-qualifier*ₒₚₜ returning
`U`”, where

- the parameter-type-list is derived from the
  *parameter-declaration-clause* as described below,
- `U` is the type specified by the *trailing-return-type*, and
- the optional `noexcept` is present if and only if the exception
  specification is non-throwing.

The optional *attribute-specifier-seq* appertains to the function type.

A type of either form is a *function type*.[^2]

``` bnf
parameter-declaration-clause:
    parameter-declaration-listₒₚₜ '...'ₒₚₜ
    parameter-declaration-list ',' '...'
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
specified, and their processing, when the function is called.

[*Note 1*:  The *parameter-declaration-clause* is used to convert the
arguments specified on the function call; see 
[[expr.call]]. — *end note*]

If the *parameter-declaration-clause* is empty, the function takes no
arguments. A parameter list consisting of a single unnamed parameter of
non-dependent type `void` is equivalent to an empty parameter list.
Except for this special case, a parameter shall not have type cv `void`.
A parameter with volatile-qualified type is deprecated; see 
[[depr.volatile.type]]. If the *parameter-declaration-clause* terminates
with an ellipsis or a function parameter pack [[temp.variadic]], the
number of arguments shall be equal to or greater than the number of
parameters that do not have a default argument and are not function
parameter packs. Where syntactically correct and where “`...`” is not
part of an *abstract-declarator*, “`, ...`” is synonymous with “`...`”.

[*Example 1*:

The declaration

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
`const` `char*`.

— *end example*]

[*Note 2*: The standard header `<cstdarg>` contains a mechanism for
accessing arguments passed using the ellipsis (see  [[expr.call]] and 
[[support.runtime]]). — *end note*]

The type of a function is determined using the following rules. The type
of each parameter (including function parameter packs) is determined
from its own *decl-specifier-seq* and *declarator*. After determining
the type of each parameter, any parameter of type “array of `T`” or of
function type `T` is adjusted to be “pointer to `T`”. After producing
the list of parameter types, any top-level *cv-qualifier*s modifying a
parameter type are deleted when forming the function type. The resulting
list of transformed parameter types and the presence or absence of the
ellipsis or a function parameter pack is the function’s
*parameter-type-list*.

[*Note 3*: This transformation does not affect the types of the
parameters. For example, `int(*)(const int p, decltype(p)*)` and
`int(*)(int, const int*)` are identical types. — *end note*]

A function type with a *cv-qualifier-seq* or a *ref-qualifier*
(including a type named by *typedef-name* ([[dcl.typedef]],
[[temp.param]])) shall appear only as:

- the function type for a non-static member function,
- the function type to which a pointer to member refers,
- the top-level function type of a function typedef declaration or
  *alias-declaration*,
- the *type-id* in the default argument of a *type-parameter*
  [[temp.param]], or
- the *type-id* of a *template-argument* for a *type-parameter*
  [[temp.arg.type]].

[*Example 2*:

``` cpp
typedef int FIC(int) const;
FIC f;              // error: does not declare a member function
struct S {
  FIC f;            // OK
};
FIC S::*pm = &S::f; // OK
```

— *end example*]

The effect of a *cv-qualifier-seq* in a function declarator is not the
same as adding cv-qualification on top of the function type. In the
latter case, the cv-qualifiers are ignored.

[*Note 4*: A function type that has a *cv-qualifier-seq* is not a
cv-qualified type; there are no cv-qualified function
types. — *end note*]

[*Example 3*:

``` cpp
typedef void F();
struct S {
  const F f;        // OK: equivalent to: void f();
};
```

— *end example*]

The return type, the parameter-type-list, the *ref-qualifier*, the
*cv-qualifier-seq*, and the exception specification, but not the default
arguments [[dcl.fct.default]] or the trailing *requires-clause*
[[dcl.decl]], are part of the function type.

[*Note 5*: Function types are checked during the assignments and
initializations of pointers to functions, references to functions, and
pointers to member functions. — *end note*]

[*Example 4*:

The declaration

``` cpp
int fseek(FILE*, long, int);
```

declares a function taking three arguments of the specified types, and
returning `int` [[dcl.type]].

— *end example*]

A single name can be used for several different functions in a single
scope; this is function overloading [[over]]. All declarations for a
function shall have equivalent return types, parameter-type-lists, and
*requires-clause*s [[temp.over.link]].

Functions shall not have a return type of type array or function,
although they may have a return type of type pointer or reference to
such things. There shall be no arrays of functions, although there can
be arrays of pointers to functions.

A volatile-qualified return type is deprecated; see 
[[depr.volatile.type]].

Types shall not be defined in return or parameter types.

A typedef of function type may be used to declare a function but shall
not be used to define a function [[dcl.fct.def]].

[*Example 5*:

``` cpp
typedef void F();
F  fv;              // OK: equivalent to void fv();
F  fv { }           // error
void fv() { }       // OK: definition of fv
```

— *end example*]

An identifier can optionally be provided as a parameter name; if present
in a function definition [[dcl.fct.def]], it names a parameter.

[*Note 6*: In particular, parameter names are also optional in function
definitions and names used for a parameter in different declarations and
the definition of a function need not be the same. If a parameter name
is present in a function declaration that is not a definition, it cannot
be used outside of its function declarator because that is the extent of
its potential scope [[basic.scope.param]]. — *end note*]

[*Example 6*:

The declaration

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
function, which is then called.

— *end example*]

[*Note 7*:

Typedefs and *trailing-return-type*s are sometimes convenient when the
return type of a function is complex. For example, the function `fpif`
above could have been declared

``` cpp
typedef int  IFUNC(int);
IFUNC*  fpif(int);
```

or

``` cpp
auto fpif(int)->int(*)(int);
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

— *end note*]

A *non-template function* is a function that is not a function template
specialization.

[*Note 8*: A function template is not a function. — *end note*]

An *abbreviated function template* is a function declaration that has
one or more generic parameter type placeholders [[dcl.spec.auto]]. An
abbreviated function template is equivalent to a function template
[[temp.fct]] whose *template-parameter-list* includes one invented type
*template-parameter* for each generic parameter type placeholder of the
function declaration, in order of appearance. For a
*placeholder-type-specifier* of the form `auto`, the invented parameter
is an unconstrained *type-parameter*. For a *placeholder-type-specifier*
of the form *type-constraint* `auto`, the invented parameter is a
*type-parameter* with that *type-constraint*. The invented type
*template-parameter* is a template parameter pack if the corresponding
*parameter-declaration* declares a function parameter pack [[dcl.fct]].
If the placeholder contains `decltype(auto)`, the program is ill-formed.
The adjusted function parameters of an abbreviated function template are
derived from the *parameter-declaration-clause* by replacing each
occurrence of a placeholder with the name of the corresponding invented
*template-parameter*.

[*Example 7*:

``` cpp
template<typename T>     concept C1 = /* ... */;
template<typename T>     concept C2 = /* ... */;
template<typename... Ts> concept C3 = /* ... */;

void g1(const C1 auto*, C2 auto&);
void g2(C1 auto&...);
void g3(C3 auto...);
void g4(C3 auto);
```

These declarations are functionally equivalent (but not equivalent) to
the following declarations.

``` cpp
template<C1 T, C2 U> void g1(const T*, U&);
template<C1... Ts>   void g2(Ts&...);
template<C3... Ts>   void g3(Ts...);
template<C3 T>       void g4(T);
```

Abbreviated function templates can be specialized like all function
templates.

``` cpp
template<> void g1<int>(const int*, const double&); // OK, specialization of g1<int, const double>
```

— *end example*]

An abbreviated function template can have a *template-head*. The
invented *template-parameters* are appended to the
*template-parameter-list* after the explicitly declared
*template-parameters*.

[*Example 8*:

``` cpp
template<typename> concept C = /* ... */;

template <typename T, C U>
  void g(T x, U y, C auto z);
```

This is functionally equivalent to each of the following two
declarations.

``` cpp
template<typename T, C U, C W>
  void g(T x, U y, W z);

template<typename T, typename U, typename W>
  requires C<U> && C<W>
  void g(T x, U y, W z);
```

— *end example*]

A function declaration at block scope shall not declare an abbreviated
function template.

A *declarator-id* or *abstract-declarator* containing an ellipsis shall
only be used in a *parameter-declaration*. When it is part of a
*parameter-declaration-clause*, the *parameter-declaration* declares a
function parameter pack [[temp.variadic]]. Otherwise, the
*parameter-declaration* is part of a *template-parameter-list* and
declares a template parameter pack; see  [[temp.param]]. A function
parameter pack is a pack expansion [[temp.variadic]].

[*Example 9*:

``` cpp
template<typename... T> void f(T (* ...t)(int, int));

int add(int, int);
float subtract(int, int);

void g() {
  f(add, subtract);
}
```

— *end example*]

There is a syntactic ambiguity when an ellipsis occurs at the end of a
*parameter-declaration-clause* without a preceding comma. In this case,
the ellipsis is parsed as part of the *abstract-declarator* if the type
of the parameter either names a template parameter pack that has not
been expanded or contains `auto`; otherwise, it is parsed as part of the
*parameter-declaration-clause*.[^3]

#### Default arguments <a id="dcl.fct.default">[[dcl.fct.default]]</a>

If an *initializer-clause* is specified in a *parameter-declaration*
this *initializer-clause* is used as a default argument.

[*Note 1*: Default arguments will be used in calls where trailing
arguments are missing [[expr.call]]. — *end note*]

[*Example 1*:

The declaration

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

— *end example*]

A default argument shall be specified only in the
*parameter-declaration-clause* of a function declaration or
*lambda-declarator* or in a *template-parameter* [[temp.param]]; in the
latter case, the *initializer-clause* shall be an
*assignment-expression*. A default argument shall not be specified for a
template parameter pack or a function parameter pack. If it is specified
in a *parameter-declaration-clause*, it shall not occur within a
*declarator* or *abstract-declarator* of a *parameter-declaration*.[^4]

For non-template functions, default arguments can be added in later
declarations of a function in the same scope. Declarations in different
scopes have completely distinct sets of default arguments. That is,
declarations in inner scopes do not acquire default arguments from
declarations in outer scopes, and vice versa. In a given function
declaration, each parameter subsequent to a parameter with a default
argument shall have a default argument supplied in this or a previous
declaration, unless the parameter was expanded from a parameter pack, or
shall be a function parameter pack.

[*Note 2*: A default argument cannot be redefined by a later
declaration (not even to the same value)
[[basic.def.odr]]. — *end note*]

[*Example 2*:

``` cpp
void g(int = 0, ...);           // OK, ellipsis is not a parameter so it can follow
                                // a parameter with a default argument
void f(int, int);
void f(int, int = 7);
void h() {
  f(3);                         // OK, calls f(3, 7)
  void f(int = 1, int);         // error: does not use default from surrounding scope
}
void m() {
  void f(int, int);             // has no defaults
  f(4);                         // error: wrong number of arguments
  void f(int, int = 5);         // OK
  f(4);                         // OK, calls f(4, 5);
  void f(int, int = 5);         // error: cannot redefine, even to same value
}
void n() {
  f(6);                         // OK, calls f(6, 7)
}
template<class ... T> struct C {
  void f(int n = 0, T...);
};
C<int> c;                       // OK, instantiates declaration void C::f(int n = 0, int)
```

— *end example*]

For a given inline function defined in different translation units, the
accumulated sets of default arguments at the end of the translation
units shall be the same; no diagnostic is required. If a friend
declaration specifies a default argument expression, that declaration
shall be a definition and shall be the only declaration of the function
or function template in the translation unit.

The default argument has the same semantic constraints as the
initializer in a declaration of a variable of the parameter type, using
the copy-initialization semantics [[dcl.init]]. The names in the default
argument are bound, and the semantic constraints are checked, at the
point where the default argument appears. Name lookup and checking of
semantic constraints for default arguments in function templates and in
member functions of class templates are performed as described in 
[[temp.inst]].

[*Example 3*:

In the following code, `g` will be called with the value `f(2)`:

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

— *end example*]

[*Note 3*: In member function declarations, names in default arguments
are looked up as described in  [[basic.lookup.unqual]]. Access checking
applies to names in default arguments as described in
[[class.access]]. — *end note*]

Except for member functions of class templates, the default arguments in
a member function definition that appears outside of the class
definition are added to the set of default arguments provided by the
member function declaration in the class definition; the program is
ill-formed if a default constructor [[class.default.ctor]], copy or move
constructor [[class.copy.ctor]], or copy or move assignment operator
[[class.copy.assign]] is so declared. Default arguments for a member
function of a class template shall be specified on the initial
declaration of the member function within the class template.

[*Example 4*:

``` cpp
class C {
  void f(int i = 3);
  void g(int i, int j = 99);
};

void C::f(int i = 3) {}         // error: default argument already specified in class scope
void C::g(int i = 88, int j) {} // in this translation unit, C::g can be called with no argument
```

— *end example*]

[*Note 4*: A local variable cannot be odr-used [[basic.def.odr]] in a
default argument. — *end note*]

[*Example 5*:

``` cpp
void f() {
  int i;
  extern void g(int x = i);         // error
  extern void h(int x = sizeof(i)); // OK
  // ...
}
```

— *end example*]

[*Note 5*:

The keyword `this` may not appear in a default argument of a member
function; see  [[expr.prim.this]].

[*Example 6*:

``` cpp
class A {
  void f(A* p = this) { }           // error
};
```

— *end example*]

— *end note*]

A default argument is evaluated each time the function is called with no
argument for the corresponding parameter. A parameter shall not appear
as a potentially-evaluated expression in a default argument. Parameters
of a function declared before a default argument are in scope and can
hide namespace and class member names.

[*Example 7*:

``` cpp
int a;
int f(int a, int b = a);            // error: parameter a used as default argument
typedef int I;
int g(float I, int b = I(2));       // error: parameter I found
int h(int a, int b = sizeof(a));    // OK, unevaluated operand
```

— *end example*]

A non-static member shall not appear in a default argument unless it
appears as the *id-expression* of a class member access expression
[[expr.ref]] or unless it is used to form a pointer to member
[[expr.unary.op]].

[*Example 8*:

The declaration of `X::mem1()` in the following example is ill-formed
because no object is supplied for the non-static member `X::a` used as
an initializer.

``` cpp
int b;
class X {
  int a;
  int mem1(int i = a);              // error: non-static member a used as default argument
  int mem2(int i = b);              // OK;  use X::b
  static int b;
};
```

The declaration of `X::mem2()` is meaningful, however, since no object
is needed to access the static member `X::b`. Classes, objects, and
members are described in [[class]].

— *end example*]

A default argument is not part of the type of a function.

[*Example 9*:

``` cpp
int f(int = 0);

void h() {
  int j = f(1);
  int k = f();                      // OK, means f(0)
}

int (*p1)(int) = &f;
int (*p2)() = &f;                   // error: type mismatch
```

— *end example*]

When a declaration of a function is introduced by way of a
*using-declaration* [[namespace.udecl]], any default argument
information associated with the declaration is made known as well. If
the function is redeclared thereafter in the namespace with additional
default arguments, the additional arguments are also known at any point
following the redeclaration where the *using-declaration* is in scope.

A virtual function call [[class.virtual]] uses the default arguments in
the declaration of the virtual function determined by the static type of
the pointer or reference denoting the object. An overriding function in
a derived class does not acquire default arguments from the function it
overrides.

[*Example 10*:

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

— *end example*]

## Initializers <a id="dcl.init">[[dcl.init]]</a>

The process of initialization described in this subclause applies to all
initializations regardless of syntactic context, including the
initialization of a function parameter [[expr.call]], the initialization
of a return value [[stmt.return]], or when an initializer follows a
declarator.

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
braced-init-list:
    \terminal{\ initializer-list \terminal{,}ₒₚₜ \terminal{\}}
    \terminal{\ designated-initializer-list \terminal{,}ₒₚₜ \terminal{\}}
    \terminal{\ \terminal{\}}
```

``` bnf
initializer-list:
    initializer-clause '...'ₒₚₜ
    initializer-list ',' initializer-clause '...'ₒₚₜ
```

``` bnf
designated-initializer-list:
    designated-initializer-clause
    designated-initializer-list ',' designated-initializer-clause
```

``` bnf
designated-initializer-clause:
    designator brace-or-equal-initializer
```

``` bnf
designator:
    '.' identifier
```

``` bnf
expr-or-braced-init-list:
    expression
    braced-init-list
```

[*Note 1*: The rules in this subclause apply even if the grammar
permits only the *brace-or-equal-initializer* form of *initializer* in a
given context. — *end note*]

Except for objects declared with the `constexpr` specifier, for which
see  [[dcl.constexpr]], an *initializer* in the definition of a variable
can consist of arbitrary expressions involving literals and previously
declared variables and functions, regardless of the variable’s storage
duration.

[*Example 1*:

``` cpp
int f(int);
int a = 2;
int b = f(a);
int c(b);
```

— *end example*]

[*Note 2*: Default arguments are more restricted; see 
[[dcl.fct.default]]. — *end note*]

[*Note 3*: The order of initialization of variables with static storage
duration is described in  [[basic.start]] and 
[[stmt.dcl]]. — *end note*]

A declaration of a block-scope variable with external or internal
linkage that has an *initializer* is ill-formed.

To *zero-initialize* an object or reference of type `T` means:

- if `T` is a scalar type [[basic.types]], the object is initialized to
  the value obtained by converting the integer literal `0` (zero) to
  `T`;[^5]
- if `T` is a (possibly cv-qualified) non-union class type, its padding
  bits [[basic.types]] are initialized to zero bits and each non-static
  data member, each non-virtual base class subobject, and, if the object
  is not a base class subobject, each virtual base class subobject is
  zero-initialized;
- if `T` is a (possibly cv-qualified) union type, its padding bits
  [[basic.types]] are initialized to zero bits and the object’s first
  non-static named data member is zero-initialized;
- if `T` is an array type, each element is zero-initialized;
- if `T` is a reference type, no initialization is performed.

To *default-initialize* an object of type `T` means:

- If `T` is a (possibly cv-qualified) class type [[class]], constructors
  are considered. The applicable constructors are enumerated
  [[over.match.ctor]], and the best one for the *initializer* `()` is
  chosen through overload resolution [[over.match]]. The constructor
  thus selected is called, with an empty argument list, to initialize
  the object.
- If `T` is an array type, each element is default-initialized.
- Otherwise, no initialization is performed.

A class type `T` is *const-default-constructible* if
default-initialization of `T` would invoke a user-provided constructor
of `T` (not inherited from a base class) or if

- each direct non-variant non-static data member `M` of `T` has a
  default member initializer or, if `M` is of class type `X` (or array
  thereof), `X` is const-default-constructible,
- if `T` is a union with at least one non-static data member, exactly
  one variant member has a default member initializer,
- if `T` is not a union, for each anonymous union member with at least
  one non-static data member (if any), exactly one non-static data
  member has a default member initializer, and
- each potentially constructed base class of `T` is
  const-default-constructible.

If a program calls for the default-initialization of an object of a
const-qualified type `T`, `T` shall be a const-default-constructible
class type or array thereof.

To *value-initialize* an object of type `T` means:

- if `T` is a (possibly cv-qualified) class type [[class]], then
  - if `T` has either no default constructor [[class.default.ctor]] or a
    default constructor that is user-provided or deleted, then the
    object is default-initialized;
  - otherwise, the object is zero-initialized and the semantic
    constraints for default-initialization are checked, and if `T` has a
    non-trivial default constructor, the object is default-initialized;
- if `T` is an array type, then each element is value-initialized;
- otherwise, the object is zero-initialized.

A program that calls for default-initialization or value-initialization
of an entity of reference type is ill-formed.

[*Note 4*: For every object of static storage duration, static
initialization [[basic.start.static]] is performed at program startup
before any other initialization takes place. In some cases, additional
initialization is done later. — *end note*]

An object whose initializer is an empty set of parentheses, i.e., `()`,
shall be value-initialized.

[*Note 5*:

Since `()` is not permitted by the syntax for *initializer*,

``` cpp
X a();
```

is not the declaration of an object of class `X`, but the declaration of
a function taking no argument and returning an `X`. The form `()` is
permitted in certain other initialization contexts ([[expr.new]],
[[expr.type.conv]], [[class.base.init]]).

— *end note*]

If no initializer is specified for an object, the object is
default-initialized.

An initializer for a static member is in the scope of the member’s
class.

[*Example 2*:

``` cpp
int a;

struct X {
  static int a;
  static int b;
};

int X::a = 1;
int X::b = a;                   // X::b = X::a
```

— *end example*]

If the entity being initialized does not have class type, the
*expression-list* in a parenthesized initializer shall be a single
expression.

The initialization that occurs in the `=` form of a
*brace-or-equal-initializer* or *condition* [[stmt.select]], as well as
in argument passing, function return, throwing an exception
[[except.throw]], handling an exception [[except.handle]], and aggregate
member initialization [[dcl.init.aggr]], is called
*copy-initialization*.

[*Note 6*: Copy-initialization may invoke a move
[[class.copy.ctor]]. — *end note*]

The initialization that occurs

- for an *initializer* that is a parenthesized *expression-list* or a
  *braced-init-list*,
- for a *new-initializer* [[expr.new]],
- in a `static_cast` expression [[expr.static.cast]],
- in a functional notation type conversion [[expr.type.conv]], and
- in the *braced-init-list* form of a *condition*

is called *direct-initialization*.

The semantics of initializers are as follows. The *destination type* is
the type of the object or reference being initialized and the *source
type* is the type of the initializer expression. If the initializer is
not a single (possibly parenthesized) expression, the source type is not
defined.

- If the initializer is a (non-parenthesized) *braced-init-list* or is
  `=` *braced-init-list*, the object or reference is list-initialized
  [[dcl.init.list]].
- If the destination type is a reference type, see  [[dcl.init.ref]].
- If the destination type is an array of characters, an array of
  `char8_t`, an array of `char16_t`, an array of `char32_t`, or an array
  of `wchar_t`, and the initializer is a *string-literal*, see 
  [[dcl.init.string]].
- If the initializer is `()`, the object is value-initialized.
- Otherwise, if the destination type is an array, the object is
  initialized as follows. Let x₁, …, xₖ be the elements of the
  *expression-list*. If the destination type is an array of unknown
  bound, it is defined as having k elements. Let n denote the array size
  after this potential adjustment. If k is greater than n, the program
  is ill-formed. Otherwise, the iᵗʰ array element is copy-initialized
  with xᵢ for each 1 ≤ i ≤ k, and value-initialized for each k < i ≤ n.
  For each 1 ≤ i < j ≤ n, every value computation and side effect
  associated with the initialization of the iᵗʰ element of the array is
  sequenced before those associated with the initialization of the jᵗʰ
  element.
- Otherwise, if the destination type is a (possibly cv-qualified) class
  type:
  - If the initializer expression is a prvalue and the cv-unqualified
    version of the source type is the same class as the class of the
    destination, the initializer expression is used to initialize the
    destination object. \[*Example 1*: `T x = T(T(T()));` calls the `T`
    default constructor to initialize `x`. — *end example*]
  - Otherwise, if the initialization is direct-initialization, or if it
    is copy-initialization where the cv-unqualified version of the
    source type is the same class as, or a derived class of, the class
    of the destination, constructors are considered. The applicable
    constructors are enumerated [[over.match.ctor]], and the best one is
    chosen through overload resolution [[over.match]]. Then:
    - If overload resolution is successful, the selected constructor is
      called to initialize the object, with the initializer expression
      or *expression-list* as its argument(s).
    - Otherwise, if no constructor is viable, the destination type is an
      aggregate class, and the initializer is a parenthesized
      *expression-list*, the object is initialized as follows. Let e₁,
      …, eₙ be the elements of the aggregate [[dcl.init.aggr]]. Let x₁,
      …, xₖ be the elements of the *expression-list*. If k is greater
      than n, the program is ill-formed. The element eᵢ is
      copy-initialized with xᵢ for 1 ≤ i ≤ k. The remaining elements are
      initialized with their default member initializers, if any, and
      otherwise are value-initialized. For each 1 ≤ i < j ≤ n, every
      value computation and side effect associated with the
      initialization of eᵢ is sequenced before those associated with the
      initialization of eⱼ.
      \[*Note 2*:
      By contrast with direct-list-initialization, narrowing conversions
      [[dcl.init.list]] are permitted, designators are not permitted, a
      temporary object bound to a reference does not have its lifetime
      extended [[class.temporary]], and there is no brace elision.
      \[*Example 2*:
      ``` cpp
      struct A {
        int a;
        int&& r;
      };

      int f();
      int n = 10;

      A a1{1, f()};                   // OK, lifetime is extended
      A a2(1, f());                   // well-formed, but dangling reference
      A a3{1.0, 1};                   // error: narrowing conversion
      A a4(1.0, 1);                   // well-formed, but dangling reference
      A a5(1.0, std::move(n));        // OK
      ```

      — *end example*]
      — *end note*]
    - Otherwise, the initialization is ill-formed.
  - Otherwise (i.e., for the remaining copy-initialization cases),
    user-defined conversions that can convert from the source type to
    the destination type or (when a conversion function is used) to a
    derived class thereof are enumerated as described in 
    [[over.match.copy]], and the best one is chosen through overload
    resolution [[over.match]]. If the conversion cannot be done or is
    ambiguous, the initialization is ill-formed. The function selected
    is called with the initializer expression as its argument; if the
    function is a constructor, the call is a prvalue of the
    cv-unqualified version of the destination type whose result object
    is initialized by the constructor. The call is used to
    direct-initialize, according to the rules above, the object that is
    the destination of the copy-initialization.
- Otherwise, if the source type is a (possibly cv-qualified) class type,
  conversion functions are considered. The applicable conversion
  functions are enumerated [[over.match.conv]], and the best one is
  chosen through overload resolution [[over.match]]. The user-defined
  conversion so selected is called to convert the initializer expression
  into the object being initialized. If the conversion cannot be done or
  is ambiguous, the initialization is ill-formed.
- Otherwise, if the initialization is direct-initialization, the source
  type is `std::nullptr_t`, and the destination type is `bool`, the
  initial value of the object being initialized is `false`.
- Otherwise, the initial value of the object being initialized is the
  (possibly converted) value of the initializer expression. A standard
  conversion sequence [[conv]] will be used, if necessary, to convert
  the initializer expression to the cv-unqualified version of the
  destination type; no user-defined conversions are considered. If the
  conversion cannot be done, the initialization is ill-formed. When
  initializing a bit-field with a value that it cannot represent, the
  resulting value of the bit-field is .
  \[*Note 3*:
  An expression of type “cv-qualifiercv1 `T`” can initialize an object
  of type “cv-qualifiercv2 `T`” independently of the cv-qualifiers
  cv-qualifiercv1 and cv-qualifiercv2.
  ``` cpp
  int a;
  const int b = a;
  int c = b;
  ```

  — *end note*]

An *initializer-clause* followed by an ellipsis is a pack expansion
[[temp.variadic]].

If the initializer is a parenthesized *expression-list*, the expressions
are evaluated in the order specified for function calls [[expr.call]].

The same *identifier* shall not appear in multiple *designator*s of a
*designated-initializer-list*.

An object whose initialization has completed is deemed to be
constructed, even if the object is of non-class type or no constructor
of the object’s class is invoked for the initialization.

[*Note 7*: Such an object might have been value-initialized or
initialized by aggregate initialization [[dcl.init.aggr]] or by an
inherited constructor [[class.inhctor.init]]. — *end note*]

Destroying an object of class type invokes the destructor of the class.
Destroying a scalar type has no effect other than ending the lifetime of
the object [[basic.life]]. Destroying an array destroys each element in
reverse subscript order.

A declaration that specifies the initialization of a variable, whether
from an explicit initializer or by default-initialization, is called the
*initializing declaration* of that variable.

[*Note 8*: In most cases this is the defining declaration [[basic.def]]
of the variable, but the initializing declaration of a non-inline static
data member [[class.static.data]] might be the declaration within the
class definition and not the definition at namespace
scope. — *end note*]

### Aggregates <a id="dcl.init.aggr">[[dcl.init.aggr]]</a>

An *aggregate* is an array or a class [[class]] with

- no user-declared or inherited constructors [[class.ctor]],
- no private or protected direct non-static data members
  [[class.access]],
- no virtual functions [[class.virtual]], and
- no virtual, private, or protected base classes [[class.mi]].

[*Note 1*: Aggregate initialization does not allow accessing protected
and private base class’ members or constructors. — *end note*]

The *elements* of an aggregate are:

- for an array, the array elements in increasing subscript order, or
- for a class, the direct base classes in declaration order, followed by
  the direct non-static data members [[class.mem]] that are not members
  of an anonymous union, in declaration order.

When an aggregate is initialized by an initializer list as specified in 
[[dcl.init.list]], the elements of the initializer list are taken as
initializers for the elements of the aggregate. The
*explicitly initialized elements* of the aggregate are determined as
follows:

- If the initializer list is a *designated-initializer-list*, the
  aggregate shall be of class type, the *identifier* in each
  *designator* shall name a direct non-static data member of the class,
  and the explicitly initialized elements of the aggregate are the
  elements that are, or contain, those members.
- If the initializer list is an *initializer-list*, the explicitly
  initialized elements of the aggregate are the first n elements of the
  aggregate, where n is the number of elements in the initializer list.
- Otherwise, the initializer list must be `{}`, and there are no
  explicitly initialized elements.

For each explicitly initialized element:

- If the element is an anonymous union object and the initializer list
  is a *designated-initializer-list*, the anonymous union object is
  initialized by the *designated-initializer-list* `{ `*D*` }`, where
  *D* is the *designated-initializer-clause* naming a member of the
  anonymous union object. There shall be only one such
  *designated-initializer-clause*.
  \[*Example 3*:
  ``` cpp
  struct C {
    union {
      int a;
      const char* p;
    };
    int x;
  } c = { .a = 1, .x = 3 };
  ```

  initializes `c.a` with 1 and `c.x` with 3.
  — *end example*]
- Otherwise, the element is copy-initialized from the corresponding
  *initializer-clause* or is initialized with the
  *brace-or-equal-initializer* of the corresponding
  *designated-initializer-clause*. If that initializer is of the form
  *assignment-expression* or `= `*assignment-expression* and a narrowing
  conversion [[dcl.init.list]] is required to convert the expression,
  the program is ill-formed.
  \[*Note 4*: If an initializer is itself an initializer list, the
  element is list-initialized, which will result in a recursive
  application of the rules in this subclause if the element is an
  aggregate. — *end note*]
  \[*Example 4*:
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
  ``` cpp
  struct base1 { int b1, b2 = 42; };
  struct base2 {
    base2() {
      b3 = 42;
    }
    int b3;
  };
  struct derived : base1, base2 {
    int d;
  };

  derived d1{{1, 2}, {}, 4};
  derived d2{{}, {}, 4};
  ```

  initializes `d1.b1` with 1, `d1.b2` with 2, `d1.b3` with 42, `d1.d`
  with 4, and `d2.b1` with 0, `d2.b2` with 42, `d2.b3` with 42, `d2.d`
  with 4.
  — *end example*]

For a non-union aggregate, each element that is not an explicitly
initialized element is initialized as follows:

- If the element has a default member initializer [[class.mem]], the
  element is initialized from that initializer.
- Otherwise, if the element is not a reference, the element is
  copy-initialized from an empty initializer list [[dcl.init.list]].
- Otherwise, the program is ill-formed.

If the aggregate is a union and the initializer list is empty, then

- if any variant member has a default member initializer, that member is
  initialized from its default member initializer;
- otherwise, the first member of the union (if any) is copy-initialized
  from an empty initializer list.

[*Example 1*:

``` cpp
struct S { int a; const char* b; int c; int d = b[a]; };
S ss = { 1, "asdf" };
```

initializes `ss.a` with 1, `ss.b` with `"asdf"`, `ss.c` with the value
of an expression of the form `int{}` (that is, `0`), and `ss.d` with the
value of `ss.b[ss.a]` (that is, `'s'`), and in

``` cpp
struct X { int i, j, k = 42; };
X a[] = { 1, 2, 3, 4, 5, 6 };
X b[2] = { { 1, 2, 3 }, { 4, 5, 6 } };
```

`a` and `b` have the same value

``` cpp
struct A {
  string a;
  int b = 42;
  int c = -1;
};
```

`A{.c=21}` has the following steps:

- Initialize `a` with `{}`
- Initialize `b` with `= 42`
- Initialize `c` with `= 21`

— *end example*]

The initializations of the elements of the aggregate are evaluated in
the element order. That is, all value computations and side effects
associated with a given element are sequenced before those of any
element that follows it in order.

An aggregate that is a class can also be initialized with a single
expression not enclosed in braces, as described in  [[dcl.init]].

The destructor for each element of class type is potentially invoked
[[class.dtor]] from the context where the aggregate initialization
occurs.

[*Note 2*: This provision ensures that destructors can be called for
fully-constructed subobjects in case an exception is thrown
[[except.ctor]]. — *end note*]

An array of unknown bound initialized with a brace-enclosed
*initializer-list* containing `n` *initializer-clause*s is defined as
having `n` elements [[dcl.array]].

[*Example 2*:

``` cpp
int x[] = { 1, 3, 5 };
```

declares and initializes `x` as a one-dimensional array that has three
elements since no size was specified and there are three initializers.

— *end example*]

An array of unknown bound shall not be initialized with an empty
*braced-init-list* `{}`. [^6]

[*Note 3*:

A default member initializer does not determine the bound for a member
array of unknown bound. Since the default member initializer is ignored
if a suitable *mem-initializer* is present [[class.base.init]], the
default member initializer is not considered to initialize the array of
unknown bound.

[*Example 3*:

``` cpp
struct S {
  int y[] = { 0 };          // error: non-static data member of incomplete type
};
```

— *end example*]

— *end note*]

[*Note 4*:

Static data members, non-static data members of anonymous union members,
and unnamed bit-fields are not considered elements of the aggregate.

[*Example 4*:

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
unnamed bit-field before it.

— *end example*]

— *end note*]

An *initializer-list* is ill-formed if the number of
*initializer-clause*s exceeds the number of elements of the aggregate.

[*Example 5*:

``` cpp
char cv[4] = { 'a', 's', 'd', 'f', 0 };     // error
```

is ill-formed.

— *end example*]

If a member has a default member initializer and a potentially-evaluated
subexpression thereof is an aggregate initialization that would use that
default member initializer, the program is ill-formed.

[*Example 6*:

``` cpp
struct A;
extern A a;
struct A {
  const A& a1 { A{a,a} };       // OK
  const A& a2 { A{} };          // error
};
A a{a,a};                       // OK

struct B {
  int n = B{}.n;                // error
};
```

— *end example*]

If an aggregate class `C` contains a subaggregate element `e` with no
elements, the *initializer-clause* for `e` shall not be omitted from an
*initializer-list* for an object of type `C` unless the
*initializer-clause*s for all elements of `C` following `e` are also
omitted.

[*Example 7*:

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
  { },              // Required initialization
  0,
  s,                // Required initialization
  0
};                  // Initialization not required for A::s3 because A::i3 is also not initialized
```

— *end example*]

When initializing a multi-dimensional array, the *initializer-clause*s
initialize the elements with the last (rightmost) index of the array
varying the fastest [[dcl.array]].

[*Example 8*:

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

— *end example*]

Braces can be elided in an *initializer-list* as follows. If the
*initializer-list* begins with a left brace, then the succeeding
comma-separated list of *initializer-clause*s initializes the elements
of a subaggregate; it is erroneous for there to be more
*initializer-clause*s than elements. If, however, the *initializer-list*
for a subaggregate does not begin with a left brace, then only enough
*initializer-clause*s from the list are taken to initialize the elements
of the subaggregate; any remaining *initializer-clause*s are left to
initialize the next element of the aggregate of which the current
subaggregate is an element.

[*Example 9*:

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

— *end example*]

All implicit type conversions [[conv]] are considered when initializing
the element with an *assignment-expression*. If the
*assignment-expression* can initialize an element, the element is
initialized. Otherwise, if the element is itself a subaggregate, brace
elision is assumed and the *assignment-expression* is considered for the
initialization of the first element of the subaggregate.

[*Note 5*: As specified above, brace elision cannot apply to
subaggregates with no elements; an *initializer-clause* for the entire
subobject is required. — *end note*]

[*Example 10*:

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

— *end example*]

[*Note 6*: An aggregate array or an aggregate class may contain
elements of a class type with a user-declared constructor
[[class.ctor]]. Initialization of these aggregate objects is described
in  [[class.expl.init]]. — *end note*]

[*Note 7*: Whether the initialization of aggregates with static storage
duration is static or dynamic is specified in  [[basic.start.static]],
[[basic.start.dynamic]], and  [[stmt.dcl]]. — *end note*]

When a union is initialized with an initializer list, there shall not be
more than one explicitly initialized element.

[*Example 11*:

``` cpp
union u { int a; const char* b; };
u a = { 1 };
u b = a;
u c = 1;                        // error
u d = { 0, "asdf" };            // error
u e = { "asdf" };               // error
u f = { .b = "asdf" };
u g = { .a = 1, .b = "asdf" };  // error
```

— *end example*]

[*Note 8*: As described above, the braces around the
*initializer-clause* for a union member can be omitted if the union is a
member of another aggregate. — *end note*]

### Character arrays <a id="dcl.init.string">[[dcl.init.string]]</a>

An array of ordinary character type [[basic.fundamental]], `char8_t`
array, `char16_t` array, `char32_t` array, or `wchar_t` array can be
initialized by an ordinary string literal, UTF-8 string literal, UTF-16
string literal, UTF-32 string literal, or wide string literal,
respectively, or by an appropriately-typed *string-literal* enclosed in
braces [[lex.string]]. Successive characters of the value of the
*string-literal* initialize the elements of the array.

[*Example 1*:

``` cpp
char msg[] = "Syntax error on line %s\n";
```

shows a character array whose members are initialized with a
*string-literal*. Note that because `'\n'` is a single character and
because a trailing `'\0'` is appended, `sizeof(msg)` is `25`.

— *end example*]

There shall not be more initializers than there are array elements.

[*Example 2*:

``` cpp
char cv[4] = "asdf";            // error
```

is ill-formed since there is no space for the implied trailing `'\0'`.

— *end example*]

If there are fewer initializers than there are array elements, each
element not explicitly initialized shall be zero-initialized
[[dcl.init]].

### References <a id="dcl.init.ref">[[dcl.init.ref]]</a>

A variable whose declared type is “reference to type `T`” [[dcl.ref]]
shall be initialized.

[*Example 1*:

``` cpp
int g(int) noexcept;
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

— *end example*]

A reference cannot be changed to refer to another object after
initialization.

[*Note 1*: Assignment to a reference assigns to the object referred to
by the reference [[expr.ass]]. — *end note*]

Argument passing [[expr.call]] and function value return [[stmt.return]]
are initializations.

The initializer can be omitted for a reference only in a parameter
declaration [[dcl.fct]], in the declaration of a function return type,
in the declaration of a class member within its class definition
[[class.mem]], and where the `extern` specifier is explicitly used.

[*Example 2*:

``` cpp
int& r1;                        // error: initializer missing
extern int& r2;                 // OK
```

— *end example*]

Given types “cv-qualifiercv1 `T1`” and “cv-qualifiercv2 `T2`”,
“cv-qualifiercv1 `T1`” is *reference-related* to “cv-qualifiercv2 `T2`”
if `T1` is similar [[conv.qual]] to `T2`, or `T1` is a base class of
`T2`. “cv-qualifiercv1 `T1`” is *reference-compatible* with
“cv-qualifiercv2 `T2`” if a prvalue of type “pointer to cv-qualifiercv2
`T2`” can be converted to the type “pointer to cv-qualifiercv1 `T1`” via
a standard conversion sequence [[conv]]. In all cases where the
reference-compatible relationship of two types is used to establish the
validity of a reference binding and the standard conversion sequence
would be ill-formed, a program that necessitates such a binding is
ill-formed.

A reference to type “cv-qualifiercv1 `T1`” is initialized by an
expression of type “cv-qualifiercv2 `T2`” as follows:

- If the reference is an lvalue reference and the initializer expression
  - is an lvalue (but is not a bit-field), and “cv-qualifiercv1 `T1`” is
    reference-compatible with “cv-qualifiercv2 `T2`”, or
  - has a class type (i.e., `T2` is a class type), where `T1` is not
    reference-related to `T2`, and can be converted to an lvalue of type
    “cv-qualifiercv3 `T3`”, where “cv-qualifiercv1 `T1`” is
    reference-compatible with “cv-qualifiercv3 `T3`”[^7] (this
    conversion is selected by enumerating the applicable conversion
    functions [[over.match.ref]] and choosing the best one through
    overload resolution [[over.match]]),

  then the reference is bound to the initializer expression lvalue in
  the first case and to the lvalue result of the conversion in the
  second case (or, in either case, to the appropriate base class
  subobject of the object).
  \[*Note 5*: The usual lvalue-to-rvalue [[conv.lval]], array-to-pointer
  [[conv.array]], and function-to-pointer [[conv.func]] standard
  conversions are not needed, and therefore are suppressed, when such
  direct bindings to lvalues are done. — *end note*]
  \[*Example 5*:
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

  — *end example*]
- Otherwise, if the reference is an lvalue reference to a type that is
  not const-qualified or is volatile-qualified, the program is
  ill-formed.
  \[*Example 6*:
  ``` cpp
  double& rd2 = 2.0;              // error: not an lvalue and reference not const
  int  i = 2;
  double& rd3 = i;                // error: type mismatch and reference not const
  ```

  — *end example*]
- Otherwise, if the initializer expression
  - is an rvalue (but not a bit-field) or function lvalue and
    “cv-qualifiercv1 `T1`” is reference-compatible with “cv-qualifiercv2
    `T2`”, or
  - has a class type (i.e., `T2` is a class type), where `T1` is not
    reference-related to `T2`, and can be converted to an rvalue or
    function lvalue of type “cv-qualifiercv3 `T3`”, where
    “cv-qualifiercv1 `T1`” is reference-compatible with “cv-qualifiercv3
    `T3`” (see  [[over.match.ref]]),

  then the value of the initializer expression in the first case and the
  result of the conversion in the second case is called the converted
  initializer. If the converted initializer is a prvalue, its type `T4`
  is adjusted to type “cv-qualifiercv1 `T4`” [[conv.qual]] and the
  temporary materialization conversion [[conv.rval]] is applied. In any
  case, the reference is bound to the resulting glvalue (or to an
  appropriate base class subobject).
  \[*Example 7*:
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
  ```

  — *end example*]
- Otherwise:
  - If `T1` or `T2` is a class type and `T1` is not reference-related to
    `T2`, user-defined conversions are considered using the rules for
    copy-initialization of an object of type “cv-qualifiercv1 `T1`” by
    user-defined conversion ([[dcl.init]], [[over.match.copy]],
    [[over.match.conv]]); the program is ill-formed if the corresponding
    non-reference copy-initialization would be ill-formed. The result of
    the call to the conversion function, as described for the
    non-reference copy-initialization, is then used to direct-initialize
    the reference. For this direct-initialization, user-defined
    conversions are not considered.
  - Otherwise, the initializer expression is implicitly converted to a
    prvalue of type “cv-qualifiercv1 `T1`”. The temporary
    materialization conversion is applied and the reference is bound to
    the result.

  If `T1` is reference-related to `T2`:
  - cv-qualifiercv1 shall be the same cv-qualification as, or greater
    cv-qualification than, cv-qualifiercv2; and
  - if the reference is an rvalue reference, the initializer expression
    shall not be an lvalue.

  \[*Example 8*:
  ``` cpp
  struct Banana { };
  struct Enigma { operator const Banana(); };
  struct Alaska { operator Banana&(); };
  void enigmatic() {
    typedef const Banana ConstBanana;
    Banana &&banana1 = ConstBanana(); // error
    Banana &&banana2 = Enigma();      // error
    Banana &&banana3 = Alaska();      // error
  }

  const double& rcd2 = 2;             // rcd2 refers to temporary with value 2.0
  double&& rrd = 2;                   // rrd refers to temporary with value 2.0
  const volatile int cvi = 1;
  const int& r2 = cvi;                // error: cv-qualifier dropped
  struct A { operator volatile int&(); } a;
  const int& r3 = a;                  // error: cv-qualifier dropped
                                      // from result of conversion function
  double d2 = 1.0;
  double&& rrd2 = d2;                 // error: initializer is lvalue of related type
  struct X { operator int&(); };
  int&& rri2 = X();                   // error: result of conversion function is lvalue of related type
  int i3 = 2;
  double&& rrd3 = i3;                 // rrd3 refers to temporary with value 2.0
  ```

  — *end example*]

In all cases except the last (i.e., implicitly converting the
initializer expression to the referenced type), the reference is said to
*bind directly* to the initializer expression.

[*Note 2*:  [[class.temporary]] describes the lifetime of temporaries
bound to references. — *end note*]

### List-initialization <a id="dcl.init.list">[[dcl.init.list]]</a>

*List-initialization* is initialization of an object or reference from a
*braced-init-list*. Such an initializer is called an *initializer list*,
and the comma-separated *initializer-clause*s of the *initializer-list*
or *designated-initializer-clause*s of the *designated-initializer-list*
are called the *elements* of the initializer list. An initializer list
may be empty. List-initialization can occur in direct-initialization or
copy-initialization contexts; list-initialization in a
direct-initialization context is called *direct-list-initialization* and
list-initialization in a copy-initialization context is called
*copy-list-initialization*.

[*Note 1*:

List-initialization can be used

- as the initializer in a variable definition [[dcl.init]]
- as the initializer in a *new-expression* [[expr.new]]
- in a `return` statement [[stmt.return]]
- as a *for-range-initializer* [[stmt.iter]]
- as a function argument [[expr.call]]
- as a subscript [[expr.sub]]
- as an argument to a constructor invocation ([[dcl.init]],
  [[expr.type.conv]])
- as an initializer for a non-static data member [[class.mem]]
- in a *mem-initializer* [[class.base.init]]
- on the right-hand side of an assignment [[expr.ass]]

[*Example 1*:

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

— *end example*]

— *end note*]

A constructor is an *initializer-list constructor* if its first
parameter is of type `std::initializer_list<E>` or reference to
cv `std::initializer_list<E>` for some type `E`, and either there are no
other parameters or else all other parameters have default arguments
[[dcl.fct.default]].

[*Note 2*: Initializer-list constructors are favored over other
constructors in list-initialization [[over.match.list]]. Passing an
initializer list as the argument to the constructor template
`template<class T> C(T)` of a class `C` does not create an
initializer-list constructor, because an initializer list argument
causes the corresponding parameter to be a non-deduced context
[[temp.deduct.call]]. — *end note*]

The template `std::initializer_list` is not predefined; if the header
`<initializer_list>` is not imported or included prior to a use of
`std::initializer_list` — even an implicit use in which the type is not
named [[dcl.spec.auto]] — the program is ill-formed.

List-initialization of an object or reference of type `T` is defined as
follows:

- If the *braced-init-list* contains a *designated-initializer-list*,
  `T` shall be an aggregate class. The ordered *identifier*s in the
  *designator*s of the *designated-initializer-list* shall form a
  subsequence of the ordered *identifier*s in the direct non-static data
  members of `T`. Aggregate initialization is performed
  [[dcl.init.aggr]].
  \[*Example 9*:
  ``` cpp
  struct A { int x; int y; int z; };
  A a{.y = 2, .x = 1};                // error: designator order does not match declaration order
  A b{.x = 1, .z = 2};                // OK, b.y initialized to 0
  ```

  — *end example*]
- If `T` is an aggregate class and the initializer list has a single
  element of type cv-qualifiercv `U`, where `U` is `T` or a class
  derived from `T`, the object is initialized from that element (by
  copy-initialization for copy-list-initialization, or by
  direct-initialization for direct-list-initialization).
- Otherwise, if `T` is a character array and the initializer list has a
  single element that is an appropriately-typed *string-literal*
  [[dcl.init.string]], initialization is performed as described in that
  subclause.
- Otherwise, if `T` is an aggregate, aggregate initialization is
  performed [[dcl.init.aggr]].
  \[*Example 10*:
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

  — *end example*]
- Otherwise, if the initializer list has no elements and `T` is a class
  type with a default constructor, the object is value-initialized.
- Otherwise, if `T` is a specialization of `std::initializer_list<E>`,
  the object is constructed as described below.
- Otherwise, if `T` is a class type, constructors are considered. The
  applicable constructors are enumerated and the best one is chosen
  through overload resolution ([[over.match]], [[over.match.list]]). If
  a narrowing conversion (see below) is required to convert any of the
  arguments, the program is ill-formed.
  \[*Example 11*:
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

  — *end example*]
  \[*Example 12*:
  ``` cpp
  struct Map {
    Map(std::initializer_list<std::pair<std::string,int>>);
  };
  Map ship = {{"Sophie",14}, {"Surprise",28}};
  ```

  — *end example*]
  \[*Example 13*:
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

  — *end example*]
- Otherwise, if `T` is an enumeration with a fixed underlying type
  [[dcl.enum]] `U`, the *initializer-list* has a single element `v`, `v`
  can be implicitly converted to `U`, and the initialization is
  direct-list-initialization, the object is initialized with the value
  `T(v)` [[expr.type.conv]]; if a narrowing conversion is required to
  convert `v` to `U`, the program is ill-formed.
  \[*Example 14*:
  ``` cpp
  enum byte : unsigned char { };
  byte b { 42 };                      // OK
  byte c = { 42 };                    // error
  byte d = byte{ 42 };                // OK; same value as b
  byte e { -1 };                      // error

  struct A { byte b; };
  A a1 = { { 42 } };                  // error
  A a2 = { byte{ 42 } };              // OK

  void f(byte);
  f({ 42 });                          // error

  enum class Handle : uint32_t { Invalid = 0 };
  Handle h { 42 };                    // OK
  ```

  — *end example*]
- Otherwise, if the initializer list has a single element of type `E`
  and either `T` is not a reference type or its referenced type is
  reference-related to `E`, the object or reference is initialized from
  that element (by copy-initialization for copy-list-initialization, or
  by direct-initialization for direct-list-initialization); if a
  narrowing conversion (see below) is required to convert the element to
  `T`, the program is ill-formed.
  \[*Example 15*:
  ``` cpp
  int x1 {2};                         // OK
  int x2 {2.0};                       // error: narrowing
  ```

  — *end example*]
- Otherwise, if `T` is a reference type, a prvalue is generated. The
  prvalue initializes its result object by copy-list-initialization. The
  prvalue is then used to direct-initialize the reference. The type of
  the temporary is the type referenced by `T`, unless `T` is “reference
  to array of unknown bound of `U`”, in which case the type of the
  temporary is the type of `x` in the declaration `U x[] H`, where H is
  the initializer list.
  \[*Note 6*: As usual, the binding will fail and the program is
  ill-formed if the reference type is an lvalue reference to a non-const
  type. — *end note*]
  \[*Example 16*:
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

  struct A { } a;
  struct B { explicit B(const A&); };
  const B& b2{a};                     // error: cannot copy-list-initialize B temporary from A
  ```

  — *end example*]
- Otherwise, if the initializer list has no elements, the object is
  value-initialized.
  \[*Example 17*:
  ``` cpp
  int** pp {};                        // initialized to null pointer
  ```

  — *end example*]
- Otherwise, the program is ill-formed.
  \[*Example 18*:
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

  — *end example*]

Within the *initializer-list* of a *braced-init-list*, the
*initializer-clause*s, including any that result from pack expansions
[[temp.variadic]], are evaluated in the order in which they appear. That
is, every value computation and side effect associated with a given
*initializer-clause* is sequenced before every value computation and
side effect associated with any *initializer-clause* that follows it in
the comma-separated list of the *initializer-list*.

[*Note 3*: This evaluation ordering holds regardless of the semantics
of the initialization; for example, it applies when the elements of the
*initializer-list* are interpreted as arguments of a constructor call,
even though ordinarily there are no sequencing constraints on the
arguments of a call. — *end note*]

An object of type `std::initializer_list<E>` is constructed from an
initializer list as if the implementation generated and materialized
[[conv.rval]] a prvalue of type “array of N `const E`”, where N is the
number of elements in the initializer list. Each element of that array
is copy-initialized with the corresponding element of the initializer
list, and the `std::initializer_list<E>` object is constructed to refer
to that array.

[*Note 4*: A constructor or conversion function selected for the copy
is required to be accessible [[class.access]] in the context of the
initializer list. — *end note*]

If a narrowing conversion is required to initialize any of the elements,
the program is ill-formed.

[*Example 2*:

``` cpp
struct X {
  X(std::initializer_list<double> v);
};
X x{ 1,2,3 };
```

The initialization will be implemented in a way roughly equivalent to
this:

``` cpp
const double __a[3] = {double{1}, double{2}, double{3}};
X x(std::initializer_list<double>(__a, __a+3));
```

assuming that the implementation can construct an `initializer_list`
object with a pair of pointers.

— *end example*]

The array has the same lifetime as any other temporary object
[[class.temporary]], except that initializing an `initializer_list`
object from the array extends the lifetime of the array exactly like
binding a reference to a temporary.

[*Example 3*:

``` cpp
typedef std::complex<double> cmplx;
std::vector<cmplx> v1 = { 1, 2, 3 };

void f() {
  std::vector<cmplx> v2{ 1, 2, 3 };
  std::initializer_list<int> i3 = { 1, 2, 3 };
}

struct A {
  std::initializer_list<int> i4;
  A() : i4{ 1, 2, 3 } {}            // ill-formed, would create a dangling reference
};
```

For `v1` and `v2`, the `initializer_list` object is a parameter in a
function call, so the array created for `{ 1, 2, 3 }` has
full-expression lifetime. For `i3`, the `initializer_list` object is a
variable, so the array persists for the lifetime of the variable. For
`i4`, the `initializer_list` object is initialized in the constructor’s
*ctor-initializer* as if by binding a temporary array to a reference
member, so the program is ill-formed [[class.base.init]].

— *end example*]

[*Note 5*: The implementation is free to allocate the array in
read-only memory if an explicit array with the same initializer could be
so allocated. — *end note*]

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
  where the source is a constant expression whose value after integral
  promotions will fit into the target type, or
- from a pointer type or a pointer-to-member type to `bool`.

[*Note 6*: As indicated above, such conversions are not allowed at the
top level in list-initializations. — *end note*]

[*Example 4*:

``` cpp
int x = 999;                    // x is not a constant expression
const int y = 999;
const int z = 99;
char c1 = x;                    // OK, though it might narrow (in this case, it does narrow)
char c2{x};                     // error: might narrow
char c3{y};                     // error: narrows (assuming char is 8 bits)
char c4{z};                     // OK: no narrowing needed
unsigned char uc1 = {5};        // OK: no narrowing needed
unsigned char uc2 = {-1};       // error: narrows
unsigned int ui1 = {-1};        // error: narrows
signed int si1 =
  { (unsigned int)-1 };         // error: narrows
int ii = {2.0};                 // error: narrows
float f1 { x };                 // error: might narrow
float f2 { 7 };                 // OK: 7 can be exactly represented as a float
bool b = {"meow"};              // error: narrows
int f(int);
int a[] = { 2, f(2), f(2.0) };  // OK: the double-to-int conversion is not at the top level
```

— *end example*]

## Function definitions <a id="dcl.fct.def">[[dcl.fct.def]]</a>

### In general <a id="dcl.fct.def.general">[[dcl.fct.def.general]]</a>

Function definitions have the form

``` bnf
function-definition:
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator virt-specifier-seqₒₚₜ function-body
    attribute-specifier-seqₒₚₜ decl-specifier-seqₒₚₜ declarator requires-clause function-body
```

``` bnf
function-body:
    ctor-initializerₒₚₜ compound-statement
    function-try-block
    '=' default ';'
    '=' delete ';'
```

Any informal reference to the body of a function should be interpreted
as a reference to the non-terminal *function-body*. The optional
*attribute-specifier-seq* in a *function-definition* appertains to the
function. A *virt-specifier-seq* can be part of a *function-definition*
only if it is a *member-declaration* [[class.mem]].

In a *function-definition*, either `void` *declarator* `;` or
*declarator* `;` shall be a well-formed function declaration as
described in  [[dcl.fct]]. A function shall be defined only in namespace
or class scope. The type of a parameter or the return type for a
function definition shall not be a (possibly cv-qualified) class type
that is incomplete or abstract within the function body unless the
function is deleted [[dcl.fct.def.delete]].

[*Example 1*:

A simple example of a complete function definition is

``` cpp
int max(int a, int b, int c) {
  int m = (a > b) ? a : b;
  return (m > c) ? m : c;
}
```

Here `int` is the *decl-specifier-seq*; `max(int` `a,` `int` `b,` `int`
`c)` is the *declarator*; `{ \commentellip{} }` is the *function-body*.

— *end example*]

A *ctor-initializer* is used only in a constructor; see  [[class.ctor]]
and  [[class.init]].

[*Note 1*: A *cv-qualifier-seq* affects the type of `this` in the body
of a member function; see  [[dcl.ref]]. — *end note*]

[*Note 2*:

Unused parameters need not be named. For example,

``` cpp
void print(int a, int) {
  std::printf("a = %d\n",a);
}
```

— *end note*]

In the *function-body*, a *function-local predefined variable* denotes a
block-scope object of static storage duration that is implicitly defined
(see  [[basic.scope.block]]).

The function-local predefined variable `__func__` is defined as if a
definition of the form

``` cpp
static const char __func__[] = "function-name";
```

had been provided, where `function-name` is an *implementation-defined*
string. It is unspecified whether such a variable has an address
distinct from that of any other object in the program.[^8]

[*Example 2*:

``` cpp
struct S {
  S() : s(__func__) { }             // OK
  const char* s;
};
void f(const char* s = __func__);   // error: __func__ is undeclared
```

— *end example*]

### Explicitly-defaulted functions <a id="dcl.fct.def.default">[[dcl.fct.def.default]]</a>

A function definition whose *function-body* is of the form `= default ;`
is called an *explicitly-defaulted* definition. A function that is
explicitly defaulted shall

- be a special member function or a comparison operator function
  [[over.binary]], and
- not have default arguments.

The type `T`₁ of an explicitly defaulted special member function `F` is
allowed to differ from the type `T`₂ it would have had if it were
implicitly declared, as follows:

- `T`₁ and `T`₂ may have differing *ref-qualifier*s;
- `T`₁ and `T`₂ may have differing exception specifications; and
- if `T`₂ has a parameter of type `const C&`, the corresponding
  parameter of `T`₁ may be of type `C&`.

If `T`₁ differs from `T`₂ in any other way, then:

- if `F` is an assignment operator, and the return type of `T`₁ differs
  from the return type of `T`₂ or `T`₁’s parameter type is not a
  reference, the program is ill-formed;
- otherwise, if `F` is explicitly defaulted on its first declaration, it
  is defined as deleted;
- otherwise, the program is ill-formed.

An explicitly-defaulted function that is not defined as deleted may be
declared `constexpr` or `consteval` only if it is constexpr-compatible (
[[special]], [[class.compare.default]]). A function explicitly defaulted
on its first declaration is implicitly inline [[dcl.inline]], and is
implicitly constexpr [[dcl.constexpr]] if it is constexpr-compatible.

[*Example 1*:

``` cpp
struct S {
  constexpr S() = default;              // error: implicit S() is not constexpr
  S(int a = 0) = default;               // error: default argument
  void operator=(const S&) = default;   // error: non-matching return type
  ~S() noexcept(false) = default;       // OK, despite mismatched exception specification
private:
  int i;
  S(S&);                                // OK: private copy constructor
};
S::S(S&) = default;                     // OK: defines copy constructor

struct T {
  T();
  T(T &&) noexcept(false);
};
struct U {
  T t;
  U();
  U(U &&) noexcept = default;
};
U u1;
U u2 = static_cast<U&&>(u1);            // OK, calls std::terminate if T::T(T&&) throws
```

— *end example*]

Explicitly-defaulted functions and implicitly-declared functions are
collectively called *defaulted* functions, and the implementation shall
provide implicit definitions for them ([[class.ctor]], [[class.dtor]],
[[class.copy.ctor]], [[class.copy.assign]]), which might mean defining
them as deleted. A defaulted prospective destructor [[class.dtor]] that
is not a destructor is defined as deleted. A defaulted special member
function that is neither a prospective destructor nor an eligible
special member function [[special]] is defined as deleted. A function is
*user-provided* if it is user-declared and not explicitly defaulted or
deleted on its first declaration. A user-provided explicitly-defaulted
function (i.e., explicitly defaulted after its first declaration) is
defined at the point where it is explicitly defaulted; if such a
function is implicitly defined as deleted, the program is ill-formed.

[*Note 1*: Declaring a function as defaulted after its first
declaration can provide efficient execution and concise definition while
enabling a stable binary interface to an evolving code
base. — *end note*]

[*Example 2*:

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
nontrivial1::nontrivial1() = default;   // not first declaration
```

— *end example*]

### Deleted definitions <a id="dcl.fct.def.delete">[[dcl.fct.def.delete]]</a>

A function definition whose *function-body* is of the form `= delete ;`
is called a *deleted definition*. A function with a deleted definition
is also called a *deleted function*.

A program that refers to a deleted function implicitly or explicitly,
other than to declare it, is ill-formed.

[*Note 1*: This includes calling the function implicitly or explicitly
and forming a pointer or pointer-to-member to the function. It applies
even for references in expressions that are not potentially-evaluated.
If a function is overloaded, it is referenced only if the function is
selected by overload resolution. The implicit odr-use [[basic.def.odr]]
of a virtual function does not, by itself, constitute a
reference. — *end note*]

[*Example 1*:

One can prevent default initialization and initialization by
non-`double`s with

``` cpp
struct onlydouble {
  onlydouble() = delete;                // OK, but redundant
  template<class T>
    onlydouble(T) = delete;
  onlydouble(double);
};
```

— *end example*]

[*Example 2*:

One can prevent use of a class in certain *new-expression*s by using
deleted definitions of a user-declared `operator new` for that class.

``` cpp
struct sometype {
  void* operator new(std::size_t) = delete;
  void* operator new[](std::size_t) = delete;
};
sometype* p = new sometype;     // error: deleted class operator new
sometype* q = new sometype[3];  // error: deleted class operator new[]
```

— *end example*]

[*Example 3*:

One can make a class uncopyable, i.e., move-only, by using deleted
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
moveonly* p;
moveonly q(*p);                 // error: deleted copy constructor
```

— *end example*]

A deleted function is implicitly an inline function [[dcl.inline]].

[*Note 2*: The one-definition rule [[basic.def.odr]] applies to deleted
definitions. — *end note*]

A deleted definition of a function shall be the first declaration of the
function or, for an explicit specialization of a function template, the
first declaration of that specialization. An implicitly declared
allocation or deallocation function [[basic.stc.dynamic]] shall not be
defined as deleted.

[*Example 4*:

``` cpp
struct sometype {
  sometype();
};
sometype::sometype() = delete;  // error: not first declaration
```

— *end example*]

### Coroutine definitions <a id="dcl.fct.def.coroutine">[[dcl.fct.def.coroutine]]</a>

A function is a *coroutine* if its *function-body* encloses a
*coroutine-return-statement* [[stmt.return.coroutine]], an
*await-expression* [[expr.await]], or a *yield-expression*
[[expr.yield]]. The *parameter-declaration-clause* of the coroutine
shall not terminate with an ellipsis that is not part of a
*parameter-declaration*.

[*Example 1*:

``` cpp
task<int> f();

task<void> g1() {
  int i = co_await f();
  std::cout << "f() => " << i << std::endl;
}

template <typename... Args>
task<void> g2(Args&&...) {      // OK, ellipsis is a pack expansion
  int i = co_await f();
  std::cout << "f() => " << i << std::endl;
}

task<void> g3(int a, ...) {     // error: variable parameter list not allowed
  int i = co_await f();
  std::cout << "f() => " << i << std::endl;
}
```

— *end example*]

The *promise type* of a coroutine is
`std::coroutine_traits<R, P_1, \dotsc, P_n>::promise_type`, where `R` is
the return type of the function, and `P₁` \dotsc `Pₙ` are the sequence
of types of the function parameters, preceded by the type of the
implicit object parameter [[over.match.funcs]] if the coroutine is a
non-static member function. The promise type shall be a class type.

In the following, `pᵢ` is an lvalue of type `Pᵢ`, where `p₁` denotes
`*this` and `p_i+1` denotes the $i^\textrm{th}$ function parameter for a
non-static member function, and `pᵢ` denotes the $i^\textrm{th}$
function parameter otherwise.

A coroutine behaves as if its *function-body* were replaced by:

``` bnf
'{'
   *promise-type* \textit{promise} *promise-constructor-arguments* ';'
% FIXME:    \exposid{promise}'.get_return_object()' ';'
% ... except that it's not a discarded-value expression
   'try' '{'
     'co_await' '\textit{promise}.initial_suspend()' ';'
     function-body
   '} catch ( ... ) {'
     'if (!\textit{initial-await-resume-called})'
       'throw' ';'
     '\textit{promise}.unhandled_exception()' ';'
   '}'
\textit{final-suspend} ':'
   'co_await' '\textit{promise}.final_suspend()' ';'
'}'
```

where

- the *await-expression* containing the call to `initial_suspend` is the
  *initial suspend point*, and
- the *await-expression* containing the call to `final_suspend` is the
  *final suspend point*, and
- *initial-await-resume-called* is initially `false` and is set to
  `true` immediately before the evaluation of the *await-resume*
  expression [[expr.await]] of the initial suspend point, and
- *promise-type* denotes the promise type, and
- the object denoted by the exposition-only name *promise* is the
  *promise object* of the coroutine, and
- the label denoted by the name *final-suspend* is defined for
  exposition only [[stmt.return.coroutine]], and
- *promise-constructor-arguments* is determined as follows: overload
  resolution is performed on a promise constructor call created by
  assembling an argument list with lvalues `p₁` \dotsc `pₙ`. If a viable
  constructor is found [[over.match.viable]], then
  *promise-constructor-arguments* is `(p_1, \dotsc, p_n)`, otherwise
  *promise-constructor-arguments* is empty.

The *unqualified-id*s `return_void` and `return_value` are looked up in
the scope of the promise type. If both are found, the program is
ill-formed.

[*Note 1*: If the *unqualified-id* `return_void` is found, flowing off
the end of a coroutine is equivalent to a `co_return` with no operand.
Otherwise, flowing off the end of a coroutine results in undefined
behavior [[stmt.return.coroutine]]. — *end note*]

The expression `promise.get_return_object()` is used to initialize the
glvalue result or prvalue result object of a call to a coroutine. The
call to `get_return_object` is sequenced before the call to
`initial_suspend` and is invoked at most once.

A suspended coroutine can be resumed to continue execution by invoking a
resumption member function [[coroutine.handle.resumption]] of a
coroutine handle [[coroutine.handle]] that refers to the coroutine. The
function that invoked a resumption member function is called the
*resumer*. Invoking a resumption member function for a coroutine that is
not suspended results in undefined behavior.

An implementation may need to allocate additional storage for a
coroutine. This storage is known as the *coroutine state* and is
obtained by calling a non-array allocation function
[[basic.stc.dynamic.allocation]]. The allocation function’s name is
looked up in the scope of the promise type. If this lookup fails, the
allocation function’s name is looked up in the global scope. If the
lookup finds an allocation function in the scope of the promise type,
overload resolution is performed on a function call created by
assembling an argument list. The first argument is the amount of space
requested, and has type `std::size_t`. The lvalues `p₁` \dotsc `pₙ` are
the succeeding arguments. If no viable function is found
[[over.match.viable]], overload resolution is performed again on a
function call created by passing just the amount of space required as an
argument of type `std::size_t`.

The *unqualified-id* `get_return_object_on_allocation_failure` is looked
up in the scope of the promise type by class member access lookup
[[basic.lookup.classref]]. If any declarations are found, then the
result of a call to an allocation function used to obtain storage for
the coroutine state is assumed to return `nullptr` if it fails to obtain
storage, and if a global allocation function is selected, the
`::operator new(size_t, nothrow_t)` form is used. The allocation
function used in this case shall have a non-throwing
*noexcept-specification*. If the allocation function returns `nullptr`,
the coroutine returns control to the caller of the coroutine and the
return value is obtained by a call to
`T::get_return_object_on_allocation_failure()`, where `T` is the promise
type.

[*Example 2*:

``` cpp
#include <iostream>
#include <coroutine>

// ::operator new(size_t, nothrow_t) will be used if allocation is needed
struct generator {
  struct promise_type;
  using handle = std::coroutine_handle<promise_type>;
  struct promise_type {
    int current_value;
    static auto get_return_object_on_allocation_failure() { return generator{nullptr}; }
    auto get_return_object() { return generator{handle::from_promise(*this)}; }
    auto initial_suspend() { return std::suspend_always{}; }
    auto final_suspend() { return std::suspend_always{}; }
    void unhandled_exception() { std::terminate(); }
    void return_void() {}
    auto yield_value(int value) {
      current_value = value;
      return std::suspend_always{};
    }
  };
  bool move_next() { return coro ? (coro.resume(), !coro.done()) : false; }
  int current_value() { return coro.promise().current_value; }
  generator(generator const&) = delete;
  generator(generator && rhs) : coro(rhs.coro) { rhs.coro = nullptr; }
  ~generator() { if (coro) coro.destroy(); }
private:
  generator(handle h) : coro(h) {}
  handle coro;
};
generator f() { co_yield 1; co_yield 2; }
int main() {
  auto g = f();
  while (g.move_next()) std::cout << g.current_value() << std::endl;
}
```

— *end example*]

The coroutine state is destroyed when control flows off the end of the
coroutine or the `destroy` member function
[[coroutine.handle.resumption]] of a coroutine handle
[[coroutine.handle]] that refers to the coroutine is invoked. In the
latter case objects with automatic storage duration that are in scope at
the suspend point are destroyed in the reverse order of the
construction. The storage for the coroutine state is released by calling
a non-array deallocation function [[basic.stc.dynamic.deallocation]]. If
`destroy` is called for a coroutine that is not suspended, the program
has undefined behavior.

The deallocation function’s name is looked up in the scope of the
promise type. If this lookup fails, the deallocation function’s name is
looked up in the global scope. If deallocation function lookup finds
both a usual deallocation function with only a pointer parameter and a
usual deallocation function with both a pointer parameter and a size
parameter, then the selected deallocation function shall be the one with
two parameters. Otherwise, the selected deallocation function shall be
the function with one parameter. If no usual deallocation function is
found, the program is ill-formed. The selected deallocation function
shall be called with the address of the block of storage to be reclaimed
as its first argument. If a deallocation function with a parameter of
type `std::size_t` is used, the size of the block is passed as the
corresponding argument.

When a coroutine is invoked, after initializing its parameters
[[expr.call]], a copy is created for each coroutine parameter. For a
parameter of type cv `T`, the copy is a variable of type cv `T` with
automatic storage duration that is direct-initialized from an xvalue of
type `T` referring to the parameter.

[*Note 2*: An original parameter object is never a const or volatile
object [[basic.type.qualifier]]. — *end note*]

The initialization and destruction of each parameter copy occurs in the
context of the called coroutine. Initializations of parameter copies are
sequenced before the call to the coroutine promise constructor and
indeterminately sequenced with respect to each other. The lifetime of
parameter copies ends immediately after the lifetime of the coroutine
promise object ends.

[*Note 3*: If a coroutine has a parameter passed by reference, resuming
the coroutine after the lifetime of the entity referred to by that
parameter has ended is likely to result in undefined
behavior. — *end note*]

If the evaluation of the expression `promise.unhandled_exception()`
exits via an exception, the coroutine is considered suspended at the
final suspend point.

The expression `co_await` `promise.final_suspend()` shall not be
potentially-throwing [[except.spec]].

## Structured binding declarations <a id="dcl.struct.bind">[[dcl.struct.bind]]</a>

A structured binding declaration introduces the *identifier*s `v₀`,
`v₁`, `v₂`, \dotsc of the *identifier-list* as names
[[basic.scope.declarative]] of *structured binding*s. Let cv denote the
*cv-qualifier*s in the *decl-specifier-seq* and *S* consist of the
*storage-class-specifier*s of the *decl-specifier-seq* (if any). A cv
that includes `volatile` is deprecated; see  [[depr.volatile.type]].
First, a variable with a unique name *e* is introduced. If the
*assignment-expression* in the *initializer* has array type `A` and no
*ref-qualifier* is present, *e* is defined by

``` bnf
attribute-specifier-seqₒₚₜ *S* cv 'A' \textit{e} ';'
```

and each element is copy-initialized or direct-initialized from the
corresponding element of the *assignment-expression* as specified by the
form of the *initializer*. Otherwise, *e* is defined as-if by

``` bnf
attribute-specifier-seqₒₚₜ decl-specifier-seq ref-qualifierₒₚₜ \textit{e} initializer ';'
```

where the declaration is never interpreted as a function declaration and
the parts of the declaration other than the *declarator-id* are taken
from the corresponding structured binding declaration. The type of the
*id-expression* *e* is called `E`.

[*Note 1*: `E` is never a reference type [[expr.prop]]. — *end note*]

If the *initializer* refers to one of the names introduced by the
structured binding declaration, the program is ill-formed.

If `E` is an array type with element type `T`, the number of elements in
the *identifier-list* shall be equal to the number of elements of `E`.
Each `v`ᵢ is the name of an lvalue that refers to the element i of the
array and whose type is `T`; the referenced type is `T`.

[*Note 2*: The top-level cv-qualifiers of `T` are cv. — *end note*]

[*Example 1*:

``` cpp
auto f() -> int(&)[2];
auto [ x, y ] = f();            // x and y refer to elements in a copy of the array return value
auto& [ xr, yr ] = f();         // xr and yr refer to elements in the array referred to by f's return value
```

— *end example*]

Otherwise, if the *qualified-id* `std::tuple_size<E>` names a complete
class type with a member named `value`, the expression
`std::tuple_size<E>::value` shall be a well-formed integral constant
expression and the number of elements in the *identifier-list* shall be
equal to the value of that expression. Let `i` be an index prvalue of
type `std::size_t` corresponding to `v`_`i`. The *unqualified-id* `get`
is looked up in the scope of `E` by class member access lookup
[[basic.lookup.classref]], and if that finds at least one declaration
that is a function template whose first template parameter is a non-type
parameter, the initializer is `e.get<i>()`. Otherwise, the initializer
is `get<i>(e)`, where `get` is looked up in the associated namespaces
[[basic.lookup.argdep]]. In either case, `get<i>` is interpreted as a
*template-id*.

[*Note 3*: Ordinary unqualified lookup [[basic.lookup.unqual]] is not
performed. — *end note*]

In either case, *e* is an lvalue if the type of the entity *e* is an
lvalue reference and an xvalue otherwise. Given the type `Tᵢ` designated
by `std::tuple_element<i, E>::type` and the type `Uᵢ` designated by
either `\tcode{T}_i&` or `\tcode{T}_i&&`, where `Uᵢ` is an lvalue
reference if the initializer is an lvalue and an rvalue reference
otherwise, variables are introduced with unique names `rᵢ` as follows:

``` bnf
*S* 'Uᵢ rᵢ =' initializer ';'
```

Each `vᵢ` is the name of an lvalue of type `Tᵢ` that refers to the
object bound to `rᵢ`; the referenced type is `Tᵢ`.

Otherwise, all of `E`’s non-static data members shall be direct members
of `E` or of the same base class of `E`, well-formed when named as
`e.name` in the context of the structured binding, `E` shall not have an
anonymous union member, and the number of elements in the
*identifier-list* shall be equal to the number of non-static data
members of `E`. Designating the non-static data members of `E` as `m₀`,
`m₁`, `m₂`, \dotsc (in declaration order), each `v`ᵢ is the name of an
lvalue that refers to the member `m`ᵢ of *e* and whose type is cv `Tᵢ`,
where `Tᵢ` is the declared type of that member; the referenced type is
cv `Tᵢ`. The lvalue is a bit-field if that member is a bit-field.

[*Example 2*:

``` cpp
struct S { int x1 : 2; volatile double y1; };
S f();
const auto [ x, y ] = f();
```

The type of the *id-expression* `x` is “`const int`”, the type of the
*id-expression* `y` is “`const volatile double`”.

— *end example*]

## Enumerations <a id="enum">[[enum]]</a>

### Enumeration declarations <a id="dcl.enum">[[dcl.enum]]</a>

An enumeration is a distinct type [[basic.compound]] with named
constants. Its name becomes an *enum-name* within its scope.

``` bnf
enum-name:
    identifier
```

``` bnf
enum-specifier:
    enum-head \terminal{\ enumerator-listₒₚₜ \terminal{\}}
    enum-head \terminal{\ enumerator-list \terminal{,} \terminal{\}}
```

``` bnf
enum-head:
    enum-key attribute-specifier-seqₒₚₜ enum-head-nameₒₚₜ enum-baseₒₚₜ
```

``` bnf
enum-head-name:
    nested-name-specifierₒₚₜ identifier
```

``` bnf
opaque-enum-declaration:
    enum-key attribute-specifier-seqₒₚₜ enum-head-name enum-baseₒₚₜ ';'
```

``` bnf
enum-key:
    enum
    enum class
    enum struct
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
    identifier attribute-specifier-seqₒₚₜ
```

The optional *attribute-specifier-seq* in the *enum-head* and the
*opaque-enum-declaration* appertains to the enumeration; the attributes
in that *attribute-specifier-seq* are thereafter considered attributes
of the enumeration whenever it is named. A `:` following “`enum`
*nested-name-specifier*ₒₚₜ *identifier*” within the *decl-specifier-seq*
of a *member-declaration* is parsed as part of an *enum-base*.

[*Note 1*:

This resolves a potential ambiguity between the declaration of an
enumeration with an *enum-base* and the declaration of an unnamed
bit-field of enumeration type.

[*Example 1*:

``` cpp
struct S {
  enum E : int {};
  enum E : int {};              // error: redeclaration of enumeration
};
```

— *end example*]

— *end note*]

If the *enum-head-name* of an *opaque-enum-declaration* contains a
*nested-name-specifier*, the declaration shall be an explicit
specialization [[temp.expl.spec]].

The enumeration type declared with an *enum-key* of only `enum` is an
*unscoped enumeration*, and its *enumerator*s are
*unscoped enumerators*. The *enum-key*s `enum class` and `enum struct`
are semantically equivalent; an enumeration type declared with one of
these is a *scoped enumeration*, and its *enumerator*s are
*scoped enumerators*. The optional *enum-head-name* shall not be omitted
in the declaration of a scoped enumeration. The *type-specifier-seq* of
an *enum-base* shall name an integral type; any cv-qualification is
ignored. An *opaque-enum-declaration* declaring an unscoped enumeration
shall not omit the *enum-base*. The identifiers in an *enumerator-list*
are declared as constants, and can appear wherever constants are
required. An *enumerator-definition* with `=` gives the associated
*enumerator* the value indicated by the *constant-expression*. If the
first *enumerator* has no *initializer*, the value of the corresponding
constant is zero. An *enumerator-definition* without an *initializer*
gives the *enumerator* the value obtained by increasing the value of the
previous *enumerator* by one.

[*Example 2*:

``` cpp
enum { a, b, c=0 };
enum { d, e, f=e+2 };
```

defines `a`, `c`, and `d` to be zero, `b` and `e` to be `1`, and `f` to
be `3`.

— *end example*]

The optional *attribute-specifier-seq* in an *enumerator* appertains to
that enumerator.

An *opaque-enum-declaration* is either a redeclaration of an enumeration
in the current scope or a declaration of a new enumeration.

[*Note 2*: An enumeration declared by an *opaque-enum-declaration* has
a fixed underlying type and is a complete type. The list of enumerators
can be provided in a later redeclaration with an
*enum-specifier*. — *end note*]

A scoped enumeration shall not be later redeclared as unscoped or with a
different underlying type. An unscoped enumeration shall not be later
redeclared as scoped and each redeclaration shall include an *enum-base*
specifying the same underlying type as in the original declaration.

If an *enum-head-name* contains a *nested-name-specifier*, it shall not
begin with a *decltype-specifier* and the enclosing *enum-specifier* or
*opaque-enum-declaration* shall refer to an enumeration that was
previously declared directly in the class or namespace to which the
*nested-name-specifier* refers, or in an element of the inline namespace
set [[namespace.def]] of that namespace (i.e., neither inherited nor
introduced by a *using-declaration*), and the *enum-specifier* or
*opaque-enum-declaration* shall appear in a namespace enclosing the
previous declaration.

Each enumeration defines a type that is different from all other types.
Each enumeration also has an *underlying type*. The underlying type can
be explicitly specified using an *enum-base*. For a scoped enumeration
type, the underlying type is `int` if it is not explicitly specified. In
both of these cases, the underlying type is said to be *fixed*.
Following the closing brace of an *enum-specifier*, each enumerator has
the type of its enumeration. If the underlying type is fixed, the type
of each enumerator prior to the closing brace is the underlying type and
the *constant-expression* in the *enumerator-definition* shall be a
converted constant expression of the underlying type [[expr.const]]. If
the underlying type is not fixed, the type of each enumerator prior to
the closing brace is determined as follows:

- If an initializer is specified for an enumerator, the
  *constant-expression* shall be an integral constant expression
  [[expr.const]]. If the expression has unscoped enumeration type, the
  enumerator has the underlying type of that enumeration type, otherwise
  it has the same type as the expression.
- If no initializer is specified for the first enumerator, its type is
  an unspecified signed integral type.
- Otherwise the type of the enumerator is the same as that of the
  preceding enumerator unless the incremented value is not representable
  in that type, in which case the type is an unspecified integral type
  sufficient to contain the incremented value. If no such type exists,
  the program is ill-formed.

An enumeration whose underlying type is fixed is an incomplete type from
its point of declaration [[basic.scope.pdecl]] to immediately after its
*enum-base* (if any), at which point it becomes a complete type. An
enumeration whose underlying type is not fixed is an incomplete type
from its point of declaration to immediately after the closing `}` of
its *enum-specifier*, at which point it becomes a complete type.

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
enumeration are the values of the underlying type. Otherwise, the values
of the enumeration are the values representable by a hypothetical
integer type with minimal width M such that all enumerators can be
represented. The width of the smallest bit-field large enough to hold
all the values of the enumeration type is M. It is possible to define an
enumeration that has values not defined by any of its enumerators. If
the *enumerator-list* is empty, the values of the enumeration are as if
the enumeration had a single enumerator with value 0.[^9]

Two enumeration types are *layout-compatible enumerations* if they have
the same underlying type.

The value of an enumerator or an object of an unscoped enumeration type
is converted to an integer by integral promotion [[conv.prom]].

[*Example 3*:

``` cpp
enum color { red, yellow, green=20, blue };
color col = red;
color* cp = &col;
if (*cp == blue)                // ...
```

makes `color` a type describing various colors, and then declares `col`
as an object of that type, and `cp` as a pointer to an object of that
type. The possible values of an object of type `color` are `red`,
`yellow`, `green`, `blue`; these values can be converted to the integral
values `0`, `1`, `20`, and `21`. Since enumerations are distinct types,
objects of type `color` can be assigned only values of type `color`.

``` cpp
color c = 1;                    // error: type mismatch, no conversion from int to color
int i = yellow;                 // OK: yellow converted to integral value 1, integral promotion
```

Note that this implicit `enum` to `int` conversion is not provided for a
scoped enumeration:

``` cpp
enum class Col { red, yellow, green };
int x = Col::red;               // error: no Col to int conversion
Col y = Col::red;
if (y) { }                      // error: no Col to bool conversion
```

— *end example*]

Each *enum-name* and each unscoped *enumerator* is declared in the scope
that immediately contains the *enum-specifier*. Each scoped *enumerator*
is declared in the scope of the enumeration. An unnamed enumeration that
does not have a typedef name for linkage purposes [[dcl.typedef]] and
that has a first enumerator is denoted, for linkage purposes
[[basic.link]], by its underlying type and its first enumerator; such an
enumeration is said to have an enumerator as a name for linkage
purposes. These names obey the scope rules defined for all names in 
[[basic.scope]] and  [[basic.lookup]].

[*Note 3*: Each unnamed enumeration with no enumerators is a distinct
type. — *end note*]

[*Example 4*:

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

— *end example*]

An enumerator declared in class scope can be referred to using the class
member access operators (`::`, `.` (dot) and `->` (arrow)), see 
[[expr.ref]].

[*Example 5*:

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

— *end example*]

### The `using enum` declaration <a id="enum.udecl">[[enum.udecl]]</a>

``` bnf
using-enum-declaration:
    'using' elaborated-enum-specifier ';'
```

The *elaborated-enum-specifier* shall not name a dependent type and the
type shall have a reachable *enum-specifier*.

A *using-enum-declaration* introduces the enumerator names of the named
enumeration as if by a *using-declaration* for each enumerator.

[*Note 1*:

A *using-enum-declaration* in class scope adds the enumerators of the
named enumeration as members to the scope. This means they are
accessible for member lookup.

[*Example 1*:

``` cpp
enum class fruit { orange, apple };
struct S {
  using enum fruit;             // OK, introduces orange and apple into S
};
void f() {
  S s;
  s.orange;                     // OK, names fruit::orange
  S::orange;                    // OK, names fruit::orange
}
```

— *end example*]

— *end note*]

[*Note 2*:

Two *using-enum-declaration*s that introduce two enumerators of the same
name conflict.

[*Example 2*:

``` cpp
enum class fruit { orange, apple };
enum class color { red, orange };
void f() {
  using enum fruit;             // OK
  using enum color;             // error: color::orange and fruit::orange conflict
}
```

— *end example*]

— *end note*]

## Namespaces <a id="basic.namespace">[[basic.namespace]]</a>

A namespace is an optionally-named declarative region. The name of a
namespace can be used to access entities declared in that namespace;
that is, the members of the namespace. Unlike other declarative regions,
the definition of a namespace can be split over several parts of one or
more translation units.

[*Note 1*: A namespace name with external linkage is exported if any of
its *namespace-definition*s is exported, or if it contains any
*export-declaration*s [[module.interface]]. A namespace is never
attached to a module, and never has module linkage even if it is not
exported. — *end note*]

[*Example 1*:

``` cpp
export module M;
namespace N1 {}                 // N1 is not exported
export namespace N2 {}          // N2 is exported
namespace N3 { export int n; }  // N3 is exported
```

— *end example*]

The outermost declarative region of a translation unit is a namespace;
see  [[basic.scope.namespace]].

### Namespace definition <a id="namespace.def">[[namespace.def]]</a>

``` bnf
namespace-name:
        identifier
        namespace-alias
```

``` bnf
namespace-definition:
        named-namespace-definition
        unnamed-namespace-definition
        nested-namespace-definition
```

``` bnf
named-namespace-definition:
        inlineₒₚₜ namespace attribute-specifier-seqₒₚₜ identifier \terminal{\ namespace-body \terminal{\}}
```

``` bnf
unnamed-namespace-definition:
        inlineₒₚₜ namespace attribute-specifier-seqₒₚₜ \terminal{\ namespace-body \terminal{\}}
```

``` bnf
nested-namespace-definition:
        namespace enclosing-namespace-specifier '::' inlineₒₚₜ identifier \terminal{\ namespace-body \terminal{\}}
```

``` bnf
enclosing-namespace-specifier:
        identifier
        enclosing-namespace-specifier '::' inlineₒₚₜ identifier
```

``` bnf
namespace-body:
        declaration-seqₒₚₜ
```

Every *namespace-definition* shall appear at namespace scope
[[basic.scope.namespace]].

In a *named-namespace-definition*, the *identifier* is the name of the
namespace. If the *identifier*, when looked up [[basic.lookup.unqual]],
refers to a *namespace-name* (but not a *namespace-alias*) that was
introduced in the namespace in which the *named-namespace-definition*
appears or that was introduced in a member of the inline namespace set
of that namespace, the *namespace-definition* *extends* the
previously-declared namespace. Otherwise, the *identifier* is introduced
as a *namespace-name* into the declarative region in which the
*named-namespace-definition* appears.

Because a *namespace-definition* contains *declaration*s in its
*namespace-body* and a *namespace-definition* is itself a *declaration*,
it follows that *namespace-definition*s can be nested.

[*Example 1*:

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

— *end example*]

The *enclosing namespaces* of a declaration are those namespaces in
which the declaration lexically appears, except for a redeclaration of a
namespace member outside its original namespace (e.g., a definition as
specified in  [[namespace.memdef]]). Such a redeclaration has the same
enclosing namespaces as the original declaration.

[*Example 2*:

``` cpp
namespace Q {
  namespace V {
    void f();                   // enclosing namespaces are the global namespace, Q, and Q::V
    class C { void m(); };
  }
  void V::f() {                 // enclosing namespaces are the global namespace, Q, and Q::V
    extern void h();            // ... so this declares Q::V::h
  }
  void V::C::m() {              // enclosing namespaces are the global namespace, Q, and Q::V
  }
}
```

— *end example*]

If the optional initial `inline` keyword appears in a
*namespace-definition* for a particular namespace, that namespace is
declared to be an *inline namespace*. The `inline` keyword may be used
on a *namespace-definition* that extends a namespace only if it was
previously used on the *namespace-definition* that initially declared
the *namespace-name* for that namespace.

The optional *attribute-specifier-seq* in a *named-namespace-definition*
appertains to the namespace being defined or extended.

Members of an inline namespace can be used in most respects as though
they were members of the enclosing namespace. Specifically, the inline
namespace and its enclosing namespace are both added to the set of
associated namespaces used in argument-dependent lookup
[[basic.lookup.argdep]] whenever one of them is, and a *using-directive*
[[namespace.udir]] that names the inline namespace is implicitly
inserted into the enclosing namespace as for an unnamed namespace
[[namespace.unnamed]]. Furthermore, each member of the inline namespace
can subsequently be partially specialized [[temp.class.spec]],
explicitly instantiated [[temp.explicit]], or explicitly specialized
[[temp.expl.spec]] as though it were a member of the enclosing
namespace. Finally, looking up a name in the enclosing namespace via
explicit qualification [[namespace.qual]] will include members of the
inline namespace brought in by the *using-directive* even if there are
declarations of that name in the enclosing namespace.

These properties are transitive: if a namespace `N` contains an inline
namespace `M`, which in turn contains an inline namespace `O`, then the
members of `O` can be used as though they were members of `M` or `N`.
The *inline namespace set* of `N` is the transitive closure of all
inline namespaces in `N`. The *enclosing namespace set* of `O` is the
set of namespaces consisting of the innermost non-inline namespace
enclosing an inline namespace `O`, together with any intervening inline
namespaces.

A *nested-namespace-definition* with an *enclosing-namespace-specifier*
`E`, *identifier* `I` and *namespace-body* `B` is equivalent to

``` cpp
namespace E { inlineₒₚₜ namespace I { B } }
```

where the optional `inline` is present if and only if the *identifier*
`I` is preceded by `inline`.

[*Example 3*:

``` cpp
namespace A::inline B::C {
  int i;
}
```

The above has the same effect as:

``` cpp
namespace A {
  inline namespace B {
    namespace C {
      int i;
    }
  }
}
```

— *end example*]

#### Unnamed namespaces <a id="namespace.unnamed">[[namespace.unnamed]]</a>

An *unnamed-namespace-definition* behaves as if it were replaced by

``` bnf
inlineₒₚₜ namespace \textit{unique} \terminal{\ \terminal{/* empty body */} \terminal{\}}
using namespace \textit{unique} \terminal{;}
namespace \textit{unique} \terminal{\ namespace-body \terminal{\}}
```

where `inline` appears if and only if it appears in the
*unnamed-namespace-definition* and all occurrences of *unique* in a
translation unit are replaced by the same identifier, and this
identifier differs from all other identifiers in the translation unit.
The optional *attribute-specifier-seq* in the
*unnamed-namespace-definition* appertains to *unique*.

[*Example 1*:

``` cpp
namespace { int i; }            // unique::i
void f() { i++; }               // unique::i++

namespace A {
  namespace {
    int i;                      // A::unique::i
    int j;                      // A::unique::j
  }
  void g() { i++; }             // A::unique::i++
}

using namespace A;
void h() {
  i++;                          // error: unique::i or A::unique::i
  A::i++;                       // A::unique::i
  j++;                          // A::unique::j
}
```

— *end example*]

#### Namespace member definitions <a id="namespace.memdef">[[namespace.memdef]]</a>

A declaration in a namespace `N` (excluding declarations in nested
scopes) whose *declarator-id* is an *unqualified-id* [[dcl.meaning]],
whose *class-head-name* [[class.pre]] or *enum-head-name* [[dcl.enum]]
is an *identifier*, or whose *elaborated-type-specifier* is of the form
*class-key* *attribute-specifier-seq*ₒₚₜ *identifier* [[dcl.type.elab]],
or that is an *opaque-enum-declaration*, declares (or redeclares) its
*unqualified-id* or *identifier* as a member of `N`.

[*Note 1*: An explicit instantiation [[temp.explicit]] or explicit
specialization [[temp.expl.spec]] of a template does not introduce a
name and thus may be declared using an *unqualified-id* in a member of
the enclosing namespace set, if the primary template is declared in an
inline namespace. — *end note*]

[*Example 1*:

``` cpp
namespace X {
  void f() { ... }        // OK: introduces X::f()

  namespace M {
    void g();                   // OK: introduces X::M::g()
  }
  using M::g;
  void g();                     // error: conflicts with X::M::g()
}
```

— *end example*]

Members of a named namespace can also be defined outside that namespace
by explicit qualification [[namespace.qual]] of the name being defined,
provided that the entity being defined was already declared in the
namespace and the definition appears after the point of declaration in a
namespace that encloses the declaration’s namespace.

[*Example 2*:

``` cpp
namespace Q {
  namespace V {
    void f();
  }
  void V::f() { ... }     // OK
  void V::g() { ... }     // error: g() is not yet a member of V
  namespace V {
    void g();
  }
}

namespace R {
  void Q::V::g() { ... }  // error: R doesn't enclose Q
}
```

— *end example*]

If a friend declaration in a non-local class first declares a class,
function, class template or function template[^10] the friend is a
member of the innermost enclosing namespace. The friend declaration does
not by itself make the name visible to unqualified lookup
[[basic.lookup.unqual]] or qualified lookup [[basic.lookup.qual]].

[*Note 2*: The name of the friend will be visible in its namespace if a
matching declaration is provided at namespace scope (either before or
after the class definition granting friendship). — *end note*]

If a friend function or function template is called, its name may be
found by the name lookup that considers functions from namespaces and
classes associated with the types of the function arguments
[[basic.lookup.argdep]]. If the name in a friend declaration is neither
qualified nor a *template-id* and the declaration is a function or an
*elaborated-type-specifier*, the lookup to determine whether the entity
has been previously declared shall not consider any scopes outside the
innermost enclosing namespace.

[*Note 3*: The other forms of friend declarations cannot declare a new
member of the innermost enclosing namespace and thus follow the usual
lookup rules. — *end note*]

[*Example 3*:

``` cpp
// Assume f and g have not yet been declared.
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
  void f(X) { ... }       // definition of A::f
  void h(int) { ... }     // definition of A::h
  // A::f, A::g and A::h are visible here and known to be friends
}

using A::x;

void h() {
  A::f(x);
  A::X::f(x);                   // error: f is not a member of A::X
  A::X::Y::g();                 // error: g is not a member of A::X::Y
}
```

— *end example*]

### Namespace alias <a id="namespace.alias">[[namespace.alias]]</a>

A *namespace-alias-definition* declares an alternate name for a
namespace according to the following grammar:

``` bnf
namespace-alias:
        identifier
```

``` bnf
namespace-alias-definition:
        namespace identifier '=' qualified-namespace-specifier ';'
```

``` bnf
qualified-namespace-specifier:
    nested-name-specifierₒₚₜ namespace-name
```

The *identifier* in a *namespace-alias-definition* is a synonym for the
name of the namespace denoted by the *qualified-namespace-specifier* and
becomes a *namespace-alias*.

[*Note 1*: When looking up a *namespace-name* in a
*namespace-alias-definition*, only namespace names are considered, see 
[[basic.lookup.udir]]. — *end note*]

In a declarative region, a *namespace-alias-definition* can be used to
redefine a *namespace-alias* declared in that declarative region to
refer only to the namespace to which it already refers.

[*Example 1*:

The following declarations are well-formed:

``` cpp
namespace Company_with_very_long_name { ... }
namespace CWVLN = Company_with_very_long_name;
namespace CWVLN = Company_with_very_long_name;  // OK: duplicate
namespace CWVLN = CWVLN;
```

— *end example*]

### Using namespace directive <a id="namespace.udir">[[namespace.udir]]</a>

``` bnf
using-directive:
    attribute-specifier-seqₒₚₜ using namespace nested-name-specifierₒₚₜ namespace-name ';'
```

A *using-directive* shall not appear in class scope, but may appear in
namespace scope or in block scope.

[*Note 1*: When looking up a *namespace-name* in a *using-directive*,
only namespace names are considered, see 
[[basic.lookup.udir]]. — *end note*]

The optional *attribute-specifier-seq* appertains to the
*using-directive*.

A *using-directive* specifies that the names in the nominated namespace
can be used in the scope in which the *using-directive* appears after
the *using-directive*. During unqualified name lookup
[[basic.lookup.unqual]], the names appear as if they were declared in
the nearest enclosing namespace which contains both the
*using-directive* and the nominated namespace.

[*Note 2*: In this context, “contains” means “contains directly or
indirectly”. — *end note*]

A *using-directive* does not add any members to the declarative region
in which it appears.

[*Example 1*:

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
  i = 5;            // error: neither i is visible
}
```

— *end example*]

For unqualified lookup [[basic.lookup.unqual]], the *using-directive* is
transitive: if a scope contains a *using-directive* that nominates a
second namespace that itself contains *using-directive*s, the effect is
as if the *using-directive*s from the second namespace also appeared in
the first.

[*Note 3*: For qualified lookup, see 
[[namespace.qual]]. — *end note*]

[*Example 2*:

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

— *end example*]

If a namespace is extended [[namespace.def]] after a *using-directive*
for that namespace is given, the additional members of the extended
namespace and the members of namespaces nominated by *using-directive*s
in the extending *namespace-definition* can be used after the extending
*namespace-definition*.

[*Note 4*:

If name lookup finds a declaration for a name in two different
namespaces, and the declarations do not declare the same entity and do
not declare functions or function templates, the use of the name is
ill-formed [[basic.lookup]]. In particular, the name of a variable,
function or enumerator does not hide the name of a class or enumeration
declared in a different namespace. For example,

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
  g();              // OK: name g refers to the same entity
  h();              // OK: overload resolution selects A::h
}
```

— *end note*]

During overload resolution, all functions from the transitive search are
considered for argument matching. The set of declarations found by the
transitive search is unordered.

[*Note 5*: In particular, the order in which namespaces were considered
and the relationships among the namespaces implied by the
*using-directive*s do not cause preference to be given to any of the
declarations found by the search. — *end note*]

An ambiguity exists if the best match finds two functions with the same
signature, even if one is in a namespace reachable through
*using-directive*s in the namespace of the other.[^11]

[*Example 3*:

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

— *end example*]

## The `using` declaration <a id="namespace.udecl">[[namespace.udecl]]</a>

``` bnf
using-declaration:
    using using-declarator-list ';'
```

``` bnf
using-declarator-list:
    using-declarator '...'ₒₚₜ
    using-declarator-list ',' using-declarator '...'ₒₚₜ
```

``` bnf
using-declarator:
    typenameₒₚₜ nested-name-specifier unqualified-id
```

Each *using-declarator* in a *using-declaration* [^12] introduces a set
of declarations into the declarative region in which the
*using-declaration* appears. The set of declarations introduced by the
*using-declarator* is found by performing qualified name lookup (
[[basic.lookup.qual]], [[class.member.lookup]]) for the name in the
*using-declarator*, excluding functions that are hidden as described
below. If the *using-declarator* does not name a constructor, the
*unqualified-id* is declared in the declarative region in which the
*using-declaration* appears as a synonym for each declaration introduced
by the *using-declarator*.

[*Note 1*: Only the specified name is so declared; specifying an
enumeration name in a *using-declaration* does not declare its
enumerators in the *using-declaration*'s declarative
region. — *end note*]

If the *using-declarator* names a constructor, it declares that the
class *inherits* the set of constructor declarations introduced by the
*using-declarator* from the nominated base class.

Every *using-declaration* is a *declaration* and a *member-declaration*
and can therefore be used in a class definition.

[*Example 1*:

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

— *end example*]

In a *using-declaration* used as a *member-declaration*, each
*using-declarator* shall either name an enumerator or have a
*nested-name-specifier* naming a base class of the class being defined.

[*Example 2*:

``` cpp
enum class button { up, down };
struct S {
  using button::up;
  button b = up;                // OK
};
```

— *end example*]

If a *using-declarator* names a constructor, its *nested-name-specifier*
shall name a direct base class of the class being defined.

[*Example 3*:

``` cpp
template <typename... bases>
struct X : bases... {
  using bases::g...;
};

X<B, D> x;                      // OK: B::g and D::g introduced
```

— *end example*]

[*Example 4*:

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

— *end example*]

[*Note 2*: Since destructors do not have names, a *using-declaration*
cannot refer to a destructor for a base class. Since specializations of
member templates for conversion functions are not found by name lookup,
they are not considered when a *using-declaration* specifies a
conversion function [[temp.mem]]. — *end note*]

If a constructor or assignment operator brought from a base class into a
derived class has the signature of a copy/move constructor or assignment
operator for the derived class ([[class.copy.ctor]],
[[class.copy.assign]]), the *using-declaration* does not by itself
suppress the implicit declaration of the derived class member; the
member from the base class is hidden or overridden by the
implicitly-declared copy/move constructor or assignment operator of the
derived class, as described below.

A *using-declaration* shall not name a *template-id*.

[*Example 5*:

``` cpp
struct A {
  template <class T> void f(T);
  template <class T> struct X { };
};
struct B : A {
  using A::f<double>;           // error
  using A::X<int>;              // error
};
```

— *end example*]

A *using-declaration* shall not name a namespace.

A *using-declaration* that names a class member other than an enumerator
shall be a *member-declaration*.

[*Example 6*:

``` cpp
struct X {
  int i;
  static int s;
};

void f() {
  using X::i;                   // error: X::i is a class member and this is not a member declaration.
  using X::s;                   // error: X::s is a class member and this is not a member declaration.
}
```

— *end example*]

Members declared by a *using-declaration* can be referred to by explicit
qualification just like other member names [[namespace.qual]].

[*Example 7*:

``` cpp
void f();

namespace A {
  void g();
}

namespace X {
  using ::f;                    // global f
  using A::g;                   // A's g
}

void h()
{
  X::f();                       // calls ::f
  X::g();                       // calls A::g
}
```

— *end example*]

A *using-declaration* is a *declaration* and can therefore be used
repeatedly where (and only where) multiple declarations are allowed.

[*Example 8*:

``` cpp
namespace A {
  int i;
}

namespace A1 {
  using A::i, A::i;             // OK: double declaration
}

struct B {
  int i;
};

struct X : B {
  using B::i, B::i;             // error: double member declaration
};
```

— *end example*]

[*Note 3*: For a *using-declaration* whose *nested-name-specifier*
names a namespace, members added to the namespace after the
*using-declaration* are not in the set of introduced declarations, so
they are not considered when a use of the name is made. Thus, additional
overloads added after the *using-declaration* are ignored, but default
function arguments [[dcl.fct.default]], default template arguments
[[temp.param]], and template specializations ([[temp.class.spec]],
[[temp.expl.spec]]) are considered. — *end note*]

[*Example 9*:

``` cpp
namespace A {
  void f(int);
}

using A::f;         // f is a synonym for A::f; that is, for A::f(int).
namespace A {
  void f(char);
}

void foo() {
  f('a');           // calls f(int), even though f(char) exists.
}

void bar() {
  using A::f;       // f is a synonym for A::f; that is, for A::f(int) and A::f(char).
  f('a');           // calls f(char)
}
```

— *end example*]

[*Note 4*: Partial specializations of class templates are found by
looking up the primary class template and then considering all partial
specializations of that template. If a *using-declaration* names a class
template, partial specializations introduced after the
*using-declaration* are effectively visible because the primary template
is visible [[temp.class.spec]]. — *end note*]

Since a *using-declaration* is a declaration, the restrictions on
declarations of the same name in the same declarative region
[[basic.scope]] also apply to *using-declaration*s.

[*Example 10*:

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

— *end example*]

If a function declaration in namespace scope or block scope has the same
name and the same parameter-type-list [[dcl.fct]] as a function
introduced by a *using-declaration*, and the declarations do not declare
the same function, the program is ill-formed. If a function template
declaration in namespace scope has the same name, parameter-type-list,
trailing *requires-clause* (if any), return type, and *template-head*,
as a function template introduced by a *using-declaration*, the program
is ill-formed.

[*Note 5*:

Two *using-declaration*s may introduce functions with the same name and
the same parameter-type-list. If, for a call to an unqualified function
name, function overload resolution selects the functions introduced by
such *using-declaration*s, the function call is ill-formed.

[*Example 11*:

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

— *end example*]

— *end note*]

When a *using-declarator* brings declarations from a base class into a
derived class, member functions and member function templates in the
derived class override and/or hide member functions and member function
templates with the same name, parameter-type-list [[dcl.fct]], trailing
*requires-clause* (if any), cv-qualification, and *ref-qualifier* (if
any), in a base class (rather than conflicting). Such hidden or
overridden declarations are excluded from the set of declarations
introduced by the *using-declarator*.

[*Example 12*:

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

struct B1 {
  B1(int);
};

struct B2 {
  B2(int);
};

struct D1 : B1, B2 {
  using B1::B1;
  using B2::B2;
};
D1 d1(0);           // error: ambiguous

struct D2 : B1, B2 {
  using B1::B1;
  using B2::B2;
  D2(int);          // OK: D2::D2(int) hides B1::B1(int) and B2::B2(int)
};
D2 d2(0);           // calls D2::D2(int)
```

— *end example*]

[*Note 6*: For the purpose of forming a set of candidates during
overload resolution, the functions that are introduced by a
*using-declaration* into a derived class are treated as though they were
members of the derived class [[class.member.lookup]]. In particular, the
implicit object parameter is treated as if it were a reference to the
derived class rather than to the base class [[over.match.funcs]]. This
has no effect on the type of the function, and in all other respects the
function remains a member of the base class. — *end note*]

Constructors that are introduced by a *using-declaration* are treated as
though they were constructors of the derived class when looking up the
constructors of the derived class [[class.qual]] or forming a set of
overload candidates ([[over.match.ctor]], [[over.match.copy]],
[[over.match.list]]).

[*Note 7*: If such a constructor is selected to perform the
initialization of an object of class type, all subobjects other than the
base class from which the constructor originated are implicitly
initialized [[class.inhctor.init]]. A constructor of a derived class is
sometimes preferred to a constructor of a base class if they would
otherwise be ambiguous [[over.match.best]]. — *end note*]

In a *using-declarator* that does not name a constructor, all members of
the set of introduced declarations shall be accessible. In a
*using-declarator* that names a constructor, no access check is
performed. In particular, if a derived class uses a *using-declarator*
to access a member of a base class, the member name shall be accessible.
If the name is that of an overloaded member function, then all functions
named shall be accessible. The base class members mentioned by a
*using-declarator* shall be visible in the scope of at least one of the
direct base classes of the class where the *using-declarator* is
specified.

[*Note 8*:

Because a *using-declarator* designates a base class member (and not a
member subobject or a member function of a base class subobject), a
*using-declarator* cannot be used to resolve inherited member
ambiguities.

[*Example 13*:

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
  return d->x();    // error: overload resolution selects A::x, but A is an ambiguous base class
}
```

— *end example*]

— *end note*]

A synonym created by a *using-declaration* has the usual accessibility
for a *member-declaration*. A *using-declarator* that names a
constructor does not create a synonym; instead, the additional
constructors are accessible if they would be accessible when used to
construct an object of the corresponding base class, and the
accessibility of the *using-declaration* is ignored.

[*Example 14*:

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

— *end example*]

If a *using-declarator* uses the keyword `typename` and specifies a
dependent name [[temp.dep]], the name introduced by the
*using-declaration* is treated as a *typedef-name* [[dcl.typedef]].

## The `asm` declaration <a id="dcl.asm">[[dcl.asm]]</a>

An `asm` declaration has the form

``` bnf
asm-declaration:
    attribute-specifier-seqₒₚₜ asm '(' string-literal ')' ';'
```

The `asm` declaration is conditionally-supported; its meaning is
*implementation-defined*. The optional *attribute-specifier-seq* in an
*asm-declaration* appertains to the `asm` declaration.

[*Note 1*: Typically it is used to pass information through the
implementation to an assembler. — *end note*]

## Linkage specifications <a id="dcl.link">[[dcl.link]]</a>

All function types, function names with external linkage, and variable
names with external linkage have a *language linkage*.

[*Note 1*: Some of the properties associated with an entity with
language linkage are specific to each implementation and are not
described here. For example, a particular language linkage may be
associated with a particular form of representing names of objects and
functions with external linkage, or with a particular calling
convention, etc. — *end note*]

The default language linkage of all function types, function names, and
variable names is C++ language linkage. Two function types with
different language linkages are distinct types even if they are
otherwise identical.

Linkage [[basic.link]] between C++ and non-C++ code fragments can be
achieved using a *linkage-specification*:

``` bnf
linkage-specification:
    extern string-literal \terminal{\ declaration-seqₒₚₜ \terminal{\}}
    extern string-literal declaration
```

The *string-literal* indicates the required language linkage. This
document specifies the semantics for the *string-literal*s `"C"` and
`"C++"`. Use of a *string-literal* other than `"C"` or `"C++"` is
conditionally-supported, with *implementation-defined* semantics.

[*Note 2*: Therefore, a linkage-specification with a *string-literal*
that is unknown to the implementation requires a
diagnostic. — *end note*]

[*Note 3*: It is recommended that the spelling of the *string-literal*
be taken from the document defining that language. For example, `Ada`
(not `ADA`) and `Fortran` or `FORTRAN`, depending on the
vintage. — *end note*]

Every implementation shall provide for linkage to functions written in
the C programming language, `"C"`, and linkage to C++ functions,
`"C++"`.

[*Example 1*:

``` cpp
complex sqrt(complex);          // C++{} linkage by default
extern "C" {
  double sqrt(double);          // C linkage
}
```

— *end example*]

A *module-import-declaration* shall not be directly contained in a
*linkage-specification*. A *module-import-declaration* appearing in a
linkage specification with other than C++ language linkage is
conditionally-supported with *implementation-defined* semantics.

Linkage specifications nest. When linkage specifications nest, the
innermost one determines the language linkage. A linkage specification
does not establish a scope. A *linkage-specification* shall occur only
in namespace scope [[basic.scope]]. In a *linkage-specification*, the
specified language linkage applies to the function types of all function
declarators, function names with external linkage, and variable names
with external linkage declared within the *linkage-specification*.

[*Example 2*:

``` cpp
extern "C"                      // the name f1 and its function type have C language linkage;
  void f1(void(*pf)(int));      // pf is a pointer to a C function

extern "C" typedef void FUNC();
FUNC f2;                        // the name f2 has C++{} language linkage and the
                                // function's type has C language linkage

extern "C" FUNC f3;             // the name of function f3 and the function's type have C language linkage

void (*pf2)(FUNC*);             // the name of the variable pf2 has C++{} linkage and the type
                                // of pf2 is ``pointer to C++{} function that takes one parameter of type
                                // pointer to C function''
extern "C" {
  static void f4();             // the name of the function f4 has internal linkage (not C language linkage)
                                // and the function's type has C language linkage.
}

extern "C" void f5() {
  extern void f4();             // OK: Name linkage (internal) and function type linkage (C language linkage)
                                // obtained from previous declaration.
}

extern void f4();               // OK: Name linkage (internal) and function type linkage (C language linkage)
                                // obtained from previous declaration.

void f6() {
  extern void f4();             // OK: Name linkage (internal) and function type linkage (C language linkage)
                                // obtained from previous declaration.
}
```

— *end example*]

A C language linkage is ignored in determining the language linkage of
the names of class members and the function type of class member
functions.

[*Example 3*:

``` cpp
extern "C" typedef void FUNC_c();

class C {
  void mf1(FUNC_c*);            // the name of the function mf1 and the member function's type have
                                // C++{} language linkage; the parameter has type ``pointer to C function''

  FUNC_c mf2;                   // the name of the function mf2 and the member function's type have
                                // C++{} language linkage

  static FUNC_c* q;             // the name of the data member q has C++{} language linkage and
                                // the data member's type is ``pointer to C function''
};

extern "C" {
  class X {
    void mf();                  // the name of the function mf and the member function's type have
                                // C++{} language linkage
    void mf2(void(*)());        // the name of the function mf2 has C++{} language linkage;
                                // the parameter has type ``pointer to C function''
  };
}
```

— *end example*]

If two declarations declare functions with the same name and
parameter-type-list [[dcl.fct]] to be members of the same namespace or
declare objects with the same name to be members of the same namespace
and the declarations give the names different language linkages, the
program is ill-formed; no diagnostic is required if the declarations
appear in different translation units. Except for functions with C++
linkage, a function declaration without a linkage specification shall
not precede the first linkage specification for that function. A
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
linkage shall not be declared with the same name as a variable in global
scope, unless both declarations denote the same entity; no diagnostic is
required if the declarations appear in different translation units. A
variable with C language linkage shall not be declared with the same
name as a function with C language linkage (ignoring the namespace names
that qualify the respective names); no diagnostic is required if the
declarations appear in different translation units.

[*Note 4*: Only one definition for an entity with a given name with C
language linkage may appear in the program (see  [[basic.def.odr]]);
this implies that such an entity must not be defined in more than one
namespace scope. — *end note*]

[*Example 4*:

``` cpp
int x;
namespace A {
  extern "C" int f();
  extern "C" int g() { return 1; }
  extern "C" int h();
  extern "C" int x();               // error: same name as global-space object x
}

namespace B {
  extern "C" int f();               // A::f and B::f refer to the same function
  extern "C" int g() { return 1; }  // error: the function g with C language linkage has two definitions
}

int A::f() { return 98; }           // definition for the function f with C language linkage
extern "C" int h() { return 97; }   // definition for the function h with C language linkage
                                    // A::h and ::h refer to the same function
```

— *end example*]

A declaration directly contained in a *linkage-specification* is treated
as if it contains the `extern` specifier [[dcl.stc]] for the purpose of
determining the linkage of the declared name and whether it is a
definition. Such a declaration shall not specify a storage class.

[*Example 5*:

``` cpp
extern "C" double f();
static double f();                  // error
extern "C" int i;                   // declaration
extern "C" {
  int i;                            // definition
}
extern "C" static void g();         // error
```

— *end example*]

[*Note 5*: Because the language linkage is part of a function type,
when indirecting through a pointer to C function, the function to which
the resulting lvalue refers is considered a C function. — *end note*]

Linkage from C++ to objects defined in other languages and to objects
defined in C++ from other languages is *implementation-defined* and
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
  '[' '[' attribute-using-prefixₒₚₜ attribute-list ']' ']'
  alignment-specifier
```

``` bnf
alignment-specifier:
  alignas '(' type-id '...'ₒₚₜ ')'
  alignas '(' constant-expression '...'ₒₚₜ ')'
```

``` bnf
attribute-using-prefix:
  using attribute-namespace ':'
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
    '(' balanced-token-seqₒₚₜ ')'
```

``` bnf
balanced-token-seq:
    balanced-token
    balanced-token-seq balanced-token
```

``` bnf
balanced-token:
    '(' balanced-token-seqₒₚₜ ')'
    '[' balanced-token-seqₒₚₜ ']'
    \terminal{\ balanced-token-seqₒₚₜ \terminal{\}}
    any *token* other than a parenthesis, a bracket, or a brace
```

If an *attribute-specifier* contains an *attribute-using-prefix*, the
*attribute-list* following that *attribute-using-prefix* shall not
contain an *attribute-scoped-token* and every *attribute-token* in that
*attribute-list* is treated as if its *identifier* were prefixed with
`N::`, where `N` is the *attribute-namespace* specified in the
*attribute-using-prefix*.

[*Note 1*: This rule imposes no constraints on how an
*attribute-using-prefix* affects the tokens in an
*attribute-argument-clause*. — *end note*]

[*Example 1*:

``` cpp
[[using CC: opt(1), debug]]         // same as [[CC::opt(1), CC::debug]]
  void f() {}
[[using CC: opt(1)]] [[CC::debug]]  // same as [[CC::opt(1)]] [[CC::debug]]
  void g() {}
[[using CC: CC::opt(1)]]            // error: cannot combine using and scoped attribute token
  void h() {}
```

— *end example*]

[*Note 2*: For each individual attribute, the form of the
*balanced-token-seq* will be specified. — *end note*]

In an *attribute-list*, an ellipsis may appear only if that
*attribute*’s specification permits it. An *attribute* followed by an
ellipsis is a pack expansion [[temp.variadic]]. An *attribute-specifier*
that contains no *attribute*s has no effect. The order in which the
*attribute-token*s appear in an *attribute-list* is not significant. If
a keyword [[lex.key]] or an alternative token [[lex.digraph]] that
satisfies the syntactic requirements of an *identifier* [[lex.name]] is
contained in an *attribute-token*, it is considered an identifier. No
name lookup [[basic.lookup]] is performed on any of the identifiers
contained in an *attribute-token*. The *attribute-token* determines
additional requirements on the *attribute-argument-clause* (if any).

Each *attribute-specifier-seq* is said to *appertain* to some entity or
statement, identified by the syntactic context where it appears (
[[stmt.stmt]], [[dcl.dcl]], [[dcl.decl]]). If an
*attribute-specifier-seq* that appertains to some entity or statement
contains an *attribute* or *alignment-specifier* that is not allowed to
apply to that entity or statement, the program is ill-formed. If an
*attribute-specifier-seq* appertains to a friend declaration
[[class.friend]], that declaration shall be a definition.

[*Note 3*: An *attribute-specifier-seq* cannot appeartain to an
explicit instantiation [[temp.explicit]]. — *end note*]

For an *attribute-token* (including an *attribute-scoped-token*) not
specified in this document, the behavior is *implementation-defined*.
Any *attribute-token* that is not recognized by the implementation is
ignored. An *attribute-token* is reserved for future standardization if

- it is not an *attribute-scoped-token* and is not specified in this
  document, or
- it is an *attribute-scoped-token* and its *attribute-namespace* is
  `std` followed by zero or more digits.

[*Note 4*: Each implementation should choose a distinctive name for the
*attribute-namespace* in an *attribute-scoped-token*. — *end note*]

Two consecutive left square bracket tokens shall appear only when
introducing an *attribute-specifier* or within the *balanced-token-seq*
of an *attribute-argument-clause*.

[*Note 5*: If two consecutive left square brackets appear where an
*attribute-specifier* is not allowed, the program is ill-formed even if
the brackets match an alternative grammar production. — *end note*]

[*Example 2*:

``` cpp
int p[10];
void f() {
  int x = 42, y[5];
  int(p[[x] { return x; }()]);  // error: invalid attribute on a nested declarator-id and
                                // not a function-style cast of an element of p.
  y[[] { return 2; }()] = 2;    // error even though attributes are not allowed in this context.
  int i [[vendor::attr([[]])]]; // well-formed implementation-defined attribute.
}
```

— *end example*]

### Alignment specifier <a id="dcl.align">[[dcl.align]]</a>

An *alignment-specifier* may be applied to a variable or to a class data
member, but it shall not be applied to a bit-field, a function
parameter, or an *exception-declaration* [[except.handle]]. An
*alignment-specifier* may also be applied to the declaration of a class
(in an *elaborated-type-specifier* [[dcl.type.elab]] or *class-head*
[[class]], respectively). An *alignment-specifier* with an ellipsis is a
pack expansion [[temp.variadic]].

When the *alignment-specifier* is of the form `alignas(`
*constant-expression* `)`:

- the *constant-expression* shall be an integral constant expression
- if the constant expression does not evaluate to an alignment value
  [[basic.align]], or evaluates to an extended alignment and the
  implementation does not support that alignment in the context of the
  declaration, the program is ill-formed.

An *alignment-specifier* of the form `alignas(` *type-id* `)` has the
same effect as `alignas({}alignof(` *type-id* `))` [[expr.alignof]].

The alignment requirement of an entity is the strictest nonzero
alignment specified by its *alignment-specifier*s, if any; otherwise,
the *alignment-specifier*s have no effect.

The combined effect of all *alignment-specifier*s in a declaration shall
not specify an alignment that is less strict than the alignment that
would be required for the entity being declared if all
*alignment-specifier*s appertaining to that entity were omitted.

[*Example 1*:

``` cpp
struct alignas(8) S {};
struct alignas(1) U {
  S s;
};  // error: U specifies an alignment that is less strict than if the alignas(1) were omitted.
```

— *end example*]

If the defining declaration of an entity has an *alignment-specifier*,
any non-defining declaration of that entity shall either specify
equivalent alignment or have no *alignment-specifier*. Conversely, if
any declaration of an entity has an *alignment-specifier*, every
defining declaration of that entity shall specify an equivalent
alignment. No diagnostic is required if declarations of an entity have
different *alignment-specifier*s in different translation units.

[*Example 2*:

``` cpp
// Translation unit #1:
struct S { int x; } s, *p = &s;

// Translation unit #2:
struct alignas(16) S;           // ill-formed, no diagnostic required: definition of S lacks alignment
extern S* p;
```

— *end example*]

[*Example 3*:

An aligned buffer with an alignment requirement of `A` and holding `N`
elements of type `T` can be declared as:

``` cpp
alignas(T) alignas(A) T buffer[N];
```

Specifying `alignas(T)` ensures that the final requested alignment will
not be weaker than `alignof(T)`, and therefore the program will not be
ill-formed.

— *end example*]

[*Example 4*:

``` cpp
alignas(double) void f();                           // error: alignment applied to function
alignas(double) unsigned char c[sizeof(double)];    // array of characters, suitably aligned for a double
extern unsigned char c[sizeof(double)];             // no alignas necessary
alignas(float)
  extern unsigned char c[sizeof(double)];           // error: different alignment in declaration
```

— *end example*]

### Carries dependency attribute <a id="dcl.attr.depend">[[dcl.attr.depend]]</a>

The *attribute-token* `carries_dependency` specifies dependency
propagation into and out of functions. It shall appear at most once in
each *attribute-list* and no *attribute-argument-clause* shall be
present. The attribute may be applied to the *declarator-id* of a
*parameter-declaration* in a function declaration or lambda, in which
case it specifies that the initialization of the parameter carries a
dependency to [[intro.multithread]] each lvalue-to-rvalue conversion
[[conv.lval]] of that object. The attribute may also be applied to the
*declarator-id* of a function declaration, in which case it specifies
that the return value, if any, carries a dependency to the evaluation of
the function call expression.

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
ill-formed, no diagnostic required.

[*Note 1*: The `carries_dependency` attribute does not change the
meaning of the program, but may result in generation of more efficient
code. — *end note*]

[*Example 1*:

``` cpp
/* Translation unit A. */

struct foo { int* a; int* b; };
std::atomic<struct foo *> foo_head[10];
int foo_array[10][10];

[[carries_dependency]] struct foo* f(int i) {
  return foo_head[i].load(memory_order::consume);
}

int g(int* x, int* y [[carries_dependency]]) {
  return kill_dependency(foo_array[*x][*y]);
}

/* Translation unit B. */

[[carries_dependency]] struct foo* f(int i);
int g(int* x, int* y [[carries_dependency]]);

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
hardware memory ordering instructions (a.k.a. fences). Function `g`’s
second parameter has a `carries_dependency` attribute, but its first
parameter does not. Therefore, function `h`’s first call to `g` carries
a dependency into `g`, but its second call does not. The implementation
might need to insert a fence prior to the second call to `g`.

— *end example*]

### Deprecated attribute <a id="dcl.attr.deprecated">[[dcl.attr.deprecated]]</a>

The *attribute-token* `deprecated` can be used to mark names and
entities whose use is still allowed, but is discouraged for some reason.

[*Note 1*: In particular, `deprecated` is appropriate for names and
entities that are deemed obsolescent or unsafe. — *end note*]

It shall appear at most once in each *attribute-list*. An
*attribute-argument-clause* may be present and, if present, it shall
have the form:

``` bnf
'(' string-literal ')'
```

[*Note 2*: The *string-literal* in the *attribute-argument-clause*
could be used to explain the rationale for deprecation and/or to suggest
a replacing entity. — *end note*]

The attribute may be applied to the declaration of a class, a
*typedef-name*, a variable, a non-static data member, a function, a
namespace, an enumeration, an enumerator, or a template specialization.

A name or entity declared without the `deprecated` attribute can later
be redeclared with the attribute and vice-versa.

[*Note 3*: Thus, an entity initially declared without the attribute can
be marked as deprecated by a subsequent redeclaration. However, after an
entity is marked as deprecated, later redeclarations do not un-deprecate
the entity. — *end note*]

Redeclarations using different forms of the attribute (with or without
the *attribute-argument-clause* or with different
*attribute-argument-clause*s) are allowed.

*Recommended practice:* Implementations should use the `deprecated`
attribute to produce a diagnostic message in case the program refers to
a name or entity other than to declare it, after a declaration that
specifies the attribute. The diagnostic message should include the text
provided within the *attribute-argument-clause* of any `deprecated`
attribute applied to the name or entity.

### Fallthrough attribute <a id="dcl.attr.fallthrough">[[dcl.attr.fallthrough]]</a>

The *attribute-token* `fallthrough` may be applied to a null statement
[[stmt.expr]]; such a statement is a fallthrough statement. The
*attribute-token* `fallthrough` shall appear at most once in each
*attribute-list* and no *attribute-argument-clause* shall be present. A
fallthrough statement may only appear within an enclosing `switch`
statement [[stmt.switch]]. The next statement that would be executed
after a fallthrough statement shall be a labeled statement whose label
is a case label or default label for the same `switch` statement and, if
the fallthrough statement is contained in an iteration statement, the
next statement shall be part of the same execution of the substatement
of the innermost enclosing iteration statement. The program is
ill-formed if there is no such statement.

*Recommended practice:* The use of a fallthrough statement should
suppress a warning that an implementation might otherwise issue for a
case or default label that is reachable from another case or default
label along some path of execution. Implementations should issue a
warning if a fallthrough statement is not dynamically reachable.

[*Example 1*:

``` cpp
void f(int n) {
  void g(), h(), i();
  switch (n) {
  case 1:
  case 2:
    g();
    [[fallthrough]];
  case 3:                       // warning on fallthrough discouraged
    do {
      [[fallthrough]];          // error: next statement is not part of the same substatement execution
    } while (false);
  case 6:
    do {
      [[fallthrough]];          // error: next statement is not part of the same substatement execution
    } while (n--);
  case 7:
    while (false) {
      [[fallthrough]];          // error: next statement is not part of the same substatement execution
    }
  case 5:
    h();
  case 4:                       // implementation may warn on fallthrough
    i();
    [[fallthrough]];            // error
  }
}
```

— *end example*]

### Likelihood attributes <a id="dcl.attr.likelihood">[[dcl.attr.likelihood]]</a>

The *attribute-token*s `likely` and `unlikely` may be applied to labels
or statements. The *attribute-token*s `likely` and `unlikely` shall
appear at most once in each *attribute-list* and no
*attribute-argument-clause* shall be present. The *attribute-token*
`likely` shall not appear in an *attribute-specifier-seq* that contains
the *attribute-token* `unlikely`.

*Recommended practice:* The use of the `likely` attribute is intended to
allow implementations to optimize for the case where paths of execution
including it are arbitrarily more likely than any alternative path of
execution that does not include such an attribute on a statement or
label. The use of the `unlikely` attribute is intended to allow
implementations to optimize for the case where paths of execution
including it are arbitrarily more unlikely than any alternative path of
execution that does not include such an attribute on a statement or
label. A path of execution includes a label if and only if it contains a
jump to that label.

[*Note 1*: Excessive usage of either of these attributes is liable to
result in performance degradation. — *end note*]

[*Example 1*:

``` cpp
void g(int);
int f(int n) {
  if (n > 5) [[unlikely]] {     // n > 5 is considered to be arbitrarily unlikely
    g(0);
    return n * 2 + 1;
  }

  switch (n) {
  case 1:
    g(1);
    [[fallthrough]];

  [[likely]] case 2:            // n == 2 is considered to be arbitrarily more
    g(2);                       // likely than any other value of n
    break;
  }
  return 3;
}
```

— *end example*]

### Maybe unused attribute <a id="dcl.attr.unused">[[dcl.attr.unused]]</a>

The *attribute-token* `maybe_unused` indicates that a name or entity is
possibly intentionally unused. It shall appear at most once in each
*attribute-list* and no *attribute-argument-clause* shall be present.

The attribute may be applied to the declaration of a class, a
*typedef-name*, a variable (including a structured binding declaration),
a non-static data member, a function, an enumeration, or an enumerator.

A name or entity declared without the `maybe_unused` attribute can later
be redeclared with the attribute and vice versa. An entity is considered
marked after the first declaration that marks it.

*Recommended practice:* For an entity marked `maybe_unused`,
implementations should not emit a warning that the entity or its
structured bindings (if any) are used or unused. For a structured
binding declaration not marked `maybe_unused`, implementations should
not emit such a warning unless all of its structured bindings are
unused.

[*Example 1*:

``` cpp
[[maybe_unused]] void f([[maybe_unused]] bool thing1,
                        [[maybe_unused]] bool thing2) {
  [[maybe_unused]] bool b = thing1 && thing2;
  assert(b);
}
```

Implementations should not warn that `b` is unused, whether or not
`NDEBUG` is defined.

— *end example*]

### Nodiscard attribute <a id="dcl.attr.nodiscard">[[dcl.attr.nodiscard]]</a>

The *attribute-token* `nodiscard` may be applied to the *declarator-id*
in a function declaration or to the declaration of a class or
enumeration. It shall appear at most once in each *attribute-list*. An
*attribute-argument-clause* may be present and, if present, shall have
the form:

``` bnf
'(' string-literal ')'
```

A name or entity declared without the `nodiscard` attribute can later be
redeclared with the attribute and vice-versa.

[*Note 1*: Thus, an entity initially declared without the attribute can
be marked as `nodiscard` by a subsequent redeclaration. However, after
an entity is marked as `nodiscard`, later redeclarations do not remove
the `nodiscard` from the entity. — *end note*]

Redeclarations using different forms of the attribute (with or without
the *attribute-argument-clause* or with different
*attribute-argument-clause*s) are allowed.

A *nodiscard type* is a (possibly cv-qualified) class or enumeration
type marked `nodiscard` in a reachable declaration. A *nodiscard call*
is either

- a function call expression [[expr.call]] that calls a function
  declared `nodiscard` in a reachable declaration or whose return type
  is a nodiscard type, or
- an explicit type conversion ([[expr.type.conv]],
  [[expr.static.cast]], [[expr.cast]]) that constructs an object through
  a constructor declared `nodiscard` in a reachable declaration, or that
  initializes an object of a nodiscard type.

*Recommended practice:* Appearance of a nodiscard call as a
potentially-evaluated discarded-value expression [[expr.prop]] is
discouraged unless explicitly cast to `void`. Implementations should
issue a warning in such cases.

[*Note 2*: This is typically because discarding the return value of a
nodiscard call has surprising consequences. — *end note*]

The *string-literal* in a `nodiscard` *attribute-argument-clause* should
be used in the message of the warning as the rationale for why the
result should not be discarded.

[*Example 1*:

``` cpp
struct [[nodiscard]] my_scopeguard { ... };
struct my_unique {
  my_unique() = default;                                // does not acquire resource
  [[nodiscard]] my_unique(int fd) { ... }         // acquires resource
  ~my_unique() noexcept { ... }                   // releases resource, if any
  ...
};
struct [[nodiscard]] error_info { ... };
error_info enable_missile_safety_mode();
void launch_missiles();
void test_missiles() {
  my_scopeguard();              // warning encouraged
  (void)my_scopeguard(),        // warning not encouraged, cast to void
    launch_missiles();          // comma operator, statement continues
  my_unique(42);                // warning encouraged
  my_unique();                  // warning not encouraged
  enable_missile_safety_mode(); // warning encouraged
  launch_missiles();
}
error_info &foo();
void f() { foo(); }             // warning not encouraged: not a nodiscard call, because neither
                                // the (reference) return type nor the function is declared nodiscard
```

— *end example*]

### Noreturn attribute <a id="dcl.attr.noreturn">[[dcl.attr.noreturn]]</a>

The *attribute-token* `noreturn` specifies that a function does not
return. It shall appear at most once in each *attribute-list* and no
*attribute-argument-clause* shall be present. The attribute may be
applied to the *declarator-id* in a function declaration. The first
declaration of a function shall specify the `noreturn` attribute if any
declaration of that function specifies the `noreturn` attribute. If a
function is declared with the `noreturn` attribute in one translation
unit and the same function is declared without the `noreturn` attribute
in another translation unit, the program is ill-formed, no diagnostic
required.

If a function `f` is called where `f` was previously declared with the
`noreturn` attribute and `f` eventually returns, the behavior is
undefined.

[*Note 1*: The function may terminate by throwing an
exception. — *end note*]

*Recommended practice:* Implementations should issue a warning if a
function marked `[[noreturn]]` might return.

[*Example 1*:

``` cpp
[[ noreturn ]] void f() {
  throw "error";                // OK
}

[[ noreturn ]] void q(int i) {  // behavior is undefined if called with an argument <= 0
  if (i > 0)
    throw "positive";
}
```

— *end example*]

### No unique address attribute <a id="dcl.attr.nouniqueaddr">[[dcl.attr.nouniqueaddr]]</a>

The *attribute-token* `no_unique_address` specifies that a non-static
data member is a potentially-overlapping subobject [[intro.object]]. It
shall appear at most once in each *attribute-list* and no
*attribute-argument-clause* shall be present. The attribute may
appertain to a non-static data member other than a bit-field.

[*Note 1*: The non-static data member can share the address of another
non-static data member or that of a base class, and any padding that
would normally be inserted at the end of the object can be reused as
storage for other members. — *end note*]

[*Example 1*:

``` cpp
template<typename Key, typename Value,
         typename Hash, typename Pred, typename Allocator>
class hash_map {
  [[no_unique_address]] Hash hasher;
  [[no_unique_address]] Pred pred;
  [[no_unique_address]] Allocator alloc;
  Bucket *buckets;
  // ...
public:
  // ...
};
```

Here, `hasher`, `pred`, and `alloc` could have the same address as
`buckets` if their respective types are all empty.

— *end example*]

<!-- Link reference definitions -->
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.def]: basic.md#basic.def
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lookup]: basic.md#basic.lookup
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.lookup.classref]: basic.md#basic.lookup.classref
[basic.lookup.elab]: basic.md#basic.lookup.elab
[basic.lookup.qual]: basic.md#basic.lookup.qual
[basic.lookup.udir]: basic.md#basic.lookup.udir
[basic.lookup.unqual]: basic.md#basic.lookup.unqual
[basic.namespace]: #basic.namespace
[basic.scope]: basic.md#basic.scope
[basic.scope.block]: basic.md#basic.scope.block
[basic.scope.declarative]: basic.md#basic.scope.declarative
[basic.scope.namespace]: basic.md#basic.scope.namespace
[basic.scope.param]: basic.md#basic.scope.param
[basic.scope.pdecl]: basic.md#basic.scope.pdecl
[basic.start]: basic.md#basic.start
[basic.start.dynamic]: basic.md#basic.start.dynamic
[basic.start.static]: basic.md#basic.start.static
[basic.stc]: basic.md#basic.stc
[basic.stc.auto]: basic.md#basic.stc.auto
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.static]: basic.md#basic.stc.static
[basic.stc.thread]: basic.md#basic.stc.thread
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[class]: class.md#class
[class.access]: class.md#class.access
[class.base.init]: class.md#class.base.init
[class.bit]: class.md#class.bit
[class.compare.default]: class.md#class.compare.default
[class.conv]: class.md#class.conv
[class.conv.ctor]: class.md#class.conv.ctor
[class.conv.fct]: class.md#class.conv.fct
[class.copy.assign]: class.md#class.copy.assign
[class.copy.ctor]: class.md#class.copy.ctor
[class.copy.elision]: class.md#class.copy.elision
[class.ctor]: class.md#class.ctor
[class.default.ctor]: class.md#class.default.ctor
[class.dtor]: class.md#class.dtor
[class.expl.init]: class.md#class.expl.init
[class.friend]: class.md#class.friend
[class.inhctor.init]: class.md#class.inhctor.init
[class.init]: class.md#class.init
[class.mem]: class.md#class.mem
[class.member.lookup]: class.md#class.member.lookup
[class.mfct]: class.md#class.mfct
[class.mi]: class.md#class.mi
[class.name]: class.md#class.name
[class.pre]: class.md#class.pre
[class.qual]: basic.md#class.qual
[class.static]: class.md#class.static
[class.static.data]: class.md#class.static.data
[class.temporary]: basic.md#class.temporary
[class.union]: class.md#class.union
[class.union.anon]: class.md#class.union.anon
[class.virtual]: class.md#class.virtual
[conv]: expr.md#conv
[conv.array]: expr.md#conv.array
[conv.func]: expr.md#conv.func
[conv.lval]: expr.md#conv.lval
[conv.prom]: expr.md#conv.prom
[conv.ptr]: expr.md#conv.ptr
[conv.qual]: expr.md#conv.qual
[conv.rval]: expr.md#conv.rval
[coroutine.handle]: support.md#coroutine.handle
[coroutine.handle.resumption]: support.md#coroutine.handle.resumption
[dcl.align]: #dcl.align
[dcl.ambig.res]: #dcl.ambig.res
[dcl.array]: #dcl.array
[dcl.asm]: #dcl.asm
[dcl.attr]: #dcl.attr
[dcl.attr.depend]: #dcl.attr.depend
[dcl.attr.deprecated]: #dcl.attr.deprecated
[dcl.attr.fallthrough]: #dcl.attr.fallthrough
[dcl.attr.grammar]: #dcl.attr.grammar
[dcl.attr.likelihood]: #dcl.attr.likelihood
[dcl.attr.nodiscard]: #dcl.attr.nodiscard
[dcl.attr.noreturn]: #dcl.attr.noreturn
[dcl.attr.nouniqueaddr]: #dcl.attr.nouniqueaddr
[dcl.attr.unused]: #dcl.attr.unused
[dcl.constexpr]: #dcl.constexpr
[dcl.constinit]: #dcl.constinit
[dcl.dcl]: #dcl.dcl
[dcl.decl]: #dcl.decl
[dcl.enum]: #dcl.enum
[dcl.fct]: #dcl.fct
[dcl.fct.def]: #dcl.fct.def
[dcl.fct.def.coroutine]: #dcl.fct.def.coroutine
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
[dcl.inline]: #dcl.inline
[dcl.link]: #dcl.link
[dcl.meaning]: #dcl.meaning
[dcl.mptr]: #dcl.mptr
[dcl.name]: #dcl.name
[dcl.pre]: #dcl.pre
[dcl.ptr]: #dcl.ptr
[dcl.ref]: #dcl.ref
[dcl.spec]: #dcl.spec
[dcl.spec.auto]: #dcl.spec.auto
[dcl.stc]: #dcl.stc
[dcl.struct.bind]: #dcl.struct.bind
[dcl.type]: #dcl.type
[dcl.type.auto.deduct]: #dcl.type.auto.deduct
[dcl.type.class.deduct]: #dcl.type.class.deduct
[dcl.type.cv]: #dcl.type.cv
[dcl.type.decltype]: #dcl.type.decltype
[dcl.type.elab]: #dcl.type.elab
[dcl.type.simple]: #dcl.type.simple
[dcl.typedef]: #dcl.typedef
[depr.volatile.type]: future.md#depr.volatile.type
[enum]: #enum
[enum.udecl]: #enum.udecl
[except.ctor]: except.md#except.ctor
[except.handle]: except.md#except.handle
[except.spec]: except.md#except.spec
[except.throw]: except.md#except.throw
[expr.alignof]: expr.md#expr.alignof
[expr.ass]: expr.md#expr.ass
[expr.await]: expr.md#expr.await
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.const]: expr.md#expr.const
[expr.const.cast]: expr.md#expr.const.cast
[expr.mptr.oper]: expr.md#expr.mptr.oper
[expr.new]: expr.md#expr.new
[expr.post.incr]: expr.md#expr.post.incr
[expr.pre.incr]: expr.md#expr.pre.incr
[expr.prim.lambda]: expr.md#expr.prim.lambda
[expr.prim.this]: expr.md#expr.prim.this
[expr.prop]: expr.md#expr.prop
[expr.ref]: expr.md#expr.ref
[expr.static.cast]: expr.md#expr.static.cast
[expr.sub]: expr.md#expr.sub
[expr.type.conv]: expr.md#expr.type.conv
[expr.unary]: expr.md#expr.unary
[expr.unary.op]: expr.md#expr.unary.op
[expr.yield]: expr.md#expr.yield
[intro.compliance]: intro.md#intro.compliance
[intro.execution]: basic.md#intro.execution
[intro.multithread]: basic.md#intro.multithread
[intro.object]: basic.md#intro.object
[lex.charset]: lex.md#lex.charset
[lex.digraph]: lex.md#lex.digraph
[lex.key]: lex.md#lex.key
[lex.name]: lex.md#lex.name
[lex.string]: lex.md#lex.string
[module.interface]: module.md#module.interface
[namespace.alias]: #namespace.alias
[namespace.def]: #namespace.def
[namespace.memdef]: #namespace.memdef
[namespace.qual]: basic.md#namespace.qual
[namespace.udecl]: #namespace.udecl
[namespace.udir]: #namespace.udir
[namespace.unnamed]: #namespace.unnamed
[over]: over.md#over
[over.binary]: over.md#over.binary
[over.match]: over.md#over.match
[over.match.best]: over.md#over.match.best
[over.match.class.deduct]: over.md#over.match.class.deduct
[over.match.conv]: over.md#over.match.conv
[over.match.copy]: over.md#over.match.copy
[over.match.ctor]: over.md#over.match.ctor
[over.match.funcs]: over.md#over.match.funcs
[over.match.list]: over.md#over.match.list
[over.match.ref]: over.md#over.match.ref
[over.match.viable]: over.md#over.match.viable
[over.oper]: over.md#over.oper
[over.sub]: over.md#over.sub
[special]: class.md#special
[stmt.ambig]: stmt.md#stmt.ambig
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.expr]: stmt.md#stmt.expr
[stmt.if]: stmt.md#stmt.if
[stmt.iter]: stmt.md#stmt.iter
[stmt.label]: stmt.md#stmt.label
[stmt.pre]: stmt.md#stmt.pre
[stmt.return]: stmt.md#stmt.return
[stmt.return.coroutine]: stmt.md#stmt.return.coroutine
[stmt.select]: stmt.md#stmt.select
[stmt.stmt]: stmt.md#stmt.stmt
[stmt.switch]: stmt.md#stmt.switch
[support.runtime]: support.md#support.runtime
[temp.arg.type]: temp.md#temp.arg.type
[temp.class.spec]: temp.md#temp.class.spec
[temp.deduct]: temp.md#temp.deduct
[temp.deduct.call]: temp.md#temp.deduct.call
[temp.deduct.guide]: temp.md#temp.deduct.guide
[temp.dep]: temp.md#temp.dep
[temp.expl.spec]: temp.md#temp.expl.spec
[temp.explicit]: temp.md#temp.explicit
[temp.fct]: temp.md#temp.fct
[temp.inst]: temp.md#temp.inst
[temp.local]: temp.md#temp.local
[temp.mem]: temp.md#temp.mem
[temp.names]: temp.md#temp.names
[temp.over.link]: temp.md#temp.over.link
[temp.param]: temp.md#temp.param
[temp.pre]: temp.md#temp.pre
[temp.res]: temp.md#temp.res
[temp.spec]: temp.md#temp.spec
[temp.variadic]: temp.md#temp.variadic

[^1]: There is no special provision for a *decl-specifier-seq* that
    lacks a *type-specifier* or that has a *type-specifier* that only
    specifies *cv-qualifier*s. The “implicit int” rule of C is no longer
    supported.

[^2]: As indicated by syntax, cv-qualifiers are a significant component
    in function return types.

[^3]: One can explicitly disambiguate the parse either by introducing a
    comma (so the ellipsis will be parsed as part of the
    *parameter-declaration-clause*) or by introducing a name for the
    parameter (so the ellipsis will be parsed as part of the
    *declarator-id*).

[^4]: This means that default arguments cannot appear, for example, in
    declarations of pointers to functions, references to functions, or
    `typedef` declarations.

[^5]: As specified in  [[conv.ptr]], converting an integer literal whose
    value is `0` to a pointer type results in a null pointer value.

[^6]: The syntax provides for empty *braced-init-list*s, but nonetheless
    C++ does not have zero length arrays.

[^7]: This requires a conversion function [[class.conv.fct]] returning a
    reference type.

[^8]: Implementations are permitted to provide additional predefined
    variables with names that are reserved to the implementation
    [[lex.name]]. If a predefined variable is not odr-used
    [[basic.def.odr]], its string value need not be present in the
    program image.

[^9]: This set of values is used to define promotion and conversion
    semantics for the enumeration type. It does not preclude an
    expression of enumeration type from having a value that falls
    outside this range.

[^10]: this implies that the name of the class or function is
    unqualified.

[^11]: During name lookup in a class hierarchy, some ambiguities may be
    resolved by considering whether one member hides the other along
    some paths [[class.member.lookup]]. There is no such disambiguation
    when considering the set of names found as a result of following
    *using-directive*s.

[^12]: A *using-declaration* with more than one *using-declarator* is
    equivalent to a corresponding sequence of *using-declaration*s with
    one *using-declarator* each.
