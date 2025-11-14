## C++ and ISO C++17 <a id="diff.cpp17">[[diff.cpp17]]</a>

This subclause lists the differences between C++ and ISO C++17 (ISO/IEC
14882:2017, *Programming Languages — C++*), by the chapters of this
document.

###  [[lex]]: lexical conventions <a id="diff.cpp17.lex">[[diff.cpp17.lex]]</a>

**Change:** New identifiers with special meaning. **Rationale:**
Required for new features. **Effect on original feature:** Logical lines
beginning with `module` or `import` may be interpreted differently in
this International Standard.

[*Example 1*:

``` cpp
class module {};
module m1;          // was variable declaration; now module-declaration
module *m2;         // variable declaration

class import {};
import j1;          // was variable declaration; now import-declaration
::import j2;        // variable declaration
```

— *end example*]

**Change:** *header-name* tokens are formed in more contexts.
**Rationale:** Required for new features. **Effect on original
feature:** When the identifier `import` is followed by a `<` character,
a *header-name* token may be formed.

[*Example 2*:

``` cpp
template<typename> class import {};
import<int> f();                // ill-formed; previously well-formed
::import<int> g();              // OK
```

— *end example*]

**Change:** New keywords. **Rationale:** Required for new features.

- The `char8_t` keyword is added to differentiate the types of ordinary
  and UTF-8 literals [[lex.string]].
- The `concept` keyword is added to enable the definition of concepts
  [[temp.concept]].
- The `consteval` keyword is added to declare immediate functions
  [[dcl.constexpr]].
- The `constinit` keyword is added to prevent unintended dynamic
  initialization [[dcl.constinit]].
- The `co_await`, `co_yield`, and `co_return` keywords are added to
  enable the definition of coroutines [[dcl.fct.def.coroutine]].
- The `requires` keyword is added to introduce constraints through a
  *requires-clause* [[temp.pre]] or a *requires-expression*
  [[expr.prim.req]].

Valid C++17 code using `char8_t`, `concept`, `consteval`, `constinit`,
`co_await`, `co_yield`, `co_return`, or `requires` as an identifier is
not valid in this International Standard.

**Change:** New operator `<=>`. **Rationale:** Necessary for new
functionality. **Effect on original feature:** Valid C++17 code that
contains a `<=` token immediately followed by a `>` token may be
ill-formed or have different semantics in this International Standard:

``` cpp
namespace N {
  struct X {};
  bool operator<=(X, X);
  template<bool(X, X)> struct Y {};
  Y<operator<=> y;              // ill-formed; previously well-formed
}
```

**Change:** Type of UTF-8 string and character literals. **Rationale:**
Required for new features. The changed types enable function
overloading, template specialization, and type deduction to distinguish
ordinary and UTF-8 string and character literals. **Effect on original
feature:** Valid C++17 code that depends on UTF-8 string literals having
type “array of `const char`” and UTF-8 character literals having type
“`char`” is not valid in this International Standard.

``` cpp
const auto *u8s = u8"text";     // u8s previously deduced as const char*; now deduced as const char8_t*
const char *ps = u8s;           // ill-formed; previously well-formed

auto u8c = u8'c';               // u8c previously deduced as char; now deduced as char8_t
char *pc = &u8c;                // ill-formed; previously well-formed

std::string s = u8"text";       // ill-formed; previously well-formed

void f(const char *s);
f(u8"text");                    // ill-formed; previously well-formed

template<typename> struct ct;
template<> struct ct<char> {
  using type = char;
};
ct<decltype(u8'c')>::type x;    // ill-formed; previously well-formed.
```

###  [[basic]]: basics <a id="diff.cpp17.basic">[[diff.cpp17.basic]]</a>

**Change:** A pseudo-destructor call ends the lifetime of the object to
which it is applied. **Rationale:** Increase consistency of the language
model. **Effect on original feature:** Valid ISO C++17 code may be
ill-formed or have undefined behavior in this International Standard.

[*Example 1*:

``` cpp
int f() {
  int a = 123;
  using T = int;
  a.~T();
  return a;         // undefined behavior; previously returned 123
}
```

— *end example*]

**Change:** Except for the initial release operation, a release sequence
consists solely of atomic read-modify-write operations. **Rationale:**
Removal of rarely used and confusing feature. **Effect on original
feature:** If a `memory_order_release` atomic store is followed by a
`memory_order_relaxed` store to the same variable by the same thread,
then reading the latter value with a `memory_order_acquire` load no
longer provides any “happens before” guarantees, even in the absence of
intervening stores by another thread.

###  [[expr]]: expressions <a id="diff.cpp17.expr">[[diff.cpp17.expr]]</a>

**Change:** Implicit lambda capture may capture additional entities.
**Rationale:** Rule simplification, necessary to resolve interactions
with constexpr if. **Effect on original feature:** Lambdas with a
*capture-default* may capture local entities that were not captured in
C++17 if those entities are only referenced in contexts that do not
result in an odr-use.

###  [[dcl.dcl]]: declarations <a id="diff.cpp17.dcl.dcl">[[diff.cpp17.dcl.dcl]]</a>

**Change:** Unnamed classes with a typedef name for linkage purposes can
contain only C-compatible constructs. **Rationale:** Necessary for
implementability. **Effect on original feature:** Valid C++17 code may
be ill-formed in this International Standard.

``` cpp
typedef struct {
  void f() {}           // ill-formed; previously well-formed
} S;
```

**Change:** A function cannot have different default arguments in
different translation units. **Rationale:** Required for modules
support. **Effect on original feature:** Valid C++17 code may be
ill-formed in this International Standard, with no diagnostic required.

``` cpp
// Translation unit 1
int f(int a = 42);
int g() { return f(); }

// Translation unit 2
int f(int a = 76) { return a; }         // ill-formed, no diagnostic required; previously well-formed
int g();
int main() { return g(); }              // used to return 42
```

**Change:** A class that has user-declared constructors is never an
aggregate. **Rationale:** Remove potentially error-prone aggregate
initialization which may apply notwithstanding the declared constructors
of a class. **Effect on original feature:** Valid C++17 code that
aggregate-initializes a type with a user-declared constructor may be
ill-formed or have different semantics in this International Standard.

``` cpp
struct A {              // not an aggregate; previously an aggregate
  A() = delete;
};

struct B {              // not an aggregate; previously an aggregate
  B() = default;
  int i = 0;
};

struct C {              // not an aggregate; previously an aggregate
  C(C&&) = default;
  int a, b;
};

A a{};                  // ill-formed; previously well-formed
B b = {1};              // ill-formed; previously well-formed
auto* c = new C{2, 3};  // ill-formed; previously well-formed

struct Y;

struct X {
  operator Y();
};

struct Y {              // not an aggregate; previously an aggregate
  Y(const Y&) = default;
  X x;
};

Y y{X{}};               // copy constructor call; previously aggregate-initialization
```

**Change:** Boolean conversion from a pointer or pointer-to-member type
is now a narrowing conversion. **Rationale:** Catches bugs. **Effect on
original feature:** Valid C++17 code may fail to compile in this
International Standard. For example:

``` cpp
bool y[] = { "bc" };    // ill-formed; previously well-formed
```

###  [[class]]: classes <a id="diff.cpp17.class">[[diff.cpp17.class]]</a>

**Change:** The class name can no longer be used parenthesized
immediately after an `explicit` *decl-specifier* in a constructor
declaration. The *conversion-function-id* can no longer be used
parenthesized immediately after an `explicit` *decl-specifier* in a
conversion function declaration. **Rationale:** Necessary for new
functionality. **Effect on original feature:** Valid C++17 code may fail
to compile in this International Standard. For example:

``` cpp
struct S {
  explicit (S)(const S&);       // ill-formed; previously well-formed
  explicit (operator int)();    // ill-formed; previously well-formed
  explicit(true) (S)(int);      // OK
};
```

**Change:** A *simple-template-id* is no longer valid as the
*declarator-id* of a constructor or destructor. **Rationale:** Remove
potentially error-prone option for redundancy. **Effect on original
feature:** Valid C++17 code may fail to compile in this International
Standard. For example:

``` cpp
template<class T>
struct A {
  A<T>();           // error: simple-template-id not allowed for constructor
  A(int);           // OK, injected-class-name used
  ~A<T>();          // error: simple-template-id not allowed for destructor
};
```

**Change:** A function returning an implicitly movable entity may invoke
a constructor taking an rvalue reference to a type different from that
of the returned expression. Function and catch-clause parameters can be
thrown using move constructors. **Rationale:** Side effect of making it
easier to write more efficient code that takes advantage of moves.
**Effect on original feature:** Valid C++17 code may fail to compile or
have different semantics in this International Standard. For example:

``` cpp
struct base {
  base();
  base(base const &);
private:
  base(base &&);
};

struct derived : base {};

base f(base b) {
  throw b;                      // error: base(base &&) is private
  derived d;
  return d;                     // error: base(base &&) is private
}

struct S {
  S(const char *s) : m(s) { }
  S(const S&) = default;
  S(S&& other) : m(other.m) { other.m = nullptr; }
  const char * m;
};

S consume(S&& s) { return s; }

void g() {
  S s("text");
  consume(static_cast<S&&>(s));
  char c = *s.m;                // undefined behavior; previously ok
}
```

###  [[over]]: overloading <a id="diff.cpp17.over">[[diff.cpp17.over]]</a>

**Change:** Equality and inequality expressions can now find reversed
and rewritten candidates. **Rationale:** Improve consistency of equality
with three-way comparison and make it easier to write the full
complement of equality operations. **Effect on original feature:**
Equality and inequality expressions between two objects of different
types, where one is convertible to the other, could invoke a different
operator. Equality and inequality expressions between two objects of the
same type could become ambiguous.

``` cpp
struct A {
  operator int() const;
};

bool operator==(A, int);        // #1
// #2 is built-in candidate: bool operator==(int, int);
// #3 is built-in candidate: bool operator!=(int, int);

int check(A x, A y) {
  return (x == y) +             // ill-formed; previously well-formed
    (10 == x) +                 // calls #1, previously selected #2
    (10 != x);                  // calls #1, previously selected #3
}
```

###  [[temp]]: templates <a id="diff.cpp17.temp">[[diff.cpp17.temp]]</a>

**Change:** An *unqualified-id* that is followed by a `<` and for which
name lookup finds nothing or finds a function will be treated as a
*template-name* in order to potentially cause argument dependent lookup
to be performed. **Rationale:** It was problematic to call a function
template with an explicit template argument list via argument dependent
lookup because of the need to have a template with the same name visible
via normal lookup. **Effect on original feature:** Previously valid code
that uses a function name as the left operand of a `<` operator would
become ill-formed.

``` cpp
struct A {};
bool operator<(void (*fp)(), A);
void f() {}
int main() {
  A a;
  f < a;    // ill-formed; previously well-formed
  (f) < a;  // still well formed
}
```

###  [[except]]: exception handling <a id="diff.cpp17.except">[[diff.cpp17.except]]</a>

**Change:** Remove `throw()` exception specification. **Rationale:**
Removal of obsolete feature that has been replaced by `noexcept`.
**Effect on original feature:** A valid C++17 function declaration,
member function declaration, function pointer declaration, or function
reference declaration that uses `throw()` for its exception
specification will be rejected as ill-formed in this International
Standard. It should simply be replaced with `noexcept` for no change of
meaning since C++17.

[*Note 1*: There is no way to write a function declaration that is
non-throwing in this International Standard and is also non-throwing in
C++03 except by using the preprocessor to generate a different token
sequence in each case. — *end note*]

###  [[library]]: library introduction <a id="diff.cpp17.library">[[diff.cpp17.library]]</a>

**Change:** New headers. **Rationale:** New functionality. **Effect on
original feature:** The following C++ headers are new: `<barrier>`,
`<bit>`, `<charconv>`, `<compare>`, `<concepts>`, `<coroutine>`,
`<format>`, `<latch>`, `<numbers>`, `<ranges>`, `<semaphore>`,
`<source_location>`, `<span>`, `<stop_token>`, `<syncstream>`, and
`<version>`. Valid C++17 code that `#include`s headers with these names
may be invalid in this International Standard.

**Change:** Remove vacuous C++ header files. **Rationale:** The empty
headers implied a false requirement to achieve C compatibility with the
C++ headers. **Effect on original feature:** A valid C++17 program that
`#include`s any of the following headers may fail to compile: , , , ,
and . To retain the same behavior:

- a `#include` of can be replaced by a `#include` of `<complex>`,
- a `#include` of can be replaced by a `#include` of `<cmath>` and a
  `#include` of `<complex>`, and
- a `#include` of , , or can simply be removed.

###  [[containers]]: containers library <a id="diff.cpp17.containers">[[diff.cpp17.containers]]</a>

**Change:** Return types of `remove`, `remove_if`, and `unique` changed
from `void` to `container::size_type`. **Rationale:** Improve efficiency
and convenience of finding number of removed elements. **Effect on
original feature:** Code that depends on the return types might have
different semantics in this International Standard. Translation units
compiled against this version of C++ may be incompatible with
translation units compiled against C++17, either failing to link or
having undefined behavior.

###  [[iterators]]: iterators library <a id="diff.cpp17.iterators">[[diff.cpp17.iterators]]</a>

**Change:** The specialization of `iterator_traits` for `void*` and for
function pointer types no longer contains any nested typedefs.
**Rationale:** Corrects an issue misidentifying pointer types that are
not incrementable as iterator types. **Effect on original feature:** A
valid C++17 program that relies on the presence of the typedefs may fail
to compile, or have different behavior.

###  [[algorithms]]: algorithms library <a id="diff.cpp17.alg.reqs">[[diff.cpp17.alg.reqs]]</a>

**Change:** The number and order of deducible template parameters for
algorithm declarations is now unspecified, instead of being as-declared.
**Rationale:** Increase implementor freedom and allow some function
templates to be implemented as function objects with templated call
operators. **Effect on original feature:** A valid C++17 program that
passes explicit template arguments to algorithms not explicitly
specified to allow such in this version of C++ may fail to compile or
have undefined behavior.

###  [[input.output]]: input/output library <a id="diff.cpp17.input.output">[[diff.cpp17.input.output]]</a>

**Change:** Character array extraction only takes array types.
**Rationale:** Increase safety via preventing buffer overflow at compile
time. **Effect on original feature:** Valid C++17 code may fail to
compile in this International Standard:

``` cpp
auto p = new char[100];
char q[100];
std::cin >> std::setw(20) >> p;         // ill-formed; previously well-formed
std::cin >> std::setw(20) >> q;         // OK
```

**Change:** Overload resolution for ostream inserters used with UTF-8
literals. **Rationale:** Required for new features. **Effect on original
feature:** Valid C++17 code that passes UTF-8 literals to
`basic_ostream<char, ...>::operator<<` or
`basic_ostream<wchar_t, ...>::operator<<` is now ill-formed.

``` cpp
std::cout << u8"text";          // previously called operator<<(const char*) and printed a string;
                                // now ill-formed
std::cout << u8'X';             // previously called operator<<(char) and printed a character;
                                // now ill-formed
```

**Change:** Overload resolution for ostream inserters used with
`wchar_t`, `char16_t`, or `char32_t` types. **Rationale:** Removal of
surprising behavior. **Effect on original feature:** Valid C++17 code
that passes `wchar_t`, `char16_t`, or `char32_t` characters or strings
to `basic_ostream<char, ...>::operator<<` or that passes `char16_t` or
`char32_t` characters or strings to
`basic_ostream<wchar_t, ...>::operator<<` is now ill-formed.

``` cpp
std::cout << u"text";           // previously formatted the string as a pointer value;
                                // now ill-formed
std::cout << u'X';              // previously formatted the character as an integer value;
                                // now ill-formed
```

**Change:** Return type of filesystem path format observer member
functions. **Rationale:** Required for new features. **Effect on
original feature:** Valid C++17 code that depends on the `u8string()`
and `generic_u8string()` member functions of `std::filesystem::path`
returning `std::string` is not valid in this International Standard.

``` cpp
std::filesystem::path p;
std::string s1 = p.u8string();          // ill-formed; previously well-formed
std::string s2 = p.generic_u8string();  // ill-formed; previously well-formed
```

###  [[depr]]: compatibility features <a id="diff.cpp17.depr">[[diff.cpp17.depr]]</a>

**Change:** Remove `uncaught_exception`. **Rationale:** The function did
not have a clear specification when multiple exceptions were active, and
has been superseded by `uncaught_exceptions`. **Effect on original
feature:** A valid C++17 program that calls `std::uncaught_exception`
may fail to compile. It might be revised to use
`std::uncaught_exceptions` instead, for clear and portable semantics.

**Change:** Remove support for adaptable function API. **Rationale:**
The deprecated support relied on a limited convention that could not be
extended to support the general case or new language features. It has
been superseded by direct language support with `decltype`, and by the
`std::bind` and `std::not_fn` function templates. **Effect on original
feature:** A valid C++17 program that relies on the presence of
`result_type`, `argument_type`, `first_argument_type`, or
`second_argument_type` in a standard library class may fail to compile.
A valid C++17 program that calls `not1` or `not2`, or uses the class
templates `unary_negate` or `binary_negate`, may fail to compile.

**Change:** Remove redundant members from `std::allocator`.
**Rationale:** `std::allocator` was overspecified, encouraging direct
usage in user containers rather than relying on `std::allocator_traits`,
leading to poor containers. **Effect on original feature:** A valid
C++17 program that directly makes use of the `pointer`, `const_pointer`,
`reference`, `const_reference`, `rebind`, `address`, `construct`,
`destroy`, or `max_size` members of `std::allocator`, or that directly
calls `allocate` with an additional hint argument, may fail to compile.

**Change:** Remove `raw_storage_iterator`. **Rationale:** The iterator
encouraged use of algorithms that might throw exceptions, but did not
return the number of elements successfully constructed that might need
to be destroyed in order to avoid leaks. **Effect on original feature:**
A valid C++17 program that uses this iterator class may fail to compile.

**Change:** Remove temporary buffers API. **Rationale:** The temporary
buffer facility was intended to provide an efficient optimization for
small memory requests, but there is little evidence this was achieved in
practice, while requiring the user to provide their own exception-safe
wrappers to guard use of the facility in many cases. **Effect on
original feature:** A valid C++17 program that calls
`get_temporary_buffer` or `return_temporary_buffer` may fail to compile.

**Change:** Remove `shared_ptr::unique`. **Rationale:** The result of a
call to this member function is not reliable in the presence of multiple
threads and weak pointers. The member function `use_count` is similarly
unreliable, but has a clearer contract in such cases, and remains
available for well defined use in single-threaded cases. **Effect on
original feature:** A valid C++17 program that calls `unique` on a
`shared_ptr` object may fail to compile.

**Change:** Remove deprecated type traits. **Rationale:** The traits had
unreliable or awkward interfaces. The `is_literal_type` trait provided
no way to detect which subset of constructors and member functions of a
type were declared `constexpr`. The `result_of` trait had a surprising
syntax that could not report the result of a regular function type. It
has been superseded by the `invoke_result` trait. **Effect on original
feature:** A valid C++17 program that relies on the `is_literal_type` or
`result_of` type traits, on the `is_literal_type_v` variable template,
or on the `result_of_t` alias template may fail to compile.

## C++ and ISO C++14 <a id="diff.cpp14">[[diff.cpp14]]</a>

This subclause lists the differences between C++ and ISO C++14 (ISO/IEC
14882:2014, *Programming Languages — C++*), in addition to those listed
above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp14.lex">[[diff.cpp14.lex]]</a>

**Change:** Removal of trigraph support as a required feature.
**Rationale:** Prevents accidental uses of trigraphs in non-raw string
literals and comments. **Effect on original feature:** Valid C++14 code
that uses trigraphs may not be valid or may have different semantics in
this International Standard. Implementations may choose to translate
trigraphs as specified in C++14 if they appear outside of a raw string
literal, as part of the *implementation-defined* mapping from physical
source file characters to the basic source character set.

**Change:** *pp-number* can contain `p` *sign* and `P` *sign*.
**Rationale:** Necessary to enable
*hexadecimal-floating-point-literal*s. **Effect on original feature:**
Valid C++14 code may fail to compile or produce different results in
this International Standard. Specifically, character sequences like
`0p+0` and `0e1_p+0` are three separate tokens each in C++14, but one
single token in this International Standard. For example:

``` cpp
#define F(a) b ## a
int b0p = F(0p+0);  // ill-formed; equivalent to ``int b0p = b0p + 0;'' in C++14{}
```

###  [[expr]]: expressions <a id="diff.cpp14.expr">[[diff.cpp14.expr]]</a>

**Change:** Remove increment operator with `bool` operand.
**Rationale:** Obsolete feature with occasionally surprising semantics.
**Effect on original feature:** A valid C++14 expression utilizing the
increment operator on a `bool` lvalue is ill-formed in this
International Standard. Note that this might occur when the lvalue has a
type given by a template parameter.

**Change:** Dynamic allocation mechanism for over-aligned types.
**Rationale:** Simplify use of over-aligned types. **Effect on original
feature:** In C++14 code that uses a *new-expression* to allocate an
object with an over-aligned class type, where that class has no
allocation functions of its own, `::operator new(std::size_t)` is used
to allocate the memory. In this International Standard,
`::operator new(std::size_t, std::align_val_t)` is used instead.

###  [[dcl.dcl]]: declarations <a id="diff.cpp14.dcl.dcl">[[diff.cpp14.dcl.dcl]]</a>

**Change:** Removal of `register` *storage-class-specifier*.
**Rationale:** Enable repurposing of deprecated keyword in future
revisions of this International Standard. **Effect on original
feature:** A valid C++14 declaration utilizing the `register`
*storage-class-specifier* is ill-formed in this International Standard.
The specifier can simply be removed to retain the original meaning.

**Change:** `auto` deduction from *braced-init-list*. **Rationale:**
More intuitive deduction behavior. **Effect on original feature:** Valid
C++14 code may fail to compile or may change meaning in this
International Standard. For example:

``` cpp
auto x1{1};         // was std::initializer_list<int>, now int
auto x2{1, 2};      // was std::initializer_list<int>, now ill-formed
```

**Change:** Make exception specifications be part of the type system.
**Rationale:** Improve type-safety. **Effect on original feature:**
Valid C++14 code may fail to compile or change meaning in this
International Standard. For example:

``` cpp
void g1() noexcept;
void g2();
template<class T> int f(T *, T *);
int x = f(g1, g2);              // ill-formed; previously well-formed
```

**Change:** Definition of an aggregate is extended to apply to
user-defined types with base classes. **Rationale:** To increase
convenience of aggregate initialization. **Effect on original feature:**
Valid C++14 code may fail to compile or produce different results in
this International Standard; initialization from an empty initializer
list will perform aggregate initialization instead of invoking a default
constructor for the affected types. For example:

``` cpp
struct derived;
struct base {
  friend struct derived;
private:
  base();
};
struct derived : base {};

derived d1{};       // error; the code was well-formed in C++14{}
derived d2;         // still OK
```

###  [[class]]: classes <a id="diff.cpp14.class">[[diff.cpp14.class]]</a>

**Change:** Inheriting a constructor no longer injects a constructor
into the derived class. **Rationale:** Better interaction with other
language features. **Effect on original feature:** Valid C++14 code that
uses inheriting constructors may not be valid or may have different
semantics. A *using-declaration* that names a constructor now makes the
corresponding base class constructors visible to initializations of the
derived class rather than declaring additional derived class
constructors.

``` cpp
struct A {
  template<typename T> A(T, typename T::type = 0);
  A(int);
};
struct B : A {
  using A::A;
  B(int);
};
B b(42L);           // now calls B(int), used to call B<long>(long),
                    // which called A(int) due to substitution failure
                    // in A<long>(long).
```

###  [[temp]]: templates <a id="diff.cpp14.temp">[[diff.cpp14.temp]]</a>

**Change:** Allowance to deduce from the type of a non-type template
argument. **Rationale:** In combination with the ability to declare
non-type template arguments with placeholder types, allows partial
specializations to decompose from the type deduced for the non-type
template argument. **Effect on original feature:** Valid C++14 code may
fail to compile or produce different results in this International
Standard. For example:

``` cpp
template <int N> struct A;
template <typename T, T N> int foo(A<N> *) = delete;
void foo(void *);
void bar(A<0> *p) {
  foo(p);           // ill-formed; previously well-formed
}
```

###  [[except]]: exception handling <a id="diff.cpp14.except">[[diff.cpp14.except]]</a>

**Change:** Remove dynamic exception specifications. **Rationale:**
Dynamic exception specifications were a deprecated feature that was
complex and brittle in use. They interacted badly with the type system,
which became a more significant issue in this International Standard
where (non-dynamic) exception specifications are part of the function
type. **Effect on original feature:** A valid C++14 function
declaration, member function declaration, function pointer declaration,
or function reference declaration, if it has a potentially throwing
dynamic exception specification, will be rejected as ill-formed in this
International Standard. Violating a non-throwing dynamic exception
specification will call `terminate` rather than `unexpected` and might
not perform stack unwinding prior to such a call.

###  [[library]]: library introduction <a id="diff.cpp14.library">[[diff.cpp14.library]]</a>

**Change:** New headers. **Rationale:** New functionality. **Effect on
original feature:** The following C++ headers are new: `<any>`,
`<charconv>`, `<execution>`, `<filesystem>`, `<memory_resource>`,
`<optional>`,  
`<string_view>`, and `<variant>`. Valid C++14 code that `#include`s
headers with these names may be invalid in this International Standard.

**Change:** New reserved namespaces. **Rationale:** Reserve namespaces
for future revisions of the standard library that might otherwise be
incompatible with existing programs. **Effect on original feature:** The
global namespaces `std` followed by an arbitrary sequence of *digit*s
[[lex.name]] are reserved for future standardization. Valid C++14 code
that uses such a top-level namespace, e.g., `std2`, may be invalid in
this International Standard.

###  [[utilities]]: general utilities library <a id="diff.cpp14.utilities">[[diff.cpp14.utilities]]</a>

**Change:** Constructors taking allocators removed. **Rationale:** No
implementation consensus. **Effect on original feature:** Valid C++14
code may fail to compile or may change meaning in this International
Standard. Specifically, constructing a `std::function` with an allocator
is ill-formed and uses-allocator construction will not pass an allocator
to `std::function` constructors in this International Standard.

**Change:** Different constraint on conversions from `unique_ptr`.
**Rationale:** Adding array support to `shared_ptr`, via the syntax
`shared_ptr<T[]>` and `shared_ptr<T[N]>`. **Effect on original
feature:** Valid C++14 code may fail to compile or may change meaning in
this International Standard. For example:

``` cpp
#include <memory>
std::unique_ptr<int[]> arr(new int[1]);
std::shared_ptr<int> ptr(std::move(arr));   // error: int(*)[] is not compatible with int*
```

###  [[strings]]: strings library <a id="diff.cpp14.string">[[diff.cpp14.string]]</a>

**Change:** Non-const `.data()` member added. **Rationale:** The lack of
a non-const `.data()` differed from the similar member of `std::vector`.
This change regularizes behavior for this International Standard.
**Effect on original feature:** Overloaded functions which have
differing code paths for `char*` and `const char*` arguments will
execute differently when called with a non-const string’s `.data()`
member in this International Standard.

``` cpp
int f(char *) = delete;
int f(const char *);
string s;
int x = f(s.data());            // ill-formed; previously well-formed
```

###  [[containers]]: containers library <a id="diff.cpp14.containers">[[diff.cpp14.containers]]</a>

**Change:** Requirements change: **Rationale:** Increase portability,
clarification of associative container requirements. **Effect on
original feature:** Valid C++14 code that attempts to use associative
containers having a comparison object with non-const function call
operator may fail to compile in this International Standard:

``` cpp
#include <set>

struct compare
{
  bool operator()(int a, int b)
  {
    return a < b;
  }
};

int main() {
  const std::set<int, compare> s;
  s.find(0);
}
```

###  [[depr]]: compatibility features <a id="diff.cpp14.depr">[[diff.cpp14.depr]]</a>

**Change:** The class templates `auto_ptr`, `unary_function`, and
`binary_function`, the function templates `random_shuffle`, and the
function templates (and their return types) `ptr_fun`, `mem_fun`,
`mem_fun_ref`, `bind1st`, and `bind2nd` are not defined. **Rationale:**
Superseded by new features. **Effect on original feature:** Valid C++14
code that uses these class templates and function templates may fail to
compile in this International Standard.

**Change:** Remove old iostreams members \[depr.ios.members\].
**Rationale:** Redundant feature for compatibility with pre-standard
code has served its time. **Effect on original feature:** A valid C++14
program using these identifiers may be ill-formed in this International
Standard.

## C++ and ISO C++11 <a id="diff.cpp11">[[diff.cpp11]]</a>

This subclause lists the differences between C++ and ISO C++11 (ISO/IEC
14882:2011, *Programming Languages — C++*), in addition to those listed
above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp11.lex">[[diff.cpp11.lex]]</a>

**Change:** *pp-number* can contain one or more single quotes.
**Rationale:** Necessary to enable single quotes as digit separators.
**Effect on original feature:** Valid C++11 code may fail to compile or
may change meaning in this International Standard. For example, the
following code is valid both in C++11 and in this International
Standard, but the macro invocation produces different outcomes because
the single quotes delimit a *character-literal* in C++11, whereas they
are digit separators in this International Standard:

``` cpp
#define M(x, ...) __VA_ARGS__
int x[2] = { M(1'2,3'4, 5) };
// int x[2] = { 5 \ \ \ \ \ } --- C++11{}
// int x[2] = { 3'4, 5 } --- this International Standard
```

###  [[basic]]: basics <a id="diff.cpp11.basic">[[diff.cpp11.basic]]</a>

**Change:** New usual (non-placement) deallocator. **Rationale:**
Required for sized deallocation. **Effect on original feature:** Valid
C++11 code could declare a global placement allocation function and
deallocation function as follows:

``` cpp
void* operator new(std::size_t, std::size_t);
void operator delete(void*, std::size_t) noexcept;
```

In this International Standard, however, the declaration of
`operator delete` might match a predefined usual (non-placement)
`operator delete` [[basic.stc.dynamic]]. If so, the program is
ill-formed, as it was for class member allocation functions and
deallocation functions [[expr.new]].

###  [[expr]]: expressions <a id="diff.cpp11.expr">[[diff.cpp11.expr]]</a>

**Change:** A conditional expression with a throw expression as its
second or third operand keeps the type and value category of the other
operand. **Rationale:** Formerly mandated conversions (lvalue-to-rvalue
[[conv.lval]], array-to-pointer [[conv.array]], and function-to-pointer
[[conv.func]] standard conversions), especially the creation of the
temporary due to lvalue-to-rvalue conversion, were considered gratuitous
and surprising. **Effect on original feature:** Valid C++11 code that
relies on the conversions may behave differently in this International
Standard:

``` cpp
struct S {
  int x = 1;
  void mf() { x = 2; }
};
int f(bool cond) {
  S s;
  (cond ? s : throw 0).mf();
  return s.x;
}
```

In C++11, `f(true)` returns `1`. In this International Standard, it
returns `2`.

``` cpp
sizeof(true ? "" : throw 0)
```

In C++11, the expression yields `sizeof(const char*)`. In this
International Standard, it yields `sizeof(const char[1])`.

###  [[dcl.dcl]]: declarations <a id="diff.cpp11.dcl.dcl">[[diff.cpp11.dcl.dcl]]</a>

**Change:** `constexpr` non-static member functions are not implicitly
`const` member functions. **Rationale:** Necessary to allow `constexpr`
member functions to mutate the object. **Effect on original feature:**
Valid C++11 code may fail to compile in this International Standard. For
example, the following code is valid in C++11 but invalid in this
International Standard because it declares the same member function
twice with different return types:

``` cpp
struct S {
  constexpr const int &f();
  int &f();
};
```

**Change:** Classes with default member initializers can be aggregates.
**Rationale:** Necessary to allow default member initializers to be used
by aggregate initialization. **Effect on original feature:** Valid C++11
code may fail to compile or may change meaning in this International
Standard. For example:

``` cpp
struct S {          // Aggregate in C++14{} onwards.
  int m = 1;
};
struct X {
  operator int();
  operator S();
};
X a{};
S b{a};             // uses copy constructor in C++11{},
                    // performs aggregate initialization in this International Standard
```

###  [[library]]: library introduction <a id="diff.cpp11.library">[[diff.cpp11.library]]</a>

**Change:** New header. **Rationale:** New functionality. **Effect on
original feature:** The C++ header `<shared_mutex>` is new. Valid C++11
code that `#include`s a header with that name may be invalid in this
International Standard.

###  [[input.output]]: input/output library <a id="diff.cpp11.input.output">[[diff.cpp11.input.output]]</a>

**Change:** `gets` is not defined. **Rationale:** Use of `gets` is
considered dangerous. **Effect on original feature:** Valid C++11 code
that uses the `gets` function may fail to compile in this International
Standard.

## C++ and ISO C++03 <a id="diff.cpp03">[[diff.cpp03]]</a>

This subclause lists the differences between C++ and ISO C++03 (ISO/IEC
14882:2003, *Programming Languages — C++*), in addition to those listed
above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp03.lex">[[diff.cpp03.lex]]</a>

**Change:** New kinds of *string-literal*s. **Rationale:** Required for
new features. **Effect on original feature:** Valid C++03 code may fail
to compile or produce different results in this International Standard.
Specifically, macros named `R`, `u8`, `u8R`, `u`, `uR`, `U`, `UR`, or
`LR` will not be expanded when adjacent to a *string-literal* but will
be interpreted as part of the *string-literal*. For example:

``` cpp
#define u8 "abc"
const char* s = u8"def";        // Previously "abcdef", now "def"
```

**Change:** User-defined literal string support. **Rationale:** Required
for new features. **Effect on original feature:** Valid C++03 code may
fail to compile or produce different results in this International
Standard. For example:

``` cpp
#define _x "there"
"hello"_x           // #1
```

Previously, \#1 would have consisted of two separate preprocessing
tokens and the macro `_x` would have been expanded. In this
International Standard, \#1 consists of a single preprocessing token, so
the macro is not expanded.

**Change:** New keywords. **Rationale:** Required for new features.
**Effect on original feature:** Added to [[lex.key]], the following
identifiers are new keywords: `alignas`, `alignof`, `char16_t`,
`char32_t`, `constexpr`, `decltype`, `noexcept`, `nullptr`,
`static_assert`, and `thread_local`. Valid C++03 code using these
identifiers is invalid in this International Standard.

**Change:** Type of integer literals. **Rationale:** C99 compatibility.
**Effect on original feature:** Certain integer literals larger than can
be represented by `long` could change from an unsigned integer type to
`signed long long`.

###  [[expr]]: expressions <a id="diff.cpp03.expr">[[diff.cpp03.expr]]</a>

**Change:** Only literals are integer null pointer constants.
**Rationale:** Removing surprising interactions with templates and
constant expressions. **Effect on original feature:** Valid C++03 code
may fail to compile or produce different results in this International
Standard. For example:

``` cpp
void f(void *);     // #1
void f(...);        // #2
template<int N> void g() {
  f(0*N);           // calls #2; used to call #1
}
```

**Change:** Specify rounding for results of integer `/` and `%`.
**Rationale:** Increase portability, C99 compatibility. **Effect on
original feature:** Valid C++03 code that uses integer division rounds
the result toward 0 or toward negative infinity, whereas this
International Standard always rounds the result toward 0.

**Change:** `&&` is valid in a *type-name*. **Rationale:** Required for
new features. **Effect on original feature:** Valid C++03 code may fail
to compile or produce different results in this International Standard.
For example:

``` cpp
bool b1 = new int && false;             // previously false, now ill-formed
struct S { operator int(); };
bool b2 = &S::operator int && false;    // previously false, now ill-formed
```

###  [[dcl.dcl]]: declarations <a id="diff.cpp03.dcl.dcl">[[diff.cpp03.dcl.dcl]]</a>

**Change:** Remove `auto` as a storage class specifier. **Rationale:**
New feature. **Effect on original feature:** Valid C++03 code that uses
the keyword `auto` as a storage class specifier may be invalid in this
International Standard. In this International Standard, `auto` indicates
that the type of a variable is to be deduced from its initializer
expression.

**Change:** Narrowing restrictions in aggregate initializers.
**Rationale:** Catches bugs. **Effect on original feature:** Valid C++03
code may fail to compile in this International Standard. For example,
the following code is valid in C++03 but invalid in this International
Standard because `double` to `int` is a narrowing conversion:

``` cpp
int x[] = { 2.0 };
```

###  [[class]]: classes <a id="diff.cpp03.class">[[diff.cpp03.class]]</a>

**Change:** Implicitly-declared special member functions are defined as
deleted when the implicit definition would have been ill-formed.
**Rationale:** Improves template argument deduction failure. **Effect on
original feature:** A valid C++03 program that uses one of these special
member functions in a context where the definition is not required
(e.g., in an expression that is not potentially evaluated) becomes
ill-formed.

**Change:** User-declared destructors have an implicit exception
specification. **Rationale:** Clarification of destructor requirements.
**Effect on original feature:** Valid C++03 code may execute differently
in this International Standard. In particular, destructors that throw
exceptions will call `std::terminate` (without calling
`std::unexpected`) if their exception specification is non-throwing.

###  [[temp]]: templates <a id="diff.cpp03.temp">[[diff.cpp03.temp]]</a>

**Change:** Remove `export`. **Rationale:** No implementation consensus.
**Effect on original feature:** A valid C++03 declaration containing
`export` is ill-formed in this International Standard.

**Change:** Remove whitespace requirement for nested closing template
right angle brackets. **Rationale:** Considered a persistent but minor
annoyance. Template aliases representing non-class types would
exacerbate whitespace issues. **Effect on original feature:** Change to
semantics of well-defined expression. A valid C++03 expression
containing a right angle bracket (“`>`”) followed immediately by another
right angle bracket may now be treated as closing two templates. For
example, the following code is valid in C++03 because “`>>`” is a
right-shift operator, but invalid in this International Standard because
“`>>`” closes two templates.

``` cpp
template <class T> struct X { };
template <int N> struct Y { };
X< Y< 1 >> 2 > > x;
```

**Change:** Allow dependent calls of functions with internal linkage.
**Rationale:** Overly constrained, simplify overload resolution rules.
**Effect on original feature:** A valid C++03 program could get a
different result than this International Standard.

###  [[library]]: library introduction <a id="diff.cpp03.library">[[diff.cpp03.library]]</a>

**Affected:** [[library]] – [[thread]] **Change:** New reserved
identifiers. **Rationale:** Required by new features. **Effect on
original feature:** Valid C++03 code that uses any identifiers added to
the C++ standard library by this International Standard may fail to
compile or produce different results in this International Standard. A
comprehensive list of identifiers used by the C++ standard library can
be found in the Index of Library Names in this International Standard.

**Change:** New headers. **Rationale:** New functionality. **Effect on
original feature:** The following C++ headers are new: `<array>`,
`<atomic>`, `<chrono>`, , `<condition_variable>`, `<forward_list>`,
`<future>`, `<initializer_list>`, `<mutex>`, `<random>`, `<ratio>`,
`<regex>`, `<scoped_allocator>`, `<system_error>`, `<thread>`,
`<tuple>`, `<typeindex>`, `<type_traits>`, `<unordered_map>`, and
`<unordered_set>`. In addition the following C compatibility headers are
new: `<cfenv>`, `<cinttypes>`, `<cstdint>`, and `<cuchar>`. Valid C++03
code that `#include`s headers with these names may be invalid in this
International Standard.

**Effect on original feature:** Function `swap` moved to a different
header **Rationale:** Remove dependency on `<algorithm>` for `swap`.
**Effect on original feature:** Valid C++03 code that has been compiled
expecting swap to be in `<algorithm>` may have to instead include
`<utility>`.

**Change:** New reserved namespace. **Rationale:** New functionality.
**Effect on original feature:** The global namespace `posix` is now
reserved for standardization. Valid C++03 code that uses a top-level
namespace `posix` may be invalid in this International Standard.

**Change:** Additional restrictions on macro names. **Rationale:** Avoid
hard to diagnose or non-portable constructs. **Effect on original
feature:** Names of attribute identifiers may not be used as macro
names. Valid C++03 code that defines `override`, `final`,
`carries_dependency`, or `noreturn` as macros is invalid in this
International Standard.

###  [[support]]: language support library <a id="diff.cpp03.language.support">[[diff.cpp03.language.support]]</a>

**Change:** `operator new` may throw exceptions other than
`std::bad_alloc`. **Rationale:** Consistent application of `noexcept`.
**Effect on original feature:** Valid C++03 code that assumes that
global `operator new` only throws `std::bad_alloc` may execute
differently in this International Standard. Valid C++03 code that
replaces the global replaceable `operator new` is ill-formed in this
International Standard, because the exception specification of
`throw(std::bad_alloc)` was removed.

###  [[diagnostics]]: diagnostics library <a id="diff.cpp03.diagnostics">[[diff.cpp03.diagnostics]]</a>

**Change:** Thread-local error numbers. **Rationale:** Support for new
thread facilities. **Effect on original feature:** Valid but
implementation-specific C++03 code that relies on `errno` being the same
across threads may change behavior in this International Standard.

###  [[utilities]]: general utilities library <a id="diff.cpp03.utilities">[[diff.cpp03.utilities]]</a>

**Change:** Minimal support for garbage-collected regions.
**Rationale:** Required by new feature. **Effect on original feature:**
Valid C++03 code, compiled without traceable pointer support, that
interacts with newer C++ code using regions declared reachable may have
different runtime behavior.

**Change:** Standard function object types no longer derived from
`std::unary_function` or `std::binary_function`. **Rationale:**
Superseded by new feature; `unary_function` and `binary_function` are no
longer defined. **Effect on original feature:** Valid C++03 code that
depends on function object types being derived from `unary_function` or
`binary_function` may fail to compile in this International Standard.

###  [[strings]]: strings library <a id="diff.cpp03.strings">[[diff.cpp03.strings]]</a>

**Change:** `basic_string` requirements no longer allow
reference-counted strings. **Rationale:** Invalidation is subtly
different with reference-counted strings. This change regularizes
behavior for this International Standard. **Effect on original
feature:** Valid C++03 code may execute differently in this
International Standard.

**Change:** Loosen `basic_string` invalidation rules. **Rationale:**
Allow small-string optimization. **Effect on original feature:** Valid
C++03 code may execute differently in this International Standard. Some
`const` member functions, such as `data` and `c_str`, no longer
invalidate iterators.

###  [[containers]]: containers library <a id="diff.cpp03.containers">[[diff.cpp03.containers]]</a>

**Change:** Complexity of `size()` member functions now constant.
**Rationale:** Lack of specification of complexity of `size()` resulted
in divergent implementations with inconsistent performance
characteristics. **Effect on original feature:** Some container
implementations that conform to C++03 may not conform to the specified
`size()` requirements in this International Standard. Adjusting
containers such as `std::list` to the stricter requirements may require
incompatible changes.

**Change:** Requirements change: relaxation. **Rationale:**
Clarification. **Effect on original feature:** Valid C++03 code that
attempts to meet the specified container requirements may now be
over-specified. Code that attempted to be portable across containers may
need to be adjusted as follows:

- not all containers provide `size()`; use `empty()` instead of
  `size() == 0`;
- not all containers are empty after construction (`array`);
- not all containers have constant complexity for `swap()` (`array`).

**Change:** Requirements change: default constructible. **Rationale:**
Clarification of container requirements. **Effect on original feature:**
Valid C++03 code that attempts to explicitly instantiate a container
using a user-defined type with no default constructor may fail to
compile.

**Change:** Signature changes: from `void` return types. **Rationale:**
Old signature threw away useful information that may be expensive to
recalculate. **Effect on original feature:** The following member
functions have changed:

- `erase(iter)` for `set`, `multiset`, `map`, `multimap`
- `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`
- `insert(pos, num, val)` for `vector`, `deque`, `list`, `forward_list`
- `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`

Valid C++03 code that relies on these functions returning `void` (e.g.,
code that creates a pointer to member function that points to one of
these functions) will fail to compile with this International Standard.

**Change:** Signature changes: from `iterator` to `const_iterator`
parameters. **Rationale:** Overspecification. **Effect on original
feature:** The signatures of the following member functions changed from
taking an `iterator` to taking a `const_iterator`:

- `insert(iter, val)` for `vector`, `deque`, `list`, `set`, `multiset`,
  `map`, `multimap`
- `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`
- `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`
- all forms of `list::splice`
- all forms of `list::merge`

Valid C++03 code that uses these functions may fail to compile with this
International Standard.

**Change:** Signature changes: `resize`. **Rationale:** Performance,
compatibility with move semantics. **Effect on original feature:** For
`vector`, `deque`, and `list` the fill value passed to `resize` is now
passed by reference instead of by value, and an additional overload of
`resize` has been added. Valid C++03 code that uses this function may
fail to compile with this International Standard.

###  [[algorithms]]: algorithms library <a id="diff.cpp03.algorithms">[[diff.cpp03.algorithms]]</a>

**Change:** Result state of inputs after application of some algorithms.
**Rationale:** Required by new feature. **Effect on original feature:**
A valid C++03 program may detect that an object with a valid but
unspecified state has a different valid but unspecified state with this
International Standard. For example, `std::remove` and `std::remove_if`
may leave the tail of the input sequence with a different set of values
than previously.

###  [[numerics]]: numerics library <a id="diff.cpp03.numerics">[[diff.cpp03.numerics]]</a>

**Change:** Specified representation of complex numbers. **Rationale:**
Compatibility with C99. **Effect on original feature:** Valid C++03 code
that uses implementation-specific knowledge about the binary
representation of the required template specializations of
`std::complex` may not be compatible with this International Standard.

###  [[input.output]]: input/output library <a id="diff.cpp03.input.output">[[diff.cpp03.input.output]]</a>

**Change:** Specify use of `explicit` in existing boolean conversion
functions. **Rationale:** Clarify intentions, avoid workarounds.
**Effect on original feature:** Valid C++03 code that relies on implicit
boolean conversions will fail to compile with this International
Standard. Such conversions occur in the following conditions:

- passing a value to a function that takes an argument of type `bool`;
- using `operator==` to compare to `false` or `true`;
- returning a value from a function with a return type of `bool`;
- initializing members of type `bool` via aggregate initialization;
- initializing a `const bool&` which would bind to a temporary object.

**Change:** Change base class of `std::ios_base::failure`.
**Rationale:** More detailed error messages. **Effect on original
feature:** `std::ios_base::failure` is no longer derived directly from
`std::exception`, but is now derived from `std::system_error`, which in
turn is derived from `std::runtime_error`. Valid C++03 code that assumes
that `std::ios_base::failure` is derived directly from `std::exception`
may execute differently in this International Standard.

**Change:** Flag types in `std::ios_base` are now bitmasks with values
defined as constexpr static members. **Rationale:** Required for new
features. **Effect on original feature:** Valid C++03 code that relies
on `std::ios_base` flag types being represented as `std::bitset` or as
an integer type may fail to compile with this International Standard.
For example:

``` cpp
#include <iostream>

int main() {
  int flag = std::ios_base::hex;
  std::cout.setf(flag);         // error: setf does not take argument of type int
}
```

## C++ and ISO C <a id="diff.iso">[[diff.iso]]</a>

This subclause lists the differences between C++ and ISO C, in addition
to those listed above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.lex">[[diff.lex]]</a>

**Change:** New Keywords  
New keywords are added to C++; see [[lex.key]]. **Rationale:** These
keywords were added in order to implement the new semantics of C++.
**Effect on original feature:** Change to semantics of well-defined
feature. Any ISO C programs that used any of these keywords as
identifiers are not valid C++ programs. Syntactic transformation.
Converting one specific program is easy. Converting a large collection
of related programs takes more work. Common.

**Change:** Type of *character-literal* is changed from `int` to `char`.
**Rationale:** This is needed for improved overloaded function argument
type matching. For example:

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

will not work the same as C++ programs. Simple. Programs which depend
upon `sizeof('x')` are probably rare.

**Change:** String literals made const.  
The type of a *string-literal* is changed from “array of `char`” to
“array of `const char`”. The type of a UTF-8 string literal is changed
from “array of `char`” to “array of `const char8_t`”. The type of a
UTF-16 string literal is changed from “array of *some-integer-type*” to
“array of `const char16_t`”. The type of a UTF-32 string literal is
changed from “array of *some-integer-type*” to “array of
`const char32_t`”. The type of a wide string literal is changed from
“array of `wchar_t`” to “array of `const wchar_t`”. **Rationale:** This
avoids calling an inappropriate overloaded function, which might expect
to be able to modify its argument. **Effect on original feature:**
Change to semantics of well-defined feature. Syntactic transformation.
The fix is to add a cast:

``` cpp
char* p = "abc";                // valid in C, invalid in C++{}
void f(char*) {
  char* p = (char*)"abc";       // OK: cast added
  f(p);
  f((char*)"def");              // OK: cast added
}
```

Programs that have a legitimate reason to treat string literal objects
as potentially modifiable memory are probably rare.

###  [[basic]]: basics <a id="diff.basic">[[diff.basic]]</a>

**Change:** C++ does not have “tentative definitions” as in C.  
E.g., at file scope,

``` cpp
int i;
int i;
```

is valid in C, invalid in C++. This makes it impossible to define
mutually referential file-local objects with static storage duration, if
initializers are restricted to the syntactic forms of C. For example,

``` cpp
struct X { int i; struct X* next; };

static struct X a;
static struct X b = { 0, &a };
static struct X a = { 1, &b };
```

**Rationale:** This avoids having different initialization rules for
fundamental types and user-defined types. **Effect on original
feature:** Deletion of semantically well-defined feature. Semantic
transformation. In C++, the initializer for one of a set of
mutually-referential file-local objects with static storage duration
must invoke a function call to achieve the initialization. Seldom.

**Change:** A `struct` is a scope in C++, not in C. **Rationale:** Class
scope is crucial to C++, and a struct is a class. **Effect on original
feature:** Change to semantics of well-defined feature. Semantic
transformation. C programs use `struct` extremely frequently, but the
change is only noticeable when `struct`, enumeration, or enumerator
names are referred to outside the `struct`. The latter is probably rare.

\[also [[dcl.type]]\] **Change:** A name of file scope that is
explicitly declared `const`, and not explicitly declared `extern`, has
internal linkage, while in C it would have external linkage.
**Rationale:** Because const objects may be used as values during
translation in C++, this feature urges programmers to provide an
explicit initializer for each const object. This feature allows the user
to put const objects in source files that are included in more than one
translation unit. **Effect on original feature:** Change to semantics of
well-defined feature. Semantic transformation. Seldom.

**Change:** The `main` function cannot be called recursively and cannot
have its address taken. **Rationale:** The `main` function may require
special actions. **Effect on original feature:** Deletion of
semantically well-defined feature. Trivial: create an intermediary
function such as `mymain(argc, argv)`. Seldom.

**Change:** C allows “compatible types” in several places, C++ does
not.  
For example, otherwise-identical `struct` types with different tag names
are “compatible” in C but are distinctly different types in C++.
**Rationale:** Stricter type checking is essential for C++. **Effect on
original feature:** Deletion of semantically well-defined feature.
Semantic transformation. The “typesafe linkage” mechanism will find
many, but not all, of such problems. Those problems not found by
typesafe linkage will continue to function properly, according to the
“layout compatibility rules” of this document. Common.

###  [[expr]]: expressions <a id="diff.expr">[[diff.expr]]</a>

**Change:** Converting `void*` to a pointer-to-object type requires
casting.

``` cpp
char a[10];
void* b=a;
void foo() {
  char* c=b;
}
```

ISO C will accept this usage of pointer to void being assigned to a
pointer to object type. C++ will not. **Rationale:** C++ tries harder
than C to enforce compile-time type safety. **Effect on original
feature:** Deletion of semantically well-defined feature. Could be
automated. Violations will be diagnosed by the C++ translator. The fix
is to add a cast. For example:

``` cpp
char* c = (char*) b;
```

This is fairly widely used but it is good programming practice to add
the cast when assigning pointer-to-void to pointer-to-object. Some ISO C
translators will give a warning if the cast is not used.

**Change:** Implicit declaration of functions is not allowed.
**Rationale:** The type-safe nature of C++. **Effect on original
feature:** Deletion of semantically well-defined feature. Note: the
original feature was labeled as “obsolescent” in ISO C. Syntactic
transformation. Facilities for producing explicit function declarations
are fairly widespread commercially. Common.

**Change:** Decrement operator is not allowed with `bool` operand.
**Rationale:** Feature with surprising semantics. **Effect on original
feature:** A valid ISO C expression utilizing the decrement operator on
a `bool` lvalue (for instance, via the C typedef in ) is ill-formed in
this International Standard.

**Change:** Types must be defined in declarations, not in expressions.  
In C, a sizeof expression or cast expression may define a new type. For
example,

``` cpp
p = (void*)(struct x {int i;} *)0;
```

defines a new type, struct `x`. **Rationale:** This prohibition helps to
clarify the location of definitions in the source code. **Effect on
original feature:** Deletion of semantically well-defined feature.
Syntactic transformation. Seldom.

**Change:** The result of a conditional expression, an assignment
expression, or a comma expression may be an lvalue. **Rationale:** C++
is an object-oriented language, placing relatively more emphasis on
lvalues. For example, function calls may yield lvalues. **Effect on
original feature:** Change to semantics of well-defined feature. Some C
expressions that implicitly rely on lvalue-to-rvalue conversions will
yield different results. For example,

``` cpp
char arr[100];
sizeof(0, arr)
```

yields `100` in C++ and `sizeof(char*)` in C. Programs must add explicit
casts to the appropriate rvalue. Rare.

###  [[stmt.stmt]]: statements <a id="diff.stat">[[diff.stat]]</a>

**Change:** It is now invalid to jump past a declaration with explicit
or implicit initializer (except across entire block not entered).
**Rationale:** Constructors used in initializers may allocate resources
which need to be de-allocated upon leaving the block. Allowing jump past
initializers would require complicated runtime determination of
allocation. Furthermore, any use of the uninitialized object could be a
disaster. With this simple compile-time rule, C++ assures that if an
initialized variable is in scope, then it has assuredly been
initialized. **Effect on original feature:** Deletion of semantically
well-defined feature. Semantic transformation. Seldom.

**Change:** It is now invalid to return (explicitly or implicitly) from
a function which is declared to return a value without actually
returning a value. **Rationale:** The caller and callee may assume
fairly elaborate return-value mechanisms for the return of class
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

###  [[dcl.dcl]]: declarations <a id="diff.dcl">[[diff.dcl]]</a>

**Change:** In C++, the `static` or `extern` specifiers can only be
applied to names of objects or functions.  
Using these specifiers with type declarations is illegal in C++. In C,
these specifiers are ignored when used on type declarations.

Example:

``` cpp
static struct S {               // valid C, invalid in C++{}
  int i;
};
```

**Rationale:** Storage class specifiers don’t have any meaning when
associated with a type. In C++, class members can be declared with the
`static` storage class specifier. Allowing storage class specifiers on
type declarations could render the code confusing for users. **Effect on
original feature:** Deletion of semantically well-defined feature.
Syntactic transformation. Seldom.

**Change:** In C++, `register` is not a storage class specifier.
**Rationale:** The storage class specifier had no effect in C++.
**Effect on original feature:** Deletion of semantically well-defined
feature. Syntactic transformation. Common.

**Change:** A C++ typedef name must be different from any class type
name declared in the same scope (except if the typedef is a synonym of
the class name with the same name). In C, a typedef name and a struct
tag name declared in the same scope can have the same name (because they
have different name spaces).

Example:

``` cpp
typedef struct name1 { ... } name1;         // valid C and C++{}
struct name { ... };
typedef int name;               // valid C, invalid C++{}
```

**Rationale:** For ease of use, C++ doesn’t require that a type name be
prefixed with the keywords `class`, `struct` or `union` when used in
object declarations or type casts.

Example:

``` cpp
class name { ... };
name i;                         // i has type class name
```

**Effect on original feature:** Deletion of semantically well-defined
feature. Semantic transformation. One of the 2 types has to be renamed.
Seldom.

\[see also [[basic.link]]\] **Change:** Const objects must be
initialized in C++ but can be left uninitialized in C. **Rationale:** A
const object cannot be assigned to so it must be initialized to hold a
useful value. **Effect on original feature:** Deletion of semantically
well-defined feature. Semantic transformation. Seldom.

**Change:** Banning implicit `int`.

In C++ a *decl-specifier-seq* must contain a *type-specifier*, unless it
is followed by a declarator for a constructor, a destructor, or a
conversion function. In the following example, the left-hand column
presents valid C; the right-hand column presents equivalent C++:

``` cpp
void f(const parm);            void f(const int parm);
const n = 3;                   const int n = 3;
main()                         int main()
    ...                      ...
```

**Rationale:** In C++, implicit int creates several opportunities for
ambiguity between expressions involving function-like casts and
declarations. Explicit declaration is increasingly considered to be
proper style. Liaison with WG14 (C) indicated support for (at least)
deprecating implicit int in the next revision of C. **Effect on original
feature:** Deletion of semantically well-defined feature. Syntactic
transformation. Could be automated. Common.

**Change:** The keyword `auto` cannot be used as a storage class
specifier.

``` cpp
void f() {
  auto int x;       // valid C, invalid C++{}
}
```

**Rationale:** Allowing the use of `auto` to deduce the type of a
variable from its initializer results in undesired interpretations of
`auto` as a storage class specifier in certain contexts. **Effect on
original feature:** Deletion of semantically well-defined feature.
Syntactic transformation. Rare.

**Change:** In C++, a function declared with an empty parameter list
takes no arguments. In C, an empty parameter list means that the number
and type of the function arguments are unknown.

Example:

``` cpp
int f();            // means   int f(void) in C++{}
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

\[see [[expr.sizeof]]\] **Change:** In C++, types may not be defined in
return or parameter types. In C, these type definitions are allowed.

Example:

``` cpp
void f( struct S { int a; } arg ) {}    // valid C, invalid C++{}
enum E { A, B, C } f() {}               // valid C, invalid C++{}
```

**Rationale:** When comparing types in different translation units, C++
relies on name equivalence when C relies on structural equivalence.
Regarding parameter types: since the type defined in a parameter list
would be in the scope of the function, the only legal calls in C++ would
be from within the function itself. **Effect on original feature:**
Deletion of semantically well-defined feature. Semantic transformation.
The type definitions must be moved to file scope, or in header files.
Seldom. This style of type definition is seen as poor coding style.

**Change:** In C++, the syntax for function definition excludes the
“old-style” C function. In C, “old-style” syntax is allowed, but
deprecated as “obsolescent”. **Rationale:** Prototypes are essential to
type safety. **Effect on original feature:** Deletion of semantically
well-defined feature. Syntactic transformation. Common in old programs,
but already known to be obsolescent.

**Change:** In C++, designated initialization support is restricted
compared to the corresponding functionality in C. In C++, designators
for non-static data members must be specified in declaration order,
designators for array elements and nested designators are not supported,
and designated and non-designated initializers cannot be mixed in the
same initializer list.

Example:

``` cpp
struct A { int x, y; };
struct B { struct A a; };
struct A a = {.y = 1, .x = 2};  // valid C, invalid C++{}
int arr[3] = {[1] = 5};         // valid C, invalid C++{}
struct B b = {.a.x = 0};        // valid C, invalid C++{}
struct A c = {.x = 1, 2};       // valid C, invalid C++{}
```

**Rationale:** In C++, members are destroyed in reverse construction
order and the elements of an initializer list are evaluated in lexical
order, so field initializers must be specified in order. Array
designators conflict with *lambda-expression* syntax. Nested designators
are seldom used. **Effect on original feature:** Deletion of feature
that is incompatible with C++. Syntactic transformation. Out-of-order
initializers are common. The other features are seldom used.

**Change:** In C++, when initializing an array of character with a
string, the number of characters in the string (including the
terminating `'\0'`) must not exceed the number of elements in the array.
In C, an array can be initialized with a string even if the array is not
large enough to contain the string-terminating `'\0'`.

Example:

``` cpp
char array[4] = "abcd";         // valid C, invalid C++{}
```

**Rationale:** When these non-terminated arrays are manipulated by
standard string functions, there is potential for major catastrophe.
**Effect on original feature:** Deletion of semantically well-defined
feature. Semantic transformation. The arrays must be declared one
element bigger to contain the string terminating `'\0'`. Seldom. This
style of array initialization is seen as poor coding style.

**Change:** C++ objects of enumeration type can only be assigned values
of the same enumeration type. In C, objects of enumeration type can be
assigned values of any integral type.

Example:

``` cpp
enum color { red, blue, green };
enum color c = 1;               // valid C, invalid C++{}
```

**Rationale:** The type-safe nature of C++. **Effect on original
feature:** Deletion of semantically well-defined feature. Syntactic
transformation. (The type error produced by the assignment can be
automatically corrected by applying an explicit cast.) Common.

**Change:** In C++, the type of an enumerator is its enumeration. In C,
the type of an enumerator is `int`.

Example:

``` cpp
enum e { A };
sizeof(A) == sizeof(int)        // in C
sizeof(A) == sizeof(e)          // in C++{}
/* and sizeof(int) is not necessarily equal to sizeof(e) */
```

**Rationale:** In C++, an enumeration is a distinct type. **Effect on
original feature:** Change to semantics of well-defined feature.
Semantic transformation. Seldom. The only time this affects existing C
code is when the size of an enumerator is taken. Taking the size of an
enumerator is not a common C coding practice.

###  [[class]]: classes <a id="diff.class">[[diff.class]]</a>

\[see also [[dcl.typedef]]\] **Change:** In C++, a class declaration
introduces the class name into the scope where it is declared and hides
any object, function or other declaration of that name in an enclosing
scope. In C, an inner scope declaration of a struct tag name never hides
the name of an object or function in an outer scope.

Example:

``` cpp
int x[99];
void f() {
  struct x { int a; };
  sizeof(x);  /* size of the array in C */
  /* size of the struct in \textit{\textrm{C++{}}} */
}
```

**Rationale:** This is one of the few incompatibilities between C and
C++ that can be attributed to the new C++ name space definition where a
name can be declared as a type and as a non-type in a single scope
causing the non-type name to hide the type name and requiring that the
keywords `class`, `struct`, `union` or `enum` be used to refer to the
type name. This new name space definition provides important notational
conveniences to C++ programmers and helps making the use of the
user-defined types as similar as possible to the use of fundamental
types. The advantages of the new name space definition were judged to
outweigh by far the incompatibility with C described above. **Effect on
original feature:** Change to semantics of well-defined feature.
Semantic transformation. If the hidden name that needs to be accessed is
at global scope, the `::` C++ operator can be used. If the hidden name
is at block scope, either the type or the struct tag has to be renamed.
Seldom.

**Change:** Copying volatile objects.

The implicitly-declared copy constructor and implicitly-declared copy
assignment operator cannot make a copy of a volatile lvalue. For
example, the following is valid in ISO C:

``` cpp
struct X { int i; };
volatile struct X x1 = {0};
struct X x2 = x1;               // invalid C++{}
struct X x3;
x3 = x1;                        // also invalid C++{}
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
assignment must be provided. If non-volatile semantics are required, an
explicit `const_cast` can be used. Seldom.

**Change:** Bit-fields of type plain `int` are signed. **Rationale:**
Leaving the choice of signedness to implementations could lead to
inconsistent definitions of template specializations. For consistency,
the implementation freedom was eliminated for non-dependent types, too.
**Effect on original feature:** The choice is implementation-defined in
C, but not so in C++. Syntactic transformation. Seldom.

**Change:** In C++, the name of a nested class is local to its enclosing
class. In C the name of the nested class belongs to the same scope as
the name of the outermost enclosing class.

Example:

``` cpp
struct X {
  struct Y { ... } y;
};
struct Y yy;                    // valid C, invalid C++{}
```

**Rationale:** C++ classes have member functions which require that
classes establish scopes. The C rule would leave classes as an
incomplete scope mechanism which would prevent C++ programmers from
maintaining locality within a class. A coherent set of scope rules for
C++ based on the C rule would be very complicated and C++ programmers
would be unable to predict reliably the meanings of nontrivial examples
involving nested or local functions. **Effect on original feature:**
Change to semantics of well-defined feature. Semantic transformation. To
make the struct type name visible in the scope of the enclosing struct,
the struct tag could be declared in the scope of the enclosing struct,
before the enclosing struct is defined. Example:

``` cpp
struct Y;                       // struct Y and struct X are at the same scope
struct X {
  struct Y { ... } y;
};
```

All the definitions of C struct types enclosed in other struct
definitions and accessed outside the scope of the enclosing struct could
be exported to the scope of the enclosing struct. Note: this is a
consequence of the difference in scope rules, which is documented in
[[basic.scope]]. Seldom.

**Change:** In C++, a typedef name may not be redeclared in a class
definition after being used in that definition.

Example:

``` cpp
typedef int I;
struct S {
  I i;
  int I;            // valid C, invalid C++{}
};
```

**Rationale:** When classes become complicated, allowing such a
redefinition after the type has been used can create confusion for C++
programmers as to what the meaning of `I` really is. **Effect on
original feature:** Deletion of semantically well-defined feature.
Semantic transformation. Either the type or the struct member has to be
renamed. Seldom.

###  [[cpp]]: preprocessing directives <a id="diff.cpp">[[diff.cpp]]</a>

**Change:** Whether `__STDC__` is defined and if so, what its value is,
are *implementation-defined*. **Rationale:** C++ is not identical to ISO
C. Mandating that `__STDC__` be defined would require that translators
make an incorrect claim. Each implementation must choose the behavior
that will be most useful to its marketplace. **Effect on original
feature:** Change to semantics of well-defined feature. Semantic
transformation. Programs and headers that reference `__STDC__` are quite
common.

## C standard library <a id="diff.library">[[diff.library]]</a>

This subclause summarizes the explicit changes in headers, definitions,
declarations, or behavior between the C standard library in the C
standard and the parts of the C++ standard library that were included
from the C standard library.

### Modifications to headers <a id="diff.mods.to.headers">[[diff.mods.to.headers]]</a>

For compatibility with the C standard library, the C++ standard library
provides the C headers enumerated in  [[depr.c.headers]], but their use
is deprecated in C++.

There are no C++ headers for the C standard library’s headers , , and ,
nor are these headers from the C standard library headers themselves
part of C++.

The C headers `<complex.h>` and `<tgmath.h>` do not contain any of the
content from the C standard library and instead merely include other
headers from the C++ standard library.

### Modifications to definitions <a id="diff.mods.to.definitions">[[diff.mods.to.definitions]]</a>

#### Types `char16_t` and `char32_t` <a id="diff.char16">[[diff.char16]]</a>

The types `char16_t` and `char32_t` are distinct types rather than
typedefs to existing integral types. The tokens `char16_t` and
`char32_t` are keywords in this International Standard [[lex.key]]. They
do not appear as macro or type names defined in `<cuchar>`.

#### Type `wchar_t` <a id="diff.wchar.t">[[diff.wchar.t]]</a>

The type `wchar_t` is a distinct type rather than a typedef to an
existing integral type. The token `wchar_t` is a keyword in this
International Standard [[lex.key]]. It does not appear as a macro or
type name defined in any of `<cstddef>`, `<cstdlib>`, or `<cwchar>`.

#### Header `<assert.h>` <a id="diff.header.assert.h">[[diff.header.assert.h]]</a>

The token `static_assert` is a keyword in this International Standard
[[lex.key]]. It does not appear as a macro name defined in `<cassert>`.

#### Header `<iso646.h>` <a id="diff.header.iso646.h">[[diff.header.iso646.h]]</a>

The tokens `and`, `and_eq`, `bitand`, `bitor`, `compl`, `not`, `not_eq`,
`or`, `or_eq`, `xor`, and `xor_eq` are keywords in this International
Standard [[lex.key]], and are not introduced as macros by .

#### Header `<stdalign.h>` <a id="diff.header.stdalign.h">[[diff.header.stdalign.h]]</a>

The token `alignas` is a keyword in this International Standard
[[lex.key]], and is not introduced as a macro by .

#### Header `<stdbool.h>` <a id="diff.header.stdbool.h">[[diff.header.stdbool.h]]</a>

The tokens `bool`, `true`, and `false` are keywords in this
International Standard [[lex.key]], and are not introduced as macros by
.

#### Macro `NULL` <a id="diff.null">[[diff.null]]</a>

The macro `NULL`, defined in any of `<clocale>`, `<cstddef>`,
`<cstdio>`, `<cstdlib>`, `<cstring>`, `<ctime>`, or `<cwchar>`, is an
*implementation-defined* C++ null pointer constant in this International
Standard [[support.types]].

### Modifications to declarations <a id="diff.mods.to.declarations">[[diff.mods.to.declarations]]</a>

Header `<cstring>`: The following functions have different declarations:

- `strchr`
- `strpbrk`
- `strrchr`
- `strstr`
- `memchr`

Subclause [[cstring.syn]] describes the changes.

Header `<cwchar>`: The following functions have different declarations:

- `wcschr`
- `wcspbrk`
- `wcsrchr`
- `wcsstr`
- `wmemchr`

Subclause [[cwchar.syn]] describes the changes.

Header `<cstddef>` declares the name `nullptr_t` in addition to the
names declared in `<stddef.h>` in the C standard library.

### Modifications to behavior <a id="diff.mods.to.behavior">[[diff.mods.to.behavior]]</a>

Header `<cstdlib>`: The following functions have different behavior:

- `atexit`
- `exit`
- `abort`

Subclause [[support.start.term]] describes the changes.

Header `<csetjmp>`: The following functions have different behavior:

- `longjmp`

Subclause [[csetjmp.syn]] describes the changes.

#### Macro `offsetof(type, member-designator)` <a id="diff.offsetof">[[diff.offsetof]]</a>

The macro `offsetof`, defined in `<cstddef>`, accepts a restricted set
of `type` arguments in this International Standard. Subclause
[[support.types.layout]] describes the change.

#### Memory allocation functions <a id="diff.malloc">[[diff.malloc]]</a>

The functions `aligned_alloc`, `calloc`, `malloc`, and `realloc` are
restricted in this International Standard. Subclause [[c.malloc]]
describes the changes.

<!-- Link reference definitions -->
[algorithms]: algorithms.md#algorithms
[basic]: basic.md#basic
[basic.link]: basic.md#basic.link
[basic.scope]: basic.md#basic.scope
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[c.malloc]: utilities.md#c.malloc
[class]: class.md#class
[containers]: containers.md#containers
[conv.array]: expr.md#conv.array
[conv.func]: expr.md#conv.func
[conv.lval]: expr.md#conv.lval
[cpp]: cpp.md#cpp
[csetjmp.syn]: support.md#csetjmp.syn
[cstring.syn]: strings.md#cstring.syn
[cwchar.syn]: strings.md#cwchar.syn
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.constinit]: dcl.md#dcl.constinit
[dcl.dcl]: dcl.md#dcl.dcl
[dcl.fct.def.coroutine]: dcl.md#dcl.fct.def.coroutine
[dcl.type]: dcl.md#dcl.type
[dcl.typedef]: dcl.md#dcl.typedef
[depr]: #depr
[depr.c.headers]: future.md#depr.c.headers
[diagnostics]: diagnostics.md#diagnostics
[diff.basic]: #diff.basic
[diff.char16]: #diff.char16
[diff.class]: #diff.class
[diff.cpp]: #diff.cpp
[diff.cpp03]: #diff.cpp03
[diff.cpp03.algorithms]: #diff.cpp03.algorithms
[diff.cpp03.class]: #diff.cpp03.class
[diff.cpp03.containers]: #diff.cpp03.containers
[diff.cpp03.dcl.dcl]: #diff.cpp03.dcl.dcl
[diff.cpp03.diagnostics]: #diff.cpp03.diagnostics
[diff.cpp03.expr]: #diff.cpp03.expr
[diff.cpp03.input.output]: #diff.cpp03.input.output
[diff.cpp03.language.support]: #diff.cpp03.language.support
[diff.cpp03.lex]: #diff.cpp03.lex
[diff.cpp03.library]: #diff.cpp03.library
[diff.cpp03.numerics]: #diff.cpp03.numerics
[diff.cpp03.strings]: #diff.cpp03.strings
[diff.cpp03.temp]: #diff.cpp03.temp
[diff.cpp03.utilities]: #diff.cpp03.utilities
[diff.cpp11]: #diff.cpp11
[diff.cpp11.basic]: #diff.cpp11.basic
[diff.cpp11.dcl.dcl]: #diff.cpp11.dcl.dcl
[diff.cpp11.expr]: #diff.cpp11.expr
[diff.cpp11.input.output]: #diff.cpp11.input.output
[diff.cpp11.lex]: #diff.cpp11.lex
[diff.cpp11.library]: #diff.cpp11.library
[diff.cpp14]: #diff.cpp14
[diff.cpp14.class]: #diff.cpp14.class
[diff.cpp14.containers]: #diff.cpp14.containers
[diff.cpp14.dcl.dcl]: #diff.cpp14.dcl.dcl
[diff.cpp14.depr]: #diff.cpp14.depr
[diff.cpp14.except]: #diff.cpp14.except
[diff.cpp14.expr]: #diff.cpp14.expr
[diff.cpp14.lex]: #diff.cpp14.lex
[diff.cpp14.library]: #diff.cpp14.library
[diff.cpp14.string]: #diff.cpp14.string
[diff.cpp14.temp]: #diff.cpp14.temp
[diff.cpp14.utilities]: #diff.cpp14.utilities
[diff.cpp17]: #diff.cpp17
[diff.cpp17.alg.reqs]: #diff.cpp17.alg.reqs
[diff.cpp17.basic]: #diff.cpp17.basic
[diff.cpp17.class]: #diff.cpp17.class
[diff.cpp17.containers]: #diff.cpp17.containers
[diff.cpp17.dcl.dcl]: #diff.cpp17.dcl.dcl
[diff.cpp17.depr]: #diff.cpp17.depr
[diff.cpp17.except]: #diff.cpp17.except
[diff.cpp17.expr]: #diff.cpp17.expr
[diff.cpp17.input.output]: #diff.cpp17.input.output
[diff.cpp17.iterators]: #diff.cpp17.iterators
[diff.cpp17.lex]: #diff.cpp17.lex
[diff.cpp17.library]: #diff.cpp17.library
[diff.cpp17.over]: #diff.cpp17.over
[diff.cpp17.temp]: #diff.cpp17.temp
[diff.dcl]: #diff.dcl
[diff.expr]: #diff.expr
[diff.header.assert.h]: #diff.header.assert.h
[diff.header.iso646.h]: #diff.header.iso646.h
[diff.header.stdalign.h]: #diff.header.stdalign.h
[diff.header.stdbool.h]: #diff.header.stdbool.h
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
[diff.stat]: #diff.stat
[diff.wchar.t]: #diff.wchar.t
[except]: except.md#except
[expr]: expr.md#expr
[expr.new]: expr.md#expr.new
[expr.prim.req]: expr.md#expr.prim.req
[expr.sizeof]: expr.md#expr.sizeof
[input.output]: input.md#input.output
[iterators]: iterators.md#iterators
[lex]: lex.md#lex
[lex.key]: lex.md#lex.key
[lex.name]: lex.md#lex.name
[lex.string]: lex.md#lex.string
[library]: library.md#library
[numerics]: numerics.md#numerics
[over]: over.md#over
[stmt.stmt]: stmt.md#stmt.stmt
[strings]: strings.md#strings
[support]: support.md#support
[support.start.term]: support.md#support.start.term
[support.types]: support.md#support.types
[support.types.layout]: support.md#support.types.layout
[temp]: temp.md#temp
[temp.concept]: temp.md#temp.concept
[temp.pre]: temp.md#temp.pre
[thread]: thread.md#thread
[utilities]: utilities.md#utilities
