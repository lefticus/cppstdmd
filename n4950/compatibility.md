## C++ and ISO C++20 <a id="diff.cpp20">[[diff.cpp20]]</a>

### General <a id="diff.cpp20.general">[[diff.cpp20.general]]</a>

Subclause [[diff.cpp20]] lists the differences between C++ and ISO C++20
(ISO/IEC 14882:2020, *Programming Languages --- C++*), by the chapters
of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp20.lex">[[diff.cpp20.lex]]</a>

Previously valid identifiers containing characters not present in
UAX #44 properties XID_Start or XID_Continue, or not in Normalization
Form C, are now rejected. Prevent confusing characters in identifiers.
Requiring normalization of names ensures consistent linker behavior.
Some identifiers are no longer well-formed.

Concatenated *string-literal*s can no longer have conflicting
*encoding-prefix*es. Removal of unimplemented conditionally-supported
feature. Concatenation of *string-literal*s with different
*encoding-prefix*es is now ill-formed. For example:

``` cpp
auto c = L"a" U"b";             // was conditionally-supported; now ill-formed
```

###  [[expr]]: expressions <a id="diff.cpp20.expr">[[diff.cpp20.expr]]</a>

Change move-eligible *id-expression*s from lvalues to xvalues. Simplify
the rules for implicit move. Valid C++20 code that relies on a returned
*id-expression*’s being an lvalue may change behavior or fail to
compile. For example:

``` cpp
decltype(auto) f(int&& x) { return (x); }       // returns int&&; previously returned int&
int& g(int&& x) { return x; }                   // ill-formed; previously well-formed
```

Change the meaning of comma in subscript expressions. Enable repurposing
a deprecated syntax to support multidimensional indexing. Valid C++20
code that uses a comma expression within a subscript expression may fail
to compile. For example:

``` cpp
arr[1, 2]               // was equivalent to arr[(1, 2)],
                        // now equivalent to arr.operator[](1, 2) or ill-formed
```

###  [[stmt.stmt]]: statements <a id="diff.cpp20.stmt">[[diff.cpp20.stmt]]</a>

The lifetime of temporary objects in the *for-range-initializer* is
extended until the end of the loop [[class.temporary]]. Improve
usability of the range-based `for` statement. Destructors of some
temporary objects are invoked later. For example:

``` cpp
void f() {
  std::vector<int> v = { 42, 17, 13 };
  std::mutex m;

  for (int x :
       static_cast<void>(std::lock_guard<std::mutex>(m)), v) {  // lock released in \CppXX
    std::lock_guard<std::mutex> guard(m);                       // OK in \CppXX, now deadlocks
  }
}
```

###  [[dcl.dcl]]: declarations <a id="diff.cpp20.dcl">[[diff.cpp20.dcl]]</a>

UTF-8 string literals may initialize arrays of `char` or
`unsigned char`. Compatibility with previously written code that
conformed to previous versions of this document. Arrays of `char` or
`unsigned char` may now be initialized with a UTF-8 string literal. This
can affect initialization that includes arrays that are directly
initialized within class types, typically aggregates. For example:

``` cpp
struct A {
  char8_t s[10];
};
struct B {
  char s[10];
};

void f(A);
void f(B);

int main() {
  f({u8""});            // ambiguous
}
```

###  [[temp]]: templates <a id="diff.cpp20.temp">[[diff.cpp20.temp]]</a>

Deducing template arguments from exception specifications. Facilitate
generic handling of throwing and non-throwing functions. Valid ISO C++20
code may be ill-formed in this revision of C++. For example:

``` cpp
template<bool> struct A { };
template<bool B> void f(void (*)(A<B>) noexcept(B));
void g(A<false>) noexcept;
void h() {
  f(g);                         // ill-formed; previously well-formed
}
```

###  [[library]]: library introduction <a id="diff.cpp20.library">[[diff.cpp20.library]]</a>

New headers. New functionality. The following C++ headers are new:
`<expected>`, `<flat_map>`, `<flat_set>`, `<generator>`, `<print>`,
`<spanstream>`, `<stacktrace>`, and `<stdatomic.h>`. Valid C++20 code
that `#include`s headers with these names may be invalid in this
revision of C++.

###  [[concepts]]: concepts library <a id="diff.cpp20.concepts">[[diff.cpp20.concepts]]</a>

Replace `common_reference_with` in `three_way_comparable_with`,
`equality_comparable_with`, and `totally_ordered_with` with an
exposition-only concept. Allow uncopyable, but movable, types to model
these concepts. Valid C++20 code relying on subsumption with
`common_reference_with` may fail to compile in this revision of C++. For
example:

``` cpp
template<class T, class U>
  requires equality_comparable_with<T, U>
bool attempted_equals(const T&, const U& u);    // previously selected overload

template<class T, class U>
  requires common_reference_with<const remove_reference_t<T>&, const remove_reference_t<U>&>
bool attempted_equals(const T& t, const U& u);  // ambiguous overload; previously
                                                // rejected by partial ordering
bool test(shared_ptr<int> p) {
  return attempted_equals(p, nullptr);          // ill-formed; previously well-formed
}
```

###  [[mem]]: memory management library <a id="diff.cpp20.memory">[[diff.cpp20.memory]]</a>

Forbid partial and explicit program-defined specializations of
`allocator_traits`. Allow addition of `allocate_at_least` to
`allocator_traits`, and potentially other members in the future. Valid
C++20 code that partially or explicitly specializes `allocator_traits`
is ill-formed with no diagnostic required in this revision of C++.

###  [[utilities]]: general utilities library <a id="diff.cpp20.utilities">[[diff.cpp20.utilities]]</a>

Signature changes: `format`, `format_to`, `vformat_to`, `format_to_n`,
`formatted_size`. Removal of `format_args_t`. Improve safety via
compile-time format string checks, avoid unnecessary template
instantiations. Valid C++20 code that contained errors in format strings
or relied on previous format string signatures or `format_args_t` may
become ill-formed. For example:

``` cpp
auto s = std::format("{:d}", "I am not a number");      // ill-formed,
                                                        // previously threw format_error
```

Signature changes: `format`, `format_to`, `format_to_n`,
`formatted_size`. Enable formatting of views that do not support
iteration when const-qualified and that are not copyable. Valid C++20
code that passes bit fields to formatting functions may become
ill-formed. For example:

``` cpp
struct tiny {
  int bit: 1;
};

auto t = tiny();
std::format("{}", t.bit);       // ill-formed, previously returned "0"
```

Restrict types of formatting arguments used as *width* or *precision* in
a *std-format-spec*. Disallow types that do not have useful or portable
semantics as a formatting width or precision. Valid C++20 code that
passes a boolean or character type as *arg-id* becomes invalid. For
example:

``` cpp
std::format("{:*^{}}", "", true);   // ill-formed, previously returned "*"
std::format("{:*^{}}", "", '1');    // ill-formed, previously returned an
                                    // implementation-defined number of '*' characters
```

Removed the `formatter` specialization:

``` cpp
template<size_t N> struct formatter<const charT[N], charT>;
```

The specialization is inconsistent with the design of `formatter`, which
is intended to be instantiated only with cv-unqualified object types.
Valid C++20 code that instantiated the removed specialization can become
ill-formed.

###  [[strings]]: strings library <a id="diff.cpp20.strings">[[diff.cpp20.strings]]</a>

Additional rvalue overload for the `substr` member function and the
corresponding constructor. Improve efficiency of operations on rvalues.
Valid C++20 code that created a substring by calling `substr` (or the
corresponding constructor) on an xvalue expression with type `S` that is
a specialization of `basic_string` may change meaning in this revision
of C++. For example:

``` cpp
std::string s1 = "some long string that forces allocation", s2 = s1;
std::move(s1).substr(10, 5);
assert(s1 == s2);       // unspecified, previously guaranteed to be true
std::string s3(std::move(s2), 10, 5);
assert(s1 == s2);       // unspecified, previously guaranteed to be true
```

###  [[containers]]: containers library <a id="diff.cpp20.containers">[[diff.cpp20.containers]]</a>

Heterogeneous `extract` and `erase` overloads for associative
containers. Improve efficiency of erasing elements from associative
containers. Valid C++20 code may fail to compile in this revision of
C++. For example:

``` cpp
struct B {
  auto operator<=>(const B&) const = default;
};

struct D : private B {
  void f(std::set<B, std::less<>>& s) {
    s.erase(*this);             // ill formed; previously well-formed
  }
};
```

###  [[thread]]: concurrency support library <a id="diff.cpp20.thread">[[diff.cpp20.thread]]</a>

In this revision of C++, it is implementation-defined whether a
barrier’s phase completion step runs if no thread calls `wait`.
Previously the phase completion step was guaranteed to run on the last
thread that calls `arrive` or `arrive_and_drop` during the phase. In
this revision of C++, it can run on any of the threads that arrived or
waited at the barrier during the phase. Correct contradictory wording
and improve implementation flexibility for performance. Valid C++20 code
using a barrier might have different semantics in this revision of C++
if it depends on a completion function’s side effects occurring exactly
once, on a specific thread running the phase completion step, or on a
completion function’s side effects occurring without `wait` having been
called. For example:

``` cpp
auto b0 = std::barrier(1);
b0.arrive();
b0.arrive();            // implementation-defined; previously well-defined

int data = 0;
auto b1 = std::barrier(1, [&] { data++; });
b1.arrive();
assert(data == 1);      // implementation-defined; previously well-defined
b1.arrive();            // implementation-defined; previously well-defined
```

## C++ and ISO C++17 <a id="diff.cpp17">[[diff.cpp17]]</a>

### General <a id="diff.cpp17.general">[[diff.cpp17.general]]</a>

Subclause [[diff.cpp17]] lists the differences between C++ and ISO C++17
(ISO/IEC 14882:2017, *Programming Languages --- C++*), by the chapters
of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp17.lex">[[diff.cpp17.lex]]</a>

New identifiers with special meaning. Required for new features. Logical
lines beginning with `module` or `import` may be interpreted differently
in this revision of C++. For example:

``` cpp
class module {};
module m1;          // was variable declaration; now module-declaration
module *m2;         // variable declaration

class import {};
import j1;          // was variable declaration; now module-import-declaration
::import j2;        // variable declaration
```

*header-name* tokens are formed in more contexts. Required for new
features. When the identifier `import` is followed by a `<` character, a
*header-name* token may be formed. For example:

``` cpp
template<typename> class import {};
import<int> f();                // ill-formed; previously well-formed
::import<int> g();              // OK
```

New keywords. Required for new features.

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
not valid in this revision of C++.

New operator `<=>`. Necessary for new functionality. Valid C++17 code
that contains a `<=` token immediately followed by a `>` token may be
ill-formed or have different semantics in this revision of C++. For
example:

``` cpp
namespace N {
  struct X {};
  bool operator<=(X, X);
  template<bool(X, X)> struct Y {};
  Y<operator<=> y;              // ill-formed; previously well-formed
}
```

Type of UTF-8 string and character literals. Required for new features.
The changed types enable function overloading, template specialization,
and type deduction to distinguish ordinary and UTF-8 string and
character literals. Valid C++17 code that depends on UTF-8 string
literals having type “array of `const char`” and UTF-8 character
literals having type “`char`” is not valid in this revision of C++. For
example:

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

A pseudo-destructor call ends the lifetime of the object to which it is
applied. Increase consistency of the language model. Valid ISO C++17
code may be ill-formed or have undefined behavior in this revision of
C++. For example:

``` cpp
int f() {
  int a = 123;
  using T = int;
  a.~T();
  return a;         // undefined behavior; previously returned 123
}
```

Except for the initial release operation, a release sequence consists
solely of atomic read-modify-write operations. Removal of rarely used
and confusing feature. If a `memory_order_release` atomic store is
followed by a `memory_order_relaxed` store to the same variable by the
same thread, then reading the latter value with a `memory_order_acquire`
load no longer provides any “happens before” guarantees, even in the
absence of intervening stores by another thread.

###  [[expr]]: expressions <a id="diff.cpp17.expr">[[diff.cpp17.expr]]</a>

Implicit lambda capture may capture additional entities. Rule
simplification, necessary to resolve interactions with constexpr if.
Lambdas with a *capture-default* may capture local entities that were
not captured in C++17 if those entities are only referenced in contexts
that do not result in an odr-use.

###  [[dcl.dcl]]: declarations <a id="diff.cpp17.dcl.dcl">[[diff.cpp17.dcl.dcl]]</a>

Unnamed classes with a typedef name for linkage purposes can contain
only C-compatible constructs. Necessary for implementability. Valid
C++17 code may be ill-formed in this revision of C++. For example:

``` cpp
typedef struct {
  void f() {}           // ill-formed; previously well-formed
} S;
```

A function cannot have different default arguments in different
translation units. Required for modules support. Valid C++17 code may be
ill-formed in this revision of C++, with no diagnostic required. For
example:

``` cpp
// Translation unit 1
int f(int a = 42);
int g() { return f(); }

// Translation unit 2
int f(int a = 76) { return a; }         // ill-formed, no diagnostic required; previously well-formed
int g();
int main() { return g(); }              // used to return 42
```

A class that has user-declared constructors is never an aggregate.
Remove potentially error-prone aggregate initialization which may apply
notwithstanding the declared constructors of a class. Valid C++17 code
that aggregate-initializes a type with a user-declared constructor may
be ill-formed or have different semantics in this revision of C++. For
example:

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

Boolean conversion from a pointer or pointer-to-member type is now a
narrowing conversion. Catches bugs. Valid C++17 code may fail to compile
in this revision of C++. For example:

``` cpp
bool y[] = { "bc" };    // ill-formed; previously well-formed
```

###  [[class]]: classes <a id="diff.cpp17.class">[[diff.cpp17.class]]</a>

The class name can no longer be used parenthesized immediately after an
`explicit` *decl-specifier* in a constructor declaration. The
*conversion-function-id* can no longer be used parenthesized immediately
after an `explicit` *decl-specifier* in a conversion function
declaration. Necessary for new functionality. Valid C++17 code may fail
to compile in this revision of C++. For example:

``` cpp
struct S {
  explicit (S)(const S&);       // ill-formed; previously well-formed
  explicit (operator int)();    // ill-formed; previously well-formed
  explicit(true) (S)(int);      // OK
};
```

A *simple-template-id* is no longer valid as the *declarator-id* of a
constructor or destructor. Remove potentially error-prone option for
redundancy. Valid C++17 code may fail to compile in this revision of
C++. For example:

``` cpp
template<class T>
struct A {
  A<T>();           // error: simple-template-id not allowed for constructor
  A(int);           // OK, injected-class-name used
  ~A<T>();          // error: simple-template-id not allowed for destructor
};
```

A function returning an implicitly movable entity may invoke a
constructor taking an rvalue reference to a type different from that of
the returned expression. Function and catch-clause parameters can be
thrown using move constructors. Side effect of making it easier to write
more efficient code that takes advantage of moves. Valid C++17 code may
fail to compile or have different semantics in this revision of C++. For
example:

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

Equality and inequality expressions can now find reversed and rewritten
candidates. Improve consistency of equality with three-way comparison
and make it easier to write the full complement of equality operations.
For certain pairs of types where one is convertible to the other,
equality or inequality expressions between an object of one type and an
object of the other type invoke a different operator. Also, for certain
types, equality or inequality expressions between two objects of that
type become ambiguous. For example:

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

Overload resolution may change for equality operators [[expr.eq]].
Support calling `operator==` with reversed order of arguments. Valid
C++17 code that uses equality operators with conversion functions may be
ill-formed or have different semantics in this revision of C++. For
example:

``` cpp
struct A {
  operator int() const { return 10; }
};

bool operator==(A, int);        // #1
// #2 is built-in candidate: bool operator==(int, int);
bool b = 10 == A();             // calls #1 with reversed order of arguments; previously selected #2

struct B {
  bool operator==(const B&);    // member function with no cv-qualifier
};
B b1;
bool eq = (b1 == b1);           // ambiguous; previously well-formed
```

###  [[temp]]: templates <a id="diff.cpp17.temp">[[diff.cpp17.temp]]</a>

An *unqualified-id* that is followed by a `<` and for which name lookup
finds nothing or finds a function will be treated as a *template-name*
in order to potentially cause argument dependent lookup to be performed.
It was problematic to call a function template with an explicit template
argument list via argument dependent lookup because of the need to have
a template with the same name visible via normal lookup. Previously
valid code that uses a function name as the left operand of a `<`
operator would become ill-formed. For example:

``` cpp
struct A {};
bool operator<(void (*fp)(), A);
void f() {}
int main() {
  A a;
  f < a;    // ill-formed; previously well-formed
  (f) < a;  // still well-formed
}
```

###  [[except]]: exception handling <a id="diff.cpp17.except">[[diff.cpp17.except]]</a>

Remove `throw()` exception specification. Removal of obsolete feature
that has been replaced by `noexcept`. A valid C++17 function
declaration, member function declaration, function pointer declaration,
or function reference declaration that uses `throw()` for its exception
specification will be rejected as ill-formed in this revision of C++. It
should simply be replaced with `noexcept` for no change of meaning since
C++17.

\[*Note 1*: There is no way to write a function declaration that is
non-throwing in this revision of C++ and is also non-throwing in C++03
except by using the preprocessor to generate a different token sequence
in each case. — *end note*\]

###  [[library]]: library introduction <a id="diff.cpp17.library">[[diff.cpp17.library]]</a>

New headers. New functionality. The following C++ headers are new:
`<barrier>`, `<bit>`, `<charconv>`, `<compare>`, `<concepts>`,
`<coroutine>`, `<format>`, `<latch>`, `<numbers>`, `<ranges>`,
`<semaphore>`, `<source_location>`, `<span>`, `<stop_token>`,
`<syncstream>`, and `<version>`. Valid C++17 code that `#include`s
headers with these names may be invalid in this revision of C++.

Remove vacuous C++ header files. The empty headers implied a false
requirement to achieve C compatibility with the C++ headers. A valid
C++17 program that `#include`s any of the following headers may fail to
compile: , , , , and . To retain the same behavior:

- a `#include` of can be replaced by a `#include` of `<complex>`,
- a `#include` of can be replaced by a `#include` of `<cmath>` and a
  `#include` of `<complex>`, and
- a `#include` of , , or can simply be removed.

###  [[containers]]: containers library <a id="diff.cpp17.containers">[[diff.cpp17.containers]]</a>

Return types of `remove`, `remove_if`, and `unique` changed from `void`
to `container::size_type`. Improve efficiency and convenience of finding
number of removed elements. Code that depends on the return types might
have different semantics in this revision of C++. Translation units
compiled against this version of C++ may be incompatible with
translation units compiled against C++17, either failing to link or
having undefined behavior.

###  [[iterators]]: iterators library <a id="diff.cpp17.iterators">[[diff.cpp17.iterators]]</a>

The specialization of `iterator_traits` for `void*` and for function
pointer types no longer contains any nested typedefs. Corrects an issue
misidentifying pointer types that are not incrementable as iterator
types. A valid C++17 program that relies on the presence of the typedefs
may fail to compile, or have different behavior.

###  [[algorithms]]: algorithms library <a id="diff.cpp17.alg.reqs">[[diff.cpp17.alg.reqs]]</a>

The number and order of deducible template parameters for algorithm
declarations is now unspecified, instead of being as-declared. Increase
implementor freedom and allow some function templates to be implemented
as function objects with templated call operators. A valid C++17 program
that passes explicit template arguments to algorithms not explicitly
specified to allow such in this version of C++ may fail to compile or
have undefined behavior.

###  [[input.output]]: input/output library <a id="diff.cpp17.input.output">[[diff.cpp17.input.output]]</a>

Character array extraction only takes array types. Increase safety via
preventing buffer overflow at compile time. Valid C++17 code may fail to
compile in this revision of C++. For example:

``` cpp
auto p = new char[100];
char q[100];
std::cin >> std::setw(20) >> p;         // ill-formed; previously well-formed
std::cin >> std::setw(20) >> q;         // OK
```

Overload resolution for ostream inserters used with UTF-8 literals.
Required for new features. Valid C++17 code that passes UTF-8 literals
to `basic_ostream<char, ...>::operator<<` or
`basic_ostream<wchar_t, ...>::operator<<` is now ill-formed. For
example:

``` cpp
std::cout << u8"text";          // previously called operator<<(const char*) and printed a string;
                                // now ill-formed
std::cout << u8'X';             // previously called operator<<(char) and printed a character;
                                // now ill-formed
```

Overload resolution for ostream inserters used with `wchar_t`,
`char16_t`, or `char32_t` types. Removal of surprising behavior. Valid
C++17 code that passes `wchar_t`, `char16_t`, or `char32_t` characters
or strings to `basic_ostream<char, ...>::operator<<` or that passes
`char16_t` or `char32_t` characters or strings to
`basic_ostream<wchar_t, ...>::operator<<` is now ill-formed. For
example:

``` cpp
std::cout << u"text";           // previously formatted the string as a pointer value;
                                // now ill-formed
std::cout << u'X';              // previously formatted the character as an integer value;
                                // now ill-formed
```

Return type of filesystem path format observer member functions.
Required for new features. Valid C++17 code that depends on the
`u8string()` and `generic_u8string()` member functions of
`std::filesystem::path` returning `std::string` is not valid in this
revision of C++. For example:

``` cpp
std::filesystem::path p;
std::string s1 = p.u8string();          // ill-formed; previously well-formed
std::string s2 = p.generic_u8string();  // ill-formed; previously well-formed
```

###  [[depr]]: compatibility features <a id="diff.cpp17.depr">[[diff.cpp17.depr]]</a>

Remove `uncaught_exception`. The function did not have a clear
specification when multiple exceptions were active, and has been
superseded by `uncaught_exceptions`. A valid C++17 program that calls
`std::uncaught_exception` may fail to compile. It can be revised to use
`std::uncaught_exceptions` instead, for clear and portable semantics.

Remove support for adaptable function API. The deprecated support relied
on a limited convention that could not be extended to support the
general case or new language features. It has been superseded by direct
language support with `decltype`, and by the `std::bind` and
`std::not_fn` function templates. A valid C++17 program that relies on
the presence of `result_type`, `argument_type`, `first_argument_type`,
or `second_argument_type` in a standard library class may fail to
compile. A valid C++17 program that calls `not1` or `not2`, or uses the
class templates `unary_negate` or `binary_negate`, may fail to compile.

Remove redundant members from `std::allocator`. `std::allocator` was
overspecified, encouraging direct usage in user containers rather than
relying on `std::allocator_traits`, leading to poor containers. A valid
C++17 program that directly makes use of the `pointer`, `const_pointer`,
`reference`, `const_reference`, `rebind`, `address`, `construct`,
`destroy`, or `max_size` members of `std::allocator`, or that directly
calls `allocate` with an additional hint argument, may fail to compile.

Remove `raw_storage_iterator`. The iterator encouraged use of
potentially-throwing algorithms, but did not return the number of
elements successfully constructed, as would be necessary to destroy
them. A valid C++17 program that uses this iterator class may fail to
compile.

Remove temporary buffers API. The temporary buffer facility was intended
to provide an efficient optimization for small memory requests, but
there is little evidence this was achieved in practice, while requiring
the user to provide their own exception-safe wrappers to guard use of
the facility in many cases. A valid C++17 program that calls
`get_temporary_buffer` or `return_temporary_buffer` may fail to compile.

Remove `shared_ptr::unique`. The result of a call to this member
function is not reliable in the presence of multiple threads and weak
pointers. The member function `use_count` is similarly unreliable, but
has a clearer contract in such cases, and remains available for
well-defined use in single-threaded cases. A valid C++17 program that
calls `unique` on a `shared_ptr` object may fail to compile.

Remove deprecated type traits. The traits had unreliable or awkward
interfaces. The `is_literal_type` trait provided no way to detect which
subset of constructors and member functions of a type were declared
`constexpr`. The `result_of` trait had a surprising syntax that did not
directly support function types. It has been superseded by the
`invoke_result` trait. A valid C++17 program that relies on the
`is_literal_type` or `result_of` type traits, on the `is_literal_type_v`
variable template, or on the `result_of_t` alias template may fail to
compile.

## C++ and ISO C++14 <a id="diff.cpp14">[[diff.cpp14]]</a>

### General <a id="diff.cpp14.general">[[diff.cpp14.general]]</a>

Subclause [[diff.cpp14]] lists the differences between C++ and ISO C++14
(ISO/IEC 14882:2014, *Programming Languages --- C++*), in addition to
those listed above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp14.lex">[[diff.cpp14.lex]]</a>

Removal of trigraph support as a required feature. Prevents accidental
uses of trigraphs in non-raw string literals and comments. Valid C++14
code that uses trigraphs may not be valid or may have different
semantics in this revision of C++. Implementations may choose to
translate trigraphs as specified in C++14 if they appear outside of a
raw string literal, as part of the *implementation-defined* mapping from
input source file characters to the translation character set.

*pp-number* can contain `p` *sign* and `P` *sign*. Necessary to enable
*hexadecimal-floating-point-literal*s. Valid C++14 code may fail to
compile or produce different results in this revision of C++.
Specifically, character sequences like `0p+0` and `0e1_p+0` are three
separate tokens each in C++14, but one single token in this revision of
C++. For example:

``` cpp
#define F(a) b ## a
int b0p = F(0p+0);  // ill-formed; equivalent to ``int b0p = b0p + 0;'' in C++14
```

###  [[expr]]: expressions <a id="diff.cpp14.expr">[[diff.cpp14.expr]]</a>

Remove increment operator with `bool` operand. Obsolete feature with
occasionally surprising semantics. A valid C++14 expression utilizing
the increment operator on a `bool` lvalue is ill-formed in this revision
of C++.

Dynamic allocation mechanism for over-aligned types. Simplify use of
over-aligned types. In C++14 code that uses a *new-expression* to
allocate an object with an over-aligned class type, where that class has
no allocation functions of its own, `::operator new(std::size_t)` is
used to allocate the memory. In this revision of C++,
`::operator new(std::size_t, std::align_val_t)` is used instead.

###  [[dcl.dcl]]: declarations <a id="diff.cpp14.dcl.dcl">[[diff.cpp14.dcl.dcl]]</a>

Removal of `register` *storage-class-specifier*. Enable repurposing of
deprecated keyword in future revisions of C++. A valid C++14 declaration
utilizing the `register` *storage-class-specifier* is ill-formed in this
revision of C++. The specifier can simply be removed to retain the
original meaning.

`auto` deduction from *braced-init-list*. More intuitive deduction
behavior. Valid C++14 code may fail to compile or may change meaning in
this revision of C++. For example:

``` cpp
auto x1{1};         // was std::initializer_list<int>, now int
auto x2{1, 2};      // was std::initializer_list<int>, now ill-formed
```

Make exception specifications be part of the type system. Improve
type-safety. Valid C++14 code may fail to compile or change meaning in
this revision of C++. For example:

``` cpp
void g1() noexcept;
void g2();
template<class T> int f(T *, T *);
int x = f(g1, g2);              // ill-formed; previously well-formed
```

Definition of an aggregate is extended to apply to user-defined types
with base classes. To increase convenience of aggregate initialization.
Valid C++14 code may fail to compile or produce different results in
this revision of C++; initialization from an empty initializer list will
perform aggregate initialization instead of invoking a default
constructor for the affected types. For example:

``` cpp
struct derived;
struct base {
  friend struct derived;
private:
  base();
};
struct derived : base {};

derived d1{};       // error; the code was well-formed in C++14
derived d2;         // still OK
```

###  [[class]]: classes <a id="diff.cpp14.class">[[diff.cpp14.class]]</a>

Inheriting a constructor no longer injects a constructor into the
derived class. Better interaction with other language features. Valid
C++14 code that uses inheriting constructors may not be valid or may
have different semantics. A *using-declaration* that names a constructor
now makes the corresponding base class constructors visible to
initializations of the derived class rather than declaring additional
derived class constructors. For example:

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

Allowance to deduce from the type of a non-type template argument. In
combination with the ability to declare non-type template arguments with
placeholder types, allows partial specializations to decompose from the
type deduced for the non-type template argument. Valid C++14 code may
fail to compile or produce different results in this revision of C++.
For example:

``` cpp
template <int N> struct A;
template <typename T, T N> int foo(A<N> *) = delete;
void foo(void *);
void bar(A<0> *p) {
  foo(p);           // ill-formed; previously well-formed
}
```

###  [[except]]: exception handling <a id="diff.cpp14.except">[[diff.cpp14.except]]</a>

Remove dynamic exception specifications. Dynamic exception
specifications were a deprecated feature that was complex and brittle in
use. They interacted badly with the type system, which became a more
significant issue in this revision of C++ where (non-dynamic) exception
specifications are part of the function type. A valid C++14 function
declaration, member function declaration, function pointer declaration,
or function reference declaration, if it has a potentially throwing
dynamic exception specification, is rejected as ill-formed in this
revision of C++. Violating a non-throwing dynamic exception
specification calls `terminate` rather than `unexpected`, and it is
unspecified whether stack unwinding is performed prior to such a call.

###  [[library]]: library introduction <a id="diff.cpp14.library">[[diff.cpp14.library]]</a>

New headers. New functionality. The following C++ headers are new:
`<any>`, `<charconv>`, `<execution>`, `<filesystem>`,
`<memory_resource>`, `<optional>`,  
`<string_view>`, and `<variant>`. Valid C++14 code that `#include`s
headers with these names may be invalid in this revision of C++.

New reserved namespaces. Reserve namespaces for future revisions of the
standard library that might otherwise be incompatible with existing
programs. The global namespaces `std` followed by an arbitrary sequence
of *digit*s [[lex.name]] are reserved for future standardization. Valid
C++14 code that uses such a top-level namespace, e.g., `std2`, may be
invalid in this revision of C++.

###  [[utilities]]: general utilities library <a id="diff.cpp14.utilities">[[diff.cpp14.utilities]]</a>

Constructors taking allocators removed. No implementation consensus.
Valid C++14 code may fail to compile or may change meaning in this
revision of C++. Specifically, constructing a `std::function` with an
allocator is ill-formed and uses-allocator construction will not pass an
allocator to `std::function` constructors in this revision of C++.

Different constraint on conversions from `unique_ptr`. Adding array
support to `shared_ptr`, via the syntax `shared_ptr<T[]>` and
`shared_ptr<T[N]>`. Valid C++14 code may fail to compile or may change
meaning in this revision of C++. For example:

``` cpp
#include <memory>
std::unique_ptr<int[]> arr(new int[1]);
std::shared_ptr<int> ptr(std::move(arr));   // error: int(*)[] is not compatible with int*
```

###  [[strings]]: strings library <a id="diff.cpp14.string">[[diff.cpp14.string]]</a>

Non-const `.data()` member added. The lack of a non-const `.data()`
differed from the similar member of `std::vector`. This change
regularizes behavior. Overloaded functions which have differing code
paths for `char*` and `const char*` arguments will execute differently
when called with a non-const string’s `.data()` member in this revision
of C++. For example:

``` cpp
int f(char *) = delete;
int f(const char *);
string s;
int x = f(s.data());            // ill-formed; previously well-formed
```

###  [[containers]]: containers library <a id="diff.cpp14.containers">[[diff.cpp14.containers]]</a>

Requirements change: Increase portability, clarification of associative
container requirements. Valid C++14 code that attempts to use
associative containers having a comparison object with non-const
function call operator may fail to compile in this revision of C++. For
example:

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

The class templates `auto_ptr`, `unary_function`, and `binary_function`,
the function templates `random_shuffle`, and the function templates (and
their return types) `ptr_fun`, `mem_fun`, `mem_fun_ref`, `bind1st`, and
`bind2nd` are not defined. Superseded by new features. Valid C++14 code
that uses these class templates and function templates may fail to
compile in this revision of C++.

Remove old iostreams members \[depr.ios.members\]. Redundant feature for
compatibility with pre-standard code has served its time. A valid C++14
program using these identifiers may be ill-formed in this revision of
C++.

## C++ and ISO C++11 <a id="diff.cpp11">[[diff.cpp11]]</a>

### General <a id="diff.cpp11.general">[[diff.cpp11.general]]</a>

Subclause [[diff.cpp11]] lists the differences between C++ and ISO C++11
(ISO/IEC 14882:2011, *Programming Languages --- C++*), in addition to
those listed above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp11.lex">[[diff.cpp11.lex]]</a>

*pp-number* can contain one or more single quotes. Necessary to enable
single quotes as digit separators. Valid C++11 code may fail to compile
or may change meaning in this revision of C++. For example, the
following code is valid both in C++11 and in this revision of C++, but
the macro invocation produces different outcomes because the single
quotes delimit a *character-literal* in C++11, whereas they are digit
separators in this revision of C++. For example:

``` cpp
#define M(x, ...) __VA_ARGS__
int x[2] = { M(1'2,3'4, 5) };
// int x[2] = { 5 \ \ \ \ \ } --- C++11
// int x[2] = { 3'4, 5 } --- this revision of \Cpp{}
```

###  [[basic]]: basics <a id="diff.cpp11.basic">[[diff.cpp11.basic]]</a>

New usual (non-placement) deallocator. Required for sized deallocation.
Valid C++11 code can declare a global placement allocation function and
deallocation function as follows:

``` cpp
void* operator new(std::size_t, std::size_t);
void operator delete(void*, std::size_t) noexcept;
```

In this revision of C++, however, the declaration of `operator delete`
might match a predefined usual (non-placement) `operator delete`
[[basic.stc.dynamic]]. If so, the program is ill-formed, as it was for
class member allocation functions and deallocation functions
[[expr.new]].

###  [[expr]]: expressions <a id="diff.cpp11.expr">[[diff.cpp11.expr]]</a>

A conditional expression with a throw expression as its second or third
operand keeps the type and value category of the other operand. Formerly
mandated conversions (lvalue-to-rvalue [[conv.lval]], array-to-pointer
[[conv.array]], and function-to-pointer [[conv.func]] standard
conversions), especially the creation of the temporary due to
lvalue-to-rvalue conversion, were considered gratuitous and surprising.
Valid C++11 code that relies on the conversions may behave differently
in this revision of C++. For example:

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

In C++11, `f(true)` returns `1`. In this revision of C++, it returns
`2`.

``` cpp
sizeof(true ? "" : throw 0)
```

In C++11, the expression yields `sizeof(const char*)`. In this revision
of C++, it yields `sizeof(const char[1])`.

###  [[dcl.dcl]]: declarations <a id="diff.cpp11.dcl.dcl">[[diff.cpp11.dcl.dcl]]</a>

`constexpr` non-static member functions are not implicitly `const`
member functions. Necessary to allow `constexpr` member functions to
mutate the object. Valid C++11 code may fail to compile in this revision
of C++. For example:

``` cpp
struct S {
  constexpr const int &f();
  int &f();
};
```

This code is valid in C++11 but invalid in this revision of C++ because
it declares the same member function twice with different return types.

Classes with default member initializers can be aggregates. Necessary to
allow default member initializers to be used by aggregate
initialization. Valid C++11 code may fail to compile or may change
meaning in this revision of C++. For example:

``` cpp
struct S {          // Aggregate in C++14 onwards.
  int m = 1;
};
struct X {
  operator int();
  operator S();
};
X a{};
S b{a};             // uses copy constructor in C++11,
                    // performs aggregate initialization in this revision of \Cpp{}
```

###  [[library]]: library introduction <a id="diff.cpp11.library">[[diff.cpp11.library]]</a>

New header. New functionality. The C++ header `<shared_mutex>` is new.
Valid C++11 code that `#include`s a header with that name may be invalid
in this revision of C++.

###  [[input.output]]: input/output library <a id="diff.cpp11.input.output">[[diff.cpp11.input.output]]</a>

`gets` is not defined. Use of `gets` is considered dangerous. Valid
C++11 code that uses the `gets` function may fail to compile in this
revision of C++.

## C++ and ISO C++03 <a id="diff.cpp03">[[diff.cpp03]]</a>

### General <a id="diff.cpp03.general">[[diff.cpp03.general]]</a>

Subclause [[diff.cpp03]] lists the differences between C++ and ISO C++03
(ISO/IEC 14882:2003, *Programming Languages --- C++*), in addition to
those listed above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.cpp03.lex">[[diff.cpp03.lex]]</a>

New kinds of *string-literal*s. Required for new features. Valid C++03
code may fail to compile or produce different results in this revision
of C++. Specifically, macros named `R`, `u8`, `u8R`, `u`, `uR`, `U`,
`UR`, or `LR` will not be expanded when adjacent to a *string-literal*
but will be interpreted as part of the *string-literal*. For example:

``` cpp
#define u8 "abc"
const char* s = u8"def";        // Previously "abcdef", now "def"
```

User-defined literal string support. Required for new features. Valid
C++03 code may fail to compile or produce different results in this
revision of C++. For example:

``` cpp
#define _x "there"
"hello"_x           // #1
```

Previously, \#1 would have consisted of two separate preprocessing
tokens and the macro `_x` would have been expanded. In this revision of
C++, \#1 consists of a single preprocessing token, so the macro is not
expanded.

New keywords. Required for new features. Added to [[lex.key]], the
following identifiers are new keywords: `alignas`, `alignof`,
`char16_t`, `char32_t`, `constexpr`, `decltype`, `noexcept`, `nullptr`,
`static_assert`, and `thread_local`. Valid C++03 code using these
identifiers is invalid in this revision of C++.

Type of integer literals. C99 compatibility. Certain integer literals
larger than can be represented by `long` could change from an unsigned
integer type to `signed long long`.

###  [[expr]]: expressions <a id="diff.cpp03.expr">[[diff.cpp03.expr]]</a>

Only literals are integer null pointer constants. Removing surprising
interactions with templates and constant expressions. Valid C++03 code
may fail to compile or produce different results in this revision of
C++. For example:

``` cpp
void f(void *);     // #1
void f(...);        // #2
template<int N> void g() {
  f(0*N);           // calls #2; used to call #1
}
```

Specify rounding for results of integer `/` and `%`. Increase
portability, C99 compatibility. Valid C++03 code that uses integer
division rounds the result toward 0 or toward negative infinity, whereas
this revision of C++ always rounds the result toward 0.

`&&` is valid in a *type-name*. Required for new features. Valid C++03
code may fail to compile or produce different results in this revision
of C++. For example:

``` cpp
bool b1 = new int && false;             // previously false, now ill-formed
struct S { operator int(); };
bool b2 = &S::operator int && false;    // previously false, now ill-formed
```

###  [[dcl.dcl]]: declarations <a id="diff.cpp03.dcl.dcl">[[diff.cpp03.dcl.dcl]]</a>

Remove `auto` as a storage class specifier. New feature. Valid C++03
code that uses the keyword `auto` as a storage class specifier may be
invalid in this revision of C++. In this revision of C++, `auto`
indicates that the type of a variable is to be deduced from its
initializer expression.

Narrowing restrictions in aggregate initializers. Catches bugs. Valid
C++03 code may fail to compile in this revision of C++. For example:

``` cpp
int x[] = { 2.0 };
```

This code is valid in C++03 but invalid in this revision of C++ because
`double` to `int` is a narrowing conversion.

###  [[class]]: classes <a id="diff.cpp03.class">[[diff.cpp03.class]]</a>

Implicitly-declared special member functions are defined as deleted when
the implicit definition would have been ill-formed. Improves template
argument deduction failure. A valid C++03 program that uses one of these
special member functions in a context where the definition is not
required (e.g., in an expression that is not potentially evaluated)
becomes ill-formed.

User-declared destructors have an implicit exception specification.
Clarification of destructor requirements. Valid C++03 code may execute
differently in this revision of C++. In particular, destructors that
throw exceptions will call `std::terminate` (without calling
`std::unexpected`) if their exception specification is non-throwing.

###  [[temp]]: templates <a id="diff.cpp03.temp">[[diff.cpp03.temp]]</a>

Repurpose `export` for modules
[[module]], [[cpp.module]], [[cpp.import]]. No implementation consensus
for the C++03 meaning of `export`. A valid C++03 program containing
`export` is ill-formed in this revision of C++.

Remove whitespace requirement for nested closing template right angle
brackets. Considered a persistent but minor annoyance. Template aliases
representing non-class types would exacerbate whitespace issues. Change
to semantics of well-defined expression. A valid C++03 expression
containing a right angle bracket (“`>`”) followed immediately by another
right angle bracket may now be treated as closing two templates. For
example:

``` cpp
template <class T> struct X { };
template <int N> struct Y { };
X< Y< 1 >> 2 > > x;
```

This code is valid in C++03 because “`>>`” is a right-shift operator,
but invalid in this revision of C++ because “`>>`” closes two templates.

Allow dependent calls of functions with internal linkage. Overly
constrained, simplify overload resolution rules. A valid C++03 program
can get a different result in this revision of C++.

###  [[library]]: library introduction <a id="diff.cpp03.library">[[diff.cpp03.library]]</a>

**Affected:** [[library]] – [[thread]] New reserved identifiers.
Required by new features. Valid C++03 code that uses any identifiers
added to the C++ standard library by later revisions of C++ may fail to
compile or produce different results in this revision of C++. A
comprehensive list of identifiers used by the C++ standard library can
be found in the Index of Library Names in this document.

New headers. New functionality. The following C++ headers are new:
`<array>`, `<atomic>`, `<chrono>`, , `<condition_variable>`,
`<forward_list>`, `<future>`, `<initializer_list>`, `<mutex>`,
`<random>`, `<ratio>`, `<regex>`, `<scoped_allocator>`,
`<system_error>`, `<thread>`, `<tuple>`, `<type\-index>`,
`<type_traits>`, `<unordered_map>`, and `<unordered_set>`. In addition
the following C compatibility headers are new: `<cfenv>`, `<cinttypes>`,
`<cstdint>`, and `<cuchar>`. Valid C++03 code that `#include`s headers
with these names may be invalid in this revision of C++.

Function `swap` moved to a different header Remove dependency on
`<algorithm>` for `swap`. Valid C++03 code that has been compiled
expecting swap to be in `<algorithm>` may have to instead include
`<utility>`.

New reserved namespace. New functionality. The global namespace `posix`
is now reserved for standardization. Valid C++03 code that uses a
top-level namespace `posix` may be invalid in this revision of C++.

Additional restrictions on macro names. Avoid hard to diagnose or
non-portable constructs. Names of attribute identifiers may not be used
as macro names. Valid C++03 code that defines `override`, `final`,
`carries_dependency`, or `noreturn` as macros is invalid in this
revision of C++.

###  [[support]]: language support library <a id="diff.cpp03.language.support">[[diff.cpp03.language.support]]</a>

`operator new` may throw exceptions other than `std::bad_alloc`.
Consistent application of `noexcept`. Valid C++03 code that assumes that
global `operator new` only throws `std::bad_alloc` may execute
differently in this revision of C++. Valid C++03 code that replaces the
global replaceable `operator new` is ill-formed in this revision of C++,
because the exception specification of `throw(std::bad_alloc)` was
removed.

###  [[diagnostics]]: diagnostics library <a id="diff.cpp03.diagnostics">[[diff.cpp03.diagnostics]]</a>

Thread-local error numbers. Support for new thread facilities. Valid but
implementation-specific C++03 code that relies on `errno` being the same
across threads may change behavior in this revision of C++.

###  [[utilities]]: general utilities library <a id="diff.cpp03.utilities">[[diff.cpp03.utilities]]</a>

Standard function object types no longer derived from
`std::unary_function` or `std::binary_function`. Superseded by new
feature; `unary_function` and `binary_function` are no longer defined.
Valid C++03 code that depends on function object types being derived
from `unary_function` or `binary_function` may fail to compile in this
revision of C++.

###  [[strings]]: strings library <a id="diff.cpp03.strings">[[diff.cpp03.strings]]</a>

`basic_string` requirements no longer allow reference-counted strings.
Invalidation is subtly different with reference-counted strings. This
change regularizes behavior. Valid C++03 code may execute differently in
this revision of C++.

Loosen `basic_string` invalidation rules. Allow small-string
optimization. Valid C++03 code may execute differently in this revision
of C++. Some `const` member functions, such as `data` and `c_str`, no
longer invalidate iterators.

###  [[containers]]: containers library <a id="diff.cpp03.containers">[[diff.cpp03.containers]]</a>

Complexity of `size()` member functions now constant. Lack of
specification of complexity of `size()` resulted in divergent
implementations with inconsistent performance characteristics. Some
container implementations that conform to C++03 may not conform to the
specified `size()` requirements in this revision of C++. Adjusting
containers such as `std::list` to the stricter requirements may require
incompatible changes.

Requirements change: relaxation. Clarification. Valid C++03 code that
attempts to meet the specified container requirements may now be
over-specified. Code that attempted to be portable across containers may
need to be adjusted as follows:

- not all containers provide `size()`; use `empty()` instead of
  `size() == 0`;
- not all containers are empty after construction (`array`);
- not all containers have constant complexity for `swap()` (`array`).

Requirements change: default constructible. Clarification of container
requirements. Valid C++03 code that attempts to explicitly instantiate a
container using a user-defined type with no default constructor may fail
to compile.

Signature changes: from `void` return types. Old signature threw away
useful information that may be expensive to recalculate. The following
member functions have changed:

- `erase(iter)` for `set`, `multiset`, `map`, `multimap`
- `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`
- `insert(pos, num, val)` for `vector`, `deque`, `list`, `forward_list`
- `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`

Valid C++03 code that relies on these functions returning `void` (e.g.,
code that creates a pointer to member function that points to one of
these functions) will fail to compile with this revision of C++.

Signature changes: from `iterator` to `const_iterator` parameters.
Overspecification. The signatures of the following member functions
changed from taking an `iterator` to taking a `const_iterator`:

- `insert(iter, val)` for `vector`, `deque`, `list`, `set`, `multiset`,
  `map`, `multimap`
- `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`
- `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`
- all forms of `list::splice`
- all forms of `list::merge`

Valid C++03 code that uses these functions may fail to compile with this
revision of C++.

Signature changes: `resize`. Performance, compatibility with move
semantics. For `vector`, `deque`, and `list` the fill value passed to
`resize` is now passed by reference instead of by value, and an
additional overload of `resize` has been added. Valid C++03 code that
uses this function may fail to compile with this revision of C++.

###  [[algorithms]]: algorithms library <a id="diff.cpp03.algorithms">[[diff.cpp03.algorithms]]</a>

Result state of inputs after application of some algorithms. Required by
new feature. A valid C++03 program may detect that an object with a
valid but unspecified state has a different valid but unspecified state
with this revision of C++. For example, `std::remove` and
`std::remove_if` may leave the tail of the input sequence with a
different set of values than previously.

###  [[numerics]]: numerics library <a id="diff.cpp03.numerics">[[diff.cpp03.numerics]]</a>

Specified representation of complex numbers. Compatibility with C99.
Valid C++03 code that uses implementation-specific knowledge about the
binary representation of the required template specializations of
`std::complex` may not be compatible with this revision of C++.

###  [[localization]]: localization library <a id="diff.cpp03.locale">[[diff.cpp03.locale]]</a>

The `num_get` facet recognizes hexadecimal floating point values.
Required by new feature. Valid C++03 code may have different behavior in
this revision of C++.

###  [[input.output]]: input/output library <a id="diff.cpp03.input.output">[[diff.cpp03.input.output]]</a>

Specify use of `explicit` in existing boolean conversion functions.
Clarify intentions, avoid workarounds. Valid C++03 code that relies on
implicit boolean conversions will fail to compile with this revision of
C++. Such conversions occur in the following conditions:

- passing a value to a function that takes an argument of type `bool`;
- using `operator==` to compare to `false` or `true`;
- returning a value from a function with a return type of `bool`;
- initializing members of type `bool` via aggregate initialization;
- initializing a `const bool&` which would bind to a temporary object.

Change base class of `std::ios_base::failure`. More detailed error
messages. `std::ios_base::failure` is no longer derived directly from
`std::exception`, but is now derived from `std::system_error`, which in
turn is derived from `std::runtime_error`. Valid C++03 code that assumes
that `std::ios_base::failure` is derived directly from `std::exception`
may execute differently in this revision of C++.

Flag types in `std::ios_base` are now bitmasks with values defined as
constexpr static members. Required for new features. Valid C++03 code
that relies on `std::ios_base` flag types being represented as
`std::bitset` or as an integer type may fail to compile with this
revision of C++. For example:

``` cpp
#include <iostream>

int main() {
  int flag = std::ios_base::hex;
  std::cout.setf(flag);         // error: setf does not take argument of type int
}
```

## C++ and ISO C <a id="diff.iso">[[diff.iso]]</a>

### General <a id="diff.iso.general">[[diff.iso.general]]</a>

Subclause [[diff.iso]] lists the differences between C++ and ISO C, in
addition to those listed above, by the chapters of this document.

###  [[lex]]: lexical conventions <a id="diff.lex">[[diff.lex]]</a>

New Keywords  
New keywords are added to C++; see [[lex.key]]. These keywords were
added in order to implement the new semantics of C++. Change to
semantics of well-defined feature. Any ISO C programs that used any of
these keywords as identifiers are not valid C++ programs. Syntactic
transformation. Converting one specific program is easy. Converting a
large collection of related programs takes more work. Common.

Type of *character-literal* is changed from `int` to `char`. This is
needed for improved overloaded function argument type matching. For
example:

``` cpp
int function( int i );
int function( char c );

function( 'x' );
```

It is preferable that this call match the second version of function
rather than the first. Change to semantics of well-defined feature. ISO
C programs which depend on

``` cpp
sizeof('x') == sizeof(int)
```

will not work the same as C++ programs. Simple. Programs which depend
upon `sizeof('x')` are probably rare.

Concatenated *string-literal*s can no longer have conflicting
*encoding-prefix*es. Removal of non-portable feature. Concatenation of
*string-literal*s with different *encoding-prefix*es is now ill-formed.
Syntactic transformation. Seldom.

String literals made const.  
The type of a *string-literal* is changed from “array of `char`” to
“array of `const char`”. The type of a UTF-8 string literal is changed
from “array of `char`” to “array of `const char8_t`”. The type of a
UTF-16 string literal is changed from “array of *some-integer-type*” to
“array of `const char16_t`”. The type of a UTF-32 string literal is
changed from “array of *some-integer-type*” to “array of
`const char32_t`”. The type of a wide string literal is changed from
“array of `wchar_t`” to “array of `const wchar_t`”. This avoids calling
an inappropriate overloaded function, which might expect to be able to
modify its argument. Change to semantics of well-defined feature.
Syntactic transformation. The fix is to add a cast:

``` cpp
char* p = "abc";                // valid in C, invalid in \Cpp{}
void f(char*) {
  char* p = (char*)"abc";       // OK, cast added
  f(p);
  f((char*)"def");              // OK, cast added
}
```

Programs that have a legitimate reason to treat string literal objects
as potentially modifiable memory are probably rare.

###  [[basic]]: basics <a id="diff.basic">[[diff.basic]]</a>

C++ does not have “tentative definitions” as in C.  
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

This avoids having different initialization rules for fundamental types
and user-defined types. Deletion of semantically well-defined feature.
Semantic transformation. In C++, the initializer for one of a set of
mutually-referential file-local objects with static storage duration
must invoke a function call to achieve the initialization. Seldom.

A `struct` is a scope in C++, not in C. For example,

``` cpp
struct X {
  struct Y { int a; } b;
};
struct Y c;
```

is valid in C but not in C++, which would require `X::Y c;`. Class scope
is crucial to C++, and a struct is a class. Change to semantics of
well-defined feature. Semantic transformation. C programs use `struct`
extremely frequently, but the change is only noticeable when `struct`,
enumeration, or enumerator names are referred to outside the `struct`.
The latter is probably rare.

\[also [[dcl.type]]\] A name of file scope that is explicitly declared
`const`, and not explicitly declared `extern`, has internal linkage,
while in C it would have external linkage. Because const objects may be
used as values during translation in C++, this feature urges programmers
to provide an explicit initializer for each const object. This feature
allows the user to put const objects in source files that are included
in more than one translation unit. Change to semantics of well-defined
feature. Semantic transformation. Seldom.

The `main` function cannot be called recursively and cannot have its
address taken. The `main` function may require special actions. Deletion
of semantically well-defined feature. Trivial: create an intermediary
function such as `mymain(argc, argv)`. Seldom.

C allows “compatible types” in several places, C++ does not.  
For example, otherwise-identical `struct` types with different tag names
are “compatible” in C but are distinctly different types in C++.
Stricter type checking is essential for C++. Deletion of semantically
well-defined feature. Semantic transformation. The “typesafe linkage”
mechanism will find many, but not all, of such problems. Those problems
not found by typesafe linkage will continue to function properly,
according to the “layout compatibility rules” of this document. Common.

###  [[expr]]: expressions <a id="diff.expr">[[diff.expr]]</a>

Converting `void*` to a pointer-to-object type requires casting.

``` cpp
char a[10];
void* b=a;
void foo() {
  char* c=b;
}
```

ISO C accepts this usage of pointer to `void` being assigned to a
pointer to object type. C++ does not. C++ tries harder than C to enforce
compile-time type safety. Deletion of semantically well-defined feature.
Can be automated. Violations will be diagnosed by the C++ translator.
The fix is to add a cast. For example:

``` cpp
char* c = (char*) b;
```

This is fairly widely used but it is good programming practice to add
the cast when assigning pointer-to-void to pointer-to-object. Some ISO C
translators will give a warning if the cast is not used.

Decrement operator is not allowed with `bool` operand. Feature with
surprising semantics. A valid ISO C expression utilizing the decrement
operator on a `bool` lvalue (for instance, via the C typedef in
`<stdbool.h>`) is ill-formed in C++.

In C++, types can only be defined in declarations, not in expressions.  
In C, a `sizeof` expression or cast expression may define a new type.
For example,

``` cpp
p = (void*)(struct x {int i;} *)0;
```

defines a new type, struct `x`. This prohibition helps to clarify the
location of definitions in the source code. Deletion of semantically
well-defined feature. Syntactic transformation. Seldom.

The result of a conditional expression, an assignment expression, or a
comma expression may be an lvalue. C++ is an object-oriented language,
placing relatively more emphasis on lvalues. For example, function calls
may yield lvalues. Change to semantics of well-defined feature. Some C
expressions that implicitly rely on lvalue-to-rvalue conversions will
yield different results. For example,

``` cpp
char arr[100];
sizeof(0, arr)
```

yields `100` in C++ and `sizeof(char*)` in C. Programs must add explicit
casts to the appropriate rvalue. Rare.

###  [[stmt.stmt]]: statements <a id="diff.stat">[[diff.stat]]</a>

It is now invalid to jump past a declaration with explicit or implicit
initializer (except across entire block not entered). Constructors used
in initializers may allocate resources which need to be de-allocated
upon leaving the block. Allowing jump past initializers would require
complicated runtime determination of allocation. Furthermore, many
operations on such an uninitialized object have undefined behavior. With
this simple compile-time rule, C++ assures that if an initialized
variable is in scope, then it has assuredly been initialized. Deletion
of semantically well-defined feature. Semantic transformation. Seldom.

It is now invalid to return (explicitly or implicitly) from a function
which is declared to return a value without actually returning a value.
The caller and callee may assume fairly elaborate return-value
mechanisms for the return of class objects. If some flow paths execute a
return without specifying any value, the implementation must embody many
more complications. Besides, promising to return a value of a given
type, and then not returning such a value, has always been recognized to
be a questionable practice, tolerated only because very-old C had no
distinction between functions with `void` and `int` return types.
Deletion of semantically well-defined feature. Semantic transformation.
Add an appropriate return value to the source code, such as zero.
Seldom. For several years, many existing C implementations have produced
warnings in this case.

###  [[dcl.dcl]]: declarations <a id="diff.dcl">[[diff.dcl]]</a>

In C++, the `static` or `extern` specifiers can only be applied to names
of objects or functions.  
Using these specifiers with type declarations is illegal in C++. In C,
these specifiers are ignored when used on type declarations.

Example:

``` cpp
static struct S {               // valid C, invalid in \Cpp{}
  int i;
};
```

Storage class specifiers don’t have any meaning when associated with a
type. In C++, class members can be declared with the `static` storage
class specifier. Storage class specifiers on type declarations can be
confusing for users. Deletion of semantically well-defined feature.
Syntactic transformation. Seldom.

In C++, `register` is not a storage class specifier. The storage class
specifier had no effect in C++. Deletion of semantically well-defined
feature. Syntactic transformation. Common.

A C++ *typedef-name* must be different from any class type name declared
in the same scope (except if the typedef is a synonym of the class name
with the same name). In C, a *typedef-name* and a struct tag name
declared in the same scope can have the same name (because they have
different name spaces).

Example:

``` cpp
typedef struct name1 { ... } name1;         // valid C and \Cpp{}
struct name { ... };
typedef int name;               // valid C, invalid \Cpp{}
```

For ease of use, C++ doesn’t require that a type name be prefixed with
the keywords `class`, `struct` or `union` when used in object
declarations or type casts.

Example:

``` cpp
class name { ... };
name i;                         // i has type class name
```

Deletion of semantically well-defined feature. Semantic transformation.
One of the 2 types has to be renamed. Seldom.

\[see also [[basic.link]]\] Const objects must be initialized in C++ but
can be left uninitialized in C. A const object cannot be assigned to so
it must be initialized to hold a useful value. Deletion of semantically
well-defined feature. Semantic transformation. Seldom.

The keyword `auto` cannot be used as a storage class specifier.

Example:

``` cpp
void f() {
  auto int x;       // valid C, invalid \Cpp{}
}
```

Allowing the use of `auto` to deduce the type of a variable from its
initializer results in undesired interpretations of `auto` as a storage
class specifier in certain contexts. Deletion of semantically
well-defined feature. Syntactic transformation. Rare.

In C++, a function declared with an empty parameter list takes no
arguments. In C, an empty parameter list means that the number and type
of the function arguments are unknown.

Example:

``` cpp
int f();            // means   int f(void) in \Cpp{}
                    // int f( unknown ) in C
```

This is to avoid erroneous function calls (i.e., function calls with the
wrong number or type of arguments). Change to semantics of well-defined
feature. This feature was marked as “obsolescent” in C. Syntactic
transformation. The function declarations using C incomplete declaration
style must be completed to become full prototype declarations. A program
may need to be updated further if different calls to the same
(non-prototype) function have different numbers of arguments or if the
type of corresponding arguments differed. Common.

\[see [[expr.sizeof]]\] In C++, types may not be defined in return or
parameter types. In C, these type definitions are allowed.

Example:

``` cpp
void f( struct S { int a; } arg ) {}    // valid C, invalid \Cpp{}
enum E { A, B, C } f() {}               // valid C, invalid \Cpp{}
```

When comparing types in different translation units, C++ relies on name
equivalence when C relies on structural equivalence. Regarding parameter
types: since the type defined in a parameter list would be in the scope
of the function, the only legal calls in C++ would be from within the
function itself. Deletion of semantically well-defined feature. Semantic
transformation. The type definitions must be moved to file scope, or in
header files. Seldom. This style of type definition is seen as poor
coding style.

In C++, the syntax for function definition excludes the “old-style” C
function. In C, “old-style” syntax is allowed, but deprecated as
“obsolescent”. Prototypes are essential to type safety. Deletion of
semantically well-defined feature. Syntactic transformation. Common in
old programs, but already known to be obsolescent.

In C++, designated initialization support is restricted compared to the
corresponding functionality in C. In C++, designators for non-static
data members must be specified in declaration order, designators for
array elements and nested designators are not supported, and designated
and non-designated initializers cannot be mixed in the same initializer
list.

Example:

``` cpp
struct A { int x, y; };
struct B { struct A a; };
struct A a = {.y = 1, .x = 2};  // valid C, invalid \Cpp{}
int arr[3] = {[1] = 5};         // valid C, invalid \Cpp{}
struct B b = {.a.x = 0};        // valid C, invalid \Cpp{}
struct A c = {.x = 1, 2};       // valid C, invalid \Cpp{}
```

In C++, members are destroyed in reverse construction order and the
elements of an initializer list are evaluated in lexical order, so field
initializers must be specified in order. Array designators conflict with
*lambda-expression* syntax. Nested designators are seldom used. Deletion
of feature that is incompatible with C++. Syntactic transformation.
Out-of-order initializers are common. The other features are seldom
used.

In C++, when initializing an array of character with a string, the
number of characters in the string (including the terminating `'\0'`)
must not exceed the number of elements in the array. In C, an array can
be initialized with a string even if the array is not large enough to
contain the string-terminating `'\0'`.

Example:

``` cpp
char array[4] = "abcd";         // valid C, invalid \Cpp{}
```

When these non-terminated arrays are manipulated by standard string
functions, there is potential for major catastrophe. Deletion of
semantically well-defined feature. Semantic transformation. The arrays
must be declared one element bigger to contain the string terminating
`'\0'`. Seldom. This style of array initialization is seen as poor
coding style.

C++ objects of enumeration type can only be assigned values of the same
enumeration type. In C, objects of enumeration type can be assigned
values of any integral type.

Example:

``` cpp
enum color { red, blue, green };
enum color c = 1;               // valid C, invalid \Cpp{}
```

The type-safe nature of C++. Deletion of semantically well-defined
feature. Syntactic transformation. (The type error produced by the
assignment can be automatically corrected by applying an explicit cast.)
Common.

In C++, the type of an enumerator is its enumeration. In C, the type of
an enumerator is `int`.

Example:

``` cpp
enum e { A };
sizeof(A) == sizeof(int)        // in C
sizeof(A) == sizeof(e)          // in \Cpp{}
/* and sizeof(int) is not necessarily equal to sizeof(e) */
```

In C++, an enumeration is a distinct type. Change to semantics of
well-defined feature. Semantic transformation. Seldom. The only time
this affects existing C code is when the size of an enumerator is taken.
Taking the size of an enumerator is not a common C coding practice.

In C++, an *alignment-specifier* is an *attribute-specifier*. In C, an
*alignment-specifier* is a .

Example:

``` cpp
#include <stdalign.h>
unsigned alignas(8) int x;      // valid C, invalid \Cpp{}
unsigned int y alignas(8);      // valid \Cpp{}, invalid C
```

C++ requires unambiguous placement of the *alignment-specifier*.
Deletion of semantically well-defined feature. Syntactic transformation.
Seldom.

###  [[class]]: classes <a id="diff.class">[[diff.class]]</a>

\[see also [[dcl.typedef]]\] In C++, a class declaration introduces the
class name into the scope where it is declared and hides any object,
function or other declaration of that name in an enclosing scope. In C,
an inner scope declaration of a struct tag name never hides the name of
an object or function in an outer scope.

Example:

``` cpp
int x[99];
void f() {
  struct x { int a; };
  sizeof(x);  /* size of the array in C */
  /* size of the struct in \textit{\textrm{\Cpp{}}} */
}
```

This is one of the few incompatibilities between C and C++ that can be
attributed to the new C++ name space definition where a name can be
declared as a type and as a non-type in a single scope causing the
non-type name to hide the type name and requiring that the keywords
`class`, `struct`, `union` or `enum` be used to refer to the type name.
This new name space definition provides important notational
conveniences to C++ programmers and helps making the use of the
user-defined types as similar as possible to the use of fundamental
types. The advantages of the new name space definition were judged to
outweigh by far the incompatibility with C described above. Change to
semantics of well-defined feature. Semantic transformation. If the
hidden name that needs to be accessed is at global scope, the `::` C++
operator can be used. If the hidden name is at block scope, either the
type or the struct tag has to be renamed. Seldom.

Copying volatile objects.

The implicitly-declared copy constructor and implicitly-declared copy
assignment operator cannot make a copy of a volatile lvalue. For
example, the following is valid in ISO C:

``` cpp
struct X { int i; };
volatile struct X x1 = {0};
struct X x2 = x1;               // invalid \Cpp{}
struct X x3;
x3 = x1;                        // also invalid \Cpp{}
```

Several alternatives were debated at length. Changing the parameter to
`volatile` `const` `X&` would greatly complicate the generation of
efficient code for class objects. Discussion of providing two
alternative signatures for these implicitly-defined operations raised
unanswered concerns about creating ambiguities and complicating the
rules that specify the formation of these operators according to the
bases and members. Deletion of semantically well-defined feature.
Semantic transformation. If volatile semantics are required for the
copy, a user-declared constructor or assignment must be provided. If
non-volatile semantics are required, an explicit `const_cast` can be
used. Seldom.

Bit-fields of type plain `int` are signed. The signedness needs to be
consistent among template specializations. For consistency, the
implementation freedom was eliminated for non-dependent types, too. The
choice is implementation-defined in C, but not so in C++. Syntactic
transformation. Seldom.

In C++, the name of a nested class is local to its enclosing class. In C
the name of the nested class belongs to the same scope as the name of
the outermost enclosing class.

Example:

``` cpp
struct X {
  struct Y { ... } y;
};
struct Y yy;                    // valid C, invalid \Cpp{}
```

C++ classes have member functions which require that classes establish
scopes. The C rule would leave classes as an incomplete scope mechanism
which would prevent C++ programmers from maintaining locality within a
class. A coherent set of scope rules for C++ based on the C rule would
be very complicated and C++ programmers would be unable to predict
reliably the meanings of nontrivial examples involving nested or local
functions. Change to semantics of well-defined feature. Semantic
transformation. To make the struct type name visible in the scope of the
enclosing struct, the struct tag can be declared in the scope of the
enclosing struct, before the enclosing struct is defined. Example:

``` cpp
struct Y;                       // struct Y and struct X are at the same scope
struct X {
  struct Y { ... } y;
};
```

All the definitions of C struct types enclosed in other struct
definitions and accessed outside the scope of the enclosing struct can
be exported to the scope of the enclosing struct. Note: this is a
consequence of the difference in scope rules, which is documented in
[[basic.scope]]. Seldom.

In C++, a *typedef-name* may not be redeclared in a class definition
after being used in that definition.

Example:

``` cpp
typedef int I;
struct S {
  I i;
  int I;            // valid C, invalid \Cpp{}
};
```

When classes become complicated, allowing such a redefinition after the
type has been used can create confusion for C++ programmers as to what
the meaning of `I` really is. Deletion of semantically well-defined
feature. Semantic transformation. Either the type or the struct member
has to be renamed. Seldom.

###  [[cpp]]: preprocessing directives <a id="diff.cpp">[[diff.cpp]]</a>

Whether `__STDC__` is defined and if so, what its value is, are
*implementation-defined*. C++ is not identical to ISO C. Mandating that
`__STDC__` be defined would require that translators make an incorrect
claim. Change to semantics of well-defined feature. Semantic
transformation. Programs and headers that reference `__STDC__` are quite
common.

## C standard library <a id="diff.library">[[diff.library]]</a>

### General <a id="diff.library.general">[[diff.library.general]]</a>

Subclause [[diff.library]] summarizes the explicit changes in headers,
definitions, declarations, or behavior between the C standard library in
the C standard and the parts of the C++ standard library that were
included from the C standard library.

### Modifications to headers <a id="diff.mods.to.headers">[[diff.mods.to.headers]]</a>

For compatibility with the C standard library, the C++ standard library
provides the C headers enumerated in  [[support.c.headers]].

There are no C++ headers for the C standard library’s headers and , nor
are these headers from the C standard library headers themselves part of
C++.

The C headers `<complex.h>` and `<tgmath.h>` do not contain any of the
content from the C standard library and instead merely include other
headers from the C++ standard library.

### Modifications to definitions <a id="diff.mods.to.definitions">[[diff.mods.to.definitions]]</a>

#### Types `char16_t` and `char32_t` <a id="diff.char16">[[diff.char16]]</a>

The types `char16_t` and `char32_t` are distinct types rather than
typedefs to existing integral types. The tokens `char16_t` and
`char32_t` are keywords in C++ [[lex.key]]. They do not appear as macro
or type names defined in `<cuchar>`.

#### Type `wchar_t` <a id="diff.wchar.t">[[diff.wchar.t]]</a>

The type `wchar_t` is a distinct type rather than a typedef to an
existing integral type. The token `wchar_t` is a keyword in C++
[[lex.key]]. It does not appear as a macro or type name defined in any
of `<cstddef>`, `<cstdlib>`, or `<cwchar>`.

#### Header `<assert.h>` <a id="diff.header.assert.h">[[diff.header.assert.h]]</a>

The token `static_assert` is a keyword in C++. It does not appear as a
macro name defined in `<cassert>`.

#### Header `<iso646.h>` <a id="diff.header.iso646.h">[[diff.header.iso646.h]]</a>

The tokens `and`, `and_eq`, `bitand`, `bitor`, `compl`, `not`, `not_eq`,
`or`, `or_eq`, `xor`, and `xor_eq` are keywords in C++ [[lex.key]], and
are not introduced as macros by `<iso646.h>`.

#### Header `<stdalign.h>` <a id="diff.header.stdalign.h">[[diff.header.stdalign.h]]</a>

The token `alignas` is a keyword in C++ [[lex.key]], and is not
introduced as a macro by `<stdalign.h>`.

#### Header `<stdbool.h>` <a id="diff.header.stdbool.h">[[diff.header.stdbool.h]]</a>

The tokens `bool`, `true`, and `false` are keywords in C++ [[lex.key]],
and are not introduced as macros by `<stdbool.h>`.

#### Macro `NULL` <a id="diff.null">[[diff.null]]</a>

The macro `NULL`, defined in any of `<clocale>`, `<cstddef>`,
`<cstdio>`, `<cstdlib>`, `<cstring>`, `<ctime>`, or `<cwchar>`, is an
*implementation-defined* null pointer constant in C++ [[support.types]].

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

Header `<cstddef>` declares the names `nullptr_t`, `byte`, and
`to_integer`, and the operators and operator templates in
[[support.types.byteops]], in addition to the names declared in
`<stddef.h>` in the C standard library.

### Modifications to behavior <a id="diff.mods.to.behavior">[[diff.mods.to.behavior]]</a>

#### General <a id="diff.mods.to.behavior.general">[[diff.mods.to.behavior.general]]</a>

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
of `type` arguments in C++. Subclause [[support.types.layout]] describes
the change.

#### Memory allocation functions <a id="diff.malloc">[[diff.malloc]]</a>

The functions `aligned_alloc`, `calloc`, `malloc`, and `realloc` are
restricted in C++. Subclause [[c.malloc]] describes the changes.

<!-- Section link definitions -->
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
[diff.cpp03.general]: #diff.cpp03.general
[diff.cpp03.input.output]: #diff.cpp03.input.output
[diff.cpp03.language.support]: #diff.cpp03.language.support
[diff.cpp03.lex]: #diff.cpp03.lex
[diff.cpp03.library]: #diff.cpp03.library
[diff.cpp03.locale]: #diff.cpp03.locale
[diff.cpp03.numerics]: #diff.cpp03.numerics
[diff.cpp03.strings]: #diff.cpp03.strings
[diff.cpp03.temp]: #diff.cpp03.temp
[diff.cpp03.utilities]: #diff.cpp03.utilities
[diff.cpp11]: #diff.cpp11
[diff.cpp11.basic]: #diff.cpp11.basic
[diff.cpp11.dcl.dcl]: #diff.cpp11.dcl.dcl
[diff.cpp11.expr]: #diff.cpp11.expr
[diff.cpp11.general]: #diff.cpp11.general
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
[diff.cpp14.general]: #diff.cpp14.general
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
[diff.cpp17.general]: #diff.cpp17.general
[diff.cpp17.input.output]: #diff.cpp17.input.output
[diff.cpp17.iterators]: #diff.cpp17.iterators
[diff.cpp17.lex]: #diff.cpp17.lex
[diff.cpp17.library]: #diff.cpp17.library
[diff.cpp17.over]: #diff.cpp17.over
[diff.cpp17.temp]: #diff.cpp17.temp
[diff.cpp20]: #diff.cpp20
[diff.cpp20.concepts]: #diff.cpp20.concepts
[diff.cpp20.containers]: #diff.cpp20.containers
[diff.cpp20.dcl]: #diff.cpp20.dcl
[diff.cpp20.expr]: #diff.cpp20.expr
[diff.cpp20.general]: #diff.cpp20.general
[diff.cpp20.lex]: #diff.cpp20.lex
[diff.cpp20.library]: #diff.cpp20.library
[diff.cpp20.memory]: #diff.cpp20.memory
[diff.cpp20.stmt]: #diff.cpp20.stmt
[diff.cpp20.strings]: #diff.cpp20.strings
[diff.cpp20.temp]: #diff.cpp20.temp
[diff.cpp20.thread]: #diff.cpp20.thread
[diff.cpp20.utilities]: #diff.cpp20.utilities
[diff.dcl]: #diff.dcl
[diff.expr]: #diff.expr
[diff.header.assert.h]: #diff.header.assert.h
[diff.header.iso646.h]: #diff.header.iso646.h
[diff.header.stdalign.h]: #diff.header.stdalign.h
[diff.header.stdbool.h]: #diff.header.stdbool.h
[diff.iso]: #diff.iso
[diff.iso.general]: #diff.iso.general
[diff.lex]: #diff.lex
[diff.library]: #diff.library
[diff.library.general]: #diff.library.general
[diff.malloc]: #diff.malloc
[diff.mods.to.behavior]: #diff.mods.to.behavior
[diff.mods.to.behavior.general]: #diff.mods.to.behavior.general
[diff.mods.to.declarations]: #diff.mods.to.declarations
[diff.mods.to.definitions]: #diff.mods.to.definitions
[diff.mods.to.headers]: #diff.mods.to.headers
[diff.null]: #diff.null
[diff.offsetof]: #diff.offsetof
[diff.stat]: #diff.stat
[diff.wchar.t]: #diff.wchar.t

<!-- Link reference definitions -->
[algorithms]: algorithms.md#algorithms
[basic]: basic.md#basic
[basic.link]: basic.md#basic.link
[basic.scope]: basic.md#basic.scope
[basic.stc.dynamic]: basic.md#basic.stc.dynamic
[c.malloc]: mem.md#c.malloc
[class]: class.md#class
[class.temporary]: basic.md#class.temporary
[concepts]: concepts.md#concepts
[containers]: containers.md#containers
[conv.array]: expr.md#conv.array
[conv.func]: expr.md#conv.func
[conv.lval]: expr.md#conv.lval
[cpp]: cpp.md#cpp
[cpp.import]: cpp.md#cpp.import
[cpp.module]: cpp.md#cpp.module
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
[diagnostics]: diagnostics.md#diagnostics
[diff.cpp03]: #diff.cpp03
[diff.cpp11]: #diff.cpp11
[diff.cpp14]: #diff.cpp14
[diff.cpp17]: #diff.cpp17
[diff.cpp20]: #diff.cpp20
[diff.iso]: #diff.iso
[diff.library]: #diff.library
[except]: except.md#except
[expr]: expr.md#expr
[expr.eq]: expr.md#expr.eq
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
[localization]: localization.md#localization
[mem]: mem.md#mem
[module]: module.md#module
[numerics]: numerics.md#numerics
[over]: over.md#over
[stmt.stmt]: stmt.md#stmt.stmt
[strings]: strings.md#strings
[support]: support.md#support
[support.c.headers]: support.md#support.c.headers
[support.start.term]: support.md#support.start.term
[support.types]: support.md#support.types
[support.types.byteops]: support.md#support.types.byteops
[support.types.layout]: support.md#support.types.layout
[temp]: temp.md#temp
[temp.concept]: temp.md#temp.concept
[temp.pre]: temp.md#temp.pre
[thread]: thread.md#thread
[utilities]: utilities.md#utilities
