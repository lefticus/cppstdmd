# Ranges library <a id="ranges">[[ranges]]</a>

## General <a id="ranges.general">[[ranges.general]]</a>

This clause describes components for dealing with ranges of elements.

The following subclauses describe range and view requirements, and
components for range primitives as summarized in [[range.summary]].

**Table: Ranges library summary**

| Subclause           |                 | Header     |
| ------------------- | --------------- | ---------- |
| [[range.access]]    | Range access    | `<ranges>` |
| [[range.req]]       | Requirements    |            |
| [[range.utility]]   | Range utilities |            |
| [[range.factories]] | Range factories |            |
| [[range.adaptors]]  | Range adaptors  |            |


## Header `<ranges>` synopsis <a id="ranges.syn">[[ranges.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]
#include <iterator>             // see [iterator.synopsis]

namespace std::ranges {
  inline namespace unspecified {
    // [range.access], range access
    inline constexpr unspecified begin = unspecified;
    inline constexpr unspecified end = unspecified;
    inline constexpr unspecified cbegin = unspecified;
    inline constexpr unspecified cend = unspecified;
    inline constexpr unspecified rbegin = unspecified;
    inline constexpr unspecified rend = unspecified;
    inline constexpr unspecified crbegin = unspecified;
    inline constexpr unspecified crend = unspecified;

    inline constexpr unspecified size = unspecified;
    inline constexpr unspecified ssize = unspecified;
    inline constexpr unspecified empty = unspecified;
    inline constexpr unspecified data = unspecified;
    inline constexpr unspecified cdata = unspecified;
  }

  // [range.range], ranges
  template<class T>
    concept range = see below;

  template<class T>
    inline constexpr bool enable_borrowed_range = false;

  template<class T>
    concept borrowed_range = see below;

  template<class T>
    using iterator_t = decltype(ranges::begin(declval<T&>()));
  template<range R>
    using sentinel_t = decltype(ranges::end(declval<R&>()));
  template<range R>
    using range_difference_t = iter_difference_t<iterator_t<R>>;
  template<sized_range R>
    using range_size_t = decltype(ranges::size(declval<R&>()));
  template<range R>
    using range_value_t = iter_value_t<iterator_t<R>>;
  template<range R>
    using range_reference_t = iter_reference_t<iterator_t<R>>;
  template<range R>
    using range_rvalue_reference_t = iter_rvalue_reference_t<iterator_t<R>>;

  // [range.sized], sized ranges
  template<class>
    inline constexpr bool disable_sized_range = false;

  template<class T>
    concept sized_range = see below;

  // [range.view], views
  template<class T>
    inline constexpr bool enable_view = see below;

  struct view_base { };

  template<class T>
    concept view = see below;

  // [range.refinements], other range refinements
  template<class R, class T>
    concept output_range = see below;

  template<class T>
    concept input_range = see below;

  template<class T>
    concept forward_range = see below;

  template<class T>
    concept bidirectional_range = see below;

  template<class T>
    concept random_access_range = see below;

  template<class T>
    concept contiguous_range = see below;

  template<class T>
    concept common_range = see below;

  template<class T>
    concept viewable_range = see below;

  // [view.interface], class template view_interface
  template<class D>
    requires is_class_v<D> && same_as<D, remove_cv_t<D>>
  class view_interface;

  // [range.subrange], sub-ranges
  enum class subrange_kind : bool { unsized, sized };

  template<input_or_output_iterator I, sentinel_for<I> S = I, subrange_kind K = see below>
    requires (K == subrange_kind::sized || !sized_sentinel_for<S, I>)
  class subrange;

  template<input_or_output_iterator I, sentinel_for<I> S, subrange_kind K>
    inline constexpr bool enable_borrowed_range<subrange<I, S, K>> = true;

  // [range.dangling], dangling iterator handling
  struct dangling;

  template<range R>
    using borrowed_iterator_t = conditional_t<borrowed_range<R>, iterator_t<R>, dangling>;

  template<range R>
    using borrowed_subrange_t =
      conditional_t<borrowed_range<R>, subrange<iterator_t<R>>, dangling>;

  // [range.empty], empty view
  template<class T>
    requires is_object_v<T>
  class empty_view;

  template<class T>
    inline constexpr bool enable_borrowed_range<empty_view<T>> = true;

  namespace views {
    template<class T>
      inline constexpr empty_view<T> empty{};
  }

  // [range.single], single view
  template<copy_constructible T>
    requires is_object_v<T>
  class single_view;

  namespace views { inline constexpr unspecified single = unspecified; }

  // [range.iota], iota view
  template<weakly_incrementable W, semiregular Bound = unreachable_sentinel_t>
    requires weakly-equality-comparable-with<W, Bound>
  class iota_view;

  template<weakly_incrementable W, semiregular Bound>
    inline constexpr bool enable_borrowed_range<iota_view<W, Bound>> = true;

  namespace views { inline constexpr unspecified iota = unspecified; }

  // [range.istream], istream view
  template<movable Val, class CharT, class Traits = char_traits<CharT>>
    requires see below
  class basic_istream_view;
  template<class Val, class CharT, class Traits>
    basic_istream_view<Val, CharT, Traits> istream_view(basic_istream<CharT, Traits>& s);

  // [range.all], all view
  namespace views {
    inline constexpr unspecified all = unspecified;

    template<viewable_range R>
      using all_t = decltype(all(declval<R>()));
  }

  template<range R>
    requires is_object_v<R>
  class ref_view;

  template<class T>
    inline constexpr bool enable_borrowed_range<ref_view<T>> = true;

  // [range.filter], filter view
  template<input_range V, indirect_unary_predicate<iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class filter_view;

  namespace views { inline constexpr unspecified filter = unspecified; }

  // [range.transform], transform view
  template<input_range V, copy_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>>
  class transform_view;

  namespace views { inline constexpr unspecified transform = unspecified; }

  // [range.take], take view
  template<view> class take_view;

  namespace views { inline constexpr unspecified take = unspecified; }

  // [range.take.while], take while view
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
    class take_while_view;

  namespace views { inline constexpr unspecified take_while = unspecified; }

  // [range.drop], drop view
  template<view V>
    class drop_view;

  namespace views { inline constexpr unspecified drop = unspecified; }

  // [range.drop.while], drop while view
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
    class drop_while_view;

  namespace views { inline constexpr unspecified drop_while = unspecified; }

  // [range.join], join view
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>> &&
             (is_reference_v<range_reference_t<V>> ||
              view<range_value_t<V>>)
  class join_view;

  namespace views { inline constexpr unspecified join = unspecified; }

  // [range.split], split view
  template<class R>
    concept tiny-range = see below;   // exposition only

  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  class split_view;

  namespace views { inline constexpr unspecified split = unspecified; }

  // [range.counted], counted view
  namespace views { inline constexpr unspecified counted = unspecified; }

  // [range.common], common view
  template<view V>
    requires (!common_range<V> && copyable<iterator_t<V>>)
  class common_view;

  namespace views { inline constexpr unspecified common = unspecified; }

  // [range.reverse], reverse view
  template<view V>
    requires bidirectional_range<V>
  class reverse_view;

  namespace views { inline constexpr unspecified reverse = unspecified; }

  // [range.elements], elements view
  template<input_range V, size_t N>
    requires see below;
  class elements_view;

  template<class R>
    using keys_view = elements_view<views::all_t<R>, 0>;
  template<class R>
    using values_view = elements_view<views::all_t<R>, 1>;

  namespace views {
    template<size_t N>
      inline constexpr unspecified elements = unspecified ;
    inline constexpr auto keys = elements<0>;
    inline constexpr auto values = elements<1>;
  }
}

namespace std {
  namespace views = ranges::views;

  template<class I, class S, ranges::subrange_kind K>
  struct tuple_size<ranges::subrange<I, S, K>>
    : integral_constant<size_t, 2> {};
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<0, ranges::subrange<I, S, K>> {
    using type = I;
  };
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<1, ranges::subrange<I, S, K>> {
    using type = S;
  };
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<0, const ranges::subrange<I, S, K>> {
    using type = I;
  };
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<1, const ranges::subrange<I, S, K>> {
    using type = S;
  };
}
```

Within this clause, for an integer-like type `X`
[[iterator.concept.winc]], `make-unsigned-like-t<X>` denotes
`make_unsigned_t<X>` if `X` is an integer type; otherwise, it denotes a
corresponding unspecified unsigned-integer-like type of the same width
as `X`. For an expression `x` of type `X`, `to-unsigned-like(x)` is `x`
explicitly converted to `make-unsigned-like-t<X>`.

## Range access <a id="range.access">[[range.access]]</a>

In addition to being available via inclusion of the `<ranges>` header,
the customization point objects in [[range.access]] are available when
`<iterator>` is included.

Within this subclause, the *reified object* of a subexpression `E`
denotes

- the same object as `E` if `E` is a glvalue, or
- the result of applying the temporary materialization conversion
  [[conv.rval]] to `E` otherwise.

### `ranges::begin` <a id="range.access.begin">[[range.access.begin]]</a>

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::begin(E)` is ill-formed.
- Otherwise, if `T` is an array type [[basic.compound]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::begin(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `T` is an array type, `ranges::begin(E)` is
  expression-equivalent to `t + 0`.
- Otherwise, if `decay-copy(t.begin())` is a valid expression whose type
  models `input_or_output_iterator`, `ranges::begin(E)` is
  expression-equivalent to `decay-copy(t.begin())`.
- Otherwise, if `T` is a class or enumeration type and
  `decay-copy(begin(t))` is a valid expression whose type models
  `input_or_output_iterator` with overload resolution performed in a
  context in which unqualified lookup for `begin` finds only the
  declarations
  ``` cpp
  void begin(auto&) = delete;
  void begin(const auto&) = delete;
  ```

  then `ranges::begin(E)` is expression-equivalent to
  `decay-copy(begin(t))` with overload resolution performed in the above
  context.
- Otherwise, `ranges::begin(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::begin(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::begin(E)` is a valid expression, its type
models `input_or_output_iterator`. — *end note*\]

### `ranges::end` <a id="range.access.end">[[range.access.end]]</a>

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::end(E)` is ill-formed.
- Otherwise, if `T` is an array type [[basic.compound]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::end(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `T` is an array of unknown bound, `ranges::end(E)` is
  ill-formed.
- Otherwise, if `T` is an array, `ranges::end(E)` is
  expression-equivalent to `t + extent_v<T>`.
- Otherwise, if `decay-copy(t.end())` is a valid expression whose type
  models `sentinel_for<iterator_t<T>>` then `ranges::end(E)` is
  expression-equivalent to `decay-copy(t.end())`.
- Otherwise, if `T` is a class or enumeration type and
  `decay-copy(end(t))` is a valid expression whose type models
  `sentinel_for<iterator_t<T>>` with overload resolution performed in a
  context in which unqualified lookup for `end` finds only the
  declarations
  ``` cpp
  void end(auto&) = delete;
  void end(const auto&) = delete;
  ```

  then `ranges::end(E)` is expression-equivalent to `decay-copy(end(t))`
  with overload resolution performed in the above context.
- Otherwise, `ranges::end(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::end(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::end(E)` is a valid expression, the types
`S` and `I` of `ranges::end(E)` and `ranges::begin(E)` model
`sentinel_for<S, I>`. — *end note*\]

### `ranges::cbegin` <a id="range.access.cbegin">[[range.access.cbegin]]</a>

- `ranges::begin(static_cast<const T&>(E))` if `E` is an lvalue.
- Otherwise, `ranges::begin(static_cast<const T&&>(E))`.

[*Note 1*: Whenever `ranges::cbegin(E)` is a valid expression, its type
models `input_or_output_iterator`. — *end note*\]

### `ranges::cend` <a id="range.access.cend">[[range.access.cend]]</a>

- `ranges::end(static_cast<const T&>(E))` if `E` is an lvalue.
- Otherwise, `ranges::end(static_cast<const T&&>(E))`.

[*Note 1*: Whenever `ranges::cend(E)` is a valid expression, the types
`S` and `I` of `ranges::cend(E)` and `ranges::cbegin(E)` model
`sentinel_for<S, I>`. — *end note*\]

### `ranges::rbegin` <a id="range.access.rbegin">[[range.access.rbegin]]</a>

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::rbegin(E)` is ill-formed.
- Otherwise, if `T` is an array type [[basic.compound]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::rbegin(E)`
  is ill-formed with no diagnostic required.
- Otherwise, if `decay-copy(t.rbegin())` is a valid expression whose
  type models `input_or_output_iterator`, `ranges::rbegin(E)` is
  expression-equivalent to `decay-copy(t.rbegin())`.
- Otherwise, if `T` is a class or enumeration type and
  `decay-copy(rbegin(t))` is a valid expression whose type models
  `input_or_output_iterator` with overload resolution performed in a
  context in which unqualified lookup for `rbegin` finds only the
  declarations
  ``` cpp
  void rbegin(auto&) = delete;
  void rbegin(const auto&) = delete;
  ```

  then `ranges::rbegin(E)` is expression-equivalent to
  `decay-copy(rbegin(t))` with overload resolution performed in the
  above context.
- Otherwise, if both `ranges::begin(t)` and `ranges::end(t)` are valid
  expressions of the same type which models `bidirectional_iterator`
  [[iterator.concept.bidir]], `ranges::rbegin(E)` is
  expression-equivalent to `make_reverse_iterator(ranges::end(t))`.
- Otherwise, `ranges::rbegin(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::rbegin(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::rbegin(E)` is a valid expression, its type
models `input_or_output_iterator`. — *end note*\]

### `ranges::rend` <a id="range.access.rend">[[range.access.rend]]</a>

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::rend(E)` is ill-formed.
- Otherwise, if `T` is an array type [[basic.compound]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::rend(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `decay-copy(t.rend())` is a valid expression whose type
  models `sentinel_for<decltype(ranges::rbegin(E))>` then
  `ranges::rend(E)` is expression-equivalent to
  `decay-copy(t.rend({}))`.
- Otherwise, if `T` is a class or enumeration type and
  `decay-copy(rend(t))` is a valid expression whose type models
  `sentinel_for<decltype(ranges::rbegin(E))>` with overload resolution
  performed in a context in which unqualified lookup for `rend` finds
  only the declarations
  ``` cpp
  void rend(auto&) = delete;
  void rend(const auto&) = delete;
  ```

  then `ranges::rend(E)` is expression-equivalent to
  `decay-copy(rend(t))` with overload resolution performed in the above
  context.
- Otherwise, if both `ranges::begin(t)` and `ranges::end(t)` are valid
  expressions of the same type which models `bidirectional_iterator`
  [[iterator.concept.bidir]], then `ranges::rend(E)` is
  expression-equivalent to `make_reverse_iterator(ranges::begin(t))`.
- Otherwise, `ranges::rend(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::rend(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::rend(E)` is a valid expression, the types
`S` and `I` of `ranges::rend(E)` and `ranges::rbegin(E)` model
`sentinel_for<S, I>`. — *end note*\]

### `ranges::crbegin` <a id="range.access.crbegin">[[range.access.crbegin]]</a>

- `ranges::{}rbegin(static_cast<const T&>(E))` if `E` is an lvalue.
- Otherwise, `ranges::rbegin(static_cast<const T&&>(E))`.

[*Note 1*: Whenever `ranges::crbegin(E)` is a valid expression, its
type models `input_or_output_iterator`. — *end note*\]

### `ranges::crend` <a id="range.access.crend">[[range.access.crend]]</a>

- `ranges::rend(static_cast<const T&>(E))` if `E` is an lvalue.
- Otherwise, `ranges::rend(static_cast<const T&&>(E))`.

[*Note 1*: Whenever `ranges::crend(E)` is a valid expression, the types
`S` and `I` of `ranges::crend(E)` and `ranges::crbegin(E)` model
`sentinel_for<S, I>`. — *end note*\]

### `ranges::size` <a id="range.prim.size">[[range.prim.size]]</a>

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `T` is an array of unknown bound [[dcl.array]], `ranges::size(E)`
  is ill-formed.
- Otherwise, if `T` is an array type, `ranges::size(E)` is
  expression-equivalent to `decay-copy(extent_v<T>)`.
- Otherwise, if `disable_sized_range<remove_cv_t<T>>` [[range.sized]] is
  `false` and `decay-copy(t.size())` is a valid expression of
  integer-like type [[iterator.concept.winc]], `ranges::size(E)` is
  expression-equivalent to `decay-copy(t.size())`.
- Otherwise, if `T` is a class or enumeration type,
  `disable_sized_range<remove_cv_t<T>>` is `false` and
  `decay-copy(size(t))` is a valid expression of integer-like type with
  overload resolution performed in a context in which unqualified lookup
  for `size` finds only the declarations
  ``` cpp
  void size(auto&) = delete;
  void size(const auto&) = delete;
  ```

  then `ranges::size(E)` is expression-equivalent to
  `decay-copy(size(t))` with overload resolution performed in the above
  context.
- Otherwise, if `to-unsigned-like(ranges::end(t) - ranges::begin(t))`
  [[ranges.syn]] is a valid expression and the types `I` and `S` of
  `ranges::begin(t)` and `ranges::end(t)` (respectively) model both
  `sized_sentinel_for<S, I>` [[iterator.concept.sizedsentinel]] and
  `forward_iterator<I>`, then `ranges::size(E)` is expression-equivalent
  to `to-unsigned-like(ranges::end(t) - ranges::begin(t))`.
- Otherwise, `ranges::size(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::size(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::size(E)` is a valid expression, its type
is integer-like. — *end note*\]

### `ranges::ssize` <a id="range.prim.ssize">[[range.prim.ssize]]</a>

The name `ranges::ssize` denotes a customization point object
[[customization.point.object]]. The expression `ranges::ssize({}E)` for
a subexpression `E` of type `T` is expression-equivalent to:

- If `range_difference_t<T>` has width less than `ptrdiff_t`,
  `static_cast<ptrdiff_t>(ranges::{}size(E))`.
- Otherwise, `static_cast<range_difference_t<T>>(ranges::size(E))`.

### `ranges::empty` <a id="range.prim.empty">[[range.prim.empty]]</a>

Given a subexpression `ranges::empty(E)` with type `T`, let `t` be an
lvalue that denotes the reified object for `E`. Then:

- If `T` is an array of unknown bound [[basic.compound]],
  `ranges::empty(E)` is ill-formed.
- Otherwise, if `bool(t.empty())` is a valid expression,
  `ranges::empty(E)` is expression-equivalent to `bool(t.empty())`.
- Otherwise, if `(ranges::size(t) == 0)` is a valid expression,
  `ranges::empty(E)` is expression-equivalent to
  `(ranges::size(t) == 0)`.
- Otherwise, if `bool(ranges::begin(t) == ranges::end(t))` is a valid
  expression and the type of `ranges::begin(t)` models
  `forward_iterator`, `ranges::empty(E)` is expression-equivalent to
  `bool({}ranges::begin(t) == ranges::end(t))`.
- Otherwise, `ranges::empty(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::empty(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::empty(E)` is a valid expression, it has
type `bool`. — *end note*\]

### `ranges::data` <a id="range.prim.data">[[range.prim.data]]</a>

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::data(E)` is ill-formed.
- Otherwise, if `T` is an array type [[basic.compound]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::data(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `decay-copy(t.data())` is a valid expression of pointer
  to object type, `ranges::data(E)` is expression-equivalent to
  `decay-copy(t.data())`.
- Otherwise, if `ranges::begin(t)` is a valid expression whose type
  models `contiguous_iterator`, `ranges::data(E)` is
  expression-equivalent to `to_address(ranges::begin(E))`.
- Otherwise, `ranges::data(E)` is ill-formed.

[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::data(E)` appears in the immediate context of a
template instantiation. — *end note*\]

[*Note 2*: Whenever `ranges::data(E)` is a valid expression, it has
pointer to object type. — *end note*\]

### `ranges::cdata` <a id="range.prim.cdata">[[range.prim.cdata]]</a>

- `ranges::data(static_cast<const T&>(E))` if `E` is an lvalue.
- Otherwise, `ranges::data(static_cast<const T&&>(E))`.

[*Note 1*: Whenever `ranges::cdata(E)` is a valid expression, it has
pointer to object type. — *end note*\]

## Range requirements <a id="range.req">[[range.req]]</a>

### General <a id="range.req.general">[[range.req.general]]</a>

Ranges are an abstraction that allow a C++ program to operate on
elements of data structures uniformly. Calling `ranges::begin` on a
range returns an object whose type models `input_or_output_iterator`
[[iterator.concept.iterator]]. Calling `ranges::end` on a range returns
an object whose type `S`, together with the type `I` of the object
returned by `ranges::begin`, models `sentinel_for<S, I>`. The library
formalizes the interfaces, semantics, and complexity of ranges to enable
algorithms and range adaptors that work efficiently on different types
of sequences.

The `range` concept requires that `ranges::begin` and `ranges::end`
return an iterator and a sentinel, respectively. The `sized_range`
concept refines `range` with the requirement that `ranges::size` be
amortized . The `view` concept specifies requirements on a `range` type
with constant-time destruction and move operations.

Several refinements of `range` group requirements that arise frequently
in concepts and algorithms. Common ranges are ranges for which
`ranges::begin` and `ranges::end` return objects of the same type.
Random access ranges are ranges for which `ranges::begin` returns a type
that models `random_access_iterator` [[iterator.concept.random.access]].
(Contiguous, bidirectional, forward, input, and output ranges are
defined similarly.) Viewable ranges can be converted to views.

### Ranges <a id="range.range">[[range.range]]</a>

The `range` concept defines the requirements of a type that allows
iteration over its elements by providing an iterator and sentinel that
denote the elements of the range.

``` cpp
template<class T>
  concept range =
    requires(T& t) {
      ranges::begin(t);                         // sometimes equality-preserving (see below)
      ranges::end(t);
    };
```

The required expressions `ranges::begin(t)` and `ranges::end(t)` of the
`range` concept do not require implicit expression
variations [[concepts.equality]].

Given an expression `t` such that `decltype((t))` is `T&`, `T` models
`range` only if

- \[`ranges::begin(t)`, `ranges::end(t)`) denotes a
  range [[iterator.requirements.general]],
- both `ranges::begin(t)` and `ranges::end(t)` are amortized constant
  time and non-modifying, and
- if the type of `ranges::begin(t)` models `forward_iterator`,
  `ranges::begin(t)` is equality-preserving.

[*Note 1*: Equality preservation of both `ranges::begin` and
`ranges::end` enables passing a `range` whose iterator type models
`forward_iterator` to multiple algorithms and making multiple passes
over the range by repeated calls to `ranges::begin` and `ranges::end`.
Since `ranges::begin` is not required to be equality-preserving when the
return type does not model `forward_iterator`, repeated calls might not
return equal values or might not be well-defined; `ranges::begin` should
be called at most once for such a range. — *end note*\]

``` cpp
template<class T>
  concept borrowed_range =
    range<T> &&
      (is_lvalue_reference_v<T> || enable_borrowed_range<remove_cvref_t<T>>);
```

Given an expression `E` such that `decltype((E))` is `T`, `T` models
`borrowed_range` only if the validity of iterators obtained from the
object denoted by `E` is not tied to the lifetime of that object.

[*Note 2*: Since the validity of iterators is not tied to the lifetime
of an object whose type models `borrowed_range`, a function can accept
arguments of such a type by value and return iterators obtained from it
without danger of dangling. — *end note*\]

``` cpp
template<class>
  inline constexpr bool enable_borrowed_range = false;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`enable_borrowed_range` for cv-unqualified program-defined types. Such
specializations shall be usable in constant expressions [[expr.const]]
and have type `const bool`.

[*Example 1*:

Each specialization `S` of class template `subrange`[[range.subrange]]
models `borrowed_range` because

- `enable_borrowed_range<S>` is specialized to have the value `true`,
  and
- `S`’s iterators do not have validity tied to the lifetime of an `S`
  object because they are “borrowed” from some other range.

— *end example*\]

### Sized ranges <a id="range.sized">[[range.sized]]</a>

The `sized_range` concept refines `range` with the requirement that the
number of elements in the range can be determined in amortized constant
time using `ranges::size`.

``` cpp
template<class T>
  concept sized_range =
    range<T> &&
    requires(T& t) { ranges::size(t); };
```

Given an lvalue `t` of type `remove_reference_t<T>`, `T` models
`sized_range` only if

- `ranges::size(t)` is amortized 𝑂(1), does not modify `t`, and is equal
  to `ranges::distance(t)`, and
- if `iterator_t<T>` models `forward_iterator`, `ranges::size(t)` is
  well-defined regardless of the evaluation of `ranges::begin(t)`.
  \[*Note 1*: `ranges::size(t)` is otherwise not required to be
  well-defined after evaluating `ranges::begin(t)`. For example,
  `ranges::size(t)` might be well-defined for a `sized_range` whose
  iterator type does not model `forward_iterator` only if evaluated
  before the first call to `ranges::begin(t)`. — *end note*\]

``` cpp
template<class>
  inline constexpr bool disable_sized_range = false;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`disable_sized_range` for cv-unqualified program-defined types. Such
specializations shall be usable in constant expressions [[expr.const]]
and have type `const bool`.

[*Note 1*: `disable_sized_range` allows use of range types with the
library that satisfy but do not in fact model
`sized_range`. — *end note*\]

### Views <a id="range.view">[[range.view]]</a>

The `view` concept specifies the requirements of a `range` type that has
constant time move construction, move assignment, and destruction; that
is, the cost of these operations is independent of the number of
elements in the `view`.

``` cpp
template<class T>
  concept view =
    range<T> && movable<T> && default_initializable<T> && enable_view<T>;
```

`T` models `view` only if:

- `T` has 𝑂(1) move construction; and
- `T` has 𝑂(1) move assignment; and
- `T` has 𝑂(1) destruction; and
- `copy_constructible<T>` is `false`, or `T` has 𝑂(1) copy construction;
  and
- `copyable<T>` is `false`, or `T` has 𝑂(1) copy assignment.

[*Example 1*:

Examples of `view`s are:

- A `range` type that wraps a pair of iterators.
- A `range` type that holds its elements by `shared_ptr` and shares
  ownership with all its copies.
- A `range` type that generates its elements on demand.

Most containers [[containers]] are not views since destruction of the
container destroys the elements, which cannot be done in constant time.

— *end example*\]

Since the difference between `range` and `view` is largely semantic, the
two are differentiated with the help of `enable_view`.

``` cpp
template<class T>
  inline constexpr bool enable_view = derived_from<T, view_base>;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`enable_view` to `true` for cv-unqualified program-defined types which
model `view`, and `false` for types which do not. Such specializations
shall be usable in constant expressions [[expr.const]] and have type
`const bool`.

### Other range refinements <a id="range.refinements">[[range.refinements]]</a>

The `output_range` concept specifies requirements of a `range` type for
which `ranges::begin` returns a model of `output_iterator`
[[iterator.concept.output]]. `input_range`, `forward_range`,
`bidirectional_range`, and `random_access_range` are defined similarly.

``` cpp
template<class R, class T>
  concept output_range =
    range<R> && output_iterator<iterator_t<R>, T>;

template<class T>
  concept input_range =
    range<T> && input_iterator<iterator_t<T>>;

template<class T>
  concept forward_range =
    input_range<T> && forward_iterator<iterator_t<T>>;

template<class T>
  concept bidirectional_range =
    forward_range<T> && bidirectional_iterator<iterator_t<T>>;

template<class T>
  concept random_access_range =
    bidirectional_range<T> && random_access_iterator<iterator_t<T>>;
```

`contiguous_range` additionally requires that the `ranges::data`
customization point [[range.prim.data]] is usable with the range.

``` cpp
template<class T>
  concept contiguous_range =
    random_access_range<T> && contiguous_iterator<iterator_t<T>> &&
    requires(T& t) {
      { ranges::data(t) } -> same_as<add_pointer_t<range_reference_t<T>>>;
    };
```

Given an expression `t` such that `decltype((t))` is `T&`, `T` models
`contiguous_range` only if
`to_address({}ranges::begin(t)) == ranges::data(t)` is `true`.

The `common_range` concept specifies requirements of a `range` type for
which `ranges::begin` and `ranges::end` return objects of the same type.

[*Example 1*: The standard containers [[containers]] model
`common_range`. — *end example*\]

``` cpp
template<class T>
  concept common_range =
    range<T> && same_as<iterator_t<T>, sentinel_t<T>>;
```

The `viewable_range` concept specifies the requirements of a `range`
type that can be converted to a `view` safely.

``` cpp
template<class T>
  concept viewable_range =
    range<T> && (borrowed_range<T> || view<remove_cvref_t<T>>);
```

## Range utilities <a id="range.utility">[[range.utility]]</a>

The components in this subclause are general utilities for representing
and manipulating ranges.

### Helper concepts <a id="range.utility.helpers">[[range.utility.helpers]]</a>

Many of the types in subclause  [[range.utility]] are specified in terms
of the following exposition-only concepts:

``` cpp
template<class R>
  concept simple-view =                         // exposition only
    view<R> && range<const R> &&
    same_as<iterator_t<R>, iterator_t<const R>> &&
    same_as<sentinel_t<R>, sentinel_t<const R>>;

template<class I>
  concept has-arrow =                           // exposition only
    input_iterator<I> && (is_pointer_v<I> || requires(I i) { i.operator->(); });

template<class T, class U>
  concept not-same-as =                         // exposition only
    !same_as<remove_cvref_t<T>, remove_cvref_t<U>>;
```

### View interface <a id="view.interface">[[view.interface]]</a>

The class template `view_interface` is a helper for defining `view`-like
types that offer a container-like interface. It is parameterized with
the type that is derived from it.

``` cpp
namespace std::ranges {
  template<class D>
    requires is_class_v<D> && same_as<D, remove_cv_t<D>>
  class view_interface : public view_base {
  private:
    constexpr D& derived() noexcept {                   // exposition only
      return static_cast<D&>(*this);
    }
    constexpr const D& derived() const noexcept {       // exposition only
      return static_cast<const D&>(*this);
    }
  public:
    constexpr bool empty() requires forward_range<D> {
      return ranges::begin(derived()) == ranges::end(derived());
    }
    constexpr bool empty() const requires forward_range<const D> {
      return ranges::begin(derived()) == ranges::end(derived());
    }

    constexpr explicit operator bool()
      requires requires { ranges::empty(derived()); } {
        return !ranges::empty(derived());
      }
    constexpr explicit operator bool() const
      requires requires { ranges::empty(derived()); } {
        return !ranges::empty(derived());
      }

    constexpr auto data() requires contiguous_iterator<iterator_t<D>> {
      return to_address(ranges::begin(derived()));
    }
    constexpr auto data() const
      requires range<const D> && contiguous_iterator<iterator_t<const D>> {
        return to_address(ranges::begin(derived()));
      }

    constexpr auto size() requires forward_range<D> &&
      sized_sentinel_for<sentinel_t<D>, iterator_t<D>> {
        return ranges::end(derived()) - ranges::begin(derived());
      }
    constexpr auto size() const requires forward_range<const D> &&
      sized_sentinel_for<sentinel_t<const D>, iterator_t<const D>> {
        return ranges::end(derived()) - ranges::begin(derived());
      }

    constexpr decltype(auto) front() requires forward_range<D>;
    constexpr decltype(auto) front() const requires forward_range<const D>;

    constexpr decltype(auto) back() requires bidirectional_range<D> && common_range<D>;
    constexpr decltype(auto) back() const
      requires bidirectional_range<const D> && common_range<const D>;

    template<random_access_range R = D>
      constexpr decltype(auto) operator[](range_difference_t<R> n) {
        return ranges::begin(derived())[n];
      }
    template<random_access_range R = const D>
      constexpr decltype(auto) operator[](range_difference_t<R> n) const {
        return ranges::begin(derived())[n];
      }
  };
}
```

The template parameter `D` for `view_interface` may be an incomplete
type. Before any member of the resulting specialization of
`view_interface` other than special member functions is referenced, `D`
shall be complete, and model both `derived_from<view_interface<D>>` and
`view`.

#### Members <a id="view.interface.members">[[view.interface.members]]</a>

``` cpp
constexpr decltype(auto) front() requires forward_range<D>;
constexpr decltype(auto) front() const requires forward_range<const D>;
```

*Preconditions:* `!empty()`.

*Effects:* Equivalent to: `return *ranges::begin(`*`derived`*`());`

``` cpp
constexpr decltype(auto) back() requires bidirectional_range<D> && common_range<D>;
constexpr decltype(auto) back() const
  requires bidirectional_range<const D> && common_range<const D>;
```

*Preconditions:* `!empty()`.

*Effects:* Equivalent to:
`return *ranges::prev(ranges::end(`*`derived`*`()));`

### Sub-ranges <a id="range.subrange">[[range.subrange]]</a>

The `subrange` class template combines together an iterator and a
sentinel into a single object that models the `view` concept.
Additionally, it models the `sized_range` concept when the final
template parameter is `subrange_kind::sized`.

``` cpp
namespace std::ranges {
  template<class From, class To>
    concept convertible-to-non-slicing =                    // exposition only
      convertible_to<From, To> &&
      !(is_pointer_v<decay_t<From>> &&
        is_pointer_v<decay_t<To>> &&
        not-same-as<remove_pointer_t<decay_t<From>>, remove_pointer_t<decay_t<To>>>);

  template<class T>
    concept pair-like =                                     // exposition only
      !is_reference_v<T> && requires(T t) {
        typename tuple_size<T>::type;                       // ensures tuple_size<T> is complete
        requires derived_from<tuple_size<T>, integral_constant<size_t, 2>>;
        typename tuple_element_t<0, remove_const_t<T>>;
        typename tuple_element_t<1, remove_const_t<T>>;
        { get<0>(t) } -> convertible_to<const tuple_element_t<0, T>&>;
        { get<1>(t) } -> convertible_to<const tuple_element_t<1, T>&>;
      };

  template<class T, class U, class V>
    concept pair-like-convertible-from =                    // exposition only
      !range<T> && pair-like<T> &&
      constructible_from<T, U, V> &&
      convertible-to-non-slicing<U, tuple_element_t<0, T>> &&
      convertible_to<V, tuple_element_t<1, T>>;

  template<class T>
    concept iterator-sentinel-pair =                        // exposition only
      !range<T> && pair-like<T> &&
      sentinel_for<tuple_element_t<1, T>, tuple_element_t<0, T>>;

  template<input_or_output_iterator I, sentinel_for<I> S = I, subrange_kind K =
      sized_sentinel_for<S, I> ? subrange_kind::sized : subrange_kind::unsized>
    requires (K == subrange_kind::sized || !sized_sentinel_for<S, I>)
  class subrange : public view_interface<subrange<I, S, K>> {
  private:
    static constexpr bool StoreSize =                           // exposition only
      K == subrange_kind::sized && !sized_sentinel_for<S, I>;
    I begin_ = I();                                             // exposition only
    S end_ = S();                                               // exposition only
    make-unsigned-like-t<iter_difference_t<I>> size_ = 0;       // exposition only; present only
                                                                // when StoreSize is true
  public:
    subrange() = default;

    constexpr subrange(convertible-to-non-slicing<I> auto i, S s) requires (!StoreSize);

    constexpr subrange(convertible-to-non-slicing<I> auto i, S s,
                       make-unsigned-like-t<iter_difference_t<I>> n)
      requires (K == subrange_kind::sized);

    template<not-same-as<subrange> R>
      requires borrowed_range<R> &&
               convertible-to-non-slicing<iterator_t<R>, I> &&
               convertible_to<sentinel_t<R>, S>
    constexpr subrange(R&& r) requires (!StoreSize || sized_range<R>);

    template<borrowed_range R>
      requires convertible-to-non-slicing<iterator_t<R>, I> &&
               convertible_to<sentinel_t<R>, S>
    constexpr subrange(R&& r, make-unsigned-like-t<iter_difference_t<I>> n)
      requires (K == subrange_kind::sized)
        : subrange{ranges::begin(r), ranges::end(r), n}
    {}

    template<not-same-as<subrange> PairLike>
      requires pair-like-convertible-from<PairLike, const I&, const S&>
    constexpr operator PairLike() const;

    constexpr I begin() const requires copyable<I>;
    [[nodiscard]] constexpr I begin() requires (!copyable<I>);
    constexpr S end() const;

    constexpr bool empty() const;
    constexpr make-unsigned-like-t<iter_difference_t<I>> size() const
      requires (K == subrange_kind::sized);

    [[nodiscard]] constexpr subrange next(iter_difference_t<I> n = 1) const &
      requires forward_iterator<I>;
    [[nodiscard]] constexpr subrange next(iter_difference_t<I> n = 1) &&;
    [[nodiscard]] constexpr subrange prev(iter_difference_t<I> n = 1) const
      requires bidirectional_iterator<I>;
    constexpr subrange& advance(iter_difference_t<I> n);
  };

  template<input_or_output_iterator I, sentinel_for<I> S>
    subrange(I, S) -> subrange<I, S>;

  template<input_or_output_iterator I, sentinel_for<I> S>
    subrange(I, S, make-unsigned-like-t<iter_difference_t<I>>) ->
      subrange<I, S, subrange_kind::sized>;

  template<iterator-sentinel-pair P>
    subrange(P) -> subrange<tuple_element_t<0, P>, tuple_element_t<1, P>>;

  template<iterator-sentinel-pair P>
    subrange(P, make-unsigned-like-t<iter_difference_t<tuple_element_t<0, P>>>) ->
      subrange<tuple_element_t<0, P>, tuple_element_t<1, P>, subrange_kind::sized>;

  template<borrowed_range R>
    subrange(R&&) ->
      subrange<iterator_t<R>, sentinel_t<R>,
               (sized_range<R> || sized_sentinel_for<sentinel_t<R>, iterator_t<R>>)
                 ? subrange_kind::sized : subrange_kind::unsized>;

  template<borrowed_range R>
    subrange(R&&, make-unsigned-like-t<range_difference_t<R>>) ->
      subrange<iterator_t<R>, sentinel_t<R>, subrange_kind::sized>;

  template<size_t N, class I, class S, subrange_kind K>
    requires (N < 2)
    constexpr auto get(const subrange<I, S, K>& r);

  template<size_t N, class I, class S, subrange_kind K>
    requires (N < 2)
    constexpr auto get(subrange<I, S, K>&& r);
}

namespace std {
  using ranges::get;
}
```

#### Constructors and conversions <a id="range.subrange.ctor">[[range.subrange.ctor]]</a>

``` cpp
constexpr subrange(convertible-to-non-slicing<I> auto i, S s) requires (!StoreSize);
```

*Preconditions:* \[`i`, `s`) is a valid range.

*Effects:* Initializes *begin\_* with `std::move(i)` and *end\_* with
`s`.

``` cpp
constexpr subrange(convertible-to-non-slicing<I> auto i, S s,
                   make-unsigned-like-t<iter_difference_t<I>> n)
  requires (K == subrange_kind::sized);
```

*Preconditions:* \[`i`, `s`) is a valid range, and
`n == `*`to-unsigned-like`*`(ranges::distance(i, s))`.

*Effects:* Initializes *begin\_* with `std::move(i)` and *end\_* with
`s`. If *StoreSize* is `true`, initializes *size\_* with `n`.

[*Note 1*: Accepting the length of the range and storing it to later
return from `size()` enables `subrange` to model `sized_range` even when
it stores an iterator and sentinel that do not model
`sized_sentinel_for`. — *end note*\]

``` cpp
template<not-same-as<subrange> R>
  requires borrowed_range<R> &&
           convertible-to-non-slicing<iterator_t<R>, I> &&
           convertible_to<sentinel_t<R>, S>
constexpr subrange(R&& r) requires (!StoreSize || sized_range<R>);
```

*Effects:* Equivalent to:

- If *StoreSize* is `true`, `subrange{r, ranges::size(r)}`.
- Otherwise, `subrange{ranges::begin(r), ranges::end(r)}`.

*PairLike*

``` cpp
template<not-same-as<subrange> PairLike>
  requires pair-like-convertible-from<PairLike, const I&, const S&>
constexpr operator PairLike() const;
```

*Effects:* Equivalent to: `return PairLike(`*`begin_`*`, `*`end_`*`);`

#### Accessors <a id="range.subrange.access">[[range.subrange.access]]</a>

``` cpp
constexpr I begin() const requires copyable<I>;
```

*Effects:* Equivalent to: `return `*`begin_`*`;`

``` cpp
[[nodiscard]] constexpr I begin() requires (!copyable<I>);
```

*Effects:* Equivalent to: `return std::move(`*`begin_`*`);`

``` cpp
constexpr S end() const;
```

*Effects:* Equivalent to: `return `*`end_`*`;`

``` cpp
constexpr bool empty() const;
```

*Effects:* Equivalent to: `return `*`begin_`*` == `*`end_`*`;`

``` cpp
constexpr make-unsigned-like-t<iter_difference_t<I>> size() const
  requires (K == subrange_kind::sized);
```

*Effects:*

- If *StoreSize* is `true`, equivalent to: `return `*`size_`*`;`
- Otherwise, equivalent to:
  `return `*`to-unsigned-like`*`(`*`end_`*` - `*`begin_`*`);`

``` cpp
[[nodiscard]] constexpr subrange next(iter_difference_t<I> n = 1) const &
  requires forward_iterator<I>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
tmp.advance(n);
return tmp;
```

``` cpp
[[nodiscard]] constexpr subrange next(iter_difference_t<I> n = 1) &&;
```

*Effects:* Equivalent to:

``` cpp
advance(n);
return std::move(*this);
```

``` cpp
[[nodiscard]] constexpr subrange prev(iter_difference_t<I> n = 1) const
  requires bidirectional_iterator<I>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
tmp.advance(-n);
return tmp;
```

``` cpp
constexpr subrange& advance(iter_difference_t<I> n);
```

*Effects:* Equivalent to:

- If *StoreSize* is `true`,
  ``` cpp
  auto d = n - ranges::advance(begin_, n, end_);
  if (d >= 0)
    size_ -= to-unsigned-like(d);
  else
    size_ += to-unsigned-like(-d);
  return *this;
  ```
- Otherwise,
  ``` cpp
  ranges::advance(begin_, n, end_);
  return *this;
  ```

``` cpp
template<size_t N, class I, class S, subrange_kind K>
  requires (N < 2)
  constexpr auto get(const subrange<I, S, K>& r);
template<size_t N, class I, class S, subrange_kind K>
  requires (N < 2)
  constexpr auto get(subrange<I, S, K>&& r);
```

*Effects:* Equivalent to:

``` cpp
if constexpr (N == 0)
  return r.begin();
else
  return r.end();
```

### Dangling iterator handling <a id="range.dangling">[[range.dangling]]</a>

The tag type `dangling` is used together with the template aliases
`borrowed_iterator_t` and `borrowed_subrange_t` to indicate that an
algorithm that typically returns an iterator into or subrange of a
`range` argument does not return an iterator or subrange which could
potentially reference a range whose lifetime has ended for a particular
rvalue `range` argument which does not model `borrowed_range`
[[range.range]].

``` cpp
namespace std::ranges {
  struct dangling {
    constexpr dangling() noexcept = default;
    template<class... Args>
      constexpr dangling(Args&&...) noexcept { }
  };
}
```

[*Example 1*:

``` cpp
vector<int> f();
auto result1 = ranges::find(f(), 42);                                   // #1
static_assert(same_as<decltype(result1), ranges::dangling>);
auto vec = f();
auto result2 = ranges::find(vec, 42);                                   // #2
static_assert(same_as<decltype(result2), vector<int>::iterator>);
auto result3 = ranges::find(subrange{vec}, 42);                         // #3
static_assert(same_as<decltype(result3), vector<int>::iterator>);
```

The call to `ranges::find` at \#1 returns `ranges::dangling` since `f()`
is an rvalue `vector`; the `vector` could potentially be destroyed
before a returned iterator is dereferenced. However, the calls at \#2
and \#3 both return iterators since the lvalue `vec` and specializations
of `subrange` model `borrowed_range`.

— *end example*\]

## Range factories <a id="range.factories">[[range.factories]]</a>

This subclause defines *range factories*, which are utilities to create
a `view`.

Range factories are declared in namespace `std::ranges::views`.

### Empty view <a id="range.empty">[[range.empty]]</a>

#### Overview <a id="range.empty.overview">[[range.empty.overview]]</a>

`empty_view` produces a `view` of no elements of a particular type.

[*Example 1*:

``` cpp
empty_view<int> e;
static_assert(ranges::empty(e));
static_assert(0 == e.size());
```

— *end example*\]

#### Class template `empty_view` <a id="range.empty.view">[[range.empty.view]]</a>

``` cpp
namespace std::ranges {
  template<class T>
    requires is_object_v<T>
  class empty_view : public view_interface<empty_view<T>> {
  public:
    static constexpr T* begin() noexcept { return nullptr; }
    static constexpr T* end() noexcept { return nullptr; }
    static constexpr T* data() noexcept { return nullptr; }
    static constexpr size_t size() noexcept { return 0; }
    static constexpr bool empty() noexcept { return true; }
  };
}
```

### Single view <a id="range.single">[[range.single]]</a>

#### Overview <a id="range.single.overview">[[range.single.overview]]</a>

`single_view` produces a `view` that contains exactly one element of a
specified value.

The name `views::single` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E`, the
expression `views::single(E)` is expression-equivalent to
`single_view{E}`.

[*Example 1*:

``` cpp
single_view s{4};
for (int i : s)
  cout << i;        // prints 4
```

— *end example*\]

#### Class template `single_view` <a id="range.single.view">[[range.single.view]]</a>

``` cpp
namespace std::ranges {
  template<copy_constructible T>
    requires is_object_v<T>
  class single_view : public view_interface<single_view<T>> {
  private:
    semiregular-box<T> value_;      // exposition only{} (see [range.semi.wrap])
  public:
    single_view() = default;
    constexpr explicit single_view(const T& t);
    constexpr explicit single_view(T&& t);
    template<class... Args>
      requires constructible_from<T, Args...>
    constexpr single_view(in_place_t, Args&&... args);

    constexpr T* begin() noexcept;
    constexpr const T* begin() const noexcept;
    constexpr T* end() noexcept;
    constexpr const T* end() const noexcept;
    static constexpr size_t size() noexcept;
    constexpr T* data() noexcept;
    constexpr const T* data() const noexcept;
  };
}
```

``` cpp
constexpr explicit single_view(const T& t);
```

*Effects:* Initializes *value\_* with `t`.

``` cpp
constexpr explicit single_view(T&& t);
```

*Effects:* Initializes *value\_* with `std::move(t)`.

``` cpp
template<class... Args>
constexpr single_view(in_place_t, Args&&... args);
```

*Effects:* Initializes *value\_* as if by
*`value_`*`{in_place, std::forward<Args>(args)...}`.

``` cpp
constexpr T* begin() noexcept;
constexpr const T* begin() const noexcept;
```

*Effects:* Equivalent to: `return data();`

``` cpp
constexpr T* end() noexcept;
constexpr const T* end() const noexcept;
```

*Effects:* Equivalent to: `return data() + 1;`

``` cpp
static constexpr size_t size() noexcept;
```

*Effects:* Equivalent to: `return 1;`

``` cpp
constexpr T* data() noexcept;
constexpr const T* data() const noexcept;
```

*Effects:* Equivalent to: `return `*`value_`*`.operator->();`

### Iota view <a id="range.iota">[[range.iota]]</a>

#### Overview <a id="range.iota.overview">[[range.iota.overview]]</a>

`iota_view` generates a sequence of elements by repeatedly incrementing
an initial value.

The name `views::iota` denotes a customization point object
[[customization.point.object]]. Given subexpressions `E` and `F`, the
expressions `views::iota(E)` and `views::iota(E, F)` are
expression-equivalent to `iota_view{E}` and `iota_view{E, F}`,
respectively.

[*Example 1*:

``` cpp
for (int i : iota_view{1, 10})
  cout << i << ' '; // prints: 1 2 3 4 5 6 7 8 9
```

— *end example*\]

#### Class template `iota_view` <a id="range.iota.view">[[range.iota.view]]</a>

``` cpp
namespace std::ranges {
  template<class I>
    concept decrementable =     // exposition only
      see below;
  template<class I>
    concept advanceable =       // exposition only
      see below;

  template<weakly_incrementable W, semiregular Bound = unreachable_sentinel_t>
    requires weakly-equality-comparable-with<W, Bound> && semiregular<W>
  class iota_view : public view_interface<iota_view<W, Bound>> {
  private:
    // [range.iota.iterator], class iota_view::iterator
    struct iterator;            // exposition only
    // [range.iota.sentinel], class iota_view::sentinel
    struct sentinel;            // exposition only
    W value_ = W();             // exposition only
    Bound bound_ = Bound();     // exposition only
  public:
    iota_view() = default;
    constexpr explicit iota_view(W value);
    constexpr iota_view(type_identity_t<W> value,
                        type_identity_t<Bound> bound);
    constexpr iota_view(iterator first, sentinel last) : iota_view(*first, last.bound_) {}

    constexpr iterator begin() const;
    constexpr auto end() const;
    constexpr iterator end() const requires same_as<W, Bound>;

    constexpr auto size() const requires see below;
  };

  template<class W, class Bound>
    requires (!is-integer-like<W> || !is-integer-like<Bound> ||
              (is-signed-integer-like<W> == is-signed-integer-like<Bound>))
    iota_view(W, Bound) -> iota_view<W, Bound>;
}
```

Let `IOTA-DIFF-T(W)` be defined as follows:

- If `W` is not an integral type, or if it is an integral type and
  `sizeof(iter_difference_t<W>)` is greater than `sizeof(W)`, then
  `IOTA-DIFF-T(W)` denotes `iter_difference_t<W>`.
- Otherwise, `IOTA-DIFF-T(W)` is a signed integer type of width greater
  than the width of `W` if such a type exists.
- Otherwise, `IOTA-DIFF-T(W)` is an unspecified signed-integer-like type
  [[iterator.concept.winc]] of width not less than the width of `W`.
  \[*Note 2*: It is unspecified whether this type satisfies
  `weakly_incrementable`. — *end note*\]

The exposition-only *decrementable* concept is equivalent to:

``` cpp
template<class I>
  concept decrementable =
    incrementable<I> && requires(I i) {
      { --i } -> same_as<I&>;
      { i-- } -> same_as<I>;
    };
```

When an object is in the domain of both pre- and post-decrement, the
object is said to be *decrementable*.

Let `a` and `b` be equal objects of type `I`. `I` models `decrementable`
only if

- If `a` and `b` are decrementable, then the following are all true:
  - `addressof(–a) == addressof(a)`
  - `bool(a– == b)`
  - `bool(((void)a–, a) == –b)`
  - `bool(++(–a) == b)`.
- If `a` and `b` are incrementable, then `bool(–(++a) == b)`.

The exposition-only *advanceable* concept is equivalent to:

``` cpp
template<class I>
  concept advanceable =
    decrementable<I> && totally_ordered<I> &&
    requires(I i, const I j, const IOTA-DIFF-T(I) n) {
      { i += n } -> same_as<I&>;
      { i -= n } -> same_as<I&>;
      I(j + n);
      I(n + j);
      I(j - n);
      { j - j } -> convertible_to<IOTA-DIFF-T(I)>;
    };
```

Let `D` be `IOTA-DIFF-T(I)`. Let `a` and `b` be objects of type `I` such
that `b` is reachable from `a` after `n` applications of `++a`, for some
value `n` of type `D`. `I` models `advanceable` only if

- `(a += n)` is equal to `b`.
- `addressof(a += n)` is equal to `addressof(a)`.
- `I(a + n)` is equal to `(a += n)`.
- For any two positive values `x` and `y` of type `D`, if
  `I(a + D(x + y))` is well-defined, then `I(a + D(x + y))` is equal to
  `I(I(a + x) + y)`.
- `I(a + D(0))` is equal to `a`.
- If `I(a + D(n - 1))` is well-defined, then `I(a + n)` is equal to
  `[](I c) { return ++c; }(I(a + D(n - 1)))`.
- `(b += -n)` is equal to `a`.
- `(b -= n)` is equal to `a`.
- `addressof(b -= n)` is equal to `addressof(b)`.
- `I(b - n)` is equal to `(b -= n)`.
- `D(b - a)` is equal to `n`.
- `D(a - b)` is equal to `D(-n)`.
- `bool(a <= b)` is `true`.

``` cpp
constexpr explicit iota_view(W value);
```

*Preconditions:* `Bound` denotes `unreachable_sentinel_t` or `Bound()`
is reachable from `value`.

*Effects:* Initializes *value\_* with `value`.

``` cpp
constexpr iota_view(type_identity_t<W> value, type_identity_t<Bound> bound);
```

*Preconditions:* `Bound` denotes `unreachable_sentinel_t` or `bound` is
reachable from `value`. When `W` and `Bound` model
`totally_ordered_with`, then `bool(value <= bound)` is `true`.

*Effects:* Initializes *value\_* with `value` and *bound\_* with
`bound`.

``` cpp
constexpr iterator begin() const;
```

*Effects:* Equivalent to: `return iterator{`*`value_`*`};`

``` cpp
constexpr auto end() const;
```

*Effects:* Equivalent to:

``` cpp
if constexpr (same_as<Bound, unreachable_sentinel_t>)
  return unreachable_sentinel;
else
  return sentinel{bound_};
```

``` cpp
constexpr iterator end() const requires same_as<W, Bound>;
```

*Effects:* Equivalent to: `return iterator{bound_};`

``` cpp
constexpr auto size() const requires see below;
```

*Effects:* Equivalent to:

``` cpp
if constexpr (is-integer-like<W> && is-integer-like<Bound>)
  return (value_ < 0)
    ? ((bound_ < 0)
      ? to-unsigned-like(-value_) - to-unsigned-like(-bound_)
      : to-unsigned-like(bound_) + to-unsigned-like(-value_))
    : to-unsigned-like(bound_) - to-unsigned-like(value_);
else
  return to-unsigned-like(bound_ - value_);
```

*Remarks:* The expression in the *requires-clause* is equivalent to

``` cpp
(same_as<W, Bound> && advanceable<W>) || (integral<W> && integral<Bound>) ||
  sized_sentinel_for<Bound, W>
```

#### Class `iota_view::iterator` <a id="range.iota.iterator">[[range.iota.iterator]]</a>

``` cpp
namespace std::ranges {
  template<weakly_incrementable W, semiregular Bound>
    requires weakly-equality-comparable-with<W, Bound>
  struct iota_view<W, Bound>::iterator {
  private:
    W value_ = W();             // exposition only
  public:
    using iterator_concept = see below;
    using iterator_category = input_iterator_tag;
    using value_type = W;
    using difference_type = IOTA-DIFF-T(W);

    iterator() = default;
    constexpr explicit iterator(W value);

    constexpr W operator*() const noexcept(is_nothrow_copy_constructible_v<W>);

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires incrementable<W>;

    constexpr iterator& operator--() requires decrementable<W>;
    constexpr iterator operator--(int) requires decrementable<W>;

    constexpr iterator& operator+=(difference_type n)
      requires advanceable<W>;
    constexpr iterator& operator-=(difference_type n)
      requires advanceable<W>;
    constexpr W operator[](difference_type n) const
      requires advanceable<W>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<W>;

    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires totally_ordered<W>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires totally_ordered<W>;
    friend constexpr bool operator<=(const iterator& x, const iterator& y)
      requires totally_ordered<W>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires totally_ordered<W>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires totally_ordered<W> && three_way_comparable<W>;

    friend constexpr iterator operator+(iterator i, difference_type n)
      requires advanceable<W>;
    friend constexpr iterator operator+(difference_type n, iterator i)
      requires advanceable<W>;

    friend constexpr iterator operator-(iterator i, difference_type n)
      requires advanceable<W>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires advanceable<W>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If `W` models `advanceable`, then `iterator_concept` is
  `random_access_iterator_tag`.
- Otherwise, if `W` models `decrementable`, then `iterator_concept` is
  `bidirectional_iterator_tag`.
- Otherwise, if `W` models `incrementable`, then `iterator_concept` is
  `forward_iterator_tag`.
- Otherwise, `iterator_concept` is `input_iterator_tag`.

[*Note 1*: Overloads for `iter_move` and `iter_swap` are omitted
intentionally. — *end note*\]

``` cpp
constexpr explicit iterator(W value);
```

*Effects:* Initializes *value\_* with `value`.

``` cpp
constexpr W operator*() const noexcept(is_nothrow_copy_constructible_v<W>);
```

*Effects:* Equivalent to: `return `*`value_`*`;`

[*Note 1*: The `noexcept` clause is needed by the default `iter_move`
implementation. — *end note*\]

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++value_;
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
constexpr iterator operator++(int) requires incrementable<W>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--() requires decrementable<W>;
```

*Effects:* Equivalent to:

``` cpp
--value_;
return *this;
```

``` cpp
constexpr iterator operator--(int) requires decrementable<W>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
constexpr iterator& operator+=(difference_type n)
  requires advanceable<W>;
```

*Effects:* Equivalent to:

``` cpp
if constexpr (is-integer-like<W> && !is-signed-integer-like<W>) {
  if (n >= difference_type(0))
    value_ += static_cast<W>(n);
  else
    value_ -= static_cast<W>(-n);
} else {
  value_ += n;
}
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type n)
  requires advanceable<W>;
```

*Effects:* Equivalent to:

``` cpp
if constexpr (is-integer-like<W> && !is-signed-integer-like<W>) {
  if (n >= difference_type(0))
    value_ -= static_cast<W>(n);
  else
    value_ += static_cast<W>(-n);
} else {
  value_ -= n;
}
return *this;
```

``` cpp
constexpr W operator[](difference_type n) const
  requires advanceable<W>;
```

*Effects:* Equivalent to: `return W(`*`value_`*` + n);`

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires equality_comparable<W>;
```

*Effects:* Equivalent to: `return x.`*`value_`*` == y.`*`value_`*`;`

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires totally_ordered<W>;
```

*Effects:* Equivalent to: `return x.`*`value_`*` < y.`*`value_`*`;`

``` cpp
friend constexpr bool operator>(const iterator& x, const iterator& y)
  requires totally_ordered<W>;
```

*Effects:* Equivalent to: `return y < x;`

``` cpp
friend constexpr bool operator<=(const iterator& x, const iterator& y)
  requires totally_ordered<W>;
```

*Effects:* Equivalent to: `return !(y < x);`

``` cpp
friend constexpr bool operator>=(const iterator& x, const iterator& y)
  requires totally_ordered<W>;
```

*Effects:* Equivalent to: `return !(x < y);`

``` cpp
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires totally_ordered<W> && three_way_comparable<W>;
```

*Effects:* Equivalent to: `return x.`*`value_`*` <=> y.`*`value_`*`;`

``` cpp
friend constexpr iterator operator+(iterator i, difference_type n)
  requires advanceable<W>;
```

*Effects:* Equivalent to: `return i += n;`

``` cpp
friend constexpr iterator operator+(difference_type n, iterator i)
  requires advanceable<W>;
```

*Effects:* Equivalent to: `return i + n;`

``` cpp
friend constexpr iterator operator-(iterator i, difference_type n)
  requires advanceable<W>;
```

*Effects:* Equivalent to: `return i -= n;`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires advanceable<W>;
```

*Effects:* Equivalent to:

``` cpp
using D = difference_type;
if constexpr (is-integer-like<W>) {
  if constexpr (is-signed-integer-like<W>)
    return D(D(x.value_) - D(y.value_));
  else
    return (y.value_ > x.value_)
      ? D(-D(y.value_ - x.value_))
      : D(x.value_ - y.value_);
} else {
  return x.value_ - y.value_;
}
```

#### Class `iota_view::sentinel` <a id="range.iota.sentinel">[[range.iota.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<weakly_incrementable W, semiregular Bound>
    requires weakly-equality-comparable-with<W, Bound>
  struct iota_view<W, Bound>::sentinel {
  private:
    Bound bound_ = Bound();     // exposition only
  public:
    sentinel() = default;
    constexpr explicit sentinel(Bound bound);

    friend constexpr bool operator==(const iterator& x, const sentinel& y);

    friend constexpr iter_difference_t<W> operator-(const iterator& x, const sentinel& y)
      requires sized_sentinel_for<Bound, W>;
    friend constexpr iter_difference_t<W> operator-(const sentinel& x, const iterator& y)
      requires sized_sentinel_for<Bound, W>;
  };
}
```

``` cpp
constexpr explicit sentinel(Bound bound);
```

*Effects:* Initializes *bound\_* with `bound`.

``` cpp
friend constexpr bool operator==(const iterator& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`value_`*` == y.`*`bound_`*`;`

``` cpp
friend constexpr iter_difference_t<W> operator-(const iterator& x, const sentinel& y)
  requires sized_sentinel_for<Bound, W>;
```

*Effects:* Equivalent to: `return x.`*`value_`*` - y.`*`bound_`*`;`

``` cpp
friend constexpr iter_difference_t<W> operator-(const sentinel& x, const iterator& y)
  requires sized_sentinel_for<Bound, W>;
```

*Effects:* Equivalent to: `return -(y - x);`

### Istream view <a id="range.istream">[[range.istream]]</a>

#### Overview <a id="range.istream.overview">[[range.istream.overview]]</a>

`basic_istream_view` models `input_range` and reads (using `operator>>`)
successive elements from its corresponding input stream.

[*Example 1*:

``` cpp
auto ints = istringstream{"0 1  2   3     4"};
ranges::copy(istream_view<int>(ints), ostream_iterator<int>{cout, "-"});
// prints 0-1-2-3-4-
```

— *end example*\]

#### Class template `basic_istream_view` <a id="range.istream.view">[[range.istream.view]]</a>

``` cpp
namespace std::ranges {
  template<class Val, class CharT, class Traits>
    concept stream-extractable =                // exposition only
      requires(basic_istream<CharT, Traits>& is, Val& t) {
         is >> t;
      };

  template<movable Val, class CharT, class Traits>
    requires default_initializable<Val> &&
             stream-extractable<Val, CharT, Traits>
  class basic_istream_view : public view_interface<basic_istream_view<Val, CharT, Traits>> {
  public:
    basic_istream_view() = default;
    constexpr explicit basic_istream_view(basic_istream<CharT, Traits>& stream);

    constexpr auto begin()
    {
      if (stream_) {
        *stream_ >> object_;
      }
      return iterator{*this};
    }

    constexpr default_sentinel_t end() const noexcept;

  private:
    struct iterator;                                    // exposition only
    basic_istream<CharT, Traits>* stream_ = nullptr;    // exposition only
    Val object_ = Val();                                // exposition only
  };
}
```

``` cpp
constexpr explicit basic_istream_view(basic_istream<CharT, Traits>& stream);
```

*Effects:* Initializes *stream\_* with `addressof(stream)`.

``` cpp
constexpr default_sentinel_t end() const noexcept;
```

*Effects:* Equivalent to: `return default_sentinel;`

``` cpp
template<class Val, class CharT, class Traits>
basic_istream_view<Val, CharT, Traits> istream_view(basic_istream<CharT, Traits>& s);
```

*Effects:* Equivalent to:
`return basic_istream_view<Val, CharT, Traits>{s};`

#### Class template `basic_istream_view::iterator` <a id="range.istream.iterator">[[range.istream.iterator]]</a>

``` cpp
namespace std::ranges {
  template<movable Val, class CharT, class Traits>
    requires default_initializable<Val> &&
             stream-extractable<Val, CharT, Traits>
  class basic_istream_view<Val, CharT, Traits>::iterator {      // exposition only
  public:
    using iterator_concept = input_iterator_tag;
    using difference_type = ptrdiff_t;
    using value_type = Val;

    iterator() = default;
    constexpr explicit iterator(basic_istream_view& parent) noexcept;

    iterator(const iterator&) = delete;
    iterator(iterator&&) = default;

    iterator& operator=(const iterator&) = delete;
    iterator& operator=(iterator&&) = default;

    iterator& operator++();
    void operator++(int);

    Val& operator*() const;

    friend bool operator==(const iterator& x, default_sentinel_t);

  private:
    basic_istream_view* parent_ = nullptr;                      // exposition only
  };
}
```

``` cpp
constexpr explicit iterator(basic_istream_view& parent) noexcept;
```

*Effects:* Initializes *parent\_* with `addressof(parent)`.

``` cpp
iterator& operator++();
```

*Preconditions:* *`parent_`*`->`*`stream_`*` != nullptr` is `true`.

*Effects:* Equivalent to:

``` cpp
*parent_->stream_>> parent_->object_;
return *this;
```

``` cpp
void operator++(int);
```

*Preconditions:* *`parent_`*`->`*`stream_`*` != nullptr` is `true`.

*Effects:* Equivalent to `++*this`.

``` cpp
Val& operator*() const;
```

*Preconditions:* *`parent_`*`->`*`stream_`*` != nullptr` is `true`.

*Effects:* Equivalent to: `return `*`parent_`*`->`*`object_`*`;`

``` cpp
friend bool operator==(const iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to:
`return x.`*`parent_`*` == nullptr || !*x.`*`parent_`*`->`*`stream_`*`;`

## Range adaptors <a id="range.adaptors">[[range.adaptors]]</a>

This subclause defines *range adaptors*, which are utilities that
transform a `range` into a `view` with custom behaviors. These adaptors
can be chained to create pipelines of range transformations that
evaluate lazily as the resulting view is iterated.

Range adaptors are declared in namespace `std::ranges::views`.

The bitwise operator is overloaded for the purpose of creating adaptor
chain pipelines. The adaptors also support function call syntax with
equivalent semantics.

[*Example 1*:

``` cpp
vector<int> ints{0,1,2,3,4,5};
auto even = [](int i){ return 0 == i % 2; };
auto square = [](int i) { return i * i; };
for (int i : ints | views::filter(even) | views::transform(square)) {
  cout << i << ' '; // prints: 0 4 16
}
assert(ranges::equal(ints | views::filter(even), views::filter(ints, even)));
```

— *end example*\]

### Range adaptor objects <a id="range.adaptor.object">[[range.adaptor.object]]</a>

A *range adaptor closure object* is a unary function object that accepts
a `viewable_range` argument and returns a `view`. For a range adaptor
closure object `C` and an expression `R` such that `decltype((R))`
models `viewable_range`, the following expressions are equivalent and
yield a `view`:

``` cpp
C(R)
R | C
```

Given an additional range adaptor closure object `D`, the expression
`C | D` is well-formed and produces another range adaptor closure object
such that the following two expressions are equivalent:

``` cpp
R | C | D
R | (C | D)
```

A *range adaptor object* is a customization point object
[[customization.point.object]] that accepts a `viewable_range` as its
first argument and returns a `view`.

If a range adaptor object accepts only one argument, then it is a range
adaptor closure object.

If a range adaptor object accepts more than one argument, then the
following expressions are equivalent:

``` cpp
adaptor(range, args...)
adaptor(args...)(range)
range | adaptor(args...)
```

In this case, `adaptor(args...)` is a range adaptor closure object.

### Semiregular wrapper <a id="range.semi.wrap">[[range.semi.wrap]]</a>

Many types in this subclause are specified in terms of an
exposition-only class template *semiregular-box*. `semiregular-box<T>`
behaves exactly like `optional<T>` with the following differences:

- `semiregular-box<T>` constrains its type parameter `T` with
  `copy_constructible<T> && is_object_v<T>`.
- If `T` models `default_initializable`, the default constructor of
  `semiregular-box<T>` is equivalent to:
  ``` cpp
  constexpr semiregular-box() noexcept(is_nothrow_default_constructible_v<T>)
    : semiregular-box{in_place}
  { }
  ```
- If `assignable_from<T&, const T&>` is not modeled, the copy assignment
  operator is equivalent to:
  ``` cpp
  semiregular-box& operator=(const semiregular-box& that)
    noexcept(is_nothrow_copy_constructible_v<T>)
  {
    if (that) emplace(*that);
    else reset();
    return *this;
  }
  ```
- If `assignable_from<T&, T>` is not modeled, the move assignment
  operator is equivalent to:
  ``` cpp
  semiregular-box& operator=(semiregular-box&& that)
    noexcept(is_nothrow_move_constructible_v<T>)
  {
    if (that) emplace(std::move(*that));
    else reset();
    return *this;
  }
  ```

### All view <a id="range.all">[[range.all]]</a>

`views::all` returns a `view` that includes all elements of its `range`
argument.

The name `views::all` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::all(E)` is expression-equivalent to:

- `decay-copy(E)` if the decayed type of `E` models `view`.
- Otherwise, `ref_view{E}` if that expression is well-formed.
- Otherwise, `subrange{E}`.

#### Class template `ref_view` <a id="range.ref.view">[[range.ref.view]]</a>

`ref_view` is a `view` of the elements of some other `range`.

``` cpp
namespace std::ranges {
  template<range R>
    requires is_object_v<R>
  class ref_view : public view_interface<ref_view<R>> {
  private:
    R* r_ = nullptr;            // exposition only
  public:
    constexpr ref_view() noexcept = default;

    template<not-same-as<ref_view> T>
      requires see below
    constexpr ref_view(T&& t);

    constexpr R& base() const { return *r_; }

    constexpr iterator_t<R> begin() const { return ranges::begin(*r_); }
    constexpr sentinel_t<R> end() const { return ranges::end(*r_); }

    constexpr bool empty() const
      requires requires { ranges::empty(*r_); }
    { return ranges::empty(*r_); }

    constexpr auto size() const requires sized_range<R>
    { return ranges::size(*r_); }

    constexpr auto data() const requires contiguous_range<R>
    { return ranges::data(*r_); }
  };
  template<class R>
    ref_view(R&) -> ref_view<R>;
}
```

``` cpp
template<not-same-as<ref_view> T>
  requires see below
constexpr ref_view(T&& t);
```

*Remarks:* Let *`FUN`* denote the exposition-only functions

``` cpp
void FUN(R&);
void FUN(R&&) = delete;
```

The expression in the *requires-clause* is equivalent to

``` cpp
convertible_to<T, R&> && requires { FUN(declval<T>()); }
```

*Effects:* Initializes *r\_* with
`addressof(static_cast<R&>(std::forward<T>(t)))`.

### Filter view <a id="range.filter">[[range.filter]]</a>

#### Overview <a id="range.filter.overview">[[range.filter.overview]]</a>

`filter_view` presents a `view` of the elements of an underlying
sequence that satisfy a predicate.

The name `views::filter` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `P`, the
expression `views::filter(E, P)` is expression-equivalent to
`filter_view{E, P}`.

[*Example 1*:

``` cpp
vector<int> is{ 0, 1, 2, 3, 4, 5, 6 };
filter_view evens{is, [](int i) { return 0 == i % 2; }};
for (int i : evens)
  cout << i << ' '; // prints: 0 2 4 6
```

— *end example*\]

#### Class template `filter_view` <a id="range.filter.view">[[range.filter.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, indirect_unary_predicate<iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class filter_view : public view_interface<filter_view<V, Pred>> {
  private:
    V base_ = V();                      // exposition only
    semiregular-box<Pred> pred_;  // exposition only

    // [range.filter.iterator], class filter_view::iterator
    class iterator;                     // exposition only
    // [range.filter.sentinel], class filter_view::sentinel
    class sentinel;                     // exposition only

  public:
    filter_view() = default;
    constexpr filter_view(V base, Pred pred);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr const Pred& pred() const;

    constexpr iterator begin();
    constexpr auto end() {
      if constexpr (common_range<V>)
        return iterator{*this, ranges::end(base_)};
      else
        return sentinel{*this};
    }
  };

  template<class R, class Pred>
    filter_view(R&&, Pred) -> filter_view<views::all_t<R>, Pred>;
}
```

``` cpp
constexpr filter_view(V base, Pred pred);
```

*Effects:* Initializes *base\_* with `std::move(base)` and initializes
*pred\_* with `std::move(pred)`.

``` cpp
constexpr const Pred& pred() const;
```

*Effects:* Equivalent to: `return *`*`pred_`*`;`

``` cpp
constexpr iterator begin();
```

*Preconditions:* `pred_.has_value()`.

*Returns:* `{*this, ranges::find_if(`*`base_`*`, ref(*`*`pred_`*`))}`.

*Remarks:* In order to provide the amortized constant time complexity
required by the `range` concept when `filter_view` models
`forward_range`, this function caches the result within the
`filter_view` for use on subsequent calls.

#### Class `filter_view::iterator` <a id="range.filter.iterator">[[range.filter.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, indirect_unary_predicate<iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class filter_view<V, Pred>::iterator {
  private:
    iterator_t<V> current_ = iterator_t<V>();   // exposition only
    filter_view* parent_ = nullptr;             // exposition only
  public:
    using iterator_concept  = see below;
    using iterator_category = see below;
    using value_type        = range_value_t<V>;
    using difference_type   = range_difference_t<V>;

    iterator() = default;
    constexpr iterator(filter_view& parent, iterator_t<V> current);

    constexpr iterator_t<V> base() const &
      requires copyable<iterator_t<V>>;
    constexpr iterator_t<V> base() &&;
    constexpr range_reference_t<V> operator*() const;
    constexpr iterator_t<V> operator->() const
      requires has-arrow<iterator_t<V>> && copyable<iterator_t<V>>;

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<V>;

    constexpr iterator& operator--() requires bidirectional_range<V>;
    constexpr iterator operator--(int) requires bidirectional_range<V>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<iterator_t<V>>;

    friend constexpr range_rvalue_reference_t<V> iter_move(const iterator& i)
      noexcept(noexcept(ranges::iter_move(i.current_)));
    friend constexpr void iter_swap(const iterator& x, const iterator& y)
      noexcept(noexcept(ranges::iter_swap(x.current_, y.current_)))
      requires indirectly_swappable<iterator_t<V>>;
  };
}
```

Modification of the element a `filter_view::iterator` denotes is
permitted, but results in undefined behavior if the resulting value does
not satisfy the filter predicate.

`iterator::iterator_concept` is defined as follows:

- If `V` models `bidirectional_range`, then `iterator_concept` denotes
  `bidirectional_iterator_tag`.
- Otherwise, if `V` models `forward_range`, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

`iterator::iterator_category` is defined as follows:

- Let `C` denote the type
  `iterator_traits<iterator_t<V>>::iterator_category`.
- If `C` models `derived_from<bidirectional_iterator_tag>`, then
  `iterator_category` denotes `bidirectional_iterator_tag`.
- Otherwise, if `C` models `derived_from<forward_iterator_tag>`, then
  `iterator_category` denotes `forward_iterator_tag`.
- Otherwise, `iterator_category` denotes `C`.

``` cpp
constexpr iterator(filter_view& parent, iterator_t<V> current);
```

*Effects:* Initializes *current\_* with `std::move(current)` and
*parent\_* with `addressof(parent)`.

``` cpp
constexpr iterator_t<V> base() const &
  requires copyable<iterator_t<V>>;
```

*Effects:* Equivalent to: `return `*`current_`*`;`

``` cpp
constexpr iterator_t<V> base() &&;
```

*Effects:* Equivalent to: `return std::move(current_);`

``` cpp
constexpr range_reference_t<V> operator*() const;
```

*Effects:* Equivalent to: `return *`*`current_`*`;`

``` cpp
constexpr iterator_t<V> operator->() const
  requires has-arrow<iterator_t<V>> && copyable<iterator_t<V>>;
```

*Effects:* Equivalent to: `return `*`current_`*`;`

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
current_ = ranges::find_if(std::move(++current_), ranges::end(parent_->base_),
                           ref(*parent_->pred_));
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
constexpr iterator operator++(int) requires forward_range<V>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--() requires bidirectional_range<V>;
```

*Effects:* Equivalent to:

``` cpp
do
  --current_;
while (!invoke(*parent_->pred_, *current_));
return *this;
```

``` cpp
constexpr iterator operator--(int) requires bidirectional_range<V>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires equality_comparable<iterator_t<V>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`current_`*`;`

``` cpp
friend constexpr range_rvalue_reference_t<V> iter_move(const iterator& i)
  noexcept(noexcept(ranges::iter_move(i.current_)));
```

*Effects:* Equivalent to: `return ranges::iter_move(i.`*`current_`*`);`

``` cpp
friend constexpr void iter_swap(const iterator& x, const iterator& y)
  noexcept(noexcept(ranges::iter_swap(x.current_, y.current_)))
  requires indirectly_swappable<iterator_t<V>>;
```

*Effects:* Equivalent to
`ranges::iter_swap(x.`*`current_`*`, y.`*`current_`*`)`.

#### Class `filter_view::sentinel` <a id="range.filter.sentinel">[[range.filter.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, indirect_unary_predicate<iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class filter_view<V, Pred>::sentinel {
  private:
    sentinel_t<V> end_ = sentinel_t<V>();       // exposition only
  public:
    sentinel() = default;
    constexpr explicit sentinel(filter_view& parent);

    constexpr sentinel_t<V> base() const;

    friend constexpr bool operator==(const iterator& x, const sentinel& y);
  };
}
```

``` cpp
constexpr explicit sentinel(filter_view& parent);
```

*Effects:* Initializes *end\_* with `ranges::end(parent.`*`base_`*`)`.

``` cpp
constexpr sentinel_t<V> base() const;
```

*Effects:* Equivalent to: `return `*`end_`*`;`

``` cpp
friend constexpr bool operator==(const iterator& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`end_`*`;`

### Transform view <a id="range.transform">[[range.transform]]</a>

#### Overview <a id="range.transform.overview">[[range.transform.overview]]</a>

`transform_view` presents a `view` of an underlying sequence after
applying a transformation function to each element.

The name `views::transform` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::transform(E, F)` is expression-equivalent to
`transform_view{E, F}`.

[*Example 1*:

``` cpp
vector<int> is{ 0, 1, 2, 3, 4 };
transform_view squares{is, [](int i) { return i * i; }};
for (int i : squares)
  cout << i << ' '; // prints: 0 1 4 9 16
```

— *end example*\]

#### Class template `transform_view` <a id="range.transform.view">[[range.transform.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, copy_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>> &&
             can-reference<invoke_result_t<F&, range_reference_t<V>>>
  class transform_view : public view_interface<transform_view<V, F>> {
  private:
    // [range.transform.iterator], class template transform_view::iterator
    template<bool> struct iterator;             // exposition only
    // [range.transform.sentinel], class template transform_view::sentinel
    template<bool> struct sentinel;             // exposition only

    V base_ = V();                              // exposition only
    semiregular-box<F> fun_;                    // exposition only

  public:
    transform_view() = default;
    constexpr transform_view(V base, F fun);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr iterator<false> begin();
    constexpr iterator<true> begin() const
      requires range<const V> &&
               regular_invocable<const F&, range_reference_t<const V>>;

    constexpr sentinel<false> end();
    constexpr iterator<false> end() requires common_range<V>;
    constexpr sentinel<true> end() const
      requires range<const V> &&
               regular_invocable<const F&, range_reference_t<const V>>;
    constexpr iterator<true> end() const
      requires common_range<const V> &&
               regular_invocable<const F&, range_reference_t<const V>>;

    constexpr auto size() requires sized_range<V> { return ranges::size(base_); }
    constexpr auto size() const requires sized_range<const V>
    { return ranges::size(base_); }
  };

  template<class R, class F>
    transform_view(R&&, F) -> transform_view<views::all_t<R>, F>;
}
```

``` cpp
constexpr transform_view(V base, F fun);
```

*Effects:* Initializes *base\_* with `std::move(base)` and *fun\_* with
`std::move(fun)`.

``` cpp
constexpr iterator<false> begin();
```

*Effects:* Equivalent to:

``` cpp
return iterator<false>{*this, ranges::begin(base_)};
```

``` cpp
constexpr iterator<true> begin() const
  requires range<const V> &&
           regular_invocable<const F&, range_reference_t<const V>>;
```

*Effects:* Equivalent to:

``` cpp
return iterator<true>{*this, ranges::begin(base_)};
```

``` cpp
constexpr sentinel<false> end();
```

*Effects:* Equivalent to:

``` cpp
return sentinel<false>{ranges::end(base_)};
```

``` cpp
constexpr iterator<false> end() requires common_range<V>;
```

*Effects:* Equivalent to:

``` cpp
return iterator<false>{*this, ranges::end(base_)};
```

``` cpp
constexpr sentinel<true> end() const
  requires range<const V> &&
           regular_invocable<const F&, range_reference_t<const V>>;
```

*Effects:* Equivalent to:

``` cpp
return sentinel<true>{ranges::end(base_)};
```

``` cpp
constexpr iterator<true> end() const
  requires common_range<const V> &&
           regular_invocable<const F&, range_reference_t<const V>>;
```

*Effects:* Equivalent to:

``` cpp
return iterator<true>{*this, ranges::end(base_)};
```

#### Class template `transform_view::iterator` <a id="range.transform.iterator">[[range.transform.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, copy_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>> &&
             can-reference<invoke_result_t<F&, range_reference_t<V>>>
  template<bool Const>
  class transform_view<V, F>::iterator {
  private:
    using Parent =                              // exposition only
      conditional_t<Const, const transform_view, transform_view>;
    using Base   =                              // exposition only
      conditional_t<Const, const V, V>;
    iterator_t<Base> current_ =                 // exposition only
      iterator_t<Base>();
    Parent* parent_ = nullptr;                  // exposition only
  public:
    using iterator_concept  = see below;
    using iterator_category = see below;
    using value_type        =
      remove_cvref_t<invoke_result_t<F&, range_reference_t<Base>>>;
    using difference_type   = range_difference_t<Base>;

    iterator() = default;
    constexpr iterator(Parent& parent, iterator_t<Base> current);
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr iterator_t<Base> base() const &
      requires copyable<iterator_t<Base>>;
    constexpr iterator_t<Base> base() &&;
    constexpr decltype(auto) operator*() const
    { return invoke(*parent_->fun_, *current_); }

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<Base>;

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type n)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type n)
      requires random_access_range<Base>;
    constexpr decltype(auto) operator[](difference_type n) const
      requires random_access_range<Base>
    { return invoke(*parent_->fun_, current_[n]); }

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<iterator_t<Base>>;

    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator<=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base> && three_way_comparable<iterator_t<Base>>;

    friend constexpr iterator operator+(iterator i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, iterator i)
      requires random_access_range<Base>;

    friend constexpr iterator operator-(iterator i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires random_access_range<Base>;

    friend constexpr decltype(auto) iter_move(const iterator& i)
      noexcept(noexcept(invoke(*i.parent_->fun_, *i.current_)))
    {
      if constexpr (is_lvalue_reference_v<decltype(*i)>)
        return std::move(*i);
      else
        return *i;
    }

    friend constexpr void iter_swap(const iterator& x, const iterator& y)
      noexcept(noexcept(ranges::iter_swap(x.current_, y.current_)))
      requires indirectly_swappable<iterator_t<Base>>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If `V` models `random_access_range`, then `iterator_concept` denotes
  `random_access_iterator_tag`.
- Otherwise, if `V` models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if `V` models `forward_range`, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

`iterator::iterator_category` is defined as follows: Let `C` denote the
type `iterator_traits<iterator_t<Base>>::iterator_category`.

- If
  `is_lvalue_reference_v<invoke_result_t<F&, range_reference_t<Base>>>`
  is `true`, then
  - if `C` models `derived_from<contiguous_iterator_tag>`,
    `iterator_category` denotes `random_access_iterator_tag`;
  - otherwise, `iterator_category` denotes `C`.
- Otherwise, `iterator_category` denotes `input_iterator_tag`.

``` cpp
constexpr iterator(Parent& parent, iterator_t<Base> current);
```

*Effects:* Initializes *current\_* with `std::move(current)` and
*parent\_* with `addressof(parent)`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`
and *parent\_* with `i.`*`parent_`*.

``` cpp
constexpr iterator_t<Base> base() const &
  requires copyable<iterator_t<Base>>;
```

*Effects:* Equivalent to: `return `*`current_`*`;`

``` cpp
constexpr iterator_t<Base> base() &&;
```

*Effects:* Equivalent to: `return std::move(current_);`

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++current_;
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++current_`.

``` cpp
constexpr iterator operator++(int) requires forward_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--() requires bidirectional_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
--current_;
return *this;
```

``` cpp
constexpr iterator operator--(int) requires bidirectional_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
constexpr iterator& operator+=(difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
current_ += n;
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
current_ -= n;
return *this;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires equality_comparable<iterator_t<Base>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`current_`*`;`

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` < y.`*`current_`*`;`

``` cpp
friend constexpr bool operator>(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return y < x;`

``` cpp
friend constexpr bool operator<=(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return !(y < x);`

``` cpp
friend constexpr bool operator>=(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return !(x < y);`

``` cpp
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires random_access_range<Base> && three_way_comparable<iterator_t<Base>>;
```

*Effects:* Equivalent to:
`return x.`*`current_`*` <=> y.`*`current_`*`;`

``` cpp
friend constexpr iterator operator+(iterator i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, iterator i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return iterator{*i.`*`parent_`*`, i.`*`current_`*` + n};`

``` cpp
friend constexpr iterator operator-(iterator i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return iterator{*i.`*`parent_`*`, i.`*`current_`*` - n};`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`current_`*`;`

``` cpp
friend constexpr void iter_swap(const iterator& x, const iterator& y)
  noexcept(noexcept(ranges::iter_swap(x.current_, y.current_)))
  requires indirectly_swappable<iterator_t<Base>>;
```

*Effects:* Equivalent to
`ranges::iter_swap(x.`*`current_`*`, y.`*`current_`*`)`.

#### Class template `transform_view::sentinel` <a id="range.transform.sentinel">[[range.transform.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, copy_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>> &&
             can-reference<invoke_result_t<F&, range_reference_t<V>>>
  template<bool Const>
  class transform_view<V, F>::sentinel {
  private:
    using Parent =                                      // exposition only
      conditional_t<Const, const transform_view, transform_view>;
    using Base = conditional_t<Const, const V, V>;      // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only
  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end);
    constexpr sentinel(sentinel<!Const> i)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    friend constexpr bool operator==(const iterator<Const>& x, const sentinel& y);

    friend constexpr range_difference_t<Base>
      operator-(const iterator<Const>& x, const sentinel& y)
        requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
    friend constexpr range_difference_t<Base>
      operator-(const sentinel& y, const iterator<Const>& x)
        requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
  };
}
```

``` cpp
constexpr explicit sentinel(sentinel_t<Base> end);
```

*Effects:* Initializes *end\_* with `end`.

``` cpp
constexpr sentinel(sentinel<!Const> i)
  requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *end\_* with `std::move(i.`*`end_`*`)`.

``` cpp
constexpr sentinel_t<Base> base() const;
```

*Effects:* Equivalent to: `return `*`end_`*`;`

``` cpp
friend constexpr bool operator==(const iterator<Const>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`end_`*`;`

``` cpp
friend constexpr range_difference_t<Base>
  operator-(const iterator<Const>& x, const sentinel& y)
    requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`end_`*`;`

``` cpp
friend constexpr range_difference_t<Base>
  operator-(const sentinel& y, const iterator<Const>& x)
    requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return y.`*`end_`*` - x.`*`current_`*`;`

### Take view <a id="range.take">[[range.take]]</a>

#### Overview <a id="range.take.overview">[[range.take.overview]]</a>

`take_view` produces a `view` of the first N elements from another
`view`, or all the elements if the adapted `view` contains fewer than N.

The name `views::take` denotes a range adaptor object
[[range.adaptor.object]]. Let `E` and `F` be expressions, let `T` be
`remove_cvref_t<decltype((E))>`, and let `D` be
`range_difference_t<decltype((E))>`. If `decltype((F))` does not model
`convertible_to<D>`, `views::take(E, F)` is ill-formed. Otherwise, the
expression `views::take(E, F)` is expression-equivalent to:

- If `T` is a specialization of `ranges::empty_view`
  [[range.empty.view]], then `((void) F, decay-copy(E))`.
- Otherwise, if `T` models `random_access_range` and `sized_range` and
  is
  - a specialization of `span` [[views.span]] where
    `T::extent == dynamic_extent`,
  - a specialization of `basic_string_view` [[string.view]],
  - a specialization of `ranges::iota_view` [[range.iota.view]], or
  - a specialization of `ranges::subrange` [[range.subrange]],

  then
  `T{ranges::begin(E), ranges::begin(E) + min<D>(ranges::size(E), F)}`,
  except that `E` is evaluated only once.
- Otherwise, `ranges::take_view{E, F}`.

[*Example 1*:

``` cpp
vector<int> is{0,1,2,3,4,5,6,7,8,9};
take_view few{is, 5};
for (int i : few)
  cout << i << ' '; // prints: 0 1 2 3 4
```

— *end example*\]

#### Class template `take_view` <a id="range.take.view">[[range.take.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
  class take_view : public view_interface<take_view<V>> {
  private:
    V base_ = V();                                      // exposition only
    range_difference_t<V> count_ = 0;                   // exposition only
    // [range.take.sentinel], class template take_view::sentinel
    template<bool> struct sentinel;                     // exposition only
  public:
    take_view() = default;
    constexpr take_view(V base, range_difference_t<V> count);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>) {
      if constexpr (sized_range<V>) {
        if constexpr (random_access_range<V>)
          return ranges::begin(base_);
        else {
          auto sz = size();
          return counted_iterator{ranges::begin(base_), sz};
        }
      } else
        return counted_iterator{ranges::begin(base_), count_};
    }

    constexpr auto begin() const requires range<const V> {
      if constexpr (sized_range<const V>) {
        if constexpr (random_access_range<const V>)
          return ranges::begin(base_);
        else {
          auto sz = size();
          return counted_iterator{ranges::begin(base_), sz};
        }
      } else
        return counted_iterator{ranges::begin(base_), count_};
    }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (sized_range<V>) {
        if constexpr (random_access_range<V>)
          return ranges::begin(base_) + size();
        else
          return default_sentinel;
      } else
        return sentinel<false>{ranges::end(base_)};
    }

    constexpr auto end() const requires range<const V> {
      if constexpr (sized_range<const V>) {
        if constexpr (random_access_range<const V>)
          return ranges::begin(base_) + size();
        else
          return default_sentinel;
      } else
        return sentinel<true>{ranges::end(base_)};
    }

    constexpr auto size() requires sized_range<V> {
      auto n = ranges::size(base_);
      return ranges::min(n, static_cast<decltype(n)>(count_));
    }

    constexpr auto size() const requires sized_range<const V> {
      auto n = ranges::size(base_);
      return ranges::min(n, static_cast<decltype(n)>(count_));
    }
  };

  template<range R>
    take_view(R&&, range_difference_t<R>)
      -> take_view<views::all_t<R>>;
}
```

``` cpp
constexpr take_view(V base, range_difference_t<V> count);
```

*Effects:* Initializes *base\_* with `std::move(base)` and *count\_*
with `count`.

#### Class template `take_view::sentinel` <a id="range.take.sentinel">[[range.take.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<view V>
  template<bool Const>
  class take_view<V>::sentinel {
  private:
    using Base = conditional_t<Const, const V, V>;      // exposition only
    using CI = counted_iterator<iterator_t<Base>>;      // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only
  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end);
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    friend constexpr bool operator==(const CI& y, const sentinel& x);
  };
}
```

``` cpp
constexpr explicit sentinel(sentinel_t<Base> end);
```

*Effects:* Initializes *end\_* with `end`.

``` cpp
constexpr sentinel(sentinel<!Const> s)
  requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *end\_* with `std::move(s.`*`end_`*`)`.

``` cpp
constexpr sentinel_t<Base> base() const;
```

*Effects:* Equivalent to: `return `*`end_`*`;`

``` cpp
friend constexpr bool operator==(const CI& y, const sentinel& x);
```

*Effects:* Equivalent to:
`return y.count() == 0 || y.base() == x.`*`end_`*`;`

### Take while view <a id="range.take.while">[[range.take.while]]</a>

#### Overview <a id="range.take.while.overview">[[range.take.while.overview]]</a>

Given a unary predicate `pred` and a `view` `r`, `take_while_view`
produces a `view` of the range \[`begin(r)`,
`ranges::find_if_not(r, pred)`).

The name `views::take_while` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::take_while(E, F)` is expression-equivalent to
`take_while_view{E, F}`.

[*Example 1*:

``` cpp
auto input = istringstream{"0 1 2 3 4 5 6 7 8 9"};
auto small = [](const auto x) noexcept { return x < 5; };
auto small_ints = istream_view<int>(input) | views::take_while(small);
for (const auto i : small_ints) {
  cout << i << ' ';                             // prints 0 1 2 3 4
}
auto i = 0;
input >> i;
cout << i;                                      // prints 6
```

— *end example*\]

#### Class template `take_while_view` <a id="range.take.while.view">[[range.take.while.view]]</a>

``` cpp
namespace std::ranges {
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
  class take_while_view : public view_interface<take_while_view<V, Pred>> {
    // [range.take.while.sentinel], class template take_while_view::sentinel
    template<bool> class sentinel;                      // exposition only

    V base_ = V();                                      // exposition only
    semiregular-box<Pred> pred_; \itcorr[-1]                       // exposition only

  public:
    take_while_view() = default;
    constexpr take_while_view(V base, Pred pred);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr const Pred& pred() const;

    constexpr auto begin() requires (!simple-view<V>)
    { return ranges::begin(base_); }

    constexpr auto begin() const requires range<const V>
    { return ranges::begin(base_); }

    constexpr auto end() requires (!simple-view<V>)
    { return sentinel<false>(ranges::end(base_), addressof(*pred_)); }

    constexpr auto end() const requires range<const V>
    { return sentinel<true>(ranges::end(base_), addressof(*pred_)); }
  };

  template<class R, class Pred>
    take_while_view(R&&, Pred) -> take_while_view<views::all_t<R>, Pred>;
}
```

``` cpp
constexpr take_while_view(V base, Pred pred);
```

*Effects:* Initializes *base\_* with `std::move(base)` and *pred\_* with
`std::move(pred)`.

``` cpp
constexpr const Pred& pred() const;
```

*Effects:* Equivalent to: `return *`*`pred_`*`;`

#### Class template `take_while_view::sentinel` <a id="range.take.while.sentinel">[[range.take.while.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
  template<bool Const>
  class take_while_view<V, Pred>::sentinel {            // exposition only
    using Base = conditional_t<Const, const V, V>;      // exposition only

    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only
    const Pred* pred_ = nullptr;                        // exposition only
  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end, const Pred* pred);
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const { return end_; }

    friend constexpr bool operator==(const iterator_t<Base>& x, const sentinel& y);
  };
}
```

``` cpp
constexpr explicit sentinel(sentinel_t<Base> end, const Pred* pred);
```

*Effects:* Initializes *end\_* with `end` and *pred\_* with `pred`.

``` cpp
constexpr sentinel(sentinel<!Const> s)
  requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *end\_* with `s.`*`end_`* and *pred\_* with
`s.`*`pred_`*.

``` cpp
friend constexpr bool operator==(const iterator_t<Base>& x, const sentinel& y);
```

*Effects:* Equivalent to:
`return y.`*`end_`*` == x || !invoke(*y.`*`pred_`*`, *x);`

### Drop view <a id="range.drop">[[range.drop]]</a>

#### Overview <a id="range.drop.overview">[[range.drop.overview]]</a>

`drop_view` produces a `view` excluding the first N elements from
another `view`, or an empty range if the adapted `view` contains fewer
than N elements.

The name `views::drop` denotes a range adaptor object
[[range.adaptor.object]]. Let `E` and `F` be expressions, let `T` be
`remove_cvref_t<decltype((E))>`, and let `D` be
`range_difference_t<decltype((E))>`. If `decltype((F))` does not model
`convertible_to<D>`, `views::drop(E, F)` is ill-formed. Otherwise, the
expression `views::drop(E, F)` is expression-equivalent to:

- If `T` is a specialization of `ranges::empty_view`
  [[range.empty.view]], then `((void) F, decay-copy(E))`.
- Otherwise, if `T` models `random_access_range` and `sized_range` and
  is
  - a specialization of `span` [[views.span]] where
    `T::extent == dynamic_extent`,
  - a specialization of `basic_string_view` [[string.view]],
  - a specialization of `ranges::iota_view` [[range.iota.view]], or
  - a specialization of `ranges::subrange` [[range.subrange]],

  then
  `T{ranges::begin(E) + min<D>(ranges::size(E), F), ranges::end(E)}`,
  except that `E` is evaluated only once.
- Otherwise, `ranges::drop_view{E, F}`.

[*Example 1*:

``` cpp
auto ints = views::iota(0) | views::take(10);
auto latter_half = drop_view{ints, 5};
for (auto i : latter_half) {
  cout << i << ' ';                             // prints 5 6 7 8 9
}
```

— *end example*\]

#### Class template `drop_view` <a id="range.drop.view">[[range.drop.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
  class drop_view : public view_interface<drop_view<V>> {
  public:
    drop_view() = default;
    constexpr drop_view(V base, range_difference_t<V> count);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin()
      requires (!(simple-view<V> && random_access_range<V>));
    constexpr auto begin() const
      requires random_access_range<const V>;

    constexpr auto end()
      requires (!simple-view<V>)
    { return ranges::end(base_); }

    constexpr auto end() const
      requires range<const V>
    { return ranges::end(base_); }

    constexpr auto size()
      requires sized_range<V>
    {
      const auto s = ranges::size(base_);
      const auto c = static_cast<decltype(s)>(count_);
      return s < c ? 0 : s - c;
    }

    constexpr auto size() const
      requires sized_range<const V>
    {
      const auto s = ranges::size(base_);
      const auto c = static_cast<decltype(s)>(count_);
      return s < c ? 0 : s - c;
    }
  private:
    V base_ = V();                              // exposition only
    range_difference_t<V> count_ = 0;           // exposition only
  };

  template<class R>
    drop_view(R&&, range_difference_t<R>) -> drop_view<views::all_t<R>>;
}
```

``` cpp
constexpr drop_view(V base, range_difference_t<V> count);
```

*Preconditions:* `count >= 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *count\_*
with `count`.

``` cpp
constexpr auto begin()
  requires (!(simple-view<V> && random_access_range<V>));
constexpr auto begin() const
  requires random_access_range<const V>;
```

*Returns:*
`ranges::next(ranges::begin(base_), count_, ranges::end(base_))`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept when `drop_view` models `forward_range`,
the first overload caches the result within the `drop_view` for use on
subsequent calls.

[*Note 1*: Without this, applying a `reverse_view` over a `drop_view`
would have quadratic iteration complexity. — *end note*\]

### Drop while view <a id="range.drop.while">[[range.drop.while]]</a>

#### Overview <a id="range.drop.while.overview">[[range.drop.while.overview]]</a>

Given a unary predicate `pred` and a `view` `r`, `drop_while_view`
produces a `view` of the range \[`ranges::find_if_not(r, pred)`,
`ranges::end(r)`).

The name `views::drop_while` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::drop_while(E, F)` is expression-equivalent to
`drop_while_view{E, F}`.

[*Example 1*:

``` cpp
constexpr auto source = "  \t   \t   \t   hello there";
auto is_invisible = [](const auto x) { return x == ' ' || x == '\t'; };
auto skip_ws = drop_while_view{source, is_invisible};
for (auto c : skip_ws) {
  cout << c;                                    // prints hello there with no leading space
}
```

— *end example*\]

#### Class template `drop_while_view` <a id="range.drop.while.view">[[range.drop.while.view]]</a>

``` cpp
namespace std::ranges {
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
  class drop_while_view : public view_interface<drop_while_view<V, Pred>> {
  public:
    drop_while_view() = default;
    constexpr drop_while_view(V base, Pred pred);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr const Pred& pred() const;

    constexpr auto begin();

    constexpr auto end()
    { return ranges::end(base_); }

  private:
    V base_ = V();                                      // exposition only
    semiregular-box<Pred> pred_; \itcorr[-1]                       // exposition only
  };

  template<class R, class Pred>
    drop_while_view(R&&, Pred) -> drop_while_view<views::all_t<R>, Pred>;
}
```

``` cpp
constexpr drop_while_view(V base, Pred pred);
```

*Effects:* Initializes *base\_* with `std::move(base)` and *pred\_* with
`std::move(pred)`.

``` cpp
constexpr const Pred& pred() const;
```

*Effects:* Equivalent to: `return *`*`pred_`*`;`

``` cpp
constexpr auto begin();
```

*Returns:* `ranges::find_if_not(base_, cref(*pred_))`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept when `drop_while_view` models
`forward_range`, the first call caches the result within the
`drop_while_view` for use on subsequent calls.

[*Note 1*: Without this, applying a `reverse_view` over a
`drop_while_view` would have quadratic iteration
complexity. — *end note*\]

### Join view <a id="range.join">[[range.join]]</a>

#### Overview <a id="range.join.overview">[[range.join.overview]]</a>

`join_view` flattens a `view` of ranges into a `view`.

The name `views::join` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::join(E)` is expression-equivalent to `join_view{E}`.

[*Example 1*:

``` cpp
vector<string> ss{"hello", " ", "world", "!"};
join_view greeting{ss};
for (char ch : greeting)
  cout << ch;                                   // prints: hello world!
```

— *end example*\]

#### Class template `join_view` <a id="range.join.view">[[range.join.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>> &&
             (is_reference_v<range_reference_t<V>> ||
              view<range_value_t<V>>)
  class join_view : public view_interface<join_view<V>> {
  private:
    using InnerRng =                    // exposition only
      range_reference_t<V>;
    // [range.join.iterator], class template join_view::iterator
    template<bool Const>
      struct iterator;                  // exposition only
    // [range.join.sentinel], class template join_view::sentinel
    template<bool Const>
      struct sentinel;                  // exposition only

    V base_ = V();                      // exposition only
    views::all_t<InnerRng> inner_ =     // exposition only, present only when !is_reference_v<InnerRng>
      views::all_t<InnerRng>();
  public:
    join_view() = default;
    constexpr explicit join_view(V base);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() {
      constexpr bool use_const = simple-view<V> &&
                                 is_reference_v<range_reference_t<V>>;
      return iterator<use_const>{*this, ranges::begin(base_)};
    }

    constexpr auto begin() const
    requires input_range<const V> &&
             is_reference_v<range_reference_t<const V>> {
      return iterator<true>{*this, ranges::begin(base_)};
    }

    constexpr auto end() {
      if constexpr (forward_range<V> &&
                    is_reference_v<InnerRng> && forward_range<InnerRng> &&
                    common_range<V> && common_range<InnerRng>)
        return iterator<simple-view<V>>{*this, ranges::end(base_)};
      else
        return sentinel<simple-view<V>>{*this};
    }

    constexpr auto end() const
    requires input_range<const V> &&
             is_reference_v<range_reference_t<const V>> {
      if constexpr (forward_range<const V> &&
                    is_reference_v<range_reference_t<const V>> &&
                    forward_range<range_reference_t<const V>> &&
                    common_range<const V> &&
                    common_range<range_reference_t<const V>>)
        return iterator<true>{*this, ranges::end(base_)};
      else
        return sentinel<true>{*this};
    }
  };

  template<class R>
    explicit join_view(R&&) -> join_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit join_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

#### Class template `join_view::iterator` <a id="range.join.iterator">[[range.join.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>> &&
             (is_reference_v<range_reference_t<V>> ||
              view<range_value_t<V>>)
  template<bool Const>
  struct join_view<V>::iterator {
  private:
    using Parent =                                              // exposition only
      conditional_t<Const, const join_view, join_view>;
    using Base   = conditional_t<Const, const V, V>;            // exposition only

    static constexpr bool ref-is-glvalue =                      // exposition only
      is_reference_v<range_reference_t<Base>>;

    iterator_t<Base> outer_ = iterator_t<Base>();               // exposition only
    iterator_t<range_reference_t<Base>> inner_ =                // exposition only
      iterator_t<range_reference_t<Base>>();
    Parent* parent_ = nullptr;                                  // exposition only

    constexpr void satisfy();                                   // exposition only
  public:
    using iterator_concept  = see below;
    using iterator_category = see below;
    using value_type        = range_value_t<range_reference_t<Base>>;
    using difference_type   = see below;

    iterator() = default;
    constexpr iterator(Parent& parent, iterator_t<Base> outer);
    constexpr iterator(iterator<!Const> i)
      requires Const &&
               convertible_to<iterator_t<V>, iterator_t<Base>> &&
               convertible_to<iterator_t<InnerRng>,
                              iterator_t<range_reference_t<Base>>>;

    constexpr decltype(auto) operator*() const { return *inner_; }

    constexpr iterator_t<Base> operator->() const
      requires has-arrow<iterator_t<Base>> && copyable<iterator_t<Base>>;

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int)
      requires ref-is-glvalue && forward_range<Base> &&
               forward_range<range_reference_t<Base>>;

    constexpr iterator& operator--()
      requires ref-is-glvalue && bidirectional_range<Base> &&
               bidirectional_range<range_reference_t<Base>> &&
               common_range<range_reference_t<Base>>;

    constexpr iterator operator--(int)
      requires ref-is-glvalue && bidirectional_range<Base> &&
               bidirectional_range<range_reference_t<Base>> &&
               common_range<range_reference_t<Base>>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires ref-is-glvalue && equality_comparable<iterator_t<Base>> &&
               equality_comparable<iterator_t<range_reference_t<Base>>>;

    friend constexpr decltype(auto) iter_move(const iterator& i)
    noexcept(noexcept(ranges::iter_move(i.inner_))) {
      return ranges::iter_move(i.inner_);
    }

    friend constexpr void iter_swap(const iterator& x, const iterator& y)
      noexcept(noexcept(ranges::iter_swap(x.inner_, y.inner_)));
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *ref-is-glvalue* is `true` and *Base* and `range_reference_t<Base>`
  each model `bidirectional_range`, then `iterator_concept` denotes
  `bidirectional_iterator_tag`.
- Otherwise, if *ref-is-glvalue* is `true` and *Base* and
  `range_reference_t<Base>` each model , then `iterator_concept` denotes
  `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

`iterator::iterator_category` is defined as follows:

- Let *OUTERC* denote
  `iterator_traits<iterator_t<Base>>::iterator_category`, and let
  *INNERC* denote
  `iterator_traits<iterator_t<range_reference_t<Base>>>::iterator_category`.
- If *ref-is-glvalue* is `true` and *OUTERC* and *INNERC* each model
  `derived_from<bidirectional_iterator_tag>`, `iterator_category`
  denotes `bidirectional_iterator_tag`.
- Otherwise, if *ref-is-glvalue* is `true` and *OUTERC* and *INNERC*
  each model `derived_from<forward_iterator_tag>`, `iterator_category`
  denotes `forward_iterator_tag`.
- Otherwise, if *OUTERC* and *INNERC* each model
  `derived_from<input_iterator_tag>`, `iterator_category` denotes
  `input_iterator_tag`.
- Otherwise, `iterator_category` denotes `output_iterator_tag`.

`iterator::difference_type` denotes the type:

``` cpp
common_type_t<
  range_difference_t<Base>,
  range_difference_t<range_reference_t<Base>>>
```

`join_view` iterators use the *satisfy* function to skip over empty
inner ranges.

``` cpp
constexpr void satisfy();       // exposition only
```

*Effects:* Equivalent to:

``` cpp
auto update_inner = [this](range_reference_t<Base> x) -> auto& {
  if constexpr (ref-is-glvalue) // x is a reference
    return x;
  else
    return (parent_->inner_ = views::all(std::move(x)));
};

for (; outer_ != ranges::end(parent_->base_); ++outer_) {
  auto& inner = update_inner(*outer_);
  inner_ = ranges::begin(inner);
  if (inner_ != ranges::end(inner))
    return;
}
if constexpr (ref-is-glvalue)
  inner_ = iterator_t<range_reference_t<Base>>();
```

``` cpp
constexpr iterator(Parent& parent, iterator_t<Base> outer);
```

*Effects:* Initializes *outer\_* with `std::move(outer)` and *parent\_*
with `addressof(parent)`; then calls *`satisfy`*`()`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const &&
           convertible_to<iterator_t<V>, iterator_t<Base>> &&
           convertible_to<iterator_t<InnerRng>,
                          iterator_t<range_reference_t<Base>>>;
```

*Effects:* Initializes *outer\_* with `std::move(i.`*`outer_`*`)`,
*inner\_* with `std::move(i.`*`inner_`*`)`, and *parent\_* with
`i.`*`parent_`*.

``` cpp
constexpr iterator_t<Base> operator->() const
  requires has-arrow<iterator_t<Base>> && copyable<iterator_t<Base>>;
```

*Effects:* Equivalent to `return `*`inner_`*`;`

``` cpp
constexpr iterator& operator++();
```

Let *`inner-range`* be:

- If *ref-is-glvalue* is `true`, `*`*`outer_`*.
- Otherwise, *`parent_`*`->`*`inner_`*.

*Effects:* Equivalent to:

``` cpp
auto&& inner_rng = inner-range;
if (++inner_ == ranges::end(inner_rng)) {
  ++outer_;
  satisfy();
}
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to: `++*this`.

``` cpp
constexpr iterator operator++(int)
  requires ref-is-glvalue && forward_range<Base> &&
           forward_range<range_reference_t<Base>>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--()
  requires ref-is-glvalue && bidirectional_range<Base> &&
           bidirectional_range<range_reference_t<Base>> &&
           common_range<range_reference_t<Base>>;
```

*Effects:* Equivalent to:

``` cpp
if (outer_ == ranges::end(parent_->base_))
  inner_ = ranges::end(*--outer_);
while (inner_ == ranges::begin(*outer_))
  inner_ = ranges::end(*--outer_);
--inner_;
return *this;
```

``` cpp
constexpr iterator operator--(int)
  requires ref-is-glvalue && bidirectional_range<Base> &&
           bidirectional_range<range_reference_t<Base>> &&
           common_range<range_reference_t<Base>>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires ref-is-glvalue && equality_comparable<iterator_t<Base>> &&
           equality_comparable<iterator_t<range_reference_t<Base>>>;
```

*Effects:* Equivalent to:
`return x.`*`outer_`*` == y.`*`outer_`*` && x.`*`inner_`*` == y.`*`inner_`*`;`

``` cpp
friend constexpr void iter_swap(const iterator& x, const iterator& y)
  noexcept(noexcept(ranges::iter_swap(x.inner_, y.inner_)));
```

*Effects:* Equivalent to:
`return ranges::iter_swap(x.`*`inner_`*`, y.`*`inner_`*`);`

#### Class template `join_view::sentinel` <a id="range.join.sentinel">[[range.join.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>> &&
             (is_reference_v<range_reference_t<V>> ||
              view<range_value_t<V>>)
  template<bool Const>
  struct join_view<V>::sentinel {
  private:
    using Parent =                                      // exposition only
      conditional_t<Const, const join_view, join_view>;
    using Base   = conditional_t<Const, const V, V>;    // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only
  public:
    sentinel() = default;

    constexpr explicit sentinel(Parent& parent);
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    friend constexpr bool operator==(const iterator<Const>& x, const sentinel& y);
  };
}
```

``` cpp
constexpr explicit sentinel(Parent& parent);
```

*Effects:* Initializes *end\_* with `ranges::end(parent.`*`base_`*`)`.

``` cpp
constexpr sentinel(sentinel<!Const> s)
  requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *end\_* with `std::move(s.`*`end_`*`)`.

``` cpp
friend constexpr bool operator==(const iterator<Const>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`outer_`*` == y.`*`end_`*`;`

### Split view <a id="range.split">[[range.split]]</a>

#### Overview <a id="range.split.overview">[[range.split.overview]]</a>

`split_view` takes a `view` and a delimiter, and splits the `view` into
subranges on the delimiter. The delimiter can be a single element or a
`view` of elements.

The name `views::split` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::split(E, F)` is expression-equivalent to
`split_view{E, F}`.

[*Example 1*:

``` cpp
string str{"the quick brown fox"};
split_view sentence{str, ' '};
for (auto word : sentence) {
  for (char ch : word)
    cout << ch;
  cout << '*';
}
// The above prints: the*quick*brown*fox*
```

— *end example*\]

#### Class template `split_view` <a id="range.split.view">[[range.split.view]]</a>

``` cpp
namespace std::ranges {
  template<auto> struct require-constant;       // exposition only

  template<class R>
  concept tiny-range =                          // exposition only
    sized_range<R> &&
    requires { typename require-constant<remove_reference_t<R>::size()>; } &&
    (remove_reference_t<R>::size() <= 1);

  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  class split_view : public view_interface<split_view<V, Pattern>> {
  private:
    V base_ = V();                              // exposition only
    Pattern pattern_ = Pattern();               // exposition only
    iterator_t<V> current_ = iterator_t<V>();   // exposition only, present only if !forward_range<V>
    // [range.split.outer], class template split_view::outer-iterator
    template<bool> struct outer-iterator;       // exposition only
    // [range.split.inner], class template split_view::inner-iterator
    template<bool> struct inner-iterator;       // exposition only
  public:
    split_view() = default;
    constexpr split_view(V base, Pattern pattern);

    template<input_range R>
      requires constructible_from<V, views::all_t<R>> &&
               constructible_from<Pattern, single_view<range_value_t<R>>>
    constexpr split_view(R&& r, range_value_t<R> e);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() {
      if constexpr (forward_range<V>)
        return outer-iterator<simple-view<V>>{*this, ranges::begin(base_)};
      else {
        current_ = ranges::begin(base_);
        return outer-iterator<false>{*this};
      }
    }

    constexpr auto begin() const requires forward_range<V> && forward_range<const V> {
      return outer-iterator<true>{*this, ranges::begin(base_)};
    }

    constexpr auto end() requires forward_range<V> && common_range<V> {
      return outer-iterator<simple-view<V>>{*this, ranges::end(base_)};
    }

    constexpr auto end() const {
      if constexpr (forward_range<V> && forward_range<const V> && common_range<const V>)
        return outer-iterator<true>{*this, ranges::end(base_)};
      else
        return default_sentinel;
    }
  };

  template<class R, class P>
    split_view(R&&, P&&) -> split_view<views::all_t<R>, views::all_t<P>>;

  template<input_range R>
    split_view(R&&, range_value_t<R>)
      -> split_view<views::all_t<R>, single_view<range_value_t<R>>>;
}
```

``` cpp
constexpr split_view(V base, Pattern pattern);
```

*Effects:* Initializes *base\_* with `std::move(base)`, and *pattern\_*
with `std::move(pattern)`.

``` cpp
template<input_range R>
  requires constructible_from<V, views::all_t<R>> &&
           constructible_from<Pattern, single_view<range_value_t<R>>>
constexpr split_view(R&& r, range_value_t<R> e);
```

*Effects:* Initializes *base\_* with `views::all(std::forward<R>(r))`,
and *pattern\_* with `single_view{std::move(e)}`.

#### Class template `split_view::outer-iterator` <a id="range.split.outer">[[range.split.outer]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  template<bool Const>
  struct split_view<V, Pattern>::outer-iterator {
  private:
    using Parent =                          // exposition only
      conditional_t<Const, const split_view, split_view>;
    using Base   =                          // exposition only
      conditional_t<Const, const V, V>;
    Parent* parent_ = nullptr;              // exposition only
    iterator_t<Base> current_ =             // exposition only, present only if V models forward_range
      iterator_t<Base>();

  public:
    using iterator_concept  =
      conditional_t<forward_range<Base>, forward_iterator_tag, input_iterator_tag>;
    using iterator_category = input_iterator_tag;
    // [range.split.outer.value], class split_view::outer-iterator::value_type
    struct value_type;
    using difference_type   = range_difference_t<Base>;

    outer-iterator() = default;
    constexpr explicit outer-iterator(Parent& parent)
      requires (!forward_range<Base>);
    constexpr outer-iterator(Parent& parent, iterator_t<Base> current)
      requires forward_range<Base>;
    constexpr outer-iterator(outer-iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr value_type operator*() const;

    constexpr outer-iterator& operator++();
    constexpr decltype(auto) operator++(int) {
      if constexpr (forward_range<Base>) {
        auto tmp = *this;
        ++*this;
        return tmp;
      } else
        ++*this;
    }

    friend constexpr bool operator==(const outer-iterator& x, const outer-iterator& y)
      requires forward_range<Base>;

    friend constexpr bool operator==(const outer-iterator& x, default_sentinel_t);
  };
}
```

Many of the following specifications refer to the notional member
*current* of *outer-iterator*. *current* is equivalent to *current\_* if
`V` models `forward_range`, and `parent_->current_` otherwise.

``` cpp
constexpr explicit outer-iterator(Parent& parent)
  requires (!forward_range<Base>);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`.

``` cpp
constexpr outer-iterator(Parent& parent, iterator_t<Base> current)
  requires forward_range<Base>;
```

*Effects:* Initializes *parent\_* with `addressof(parent)` and
*current\_* with `std::move(current)`.

``` cpp
constexpr outer-iterator(outer-iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;
```

*Effects:* Initializes *parent\_* with `i.`*`parent_`* and *current\_*
with `std::move(i.`*`current_`*`)`.

``` cpp
constexpr value_type operator*() const;
```

*Effects:* Equivalent to: `return value_type{*this};`

``` cpp
constexpr outer-iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
const auto end = ranges::end(parent_->base_);
if (current == end) return *this;
const auto [pbegin, pend] = subrange{parent_->pattern_};
if (pbegin == pend) ++current;
else {
  do {
    auto [b, p] = ranges::mismatch(std::move(current), end, pbegin, pend);
    current = std::move(b);
    if (p == pend) {
      break;            // The pattern matched; skip it
    }
  } while (++current != end);
}
return *this;
```

``` cpp
friend constexpr bool operator==(const outer-iterator& x, const outer-iterator& y)
  requires forward_range<Base>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`current_`*`;`

``` cpp
friend constexpr bool operator==(const outer-iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to:
`return x.`*`current`*` == ranges::end(x.`*`parent_`*`->`*`base_`*`);`

#### Class `split_view::outer-iterator::value_type` <a id="range.split.outer.value">[[range.split.outer.value]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  template<bool Const>
  struct split_view<V, Pattern>::outer-iterator<Const>::value_type
    : view_interface<value_type> {
  private:
    outer-iterator i_ = outer-iterator();               // exposition only
  public:
    value_type() = default;
    constexpr explicit value_type(outer-iterator i);

    constexpr inner-iterator<Const> begin() const requires copyable<outer-iterator>;
    constexpr inner-iterator<Const> begin() requires (!copyable<outer-iterator>);
    constexpr default_sentinel_t end() const;
  };
}
```

``` cpp
constexpr explicit value_type(outer-iterator i);
```

*Effects:* Initializes *i\_* with `std::move(i)`.

``` cpp
constexpr inner-iterator<Const> begin() const requires copyable<outer-iterator>;
```

*Effects:* Equivalent to:
`return `*`inner-iterator`*`<Const>{`*`i_`*`};`

``` cpp
constexpr inner-iterator<Const> begin() requires (!copyable<outer-iterator>);
```

*Effects:* Equivalent to:
`return `*`inner-iterator`*`<Const>{std::move(`*`i_`*`)};`

``` cpp
constexpr default_sentinel_t end() const;
```

*Effects:* Equivalent to: `return default_sentinel;`

#### Class template `split_view::inner-iterator` <a id="range.split.inner">[[range.split.inner]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  template<bool Const>
  struct split_view<V, Pattern>::inner-iterator {
  private:
    using Base = conditional_t<Const, const V, V>;      // exposition only
    outer-iterator<Const> i_ = outer-iterator<Const>(); // exposition only
    bool incremented_ = false;                          // exposition only
  public:
    using iterator_concept  = typename outer-iterator<Const>::iterator_concept;
    using iterator_category = see below;
    using value_type        = range_value_t<Base>;
    using difference_type   = range_difference_t<Base>;

    inner-iterator() = default;
    constexpr explicit inner-iterator(outer-iterator<Const> i);

    constexpr decltype(auto) operator*() const { return *i_.current; }

    constexpr inner-iterator& operator++();
    constexpr decltype(auto) operator++(int) {
      if constexpr (forward_range<V>) {
        auto tmp = *this;
        ++*this;
        return tmp;
      } else
        ++*this;
    }

    friend constexpr bool operator==(const inner-iterator& x, const inner-iterator& y)
      requires forward_range<Base>;

    friend constexpr bool operator==(const inner-iterator& x, default_sentinel_t);

    friend constexpr decltype(auto) iter_move(const inner-iterator& i)
    noexcept(noexcept(ranges::iter_move(i.i_.current))) {
      return ranges::iter_move(i.i_.current);
    }

    friend constexpr void iter_swap(const inner-iterator& x, const inner-iterator& y)
      noexcept(noexcept(ranges::iter_swap(x.i_.current, y.i_.current)))
      requires indirectly_swappable<iterator_t<Base>>;
  };
}
```

The *typedef-name* `iterator_category` denotes:

- `forward_iterator_tag` if
  `iterator_traits<iterator_t<Base>>::iterator_category` models
  `derived_from<forward_iterator_tag>`;
- otherwise, `iterator_traits<iterator_t<Base>>::iterator_category`.

``` cpp
constexpr explicit inner-iterator(outer-iterator<Const> i);
```

*Effects:* Initializes *i\_* with `std::move(i)`.

``` cpp
constexpr inner-iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
incremented_ = true;
if constexpr (!forward_range<Base>) {
  if constexpr (Pattern::size() == 0) {
    return *this;
  }
}
++i_.current;
return *this;
```

``` cpp
friend constexpr bool operator==(const inner-iterator& x, const inner-iterator& y)
  requires forward_range<Base>;
```

*Effects:* Equivalent to:
`return x.`*`i_`*`.`*`current`*` == y.`*`i_`*`.`*`current`*`;`

``` cpp
friend constexpr bool operator==(const inner-iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to:

``` cpp
auto [pcur, pend] = subrange{x.i_.parent_->pattern_};
auto end = ranges::end(x.i_.parent_->base_);
if constexpr (tiny-range<Pattern>) {
  const auto & cur = x.i_.current;
  if (cur == end) return true;
  if (pcur == pend) return x.incremented_;
  return *cur == *pcur;
} else {
  auto cur = x.i_.current;
  if (cur == end) return true;
  if (pcur == pend) return x.incremented_;
  do {
    if (*cur != *pcur) return false;
    if (++pcur == pend) return true;
  } while (++cur != end);
  return false;
}
```

``` cpp
friend constexpr void iter_swap(const inner-iterator& x, const inner-iterator& y)
  noexcept(noexcept(ranges::iter_swap(x.i_.current, y.i_.current)))
  requires indirectly_swappable<iterator_t<Base>>;
```

*Effects:* Equivalent to
`ranges::iter_swap(x.`*`i_`*`.`*`current`*`, y.`*`i_`*`.`*`current`*`)`.

### Counted view <a id="range.counted">[[range.counted]]</a>

A counted view presents a `view` of the elements of the counted range
[[iterator.requirements.general]] `i`+\[0, `n`) for an iterator `i` and
non-negative integer `n`.

The name `views::counted` denotes a customization point object
[[customization.point.object]]. Let `E` and `F` be expressions, let `T`
be `decay_t<decltype((E))>`, and let `D` be `iter_difference_t<T>`. If
`decltype((F))` does not model `convertible_to<D>`,
`views::counted(E, F)` is ill-formed.

[*Note 1*: This case can result in substitution failure when
`views::counted(E, F)` appears in the immediate context of a template
instantiation. — *end note*\]

Otherwise, `views::counted(E, F)` is expression-equivalent to:

- If `T` models `contiguous_iterator`, then
  `span{to_address(E), static_cast<D>(F)}`.
- Otherwise, if `T` models `random_access_iterator`, then
  `subrange{E, E + static_cast<D>(F)}`, except that `E` is evaluated
  only once.
- Otherwise, `subrange{counted_iterator{E, F}, default_sentinel}`.

### Common view <a id="range.common">[[range.common]]</a>

#### Overview <a id="range.common.overview">[[range.common.overview]]</a>

`common_view` takes a `view` which has different types for its iterator
and sentinel and turns it into a `view` of the same elements with an
iterator and sentinel of the same type.

[*Note 1*: `common_view` is useful for calling legacy algorithms that
expect a range’s iterator and sentinel types to be the
same. — *end note*\]

The name `views::common` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::common(E)` is expression-equivalent to:

- `views::all(E)`, if `decltype((E))` models `common_range` and
  `views::all(E)` is a well-formed expression.
- Otherwise, `common_view{E}`.

[*Example 1*:

``` cpp
// Legacy algorithm:
template<class ForwardIterator>
size_t count(ForwardIterator first, ForwardIterator last);

template<forward_range R>
void my_algo(R&& r) {
  auto&& common = common_view{r};
  auto cnt = count(common.begin(), common.end());
  // ...
}
```

— *end example*\]

#### Class template `common_view` <a id="range.common.view">[[range.common.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires (!common_range<V> && copyable<iterator_t<V>>)
  class common_view : public view_interface<common_view<V>> {
  private:
    V base_ = V();  // exposition only
  public:
    common_view() = default;

    constexpr explicit common_view(V r);

    template<viewable_range R>
      requires (!common_range<R> && constructible_from<V, views::all_t<R>>)
    constexpr explicit common_view(R&& r);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() {
      if constexpr (random_access_range<V> && sized_range<V>)
        return ranges::begin(base_);
      else
        return common_iterator<iterator_t<V>, sentinel_t<V>>(ranges::begin(base_));
    }

    constexpr auto begin() const requires range<const V> {
      if constexpr (random_access_range<const V> && sized_range<const V>)
        return ranges::begin(base_);
      else
        return common_iterator<iterator_t<const V>, sentinel_t<const V>>(ranges::begin(base_));
    }

    constexpr auto end() {
      if constexpr (random_access_range<V> && sized_range<V>)
        return ranges::begin(base_) + ranges::size(base_);
      else
        return common_iterator<iterator_t<V>, sentinel_t<V>>(ranges::end(base_));
    }

    constexpr auto end() const requires range<const V> {
      if constexpr (random_access_range<const V> && sized_range<const V>)
        return ranges::begin(base_) + ranges::size(base_);
      else
        return common_iterator<iterator_t<const V>, sentinel_t<const V>>(ranges::end(base_));
    }

    constexpr auto size() requires sized_range<V> {
      return ranges::size(base_);
    }
    constexpr auto size() const requires sized_range<const V> {
      return ranges::size(base_);
    }
  };

  template<class R>
    common_view(R&&) -> common_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit common_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

``` cpp
template<viewable_range R>
  requires (!common_range<R> && constructible_from<V, views::all_t<R>>)
constexpr explicit common_view(R&& r);
```

*Effects:* Initializes *base\_* with `views::all(std::forward<R>(r))`.

### Reverse view <a id="range.reverse">[[range.reverse]]</a>

#### Overview <a id="range.reverse.overview">[[range.reverse.overview]]</a>

`reverse_view` takes a bidirectional `view` and produces another `view`
that iterates the same elements in reverse order.

The name `views::reverse` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::reverse(E)` is expression-equivalent to:

- If the type of `E` is a (possibly cv-qualified) specialization of
  `reverse_view`, equivalent to `E.base()`.
- Otherwise, if the type of `E` is cv-qualified
  ``` cpp
  subrange<reverse_iterator<I>, reverse_iterator<I>, K>
  ```

  for some iterator type `I` and value `K` of type `subrange_kind`,
  - if `K` is `subrange_kind::sized`, equivalent to:
    ``` cpp
    subrange<I, I, K>(E.end().base(), E.begin().base(), E.size())
    ```
  - otherwise, equivalent to:
    ``` cpp
    subrange<I, I, K>(E.end().base(), E.begin().base())
    ```

  However, in either case `E` is evaluated only once.
- Otherwise, equivalent to `reverse_view{E}`.

[*Example 1*:

``` cpp
vector<int> is {0,1,2,3,4};
reverse_view rv {is};
for (int i : rv)
  cout << i << ' '; // prints: 4 3 2 1 0
```

— *end example*\]

#### Class template `reverse_view` <a id="range.reverse.view">[[range.reverse.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires bidirectional_range<V>
  class reverse_view : public view_interface<reverse_view<V>> {
  private:
    V base_ = V();  // exposition only
  public:
    reverse_view() = default;

    constexpr explicit reverse_view(V r);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr reverse_iterator<iterator_t<V>> begin();
    constexpr reverse_iterator<iterator_t<V>> begin() requires common_range<V>;
    constexpr auto begin() const requires common_range<const V>;

    constexpr reverse_iterator<iterator_t<V>> end();
    constexpr auto end() const requires common_range<const V>;

    constexpr auto size() requires sized_range<V> {
      return ranges::size(base_);
    }
    constexpr auto size() const requires sized_range<const V> {
      return ranges::size(base_);
    }
  };

  template<class R>
    reverse_view(R&&) -> reverse_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit reverse_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

``` cpp
constexpr reverse_iterator<iterator_t<V>> begin();
```

*Returns:*

``` cpp
make_reverse_iterator(ranges::next(ranges::begin(base_), ranges::end(base_)))
```

*Remarks:* In order to provide the amortized constant time complexity
required by the `range` concept, this function caches the result within
the `reverse_view` for use on subsequent calls.

``` cpp
constexpr reverse_iterator<iterator_t<V>> begin() requires common_range<V>;
constexpr auto begin() const requires common_range<const V>;
```

*Effects:* Equivalent to:
`return make_reverse_iterator(ranges::end(base_));`

``` cpp
constexpr reverse_iterator<iterator_t<V>> end();
constexpr auto end() const requires common_range<const V>;
```

*Effects:* Equivalent to:
`return make_reverse_iterator(ranges::begin(base_));`

### Elements view <a id="range.elements">[[range.elements]]</a>

#### Overview <a id="range.elements.overview">[[range.elements.overview]]</a>

`elements_view` takes a `view` of tuple-like values and a `size_t`, and
produces a `view` with a value-type of the Nᵗʰ element of the adapted
`view`’s value-type.

The name `views::elements<N>` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E` and constant
expression `N`, the expression `views::elements<N>(E)` is
expression-equivalent to
`elements_view<views::all_t<decltype((E))>, N>{E}`.

[*Example 1*:

``` cpp
auto historical_figures = map{
  {"Lovelace"sv, 1815},
  {"Turing"sv, 1912},
  {"Babbage"sv, 1791},
  {"Hamilton"sv, 1936}
};

auto names = historical_figures | views::elements<0>;
for (auto&& name : names) {
  cout << name << ' ';          // prints Babbage Hamilton Lovelace Turing
}

auto birth_years = historical_figures | views::elements<1>;
for (auto&& born : birth_years) {
  cout << born << ' ';          // prints 1791 1936 1815 1912
}
```

— *end example*\]

`keys_view` is an alias for `elements_view<views::all_t<R>, 0>`, and is
useful for extracting keys from associative containers.

[*Example 2*:

``` cpp
auto names = keys_view{historical_figures};
for (auto&& name : names) {
  cout << name << ' ';          // prints Babbage Hamilton Lovelace Turing
}
```

— *end example*\]

`values_view` is an alias for `elements_view<views::all_t<R>, 1>`, and
is useful for extracting values from associative containers.

[*Example 3*:

``` cpp
auto is_even = [](const auto x) { return x % 2 == 0; };
cout << ranges::count_if(values_view{historical_figures}, is_even);     // prints 2
```

— *end example*\]

#### Class template `elements_view` <a id="range.elements.view">[[range.elements.view]]</a>

``` cpp
namespace std::ranges {
  template<class T, size_t N>
  concept has-tuple-element =                   // exposition only
    requires(T t) {
      typename tuple_size<T>::type;
      requires N < tuple_size_v<T>;
      typename tuple_element_t<N, T>;
      { get<N>(t) } -> convertible_to<const tuple_element_t<N, T>&>;
    };


  template<input_range V, size_t N>
    requires view<V> && has-tuple-element<range_value_t<V>, N> &&
             has-tuple-element<remove_reference_t<range_reference_t<V>>, N>
  class elements_view : public view_interface<elements_view<V, N>> {
  public:
    elements_view() = default;
    constexpr explicit elements_view(V base);

    constexpr V base() const& requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>)
    { return iterator<false>(ranges::begin(base_)); }

    constexpr auto begin() const requires simple-view<V>
    { return iterator<true>(ranges::begin(base_)); }

    constexpr auto end()
    { return sentinel<false>{ranges::end(base_)}; }

    constexpr auto end() requires common_range<V>
    { return iterator<false>{ranges::end(base_)}; }

    constexpr auto end() const requires range<const V>
    { return sentinel<true>{ranges::end(base_)}; }

    constexpr auto end() const requires common_range<const V>
    { return iterator<true>{ranges::end(base_)}; }

    constexpr auto size() requires sized_range<V>
    { return ranges::size(base_); }

    constexpr auto size() const requires sized_range<const V>
    { return ranges::size(base_); }

  private:
    // [range.elements.iterator], class template elements_view::iterator
    template<bool> struct iterator;                     // exposition only
    // [range.elements.sentinel], class template elements_view::sentinel
    template<bool> struct sentinel;                     // exposition only
    V base_ = V();                                      // exposition only
  };
}
```

``` cpp
constexpr explicit elements_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

#### Class template `elements_view::iterator` <a id="range.elements.iterator">[[range.elements.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, size_t N>
    requires view<V> && has-tuple-element<range_value_t<V>, N> &&
             has-tuple-element<remove_reference_t<range_reference_t<V>>, N>
  template<bool Const>
  class elements_view<V, N>::iterator {                 // exposition only
    using Base = conditional_t<Const, const V, V>;      // exposition only

    iterator_t<Base> current_ = iterator_t<Base>();
  public:
    using iterator_category = typename iterator_traits<iterator_t<Base>>::iterator_category;
    using value_type = remove_cvref_t<tuple_element_t<N, range_value_t<Base>>>;
    using difference_type = range_difference_t<Base>;

    iterator() = default;
    constexpr explicit iterator(iterator_t<Base> current);
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr iterator_t<Base> base() const&
      requires copyable<iterator_t<Base>>;
    constexpr iterator_t<Base> base() &&;

    constexpr decltype(auto) operator*() const
    { return get<N>(*current_); }

    constexpr iterator& operator++();
    constexpr void operator++(int) requires (!forward_range<Base>);
    constexpr iterator operator++(int) requires forward_range<Base>;

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x)
      requires random_access_range<Base>;

    constexpr decltype(auto) operator[](difference_type n) const
      requires random_access_range<Base>
    { return get<N>(*(current_ + n)); }

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<iterator_t<Base>>;

    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator<=(const iterator& y, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base> && three_way_comparable<iterator_t<Base>>;

    friend constexpr iterator operator+(const iterator& x, difference_type y)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& x, difference_type y)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
  };
}
```

``` cpp
constexpr explicit iterator(iterator_t<Base> current);
```

*Effects:* Initializes *current\_* with `std::move(current)`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`.

``` cpp
constexpr iterator_t<Base> base() const&
  requires copyable<iterator_t<Base>>;
```

*Effects:* Equivalent to: `return `*`current_`*`;`

``` cpp
constexpr iterator_t<Base> base() &&;
```

*Effects:* Equivalent to: `return std::move(`*`current_`*`);`

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++current_;
return *this;
```

``` cpp
constexpr void operator++(int) requires (!forward_range<Base>);
```

*Effects:* Equivalent to: `++`*`current_`*.

``` cpp
constexpr iterator operator++(int) requires forward_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto temp = *this;
++current_;
return temp;
```

``` cpp
constexpr iterator& operator--() requires bidirectional_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
--current_;
return *this;
```

``` cpp
constexpr iterator operator--(int) requires bidirectional_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto temp = *this;
--current_;
return temp;
```

``` cpp
constexpr iterator& operator+=(difference_type n);
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
current_ += n;
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
current_ -= n;
return *this;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires equality_comparable<Base>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`current_`*`;`

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` < y.`*`current_`*`;`

``` cpp
friend constexpr bool operator>(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return y < x;`

``` cpp
friend constexpr bool operator<=(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return !(y < x);`

``` cpp
friend constexpr bool operator>=(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return !(x < y);`

``` cpp
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires random_access_range<Base> && three_way_comparable<iterator_t<Base>>;
```

*Effects:* Equivalent to:
`return x.`*`current_`*` <=> y.`*`current_`*`;`

``` cpp
friend constexpr iterator operator+(const iterator& x, difference_type y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return iterator{x} += y;`

``` cpp
friend constexpr iterator operator+(difference_type x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return y + x;`

``` cpp
constexpr iterator operator-(const iterator& x, difference_type y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return iterator{x} -= y;`

``` cpp
constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`current_`*`;`

#### Class template `elements_view::sentinel` <a id="range.elements.sentinel">[[range.elements.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, size_t N>
    requires view<V> && has-tuple-element<range_value_t<V>, N> &&
             has-tuple-element<remove_reference_t<range_reference_t<V>>, N>
  template<bool Const>
  class elements_view<V, N>::sentinel {                 // exposition only
  private:
    using Base = conditional_t<Const, const V, V>;      // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only
  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end);
    constexpr sentinel(sentinel<!Const> other)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    friend constexpr bool operator==(const iterator<Const>& x, const sentinel& y);

    friend constexpr range_difference_t<Base>
      operator-(const iterator<Const>& x, const sentinel& y)
        requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;

    friend constexpr range_difference_t<Base>
      operator-(const sentinel& x, const iterator<Const>& y)
        requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
  };
}
```

``` cpp
constexpr explicit sentinel(sentinel_t<Base> end);
```

*Effects:* Initializes *end\_* with `end`.

``` cpp
constexpr sentinel(sentinel<!Const> other)
  requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *end\_* with `std::move(other.`*`end_`*`)`.

``` cpp
constexpr sentinel_t<Base> base() const;
```

*Effects:* Equivalent to: `return `*`end_`*`;`

``` cpp
friend constexpr bool operator==(const iterator<Const>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`end_`*`;`

``` cpp
friend constexpr range_difference_t<Base>
  operator-(const iterator<Const>& x, const sentinel& y)
    requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`end_`*`;`

``` cpp
friend constexpr range_difference_t<Base>
  operator-(const sentinel& x, const iterator<Const>& y)
    requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return x.`*`end_`*` - y.`*`current_`*`;`

<!-- Section link definitions -->
[range.access]: #range.access
[range.access.begin]: #range.access.begin
[range.access.cbegin]: #range.access.cbegin
[range.access.cend]: #range.access.cend
[range.access.crbegin]: #range.access.crbegin
[range.access.crend]: #range.access.crend
[range.access.end]: #range.access.end
[range.access.rbegin]: #range.access.rbegin
[range.access.rend]: #range.access.rend
[range.adaptor.object]: #range.adaptor.object
[range.adaptors]: #range.adaptors
[range.all]: #range.all
[range.common]: #range.common
[range.common.overview]: #range.common.overview
[range.common.view]: #range.common.view
[range.counted]: #range.counted
[range.dangling]: #range.dangling
[range.drop]: #range.drop
[range.drop.overview]: #range.drop.overview
[range.drop.view]: #range.drop.view
[range.drop.while]: #range.drop.while
[range.drop.while.overview]: #range.drop.while.overview
[range.drop.while.view]: #range.drop.while.view
[range.elements]: #range.elements
[range.elements.iterator]: #range.elements.iterator
[range.elements.overview]: #range.elements.overview
[range.elements.sentinel]: #range.elements.sentinel
[range.elements.view]: #range.elements.view
[range.empty]: #range.empty
[range.empty.overview]: #range.empty.overview
[range.empty.view]: #range.empty.view
[range.factories]: #range.factories
[range.filter]: #range.filter
[range.filter.iterator]: #range.filter.iterator
[range.filter.overview]: #range.filter.overview
[range.filter.sentinel]: #range.filter.sentinel
[range.filter.view]: #range.filter.view
[range.iota]: #range.iota
[range.iota.iterator]: #range.iota.iterator
[range.iota.overview]: #range.iota.overview
[range.iota.sentinel]: #range.iota.sentinel
[range.iota.view]: #range.iota.view
[range.istream]: #range.istream
[range.istream.iterator]: #range.istream.iterator
[range.istream.overview]: #range.istream.overview
[range.istream.view]: #range.istream.view
[range.join]: #range.join
[range.join.iterator]: #range.join.iterator
[range.join.overview]: #range.join.overview
[range.join.sentinel]: #range.join.sentinel
[range.join.view]: #range.join.view
[range.prim.cdata]: #range.prim.cdata
[range.prim.data]: #range.prim.data
[range.prim.empty]: #range.prim.empty
[range.prim.size]: #range.prim.size
[range.prim.ssize]: #range.prim.ssize
[range.range]: #range.range
[range.ref.view]: #range.ref.view
[range.refinements]: #range.refinements
[range.req]: #range.req
[range.req.general]: #range.req.general
[range.reverse]: #range.reverse
[range.reverse.overview]: #range.reverse.overview
[range.reverse.view]: #range.reverse.view
[range.semi.wrap]: #range.semi.wrap
[range.single]: #range.single
[range.single.overview]: #range.single.overview
[range.single.view]: #range.single.view
[range.sized]: #range.sized
[range.split]: #range.split
[range.split.inner]: #range.split.inner
[range.split.outer]: #range.split.outer
[range.split.outer.value]: #range.split.outer.value
[range.split.overview]: #range.split.overview
[range.split.view]: #range.split.view
[range.subrange]: #range.subrange
[range.subrange.access]: #range.subrange.access
[range.subrange.ctor]: #range.subrange.ctor
[range.take]: #range.take
[range.take.overview]: #range.take.overview
[range.take.sentinel]: #range.take.sentinel
[range.take.view]: #range.take.view
[range.take.while]: #range.take.while
[range.take.while.overview]: #range.take.while.overview
[range.take.while.sentinel]: #range.take.while.sentinel
[range.take.while.view]: #range.take.while.view
[range.transform]: #range.transform
[range.transform.iterator]: #range.transform.iterator
[range.transform.overview]: #range.transform.overview
[range.transform.sentinel]: #range.transform.sentinel
[range.transform.view]: #range.transform.view
[range.utility]: #range.utility
[range.utility.helpers]: #range.utility.helpers
[range.view]: #range.view
[ranges]: #ranges
[ranges.general]: #ranges.general
[ranges.syn]: #ranges.syn
[view.interface]: #view.interface
[view.interface.members]: #view.interface.members

<!-- Link reference definitions -->
[basic.compound]: basic.md#basic.compound
[concepts.equality]: concepts.md#concepts.equality
[containers]: containers.md#containers
[conv.rval]: expr.md#conv.rval
[customization.point.object]: library.md#customization.point.object
[dcl.array]: dcl.md#dcl.array
[expr.const]: expr.md#expr.const
[iterator.concept.bidir]: iterators.md#iterator.concept.bidir
[iterator.concept.iterator]: iterators.md#iterator.concept.iterator
[iterator.concept.output]: iterators.md#iterator.concept.output
[iterator.concept.random.access]: iterators.md#iterator.concept.random.access
[iterator.concept.sizedsentinel]: iterators.md#iterator.concept.sizedsentinel
[iterator.concept.winc]: iterators.md#iterator.concept.winc
[iterator.requirements.general]: iterators.md#iterator.requirements.general
[namespace.std]: library.md#namespace.std
[range.access]: #range.access
[range.adaptor.object]: #range.adaptor.object
[range.adaptors]: #range.adaptors
[range.empty.view]: #range.empty.view
[range.factories]: #range.factories
[range.iota.view]: #range.iota.view
[range.prim.data]: #range.prim.data
[range.range]: #range.range
[range.req]: #range.req
[range.sized]: #range.sized
[range.subrange]: #range.subrange
[range.summary]: #range.summary
[range.utility]: #range.utility
[ranges.syn]: #ranges.syn
[string.view]: strings.md#string.view
[views.span]: containers.md#views.span
