# Compatibility (informative) <a id="diff" data-annex="true" data-annex-type="informative">[[diff]]</a>

## C++and ISO C <a id="diff.iso">[[diff.iso]]</a>

This subclause lists the differences between C++and ISO C, by the
chapters of this document.

### Clause  [[lex]]: lexical conventions <a id="diff.lex">[[diff.lex]]</a>

[[lex.key]] **Change:** New Keywords  
New keywords are added to C++; see [[lex.key]]. **Rationale:** These
keywords were added in order to implement the new semantics of C++.
**Effect on original feature:** Change to semantics of well-defined
feature. Any ISO C programs that used any of these keywords as
identifiers are not valid C++programs. Syntactic transformation.
Converting one specific program is easy. Converting a large collection
of related programs takes more work. Common.

[[lex.ccon]] **Change:** Type of character literal is changed from `int`
to `char` **Rationale:** This is needed for improved overloaded function
argument type matching. For example:

``` cpp
int function( int i );
int function( char c );

function( 'x' );
```

It is preferable that this call match the second version of function
rather than the first. **Effect on original feature:** Change to
semantics of well-defined feature. ISO C programs which depend on

``` cpp
sizeof('x') == sizeof(int)
```

will not work the same as C++programs. Simple. Programs which depend
upon `sizeof('x')` are probably rare.

Subclause [[lex.string]]: **Change:** String literals made const  
The type of a string literal is changed from “array of `char`” to “array
of `const char`.” The type of a `char16_t` string literal is changed
from “array of *some-integer-type*” to “array of `const char16_t`.” The
type of a `char32_t` string literal is changed from “array of
*some-integer-type*” to “array of `const char32_t`.” The type of a wide
string literal is changed from “array of `wchar_t`” to “array of
`const wchar_t`.” **Rationale:** This avoids calling an inappropriate
overloaded function, which might expect to be able to modify its
argument. **Effect on original feature:** Change to semantics of
well-defined feature. Syntactic transformation. The fix is to add a
cast:

``` cpp
char* p = "abc";                // valid in C, invalid in C++
void f(char*) {
  char* p = (char*)"abc";       // OK: cast added
  f(p);
  f((char*)"def");              // OK: cast added
}
```

Programs that have a legitimate reason to treat string literals as
pointers to potentially modifiable memory are probably rare.

### Clause  [[basic]]: basic concepts <a id="diff.basic">[[diff.basic]]</a>

[[basic.def]] **Change:** C++does not have “tentative definitions” as in
C E.g., at file scope,

``` cpp
int i;
int i;
```

is valid in C, invalid in C++. This makes it impossible to define
mutually referential file-local static objects, if initializers are
restricted to the syntactic forms of C. For example,

``` cpp
struct X { int i; struct X* next; };

static struct X a;
static struct X b = { 0, &a };
static struct X a = { 1, &b };
```

**Rationale:** This avoids having different initialization rules for
fundamental types and user-defined types. **Effect on original
feature:** Deletion of semantically well-defined feature. Semantic
transformation. **Rationale:** In C++, the initializer for one of a set
of mutually-referential file-local static objects must invoke a function
call to achieve the initialization. Seldom.

[[basic.scope]] **Change:** A `struct` is a scope in C++, not in C
**Rationale:** Class scope is crucial to C++, and a struct is a class.
**Effect on original feature:** Change to semantics of well-defined
feature. Semantic transformation. C programs use `struct` extremely
frequently, but the change is only noticeable when `struct`,
enumeration, or enumerator names are referred to outside the `struct`.
The latter is probably rare.

[[basic.link]] \[also [[dcl.type]]\] **Change:** A name of file scope
that is explicitly declared `const`, and not explicitly declared
`extern`, has internal linkage, while in C it would have external
linkage **Rationale:** Because `const` objects can be used as
compile-time values in C++, this feature urges programmers to provide
explicit initializer values for each `const`. This feature allows the
user to put `const`objects in header files that are included in many
compilation units. **Effect on original feature:** Change to semantics
of well-defined feature. Semantic transformation Seldom

[[basic.start]] **Change:** Main cannot be called recursively and cannot
have its address taken **Rationale:** The main function may require
special actions. **Effect on original feature:** Deletion of
semantically well-defined feature Trivial: create an intermediary
function such as `mymain(argc, argv)`. Seldom

[[basic.types]] **Change:** C allows “compatible types” in several
places, C++does not For example, otherwise-identical `struct` types with
different tag names are “compatible” in C but are distinctly different
types in C++. **Rationale:** Stricter type checking is essential for
C++. **Effect on original feature:** Deletion of semantically
well-defined feature. Semantic transformation. The “typesafe linkage”
mechanism will find many, but not all, of such problems. Those problems
not found by typesafe linkage will continue to function properly,
according to the “layout compatibility rules” of this International
Standard. Common.

### Clause  [[conv]]: standard conversions <a id="diff.conv">[[diff.conv]]</a>

[[conv.ptr]] **Change:** Converting `void*` to a pointer-to-object type
requires casting

``` cpp
char a[10];
void* b=a;
void foo() {
  char* c=b;
}
```

ISO C will accept this usage of pointer to void being assigned to a
pointer to object type. C++will not. **Rationale:** C++tries harder than
C to enforce compile-time type safety. **Effect on original feature:**
Deletion of semantically well-defined feature. Could be automated.
Violations will be diagnosed by the C++translator. The fix is to add a
cast. For example:

``` cpp
char* c = (char*) b;
```

This is fairly widely used but it is good programming practice to add
the cast when assigning pointer-to-void to pointer-to-object. Some ISO C
translators will give a warning if the cast is not used.

### Clause  [[expr]]: expressions <a id="diff.expr">[[diff.expr]]</a>

[[expr.call]] **Change:** Implicit declaration of functions is not
allowed **Rationale:** The type-safe nature of C++. **Effect on original
feature:** Deletion of semantically well-defined feature. Note: the
original feature was labeled as “obsolescent” in ISO C. Syntactic
transformation. Facilities for producing explicit function declarations
are fairly widespread commercially. Common.

[[expr.sizeof]], [[expr.cast]] **Change:** Types must be declared in
declarations, not in expressions In C, a sizeof expression or cast
expression may create a new type. For example,

``` cpp
p = (void*)(struct x {int i;} *)0;
```

declares a new type, struct x . **Rationale:** This prohibition helps to
clarify the location of declarations in the source code. **Effect on
original feature:** Deletion of a semantically well-defined feature.
Syntactic transformation. Seldom.

[[expr.cond]], [[expr.ass]], [[expr.comma]]

**Change:** The result of a conditional expression, an assignment
expression, or a comma expression may be an lvalue **Rationale:** C++is
an object-oriented language, placing relatively more emphasis on
lvalues. For example, functions may return lvalues. **Effect on original
feature:** Change to semantics of well-defined feature. Some C
expressions that implicitly rely on lvalue-to-rvalue conversions will
yield different results. For example,

``` cpp
char arr[100];
sizeof(0, arr)
```

yields `100` in C++and `sizeof(char*)` in C. Programs must add explicit
casts to the appropriate rvalue. Rare.

### Clause  [[stmt.stmt]]: statements <a id="diff.stat">[[diff.stat]]</a>

[[stmt.switch]], [[stmt.goto]] **Change:** It is now invalid to jump
past a declaration with explicit or implicit initializer (except across
entire block not entered) **Rationale:** Constructors used in
initializers may allocate resources which need to be de-allocated upon
leaving the block. Allowing jump past initializers would require
complicated run-time determination of allocation. Furthermore, any use
of the uninitialized object could be a disaster. With this simple
compile-time rule, C++assures that if an initialized variable is in
scope, then it has assuredly been initialized. **Effect on original
feature:** Deletion of semantically well-defined feature. Semantic
transformation. Seldom.

[[stmt.return]] **Change:** It is now invalid to return (explicitly or
implicitly) from a function which is declared to return a value without
actually returning a value **Rationale:** The caller and callee may
assume fairly elaborate return-value mechanisms for the return of class
objects. If some flow paths execute a return without specifying any
value, the implementation must embody many more complications. Besides,
promising to return a value of a given type, and then not returning such
a value, has always been recognized to be a questionable practice,
tolerated only because very-old C had no distinction between void
functions and int functions. **Effect on original feature:** Deletion of
semantically well-defined feature. Semantic transformation. Add an
appropriate return value to the source code, such as zero. Seldom. For
several years, many existing C implementations have produced warnings in
this case.

### Clause  [[dcl.dcl]]: declarations <a id="diff.dcl">[[diff.dcl]]</a>

[[dcl.stc]] **Change:** In C++, the `static` or `extern` specifiers can
only be applied to names of objects or functions Using these specifiers
with type declarations is illegal in C++. In C, these specifiers are
ignored when used on type declarations.

Example:

``` cpp
static struct S {               // valid C, invalid in C++
  int i;
};
```

**Rationale:** Storage class specifiers don’t have any meaning when
associated with a type. In C++, class members can be declared with the
`static` storage class specifier. Allowing storage class specifiers on
type declarations could render the code confusing for users. **Effect on
original feature:** Deletion of semantically well-defined feature.
Syntactic transformation. Seldom.

[[dcl.typedef]] **Change:** A C++typedef name must be different from any
class type name declared in the same scope (except if the typedef is a
synonym of the class name with the same name). In C, a typedef name and
a struct tag name declared in the same scope can have the same name
(because they have different name spaces)

Example:

``` cpp
typedef struct name1 { /*...*/ } name1;         // valid C and C++
struct name { /*...*/ };
typedef int name;               // valid C, invalid C++
```

**Rationale:** For ease of use, C++doesn’t require that a type name be
prefixed with the keywords `class`, `struct` or `union` when used in
object declarations or type casts.

Example:

``` cpp
class name { /*...*/ };
name i;                         // i has type class name
```

**Effect on original feature:** Deletion of semantically well-defined
feature. Semantic transformation. One of the 2 types has to be renamed.
Seldom.

[[dcl.type]] \[see also [[basic.link]]\] **Change:** const objects must
be initialized in C++but can be left uninitialized in C **Rationale:** A
const object cannot be assigned to so it must be initialized to hold a
useful value. **Effect on original feature:** Deletion of semantically
well-defined feature. Semantic transformation. Seldom.

[[dcl.type]] **Change:** Banning implicit int

In C++a *decl-specifier-seq* must contain a *type-specifier*, unless it
is followed by a declarator for a constructor, a destructor, or a
conversion function. In the following example, the left-hand column
presents valid C; the right-hand column presents equivalent C++:

``` cpp
void f(const parm);            void f(const int parm);
const n = 3;                   const int n = 3;
main()                         int main()
    /* ... */                      /* ... */
```

**Rationale:** In C++, implicit int creates several opportunities for
ambiguity between expressions involving function-like casts and
declarations. Explicit declaration is increasingly considered to be
proper style. Liaison with WG14 (C) indicated support for (at least)
deprecating implicit int in the next revision of C. **Effect on original
feature:** Deletion of semantically well-defined feature. Syntactic
transformation. Could be automated. Common.

[[dcl.spec.auto]] **Change:** The keyword `auto` cannot be used as a
storage class specifier.

``` cpp
void f() {
  auto int x;     // valid C, invalid C++
}
```

**Rationale:** Allowing the use of `auto` to deduce the type of a
variable from its initializer results in undesired interpretations of
`auto` as a storage class specifier in certain contexts. **Effect on
original feature:** Deletion of semantically well-defined feature.
Syntactic transformation. Rare.

[[dcl.enum]] **Change:** C++objects of enumeration type can only be
assigned values of the same enumeration type. In C, objects of
enumeration type can be assigned values of any integral type

Example:

``` cpp
enum color { red, blue, green };
enum color c = 1;               // valid C, invalid C++
```

**Rationale:** The type-safe nature of C++. **Effect on original
feature:** Deletion of semantically well-defined feature. Syntactic
transformation. (The type error produced by the assignment can be
automatically corrected by applying an explicit cast.) Common.

[[dcl.enum]] **Change:** In C++, the type of an enumerator is its
enumeration. In C, the type of an enumerator is `int`.

Example:

``` cpp
enum e { A };
sizeof(A) == sizeof(int)        // in C
sizeof(A) == sizeof(e)          // in C++
/* and sizeof(int) is not necessarily equal to sizeof(e) */
```

**Rationale:** In C++, an enumeration is a distinct type. **Effect on
original feature:** Change to semantics of well-defined feature.
Semantic transformation. Seldom. The only time this affects existing C
code is when the size of an enumerator is taken. Taking the size of an
enumerator is not a common C coding practice.

### Clause  [[dcl.decl]]: declarators <a id="diff.decl">[[diff.decl]]</a>

[[dcl.fct]] **Change:** In C++, a function declared with an empty
parameter list takes no arguments. In C, an empty parameter list means
that the number and type of the function arguments are unknown.

Example:

``` cpp
int f();            // means   int f(void) in C++
                    // int f( unknown ) in C
```

**Rationale:** This is to avoid erroneous function calls (i.e., function
calls with the wrong number or type of arguments). **Effect on original
feature:** Change to semantics of well-defined feature. This feature was
marked as “obsolescent” in C. Syntactic transformation. The function
declarations using C incomplete declaration style must be completed to
become full prototype declarations. A program may need to be updated
further if different calls to the same (non-prototype) function have
different numbers of arguments or if the type of corresponding arguments
differed. Common.

[[dcl.fct]] \[see [[expr.sizeof]]\] **Change:** In C++, types may not be
defined in return or parameter types. In C, these type definitions are
allowed

Example:

``` cpp
void f( struct S { int a; } arg ) {}    // valid C, invalid C++
enum E { A, B, C } f() {}               // valid C, invalid C++
```

**Rationale:** When comparing types in different compilation units,
C++relies on name equivalence when C relies on structural equivalence.
Regarding parameter types: since the type defined in an parameter list
would be in the scope of the function, the only legal calls in C++ would
be from within the function itself. **Effect on original feature:**
Deletion of semantically well-defined feature. Semantic transformation.
The type definitions must be moved to file scope, or in header files.
Seldom. This style of type definitions is seen as poor coding style.

[[dcl.fct.def]] **Change:** In C++, the syntax for function definition
excludes the “old-style” C function. In C, “old-style” syntax is
allowed, but deprecated as “obsolescent.” **Rationale:** Prototypes are
essential to type safety. **Effect on original feature:** Deletion of
semantically well-defined feature. Syntactic transformation. Common in
old programs, but already known to be obsolescent.

[[dcl.init.string]] **Change:** In C++, when initializing an array of
character with a string, the number of characters in the string
(including the terminating `'\0'`) must not exceed the number of
elements in the array. In C, an array can be initialized with a string
even if the array is not large enough to contain the string-terminating
`'\0'`

Example:

``` cpp
char array[4] = "abcd";         // valid C, invalid C++
```

**Rationale:** When these non-terminated arrays are manipulated by
standard string routines, there is potential for major catastrophe.
**Effect on original feature:** Deletion of semantically well-defined
feature. Semantic transformation. The arrays must be declared one
element bigger to contain the string terminating `'\0'`. Seldom. This
style of array initialization is seen as poor coding style.

### Clause  [[class]]: classes <a id="diff.class">[[diff.class]]</a>

[[class.name]] \[see also [[dcl.typedef]]\] **Change:** In C++, a class
declaration introduces the class name into the scope where it is
declared and hides any object, function or other declaration of that
name in an enclosing scope. In C, an inner scope declaration of a struct
tag name never hides the name of an object or function in an outer scope

Example:

``` cpp
int x[99];
void f() {
  struct x { int a; };
  sizeof(x);  /* size of the array in C */
  /* size of the struct in C++ */
}
```

**Rationale:** This is one of the few incompatibilities between C and
C++that can be attributed to the new C++name space definition where a
name can be declared as a type and as a non-type in a single scope
causing the non-type name to hide the type name and requiring that the
keywords `class`, `struct`, `union` or `enum` be used to refer to the
type name. This new name space definition provides important notational
conveniences to C++programmers and helps making the use of the
user-defined types as similar as possible to the use of fundamental
types. The advantages of the new name space definition were judged to
outweigh by far the incompatibility with C described above. **Effect on
original feature:** Change to semantics of well-defined feature.
Semantic transformation. If the hidden name that needs to be accessed is
at global scope, the `::` C++operator can be used. If the hidden name is
at block scope, either the type or the struct tag has to be renamed.
Seldom.

[[class.bit]] **Change:** Bit-fields of type plain `int` are signed.
**Rationale:** Leaving the choice of signedness to implementations could
lead to inconsistent definitions of template specializations. For
consistency, the implementation freedom was eliminated for non-dependent
types, too. **Effect on original feature:** The choise is
implementation-defined in C, but not so in C++. Syntactic
transformation. Seldom.

[[class.nest]] **Change:** In C++, the name of a nested class is local
to its enclosing class. In C the name of the nested class belongs to the
same scope as the name of the outermost enclosing class.

Example:

``` cpp
struct X {
  struct Y { /* ... */ } y;
};
struct Y yy;                    // valid C, invalid C++
```

**Rationale:** C++classes have member functions which require that
classes establish scopes. The C rule would leave classes as an
incomplete scope mechanism which would prevent C++programmers from
maintaining locality within a class. A coherent set of scope rules for
C++based on the C rule would be very complicated and C++programmers
would be unable to predict reliably the meanings of nontrivial examples
involving nested or local functions. **Effect on original feature:**
Change of semantics of well-defined feature. Semantic transformation. To
make the struct type name visible in the scope of the enclosing struct,
the struct tag could be declared in the scope of the enclosing struct,
before the enclosing struct is defined. Example:

``` cpp
struct Y;                       // struct Y and struct X are at the same scope
struct X {
  struct Y { /* ... */ } y;
};
```

All the definitions of C struct types enclosed in other struct
definitions and accessed outside the scope of the enclosing struct could
be exported to the scope of the enclosing struct. Note: this is a
consequence of the difference in scope rules, which is documented in
[[basic.scope]]. Seldom.

[[class.nested.type]] **Change:** In C++, a typedef name may not be
redeclared in a class definition after being used in that definition

Example:

``` cpp
typedef int I;
struct S {
  I i;
  int I;                  // valid C, invalid C++
};
```

**Rationale:** When classes become complicated, allowing such a
redefinition after the type has been used can create confusion for C++
programmers as to what the meaning of ’I’ really is. **Effect on
original feature:** Deletion of semantically well-defined feature.
Semantic transformation. Either the type or the struct member has to be
renamed. Seldom.

### Clause  [[special]]: special member functions <a id="diff.special">[[diff.special]]</a>

[[class.copy]] **Change:** Copying volatile objects

The implicitly-declared copy constructor and implicitly-declared copy
assignment operator cannot make a copy of a volatile lvalue. For
example, the following is valid in ISO C:

``` cpp
struct X { int i; };
volatile struct X x1 = {0};
struct X x2(x1);                // invalid C++
struct X x3;
x3 = x1;                        // also invalid C++
```

**Rationale:** Several alternatives were debated at length. Changing the
parameter to `volatile` `const` `X&` would greatly complicate the
generation of efficient code for class objects. Discussion of providing
two alternative signatures for these implicitly-defined operations
raised unanswered concerns about creating ambiguities and complicating
the rules that specify the formation of these operators according to the
bases and members. **Effect on original feature:** Deletion of
semantically well-defined feature. Semantic transformation. If volatile
semantics are required for the copy, a user-declared constructor or
assignment must be provided. This user-declared constructor may be
explicitly defaulted. If non-volatile semantics are required, an
explicit `const_cast` can be used. Seldom.

### Clause  [[cpp]]: preprocessing directives <a id="diff.cpp">[[diff.cpp]]</a>

[[cpp.predefined]] **Change:** Whether `__STDC__` is defined and if so,
what its value is, are implementation-defined **Rationale:** C++is not
identical to ISO C. Mandating that `__STDC__` be defined would require
that translators make an incorrect claim. Each implementation must
choose the behavior that will be most useful to its marketplace.
**Effect on original feature:** Change to semantics of well-defined
feature. Semantic transformation. Programs and headers that reference
`__STDC__` are quite common.

## C++and ISO C++03 <a id="diff.cpp03">[[diff.cpp03]]</a>

This subclause lists the differences between C++and ISO C++03(ISO/IEC
14882:2003, *Programming Languages — C++*), by the chapters of this
document.

### Clause  [[lex]]: lexical conventions <a id="diff.cpp03.lex">[[diff.cpp03.lex]]</a>

[[lex.pptoken]] **Change:** New kinds of string literals **Rationale:**
Required for new features. **Effect on original feature:** Valid
C++03code may fail to compile or produce different results in this
International Standard. Specifically, macros named `R`, `u8`, `u8R`,
`u`, `uR`, `U`, `UR`, or `LR` will not be expanded when adjacent to a
string literal but will be interpreted as part of the string literal.
For example,

``` cpp
#define u8 "abc"
const char* s = u8"def";        // Previously "abcdef", now "def"
```

[[lex.pptoken]] **Change:** User-defined literal string support
**Rationale:** Required for new features. **Effect on original
feature:** Valid C++03code may fail to compile or produce different
results in this International Standard, as the following example
illustrates.

``` cpp
#define _x "there"
"hello"_x         // #1
```

Previously, \#1 would have consisted of two separate preprocessing
tokens and the macro `_x` would have been expanded. In this
International Standard, \#1 consists of a single preprocessing tokens,
so the macro is not expanded.

[[lex.key]] **Change:** New keywords **Rationale:** Required for new
features. **Effect on original feature:** Added to Table 
[[tab:keywords]], the following identifiers are new keywords: `alignas`,
`alignof`, `char16_t`, `char32_t`, `constexpr`, `decltype`, `noexcept`,
`nullptr`, `static_assert`, and `thread_local`. Valid C++03code using
these identifiers is invalid in this International Standard.

[[lex.icon]] **Change:** Type of integer literals **Rationale:** C99
compatibility. **Effect on original feature:** Certain integer literals
larger than can be represented by `long` could change from an unsigned
integer type to `signed long long`.

### Clause  [[conv]]: standard conversions <a id="diff.cpp03.conv">[[diff.cpp03.conv]]</a>

[[conv.ptr]] **Change:** Only literals are integer null pointer
constants **Rationale:** Removing surprising interactions with templates
and constant expressions **Effect on original feature:** Valid C++03code
may fail to compile or produce different results in this International
Standard, as the following example illustrates:

``` cpp
void f(void *);  // #1
void f(...);     // #2
template<int N> void g() {
  f(0*N);        // calls #2; used to call #1
}
```

### Clause  [[expr]]: expressions <a id="diff.cpp03.expr">[[diff.cpp03.expr]]</a>

[[expr.mul]] **Change:** Specify rounding for results of integer `/` and
`%` **Rationale:** Increase portability, C99 compatibility. **Effect on
original feature:** Valid C++03code that uses integer division rounds
the result toward 0 or toward negative infinity, whereas this
International Standard always rounds the result toward 0.

### Clause  [[dcl.dcl]]: declarations <a id="diff.cpp03.dcl.dcl">[[diff.cpp03.dcl.dcl]]</a>

[[dcl.spec]] **Change:** Remove `auto` as a storage class specifier
**Rationale:** New feature. **Effect on original feature:** Valid
C++03code that uses the keyword `auto` as a storage class specifier may
be invalid in this International Standard. In this International
Standard, `auto` indicates that the type of a variable is to be deduced
from its initializer expression.

### Clause  [[dcl.decl]]: declarators <a id="diff.cpp03.dcl.decl">[[diff.cpp03.dcl.decl]]</a>

[[dcl.init.list]] **Change:** Narrowing restrictions in aggregate
initializers **Rationale:** Catches bugs. **Effect on original
feature:** Valid C++03code may fail to compile in this International
Standard. For example, the following code is valid in C++03but invalid
in this International Standard because `double` to `int` is a narrowing
conversion:

``` cpp
int x[] = { 2.0 };
```

### Clause  [[special]]: special member functions <a id="diff.cpp03.special">[[diff.cpp03.special]]</a>

[[class.ctor]], [[class.dtor]], [[class.copy]] **Change:**
Implicitly-declared special member functions are defined as deleted when
the implicit definition would have been ill-formed. **Rationale:**
Improves template argument deduction failure. **Effect on original
feature:** A valid C++03program that uses one of these special member
functions in a context where the definition is not required (e.g., in an
expression that is not potentially evaluated) becomes ill-formed.

[[class.dtor]] (destructors) **Change:** User-declared destructors have
an implicit exception specification. **Rationale:** Clarification of
destructor requirements. **Effect on original feature:** Valid C++03code
may execute differently in this International Standard. In particular,
destructors that throw exceptions will call `std::terminate()` (without
calling `std::unexpected()`) if their exception specification is
`noexcept` or `noexcept(true)`. For a throwing virtual destructor of a
derived class, `std::terminate()` can be avoided only if the base class
virtual destructor has an exception specification that is not `noexcept`
and not `noexcept(true)`.

### Clause  [[temp]]: templates <a id="diff.cpp03.temp">[[diff.cpp03.temp]]</a>

[[temp.param]] **Change:** Remove `export` **Rationale:** No
implementation consensus. **Effect on original feature:** A valid
C++03declaration containing `export` is ill-formed in this International
Standard.

[[temp.arg]] **Change:** Remove whitespace requirement for nested
closing template right angle brackets **Rationale:** Considered a
persistent but minor annoyance. Template aliases representing nonclass
types would exacerbate whitespace issues. **Effect on original
feature:** Change to semantics of well-defined expression. A valid
C++03expression containing a right angle bracket (“`>`”) followed
immediately by another right angle bracket may now be treated as closing
two templates. For example, the following code is valid in C++03because
“`\shr`” is a right-shift operator, but invalid in this International
Standard because “`\shr`” closes two templates.

``` cpp
template <class T> struct X { };
template <int N> struct Y { };
X< Y< 1 >> 2 > > x;
```

[[temp.dep.candidate]] **Change:** Allow dependent calls of functions
with internal linkage **Rationale:** Overly constrained, simplify
overload resolution rules. **Effect on original feature:** A valid
C++03program could get a different result than this International
Standard.

### Clause  [[library]]: library introduction <a id="diff.cpp03.library">[[diff.cpp03.library]]</a>

[[library]] – [[thread]] **Change:** New reserved identifiers
**Rationale:** Required by new features. **Effect on original feature:**
Valid C++03code that uses any identifiers added to the C++standard
library by this International Standard may fail to compile or produce
different results in This International Standard. A comprehensive list
of identifiers used by the C++standard library can be found in the Index
of Library Names in this International Standard.

[[headers]] **Change:** New headers **Rationale:** New functionality.
**Effect on original feature:** The following C++headers are new:
`<array>`, `<atomic>`, `<chrono>`, `<codecvt>`, `<condition_variable>`,
`<forward_list>`, `<future>`, `<initializer_list>`, `<mutex>`,
`<random>`, `<ratio>`, `<regex>`, `<scoped_allocator>`,
`<system_error>`, `<thread>`, `<tuple>`, `<typeindex>`,
`<type_traits>`,  
`<unordered_map>`, and `<unordered_set>`. In addition the following C
compatibility headers are new: `<ccomplex>`, `<cfenv>`, `<cinttypes>`,
`<cstdalign>`, `<cstdbool>`, `<cstdint>`, `<ctgmath>`, and `<cuchar>`.
Valid C++03code that `#include`s headers with these names may be invalid
in this International Standard.

[[swappable.requirements]] **Effect on original feature:** Function
`swap` moved to a different header **Rationale:** Remove dependency on
`<algorithm>` for `swap`. **Effect on original feature:** Valid
C++03code that has been compiled expecting swap to be in `<algorithm>`
may have to instead include `<utility>`.

[[namespace.posix]] **Change:** New reserved namespace **Rationale:**
New functionality. **Effect on original feature:** The global namespace
`posix` is now reserved for standardization. Valid C++03code that uses a
top-level namespace `posix` may be invalid in this International
Standard.

[[res.on.macro.definitions]] **Change:** Additional restrictions on
macro names **Rationale:** Avoid hard to diagnose or non-portable
constructs. **Effect on original feature:** Names of attribute
identifiers may not be used as macro names. Valid C++ 2003 code that
defines `override`, `final`, `carries_dependency`, or `noreturn` as
macros is invalid in this International Standard.

### Clause  [[language.support]]: language support library <a id="diff.cpp03.language.support">[[diff.cpp03.language.support]]</a>

[[new.delete.single]] **Change:** Linking `new` and `delete` operators
**Rationale:** The two throwing single-object signatures of
`operator new` and `operator delete` are now specified to form the base
functionality for the other operators. This clarifies that replacing
just these two signatures changes others, even if they are not
explicitly changed. **Effect on original feature:** Valid C++03code that
replaces global `new` or `delete` operators may execute differently in
this International Standard. For example, the following program should
write `"custom deallocation"` twice, once for the single-object delete
and once for the array delete.

``` cpp
#include <cstdio>
#include <cstdlib>
#include <new>

void* operator new(std::size_t size) throw(std::bad_alloc) {
  return std::malloc(size);
}

void operator delete(void* ptr) throw() {
  std::puts("custom deallocation");
  std::free(ptr);
}

int main() {
  int* i = new int;
  delete i;                     // single-object delete
  int* a = new int[3];
  delete [] a;                  // array delete
  return 0;
}
```

[[new.delete.single]] **Change:** `operator new` may throw exceptions
other than `std::bad_alloc` **Rationale:** Consistent application of
`noexcept`. **Effect on original feature:** Valid C++03code that assumes
that global `operator new` only throws `std::bad_alloc` may execute
differently in this International Standard.

### Clause  [[diagnostics]]: diagnostics library <a id="diff.cpp03.diagnostics">[[diff.cpp03.diagnostics]]</a>

[[errno]] **Change:** Thread-local error numbers **Rationale:** Support
for new thread facilities. **Effect on original feature:** Valid but
implementation-specific C++03code that relies on `errno` being the same
across threads may change behavior in this International Standard.

### Clause  [[utilities]]: general utilities library <a id="diff.cpp03.utilities">[[diff.cpp03.utilities]]</a>

[[util.dynamic.safety]] **Change:** Minimal support for
garbage-collected regions **Rationale:** Required by new feature.
**Effect on original feature:** Valid C++03code, compiled without
traceable pointer support, that interacts with newer C++code using
regions declared reachable may have different runtime behavior.

[[refwrap]], [[arithmetic.operations]], [[comparisons]],
[[logical.operations]], [[bitwise.operations]], [[negators]] **Change:**
Standard function object types no longer derived from
`std::unary_function` or `std::binary_function` **Rationale:**
Superseded by new feature. **Effect on original feature:** Valid
C++03code that depends on function object types being derived from
`unary_function` or `binary_function` will execute differently in this
International Standard.

### Clause  [[strings]]: strings library <a id="diff.cpp03.strings">[[diff.cpp03.strings]]</a>

[[string.classes]] **Change:** `basic_string` requirements no longer
allow reference-counted strings **Rationale:** Invalidation is subtly
different with reference-counted strings. This change regularizes
behavior for this International Standard. **Effect on original
feature:** Valid C++03code may execute differently in this International
Standard.

[[string.require]] **Change:** Loosen `basic_string` invalidation rules
**Rationale:** Allow small-string optimization. **Effect on original
feature:** Valid C++03code may execute differently in this International
Standard. Some `const` member functions, such as `data` and `c_str`, no
longer invalidate iterators.

### Clause  [[containers]]: containers library <a id="diff.cpp03.containers">[[diff.cpp03.containers]]</a>

[[container.requirements]] **Change:** Complexity of `size()` member
functions now constant **Rationale:** Lack of specification of
complexity of `size()` resulted in divergent implementations with
inconsistent performance characteristics. **Effect on original
feature:** Some container implementations that conform to C++03may not
conform to the specified `size()` requirements in this International
Standard. Adjusting containers such as `std::list` to the stricter
requirements may require incompatible changes.

[[container.requirements]] **Change:** Requirements change: relaxation
**Rationale:** Clarification. **Effect on original feature:** Valid
C++03code that attempts to meet the specified container requirements may
now be over-specified. Code that attempted to be portable across
containers may need to be adjusted as follows:

- not all containers provide `size()`; use `empty()` instead of
  `size() == 0`;
- not all containers are empty after construction (`array`);
- not all containers have constant complexity for `swap()` (`array`).

[[container.requirements]] **Change:** Requirements change: default
constructible **Rationale:** Clarification of container requirements.
**Effect on original feature:** Valid C++03code that attempts to
explicitly instantiate a container using a user-defined type with no
default constructor may fail to compile.

[[sequence.reqmts]], [[associative.reqmts]] **Change:** Signature
changes: from `void` return types **Rationale:** Old signature threw
away useful information that may be expensive to recalculate. **Effect
on original feature:** The following member functions have changed:

- `erase(iter)` for `set`, `multiset`, `map`, `multimap`
- `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`
- `insert(pos, num, val)` for `vector`, `deque`, `list`, `forward_list`
- `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`

Valid C++03code that relies on these functions returning `void` (e.g.,
code that creates a pointer to member function that points to one of
these functions) will fail to compile with this International Standard.

[[sequence.reqmts]], [[associative.reqmts]] **Change:** Signature
changes: from `iterator` to `const_iterator` parameters **Rationale:**
Overspecification. *Effects:* The signatures of the following member
functions changed from taking an `iterator` to taking a
`const_iterator`:

- `insert(iter, val)` for `vector`, `deque`, `list`, `set`, `multiset`,
  `map`, `multimap`
- `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`
- `erase(iter)` for `set`, `multiset`, `map`, `multimap`
- `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`
- all forms of `list::splice`
- all forms of `list::merge`

Valid C++03code that uses these functions may fail to compile with this
International Standard.

[[sequence.reqmts]], [[associative.reqmts]] **Change:** Signature
changes: `resize` **Rationale:** Performance, compatibility with move
semantics. **Effect on original feature:** For `vector`, `deque`, and
`list` the fill value passed to `resize` is now passed by reference
instead of by value, and an additional overload of `resize` has been
added. Valid C++03code that uses this function may fail to compile with
this International Standard.

### Clause  [[algorithms]]: algorithms library <a id="diff.cpp03.algorithms">[[diff.cpp03.algorithms]]</a>

[[algorithms.general]] **Change:** Result state of inputs after
application of some algorithms **Rationale:** Required by new feature.
**Effect on original feature:** A valid C++03program may detect that an
object with a valid but unspecified state has a different valid but
unspecified state with this International Standard. For example,
`std::remove` and `std::remove_if` may leave the tail of the input
sequence with a different set of values than previously.

### Clause  [[numerics]]: numerics library <a id="diff.cpp03.numerics">[[diff.cpp03.numerics]]</a>

[[complex.numbers]] **Change:** Specified representation of complex
numbers **Rationale:** Compatibility with C99. **Effect on original
feature:** Valid C++03code that uses implementation-specific knowledge
about the binary representation of the required template specializations
of `std::complex` may not be compatible with this International
Standard.

### Clause  [[input.output]]: Input/output library <a id="diff.cpp03.input.output">[[diff.cpp03.input.output]]</a>

[[istream::sentry]], [[ostream::sentry]], [[iostate.flags]] **Change:**
Specify use of explicit in existing boolean conversion operators
**Rationale:** Clarify intentions, avoid workarounds. **Effect on
original feature:** Valid C++03code that relies on implicit boolean
conversions will fail to compile with this International Standard. Such
conversions occur in the following conditions:

- passing a value to a function that takes an argument of type `bool`;
- using `operator==` to compare to `false` or `true`;
- returning a value from a function with a return type of `bool`;
- initializing members of type `bool` via aggregate initialization;
- initializing a `const bool&` which would bind to a temporary.

[[ios::failure]] **Change:** Change base class of
`std::ios_base::failure` **Rationale:** More detailed error messages.
**Effect on original feature:** `std::ios_base::failure` is no longer
derived directly from `std::exception`, but is now derived from
`std::system_error`, which in turn is derived from `std::runtime_error`.
Valid C++03code that assumes that `std::ios_base::failure` is derived
directly from `std::exception` may execute differently in this
International Standard.

[[ios.base]] **Change:** Flag types in `std::ios_base` are now bitmasks
with values defined as constexpr static members **Rationale:** Required
for new features. **Effect on original feature:** Valid C++03code that
relies on `std::ios_base` flag types being represented as `std::bitset`
or as an integer type may fail to compile with this International
Standard. For example:

``` cpp
#include <iostream>

int main() {
  int flag = std::ios_base::hex;
  std::cout.setf(flag);         // error: setf does not take argument of type int
  return 0;
}
```

## C++and ISO C++11 <a id="diff.cpp11">[[diff.cpp11]]</a>

This subclause lists the differences between C++and ISO C++11(ISO/IEC
14882:2011, *Programming Languages — C++*), by the chapters of this
document.

### Clause  [[lex]]: lexical conventions <a id="diff.cpp11.lex">[[diff.cpp11.lex]]</a>

[[lex.ppnumber]] **Change:** *pp-number* can contain one or more single
quotes. **Rationale:** Necessary to enable single quotes as digit
separators. **Effect on original feature:** Valid C++11code may fail to
compile or may change meaning in this International Standard. For
example, the following code is valid both in C++11and in this
International Standard, but the macro invocation produces different
outcomes because the single quotes delimit a character literal in C++11,
whereas they are digit separators in this International Standard:

``` cpp
#define M(x, ...) __VA_ARGS__
int x[2] = { M(1'2,3'4) };
// int x[2] = {\ \ \ \ \ } --- C++11
// int x[2] = { 3'4 } --- this International Standard
```

### Clause  [[basic]]: basic concepts <a id="diff.cpp11.basic">[[diff.cpp11.basic]]</a>

[[basic.stc.dynamic.deallocation]] **Change:** New usual (non-placement)
deallocator **Rationale:** Required for sized deallocation. **Effect on
original feature:** Valid C++11code could declare a global placement
allocation function and deallocation function as follows:

``` cpp
void operator new(std::size_t, std::size_t);
void operator delete(void*, std::size_t) noexcept;
```

In this International Standard, however, the declaration of
`operator delete` might match a predefined usual (non-placement)
`operator delete` ([[basic.stc.dynamic]]). If so, the program is
ill-formed, as it was for class member allocation functions and
deallocation functions ([[expr.new]]).

### Clause  [[dcl.dcl]]: declarations <a id="diff.cpp11.dcl.dcl">[[diff.cpp11.dcl.dcl]]</a>

[[dcl.constexpr]] **Change:** `constexpr` non-static member functions
are not implicitly `const` member functions. **Rationale:** Necessary to
allow `constexpr` member functions to mutate the object. **Effect on
original feature:** Valid C++11code may fail to compile in this
International Standard. For example, the following code is valid in
C++11 but invalid in this International Standard because it declares the
same member function twice with different return types:

``` cpp
struct S {
  constexpr const int &f();
  int &f();
};
```

### Clause  [[input.output]]: input/output library <a id="diff.cpp11.input.output">[[diff.cpp11.input.output]]</a>

[[c.files]] **Change:** `gets` is not defined. **Rationale:** Use of
`gets` is considered dangerous. **Effect on original feature:** Valid
C++11code that uses the `gets` function may fail to compile in this
International Standard.

## C standard library <a id="diff.library">[[diff.library]]</a>

This subclause summarizes the contents of the C++standard library
included from the Standard C library. It also summarizes the explicit
changes in definitions, declarations, or behavior from the Standard C
library noted in other subclauses ([[headers]], [[support.types]],
[[c.strings]]).

The C++standard library provides 57 standard macros from the C library,
as shown in Table  [[tab:diff.standard.macros]].

The header names (enclosed in `<` and `>`) indicate that the macro may
be defined in more than one header. All such definitions are equivalent
([[basic.def.odr]]).

**Table: Standard macros** <a id="tab:diff.standard.macros">[tab:diff.standard.macros]</a>

|                  |                  |                 |           |                  |
| ---------------- | ---------------- | --------------- | --------- | ---------------- |
| `BUFSIZ`         | `LC_ALL`         | `NULL <ctime>`  | `SIGSEGV` | `va_start`       |
| `CLOCKS_PER_SEC` | `LC_COLLATE`     | `NULL <cwchar>` | `SIGTERM` | `WCHAR_MAX`      |
| `EDOM`           | `LC_CTYPE`       | `offsetof`      | `SIG_DFL` | `WCHAR_MIN`      |
| `EILSEQ`         | `LC_MONETARY`    | `RAND_MAX`      | `SIG_ERR` | `WEOF <cwchar>`  |
| `EOF`            | `LC_NUMERIC`     | `SEEK_CUR`      | `SIG_IGN` | `WEOF <cwctype>` |
| `ERANGE`         | `LC_TIME`        | `SEEK_END`      | `stderr`  | `_IOFBF`         |
| `errno`          | `L_tmpnam`       | `SEEK_SET`      | `stdin`   | `_IOLBF`         |
| `EXIT_FAILURE`   | `MB_CUR_MAX`     | `setjmp`        | `stdout`  | `_IONBF`         |
| `EXIT_SUCCESS`   | `NULL <clocale>` | `SIGABRT`       | `TMP_MAX` |                  |
| `FILENAME_MAX`   | `NULL <cstddef>` | `SIGFPE`        | `va_arg`  |                  |
| `FOPEN_MAX`      | `NULL <cstdlib>` | `SIGILL`        | `va_copy` |                  |


The C++standard library provides 57 standard values from the C library,
as shown in Table  [[tab:diff.standard.values]].

**Table: Standard values** <a id="tab:diff.standard.values">[tab:diff.standard.values]</a>

|                  |                  |                   |             |
| ---------------- | ---------------- | ----------------- | ----------- |
| `CHAR_MAX`       | `FLT_EPSILON`    | `LDBL_DIG`        | `SCHAR_MAX` |
| `CHAR_MIN`       | `FLT_MANT_DIG`   | `LDBL_EPSILON`    | `SCHAR_MIN` |
| `DBL_DIG`        | `FLT_MAX`        | `LDBL_MANT_DIG`   | `SHRT_MAX`  |
| `DBL_EPSILON`    | `FLT_MAX_10_EXP` | `LDBL_MAX`        | `SHRT_MIN`  |
| `DBL_MANT_DIG`   | `FLT_MAX_EXP`    | `LDBL_MAX_10_EXP` | `UCHAR_MAX` |
| `DBL_MAX`        | `FLT_MIN`        | `LDBL_MAX_EXP`    | `UINT_MAX`  |
| `DBL_MAX_10_EXP` | `FLT_MIN_10_EXP` | `LDBL_MIN`        | `ULONG_MAX` |
| `DBL_MAX_EXP`    | `FLT_MIN_EXP`    | `LDBL_MIN_10_EXP` | `USHRT_MAX` |
| `DBL_MIN`        | `FLT_RADIX`      | `LDBL_MIN_EXP`    |             |
| `DBL_MIN_10_EXP` | `FLT_ROUNDS`     | `LONG_MAX`        |             |
| `DBL_MIN_EXP`    | `INT_MAX`        | `LONG_MIN`        |             |


The C++standard library provides 20 standard types from the C library,
as shown in Table  [[tab:diff.standard.types]].

**Table: Standard types** <a id="tab:diff.standard.types">[tab:diff.standard.types]</a>

|           |                    |                    |                    |
| --------- | ------------------ | ------------------ | ------------------ |
| `div_t`   | `mbstate_t`        | `size_t <cstdlib>` | `wctrans_t`        |
| `FILE`    | `ptrdiff_t`        | `size_t <cstring>` | `wctype_t`         |
| `fpos_t`  | `sig_atomic_t`     | `size_t <ctime>`   | `wint_t <cwchar>`  |
| `jmp_buf` | `size_t <cstddef>` | `time_t`           | `wint_t <cwctype>` |


The C++standard library provides 2 standard `struct`s from the C
library, as shown in Table  [[tab:diff.standard.structs]].

**Table: Standard structs** <a id="tab:diff.standard.structs">[tab:diff.standard.structs]</a>



The C++standard library provides 209 standard functions from the C
library, as shown in Table  [[tab:diff.standard.functions]].

**Table: Standard functions** <a id="tab:diff.standard.functions">[tab:diff.standard.functions]</a>

|            |            |              |             |             |             |
| ---------- | ---------- | ------------ | ----------- | ----------- | ----------- |
| `abs`      | `fopen`    | `iswalpha`   | `perror`    | `strncat`   | `wcschr`    |
| `acos`     | `fprintf`  | `iswcntrl`   | `pow`       | `strncmp`   | `wcscmp`    |
| `asctime`  | `fputc`    | `iswctype`   | `printf`    | `strncpy`   | `wcscoll`   |
| `asin`     | `fputs`    | `iswdigit`   | `putc`      | `strpbrk`   | `wcscpy`    |
| `atan`     | `fputwc`   | `iswgraph`   | `putchar`   | `strrchr`   | `wcscspn`   |
| `atan2`    | `fputws`   | `iswlower`   | `puts`      | `strspn`    | `wcsftime`  |
| `atexit`   | `fread`    | `iswprint`   | `putwc`     | `strstr`    | `wcslen`    |
| `atof`     | `free`     | `iswpunct`   | `putwchar`  | `strtod`    | `wcsncat`   |
| `atoi`     | `freopen`  | `iswspace`   | `qsort`     | `strtok`    | `wcsncmp`   |
| `atol`     | `frexp`    | `iswupper`   | `raise`     | `strtol`    | `wcsncpy`   |
| `bsearch`  | `fscanf`   | `iswxdigit`  | `rand`      | `strtoul`   | `wcspbrk`   |
| `btowc`    | `fseek`    | `isxdigit`   | `realloc`   | `strxfrm`   | `wcsrchr`   |
| `calloc`   | `fsetpos`  | `labs`       | `remove`    | `swprintf`  | `wcsrtombs` |
| `ceil`     | `ftell`    | `ldexp`      | `rename`    | `swscanf`   | `wcsspn`    |
| `clearerr` | `fwide`    | `ldiv`       | `rewind`    | `system`    | `wcsstr`    |
| `clock`    | `fwprintf` | `localeconv` | `scanf`     | `tan`       | `wcstod`    |
| `cos`      | `fwrite`   | `localtime`  | `setbuf`    | `tanh`      | `wcstok`    |
| `cosh`     | `fwscanf`  | `log`        | `setlocale` | `time`      | `wcstol`    |
| `ctime`    | `getc`     | `log10`      | `setvbuf`   | `tmpfile`   | `wcstombs`  |
| `difftime` | `getchar`  | `longjmp`    | `signal`    | `tmpnam`    | `wcstoul`   |
| `div`      | `getenv`   | `malloc`     | `sin`       | `tolower`   | `wcsxfrm`   |
| `exit`     | `getwc`    | `mblen`      | `sinh`      | `toupper`   | `wctob`     |
| `exp`      | `getwchar` | `mbrlen`     | `sprintf`   | `towctrans` | `wctomb`    |
| `fabs`     | `gmtime`   | `mbrtowc`    | `sqrt`      | `towlower`  | `wctrans`   |
| `fclose`   | `isalnum`  | `mbsinit`    | `srand`     | `towupper`  | `wctype`    |
| `feof`     | `isalpha`  | `mbsrtowcs`  | `sscanf`    | `ungetc`    | `wmemchr`   |
| `ferror`   | `iscntrl`  | `mbstowcs`   | `strcat`    | `ungetwc`   | `wmemcmp`   |
| `fflush`   | `isdigit`  | `mbtowc`     | `strchr`    | `vfprintf`  | `wmemcpy`   |
| `fgetc`    | `isgraph`  | `memchr`     | `strcmp`    | `vfwprintf` | `wmemmove`  |
| `fgetpos`  | `islower`  | `memcmp`     | `strcoll`   | `vprintf`   | `wmemset`   |
| `fgets`    | `isprint`  | `memcpy`     | `strcpy`    | `vsprintf`  | `wprintf`   |
| `fgetwc`   | `ispunct`  | `memmove`    | `strcspn`   | `vswprintf` | `wscanf`    |
| `fgetws`   | `isspace`  | `memset`     | `strerror`  | `vwprintf`  |             |
| `floor`    | `isupper`  | `mktime`     | `strftime`  | `wcrtomb`   |             |


### Modifications to headers <a id="diff.mods.to.headers">[[diff.mods.to.headers]]</a>

For compatibility with the Standard C library, the C++standard library
provides the C headers enumerated in  [[depr.c.headers]], but their use
is deprecated in C++.

### Modifications to definitions <a id="diff.mods.to.definitions">[[diff.mods.to.definitions]]</a>

#### Types `char16_t` and `char32_t` <a id="diff.char16">[[diff.char16]]</a>

The types `char16_t` and `char32_t` are distinct types rather than
typedefs to existing integral types.

#### Type `wchar_t` <a id="diff.wchar.t">[[diff.wchar.t]]</a>

`wchar_t`

is a keyword in this International Standard ([[lex.key]]). It does not
appear as a type name defined in any of `<cstddef>`, `<cstdlib>`, or
`<cwchar>` ([[c.strings]]).

#### Header `<iso646.h>` <a id="diff.header.iso646.h">[[diff.header.iso646.h]]</a>

The tokens `and`, `and_eq`, `bitand`, `bitor`, `compl`, `not_eq`, `not`,
`or`, `or_eq`, `xor`, and `xor_eq` are keywords in this International
Standard ([[lex.key]]). They do not appear as macro names defined in
`<ciso646>`.

#### Macro `NULL` <a id="diff.null">[[diff.null]]</a>

The macro `NULL`, defined in any of `<clocale>`, `<cstddef>`,
`<cstdio>`, `<cstdlib>`, `<cstring>`, `<ctime>`, or `<cwchar>`, is an
implementation-defined C++null pointer constant in this International
Standard ([[support.types]]).

### Modifications to declarations <a id="diff.mods.to.declarations">[[diff.mods.to.declarations]]</a>

Header `<cstring>`: The following functions have different declarations:

- `strchr`
- `strpbrk`
- `strrchr`
- `strstr`
- `memchr`

[[c.strings]] describes the changes.

### Modifications to behavior <a id="diff.mods.to.behavior">[[diff.mods.to.behavior]]</a>

Header `<cstdlib>`: The following functions have different behavior:

- `atexit`
- `exit`
- `abort`

[[support.start.term]] describes the changes.

Header `<csetjmp>`: The following functions have different behavior:

- `longjmp`

[[support.runtime]] describes the changes.

#### Macro `offsetof(type, member-designator)` <a id="diff.offsetof">[[diff.offsetof]]</a>

The macro `offsetof`, defined in `<cstddef>`, accepts a restricted set
of `type` arguments in this International Standard. [[support.types]]
describes the change.

#### Memory allocation functions <a id="diff.malloc">[[diff.malloc]]</a>

The functions `calloc`, `malloc`, and `realloc` are restricted in this
International Standard. [[c.malloc]] describes the changes.

<!-- Link reference definitions -->
[algorithms]: algorithms.md#algorithms
[algorithms.general]: algorithms.md#algorithms.general
[arithmetic.operations]: utilities.md#arithmetic.operations
[associative.reqmts]: containers.md#associative.reqmts
[basic]: basic.md#basic
[basic.def]: basic.md#basic.def
[basic.def.odr]: basic.md#basic.def.odr
[basic.link]: basic.md#basic.link
[basic.scope]: basic.md#basic.scope
[basic.start]: basic.md#basic.start
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.types]: basic.md#basic.types
[bitwise.operations]: utilities.md#bitwise.operations
[c.files]: input.md#c.files
[c.malloc]: utilities.md#c.malloc
[c.strings]: strings.md#c.strings
[class]: class.md#class
[class.bit]: class.md#class.bit
[class.copy]: special.md#class.copy
[class.ctor]: special.md#class.ctor
[class.dtor]: special.md#class.dtor
[class.name]: class.md#class.name
[class.nest]: class.md#class.nest
[class.nested.type]: class.md#class.nested.type
[comparisons]: utilities.md#comparisons
[complex.numbers]: numerics.md#complex.numbers
[container.requirements]: containers.md#container.requirements
[containers]: containers.md#containers
[conv]: conv.md#conv
[conv.ptr]: conv.md#conv.ptr
[cpp]: cpp.md#cpp
[cpp.predefined]: cpp.md#cpp.predefined
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.decl]: dcl.md#dcl.decl
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def]: dcl.md#dcl.fct.def
[dcl.init.list]: dcl.md#dcl.init.list
[dcl.init.string]: dcl.md#dcl.init.string
[dcl.spec]: dcl.md#dcl.spec
[dcl.spec.auto]: dcl.md#dcl.spec.auto
[dcl.stc]: dcl.md#dcl.stc
[dcl.type]: dcl.md#dcl.type
[dcl.typedef]: dcl.md#dcl.typedef
[depr.c.headers]: future.md#depr.c.headers
[diagnostics]: diagnostics.md#diagnostics
[diff]: #diff
[diff.basic]: #diff.basic
[diff.char16]: #diff.char16
[diff.class]: #diff.class
[diff.conv]: #diff.conv
[diff.cpp]: #diff.cpp
[diff.cpp03]: #diff.cpp03
[diff.cpp03.algorithms]: #diff.cpp03.algorithms
[diff.cpp03.containers]: #diff.cpp03.containers
[diff.cpp03.conv]: #diff.cpp03.conv
[diff.cpp03.dcl.dcl]: #diff.cpp03.dcl.dcl
[diff.cpp03.dcl.decl]: #diff.cpp03.dcl.decl
[diff.cpp03.diagnostics]: #diff.cpp03.diagnostics
[diff.cpp03.expr]: #diff.cpp03.expr
[diff.cpp03.input.output]: #diff.cpp03.input.output
[diff.cpp03.language.support]: #diff.cpp03.language.support
[diff.cpp03.lex]: #diff.cpp03.lex
[diff.cpp03.library]: #diff.cpp03.library
[diff.cpp03.numerics]: #diff.cpp03.numerics
[diff.cpp03.special]: #diff.cpp03.special
[diff.cpp03.strings]: #diff.cpp03.strings
[diff.cpp03.temp]: #diff.cpp03.temp
[diff.cpp03.utilities]: #diff.cpp03.utilities
[diff.cpp11]: #diff.cpp11
[diff.cpp11.basic]: #diff.cpp11.basic
[diff.cpp11.dcl.dcl]: #diff.cpp11.dcl.dcl
[diff.cpp11.input.output]: #diff.cpp11.input.output
[diff.cpp11.lex]: #diff.cpp11.lex
[diff.dcl]: #diff.dcl
[diff.decl]: #diff.decl
[diff.expr]: #diff.expr
[diff.header.iso646.h]: #diff.header.iso646.h
[diff.iso]: #diff.iso
[diff.lex]: #diff.lex
[diff.library]: #diff.library
[diff.malloc]: #diff.malloc
[diff.mods.to.behavior]: #diff.mods.to.behavior
[diff.mods.to.declarations]: #diff.mods.to.declarations
[diff.mods.to.definitions]: #diff.mods.to.definitions
[diff.mods.to.headers]: #diff.mods.to.headers
[diff.null]: #diff.null
[diff.offsetof]: #diff.offsetof
[diff.special]: #diff.special
[diff.stat]: #diff.stat
[diff.wchar.t]: #diff.wchar.t
[errno]: diagnostics.md#errno
[expr]: expr.md#expr
[expr.ass]: expr.md#expr.ass
[expr.call]: expr.md#expr.call
[expr.cast]: expr.md#expr.cast
[expr.comma]: expr.md#expr.comma
[expr.cond]: expr.md#expr.cond
[expr.mul]: expr.md#expr.mul
[expr.new]: expr.md#expr.new
[expr.sizeof]: expr.md#expr.sizeof
[headers]: library.md#headers
[input.output]: input.md#input.output
[ios.base]: input.md#ios.base
[ios::failure]: input.md#ios::failure
[iostate.flags]: input.md#iostate.flags
[istream::sentry]: input.md#istream::sentry
[language.support]: language.md#language.support
[lex]: lex.md#lex
[lex.ccon]: lex.md#lex.ccon
[lex.icon]: lex.md#lex.icon
[lex.key]: lex.md#lex.key
[lex.ppnumber]: lex.md#lex.ppnumber
[lex.pptoken]: lex.md#lex.pptoken
[lex.string]: lex.md#lex.string
[library]: library.md#library
[logical.operations]: utilities.md#logical.operations
[namespace.posix]: library.md#namespace.posix
[negators]: utilities.md#negators
[new.delete.single]: language.md#new.delete.single
[numerics]: numerics.md#numerics
[ostream::sentry]: input.md#ostream::sentry
[refwrap]: utilities.md#refwrap
[res.on.macro.definitions]: library.md#res.on.macro.definitions
[sequence.reqmts]: containers.md#sequence.reqmts
[special]: special.md#special
[stmt.goto]: stmt.md#stmt.goto
[stmt.return]: stmt.md#stmt.return
[stmt.stmt]: stmt.md#stmt.stmt
[stmt.switch]: stmt.md#stmt.switch
[string.classes]: strings.md#string.classes
[string.require]: strings.md#string.require
[strings]: strings.md#strings
[support.runtime]: language.md#support.runtime
[support.start.term]: language.md#support.start.term
[support.types]: language.md#support.types
[swappable.requirements]: library.md#swappable.requirements
[tab:diff.standard.functions]: #tab:diff.standard.functions
[tab:diff.standard.macros]: #tab:diff.standard.macros
[tab:diff.standard.structs]: #tab:diff.standard.structs
[tab:diff.standard.types]: #tab:diff.standard.types
[tab:diff.standard.values]: #tab:diff.standard.values
[tab:keywords]: #tab:keywords
[temp]: temp.md#temp
[temp.arg]: temp.md#temp.arg
[temp.dep.candidate]: temp.md#temp.dep.candidate
[temp.param]: temp.md#temp.param
[thread]: thread.md#thread
[util.dynamic.safety]: utilities.md#util.dynamic.safety
[utilities]: utilities.md#utilities
