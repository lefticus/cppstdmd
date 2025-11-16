# General utilities library <a id="utilities">[[utilities]]</a>

## General <a id="utilities.general">[[utilities.general]]</a>

This Clause describes utilities that are generally useful in C++
programs; some of these utilities are used by other elements of the C++
standard library. These utilities are summarized in
[[utilities.summary]].

**Table: General utilities library summary**

| Subclause            |                              | Header         |
| -------------------- | ---------------------------- | -------------- |
| [[utility]]          | Utility components           | `<utility>`    |
| [[pairs]]            | Pairs                        |                |
| [[tuple]]            | Tuples                       | `<tuple>`      |
| [[optional]]         | Optional objects             | `<optional>`   |
| [[variant]]          | Variants                     | `<variant>`    |
| [[any]]              | Storage for any type         | `<any>`        |
| [[expected]]         | Expected objects             | `<expected>`   |
| [[bitset]]           | Fixed-size sequences of bits | `<bitset>`     |
| [[function.objects]] | Function objects             | `<functional>` |
| [[bit]]              | Bit manipulation             | `<bit>`        |


## Utility components <a id="utility">[[utility]]</a>

### Header `<utility>` synopsis <a id="utility.syn">[[utility.syn]]</a>

The header `<utility>` contains some basic function and class templates
that are used throughout the rest of the library.

``` cpp
// all freestanding
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
    constexpr T exchange(T& obj, U&& new_val) noexcept(see below);

  // [forward], forward/move
  template<class T>
    constexpr T&& forward(remove_reference_t<T>& t) noexcept;
  template<class T>
    constexpr T&& forward(remove_reference_t<T>&& t) noexcept;
  template<class T, class U>
    constexpr auto forward_like(U&& x) noexcept -> see below;
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

  // [utility.underlying], to_underlying
  template<class T>
    constexpr underlying_type_t<T> to_underlying(T value) noexcept;

  // [utility.undefined], undefined behavior
  [[noreturn]] void unreachable();
  void observable_checkpoint() noexcept;

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

  template<class T1, class T2, class U1, class U2,
           template<class> class TQual, template<class> class UQual>
    requires requires { typename pair<common_reference_t<TQual<T1>, UQual<U1>>,
                                      common_reference_t<TQual<T2>, UQual<U2>>>; }
  struct basic_common_reference<pair<T1, T2>, pair<U1, U2>, TQual, UQual> {
    using type = pair<common_reference_t<TQual<T1>, UQual<U1>>,
                      common_reference_t<TQual<T2>, UQual<U2>>>;
  };

  template<class T1, class T2, class U1, class U2>
    requires requires { typename pair<common_type_t<T1, U1>, common_type_t<T2, U2>>; }
  struct common_type<pair<T1, T2>, pair<U1, U2>> {
    using type = pair<common_type_t<T1, U1>, common_type_t<T2, U2>>;
  };

  // [pairs.spec], pair specialized algorithms
  template<class T1, class T2, class U1, class U2>
    constexpr bool operator==(const pair<T1, T2>&, const pair<U1, U2>&);
  template<class T1, class T2, class U1, class U2>
    constexpr common_comparison_category_t<synth-three-way-result<T1, U1>,
                                           synth-three-way-result<T2, U2>>
      operator<=>(const pair<T1, T2>&, const pair<U1, U2>&);

  template<class T1, class T2>
    constexpr void swap(pair<T1, T2>& x, pair<T1, T2>& y) noexcept(noexcept(x.swap(y)));
  template<class T1, class T2>
    constexpr void swap(const pair<T1, T2>& x, const pair<T1, T2>& y)
      noexcept(noexcept(x.swap(y)));

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
  template<class T> constexpr in_place_type_t<T> in_place_type{};

  template<size_t I>
    struct in_place_index_t {
      explicit in_place_index_t() = default;
    };
  template<size_t I> constexpr in_place_index_t<I> in_place_index{};

  // nontype argument tag%
%

  template<auto V>
    struct nontype_t {
      explicit nontype_t() = default;
    };
  template<auto V> constexpr nontype_t<V> nontype{};

  // [variant.monostate], class monostate%

  struct monostate;

  // [variant.monostate.relops], monostate relational operators%
{monostate{monostate}
  constexpr bool operator==(monostate, monostate) noexcept;
  constexpr strong_ordering operator<=>(monostate, monostate) noexcept;

  // [variant.hash], hash support%
{monostate}
  template<class T> struct hash;
  template<> struct hash<monostate>;
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

*Remarks:* The exception specification is equivalent to:

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
  constexpr T exchange(T& obj, U&& new_val) noexcept(see below);
```

*Effects:* Equivalent to:

``` cpp
T old_val = std::move(obj);
obj = std::forward<U>(new_val);
return old_val;
```

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_move_constructible_v<T> && is_nothrow_assignable_v<T&, U>
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
template<class T, class U>
  constexpr auto forward_like(U&& x) noexcept -> see below;
```

*Mandates:* `T` is a referenceable type [[defns.referenceable]].

- Let *`COPY_CONST`*`(A, B)` be `const B` if `A` is a const type,
  otherwise `B`.
- Let *`OVERRIDE_REF`*`(A, B)` be `remove_reference_t<B>&&` if `A` is an
  rvalue reference type, otherwise `B&`.
- Let `V` be
  ``` cpp
  OVERRIDE_REF(T&&, COPY_CONST(remove_reference_t<T>, remove_reference_t<U>))
  ```

*Returns:* `static_cast<V>(x)`.

*Remarks:* The return type is `V`.

[*Example 2*:

``` cpp
struct accessor {
  vector<string>* container;
  decltype(auto) operator[](this auto&& self, size_t i) {
    return std::forward_like<decltype(self)>((*container)[i]);
  }
};
void g() {
  vector v{"a"s, "b"s};
  accessor a{&v};
  string& x = a[0];                             // OK, binds to lvalue reference
  string&& y = std::move(a)[0];                 // OK, is rvalue reference
  string const&& z = std::move(as_const(a))[1]; // OK, is const&&
  string& w = as_const(a)[1];                   // error: will not bind to non-const
}
```

— *end example*]

``` cpp
template<class T> constexpr remove_reference_t<T>&& move(T&& t) noexcept;
```

*Returns:* `static_cast<remove_reference_t<T>&&>(t)`.

[*Example 3*:

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
  shared_ptr<A> sp2 = factory<A>(std::move(a));     // ``a'' binds to A(A&&)
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
[[term.unevaluated.operand]].

``` cpp
template<class T> add_rvalue_reference_t<T> declval() noexcept;    // as unevaluated operand
```

*Mandates:* This function is not odr-used [[term.odr.use]].

*Remarks:* The template parameter `T` of `declval` may be an incomplete
type.

[*Example 1*:

``` cpp
template<class To, class From> decltype(static_cast<To>(declval<From>())) convert(From&&);
```

declares a function template `convert` which only participates in
overload resolution if the type `From` can be explicitly converted to
type `To`. For another example see class template
`common_type`[[meta.trans.other]].

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

### Function template `to_underlying` <a id="utility.underlying">[[utility.underlying]]</a>

``` cpp
template<class T>
  constexpr underlying_type_t<T> to_underlying(T value) noexcept;
```

*Returns:* `static_cast<underlying_type_t<T>>(value)`.

### Undefined behavior <a id="utility.undefined">[[utility.undefined]]</a>

``` cpp
[[noreturn]] void unreachable();
```

*Preconditions:* `false` is `true`.

[*Note 1*: This precondition cannot be satisfied, thus the behavior of
calling `unreachable` is undefined. — *end note*]

[*Example 1*:

``` cpp
int f(int x) {
  switch (x) {
  case 0:
  case 1:
    return x;
  default:
    std::unreachable();
  }
}
int a = f(1);           // OK, a has value 1
int b = f(3);           // undefined behavior
```

— *end example*]

``` cpp
void observable_checkpoint() noexcept;
```

*Effects:* Establishes an observable checkpoint [[intro.abstract]].

## Pairs <a id="pairs">[[pairs]]</a>

### General <a id="pairs.general">[[pairs.general]]</a>

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
    template<class U1 = T1, class U2 = T2>
      constexpr explicit(see below) pair(U1&& x, U2&& y);
    template<class U1, class U2>
      constexpr explicit(see below) pair(pair<U1, U2>& p);
    template<class U1, class U2>
      constexpr explicit(see below) pair(const pair<U1, U2>& p);
    template<class U1, class U2>
      constexpr explicit(see below) pair(pair<U1, U2>&& p);
    template<class U1, class U2>
      constexpr explicit(see below) pair(const pair<U1, U2>&& p);
    template<pair-like P>
      constexpr explicit(see below) pair(P&& p);
    template<class... Args1, class... Args2>
      constexpr pair(piecewise_construct_t,
                     tuple<Args1...> first_args, tuple<Args2...> second_args);

    constexpr pair& operator=(const pair& p);
    constexpr const pair& operator=(const pair& p) const;
    template<class U1, class U2>
      constexpr pair& operator=(const pair<U1, U2>& p);
    template<class U1, class U2>
      constexpr const pair& operator=(const pair<U1, U2>& p) const;
    constexpr pair& operator=(pair&& p) noexcept(see below);
    constexpr const pair& operator=(pair&& p) const;
    template<class U1, class U2>
      constexpr pair& operator=(pair<U1, U2>&& p);
    template<class U1, class U2>
      constexpr const pair& operator=(pair<U1, U2>&& p) const;
    template<pair-like P>
      constexpr pair& operator=(P&& p);
    template<pair-like P>
      constexpr const pair& operator=(P&& p) const;

    constexpr void swap(pair& p) noexcept(see below);
    constexpr void swap(const pair& p) const noexcept(see below);
  };

  template<class T1, class T2>
    pair(T1, T2) -> pair<T1, T2>;
}
```

Member functions of `pair` do not throw exceptions unless one of the
element-wise operations specified to be called for that operation throws
an exception.

The defaulted move and copy constructor, respectively, of `pair` is a
constexpr function if and only if all required element-wise
initializations for move and copy, respectively, would be
constexpr-suitable [[dcl.constexpr]].

If
`(is_trivially_destructible_v<T1> && is_trivially_destructible_v<T2>)`
is `true`, then the destructor of `pair` is trivial.

`pair<T, U>` is a structural type [[term.structural.type]] if `T` and
`U` are both structural types. Two values `p1` and `p2` of type
`pair<T, U>` are template-argument-equivalent [[temp.type]] if and only
if `p1.first` and `p2.first` are template-argument-equivalent and
`p1.second` and `p2.second` are template-argument-equivalent.

``` cpp
constexpr explicit(see below) pair();
```

*Constraints:*

- `is_default_constructible_v<T1>` is `true` and
- `is_default_constructible_v<T2>` is `true`.

*Effects:* Value-initializes `first` and `second`.

*Remarks:* The expression inside `explicit` evaluates to `true` if and
only if either `T1` or `T2` is not implicitly default-constructible.

[*Note 1*: This behavior can be implemented with a trait that checks
whether a `const T1&` or a `const T2&` can be initialized with
`{}`. — *end note*]

``` cpp
constexpr explicit(see below) pair(const T1& x, const T2& y);
```

*Constraints:*

- `is_copy_constructible_v<T1>` is `true` and
- `is_copy_constructible_v<T2>` is `true`.

*Effects:* Initializes `first` with `x` and `second` with `y`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<const T1&, T1> || !is_convertible_v<const T2&, T2>
```

``` cpp
template<class U1 = T1, class U2 = T2> constexpr explicit(see below) pair(U1&& x, U2&& y);
```

*Constraints:*

- `is_constructible_v<T1, U1>` is `true` and
- `is_constructible_v<T2, U2>` is `true`.

*Effects:* Initializes `first` with `std::forward<U1>(x)` and `second`
with `std::forward<U2>(y)`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<U1, T1> || !is_convertible_v<U2, T2>
```

This constructor is defined as deleted if
`reference_constructs_from_temporary_v<first_type, U1&&>` is `true` or
`reference_constructs_from_temporary_v<second_type, U2&&>` is `true`.

``` cpp
template<class U1, class U2> constexpr explicit(see below) pair(pair<U1, U2>& p);
template<class U1, class U2> constexpr explicit(see below) pair(const pair<U1, U2>& p);
template<class U1, class U2> constexpr explicit(see below) pair(pair<U1, U2>&& p);
template<class U1, class U2> constexpr explicit(see below) pair(const pair<U1, U2>&& p);
template<pair-like P> constexpr explicit(see below) pair(P&& p);
```

Let *`FWD`*`(u)` be `static_cast<decltype(u)>(u)`.

*Constraints:*

- For the last overload, `remove_cvref_t<P>` is not a specialization of
  `ranges::subrange`,
- `is_constructible_v<T1, decltype(get<0>(`*`FWD`*`(p)))>` is `true`,
  and
- `is_constructible_v<T2, decltype(get<1>(`*`FWD`*`(p)))>` is `true`.

*Effects:* Initializes `first` with `get<0>(`*`FWD`*`(p))` and `second`
with `get<1>(`*`FWD`*`(p))`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<decltype(get<0>(FWD(p))), T1> ||
!is_convertible_v<decltype(get<1>(FWD(p))), T2>
```

The constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<first_type, decltype(get<0>(FWD(p)))> ||
reference_constructs_from_temporary_v<second_type, decltype(get<1>(FWD(p)))>
```

is `true`.

``` cpp
template<class... Args1, class... Args2>
  constexpr pair(piecewise_construct_t,
                 tuple<Args1...> first_args, tuple<Args2...> second_args);
```

*Mandates:*

- `is_constructible_v<T1, Args1...>` is `true` and
- `is_constructible_v<T2, Args2...>` is `true`.

*Effects:* Initializes `first` with arguments of types `Args1...`
obtained by forwarding the elements of `first_args` and initializes
`second` with arguments of types `Args2...` obtained by forwarding the
elements of `second_args`. (Here, forwarding an element `x` of type `U`
within a `tuple` object means calling `std::forward<U>(x)`.) This form
of construction, whereby constructor arguments for `first` and `second`
are each provided in a separate `tuple` object, is called *piecewise
construction*.

[*Note 2*: If a data member of `pair` is of reference type and its
initialization binds it to a temporary object, the program is
ill-formed [[class.base.init]]. — *end note*]

``` cpp
constexpr pair& operator=(const pair& p);
```

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

*Remarks:* This operator is defined as deleted unless
`is_copy_assignable_v<T1>` is `true` and `is_copy_assignable_v<T2>` is
`true`.

``` cpp
constexpr const pair& operator=(const pair& p) const;
```

*Constraints:*

- `is_copy_assignable_v<const T1>` is `true` and
- `is_copy_assignable_v<const T2>` is `true`.

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr pair& operator=(const pair<U1, U2>& p);
```

*Constraints:*

- `is_assignable_v<T1&, const U1&>` is `true` and
- `is_assignable_v<T2&, const U2&>` is `true`.

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr const pair& operator=(const pair<U1, U2>& p) const;
```

*Constraints:*

- `is_assignable_v<const T1&, const U1&>` is `true`, and
- `is_assignable_v<const T2&, const U2&>` is `true`.

*Effects:* Assigns `p.first` to `first` and `p.second` to `second`.

*Returns:* `*this`.

``` cpp
constexpr pair& operator=(pair&& p) noexcept(see below);
```

*Constraints:*

- `is_move_assignable_v<T1>` is `true` and
- `is_move_assignable_v<T2>` is `true`.

*Effects:* Assigns `std::forward<T1>(p.first)` to `first` and
`std::forward<T2>(p.second)` to `second`.

*Returns:* `*this`.

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_move_assignable_v<T1> && is_nothrow_move_assignable_v<T2>
```

``` cpp
constexpr const pair& operator=(pair&& p) const;
```

*Constraints:*

- `is_assignable_v<const T1&, T1>` is `true` and
- `is_assignable_v<const T2&, T2>` is `true`.

*Effects:* Assigns `std::forward<T1>(p.first)` to `first` and
`std::forward<T2>(p.second)` to `second`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr pair& operator=(pair<U1, U2>&& p);
```

*Constraints:*

- `is_assignable_v<T1&, U1>` is `true` and
- `is_assignable_v<T2&, U2>` is `true`.

*Effects:* Assigns `std::forward<U1>(p.first)` `first` and
`std::forward<U2>(p.second)` to `second`.

*Returns:* `*this`.

``` cpp
template<pair-like P> constexpr pair& operator=(P&& p);
```

*Constraints:*

- `different-from<P, pair>`[[range.utility.helpers]] is `true`,
- `remove_cvref_t<P>` is not a specialization of `ranges::subrange`,
- `is_assignable_v<T1&, decltype(get<0>(std::forward<P>(p)))>` is
  `true`, and
- `is_assignable_v<T2&, decltype(get<1>(std::forward<P>(p)))>` is
  `true`.

*Effects:* Assigns `get<0>(std::forward<P>(p))` to `first` and
`get<1>(std::forward<P>(p))` to `second`.

*Returns:* `*this`.

``` cpp
template<pair-like P> constexpr const pair& operator=(P&& p) const;
```

*Constraints:*

- `different-from<P, pair>`[[range.utility.helpers]] is `true`,
- `remove_cvref_t<P>` is not a specialization of `ranges::subrange`,
- `is_assignable_v<const T1&, decltype(get<0>(std::forward<P>(p)))>` is
  `true`, and
- `is_assignable_v<const T2&, decltype(get<1>(std::forward<P>(p)))>` is
  `true`.

*Effects:* Assigns `get<0>(std::forward<P>(p))` to `first` and
`get<1>(std::forward<P>(p))` to `second`.

*Returns:* `*this`.

``` cpp
template<class U1, class U2> constexpr const pair& operator=(pair<U1, U2>&& p) const;
```

*Constraints:*

- `is_assignable_v<const T1&, U1>` is `true`, and
- `is_assignable_v<const T2&, U2>` is `true`.

*Effects:* Assigns `std::forward<U1>(p.first)` to `first` and
`std::forward<U2>(u.second)` to `second`.

*Returns:* `*this`.

``` cpp
constexpr void swap(pair& p) noexcept(see below);
constexpr void swap(const pair& p) const noexcept(see below);
```

*Mandates:*

- For the first overload, `is_swappable_v<T1>` is `true` and
  `is_swappable_v<T2>` is `true`.
- For the second overload, `is_swappable_v<const T1>` is `true` and
  `is_swappable_v<const T2>` is `true`.

*Preconditions:* `first` is swappable with [[swappable.requirements]]
`p.first` and `second` is swappable with `p.second`.

*Effects:* Swaps `first` with `p.first` and `second` with `p.second`.

*Remarks:* The exception specification is equivalent to:

- `is_nothrow_swappable_v<T1> && is_nothrow_swappable_v<T2>` for the
  first overload, and
- `is_nothrow_swappable_v<const T1> && is_nothrow_swappable_v<const T2>`
  for the second overload.

### Specialized algorithms <a id="pairs.spec">[[pairs.spec]]</a>

``` cpp
template<class T1, class T2, class U1, class U2>
  constexpr bool operator==(const pair<T1, T2>& x, const pair<U1, U2>& y);
```

*Constraints:* `x.first == y.first` and `x.second == y.second` are valid
expressions and each of `decltype(x.first == y.first)` and
`decltype(x.second == y.second)` models .

*Returns:* `x.first == y.first && x.second == y.second`.

``` cpp
template<class T1, class T2, class U1, class U2>
  constexpr common_comparison_category_t<synth-three-way-result<T1, U1>,
                                         synth-three-way-result<T2, U2>>
    operator<=>(const pair<T1, T2>& x, const pair<U1, U2>& y);
```

*Effects:* Equivalent to:

``` cpp
if (auto c = synth-three-way(x.first, y.first); c != 0) return c;
return synth-three-way(x.second, y.second);
```

``` cpp
template<class T1, class T2>
  constexpr void swap(pair<T1, T2>& x, pair<T1, T2>& y) noexcept(noexcept(x.swap(y)));
template<class T1, class T2>
  constexpr void swap(const pair<T1, T2>& x, const pair<T1, T2>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:*

- For the first overload, `is_swappable_v<T1>` is `true` and
  `is_swappable_v<T2>` is `true`.
- For the second overload, `is_swappable_v<const T1>` is `true` and
  `is_swappable_v<const T2>` is `true`.

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

*Result:* The type `T1` if `I` is 0, otherwise the type `T2`.

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

### General <a id="tuple.general">[[tuple.general]]</a>

Subclause  [[tuple]] describes the tuple library that provides a tuple
type as the class template `tuple` that can be instantiated with any
number of arguments. Each template argument specifies the type of an
element in the `tuple`. Consequently, tuples are heterogeneous,
fixed-size collections of values. An instantiation of `tuple` with two
arguments is similar to an instantiation of `pair` with the same two
arguments. See  [[pairs]].

In addition to being available via inclusion of the `<tuple>` header,
`ignore` [[tuple.syn]] is available when `<utility>` [[utility]] is
included.

### Header `<tuple>` synopsis <a id="tuple.syn">[[tuple.syn]]</a>

``` cpp
// all freestanding
#include <compare>              // see [compare.syn]

namespace std {
  // [tuple.tuple], class template tuple
  template<class... Types>
    class tuple;

  // [tuple.like], concept tuple-like
  template<class T>
    concept tuple-like = see belownc;         // exposition only
  template<class T>
    concept pair-like =                     // exposition only
      tuple-like<T> && tuple_size_v<remove_cvref_t<T>> == 2;

  // [tuple.common.ref], common_reference related specializations
  template<exposition onlyconceptnc{tuple-like} TTuple, exposition onlyconceptnc{tuple-like} UTuple,
           template<class> class TQual, template<class> class UQual>
    struct basic_common_reference<TTuple, UTuple, TQual, UQual>;
  template<exposition onlyconceptnc{tuple-like} TTuple, exposition onlyconceptnc{tuple-like} UTuple>
    struct common_type<TTuple, UTuple>;

  // ignore
  struct ignore-type {                      // exposition only
    constexpr const ignore-type&
      operator=(const auto &) const noexcept { return *this; }
  };
  inline constexpr ignore-type ignore;

  // [tuple.creation], tuple creation functions
  template<class... TTypes>
    constexpr tuple<unwrap_ref_decay_t<TTypes>...> make_tuple(TTypes&&...);

  template<class... TTypes>
    constexpr tuple<TTypes&&...> forward_as_tuple(TTypes&&...) noexcept;

  template<class... TTypes>
    constexpr tuple<TTypes&...> tie(TTypes&...) noexcept;

  template<exposition onlyconceptnc{tuple-like}... Tuples>
    constexpr tuple<CTypes...> tuple_cat(Tuples&&...);

  // [tuple.apply], calling a function with a tuple of arguments
  template<class F, exposition onlyconceptnc{tuple-like} Tuple>
    constexpr apply_result_t<F, Tuple> apply(F&& f, Tuple&& t)
      noexcept(is_nothrow_applicable_v<F, Tuple>);

  template<class T, exposition onlyconceptnc{tuple-like} Tuple>
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
    using tuple_element_t = tuple_element<I, T>::type;

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
  template<class... TTypes, exposition onlyconceptnc{tuple-like} UTuple>
    constexpr bool operator==(const tuple<TTypes...>&, const UTuple&);
  template<class... TTypes, class... UTypes>
    constexpr common_comparison_category_t<synth-three-way-result<TTypes, UTypes>...>
      operator<=>(const tuple<TTypes...>&, const tuple<UTypes...>&);
  template<class... TTypes, exposition onlyconceptnc{tuple-like} UTuple>
    constexpr see belownc operator<=>(const tuple<TTypes...>&, const UTuple&);

  // [tuple.traits], allocator-related traits
  template<class... Types, class Alloc>
    struct uses_allocator<tuple<Types...>, Alloc>;

  // [tuple.special], specialized algorithms
  template<class... Types>
    constexpr void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);
  template<class... Types>
    constexpr void swap(const tuple<Types...>& x, const tuple<Types...>& y) noexcept(see below);

  // [tuple.helper], tuple helper classes
  template<class T>
    constexpr size_t tuple_size_v@ = tuple_size<T>::value;
}
```

### Concept  <a id="tuple.like">[[tuple.like]]</a>

``` cpp
template<class T>
  concept tuple-like = see belownc;           // exposition only
```

A type `T` models and satisfies the exposition-only concept `tuple-like`
if `remove_cvref_t<T>` is a specialization of `array`, `complex`,
`pair`, `tuple`, or `ranges::subrange`.

### Class template `tuple` <a id="tuple.tuple">[[tuple.tuple]]</a>

#### General <a id="tuple.tuple.general">[[tuple.tuple.general]]</a>

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
      constexpr explicit(see below) tuple(tuple<UTypes...>&);
    template<class... UTypes>
      constexpr explicit(see below) tuple(const tuple<UTypes...>&);
    template<class... UTypes>
      constexpr explicit(see below) tuple(tuple<UTypes...>&&);
    template<class... UTypes>
      constexpr explicit(see below) tuple(const tuple<UTypes...>&&);

    template<class U1, class U2>
      constexpr explicit(see below) tuple(pair<U1, U2>&);         // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr explicit(see below) tuple(const pair<U1, U2>&);   // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr explicit(see below) tuple(pair<U1, U2>&&);        // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr explicit(see below) tuple(const pair<U1, U2>&&);  // only if sizeof...(Types) == 2

    template<tuple-like UTuple>
      constexpr explicit(see below) tuple(UTuple&&);

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
        tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&);
    template<class Alloc, class... UTypes>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
    template<class Alloc, class... UTypes>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
    template<class Alloc, class... UTypes>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&&);
    template<class Alloc, class U1, class U2>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&);
    template<class Alloc, class U1, class U2>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
    template<class Alloc, class U1, class U2>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);
    template<class Alloc, class U1, class U2>
      constexpr explicit(see below)
        tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&&);

    template<class Alloc, exposition onlyconceptnc{tuple-like} UTuple>
      constexpr explicit(see below) tuple(allocator_arg_t, const Alloc& a, UTuple&&);

    // [tuple.assign], tuple assignment
    constexpr tuple& operator=(const tuple&);
    constexpr const tuple& operator=(const tuple&) const;
    constexpr tuple& operator=(tuple&&) noexcept(see below);
    constexpr const tuple& operator=(tuple&&) const;

    template<class... UTypes>
      constexpr tuple& operator=(const tuple<UTypes...>&);
    template<class... UTypes>
      constexpr const tuple& operator=(const tuple<UTypes...>&) const;
    template<class... UTypes>
      constexpr tuple& operator=(tuple<UTypes...>&&);
    template<class... UTypes>
      constexpr const tuple& operator=(tuple<UTypes...>&&) const;

    template<class U1, class U2>
      constexpr tuple& operator=(const pair<U1, U2>&);          // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr const tuple& operator=(const pair<U1, U2>&) const;
                                                                // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr tuple& operator=(pair<U1, U2>&&);               // only if sizeof...(Types) == 2
    template<class U1, class U2>
      constexpr const tuple& operator=(pair<U1, U2>&&) const;   // only if sizeof...(Types) == 2

    template<exposition onlyconceptnc{tuple-like} UTuple>
      constexpr tuple& operator=(UTuple&&);
    template<exposition onlyconceptnc{tuple-like}@ UTuple>
      constexpr const tuple& operator=(UTuple&&) const;

    // [tuple.swap], tuple swap
    constexpr void swap(tuple&) noexcept(see below);
    constexpr void swap(const tuple&) const noexcept(see below);
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

If a program declares an explicit or partial specialization of `tuple`,
the program is ill-formed, no diagnostic required.

#### Construction <a id="tuple.cnstr">[[tuple.cnstr]]</a>

In the descriptions that follow, let i be in the range \[`0`,
`sizeof...(Types)`) in order, `Tᵢ` be the iᵗʰ type in `Types`, and `Uᵢ`
be the iᵗʰ type in a template parameter pack named `UTypes`, where
indexing is zero-based.

For each `tuple` constructor, an exception is thrown only if the
construction of one of the types in `Types` throws an exception.

The defaulted move and copy constructor, respectively, of `tuple` is a
constexpr function if and only if all required element-wise
initializations for move and copy, respectively, would be
constexpr-suitable [[dcl.constexpr]]. The defaulted move and copy
constructor of `tuple<>` are constexpr functions.

If `is_trivially_destructible_v<\tcode{T}_i>` is `true` for all `Tᵢ`,
then the destructor of `tuple` is trivial.

The default constructor of `tuple<>` is trivial.

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

Let *disambiguating-constraint* be:

- `negation<is_same<remove_cvref_t<``U₀``>, tuple>>` if
  `sizeof...(Types)` is 1;
- otherwise,
  `bool_constant<!is_same_v<remove_cvref_t<``U₀``>, allocator_arg_t> || is_-`\newline`same_v<remove_cvref_t<``T₀``>, allocator_arg_t>>`
  if `sizeof...(Types)` is 2 or 3;
- otherwise, `true_type`.

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)`,
- `sizeof...(Types)` ≥ 1, and
- `conjunction_v<`*`disambiguating-constraint`*`, is_constructible<Types, UTypes>...>`
  is`true`.

*Effects:* Initializes the elements in the tuple with the corresponding
value in `std::forward<UTypes>(u)`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!conjunction_v<is_convertible<UTypes, Types>...>
```

This constructor is defined as deleted if

``` cpp
(reference_constructs_from_temporary_v<Types, UTypes&&> || ...)
```

is `true`.

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
template<class... UTypes> constexpr explicit(see below) tuple(tuple<UTypes...>& u);
template<class... UTypes> constexpr explicit(see below) tuple(const tuple<UTypes...>& u);
template<class... UTypes> constexpr explicit(see below) tuple(tuple<UTypes...>&& u);
template<class... UTypes> constexpr explicit(see below) tuple(const tuple<UTypes...>&& u);
```

Let `I` be the pack `0, 1, `…`, (sizeof...(Types) - 1)`. Let
*`FWD`*`(u)` be `static_cast<decltype(u)>(u)`.

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)`, and
- `(is_constructible_v<Types, decltype(get<I>(`*`FWD`*`(u)))> && ...)`
  is `true`, and
- either `sizeof...(Types)` is not 1, or (when `Types...` expands to `T`
  and `UTypes...` expands to `U`) `is_convertible_v<decltype(u), T>`,
  `is_constructible_v<T, decltype(u)>`, and `is_same_v<T, U>` are all
  `false`.

*Effects:* For all i, initializes the $i^\textrm{th}$ element of `*this`
with `get<`i`>(`*`FWD`*`(u))`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!(is_convertible_v<decltype(get<I>(FWD(u))), Types> && ...)
```

The constructor is defined as deleted if

``` cpp
(reference_constructs_from_temporary_v<Types, decltype(get<I>(FWD(u)))> || ...)
```

is `true`.

``` cpp
template<class U1, class U2> constexpr explicit(see below) tuple(pair<U1, U2>& u);
template<class U1, class U2> constexpr explicit(see below) tuple(const pair<U1, U2>& u);
template<class U1, class U2> constexpr explicit(see below) tuple(pair<U1, U2>&& u);
template<class U1, class U2> constexpr explicit(see below) tuple(const pair<U1, U2>&& u);
```

Let *`FWD`*`(u)` be `static_cast<decltype(u)>(u)`.

*Constraints:*

- `sizeof...(Types)` is 2,
- `is_constructible_v<``T₀``, decltype(get<0>(`*`FWD`*`(u)))>` is
  `true`, and
- `is_constructible_v<``T₁``, decltype(get<1>(`*`FWD`*`(u)))>` is
  `true`.

*Effects:* Initializes the first element with `get<0>(`*`FWD`*`(u))` and
the second element with `get<1>(`*`FWD`*`(u))`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<decltype(get<0>(FWD(u))), $T_0$> ||
!is_convertible_v<decltype(get<1>(FWD(u))), $T_1$>
```

The constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<$T_0$, decltype(get<0>(FWD(u)))> ||
reference_constructs_from_temporary_v<$T_1$, decltype(get<1>(FWD(u)))>
```

is `true`.

``` cpp
template<tuple-like UTuple>
  constexpr explicit(see below) tuple(UTuple&& u);
```

Let `I` be the pack `0, 1, `…`, (sizeof...(Types) - 1)`.

*Constraints:*

- `different-from<UTuple, tuple>`[[range.utility.helpers]] is `true`,
- `remove_cvref_t<UTuple>` is not a specialization of
  `ranges::subrange`,
- `sizeof...(Types)` equals `tuple_size_v<remove_cvref_t<UTuple>>`,
- `(is_constructible_v<Types, decltype(get<I>(std::forward<UTuple>(u)))> && ...)`
  is `true`, and
- either `sizeof...(Types)` is not 1, or (when `Types...` expands to
  `T`) `is_convertible_v<UTuple, T>` and `is_constructible_v<T, UTuple>`
  are both `false`.

*Effects:* For all i, initializes the iᵗʰ element of `*this` with
`get<`i`>(std::forward<UTuple>(u))`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!(is_convertible_v<decltype(get<I>(std::forward<UTuple>(u))), Types> && ...)
```

The constructor is defined as deleted if

``` cpp
(reference_constructs_from_temporary_v<Types, decltype(get<I>(std::forward<UTuple>(u)))>
 || ...)
```

is `true`.

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
    tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&);
template<class Alloc, class... UTypes>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&);
template<class Alloc, class... UTypes>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, tuple<UTypes...>&&);
template<class Alloc, class... UTypes>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const tuple<UTypes...>&&);
template<class Alloc, class U1, class U2>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&);
template<class Alloc, class U1, class U2>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&);
template<class Alloc, class U1, class U2>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, pair<U1, U2>&&);
template<class Alloc, class U1, class U2>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, const pair<U1, U2>&&);
template<class Alloc, tuple-like UTuple>
  constexpr explicit(see below)
    tuple(allocator_arg_t, const Alloc& a, UTuple&&);
```

*Preconditions:* `Alloc` meets the *Cpp17Allocator*
requirements [[allocator.requirements.general]].

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

*Returns:* `*this`.

*Remarks:* This operator is defined as deleted unless
`is_copy_assignable_v<``Tᵢ``>` is `true` for all i.

``` cpp
constexpr const tuple& operator=(const tuple& u) const;
```

*Constraints:* `(is_copy_assignable_v<const Types> && ...)` is `true`.

*Effects:* Assigns each element of `u` to the corresponding element of
`*this`.

*Returns:* `*this`.

``` cpp
constexpr tuple& operator=(tuple&& u) noexcept(see below);
```

*Constraints:* `is_move_assignable_v<``Tᵢ``>` is `true` for all i.

*Effects:* For all i, assigns `std::forward<``Tᵢ``>(get<`i`>(u))` to
`get<`i`>(*this)`.

*Returns:* `*this`.

*Remarks:* The exception specification is equivalent to the logical of
the following expressions:

``` cpp
is_nothrow_move_assignable_v<Tᵢ>
```

where Tᵢ is the iᵗʰ type in `Types`.

``` cpp
constexpr const tuple& operator=(tuple&& u) const;
```

*Constraints:* `(is_assignable_v<const Types&, Types> && ...)` is
`true`.

*Effects:* For all i, assigns `std::forward<T`ᵢ`>(get<`i`>(u))` to
`get<`i`>(*this)`.

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
template<class... UTypes> constexpr const tuple& operator=(const tuple<UTypes...>& u) const;
```

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)` and
- `(is_assignable_v<const Types&, const UTypes&> && ...)` is `true`.

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
template<class... UTypes> constexpr const tuple& operator=(tuple<UTypes...>&& u) const;
```

*Constraints:*

- `sizeof...(Types)` equals `sizeof...(UTypes)` and
- `(is_assignable_v<const Types&, UTypes> && ...)` is `true`.

*Effects:* For all i, assigns `std::forward<U`ᵢ`>(get<`i`>(u))` to
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
template<class U1, class U2> constexpr const tuple& operator=(const pair<U1, U2>& u) const;
```

*Constraints:*

- `sizeof...(Types)` is 2,
- `is_assignable_v<const ``T₀``&, const U1&>` is `true`, and
- `is_assignable_v<const ``T₁``&, const U2&>` is `true`.

*Effects:* Assigns `u.first` to the first element and `u.second` to the
second element.

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

``` cpp
template<class U1, class U2> constexpr const tuple& operator=(pair<U1, U2>&& u) const;
```

*Constraints:*

- `sizeof...(Types)` is 2,
- `is_assignable_v<const ``T₀``&, U1>` is `true`, and
- `is_assignable_v<const ``T₁``&, U2>` is `true`.

*Effects:* Assigns `std::forward<U1>(u.first)` to the first element
and  
`std::forward<U2>(u.second)` to the second element.

*Returns:* `*this`.

``` cpp
template<tuple-like UTuple>
  constexpr tuple& operator=(UTuple&& u);
```

*Constraints:*

- `different-from<UTuple, tuple>`[[range.utility.helpers]] is `true`,
- `remove_cvref_t<UTuple>` is not a specialization of
  `ranges::subrange`,
- `sizeof...(Types)` equals `tuple_size_v<remove_cvref_t<UTuple>>`, and
- `is_assignable_v<``Tᵢ``&, decltype(get<`i`>(std::forward<UTuple>(u)))>`
  is `true` for all i.

*Effects:* For all i, assigns `get<`i`>(std::forward<UTuple>(u))` to
`get<`i`>(*this)`.

*Returns:* `*this`.

``` cpp
template<tuple-like UTuple>
  constexpr const tuple& operator=(UTuple&& u) const;
```

*Constraints:*

- `different-from<UTuple, tuple>`[[range.utility.helpers]] is `true`,
- `remove_cvref_t<UTuple>` is not a specialization of
  `ranges::subrange`,
- `sizeof...(Types)` equals `tuple_size_v<remove_cvref_t<UTuple>>`, and
- `is_assignable_v<const ``Tᵢ``&, decltype(get<`i`>(std::forward<UTuple>(u)))>`
  is `true` for all i.

*Effects:* For all i, assigns `get<`i`>(std::forward<UTuple>(u))` to
`get<`i`>(*this)`.

*Returns:* `*this`.

#### `swap` <a id="tuple.swap">[[tuple.swap]]</a>

``` cpp
constexpr void swap(tuple& rhs) noexcept(see below);
constexpr void swap(const tuple& rhs) const noexcept(see below);
```

Let i be in the range \[`0`, `sizeof...(Types)`) in order.

*Mandates:*

- For the first overload, `(is_swappable_v<Types> && ...)` is `true`.
- For the second overload, `(is_swappable_v<const Types> && ...)` is
  `true`.

*Preconditions:* For all i, `get<`i`>(*this)` is swappable
with [[swappable.requirements]] `get<`i`>(rhs)`.

*Effects:* For each i, calls `swap` for `get<`i`>(*this)` and
`get<`i`>(rhs)`.

*Throws:* Nothing unless one of the element-wise `swap` calls throws an
exception.

*Remarks:* The exception specification is equivalent to

- `(is_nothrow_swappable_v<Types> && ...)` for the first overload and
- `(is_nothrow_swappable_v<const Types> && ...)` for the second
  overload.

### Tuple creation functions <a id="tuple.creation">[[tuple.creation]]</a>

``` cpp
template<class... TTypes>
  constexpr tuple<unwrap_ref_decay_t<TTypes>...> make_tuple(TTypes&&... t);
```

*Returns:*
`tuple<unwrap_ref_decay_t<TTypes>...>(std::forward<TTypes>(t)...)`.

[*Example 1*:

``` cpp
int i; float j;
make_tuple(1, ref(i), cref(j));
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

*Returns:* `tuple<TTypes&...>(t...)`.

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
template<tuple-like... Tuples>
  constexpr tuple<CTypes...> tuple_cat(Tuples&&... tpls);
```

Let n be `sizeof...(Tuples)`. For every integer 0 ≤ i < n:

- Let `Tᵢ` be the iᵗʰ type in `Tuples`.
- Let `Uᵢ` be `remove_cvref_t<``Tᵢ``>`.
- Let `tpᵢ` be the iᵗʰ element in the function parameter pack `tpls`.
- Let Sᵢ be `tuple_size_v<``Uᵢ``>`.
- Let Eᵢᵏ be `tuple_element_t<`k`, ``Uᵢ``>`.
- Let eᵢᵏ be `get<`k`>(std::forward<``Tᵢ``>(``tpᵢ``))`.
- Let Elemsᵢ be a pack of the types $E_i^0, \dotsc, E_i^{S_{i-1}}$.
- Let elemsᵢ be a pack of the expressions
  $e_i^0, \dotsc, e_i^{S_{i-1}}$.

The types in `CTypes` are equal to the ordered sequence of the expanded
packs of types Elems₀`...`, Elems₁`...`, …, Elemsₙ₋₁`...`. Let `celems`
be the ordered sequence of the expanded packs of expressions
elems₀`...`, …, elemsₙ₋₁`...`.

*Mandates:* `(is_constructible_v<CTypes, decltype(celems)> && ...)` is
`true`.

*Returns:* `tuple<CTypes...>(celems...)`.

### Calling a function with a `tuple` of arguments <a id="tuple.apply">[[tuple.apply]]</a>

``` cpp
template<class F, tuple-like Tuple>
  constexpr apply_result_t<F, Tuple> apply(F&& f, Tuple&& t)
    noexcept(is_nothrow_applicable_v<F, Tuple>);
```

*Effects:* Given the exposition-only function template:

``` cpp
namespace std {
  template<class F, tuple-like Tuple, size_t... I>
  constexpr decltype(auto) apply-impl(F&& f, Tuple&& t, index_sequence<I...>) {
                                                                        // exposition only
    return INVOKE(std::forward<F>(f), get<I>(std::forward<Tuple>(t))...);     // see REF:func.require
  }
}
```

Equivalent to:

``` cpp
return apply-impl(std::forward<F>(f), std::forward<Tuple>(t),
                  make_index_sequence<tuple_size_v<remove_reference_t<Tuple>>>{});
```

``` cpp
template<class T, tuple-like Tuple>
  constexpr T make_from_tuple(Tuple&& t);
```

*Mandates:* If `tuple_size_v<remove_reference_t<Tuple>>` is 1, then
`reference_constructs_from_temporary_v<T, decltype(get<0>(declval<Tuple>()))>`
is `false`.

*Effects:* Given the exposition-only function template:

``` cpp
namespace std {
  template<class T, tuple-like Tuple, size_t... I>
    requires is_constructible_v<T, decltype(get<I>(declval<Tuple>()))...>
  constexpr T make-from-tuple-impl(Tuple&& t, index_sequence<I...>) {   // exposition only
    return T(get<I>(std::forward<Tuple>(t))...);
  }
}
```

Equivalent to:

``` cpp
return make-from-tuple-impl<T>(
           std::forward<Tuple>(t),
           make_index_sequence<tuple_size_v<remove_reference_t<Tuple>>>{});
```

[*Note 1*: The type of `T` must be supplied as an explicit template
parameter, as it cannot be deduced from the argument
list. — *end note*]

### Tuple helper classes <a id="tuple.helper">[[tuple.helper]]</a>

``` cpp
template<class T> struct tuple_size;
```

Except where specified otherwise, all specializations of `tuple_size`
meet the *Cpp17UnaryTypeTrait* requirements [[meta.rqmts]] with a base
characteristic of `integral_constant<size_t, N>` for some `N`.

``` cpp
template<class... Types>
  struct tuple_size<tuple<Types...>> : integral_constant<size_t, sizeof...(Types)> { };
```

``` cpp
template<size_t I, class... Types>
  struct tuple_element<I, tuple<Types...>> {
    using type = TI;
  };
```

*Mandates:* `I` < `sizeof...(Types)`.

*Result:* `TI` is the type of the `I`^\text{th} element of `Types`,
where indexing is zero-based.

``` cpp
template<class T> struct tuple_size<const T>;
```

Let `TS` denote `tuple_size<T>` of the cv-unqualified type `T`. If the
expression `TS::value` is well-formed when treated as an unevaluated
operand [[term.unevaluated.operand]], then each specialization of the
template meets the *Cpp17UnaryTypeTrait* requirements [[meta.rqmts]]
with a base characteristic of

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
    get(tuple<Types...>&& t) noexcept;        // #1
template<size_t I, class... Types>
  constexpr const tuple_element_t<I, tuple<Types...>>&
    get(const tuple<Types...>& t) noexcept;   // #2
template<size_t I, class... Types>
  constexpr const tuple_element_t<I, tuple<Types...>>&& get(const tuple<Types...>&& t) noexcept;
```

*Mandates:* `I` < `sizeof...(Types)`.

*Returns:* A reference to the `I`^\text{th} element of `t`, where
indexing is zero-based.

[*Note 1*: For the overload marked \#1, if a type `T` in `Types` is
some reference type `X&`, the return type is `X&`, not `X&&`. However,
if the element type is a non-reference type `T`, the return type is
`T&&`. — *end note*]

[*Note 2*: Constness is shallow. For the overload marked \#2, if a type
`T` in `Types` is some reference type `X&`, the return type is `X&`, not
`const X&`. However, if the element type is a non-reference type `T`,
the return type is `const T&`. This is consistent with how constness is
defined to work for non-static data members of reference
type. — *end note*]

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
template<class... TTypes, tuple-like UTuple>
  constexpr bool operator==(const tuple<TTypes...>& t, const UTuple& u);
```

For the first overload let `UTuple` be `tuple<UTypes...>`.

*Constraints:* For all `i`, where 0 ≤ `i` < `sizeof...(TTypes)`,
`get<i>(t) == get<i>(u)` is a valid expression and
`decltype(get<i>(t) == get<i>(u))` models `boolean-testable`.
`sizeof...(TTypes)` equals `tuple_size_v<UTuple>`.

*Returns:* `true` if `get<i>(t) == get<i>(u)` for all `i`, otherwise
`false`.

[*Note 1*: If `sizeof...(TTypes)` equals zero, returns
`true`. — *end note*]

*Remarks:*

- The elementary comparisons are performed in order from the zeroth
  index upwards. No comparisons or element accesses are performed after
  the first equality comparison that evaluates to `false`.
- The second overload is to be found via argument-dependent
  lookup [[basic.lookup.argdep]] only.

``` cpp
template<class... TTypes, class... UTypes>
  constexpr common_comparison_category_t<synth-three-way-result<TTypes, UTypes>...>
    operator<=>(const tuple<TTypes...>& t, const tuple<UTypes...>& u);
template<class... TTypes, tuple-like UTuple>
  constexpr common_comparison_category_t<synth-three-way-result<TTypes, Elems>...>
    operator<=>(const tuple<TTypes...>& t, const UTuple& u);
```

For the second overload, `Elems` denotes the pack of types
`tuple_element_t<0, UTuple>`, `tuple_element_t<1, UTuple>`, …,
`tuple_element_t<tuple_size_v<UTuple> - 1, UTuple>`.

*Effects:* Performs a lexicographical comparison between `t` and `u`. If
`sizeof...(TTypes)` equals zero, returns `strong_ordering::equal`.
Otherwise, equivalent to:

``` cpp
if (auto c = synth-three-way(get<0>(t), get<0>(u)); c != 0) return c;
return $t_tail$ <=> $u_tail$;
```

where `r_tail` for some `r` is a tuple containing all but the first
element of `r`.

*Remarks:* The second overload is to be found via argument-dependent
lookup [[basic.lookup.argdep]] only.

[*Note 1*: The above definition does not require `t_{tail}` (or
`u_{tail}`) to be constructed. It might not even be possible, as `t` and
`u` are not required to be copy constructible. Also, all comparison
operator functions are short circuited; they do not perform element
accesses beyond what is needed to determine the result of the
comparison. — *end note*]

### `common_reference` related specializations <a id="tuple.common.ref">[[tuple.common.ref]]</a>

In the descriptions that follow:

- Let `TTypes` be a pack formed by the sequence of
  `tuple_element_t<i, TTuple>` for every integer
  0 ≤ i < `tuple_size_v<TTuple>`.
- Let `UTypes` be a pack formed by the sequence of
  `tuple_element_t<i, UTuple>` for every integer
  0 ≤ i < `tuple_size_v<UTuple>`.

``` cpp
template<tuple-like TTuple, tuple-like UTuple,
         template<class> class TQual, template<class> class UQual>
struct basic_common_reference<TTuple, UTuple, TQual, UQual> {
  using type = see below;
};
```

*Constraints:*

- `TTuple` is a specialization of `tuple` or `UTuple` is a
  specialization of `tuple`.
- `is_same_v<TTuple, decay_t<TTuple>>` is `true`.
- `is_same_v<UTuple, decay_t<UTuple>>` is `true`.
- `tuple_size_v<TTuple>` equals `tuple_size_v<UTuple>`.
- `tuple<common_reference_t<TQual<TTypes>, UQual<UTypes>>...>` denotes a
  type.

*Result:* The member *typedef-name* `type` denotes the type
`tuple<common_reference_t<TQual<TTypes>, UQual<UTypes>>...>`.

``` cpp
template<tuple-like TTuple, tuple-like UTuple>
struct common_type<TTuple, UTuple> {
  using type = see below;
};
```

*Constraints:*

- `TTuple` is a specialization of `tuple` or `UTuple` is a
  specialization of `tuple`.
- `is_same_v<TTuple, decay_t<TTuple>>` is `true`.
- `is_same_v<UTuple, decay_t<UTuple>>` is `true`.
- `tuple_size_v<TTuple>` equals `tuple_size_v<UTuple>`.
- `tuple<common_type_t<TTypes, UTypes>...>` denotes a type.

*Result:* The member *typedef-name* `type` denotes the type  
`tuple<common_type_t<TTypes, UTypes>...>`.

### Tuple traits <a id="tuple.traits">[[tuple.traits]]</a>

``` cpp
template<class... Types, class Alloc>
  struct uses_allocator<tuple<Types...>, Alloc> : true_type { };
```

*Preconditions:* `Alloc` meets the *Cpp17Allocator*
requirements [[allocator.requirements.general]].

[*Note 1*: Specialization of this trait informs other library
components that `tuple` can be constructed with an allocator, even
though it does not have a nested `allocator_type`. — *end note*]

### Tuple specialized algorithms <a id="tuple.special">[[tuple.special]]</a>

``` cpp
template<class... Types>
  constexpr void swap(tuple<Types...>& x, tuple<Types...>& y) noexcept(see below);
template<class... Types>
  constexpr void swap(const tuple<Types...>& x, const tuple<Types...>& y) noexcept(see below);
```

*Constraints:*

- For the first overload, `(is_swappable_v<Types> && ...)` is `true`.
- For the second overload, `(is_swappable_v<const Types> && ...)` is
  `true`.

*Effects:* As if by `x.swap(y)`.

*Remarks:* The exception specification is equivalent to:

``` cpp
noexcept(x.swap(y))
```

## Optional objects <a id="optional">[[optional]]</a>

### General <a id="optional.general">[[optional.general]]</a>

Subclause  [[optional]] describes class template `optional` that
represents optional objects. An *optional object* is an object that
contains the storage for another object and manages the lifetime of this
contained object, if any. The contained object may be initialized after
the optional object has been initialized, and may be destroyed before
the optional object has been destroyed. The initialization state of the
contained object is tracked by the optional object.

### Header `<optional>` synopsis <a id="optional.syn">[[optional.syn]]</a>

``` cpp
// mostly freestanding
#include <compare>              // see [compare.syn]

namespace std {
  // [optional.optional], class template optional
  template<class T>
    class optional;                                             // partially freestanding

  // [optional.optional.ref], partial specialization of optional for lvalue reference types
  template<class T>
    class optional<T&>;                                         // partially freestanding

  template<class T>
    constexpr bool ranges::enable_view<optional<T>> = true;
  template<class T>
    constexpr auto format_kind<optional<T>> = range_format::disabled;
  template<class T>
    constexpr bool ranges::enable_borrowed_range<optional<T&>> = true;

  template<class T>
    concept \defexposconceptnc{is-derived-from-optional} = requires(const T& t) {   // exposition only
      []<class U>(const optional<U>&){ }(t);
    };

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
    constexpr compare_three_way_result_t<T, U>
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
  template<class T, class U>
      requires (!is-derived-from-optional<U>) && three_way_comparable_with<T, U>
    constexpr compare_three_way_result_t<T, U>
      operator<=>(const optional<T>&, const U&);

  // [optional.specalg], specialized algorithms
  template<class T>
    constexpr void swap(optional<T>&, optional<T>&) noexcept(see below);

  template<class T>
    constexpr optional<decay_t<T>> make_optional(T&&);
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

#### General <a id="optional.optional.general">[[optional.optional.general]]</a>

``` cpp
namespace std {
  template<class T>
  class optional {
  public:
    using value_type     = T;
    using iterator       = implementation-defined;              // see~[optional.iterators]
    using const_iterator = implementation-defined;              // see~[optional.iterators]

    // [optional.ctor], constructors
    constexpr optional() noexcept;
    constexpr optional(nullopt_t) noexcept;
    constexpr optional(const optional&);
    constexpr optional(optional&&) noexcept(see below);
    template<class... Args>
      constexpr explicit optional(in_place_t, Args&&...);
    template<class U, class... Args>
      constexpr explicit optional(in_place_t, initializer_list<U>, Args&&...);
    template<class U = remove_cv_t<T>>
      constexpr explicit(see below) optional(U&&);
    template<class U>
      constexpr explicit(see below) optional(const optional<U>&);
    template<class U>
      constexpr explicit(see below) optional(optional<U>&&);

    // [optional.dtor], destructor
    constexpr ~optional();

    // [optional.assign], assignment
    constexpr optional& operator=(nullopt_t) noexcept;
    constexpr optional& operator=(const optional&);
    constexpr optional& operator=(optional&&) noexcept(see below);
    template<class U = remove_cv_t<T>> constexpr optional& operator=(U&&);
    template<class U> constexpr optional& operator=(const optional<U>&);
    template<class U> constexpr optional& operator=(optional<U>&&);
    template<class... Args> constexpr T& emplace(Args&&...);
    template<class U, class... Args> constexpr T& emplace(initializer_list<U>, Args&&...);

    // [optional.swap], swap
    constexpr void swap(optional&) noexcept(see below);

    // [optional.iterators], iterator support
    constexpr iterator begin() noexcept;
    constexpr const_iterator begin() const noexcept;
    constexpr iterator end() noexcept;
    constexpr const_iterator end() const noexcept;

    // [optional.observe], observers
    constexpr const T* operator->() const noexcept;
    constexpr T* operator->() noexcept;
    constexpr const T& operator*() const & noexcept;
    constexpr T& operator*() & noexcept;
    constexpr T&& operator*() && noexcept;
    constexpr const T&& operator*() const && noexcept;
    constexpr explicit operator bool() const noexcept;
    constexpr bool has_value() const noexcept;
    constexpr const T& value() const &;                                 // freestanding-deleted
    constexpr T& value() &;                                             // freestanding-deleted
    constexpr T&& value() &&;                                           // freestanding-deleted
    constexpr const T&& value() const &&;                               // freestanding-deleted
    template<class U = remove_cv_t<T>> constexpr T value_or(U&&) const &;
    template<class U = remove_cv_t<T>> constexpr T value_or(U&&) &&;

    // [optional.monadic], monadic operations
    template<class F> constexpr auto and_then(F&& f) &;
    template<class F> constexpr auto and_then(F&& f) &&;
    template<class F> constexpr auto and_then(F&& f) const &;
    template<class F> constexpr auto and_then(F&& f) const &&;
    template<class F> constexpr auto transform(F&& f) &;
    template<class F> constexpr auto transform(F&& f) &&;
    template<class F> constexpr auto transform(F&& f) const &;
    template<class F> constexpr auto transform(F&& f) const &&;
    template<class F> constexpr optional or_else(F&& f) &&;
    template<class F> constexpr optional or_else(F&& f) const &;

    // [optional.mod], modifiers
    constexpr void reset() noexcept;

  private:
    T* val;         // exposition only
  };

  template<class T>
    optional(T) -> optional<T>;
}
```

An object of type `optional<T>` at any given time either contains a
value or does not contain a value. When an object of type `optional<T>`
*contains a value*, it means that an object of type `T`, referred to as
the optional object’s *contained value*, is nested within
[[intro.object]] the optional object. When an object of type
`optional<T>` is contextually converted to `bool`, the conversion
returns `true` if the object contains a value; otherwise the conversion
returns `false`.

When an object of type `optional<T>` contains a value, member `val`
points to the contained value.

A type `X` is a *valid contained type* for `optional` if `X` is an
lvalue reference type or a complete non-array object type, and
`remove_cvref_t<X>` is a type other than `in_place_t` or `nullopt_t`. If
a specialization of `optional` is instantiated with a type `T` that is
not a valid contained type for `optional`, the program is ill-formed. If
`T` is an object type, `T` shall meet the *Cpp17Destructible*
requirements ([[cpp17.destructible]]).

#### Constructors <a id="optional.ctor">[[optional.ctor]]</a>

The exposition-only variable template *converts-from-any-cvref* is used
by some constructors for `optional`.

``` cpp
template<class T, class W>
constexpr bool converts-from-any-cvref =  // exposition only
  disjunction_v<is_constructible<T, W&>, is_convertible<W&, T>,
                is_constructible<T, W>, is_convertible<W, T>,
                is_constructible<T, const W&>, is_convertible<const W&, T>,
                is_constructible<T, const W>, is_convertible<const W, T>>;
```

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

*Effects:* If `rhs` contains a value, direct-non-list-initializes the
contained value with `*rhs`.

*Ensures:* `rhs.has_value() == this->has_value()`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* This constructor is defined as deleted unless
`is_copy_constructible_v<T>` is `true`. If
`is_trivially_copy_constructible_v<T>` is `true`, this constructor is
trivial.

``` cpp
constexpr optional(optional&& rhs) noexcept(see below);
```

*Constraints:* `is_move_constructible_v<T>` is `true`.

*Effects:* If `rhs` contains a value, direct-non-list-initializes the
contained value with `*std::move(rhs)`. `rhs.has_value()` is unchanged.

*Ensures:* `rhs.has_value() == this->has_value()`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The exception specification is equivalent to
`is_nothrow_move_constructible_v<T>`. If
`is_trivially_move_constructible_v<T>` is `true`, this constructor is
trivial.

``` cpp
template<class... Args> constexpr explicit optional(in_place_t, Args&&... args);
```

*Constraints:* `is_constructible_v<T, Args...>` is `true`.

*Effects:* Direct-non-list-initializes the contained value with
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

*Effects:* Direct-non-list-initializes the contained value with
`il, std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If `T`’s constructor selected for the initialization is a
constexpr constructor, this constructor is a constexpr constructor.

``` cpp
template<class U = remove_cv_t<T>> constexpr explicit(see below) optional(U&& v);
```

*Constraints:*

- `is_constructible_v<T, U>` is `true`,
- `is_same_v<remove_cvref_t<U>, in_place_t>` is `false`,
- `is_same_v<remove_cvref_t<U>, optional>` is `false`, and
- if `T` is cv `bool`, `remove_cvref_t<U>` is not a specialization of
  `optional`.

*Effects:* Direct-non-list-initializes the contained value with
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
template<class U> constexpr explicit(see below) optional(const optional<U>& rhs);
```

*Constraints:*

- `is_constructible_v<T, const U&>` is `true`, and
- if `T` is not cv `bool`, *`converts-from-any-cvref`*`<T, optional<U>>`
  is `false`.

*Effects:* If `rhs` contains a value, direct-non-list-initializes the
contained value with `*rhs`.

*Ensures:* `rhs.has_value() == this->has_value()`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<const U&, T>
```

``` cpp
template<class U> constexpr explicit(see below) optional(optional<U>&& rhs);
```

*Constraints:*

- `is_constructible_v<T, U>` is `true`, and
- if `T` is not cv `bool`, *`converts-from-any-cvref`*`<T, optional<U>>`
  is `false`.

*Effects:* If `rhs` contains a value, direct-non-list-initializes the
contained value with `*std::move(rhs)`. `rhs.has_value()` is unchanged.

*Ensures:* `rhs.has_value() == this->has_value()`.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* The expression inside `explicit` is equivalent to:

``` cpp
!is_convertible_v<U, T>
```

#### Destructor <a id="optional.dtor">[[optional.dtor]]</a>

``` cpp
constexpr ~optional();
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
constexpr optional<T>& operator=(nullopt_t) noexcept;
```

*Effects:* If `*this` contains a value, calls `val->T::T̃()` to destroy
the contained value; otherwise no effect.

*Ensures:* `*this` does not contain a value.

*Returns:* `*this`.

``` cpp
constexpr optional<T>& operator=(const optional& rhs);
```

*Effects:* See [[optional.assign.copy]].

**Table: `optional::operator=(const optional&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                            |
| ------------------------------ | ------------------------------------------------------ | ----------------------------------------------------------- |
| `rhs` contains a value         | assigns `*rhs` to the contained value                  | direct-non-list-initializes the contained value with `*rhs` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                   |


*Ensures:* `rhs.has_value() == this->has_value()`.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`this->has_value()` remains unchanged. If an exception is thrown during
the call to `T`’s copy constructor, no effect. If an exception is thrown
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
`rhs.has_value()` remains unchanged.

**Table: `optional::operator=(optional&&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                                       |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `*std::move(rhs)` to the contained value       | direct-non-list-initializes the contained value with `*std::move(rhs)` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                              |


*Ensures:* `rhs.has_value() == this->has_value()`.

*Returns:* `*this`.

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_move_assignable_v<T> && is_nothrow_move_constructible_v<T>
```

If any exception is thrown, the result of the expression
`this->has_value()` remains unchanged. If an exception is thrown during
the call to `T`’s move constructor, the state of `*rhs.val` is
determined by the exception safety guarantee of `T`’s move constructor.
If an exception is thrown during the call to `T`’s move assignment, the
state of `*val` and `*rhs.val` is determined by the exception safety
guarantee of `T`’s move assignment. If
`is_trivially_move_constructible_v<T> &&`
`is_trivially_move_assignable_v<T> &&` `is_trivially_destructible_v<T>`
is `true`, this assignment operator is trivial.

``` cpp
template<class U = remove_cv_t<T>> constexpr optional& operator=(U&& v);
```

*Constraints:*

- `is_same_v<remove_cvref_t<U>, optional>` is `false`,
- `conjunction_v<is_scalar<T>, is_same<T, decay_t<U>>>` is `false`,
- `is_constructible_v<T, U>` is `true`, and
- `is_assignable_v<T&, U>` is `true`.

*Effects:* If `*this` contains a value, assigns `std::forward<U>(v)` to
the contained value; otherwise direct-non-list-initializes the contained
value with `std::forward<U>(v)`.

*Ensures:* `*this` contains a value.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`this->has_value()` remains unchanged. If an exception is thrown during
the call to `T`’s constructor, the state of `v` is determined by the
exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and `v`
is determined by the exception safety guarantee of `T`’s assignment.

``` cpp
template<class U> constexpr optional<T>& operator=(const optional<U>& rhs);
```

*Constraints:*

- `is_constructible_v<T, const U&>` is `true`,
- `is_assignable_v<T&, const U&>` is `true`,
- *`converts-from-any-cvref`*`<T, optional<U>>` is `false`,
- `is_assignable_v<T&, optional<U>&>` is `false`,
- `is_assignable_v<T&, optional<U>&&>` is `false`,
- `is_assignable_v<T&, const optional<U>&>` is `false`, and
- `is_assignable_v<T&, const optional<U>&&>` is `false`.

*Effects:* See [[optional.assign.copy.templ]].

**Table: `optional::operator=(const optional<U>&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                            |
| ------------------------------ | ------------------------------------------------------ | ----------------------------------------------------------- |
| `rhs` contains a value         | assigns `*rhs` to the contained value                  | direct-non-list-initializes the contained value with `*rhs` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                   |


*Ensures:* `rhs.has_value() == this->has_value()`.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`this->has_value()` remains unchanged. If an exception is thrown during
the call to `T`’s constructor, the state of `*rhs.val` is determined by
the exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s
assignment.

``` cpp
template<class U> constexpr optional<T>& operator=(optional<U>&& rhs);
```

*Constraints:*

- `is_constructible_v<T, U>` is `true`,
- `is_assignable_v<T&, U>` is `true`,
- *`converts-from-any-cvref`*`<T, optional<U>>` is `false`,
- `is_assignable_v<T&, optional<U>&>` is `false`,
- `is_assignable_v<T&, optional<U>&&>` is `false`,
- `is_assignable_v<T&, const optional<U>&>` is `false`, and
- `is_assignable_v<T&, const optional<U>&&>` is `false`.

*Effects:* See [[optional.assign.move.templ]]. The result of the
expression `rhs.has_value()` remains unchanged.

**Table: `optional::operator=(optional<U>&&)` effects**

|                                | `*this` contains a value                               | `*this` does not contain a value                                       |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| `rhs` contains a value         | assigns `*std::move(rhs)` to the contained value       | direct-non-list-initializes the contained value with `*std::move(rhs)` |
| `rhs` does not contain a value | destroys the contained value by calling `val->T::~T()` | no effect                                                              |


*Ensures:* `rhs.has_value() == this->has_value()`.

*Returns:* `*this`.

*Remarks:* If any exception is thrown, the result of the expression
`this->has_value()` remains unchanged. If an exception is thrown during
the call to `T`’s constructor, the state of `*rhs.val` is determined by
the exception safety guarantee of `T`’s constructor. If an exception is
thrown during the call to `T`’s assignment, the state of `*val` and
`*rhs.val` is determined by the exception safety guarantee of `T`’s
assignment.

``` cpp
template<class... Args> constexpr T& emplace(Args&&... args);
```

*Mandates:* `is_constructible_v<T, Args...>` is `true`.

*Effects:* Calls `*this = nullopt`. Then direct-non-list-initializes the
contained value with `std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If an exception is thrown during the call to `T`’s
constructor, `*this` does not contain a value, and the previous `*val`
(if any) has been destroyed.

``` cpp
template<class U, class... Args> constexpr T& emplace(initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<T, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Calls `*this = nullopt`. Then direct-non-list-initializes the
contained value with `il, std::forward<Args>(args)...`.

*Ensures:* `*this` contains a value.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown by the selected constructor of `T`.

*Remarks:* If an exception is thrown during the call to `T`’s
constructor, `*this` does not contain a value, and the previous `*val`
(if any) has been destroyed.

#### Swap <a id="optional.swap">[[optional.swap]]</a>

``` cpp
constexpr void swap(optional& rhs) noexcept(see below);
```

*Mandates:* `is_move_constructible_v<T>` is `true`.

*Preconditions:* `T` meets the *Cpp17Swappable*
requirements [[swappable.requirements]].

*Effects:* See [[optional.swap]].

**Table: `optional::swap(optional&)` effects**

|                                | `*this` contains a value                                                                                                                                                                           | `*this` does not contain a value                                                                                                                                                                     |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rhs` contains a value         | calls `swap(*(*this), *rhs)`                                                                                                                                                                       | direct-non-list-initializes the contained value of `*this` with `std::move(*rhs)`, followed by `rhs.val->T::~T()`; postcondition is that `*this` contains a value and `rhs` does not contain a value |
| `rhs` does not contain a value | direct-non-list-initializes the contained value of `rhs` with `std::move(*(*this))`, followed by `val->T::~T()`; postcondition is that `*this` does not contain a value and `rhs` contains a value | no effect                                                                                                                                                                                            |


*Throws:* Any exceptions thrown by the operations in the relevant part
of [[optional.swap]].

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_move_constructible_v<T> && is_nothrow_swappable_v<T>
```

If any exception is thrown, the results of the expressions
`this->has_value()` and `rhs.has_value()` remain unchanged. If an
exception is thrown during the call to function `swap`, the state of
`*val` and `*rhs.val` is determined by the exception safety guarantee of
`swap` for lvalues of `T`. If an exception is thrown during the call to
`T`’s move constructor, the state of `*val` and `*rhs.val` is determined
by the exception safety guarantee of `T`’s move constructor.

#### Iterator support <a id="optional.iterators">[[optional.iterators]]</a>

``` cpp
using iterator       = implementation-defined;
using const_iterator = implementation-defined;
```

These types model `contiguous_iterator`[[iterator.concept.contiguous]],
meet the *Cpp17RandomAccessIterator*
requirements [[random.access.iterators]], and meet the requirements for
constexpr iterators [[iterator.requirements.general]], with value type
`remove_cv_t<T>`. The reference type is `T&` for `iterator` and
`const T&` for `const_iterator`.

All requirements on container iterators [[container.reqmts]] apply to
`optional::iterator` and `optional::const_iterator` as well.

Any operation that initializes or destroys the contained value of an
optional object invalidates all iterators into that object.

``` cpp
constexpr iterator begin() noexcept;
constexpr const_iterator begin() const noexcept;
```

*Returns:* If `has_value()` is `true`, an iterator referring to the
contained value. Otherwise, a past-the-end iterator value.

``` cpp
constexpr iterator end() noexcept;
constexpr const_iterator end() const noexcept;
```

*Returns:* `begin() + has_value()`.

#### Observers <a id="optional.observe">[[optional.observe]]</a>

``` cpp
constexpr const T* operator->() const noexcept;
constexpr T* operator->() noexcept;
```

`has_value()` is `true`.

*Returns:* `val`.

*Remarks:* These functions are constexpr functions.

``` cpp
constexpr const T& operator*() const & noexcept;
constexpr T& operator*() & noexcept;
```

`has_value()` is `true`.

*Returns:* `*val`.

*Remarks:* These functions are constexpr functions.

``` cpp
constexpr T&& operator*() && noexcept;
constexpr const T&& operator*() const && noexcept;
```

`has_value()` is `true`.

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
constexpr const T& value() const &;
constexpr T& value() &;
```

*Effects:* Equivalent to:

``` cpp
return has_value() ? *val : throw bad_optional_access();
```

``` cpp
constexpr T&& value() &&;
constexpr const T&& value() const &&;
```

*Effects:* Equivalent to:

``` cpp
return has_value() ? std::move(*val) : throw bad_optional_access();
```

``` cpp
template<class U = remove_cv_t<T>> constexpr T value_or(U&& v) const &;
```

*Mandates:* `is_copy_constructible_v<T> && is_convertible_v<U&&, T>` is
`true`.

*Effects:* Equivalent to:

``` cpp
return has_value() ? **this : static_cast<T>(std::forward<U>(v));
```

``` cpp
template<class U = remove_cv_t<T>> constexpr T value_or(U&& v) &&;
```

*Mandates:* `is_move_constructible_v<T> && is_convertible_v<U&&, T>` is
`true`.

*Effects:* Equivalent to:

``` cpp
return has_value() ? std::move(**this) : static_cast<T>(std::forward<U>(v));
```

#### Monadic operations <a id="optional.monadic">[[optional.monadic]]</a>

``` cpp
template<class F> constexpr auto and_then(F&& f) &;
template<class F> constexpr auto and_then(F&& f) const &;
```

Let `U` be `invoke_result_t<F, decltype(*`*`val`*`)>`.

*Mandates:* `remove_cvref_t<U>` is a specialization of `optional`.

*Effects:* Equivalent to:

``` cpp
if (*this) {
  return invoke(std::forward<F>(f), *val);
} else {
  return remove_cvref_t<U>();
}
```

``` cpp
template<class F> constexpr auto and_then(F&& f) &&;
template<class F> constexpr auto and_then(F&& f) const &&;
```

Let `U` be `invoke_result_t<F, decltype(std::move(*`*`val`*`))>`.

*Mandates:* `remove_cvref_t<U>` is a specialization of `optional`.

*Effects:* Equivalent to:

``` cpp
if (*this) {
  return invoke(std::forward<F>(f), std::move(*val));
} else {
  return remove_cvref_t<U>();
}
```

``` cpp
template<class F> constexpr auto transform(F&& f) &;
template<class F> constexpr auto transform(F&& f) const &;
```

Let `U` be `remove_cv_t<invoke_result_t<F, decltype(*`*`val`*`)>>`.

*Mandates:* `U` is a valid contained type for `optional`. The
declaration

``` cpp
U u(invoke(std::forward<F>(f), *val));
```

is well-formed for some invented variable `u`.

[*Note 1*: There is no requirement that `U` is
movable [[dcl.init.general]]. — *end note*]

*Returns:* If `*this` contains a value, an `optional<U>` object whose
contained value is direct-non-list-initialized with
`invoke(std::forward<F>(f), *`*`val`*`)`; otherwise, `optional<U>()`.

``` cpp
template<class F> constexpr auto transform(F&& f) &&;
template<class F> constexpr auto transform(F&& f) const &&;
```

Let `U` be
`remove_cv_t<invoke_result_t<F, decltype(std::move(*`*`val`*`))>>`.

*Mandates:* `U` is a valid contained type for `optional`. The
declaration

``` cpp
U u(invoke(std::forward<F>(f), std::move(*val)));
```

is well-formed for some invented variable `u`.

[*Note 2*: There is no requirement that `U` is
movable [[dcl.init.general]]. — *end note*]

*Returns:* If `*this` contains a value, an `optional<U>` object whose
contained value is direct-non-list-initialized with
`invoke(std::forward<F>(f), std::move(*`*`val`*`))`; otherwise,
`optional<U>()`.

``` cpp
template<class F> constexpr optional or_else(F&& f) const &;
```

*Constraints:* `F` models `invocable` and `T` models
`copy_constructible`.

*Mandates:* `is_same_v<remove_cvref_t<invoke_result_t<F>>, optional>` is
`true`.

*Effects:* Equivalent to:

``` cpp
if (*this) {
  return *this;
} else {
  return std::forward<F>(f)();
}
```

``` cpp
template<class F> constexpr optional or_else(F&& f) &&;
```

*Constraints:* `F` models `invocable` and `T` models
`move_constructible`.

*Mandates:* `is_same_v<remove_cvref_t<invoke_result_t<F>>, optional>` is
`true`.

*Effects:* Equivalent to:

``` cpp
if (*this) {
  return std::move(*this);
} else {
  return std::forward<F>(f)();
}
```

#### Modifiers <a id="optional.mod">[[optional.mod]]</a>

``` cpp
constexpr void reset() noexcept;
```

*Effects:* If `*this` contains a value, calls `val->T::T̃()` to destroy
the contained value; otherwise no effect.

*Ensures:* `*this` does not contain a value.

### Partial specialization of `optional` for reference types <a id="optional.optional.ref">[[optional.optional.ref]]</a>

#### General <a id="optional.optional.ref.general">[[optional.optional.ref.general]]</a>

``` cpp
namespace std {
  template<class T>
  class optional<T&> {
  public:
    using value_type     = T;
    using iterator       = implementation-defined;              // see~[optional.ref.iterators]

  public:
    // [optional.ref.ctor], constructors
    constexpr optional() noexcept = default;
    constexpr optional(nullopt_t) noexcept : optional() {}
    constexpr optional(const optional& rhs) noexcept = default;

    template<class Arg>
      constexpr explicit optional(in_place_t, Arg&& arg);
    template<class U>
      constexpr explicit(see below) optional(U&& u) noexcept(see below);
    template<class U>
      constexpr explicit(see below) optional(optional<U>& rhs) noexcept(see below);
    template<class U>
      constexpr explicit(see below) optional(const optional<U>& rhs) noexcept(see below);
    template<class U>
      constexpr explicit(see below) optional(optional<U>&& rhs) noexcept(see below);
    template<class U>
      constexpr explicit(see below) optional(const optional<U>&& rhs) noexcept(see below);

    constexpr ~optional() = default;

    // [optional.ref.assign], assignment
    constexpr optional& operator=(nullopt_t) noexcept;
    constexpr optional& operator=(const optional& rhs) noexcept = default;

    template<class U> constexpr T& emplace(U&& u) noexcept(see below);

    // [optional.ref.swap], swap
    constexpr void swap(optional& rhs) noexcept;

    // [optional.ref.iterators], iterator support
    constexpr iterator begin() const noexcept;
    constexpr iterator end() const noexcept;

    // [optional.ref.observe], observers
    constexpr T*       operator->() const noexcept;
    constexpr T&       operator*() const noexcept;
    constexpr explicit operator bool() const noexcept;
    constexpr bool     has_value() const noexcept;
    constexpr T&       value() const;                           // freestanding-deleted
    template<class U = remove_cv_t<T>>
      constexpr remove_cv_t<T> value_or(U&& u) const;

    // [optional.ref.monadic], monadic operations
    template<class F> constexpr auto and_then(F&& f) const;
    template<class F> constexpr optional<invoke_result_t<F, T&>> transform(F&& f) const;
    template<class F> constexpr optional or_else(F&& f) const;

    // [optional.ref.mod], modifiers
    constexpr void reset() noexcept;

  private:
    T* val = nullptr;                                           // exposition only

    // [optional.ref.expos], exposition only helper functions
    template<class U>
      constexpr void convert-ref-init-val(U&& u);               // exposition only
  };
}
```

An object of type `optional<T&>` *contains a value* if and only if
`val != nullptr` is `true`. When an `optional<T&>` contains a value, the
*contained value* is a reference to `*val`.

#### Constructors <a id="optional.ref.ctor">[[optional.ref.ctor]]</a>

``` cpp
template<class Arg>
  constexpr explicit optional(in_place_t, Arg&& arg);
```

*Constraints:*

- `is_constructible_v<T&, Arg>` is `true`, and
- `reference_constructs_from_temporary_v<T&, Arg>` is `false`.

*Effects:* Equivalent to:
*`convert-ref-init-val`*`(std::forward<Arg>(arg))`.

*Ensures:* `*this` contains a value.

``` cpp
template<class U>
  constexpr explicit(!is_convertible_v<U, T&>)
  optional(U&& u) noexcept(is_nothrow_constructible_v<T&, U>);
```

*Constraints:*

- `is_same_v<remove_cvref_t<U>, optional>` is `false`,
- `is_same_v<remove_cvref_t<U>, in_place_t>` is `false`, and
- `is_constructible_v<T&, U>` is `true`.

*Effects:* Equivalent to:
*`convert-ref-init-val`*`(std::forward<U>(u))`.

*Ensures:* `*this` contains a value.

*Remarks:* This constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<T&, U>
```

is `true`.

``` cpp
template<class U>
  constexpr explicit(!is_convertible_v<U&, T&>)
  optional(optional<U>& rhs) noexcept(is_nothrow_constructible_v<T&, U&>);
```

*Constraints:*

- `is_same_v<remove_cv_t<T>, optional<U>>` is `false`,
- `is_same_v<T&, U>` is `false`, and
- `is_constructible_v<T&, U&>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (rhs.has_value()) convert-ref-init-val(*rhs);
```

*Remarks:* This constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<T&, U&>
```

is `true`.

``` cpp
template<class U>
  constexpr explicit(!is_convertible_v<const U&, T&>)
  optional(const optional<U>& rhs) noexcept(is_nothrow_constructible_v<T&, const U&>);
```

*Constraints:*

- `is_same_v<remove_cv_t<T>, optional<U>>` is `false`,
- `is_same_v<T&, U>` is `false`, and
- `is_constructible_v<T&, const U&>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (rhs.has_value()) convert-ref-init-val(*rhs);
```

*Remarks:* This constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<T&, const U&>
```

is `true`.

``` cpp
template<class U>
  constexpr explicit(!is_convertible_v<U, T&>)
  optional(optional<U>&& rhs) noexcept(is_nothrow_constructible_v<T&, U>);
```

*Constraints:*

- `is_same_v<remove_cv_t<T>, optional<U>>` is `false`,
- `is_same_v<T&, U>` is `false`, and
- `is_constructible_v<T&, U>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (rhs.has_value()) convert-ref-init-val(*std::move(rhs));
```

*Remarks:* This constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<T&, U>
```

is `true`.

``` cpp
template<class U>
  constexpr explicit(!is_convertible_v<const U, T&>)
  optional(const optional<U>&& rhs) noexcept(is_nothrow_constructible_v<T&, const U>);
```

*Constraints:*

- `is_same_v<remove_cv_t<T>, optional<U>>` is `false`,
- `is_same_v<T&, U>` is `false`, and
- `is_constructible_v<T&, const U>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (rhs.has_value()) convert-ref-init-val(*std::move(rhs));
```

*Remarks:* This constructor is defined as deleted if

``` cpp
reference_constructs_from_temporary_v<T&, const U>
```

is `true`.

#### Assignment <a id="optional.ref.assign">[[optional.ref.assign]]</a>

``` cpp
constexpr optional& operator=(nullopt_t) noexcept;
```

*Effects:* Assigns `nullptr` to *val*.

*Ensures:* `*this` does not contain a value.

*Returns:* `*this`.

``` cpp
template<class U>
  constexpr T& emplace(U&& u) noexcept(is_nothrow_constructible_v<T&, U>);
```

*Constraints:*

- `is_constructible_v<T&, U>` is `true`, and
- `reference_constructs_from_temporary_v<T&, U>` is `false`.

*Effects:* Equivalent to:
*`convert-ref-init-val`*`(std::forward<U>(u))`.

*Returns:* `*`*`val`*.

#### Swap <a id="optional.ref.swap">[[optional.ref.swap]]</a>

``` cpp
constexpr void swap(optional& rhs) noexcept;
```

*Effects:* Equivalent to: `swap(`*`val`*`, rhs.`*`val`*`)`.

#### Iterator support <a id="optional.ref.iterators">[[optional.ref.iterators]]</a>

``` cpp
using iterator = implementation-defined;
```

This type models `contiguous_iterator`[[iterator.concept.contiguous]],
meets the *Cpp17RandomAccessIterator*
requirements [[random.access.iterators]], and meets the requirements for
constexpr iterators [[iterator.requirements.general]], with value type
`remove_cv_t<T>`. The reference type is `T&` for `iterator`.

All requirements on container iterators [[container.reqmts]] apply to
`optional::iterator`.

``` cpp
constexpr iterator begin() const noexcept;
```

*Returns:* If `has_value()` is `true`, an iterator referring to
`*`*`val`*. Otherwise, a past-the-end iterator value.

``` cpp
constexpr iterator end() const noexcept;
```

*Returns:* `begin() + has_value()`.

#### Observers <a id="optional.ref.observe">[[optional.ref.observe]]</a>

``` cpp
constexpr T* operator->() const noexcept;
```

`has_value()` is `true`.

*Returns:* *val*.

``` cpp
constexpr T& operator*() const noexcept;
```

`has_value()` is `true`.

*Returns:* `*`*`val`*.

``` cpp
constexpr explicit operator bool() const noexcept;
```

*Returns:* *`val`*` != nullptr`.

``` cpp
constexpr bool has_value() const noexcept;
```

*Returns:* *`val`*` != nullptr`.

``` cpp
constexpr T& value() const;
```

*Effects:* Equivalent to:

``` cpp
return has_value() ? *val : throw bad_optional_access();
```

``` cpp
template<class U = remove_cv_t<T>> constexpr remove_cv_t<T> value_or(U&& u) const;
```

Let `X` be `remove_cv_t<T>`.

*Mandates:* `is_constructible_v<X, T&> && is_convertible_v<U, X>` is
`true`.

*Effects:* Equivalent to:

``` cpp
return has_value() ? *val : static_cast<X>(std::forward<U>(u));
```

#### Monadic operations <a id="optional.ref.monadic">[[optional.ref.monadic]]</a>

``` cpp
template<class F> constexpr auto and_then(F&& f) const;
```

Let `U` be `invoke_result_t<F, T&>`.

*Mandates:* `remove_cvref_t<U>` is a specialization of `optional`.

*Effects:* Equivalent to:

``` cpp
if (has_value()) {
  return invoke(std::forward<F>(f), *val);
} else {
  return remove_cvref_t<U>();
}
```

``` cpp
template<class F>
  constexpr optional<remove_cv_t<invoke_result_t<F, T&>>> transform(F&& f) const;
```

Let `U` be `remove_cv_t<invoke_result_t<F, T&>>`.

*Mandates:* The declaration

``` cpp
U u(invoke(std::forward<F>(f), *val));
```

is well-formed for some invented variable `u`.

[*Note 1*: There is no requirement that `U` is
movable [[dcl.init.general]]. — *end note*]

*Returns:* If `*this` contains a value, an `optional<U>` object whose
contained value is direct-non-list-initialized with
`invoke(std::forward<F>(f), *`*`val`*`)`; otherwise, `optional<U>()`.

``` cpp
template<class F> constexpr optional or_else(F&& f) const;
```

*Constraints:* `F` models `invocable`.

*Mandates:* `is_same_v<remove_cvref_t<invoke_result_t<F>>, optional>` is
`true`.

*Effects:* Equivalent to:

``` cpp
if (has_value()) {
  return *val;
} else {
  return std::forward<F>(f)();
}
```

#### Modifiers <a id="optional.ref.mod">[[optional.ref.mod]]</a>

``` cpp
constexpr void reset() noexcept;
```

*Effects:* Assigns `nullptr` to *val*.

*Ensures:* `*this` does not contain a value.

#### Exposition only helper functions <a id="optional.ref.expos">[[optional.ref.expos]]</a>

``` cpp
template<class U>
  constexpr void convert-ref-init-val(U&& u);  // exposition only
```

*Effects:* Creates a variable `r` as if by `T& r(std::forward<U>(u));`
and then initializes *val* with `addressof(r)`.

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
namespace std {
  class bad_optional_access : public exception {
  public:
    // see [exception] for the specification of the special member functions
    constexpr const char* what() const noexcept override;
  };
}
```

The class `bad_optional_access` defines the type of objects thrown as
exceptions to report the situation where an attempt is made to access
the value of an optional object that does not contain a value.

``` cpp
constexpr const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS, which during constant
evaluation is encoded with the ordinary literal encoding [[lex.ccon]].

### Relational operators <a id="optional.relops">[[optional.relops]]</a>

``` cpp
template<class T, class U> constexpr bool operator==(const optional<T>& x, const optional<U>& y);
```

*Constraints:* The expression `*x == *y` is well-formed and its result
is convertible to `bool`.

[*Note 1*: `T` need not be *Cpp17EqualityComparable*. — *end note*]

*Returns:* If `x.has_value() != y.has_value()`, `false`; otherwise if
`x.has_value() == false`, `true`; otherwise `*x == *y`.

*Remarks:* Specializations of this function template for which
`*x == *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator!=(const optional<T>& x, const optional<U>& y);
```

*Constraints:* The expression `*x != *y` is well-formed and its result
is convertible to `bool`.

*Returns:* If `x.has_value() != y.has_value()`, `true`; otherwise, if
`x.has_value() == false`, `false`; otherwise `*x != *y`.

*Remarks:* Specializations of this function template for which
`*x != *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator<(const optional<T>& x, const optional<U>& y);
```

*Constraints:* `*x < *y` is well-formed and its result is convertible to
`bool`.

*Returns:* If `!y`, `false`; otherwise, if `!x`, `true`; otherwise
`*x < *y`.

*Remarks:* Specializations of this function template for which `*x < *y`
is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator>(const optional<T>& x, const optional<U>& y);
```

*Constraints:* The expression `*x > *y` is well-formed and its result is
convertible to `bool`.

*Returns:* If `!x`, `false`; otherwise, if `!y`, `true`; otherwise
`*x > *y`.

*Remarks:* Specializations of this function template for which `*x > *y`
is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator<=(const optional<T>& x, const optional<U>& y);
```

*Constraints:* The expression `*x <= *y` is well-formed and its result
is convertible to `bool`.

*Returns:* If `!x`, `true`; otherwise, if `!y`, `false`; otherwise
`*x <= *y`.

*Remarks:* Specializations of this function template for which
`*x <= *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, class U> constexpr bool operator>=(const optional<T>& x, const optional<U>& y);
```

*Constraints:* The expression `*x >= *y` is well-formed and its result
is convertible to `bool`.

*Returns:* If `!y`, `true`; otherwise, if `!x`, `false`; otherwise
`*x >= *y`.

*Remarks:* Specializations of this function template for which
`*x >= *y` is a core constant expression are constexpr functions.

``` cpp
template<class T, three_way_comparable_with<T> U>
  constexpr compare_three_way_result_t<T, U>
    operator<=>(const optional<T>& x, const optional<U>& y);
```

*Returns:* If `x && y`, `*x <=> *y`; otherwise
`x.has_value() <=> y.has_value()`.

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

*Returns:* `x.has_value() <=> false`.

### Comparison with `T` <a id="optional.comp.with.t">[[optional.comp.with.t]]</a>

``` cpp
template<class T, class U> constexpr bool operator==(const optional<T>& x, const U& v);
```

*Constraints:* `U` is not a specialization of `optional`. The expression
`*x == v` is well-formed and its result is convertible to `bool`.

[*Note 1*: `T` need not be *Cpp17EqualityComparable*. — *end note*]

*Effects:* Equivalent to: `return x.has_value() ? *x == v : false;`

``` cpp
template<class T, class U> constexpr bool operator==(const T& v, const optional<U>& x);
```

*Constraints:* `T` is not a specialization of `optional`. The expression
`v == *x` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? v == *x : false;`

``` cpp
template<class T, class U> constexpr bool operator!=(const optional<T>& x, const U& v);
```

*Constraints:* `U` is not a specialization of `optional`. The expression
`*x != v` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? *x != v : true;`

``` cpp
template<class T, class U> constexpr bool operator!=(const T& v, const optional<U>& x);
```

*Constraints:* `T` is not a specialization of `optional`. The expression
`v != *x` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? v != *x : true;`

``` cpp
template<class T, class U> constexpr bool operator<(const optional<T>& x, const U& v);
```

*Constraints:* `U` is not a specialization of `optional`. The expression
`*x < v` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? *x < v : true;`

``` cpp
template<class T, class U> constexpr bool operator<(const T& v, const optional<U>& x);
```

*Constraints:* `T` is not a specialization of `optional`. The expression
`v < *x` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? v < *x : false;`

``` cpp
template<class T, class U> constexpr bool operator>(const optional<T>& x, const U& v);
```

*Constraints:* `U` is not a specialization of `optional`. The expression
`*x > v` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? *x > v : false;`

``` cpp
template<class T, class U> constexpr bool operator>(const T& v, const optional<U>& x);
```

*Constraints:* `T` is not a specialization of `optional`. The expression
`v > *x` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? v > *x : true;`

``` cpp
template<class T, class U> constexpr bool operator<=(const optional<T>& x, const U& v);
```

*Constraints:* `U` is not a specialization of `optional`. The expression
`*x <= v` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? *x <= v : true;`

``` cpp
template<class T, class U> constexpr bool operator<=(const T& v, const optional<U>& x);
```

*Constraints:* `T` is not a specialization of `optional`. The expression
`v <= *x` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? v <= *x : false;`

``` cpp
template<class T, class U> constexpr bool operator>=(const optional<T>& x, const U& v);
```

*Constraints:* `U` is not a specialization of `optional`. The expression
`*x >= v` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? *x >= v : false;`

``` cpp
template<class T, class U> constexpr bool operator>=(const T& v, const optional<U>& x);
```

*Constraints:* `T` is not a specialization of `optional`. The expression
`v >= *x` is well-formed and its result is convertible to `bool`.

*Effects:* Equivalent to: `return x.has_value() ? v >= *x : true;`

``` cpp
template<class T, class U>
    requires (!is-derived-from-optional<U>) && three_way_comparable_with<T, U>
  constexpr compare_three_way_result_t<T, U>
    operator<=>(const optional<T>& x, const U& v);
```

*Effects:* Equivalent to:
`return x.has_value() ? *x <=> v : strong_ordering::less;`

### Specialized algorithms <a id="optional.specalg">[[optional.specalg]]</a>

``` cpp
template<class T>
  constexpr void swap(optional<T>& x, optional<T>& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:*

``` cpp
is_reference_v<T> || (is_move_constructible_v<T> && is_swappable_v<T>)
```

is `true`.

*Effects:* Calls `x.swap(y)`.

``` cpp
template<class T> constexpr optional<decay_t<T>> make_optional(T&& v);
```

*Constraints:* The call to `make_optional` does not use an explicit
*template-argument-list* that begins with a type *template-argument*.

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
object `o` of type `optional<T>`, if `o.has_value() == true`, then
`hash<optional<T>>()(o)` evaluates to the same value as
`hash<remove_const_t<T>>()(*o)`; otherwise it evaluates to an
unspecified value. The member functions are not guaranteed to be
`noexcept`.

## Variants <a id="variant">[[variant]]</a>

### General <a id="variant.general">[[variant.general]]</a>

A variant object holds and manages the lifetime of a value. If the
`variant` holds a value, that value’s type has to be one of the template
argument types given to `variant`. These template arguments are called
alternatives.

In [[variant]], *GET* denotes a set of exposition-only function
templates [[variant.get]].

### Header `<variant>` synopsis <a id="variant.syn">[[variant.syn]]</a>

``` cpp
// mostly freestanding
#include <compare>              // see [compare.syn]

namespace std {
  // [variant.variant], class template variant
  template<class... Types>
    class variant;

  // [variant.helper], variant helper classes
  template<class T> struct variant_size;                        // not defined
  template<class T> struct variant_size<const T>;
  template<class T>
    constexpr size_t variant_size_v = variant_size<T>::value;

  template<class... Types>
    struct variant_size<variant<Types...>>;

  template<size_t I, class T> struct variant_alternative;       // not defined
  template<size_t I, class T> struct variant_alternative<I, const T>;
  template<size_t I, class T>
    using variant_alternative_t = variant_alternative<I, T>::type;

  template<size_t I, class... Types>
    struct variant_alternative<I, variant<Types...>>;

  inline constexpr size_t variant_npos = -1;

  // [variant.get], value access
  template<class T, class... Types>
    constexpr bool holds_alternative(const variant<Types...>&) noexcept;

  template<size_t I, class... Types>
    constexpr variant_alternative_t<I, variant<Types...>>&
      get(variant<Types...>&);                                          // freestanding-deleted
  template<size_t I, class... Types>
    constexpr variant_alternative_t<I, variant<Types...>>&&
      get(variant<Types...>&&);                                         // freestanding-deleted
  template<size_t I, class... Types>
    constexpr const variant_alternative_t<I, variant<Types...>>&
      get(const variant<Types...>&);                                    // freestanding-deleted
  template<size_t I, class... Types>
    constexpr const variant_alternative_t<I, variant<Types...>>&&
      get(const variant<Types...>&&);                                   // freestanding-deleted

  template<class T, class... Types>
    constexpr T& get(variant<Types...>&);                               // freestanding-deleted
  template<class T, class... Types>
    constexpr T&& get(variant<Types...>&&);                             // freestanding-deleted
  template<class T, class... Types>
    constexpr const T& get(const variant<Types...>&);                   // freestanding-deleted
  template<class T, class... Types>
    constexpr const T&& get(const variant<Types...>&&);                 // freestanding-deleted

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
    constexpr void swap(variant<Types...>&, variant<Types...>&) noexcept(see below);

  // [variant.bad.access], class bad_variant_access
  class bad_variant_access;

  // [variant.hash], hash support
  template<class T> struct hash;
  template<class... Types> struct hash<variant<Types...>>;
  template<> struct hash<monostate>;
}
```

### Class template `variant` <a id="variant.variant">[[variant.variant]]</a>

#### General <a id="variant.variant.general">[[variant.variant.general]]</a>

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
    constexpr ~variant();

    // [variant.assign], assignment
    constexpr variant& operator=(const variant&);
    constexpr variant& operator=(variant&&) noexcept(see below);

    template<class T> constexpr variant& operator=(T&&) noexcept(see below);

    // [variant.mod], modifiers
    template<class T, class... Args>
      constexpr T& emplace(Args&&...);
    template<class T, class U, class... Args>
      constexpr T& emplace(initializer_list<U>, Args&&...);
    template<size_t I, class... Args>
      constexpr variant_alternative_t<I, variant<Types...>>& emplace(Args&&...);
    template<size_t I, class U, class... Args>
      constexpr variant_alternative_t<I, variant<Types...>>&
        emplace(initializer_list<U>, Args&&...);

    // [variant.status], value status
    constexpr bool valueless_by_exception() const noexcept;
    constexpr size_t index() const noexcept;

    // [variant.swap], swap
    constexpr void swap(variant&) noexcept(see below);

    // [variant.visit], visitation
    template<class Self, class Visitor>
      constexpr decltype(auto) visit(this Self&&, Visitor&&);
    template<class R, class Self, class Visitor>
      constexpr R visit(this Self&&, Visitor&&);
  };
}
```

Any instance of `variant` at any given time either holds a value of one
of its alternative types or holds no value. When an instance of
`variant` holds a value of alternative type `T`, it means that a value
of type `T`, referred to as the `variant` object’s *contained value*, is
nested within [[intro.object]] the `variant` object.

All types in `Types` shall meet the *Cpp17Destructible* requirements (
[[cpp17.destructible]]).

A program that instantiates the definition of `variant` with no template
arguments is ill-formed.

If a program declares an explicit or partial specialization of
`variant`, the program is ill-formed, no diagnostic required.

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
value-initialization of the alternative type `T₀` would be
constexpr-suitable [[dcl.constexpr]]. The exception specification is
equivalent to `is_nothrow_default_constructible_v<``T₀``>`.

[*Note 1*: See also class `monostate`. — *end note*]

``` cpp
constexpr variant(const variant& w);
```

*Effects:* If `w` holds a value, initializes the `variant` to hold the
same alternative as `w` and direct-initializes the contained value with
*`GET`*`<j>(w)`, where `j` is `w.index()`. Otherwise, initializes the
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
*`GET`*`<j>(std::move(w))`, where `j` is `w.index()`. Otherwise,
initializes the `variant` to not hold a value.

*Throws:* Any exception thrown by move-constructing any `Tᵢ` for all i.

*Remarks:* The exception specification is equivalent to the logical of
`is_nothrow_move_constructible_v<``Tᵢ``>` for all i. If
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
direct-non-list-initializes the contained value with
`std::forward<T>(t)`.

*Ensures:* `holds_alternative<``Tⱼ``>(*this)` is `true`.

*Throws:* Any exception thrown by the initialization of the selected
alternative `Tⱼ`.

*Remarks:* The exception specification is equivalent to
`is_nothrow_constructible_v<``Tⱼ``, T>`. If `Tⱼ`’s selected constructor
is a constexpr constructor, this constructor is a constexpr constructor.

``` cpp
template<class T, class... Args> constexpr explicit variant(in_place_type_t<T>, Args&&... args);
```

*Constraints:*

- There is exactly one occurrence of `T` in `Types...` and
- `is_constructible_v<T, Args...>` is `true`.

*Effects:* Direct-non-list-initializes the contained value of type `T`
with `std::forward<Args>(args)...`.

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

*Effects:* Direct-non-list-initializes the contained value of type `T`
with `il, std::forward<Args>(args)...`.

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

*Effects:* Direct-non-list-initializes the contained value of type `T_I`
with `std::forward<Args>(args)...`.

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

*Effects:* Direct-non-list-initializes the contained value of type `T_I`
with `il, std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Remarks:* If `T_I`’s selected constructor is a constexpr constructor,
this constructor is a constexpr constructor.

#### Destructor <a id="variant.dtor">[[variant.dtor]]</a>

``` cpp
constexpr ~variant();
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
  equivalent to `emplace<`j`>(`*`GET`*`<`j`>(rhs))`.
- Otherwise, equivalent to `operator=(variant(rhs))`.

*Ensures:* `index() == rhs.index()`.

*Returns:* `*this`.

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
- Otherwise, if `index() == `j, assigns *`GET`*`<`j`>(std::move(rhs))`
  to the value contained in `*this`.
- Otherwise, equivalent to
  `emplace<`j`>(`*`GET`*`<`j`>(std::move(rhs)))`.

*Returns:* `*this`.

*Remarks:* If `is_trivially_move_constructible_v<``Tᵢ``> &&`
`is_trivially_move_assignable_v<``Tᵢ``> &&`
`is_trivially_destructible_v<``Tᵢ``>` is `true` for all i, this
assignment operator is trivial. The exception specification is
equivalent to
`is_nothrow_move_constructible_v<``Tᵢ``> && is_nothrow_move_assignable_v<``Tᵢ``>`
for all i.

- If an exception is thrown during the call to `Tⱼ`’s move construction
  (with j being `rhs.index()`), the `variant` will hold no value.
- If an exception is thrown during the call to `Tⱼ`’s move assignment,
  the state of the contained value is as defined by the exception safety
  guarantee of `Tⱼ`’s move assignment; `index()` will be j.

``` cpp
template<class T> constexpr variant& operator=(T&& t) noexcept(see below);
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
  \[*Note 2*:
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
- Otherwise, equivalent to `emplace<`j`>(``Tⱼ``(std::forward<T>(t)))`.

*Ensures:* `holds_alternative<``Tⱼ``>(*this)` is `true`, with `Tⱼ`
selected by the imaginary function overload resolution described above.

*Returns:* `*this`.

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_assignable_v<Tⱼ&, T> && is_nothrow_constructible_v<Tⱼ, T>
```

- If an exception is thrown during the assignment of
  `std::forward<T>(t)` to the value contained in `*this`, the state of
  the contained value and `t` are as defined by the exception safety
  guarantee of the assignment expression; `valueless_by_exception()`
  will be `false`.
- If an exception is thrown during the initialization of the contained
  value, the `variant` object is permitted to not hold a value.

#### Modifiers <a id="variant.mod">[[variant.mod]]</a>

``` cpp
template<class T, class... Args> constexpr T& emplace(Args&&... args);
```

*Constraints:* `is_constructible_v<T, Args...>` is `true`, and `T`
occurs exactly once in `Types`.

*Effects:* Equivalent to:

``` cpp
return emplace<I>(std::forward<Args>(args)...);
```

where I is the zero-based index of `T` in `Types`.

``` cpp
template<class T, class U, class... Args>
  constexpr T& emplace(initializer_list<U> il, Args&&... args);
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
  constexpr variant_alternative_t<I, variant<Types...>>& emplace(Args&&... args);
```

*Mandates:* `I` < `sizeof...(Types)`.

*Constraints:* `is_constructible_v<``T_I``, Args...>` is `true`.

*Effects:* Destroys the currently contained value if
`valueless_by_exception()` is `false`. Then direct-non-list-initializes
the contained value of type `T_I` with the arguments
`std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown during the initialization of the
contained value.

*Remarks:* If an exception is thrown during the initialization of the
contained value, the `variant` is permitted to not hold a value.

``` cpp
template<size_t I, class U, class... Args>
  constexpr variant_alternative_t<I, variant<Types...>>&
    emplace(initializer_list<U> il, Args&&... args);
```

*Mandates:* `I` < `sizeof...(Types)`.

*Constraints:*
`is_constructible_v<``T_I``, initializer_list<U>&, Args...>` is `true`.

*Effects:* Destroys the currently contained value if
`valueless_by_exception()` is `false`. Then direct-non-list-initializes
the contained value of type `T_I` with
`il, std::forward<Args>(args)...`.

*Ensures:* `index()` is `I`.

*Returns:* A reference to the new contained value.

*Throws:* Any exception thrown during the initialization of the
contained value.

*Remarks:* If an exception is thrown during the initialization of the
contained value, the `variant` is permitted to not hold a value.

#### Value status <a id="variant.status">[[variant.status]]</a>

``` cpp
constexpr bool valueless_by_exception() const noexcept;
```

*Effects:* Returns `false` if and only if the `variant` holds a value.

[*Note 1*:

It is possible for a `variant` to hold no value if an exception is
thrown during a type-changing assignment or emplacement. The latter
means that even a `variant<float, int>` can become
`valueless_by_exception()`, for instance by

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
constexpr void swap(variant& rhs) noexcept(see below);
```

*Mandates:* `is_move_constructible_v<``Tᵢ``>` is `true` for all i.

*Preconditions:* Each `Tᵢ` meets the *Cpp17Swappable*
requirements [[swappable.requirements]].

*Effects:*

- If `valueless_by_exception() && rhs.valueless_by_exception()` no
  effect.
- Otherwise, if `index() == rhs.index()`, calls
  `swap(`*`GET`*`<`i`>(*this), `*`GET`*`<`i`>(rhs))` where i is
  `index()`.
- Otherwise, exchanges values of `rhs` and `*this`.

*Throws:* If `index() == rhs.index()`, any exception thrown by
`swap(`*`GET`*`<`i`>(*this), `*`GET`*`<`i`>(rhs))` with i being
`index()`. Otherwise, any exception thrown by the move constructor of
`Tᵢ` or `Tⱼ` with i being `index()` and j being `rhs.index()`.

*Remarks:* If an exception is thrown during the call to function
`swap(`*`GET`*`<`i`>(*this), `*`GET`*`<`i`>(rhs))`, the states of the
contained values of `*this` and of `rhs` are determined by the exception
safety guarantee of `swap` for lvalues of `Tᵢ` with i being `index()`.
If an exception is thrown during the exchange of the values of `*this`
and `rhs`, the states of the values of `*this` and of `rhs` are
determined by the exception safety guarantee of `variant`’s move
constructor. The exception specification is equivalent to the logical of
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
template<class T> struct variant_size<const T>;
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
template<size_t I, class T> struct variant_alternative<I, const T>;
```

Let `VA` denote `variant_alternative<I, T>` of the cv-unqualified type
`T`. Then each specialization of the template meets the
*Cpp17TransformationTrait* requirements [[meta.rqmts]] with a member
typedef `type` that names the type `add_const_t<VA::type>`.

``` cpp
variant_alternative<I, variant<Types...>>::type
```

*Mandates:* `I` < `sizeof...(Types)`.

*Result:* The type `T_I`.

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
  constexpr variant_alternative_t<I, variant<Types...>>&
    GET(variant<Types...>& v);                                  // exposition only
template<size_t I, class... Types>
  constexpr variant_alternative_t<I, variant<Types...>>&&
    GET(variant<Types...>&& v);                                 // exposition only
template<size_t I, class... Types>
  constexpr const variant_alternative_t<I, variant<Types...>>&
    GET(const variant<Types...>& v);                            // exposition only
template<size_t I, class... Types>
  constexpr const variant_alternative_t<I, variant<Types...>>&&
    GET(const variant<Types...>&& v);                           // exposition only
```

*Mandates:* `I` < `sizeof...(Types)`.

*Preconditions:* `v.index()` is `I`.

*Returns:* A reference to the object stored in the `variant`.

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

*Constraints:* *`GET`*`<`i`>(v) == `*`GET`*`<`i`>(w)` is a valid
expression that is convertible to `bool`, for all i.

*Returns:* If `v.index() != w.index()`, `false`; otherwise if
`v.valueless_by_exception()`, `true`; otherwise
*`GET`*`<`i`>(v) == `*`GET`*`<`i`>(w)` with i being `v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator!=(const variant<Types...>& v, const variant<Types...>& w);
```

*Constraints:* *`GET`*`<`i`>(v) != `*`GET`*`<`i`>(w)` is a valid
expression that is convertible to `bool`, for all i.

*Returns:* If `v.index() != w.index()`, `true`; otherwise if
`v.valueless_by_exception()`, `false`; otherwise
*`GET`*`<`i`>(v) != `*`GET`*`<`i`>(w)` with i being `v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator<(const variant<Types...>& v, const variant<Types...>& w);
```

*Constraints:* *`GET`*`<`i`>(v) < `*`GET`*`<`i`>(w)` is a valid
expression that is convertible to `bool`, for all i.

*Returns:* If `w.valueless_by_exception()`, `false`; otherwise if
`v.valueless_by_exception()`, `true`; otherwise, if
`v.index() < w.index()`, `true`; otherwise if `v.index() > w.index()`,
`false`; otherwise *`GET`*`<`i`>(v) < `*`GET`*`<`i`>(w)` with i being
`v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator>(const variant<Types...>& v, const variant<Types...>& w);
```

*Constraints:* *`GET`*`<`i`>(v) > `*`GET`*`<`i`>(w)` is a valid
expression that is convertible to `bool`, for all i.

*Returns:* If `v.valueless_by_exception()`, `false`; otherwise if
`w.valueless_by_exception()`, `true`; otherwise, if
`v.index() > w.index()`, `true`; otherwise if `v.index() < w.index()`,
`false`; otherwise *`GET`*`<`i`>(v) > `*`GET`*`<`i`>(w)` with i being
`v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator<=(const variant<Types...>& v, const variant<Types...>& w);
```

*Constraints:* *`GET`*`<`i`>(v) <= `*`GET`*`<`i`>(w)` is a valid
expression that is convertible to `bool`, for all i.

*Returns:* If `v.valueless_by_exception()`, `true`; otherwise if
`w.valueless_by_exception()`, `false`; otherwise, if
`v.index() < w.index()`, `true`; otherwise if `v.index() > w.index()`,
`false`; otherwise *`GET`*`<`i`>(v) <= `*`GET`*`<`i`>(w)` with i being
`v.index()`.

``` cpp
template<class... Types>
  constexpr bool operator>=(const variant<Types...>& v, const variant<Types...>& w);
```

*Constraints:* *`GET`*`<`i`>(v) >= `*`GET`*`<`i`>(w)` is a valid
expression that is convertible to `bool`, for all i.

*Returns:* If `w.valueless_by_exception()`, `true`; otherwise if
`v.valueless_by_exception()`, `false`; otherwise, if
`v.index() > w.index()`, `true`; otherwise if `v.index() < w.index()`,
`false`; otherwise *`GET`*`<`i`>(v) >= `*`GET`*`<`i`>(w)` with i being
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
return GET<i>(v) <=> GET<i>(w);
```

with i being `v.index()`.

### Visitation <a id="variant.visit">[[variant.visit]]</a>

``` cpp
template<class Visitor, class... Variants>
  constexpr see below visit(Visitor&& vis, Variants&&... vars);
template<class R, class Visitor, class... Variants>
  constexpr R visit(Visitor&& vis, Variants&&... vars);
```

Let *as-variant* denote the following exposition-only function
templates:

``` cpp
template<class... Ts>
  constexpr auto&& as-variant(variant<Ts...>& var) { return var; }
template<class... Ts>
  constexpr auto&& as-variant(const variant<Ts...>& var) { return var; }
template<class... Ts>
  constexpr auto&& as-variant(variant<Ts...>&& var) { return std::move(var); }
template<class... Ts>
  constexpr auto&& as-variant(const variant<Ts...>&& var) { return std::move(var); }
```

Let n be `sizeof...(Variants)`. For each 0 ≤ i < n, let `Vᵢ` denote the
type
`decltype(`*`as-variant`*`(``std::forward<``Variantsᵢ``>(``varsᵢ``)``))`.

*Constraints:* `Vᵢ` is a valid type for all 0 ≤ i < n.

Let `V` denote the pack of types `Vᵢ`.

Let m be a pack of n values of type `size_t`. Such a pack is valid if
0 ≤ m_i < `variant_size_v<remove_reference_t<Vᵢ``>>` for all 0 ≤ i < n.
For each valid pack m, let e(m) denote the expression:

``` cpp
INVOKE(std::forward<Visitor>(vis), GET<m>(std::forward<V>(vars))...)  // see REF:func.require
```

for the first form and

``` cpp
INVOKE<R>(std::forward<Visitor>(vis), GET<m>(std::forward<V>(vars))...)  // see REF:func.require
```

for the second form.

*Mandates:* For each valid pack m, e(m) is a valid expression. All such
expressions are of the same type and value category.

*Returns:* e(m), where m is the pack for which mᵢ is
*`as-variant`*`(vars`ᵢ`).index()` for all 0 ≤ i < n. The return type is
`decltype(`e(m)`)` for the first form.

*Throws:* `bad_variant_access` if
`(`*`as-variant`*`(vars).valueless_by_exception() || ...)` is `true`.

*Complexity:* For n ≤ 1, the invocation of the callable object is
implemented in constant time, i.e., for n = 1, it does not depend on the
number of alternative types of `V₀`. For n > 1, the invocation of the
callable object has no complexity requirements.

``` cpp
template<class Self, class Visitor>
  constexpr decltype(auto) visit(this Self&& self, Visitor&& vis);
```

Let `V` be
*`OVERRIDE_REF`*`(Self&&, `*`COPY_CONST`*`(remove_reference_t<Self>, variant))`[[forward]].

*Constraints:* The call to `visit` does not use an explicit
*template-argument-list* that begins with a type *template-argument*.

*Effects:* Equivalent to:
`return std::visit(std::forward<Visitor>(vis), (V)self);`

``` cpp
template<class R, class Self, class Visitor>
  constexpr R visit(this Self&& self, Visitor&& vis);
```

Let `V` be
*`OVERRIDE_REF`*`(Self&&, `*`COPY_CONST`*`(remove_reference_t<Self>, variant))`[[forward]].

*Effects:* Equivalent to:
`return std::visit<R>(std::forward<Visitor>(vis), (V)self);`

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
  constexpr void swap(variant<Types...>& v, variant<Types...>& w) noexcept(see below);
```

*Constraints:*
`is_move_constructible_v<``Tᵢ``> && is_swappable_v<``Tᵢ``>` is `true`
for all i.

*Effects:* Equivalent to `v.swap(w)`.

*Remarks:* The exception specification is equivalent to
`noexcept(v.swap(w))`.

### Class `bad_variant_access` <a id="variant.bad.access">[[variant.bad.access]]</a>

``` cpp
namespace std {
  class bad_variant_access : public exception {
  public:
    // see [exception] for the specification of the special member functions
    constexpr const char* what() const noexcept override;
  };
}
```

Objects of type `bad_variant_access` are thrown to report invalid
accesses to the value of a `variant` object.

``` cpp
constexpr const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS, which during constant
evaluation is encoded with the ordinary literal encoding [[lex.ccon]].

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

### General <a id="any.general">[[any.general]]</a>

Subclause [[any]] describes components that C++ programs may use to
perform operations on objects of a discriminated type.

[*Note 1*: The discriminated type can contain values of different types
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
namespace std {
  class bad_any_cast : public bad_cast {
  public:
    // see [exception] for the specification of the special member functions
    const char* what() const noexcept override;
  };
}
```

Objects of type `bad_any_cast` are thrown by a failed `any_cast`
[[any.nonmembers]].

``` cpp
const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS.

### Class `any` <a id="any.class">[[any.class]]</a>

#### General <a id="any.class.general">[[any.class.general]]</a>

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

*Effects:* Direct-non-list-initializes the contained value of type `VT`
with `std::forward<Args>(args)...`.

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

*Effects:* Direct-non-list-initializes the contained value of type `VT`
with `il, std::forward<Args>(args)...`.

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

*Ensures:* The state of `*this` is equivalent to the original state of
`rhs`.

*Returns:* `*this`.

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

*Effects:* Calls `reset()`. Then direct-non-list-initializes the
contained value of type `VT` with `std::forward<Args>(args)...`.

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

*Effects:* Calls `reset()`. Then direct-non-list-initializes the
contained value of type `VT` with `il, std::forward<Args>(args)...`.

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

*Mandates:* `is_void_v<T>` is `false`.

*Returns:* If `operand != nullptr && operand->type() == typeid(T)` is
`true`, a pointer to the object contained by `operand`; otherwise,
`nullptr`.

[*Example 2*:

``` cpp
bool is_string(const any& operand) {
  return any_cast<string>(&operand) != nullptr;
}
```

— *end example*]

## Expected objects <a id="expected">[[expected]]</a>

### General <a id="expected.general">[[expected.general]]</a>

Subclause [[expected]] describes the class template `expected` that
represents expected objects. An `expected<T, E>` object holds an object
of type `T` or an object of type `E` and manages the lifetime of the
contained objects.

### Header `<expected>` synopsis <a id="expected.syn">[[expected.syn]]</a>

``` cpp
// mostly freestanding
namespace std {
  // [expected.unexpected], class template unexpected
  template<class E> class unexpected;

  // [expected.bad], class template bad_expected_access
  template<class E> class bad_expected_access;

  // [expected.bad.void], specialization for void
  template<> class bad_expected_access<void>;

  // in-place construction of unexpected values
  struct unexpect_t {
    explicit unexpect_t() = default;
  };
  inline constexpr unexpect_t unexpect{};

  // [expected.expected], class template expected
  template<class T, class E> class expected;                                // partially freestanding

  // [expected.void], partial specialization of expected for void types
  template<class T, class E> requires is_void_v<T> class expected<T, E>;    // partially freestanding
}
```

### Class template `unexpected` <a id="expected.unexpected">[[expected.unexpected]]</a>

#### General <a id="expected.un.general">[[expected.un.general]]</a>

Subclause [[expected.unexpected]] describes the class template
`unexpected` that represents unexpected objects stored in `expected`
objects.

``` cpp
namespace std {
  template<class E>
  class unexpected {
  public:
    // [expected.un.cons], constructors
    constexpr unexpected(const unexpected&) = default;
    constexpr unexpected(unexpected&&) = default;
    template<class Err = E>
      constexpr explicit unexpected(Err&&);
    template<class... Args>
      constexpr explicit unexpected(in_place_t, Args&&...);
    template<class U, class... Args>
      constexpr explicit unexpected(in_place_t, initializer_list<U>, Args&&...);

    constexpr unexpected& operator=(const unexpected&) = default;
    constexpr unexpected& operator=(unexpected&&) = default;

    constexpr const E& error() const & noexcept;
    constexpr E& error() & noexcept;
    constexpr const E&& error() const && noexcept;
    constexpr E&& error() && noexcept;

    constexpr void swap(unexpected& other) noexcept(see below);

    template<class E2>
      friend constexpr bool operator==(const unexpected&, const unexpected<E2>&);

    friend constexpr void swap(unexpected& x, unexpected& y) noexcept(noexcept(x.swap(y)));

  private:
    E unex;             // exposition only
  };

  template<class E> unexpected(E) -> unexpected<E>;
}
```

A program that instantiates the definition of `unexpected` for a
non-object type, an array type, a specialization of `unexpected`, or a
cv-qualified type is ill-formed.

#### Constructors <a id="expected.un.cons">[[expected.un.cons]]</a>

``` cpp
template<class Err = E>
  constexpr explicit unexpected(Err&& e);
```

*Constraints:*

- `is_same_v<remove_cvref_t<Err>, unexpected>` is `false`; and
- `is_same_v<remove_cvref_t<Err>, in_place_t>` is `false`; and
- `is_constructible_v<E, Err>` is `true`.

*Effects:* Direct-non-list-initializes *unex* with
`std::forward<Err>(e)`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
template<class... Args>
  constexpr explicit unexpected(in_place_t, Args&&... args);
```

*Constraints:* `is_constructible_v<E, Args...>` is `true`.

*Effects:* Direct-non-list-initializes *unex* with
`std::forward<Args>(args)...`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
template<class U, class... Args>
  constexpr explicit unexpected(in_place_t, initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<E, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Direct-non-list-initializes *unex* with
`il, std::forward<Args>(args)...`.

*Throws:* Any exception thrown by the initialization of *unex*.

#### Observers <a id="expected.un.obs">[[expected.un.obs]]</a>

``` cpp
constexpr const E& error() const & noexcept;
constexpr E& error() & noexcept;
```

*Returns:* *unex*.

``` cpp
constexpr E&& error() && noexcept;
constexpr const E&& error() const && noexcept;
```

*Returns:* `std::move(`*`unex`*`)`.

#### Swap <a id="expected.un.swap">[[expected.un.swap]]</a>

``` cpp
constexpr void swap(unexpected& other) noexcept(is_nothrow_swappable_v<E>);
```

*Mandates:* `is_swappable_v<E>` is `true`.

*Effects:* Equivalent to:
`using std::swap; swap(`*`unex`*`, other.`*`unex`*`);`

``` cpp
friend constexpr void swap(unexpected& x, unexpected& y) noexcept(noexcept(x.swap(y)));
```

*Constraints:* `is_swappable_v<E>` is `true`.

*Effects:* Equivalent to `x.swap(y)`.

#### Equality operator <a id="expected.un.eq">[[expected.un.eq]]</a>

``` cpp
template<class E2>
  friend constexpr bool operator==(const unexpected& x, const unexpected<E2>& y);
```

*Mandates:* The expression `x.error() == y.error()` is well-formed and
its result is convertible to `bool`.

*Returns:* `x.error() == y.error()`.

### Class template `bad_expected_access` <a id="expected.bad">[[expected.bad]]</a>

``` cpp
namespace std {
  template<class E>
  class bad_expected_access : public bad_expected_access<void> {
  public:
    constexpr explicit bad_expected_access(E);
    constexpr const char* what() const noexcept override;
    constexpr E& error() & noexcept;
    constexpr const E& error() const & noexcept;
    constexpr E&& error() && noexcept;
    constexpr const E&& error() const && noexcept;

  private:
    E unex;             // exposition only
  };
}
```

The class template `bad_expected_access` defines the type of objects
thrown as exceptions to report the situation where an attempt is made to
access the value of an `expected<T, E>` object for which `has_value()`
is `false`.

``` cpp
constexpr explicit bad_expected_access(E e);
```

*Effects:* Initializes *unex* with `std::move(e)`.

``` cpp
constexpr const E& error() const & noexcept;
constexpr E& error() & noexcept;
```

*Returns:* *unex*.

``` cpp
constexpr E&& error() && noexcept;
constexpr const E&& error() const && noexcept;
```

*Returns:* `std::move(`*`unex`*`)`.

``` cpp
constexpr const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS, which during constant
evaluation is encoded with the ordinary literal encoding [[lex.ccon]].

### Class template specialization `bad_expected_access<void>` <a id="expected.bad.void">[[expected.bad.void]]</a>

``` cpp
namespace std {
  template<>
  class bad_expected_access<void> : public exception {
  protected:
    constexpr bad_expected_access() noexcept;
    constexpr bad_expected_access(const bad_expected_access&) noexcept;
    constexpr bad_expected_access(bad_expected_access&&) noexcept;
    constexpr bad_expected_access& operator=(const bad_expected_access&) noexcept;
    constexpr bad_expected_access& operator=(bad_expected_access&&) noexcept;
    constexpr ~bad_expected_access();

  public:
    constexpr const char* what() const noexcept override;
  };
}
```

``` cpp
constexpr const char* what() const noexcept override;
```

*Returns:* An *implementation-defined* NTBS, which during constant
evaluation is encoded with the ordinary literal encoding [[lex.ccon]].

### Class template `expected` <a id="expected.expected">[[expected.expected]]</a>

#### General <a id="expected.object.general">[[expected.object.general]]</a>

``` cpp
namespace std {
  template<class T, class E>
  class expected {
  public:
    using value_type = T;
    using error_type = E;
    using unexpected_type = unexpected<E>;

    template<class U>
    using rebind = expected<U, error_type>;

    // [expected.object.cons], constructors
    constexpr expected();
    constexpr expected(const expected&);
    constexpr expected(expected&&) noexcept(see below);
    template<class U, class G>
      constexpr explicit(see below) expected(const expected<U, G>&);
    template<class U, class G>
      constexpr explicit(see below) expected(expected<U, G>&&);

    template<class U = remove_cv_t<T>>
      constexpr explicit(see below) expected(U&& v);

    template<class G>
      constexpr explicit(see below) expected(const unexpected<G>&);
    template<class G>
      constexpr explicit(see below) expected(unexpected<G>&&);

    template<class... Args>
      constexpr explicit expected(in_place_t, Args&&...);
    template<class U, class... Args>
      constexpr explicit expected(in_place_t, initializer_list<U>, Args&&...);
    template<class... Args>
      constexpr explicit expected(unexpect_t, Args&&...);
    template<class U, class... Args>
      constexpr explicit expected(unexpect_t, initializer_list<U>, Args&&...);

    // [expected.object.dtor], destructor
    constexpr ~expected();

    // [expected.object.assign], assignment
    constexpr expected& operator=(const expected&);
    constexpr expected& operator=(expected&&) noexcept(see below);
    template<class U = remove_cv_t<T>> constexpr expected& operator=(U&&);
    template<class G>
      constexpr expected& operator=(const unexpected<G>&);
    template<class G>
      constexpr expected& operator=(unexpected<G>&&);

    template<class... Args>
      constexpr T& emplace(Args&&...) noexcept;
    template<class U, class... Args>
      constexpr T& emplace(initializer_list<U>, Args&&...) noexcept;

    // [expected.object.swap], swap
    constexpr void swap(expected&) noexcept(see below);
    friend constexpr void swap(expected& x, expected& y) noexcept(noexcept(x.swap(y)));

    // [expected.object.obs], observers
    constexpr const T* operator->() const noexcept;
    constexpr T* operator->() noexcept;
    constexpr const T& operator*() const & noexcept;
    constexpr T& operator*() & noexcept;
    constexpr const T&& operator*() const && noexcept;
    constexpr T&& operator*() && noexcept;
    constexpr explicit operator bool() const noexcept;
    constexpr bool has_value() const noexcept;
    constexpr const T& value() const &;                                     // freestanding-deleted
    constexpr T& value() &;                                                 // freestanding-deleted
    constexpr const T&& value() const &&;                                   // freestanding-deleted
    constexpr T&& value() &&;                                               // freestanding-deleted
    constexpr const E& error() const & noexcept;
    constexpr E& error() & noexcept;
    constexpr const E&& error() const && noexcept;
    constexpr E&& error() && noexcept;
    template<class U = remove_cv_t<T>> constexpr T value_or(U&&) const &;
    template<class U = remove_cv_t<T>> constexpr T value_or(U&&) &&;
    template<class G = E> constexpr E error_or(G&&) const &;
    template<class G = E> constexpr E error_or(G&&) &&;

    // [expected.object.monadic], monadic operations
    template<class F> constexpr auto and_then(F&& f) &;
    template<class F> constexpr auto and_then(F&& f) &&;
    template<class F> constexpr auto and_then(F&& f) const &;
    template<class F> constexpr auto and_then(F&& f) const &&;
    template<class F> constexpr auto or_else(F&& f) &;
    template<class F> constexpr auto or_else(F&& f) &&;
    template<class F> constexpr auto or_else(F&& f) const &;
    template<class F> constexpr auto or_else(F&& f) const &&;
    template<class F> constexpr auto transform(F&& f) &;
    template<class F> constexpr auto transform(F&& f) &&;
    template<class F> constexpr auto transform(F&& f) const &;
    template<class F> constexpr auto transform(F&& f) const &&;
    template<class F> constexpr auto transform_error(F&& f) &;
    template<class F> constexpr auto transform_error(F&& f) &&;
    template<class F> constexpr auto transform_error(F&& f) const &;
    template<class F> constexpr auto transform_error(F&& f) const &&;

    // [expected.object.eq], equality operators
    template<class T2, class E2> requires (!is_void_v<T2>)
      friend constexpr bool operator==(const expected& x, const expected<T2, E2>& y);
    template<class T2>
      friend constexpr bool operator==(const expected&, const T2&);
    template<class E2>
      friend constexpr bool operator==(const expected&, const unexpected<E2>&);

  private:
    bool has_val;       // exposition only
    union {
      T val;            // exposition only
      E unex;           // exposition only
    };
  };
}
```

Any object of type `expected<T, E>` either contains a value of type `T`
or a value of type `E` nested within [[intro.object]] it. Member
*has_val* indicates whether the `expected<T, E>` object contains an
object of type `T`.

A type `T` is a *valid value type for `expected`*, if `remove_cv_t<T>`
is `void` or a complete non-array object type that is not `in_place_t`,
`unexpect_t`, or a specialization of `unexpected`. A program which
instantiates class template `expected<T, E>` with an argument `T` that
is not a valid value type for `expected` is ill-formed. A program that
instantiates the definition of the template `expected<T, E>` with a type
for the `E` parameter that is not a valid template argument for
`unexpected` is ill-formed.

When `T` is not cv `void`, it shall meet the *Cpp17Destructible*
requirements ([[cpp17.destructible]]). `E` shall meet the
*Cpp17Destructible* requirements.

#### Constructors <a id="expected.object.cons">[[expected.object.cons]]</a>

The exposition-only variable template *converts-from-any-cvref* defined
in [[optional.ctor]] is used by some constructors for `expected`.

``` cpp
constexpr expected();
```

*Constraints:* `is_default_constructible_v<T>` is `true`.

*Effects:* Value-initializes *val*.

*Ensures:* `has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *val*.

``` cpp
constexpr expected(const expected& rhs);
```

*Effects:* If `rhs.has_value()` is `true`, direct-non-list-initializes
*val* with `*rhs`. Otherwise, direct-non-list-initializes *unex* with
`rhs.error()`.

*Ensures:* `rhs.has_value() == this->has_value()`.

*Throws:* Any exception thrown by the initialization of *val* or *unex*.

*Remarks:* This constructor is defined as deleted unless

- `is_copy_constructible_v<T>` is `true` and
- `is_copy_constructible_v<E>` is `true`.

This constructor is trivial if

- `is_trivially_copy_constructible_v<T>` is `true` and
- `is_trivially_copy_constructible_v<E>` is `true`.

``` cpp
constexpr expected(expected&& rhs) noexcept(see below);
```

*Constraints:*

- `is_move_constructible_v<T>` is `true` and
- `is_move_constructible_v<E>` is `true`.

*Effects:* If `rhs.has_value()` is `true`, direct-non-list-initializes
*val* with `std::move(*rhs)`. Otherwise, direct-non-list-initializes
*unex* with `std::move(rhs.error())`.

*Ensures:* `rhs.has_value()` is unchanged;
`rhs.has_value() == this->has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *val* or *unex*.

*Remarks:* The exception specification is equivalent to
`is_nothrow_move_constructible_v<T> && is_nothrow_move_constructible_v<E>`.

This constructor is trivial if

- `is_trivially_move_constructible_v<T>` is `true` and
- `is_trivially_move_constructible_v<E>` is `true`.

``` cpp
template<class U, class G>
  constexpr explicit(see below) expected(const expected<U, G>& rhs);
template<class U, class G>
  constexpr explicit(see below) expected(expected<U, G>&& rhs);
```

Let:

- `UF` be `const U&` for the first overload and `U` for the second
  overload.
- `GF` be `const G&` for the first overload and `G` for the second
  overload.

*Constraints:*

- `is_constructible_v<T, UF>` is `true`; and
- `is_constructible_v<E, GF>` is `true`; and
- if `T` is not cv `bool`,
  *`converts-from-any-cvref`*`<T, expected<U, G>>` is `false`; and
- `is_constructible_v<unexpected<E>, expected<U, G>&>` is `false`; and
- `is_constructible_v<unexpected<E>, expected<U, G>>` is `false`; and
- `is_constructible_v<unexpected<E>, const expected<U, G>&>` is `false`;
  and
- `is_constructible_v<unexpected<E>, const expected<U, G>>` is `false`.

*Effects:* If `rhs.has_value()`, direct-non-list-initializes *val* with
`std::forward<UF>(*rhs)`. Otherwise, direct-non-list-initializes *unex*
with `std::forward<GF>(rhs.error())`.

*Ensures:* `rhs.has_value()` is unchanged;
`rhs.has_value() == this->has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *val* or *unex*.

*Remarks:* The expression inside `explicit` is equivalent to
`!is_convertible_v<UF, T> || !is_convertible_v<GF, E>`.

``` cpp
template<class U = remove_cv_t<T>>
  constexpr explicit(!is_convertible_v<U, T>) expected(U&& v);
```

*Constraints:*

- `is_same_v<remove_cvref_t<U>, in_place_t>` is `false`; and
- `is_same_v<remove_cvref_t<U>, expected>` is `false`; and
- `is_same_v<remove_cvref_t<U>, unexpect_t>` is `false`; and
- `remove_cvref_t<U>` is not a specialization of `unexpected`; and
- `is_constructible_v<T, U>` is `true`; and
- if `T` is cv `bool`, `remove_cvref_t<U>` is not a specialization of
  `expected`.

*Effects:* Direct-non-list-initializes *val* with `std::forward<U>(v)`.

*Ensures:* `has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *val*.

``` cpp
template<class G>
  constexpr explicit(!is_convertible_v<const G&, E>) expected(const unexpected<G>& e);
template<class G>
  constexpr explicit(!is_convertible_v<G, E>) expected(unexpected<G>&& e);
```

Let `GF` be `const G&` for the first overload and `G` for the second
overload.

*Constraints:* `is_constructible_v<E, GF>` is `true`.

*Effects:* Direct-non-list-initializes *unex* with
`std::forward<GF>(e.error())`.

*Ensures:* `has_value()` is `false`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
template<class... Args>
  constexpr explicit expected(in_place_t, Args&&... args);
```

*Constraints:* `is_constructible_v<T, Args...>` is `true`.

*Effects:* Direct-non-list-initializes *val* with
`std::forward<Args>(args)...`.

*Ensures:* `has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *val*.

``` cpp
template<class U, class... Args>
  constexpr explicit expected(in_place_t, initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<T, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Direct-non-list-initializes *val* with
`il, std::forward<Args>(args)...`.

*Ensures:* `has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *val*.

``` cpp
template<class... Args>
  constexpr explicit expected(unexpect_t, Args&&... args);
```

*Constraints:* `is_constructible_v<E, Args...>` is `true`.

*Effects:* Direct-non-list-initializes *unex* with
`std::forward<Args>(args)...`.

*Ensures:* `has_value()` is `false`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
template<class U, class... Args>
  constexpr explicit expected(unexpect_t, initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<E, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Direct-non-list-initializes *unex* with
`il, std::forward<Args>(args)...`.

*Ensures:* `has_value()` is `false`.

*Throws:* Any exception thrown by the initialization of *unex*.

#### Destructor <a id="expected.object.dtor">[[expected.object.dtor]]</a>

``` cpp
constexpr ~expected();
```

*Effects:* If `has_value()` is `true`, destroys *val*, otherwise
destroys *unex*.

*Remarks:* If `is_trivially_destructible_v<T>` is `true`, and
`is_trivially_destructible_v<E>` is `true`, then this destructor is a
trivial destructor.

#### Assignment <a id="expected.object.assign">[[expected.object.assign]]</a>

This subclause makes use of the following exposition-only function
template:

``` cpp
template<class T, class U, class... Args>
constexpr void reinit-expected(T& newval, U& oldval, Args&&... args) {  // exposition only
  if constexpr (is_nothrow_constructible_v<T, Args...>) {
    destroy_at(addressof(oldval));
    construct_at(addressof(newval), std::forward<Args>(args)...);
  } else if constexpr (is_nothrow_move_constructible_v<T>) {
    T tmp(std::forward<Args>(args)...);
    destroy_at(addressof(oldval));
    construct_at(addressof(newval), std::move(tmp));
  } else {
    U tmp(std::move(oldval));
    destroy_at(addressof(oldval));
    try {
      construct_at(addressof(newval), std::forward<Args>(args)...);
    } catch (...) {
      construct_at(addressof(oldval), std::move(tmp));
      throw;
    }
  }
}
```

``` cpp
constexpr expected& operator=(const expected& rhs);
```

*Effects:*

- If `this->has_value() && rhs.has_value()` is `true`, equivalent to
  *`val`*` = *rhs`.
- Otherwise, if `this->has_value()` is `true`, equivalent to:
  ``` cpp
  reinit-expected(unex, val, rhs.error())
  ```
- Otherwise, if `rhs.has_value()` is `true`, equivalent to:
  ``` cpp
  reinit-expected(val, unex, *rhs)
  ```
- Otherwise, equivalent to *`unex`*` = rhs.error()`.

Then, if no exception was thrown, equivalent to:
*`has_val`*` = rhs.has_value(); return *this;`

*Returns:* `*this`.

*Remarks:* This operator is defined as deleted unless:

- `is_copy_assignable_v<T>` is `true` and
- `is_copy_constructible_v<T>` is `true` and
- `is_copy_assignable_v<E>` is `true` and
- `is_copy_constructible_v<E>` is `true` and
- `is_nothrow_move_constructible_v<T> || is_nothrow_move_constructible_v<E>`
  is `true`.

``` cpp
constexpr expected& operator=(expected&& rhs) noexcept(see below);
```

*Constraints:*

- `is_move_constructible_v<T>` is `true` and
- `is_move_assignable_v<T>` is `true` and
- `is_move_constructible_v<E>` is `true` and
- `is_move_assignable_v<E>` is `true` and
- `is_nothrow_move_constructible_v<T> || is_nothrow_move_constructible_v<E>`
  is `true`.

*Effects:*

- If `this->has_value() && rhs.has_value()` is `true`, equivalent to
  *`val`*` = std::move(*rhs)`.
- Otherwise, if `this->has_value()` is `true`, equivalent to:
  ``` cpp
  reinit-expected(unex, val, std::move(rhs.error()))
  ```
- Otherwise, if `rhs.has_value()` is `true`, equivalent to:
  ``` cpp
  reinit-expected(val, unex, std::move(*rhs))
  ```
- Otherwise, equivalent to *`unex`*` = std::move(rhs.error())`.

Then, if no exception was thrown, equivalent to:
`has_val = rhs.has_value(); return *this;`

*Returns:* `*this`.

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_move_assignable_v<T> && is_nothrow_move_constructible_v<T> &&
is_nothrow_move_assignable_v<E> && is_nothrow_move_constructible_v<E>
```

``` cpp
template<class U = remove_cv_t<T>>
  constexpr expected& operator=(U&& v);
```

*Constraints:*

- `is_same_v<expected, remove_cvref_t<U>>` is `false`; and
- `remove_cvref_t<U>` is not a specialization of `unexpected`; and
- `is_constructible_v<T, U>` is `true`; and
- `is_assignable_v<T&, U>` is `true`; and
- `is_nothrow_constructible_v<T, U> || is_nothrow_move_constructible_v<T> ||`` is_nothrow_move_constructible_v<E>`
  is `true`.

*Effects:*

- If `has_value()` is `true`, equivalent to:
  *`val`*` = std::forward<U>(v);`
- Otherwise, equivalent to:
  ``` cpp
  reinit-expected(val, unex, std::forward<U>(v));
  has_val = true;
  ```

*Returns:* `*this`.

``` cpp
template<class G>
  constexpr expected& operator=(const unexpected<G>& e);
template<class G>
  constexpr expected& operator=(unexpected<G>&& e);
```

Let `GF` be `const G&` for the first overload and `G` for the second
overload.

*Constraints:*

- `is_constructible_v<E, GF>` is `true`; and
- `is_assignable_v<E&, GF>` is `true`; and
- `is_nothrow_constructible_v<E, GF> || is_nothrow_move_constructible_v<T> ||`` is_nothrow_move_constructible_v<E>`
  is `true`.

*Effects:*

- If `has_value()` is `true`, equivalent to:
  ``` cpp
  reinit-expected(unex, val, std::forward<GF>(e.error()));
  has_val = false;
  ```
- Otherwise, equivalent to: *`unex`*` = std::forward<GF>(e.error());`

*Returns:* `*this`.

``` cpp
template<class... Args>
  constexpr T& emplace(Args&&... args) noexcept;
```

*Constraints:* `is_nothrow_constructible_v<T, Args...>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value()) {
  destroy_at(addressof(val));
} else {
  destroy_at(addressof(unex));
  has_val = true;
}
return *construct_at(addressof(val), std::forward<Args>(args)...);
```

``` cpp
template<class U, class... Args>
  constexpr T& emplace(initializer_list<U> il, Args&&... args) noexcept;
```

*Constraints:*
`is_nothrow_constructible_v<T, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Equivalent to:

``` cpp
if (has_value()) {
  destroy_at(addressof(val));
} else {
  destroy_at(addressof(unex));
  has_val = true;
}
return *construct_at(addressof(val), il, std::forward<Args>(args)...);
```

#### Swap <a id="expected.object.swap">[[expected.object.swap]]</a>

``` cpp
constexpr void swap(expected& rhs) noexcept(see below);
```

*Constraints:*

- `is_swappable_v<T>` is `true` and
- `is_swappable_v<E>` is `true` and
- `is_move_constructible_v<T> && is_move_constructible_v<E>` is `true`,
  and
- `is_nothrow_move_constructible_v<T> || is_nothrow_move_constructible_v<E>`
  is `true`.

*Effects:* See [[expected.object.swap]].

**Table: `swap(expected&)` effects**

| `this->has_value()` | `!this->has_value()` |
| ------------------- | -------------------- |


For the case where `rhs.has_value()` is `false` and `this->has_value()`
is `true`, equivalent to:

``` cpp
if constexpr (is_nothrow_move_constructible_v<E>) {
  E tmp(std::move(rhs.unex));
  destroy_at(addressof(rhs.unex));
  try {
    construct_at(addressof(rhs.val), std::move(val));
    destroy_at(addressof(val));
    construct_at(addressof(unex), std::move(tmp));
  } catch(...) {
    construct_at(addressof(rhs.unex), std::move(tmp));
    throw;
  }
} else {
  T tmp(std::move(val));
  destroy_at(addressof(val));
  try {
    construct_at(addressof(unex), std::move(rhs.unex));
    destroy_at(addressof(rhs.unex));
    construct_at(addressof(rhs.val), std::move(tmp));
  } catch (...) {
    construct_at(addressof(val), std::move(tmp));
    throw;
  }
}
has_val = false;
rhs.has_val = true;
```

*Throws:* Any exception thrown by the expressions in the *Effects*.

*Remarks:* The exception specification is equivalent to:

``` cpp
is_nothrow_move_constructible_v<T> && is_nothrow_swappable_v<T> &&
is_nothrow_move_constructible_v<E> && is_nothrow_swappable_v<E>
```

``` cpp
friend constexpr void swap(expected& x, expected& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* Equivalent to `x.swap(y)`.

#### Observers <a id="expected.object.obs">[[expected.object.obs]]</a>

``` cpp
constexpr const T* operator->() const noexcept;
constexpr T* operator->() noexcept;
```

`has_value()` is `true`.

*Returns:* `addressof(`*`val`*`)`.

``` cpp
constexpr const T& operator*() const & noexcept;
constexpr T& operator*() & noexcept;
```

`has_value()` is `true`.

*Returns:* *val*.

``` cpp
constexpr T&& operator*() && noexcept;
constexpr const T&& operator*() const && noexcept;
```

`has_value()` is `true`.

*Returns:* `std::move(`*`val`*`)`.

``` cpp
constexpr explicit operator bool() const noexcept;
constexpr bool has_value() const noexcept;
```

*Returns:* *has_val*.

``` cpp
constexpr const T& value() const &;
constexpr T& value() &;
```

*Mandates:* `is_copy_constructible_v<E>` is `true`.

*Returns:* *val*, if `has_value()` is `true`.

*Throws:* `bad_expected_access(as_const(error()))` if `has_value()` is
`false`.

``` cpp
constexpr T&& value() &&;
constexpr const T&& value() const &&;
```

*Mandates:* `is_copy_constructible_v<E>` is `true` and
`is_constructible_v<E, decltype(std::move(error()))>` is `true`.

*Returns:* `std::move(`*`val`*`)`, if `has_value()` is `true`.

*Throws:* `bad_expected_access(std::move(error()))` if `has_value()` is
`false`.

``` cpp
constexpr const E& error() const & noexcept;
constexpr E& error() & noexcept;
```

`has_value()` is `false`.

*Returns:* *unex*.

``` cpp
constexpr E&& error() && noexcept;
constexpr const E&& error() const && noexcept;
```

`has_value()` is `false`.

*Returns:* `std::move(`*`unex`*`)`.

``` cpp
template<class U = remove_cv_t<T>> constexpr T value_or(U&& v) const &;
```

*Mandates:* `is_copy_constructible_v<T>` is `true` and
`is_convertible_v<U, T>` is `true`.

*Returns:* `has_value() ? **this : static_cast<T>(std::forward<U>(v))`.

``` cpp
template<class U = remove_cv_t<T>> constexpr T value_or(U&& v) &&;
```

*Mandates:* `is_move_constructible_v<T>` is `true` and
`is_convertible_v<U, T>` is `true`.

*Returns:*
`has_value() ? std::move(**this) : static_cast<T>(std::forward<U>(v))`.

``` cpp
template<class G = E> constexpr E error_or(G&& e) const &;
```

*Mandates:* `is_copy_constructible_v<E>` is `true` and
`is_convertible_v<G, E>` is `true`.

*Returns:* `std::forward<G>(e)` if `has_value()` is `true`, `error()`
otherwise.

``` cpp
template<class G = E> constexpr E error_or(G&& e) &&;
```

*Mandates:* `is_move_constructible_v<E>` is `true` and
`is_convertible_v<G, E>` is `true`.

*Returns:* `std::forward<G>(e)` if `has_value()` is `true`,
`std::move(error())` otherwise.

#### Monadic operations <a id="expected.object.monadic">[[expected.object.monadic]]</a>

``` cpp
template<class F> constexpr auto and_then(F&& f) &;
template<class F> constexpr auto and_then(F&& f) const &;
```

Let `U` be `remove_cvref_t<invoke_result_t<F, decltype((`*`val`*`))>>`.

*Constraints:* `is_constructible_v<E, decltype(error())>` is `true`.

*Mandates:* `U` is a specialization of `expected` and
`is_same_v<typename U::error_type, E>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return invoke(std::forward<F>(f), val);
else
  return U(unexpect, error());
```

``` cpp
template<class F> constexpr auto and_then(F&& f) &&;
template<class F> constexpr auto and_then(F&& f) const &&;
```

Let `U` be
`remove_cvref_t<invoke_result_t<F, decltype(std::move(`*`val`*`))>>`.

*Constraints:* `is_constructible_v<E, decltype(std::move(error()))>` is
`true`.

*Mandates:* `U` is a specialization of `expected` and
`is_same_v<typename U::error_type, E>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return invoke(std::forward<F>(f), std::move(val));
else
  return U(unexpect, std::move(error()));
```

``` cpp
template<class F> constexpr auto or_else(F&& f) &;
template<class F> constexpr auto or_else(F&& f) const &;
```

Let `G` be `remove_cvref_t<invoke_result_t<F, decltype(error())>>`.

*Constraints:* `is_constructible_v<T, decltype((`*`val`*`))>` is `true`.

*Mandates:* `G` is a specialization of `expected` and
`is_same_v<typename G::value_type, T>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return G(in_place, val);
else
  return invoke(std::forward<F>(f), error());
```

``` cpp
template<class F> constexpr auto or_else(F&& f) &&;
template<class F> constexpr auto or_else(F&& f) const &&;
```

Let `G` be
`remove_cvref_t<invoke_result_t<F, decltype(std::move(error()))>>`.

*Constraints:* `is_constructible_v<T, decltype(std::move(`*`val`*`))>`
is `true`.

*Mandates:* `G` is a specialization of `expected` and
`is_same_v<typename G::value_type, T>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return G(in_place, std::move(val));
else
  return invoke(std::forward<F>(f), std::move(error()));
```

``` cpp
template<class F> constexpr auto transform(F&& f) &;
template<class F> constexpr auto transform(F&& f) const &;
```

Let `U` be `remove_cv_t<invoke_result_t<F, decltype((`*`val`*`))>>`.

*Constraints:* `is_constructible_v<E, decltype(error())>` is `true`.

*Mandates:* `U` is a valid value type for `expected`. If `is_void_v<U>`
is `false`, the declaration

``` cpp
U u(invoke(std::forward<F>(f), val));
```

is well-formed.

*Effects:*

- If `has_value()` is `false`, returns
  `expected<U, E>(unexpect, error())`.
- Otherwise, if `is_void_v<U>` is `false`, returns an `expected<U, E>`
  object whose *has_val* member is `true` and *val* member is
  direct-non-list-initialized with
  `invoke(std::forward<F>(f), `*`val`*`)`.
- Otherwise, evaluates `invoke(std::forward<F>(f), `*`val`*`)` and then
  returns `expected<U, E>()`.

``` cpp
template<class F> constexpr auto transform(F&& f) &&;
template<class F> constexpr auto transform(F&& f) const &&;
```

Let `U` be
`remove_cv_t<invoke_result_t<F, decltype(std::move(`*`val`*`))>>`.

*Constraints:* `is_constructible_v<E, decltype(std::move(error()))>` is
`true`.

*Mandates:* `U` is a valid value type for `expected`. If `is_void_v<U>`
is `false`, the declaration

``` cpp
U u(invoke(std::forward<F>(f), std::move(val)));
```

is well-formed.

*Effects:*

- If `has_value()` is `false`, returns
  `expected<U, E>(unexpect, std::move(error()))`.
- Otherwise, if `is_void_v<U>` is `false`, returns an `expected<U, E>`
  object whose *has_val* member is `true` and *val* member is
  direct-non-list-initialized with
  `invoke(std::forward<F>(f), std::move(`*`val`*`))`.
- Otherwise, evaluates
  `invoke(std::forward<F>(f), std::move(`*`val`*`))` and then returns
  `expected<U, E>()`.

``` cpp
template<class F> constexpr auto transform_error(F&& f) &;
template<class F> constexpr auto transform_error(F&& f) const &;
```

Let `G` be `remove_cv_t<invoke_result_t<F, decltype(error())>>`.

*Constraints:* `is_constructible_v<T, decltype((`*`val`*`))>` is `true`.

*Mandates:* `G` is a valid template argument for
`unexpected`[[expected.un.general]] and the declaration

``` cpp
G g(invoke(std::forward<F>(f), error()));
```

is well-formed.

*Returns:* If `has_value()` is `true`,
`expected<T, G>(in_place, `*`val`*`)`; otherwise, an `expected<T, G>`
object whose *has_val* member is `false` and *unex* member is
direct-non-list-initialized with `invoke(std::forward<F>(f), error())`.

``` cpp
template<class F> constexpr auto transform_error(F&& f) &&;
template<class F> constexpr auto transform_error(F&& f) const &&;
```

Let `G` be
`remove_cv_t<invoke_result_t<F, decltype(std::move(error()))>>`.

*Constraints:* `is_constructible_v<T, decltype(std::move(`*`val`*`))>`
is `true`.

*Mandates:* `G` is a valid template argument for
`unexpected`[[expected.un.general]] and the declaration

``` cpp
G g(invoke(std::forward<F>(f), std::move(error())));
```

is well-formed.

*Returns:* If `has_value()` is `true`,
`expected<T, G>(in_place, std::move(`*`val`*`))`; otherwise, an
`expected<T, G>` object whose *has_val* member is `false` and *unex*
member is direct-non-list-initialized with
`invoke(std::forward<F>(f), std::move(error()))`.

#### Equality operators <a id="expected.object.eq">[[expected.object.eq]]</a>

``` cpp
template<class T2, class E2> requires (!is_void_v<T2>)
  friend constexpr bool operator==(const expected& x, const expected<T2, E2>& y);
```

*Constraints:* The expressions `*x == *y` and `x.error() == y.error()`
are well-formed and their results are convertible to `bool`.

*Returns:* If `x.has_value()` does not equal `y.has_value()`, `false`;
otherwise if `x.has_value()` is `true`, `*x == *y`; otherwise
`x.error() == y.error()`.

``` cpp
template<class T2> friend constexpr bool operator==(const expected& x, const T2& v);
```

*Constraints:* `T2` is not a specialization of `expected`. The
expression `*x == v` is well-formed and its result is convertible to
`bool`.

[*Note 1*: `T` need not be *Cpp17EqualityComparable*. — *end note*]

*Returns:* `x.has_value() && static_cast<bool>(*x == v)`.

``` cpp
template<class E2> friend constexpr bool operator==(const expected& x, const unexpected<E2>& e);
```

*Constraints:* The expression `x.error() == e.error()` is well-formed
and its result is convertible to `bool`.

*Returns:*
`!x.has_value() && static_cast<bool>(x.error() == e.error())`.

### Partial specialization of `expected` for `void` types <a id="expected.void">[[expected.void]]</a>

#### General <a id="expected.void.general">[[expected.void.general]]</a>

``` cpp
template<class T, class E> requires is_void_v<T>
class expected<T, E> {
public:
  using value_type = T;
  using error_type = E;
  using unexpected_type = unexpected<E>;

  template<class U>
  using rebind = expected<U, error_type>;

  // [expected.void.cons], constructors
  constexpr expected() noexcept;
  constexpr expected(const expected&);
  constexpr expected(expected&&) noexcept(see below);
  template<class U, class G>
    constexpr explicit(see below) expected(const expected<U, G>&);
  template<class U, class G>
    constexpr explicit(see below) expected(expected<U, G>&&);

  template<class G>
    constexpr explicit(see below) expected(const unexpected<G>&);
  template<class G>
    constexpr explicit(see below) expected(unexpected<G>&&);

  constexpr explicit expected(in_place_t) noexcept;
  template<class... Args>
    constexpr explicit expected(unexpect_t, Args&&...);
  template<class U, class... Args>
    constexpr explicit expected(unexpect_t, initializer_list<U>, Args&&...);


  // [expected.void.dtor], destructor
  constexpr ~expected();

  // [expected.void.assign], assignment
  constexpr expected& operator=(const expected&);
  constexpr expected& operator=(expected&&) noexcept(see below);
  template<class G>
    constexpr expected& operator=(const unexpected<G>&);
  template<class G>
    constexpr expected& operator=(unexpected<G>&&);
  constexpr void emplace() noexcept;

  // [expected.void.swap], swap
  constexpr void swap(expected&) noexcept(see below);
  friend constexpr void swap(expected& x, expected& y) noexcept(noexcept(x.swap(y)));

  // [expected.void.obs], observers
  constexpr explicit operator bool() const noexcept;
  constexpr bool has_value() const noexcept;
  constexpr void operator*() const noexcept;
  constexpr void value() const &;                                           // freestanding-deleted
  constexpr void value() &&;                                                // freestanding-deleted
  constexpr const E& error() const & noexcept;
  constexpr E& error() & noexcept;
  constexpr const E&& error() const && noexcept;
  constexpr E&& error() && noexcept;
  template<class G = E> constexpr E error_or(G&&) const &;
  template<class G = E> constexpr E error_or(G&&) &&;

  // [expected.void.monadic], monadic operations
  template<class F> constexpr auto and_then(F&& f) &;
  template<class F> constexpr auto and_then(F&& f) &&;
  template<class F> constexpr auto and_then(F&& f) const &;
  template<class F> constexpr auto and_then(F&& f) const &&;
  template<class F> constexpr auto or_else(F&& f) &;
  template<class F> constexpr auto or_else(F&& f) &&;
  template<class F> constexpr auto or_else(F&& f) const &;
  template<class F> constexpr auto or_else(F&& f) const &&;
  template<class F> constexpr auto transform(F&& f) &;
  template<class F> constexpr auto transform(F&& f) &&;
  template<class F> constexpr auto transform(F&& f) const &;
  template<class F> constexpr auto transform(F&& f) const &&;
  template<class F> constexpr auto transform_error(F&& f) &;
  template<class F> constexpr auto transform_error(F&& f) &&;
  template<class F> constexpr auto transform_error(F&& f) const &;
  template<class F> constexpr auto transform_error(F&& f) const &&;

  // [expected.void.eq], equality operators
  template<class T2, class E2> requires is_void_v<T2>
    friend constexpr bool operator==(const expected& x, const expected<T2, E2>& y);
  template<class E2>
    friend constexpr bool operator==(const expected&, const unexpected<E2>&);

private:
  bool has_val;         // exposition only
  union {
    E unex;             // exposition only
  };
};
```

Any object of type `expected<T, E>` either represents a value of type
`T`, or contains a value of type `E` nested within [[intro.object]] it.
Member *has_val* indicates whether the `expected<T, E>` object
represents a value of type `T`.

A program that instantiates the definition of the template
`expected<T, E>` with a type for the `E` parameter that is not a valid
template argument for `unexpected` is ill-formed.

`E` shall meet the requirements of *Cpp17Destructible* (
[[cpp17.destructible]]).

#### Constructors <a id="expected.void.cons">[[expected.void.cons]]</a>

``` cpp
constexpr expected() noexcept;
```

*Ensures:* `has_value()` is `true`.

``` cpp
constexpr expected(const expected& rhs);
```

*Effects:* If `rhs.has_value()` is `false`, direct-non-list-initializes
*unex* with `rhs.error()`.

*Ensures:* `rhs.has_value() == this->has_value()`.

*Throws:* Any exception thrown by the initialization of *unex*.

*Remarks:* This constructor is defined as deleted unless
`is_copy_constructible_v<E>` is `true`.

This constructor is trivial if `is_trivially_copy_constructible_v<E>` is
`true`.

``` cpp
constexpr expected(expected&& rhs) noexcept(is_nothrow_move_constructible_v<E>);
```

*Constraints:* `is_move_constructible_v<E>` is `true`.

*Effects:* If `rhs.has_value()` is `false`, direct-non-list-initializes
*unex* with `std::move(rhs.error())`.

*Ensures:* `rhs.has_value()` is unchanged;
`rhs.has_value() == this->has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *unex*.

*Remarks:* This constructor is trivial if
`is_trivially_move_constructible_v<E>` is `true`.

``` cpp
template<class U, class G>
  constexpr explicit(!is_convertible_v<const G&, E>) expected(const expected<U, G>& rhs);
template<class U, class G>
  constexpr explicit(!is_convertible_v<G, E>) expected(expected<U, G>&& rhs);
```

Let `GF` be `const G&` for the first overload and `G` for the second
overload.

*Constraints:*

- `is_void_v<U>` is `true`; and
- `is_constructible_v<E, GF>` is `true`; and
- `is_constructible_v<unexpected<E>, expected<U, G>&>` is `false`; and
- `is_constructible_v<unexpected<E>, expected<U, G>>` is `false`; and
- `is_constructible_v<unexpected<E>, const expected<U, G>&>` is `false`;
  and
- `is_constructible_v<unexpected<E>, const expected<U, G>>` is `false`.

*Effects:* If `rhs.has_value()` is `false`, direct-non-list-initializes
*unex* with `std::forward<GF>(rhs.error())`.

*Ensures:* `rhs.has_value()` is unchanged;
`rhs.has_value() == this->has_value()` is `true`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
template<class G>
  constexpr explicit(!is_convertible_v<const G&, E>) expected(const unexpected<G>& e);
template<class G>
  constexpr explicit(!is_convertible_v<G, E>) expected(unexpected<G>&& e);
```

Let `GF` be `const G&` for the first overload and `G` for the second
overload.

*Constraints:* `is_constructible_v<E, GF>` is `true`.

*Effects:* Direct-non-list-initializes *unex* with
`std::forward<GF>(e.error())`.

*Ensures:* `has_value()` is `false`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
constexpr explicit expected(in_place_t) noexcept;
```

*Ensures:* `has_value()` is `true`.

``` cpp
template<class... Args>
  constexpr explicit expected(unexpect_t, Args&&... args);
```

*Constraints:* `is_constructible_v<E, Args...>` is `true`.

*Effects:* Direct-non-list-initializes *unex* with
`std::forward<Args>(args)...`.

*Ensures:* `has_value()` is `false`.

*Throws:* Any exception thrown by the initialization of *unex*.

``` cpp
template<class U, class... Args>
  constexpr explicit expected(unexpect_t, initializer_list<U> il, Args&&... args);
```

*Constraints:* `is_constructible_v<E, initializer_list<U>&, Args...>` is
`true`.

*Effects:* Direct-non-list-initializes *unex* with
`il, std::forward<Args>(args)...`.

*Ensures:* `has_value()` is `false`.

*Throws:* Any exception thrown by the initialization of *unex*.

#### Destructor <a id="expected.void.dtor">[[expected.void.dtor]]</a>

``` cpp
constexpr ~expected();
```

*Effects:* If `has_value()` is `false`, destroys *unex*.

*Remarks:* If `is_trivially_destructible_v<E>` is `true`, then this
destructor is a trivial destructor.

#### Assignment <a id="expected.void.assign">[[expected.void.assign]]</a>

``` cpp
constexpr expected& operator=(const expected& rhs);
```

*Effects:*

- If `this->has_value() && rhs.has_value()` is `true`, no effects.
- Otherwise, if `this->has_value()` is `true`, equivalent to:
  `construct_at(addressof(`*`unex`*`), rhs.`*`unex`*`); `*`has_val`*` = false;`
- Otherwise, if `rhs.has_value()` is `true`, destroys *unex* and sets
  *has_val* to `true`.
- Otherwise, equivalent to *`unex`*` = rhs.error()`.

*Returns:* `*this`.

*Remarks:* This operator is defined as deleted unless
`is_copy_assignable_v<E>` is `true` and `is_copy_constructible_v<E>` is
`true`.

``` cpp
constexpr expected& operator=(expected&& rhs) noexcept(see below);
```

*Constraints:* `is_move_constructible_v<E>` is `true` and
`is_move_assignable_v<E>` is `true`.

*Effects:*

- If `this->has_value() && rhs.has_value()` is `true`, no effects.
- Otherwise, if `this->has_value()` is `true`, equivalent to:
  ``` cpp
  construct_at(addressof(unex), std::move(rhs.unex));
  has_val = false;
  ```
- Otherwise, if `rhs.has_value()` is `true`, destroys *unex* and sets
  *has_val* to `true`.
- Otherwise, equivalent to *`unex`*` = std::move(rhs.error())`.

*Returns:* `*this`.

*Remarks:* The exception specification is equivalent to
`is_nothrow_move_constructible_v<E> && is_nothrow_move_assignable_v<E>`.

``` cpp
template<class G>
  constexpr expected& operator=(const unexpected<G>& e);
template<class G>
  constexpr expected& operator=(unexpected<G>&& e);
```

Let `GF` be `const G&` for the first overload and `G` for the second
overload.

*Constraints:* `is_constructible_v<E, GF>` is `true` and
`is_assignable_v<E&, GF>` is `true`.

*Effects:*

- If `has_value()` is `true`, equivalent to:
  ``` cpp
  construct_at(addressof(unex), std::forward<GF>(e.error()));
  has_val = false;
  ```
- Otherwise, equivalent to: *`unex`*` = std::forward<GF>(e.error());`

*Returns:* `*this`.

``` cpp
constexpr void emplace() noexcept;
```

*Effects:* If `has_value()` is `false`, destroys *unex* and sets
*has_val* to `true`.

#### Swap <a id="expected.void.swap">[[expected.void.swap]]</a>

``` cpp
constexpr void swap(expected& rhs) noexcept(see below);
```

*Constraints:* `is_swappable_v<E>` is `true` and
`is_move_constructible_v<E>` is `true`.

*Effects:* See [[expected.void.swap]].

**Table: `swap(expected&)` effects**

| `this->has_value()` | `!this->has_value()` |
| ------------------- | -------------------- |


For the case where `rhs.has_value()` is `false` and `this->has_value()`
is `true`, equivalent to:

``` cpp
construct_at(addressof(unex), std::move(rhs.unex));
destroy_at(addressof(rhs.unex));
has_val = false;
rhs.has_val = true;
```

*Throws:* Any exception thrown by the expressions in the *Effects*.

*Remarks:* The exception specification is equivalent to
`is_nothrow_move_constructible_v<E> && is_nothrow_swappable_v<E>`.

``` cpp
friend constexpr void swap(expected& x, expected& y) noexcept(noexcept(x.swap(y)));
```

*Effects:* Equivalent to `x.swap(y)`.

#### Observers <a id="expected.void.obs">[[expected.void.obs]]</a>

``` cpp
constexpr explicit operator bool() const noexcept;
constexpr bool has_value() const noexcept;
```

*Returns:* *has_val*.

``` cpp
constexpr void operator*() const noexcept;
```

`has_value()` is `true`.

``` cpp
constexpr void value() const &;
```

*Mandates:* `is_copy_constructible_v<E>` is `true`.

*Throws:* `bad_expected_access(error())` if `has_value()` is `false`.

``` cpp
constexpr void value() &&;
```

*Mandates:* `is_copy_constructible_v<E>` is `true` and
`is_move_constructible_v<E>` is `true`.

*Throws:* `bad_expected_access(std::move(error()))` if `has_value()` is
`false`.

``` cpp
constexpr const E& error() const & noexcept;
constexpr E& error() & noexcept;
```

`has_value()` is `false`.

*Returns:* *unex*.

``` cpp
constexpr E&& error() && noexcept;
constexpr const E&& error() const && noexcept;
```

`has_value()` is `false`.

*Returns:* `std::move(`*`unex`*`)`.

``` cpp
template<class G = E> constexpr E error_or(G&& e) const &;
```

*Mandates:* `is_copy_constructible_v<E>` is `true` and
`is_convertible_v<G, E>` is `true`.

*Returns:* `std::forward<G>(e)` if `has_value()` is `true`, `error()`
otherwise.

``` cpp
template<class G = E> constexpr E error_or(G&& e) &&;
```

*Mandates:* `is_move_constructible_v<E>` is `true` and
`is_convertible_v<G, E>` is `true`.

*Returns:* `std::forward<G>(e)` if `has_value()` is `true`,
`std::move(error())` otherwise.

#### Monadic operations <a id="expected.void.monadic">[[expected.void.monadic]]</a>

``` cpp
template<class F> constexpr auto and_then(F&& f) &;
template<class F> constexpr auto and_then(F&& f) const &;
```

Let `U` be `remove_cvref_t<invoke_result_t<F>>`.

*Constraints:* `is_constructible_v<E, decltype(error())>>` is `true`.

*Mandates:* `U` is a specialization of `expected` and
`is_same_v<typename U::error_type, E>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return invoke(std::forward<F>(f));
else
  return U(unexpect, error());
```

``` cpp
template<class F> constexpr auto and_then(F&& f) &&;
template<class F> constexpr auto and_then(F&& f) const &&;
```

Let `U` be `remove_cvref_t<invoke_result_t<F>>`.

*Constraints:* `is_constructible_v<E, decltype(std::move(error()))>` is
`true`.

*Mandates:* `U` is a specialization of `expected` and
`is_same_v<typename U::error_type, E>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return invoke(std::forward<F>(f));
else
  return U(unexpect, std::move(error()));
```

``` cpp
template<class F> constexpr auto or_else(F&& f) &;
template<class F> constexpr auto or_else(F&& f) const &;
```

Let `G` be `remove_cvref_t<invoke_result_t<F, decltype(error())>>`.

*Mandates:* `G` is a specialization of `expected` and
`is_same_v<typename G::value_type, T>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return G();
else
  return invoke(std::forward<F>(f), error());
```

``` cpp
template<class F> constexpr auto or_else(F&& f) &&;
template<class F> constexpr auto or_else(F&& f) const &&;
```

Let `G` be
`remove_cvref_t<invoke_result_t<F, decltype(std::move(error()))>>`.

*Mandates:* `G` is a specialization of `expected` and
`is_same_v<typename G::value_type, T>` is `true`.

*Effects:* Equivalent to:

``` cpp
if (has_value())
  return G();
else
  return invoke(std::forward<F>(f), std::move(error()));
```

``` cpp
template<class F> constexpr auto transform(F&& f) &;
template<class F> constexpr auto transform(F&& f) const &;
```

Let `U` be `remove_cv_t<invoke_result_t<F>>`.

*Constraints:* `is_constructible_v<E, decltype(error())>` is `true`.

*Mandates:* `U` is a valid value type for `expected`. If `is_void_v<U>`
is `false`, the declaration

``` cpp
U u(invoke(std::forward<F>(f)));
```

is well-formed.

*Effects:*

- If `has_value()` is `false`, returns
  `expected<U, E>(unexpect, error())`.
- Otherwise, if `is_void_v<U>` is `false`, returns an `expected<U, E>`
  object whose *has_val* member is `true` and *val* member is
  direct-non-list-initialized with `invoke(std::forward<F>(f))`.
- Otherwise, evaluates `invoke(std::forward<F>(f))` and then returns
  `expected<U, E>()`.

``` cpp
template<class F> constexpr auto transform(F&& f) &&;
template<class F> constexpr auto transform(F&& f) const &&;
```

Let `U` be `remove_cv_t<invoke_result_t<F>>`.

*Constraints:* `is_constructible_v<E, decltype(std::move(error()))>` is
`true`.

*Mandates:* `U` is a valid value type for `expected`. If `is_void_v<U>`
is `false`, the declaration

``` cpp
U u(invoke(std::forward<F>(f)));
```

is well-formed.

*Effects:*

- If `has_value()` is `false`, returns
  `expected<U, E>(unexpect, std::move(error()))`.
- Otherwise, if `is_void_v<U>` is `false`, returns an `expected<U, E>`
  object whose *has_val* member is `true` and *val* member is
  direct-non-list-initialized with `invoke(std::forward<F>(f))`.
- Otherwise, evaluates `invoke(std::forward<F>(f))` and then returns
  `expected<U, E>()`.

``` cpp
template<class F> constexpr auto transform_error(F&& f) &;
template<class F> constexpr auto transform_error(F&& f) const &;
```

Let `G` be `remove_cv_t<invoke_result_t<F, decltype(error())>>`.

*Mandates:* `G` is a valid template argument for
`unexpected`[[expected.un.general]] and the declaration

``` cpp
G g(invoke(std::forward<F>(f), error()));
```

is well-formed.

*Returns:* If `has_value()` is `true`, `expected<T, G>()`; otherwise, an
`expected<T, G>` object whose *has_val* member is `false` and *unex*
member is direct-non-list-initialized with
`invoke(std::forward<F>(f), error())`.

``` cpp
template<class F> constexpr auto transform_error(F&& f) &&;
template<class F> constexpr auto transform_error(F&& f) const &&;
```

Let `G` be
`remove_cv_t<invoke_result_t<F, decltype(std::move(error()))>>`.

*Mandates:* `G` is a valid template argument for
`unexpected`[[expected.un.general]] and the declaration

``` cpp
G g(invoke(std::forward<F>(f), std::move(error())));
```

is well-formed.

*Returns:* If `has_value()` is `true`, `expected<T, G>()`; otherwise, an
`expected<T, G>` object whose *has_val* member is `false` and *unex*
member is direct-non-list-initialized with
`invoke(std::forward<F>(f), std::move(error()))`.

#### Equality operators <a id="expected.void.eq">[[expected.void.eq]]</a>

``` cpp
template<class T2, class E2> requires is_void_v<T2>
  friend constexpr bool operator==(const expected& x, const expected<T2, E2>& y);
```

*Constraints:* The expression `x.error() == y.error()` is well-formed
and its result is convertible to `bool`.

*Returns:* If `x.has_value()` does not equal `y.has_value()`, `false`;
otherwise `x.has_value() || static_cast<bool>(x.error() == y.error())`.

``` cpp
template<class E2>
  friend constexpr bool operator==(const expected& x, const unexpected<E2>& e);
```

*Constraints:* The expression `x.error() == e.error()` is well-formed
and its result is convertible to `bool`.

*Returns:*
`!x.has_value() && static_cast<bool>(x.error() == e.error())`.

## Bitsets <a id="bitset">[[bitset]]</a>

### Header `<bitset>` synopsis <a id="bitset.syn">[[bitset.syn]]</a>

The header `<bitset>` defines a class template and several related
functions for representing and manipulating fixed-size sequences of
bits.

``` cpp
#include <string>   // see [string.syn]
#include <iosfwd>   // for istream[istream.syn], ostream[ostream.syn], see [iosfwd.syn]

namespace std {
  template<size_t N> class bitset;

  // [bitset.operators], bitset operators
  template<size_t N>
    constexpr bitset<N> operator&(const bitset<N>&, const bitset<N>&) noexcept;
  template<size_t N>
    constexpr bitset<N> operator|(const bitset<N>&, const bitset<N>&) noexcept;
  template<size_t N>
    constexpr bitset<N> operator^(const bitset<N>&, const bitset<N>&) noexcept;
  template<class charT, class traits, size_t N>
    basic_istream<charT, traits>&
      operator>>(basic_istream<charT, traits>& is, bitset<N>& x);
  template<class charT, class traits, size_t N>
    basic_ostream<charT, traits>&
      operator<<(basic_ostream<charT, traits>& os, const bitset<N>& x);
}
```

### Class template `bitset` <a id="template.bitset">[[template.bitset]]</a>

#### General <a id="template.bitset.general">[[template.bitset.general]]</a>

``` cpp
namespace std {
  template<size_t N> class bitset {
  public:
    // bit reference
    class reference {
    public:
      constexpr reference(const reference&) = default;
      constexpr ~reference();
      constexpr reference& operator=(bool x) noexcept;              // for b[i] = x;
      constexpr reference& operator=(const reference&) noexcept;    // for b[i] = b[j];
      constexpr bool operator~() const noexcept;                    // flips the bit
      constexpr operator bool() const noexcept;                     // for x = b[i];
      constexpr reference& flip() noexcept;                         // for b[i].flip();
    };

    // [bitset.cons], constructors
    constexpr bitset() noexcept;
    constexpr bitset(unsigned long long val) noexcept;
    template<class charT, class traits, class Allocator>
      constexpr explicit bitset(
        const basic_string<charT, traits, Allocator>& str,
        typename basic_string<charT, traits, Allocator>::size_type pos = 0,
        typename basic_string<charT, traits, Allocator>::size_type n
          = basic_string<charT, traits, Allocator>::npos,
        charT zero = charT('0'),
        charT one = charT('1'));
    template<class charT, class traits>
      constexpr explicit bitset(
        basic_string_view<charT, traits> str,
        typename basic_string_view<charT, traits>::size_type pos = 0,
        typename basic_string_view<charT, traits>::size_type n
          = basic_string_view<charT, traits>::npos,
        charT zero = charT('0'),
        charT one = charT('1'));
    template<class charT>
      constexpr explicit bitset(
        const charT* str,
        typename basic_string_view<charT>::size_type n = basic_string_view<charT>::npos,
        charT zero = charT('0'),
        charT one = charT('1'));

    // [bitset.members], bitset operations
    constexpr bitset& operator&=(const bitset& rhs) noexcept;
    constexpr bitset& operator|=(const bitset& rhs) noexcept;
    constexpr bitset& operator^=(const bitset& rhs) noexcept;
    constexpr bitset& operator<<=(size_t pos) noexcept;
    constexpr bitset& operator>>=(size_t pos) noexcept;
    constexpr bitset  operator<<(size_t pos) const noexcept;
    constexpr bitset  operator>>(size_t pos) const noexcept;
    constexpr bitset& set() noexcept;
    constexpr bitset& set(size_t pos, bool val = true);
    constexpr bitset& reset() noexcept;
    constexpr bitset& reset(size_t pos);
    constexpr bitset  operator~() const noexcept;
    constexpr bitset& flip() noexcept;
    constexpr bitset& flip(size_t pos);

    // element access
    constexpr bool operator[](size_t pos) const;
    constexpr reference operator[](size_t pos);

    constexpr unsigned long to_ulong() const;
    constexpr unsigned long long to_ullong() const;
    template<class charT = char,
             class traits = char_traits<charT>,
             class Allocator = allocator<charT>>
      constexpr basic_string<charT, traits, Allocator>
        to_string(charT zero = charT('0'), charT one = charT('1')) const;

    // observers
    constexpr size_t count() const noexcept;
    constexpr size_t size() const noexcept;
    constexpr bool operator==(const bitset& rhs) const noexcept;
    constexpr bool test(size_t pos) const;
    constexpr bool all() const noexcept;
    constexpr bool any() const noexcept;
    constexpr bool none() const noexcept;
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

The functions described in [[template.bitset]] can report three kinds of
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
the value representation [[term.object.representation]] of
`unsigned long long`. If `M < N`, the remaining bit positions are
initialized to zero.

``` cpp
template<class charT, class traits, class Allocator>
  constexpr explicit bitset(
    const basic_string<charT, traits, Allocator>& str,
    typename basic_string<charT, traits, Allocator>::size_type pos = 0,
    typename basic_string<charT, traits, Allocator>::size_type n
      = basic_string<charT, traits, Allocator>::npos,
    charT zero = charT('0'),
    charT one = charT('1'));
template<class charT, class traits>
  constexpr explicit bitset(
    basic_string_view<charT, traits> str,
    typename basic_string_view<charT, traits>::size_type pos = 0,
    typename basic_string_view<charT, traits>::size_type n
      = basic_string_view<charT, traits>::npos,
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
  constexpr explicit bitset(
    const charT* str,
    typename basic_string_view<charT>::size_type n = basic_string_view<charT>::npos,
    charT zero = charT('0'),
    charT one = charT('1'));
```

*Effects:* As if by:

``` cpp
bitset(n == basic_string_view<charT>::npos
          ? basic_string_view<charT>(str)
          : basic_string_view<charT>(str, n),
       0, n, zero, one)
```

#### Members <a id="bitset.members">[[bitset.members]]</a>

``` cpp
constexpr bitset& operator&=(const bitset& rhs) noexcept;
```

*Effects:* Clears each bit in `*this` for which the corresponding bit in
`rhs` is clear, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
constexpr bitset& operator|=(const bitset& rhs) noexcept;
```

*Effects:* Sets each bit in `*this` for which the corresponding bit in
`rhs` is set, and leaves all other bits unchanged.

*Returns:* `*this`.

\indexlibrarymember{operator^=}{bitset}

``` cpp
constexpr bitset& operator^=(const bitset& rhs) noexcept;
```

*Effects:* Toggles each bit in `*this` for which the corresponding bit
in `rhs` is set, and leaves all other bits unchanged.

*Returns:* `*this`.

``` cpp
constexpr bitset& operator<<=(size_t pos) noexcept;
```

*Effects:* Replaces each bit at position `I` in `*this` with a value
determined as follows:

- If `I < pos`, the new value is zero;
- If `I >= pos`, the new value is the previous value of the bit at
  position `I - pos`.

*Returns:* `*this`.

``` cpp
constexpr bitset& operator>>=(size_t pos) noexcept;
```

*Effects:* Replaces each bit at position `I` in `*this` with a value
determined as follows:

- If `pos >= N - I`, the new value is zero;
- If `pos < N - I`, the new value is the previous value of the bit at
  position `I + pos`.

*Returns:* `*this`.

``` cpp
constexpr bitset operator<<(size_t pos) const noexcept;
```

*Returns:* `bitset(*this) <<= pos`.

``` cpp
constexpr bitset operator>>(size_t pos) const noexcept;
```

*Returns:* `bitset(*this) >>= pos`.

``` cpp
constexpr bitset& set() noexcept;
```

*Effects:* Sets all bits in `*this`.

*Returns:* `*this`.

``` cpp
constexpr bitset& set(size_t pos, bool val = true);
```

*Effects:* Stores a new value in the bit at position `pos` in `*this`.
If `val` is `true`, the stored value is one, otherwise it is zero.

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

``` cpp
constexpr bitset& reset() noexcept;
```

*Effects:* Resets all bits in `*this`.

*Returns:* `*this`.

``` cpp
constexpr bitset& reset(size_t pos);
```

*Effects:* Resets the bit at position `pos` in `*this`.

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

\indexlibrarymember{operator~}{bitset}

``` cpp
constexpr bitset operator~() const noexcept;
```

*Effects:* Constructs an object `x` of class `bitset` and initializes it
with `*this`.

*Returns:* `x.flip()`.

``` cpp
constexpr bitset& flip() noexcept;
```

*Effects:* Toggles all bits in `*this`.

*Returns:* `*this`.

``` cpp
constexpr bitset& flip(size_t pos);
```

*Effects:* Toggles the bit at position `pos` in `*this`.

*Returns:* `*this`.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

``` cpp
constexpr bool operator[](size_t pos) const;
```

`pos < size()` is `true`.

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one, otherwise `false`.

*Throws:* Nothing.

``` cpp
constexpr bitset::reference operator[](size_t pos);
```

`pos < size()` is `true`.

*Returns:* An object of type `bitset::reference` such that
`(*this)[pos] == this->test(pos)`, and such that `(*this)[pos] = val` is
equivalent to `this->set(pos, val)`.

*Throws:* Nothing.

*Remarks:* For the purpose of determining the presence of a data
race [[intro.multithread]], any access or update through the resulting
reference potentially accesses or modifies, respectively, the entire
underlying bitset.

``` cpp
constexpr unsigned long to_ulong() const;
```

*Returns:* `x`.

*Throws:* `overflow_error` if the integral value `x` corresponding to
the bits in `*this` cannot be represented as type `unsigned long`.

``` cpp
constexpr unsigned long long to_ullong() const;
```

*Returns:* `x`.

*Throws:* `overflow_error` if the integral value `x` corresponding to
the bits in `*this` cannot be represented as type `unsigned long long`.

``` cpp
template<class charT = char,
         class traits = char_traits<charT>,
         class Allocator = allocator<charT>>
  constexpr basic_string<charT, traits, Allocator>
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
constexpr size_t count() const noexcept;
```

*Returns:* A count of the number of bits set in `*this`.

``` cpp
constexpr size_t size() const noexcept;
```

*Returns:* `N`.

``` cpp
constexpr bool operator==(const bitset& rhs) const noexcept;
```

*Returns:* `true` if the value of each bit in `*this` equals the value
of the corresponding bit in `rhs`.

``` cpp
constexpr bool test(size_t pos) const;
```

*Returns:* `true` if the bit at position `pos` in `*this` has the value
one.

*Throws:* `out_of_range` if `pos` does not correspond to a valid bit
position.

``` cpp
constexpr bool all() const noexcept;
```

*Returns:* `count() == size()`.

``` cpp
constexpr bool any() const noexcept;
```

*Returns:* `count() != 0`.

``` cpp
constexpr bool none() const noexcept;
```

*Returns:* `count() == 0`.

### `bitset` hash support <a id="bitset.hash">[[bitset.hash]]</a>

``` cpp
template<size_t N> struct hash<bitset<N>>;
```

The specialization is enabled [[unord.hash]].

### `bitset` operators <a id="bitset.operators">[[bitset.operators]]</a>

``` cpp
template<size_t N>
  constexpr bitset<N> operator&(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) &= rhs`.

``` cpp
template<size_t N>
  constexpr bitset<N> operator|(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
```

*Returns:* `bitset<N>(lhs) |= rhs`.

\indexlibrarymember{operator^}{bitset}

``` cpp
template<size_t N>
  constexpr bitset<N> operator^(const bitset<N>& lhs, const bitset<N>& rhs) noexcept;
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

If `N > 0` and no characters are stored in `str`, `ios_base::failbit` is
set in the input function’s local error state before `setstate` is
called.

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

## Function objects <a id="function.objects">[[function.objects]]</a>

### General <a id="function.objects.general">[[function.objects.general]]</a>

A *function object type* is an object type [[term.object.type]] that can
be the type of the *postfix-expression* in a function call
[[expr.call]], [[over.match.call]].[^1]

A *function object* is an object of a function object type. In the
places where one would expect to pass a pointer to a function to an
algorithmic template [[algorithms]], the interface is specified to
accept a function object. This not only makes algorithmic templates work
with pointers to functions, but also enables them to work with arbitrary
function objects.

### Header `<functional>` synopsis <a id="functional.syn">[[functional.syn]]</a>

``` cpp
namespace std {
  // [func.invoke], invoke
  template<class F, class... Args>
    constexpr invoke_result_t<F, Args...> invoke(F&& f, Args&&... args)             // freestanding
      noexcept(is_nothrow_invocable_v<F, Args...>);

  template<class R, class F, class... Args>
    constexpr R invoke_r(F&& f, Args&&... args)                                     // freestanding
      noexcept(is_nothrow_invocable_r_v<R, F, Args...>);

  // [refwrap], reference_wrapper
  template<class T> class reference_wrapper;                                        // freestanding

  template<class T> constexpr reference_wrapper<T> ref(T&) noexcept;                // freestanding
  template<class T> constexpr reference_wrapper<const T> cref(const T&) noexcept;   // freestanding
  template<class T> void ref(const T&&) = delete;                                   // freestanding
  template<class T> void cref(const T&&) = delete;                                  // freestanding

  template<class T>
    constexpr reference_wrapper<T> ref(reference_wrapper<T>) noexcept;              // freestanding
  template<class T>
    constexpr reference_wrapper<const T> cref(reference_wrapper<T>) noexcept;       // freestanding

  // [refwrap.common.ref], common_reference related specializations
  template<class R, class T, template<class> class RQual, template<class> class TQual>
    requires see below
  struct basic_common_reference<R, T, RQual, TQual>;

  template<class T, class R, template<class> class TQual, template<class> class RQual>
    requires see below
  struct basic_common_reference<T, R, TQual, RQual>;

  // [arithmetic.operations], arithmetic operations
  template<class T = void> struct plus;                                             // freestanding
  template<class T = void> struct minus;                                            // freestanding
  template<class T = void> struct multiplies;                                       // freestanding
  template<class T = void> struct divides;                                          // freestanding
  template<class T = void> struct modulus;                                          // freestanding
  template<class T = void> struct negate;                                           // freestanding
  template<> struct plus<void>;                                                     // freestanding
  template<> struct minus<void>;                                                    // freestanding
  template<> struct multiplies<void>;                                               // freestanding
  template<> struct divides<void>;                                                  // freestanding
  template<> struct modulus<void>;                                                  // freestanding
  template<> struct negate<void>;                                                   // freestanding

  // [comparisons], comparisons
  template<class T = void> struct equal_to;                                         // freestanding
  template<class T = void> struct not_equal_to;                                     // freestanding
  template<class T = void> struct greater;                                          // freestanding
  template<class T = void> struct less;                                             // freestanding
  template<class T = void> struct greater_equal;                                    // freestanding
  template<class T = void> struct less_equal;                                       // freestanding
  template<> struct equal_to<void>;                                                 // freestanding
  template<> struct not_equal_to<void>;                                             // freestanding
  template<> struct greater<void>;                                                  // freestanding
  template<> struct less<void>;                                                     // freestanding
  template<> struct greater_equal<void>;                                            // freestanding
  template<> struct less_equal<void>;                                               // freestanding

  // [comparisons.three.way], class compare_three_way
  struct compare_three_way;                                                         // freestanding

  // [logical.operations], logical operations
  template<class T = void> struct logical_and;                                      // freestanding
  template<class T = void> struct logical_or;                                       // freestanding
  template<class T = void> struct logical_not;                                      // freestanding
  template<> struct logical_and<void>;                                              // freestanding
  template<> struct logical_or<void>;                                               // freestanding
  template<> struct logical_not<void>;                                              // freestanding

  // [bitwise.operations], bitwise operations
  template<class T = void> struct bit_and;                                          // freestanding
  template<class T = void> struct bit_or;                                           // freestanding
  template<class T = void> struct bit_xor;                                          // freestanding
  template<class T = void> struct bit_not;                                          // freestanding
  template<> struct bit_and<void>;                                                  // freestanding
  template<> struct bit_or<void>;                                                   // freestanding
  template<> struct bit_xor<void>;                                                  // freestanding
  template<> struct bit_not<void>;                                                  // freestanding

  // [func.identity], identity
  struct identity;                                                                  // freestanding

  // [func.not.fn], function template not_fn
  template<class F> constexpr unspecified not_fn(F&& f);                            // freestanding
  template<auto f> constexpr unspecified not_fn() noexcept;                         // freestanding

  // [func.bind.partial], function templates bind_front and bind_back
  template<class F, class... Args>
    constexpr unspecified bind_front(F&&, Args&&...);                               // freestanding
  template<auto f, class... Args>
    constexpr unspecified bind_front(Args&&...);                                    // freestanding
  template<class F, class... Args>
    constexpr unspecified bind_back(F&&, Args&&...);                                // freestanding
  template<auto f, class... Args>
    constexpr unspecified bind_back(Args&&...);                                     // freestanding

  // [func.bind], bind
  template<class T> struct is_bind_expression;                                      // freestanding
  template<class T>
    constexpr bool is_bind_expression_v =                                           // freestanding
      is_bind_expression<T>::value;
  template<class T> struct is_placeholder;                                          // freestanding
  template<class T>
    constexpr int is_placeholder_v =                                                // freestanding
      is_placeholder<T>::value;

  template<class F, class... BoundArgs>
    constexpr unspecified bind(F&&, BoundArgs&&...);                                // freestanding
  template<class R, class F, class... BoundArgs>
    constexpr unspecified bind(F&&, BoundArgs&&...);                                // freestanding

  namespace placeholders {
    // M is the implementation-defined number of placeholders
    see belownc _1;                                                                   // freestanding
    see belownc _2;                                                                   // freestanding
               ⋮
    see belownc _M;                                                                   // freestanding
  }

  // [func.memfn], member function adaptors
  template<class R, class T>
    constexpr unspecified mem_fn(R T::*) noexcept;                                  // freestanding

  // [func.wrap], polymorphic function wrappers
  // [func.wrap.badcall], class bad_function_call
  class bad_function_call;

  // [func.wrap.func], class template function
  template<class> class function;       // not defined
  template<class R, class... ArgTypes> class function<R(ArgTypes...)>;

  // [func.wrap.func.alg], function specialized algorithms
  template<class R, class... ArgTypes>
    void swap(function<R(ArgTypes...)>&, function<R(ArgTypes...)>&) noexcept;

  // [func.wrap.func.nullptr], function null pointer comparison operator functions
  template<class R, class... ArgTypes>
    bool operator==(const function<R(ArgTypes...)>&, nullptr_t) noexcept;

  // [func.wrap.move], move-only wrapper
  template<class... S> class move_only_function;                        // not defined
  template<class R, class... ArgTypes>
    class move_only_function<R(ArgTypes...) cv{}\itcorr[-1] ref noexcept(noex)>;     // see below

  // [func.wrap.copy], copyable wrapper
  template<class... S> class copyable_function;                         // not defined
  template<class R, class... ArgTypes>
    class copyable_function<R(ArgTypes...) cv{}\itcorr[-1] ref noexcept(noex)>;      // see below

  // [func.wrap.ref], non-owning wrapper
  template<class... S> class function_ref;                              // freestanding, not defined
  template<class R, class... ArgTypes>
    class function_ref<R(ArgTypes...) cv{}\itcorr[-1] noexcept(noex)>;               // freestanding, see below

  // [func.search], searchers
  template<class ForwardIterator1, class BinaryPredicate = equal_to<>>
    class default_searcher;                                                         // freestanding

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
    struct hash;                                                                    // freestanding

  namespace ranges {
    // [range.cmp], concept-constrained comparisons
    struct equal_to;                                                                // freestanding
    struct not_equal_to;                                                            // freestanding
    struct greater;                                                                 // freestanding
    struct less;                                                                    // freestanding
    struct greater_equal;                                                           // freestanding
    struct less_equal;                                                              // freestanding
  }

  template<class Fn, class... Args>
    concept \defexposconceptnc{callable} =                                                  // exposition only
      requires (Fn&& fn, Args&&... args) {
        std::forward<Fn>(fn)(std::forward<Args>(args)...);
      };

  template<class Fn, class... Args>
    concept \defexposconceptnc{nothrow-callable} =                                          // exposition only
      callable<Fn, Args...> &&
      requires (Fn&& fn, Args&&... args) {
        { std::forward<Fn>(fn)(std::forward<Args>(args)...) } noexcept;
      };

  template<class Fn, class... Args>
    using call-result-t = decltype(declval<Fn>()(declval<Args>()...));  // exposition only

  template<const auto& T>
    using decayed-typeof = decltype(auto(T));                           // exposition only
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

Define `INVOKE(f, t_1, t_2, \dotsc, t_N)` as follows:

- `(t_1.*f)(t_2, \dotsc, t_N)` when `f` is a pointer to a member
  function of a class `T` and
  `is_same_v<T, remove_cvref_t<decltype(t_1)>> ||`
  `is_base_of_v<T, remove_cvref_t<decltype(t_1)>>` is `true`;
- `(t_1.get().*f)(t_2, \dotsc, t_N)` when `f` is a pointer to a member
  function of a class `T` and `remove_cvref_t<decltype(t_1)>` is a
  specialization of `reference_wrapper`;
- `((*t_1).*f)(t_2, \dotsc, t_N)` when `f` is a pointer to a member
  function of a class `T` and `t_1` does not satisfy the previous two
  items;
- `t_1.*f` when N = 1 and `f` is a pointer to data member of a class `T`
  and `is_same_v<T, remove_cvref_t<decltype(t_1)>> ||`
  `is_base_of_v<T, remove_cvref_t<decltype(t_1)>>` is `true`;
- `t_1.get().*f` when N = 1 and `f` is a pointer to data member of a
  class `T` and `remove_cvref_t<decltype(t_1)>` is a specialization of
  `reference_wrapper`;
- `(*t_1).*f` when N = 1 and `f` is a pointer to data member of a class
  `T` and `t_1` does not satisfy the previous two items;
- `f(t_1, t_2, \dotsc, t_N)` in all other cases.

Define `INVOKE<R>(f, t_1, t_2, \dotsc, t_N)` as
`static_cast<void>(INVOKE(f, t_1, t_2, \dotsc, t_N))` if `R` is
cv `void`, otherwise `INVOKE(f, t_1, t_2, \dotsc, t_N)` implicitly
converted to `R`. If
`reference_converts_from_temporary_v<R, decltype(INVOKE(f, t_1, t_2, \dotsc, t_N))>`
is `true`, `INVOKE<R>(f, t_1, t_2, \dotsc, t_N)` is ill-formed.

Every call wrapper [[func.def]] meets the *Cpp17MoveConstructible* and
*Cpp17Destructible* requirements. An *argument forwarding call wrapper*
is a call wrapper that can be called with an arbitrary argument list and
delivers the arguments to the target object as references. This
forwarding step delivers rvalue arguments as rvalue references and
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
wrapper is expression-equivalent [[defns.expression.equivalent]] to an
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

### `invoke` functions <a id="func.invoke">[[func.invoke]]</a>

``` cpp
template<class F, class... Args>
  constexpr invoke_result_t<F, Args...> invoke(F&& f, Args&&... args)
    noexcept(is_nothrow_invocable_v<F, Args...>);
```

*Constraints:* `is_invocable_v<F, Args...>` is `true`.

*Returns:* *INVOKE*(std::forward\<F\>(f),
std::forward\<Args\>(args)...) [[func.require]].

``` cpp
template<class R, class F, class... Args>
  constexpr R invoke_r(F&& f, Args&&... args)
    noexcept(is_nothrow_invocable_r_v<R, F, Args...>);
```

*Constraints:* `is_invocable_r_v<R, F, Args...>` is `true`.

*Returns:* *INVOKE*\<R\>(std::forward\<F\>(f),
std::forward\<Args\>(args)...) [[func.require]].

### Class template `reference_wrapper` <a id="refwrap">[[refwrap]]</a>

#### General <a id="refwrap.general">[[refwrap.general]]</a>

``` cpp
namespace std {
  template<class T> class reference_wrapper {
  public:
    // types
    using type = T;

    // [refwrap.const], constructors
    template<class U>
      constexpr reference_wrapper(U&&) noexcept(see below);
    constexpr reference_wrapper(const reference_wrapper& x) noexcept;

    // [refwrap.assign], assignment
    constexpr reference_wrapper& operator=(const reference_wrapper& x) noexcept;

    // [refwrap.access], access
    constexpr operator T& () const noexcept;
    constexpr T& get() const noexcept;

    // [refwrap.invoke], invocation
    template<class... ArgTypes>
      constexpr invoke_result_t<T&, ArgTypes...> operator()(ArgTypes&&...) const
        noexcept(is_nothrow_invocable_v<T&, ArgTypes...>);

    // [refwrap.comparisons], comparisons
    friend constexpr bool operator==(reference_wrapper, reference_wrapper);
    friend constexpr bool operator==(reference_wrapper, const T&);
    friend constexpr bool operator==(reference_wrapper, reference_wrapper<const T>);

    friend constexpr auto operator<=>(reference_wrapper, reference_wrapper);
    friend constexpr auto operator<=>(reference_wrapper, const T&);
    friend constexpr auto operator<=>(reference_wrapper, reference_wrapper<const T>);
  };

  template<class T>
    reference_wrapper(T&) -> reference_wrapper<T>;
}
```

`reference_wrapper<T>` is a *Cpp17CopyConstructible* and
*Cpp17CopyAssignable* wrapper around a reference to an object or
function of type `T`.

`reference_wrapper<T>` is a trivially copyable type
[[term.trivially.copyable.type]].

The template parameter `T` of `reference_wrapper` may be an incomplete
type.

[*Note 1*: Using the comparison operators described in
[[refwrap.comparisons]] with `T` being an incomplete type can lead to an
ill-formed program with no diagnostic required
[[temp.point]], [[temp.constr.atomic]]. — *end note*]

#### Constructors <a id="refwrap.const">[[refwrap.const]]</a>

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

*Remarks:* The exception specification is equivalent to
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
    operator()(ArgTypes&&... args) const noexcept(is_nothrow_invocable_v<T&, ArgTypes...>);
```

*Mandates:* `T` is a complete type.

*Returns:* *INVOKE*(get(),
std::forward\<ArgTypes\>(args)...) [[func.require]].

#### Comparisons <a id="refwrap.comparisons">[[refwrap.comparisons]]</a>

``` cpp
friend constexpr bool operator==(reference_wrapper x, reference_wrapper y);
```

*Constraints:* The expression `x.get() == y.get()` is well-formed and
its result is convertible to `bool`.

*Returns:* `x.get() == y.get()`.

``` cpp
friend constexpr bool operator==(reference_wrapper x, const T& y);
```

*Constraints:* The expression `x.get() == y` is well-formed and its
result is convertible to `bool`.

*Returns:* `x.get() == y`.

``` cpp
friend constexpr bool operator==(reference_wrapper x, reference_wrapper<const T> y);
```

*Constraints:* `is_const_v<T>` is `false` and the expression
`x.get() == y.get()` is well-formed and its result is convertible to
`bool`.

*Returns:* `x.get() == y.get()`.

``` cpp
friend constexpr auto operator<=>(reference_wrapper x, reference_wrapper y);
```

*Constraints:* The expression *`synth-three-way`*`(x.get(), y.get())` is
well-formed.

*Returns:* *`synth-three-way`*`(x.get(), y.get())`.

``` cpp
friend constexpr auto operator<=>(reference_wrapper x, const T& y);
```

*Constraints:* The expression *`synth-three-way`*`(x.get(), y)` is
well-formed.

*Returns:* *`synth-three-way`*`(x.get(), y)`.

``` cpp
friend constexpr auto operator<=>(reference_wrapper x, reference_wrapper<const T> y);
```

*Constraints:* `is_const_v<T>` is `false`. The expression
*`synth-three-way`*`(x.get(), y.get())` is well-formed.

*Returns:* *`synth-three-way`*`(x.get(), y.get())`.

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

*Returns:* `t`.

``` cpp
template<class T> constexpr reference_wrapper<const T> cref(const T& t) noexcept;
```

*Returns:* `reference_wrapper<const T>(t)`.

``` cpp
template<class T> constexpr reference_wrapper<const T> cref(reference_wrapper<T> t) noexcept;
```

*Returns:* `t`.

#### `common_reference` related specializations <a id="refwrap.common.ref">[[refwrap.common.ref]]</a>

``` cpp
namespace std {
  template<class T>
    constexpr bool is-ref-wrapper = false;                              // exposition only

  template<class T>
    constexpr bool is-ref-wrapper<reference_wrapper<T>> = true;

  template<class R, class T, class RQ, class TQ>
    concept ref-wrap-common-reference-exists-with =                     // exposition only
      is-ref-wrapper<R> &&
      requires { typename common_reference_t<typename R::type&, TQ>; } &&
      convertible_to<RQ, common_reference_t<typename R::type&, TQ>>;

  template<class R, class T, template<class> class RQual, template<class> class TQual>
    requires (ref-wrap-common-reference-exists-with<R, T, RQual<R>, TQual<T>> &&
              !ref-wrap-common-reference-exists-with<T, R, TQual<T>, RQual<R>>)
  struct basic_common_reference<R, T, RQual, TQual> {
    using type = common_reference_t<typename R::type&, TQual<T>>;
  };

  template<class T, class R, template<class> class TQual, template<class> class RQual>
    requires (ref-wrap-common-reference-exists-with<R, T, RQual<R>, TQual<T>> &&
              !ref-wrap-common-reference-exists-with<T, R, TQual<T>, RQual<R>>)
  struct basic_common_reference<T, R, TQual, RQual> {
    using type = common_reference_t<typename R::type&, TQual<T>>;
  };
}
```

### Arithmetic operations <a id="arithmetic.operations">[[arithmetic.operations]]</a>

#### General <a id="arithmetic.operations.general">[[arithmetic.operations.general]]</a>

The library provides basic function object classes for all of the
arithmetic operators in the language [[expr.mul]], [[expr.add]].

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

#### General <a id="comparisons.general">[[comparisons.general]]</a>

The library provides basic function object classes for all of the
comparison operators in the language [[expr.rel]], [[expr.eq]].

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

``` cpp
namespace std {
  struct compare_three_way {
    template<class T, class U>
      constexpr auto operator()(T&& t, U&& u) const;

    using is_transparent = unspecified;
  };
}
```

``` cpp
template<class T, class U>
  constexpr auto operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `three_way_comparable_with`.

*Preconditions:* If the expression
`std::forward<T>(t) <=> std::forward<U>(u)` results in a call to a
built-in operator `<=>` comparing pointers of type `P`, the conversion
sequences from both `T` and `U` to `P` are
equality-preserving [[concepts.equality]]; otherwise, `T` and `U` model
`three_way_comparable_with`.

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

``` cpp
struct ranges::equal_to {
  template<class T, class U>
    constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  constexpr bool operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `equality_comparable_with`.

*Preconditions:* If the expression
`std::forward<T>(t) == std::forward<U>(u)` results in a call to a
built-in operator `==` comparing pointers of type `P`, the conversion
sequences from both `T` and `U` to `P` are
equality-preserving [[concepts.equality]]; otherwise, `T` and `U` model
`equality_comparable_with`.

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
    constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  constexpr bool operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `equality_comparable_with`.

*Effects:* Equivalent to:

``` cpp
return !ranges::equal_to{}(std::forward<T>(t), std::forward<U>(u));
```

``` cpp
struct ranges::greater {
  template<class T, class U>
    constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  constexpr bool operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `totally_ordered_with`.

*Effects:* Equivalent to:

``` cpp
return ranges::less{}(std::forward<U>(u), std::forward<T>(t));
```

``` cpp
struct ranges::less {
  template<class T, class U>
    constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  constexpr bool operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `totally_ordered_with`.

*Preconditions:* If the expression
`std::forward<T>(t) < std::forward<U>(u)` results in a call to a
built-in operator `<` comparing pointers of type `P`, the conversion
sequences from both `T` and `U` to `P` are
equality-preserving [[concepts.equality]]; otherwise, `T` and `U` model
`totally_ordered_with`. For any expressions `ET` and `EU` such that
`decltype((ET))` is `T` and `decltype((EU))` is `U`, exactly one of
`ranges::less{}(ET, EU)`, `ranges::less{}(EU, ET)`, or
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
    constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  constexpr bool operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `totally_ordered_with`.

*Effects:* Equivalent to:

``` cpp
return !ranges::less{}(std::forward<T>(t), std::forward<U>(u));
```

``` cpp
struct ranges::less_equal {
  template<class T, class U>
    constexpr bool operator()(T&& t, U&& u) const;

  using is_transparent = unspecified;
};
```

``` cpp
template<class T, class U>
  constexpr bool operator()(T&& t, U&& u) const;
```

*Constraints:* `T` and `U` satisfy `totally_ordered_with`.

*Effects:* Equivalent to:

``` cpp
return !ranges::less{}(std::forward<U>(u), std::forward<T>(t));
```

### Logical operations <a id="logical.operations">[[logical.operations]]</a>

#### General <a id="logical.operations.general">[[logical.operations.general]]</a>

The library provides basic function object classes for all of the
logical operators in the language
[[expr.log.and]], [[expr.log.or]], [[expr.unary.op]].

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

#### General <a id="bitwise.operations.general">[[bitwise.operations.general]]</a>

The library provides basic function object classes for all of the
bitwise operators in the language
[[expr.bit.and]], [[expr.or]], [[expr.xor]], [[expr.unary.op]].

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
template<class T> constexpr auto operator()(T&& t) const
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

*Returns:* A perfect forwarding call
wrapper [[term.perfect.forwarding.call.wrapper]] `g` with call pattern
`!invoke(fd, call_args...)`.

*Throws:* Any exception thrown by the initialization of `fd`.

``` cpp
template<auto f> constexpr unspecified not_fn() noexcept;
```

In the text that follows:

- `F` is the type of `f`,
- `g` is a value of the result of a `not_fn` invocation,
- `call_args` is an argument pack used in a function call
  expression [[expr.call]] of `g`.

*Mandates:* If `is_pointer_v<F> || is_member_pointer_v<F>` is `true`,
then `f != nullptr` is `true`.

*Returns:* A perfect forwarding call wrapper [[func.require]] `g` that
does not have state entities, and has the call pattern
`!invoke(f, call_args...)`.

### Function templates `bind_front` and `bind_back` <a id="func.bind.partial">[[func.bind.partial]]</a>

``` cpp
template<class F, class... Args>
  constexpr unspecified bind_front(F&& f, Args&&... args);
template<class F, class... Args>
  constexpr unspecified bind_back(F&& f, Args&&... args);
```

Within this subclause:

- `g` is a value of the result of a `bind_front` or `bind_back`
  invocation,
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

*Returns:* A perfect forwarding call
wrapper [[term.perfect.forwarding.call.wrapper]] `g` with call pattern:

- `invoke(fd, bound_args..., call_args...)` for a `bind_front`
  invocation, or
- `invoke(fd, call_args..., bound_args...)` for a `bind_back`
  invocation.

*Throws:* Any exception thrown by the initialization of the state
entities of `g`[[func.def]].

``` cpp
template<auto f, class... Args>
  constexpr unspecified bind_front(Args&&... args);
template<auto f, class... Args>
  constexpr unspecified bind_back(Args&&... args);
```

Within this subclause:

- `F` is the type of `f`,
- `g` is a value of the result of a `bind_front` or `bind_back`
  invocation,
- `BoundArgs` is a pack that denotes `decay_t<Args>...`,
- `bound_args` is a pack of bound argument entities of `g`[[func.def]]
  of types `BoundArgs...`, direct-non-list-initialized with
  `std::forward<Args>(args)...`, respectively, and
- `call_args` is an argument pack used in a function call
  expression [[expr.call]] of `g`.

*Mandates:*

- `(is_constructible_v<BoundArgs, Args> && ...)` is `true`, and
- `(is_move_constructible_v<BoundArgs> && ...)` is `true`, and
- if `is_pointer_v<F> || is_member_pointer_v<F>` is `true`, then
  `f != nullptr` is `true`.

*Preconditions:* For each `Tᵢ` in `BoundArgs`, `Tᵢ` meets the
*Cpp17MoveConstructible* requirements.

*Returns:* A perfect forwarding call wrapper [[func.require]] `g` that
does not have a target object, and has the call pattern:

- `invoke(f, bound_args..., call_args...)` for a `bind_front`
  invocation, or
- `invoke(f, call_args..., bound_args...)` for a `bind_back` invocation.

*Throws:* Any exception thrown by the initialization of `bound_args`.

### Function object binders <a id="func.bind">[[func.bind]]</a>

#### General <a id="func.bind.general">[[func.bind.general]]</a>

Subclause [[func.bind]] describes a uniform mechanism for binding
arguments of callable objects.

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
placeholders `_1`, `_2`, and so on [[func.bind.place]]. The function
template `bind` uses `is_placeholder` to detect placeholders.

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
- `TDᵢ` is the type `decay_t<\tcode{T}_i>`,
- `tᵢ` is the iᵗʰ argument in the function parameter pack `bound_args`,
- `tdᵢ` is a bound argument entity of `g` [[func.def]] of type `TDᵢ`
  direct-non-list-initialized with
  `std::forward<{}\tcode{T}_i>(\tcode{t}_i)`,
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
expression-equivalent [[defns.expression.equivalent]] to

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

- if `TDᵢ` is `reference_wrapper<T>`, the argument is
  `\tcode{td}_i.get()` and its type `Vᵢ` is `T&`;
- if the value of `is_bind_expression_v<\tcode{TD}_i>` is `true`, the
  argument is
  ``` cpp
  static_cast<cv{} $TD_i$&>(td_i)(std::forward<U_j>(u_j)...)
  ```

  and its type `Vᵢ` is
  `invoke_result_t<cv{} \tcode{TD}_i&, \tcode{U}_j...>&&`;
- if the value `j` of `is_placeholder_v<\tcode{TD}_i>` is not zero, the
  argument is `std::forward<\tcode{U}_j>(\tcode{u}_j)` and its type `Vᵢ`
  is `\tcode{U}_j&&`;
- otherwise, the value is `tdᵢ` and its type `Vᵢ` is
  `cv{} \tcode{TD}_i&`.

The value of the target argument `v`_`fd` is `fd` and its corresponding
type `V`_`fd` is `cv{} FD&`.

#### Placeholders <a id="func.bind.place">[[func.bind.place]]</a>

``` cpp
namespace std::placeholders {
  // M is the number of placeholders
  see below _1;
  see below _2;
             \itcorr⋮
  see below _M;
}
```

The number `M` of placeholders is *implementation-defined*.

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

Placeholders are freestanding items [[freestanding.item]].

### Function template `mem_fn` <a id="func.memfn">[[func.memfn]]</a>

``` cpp
template<class R, class T> constexpr unspecified mem_fn(R T::* pm) noexcept;
```

*Returns:* A simple call wrapper [[term.simple.call.wrapper]] `fn` with
call pattern `invoke(pmd, call_args...)`, where `pmd` is the target
object of `fn` of type `R T::*` direct-non-list-initialized with `pm`,
and `call_args` is an argument pack used in a function call
expression [[expr.call]] of `fn`.

### Polymorphic function wrappers <a id="func.wrap">[[func.wrap]]</a>

#### General <a id="func.wrap.general">[[func.wrap.general]]</a>

Subclause [[func.wrap]] describes polymorphic wrapper classes that
encapsulate arbitrary callable objects.

Let `t` be an object of a type that is a specialization of `function`,
`copyable_function`, or `move_only_function`, such that the target
object `x` of `t` has a type that is a specialization of `function`,
`copyable_function`, or `move_only_function`. Each argument of the
invocation of `x` evaluated as part of the invocation of `t` may alias
an argument in the same position in the invocation of `t` that has the
same type, even if the corresponding parameter is not of reference type.

[*Example 1*:

``` cpp
move_only_function<void(T)> f{copyable_function<void(T)>{[](T) {}}};
T t;
f(t);                               // it is unspecified how many copies of T are made
```

— *end example*]

*Recommended practice:* Implementations should avoid double wrapping
when constructing polymorphic wrappers from one another.

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

##### General <a id="func.wrap.func.general">[[func.wrap.func.general]]</a>

``` cpp
namespace std {
  template<class R, class... ArgTypes>
  class function<R(ArgTypes...)> {
  public:
    using result_type = R;

    // [func.wrap.func.con], construct/copy/destroy
    function() noexcept;
    function(nullptr_t) noexcept;
    function(const function&);
    function(function&&) noexcept;
    template<class F> function(F&&);

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
}
```

The `function` class template provides polymorphic wrappers that
generalize the notion of a function pointer. Wrappers can store, copy,
and call arbitrary callable objects [[func.def]], given a call signature
[[func.def]].

The `function` class template is a call wrapper [[func.def]] whose call
signature [[func.def]] is `R(ArgTypes...)`.

[*Note 1*: The types deduced by the deduction guides for `function`
might change in future revisions of C++. — *end note*]

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

*Ensures:* `!*this` if `!f`; otherwise, the target object of `*this` is
a copy of the target object of `f`.

*Throws:* Nothing if `f`’s target is a specialization of
`reference_wrapper` or a function pointer. Otherwise, may throw
`bad_alloc` or any exception thrown by the copy constructor of the
stored callable object.

*Recommended practice:* Implementations should avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f`’s target is an object holding only a pointer or reference to
an object and a member function pointer.

``` cpp
function(function&& f) noexcept;
```

*Ensures:* If `!f`, `*this` has no target; otherwise, the target of
`*this` is equivalent to the target of `f` before the construction, and
`f` is in a valid state with an unspecified value.

*Recommended practice:* Implementations should avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f`’s target is an object holding only a pointer or reference to
an object and a member function pointer.

``` cpp
template<class F> function(F&& f);
```

Let `FD` be `decay_t<F>`.

*Constraints:*

- `is_same_v<remove_cvref_t<F>, function>` is `false`, and
- `is_invocable_r_v<R, FD&, ArgTypes...>` is `true`.

*Mandates:*

- `is_copy_constructible_v<FD>` is `true`, and
- `is_constructible_v<FD, F>` is `true`.

*Preconditions:* `FD` meets the *Cpp17CopyConstructible* requirements.

*Ensures:* `!*this` is `true` if any of the following hold:

- `f` is a null function pointer value.
- `f` is a null member pointer value.
- `remove_cvref_t<F>` is a specialization of the `function` class
  template, and `!f` is `true`.

Otherwise, `*this` has a target object of type `FD`
direct-non-list-initialized with `std::forward<F>(f)`.

*Throws:* Nothing if `FD` is a specialization of `reference_wrapper` or
a function pointer type. Otherwise, may throw `bad_alloc` or any
exception thrown by the initialization of the target object.

*Recommended practice:* Implementations should avoid the use of
dynamically allocated memory for small callable objects, for example,
where `f` refers to an object holding only a pointer or reference to an
object and a member function pointer.

``` cpp
template<class F> function(F) -> function<see below>;
```

*Constraints:* `&F::operator()` is well-formed when treated as an
unevaluated operand and either

- `F::operator()` is a non-static member function and
  `decltype(&F::operator())` is either of the form
  `R(G::*)(A...)` cv `&ₒₚₜ noexceptₒₚₜ` or of the form
  `R(*)(G, A...) noexceptₒₚₜ` for a type `G`, or
- `F::operator()` is a static member function and
  `decltype(&F::operator())` is of the form `R(*)(A...) noexceptₒₚₜ`.

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

*Constraints:* `is_invocable_r_v<R, decay_t<F>&, ArgTypes...>` is
`true`.

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

*Effects:* Interchanges the target objects of `*this` and `other`.

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
thrown by the target object.

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

##### Null pointer comparison operator functions <a id="func.wrap.func.nullptr">[[func.wrap.func.nullptr]]</a>

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

#### Move-only wrapper <a id="func.wrap.move">[[func.wrap.move]]</a>

##### General <a id="func.wrap.move.general">[[func.wrap.move.general]]</a>

The header provides partial specializations of `move_only_function` for
each combination of the possible replacements of the placeholders cv,
*ref*, and *noex* where

- cv is either const or empty,
- *ref* is either `&`, `&&`, or empty, and
- *noex* is either `true` or `false`.

For each of the possible combinations of the placeholders mentioned
above, there is a placeholder *inv-quals* defined as follows:

- If *ref* is empty, let *inv-quals* be cv`&`,
- otherwise, let *inv-quals* be cv *ref*.

##### Class template `move_only_function` <a id="func.wrap.move.class">[[func.wrap.move.class]]</a>

``` cpp
namespace std {
  template<class R, class... ArgTypes>
  class move_only_function<R(ArgTypes...) cv{} ref noexcept(noex)> {
  public:
    using result_type = R;

    // [func.wrap.move.ctor], constructors, assignments, and destructor
    move_only_function() noexcept;
    move_only_function(nullptr_t) noexcept;
    move_only_function(move_only_function&&) noexcept;
    template<class F> move_only_function(F&&);
    template<class T, class... Args>
      explicit move_only_function(in_place_type_t<T>, Args&&...);
    template<class T, class U, class... Args>
      explicit move_only_function(in_place_type_t<T>, initializer_list<U>, Args&&...);

    move_only_function& operator=(move_only_function&&);
    move_only_function& operator=(nullptr_t) noexcept;
    template<class F> move_only_function& operator=(F&&);

    ~move_only_function();

    // [func.wrap.move.inv], invocation
    explicit operator bool() const noexcept;
    R operator()(ArgTypes...) cv{} ref noexcept(noex);

    // [func.wrap.move.util], utility
    void swap(move_only_function&) noexcept;
    friend void swap(move_only_function&, move_only_function&) noexcept;
    friend bool operator==(const move_only_function&, nullptr_t) noexcept;

  private:
    template<class VT>
      static constexpr bool is-callable-from = see below;       // exposition only
  };
}
```

The `move_only_function` class template provides polymorphic wrappers
that generalize the notion of a callable object [[func.def]]. These
wrappers can store, move, and call arbitrary callable objects, given a
call signature.

*Recommended practice:* Implementations should avoid the use of
dynamically allocated memory for a small contained value.

[*Note 1*: Such small-object optimization can only be applied to a type
`T` for which `is_nothrow_move_constructible_v<T>` is
`true`. — *end note*]

##### Constructors, assignments, and destructor <a id="func.wrap.move.ctor">[[func.wrap.move.ctor]]</a>

``` cpp
template<class VT>
  static constexpr bool is-callable-from = see below;
```

If *noex* is `true`, *`is-callable-from`*`<VT>` is equal to:

``` cpp
is_nothrow_invocable_r_v<R, VT cv{} ref, ArgTypes...> &&
is_nothrow_invocable_r_v<R, VT inv-quals, ArgTypes...>
```

Otherwise, *`is-callable-from`*`<VT>` is equal to:

``` cpp
is_invocable_r_v<R, VT cv{} ref, ArgTypes...> &&
is_invocable_r_v<R, VT inv-quals, ArgTypes...>
```

``` cpp
move_only_function() noexcept;
move_only_function(nullptr_t) noexcept;
```

*Ensures:* `*this` has no target object.

``` cpp
move_only_function(move_only_function&& f) noexcept;
```

*Ensures:* The target object of `*this` is the target object `f` had
before construction, and `f` is in a valid state with an unspecified
value.

``` cpp
template<class F> move_only_function(F&& f);
```

Let `VT` be `decay_t<F>`.

*Constraints:*

- `remove_cvref_t<F>` is not the same type as `move_only_function`, and
- `remove_cvref_t<F>` is not a specialization of `in_place_type_t`, and
- *`is-callable-from`*`<VT>` is `true`.

*Mandates:* `is_constructible_v<VT, F>` is `true`.

*Preconditions:* `VT` meets the *Cpp17Destructible* requirements, and if
`is_move_constructible_v<VT>` is `true`, `VT` meets the
*Cpp17MoveConstructible* requirements.

*Ensures:* `*this` has no target object if any of the following hold:

- `f` is a null function pointer value, or
- `f` is a null member pointer value, or
- `remove_cvref_t<F>` is a specialization of the `move_only_function`
  class template, and `f` has no target object.

Otherwise, `*this` has a target object of type `VT`
direct-non-list-initialized with `std::forward<F>(f)`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc` unless `VT` is a function pointer or a
specialization of `reference_wrapper`.

``` cpp
template<class T, class... Args>
  explicit move_only_function(in_place_type_t<T>, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:*

- `is_constructible_v<VT, Args...>` is `true`, and
- *`is-callable-from`*`<VT>` is `true`.

*Mandates:* `VT` is the same type as `T`.

*Preconditions:* `VT` meets the *Cpp17Destructible* requirements, and if
`is_move_constructible_v<VT>` is `true`, `VT` meets the
*Cpp17MoveConstructible* requirements.

*Ensures:* `*this` has a target object of type `VT`
direct-non-list-initialized with `std::forward<Args>(args)...`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc` unless `VT` is a function pointer or a
specialization of `reference_wrapper`.

``` cpp
template<class T, class U, class... Args>
  explicit move_only_function(in_place_type_t<T>, initializer_list<U> ilist, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:*

- `is_constructible_v<VT, initializer_list<U>&, Args...>` is `true`, and
- *`is-callable-from`*`<VT>` is `true`.

*Mandates:* `VT` is the same type as `T`.

*Preconditions:* `VT` meets the *Cpp17Destructible* requirements, and if
`is_move_constructible_v<VT>` is `true`, `VT` meets the
*Cpp17MoveConstructible* requirements.

*Ensures:* `*this` has a target object of type `VT`
direct-non-list-initialized with `ilist, std::forward<Args>(args)...`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc` unless `VT` is a function pointer or a
specialization of `reference_wrapper`.

``` cpp
move_only_function& operator=(move_only_function&& f);
```

*Effects:* Equivalent to:
`move_only_function(std::move(f)).swap(*this);`

*Returns:* `*this`.

``` cpp
move_only_function& operator=(nullptr_t) noexcept;
```

*Effects:* Destroys the target object of `*this`, if any.

*Returns:* `*this`.

``` cpp
template<class F> move_only_function& operator=(F&& f);
```

*Effects:* Equivalent to:
`move_only_function(std::forward<F>(f)).swap(*this);`

*Returns:* `*this`.

``` cpp
~move_only_function();
```

*Effects:* Destroys the target object of `*this`, if any.

##### Invocation <a id="func.wrap.move.inv">[[func.wrap.move.inv]]</a>

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `true` if `*this` has a target object, otherwise `false`.

``` cpp
R operator()(ArgTypes... args) cv{} ref noexcept(noex);
```

*Preconditions:* `*this` has a target object.

*Effects:* Equivalent to:

``` cpp
return INVOKE<R>(static_cast<F inv-quals>(f), std::forward<ArgTypes>(args)...);
```

where `f` is an lvalue designating the target object of `*this` and `F`
is the type of `f`.

##### Utility <a id="func.wrap.move.util">[[func.wrap.move.util]]</a>

``` cpp
void swap(move_only_function& other) noexcept;
```

*Effects:* Exchanges the target objects of `*this` and `other`.

``` cpp
friend void swap(move_only_function& f1, move_only_function& f2) noexcept;
```

*Effects:* Equivalent to `f1.swap(f2)`.

``` cpp
friend bool operator==(const move_only_function& f, nullptr_t) noexcept;
```

*Returns:* `true` if `f` has no target object, otherwise `false`.

#### Copyable wrapper <a id="func.wrap.copy">[[func.wrap.copy]]</a>

##### General <a id="func.wrap.copy.general">[[func.wrap.copy.general]]</a>

The header provides partial specializations of `copyable_function` for
each combination of the possible replacements of the placeholders cv,
*ref*, and *noex* where

- cv is either const or empty,
- *ref* is either `&`, `&&`, or empty, and
- *noex* is either `true` or `false`.

For each of the possible combinations of the placeholders mentioned
above, there is a placeholder *inv-quals* defined as follows:

- If *ref* is empty, let *inv-quals* be cv`&`,
- otherwise, let *inv-quals* be cv *ref*.

##### Class template `copyable_function` <a id="func.wrap.copy.class">[[func.wrap.copy.class]]</a>

``` cpp
namespace std {
  template<class R, class... ArgTypes>
  class copyable_function<R(ArgTypes...) cv{} ref noexcept(noex)> {
  public:
    using result_type = R;

    // [func.wrap.copy.ctor], constructors, assignments, and destructor
    copyable_function() noexcept;
    copyable_function(nullptr_t) noexcept;
    copyable_function(const copyable_function&);
    copyable_function(copyable_function&&) noexcept;
    template<class F> copyable_function(F&&);
    template<class T, class... Args>
      explicit copyable_function(in_place_type_t<T>, Args&&...);
    template<class T, class U, class... Args>
      explicit copyable_function(in_place_type_t<T>, initializer_list<U>, Args&&...);

    copyable_function& operator=(const copyable_function&);
    copyable_function& operator=(copyable_function&&);
    copyable_function& operator=(nullptr_t) noexcept;
    template<class F> copyable_function& operator=(F&&);

    ~copyable_function();

    // [func.wrap.copy.inv], invocation
    explicit operator bool() const noexcept;
    R operator()(ArgTypes...) cv{} ref noexcept(noex);

    // [func.wrap.copy.util], utility
    void swap(copyable_function&) noexcept;
    friend void swap(copyable_function&, copyable_function&) noexcept;
    friend bool operator==(const copyable_function&, nullptr_t) noexcept;

  private:
    template<class VT>
      static constexpr bool is-callable-from = see below;       // exposition only
  };
}
```

The `copyable_function` class template provides polymorphic wrappers
that generalize the notion of a callable object [[func.def]]. These
wrappers can store, copy, move, and call arbitrary callable objects,
given a call signature.

*Recommended practice:* Implementations should avoid the use of
dynamically allocated memory for a small contained value.

[*Note 1*: Such small-object optimization can only be applied to a type
`T` for which `is_nothrow_move_constructible_v<T>` is
`true`. — *end note*]

##### Constructors, assignments, and destructor <a id="func.wrap.copy.ctor">[[func.wrap.copy.ctor]]</a>

``` cpp
template<class VT>
  static constexpr bool is-callable-from = see below;
```

If *noex* is `true`, *`is-callable-from`*`<VT>` is equal to:

``` cpp
is_nothrow_invocable_r_v<R, VT cv{} ref, ArgTypes...> &&
is_nothrow_invocable_r_v<R, VT inv-quals, ArgTypes...>
```

Otherwise, *`is-callable-from`*`<VT>` is equal to:

``` cpp
is_invocable_r_v<R, VT cv{} ref, ArgTypes...> &&
is_invocable_r_v<R, VT inv-quals, ArgTypes...>
```

``` cpp
copyable_function() noexcept;
copyable_function(nullptr_t) noexcept;
```

*Ensures:* `*this` has no target object.

``` cpp
copyable_function(const copyable_function& f);
```

*Ensures:* `*this` has no target object if `f` had no target object.
Otherwise, the target object of `*this` is a copy of the target object
of `f`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc`.

``` cpp
copyable_function(copyable_function&& f) noexcept;
```

*Ensures:* The target object of `*this` is the target object `f` had
before construction, and `f` is in a valid state with an unspecified
value.

``` cpp
template<class F> copyable_function(F&& f);
```

Let `VT` be `decay_t<F>`.

*Constraints:*

- `remove_cvref_t<F>` is not the same type as `copyable_function`, and
- `remove_cvref_t<F>` is not a specialization of `in_place_type_t`, and
- *`is-callable-from`*`<VT>` is `true`.

*Mandates:*

- `is_constructible_v<VT, F>` is `true`, and
- `is_copy_constructible_v<VT>` is `true`.

*Preconditions:* `VT` meets the *Cpp17Destructible* and
*Cpp17CopyConstructible* requirements.

*Ensures:* `*this` has no target object if any of the following hold:

- `f` is a null function pointer value, or
- `f` is a null member pointer value, or
- `remove_cvref_t<F>` is a specialization of the `copyable_function`
  class template, and `f` has no target object.

Otherwise, `*this` has a target object of type `VT`
direct-non-list-initialized with `std::forward<F>(f)`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc` unless `VT` is a function pointer or a
specialization of `reference_wrapper`.

``` cpp
template<class T, class... Args>
  explicit copyable_function(in_place_type_t<T>, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:*

- `is_constructible_v<VT, Args...>` is `true`, and
- *`is-callable-from`*`<VT>` is `true`.

*Mandates:*

- `VT` is the same type as `T`, and
- `is_copy_constructible_v<VT>` is `true`.

*Preconditions:* `VT` meets the *Cpp17Destructible* and
*Cpp17CopyConstructible* requirements.

*Ensures:* `*this` has a target object of type `VT`
direct-non-list-initialized with `std::forward<Args>(args)...`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc` unless `VT` is a pointer or a
specialization of `reference_wrapper`.

``` cpp
template<class T, class U, class... Args>
  explicit copyable_function(in_place_type_t<T>, initializer_list<U> ilist, Args&&... args);
```

Let `VT` be `decay_t<T>`.

*Constraints:*

- `is_constructible_v<VT, initializer_list<U>&, Args...>` is `true`, and
- *`is-callable-from`*`<VT>` is `true`.

*Mandates:*

- `VT` is the same type as `T`, and
- `is_copy_constructible_v<VT>` is `true`.

*Preconditions:* `VT` meets the *Cpp17Destructible* and
*Cpp17CopyConstructible* requirements.

*Ensures:* `*this` has a target object of type `VT`
direct-non-list-initialized with `ilist, std::forward<Args>(args)...`.

*Throws:* Any exception thrown by the initialization of the target
object. May throw `bad_alloc` unless `VT` is a pointer or a
specialization of `reference_wrapper`.

``` cpp
copyable_function& operator=(const copyable_function& f);
```

*Effects:* Equivalent to: `copyable_function(f).swap(*this);`

*Returns:* `*this`.

``` cpp
copyable_function& operator=(copyable_function&& f);
```

*Effects:* Equivalent to: `copyable_function(std::move(f)).swap(*this);`

*Returns:* `*this`.

``` cpp
copyable_function& operator=(nullptr_t) noexcept;
```

*Effects:* Destroys the target object of `*this`, if any.

*Returns:* `*this`.

``` cpp
template<class F> copyable_function& operator=(F&& f);
```

*Effects:* Equivalent to:
`copyable_function(std::forward<F>(f)).swap(*this);`

*Returns:* `*this`.

``` cpp
~copyable_function();
```

*Effects:* Destroys the target object of `*this`, if any.

##### Invocation <a id="func.wrap.copy.inv">[[func.wrap.copy.inv]]</a>

``` cpp
explicit operator bool() const noexcept;
```

*Returns:* `true` if `*this` has a target object, otherwise `false`.

``` cpp
R operator()(ArgTypes... args) cv{} ref noexcept(noex);
```

*Preconditions:* `*this` has a target object.

*Effects:* Equivalent to:

``` cpp
return INVOKE<R>(static_cast<F inv-quals>(f), std::forward<ArgTypes>(args)...);
```

where `f` is an lvalue designating the target object of `*this` and `F`
is the type of `f`.

##### Utility <a id="func.wrap.copy.util">[[func.wrap.copy.util]]</a>

``` cpp
void swap(copyable_function& other) noexcept;
```

*Effects:* Exchanges the target objects of `*this` and `other`.

``` cpp
friend void swap(copyable_function& f1, copyable_function& f2) noexcept;
```

*Effects:* Equivalent to `f1.swap(f2)`.

``` cpp
friend bool operator==(const copyable_function& f, nullptr_t) noexcept;
```

*Returns:* `true` if `f` has no target object, otherwise `false`.

#### Non-owning wrapper <a id="func.wrap.ref">[[func.wrap.ref]]</a>

##### General <a id="func.wrap.ref.general">[[func.wrap.ref.general]]</a>

The header provides partial specializations of `function_ref` for each
combination of the possible replacements of the placeholders cv and
*noex* where:

- cv is either const or empty, and
- *noex* is either `true` or `false`.

##### Class template `function_ref` <a id="func.wrap.ref.class">[[func.wrap.ref.class]]</a>

``` cpp
namespace std {
  template<class R, class... ArgTypes>
  class function_ref<R(ArgTypes...) cv{} noexcept(noex)> {
  public:
    // [func.wrap.ref.ctor], constructors and assignment operators
    template<class F> function_ref(F*) noexcept;
    template<class F> constexpr function_ref(F&&) noexcept;
    template<auto f> constexpr function_ref(nontype_t<f>) noexcept;
    template<auto f, class U> constexpr function_ref(nontype_t<f>, U&&) noexcept;
    template<auto f, class T> constexpr function_ref(nontype_t<f>, cv{} T*) noexcept;

    constexpr function_ref(const function_ref&) noexcept = default;
    constexpr function_ref& operator=(const function_ref&) noexcept = default;
    template<class T> function_ref& operator=(T) = delete;

    // [func.wrap.ref.inv], invocation
    R operator()(ArgTypes...) const noexcept(noex);

  private:
    template<class... T>
      static constexpr bool is-invocable-using = see belownc;             // exposition only

    R (*thunk-ptr)(BoundEntityType, ArgTypes&&...) noexcept(noex);      // exposition only
    BoundEntityType bound-entity;                                       // exposition only
  };

  // [func.wrap.ref.deduct], deduction guides
  template<class F>
    function_ref(F*) -> function_ref<F>;
  template<auto f>
    function_ref(nontype_t<f>) -> function_ref<see below>;
  template<auto f, class T>
    function_ref(nontype_t<f>, T&&) -> function_ref<see below>;
}
```

An object of class `function_ref<R(Args...) cv{} noexcept(noex)>` stores
a pointer to function *thunk-ptr* and an object *bound-entity*. The
object *bound-entity* has an unspecified trivially copyable type
*BoundEntityType*, that models `copyable` and is capable of storing a
pointer to object value or a pointer to function value. The type of
*thunk-ptr* is `R(*)(BoundEntityType, Args&&...) noexcept(noex)`.

Each specialization of `function_ref` is a trivially copyable type
[[term.trivially.copyable.type]] that models `copyable`.

Within subclause  [[func.wrap.ref]], `call-args` is an argument pack
with elements such that

``` cpp
decltype((call-args))...
```

denote `ArgTypes&&...` respectively.

##### Constructors and assignment operators <a id="func.wrap.ref.ctor">[[func.wrap.ref.ctor]]</a>

``` cpp
template<class... T>
  static constexpr bool is-invocable-using = see below;
```

If *noex* is `true`, *`is-invocable-using`*`<T...>` is equal to:

``` cpp
is_nothrow_invocable_r_v<R, T..., ArgTypes...>
```

Otherwise, *`is-invocable-using`*`<T...>` is equal to:

``` cpp
is_invocable_r_v<R, T..., ArgTypes...>
```

``` cpp
template<class F> function_ref(F* f) noexcept;
```

*Constraints:*

- `is_function_v<F>` is `true`, and
- *`is-invocable-using`*`<F>` is `true`.

*Preconditions:* `f` is not a null pointer.

*Effects:* Initializes *bound-entity* with `f`, and *thunk-ptr* with the
address of a function *`thunk`* such that
*`thunk`*`(`*`bound-entity`*`, `*`call-args`*`...)` is
expression-equivalent [[defns.expression.equivalent]] to
`invoke_r<R>(f, `*`call-args`*`...)`.

``` cpp
template<class F> constexpr function_ref(F&& f) noexcept;
```

Let `T` be `remove_reference_t<F>`.

*Constraints:*

- `remove_cvref_t<F>` is not the same type as `function_ref`,
- `is_member_pointer_v<T>` is `false`, and
- *`is-invocable-using`*`<cv T&>` is `true`.

*Effects:* Initializes *bound-entity* with `addressof(f)`, and
*thunk-ptr* with the address of a function *`thunk`* such that
*`thunk`*`(`*`bound-entity`*`, `*`call-args`*`...)` is
expression-equivalent [[defns.expression.equivalent]] to
`invoke_r<R>(static_cast<cv T&>(f), `*`call-args`*`...)`.

``` cpp
template<auto f> constexpr function_ref(nontype_t<f>) noexcept;
```

Let `F` be `decltype(f)`.

*Constraints:* *`is-invocable-using`*`<F>` is `true`.

*Mandates:* If `is_pointer_v<F> || is_member_pointer_v<F>` is `true`,
then `f != nullptr` is `true`.

*Effects:* Initializes *bound-entity* with a pointer to an unspecified
object or null pointer value, and *thunk-ptr* with the address of a
function *`thunk`* such that
*`thunk`*`(`*`bound-entity`*`, `*`call-args`*`...)` is
expression-equivalent [[defns.expression.equivalent]] to
`invoke_r<R>(f, `*`call-args`*`...)`.

``` cpp
template<auto f, class U>
  constexpr function_ref(nontype_t<f>, U&& obj) noexcept;
```

Let `T` be `remove_reference_t<U>` and `F` be `decltype(f)`.

*Constraints:*

- `is_rvalue_reference_v<U&&>` is `false`, and
- *`is-invocable-using`*`<F, cv T&>` is `true`.

*Mandates:* If `is_pointer_v<F> || is_member_pointer_v<F>` is `true`,
then `f != nullptr` is `true`.

*Effects:* Initializes *bound-entity* with `addressof(obj)`, and
*thunk-ptr* with the address of a function *`thunk`* such that
*`thunk`*`(`*`bound-entity`*`, `*`call-args`*`...)` is
expression-equivalent [[defns.expression.equivalent]] to
`invoke_r<R>(f, static_cast<cv T&>(obj), `*`call-args`*`...)`.

``` cpp
template<auto f, class T>
  constexpr function_ref(nontype_t<f>, cv{} T* obj) noexcept;
```

Let `F` be `decltype(f)`.

*Constraints:* *`is-invocable-using`*`<F, cv T*>` is `true`.

*Mandates:* If `is_pointer_v<F> || is_member_pointer_v<F>` is `true`,
then `f != nullptr` is `true`.

*Preconditions:* If `is_member_pointer_v<F>` is `true`, `obj` is not a
null pointer.

*Effects:* Initializes *bound-entity* with `obj`, and *thunk-ptr* with
the address of a function *`thunk`* such that
*`thunk`*`(`*`bound-entity`*`, `*`call-args`*`...)` is
expression-equivalent [[defns.expression.equivalent]] to
`invoke_r<R>(f, obj, `*`call-args`*`...)`.

``` cpp
template<class T> function_ref& operator=(T) = delete;
```

*Constraints:*

- `T` is not the same type as `function_ref`,
- `is_pointer_v<T>` is `false`, and
- `T` is not a specialization of `nontype_t`.

##### Invocation <a id="func.wrap.ref.inv">[[func.wrap.ref.inv]]</a>

``` cpp
R operator()(ArgTypes... args) const noexcept(noex);
```

*Effects:* Equivalent to:
`return `*`thunk-ptr`*`(`*`bound-entity`*`, std::forward<ArgTypes>(args)...);`

##### Deduction guides <a id="func.wrap.ref.deduct">[[func.wrap.ref.deduct]]</a>

``` cpp
template<class F>
  function_ref(F*) -> function_ref<F>;
```

*Constraints:* `is_function_v<F>` is `true`.

``` cpp
template<auto f>
  function_ref(nontype_t<f>) -> function_ref<see below>;
```

Let `F` be `remove_pointer_t<decltype(f)>`.

*Constraints:* `is_function_v<F>` is `true`.

*Remarks:* The deduced type is `function_ref<F>`.

``` cpp
template<auto f, class T>
  function_ref(nontype_t<f>, T&&) -> function_ref<see below>;
```

Let `F` be `decltype(f)`.

*Constraints:*

- `F` is of the form `R(G::*)(A...) cv &ₒₚₜ noexcept(E)` for a type `G`,
  or
- `F` is of the form `M G::*` for a type `G` and an object type `M`, in
  which case let `R` be `invoke_result_t<F, T&>`, `A...` be an empty
  pack, and `E` be `false`, or
- `F` is of the form `R(*)(G, A...) noexcept(E)` for a type `G`.

*Remarks:* The deduced type is `function_ref<R(A...) noexcept(E)>`.

### Searchers <a id="func.search">[[func.search]]</a>

#### General <a id="func.search.general">[[func.search.general]]</a>

Subclause [[func.search]] provides function object types
[[function.objects]] for operations that search for a sequence
\[`pat``first`, `pat_last`) in another sequence \[`first`, `last`) that
is provided to the object’s function call operator. The first sequence
(the pattern to be searched for) is provided to the object’s
constructor, and the second (the sequence to be searched) is provided to
the function call operator.

Each specialization of a class template specified in [[func.search]]
shall meet the *Cpp17CopyConstructible* and *Cpp17CopyAssignable*
requirements. Template parameters named

- `ForwardIterator`,
- `ForwardIterator1`,
- `ForwardIterator2`,
- `RandomAccessIterator`,
- `RandomAccessIterator1`,
- `RandomAccessIterator2`, and
- `BinaryPredicate`

of templates specified in [[func.search]] shall meet the same
requirements and semantics as specified in [[algorithms.general]].
Template parameters named `Hash` shall meet the *Cpp17Hash* requirements
([[cpp17.hash]]).

The Boyer-Moore searcher implements the Boyer-Moore search algorithm.
The Boyer-Moore-Horspool searcher implements the Boyer-Moore-Horspool
search algorithm. In general, the Boyer-Moore searcher will use more
memory and give better runtime performance than Boyer-Moore-Horspool.

#### Class template `default_searcher` <a id="func.search.default">[[func.search.default]]</a>

``` cpp
namespace std {
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
}
```

``` cpp
constexpr default_searcher(ForwardIterator1 pat_first, ForwardIterator1 pat_last,
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
namespace std {
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
}
```

``` cpp
boyer_moore_searcher(RandomAccessIterator1 pat_first,
                     RandomAccessIterator1 pat_last,
                     Hash hf = Hash(),
                     BinaryPredicate pred = BinaryPredicate());
```

*Preconditions:* The value type of `RandomAccessIterator1` meets the
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*, and
*Cpp17CopyAssignable* requirements.

Let `V` be `iterator_traits<RandomAccessIterator1>::value_type`. For any
two values `A` and `B` of type `V`, if `pred(A, B) == true`, then
`hf(A) == hf(B)` is `true`.

*Effects:* Initializes `pat_first_` with `pat_first`, `pat_last_` with
`pat_last`, `hash_` with `hf`, and \texttt{pred\_} with `pred`.

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
namespace std {
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
}
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

Let `V` be `iterator_traits<RandomAccessIterator1>::value_type`. For any
two values `A` and `B` of type `V`, if `pred(A, B) == true`, then
`hf(A) == hf(B)` is `true`.

*Effects:* Initializes `pat_first_` with `pat_first`, `pat_last_` with
`pat_last`, `hash_` with `hf`, and \texttt{pred\_} with `pred`.

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
  *Cpp17CopyAssignable* requirements ([[cpp17.copyassignable]]), the
  *Cpp17Swappable* requirements [[swappable.requirements]],
- meet the requirement that if `k1 == k2` is `true`, `h(k1) == h(k2)` is
  also `true`, where `h` is an object of type `hash<Key>` and `k1` and
  `k2` are objects of type `Key`;
- meet the requirement that the expression `h(k)`, where `h` is an
  object of type `hash<Key>` and `k` is an object of type `Key`, shall
  not throw an exception unless `hash<Key>` is a program-defined
  specialization.

## Bit manipulation <a id="bit">[[bit]]</a>

### General <a id="bit.general">[[bit.general]]</a>

The header `<bit>` provides components to access, manipulate and process
both individual bits and bit sequences.

### Header `<bit>` synopsis <a id="bit.syn">[[bit.syn]]</a>

``` cpp
// all freestanding
namespace std {
  // [bit.cast], bit_cast
  template<class To, class From>
    constexpr To bit_cast(const From& from) noexcept;

  // [bit.byteswap], byteswap
  template<class T>
    constexpr T byteswap(T value) noexcept;

  // [bit.pow.two], integral powers of 2
  template<class T>
    constexpr bool has_single_bit(T x) noexcept;
  template<class T>
    constexpr T bit_ceil(T x);
  template<class T>
    constexpr T bit_floor(T x) noexcept;
  template<class T>
    constexpr int bit_width(T x) noexcept;

  // [bit.rotate], rotating
  template<class T>
    constexpr T rotl(T x, int s) noexcept;
  template<class T>
    constexpr T rotr(T x, int s) noexcept;

  // [bit.count], counting
  template<class T>
    constexpr int countl_zero(T x) noexcept;
  template<class T>
    constexpr int countl_one(T x) noexcept;
  template<class T>
    constexpr int countr_zero(T x) noexcept;
  template<class T>
    constexpr int countr_one(T x) noexcept;
  template<class T>
    constexpr int popcount(T x) noexcept;

  // [bit.endian], endian
  enum class endian {
    little = see below,
    big    = see below,
    native = see below
  };
}
```

### Function template `bit_cast` <a id="bit.cast">[[bit.cast]]</a>

``` cpp
template<class To, class From>
  constexpr To bit_cast(const From& from) noexcept;
```

*Constraints:*

- `sizeof(To) == sizeof(From)` is `true`;
- `is_trivially_copyable_v<To>` is `true`; and
- `is_trivially_copyable_v<From>` is `true`.

*Mandates:* Neither `To` nor `From` are consteval-only
types [[basic.types.general]].

`To`, `From`, and the types of all subobjects of `To` and `From` are
types `T` such that:

- `is_union_v<T>` is `false`;
- `is_pointer_v<T>` is `false`;
- `is_member_pointer_v<T>` is `false`;
- `is_volatile_v<T>` is `false`; and
- `T` has no non-static data members of reference type.

*Returns:* An object of type `To`. Implicitly creates objects nested
within the result [[intro.object]]. Each bit of the value representation
of the result is equal to the corresponding bit in the object
representation of `from`. Padding bits of the result are unspecified.
For the result and each object created within it, if there is no value
of the object’s type corresponding to the value representation produced,
the behavior is undefined. If there are multiple such values, which
value is produced is unspecified. A bit in the value representation of
the result is indeterminate if it does not correspond to a bit in the
value representation of `from` or corresponds to a bit for which the
smallest enclosing object is not within its lifetime or has an
indeterminate value [[basic.indet]]. A bit in the value representation
of the result is erroneous if it corresponds to a bit for which the
smallest enclosing object has an erroneous value. For each bit b in the
value representation of the result that is indeterminate or erroneous,
let u be the smallest object containing that bit enclosing b:

- If u is of unsigned ordinary character type or `std::byte` type, u has
  an indeterminate value if any of the bits in its value representation
  are indeterminate, or otherwise has an erroneous value.
- Otherwise, if b is indeterminate, the behavior is undefined.
- Otherwise, the behavior is erroneous, and the result is as specified
  above.

The result does not otherwise contain any indeterminate or erroneous
values.

### `byteswap` <a id="bit.byteswap">[[bit.byteswap]]</a>

``` cpp
template<class T>
  constexpr T byteswap(T value) noexcept;
```

*Constraints:* `T` models `integral`.

*Mandates:* `T` does not have padding bits [[basic.types.general]].

Let the sequence R comprise the bytes of the object representation of
`value` in reverse order.

*Returns:* An object `v` of type `T` such that each byte in the object
representation of `v` is equal to the byte in the corresponding position
in R.

### Integral powers of 2 <a id="bit.pow.two">[[bit.pow.two]]</a>

``` cpp
template<class T>
  constexpr bool has_single_bit(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* `true` if `x` is an integral power of two; `false` otherwise.

``` cpp
template<class T>
  constexpr T bit_ceil(T x);
```

Let N be the smallest power of 2 greater than or equal to `x`.

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Preconditions:* N is representable as a value of type `T`.

*Returns:* N.

*Throws:* Nothing.

*Remarks:* A function call expression that violates the precondition in
the *Preconditions:* element is not a core constant
expression [[expr.const]].

``` cpp
template<class T>
  constexpr T bit_floor(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* If `x == 0`, `0`; otherwise the maximal value `y` such that
`has_single_bit(y)` is `true` and `y <= x`.

``` cpp
template<class T>
  constexpr int bit_width(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* If `x == 0`, `0`; otherwise one plus the base-2 logarithm of
`x`, with any fractional part discarded.

### Rotating <a id="bit.rotate">[[bit.rotate]]</a>

In the following descriptions, let `N` denote
`numeric_limits<T>::digits`.

``` cpp
template<class T>
  constexpr T rotl(T x, int s) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

Let `r` be `s % N`.

*Returns:* If `r` is `0`, `x`; if `r` is positive,
`(x << r) | (x >> (N - r))`; if `r` is negative, `rotr(x, -r)`.

``` cpp
template<class T>
  constexpr T rotr(T x, int s) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

Let `r` be `s % N`.

*Returns:* If `r` is `0`, `x`; if `r` is positive,
`(x >> r) | (x << (N - r))`; if `r` is negative, `rotl(x, -r)`.

### Counting <a id="bit.count">[[bit.count]]</a>

In the following descriptions, let `N` denote
`numeric_limits<T>::digits`.

``` cpp
template<class T>
  constexpr int countl_zero(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* The number of consecutive `0` bits in the value of `x`,
starting from the most significant bit.

[*Note 1*: Returns `N` if `x == 0`. — *end note*]

``` cpp
template<class T>
  constexpr int countl_one(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* The number of consecutive `1` bits in the value of `x`,
starting from the most significant bit.

[*Note 2*: Returns `N` if
`x == numeric_limits<T>::max()`. — *end note*]

``` cpp
template<class T>
  constexpr int countr_zero(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* The number of consecutive `0` bits in the value of `x`,
starting from the least significant bit.

[*Note 3*: Returns `N` if `x == 0`. — *end note*]

``` cpp
template<class T>
  constexpr int countr_one(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* The number of consecutive `1` bits in the value of `x`,
starting from the least significant bit.

[*Note 4*: Returns `N` if
`x == numeric_limits<T>::max()`. — *end note*]

``` cpp
template<class T>
  constexpr int popcount(T x) noexcept;
```

*Constraints:* `T` is an unsigned integer type [[basic.fundamental]].

*Returns:* The number of `1` bits in the value of `x`.

### Endian <a id="bit.endian">[[bit.endian]]</a>

Two common methods of byte ordering in multibyte scalar types are
big-endian and little-endian in the execution environment. Big-endian is
a format for storage of binary data in which the most significant byte
is placed first, with the rest in descending order. Little-endian is a
format for storage of binary data in which the least significant byte is
placed first, with the rest in ascending order. This subclause describes
the endianness of the scalar types of the execution environment.

``` cpp
enum class endian {
  little = see below,
  big    = see below,
  native = see below
};
```

If all scalar types have size 1 byte, then all of `endian::little`,
`endian::big`, and `endian::native` have the same value. Otherwise,
`endian::little` is not equal to `endian::big`. If all scalar types are
big-endian, `endian::native` is equal to `endian::big`. If all scalar
types are little-endian, `endian::native` is equal to `endian::little`.
Otherwise, `endian::native` is not equal to either `endian::big` or
`endian::little`.

## Header `<stdbit.h>` synopsis <a id="stdbit.h.syn">[[stdbit.h.syn]]</a>

``` cpp
// all freestanding

#define \libmacro{__STDC_VERSION_STDBIT_H__} 202311L

#define \libmacro{__STDC_ENDIAN_BIG__}     see below
#define \libmacro{__STDC_ENDIAN_LITTLE__}  see below
#define \libmacro{__STDC_ENDIAN_NATIVE__}  see below

unsigned int stdc_leading_zeros_uc(unsigned char value);
unsigned int stdc_leading_zeros_us(unsigned short value);
unsigned int stdc_leading_zeros_ui(unsigned int value);
unsigned int stdc_leading_zeros_ul(unsigned long int value);
unsigned int stdc_leading_zeros_ull(unsigned long long int value);
template<class T> see below stdc_leading_zeros(T value);

unsigned int stdc_leading_ones_uc(unsigned char value);
unsigned int stdc_leading_ones_us(unsigned short value);
unsigned int stdc_leading_ones_ui(unsigned int value);
unsigned int stdc_leading_ones_ul(unsigned long int value);
unsigned int stdc_leading_ones_ull(unsigned long long int value);
template<class T> see below stdc_leading_ones(T value);

unsigned int stdc_trailing_zeros_uc(unsigned char value);
unsigned int stdc_trailing_zeros_us(unsigned short value);
unsigned int stdc_trailing_zeros_ui(unsigned int value);
unsigned int stdc_trailing_zeros_ul(unsigned long int value);
unsigned int stdc_trailing_zeros_ull(unsigned long long int value);
template<class T> see below stdc_trailing_zeros(T value);

unsigned int stdc_trailing_ones_uc(unsigned char value);
unsigned int stdc_trailing_ones_us(unsigned short value);
unsigned int stdc_trailing_ones_ui(unsigned int value);
unsigned int stdc_trailing_ones_ul(unsigned long int value);
unsigned int stdc_trailing_ones_ull(unsigned long long int value);
template<class T> see below stdc_trailing_ones(T value);

unsigned int stdc_first_leading_zero_uc(unsigned char value);
unsigned int stdc_first_leading_zero_us(unsigned short value);
unsigned int stdc_first_leading_zero_ui(unsigned int value);
unsigned int stdc_first_leading_zero_ul(unsigned long int value);
unsigned int stdc_first_leading_zero_ull(unsigned long long int value);
template<class T> see below stdc_first_leading_zero(T value);

unsigned int stdc_first_leading_one_uc(unsigned char value);
unsigned int stdc_first_leading_one_us(unsigned short value);
unsigned int stdc_first_leading_one_ui(unsigned int value);
unsigned int stdc_first_leading_one_ul(unsigned long int value);
unsigned int stdc_first_leading_one_ull(unsigned long long int value);
template<class T> see below stdc_first_leading_one(T value);

unsigned int stdc_first_trailing_zero_uc(unsigned char value);
unsigned int stdc_first_trailing_zero_us(unsigned short value);
unsigned int stdc_first_trailing_zero_ui(unsigned int value);
unsigned int stdc_first_trailing_zero_ul(unsigned long int value);
unsigned int stdc_first_trailing_zero_ull(unsigned long long int value);
template<class T> see below stdc_first_trailing_zero(T value);

unsigned int stdc_first_trailing_one_uc(unsigned char value);
unsigned int stdc_first_trailing_one_us(unsigned short value);
unsigned int stdc_first_trailing_one_ui(unsigned int value);
unsigned int stdc_first_trailing_one_ul(unsigned long int value);
unsigned int stdc_first_trailing_one_ull(unsigned long long int value);
template<class T> see below stdc_first_trailing_one(T value);

unsigned int stdc_count_zeros_uc(unsigned char value);
unsigned int stdc_count_zeros_us(unsigned short value);
unsigned int stdc_count_zeros_ui(unsigned int value);
unsigned int stdc_count_zeros_ul(unsigned long int value);
unsigned int stdc_count_zeros_ull(unsigned long long int value);
template<class T> see below stdc_count_zeros(T value);

unsigned int stdc_count_ones_uc(unsigned char value);
unsigned int stdc_count_ones_us(unsigned short value);
unsigned int stdc_count_ones_ui(unsigned int value);
unsigned int stdc_count_ones_ul(unsigned long int value);
unsigned int stdc_count_ones_ull(unsigned long long int value);
template<class T> see below stdc_count_ones(T value);

bool stdc_has_single_bit_uc(unsigned char value);
bool stdc_has_single_bit_us(unsigned short value);
bool stdc_has_single_bit_ui(unsigned int value);
bool stdc_has_single_bit_ul(unsigned long int value);
bool stdc_has_single_bit_ull(unsigned long long int value);
template<class T> bool stdc_has_single_bit(T value);

unsigned int stdc_bit_width_uc(unsigned char value);
unsigned int stdc_bit_width_us(unsigned short value);
unsigned int stdc_bit_width_ui(unsigned int value);
unsigned int stdc_bit_width_ul(unsigned long int value);
unsigned int stdc_bit_width_ull(unsigned long long int value);
template<class T> see below stdc_bit_width(T value);

unsigned char stdc_bit_floor_uc(unsigned char value);
unsigned short stdc_bit_floor_us(unsigned short value);
unsigned int stdc_bit_floor_ui(unsigned int value);
unsigned long int stdc_bit_floor_ul(unsigned long int value);
unsigned long long int stdc_bit_floor_ull(unsigned long long int value);
template<class T> T stdc_bit_floor(T value);

unsigned char stdc_bit_ceil_uc(unsigned char value);
unsigned short stdc_bit_ceil_us(unsigned short value);
unsigned int stdc_bit_ceil_ui(unsigned int value);
unsigned long int stdc_bit_ceil_ul(unsigned long int value);
unsigned long long int stdc_bit_ceil_ull(unsigned long long int value);
template<class T> T stdc_bit_ceil(T value);
```

For a function template whose return type is not specified above, the
return type is an *implementation-defined* unsigned integer type large
enough to represent all possible result values. Each function template
has the same semantics as the corresponding type-generic function with
the same name specified in .

*Mandates:* `T` is an unsigned integer type.

Otherwise, the contents and meaning of the header `<stdbit.h>` are the
same as the C standard library header `<stdbit.h>`.

<!-- Link reference definitions -->
[algorithms]: algorithms.md#algorithms
[algorithms.general]: algorithms.md#algorithms.general
[allocator.requirements.general]: library.md#allocator.requirements.general
[allocator.uses.construction]: mem.md#allocator.uses.construction
[any]: #any
[any.assign]: #any.assign
[any.bad.any.cast]: #any.bad.any.cast
[any.class]: #any.class
[any.class.general]: #any.class.general
[any.cons]: #any.cons
[any.general]: #any.general
[any.modifiers]: #any.modifiers
[any.nonmembers]: #any.nonmembers
[any.observers]: #any.observers
[any.synop]: #any.synop
[arithmetic.operations]: #arithmetic.operations
[arithmetic.operations.divides]: #arithmetic.operations.divides
[arithmetic.operations.general]: #arithmetic.operations.general
[arithmetic.operations.minus]: #arithmetic.operations.minus
[arithmetic.operations.modulus]: #arithmetic.operations.modulus
[arithmetic.operations.multiplies]: #arithmetic.operations.multiplies
[arithmetic.operations.negate]: #arithmetic.operations.negate
[arithmetic.operations.plus]: #arithmetic.operations.plus
[basic.fundamental]: basic.md#basic.fundamental
[basic.indet]: basic.md#basic.indet
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.types.general]: basic.md#basic.types.general
[bit]: #bit
[bit.byteswap]: #bit.byteswap
[bit.cast]: #bit.cast
[bit.count]: #bit.count
[bit.endian]: #bit.endian
[bit.general]: #bit.general
[bit.pow.two]: #bit.pow.two
[bit.rotate]: #bit.rotate
[bit.syn]: #bit.syn
[bitset]: #bitset
[bitset.cons]: #bitset.cons
[bitset.hash]: #bitset.hash
[bitset.members]: #bitset.members
[bitset.operators]: #bitset.operators
[bitset.syn]: #bitset.syn
[bitwise.operations]: #bitwise.operations
[bitwise.operations.and]: #bitwise.operations.and
[bitwise.operations.general]: #bitwise.operations.general
[bitwise.operations.not]: #bitwise.operations.not
[bitwise.operations.or]: #bitwise.operations.or
[bitwise.operations.xor]: #bitwise.operations.xor
[class.base.init]: class.md#class.base.init
[class.copy.ctor]: class.md#class.copy.ctor
[comparisons]: #comparisons
[comparisons.equal.to]: #comparisons.equal.to
[comparisons.general]: #comparisons.general
[comparisons.greater]: #comparisons.greater
[comparisons.greater.equal]: #comparisons.greater.equal
[comparisons.less]: #comparisons.less
[comparisons.less.equal]: #comparisons.less.equal
[comparisons.not.equal.to]: #comparisons.not.equal.to
[comparisons.three.way]: #comparisons.three.way
[concepts.equality]: concepts.md#concepts.equality
[container.reqmts]: containers.md#container.reqmts
[cpp17.copyassignable]: #cpp17.copyassignable
[cpp17.defaultconstructible]: #cpp17.defaultconstructible
[cpp17.destructible]: #cpp17.destructible
[cpp17.hash]: #cpp17.hash
[cpp17.moveassignable]: #cpp17.moveassignable
[cpp17.moveconstructible]: #cpp17.moveconstructible
[dcl.constexpr]: dcl.md#dcl.constexpr
[dcl.init.general]: dcl.md#dcl.init.general
[declval]: #declval
[defns.expression.equivalent]: intro.md#defns.expression.equivalent
[defns.order.ptr]: #defns.order.ptr
[defns.referenceable]: intro.md#defns.referenceable
[expected]: #expected
[expected.bad]: #expected.bad
[expected.bad.void]: #expected.bad.void
[expected.expected]: #expected.expected
[expected.general]: #expected.general
[expected.object.assign]: #expected.object.assign
[expected.object.cons]: #expected.object.cons
[expected.object.dtor]: #expected.object.dtor
[expected.object.eq]: #expected.object.eq
[expected.object.general]: #expected.object.general
[expected.object.monadic]: #expected.object.monadic
[expected.object.obs]: #expected.object.obs
[expected.object.swap]: #expected.object.swap
[expected.syn]: #expected.syn
[expected.un.cons]: #expected.un.cons
[expected.un.eq]: #expected.un.eq
[expected.un.general]: #expected.un.general
[expected.un.obs]: #expected.un.obs
[expected.un.swap]: #expected.un.swap
[expected.unexpected]: #expected.unexpected
[expected.void]: #expected.void
[expected.void.assign]: #expected.void.assign
[expected.void.cons]: #expected.void.cons
[expected.void.dtor]: #expected.void.dtor
[expected.void.eq]: #expected.void.eq
[expected.void.general]: #expected.void.general
[expected.void.monadic]: #expected.void.monadic
[expected.void.obs]: #expected.void.obs
[expected.void.swap]: #expected.void.swap
[expr.add]: expr.md#expr.add
[expr.bit.and]: expr.md#expr.bit.and
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.eq]: expr.md#expr.eq
[expr.log.and]: expr.md#expr.log.and
[expr.log.or]: expr.md#expr.log.or
[expr.mul]: expr.md#expr.mul
[expr.or]: expr.md#expr.or
[expr.rel]: expr.md#expr.rel
[expr.unary.op]: expr.md#expr.unary.op
[expr.xor]: expr.md#expr.xor
[forward]: #forward
[freestanding.item]: library.md#freestanding.item
[func.bind]: #func.bind
[func.bind.bind]: #func.bind.bind
[func.bind.general]: #func.bind.general
[func.bind.isbind]: #func.bind.isbind
[func.bind.isplace]: #func.bind.isplace
[func.bind.partial]: #func.bind.partial
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
[func.search.general]: #func.search.general
[func.wrap]: #func.wrap
[func.wrap.badcall]: #func.wrap.badcall
[func.wrap.copy]: #func.wrap.copy
[func.wrap.copy.class]: #func.wrap.copy.class
[func.wrap.copy.ctor]: #func.wrap.copy.ctor
[func.wrap.copy.general]: #func.wrap.copy.general
[func.wrap.copy.inv]: #func.wrap.copy.inv
[func.wrap.copy.util]: #func.wrap.copy.util
[func.wrap.func]: #func.wrap.func
[func.wrap.func.alg]: #func.wrap.func.alg
[func.wrap.func.cap]: #func.wrap.func.cap
[func.wrap.func.con]: #func.wrap.func.con
[func.wrap.func.general]: #func.wrap.func.general
[func.wrap.func.inv]: #func.wrap.func.inv
[func.wrap.func.mod]: #func.wrap.func.mod
[func.wrap.func.nullptr]: #func.wrap.func.nullptr
[func.wrap.func.targ]: #func.wrap.func.targ
[func.wrap.general]: #func.wrap.general
[func.wrap.move]: #func.wrap.move
[func.wrap.move.class]: #func.wrap.move.class
[func.wrap.move.ctor]: #func.wrap.move.ctor
[func.wrap.move.general]: #func.wrap.move.general
[func.wrap.move.inv]: #func.wrap.move.inv
[func.wrap.move.util]: #func.wrap.move.util
[func.wrap.ref]: #func.wrap.ref
[func.wrap.ref.class]: #func.wrap.ref.class
[func.wrap.ref.ctor]: #func.wrap.ref.ctor
[func.wrap.ref.deduct]: #func.wrap.ref.deduct
[func.wrap.ref.general]: #func.wrap.ref.general
[func.wrap.ref.inv]: #func.wrap.ref.inv
[function.objects]: #function.objects
[function.objects.general]: #function.objects.general
[functional.syn]: #functional.syn
[intro.abstract]: intro.md#intro.abstract
[intro.multithread]: basic.md#intro.multithread
[intro.object]: basic.md#intro.object
[invalid.argument]: diagnostics.md#invalid.argument
[istream.formatted]: input.md#istream.formatted
[iterator.concept.contiguous]: iterators.md#iterator.concept.contiguous
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[lex.ccon]: lex.md#lex.ccon
[logical.operations]: #logical.operations
[logical.operations.and]: #logical.operations.and
[logical.operations.general]: #logical.operations.general
[logical.operations.not]: #logical.operations.not
[logical.operations.or]: #logical.operations.or
[meta.rqmts]: meta.md#meta.rqmts
[meta.trans.other]: meta.md#meta.trans.other
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
[optional.iterators]: #optional.iterators
[optional.mod]: #optional.mod
[optional.monadic]: #optional.monadic
[optional.nullops]: #optional.nullops
[optional.nullopt]: #optional.nullopt
[optional.observe]: #optional.observe
[optional.optional]: #optional.optional
[optional.optional.general]: #optional.optional.general
[optional.optional.ref]: #optional.optional.ref
[optional.optional.ref.general]: #optional.optional.ref.general
[optional.ref.assign]: #optional.ref.assign
[optional.ref.ctor]: #optional.ref.ctor
[optional.ref.expos]: #optional.ref.expos
[optional.ref.iterators]: #optional.ref.iterators
[optional.ref.mod]: #optional.ref.mod
[optional.ref.monadic]: #optional.ref.monadic
[optional.ref.observe]: #optional.ref.observe
[optional.ref.swap]: #optional.ref.swap
[optional.relops]: #optional.relops
[optional.specalg]: #optional.specalg
[optional.swap]: #optional.swap
[optional.syn]: #optional.syn
[ostream.formatted]: input.md#ostream.formatted
[out.of.range]: diagnostics.md#out.of.range
[over.match.call]: over.md#over.match.call
[overflow.error]: diagnostics.md#overflow.error
[pair.astuple]: #pair.astuple
[pair.piecewise]: #pair.piecewise
[pairs]: #pairs
[pairs.general]: #pairs.general
[pairs.pair]: #pairs.pair
[pairs.spec]: #pairs.spec
[random.access.iterators]: iterators.md#random.access.iterators
[range.cmp]: #range.cmp
[range.utility.helpers]: ranges.md#range.utility.helpers
[refwrap]: #refwrap
[refwrap.access]: #refwrap.access
[refwrap.assign]: #refwrap.assign
[refwrap.common.ref]: #refwrap.common.ref
[refwrap.comparisons]: #refwrap.comparisons
[refwrap.const]: #refwrap.const
[refwrap.general]: #refwrap.general
[refwrap.helpers]: #refwrap.helpers
[refwrap.invoke]: #refwrap.invoke
[stdbit.h.syn]: #stdbit.h.syn
[support.signal]: support.md#support.signal
[swappable.requirements]: library.md#swappable.requirements
[temp.constr.atomic]: temp.md#temp.constr.atomic
[temp.point]: temp.md#temp.point
[temp.type]: temp.md#temp.type
[template.bitset]: #template.bitset
[template.bitset.general]: #template.bitset.general
[term.object.representation]: basic.md#term.object.representation
[term.object.type]: basic.md#term.object.type
[term.odr.use]: basic.md#term.odr.use
[term.perfect.forwarding.call.wrapper]: #term.perfect.forwarding.call.wrapper
[term.simple.call.wrapper]: #term.simple.call.wrapper
[term.structural.type]: temp.md#term.structural.type
[term.trivially.copyable.type]: basic.md#term.trivially.copyable.type
[term.unevaluated.operand]: expr.md#term.unevaluated.operand
[tuple]: #tuple
[tuple.apply]: #tuple.apply
[tuple.assign]: #tuple.assign
[tuple.cnstr]: #tuple.cnstr
[tuple.common.ref]: #tuple.common.ref
[tuple.creation]: #tuple.creation
[tuple.elem]: #tuple.elem
[tuple.general]: #tuple.general
[tuple.helper]: #tuple.helper
[tuple.like]: #tuple.like
[tuple.rel]: #tuple.rel
[tuple.special]: #tuple.special
[tuple.swap]: #tuple.swap
[tuple.syn]: #tuple.syn
[tuple.traits]: #tuple.traits
[tuple.tuple]: #tuple.tuple
[tuple.tuple.general]: #tuple.tuple.general
[unord]: containers.md#unord
[unord.hash]: #unord.hash
[utilities]: #utilities
[utilities.general]: #utilities.general
[utilities.summary]: #utilities.summary
[utility]: #utility
[utility.as.const]: #utility.as.const
[utility.exchange]: #utility.exchange
[utility.intcmp]: #utility.intcmp
[utility.swap]: #utility.swap
[utility.syn]: #utility.syn
[utility.undefined]: #utility.undefined
[utility.underlying]: #utility.underlying
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
[variant.variant.general]: #variant.variant.general
[variant.visit]: #variant.visit

[^1]: Such a type is a function pointer or a class type which has a
    member `operator()` or a class type which has a conversion to a
    pointer to function.
