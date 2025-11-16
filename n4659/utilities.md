# General utilities library <a id="utilities">[[utilities]]</a>

## General <a id="utilities.general">[[utilities.general]]</a>

This Clause describes utilities that are generally useful in
C++programs; some of these utilities are used by other elements of the
C++standard library. These utilities are summarized in Table 
[[tab:util.lib.summary]].

**Table: General utilities library summary**

| Subclause             |                                  | Header               |
| --------------------- | -------------------------------- | -------------------- |
| [[utility]]           | Utility components               | `<utility>`          |
| [[intseq]]            | Compile-time integer sequences   | `<utility>`          |
| [[pairs]]             | Pairs                            | `<utility>`          |
| [[tuple]]             | Tuples                           | `<tuple>`            |
| [[optional]]          | Optional objects                 | `<optional>`         |
| [[variant]]           | Variants                         | `<variant>`          |
| [[any]]               | Storage for any type             | `<any>`              |
| [[bitset]]            | Fixed-size sequences of bits     | `<bitset>`           |
| [[memory]]            | Memory                           | `<memory>`           |
|                       |                                  | `<cstdlib>`          |
| [[smartptr]]          | Smart pointers                   | `<memory>`           |
| [[mem.res]]           | Memory resources                 | `<memory_resource>`  |
| [[allocator.adaptor]] | Scoped allocators                | `<scoped_allocator>` |
| [[function.objects]]  | Function objects                 | `<functional>`       |
| [[meta]]              | Type traits                      | `<type_traits>`      |
| [[ratio]]             | Compile-time rational arithmetic | `<ratio>`            |
| [[time]]              | Time utilities                   | `<chrono>`           |
|                       |                                  | `<ctime>`            |
| [[type.index]]        | Type indexes                     | `<typeindex>`        |
| [[execpol]]           | Execution policies               | `<execution>`        |


## Utility components <a id="utility">[[utility]]</a>

This subclause contains some basic function and class templates that are
used throughout the rest of the library.

### Header `<utility>` synopsis <a id="utility.syn">[[utility.syn]]</a>

``` cpp
#include <initializer_list>     // see [initializer_list.syn]

namespace std {
  // [operators], operators
  namespace rel_ops {
    template<class T> bool operator!=(const T&, const T&);
    template<class T> bool operator> (const T&, const T&);
    template<class T> bool operator<=(const T&, const T&);
    template<class T> bool operator>=(const T&, const T&);
  }

  // [utility.swap], swap
  template <class T>
    void swap(T& a, T& b) noexcept(see below);
  template <class T, size_t N>
    void swap(T (&a)[N], T (&b)[N]) noexcept(is_nothrow_swappable_v<T>);

  // [utility.exchange], exchange
  template <class T, class U = T>
    T exchange(T& obj, U&& new_val);

  // [forward], forward/move
  template <class T>
    constexpr T&& forward(remove_reference_t<T>& t) noexcept;
  template <class T>
    constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
  template <class T>
    constexpr remove_reference_t<T>&& move(T&&) noexcept;
  template <class T>
    constexpr conditional_t<
        !is_nothrow_move_constructible_v<T> && is_copy_constructible_v<T>, const T&, T&&>
      move_if_noexcept(T& x) noexcept;

  // [utility.as_const], as_const
  template <class T>
    constexpr add_const_t<T>& as_const(T& t) noexcept;
  template <class T>
    void as_const(const T&&) = delete;

  // [declval], declval
  template <class T>
    add_rvalue_reference_t<T> declval() noexcept;  // as unevaluated operand
%

  // [intseq], Compile-time integer sequences
  template<class T, T...>
    struct integer_sequence;
  template<size_t... I>
    using index_sequence = integer_sequence<size_t, I...>;

  template<class T, T N>
    using make_integer_sequence = integer_sequence<T, see below{}>;
  template<size_t N>
    using make_index_sequence = make_integer_sequence<size_t, N>;

  template<class... T>
    using index_sequence_for = make_index_sequence<sizeof...(T)>;

  // [pairs], class template pair
  template <class T1, class T2>
    struct pair;

  // [pairs.spec], pair specialized algorithms
  template <class T1, class T2>
    constexpr bool operator==(const pair<T1, T2>&, const pair<T1, T2>&);
  template <class T1, class T2>
    constexpr bool operator< (const pair<T1, T2>&, const pair<T1, T2>&);
  template <class T1, class T2>
    constexpr bool operator!=(const pair<T1, T2>&, const pair<T1, T2>&);
  template <class T1, class T2>
    constexpr bool operator> (const pair<T1, T2>&, const pair<T1, T2>&);
  template <class T1, class T2>
    constexpr bool operator>=(const pair<T1, T2>&, const pair<T1, T2>&);
  template <class T1, class T2>
    constexpr bool operator<=(const pair<T1, T2>&, const pair<T1, T2>&);

  template <class T1, class T2>
    void swap(pair<T1, T2>& x, pair<T1, T2>& y) noexcept(noexcept(x.swap(y)));

  template <class T1, class T2>
    constexpr see below make_pair(T1&&, T2&&);

  // [pair.astuple], tuple-like access to pair
  template <class T> class tuple_size;
  template <size_t I, class T> class tuple_element;

  template <class T1, class T2> struct tuple_size<pair<T1, T2>>;
  template <class T1, class T2> struct tuple_element<0, pair<T1, T2>>;
  template <class T1, class T2> struct tuple_element<1, pair<T1, T2>>;

  template<size_t I, class T1, class T2>
    constexpr tuple_element_t<I, pair<T1, T2>>& get(pair<T1, T2>&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr tuple_element_t<I, pair<T1, T2>>&& get(pair<T1, T2>&&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr const tuple_element_t<I, pair<T1, T2>>& get(const pair<T1, T2>&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr const tuple_element_t<I, pair<T1, T2>>&& get(const pair<T1, T2>&&) noexcept;
  template <class T1, class T2>
    constexpr T1& get(pair<T1, T2>& p) noexcept;
  template <class T1, class T2>
    constexpr const T1& get(const pair<T1, T2>& p) noexcept;
  template <class T1, class T2>
    constexpr T1&& get(pair<T1, T2>&& p) noexcept;
  template <class T1, class T2>
    constexpr const T1&& get(const pair<T1, T2>&& p) noexcept;
  template <class T2, class T1>
    constexpr T2& get(pair<T1, T2>& p) noexcept;
  template <class T2, class T1>
    constexpr const T2& get(const pair<T1, T2>& p) noexcept;
  template <class T2, class T1>
    constexpr T2&& get(pair<T1, T2>&& p) noexcept;
  template <class T2, class T1>
    constexpr const T2&& get(const pair<T1, T2>&& p) noexcept;

  // [pair.piecewise], pair piecewise construction
  struct piecewise_construct_t {
    explicit piecewise_construct_t() = default;
  };
  inline constexpr piecewise_construct_t piecewise_construct{};
  template <class... Types> class tuple;        // defined in <tuple> ([tuple.syn])

  // in-place construction
  struct in_place_t {
    explicit in_place_t() = default;
  };
  inline constexpr in_place_t in_place{};
  template <class T>
    struct in_place_type_t {
      explicit in_place_type_t() = default;
    };
  template <class T> inline constexpr in_place_type_t<T> in_place_type{};
  template <size_t I>
    struct in_place_index_t {
      explicit in_place_index_t() = default;
    };
  template <size_t I> inline constexpr in_place_index_t<I> in_place_index{};

{chars_format{chars_format{chars_format{chars_format
  // floating-point format for primitive numerical conversion
  enum class chars_format {
    scientific = unspecified,
    fixed = unspecified,
    hex = unspecified,
    general = fixed | scientific
  };

{to_chars_result{to_chars_result}

  // [utility.to.chars], primitive numerical output conversion
  struct to_chars_result {
    char* ptr;
    error_code ec;
  };

  to_chars_result to_chars(char* first, char* last, see below value, int base = 10);

  to_chars_result to_chars(char* first, char* last, float value);
  to_chars_result to_chars(char* first, char* last, double value);
  to_chars_result to_chars(char* first, char* last, long double value);

  to_chars_result to_chars(char* first, char* last, float value,
                           chars_format fmt);
  to_chars_result to_chars(char* first, char* last, double value,
                           chars_format fmt);
  to_chars_result to_chars(char* first, char* last, long double value,
                           chars_format fmt);

  to_chars_result to_chars(char* first, char* last, float value,
                           chars_format fmt, int precision);
  to_chars_result to_chars(char* first, char* last, double value,
                           chars_format fmt, int precision);
  to_chars_result to_chars(char* first, char* last, long double value,
                           chars_format fmt, int precision);

{from_chars_result{from_chars_result}

  // [utility.from.chars], primitive numerical input conversion
  struct from_chars_result {
    const char* ptr;
    error_code ec;
  };

  from_chars_result from_chars(const char* first, const char* last,
                               see below& value, int base = 10);

  from_chars_result from_chars(const char* first, const char* last, float& value,
                               chars_format fmt = chars_format::general);
  from_chars_result from_chars(const char* first, const char* last, double& value,
                               chars_format fmt = chars_format::general);
  from_chars_result from_chars(const char* first, const char* last, long double& value,
                               chars_format fmt = chars_format::general);
}
```

The header `<utility>` defines several types and function templates that
are described in this Clause. It also defines the template `pair` and
various function templates that operate on `pair` objects.

The type `chars_format` is a bitmask type ([[bitmask.types]]) with
elements `scientific`, `fixed`, and `hex`.

### Operators <a id="operators">[[operators]]</a>

To avoid redundant definitions of `operator!=` out of `operator==` and
operators `>`, `<=`, and `>=` out of `operator<`, the library provides
the following:

``` cpp
template <class T> bool operator!=(const T& x, const T& y);
```

*Requires:* Type `T` is `EqualityComparable`
(Table  [[tab:equalitycomparable]]).

*Returns:* `!(x == y)`.

``` cpp
template <class T> bool operator>(const T& x, const T& y);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[tab:lessthancomparable]]).

*Returns:* `y < x`.

``` cpp
template <class T> bool operator<=(const T& x, const T& y);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[tab:lessthancomparable]]).

*Returns:* `!(y < x)`.

``` cpp
template <class T> bool operator>=(const T& x, const T& y);
```

*Requires:* Type `T` is `LessThanComparable`
(Table  [[tab:lessthancomparable]]).

*Returns:* `!(x < y)`.

In this library, whenever a declaration is provided for an `operator!=`,
`operator>`, `operator>=`, or `operator<=`, and requirements and
semantics are not explicitly provided, the requirements and semantics
are as specified in this Clause.

### `swap` <a id="utility.swap">[[utility.swap]]</a>

``` cpp
template <class T>
  void swap(T& a, T& b) noexcept(see below);
```

*Remarks:* This function shall not participate in overload resolution
unless `is_move_constructible_v<T>` is `true` and
`is_move_assignable_v<T>` is `true`. The expression inside `noexcept` is
equivalent to:

``` cpp
is_nothrow_move_constructible_v<T> && is_nothrow_move_assignable_v<T>
```

*Requires:* Type `T` shall be `MoveConstructible`
(Table  [[tab:moveconstructible]]) and `MoveAssignable`
(Table  [[tab:moveassignable]]).

*Effects:* Exchanges values stored in two locations.

``` cpp
template <class T, size_t N>
  void swap(T (&a)[N], T (&b)[N]) noexcept(is_nothrow_swappable_v<T>);
```

*Remarks:* This function shall not participate in overload resolution
unless `is_swappable_v<T>` is `true`.

*Requires:* `a[i]` shall be swappable with ([[swappable.requirements]])
`b[i]` for all `i` in the range \[`0`, `N`).

*Effects:* As if by `swap_ranges(a, a + N, b)`.

### `exchange` <a id="utility.exchange">[[utility.exchange]]</a>

``` cpp
template <class T, class U = T> T exchange(T& obj, U&& new_val);
```

*Effects:* Equivalent to:

``` cpp
T old_val = std::move(obj);
obj = std::forward<U>(new_val);
return old_val;
```

### Forward/move helpers <a id="forward">[[forward]]</a>

The library provides templated helper functions to simplify applying
move semantics to an lvalue and to simplify the implementation of
forwarding functions. All functions specified in this subclause are
signal-safe ([[csignal.syn]]).

``` cpp
template <class T> constexpr T&& forward(remove_reference_t<T>& t) noexcept;
template <class T> constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
```

*Returns:* `static_cast<T&&>(t)`.

*Remarks:* If the second form is instantiated with an lvalue reference
type, the program is ill-formed.

[*Example 1*:

``` cpp
template <class T, class A1, class A2>
shared_ptr<T> factory(A1&& a1, A2&& a2) {
  return shared_ptr<T>(new T(std::forward<A1>(a1), std::forward<A2>(a2)));
}

struct A {
  A(int&, const double&);
};

void g() {
  shared_ptr<A> sp1 = factory<A>(2, 1.414); // error: 2 will not bind to int&
  int i = 2;
  shared_ptr<A> sp2 = factory<A>(i, 1.414); // OK
}
```

In the first call to `factory`, `A1` is deduced as `int`, so 2 is
forwarded to `A`’s constructor as an rvalue. In the second call to
`factory`, `A1` is deduced as `int&`, so `i` is forwarded to `A`’s
constructor as an lvalue. In both cases, `A2` is deduced as `double`, so
1.414 is forwarded to `A`’s constructor as an rvalue.

— *end example*]

``` cpp
template <class T> constexpr remove_reference_t<T>&& move(T&& t) noexcept;
```

*Returns:* `static_cast<remove_reference_t<T>&&>(t)`.

[*Example 2*:

``` cpp
template <class T, class A1>
shared_ptr<T> factory(A1&& a1) {
  return shared_ptr<T>(new T(std::forward<A1>(a1)));
}

struct A {
  A();
  A(const A&);      // copies from lvalues
  A(A&&);           // moves from rvalues
};

void g() {
  A a;
  shared_ptr<A> sp1 = factory<A>(a);                // ``a'' binds to A(const A&)
  shared_ptr<A> sp1 = factory<A>(std::move(a));     // ``a'' binds to A(A&&)
}
```

In the first call to `factory`, `A1` is deduced as `A&`, so `a` is
forwarded as a non-const lvalue. This binds to the constructor
`A(const A&)`, which copies the value from `a`. In the second call to
`factory`, because of the call `std::move(a)`, `A1` is deduced as `A`,
so `a` is forwarded as an rvalue. This binds to the constructor
`A(A&&)`, which moves the value from `a`.

— *end example*]

``` cpp
template <class T> constexpr conditional_t<
    !is_nothrow_move_constructible_v<T> && is_copy_constructible_v<T>, const T&, T&&>
  move_if_noexcept(T& x) noexcept;
```

*Returns:* `std::move(x)`.

### Function template `as_const` <a id="utility.as_const">[[utility.as_const]]</a>

``` cpp
template <class T> constexpr add_const_t<T>& as_const(T& t) noexcept;
```

*Returns:* `t`.

### Function template `declval` <a id="declval">[[declval]]</a>

The library provides the function template `declval` to simplify the
definition of expressions which occur as unevaluated operands (Clause 
[[expr]]).

``` cpp
template <class T> add_rvalue_reference_t<T> declval() noexcept;    // as unevaluated operand
```

*Remarks:* If this function is odr-used ([[basic.def.odr]]), the
program is ill-formed.

*Remarks:* The template parameter `T` of `declval` may be an incomplete
type.

[*Example 1*:

``` cpp
template <class To, class From> decltype(static_cast<To>(declval<From>())) convert(From&&);
```

declares a function template `convert` which only participates in
overloading if the type `From` can be explicitly converted to type `To`.
For another example see class template `common_type` (
[[meta.trans.other]]).

— *end example*]

### Primitive numeric output conversion <a id="utility.to.chars">[[utility.to.chars]]</a>

All functions named `to_chars` convert `value` into a character string
by successively filling the range \[`first`, `last`), where \[`first`,
`last`) is required to be a valid range. If the member `ec` of the
return value is such that the value, when converted to `bool`, is
`false`, the conversion was successful and the member `ptr` is the
one-past-the-end pointer of the characters written. Otherwise, the
member `ec` has the value `errc::value_too_large`, the member `ptr` has
the value `last`, and the contents of the range \[`first`, `last`) are
unspecified.

The functions that take a floating-point `value` but not a `precision`
parameter ensure that the string representation consists of the smallest
number of characters such that there is at least one digit before the
radix point (if present) and parsing the representation using the
corresponding `from_chars` function recovers `value` exactly.

[*Note 1*: This guarantee applies only if `to_chars` and `from_chars`
are executed on the same implementation. — *end note*]

The functions taking a `chars_format` parameter determine the conversion
specifier for `printf` as follows: The conversion specifier is `f` if
`fmt` is `chars_format::fixed`, `e` if `fmt` is
`chars_format::scientific`, `a` (without leading `"0x"` in the result)
if `fmt` is `chars_format::hex`, and `g` if `fmt` is
`chars_format::general`.

``` cpp
to_chars_result to_chars(char* first, char* last, see below value, int base = 10);
```

*Requires:* `base` has a value between 2 and 36 (inclusive).

*Effects:* The value of `value` is converted to a string of digits in
the given base (with no redundant leading zeroes). Digits in the range
10..35 (inclusive) are represented as lowercase characters `a`..`z`. If
`value` is less than zero, the representation starts with a minus sign.

*Throws:* Nothing.

*Remarks:* The implementation shall provide overloads for all signed and
unsigned integer types and `char` as the type of the parameter `value`.

``` cpp
to_chars_result to_chars(char* first, char* last, float value);
to_chars_result to_chars(char* first, char* last, double value);
to_chars_result to_chars(char* first, char* last, long double value);
```

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale. The conversion specifier is `f` or `e`, chosen
according to the requirement for a shortest representation (see above);
a tie is resolved in favor of `f`.

*Throws:* Nothing.

``` cpp
to_chars_result to_chars(char* first, char* last, float value, chars_format fmt);
to_chars_result to_chars(char* first, char* last, double value, chars_format fmt);
to_chars_result to_chars(char* first, char* last, long double value, chars_format fmt);
```

*Requires:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale.

*Throws:* Nothing.

``` cpp
to_chars_result to_chars(char* first, char* last, float value,
                         chars_format fmt, int precision);
to_chars_result to_chars(char* first, char* last, double value,
                         chars_format fmt, int precision);
to_chars_result to_chars(char* first, char* last, long double value,
                         chars_format fmt, int precision);
```

*Requires:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale with the given precision.

*Throws:* Nothing.

ISO C 7.21.6.1.

### Primitive numeric input conversion <a id="utility.from.chars">[[utility.from.chars]]</a>

All functions named `from_chars` analyze the string \[`first`, `last`)
for a pattern, where \[`first`, `last`) is required to be a valid range.
If no characters match the pattern, `value` is unmodified, the member
`ptr` of the return value is `first` and the member `ec` is equal to
`errc::invalid_argument`. Otherwise, the characters matching the pattern
are interpreted as a representation of a value of the type of `value`.
The member `ptr` of the return value points to the first character not
matching the pattern, or has the value `last` if all characters match.
If the parsed value is not in the range representable by the type of
`value`, `value` is unmodified and the member `ec` of the return value
is equal to `errc::result_out_of_range`. Otherwise, `value` is set to
the parsed value and the member `ec` is set such that the conversion to
`bool` yields `false`.

``` cpp
from_chars_result from_chars(const char* first, const char* last,
                             see below&\itcorr[-1] value, int base = 10);
```

*Requires:* `base` has a value between 2 and 36 (inclusive).

*Effects:* The pattern is the expected form of the subject sequence in
the `"C"` locale for the given nonzero base, as described for `strtol`,
except that no `"0x"` or `"0X"` prefix shall appear if the value of
`base` is 16, and except that a minus sign is the only sign that may
appear, and only if `value` has a signed type.

*Throws:* Nothing.

*Remarks:* The implementation shall provide overloads for all signed and
unsigned integer types and `char` as the referenced type of the
parameter `value`.

``` cpp
from_chars_result from_chars(const char* first, const char* last, float& value,
                             chars_format fmt = chars_format::general);
from_chars_result from_chars(const char* first, const char* last, double& value,
                             chars_format fmt = chars_format::general);
from_chars_result from_chars(const char* first, const char* last, long double& value,
                             chars_format fmt = chars_format::general);
```

*Requires:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* The pattern is the expected form of the subject sequence in
the `"C"` locale, as described for `strtod`, except that

- the only sign that may appear is a minus sign;
- if `fmt` has `chars_format::scientific` set but not
  `chars_format::fixed`, the otherwise optional exponent part shall
  appear;
- if `fmt` has `chars_format::fixed` set but not
  `chars_format::scientific`, the optional exponent part shall not
  appear; and
- if `fmt` is `chars_format::hex`, the prefix `"0x"` or `"0X"` is
  assumed. \[*Example 1*: The string `0x123` is parsed to have the value
  `0` with remaining characters `x123`. — *end example*]

In any case, the resulting `value` is one of at most two floating-point
values closest to the value of the string matching the pattern.

*Throws:* Nothing.

ISO C 7.22.1.3, ISO C 7.22.1.4.

## Compile-time integer sequences <a id="intseq">[[intseq]]</a>

### In general <a id="intseq.general">[[intseq.general]]</a>

The library provides a class template that can represent an integer
sequence. When used as an argument to a function template the parameter
pack defining the sequence can be deduced and used in a pack expansion.

[*Note 1*: The `index_sequence` alias template is provided for the
common case of an integer sequence of type `size_t`; see also
[[tuple.apply]]. — *end note*]

### Class template `integer_sequence` <a id="intseq.intseq">[[intseq.intseq]]</a>

``` cpp
namespace std {
  template<class T, T... I>
    struct integer_sequence {
      using value_type = T;
      static constexpr size_t size() noexcept { return sizeof...(I); }
    };
}
```

`T` shall be an integer type.

### Alias template `make_integer_sequence` <a id="intseq.make">[[intseq.make]]</a>

``` cpp
template<class T, T N>
  using make_integer_sequence = integer_sequence<T, see below{}>;
```

If `N` is negative the program is ill-formed. The alias template
`make_integer_sequence` denotes a specialization of `integer_sequence`
with `N` template non-type arguments. The type
`make_integer_sequence<T, N>` denotes the type
`integer_sequence<T, 0, 1, ..., N-1>`.

[*Note 1*: `make_integer_sequence<int, 0>` denotes the type
`integer_sequence<int>` — *end note*]

## Pairs <a id="pairs">[[pairs]]</a>

### In general <a id="pairs.general">[[pairs.general]]</a>

The library provides a template for heterogeneous pairs of values. The
library also provides a matching function template to simplify their
construction and several templates that provide access to `pair` objects
as if they were `tuple` objects (see  [[tuple.helper]] and 
[[tuple.elem]]).

### Class template `pair` <a id="pairs.pair">[[pairs.pair]]</a>

``` cpp
namespace std {
  template <class T1, class T2>
    struct pair {
      using first_type  = T1;
      using second_type = T2;

      T1 first;
      T2 second;

      pair(const pair&) = default;
      pair(pair&&) = default;
      \EXPLICIT constexpr pair();
      \EXPLICIT constexpr pair(const T1& x, const T2& y);
      template<class U1, class U2> \EXPLICIT constexpr pair(U1&& x, U2&& y);
      template<class U1, class U2> \EXPLICIT constexpr pair(const pair<U1, U2>& p);
      template<class U1, class U2> \EXPLICIT constexpr pair(pair<U1, U2>&& p);
      template <class... Args1, class... Args2>
        pair(piecewise_construct_t, tuple<Args1...> first_args, tuple<Args2...> second_args);

      pair& operator=(const pair& p);
      template<class U1, class U2> pair& operator=(const pair<U1, U2>& p);
      pair& operator=(pair&& p) noexcept(see below);
      template<class U1, class U2> pair& operator=(pair<U1, U2>&& p);

      void swap(pair& p) noexcept(see below);
    };

  template<class T1, class T2>
    pair(T1, T2) -> pair<T1, T2>;
}
```

Constructors and member functions of `pair` shall not throw exceptions
unless one of the element-wise operations specified to be called for
that operation throws an exception.

The defaulted move and copy constructor, respectively, of `pair` shall
be a constexpr function if and only if all required element-wise
initializations for copy and move, respectively, would satisfy the
requirements for a constexpr function. The destructor of `pair` shall be
a trivial destructor if
`(is_trivially_destructible_v<T1> && is_trivially_destructible_v<T2>)`
is `true`.

``` cpp
\EXPLICIT constexpr pair();
```

*Effects:* Value-initializes `first` and `second`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_default_constructible_v<first_type>` is `true` and
`is_default_constructible_v<second_type>` is `true`.

[*Note 1*: This behavior can be implemented by a constructor template
with default template arguments. — *end note*]

The constructor is explicit if and only if either `first_type` or
`second_type` is not implicitly default-constructible.

[*Note 2*: This behavior can be implemented with a trait that checks
whether a `const first_type&` or a `const second_type&` can be
initialized with `{}`. — *end note*]

``` cpp
\EXPLICIT constexpr pair(const T1& x, const T2& y);
```

*Effects:* Initializes `first` with `x` and `second` with `y`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_copy_constructible_v<first_type>` is `true` and
`is_copy_constructible_v<second_type>` is `true`. The constructor is
explicit if and only if
`is_convertible_v<const first_type&, first_type>` is `false` or
`is_convertible_v<const second_type&, second_type>` is `false`.

``` cpp
template<class U1, class U2> \EXPLICIT constexpr pair(U1&& x, U2&& y);
```

*Effects:* Initializes `first` with `std::forward<U1>(x)` and `second`
with `std::forward<U2>(y)`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<first_type, U1&&>` is `true` and
`is_constructible_v<second_type, U2&&>` is `true`. The constructor is
explicit if and only if `is_convertible_v<U1&&, first_type>` is `false`
or `is_convertible_v<U2&&, second_type>` is `false`.

``` cpp
template<class U1, class U2> \EXPLICIT constexpr pair(const pair<U1, U2>& p);
```

*Effects:* Initializes members from the corresponding members of the
argument.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<first_type, const U1&>` is `true` and
`is_constructible_v<second_type, const U2&>` is `true`. The constructor
is explicit if and only if `is_convertible_v<const U1&, first_type>` is
`false` or `is_convertible_v<const U2&, second_type>` is `false`.

``` cpp
template<class U1, class U2> \EXPLICIT constexpr pair(pair<U1, U2>&& p);
```

*Effects:* Initializes `first` with `std::forward<U1>(p.first)` and
`second` with `std::forward<U2>(p.second)`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<first_type, U1&&>` is `true` and
`is_constructible_v<second_type, U2&&>` is `true`. The constructor is
explicit if and only if `is_convertible_v<U1&&, first_type>` is `false`
or `is_convertible_v<U2&&, second_type>` is `false`.

``` cpp
template<class... Args1, class... Args2>
  pair(piecewise_construct_t, tuple<Args1...> first_args, tuple<Args2...> second_args);
```

*Requires:* `is_constructible_v<first_type, Args1&&...>` is `true` and
`is_constructible_v<second_type, Args2&&...>` is `true`.

*Effects:* Initializes `first` with arguments of types `Args1...`
obtained by forwarding the elements of `first_args` and initializes
`second` with arguments of types `Args2...` obtained by forwarding the
elements of `second_args`. (Here, forwarding an element `x` of type `U`
within a `tuple` object means calling `std::forward<U>(x)`.) This form
of construction, whereby constructor arguments for `first` and `second`
are each provided in a separate `tuple` object, is called *piecewise
construction*.

``` cpp
pair& operator=(const pair& p);
```

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Remarks:* This operator shall be defined as deleted unless
`is_copy_assignable_v<first_type>` is `true` and
`is_copy_assignable_v<second_type>` is `true`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> pair& operator=(const pair<U1, U2>& p);
```

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Remarks:* This operator shall not participate in overload resolution
unless `is_assignable_v<first_type&, const U1&>` is `true` and
`is_assignable_v<second_type&, const U2&>` is `true`.

*Returns:* `*this`.

``` cpp
pair& operator=(pair&& p) noexcept(see below);
```

*Effects:* Assigns to `first` with `std::forward<first_type>(p.first)`
and to `second` with  
`std::forward<second_type>(p.second)`.

*Remarks:* This operator shall be defined as deleted unless
`is_move_assignable_v<first_type>` is `true` and
`is_move_assignable_v<second_type>` is `true`.

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_move_assignable_v<T1> && is_nothrow_move_assignable_v<T2>
```

*Returns:* `*this`.

``` cpp
template<class U1, class U2> pair& operator=(pair<U1, U2>&& p);
```

*Effects:* Assigns to `first` with `std::forward<U>(p.first)` and to
`second` with  
`std::forward<V>(p.second)`.

*Remarks:* This operator shall not participate in overload resolution
unless `is_assignable_v<first_type&, U1&&>` is `true` and
`is_assignable_v<second_type&, U2&&>` is `true`.

*Returns:* `*this`.

``` cpp
void swap(pair& p) noexcept(see below);
```

*Requires:* `first` shall be swappable
with ([[swappable.requirements]]) `p.first` and `second` shall be
swappable with `p.second`.

*Effects:* Swaps `first` with `p.first` and `second` with `p.second`.

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_swappable_v<first_type> && is_nothrow_swappable_v<second_type>
```

### Specialized algorithms <a id="pairs.spec">[[pairs.spec]]</a>

``` cpp
template <class T1, class T2>
  constexpr bool operator==(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `x.first == y.first && x.second == y.second`.

``` cpp
template <class T1, class T2>
  constexpr bool operator<(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:*
`x.first < y.first || (!(y.first < x.first) && x.second < y.second)`.

``` cpp
template <class T1, class T2>
  constexpr bool operator!=(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `!(x == y)`.

``` cpp
template <class T1, class T2>
  constexpr bool operator>(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `y < x`.

``` cpp
template <class T1, class T2>
  constexpr bool operator>=(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `!(x < y)`.

``` cpp
template <class T1, class T2>
  constexpr bool operator<=(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `!(y < x)`.

``` cpp
template<class T1, class T2> void swap(pair<T1, T2>& x, pair<T1, T2>& y)
  noexcept(noexcept(x.swap(y)));
```

*Effects:* As if by `x.swap(y)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_swappable_v<T1>` is `true` and `is_swappable_v<T2>` is
`true`.

``` cpp
template <class T1, class T2>
  constexpr pair<V1, V2> make_pair(T1&& x, T2&& y);
```

*Returns:* `pair<V1, V2>(std::forward<T1>(x), std::forward<T2>(y))`,
where `V1` and `V2` are determined as follows: Let `Ui` be `decay_t<Ti>`
for each `Ti`. If `Ui` is a specialization of `reference_wrapper`, then
`Vi` is `Ui::type&`, otherwise `Vi` is `Ui`.

[*Example 1*:

In place of:

``` cpp
  return pair<int, double>(5, 3.1415926);   // explicit types
```

a C++program may contain:

``` cpp
  return make_pair(5, 3.1415926);           // types are deduced
```

— *end example*]

### Tuple-like access to pair <a id="pair.astuple">[[pair.astuple]]</a>

``` cpp
template <class T1, class T2>
  struct tuple_size<pair<T1, T2>> : integral_constant<size_t, 2> { };
```

``` cpp
tuple_element<0, pair<T1, T2>>::type
```

*Value:* The type `T1`.

``` cpp
tuple_element<1, pair<T1, T2>>::type
```

*Value:* The type T2.

``` cpp
template<size_t I, class T1, class T2>
  constexpr tuple_element_t<I, pair<T1, T2>>& get(pair<T1, T2>& p) noexcept;
template<size_t I, class T1, class T2>
  constexpr const tuple_element_t<I, pair<T1, T2>>& get(const pair<T1, T2>& p) noexcept;
template<size_t I, class T1, class T2>
  constexpr tuple_element_t<I, pair<T1, T2>>&& get(pair<T1, T2>&& p) noexcept;
template<size_t I, class T1, class T2>
  constexpr const tuple_element_t<I, pair<T1, T2>>&& get(const pair<T1, T2>&& p) noexcept;
```

*Returns:* If `I == 0` returns a reference to `p.first`; if `I == 1`
returns a reference to `p.second`; otherwise the program is ill-formed.

``` cpp
template <class T1, class T2>
  constexpr T1& get(pair<T1, T2>& p) noexcept;
template <class T1, class T2>
  constexpr const T1& get(const pair<T1, T2>& p) noexcept;
template <class T1, class T2>
  constexpr T1&& get(pair<T1, T2>&& p) noexcept;
template <class T1, class T2>
  constexpr const T1&& get(const pair<T1, T2>&& p) noexcept;
```

*Requires:* `T1` and `T2` are distinct types. Otherwise, the program is
ill-formed.

*Returns:* A reference to `p.first`.

``` cpp
template <class T2, class T1>
  constexpr T2& get(pair<T1, T2>& p) noexcept;
template <class T2, class T1>
  constexpr const T2& get(const pair<T1, T2>& p) noexcept;
template <class T2, class T1>
  constexpr T2&& get(pair<T1, T2>&& p) noexcept;
template <class T2, class T1>
  constexpr const T2&& get(const pair<T1, T2>&& p) noexcept;
```

*Requires:* `T1` and `T2` are distinct types. Otherwise, the program is
ill-formed.

*Returns:* A reference to `p.second`.

### Piecewise construction <a id="pair.piecewise">[[pair.piecewise]]</a>

``` cpp
struct piecewise_construct_t {
  explicit piecewise_construct_t() = default;
};
inline constexpr piecewise_construct_t piecewise_construct{};
```

The `struct` `piecewise_construct_t` is an empty structure type used as
a unique type to disambiguate constructor and function overloading.
Specifically, `pair` has a constructor with `piecewise_construct_t` as
the first argument, immediately followed by two `tuple` ([[tuple]])
arguments used for piecewise construction of the elements of the `pair`
object.

## Tuples <a id="tuple">[[tuple]]</a>

### In general <a id="tuple.general">[[tuple.general]]</a>

This subclause describes the tuple library that provides a tuple type as
the class template `tuple` that can be instantiated with any number of
arguments. Each template argument specifies the type of an element in
the `tuple`. Consequently, tuples are heterogeneous, fixed-size
collections of values. An instantiation of `tuple` with two arguments is
similar to an instantiation of `pair` with the same two arguments. See 
[[pairs]].

### Header `<tuple>` synopsis <a id="tuple.syn">[[tuple.syn]]</a>

``` cpp
namespace std {
  // [tuple.tuple], class template tuple
  template <class... Types>
    class tuple;

  // [tuple.creation], tuple creation functions
  inline constexpr unspecified ignore;

  template <class... TTypes>
    constexpr tuple<VTypes...> make_tuple(TTypes&&...);

  template <class... TTypes>
    constexpr tuple<TTypes&&...> forward_as_tuple(TTypes&&...) noexcept;

  template<class... TTypes>
    constexpr tuple<TTypes&...> tie(TTypes&...) noexcept;

  template <class... Tuples>
    constexpr tuple<CTypes...> tuple_cat(Tuples&&...);

  // [tuple.apply], calling a function with a tuple of arguments
  template <class F, class Tuple>
    constexpr decltype(auto) apply(F&& f, Tuple&& t);

  template <class T, class Tuple>
    constexpr T make_from_tuple(Tuple&& t);

  // [tuple.helper], tuple helper classes
  template <class T> class tuple_size;                  // not defined
  template <class T> class tuple_size<const T>;
  template <class T> class tuple_size<volatile T>;
  template <class T> class tuple_size<const volatile T>;

  template <class... Types> class tuple_size<tuple<Types...>>;

  template <size_t I, class T> class tuple_element;     // not defined
  template <size_t I, class T> class tuple_element<I, const T>;
  template <size_t I, class T> class tuple_element<I, volatile T>;
  template <size_t I, class T> class tuple_element<I, const volatile T>;

  template <size_t I, class... Types>
    class tuple_element<I, tuple<Types...>>;

  template <size_t I, class T>
    using tuple_element_t = typename tuple_element<I, T>::type;

  // [tuple.elem], element access
  template <size_t I, class... Types>
    constexpr tuple_element_t<I, tuple<Types...>>& get(tuple<Types...>&) noexcept;
  template <size_t I, class... Types>
    constexpr tuple_element_t<I, tuple<Types...>>&& get(tuple<Types...>&&) noexcept;
  template <size_t I, class... Types>
    constexpr const tuple_element_t<I, tuple<Types...>>& get(const tuple<Types...>&) noexcept;
  template <size_t I, class... Types>
    constexpr const tuple_element_t<I, tuple<Types...>>&& get(const tuple<Types...>&&) noexcept;
  template <class T, class... Types>
    constexpr T& get(tuple<Types...>& t) noexcept;
  template <class T, class... Types>
    constexpr T&& get(tuple<Types...>&& t) noexcept;
  template <class T, class... Types>
    constexpr const T& get(const tuple<Types...>& t) noexcept;
  template <class T, class... Types>
    constexpr const T&& get(const tuple<Types...>&& t) noexcept;

  // [tuple.rel], relational operators
  template<class... TTypes, class... UTypes>
    constexpr bool operator==(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator<(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator!=(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator>(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator<=(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr bool operator>=(const tuple<TTypes...>&, const tuple<UTypes...>&);

  // [tuple.traits], allocator-related traits
  template <class... Types, class Alloc>
    struct uses_allocator<tuple<Types...>, Alloc>;

  // [tuple.special], specialized algorithms
  template <class... Types>
    void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);

  // [tuple.helper], tuple helper classes
  template <class T>
    inline constexpr size_t tuple_size_v = tuple_size<T>::value;
}
```

### Class template `tuple` <a id="tuple.tuple">[[tuple.tuple]]</a>

``` cpp
namespace std {
  template <class... Types>
    class tuple  {
    public:
      // [tuple.cnstr], tuple construction
      \EXPLICIT constexpr tuple();
      \EXPLICIT constexpr tuple(const Types&...);         // only if sizeof...(Types) >= 1
      template <class... UTypes>
        \EXPLICIT constexpr tuple(UTypes&&...);           // only if sizeof...(Types) >= 1

      tuple(const tuple&) = default;
      tuple(tuple&&) = default;

      template <class... UTypes>
        \EXPLICIT constexpr tuple(const tuple<UTypes...>&);
      template <class... UTypes>
        \EXPLICIT constexpr tuple(tuple<UTypes...>&&);

      template <class U1, class U2>
        \EXPLICIT constexpr tuple(const pair<U1, U2>&);   // only if sizeof...(Types) == 2
      template <class U1, class U2>
        \EXPLICIT constexpr tuple(pair<U1, U2>&&);        // only if sizeof...(Types) == 2

      // allocator-extended constructors
      template <class Alloc>
        tuple(allocator_arg_t, const Alloc& a);
      template <class Alloc>
        \EXPLICIT tuple(allocator_arg_t, const Alloc& a, const Types&...);
      template <class Alloc, class... UTypes>
        \EXPLICIT tuple(allocator_arg_t, const Alloc& a, UTypes&&...);
      template <class Alloc>
        tuple(allocator_arg_t, const Alloc& a, const tuple&);
      template <class Alloc>
        tuple(allocator_arg_t, const Alloc& a, tuple&&);
      template <class Alloc, class... UTypes>
        \EXPLICIT tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
      template <class Alloc, class... UTypes>
        \EXPLICIT tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
      template <class Alloc, class U1, class U2>
        \EXPLICIT tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
      template <class Alloc, class U1, class U2>
        \EXPLICIT tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);

      // [tuple.assign], tuple assignment
      tuple& operator=(const tuple&);
      tuple& operator=(tuple&&) noexcept(see below);

      template <class... UTypes>
        tuple& operator=(const tuple<UTypes...>&);
      template <class... UTypes>
        tuple& operator=(tuple<UTypes...>&&);

      template <class U1, class U2>
        tuple& operator=(const pair<U1, U2>&);              // only if sizeof...(Types) == 2
      template <class U1, class U2>
        tuple& operator=(pair<U1, U2>&&);                   // only if sizeof...(Types) == 2

      // [tuple.swap], tuple swap
      void swap(tuple&) noexcept(see below);
    };

  template<class... UTypes>
    tuple(UTypes...) -> tuple<UTypes...>;
  template<class T1, class T2>
    tuple(pair<T1, T2>) -> tuple<T1, T2>;
  template<class Alloc, class... UTypes>
    tuple(allocator_arg_t, Alloc, UTypes...) -> tuple<UTypes...>;
  template<class Alloc, class T1, class T2>
    tuple(allocator_arg_t, Alloc, pair<T1, T2>) -> tuple<T1, T2>;
  template<class Alloc, class... UTypes>
    tuple(allocator_arg_t, Alloc, tuple<UTypes...>) -> tuple<UTypes...>;
}
```

#### Construction <a id="tuple.cnstr">[[tuple.cnstr]]</a>

For each `tuple` constructor, an exception is thrown only if the
construction of one of the types in `Types` throws an exception.

The defaulted move and copy constructor, respectively, of `tuple` shall
be a constexpr function if and only if all required element-wise
initializations for copy and move, respectively, would satisfy the
requirements for a constexpr function. The defaulted move and copy
constructor of `tuple<>` shall be constexpr functions.

The destructor of tuple shall be a trivial destructor if
`(is_trivially_destructible_v<Types> && ...)` is `true`.

In the constructor descriptions that follow, let i be in the range
\[`0`, `sizeof...(Types)`) in order, `Tᵢ` be the iᵗʰ type in `Types`,
and `Uᵢ` be the iᵗʰ type in a template parameter pack named `UTypes`,
where indexing is zero-based.

``` cpp
\EXPLICIT constexpr tuple();
```

*Effects:* Value-initializes each element.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_default_constructible_v<``Tᵢ``>` is `true` for all i.

[*Note 1*: This behavior can be implemented by a constructor template
with default template arguments. — *end note*]

The constructor is explicit if and only if `Tᵢ` is not implicitly
default-constructible for at least one i.

[*Note 2*: This behavior can be implemented with a trait that checks
whether a `const ``Tᵢ``&` can be initialized with `{}`. — *end note*]

``` cpp
\EXPLICIT constexpr tuple(const Types&...);
```

*Effects:* Initializes each element with the value of the corresponding
parameter.

*Remarks:* This constructor shall not participate in overload resolution
unless `sizeof...(Types) >= 1` and `is_copy_constructible_v<``Tᵢ``>` is
`true` for all i. The constructor is explicit if and only if
`is_convertible_v<const ``Tᵢ``&, ``Tᵢ``>` is `false` for at least one i.

``` cpp
template <class... UTypes> \EXPLICIT constexpr tuple(UTypes&&... u);
```

*Effects:* Initializes the elements in the tuple with the corresponding
value in `std::forward<UTypes>(u)`.

*Remarks:* This constructor shall not participate in overload resolution
unless `sizeof...(Types)` `==` `sizeof...(UTypes)` and
`sizeof...(Types) >= 1` and `is_constructible_v<``Tᵢ``, ``Uᵢ``&&>` is
`true` for all i. The constructor is explicit if and only if
`is_convertible_v<``Uᵢ``&&, ``Tᵢ``>` is `false` for at least one i.

``` cpp
tuple(const tuple& u) = default;
```

*Requires:* `is_copy_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* Initializes each element of `*this` with the corresponding
element of `u`.

``` cpp
tuple(tuple&& u) = default;
```

*Requires:* `is_move_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`std::forward<``Tᵢ``>(get<`i`>(u))`.

``` cpp
template <class... UTypes> \EXPLICIT constexpr tuple(const tuple<UTypes...>& u);
```

*Effects:* Initializes each element of `*this` with the corresponding
element of `u`.

*Remarks:* This constructor shall not participate in overload resolution
unless

- `sizeof...(Types)` `==` `sizeof...(UTypes)` and
- `is_constructible_v<``Tᵢ``, const ``Uᵢ``&>` is `true` for all i, and
- `sizeof...(Types) != 1`, or (when `Types...` expands to `T` and
  `UTypes...` expands to `U`)
  `!is_convertible_v<const tuple<U>&, T> && !is_constructible_v<T, const tuple<U>&>&& !is_same_v<T, U>`
  is `true`.

The constructor is explicit if and only if
`is_convertible_v<const ``Uᵢ``&, ``Tᵢ``>` is `false` for at least one i.

``` cpp
template <class... UTypes> \EXPLICIT constexpr tuple(tuple<UTypes...>&& u);
```

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`std::forward<``Uᵢ``>(get<`i`>(u))`.

*Remarks:* This constructor shall not participate in overload resolution
unless

- `sizeof...(Types)` `==` `sizeof...(UTypes)`, and
- `is_constructible_v<``Tᵢ``, ``Uᵢ``&&>` is `true` for all i, and
- `sizeof...(Types) != 1`, or (when `Types...` expands to `T` and
  `UTypes...` expands to `U`)
  `!is_convertible_v<tuple<U>, T> && !is_constructible_v<T, tuple<U>> &&!is_same_v<T, U>`
  is `true`.

The constructor is explicit if and only if
`is_convertible_v<``Uᵢ``&&, ``Tᵢ``>` is `false` for at least one i.

``` cpp
template <class U1, class U2> \EXPLICIT constexpr tuple(const pair<U1, U2>& u);
```

*Effects:* Initializes the first element with `u.first` and the second
element with `u.second`.

*Remarks:* This constructor shall not participate in overload resolution
unless `sizeof...(Types) == 2`, `is_constructible_v<``T₀``, const U1&>`
is `true` and `is_constructible_v<``T₁``, const U2&>` is `true`.

The constructor is explicit if and only if
`is_convertible_v<const U1&, ``T₀``>` is `false` or
`is_convertible_v<const U2&, ``T₁``>` is `false`.

``` cpp
template <class U1, class U2> \EXPLICIT constexpr tuple(pair<U1, U2>&& u);
```

*Effects:* Initializes the first element with
`std::forward<U1>(u.first)` and the second element with
`std::forward<U2>(u.second)`.

*Remarks:* This constructor shall not participate in overload resolution
unless `sizeof...(Types) == 2`, `is_constructible_v<``T₀``, U1&&>` is
`true` and `is_constructible_v<``T₁``, U2&&>` is `true`.

The constructor is explicit if and only if
`is_convertible_v<U1&&, ``T₀``>` is `false` or
`is_convertible_v<U2&&, ``T₁``>` is `false`.

``` cpp
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a);
template <class Alloc>
  \EXPLICIT tuple(allocator_arg_t, const Alloc& a, const Types&...);
template <class Alloc, class... UTypes>
  \EXPLICIT tuple(allocator_arg_t, const Alloc& a, UTypes&&...);
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a, const tuple&);
template <class Alloc>
  tuple(allocator_arg_t, const Alloc& a, tuple&&);
template <class Alloc, class... UTypes>
  \EXPLICIT tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
template <class Alloc, class... UTypes>
  \EXPLICIT tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
template <class Alloc, class U1, class U2>
  \EXPLICIT tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
template <class Alloc, class U1, class U2>
  \EXPLICIT tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);
```

*Requires:* `Alloc` shall meet the requirements for an
`Allocator` ([[allocator.requirements]]).

*Effects:* Equivalent to the preceding constructors except that each
element is constructed with uses-allocator
construction ([[allocator.uses.construction]]).

#### Assignment <a id="tuple.assign">[[tuple.assign]]</a>

For each `tuple` assignment operator, an exception is thrown only if the
assignment of one of the types in `Types` throws an exception. In the
function descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`) in order, `Tᵢ` be the iᵗʰ type in `Types`, and `Uᵢ`
be the iᵗʰ type in a template parameter pack named `UTypes`, where
indexing is zero-based.

``` cpp
tuple& operator=(const tuple& u);
```

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Remarks:* This operator shall be defined as deleted unless
`is_copy_assignable_v<``Tᵢ``>` is `true` for all i.

*Returns:* `*this`.

``` cpp
tuple& operator=(tuple&& u) noexcept(see below);
```

*Effects:* For all i, assigns `std::forward<``Tᵢ``>(get<`i`>(u))` to
`get<`i`>(*this)`.

*Remarks:* This operator shall be defined as deleted unless
`is_move_assignable_v<``Tᵢ``>` is `true` for all i.

*Remarks:* The expression inside `noexcept` is equivalent to the logical
<span class="smallcaps">and</span> of the following expressions:

``` cpp
is_nothrow_move_assignable_v<Tᵢ>
```

where Tᵢ is the iᵗʰ type in `Types`.

*Returns:* `*this`.

``` cpp
template <class... UTypes> tuple& operator=(const tuple<UTypes...>& u);
```

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Remarks:* This operator shall not participate in overload resolution
unless `sizeof...(Types) == sizeof...(UTypes)` and
`is_assignable_v<``Tᵢ``&, const ``Uᵢ``&>` is `true` for all i.

*Returns:* `*this`.

``` cpp
template <class... UTypes> tuple& operator=(tuple<UTypes...>&& u);
```

*Effects:* For all i, assigns `std::forward<``Uᵢ``>(get<`i`>(u))` to
`get<`i`>(*this)`.

*Remarks:* This operator shall not participate in overload resolution
unless `is_assignable_v<``Tᵢ``&, ``Uᵢ``&&> == true` for all i and
`sizeof...(Types) == sizeof...(UTypes)`.

*Returns:* `*this`.

``` cpp
template <class U1, class U2> tuple& operator=(const pair<U1, U2>& u);
```

*Effects:* Assigns `u.first` to the first element of `*this` and
`u.second` to the second element of `*this`.

*Remarks:* This operator shall not participate in overload resolution
unless `sizeof...(Types) == 2` and `is_assignable_v<``T₀``&, const U1&>`
is `true` for the first type `T₀` in `Types` and
`is_assignable_v<``T₁``&, const U2&>` is `true` for the second type `T₁`
in `Types`.

*Returns:* `*this`.

``` cpp
template <class U1, class U2> tuple& operator=(pair<U1, U2>&& u);
```

*Effects:* Assigns `std::forward<U1>(u.first)` to the first element of
`*this` and  
`std::forward<U2>(u.second)` to the second element of `*this`.

*Remarks:* This operator shall not participate in overload resolution
unless `sizeof...(Types) == 2` and `is_assignable_v<``T₀``&, U1&&>` is
`true` for the first type `T₀` in `Types` and
`is_assignable_v<``T₁``&, U2&&>` is `true` for the second type `T₁` in
`Types`.

*Returns:* `*this`.

#### `swap` <a id="tuple.swap">[[tuple.swap]]</a>

``` cpp
void swap(tuple& rhs) noexcept(see below);
```

*Requires:* Each element in `*this` shall be swappable
with ([[swappable.requirements]]) the corresponding element in `rhs`.

*Effects:* Calls `swap` for each element in `*this` and its
corresponding element in `rhs`.

*Remarks:* The expression inside `noexcept` is equivalent to the logical
<span class="smallcaps">and</span> of the following expressions:

``` cpp
is_nothrow_swappable_v<Tᵢ>
```

where Tᵢ is the iᵗʰ type in `Types`.

*Throws:* Nothing unless one of the element-wise `swap` calls throws an
exception.

#### Tuple creation functions <a id="tuple.creation">[[tuple.creation]]</a>

In the function descriptions that follow, the members of a parameter
pack `XTypes` are denoted by `X`ᵢ for i in \[`0`,
`sizeof...(`*X*`Types)`) in order, where indexing is zero-based.

``` cpp
template<class... TTypes>
  constexpr tuple<VTypes...> make_tuple(TTypes&&... t);
```

The pack `VTypes` is defined as follows. Let `U`ᵢ be `decay_t<T`ᵢ`>` for
each `T`ᵢ in `TTypes`. If `U`ᵢ is a specialization of
`reference_wrapper`, then `V`ᵢ in `VTypes` is `U`ᵢ`::type&`, otherwise
`V`ᵢ is `U`ᵢ.

*Returns:* `tuple<VTypes...>(std::forward<TTypes>(t)...)`.

[*Example 1*:

``` cpp
int i; float j;
make_tuple(1, ref(i), cref(j))
```

creates a tuple of type `tuple<int, int&, const float&>`.

— *end example*]

``` cpp
template<class... TTypes>
  constexpr tuple<TTypes&&...> forward_as_tuple(TTypes&&... t) noexcept;
```

*Effects:* Constructs a tuple of references to the arguments in `t`
suitable for forwarding as arguments to a function. Because the result
may contain references to temporary variables, a program shall ensure
that the return value of this function does not outlive any of its
arguments (e.g., the program should typically not store the result in a
named variable).

*Returns:* `tuple<TTypes&&...>(std::forward<TTypes>(t)...)`.

``` cpp
template<class... TTypes>
  constexpr tuple<TTypes&...> tie(TTypes&... t) noexcept;
```

*Returns:* `tuple<TTypes&...>(t...)`. When an argument in `t` is
`ignore`, assigning any value to the corresponding tuple element has no
effect.

[*Example 2*:

`tie` functions allow one to create tuples that unpack tuples into
variables. `ignore` can be used for elements that are not needed:

``` cpp
int i; std::string s;
tie(i, ignore, s) = make_tuple(42, 3.14, "C++");
// i == 42, s == "C++"
```

— *end example*]

``` cpp
template <class... Tuples>
  constexpr tuple<CTypes...> tuple_cat(Tuples&&... tpls);
```

In the following paragraphs, let `Tᵢ` be the iᵗʰ type in `Tuples`, `Uᵢ`
be `remove_reference_t<T`ᵢ`>`, and `tpᵢ` be the iᵗʰ parameter in the
function parameter pack `tpls`, where all indexing is zero-based.

*Requires:* For all i, `Uᵢ` shall be the type cvᵢ `tuple<``Argsᵢ``...>`,
where cvᵢ is the (possibly empty) iᵗʰ *cv-qualifier-seq* and `Argsᵢ` is
the parameter pack representing the element types in `Uᵢ`. Let `Aᵢk` be
the ${k}^\text{th}$ type in `Argsᵢ`. For all `Aᵢk` the following
requirements shall be satisfied:

- If `Tᵢ` is deduced as an lvalue reference type, then
  `is_constructible_v<``Aᵢk``, `cvᵢ `Aᵢk``&> == true`, otherwise
- `is_constructible_v<``Aᵢk``, `cvᵢ `Aᵢk``&&> == true`.

*Remarks:* The types in `CTypes` shall be equal to the ordered sequence
of the extended types `Args₀``..., ``Args₁``..., `…`, ``Argsₙ-1``...`,
where n is equal to `sizeof...(Tuples)`. Let `eᵢ``...` be the iᵗʰ
ordered sequence of tuple elements of the resulting `tuple` object
corresponding to the type sequence `Argsᵢ`.

*Returns:* A `tuple` object constructed by initializing the
${k_i}^\text{th}$ type element `eᵢk` in `eᵢ``...` with

``` cpp
get<kᵢ>(std::forward<$T_i$>($tp_i$))
```

for each valid kᵢ and each group `eᵢ` in order.

[*Note 1*: An implementation may support additional types in the
parameter pack `Tuples` that support the `tuple`-like protocol, such as
`pair` and `array`. — *end note*]

#### Calling a function with a `tuple` of arguments <a id="tuple.apply">[[tuple.apply]]</a>

``` cpp
template <class F, class Tuple>
  constexpr decltype(auto) apply(F&& f, Tuple&& t);
```

*Effects:* Given the exposition-only function:

``` cpp
template <class F, class Tuple, size_t... I>
constexpr decltype(auto)
    apply_impl(F&& f, Tuple&& t, index_sequence<I...>) {                // exposition only
  return INVOKE(std::forward<F>(f), std::get<I>(std::forward<Tuple>(t))...);
}
```

Equivalent to:

``` cpp
return apply_impl(std::forward<F>(f), std::forward<Tuple>(t),
                  make_index_sequence<tuple_size_v<decay_t<Tuple>>>{});
```

``` cpp
template <class T, class Tuple>
  constexpr T make_from_tuple(Tuple&& t);
```

*Effects:* Given the exposition-only function:

``` cpp
template <class T, class Tuple, size_t... I>
constexpr T make_from_tuple_impl(Tuple&& t, index_sequence<I...>) {     // exposition only
  return T(get<I>(std::forward<Tuple>(t))...);
}
```

Equivalent to:

``` cpp
return make_from_tuple_impl<T>(forward<Tuple>(t),
                               make_index_sequence<tuple_size_v<decay_t<Tuple>>>{});
```

[*Note 1*: The type of `T` must be supplied as an explicit template
parameter, as it cannot be deduced from the argument
list. — *end note*]

#### Tuple helper classes <a id="tuple.helper">[[tuple.helper]]</a>

``` cpp
template <class T> struct tuple_size;
```

*Remarks:* All specializations of `tuple_size` shall meet the
`UnaryTypeTrait` requirements ([[meta.rqmts]]) with a base
characteristic of `integral_constant<size_t, N>` for some `N`.

``` cpp
template <class... Types>
  class tuple_size<tuple<Types...>> : public integral_constant<size_t, sizeof...(Types)> { };
```

``` cpp
template <size_t I, class... Types>
  class tuple_element<I, tuple<Types...>> {
  public:
    using type = TI;
  };
```

*Requires:* `I < sizeof...(Types)`. The program is ill-formed if `I` is
out of bounds.

*Type:* `TI` is the type of the `I`th element of `Types`, where indexing
is zero-based.

``` cpp
template <class T> class tuple_size<const T>;
template <class T> class tuple_size<volatile T>;
template <class T> class tuple_size<const volatile T>;
```

Let *`TS`* denote `tuple_size<T>` of the cv-unqualified type `T`. If the
expression *`TS`*`::value` is well-formed when treated as an unevaluated
operand, then each of the three templates shall meet the
`UnaryTypeTrait` requirements ([[meta.rqmts]]) with a base
characteristic of

``` cpp
integral_constant<size_t, TS::value>
```

Otherwise, they shall have no member `value`.

Access checking is performed as if in a context unrelated to *`TS`* and
`T`. Only the validity of the immediate context of the expression is
considered.

[*Note 1*: The compilation of the expression can result in side effects
such as the instantiation of class template specializations and function
template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*]

In addition to being available via inclusion of the `<tuple>` header,
the three templates are available when either of the headers `<array>`
or `<utility>` are included.

``` cpp
template <size_t I, class T> class tuple_element<I, const T>;
template <size_t I, class T> class tuple_element<I, volatile T>;
template <size_t I, class T> class tuple_element<I, const volatile T>;
```

Let *`TE`* denote `tuple_element_t<I, T>` of the cv-unqualified type
`T`. Then each of the three templates shall meet the
`TransformationTrait` requirements ([[meta.rqmts]]) with a member
typedef `type` that names the following type:

- for the first specialization, `add_const_t<`*`TE`*`>`,
- for the second specialization, `add_volatile_t<`*`TE`*`>`, and
- for the third specialization, `add_cv_t<`*`TE`*`>`.

In addition to being available via inclusion of the `<tuple>` header,
the three templates are available when either of the headers `<array>`
or `<utility>` are included.

#### Element access <a id="tuple.elem">[[tuple.elem]]</a>

``` cpp
template <size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...>>&
    get(tuple<Types...>& t) noexcept;
template <size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...>>&&
    get(tuple<Types...>&& t) noexcept;        // Note A
template <size_t I, class... Types>
  constexpr const tuple_element_t<I, tuple<Types...>>&
    get(const tuple<Types...>& t) noexcept;   // Note B
template <size_t I, class... Types>
  constexpr const tuple_element_t<I, tuple<Types...>>&& get(const tuple<Types...>&& t) noexcept;
```

*Requires:* `I < sizeof...(Types)`. The program is ill-formed if `I` is
out of bounds.

*Returns:* A reference to the `I`th element of `t`, where indexing is
zero-based.

[*Note 1*: \[Note A\]If a `T` in `Types` is some reference type `X&`,
the return type is `X&`, not `X&&`. However, if the element type is a
non-reference type `T`, the return type is `T&&`. — *end note*]

[*Note 2*: \[Note B\]Constness is shallow. If a `T` in `Types` is some
reference type `X&`, the return type is `X&`, not `const X&`. However,
if the element type is a non-reference type `T`, the return type is
`const T&`. This is consistent with how constness is defined to work for
member variables of reference type. — *end note*]

``` cpp
template <class T, class... Types>
  constexpr T& get(tuple<Types...>& t) noexcept;
template <class T, class... Types>
  constexpr T&& get(tuple<Types...>&& t) noexcept;
template <class T, class... Types>
  constexpr const T& get(const tuple<Types...>& t) noexcept;
template <class T, class... Types>
  constexpr const T&& get(const tuple<Types...>&& t) noexcept;
```

*Requires:* The type `T` occurs exactly once in `Types...`. Otherwise,
the program is ill-formed.

*Returns:* A reference to the element of `t` corresponding to the type
`T` in `Types...`.

[*Example 1*:

``` cpp
const tuple<int, const int, double, double> t(1, 2, 3.4, 5.6);
  const int& i1 = get<int>(t);        // OK. Not ambiguous. i1 == 1
  const int& i2 = get<const int>(t);  // OK. Not ambiguous. i2 == 2
  const double& d = get<double>(t);   // ERROR. ill-formed
```

— *end example*]

[*Note 1*: The reason `get` is a non-member function is that if this
functionality had been provided as a member function, code where the
type depended on a template parameter would have required using the
`template` keyword. — *end note*]

#### Relational operators <a id="tuple.rel">[[tuple.rel]]</a>

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator==(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Requires:* For all `i`, where `0 <= i` and `i < sizeof...(TTypes)`,
`get<i>(t) == get<i>(u)` is a valid expression returning a type that is
convertible to `bool`. `sizeof...(TTypes)` `==` `sizeof...(UTypes)`.

*Returns:* `true` if `get<i>(t) == get<i>(u)` for all `i`, otherwise
`false`. For any two zero-length tuples `e` and `f`, `e == f` returns
`true`.

*Effects:* The elementary comparisons are performed in order from the
zeroth index upwards. No comparisons or element accesses are performed
after the first equality comparison that evaluates to `false`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator<(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Requires:* For all `i`, where `0 <= i` and `i < sizeof...(TTypes)`,
both `get<i>(t) < get<i>(u)` and `get<i>(u) < get<i>(t)` are valid
expressions returning types that are convertible to `bool`.
`sizeof...(TTypes)` `==` `sizeof...(UTypes)`.

*Returns:* The result of a lexicographical comparison between `t` and
`u`. The result is defined as:
`(bool)(get<0>(t) < get<0>(u)) || (!(bool)(get<0>(u) < get<0>(t)) && t`ₜₐᵢₗ` < u`ₜₐᵢₗ`)`,
where `r`ₜₐᵢₗ for some tuple `r` is a tuple containing all but the first
element of `r`. For any two zero-length tuples `e` and `f`, `e < f`
returns `false`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator!=(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `!(t == u)`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator>(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `u < t`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator<=(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `!(u < t)`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator>=(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Returns:* `!(t < u)`.

[*Note 1*: The above definitions for comparison functions do not
require `t_{tail}` (or `u_{tail}`) to be constructed. It may not even be
possible, as `t` and `u` are not required to be copy constructible.
Also, all comparison functions are short circuited; they do not perform
element accesses beyond what is required to determine the result of the
comparison. — *end note*]

#### Tuple traits <a id="tuple.traits">[[tuple.traits]]</a>

``` cpp
template <class... Types, class Alloc>
  struct uses_allocator<tuple<Types...>, Alloc> : true_type { };
```

*Requires:* `Alloc` shall be an
`Allocator` ([[allocator.requirements]]).

[*Note 1*: Specialization of this trait informs other library
components that `tuple` can be constructed with an allocator, even
though it does not have a nested `allocator_type`. — *end note*]

#### Tuple specialized algorithms <a id="tuple.special">[[tuple.special]]</a>

``` cpp
template <class... Types>
  void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);
```

*Remarks:* This function shall not participate in overload resolution
unless `is_swappable_v<``Tᵢ``>` is `true` for all i, where
0 ≤ i < `sizeof...(Types)`. The expression inside `noexcept` is
equivalent to:

``` cpp
noexcept(x.swap(y))
```

*Effects:* As if by `x.swap(y)`.

## Optional objects <a id="optional">[[optional]]</a>

### In general <a id="optional.general">[[optional.general]]</a>

This subclause describes class template `optional` that represents
optional objects. An *optional object* is an object that contains the
storage for another object and manages the lifetime of this contained
object, if any. The contained object may be initialized after the
optional object has been initialized, and may be destroyed before the
optional object has been destroyed. The initialization state of the
contained object is tracked by the optional object.

### Header `<optional>` synopsis <a id="optional.syn">[[optional.syn]]</a>

``` cpp
namespace std {
  // [optional.optional], class template optional
  template <class T>
    class optional;

  // [optional.nullopt], no-value state indicator
  struct nullopt_t{see below};
  inline constexpr nullopt_t nullopt(unspecified);

  // [optional.bad.access], class bad_optional_access
  class bad_optional_access;

  // [optional.relops], relational operators
  template <class T, class U>
  constexpr bool operator==(const optional<T>&, const optional<U>&);
  template <class T, class U>
  constexpr bool operator!=(const optional<T>&, const optional<U>&);
  template <class T, class U>
  constexpr bool operator<(const optional<T>&, const optional<U>&);
  template <class T, class U>
  constexpr bool operator>(const optional<T>&, const optional<U>&);
  template <class T, class U>
  constexpr bool operator<=(const optional<T>&, const optional<U>&);
  template <class T, class U>
  constexpr bool operator>=(const optional<T>&, const optional<U>&);

  // [optional.nullops], comparison with nullopt
  template <class T> constexpr bool operator==(const optional<T>&, nullopt_t) noexcept;
  template <class T> constexpr bool operator==(nullopt_t, const optional<T>&) noexcept;
  template <class T> constexpr bool operator!=(const optional<T>&, nullopt_t) noexcept;
  template <class T> constexpr bool operator!=(nullopt_t, const optional<T>&) noexcept;
  template <class T> constexpr bool operator<(const optional<T>&, nullopt_t) noexcept;
  template <class T> constexpr bool operator<(nullopt_t, const optional<T>&) noexcept;
  template <class T> constexpr bool operator<=(const optional<T>&, nullopt_t) noexcept;
  template <class T> constexpr bool operator<=(nullopt_t, const optional<T>&) noexcept;
  template <class T> constexpr bool operator>(const optional<T>&, nullopt_t) noexcept;
  template <class T> constexpr bool operator>(nullopt_t, const optional<T>&) noexcept;
  template <class T> constexpr bool operator>=(const optional<T>&, nullopt_t) noexcept;
  template <class T> constexpr bool operator>=(nullopt_t, const optional<T>&) noexcept;

  // [optional.comp_with_t], comparison with T
  template <class T, class U> constexpr bool operator==(const optional<T>&, const U&);
  template <class T, class U> constexpr bool operator==(const U&, const optional<T>&);
  template <class T, class U> constexpr bool operator!=(const optional<T>&, const U&);
  template <class T, class U> constexpr bool operator!=(const U&, const optional<T>&);
  template <class T, class U> constexpr bool operator<(const optional<T>&, const U&);
  template <class T, class U> constexpr bool operator<(const U&, const optional<T>&);
  template <class T, class U> constexpr bool operator<=(const optional<T>&, const U&);
  template <class T, class U> constexpr bool operator<=(const U&, const optional<T>&);
  template <class T, class U> constexpr bool operator>(const optional<T>&, const U&);
  template <class T, class U> constexpr bool operator>(const U&, const optional<T>&);
  template <class T, class U> constexpr bool operator>=(const optional<T>&, const U&);
  template <class T, class U> constexpr bool operator>=(const U&, const optional<T>&);

  // [optional.specalg], specialized algorithms
  template <class T>
    void swap(optional<T>&, optional<T>&) noexcept(see below);

  template <class T>
    constexpr optional<see below> make_optional(T&&);
  template <class T, class... Args>
    constexpr optional<T> make_optional(Args&&... args);
  template <class T, class U, class... Args>
    constexpr optional<T> make_optional(initializer_list<U> il, Args&&... args);

  // [optional.hash], hash support
  template <class T> struct hash;
  template <class T> struct hash<optional<T>>;
}
```

A program that necessitates the instantiation of template `optional` for
a reference type, or for possibly cv-qualified types `in_place_t` or
`nullopt_t` is ill-formed.

### Class template `optional` <a id="optional.optional">[[optional.optional]]</a>

``` cpp
template <class T>
  class optional {
  public:
    using value_type = T;

    // [optional.ctor], constructors
    constexpr optional() noexcept;
    constexpr optional(nullopt_t) noexcept;
    constexpr optional(const optional&);
    constexpr optional(optional&&) noexcept(see below);
    template <class... Args>
      constexpr explicit optional(in_place_t, Args&&...);
    template <class U, class... Args>
      constexpr explicit optional(in_place_t, initializer_list<U>, Args&&...);
    template <class U = T>
      \EXPLICIT constexpr optional(U&&);
    template <class U>
      \EXPLICIT optional(const optional<U>&);
    template <class U>
      \EXPLICIT optional(optional<U>&&);

    // [optional.dtor], destructor
    ~optional();

    // [optional.assign], assignment
    optional& operator=(nullopt_t) noexcept;
    optional& operator=(const optional&);
    optional& operator=(optional&&) noexcept(see below);
    template <class U = T> optional& operator=(U&&);
    template <class U> optional& operator=(const optional<U>&);
    template <class U> optional& operator=(optional<U>&&);
    template <class... Args> T& emplace(Args&&...);
    template <class U, class... Args> T& emplace(initializer_list<U>, Args&&...);

    // [optional.swap], swap
    void swap(optional&) noexcept(see below);

    // [optional.observe], observers
    constexpr const T* operator->() const;
    constexpr T* operator->();
    constexpr const T& operator*() const&;
    constexpr T& operator*() &;
    constexpr T&& operator*() &&;
    constexpr const T&& operator*() const&&;
    constexpr explicit operator bool() const noexcept;
    constexpr bool has_value() const noexcept;
    constexpr const T& value() const&;
    constexpr T& value() &;
    constexpr T&& value() &&;
    constexpr const T&& value() const&&;
    template <class U> constexpr T value_or(U&&) const&;
    template <class U> constexpr T value_or(U&&) &&;

    // [optional.mod], modifiers
    void reset() noexcept;

  private:
    T *val; // exposition only
  };

template<class T> optional(T) -> optional<T>;
```

Any instance of `optional<T>` at any given time either contains a value
or does not contain a value. When an instance of `optional<T>`
*contains a value*, it means that an object of type `T`, referred to as
the optional object’s *contained value*, is allocated within the storage
of the optional object. Implementations are not permitted to use
additional storage, such as dynamic memory, to allocate its contained
value. The contained value shall be allocated in a region of the
`optional<T>` storage suitably aligned for the type `T`. When an object
of type `optional<T>` is contextually converted to `bool`, the
conversion returns `true` if the object contains a value; otherwise the
conversion returns `false`.

Member `val` is provided for exposition only. When an `optional<T>`
object contains a value, `val` points to the contained value.

`T` shall be an object type and shall satisfy the requirements of
`Destructible` (Table  [[tab:destructible]]).

#### Constructors <a id="optional.ctor">[[optional.ctor]]</a>

``` cpp
constexpr optional() noexcept;
constexpr optional(nullopt_t) noexcept;
```

*Postconditions:* `*this` does not contain a value.

*Remarks:* No contained value is initialized. For every object type `T`
these constructors shall be constexpr constructors ([[dcl.constexpr]]).

``` cpp
constexpr optional(const optional& rhs);
```

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `*rhs`.

*Postconditions:* `bool(rhs) == bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* This constructor shall be defined as deleted unless
`is_copy_constructible_v<T>` is `true`. If
`is_trivially_copy_constructible_v<T>` is `true`, this constructor shall
be a `constexpr` constructor.

``` cpp
constexpr optional(optional&& rhs) noexcept(see below);
```

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `std::move(*rhs)`. `bool(rhs)` is unchanged.

*Postconditions:* `bool(rhs) == bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The expression inside `noexcept` is equivalent to
`is_nothrow_move_constructible_v<T>`. This constructor shall not
participate in overload resolution unless `is_move_constructible_v<T>`
is `true`. If `is_trivially_move_constructible_v<T>` is `true`, this
constructor shall be a `constexpr` constructor.

``` cpp
template <class... Args> constexpr explicit optional(in_place_t, Args&&... args);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If `T`’s constructor selected for the initialization is a
constexpr constructor, this constructor shall be a constexpr
constructor. This constructor shall not participate in overload
resolution unless `is_constructible_v<T, Args...>` is `true`.

``` cpp
template <class U, class... Args>
  constexpr explicit optional(in_place_t, initializer_list<U> il, Args&&... args);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`il, std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<T, initializer_list<U>&, Args&&...>` is
`true`. If `T`’s constructor selected for the initialization is a
constexpr constructor, this constructor shall be a constexpr
constructor.

[*Note 1*: The following constructors are conditionally specified as
explicit. This is typically implemented by declaring two such
constructors, of which at most one participates in overload
resolution. — *end note*]

``` cpp
template <class U = T> \EXPLICIT constexpr optional(U&& v);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the expression
`std::forward<U>(v)`.

*Postconditions:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If `T`’s selected constructor is a constexpr constructor,
this constructor shall be a constexpr constructor. This constructor
shall not participate in overload resolution unless
`is_constructible_v<T, U&&>` is `true`,
`is_same_v<decay_t<U>, in_place_t>` is `false`, and
`is_same_v<optional<T>, decay_t<U>>` is `false`. The constructor is
explicit if and only if `is_convertible_v<U&&, T>` is `false`.

``` cpp
template <class U> \EXPLICIT optional(const optional<U>& rhs);
```

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `*rhs`.

*Postconditions:* `bool(rhs)` == `bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* This constructor shall not participate in overload resolution
unless

- `is_constructible_v<T, const U&>` is `true`,
- `is_constructible_v<T, optional<U>&>` is `false`,
- `is_constructible_v<T, optional<U>&&>` is `false`,
- `is_constructible_v<T, const optional<U>&>` is `false`,
- `is_constructible_v<T, const optional<U>&&>` is `false`,
- `is_convertible_v<optional<U>&, T>` is `false`,
- `is_convertible_v<optional<U>&&, T>` is `false`,
- `is_convertible_v<const optional<U>&, T>` is `false`, and
- `is_convertible_v<const optional<U>&&, T>` is `false`.

The constructor is explicit if and only if
`is_convertible_v<const U&, T>` is `false`.

``` cpp
template <class U> \EXPLICIT optional(optional<U>&& rhs);
```

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `std::move(*rhs)`. `bool(rhs)` is unchanged.

*Postconditions:* `bool(rhs)` == `bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* This constructor shall not participate in overload resolution
unless

- `is_constructible_v<T, U&&>` is true,
- `is_constructible_v<T, optional<U>&>` is `false`,
- `is_constructible_v<T, optional<U>&&>` is `false`,
- `is_constructible_v<T, const optional<U>&>` is `false`,
- `is_constructible_v<T, const optional<U>&&>` is `false`,
- `is_convertible_v<optional<U>&, T>` is `false`,
- `is_convertible_v<optional<U>&&, T>` is `false`,
- `is_convertible_v<const optional<U>&, T>` is `false`, and
- `is_convertible_v<const optional<U>&&, T>` is `false`.

The constructor is explicit if and only if `is_convertible_v<U&&, T>` is
`false`.

#### Destructor <a id="optional.dtor">[[optional.dtor]]</a>

``` cpp
~optional();
```

*Effects:* If `is_trivially_destructible_v<T> != true` and `*this`
contains a value, calls

``` cpp
val->T::~T()
```

*Remarks:* If `is_trivially_destructible_v<T> == true` then this
destructor shall be a trivial destructor.

#### Assignment <a id="optional.assign">[[optional.assign]]</a>

``` cpp
optional<T>& operator=(nullopt_t) noexcept;
```

*Effects:* If `*this` contains a value, calls `val->T::T̃()` to destroy
the contained value; otherwise no effect.

*Returns:* `*this`.

*Postconditions:* `*this` does not contain a value.

``` cpp
optional<T>& operator=(const optional& rhs);
```

*Effects:* See Table  [[tab:optional.assign.copy]].

**Table: `optional::operator=(const optional&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                     |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `*rhs` to the contained value                  | initializes the contained value as if direct-non-list-initializing an object of type `T` with `*rhs` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                            |


*Returns:* `*this`.

*Postconditions:* `bool(rhs) == bool(*this)`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s copy constructor, no effect. If an exception is thrown
during the call to `T`’s copy assignment, the state of its contained
value is as defined by the exception safety guarantee of `T`’s copy
assignment. This operator shall be defined as deleted unless
`is_copy_constructible_v<T>` is `true` and `is_copy_assignable_v<T>` is
`true`.

``` cpp
optional<T>& operator=(optional&& rhs) noexcept(see below);
```

*Effects:* See Table  [[tab:optional.assign.move]]. The result of the
expression `bool(rhs)` remains unchanged.

**Table: `optional::operator=(optional&&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                                |
| ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `std::move(*rhs)` to the contained value       | initializes the contained value as if direct-non-list-initializing an object of type `T` with `std::move(*rhs)` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                                       |


*Returns:* `*this`.

*Postconditions:* `bool(rhs) == bool(*this)`.

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_move_assignable_v<T> && is_nothrow_move_constructible_v<T>
```

If any exception is thrown, the result of the expression `bool(*this)`
remains unchanged. If an exception is thrown during the call to `T`’s
move constructor, the state of `*rhs.val` is determined by the exception
safety guarantee of `T`’s move constructor. If an exception is thrown
during the call to `T`’s move assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s move
assignment. This operator shall not participate in overload resolution
unless `is_move_constructible_v<T>` is `true` and
`is_move_assignable_v<T>` is `true`.

``` cpp
template <class U = T> optional<T>& operator=(U&& v);
```

*Effects:* If `*this` contains a value, assigns `std::forward<U>(v)` to
the contained value; otherwise initializes the contained value as if
direct-non-list-initializing object of type `T` with
`std::forward<U>(v)`.

*Returns:* `*this`.

*Postconditions:* `*this` contains a value.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s constructor, the state of `v` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and `v`
is determined by the exception safety guarantee of `T`’s assignment.
This function shall not participate in overload resolution unless
`is_same_v<optional<T>, decay_t<U>>` is `false`,
`conjunction_v<is_scalar<T>, is_same<T, decay_t<U>>>` is `false`,
`is_constructible_v<T, U>` is `true`, and `is_assignable_v<T&, U>` is
`true`.

``` cpp
template <class U> optional<T>& operator=(const optional<U>& rhs);
```

*Effects:* See Table  [[tab:optional.assign.copy.templ]].

**Table: `optional::operator=(const optional<U>&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                     |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `*rhs` to the contained value                  | initializes the contained value as if direct-non-list-initializing an object of type `T` with `*rhs` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                            |


*Returns:* `*this`.

*Postconditions:* `bool(rhs) == bool(*this)`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s constructor, the state of `*rhs.val` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s
assignment. This function shall not participate in overload resolution
unless

- `is_constructible_v<T, const U&>` is `true`,
- `is_assignable_v<T&, const U&>` is `true`,
- `is_constructible_v<T, optional<U>&>` is `false`,
- `is_constructible_v<T, optional<U>&&>` is `false`,
- `is_constructible_v<T, const optional<U>&>` is `false`,
- `is_constructible_v<T, const optional<U>&&>` is `false`,
- `is_convertible_v<optional<U>&, T>` is `false`,
- `is_convertible_v<optional<U>&&, T>` is `false`,
- `is_convertible_v<const optional<U>&, T>` is `false`,
- `is_convertible_v<const optional<U>&&, T>` is `false`,
- `is_assignable_v<T&, optional<U>&>` is `false`,
- `is_assignable_v<T&, optional<U>&&>` is `false`,
- `is_assignable_v<T&, const optional<U>&>` is `false`, and
- `is_assignable_v<T&, const optional<U>&&>` is `false`.

``` cpp
template <class U> optional<T>& operator=(optional<U>&& rhs);
```

*Effects:* See Table  [[tab:optional.assign.move.templ]]. The result of
the expression `bool(rhs)` remains unchanged.

**Table: `optional::operator=(optional<U>&&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                                |
| ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `std::move(*rhs)` to the contained value       | initializes the contained value as if direct-non-list-initializing an object of type `T` with `std::move(*rhs)` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                                       |


*Returns:* `*this`.

*Postconditions:* `bool(rhs) == bool(*this)`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s constructor, the state of `*rhs.val` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s
assignment. This function shall not participate in overload resolution
unless

- `is_constructible_v<T, U>` is `true`,
- `is_assignable_v<T&, U>` is `true`,
- `is_constructible_v<T, optional<U>&>` is `false`,
- `is_constructible_v<T, optional<U>&&>` is `false`,
- `is_constructible_v<T, const optional<U>&>` is `false`,
- `is_constructible_v<T, const optional<U>&&>` is `false`,
- `is_convertible_v<optional<U>&, T>` is `false`,
- `is_convertible_v<optional<U>&&, T>` is `false`,
- `is_convertible_v<const optional<U>&, T>` is `false`,
- `is_convertible_v<const optional<U>&&, T>` is `false`,
- `is_assignable_v<T&, optional<U>&>` is `false`,
- `is_assignable_v<T&, optional<U>&&>` is `false`,
- `is_assignable_v<T&, const optional<U>&>` is `false`, and
- `is_assignable_v<T&, const optional<U>&&>` is `false`.

``` cpp
template <class... Args> T& emplace(Args&&... args);
```

*Requires:* `is_constructible_v<T, Args&&...>` is `true`.

*Effects:* Calls `*this = nullopt`. Then initializes the contained value
as if direct-non-list-initializing an object of type `T` with the
arguments `std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If an exception is thrown during the call to `T`’s
constructor, `*this` does not contain a value, and the previous `*val`
(if any) has been destroyed.

``` cpp
template <class U, class... Args> T& emplace(initializer_list<U> il, Args&&... args);
```

*Effects:* Calls `*this = nullopt`. Then initializes the contained value
as if direct-non-list-initializing an object of type `T` with the
arguments `il, std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If an exception is thrown during the call to `T`’s
constructor, `*this` does not contain a value, and the previous `*val`
(if any) has been destroyed. This function shall not participate in
overload resolution unless
`is_constructible_v<T, initializer_list<U>&, Args&&...>` is `true`.

#### Swap <a id="optional.swap">[[optional.swap]]</a>

``` cpp
void swap(optional& rhs) noexcept(see below);
```

*Requires:* Lvalues of type `T` shall be swappable and
`is_move_constructible_v<T>` is `true`.

*Effects:* See Table  [[tab:optional.swap]].

**Table: `optional::swap(optional&)` effects**

|                                | `*this` contains a value                                                                                                                                                                                                                                   | `*this` does not contain a value                                                                                                                                                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rhs` contains a value         | calls `swap(*(*this), *rhs)`                                                                                                                                                                                                                               | initializes the contained value of `*this` as if direct-non-list-initializing an object of type `T` with the expression `std::move(*rhs)`, followed by `rhs.val->T::~T()`; postcondition is that `*this` contains a value and `rhs` does not contain a value |
| `rhs` does not contain a value | initializes the contained value of `rhs` as if direct-non-list-initializing an object of type `T` with the expression `std::move(*(*this))`, followed by `val->T::~T()`; postcondition is that `*this` does not contain a value and `rhs` contains a value | no effect                                                                                                                                                                                                                                                    |


*Throws:* Any exceptions thrown by the operations in the relevant part
of Table  [[tab:optional.swap]].

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_move_constructible_v<T> && is_nothrow_swappable_v<T>
```

If any exception is thrown, the results of the expressions `bool(*this)`
and `bool(rhs)` remain unchanged. If an exception is thrown during the
call to function `swap`, the state of `*val` and `*rhs.val` is
determined by the exception safety guarantee of `swap` for lvalues of
`T`. If an exception is thrown during the call to `T`’s move
constructor, the state of `*val` and `*rhs.val` is determined by the
exception safety guarantee of `T`’s move constructor.

#### Observers <a id="optional.observe">[[optional.observe]]</a>

``` cpp
constexpr const T* operator->() const;
constexpr T* operator->();
```

*Requires:* `*this` contains a value.

*Returns:* `val`.

*Throws:* Nothing.

*Remarks:* These functions shall be constexpr functions.

``` cpp
constexpr const T& operator*() const&;
constexpr T& operator*() &;
```

*Requires:* `*this` contains a value.

*Returns:* `*val`.

*Throws:* Nothing.

*Remarks:* These functions shall be constexpr functions.

``` cpp
constexpr T&& operator*() &&;
constexpr const T&& operator*() const&&;
```

*Requires:* `*this` contains a value.

*Effects:* Equivalent to: `return std::move(*val);`

``` cpp
constexpr explicit operator bool() const noexcept;
```

*Returns:* `true` if and only if `*this` contains a value.

*Remarks:* This function shall be a constexpr function.

``` cpp
constexpr bool has_value() const noexcept;
```

*Returns:* `true` if and only if `*this` contains a value.

*Remarks:* This function shall be a constexpr function.

``` cpp
constexpr const T& value() const&;
constexpr T& value() &;
```

*Effects:* Equivalent to:

``` cpp
return bool(*this) ? *val : throw bad_optional_access();
```

``` cpp
constexpr T&& value() &&;
constexpr const T&& value() const&&;
```

*Effects:* Equivalent to:

``` cpp
return bool(*this) ? std::move(*val) : throw bad_optional_access();
```

``` cpp
template <class U> constexpr T value_or(U&& v) const&;
```

*Effects:* Equivalent to:

``` cpp
return bool(*this) ? **this : static_cast<T>(std::forward<U>(v));
```

*Remarks:* If `is_copy_constructible_v<T> && is_convertible_v<U&&, T>`
is `false`, the program is ill-formed.

``` cpp
template <class U> constexpr T value_or(U&& v) &&;
```

*Effects:* Equivalent to:

``` cpp
return bool(*this) ? std::move(**this) : static_cast<T>(std::forward<U>(v));
```

*Remarks:* If `is_move_constructible_v<T> && is_convertible_v<U&&, T>`
is `false`, the program is ill-formed.

#### Modifiers <a id="optional.mod">[[optional.mod]]</a>

``` cpp
void reset() noexcept;
```

*Effects:* If `*this` contains a value, calls `val->T::T̃()` to destroy
the contained value; otherwise no effect.

*Postconditions:* `*this` does not contain a value.

### No-value state indicator <a id="optional.nullopt">[[optional.nullopt]]</a>

``` cpp
struct nullopt_t{see below};
inline constexpr nullopt_t nullopt(unspecified);
```

The struct `nullopt_t` is an empty structure type used as a unique type
to indicate the state of not containing a value for `optional` objects.
In particular, `optional<T>` has a constructor with `nullopt_t` as a
single argument; this indicates that an optional object not containing a
value shall be constructed.

Type `nullopt_t` shall not have a default constructor or an
initializer-list constructor, and shall not be an aggregate.

### Class `bad_optional_access` <a id="optional.bad.access">[[optional.bad.access]]</a>

``` cpp
class bad_optional_access : public exception {
public:
  bad_optional_access();
};
```

The class `bad_optional_access` defines the type of objects thrown as
exceptions to report the situation where an attempt is made to access
the value of an optional object that does not contain a value.

``` cpp
bad_optional_access();
```

*Effects:* Constructs an object of class `bad_optional_access`.

*Postconditions:* `what()` returns an *implementation-defined* NTBS.

### Relational operators <a id="optional.relops">[[optional.relops]]</a>

``` cpp
template <class T, class U> constexpr bool operator==(const optional<T>& x, const optional<U>& y);
```

*Requires:* The expression `*x == *y` shall be well-formed and its
result shall be convertible to `bool`.

[*Note 1*: `T` need not be `EqualityComparable`. — *end note*]

*Returns:* If `bool(x) != bool(y)`, `false`; otherwise if
`bool(x) == false`, `true`; otherwise `*x == *y`.

*Remarks:* Specializations of this function template for which
`*x == *y` is a core constant expression shall be constexpr functions.

``` cpp
template <class T, class U> constexpr bool operator!=(const optional<T>& x, const optional<U>& y);
```

*Requires:* The expression `*x != *y` shall be well-formed and its
result shall be convertible to `bool`.

*Returns:* If `bool(x) != bool(y)`, `true`; otherwise, if
`bool(x) == false`, `false`; otherwise `*x != *y`.

*Remarks:* Specializations of this function template for which
`*x != *y` is a core constant expression shall be constexpr functions.

``` cpp
template <class T, class U> constexpr bool operator<(const optional<T>& x, const optional<U>& y);
```

*Requires:* `*x < *y` shall be well-formed and its result shall be
convertible to `bool`.

*Returns:* If `!y`, `false`; otherwise, if `!x`, `true`; otherwise
`*x < *y`.

*Remarks:* Specializations of this function template for which `*x < *y`
is a core constant expression shall be constexpr functions.

``` cpp
template <class T, class U> constexpr bool operator>(const optional<T>& x, const optional<U>& y);
```

*Requires:* The expression `*x > *y` shall be well-formed and its result
shall be convertible to `bool`.

*Returns:* If `!x`, `false`; otherwise, if `!y`, `true`; otherwise
`*x > *y`.

*Remarks:* Specializations of this function template for which `*x > *y`
is a core constant expression shall be constexpr functions.

``` cpp
template <class T, class U> constexpr bool operator<=(const optional<T>& x, const optional<U>& y);
```

*Requires:* The expression `*x <= *y` shall be well-formed and its
result shall be convertible to `bool`.

*Returns:* If `!x`, `true`; otherwise, if `!y`, `false`; otherwise
`*x <= *y`.

*Remarks:* Specializations of this function template for which
`*x <= *y` is a core constant expression shall be constexpr functions.

``` cpp
template <class T, class U> constexpr bool operator>=(const optional<T>& x, const optional<U>& y);
```

*Requires:* The expression `*x >= *y` shall be well-formed and its
result shall be convertible to `bool`.

*Returns:* If `!y`, `true`; otherwise, if `!x`, `false`; otherwise
`*x >= *y`.

*Remarks:* Specializations of this function template for which
`*x >= *y` is a core constant expression shall be constexpr functions.

### Comparison with `nullopt` <a id="optional.nullops">[[optional.nullops]]</a>

``` cpp
template <class T> constexpr bool operator==(const optional<T>& x, nullopt_t) noexcept;
template <class T> constexpr bool operator==(nullopt_t, const optional<T>& x) noexcept;
```

*Returns:* `!x`.

``` cpp
template <class T> constexpr bool operator!=(const optional<T>& x, nullopt_t) noexcept;
template <class T> constexpr bool operator!=(nullopt_t, const optional<T>& x) noexcept;
```

*Returns:* `bool(x)`.

``` cpp
template <class T> constexpr bool operator<(const optional<T>& x, nullopt_t) noexcept;
```

*Returns:* `false`.

``` cpp
template <class T> constexpr bool operator<(nullopt_t, const optional<T>& x) noexcept;
```

*Returns:* `bool(x)`.

``` cpp
template <class T> constexpr bool operator<=(const optional<T>& x, nullopt_t) noexcept;
```

*Returns:* `!x`.

``` cpp
template <class T> constexpr bool operator<=(nullopt_t, const optional<T>& x) noexcept;
```

*Returns:* `true`.

``` cpp
template <class T> constexpr bool operator>(const optional<T>& x, nullopt_t) noexcept;
```

*Returns:* `bool(x)`.

``` cpp
template <class T> constexpr bool operator>(nullopt_t, const optional<T>& x) noexcept;
```

*Returns:* `false`.

``` cpp
template <class T> constexpr bool operator>=(const optional<T>& x, nullopt_t) noexcept;
```

*Returns:* `true`.

``` cpp
template <class T> constexpr bool operator>=(nullopt_t, const optional<T>& x) noexcept;
```

*Returns:* `!x`.

### Comparison with `T` <a id="optional.comp_with_t">[[optional.comp_with_t]]</a>

``` cpp
template <class T, class U> constexpr bool operator==(const optional<T>& x, const U& v);
```

*Requires:* The expression `*x == v` shall be well-formed and its result
shall be convertible to `bool`.

[*Note 1*: `T` need not be `EqualityComparable`. — *end note*]

*Effects:* Equivalent to: `return bool(x) ? *x == v : false;`

``` cpp
template <class T, class U> constexpr bool operator==(const U& v, const optional<T>& x);
```

*Requires:* The expression `v == *x` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v == *x : false;`

``` cpp
template <class T, class U> constexpr bool operator!=(const optional<T>& x, const U& v);
```

*Requires:* The expression `*x != v` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x != v : true;`

``` cpp
template <class T, class U> constexpr bool operator!=(const U& v, const optional<T>& x);
```

*Requires:* The expression `v != *x` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v != *x : true;`

``` cpp
template <class T, class U> constexpr bool operator<(const optional<T>& x, const U& v);
```

*Requires:* The expression `*x < v` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x < v : true;`

``` cpp
template <class T, class U> constexpr bool operator<(const U& v, const optional<T>& x);
```

*Requires:* The expression `v < *x` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v < *x : false;`

``` cpp
template <class T, class U> constexpr bool operator<=(const optional<T>& x, const U& v);
```

*Requires:* The expression `*x <= v` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x <= v : true;`

``` cpp
template <class T, class U> constexpr bool operator<=(const U& v, const optional<T>& x);
```

*Requires:* The expression `v <= *x` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v <= *x : false;`

``` cpp
template <class T, class U> constexpr bool operator>(const optional<T>& x, const U& v);
```

*Requires:* The expression `*x > v` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x > v : false;`

``` cpp
template <class T, class U> constexpr bool operator>(const U& v, const optional<T>& x);
```

*Requires:* The expression `v > *x` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v > *x : true;`

``` cpp
template <class T, class U> constexpr bool operator>=(const optional<T>& x, const U& v);
```

*Requires:* The expression `*x >= v` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x >= v : false;`

``` cpp
template <class T, class U> constexpr bool operator>=(const U& v, const optional<T>& x);
```

*Requires:* The expression `v >= *x` shall be well-formed and its result
shall be convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v >= *x : true;`

### Specialized algorithms <a id="optional.specalg">[[optional.specalg]]</a>

``` cpp
template <class T> void swap(optional<T>& x, optional<T>& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* Calls `x.swap(y)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_move_constructible_v<T>` is `true` and `is_swappable_v<T>` is
`true`.

``` cpp
template <class T> constexpr optional<decay_t<T>> make_optional(T&& v);
```

*Returns:* `optional<decay_t<T>>(std::forward<T>(v))`.

``` cpp
template <class T, class...Args>
  constexpr optional<T> make_optional(Args&&... args);
```

*Effects:* Equivalent to:
`return optional<T>(in_place, std::forward<Args>(args)...);`

``` cpp
template <class T, class U, class... Args>
  constexpr optional<T> make_optional(initializer_list<U> il, Args&&... args);
```

*Effects:* Equivalent to:
`return optional<T>(in_place, il, std::forward<Args>(args)...);`

### Hash support <a id="optional.hash">[[optional.hash]]</a>

``` cpp
template <class T> struct hash<optional<T>>;
```

The specialization `hash<optional<T>>` is enabled ([[unord.hash]]) if
and only if `hash<remove_const_t<T>>` is enabled. When enabled, for an
object `o` of type `optional<T>`, if `bool(o) == true`, then
`hash<optional<T>>()(o)` shall evaluate to the same value as
`hash<remove_const_t<T>>()(*o)`; otherwise it evaluates to an
unspecified value. The member functions are not guaranteed to be
`noexcept`.

## Variants <a id="variant">[[variant]]</a>

### In general <a id="variant.general">[[variant.general]]</a>

A variant object holds and manages the lifetime of a value. If the
`variant` holds a value, that value’s type has to be one of the template
argument types given to variant. These template arguments are called
alternatives.

### Header `<variant>` synopsis <a id="variant.syn">[[variant.syn]]</a>

``` cpp
namespace std {
  // [variant.variant], class template variant
  template <class... Types>
    class variant;

  // [variant.helper], variant helper classes
  template <class T> struct variant_size;                   // not defined
  template <class T> struct variant_size<const T>;
  template <class T> struct variant_size<volatile T>;
  template <class T> struct variant_size<const volatile T>;
  template <class T>
    inline constexpr size_t variant_size_v = variant_size<T>::value;

  template <class... Types>
    struct variant_size<variant<Types...>>;

  template <size_t I, class T> struct variant_alternative;  // not defined
  template <size_t I, class T> struct variant_alternative<I, const T>;
  template <size_t I, class T> struct variant_alternative<I, volatile T>;
  template <size_t I, class T> struct variant_alternative<I, const volatile T>;
  template <size_t I, class T>
    using variant_alternative_t = typename variant_alternative<I, T>::type;

  template <size_t I, class... Types>
    struct variant_alternative<I, variant<Types...>>;

  inline constexpr size_t variant_npos = -1;

  // [variant.get], value access
  template <class T, class... Types>
    constexpr bool holds_alternative(const variant<Types...>&) noexcept;

  template <size_t I, class... Types>
    constexpr variant_alternative_t<I, variant<Types...>>& get(variant<Types...>&);
  template <size_t I, class... Types>
    constexpr variant_alternative_t<I, variant<Types...>>&& get(variant<Types...>&&);
  template <size_t I, class... Types>
    constexpr const variant_alternative_t<I, variant<Types...>>& get(const variant<Types...>&);
  template <size_t I, class... Types>
    constexpr const variant_alternative_t<I, variant<Types...>>&& get(const variant<Types...>&&);

  template <class T, class... Types>
    constexpr T& get(variant<Types...>&);
  template <class T, class... Types>
    constexpr T&& get(variant<Types...>&&);
  template <class T, class... Types>
    constexpr const T& get(const variant<Types...>&);
  template <class T, class... Types>
    constexpr const T&& get(const variant<Types...>&&);

  template <size_t I, class... Types>
    constexpr add_pointer_t<variant_alternative_t<I, variant<Types...>>>
      get_if(variant<Types...>*) noexcept;
  template <size_t I, class... Types>
    constexpr add_pointer_t<const variant_alternative_t<I, variant<Types...>>>
      get_if(const variant<Types...>*) noexcept;

  template <class T, class... Types>
    constexpr add_pointer_t<T>
      get_if(variant<Types...>*) noexcept;
  template <class T, class... Types>
    constexpr add_pointer_t<const T>
      get_if(const variant<Types...>*) noexcept;

  // [variant.relops], relational operators
  template <class... Types>
    constexpr bool operator==(const variant<Types...>&, const variant<Types...>&);
  template <class... Types>
    constexpr bool operator!=(const variant<Types...>&, const variant<Types...>&);
  template <class... Types>
    constexpr bool operator<(const variant<Types...>&, const variant<Types...>&);
  template <class... Types>
    constexpr bool operator>(const variant<Types...>&, const variant<Types...>&);
  template <class... Types>
    constexpr bool operator<=(const variant<Types...>&, const variant<Types...>&);
  template <class... Types>
    constexpr bool operator>=(const variant<Types...>&, const variant<Types...>&);

  // [variant.visit], visitation
  template <class Visitor, class... Variants>
    constexpr see below visit(Visitor&&, Variants&&...);

  // [variant.monostate], class monostate
  struct monostate;

  // [variant.monostate.relops], monostate relational operators
  constexpr bool operator<(monostate, monostate) noexcept;
  constexpr bool operator>(monostate, monostate) noexcept;
  constexpr bool operator<=(monostate, monostate) noexcept;
  constexpr bool operator>=(monostate, monostate) noexcept;
  constexpr bool operator==(monostate, monostate) noexcept;
  constexpr bool operator!=(monostate, monostate) noexcept;

  // [variant.specalg], specialized algorithms
  template <class... Types>
    void swap(variant<Types...>&, variant<Types...>&) noexcept(see below);

  // [variant.bad.access], class bad_variant_access
  class bad_variant_access;

  // [variant.hash], hash support
  template <class T> struct hash;
  template <class... Types> struct hash<variant<Types...>>;
  template <> struct hash<monostate>;

  // [variant.traits], allocator-related traits
  template <class T, class Alloc> struct uses_allocator;
  template <class... Types, class Alloc> struct uses_allocator<variant<Types...>, Alloc>;
}
```

### Class template `variant` <a id="variant.variant">[[variant.variant]]</a>

``` cpp
namespace std {
  template <class... Types>
    class variant {
    public:
      // [variant.ctor], constructors
      constexpr variant() noexcept(see below);
      variant(const variant&);
      variant(variant&&) noexcept(see below);

      template <class T>
        constexpr variant(T&&) noexcept(see below);

      template <class T, class... Args>
        constexpr explicit variant(in_place_type_t<T>, Args&&...);
      template <class T, class U, class... Args>
        constexpr explicit variant(in_place_type_t<T>, initializer_list<U>, Args&&...);

      template <size_t I, class... Args>
        constexpr explicit variant(in_place_index_t<I>, Args&&...);
      template <size_t I, class U, class... Args>
        constexpr explicit variant(in_place_index_t<I>, initializer_list<U>, Args&&...);

      // allocator-extended constructors
      template <class Alloc>
        variant(allocator_arg_t, const Alloc&);
      template <class Alloc>
        variant(allocator_arg_t, const Alloc&, const variant&);
      template <class Alloc>
        variant(allocator_arg_t, const Alloc&, variant&&);
      template <class Alloc, class T>
        variant(allocator_arg_t, const Alloc&, T&&);
      template <class Alloc, class T, class... Args>
        variant(allocator_arg_t, const Alloc&, in_place_type_t<T>, Args&&...);
      template <class Alloc, class T, class U, class... Args>
        variant(allocator_arg_t, const Alloc&, in_place_type_t<T>,
                initializer_list<U>, Args&&...);
      template <class Alloc, size_t I, class... Args>
        variant(allocator_arg_t, const Alloc&, in_place_index_t<I>, Args&&...);
      template <class Alloc, size_t I, class U, class... Args>
        variant(allocator_arg_t, const Alloc&, in_place_index_t<I>,
                initializer_list<U>, Args&&...);

      // [variant.dtor], destructor
      ~variant();

      // [variant.assign], assignment
      variant& operator=(const variant&);
      variant& operator=(variant&&) noexcept(see below);

      template <class T> variant& operator=(T&&) noexcept(see below);

      // [variant.mod], modifiers
      template <class T, class... Args>
        T& emplace(Args&&...);
      template <class T, class U, class... Args>
        T& emplace(initializer_list<U>, Args&&...);
      template <size_t I, class... Args>
        variant_alternative_t<I, variant<Types...>>& emplace(Args&&...);
      template <size_t I, class U, class... Args>
        variant_alternative_t<I, variant<Types...>>& emplace(initializer_list<U>, Args&&...);

      // [variant.status], value status
      constexpr bool valueless_by_exception() const noexcept;
      constexpr size_t index() const noexcept;

      // [variant.swap], swap
      void swap(variant&) noexcept(see below);
    };
}
```

Any instance of `variant` at any given time either holds a value of one
of its alternative types, or it holds no value. When an instance of
`variant` holds a value of alternative type `T`, it means that a value
of type `T`, referred to as the `variant` object’s *contained value*, is
allocated within the storage of the `variant` object. Implementations
are not permitted to use additional storage, such as dynamic memory, to
allocate the contained value. The contained value shall be allocated in
a region of the `variant` storage suitably aligned for all types in
`Types...`. It is *implementation-defined* whether over-aligned types
are supported.

All types in `Types...` shall be (possibly cv-qualified) object types
that are not arrays.

A program that instantiates the definition of `variant` with no template
arguments is ill-formed.

#### Constructors <a id="variant.ctor">[[variant.ctor]]</a>

In the descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`), and `Tᵢ` be the iᵗʰ type in `Types...`.

``` cpp
constexpr variant() noexcept(see below);
```

*Effects:* Constructs a `variant` holding a value-initialized value of
type `T₀`.

*Postconditions:* `valueless_by_exception()` is `false` and `index()` is
`0`.

*Throws:* Any exception thrown by the value-initialization of `T₀`.

*Remarks:* This function shall be `constexpr` if and only if the
value-initialization of the alternative type `T₀` would satisfy the
requirements for a constexpr function. The expression inside `noexcept`
is equivalent to `is_nothrow_default_constructible_v<``T₀``>`. This
function shall not participate in overload resolution unless
`is_default_constructible_v<``T₀``>` is `true`.

[*Note 1*: See also class `monostate`. — *end note*]

``` cpp
variant(const variant& w);
```

*Effects:* If `w` holds a value, initializes the `variant` to hold the
same alternative as `w` and direct-initializes the contained value with
`get<j>(w)`, where `j` is `w.index()`. Otherwise, initializes the
`variant` to not hold a value.

*Throws:* Any exception thrown by direct-initializing any `Tᵢ` for all
i.

*Remarks:* This function shall not participate in overload resolution
unless `is_copy_constructible_v<``Tᵢ``>` is `true` for all i.

``` cpp
variant(variant&& w) noexcept(see below);
```

*Effects:* If `w` holds a value, initializes the `variant` to hold the
same alternative as `w` and direct-initializes the contained value with
`get<j>(std::move(w))`, where `j` is `w.index()`. Otherwise, initializes
the `variant` to not hold a value.

*Throws:* Any exception thrown by move-constructing any `Tᵢ` for all i.

*Remarks:* The expression inside `noexcept` is equivalent to the logical
AND of `is_nothrow_move_constructible_v<``Tᵢ``>` for all i. This
function shall not participate in overload resolution unless
`is_move_constructible_v<``Tᵢ``>` is `true` for all i.

``` cpp
template <class T> constexpr variant(T&& t) noexcept(see below);
```

Let `Tⱼ` be a type that is determined as follows: build an imaginary
function *FUN*(Tᵢ) for each alternative type `Tᵢ`. The overload
*FUN*(Tⱼ) selected by overload resolution for the expression
*FUN*(std::forward\<T\>(t)) defines the alternative `Tⱼ` which is the
type of the contained value after construction.

*Effects:* Initializes `*this` to hold the alternative type `Tⱼ` and
direct-initializes the contained value as if
direct-non-list-initializing it with `std::forward<T>(t)`.

*Postconditions:* `holds_alternative<``Tⱼ``>(*this)` is `true`.

*Throws:* Any exception thrown by the initialization of the selected
alternative `Tⱼ`.

*Remarks:* This function shall not participate in overload resolution
unless `is_same_v<decay_t<T>, variant>` is `false`, unless `decay_t<T>`
is neither a specialization of `in_place_type_t` nor a specialization of
`in_place_index_t`, unless `is_constructible_v<``Tⱼ``, T>` is `true`,
and unless the expression *FUN*(`std::forward<T>(t))` (with *FUN* being
the above-mentioned set of imaginary functions) is well formed.

[*Note 2*:

``` cpp
variant<string, string> v("abc");
```

is ill-formed, as both alternative types have an equally viable
constructor for the argument.

— *end note*]

The expression inside `noexcept` is equivalent to
`is_nothrow_constructible_v<``Tⱼ``, T>`. If `Tⱼ`’s selected constructor
is a constexpr constructor, this constructor shall be a constexpr
constructor.

``` cpp
template <class T, class... Args> constexpr explicit variant(in_place_type_t<T>, Args&&... args);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`std::forward<Args>(args)...`.

*Postconditions:* `holds_alternative<T>(*this)` is `true`.

*Throws:* Any exception thrown by calling the selected constructor of
`T`.

*Remarks:* This function shall not participate in overload resolution
unless there is exactly one occurrence of `T` in `Types...` and
`is_constructible_v<T, Args...>` is `true`. If `T`’s selected
constructor is a constexpr constructor, this constructor shall be a
constexpr constructor.

``` cpp
template <class T, class U, class... Args>
  constexpr explicit variant(in_place_type_t<T>, initializer_list<U> il, Args&&... args);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`il, std::forward<Args>(args)...`.

*Postconditions:* `holds_alternative<T>(*this)` is `true`.

*Throws:* Any exception thrown by calling the selected constructor of
`T`.

*Remarks:* This function shall not participate in overload resolution
unless there is exactly one occurrence of `T` in `Types...` and
`is_constructible_v<T, initializer_list<U>&, Args...>` is `true`. If
`T`’s selected constructor is a constexpr constructor, this constructor
shall be a constexpr constructor.

``` cpp
template <size_t I, class... Args> constexpr explicit variant(in_place_index_t<I>, Args&&... args);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type $\texttt{T}_I$ with the
arguments `std::forward<Args>(args)...`.

*Postconditions:* `index()` is `I`.

*Throws:* Any exception thrown by calling the selected constructor of
$\texttt{T}_I$.

*Remarks:* This function shall not participate in overload resolution
unless

- `I` is less than `sizeof...(Types)` and
- `is_constructible_v<`$\texttt{T}_I$`, Args...>` is `true`.

If $\texttt{T}_I$’s selected constructor is a constexpr constructor,
this constructor shall be a constexpr constructor.

``` cpp
template <size_t I, class U, class... Args>
  constexpr explicit variant(in_place_index_t<I>, initializer_list<U> il, Args&&... args);
```

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type $\texttt{T}_I$ with the
arguments `il, std::forward<Args>(args)...`.

*Postconditions:* `index()` is `I`.

*Remarks:* This function shall not participate in overload resolution
unless

- `I` is less than `sizeof...(Types)` and
- `is_constructible_v<`$\texttt{T}_I$`, initializer_list<U>&, Args...>`
  is `true`.

If $\texttt{T}_I$’s selected constructor is a constexpr constructor,
this constructor shall be a constexpr constructor.

``` cpp
// allocator-extended constructors
template <class Alloc>
  variant(allocator_arg_t, const Alloc& a);
template <class Alloc>
  variant(allocator_arg_t, const Alloc& a, const variant& v);
template <class Alloc>
  variant(allocator_arg_t, const Alloc& a, variant&& v);
template <class Alloc, class T>
  variant(allocator_arg_t, const Alloc& a, T&& t);
template <class Alloc, class T, class... Args>
  variant(allocator_arg_t, const Alloc& a, in_place_type_t<T>, Args&&... args);
template <class Alloc, class T, class U, class... Args>
  variant(allocator_arg_t, const Alloc& a, in_place_type_t<T>,
          initializer_list<U> il, Args&&... args);
template <class Alloc, size_t I, class... Args>
  variant(allocator_arg_t, const Alloc& a, in_place_index_t<I>, Args&&... args);
template <class Alloc, size_t I, class U, class... Args>
  variant(allocator_arg_t, const Alloc& a, in_place_index_t<I>,
          initializer_list<U> il, Args&&... args);
```

*Requires:* `Alloc` shall meet the requirements for an
Allocator ([[allocator.requirements]]).

*Effects:* Equivalent to the preceding constructors except that the
contained value is constructed with uses-allocator
construction ([[allocator.uses.construction]]).

#### Destructor <a id="variant.dtor">[[variant.dtor]]</a>

``` cpp
~variant();
```

*Effects:* If `valueless_by_exception()` is `false`, destroys the
currently contained value.

*Remarks:* If `is_trivially_destructible_v<``Tᵢ``> == true` for all `Tᵢ`
then this destructor shall be a trivial destructor.

#### Assignment <a id="variant.assign">[[variant.assign]]</a>

``` cpp
variant& operator=(const variant& rhs);
```

Let j be `rhs.index()`.

*Effects:*

- If neither `*this` nor `rhs` holds a value, there is no effect.
  Otherwise,
- if `*this` holds a value but `rhs` does not, destroys the value
  contained in `*this` and sets `*this` to not hold a value. Otherwise,
- if `index() == `j, assigns the value contained in `rhs` to the value
  contained in `*this`. Otherwise,
- if either `is_nothrow_copy_constructible_v<``Tⱼ``>` or
  `!is_nothrow_move_constructible_v<``Tⱼ``>` is `true`, equivalent to
  `emplace<`j`>(get<`j`>(rhs))`. Otherwise,
- equivalent to `operator=(variant(rhs))`.

*Returns:* `*this`.

*Postconditions:* `index() == rhs.index()`.

*Remarks:* This function shall not participate in overload resolution
unless `is_copy_constructible_v<``Tᵢ``> &&`
`is_copy_assignable_v<``Tᵢ``>` is `true` for all i.

``` cpp
variant& operator=(variant&& rhs) noexcept(see below);
```

Let j be `rhs.index()`.

*Effects:*

- If neither `*this` nor `rhs` holds a value, there is no effect.
  Otherwise,
- if `*this` holds a value but `rhs` does not, destroys the value
  contained in `*this` and sets `*this` to not hold a value. Otherwise,
- if `index() == `j, assigns `get<`j`>(std::move(rhs))` to the value
  contained in `*this`. Otherwise,
- equivalent to `emplace<`j`>(get<`j`>(std::move(rhs)))`.

*Returns:* `*this`.

*Remarks:* This function shall not participate in overload resolution
unless `is_move_constructible_v<``Tᵢ``> && is_move_assignable_v<``Tᵢ``>`
is `true` for all i. The expression inside `noexcept` is equivalent to:
`is_nothrow_move_constructible_v<``Tᵢ``> && is_nothrow_move_assignable_v<``Tᵢ``>`
for all i.

- If an exception is thrown during the call to `Tⱼ`’s move construction
  (with j being `rhs.index())`, the `variant` will hold no value.
- If an exception is thrown during the call to `Tⱼ`’s move assignment,
  the state of the contained value is as defined by the exception safety
  guarantee of `Tⱼ`’s move assignment; `index()` will be j.

``` cpp
template <class T> variant& operator=(T&& t) noexcept(see below);
```

Let `Tⱼ` be a type that is determined as follows: build an imaginary
function *FUN*(Tᵢ) for each alternative type `Tᵢ`. The overload
*FUN*(Tⱼ) selected by overload resolution for the expression
*FUN*(std::forward\<T\>(t)) defines the alternative `Tⱼ` which is the
type of the contained value after assignment.

*Effects:*

- If `*this` holds a `Tⱼ`, assigns `std::forward<T>(t)` to the value
  contained in `*this`. Otherwise,
- if `is_nothrow_constructible_v<``Tⱼ``, T> ||`
  `!is_nothrow_move_constructible_v<``Tⱼ``>` is `true`, equivalent to
  `emplace<`j`>(std::forward<T>(t))`. Otherwise,
- equivalent to `operator=(variant(std::forward<T>(t)))`.

*Postconditions:* `holds_alternative<``Tⱼ``>(*this)` is `true`, with
`Tⱼ` selected by the imaginary function overload resolution described
above.

*Returns:* `*this`.

*Remarks:* This function shall not participate in overload resolution
unless `is_same_v<decay_t<T>, variant>` is `false`, unless
`is_assignable_v<``Tⱼ``&, T> && is_constructible_v<``Tⱼ``, T>` is
`true`, and unless the expression *FUN*(std::forward\<T\>(t)) (with
*FUN* being the above-mentioned set of imaginary functions) is well
formed.

[*Note 1*:

``` cpp
variant<string, string> v;
v = "abc";
```

is ill-formed, as both alternative types have an equally viable
constructor for the argument.

— *end note*]

The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_assignable_v<Tⱼ&, T> && is_nothrow_constructible_v<Tⱼ, T>
```

- If an exception is thrown during the assignment of
  `std::forward<T>(t)` to the value contained in `*this`, the state of
  the contained value and `t` are as defined by the exception safety
  guarantee of the assignment expression; `valueless_by_exception()`
  will be `false`.
- If an exception is thrown during the initialization of the contained
  value, the `variant` object might not hold a value.

#### Modifiers <a id="variant.mod">[[variant.mod]]</a>

``` cpp
template <class T, class... Args> T& emplace(Args&&... args);
```

Let I be the zero-based index of `T` in `Types...`.

*Effects:* Equivalent to:
`return emplace<`I`>(std::forward<Args>(args)...);`

*Remarks:* This function shall not participate in overload resolution
unless `is_constructible_v<T, Args...>` is `true`, and `T` occurs
exactly once in `Types...`.

``` cpp
template <class T, class U, class... Args> T& emplace(initializer_list<U> il, Args&&... args);
```

Let I be the zero-based index of `T` in `Types...`.

*Effects:* Equivalent to:
`return emplace<`I`>(il, std::forward<Args>(args)...);`

*Remarks:* This function shall not participate in overload resolution
unless `is_constructible_v<T, initializer_list<U>&, Args...>` is `true`,
and `T` occurs exactly once in `Types...`.

``` cpp
template <size_t I, class... Args>
  variant_alternative_t<I, variant<Types...>>& emplace(Args&&... args);
```

*Requires:* `I < sizeof...(Types)`.

*Effects:* Destroys the currently contained value if
`valueless_by_exception()` is `false`. Then initializes the contained
value as if direct-non-list-initializing a value of type $\texttt{T}_I$
with the arguments `std::forward<Args>(args)...`.

*Postconditions:* `index()` is `I`.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown during the initialization of the
contained value.

*Remarks:* This function shall not participate in overload resolution
unless `is_constructible_v<`$\texttt{T}_I$`, Args...>` is `true`. If an
exception is thrown during the initialization of the contained value,
the `variant` might not hold a value.

``` cpp
template <size_t I, class U, class... Args>
  variant_alternative_t<I, variant<Types...>>& emplace(initializer_list<U> il, Args&&... args);
```

*Requires:* `I < sizeof...(Types)`.

*Effects:* Destroys the currently contained value if
`valueless_by_exception()` is `false`. Then initializes the contained
value as if direct-non-list-initializing a value of type $\texttt{T}_I$
with the arguments `il, std::forward<Args>(args)...`.

*Postconditions:* `index()` is `I`.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown during the initialization of the
contained value.

*Remarks:* This function shall not participate in overload resolution
unless
`is_constructible_v<`$\texttt{T}_I$`, initializer_list<U>&, Args...>` is
`true`. If an exception is thrown during the initialization of the
contained value, the `variant` might not hold a value.

#### Value status <a id="variant.status">[[variant.status]]</a>

``` cpp
constexpr bool valueless_by_exception() const noexcept;
```

*Effects:* Returns `false` if and only if the `variant` holds a value.

[*Note 1*:

A `variant` might not hold a value if an exception is thrown during a
type-changing assignment or emplacement. The latter means that even a
`variant<float, int>` can become `valueless_by_exception()`, for
instance by

``` cpp
struct S { operator int() { throw 42; }};
variant<float, int> v{12.f};
v.emplace<1>(S());
```

— *end note*]

``` cpp
constexpr size_t index() const noexcept;
```

*Effects:* If `valueless_by_exception()` is `true`, returns
`variant_npos`. Otherwise, returns the zero-based index of the
alternative of the contained value.

#### Swap <a id="variant.swap">[[variant.swap]]</a>

``` cpp
void swap(variant& rhs) noexcept(see below);
```

*Requires:* Lvalues of type `Tᵢ` shall be
swappable ([[swappable.requirements]]) and
`is_move_constructible_v<``Tᵢ``>` shall be `true` for all i.

*Effects:*

- if `valueless_by_exception() && rhs.valueless_by_exception()` no
  effect. Otherwise,
- if `index() == rhs.index()`, calls
  `swap(get<`i`>(*this), get<`i`>(rhs))` where i is `index()`.
  Otherwise,
- exchanges values of `rhs` and `*this`.

*Throws:* If `index() == rhs.index()`, any exception thrown by
`swap(get<`i`>(*this), get<`i`>(rhs))` with i being `index()`.
Otherwise, any exception thrown by the move constructor of `Tᵢ` or `Tⱼ`
with i being `index()` and j being `rhs.index()`.

*Remarks:* If an exception is thrown during the call to function
`swap(get<`i`>(*this), get<`i`>(rhs))`, the states of the contained
values of `*this` and of `rhs` are determined by the exception safety
guarantee of `swap` for lvalues of `Tᵢ` with i being `index()`. If an
exception is thrown during the exchange of the values of `*this` and
`rhs`, the states of the values of `*this` and of `rhs` are determined
by the exception safety guarantee of `variant`’s move constructor. The
expression inside `noexcept` is equivalent to the logical AND of
`is_nothrow_move_constructible_v<``Tᵢ``> && is_nothrow_swappable_v<``Tᵢ``>`
for all i.

### `variant` helper classes <a id="variant.helper">[[variant.helper]]</a>

``` cpp
template <class T> struct variant_size;
```

*Remarks:* All specializations of `variant_size` shall meet the
`UnaryTypeTrait` requirements ([[meta.rqmts]]) with a base
characteristic of `integral_constant<size_t, N>` for some `N`.

``` cpp
template <class T> class variant_size<const T>;
template <class T> class variant_size<volatile T>;
template <class T> class variant_size<const volatile T>;
```

Let `VS` denote `variant_size<T>` of the cv-unqualified type `T`. Then
each of the three templates shall meet the `UnaryTypeTrait`
requirements ([[meta.rqmts]]) with a base characteristic of
`integral_constant<size_t, VS::value>`.

``` cpp
template <class... Types>
  struct variant_size<variant<Types...>> : integral_constant<size_t, sizeof...(Types)> { };
```

``` cpp
template <size_t I, class T> class variant_alternative<I, const T>;
template <size_t I, class T> class variant_alternative<I, volatile T>;
template <size_t I, class T> class variant_alternative<I, const volatile T>;
```

Let `VA` denote `variant_alternative<I, T>` of the cv-unqualified type
`T`. Then each of the three templates shall meet the
`TransformationTrait` requirements ([[meta.rqmts]]) with a member
typedef `type` that names the following type:

- for the first specialization, `add_const_t<VA::type>`,
- for the second specialization, `add_volatile_t<VA::type>`, and
- for the third specialization, `add_cv_t<VA::type>`.

``` cpp
variant_alternative<I, variant<Types...>>::type
```

*Requires:* `I < sizeof...(Types)`.

*Value:* The type $\texttt{T}_I$.

### Value access <a id="variant.get">[[variant.get]]</a>

``` cpp
template <class T, class... Types>
  constexpr bool holds_alternative(const variant<Types...>& v) noexcept;
```

*Requires:* The type `T` occurs exactly once in `Types...`. Otherwise,
the program is ill-formed.

*Returns:* `true` if `index()` is equal to the zero-based index of `T`
in `Types...`.

``` cpp
template <size_t I, class... Types>
  constexpr variant_alternative_t<I, variant<Types...>>& get(variant<Types...>& v);
template <size_t I, class... Types>
  constexpr variant_alternative_t<I, variant<Types...>>&& get(variant<Types...>&& v);
template <size_t I, class... Types>
  constexpr const variant_alternative_t<I, variant<Types...>>& get(const variant<Types...>& v);
template <size_t I, class... Types>
  constexpr const variant_alternative_t<I, variant<Types...>>&& get(const variant<Types...>&& v);
```

*Requires:* `I < sizeof...(Types)`. Otherwise the program is ill-formed.

*Effects:* If `v.index()` is `I`, returns a reference to the object
stored in the `variant`. Otherwise, throws an exception of type
`bad_variant_access`.

``` cpp
template <class T, class... Types> constexpr T& get(variant<Types...>& v);
template <class T, class... Types> constexpr T&& get(variant<Types...>&& v);
template <class T, class... Types> constexpr const T& get(const variant<Types...>& v);
template <class T, class... Types> constexpr const T&& get(const variant<Types...>&& v);
```

*Requires:* The type `T` occurs exactly once in `Types...`. Otherwise,
the program is ill-formed.

*Effects:* If `v` holds a value of type `T`, returns a reference to that
value. Otherwise, throws an exception of type `bad_variant_access`.

``` cpp
template <size_t I, class... Types>
  constexpr add_pointer_t<variant_alternative_t<I, variant<Types...>>>
    get_if(variant<Types...>* v) noexcept;
template <size_t I, class... Types>
  constexpr add_pointer_t<const variant_alternative_t<I, variant<Types...>>>
    get_if(const variant<Types...>* v) noexcept;
```

*Requires:* `I < sizeof...(Types)`. Otherwise the program is ill-formed.

*Returns:* A pointer to the value stored in the `variant`, if
`v != nullptr` and `v->index() == I`. Otherwise, returns `nullptr`.

``` cpp
template <class T, class... Types>
  constexpr add_pointer_t<T>
    get_if(variant<Types...>* v) noexcept;
template <class T, class... Types>
  constexpr add_pointer_t<const T>
    get_if(const variant<Types...>* v) noexcept;
```

*Requires:* The type `T` occurs exactly once in `Types...`. Otherwise,
the program is ill-formed.

*Effects:* Equivalent to: `return get_if<`i`>(v);` with i being the
zero-based index of `T` in `Types...`.

### Relational operators <a id="variant.relops">[[variant.relops]]</a>

``` cpp
template <class... Types>
  constexpr bool operator==(const variant<Types...>& v, const variant<Types...>& w);
```

*Requires:* `get<`i`>(v) == get<`i`>(w)` is a valid expression returning
a type that is convertible to `bool`, for all i.

*Returns:* If `v.index() != w.index()`, `false`; otherwise if
`v.valueless_by_exception()`, `true`; otherwise
`get<`i`>(v) == get<`i`>(w)` with i being `v.index()`.

``` cpp
template <class... Types>
  constexpr bool operator!=(const variant<Types...>& v, const variant<Types...>& w);
```

*Requires:* `get<`i`>(v) != get<`i`>(w)` is a valid expression returning
a type that is convertible to `bool`, for all i.

*Returns:* If `v.index() != w.index()`, `true`; otherwise if
`v.valueless_by_exception()`, `false`; otherwise
`get<`i`>(v) != get<`i`>(w)` with i being `v.index()`.

``` cpp
template <class... Types>
  constexpr bool operator<(const variant<Types...>& v, const variant<Types...>& w);
```

*Requires:* `get<`i`>(v) < get<`i`>(w)` is a valid expression returning
a type that is convertible to `bool`, for all i.

*Returns:* If `w.valueless_by_exception()`, `false`; otherwise if
`v.valueless_by_exception()`, `true`; otherwise, if
`v.index() < w.index()`, `true`; otherwise if `v.index() > w.index()`,
`false`; otherwise `get<`i`>(v) < get<`i`>(w)` with i being `v.index()`.

``` cpp
template <class... Types>
  constexpr bool operator>(const variant<Types...>& v, const variant<Types...>& w);
```

*Requires:* `get<`i`>(v) > get<`i`>(w)` is a valid expression returning
a type that is convertible to `bool`, for all i.

*Returns:* If `v.valueless_by_exception()`, `false`; otherwise if
`w.valueless_by_exception()`, `true`; otherwise, if
`v.index() > w.index()`, `true`; otherwise if `v.index() < w.index()`,
`false`; otherwise `get<`i`>(v) > get<`i`>(w)` with i being `v.index()`.

``` cpp
template <class... Types>
  constexpr bool operator<=(const variant<Types...>& v, const variant<Types...>& w);
```

*Requires:* `get<`i`>(v) <= get<`i`>(w)` is a valid expression returning
a type that is convertible to `bool`, for all i.

*Returns:* If `v.valueless_by_exception()`, `true`; otherwise if
`w.valueless_by_exception()`, `false`; otherwise, if
`v.index() < w.index()`, `true`; otherwise if `v.index() > w.index()`,
`false`; otherwise `get<`i`>(v) <= get<`i`>(w)` with i being
`v.index()`.

``` cpp
template <class... Types>
  constexpr bool operator>=(const variant<Types...>& v, const variant<Types...>& w);
```

*Requires:* `get<`i`>(v) >= get<`i`>(w)` is a valid expression returning
a type that is convertible to `bool`, for all i.

*Returns:* If `w.valueless_by_exception()`, `true`; otherwise if
`v.valueless_by_exception()`, `false`; otherwise, if
`v.index() > w.index()`, `true`; otherwise if `v.index() < w.index()`,
`false`; otherwise `get<`i`>(v) >= get<`i`>(w)` with i being
`v.index()`.

### Visitation <a id="variant.visit">[[variant.visit]]</a>

``` cpp
template <class Visitor, class... Variants>
  constexpr see below visit(Visitor&& vis, Variants&&... vars);
```

*Requires:* The expression in the *Effects:* element shall be a valid
expression of the same type and value category, for all combinations of
alternative types of all variants. Otherwise, the program is ill-formed.

*Effects:* Let `is...` be `vars.index()...`. Returns
*INVOKE*(forward\<Visitor\>(vis), get\<is\>(
`forward<Variants>(vars))...);`.

*Remarks:* The return type is the common type of all possible *`INVOKE`*
expressions of the *Effects:* element.

*Throws:* `bad_variant_access` if any `variant` in `vars` is
`valueless_by_exception()`.

*Complexity:* For `sizeof...(Variants) <= 1`, the invocation of the
callable object is implemented in constant time, i.e. it does not depend
on `sizeof...(Types).` For `sizeof...(Variants) > 1`, the invocation of
the callable object has no complexity requirements.

### Class `monostate` <a id="variant.monostate">[[variant.monostate]]</a>

``` cpp
struct monostate{};
```

The class `monostate` can serve as a first alternative type for a
`variant` to make the `variant` type default constructible.

### `monostate` relational operators <a id="variant.monostate.relops">[[variant.monostate.relops]]</a>

``` cpp
constexpr bool operator<(monostate, monostate) noexcept { return false; }
constexpr bool operator>(monostate, monostate) noexcept { return false; }
constexpr bool operator<=(monostate, monostate) noexcept { return true; }
constexpr bool operator>=(monostate, monostate) noexcept { return true; }
constexpr bool operator==(monostate, monostate) noexcept { return true; }
constexpr bool operator!=(monostate, monostate) noexcept { return false; }
```

[*Note 1*: `monostate` objects have only a single state; they thus
always compare equal. — *end note*]

### Specialized algorithms <a id="variant.specalg">[[variant.specalg]]</a>

``` cpp
template <class... Types>
  void swap(variant<Types...>& v, variant<Types...>& w) noexcept(see below);
```

*Effects:* Equivalent to `v.swap(w)`.

*Remarks:* This function shall not participate in overload resolution
unless `is_move_constructible_v<``Tᵢ``> && is_swappable_v<``Tᵢ``>` is
`true` for all i. The expression inside `noexcept` is equivalent to
`noexcept(v.swap(w))`.

### Class `bad_variant_access` <a id="variant.bad.access">[[variant.bad.access]]</a>

``` cpp
class bad_variant_access : public exception {
public:
  bad_variant_access() noexcept;
  const char* what() const noexcept override;
};
```

Objects of type `bad_variant_access` are thrown to report invalid
accesses to the value of a `variant` object.

``` cpp
bad_variant_access() noexcept;
```

Constructs a `bad_variant_access` object.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Hash support <a id="variant.hash">[[variant.hash]]</a>

``` cpp
template <class... Types> struct hash<variant<Types...>>;
```

The specialization `hash<variant<Types...>>` is
enabled ([[unord.hash]]) if and only if every specialization in
`hash<remove_const_t<Types>>...` is enabled. The member functions are
not guaranteed to be `noexcept`.

``` cpp
template <> struct hash<monostate>;
```

The specialization is enabled ([[unord.hash]]).

### Allocator-related traits <a id="variant.traits">[[variant.traits]]</a>

``` cpp
template <class... Types, class Alloc>
  struct uses_allocator<variant<Types...>, Alloc> : true_type { };
```

*Requires:* `Alloc` shall be an Allocator ([[allocator.requirements]]).

[*Note 1*: Specialization of this trait informs other library
components that variant can be constructed with an allocator, even
though it does not have a nested `allocator_type`. — *end note*]

## Storage for any type <a id="any">[[any]]</a>

This section describes components that C++programs may use to perform
operations on objects of a discriminated type.

[*Note 1*: The discriminated type may contain values of different types
but does not attempt conversion between them, i.e. `5` is held strictly
as an `int` and is not implicitly convertible either to `"5"` or to
`5.0`. This indifference to interpretation but awareness of type
effectively allows safe, generic containers of single values, with no
scope for surprises from ambiguous conversions. — *end note*]

### Header `<any>` synopsis <a id="any.synop">[[any.synop]]</a>

``` cpp
namespace std {
  // [any.bad_any_cast], class bad_any_cast
  class bad_any_cast;

  // [any.class], class any
  class any;

  // [any.nonmembers], non-member functions
  void swap(any& x, any& y) noexcept;

  template <class T, class... Args>
    any make_any(Args&& ...args);
  template <class T, class U, class... Args>
    any make_any(initializer_list<U> il, Args&& ...args);

  template<class T>
    T any_cast(const any& operand);
  template<class T>
    T any_cast(any& operand);
  template<class T>
    T any_cast(any&& operand);

  template<class T>
    const T* any_cast(const any* operand) noexcept;
  template<class T>
    T* any_cast(any* operand) noexcept;
}
```

### Class `bad_any_cast` <a id="any.bad_any_cast">[[any.bad_any_cast]]</a>

``` cpp
class bad_any_cast : public bad_cast {
public:
  const char* what() const noexcept override;
};
```

Objects of type `bad_any_cast` are thrown by a failed `any_cast` (
[[any.nonmembers]]).

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

*Remarks:* The message may be a null-terminated multibyte
string ([[multibyte.strings]]), suitable for conversion and display as
a wstring ([[string.classes]], [[locale.codecvt]]).

### Class `any` <a id="any.class">[[any.class]]</a>

``` cpp
class any {
public:
  // [any.cons], construction and destruction
  constexpr any() noexcept;

  any(const any& other);
  any(any&& other) noexcept;

  template <class T> any(T&& value);

  template <class T, class... Args>
    explicit any(in_place_type_t<T>, Args&&...);
  template <class T, class U, class... Args>
    explicit any(in_place_type_t<T>, initializer_list<U>, Args&&...);

  ~any();

  // [any.assign], assignments
  any& operator=(const any& rhs);
  any& operator=(any&& rhs) noexcept;

  template <class T> any& operator=(T&& rhs);

  // [any.modifiers], modifiers
  template <class T, class... Args>
    decay_t<T>& emplace(Args&& ...);
  template <class T, class U, class... Args>
    decay_t<T>& emplace(initializer_list<U>, Args&&...);
  void reset() noexcept;
  void swap(any& rhs) noexcept;

  // [any.observers], observers
  bool has_value() const noexcept;
  const type_info& type() const noexcept;
};
```

An object of class `any` stores an instance of any type that satisfies
the constructor requirements or it has no value, and this is referred to
as the *state* of the class `any` object. The stored instance is called
the *contained value*, Two states are equivalent if either they both
have no value, or both have a value and the contained values are
equivalent.

The non-member `any_cast` functions provide type-safe access to the
contained value.

Implementations should avoid the use of dynamically allocated memory for
a small contained value.

[*Example 1*: where the object constructed is holding only an
`int`. — *end example*]

Such small-object optimization shall only be applied to types `T` for
which `is_nothrow_move_constructible_v<T>` is `true`.

#### Construction and destruction <a id="any.cons">[[any.cons]]</a>

``` cpp
constexpr any() noexcept;
```

*Postconditions:* `has_value()` is `false`.

``` cpp
any(const any& other);
```

*Effects:* If `other.has_value()` is `false`, constructs an object that
has no value. Otherwise, equivalent to
`any(in_place<T>, any_cast<const T&>(other))` where `T` is the type of
the contained object.

*Throws:* Any exceptions arising from calling the selected constructor
for the contained value.

``` cpp
any(any&& other) noexcept;
```

*Effects:* If `other.has_value()` is `false`, constructs an object that
has no value. Otherwise, constructs an object of type `any` that
contains either the contained object of `other`, or contains an object
of the same type constructed from the contained object of `other`
considering that contained object as an rvalue.

*Postconditions:* `other` is left in a valid but otherwise unspecified
state.

``` cpp
template<class T>
  any(T&& value);
```

Let `VT` be `decay_t<T>`.

*Requires:* `VT` shall satisfy the `CopyConstructible` requirements.

*Effects:* Constructs an object of type `any` that contains an object of
type `VT` direct-initialized with `std::forward<T>(value)`.

*Remarks:* This constructor shall not participate in overload resolution
unless `VT` is not the same type as `any`, `VT` is not a specialization
of `in_place_type_t`, and `is_copy_constructible_v<VT>` is `true`.

*Throws:* Any exception thrown by the selected constructor of `VT`.

``` cpp
template <class T, class... Args>
  explicit any(in_place_type_t<T>, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Requires:* `VT` shall satisfy the `CopyConstructible` requirements.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value of type `VT`.

*Throws:* Any exception thrown by the selected constructor of `VT`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_copy_constructible_v<VT>` is `true` and
`is_constructible_v<VT, Args...>` is `true`.

``` cpp
template <class T, class U, class... Args>
  explicit any(in_place_type_t<T>, initializer_list<U> il, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Requires:* `VT` shall satisfy the `CopyConstructible` requirements.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`il, std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `VT`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_copy_constructible_v<VT>` is `true` and
`is_constructible_v<VT, initializer_list<U>&, Args...>` is `true`.

``` cpp
~any();
```

*Effects:* As if by `reset()`.

#### Assignment <a id="any.assign">[[any.assign]]</a>

``` cpp
any& operator=(const any& rhs);
```

*Effects:* As if by `any(rhs).swap(*this)`. No effects if an exception
is thrown.

*Returns:* `*this`.

*Throws:* Any exceptions arising from the copy constructor for the
contained value.

``` cpp
any& operator=(any&& rhs) noexcept;
```

*Effects:* As if by `any(std::move(rhs)).swap(*this)`.

*Returns:* `*this`.

*Postconditions:* The state of `*this` is equivalent to the original
state of `rhs` and `rhs` is left in a valid but otherwise unspecified
state.

``` cpp
template<class T>
  any& operator=(T&& rhs);
```

Let `VT` be `decay_t<T>`.

*Requires:* `VT` shall satisfy the `CopyConstructible` requirements.

*Effects:* Constructs an object `tmp` of type `any` that contains an
object of type `VT` direct-initialized with `std::forward<T>(rhs)`, and
`tmp.swap(*this)`. No effects if an exception is thrown.

*Returns:* `*this`.

*Remarks:* This operator shall not participate in overload resolution
unless `VT` is not the same type as `any` and
`is_copy_constructible_v<VT>` is `true`.

*Throws:* Any exception thrown by the selected constructor of `VT`.

#### Modifiers <a id="any.modifiers">[[any.modifiers]]</a>

``` cpp
template <class T, class... Args>
  decay_t<T>& emplace(Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Requires:* `VT` shall satisfy the `CopyConstructible` requirements.

*Effects:* Calls `reset()`. Then initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `VT`.

*Remarks:* If an exception is thrown during the call to `VT`’s
constructor, `*this` does not contain a value, and any previously
contained value has been destroyed. This function shall not participate
in overload resolution unless `is_copy_constructible_v<VT>` is `true`
and `is_constructible_v<VT, Args...>` is `true`.

``` cpp
template <class T, class U, class... Args>
  decay_t<T>& emplace(initializer_list<U> il, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Requires:* `VT` shall satisfy the `CopyConstructible` requirements.

*Effects:* Calls `reset()`. Then initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`il, std::forward<Args>(args)...`.

*Postconditions:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `VT`.

*Remarks:* If an exception is thrown during the call to `VT`’s
constructor, `*this` does not contain a value, and any previously
contained value has been destroyed. The function shall not participate
in overload resolution unless `is_copy_constructible_v<VT>` is `true`
and `is_constructible_v<VT, initializer_list<U>&, Args...>` is `true`.

``` cpp
void reset() noexcept;
```

*Effects:* If `has_value()` is `true`, destroys the contained value.

*Postconditions:* `has_value()` is `false`.

``` cpp
void swap(any& rhs) noexcept;
```

*Effects:* Exchanges the states of `*this` and `rhs`.

#### Observers <a id="any.observers">[[any.observers]]</a>

``` cpp
bool has_value() const noexcept;
```

*Returns:* `true` if `*this` contains an object, otherwise `false`.

``` cpp
const type_info& type() const noexcept;
```

*Returns:* `typeid(T)` if `*this` has a contained value of type `T`,
otherwise `typeid(void)`.

[*Note 1*: Useful for querying against types known either at compile
time or only at runtime. — *end note*]

### Non-member functions <a id="any.nonmembers">[[any.nonmembers]]</a>

``` cpp
void swap(any& x, any& y) noexcept;
```

*Effects:* As if by `x.swap(y)`.

``` cpp
template <class T, class... Args>
  any make_any(Args&& ...args);
```

*Effects:* Equivalent to:
`return any(in_place_type<T>, std::forward<Args>(args)...);`

``` cpp
template <class T, class U, class... Args>
  any make_any(initializer_list<U> il, Args&& ...args);
```

*Effects:* Equivalent to:
`return any(in_place_type<T>, il, std::forward<Args>(args)...);`

``` cpp
template<class T>
  T any_cast(const any& operand);
template<class T>
  T any_cast(any& operand);
template<class T>
  T any_cast(any&& operand);
```

Let `U` be the type `remove_cv_t<remove_reference_t<ValueType>>`.

*Requires:* For the first overload,
`is_constructible_v<ValueType, const U&>` is `true`. For the second
overload, `is_constructible_v<ValueType, U&>` is `true`. For the third
overload, `is_constructible_v<ValueType, U>` is `true`. Otherwise the
program is ill-formed.

*Returns:* For the first and second overload,
`static_cast<ValueType>(*any_cast<U>(&operand))`. For the third
overload, `static_cast<ValueType>(std::move(*any_cast<U>(&operand)))`.

*Throws:* `bad_any_cast` if
`operand.type() != typeid(remove_reference_t<T>)`.

[*Example 1*:

``` cpp
any x(5);                                   // x holds int
assert(any_cast<int>(x) == 5);              // cast to value
any_cast<int&>(x) = 10;                     // cast to reference
assert(any_cast<int>(x) == 10);

x = "Meow";                                 // x holds const char*
assert(strcmp(any_cast<const char*>(x), "Meow") == 0);
any_cast<const char*&>(x) = "Harry";
assert(strcmp(any_cast<const char*>(x), "Harry") == 0);

x = string("Meow");                         // x holds string
string s, s2("Jane");
s = move(any_cast<string&>(x));             // move from any
assert(s == "Meow");
any_cast<string&>(x) = move(s2);            // move to any
assert(any_cast<const string&>(x) == "Jane");

string cat("Meow");
const any y(cat);                           // const y holds string
assert(any_cast<const string&>(y) == cat);

any_cast<string&>(y);                       // error; cannot
                                            // any_cast away const
```

— *end example*]

``` cpp
template<class T>
  const T* any_cast(const any* operand) noexcept;
template<class T>
  T* any_cast(any* operand) noexcept;
```

*Returns:* If `operand != nullptr && operand->type() == typeid(T)`, a
pointer to the object contained by `operand`; otherwise, `nullptr`.

[*Example 2*:

``` cpp
bool is_string(const any& operand) {
  return any_cast<string>(&operand) != nullptr;
}
```

— *end example*]

## Bitsets <a id="bitset">[[bitset]]</a>

### Header `<bitset>` synopsis <a id="bitset.syn">[[bitset.syn]]</a>

``` cpp
#include <string>
#include <iosfwd>   // for istream ([istream.syn]), ostream ([ostream.syn]), see [iosfwd.syn]

namespace std {
  template <size_t N> class bitset;

  // [bitset.operators], bitset operators
  template <size_t N>
    bitset<N> operator&(const bitset<N>&, const bitset<N>&) noexcept;
  template <size_t N>
    bitset<N> operator|(const bitset<N>&, const bitset<N>&) noexcept;
  template <size_t N>
    bitset<N> operator^(const bitset<N>&, const bitset<N>&) noexcept;
  template <class charT, class traits, size_t N>
    basic_istream<charT, traits>&
      operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
  template <class charT, class traits, size_t N>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const bitset<N>& x);
}
```

The header `<bitset>` defines a class template and several related
functions for representing and manipulating fixed-size sequences of
bits.

### Class template `bitset` <a id="template.bitset">[[template.bitset]]</a>

``` cpp
namespace std {
  template<size_t N> class bitset {
  public:
    // bit reference:
    class reference {
      friend class bitset;
      reference() noexcept;
    public:
      ~reference() noexcept;
      reference& operator=(bool x) noexcept;             // for b[i] = x;
      reference& operator=(const reference&) noexcept;   // for b[i] = b[j];
      bool operator~() const noexcept;                   // flips the bit
      operator bool() const noexcept;                    // for x = b[i];
      reference& flip() noexcept;                        // for b[i].flip();
    };

    // [bitset.cons], constructors
    constexpr bitset() noexcept;
    constexpr bitset(unsigned long long val) noexcept;
    template<class charT, class traits, class Allocator>
      explicit bitset(
        const basic_string<charT, traits, Allocator>& str,
        typename basic_string<charT, traits, Allocator>::size_type pos = 0,
        typename basic_string<charT, traits, Allocator>::size_type n =
          basic_string<charT, traits, Allocator>::npos,
        charT zero = charT('0'),
        charT one = charT('1'));
    template <class charT>
      explicit bitset(
        const charT* str,
        typename basic_string<charT>::size_type n = basic_string<charT>::npos,
        charT zero = charT('0'),
        charT one = charT('1'));

    // [bitset.members], bitset operations
    bitset<N>& operator&=(const bitset<N>& rhs) noexcept;
    bitset<N>& operator|=(const bitset<N>& rhs) noexcept;
    bitset<N>& operator^=(const bitset<N>& rhs) noexcept;
    bitset<N>& operator<<=(size_t pos) noexcept;
    bitset<N>& operator>>=(size_t pos) noexcept;
    bitset<N>& set() noexcept;
    bitset<N>& set(size_t pos, bool val = true);
    bitset<N>& reset() noexcept;
    bitset<N>& reset(size_t pos);
    bitset<N>  operator~() const noexcept;
    bitset<N>& flip() noexcept;
    bitset<N>& flip(size_t pos);

    // element access:
    constexpr bool operator[](size_t pos) const;       // for b[i];
    reference operator[](size_t pos);                  // for b[i];

    unsigned long to_ulong() const;
    unsigned long long to_ullong() const;
    template <class charT = char,
              class traits = char_traits<charT>,
              class Allocator = allocator<charT>>
      basic_string<charT, traits, Allocator>
        to_string(charT zero = charT('0'), charT one = charT('1')) const;

    size_t count() const noexcept;
    constexpr size_t size() const noexcept;
    bool operator==(const bitset<N>& rhs) const noexcept;
    bool operator!=(const bitset<N>& rhs) const noexcept;
    bool test(size_t pos) const;
    bool all() const noexcept;
    bool any() const noexcept;
    bool none() const noexcept;
    bitset<N> operator<<(size_t pos) const noexcept;
    bitset<N> operator>>(size_t pos) const noexcept;
  };

  // [bitset.hash], hash support
  template <class T> struct hash;
  template <size_t N> struct hash<bitset<N>>;
}
```

The class template `bitset<N>` describes an object that can store a
sequence consisting of a fixed number of bits, `N`.

Each bit represents either the value zero (reset) or one (set). To
*toggle* a bit is to change the value zero to one, or the value one to
zero. Each bit has a non-negative position `pos`. When converting
between an object of class `bitset<N>` and a value of some integral
type, bit position `pos` corresponds to the *bit value* `1 << pos`. The
integral value corresponding to two or more bits is the sum of their bit
values.

The functions described in this subclause can report three kinds of
errors, each associated with a distinct exception:

- an *invalid-argument* error is associated with exceptions of type
  `invalid_argument` ([[invalid.argument]]);
- an *out-of-range* error is associated with exceptions of type
  `out_of_range` ([[out.of.range]]);
- an *overflow* error is associated with exceptions of type
  `overflow_error` ([[overflow.error]]).

#### `bitset` constructors <a id="bitset.cons">[[bitset.cons]]</a>

``` cpp
constexpr bitset() noexcept;
```

*Effects:* Constructs an object of class `bitset<N>`, initializing all
bits to zero.

``` cpp
constexpr bitset(unsigned long long val) noexcept;
```

*Effects:* Constructs an object of class `bitset<N>`, initializing the
first `M` bit positions to the corresponding bit values in `val`. `M` is
the smaller of `N` and the number of bits in the value
representation ([[basic.types]]) of `unsigned long long`. If `M < N`,
the remaining bit positions are initialized to zero.

``` cpp
template <class charT, class traits, class Allocator>
explicit
bitset(const basic_string<charT, traits, Allocator>& str,
       typename basic_string<charT, traits, Allocator>::size_type pos = 0,
       typename basic_string<charT, traits, Allocator>::size_type n =
         basic_string<charT, traits, Allocator>::npos,
         charT zero = charT('0'), charT one = charT('1'));
```

*Throws:* `out_of_range` if `pos > str.size()` or `invalid_argument` if
an invalid character is found (see below).

*Effects:* Determines the effective length `rlen` of the initializing
string as the smaller of `n` and `str.size() - pos`.

The function then throws

`invalid_argument` if any of the `rlen` characters in `str` beginning at
position `pos` is other than `zero` or `one`. The function uses
`traits::eq()` to compare the character values.

Otherwise, the function constructs an object of class `bitset<N>`,
initializing the first `M` bit positions to values determined from the
corresponding characters in the string `str`. `M` is the smaller of `N`
and `rlen`.

An element of the constructed object has value zero if the corresponding
character in `str`, beginning at position `pos`, is `zero`. Otherwise,
the element has the value one. Character position `pos + M - 1`
corresponds to bit position zero. Subsequent decreasing character
positions correspond to increasing bit positions.

If `M < N`, remaining bit positions are initialized to zero.

``` cpp
template <class charT>
  explicit bitset(
    const charT* str,
    typename basic_string<charT>::size_type n = basic_string<charT>::npos,
    charT zero = charT('0'), charT one = charT('1'));
```

*Effects:* Constructs an object of class `bitset<N>` as if by:

``` cpp
bitset(
  n == basic_string<charT>::npos
    ? basic_string<charT>(str)
    : basic_string<charT>(str, n),
  0, n, zero, one)
```

#### `bitset` members <a id="bitset.members">[[bitset.members]]</a>

``` cpp
bitset<N>& operator&=(const bitset<N>& rhs) noexcept;
```

*Effects:* Clears each bit in `*this` for which the corresponding bit in
`rhs` is clear, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
bitset<N>& operator|=(const bitset<N>& rhs) noexcept;
```

*Effects:* Sets each bit in `*this` for which the corresponding bit in
`rhs` is set, and leaves all other bits unchanged.

*Returns:* `*this`.

\indexlibrarymember{operator^=}{bitset}

``` cpp
bitset<N>& operator^=(const bitset<N>& rhs) noexcept;
```

*Effects:* Toggles each bit in `*this` for which the corresponding bit
in `rhs` is set, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
bitset<N>& operator<<=(size_t pos) noexcept;
```

*Effects:* Replaces each bit at position `I` in `*this` with a value
determined as follows:

- If `I < pos`, the new value is zero;
- If `I >= pos`, the new value is the previous value of the bit at
  position `I - pos`.

*Returns:* `*this`.

``` cpp
bitset<N>& operator>>=(size_t pos) noexcept;
```

*Effects:* Replaces each bit at position `I` in `*this` with a value
determined as follows:

- If `pos >= N - I`, the new value is zero;
- If `pos < N - I`, the new value is the previous value of the bit at
  position `I + pos`.

*Returns:* `*this`.

``` cpp
bitset<N>& set() noexcept;
```

*Effects:* Sets all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& set(size_t pos, bool val = true);
```

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Effects:* Stores a new value in the bit at position `pos` in `*this`.
If `val` is nonzero, the stored value is one, otherwise it is zero.

*Returns:* `*this`.

``` cpp
bitset<N>& reset() noexcept;
```

*Effects:* Resets all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& reset(size_t pos);
```

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Effects:* Resets the bit at position `pos` in `*this`.

*Returns:* `*this`.

\indexlibrarymember{operator~}{bitset}

``` cpp
bitset<N> operator~() const noexcept;
```

*Effects:* Constructs an object `x` of class `bitset<N>` and initializes
it with `*this`.

*Returns:* `x.flip()`.

``` cpp
bitset<N>& flip() noexcept;
```

*Effects:* Toggles all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& flip(size_t pos);
```

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Effects:* Toggles the bit at position `pos` in `*this`.

*Returns:* `*this`.

``` cpp
unsigned long to_ulong() const;
```

*Throws:* `overflow_error`

if the integral value `x` corresponding to the bits in `*this` cannot be
represented as type `unsigned long`.

*Returns:* `x`.

``` cpp
unsigned long long to_ullong() const;
```

*Throws:* `overflow_error` if the integral value `x` corresponding to
the bits in `*this` cannot be represented as type `unsigned long long`.

*Returns:* `x`.

``` cpp
template <class charT = char,
    class traits = char_traits<charT>,
    class Allocator = allocator<charT>>
  basic_string<charT, traits, Allocator>
  to_string(charT zero = charT('0'), charT one = charT('1')) const;
```

*Effects:* Constructs a string object of the appropriate type and
initializes it to a string of length `N` characters. Each character is
determined by the value of its corresponding bit position in `*this`.
Character position `N - 1` corresponds to bit position zero. Subsequent
decreasing character positions correspond to increasing bit positions.
Bit value zero becomes the character `zero`, bit value one becomes the
character `one`.

*Returns:* The created object.

``` cpp
size_t count() const noexcept;
```

*Returns:* A count of the number of bits set in `*this`.

``` cpp
constexpr size_t size() const noexcept;
```

*Returns:* `N`.

``` cpp
bool operator==(const bitset<N>& rhs) const noexcept;
```

*Returns:* `true` if the value of each bit in `*this` equals the value
of the corresponding bit in `rhs`.

``` cpp
bool operator!=(const bitset<N>& rhs) const noexcept;
```

*Returns:* `true` if `!(*this == rhs)`.

``` cpp
bool test(size_t pos) const;
```

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one.

``` cpp
bool all() const noexcept;
```

*Returns:* `count() == size()`.

``` cpp
bool any() const noexcept;
```

*Returns:* `count() != 0`.

``` cpp
bool none() const noexcept;
```

*Returns:* `count() == 0`.

``` cpp
bitset<N> operator<<(size_t pos) const noexcept;
```

*Returns:* `bitset<N>(*this) <<= pos`.

``` cpp
bitset<N> operator>>(size_t pos) const noexcept;
```

*Returns:* `bitset<N>(*this) >>= pos`.

``` cpp
constexpr bool operator[](size_t pos) const;
```

*Requires:* `pos` shall be valid.

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one, otherwise `false`.

*Throws:* Nothing.

``` cpp
bitset<N>::reference operator[](size_t pos);
```

*Requires:* `pos` shall be valid.

*Returns:* An object of type `bitset<N>::reference` such that
`(*this)[pos] == this->test(pos)`, and such that `(*this)[pos] = val` is
equivalent to `this->set(pos, val)`.

*Throws:* Nothing.

*Remarks:* For the purpose of determining the presence of a data
race ([[intro.multithread]]), any access or update through the
resulting reference potentially accesses or modifies, respectively, the
entire underlying bitset.

### `bitset` hash support <a id="bitset.hash">[[bitset.hash]]</a>

``` cpp
template <size_t N> struct hash<bitset<N>>;
```

The specialization is enabled ([[unord.hash]]).

### `bitset` operators <a id="bitset.operators">[[bitset.operators]]</a>

``` cpp
bitset<N> operator&(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) &= rhs`.

``` cpp
bitset<N> operator|(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) |= rhs`.

\indexlibrarymember{operator^}{bitset}

``` cpp
bitset<N> operator^(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) ^= rhs`.

``` cpp
template <class charT, class traits, size_t N>
  basic_istream<charT, traits>&
  operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
```

A formatted input function ([[istream.formatted]]).

*Effects:* Extracts up to `N` characters from `is`. Stores these
characters in a temporary object `str` of type
`basic_string<charT, traits>`, then evaluates the expression
`x = bitset<N>(str)`. Characters are extracted and stored until any of
the following occurs:

- `N` characters have been extracted and stored;
- end-of-file occurs on the input sequence;
- the next input character is neither `is.widen(’0’)` nor
  `is.widen(’1’)` (in which case the input character is not extracted).

If no characters are stored in `str`, calls
`is.setstate(ios_base::failbit)` (which may throw
`ios_base::failure` ([[iostate.flags]])).

*Returns:* `is`.

``` cpp
template <class charT, class traits, size_t N>
  basic_ostream<charT, traits>&
  operator<<(basic_ostream<charT, traits>& os, const bitset<N>& x);
```

*Returns:*

``` cpp
os << x.template to_string<charT, traits, allocator<charT>>(
  use_facet<ctype<charT>>(os.getloc()).widen('0'),
  use_facet<ctype<charT>>(os.getloc()).widen('1'))
```

(see  [[ostream.formatted]]).

## Memory <a id="memory">[[memory]]</a>

### In general <a id="memory.general">[[memory.general]]</a>

This subclause describes the contents of the header `<memory>` (
[[memory.syn]]) and some of the contents of the header `<cstdlib>` (
[[cstdlib.syn]]).

### Header `<memory>` synopsis <a id="memory.syn">[[memory.syn]]</a>

The header `<memory>` defines several types and function templates that
describe properties of pointers and pointer-like types, manage memory
for containers and other template types, destroy objects, and construct
multiple objects in uninitialized memory buffers ([[pointer.traits]]–
[[specialized.algorithms]]). The header also defines the templates
`unique_ptr`, `shared_ptr`, `weak_ptr`, and various function templates
that operate on objects of these types ([[smartptr]]).

``` cpp
namespace std {
  // [pointer.traits], pointer traits
  template <class Ptr> struct pointer_traits;
  template <class T> struct pointer_traits<T*>;

  // [util.dynamic.safety], pointer safety
  enum class pointer_safety { relaxed, preferred, strict };
  void declare_reachable(void* p);
  template <class T> T* undeclare_reachable(T* p);
  void declare_no_pointers(char* p, size_t n);
  void undeclare_no_pointers(char* p, size_t n);
  pointer_safety get_pointer_safety() noexcept;

  // [ptr.align], pointer alignment function
  void* align(size_t alignment, size_t size, void*& ptr, size_t& space);

  // [allocator.tag], allocator argument tag
  struct allocator_arg_t { explicit allocator_arg_t() = default; };
  inline constexpr allocator_arg_t allocator_arg{};

  // [allocator.uses], uses_allocator
  template <class T, class Alloc> struct uses_allocator;

  // [allocator.traits], allocator traits
  template <class Alloc> struct allocator_traits;

  // [default.allocator], the default allocator
  template <class T> class allocator;
  template <class T, class U>
    bool operator==(const allocator<T>&, const allocator<U>&) noexcept;
  template <class T, class U>
    bool operator!=(const allocator<T>&, const allocator<U>&) noexcept;

  // [specialized.algorithms], specialized algorithms
  template <class T> constexpr T* addressof(T& r) noexcept;
  template <class T> const T* addressof(const T&&) = delete;
  template <class ForwardIterator>
    void uninitialized_default_construct(ForwardIterator first, ForwardIterator last);
  template <class ExecutionPolicy, class ForwardIterator>
    void uninitialized_default_construct(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                         ForwardIterator first, ForwardIterator last);
  template <class ForwardIterator, class Size>
    ForwardIterator uninitialized_default_construct_n(ForwardIterator first, Size n);
  template <class ExecutionPolicy, class ForwardIterator, class Size>
    ForwardIterator uninitialized_default_construct_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                                      ForwardIterator first, Size n);
  template <class ForwardIterator>
    void uninitialized_value_construct(ForwardIterator first, ForwardIterator last);
  template <class ExecutionPolicy, class ForwardIterator>
    void uninitialized_value_construct(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                       ForwardIterator first, ForwardIterator last);
  template <class ForwardIterator, class Size>
    ForwardIterator uninitialized_value_construct_n(ForwardIterator first, Size n);
  template <class ExecutionPolicy, class ForwardIterator, class Size>
    ForwardIterator uninitialized_value_construct_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                                    ForwardIterator first, Size n);
  template <class InputIterator, class ForwardIterator>
    ForwardIterator uninitialized_copy(InputIterator first, InputIterator last,
                                       ForwardIterator result);
  template <class ExecutionPolicy, class InputIterator, class ForwardIterator>
    ForwardIterator uninitialized_copy(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                       InputIterator first, InputIterator last,
                                       ForwardIterator result);
  template <class InputIterator, class Size, class ForwardIterator>
    ForwardIterator uninitialized_copy_n(InputIterator first, Size n,
                                         ForwardIterator result);
  template <class ExecutionPolicy, class InputIterator, class Size, class ForwardIterator>
    ForwardIterator uninitialized_copy_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                         InputIterator first, Size n,
                                         ForwardIterator result);
  template <class InputIterator, class ForwardIterator>
    ForwardIterator uninitialized_move(InputIterator first, InputIterator last,
                                       ForwardIterator result);
  template <class ExecutionPolicy, class InputIterator, class ForwardIterator>
    ForwardIterator uninitialized_move(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                       InputIterator first, InputIterator last,
                                       ForwardIterator result);
  template <class InputIterator, class Size, class ForwardIterator>
    pair<InputIterator, ForwardIterator>
      uninitialized_move_n(InputIterator first, Size n, ForwardIterator result);
  template <class ExecutionPolicy, class InputIterator, class Size, class ForwardIterator>
    pair<InputIterator, ForwardIterator>
      uninitialized_move_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                           InputIterator first, Size n, ForwardIterator result);
  template <class ForwardIterator, class T>
    void uninitialized_fill(ForwardIterator first, ForwardIterator last,
                            const T& x);
  template <class ExecutionPolicy, class ForwardIterator, class T>
    void uninitialized_fill(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                            ForwardIterator first, ForwardIterator last,
                            const T& x);
  template <class ForwardIterator, class Size, class T>
    ForwardIterator uninitialized_fill_n(ForwardIterator first, Size n, const T& x);
  template <class ExecutionPolicy, class ForwardIterator, class Size, class T>
    ForwardIterator uninitialized_fill_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                         ForwardIterator first, Size n, const T& x);
  template <class T>
    void destroy_at(T* location);
  template <class ForwardIterator>
    void destroy(ForwardIterator first, ForwardIterator last);
  template <class ExecutionPolicy, class ForwardIterator>
    void destroy(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                 ForwardIterator first, ForwardIterator last);
  template <class ForwardIterator, class Size>
    ForwardIterator destroy_n(ForwardIterator first, Size n);
  template <class ExecutionPolicy, class ForwardIterator, class Size>
    ForwardIterator destroy_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                              ForwardIterator first, Size n);

  // [unique.ptr], class template unique_ptr
  template <class T> struct default_delete;
  template <class T> struct default_delete<T[]>;
  template <class T, class D = default_delete<T>> class unique_ptr;
  template <class T, class D> class unique_ptr<T[], D>;

  template <class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
  template <class T> unique_ptr<T> make_unique(size_t n);
  template <class T, class... Args> unspecified make_unique(Args&&...) = delete;

  template <class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;

  template <class T1, class D1, class T2, class D2>
    bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator!=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template <class T1, class D1, class T2, class D2>
    bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);

  template <class T, class D>
    bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator==(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator!=(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator!=(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator<(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<=(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>=(nullptr_t, const unique_ptr<T, D>& y);

  // [util.smartptr.weak.bad], class bad_weak_ptr
  class bad_weak_ptr;

  // [util.smartptr.shared], class template shared_ptr
  template<class T> class shared_ptr;

  // [util.smartptr.shared.create], shared_ptr creation
  template<class T, class... Args>
    shared_ptr<T> make_shared(Args&&... args);
  template<class T, class A, class... Args>
    shared_ptr<T> allocate_shared(const A& a, Args&&... args);

  // [util.smartptr.shared.cmp], shared_ptr comparisons
  template<class T, class U>
    bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator!=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator<(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator<=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator>=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;

  template <class T>
    bool operator==(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator==(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator!=(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator!=(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator<(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator<(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator<=(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator<=(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator>(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator>(nullptr_t, const shared_ptr<T>& y) noexcept;
  template <class T>
    bool operator>=(const shared_ptr<T>& x, nullptr_t) noexcept;
  template <class T>
    bool operator>=(nullptr_t, const shared_ptr<T>& y) noexcept;

  // [util.smartptr.shared.spec], shared_ptr specialized algorithms
  template<class T>
    void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.cast], shared_ptr casts
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;

  // [util.smartptr.getdeleter], shared_ptr get_deleter
  template<class D, class T>
    D* get_deleter(const shared_ptr<T>& p) noexcept;

  // [util.smartptr.shared.io], shared_ptr I/O
  template<class E, class T, class Y>
    basic_ostream<E, T>& operator<< (basic_ostream<E, T>& os, const shared_ptr<Y>& p);

  // [util.smartptr.weak], class template weak_ptr
  template<class T> class weak_ptr;

  // [util.smartptr.weak.spec], weak_ptr specialized algorithms
  template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;

  // [util.smartptr.ownerless], class template owner_less
  template<class T = void> struct owner_less;

  // [util.smartptr.enab], class template enable_shared_from_this
  template<class T> class enable_shared_from_this;

  // [util.smartptr.shared.atomic], shared_ptr atomic access
  template<class T>
    bool atomic_is_lock_free(const shared_ptr<T>* p);

  template<class T>
    shared_ptr<T> atomic_load(const shared_ptr<T>* p);
  template<class T>
    shared_ptr<T> atomic_load_explicit(const shared_ptr<T>* p, memory_order mo);

  template<class T>
    void atomic_store(shared_ptr<T>* p, shared_ptr<T> r);
  template<class T>
    void atomic_store_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);

  template<class T>
    shared_ptr<T> atomic_exchange(shared_ptr<T>* p, shared_ptr<T> r);
  template<class T>
    shared_ptr<T> atomic_exchange_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);

  template<class T>
    bool atomic_compare_exchange_weak(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
  template<class T>
    bool atomic_compare_exchange_strong(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
  template<class T>
    bool atomic_compare_exchange_weak_explicit(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
      memory_order success, memory_order failure);
  template<class T>
    bool atomic_compare_exchange_strong_explicit(
      shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
      memory_order success, memory_order failure);

  // [util.smartptr.hash], hash support
  template <class T> struct hash;
  template <class T, class D> struct hash<unique_ptr<T, D>>;
  template <class T> struct hash<shared_ptr<T>>;

  // [allocator.uses.trait], uses_allocator
  template <class T, class Alloc>
    inline constexpr bool uses_allocator_v = uses_allocator<T, Alloc>::value;
}
```

### Pointer traits <a id="pointer.traits">[[pointer.traits]]</a>

The class template `pointer_traits` supplies a uniform interface to
certain attributes of pointer-like types.

``` cpp
namespace std {
  template <class Ptr> struct pointer_traits {
    using pointer         = Ptr;
    using element_type    = see below;
    using difference_type = see below;

    template <class U> using rebind = see below;

    static pointer pointer_to(see below r);
  };

  template <class T> struct pointer_traits<T*> {
    using pointer         = T*;
    using element_type    = T;
    using difference_type = ptrdiff_t;

    template <class U> using rebind = U*;

    static pointer pointer_to(see below r) noexcept;
  };
}
```

#### Pointer traits member types <a id="pointer.traits.types">[[pointer.traits.types]]</a>

``` cpp
using element_type = see below;
```

*Type:* `Ptr::element_type` if the *qualified-id* `Ptr::element_type` is
valid and denotes a type ([[temp.deduct]]); otherwise, `T` if `Ptr` is
a class template instantiation of the form `SomePointer<T, Args>`, where
`Args` is zero or more type arguments; otherwise, the specialization is
ill-formed.

``` cpp
using difference_type = see below;
```

*Type:* `Ptr::difference_type` if the *qualified-id*
`Ptr::difference_type` is valid and denotes a type ([[temp.deduct]]);
otherwise, `ptrdiff_t`.

``` cpp
template <class U> using rebind = see below;
```

*Alias template:* `Ptr::rebind<U>` if the *qualified-id*
`Ptr::rebind<U>` is valid and denotes a type ([[temp.deduct]]);
otherwise, `SomePointer<U, Args>` if `Ptr` is a class template
instantiation of the form `SomePointer<T, Args>`, where `Args` is zero
or more type arguments; otherwise, the instantiation of `rebind` is
ill-formed.

#### Pointer traits member functions <a id="pointer.traits.functions">[[pointer.traits.functions]]</a>

``` cpp
static pointer pointer_traits::pointer_to(see below r);
static pointer pointer_traits<T*>::pointer_to(see below r) noexcept;
```

*Remarks:* If `element_type` is cv `void`, the type of `r` is
unspecified; otherwise, it is `element_type&`.

*Returns:* The first member function returns a pointer to `r` obtained
by calling `Ptr::pointer_to(r)` through which indirection is valid; an
instantiation of this function is ill-formed if `Ptr` does not have a
matching `pointer_to` static member function. The second member function
returns `addressof(r)`.

### Pointer safety <a id="util.dynamic.safety">[[util.dynamic.safety]]</a>

A complete object is while the number of calls to `declare_reachable`
with an argument referencing the object exceeds the number of calls to
`undeclare_reachable` with an argument referencing the object.

``` cpp
void declare_reachable(void* p);
```

*Requires:* `p` shall be a safely-derived
pointer ([[basic.stc.dynamic.safety]]) or a null pointer value.

*Effects:* If `p` is not null, the complete object referenced by `p` is
subsequently declared reachable ([[basic.stc.dynamic.safety]]).

*Throws:* May throw `bad_alloc` if the system cannot allocate additional
memory that may be required to track objects declared reachable.

``` cpp
template <class T> T* undeclare_reachable(T* p);
```

*Requires:* If `p` is not null, the complete object referenced by `p`
shall have been previously declared reachable, and shall be
live ([[basic.life]]) from the time of the call until the last
`undeclare_reachable(p)` call on the object.

*Returns:* A safely derived copy of `p` which shall compare equal to
`p`.

*Throws:* Nothing.

[*Note 1*: It is expected that calls to `declare_reachable(p)` will
consume a small amount of memory in addition to that occupied by the
referenced object until the matching call to `undeclare_reachable(p)` is
encountered. Long running programs should arrange that calls are
matched. — *end note*]

``` cpp
void declare_no_pointers(char* p, size_t n);
```

*Requires:* No bytes in the specified range are currently registered
with `declare_no_pointers()`. If the specified range is in an allocated
object, then it must be entirely within a single allocated object. The
object must be live until the corresponding `undeclare_no_pointers()`
call.

[*Note 2*: In a garbage-collecting implementation, the fact that a
region in an object is registered with `declare_no_pointers()` should
not prevent the object from being collected. — *end note*]

*Effects:* The `n` bytes starting at `p` no longer contain traceable
pointer locations, independent of their type. Hence indirection through
a pointer located there is undefined if the object it points to was
created by global `operator new` and not previously declared reachable.

[*Note 3*: This may be used to inform a garbage collector or leak
detector that this region of memory need not be traced. — *end note*]

*Throws:* Nothing.

[*Note 4*: Under some conditions implementations may need to allocate
memory. However, the request can be ignored if memory allocation
fails. — *end note*]

``` cpp
void undeclare_no_pointers(char* p, size_t n);
```

*Requires:* The same range must previously have been passed to
`declare_no_pointers()`.

*Effects:* Unregisters a range registered with `declare_no_pointers()`
for destruction. It must be called before the lifetime of the object
ends.

*Throws:* Nothing.

``` cpp
pointer_safety get_pointer_safety() noexcept;
```

*Returns:* `pointer_safety::strict` if the implementation has strict
pointer safety ([[basic.stc.dynamic.safety]]). It is
*implementation-defined* whether `get_pointer_safety` returns
`pointer_safety::relaxed` or `pointer_safety::preferred` if the
implementation has relaxed pointer safety.[^1]

### Align <a id="ptr.align">[[ptr.align]]</a>

``` cpp
void* align(size_t alignment, size_t size, void*& ptr, size_t& space);
```

*Effects:* If it is possible to fit `size` bytes of storage aligned by
`alignment` into the buffer pointed to by `ptr` with length `space`, the
function updates `ptr` to represent the first possible address of such
storage and decreases `space` by the number of bytes used for alignment.
Otherwise, the function does nothing.

*Requires:*

- `alignment` shall be a power of two
- `ptr` shall represent the address of contiguous storage of at least
  `space` bytes

*Returns:* A null pointer if the requested aligned buffer would not fit
into the available space, otherwise the adjusted value of `ptr`.

[*Note 1*: The function updates its `ptr` and `space` arguments so that
it can be called repeatedly with possibly different `alignment` and
`size` arguments for the same buffer. — *end note*]

### Allocator argument tag <a id="allocator.tag">[[allocator.tag]]</a>

``` cpp
namespace std {
  struct allocator_arg_t { explicit allocator_arg_t() = default; };
  inline constexpr allocator_arg_t allocator_arg{};
}
```

The `allocator_arg_t` struct is an empty structure type used as a unique
type to disambiguate constructor and function overloading. Specifically,
several types (see `tuple`  [[tuple]]) have constructors with
`allocator_arg_t` as the first argument, immediately followed by an
argument of a type that satisfies the `Allocator` requirements (
[[allocator.requirements]]).

### `uses_allocator` <a id="allocator.uses">[[allocator.uses]]</a>

#### `uses_allocator` trait <a id="allocator.uses.trait">[[allocator.uses.trait]]</a>

``` cpp
template <class T, class Alloc> struct uses_allocator;
```

*Remarks:* Automatically detects whether `T` has a nested
`allocator_type` that is convertible from `Alloc`. Meets the
`BinaryTypeTrait` requirements ([[meta.rqmts]]). The implementation
shall provide a definition that is derived from `true_type` if the
*qualified-id* `T::allocator_type` is valid and denotes a
type ([[temp.deduct]]) and
`is_convertible_v<Alloc, T::allocator_type> != false`, otherwise it
shall be derived from `false_type`. A program may specialize this
template to derive from `true_type` for a user-defined type `T` that
does not have a nested `allocator_type` but nonetheless can be
constructed with an allocator where either:

- the first argument of a constructor has type `allocator_arg_t` and the
  second argument has type `Alloc` or
- the last argument of a constructor has type `Alloc`.

#### Uses-allocator construction <a id="allocator.uses.construction">[[allocator.uses.construction]]</a>

*Uses-allocator construction* with allocator `Alloc` refers to the
construction of an object `obj` of type `T`, using constructor arguments
`v1, v2, ..., vN` of types `V1, V2, ..., VN`, respectively, and an
allocator `alloc` of type `Alloc`, according to the following rules:

- if `uses_allocator_v<T, Alloc>` is `false` and
  `is_constructible_v<T, V1, V2, ..., VN>` is `true`, then `obj` is
  initialized as `obj(v1, v2, ..., vN)`;
- otherwise, if `uses_allocator_v<T, Alloc>` is `true` and
  `is_constructible_v<T, allocator_arg_t, Alloc,` `V1, V2, ..., VN>` is
  `true`, then `obj` is initialized as `obj(allocator_arg, alloc, v1,
  v2, ..., vN)`;
- otherwise, if `uses_allocator_v<T, Alloc>` is `true` and
  `is_constructible_v<T, V1, V2, ..., VN, Alloc>` is `true`, then `obj`
  is initialized as `obj(v1, v2, ..., vN, alloc)`;
- otherwise, the request for uses-allocator construction is ill-formed.
  \[*Note 1*: An error will result if `uses_allocator_v<T, Alloc>` is
  `true` but the specific constructor does not take an allocator. This
  definition prevents a silent failure to pass the allocator to an
  element. — *end note*]

### Allocator traits <a id="allocator.traits">[[allocator.traits]]</a>

The class template `allocator_traits` supplies a uniform interface to
all allocator types. An allocator cannot be a non-class type, however,
even if `allocator_traits` supplies the entire required interface.

[*Note 1*: Thus, it is always possible to create a derived class from
an allocator. — *end note*]

``` cpp
namespace std {
  template <class Alloc> struct allocator_traits {
    using allocator_type     = Alloc;

    using value_type         = typename Alloc::value_type;

    using pointer            = see below;
    using const_pointer      = see below;
    using void_pointer       = see below;
    using const_void_pointer = see below;

    using difference_type    = see below;
    using size_type          = see below;

    using propagate_on_container_copy_assignment = see below;
    using propagate_on_container_move_assignment = see below;
    using propagate_on_container_swap            = see below;
    using is_always_equal                        = see below;

    template <class T> using rebind_alloc = see below;
    template <class T> using rebind_traits = allocator_traits<rebind_alloc<T>>;

    static pointer allocate(Alloc& a, size_type n);
    static pointer allocate(Alloc& a, size_type n, const_void_pointer hint);

    static void deallocate(Alloc& a, pointer p, size_type n);

    template <class T, class... Args>
      static void construct(Alloc& a, T* p, Args&&... args);

    template <class T>
      static void destroy(Alloc& a, T* p);

    static size_type max_size(const Alloc& a) noexcept;

    static Alloc select_on_container_copy_construction(const Alloc& rhs);
  };
}
```

#### Allocator traits member types <a id="allocator.traits.types">[[allocator.traits.types]]</a>

``` cpp
using pointer = see below;
```

*Type:* `Alloc::pointer` if the *qualified-id* `Alloc::pointer` is valid
and denotes a type ([[temp.deduct]]); otherwise, `value_type*`.

``` cpp
using const_pointer = see below;
```

*Type:* `Alloc::const_pointer` if the *qualified-id*
`Alloc::const_pointer` is valid and denotes a type ([[temp.deduct]]);
otherwise, `pointer_traits<pointer>::rebind<const value_type>`.

``` cpp
using void_pointer = see below;
```

*Type:* `Alloc::void_pointer` if the *qualified-id*
`Alloc::void_pointer` is valid and denotes a type ([[temp.deduct]]);
otherwise, `pointer_traits<pointer>::rebind<void>`.

``` cpp
using const_void_pointer = see below;
```

*Type:* `Alloc::const_void_pointer` if the *qualified-id*
`Alloc::const_void_pointer` is valid and denotes a
type ([[temp.deduct]]); otherwise,
`pointer_traits<pointer>::rebind<const void>`.

``` cpp
using difference_type = see below;
```

*Type:* `Alloc::difference_type` if the *qualified-id*
`Alloc::difference_type` is valid and denotes a type ([[temp.deduct]]);
otherwise, `pointer_traits<pointer>::difference_type`.

``` cpp
using size_type = see below;
```

*Type:* `Alloc::size_type` if the *qualified-id* `Alloc::size_type` is
valid and denotes a type ([[temp.deduct]]); otherwise,
`make_unsigned_t<difference_type>`.

``` cpp
using propagate_on_container_copy_assignment = see below;
```

*Type:* `Alloc::propagate_on_container_copy_assignment` if the
*qualified-id* `Alloc::propagate_on_container_copy_assignment` is valid
and denotes a type ([[temp.deduct]]); otherwise `false_type`.

``` cpp
using propagate_on_container_move_assignment = see below;
```

*Type:* `Alloc::propagate_on_container_move_assignment` if the
*qualified-id* `Alloc::propagate_on_container_move_assignment` is valid
and denotes a type ([[temp.deduct]]); otherwise `false_type`.

``` cpp
using propagate_on_container_swap = see below;
```

*Type:* `Alloc::propagate_on_container_swap` if the *qualified-id*
`Alloc::propagate_on_container_swap` is valid and denotes a
type ([[temp.deduct]]); otherwise `false_type`.

``` cpp
using is_always_equal = see below;
```

*Type:* `Alloc::is_always_equal` if the *qualified-id*
`Alloc::is_always_equal` is valid and denotes a type ([[temp.deduct]]);
otherwise `is_empty<Alloc>::type`.

``` cpp
template <class T> using rebind_alloc = see below;
```

*Alias template:* `Alloc::rebind<T>::other` if the *qualified-id*
`Alloc::rebind<T>::other` is valid and denotes a
type ([[temp.deduct]]); otherwise, `Alloc<T, Args>` if `Alloc` is a
class template instantiation of the form `Alloc<U, Args>`, where `Args`
is zero or more type arguments; otherwise, the instantiation of
`rebind_alloc` is ill-formed.

#### Allocator traits static member functions <a id="allocator.traits.members">[[allocator.traits.members]]</a>

``` cpp
static pointer allocate(Alloc& a, size_type n);
```

*Returns:* `a.allocate(n)`.

``` cpp
static pointer allocate(Alloc& a, size_type n, const_void_pointer hint);
```

*Returns:* `a.allocate(n, hint)` if that expression is well-formed;
otherwise, `a.allocate(n)`.

``` cpp
static void deallocate(Alloc& a, pointer p, size_type n);
```

*Effects:* Calls `a.deallocate(p, n)`.

*Throws:* Nothing.

``` cpp
template <class T, class... Args>
  static void construct(Alloc& a, T* p, Args&&... args);
```

*Effects:* Calls `a.construct(p, std::forward<Args>(args)...)` if that
call is well-formed; otherwise, invokes
`::new (static_cast<void*>(p)) T(std::forward<Args>(args)...)`.

``` cpp
template <class T>
  static void destroy(Alloc& a, T* p);
```

*Effects:* Calls `a.destroy(p)` if that call is well-formed; otherwise,
invokes `p->~T()`.

``` cpp
static size_type max_size(const Alloc& a) noexcept;
```

*Returns:* `a.max_size()` if that expression is well-formed; otherwise,
`numeric_limits<size_type>::max()/sizeof(value_type)`.

``` cpp
static Alloc select_on_container_copy_construction(const Alloc& rhs);
```

*Returns:* `rhs.select_on_container_copy_construction()` if that
expression is well-formed; otherwise, `rhs`.

### The default allocator <a id="default.allocator">[[default.allocator]]</a>

All specializations of the default allocator satisfy the allocator
completeness requirements ([[allocator.requirements.completeness]]).

``` cpp
namespace std {
  template <class T> class allocator {
   public:
    using value_type      = T;
    using propagate_on_container_move_assignment = true_type;
    using is_always_equal = true_type;

    allocator() noexcept;
    allocator(const allocator&) noexcept;
    template <class U> allocator(const allocator<U>&) noexcept;
    ~allocator();

    T* allocate(size_t n);
    void deallocate(T* p, size_t n);
  };
}
```

#### `allocator` members <a id="allocator.members">[[allocator.members]]</a>

Except for the destructor, member functions of the default allocator
shall not introduce data races ([[intro.multithread]]) as a result of
concurrent calls to those member functions from different threads. Calls
to these functions that allocate or deallocate a particular unit of
storage shall occur in a single total order, and each such deallocation
call shall happen before the next allocation (if any) in this order.

``` cpp
T* allocate(size_t n);
```

*Returns:* A pointer to the initial element of an array of storage of
size `n` `* sizeof(T)`, aligned appropriately for objects of type `T`.

*Remarks:* the storage is obtained by calling
`::operator new` ([[new.delete]]), but it is unspecified when or how
often this function is called.

*Throws:* `bad_alloc` if the storage cannot be obtained.

``` cpp
void deallocate(T* p, size_t n);
```

*Requires:* `p` shall be a pointer value obtained from `allocate()`. `n`
shall equal the value passed as the first argument to the invocation of
allocate which returned `p`.

*Effects:* Deallocates the storage referenced by `p` .

*Remarks:* Uses `::operator delete` ([[new.delete]]), but it is
unspecified when this function is called.

#### `allocator` globals <a id="allocator.globals">[[allocator.globals]]</a>

``` cpp
template <class T, class U>
  bool operator==(const allocator<T>&, const allocator<U>&) noexcept;
```

*Returns:* `true`.

``` cpp
template <class T, class U>
  bool operator!=(const allocator<T>&, const allocator<U>&) noexcept;
```

*Returns:* `false`.

### Specialized algorithms <a id="specialized.algorithms">[[specialized.algorithms]]</a>

Throughout this subclause, the names of template parameters are used to
express type requirements.

- If an algorithm’s template parameter is named `InputIterator`, the
  template argument shall satisfy the requirements of an input
  iterator ([[input.iterators]]).
- If an algorithm’s template parameter is named `ForwardIterator`, the
  template argument shall satisfy the requirements of a forward
  iterator ([[forward.iterators]]), and is required to have the
  property that no exceptions are thrown from increment, assignment,
  comparison, or indirection through valid iterators.

Unless otherwise specified, if an exception is thrown in the following
algorithms there are no effects.

#### `addressof` <a id="specialized.addressof">[[specialized.addressof]]</a>

``` cpp
template <class T> constexpr T* addressof(T& r) noexcept;
```

*Returns:* The actual address of the object or function referenced by
`r`, even in the presence of an overloaded `operator&`.

*Remarks:* An expression `addressof(E)` is a constant
subexpression ([[defns.const.subexpr]]) if `E` is an lvalue constant
subexpression.

#### `uninitialized_default_construct` <a id="uninitialized.construct.default">[[uninitialized.construct.default]]</a>

``` cpp
template <class ForwardIterator>
  void uninitialized_default_construct(ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (static_cast<void*>(addressof(*first)))
    typename iterator_traits<ForwardIterator>::value_type;
```

``` cpp
template <class ForwardIterator, class Size>
  ForwardIterator uninitialized_default_construct_n(ForwardIterator first, Size n);
```

*Effects:* Equivalent to:

``` cpp
for (; n>0; (void)++first, --n)
  ::new (static_cast<void*>(addressof(*first)))
    typename iterator_traits<ForwardIterator>::value_type;
return first;
```

#### `uninitialized_value_construct` <a id="uninitialized.construct.value">[[uninitialized.construct.value]]</a>

``` cpp
template <class ForwardIterator>
  void uninitialized_value_construct(ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; ++first)
  ::new (static_cast<void*>(addressof(*first)))
    typename iterator_traits<ForwardIterator>::value_type();
```

``` cpp
template <class ForwardIterator, class Size>
  ForwardIterator uninitialized_value_construct_n(ForwardIterator first, Size n);
```

*Effects:* Equivalent to:

``` cpp
for (; n>0; (void)++first, --n)
  ::new (static_cast<void*>(addressof(*first)))
    typename iterator_traits<ForwardIterator>::value_type();
return first;
```

#### `uninitialized_copy` <a id="uninitialized.copy">[[uninitialized.copy]]</a>

``` cpp
template <class InputIterator, class ForwardIterator>
  ForwardIterator uninitialized_copy(InputIterator first, InputIterator last,
                                     ForwardIterator result);
```

*Effects:* As if by:

``` cpp
for (; first != last; ++result, (void) ++first)
  ::new (static_cast<void*>(addressof(*result)))
    typename iterator_traits<ForwardIterator>::value_type(*first);
```

*Returns:* `result`.

``` cpp
template <class InputIterator, class Size, class ForwardIterator>
  ForwardIterator uninitialized_copy_n(InputIterator first, Size n,
                                       ForwardIterator result);
```

*Effects:* As if by:

``` cpp
for ( ; n > 0; ++result, (void) ++first, --n) {
  ::new (static_cast<void*>(addressof(*result)))
    typename iterator_traits<ForwardIterator>::value_type(*first);
}
```

*Returns:* `result`.

#### `uninitialized_move` <a id="uninitialized.move">[[uninitialized.move]]</a>

``` cpp
template <class InputIterator, class ForwardIterator>
  ForwardIterator uninitialized_move(InputIterator first, InputIterator last,
                                     ForwardIterator result);
```

*Effects:* Equivalent to:

``` cpp
for (; first != last; (void)++result, ++first)
  ::new (static_cast<void*>(addressof(*result)))
    typename iterator_traits<ForwardIterator>::value_type(std::move(*first));
return result;
```

*Remarks:* If an exception is thrown, some objects in the range
\[`first`, `last`) are left in a valid but unspecified state.

``` cpp
template <class InputIterator, class Size, class ForwardIterator>
  pair<InputIterator, ForwardIterator>
    uninitialized_move_n(InputIterator first, Size n, ForwardIterator result);
```

*Effects:* Equivalent to:

``` cpp
for (; n > 0; ++result, (void) ++first, --n)
  ::new (static_cast<void*>(addressof(*result)))
    typename iterator_traits<ForwardIterator>::value_type(std::move(*first));
return {first,result};
```

*Remarks:* If an exception is thrown, some objects in the range
\[`first`, `std::next(first,n)`) are left in a valid but unspecified
state.

#### `uninitialized_fill` <a id="uninitialized.fill">[[uninitialized.fill]]</a>

``` cpp
template <class ForwardIterator, class T>
  void uninitialized_fill(ForwardIterator first, ForwardIterator last,
                          const T& x);
```

*Effects:* As if by:

``` cpp
for (; first != last; ++first)
  ::new (static_cast<void*>(addressof(*first)))
    typename iterator_traits<ForwardIterator>::value_type(x);
```

``` cpp
template <class ForwardIterator, class Size, class T>
  ForwardIterator uninitialized_fill_n(ForwardIterator first, Size n, const T& x);
```

*Effects:* As if by:

``` cpp
for (; n--; ++first)
  ::new (static_cast<void*>(addressof(*first)))
    typename iterator_traits<ForwardIterator>::value_type(x);
return first;
```

#### `destroy` <a id="specialized.destroy">[[specialized.destroy]]</a>

``` cpp
template <class T>
  void destroy_at(T* location);
```

*Effects:* Equivalent to:

``` cpp
location->~T();
```

``` cpp
template <class ForwardIterator>
  void destroy(ForwardIterator first, ForwardIterator last);
```

*Effects:* Equivalent to:

``` cpp
for (; first!=last; ++first)
  destroy_at(addressof(*first));
```

``` cpp
template <class ForwardIterator, class Size>
  ForwardIterator destroy_n(ForwardIterator first, Size n);
```

*Effects:* Equivalent to:

``` cpp
for (; n > 0; (void)++first, --n)
  destroy_at(addressof(*first));
return first;
```

### C library memory allocation <a id="c.malloc">[[c.malloc]]</a>

[*Note 1*: The header `<cstdlib>` ([[cstdlib.syn]]) declares the
functions described in this subclause. — *end note*]

``` cpp
void* aligned_alloc(size_t alignment, size_t size);
void* calloc(size_t nmemb, size_t size);
void* malloc(size_t size);
void* realloc(void* ptr, size_t size);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* These functions do not attempt to allocate storage by calling
`::operator new()` ([[support.dynamic]]).

Storage allocated directly with these functions is implicitly declared
reachable (see  [[basic.stc.dynamic.safety]]) on allocation, ceases to
be declared reachable on deallocation, and need not cease to be declared
reachable as the result of an `undeclare_reachable()` call.

[*Note 1*: This allows existing C libraries to remain unaffected by
restrictions on pointers that are not safely derived, at the expense of
providing far fewer garbage collection and leak detection options for
`malloc()`-allocated objects. It also allows `malloc()` to be
implemented with a separate allocation arena, bypassing the normal
`declare_reachable()` implementation. The above functions should never
intentionally be used as a replacement for `declare_reachable()`, and
newly written code is strongly encouraged to treat memory allocated with
these functions as though it were allocated with
`operator new`. — *end note*]

``` cpp
void free(void* ptr);
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* This function does not attempt to deallocate storage by
calling `::operator delete()`.

ISO C 7.22.3.

## Smart pointers <a id="smartptr">[[smartptr]]</a>

### Class template `unique_ptr` <a id="unique.ptr">[[unique.ptr]]</a>

A *unique pointer* is an object that owns another object and manages
that other object through a pointer. More precisely, a unique pointer is
an object *u* that stores a pointer to a second object *p* and will
dispose of *p* when *u* is itself destroyed (e.g., when leaving block
scope ([[stmt.dcl]])). In this context, *u* is said to *own* `p`.

The mechanism by which *u* disposes of *p* is known as *p*’s associated
*deleter*, a function object whose correct invocation results in *p*’s
appropriate disposition (typically its deletion).

Let the notation *u.p* denote the pointer stored by *u*, and let *u.d*
denote the associated deleter. Upon request, *u* can *reset* (replace)
*u.p* and *u.d* with another pointer and deleter, but must properly
dispose of its owned object via the associated deleter before such
replacement is considered completed.

Additionally, *u* can, upon request, *transfer ownership* to another
unique pointer *u2*. Upon completion of such a transfer, the following
postconditions hold:

- *u2.p* is equal to the pre-transfer *u.p*,
- *u.p* is equal to `nullptr`, and
- if the pre-transfer *u.d* maintained state, such state has been
  transferred to *u2.d*.

As in the case of a reset, *u2* must properly dispose of its
pre-transfer owned object via the pre-transfer associated deleter before
the ownership transfer is considered complete.

[*Note 1*: A deleter’s state need never be copied, only moved or
swapped as ownership is transferred. — *end note*]

Each object of a type `U` instantiated from the `unique_ptr` template
specified in this subclause has the strict ownership semantics,
specified above, of a unique pointer. In partial satisfaction of these
semantics, each such `U` is `MoveConstructible` and `MoveAssignable`,
but is not `CopyConstructible` nor `CopyAssignable`. The template
parameter `T` of `unique_ptr` may be an incomplete type.

[*Note 2*: The uses of `unique_ptr` include providing exception safety
for dynamically allocated memory, passing ownership of dynamically
allocated memory to a function, and returning dynamically allocated
memory from a function. — *end note*]

``` cpp
namespace std {
  template<class T> struct default_delete;
  template<class T> struct default_delete<T[]>;

  template<class T, class D = default_delete<T>> class unique_ptr;
  template<class T, class D> class unique_ptr<T[], D>;

  template<class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
  template<class T> unique_ptr<T> make_unique(size_t n);
  template<class T, class... Args> unspecified make_unique(Args&&...) = delete;

  template<class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;

  template<class T1, class D1, class T2, class D2>
    bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator!=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);

  template <class T, class D>
    bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator==(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator!=(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template <class T, class D>
    bool operator!=(nullptr_t, const unique_ptr<T, D>& y) noexcept;
  template <class T, class D>
    bool operator<(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator<=(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>(nullptr_t, const unique_ptr<T, D>& y);
  template <class T, class D>
    bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
  template <class T, class D>
    bool operator>=(nullptr_t, const unique_ptr<T, D>& y);

}
```

#### Default deleters <a id="unique.ptr.dltr">[[unique.ptr.dltr]]</a>

##### In general <a id="unique.ptr.dltr.general">[[unique.ptr.dltr.general]]</a>

The class template `default_delete` serves as the default deleter
(destruction policy) for the class template `unique_ptr`.

The template parameter `T` of `default_delete` may be an incomplete
type.

##### `default_delete` <a id="unique.ptr.dltr.dflt">[[unique.ptr.dltr.dflt]]</a>

``` cpp
namespace std {
  template <class T> struct default_delete {
    constexpr default_delete() noexcept = default;
    template <class U> default_delete(const default_delete<U>&) noexcept;
    void operator()(T*) const;
  };
}
```

``` cpp
template <class U> default_delete(const default_delete<U>& other) noexcept;
```

*Effects:* Constructs a `default_delete` object from another
`default_delete<U>` object.

*Remarks:* This constructor shall not participate in overload resolution
unless `U*` is implicitly convertible to `T*`.

``` cpp
void operator()(T* ptr) const;
```

*Effects:* Calls `delete` on `ptr`.

*Remarks:* If `T` is an incomplete type, the program is ill-formed.

##### `default_delete<T[]>` <a id="unique.ptr.dltr.dflt1">[[unique.ptr.dltr.dflt1]]</a>

``` cpp
namespace std {
  template <class T> struct default_delete<T[]> {
    constexpr default_delete() noexcept = default;
    template <class U> default_delete(const default_delete<U[]>&) noexcept;
    template <class U> void operator()(U* ptr) const;
  };
}
```

``` cpp
template <class U> default_delete(const default_delete<U[]>& other) noexcept;
```

*Effects:* constructs a `default_delete` object from another
`default_delete<U[]>` object.

*Remarks:* This constructor shall not participate in overload resolution
unless `U(*)[]` is convertible to `T(*)[]`.

``` cpp
template <class U> void operator()(U* ptr) const;
```

*Effects:* Calls `delete[]` on `ptr`.

*Remarks:* If `U` is an incomplete type, the program is ill-formed. This
function shall not participate in overload resolution unless `U(*)[]` is
convertible to `T(*)[]`.

#### `unique_ptr` for single objects <a id="unique.ptr.single">[[unique.ptr.single]]</a>

``` cpp
namespace std {
  template <class T, class D = default_delete<T>> class unique_ptr {
  public:
    using pointer      = see below;
    using element_type = T;
    using deleter_type = D;

    // [unique.ptr.single.ctor], constructors
    constexpr unique_ptr() noexcept;
    explicit unique_ptr(pointer p) noexcept;
    unique_ptr(pointer p, see below d1) noexcept;
    unique_ptr(pointer p, see below d2) noexcept;
    unique_ptr(unique_ptr&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept;
    template <class U, class E>
      unique_ptr(unique_ptr<U, E>&& u) noexcept;

    // [unique.ptr.single.dtor], destructor
    ~unique_ptr();

    // [unique.ptr.single.asgn], assignment
    unique_ptr& operator=(unique_ptr&& u) noexcept;
    template <class U, class E> unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
    unique_ptr& operator=(nullptr_t) noexcept;

    // [unique.ptr.single.observers], observers
    add_lvalue_reference_t<T> operator*() const;
    pointer operator->() const noexcept;
    pointer get() const noexcept;
    deleter_type& get_deleter() noexcept;
    const deleter_type& get_deleter() const noexcept;
    explicit operator bool() const noexcept;

    // [unique.ptr.single.modifiers], modifiers
    pointer release() noexcept;
    void reset(pointer p = pointer()) noexcept;
    void swap(unique_ptr& u) noexcept;

    // disable copy from lvalue
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
  };
}
```

The default type for the template parameter `D` is `default_delete`. A
client-supplied template argument `D` shall be a function object type (
[[function.objects]]), lvalue reference to function, or lvalue reference
to function object type for which, given a value `d` of type `D` and a
value `ptr` of type `unique_ptr<T, D>::pointer`, the expression `d(ptr)`
is valid and has the effect of disposing of the pointer as appropriate
for that deleter.

If the deleter’s type `D` is not a reference type, `D` shall satisfy the
requirements of `Destructible` (Table  [[tab:destructible]]).

If the *qualified-id* `remove_reference_t<D>::pointer` is valid and
denotes a type ([[temp.deduct]]), then `unique_ptr<T,
D>::pointer` shall be a synonym for `remove_reference_t<D>::pointer`.
Otherwise `unique_ptr<T, D>::pointer` shall be a synonym for
`element_type*`. The type `unique_ptr<T,
D>::pointer` shall satisfy the requirements of `NullablePointer` (
[[nullablepointer.requirements]]).

[*Example 1*: Given an allocator type `X` ([[allocator.requirements]])
and letting `A` be a synonym for `allocator_traits<X>`, the types
`A::pointer`, `A::const_pointer`, `A::void_pointer`, and
`A::const_void_pointer` may be used as
`unique_ptr<T, D>::pointer`. — *end example*]

##### `unique_ptr` constructors <a id="unique.ptr.single.ctor">[[unique.ptr.single.ctor]]</a>

``` cpp
constexpr unique_ptr() noexcept;
constexpr unique_ptr(nullptr_t) noexcept;
```

*Requires:* `D` shall satisfy the requirements of `DefaultConstructible`
(Table  [[tab:defaultconstructible]]), and that construction shall not
throw an exception.

*Effects:* Constructs a `unique_ptr` object that owns nothing,
value-initializing the stored pointer and the stored deleter.

*Postconditions:* `get() == nullptr`. `get_deleter()` returns a
reference to the stored deleter.

*Remarks:* If `is_pointer_v<deleter_type>` is `true` or
`is_default_constructible_v<deleter_type>` is `false`, this constructor
shall not participate in overload resolution.

``` cpp
explicit unique_ptr(pointer p) noexcept;
```

*Requires:* `D` shall satisfy the requirements of `DefaultConstructible`
(Table  [[tab:defaultconstructible]]), and that construction shall not
throw an exception.

*Effects:* Constructs a `unique_ptr` which owns `p`, initializing the
stored pointer with `p` and value-initializing the stored deleter.

*Postconditions:* `get() == p`. `get_deleter()` returns a reference to
the stored deleter.

*Remarks:* If `is_pointer_v<deleter_type>` is `true` or
`is_default_constructible_v<deleter_type>` is `false`, this constructor
shall not participate in overload resolution. If class template argument
deduction ([[over.match.class.deduct]]) would select the function
template corresponding to this constructor, then the program is
ill-formed.

``` cpp
unique_ptr(pointer p, see below d1) noexcept;
unique_ptr(pointer p, see below d2) noexcept;
```

The signature of these constructors depends upon whether `D` is a
reference type. If `D` is a non-reference type `A`, then the signatures
are:

``` cpp
unique_ptr(pointer p, const A& d) noexcept;
unique_ptr(pointer p, A&& d) noexcept;
```

If `D` is an lvalue reference type `A&`, then the signatures are:

``` cpp
unique_ptr(pointer p, A& d) noexcept;
unique_ptr(pointer p, A&& d) = delete;
```

If `D` is an lvalue reference type `const A&`, then the signatures are:

``` cpp
unique_ptr(pointer p, const A& d) noexcept;
unique_ptr(pointer p, const A&& d) = delete;
```

*Effects:* Constructs a `unique_ptr` object which owns `p`, initializing
the stored pointer with `p` and initializing the deleter from
`std::forward<decltype(d)>(d)`.

*Remarks:* These constructors shall not participate in overload
resolution unless `is_constructible_v<D, decltype(d)>` is `true`.

*Postconditions:* `get() == p`. `get_deleter()` returns a reference to
the stored deleter. If `D` is a reference type then `get_deleter()`
returns a reference to the lvalue `d`.

*Remarks:* If class template argument
deduction ([[over.match.class.deduct]]) would select a function
template corresponding to either of these constructors, then the program
is ill-formed.

[*Example 1*:

``` cpp
D d;
unique_ptr<int, D> p1(new int, D());        // D must be MoveConstructible
unique_ptr<int, D> p2(new int, d);          // D must be CopyConstructible
unique_ptr<int, D&> p3(new int, d);         // p3 holds a reference to d
unique_ptr<int, const D&> p4(new int, D()); // error: rvalue deleter object combined
                                            // with reference deleter type
```

— *end example*]

``` cpp
unique_ptr(unique_ptr&& u) noexcept;
```

*Requires:* If `D` is not a reference type, `D` shall satisfy the
requirements of `MoveConstructible` (Table  [[tab:moveconstructible]]).
Construction of the deleter from an rvalue of type `D` shall not throw
an exception.

*Effects:* Constructs a `unique_ptr` by transferring ownership from `u`
to `*this`. If `D` is a reference type, this deleter is copy constructed
from `u`’s deleter; otherwise, this deleter is move constructed from
`u`’s deleter.

[*Note 1*: The deleter constructor can be implemented with
`std::forward<D>`. — *end note*]

*Postconditions:* `get()` yields the value `u.get()` yielded before the
construction. `get_deleter()` returns a reference to the stored deleter
that was constructed from `u.get_deleter()`. If `D` is a reference type
then `get_deleter()` and `u.get_deleter()` both reference the same
lvalue deleter.

``` cpp
template <class U, class E> unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

*Requires:* If `E` is not a reference type, construction of the deleter
from an rvalue of type `E` shall be well formed and shall not throw an
exception. Otherwise, `E` is a reference type and construction of the
deleter from an lvalue of type `E` shall be well formed and shall not
throw an exception.

*Remarks:* This constructor shall not participate in overload resolution
unless:

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
- `U` is not an array type, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

*Effects:* Constructs a `unique_ptr` by transferring ownership from `u`
to `*this`. If `E` is a reference type, this deleter is copy constructed
from `u`’s deleter; otherwise, this deleter is move constructed from
`u`’s deleter.

[*Note 2*: The deleter constructor can be implemented with
`std::forward<E>`. — *end note*]

*Postconditions:* `get()` yields the value `u.get()` yielded before the
construction. `get_deleter()` returns a reference to the stored deleter
that was constructed from `u.get_deleter()`.

##### `unique_ptr` destructor <a id="unique.ptr.single.dtor">[[unique.ptr.single.dtor]]</a>

``` cpp
~unique_ptr();
```

*Requires:* The expression `get_deleter()(get())` shall be well formed,
shall have well-defined behavior, and shall not throw exceptions.

[*Note 3*: The use of `default_delete` requires `T` to be a complete
type. — *end note*]

*Effects:* If `get() == nullptr` there are no effects. Otherwise
`get_deleter()(get())`.

##### `unique_ptr` assignment <a id="unique.ptr.single.asgn">[[unique.ptr.single.asgn]]</a>

``` cpp
unique_ptr& operator=(unique_ptr&& u) noexcept;
```

*Requires:* If `D` is not a reference type, `D` shall satisfy the
requirements of `MoveAssignable` (Table  [[tab:moveassignable]]) and
assignment of the deleter from an rvalue of type `D` shall not throw an
exception. Otherwise, `D` is a reference type; `remove_reference_t<D>`
shall satisfy the `CopyAssignable` requirements and assignment of the
deleter from an lvalue of type `D` shall not throw an exception.

*Effects:* Transfers ownership from `u` to `*this` as if by calling
`reset(u.release())` followed by
`get_deleter() = std::forward<D>(u.get_deleter())`.

*Returns:* `*this`.

``` cpp
template <class U, class E> unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
```

*Requires:* If `E` is not a reference type, assignment of the deleter
from an rvalue of type `E` shall be well-formed and shall not throw an
exception. Otherwise, `E` is a reference type and assignment of the
deleter from an lvalue of type `E` shall be well-formed and shall not
throw an exception.

*Remarks:* This operator shall not participate in overload resolution
unless:

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
  and
- `U` is not an array type, and
- `is_assignable_v<D&, E&&>` is `true`.

*Effects:* Transfers ownership from `u` to `*this` as if by calling
`reset(u.release())` followed by
`get_deleter() = std::forward<E>(u.get_deleter())`.

*Returns:* `*this`.

``` cpp
unique_ptr& operator=(nullptr_t) noexcept;
```

*Effects:* As if by `reset()`.

*Postconditions:* `get() == nullptr`.

*Returns:* `*this`.

##### `unique_ptr` observers <a id="unique.ptr.single.observers">[[unique.ptr.single.observers]]</a>

``` cpp
add_lvalue_reference_t<T> operator*() const;
```

*Requires:* `get() != nullptr`.

*Returns:* `*get()`.

``` cpp
pointer operator->() const noexcept;
```

*Requires:* `get() != nullptr`.

*Returns:* `get()`.

[*Note 4*: The use of this function typically requires that `T` be a
complete type. — *end note*]

``` cpp
pointer get() const noexcept;
```

*Returns:* The stored pointer.

``` cpp
deleter_type& get_deleter() noexcept;
const deleter_type& get_deleter() const noexcept;
```

*Returns:* A reference to the stored deleter.

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `get() != nullptr`.

##### `unique_ptr` modifiers <a id="unique.ptr.single.modifiers">[[unique.ptr.single.modifiers]]</a>

``` cpp
pointer release() noexcept;
```

*Postconditions:* `get() == nullptr`.

*Returns:* The value `get()` had at the start of the call to `release`.

``` cpp
void reset(pointer p = pointer()) noexcept;
```

*Requires:* The expression `get_deleter()(get())` shall be well formed,
shall have well-defined behavior, and shall not throw exceptions.

*Effects:* Assigns `p` to the stored pointer, and then if and only if
the old value of the stored pointer, `old_p`, was not equal to
`nullptr`, calls `get_deleter()(old_p)`.

[*Note 5*: The order of these operations is significant because the
call to `get_deleter()` may destroy `*this`. — *end note*]

*Postconditions:* `get() == p`.

[*Note 6*: The postcondition does not hold if the call to
`get_deleter()` destroys `*this` since `this->get()` is no longer a
valid expression. — *end note*]

``` cpp
void swap(unique_ptr& u) noexcept;
```

*Requires:* `get_deleter()` shall be
swappable ([[swappable.requirements]]) and shall not throw an exception
under `swap`.

*Effects:* Invokes `swap` on the stored pointers and on the stored
deleters of `*this` and `u`.

#### `unique_ptr` for array objects with a runtime length <a id="unique.ptr.runtime">[[unique.ptr.runtime]]</a>

``` cpp
namespace std {
  template <class T, class D> class unique_ptr<T[], D> {
  public:
    using pointer      = see below;
    using element_type = T;
    using deleter_type = D;

    // [unique.ptr.runtime.ctor], constructors
    constexpr unique_ptr() noexcept;
    template <class U> explicit unique_ptr(U p) noexcept;
    template <class U> unique_ptr(U p, see below d) noexcept;
    template <class U> unique_ptr(U p, see below d) noexcept;
    unique_ptr(unique_ptr&& u) noexcept;
    template <class U, class E>
      unique_ptr(unique_ptr<U, E>&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept;

    // destructor
    ~unique_ptr();

    // assignment
    unique_ptr& operator=(unique_ptr&& u) noexcept;
    template <class U, class E>
      unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
    unique_ptr& operator=(nullptr_t) noexcept;

    // [unique.ptr.runtime.observers], observers
    T& operator[](size_t i) const;
    pointer get() const noexcept;
    deleter_type& get_deleter() noexcept;
    const deleter_type& get_deleter() const noexcept;
    explicit operator bool() const noexcept;

    // [unique.ptr.runtime.modifiers], modifiers
    pointer release() noexcept;
    template <class U> void reset(U p) noexcept;
    void reset(nullptr_t = nullptr) noexcept;
    void swap(unique_ptr& u) noexcept;

    // disable copy from lvalue
    unique_ptr(const unique_ptr&) = delete;
    unique_ptr& operator=(const unique_ptr&) = delete;
  };
}
```

A specialization for array types is provided with a slightly altered
interface.

- Conversions between different types of `unique_ptr<T[], D>` that would
  be disallowed for the corresponding pointer-to-array types, and
  conversions to or from the non-array forms of `unique_ptr`, produce an
  ill-formed program.
- Pointers to types derived from `T` are rejected by the constructors,
  and by `reset`.
- The observers `operator*` and `operator->` are not provided.
- The indexing observer `operator[]` is provided.
- The default deleter will call `delete[]`.

Descriptions are provided below only for members that differ from the
primary template.

The template argument `T` shall be a complete type.

##### `unique_ptr` constructors <a id="unique.ptr.runtime.ctor">[[unique.ptr.runtime.ctor]]</a>

``` cpp
template <class U> explicit unique_ptr(U p) noexcept;
```

This constructor behaves the same as the constructor in the primary
template that takes a single parameter of type `pointer` except that it
additionally shall not participate in overload resolution unless

- `U` is the same type as `pointer`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

``` cpp
template <class U> unique_ptr(U p, see below d) noexcept;
template <class U> unique_ptr(U p, see below d) noexcept;
```

These constructors behave the same as the constructors in the primary
template that take a parameter of type `pointer` and a second parameter
except that they shall not participate in overload resolution unless
either

- `U` is the same type as `pointer`,
- `U` is `nullptr_t`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

``` cpp
template <class U, class E>
  unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

This constructor behaves the same as in the primary template, except
that it shall not participate in overload resolution unless all of the
following conditions hold, where `UP` is `unique_ptr<U, E>`:

- `U` is an array type, and
- `pointer` is the same type as `element_type*`, and
- `UP::pointer` is the same type as `UP::element_type*`, and
- `UP::element_type(*)[]` is convertible to `element_type(*)[]`, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

[*Note 1*: This replaces the overload-resolution specification of the
primary template — *end note*]

##### `unique_ptr` assignment <a id="unique.ptr.runtime.asgn">[[unique.ptr.runtime.asgn]]</a>

``` cpp
template <class U, class E>
  unique_ptr& operator=(unique_ptr<U, E>&& u)noexcept;
```

This operator behaves the same as in the primary template, except that
it shall not participate in overload resolution unless all of the
following conditions hold, where `UP` is `unique_ptr<U, E>`:

- `U` is an array type, and
- `pointer` is the same type as `element_type*`, and
- `UP::pointer` is the same type as `UP::element_type*`, and
- `UP::element_type(*)[]` is convertible to `element_type(*)[]`, and
- `is_assignable_v<D&, E&&>` is `true`.

[*Note 2*: This replaces the overload-resolution specification of the
primary template — *end note*]

##### `unique_ptr` observers <a id="unique.ptr.runtime.observers">[[unique.ptr.runtime.observers]]</a>

``` cpp
T& operator[](size_t i) const;
```

*Requires:* `i <` the number of elements in the array to which the
stored pointer points.

*Returns:* `get()[i]`.

##### `unique_ptr` modifiers <a id="unique.ptr.runtime.modifiers">[[unique.ptr.runtime.modifiers]]</a>

``` cpp
void reset(nullptr_t p = nullptr) noexcept;
```

*Effects:* Equivalent to `reset(pointer())`.

``` cpp
template <class U> void reset(U p) noexcept;
```

This function behaves the same as the `reset` member of the primary
template, except that it shall not participate in overload resolution
unless either

- `U` is the same type as `pointer`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

#### `unique_ptr` creation <a id="unique.ptr.create">[[unique.ptr.create]]</a>

``` cpp
template <class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
```

*Remarks:* This function shall not participate in overload resolution
unless `T` is not an array.

*Returns:* `unique_ptr<T>(new T(std::forward<Args>(args)...))`.

``` cpp
template <class T> unique_ptr<T> make_unique(size_t n);
```

*Remarks:* This function shall not participate in overload resolution
unless `T` is an array of unknown bound.

*Returns:* `unique_ptr<T>(new remove_extent_t<T>[n]())`.

``` cpp
template <class T, class... Args> unspecified make_unique(Args&&...) = delete;
```

*Remarks:* This function shall not participate in overload resolution
unless `T` is an array of known bound.

#### `unique_ptr` specialized algorithms <a id="unique.ptr.special">[[unique.ptr.special]]</a>

``` cpp
template <class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;
```

*Remarks:* This function shall not participate in overload resolution
unless `is_swappable_v<D>` is `true`.

*Effects:* Calls `x.swap(y)`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `x.get() == y.get()`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator!=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `x.get() != y.get()`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Requires:* Let *`CT`* denote

``` cpp
common_type_t<typename unique_ptr<T1, D1>::pointer,
              typename unique_ptr<T2, D2>::pointer>
```

Then the specialization `less<`*`CT`*`>` shall be a function object
type ([[function.objects]]) that induces a strict weak
ordering ([[alg.sorting]]) on the pointer values.

*Returns:* `less<`*`CT`*`>()(x.get(), y.get())`.

*Remarks:* If `unique_ptr<T1, D1>::pointer` is not implicitly
convertible to *`CT`* or `unique_ptr<T2, D2>::pointer` is not implicitly
convertible to *`CT`*, the program is ill-formed.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(y < x)`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `y < x`.

``` cpp
template <class T1, class D1, class T2, class D2>
  bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(x < y)`.

``` cpp
template <class T, class D>
  bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
template <class T, class D>
  bool operator==(nullptr_t, const unique_ptr<T, D>& x) noexcept;
```

*Returns:* `!x`.

``` cpp
template <class T, class D>
  bool operator!=(const unique_ptr<T, D>& x, nullptr_t) noexcept;
template <class T, class D>
  bool operator!=(nullptr_t, const unique_ptr<T, D>& x) noexcept;
```

*Returns:* `(bool)x`.

``` cpp
template <class T, class D>
  bool operator<(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator<(nullptr_t, const unique_ptr<T, D>& x);
```

*Requires:* The specialization `less<unique_ptr<T, D>::pointer>` shall
be a function object type ([[function.objects]]) that induces a strict
weak ordering ([[alg.sorting]]) on the pointer values.

*Returns:* The first function template returns
`less<unique_ptr<T, D>::pointer>()(x.get(),`  
`nullptr)`. The second function template returns
`less<unique_ptr<T, D>::pointer>()(nullptr, x.get())`.

``` cpp
template <class T, class D>
  bool operator>(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator>(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `nullptr < x`. The second
function template returns `x < nullptr`.

``` cpp
template <class T, class D>
  bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator<=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(nullptr < x)`. The
second function template returns `!(x < nullptr)`.

``` cpp
template <class T, class D>
  bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
template <class T, class D>
  bool operator>=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(x < nullptr)`. The
second function template returns `!(nullptr < x)`.

### Shared-ownership pointers <a id="util.smartptr">[[util.smartptr]]</a>

#### Class `bad_weak_ptr` <a id="util.smartptr.weak.bad">[[util.smartptr.weak.bad]]</a>

``` cpp
namespace std {
  class bad_weak_ptr : public exception {
  public:
    bad_weak_ptr() noexcept;
  };
}
```

An exception of type `bad_weak_ptr` is thrown by the `shared_ptr`
constructor taking a `weak_ptr`.

``` cpp
bad_weak_ptr() noexcept;
```

*Postconditions:* `what()` returns an *implementation-defined* NTBS.

#### Class template `shared_ptr` <a id="util.smartptr.shared">[[util.smartptr.shared]]</a>

The `shared_ptr` class template stores a pointer, usually obtained via
`new`. `shared_ptr` implements semantics of shared ownership; the last
remaining owner of the pointer is responsible for destroying the object,
or otherwise releasing the resources associated with the stored pointer.
A `shared_ptr` is said to be empty if it does not own a pointer.

``` cpp
namespace std {
  template<class T> class shared_ptr {
  public:
    using element_type = remove_extent_t<T>;
    using weak_type    = weak_ptr<T>;

    // [util.smartptr.shared.const], constructors
    constexpr shared_ptr() noexcept;
    template<class Y> explicit shared_ptr(Y* p);
    template<class Y, class D> shared_ptr(Y* p, D d);
    template<class Y, class D, class A> shared_ptr(Y* p, D d, A a);
    template <class D> shared_ptr(nullptr_t p, D d);
    template <class D, class A> shared_ptr(nullptr_t p, D d, A a);
    template<class Y> shared_ptr(const shared_ptr<Y>& r, element_type* p) noexcept;
    shared_ptr(const shared_ptr& r) noexcept;
    template<class Y> shared_ptr(const shared_ptr<Y>& r) noexcept;
    shared_ptr(shared_ptr&& r) noexcept;
    template<class Y> shared_ptr(shared_ptr<Y>&& r) noexcept;
    template<class Y> explicit shared_ptr(const weak_ptr<Y>& r);
    template <class Y, class D> shared_ptr(unique_ptr<Y, D>&& r);
    constexpr shared_ptr(nullptr_t) noexcept : shared_ptr() { }

    // [util.smartptr.shared.dest], destructor
    ~shared_ptr();

    // [util.smartptr.shared.assign], assignment
    shared_ptr& operator=(const shared_ptr& r) noexcept;
    template<class Y> shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    shared_ptr& operator=(shared_ptr&& r) noexcept;
    template<class Y> shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
    template <class Y, class D> shared_ptr& operator=(unique_ptr<Y, D>&& r);

    // [util.smartptr.shared.mod], modifiers
    void swap(shared_ptr& r) noexcept;
    void reset() noexcept;
    template<class Y> void reset(Y* p);
    template<class Y, class D> void reset(Y* p, D d);
    template<class Y, class D, class A> void reset(Y* p, D d, A a);

    // [util.smartptr.shared.obs], observers
    element_type* get() const noexcept;
    T& operator*() const noexcept;
    T* operator->() const noexcept;
    element_type& operator[](ptrdiff_t i) const;
    long use_count() const noexcept;
    explicit operator bool() const noexcept;
    template<class U> bool owner_before(const shared_ptr<U>& b) const noexcept;
    template<class U> bool owner_before(const weak_ptr<U>& b) const noexcept;
  };

  template<class T> shared_ptr(weak_ptr<T>) -> shared_ptr<T>;
  template<class T, class D> shared_ptr(unique_ptr<T, D>) -> shared_ptr<T>;

  // [util.smartptr.shared.create], shared_ptr creation
  template<class T, class... Args>
    shared_ptr<T> make_shared(Args&&... args);
  template<class T, class A, class... Args>
    shared_ptr<T> allocate_shared(const A& a, Args&&... args);

  // [util.smartptr.shared.cmp], shared_ptr comparisons
  template<class T, class U>
    bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator!=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator<(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator<=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    bool operator>=(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;

  template <class T>
    bool operator==(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator==(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator!=(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator!=(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator<(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator<(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator<=(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator<=(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator>(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator>(nullptr_t, const shared_ptr<T>& b) noexcept;
  template <class T>
    bool operator>=(const shared_ptr<T>& a, nullptr_t) noexcept;
  template <class T>
    bool operator>=(nullptr_t, const shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.spec], shared_ptr specialized algorithms
  template<class T>
    void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.cast], shared_ptr casts
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& r) noexcept;

  // [util.smartptr.getdeleter], shared_ptr get_deleter
  template<class D, class T>
    D* get_deleter(const shared_ptr<T>& p) noexcept;

  // [util.smartptr.shared.io], shared_ptr I/O
  template<class E, class T, class Y>
    basic_ostream<E, T>& operator<< (basic_ostream<E, T>& os, const shared_ptr<Y>& p);
}
```

Specializations of `shared_ptr` shall be `CopyConstructible`,
`CopyAssignable`, and `LessThanComparable`, allowing their use in
standard containers. Specializations of `shared_ptr` shall be
contextually convertible to `bool`, allowing their use in boolean
expressions and declarations in conditions. The template parameter `T`
of `shared_ptr` may be an incomplete type.

[*Example 1*:

``` cpp
if (shared_ptr<X> px = dynamic_pointer_cast<X>(py)) {
  // do something with px
}
```

— *end example*]

For purposes of determining the presence of a data race, member
functions shall access and modify only the `shared_ptr` and `weak_ptr`
objects themselves and not objects they refer to. Changes in
`use_count()` do not reflect modifications that can introduce data
races.

For the purposes of subclause [[util.smartptr]], a pointer type `Y*` is
said to be *compatible with* a pointer type `T*` when either `Y*` is
convertible to `T*` or `Y` is `U[N]` and `T` is cv `U[]`.

##### `shared_ptr` constructors <a id="util.smartptr.shared.const">[[util.smartptr.shared.const]]</a>

In the constructor definitions below, enables `shared_from_this` with
`p`, for a pointer `p` of type `Y*`, means that if `Y` has an
unambiguous and accessible base class that is a specialization of
`enable_shared_from_this` ([[util.smartptr.enab]]), then
`remove_cv_t<Y>*` shall be implicitly convertible to `T*` and the
constructor evaluates the statement:

``` cpp
if (p != nullptr && p->weak_this.expired())
  p->weak_this = shared_ptr<remove_cv_t<Y>>(*this, const_cast<remove_cv_t<Y>*>(p));
```

The assignment to the `weak_this` member is not atomic and conflicts
with any potentially concurrent access to the same object (
[[intro.multithread]]).

``` cpp
constexpr shared_ptr() noexcept;
```

*Effects:* Constructs an empty `shared_ptr` object.

*Postconditions:* `use_count() == 0 && get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(Y* p);
```

*Requires:* `Y` shall be a complete type. The expression `delete[] p`,
when `T` is an array type, or `delete p`, when `T` is not an array type,
shall have well-defined behavior, and shall not throw exceptions.

*Effects:* When `T` is not an array type, constructs a `shared_ptr`
object that owns the pointer `p`. Otherwise, constructs a `shared_ptr`
that owns `p` and a deleter of an unspecified type that calls
`delete[] p`. When `T` is not an array type, enables `shared_from_this`
with `p`. If an exception is thrown, `delete p` is called when `T` is
not an array type, `delete[] p` otherwise.

*Postconditions:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

*Remarks:* When `T` is an array type, this constructor shall not
participate in overload resolution unless the expression `delete[] p` is
well-formed and either `T` is `U[N]` and `Y(*)[N]` is convertible to
`T*`, or `T` is `U[]` and `Y(*)[]` is convertible to `T*`. When `T` is
not an array type, this constructor shall not participate in overload
resolution unless the expression `delete p` is well-formed and `Y*` is
convertible to `T*`.

``` cpp
template<class Y, class D> shared_ptr(Y* p, D d);
template<class Y, class D, class A> shared_ptr(Y* p, D d, A a);
template <class D> shared_ptr(nullptr_t p, D d);
template <class D, class A> shared_ptr(nullptr_t p, D d, A a);
```

*Requires:* Construction of `d` and a deleter of type `D` initialized
with `std::move(d)` shall not throw exceptions. The expression `d(p)`
shall have well-defined behavior and shall not throw exceptions. `A`
shall be an allocator ([[allocator.requirements]]).

*Effects:* Constructs a `shared_ptr` object that owns the object `p` and
the deleter `d`. When `T` is not an array type, the first and second
constructors enable `shared_from_this` with `p`. The second and fourth
constructors shall use a copy of `a` to allocate memory for internal
use. If an exception is thrown, `d(p)` is called.

*Postconditions:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

*Remarks:* When `T` is an array type, this constructor shall not
participate in overload resolution unless `is_move_constructible_v<D>`
is `true`, the expression `d(p)` is well-formed, and either `T` is
`U[N]` and `Y(*)[N]` is convertible to `T*`, or `T` is `U[]` and
`Y(*)[]` is convertible to `T*`. When `T` is not an array type, this
constructor shall not participate in overload resolution unless
`is_move_constructible_v<D>` is `true`, the expression `d(p)` is
well-formed, and `Y*` is convertible to `T*`.

``` cpp
template<class Y> shared_ptr(const shared_ptr<Y>& r, element_type* p) noexcept;
```

*Effects:* Constructs a `shared_ptr` instance that stores `p` and shares
ownership with `r`.

*Postconditions:* `get() == p && use_count() == r.use_count()`.

[*Note 1*: To avoid the possibility of a dangling pointer, the user of
this constructor must ensure that `p` remains valid at least until the
ownership group of `r` is destroyed. — *end note*]

[*Note 2*: This constructor allows creation of an empty `shared_ptr`
instance with a non-null stored pointer. — *end note*]

``` cpp
shared_ptr(const shared_ptr& r) noexcept;
template<class Y> shared_ptr(const shared_ptr<Y>& r) noexcept;
```

*Remarks:* The second constructor shall not participate in overload
resolution unless `Y*` is compatible with `T*`.

*Effects:* If `r` is empty, constructs an empty `shared_ptr` object;
otherwise, constructs a `shared_ptr` object that shares ownership with
`r`.

*Postconditions:* `get() == r.get() && use_count() == r.use_count()`.

``` cpp
shared_ptr(shared_ptr&& r) noexcept;
template<class Y> shared_ptr(shared_ptr<Y>&& r) noexcept;
```

*Remarks:* The second constructor shall not participate in overload
resolution unless `Y*` is compatible with `T*`.

*Effects:* Move constructs a `shared_ptr` instance from `r`.

*Postconditions:* `*this` shall contain the old value of `r`. `r` shall
be empty. `r.get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(const weak_ptr<Y>& r);
```

*Effects:* Constructs a `shared_ptr` object that shares ownership with
`r` and stores a copy of the pointer stored in `r`. If an exception is
thrown, the constructor has no effect.

*Postconditions:* `use_count() == r.use_count()`.

*Throws:* `bad_weak_ptr` when `r.expired()`.

*Remarks:* This constructor shall not participate in overload resolution
unless `Y*` is compatible with `T*`.

``` cpp
template <class Y, class D> shared_ptr(unique_ptr<Y, D>&& r);
```

*Remarks:* This constructor shall not participate in overload resolution
unless `Y*` is compatible with `T*` and `unique_ptr<Y, D>::pointer` is
convertible to `element_type*`.

*Effects:* If `r.get() == nullptr`, equivalent to `shared_ptr()`.
Otherwise, if `D` is not a reference type, equivalent to
`shared_ptr(r.release(), r.get_deleter())`. Otherwise, equivalent to
`shared_ptr(r.release(), ref(r.get_deleter()))`. If an exception is
thrown, the constructor has no effect.

##### `shared_ptr` destructor <a id="util.smartptr.shared.dest">[[util.smartptr.shared.dest]]</a>

``` cpp
~shared_ptr();
```

*Effects:*

- If `*this` is empty or shares ownership with another `shared_ptr`
  instance (`use_count() > 1`), there are no side effects.
- Otherwise, if `*this` owns an object `p` and a deleter `d`, `d(p)` is
  called.
- Otherwise, `*this` owns a pointer `p`, and `delete p` is called.

[*Note 1*: Since the destruction of `*this` decreases the number of
instances that share ownership with `*this` by one, after `*this` has
been destroyed all `shared_ptr` instances that shared ownership with
`*this` will report a `use_count()` that is one less than its previous
value. — *end note*]

##### `shared_ptr` assignment <a id="util.smartptr.shared.assign">[[util.smartptr.shared.assign]]</a>

``` cpp
shared_ptr& operator=(const shared_ptr& r) noexcept;
template<class Y> shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `shared_ptr(r).swap(*this)`.

*Returns:* `*this`.

[*Note 3*:

The use count updates caused by the temporary object construction and
destruction are not observable side effects, so the implementation may
meet the effects (and the implied guarantees) via different means,
without creating a temporary. In particular, in the example:

``` cpp
shared_ptr<int> p(new int);
shared_ptr<void> q(p);
p = p;
q = p;
```

both assignments may be no-ops.

— *end note*]

``` cpp
shared_ptr& operator=(shared_ptr&& r) noexcept;
template<class Y> shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

``` cpp
template <class Y, class D> shared_ptr& operator=(unique_ptr<Y, D>&& r);
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

##### `shared_ptr` modifiers <a id="util.smartptr.shared.mod">[[util.smartptr.shared.mod]]</a>

``` cpp
void swap(shared_ptr& r) noexcept;
```

*Effects:* Exchanges the contents of `*this` and `r`.

``` cpp
void reset() noexcept;
```

*Effects:* Equivalent to `shared_ptr().swap(*this)`.

``` cpp
template<class Y> void reset(Y* p);
```

*Effects:* Equivalent to `shared_ptr(p).swap(*this)`.

``` cpp
template<class Y, class D> void reset(Y* p, D d);
```

*Effects:* Equivalent to `shared_ptr(p, d).swap(*this)`.

``` cpp
template<class Y, class D, class A> void reset(Y* p, D d, A a);
```

*Effects:* Equivalent to `shared_ptr(p, d, a).swap(*this)`.

##### `shared_ptr` observers <a id="util.smartptr.shared.obs">[[util.smartptr.shared.obs]]</a>

``` cpp
element_type* get() const noexcept;
```

*Returns:* The stored pointer.

``` cpp
T& operator*() const noexcept;
```

*Requires:* `get() != 0`.

*Returns:* `*get()`.

*Remarks:* When `T` is an array type or cv `void`, it is unspecified
whether this member function is declared. If it is declared, it is
unspecified what its return type is, except that the declaration
(although not necessarily the definition) of the function shall be well
formed.

``` cpp
T* operator->() const noexcept;
```

*Requires:* `get() != 0`.

*Returns:* `get()`.

*Remarks:* When `T` is an array type, it is unspecified whether this
member function is declared. If it is declared, it is unspecified what
its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well formed.

``` cpp
element_type& operator[](ptrdiff_t i) const;
```

*Requires:* `get() != 0 && i >= 0`. If `T` is `U[N]`, `i < N`.

*Returns:* `get()[i]`.

*Remarks:* When `T` is not an array type, it is unspecified whether this
member function is declared. If it is declared, it is unspecified what
its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well formed.

*Throws:* Nothing.

``` cpp
long use_count() const noexcept;
```

*Returns:* The number of `shared_ptr` objects, `*this` included, that
share ownership with `*this`, or `0` when `*this` is empty.

*Synchronization:* None.

[*Note 4*: `get() == nullptr` does not imply a specific return value of
`use_count()`. — *end note*]

[*Note 5*: `weak_ptr<T>::lock()` can affect the return value of
`use_count()`. — *end note*]

[*Note 6*: When multiple threads can affect the return value of
`use_count()`, the result should be treated as approximate. In
particular, `use_count() == 1` does not imply that accesses through a
previously destroyed `shared_ptr` have in any sense
completed. — *end note*]

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `get() != 0`.

``` cpp
template<class U> bool owner_before(const shared_ptr<U>& b) const noexcept;
template<class U> bool owner_before(const weak_ptr<U>& b) const noexcept;
```

*Returns:* An unspecified value such that

- `x.owner_before(y)` defines a strict weak ordering as defined
  in  [[alg.sorting]];
- under the equivalence relation defined by `owner_before`,
  `!a.owner_before(b) && !b.owner_before(a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

##### `shared_ptr` creation <a id="util.smartptr.shared.create">[[util.smartptr.shared.create]]</a>

``` cpp
template<class T, class... Args>
  shared_ptr<T> make_shared(Args&&... args);
template<class T, class A, class... Args>
  shared_ptr<T> allocate_shared(const A& a, Args&&... args);
```

*Requires:* The expression `::new (pv) T(std::forward<Args>(args)...)`,
where `pv` has type `void*` and points to storage suitable to hold an
object of type `T`, shall be well formed. `A` shall be an
allocator ([[allocator.requirements]]). The copy constructor and
destructor of `A` shall not throw exceptions.

*Effects:* Allocates memory suitable for an object of type `T` and
constructs an object in that memory via the placement *new-expression*
`::new (pv) T(std::forward<Args>(args)...)`. The template
`allocate_shared` uses a copy of `a` to allocate memory. If an exception
is thrown, the functions have no effect.

*Returns:* A `shared_ptr` instance that stores and owns the address of
the newly constructed object of type `T`.

*Postconditions:* `get() != 0 && use_count() == 1`.

*Throws:* `bad_alloc`, or an exception thrown from `A::allocate` or from
the constructor of `T`.

*Remarks:* The `shared_ptr` constructor called by this function enables
`shared_from_this` with the address of the newly constructed object of
type `T`. Implementations should perform no more than one memory
allocation.

[*Note 7*: This provides efficiency equivalent to an intrusive smart
pointer. — *end note*]

[*Note 8*: These functions will typically allocate more memory than
`sizeof(T)` to allow for internal bookkeeping structures such as the
reference counts. — *end note*]

##### `shared_ptr` comparison <a id="util.smartptr.shared.cmp">[[util.smartptr.shared.cmp]]</a>

``` cpp
template<class T, class U>
  bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `a.get() == b.get()`.

``` cpp
template<class T, class U>
  bool operator<(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `less<>()(a.get(), b.get())`.

[*Note 9*: Defining a comparison function allows `shared_ptr` objects
to be used as keys in associative containers. — *end note*]

``` cpp
template <class T>
  bool operator==(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator==(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* `!a`.

``` cpp
template <class T>
  bool operator!=(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator!=(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* `(bool)a`.

``` cpp
template <class T>
  bool operator<(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator<(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns
`less<shared_ptr<T>::element_type*>()(a.get(), nullptr)`. The second
function template returns
`less<shared_ptr<T>::element_type*>()(nullptr, a.get())`.

``` cpp
template <class T>
  bool operator>(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator>(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns `nullptr < a`. The second
function template returns `a < nullptr`.

``` cpp
template <class T>
  bool operator<=(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator<=(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns `!(nullptr < a)`. The
second function template returns `!(a < nullptr)`.

``` cpp
template <class T>
  bool operator>=(const shared_ptr<T>& a, nullptr_t) noexcept;
template <class T>
  bool operator>=(nullptr_t, const shared_ptr<T>& a) noexcept;
```

*Returns:* The first function template returns `!(a < nullptr)`. The
second function template returns `!(nullptr < a)`.

##### `shared_ptr` specialized algorithms <a id="util.smartptr.shared.spec">[[util.smartptr.shared.spec]]</a>

``` cpp
template<class T>
  void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

##### `shared_ptr` casts <a id="util.smartptr.shared.cast">[[util.smartptr.shared.cast]]</a>

``` cpp
template<class T, class U>
  shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `static_cast<T*>((U*)0)` shall be well
formed.

*Returns:*

``` cpp
shared_ptr<T>(r, static_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

[*Note 10*: The seemingly equivalent expression
`shared_ptr<T>(static_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

``` cpp
template<class T, class U>
  shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `dynamic_cast<T*>((U*)0)` shall be well
formed and shall have well defined behavior.

*Returns:*

- When `dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())`
  returns a nonzero value `p`, `shared_ptr<T>(r, p)`.
- Otherwise, `shared_ptr<T>()`.

[*Note 11*: The seemingly equivalent expression
`shared_ptr<T>(dynamic_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

``` cpp
template<class T, class U>
  shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `const_cast<T*>((U*)0)` shall be well formed.

*Returns:*

``` cpp
shared_ptr<T>(r, const_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

[*Note 12*: The seemingly equivalent expression
`shared_ptr<T>(const_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

``` cpp
template<class T, class U>
  shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& r) noexcept;
```

*Requires:* The expression `reinterpret_cast<T*>((U*)0)` shall be well
formed.

*Returns:*

``` cpp
shared_ptr<T>(r, reinterpret_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

[*Note 13*: The seemingly equivalent expression
`shared_ptr<T>(reinterpret_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

##### `get_deleter` <a id="util.smartptr.getdeleter">[[util.smartptr.getdeleter]]</a>

``` cpp
template<class D, class T>
  D* get_deleter(const shared_ptr<T>& p) noexcept;
```

*Returns:* If `p` owns a deleter `d` of type cv-unqualified `D`, returns
`addressof(d)`; otherwise returns `nullptr`. The returned pointer
remains valid as long as there exists a `shared_ptr` instance that owns
`d`.

[*Note 14*: It is unspecified whether the pointer remains valid longer
than that. This can happen if the implementation doesn’t destroy the
deleter until all `weak_ptr` instances that share ownership with `p`
have been destroyed. — *end note*]

##### `shared_ptr` I/O <a id="util.smartptr.shared.io">[[util.smartptr.shared.io]]</a>

``` cpp
template<class E, class T, class Y>
  basic_ostream<E, T>& operator<< (basic_ostream<E, T>& os, const shared_ptr<Y>& p);
```

*Effects:* As if by: `os << p.get();`

*Returns:* `os`.

#### Class template `weak_ptr` <a id="util.smartptr.weak">[[util.smartptr.weak]]</a>

The `weak_ptr` class template stores a weak reference to an object that
is already managed by a `shared_ptr`. To access the object, a `weak_ptr`
can be converted to a `shared_ptr` using the member function `lock`.

``` cpp
namespace std {
  template<class T> class weak_ptr {
  public:
    using element_type = T;

    // [util.smartptr.weak.const], constructors
    constexpr weak_ptr() noexcept;
    template<class Y> weak_ptr(const shared_ptr<Y>& r) noexcept;
    weak_ptr(const weak_ptr& r) noexcept;
    template<class Y> weak_ptr(const weak_ptr<Y>& r) noexcept;
    weak_ptr(weak_ptr&& r) noexcept;
    template<class Y> weak_ptr(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.dest], destructor
    ~weak_ptr();

    // [util.smartptr.weak.assign], assignment
    weak_ptr& operator=(const weak_ptr& r) noexcept;
    template<class Y> weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
    template<class Y> weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    weak_ptr& operator=(weak_ptr&& r) noexcept;
    template<class Y> weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.mod], modifiers
    void swap(weak_ptr& r) noexcept;
    void reset() noexcept;

    // [util.smartptr.weak.obs], observers
    long use_count() const noexcept;
    bool expired() const noexcept;
    shared_ptr<T> lock() const noexcept;
    template<class U> bool owner_before(const shared_ptr<U>& b) const;
    template<class U> bool owner_before(const weak_ptr<U>& b) const;
  };

  template<class T> weak_ptr(shared_ptr<T>) -> weak_ptr<T>;


  // [util.smartptr.weak.spec], specialized algorithms
  template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
}
```

Specializations of `weak_ptr` shall be `CopyConstructible` and
`CopyAssignable`, allowing their use in standard containers. The
template parameter `T` of `weak_ptr` may be an incomplete type.

##### `weak_ptr` constructors <a id="util.smartptr.weak.const">[[util.smartptr.weak.const]]</a>

``` cpp
constexpr weak_ptr() noexcept;
```

*Effects:* Constructs an empty `weak_ptr` object.

*Postconditions:* `use_count() == 0`.

``` cpp
weak_ptr(const weak_ptr& r) noexcept;
template<class Y> weak_ptr(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr(const shared_ptr<Y>& r) noexcept;
```

*Remarks:* The second and third constructors shall not participate in
overload resolution unless `Y*` is compatible with `T*`.

*Effects:* If `r` is empty, constructs an empty `weak_ptr` object;
otherwise, constructs a `weak_ptr` object that shares ownership with `r`
and stores a copy of the pointer stored in `r`.

*Postconditions:* `use_count() == r.use_count()`.

``` cpp
weak_ptr(weak_ptr&& r) noexcept;
template<class Y> weak_ptr(weak_ptr<Y>&& r) noexcept;
```

*Remarks:* The second constructor shall not participate in overload
resolution unless `Y*` is compatible with `T*`.

*Effects:* Move constructs a `weak_ptr` instance from `r`.

*Postconditions:* `*this` shall contain the old value of `r`. `r` shall
be empty. `r.use_count() == 0`.

##### `weak_ptr` destructor <a id="util.smartptr.weak.dest">[[util.smartptr.weak.dest]]</a>

``` cpp
~weak_ptr();
```

*Effects:* Destroys this `weak_ptr` object but has no effect on the
object its stored pointer points to.

##### `weak_ptr` assignment <a id="util.smartptr.weak.assign">[[util.smartptr.weak.assign]]</a>

``` cpp
weak_ptr& operator=(const weak_ptr& r) noexcept;
template<class Y> weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(r).swap(*this)`.

*Remarks:* The implementation may meet the effects (and the implied
guarantees) via different means, without creating a temporary.

*Returns:* `*this`.

``` cpp
weak_ptr& operator=(weak_ptr&& r) noexcept;
template<class Y> weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

##### `weak_ptr` modifiers <a id="util.smartptr.weak.mod">[[util.smartptr.weak.mod]]</a>

``` cpp
void swap(weak_ptr& r) noexcept;
```

*Effects:* Exchanges the contents of `*this` and `r`.

``` cpp
void reset() noexcept;
```

*Effects:* Equivalent to `weak_ptr().swap(*this)`.

##### `weak_ptr` observers <a id="util.smartptr.weak.obs">[[util.smartptr.weak.obs]]</a>

``` cpp
long use_count() const noexcept;
```

*Returns:* `0` if `*this` is empty; otherwise, the number of
`shared_ptr` instances that share ownership with `*this`.

``` cpp
bool expired() const noexcept;
```

*Returns:* `use_count() == 0`.

``` cpp
shared_ptr<T> lock() const noexcept;
```

*Returns:* `expired() ? shared_ptr<T>() : shared_ptr<T>(*this)`,
executed atomically.

``` cpp
template<class U> bool owner_before(const shared_ptr<U>& b) const;
template<class U> bool owner_before(const weak_ptr<U>& b) const;
```

*Returns:* An unspecified value such that

- `x.owner_before(y)` defines a strict weak ordering as defined
  in  [[alg.sorting]];
- under the equivalence relation defined by `owner_before`,
  `!a.owner_before(b) && !b.owner_before(a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

##### `weak_ptr` specialized algorithms <a id="util.smartptr.weak.spec">[[util.smartptr.weak.spec]]</a>

``` cpp
template<class T>
  void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

#### Class template `owner_less` <a id="util.smartptr.ownerless">[[util.smartptr.ownerless]]</a>

The class template `owner_less` allows ownership-based mixed comparisons
of shared and weak pointers.

``` cpp
namespace std {
  template<class T = void> struct owner_less;

  template<class T> struct owner_less<shared_ptr<T>> {
    bool operator()(const shared_ptr<T>&, const shared_ptr<T>&) const noexcept;
    bool operator()(const shared_ptr<T>&, const weak_ptr<T>&) const noexcept;
    bool operator()(const weak_ptr<T>&, const shared_ptr<T>&) const noexcept;
  };

  template<class T> struct owner_less<weak_ptr<T>> {
    bool operator()(const weak_ptr<T>&, const weak_ptr<T>&) const noexcept;
    bool operator()(const shared_ptr<T>&, const weak_ptr<T>&) const noexcept;
    bool operator()(const weak_ptr<T>&, const shared_ptr<T>&) const noexcept;
  };

  template<> struct owner_less<void> {
    template<class T, class U>
      bool operator()(const shared_ptr<T>&, const shared_ptr<U>&) const noexcept;
    template<class T, class U>
      bool operator()(const shared_ptr<T>&, const weak_ptr<U>&) const noexcept;
    template<class T, class U>
      bool operator()(const weak_ptr<T>&, const shared_ptr<U>&) const noexcept;
    template<class T, class U>
      bool operator()(const weak_ptr<T>&, const weak_ptr<U>&) const noexcept;

    using is_transparent = unspecified;
  };
}
```

`operator()(x, y)` shall return `x.owner_before(y)`.

[*Note 1*:

Note that

- `operator()` defines a strict weak ordering as defined in 
  [[alg.sorting]];
- under the equivalence relation defined by `operator()`,
  `!operator()(a, b) && !operator()(b, a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

— *end note*]

#### Class template `enable_shared_from_this` <a id="util.smartptr.enab">[[util.smartptr.enab]]</a>

A class `T` can inherit from `enable_shared_from_this<T>` to inherit the
`shared_from_this` member functions that obtain a `shared_ptr` instance
pointing to `*this`.

[*Example 1*:

``` cpp
struct X: public enable_shared_from_this<X> { };

int main() {
  shared_ptr<X> p(new X);
  shared_ptr<X> q = p->shared_from_this();
  assert(p == q);
  assert(!p.owner_before(q) && !q.owner_before(p)); // p and q share ownership
}
```

— *end example*]

``` cpp
namespace std {
  template<class T> class enable_shared_from_this {
  protected:
    constexpr enable_shared_from_this() noexcept;
    enable_shared_from_this(const enable_shared_from_this&) noexcept;
    enable_shared_from_this& operator=(const enable_shared_from_this&) noexcept;
    ~enable_shared_from_this();
  public:
    shared_ptr<T> shared_from_this();
    shared_ptr<T const> shared_from_this() const;
    weak_ptr<T> weak_from_this() noexcept;
    weak_ptr<T const> weak_from_this() const noexcept;
  private:
    mutable weak_ptr<T> weak_this; // exposition only
  };
}
```

The template parameter `T` of `enable_shared_from_this` may be an
incomplete type.

``` cpp
constexpr enable_shared_from_this() noexcept;
enable_shared_from_this(const enable_shared_from_this<T>&) noexcept;
```

*Effects:* Value-initializes `weak_this`.

``` cpp
enable_shared_from_this<T>& operator=(const enable_shared_from_this<T>&) noexcept;
```

*Returns:* `*this`.

[*Note 1*: `weak_this` is not changed. — *end note*]

``` cpp
shared_ptr<T>       shared_from_this();
shared_ptr<T const> shared_from_this() const;
```

*Returns:* `shared_ptr<T>(weak_this)`.

``` cpp
weak_ptr<T>       weak_from_this() noexcept;
weak_ptr<T const> weak_from_this() const noexcept;
```

*Returns:* `weak_this`.

#### `shared_ptr` atomic access <a id="util.smartptr.shared.atomic">[[util.smartptr.shared.atomic]]</a>

Concurrent access to a `shared_ptr` object from multiple threads does
not introduce a data race if the access is done exclusively via the
functions in this section and the instance is passed as their first
argument.

The meaning of the arguments of type `memory_order` is explained in 
[[atomics.order]].

``` cpp
template<class T>
  bool atomic_is_lock_free(const shared_ptr<T>* p);
```

*Requires:* `p` shall not be null.

*Returns:* `true` if atomic access to `*p` is lock-free, `false`
otherwise.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_load(const shared_ptr<T>* p);
```

*Requires:* `p` shall not be null.

*Returns:* `atomic_load_explicit(p, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_load_explicit(const shared_ptr<T>* p, memory_order mo);
```

*Requires:* `p` shall not be null.

*Requires:* `mo` shall not be `memory_order_release` or
`memory_order_acq_rel`.

*Returns:* `*p`.

*Throws:* Nothing.

``` cpp
template<class T>
  void atomic_store(shared_ptr<T>* p, shared_ptr<T> r);
```

*Requires:* `p` shall not be null.

*Effects:* As if by `atomic_store_explicit(p, r, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  void atomic_store_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);
```

*Requires:* `p` shall not be null.

*Requires:* `mo` shall not be `memory_order_acquire` or
`memory_order_acq_rel`.

*Effects:* As if by `p->swap(r)`.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_exchange(shared_ptr<T>* p, shared_ptr<T> r);
```

*Requires:* `p` shall not be null.

*Returns:* `atomic_exchange_explicit(p, r, memory_order_seq_cst)`.

*Throws:* Nothing.

``` cpp
template<class T>
  shared_ptr<T> atomic_exchange_explicit(shared_ptr<T>* p, shared_ptr<T> r, memory_order mo);
```

*Requires:* `p` shall not be null.

*Effects:* As if by `p->swap(r)`.

*Returns:* The previous value of `*p`.

*Throws:* Nothing.

``` cpp
template<class T>
  bool atomic_compare_exchange_weak(shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
```

*Requires:* `p` shall not be null and `v` shall not be null.

*Returns:*

``` cpp
atomic_compare_exchange_weak_explicit(p, v, w, memory_order_seq_cst, memory_order_seq_cst)
```

*Throws:* Nothing.

``` cpp
template<class T>
  bool atomic_compare_exchange_strong(shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w);
```

*Returns:*

``` cpp
atomic_compare_exchange_strong_explicit(p, v, w, memory_order_seq_cst, memory_order_seq_cst)
```

``` cpp
template<class T>
  bool atomic_compare_exchange_weak_explicit(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
    memory_order success, memory_order failure);
template<class T>
  bool atomic_compare_exchange_strong_explicit(
    shared_ptr<T>* p, shared_ptr<T>* v, shared_ptr<T> w,
    memory_order success, memory_order failure);
```

*Requires:* `p` shall not be null and `v` shall not be null. The
`failure` argument shall not be `memory_order_release` nor
`memory_order_acq_rel`.

*Effects:* If `*p` is equivalent to `*v`, assigns `w` to `*p` and has
synchronization semantics corresponding to the value of `success`,
otherwise assigns `*p` to `*v` and has synchronization semantics
corresponding to the value of `failure`.

*Returns:* `true` if `*p` was equivalent to `*v`, `false` otherwise.

*Throws:* Nothing.

*Remarks:* Two `shared_ptr` objects are equivalent if they store the
same pointer value and share ownership. The weak form may fail
spuriously. See  [[atomics.types.operations]].

#### Smart pointer hash support <a id="util.smartptr.hash">[[util.smartptr.hash]]</a>

``` cpp
template <class T, class D> struct hash<unique_ptr<T, D>>;
```

Letting `UP` be `unique_ptr<T,D>`, the specialization `hash<UP>` is
enabled ([[unord.hash]]) if and only if `hash<typename UP::pointer>` is
enabled. When enabled, for an object `p` of type `UP`, `hash<UP>()(p)`
shall evaluate to the same value as
`hash<typename UP::pointer>()(p.get())`. The member functions are not
guaranteed to be `noexcept`.

``` cpp
template <class T> struct hash<shared_ptr<T>>;
```

For an object `p` of type `shared_ptr<T>`, `hash<shared_ptr<T>>()(p)`
shall evaluate to the same value as
`hash<typename shared_ptr<T>::element_type*>()(p.get())`.

## Memory resources <a id="mem.res">[[mem.res]]</a>

### Header `<memory_resource>` synopsis <a id="mem.res.syn">[[mem.res.syn]]</a>

``` cpp
namespace std::pmr {
  // [mem.res.class], class memory_resource
  class memory_resource;

  bool operator==(const memory_resource& a, const memory_resource& b) noexcept;
  bool operator!=(const memory_resource& a, const memory_resource& b) noexcept;

  // [mem.poly.allocator.class], class template polymorphic_allocator
  template <class Tp> class polymorphic_allocator;

  template <class T1, class T2>
    bool operator==(const polymorphic_allocator<T1>& a,
                    const polymorphic_allocator<T2>& b) noexcept;
  template <class T1, class T2>
    bool operator!=(const polymorphic_allocator<T1>& a,
                    const polymorphic_allocator<T2>& b) noexcept;

  // [mem.res.global], global memory resources
  memory_resource* new_delete_resource() noexcept;
  memory_resource* null_memory_resource() noexcept;
  memory_resource* set_default_resource(memory_resource* r) noexcept;
  memory_resource* get_default_resource() noexcept;

  // [mem.res.pool], pool resource classes
  struct pool_options;
  class synchronized_pool_resource;
  class unsynchronized_pool_resource;
  class monotonic_buffer_resource;
}
```

### Class `memory_resource` <a id="mem.res.class">[[mem.res.class]]</a>

The `memory_resource` class is an abstract interface to an unbounded set
of classes encapsulating memory resources.

``` cpp
class memory_resource {
  static constexpr size_t max_align = alignof(max_align_t); // exposition only

public:
  virtual ~memory_resource();

  void* allocate(size_t bytes, size_t alignment = max_align);
  void deallocate(void* p, size_t bytes, size_t alignment = max_align);

  bool is_equal(const memory_resource& other) const noexcept;

private:
  virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
  virtual void do_deallocate(void* p, size_t bytes, size_t alignment) = 0;

  virtual bool do_is_equal(const memory_resource& other) const noexcept = 0;
};
```

#### `memory_resource` public member functions <a id="mem.res.public">[[mem.res.public]]</a>

``` cpp
~memory_resource();
```

*Effects:* Destroys this `memory_resource`.

``` cpp
void* allocate(size_t bytes, size_t alignment = max_align);
```

*Effects:* Equivalent to: `return do_allocate(bytes, alignment);`

``` cpp
void deallocate(void* p, size_t bytes, size_t alignment = max_align);
```

*Effects:* Equivalent to: `do_deallocate(p, bytes, alignment);`

``` cpp
bool is_equal(const memory_resource& other) const noexcept;
```

*Effects:* Equivalent to: `return do_is_equal(other);`

#### `memory_resource` private virtual member functions <a id="mem.res.private">[[mem.res.private]]</a>

``` cpp
virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
```

*Requires:* `alignment` shall be a power of two.

*Returns:* A derived class shall implement this function to return a
pointer to allocated storage ([[basic.stc.dynamic.deallocation]]) with
a size of at least `bytes`. The returned storage is aligned to the
specified alignment, if such alignment is supported ([[basic.align]]);
otherwise it is aligned to `max_align`.

*Throws:* A derived class implementation shall throw an appropriate
exception if it is unable to allocate memory with the requested size and
alignment.

``` cpp
virtual void do_deallocate(void* p, size_t bytes, size_t alignment) = 0;
```

*Requires:* `p` shall have been returned from a prior call to
`allocate(bytes, alignment)` on a memory resource equal to `*this`, and
the storage at `p` shall not yet have been deallocated.

*Effects:* A derived class shall implement this function to dispose of
allocated storage.

*Throws:* Nothing.

``` cpp
virtual bool do_is_equal(const memory_resource& other) const noexcept = 0;
```

*Returns:* A derived class shall implement this function to return
`true` if memory allocated from `this` can be deallocated from `other`
and vice-versa, otherwise `false`.

[*Note 1*: The most-derived type of `other` might not match the type of
`this`. For a derived class `D`, a typical implementation of this
function will immediately return `false` if
`dynamic_cast<const D*>(&other) == nullptr`. — *end note*]

#### `memory_resource` equality <a id="mem.res.eq">[[mem.res.eq]]</a>

``` cpp
bool operator==(const memory_resource& a, const memory_resource& b) noexcept;
```

*Returns:* `&a == &b || a.is_equal(b)`.

``` cpp
bool operator!=(const memory_resource& a, const memory_resource& b) noexcept;
```

*Returns:* `!(a == b)`.

### Class template `polymorphic_allocator` <a id="mem.poly.allocator.class">[[mem.poly.allocator.class]]</a>

A specialization of class template `pmr::polymorphic_allocator` conforms
to the `Allocator` requirements ([[allocator.requirements]]).
Constructed with different memory resources, different instances of the
same specialization of `pmr::polymorphic_allocator` can exhibit entirely
different allocation behavior. This runtime polymorphism allows objects
that use `polymorphic_allocator` to behave as if they used different
allocator types at run time even though they use the same static
allocator type.

``` cpp
template <class Tp>
class polymorphic_allocator {
  memory_resource* memory_rsrc; // exposition only

public:
  using value_type = Tp;

  // [mem.poly.allocator.ctor], constructors
  polymorphic_allocator() noexcept;
  polymorphic_allocator(memory_resource* r);

  polymorphic_allocator(const polymorphic_allocator& other) = default;

  template <class U>
    polymorphic_allocator(const polymorphic_allocator<U>& other) noexcept;

  polymorphic_allocator&
    operator=(const polymorphic_allocator& rhs) = delete;

  // [mem.poly.allocator.mem], member functions
  Tp* allocate(size_t n);
  void deallocate(Tp* p, size_t n);

  template <class T, class... Args>
  void construct(T* p, Args&&... args);

  template <class T1, class T2, class... Args1, class... Args2>
    void construct(pair<T1,T2>* p, piecewise_construct_t,
                   tuple<Args1...> x, tuple<Args2...> y);
  template <class T1, class T2>
    void construct(pair<T1,T2>* p);
  template <class T1, class T2, class U, class V>
    void construct(pair<T1,T2>* p, U&& x, V&& y);
  template <class T1, class T2, class U, class V>
    void construct(pair<T1,T2>* p, const pair<U, V>& pr);
  template <class T1, class T2, class U, class V>
    void construct(pair<T1,T2>* p, pair<U, V>&& pr);

  template <class T>
    void destroy(T* p);

  polymorphic_allocator select_on_container_copy_construction() const;

  memory_resource* resource() const;
};
```

#### `polymorphic_allocator` constructors <a id="mem.poly.allocator.ctor">[[mem.poly.allocator.ctor]]</a>

``` cpp
polymorphic_allocator() noexcept;
```

*Effects:* Sets `memory_rsrc` to `get_default_resource()`.

``` cpp
polymorphic_allocator(memory_resource* r);
```

*Requires:* `r` is non-null.

*Effects:* Sets `memory_rsrc` to `r`.

*Throws:* Nothing.

[*Note 1*: This constructor provides an implicit conversion from
`memory_resource*`. — *end note*]

``` cpp
template <class U>
  polymorphic_allocator(const polymorphic_allocator<U>& other) noexcept;
```

*Effects:* Sets `memory_rsrc` to `other.resource()`.

#### `polymorphic_allocator` member functions <a id="mem.poly.allocator.mem">[[mem.poly.allocator.mem]]</a>

``` cpp
Tp* allocate(size_t n);
```

*Returns:* Equivalent to

``` cpp
return static_cast<Tp*>(memory_rsrc->allocate(n * sizeof(Tp), alignof(Tp)));
```

``` cpp
void deallocate(Tp* p, size_t n);
```

*Requires:* `p` was allocated from a memory resource `x`, equal to
`*memory_rsrc`, using `x.allocate(n * sizeof(Tp), alignof(Tp))`.

*Effects:* Equivalent to
`memory_rsrc->deallocate(p, n * sizeof(Tp), alignof(Tp))`.

*Throws:* Nothing.

``` cpp
template <class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Requires:* Uses-allocator construction of `T` with allocator
`resource()` (see  [[allocator.uses.construction]]) and constructor
arguments `std::forward<Args>(args)...` is well-formed.

[*Note 1*: Uses-allocator construction is always well formed for types
that do not use allocators. — *end note*]

*Effects:* Construct a `T` object in the storage whose address is
represented by `p` by uses-allocator construction with allocator
`resource()` and constructor arguments `std::forward<Args>(args)...`.

*Throws:* Nothing unless the constructor for `T` throws.

``` cpp
template <class T1, class T2, class... Args1, class... Args2>
  void construct(pair<T1,T2>* p, piecewise_construct_t,
                 tuple<Args1...> x, tuple<Args2...> y);
```

[*Note 2*: This method and the `construct` methods that follow are
overloads for piecewise construction of
pairs ([[pairs.pair]]). — *end note*]

*Effects:* Let `xprime` be a `tuple` constructed from `x` according to
the appropriate rule from the following list.

[*Note 3*: The following description can be summarized as constructing
a `pair<T1, T2>` object in the storage whose address is represented by
`p`, as if by separate uses-allocator construction with allocator
`resource()` ([[allocator.uses.construction]]) of `p->first` using the
elements of `x` and `p->second` using the elements of
`y`. — *end note*]

- If `uses_allocator_v<T1,memory_resource*>` is `false`  
  and `is_constructible_v<T1,Args1...>` is `true`,  
  then `xprime` is `x`.
- Otherwise, if `uses_allocator_v<T1,memory_resource*>` is `true`  
  and `is_constructible_v<T1,allocator_arg_t,memory_resource*,Args1...>`
  is `true`,  
  then `xprime` is
  `tuple_cat(make_tuple(allocator_arg, resource()), std::move(x))`.
- Otherwise, if `uses_allocator_v<T1,memory_resource*>` is `true`  
  and `is_constructible_v<T1,Args1...,memory_resource*>` is `true`,  
  then `xprime` is `tuple_cat(std::move(x), make_tuple(resource()))`.
- Otherwise the program is ill formed.

Let `yprime` be a tuple constructed from `y` according to the
appropriate rule from the following list:

- If `uses_allocator_v<T2,memory_resource*>` is `false`  
  and `is_constructible_v<T2,Args2...>` is `true`,  
  then `yprime` is `y`.
- Otherwise, if `uses_allocator_v<T2,memory_resource*>` is `true`  
  and `is_constructible_v<T2,allocator_arg_t,memory_resource*,Args2...>`
  is `true`,  
  then `yprime` is
  `tuple_cat(make_tuple(allocator_arg, resource()), std::move(y))`.
- Otherwise, if `uses_allocator_v<T2,memory_resource*>` is `true`  
  and `is_constructible_v<T2,Args2...,memory_resource*>` is `true`,  
  then `yprime` is `tuple_cat(std::move(y), make_tuple(resource()))`.
- Otherwise the program is ill formed.

Then, using `piecewise_construct`, `xprime`, and `yprime` as the
constructor arguments, this function constructs a `pair<T1, T2>` object
in the storage whose address is represented by `p`.

``` cpp
template <class T1, class T2>
  void construct(pair<T1,T2>* p);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct, tuple<>(), tuple<>());
```

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1,T2>* p, U&& x, V&& y);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct,
          forward_as_tuple(std::forward<U>(x)),
          forward_as_tuple(std::forward<V>(y)));
```

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1,T2>* p, const pair<U, V>& pr);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct,
          forward_as_tuple(pr.first),
          forward_as_tuple(pr.second));
```

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1,T2>* p, pair<U, V>&& pr);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct,
          forward_as_tuple(std::forward<U>(pr.first)),
          forward_as_tuple(std::forward<V>(pr.second)));
```

``` cpp
template <class T>
  void destroy(T* p);
```

*Effects:* As if by `p->T̃()`.

``` cpp
polymorphic_allocator select_on_container_copy_construction() const;
```

*Returns:* `polymorphic_allocator()`.

[*Note 4*: The memory resource is not propagated. — *end note*]

``` cpp
memory_resource* resource() const;
```

*Returns:* `memory_rsrc`.

#### `polymorphic_allocator` equality <a id="mem.poly.allocator.eq">[[mem.poly.allocator.eq]]</a>

``` cpp
template <class T1, class T2>
  bool operator==(const polymorphic_allocator<T1>& a,
                  const polymorphic_allocator<T2>& b) noexcept;
```

*Returns:* `*a.resource() == *b.resource()`.

``` cpp
template <class T1, class T2>
  bool operator!=(const polymorphic_allocator<T1>& a,
                  const polymorphic_allocator<T2>& b) noexcept;
```

*Returns:* `!(a == b)`.

### Access to program-wide `memory_resource` objects <a id="mem.res.global">[[mem.res.global]]</a>

``` cpp
memory_resource* new_delete_resource() noexcept;
```

*Returns:* A pointer to a static-duration object of a type derived from
`memory_resource` that can serve as a resource for allocating memory
using `::operator new` and `::operator delete`. The same value is
returned every time this function is called. For a return value `p` and
a memory resource `r`, `p->is_equal(r)` returns `&r == p`.

``` cpp
memory_resource* null_memory_resource() noexcept;
```

*Returns:* A pointer to a static-duration object of a type derived from
`memory_resource` for which `allocate()` always throws `bad_alloc` and
for which `deallocate()` has no effect. The same value is returned every
time this function is called. For a return value `p` and a memory
resource `r`, `p->is_equal(r)` returns `&r == p`.

The *default memory resource pointer* is a pointer to a memory resource
that is used by certain facilities when an explicit memory resource is
not supplied through the interface. Its initial value is the return
value of `new_delete_resource()`.

``` cpp
memory_resource* set_default_resource(memory_resource* r) noexcept;
```

*Effects:* If `r` is non-null, sets the value of the default memory
resource pointer to `r`, otherwise sets the default memory resource
pointer to `new_delete_resource()`.

*Postconditions:* `get_default_resource() == r`.

*Returns:* The previous value of the default memory resource pointer.

*Remarks:* Calling the `set_default_resource` and `get_default_resource`
functions shall not incur a data race. A call to the
`set_default_resource` function shall synchronize with subsequent calls
to the `set_default_resource` and `get_default_resource` functions.

``` cpp
memory_resource* get_default_resource() noexcept;
```

*Returns:* The current value of the default memory resource pointer.

### Pool resource classes <a id="mem.res.pool">[[mem.res.pool]]</a>

#### Classes `synchronized_pool_resource` and `unsynchronized_pool_resource` <a id="mem.res.pool.overview">[[mem.res.pool.overview]]</a>

The `synchronized_pool_resource` and `unsynchronized_pool_resource`
classes (collectively called *pool resource classes*) are
general-purpose memory resources having the following qualities:

- Each resource frees its allocated memory on destruction, even if
  `deallocate` has not been called for some of the allocated blocks.
- A pool resource consists of a collection of *pools*, serving requests
  for different block sizes. Each individual pool manages a collection
  of *chunks* that are in turn divided into blocks of uniform size,
  returned via calls to `do_allocate`. Each call to
  `do_allocate(size, alignment)` is dispatched to the pool serving the
  smallest blocks accommodating at least `size` bytes.
- When a particular pool is exhausted, allocating a block from that pool
  results in the allocation of an additional chunk of memory from the
  *upstream allocator* (supplied at construction), thus replenishing the
  pool. With each successive replenishment, the chunk size obtained
  increases geometrically. \[*Note 2*: By allocating memory in chunks,
  the pooling strategy increases the chance that consecutive allocations
  will be close together in memory. — *end note*]
- Allocation requests that exceed the largest block size of any pool are
  fulfilled directly from the upstream allocator.
- A `pool_options` struct may be passed to the pool resource
  constructors to tune the largest block size and the maximum chunk
  size.

A `synchronized_pool_resource` may be accessed from multiple threads
without external synchronization and may have thread-specific pools to
reduce synchronization costs. An `unsynchronized_pool_resource` class
may not be accessed from multiple threads simultaneously and thus avoids
the cost of synchronization entirely in single-threaded applications.

``` cpp
struct pool_options {
  size_t max_blocks_per_chunk = 0;
  size_t largest_required_pool_block = 0;
};

class synchronized_pool_resource : public memory_resource {
public:
  synchronized_pool_resource(const pool_options& opts,
                             memory_resource* upstream);

  synchronized_pool_resource()
      : synchronized_pool_resource(pool_options(), get_default_resource()) {}
  explicit synchronized_pool_resource(memory_resource* upstream)
      : synchronized_pool_resource(pool_options(), upstream) {}
  explicit synchronized_pool_resource(const pool_options& opts)
      : synchronized_pool_resource(opts, get_default_resource()) {}

  synchronized_pool_resource(const synchronized_pool_resource&) = delete;
  virtual ~synchronized_pool_resource();

  synchronized_pool_resource&
    operator=(const synchronized_pool_resource&) = delete;

  void release();
  memory_resource* upstream_resource() const;
  pool_options options() const;

protected:
  void *do_allocate(size_t bytes, size_t alignment) override;
  void do_deallocate(void *p, size_t bytes, size_t alignment) override;

  bool do_is_equal(const memory_resource& other) const noexcept override;
};

class unsynchronized_pool_resource : public memory_resource {
public:
  unsynchronized_pool_resource(const pool_options& opts,
                               memory_resource* upstream);

  unsynchronized_pool_resource()
      : unsynchronized_pool_resource(pool_options(), get_default_resource()) {}
  explicit unsynchronized_pool_resource(memory_resource* upstream)
      : unsynchronized_pool_resource(pool_options(), upstream) {}
  explicit unsynchronized_pool_resource(const pool_options& opts)
      : unsynchronized_pool_resource(opts, get_default_resource()) {}

  unsynchronized_pool_resource(const unsynchronized_pool_resource&) = delete;
  virtual ~unsynchronized_pool_resource();

  unsynchronized_pool_resource&
    operator=(const unsynchronized_pool_resource&) = delete;

  void release();
  memory_resource *upstream_resource() const;
  pool_options options() const;

protected:
  void* do_allocate(size_t bytes, size_t alignment) override;
  void do_deallocate(void* p, size_t bytes, size_t alignment) override;

  bool do_is_equal(const memory_resource& other) const noexcept override;
};
```

#### `pool_options` data members <a id="mem.res.pool.options">[[mem.res.pool.options]]</a>

The members of `pool_options` comprise a set of constructor options for
pool resources. The effect of each option on the pool resource behavior
is described below:

``` cpp
size_t max_blocks_per_chunk;
```

The maximum number of blocks that will be allocated at once from the
upstream memory resource ([[mem.res.monotonic.buffer]]) to replenish a
pool. If the value of `max_blocks_per_chunk` is zero or is greater than
an *implementation-defined* limit, that limit is used instead. The
implementation may choose to use a smaller value than is specified in
this field and may use different values for different pools.

``` cpp
size_t largest_required_pool_block;
```

The largest allocation size that is required to be fulfilled using the
pooling mechanism. Attempts to allocate a single block larger than this
threshold will be allocated directly from the upstream memory resource.
If `largest_required_pool_block` is zero or is greater than an
*implementation-defined* limit, that limit is used instead. The
implementation may choose a pass-through threshold larger than specified
in this field.

#### Pool resource constructors and destructors <a id="mem.res.pool.ctor">[[mem.res.pool.ctor]]</a>

``` cpp
synchronized_pool_resource(const pool_options& opts, memory_resource* upstream);
unsynchronized_pool_resource(const pool_options& opts, memory_resource* upstream);
```

*Requires:* `upstream` is the address of a valid memory resource.

*Effects:* Constructs a pool resource object that will obtain memory
from `upstream` whenever the pool resource is unable to satisfy a memory
request from its own internal data structures. The resulting object will
hold a copy of `upstream`, but will not own the resource to which
`upstream` points.

[*Note 1*: The intention is that calls to `upstream->allocate()` will
be substantially fewer than calls to `this->allocate()` in most
cases. — *end note*]

The behavior of the pooling mechanism is tuned according to the value of
the `opts` argument.

*Throws:* Nothing unless `upstream->allocate()` throws. It is
unspecified if, or under what conditions, this constructor calls
`upstream->allocate()`.

``` cpp
virtual ~synchronized_pool_resource();
virtual ~unsynchronized_pool_resource();
```

*Effects:* Calls `release()`.

#### Pool resource members <a id="mem.res.pool.mem">[[mem.res.pool.mem]]</a>

``` cpp
void release();
```

*Effects:* Calls `upstream_resource()->deallocate()` as necessary to
release all allocated memory.

[*Note 1*: The memory is released back to `upstream_resource()` even if
`deallocate` has not been called for some of the allocated
blocks. — *end note*]

``` cpp
memory_resource* upstream_resource() const;
```

*Returns:* The value of the `upstream` argument provided to the
constructor of this object.

``` cpp
pool_options options() const;
```

*Returns:* The options that control the pooling behavior of this
resource. The values in the returned struct may differ from those
supplied to the pool resource constructor in that values of zero will be
replaced with *implementation-defined* defaults, and sizes may be
rounded to unspecified granularity.

``` cpp
void* do_allocate(size_t bytes, size_t alignment) override;
```

*Returns:* A pointer to allocated storage
([[basic.stc.dynamic.deallocation]]) with a size of at least `bytes`.
The size and alignment of the allocated memory shall meet the
requirements for a class derived from `memory_resource` ([[mem.res]]).

*Effects:* If the pool selected for a block of size `bytes` is unable to
satisfy the memory request from its own internal data structures, it
will call `upstream_resource()->allocate()` to obtain more memory. If
`bytes` is larger than that which the largest pool can handle, then
memory will be allocated using `upstream_resource()->allocate()`.

*Throws:* Nothing unless `upstream_resource()->allocate()` throws.

``` cpp
void do_deallocate(void* p, size_t bytes, size_t alignment) override;
```

*Effects:* Returns the memory at `p` to the pool. It is unspecified if,
or under what circumstances, this operation will result in a call to
`upstream_resource()->deallocate()`.

*Throws:* Nothing.

``` cpp
bool synchronized_pool_resource::do_is_equal(
    const memory_resource& other) const noexcept override;
```

*Returns:*
`this == dynamic_cast<const synchronized_pool_resource*>(&other)`.

``` cpp
bool unsynchronized_pool_resource::do_is_equal(
    const memory_resource& other) const noexcept override;
```

*Returns:*
`this == dynamic_cast<const unsynchronized_pool_resource*>(&other)`.

### Class `monotonic_buffer_resource` <a id="mem.res.monotonic.buffer">[[mem.res.monotonic.buffer]]</a>

A `monotonic_buffer_resource` is a special-purpose memory resource
intended for very fast memory allocations in situations where memory is
used to build up a few objects and then is released all at once when the
memory resource object is destroyed. It has the following qualities:

- A call to `deallocate` has no effect, thus the amount of memory
  consumed increases monotonically until the resource is destroyed.
- The program can supply an initial buffer, which the allocator uses to
  satisfy memory requests.
- When the initial buffer (if any) is exhausted, it obtains additional
  buffers from an *upstream* memory resource supplied at construction.
  Each additional buffer is larger than the previous one, following a
  geometric progression.
- It is intended for access from one thread of control at a time.
  Specifically, calls to `allocate` and `deallocate` do not synchronize
  with one another.
- It frees the allocated memory on destruction, even if `deallocate` has
  not been called for some of the allocated blocks.

``` cpp
class monotonic_buffer_resource : public memory_resource {
  memory_resource *upstream_rsrc; // exposition only
  void *current_buffer;           // exposition only
  size_t next_buffer_size;        // exposition only

public:
  explicit monotonic_buffer_resource(memory_resource *upstream);
  monotonic_buffer_resource(size_t initial_size, memory_resource *upstream);
  monotonic_buffer_resource(void *buffer, size_t buffer_size,
                            memory_resource *upstream);

  monotonic_buffer_resource()
      : monotonic_buffer_resource(get_default_resource()) {}
  explicit monotonic_buffer_resource(size_t initial_size)
      : monotonic_buffer_resource(initial_size, get_default_resource()) {}
  monotonic_buffer_resource(void *buffer, size_t buffer_size)
      : monotonic_buffer_resource(buffer, buffer_size, get_default_resource()) {}

  monotonic_buffer_resource(const monotonic_buffer_resource&) = delete;

  virtual ~monotonic_buffer_resource();

  monotonic_buffer_resource
    operator=(const monotonic_buffer_resource&) = delete;

  void release();
  memory_resource* upstream_resource() const;

protected:
  void* do_allocate(size_t bytes, size_t alignment) override;
  void do_deallocate(void* p, size_t bytes, size_t alignment) override;

  bool do_is_equal(const memory_resource& other) const noexcept override;
};
```

#### `monotonic_buffer_resource` constructor and destructor <a id="mem.res.monotonic.buffer.ctor">[[mem.res.monotonic.buffer.ctor]]</a>

``` cpp
explicit monotonic_buffer_resource(memory_resource* upstream);
monotonic_buffer_resource(size_t initial_size, memory_resource* upstream);
```

*Requires:* `upstream` shall be the address of a valid memory resource.
`initial_size`, if specified, shall be greater than zero.

*Effects:* Sets `upstream_rsrc` to `upstream` and `current_buffer` to
`nullptr`. If `initial_size` is specified, sets `next_buffer_size` to at
least `initial_size`; otherwise sets `next_buffer_size` to an
*implementation-defined* size.

``` cpp
monotonic_buffer_resource(void* buffer, size_t buffer_size, memory_resource* upstream);
```

*Requires:* `upstream` shall be the address of a valid memory resource.
`buffer_size` shall be no larger than the number of bytes in `buffer`.

*Effects:* Sets `upstream_rsrc` to `upstream`, `current_buffer` to
`buffer`, and `next_buffer_size` to `buffer_size` (but not less than 1),
then increases `next_buffer_size` by an *implementation-defined* growth
factor (which need not be integral).

``` cpp
~monotonic_buffer_resource();
```

*Effects:* Calls `release()`.

#### `monotonic_buffer_resource` members <a id="mem.res.monotonic.buffer.mem">[[mem.res.monotonic.buffer.mem]]</a>

``` cpp
void release();
```

*Effects:* Calls `upstream_rsrc->deallocate()` as necessary to release
all allocated memory.

[*Note 1*: The memory is released back to `upstream_rsrc` even if some
blocks that were allocated from `this` have not been deallocated from
`this`. — *end note*]

``` cpp
memory_resource* upstream_resource() const;
```

*Returns:* The value of `upstream_rsrc`.

``` cpp
void* do_allocate(size_t bytes, size_t alignment) override;
```

*Returns:* A pointer to allocated storage
([[basic.stc.dynamic.deallocation]]) with a size of at least `bytes`.
The size and alignment of the allocated memory shall meet the
requirements for a class derived from `memory_resource` ([[mem.res]]).

*Effects:* If the unused space in `current_buffer` can fit a block with
the specified `bytes` and `alignment`, then allocate the return block
from `current_buffer`; otherwise set `current_buffer` to
`upstream_rsrc->allocate(n, m)`, where `n` is not less than
`max(bytes, next_buffer_size)` and `m` is not less than `alignment`, and
increase `next_buffer_size` by an *implementation-defined* growth factor
(which need not be integral), then allocate the return block from the
newly-allocated `current_buffer`.

*Throws:* Nothing unless `upstream_rsrc->allocate()` throws.

``` cpp
void do_deallocate(void* p, size_t bytes, size_t alignment) override;
```

*Effects:* None.

*Throws:* Nothing.

*Remarks:* Memory used by this resource increases monotonically until
its destruction.

``` cpp
bool do_is_equal(const memory_resource& other) const noexcept override;
```

*Returns:*
`this == dynamic_cast<const monotonic_buffer_resource*>(&other)`.

## Class template `scoped_allocator_adaptor` <a id="allocator.adaptor">[[allocator.adaptor]]</a>

### Header `<scoped_allocator>` synopsis <a id="allocator.adaptor.syn">[[allocator.adaptor.syn]]</a>

``` cpp
// scoped allocator adaptor
  template <class OuterAlloc, class... InnerAlloc>
    class scoped_allocator_adaptor;
  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator!=(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

The class template `scoped_allocator_adaptor` is an allocator template
that specifies the memory resource (the outer allocator) to be used by a
container (as any other allocator does) and also specifies an inner
allocator resource to be passed to the constructor of every element
within the container. This adaptor is instantiated with one outer and
zero or more inner allocator types. If instantiated with only one
allocator type, the inner allocator becomes the
`scoped_allocator_adaptor` itself, thus using the same allocator
resource for the container and every element within the container and,
if the elements themselves are containers, each of their elements
recursively. If instantiated with more than one allocator, the first
allocator is the outer allocator for use by the container, the second
allocator is passed to the constructors of the container’s elements,
and, if the elements themselves are containers, the third allocator is
passed to the elements’ elements, and so on. If containers are nested to
a depth greater than the number of allocators, the last allocator is
used repeatedly, as in the single-allocator case, for any remaining
recursions.

[*Note 1*: The `scoped_allocator_adaptor` is derived from the outer
allocator type so it can be substituted for the outer allocator type in
most expressions. — *end note*]

``` cpp
namespace std {
  template <class OuterAlloc, class... InnerAllocs>
    class scoped_allocator_adaptor : public OuterAlloc {
  private:
    using OuterTraits = allocator_traits<OuterAlloc>; // exposition only
    scoped_allocator_adaptor<InnerAllocs...> inner;   // exposition only
  public:
    using outer_allocator_type = OuterAlloc;
    using inner_allocator_type = see below;

    using value_type           = typename OuterTraits::value_type;
    using size_type            = typename OuterTraits::size_type;
    using difference_type      = typename OuterTraits::difference_type;
    using pointer              = typename OuterTraits::pointer;
    using const_pointer        = typename OuterTraits::const_pointer;
    using void_pointer         = typename OuterTraits::void_pointer;
    using const_void_pointer   = typename OuterTraits::const_void_pointer;

    using propagate_on_container_copy_assignment = see below;
    using propagate_on_container_move_assignment = see below;
    using propagate_on_container_swap            = see below;
    using is_always_equal                        = see below;

    template <class Tp>
      struct rebind {
        using other = scoped_allocator_adaptor<
          OuterTraits::template rebind_alloc<Tp>, InnerAllocs...>;
      };

    scoped_allocator_adaptor();
    template <class OuterA2>
      scoped_allocator_adaptor(OuterA2&& outerAlloc,
                               const InnerAllocs&... innerAllocs) noexcept;

    scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
    scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;

    template <class OuterA2>
      scoped_allocator_adaptor(
        const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& other) noexcept;
    template <class OuterA2>
      scoped_allocator_adaptor(
        scoped_allocator_adaptor<OuterA2, InnerAllocs...>&& other) noexcept;

    scoped_allocator_adaptor& operator=(const scoped_allocator_adaptor&) = default;
    scoped_allocator_adaptor& operator=(scoped_allocator_adaptor&&) = default;

    ~scoped_allocator_adaptor();

    inner_allocator_type& inner_allocator() noexcept;
    const inner_allocator_type& inner_allocator() const noexcept;
    outer_allocator_type& outer_allocator() noexcept;
    const outer_allocator_type& outer_allocator() const noexcept;

    pointer allocate(size_type n);
    pointer allocate(size_type n, const_void_pointer hint);
    void deallocate(pointer p, size_type n);
    size_type max_size() const;

    template <class T, class... Args>
      void construct(T* p, Args&&... args);
    template <class T1, class T2, class... Args1, class... Args2>
      void construct(pair<T1, T2>* p, piecewise_construct_t,
                     tuple<Args1...> x, tuple<Args2...> y);
    template <class T1, class T2>
      void construct(pair<T1, T2>* p);
    template <class T1, class T2, class U, class V>
      void construct(pair<T1, T2>* p, U&& x, V&& y);
    template <class T1, class T2, class U, class V>
      void construct(pair<T1, T2>* p, const pair<U, V>& x);
    template <class T1, class T2, class U, class V>
      void construct(pair<T1, T2>* p, pair<U, V>&& x);

    template <class T>
      void destroy(T* p);

    scoped_allocator_adaptor select_on_container_copy_construction() const;
  };

  template<class OuterAlloc, class... InnerAllocs>
    scoped_allocator_adaptor(OuterAlloc, InnerAllocs...)
      -> scoped_allocator_adaptor<OuterAlloc, InnerAllocs...>;

  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
  template <class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator!=(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
}
```

### Scoped allocator adaptor member types <a id="allocator.adaptor.types">[[allocator.adaptor.types]]</a>

``` cpp
using inner_allocator_type = see below;
```

*Type:* `scoped_allocator_adaptor<OuterAlloc>` if
`sizeof...(InnerAllocs)` is zero; otherwise,  
`scoped_allocator_adaptor<InnerAllocs...>`.

``` cpp
using propagate_on_container_copy_assignment = see below;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_copy_assignment::value` is
`true` for any `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

``` cpp
using propagate_on_container_move_assignment = see below;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_move_assignment::value` is
`true` for any `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

``` cpp
using propagate_on_container_swap = see below;
```

*Type:* `true_type` if
`allocator_traits<A>::propagate_on_container_swap::value` is `true` for
any `A` in the set of `OuterAlloc` and `InnerAllocs...`; otherwise,
`false_type`.

``` cpp
using is_always_equal = see below;
```

*Type:* `true_type` if `allocator_traits<A>::is_always_equal::value` is
`true` for every `A` in the set of `OuterAlloc` and `InnerAllocs...`;
otherwise, `false_type`.

### Scoped allocator adaptor constructors <a id="allocator.adaptor.cnstr">[[allocator.adaptor.cnstr]]</a>

``` cpp
scoped_allocator_adaptor();
```

*Effects:* Value-initializes the `OuterAlloc` base class and the `inner`
allocator object.

``` cpp
template <class OuterA2>
  scoped_allocator_adaptor(OuterA2&& outerAlloc,
                           const InnerAllocs&... innerAllocs) noexcept;
```

*Effects:* Initializes the `OuterAlloc` base class with
`std::forward<OuterA2>(outerAlloc)` and `inner` with `innerAllocs...`
(hence recursively initializing each allocator within the adaptor with
the corresponding allocator from the argument list).

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<OuterAlloc, OuterA2>` is `true`.

``` cpp
scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
```

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;
```

*Effects:* Move constructs each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
template <class OuterA2>
  scoped_allocator_adaptor(const scoped_allocator_adaptor<OuterA2,
                                                          InnerAllocs...>& other) noexcept;
```

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator from `other`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<OuterAlloc, const OuterA2&>` is `true`.

``` cpp
template <class OuterA2>
  scoped_allocator_adaptor(scoped_allocator_adaptor<OuterA2,
                                                    InnerAllocs...>&& other) noexcept;
```

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator rvalue from `other`.

*Remarks:* This constructor shall not participate in overload resolution
unless `is_constructible_v<OuterAlloc, OuterA2>` is `true`.

### Scoped allocator adaptor members <a id="allocator.adaptor.members">[[allocator.adaptor.members]]</a>

In the `construct` member functions, `OUTERMOST(x)` is `x` if `x` does
not have an `outer_allocator()` member function and
`OUTERMOST(x.outer_allocator())` otherwise; `OUTERMOST_ALLOC_TRAITS(x)`
is `allocator_traits<decltype(OUTERMOST(x))>`.

[*Note 1*: `OUTERMOST(x)` and `OUTERMOST_ALLOC_TRAITS(x)` are recursive
operations. It is incumbent upon the definition of `outer_allocator()`
to ensure that the recursion terminates. It will terminate for all
instantiations of `scoped_allocator_adaptor`. — *end note*]

``` cpp
inner_allocator_type& inner_allocator() noexcept;
const inner_allocator_type& inner_allocator() const noexcept;
```

*Returns:* `*this` if `sizeof...(InnerAllocs)` is zero; otherwise,
`inner`.

``` cpp
outer_allocator_type& outer_allocator() noexcept;
```

*Returns:* `static_cast<OuterAlloc&>(*this)`.

``` cpp
const outer_allocator_type& outer_allocator() const noexcept;
```

*Returns:* `static_cast<const OuterAlloc&>(*this)`.

``` cpp
pointer allocate(size_type n);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n)`.

``` cpp
pointer allocate(size_type n, const_void_pointer hint);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n, hint)`.

``` cpp
void deallocate(pointer p, size_type n) noexcept;
```

*Effects:* As if by:
`allocator_traits<OuterAlloc>::deallocate(outer_allocator(), p, n);`

``` cpp
size_type max_size() const;
```

*Returns:* `allocator_traits<OuterAlloc>::max_size(outer_allocator())`.

``` cpp
template <class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Effects:*

- If `uses_allocator_v<T, inner_allocator_type>` is `false` and
  `is_constructible_v<T,`  
  `Args...>` is `true`, calls:
  ``` cpp
  OUTERMOST_ALLOC_TRAITS(*this)::construct(
      OUTERMOST(*this), p, std::forward<Args>(args)...)
  ```
- Otherwise, if `uses_allocator_v<T, inner_allocator_type>` is `true`
  and
  `is_constructible_v<T, allocator_arg_t, inner_allocator_type&, Args...>`
  is `true`, calls:
  ``` cpp
  OUTERMOST_ALLOC_TRAITS(*this)::construct(
      OUTERMOST(*this), p, allocator_arg, inner_allocator(), std::forward<Args>(args)...)
  ```
- Otherwise, if `uses_allocator_v<T, inner_allocator_type>` is `true`
  and `is_constructible_v<T, Args..., inner_allocator_type&>` is `true`,
  calls:
  ``` cpp
  OUTERMOST_ALLOC_TRAITS(*this)::construct(
      OUTERMOST(*this), p, std::forward<Args>(args)..., inner_allocator())
  ```
- Otherwise, the program is ill-formed. \[*Note 3*: An error will result
  if `uses_allocator` evaluates to `true` but the specific constructor
  does not take an allocator. This definition prevents a silent failure
  to pass an inner allocator to a contained element. — *end note*]

``` cpp
template <class T1, class T2, class... Args1, class... Args2>
  void construct(pair<T1, T2>* p, piecewise_construct_t,
                 tuple<Args1...> x, tuple<Args2...> y);
```

*Requires:* all of the types in `Args1` and `Args2` shall be
`CopyConstructible` (Table  [[tab:copyconstructible]]).

*Effects:* Constructs a `tuple` object `xprime` from `x` by the
following rules:

- If `uses_allocator_v<T1, inner_allocator_type>` is `false` and
  `is_constructible_v<T1,`  
  `Args1...>` is `true`, then `xprime` is `x`.
- Otherwise, if `uses_allocator_v<T1, inner_allocator_type>` is `true`
  and
  `is_constructible_v<T1, allocator_arg_t, inner_allocator_type&, Args1...>`
  is `true`, then `xprime` is:
  ``` cpp
  tuple_cat(
      tuple<allocator_arg_t, inner_allocator_type&>(allocator_arg, inner_allocator()),
      std::move(x))
  ```
- Otherwise, if `uses_allocator_v<T1, inner_allocator_type>` is `true`
  and `is_constructible_v<T1, Args1..., inner_allocator_type&>` is
  `true`, then `xprime` is:
  ``` cpp
  tuple_cat(std::move(x), tuple<inner_allocator_type&>(inner_allocator()))
  ```
- Otherwise, the program is ill-formed.

and constructs a `tuple` object `yprime` from `y` by the following
rules:

- If `uses_allocator_v<T2, inner_allocator_type>` is `false` and
  `is_constructible_v<T2,`  
  `Args2...>` is `true`, then `yprime` is `y`.
- Otherwise, if `uses_allocator_v<T2, inner_allocator_type>` is `true`
  and
  `is_constructible_v<T2, allocator_arg_t, inner_allocator_type&, Args2...>`
  is `true`, then `yprime` is:
  ``` cpp
  tuple_cat(
      tuple<allocator_arg_t, inner_allocator_type&>(allocator_arg, inner_allocator()),
      std::move(y))
  ```
- Otherwise, if `uses_allocator_v<T2, inner_allocator_type>` is `true`
  and `is_constructible_v<T2, Args2..., inner_allocator_type&>` is
  `true`, then `yprime` is:
  ``` cpp
  tuple_cat(std::move(y), tuple<inner_allocator_type&>(inner_allocator()))
  ```
- Otherwise, the program is ill-formed.

then calls:

``` cpp
OUTERMOST_ALLOC_TRAITS(*this)::construct(
    OUTERMOST(*this), p, piecewise_construct, std::move(xprime), std::move(yprime))
```

``` cpp
template <class T1, class T2>
  void construct(pair<T1, T2>* p);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct, tuple<>(), tuple<>());
```

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1, T2>* p, U&& x, V&& y);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct,
          forward_as_tuple(std::forward<U>(x)),
          forward_as_tuple(std::forward<V>(y)));
```

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1, T2>* p, const pair<U, V>& x);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct,
          forward_as_tuple(x.first),
          forward_as_tuple(x.second));
```

``` cpp
template <class T1, class T2, class U, class V>
  void construct(pair<T1, T2>* p, pair<U, V>&& x);
```

*Effects:* Equivalent to:

``` cpp
construct(p, piecewise_construct,
          forward_as_tuple(std::forward<U>(x.first)),
          forward_as_tuple(std::forward<V>(x.second)));
```

``` cpp
template <class T>
  void destroy(T* p);
```

*Effects:* Calls
*OUTERMOST_ALLOC_TRAITS*(\*this)::destroy(*OUTERMOST*(\*this), p).

``` cpp
scoped_allocator_adaptor select_on_container_copy_construction() const;
```

*Returns:* A new `scoped_allocator_adaptor` object where each allocator
`A` in the adaptor is initialized from the result of calling
`allocator_traits<A>::select_on_container_copy_construction()` on the
corresponding allocator in `*this`.

### Scoped allocator operators <a id="scoped.adaptor.operators">[[scoped.adaptor.operators]]</a>

``` cpp
template <class OuterA1, class OuterA2, class... InnerAllocs>
  bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                  const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

*Returns:* If `sizeof...(InnerAllocs)` is zero,

``` cpp
a.outer_allocator() == b.outer_allocator()
```

otherwise

``` cpp
a.outer_allocator() == b.outer_allocator() && a.inner_allocator() == b.inner_allocator()
```

``` cpp
template <class OuterA1, class OuterA2, class... InnerAllocs>
  bool operator!=(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                  const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
```

*Returns:* `!(a == b)`.

## Function objects <a id="function.objects">[[function.objects]]</a>

A *function object type* is an object type ([[basic.types]]) that can
be the type of the *postfix-expression* in a function call (
[[expr.call]],  [[over.match.call]]).[^2] A *function object* is an
object of a function object type. In the places where one would expect
to pass a pointer to a function to an algorithmic template (Clause 
[[algorithms]]), the interface is specified to accept a function object.
This not only makes algorithmic templates work with pointers to
functions, but also enables them to work with arbitrary function
objects.

### Header `<functional>` synopsis <a id="functional.syn">[[functional.syn]]</a>

``` cpp
namespace std {
  // [func.invoke], invoke
  template <class F, class... Args>
    invoke_result_t<F, Args...> invoke(F&& f, Args&&... args)
      noexcept(is_nothrow_invocable_v<F, Args...>);

  // [refwrap], reference_wrapper
  template <class T> class reference_wrapper;

  template <class T> reference_wrapper<T> ref(T&) noexcept;
  template <class T> reference_wrapper<const T> cref(const T&) noexcept;
  template <class T> void ref(const T&&) = delete;
  template <class T> void cref(const T&&) = delete;

  template <class T> reference_wrapper<T> ref(reference_wrapper<T>) noexcept;
  template <class T> reference_wrapper<const T> cref(reference_wrapper<T>) noexcept;

  // [arithmetic.operations], arithmetic operations
  template <class T = void> struct plus;
  template <class T = void> struct minus;
  template <class T = void> struct multiplies;
  template <class T = void> struct divides;
  template <class T = void> struct modulus;
  template <class T = void> struct negate;
  template <> struct plus<void>;
  template <> struct minus<void>;
  template <> struct multiplies<void>;
  template <> struct divides<void>;
  template <> struct modulus<void>;
  template <> struct negate<void>;

  // [comparisons], comparisons
  template <class T = void> struct equal_to;
  template <class T = void> struct not_equal_to;
  template <class T = void> struct greater;
  template <class T = void> struct less;
  template <class T = void> struct greater_equal;
  template <class T = void> struct less_equal;
  template <> struct equal_to<void>;
  template <> struct not_equal_to<void>;
  template <> struct greater<void>;
  template <> struct less<void>;
  template <> struct greater_equal<void>;
  template <> struct less_equal<void>;

  // [logical.operations], logical operations
  template <class T = void> struct logical_and;
  template <class T = void> struct logical_or;
  template <class T = void> struct logical_not;
  template <> struct logical_and<void>;
  template <> struct logical_or<void>;
  template <> struct logical_not<void>;

  // [bitwise.operations], bitwise operations
  template <class T = void> struct bit_and;
  template <class T = void> struct bit_or;
  template <class T = void> struct bit_xor;
  template <class T = void> struct bit_not;
  template <> struct bit_and<void>;
  template <> struct bit_or<void>;
  template <> struct bit_xor<void>;
  template <> struct bit_not<void>;

  // [func.not_fn], function template not_fn
  template <class F>
    unspecified not_fn(F&& f);

  // [func.bind], bind
  template<class T> struct is_bind_expression;
  template<class T> struct is_placeholder;

  template<class F, class... BoundArgs>
    unspecified bind(F&&, BoundArgs&&...);
  template<class R, class F, class... BoundArgs>
    unspecified bind(F&&, BoundArgs&&...);

  namespace placeholders {
    // M is the implementation-defined number of placeholders
    see belownc _1;
    see belownc _2;
               .
               .
               .
    see belownc _M;
  }

  // [func.memfn], member function adaptors
  template<class R, class T>
    unspecified mem_fn(R T::*) noexcept;

  // [func.wrap], polymorphic function wrappers
  class bad_function_call;

  template<class> class function; // not defined
  template<class R, class... ArgTypes> class function<R(ArgTypes...)>;

  template<class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&) noexcept;

  template<class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t) noexcept;
  template<class R, class... ArgTypes>
    bool operator==(nullptr_t, const function<R(ArgTypes...)>&) noexcept;
  template<class R, class... ArgTypes>
    bool operator!=(const function<R(ArgTypes...)>&, nullptr_t) noexcept;
  template<class R, class... ArgTypes>
    bool operator!=(nullptr_t, const function<R(ArgTypes...)>&) noexcept;

  // [func.search], searchers
  template<class ForwardIterator, class BinaryPredicate = equal_to<>>
    class default_searcher;

  template<class RandomAccessIterator,
           class Hash = hash<typename iterator_traits<RandomAccessIterator>::value_type>,
           class BinaryPredicate = equal_to<>>
    class boyer_moore_searcher;

  template<class RandomAccessIterator,
           class Hash = hash<typename iterator_traits<RandomAccessIterator>::value_type>,
           class BinaryPredicate = equal_to<>>
    class boyer_moore_horspool_searcher;

  // [unord.hash], hash function primary template
  template <class T>
    struct hash;

  // [func.bind], function object binders
  template <class T>
    inline constexpr bool is_bind_expression_v = is_bind_expression<T>::value;
  template <class T>
    inline constexpr int is_placeholder_v = is_placeholder<T>::value;
}
```

[*Example 1*:

If a C++program wants to have a by-element addition of two vectors `a`
and `b` containing `double` and put the result into `a`, it can do:

``` cpp
transform(a.begin(), a.end(), b.begin(), a.begin(), plus<double>());
```

— *end example*]

[*Example 2*:

To negate every element of `a`:

``` cpp
transform(a.begin(), a.end(), a.begin(), negate<double>());
```

— *end example*]

### Definitions <a id="func.def">[[func.def]]</a>

The following definitions apply to this Clause:

A *call signature* is the name of a return type followed by a
parenthesized comma-separated list of zero or more argument types.

A *callable type* is a function object type ([[function.objects]]) or a
pointer to member.

A *callable object* is an object of a callable type.

A *call wrapper type* is a type that holds a callable object and
supports a call operation that forwards to that object.

A *call wrapper* is an object of a call wrapper type.

A *target object* is the callable object held by a call wrapper.

### Requirements <a id="func.require">[[func.require]]</a>

Define `INVOKE(f, t1, t2, ..., tN)` as follows:

- `(t1.*f)(t2, ..., tN)` when `f` is a pointer to a member function of a
  class `T` and `is_base_of_v<T, decay_t<decltype(t1)>>` is `true`;
- `(t1.get().*f)(t2, ..., tN)` when `f` is a pointer to a member
  function of a class `T` and `decay_t<decltype(t1)>` is a
  specialization of `reference_wrapper`;
- `((*t1).*f)(t2, ..., tN)` when `f` is a pointer to a member function
  of a class `T` and `t1` does not satisfy the previous two items;
- `t1.*f` when `N == 1` and `f` is a pointer to data member of a class
  `T` and `is_base_of_v<T, decay_t<decltype(t1)>>` is `true`;
- `t1.get().*f` when `N == 1` and `f` is a pointer to data member of a
  class `T` and `decay_t<decltype(t1)>` is a specialization of
  `reference_wrapper`;
- `(*t1).*f` when `N == 1` and `f` is a pointer to data member of a
  class `T` and `t1` does not satisfy the previous two items;
- `f(t1, t2, ..., tN)` in all other cases.

Define `INVOKE<R>(f, t1, t2, ..., tN)` as
`static_cast<void>(INVOKE(f, t1, t2, ..., tN))` if `R` is cv `void`,
otherwise `INVOKE(f, t1, t2, ..., tN)` implicitly converted to `R`.

Every call wrapper ([[func.def]]) shall be `MoveConstructible`. A
*forwarding call wrapper* is a call wrapper that can be called with an
arbitrary argument list and delivers the arguments to the wrapped
callable object as references. This forwarding step shall ensure that
rvalue arguments are delivered as rvalue references and lvalue arguments
are delivered as lvalue references. A *simple call wrapper* is a
forwarding call wrapper that is `CopyConstructible` and `CopyAssignable`
and whose copy constructor, move constructor, and assignment operator do
not throw exceptions.

[*Note 1*:

In a typical implementation forwarding call wrappers have an overloaded
function call operator of the form

``` cpp
template<class... UnBoundArgs>
R operator()(UnBoundArgs&&... unbound_args) cv-qual;
```

— *end note*]

### Function template `invoke` <a id="func.invoke">[[func.invoke]]</a>

``` cpp
template <class F, class... Args>
  invoke_result_t<F, Args...> invoke(F&& f, Args&&... args)
    noexcept(is_nothrow_invocable_v<F, Args...>);
```

*Returns:* *INVOKE*(std::forward\<F\>(f),
std::forward\<Args\>(args)...) ([[func.require]]).

### Class template `reference_wrapper` <a id="refwrap">[[refwrap]]</a>

``` cpp
namespace std {
  template <class T> class reference_wrapper {
  public :
    // types
    using type = T;

    // construct/copy/destroy
    reference_wrapper(T&) noexcept;
    reference_wrapper(T&&) = delete;     // do not bind to temporary objects
    reference_wrapper(const reference_wrapper& x) noexcept;

    // assignment
    reference_wrapper& operator=(const reference_wrapper& x) noexcept;

    // access
    operator T& () const noexcept;
    T& get() const noexcept;

    // invocation
    template <class... ArgTypes>
      invoke_result_t<T&, ArgTypes...>
      operator() (ArgTypes&&...) const;
  };

  template<class T>
    reference_wrapper(reference_wrapper<T>) -> reference_wrapper<T>;
}
```

`reference_wrapper<T>` is a `CopyConstructible` and `CopyAssignable`
wrapper around a reference to an object or function of type `T`.

`reference_wrapper<T>` shall be a trivially copyable type (
[[basic.types]]).

#### `reference_wrapper` construct/copy/destroy <a id="refwrap.const">[[refwrap.const]]</a>

``` cpp
reference_wrapper(T& t) noexcept;
```

*Effects:* Constructs a `reference_wrapper` object that stores a
reference to `t`.

``` cpp
reference_wrapper(const reference_wrapper& x) noexcept;
```

*Effects:* Constructs a `reference_wrapper` object that stores a
reference to `x.get()`.

#### `reference_wrapper` assignment <a id="refwrap.assign">[[refwrap.assign]]</a>

``` cpp
reference_wrapper& operator=(const reference_wrapper& x) noexcept;
```

*Postconditions:* `*this` stores a reference to `x.get()`.

#### `reference_wrapper` access <a id="refwrap.access">[[refwrap.access]]</a>

``` cpp
operator T& () const noexcept;
```

*Returns:* The stored reference.

``` cpp
T& get() const noexcept;
```

*Returns:* The stored reference.

#### `reference_wrapper` invocation <a id="refwrap.invoke">[[refwrap.invoke]]</a>

``` cpp
template <class... ArgTypes>
  invoke_result_t<T&, ArgTypes...>
    operator()(ArgTypes&&... args) const;
```

*Returns:* *INVOKE*(get(),
std::forward\<ArgTypes\>(args)...). ([[func.require]])

#### `reference_wrapper` helper functions <a id="refwrap.helpers">[[refwrap.helpers]]</a>

``` cpp
template <class T> reference_wrapper<T> ref(T& t) noexcept;
```

*Returns:* `reference_wrapper<T>(t)`.

``` cpp
template <class T> reference_wrapper<T> ref(reference_wrapper<T> t) noexcept;
```

*Returns:* `ref(t.get())`.

``` cpp
template <class T> reference_wrapper<const T> cref(const T& t) noexcept;
```

*Returns:* `reference_wrapper <const T>(t)`.

``` cpp
template <class T> reference_wrapper<const T> cref(reference_wrapper<T> t) noexcept;
```

*Returns:* `cref(t.get())`.

### Arithmetic operations <a id="arithmetic.operations">[[arithmetic.operations]]</a>

The library provides basic function object classes for all of the
arithmetic operators in the language ([[expr.mul]], [[expr.add]]).

#### Class template `plus` <a id="arithmetic.operations.plus">[[arithmetic.operations.plus]]</a>

``` cpp
template <class T = void> struct plus {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x + y`.

``` cpp
template <> struct plus<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) + std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) + std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) + std::forward<U>(u)`.

#### Class template `minus` <a id="arithmetic.operations.minus">[[arithmetic.operations.minus]]</a>

``` cpp
template <class T = void> struct minus {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x - y`.

``` cpp
template <> struct minus<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) - std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) - std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) - std::forward<U>(u)`.

#### Class template `multiplies` <a id="arithmetic.operations.multiplies">[[arithmetic.operations.multiplies]]</a>

``` cpp
template <class T = void> struct multiplies {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x * y`.

``` cpp
template <> struct multiplies<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) * std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) * std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) * std::forward<U>(u)`.

#### Class template `divides` <a id="arithmetic.operations.divides">[[arithmetic.operations.divides]]</a>

``` cpp
template <class T = void> struct divides {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x / y`.

``` cpp
template <> struct divides<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) / std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) / std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) / std::forward<U>(u)`.

#### Class template `modulus` <a id="arithmetic.operations.modulus">[[arithmetic.operations.modulus]]</a>

``` cpp
template <class T = void> struct modulus {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x % y`.

``` cpp
template <> struct modulus<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) % std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) % std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) % std::forward<U>(u)`.

#### Class template `negate` <a id="arithmetic.operations.negate">[[arithmetic.operations.negate]]</a>

``` cpp
template <class T = void> struct negate {
  constexpr T operator()(const T& x) const;
};
```

``` cpp
constexpr T operator()(const T& x) const;
```

*Returns:* `-x`.

``` cpp
template <> struct negate<void> {
  template <class T> constexpr auto operator()(T&& t) const
    -> decltype(-std::forward<T>(t));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T> constexpr auto operator()(T&& t) const
    -> decltype(-std::forward<T>(t));
```

*Returns:* `-std::forward<T>(t)`.

### Comparisons <a id="comparisons">[[comparisons]]</a>

The library provides basic function object classes for all of the
comparison operators in the language ([[expr.rel]], [[expr.eq]]).

For templates `less`, `greater`, `less_equal`, and `greater_equal`, the
specializations for any pointer type yield a strict total order that is
consistent among those specializations and is also consistent with the
partial order imposed by the built-in operators `<`, `>`, `<=`, `>=`.

[*Note 1*: When `a < b` is well-defined for pointers `a` and `b` of
type `P`, this implies `(a < b) == less<P>(a, b)`,
`(a > b) == greater<P>(a, b)`, and so forth. — *end note*]

For template specializations `less<void>`, `greater<void>`,
`less_equal<void>`, and `greater_equal<void>`, if the call operator
calls a built-in operator comparing pointers, the call operator yields a
strict total order that is consistent among those specializations and is
also consistent with the partial order imposed by those built-in
operators.

#### Class template `equal_to` <a id="comparisons.equal_to">[[comparisons.equal_to]]</a>

``` cpp
template <class T = void> struct equal_to {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x == y`.

``` cpp
template <> struct equal_to<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) == std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) == std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) == std::forward<U>(u)`.

#### Class template `not_equal_to` <a id="comparisons.not_equal_to">[[comparisons.not_equal_to]]</a>

``` cpp
template <class T = void> struct not_equal_to {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x != y`.

``` cpp
template <> struct not_equal_to<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) != std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) != std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) != std::forward<U>(u)`.

#### Class template `greater` <a id="comparisons.greater">[[comparisons.greater]]</a>

``` cpp
template <class T = void> struct greater {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x > y`.

``` cpp
template <> struct greater<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) > std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) > std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) > std::forward<U>(u)`.

#### Class template `less` <a id="comparisons.less">[[comparisons.less]]</a>

``` cpp
template <class T = void> struct less {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x < y`.

``` cpp
template <> struct less<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) < std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) < std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) < std::forward<U>(u)`.

#### Class template `greater_equal` <a id="comparisons.greater_equal">[[comparisons.greater_equal]]</a>

``` cpp
template <class T = void> struct greater_equal {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x >= y`.

``` cpp
template <> struct greater_equal<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) >= std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) >= std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) >= std::forward<U>(u)`.

#### Class template `less_equal` <a id="comparisons.less_equal">[[comparisons.less_equal]]</a>

``` cpp
template <class T = void> struct less_equal {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x <= y`.

``` cpp
template <> struct less_equal<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) <= std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) <= std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) <= std::forward<U>(u)`.

### Logical operations <a id="logical.operations">[[logical.operations]]</a>

The library provides basic function object classes for all of the
logical operators in the language ([[expr.log.and]], [[expr.log.or]],
[[expr.unary.op]]).

#### Class template `logical_and` <a id="logical.operations.and">[[logical.operations.and]]</a>

``` cpp
template <class T = void> struct logical_and {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x && y`.

``` cpp
template <> struct logical_and<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) && std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) && std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) && std::forward<U>(u)`.

#### Class template `logical_or` <a id="logical.operations.or">[[logical.operations.or]]</a>

``` cpp
template <class T = void> struct logical_or {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x || y`.

``` cpp
template <> struct logical_or<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) || std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) || std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) || std::forward<U>(u)`.

#### Class template `logical_not` <a id="logical.operations.not">[[logical.operations.not]]</a>

``` cpp
template <class T = void> struct logical_not {
  constexpr bool operator()(const T& x) const;
};
```

``` cpp
constexpr bool operator()(const T& x) const;
```

*Returns:* `!x`.

``` cpp
template <> struct logical_not<void> {
  template <class T> constexpr auto operator()(T&& t) const
    -> decltype(!std::forward<T>(t));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T> constexpr auto operator()(T&& t) const
    -> decltype(!std::forward<T>(t));
```

*Returns:* `!std::forward<T>(t)`.

### Bitwise operations <a id="bitwise.operations">[[bitwise.operations]]</a>

The library provides basic function object classes for all of the
bitwise operators in the language ([[expr.bit.and]], [[expr.or]],
[[expr.xor]], [[expr.unary.op]]).

#### Class template `bit_and` <a id="bitwise.operations.and">[[bitwise.operations.and]]</a>

``` cpp
template <class T = void> struct bit_and {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x & y`.

``` cpp
template <> struct bit_and<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) & std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) & std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) & std::forward<U>(u)`.

#### Class template `bit_or` <a id="bitwise.operations.or">[[bitwise.operations.or]]</a>

``` cpp
template <class T = void> struct bit_or {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x | y`.

``` cpp
template <> struct bit_or<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) | std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) | std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) | std::forward<U>(u)`.

#### Class template `bit_xor` <a id="bitwise.operations.xor">[[bitwise.operations.xor]]</a>

``` cpp
template <class T = void> struct bit_xor {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x ^ y`.

``` cpp
template <> struct bit_xor<void> {
  template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) ^ std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) ^ std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) ^ std::forward<U>(u)`.

#### Class template `bit_not` <a id="bitwise.operations.not">[[bitwise.operations.not]]</a>

``` cpp
template <class T = void> struct bit_not {
  constexpr T operator()(const T& x) const;
};
```

``` cpp
constexpr T operator()(const T& x) const;
```

*Returns:* `~x`.

``` cpp
template <> struct bit_not<void> {
  template <class T> constexpr auto operator()(T&& t) const
    -> decltype(~std::forward<T>(t));

  using is_transparent = unspecified;
};
```

``` cpp
template <class T> constexpr auto operator()(T&&) const
    -> decltype(~std::forward<T>(t));
```

*Returns:* `~std::forward<T>(t)`.

### Function template `not_fn` <a id="func.not_fn">[[func.not_fn]]</a>

``` cpp
template <class F> unspecified not_fn(F&& f);
```

*Effects:* Equivalent to
`return `*`call_wrapper`*`(std::forward<F>(f));` where *`call_wrapper`*
is an exposition only class defined as follows:

``` cpp
class call_wrapper {
  using FD = decay_t<F>;
  FD fd;

  explicit call_wrapper(F&& f);

public:
  call_wrapper(call_wrapper&&) = default;
  call_wrapper(const call_wrapper&) = default;

  template<class... Args>
    auto operator()(Args&&...) &
      -> decltype(!declval<invoke_result_t<FD&, Args...>>());

  template<class... Args>
    auto operator()(Args&&...) const&
      -> decltype(!declval<invoke_result_t<const FD&, Args...>>());

  template<class... Args>
    auto operator()(Args&&...) &&
      -> decltype(!declval<invoke_result_t<FD, Args...>>());

  template<class... Args>
    auto operator()(Args&&...) const&&
      -> decltype(!declval<invoke_result_t<const FD, Args...>>());
};
```

``` cpp
explicit call_wrapper(F&& f);
```

*Requires:* `FD` shall satisfy the requirements of `MoveConstructible`.
`is_constructible_v<FD, F>` shall be `true`. `fd` shall be a callable
object ([[func.def]]).

*Effects:* Initializes `fd` from `std::forward<F>(f)`.

*Throws:* Any exception thrown by construction of `fd`.

``` cpp
template<class... Args>
  auto operator()(Args&&... args) &
    -> decltype(!declval<invoke_result_t<FD&, Args...>>());
template<class... Args>
  auto operator()(Args&&... args) const&
    -> decltype(!declval<invoke_result_t<const FD&, Args...>>());
```

*Effects:* Equivalent to:

``` cpp
return !INVOKE(fd, std::forward<Args>(args)...);              // see REF:func.require
```

``` cpp
template<class... Args>
  auto operator()(Args&&... args) &&
    -> decltype(!declval<invoke_result_t<FD, Args...>>());
template<class... Args>
  auto operator()(Args&&... args) const&&
    -> decltype(!declval<invoke_result_t<const FD, Args...>>());
```

*Effects:* Equivalent to:

``` cpp
return !INVOKE(std::move(fd), std::forward<Args>(args)...);   // see REF:func.require
```

### Function object binders <a id="func.bind">[[func.bind]]</a>

This subclause describes a uniform mechanism for binding arguments of
callable objects.

#### Class template `is_bind_expression` <a id="func.bind.isbind">[[func.bind.isbind]]</a>

``` cpp
namespace std {
  template<class T> struct is_bind_expression;  // see below
}
```

The class template `is_bind_expression` can be used to detect function
objects generated by `bind`. The function template `bind` uses
`is_bind_expression` to detect subexpressions.

Instantiations of the `is_bind_expression` template shall meet the
`UnaryTypeTrait` requirements ([[meta.rqmts]]). The implementation
shall provide a definition that has a base characteristic of `true_type`
if `T` is a type returned from `bind`, otherwise it shall have a base
characteristic of `false_type`. A program may specialize this template
for a user-defined type `T` to have a base characteristic of `true_type`
to indicate that `T` should be treated as a subexpression in a `bind`
call.

#### Class template `is_placeholder` <a id="func.bind.isplace">[[func.bind.isplace]]</a>

``` cpp
namespace std {
  template<class T> struct is_placeholder;      // see below
}
```

The class template `is_placeholder` can be used to detect the standard
placeholders `_1`, `_2`, and so on. The function template `bind` uses
`is_placeholder` to detect placeholders.

Instantiations of the `is_placeholder` template shall meet the
`UnaryTypeTrait` requirements ([[meta.rqmts]]). The implementation
shall provide a definition that has the base characteristic of
`integral_constant<int, J>` if `T` is the type of
`std::placeholders::_J`, otherwise it shall have a base characteristic
of `integral_constant<int, 0>`. A program may specialize this template
for a user-defined type `T` to have a base characteristic of
`integral_constant<int, N>` with `N > 0` to indicate that `T` should be
treated as a placeholder type.

#### Function template `bind` <a id="func.bind.bind">[[func.bind.bind]]</a>

In the text that follows:

- `FD` is the type `decay_t<F>`,
- `fd` is an lvalue of type `FD` constructed from `std::forward<F>(f)`,
- `Tᵢ` is the iᵗʰ type in the template parameter pack `BoundArgs`,
- `TDᵢ` is the type `decay_t<\tcode{T}_i>`,
- `tᵢ` is the iᵗʰ argument in the function parameter pack `bound_args`,
- `tdᵢ` is an lvalue of type `TDᵢ` constructed from
  `std::forward<\tcode{T}_i>(\tcode{t}_i)`,
- `Uⱼ` is the jᵗʰ deduced type of the `UnBoundArgs&&...` parameter of
  the forwarding call wrapper, and
- `uⱼ` is the jᵗʰ argument associated with `Uⱼ`.

``` cpp
template<class F, class... BoundArgs>
  unspecified bind(F&& f, BoundArgs&&... bound_args);
```

*Requires:* `is_constructible_v<FD, F>` shall be `true`. For each `Tᵢ`
in `BoundArgs`, `is_constructible_v<``TDᵢ``, ``Tᵢ``>` shall be `true`.
*INVOKE*(fd, w₁, w₂, …, $w_N$) ([[func.require]]) shall be a valid
expression for some values `w₁`, `w₂`, …, $\texttt{w}_N$, where N has
the value `sizeof...(bound_args)`. The cv-qualifiers cv of the call
wrapper `g`, as specified below, shall be neither `volatile` nor
`const volatile`.

*Returns:* A forwarding call wrapper `g` ([[func.require]]). The effect
of `g(``u₁``, ``u₂``, …, `$\texttt{u}_M$`)` shall be

``` cpp
INVOKE(fd, std::forward<$V_1$>($v_1$), std::forward<$V_2$>($v_2$), … , std::forward<$V_N$>($v_N$))
```

where the values and types of the bound arguments `v₁`, `v₂`, …,
$\texttt{v}_N$ are determined as specified below. The copy constructor
and move constructor of the forwarding call wrapper shall throw an
exception if and only if the corresponding constructor of `FD` or of any
of the types `TDᵢ` throws an exception.

*Throws:* Nothing unless the construction of `fd` or of one of the
values `tdᵢ` throws an exception.

*Remarks:* The return type shall satisfy the requirements of
`MoveConstructible`. If all of `FD` and `TDᵢ` satisfy the requirements
of `CopyConstructible`, then the return type shall satisfy the
requirements of `CopyConstructible`.

[*Note 1*: This implies that all of `FD` and `TDᵢ` are
`MoveConstructible`. — *end note*]

``` cpp
template<class R, class F, class... BoundArgs>
  unspecified bind(F&& f, BoundArgs&&... bound_args);
```

*Requires:* `is_constructible_v<FD, F>` shall be `true`. For each `Tᵢ`
in `BoundArgs`, `is_constructible_v<``TDᵢ``, ``Tᵢ``>` shall be `true`.
*INVOKE*(fd, w₁, w₂, …, $w_N$) shall be a valid expression for some
values `w₁`, `w₂`, …, $\texttt{w}_N$, where N has the value
`sizeof...(bound_args)`. The cv-qualifiers cv of the call wrapper `g`,
as specified below, shall be neither `volatile` nor `const volatile`.

*Returns:* A forwarding call wrapper `g` ([[func.require]]). The effect
of `g(``u₁``, ``u₂``, …, `$\texttt{u}_M$`)` shall be

``` cpp
INVOKE<R>(fd, std::forward<$V_1$>($v_1$), std::forward<$V_2$>($v_2$), … , std::forward<$V_N$>($v_N$))
```

where the values and types of the bound arguments `v₁`, `v₂`, …,
$\texttt{v}_N$ are determined as specified below. The copy constructor
and move constructor of the forwarding call wrapper shall throw an
exception if and only if the corresponding constructor of `FD` or of any
of the types `TDᵢ` throws an exception.

*Throws:* Nothing unless the construction of `fd` or of one of the
values `tdᵢ` throws an exception.

*Remarks:* The return type shall satisfy the requirements of
`MoveConstructible`. If all of `FD` and `TDᵢ` satisfy the requirements
of `CopyConstructible`, then the return type shall satisfy the
requirements of `CopyConstructible`.

[*Note 2*: This implies that all of `FD` and `TDᵢ` are
`MoveConstructible`. — *end note*]

The values of the `v₁`, `v₂`, …, $\tcode{v}_N$ and their corresponding
types `V₁`, `V₂`, …, $\tcode{V}_N$ depend on the types `TDᵢ` derived
from the call to `bind` and the cv-qualifiers cv of the call wrapper `g`
as follows:

- if `TDᵢ` is `reference_wrapper<T>`, the argument is
  `\tcode{td}_i.get()` and its type `Vᵢ` is `T&`;
- if the value of `is_bind_expression_v<\tcode{TD}_i>` is `true`, the
  argument is `\tcode{td}_i(std::forward<\tcode{U}_j>(\tcode{u}_j)...)`
  and its type `Vᵢ` is
  `invoke_result_t<\tcode{TD}_i cv{} &, \tcode{U}_j...>&&`;
- if the value `j` of `is_placeholder_v<\tcode{TD}_i>` is not zero, the
  argument is `std::forward<\tcode{U}_j>(\tcode{u}_j)` and its type `Vᵢ`
  is `\tcode{U}_j&&`;
- otherwise, the value is `tdᵢ` and its type `Vᵢ` is
  `\tcode{TD}_i cv{} &`.

#### Placeholders <a id="func.bind.place">[[func.bind.place]]</a>

``` cpp
namespace std::placeholders {
  // M is the implementation-defined number of placeholders
  see below _1;
  see below _2;
              .
              .
              .
  see below _M;
}
```

All placeholder types shall be `DefaultConstructible` and
`CopyConstructible`, and their default constructors and copy/move
constructors shall not throw exceptions. It is *implementation-defined*
whether placeholder types are `CopyAssignable`. `CopyAssignable`
placeholders’ copy assignment operators shall not throw exceptions.

Placeholders should be defined as:

``` cpp
inline constexpr unspecified _1{};
```

If they are not, they shall be declared as:

``` cpp
extern unspecified _1;
```

### Function template `mem_fn` <a id="func.memfn">[[func.memfn]]</a>

``` cpp
template<class R, class T> unspecified mem_fn(R T::* pm) noexcept;
```

*Returns:* A simple call wrapper ([[func.def]]) `fn` such that the
expression `fn(t, a2, ..., aN)` is equivalent to *INVOKE*(pm, t, a2,
..., aN) ([[func.require]]).

### Polymorphic function wrappers <a id="func.wrap">[[func.wrap]]</a>

This subclause describes a polymorphic wrapper class that encapsulates
arbitrary callable objects.

#### Class `bad_function_call` <a id="func.wrap.badcall">[[func.wrap.badcall]]</a>

An exception of type `bad_function_call` is thrown by
`function::operator()` ([[func.wrap.func.inv]]) when the function
wrapper object has no target.

``` cpp
namespace std {
  class bad_function_call : public exception {
  public:
    // [func.wrap.badcall.const], constructor
    bad_function_call() noexcept;
  };
}
```

##### `bad_function_call` constructor <a id="func.wrap.badcall.const">[[func.wrap.badcall.const]]</a>

``` cpp
bad_function_call() noexcept;
```

*Effects:* Constructs a `bad_function_call` object.

*Postconditions:* `what()` returns an *implementation-defined* NTBS.

#### Class template `function` <a id="func.wrap.func">[[func.wrap.func]]</a>

``` cpp
namespace std {
  template<class> class function; // not defined

  template<class R, class... ArgTypes>
  class function<R(ArgTypes...)> {
  public:
    using result_type = R;

    // [func.wrap.func.con], construct/copy/destroy
    function() noexcept;
    function(nullptr_t) noexcept;
    function(const function&);
    function(function&&);
    template<class F> function(F);

    function& operator=(const function&);
    function& operator=(function&&);
    function& operator=(nullptr_t) noexcept;
    template<class F> function& operator=(F&&);
    template<class F> function& operator=(reference_wrapper<F>) noexcept;

    ~function();

    // [func.wrap.func.mod], function modifiers
    void swap(function&) noexcept;

    // [func.wrap.func.cap], function capacity
    explicit operator bool() const noexcept;

    // [func.wrap.func.inv], function invocation
    R operator()(ArgTypes...) const;

    // [func.wrap.func.targ], function target access
    const type_info& target_type() const noexcept;
    template<class T>       T* target() noexcept;
    template<class T> const T* target() const noexcept;
  };

  template<class R, class... ArgTypes>
    function(R(*)(ArgTypes...)) -> function<R(ArgTypes...)>;

  template<class F> function(F) -> function<see below>;

  // [func.wrap.func.nullptr], Null pointer comparisons
  template <class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

  template <class R, class... ArgTypes>
    bool operator==(nullptr_t, const function<R(ArgTypes...)>&) noexcept;

  template <class R, class... ArgTypes>
    bool operator!=(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

  template <class R, class... ArgTypes>
    bool operator!=(nullptr_t, const function<R(ArgTypes...)>&) noexcept;

  // [func.wrap.func.alg], specialized algorithms
  template <class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&) noexcept;
}
```

The `function` class template provides polymorphic wrappers that
generalize the notion of a function pointer. Wrappers can store, copy,
and call arbitrary callable objects ([[func.def]]), given a call
signature ([[func.def]]), allowing functions to be first-class objects.

A callable type ([[func.def]]) `F` is *Lvalue-Callable* for argument
types `ArgTypes` and return type `R` if the expression
`INVOKE<R>(declval<F&>(), declval<ArgTypes>()...)`, considered as an
unevaluated operand (Clause  [[expr]]), is well formed (
[[func.require]]).

The `function` class template is a call wrapper ([[func.def]]) whose
call signature ([[func.def]]) is `R(ArgTypes...)`.

[*Note 1*: The types deduced by the deduction guides for `function` may
change in future versions of this International Standard. — *end note*]

##### `function` construct/copy/destroy <a id="func.wrap.func.con">[[func.wrap.func.con]]</a>

``` cpp
function() noexcept;
```

*Postconditions:* `!*this`.

``` cpp
function(nullptr_t) noexcept;
```

*Postconditions:* `!*this`.

``` cpp
function(const function& f);
```

*Postconditions:* `!*this` if `!f`; otherwise, `*this` targets a copy of
`f.target()`.

*Throws:* shall not throw exceptions if `f`’s target is a specialization
of `reference_wrapper` or a function pointer. Otherwise, may throw
`bad_alloc` or any exception thrown by the copy constructor of the
stored callable object.

[*Note 1*: Implementations are encouraged to avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f`’s target is an object holding only a pointer or reference to
an object and a member function pointer. — *end note*]

``` cpp
function(function&& f);
```

*Postconditions:* If `!f`, `*this` has no target; otherwise, the target
of `*this` is equivalent to the target of `f` before the construction,
and `f` is in a valid state with an unspecified value.

*Throws:* shall not throw exceptions if `f`’s target is a specialization
of `reference_wrapper` or a function pointer. Otherwise, may throw
`bad_alloc` or any exception thrown by the copy or move constructor of
the stored callable object.

[*Note 2*: Implementations are encouraged to avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f`’s target is an object holding only a pointer or reference to
an object and a member function pointer. — *end note*]

``` cpp
template<class F> function(F f);
```

*Requires:* `F` shall be `CopyConstructible`.

*Remarks:* This constructor template shall not participate in overload
resolution unless `F` is Lvalue-Callable ([[func.wrap.func]]) for
argument types `ArgTypes...` and return type `R`.

*Postconditions:* `!*this` if any of the following hold:

- `f` is a null function pointer value.
- `f` is a null member pointer value.
- `F` is an instance of the `function` class template, and `!f`.

Otherwise, `*this` targets a copy of `f` initialized with
`std::move(f)`.

[*Note 3*: Implementations are encouraged to avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f` is an object holding only a pointer or reference to an object
and a member function pointer. — *end note*]

*Throws:* shall not throw exceptions when `f` is a function pointer or a
`reference_wrapper<T>` for some `T`. Otherwise, may throw `bad_alloc` or
any exception thrown by `F`’s copy or move constructor.

``` cpp
template<class F> function(F) -> function<see below>;
```

*Remarks:* This deduction guide participates in overload resolution only
if `&F::operator()` is well-formed when treated as an unevaluated
operand. In that case, if `decltype(&F::operator())` is of the form
`R(G::*)(A...)` cv `&ₒₚₜ noexcept` for a class type `G`, then the
deduced type is `function<R(A...)>`.

[*Example 1*:

``` cpp
void f() {
  int i{5};
  function g = [&](double) { return i; }; // deduces function<int(double)>
}
```

— *end example*]

``` cpp
function& operator=(const function& f);
```

*Effects:* As if by `function(f).swap(*this);`

*Returns:* `*this`.

``` cpp
function& operator=(function&& f);
```

*Effects:* Replaces the target of `*this` with the target of `f`.

*Returns:* `*this`.

``` cpp
function& operator=(nullptr_t) noexcept;
```

*Effects:* If `*this != nullptr`, destroys the target of `this`.

*Postconditions:* `!(*this)`.

*Returns:* `*this`.

``` cpp
template<class F> function& operator=(F&& f);
```

*Effects:* As if by: `function(std::forward<F>(f)).swap(*this);`

*Returns:* `*this`.

*Remarks:* This assignment operator shall not participate in overload
resolution unless `decay_t<F>` is Lvalue-Callable ([[func.wrap.func]])
for argument types `ArgTypes...` and return type `R`.

``` cpp
template<class F> function& operator=(reference_wrapper<F> f) noexcept;
```

*Effects:* As if by: `function(f).swap(*this);`

*Returns:* `*this`.

``` cpp
~function();
```

*Effects:* If `*this != nullptr`, destroys the target of `this`.

##### `function` modifiers <a id="func.wrap.func.mod">[[func.wrap.func.mod]]</a>

``` cpp
void swap(function& other) noexcept;
```

*Effects:* interchanges the targets of `*this` and `other`.

##### `function` capacity <a id="func.wrap.func.cap">[[func.wrap.func.cap]]</a>

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `true` if `*this` has a target, otherwise `false`.

##### `function` invocation <a id="func.wrap.func.inv">[[func.wrap.func.inv]]</a>

``` cpp
R operator()(ArgTypes... args) const;
```

*Returns:* *INVOKE*\<R\>(f,
std::forward\<ArgTypes\>(args)...) ([[func.require]]), where `f` is the
target object ([[func.def]]) of `*this`.

*Throws:* `bad_function_call` if `!*this`; otherwise, any exception
thrown by the wrapped callable object.

##### `function` target access <a id="func.wrap.func.targ">[[func.wrap.func.targ]]</a>

``` cpp
const type_info& target_type() const noexcept;
```

*Returns:* If `*this` has a target of type `T`, `typeid(T)`; otherwise,
`typeid(void)`.

``` cpp
template<class T>       T* target() noexcept;
template<class T> const T* target() const noexcept;
```

*Returns:* If `target_type() == typeid(T)` a pointer to the stored
function target; otherwise a null pointer.

##### null pointer comparison functions <a id="func.wrap.func.nullptr">[[func.wrap.func.nullptr]]</a>

``` cpp
template <class R, class... ArgTypes>
  bool operator==(const function<R(ArgTypes...)>& f, nullptr_t) noexcept;
template <class R, class... ArgTypes>
  bool operator==(nullptr_t, const function<R(ArgTypes...)>& f) noexcept;
```

*Returns:* `!f`.

``` cpp
template <class R, class... ArgTypes>
  bool operator!=(const function<R(ArgTypes...)>& f, nullptr_t) noexcept;
template <class R, class... ArgTypes>
  bool operator!=(nullptr_t, const function<R(ArgTypes...)>& f) noexcept;
```

*Returns:* `(bool)f`.

##### specialized algorithms <a id="func.wrap.func.alg">[[func.wrap.func.alg]]</a>

``` cpp
template<class R, class... ArgTypes>
  void swap(function<R(ArgTypes...)>& f1, function<R(ArgTypes...)>& f2) noexcept;
```

*Effects:* As if by: `f1.swap(f2);`

### Searchers <a id="func.search">[[func.search]]</a>

This subclause provides function object types ([[function.objects]])
for operations that search for a sequence \[`pat``first`, `pat_last`) in
another sequence \[`first`, `last`) that is provided to the object’s
function call operator. The first sequence (the pattern to be searched
for) is provided to the object’s constructor, and the second (the
sequence to be searched) is provided to the function call operator.

Each specialization of a class template specified in this subclause
[[func.search]] shall meet the `CopyConstructible` and `CopyAssignable`
requirements. Template parameters named

- `ForwardIterator`,
- `ForwardIterator1`,
- `ForwardIterator2`,
- `RandomAccessIterator`,
- `RandomAccessIterator1`,
- `RandomAccessIterator2`, and
- `BinaryPredicate`

of templates specified in this subclause [[func.search]] shall meet the
same requirements and semantics as specified in [[algorithms.general]].
Template parameters named `Hash` shall meet the requirements as
specified in [[hash.requirements]].

The Boyer-Moore searcher implements the Boyer-Moore search algorithm.
The Boyer-Moore-Horspool searcher implements the Boyer-Moore-Horspool
search algorithm. In general, the Boyer-Moore searcher will use more
memory and give better runtime performance than Boyer-Moore-Horspool.

#### Class template `default_searcher` <a id="func.search.default">[[func.search.default]]</a>

``` cpp
template <class ForwardIterator1, class BinaryPredicate = equal_to<>>
  class default_searcher {
  public:
    default_searcher(ForwardIterator1 pat_first, ForwardIterator1 pat_last,
                     BinaryPredicate pred = BinaryPredicate());

    template <class ForwardIterator2>
      pair<ForwardIterator2, ForwardIterator2>
        operator()(ForwardIterator2 first, ForwardIterator2 last) const;

  private:
    ForwardIterator1 pat_first_;        // exposition only
    ForwardIterator1 pat_last_;         // exposition only
    BinaryPredicate pred_;              // exposition only
  };
```

``` cpp
default_searcher(ForwardIterator pat_first, ForwardIterator pat_last,
                 BinaryPredicate pred = BinaryPredicate());
```

*Effects:* Constructs a `default_searcher` object, initializing
`pat_first_` with `pat_first`, \texttt{pat_last\_} with `pat_last`, and
`pred_` with `pred`.

*Throws:* Any exception thrown by the copy constructor of
`BinaryPredicate` or `ForwardIterator1`.

``` cpp
template<class ForwardIterator2>
  pair<ForwardIterator2, ForwardIterator2>
    operator()(ForwardIterator2 first, ForwardIterator2 last) const;
```

*Effects:* Returns a pair of iterators `i` and `j` such that

- `i == search(first, last, pat_first_, pat_last_, pred_)`, and
- if `i == last`, then `j == last`, otherwise
  `j == next(i, distance(pat_first_, pat_last_))`.

#### Class template `boyer_moore_searcher` <a id="func.search.bm">[[func.search.bm]]</a>

``` cpp
template <class RandomAccessIterator1,
          class Hash = hash<typename iterator_traits<RandomAccessIterator1>::value_type>,
          class BinaryPredicate = equal_to<>>
  class boyer_moore_searcher {
  public:
    boyer_moore_searcher(RandomAccessIterator1 pat_first,
                         RandomAccessIterator1 pat_last,
                         Hash hf = Hash(),
                         BinaryPredicate pred = BinaryPredicate());

    template <class RandomAccessIterator2>
      pair<RandomAccessIterator2, RandomAccessIterator2>
        operator()(RandomAccessIterator2 first, RandomAccessIterator2 last) const;

  private:
    RandomAccessIterator1 pat_first_;   // exposition only
    RandomAccessIterator1 pat_last_;    // exposition only
    Hash hash_;                         // exposition only
    BinaryPredicate pred_;              // exposition only
  };
```

``` cpp
boyer_moore_searcher(RandomAccessIterator1 pat_first,
                     RandomAccessIterator1 pat_last,
                     Hash hf = Hash(),
                     BinaryPredicate pred = BinaryPredicate());
```

*Requires:* The value type of `RandomAccessIterator1` shall meet the
`DefaultConstructible` requirements, the `CopyConstructible`
requirements, and the `CopyAssignable` requirements.

*Requires:* For any two values `A` and `B` of the type
`iterator_traits<RandomAccessIterator1>::value_type`, if
`pred(A, B) == true`, then `hf(A) == hf(B)` shall be `true`.

*Effects:* Constructs a `boyer_moore_searcher` object, initializing
`pat_first_` with `pat_first`, `pat_last_` with `pat_last`, `hash_` with
`hf`, and `pred_` with `pred`.

*Throws:* Any exception thrown by the copy constructor of
`RandomAccessIterator1`, or by the default constructor, copy
constructor, or the copy assignment operator of the value type of
`RandomAccessIterator1`, or the copy constructor or `operator()` of
`BinaryPredicate` or `Hash`. May throw `bad_alloc` if additional memory
needed for internal data structures cannot be allocated.

``` cpp
template <class RandomAccessIterator2>
  pair<RandomAccessIterator2, RandomAccessIterator2>
    operator()(RandomAccessIterator2 first, RandomAccessIterator2 last) const;
```

*Requires:* `RandomAccessIterator1` and `RandomAccessIterator2` shall
have the same value type.

*Effects:* Finds a subsequence of equal values in a sequence.

*Returns:* A pair of iterators `i` and `j` such that

- `i` is the first iterator in the range \[`first`,
  `last - (pat_last_ - pat_first_)`) such that for every non-negative
  integer `n` less than `pat_last_ - pat_first_` the following condition
  holds: `pred(*(i + n), *(pat_first_ + n)) != false`, and
- `j == next(i, distance(pat_first_, pat_last_))`.

Returns `make_pair(first, first)` if \[`pat_first_`, `pat_last_`) is
empty, otherwise returns `make_pair(last, last)` if no such iterator is
found.

*Complexity:* At most `(last - first) * (pat_last_ - pat_first_)`
applications of the predicate.

#### Class template `boyer_moore_horspool_searcher` <a id="func.search.bmh">[[func.search.bmh]]</a>

``` cpp
template <class RandomAccessIterator1,
          class Hash = hash<typename iterator_traits<RandomAccessIterator1>::value_type>,
          class BinaryPredicate = equal_to<>>
  class boyer_moore_horspool_searcher {
  public:
    boyer_moore_horspool_searcher(RandomAccessIterator1 pat_first,
                                  RandomAccessIterator1 pat_last,
                                  Hash hf = Hash(),
                                  BinaryPredicate pred = BinaryPredicate());

    template <class RandomAccessIterator2>
      pair<RandomAccessIterator2, RandomAccessIterator2>
        operator()(RandomAccessIterator2 first, RandomAccessIterator2 last) const;

  private:
    RandomAccessIterator1 pat_first_;   // exposition only
    RandomAccessIterator1 pat_last_;    // exposition only
    Hash hash_;                         // exposition only
    BinaryPredicate pred_;              // exposition only
  };
```

``` cpp
boyer_moore_horspool_searcher(RandomAccessIterator1 pat_first,
                              RandomAccessIterator1 pat_last,
                              Hash hf = Hash(),
                              BinaryPredicate pred = BinaryPredicate());
```

*Requires:* The value type of `RandomAccessIterator1` shall meet the
`DefaultConstructible`, `CopyConstructible`, and `CopyAssignable`
requirements.

*Requires:* For any two values `A` and `B` of the type
`iterator_traits<RandomAccessIterator1>::value_type`, if
`pred(A, B) == true`, then `hf(A) == hf(B)` shall be `true`.

*Effects:* Constructs a `boyer_moore_horspool_searcher` object,
initializing `pat_first_` with `pat_first`, `pat_last_` with `pat_last`,
`hash_` with `hf`, and `pred_` with `pred`.

*Throws:* Any exception thrown by the copy constructor of
`RandomAccessIterator1`, or by the default constructor, copy
constructor, or the copy assignment operator of the value type of
`RandomAccessIterator1` or the copy constructor or `operator()` of
`BinaryPredicate` or `Hash`. May throw `bad_alloc` if additional memory
needed for internal data structures cannot be allocated.

``` cpp
template <class RandomAccessIterator2>
  pair<RandomAccessIterator2, RandomAccessIterator2>
    operator()(RandomAccessIterator2 first, RandomAccessIterator2 last) const;
```

*Requires:* `RandomAccessIterator1` and `RandomAccessIterator2` shall
have the same value type.

*Effects:* Finds a subsequence of equal values in a sequence.

*Returns:* A pair of iterators `i` and `j` such that

- `i` is the first iterator `i` in the range \[`first`,
  `last - (pat_last_ - pat_first_)`) such that for every non-negative
  integer `n` less than `pat_last_ - pat_first_` the following condition
  holds: `pred(*(i + n), *(pat_first_ + n)) != false`, and
- `j == next(i, distance(pat_first_, pat_last_))`.

Returns `make_pair(first, first)` if \[`pat_first_`, `pat_last_`) is
empty, otherwise returns `make_pair(last, last)` if no such iterator is
found.

*Complexity:* At most `(last - first) * (pat_last_ - pat_first_)`
applications of the predicate.

### Class template `hash` <a id="unord.hash">[[unord.hash]]</a>

The unordered associative containers defined in [[unord]] use
specializations of the class template `hash` ([[functional.syn]]) as
the default hash function.

Each specialization of `hash` is either enabled or disabled, as
described below.

[*Note 1*: Enabled specializations meet the requirements of `Hash`, and
disabled specializations do not. — *end note*]

Each header that declares the template `hash` provides enabled
specializations of `hash` for `nullptr_t` and all cv-unqualified
arithmetic, enumeration, and pointer types. For any type `Key` for which
neither the library nor the user provides an explicit or partial
specialization of the class template `hash`, `hash<Key>` is disabled.

If the library provides an explicit or partial specialization of
`hash<Key>`, that specialization is enabled except as noted otherwise,
and its member functions are `noexcept` except as noted otherwise.

If `H` is a disabled specialization of `hash`, these values are `false`:
`is_default_constructible_v<H>`, `is_copy_constructible_v<H>`,
`is_move_constructible_v<H>`, `is_copy_assignable_v<H>`, and
`is_move_assignable_v<H>`. Disabled specializations of `hash` are not
function object types ([[function.objects]]).

[*Note 2*: This means that the specialization of `hash` exists, but any
attempts to use it as a `Hash` will be ill-formed. — *end note*]

An enabled specialization `hash<Key>` will:

- satisfy the `Hash` requirements ([[hash.requirements]]), with `Key`
  as the function call argument type, the `DefaultConstructible`
  requirements (Table  [[tab:defaultconstructible]]), the
  `CopyAssignable` requirements (Table  [[tab:copyassignable]]),
- be swappable ([[swappable.requirements]]) for lvalues,
- satisfy the requirement that if `k1 == k2` is `true`, `h(k1) == h(k2)`
  is also `true`, where `h` is an object of type `hash<Key>` and `k1`
  and `k2` are objects of type `Key`;
- satisfy the requirement that the expression `h(k)`, where `h` is an
  object of type `hash<Key>` and `k` is an object of type `Key`, shall
  not throw an exception unless `hash<Key>` is a user-defined
  specialization that depends on at least one user-defined type.

## Metaprogramming and type traits <a id="meta">[[meta]]</a>

This subclause describes components used by C++programs, particularly in
templates, to support the widest possible range of types, optimise
template code usage, detect type related user errors, and perform type
inference and transformation at compile time. It includes type
classification traits, type property inspection traits, and type
transformations. The type classification traits describe a complete
taxonomy of all possible C++types, and state where in that taxonomy a
given type belongs. The type property inspection traits allow important
characteristics of types or of combinations of types to be inspected.
The type transformations allow certain properties of types to be
manipulated.

All functions specified in this subclause are signal-safe (
[[csignal.syn]]).

### Requirements <a id="meta.rqmts">[[meta.rqmts]]</a>

A *UnaryTypeTrait* describes a property of a type. It shall be a class
template that takes one template type argument and, optionally,
additional arguments that help define the property being described. It
shall be `DefaultConstructible`, `CopyConstructible`, and publicly and
unambiguously derived, directly or indirectly, from its *base
characteristic*, which is a specialization of the template
`integral_constant` ([[meta.help]]), with the arguments to the template
`integral_constant` determined by the requirements for the particular
property being described. The member names of the base characteristic
shall not be hidden and shall be unambiguously available in the
`UnaryTypeTrait`.

A *BinaryTypeTrait* describes a relationship between two types. It shall
be a class template that takes two template type arguments and,
optionally, additional arguments that help define the relationship being
described. It shall be `DefaultConstructible`, `CopyConstructible`, and
publicly and unambiguously derived, directly or indirectly, from its
*base characteristic*, which is a specialization of the template
`integral_constant` ([[meta.help]]), with the arguments to the template
`integral_constant` determined by the requirements for the particular
relationship being described. The member names of the base
characteristic shall not be hidden and shall be unambiguously available
in the `BinaryTypeTrait`.

A *TransformationTrait* modifies a property of a type. It shall be a
class template that takes one template type argument and, optionally,
additional arguments that help define the modification. It shall define
a publicly accessible nested type named `type`, which shall be a synonym
for the modified type.

### Header `<type_traits>` synopsis <a id="meta.type.synop">[[meta.type.synop]]</a>

``` cpp
namespace std {
  // [meta.help], helper class
  template <class T, T v> struct integral_constant;

  template <bool B>
    using bool_constant = integral_constant<bool, B>;
  using true_type  = bool_constant<true>;
  using false_type = bool_constant<false>;

  // [meta.unary.cat], primary type categories
  template <class T> struct is_void;
  template <class T> struct is_null_pointer;
  template <class T> struct is_integral;
  template <class T> struct is_floating_point;
  template <class T> struct is_array;
  template <class T> struct is_pointer;
  template <class T> struct is_lvalue_reference;
  template <class T> struct is_rvalue_reference;
  template <class T> struct is_member_object_pointer;
  template <class T> struct is_member_function_pointer;
  template <class T> struct is_enum;
  template <class T> struct is_union;
  template <class T> struct is_class;
  template <class T> struct is_function;

  // [meta.unary.comp], composite type categories
  template <class T> struct is_reference;
  template <class T> struct is_arithmetic;
  template <class T> struct is_fundamental;
  template <class T> struct is_object;
  template <class T> struct is_scalar;
  template <class T> struct is_compound;
  template <class T> struct is_member_pointer;

  // [meta.unary.prop], type properties
  template <class T> struct is_const;
  template <class T> struct is_volatile;
  template <class T> struct is_trivial;
  template <class T> struct is_trivially_copyable;
  template <class T> struct is_standard_layout;
  template <class T> struct is_pod;
  template <class T> struct is_empty;
  template <class T> struct is_polymorphic;
  template <class T> struct is_abstract;
  template <class T> struct is_final;
  template <class T> struct is_aggregate;

  template <class T> struct is_signed;
  template <class T> struct is_unsigned;

  template <class T, class... Args> struct is_constructible;
  template <class T> struct is_default_constructible;
  template <class T> struct is_copy_constructible;
  template <class T> struct is_move_constructible;

  template <class T, class U> struct is_assignable;
  template <class T> struct is_copy_assignable;
  template <class T> struct is_move_assignable;

  template <class T, class U> struct is_swappable_with;
  template <class T> struct is_swappable;

  template <class T> struct is_destructible;

  template <class T, class... Args> struct is_trivially_constructible;
  template <class T> struct is_trivially_default_constructible;
  template <class T> struct is_trivially_copy_constructible;
  template <class T> struct is_trivially_move_constructible;

  template <class T, class U> struct is_trivially_assignable;
  template <class T> struct is_trivially_copy_assignable;
  template <class T> struct is_trivially_move_assignable;
  template <class T> struct is_trivially_destructible;

  template <class T, class... Args> struct is_nothrow_constructible;
  template <class T> struct is_nothrow_default_constructible;
  template <class T> struct is_nothrow_copy_constructible;
  template <class T> struct is_nothrow_move_constructible;

  template <class T, class U> struct is_nothrow_assignable;
  template <class T> struct is_nothrow_copy_assignable;
  template <class T> struct is_nothrow_move_assignable;

  template <class T, class U> struct is_nothrow_swappable_with;
  template <class T> struct is_nothrow_swappable;

  template <class T> struct is_nothrow_destructible;

  template <class T> struct has_virtual_destructor;

  template <class T> struct has_unique_object_representations;

  // [meta.unary.prop.query], type property queries
  template <class T> struct alignment_of;
  template <class T> struct rank;
  template <class T, unsigned I = 0> struct extent;

  // [meta.rel], type relations
  template <class T, class U> struct is_same;
  template <class Base, class Derived> struct is_base_of;
  template <class From, class To> struct is_convertible;

  template <class Fn, class... ArgTypes> struct is_invocable;
  template <class R, class Fn, class... ArgTypes> struct is_invocable_r;

  template <class Fn, class... ArgTypes> struct is_nothrow_invocable;
  template <class R, class Fn, class... ArgTypes> struct is_nothrow_invocable_r;

  // [meta.trans.cv], const-volatile modifications
  template <class T> struct remove_const;
  template <class T> struct remove_volatile;
  template <class T> struct remove_cv;
  template <class T> struct add_const;
  template <class T> struct add_volatile;
  template <class T> struct add_cv;

  template <class T>
    using remove_const_t    = typename remove_const<T>::type;
  template <class T>
    using remove_volatile_t = typename remove_volatile<T>::type;
  template <class T>
    using remove_cv_t       = typename remove_cv<T>::type;
  template <class T>
    using add_const_t       = typename add_const<T>::type;
  template <class T>
    using add_volatile_t    = typename add_volatile<T>::type;
  template <class T>
    using add_cv_t          = typename add_cv<T>::type;

  // [meta.trans.ref], reference modifications
  template <class T> struct remove_reference;
  template <class T> struct add_lvalue_reference;
  template <class T> struct add_rvalue_reference;

  template <class T>
    using remove_reference_t     = typename remove_reference<T>::type;
  template <class T>
    using add_lvalue_reference_t = typename add_lvalue_reference<T>::type;
  template <class T>
    using add_rvalue_reference_t = typename add_rvalue_reference<T>::type;

  // [meta.trans.sign], sign modifications
  template <class T> struct make_signed;
  template <class T> struct make_unsigned;

  template <class T>
    using make_signed_t   = typename make_signed<T>::type;
  template <class T>
    using make_unsigned_t = typename make_unsigned<T>::type;

  // [meta.trans.arr], array modifications
  template <class T> struct remove_extent;
  template <class T> struct remove_all_extents;

  template <class T>
    using remove_extent_t      = typename remove_extent<T>::type;
  template <class T>
    using remove_all_extents_t = typename remove_all_extents<T>::type;

  // [meta.trans.ptr], pointer modifications
  template <class T> struct remove_pointer;
  template <class T> struct add_pointer;

  template <class T>
    using remove_pointer_t = typename remove_pointer<T>::type;
  template <class T>
    using add_pointer_t    = typename add_pointer<T>::type;

  // [meta.trans.other], other transformations
  template <size_t Len,
            size_t Align = default-alignment> // see [meta.trans.other]
    struct aligned_storage;
  template <size_t Len, class... Types> struct aligned_union;
  template <class T> struct decay;
  template <bool, class T = void> struct enable_if;
  template <bool, class T, class F> struct conditional;
  template <class... T> struct common_type;
  template <class T> struct underlying_type;
  template <class Fn, class... ArgTypes> struct invoke_result;

  template <size_t Len,
            size_t Align = default-alignment> // see [meta.trans.other]
    using aligned_storage_t = typename aligned_storage<Len, Align>::type;
  template <size_t Len, class... Types>
    using aligned_union_t   = typename aligned_union<Len, Types...>::type;
  template <class T>
    using decay_t           = typename decay<T>::type;
  template <bool b, class T = void>
    using enable_if_t       = typename enable_if<b, T>::type;
  template <bool b, class T, class F>
    using conditional_t     = typename conditional<b, T, F>::type;
  template <class... T>
    using common_type_t     = typename common_type<T...>::type;
  template <class T>
    using underlying_type_t = typename underlying_type<T>::type;
  template <class Fn, class... ArgTypes>
    using invoke_result_t   = typename invoke_result<Fn, ArgTypes...>::type;
  template <class...>
    using void_t            = void;

  // [meta.logical], logical operator traits
  template<class... B> struct conjunction;
  template<class... B> struct disjunction;
  template<class B> struct negation;

  // [meta.unary.cat], primary type categories
  template <class T> inline constexpr bool is_void_v
    = is_void<T>::value;
  template <class T> inline constexpr bool is_null_pointer_v
    = is_null_pointer<T>::value;
  template <class T> inline constexpr bool is_integral_v
    = is_integral<T>::value;
  template <class T> inline constexpr bool is_floating_point_v
    = is_floating_point<T>::value;
  template <class T> inline constexpr bool is_array_v
    = is_array<T>::value;
  template <class T> inline constexpr bool is_pointer_v
    = is_pointer<T>::value;
  template <class T> inline constexpr bool is_lvalue_reference_v
    = is_lvalue_reference<T>::value;
  template <class T> inline constexpr bool is_rvalue_reference_v
    = is_rvalue_reference<T>::value;
  template <class T> inline constexpr bool is_member_object_pointer_v
    = is_member_object_pointer<T>::value;
  template <class T> inline constexpr bool is_member_function_pointer_v
    = is_member_function_pointer<T>::value;
  template <class T> inline constexpr bool is_enum_v
    = is_enum<T>::value;
  template <class T> inline constexpr bool is_union_v
    = is_union<T>::value;
  template <class T> inline constexpr bool is_class_v
    = is_class<T>::value;
  template <class T> inline constexpr bool is_function_v
    = is_function<T>::value;

  // [meta.unary.comp], composite type categories
  template <class T> inline constexpr bool is_reference_v
    = is_reference<T>::value;
  template <class T> inline constexpr bool is_arithmetic_v
    = is_arithmetic<T>::value;
  template <class T> inline constexpr bool is_fundamental_v
    = is_fundamental<T>::value;
  template <class T> inline constexpr bool is_object_v
    = is_object<T>::value;
  template <class T> inline constexpr bool is_scalar_v
    = is_scalar<T>::value;
  template <class T> inline constexpr bool is_compound_v
    = is_compound<T>::value;
  template <class T> inline constexpr bool is_member_pointer_v
    = is_member_pointer<T>::value;

  // [meta.unary.prop], type properties
  template <class T> inline constexpr bool is_const_v
    = is_const<T>::value;
  template <class T> inline constexpr bool is_volatile_v
    = is_volatile<T>::value;
  template <class T> inline constexpr bool is_trivial_v
    = is_trivial<T>::value;
  template <class T> inline constexpr bool is_trivially_copyable_v
    = is_trivially_copyable<T>::value;
  template <class T> inline constexpr bool is_standard_layout_v
    = is_standard_layout<T>::value;
  template <class T> inline constexpr bool is_pod_v
    = is_pod<T>::value;
  template <class T> inline constexpr bool is_empty_v
    = is_empty<T>::value;
  template <class T> inline constexpr bool is_polymorphic_v
    = is_polymorphic<T>::value;
  template <class T> inline constexpr bool is_abstract_v
    = is_abstract<T>::value;
  template <class T> inline constexpr bool is_final_v
    = is_final<T>::value;
  template <class T> inline constexpr bool is_aggregate_v
    = is_aggregate<T>::value;
  template <class T> inline constexpr bool is_signed_v
    = is_signed<T>::value;
  template <class T> inline constexpr bool is_unsigned_v
    = is_unsigned<T>::value;
  template <class T, class... Args> inline constexpr bool is_constructible_v
    = is_constructible<T, Args...>::value;
  template <class T> inline constexpr bool is_default_constructible_v
    = is_default_constructible<T>::value;
  template <class T> inline constexpr bool is_copy_constructible_v
    = is_copy_constructible<T>::value;
  template <class T> inline constexpr bool is_move_constructible_v
    = is_move_constructible<T>::value;
  template <class T, class U> inline constexpr bool is_assignable_v
    = is_assignable<T, U>::value;
  template <class T> inline constexpr bool is_copy_assignable_v
    = is_copy_assignable<T>::value;
  template <class T> inline constexpr bool is_move_assignable_v
    = is_move_assignable<T>::value;
  template <class T, class U> inline constexpr bool is_swappable_with_v
    = is_swappable_with<T, U>::value;
  template <class T> inline constexpr bool is_swappable_v
    = is_swappable<T>::value;
  template <class T> inline constexpr bool is_destructible_v
    = is_destructible<T>::value;
  template <class T, class... Args> inline constexpr bool is_trivially_constructible_v
    = is_trivially_constructible<T, Args...>::value;
  template <class T> inline constexpr bool is_trivially_default_constructible_v
    = is_trivially_default_constructible<T>::value;
  template <class T> inline constexpr bool is_trivially_copy_constructible_v
    = is_trivially_copy_constructible<T>::value;
  template <class T> inline constexpr bool is_trivially_move_constructible_v
    = is_trivially_move_constructible<T>::value;
  template <class T, class U> inline constexpr bool is_trivially_assignable_v
    = is_trivially_assignable<T, U>::value;
  template <class T> inline constexpr bool is_trivially_copy_assignable_v
    = is_trivially_copy_assignable<T>::value;
  template <class T> inline constexpr bool is_trivially_move_assignable_v
    = is_trivially_move_assignable<T>::value;
  template <class T> inline constexpr bool is_trivially_destructible_v
    = is_trivially_destructible<T>::value;
  template <class T, class... Args> inline constexpr bool is_nothrow_constructible_v
    = is_nothrow_constructible<T, Args...>::value;
  template <class T> inline constexpr bool is_nothrow_default_constructible_v
    = is_nothrow_default_constructible<T>::value;
  template <class T> inline constexpr bool is_nothrow_copy_constructible_v
    = is_nothrow_copy_constructible<T>::value;
  template <class T> inline constexpr bool is_nothrow_move_constructible_v
    = is_nothrow_move_constructible<T>::value;
  template <class T, class U> inline constexpr bool is_nothrow_assignable_v
    = is_nothrow_assignable<T, U>::value;
  template <class T> inline constexpr bool is_nothrow_copy_assignable_v
    = is_nothrow_copy_assignable<T>::value;
  template <class T> inline constexpr bool is_nothrow_move_assignable_v
    = is_nothrow_move_assignable<T>::value;
  template <class T, class U> inline constexpr bool is_nothrow_swappable_with_v
    = is_nothrow_swappable_with<T, U>::value;
  template <class T> inline constexpr bool is_nothrow_swappable_v
    = is_nothrow_swappable<T>::value;
  template <class T> inline constexpr bool is_nothrow_destructible_v
    = is_nothrow_destructible<T>::value;
  template <class T> inline constexpr bool has_virtual_destructor_v
    = has_virtual_destructor<T>::value;
  template <class T> inline constexpr bool has_unique_object_representations_v
    = has_unique_object_representations<T>::value;

  // [meta.unary.prop.query], type property queries
  template <class T> inline constexpr size_t alignment_of_v
    = alignment_of<T>::value;
  template <class T> inline constexpr size_t rank_v
    = rank<T>::value;
  template <class T, unsigned I = 0> inline constexpr size_t extent_v
    = extent<T, I>::value;

  // [meta.rel], type relations
  template <class T, class U> inline constexpr bool is_same_v
    = is_same<T, U>::value;
  template <class Base, class Derived> inline constexpr bool is_base_of_v
    = is_base_of<Base, Derived>::value;
  template <class From, class To> inline constexpr bool is_convertible_v
    = is_convertible<From, To>::value;
  template <class Fn, class... ArgTypes> inline constexpr bool is_invocable_v
    = is_invocable<Fn, ArgTypes...>::value;
  template <class R, class Fn, class... ArgTypes> inline constexpr bool is_invocable_r_v
    = is_invocable_r<R, Fn, ArgTypes...>::value;
  template <class Fn, class... ArgTypes> inline constexpr bool is_nothrow_invocable_v
    = is_nothrow_invocable<Fn, ArgTypes...>::value;
  template <class R, class Fn, class... ArgTypes> inline constexpr bool is_nothrow_invocable_r_v
    = is_nothrow_invocable_r<R, Fn, ArgTypes...>::value;

  // [meta.logical], logical operator traits
  template<class... B> inline constexpr bool conjunction_v = conjunction<B...>::value;
  template<class... B> inline constexpr bool disjunction_v = disjunction<B...>::value;
  template<class B> inline constexpr bool negation_v = negation<B>::value;
}
```

The behavior of a program that adds specializations for any of the
templates defined in this subclause is undefined unless otherwise
specified.

Unless otherwise specified, an incomplete type may be used to
instantiate a template in this subclause.

### Helper classes <a id="meta.help">[[meta.help]]</a>

``` cpp
namespace std {
  template <class T, T v>
  struct integral_constant {
    static constexpr T value = v;
    using value_type = T;
    using type       = integral_constant<T, v>;
    constexpr operator value_type() const noexcept { return value; }
    constexpr value_type operator()() const noexcept { return value; }
  };
}
```

The class template `integral_constant`, alias template `bool_constant`,
and its associated *typedef-name*s `true_type` and `false_type` are used
as base classes to define the interface for various type traits.

### Unary type traits <a id="meta.unary">[[meta.unary]]</a>

This subclause contains templates that may be used to query the
properties of a type at compile time.

Each of these templates shall be a `UnaryTypeTrait` ([[meta.rqmts]])
with a base characteristic of `true_type` if the corresponding condition
is `true`, otherwise `false_type`.

#### Primary type categories <a id="meta.unary.cat">[[meta.unary.cat]]</a>

The primary type categories correspond to the descriptions given in
section  [[basic.types]] of the C++standard.

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

[*Note 1*: For any given type `T`, exactly one of the primary type
categories has a `value` member that evaluates to `true`. — *end note*]

#### Composite type traits <a id="meta.unary.comp">[[meta.unary.comp]]</a>

These templates provide convenient compositions of the primary type
categories, corresponding to the descriptions given in section 
[[basic.types]].

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

#### Type properties <a id="meta.unary.prop">[[meta.unary.prop]]</a>

These templates provide access to some of the more important properties
of types.

It is unspecified whether the library defines any full or partial
specializations of any of these templates.

For all of the class templates `X` declared in this subclause,
instantiating that template with a template-argument that is a class
template specialization may result in the implicit instantiation of the
template argument if and only if the semantics of `X` require that the
argument must be a complete type.

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial ([[basic.types]], [[special]]) function call that is not an
odr-use ([[basic.def.odr]]) of `declval` in the context of the
corresponding definition notwithstanding the restrictions of 
[[declval]].

[*Note 1*: A union is a class type that can be marked with
`final`. — *end note*]

[*Example 1*:

``` cpp
is_const_v<const volatile int>     // true
is_const_v<const int*>             // false
is_const_v<const int&>             // false
is_const_v<int[3]>                 // false
is_const_v<const int[3]>           // true
```

— *end example*]

[*Example 2*:

``` cpp
remove_const_t<const volatile int>  // volatile int
remove_const_t<const int* const>    // const int*
remove_const_t<const int&>          // const int&
remove_const_t<const int[3]>        // int[3]
```

— *end example*]

[*Example 3*:

``` cpp
// Given:
struct P final { };
union U1 { };
union U2 final { };

// the following assertions hold:
static_assert(!is_final_v<int>);
static_assert(is_final_v<P>);
static_assert(!is_final_v<U1>);
static_assert(is_final_v<U2>);
```

— *end example*]

The predicate condition for a template specialization
`is_constructible<T, Args...>` shall be satisfied if and only if the
following variable definition would be well-formed for some invented
variable `t`:

``` cpp
T t(declval<Args>()...);
```

[*Note 2*: These tokens are never interpreted as a function
declaration. — *end note*]

Access checking is performed as if in a context unrelated to `T` and any
of the `Args`. Only the validity of the immediate context of the
variable initialization is considered.

[*Note 3*: The evaluation of the initialization can result in side
effects such as the instantiation of class template specializations and
function template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*]

The predicate condition for a template specialization
`has_unique_object_representations<T>` shall be satisfied if and only
if:

- `T` is trivially copyable, and
- any two objects of type `T` with the same value have the same object
  representation, where two objects of array or non-union class type are
  considered to have the same value if their respective sequences of
  direct subobjects have the same values, and two objects of union type
  are considered to have the same value if they have the same active
  member and the corresponding members have the same value.

The set of scalar types for which this condition holds is
*implementation-defined*.

[*Note 4*: If a type has padding bits, the condition does not hold;
otherwise, the condition holds true for unsigned integral
types. — *end note*]

### Type property queries <a id="meta.unary.prop.query">[[meta.unary.prop.query]]</a>

This subclause contains templates that may be used to query properties
of types at compile time.

Each of these templates shall be a `UnaryTypeTrait` ([[meta.rqmts]])
with a base characteristic of `integral_constant<size_t, Value>`.

[*Example 1*:

``` cpp
// the following assertions hold:
assert(rank_v<int> == 0);
assert(rank_v<int[2]> == 1);
assert(rank_v<int[][4]> == 2);
```

— *end example*]

[*Example 2*:

``` cpp
// the following assertions hold:
assert(extent_v<int> == 0);
assert(extent_v<int[2]> == 2);
assert(extent_v<int[2][4]> == 2);
assert(extent_v<int[][4]> == 0);
assert((extent_v<int, 1>) == 0);
assert((extent_v<int[2], 1>) == 0);
assert((extent_v<int[2][4], 1>) == 4);
assert((extent_v<int[][4], 1>) == 4);
```

— *end example*]

### Relationships between types <a id="meta.rel">[[meta.rel]]</a>

This subclause contains templates that may be used to query
relationships between types at compile time.

Each of these templates shall be a `BinaryTypeTrait` ([[meta.rqmts]])
with a base characteristic of `true_type` if the corresponding condition
is true, otherwise `false_type`.

[*Note 1*: Base classes that are private, protected, or ambiguous are,
nonetheless, base classes. — *end note*]

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial ([[basic.types]], [[special]]) function call that is not an
odr-use ([[basic.def.odr]]) of `declval` in the context of the
corresponding definition notwithstanding the restrictions of 
[[declval]].

[*Example 1*:

``` cpp
struct B {};
struct B1 : B {};
struct B2 : B {};
struct D : private B1, private B2 {};

is_base_of_v<B, D>         // true
is_base_of_v<const B, D>   // true
is_base_of_v<B, const D>   // true
is_base_of_v<B, const B>   // true
is_base_of_v<D, B>         // false
is_base_of_v<B&, D&>       // false
is_base_of_v<B[3], D[3]>   // false
is_base_of_v<int, int>     // false
```

— *end example*]

The predicate condition for a template specialization
`is_convertible<From, To>` shall be satisfied if and only if the return
expression in the following code would be well-formed, including any
implicit conversions to the return type of the function:

``` cpp
To test() {
  return declval<From>();
}
```

[*Note 2*: This requirement gives well defined results for reference
types, void types, array types, and function types. — *end note*]

Access checking is performed in a context unrelated to `To` and `From`.
Only the validity of the immediate context of the *expression* of the
`return` statement (including initialization of the returned object or
reference) is considered.

[*Note 3*: The initialization can result in side effects such as the
instantiation of class template specializations and function template
specializations, the generation of implicitly-defined functions, and so
on. Such side effects are not in the “immediate context” and can result
in the program being ill-formed. — *end note*]

### Transformations between types <a id="meta.trans">[[meta.trans]]</a>

Each of the templates in this subclause shall be a
`TransformationTrait` ([[meta.rqmts]]).

#### Const-volatile modifications <a id="meta.trans.cv">[[meta.trans.cv]]</a>

[*Example 1*: `remove_const_t<const volatile int>` evaluates to
`volatile int`, whereas `remove_const_t<const int*>` evaluates to
`const int*`. — *end example*]

#### Reference modifications <a id="meta.trans.ref">[[meta.trans.ref]]</a>

[*Note 1*: This rule reflects the semantics of reference collapsing (
[[dcl.ref]]). — *end note*]

#### Sign modifications <a id="meta.trans.sign">[[meta.trans.sign]]</a>

#### Array modifications <a id="meta.trans.arr">[[meta.trans.arr]]</a>

[*Note 1*: For multidimensional arrays, only the first array dimension
is removed. For a type “array of `const U`”, the resulting type is
`const U`. — *end note*]

[*Example 1*:

``` cpp
// the following assertions hold:
assert((is_same_v<remove_extent_t<int>, int>));
assert((is_same_v<remove_extent_t<int[2]>, int>));
assert((is_same_v<remove_extent_t<int[2][3]>, int[3]>));
assert((is_same_v<remove_extent_t<int[][3]>, int[3]>));
```

— *end example*]

[*Example 2*:

``` cpp
// the following assertions hold:
assert((is_same_v<remove_all_extents_t<int>, int>));
assert((is_same_v<remove_all_extents_t<int[2]>, int>));
assert((is_same_v<remove_all_extents_t<int[2][3]>, int>));
assert((is_same_v<remove_all_extents_t<int[][3]>, int>));
```

— *end example*]

#### Pointer modifications <a id="meta.trans.ptr">[[meta.trans.ptr]]</a>

#### Other transformations <a id="meta.trans.other">[[meta.trans.other]]</a>

[*Note 1*: This behavior is similar to the lvalue-to-rvalue (
[[conv.lval]]), array-to-pointer ([[conv.array]]), and
function-to-pointer ([[conv.func]]) conversions applied when an lvalue
expression is used as an rvalue, but also strips cv-qualifiers from
class types in order to more closely model by-value argument
passing. — *end note*]

[*Note 2*:

A typical implementation would define `aligned_storage` as:

``` cpp
template <size_t Len, size_t Alignment>
struct aligned_storage {
  typedef struct {
    alignas(Alignment) unsigned char __data[Len];
  } type;
};
```

— *end note*]

It is *implementation-defined* whether any extended alignment is
supported ([[basic.align]]).

Note A: For the `common_type` trait applied to a parameter pack `T` of
types, the member `type` shall be either defined or not present as
follows:

- If `sizeof...(T)` is zero, there shall be no member `type`.
- If `sizeof...(T)` is one, let `T0` denote the sole type constituting
  the pack `T`. The member *typedef-name* `type` shall denote the same
  type, if any, as `common_type_t<T0, T0>`; otherwise there shall be no
  member `type`.
- If `sizeof...(T)` is two, let the first and second types constituting
  `T` be denoted by `T1` and `T2`, respectively, and let `D1` and `D2`
  denote the same types as `decay_t<T1>` and `decay_t<T2>`,
  respectively.
  - If `is_same_v<T1, D1>` is `false` or `is_same_v<T2, D2>` is `false`,
    let `C` denote the same type, if any, as `common_type_t<D1, D2>`.
  - Otherwise, let `C` denote the same type, if any, as
    ``` cpp
    decay_t<decltype(false ? declval<D1>() : declval<D2>())>
    ```

    \[*Note 4*: This will not apply if there is a specialization
    `common_type<D1, D2>`. — *end note*]

  In either case, the member *typedef-name* `type` shall denote the same
  type, if any, as `C`. Otherwise, there shall be no member `type`.
- If `sizeof...(T)` is greater than two, let `T1`, `T2`, and `R`,
  respectively, denote the first, second, and (pack of) remaining types
  constituting `T`. Let `C` denote the same type, if any, as
  `common_type_t<T1, T2>`. If there is such a type `C`, the member
  *typedef-name* `type` shall denote the same type, if any, as
  `common_type_t<C, R...>`. Otherwise, there shall be no member `type`.

Note B: Notwithstanding the provisions of [[meta.type.synop]], and
pursuant to [[namespace.std]], a program may specialize
`common_type<T1, T2>` for types `T1` and `T2` such that
`is_same_v<T1, decay_t<T1>>` and `is_same_v<T2, decay_t<T2>>` are each
`true`.

[*Note 3*: Such specializations are needed when only explicit
conversions are desired between the template arguments. — *end note*]

Such a specialization need not have a member named `type`, but if it
does, that member shall be a *typedef-name* for an accessible and
unambiguous cv-unqualified non-reference type `C` to which each of the
types `T1` and `T2` is explicitly convertible. Moreover,
`common_type_t<T1, T2>` shall denote the same type, if any, as does
`common_type_t<T2, T1>`. No diagnostic is required for a violation of
this Note’s rules.

[*Example 1*:

Given these definitions:

``` cpp
using PF1 = bool  (&)();
using PF2 = short (*)(long);

struct S {
  operator PF2() const;
  double operator()(char, int&);
  void fn(long) const;
  char data;
};

using PMF = void (S::*)(long) const;
using PMD = char  S::*;
```

the following assertions will hold:

``` cpp
static_assert(is_same_v<invoke_result_t<S, int>, short>);
static_assert(is_same_v<invoke_result_t<S&, unsigned char, int&>, double>);
static_assert(is_same_v<invoke_result_t<PF1>, bool>);
static_assert(is_same_v<invoke_result_t<PMF, unique_ptr<S>, int>, void>);
static_assert(is_same_v<invoke_result_t<PMD, S>, char&&>);
static_assert(is_same_v<invoke_result_t<PMD, const S*>, const char&>);
```

— *end example*]

### Logical operator traits <a id="meta.logical">[[meta.logical]]</a>

This subclause describes type traits for applying logical operators to
other type traits.

``` cpp
template<class... B> struct conjunction : see below { };
```

The class template `conjunction` forms the logical conjunction of its
template type arguments.

For a specialization `conjunction<B1, ..., BN>`, if there is a template
type argument `Bi` for which `bool(Bi::value)` is `false`, then
instantiating `conjunction<B1, ..., BN>::value` does not require the
instantiation of `Bj::value` for `j > i`.

[*Note 1*: This is analogous to the short-circuiting behavior of the
built-in operator `&&`. — *end note*]

Every template type argument for which `Bi::value` is instantiated shall
be usable as a base class and shall have a member `value` which is
convertible to `bool`, is not hidden, and is unambiguously available in
the type.

The specialization `conjunction<B1, ..., BN>` has a public and
unambiguous base that is either

- the first type `Bi` in the list `true_type, B1, ..., BN` for which
  `bool(Bi::value)` is `false`, or
- if there is no such `Bi`, the last type in the list.

[*Note 2*: This means a specialization of `conjunction` does not
necessarily inherit from either `true_type` or
`false_type`. — *end note*]

The member names of the base class, other than `conjunction` and
`operator=`, shall not be hidden and shall be unambiguously available in
`conjunction`.

``` cpp
template<class... B> struct disjunction : see below { };
```

The class template `disjunction` forms the logical disjunction of its
template type arguments.

For a specialization `disjunction<B1, ..., BN>`, if there is a template
type argument `Bi` for which `bool(Bi::value)` is `true`, then
instantiating `disjunction<B1, ..., BN>::value` does not require the
instantiation of `Bj::value` for `j > i`.

[*Note 3*: This is analogous to the short-circuiting behavior of the
built-in operator `||`. — *end note*]

Every template type argument for which `Bi::value` is instantiated shall
be usable as a base class and shall have a member `value` which is
convertible to `bool`, is not hidden, and is unambiguously available in
the type.

The specialization `disjunction<B1, ..., BN>` has a public and
unambiguous base that is either

- the first type `Bi` in the list `false_type, B1, ..., BN` for which
  `bool(Bi::value)` is `true`, or
- if there is no such `Bi`, the last type in the list.

[*Note 4*: This means a specialization of `disjunction` does not
necessarily inherit from either `true_type` or
`false_type`. — *end note*]

The member names of the base class, other than `disjunction` and
`operator=`, shall not be hidden and shall be unambiguously available in
`disjunction`.

``` cpp
template<class B> struct negation : see below { };
```

The class template `negation` forms the logical negation of its template
type argument. The type `negation<B>` is a `UnaryTypeTrait` with a base
characteristic of `bool_constant<!bool(B::value)>`.

## Compile-time rational arithmetic <a id="ratio">[[ratio]]</a>

### In general <a id="ratio.general">[[ratio.general]]</a>

This subclause describes the ratio library. It provides a class template
`ratio` which exactly represents any finite rational number with a
numerator and denominator representable by compile-time constants of
type `intmax_t`.

Throughout this subclause, the names of template parameters are used to
express type requirements. If a template parameter is named `R1` or
`R2`, and the template argument is not a specialization of the `ratio`
template, the program is ill-formed.

### Header `<ratio>` synopsis <a id="ratio.syn">[[ratio.syn]]</a>

``` cpp
namespace std {
  // [ratio.ratio], class template ratio
  template <intmax_t N, intmax_t D = 1> class ratio;

  // [ratio.arithmetic], ratio arithmetic
  template <class R1, class R2> using ratio_add = see below;
  template <class R1, class R2> using ratio_subtract = see below;
  template <class R1, class R2> using ratio_multiply = see below;
  template <class R1, class R2> using ratio_divide = see below;

  // [ratio.comparison], ratio comparison
  template <class R1, class R2> struct ratio_equal;
  template <class R1, class R2> struct ratio_not_equal;
  template <class R1, class R2> struct ratio_less;
  template <class R1, class R2> struct ratio_less_equal;
  template <class R1, class R2> struct ratio_greater;
  template <class R1, class R2> struct ratio_greater_equal;

  template <class R1, class R2>
    inline constexpr bool ratio_equal_v = ratio_equal<R1, R2>::value;
  template <class R1, class R2>
    inline constexpr bool ratio_not_equal_v = ratio_not_equal<R1, R2>::value;
  template <class R1, class R2>
    inline constexpr bool ratio_less_v = ratio_less<R1, R2>::value;
  template <class R1, class R2>
    inline constexpr bool ratio_less_equal_v = ratio_less_equal<R1, R2>::value;
  template <class R1, class R2>
    inline constexpr bool ratio_greater_v = ratio_greater<R1, R2>::value;
  template <class R1, class R2>
    inline constexpr bool ratio_greater_equal_v = ratio_greater_equal<R1, R2>::value;

  // [ratio.si], convenience SI typedefs
  using yocto = ratio<1, 1'000'000'000'000'000'000'000'000>;  // see below
  using zepto = ratio<1,     1'000'000'000'000'000'000'000>;  // see below
  using atto  = ratio<1,         1'000'000'000'000'000'000>;
  using femto = ratio<1,             1'000'000'000'000'000>;
  using pico  = ratio<1,                 1'000'000'000'000>;
  using nano  = ratio<1,                     1'000'000'000>;
  using micro = ratio<1,                         1'000'000>;
  using milli = ratio<1,                             1'000>;
  using centi = ratio<1,                               100>;
  using deci  = ratio<1,                                10>;
  using deca  = ratio<                               10, 1>;
  using hecto = ratio<                              100, 1>;
  using kilo  = ratio<                            1'000, 1>;
  using mega  = ratio<                        1'000'000, 1>;
  using giga  = ratio<                    1'000'000'000, 1>;
  using tera  = ratio<                1'000'000'000'000, 1>;
  using peta  = ratio<            1'000'000'000'000'000, 1>;
  using exa   = ratio<        1'000'000'000'000'000'000, 1>;
  using zetta = ratio<    1'000'000'000'000'000'000'000, 1>;  // see below
  using yotta = ratio<1'000'000'000'000'000'000'000'000, 1>;  // see below
}
```

### Class template `ratio` <a id="ratio.ratio">[[ratio.ratio]]</a>

``` cpp
namespace std {
  template <intmax_t N, intmax_t D = 1>
  class ratio {
  public:
    static constexpr intmax_t num;
    static constexpr intmax_t den;
    using type = ratio<num, den>;
  };
}
```

If the template argument `D` is zero or the absolute values of either of
the template arguments `N` and `D` is not representable by type
`intmax_t`, the program is ill-formed.

[*Note 1*: These rules ensure that infinite ratios are avoided and that
for any negative input, there exists a representable value of its
absolute value which is positive. In a two’s complement representation,
this excludes the most negative value. — *end note*]

The static data members `num` and `den` shall have the following values,
where `gcd` represents the greatest common divisor of the absolute
values of `N` and `D`:

- `num` shall have the value `sign(N) * sign(D) * abs(N) / gcd`.
- `den` shall have the value `abs(D) / gcd`.

### Arithmetic on `ratio`s <a id="ratio.arithmetic">[[ratio.arithmetic]]</a>

Each of the alias templates `ratio_add`, `ratio_subtract`,
`ratio_multiply`, and `ratio_divide` denotes the result of an arithmetic
computation on two `ratio`s `R1` and `R2`. With `X` and `Y` computed (in
the absence of arithmetic overflow) as specified by Table 
[[tab:ratio.arithmetic]], each alias denotes a `ratio<U, V>` such that
`U` is the same as `ratio<X, Y>::num` and `V` is the same as
`ratio<X, Y>::den`.

If it is not possible to represent `U` or `V` with `intmax_t`, the
program is ill-formed. Otherwise, an implementation should yield correct
values of `U` and `V`. If it is not possible to represent `X` or `Y`
with `intmax_t`, the program is ill-formed unless the implementation
yields correct values of `U` and `V`.

**Table: Expressions used to perform ratio arithmetic**

|                          |                       |                     |
| ------------------------ | --------------------- | ------------------- |
| `ratio_add<R1, R2>`      | `R1::num * R2::den +` | `R1::den * R2::den` |
|                          | `R2::num * R1::den`   |                     |
| `ratio_subtract<R1, R2>` | `R1::num * R2::den -` | `R1::den * R2::den` |
|                          | `R2::num * R1::den`   |                     |
| `ratio_multiply<R1, R2>` | `R1::num * R2::num`   | `R1::den * R2::den` |
| `ratio_divide<R1, R2>`   | `R1::num * R2::den`   | `R1::den * R2::num` |


[*Example 1*:

``` cpp
static_assert(ratio_add<ratio<1, 3>, ratio<1, 6>>::num == 1, "1/3+1/6 == 1/2");
static_assert(ratio_add<ratio<1, 3>, ratio<1, 6>>::den == 2, "1/3+1/6 == 1/2");
static_assert(ratio_multiply<ratio<1, 3>, ratio<3, 2>>::num == 1, "1/3*3/2 == 1/2");
static_assert(ratio_multiply<ratio<1, 3>, ratio<3, 2>>::den == 2, "1/3*3/2 == 1/2");

// The following cases may cause the program to be ill-formed under some implementations
static_assert(ratio_add<ratio<1, INT_MAX>, ratio<1, INT_MAX>>::num == 2,
  "1/MAX+1/MAX == 2/MAX");
static_assert(ratio_add<ratio<1, INT_MAX>, ratio<1, INT_MAX>>::den == INT_MAX,
  "1/MAX+1/MAX == 2/MAX");
static_assert(ratio_multiply<ratio<1, INT_MAX>, ratio<INT_MAX, 2>>::num == 1,
  "1/MAX * MAX/2 == 1/2");
static_assert(ratio_multiply<ratio<1, INT_MAX>, ratio<INT_MAX, 2>>::den == 2,
  "1/MAX * MAX/2 == 1/2");
```

— *end example*]

### Comparison of `ratio`s <a id="ratio.comparison">[[ratio.comparison]]</a>

``` cpp
template <class R1, class R2>
  struct ratio_equal : bool_constant<R1::num == R2::num && R1::den == R2::den> { };
```

``` cpp
template <class R1, class R2>
  struct ratio_not_equal : bool_constant<!ratio_equal_v<R1, R2>> { };
```

``` cpp
template <class R1, class R2>
  struct ratio_less : bool_constant<see below> { };
```

If `R1::num` × `R2::den` is less than `R2::num` × `R1::den`,
`ratio_less<R1, R2>` shall be derived from `bool_constant<true>`;
otherwise it shall be derived from `bool_constant<false>`.
Implementations may use other algorithms to compute this relationship to
avoid overflow. If overflow occurs, the program is ill-formed.

``` cpp
template <class R1, class R2>
  struct ratio_less_equal : bool_constant<!ratio_less_v<R2, R1>> { };
```

``` cpp
template <class R1, class R2>
  struct ratio_greater : bool_constant<ratio_less_v<R2, R1>> { };
```

``` cpp
template <class R1, class R2>
  struct ratio_greater_equal : bool_constant<!ratio_less_v<R1, R2>> { };
```

### SI types for `ratio` <a id="ratio.si">[[ratio.si]]</a>

For each of the *typedef-name*s `yocto`, `zepto`, `zetta`, and `yotta`,
if both of the constants used in its specification are representable by
`intmax_t`, the typedef shall be defined; if either of the constants is
not representable by `intmax_t`, the typedef shall not be defined.

## Time utilities <a id="time">[[time]]</a>

### In general <a id="time.general">[[time.general]]</a>

This subclause describes the chrono library ([[time.syn]]) and various
C functions ([[ctime.syn]]) that provide generally useful time
utilities.

### Header `<chrono>` synopsis <a id="time.syn">[[time.syn]]</a>

``` cpp
namespace std {
  namespace chrono {
    // [time.duration], class template duration
    template <class Rep, class Period = ratio<1>> class duration;

    // [time.point], class template time_point
    template <class Clock, class Duration = typename Clock::duration> class time_point;
  }

  // [time.traits.specializations], common_type specializations
  template <class Rep1, class Period1, class Rep2, class Period2>
    struct common_type<chrono::duration<Rep1, Period1>,
                       chrono::duration<Rep2, Period2>>;

  template <class Clock, class Duration1, class Duration2>
    struct common_type<chrono::time_point<Clock, Duration1>,
                       chrono::time_point<Clock, Duration2>>;

  namespace chrono {
    // [time.traits], customization traits
    template <class Rep> struct treat_as_floating_point;
    template <class Rep> struct duration_values;
    template <class Rep> inline constexpr bool treat_as_floating_point_v
      = treat_as_floating_point<Rep>::value;

    // [time.duration.nonmember], duration arithmetic
    template <class Rep1, class Period1, class Rep2, class Period2>
      common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
      constexpr operator+(const duration<Rep1, Period1>& lhs,
                          const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
      common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
      constexpr operator-(const duration<Rep1, Period1>& lhs,
                          const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period, class Rep2>
      duration<common_type_t<Rep1, Rep2>, Period>
      constexpr operator*(const duration<Rep1, Period>& d, const Rep2& s);
    template <class Rep1, class Rep2, class Period>
      duration<common_type_t<Rep1, Rep2>, Period>
      constexpr operator*(const Rep1& s, const duration<Rep2, Period>& d);
    template <class Rep1, class Period, class Rep2>
      duration<common_type_t<Rep1, Rep2>, Period>
      constexpr operator/(const duration<Rep1, Period>& d, const Rep2& s);
    template <class Rep1, class Period1, class Rep2, class Period2>
      common_type_t<Rep1, Rep2>
      constexpr operator/(const duration<Rep1, Period1>& lhs,
                          const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period, class Rep2>
      duration<common_type_t<Rep1, Rep2>, Period>
      constexpr operator%(const duration<Rep1, Period>& d, const Rep2& s);
    template <class Rep1, class Period1, class Rep2, class Period2>
      common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
      constexpr operator%(const duration<Rep1, Period1>& lhs,
                          const duration<Rep2, Period2>& rhs);

    // [time.duration.comparisons], duration comparisons
    template <class Rep1, class Period1, class Rep2, class Period2>
      constexpr bool operator==(const duration<Rep1, Period1>& lhs,
                                const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
      constexpr bool operator!=(const duration<Rep1, Period1>& lhs,
                                const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
      constexpr bool operator< (const duration<Rep1, Period1>& lhs,
                                const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
      constexpr bool operator<=(const duration<Rep1, Period1>& lhs,
                                const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
      constexpr bool operator> (const duration<Rep1, Period1>& lhs,
                                const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Rep2, class Period2>
      constexpr bool operator>=(const duration<Rep1, Period1>& lhs,
                                const duration<Rep2, Period2>& rhs);

    // [time.duration.cast], duration_cast
    template <class ToDuration, class Rep, class Period>
      constexpr ToDuration duration_cast(const duration<Rep, Period>& d);
    template <class ToDuration, class Rep, class Period>
      constexpr ToDuration floor(const duration<Rep, Period>& d);
    template <class ToDuration, class Rep, class Period>
      constexpr ToDuration ceil(const duration<Rep, Period>& d);
    template <class ToDuration, class Rep, class Period>
      constexpr ToDuration round(const duration<Rep, Period>& d);

    // convenience typedefs
    using nanoseconds  = duration<signed integer type of at least 64 bits, nano>;
    using microseconds = duration<signed integer type of at least 55 bits, micro>;
    using milliseconds = duration<signed integer type of at least 45 bits, milli>;
    using seconds      = duration<signed integer type of at least 35 bits>;
    using minutes      = duration<signed integer type of at least 29 bits, ratio<  60>>;
    using hours        = duration<signed integer type of at least 23 bits, ratio<3600>>;

    // [time.point.nonmember], time_point arithmetic
    template <class Clock, class Duration1, class Rep2, class Period2>
      constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
      operator+(const time_point<Clock, Duration1>& lhs,
                const duration<Rep2, Period2>& rhs);
    template <class Rep1, class Period1, class Clock, class Duration2>
      constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
      operator+(const duration<Rep1, Period1>& lhs,
                const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Rep2, class Period2>
      constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
      operator-(const time_point<Clock, Duration1>& lhs,
                const duration<Rep2, Period2>& rhs);
    template <class Clock, class Duration1, class Duration2>
      constexpr common_type_t<Duration1, Duration2>
      operator-(const time_point<Clock, Duration1>& lhs,
                const time_point<Clock, Duration2>& rhs);

    // [time.point.comparisons], time_point comparisons
    template <class Clock, class Duration1, class Duration2>
       constexpr bool operator==(const time_point<Clock, Duration1>& lhs,
                                 const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
       constexpr bool operator!=(const time_point<Clock, Duration1>& lhs,
                                 const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
       constexpr bool operator< (const time_point<Clock, Duration1>& lhs,
                                 const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
       constexpr bool operator<=(const time_point<Clock, Duration1>& lhs,
                                 const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
       constexpr bool operator> (const time_point<Clock, Duration1>& lhs,
                                 const time_point<Clock, Duration2>& rhs);
    template <class Clock, class Duration1, class Duration2>
       constexpr bool operator>=(const time_point<Clock, Duration1>& lhs,
                                 const time_point<Clock, Duration2>& rhs);

    // [time.point.cast], time_point_cast
    template <class ToDuration, class Clock, class Duration>
      constexpr time_point<Clock, ToDuration>
      time_point_cast(const time_point<Clock, Duration>& t);
    template <class ToDuration, class Clock, class Duration>
      constexpr time_point<Clock, ToDuration>
      floor(const time_point<Clock, Duration>& tp);
    template <class ToDuration, class Clock, class Duration>
      constexpr time_point<Clock, ToDuration>
      ceil(const time_point<Clock, Duration>& tp);
    template <class ToDuration, class Clock, class Duration>
      constexpr time_point<Clock, ToDuration>
      round(const time_point<Clock, Duration>& tp);

    // [time.duration.alg], specialized algorithms
    template <class Rep, class Period>
      constexpr duration<Rep, Period> abs(duration<Rep, Period> d);

    // [time.clock], clocks
    class system_clock;
    class steady_clock;
    class high_resolution_clock;
  }

  inline namespace literals {
    inline namespace chrono_literals {
      // [time.duration.literals], suffixes for duration literals
      constexpr chrono::hours                                operator""h(unsigned long long);
      constexpr chrono::duration<unspecified, ratio<3600,1>> operator""h(long double);
      constexpr chrono::minutes                              operator""min(unsigned long long);
      constexpr chrono::duration<unspecified, ratio<60,1>>   operator""min(long double);
      constexpr chrono::seconds                              operator""s(unsigned long long);
      constexpr chrono::duration<unspecified> \itcorr[-1]               operator""s(long double);
      constexpr chrono::milliseconds                         operator""ms(unsigned long long);
      constexpr chrono::duration<unspecified, milli>          operator""ms(long double);
      constexpr chrono::microseconds                         operator""us(unsigned long long);
      constexpr chrono::duration<unspecified, micro>         operator""us(long double);
      constexpr chrono::nanoseconds                          operator""ns(unsigned long long);
      constexpr chrono::duration<unspecified, nano>          operator""ns(long double);
    }
  }

  namespace chrono {
    using namespace literals::chrono_literals;
  }
}
```

### Clock requirements <a id="time.clock.req">[[time.clock.req]]</a>

A clock is a bundle consisting of a `duration`, a `time_point`, and a
function `now()` to get the current `time_point`. The origin of the
clock’s `time_point` is referred to as the clock’s *epoch*. A clock
shall meet the requirements in Table  [[tab:time.clock]].

In Table  [[tab:time.clock]] `C1` and `C2` denote clock types. `t1` and
`t2` are values returned by `C1::now()` where the call returning `t1`
happens before ([[intro.multithread]]) the call returning `t2` and both
of these calls occur before `C1::time_point::max()`.

[*Note 1*: This means `C1` did not wrap around between `t1` and
`t2`. — *end note*]

[*Note 2*: The relative difference in durations between those reported
by a given clock and the SI definition is a measure of the quality of
implementation. — *end note*]

A type `TC` meets the `TrivialClock` requirements if:

- `TC` satisfies the `Clock` requirements ([[time.clock.req]]),
- the types `TC::rep`, `TC::duration`, and `TC::time_point` satisfy the
  requirements of `EqualityComparable` (Table 
  [[tab:equalitycomparable]]), `LessThanComparable` (Table 
  [[tab:lessthancomparable]]), `DefaultConstructible` (Table 
  [[tab:defaultconstructible]]), `CopyConstructible` (Table 
  [[tab:copyconstructible]]), `CopyAssignable` (Table 
  [[tab:copyassignable]]), `Destructible` (Table  [[tab:destructible]]),
  and the requirements of numeric types ([[numeric.requirements]]).
  \[*Note 5*: This means, in particular, that operations on these types
  will not throw exceptions. — *end note*]
- lvalues of the types `TC::rep`, `TC::duration`, and `TC::time_point`
  are swappable ([[swappable.requirements]]),
- the function `TC::now()` does not throw exceptions, and
- the type `TC::time_point::clock` meets the `TrivialClock`
  requirements, recursively.

### Time-related traits <a id="time.traits">[[time.traits]]</a>

#### `treat_as_floating_point` <a id="time.traits.is_fp">[[time.traits.is_fp]]</a>

``` cpp
template <class Rep> struct treat_as_floating_point
  : is_floating_point<Rep> { };
```

The `duration` template uses the `treat_as_floating_point` trait to help
determine if a `duration` object can be converted to another `duration`
with a different tick `period`. If `treat_as_floating_point_v<Rep>` is
`true`, then implicit conversions are allowed among `duration`s.
Otherwise, the implicit convertibility depends on the tick `period`s of
the `duration`s.

[*Note 1*: The intention of this trait is to indicate whether a given
class behaves like a floating-point type, and thus allows division of
one value by another with acceptable loss of precision. If
`treat_as_floating_point_v<Rep>` is `false`, `Rep` will be treated as if
it behaved like an integral type for the purpose of these
conversions. — *end note*]

#### `duration_values` <a id="time.traits.duration_values">[[time.traits.duration_values]]</a>

``` cpp
template <class Rep>
struct duration_values {
public:
  static constexpr Rep zero();
  static constexpr Rep min();
  static constexpr Rep max();
};
```

The `duration` template uses the `duration_values` trait to construct
special values of the durations representation (`Rep`). This is done
because the representation might be a class type with behavior which
requires some other implementation to return these special values. In
that case, the author of that class type should specialize
`duration_values` to return the indicated values.

``` cpp
static constexpr Rep zero();
```

*Returns:* `Rep(0)`.

[*Note 1*: `Rep(0)` is specified instead of `Rep()` because `Rep()` may
have some other meaning, such as an uninitialized value. — *end note*]

*Remarks:* The value returned shall be the additive identity.

``` cpp
static constexpr Rep min();
```

*Returns:* `numeric_limits<Rep>::lowest()`.

*Remarks:* The value returned shall compare less than or equal to
`zero()`.

``` cpp
static constexpr Rep max();
```

*Returns:* `numeric_limits<Rep>::max()`.

*Remarks:* The value returned shall compare greater than `zero()`.

#### Specializations of `common_type` <a id="time.traits.specializations">[[time.traits.specializations]]</a>

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
struct common_type<chrono::duration<Rep1, Period1>, chrono::duration<Rep2, Period2>> {
  using type = chrono::duration<common_type_t<Rep1, Rep2>, see below>;
};
```

The `period` of the `duration` indicated by this specialization of
`common_type` shall be the greatest common divisor of `Period1` and
`Period2`.

[*Note 1*: This can be computed by forming a ratio of the greatest
common divisor of `Period1::num` and `Period2::num` and the least common
multiple of `Period1::den` and `Period2::den`. — *end note*]

[*Note 2*: The `typedef` name `type` is a synonym for the `duration`
with the largest tick `period` possible where both `duration` arguments
will convert to it without requiring a division operation. The
representation of this type is intended to be able to hold any value
resulting from this conversion with no truncation error, although
floating-point durations may have round-off errors. — *end note*]

``` cpp
template <class Clock, class Duration1, class Duration2>
struct common_type<chrono::time_point<Clock, Duration1>, chrono::time_point<Clock, Duration2>> {
  using type = chrono::time_point<Clock, common_type_t<Duration1, Duration2>>;
};
```

The common type of two `time_point` types is a `time_point` with the
same clock as the two types and the common type of their two
`duration`s.

### Class template `duration` <a id="time.duration">[[time.duration]]</a>

A `duration` type measures time between two points in time
(`time_point`s). A `duration` has a representation which holds a count
of ticks and a tick period. The tick period is the amount of time which
occurs from one tick to the next, in units of seconds. It is expressed
as a rational constant using the template `ratio`.

``` cpp
template <class Rep, class Period = ratio<1>>
class duration {
public:
  using rep    = Rep;
  using period = typename Period::type;
private:
  rep rep_;  // exposition only
public:
  // [time.duration.cons], construct/copy/destroy
  constexpr duration() = default;
  template <class Rep2>
      constexpr explicit duration(const Rep2& r);
  template <class Rep2, class Period2>
     constexpr duration(const duration<Rep2, Period2>& d);
  ~duration() = default;
  duration(const duration&) = default;
  duration& operator=(const duration&) = default;

  // [time.duration.observer], observer
  constexpr rep count() const;

  // [time.duration.arithmetic], arithmetic
  constexpr common_type_t<duration> operator+() const;
  constexpr common_type_t<duration> operator-() const;
  constexpr duration& operator++();
  constexpr duration  operator++(int);
  constexpr duration& operator--();
  constexpr duration  operator--(int);

  constexpr duration& operator+=(const duration& d);
  constexpr duration& operator-=(const duration& d);

  constexpr duration& operator*=(const rep& rhs);
  constexpr duration& operator/=(const rep& rhs);
  constexpr duration& operator%=(const rep& rhs);
  constexpr duration& operator%=(const duration& rhs);

  // [time.duration.special], special values
  static constexpr duration zero();
  static constexpr duration min();
  static constexpr duration max();
};
```

`Rep` shall be an arithmetic type or a class emulating an arithmetic
type. If `duration` is instantiated with a `duration` type as the
argument for the template parameter `Rep`, the program is ill-formed.

If `Period` is not a specialization of `ratio`, the program is
ill-formed. If `Period::num` is not positive, the program is ill-formed.

Members of `duration` shall not throw exceptions other than those thrown
by the indicated operations on their representations.

The defaulted copy constructor of duration shall be a constexpr function
if and only if the required initialization of the member `rep_` for copy
and move, respectively, would satisfy the requirements for a constexpr
function.

[*Example 1*:

``` cpp
duration<long, ratio<60>> d0;       // holds a count of minutes using a long
duration<long long, milli> d1;      // holds a count of milliseconds using a long long
duration<double, ratio<1, 30>>  d2; // holds a count with a tick period of $\frac{1}{30}$ of a second
                                    // (30 Hz) using a double
```

— *end example*]

#### `duration` constructors <a id="time.duration.cons">[[time.duration.cons]]</a>

``` cpp
template <class Rep2>
  constexpr explicit duration(const Rep2& r);
```

*Remarks:* This constructor shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `rep` and

- `treat_as_floating_point_v<rep>` is `true` or
- `treat_as_floating_point_v<Rep2>` is `false`.

[*Example 1*:

``` cpp
duration<int, milli> d(3);          // OK
duration<int, milli> d(3.5);        // error
```

— *end example*]

*Effects:* Constructs an object of type `duration`.

*Postconditions:* `count() == static_cast<rep>(r)`.

``` cpp
template <class Rep2, class Period2>
  constexpr duration(const duration<Rep2, Period2>& d);
```

*Remarks:* This constructor shall not participate in overload resolution
unless no overflow is induced in the conversion and
`treat_as_floating_point_v<rep>` is `true` or both
`ratio_divide<Period2, period>::den` is `1` and
`treat_as_floating_point_v<Rep2>` is `false`.

[*Note 1*: This requirement prevents implicit truncation error when
converting between integral-based `duration` types. Such a construction
could easily lead to confusion about the value of the
`duration`. — *end note*]

[*Example 2*:

``` cpp
duration<int, milli> ms(3);
duration<int, micro> us = ms;       // OK
duration<int, milli> ms2 = us;      // error
```

— *end example*]

*Effects:* Constructs an object of type `duration`, constructing `rep_`
from  
`duration_cast<duration>(d).count()`.

#### `duration` observer <a id="time.duration.observer">[[time.duration.observer]]</a>

``` cpp
constexpr rep count() const;
```

*Returns:* `rep_`.

#### `duration` arithmetic <a id="time.duration.arithmetic">[[time.duration.arithmetic]]</a>

``` cpp
constexpr common_type_t<duration> operator+() const;
```

*Returns:* `common_type_t<duration>(*this)`.

``` cpp
constexpr common_type_t<duration> operator-() const;
```

*Returns:* `common_type_t<duration>(-rep_)`.

``` cpp
constexpr duration& operator++();
```

*Effects:* As if by `++rep_`.

*Returns:* `*this`.

``` cpp
constexpr duration operator++(int);
```

*Returns:* `duration(rep_++)`.

``` cpp
constexpr duration& operator--();
```

*Effects:* As if by `–rep_`.

*Returns:* `*this`.

``` cpp
constexpr duration operator--(int);
```

*Returns:* `duration(rep_--)`.

``` cpp
constexpr duration& operator+=(const duration& d);
```

*Effects:* As if by: `rep_ += d.count();`

*Returns:* `*this`.

``` cpp
constexpr duration& operator-=(const duration& d);
```

*Effects:* As if by: `rep_ -= d.count();`

*Returns:* `*this`.

``` cpp
constexpr duration& operator*=(const rep& rhs);
```

*Effects:* As if by: `rep_ *= rhs;`

*Returns:* `*this`.

``` cpp
constexpr duration& operator/=(const rep& rhs);
```

*Effects:* As if by: `rep_ /= rhs;`

*Returns:* `*this`.

``` cpp
constexpr duration& operator%=(const rep& rhs);
```

*Effects:* As if by: `rep_ %= rhs;`

*Returns:* `*this`.

``` cpp
constexpr duration& operator%=(const duration& rhs);
```

*Effects:* As if by: `rep_ %= rhs.count();`

*Returns:* `*this`.

#### `duration` special values <a id="time.duration.special">[[time.duration.special]]</a>

``` cpp
static constexpr duration zero();
```

*Returns:* `duration(duration_values<rep>::zero())`.

``` cpp
static constexpr duration min();
```

*Returns:* `duration(duration_values<rep>::min())`.

``` cpp
static constexpr duration max();
```

*Returns:* `duration(duration_values<rep>::max())`.

#### `duration` non-member arithmetic <a id="time.duration.nonmember">[[time.duration.nonmember]]</a>

In the function descriptions that follow, `CD` represents the return
type of the function. `CR(A, B)` represents `common_type_t<A, B>`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator+(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(CD(lhs).count() + CD(rhs).count())`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator-(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(CD(lhs).count() - CD(rhs).count())`.

``` cpp
template <class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator*(const duration<Rep1, Period>& d, const Rep2& s);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `CR(Rep1, Rep2)`.

*Returns:* `CD(CD(d).count() * s)`.

``` cpp
template <class Rep1, class Rep2, class Period>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator*(const Rep1& s, const duration<Rep2, Period>& d);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep1` is implicitly convertible to `CR(Rep1, Rep2)`.

*Returns:* `d * s`.

``` cpp
template <class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator/(const duration<Rep1, Period>& d, const Rep2& s);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `CR(Rep1, Rep2)` and `Rep2`
is not a specialization of `duration`.

*Returns:* `CD(CD(d).count() / s)`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<Rep1, Rep2>
  operator/(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(lhs).count() / CD(rhs).count()`.

``` cpp
template <class Rep1, class Period, class Rep2>
  constexpr duration<common_type_t<Rep1, Rep2>, Period>
  operator%(const duration<Rep1, Period>& d, const Rep2& s);
```

*Remarks:* This operator shall not participate in overload resolution
unless `Rep2` is implicitly convertible to `CR(Rep1, Rep2)` and `Rep2`
is not a specialization of `duration`.

*Returns:* `CD(CD(d).count() % s)`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr common_type_t<duration<Rep1, Period1>, duration<Rep2, Period2>>
  operator%(const duration<Rep1, Period1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* `CD(CD(lhs).count() % CD(rhs).count())`.

#### `duration` comparisons <a id="time.duration.comparisons">[[time.duration.comparisons]]</a>

In the function descriptions that follow, `CT` represents
`common_type_t<A, B>`, where `A` and `B` are the types of the two
arguments to the function.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator==(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* *`CT`*`(lhs).count() == `*`CT`*`(rhs).count()`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator!=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<(const duration<Rep1, Period1>& lhs,
                           const duration<Rep2, Period2>& rhs);
```

*Returns:* *`CT`*`(lhs).count() < `*`CT`*`(rhs).count()`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator<=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>(const duration<Rep1, Period1>& lhs,
                           const duration<Rep2, Period2>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class Rep1, class Period1, class Rep2, class Period2>
  constexpr bool operator>=(const duration<Rep1, Period1>& lhs,
                            const duration<Rep2, Period2>& rhs);
```

*Returns:* `!(lhs < rhs)`.

#### `duration_cast` <a id="time.duration.cast">[[time.duration.cast]]</a>

``` cpp
template <class ToDuration, class Rep, class Period>
  constexpr ToDuration duration_cast(const duration<Rep, Period>& d);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`.

*Returns:* Let `CF` be
`ratio_divide<Period, typename ToDuration::period>`, and `CR` be
`common_type<` `typename ToDuration::rep, Rep, intmax_t>::type`.

- If `CF::num == 1` and `CF::den == 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(d.count()))
  ```
- otherwise, if `CF::num != 1` and `CF::den == 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) * static_cast<CR>(CF::num)))
  ```
- otherwise, if `CF::num == 1` and `CF::den != 1`, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) / static_cast<CR>(CF::den)))
  ```
- otherwise, returns
  ``` cpp
  ToDuration(static_cast<typename ToDuration::rep>(
    static_cast<CR>(d.count()) * static_cast<CR>(CF::num) / static_cast<CR>(CF::den)))
  ```

[*Note 1*: This function does not use any implicit conversions; all
conversions are done with `static_cast`. It avoids multiplications and
divisions when it is known at compile time that one or more arguments
is 1. Intermediate computations are carried out in the widest
representation and only converted to the destination representation at
the final step. — *end note*]

``` cpp
template <class ToDuration, class Rep, class Period>
  constexpr ToDuration floor(const duration<Rep, Period>& d);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`.

*Returns:* The greatest result `t` representable in `ToDuration` for
which `t <= d`.

``` cpp
template <class ToDuration, class Rep, class Period>
  constexpr ToDuration ceil(const duration<Rep, Period>& d);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`.

*Returns:* The least result `t` representable in `ToDuration` for which
`t >= d`.

``` cpp
template <class ToDuration, class Rep, class Period>
  constexpr ToDuration round(const duration<Rep, Period>& d);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`, and
`treat_as_floating_point_v<typename ToDuration::rep>` is `false`.

*Returns:* The value of `ToDuration` that is closest to `d`. If there
are two closest values, then return the value `t` for which
`t % 2 == 0`.

#### Suffixes for duration literals <a id="time.duration.literals">[[time.duration.literals]]</a>

This section describes literal suffixes for constructing duration
literals. The suffixes `h`, `min`, `s`, `ms`, `us`, `ns` denote duration
values of the corresponding types `hours`, `minutes`, `seconds`,
`milliseconds`, `microseconds`, and `nanoseconds` respectively if they
are applied to integral literals.

If any of these suffixes are applied to a floating-point literal the
result is a `chrono::duration` literal with an unspecified
floating-point representation.

If any of these suffixes are applied to an integer literal and the
resulting `chrono::duration` value cannot be represented in the result
type because of overflow, the program is ill-formed.

[*Example 1*:

The following code shows some duration literals.

``` cpp
using namespace std::chrono_literals;
auto constexpr aday=24h;
auto constexpr lesson=45min;
auto constexpr halfanhour=0.5h;
```

— *end example*]

``` cpp
constexpr chrono::hours                                 operator""h(unsigned long long hours);
constexpr chrono::duration<unspecified, ratio<3600, 1>> operator""h(long double hours);
```

*Returns:* A `duration` literal representing `hours` hours.

``` cpp
constexpr chrono::minutes                             operator""min(unsigned long long minutes);
constexpr chrono::duration<unspecified, ratio<60, 1>> operator""min(long double minutes);
```

*Returns:* A `duration` literal representing `minutes` minutes.

``` cpp
constexpr chrono::seconds  \itcorr             operator""s(unsigned long long sec);
constexpr chrono::duration<unspecified> operator""s(long double sec);
```

*Returns:* A `duration` literal representing `sec` seconds.

[*Note 1*: The same suffix `s` is used for `basic_string` but there is
no conflict, since duration suffixes apply to numbers and string literal
suffixes apply to character array literals. — *end note*]

``` cpp
constexpr chrono::milliseconds                 operator""ms(unsigned long long msec);
constexpr chrono::duration<unspecified, milli> operator""ms(long double msec);
```

*Returns:* A `duration` literal representing `msec` milliseconds.

``` cpp
constexpr chrono::microseconds                 operator""us(unsigned long long usec);
constexpr chrono::duration<unspecified, micro> operator""us(long double usec);
```

*Returns:* A `duration` literal representing `usec` microseconds.

``` cpp
constexpr chrono::nanoseconds                 operator""ns(unsigned long long nsec);
constexpr chrono::duration<unspecified, nano> operator""ns(long double nsec);
```

*Returns:* A `duration` literal representing `nsec` nanoseconds.

#### `duration` algorithms <a id="time.duration.alg">[[time.duration.alg]]</a>

``` cpp
template <class Rep, class Period>
  constexpr duration<Rep, Period> abs(duration<Rep, Period> d);
```

*Remarks:* This function shall not participate in overload resolution
unless `numeric_limits<Rep>::is_signed` is `true`.

*Returns:* If `d >= d.zero()`, return `d`, otherwise return `-d`.

### Class template `time_point` <a id="time.point">[[time.point]]</a>

``` cpp
template <class Clock, class Duration = typename Clock::duration>
class time_point {
public:
  using clock    = Clock;
  using duration = Duration;
  using rep      = typename duration::rep;
  using period   = typename duration::period;
private:
  duration d_;  // exposition only

public:
  // [time.point.cons], construct
  constexpr time_point();  // has value epoch
  constexpr explicit time_point(const duration& d);  // same as time_point() + d
  template <class Duration2>
    constexpr time_point(const time_point<clock, Duration2>& t);

  // [time.point.observer], observer
  constexpr duration time_since_epoch() const;

  // [time.point.arithmetic], arithmetic
  constexpr time_point& operator+=(const duration& d);
  constexpr time_point& operator-=(const duration& d);

  // [time.point.special], special values
  static constexpr time_point min();
  static constexpr time_point max();
};
```

`Clock` shall meet the Clock requirements ([[time.clock.req]]).

If `Duration` is not an instance of `duration`, the program is
ill-formed.

#### `time_point` constructors <a id="time.point.cons">[[time.point.cons]]</a>

``` cpp
constexpr time_point();
```

*Effects:* Constructs an object of type `time_point`, initializing `d_`
with `duration::zero()`. Such a `time_point` object represents the
epoch.

``` cpp
constexpr explicit time_point(const duration& d);
```

*Effects:* Constructs an object of type `time_point`, initializing `d_`
with `d`. Such a `time_point` object represents the epoch `+ d`.

``` cpp
template <class Duration2>
  constexpr time_point(const time_point<clock, Duration2>& t);
```

*Remarks:* This constructor shall not participate in overload resolution
unless `Duration2` is implicitly convertible to `duration`.

*Effects:* Constructs an object of type `time_point`, initializing `d_`
with `t.time_since_epoch()`.

#### `time_point` observer <a id="time.point.observer">[[time.point.observer]]</a>

``` cpp
constexpr duration time_since_epoch() const;
```

*Returns:* `d_`.

#### `time_point` arithmetic <a id="time.point.arithmetic">[[time.point.arithmetic]]</a>

``` cpp
constexpr time_point& operator+=(const duration& d);
```

*Effects:* As if by: `d_ += d;`

*Returns:* `*this`.

``` cpp
constexpr time_point& operator-=(const duration& d);
```

*Effects:* As if by: `d_ -= d;`

*Returns:* `*this`.

#### `time_point` special values <a id="time.point.special">[[time.point.special]]</a>

``` cpp
static constexpr time_point min();
```

*Returns:* `time_point(duration::min())`.

``` cpp
static constexpr time_point max();
```

*Returns:* `time_point(duration::max())`.

#### `time_point` non-member arithmetic <a id="time.point.nonmember">[[time.point.nonmember]]</a>

``` cpp
template <class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
  operator+(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* *`CT`*`(lhs.time_since_epoch() + rhs)`, where *`CT`* is the
type of the return value.

``` cpp
template <class Rep1, class Period1, class Clock, class Duration2>
  constexpr time_point<Clock, common_type_t<duration<Rep1, Period1>, Duration2>>
  operator+(const duration<Rep1, Period1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `rhs + lhs`.

``` cpp
template <class Clock, class Duration1, class Rep2, class Period2>
  constexpr time_point<Clock, common_type_t<Duration1, duration<Rep2, Period2>>>
  operator-(const time_point<Clock, Duration1>& lhs, const duration<Rep2, Period2>& rhs);
```

*Returns:* *`CT`*`(lhs.time_since_epoch() - rhs)`, where *`CT`* is the
type of the return value.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr common_type_t<Duration1, Duration2>
  operator-(const time_point<Clock, Duration1>& lhs, const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() - rhs.time_since_epoch()`.

#### `time_point` comparisons <a id="time.point.comparisons">[[time.point.comparisons]]</a>

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator==(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() == rhs.time_since_epoch()`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator!=(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(lhs == rhs)`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator<(const time_point<Clock, Duration1>& lhs,
                           const time_point<Clock, Duration2>& rhs);
```

*Returns:* `lhs.time_since_epoch() < rhs.time_since_epoch()`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator<=(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(rhs < lhs)`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator>(const time_point<Clock, Duration1>& lhs,
                           const time_point<Clock, Duration2>& rhs);
```

*Returns:* `rhs < lhs`.

``` cpp
template <class Clock, class Duration1, class Duration2>
  constexpr bool operator>=(const time_point<Clock, Duration1>& lhs,
                            const time_point<Clock, Duration2>& rhs);
```

*Returns:* `!(lhs < rhs)`.

#### `time_point_cast` <a id="time.point.cast">[[time.point.cast]]</a>

``` cpp
template <class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration>
  time_point_cast(const time_point<Clock, Duration>& t);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`.

*Returns:*

``` cpp
time_point<Clock, ToDuration>(duration_cast<ToDuration>(t.time_since_epoch()))
```

``` cpp
template <class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration>
  floor(const time_point<Clock, Duration>& tp);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`.

*Returns:*
`time_point<Clock, ToDuration>(floor<ToDuration>(tp.time_since_epoch()))`.

``` cpp
template <class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration>
  ceil(const time_point<Clock, Duration>& tp);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`.

*Returns:*
`time_point<Clock, ToDuration>(ceil<ToDuration>(tp.time_since_epoch()))`.

``` cpp
template <class ToDuration, class Clock, class Duration>
  constexpr time_point<Clock, ToDuration>
  round(const time_point<Clock, Duration>& tp);
```

*Remarks:* This function shall not participate in overload resolution
unless `ToDuration` is a specialization of `duration`, and
`treat_as_floating_point_v<typename ToDuration::rep>` is `false`.

*Returns:*
`time_point<Clock, ToDuration>(round<ToDuration>(tp.time_since_epoch()))`.

### Clocks <a id="time.clock">[[time.clock]]</a>

The types defined in this subclause shall satisfy the `TrivialClock`
requirements ([[time.clock.req]]).

#### Class `system_clock` <a id="time.clock.system">[[time.clock.system]]</a>

Objects of class `system_clock` represent wall clock time from the
system-wide realtime clock.

``` cpp
class system_clock {
public:
  using rep        = see below;
  using period     = ratio<unspecified, unspecified{}>;
  using duration   = chrono::duration<rep, period>;
  using time_point = chrono::time_point<system_clock>;
  static constexpr bool is_steady = unspecified;

  static time_point now() noexcept;

  // Map to C API
  static time_t      to_time_t  (const time_point& t) noexcept;
  static time_point  from_time_t(time_t t) noexcept;
};
```

``` cpp
using system_clock::rep = unspecified;
```

*Requires:*
`system_clock::duration::min() < system_clock::duration::zero()` shall
be `true`.  

[*Note 1*: This implies that `rep` is a signed type. — *end note*]

``` cpp
static time_t to_time_t(const time_point& t) noexcept;
```

*Returns:* A `time_t` object that represents the same point in time as
`t` when both values are restricted to the coarser of the precisions of
`time_t` and `time_point`. It is *implementation-defined* whether values
are rounded or truncated to the required precision.

``` cpp
static time_point from_time_t(time_t t) noexcept;
```

*Returns:* A `time_point` object that represents the same point in time
as `t` when both values are restricted to the coarser of the precisions
of `time_t` and `time_point`. It is *implementation-defined* whether
values are rounded or truncated to the required precision.

#### Class `steady_clock` <a id="time.clock.steady">[[time.clock.steady]]</a>

Objects of class `steady_clock` represent clocks for which values of
`time_point` never decrease as physical time advances and for which
values of `time_point` advance at a steady rate relative to real time.
That is, the clock may not be adjusted.

``` cpp
class steady_clock {
public:
  using rep        = unspecified;
  using period     = ratio<unspecified, unspecified{}>;
  using duration   = chrono::duration<rep, period>;
  using time_point = chrono::time_point<unspecified, duration>;
  static constexpr bool is_steady = true;

  static time_point now() noexcept;
};
```

#### Class `high_resolution_clock` <a id="time.clock.hires">[[time.clock.hires]]</a>

Objects of class `high_resolution_clock` represent clocks with the
shortest tick period. `high_resolution_clock` may be a synonym for
`system_clock` or `steady_clock`.

``` cpp
class high_resolution_clock {
public:
  using rep        = unspecified;
  using period     = ratio<unspecified, unspecified{}>;
  using duration   = chrono::duration<rep, period>;
  using time_point = chrono::time_point<unspecified, duration>;
  static constexpr bool is_steady = unspecified;

  static time_point now() noexcept;
};
```

### Header `<ctime>` synopsis <a id="ctime.syn">[[ctime.syn]]</a>

``` cpp
#define NULL see [support.types.nullptr]
#define CLOCKS_PER_SEC see below
#define TIME_UTC see below

namespace std {
  using size_t = see [support.types.layout];
  using clock_t = see below;
  using time_t = see below;

  struct timespec;
  struct tm;

  clock_t clock();
  double difftime(time_t time1, time_t time0);
  time_t mktime(struct tm* timeptr);
  time_t time(time_t* timer);
  int timespec_get(timespec* ts, int base);
  char* asctime(const struct tm* timeptr);
  char* ctime(const time_t* timer);
  struct tm* gmtime(const time_t* timer);
  struct tm* localtime(const time_t* timer);
  size_t strftime(char* s, size_t maxsize, const char* format, const struct tm* timeptr);
}
```

The contents of the header `<ctime>` are the same as the C standard
library header `<time.h>`. [^3]

The functions `asctime`, `ctime`, `gmtime`, and `localtime` are not
required to avoid data races ([[res.on.data.races]]).

ISO C 7.27.

## Class `type_index` <a id="type.index">[[type.index]]</a>

### Header `<typeindex>` synopsis <a id="type.index.synopsis">[[type.index.synopsis]]</a>

``` cpp
namespace std {
  class type_index;
  template <class T> struct hash;
  template<> struct hash<type_index>;
}
```

### `type_index` overview <a id="type.index.overview">[[type.index.overview]]</a>

``` cpp
namespace std {
  class type_index {
  public:
    type_index(const type_info& rhs) noexcept;
    bool operator==(const type_index& rhs) const noexcept;
    bool operator!=(const type_index& rhs) const noexcept;
    bool operator< (const type_index& rhs) const noexcept;
    bool operator<= (const type_index& rhs) const noexcept;
    bool operator> (const type_index& rhs) const noexcept;
    bool operator>= (const type_index& rhs) const noexcept;
    size_t hash_code() const noexcept;
    const char* name() const noexcept;
  private:
    const type_info* target;    // exposition only
    // Note that the use of a pointer here, rather than a reference,
    // means that the default copy/move constructor and assignment
    // operators will be provided and work as expected.
  };
}
```

The class `type_index` provides a simple wrapper for `type_info` which
can be used as an index type in associative containers (
[[associative]]) and in unordered associative containers ([[unord]]).

### `type_index` members <a id="type.index.members">[[type.index.members]]</a>

``` cpp
type_index(const type_info& rhs) noexcept;
```

*Effects:* Constructs a `type_index` object, the equivalent of
`target = &rhs`.

``` cpp
bool operator==(const type_index& rhs) const noexcept;
```

*Returns:* `*target == *rhs.target`.

``` cpp
bool operator!=(const type_index& rhs) const noexcept;
```

*Returns:* `*target != *rhs.target`.

``` cpp
bool operator<(const type_index& rhs) const noexcept;
```

*Returns:* `target->before(*rhs.target)`.

``` cpp
bool operator<=(const type_index& rhs) const noexcept;
```

*Returns:* `!rhs.target->before(*target)`.

``` cpp
bool operator>(const type_index& rhs) const noexcept;
```

*Returns:* `rhs.target->before(*target)`.

``` cpp
bool operator>=(const type_index& rhs) const noexcept;
```

*Returns:* `!target->before(*rhs.target)`.

``` cpp
size_t hash_code() const noexcept;
```

*Returns:* `target->hash_code()`.

``` cpp
const char* name() const noexcept;
```

*Returns:* `target->name()`.

### Hash support <a id="type.index.hash">[[type.index.hash]]</a>

``` cpp
template <> struct hash<type_index>;
```

For an object `index` of type `type_index`, `hash<type_index>()(index)`
shall evaluate to the same result as `index.hash_code()`.

## Execution policies <a id="execpol">[[execpol]]</a>

### In general <a id="execpol.general">[[execpol.general]]</a>

This subclause describes classes that are *execution policy* types. An
object of an execution policy type indicates the kinds of parallelism
allowed in the execution of an algorithm and expresses the consequent
requirements on the element access functions.

[*Example 1*:

``` cpp
using namespace std;
vector<int> v = ...;

// standard sequential sort
sort(v.begin(), v.end());

// explicitly sequential sort
sort(execution::seq, v.begin(), v.end());

// permitting parallel execution
sort(execution::par, v.begin(), v.end());

// permitting vectorization as well
sort(execution::par_unseq, v.begin(), v.end());
```

— *end example*]

[*Note 1*: Because different parallel architectures may require
idiosyncratic parameters for efficient execution, implementations may
provide additional execution policies to those described in this
standard as extensions. — *end note*]

### Header `<execution>` synopsis <a id="execution.syn">[[execution.syn]]</a>

``` cpp
namespace std {
  // [execpol.type], execution policy type trait
  template<class T> struct is_execution_policy;
  template<class T> inline constexpr bool is_execution_policy_v = is_execution_policy<T>::value;
}

namespace std::execution {
  // [execpol.seq], sequenced execution policy
  class sequenced_policy;

  // [execpol.par], parallel execution policy
  class parallel_policy;

  // [execpol.parunseq], parallel and unsequenced execution policy
  class parallel_unsequenced_policy;

  // [execpol.objects], execution policy objects
  inline constexpr sequenced_policy            seq{ unspecified };
  inline constexpr parallel_policy             par{ unspecified };
  inline constexpr parallel_unsequenced_policy par_unseq{ unspecified };
}
```

### Execution policy type trait <a id="execpol.type">[[execpol.type]]</a>

``` cpp
template<class T> struct is_execution_policy { see below };
```

`is_execution_policy` can be used to detect execution policies for the
purpose of excluding function signatures from otherwise ambiguous
overload resolution participation.

`is_execution_policy<T>` shall be a `UnaryTypeTrait` with a base
characteristic of `true_type` if `T` is the type of a standard or
*implementation-defined* execution policy, otherwise `false_type`.

[*Note 1*: This provision reserves the privilege of creating
non-standard execution policies to the library
implementation. — *end note*]

The behavior of a program that adds specializations for
`is_execution_policy` is undefined.

### Sequenced execution policy <a id="execpol.seq">[[execpol.seq]]</a>

``` cpp
class execution::sequenced_policy { unspecified };
```

The class `execution::sequenced_policy` is an execution policy type used
as a unique type to disambiguate parallel algorithm overloading and
require that a parallel algorithm’s execution may not be parallelized.

During the execution of a parallel algorithm with the
`execution::sequenced_policy` policy, if the invocation of an element
access function exits via an uncaught exception, `terminate()` shall be
called.

### Parallel execution policy <a id="execpol.par">[[execpol.par]]</a>

``` cpp
class execution::parallel_policy { unspecified };
```

The class `execution::parallel_policy` is an execution policy type used
as a unique type to disambiguate parallel algorithm overloading and
indicate that a parallel algorithm’s execution may be parallelized.

During the execution of a parallel algorithm with the
`execution::parallel_policy` policy, if the invocation of an element
access function exits via an uncaught exception, `terminate()` shall be
called.

### Parallel and unsequenced execution policy <a id="execpol.parunseq">[[execpol.parunseq]]</a>

``` cpp
class execution::parallel_unsequenced_policy { unspecified };
```

The class `execution::parallel_unsequenced_policy` is an execution
policy type used as a unique type to disambiguate parallel algorithm
overloading and indicate that a parallel algorithm’s execution may be
parallelized and vectorized.

During the execution of a parallel algorithm with the
`execution::parallel_unsequenced_policy` policy, if the invocation of an
element access function exits via an uncaught exception, `terminate()`
shall be called.

### Execution policy objects <a id="execpol.objects">[[execpol.objects]]</a>

``` cpp
inline constexpr execution::sequenced_policy            execution::seq{ unspecified };
inline constexpr execution::parallel_policy             execution::par{ unspecified };
inline constexpr execution::parallel_unsequenced_policy execution::par_unseq{ unspecified };
```

The header `<execution>` declares global objects associated with each
type of execution policy.

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[algorithms]: algorithms.md#algorithms
[algorithms.general]: algorithms.md#algorithms.general
[allocator.adaptor]: #allocator.adaptor
[allocator.adaptor.cnstr]: #allocator.adaptor.cnstr
[allocator.adaptor.members]: #allocator.adaptor.members
[allocator.adaptor.syn]: #allocator.adaptor.syn
[allocator.adaptor.types]: #allocator.adaptor.types
[allocator.globals]: #allocator.globals
[allocator.members]: #allocator.members
[allocator.requirements]: library.md#allocator.requirements
[allocator.requirements.completeness]: library.md#allocator.requirements.completeness
[allocator.tag]: #allocator.tag
[allocator.traits]: #allocator.traits
[allocator.traits.members]: #allocator.traits.members
[allocator.traits.types]: #allocator.traits.types
[allocator.uses]: #allocator.uses
[allocator.uses.construction]: #allocator.uses.construction
[allocator.uses.trait]: #allocator.uses.trait
[any]: #any
[any.assign]: #any.assign
[any.bad_any_cast]: #any.bad_any_cast
[any.class]: #any.class
[any.cons]: #any.cons
[any.modifiers]: #any.modifiers
[any.nonmembers]: #any.nonmembers
[any.observers]: #any.observers
[any.synop]: #any.synop
[arithmetic.operations]: #arithmetic.operations
[arithmetic.operations.divides]: #arithmetic.operations.divides
[arithmetic.operations.minus]: #arithmetic.operations.minus
[arithmetic.operations.modulus]: #arithmetic.operations.modulus
[arithmetic.operations.multiplies]: #arithmetic.operations.multiplies
[arithmetic.operations.negate]: #arithmetic.operations.negate
[arithmetic.operations.plus]: #arithmetic.operations.plus
[array]: containers.md#array
[associative]: containers.md#associative
[atomics.order]: atomics.md#atomics.order
[atomics.types.operations]: atomics.md#atomics.types.operations
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.stc.dynamic.deallocation]: basic.md#basic.stc.dynamic.deallocation
[basic.stc.dynamic.safety]: basic.md#basic.stc.dynamic.safety
[basic.types]: basic.md#basic.types
[bitmask.types]: library.md#bitmask.types
[bitset]: #bitset
[bitset.cons]: #bitset.cons
[bitset.hash]: #bitset.hash
[bitset.members]: #bitset.members
[bitset.operators]: #bitset.operators
[bitset.syn]: #bitset.syn
[bitwise.operations]: #bitwise.operations
[bitwise.operations.and]: #bitwise.operations.and
[bitwise.operations.not]: #bitwise.operations.not
[bitwise.operations.or]: #bitwise.operations.or
[bitwise.operations.xor]: #bitwise.operations.xor
[c.malloc]: #c.malloc
[comparisons]: #comparisons
[comparisons.equal_to]: #comparisons.equal_to
[comparisons.greater]: #comparisons.greater
[comparisons.greater_equal]: #comparisons.greater_equal
[comparisons.less]: #comparisons.less
[comparisons.less_equal]: #comparisons.less_equal
[comparisons.not_equal_to]: #comparisons.not_equal_to
[conv.array]: conv.md#conv.array
[conv.func]: conv.md#conv.func
[conv.lval]: conv.md#conv.lval
[conv.rank]: conv.md#conv.rank
[csignal.syn]: language.md#csignal.syn
[cstdlib.syn]: language.md#cstdlib.syn
[ctime.syn]: #ctime.syn
[dcl.array]: dcl.md#dcl.array
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.ref]: dcl.md#dcl.ref
[declval]: #declval
[default.allocator]: #default.allocator
[defns.const.subexpr]: library.md#defns.const.subexpr
[defns.referenceable]: library.md#defns.referenceable
[execpol]: #execpol
[execpol.general]: #execpol.general
[execpol.objects]: #execpol.objects
[execpol.par]: #execpol.par
[execpol.parunseq]: #execpol.parunseq
[execpol.seq]: #execpol.seq
[execpol.type]: #execpol.type
[execution.syn]: #execution.syn
[expr]: expr.md#expr
[expr.add]: expr.md#expr.add
[expr.alignof]: expr.md#expr.alignof
[expr.bit.and]: expr.md#expr.bit.and
[expr.call]: expr.md#expr.call
[expr.eq]: expr.md#expr.eq
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.mul]: expr.md#expr.mul
[expr.or]: expr.md#expr.or
[expr.rel]: expr.md#expr.rel
[expr.unary.op]: expr.md#expr.unary.op
[expr.xor]: expr.md#expr.xor
[forward]: #forward
[forward.iterators]: iterators.md#forward.iterators
[func.bind]: #func.bind
[func.bind.bind]: #func.bind.bind
[func.bind.isbind]: #func.bind.isbind
[func.bind.isplace]: #func.bind.isplace
[func.bind.place]: #func.bind.place
[func.def]: #func.def
[func.invoke]: #func.invoke
[func.memfn]: #func.memfn
[func.not_fn]: #func.not_fn
[func.require]: #func.require
[func.search]: #func.search
[func.search.bm]: #func.search.bm
[func.search.bmh]: #func.search.bmh
[func.search.default]: #func.search.default
[func.wrap]: #func.wrap
[func.wrap.badcall]: #func.wrap.badcall
[func.wrap.badcall.const]: #func.wrap.badcall.const
[func.wrap.func]: #func.wrap.func
[func.wrap.func.alg]: #func.wrap.func.alg
[func.wrap.func.cap]: #func.wrap.func.cap
[func.wrap.func.con]: #func.wrap.func.con
[func.wrap.func.inv]: #func.wrap.func.inv
[func.wrap.func.mod]: #func.wrap.func.mod
[func.wrap.func.nullptr]: #func.wrap.func.nullptr
[func.wrap.func.targ]: #func.wrap.func.targ
[function.objects]: #function.objects
[functional.syn]: #functional.syn
[hash.requirements]: library.md#hash.requirements
[input.iterators]: iterators.md#input.iterators
[intro.multithread]: intro.md#intro.multithread
[intseq]: #intseq
[intseq.general]: #intseq.general
[intseq.intseq]: #intseq.intseq
[intseq.make]: #intseq.make
[invalid.argument]: diagnostics.md#invalid.argument
[iostate.flags]: input.md#iostate.flags
[istream.formatted]: input.md#istream.formatted
[locale.codecvt]: localization.md#locale.codecvt
[logical.operations]: #logical.operations
[logical.operations.and]: #logical.operations.and
[logical.operations.not]: #logical.operations.not
[logical.operations.or]: #logical.operations.or
[mem.poly.allocator.class]: #mem.poly.allocator.class
[mem.poly.allocator.ctor]: #mem.poly.allocator.ctor
[mem.poly.allocator.eq]: #mem.poly.allocator.eq
[mem.poly.allocator.mem]: #mem.poly.allocator.mem
[mem.res]: #mem.res
[mem.res.class]: #mem.res.class
[mem.res.eq]: #mem.res.eq
[mem.res.global]: #mem.res.global
[mem.res.monotonic.buffer]: #mem.res.monotonic.buffer
[mem.res.monotonic.buffer.ctor]: #mem.res.monotonic.buffer.ctor
[mem.res.monotonic.buffer.mem]: #mem.res.monotonic.buffer.mem
[mem.res.pool]: #mem.res.pool
[mem.res.pool.ctor]: #mem.res.pool.ctor
[mem.res.pool.mem]: #mem.res.pool.mem
[mem.res.pool.options]: #mem.res.pool.options
[mem.res.pool.overview]: #mem.res.pool.overview
[mem.res.private]: #mem.res.private
[mem.res.public]: #mem.res.public
[mem.res.syn]: #mem.res.syn
[memory]: #memory
[memory.general]: #memory.general
[memory.syn]: #memory.syn
[meta]: #meta
[meta.help]: #meta.help
[meta.logical]: #meta.logical
[meta.rel]: #meta.rel
[meta.rqmts]: #meta.rqmts
[meta.trans]: #meta.trans
[meta.trans.arr]: #meta.trans.arr
[meta.trans.cv]: #meta.trans.cv
[meta.trans.other]: #meta.trans.other
[meta.trans.ptr]: #meta.trans.ptr
[meta.trans.ref]: #meta.trans.ref
[meta.trans.sign]: #meta.trans.sign
[meta.type.synop]: #meta.type.synop
[meta.unary]: #meta.unary
[meta.unary.cat]: #meta.unary.cat
[meta.unary.comp]: #meta.unary.comp
[meta.unary.prop]: #meta.unary.prop
[meta.unary.prop.query]: #meta.unary.prop.query
[multibyte.strings]: library.md#multibyte.strings
[namespace.std]: library.md#namespace.std
[new.delete]: language.md#new.delete
[nullablepointer.requirements]: library.md#nullablepointer.requirements
[numeric.requirements]: numerics.md#numeric.requirements
[operators]: #operators
[optional]: #optional
[optional.assign]: #optional.assign
[optional.bad.access]: #optional.bad.access
[optional.comp_with_t]: #optional.comp_with_t
[optional.ctor]: #optional.ctor
[optional.dtor]: #optional.dtor
[optional.general]: #optional.general
[optional.hash]: #optional.hash
[optional.mod]: #optional.mod
[optional.nullops]: #optional.nullops
[optional.nullopt]: #optional.nullopt
[optional.observe]: #optional.observe
[optional.optional]: #optional.optional
[optional.relops]: #optional.relops
[optional.specalg]: #optional.specalg
[optional.swap]: #optional.swap
[optional.syn]: #optional.syn
[ostream.formatted]: input.md#ostream.formatted
[out.of.range]: diagnostics.md#out.of.range
[over.match.call]: over.md#over.match.call
[over.match.class.deduct]: over.md#over.match.class.deduct
[overflow.error]: diagnostics.md#overflow.error
[pair.astuple]: #pair.astuple
[pair.piecewise]: #pair.piecewise
[pairs]: #pairs
[pairs.general]: #pairs.general
[pairs.pair]: #pairs.pair
[pairs.spec]: #pairs.spec
[pointer.traits]: #pointer.traits
[pointer.traits.functions]: #pointer.traits.functions
[pointer.traits.types]: #pointer.traits.types
[ptr.align]: #ptr.align
[ratio]: #ratio
[ratio.arithmetic]: #ratio.arithmetic
[ratio.comparison]: #ratio.comparison
[ratio.general]: #ratio.general
[ratio.ratio]: #ratio.ratio
[ratio.si]: #ratio.si
[ratio.syn]: #ratio.syn
[refwrap]: #refwrap
[refwrap.access]: #refwrap.access
[refwrap.assign]: #refwrap.assign
[refwrap.const]: #refwrap.const
[refwrap.helpers]: #refwrap.helpers
[refwrap.invoke]: #refwrap.invoke
[res.on.data.races]: library.md#res.on.data.races
[scoped.adaptor.operators]: #scoped.adaptor.operators
[smartptr]: #smartptr
[special]: special.md#special
[specialized.addressof]: #specialized.addressof
[specialized.algorithms]: #specialized.algorithms
[specialized.destroy]: #specialized.destroy
[stmt.dcl]: stmt.md#stmt.dcl
[string.classes]: strings.md#string.classes
[support.dynamic]: language.md#support.dynamic
[swappable.requirements]: library.md#swappable.requirements
[tab:copyassignable]: #tab:copyassignable
[tab:copyconstructible]: #tab:copyconstructible
[tab:defaultconstructible]: #tab:defaultconstructible
[tab:destructible]: #tab:destructible
[tab:equalitycomparable]: #tab:equalitycomparable
[tab:lessthancomparable]: #tab:lessthancomparable
[tab:moveassignable]: #tab:moveassignable
[tab:moveconstructible]: #tab:moveconstructible
[tab:optional.assign.copy]: #tab:optional.assign.copy
[tab:optional.assign.copy.templ]: #tab:optional.assign.copy.templ
[tab:optional.assign.move]: #tab:optional.assign.move
[tab:optional.assign.move.templ]: #tab:optional.assign.move.templ
[tab:optional.swap]: #tab:optional.swap
[tab:ratio.arithmetic]: #tab:ratio.arithmetic
[tab:time.clock]: #tab:time.clock
[tab:util.lib.summary]: #tab:util.lib.summary
[temp.deduct]: temp.md#temp.deduct
[template.bitset]: #template.bitset
[time]: #time
[time.clock]: #time.clock
[time.clock.hires]: #time.clock.hires
[time.clock.req]: #time.clock.req
[time.clock.steady]: #time.clock.steady
[time.clock.system]: #time.clock.system
[time.duration]: #time.duration
[time.duration.alg]: #time.duration.alg
[time.duration.arithmetic]: #time.duration.arithmetic
[time.duration.cast]: #time.duration.cast
[time.duration.comparisons]: #time.duration.comparisons
[time.duration.cons]: #time.duration.cons
[time.duration.literals]: #time.duration.literals
[time.duration.nonmember]: #time.duration.nonmember
[time.duration.observer]: #time.duration.observer
[time.duration.special]: #time.duration.special
[time.general]: #time.general
[time.point]: #time.point
[time.point.arithmetic]: #time.point.arithmetic
[time.point.cast]: #time.point.cast
[time.point.comparisons]: #time.point.comparisons
[time.point.cons]: #time.point.cons
[time.point.nonmember]: #time.point.nonmember
[time.point.observer]: #time.point.observer
[time.point.special]: #time.point.special
[time.syn]: #time.syn
[time.traits]: #time.traits
[time.traits.duration_values]: #time.traits.duration_values
[time.traits.is_fp]: #time.traits.is_fp
[time.traits.specializations]: #time.traits.specializations
[tuple]: #tuple
[tuple.apply]: #tuple.apply
[tuple.assign]: #tuple.assign
[tuple.cnstr]: #tuple.cnstr
[tuple.creation]: #tuple.creation
[tuple.elem]: #tuple.elem
[tuple.general]: #tuple.general
[tuple.helper]: #tuple.helper
[tuple.rel]: #tuple.rel
[tuple.special]: #tuple.special
[tuple.swap]: #tuple.swap
[tuple.syn]: #tuple.syn
[tuple.traits]: #tuple.traits
[tuple.tuple]: #tuple.tuple
[type.index]: #type.index
[type.index.hash]: #type.index.hash
[type.index.members]: #type.index.members
[type.index.overview]: #type.index.overview
[type.index.synopsis]: #type.index.synopsis
[uninitialized.construct.default]: #uninitialized.construct.default
[uninitialized.construct.value]: #uninitialized.construct.value
[uninitialized.copy]: #uninitialized.copy
[uninitialized.fill]: #uninitialized.fill
[uninitialized.move]: #uninitialized.move
[unique.ptr]: #unique.ptr
[unique.ptr.create]: #unique.ptr.create
[unique.ptr.dltr]: #unique.ptr.dltr
[unique.ptr.dltr.dflt]: #unique.ptr.dltr.dflt
[unique.ptr.dltr.dflt1]: #unique.ptr.dltr.dflt1
[unique.ptr.dltr.general]: #unique.ptr.dltr.general
[unique.ptr.runtime]: #unique.ptr.runtime
[unique.ptr.runtime.asgn]: #unique.ptr.runtime.asgn
[unique.ptr.runtime.ctor]: #unique.ptr.runtime.ctor
[unique.ptr.runtime.modifiers]: #unique.ptr.runtime.modifiers
[unique.ptr.runtime.observers]: #unique.ptr.runtime.observers
[unique.ptr.single]: #unique.ptr.single
[unique.ptr.single.asgn]: #unique.ptr.single.asgn
[unique.ptr.single.ctor]: #unique.ptr.single.ctor
[unique.ptr.single.dtor]: #unique.ptr.single.dtor
[unique.ptr.single.modifiers]: #unique.ptr.single.modifiers
[unique.ptr.single.observers]: #unique.ptr.single.observers
[unique.ptr.special]: #unique.ptr.special
[unord]: containers.md#unord
[unord.hash]: #unord.hash
[util.dynamic.safety]: #util.dynamic.safety
[util.smartptr]: #util.smartptr
[util.smartptr.enab]: #util.smartptr.enab
[util.smartptr.getdeleter]: #util.smartptr.getdeleter
[util.smartptr.hash]: #util.smartptr.hash
[util.smartptr.ownerless]: #util.smartptr.ownerless
[util.smartptr.shared]: #util.smartptr.shared
[util.smartptr.shared.assign]: #util.smartptr.shared.assign
[util.smartptr.shared.atomic]: #util.smartptr.shared.atomic
[util.smartptr.shared.cast]: #util.smartptr.shared.cast
[util.smartptr.shared.cmp]: #util.smartptr.shared.cmp
[util.smartptr.shared.const]: #util.smartptr.shared.const
[util.smartptr.shared.create]: #util.smartptr.shared.create
[util.smartptr.shared.dest]: #util.smartptr.shared.dest
[util.smartptr.shared.io]: #util.smartptr.shared.io
[util.smartptr.shared.mod]: #util.smartptr.shared.mod
[util.smartptr.shared.obs]: #util.smartptr.shared.obs
[util.smartptr.shared.spec]: #util.smartptr.shared.spec
[util.smartptr.weak]: #util.smartptr.weak
[util.smartptr.weak.assign]: #util.smartptr.weak.assign
[util.smartptr.weak.bad]: #util.smartptr.weak.bad
[util.smartptr.weak.const]: #util.smartptr.weak.const
[util.smartptr.weak.dest]: #util.smartptr.weak.dest
[util.smartptr.weak.mod]: #util.smartptr.weak.mod
[util.smartptr.weak.obs]: #util.smartptr.weak.obs
[util.smartptr.weak.spec]: #util.smartptr.weak.spec
[utilities]: #utilities
[utilities.general]: #utilities.general
[utility]: #utility
[utility.as_const]: #utility.as_const
[utility.exchange]: #utility.exchange
[utility.from.chars]: #utility.from.chars
[utility.swap]: #utility.swap
[utility.syn]: #utility.syn
[utility.to.chars]: #utility.to.chars
[variant]: #variant
[variant.assign]: #variant.assign
[variant.bad.access]: #variant.bad.access
[variant.ctor]: #variant.ctor
[variant.dtor]: #variant.dtor
[variant.general]: #variant.general
[variant.get]: #variant.get
[variant.hash]: #variant.hash
[variant.helper]: #variant.helper
[variant.mod]: #variant.mod
[variant.monostate]: #variant.monostate
[variant.monostate.relops]: #variant.monostate.relops
[variant.relops]: #variant.relops
[variant.specalg]: #variant.specalg
[variant.status]: #variant.status
[variant.swap]: #variant.swap
[variant.syn]: #variant.syn
[variant.traits]: #variant.traits
[variant.variant]: #variant.variant
[variant.visit]: #variant.visit

[^1]: `pointer_safety::preferred` might be returned to indicate that a
    leak detector is running so that the program can avoid spurious leak
    reports.

[^2]: Such a type is a function pointer or a class type which has a
    member `operator()` or a class type which has a conversion to a
    pointer to function.

[^3]: `strftime` supports the C conversion specifiers `C`, `D`, `e`,
    `F`, `g`, `G`, `h`, `r`, `R`, `t`, `T`, `u`, `V`, and `z`, and the
    modifiers `E` and `O`.
