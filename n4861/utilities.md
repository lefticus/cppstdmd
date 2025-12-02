# General utilities library <a id="utilities">[[utilities]]</a>

## General <a id="utilities.general">[[utilities.general]]</a>

This Clause describes utilities that are generally useful in C++
programs; some of these utilities are used by other elements of the C++
standard library. These utilities are summarized in
[[utilities.summary]].

**Table: General utilities library summary** <a id="utilities.summary">[utilities.summary]</a>

| Subclause             |                                  | Header                  |
| --------------------- | -------------------------------- | ----------------------- |
| [[utility]]           | Utility components               | `<utility>`             |
| [[intseq]]            | Compile-time integer sequences   |                         |
| [[pairs]]             | Pairs                            |                         |
| [[tuple]]             | Tuples                           | `<tuple>`               |
| [[optional]]          | Optional objects                 | `<optional>`            |
| [[variant]]           | Variants                         | `<variant>`             |
| [[any]]               | Storage for any type             | `<any>`                 |
| [[bitset]]            | Fixed-size sequences of bits     | `<bitset>`              |
| [[memory]]            | Memory                           | `<cstdlib>`, `<memory>` |
| [[smartptr]]          | Smart pointers                   | `<memory>`              |
| [[mem.res]]           | Memory resources                 | `<memory_resource>`     |
| [[allocator.adaptor]] | Scoped allocators                | `<scoped_allocator>`    |
| [[function.objects]]  | Function objects                 | `<functional>`          |
| [[meta]]              | Type traits                      | `<type_traits>`         |
| [[ratio]]             | Compile-time rational arithmetic | `<ratio>`               |
| [[type.index]]        | Type indexes                     | `<typeindex>`           |
| [[execpol]]           | Execution policies               | `<execution>`           |
| [[charconv]]          | Primitive numeric conversions    | `<charconv>`            |
| [[format]]            | Formatting                       | `<format>`              |


## Utility components <a id="utility">[[utility]]</a>

### Header `<utility>` synopsis <a id="utility.syn">[[utility.syn]]</a>

The header `<utility>` contains some basic function and class templates
that are used throughout the rest of the library.

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [utility.swap], swap
  template<class T>
    constexpr void swap(T& a, T& b) noexcept(see below);
  template<class T, size_t N>
    constexpr void swap(T (&a)[N], T (&b)[N]) noexcept(is_nothrow_swappable_v<T>);

  // [utility.exchange], exchange
  template<class T, class U = T>
    constexpr T exchange(T& obj, U&& new_val);

  // [forward], forward/move
  template<class T>
    constexpr T&& forward(remove_reference_t<T>& t) noexcept;
  template<class T>
    constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
  template<class T>
    constexpr remove_reference_t<T>&& move(T&&) noexcept;
  template<class T>
    constexpr conditional_t<
        !is_nothrow_move_constructible_v<T> && is_copy_constructible_v<T>, const T&, T&&>
      move_if_noexcept(T& x) noexcept;

  // [utility.as.const], as_const
  template<class T>
    constexpr add_const_t<T>& as_const(T& t) noexcept;
  template<class T>
    void as_const(const T&&) = delete;

  // [declval], declval
  template<class T>
    add_rvalue_reference_t<T> declval() noexcept;   // as unevaluated operand

  // [utility.intcmp], integer comparison functions
  template<class T, class U>
    constexpr bool cmp_equal(T t, U u) noexcept;
  template<class T, class U>
    constexpr bool cmp_not_equal(T t, U u) noexcept;

  template<class T, class U>
    constexpr bool cmp_less(T t, U u) noexcept;
  template<class T, class U>
    constexpr bool cmp_greater(T t, U u) noexcept;
  template<class T, class U>
    constexpr bool cmp_less_equal(T t, U u) noexcept;
  template<class T, class U>
    constexpr bool cmp_greater_equal(T t, U u) noexcept;

  template<class R, class T>
    constexpr bool in_range(T t) noexcept;

  // [intseq], compile-time integer sequences%
%
%

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
  template<class T1, class T2>
    struct pair;

  // [pairs.spec], pair specialized algorithms
  template<class T1, class T2>
    constexpr bool operator==(const pair<T1, T2>&, const pair<T1, T2>&);
  template<class T1, class T2>
    constexpr common_comparison_category_t<synth-three-way-result<T1>,
                                           synth-three-way-result<T2>>
      operator<=>(const pair<T1, T2>&, const pair<T1, T2>&);

  template<class T1, class T2>
    constexpr void swap(pair<T1, T2>& x, pair<T1, T2>& y) noexcept(noexcept(x.swap(y)));

  template<class T1, class T2>
    constexpr see below make_pair(T1&&, T2&&);

  // [pair.astuple], tuple-like access to pair
  template<class T> struct tuple_size;
  template<size_t I, class T> struct tuple_element;

  template<class T1, class T2> struct tuple_size<pair<T1, T2>>;
  template<size_t I, class T1, class T2> struct tuple_element<I, pair<T1, T2>>;

  template<size_t I, class T1, class T2>
    constexpr tuple_element_t<I, pair<T1, T2>>& get(pair<T1, T2>&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr tuple_element_t<I, pair<T1, T2>>&& get(pair<T1, T2>&&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr const tuple_element_t<I, pair<T1, T2>>& get(const pair<T1, T2>&) noexcept;
  template<size_t I, class T1, class T2>
    constexpr const tuple_element_t<I, pair<T1, T2>>&& get(const pair<T1, T2>&&) noexcept;
  template<class T1, class T2>
    constexpr T1& get(pair<T1, T2>& p) noexcept;
  template<class T1, class T2>
    constexpr const T1& get(const pair<T1, T2>& p) noexcept;
  template<class T1, class T2>
    constexpr T1&& get(pair<T1, T2>&& p) noexcept;
  template<class T1, class T2>
    constexpr const T1&& get(const pair<T1, T2>&& p) noexcept;
  template<class T2, class T1>
    constexpr T2& get(pair<T1, T2>& p) noexcept;
  template<class T2, class T1>
    constexpr const T2& get(const pair<T1, T2>& p) noexcept;
  template<class T2, class T1>
    constexpr T2&& get(pair<T1, T2>&& p) noexcept;
  template<class T2, class T1>
    constexpr const T2&& get(const pair<T1, T2>&& p) noexcept;

  // [pair.piecewise], pair piecewise construction
  struct piecewise_construct_t {
    explicit piecewise_construct_t() = default;
  };
  inline constexpr piecewise_construct_t piecewise_construct{};
  template<class... Types> class tuple;         // defined in <tuple>

  // in-place construction%
%
%
%
%
%

  struct in_place_t {
    explicit in_place_t() = default;
  };
  inline constexpr in_place_t in_place{};

  template<class T>
    struct in_place_type_t {
      explicit in_place_type_t() = default;
    };
  template<class T> inline constexpr in_place_type_t<T> in_place_type{};

  template<size_t I>
    struct in_place_index_t {
      explicit in_place_index_t() = default;
    };
  template<size_t I> inline constexpr in_place_index_t<I> in_place_index{};
}
```

### `swap` <a id="utility.swap">[[utility.swap]]</a>

``` cpp
template<class T>
  constexpr void swap(T& a, T& b) noexcept(see below);
```

*Constraints:* `is_move_constructible_v<T>` is `true` and
`is_move_assignable_v<T>` is `true`.

*Preconditions:* Type `T` meets the *Cpp17MoveConstructible*
([[cpp17.moveconstructible]]) and *Cpp17MoveAssignable*
([[cpp17.moveassignable]]) requirements.

*Effects:* Exchanges values stored in two locations.

*Remarks:* This function is a designated customization
point [[namespace.std]]. The expression inside `noexcept` is equivalent
to:

``` cpp
is_nothrow_move_constructible_v<T> && is_nothrow_move_assignable_v<T>
```

``` cpp
template<class T, size_t N>
  constexpr void swap(T (&a)[N], T (&b)[N]) noexcept(is_nothrow_swappable_v<T>);
```

*Constraints:* `is_swappable_v<T>` is `true`.

*Preconditions:* `a[i]` is swappable with [[swappable.requirements]]
`b[i]` for all `i` in the range \[`0`, `N`).

*Effects:* As if by `swap_ranges(a, a + N, b)`.

### `exchange` <a id="utility.exchange">[[utility.exchange]]</a>

``` cpp
template<class T, class U = T>
  constexpr T exchange(T& obj, U&& new_val);
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
signal-safe [[support.signal]].

``` cpp
template<class T> constexpr T&& forward(remove_reference_t<T>& t) noexcept;
template<class T> constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
```

*Mandates:* For the second overload, `is_lvalue_reference_v<T>` is
`false`.

*Returns:* `static_cast<T&&>(t)`.

[*Example 1*:

``` cpp
template<class T, class A1, class A2>
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
template<class T> constexpr remove_reference_t<T>&& move(T&& t) noexcept;
```

*Returns:* `static_cast<remove_reference_t<T>&&>(t)`.

[*Example 2*:

``` cpp
template<class T, class A1>
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
template<class T> constexpr conditional_t<
    !is_nothrow_move_constructible_v<T> && is_copy_constructible_v<T>, const T&, T&&>
  move_if_noexcept(T& x) noexcept;
```

*Returns:* `std::move(x)`.

### Function template `as_const` <a id="utility.as.const">[[utility.as.const]]</a>

``` cpp
template<class T> constexpr add_const_t<T>& as_const(T& t) noexcept;
```

*Returns:* `t`.

### Function template `declval` <a id="declval">[[declval]]</a>

The library provides the function template `declval` to simplify the
definition of expressions which occur as unevaluated operands
[[expr.prop]].

``` cpp
template<class T> add_rvalue_reference_t<T> declval() noexcept;    // as unevaluated operand
```

*Mandates:* This function is not odr-used [[basic.def.odr]].

*Remarks:* The template parameter `T` of `declval` may be an incomplete
type.

[*Example 1*:

``` cpp
template<class To, class From> decltype(static_cast<To>(declval<From>())) convert(From&&);
```

declares a function template `convert` which only participates in
overloading if the type `From` can be explicitly converted to type `To`.
For another example see class template `common_type`
[[meta.trans.other]].

— *end example*]

### Integer comparison functions <a id="utility.intcmp">[[utility.intcmp]]</a>

``` cpp
template<class T, class U>
  constexpr bool cmp_equal(T t, U u) noexcept;
```

*Mandates:* Both `T` and `U` are standard integer types or extended
integer types [[basic.fundamental]].

*Effects:* Equivalent to:

``` cpp
using UT = make_unsigned_t<T>;
using UU = make_unsigned_t<U>;
if constexpr (is_signed_v<T> == is_signed_v<U>)
  return t == u;
else if constexpr (is_signed_v<T>)
  return t < 0 ? false : UT(t) == u;
else
  return u < 0 ? false : t == UU(u);
```

``` cpp
template<class T, class U>
  constexpr bool cmp_not_equal(T t, U u) noexcept;
```

*Effects:* Equivalent to: `return !cmp_equal(t, u);`

``` cpp
template<class T, class U>
  constexpr bool cmp_less(T t, U u) noexcept;
```

*Mandates:* Both `T` and `U` are standard integer types or extended
integer types [[basic.fundamental]].

*Effects:* Equivalent to:

``` cpp
using UT = make_unsigned_t<T>;
using UU = make_unsigned_t<U>;
if constexpr (is_signed_v<T> == is_signed_v<U>)
  return t < u;
else if constexpr (is_signed_v<T>)
  return t < 0 ? true : UT(t) < u;
else
  return u < 0 ? false : t < UU(u);
```

``` cpp
template<class T, class U>
  constexpr bool cmp_greater(T t, U u) noexcept;
```

*Effects:* Equivalent to: `return cmp_less(u, t);`

``` cpp
template<class T, class U>
  constexpr bool cmp_less_equal(T t, U u) noexcept;
```

*Effects:* Equivalent to: `return !cmp_greater(t, u);`

``` cpp
template<class T, class U>
  constexpr bool cmp_greater_equal(T t, U u) noexcept;
```

*Effects:* Equivalent to: `return !cmp_less(t, u);`

``` cpp
template<class R, class T>
  constexpr bool in_range(T t) noexcept;
```

*Mandates:* Both `T` and `R` are standard integer types or extended
integer types [[basic.fundamental]].

*Effects:* Equivalent to:

``` cpp
return cmp_greater_equal(t, numeric_limits<R>::min()) &&
       cmp_less_equal(t, numeric_limits<R>::max());
```

[*Note 1*: These function templates cannot be used to compare `byte`,
`char`, `char8_t`, `char16_t`, `char32_t`, `wchar_t`, and
`bool`. — *end note*]

## Compile-time integer sequences <a id="intseq">[[intseq]]</a>

### In general <a id="intseq.general">[[intseq.general]]</a>

The library provides a class template that can represent an integer
sequence. When used as an argument to a function template the template
parameter pack defining the sequence can be deduced and used in a pack
expansion.

[*Note 1*: The `index_sequence` alias template is provided for the
common case of an integer sequence of type `size_t`; see also
[[tuple.apply]]. — *end note*]

### Class template `integer_sequence` <a id="intseq.intseq">[[intseq.intseq]]</a>

``` cpp
namespace std {
  template<class T, T... I> struct integer_sequence {
    using value_type = T;
    static constexpr size_t size() noexcept { return sizeof...(I); }
  };
}
```

*Mandates:* `T` is an integer type.

### Alias template `make_integer_sequence` <a id="intseq.make">[[intseq.make]]</a>

``` cpp
template<class T, T N>
  using make_integer_sequence = integer_sequence<T, see below{}>;
```

*Mandates:* `N` ≥ 0.

The alias template `make_integer_sequence` denotes a specialization of
`integer_sequence` with `N` non-type template arguments. The type
`make_integer_sequence<T, N>` is an alias for the type
`integer_sequence<T, 0, 1, ..., N-1>`.

[*Note 1*: `make_integer_sequence<int, 0>` is an alias for the type
`integer_sequence<int>`. — *end note*]

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
  template<class T1, class T2>
  struct pair {
    using first_type  = T1;
    using second_type = T2;

    T1 first;
    T2 second;

    pair(const pair&) = default;
    pair(pair&&) = default;
    constexpr explicit(see below) pair();
    constexpr explicit(see below) pair(const T1& x, const T2& y);
    template<class U1, class U2>
      constexpr explicit(see below) pair(U1&& x, U2&& y);
    template<class U1, class U2>
      constexpr explicit(see below) pair(const pair<U1, U2>& p);
    template<class U1, class U2>
      constexpr explicit(see below) pair(pair<U1, U2>&& p);
    template<class... Args1, class... Args2>
      constexpr pair(piecewise_construct_t,
                     tuple<Args1...> first_args, tuple<Args2...> second_args);

    constexpr pair& operator=(const pair& p);
    template<class U1, class U2>
      constexpr pair& operator=(const pair<U1, U2>& p);
    constexpr pair& operator=(pair&& p) noexcept(see below);
    template<class U1, class U2>
      constexpr pair& operator=(pair<U1, U2>&& p);

    constexpr void swap(pair& p) noexcept(see below);
  };

  template<class T1, class T2>
    pair(T1, T2) -> pair<T1, T2>;
}
```

Constructors and member functions of `pair` do not throw exceptions
unless one of the element-wise operations specified to be called for
that operation throws an exception.

The defaulted move and copy constructor, respectively, of `pair` is a
constexpr function if and only if all required element-wise
initializations for move and copy, respectively, would satisfy the
requirements for a constexpr function.

If
`(is_trivially_destructible_v<T1> && is_trivially_destructible_v<T2>)`
is `true`, then the destructor of `pair` is trivial.

`pair<T, U>` is a structural type [[temp.param]] if `T` and `U` are both
structural types. Two values `p1` and `p2` of type `pair<T, U>` are
template-argument-equivalent [[temp.type]] if and only if `p1.first` and
`p2.first` are template-argument-equivalent and `p1.second` and
`p2.second` are template-argument-equivalent.

``` cpp
constexpr explicit(see below) pair();
```

*Constraints:*

- `is_default_constructible_v<first_type>` is `true` and
- `is_default_constructible_v<second_type>` is `true`.

*Effects:* Value-initializes `first` and `second`.

*Remarks:* The expression inside `explicit` evaluates to `true` if and
only if either `first_type` or `second_type` is not implicitly
default-constructible.

[*Note 1*: This behavior can be implemented with a trait that checks
whether a `const first_type&` or a `const second_type&` can be
initialized with `{}`. — *end note*]

``` cpp
constexpr explicit(see below) pair(const T1& x, const T2& y);
```

*Constraints:*

- `is_copy_constructible_v<first_type>` is `true` and
- `is_copy_constructible_v<second_type>` is `true`.

*Effects:* Initializes `first` with `x` and `second` with `y`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<const first_type&, first_type> ||
  !is_convertible_v<const second_type&, second_type>
```

``` cpp
template<class U1, class U2> constexpr explicit(see below) pair(U1&& x, U2&& y);
```

*Constraints:*

- `is_constructible_v<first_type, U1>` is `true` and
- `is_constructible_v<second_type, U2>` is `true`.

*Effects:* Initializes `first` with `std::forward<U1>(x)` and `second`
with `std::forward<U2>(y)`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<U1, first_type> || !is_convertible_v<U2, second_type>
```

``` cpp
template<class U1, class U2> constexpr explicit(see below) pair(const pair<U1, U2>& p);
```

*Constraints:*

- `is_constructible_v<first_type, const U1&>` is `true` and
- `is_constructible_v<second_type, const U2&>` is `true`.

*Effects:* Initializes members from the corresponding members of the
argument.

*Remarks:* The expression inside explicit is equivalent to:

``` cpp
!is_convertible_v<const U1&, first_type> || !is_convertible_v<const U2&, second_type>
```

``` cpp
template<class U1, class U2> constexpr explicit(see below) pair(pair<U1, U2>&& p);
```

*Constraints:*

- `is_constructible_v<first_type, U1>` is `true` and
- `is_constructible_v<second_type, U2>` is `true`.

*Effects:* Initializes `first` with `std::forward<U1>(p.first)` and
`second` with `std::forward<U2>(p.second)`.

*Remarks:* The expression inside explicit is equivalent to:

``` cpp
!is_convertible_v<U1, first_type> || !is_convertible_v<U2, second_type>
```

``` cpp
template<class... Args1, class... Args2>
  constexpr pair(piecewise_construct_t,
                 tuple<Args1...> first_args, tuple<Args2...> second_args);
```

*Mandates:*

- `is_constructible_v<first_type, Args1...>` is `true` and
- `is_constructible_v<second_type, Args2...>` is `true`.

*Effects:* Initializes `first` with arguments of types `Args1...`
obtained by forwarding the elements of `first_args` and initializes
`second` with arguments of types `Args2...` obtained by forwarding the
elements of `second_args`. (Here, forwarding an element `x` of type `U`
within a `tuple` object means calling `std::forward<U>(x)`.) This form
of construction, whereby constructor arguments for `first` and `second`
are each provided in a separate `tuple` object, is called *piecewise
construction*.

``` cpp
constexpr pair& operator=(const pair& p);
```

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Remarks:* This operator is defined as deleted unless
`is_copy_assignable_v<first_type>` is `true` and
`is_copy_assignable_v<second_type>` is `true`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr pair& operator=(const pair<U1, U2>& p);
```

*Constraints:*

- `is_assignable_v<first_type&, const U1&>` is `true` and
- `is_assignable_v<second_type&, const U2&>` is `true`.

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

``` cpp
constexpr pair& operator=(pair&& p) noexcept(see below);
```

*Constraints:*

- `is_move_assignable_v<first_type>` is `true` and
- `is_move_assignable_v<second_type>` is `true`.

*Effects:* Assigns to `first` with `std::forward<first_type>(p.first)`
and to `second` with  
`std::forward<second_type>(p.second)`.

*Returns:* `*this`.

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_move_assignable_v<T1> && is_nothrow_move_assignable_v<T2>
```

``` cpp
template<class U1, class U2> constexpr pair& operator=(pair<U1, U2>&& p);
```

*Constraints:*

- `is_assignable_v<first_type&, U1>` is `true` and
- `is_assignable_v<second_type&, U2>` is `true`.

*Effects:* Assigns to `first` with `std::forward<U1>(p.first)` and to
`second` with  
`std::forward<U2>(p.second)`.

*Returns:* `*this`.

``` cpp
constexpr void swap(pair& p) noexcept(see below);
```

*Preconditions:* `first` is swappable with [[swappable.requirements]]
`p.first` and `second` is swappable with `p.second`.

*Effects:* Swaps `first` with `p.first` and `second` with `p.second`.

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
is_nothrow_swappable_v<first_type> && is_nothrow_swappable_v<second_type>
```

### Specialized algorithms <a id="pairs.spec">[[pairs.spec]]</a>

``` cpp
template<class T1, class T2>
  constexpr bool operator==(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Returns:* `x.first == y.first && x.second == y.second`.

``` cpp
template<class T1, class T2>
  constexpr common_comparison_category_t<synth-three-way-result<T1>,
                                         synth-three-way-result<T2>>
    operator<=>(const pair<T1, T2>& x, const pair<T1, T2>& y);
```

*Effects:* Equivalent to:

``` cpp
if (auto c = synth-three-way(x.first, y.first); c != 0) return c;
return synth-three-way(x.second, y.second);
```

``` cpp
template<class T1, class T2>
  constexpr void swap(pair<T1, T2>& x, pair<T1, T2>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `is_swappable_v<T1>` is `true` and `is_swappable_v<T2>`
is `true`.

*Effects:* Equivalent to `x.swap(y)`.

``` cpp
template<class T1, class T2>
  constexpr pair<unwrap_ref_decay_t<T1>, unwrap_ref_decay_t<T2>> make_pair(T1&& x, T2&& y);
```

*Returns:*

``` cpp
pair<unwrap_ref_decay_t<T1>,
     unwrap_ref_decay_t<T2>>(std::forward<T1>(x), std::forward<T2>(y))
```

[*Example 1*:

In place of:

``` cpp
return pair<int, double>(5, 3.1415926);     // explicit types
```

a C++ program may contain:

``` cpp
return make_pair(5, 3.1415926);             // types are deduced
```

— *end example*]

### Tuple-like access to pair <a id="pair.astuple">[[pair.astuple]]</a>

``` cpp
template<class T1, class T2>
  struct tuple_size<pair<T1, T2>> : integral_constant<size_t, 2> { };
```

``` cpp
template<size_t I, class T1, class T2>
  struct tuple_element<I, pair<T1, T2>> {
    using type = see below ;
  };
```

*Mandates:* `I` < 2.

*Type:* The type `T1` if `I` is 0, otherwise the type `T2`.

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

*Mandates:* `I` < 2.

*Returns:*

- If `I` is 0, returns a reference to `p.first`.
- If `I` is 1, returns a reference to `p.second`.

``` cpp
template<class T1, class T2>
  constexpr T1& get(pair<T1, T2>& p) noexcept;
template<class T1, class T2>
  constexpr const T1& get(const pair<T1, T2>& p) noexcept;
template<class T1, class T2>
  constexpr T1&& get(pair<T1, T2>&& p) noexcept;
template<class T1, class T2>
  constexpr const T1&& get(const pair<T1, T2>&& p) noexcept;
```

*Mandates:* `T1` and `T2` are distinct types.

*Returns:* A reference to `p.first`.

``` cpp
template<class T2, class T1>
  constexpr T2& get(pair<T1, T2>& p) noexcept;
template<class T2, class T1>
  constexpr const T2& get(const pair<T1, T2>& p) noexcept;
template<class T2, class T1>
  constexpr T2&& get(pair<T1, T2>&& p) noexcept;
template<class T2, class T1>
  constexpr const T2&& get(const pair<T1, T2>&& p) noexcept;
```

*Mandates:* `T1` and `T2` are distinct types.

*Returns:* A reference to `p.second`.

### Piecewise construction <a id="pair.piecewise">[[pair.piecewise]]</a>

``` cpp
struct piecewise_construct_t {
  explicit piecewise_construct_t() = default;
};
inline constexpr piecewise_construct_t piecewise_construct{};
```

The `struct` `piecewise_construct_t` is an empty class type used as a
unique type to disambiguate constructor and function overloading.
Specifically, `pair` has a constructor with `piecewise_construct_t` as
the first argument, immediately followed by two `tuple` [[tuple]]
arguments used for piecewise construction of the elements of the `pair`
object.

## Tuples <a id="tuple">[[tuple]]</a>

### In general <a id="tuple.general">[[tuple.general]]</a>

Subclause  [[tuple]] describes the tuple library that provides a tuple
type as the class template `tuple` that can be instantiated with any
number of arguments. Each template argument specifies the type of an
element in the `tuple`. Consequently, tuples are heterogeneous,
fixed-size collections of values. An instantiation of `tuple` with two
arguments is similar to an instantiation of `pair` with the same two
arguments. See  [[pairs]].

### Header `<tuple>` synopsis <a id="tuple.syn">[[tuple.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  // [tuple.tuple], class template tuple
  template<class... Types>
    class tuple;

  // [tuple.creation], tuple creation functions
  inline constexpr unspecified ignore;

  template<class... TTypes>
    constexpr tuple<unwrap_ref_decay_t<TTypes>...> make_tuple(TTypes&&...);

  template<class... TTypes>
    constexpr tuple<TTypes&&...> forward_as_tuple(TTypes&&...) noexcept;

  template<class... TTypes>
    constexpr tuple<TTypes&...> tie(TTypes&...) noexcept;

  template<class... Tuples>
    constexpr tuple<CTypes...> tuple_cat(Tuples&&...);

  // [tuple.apply], calling a function with a tuple of arguments
  template<class F, class Tuple>
    constexpr decltype(auto) apply(F&& f, Tuple&& t);

  template<class T, class Tuple>
    constexpr T make_from_tuple(Tuple&& t);

  // [tuple.helper], tuple helper classes
  template<class T> struct tuple_size;                  // not defined
  template<class T> struct tuple_size<const T>;

  template<class... Types> struct tuple_size<tuple<Types...>>;

  template<size_t I, class T> struct tuple_element;     // not defined
  template<size_t I, class T> struct tuple_element<I, const T>;

  template<size_t I, class... Types>
    struct tuple_element<I, tuple<Types...>>;

  template<size_t I, class T>
    using tuple_element_t = typename tuple_element<I, T>::type;

  // [tuple.elem], element access
  template<size_t I, class... Types>
    constexpr tuple_element_t<I, tuple<Types...>>& get(tuple<Types...>&) noexcept;
  template<size_t I, class... Types>
    constexpr tuple_element_t<I, tuple<Types...>>&& get(tuple<Types...>&&) noexcept;
  template<size_t I, class... Types>
    constexpr const tuple_element_t<I, tuple<Types...>>& get(const tuple<Types...>&) noexcept;
  template<size_t I, class... Types>
    constexpr const tuple_element_t<I, tuple<Types...>>&& get(const tuple<Types...>&&) noexcept;
  template<class T, class... Types>
    constexpr T& get(tuple<Types...>& t) noexcept;
  template<class T, class... Types>
    constexpr T&& get(tuple<Types...>&& t) noexcept;
  template<class T, class... Types>
    constexpr const T& get(const tuple<Types...>& t) noexcept;
  template<class T, class... Types>
    constexpr const T&& get(const tuple<Types...>&& t) noexcept;

  // [tuple.rel], relational operators
  template<class... TTypes, class... UTypes>
    constexpr bool operator==(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, class... UTypes>
    constexpr common_comparison_category_t<synth-three-way-result<TTypes, UTypes>...>
      operator<=>(const tuple<TTypes...>&, const tuple<UTypes...>&);

  // [tuple.traits], allocator-related traits
  template<class... Types, class Alloc>
    struct uses_allocator<tuple<Types...>, Alloc>;

  // [tuple.special], specialized algorithms
  template<class... Types>
    constexpr void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);

  // [tuple.helper], tuple helper classes
  template<class T>
    inline constexpr size_t tuple_size_v = tuple_size<T>::value;
}
```

### Class template `tuple` <a id="tuple.tuple">[[tuple.tuple]]</a>

``` cpp
namespace std {
  template<class... Types>
  class tuple {
  public:
    // [tuple.cnstr], tuple construction
    constexpr explicit(see below) tuple();
    constexpr explicit(see below) tuple(const Types&...);         // only if sizeof...(Types) >= 1
    template<class... UTypes>
      constexpr explicit(see below) tuple(UTypes&&...);           // only if sizeof...(Types) >= 1

    tuple(const tuple&) = default;
    tuple(tuple&&) = default;

    template<class... UTypes>
      constexpr explicit(see below) tuple(const tuple<UTypes...>&);
    template<class... UTypes>
      constexpr explicit(see below) tuple(tuple<UTypes...>&&);

    template<class U1, class U2>
      constexpr explicit(see below) tuple(const pair<U1, U2>&);   // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr explicit(see below) tuple(pair<U1, U2>&&);        // only if sizeof...(Types) == 2

    // allocator-extended constructors
    template<class Alloc>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a);
    template<class Alloc>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const Types&...);
    template<class Alloc, class... UTypes>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, UTypes&&...);
    template<class Alloc>
      constexpr tuple(allocator_arg_t, const Alloc& a, const tuple&);
    template<class Alloc>
      constexpr tuple(allocator_arg_t, const Alloc& a, tuple&&);
    template<class Alloc, class... UTypes>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
    template<class Alloc, class... UTypes>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
    template<class Alloc, class U1, class U2>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
    template<class Alloc, class U1, class U2>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);

    // [tuple.assign], tuple assignment
    constexpr tuple& operator=(const tuple&);
    constexpr tuple& operator=(tuple&&) noexcept(see below);

    template<class... UTypes>
      constexpr tuple& operator=(const tuple<UTypes...>&);
    template<class... UTypes>
      constexpr tuple& operator=(tuple<UTypes...>&&);

    template<class U1, class U2>
      constexpr tuple& operator=(const pair<U1, U2>&);          // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr tuple& operator=(pair<U1, U2>&&);               // only if sizeof...(Types) == 2

    // [tuple.swap], tuple swap
    constexpr void swap(tuple&) noexcept(see below);
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

In the descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`) in order, `Tᵢ` be the iᵗʰ type in `Types`, and `Uᵢ`
be the iᵗʰ type in a template parameter pack named `UTypes`, where
indexing is zero-based.

For each `tuple` constructor, an exception is thrown only if the
construction of one of the types in `Types` throws an exception.

The defaulted move and copy constructor, respectively, of `tuple` is a
constexpr function if and only if all required element-wise
initializations for move and copy, respectively, would satisfy the
requirements for a constexpr function. The defaulted move and copy
constructor of `tuple<>` are constexpr functions.

If `is_trivially_destructible_v<Tᵢ>` is `true` for all `Tᵢ`, then the
destructor of `tuple` is trivial.

``` cpp
constexpr explicit(see below) tuple();
```

*Constraints:* `is_default_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* Value-initializes each element.

*Remarks:* The expression inside `explicit` evaluates to `true` if and
only if `Tᵢ` is not copy-list-initializable from an empty list for at
least one i.

[*Note 1*: This behavior can be implemented with a trait that checks
whether a `const ``Tᵢ``&` can be initialized with `{}`. — *end note*]

``` cpp
constexpr explicit(see below) tuple(const Types&...);
```

*Constraints:* `sizeof...(Types)` ≥ 1 and
`is_copy_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* Initializes each element with the value of the corresponding
parameter.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!conjunction_v<is_convertible<const Types&, Types>...>
```

``` cpp
template<class... UTypes> constexpr explicit(see below) tuple(UTypes&&... u);
```

*Constraints:* `sizeof...(Types)` equals `sizeof...(UTypes)` and
`sizeof...(Types)` ≥ 1 and `is_constructible_v<``Tᵢ``, ``Uᵢ``>` is
`true` for all i.

*Effects:* Initializes the elements in the tuple with the corresponding
value in `std::forward<UTypes>(u)`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!conjunction_v<is_convertible<UTypes, Types>...>
```

``` cpp
tuple(const tuple& u) = default;
```

*Mandates:* `is_copy_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* Initializes each element of `*this` with the corresponding
element of `u`.

``` cpp
tuple(tuple&& u) = default;
```

*Constraints:* `is_move_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`std::forward<``Tᵢ``>(get<`i`>(u))`.

``` cpp
template<class... UTypes> constexpr explicit(see below) tuple(const tuple<UTypes...>& u);
```

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)` and
- `is_constructible_v<``Tᵢ``, const ``Uᵢ``&>` is `true` for all i, and
- either `sizeof...(Types)` is not 1, or (when `Types...` expands to `T`
  and `UTypes...` expands to `U`)
  `is_convertible_v<const tuple<U>&, T>`,
  `is_constructible_v<T, const tuple<U>&>`, and `is_same_v<T, U>` are
  all `false`.

*Effects:* Initializes each element of `*this` with the corresponding
element of `u`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!conjunction_v<is_convertible<const UTypes&, Types>...>
```

``` cpp
template<class... UTypes> constexpr explicit(see below) tuple(tuple<UTypes...>&& u);
```

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)`, and
- `is_constructible_v<``Tᵢ``, ``Uᵢ``>` is `true` for all i, and
- either `sizeof...(Types)` is not 1, or (when `Types...` expands to `T`
  and `UTypes...` expands to `U`) `is_convertible_v<tuple<U>, T>`,
  `is_constructible_v<T, tuple<U>>`, and `is_same_v<T, U>` are all
  `false`.

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`std::forward<``Uᵢ``>(get<`i`>(u))`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!conjunction_v<is_convertible<UTypes, Types>...>
```

``` cpp
template<class U1, class U2> constexpr explicit(see below) tuple(const pair<U1, U2>& u);
```

*Constraints:*

- `sizeof...(Types)` is 2,
- `is_constructible_v<``T₀``, const U1&>` is `true`, and
- `is_constructible_v<``T₁``, const U2&>` is `true`.

*Effects:* Initializes the first element with `u.first` and the second
element with `u.second`.

The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<const U1&, $T_0$> || !is_convertible_v<const U2&, $T_1$>
```

``` cpp
template<class U1, class U2> constexpr explicit(see below) tuple(pair<U1, U2>&& u);
```

*Constraints:*

- `sizeof...(Types)` is 2,
- `is_constructible_v<``T₀``, U1>` is `true`, and
- `is_constructible_v<``T₁``, U2>` is `true`.

*Effects:* Initializes the first element with
`std::forward<U1>(u.first)` and the second element with
`std::forward<U2>(u.second)`.

The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<U1, $T_0$> || !is_convertible_v<U2, $T_1$>
```

``` cpp
template<class Alloc>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a);
template<class Alloc>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const Types&...);
template<class Alloc, class... UTypes>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, UTypes&&...);
template<class Alloc>
  constexpr tuple(allocator_arg_t, const Alloc& a, const tuple&);
template<class Alloc>
  constexpr tuple(allocator_arg_t, const Alloc& a, tuple&&);
template<class Alloc, class... UTypes>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
template<class Alloc, class... UTypes>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
template<class Alloc, class U1, class U2>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
template<class Alloc, class U1, class U2>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);
```

*Preconditions:* `Alloc` meets the *Cpp17Allocator* requirements
([[cpp17.allocator]]).

*Effects:* Equivalent to the preceding constructors except that each
element is constructed with uses-allocator
construction [[allocator.uses.construction]].

#### Assignment <a id="tuple.assign">[[tuple.assign]]</a>

For each `tuple` assignment operator, an exception is thrown only if the
assignment of one of the types in `Types` throws an exception. In the
function descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`) in order, `Tᵢ` be the iᵗʰ type in `Types`, and `Uᵢ`
be the iᵗʰ type in a template parameter pack named `UTypes`, where
indexing is zero-based.

``` cpp
constexpr tuple& operator=(const tuple& u);
```

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Remarks:* This operator is defined as deleted unless
`is_copy_assignable_v<``Tᵢ``>` is `true` for all i.

*Returns:* `*this`.

``` cpp
constexpr tuple& operator=(tuple&& u) noexcept(see below);
```

*Constraints:* `is_move_assignable_v<``Tᵢ``>` is `true` for all i.

*Effects:* For all i, assigns `std::forward<``Tᵢ``>(get<`i`>(u))` to
`get<`i`>(*this)`.

*Remarks:* The expression inside `noexcept` is equivalent to the logical
<span class="smallcaps">and</span> of the following expressions:

``` cpp
is_nothrow_move_assignable_v<Tᵢ>
```

where Tᵢ is the iᵗʰ type in `Types`.

*Returns:* `*this`.

``` cpp
template<class... UTypes> constexpr tuple& operator=(const tuple<UTypes...>& u);
```

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)` and
- `is_assignable_v<``Tᵢ``&, const ``Uᵢ``&>` is `true` for all i.

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Returns:* `*this`.

``` cpp
template<class... UTypes> constexpr tuple& operator=(tuple<UTypes...>&& u);
```

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)` and
- `is_assignable_v<``Tᵢ``&, ``Uᵢ``>` is `true` for all i.

*Effects:* For all i, assigns `std::forward<``Uᵢ``>(get<`i`>(u))` to
`get<`i`>(*this)`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr tuple& operator=(const pair<U1, U2>& u);
```

*Constraints:*

- `sizeof...(Types)` is 2 and
- `is_assignable_v<``T₀``&, const U1&>` is `true`, and
- `is_assignable_v<``T₁``&, const U2&>` is `true`.

*Effects:* Assigns `u.first` to the first element of `*this` and
`u.second` to the second element of `*this`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr tuple& operator=(pair<U1, U2>&& u);
```

*Constraints:*

- `sizeof...(Types)` is 2 and
- `is_assignable_v<``T₀``&, U1>` is `true`, and
- `is_assignable_v<``T₁``&, U2>` is `true`.

*Effects:* Assigns `std::forward<U1>(u.first)` to the first element of
`*this` and  
`std::forward<U2>(u.second)` to the second element of `*this`.

*Returns:* `*this`.

#### `swap` <a id="tuple.swap">[[tuple.swap]]</a>

``` cpp
constexpr void swap(tuple& rhs) noexcept(see below);
```

*Preconditions:* Each element in `*this` is swappable
with [[swappable.requirements]] the corresponding element in `rhs`.

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

### Tuple creation functions <a id="tuple.creation">[[tuple.creation]]</a>

In the function descriptions that follow, the members of a template
parameter pack `XTypes` are denoted by `X`ᵢ for i in \[`0`,
`sizeof...(`*X*`Types)`) in order, where indexing is zero-based.

``` cpp
template<class... TTypes>
  constexpr tuple<unwrap_ref_decay_t<TTypes>...> make_tuple(TTypes&&... t);
```

*Returns:*
`tuple<unwrap_ref_decay_t<TTypes>...>(std::forward<TTypes>(t)...)`.

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
may contain references to temporary objects, a program shall ensure that
the return value of this function does not outlive any of its arguments
(e.g., the program should typically not store the result in a named
variable).

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
template<class... Tuples>
  constexpr tuple<CTypes...> tuple_cat(Tuples&&... tpls);
```

In the following paragraphs, let `Tᵢ` be the iᵗʰ type in `Tuples`, `Uᵢ`
be `remove_reference_t<T`ᵢ`>`, and `tpᵢ` be the iᵗʰ parameter in the
function parameter pack `tpls`, where all indexing is zero-based.

*Preconditions:* For all i, `Uᵢ` is the type cvᵢ `tuple<``Argsᵢ``...>`,
where cvᵢ is the (possibly empty) iᵗʰ *cv-qualifier-seq* and `Argsᵢ` is
the template parameter pack representing the element types in `Uᵢ`. Let
`A_ik` be the kᵗʰ type in `Argsᵢ`. For all `A_ik` the following
requirements are met:

- If `Tᵢ` is deduced as an lvalue reference type, then
  `is_constructible_v<``A_ik``, `cvᵢ `A_ik``&> == true`, otherwise
- `is_constructible_v<``A_ik``, `cvᵢ `A_ik``&&> == true`.

*Remarks:* The types in `CTypes` are equal to the ordered sequence of
the extended types `Args₀``..., ``Args₁``..., `…`, ``Args_n-1``...`,
where n is equal to `sizeof...(Tuples)`. Let `eᵢ``...` be the iᵗʰ
ordered sequence of tuple elements of the resulting `tuple` object
corresponding to the type sequence `Argsᵢ`.

*Returns:* A `tuple` object constructed by initializing the kᵢᵗʰ type
element `e_ik` in `eᵢ``...` with

``` cpp
get<kᵢ>(std::forward<$T_i$>($tp_i$))
```

for each valid kᵢ and each group `eᵢ` in order.

[*Note 1*: An implementation may support additional types in the
template parameter pack `Tuples` that support the `tuple`-like protocol,
such as `pair` and `array`. — *end note*]

### Calling a function with a `tuple` of arguments <a id="tuple.apply">[[tuple.apply]]</a>

``` cpp
template<class F, class Tuple>
  constexpr decltype(auto) apply(F&& f, Tuple&& t);
```

*Effects:* Given the exposition-only function:

``` cpp
template<class F, class Tuple, size_t... I>
constexpr decltype(auto) apply-impl(F&& f, Tuple&& t, index_sequence<I...>) {
                                                                        // exposition only
  return INVOKE(std::forward<F>(f), std::get<I>(std::forward<Tuple>(t))...);  // see REF:func.require
}
```

Equivalent to:

``` cpp
return apply-impl(std::forward<F>(f), std::forward<Tuple>(t),
                  make_index_sequence<tuple_size_v<remove_reference_t<Tuple>>>{});
```

``` cpp
template<class T, class Tuple>
  constexpr T make_from_tuple(Tuple&& t);
```

*Effects:* Given the exposition-only function:

``` cpp
template<class T, class Tuple, size_t... I>
constexpr T make-from-tuple-impl(Tuple&& t, index_sequence<I...>) {     // exposition only
  return T(get<I>(std::forward<Tuple>(t))...);
}
```

Equivalent to:

``` cpp
return make-from-tuple-impl<T>(
           forward<Tuple>(t),
           make_index_sequence<tuple_size_v<remove_reference_t<Tuple>>>{});
```

[*Note 1*: The type of `T` must be supplied as an explicit template
parameter, as it cannot be deduced from the argument
list. — *end note*]

### Tuple helper classes <a id="tuple.helper">[[tuple.helper]]</a>

``` cpp
template<class T> struct tuple_size;
```

All specializations of `tuple_size` meet the *Cpp17UnaryTypeTrait*
requirements [[meta.rqmts]] with a base characteristic of
`integral_constant<size_t, N>` for some `N`.

``` cpp
template<class... Types>
  struct tuple_size<tuple<Types...>> : public integral_constant<size_t, sizeof...(Types)> { };
```

``` cpp
template<size_t I, class... Types>
  struct tuple_element<I, tuple<Types...>> {
    using type = TI;
  };
```

*Mandates:* `I` < `sizeof...(Types)`.

*Type:* `TI` is the type of the `I`ᵗʰ element of `Types`, where indexing
is zero-based.

``` cpp
template<class T> struct tuple_size<const T>;
```

Let `TS` denote `tuple_size<T>` of the cv-unqualified type `T`. If the
expression `TS::value` is well-formed when treated as an unevaluated
operand, then each specialization of the template meets the
*Cpp17UnaryTypeTrait* requirements [[meta.rqmts]] with a base
characteristic of

``` cpp
integral_constant<size_t, TS::value>
```

Otherwise, it has no member `value`.

Access checking is performed as if in a context unrelated to `TS` and
`T`. Only the validity of the immediate context of the expression is
considered.

[*Note 1*: The compilation of the expression can result in side effects
such as the instantiation of class template specializations and function
template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*]

In addition to being available via inclusion of the `<tuple>` header,
the template is available when any of the headers `<array>`, `<ranges>`,
or `<utility>` are included.

``` cpp
template<size_t I, class T> struct tuple_element<I, const T>;
```

Let `TE` denote `tuple_element_t<I, T>` of the cv-unqualified type `T`.
Then each specialization of the template meets the
*Cpp17TransformationTrait* requirements [[meta.rqmts]] with a member
typedef `type` that names the type `add_const_t<TE>`.

In addition to being available via inclusion of the `<tuple>` header,
the template is available when any of the headers `<array>`, `<ranges>`,
or `<utility>` are included.

### Element access <a id="tuple.elem">[[tuple.elem]]</a>

``` cpp
template<size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...>>&
    get(tuple<Types...>& t) noexcept;
template<size_t I, class... Types>
  constexpr tuple_element_t<I, tuple<Types...>>&&
    get(tuple<Types...>&& t) noexcept;        // Note A
template<size_t I, class... Types>
  constexpr const tuple_element_t<I, tuple<Types...>>&
    get(const tuple<Types...>& t) noexcept;   // Note B
template<size_t I, class... Types>
  constexpr const tuple_element_t<I, tuple<Types...>>&& get(const tuple<Types...>&& t) noexcept;
```

*Mandates:* `I` < `sizeof...(Types)`.

*Returns:* A reference to the `I`ᵗʰ element of `t`, where indexing is
zero-based.

[*Note 1*: \[Note A\]If a type `T` in `Types` is some reference type
`X&`, the return type is `X&`, not `X&&`. However, if the element type
is a non-reference type `T`, the return type is `T&&`. — *end note*]

[*Note 2*: \[Note B\]Constness is shallow. If a type `T` in `Types` is
some reference type `X&`, the return type is `X&`, not `const X&`.
However, if the element type is a non-reference type `T`, the return
type is `const T&`. This is consistent with how constness is defined to
work for member variables of reference type. — *end note*]

``` cpp
template<class T, class... Types>
  constexpr T& get(tuple<Types...>& t) noexcept;
template<class T, class... Types>
  constexpr T&& get(tuple<Types...>&& t) noexcept;
template<class T, class... Types>
  constexpr const T& get(const tuple<Types...>& t) noexcept;
template<class T, class... Types>
  constexpr const T&& get(const tuple<Types...>&& t) noexcept;
```

*Mandates:* The type `T` occurs exactly once in `Types`.

*Returns:* A reference to the element of `t` corresponding to the type
`T` in `Types`.

[*Example 1*:

``` cpp
const tuple<int, const int, double, double> t(1, 2, 3.4, 5.6);
const int& i1 = get<int>(t);                    // OK, i1 has value 1
const int& i2 = get<const int>(t);              // OK, i2 has value 2
const double& d = get<double>(t);               // error: type double is not unique within t
```

— *end example*]

[*Note 1*: The reason `get` is a non-member function is that if this
functionality had been provided as a member function, code where the
type depended on a template parameter would have required using the
`template` keyword. — *end note*]

### Relational operators <a id="tuple.rel">[[tuple.rel]]</a>

``` cpp
template<class... TTypes, class... UTypes>
  constexpr bool operator==(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Mandates:* For all `i`, where 0 ≤ `i` < `sizeof...(TTypes)`,
`get<i>(t) == get<i>(u)` is a valid expression returning a type that is
convertible to `bool`. `sizeof...(TTypes)` equals `sizeof...(UTypes)`.

*Returns:* `true` if `get<i>(t) == get<i>(u)` for all `i`, otherwise
`false`. For any two zero-length tuples `e` and `f`, `e == f` returns
`true`.

*Effects:* The elementary comparisons are performed in order from the
zeroth index upwards. No comparisons or element accesses are performed
after the first equality comparison that evaluates to `false`.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr common_comparison_category_t<synth-three-way-result<TTypes, UTypes>...>
    operator<=>(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
```

*Effects:* Performs a lexicographical comparison between `t` and `u`.
For any two zero-length tuples `t` and `u`, `t <=> u` returns
`strong_ordering::equal`. Otherwise, equivalent to:

``` cpp
if (auto c = synth-three-way(get<0>(t), get<0>(u)); c != 0) return c;
return $t_tail$ <=> $u_tail$;
```

where `r_tail` for some tuple `r` is a tuple containing all but the
first element of `r`.

[*Note 1*: The above definition does not require `tₜₐᵢₗ` (or `uₜₐᵢₗ`)
to be constructed. It may not even be possible, as `t` and `u` are not
required to be copy constructible. Also, all comparison functions are
short circuited; they do not perform element accesses beyond what is
required to determine the result of the comparison. — *end note*]

### Tuple traits <a id="tuple.traits">[[tuple.traits]]</a>

``` cpp
template<class... Types, class Alloc>
  struct uses_allocator<tuple<Types...>, Alloc> : true_type { };
```

*Preconditions:* `Alloc` meets the *Cpp17Allocator* requirements
([[cpp17.allocator]]).

[*Note 1*: Specialization of this trait informs other library
components that `tuple` can be constructed with an allocator, even
though it does not have a nested `allocator_type`. — *end note*]

### Tuple specialized algorithms <a id="tuple.special">[[tuple.special]]</a>

``` cpp
template<class... Types>
  constexpr void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);
```

*Constraints:* `is_swappable_v<T>` is `true` for every type `T` in
`Types`.

*Remarks:* The expression inside `noexcept` is equivalent to:

``` cpp
noexcept(x.swap(y))
```

*Effects:* As if by `x.swap(y)`.

## Optional objects <a id="optional">[[optional]]</a>

### In general <a id="optional.general">[[optional.general]]</a>

Subclause  [[optional]] describes class template `optional` that
represents optional objects. An *optional object* is an object that
contains the storage for another object and manages the lifetime of this
contained object, if any. The contained object may be initialized after
the optional object has been initialized, and may be destroyed before
the optional object has been destroyed. The initialization state of the
contained object is tracked by the optional object.

### Header `<optional>` synopsis <a id="optional.syn">[[optional.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  // [optional.optional], class template optional
  template<class T>
    class optional;

  // [optional.nullopt], no-value state indicator
  struct nullopt_t{see below};
  inline constexpr nullopt_t nullopt(unspecified);

  // [optional.bad.access], class bad_optional_access
  class bad_optional_access;

  // [optional.relops], relational operators
  template<class T, class U>
    constexpr bool operator==(const optional<T>&, const optional<U>&);
  template<class T, class U>
    constexpr bool operator!=(const optional<T>&, const optional<U>&);
  template<class T, class U>
    constexpr bool operator<(const optional<T>&, const optional<U>&);
  template<class T, class U>
    constexpr bool operator>(const optional<T>&, const optional<U>&);
  template<class T, class U>
    constexpr bool operator<=(const optional<T>&, const optional<U>&);
  template<class T, class U>
    constexpr bool operator>=(const optional<T>&, const optional<U>&);
  template<class T, three_way_comparable_with<T> U>
    constexpr compare_three_way_result_t<T,U>
      operator<=>(const optional<T>&, const optional<U>&);

  // [optional.nullops], comparison with nullopt
  template<class T> constexpr bool operator==(const optional<T>&, nullopt_t) noexcept;
  template<class T>
    constexpr strong_ordering operator<=>(const optional<T>&, nullopt_t) noexcept;

  // [optional.comp.with.t], comparison with T
  template<class T, class U> constexpr bool operator==(const optional<T>&, const U&);
  template<class T, class U> constexpr bool operator==(const T&, const optional<U>&);
  template<class T, class U> constexpr bool operator!=(const optional<T>&, const U&);
  template<class T, class U> constexpr bool operator!=(const T&, const optional<U>&);
  template<class T, class U> constexpr bool operator<(const optional<T>&, const U&);
  template<class T, class U> constexpr bool operator<(const T&, const optional<U>&);
  template<class T, class U> constexpr bool operator>(const optional<T>&, const U&);
  template<class T, class U> constexpr bool operator>(const T&, const optional<U>&);
  template<class T, class U> constexpr bool operator<=(const optional<T>&, const U&);
  template<class T, class U> constexpr bool operator<=(const T&, const optional<U>&);
  template<class T, class U> constexpr bool operator>=(const optional<T>&, const U&);
  template<class T, class U> constexpr bool operator>=(const T&, const optional<U>&);
  template<class T, three_way_comparable_with<T> U>
    constexpr compare_three_way_result_t<T,U>
      operator<=>(const optional<T>&, const U&);

  // [optional.specalg], specialized algorithms
  template<class T>
    void swap(optional<T>&, optional<T>&) noexcept(see below);

  template<class T>
    constexpr optional<see below> make_optional(T&&);
  template<class T, class... Args>
    constexpr optional<T> make_optional(Args&&... args);
  template<class T, class U, class... Args>
    constexpr optional<T> make_optional(initializer_list<U> il, Args&&... args);

  // [optional.hash], hash support
  template<class T> struct hash;
  template<class T> struct hash<optional<T>>;
}
```

### Class template `optional` <a id="optional.optional">[[optional.optional]]</a>

``` cpp
namespace std {
  template<class T>
  class optional {
  public:
    using value_type = T;

    // [optional.ctor], constructors
    constexpr optional() noexcept;
    constexpr optional(nullopt_t) noexcept;
    constexpr optional(const optional&);
    constexpr optional(optional&&) noexcept(see below);
    template<class... Args>
      constexpr explicit optional(in_place_t, Args&&...);
    template<class U, class... Args>
      constexpr explicit optional(in_place_t, initializer_list<U>, Args&&...);
    template<class U = T>
      constexpr explicit(see below) optional(U&&);
    template<class U>
      explicit(see below) optional(const optional<U>&);
    template<class U>
      explicit(see below) optional(optional<U>&&);

    // [optional.dtor], destructor
    ~optional();

    // [optional.assign], assignment
    optional& operator=(nullopt_t) noexcept;
    constexpr optional& operator=(const optional&);
    constexpr optional& operator=(optional&&) noexcept(see below);
    template<class U = T> optional& operator=(U&&);
    template<class U> optional& operator=(const optional<U>&);
    template<class U> optional& operator=(optional<U>&&);
    template<class... Args> T& emplace(Args&&...);
    template<class U, class... Args> T& emplace(initializer_list<U>, Args&&...);

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
    template<class U> constexpr T value_or(U&&) const&;
    template<class U> constexpr T value_or(U&&) &&;

    // [optional.mod], modifiers
    void reset() noexcept;

  private:
    T *val;         // exposition only
  };

  template<class T>
    optional(T) -> optional<T>;
}
```

Any instance of `optional<T>` at any given time either contains a value
or does not contain a value. When an instance of `optional<T>` *contains
a value*, it means that an object of type `T`, referred to as the
optional object’s *contained value*, is allocated within the storage of
the optional object. Implementations are not permitted to use additional
storage, such as dynamic memory, to allocate its contained value. The
contained value shall be allocated in a region of the `optional<T>`
storage suitably aligned for the type `T`. When an object of type
`optional<T>` is contextually converted to `bool`, the conversion
returns `true` if the object contains a value; otherwise the conversion
returns `false`.

Member `val` is provided for exposition only. When an `optional<T>`
object contains a value, `val` points to the contained value.

`T` shall be a type other than cv `in_place_t` or cv `nullopt_t` that
meets the *Cpp17Destructible* requirements ([[cpp17.destructible]]).

#### Constructors <a id="optional.ctor">[[optional.ctor]]</a>

``` cpp
constexpr optional() noexcept;
constexpr optional(nullopt_t) noexcept;
```

*Ensures:* `*this` does not contain a value.

*Remarks:* No contained value is initialized. For every object type `T`
these constructors are constexpr constructors [[dcl.constexpr]].

``` cpp
constexpr optional(const optional& rhs);
```

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `*rhs`.

*Ensures:* `bool(rhs) == bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* This constructor is defined as deleted unless
`is_copy_constructible_v<T>` is `true`. If
`is_trivially_copy_constructible_v<T>` is `true`, this constructor is
trivial.

``` cpp
constexpr optional(optional&& rhs) noexcept(see below);
```

*Constraints:* `is_move_constructible_v<T>` is `true`.

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `std::move(*rhs)`. `bool(rhs)` is unchanged.

*Ensures:* `bool(rhs) == bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The expression inside `noexcept` is equivalent to
`is_nothrow_move_constructible_v<T>`. If
`is_trivially_move_constructible_v<T>` is `true`, this constructor is
trivial.

``` cpp
template<class... Args> constexpr explicit optional(in_place_t, Args&&... args);
```

*Constraints:* `is_constructible_v<T, Args...>` is `true`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If `T`’s constructor selected for the initialization is a
constexpr constructor, this constructor is a constexpr constructor.

``` cpp
template<class U, class... Args>
  constexpr explicit optional(in_place_t, initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<T, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`il, std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If `T`’s constructor selected for the initialization is a
constexpr constructor, this constructor is a constexpr constructor.

``` cpp
template<class U = T> constexpr explicit(see below) optional(U&& v);
```

*Constraints:* `is_constructible_v<T, U>` is `true`,
`is_same_v<remove_cvref_t<U>, in_place_t>` is `false`, and
`is_same_v<remove_cvref_t<U>, optional>` is `false`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the expression
`std::forward<U>(v)`.

*Ensures:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If `T`’s selected constructor is a constexpr constructor,
this constructor is a constexpr constructor. The expression inside
`explicit` is equivalent to:

``` cpp
!is_convertible_v<U, T>
```

``` cpp
template<class U> explicit(see below) optional(const optional<U>& rhs);
```

*Constraints:*

- `is_constructible_v<T, const U&>` is `true`,
- `is_constructible_v<T, optional<U>&>` is `false`,
- `is_constructible_v<T, optional<U>&&>` is `false`,
- `is_constructible_v<T, const optional<U>&>` is `false`,
- `is_constructible_v<T, const optional<U>&&>` is `false`,
- `is_convertible_v<optional<U>&, T>` is `false`,
- `is_convertible_v<optional<U>&&, T>` is `false`,
- `is_convertible_v<const optional<U>&, T>` is `false`, and
- `is_convertible_v<const optional<U>&&, T>` is `false`.

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `*rhs`.

*Ensures:* `bool(rhs)` == `bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<const U&, T>
```

``` cpp
template<class U> explicit(see below) optional(optional<U>&& rhs);
```

*Constraints:*

- `is_constructible_v<T, U>` is true,
- `is_constructible_v<T, optional<U>&>` is `false`,
- `is_constructible_v<T, optional<U>&&>` is `false`,
- `is_constructible_v<T, const optional<U>&>` is `false`,
- `is_constructible_v<T, const optional<U>&&>` is `false`,
- `is_convertible_v<optional<U>&, T>` is `false`,
- `is_convertible_v<optional<U>&&, T>` is `false`,
- `is_convertible_v<const optional<U>&, T>` is `false`, and
- `is_convertible_v<const optional<U>&&, T>` is `false`.

*Effects:* If `rhs` contains a value, initializes the contained value as
if direct-non-list-initializing an object of type `T` with the
expression `std::move(*rhs)`. `bool(rhs)` is unchanged.

*Ensures:* `bool(rhs)` == `bool(*this)`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<U, T>
```

#### Destructor <a id="optional.dtor">[[optional.dtor]]</a>

``` cpp
~optional();
```

*Effects:* If `is_trivially_destructible_v<T> != true` and `*this`
contains a value, calls

``` cpp
val->T::~T()
```

*Remarks:* If `is_trivially_destructible_v<T>` is `true`, then this
destructor is trivial.

#### Assignment <a id="optional.assign">[[optional.assign]]</a>

``` cpp
optional<T>& operator=(nullopt_t) noexcept;
```

*Effects:* If `*this` contains a value, calls `val->T::T̃()` to destroy
the contained value; otherwise no effect.

*Ensures:* `*this` does not contain a value.

*Returns:* `*this`.

``` cpp
constexpr optional<T>& operator=(const optional& rhs);
```

*Effects:* See [[optional.assign.copy]].

**Table: `optional::operator=(const optional&)` effects** <a id="optional.assign.copy">[optional.assign.copy]</a>

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                     |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `*rhs` to the contained value                  | initializes the contained value as if direct-non-list-initializing an object of type `T` with `*rhs` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                            |


*Ensures:* `bool(rhs) == bool(*this)`.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s copy constructor, no effect. If an exception is thrown
during the call to `T`’s copy assignment, the state of its contained
value is as defined by the exception safety guarantee of `T`’s copy
assignment. This operator is defined as deleted unless
`is_copy_constructible_v<T>` is `true` and `is_copy_assignable_v<T>` is
`true`. If `is_trivially_copy_constructible_v<T> &&`
`is_trivially_copy_assignable_v<T> &&` `is_trivially_destructible_v<T>`
is `true`, this assignment operator is trivial.

``` cpp
constexpr optional& operator=(optional&& rhs) noexcept(see below);
```

*Constraints:* `is_move_constructible_v<T>` is `true` and
`is_move_assignable_v<T>` is `true`.

*Effects:* See [[optional.assign.move]]. The result of the expression
`bool(rhs)` remains unchanged.

**Table: `optional::operator=(optional&&)` effects** <a id="optional.assign.move">[optional.assign.move]</a>

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                                |
| ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `std::move(*rhs)` to the contained value       | initializes the contained value as if direct-non-list-initializing an object of type `T` with `std::move(*rhs)` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                                       |


*Ensures:* `bool(rhs) == bool(*this)`.

*Returns:* `*this`.

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
assignment. If `is_trivially_move_constructible_v<T> &&`
`is_trivially_move_assignable_v<T> &&` `is_trivially_destructible_v<T>`
is `true`, this assignment operator is trivial.

``` cpp
template<class U = T> optional<T>& operator=(U&& v);
```

*Constraints:* `is_same_v<remove_cvref_t<U>, optional>` is `false`,
`conjunction_v<is_scalar<T>, is_same<T, decay_t<U>>>` is `false`,
`is_constructible_v<T, U>` is `true`, and `is_assignable_v<T&, U>` is
`true`.

*Effects:* If `*this` contains a value, assigns `std::forward<U>(v)` to
the contained value; otherwise initializes the contained value as if
direct-non-list-initializing object of type `T` with
`std::forward<U>(v)`.

*Ensures:* `*this` contains a value.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s constructor, the state of `v` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and `v`
is determined by the exception safety guarantee of `T`’s assignment.

``` cpp
template<class U> optional<T>& operator=(const optional<U>& rhs);
```

*Constraints:*

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

*Effects:* See [[optional.assign.copy.templ]].

**Table: `optional::operator=(const optional<U>&)` effects** <a id="optional.assign.copy.templ">[optional.assign.copy.templ]</a>

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                     |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `*rhs` to the contained value                  | initializes the contained value as if direct-non-list-initializing an object of type `T` with `*rhs` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                            |


*Ensures:* `bool(rhs) == bool(*this)`.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s constructor, the state of `*rhs.val` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s
assignment.

``` cpp
template<class U> optional<T>& operator=(optional<U>&& rhs);
```

*Constraints:*

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

*Effects:* See [[optional.assign.move.templ]]. The result of the
expression `bool(rhs)` remains unchanged.

**Table: `optional::operator=(optional<U>&&)` effects** <a id="optional.assign.move.templ">[optional.assign.move.templ]</a>

|                                | `*this` contains a value                               | `*this` does not contain a value                                                                                |
| ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `std::move(*rhs)` to the contained value       | initializes the contained value as if direct-non-list-initializing an object of type `T` with `std::move(*rhs)` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                                                                       |


*Ensures:* `bool(rhs) == bool(*this)`.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`bool(*this)` remains unchanged. If an exception is thrown during the
call to `T`’s constructor, the state of `*rhs.val` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s
assignment.

``` cpp
template<class... Args> T& emplace(Args&&... args);
```

*Mandates:* `is_constructible_v<T, Args...>` is `true`.

*Effects:* Calls `*this = nullopt`. Then initializes the contained value
as if direct-non-list-initializing an object of type `T` with the
arguments `std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If an exception is thrown during the call to `T`’s
constructor, `*this` does not contain a value, and the previous `*val`
(if any) has been destroyed.

``` cpp
template<class U, class... Args> T& emplace(initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<T, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Calls `*this = nullopt`. Then initializes the contained value
as if direct-non-list-initializing an object of type `T` with the
arguments `il, std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If an exception is thrown during the call to `T`’s
constructor, `*this` does not contain a value, and the previous `*val`
(if any) has been destroyed.

#### Swap <a id="optional.swap">[[optional.swap]]</a>

``` cpp
void swap(optional& rhs) noexcept(see below);
```

*Mandates:* `is_move_constructible_v<T>` is `true`.

*Preconditions:* Lvalues of type `T` are swappable.

*Effects:* See [[optional.swap]].

**Table: `optional::swap(optional&)` effects** <a id="optional.swap">[optional.swap]</a>

|                                | `*this` contains a value                                                                                                                                                                                                                                   | `*this` does not contain a value                                                                                                                                                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rhs` contains a value         | calls `swap(*(*this), *rhs)`                                                                                                                                                                                                                               | initializes the contained value of `*this` as if direct-non-list-initializing an object of type `T` with the expression `std::move(*rhs)`, followed by `rhs.val->T::~T()`; postcondition is that `*this` contains a value and `rhs` does not contain a value |
| `rhs` does not contain a value | initializes the contained value of `rhs` as if direct-non-list-initializing an object of type `T` with the expression `std::move(*(*this))`, followed by `val->T::~T()`; postcondition is that `*this` does not contain a value and `rhs` contains a value | no effect                                                                                                                                                                                                                                                    |


*Throws:* Any exceptions thrown by the operations in the relevant part
of [[optional.swap]].

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

*Preconditions:* `*this` contains a value.

*Returns:* `val`.

*Throws:* Nothing.

*Remarks:* These functions are constexpr functions.

``` cpp
constexpr const T& operator*() const&;
constexpr T& operator*() &;
```

*Preconditions:* `*this` contains a value.

*Returns:* `*val`.

*Throws:* Nothing.

*Remarks:* These functions are constexpr functions.

``` cpp
constexpr T&& operator*() &&;
constexpr const T&& operator*() const&&;
```

*Preconditions:* `*this` contains a value.

*Effects:* Equivalent to: `return std::move(*val);`

``` cpp
constexpr explicit operator bool() const noexcept;
```

*Returns:* `true` if and only if `*this` contains a value.

*Remarks:* This function is a constexpr function.

``` cpp
constexpr bool has_value() const noexcept;
```

*Returns:* `true` if and only if `*this` contains a value.

*Remarks:* This function is a constexpr function.

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
template<class U> constexpr T value_or(U&& v) const&;
```

*Mandates:* `is_copy_constructible_v<T> && is_convertible_v<U&&, T>` is
`true`.

*Effects:* Equivalent to:

``` cpp
return bool(*this) ? **this : static_cast<T>(std::forward<U>(v));
```

``` cpp
template<class U> constexpr T value_or(U&& v) &&;
```

*Mandates:* `is_move_constructible_v<T> && is_convertible_v<U&&, T>` is
`true`.

*Effects:* Equivalent to:

``` cpp
return bool(*this) ? std::move(**this) : static_cast<T>(std::forward<U>(v));
```

#### Modifiers <a id="optional.mod">[[optional.mod]]</a>

``` cpp
void reset() noexcept;
```

*Effects:* If `*this` contains a value, calls `val->T::T̃()` to destroy
the contained value; otherwise no effect.

*Ensures:* `*this` does not contain a value.

### No-value state indicator <a id="optional.nullopt">[[optional.nullopt]]</a>

``` cpp
struct nullopt_t{see below};
inline constexpr nullopt_t nullopt(unspecified);
```

The struct `nullopt_t` is an empty class type used as a unique type to
indicate the state of not containing a value for `optional` objects. In
particular, `optional<T>` has a constructor with `nullopt_t` as a single
argument; this indicates that an optional object not containing a value
shall be constructed.

Type `nullopt_t` shall not have a default constructor or an
initializer-list constructor, and shall not be an aggregate.

### Class `bad_optional_access` <a id="optional.bad.access">[[optional.bad.access]]</a>

``` cpp
class bad_optional_access : public exception {
public:
  // see [exception] for the specification of the special member functions
  const char* what() const noexcept override;
};
```

The class `bad_optional_access` defines the type of objects thrown as
exceptions to report the situation where an attempt is made to access
the value of an optional object that does not contain a value.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Relational operators <a id="optional.relops">[[optional.relops]]</a>

``` cpp
template<class T, class U> constexpr bool operator==(const optional<T>& x, const optional<U>& y);
```

*Mandates:* The expression `*x == *y` is well-formed and its result is
convertible to `bool`.

[*Note 1*: `T` need not be *Cpp17EqualityComparable*. — *end note*]

*Returns:* If `bool(x) != bool(y)`, `false`; otherwise if
`bool(x) == false`, `true`; otherwise `*x == *y`.

*Remarks:* Specializations of this function template for which
`*x == *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator!=(const optional<T>& x, const optional<U>& y);
```

*Mandates:* The expression `*x != *y` is well-formed and its result is
convertible to `bool`.

*Returns:* If `bool(x) != bool(y)`, `true`; otherwise, if
`bool(x) == false`, `false`; otherwise `*x != *y`.

*Remarks:* Specializations of this function template for which
`*x != *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator<(const optional<T>& x, const optional<U>& y);
```

*Mandates:* `*x < *y` is well-formed and its result is convertible to
`bool`.

*Returns:* If `!y`, `false`; otherwise, if `!x`, `true`; otherwise
`*x < *y`.

*Remarks:* Specializations of this function template for which `*x < *y`
is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator>(const optional<T>& x, const optional<U>& y);
```

*Mandates:* The expression `*x > *y` is well-formed and its result is
convertible to `bool`.

*Returns:* If `!x`, `false`; otherwise, if `!y`, `true`; otherwise
`*x > *y`.

*Remarks:* Specializations of this function template for which `*x > *y`
is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator<=(const optional<T>& x, const optional<U>& y);
```

*Mandates:* The expression `*x <= *y` is well-formed and its result is
convertible to `bool`.

*Returns:* If `!x`, `true`; otherwise, if `!y`, `false`; otherwise
`*x <= *y`.

*Remarks:* Specializations of this function template for which
`*x <= *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator>=(const optional<T>& x, const optional<U>& y);
```

*Mandates:* The expression `*x >= *y` is well-formed and its result is
convertible to `bool`.

*Returns:* If `!y`, `true`; otherwise, if `!x`, `false`; otherwise
`*x >= *y`.

*Remarks:* Specializations of this function template for which
`*x >= *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, three_way_comparable_with<T> U>
  constexpr compare_three_way_result_t<T,U>
    operator<=>(const optional<T>& x, const optional<U>& y);
```

*Returns:* If `x && y`, `*x <=> *y`; otherwise `bool(x) <=> bool(y)`.

*Remarks:* Specializations of this function template for which
`*x <=> *y` is a core constant expression are constexpr functions.

### Comparison with `nullopt` <a id="optional.nullops">[[optional.nullops]]</a>

``` cpp
template<class T> constexpr bool operator==(const optional<T>& x, nullopt_t) noexcept;
```

*Returns:* `!x`.

``` cpp
template<class T> constexpr strong_ordering operator<=>(const optional<T>& x, nullopt_t) noexcept;
```

*Returns:* `bool(x) <=> false`.

### Comparison with `T` <a id="optional.comp.with.t">[[optional.comp.with.t]]</a>

``` cpp
template<class T, class U> constexpr bool operator==(const optional<T>& x, const U& v);
```

*Mandates:* The expression `*x == v` is well-formed and its result is
convertible to `bool`.

[*Note 1*: `T` need not be *Cpp17EqualityComparable*. — *end note*]

*Effects:* Equivalent to: `return bool(x) ? *x == v : false;`

``` cpp
template<class T, class U> constexpr bool operator==(const T& v, const optional<U>& x);
```

*Mandates:* The expression `v == *x` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v == *x : false;`

``` cpp
template<class T, class U> constexpr bool operator!=(const optional<T>& x, const U& v);
```

*Mandates:* The expression `*x != v` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x != v : true;`

``` cpp
template<class T, class U> constexpr bool operator!=(const T& v, const optional<U>& x);
```

*Mandates:* The expression `v != *x` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v != *x : true;`

``` cpp
template<class T, class U> constexpr bool operator<(const optional<T>& x, const U& v);
```

*Mandates:* The expression `*x < v` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x < v : true;`

``` cpp
template<class T, class U> constexpr bool operator<(const T& v, const optional<U>& x);
```

*Mandates:* The expression `v < *x` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v < *x : false;`

``` cpp
template<class T, class U> constexpr bool operator>(const optional<T>& x, const U& v);
```

*Mandates:* The expression `*x > v` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x > v : false;`

``` cpp
template<class T, class U> constexpr bool operator>(const T& v, const optional<U>& x);
```

*Mandates:* The expression `v > *x` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v > *x : true;`

``` cpp
template<class T, class U> constexpr bool operator<=(const optional<T>& x, const U& v);
```

*Mandates:* The expression `*x <= v` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x <= v : true;`

``` cpp
template<class T, class U> constexpr bool operator<=(const T& v, const optional<U>& x);
```

*Mandates:* The expression `v <= *x` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v <= *x : false;`

``` cpp
template<class T, class U> constexpr bool operator>=(const optional<T>& x, const U& v);
```

*Mandates:* The expression `*x >= v` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? *x >= v : false;`

``` cpp
template<class T, class U> constexpr bool operator>=(const T& v, const optional<U>& x);
```

*Mandates:* The expression `v >= *x` is well-formed and its result is
convertible to `bool`.

*Effects:* Equivalent to: `return bool(x) ? v >= *x : true;`

``` cpp
template<class T, three_way_comparable_with<T> U>
  constexpr compare_three_way_result_t<T,U>
    operator<=>(const optional<T>& x, const U& v);
```

*Effects:* Equivalent to:
`return bool(x) ? *x <=> v : strong_ordering::less;`

### Specialized algorithms <a id="optional.specalg">[[optional.specalg]]</a>

``` cpp
template<class T> void swap(optional<T>& x, optional<T>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `is_move_constructible_v<T>` is `true` and
`is_swappable_v<T>` is `true`.

*Effects:* Calls `x.swap(y)`.

``` cpp
template<class T> constexpr optional<decay_t<T>> make_optional(T&& v);
```

*Returns:* `optional<decay_t<T>>(std::forward<T>(v))`.

``` cpp
template<class T, class...Args>
  constexpr optional<T> make_optional(Args&&... args);
```

*Effects:* Equivalent to:
`return optional<T>(in_place, std::forward<Args>(args)...);`

``` cpp
template<class T, class U, class... Args>
  constexpr optional<T> make_optional(initializer_list<U> il, Args&&... args);
```

*Effects:* Equivalent to:
`return optional<T>(in_place, il, std::forward<Args>(args)...);`

### Hash support <a id="optional.hash">[[optional.hash]]</a>

``` cpp
template<class T> struct hash<optional<T>>;
```

The specialization `hash<optional<T>>` is enabled [[unord.hash]] if and
only if `hash<remove_const_t<T>>` is enabled. When enabled, for an
object `o` of type `optional<T>`, if `bool(o) == true`, then
`hash<optional<T>>()(o)` evaluates to the same value as
`hash<remove_const_t<T>>()(*o)`; otherwise it evaluates to an
unspecified value. The member functions are not guaranteed to be
`noexcept`.

## Variants <a id="variant">[[variant]]</a>

### In general <a id="variant.general">[[variant.general]]</a>

A variant object holds and manages the lifetime of a value. If the
`variant` holds a value, that value’s type has to be one of the template
argument types given to `variant`. These template arguments are called
alternatives.

### Header `<variant>` synopsis <a id="variant.syn">[[variant.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  // [variant.variant], class template variant
  template<class... Types>
    class variant;

  // [variant.helper], variant helper classes
  template<class T> struct variant_size;                        // not defined
  template<class T> struct variant_size<const T>;
  template<class T>
    inline constexpr size_t variant_size_v = variant_size<T>::value;

  template<class... Types>
    struct variant_size<variant<Types...>>;

  template<size_t I, class T> struct variant_alternative;       // not defined
  template<size_t I, class T> struct variant_alternative<I, const T>;
  template<size_t I, class T>
    using variant_alternative_t = typename variant_alternative<I, T>::type;

  template<size_t I, class... Types>
    struct variant_alternative<I, variant<Types...>>;

  inline constexpr size_t variant_npos = -1;

  // [variant.get], value access
  template<class T, class... Types>
    constexpr bool holds_alternative(const variant<Types...>&) noexcept;

  template<size_t I, class... Types>
    constexpr variant_alternative_t<I, variant<Types...>>& get(variant<Types...>&);
  template<size_t I, class... Types>
    constexpr variant_alternative_t<I, variant<Types...>>&& get(variant<Types...>&&);
  template<size_t I, class... Types>
    constexpr const variant_alternative_t<I, variant<Types...>>& get(const variant<Types...>&);
  template<size_t I, class... Types>
    constexpr const variant_alternative_t<I, variant<Types...>>&& get(const variant<Types...>&&);

  template<class T, class... Types>
    constexpr T& get(variant<Types...>&);
  template<class T, class... Types>
    constexpr T&& get(variant<Types...>&&);
  template<class T, class... Types>
    constexpr const T& get(const variant<Types...>&);
  template<class T, class... Types>
    constexpr const T&& get(const variant<Types...>&&);

  template<size_t I, class... Types>
    constexpr add_pointer_t<variant_alternative_t<I, variant<Types...>>>
      get_if(variant<Types...>*) noexcept;
  template<size_t I, class... Types>
    constexpr add_pointer_t<const variant_alternative_t<I, variant<Types...>>>
      get_if(const variant<Types...>*) noexcept;

  template<class T, class... Types>
    constexpr add_pointer_t<T>
      get_if(variant<Types...>*) noexcept;
  template<class T, class... Types>
    constexpr add_pointer_t<const T>
      get_if(const variant<Types...>*) noexcept;

  // [variant.relops], relational operators
  template<class... Types>
    constexpr bool operator==(const variant<Types...>&, const variant<Types...>&);
  template<class... Types>
    constexpr bool operator!=(const variant<Types...>&, const variant<Types...>&);
  template<class... Types>
    constexpr bool operator<(const variant<Types...>&, const variant<Types...>&);
  template<class... Types>
    constexpr bool operator>(const variant<Types...>&, const variant<Types...>&);
  template<class... Types>
    constexpr bool operator<=(const variant<Types...>&, const variant<Types...>&);
  template<class... Types>
    constexpr bool operator>=(const variant<Types...>&, const variant<Types...>&);
  template<class... Types> requires (three_way_comparable<Types> && ...)
    constexpr common_comparison_category_t<compare_three_way_result_t<Types>...>
      operator<=>(const variant<Types...>&, const variant<Types...>&);

  // [variant.visit], visitation
  template<class Visitor, class... Variants>
    constexpr see below visit(Visitor&&, Variants&&...);
  template<class R, class Visitor, class... Variants>
    constexpr R visit(Visitor&&, Variants&&...);

  // [variant.monostate], class monostate
  struct monostate;

  // [variant.monostate.relops], monostate relational operators
  constexpr bool operator==(monostate, monostate) noexcept;
  constexpr strong_ordering operator<=>(monostate, monostate) noexcept;

  // [variant.specalg], specialized algorithms
  template<class... Types>
    void swap(variant<Types...>&, variant<Types...>&) noexcept(see below);

  // [variant.bad.access], class bad_variant_access
  class bad_variant_access;

  // [variant.hash], hash support
  template<class T> struct hash;
  template<class... Types> struct hash<variant<Types...>>;
  template<> struct hash<monostate>;
}
```

### Class template `variant` <a id="variant.variant">[[variant.variant]]</a>

``` cpp
namespace std {
  template<class... Types>
  class variant {
  public:
    // [variant.ctor], constructors
    constexpr variant() noexcept(see below);
    constexpr variant(const variant&);
    constexpr variant(variant&&) noexcept(see below);

    template<class T>
      constexpr variant(T&&) noexcept(see below);

    template<class T, class... Args>
      constexpr explicit variant(in_place_type_t<T>, Args&&...);
    template<class T, class U, class... Args>
      constexpr explicit variant(in_place_type_t<T>, initializer_list<U>, Args&&...);

    template<size_t I, class... Args>
      constexpr explicit variant(in_place_index_t<I>, Args&&...);
    template<size_t I, class U, class... Args>
      constexpr explicit variant(in_place_index_t<I>, initializer_list<U>, Args&&...);

    // [variant.dtor], destructor
    ~variant();

    // [variant.assign], assignment
    constexpr variant& operator=(const variant&);
    constexpr variant& operator=(variant&&) noexcept(see below);

    template<class T> variant& operator=(T&&) noexcept(see below);

    // [variant.mod], modifiers
    template<class T, class... Args>
      T& emplace(Args&&...);
    template<class T, class U, class... Args>
      T& emplace(initializer_list<U>, Args&&...);
    template<size_t I, class... Args>
      variant_alternative_t<I, variant<Types...>>& emplace(Args&&...);
    template<size_t I, class U, class... Args>
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
of its alternative types or holds no value. When an instance of
`variant` holds a value of alternative type `T`, it means that a value
of type `T`, referred to as the `variant` object’s *contained value*, is
allocated within the storage of the `variant` object. Implementations
are not permitted to use additional storage, such as dynamic memory, to
allocate the contained value. The contained value shall be allocated in
a region of the `variant` storage suitably aligned for all types in
`Types`.

All types in `Types` shall meet the *Cpp17Destructible* requirements (
[[cpp17.destructible]]).

A program that instantiates the definition of `variant` with no template
arguments is ill-formed.

#### Constructors <a id="variant.ctor">[[variant.ctor]]</a>

In the descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`), and `Tᵢ` be the iᵗʰ type in `Types`.

``` cpp
constexpr variant() noexcept(see below);
```

*Constraints:* `is_default_constructible_v<``T₀``>` is `true`.

*Effects:* Constructs a `variant` holding a value-initialized value of
type `T₀`.

*Ensures:* `valueless_by_exception()` is `false` and `index()` is `0`.

*Throws:* Any exception thrown by the value-initialization of `T₀`.

*Remarks:* This function is `constexpr` if and only if the
value-initialization of the alternative type `T₀` would satisfy the
requirements for a constexpr function. The expression inside `noexcept`
is equivalent to `is_nothrow_default_constructible_v<``T₀``>`.

[*Note 1*: See also class `monostate`. — *end note*]

``` cpp
constexpr variant(const variant& w);
```

*Effects:* If `w` holds a value, initializes the `variant` to hold the
same alternative as `w` and direct-initializes the contained value with
`get<j>(w)`, where `j` is `w.index()`. Otherwise, initializes the
`variant` to not hold a value.

*Throws:* Any exception thrown by direct-initializing any `Tᵢ` for all
i.

*Remarks:* This constructor is defined as deleted unless
`is_copy_constructible_v<``Tᵢ``>` is `true` for all i. If
`is_trivially_copy_constructible_v<``Tᵢ``>` is `true` for all i, this
constructor is trivial.

``` cpp
constexpr variant(variant&& w) noexcept(see below);
```

*Constraints:* `is_move_constructible_v<``Tᵢ``>` is `true` for all i.

*Effects:* If `w` holds a value, initializes the `variant` to hold the
same alternative as `w` and direct-initializes the contained value with
`get<j>(std::move(w))`, where `j` is `w.index()`. Otherwise, initializes
the `variant` to not hold a value.

*Throws:* Any exception thrown by move-constructing any `Tᵢ` for all i.

*Remarks:* The expression inside `noexcept` is equivalent to the logical
of `is_nothrow_move_constructible_v<``Tᵢ``>` for all i. If
`is_trivially_move_constructible_v<``Tᵢ``>` is `true` for all i, this
constructor is trivial.

``` cpp
template<class T> constexpr variant(T&& t) noexcept(see below);
```

Let `Tⱼ` be a type that is determined as follows: build an imaginary
function *FUN*(Tᵢ) for each alternative type `Tᵢ` for which `Tᵢ`` x[] =`
`{std::forward<T>(t)};` is well-formed for some invented variable `x`.
The overload *FUN*(Tⱼ) selected by overload resolution for the
expression *FUN*(std::forward\<T\>(t)) defines the alternative `Tⱼ`
which is the type of the contained value after construction.

*Constraints:*

- `sizeof...(Types)` is nonzero,
- `is_same_v<remove_cvref_t<T>, variant>` is `false`,
- `remove_cvref_t<T>` is neither a specialization of `in_place_type_t`
  nor a specialization of `in_place_index_t`,
- `is_constructible_v<``Tⱼ``, T>` is `true`, and
- the expression *FUN*(`std::forward<T>(t))` (with *FUN* being the
  above-mentioned set of imaginary functions) is well-formed.
  \[*Note 1*:
      variant<string, string> v("abc");

  is ill-formed, as both alternative types have an equally viable
  constructor for the argument.
  — *end note*]

*Effects:* Initializes `*this` to hold the alternative type `Tⱼ` and
direct-initializes the contained value as if
direct-non-list-initializing it with `std::forward<T>(t)`.

*Ensures:* `holds_alternative<``Tⱼ``>(*this)` is `true`.

*Throws:* Any exception thrown by the initialization of the selected
alternative `Tⱼ`.

*Remarks:* The expression inside `noexcept` is equivalent to
`is_nothrow_constructible_v<``Tⱼ``, T>`. If `Tⱼ`’s selected constructor
is a constexpr constructor, this constructor is a constexpr constructor.

``` cpp
template<class T, class... Args> constexpr explicit variant(in_place_type_t<T>, Args&&... args);
```

*Constraints:*

- There is exactly one occurrence of `T` in `Types...` and
- `is_constructible_v<T, Args...>` is `true`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`std::forward<Args>(args)...`.

*Ensures:* `holds_alternative<T>(*this)` is `true`.

*Throws:* Any exception thrown by calling the selected constructor of
`T`.

*Remarks:* If `T`’s selected constructor is a constexpr constructor,
this constructor is a constexpr constructor.

``` cpp
template<class T, class U, class... Args>
  constexpr explicit variant(in_place_type_t<T>, initializer_list<U> il, Args&&... args);
```

*Constraints:*

- There is exactly one occurrence of `T` in `Types...` and
- `is_constructible_v<T, initializer_list<U>&, Args...>` is `true`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T` with the arguments
`il, std::forward<Args>(args)...`.

*Ensures:* `holds_alternative<T>(*this)` is `true`.

*Throws:* Any exception thrown by calling the selected constructor of
`T`.

*Remarks:* If `T`’s selected constructor is a constexpr constructor,
this constructor is a constexpr constructor.

``` cpp
template<size_t I, class... Args> constexpr explicit variant(in_place_index_t<I>, Args&&... args);
```

*Constraints:*

- `I` is less than `sizeof...(Types)` and
- `is_constructible_v<``T_I``, Args...>` is `true`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T_I` with the arguments
`std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Throws:* Any exception thrown by calling the selected constructor of
`T_I`.

*Remarks:* If `T_I`’s selected constructor is a constexpr constructor,
this constructor is a constexpr constructor.

``` cpp
template<size_t I, class U, class... Args>
  constexpr explicit variant(in_place_index_t<I>, initializer_list<U> il, Args&&... args);
```

*Constraints:*

- `I` is less than `sizeof...(Types)` and
- `is_constructible_v<``T_I``, initializer_list<U>&, Args...>` is
  `true`.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `T_I` with the arguments
`il, std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Remarks:* If `T_I`’s selected constructor is a constexpr constructor,
this constructor is a constexpr constructor.

#### Destructor <a id="variant.dtor">[[variant.dtor]]</a>

``` cpp
~variant();
```

*Effects:* If `valueless_by_exception()` is `false`, destroys the
currently contained value.

*Remarks:* If `is_trivially_destructible_v<``Tᵢ``>` is `true` for all
`Tᵢ`, then this destructor is trivial.

#### Assignment <a id="variant.assign">[[variant.assign]]</a>

``` cpp
constexpr variant& operator=(const variant& rhs);
```

Let j be `rhs.index()`.

*Effects:*

- If neither `*this` nor `rhs` holds a value, there is no effect.
- Otherwise, if `*this` holds a value but `rhs` does not, destroys the
  value contained in `*this` and sets `*this` to not hold a value.
- Otherwise, if `index() == `j, assigns the value contained in `rhs` to
  the value contained in `*this`.
- Otherwise, if either `is_nothrow_copy_constructible_v<``Tⱼ``>` is
  `true` or `is_nothrow_move_constructible_v<``Tⱼ``>` is `false`,
  equivalent to `emplace<`j`>(get<`j`>(rhs))`.
- Otherwise, equivalent to `operator=(variant(rhs))`.

*Returns:* `*this`.

*Ensures:* `index() == rhs.index()`.

*Remarks:* This operator is defined as deleted unless
`is_copy_constructible_v<``Tᵢ``> &&` `is_copy_assignable_v<``Tᵢ``>` is
`true` for all i. If `is_trivially_copy_constructible_v<``Tᵢ``> &&`
`is_trivially_copy_assignable_v<``Tᵢ``> &&`
`is_trivially_destructible_v<``Tᵢ``>` is `true` for all i, this
assignment operator is trivial.

``` cpp
constexpr variant& operator=(variant&& rhs) noexcept(see below);
```

Let j be `rhs.index()`.

*Constraints:* `is_move_constructible_v<``Tᵢ``> &&`
`is_move_assignable_v<``Tᵢ``>` is `true` for all i.

*Effects:*

- If neither `*this` nor `rhs` holds a value, there is no effect.
- Otherwise, if `*this` holds a value but `rhs` does not, destroys the
  value contained in `*this` and sets `*this` to not hold a value.
- Otherwise, if `index() == `j, assigns `get<`j`>(std::move(rhs))` to
  the value contained in `*this`.
- Otherwise, equivalent to `emplace<`j`>(get<`j`>(std::move(rhs)))`.

*Returns:* `*this`.

*Remarks:* If `is_trivially_move_constructible_v<``Tᵢ``> &&`
`is_trivially_move_assignable_v<``Tᵢ``> &&`
`is_trivially_destructible_v<``Tᵢ``>` is `true` for all i, this
assignment operator is trivial. The expression inside `noexcept` is
equivalent to:
`is_nothrow_move_constructible_v<``Tᵢ``> && is_nothrow_move_assignable_v<``Tᵢ``>`
for all i.

- If an exception is thrown during the call to `Tⱼ`’s move construction
  (with j being `rhs.index()`), the `variant` will hold no value.
- If an exception is thrown during the call to `Tⱼ`’s move assignment,
  the state of the contained value is as defined by the exception safety
  guarantee of `Tⱼ`’s move assignment; `index()` will be j.

``` cpp
template<class T> variant& operator=(T&& t) noexcept(see below);
```

Let `Tⱼ` be a type that is determined as follows: build an imaginary
function *FUN*(Tᵢ) for each alternative type `Tᵢ` for which `Tᵢ`` x[] =`
`{std::forward<T>(t)};` is well-formed for some invented variable `x`.
The overload *FUN*(Tⱼ) selected by overload resolution for the
expression *FUN*(std::forward\<T\>(t)) defines the alternative `Tⱼ`
which is the type of the contained value after assignment.

*Constraints:*

- `is_same_v<remove_cvref_t<T>, variant>` is `false`,
- `is_assignable_v<``Tⱼ``&, T> && is_constructible_v<``Tⱼ``, T>` is
  `true`, and
- the expression *FUN*(std::forward\<T\>(t)) (with *FUN* being the
  above-mentioned set of imaginary functions) is well-formed.
  \[*Note 1*:
      variant<string, string> v;
      v = "abc";

  is ill-formed, as both alternative types have an equally viable
  constructor for the argument.
  — *end note*]

*Effects:*

- If `*this` holds a `Tⱼ`, assigns `std::forward<T>(t)` to the value
  contained in `*this`.
- Otherwise, if `is_nothrow_constructible_v<``Tⱼ``, T> ||`
  `!is_nothrow_move_constructible_v<``Tⱼ``>` is `true`, equivalent to
  `emplace<`j`>(std::forward<T>(t))`.
- Otherwise, equivalent to `operator=(variant(std::forward<T>(t)))`.

*Ensures:* `holds_alternative<``Tⱼ``>(*this)` is `true`, with `Tⱼ`
selected by the imaginary function overload resolution described above.

*Returns:* `*this`.

*Remarks:* The expression inside `noexcept` is equivalent to:

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
template<class T, class... Args> T& emplace(Args&&... args);
```

*Constraints:* `is_constructible_v<T, Args...>` is `true`, and `T`
occurs exactly once in `Types`.

*Effects:* Equivalent to:

``` cpp
return emplace<I>(std::forward<Args>(args)...);
```

where I is the zero-based index of `T` in `Types`.

``` cpp
template<class T, class U, class... Args> T& emplace(initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<T, initializer_list<U>&, Args...>` is
`true`, and `T` occurs exactly once in `Types`.

*Effects:* Equivalent to:

``` cpp
return emplace<I>(il, std::forward<Args>(args)...);
```

where I is the zero-based index of `T` in `Types`.

``` cpp
template<size_t I, class... Args>
  variant_alternative_t<I, variant<Types...>>& emplace(Args&&... args);
```

*Mandates:* `I` < `sizeof...(Types)`.

*Constraints:* `is_constructible_v<``T_I``, Args...>` is `true`.

*Effects:* Destroys the currently contained value if
`valueless_by_exception()` is `false`. Then initializes the contained
value as if direct-non-list-initializing a value of type `T_I` with the
arguments `std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown during the initialization of the
contained value.

*Remarks:* If an exception is thrown during the initialization of the
contained value, the `variant` might not hold a value.

``` cpp
template<size_t I, class U, class... Args>
  variant_alternative_t<I, variant<Types...>>& emplace(initializer_list<U> il, Args&&... args);
```

*Mandates:* `I` < `sizeof...(Types)`.

*Constraints:*
`is_constructible_v<``T_I``, initializer_list<U>&, Args...>` is `true`.

*Effects:* Destroys the currently contained value if
`valueless_by_exception()` is `false`. Then initializes the contained
value as if direct-non-list-initializing a value of type `T_I` with the
arguments `il, std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown during the initialization of the
contained value.

*Remarks:* If an exception is thrown during the initialization of the
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

*Mandates:* `is_move_constructible_v<``Tᵢ``>` is `true` for all i.

*Preconditions:* Lvalues of type `Tᵢ` are
swappable [[swappable.requirements]].

*Effects:*

- If `valueless_by_exception() && rhs.valueless_by_exception()` no
  effect.
- Otherwise, if `index() == rhs.index()`, calls
  `swap(get<`i`>(*this), get<`i`>(rhs))` where i is `index()`.
- Otherwise, exchanges values of `rhs` and `*this`.

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
expression inside `noexcept` is equivalent to the logical of
`is_nothrow_move_constructible_v<``Tᵢ``> && is_nothrow_swappable_v<``Tᵢ``>`
for all i.

### `variant` helper classes <a id="variant.helper">[[variant.helper]]</a>

``` cpp
template<class T> struct variant_size;
```

All specializations of `variant_size` meet the *Cpp17UnaryTypeTrait*
requirements [[meta.rqmts]] with a base characteristic of
`integral_constant<size_t, N>` for some `N`.

``` cpp
template<class T> class variant_size<const T>;
```

Let `VS` denote `variant_size<T>` of the cv-unqualified type `T`. Then
each specialization of the template meets the *Cpp17UnaryTypeTrait*
requirements [[meta.rqmts]] with a base characteristic of
`integral_constant<size_t, VS::value>`.

``` cpp
template<class... Types>
  struct variant_size<variant<Types...>> : integral_constant<size_t, sizeof...(Types)> { };
```

``` cpp
template<size_t I, class T> class variant_alternative<I, const T>;
```

Let `VA` denote `variant_alternative<I, T>` of the cv-unqualified type
`T`. Then each specialization of the template meets the
*Cpp17TransformationTrait* requirements [[meta.rqmts]] with a member
typedef `type` that names the type `add_const_t<VA::type>`.

``` cpp
variant_alternative<I, variant<Types...>>::type
```

*Mandates:* `I` < `sizeof...(Types)`.

*Type:* The type `T_I`.

### Value access <a id="variant.get">[[variant.get]]</a>

``` cpp
template<class T, class... Types>
  constexpr bool holds_alternative(const variant<Types...>& v) noexcept;
```

*Mandates:* The type `T` occurs exactly once in `Types`.

*Returns:* `true` if `index()` is equal to the zero-based index of `T`
in `Types`.

``` cpp
template<size_t I, class... Types>
  constexpr variant_alternative_t<I, variant<Types...>>& get(variant<Types...>& v);
template<size_t I, class... Types>
  constexpr variant_alternative_t<I, variant<Types...>>&& get(variant<Types...>&& v);
template<size_t I, class... Types>
  constexpr const variant_alternative_t<I, variant<Types...>>& get(const variant<Types...>& v);
template<size_t I, class... Types>
  constexpr const variant_alternative_t<I, variant<Types...>>&& get(const variant<Types...>&& v);
```

*Mandates:* `I` < `sizeof...(Types)`.

*Effects:* If `v.index()` is `I`, returns a reference to the object
stored in the `variant`. Otherwise, throws an exception of type
`bad_variant_access`.

``` cpp
template<class T, class... Types> constexpr T& get(variant<Types...>& v);
template<class T, class... Types> constexpr T&& get(variant<Types...>&& v);
template<class T, class... Types> constexpr const T& get(const variant<Types...>& v);
template<class T, class... Types> constexpr const T&& get(const variant<Types...>&& v);
```

*Mandates:* The type `T` occurs exactly once in `Types`.

*Effects:* If `v` holds a value of type `T`, returns a reference to that
value. Otherwise, throws an exception of type `bad_variant_access`.

``` cpp
template<size_t I, class... Types>
  constexpr add_pointer_t<variant_alternative_t<I, variant<Types...>>>
    get_if(variant<Types...>* v) noexcept;
template<size_t I, class... Types>
  constexpr add_pointer_t<const variant_alternative_t<I, variant<Types...>>>
    get_if(const variant<Types...>* v) noexcept;
```

*Mandates:* `I` < `sizeof...(Types)`.

*Returns:* A pointer to the value stored in the `variant`, if
`v != nullptr` and `v->index() == I`. Otherwise, returns `nullptr`.

``` cpp
template<class T, class... Types>
  constexpr add_pointer_t<T>
    get_if(variant<Types...>* v) noexcept;
template<class T, class... Types>
  constexpr add_pointer_t<const T>
    get_if(const variant<Types...>* v) noexcept;
```

*Mandates:* The type `T` occurs exactly once in `Types`.

*Effects:* Equivalent to: `return get_if<`i`>(v);` with i being the
zero-based index of `T` in `Types`.

### Relational operators <a id="variant.relops">[[variant.relops]]</a>

``` cpp
template<class... Types>
  constexpr bool operator==(const variant<Types...>& v, const variant<Types...>& w);
```

*Mandates:* `get<`i`>(v) == get<`i`>(w)` is a valid expression that is
convertible to `bool`, for all i.

*Returns:* If `v.index() != w.index()`, `false`; otherwise if
`v.valueless_by_exception()`, `true`; otherwise
`get<`i`>(v) == get<`i`>(w)` with i being `v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator!=(const variant<Types...>& v, const variant<Types...>& w);
```

*Mandates:* `get<`i`>(v) != get<`i`>(w)` is a valid expression that is
convertible to `bool`, for all i.

*Returns:* If `v.index() != w.index()`, `true`; otherwise if
`v.valueless_by_exception()`, `false`; otherwise
`get<`i`>(v) != get<`i`>(w)` with i being `v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator<(const variant<Types...>& v, const variant<Types...>& w);
```

*Mandates:* `get<`i`>(v) < get<`i`>(w)` is a valid expression that is
convertible to `bool`, for all i.

*Returns:* If `w.valueless_by_exception()`, `false`; otherwise if
`v.valueless_by_exception()`, `true`; otherwise, if
`v.index() < w.index()`, `true`; otherwise if `v.index() > w.index()`,
`false`; otherwise `get<`i`>(v) < get<`i`>(w)` with i being `v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator>(const variant<Types...>& v, const variant<Types...>& w);
```

*Mandates:* `get<`i`>(v) > get<`i`>(w)` is a valid expression that is
convertible to `bool`, for all i.

*Returns:* If `v.valueless_by_exception()`, `false`; otherwise if
`w.valueless_by_exception()`, `true`; otherwise, if
`v.index() > w.index()`, `true`; otherwise if `v.index() < w.index()`,
`false`; otherwise `get<`i`>(v) > get<`i`>(w)` with i being `v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator<=(const variant<Types...>& v, const variant<Types...>& w);
```

*Mandates:* `get<`i`>(v) <= get<`i`>(w)` is a valid expression that is
convertible to `bool`, for all i.

*Returns:* If `v.valueless_by_exception()`, `true`; otherwise if
`w.valueless_by_exception()`, `false`; otherwise, if
`v.index() < w.index()`, `true`; otherwise if `v.index() > w.index()`,
`false`; otherwise `get<`i`>(v) <= get<`i`>(w)` with i being
`v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator>=(const variant<Types...>& v, const variant<Types...>& w);
```

*Mandates:* `get<`i`>(v) >= get<`i`>(w)` is a valid expression that is
convertible to `bool`, for all i.

*Returns:* If `w.valueless_by_exception()`, `true`; otherwise if
`v.valueless_by_exception()`, `false`; otherwise, if
`v.index() > w.index()`, `true`; otherwise if `v.index() < w.index()`,
`false`; otherwise `get<`i`>(v) >= get<`i`>(w)` with i being
`v.index()`.

``` cpp
template<class... Types> requires (three_way_comparable<Types> && ...)
  constexpr common_comparison_category_t<compare_three_way_result_t<Types>...>
    operator<=>(const variant<Types...>& v, const variant<Types...>& w);
```

*Effects:* Equivalent to:

``` cpp
if (v.valueless_by_exception() && w.valueless_by_exception())
  return strong_ordering::equal;
if (v.valueless_by_exception()) return strong_ordering::less;
if (w.valueless_by_exception()) return strong_ordering::greater;
if (auto c = v.index() <=> w.index(); c != 0) return c;
return get<i>(v) <=> get<i>(w);
```

with i being `v.index()`.

### Visitation <a id="variant.visit">[[variant.visit]]</a>

``` cpp
template<class Visitor, class... Variants>
  constexpr see below visit(Visitor&& vis, Variants&&... vars);
template<class R, class Visitor, class... Variants>
  constexpr R visit(Visitor&& vis, Variants&&... vars);
```

Let n be `sizeof...(Variants)`. Let `m` be a pack of n values of type
`size_t`. Such a pack is called valid if 0 ≤
`mᵢ` < `variant_size_v<remove_reference_t<Variantsᵢ``>>` for all
0 ≤ i < n. For each valid pack `m`, let e(`m`) denote the expression:

``` cpp
INVOKE(std::forward<Visitor>(vis), get<m>(std::forward<Variants>(vars))...) // see REF:func.require
```

for the first form and

``` cpp
INVOKE<R>(std::forward<Visitor>(vis), get<m>(std::forward<Variants>(vars))...) // see REF:func.require
```

for the second form.

*Mandates:* For each valid pack `m`, e(`m`) is a valid expression. All
such expressions are of the same type and value category.

*Returns:* e(`m`), where `m` is the pack for which `mᵢ` is
`vars`ᵢ`.index()` for all 0 ≤ i < n. The return type is
`decltype(`e(`m`)`)` for the first form.

*Throws:* `bad_variant_access` if any `variant` in `vars` is
`valueless_by_exception()`.

*Complexity:* For n ≤ 1, the invocation of the callable object is
implemented in constant time, i.e., for n = 1, it does not depend on the
number of alternative types of `Variants₀`. For n > 1, the invocation of
the callable object has no complexity requirements.

### Class `monostate` <a id="variant.monostate">[[variant.monostate]]</a>

``` cpp
struct monostate{};
```

The class `monostate` can serve as a first alternative type for a
`variant` to make the `variant` type default constructible.

### `monostate` relational operators <a id="variant.monostate.relops">[[variant.monostate.relops]]</a>

``` cpp
constexpr bool operator==(monostate, monostate) noexcept { return true; }
constexpr strong_ordering operator<=>(monostate, monostate) noexcept
{ return strong_ordering::equal; }
```

[*Note 1*: `monostate` objects have only a single state; they thus
always compare equal. — *end note*]

### Specialized algorithms <a id="variant.specalg">[[variant.specalg]]</a>

``` cpp
template<class... Types>
  void swap(variant<Types...>& v, variant<Types...>& w) noexcept(see below);
```

*Constraints:*
`is_move_constructible_v<``Tᵢ``> && is_swappable_v<``Tᵢ``>` is `true`
for all i.

*Effects:* Equivalent to `v.swap(w)`.

*Remarks:* The expression inside `noexcept` is equivalent to
`noexcept(v.swap(w))`.

### Class `bad_variant_access` <a id="variant.bad.access">[[variant.bad.access]]</a>

``` cpp
class bad_variant_access : public exception {
public:
  // see [exception] for the specification of the special member functions
  const char* what() const noexcept override;
};
```

Objects of type `bad_variant_access` are thrown to report invalid
accesses to the value of a `variant` object.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Hash support <a id="variant.hash">[[variant.hash]]</a>

``` cpp
template<class... Types> struct hash<variant<Types...>>;
```

The specialization `hash<variant<Types...>>` is enabled [[unord.hash]]
if and only if every specialization in `hash<remove_const_t<Types>>...`
is enabled. The member functions are not guaranteed to be `noexcept`.

``` cpp
template<> struct hash<monostate>;
```

The specialization is enabled [[unord.hash]].

## Storage for any type <a id="any">[[any]]</a>

This subclause describes components that C++ programs may use to perform
operations on objects of a discriminated type.

[*Note 1*: The discriminated type may contain values of different types
but does not attempt conversion between them, i.e., `5` is held strictly
as an `int` and is not implicitly convertible either to `"5"` or to
`5.0`. This indifference to interpretation but awareness of type
effectively allows safe, generic containers of single values, with no
scope for surprises from ambiguous conversions. — *end note*]

### Header `<any>` synopsis <a id="any.synop">[[any.synop]]</a>

``` cpp
namespace std {
  // [any.bad.any.cast], class bad_any_cast
  class bad_any_cast;

  // [any.class], class any
  class any;

  // [any.nonmembers], non-member functions
  void swap(any& x, any& y) noexcept;

  template<class T, class... Args>
    any make_any(Args&&... args);
  template<class T, class U, class... Args>
    any make_any(initializer_list<U> il, Args&&... args);

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

### Class `bad_any_cast` <a id="any.bad.any.cast">[[any.bad.any.cast]]</a>

``` cpp
class bad_any_cast : public bad_cast {
public:
  // see [exception] for the specification of the special member functions
  const char* what() const noexcept override;
};
```

Objects of type `bad_any_cast` are thrown by a failed `any_cast`
[[any.nonmembers]].

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Class `any` <a id="any.class">[[any.class]]</a>

``` cpp
namespace std {
  class any {
  public:
    // [any.cons], construction and destruction
    constexpr any() noexcept;

    any(const any& other);
    any(any&& other) noexcept;

    template<class T>
      any(T&& value);

    template<class T, class... Args>
      explicit any(in_place_type_t<T>, Args&&...);
    template<class T, class U, class... Args>
      explicit any(in_place_type_t<T>, initializer_list<U>, Args&&...);

    ~any();

    // [any.assign], assignments
    any& operator=(const any& rhs);
    any& operator=(any&& rhs) noexcept;

    template<class T>
      any& operator=(T&& rhs);

    // [any.modifiers], modifiers
    template<class T, class... Args>
      decay_t<T>& emplace(Args&&...);
    template<class T, class U, class... Args>
      decay_t<T>& emplace(initializer_list<U>, Args&&...);
    void reset() noexcept;
    void swap(any& rhs) noexcept;

    // [any.observers], observers
    bool has_value() const noexcept;
    const type_info& type() const noexcept;
  };
}
```

An object of class `any` stores an instance of any type that meets the
constructor requirements or it has no value, and this is referred to as
the *state* of the class `any` object. The stored instance is called the
*contained value*. Two states are equivalent if either they both have no
value, or they both have a value and the contained values are
equivalent.

The non-member `any_cast` functions provide type-safe access to the
contained value.

Implementations should avoid the use of dynamically allocated memory for
a small contained value. However, any such small-object optimization
shall only be applied to types `T` for which
`is_nothrow_move_constructible_v<T>` is `true`.

[*Example 1*: A contained value of type `int` could be stored in an
internal buffer, not in separately-allocated memory. — *end example*]

#### Construction and destruction <a id="any.cons">[[any.cons]]</a>

``` cpp
constexpr any() noexcept;
```

*Ensures:* `has_value()` is `false`.

``` cpp
any(const any& other);
```

*Effects:* If `other.has_value()` is `false`, constructs an object that
has no value. Otherwise, equivalent to
`any(in_place_type<T>, any_cast<const T&>(other))` where `T` is the type
of the contained value.

*Throws:* Any exceptions arising from calling the selected constructor
for the contained value.

``` cpp
any(any&& other) noexcept;
```

*Effects:* If `other.has_value()` is `false`, constructs an object that
has no value. Otherwise, constructs an object of type `any` that
contains either the contained value of `other`, or contains an object of
the same type constructed from the contained value of `other`
considering that contained value as an rvalue.

``` cpp
template<class T>
  any(T&& value);
```

Let `VT` be `decay_t<T>`.

*Constraints:* `VT` is not the same type as `any`, `VT` is not a
specialization of `in_place_type_t`, and `is_copy_constructible_v<VT>`
is `true`.

*Preconditions:* `VT` meets the *Cpp17CopyConstructible* requirements.

*Effects:* Constructs an object of type `any` that contains an object of
type `VT` direct-initialized with `std::forward<T>(value)`.

*Throws:* Any exception thrown by the selected constructor of `VT`.

``` cpp
template<class T, class... Args>
  explicit any(in_place_type_t<T>, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:* `is_copy_constructible_v<VT>` is `true` and
`is_constructible_v<VT, Args...>` is `true`.

*Preconditions:* `VT` meets the *Cpp17CopyConstructible* requirements.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value of type `VT`.

*Throws:* Any exception thrown by the selected constructor of `VT`.

``` cpp
template<class T, class U, class... Args>
  explicit any(in_place_type_t<T>, initializer_list<U> il, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:* `is_copy_constructible_v<VT>` is `true` and
`is_constructible_v<VT, initializer_list<U>&, Args...>` is `true`.

*Preconditions:* `VT` meets the *Cpp17CopyConstructible* requirements.

*Effects:* Initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`il, std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `VT`.

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

*Ensures:* The state of `*this` is equivalent to the original state of
`rhs`.

``` cpp
template<class T>
  any& operator=(T&& rhs);
```

Let `VT` be `decay_t<T>`.

*Constraints:* `VT` is not the same type as `any` and
`is_copy_constructible_v<VT>` is `true`.

*Preconditions:* `VT` meets the *Cpp17CopyConstructible* requirements.

*Effects:* Constructs an object `tmp` of type `any` that contains an
object of type `VT` direct-initialized with `std::forward<T>(rhs)`, and
`tmp.swap(*this)`. No effects if an exception is thrown.

*Returns:* `*this`.

*Throws:* Any exception thrown by the selected constructor of `VT`.

#### Modifiers <a id="any.modifiers">[[any.modifiers]]</a>

``` cpp
template<class T, class... Args>
  decay_t<T>& emplace(Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:* `is_copy_constructible_v<VT>` is `true` and
`is_constructible_v<VT, Args...>` is `true`.

*Preconditions:* `VT` meets the *Cpp17CopyConstructible* requirements.

*Effects:* Calls `reset()`. Then initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `VT`.

*Remarks:* If an exception is thrown during the call to `VT`’s
constructor, `*this` does not contain a value, and any previously
contained value has been destroyed.

``` cpp
template<class T, class U, class... Args>
  decay_t<T>& emplace(initializer_list<U> il, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:* `is_copy_constructible_v<VT>` is `true` and
`is_constructible_v<VT, initializer_list<U>&, Args...>` is `true`.

*Preconditions:* `VT` meets the *Cpp17CopyConstructible* requirements.

*Effects:* Calls `reset()`. Then initializes the contained value as if
direct-non-list-initializing an object of type `VT` with the arguments
`il, std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `VT`.

*Remarks:* If an exception is thrown during the call to `VT`’s
constructor, `*this` does not contain a value, and any previously
contained value has been destroyed.

``` cpp
void reset() noexcept;
```

*Effects:* If `has_value()` is `true`, destroys the contained value.

*Ensures:* `has_value()` is `false`.

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

*Effects:* Equivalent to `x.swap(y)`.

``` cpp
template<class T, class... Args>
  any make_any(Args&&... args);
```

*Effects:* Equivalent to:
`return any(in_place_type<T>, std::forward<Args>(args)...);`

``` cpp
template<class T, class U, class... Args>
  any make_any(initializer_list<U> il, Args&&... args);
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

Let `U` be the type `remove_cvref_t<T>`.

*Mandates:* For the first overload, `is_constructible_v<T, const U&>` is
`true`. For the second overload, `is_constructible_v<T, U&>` is `true`.
For the third overload, `is_constructible_v<T, U>` is `true`.

*Returns:* For the first and second overload,
`static_cast<T>(*any_cast<U>(&operand))`. For the third overload,
`static_cast<T>(std::move(*any_cast<U>(&operand)))`.

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

any_cast<string&>(y);                       // error: cannot any_cast away const
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

The header `<bitset>` defines a class template and several related
functions for representing and manipulating fixed-size sequences of
bits.

``` cpp
#include <string>
#include <iosfwd>   // for istream[istream.syn], ostream[ostream.syn], see [iosfwd.syn]

namespace std {
  template<size_t N> class bitset;

  // [bitset.operators], bitset operators
  template<size_t N>
    bitset<N> operator&(const bitset<N>&, const bitset<N>&) noexcept;
  template<size_t N>
    bitset<N> operator|(const bitset<N>&, const bitset<N>&) noexcept;
  template<size_t N>
    bitset<N> operator^(const bitset<N>&, const bitset<N>&) noexcept;
  template<class charT, class traits, size_t N>
    basic_istream<charT, traits>&
      operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
  template<class charT, class traits, size_t N>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const bitset<N>& x);
}
```

### Class template `bitset` <a id="template.bitset">[[template.bitset]]</a>

``` cpp
namespace std {
  template<size_t N> class bitset {
  public:
    // bit reference
    class reference {
      friend class bitset;
      reference() noexcept;

    public:
      reference(const reference&) = default;
      ~reference();
      reference& operator=(bool x) noexcept;            // for b[i] = x;
      reference& operator=(const reference&) noexcept;  // for b[i] = b[j];
      bool operator~() const noexcept;                  // flips the bit
      operator bool() const noexcept;                   // for x = b[i];
      reference& flip() noexcept;                       // for b[i].flip();
    };

    // [bitset.cons], constructors
    constexpr bitset() noexcept;
    constexpr bitset(unsigned long long val) noexcept;
    template<class charT, class traits, class Allocator>
      explicit bitset(
        const basic_string<charT, traits, Allocator>& str,
        typename basic_string<charT, traits, Allocator>::size_type pos = 0,
        typename basic_string<charT, traits, Allocator>::size_type n
          = basic_string<charT, traits, Allocator>::npos,
        charT zero = charT('0'),
        charT one = charT('1'));
    template<class charT>
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

    // element access
    constexpr bool operator[](size_t pos) const;        // for b[i];
    reference operator[](size_t pos);                   // for b[i];

    unsigned long to_ulong() const;
    unsigned long long to_ullong() const;
    template<class charT = char,
             class traits = char_traits<charT>,
             class Allocator = allocator<charT>>
      basic_string<charT, traits, Allocator>
        to_string(charT zero = charT('0'), charT one = charT('1')) const;

    size_t count() const noexcept;
    constexpr size_t size() const noexcept;
    bool operator==(const bitset<N>& rhs) const noexcept;
    bool test(size_t pos) const;
    bool all() const noexcept;
    bool any() const noexcept;
    bool none() const noexcept;
    bitset<N> operator<<(size_t pos) const noexcept;
    bitset<N> operator>>(size_t pos) const noexcept;
  };

  // [bitset.hash], hash support
  template<class T> struct hash;
  template<size_t N> struct hash<bitset<N>>;
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
  `invalid_argument` [[invalid.argument]];
- an *out-of-range* error is associated with exceptions of type
  `out_of_range` [[out.of.range]];
- an *overflow* error is associated with exceptions of type
  `overflow_error` [[overflow.error]].

#### Constructors <a id="bitset.cons">[[bitset.cons]]</a>

``` cpp
constexpr bitset() noexcept;
```

*Effects:* Initializes all bits in `*this` to zero.

``` cpp
constexpr bitset(unsigned long long val) noexcept;
```

*Effects:* Initializes the first `M` bit positions to the corresponding
bit values in `val`. `M` is the smaller of `N` and the number of bits in
the value representation [[basic.types]] of `unsigned long long`. If
`M < N`, the remaining bit positions are initialized to zero.

``` cpp
template<class charT, class traits, class Allocator>
  explicit bitset(
    const basic_string<charT, traits, Allocator>& str,
    typename basic_string<charT, traits, Allocator>::size_type pos = 0,
    typename basic_string<charT, traits, Allocator>::size_type n
      = basic_string<charT, traits, Allocator>::npos,
    charT zero = charT('0'),
    charT one = charT('1'));
```

*Effects:* Determines the effective length `rlen` of the initializing
string as the smaller of `n` and `str.size() - pos`. Initializes the
first `M` bit positions to values determined from the corresponding
characters in the string `str`. `M` is the smaller of `N` and `rlen`.

An element of the constructed object has value zero if the corresponding
character in `str`, beginning at position `pos`, is `zero`. Otherwise,
the element has the value one. Character position `pos + M - 1`
corresponds to bit position zero. Subsequent decreasing character
positions correspond to increasing bit positions.

If `M < N`, remaining bit positions are initialized to zero.

The function uses `traits::eq` to compare the character values.

*Throws:* `out_of_range` if `pos > str.size()` or `invalid_argument` if
any of the `rlen` characters in `str` beginning at position `pos` is
other than `zero` or `one`.

``` cpp
template<class charT>
  explicit bitset(
    const charT* str,
    typename basic_string<charT>::size_type n = basic_string<charT>::npos,
    charT zero = charT('0'),
    charT one = charT('1'));
```

*Effects:* As if by:

``` cpp
bitset(n == basic_string<charT>::npos
          ? basic_string<charT>(str)
          : basic_string<charT>(str, n),
       0, n, zero, one)
```

#### Members <a id="bitset.members">[[bitset.members]]</a>

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

*Effects:* Stores a new value in the bit at position `pos` in `*this`.
If `val` is `true`, the stored value is one, otherwise it is zero.

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

``` cpp
bitset<N>& reset() noexcept;
```

*Effects:* Resets all bits in `*this`.

*Returns:* `*this`.

``` cpp
bitset<N>& reset(size_t pos);
```

*Effects:* Resets the bit at position `pos` in `*this`.

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

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

*Effects:* Toggles the bit at position `pos` in `*this`.

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

``` cpp
unsigned long to_ulong() const;
```

*Returns:* `x`.

*Throws:* `overflow_error` if the integral value `x` corresponding to
the bits in `*this` cannot be represented as type `unsigned long`.

``` cpp
unsigned long long to_ullong() const;
```

*Returns:* `x`.

*Throws:* `overflow_error` if the integral value `x` corresponding to
the bits in `*this` cannot be represented as type `unsigned long long`.

``` cpp
template<class charT = char,
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
bool test(size_t pos) const;
```

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

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

*Preconditions:* `pos` is valid.

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one, otherwise `false`.

*Throws:* Nothing.

``` cpp
bitset<N>::reference operator[](size_t pos);
```

*Preconditions:* `pos` is valid.

*Returns:* An object of type `bitset<N>::reference` such that
`(*this)[pos] == this->test(pos)`, and such that `(*this)[pos] = val` is
equivalent to `this->set(pos, val)`.

*Throws:* Nothing.

*Remarks:* For the purpose of determining the presence of a data
race [[intro.multithread]], any access or update through the resulting
reference potentially accesses or modifies, respectively, the entire
underlying bitset.

### `bitset` hash support <a id="bitset.hash">[[bitset.hash]]</a>

``` cpp
template<size_t N> struct hash<bitset<N>>;
```

The specialization is enabled [[unord.hash]].

### `bitset` operators <a id="bitset.operators">[[bitset.operators]]</a>

``` cpp
bitset<N> operator&(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) &= rhs`.

``` cpp
bitset<N> operator|(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) |= rhs`.

``` cpp
bitset<N> operator^(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) ^= rhs`.

``` cpp
template<class charT, class traits, size_t N>
  basic_istream<charT, traits>&
    operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
```

A formatted input function [[istream.formatted]].

*Effects:* Extracts up to `N` characters from `is`. Stores these
characters in a temporary object `str` of type
`basic_string<charT, traits>`, then evaluates the expression
`x = bitset<N>(str)`. Characters are extracted and stored until any of
the following occurs:

- `N` characters have been extracted and stored;
- end-of-file occurs on the input sequence;
- the next input character is neither `is.widen(’0’)` nor
  `is.widen(’1’)` (in which case the input character is not extracted).

If `N > 0` and no characters are stored in `str`, calls
`is.setstate(ios_base::failbit)` (which may throw
`ios_base::failure`[[iostate.flags]]).

*Returns:* `is`.

``` cpp
template<class charT, class traits, size_t N>
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

Subclause  [[memory]] describes the contents of the header `<memory>`
and some of the contents of the header `<cstdlib>`.

### Header `<memory>` synopsis <a id="memory.syn">[[memory.syn]]</a>

The header `<memory>` defines several types and function templates that
describe properties of pointers and pointer-like types, manage memory
for containers and other template types, destroy objects, and construct
objects in uninitialized memory buffers ([[pointer.traits]]–
[[specialized.addressof]] and [[specialized.algorithms]]). The header
also defines the templates `unique_ptr`, `shared_ptr`, `weak_ptr`, and
various function templates that operate on objects of these types
[[smartptr]].

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  // [pointer.traits], pointer traits
  template<class Ptr> struct pointer_traits;
  template<class T> struct pointer_traits<T*>;

  // [pointer.conversion], pointer conversion
  template<class T>
    constexpr T* to_address(T* p) noexcept;
  template<class Ptr>
    constexpr auto to_address(const Ptr& p) noexcept;

  // [util.dynamic.safety], pointer safety%
%
{pointer_safety{pointer_safety{pointer_safety}
  enum class pointer_safety { relaxed, preferred, strict };
  void declare_reachable(void* p);
  template<class T>
    T* undeclare_reachable(T* p);
  void declare_no_pointers(char* p, size_t n);
  void undeclare_no_pointers(char* p, size_t n);
  pointer_safety get_pointer_safety() noexcept;

  // [ptr.align], pointer alignment
  void* align(size_t alignment, size_t size, void*& ptr, size_t& space);
  template<size_t N, class T>
    [[nodiscard]] constexpr T* assume_aligned(T* ptr);

  // [allocator.tag], allocator argument tag
  struct allocator_arg_t { explicit allocator_arg_t() = default; };
  inline constexpr allocator_arg_t allocator_arg{};

  // [allocator.uses], uses_allocator
  template<class T, class Alloc> struct uses_allocator;

  // [allocator.uses.trait], uses_allocator
  template<class T, class Alloc>
    inline constexpr bool uses_allocator_v = uses_allocator<T, Alloc>::value;

  // [allocator.uses.construction], uses-allocator construction
  template<class T, class Alloc, class... Args>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                    Args&&... args) noexcept -> see below;
  template<class T, class Alloc, class Tuple1, class Tuple2>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc, piecewise_construct_t,
                                                    Tuple1&& x, Tuple2&& y)
                                                    noexcept ->  see below;
  template<class T, class Alloc>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc) noexcept -> see below;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                    U&& u, V&& v) noexcept -> see below;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                    const pair<U,V>& pr) noexcept -> see below;
  template<class T, class Alloc, class U, class V>
    constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                    pair<U,V>&& pr) noexcept -> see below;
  template<class T, class Alloc, class... Args>
    constexpr T make_obj_using_allocator(const Alloc& alloc, Args&&... args);
  template<class T, class Alloc, class... Args>
    constexpr T* uninitialized_construct_using_allocator(T* p, const Alloc& alloc,
                                                         Args&&... args);

  // [allocator.traits], allocator traits
  template<class Alloc> struct allocator_traits;

  // [default.allocator], the default allocator
  template<class T> class allocator;
  template<class T, class U>
    constexpr bool operator==(const allocator<T>&, const allocator<U>&) noexcept;

  // [specialized.addressof], addressof
  template<class T>
    constexpr T* addressof(T& r) noexcept;
  template<class T>
    const T* addressof(const T&&) = delete;

  // [specialized.algorithms], specialized algorithms
  // [special.mem.concepts], special memory concepts
  template<class I>
    concept no-throw-input-iterator = see below;    // exposition only
  template<class I>
    concept no-throw-forward-iterator = see below;  // exposition only
  template<class S, class I>
    concept no-throw-sentinel = see below;          // exposition only
  template<class R>
    concept no-throw-input-range = see below;       // exposition only
  template<class R>
    concept no-throw-forward-range = see below;     // exposition only

  template<class NoThrowForwardIterator>
    void uninitialized_default_construct(NoThrowForwardIterator first,
                                         NoThrowForwardIterator last);
  template<class ExecutionPolicy, class NoThrowForwardIterator>
    void uninitialized_default_construct(ExecutionPolicy&& exec,        // see [algorithms.parallel.overloads]
                                         NoThrowForwardIterator first,
                                         NoThrowForwardIterator last);
  template<class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_default_construct_n(NoThrowForwardIterator first, Size n);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_default_construct_n(ExecutionPolicy&& exec,         // see [algorithms.parallel.overloads]
                                        NoThrowForwardIterator first, Size n);

  namespace ranges {
    template<no-throw-forward-iterator I, no-throw-sentinel<I> S>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_default_construct(I first, S last);
    template<no-throw-forward-range R>
      requires default_initializable<range_value_t<R>>
        borrowed_iterator_t<R> uninitialized_default_construct(R&& r);

    template<no-throw-forward-iterator I>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_default_construct_n(I first, iter_difference_t<I> n);
  }

  template<class NoThrowForwardIterator>
    void uninitialized_value_construct(NoThrowForwardIterator first,
                                       NoThrowForwardIterator last);
  template<class ExecutionPolicy, class NoThrowForwardIterator>
    void uninitialized_value_construct(ExecutionPolicy&& exec,  // see [algorithms.parallel.overloads]
                                       NoThrowForwardIterator first,
                                       NoThrowForwardIterator last);
  template<class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_value_construct_n(NoThrowForwardIterator first, Size n);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator
      uninitialized_value_construct_n(ExecutionPolicy&& exec,   // see [algorithms.parallel.overloads]
                                      NoThrowForwardIterator first, Size n);

  namespace ranges {
    template<no-throw-forward-iterator I, no-throw-sentinel<I> S>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_value_construct(I first, S last);
    template<no-throw-forward-range R>
      requires default_initializable<range_value_t<R>>
        borrowed_iterator_t<R> uninitialized_value_construct(R&& r);

    template<no-throw-forward-iterator I>
      requires default_initializable<iter_value_t<I>>
        I uninitialized_value_construct_n(I first, iter_difference_t<I> n);
  }

  template<class InputIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy(InputIterator first, InputIterator last,
                                              NoThrowForwardIterator result);
  template<class ExecutionPolicy, class InputIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy(ExecutionPolicy&& exec,   // see [algorithms.parallel.overloads]
                                              InputIterator first, InputIterator last,
                                              NoThrowForwardIterator result);
  template<class InputIterator, class Size, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy_n(InputIterator first, Size n,
                                                NoThrowForwardIterator result);
  template<class ExecutionPolicy, class InputIterator, class Size, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_copy_n(ExecutionPolicy&& exec, // see [algorithms.parallel.overloads]
                                                InputIterator first, Size n,
                                                NoThrowForwardIterator result);

  namespace ranges {
    template<class I, class O>
      using uninitialized_copy_result = in_out_result<I, O>;
    template<input_iterator I, sentinel_for<I> S1,
             no-throw-forward-iterator O, no-throw-sentinel<O> S2>
      requires constructible_from<iter_value_t<O>, iter_reference_t<I>>
        uninitialized_copy_result<I, O>
          uninitialized_copy(I ifirst, S1 ilast, O ofirst, S2 olast);
    template<input_range IR, no-throw-forward-range OR>
      requires constructible_from<range_value_t<OR>, range_reference_t<IR>>
        uninitialized_copy_result<borrowed_iterator_t<IR>, borrowed_iterator_t<OR>>
          uninitialized_copy(IR&& in_range, OR&& out_range);

    template<class I, class O>
      using uninitialized_copy_n_result = in_out_result<I, O>;
    template<input_iterator I, no-throw-forward-iterator O, no-throw-sentinel<O> S>
      requires constructible_from<iter_value_t<O>, iter_reference_t<I>>
        uninitialized_copy_n_result<I, O>
          uninitialized_copy_n(I ifirst, iter_difference_t<I> n, O ofirst, S olast);
  }

  template<class InputIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_move(InputIterator first, InputIterator last,
                                              NoThrowForwardIterator result);
  template<class ExecutionPolicy, class InputIterator, class NoThrowForwardIterator>
    NoThrowForwardIterator uninitialized_move(ExecutionPolicy&& exec,   // see [algorithms.parallel.overloads]
                                              InputIterator first, InputIterator last,
                                              NoThrowForwardIterator result);
  template<class InputIterator, class Size, class NoThrowForwardIterator>
    pair<InputIterator, NoThrowForwardIterator>
      uninitialized_move_n(InputIterator first, Size n, NoThrowForwardIterator result);
  template<class ExecutionPolicy, class InputIterator, class Size, class NoThrowForwardIterator>
    pair<InputIterator, NoThrowForwardIterator>
      uninitialized_move_n(ExecutionPolicy&& exec,              // see [algorithms.parallel.overloads]
                           InputIterator first, Size n, NoThrowForwardIterator result);

  namespace ranges {
    template<class I, class O>
      using uninitialized_move_result = in_out_result<I, O>;
    template<input_iterator I, sentinel_for<I> S1,
             no-throw-forward-iterator O, no-throw-sentinel<O> S2>
      requires constructible_from<iter_value_t<O>, iter_rvalue_reference_t<I>>
        uninitialized_move_result<I, O>
          uninitialized_move(I ifirst, S1 ilast, O ofirst, S2 olast);
    template<input_range IR, no-throw-forward-range OR>
      requires constructible_from<range_value_t<OR>, range_rvalue_reference_t<IR>>
        uninitialized_move_result<borrowed_iterator_t<IR>, borrowed_iterator_t<OR>>
          uninitialized_move(IR&& in_range, OR&& out_range);

    template<class I, class O>
      using uninitialized_move_n_result = in_out_result<I, O>;
    template<input_iterator I,
             no-throw-forward-iterator O, no-throw-sentinel<O> S>
      requires constructible_from<iter_value_t<O>, iter_rvalue_reference_t<I>>
        uninitialized_move_n_result<I, O>
          uninitialized_move_n(I ifirst, iter_difference_t<I> n, O ofirst, S olast);
  }

  template<class NoThrowForwardIterator, class T>
    void uninitialized_fill(NoThrowForwardIterator first, NoThrowForwardIterator last,
                            const T& x);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class T>
    void uninitialized_fill(ExecutionPolicy&& exec,             // see [algorithms.parallel.overloads]
                            NoThrowForwardIterator first, NoThrowForwardIterator last,
                            const T& x);
  template<class NoThrowForwardIterator, class Size, class T>
    NoThrowForwardIterator
      uninitialized_fill_n(NoThrowForwardIterator first, Size n, const T& x);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size, class T>
    NoThrowForwardIterator
      uninitialized_fill_n(ExecutionPolicy&& exec,              // see [algorithms.parallel.overloads]
                           NoThrowForwardIterator first, Size n, const T& x);

  namespace ranges {
    template<no-throw-forward-iterator I, no-throw-sentinel<I> S, class T>
      requires constructible_from<iter_value_t<I>, const T&>
        I uninitialized_fill(I first, S last, const T& x);
    template<no-throw-forward-range R, class T>
      requires constructible_from<range_value_t<R>, const T&>
        borrowed_iterator_t<R> uninitialized_fill(R&& r, const T& x);

    template<no-throw-forward-iterator I, class T>
      requires constructible_from<iter_value_t<I>, const T&>
        I uninitialized_fill_n(I first, iter_difference_t<I> n, const T& x);
  }

  // [specialized.construct], construct_at
  template<class T, class... Args>
    constexpr T* construct_at(T* location, Args&&... args);

  namespace ranges {
    template<class T, class... Args>
      constexpr T* construct_at(T* location, Args&&... args);
  }

  // [specialized.destroy], destroy
  template<class T>
    constexpr void destroy_at(T* location);
  template<class NoThrowForwardIterator>
    constexpr void destroy(NoThrowForwardIterator first, NoThrowForwardIterator last);
  template<class ExecutionPolicy, class NoThrowForwardIterator>
    void destroy(ExecutionPolicy&& exec,                        // see [algorithms.parallel.overloads]
                 NoThrowForwardIterator first, NoThrowForwardIterator last);
  template<class NoThrowForwardIterator, class Size>
    constexpr NoThrowForwardIterator destroy_n(NoThrowForwardIterator first, Size n);
  template<class ExecutionPolicy, class NoThrowForwardIterator, class Size>
    NoThrowForwardIterator destroy_n(ExecutionPolicy&& exec,    // see [algorithms.parallel.overloads]
                                     NoThrowForwardIterator first, Size n);

  namespace ranges {
    template<destructible T>
      constexpr void destroy_at(T* location) noexcept;

    template<no-throw-input-iterator I, no-throw-sentinel<I> S>
      requires destructible<iter_value_t<I>>
        constexpr I destroy(I first, S last) noexcept;
    template<no-throw-input-range R>
      requires destructible<range_value_t<R>>
        constexpr borrowed_iterator_t<R> destroy(R&& r) noexcept;

    template<no-throw-input-iterator I>
      requires destructible<iter_value_t<I>>
        constexpr I destroy_n(I first, iter_difference_t<I> n) noexcept;
  }

  // [unique.ptr], class template unique_ptr
  template<class T> struct default_delete;
  template<class T> struct default_delete<T[]>;
  template<class T, class D = default_delete<T>> class unique_ptr;
  template<class T, class D> class unique_ptr<T[], D>;

  template<class T, class... Args>
    unique_ptr<T> make_unique(Args&&... args);                                  // T is not array
  template<class T>
    unique_ptr<T> make_unique(size_t n);                                        // T is U[]
  template<class T, class... Args>
    unspecified make_unique(Args&&...) = delete;                                // T is U[N]

  template<class T>
    unique_ptr<T> make_unique_for_overwrite();                                  // T is not array
  template<class T>
    unique_ptr<T> make_unique_for_overwrite(size_t n);                          // T is U[]
  template<class T, class... Args>
    unspecified make_unique_for_overwrite(Args&&...) = delete;                  // T is U[N]

  template<class T, class D>
    void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;

  template<class T1, class D1, class T2, class D2>
    bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
  template<class T1, class D1, class T2, class D2>
    requires three_way_comparable_with<typename unique_ptr<T1, D1>::pointer,
                                       typename unique_ptr<T2, D2>::pointer>
    compare_three_way_result_t<typename unique_ptr<T1, D1>::pointer,
                               typename unique_ptr<T2, D2>::pointer>
      operator<=>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);

  template<class T, class D>
    bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
  template<class T, class D>
    bool operator<(const unique_ptr<T, D>& x, nullptr_t);
  template<class T, class D>
    bool operator<(nullptr_t, const unique_ptr<T, D>& y);
  template<class T, class D>
    bool operator>(const unique_ptr<T, D>& x, nullptr_t);
  template<class T, class D>
    bool operator>(nullptr_t, const unique_ptr<T, D>& y);
  template<class T, class D>
    bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
  template<class T, class D>
    bool operator<=(nullptr_t, const unique_ptr<T, D>& y);
  template<class T, class D>
    bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
  template<class T, class D>
    bool operator>=(nullptr_t, const unique_ptr<T, D>& y);
  template<class T, class D>
    requires three_way_comparable_with<typename unique_ptr<T, D>::pointer, nullptr_t>
    compare_three_way_result_t<typename unique_ptr<T, D>::pointer, nullptr_t>
      operator<=>(const unique_ptr<T, D>& x, nullptr_t);

  template<class E, class T, class Y, class D>
    basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const unique_ptr<Y, D>& p);

  // [util.smartptr.weak.bad], class bad_weak_ptr
  class bad_weak_ptr;

  // [util.smartptr.shared], class template shared_ptr
  template<class T> class shared_ptr;

  // [util.smartptr.shared.create], shared_ptr creation
  template<class T, class... Args>
    shared_ptr<T> make_shared(Args&&... args);                                  // T is not array
  template<class T, class A, class... Args>
    shared_ptr<T> allocate_shared(const A& a, Args&&... args);                  // T is not array

  template<class T>
    shared_ptr<T> make_shared(size_t N);                                        // T is U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a, size_t N);                        // T is U[]

  template<class T>
    shared_ptr<T> make_shared();                                                // T is U[N]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a);                                  // T is U[N]

  template<class T>
    shared_ptr<T> make_shared(size_t N, const remove_extent_t<T>& u);           // T is U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a, size_t N,
                                  const remove_extent_t<T>& u);                 // T is U[]

  template<class T>
    shared_ptr<T> make_shared(const remove_extent_t<T>& u);                     // T is U[N]
  template<class T, class A>
    shared_ptr<T> allocate_shared(const A& a, const remove_extent_t<T>& u);     // T is U[N]

  template<class T>
    shared_ptr<T> make_shared_for_overwrite();                                  // T is not U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared_for_overwrite(const A& a);                    // T is not U[]

  template<class T>
    shared_ptr<T> make_shared_for_overwrite(size_t N);                          // T is U[]
  template<class T, class A>
    shared_ptr<T> allocate_shared_for_overwrite(const A& a, size_t N);          // T is U[]

  // [util.smartptr.shared.cmp], shared_ptr comparisons
  template<class T, class U>
    bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
  template<class T, class U>
    strong_ordering operator<=>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;

  template<class T>
    bool operator==(const shared_ptr<T>& x, nullptr_t) noexcept;
  template<class T>
    strong_ordering operator<=>(const shared_ptr<T>& x, nullptr_t) noexcept;

  // [util.smartptr.shared.spec], shared_ptr specialized algorithms
  template<class T>
    void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;

  // [util.smartptr.shared.cast], shared_ptr casts
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> static_pointer_cast(shared_ptr<U>&& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> dynamic_pointer_cast(shared_ptr<U>&& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> const_pointer_cast(shared_ptr<U>&& r) noexcept;
  template<class T, class U>
    shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& r) noexcept;
  template<class T, class U>
    shared_ptr<T> reinterpret_pointer_cast(shared_ptr<U>&& r) noexcept;

  // [util.smartptr.getdeleter], shared_ptr get_deleter
  template<class D, class T>
    D* get_deleter(const shared_ptr<T>& p) noexcept;

  // [util.smartptr.shared.io], shared_ptr I/O
  template<class E, class T, class Y>
    basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const shared_ptr<Y>& p);

  // [util.smartptr.weak], class template weak_ptr
  template<class T> class weak_ptr;

  // [util.smartptr.weak.spec], weak_ptr specialized algorithms
  template<class T> void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;

  // [util.smartptr.ownerless], class template owner_less
  template<class T = void> struct owner_less;

  // [util.smartptr.enab], class template enable_shared_from_this
  template<class T> class enable_shared_from_this;

  // [util.smartptr.hash], hash support
  template<class T> struct hash;
  template<class T, class D> struct hash<unique_ptr<T, D>>;
  template<class T> struct hash<shared_ptr<T>>;

  // [util.smartptr.atomic], atomic smart pointers
  template<class T> struct atomic;
  template<class T> struct atomic<shared_ptr<T>>;
  template<class T> struct atomic<weak_ptr<T>>;
}
```

### Pointer traits <a id="pointer.traits">[[pointer.traits]]</a>

The class template `pointer_traits` supplies a uniform interface to
certain attributes of pointer-like types.

``` cpp
namespace std {
  template<class Ptr> struct pointer_traits {
    using pointer         = Ptr;
    using element_type    = see below;
    using difference_type = see below;

    template<class U> using rebind = see below;

    static pointer pointer_to(see below r);
  };

  template<class T> struct pointer_traits<T*> {
    using pointer         = T*;
    using element_type    = T;
    using difference_type = ptrdiff_t;

    template<class U> using rebind = U*;

    static constexpr pointer pointer_to(see below r) noexcept;
  };
}
```

#### Member types <a id="pointer.traits.types">[[pointer.traits.types]]</a>

``` cpp
using element_type = see below;
```

*Type:* `Ptr::element_type` if the *qualified-id* `Ptr::element_type` is
valid and denotes a type [[temp.deduct]]; otherwise, `T` if `Ptr` is a
class template instantiation of the form `SomePointer<T, Args>`, where
`Args` is zero or more type arguments; otherwise, the specialization is
ill-formed.

``` cpp
using difference_type = see below;
```

*Type:* `Ptr::difference_type` if the *qualified-id*
`Ptr::difference_type` is valid and denotes a type [[temp.deduct]];
otherwise, `ptrdiff_t`.

``` cpp
template<class U> using rebind = see below;
```

*Alias template:* `Ptr::rebind<U>` if the *qualified-id*
`Ptr::rebind<U>` is valid and denotes a type [[temp.deduct]]; otherwise,
`SomePointer<U, Args>` if `Ptr` is a class template instantiation of the
form `SomePointer<T, Args>`, where `Args` is zero or more type
arguments; otherwise, the instantiation of `rebind` is ill-formed.

#### Member functions <a id="pointer.traits.functions">[[pointer.traits.functions]]</a>

``` cpp
static pointer pointer_traits::pointer_to(see below r);
static constexpr pointer pointer_traits<T*>::pointer_to(see below r) noexcept;
```

*Mandates:* For the first member function, `Ptr::pointer_to(r)` is
well-formed.

*Preconditions:* For the first member function, `Ptr::pointer_to(r)`
returns a pointer to `r` through which indirection is valid.

*Returns:* The first member function returns `Ptr::pointer_to(r)`. The
second member function returns `addressof(r)`.

*Remarks:* If `element_type` is cv `void`, the type of `r` is
unspecified; otherwise, it is `element_type&`.

#### Optional members <a id="pointer.traits.optmem">[[pointer.traits.optmem]]</a>

Specializations of `pointer_traits` may define the member declared in
this subclause to customize the behavior of the standard library.

``` cpp
static element_type* to_address(pointer p) noexcept;
```

*Returns:* A pointer of type `element_type*` that references the same
location as the argument `p`.

[*Note 1*: This function should be the inverse of `pointer_to`. If
defined, it customizes the behavior of the non-member function
`to_address`[[pointer.conversion]]. — *end note*]

### Pointer conversion <a id="pointer.conversion">[[pointer.conversion]]</a>

``` cpp
template<class T> constexpr T* to_address(T* p) noexcept;
```

*Mandates:* `T` is not a function type.

*Returns:* `p`.

``` cpp
template<class Ptr> constexpr auto to_address(const Ptr& p) noexcept;
```

*Returns:* `pointer_traits<Ptr>::to_address(p)` if that expression is
well-formed (see [[pointer.traits.optmem]]), otherwise
`to_address(p.operator->())`.

### Pointer safety <a id="util.dynamic.safety">[[util.dynamic.safety]]</a>

A complete object is *declared reachable* while the number of calls to
`declare_reachable` with an argument referencing the object exceeds the
number of calls to `undeclare_reachable` with an argument referencing
the object.

``` cpp
void declare_reachable(void* p);
```

*Preconditions:* `p` is a safely-derived
pointer [[basic.stc.dynamic.safety]] or a null pointer value.

*Effects:* If `p` is not null, the complete object referenced by `p` is
subsequently declared reachable [[basic.stc.dynamic.safety]].

*Throws:* May throw `bad_alloc` if the system cannot allocate additional
memory that may be required to track objects declared reachable.

``` cpp
template<class T> T* undeclare_reachable(T* p);
```

*Preconditions:* If `p` is not null, the complete object referenced by
`p` has been previously declared reachable, and is live [[basic.life]]
from the time of the call until the last `undeclare_reachable(p)` call
on the object.

*Returns:* A safely derived copy of `p` which compares equal to `p`.

*Throws:* Nothing.

[*Note 1*: It is expected that calls to `declare_reachable(p)` will
consume a small amount of memory in addition to that occupied by the
referenced object until the matching call to `undeclare_reachable(p)` is
encountered. Long running programs should arrange that calls are
matched. — *end note*]

``` cpp
void declare_no_pointers(char* p, size_t n);
```

*Preconditions:* No bytes in the specified range are currently
registered with `declare_no_pointers()`. If the specified range is in an
allocated object, then it is entirely within a single allocated object.
The object is live until the corresponding `undeclare_no_pointers()`
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

*Preconditions:* The same range has previously been passed to
`declare_no_pointers()`.

*Effects:* Unregisters a range registered with `declare_no_pointers()`
for destruction. It shall be called before the lifetime of the object
ends.

*Throws:* Nothing.

``` cpp
pointer_safety get_pointer_safety() noexcept;
```

*Returns:* `pointer_safety::strict` if the implementation has strict
pointer safety [[basic.stc.dynamic.safety]]. It is
*implementation-defined* whether `get_pointer_safety` returns
`pointer_safety::relaxed` or `pointer_safety::preferred` if the
implementation has relaxed pointer safety.[^1]

### Pointer alignment <a id="ptr.align">[[ptr.align]]</a>

``` cpp
void* align(size_t alignment, size_t size, void*& ptr, size_t& space);
```

*Preconditions:*

- `alignment` is a power of two
- `ptr` represents the address of contiguous storage of at least `space`
  bytes

*Effects:* If it is possible to fit `size` bytes of storage aligned by
`alignment` into the buffer pointed to by `ptr` with length `space`, the
function updates `ptr` to represent the first possible address of such
storage and decreases `space` by the number of bytes used for alignment.
Otherwise, the function does nothing.

*Returns:* A null pointer if the requested aligned buffer would not fit
into the available space, otherwise the adjusted value of `ptr`.

[*Note 1*: The function updates its `ptr` and `space` arguments so that
it can be called repeatedly with possibly different `alignment` and
`size` arguments for the same buffer. — *end note*]

``` cpp
template<size_t N, class T>
  [[nodiscard]] constexpr T* assume_aligned(T* ptr);
```

*Mandates:* `N` is a power of two.

*Preconditions:* `ptr` points to an object `X` of a type
similar [[conv.qual]] to `T`, where `X` has alignment
`N`[[basic.align]].

*Returns:* `ptr`.

*Throws:* Nothing.

[*Note 2*: The alignment assumption on an object `X` expressed by a
call to `assume_aligned` may result in generation of more efficient
code. It is up to the program to ensure that the assumption actually
holds. The call does not cause the compiler to verify or enforce this.
An implementation might only make the assumption for those operations on
`X` that access `X` through the pointer returned by
`assume_aligned`. — *end note*]

### Allocator argument tag <a id="allocator.tag">[[allocator.tag]]</a>

``` cpp
namespace std {
  struct allocator_arg_t { explicit allocator_arg_t() = default; };
  inline constexpr allocator_arg_t allocator_arg{};
}
```

The `allocator_arg_t` struct is an empty class type used as a unique
type to disambiguate constructor and function overloading. Specifically,
several types (see `tuple`  [[tuple]]) have constructors with
`allocator_arg_t` as the first argument, immediately followed by an
argument of a type that meets the *Cpp17Allocator* requirements (
[[cpp17.allocator]]).

### `uses_allocator` <a id="allocator.uses">[[allocator.uses]]</a>

#### `uses_allocator` trait <a id="allocator.uses.trait">[[allocator.uses.trait]]</a>

``` cpp
template<class T, class Alloc> struct uses_allocator;
```

*Remarks:* Automatically detects whether `T` has a nested
`allocator_type` that is convertible from `Alloc`. Meets the
*Cpp17BinaryTypeTrait* requirements [[meta.rqmts]]. The implementation
shall provide a definition that is derived from `true_type` if the
*qualified-id* `T::allocator_type` is valid and denotes a
type [[temp.deduct]] and
`is_convertible_v<Alloc, T::allocator_type> != false`, otherwise it
shall be derived from `false_type`. A program may specialize this
template to derive from `true_type` for a program-defined type `T` that
does not have a nested `allocator_type` but nonetheless can be
constructed with an allocator where either:

- the first argument of a constructor has type `allocator_arg_t` and the
  second argument has type `Alloc` or
- the last argument of a constructor has type `Alloc`.

#### Uses-allocator construction <a id="allocator.uses.construction">[[allocator.uses.construction]]</a>

*Uses-allocator construction* with allocator `alloc` and constructor
arguments `args...` refers to the construction of an object of type `T`
such that `alloc` is passed to the constructor of `T` if `T` uses an
allocator type compatible with `alloc`. When applied to the construction
of an object of type `T`, it is equivalent to initializing it with the
value of the expression `make_obj_using_allocator<T>(alloc, args...)`,
described below.

The following utility functions support three conventions for passing
`alloc` to a constructor:

- If `T` does not use an allocator compatible with `alloc`, then `alloc`
  is ignored.
- Otherwise, if `T` has a constructor invocable as
  `T(allocator_arg, alloc, args...)` (leading-allocator convention),
  then uses-allocator construction chooses this constructor form.
- Otherwise, if `T` has a constructor invocable as `T(args..., alloc)`
  (trailing-allocator convention), then uses-allocator construction
  chooses this constructor form.

The `uses_allocator_construction_args` function template takes an
allocator and argument list and produces (as a tuple) a new argument
list matching one of the above conventions. Additionally, overloads are
provided that treat specializations of `pair` such that uses-allocator
construction is applied individually to the `first` and `second` data
members. The `make_obj_using_allocator` and
`uninitialized_construct_using_allocator` function templates apply the
modified constructor arguments to construct an object of type `T` as a
return value or in-place, respectively.

[*Note 1*: For `uses_allocator_construction_args` and
`make_obj_using_allocator`, type `T` is not deduced and must therefore
be specified explicitly by the caller. — *end note*]

``` cpp
template<class T, class Alloc, class... Args>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  Args&&... args) noexcept -> see below;
```

*Constraints:* `T` is not a specialization of `pair`.

*Returns:* A `tuple` value determined as follows:

- If `uses_allocator_v<T, Alloc>` is `false` and
  `is_constructible_v<T, Args...>` is `true`, return
  `forward_as_tuple(std::forward<Args>(args)...)`.
- Otherwise, if `uses_allocator_v<T, Alloc>` is `true` and
  `is_constructible_v<T, allocator_arg_t, const Alloc&, Args...>` is
  `true`, return
  ``` cpp
  tuple<allocator_arg_t, const Alloc&, Args&&...>(
    allocator_arg, alloc, std::forward<Args>(args)...)
  ```
- Otherwise, if `uses_allocator_v<T, Alloc>` is `true` and
  `is_constructible_v<T, Args..., const Alloc&>` is `true`, return
  `forward_as_tuple(std::forward<Args>(args)..., alloc)`.
- Otherwise, the program is ill-formed.

[*Note 1*: This definition prevents a silent failure to pass the
allocator to a constructor of a type for which
`uses_allocator_v<T, Alloc>` is `true`. — *end note*]

``` cpp
template<class T, class Alloc, class Tuple1, class Tuple2>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc, piecewise_construct_t,
                                                  Tuple1&& x, Tuple2&& y)
                                                  noexcept -> see below;
```

*Constraints:* `T` is a specialization of `pair`.

*Effects:* For `T` specified as `pair<T1, T2>`, equivalent to:

``` cpp
return make_tuple(
  piecewise_construct,
  apply([&alloc](auto&&... args1) {
          return uses_allocator_construction_args<T1>(
            alloc, std::forward<decltype(args1)>(args1)...);
        }, std::forward<Tuple1>(x)),
  apply([&alloc](auto&&... args2) {
          return uses_allocator_construction_args<T2>(
            alloc, std::forward<decltype(args2)>(args2)...);
        }, std::forward<Tuple2>(y)));
```

``` cpp
template<class T, class Alloc>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc) noexcept -> see below;
```

*Constraints:* `T` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           tuple<>{}, tuple<>{});
```

``` cpp
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  U&& u, V&& v) noexcept -> see below;
```

*Constraints:* `T` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(std::forward<U>(u)),
                                           forward_as_tuple(std::forward<V>(v)));
```

``` cpp
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  const pair<U,V>& pr) noexcept -> see below;
```

*Constraints:* `T` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(pr.first),
                                           forward_as_tuple(pr.second));
```

``` cpp
template<class T, class Alloc, class U, class V>
  constexpr auto uses_allocator_construction_args(const Alloc& alloc,
                                                  pair<U,V>&& pr) noexcept -> see below;
```

*Constraints:* `T` is a specialization of `pair`.

*Effects:* Equivalent to:

``` cpp
return uses_allocator_construction_args<T>(alloc, piecewise_construct,
                                           forward_as_tuple(std::move(pr).first),
                                           forward_as_tuple(std::move(pr).second));
```

``` cpp
template<class T, class Alloc, class... Args>
  constexpr T make_obj_using_allocator(const Alloc& alloc, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return make_from_tuple<T>(uses_allocator_construction_args<T>(
                            alloc, std::forward<Args>(args)...));
```

``` cpp
template<class T, class Alloc, class... Args>
  constexpr T* uninitialized_construct_using_allocator(T* p, const Alloc& alloc, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
return apply([&]<class... U>(U&&... xs) {
       return construct_at(p, std::forward<U>(xs)...);
     }, uses_allocator_construction_args<T>(alloc, std::forward<Args>(args)...));
```

### Allocator traits <a id="allocator.traits">[[allocator.traits]]</a>

The class template `allocator_traits` supplies a uniform interface to
all allocator types. An allocator cannot be a non-class type, however,
even if `allocator_traits` supplies the entire required interface.

[*Note 1*: Thus, it is always possible to create a derived class from
an allocator. — *end note*]

``` cpp
namespace std {
  template<class Alloc> struct allocator_traits {
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

    template<class T> using rebind_alloc = see below;
    template<class T> using rebind_traits = allocator_traits<rebind_alloc<T>>;

    [[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n);
    [[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n,
                                                    const_void_pointer hint);

    static constexpr void deallocate(Alloc& a, pointer p, size_type n);

    template<class T, class... Args>
      static constexpr void construct(Alloc& a, T* p, Args&&... args);

    template<class T>
      static constexpr void destroy(Alloc& a, T* p);

    static constexpr size_type max_size(const Alloc& a) noexcept;

    static constexpr Alloc select_on_container_copy_construction(const Alloc& rhs);
  };
}
```

#### Member types <a id="allocator.traits.types">[[allocator.traits.types]]</a>

``` cpp
using pointer = see below;
```

*Type:* `Alloc::pointer` if the *qualified-id* `Alloc::pointer` is valid
and denotes a type [[temp.deduct]]; otherwise, `value_type*`.

``` cpp
using const_pointer = see below;
```

*Type:* `Alloc::const_pointer` if the *qualified-id*
`Alloc::const_pointer` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::rebind<const value_type>`.

``` cpp
using void_pointer = see below;
```

*Type:* `Alloc::void_pointer` if the *qualified-id*
`Alloc::void_pointer` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::rebind<void>`.

``` cpp
using const_void_pointer = see below;
```

*Type:* `Alloc::const_void_pointer` if the *qualified-id*
`Alloc::const_void_pointer` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::rebind<const void>`.

``` cpp
using difference_type = see below;
```

*Type:* `Alloc::difference_type` if the *qualified-id*
`Alloc::difference_type` is valid and denotes a type [[temp.deduct]];
otherwise, `pointer_traits<pointer>::difference_type`.

``` cpp
using size_type = see below;
```

*Type:* `Alloc::size_type` if the *qualified-id* `Alloc::size_type` is
valid and denotes a type [[temp.deduct]]; otherwise,
`make_unsigned_t<difference_type>`.

``` cpp
using propagate_on_container_copy_assignment = see below;
```

*Type:* `Alloc::propagate_on_container_copy_assignment` if the
*qualified-id* `Alloc::propagate_on_container_copy_assignment` is valid
and denotes a type [[temp.deduct]]; otherwise `false_type`.

``` cpp
using propagate_on_container_move_assignment = see below;
```

*Type:* `Alloc::propagate_on_container_move_assignment` if the
*qualified-id* `Alloc::propagate_on_container_move_assignment` is valid
and denotes a type [[temp.deduct]]; otherwise `false_type`.

``` cpp
using propagate_on_container_swap = see below;
```

*Type:* `Alloc::propagate_on_container_swap` if the *qualified-id*
`Alloc::propagate_on_container_swap` is valid and denotes a
type [[temp.deduct]]; otherwise `false_type`.

``` cpp
using is_always_equal = see below;
```

*Type:* `Alloc::is_always_equal` if the *qualified-id*
`Alloc::is_always_equal` is valid and denotes a type [[temp.deduct]];
otherwise `is_empty<Alloc>::type`.

``` cpp
template<class T> using rebind_alloc = see below;
```

*Alias template:* `Alloc::rebind<T>::other` if the *qualified-id*
`Alloc::rebind<T>::other` is valid and denotes a type [[temp.deduct]];
otherwise, `Alloc<T, Args>` if `Alloc` is a class template instantiation
of the form `Alloc<U, Args>`, where `Args` is zero or more type
arguments; otherwise, the instantiation of `rebind_alloc` is ill-formed.

#### Static member functions <a id="allocator.traits.members">[[allocator.traits.members]]</a>

``` cpp
[[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n);
```

*Returns:* `a.allocate(n)`.

``` cpp
[[nodiscard]] static constexpr pointer allocate(Alloc& a, size_type n, const_void_pointer hint);
```

*Returns:* `a.allocate(n, hint)` if that expression is well-formed;
otherwise, `a.allocate(n)`.

``` cpp
static constexpr void deallocate(Alloc& a, pointer p, size_type n);
```

*Effects:* Calls `a.deallocate(p, n)`.

*Throws:* Nothing.

``` cpp
template<class T, class... Args>
  static constexpr void construct(Alloc& a, T* p, Args&&... args);
```

*Effects:* Calls `a.construct(p, std::forward<Args>(args)...)` if that
call is well-formed; otherwise, invokes
`construct_at(p, std::forward<Args>(args)...)`.

``` cpp
template<class T>
  static constexpr void destroy(Alloc& a, T* p);
```

*Effects:* Calls `a.destroy(p)` if that call is well-formed; otherwise,
invokes `destroy_at(p)`.

``` cpp
static constexpr size_type max_size(const Alloc& a) noexcept;
```

*Returns:* `a.max_size()` if that expression is well-formed; otherwise,
`numeric_limits<size_type>::max()/sizeof(value_type)`.

``` cpp
static constexpr Alloc select_on_container_copy_construction(const Alloc& rhs);
```

*Returns:* `rhs.select_on_container_copy_construction()` if that
expression is well-formed; otherwise, `rhs`.

### The default allocator <a id="default.allocator">[[default.allocator]]</a>

All specializations of the default allocator meet the allocator
completeness requirements [[allocator.requirements.completeness]].

``` cpp
namespace std {
  template<class T> class allocator {
   public:
    using value_type                             = T;
    using size_type                              = size_t;
    using difference_type                        = ptrdiff_t;
    using propagate_on_container_move_assignment = true_type;
    using is_always_equal                        = true_type;

    constexpr allocator() noexcept;
    constexpr allocator(const allocator&) noexcept;
    template<class U> constexpr allocator(const allocator<U>&) noexcept;
    constexpr ~allocator();
    constexpr allocator& operator=(const allocator&) = default;

    [[nodiscard]] constexpr T* allocate(size_t n);
    constexpr void deallocate(T* p, size_t n);
  };
}
```

#### Members <a id="allocator.members">[[allocator.members]]</a>

Except for the destructor, member functions of the default allocator
shall not introduce data races [[intro.multithread]] as a result of
concurrent calls to those member functions from different threads. Calls
to these functions that allocate or deallocate a particular unit of
storage shall occur in a single total order, and each such deallocation
call shall happen before the next allocation (if any) in this order.

``` cpp
[[nodiscard]] constexpr T* allocate(size_t n);
```

*Mandates:* `T` is not an incomplete type [[basic.types]].

*Returns:* A pointer to the initial element of an array of `n` `T`.

*Remarks:* The storage for the array is obtained by calling
`::operator new`[[new.delete]], but it is unspecified when or how often
this function is called. This function starts the lifetime of the array
object, but not that of any of the array elements.

*Throws:* `bad_array_new_length` if
`numeric_limits<size_t>::max() / sizeof(T) < n`, or `bad_alloc` if the
storage cannot be obtained.

``` cpp
constexpr void deallocate(T* p, size_t n);
```

*Preconditions:* `p` is a pointer value obtained from `allocate()`. `n`
equals the value passed as the first argument to the invocation of
allocate which returned `p`.

*Effects:* Deallocates the storage referenced by `p` .

*Remarks:* Uses `::operator delete`[[new.delete]], but it is unspecified
when this function is called.

#### Operators <a id="allocator.globals">[[allocator.globals]]</a>

``` cpp
template<class T, class U>
  constexpr bool operator==(const allocator<T>&, const allocator<U>&) noexcept;
```

*Returns:* `true`.

### `addressof` <a id="specialized.addressof">[[specialized.addressof]]</a>

``` cpp
template<class T> constexpr T* addressof(T& r) noexcept;
```

*Returns:* The actual address of the object or function referenced by
`r`, even in the presence of an overloaded `operator&`.

*Remarks:* An expression `addressof(E)` is a constant
subexpression [[defns.const.subexpr]] if `E` is an lvalue constant
subexpression.

### C library memory allocation <a id="c.malloc">[[c.malloc]]</a>

[*Note 1*: The header `<cstdlib>` declares the functions described in
this subclause. — *end note*]

``` cpp
void* aligned_alloc(size_t alignment, size_t size);
void* calloc(size_t nmemb, size_t size);
void* malloc(size_t size);
void* realloc(void* ptr, size_t size);
```

*Effects:* These functions have the semantics specified in the C
standard library.

*Remarks:* These functions do not attempt to allocate storage by calling
`::operator new()`[[new.delete]].

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

These functions implicitly create objects [[intro.object]] in the
returned region of storage and return a pointer to a suitable created
object. In the case of `calloc` and `realloc`, the objects are created
before the storage is zeroed or copied, respectively.

``` cpp
void free(void* ptr);
```

*Effects:* This function has the semantics specified in the C standard
library.

*Remarks:* This function does not attempt to deallocate storage by
calling `::operator delete()`.

See also: ISO C 7.22.3

## Smart pointers <a id="smartptr">[[smartptr]]</a>

### Class template `unique_ptr` <a id="unique.ptr">[[unique.ptr]]</a>

A *unique pointer* is an object that owns another object and manages
that other object through a pointer. More precisely, a unique pointer is
an object *u* that stores a pointer to a second object *p* and will
dispose of *p* when *u* is itself destroyed (e.g., when leaving block
scope [[stmt.dcl]]). In this context, *u* is said to *own* `p`.

The mechanism by which *u* disposes of *p* is known as *p*’s associated
*deleter*, a function object whose correct invocation results in *p*’s
appropriate disposition (typically its deletion).

Let the notation *u.p* denote the pointer stored by *u*, and let *u.d*
denote the associated deleter. Upon request, *u* can *reset* (replace)
*u.p* and *u.d* with another pointer and deleter, but properly disposes
of its owned object via the associated deleter before such replacement
is considered completed.

Each object of a type `U` instantiated from the `unique_ptr` template
specified in this subclause has the strict ownership semantics,
specified above, of a unique pointer. In partial satisfaction of these
semantics, each such `U` is *Cpp17MoveConstructible* and
*Cpp17MoveAssignable*, but is not *Cpp17CopyConstructible* nor
*Cpp17CopyAssignable*. The template parameter `T` of `unique_ptr` may be
an incomplete type.

[*Note 1*: The uses of `unique_ptr` include providing exception safety
for dynamically allocated memory, passing ownership of dynamically
allocated memory to a function, and returning dynamically allocated
memory from a function. — *end note*]

#### Default deleters <a id="unique.ptr.dltr">[[unique.ptr.dltr]]</a>

##### In general <a id="unique.ptr.dltr.general">[[unique.ptr.dltr.general]]</a>

The class template `default_delete` serves as the default deleter
(destruction policy) for the class template `unique_ptr`.

The template parameter `T` of `default_delete` may be an incomplete
type.

##### `default_delete` <a id="unique.ptr.dltr.dflt">[[unique.ptr.dltr.dflt]]</a>

``` cpp
namespace std {
  template<class T> struct default_delete {
    constexpr default_delete() noexcept = default;
    template<class U> default_delete(const default_delete<U>&) noexcept;
    void operator()(T*) const;
  };
}
```

``` cpp
template<class U> default_delete(const default_delete<U>& other) noexcept;
```

*Constraints:* `U*` is implicitly convertible to `T*`.

*Effects:* Constructs a `default_delete` object from another
`default_delete<U>` object.

``` cpp
void operator()(T* ptr) const;
```

*Mandates:* `T` is a complete type.

*Effects:* Calls `delete` on `ptr`.

##### `default_delete<T[]>` <a id="unique.ptr.dltr.dflt1">[[unique.ptr.dltr.dflt1]]</a>

``` cpp
namespace std {
  template<class T> struct default_delete<T[]> {
    constexpr default_delete() noexcept = default;
    template<class U> default_delete(const default_delete<U[]>&) noexcept;
    template<class U> void operator()(U* ptr) const;
  };
}
```

``` cpp
template<class U> default_delete(const default_delete<U[]>& other) noexcept;
```

*Constraints:* `U(*)[]` is convertible to `T(*)[]`.

*Effects:* Constructs a `default_delete` object from another
`default_delete<U[]>` object.

``` cpp
template<class U> void operator()(U* ptr) const;
```

*Mandates:* `U` is a complete type.

*Constraints:* `U(*)[]` is convertible to `T(*)[]`.

*Effects:* Calls `delete[]` on `ptr`.

#### `unique_ptr` for single objects <a id="unique.ptr.single">[[unique.ptr.single]]</a>

``` cpp
namespace std {
  template<class T, class D = default_delete<T>> class unique_ptr {
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
    template<class U, class E>
      unique_ptr(unique_ptr<U, E>&& u) noexcept;

    // [unique.ptr.single.dtor], destructor
    ~unique_ptr();

    // [unique.ptr.single.asgn], assignment
    unique_ptr& operator=(unique_ptr&& u) noexcept;
    template<class U, class E>
      unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
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
client-supplied template argument `D` shall be a function object type
[[function.objects]], lvalue reference to function, or lvalue reference
to function object type for which, given a value `d` of type `D` and a
value `ptr` of type `unique_ptr<T, D>::pointer`, the expression `d(ptr)`
is valid and has the effect of disposing of the pointer as appropriate
for that deleter.

If the deleter’s type `D` is not a reference type, `D` shall meet the
*Cpp17Destructible* requirements ([[cpp17.destructible]]).

If the *qualified-id* `remove_reference_t<D>::pointer` is valid and
denotes a type [[temp.deduct]], then `unique_ptr<T,
D>::pointer` shall be a synonym for `remove_reference_t<D>::pointer`.
Otherwise `unique_ptr<T, D>::pointer` shall be a synonym for
`element_type*`. The type `unique_ptr<T,
D>::pointer` shall meet the *Cpp17NullablePointer* requirements (
[[cpp17.nullablepointer]]).

[*Example 1*: Given an allocator type `X` ([[cpp17.allocator]]) and
letting `A` be a synonym for `allocator_traits<X>`, the types
`A::pointer`, `A::const_pointer`, `A::void_pointer`, and
`A::const_void_pointer` may be used as
`unique_ptr<T, D>::pointer`. — *end example*]

##### Constructors <a id="unique.ptr.single.ctor">[[unique.ptr.single.ctor]]</a>

``` cpp
constexpr unique_ptr() noexcept;
constexpr unique_ptr(nullptr_t) noexcept;
```

*Preconditions:* `D` meets the *Cpp17DefaultConstructible* requirements
([[cpp17.defaultconstructible]]), and that construction does not throw
an exception.

*Constraints:* `is_pointer_v<deleter_type>` is `false` and
`is_default_constructible_v<deleter_type>` is `true`.

*Effects:* Constructs a `unique_ptr` object that owns nothing,
value-initializing the stored pointer and the stored deleter.

*Ensures:* `get() == nullptr`. `get_deleter()` returns a reference to
the stored deleter.

``` cpp
explicit unique_ptr(pointer p) noexcept;
```

*Constraints:* `is_pointer_v<deleter_type>` is `false` and
`is_default_constructible_v<deleter_type>` is `true`.

*Mandates:* This constructor is not selected by class template argument
deduction [[over.match.class.deduct]].

*Preconditions:* `D` meets the *Cpp17DefaultConstructible* requirements
([[cpp17.defaultconstructible]]), and that construction does not throw
an exception.

*Effects:* Constructs a `unique_ptr` which owns `p`, initializing the
stored pointer with `p` and value-initializing the stored deleter.

*Ensures:* `get() == p`. `get_deleter()` returns a reference to the
stored deleter.

``` cpp
unique_ptr(pointer p, const D& d) noexcept;
unique_ptr(pointer p, remove_reference_t<D>&& d) noexcept;
```

*Constraints:* `is_constructible_v<D, decltype(d)>` is `true`.

*Mandates:* These constructors are not selected by class template
argument deduction [[over.match.class.deduct]].

*Preconditions:* For the first constructor, if `D` is not a reference
type, `D` meets the *Cpp17CopyConstructible* requirements and such
construction does not exit via an exception. For the second constructor,
if `D` is not a reference type, `D` meets the *Cpp17MoveConstructible*
requirements and such construction does not exit via an exception.

*Effects:* Constructs a `unique_ptr` object which owns `p`, initializing
the stored pointer with `p` and initializing the deleter from
`std::forward<decltype(d)>(d)`.

*Ensures:* `get() == p`. `get_deleter()` returns a reference to the
stored deleter. If `D` is a reference type then `get_deleter()` returns
a reference to the lvalue `d`.

*Remarks:* If `D` is a reference type, the second constructor is defined
as deleted.

[*Example 1*:

``` cpp
D d;
unique_ptr<int, D> p1(new int, D());        // D must be Cpp17MoveConstructible
unique_ptr<int, D> p2(new int, d);          // D must be Cpp17CopyConstructible
unique_ptr<int, D&> p3(new int, d);         // p3 holds a reference to d
unique_ptr<int, const D&> p4(new int, D()); // error: rvalue deleter object combined
                                            // with reference deleter type
```

— *end example*]

``` cpp
unique_ptr(unique_ptr&& u) noexcept;
```

*Constraints:* `is_move_constructible_v<D>` is `true`.

*Preconditions:* If `D` is not a reference type, `D` meets the
*Cpp17MoveConstructible* requirements ([[cpp17.moveconstructible]]).
Construction of the deleter from an rvalue of type `D` does not throw an
exception.

*Effects:* Constructs a `unique_ptr` from `u`. If `D` is a reference
type, this deleter is copy constructed from `u`’s deleter; otherwise,
this deleter is move constructed from `u`’s deleter.

[*Note 1*: The construction of the deleter can be implemented with
`std::forward<D>`. — *end note*]

*Ensures:* `get()` yields the value `u.get()` yielded before the
construction. `u.get() == nullptr`. `get_deleter()` returns a reference
to the stored deleter that was constructed from `u.get_deleter()`. If
`D` is a reference type then `get_deleter()` and `u.get_deleter()` both
reference the same lvalue deleter.

``` cpp
template<class U, class E> unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

*Constraints:*

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
- `U` is not an array type, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

*Preconditions:* If `E` is not a reference type, construction of the
deleter from an rvalue of type `E` is well-formed and does not throw an
exception. Otherwise, `E` is a reference type and construction of the
deleter from an lvalue of type `E` is well-formed and does not throw an
exception.

*Effects:* Constructs a `unique_ptr` from `u`. If `E` is a reference
type, this deleter is copy constructed from `u`’s deleter; otherwise,
this deleter is move constructed from `u`’s deleter.

[*Note 2*: The deleter constructor can be implemented with
`std::forward<E>`. — *end note*]

*Ensures:* `get()` yields the value `u.get()` yielded before the
construction. `u.get() == nullptr`. `get_deleter()` returns a reference
to the stored deleter that was constructed from `u.get_deleter()`.

##### Destructor <a id="unique.ptr.single.dtor">[[unique.ptr.single.dtor]]</a>

``` cpp
~unique_ptr();
```

*Preconditions:* The expression `get_deleter()(get())` is well-formed,
has well-defined behavior, and does not throw exceptions.

[*Note 3*: The use of `default_delete` requires `T` to be a complete
type. — *end note*]

*Effects:* If `get() == nullptr` there are no effects. Otherwise
`get_deleter()(get())`.

##### Assignment <a id="unique.ptr.single.asgn">[[unique.ptr.single.asgn]]</a>

``` cpp
unique_ptr& operator=(unique_ptr&& u) noexcept;
```

*Constraints:* `is_move_assignable_v<D>` is `true`.

*Preconditions:* If `D` is not a reference type, `D` meets the
*Cpp17MoveAssignable* requirements ([[cpp17.moveassignable]]) and
assignment of the deleter from an rvalue of type `D` does not throw an
exception. Otherwise, `D` is a reference type; `remove_reference_t<D>`
meets the *Cpp17CopyAssignable* requirements and assignment of the
deleter from an lvalue of type `D` does not throw an exception.

*Effects:* Calls `reset(u.release())` followed by
`get_deleter() = std::forward<D>(u.get_deleter())`.

*Returns:* `*this`.

*Ensures:* `u.get() == nullptr`.

``` cpp
template<class U, class E> unique_ptr& operator=(unique_ptr<U, E>&& u) noexcept;
```

*Constraints:*

- `unique_ptr<U, E>::pointer` is implicitly convertible to `pointer`,
  and
- `U` is not an array type, and
- `is_assignable_v<D&, E&&>` is `true`.

*Preconditions:* If `E` is not a reference type, assignment of the
deleter from an rvalue of type `E` is well-formed and does not throw an
exception. Otherwise, `E` is a reference type and assignment of the
deleter from an lvalue of type `E` is well-formed and does not throw an
exception.

*Effects:* Calls `reset(u.release())` followed by
`get_deleter() = std::forward<E>(u.get_deleter())`.

*Returns:* `*this`.

*Ensures:* `u.get() == nullptr`.

``` cpp
unique_ptr& operator=(nullptr_t) noexcept;
```

*Effects:* As if by `reset()`.

*Ensures:* `get() == nullptr`.

*Returns:* `*this`.

##### Observers <a id="unique.ptr.single.observers">[[unique.ptr.single.observers]]</a>

``` cpp
add_lvalue_reference_t<T> operator*() const;
```

*Preconditions:* `get() != nullptr`.

*Returns:* `*get()`.

``` cpp
pointer operator->() const noexcept;
```

*Preconditions:* `get() != nullptr`.

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

##### Modifiers <a id="unique.ptr.single.modifiers">[[unique.ptr.single.modifiers]]</a>

``` cpp
pointer release() noexcept;
```

*Ensures:* `get() == nullptr`.

*Returns:* The value `get()` had at the start of the call to `release`.

``` cpp
void reset(pointer p = pointer()) noexcept;
```

*Preconditions:* The expression `get_deleter()(get())` is well-formed,
has well-defined behavior, and does not throw exceptions.

*Effects:* Assigns `p` to the stored pointer, and then if and only if
the old value of the stored pointer, `old_p`, was not equal to
`nullptr`, calls `get_deleter()(old_p)`.

[*Note 5*: The order of these operations is significant because the
call to `get_deleter()` may destroy `*this`. — *end note*]

*Ensures:* `get() == p`.

[*Note 6*: The postcondition does not hold if the call to
`get_deleter()` destroys `*this` since `this->get()` is no longer a
valid expression. — *end note*]

``` cpp
void swap(unique_ptr& u) noexcept;
```

*Preconditions:* `get_deleter()` is swappable [[swappable.requirements]]
and does not throw an exception under `swap`.

*Effects:* Invokes `swap` on the stored pointers and on the stored
deleters of `*this` and `u`.

#### `unique_ptr` for array objects with a runtime length <a id="unique.ptr.runtime">[[unique.ptr.runtime]]</a>

``` cpp
namespace std {
  template<class T, class D> class unique_ptr<T[], D> {
  public:
    using pointer      = see below;
    using element_type = T;
    using deleter_type = D;

    // [unique.ptr.runtime.ctor], constructors
    constexpr unique_ptr() noexcept;
    template<class U> explicit unique_ptr(U p) noexcept;
    template<class U> unique_ptr(U p, see below d) noexcept;
    template<class U> unique_ptr(U p, see below d) noexcept;
    unique_ptr(unique_ptr&& u) noexcept;
    template<class U, class E>
      unique_ptr(unique_ptr<U, E>&& u) noexcept;
    constexpr unique_ptr(nullptr_t) noexcept;

    // destructor
    ~unique_ptr();

    // assignment
    unique_ptr& operator=(unique_ptr&& u) noexcept;
    template<class U, class E>
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
    template<class U> void reset(U p) noexcept;
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

##### Constructors <a id="unique.ptr.runtime.ctor">[[unique.ptr.runtime.ctor]]</a>

``` cpp
template<class U> explicit unique_ptr(U p) noexcept;
```

This constructor behaves the same as the constructor in the primary
template that takes a single parameter of type `pointer`.

*Constraints:*

- `U` is the same type as `pointer`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

``` cpp
template<class U> unique_ptr(U p, see below d) noexcept;
template<class U> unique_ptr(U p, see below d) noexcept;
```

These constructors behave the same as the constructors in the primary
template that take a parameter of type `pointer` and a second parameter.

*Constraints:*

- `U` is the same type as `pointer`,
- `U` is `nullptr_t`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

``` cpp
template<class U, class E> unique_ptr(unique_ptr<U, E>&& u) noexcept;
```

This constructor behaves the same as in the primary template.

*Constraints:* Where `UP` is `unique_ptr<U, E>`:

- `U` is an array type, and
- `pointer` is the same type as `element_type*`, and
- `UP::pointer` is the same type as `UP::element_type*`, and
- `UP::element_type(*)[]` is convertible to `element_type(*)[]`, and
- either `D` is a reference type and `E` is the same type as `D`, or `D`
  is not a reference type and `E` is implicitly convertible to `D`.

[*Note 1*: This replaces the *Constraints:* specification of the
primary template. — *end note*]

##### Assignment <a id="unique.ptr.runtime.asgn">[[unique.ptr.runtime.asgn]]</a>

``` cpp
template<class U, class E> unique_ptr& operator=(unique_ptr<U, E>&& u)noexcept;
```

This operator behaves the same as in the primary template.

*Constraints:* Where `UP` is `unique_ptr<U, E>`:

- `U` is an array type, and
- `pointer` is the same type as `element_type*`, and
- `UP::pointer` is the same type as `UP::element_type*`, and
- `UP::element_type(*)[]` is convertible to `element_type(*)[]`, and
- `is_assignable_v<D&, E&&>` is `true`.

[*Note 2*: This replaces the *Constraints:* specification of the
primary template. — *end note*]

##### Observers <a id="unique.ptr.runtime.observers">[[unique.ptr.runtime.observers]]</a>

``` cpp
T& operator[](size_t i) const;
```

*Preconditions:* `i` < the number of elements in the array to which the
stored pointer points.

*Returns:* `get()[i]`.

##### Modifiers <a id="unique.ptr.runtime.modifiers">[[unique.ptr.runtime.modifiers]]</a>

``` cpp
void reset(nullptr_t p = nullptr) noexcept;
```

*Effects:* Equivalent to `reset(pointer())`.

``` cpp
template<class U> void reset(U p) noexcept;
```

This function behaves the same as the `reset` member of the primary
template.

*Constraints:*

- `U` is the same type as `pointer`, or
- `pointer` is the same type as `element_type*`, `U` is a pointer type
  `V*`, and `V(*)[]` is convertible to `element_type(*)[]`.

#### Creation <a id="unique.ptr.create">[[unique.ptr.create]]</a>

``` cpp
template<class T, class... Args> unique_ptr<T> make_unique(Args&&... args);
```

*Constraints:* `T` is not an array type.

*Returns:* `unique_ptr<T>(new T(std::forward<Args>(args)...))`.

``` cpp
template<class T> unique_ptr<T> make_unique(size_t n);
```

*Constraints:* `T` is an array of unknown bound.

*Returns:* `unique_ptr<T>(new remove_extent_t<T>[n]())`.

``` cpp
template<class T, class... Args> unspecified make_unique(Args&&...) = delete;
```

*Constraints:* `T` is an array of known bound.

``` cpp
template<class T> unique_ptr<T> make_unique_for_overwrite();
```

*Constraints:* `T` is not an array type.

*Returns:* `unique_ptr<T>(new T)`.

``` cpp
template<class T> unique_ptr<T> make_unique_for_overwrite(size_t n);
```

*Constraints:* `T` is an array of unknown bound.

*Returns:* `unique_ptr<T>(new remove_extent_t<T>[n])`.

``` cpp
template<class T, class... Args> unspecified make_unique_for_overwrite(Args&&...) = delete;
```

*Constraints:* `T` is an array of known bound.

#### Specialized algorithms <a id="unique.ptr.special">[[unique.ptr.special]]</a>

``` cpp
template<class T, class D> void swap(unique_ptr<T, D>& x, unique_ptr<T, D>& y) noexcept;
```

*Constraints:* `is_swappable_v<D>` is `true`.

*Effects:* Calls `x.swap(y)`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator==(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `x.get() == y.get()`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator<(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

Let `CT` denote

``` cpp
common_type_t<typename unique_ptr<T1, D1>::pointer,
              typename unique_ptr<T2, D2>::pointer>
```

*Mandates:*

- `unique_ptr<T1, D1>::pointer` is implicitly convertible to `CT` and
- `unique_ptr<T2, D2>::pointer` is implicitly convertible to `CT`.

*Preconditions:* The specialization `less<CT>` is a function object
type [[function.objects]] that induces a strict weak
ordering [[alg.sorting]] on the pointer values.

*Returns:* `less<CT>()(x.get(), y.get())`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `y < x`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator<=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(y < x)`.

``` cpp
template<class T1, class D1, class T2, class D2>
  bool operator>=(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `!(x < y)`.

``` cpp
template<class T1, class D1, class T2, class D2>
  requires three_way_comparable_with<typename unique_ptr<T1, D1>::pointer,
                                     typename unique_ptr<T2, D2>::pointer>
  compare_three_way_result_t<typename unique_ptr<T1, D1>::pointer,
                             typename unique_ptr<T2, D2>::pointer>
    operator<=>(const unique_ptr<T1, D1>& x, const unique_ptr<T2, D2>& y);
```

*Returns:* `compare_three_way()(x.get(), y.get())`.

``` cpp
template<class T, class D>
  bool operator==(const unique_ptr<T, D>& x, nullptr_t) noexcept;
```

*Returns:* `!x`.

``` cpp
template<class T, class D>
  bool operator<(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  bool operator<(nullptr_t, const unique_ptr<T, D>& x);
```

*Preconditions:* The specialization `less<unique_ptr<T, D>::pointer>` is
a function object type [[function.objects]] that induces a strict weak
ordering [[alg.sorting]] on the pointer values.

*Returns:* The first function template returns

``` cpp
less<unique_ptr<T, D>::pointer>()(x.get(), nullptr)
```

The second function template returns

``` cpp
less<unique_ptr<T, D>::pointer>()(nullptr, x.get())
```

``` cpp
template<class T, class D>
  bool operator>(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  bool operator>(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `nullptr < x`. The second
function template returns `x < nullptr`.

``` cpp
template<class T, class D>
  bool operator<=(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  bool operator<=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(nullptr < x)`. The
second function template returns `!(x < nullptr)`.

``` cpp
template<class T, class D>
  bool operator>=(const unique_ptr<T, D>& x, nullptr_t);
template<class T, class D>
  bool operator>=(nullptr_t, const unique_ptr<T, D>& x);
```

*Returns:* The first function template returns `!(x < nullptr)`. The
second function template returns `!(nullptr < x)`.

``` cpp
template<class T, class D>
  requires three_way_comparable_with<typename unique_ptr<T, D>::pointer, nullptr_t>
  compare_three_way_result_t<typename unique_ptr<T, D>::pointer, nullptr_t>
    operator<=>(const unique_ptr<T, D>& x, nullptr_t);
```

*Returns:* `compare_three_way()(x.get(), nullptr)`.

#### I/O <a id="unique.ptr.io">[[unique.ptr.io]]</a>

``` cpp
template<class E, class T, class Y, class D>
  basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const unique_ptr<Y, D>& p);
```

*Constraints:* `os << p.get()` is a valid expression.

*Effects:* Equivalent to: `os << p.get();`

*Returns:* `os`.

### Class `bad_weak_ptr` <a id="util.smartptr.weak.bad">[[util.smartptr.weak.bad]]</a>

``` cpp
namespace std {
  class bad_weak_ptr : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

An exception of type `bad_weak_ptr` is thrown by the `shared_ptr`
constructor taking a `weak_ptr`.

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Class template `shared_ptr` <a id="util.smartptr.shared">[[util.smartptr.shared]]</a>

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
    constexpr shared_ptr(nullptr_t) noexcept : shared_ptr() { }
    template<class Y>
      explicit shared_ptr(Y* p);
    template<class Y, class D>
      shared_ptr(Y* p, D d);
    template<class Y, class D, class A>
      shared_ptr(Y* p, D d, A a);
    template<class D>
      shared_ptr(nullptr_t p, D d);
    template<class D, class A>
      shared_ptr(nullptr_t p, D d, A a);
    template<class Y>
      shared_ptr(const shared_ptr<Y>& r, element_type* p) noexcept;
    template<class Y>
      shared_ptr(shared_ptr<Y>&& r, element_type* p) noexcept;
    shared_ptr(const shared_ptr& r) noexcept;
    template<class Y>
      shared_ptr(const shared_ptr<Y>& r) noexcept;
    shared_ptr(shared_ptr&& r) noexcept;
    template<class Y>
      shared_ptr(shared_ptr<Y>&& r) noexcept;
    template<class Y>
      explicit shared_ptr(const weak_ptr<Y>& r);
    template<class Y, class D>
      shared_ptr(unique_ptr<Y, D>&& r);

    // [util.smartptr.shared.dest], destructor
    ~shared_ptr();

    // [util.smartptr.shared.assign], assignment
    shared_ptr& operator=(const shared_ptr& r) noexcept;
    template<class Y>
      shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    shared_ptr& operator=(shared_ptr&& r) noexcept;
    template<class Y>
      shared_ptr& operator=(shared_ptr<Y>&& r) noexcept;
    template<class Y, class D>
      shared_ptr& operator=(unique_ptr<Y, D>&& r);

    // [util.smartptr.shared.mod], modifiers
    void swap(shared_ptr& r) noexcept;
    void reset() noexcept;
    template<class Y>
      void reset(Y* p);
    template<class Y, class D>
      void reset(Y* p, D d);
    template<class Y, class D, class A>
      void reset(Y* p, D d, A a);

    // [util.smartptr.shared.obs], observers
    element_type* get() const noexcept;
    T& operator*() const noexcept;
    T* operator->() const noexcept;
    element_type& operator[](ptrdiff_t i) const;
    long use_count() const noexcept;
    explicit operator bool() const noexcept;
    template<class U>
      bool owner_before(const shared_ptr<U>& b) const noexcept;
    template<class U>
      bool owner_before(const weak_ptr<U>& b) const noexcept;
  };

  template<class T>
    shared_ptr(weak_ptr<T>) -> shared_ptr<T>;
  template<class T, class D>
    shared_ptr(unique_ptr<T, D>) -> shared_ptr<T>;
}
```

Specializations of `shared_ptr` shall be *Cpp17CopyConstructible*,
*Cpp17CopyAssignable*, and *Cpp17LessThanComparable*, allowing their use
in standard containers. Specializations of `shared_ptr` shall be
contextually convertible to `bool`, allowing their use in boolean
expressions and declarations in conditions.

The template parameter `T` of `shared_ptr` may be an incomplete type.

[*Note 1*: `T` may be a function type. — *end note*]

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

For the purposes of subclause [[smartptr]], a pointer type `Y*` is said
to be *compatible with* a pointer type `T*` when either `Y*` is
convertible to `T*` or `Y` is `U[N]` and `T` is cv `U[]`.

#### Constructors <a id="util.smartptr.shared.const">[[util.smartptr.shared.const]]</a>

In the constructor definitions below, enables `shared_from_this` with
`p`, for a pointer `p` of type `Y*`, means that if `Y` has an
unambiguous and accessible base class that is a specialization of
`enable_shared_from_this` [[util.smartptr.enab]], then `remove_cv_t<Y>*`
shall be implicitly convertible to `T*` and the constructor evaluates
the statement:

``` cpp
if (p != nullptr && p->weak_this.expired())
  p->weak_this = shared_ptr<remove_cv_t<Y>>(*this, const_cast<remove_cv_t<Y>*>(p));
```

The assignment to the `weak_this` member is not atomic and conflicts
with any potentially concurrent access to the same object
[[intro.multithread]].

``` cpp
constexpr shared_ptr() noexcept;
```

*Ensures:* `use_count() == 0 && get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(Y* p);
```

*Mandates:* `Y` is a complete type.

*Constraints:* When `T` is an array type, the expression `delete[] p` is
well-formed and either `T` is `U[N]` and `Y(*)[N]` is convertible to
`T*`, or `T` is `U[]` and `Y(*)[]` is convertible to `T*`. When `T` is
not an array type, the expression `delete p` is well-formed and `Y*` is
convertible to `T*`.

*Preconditions:* The expression `delete[] p`, when `T` is an array type,
or `delete p`, when `T` is not an array type, has well-defined behavior,
and does not throw exceptions.

*Effects:* When `T` is not an array type, constructs a `shared_ptr`
object that owns the pointer `p`. Otherwise, constructs a `shared_ptr`
that owns `p` and a deleter of an unspecified type that calls
`delete[] p`. When `T` is not an array type, enables `shared_from_this`
with `p`. If an exception is thrown, `delete p` is called when `T` is
not an array type, `delete[] p` otherwise.

*Ensures:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

``` cpp
template<class Y, class D> shared_ptr(Y* p, D d);
template<class Y, class D, class A> shared_ptr(Y* p, D d, A a);
template<class D> shared_ptr(nullptr_t p, D d);
template<class D, class A> shared_ptr(nullptr_t p, D d, A a);
```

*Constraints:* `is_move_constructible_v<D>` is `true`, and `d(p)` is a
well-formed expression. For the first two overloads:

- If `T` is an array type, then either `T` is `U[N]` and `Y(*)[N]` is
  convertible to `T*`, or `T` is `U[]` and `Y(*)[]` is convertible to
  `T*`.
- If `T` is not an array type, then `Y*` is convertible to `T*`.

*Preconditions:* Construction of `d` and a deleter of type `D`
initialized with `std::move(d)` do not throw exceptions. The expression
`d(p)` has well-defined behavior and does not throw exceptions. `A`
meets the *Cpp17Allocator* requirements ([[cpp17.allocator]]).

*Effects:* Constructs a `shared_ptr` object that owns the object `p` and
the deleter `d`. When `T` is not an array type, the first and second
constructors enable `shared_from_this` with `p`. The second and fourth
constructors shall use a copy of `a` to allocate memory for internal
use. If an exception is thrown, `d(p)` is called.

*Ensures:* `use_count() == 1 && get() == p`.

*Throws:* `bad_alloc`, or an *implementation-defined* exception when a
resource other than memory could not be obtained.

``` cpp
template<class Y> shared_ptr(const shared_ptr<Y>& r, element_type* p) noexcept;
template<class Y> shared_ptr(shared_ptr<Y>&& r, element_type* p) noexcept;
```

*Effects:* Constructs a `shared_ptr` instance that stores `p` and shares
ownership with the initial value of `r`.

*Ensures:* `get() == p`. For the second overload, `r` is empty and
`r.get() == nullptr`.

[*Note 1*: To avoid the possibility of a dangling pointer, the user of
this constructor should ensure that `p` remains valid at least until the
ownership group of `r` is destroyed. — *end note*]

[*Note 2*: This constructor allows creation of an empty `shared_ptr`
instance with a non-null stored pointer. — *end note*]

``` cpp
shared_ptr(const shared_ptr& r) noexcept;
template<class Y> shared_ptr(const shared_ptr<Y>& r) noexcept;
```

*Constraints:* For the second constructor, `Y*` is compatible with `T*`.

*Effects:* If `r` is empty, constructs an empty `shared_ptr` object;
otherwise, constructs a `shared_ptr` object that shares ownership with
`r`.

*Ensures:* `get() == r.get() && use_count() == r.use_count()`.

``` cpp
shared_ptr(shared_ptr&& r) noexcept;
template<class Y> shared_ptr(shared_ptr<Y>&& r) noexcept;
```

*Constraints:* For the second constructor, `Y*` is compatible with `T*`.

*Effects:* Move constructs a `shared_ptr` instance from `r`.

*Ensures:* `*this` shall contain the old value of `r`. `r` shall be
empty. `r.get() == nullptr`.

``` cpp
template<class Y> explicit shared_ptr(const weak_ptr<Y>& r);
```

*Constraints:* `Y*` is compatible with `T*`.

*Effects:* Constructs a `shared_ptr` object that shares ownership with
`r` and stores a copy of the pointer stored in `r`. If an exception is
thrown, the constructor has no effect.

*Ensures:* `use_count() == r.use_count()`.

*Throws:* `bad_weak_ptr` when `r.expired()`.

``` cpp
template<class Y, class D> shared_ptr(unique_ptr<Y, D>&& r);
```

*Constraints:* `Y*` is compatible with `T*` and
`unique_ptr<Y, D>::pointer` is convertible to `element_type*`.

*Effects:* If `r.get() == nullptr`, equivalent to `shared_ptr()`.
Otherwise, if `D` is not a reference type, equivalent to
`shared_ptr(r.release(), r.get_deleter())`. Otherwise, equivalent to
`shared_ptr(r.release(), ref(r.get_deleter()))`. If an exception is
thrown, the constructor has no effect.

#### Destructor <a id="util.smartptr.shared.dest">[[util.smartptr.shared.dest]]</a>

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

#### Assignment <a id="util.smartptr.shared.assign">[[util.smartptr.shared.assign]]</a>

``` cpp
shared_ptr& operator=(const shared_ptr& r) noexcept;
template<class Y> shared_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `shared_ptr(r).swap(*this)`.

*Returns:* `*this`.

[*Note 1*:

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
template<class Y, class D> shared_ptr& operator=(unique_ptr<Y, D>&& r);
```

*Effects:* Equivalent to `shared_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

#### Modifiers <a id="util.smartptr.shared.mod">[[util.smartptr.shared.mod]]</a>

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

#### Observers <a id="util.smartptr.shared.obs">[[util.smartptr.shared.obs]]</a>

``` cpp
element_type* get() const noexcept;
```

*Returns:* The stored pointer.

``` cpp
T& operator*() const noexcept;
```

*Preconditions:* `get() != 0`.

*Returns:* `*get()`.

*Remarks:* When `T` is an array type or cv `void`, it is unspecified
whether this member function is declared. If it is declared, it is
unspecified what its return type is, except that the declaration
(although not necessarily the definition) of the function shall be
well-formed.

``` cpp
T* operator->() const noexcept;
```

*Preconditions:* `get() != 0`.

*Returns:* `get()`.

*Remarks:* When `T` is an array type, it is unspecified whether this
member function is declared. If it is declared, it is unspecified what
its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well-formed.

``` cpp
element_type& operator[](ptrdiff_t i) const;
```

*Preconditions:* `get() != 0 && i >= 0`. If `T` is `U[N]`, `i < N`.

*Returns:* `get()[i]`.

*Remarks:* When `T` is not an array type, it is unspecified whether this
member function is declared. If it is declared, it is unspecified what
its return type is, except that the declaration (although not
necessarily the definition) of the function shall be well-formed.

*Throws:* Nothing.

``` cpp
long use_count() const noexcept;
```

*Returns:* The number of `shared_ptr` objects, `*this` included, that
share ownership with `*this`, or `0` when `*this` is empty.

*Synchronization:* None.

[*Note 1*: `get() == nullptr` does not imply a specific return value of
`use_count()`. — *end note*]

[*Note 2*: `weak_ptr<T>::lock()` can affect the return value of
`use_count()`. — *end note*]

[*Note 3*: When multiple threads can affect the return value of
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

#### Creation <a id="util.smartptr.shared.create">[[util.smartptr.shared.create]]</a>

The common requirements that apply to all `make_shared`,
`allocate_shared`, `make_shared_for_overwrite`, and
`allocate_shared_for_overwrite` overloads, unless specified otherwise,
are described below.

``` cpp
template<class T, ...>
  shared_ptr<T> make_shared(args);
template<class T, class A, ...>
  shared_ptr<T> allocate_shared(const A& a, args);
template<class T, ...>
  shared_ptr<T> make_shared_for_overwrite(args);
template<class T, class A, ...>
  shared_ptr<T> allocate_shared_for_overwrite(const A& a, args);
```

*Preconditions:* `A` meets the *Cpp17Allocator* requirements
([[cpp17.allocator]]).

*Effects:* Allocates memory for an object of type `T` (or `U[N]` when
`T` is `U[]`, where `N` is determined from *args* as specified by the
concrete overload). The object is initialized from *args* as specified
by the concrete overload. The `allocate_shared` and
`allocate_shared_for_overwrite` templates use a copy of `a` (rebound for
an unspecified `value_type`) to allocate memory. If an exception is
thrown, the functions have no effect.

*Returns:* A `shared_ptr` instance that stores and owns the address of
the newly constructed object.

*Ensures:* `r.get() != 0 && r.use_count() == 1`, where `r` is the return
value.

*Throws:* `bad_alloc`, or an exception thrown from `allocate` or from
the initialization of the object.

*Remarks:*

- Implementations should perform no more than one memory allocation.
  \[*Note 1*: This provides efficiency equivalent to an intrusive smart
  pointer. — *end note*]
- When an object of an array type `U` is specified to have an initial
  value of `u` (of the same type), this shall be interpreted to mean
  that each array element of the object has as its initial value the
  corresponding element from `u`.
- When an object of an array type is specified to have a default initial
  value, this shall be interpreted to mean that each array element of
  the object has a default initial value.
- When a (sub)object of a non-array type `U` is specified to have an
  initial value of `v`, or `U(l...)`, where `l...` is a list of
  constructor arguments, `make_shared` shall initialize this (sub)object
  via the expression `::new(pv) U(v)` or `::new(pv) U(l...)`
  respectively, where `pv` has type `void*` and points to storage
  suitable to hold an object of type `U`.
- When a (sub)object of a non-array type `U` is specified to have an
  initial value of `v`, or `U(l...)`, where `l...` is a list of
  constructor arguments, `allocate_shared` shall initialize this
  (sub)object via the expression
  - `allocator_traits<A2>::construct(a2, pv, v)` or
  - `allocator_traits<A2>::construct(a2, pv, l...)`

  respectively, where `pv` points to storage suitable to hold an object
  of type `U` and `a2` of type `A2` is a rebound copy of the allocator
  `a` passed to `allocate_shared` such that its `value_type` is
  `remove_cv_t<U>`.
- When a (sub)object of non-array type `U` is specified to have a
  default initial value, `make_shared` shall initialize this (sub)object
  via the expression `::new(pv) U()`, where `pv` has type `void*` and
  points to storage suitable to hold an object of type `U`.
- When a (sub)object of non-array type `U` is specified to have a
  default initial value, `allocate_shared` shall initialize this
  (sub)object via the expression
  `allocator_traits<A2>::construct(a2, pv)`, where `pv` points to
  storage suitable to hold an object of type `U` and `a2` of type `A2`
  is a rebound copy of the allocator `a` passed to `allocate_shared`
  such that its `value_type` is `remove_cv_t<U>`.
- When a (sub)object of non-array type `U` is initialized by
  `make_shared_for_overwrite` or `allocate_shared_for_overwrite`, it is
  initialized via the expression `::new(pv) U`, where `pv` has type
  `void*` and points to storage suitable to hold an object of type `U`.
- Array elements are initialized in ascending order of their addresses.
- When the lifetime of the object managed by the return value ends, or
  when the initialization of an array element throws an exception, the
  initialized elements are destroyed in the reverse order of their
  original construction.
- When a (sub)object of non-array type `U` that was initialized by
  `make_shared` is to be destroyed, it is destroyed via the expression
  `pv->~U()` where `pv` points to that object of type `U`.
- When a (sub)object of non-array type `U` that was initialized by
  `allocate_shared` is to be destroyed, it is destroyed via the
  expression `allocator_traits<A2>::destroy(a2, pv)` where `pv` points
  to that object of type `remove_cv_t<U>` and `a2` of type `A2` is a
  rebound copy of the allocator `a` passed to `allocate_shared` such
  that its `value_type` is `remove_cv_t<U>`.

[*Note 1*: These functions will typically allocate more memory than
`sizeof(T)` to allow for internal bookkeeping structures such as
reference counts. — *end note*]

``` cpp
template<class T, class... Args>
  shared_ptr<T> make_shared(Args&&... args);                    // T is not array
template<class T, class A, class... Args>
  shared_ptr<T> allocate_shared(const A& a, Args&&... args);    // T is not array
```

*Constraints:* `T` is not an array type.

*Returns:* A `shared_ptr` to an object of type `T` with an initial value
`T(forward<Args>(args)...)`.

*Remarks:* The `shared_ptr` constructors called by these functions
enable `shared_from_this` with the address of the newly constructed
object of type `T`.

[*Example 1*:

``` cpp
shared_ptr<int> p = make_shared<int>(); // shared_ptr to int()
shared_ptr<vector<int>> q = make_shared<vector<int>>(16, 1);
  // shared_ptr to vector of 16 elements with value 1
```

— *end example*]

``` cpp
template<class T> shared_ptr<T>
  make_shared(size_t N);                                        // T is U[]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a, size_t N);          // T is U[]
```

*Constraints:* `T` is of the form `U[]`.

*Returns:* A `shared_ptr` to an object of type `U[N]` with a default
initial value, where `U` is `remove_extent_t<T>`.

[*Example 2*:

``` cpp
shared_ptr<double[]> p = make_shared<double[]>(1024);
  // shared_ptr to a value-initialized double[1024]
shared_ptr<double[][2][2]> q = make_shared<double[][2][2]>(6);
  // shared_ptr to a value-initialized double[6][2][2]
```

— *end example*]

``` cpp
template<class T>
  shared_ptr<T> make_shared();                                  // T is U[N]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a);                    // T is U[N]
```

*Constraints:* `T` is of the form `U[N]`.

*Returns:* A `shared_ptr` to an object of type `T` with a default
initial value.

[*Example 3*:

``` cpp
shared_ptr<double[1024]> p = make_shared<double[1024]>();
  // shared_ptr to a value-initialized double[1024]
shared_ptr<double[6][2][2]> q = make_shared<double[6][2][2]>();
  // shared_ptr to a value-initialized double[6][2][2]
```

— *end example*]

``` cpp
template<class T>
  shared_ptr<T> make_shared(size_t N,
                            const remove_extent_t<T>& u);       // T is U[]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a, size_t N,
                                const remove_extent_t<T>& u);   // T is U[]
```

*Constraints:* `T` is of the form `U[]`.

*Returns:* A `shared_ptr` to an object of type `U[N]`, where `U` is
`remove_extent_t<T>` and each array element has an initial value of `u`.

[*Example 4*:

``` cpp
shared_ptr<double[]> p = make_shared<double[]>(1024, 1.0);
  // shared_ptr to a double[1024], where each element is 1.0
shared_ptr<double[][2]> q = make_shared<double[][2]>(6, {1.0, 0.0});
  // shared_ptr to a double[6][2], where each double[2] element is {1.0, 0.0}
shared_ptr<vector<int>[]> r = make_shared<vector<int>[]>(4, {1, 2});
  // shared_ptr to a vector<int>[4], where each vector has contents {1, 2}
```

— *end example*]

``` cpp
template<class T>
  shared_ptr<T> make_shared(const remove_extent_t<T>& u);       // T is U[N]
template<class T, class A>
  shared_ptr<T> allocate_shared(const A& a,
                                const remove_extent_t<T>& u);   // T is U[N]
```

*Constraints:* `T` is of the form `U[N]`.

*Returns:* A `shared_ptr` to an object of type `T`, where each array
element of type `remove_extent_t<T>` has an initial value of `u`.

[*Example 5*:

``` cpp
shared_ptr<double[1024]> p = make_shared<double[1024]>(1.0);
  // shared_ptr to a double[1024], where each element is 1.0
shared_ptr<double[6][2]> q = make_shared<double[6][2]>({1.0, 0.0});
  // shared_ptr to a double[6][2], where each double[2] element is {1.0, 0.0}
shared_ptr<vector<int>[4]> r = make_shared<vector<int>[4]>({1, 2});
  // shared_ptr to a vector<int>[4], where each vector has contents {1, 2}
```

— *end example*]

``` cpp
template<class T>
  shared_ptr<T> make_shared_for_overwrite();
template<class T, class A>
  shared_ptr<T> allocate_shared_for_overwrite(const A& a);
```

*Constraints:* `T` is not an array of unknown bound.

*Returns:* A `shared_ptr` to an object of type `T`.

[*Example 6*:

``` cpp
struct X { double data[1024]; };
shared_ptr<X> p = make_shared_for_overwrite<X>();
  // shared_ptr to a default-initialized X, where each element in X::data has an indeterminate value

shared_ptr<double[1024]> q = make_shared_for_overwrite<double[1024]>();
  // shared_ptr to a default-initialized double[1024], where each element has an indeterminate value
```

— *end example*]

``` cpp
template<class T>
  shared_ptr<T> make_shared_for_overwrite(size_t N);
template<class T, class A>
  shared_ptr<T> allocate_shared_for_overwrite(const A& a, size_t N);
```

*Constraints:* `T` is an array of unknown bound.

*Returns:* A `shared_ptr` to an object of type `U[N]`, where `U` is
`remove_extent_t<T>`.

[*Example 7*:

``` cpp
shared_ptr<double[]> p = make_shared_for_overwrite<double[]>(1024);
  // shared_ptr to a default-initialized double[1024], where each element has an indeterminate value
```

— *end example*]

#### Comparison <a id="util.smartptr.shared.cmp">[[util.smartptr.shared.cmp]]</a>

``` cpp
template<class T, class U>
  bool operator==(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `a.get() == b.get()`.

``` cpp
template<class T>
  bool operator==(const shared_ptr<T>& a, nullptr_t) noexcept;
```

*Returns:* `!a`.

``` cpp
template<class T, class U>
  strong_ordering operator<=>(const shared_ptr<T>& a, const shared_ptr<U>& b) noexcept;
```

*Returns:* `compare_three_way()(a.get(), b.get())`.

[*Note 1*: Defining a comparison function allows `shared_ptr` objects
to be used as keys in associative containers. — *end note*]

``` cpp
template<class T>
  strong_ordering operator<=>(const shared_ptr<T>& a, nullptr_t) noexcept;
```

*Returns:* `compare_three_way()(a.get(), nullptr)`.

#### Specialized algorithms <a id="util.smartptr.shared.spec">[[util.smartptr.shared.spec]]</a>

``` cpp
template<class T>
  void swap(shared_ptr<T>& a, shared_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

#### Casts <a id="util.smartptr.shared.cast">[[util.smartptr.shared.cast]]</a>

``` cpp
template<class T, class U>
  shared_ptr<T> static_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> static_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `static_cast<T*>((U*)nullptr)` is
well-formed.

*Returns:*

``` cpp
shared_ptr<T>(R, static_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

where *`R`* is `r` for the first overload, and `std::move(r)` for the
second.

[*Note 1*: The seemingly equivalent expression
`shared_ptr<T>(static_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

``` cpp
template<class T, class U>
  shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> dynamic_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `dynamic_cast<T*>((U*)nullptr)` is
well-formed. The expression
`dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())` is well
formed.

*Preconditions:* The expression
`dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())` has
well-defined behavior.

*Returns:*

- When `dynamic_cast<typename shared_ptr<T>::element_type*>(r.get())`
  returns a non-null value `p`, `shared_ptr<T>(`*`R`*`, p)`, where *`R`*
  is `r` for the first overload, and `std::move(r)` for the second.
- Otherwise, `shared_ptr<T>()`.

[*Note 2*: The seemingly equivalent expression
`shared_ptr<T>(dynamic_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

``` cpp
template<class T, class U>
  shared_ptr<T> const_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> const_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `const_cast<T*>((U*)nullptr)` is well-formed.

*Returns:*

``` cpp
shared_ptr<T>(R, const_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

where *`R`* is `r` for the first overload, and `std::move(r)` for the
second.

[*Note 3*: The seemingly equivalent expression
`shared_ptr<T>(const_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

``` cpp
template<class T, class U>
  shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& r) noexcept;
template<class T, class U>
  shared_ptr<T> reinterpret_pointer_cast(shared_ptr<U>&& r) noexcept;
```

*Mandates:* The expression `reinterpret_cast<T*>((U*)nullptr)` is
well-formed.

*Returns:*

``` cpp
shared_ptr<T>(R, reinterpret_cast<typename shared_ptr<T>::element_type*>(r.get()))
```

where *`R`* is `r` for the first overload, and `std::move(r)` for the
second.

[*Note 4*: The seemingly equivalent expression
`shared_ptr<T>(reinterpret_cast<T*>(r.get()))` will eventually result in
undefined behavior, attempting to delete the same object
twice. — *end note*]

#### `get_deleter` <a id="util.smartptr.getdeleter">[[util.smartptr.getdeleter]]</a>

``` cpp
template<class D, class T>
  D* get_deleter(const shared_ptr<T>& p) noexcept;
```

*Returns:* If `p` owns a deleter `d` of type cv-unqualified `D`, returns
`addressof(d)`; otherwise returns `nullptr`. The returned pointer
remains valid as long as there exists a `shared_ptr` instance that owns
`d`.

[*Note 1*: It is unspecified whether the pointer remains valid longer
than that. This can happen if the implementation doesn’t destroy the
deleter until all `weak_ptr` instances that share ownership with `p`
have been destroyed. — *end note*]

#### I/O <a id="util.smartptr.shared.io">[[util.smartptr.shared.io]]</a>

``` cpp
template<class E, class T, class Y>
  basic_ostream<E, T>& operator<<(basic_ostream<E, T>& os, const shared_ptr<Y>& p);
```

*Effects:* As if by: `os << p.get();`

*Returns:* `os`.

### Class template `weak_ptr` <a id="util.smartptr.weak">[[util.smartptr.weak]]</a>

The `weak_ptr` class template stores a weak reference to an object that
is already managed by a `shared_ptr`. To access the object, a `weak_ptr`
can be converted to a `shared_ptr` using the member function `lock`.

``` cpp
namespace std {
  template<class T> class weak_ptr {
  public:
    using element_type = remove_extent_t<T>;

    // [util.smartptr.weak.const], constructors
    constexpr weak_ptr() noexcept;
    template<class Y>
      weak_ptr(const shared_ptr<Y>& r) noexcept;
    weak_ptr(const weak_ptr& r) noexcept;
    template<class Y>
      weak_ptr(const weak_ptr<Y>& r) noexcept;
    weak_ptr(weak_ptr&& r) noexcept;
    template<class Y>
      weak_ptr(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.dest], destructor
    ~weak_ptr();

    // [util.smartptr.weak.assign], assignment
    weak_ptr& operator=(const weak_ptr& r) noexcept;
    template<class Y>
      weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
    template<class Y>
      weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
    weak_ptr& operator=(weak_ptr&& r) noexcept;
    template<class Y>
      weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;

    // [util.smartptr.weak.mod], modifiers
    void swap(weak_ptr& r) noexcept;
    void reset() noexcept;

    // [util.smartptr.weak.obs], observers
    long use_count() const noexcept;
    bool expired() const noexcept;
    shared_ptr<T> lock() const noexcept;
    template<class U>
      bool owner_before(const shared_ptr<U>& b) const noexcept;
    template<class U>
      bool owner_before(const weak_ptr<U>& b) const noexcept;
  };

  template<class T>
    weak_ptr(shared_ptr<T>) -> weak_ptr<T>;

  // [util.smartptr.weak.spec], specialized algorithms
  template<class T>
    void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
}
```

Specializations of `weak_ptr` shall be *Cpp17CopyConstructible* and
*Cpp17CopyAssignable*, allowing their use in standard containers. The
template parameter `T` of `weak_ptr` may be an incomplete type.

#### Constructors <a id="util.smartptr.weak.const">[[util.smartptr.weak.const]]</a>

``` cpp
constexpr weak_ptr() noexcept;
```

*Effects:* Constructs an empty `weak_ptr` object.

*Ensures:* `use_count() == 0`.

``` cpp
weak_ptr(const weak_ptr& r) noexcept;
template<class Y> weak_ptr(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr(const shared_ptr<Y>& r) noexcept;
```

*Constraints:* For the second and third constructors, `Y*` is compatible
with `T*`.

*Effects:* If `r` is empty, constructs an empty `weak_ptr` object;
otherwise, constructs a `weak_ptr` object that shares ownership with `r`
and stores a copy of the pointer stored in `r`.

*Ensures:* `use_count() == r.use_count()`.

``` cpp
weak_ptr(weak_ptr&& r) noexcept;
template<class Y> weak_ptr(weak_ptr<Y>&& r) noexcept;
```

*Constraints:* For the second constructor, `Y*` is compatible with `T*`.

*Effects:* Move constructs a `weak_ptr` instance from `r`.

*Ensures:* `*this` shall contain the old value of `r`. `r` shall be
empty. `r.use_count() == 0`.

#### Destructor <a id="util.smartptr.weak.dest">[[util.smartptr.weak.dest]]</a>

``` cpp
~weak_ptr();
```

*Effects:* Destroys this `weak_ptr` object but has no effect on the
object its stored pointer points to.

#### Assignment <a id="util.smartptr.weak.assign">[[util.smartptr.weak.assign]]</a>

``` cpp
weak_ptr& operator=(const weak_ptr& r) noexcept;
template<class Y> weak_ptr& operator=(const weak_ptr<Y>& r) noexcept;
template<class Y> weak_ptr& operator=(const shared_ptr<Y>& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(r).swap(*this)`.

*Remarks:* The implementation may meet the effects (and the implied
guarantees) via different means, without creating a temporary object.

*Returns:* `*this`.

``` cpp
weak_ptr& operator=(weak_ptr&& r) noexcept;
template<class Y> weak_ptr& operator=(weak_ptr<Y>&& r) noexcept;
```

*Effects:* Equivalent to `weak_ptr(std::move(r)).swap(*this)`.

*Returns:* `*this`.

#### Modifiers <a id="util.smartptr.weak.mod">[[util.smartptr.weak.mod]]</a>

``` cpp
void swap(weak_ptr& r) noexcept;
```

*Effects:* Exchanges the contents of `*this` and `r`.

``` cpp
void reset() noexcept;
```

*Effects:* Equivalent to `weak_ptr().swap(*this)`.

#### Observers <a id="util.smartptr.weak.obs">[[util.smartptr.weak.obs]]</a>

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

#### Specialized algorithms <a id="util.smartptr.weak.spec">[[util.smartptr.weak.spec]]</a>

``` cpp
template<class T>
  void swap(weak_ptr<T>& a, weak_ptr<T>& b) noexcept;
```

*Effects:* Equivalent to `a.swap(b)`.

### Class template `owner_less` <a id="util.smartptr.ownerless">[[util.smartptr.ownerless]]</a>

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

`operator()(x, y)` returns `x.owner_before(y)`.

[*Note 1*:

Note that

- `operator()` defines a strict weak ordering as defined in 
  [[alg.sorting]];
- under the equivalence relation defined by `operator()`,
  `!operator()(a, b) && !operator()(b, a)`, two `shared_ptr` or
  `weak_ptr` instances are equivalent if and only if they share
  ownership or are both empty.

— *end note*]

### Class template `enable_shared_from_this` <a id="util.smartptr.enab">[[util.smartptr.enab]]</a>

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
    mutable weak_ptr<T> weak_this;  // exposition only
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

### Smart pointer hash support <a id="util.smartptr.hash">[[util.smartptr.hash]]</a>

``` cpp
template<class T, class D> struct hash<unique_ptr<T, D>>;
```

Letting `UP` be `unique_ptr<T,D>`, the specialization `hash<UP>` is
enabled [[unord.hash]] if and only if `hash<typename UP::pointer>` is
enabled. When enabled, for an object `p` of type `UP`, `hash<UP>()(p)`
evaluates to the same value as `hash<typename UP::pointer>()(p.get())`.
The member functions are not guaranteed to be `noexcept`.

``` cpp
template<class T> struct hash<shared_ptr<T>>;
```

For an object `p` of type `shared_ptr<T>`, `hash<shared_ptr<T>>()(p)`
evaluates to the same value as
`hash<typename shared_ptr<T>::element_type*>()(p.get())`.

## Memory resources <a id="mem.res">[[mem.res]]</a>

### Header `<memory_resource>` synopsis <a id="mem.res.syn">[[mem.res.syn]]</a>

``` cpp
namespace std::pmr {
  // [mem.res.class], class memory_resource
  class memory_resource;

  bool operator==(const memory_resource& a, const memory_resource& b) noexcept;

  // [mem.poly.allocator.class], class template polymorphic_allocator
  template<class Tp> class polymorphic_allocator;

  template<class T1, class T2>
    bool operator==(const polymorphic_allocator<T1>& a,
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
namespace std::pmr {
  class memory_resource {
    static constexpr size_t max_align = alignof(max_align_t);   // exposition only

  public:
    memory_resource() = default;
    memory_resource(const memory_resource&) = default;
    virtual ~memory_resource();

    memory_resource& operator=(const memory_resource&) = default;

    [[nodiscard]] void* allocate(size_t bytes, size_t alignment = max_align);
    void deallocate(void* p, size_t bytes, size_t alignment = max_align);

    bool is_equal(const memory_resource& other) const noexcept;

  private:
    virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
    virtual void do_deallocate(void* p, size_t bytes, size_t alignment) = 0;

    virtual bool do_is_equal(const memory_resource& other) const noexcept = 0;
  };
}
```

#### Public member functions <a id="mem.res.public">[[mem.res.public]]</a>

``` cpp
~memory_resource();
```

*Effects:* Destroys this `memory_resource`.

``` cpp
[[nodiscard]] void* allocate(size_t bytes, size_t alignment = max_align);
```

*Effects:* Equivalent to: `return do_allocate(bytes, alignment);`

``` cpp
void deallocate(void* p, size_t bytes, size_t alignment = max_align);
```

*Effects:* Equivalent to `do_deallocate(p, bytes, alignment)`.

``` cpp
bool is_equal(const memory_resource& other) const noexcept;
```

*Effects:* Equivalent to: `return do_is_equal(other);`

#### Private virtual member functions <a id="mem.res.private">[[mem.res.private]]</a>

``` cpp
virtual void* do_allocate(size_t bytes, size_t alignment) = 0;
```

*Preconditions:* `alignment` is a power of two.

*Returns:* A derived class shall implement this function to return a
pointer to allocated storage [[basic.stc.dynamic.allocation]] with a
size of at least `bytes`, aligned to the specified `alignment`.

*Throws:* A derived class implementation shall throw an appropriate
exception if it is unable to allocate memory with the requested size and
alignment.

``` cpp
virtual void do_deallocate(void* p, size_t bytes, size_t alignment) = 0;
```

*Preconditions:* `p` was returned from a prior call to
`allocate(bytes, alignment)` on a memory resource equal to `*this`, and
the storage at `p` has not yet been deallocated.

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
`this`. For a derived class `D`, an implementation of this function
could immediately return `false` if
`dynamic_cast<const D*>(&other) == nullptr`. — *end note*]

#### Equality <a id="mem.res.eq">[[mem.res.eq]]</a>

``` cpp
bool operator==(const memory_resource& a, const memory_resource& b) noexcept;
```

*Returns:* `&a == &b || a.is_equal(b)`.

### Class template `polymorphic_allocator` <a id="mem.poly.allocator.class">[[mem.poly.allocator.class]]</a>

A specialization of class template `pmr::polymorphic_allocator` meets
the *Cpp17Allocator* requirements ([[cpp17.allocator]]). Constructed
with different memory resources, different instances of the same
specialization of `pmr::polymorphic_allocator` can exhibit entirely
different allocation behavior. This runtime polymorphism allows objects
that use `polymorphic_allocator` to behave as if they used different
allocator types at run time even though they use the same static
allocator type.

All specializations of class template `pmr::polymorphic_allocator` meet
the allocator completeness requirements
[[allocator.requirements.completeness]].

``` cpp
namespace std::pmr {
  template<class Tp = byte> class polymorphic_allocator {
    memory_resource* memory_rsrc;       // exposition only

  public:
    using value_type = Tp;

    // [mem.poly.allocator.ctor], constructors
    polymorphic_allocator() noexcept;
    polymorphic_allocator(memory_resource* r);

    polymorphic_allocator(const polymorphic_allocator& other) = default;

    template<class U>
      polymorphic_allocator(const polymorphic_allocator<U>& other) noexcept;

    polymorphic_allocator& operator=(const polymorphic_allocator&) = delete;

    // [mem.poly.allocator.mem], member functions
    [[nodiscard]] Tp* allocate(size_t n);
    void deallocate(Tp* p, size_t n);

    [[nodiscard]] void* allocate_bytes(size_t nbytes, size_t alignment = alignof(max_align_t));
    void deallocate_bytes(void* p, size_t nbytes, size_t alignment = alignof(max_align_t));
    template<class T> [[nodiscard]] T* allocate_object(size_t n = 1);
    template<class T> void deallocate_object(T* p, size_t n = 1);
    template<class T, class... CtorArgs> [[nodiscard]] T* new_object(CtorArgs&&... ctor_args);
    template<class T> void delete_object(T* p);

    template<class T, class... Args>
      void construct(T* p, Args&&... args);

    template<class T>
      void destroy(T* p);

    polymorphic_allocator select_on_container_copy_construction() const;

    memory_resource* resource() const;
  };
}
```

#### Constructors <a id="mem.poly.allocator.ctor">[[mem.poly.allocator.ctor]]</a>

``` cpp
polymorphic_allocator() noexcept;
```

*Effects:* Sets `memory_rsrc` to `get_default_resource()`.

``` cpp
polymorphic_allocator(memory_resource* r);
```

*Preconditions:* `r` is non-null.

*Effects:* Sets `memory_rsrc` to `r`.

*Throws:* Nothing.

[*Note 1*: This constructor provides an implicit conversion from
`memory_resource*`. — *end note*]

``` cpp
template<class U> polymorphic_allocator(const polymorphic_allocator<U>& other) noexcept;
```

*Effects:* Sets `memory_rsrc` to `other.resource()`.

#### Member functions <a id="mem.poly.allocator.mem">[[mem.poly.allocator.mem]]</a>

``` cpp
[[nodiscard]] Tp* allocate(size_t n);
```

*Effects:* If `numeric_limits<size_t>::max() / sizeof(Tp) < n`, throws
`bad_array_new_length`. Otherwise equivalent to:

``` cpp
return static_cast<Tp*>(memory_rsrc->allocate(n * sizeof(Tp), alignof(Tp)));
```

``` cpp
void deallocate(Tp* p, size_t n);
```

*Preconditions:* `p` was allocated from a memory resource `x`, equal to
`*memory_rsrc`, using `x.allocate(n * sizeof(Tp), alignof(Tp))`.

*Effects:* Equivalent to
`memory_rsrc->deallocate(p, n * sizeof(Tp), alignof(Tp))`.

*Throws:* Nothing.

``` cpp
[[nodiscard]] void* allocate_bytes(size_t nbytes, size_t alignment = alignof(max_align_t));
```

*Effects:* Equivalent to:
`return memory_rsrc->allocate(nbytes, alignment);`

[*Note 1*: The return type is `void*` (rather than, e.g., `byte*`) to
support conversion to an arbitrary pointer type `U*` by
`static_cast<U*>`, thus facilitating construction of a `U` object in the
allocated memory. — *end note*]

``` cpp
void deallocate_bytes(void* p, size_t nbytes, size_t alignment = alignof(max_align_t));
```

*Effects:* Equivalent to
`memory_rsrc->deallocate(p, nbytes, alignment)`.

``` cpp
template<class T>
  [[nodiscard]] T* allocate_object(size_t n = 1);
```

*Effects:* Allocates memory suitable for holding an array of `n` objects
of type `T`, as follows:

- if `numeric_limits<size_t>::max() / sizeof(T) < n`, throws
  `bad_array_new_length`,
- otherwise equivalent to:
  ``` cpp
  return static_cast<T*>(allocate_bytes(n*sizeof(T), alignof(T)));
  ```

[*Note 2*: `T` is not deduced and must therefore be provided as a
template argument. — *end note*]

``` cpp
template<class T>
  void deallocate_object(T* p, size_t n = 1);
```

*Effects:* Equivalent to `deallocate_bytes(p, n*sizeof(T), alignof(T))`.

``` cpp
template<class T, class CtorArgs...>
  [[nodiscard]] T* new_object(CtorArgs&&... ctor_args);
```

*Effects:* Allocates and constructs an object of type `T`, as follows.
Equivalent to:

``` cpp
T* p = allocate_object<T>();
try {
  construct(p, std::forward<CtorArgs>(ctor_args)...);
} catch (...) {
  deallocate_object(p);
  throw;
}
return p;
```

[*Note 3*: `T` is not deduced and must therefore be provided as a
template argument. — *end note*]

``` cpp
template<class T>
  void delete_object(T* p);
```

*Effects:* Equivalent to:

``` cpp
destroy(p);
deallocate_object(p);
```

``` cpp
template<class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Mandates:* Uses-allocator construction of `T` with allocator `*this`
(see  [[allocator.uses.construction]]) and constructor arguments
`std::forward<Args>(args)...` is well-formed.

*Effects:* Construct a `T` object in the storage whose address is
represented by `p` by uses-allocator construction with allocator `*this`
and constructor arguments `std::forward<Args>(args)...`.

*Throws:* Nothing unless the constructor for `T` throws.

``` cpp
template<class T>
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

#### Equality <a id="mem.poly.allocator.eq">[[mem.poly.allocator.eq]]</a>

``` cpp
template<class T1, class T2>
  bool operator==(const polymorphic_allocator<T1>& a,
                  const polymorphic_allocator<T2>& b) noexcept;
```

*Returns:* `*a.resource() == *b.resource()`.

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
  increases geometrically. \[*Note 1*: By allocating memory in chunks,
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
namespace std::pmr {
  struct pool_options {
    size_t max_blocks_per_chunk = 0;
    size_t largest_required_pool_block = 0;
  };

  class synchronized_pool_resource : public memory_resource {
  public:
    synchronized_pool_resource(const pool_options& opts, memory_resource* upstream);

    synchronized_pool_resource()
        : synchronized_pool_resource(pool_options(), get_default_resource()) {}
    explicit synchronized_pool_resource(memory_resource* upstream)
        : synchronized_pool_resource(pool_options(), upstream) {}
    explicit synchronized_pool_resource(const pool_options& opts)
        : synchronized_pool_resource(opts, get_default_resource()) {}

    synchronized_pool_resource(const synchronized_pool_resource&) = delete;
    virtual ~synchronized_pool_resource();

    synchronized_pool_resource& operator=(const synchronized_pool_resource&) = delete;

    void release();
    memory_resource* upstream_resource() const;
    pool_options options() const;

  protected:
    void* do_allocate(size_t bytes, size_t alignment) override;
    void do_deallocate(void* p, size_t bytes, size_t alignment) override;

    bool do_is_equal(const memory_resource& other) const noexcept override;
  };

  class unsynchronized_pool_resource : public memory_resource {
  public:
    unsynchronized_pool_resource(const pool_options& opts, memory_resource* upstream);

    unsynchronized_pool_resource()
        : unsynchronized_pool_resource(pool_options(), get_default_resource()) {}
    explicit unsynchronized_pool_resource(memory_resource* upstream)
        : unsynchronized_pool_resource(pool_options(), upstream) {}
    explicit unsynchronized_pool_resource(const pool_options& opts)
        : unsynchronized_pool_resource(opts, get_default_resource()) {}

    unsynchronized_pool_resource(const unsynchronized_pool_resource&) = delete;
    virtual ~unsynchronized_pool_resource();

    unsynchronized_pool_resource& operator=(const unsynchronized_pool_resource&) = delete;

    void release();
    memory_resource* upstream_resource() const;
    pool_options options() const;

  protected:
    void* do_allocate(size_t bytes, size_t alignment) override;
    void do_deallocate(void* p, size_t bytes, size_t alignment) override;

    bool do_is_equal(const memory_resource& other) const noexcept override;
  };
}
```

#### `pool_options` data members <a id="mem.res.pool.options">[[mem.res.pool.options]]</a>

The members of `pool_options` comprise a set of constructor options for
pool resources. The effect of each option on the pool resource behavior
is described below:

``` cpp
size_t max_blocks_per_chunk;
```

The maximum number of blocks that will be allocated at once from the
upstream memory resource [[mem.res.monotonic.buffer]] to replenish a
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

#### Constructors and destructors <a id="mem.res.pool.ctor">[[mem.res.pool.ctor]]</a>

``` cpp
synchronized_pool_resource(const pool_options& opts, memory_resource* upstream);
unsynchronized_pool_resource(const pool_options& opts, memory_resource* upstream);
```

*Preconditions:* `upstream` is the address of a valid memory resource.

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

#### Members <a id="mem.res.pool.mem">[[mem.res.pool.mem]]</a>

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

*Returns:* A pointer to allocated
storage [[basic.stc.dynamic.allocation]] with a size of at least
`bytes`. The size and alignment of the allocated memory shall meet the
requirements for a class derived from
`memory_resource`[[mem.res.class]].

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
bool do_is_equal(const memory_resource& other) const noexcept override;
```

*Returns:* `this == &other`.

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
namespace std::pmr {
  class monotonic_buffer_resource : public memory_resource {
    memory_resource* upstream_rsrc;     // exposition only
    void* current_buffer;               // exposition only
    size_t next_buffer_size;            // exposition only

  public:
    explicit monotonic_buffer_resource(memory_resource* upstream);
    monotonic_buffer_resource(size_t initial_size, memory_resource* upstream);
    monotonic_buffer_resource(void* buffer, size_t buffer_size, memory_resource* upstream);

    monotonic_buffer_resource()
      : monotonic_buffer_resource(get_default_resource()) {}
    explicit monotonic_buffer_resource(size_t initial_size)
      : monotonic_buffer_resource(initial_size, get_default_resource()) {}
    monotonic_buffer_resource(void* buffer, size_t buffer_size)
      : monotonic_buffer_resource(buffer, buffer_size, get_default_resource()) {}

    monotonic_buffer_resource(const monotonic_buffer_resource&) = delete;

    virtual ~monotonic_buffer_resource();

    monotonic_buffer_resource& operator=(const monotonic_buffer_resource&) = delete;

    void release();
    memory_resource* upstream_resource() const;

  protected:
    void* do_allocate(size_t bytes, size_t alignment) override;
    void do_deallocate(void* p, size_t bytes, size_t alignment) override;

    bool do_is_equal(const memory_resource& other) const noexcept override;
  };
}
```

#### Constructors and destructor <a id="mem.res.monotonic.buffer.ctor">[[mem.res.monotonic.buffer.ctor]]</a>

``` cpp
explicit monotonic_buffer_resource(memory_resource* upstream);
monotonic_buffer_resource(size_t initial_size, memory_resource* upstream);
```

*Preconditions:* `upstream` is the address of a valid memory resource.
`initial_size`, if specified, is greater than zero.

*Effects:* Sets `upstream_rsrc` to `upstream` and `current_buffer` to
`nullptr`. If `initial_size` is specified, sets `next_buffer_size` to at
least `initial_size`; otherwise sets `next_buffer_size` to an
*implementation-defined* size.

``` cpp
monotonic_buffer_resource(void* buffer, size_t buffer_size, memory_resource* upstream);
```

*Preconditions:* `upstream` is the address of a valid memory resource.
`buffer_size` is no larger than the number of bytes in `buffer`.

*Effects:* Sets `upstream_rsrc` to `upstream`, `current_buffer` to
`buffer`, and `next_buffer_size` to `buffer_size` (but not less than 1),
then increases `next_buffer_size` by an *implementation-defined* growth
factor (which need not be integral).

``` cpp
~monotonic_buffer_resource();
```

*Effects:* Calls `release()`.

#### Members <a id="mem.res.monotonic.buffer.mem">[[mem.res.monotonic.buffer.mem]]</a>

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

*Returns:* A pointer to allocated
storage [[basic.stc.dynamic.allocation]] with a size of at least
`bytes`. The size and alignment of the allocated memory shall meet the
requirements for a class derived from
`memory_resource`[[mem.res.class]].

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

*Returns:* `this == &other`.

## Class template `scoped_allocator_adaptor` <a id="allocator.adaptor">[[allocator.adaptor]]</a>

### Header `<scoped_allocator>` synopsis <a id="allocator.adaptor.syn">[[allocator.adaptor.syn]]</a>

``` cpp
namespace std {
  // class template scoped allocator adaptor
  template<class OuterAlloc, class... InnerAlloc>
    class scoped_allocator_adaptor;

  // [scoped.adaptor.operators], scoped allocator operators
  template<class OuterA1, class OuterA2, class... InnerAllocs>
    bool operator==(const scoped_allocator_adaptor<OuterA1, InnerAllocs...>& a,
                    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& b) noexcept;
}
```

The class template `scoped_allocator_adaptor` is an allocator template
that specifies an allocator resource (the outer allocator) to be used by
a container (as any other allocator does) and also specifies an inner
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
  template<class OuterAlloc, class... InnerAllocs>
  class scoped_allocator_adaptor : public OuterAlloc {
  private:
    using OuterTraits = allocator_traits<OuterAlloc>;   // exposition only
    scoped_allocator_adaptor<InnerAllocs...> inner;     // exposition only

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

    template<class Tp> struct rebind {
      using other = scoped_allocator_adaptor<
        OuterTraits::template rebind_alloc<Tp>, InnerAllocs...>;
    };

    scoped_allocator_adaptor();
    template<class OuterA2>
      scoped_allocator_adaptor(OuterA2&& outerAlloc,
                               const InnerAllocs&... innerAllocs) noexcept;

    scoped_allocator_adaptor(const scoped_allocator_adaptor& other) noexcept;
    scoped_allocator_adaptor(scoped_allocator_adaptor&& other) noexcept;

    template<class OuterA2>
      scoped_allocator_adaptor(
        const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& other) noexcept;
    template<class OuterA2>
      scoped_allocator_adaptor(
        scoped_allocator_adaptor<OuterA2, InnerAllocs...>&& other) noexcept;

    scoped_allocator_adaptor& operator=(const scoped_allocator_adaptor&) = default;
    scoped_allocator_adaptor& operator=(scoped_allocator_adaptor&&) = default;

    ~scoped_allocator_adaptor();

    inner_allocator_type& inner_allocator() noexcept;
    const inner_allocator_type& inner_allocator() const noexcept;
    outer_allocator_type& outer_allocator() noexcept;
    const outer_allocator_type& outer_allocator() const noexcept;

    [[nodiscard]] pointer allocate(size_type n);
    [[nodiscard]] pointer allocate(size_type n, const_void_pointer hint);
    void deallocate(pointer p, size_type n);
    size_type max_size() const;

    template<class T, class... Args>
      void construct(T* p, Args&&... args);

    template<class T>
      void destroy(T* p);

    scoped_allocator_adaptor select_on_container_copy_construction() const;
  };

  template<class OuterAlloc, class... InnerAllocs>
    scoped_allocator_adaptor(OuterAlloc, InnerAllocs...)
      -> scoped_allocator_adaptor<OuterAlloc, InnerAllocs...>;
}
```

### Member types <a id="allocator.adaptor.types">[[allocator.adaptor.types]]</a>

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

### Constructors <a id="allocator.adaptor.cnstr">[[allocator.adaptor.cnstr]]</a>

``` cpp
scoped_allocator_adaptor();
```

*Effects:* Value-initializes the `OuterAlloc` base class and the `inner`
allocator object.

``` cpp
template<class OuterA2>
  scoped_allocator_adaptor(OuterA2&& outerAlloc, const InnerAllocs&... innerAllocs) noexcept;
```

*Constraints:* `is_constructible_v<OuterAlloc, OuterA2>` is `true`.

*Effects:* Initializes the `OuterAlloc` base class with
`std::forward<OuterA2>(outerAlloc)` and `inner` with `innerAllocs...`
(hence recursively initializing each allocator within the adaptor with
the corresponding allocator from the argument list).

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
template<class OuterA2>
  scoped_allocator_adaptor(
    const scoped_allocator_adaptor<OuterA2, InnerAllocs...>& other) noexcept;
```

*Constraints:* `is_constructible_v<OuterAlloc, const OuterA2&>` is
`true`.

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator from `other`.

``` cpp
template<class OuterA2>
  scoped_allocator_adaptor(scoped_allocator_adaptor<OuterA2, InnerAllocs...>&& other) noexcept;
```

*Constraints:* `is_constructible_v<OuterAlloc, OuterA2>` is `true`.

*Effects:* Initializes each allocator within the adaptor with the
corresponding allocator rvalue from `other`.

### Members <a id="allocator.adaptor.members">[[allocator.adaptor.members]]</a>

In the `construct` member functions, `OUTERMOST(x)` is
`OUTERMOST(x.outer_allocator())` if the expression `x.outer_allocator()`
is valid  [[temp.deduct]] and `x` otherwise; `OUTERMOST_ALLOC_TRAITS(x)`
is `allocator_traits<remove_reference_t<decltype(OUTERMOST(x))>>`.

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
[[nodiscard]] pointer allocate(size_type n);
```

*Returns:*
`allocator_traits<OuterAlloc>::allocate(outer_allocator(), n)`.

``` cpp
[[nodiscard]] pointer allocate(size_type n, const_void_pointer hint);
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
template<class T, class... Args>
  void construct(T* p, Args&&... args);
```

*Effects:* Equivalent to:

``` cpp
apply([p, this](auto&&... newargs) {
        OUTERMOST_ALLOC_TRAITS(*this)::construct(
          OUTERMOST(*this), p,
          std::forward<decltype(newargs)>(newargs)...);
      },
      uses_allocator_construction_args<T>(inner_allocator(),
                                          std::forward<Args>(args)...));
```

``` cpp
template<class T>
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

### Operators <a id="scoped.adaptor.operators">[[scoped.adaptor.operators]]</a>

``` cpp
template<class OuterA1, class OuterA2, class... InnerAllocs>
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

## Function objects <a id="function.objects">[[function.objects]]</a>

A *function object type* is an object type [[basic.types]] that can be
the type of the *postfix-expression* in a function call ([[expr.call]],
[[over.match.call]]).[^2] A *function object* is an object of a function
object type. In the places where one would expect to pass a pointer to a
function to an algorithmic template [[algorithms]], the interface is
specified to accept a function object. This not only makes algorithmic
templates work with pointers to functions, but also enables them to work
with arbitrary function objects.

### Header `<functional>` synopsis <a id="functional.syn">[[functional.syn]]</a>

``` cpp
namespace std {
  // [func.invoke], invoke
  template<class F, class... Args>
    constexpr invoke_result_t<F, Args...> invoke(F&& f, Args&&... args)
      noexcept(is_nothrow_invocable_v<F, Args...>);

  // [refwrap], reference_wrapper
  template<class T> class reference_wrapper;

  template<class T> constexpr reference_wrapper<T> ref(T&) noexcept;
  template<class T> constexpr reference_wrapper<const T> cref(const T&) noexcept;
  template<class T> void ref(const T&&) = delete;
  template<class T> void cref(const T&&) = delete;

  template<class T> constexpr reference_wrapper<T> ref(reference_wrapper<T>) noexcept;
  template<class T> constexpr reference_wrapper<const T> cref(reference_wrapper<T>) noexcept;

  // [arithmetic.operations], arithmetic operations
  template<class T = void> struct plus;
  template<class T = void> struct minus;
  template<class T = void> struct multiplies;
  template<class T = void> struct divides;
  template<class T = void> struct modulus;
  template<class T = void> struct negate;
  template<> struct plus<void>;
  template<> struct minus<void>;
  template<> struct multiplies<void>;
  template<> struct divides<void>;
  template<> struct modulus<void>;
  template<> struct negate<void>;

  // [comparisons], comparisons
  template<class T = void> struct equal_to;
  template<class T = void> struct not_equal_to;
  template<class T = void> struct greater;
  template<class T = void> struct less;
  template<class T = void> struct greater_equal;
  template<class T = void> struct less_equal;
  template<> struct equal_to<void>;
  template<> struct not_equal_to<void>;
  template<> struct greater<void>;
  template<> struct less<void>;
  template<> struct greater_equal<void>;
  template<> struct less_equal<void>;

  // [comparisons.three.way], class compare_three_way
  struct compare_three_way;

  // [logical.operations], logical operations
  template<class T = void> struct logical_and;
  template<class T = void> struct logical_or;
  template<class T = void> struct logical_not;
  template<> struct logical_and<void>;
  template<> struct logical_or<void>;
  template<> struct logical_not<void>;

  // [bitwise.operations], bitwise operations
  template<class T = void> struct bit_and;
  template<class T = void> struct bit_or;
  template<class T = void> struct bit_xor;
  template<class T = void> struct bit_not;
  template<> struct bit_and<void>;
  template<> struct bit_or<void>;
  template<> struct bit_xor<void>;
  template<> struct bit_not<void>;

  // [func.identity], identity
  struct identity;

  // [func.not.fn], function template not_fn
  template<class F> constexpr unspecified not_fn(F&& f);

  // [func.bind.front], function template bind_front
  template<class F, class... Args> constexpr unspecified bind_front(F&&, Args&&...);

  // [func.bind], bind
  template<class T> struct is_bind_expression;
  template<class T>
    inline constexpr bool is_bind_expression_v = is_bind_expression<T>::value;
  template<class T> struct is_placeholder;
  template<class T>
    inline constexpr int is_placeholder_v = is_placeholder<T>::value;

  template<class F, class... BoundArgs>
    constexpr unspecified bind(F&&, BoundArgs&&...);
  template<class R, class F, class... BoundArgs>
    constexpr unspecified bind(F&&, BoundArgs&&...);

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
    constexpr unspecified mem_fn(R T::*) noexcept;

  // [func.wrap], polymorphic function wrappers
  class bad_function_call;

  template<class> class function;       // not defined
  template<class R, class... ArgTypes> class function<R(ArgTypes...)>;

  template<class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&) noexcept;

  template<class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

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

  // [unord.hash], class template hash
  template<class T>
    struct hash;

  namespace ranges {
    // [range.cmp], concept-constrained comparisons
    struct equal_to;
    struct not_equal_to;
    struct greater;
    struct less;
    struct greater_equal;
    struct less_equal;
  }
}
```

[*Example 1*:

If a C++ program wants to have a by-element addition of two vectors `a`
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

A *callable type* is a function object type [[function.objects]] or a
pointer to member.

A *callable object* is an object of a callable type.

A *call wrapper type* is a type that holds a callable object and
supports a call operation that forwards to that object.

A *call wrapper* is an object of a call wrapper type.

A *target object* is the callable object held by a call wrapper.

A call wrapper type may additionally hold a sequence of objects and
references that may be passed as arguments to the target object. These
entities are collectively referred to as *bound argument entities*.

The target object and bound argument entities of the call wrapper are
collectively referred to as *state entities*.

### Requirements <a id="func.require">[[func.require]]</a>

Define `INVOKE(f, t₁, t₂, …, t_N)` as follows:

- `(t₁.*f)(t₂, …, t_N)` when `f` is a pointer to a member function of a
  class `T` and `is_base_of_v<T, remove_reference_t<decltype(t₁)>>` is
  `true`;
- `(t₁.get().*f)(t₂, …, t_N)` when `f` is a pointer to a member function
  of a class `T` and `remove_cvref_t<decltype(t₁)>` is a specialization
  of `reference_wrapper`;
- `((*t₁).*f)(t₂, …, t_N)` when `f` is a pointer to a member function of
  a class `T` and `t₁` does not satisfy the previous two items;
- `t₁.*f` when `N == 1` and `f` is a pointer to data member of a class
  `T` and `is_base_of_v<T, remove_reference_t<decltype(t₁)>>` is `true`;
- `t₁.get().*f` when `N == 1` and `f` is a pointer to data member of a
  class `T` and `remove_cvref_t<decltype(t₁)>` is a specialization of
  `reference_wrapper`;
- `(*t₁).*f` when `N == 1` and `f` is a pointer to data member of a
  class `T` and `t₁` does not satisfy the previous two items;
- `f(t₁, t₂, …, t_N)` in all other cases.

Define `INVOKE<R>(f, t₁, t₂, …, t_N)` as
`static_cast<void>(INVOKE(f, t₁, t₂, …, t_N))` if `R` is cv `void`,
otherwise `INVOKE(f, t₁, t₂, …, t_N)` implicitly converted to `R`.

Every call wrapper [[func.def]] meets the *Cpp17MoveConstructible* and
*Cpp17Destructible* requirements. An *argument forwarding call wrapper*
is a call wrapper that can be called with an arbitrary argument list and
delivers the arguments to the wrapped callable object as references.
This forwarding step delivers rvalue arguments as rvalue references and
lvalue arguments as lvalue references.

[*Note 1*:

In a typical implementation, argument forwarding call wrappers have an
overloaded function call operator of the form

``` cpp
template<class... UnBoundArgs>
  constexpr R operator()(UnBoundArgs&&... unbound_args) cv-qual;
```

— *end note*]

A *perfect forwarding call wrapper* is an argument forwarding call
wrapper that forwards its state entities to the underlying call
expression. This forwarding step delivers a state entity of type `T` as
cv `T&` when the call is performed on an lvalue of the call wrapper type
and as cv `T&&` otherwise, where cv represents the cv-qualifiers of the
call wrapper and where cv shall be neither `volatile` nor
`const volatile`.

A *call pattern* defines the semantics of invoking a perfect forwarding
call wrapper. A postfix call performed on a perfect forwarding call
wrapper is expression-equivalent [[defns.expression-equivalent]] to an
expression `e` determined from its call pattern `cp` by replacing all
occurrences of the arguments of the call wrapper and its state entities
with references as described in the corresponding forwarding steps.

A *simple call wrapper* is a perfect forwarding call wrapper that meets
the *Cpp17CopyConstructible* and *Cpp17CopyAssignable* requirements and
whose copy constructor, move constructor, and assignment operators are
constexpr functions that do not throw exceptions.

The copy/move constructor of an argument forwarding call wrapper has the
same apparent semantics as if memberwise copy/move of its state entities
were performed [[class.copy.ctor]].

[*Note 2*: This implies that each of the copy/move constructors has the
same exception-specification as the corresponding implicit definition
and is declared as `constexpr` if the corresponding implicit definition
would be considered to be constexpr. — *end note*]

Argument forwarding call wrappers returned by a given standard library
function template have the same type if the types of their corresponding
state entities are the same.

### Function template `invoke` <a id="func.invoke">[[func.invoke]]</a>

``` cpp
template<class F, class... Args>
  constexpr invoke_result_t<F, Args...> invoke(F&& f, Args&&... args)
    noexcept(is_nothrow_invocable_v<F, Args...>);
```

*Returns:* *INVOKE*(std::forward\<F\>(f),
std::forward\<Args\>(args)...) [[func.require]].

### Class template `reference_wrapper` <a id="refwrap">[[refwrap]]</a>

``` cpp
namespace std {
  template<class T> class reference_wrapper {
  public:
    // types
    using type = T;

    // construct/copy/destroy
    template<class U>
      constexpr reference_wrapper(U&&) noexcept(see below);
    constexpr reference_wrapper(const reference_wrapper& x) noexcept;

    // assignment
    constexpr reference_wrapper& operator=(const reference_wrapper& x) noexcept;

    // access
    constexpr operator T& () const noexcept;
    constexpr T& get() const noexcept;

    // invocation
    template<class... ArgTypes>
      constexpr invoke_result_t<T&, ArgTypes...> operator()(ArgTypes&&...) const;
  };
  template<class T>
    reference_wrapper(T&) -> reference_wrapper<T>;
}
```

`reference_wrapper<T>` is a *Cpp17CopyConstructible* and
*Cpp17CopyAssignable* wrapper around a reference to an object or
function of type `T`.

`reference_wrapper<T>` is a trivially copyable type [[basic.types]].

The template parameter `T` of `reference_wrapper` may be an incomplete
type.

#### Constructors and destructor <a id="refwrap.const">[[refwrap.const]]</a>

``` cpp
template<class U>
  constexpr reference_wrapper(U&& u) noexcept(see below);
```

Let *FUN* denote the exposition-only functions

``` cpp
void FUN(T&) noexcept;
void FUN(T&&) = delete;
```

*Constraints:* The expression *FUN*(declval\<U\>()) is well-formed and
`is_same_v<remove_cvref_t<U>, reference_wrapper>` is `false`.

*Effects:* Creates a variable `r` as if by `T& r = std::forward<U>(u)`,
then constructs a `reference_wrapper` object that stores a reference to
`r`.

*Remarks:* The expression inside `noexcept` is equivalent to
`noexcept(`*`FUN`*`(declval<U>()))`.

``` cpp
constexpr reference_wrapper(const reference_wrapper& x) noexcept;
```

*Effects:* Constructs a `reference_wrapper` object that stores a
reference to `x.get()`.

#### Assignment <a id="refwrap.assign">[[refwrap.assign]]</a>

``` cpp
constexpr reference_wrapper& operator=(const reference_wrapper& x) noexcept;
```

*Ensures:* `*this` stores a reference to `x.get()`.

#### Access <a id="refwrap.access">[[refwrap.access]]</a>

``` cpp
constexpr operator T& () const noexcept;
```

*Returns:* The stored reference.

``` cpp
constexpr T& get() const noexcept;
```

*Returns:* The stored reference.

#### Invocation <a id="refwrap.invoke">[[refwrap.invoke]]</a>

``` cpp
template<class... ArgTypes>
  constexpr invoke_result_t<T&, ArgTypes...>
    operator()(ArgTypes&&... args) const;
```

*Mandates:* `T` is a complete type.

*Returns:* *INVOKE*(get(),
std::forward\<ArgTypes\>(args)...). [[func.require]]

#### Helper functions <a id="refwrap.helpers">[[refwrap.helpers]]</a>

The template parameter `T` of the following `ref` and `cref` function
templates may be an incomplete type.

``` cpp
template<class T> constexpr reference_wrapper<T> ref(T& t) noexcept;
```

*Returns:* `reference_wrapper<T>(t)`.

``` cpp
template<class T> constexpr reference_wrapper<T> ref(reference_wrapper<T> t) noexcept;
```

*Returns:* `ref(t.get())`.

``` cpp
template<class T> constexpr reference_wrapper<const T> cref(const T& t) noexcept;
```

*Returns:* `reference_wrapper <const T>(t)`.

``` cpp
template<class T> constexpr reference_wrapper<const T> cref(reference_wrapper<T> t) noexcept;
```

*Returns:* `cref(t.get())`.

### Arithmetic operations <a id="arithmetic.operations">[[arithmetic.operations]]</a>

The library provides basic function object classes for all of the
arithmetic operators in the language ([[expr.mul]], [[expr.add]]).

#### Class template `plus` <a id="arithmetic.operations.plus">[[arithmetic.operations.plus]]</a>

``` cpp
template<class T = void> struct plus {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x + y`.

``` cpp
template<> struct plus<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) + std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) + std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) + std::forward<U>(u)`.

#### Class template `minus` <a id="arithmetic.operations.minus">[[arithmetic.operations.minus]]</a>

``` cpp
template<class T = void> struct minus {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x - y`.

``` cpp
template<> struct minus<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) - std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) - std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) - std::forward<U>(u)`.

#### Class template `multiplies` <a id="arithmetic.operations.multiplies">[[arithmetic.operations.multiplies]]</a>

``` cpp
template<class T = void> struct multiplies {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x * y`.

``` cpp
template<> struct multiplies<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) * std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) * std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) * std::forward<U>(u)`.

#### Class template `divides` <a id="arithmetic.operations.divides">[[arithmetic.operations.divides]]</a>

``` cpp
template<class T = void> struct divides {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x / y`.

``` cpp
template<> struct divides<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) / std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) / std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) / std::forward<U>(u)`.

#### Class template `modulus` <a id="arithmetic.operations.modulus">[[arithmetic.operations.modulus]]</a>

``` cpp
template<class T = void> struct modulus {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x % y`.

``` cpp
template<> struct modulus<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) % std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) % std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) % std::forward<U>(u)`.

#### Class template `negate` <a id="arithmetic.operations.negate">[[arithmetic.operations.negate]]</a>

``` cpp
template<class T = void> struct negate {
  constexpr T operator()(const T& x) const;
};
```

``` cpp
constexpr T operator()(const T& x) const;
```

*Returns:* `-x`.

``` cpp
template<> struct negate<void> {
  template<class T> constexpr auto operator()(T&& t) const
    -> decltype(-std::forward<T>(t));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T> constexpr auto operator()(T&& t) const
    -> decltype(-std::forward<T>(t));
```

*Returns:* `-std::forward<T>(t)`.

### Comparisons <a id="comparisons">[[comparisons]]</a>

The library provides basic function object classes for all of the
comparison operators in the language ([[expr.rel]], [[expr.eq]]).

For templates `less`, `greater`, `less_equal`, and `greater_equal`, the
specializations for any pointer type yield a result consistent with the
implementation-defined strict total order over pointers
[[defns.order.ptr]].

[*Note 1*: If `a < b` is well-defined for pointers `a` and `b` of type
`P`, then `(a < b) == less<P>()(a, b)`, `(a > b) == greater<P>()(a, b)`,
and so forth. — *end note*]

For template specializations `less<void>`, `greater<void>`,
`less_equal<void>`, and `greater_equal<void>`, if the call operator
calls a built-in operator comparing pointers, the call operator yields a
result consistent with the implementation-defined strict total order
over pointers.

#### Class template `equal_to` <a id="comparisons.equal.to">[[comparisons.equal.to]]</a>

``` cpp
template<class T = void> struct equal_to {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x == y`.

``` cpp
template<> struct equal_to<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) == std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) == std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) == std::forward<U>(u)`.

#### Class template `not_equal_to` <a id="comparisons.not.equal.to">[[comparisons.not.equal.to]]</a>

``` cpp
template<class T = void> struct not_equal_to {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x != y`.

``` cpp
template<> struct not_equal_to<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) != std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) != std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) != std::forward<U>(u)`.

#### Class template `greater` <a id="comparisons.greater">[[comparisons.greater]]</a>

``` cpp
template<class T = void> struct greater {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x > y`.

``` cpp
template<> struct greater<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) > std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) > std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) > std::forward<U>(u)`.

#### Class template `less` <a id="comparisons.less">[[comparisons.less]]</a>

``` cpp
template<class T = void> struct less {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x < y`.

``` cpp
template<> struct less<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) < std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) < std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) < std::forward<U>(u)`.

#### Class template `greater_equal` <a id="comparisons.greater.equal">[[comparisons.greater.equal]]</a>

``` cpp
template<class T = void> struct greater_equal {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x >= y`.

``` cpp
template<> struct greater_equal<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) >= std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) >= std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) >= std::forward<U>(u)`.

#### Class template `less_equal` <a id="comparisons.less.equal">[[comparisons.less.equal]]</a>

``` cpp
template<class T = void> struct less_equal {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x <= y`.

``` cpp
template<> struct less_equal<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) <= std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) <= std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) <= std::forward<U>(u)`.

#### Class `compare_three_way` <a id="comparisons.three.way">[[comparisons.three.way]]</a>

In this subclause, `BUILTIN-PTR-THREE-WAY(T, U)` for types `T` and `U`
is a boolean constant expression. `BUILTIN-PTR-THREE-WAY(T, U)` is
`true` if and only if `<=>` in the expression

``` cpp
declval<T>() <=> declval<U>()
```

resolves to a built-in operator comparing pointers.

``` cpp
struct compare_three_way {
  template<class T, class U>
    requires three_way_comparable_with<T, U> || BUILTIN-PTR-THREE-WAY(T, U)
  constexpr auto operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  requires three_way_comparable_with<T, U> || BUILTIN-PTR-THREE-WAY(T, U)
constexpr auto operator()(T&& t, U&& u) const;
```

*Preconditions:* If the expression
`std::forward<T>(t) <=> std::forward<U>(u)` results in a call to a
built-in operator `<=>` comparing pointers of type `P`, the conversion
sequences from both `T` and `U` to `P` are
equality-preserving [[concepts.equality]].

*Effects:*

- If the expression `std::forward<T>(t) <=> std::forward<U>(u)` results
  in a call to a built-in operator `<=>` comparing pointers of type `P`,
  returns `strong_ordering::less` if (the converted value of) `t`
  precedes `u` in the implementation-defined strict total order over
  pointers [[defns.order.ptr]], `strong_ordering::greater` if `u`
  precedes `t`, and otherwise `strong_ordering::equal`.
- Otherwise, equivalent to:
  `return std::forward<T>(t) <=> std::forward<U>(u);`

### Concept-constrained comparisons <a id="range.cmp">[[range.cmp]]</a>

In this subclause, `BUILTIN-PTR-CMP(T, op, U)` for types `T` and `U` and
where op is an equality [[expr.eq]] or relational operator [[expr.rel]]
is a boolean constant expression. `BUILTIN-PTR-CMP(T, op, U)` is `true`
if and only if op in the expression `declval<T>() op declval<U>()`
resolves to a built-in operator comparing pointers.

``` cpp
struct ranges::equal_to {
  template<class T, class U>
    requires equality_comparable_with<T, U> || BUILTIN-PTR-CMP(T, ==, U)
  constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

*Preconditions:* If the expression
`std::forward<T>(t) == std::forward<U>(u)` results in a call to a
built-in operator `==` comparing pointers of type `P`, the conversion
sequences from both `T` and `U` to `P` are
equality-preserving [[concepts.equality]].

*Effects:*

- If the expression `std::forward<T>(t) == std::forward<U>(u)` results
  in a call to a built-in operator `==` comparing pointers: returns
  `false` if either (the converted value of) `t` precedes `u` or `u`
  precedes `t` in the implementation-defined strict total order over
  pointers [[defns.order.ptr]] and otherwise `true`.
- Otherwise, equivalent to:
  `return std::forward<T>(t) == std::forward<U>(u);`

``` cpp
struct ranges::not_equal_to {
  template<class T, class U>
    requires equality_comparable_with<T, U> || BUILTIN-PTR-CMP(T, ==, U)
  constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

`operator()` has effects equivalent to:

``` cpp
return !ranges::equal_to{}(std::forward<T>(t), std::forward<U>(u));
```

``` cpp
struct ranges::greater {
  template<class T, class U>
    requires totally_ordered_with<T, U> || BUILTIN-PTR-CMP(U, <, T)
  constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

`operator()` has effects equivalent to:

``` cpp
return ranges::less{}(std::forward<U>(u), std::forward<T>(t));
```

``` cpp
struct ranges::less {
  template<class T, class U>
    requires totally_ordered_with<T, U> || BUILTIN-PTR-CMP(T, <, U)
  constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

*Preconditions:* If the expression
`std::forward<T>(t) < std::forward<U>(u)` results in a call to a
built-in operator `<` comparing pointers of type `P`, the conversion
sequences from both `T` and `U` to `P` are
equality-preserving [[concepts.equality]]. For any expressions `ET` and
`EU` such that `decltype((ET))` is `T` and `decltype((EU))` is `U`,
exactly one of `ranges::less{}(ET, EU)`, `ranges::less{}(EU, ET)`, or
`ranges::equal_to{}(ET, EU)` is `true`.

*Effects:*

- If the expression `std::forward<T>(t) < std::forward<U>(u)` results in
  a call to a built-in operator `<` comparing pointers: returns `true`
  if (the converted value of) `t` precedes `u` in the
  implementation-defined strict total order over
  pointers [[defns.order.ptr]] and otherwise `false`.
- Otherwise, equivalent to:
  `return std::forward<T>(t) < std::forward<U>(u);`

``` cpp
struct ranges::greater_equal {
  template<class T, class U>
    requires totally_ordered_with<T, U> || BUILTIN-PTR-CMP(T, <, U)
  constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

`operator()` has effects equivalent to:

``` cpp
return !ranges::less{}(std::forward<T>(t), std::forward<U>(u));
```

``` cpp
struct ranges::less_equal {
  template<class T, class U>
    requires totally_ordered_with<T, U> || BUILTIN-PTR-CMP(U, <, T)
  constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

`operator()` has effects equivalent to:

``` cpp
return !ranges::less{}(std::forward<U>(u), std::forward<T>(t));
```

### Logical operations <a id="logical.operations">[[logical.operations]]</a>

The library provides basic function object classes for all of the
logical operators in the language ([[expr.log.and]], [[expr.log.or]],
[[expr.unary.op]]).

#### Class template `logical_and` <a id="logical.operations.and">[[logical.operations.and]]</a>

``` cpp
template<class T = void> struct logical_and {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x && y`.

``` cpp
template<> struct logical_and<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) && std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) && std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) && std::forward<U>(u)`.

#### Class template `logical_or` <a id="logical.operations.or">[[logical.operations.or]]</a>

``` cpp
template<class T = void> struct logical_or {
  constexpr bool operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr bool operator()(const T& x, const T& y) const;
```

*Returns:* `x || y`.

``` cpp
template<> struct logical_or<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) || std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) || std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) || std::forward<U>(u)`.

#### Class template `logical_not` <a id="logical.operations.not">[[logical.operations.not]]</a>

``` cpp
template<class T = void> struct logical_not {
  constexpr bool operator()(const T& x) const;
};
```

``` cpp
constexpr bool operator()(const T& x) const;
```

*Returns:* `!x`.

``` cpp
template<> struct logical_not<void> {
  template<class T> constexpr auto operator()(T&& t) const
    -> decltype(!std::forward<T>(t));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T> constexpr auto operator()(T&& t) const
    -> decltype(!std::forward<T>(t));
```

*Returns:* `!std::forward<T>(t)`.

### Bitwise operations <a id="bitwise.operations">[[bitwise.operations]]</a>

The library provides basic function object classes for all of the
bitwise operators in the language ([[expr.bit.and]], [[expr.or]],
[[expr.xor]], [[expr.unary.op]]).

#### Class template `bit_and` <a id="bitwise.operations.and">[[bitwise.operations.and]]</a>

``` cpp
template<class T = void> struct bit_and {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x & y`.

``` cpp
template<> struct bit_and<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) & std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) & std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) & std::forward<U>(u)`.

#### Class template `bit_or` <a id="bitwise.operations.or">[[bitwise.operations.or]]</a>

``` cpp
template<class T = void> struct bit_or {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x | y`.

``` cpp
template<> struct bit_or<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) | std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) | std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) | std::forward<U>(u)`.

#### Class template `bit_xor` <a id="bitwise.operations.xor">[[bitwise.operations.xor]]</a>

``` cpp
template<class T = void> struct bit_xor {
  constexpr T operator()(const T& x, const T& y) const;
};
```

``` cpp
constexpr T operator()(const T& x, const T& y) const;
```

*Returns:* `x ^ y`.

``` cpp
template<> struct bit_xor<void> {
  template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) ^ std::forward<U>(u));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U> constexpr auto operator()(T&& t, U&& u) const
    -> decltype(std::forward<T>(t) ^ std::forward<U>(u));
```

*Returns:* `std::forward<T>(t) ^ std::forward<U>(u)`.

#### Class template `bit_not` <a id="bitwise.operations.not">[[bitwise.operations.not]]</a>

``` cpp
template<class T = void> struct bit_not {
  constexpr T operator()(const T& x) const;
};
```

``` cpp
constexpr T operator()(const T& x) const;
```

*Returns:* `~x`.

``` cpp
template<> struct bit_not<void> {
  template<class T> constexpr auto operator()(T&& t) const
    -> decltype(~std::forward<T>(t));

  using is_transparent = unspecified;
};
```

``` cpp
template<class T> constexpr auto operator()(T&&) const
    -> decltype(~std::forward<T>(t));
```

*Returns:* `~std::forward<T>(t)`.

### Class `identity` <a id="func.identity">[[func.identity]]</a>

``` cpp
struct identity {
  template<class T>
    constexpr T&& operator()(T&& t) const noexcept;

  using is_transparent = unspecified;
};

template<class T>
  constexpr T&& operator()(T&& t) const noexcept;
```

*Effects:* Equivalent to: `return std::forward<T>(t);`

### Function template `not_fn` <a id="func.not.fn">[[func.not.fn]]</a>

``` cpp
template<class F> constexpr unspecified not_fn(F&& f);
```

In the text that follows:

- `g` is a value of the result of a `not_fn` invocation,
- `FD` is the type `decay_t<F>`,
- `fd` is the target object of `g`[[func.def]] of type `FD`,
  direct-non-list-initialized with `std::forward<F>(f)`,
- `call_args` is an argument pack used in a function call
  expression [[expr.call]] of `g`.

*Mandates:* `is_constructible_v<FD, F> && is_move_constructible_v<FD>`
is `true`.

*Preconditions:* `FD` meets the *Cpp17MoveConstructible* requirements.

*Returns:* A perfect forwarding call wrapper `g` with call pattern
`!invoke(fd, call_args...)`.

*Throws:* Any exception thrown by the initialization of `fd`.

### Function template `bind_front` <a id="func.bind.front">[[func.bind.front]]</a>

``` cpp
template<class F, class... Args>
  constexpr unspecified bind_front(F&& f, Args&&... args);
```

In the text that follows:

- `g` is a value of the result of a `bind_front` invocation,
- `FD` is the type `decay_t<F>`,
- `fd` is the target object of `g`[[func.def]] of type `FD`,
  direct-non-list-initialized with `std::forward<F>(f)`,
- `BoundArgs` is a pack that denotes `decay_t<Args>...`,
- `bound_args` is a pack of bound argument entities of `g`[[func.def]]
  of types `BoundArgs...`, direct-non-list-initialized with
  `std::forward<Args>(args)...`, respectively, and
- `call_args` is an argument pack used in a function call
  expression [[expr.call]] of `g`.

*Mandates:*

``` cpp
is_constructible_v<FD, F> &&
is_move_constructible_v<FD> &&
(is_constructible_v<BoundArgs, Args> && ...) &&
(is_move_constructible_v<BoundArgs> && ...)
```

is `true`.

*Preconditions:* `FD` meets the *Cpp17MoveConstructible* requirements.
For each `Tᵢ` in `BoundArgs`, if `Tᵢ` is an object type, `Tᵢ` meets the
*Cpp17MoveConstructible* requirements.

*Returns:* A perfect forwarding call wrapper `g` with call pattern
`invoke(fd, bound_args..., call_args...)`.

*Throws:* Any exception thrown by the initialization of the state
entities of `g`[[func.def]].

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

Specializations of the `is_bind_expression` template shall meet the
*Cpp17UnaryTypeTrait* requirements [[meta.rqmts]]. The implementation
provides a definition that has a base characteristic of `true_type` if
`T` is a type returned from `bind`, otherwise it has a base
characteristic of `false_type`. A program may specialize this template
for a program-defined type `T` to have a base characteristic of
`true_type` to indicate that `T` should be treated as a subexpression in
a `bind` call.

#### Class template `is_placeholder` <a id="func.bind.isplace">[[func.bind.isplace]]</a>

``` cpp
namespace std {
  template<class T> struct is_placeholder;      // see below
}
```

The class template `is_placeholder` can be used to detect the standard
placeholders `_1`, `_2`, and so on. The function template `bind` uses
`is_placeholder` to detect placeholders.

Specializations of the `is_placeholder` template shall meet the
*Cpp17UnaryTypeTrait* requirements [[meta.rqmts]]. The implementation
provides a definition that has the base characteristic of
`integral_constant<int, J>` if `T` is the type of
`std::placeholders::_J`, otherwise it has a base characteristic of
`integral_constant<int, 0>`. A program may specialize this template for
a program-defined type `T` to have a base characteristic of
`integral_constant<int, N>` with `N > 0` to indicate that `T` should be
treated as a placeholder type.

#### Function template `bind` <a id="func.bind.bind">[[func.bind.bind]]</a>

In the text that follows:

- `g` is a value of the result of a `bind` invocation,
- `FD` is the type `decay_t<F>`,
- `fd` is an lvalue that is a target object of `g` [[func.def]] of type
  `FD` direct-non-list-initialized with `std::forward<F>(f)`,
- `Tᵢ` is the iᵗʰ type in the template parameter pack `BoundArgs`,
- `TDᵢ` is the type `decay_t<Tᵢ>`,
- `tᵢ` is the iᵗʰ argument in the function parameter pack `bound_args`,
- `tdᵢ` is a bound argument entity of `g` [[func.def]] of type `TDᵢ`
  direct-non-list-initialized with `std::forward<{}Tᵢ>(tᵢ)`,
- `Uⱼ` is the jᵗʰ deduced type of the `UnBoundArgs&&...` parameter of
  the argument forwarding call wrapper, and
- `uⱼ` is the jᵗʰ argument associated with `Uⱼ`.

``` cpp
template<class F, class... BoundArgs>
  constexpr unspecified bind(F&& f, BoundArgs&&... bound_args);
template<class R, class F, class... BoundArgs>
  constexpr unspecified bind(F&& f, BoundArgs&&... bound_args);
```

*Mandates:* `is_constructible_v<FD, F>` is `true`. For each `Tᵢ` in
`BoundArgs`, `is_constructible_v<``TDᵢ``, ``Tᵢ``>` is `true`.

*Preconditions:* `FD` and each `TDᵢ` meet the *Cpp17MoveConstructible*
and *Cpp17Destructible* requirements. *INVOKE*(fd, w₁, w₂, …,
$w_N$) [[func.require]] is a valid expression for some values `w₁`,
`w₂`, …, `w_N`, where N has the value `sizeof...(bound_args)`.

*Returns:* An argument forwarding call wrapper `g`[[func.require]]. A
program that attempts to invoke a volatile-qualified `g` is ill-formed.
When `g` is not volatile-qualified, invocation of
`g(``u₁``, ``u₂``, `…`, ``u_M``)` is
expression-equivalent [[defns.expression-equivalent]] to

``` cpp
INVOKE(static_cast<$V_fd$>($v_fd$),
       static_cast<$V_1$>($v_1$), static_cast<$V_2$>($v_2$), …, static_cast<$V_N$>($v_N$))
```

for the first overload, and

``` cpp
INVOKE<R>(static_cast<$V_fd$>($v_fd$),
          static_cast<$V_1$>($v_1$), static_cast<$V_2$>($v_2$), …, static_cast<$V_N$>($v_N$))
```

for the second overload, where the values and types of the target
argument `v`_`fd` and of the bound arguments `v₁`, `v₂`, …, `v_N` are
determined as specified below.

*Throws:* Any exception thrown by the initialization of the state
entities of `g`.

[*Note 1*: If all of `FD` and `TDᵢ` meet the requirements of
*Cpp17CopyConstructible*, then the return type meets the requirements of
*Cpp17CopyConstructible*. — *end note*]

The values of the *bound arguments* `v₁`, `v₂`, …, `v_N` and their
corresponding types `V₁`, `V₂`, …, `V_N` depend on the types `TDᵢ`
derived from the call to `bind` and the cv-qualifiers cv of the call
wrapper `g` as follows:

- if `TDᵢ` is `reference_wrapper<T>`, the argument is `tdᵢ.get()` and
  its type `Vᵢ` is `T&`;
- if the value of `is_bind_expression_v<TDᵢ>` is `true`, the argument is
  ``` cpp
  static_cast<cv `TD`_i&>(td_i)(std::forward<U_j>(u_j)...)
  ```

  and its type `Vᵢ` is `invoke_result_t<cv TDᵢ&, Uⱼ...>&&`;
- if the value `j` of `is_placeholder_v<TDᵢ>` is not zero, the argument
  is `std::forward<Uⱼ>(uⱼ)` and its type `Vᵢ` is `Uⱼ&&`;
- otherwise, the value is `tdᵢ` and its type `Vᵢ` is `cv TDᵢ&`.

The value of the target argument `v`_`fd` is `fd` and its corresponding
type `V`_`fd` is `cv FD&`.

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

All placeholder types meet the *Cpp17DefaultConstructible* and
*Cpp17CopyConstructible* requirements, and their default constructors
and copy/move constructors are constexpr functions that do not throw
exceptions. It is *implementation-defined* whether placeholder types
meet the *Cpp17CopyAssignable* requirements, but if so, their copy
assignment operators are constexpr functions that do not throw
exceptions.

Placeholders should be defined as:

``` cpp
inline constexpr unspecified _1{};
```

If they are not, they are declared as:

``` cpp
extern unspecified _1;
```

### Function template `mem_fn` <a id="func.memfn">[[func.memfn]]</a>

``` cpp
template<class R, class T> constexpr unspecified mem_fn(R T::* pm) noexcept;
```

*Returns:* A simple call wrapper [[func.def]] `fn` with call pattern
`invoke(pmd, call_args...)`, where `pmd` is the target object of `fn` of
type `R T::*` direct-non-list-initialized with `pm`, and `call_args` is
an argument pack used in a function call expression [[expr.call]] of
`pm`.

### Polymorphic function wrappers <a id="func.wrap">[[func.wrap]]</a>

This subclause describes a polymorphic wrapper class that encapsulates
arbitrary callable objects.

#### Class `bad_function_call` <a id="func.wrap.badcall">[[func.wrap.badcall]]</a>

An exception of type `bad_function_call` is thrown by
`function::operator()` [[func.wrap.func.inv]] when the function wrapper
object has no target.

``` cpp
namespace std {
  class bad_function_call : public exception {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

#### Class template `function` <a id="func.wrap.func">[[func.wrap.func]]</a>

``` cpp
namespace std {
  template<class> class function;       // not defined

  template<class R, class... ArgTypes>
  class function<R(ArgTypes...)> {
  public:
    using result_type = R;

    // [func.wrap.func.con], construct/copy/destroy
    function() noexcept;
    function(nullptr_t) noexcept;
    function(const function&);
    function(function&&) noexcept;
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

  // [func.wrap.func.nullptr], null pointer comparison functions
  template<class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

  // [func.wrap.func.alg], specialized algorithms
  template<class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&) noexcept;
}
```

The `function` class template provides polymorphic wrappers that
generalize the notion of a function pointer. Wrappers can store, copy,
and call arbitrary callable objects [[func.def]], given a call signature
[[func.def]], allowing functions to be first-class objects.

A callable type [[func.def]] `F` is *Lvalue-Callable* for argument types
`ArgTypes` and return type `R` if the expression
`INVOKE<R>(declval<F&>(), declval<ArgTypes>()...)`, considered as an
unevaluated operand [[expr.prop]], is well-formed [[func.require]].

The `function` class template is a call wrapper [[func.def]] whose call
signature [[func.def]] is `R(ArgTypes...)`.

[*Note 1*: The types deduced by the deduction guides for `function` may
change in future versions of this International Standard. — *end note*]

##### Constructors and destructor <a id="func.wrap.func.con">[[func.wrap.func.con]]</a>

``` cpp
function() noexcept;
```

*Ensures:* `!*this`.

``` cpp
function(nullptr_t) noexcept;
```

*Ensures:* `!*this`.

``` cpp
function(const function& f);
```

*Ensures:* `!*this` if `!f`; otherwise, `*this` targets a copy of
`f.target()`.

*Throws:* Nothing if `f`’s target is a specialization of
`reference_wrapper` or a function pointer. Otherwise, may throw
`bad_alloc` or any exception thrown by the copy constructor of the
stored callable object.

[*Note 1*: Implementations should avoid the use of dynamically
allocated memory for small callable objects, for example, where `f`’s
target is an object holding only a pointer or reference to an object and
a member function pointer. — *end note*]

``` cpp
function(function&& f) noexcept;
```

*Ensures:* If `!f`, `*this` has no target; otherwise, the target of
`*this` is equivalent to the target of `f` before the construction, and
`f` is in a valid state with an unspecified value.

[*Note 2*: Implementations should avoid the use of dynamically
allocated memory for small callable objects, for example, where `f`’s
target is an object holding only a pointer or reference to an object and
a member function pointer. — *end note*]

``` cpp
template<class F> function(F f);
```

*Constraints:* `F` is Lvalue-Callable [[func.wrap.func]] for argument
types `ArgTypes...` and return type `R`.

*Preconditions:* `F` meets the *Cpp17CopyConstructible* requirements.

*Ensures:* `!*this` if any of the following hold:

- `f` is a null function pointer value.
- `f` is a null member pointer value.
- `F` is an instance of the `function` class template, and `!f`.

Otherwise, `*this` targets a copy of `f` initialized with
`std::move(f)`.

[*Note 3*: Implementations should avoid the use of dynamically
allocated memory for small callable objects, for example, where `f` is
an object holding only a pointer or reference to an object and a member
function pointer. — *end note*]

*Throws:* Nothing if `f` is a specialization of `reference_wrapper` or a
function pointer. Otherwise, may throw `bad_alloc` or any exception
thrown by `F`’s copy or move constructor.

``` cpp
template<class F> function(F) -> function<see below>;
```

*Constraints:* `&F::operator()` is well-formed when treated as an
unevaluated operand and `decltype(&F::operator())` is of the form
`R(G::*)(A...)` cv \\ₒₚₜ ` `noexceptₒₚₜ  for a class type `G`.

*Remarks:* The deduced type is `function<R(A...)>`.

[*Example 1*:

``` cpp
void f() {
  int i{5};
  function g = [&](double) { return i; };       // deduces function<int(double)>
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

*Ensures:* `!(*this)`.

*Returns:* `*this`.

``` cpp
template<class F> function& operator=(F&& f);
```

*Constraints:* `decay_t<F>` is Lvalue-Callable [[func.wrap.func]] for
argument types `ArgTypes...` and return type `R`.

*Effects:* As if by: `function(std::forward<F>(f)).swap(*this);`

*Returns:* `*this`.

``` cpp
template<class F> function& operator=(reference_wrapper<F> f) noexcept;
```

*Effects:* As if by: `function(f).swap(*this);`

*Returns:* `*this`.

``` cpp
~function();
```

*Effects:* If `*this != nullptr`, destroys the target of `this`.

##### Modifiers <a id="func.wrap.func.mod">[[func.wrap.func.mod]]</a>

``` cpp
void swap(function& other) noexcept;
```

*Effects:* Interchanges the targets of `*this` and `other`.

##### Capacity <a id="func.wrap.func.cap">[[func.wrap.func.cap]]</a>

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `true` if `*this` has a target, otherwise `false`.

##### Invocation <a id="func.wrap.func.inv">[[func.wrap.func.inv]]</a>

``` cpp
R operator()(ArgTypes... args) const;
```

*Returns:* *INVOKE*\<R\>(f,
std::forward\<ArgTypes\>(args)...) [[func.require]], where `f` is the
target object [[func.def]] of `*this`.

*Throws:* `bad_function_call` if `!*this`; otherwise, any exception
thrown by the wrapped callable object.

##### Target access <a id="func.wrap.func.targ">[[func.wrap.func.targ]]</a>

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

##### Null pointer comparison functions <a id="func.wrap.func.nullptr">[[func.wrap.func.nullptr]]</a>

``` cpp
template<class R, class... ArgTypes>
  bool operator==(const function<R(ArgTypes...)>& f, nullptr_t) noexcept;
```

*Returns:* `!f`.

##### Specialized algorithms <a id="func.wrap.func.alg">[[func.wrap.func.alg]]</a>

``` cpp
template<class R, class... ArgTypes>
  void swap(function<R(ArgTypes...)>& f1, function<R(ArgTypes...)>& f2) noexcept;
```

*Effects:* As if by: `f1.swap(f2);`

### Searchers <a id="func.search">[[func.search]]</a>

This subclause provides function object types [[function.objects]] for
operations that search for a sequence \[`pat``first`, `pat_last`) in
another sequence \[`first`, `last`) that is provided to the object’s
function call operator. The first sequence (the pattern to be searched
for) is provided to the object’s constructor, and the second (the
sequence to be searched) is provided to the function call operator.

Each specialization of a class template specified in this subclause
[[func.search]] shall meet the *Cpp17CopyConstructible* and
*Cpp17CopyAssignable* requirements. Template parameters named

- `ForwardIterator`,
- `ForwardIterator1`,
- `ForwardIterator2`,
- `RandomAccessIterator`,
- `RandomAccessIterator1`,
- `RandomAccessIterator2`, and
- `BinaryPredicate`

of templates specified in this subclause [[func.search]] shall meet the
same requirements and semantics as specified in [[algorithms.general]].
Template parameters named `Hash` shall meet the *Cpp17Hash* requirements
([[cpp17.hash]]).

The Boyer-Moore searcher implements the Boyer-Moore search algorithm.
The Boyer-Moore-Horspool searcher implements the Boyer-Moore-Horspool
search algorithm. In general, the Boyer-Moore searcher will use more
memory and give better runtime performance than Boyer-Moore-Horspool.

#### Class template `default_searcher` <a id="func.search.default">[[func.search.default]]</a>

``` cpp
template<class ForwardIterator1, class BinaryPredicate = equal_to<>>
  class default_searcher {
  public:
    constexpr default_searcher(ForwardIterator1 pat_first, ForwardIterator1 pat_last,
                               BinaryPredicate pred = BinaryPredicate());

    template<class ForwardIterator2>
      constexpr pair<ForwardIterator2, ForwardIterator2>
        operator()(ForwardIterator2 first, ForwardIterator2 last) const;

  private:
    ForwardIterator1 pat_first_;        // exposition only
    ForwardIterator1 pat_last_;         // exposition only
    BinaryPredicate pred_;              // exposition only
  };
```

``` cpp
constexpr default_searcher(ForwardIterator pat_first, ForwardIterator pat_last,
                           BinaryPredicate pred = BinaryPredicate());
```

*Effects:* Constructs a `default_searcher` object, initializing
`pat_first_` with `pat_first`, \texttt{pat_last\_} with `pat_last`, and
`pred_` with `pred`.

*Throws:* Any exception thrown by the copy constructor of
`BinaryPredicate` or `ForwardIterator1`.

``` cpp
template<class ForwardIterator2>
  constexpr pair<ForwardIterator2, ForwardIterator2>
    operator()(ForwardIterator2 first, ForwardIterator2 last) const;
```

*Effects:* Returns a pair of iterators `i` and `j` such that

- `i == search(first, last, pat_first_, pat_last_, pred_)`, and
- if `i == last`, then `j == last`, otherwise
  `j == next(i, distance(pat_first_, pat_last_))`.

#### Class template `boyer_moore_searcher` <a id="func.search.bm">[[func.search.bm]]</a>

``` cpp
template<class RandomAccessIterator1,
         class Hash = hash<typename iterator_traits<RandomAccessIterator1>::value_type>,
         class BinaryPredicate = equal_to<>>
  class boyer_moore_searcher {
  public:
    boyer_moore_searcher(RandomAccessIterator1 pat_first,
                         RandomAccessIterator1 pat_last,
                         Hash hf = Hash(),
                         BinaryPredicate pred = BinaryPredicate());

    template<class RandomAccessIterator2>
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

*Preconditions:* The value type of `RandomAccessIterator1` meets the
*Cpp17DefaultConstructible* requirements, the *Cpp17CopyConstructible*
requirements, and the *Cpp17CopyAssignable* requirements.

*Preconditions:* Let `V` be
`iterator_traits<RandomAccessIterator1>::value_type`. For any two values
`A` and `B` of type `V`, if `pred(A, B) == true`, then `hf(A) == hf(B)`
is `true`.

*Effects:* Initializes `pat_first_` with `pat_first`, `pat_last_` with
`pat_last`, `hash_` with `hf`, and `pred_` with `pred`.

*Throws:* Any exception thrown by the copy constructor of
`RandomAccessIterator1`, or by the default constructor, copy
constructor, or the copy assignment operator of the value type of
`RandomAccessIterator1`, or the copy constructor or `operator()` of
`BinaryPredicate` or `Hash`. May throw `bad_alloc` if additional memory
needed for internal data structures cannot be allocated.

``` cpp
template<class RandomAccessIterator2>
  pair<RandomAccessIterator2, RandomAccessIterator2>
    operator()(RandomAccessIterator2 first, RandomAccessIterator2 last) const;
```

*Mandates:* `RandomAccessIterator1` and `RandomAccessIterator2` have the
same value type.

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
template<class RandomAccessIterator1,
         class Hash = hash<typename iterator_traits<RandomAccessIterator1>::value_type>,
         class BinaryPredicate = equal_to<>>
  class boyer_moore_horspool_searcher {
  public:
    boyer_moore_horspool_searcher(RandomAccessIterator1 pat_first,
                                  RandomAccessIterator1 pat_last,
                                  Hash hf = Hash(),
                                  BinaryPredicate pred = BinaryPredicate());

    template<class RandomAccessIterator2>
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

*Preconditions:* The value type of `RandomAccessIterator1` meets the
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*, and
*Cpp17CopyAssignable* requirements.

*Preconditions:* Let `V` be
`iterator_traits<RandomAccessIterator1>::value_type`. For any two values
`A` and `B` of type `V`, if `pred(A, B) == true`, then `hf(A) == hf(B)`
is `true`.

*Effects:* Initializes `pat_first_` with `pat_first`, `pat_last_` with
`pat_last`, `hash_` with `hf`, and `pred_` with `pred`.

*Throws:* Any exception thrown by the copy constructor of
`RandomAccessIterator1`, or by the default constructor, copy
constructor, or the copy assignment operator of the value type of
`RandomAccessIterator1` or the copy constructor or `operator()` of
`BinaryPredicate` or `Hash`. May throw `bad_alloc` if additional memory
needed for internal data structures cannot be allocated.

``` cpp
template<class RandomAccessIterator2>
  pair<RandomAccessIterator2, RandomAccessIterator2>
    operator()(RandomAccessIterator2 first, RandomAccessIterator2 last) const;
```

*Mandates:* `RandomAccessIterator1` and `RandomAccessIterator2` have the
same value type.

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
specializations of the class template `hash` [[functional.syn]] as the
default hash function.

Each specialization of `hash` is either enabled or disabled, as
described below.

[*Note 1*: Enabled specializations meet the *Cpp17Hash* requirements,
and disabled specializations do not. — *end note*]

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
function object types [[function.objects]].

[*Note 2*: This means that the specialization of `hash` exists, but any
attempts to use it as a *Cpp17Hash* will be ill-formed. — *end note*]

An enabled specialization `hash<Key>` will:

- meet the *Cpp17Hash* requirements ([[cpp17.hash]]), with `Key` as the
  function call argument type, the *Cpp17DefaultConstructible*
  requirements ([[cpp17.defaultconstructible]]), the
  *Cpp17CopyAssignable* requirements ([[cpp17.copyassignable]]),
- be swappable [[swappable.requirements]] for lvalues,
- meet the requirement that if `k1 == k2` is `true`, `h(k1) == h(k2)` is
  also `true`, where `h` is an object of type `hash<Key>` and `k1` and
  `k2` are objects of type `Key`;
- meet the requirement that the expression `h(k)`, where `h` is an
  object of type `hash<Key>` and `k` is an object of type `Key`, shall
  not throw an exception unless `hash<Key>` is a program-defined
  specialization that depends on at least one program-defined type.

## Metaprogramming and type traits <a id="meta">[[meta]]</a>

This subclause describes components used by C++ programs, particularly
in templates, to support the widest possible range of types, optimise
template code usage, detect type related user errors, and perform type
inference and transformation at compile time. It includes type
classification traits, type property inspection traits, and type
transformations. The type classification traits describe a complete
taxonomy of all possible C++ types, and state where in that taxonomy a
given type belongs. The type property inspection traits allow important
characteristics of types or of combinations of types to be inspected.
The type transformations allow certain properties of types to be
manipulated.

All functions specified in this subclause are signal-safe
[[support.signal]].

### Requirements <a id="meta.rqmts">[[meta.rqmts]]</a>

A describes a property of a type. It shall be a class template that
takes one template type argument and, optionally, additional arguments
that help define the property being described. It shall be
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*, and publicly and
unambiguously derived, directly or indirectly, from its *base
characteristic*, which is a specialization of the template
`integral_constant` [[meta.help]], with the arguments to the template
`integral_constant` determined by the requirements for the particular
property being described. The member names of the base characteristic
shall not be hidden and shall be unambiguously available in the
*Cpp17UnaryTypeTrait*.

A describes a relationship between two types. It shall be a class
template that takes two template type arguments and, optionally,
additional arguments that help define the relationship being described.
It shall be *Cpp17DefaultConstructible*, *Cpp17CopyConstructible*, and
publicly and unambiguously derived, directly or indirectly, from its
*base characteristic*, which is a specialization of the template
`integral_constant` [[meta.help]], with the arguments to the template
`integral_constant` determined by the requirements for the particular
relationship being described. The member names of the base
characteristic shall not be hidden and shall be unambiguously available
in the *Cpp17BinaryTypeTrait*.

A modifies a property of a type. It shall be a class template that takes
one template type argument and, optionally, additional arguments that
help define the modification. It shall define a publicly accessible
nested type named `type`, which shall be a synonym for the modified
type.

Unless otherwise specified, the behavior of a program that adds
specializations for any of the templates specified in this subclause 
[[meta]] is undefined.

Unless otherwise specified, an incomplete type may be used to
instantiate a template specified in this subclause. The behavior of a
program is undefined if:

- an instantiation of a template specified in subclause  [[meta]]
  directly or indirectly depends on an incompletely-defined object type
  `T`, and
- that instantiation could yield a different result were `T`
  hypothetically completed.

### Header `<type_traits>` synopsis <a id="meta.type.synop">[[meta.type.synop]]</a>

``` cpp
namespace std {
  // [meta.help], helper class
  template<class T, T v> struct integral_constant;

  template<bool B>
    using bool_constant = integral_constant<bool, B>;
  using true_type  = bool_constant<true>;
  using false_type = bool_constant<false>;

  // [meta.unary.cat], primary type categories
  template<class T> struct is_void;
  template<class T> struct is_null_pointer;
  template<class T> struct is_integral;
  template<class T> struct is_floating_point;
  template<class T> struct is_array;
  template<class T> struct is_pointer;
  template<class T> struct is_lvalue_reference;
  template<class T> struct is_rvalue_reference;
  template<class T> struct is_member_object_pointer;
  template<class T> struct is_member_function_pointer;
  template<class T> struct is_enum;
  template<class T> struct is_union;
  template<class T> struct is_class;
  template<class T> struct is_function;

  // [meta.unary.comp], composite type categories
  template<class T> struct is_reference;
  template<class T> struct is_arithmetic;
  template<class T> struct is_fundamental;
  template<class T> struct is_object;
  template<class T> struct is_scalar;
  template<class T> struct is_compound;
  template<class T> struct is_member_pointer;

  // [meta.unary.prop], type properties
  template<class T> struct is_const;
  template<class T> struct is_volatile;
  template<class T> struct is_trivial;
  template<class T> struct is_trivially_copyable;
  template<class T> struct is_standard_layout;
  template<class T> struct is_empty;
  template<class T> struct is_polymorphic;
  template<class T> struct is_abstract;
  template<class T> struct is_final;
  template<class T> struct is_aggregate;

  template<class T> struct is_signed;
  template<class T> struct is_unsigned;
  template<class T> struct is_bounded_array;
  template<class T> struct is_unbounded_array;

  template<class T, class... Args> struct is_constructible;
  template<class T> struct is_default_constructible;
  template<class T> struct is_copy_constructible;
  template<class T> struct is_move_constructible;

  template<class T, class U> struct is_assignable;
  template<class T> struct is_copy_assignable;
  template<class T> struct is_move_assignable;

  template<class T, class U> struct is_swappable_with;
  template<class T> struct is_swappable;

  template<class T> struct is_destructible;

  template<class T, class... Args> struct is_trivially_constructible;
  template<class T> struct is_trivially_default_constructible;
  template<class T> struct is_trivially_copy_constructible;
  template<class T> struct is_trivially_move_constructible;

  template<class T, class U> struct is_trivially_assignable;
  template<class T> struct is_trivially_copy_assignable;
  template<class T> struct is_trivially_move_assignable;
  template<class T> struct is_trivially_destructible;

  template<class T, class... Args> struct is_nothrow_constructible;
  template<class T> struct is_nothrow_default_constructible;
  template<class T> struct is_nothrow_copy_constructible;
  template<class T> struct is_nothrow_move_constructible;

  template<class T, class U> struct is_nothrow_assignable;
  template<class T> struct is_nothrow_copy_assignable;
  template<class T> struct is_nothrow_move_assignable;

  template<class T, class U> struct is_nothrow_swappable_with;
  template<class T> struct is_nothrow_swappable;

  template<class T> struct is_nothrow_destructible;

  template<class T> struct has_virtual_destructor;

  template<class T> struct has_unique_object_representations;

  // [meta.unary.prop.query], type property queries
  template<class T> struct alignment_of;
  template<class T> struct rank;
  template<class T, unsigned I = 0> struct extent;

  // [meta.rel], type relations
  template<class T, class U> struct is_same;
  template<class Base, class Derived> struct is_base_of;
  template<class From, class To> struct is_convertible;
  template<class From, class To> struct is_nothrow_convertible;
  template<class T, class U> struct is_layout_compatible;
  template<class Base, class Derived> struct is_pointer_interconvertible_base_of;

  template<class Fn, class... ArgTypes> struct is_invocable;
  template<class R, class Fn, class... ArgTypes> struct is_invocable_r;

  template<class Fn, class... ArgTypes> struct is_nothrow_invocable;
  template<class R, class Fn, class... ArgTypes> struct is_nothrow_invocable_r;

  // [meta.trans.cv], const-volatile modifications
  template<class T> struct remove_const;
  template<class T> struct remove_volatile;
  template<class T> struct remove_cv;
  template<class T> struct add_const;
  template<class T> struct add_volatile;
  template<class T> struct add_cv;

  template<class T>
    using remove_const_t    = typename remove_const<T>::type;
  template<class T>
    using remove_volatile_t = typename remove_volatile<T>::type;
  template<class T>
    using remove_cv_t       = typename remove_cv<T>::type;
  template<class T>
    using add_const_t       = typename add_const<T>::type;
  template<class T>
    using add_volatile_t    = typename add_volatile<T>::type;
  template<class T>
    using add_cv_t          = typename add_cv<T>::type;

  // [meta.trans.ref], reference modifications
  template<class T> struct remove_reference;
  template<class T> struct add_lvalue_reference;
  template<class T> struct add_rvalue_reference;

  template<class T>
    using remove_reference_t     = typename remove_reference<T>::type;
  template<class T>
    using add_lvalue_reference_t = typename add_lvalue_reference<T>::type;
  template<class T>
    using add_rvalue_reference_t = typename add_rvalue_reference<T>::type;

  // [meta.trans.sign], sign modifications
  template<class T> struct make_signed;
  template<class T> struct make_unsigned;

  template<class T>
    using make_signed_t   = typename make_signed<T>::type;
  template<class T>
    using make_unsigned_t = typename make_unsigned<T>::type;

  // [meta.trans.arr], array modifications
  template<class T> struct remove_extent;
  template<class T> struct remove_all_extents;

  template<class T>
    using remove_extent_t      = typename remove_extent<T>::type;
  template<class T>
    using remove_all_extents_t = typename remove_all_extents<T>::type;

  // [meta.trans.ptr], pointer modifications
  template<class T> struct remove_pointer;
  template<class T> struct add_pointer;

  template<class T>
    using remove_pointer_t = typename remove_pointer<T>::type;
  template<class T>
    using add_pointer_t    = typename add_pointer<T>::type;

  // [meta.trans.other], other transformations
  template<class T> struct type_identity;
  template<size_t Len, size_t Align = default-alignment> // see [meta.trans.other]
    struct aligned_storage;
  template<size_t Len, class... Types> struct aligned_union;
  template<class T> struct remove_cvref;
  template<class T> struct decay;
  template<bool, class T = void> struct enable_if;
  template<bool, class T, class F> struct conditional;
  template<class... T> struct common_type;
  template<class T, class U, template<class> class TQual, template<class> class UQual>
    struct basic_common_reference { };
  template<class... T> struct common_reference;
  template<class T> struct underlying_type;
  template<class Fn, class... ArgTypes> struct invoke_result;
  template<class T> struct unwrap_reference;
  template<class T> struct unwrap_ref_decay;

  template<class T>
    using type_identity_t    = typename type_identity<T>::type;
  template<size_t Len, size_t Align = default-alignment> // see [meta.trans.other]
    using aligned_storage_t  = typename aligned_storage<Len, Align>::type;
  template<size_t Len, class... Types>
    using aligned_union_t    = typename aligned_union<Len, Types...>::type;
  template<class T>
    using remove_cvref_t     = typename remove_cvref<T>::type;
  template<class T>
    using decay_t            = typename decay<T>::type;
  template<bool b, class T = void>
    using enable_if_t        = typename enable_if<b, T>::type;
  template<bool b, class T, class F>
    using conditional_t      = typename conditional<b, T, F>::type;
  template<class... T>
    using common_type_t      = typename common_type<T...>::type;
  template<class... T>
    using common_reference_t = typename common_reference<T...>::type;
  template<class T>
    using underlying_type_t  = typename underlying_type<T>::type;
  template<class Fn, class... ArgTypes>
    using invoke_result_t    = typename invoke_result<Fn, ArgTypes...>::type;
  template<class T>
    using unwrap_reference_t = typename unwrap_reference<T>::type;
  template<class T>
    using unwrap_ref_decay_t = typename unwrap_ref_decay<T>::type;
  template<class...>
    using void_t             = void;

  // [meta.logical], logical operator traits
  template<class... B> struct conjunction;
  template<class... B> struct disjunction;
  template<class B> struct negation;

  // [meta.unary.cat], primary type categories
  template<class T>
    inline constexpr bool is_void_v = is_void<T>::value;
  template<class T>
    inline constexpr bool is_null_pointer_v = is_null_pointer<T>::value;
  template<class T>
    inline constexpr bool is_integral_v = is_integral<T>::value;
  template<class T>
    inline constexpr bool is_floating_point_v = is_floating_point<T>::value;
  template<class T>
    inline constexpr bool is_array_v = is_array<T>::value;
  template<class T>
    inline constexpr bool is_pointer_v = is_pointer<T>::value;
  template<class T>
    inline constexpr bool is_lvalue_reference_v = is_lvalue_reference<T>::value;
  template<class T>
    inline constexpr bool is_rvalue_reference_v = is_rvalue_reference<T>::value;
  template<class T>
    inline constexpr bool is_member_object_pointer_v = is_member_object_pointer<T>::value;
  template<class T>
    inline constexpr bool is_member_function_pointer_v = is_member_function_pointer<T>::value;
  template<class T>
    inline constexpr bool is_enum_v = is_enum<T>::value;
  template<class T>
    inline constexpr bool is_union_v = is_union<T>::value;
  template<class T>
    inline constexpr bool is_class_v = is_class<T>::value;
  template<class T>
    inline constexpr bool is_function_v = is_function<T>::value;

  // [meta.unary.comp], composite type categories
  template<class T>
    inline constexpr bool is_reference_v = is_reference<T>::value;
  template<class T>
    inline constexpr bool is_arithmetic_v = is_arithmetic<T>::value;
  template<class T>
    inline constexpr bool is_fundamental_v = is_fundamental<T>::value;
  template<class T>
    inline constexpr bool is_object_v = is_object<T>::value;
  template<class T>
    inline constexpr bool is_scalar_v = is_scalar<T>::value;
  template<class T>
    inline constexpr bool is_compound_v = is_compound<T>::value;
  template<class T>
    inline constexpr bool is_member_pointer_v = is_member_pointer<T>::value;

  // [meta.unary.prop], type properties
  template<class T>
    inline constexpr bool is_const_v = is_const<T>::value;
  template<class T>
    inline constexpr bool is_volatile_v = is_volatile<T>::value;
  template<class T>
    inline constexpr bool is_trivial_v = is_trivial<T>::value;
  template<class T>
    inline constexpr bool is_trivially_copyable_v = is_trivially_copyable<T>::value;
  template<class T>
    inline constexpr bool is_standard_layout_v = is_standard_layout<T>::value;
  template<class T>
    inline constexpr bool is_empty_v = is_empty<T>::value;
  template<class T>
    inline constexpr bool is_polymorphic_v = is_polymorphic<T>::value;
  template<class T>
    inline constexpr bool is_abstract_v = is_abstract<T>::value;
  template<class T>
    inline constexpr bool is_final_v = is_final<T>::value;
  template<class T>
    inline constexpr bool is_aggregate_v = is_aggregate<T>::value;
  template<class T>
    inline constexpr bool is_signed_v = is_signed<T>::value;
  template<class T>
    inline constexpr bool is_unsigned_v = is_unsigned<T>::value;
  template<class T>
    inline constexpr bool is_bounded_array_v = is_bounded_array<T>::value;
  template<class T>
    inline constexpr bool is_unbounded_array_v = is_unbounded_array<T>::value;
  template<class T, class... Args>
    inline constexpr bool is_constructible_v = is_constructible<T, Args...>::value;
  template<class T>
    inline constexpr bool is_default_constructible_v = is_default_constructible<T>::value;
  template<class T>
    inline constexpr bool is_copy_constructible_v = is_copy_constructible<T>::value;
  template<class T>
    inline constexpr bool is_move_constructible_v = is_move_constructible<T>::value;
  template<class T, class U>
    inline constexpr bool is_assignable_v = is_assignable<T, U>::value;
  template<class T>
    inline constexpr bool is_copy_assignable_v = is_copy_assignable<T>::value;
  template<class T>
    inline constexpr bool is_move_assignable_v = is_move_assignable<T>::value;
  template<class T, class U>
    inline constexpr bool is_swappable_with_v = is_swappable_with<T, U>::value;
  template<class T>
    inline constexpr bool is_swappable_v = is_swappable<T>::value;
  template<class T>
    inline constexpr bool is_destructible_v = is_destructible<T>::value;
  template<class T, class... Args>
    inline constexpr bool is_trivially_constructible_v
      = is_trivially_constructible<T, Args...>::value;
  template<class T>
    inline constexpr bool is_trivially_default_constructible_v
      = is_trivially_default_constructible<T>::value;
  template<class T>
    inline constexpr bool is_trivially_copy_constructible_v
      = is_trivially_copy_constructible<T>::value;
  template<class T>
    inline constexpr bool is_trivially_move_constructible_v
      = is_trivially_move_constructible<T>::value;
  template<class T, class U>
    inline constexpr bool is_trivially_assignable_v = is_trivially_assignable<T, U>::value;
  template<class T>
    inline constexpr bool is_trivially_copy_assignable_v
      = is_trivially_copy_assignable<T>::value;
  template<class T>
    inline constexpr bool is_trivially_move_assignable_v
      = is_trivially_move_assignable<T>::value;
  template<class T>
    inline constexpr bool is_trivially_destructible_v = is_trivially_destructible<T>::value;
  template<class T, class... Args>
    inline constexpr bool is_nothrow_constructible_v
      = is_nothrow_constructible<T, Args...>::value;
  template<class T>
    inline constexpr bool is_nothrow_default_constructible_v
      = is_nothrow_default_constructible<T>::value;
  template<class T>
    inline constexpr bool is_nothrow_copy_constructible_v
    = is_nothrow_copy_constructible<T>::value;
  template<class T>
    inline constexpr bool is_nothrow_move_constructible_v
      = is_nothrow_move_constructible<T>::value;
  template<class T, class U>
    inline constexpr bool is_nothrow_assignable_v = is_nothrow_assignable<T, U>::value;
  template<class T>
    inline constexpr bool is_nothrow_copy_assignable_v = is_nothrow_copy_assignable<T>::value;
  template<class T>
    inline constexpr bool is_nothrow_move_assignable_v = is_nothrow_move_assignable<T>::value;
  template<class T, class U>
    inline constexpr bool is_nothrow_swappable_with_v = is_nothrow_swappable_with<T, U>::value;
  template<class T>
    inline constexpr bool is_nothrow_swappable_v = is_nothrow_swappable<T>::value;
  template<class T>
    inline constexpr bool is_nothrow_destructible_v = is_nothrow_destructible<T>::value;
  template<class T>
    inline constexpr bool has_virtual_destructor_v = has_virtual_destructor<T>::value;
  template<class T>
    inline constexpr bool has_unique_object_representations_v
      = has_unique_object_representations<T>::value;

  // [meta.unary.prop.query], type property queries
  template<class T>
    inline constexpr size_t alignment_of_v = alignment_of<T>::value;
  template<class T>
    inline constexpr size_t rank_v = rank<T>::value;
  template<class T, unsigned I = 0>
    inline constexpr size_t extent_v = extent<T, I>::value;

  // [meta.rel], type relations
  template<class T, class U>
    inline constexpr bool is_same_v = is_same<T, U>::value;
  template<class Base, class Derived>
    inline constexpr bool is_base_of_v = is_base_of<Base, Derived>::value;
  template<class From, class To>
    inline constexpr bool is_convertible_v = is_convertible<From, To>::value;
  template<class From, class To>
    inline constexpr bool is_nothrow_convertible_v = is_nothrow_convertible<From, To>::value;
  template<class T, class U>
    inline constexpr bool is_layout_compatible_v = is_layout_compatible<T, U>::value;
  template<class Base, class Derived>
    inline constexpr bool is_pointer_interconvertible_base_of_v
      = is_pointer_interconvertible_base_of<Base, Derived>::value;
  template<class Fn, class... ArgTypes>
    inline constexpr bool is_invocable_v = is_invocable<Fn, ArgTypes...>::value;
  template<class R, class Fn, class... ArgTypes>
    inline constexpr bool is_invocable_r_v = is_invocable_r<R, Fn, ArgTypes...>::value;
  template<class Fn, class... ArgTypes>
    inline constexpr bool is_nothrow_invocable_v = is_nothrow_invocable<Fn, ArgTypes...>::value;
  template<class R, class Fn, class... ArgTypes>
    inline constexpr bool is_nothrow_invocable_r_v
      = is_nothrow_invocable_r<R, Fn, ArgTypes...>::value;

  // [meta.logical], logical operator traits
  template<class... B>
    inline constexpr bool conjunction_v = conjunction<B...>::value;
  template<class... B>
    inline constexpr bool disjunction_v = disjunction<B...>::value;
  template<class B>
    inline constexpr bool negation_v = negation<B>::value;

  // [meta.member], member relationships
  template<class S, class M>
    constexpr bool is_pointer_interconvertible_with_class(M S::*m) noexcept;
  template<class S1, class S2, class M1, class M2>
    constexpr bool is_corresponding_member(M1 S1::*m1, M2 S2::*m2) noexcept;

  // [meta.const.eval], constant evaluation context
  constexpr bool is_constant_evaluated() noexcept;
}
```

### Helper classes <a id="meta.help">[[meta.help]]</a>

``` cpp
namespace std {
  template<class T, T v> struct integral_constant {
    static constexpr T value = v;

    using value_type = T;
    using type = integral_constant<T, v>;

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

Each of these templates shall be a *Cpp17UnaryTypeTrait* [[meta.rqmts]]
with a base characteristic of `true_type` if the corresponding condition
is `true`, otherwise `false_type`.

#### Primary type categories <a id="meta.unary.cat">[[meta.unary.cat]]</a>

The primary type categories correspond to the descriptions given in
subclause  [[basic.types]] of the C++ standard.

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

[*Note 1*: For any given type `T`, exactly one of the primary type
categories has a `value` member that evaluates to `true`. — *end note*]

#### Composite type traits <a id="meta.unary.comp">[[meta.unary.comp]]</a>

These templates provide convenient compositions of the primary type
categories, corresponding to the descriptions given in subclause 
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
argument is a complete type.

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial ([[basic.types]], [[special]]) function call that is not an
odr-use [[basic.def.odr]] of `declval` in the context of the
corresponding definition notwithstanding the restrictions of 
[[declval]].

[*Note 1*: A union is a class type that can be marked with
`final`. — *end note*]

[*Example 1*:

``` cpp
is_const_v<const volatile int>      // true
is_const_v<const int*>              // false
is_const_v<const int&>              // false
is_const_v<int[3]>                  // false
is_const_v<const int[3]>            // true
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
otherwise, the condition holds true for integral types. — *end note*]

### Type property queries <a id="meta.unary.prop.query">[[meta.unary.prop.query]]</a>

This subclause contains templates that may be used to query properties
of types at compile time.

Each of these templates shall be a *Cpp17UnaryTypeTrait* [[meta.rqmts]]
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

Each of these templates shall be a *Cpp17BinaryTypeTrait* [[meta.rqmts]]
with a base characteristic of `true_type` if the corresponding condition
is true, otherwise `false_type`.

[*Note 1*: Base classes that are private, protected, or ambiguous are,
nonetheless, base classes. — *end note*]

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial ([[basic.types]], [[special]]) function call that is not an
odr-use [[basic.def.odr]] of `declval` in the context of the
corresponding definition notwithstanding the restrictions of 
[[declval]].

[*Example 1*:

``` cpp
struct B {};
struct B1 : B {};
struct B2 : B {};
struct D : private B1, private B2 {};

is_base_of_v<B, D>              // true
is_base_of_v<const B, D>        // true
is_base_of_v<B, const D>        // true
is_base_of_v<B, const B>        // true
is_base_of_v<D, B>              // false
is_base_of_v<B&, D&>            // false
is_base_of_v<B[3], D[3]>        // false
is_base_of_v<int, int>          // false
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

[*Note 2*: This requirement gives well-defined results for reference
types, void types, array types, and function types. — *end note*]

Access checking is performed in a context unrelated to `To` and `From`.
Only the validity of the immediate context of the *expression* of the
`return` statement [[stmt.return]] (including initialization of the
returned object or reference) is considered.

[*Note 3*: The initialization can result in side effects such as the
instantiation of class template specializations and function template
specializations, the generation of implicitly-defined functions, and so
on. Such side effects are not in the “immediate context” and can result
in the program being ill-formed. — *end note*]

### Transformations between types <a id="meta.trans">[[meta.trans]]</a>

This subclause contains templates that may be used to transform one type
to another following some predefined rule.

Each of the templates in this subclause shall be a
*Cpp17TransformationTrait* [[meta.rqmts]].

#### Const-volatile modifications <a id="meta.trans.cv">[[meta.trans.cv]]</a>

[*Example 1*: `remove_const_t<const volatile int>` evaluates to
`volatile int`, whereas `remove_const_t<const int*>` evaluates to
`const int*`. — *end example*]

#### Reference modifications <a id="meta.trans.ref">[[meta.trans.ref]]</a>

[*Note 1*: This rule reflects the semantics of reference collapsing
[[dcl.ref]]. — *end note*]

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

[*Note 1*: This behavior is similar to the lvalue-to-rvalue
[[conv.lval]], array-to-pointer [[conv.array]], and function-to-pointer
[[conv.func]] conversions applied when an lvalue is used as an rvalue,
but also strips cv-qualifiers from class types in order to more closely
model by-value argument passing. — *end note*]

[*Note 2*:

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

In addition to being available via inclusion of the `<type_traits>`
header, the templates `unwrap_reference`, `unwrap_ref_decay`,
`unwrap_reference_t`, and `unwrap_ref_decay_t` are available when the
header `<functional>` [[functional.syn]] is included.

Let:

- `CREF(A)` be `add_lvalue_reference_t<const remove_reference_t<A>{}>`,
- `XREF(A)` denote a unary alias template `T` such that `T<U>` denotes
  the same type as `U` with the addition of `A`’s cv and reference
  qualifiers, for a non-reference cv-unqualified type `U`,
- `COPYCV(FROM, TO)` be an alias for type `TO` with the addition of
  `FROM`’s top-level cv-qualifiers,
  \[*Example 1*: `COPYCV(const int, volatile short)` is an alias for
  `const volatile short`. — *end example*]
- `COND-RES(X, Y)` be
  `decltype(false ?\ declval<X(&)()>()() :\ declval<Y(&)()>()())`.

Given types `A` and `B`, let `X` be `remove_reference_t<A>`, let `Y` be
`remove_reference_t<B>`, and let `COMMON-{REF}(A, B)` be:

- If `A` and `B` are both lvalue reference types, `COMMON-REF(A, B)` is
  `COND-RES(COPYCV(X, Y) &,
      COPYCV({}Y, X) &)` if that type exists and is a reference type.
- Otherwise, let `C` be `remove_reference_t<COMMON-REF(X&, Y&)>&&`. If
  `A` and `B` are both rvalue reference types, `C` is well-formed, and
  `is_convertible_v<A, C> && is_convertible_v<B, C>` is `true`, then
  `COMMON-REF(A, B)` is `C`.
- Otherwise, let `D` be `COMMON-REF(const X&, Y&)`. If `A` is an rvalue
  reference and `B` is an lvalue reference and `D` is well-formed and
  `is_convertible_v<A, D>` is `true`, then `COMMON-REF(A, B)` is `D`.
- Otherwise, if `A` is an lvalue reference and `B` is an rvalue
  reference, then `COMMON-REF(A, B)` is `COMMON-REF(B, A)`.
- Otherwise, `COMMON-REF(A, B)` is ill-formed.

If any of the types computed above is ill-formed, then
`COMMON-REF(A, B)` is ill-formed.

Note A: For the `common_type` trait applied to a template parameter pack
`T` of types, the member `type` shall be either defined or not present
as follows:

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
  - \[*Note 3*: None of the following will apply if there is a
    specialization `common_type<D1, D2>`. — *end note*]
  - Otherwise, if
    ``` cpp
    decay_t<decltype(false ? declval<D1>() : declval<D2>())>
    ```

    denotes a valid type, let `C` denote that type.
  - Otherwise, if `COND-RES(CREF(D1),
          CREF(D2))` denotes a type, let `C` denote the type
    `decay_t<COND-RES(CREF(D1),
          CREF(D2))>`.

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

[*Note 4*: Such specializations are needed when only explicit
conversions are desired between the template arguments. — *end note*]

Such a specialization need not have a member named `type`, but if it
does, that member shall be a *typedef-name* for an accessible and
unambiguous cv-unqualified non-reference type `C` to which each of the
types `T1` and `T2` is explicitly convertible. Moreover,
`common_type_t<T1, T2>` shall denote the same type, if any, as does
`common_type_t<T2, T1>`. No diagnostic is required for a violation of
this Note’s rules.

Note C: For the `common_reference` trait applied to a parameter pack `T`
of types, the member `type` shall be either defined or not present as
follows:

- If `sizeof...(T)` is zero, there shall be no member `type`.
- Otherwise, if `sizeof...(T)` is one, let `T0` denote the sole type in
  the pack `T`. The member typedef `type` shall denote the same type as
  `T0`.
- Otherwise, if `sizeof...(T)` is two, let `T1` and `T2` denote the two
  types in the pack `T`. Then
  - If `T1` and `T2` are reference types and `COMMON-REF(T1, T2)` is
    well-formed, then the member typedef `type` denotes that type.
  - Otherwise, if
    `basic_common_reference<remove_cvref_t<T1>, remove_cvref_t<T2>,
          {}XREF({}T1), XREF(T2)>::type` is well-formed, then the member
    typedef `type` denotes that type.
  - Otherwise, if `COND-RES(T1, T2)` is well-formed, then the member
    typedef `type` denotes that type.
  - Otherwise, if `common_type_t<T1, T2>` is well-formed, then the
    member typedef `type` denotes that type.
  - Otherwise, there shall be no member `type`.
- Otherwise, if `sizeof...(T)` is greater than two, let `T1`, `T2`, and
  `Rest`, respectively, denote the first, second, and (pack of)
  remaining types comprising `T`. Let `C` be the type
  `common_reference_t<T1, T2>`. Then:
  - If there is such a type `C`, the member typedef `type` shall denote
    the same type, if any, as `common_reference_t<C, Rest...>`.
  - Otherwise, there shall be no member `type`.

Note D: Notwithstanding the provisions of [[meta.type.synop]], and
pursuant to [[namespace.std]], a program may partially specialize
`basic_common_reference<T, U, TQual, UQual>` for types `T` and `U` such
that `is_same_v<T, decay_t<T>{>}` and `is_same_v<U, decay_t<U>{>}` are
each `true`.

[*Note 5*: Such specializations can be used to influence the result of
`common_reference`, and are needed when only explicit conversions are
desired between the template arguments. — *end note*]

Such a specialization need not have a member named `type`, but if it
does, that member shall be a *typedef-name* for an accessible and
unambiguous type `C` to which each of the types `TQual<T>` and
`UQual<U>` is convertible. Moreover,
`basic_common_reference<T, U, TQual, UQual>::type` shall denote the same
type, if any, as does
`basic_common_reference<U, T, UQual, TQual>::type`. No diagnostic is
required for a violation of these rules.

[*Example 2*:

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

For a specialization `conjunction<``B₁``, `…`, ``B_N``>`, if there is a
template type argument `Bᵢ` for which `bool(``Bᵢ``::value)` is `false`,
then instantiating `conjunction<``B₁``, `…`, ``B_N``>::value` does not
require the instantiation of `Bⱼ``::value` for j > i.

[*Note 1*: This is analogous to the short-circuiting behavior of the
built-in operator `&&`. — *end note*]

Every template type argument for which `Bᵢ``::value` is instantiated
shall be usable as a base class and shall have a member `value` which is
convertible to `bool`, is not hidden, and is unambiguously available in
the type.

The specialization `conjunction<``B₁``, `…`, ``B_N``>` has a public and
unambiguous base that is either

- the first type `Bᵢ` in the list `true_type, ``B₁``, `…`, ``B_N` for
  which `bool(``Bᵢ``::value)` is `false`, or
- if there is no such `Bᵢ`, the last type in the list.

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

For a specialization `disjunction<``B₁``, `…`, ``B_N``>`, if there is a
template type argument `Bᵢ` for which `bool(``Bᵢ``::value)` is `true`,
then instantiating `disjunction<``B₁``, `…`, ``B_N``>::value` does not
require the instantiation of `Bⱼ``::value` for j > i.

[*Note 3*: This is analogous to the short-circuiting behavior of the
built-in operator `||`. — *end note*]

Every template type argument for which `Bᵢ``::value` is instantiated
shall be usable as a base class and shall have a member `value` which is
convertible to `bool`, is not hidden, and is unambiguously available in
the type.

The specialization `disjunction<``B₁``, `…`, ``B_N``>` has a public and
unambiguous base that is either

- the first type `Bᵢ` in the list `false_type, ``B₁``, `…`, ``B_N` for
  which `bool(``Bᵢ``::value)` is `true`, or
- if there is no such `Bᵢ`, the last type in the list.

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
type argument. The type `negation<B>` is a *Cpp17UnaryTypeTrait* with a
base characteristic of `bool_constant<!bool(B::value)>`.

### Member relationships <a id="meta.member">[[meta.member]]</a>

``` cpp
template<class S, class M>
  constexpr bool is_pointer_interconvertible_with_class(M S::*m) noexcept;
```

*Mandates:* `S` is a complete type.

*Returns:* `true` if and only if `S` is a standard-layout type, `M` is
an object type, `m` is not null, and each object `s` of type `S` is
pointer-interconvertible [[basic.compound]] with its subobject `s.*m`.

``` cpp
template<class S1, class S2, class M1, class M2>
  constexpr bool is_corresponding_member(M1 S1::*m1, M2 S2::*m2) noexcept;
```

*Mandates:* `S1` and `S2` are complete types.

*Returns:* `true` if and only if `S1` and `S2` are standard-layout
types, `M1` and `M2` are object types, `m1` and `m2` are not null, and
`m1` and `m2` point to corresponding members of the common initial
sequence [[class.mem]] of `S1` and `S2`.

[*Note 1*:

The type of a pointer-to-member expression `&C::b` is not always a
pointer to member of `C`, leading to potentially surprising results when
using these functions in conjunction with inheritance.

[*Example 1*:

``` cpp
struct A { int a; };                    // a standard-layout class
struct B { int b; };                    // a standard-layout class
struct C: public A, public B { };       // not a standard-layout class

static_assert( is_pointer_interconvertible_with_class( &C::b ) );
  // Succeeds because, despite its appearance, &C::b has type
  // ``pointer to member of B of type int''.
static_assert( is_pointer_interconvertible_with_class<C>( &C::b ) );
  // Forces the use of class C, and fails.

static_assert( is_corresponding_member( &C::a, &C::b ) );
  // Succeeds because, despite its appearance, &C::a and &C::b have types
  // ``pointer to member of A of type int'' and
  // ``pointer to member of B of type int'', respectively.
static_assert( is_corresponding_member<C, C>( &C::a, &C::b ) );
  // Forces the use of class C, and fails.
```

— *end example*]

— *end note*]

### Constant evaluation context <a id="meta.const.eval">[[meta.const.eval]]</a>

``` cpp
constexpr bool is_constant_evaluated() noexcept;
```

*Returns:* `true` if and only if evaluation of the call occurs within
the evaluation of an expression or conversion that is manifestly
constant-evaluated [[expr.const]].

[*Example 1*:

``` cpp
constexpr void f(unsigned char *p, int n) {
  if (std::is_constant_evaluated()) {           // should not be a constexpr if statement
    for (int k = 0; k<n; ++k) p[k] = 0;
  } else {
    memset(p, 0, n);                            // not a core constant expression
  }
}
```

— *end example*]

## Compile-time rational arithmetic <a id="ratio">[[ratio]]</a>

### In general <a id="ratio.general">[[ratio.general]]</a>

Subclause  [[ratio]] describes the ratio library. It provides a class
template `ratio` which exactly represents any finite rational number
with a numerator and denominator representable by compile-time constants
of type `intmax_t`.

Throughout subclause  [[ratio]], the names of template parameters are
used to express type requirements. If a template parameter is named `R1`
or `R2`, and the template argument is not a specialization of the
`ratio` template, the program is ill-formed.

### Header `<ratio>` synopsis <a id="ratio.syn">[[ratio.syn]]</a>

``` cpp
namespace std {
  // [ratio.ratio], class template ratio
  template<intmax_t N, intmax_t D = 1> class ratio;

  // [ratio.arithmetic], ratio arithmetic
  template<class R1, class R2> using ratio_add = see below;
  template<class R1, class R2> using ratio_subtract = see below;
  template<class R1, class R2> using ratio_multiply = see below;
  template<class R1, class R2> using ratio_divide = see below;

  // [ratio.comparison], ratio comparison
  template<class R1, class R2> struct ratio_equal;
  template<class R1, class R2> struct ratio_not_equal;
  template<class R1, class R2> struct ratio_less;
  template<class R1, class R2> struct ratio_less_equal;
  template<class R1, class R2> struct ratio_greater;
  template<class R1, class R2> struct ratio_greater_equal;

  template<class R1, class R2>
    inline constexpr bool ratio_equal_v = ratio_equal<R1, R2>::value;
  template<class R1, class R2>
    inline constexpr bool ratio_not_equal_v = ratio_not_equal<R1, R2>::value;
  template<class R1, class R2>
    inline constexpr bool ratio_less_v = ratio_less<R1, R2>::value;
  template<class R1, class R2>
    inline constexpr bool ratio_less_equal_v = ratio_less_equal<R1, R2>::value;
  template<class R1, class R2>
    inline constexpr bool ratio_greater_v = ratio_greater<R1, R2>::value;
  template<class R1, class R2>
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
  template<intmax_t N, intmax_t D = 1> class ratio {
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
absolute value which is positive. This excludes the most negative
value. — *end note*]

The static data members `num` and `den` shall have the following values,
where `gcd` represents the greatest common divisor of the absolute
values of `N` and `D`:

- `num` shall have the value `sign(N) * sign(D) * abs(N) / gcd`.
- `den` shall have the value `abs(D) / gcd`.

### Arithmetic on `ratio`s <a id="ratio.arithmetic">[[ratio.arithmetic]]</a>

Each of the alias templates `ratio_add`, `ratio_subtract`,
`ratio_multiply`, and `ratio_divide` denotes the result of an arithmetic
computation on two `ratio`s `R1` and `R2`. With `X` and `Y` computed (in
the absence of arithmetic overflow) as specified by
[[ratio.arithmetic]], each alias denotes a `ratio<U, V>` such that `U`
is the same as `ratio<X, Y>::num` and `V` is the same as
`ratio<X, Y>::den`.

If it is not possible to represent `U` or `V` with `intmax_t`, the
program is ill-formed. Otherwise, an implementation should yield correct
values of `U` and `V`. If it is not possible to represent `X` or `Y`
with `intmax_t`, the program is ill-formed unless the implementation
yields correct values of `U` and `V`.

**Table: Expressions used to perform ratio arithmetic** <a id="ratio.arithmetic">[ratio.arithmetic]</a>

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
template<class R1, class R2>
  struct ratio_equal : bool_constant<R1::num == R2::num && R1::den == R2::den> { };
```

``` cpp
template<class R1, class R2>
  struct ratio_not_equal : bool_constant<!ratio_equal_v<R1, R2>> { };
```

``` cpp
template<class R1, class R2>
  struct ratio_less : bool_constant<see below> { };
```

If `R1::num` × `R2::den` is less than `R2::num` × `R1::den`,
`ratio_less<R1, R2>` shall be derived from `bool_constant<true>`;
otherwise it shall be derived from `bool_constant<false>`.
Implementations may use other algorithms to compute this relationship to
avoid overflow. If overflow occurs, the program is ill-formed.

``` cpp
template<class R1, class R2>
  struct ratio_less_equal : bool_constant<!ratio_less_v<R2, R1>> { };
```

``` cpp
template<class R1, class R2>
  struct ratio_greater : bool_constant<ratio_less_v<R2, R1>> { };
```

``` cpp
template<class R1, class R2>
  struct ratio_greater_equal : bool_constant<!ratio_less_v<R1, R2>> { };
```

### SI types for `ratio` <a id="ratio.si">[[ratio.si]]</a>

For each of the *typedef-name*s `yocto`, `zepto`, `zetta`, and `yotta`,
if both of the constants used in its specification are representable by
`intmax_t`, the typedef is defined; if either of the constants is not
representable by `intmax_t`, the typedef is not defined.

## Class `type_index` <a id="type.index">[[type.index]]</a>

### Header `<typeindex>` synopsis <a id="type.index.synopsis">[[type.index.synopsis]]</a>

``` cpp
#include <compare>              // see [compare.syn]

namespace std {
  class type_index;
  template<class T> struct hash;
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
    bool operator< (const type_index& rhs) const noexcept;
    bool operator> (const type_index& rhs) const noexcept;
    bool operator<=(const type_index& rhs) const noexcept;
    bool operator>=(const type_index& rhs) const noexcept;
    strong_ordering operator<=>(const type_index& rhs) const noexcept;
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
can be used as an index type in associative containers [[associative]]
and in unordered associative containers [[unord]].

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
bool operator<(const type_index& rhs) const noexcept;
```

*Returns:* `target->before(*rhs.target)`.

``` cpp
bool operator>(const type_index& rhs) const noexcept;
```

*Returns:* `rhs.target->before(*target)`.

``` cpp
bool operator<=(const type_index& rhs) const noexcept;
```

*Returns:* `!rhs.target->before(*target)`.

``` cpp
bool operator>=(const type_index& rhs) const noexcept;
```

*Returns:* `!target->before(*rhs.target)`.

``` cpp
strong_ordering operator<=>(const type_index& rhs) const noexcept;
```

*Effects:* Equivalent to:

``` cpp
if (*target == *rhs.target) return strong_ordering::equal;
if (target->before(*rhs.target)) return strong_ordering::less;
return strong_ordering::greater;
```

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
template<> struct hash<type_index>;
```

For an object `index` of type `type_index`, `hash<type_index>()(index)`
shall evaluate to the same result as `index.hash_code()`.

## Execution policies <a id="execpol">[[execpol]]</a>

### In general <a id="execpol.general">[[execpol.general]]</a>

Subclause  [[execpol]] describes classes that are *execution policy*
types. An object of an execution policy type indicates the kinds of
parallelism allowed in the execution of an algorithm and expresses the
consequent requirements on the element access functions.

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

  // [execpol.unseq], unsequenced execution policy
  class unsequenced_policy;

  // [execpol.objects], execution policy objects
  inline constexpr sequenced_policy            seq{ unspecified };
  inline constexpr parallel_policy             par{ unspecified };
  inline constexpr parallel_unsequenced_policy par_unseq{ unspecified };
  inline constexpr unsequenced_policy          unseq{ unspecified };
}
```

### Execution policy type trait <a id="execpol.type">[[execpol.type]]</a>

``` cpp
template<class T> struct is_execution_policy { see below };
```

`is_execution_policy` can be used to detect execution policies for the
purpose of excluding function signatures from otherwise ambiguous
overload resolution participation.

`is_execution_policy<T>` is a *Cpp17UnaryTypeTrait* with a base
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
access function exits via an uncaught exception, `terminate()` is
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
access function exits via an uncaught exception, `terminate()` is
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
is called.

### Unsequenced execution policy <a id="execpol.unseq">[[execpol.unseq]]</a>

``` cpp
class execution::unsequenced_policy { unspecified };
```

The class `unsequenced_policy` is an execution policy type used as a
unique type to disambiguate parallel algorithm overloading and indicate
that a parallel algorithm’s execution may be vectorized, e.g., executed
on a single thread using instructions that operate on multiple data
items.

During the execution of a parallel algorithm with the
`execution::unsequenced_policy` policy, if the invocation of an element
access function exits via an uncaught exception, `terminate()` is
called.

### Execution policy objects <a id="execpol.objects">[[execpol.objects]]</a>

``` cpp
inline constexpr execution::sequenced_policy            execution::seq{ unspecified };
inline constexpr execution::parallel_policy             execution::par{ unspecified };
inline constexpr execution::parallel_unsequenced_policy execution::par_unseq{ unspecified };
inline constexpr execution::unsequenced_policy          execution::unseq{ unspecified };
```

The header `<execution>` declares global objects associated with each
type of execution policy.

## Primitive numeric conversions <a id="charconv">[[charconv]]</a>

### Header `<charconv>` synopsis <a id="charconv.syn">[[charconv.syn]]</a>

``` cpp
%
%
{chars_format{chars_format{chars_format{chars_formatnamespace std {
  // floating-point format for primitive numerical conversion
  enum class chars_format {
    scientific = unspecified,
    fixed = unspecified,
    hex = unspecified,
    general = fixed | scientific
  };
%
%
{to_chars_result{to_chars_result}

  // [charconv.to.chars], primitive numerical output conversion
  struct to_chars_result {
    char* ptr;
    errc ec;
    friend bool operator==(const to_chars_result&, const to_chars_result&) = default;
  };

  to_chars_result to_chars(char* first, char* last, see below value, int base = 10);
  to_chars_result to_chars(char* first, char* last, bool value, int base = 10) = delete;

  to_chars_result to_chars(char* first, char* last, float value);
  to_chars_result to_chars(char* first, char* last, double value);
  to_chars_result to_chars(char* first, char* last, long double value);

  to_chars_result to_chars(char* first, char* last, float value, chars_format fmt);
  to_chars_result to_chars(char* first, char* last, double value, chars_format fmt);
  to_chars_result to_chars(char* first, char* last, long double value, chars_format fmt);

  to_chars_result to_chars(char* first, char* last, float value,
                           chars_format fmt, int precision);
  to_chars_result to_chars(char* first, char* last, double value,
                           chars_format fmt, int precision);
  to_chars_result to_chars(char* first, char* last, long double value,
                           chars_format fmt, int precision);
%
%
{from_chars_result{from_chars_result}

  // [charconv.from.chars], primitive numerical input conversion
  struct from_chars_result {
    const char* ptr;
    errc ec;
    friend bool operator==(const from_chars_result&, const from_chars_result&) = default;
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

The type `chars_format` is a bitmask type [[bitmask.types]] with
elements `scientific`, `fixed`, and `hex`.

The types `to_chars_result` and `from_chars_result` have the data
members and special members specified above. They have no base classes
or members other than those specified.

### Primitive numeric output conversion <a id="charconv.to.chars">[[charconv.to.chars]]</a>

All functions named `to_chars` convert `value` into a character string
by successively filling the range \[`first`, `last`), where \[`first`,
`last`) is required to be a valid range. If the member `ec` of the
return value is such that the value is equal to the value of a
value-initialized `errc`, the conversion was successful and the member
`ptr` is the one-past-the-end pointer of the characters written.
Otherwise, the member `ec` has the value `errc::value_too_large`, the
member `ptr` has the value `last`, and the contents of the range
\[`first`, `last`) are unspecified.

The functions that take a floating-point `value` but not a `precision`
parameter ensure that the string representation consists of the smallest
number of characters such that there is at least one digit before the
radix point (if present) and parsing the representation using the
corresponding `from_chars` function recovers `value` exactly.

[*Note 1*: This guarantee applies only if `to_chars` and `from_chars`
are executed on the same implementation. — *end note*]

If there are several such representations, the representation with the
smallest difference from the floating-point argument value is chosen,
resolving any remaining ties using rounding according to
`round_to_nearest` [[round.style]].

The functions taking a `chars_format` parameter determine the conversion
specifier for `printf` as follows: The conversion specifier is `f` if
`fmt` is `chars_format::fixed`, `e` if `fmt` is
`chars_format::scientific`, `a` (without leading `"0x"` in the result)
if `fmt` is `chars_format::hex`, and `g` if `fmt` is
`chars_format::general`.

``` cpp
to_chars_result to_chars(char* first, char* last, see below value, int base = 10);
```

*Preconditions:* `base` has a value between 2 and 36 (inclusive).

*Effects:* The value of `value` is converted to a string of digits in
the given base (with no redundant leading zeroes). Digits in the range
10..35 (inclusive) are represented as lowercase characters `a`..`z`. If
`value` is less than zero, the representation starts with `’-’`.

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

*Preconditions:* `fmt` has the value of one of the enumerators of
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

*Preconditions:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* `value` is converted to a string in the style of `printf` in
the `"C"` locale with the given precision.

*Throws:* Nothing.

See also: ISO C 7.21.6.1

### Primitive numeric input conversion <a id="charconv.from.chars">[[charconv.from.chars]]</a>

All functions named `from_chars` analyze the string \[`first`, `last`)
for a pattern, where \[`first`, `last`) is required to be a valid range.
If no characters match the pattern, `value` is unmodified, the member
`ptr` of the return value is `first` and the member `ec` is equal to
`errc::invalid_argument`.

[*Note 1*: If the pattern allows for an optional sign, but the string
has no digit characters following the sign, no characters match the
pattern. — *end note*]

Otherwise, the characters matching the pattern are interpreted as a
representation of a value of the type of `value`. The member `ptr` of
the return value points to the first character not matching the pattern,
or has the value `last` if all characters match. If the parsed value is
not in the range representable by the type of `value`, `value` is
unmodified and the member `ec` of the return value is equal to
`errc::result_out_of_range`. Otherwise, `value` is set to the parsed
value, after rounding according to `round_to_nearest` [[round.style]],
and the member `ec` is value-initialized.

``` cpp
from_chars_result from_chars(const char* first, const char* last,
                             see below& value, int base = 10);
```

*Preconditions:* `base` has a value between 2 and 36 (inclusive).

*Effects:* The pattern is the expected form of the subject sequence in
the `"C"` locale for the given nonzero base, as described for `strtol`,
except that no `"0x"` or `"0X"` prefix shall appear if the value of
`base` is 16, and except that `’-’` is the only sign that may appear,
and only if `value` has a signed type.

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

*Preconditions:* `fmt` has the value of one of the enumerators of
`chars_format`.

*Effects:* The pattern is the expected form of the subject sequence in
the `"C"` locale, as described for `strtod`, except that

- the sign `’+’` may only appear in the exponent part;
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

See also: ISO C 7.22.1.3, 7.22.1.4

## Formatting <a id="format">[[format]]</a>

### Header `<format>` synopsis <a id="format.syn">[[format.syn]]</a>

``` cpp
namespace std {
  // [format.functions], formatting functions
  template<class... Args>
    string format(string_view fmt, const Args&... args);
  template<class... Args>
    wstring format(wstring_view fmt, const Args&... args);
  template<class... Args>
    string format(const locale& loc, string_view fmt, const Args&... args);
  template<class... Args>
    wstring format(const locale& loc, wstring_view fmt, const Args&... args);

  string vformat(string_view fmt, format_args args);
  wstring vformat(wstring_view fmt, wformat_args args);
  string vformat(const locale& loc, string_view fmt, format_args args);
  wstring vformat(const locale& loc, wstring_view fmt, wformat_args args);

  template<class Out, class... Args>
    Out format_to(Out out, string_view fmt, const Args&... args);
  template<class Out, class... Args>
    Out format_to(Out out, wstring_view fmt, const Args&... args);
  template<class Out, class... Args>
    Out format_to(Out out, const locale& loc, string_view fmt, const Args&... args);
  template<class Out, class... Args>
    Out format_to(Out out, const locale& loc, wstring_view fmt, const Args&... args);

  template<class Out>
    Out vformat_to(Out out, string_view fmt,
                   format_args_t<type_identity_t<Out>, char> args);
  template<class Out>
    Out vformat_to(Out out, wstring_view fmt,
                   format_args_t<type_identity_t<Out>, wchar_t> args);
  template<class Out>
    Out vformat_to(Out out, const locale& loc, string_view fmt,
                   format_args_t<type_identity_t<Out>, char> args);
  template<class Out>
    Out vformat_to(Out out, const locale& loc, wstring_view fmt,
                   format_args_t<type_identity_t<Out>, wchar_t> args);

  template<class Out> struct format_to_n_result {
    Out out;
    iter_difference_t<Out> size;
  };
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        string_view fmt, const Args&... args);
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        wstring_view fmt, const Args&... args);
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        const locale& loc, string_view fmt,
                                        const Args&... args);
  template<class Out, class... Args>
    format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                        const locale& loc, wstring_view fmt,
                                        const Args&... args);

  template<class... Args>
    size_t formatted_size(string_view fmt, const Args&... args);
  template<class... Args>
    size_t formatted_size(wstring_view fmt, const Args&... args);
  template<class... Args>
    size_t formatted_size(const locale& loc, string_view fmt, const Args&... args);
  template<class... Args>
    size_t formatted_size(const locale& loc, wstring_view fmt, const Args&... args);

  // [format.formatter], formatter
  template<class T, class charT = char> struct formatter;

  // [format.parse.ctx], class template basic_format_parse_context
  template<class charT> class basic_format_parse_context;
  using format_parse_context = basic_format_parse_context<char>;
  using wformat_parse_context = basic_format_parse_context<wchar_t>;

  template<class Out, class charT> class basic_format_context;
  using format_context = basic_format_context<unspecified, char>;
  using wformat_context = basic_format_context<unspecified, wchar_t>;

  // [format.arguments], arguments
  // [format.arg], class template basic_format_arg
  template<class Context> class basic_format_arg;

  template<class Visitor, class Context>
    see below visit_format_arg(Visitor&& vis, basic_format_arg<Context> arg);

  // [format.arg.store], class template format-arg-store
  template<class Context, class... Args> struct format-arg-store;      // exposition only

  template<class Context = format_context, class... Args>
    format-arg-store<Context, Args...>
      make_format_args(const Args&... args);
  template<class... Args>
    format-arg-store<wformat_context, Args...>
      make_wformat_args(const Args&... args);

  // [format.args], class template basic_format_args
  template<class Context> class basic_format_args;
  using format_args = basic_format_args<format_context>;
  using wformat_args = basic_format_args<wformat_context>;

  template<class Out, class charT>
    using format_args_t = basic_format_args<basic_format_context<Out, charT>>;

  // [format.error], class format_error
  class format_error;
}
```

The class template `format_to_n_result` has the template parameters,
data members, and special members specified above. It has no base
classes or members other than those specified.

### Format string <a id="format.string">[[format.string]]</a>

#### In general <a id="format.string.general">[[format.string.general]]</a>

A *format string* for arguments `args` is a (possibly empty) sequence of
*replacement fields*, *escape sequences*, and characters other than `{`
and `}`. Let `charT` be the character type of the format string. Each
character that is not part of a replacement field or an escape sequence
is copied unchanged to the output. An escape sequence is one of `{{` or
`}}`. It is replaced with `{` or `}`, respectively, in the output. The
syntax of replacement fields is as follows:

``` bnf
replacement-field
    '{' arg-idₒₚₜ format-specifierₒₚₜ '}'
```

``` bnf
arg-id
    '0'
    positive-integer
```

``` bnf
positive-integer
    nonzero-digit
    positive-integer digit
```

``` bnf
nonnegative-integer
    digit
    nonnegative-integer digit
```

``` bnf
nonzero-digit one of
    '1 2 3 4 5 6 7 8 9'
```

``` bnf
digit one of
    '0 1 2 3 4 5 6 7 8 9'
```

``` bnf
format-specifier
    ':' format-spec
```

``` bnf
format-spec
    as specified by the formatter specialization for the argument type
```

The *arg-id* field specifies the index of the argument in `args` whose
value is to be formatted and inserted into the output instead of the
replacement field. If there is no argument with the index *arg-id* in
`args`, the string is not a format string for `args`. The optional
*format-specifier* field explicitly specifies a format for the
replacement value.

[*Example 1*:

``` cpp
string s = format("{0}-{{", 8);         // value of s is "8-{"
```

— *end example*]

If all *arg-id*s in a format string are omitted (including those in the
*format-spec*, as interpreted by the corresponding `formatter`
specialization), argument indices 0, 1, 2, … will automatically be used
in that order. If some *arg-id*s are omitted and some are present, the
string is not a format string.

[*Note 1*: A format string cannot contain a mixture of automatic and
manual indexing. — *end note*]

[*Example 2*:

``` cpp
string s0 = format("{} to {}",   "a", "b"); // OK, automatic indexing
string s1 = format("{1} to {0}", "a", "b"); // OK, manual indexing
string s2 = format("{0} to {}",  "a", "b"); // not a format string (mixing automatic and manual indexing),
                                            // throws format_error
string s3 = format("{} to {1}",  "a", "b"); // not a format string (mixing automatic and manual indexing),
                                            // throws format_error
```

— *end example*]

The *format-spec* field contains *format specifications* that define how
the value should be presented. Each type can define its own
interpretation of the *format-spec* field. If *format-spec* does not
conform to the format specifications for the argument type referred to
by *arg-id*, the string is not a format string for `args`.

[*Example 3*:

- For arithmetic, pointer, and string types the *format-spec* is
  interpreted as a *std-format-spec* as described in
  [[format.string.std]].
- For chrono types the *format-spec* is interpreted as a
  *chrono-format-spec* as described in [[time.format]].
- For user-defined `formatter` specializations, the behavior of the
  `parse` member function determines how the *format-spec* is
  interpreted.

— *end example*]

#### Standard format specifiers <a id="format.string.std">[[format.string.std]]</a>

Each `formatter` specializations described in [[format.formatter.spec]]
for fundamental and string types interprets *format-spec* as a
*std-format-spec*.

[*Note 1*: The format specification can be used to specify such details
as field width, alignment, padding, and decimal precision. Some of the
formatting options are only supported for arithmetic
types. — *end note*]

The syntax of format specifications is as follows:

``` bnf
std-format-spec
    fill-and-alignₒₚₜ signₒₚₜ '#'ₒₚₜ '0'ₒₚₜ widthₒₚₜ precisionₒₚₜ 'L'ₒₚₜ typeₒₚₜ
```

``` bnf
fill-and-align
    fillₒₚₜ align
```

``` bnf
fill
    any character other than \{ or \}
```

``` bnf
align one of
    '< > ^'
```

``` bnf
sign one of
    '+ -' space
```

``` bnf
width
    positive-integer
    '{' arg-idₒₚₜ '}'
```

``` bnf
precision
    '.' nonnegative-integer
    '.' '{' arg-idₒₚₜ '}'
```

``` bnf
type one of
    'a A b B c d e E f F g G o p s x X'
```

[*Note 2*: The *fill* character can be any character other than `{` or
`}`. The presence of a fill character is signaled by the character
following it, which must be one of the alignment options. If the second
character of *std-format-spec* is not a valid alignment option, then it
is assumed that both the fill character and the alignment option are
absent. — *end note*]

The *align* specifier applies to all argument types. The meaning of the
various alignment options is as specified in [[format.align]].

[*Example 1*:

``` cpp
char c = 120;
string s0 = format("{:6}", 42);         // value of s0 is "\ \ \ \ 42"
string s1 = format("{:6}", 'x');        // value of s1 is "x\ \ \ \ \ "
string s2 = format("{:*<6}", 'x');      // value of s2 is "x*****"
string s3 = format("{:*>6}", 'x');      // value of s3 is "*****x"
string s4 = format("{:*^6}", 'x');      // value of s4 is "**x***"
string s5 = format("{:6d}", c);         // value of s5 is "\ \ \ 120"
string s6 = format("{:6}", true);       // value of s6 is "true\ \ "
```

— *end example*]

[*Note 3*: Unless a minimum field width is defined, the field width is
determined by the size of the content and the alignment option has no
effect. — *end note*]

**Table: Meaning of align options** <a id="format.align">[format.align]</a>

| Option | Meaning                                                                                                                                                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<`    | Forces the field to be aligned to the start of the available space. This is the default for non-arithmetic types, `charT`, and `bool`, unless an integer presentation type is specified.                                                                            |
| % `>`  | Forces the field to be aligned to the end of the available space. This is the default for arithmetic types other than `charT` and `bool` or when an integer presentation type is specified.                                                                         |
| % `^`  | Forces the field to be centered within the available space by inserting $\bigl\lfloor \frac{n}{2} \bigr\rfloor$ characters before and $\bigl\lceil \frac{n}{2} \bigr\rceil$ characters after the value, where $n$ is the total number of fill characters to insert. |


The *sign* option is only valid for arithmetic types other than `charT`
and `bool` or when an integer presentation type is specified. The
meaning of the various options is as specified in [[format.sign]].

[*Note 4*: For negative numbers and negative zero the output of
`to_chars` will already contain the sign so no additional transformation
is performed. — *end note*]

The *sign* option applies to floating-point infinity and NaN.

[*Example 2*:

``` cpp
double inf = numeric_limits<double>::infinity();
double nan = numeric_limits<double>::quiet_NaN();
string s0 = format("{0:},{0:+},{0:-},{0: }", 1);        // value of s0 is "1,+1,1, 1"
string s1 = format("{0:},{0:+},{0:-},{0: }", -1);       // value of s1 is "-1,-1,-1,-1"
string s2 = format("{0:},{0:+},{0:-},{0: }", inf);      // value of s2 is "inf,+inf,inf, inf"
string s3 = format("{0:},{0:+},{0:-},{0: }", nan);      // value of s3 is "nan,+nan,nan, nan"
```

— *end example*]

The `#` option causes the *alternate form* to be used for the
conversion. This option is valid for arithmetic types other than `charT`
and `bool` or when an integer presentation type is specified, and not
otherwise. For integral types, the alternate form inserts the base
prefix (if any) specified in [[format.type.int]] into the output after
the sign character (possibly space) if there is one, or before the
output of `to_chars` otherwise. For floating-point types, the alternate
form causes the result of the conversion of finite values to always
contain a decimal-point character, even if no digits follow it.
Normally, a decimal-point character appears in the result of these
conversions only if a digit follows it. In addition, for `g` and `G`
conversions, trailing zeros are not removed from the result.

If `{ \opt{arg-id} }` is used in a *width* or *precision*, the value of
the corresponding formatting argument is used in its place. If the
corresponding formatting argument is not of integral type, or its value
is negative for *precision* or non-positive for *width*, an exception of
type `format_error` is thrown.

The *positive-integer* in *width* is a decimal integer defining the
minimum field width. If *width* is not specified, there is no minimum
field width, and the field width is determined based on the content of
the field.

The *width* of a string is defined as the estimated number of column
positions appropriate for displaying it in a terminal.

[*Note 5*: This is similar to the semantics of the POSIX `wcswidth`
function. — *end note*]

For the purposes of width computation, a string is assumed to be in a
locale-independent, implementation-defined encoding. Implementations
should use a Unicode encoding on platforms capable of displaying Unicode
text in a terminal.

[*Note 6*: This is the case for Windows-based and many POSIX-based
operating systems. — *end note*]

For a string in a Unicode encoding, implementations should estimate the
width of a string as the sum of estimated widths of the first code
points in its extended grapheme clusters. The extended grapheme clusters
of a string are defined by UAX \#29. The estimated width of the
following code points is 2:

- `U+1100-U+115F`
- `U+2329-U+232A`
- `U+2E80-U+303E`
- `U+3040-U+A4CF`
- `U+AC00-U+D7A3`
- `U+F900-U+FAFF`
- `U+FE10-U+FE19`
- `U+FE30-U+FE6F`
- `U+FF00-U+FF60`
- `U+FFE0-U+FFE6`
- `U+1F300-U+1F64F`
- `U+1F900-U+1F9FF`
- `U+20000-U+2FFFD`
- `U+30000-U+3FFFD`

The estimated width of other code points is 1.

For a string in a non-Unicode encoding, the width of a string is
unspecified.

A zero (`0`) character preceding the *width* field pads the field with
leading zeros (following any indication of sign or base) to the field
width, except when applied to an infinity or NaN. This option is only
valid for arithmetic types other than `charT` and `bool` or when an
integer presentation type is specified. If the `0` character and an
*align* option both appear, the `0` character is ignored.

[*Example 3*:

``` cpp
char c = 120;
string s1 = format("{:+06d}", c);       // value of s1 is "+00120"
string s2 = format("{:#06x}", 0xa);     // value of s2 is "0x000a"
string s3 = format("{:<06}", -42);      // value of s3 is "-42\ \ \ " (0 is ignored because of < alignment)
```

— *end example*]

The *nonnegative-integer* in *precision* is a decimal integer defining
the precision or maximum field size. It can only be used with
floating-point and string types. For floating-point types this field
specifies the formatting precision. For string types, this field
provides an upper bound for the estimated width of the prefix of the
input string that is copied into the output. For a string in a Unicode
encoding, the formatter copies to the output the longest prefix of whole
extended grapheme clusters whose estimated width is no greater than the
precision.

When the `L` option is used, the form used for the conversion is called
the *locale-specific form*. The `L` option is only valid for arithmetic
types, and its effect depends upon the type.

- For integral types, the locale-specific form causes the context’s
  locale to be used to insert the appropriate digit group separator
  characters.
- For floating-point types, the locale-specific form causes the
  context’s locale to be used to insert the appropriate digit group and
  radix separator characters.
- For the textual representation of `bool`, the locale-specific form
  causes the context’s locale to be used to insert the appropriate
  string as if obtained with `numpunct::truename` or
  `numpunct::falsename`.

The *type* determines how the data should be presented.

The available string presentation types are specified in
[[format.type.string]].

**Table: Meaning of type options for strings** <a id="format.type.string">[format.type.string]</a>

| Type      | Meaning                          |
| --------- | -------------------------------- |
| none, `s` | Copies the string to the output. |


The meaning of some non-string presentation types is defined in terms of
a call to `to_chars`. In such cases, let \[`first`, `last`) be a range
large enough to hold the `to_chars` output and `value` be the formatting
argument value. Formatting is done as if by calling `to_chars` as
specified and copying the output through the output iterator of the
format context.

[*Note 7*: Additional padding and adjustments are performed prior to
copying the output through the output iterator as specified by the
format specifiers. — *end note*]

The available integer presentation types for integral types other than
`bool` and `charT` are specified in [[format.type.int]].

[*Example 4*:

``` cpp
string s0 = format("{}", 42);                           // value of s0 is "42"
string s1 = format("{0:b} {0:d} {0:o} {0:x}", 42);      // value of s1 is "101010 42 52 2a"
string s2 = format("{0:#x} {0:#X}", 42);                // value of s2 is "0x2a 0X2A"
string s3 = format("{:L}", 1234);                       // value of s3 might be "1,234"
                                                        // (depending on the locale)
```

— *end example*]

[*Note 8*: If the formatting argument type is `charT` or `bool`, the
default is instead `c` or `s`, respectively. — *end note*]

The available `charT` presentation types are specified in
[[format.type.char]].

**Table: Meaning of type options for `charT`** <a id="format.type.char">[format.type.char]</a>

| Type                           | Meaning                              |
| ------------------------------ | ------------------------------------ |
| none, `c`                      | Copies the character to the output.  |
| % `b`, `B`, `d`, `o`, `x`, `X` | As specified in [[format.type.int]]. |


The available `bool` presentation types are specified in
[[format.type.bool]].

**Table: Meaning of type options for `bool`** <a id="format.type.bool">[format.type.bool]</a>

| Type                                | Meaning                                                                                |
| ----------------------------------- | -------------------------------------------------------------------------------------- |
| none, `s`                           | Copies textual representation, either `true` or `false`, to the output.                |
| % `b`, `B`, `c`, `d`, `o`, `x`, `X` | As specified in [[format.type.int]] for the value `static_cast<unsigned char>(value)`. |


The available floating-point presentation types and their meanings for
values other than infinity and NaN are specified in
[[format.type.float]]. For lower-case presentation types, infinity and
NaN are formatted as `inf` and `nan`, respectively. For upper-case
presentation types, infinity and NaN are formatted as `INF` and `NAN`,
respectively.

[*Note 9*: In either case, a sign is included if indicated by the
*sign* option. — *end note*]

**Table: Meaning of type options for floating-point types** <a id="format.type.float">[format.type.float]</a>

| Type       | Meaning                                                                                                                                                                                                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `a`        | If precision is specified, equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::hex, precision) \end{codeblock} where `precision` is the specified formatting precision; equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::hex) \end{codeblock} otherwise. |
| % `A`      | The same as `a`, except that it uses uppercase letters for digits above 9 and `P` to indicate the exponent.                                                                                                                                                                                               |
| % `e`      | Equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::scientific, precision) \end{codeblock} where `precision` is the specified formatting precision, or `6` if precision is not specified.                                                                                          |
| % `E`      | The same as `e`, except that it uses `E` to indicate exponent.                                                                                                                                                                                                                                            |
| % `f`, `F` | Equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::fixed, precision) \end{codeblock} where `precision` is the specified formatting precision, or `6` if precision is not specified.                                                                                               |
| % `g`      | Equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::general, precision) \end{codeblock} where `precision` is the specified formatting precision, or `6` if precision is not specified.                                                                                             |
| % `G`      | The same as `g`, except that it uses `E` to indicate exponent.                                                                                                                                                                                                                                            |
| % none     | If precision is specified, equivalent to \begin{codeblock} to_chars(first, last, value, chars_format::general, precision) \end{codeblock} where `precision` is the specified formatting precision; equivalent to \begin{codeblock} to_chars(first, last, value) \end{codeblock} otherwise.                |


The available pointer presentation types and their mapping to `to_chars`
are specified in [[format.type.ptr]].

[*Note 10*: Pointer presentation types also apply to
`nullptr_t`. — *end note*]

**Table: Meaning of type options for pointer types** <a id="format.type.ptr">[format.type.ptr]</a>

| Type      | Meaning                                                                                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| none, `p` | If `uintptr_t` is defined, \begin{codeblock} to_chars(first, last, reinterpret_cast<uintptr_t>(value), 16) \end{codeblock} with the prefix `0x` added to the output; otherwise, implementation-defined. |


### Error reporting <a id="format.err.report">[[format.err.report]]</a>

Formatting functions throw `format_error` if an argument `fmt` is passed
that is not a format string for `args`. They propagate exceptions thrown
by operations of `formatter` specializations and iterators. Failure to
allocate storage is reported by throwing an exception as described in 
[[res.on.exception.handling]].

### Formatting functions <a id="format.functions">[[format.functions]]</a>

In the description of the functions, operator `+` is used for some of
the iterator categories for which it does not have to be defined. In
these cases the semantics of `a + n` are the same as in
[[algorithms.requirements]].

``` cpp
template<class... Args>
  string format(string_view fmt, const Args&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(fmt, make_format_args(args...));
```

``` cpp
template<class... Args>
  wstring format(wstring_view fmt, const Args&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(fmt, make_wformat_args(args...));
```

``` cpp
template<class... Args>
  string format(const locale& loc, string_view fmt, const Args&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(loc, fmt, make_format_args(args...));
```

``` cpp
template<class... Args>
  wstring format(const locale& loc, wstring_view fmt, const Args&... args);
```

*Effects:* Equivalent to:

``` cpp
return vformat(loc, fmt, make_wformat_args(args...));
```

``` cpp
string vformat(string_view fmt, format_args args);
wstring vformat(wstring_view fmt, wformat_args args);
string vformat(const locale& loc, string_view fmt, format_args args);
wstring vformat(const locale& loc, wstring_view fmt, wformat_args args);
```

*Returns:* A string object holding the character representation of
formatting arguments provided by `args` formatted according to
specifications given in `fmt`. If present, `loc` is used for
locale-specific formatting.

*Throws:* As specified in  [[format.err.report]].

``` cpp
template<class Out, class... Args>
  Out format_to(Out out, string_view fmt, const Args&... args);
template<class Out, class... Args>
  Out format_to(Out out, wstring_view fmt, const Args&... args);
```

*Effects:* Equivalent to:

``` cpp
using context = basic_format_context<Out, decltype(fmt)::value_type>;
return vformat_to(out, fmt, make_format_args<context>(args...));
```

``` cpp
template<class Out, class... Args>
  Out format_to(Out out, const locale& loc, string_view fmt, const Args&... args);
template<class Out, class... Args>
  Out format_to(Out out, const locale& loc, wstring_view fmt, const Args&... args);
```

*Effects:* Equivalent to:

``` cpp
using context = basic_format_context<Out, decltype(fmt)::value_type>;
return vformat_to(out, loc, fmt, make_format_args<context>(args...));
```

``` cpp
template<class Out>
  Out vformat_to(Out out, string_view fmt,
                 format_args_t<type_identity_t<Out>, char> args);
template<class Out>
  Out vformat_to(Out out, wstring_view fmt,
                 format_args_t<type_identity_t<Out>, wchar_t> args);
template<class Out>
  Out vformat_to(Out out, const locale& loc, string_view fmt,
                 format_args_t<type_identity_t<Out>, char> args);
template<class Out>
  Out vformat_to(Out out, const locale& loc, wstring_view fmt,
                 format_args_t<type_identity_t<Out>, wchar_t> args);
```

Let `charT` be `decltype(fmt)::value_type`.

*Constraints:* `Out` satisfies `output_iterator<const charT&>`.

*Preconditions:* `Out` models `output_iterator<const charT&>`.

*Effects:* Places the character representation of formatting the
arguments provided by `args`, formatted according to the specifications
given in `fmt`, into the range \[`out`, `out + N`), where `N` is
`formatted_size(fmt, args...)` for the functions without a `loc`
parameter and `formatted_size(loc, fmt, args...)` for the functions with
a `loc` parameter. If present, `loc` is used for locale-specific
formatting.

*Returns:* `out + N`.

*Throws:* As specified in  [[format.err.report]].

``` cpp
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      string_view fmt, const Args&... args);
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      wstring_view fmt, const Args&... args);
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      const locale& loc, string_view fmt,
                                      const Args&... args);
template<class Out, class... Args>
  format_to_n_result<Out> format_to_n(Out out, iter_difference_t<Out> n,
                                      const locale& loc, wstring_view fmt,
                                      const Args&... args);
```

Let

- `charT` be `decltype(fmt)::value_type`,
- `N` be `formatted_size(fmt, args...)` for the functions without a
  `loc` parameter and `formatted_size(loc, fmt, args...)` for the
  functions with a `loc` parameter, and
- `M` be `clamp(n, 0, N)`.

*Constraints:* `Out` satisfies `output_iterator<const charT&>`.

*Preconditions:* `Out` models `output_iterator<const charT&>`, and
`formatter<``Tᵢ``, charT>` meets the
requirements [[formatter.requirements]] for each `Tᵢ` in `Args`.

*Effects:* Places the first `M` characters of the character
representation of formatting the arguments provided by `args`, formatted
according to the specifications given in `fmt`, into the range \[`out`,
`out + M`). If present, `loc` is used for locale-specific formatting.

*Returns:* `{out + M, N}`.

*Throws:* As specified in  [[format.err.report]].

``` cpp
template<class... Args>
  size_t formatted_size(string_view fmt, const Args&... args);
template<class... Args>
  size_t formatted_size(wstring_view fmt, const Args&... args);
template<class... Args>
  size_t formatted_size(const locale& loc, string_view fmt, const Args&... args);
template<class... Args>
  size_t formatted_size(const locale& loc, wstring_view fmt, const Args&... args);
```

Let `charT` be `decltype(fmt)::value_type`.

*Preconditions:* `formatter<``Tᵢ``, charT>` meets the
requirements [[formatter.requirements]] for each `Tᵢ` in `Args`.

*Returns:* The number of characters in the character representation of
formatting arguments `args` formatted according to specifications given
in `fmt`. If present, `loc` is used for locale-specific formatting.

*Throws:* As specified in  [[format.err.report]].

### Formatter <a id="format.formatter">[[format.formatter]]</a>

#### Formatter requirements <a id="formatter.requirements">[[formatter.requirements]]</a>

A type `F` meets the requirements if:

- it meets the
  - *Cpp17DefaultConstructible* ([[cpp17.defaultconstructible]]),
  - *Cpp17CopyConstructible* ([[cpp17.copyconstructible]]),
  - *Cpp17CopyAssignable* ([[cpp17.copyassignable]]), and
  - *Cpp17Destructible* ([[cpp17.destructible]])

  requirements,
- it is swappable [[swappable.requirements]] for lvalues, and
- the expressions shown in [[formatter]] are valid and have the
  indicated semantics.

Given character type `charT`, output iterator type `Out`, and formatting
argument type `T`, in [[formatter]]:

- `f` is a value of type `F`,
- `u` is an lvalue of type `T`,
- `t` is a value of a type convertible to (possibly const) `T`,
- `PC` is `basic_format_parse_context<charT>`,
- `FC` is `basic_format_context<Out, charT>`,
- `pc` is an lvalue of type `PC`, and
- `fc` is an lvalue of type `FC`.

`pc.begin()` points to the beginning of the *format-spec*
[[format.string]] of the replacement field being formatted in the format
string. If *format-spec* is empty then either `pc.begin() == pc.end()`
or `*pc.begin() == '}'`.

[*Note 1*: This allows formatters to emit meaningful error
messages. — *end note*]

#### Formatter specializations <a id="format.formatter.spec">[[format.formatter.spec]]</a>

The functions defined in [[format.functions]] use specializations of the
class template `formatter` to format individual arguments.

Let `charT` be either `char` or `wchar_t`. Each specialization of
`formatter` is either enabled or disabled, as described below.

[*Note 1*: Enabled specializations meet the requirements, and disabled
specializations do not. — *end note*]

Each header that declares the template `formatter` provides the
following enabled specializations:

- The specializations
  ``` cpp
  template<> struct formatter<char, char>;
  template<> struct formatter<char, wchar_t>;
  template<> struct formatter<wchar_t, wchar_t>;
  ```
- For each `charT`, the string type specializations
  ``` cpp
  template<> struct formatter<charT*, charT>;
  template<> struct formatter<const charT*, charT>;
  template<size_t N> struct formatter<const charT[N], charT>;
  template<class traits, class Allocator>
    struct formatter<basic_string<charT, traits, Allocator>, charT>;
  template<class traits>
    struct formatter<basic_string_view<charT, traits>, charT>;
  ```
- For each `charT`, for each cv-unqualified arithmetic type
  `ArithmeticT` other than `char`, `wchar_t`, `char8_t`, `char16_t`, or
  `char32_t`, a specialization
  ``` cpp
  template<> struct formatter<ArithmeticT, charT>;
  ```
- For each `charT`, the pointer type specializations
  ``` cpp
  template<> struct formatter<nullptr_t, charT>;
  template<> struct formatter<void*, charT>;
  template<> struct formatter<const void*, charT>;
  ```

The `parse` member functions of these formatters interpret the format
specification as a *std-format-spec* as described in
[[format.string.std]].

[*Note 2*: Specializations such as `formatter<wchar_t, char>` and
`formatter<const char*, wchar_t>` that would require implicit multibyte
/ wide string or character conversion are disabled. — *end note*]

For any types `T` and `charT` for which neither the library nor the user
provides an explicit or partial specialization of the class template
`formatter`, `formatter<T, charT>` is disabled.

If the library provides an explicit or partial specialization of
`formatter<T, charT>`, that specialization is enabled except as noted
otherwise.

If `F` is a disabled specialization of `formatter`, these values are
`false`:

- `is_default_constructible_v<F>`,
- `is_copy_constructible_v<F>`,
- `is_move_constructible_v<F>`,
- `is_copy_assignable_v<F>`, and
- `is_move_assignable_v<F>`.

An enabled specialization `formatter<T, charT>` meets the requirements
[[formatter.requirements]].

[*Example 1*:

``` cpp
#include <format>

enum color { red, green, blue };
const char* color_names[] = { "red", "green", "blue" };

template<> struct std::formatter<color> : std::formatter<const char*> {
  auto format(color c, format_context& ctx) {
    return formatter<const char*>::format(color_names[c], ctx);
  }
};

struct err {};

std::string s0 = std::format("{}", 42);         // OK, library-provided formatter
std::string s1 = std::format("{}", L"foo");     // error: disabled formatter
std::string s2 = std::format("{}", red);        // OK, user-provided formatter
std::string s3 = std::format("{}", err{});      // error: disabled formatter
```

— *end example*]

#### Class template `basic_format_parse_context` <a id="format.parse.ctx">[[format.parse.ctx]]</a>

``` cpp
namespace std {
  template<class charT>
  class basic_format_parse_context {
  public:
    using char_type = charT;
    using const_iterator = typename basic_string_view<charT>::const_iterator;
    using iterator = const_iterator;

  private:
    iterator begin_;                                    // exposition only
    iterator end_;                                      // exposition only
    enum indexing { unknown, manual, automatic };       // exposition only
    indexing indexing_;                                 // exposition only
    size_t next_arg_id_;                                // exposition only
    size_t num_args_;                                   // exposition only

  public:
    constexpr explicit basic_format_parse_context(basic_string_view<charT> fmt,
                                                  size_t num_args = 0) noexcept;
    basic_format_parse_context(const basic_format_parse_context&) = delete;
    basic_format_parse_context& operator=(const basic_format_parse_context&) = delete;

    constexpr const_iterator begin() const noexcept;
    constexpr const_iterator end() const noexcept;
    constexpr void advance_to(const_iterator it);

    constexpr size_t next_arg_id();
    constexpr void check_arg_id(size_t id);
  };
}
```

An instance of `basic_format_parse_context` holds the format string
parsing state consisting of the format string range being parsed and the
argument counter for automatic indexing.

``` cpp
constexpr explicit basic_format_parse_context(basic_string_view<charT> fmt,
                                              size_t num_args = 0) noexcept;
```

*Effects:* Initializes `begin_` with `fmt.begin()`, `end_` with
`fmt.end()`, `indexing_` with `unknown`, `next_arg_id_` with `0`, and
`num_args_` with `num_args`.

``` cpp
constexpr const_iterator begin() const noexcept;
```

*Returns:* `begin_`.

``` cpp
constexpr const_iterator end() const noexcept;
```

*Returns:* `end_`.

``` cpp
constexpr void advance_to(const_iterator it);
```

*Preconditions:* `end()` is reachable from `it`.

*Effects:* Equivalent to: `begin_ = it;`

``` cpp
constexpr size_t next_arg_id();
```

*Effects:* If `indexing_ != manual`, equivalent to:

``` cpp
if (indexing_ == unknown)
  indexing_ = automatic;
return next_arg_id_++;
```

*Throws:* `format_error` if `indexing_ == manual` which indicates mixing
of automatic and manual argument indexing.

``` cpp
constexpr void check_arg_id(size_t id);
```

*Effects:* If `indexing_ != automatic`, equivalent to:

``` cpp
if (indexing_ == unknown)
  indexing_ = manual;
```

*Throws:* `format_error` if `indexing_ == automatic` which indicates
mixing of automatic and manual argument indexing.

*Remarks:* Call expressions where `id >= num_args_` are not core
constant expressions [[expr.const]].

#### Class template `basic_format_context` <a id="format.context">[[format.context]]</a>

``` cpp
namespace std {
  template<class Out, class charT>
  class basic_format_context {
    basic_format_args<basic_format_context> args_;      // exposition only
    Out out_;                                           // exposition only

  public:
    using iterator = Out;
    using char_type = charT;
    template<class T> using formatter_type = formatter<T, charT>;

    basic_format_arg<basic_format_context> arg(size_t id) const;
    std::locale locale();

    iterator out();
    void advance_to(iterator it);
  };
}
```

An instance of `basic_format_context` holds formatting state consisting
of the formatting arguments and the output iterator.

`Out` shall model `output_iterator<const charT&>`.

`format_context` is an alias for a specialization of
`basic_format_context` with an output iterator that appends to `string`,
such as `back_insert_iterator<string>`. Similarly, `wformat_context` is
an alias for a specialization of `basic_format_context` with an output
iterator that appends to `wstring`.

[*Note 1*: For a given type `charT`, implementations are encouraged to
provide a single instantiation of `basic_format_context` for appending
to `basic_string<charT>`, `vector<charT>`, or any other container with
contiguous storage by wrapping those in temporary objects with a uniform
interface (such as a `span<charT>`) and polymorphic
reallocation. — *end note*]

``` cpp
basic_format_arg<basic_format_context> arg(size_t id) const;
```

*Returns:* `args_.get(id)`.

``` cpp
std::locale locale();
```

*Returns:* The locale passed to the formatting function if the latter
takes one, and `std::locale()` otherwise.

``` cpp
iterator out();
```

*Returns:* `out_`.

``` cpp
void advance_to(iterator it);
```

*Effects:* Equivalent to: `out_ = it;`

[*Example 1*:

``` cpp
struct S { int value; };

template<> struct std::formatter<S> {
  size_t width_arg_id = 0;

  // Parses a width argument id in the format { digit }.
  constexpr auto parse(format_parse_context& ctx) {
    auto iter = ctx.begin();
    auto get_char = [&]() { return iter != ctx.end() ? *iter : 0; };
    if (get_char() != '{')
      return iter;
    ++iter;
    char c = get_char();
    if (!isdigit(c) || (++iter, get_char()) != '}')
      throw format_error("invalid format");
    width_arg_id = c - '0';
    ctx.check_arg_id(width_arg_id);
    return ++iter;
  }

  // Formats an S with width given by the argument width_arg_id.
  auto format(S s, format_context& ctx) {
    int width = visit_format_arg([](auto value) -> int {
      if constexpr (!is_integral_v<decltype(value)>)
        throw format_error("width is not integral");
      else if (value < 0 || value > numeric_limits<int>::max())
        throw format_error("invalid width");
      else
        return value;
      }, ctx.arg(width_arg_id));
    return format_to(ctx.out(), "{0:x<{1}}", s.value, width);
  }
};

std::string s = std::format("{0:{1}}", S{42}, 10);  // value of s is "xxxxxxxx42"
```

— *end example*]

### Arguments <a id="format.arguments">[[format.arguments]]</a>

#### Class template `basic_format_arg` <a id="format.arg">[[format.arg]]</a>

``` cpp
namespace std {
  template<class Context>
  class basic_format_arg {
  public:
    class handle;

  private:
    using char_type = typename Context::char_type;                              // exposition only

    variant<monostate, bool, char_type,
            int, unsigned int, long long int, unsigned long long int,
            float, double, long double,
            const char_type*, basic_string_view<char_type>,
            const void*, handle> value;                                         // exposition only

    template<class T> explicit basic_format_arg(const T& v) noexcept;           // exposition only
    explicit basic_format_arg(float n) noexcept;                                // exposition only
    explicit basic_format_arg(double n) noexcept;                               // exposition only
    explicit basic_format_arg(long double n) noexcept;                          // exposition only
    explicit basic_format_arg(const char_type* s);                              // exposition only

    template<class traits>
      explicit basic_format_arg(
        basic_string_view<char_type, traits> s) noexcept;                       // exposition only

    template<class traits, class Allocator>
      explicit basic_format_arg(
        const basic_string<char_type, traits, Allocator>& s) noexcept;          // exposition only

    explicit basic_format_arg(nullptr_t) noexcept;                              // exposition only

    template<class T>
      explicit basic_format_arg(const T* p) noexcept;                           // exposition only

  public:
    basic_format_arg() noexcept;

    explicit operator bool() const noexcept;
  };
}
```

An instance of `basic_format_arg` provides access to a formatting
argument for user-defined formatters.

The behavior of a program that adds specializations of
`basic_format_arg` is undefined.

``` cpp
basic_format_arg() noexcept;
```

*Ensures:* `!(*this)`.

``` cpp
template<class T> explicit basic_format_arg(const T& v) noexcept;
```

*Constraints:* The template specialization

``` cpp
typename Context::template formatter_type<T>
```

meets the requirements [[formatter.requirements]]. The extent to which
an implementation determines that the specialization meets the
requirements is unspecified, except that as a minimum the expression

``` cpp
typename Context::template formatter_type<T>()
  .format(declval<const T&>(), declval<Context&>())
```

shall be well-formed when treated as an unevaluated operand.

*Effects:*

- if `T` is `bool` or `char_type`, initializes `value` with `v`;
- otherwise, if `T` is `char` and `char_type` is `wchar_t`, initializes
  `value` with `static_cast<wchar_t>(v)`;
- otherwise, if `T` is a signed integer type [[basic.fundamental]] and
  `sizeof(T) <= sizeof(int)`, initializes `value` with
  `static_cast<int>(v)`;
- otherwise, if `T` is an unsigned integer type and
  `sizeof(T) <= sizeof(unsigned int)`, initializes `value` with
  `static_cast<unsigned int>(v)`;
- otherwise, if `T` is a signed integer type and
  `sizeof(T) <= sizeof(long long int)`, initializes `value` with
  `static_cast<long long int>(v)`;
- otherwise, if `T` is an unsigned integer type and
  `sizeof(T) <= sizeof(unsigned long long int)`, initializes `value`
  with `static_cast<unsigned long long int>(v)`;
- otherwise, initializes `value` with `handle(v)`.

``` cpp
explicit basic_format_arg(float n) noexcept;
explicit basic_format_arg(double n) noexcept;
explicit basic_format_arg(long double n) noexcept;
```

*Effects:* Initializes `value` with `n`.

``` cpp
explicit basic_format_arg(const char_type* s);
```

*Preconditions:* `s` points to a NTCTS [[defns.ntcts]].

*Effects:* Initializes `value` with `s`.

``` cpp
template<class traits>
  explicit basic_format_arg(basic_string_view<char_type, traits> s) noexcept;
```

*Effects:* Initializes `value` with `s`.

``` cpp
template<class traits, class Allocator>
  explicit basic_format_arg(
    const basic_string<char_type, traits, Allocator>& s) noexcept;
```

*Effects:* Initializes `value` with
`basic_string_view<char_type>(s.data(), s.size())`.

``` cpp
explicit basic_format_arg(nullptr_t) noexcept;
```

*Effects:* Initializes `value` with `static_cast<const void*>(nullptr)`.

``` cpp
template<class T> explicit basic_format_arg(const T* p) noexcept;
```

*Constraints:* `is_void_v<T>` is `true`.

*Effects:* Initializes `value` with `p`.

[*Note 1*: Constructing `basic_format_arg` from a pointer to a member
is ill-formed unless the user provides an enabled specialization of
`formatter` for that pointer to member type. — *end note*]

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `!holds_alternative<monostate>(value)`.

The class `handle` allows formatting an object of a user-defined type.

``` cpp
namespace std {
  template<class Context>
  class basic_format_arg<Context>::handle {
    const void* ptr_;                                           // exposition only
    void (*format_)(basic_format_parse_context<char_type>&,
                    Context&, const void*);                     // exposition only

    template<class T> explicit handle(const T& val) noexcept;   // exposition only

    friend class basic_format_arg<Context>;                     // exposition only

  public:
    void format(basic_format_parse_context<char_type>&, Context& ctx) const;
  };
}
```

``` cpp
template<class T> explicit handle(const T& val) noexcept;
```

*Effects:* Initializes `ptr_` with `addressof(val)` and `format_` with

``` cpp
[](basic_format_parse_context<char_type>& parse_ctx,
   Context& format_ctx, const void* ptr) {
  typename Context::template formatter_type<T> f;
  parse_ctx.advance_to(f.parse(parse_ctx));
  format_ctx.advance_to(f.format(*static_cast<const T*>(ptr), format_ctx));
}
```

``` cpp
void format(basic_format_parse_context<char_type>& parse_ctx, Context& format_ctx) const;
```

*Effects:* Equivalent to: `format_(parse_ctx, format_ctx, ptr_);`

``` cpp
template<class Visitor, class Context>
  see below visit_format_arg(Visitor&& vis, basic_format_arg<Context> arg);
```

*Effects:* Equivalent to:
`return visit(forward<Visitor>(vis), arg.value);`

#### Class template *`format-arg-store`* <a id="format.arg.store">[[format.arg.store]]</a>

``` cpp
namespace std {
  template<class Context, class... Args>
  struct format-arg-store {      // exposition only
    array<basic_format_arg<Context>, sizeof...(Args)> args;
  };
}
```

An instance of *`format-arg-store`* stores formatting arguments.

``` cpp
template<class Context = format_context, class... Args>
  format-arg-store<Context, Args...> make_format_args(const Args&... args);
```

*Preconditions:* The type
`typename Context::template formatter_type<``Tᵢ``>` meets the
requirements [[formatter.requirements]] for each `Tᵢ` in `Args`.

*Returns:* `{basic_format_arg<Context>(args)...}`.

``` cpp
template<class... Args>
  format-arg-store<wformat_context, Args...> make_wformat_args(const Args&... args);
```

*Effects:* Equivalent to:
`return make_format_args<wformat_context>(args...);`

#### Class template `basic_format_args` <a id="format.args">[[format.args]]</a>

``` cpp
namespace std {
  template<class Context>
  class basic_format_args {
    size_t size_;                               // exposition only
    const basic_format_arg<Context>* data_;     // exposition only

  public:
    basic_format_args() noexcept;

    template<class... Args>
      basic_format_args(const format-arg-store<Context, Args...>& store) noexcept;

    basic_format_arg<Context> get(size_t i) const noexcept;
  };
}
```

An instance of `basic_format_args` provides access to formatting
arguments.

``` cpp
basic_format_args() noexcept;
```

*Effects:* Initializes `size_` with `0`.

``` cpp
template<class... Args>
  basic_format_args(const format-arg-store<Context, Args...>& store) noexcept;
```

*Effects:* Initializes `size_` with `sizeof...(Args)` and `data_` with
`store.args.data()`.

``` cpp
basic_format_arg<Context> get(size_t i) const noexcept;
```

*Returns:* `i < size_ ? data_[i] : basic_format_arg<Context>()`.

[*Note 1*: Implementations are encouraged to optimize the
representation of `basic_format_args` for small number of formatting
arguments by storing indices of type alternatives separately from values
and packing the former. — *end note*]

### Class `format_error` <a id="format.error">[[format.error]]</a>

``` cpp
namespace std {
  class format_error : public runtime_error {
  public:
    explicit format_error(const string& what_arg);
    explicit format_error(const char* what_arg);
  };
}
```

The class `format_error` defines the type of objects thrown as
exceptions to report errors from the formatting library.

``` cpp
format_error(const string& what_arg);
```

*Ensures:* `strcmp(what(), what_arg.c_str()) == 0`.

``` cpp
format_error(const char* what_arg);
```

*Ensures:* `strcmp(what(), what_arg) == 0`.

<!-- Link reference definitions -->
[alg.sorting]: algorithms.md#alg.sorting
[algorithms]: algorithms.md#algorithms
[algorithms.general]: algorithms.md#algorithms.general
[algorithms.requirements]: algorithms.md#algorithms.requirements
[allocator.adaptor]: #allocator.adaptor
[allocator.adaptor.cnstr]: #allocator.adaptor.cnstr
[allocator.adaptor.members]: #allocator.adaptor.members
[allocator.adaptor.syn]: #allocator.adaptor.syn
[allocator.adaptor.types]: #allocator.adaptor.types
[allocator.globals]: #allocator.globals
[allocator.members]: #allocator.members
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
[any.bad.any.cast]: #any.bad.any.cast
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
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.def.odr]: basic.md#basic.def.odr
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.stc.dynamic.allocation]: basic.md#basic.stc.dynamic.allocation
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
[charconv]: #charconv
[charconv.from.chars]: #charconv.from.chars
[charconv.syn]: #charconv.syn
[charconv.to.chars]: #charconv.to.chars
[class.copy.ctor]: class.md#class.copy.ctor
[class.mem]: class.md#class.mem
[comparisons]: #comparisons
[comparisons.equal.to]: #comparisons.equal.to
[comparisons.greater]: #comparisons.greater
[comparisons.greater.equal]: #comparisons.greater.equal
[comparisons.less]: #comparisons.less
[comparisons.less.equal]: #comparisons.less.equal
[comparisons.not.equal.to]: #comparisons.not.equal.to
[comparisons.three.way]: #comparisons.three.way
[concepts.equality]: concepts.md#concepts.equality
[conv.array]: expr.md#conv.array
[conv.func]: expr.md#conv.func
[conv.lval]: expr.md#conv.lval
[conv.qual]: expr.md#conv.qual
[conv.rank]: basic.md#conv.rank
[cpp17.allocator]: #cpp17.allocator
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.copyconstructible]: #cpp17.copyconstructible
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[cpp17.hash]: #cpp17.hash
[cpp17.moveassignable]: #cpp17.moveassignable
[cpp17.moveconstructible]: #cpp17.moveconstructible
[cpp17.nullablepointer]: #cpp17.nullablepointer
[dcl.array]: dcl.md#dcl.array
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.ref]: dcl.md#dcl.ref
[declval]: #declval
[default.allocator]: #default.allocator
[defns.const.subexpr]: library.md#defns.const.subexpr
[defns.expression-equivalent]: library.md#defns.expression-equivalent
[defns.ntcts]: library.md#defns.ntcts
[defns.order.ptr]: #defns.order.ptr
[defns.referenceable]: library.md#defns.referenceable
[execpol]: #execpol
[execpol.general]: #execpol.general
[execpol.objects]: #execpol.objects
[execpol.par]: #execpol.par
[execpol.parunseq]: #execpol.parunseq
[execpol.seq]: #execpol.seq
[execpol.type]: #execpol.type
[execpol.unseq]: #execpol.unseq
[execution.syn]: #execution.syn
[expr.add]: expr.md#expr.add
[expr.alignof]: expr.md#expr.alignof
[expr.bit.and]: expr.md#expr.bit.and
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.eq]: expr.md#expr.eq
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.mul]: expr.md#expr.mul
[expr.or]: expr.md#expr.or
[expr.prop]: expr.md#expr.prop
[expr.rel]: expr.md#expr.rel
[expr.unary.op]: expr.md#expr.unary.op
[expr.xor]: expr.md#expr.xor
[format]: #format
[format.align]: #format.align
[format.arg]: #format.arg
[format.arg.store]: #format.arg.store
[format.args]: #format.args
[format.arguments]: #format.arguments
[format.context]: #format.context
[format.err.report]: #format.err.report
[format.error]: #format.error
[format.formatter]: #format.formatter
[format.formatter.spec]: #format.formatter.spec
[format.functions]: #format.functions
[format.parse.ctx]: #format.parse.ctx
[format.sign]: #format.sign
[format.string]: #format.string
[format.string.general]: #format.string.general
[format.string.std]: #format.string.std
[format.syn]: #format.syn
[format.type.bool]: #format.type.bool
[format.type.char]: #format.type.char
[format.type.float]: #format.type.float
[format.type.int]: #format.type.int
[format.type.ptr]: #format.type.ptr
[format.type.string]: #format.type.string
[formatter]: #formatter
[formatter.requirements]: #formatter.requirements
[forward]: #forward
[func.bind]: #func.bind
[func.bind.bind]: #func.bind.bind
[func.bind.front]: #func.bind.front
[func.bind.isbind]: #func.bind.isbind
[func.bind.isplace]: #func.bind.isplace
[func.bind.place]: #func.bind.place
[func.def]: #func.def
[func.identity]: #func.identity
[func.invoke]: #func.invoke
[func.memfn]: #func.memfn
[func.not.fn]: #func.not.fn
[func.require]: #func.require
[func.search]: #func.search
[func.search.bm]: #func.search.bm
[func.search.bmh]: #func.search.bmh
[func.search.default]: #func.search.default
[func.wrap]: #func.wrap
[func.wrap.badcall]: #func.wrap.badcall
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
[intro.multithread]: basic.md#intro.multithread
[intro.object]: basic.md#intro.object
[intseq]: #intseq
[intseq.general]: #intseq.general
[intseq.intseq]: #intseq.intseq
[intseq.make]: #intseq.make
[invalid.argument]: diagnostics.md#invalid.argument
[iostate.flags]: input.md#iostate.flags
[istream.formatted]: input.md#istream.formatted
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
[meta.const.eval]: #meta.const.eval
[meta.help]: #meta.help
[meta.logical]: #meta.logical
[meta.member]: #meta.member
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
[namespace.std]: library.md#namespace.std
[new.delete]: support.md#new.delete
[optional]: #optional
[optional.assign]: #optional.assign
[optional.assign.copy]: #optional.assign.copy
[optional.assign.copy.templ]: #optional.assign.copy.templ
[optional.assign.move]: #optional.assign.move
[optional.assign.move.templ]: #optional.assign.move.templ
[optional.bad.access]: #optional.bad.access
[optional.comp.with.t]: #optional.comp.with.t
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
[pointer.conversion]: #pointer.conversion
[pointer.traits]: #pointer.traits
[pointer.traits.functions]: #pointer.traits.functions
[pointer.traits.optmem]: #pointer.traits.optmem
[pointer.traits.types]: #pointer.traits.types
[ptr.align]: #ptr.align
[range.cmp]: #range.cmp
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
[res.on.exception.handling]: library.md#res.on.exception.handling
[round.style]: support.md#round.style
[scoped.adaptor.operators]: #scoped.adaptor.operators
[smartptr]: #smartptr
[special]: class.md#special
[specialized.addressof]: #specialized.addressof
[specialized.algorithms]: algorithms.md#specialized.algorithms
[stmt.dcl]: stmt.md#stmt.dcl
[stmt.return]: stmt.md#stmt.return
[support.signal]: support.md#support.signal
[swappable.requirements]: library.md#swappable.requirements
[temp.deduct]: temp.md#temp.deduct
[temp.param]: temp.md#temp.param
[temp.type]: temp.md#temp.type
[template.bitset]: #template.bitset
[time.format]: time.md#time.format
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
[unique.ptr]: #unique.ptr
[unique.ptr.create]: #unique.ptr.create
[unique.ptr.dltr]: #unique.ptr.dltr
[unique.ptr.dltr.dflt]: #unique.ptr.dltr.dflt
[unique.ptr.dltr.dflt1]: #unique.ptr.dltr.dflt1
[unique.ptr.dltr.general]: #unique.ptr.dltr.general
[unique.ptr.io]: #unique.ptr.io
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
[util.smartptr.enab]: #util.smartptr.enab
[util.smartptr.getdeleter]: #util.smartptr.getdeleter
[util.smartptr.hash]: #util.smartptr.hash
[util.smartptr.ownerless]: #util.smartptr.ownerless
[util.smartptr.shared]: #util.smartptr.shared
[util.smartptr.shared.assign]: #util.smartptr.shared.assign
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
[utilities.summary]: #utilities.summary
[utility]: #utility
[utility.as.const]: #utility.as.const
[utility.exchange]: #utility.exchange
[utility.intcmp]: #utility.intcmp
[utility.swap]: #utility.swap
[utility.syn]: #utility.syn
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
[variant.variant]: #variant.variant
[variant.visit]: #variant.visit

[^1]: `pointer_safety::preferred` might be returned to indicate that a
    leak detector is running so that the program can avoid spurious leak
    reports.

[^2]: Such a type is a function pointer or a class type which has a
    member `operator()` or a class type which has a conversion to a
    pointer to function.
