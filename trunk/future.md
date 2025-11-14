## General <a id="depr.general">[[depr.general]]</a>

This Annex describes features of this document that are specified for
compatibility with existing implementations.

These are deprecated features, where *deprecated* is defined as:
Normative for the current revision of C++, but having been identified as
a candidate for removal from future revisions. An implementation may
declare library names and entities described in this Clause with the
`deprecated` attribute [[dcl.attr.deprecated]].

## Non-local use of TU-local entities <a id="depr.local">[[depr.local]]</a>

A declaration of a non-TU-local entity that is an exposure
[[basic.link]] is deprecated.

[*Note 1*: Such a declaration in an importable module unit is
ill-formed. — *end note*]

[*Example 1*:

``` cpp
namespace {
  struct A {
    void f() {}
  };
}
A h();                          // deprecated: not internal linkage
inline void g() {A().f();}      // deprecated: inline and not internal linkage
```

— *end example*]

## Implicit capture of `*this` by reference <a id="depr.capture.this">[[depr.capture.this]]</a>

For compatibility with prior revisions of C++, a *lambda-expression*
with *capture-default* `=` [[expr.prim.lambda.capture]] may implicitly
capture `*this` by reference.

[*Example 1*:

``` cpp
struct X {
  int x;
  void foo(int n) {
    auto f = [=]() { x = n; };          // deprecated: x means this->x, not a copy thereof
    auto g = [=, this]() { x = n; };    // recommended replacement
  }
};
```

— *end example*]

## Deprecated `volatile` types <a id="depr.volatile.type">[[depr.volatile.type]]</a>

Postfix `++` and `--` expressions [[expr.post.incr]] and prefix `++` and
`--` expressions [[expr.pre.incr]] of volatile-qualified arithmetic and
pointer types are deprecated.

[*Example 1*:

``` cpp
volatile int velociraptor;
++velociraptor;                     // deprecated
```

— *end example*]

Certain assignments where the left operand is a volatile-qualified
non-class type are deprecated; see  [[expr.assign]].

[*Example 2*:

``` cpp
int neck, tail;
volatile int brachiosaur;
brachiosaur = neck;                 // OK
tail = brachiosaur;                 // OK
tail = brachiosaur = neck;          // deprecated
brachiosaur += neck;                // OK
```

— *end example*]

A function type [[dcl.fct]] with a parameter with volatile-qualified
type or with a volatile-qualified return type is deprecated.

[*Example 3*:

``` cpp
volatile struct amber jurassic();                               // deprecated
void trex(volatile short left_arm, volatile short right_arm);   // deprecated
void fly(volatile struct pterosaur* pteranodon);                // OK
```

— *end example*]

A structured binding [[dcl.struct.bind]] of a volatile-qualified type is
deprecated.

[*Example 4*:

``` cpp
struct linhenykus { short forelimb; };
void park(linhenykus alvarezsauroid) {
  volatile auto [what_is_this] = alvarezsauroid;                // deprecated
  // ...
}
```

— *end example*]

## Non-comma-separated ellipsis parameters <a id="depr.ellipsis.comma">[[depr.ellipsis.comma]]</a>

A *parameter-declaration-clause* of the form
*parameter-declaration-list* `...` is deprecated [[dcl.fct]].

[*Example 1*:

``` cpp
void f(int...);         // deprecated
void g(auto...);        // OK, declares a function parameter pack
void h(auto......);     // deprecated
```

— *end example*]

## Implicit declaration of copy functions <a id="depr.impldec">[[depr.impldec]]</a>

The implicit definition of a copy constructor [[class.copy.ctor]] as
defaulted is deprecated if the class has a user-declared copy assignment
operator or a user-declared destructor [[class.dtor]]. The implicit
definition of a copy assignment operator [[class.copy.assign]] as
defaulted is deprecated if the class has a user-declared copy
constructor or a user-declared destructor. It is possible that future
versions of C++ will specify that these implicit definitions are deleted
[[dcl.fct.def.delete]].

## Redeclaration of `static constexpr` data members <a id="depr.static.constexpr">[[depr.static.constexpr]]</a>

For compatibility with prior revisions of C++, a `constexpr` static data
member may be redundantly redeclared outside the class with no
initializer [[basic.def]], [[class.static.data]]. This usage is
deprecated.

[*Example 1*:

``` cpp
struct A {
  static constexpr int n = 5;   // definition (declaration in C++14{})
};

constexpr int A::n;             // redundant declaration (definition in C++14{})
```

— *end example*]

## Literal operator function declarations using an identifier <a id="depr.lit">[[depr.lit]]</a>

A *literal-operator-id* [[over.literal]] of the form

``` cpp
operator unevaluated-string identifier
```

is deprecated.

## `template` keyword before qualified names <a id="depr.template.template">[[depr.template.template]]</a>

The use of the keyword `template` before the qualified name of a class
or alias template without a template argument list is deprecated
[[temp.names]].

## `has_denorm` members in `numeric_limits` <a id="depr.numeric.limits.has.denorm">[[depr.numeric.limits.has.denorm]]</a>

The following type is defined in addition to those specified in
`<limits>`:

``` cpp
namespace std {
  enum float_denorm_style {
    denorm_indeterminate = -1,
    denorm_absent = 0,
    denorm_present = 1
  };
}
```

The following members are defined in addition to those specified in
[[numeric.limits.general]]:

``` cpp
static constexpr float_denorm_style has_denorm = denorm_absent;
static constexpr bool has_denorm_loss = false;
```

The values of `has_denorm` and `has_denorm_loss` of specializations of
`numeric_limits` are unspecified.

The following members of the specialization `numeric_limits<bool>` are
defined in addition to those specified in [[numeric.special]]:

``` cpp
static constexpr float_denorm_style has_denorm = denorm_absent;
static constexpr bool has_denorm_loss = false;
```

## Deprecated C macros <a id="depr.c.macros">[[depr.c.macros]]</a>

The header `<cfloat>` has the following macros:

``` cpp
#define \libmacro{FLT_HAS_SUBNORM} see below
#define \libmacro{DBL_HAS_SUBNORM} see below
#define \libmacro{LDBL_HAS_SUBNORM} see below
#define \libmacro{DECIMAL_DIG} see below
```

The header defines these macros the same as the C standard library
header `<float.h>`.

In addition to being available via inclusion of the `<cfloat>` header,
the macros `INFINITY` and `NAN` are available when `<cmath>` is
included.

The header `<stdbool.h>` has the following macro:

``` cpp
#define \libxmacro{bool_true_false_are_defined} 1
```

## Deprecated error numbers <a id="depr.cerrno">[[depr.cerrno]]</a>

The header `<cerrno>` has the following additional macros:

``` cpp
#define \libmacro{ENODATA} see below
#define \libmacro{ENOSR} see below
#define \libmacro{ENOSTR} see below
#define \libmacro{ETIME} see below
```

The meaning of these macros is defined by the POSIX standard.

The following `enum errc` enumerators are defined in addition to those
specified in [[system.error.syn]]:

``` cpp
no_message_available,               // ENODATA
no_stream_resources,                // ENOSR
not_a_stream,                       // ENOSTR
stream_timeout,                     // ETIME
```

The value of each `enum errc` enumerator above is the same as the value
of the `<cerrno>` macro shown in the above synopsis.

## Deprecated type traits <a id="depr.meta.types">[[depr.meta.types]]</a>

The header `<type_traits>` has the following addition:

``` cpp
namespace std {
  template<class T> struct is_trivial;
  template<class T> constexpr bool is_trivial_v = is_trivial<T>::value;
  template<class T> struct is_pod;
  template<class T> constexpr bool is_pod_v = is_pod<T>::value;
  template<size_t Len, size_t Align = default-alignment> // see below
    struct aligned_storage;
  template<size_t Len, size_t Align = default-alignment> // see below
    using aligned_storage_t = aligned_storage<Len, Align>::type;
  template<size_t Len, class... Types>
    struct aligned_union;
  template<size_t Len, class... Types>
    using aligned_union_t = aligned_union<Len, Types...>::type;
}
```

The behavior of a program that adds specializations for any of the
templates defined in this subclause is undefined, unless explicitly
permitted by the specification of the corresponding template.

A *trivial class* is a class that is trivially copyable and has one or
more eligible default constructors, all of which are trivial.

[*Note 1*: In particular, a trivial class does not have virtual
functions or virtual base classes. — *end note*]

A *trivial type* is a scalar type, a trivial class, an array of such a
type, or a cv-qualified version of one of these types.

A *POD class* is a class that is both a trivial class and a
standard-layout class, and has no non-static data members of type
non-POD class (or array thereof). A *POD type* is a scalar type, a POD
class, an array of such a type, or a cv-qualified version of one of
these types.

``` cpp
template<class T> struct is_trivial;
```

*Preconditions:* `remove_all_extents_t<T>` shall be a complete type or
cv `void`.

*Remarks:* `is_trivial<T>` is a *Cpp17UnaryTypeTrait*[[meta.rqmts]] with
a base characteristic of `true_type` if `T` is a trivial type, and
`false_type` otherwise.

[*Note 1*: It is unspecified whether a closure
type [[expr.prim.lambda.closure]] is a trivial type. — *end note*]

``` cpp
template<class T> struct is_pod;
```

*Preconditions:* `remove_all_extents_t<T>` shall be a complete type or
cv `void`.

*Remarks:* `is_pod<T>` is a *Cpp17UnaryTypeTrait*[[meta.rqmts]] with a
base characteristic of `true_type` if `T` is a POD type, and
`false_type` otherwise.

[*Note 2*: It is unspecified whether a closure
type [[expr.prim.lambda.closure]] is a POD type. — *end note*]

``` cpp
template<size_t Len, size_t Align = default-alignment>
  struct aligned_storage;
```

The value of *default-alignment* is the most stringent alignment
requirement for any object type whose size is no greater than
`Len`[[basic.types]].

*Mandates:* `Len` is not zero. `Align` is equal to `alignof(T)` for some
type `T` or to *default-alignment*.

The member typedef `type` denotes a trivial standard-layout type
suitable for use as uninitialized storage for any object whose size is
at most `Len` and whose alignment is a divisor of `Align`.

[*Note 3*: Uses of `aligned_storage<Len, Align>::type` can be replaced
by an array `std::byte[Len]` declared with
`alignas(Align)`. — *end note*]

[*Note 4*:

A typical implementation would define `aligned_storage` as:

``` cpp
template<size_t Len, size_t Alignment>
struct aligned_storage {
  typedef struct {
    alignas(Alignment) unsigned char __data[Len];
  } type;
};
```

— *end note*]

``` cpp
template<size_t Len, class... Types>
  struct aligned_union;
```

*Mandates:* At least one type is provided. Each type in the template
parameter pack `Types` is a complete object type.

The member typedef `type` denotes a trivial standard-layout type
suitable for use as uninitialized storage for any object whose type is
listed in `Types`; its size shall be at least `Len`. The static member
`alignment_value` is an integral constant of type `size_t` whose value
is the strictest alignment of all types listed in `Types`.

## Relational operators <a id="depr.relops">[[depr.relops]]</a>

The header `<utility>` has the following additions:

``` cpp
namespace std::rel_ops {
  template<class T> bool operator!=(const T&, const T&);
  template<class T> bool operator> (const T&, const T&);
  template<class T> bool operator<=(const T&, const T&);
  template<class T> bool operator>=(const T&, const T&);
}
```

To avoid redundant definitions of `operator!=` out of `operator==` and
operators `>`, `<=`, and `>=` out of `operator<`, the library provides
the following:

``` cpp
template<class T> bool operator!=(const T& x, const T& y);
```

*Preconditions:* `T` meets the *Cpp17EqualityComparable* requirements
([[cpp17.equalitycomparable]]).

*Returns:* `!(x == y)`.

``` cpp
template<class T> bool operator>(const T& x, const T& y);
```

*Preconditions:* `T` meets the *Cpp17LessThanComparable* requirements
([[cpp17.lessthancomparable]]).

*Returns:* `y < x`.

``` cpp
template<class T> bool operator<=(const T& x, const T& y);
```

*Preconditions:* `T` meets the *Cpp17LessThanComparable* requirements
([[cpp17.lessthancomparable]]).

*Returns:* `!(y < x)`.

``` cpp
template<class T> bool operator>=(const T& x, const T& y);
```

*Preconditions:* `T` meets the *Cpp17LessThanComparable* requirements
([[cpp17.lessthancomparable]]).

*Returns:* `!(x < y)`.

## Tuple <a id="depr.tuple">[[depr.tuple]]</a>

The header `<tuple>` has the following additions:

``` cpp
namespace std {
  template<class T> struct tuple_size<volatile T>;
  template<class T> struct tuple_size<const volatile T>;

  template<size_t I, class T> struct tuple_element<I, volatile T>;
  template<size_t I, class T> struct tuple_element<I, const volatile T>;
}
```

``` cpp
template<class T> struct tuple_size<volatile T>;
template<class T> struct tuple_size<const volatile T>;
```

Let `TS` denote `tuple_size<T>` of the cv-unqualified type `T`. If the
expression `TS::value` is well-formed when treated as an unevaluated
operand [[term.unevaluated.operand]], then specializations of each of
the two templates meet the *Cpp17TransformationTrait* requirements with
a base characteristic of `integral_constant<size_t, TS::value>`.
Otherwise, they have no member `value`.

Access checking is performed as if in a context unrelated to `TS` and
`T`. Only the validity of the immediate context of the expression is
considered.

In addition to being available via inclusion of the `<tuple>` header,
the two templates are available when any of the headers `<array>`,
`<ranges>`, or `<utility>` are included.

``` cpp
template<size_t I, class T> struct tuple_element<I, volatile T>;
template<size_t I, class T> struct tuple_element<I, const volatile T>;
```

Let `TE` denote `tuple_element_t<I, T>` of the cv-unqualified type `T`.
Then specializations of each of the two templates meet the
*Cpp17TransformationTrait* requirements with a member typedef `type`
that names the following type:

- for the first specialization, `add_volatile_t<TE>`, and
- for the second specialization, `add_cv_t<TE>`.

In addition to being available via inclusion of the `<tuple>` header,
the two templates are available when any of the headers `<array>`,
`<ranges>`, or `<utility>` are included.

## Variant <a id="depr.variant">[[depr.variant]]</a>

The header `<variant>` has the following additions:

``` cpp
namespace std {
  template<class T> struct variant_size<volatile T>;
  template<class T> struct variant_size<const volatile T>;

  template<size_t I, class T> struct variant_alternative<I, volatile T>;
  template<size_t I, class T> struct variant_alternative<I, const volatile T>;
}
```

``` cpp
template<class T> struct variant_size<volatile T>;
template<class T> struct variant_size<const volatile T>;
```

Let `VS` denote `variant_size<T>` of the cv-unqualified type `T`. Then
specializations of each of the two templates meet the
*Cpp17UnaryTypeTrait* requirements with a base characteristic of
`integral_constant<size_t, VS::value>`.

``` cpp
template<size_t I, class T> struct variant_alternative<I, volatile T>;
template<size_t I, class T> struct variant_alternative<I, const volatile T>;
```

Let `VA` denote `variant_alternative<I, T>` of the cv-unqualified type
`T`. Then specializations of each of the two templates meet the
*Cpp17TransformationTrait* requirements with a member typedef `type`
that names the following type:

- for the first specialization, `add_volatile_t<VA::type>`, and
- for the second specialization, `add_cv_t<VA::type>`.

## Deprecated `iterator` class template <a id="depr.iterator">[[depr.iterator]]</a>

The header `<iterator>` has the following addition:

``` cpp
namespace std {
  template<class Category, class T, class Distance = ptrdiff_t,
           class Pointer = T*, class Reference = T&>
  struct iterator {
    using iterator_category = Category;
    using value_type        = T;
    using difference_type   = Distance;
    using pointer           = Pointer;
    using reference         = Reference;
  };
}
```

The `iterator` template may be used as a base class to ease the
definition of required types for new iterators.

[*Note 1*: If the new iterator type is a class template, then these
aliases will not be visible from within the iterator class’s template
definition, but only to callers of that class. — *end note*]

[*Example 1*:

If a C++ program wants to define a bidirectional iterator for some data
structure containing `double` and such that it works on a large memory
model of the implementation, it can do so with:

``` cpp
class MyIterator :
  public iterator<bidirectional_iterator_tag, double, long, T*, T&> {
  // code implementing ++, etc.
};
```

— *end example*]

## Deprecated `move_iterator` access <a id="depr.move.iter.elem">[[depr.move.iter.elem]]</a>

The following member is declared in addition to those members specified
in [[move.iter.elem]]:

``` cpp
namespace std {
  template<class Iterator>
  class move_iterator {
  public:
    constexpr pointer operator->() const;
  };
}
```

``` cpp
constexpr pointer operator->() const;
```

*Returns:* `current`.

## Deprecated locale category facets <a id="depr.locale.category">[[depr.locale.category]]</a>

The `ctype` locale category includes the following facets as if they
were specified in [[locale.category.facets]] of [[locale.category]].

``` cpp
codecvt<char16_t, char, mbstate_t>
codecvt<char32_t, char, mbstate_t>
codecvt<char16_t, char8_t, mbstate_t>
codecvt<char32_t, char8_t, mbstate_t>
```

The `ctype` locale category includes the following facets as if they
were specified in [[locale.spec]] of [[locale.category]].

``` cpp
codecvt_byname<char16_t, char, mbstate_t>
codecvt_byname<char32_t, char, mbstate_t>
codecvt_byname<char16_t, char8_t, mbstate_t>
codecvt_byname<char32_t, char8_t, mbstate_t>
```

The following class template specializations are required in addition to
those specified in  [[locale.codecvt]]. The specializations
`codecvt<char16_t, char, mbstate_t>` and
`codecvt<char16_t, char8_t, mbstate_t>` convert between the UTF-16 and
UTF-8 encoding forms, and the specializations
`codecvt<char32_t, char, mbstate_t>` and
`codecvt<char32_t, char8_t, mbstate_t>` convert between the UTF-32 and
UTF-8 encoding forms.

## Deprecated formatting <a id="depr.format">[[depr.format]]</a>

### Header `<format>` synopsis <a id="depr.format.syn">[[depr.format.syn]]</a>

The header `<format>` has the following additions:

``` cpp
namespace std {
  template<class Visitor, class Context>
    decltype(auto) visit_format_arg(Visitor&& vis, basic_format_arg<Context> arg);
}
```

### Formatting arguments <a id="depr.format.arg">[[depr.format.arg]]</a>

``` cpp
template<class Visitor, class Context>
  decltype(auto) visit_format_arg(Visitor&& vis, basic_format_arg<Context> arg);
```

*Effects:* Equivalent to:
`return visit(std::forward<Visitor>(vis), arg.value);`

## Deprecated time formatting <a id="depr.ctime">[[depr.ctime]]</a>

The header `<ctime>` has the following additions:

``` cpp
char* asctime(const tm* timeptr);
char* ctime(const time_t* timer);
```

The functions `asctime` and `ctime` are not required to avoid data races
[[res.on.data.races]].

## Deprecated file systems <a id="depr.filesystems">[[depr.filesystems]]</a>

### Deprecated filesystem path factory functions <a id="depr.fs.path.factory">[[depr.fs.path.factory]]</a>

The header `<filesystem>` has the following additions:

``` cpp
template<class Source>
  path u8path(const Source& source);
template<class InputIterator>
  path u8path(InputIterator first, InputIterator last);
```

*Mandates:* The value type of `Source` and `InputIterator` is `char` or
`char8_t`.

*Preconditions:* The `source` and \[`first`, `last`) sequences are UTF-8
encoded. `Source` meets the requirements specified in [[fs.path.req]].

*Returns:*

- If `path::value_type` is `char` and the current native narrow
  encoding [[fs.path.type.cvt]] is UTF-8, return `path(source)` or
  `path(first, last)`; otherwise,
- if `path::value_type` is `wchar_t` and the native wide encoding is
  UTF-16, or if `path::value_type` is `char16_t` or `char32_t`, convert
  `source` or \[`first`, `last`) to a temporary, `tmp`, of type
  `path::string_type` and return `path(tmp)`; otherwise,
- convert `source` or \[`first`, `last`) to a temporary, `tmp`, of type
  `u32string` and return `path(tmp)`.

*Remarks:* Argument format conversion [[fs.path.fmt.cvt]] applies to the
arguments for these functions. How Unicode encoding conversions are
performed is unspecified.

[*Example 1*:

A string is to be read from a database that is encoded in UTF-8, and
used to create a directory using the native encoding for filenames:

``` cpp
namespace fs = std::filesystem;
std::string utf8_string = read_utf8_data();
fs::create_directory(fs::u8path(utf8_string));
```

For POSIX-based operating systems with the native narrow encoding set to
UTF-8, no encoding or type conversion occurs.

For POSIX-based operating systems with the native narrow encoding not
set to UTF-8, a conversion to UTF-32 occurs, followed by a conversion to
the current native narrow encoding. Some Unicode characters may have no
native character set representation.

For Windows-based operating systems a conversion from UTF-8 to UTF-16
occurs.

— *end example*]

[*Note 1*: The example above is representative of a historical use of
`filesystem::u8path`. To indicate a UTF-8 encoding, passing a
`std::u8string` to `path`’s constructor is preferred as it is consistent
with `path`’s handling of other encodings. — *end note*]

### Deprecated filesystem path format observers <a id="depr.fs.path.obs">[[depr.fs.path.obs]]</a>

The following members are declared in addition to those members
specified in [[fs.path.member]]:

``` cpp
namespace std::filesystem {
  class path {
  public:
    std::string string() const;
    std::string generic_string() const;
  };
}
```

``` cpp
std::string string() const;
```

*Returns:* `system_encoded_string()`.

``` cpp
std::string generic_string() const;
```

*Returns:* `generic_system_encoded_string()`.

## Deprecated atomic operations <a id="depr.atomics">[[depr.atomics]]</a>

### General <a id="depr.atomics.general">[[depr.atomics.general]]</a>

The header `<atomic>` has the following additions.

``` cpp
namespace std {
  template<class T>
    void atomic_init(volatile atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    void atomic_init(atomic<T>*, typename atomic<T>::value_type) noexcept;
  template<class T>
    constexpr T kill_dependency(T y) noexcept;                                  // freestanding
  inline constexpr memory_order memory_order_consume = memory_order::consume;   // freestanding

  #define \libmacro{ATOMIC_VAR_INIT}(value) see below
}
```

### Volatile access <a id="depr.atomics.volatile">[[depr.atomics.volatile]]</a>

If an `atomic` [[atomics.types.generic]] specialization has one of the
following overloads, then that overload participates in overload
resolution even if `atomic<T>::is_always_lock_free` is `false`:

``` cpp
void store(T desired, memory_order order = memory_order::seq_cst) volatile noexcept;
T operator=(T desired) volatile noexcept;
T load(memory_order order = memory_order::seq_cst) const volatile noexcept;
operator T() const volatile noexcept;
T exchange(T desired, memory_order order = memory_order::seq_cst) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order success, memory_order failure) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order success, memory_order failure) volatile noexcept;
bool compare_exchange_weak(T& expected, T desired,
                           memory_order order = memory_order::seq_cst) volatile noexcept;
bool compare_exchange_strong(T& expected, T desired,
                             memory_order order = memory_order::seq_cst) volatile noexcept;
T fetch_key(T operand, memory_order order = memory_order::seq_cst) volatile noexcept;
T operator op=(T operand) volatile noexcept;
T* fetch_key(ptrdiff_t operand, memory_order order = memory_order::seq_cst) volatile noexcept;
```

### Non-member functions <a id="depr.atomics.nonmembers">[[depr.atomics.nonmembers]]</a>

``` cpp
template<class T>
  void atomic_init(volatile atomic<T>* object, typename atomic<T>::value_type desired) noexcept;
template<class T>
  void atomic_init(atomic<T>* object, typename atomic<T>::value_type desired) noexcept;
```

*Effects:* Equivalent to:
`atomic_store_explicit(object, desired, memory_order::relaxed);`

### Operations on atomic types <a id="depr.atomics.types.operations">[[depr.atomics.types.operations]]</a>

``` cpp
#define \libmacro{ATOMIC_VAR_INIT}(value) see below
```

The macro expands to a token sequence suitable for constant
initialization of an atomic variable with static storage duration of a
type that is initialization-compatible with `value`.

[*Note 1*: This operation possibly needs to initialize
locks. — *end note*]

Concurrent access to the variable being initialized, even via an atomic
operation, constitutes a data race.

[*Example 1*:

``` cpp
atomic<int> v = ATOMIC_VAR_INIT(5);
```

— *end example*]

### `memory_order::consume` <a id="depr.atomics.order">[[depr.atomics.order]]</a>

The `memory_order` enumeration contains an additional enumerator:

``` cpp
consume = 1
```

The `memory_order::consume` enumerator is allowed wherever
`memory_order::acquire` is allowed, and it has the same meaning.

``` cpp
template<class T> constexpr T kill_dependency(T y) noexcept;
```

*Returns:* `y`.

<!-- Link reference definitions -->
[atomics.types.generic]: thread.md#atomics.types.generic
[basic.def]: basic.md#basic.def
[basic.link]: basic.md#basic.link
[basic.types]: basic.md#basic.types
[class.copy.assign]: class.md#class.copy.assign
[class.copy.ctor]: class.md#class.copy.ctor
[class.dtor]: class.md#class.dtor
[class.static.data]: class.md#class.static.data
[cpp17.equalitycomparable]: #cpp17.equalitycomparable
[cpp17.lessthancomparable]: #cpp17.lessthancomparable
[dcl.attr.deprecated]: dcl.md#dcl.attr.deprecated
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.struct.bind]: dcl.md#dcl.struct.bind
[depr.atomics]: #depr.atomics
[depr.atomics.general]: #depr.atomics.general
[depr.atomics.nonmembers]: #depr.atomics.nonmembers
[depr.atomics.order]: #depr.atomics.order
[depr.atomics.types.operations]: #depr.atomics.types.operations
[depr.atomics.volatile]: #depr.atomics.volatile
[depr.c.macros]: #depr.c.macros
[depr.capture.this]: #depr.capture.this
[depr.cerrno]: #depr.cerrno
[depr.ctime]: #depr.ctime
[depr.ellipsis.comma]: #depr.ellipsis.comma
[depr.filesystems]: #depr.filesystems
[depr.format]: #depr.format
[depr.format.arg]: #depr.format.arg
[depr.format.syn]: #depr.format.syn
[depr.fs.path.factory]: #depr.fs.path.factory
[depr.fs.path.obs]: #depr.fs.path.obs
[depr.general]: #depr.general
[depr.impldec]: #depr.impldec
[depr.iterator]: #depr.iterator
[depr.lit]: #depr.lit
[depr.local]: #depr.local
[depr.locale.category]: #depr.locale.category
[depr.meta.types]: #depr.meta.types
[depr.move.iter.elem]: #depr.move.iter.elem
[depr.numeric.limits.has.denorm]: #depr.numeric.limits.has.denorm
[depr.relops]: #depr.relops
[depr.static.constexpr]: #depr.static.constexpr
[depr.template.template]: #depr.template.template
[depr.tuple]: #depr.tuple
[depr.variant]: #depr.variant
[depr.volatile.type]: #depr.volatile.type
[expr.assign]: expr.md#expr.assign
[expr.post.incr]: expr.md#expr.post.incr
[expr.pre.incr]: expr.md#expr.pre.incr
[expr.prim.lambda.capture]: expr.md#expr.prim.lambda.capture
[expr.prim.lambda.closure]: expr.md#expr.prim.lambda.closure
[fs.path.fmt.cvt]: input.md#fs.path.fmt.cvt
[fs.path.member]: input.md#fs.path.member
[fs.path.req]: input.md#fs.path.req
[fs.path.type.cvt]: input.md#fs.path.type.cvt
[locale.category]: text.md#locale.category
[locale.category.facets]: #locale.category.facets
[locale.codecvt]: text.md#locale.codecvt
[locale.spec]: #locale.spec
[meta.rqmts]: meta.md#meta.rqmts
[move.iter.elem]: iterators.md#move.iter.elem
[numeric.limits.general]: support.md#numeric.limits.general
[numeric.special]: support.md#numeric.special
[over.literal]: over.md#over.literal
[res.on.data.races]: library.md#res.on.data.races
[system.error.syn]: diagnostics.md#system.error.syn
[temp.names]: temp.md#temp.names
[term.unevaluated.operand]: expr.md#term.unevaluated.operand
