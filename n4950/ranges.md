# Ranges library <a id="ranges">[[ranges]]</a>

## General <a id="ranges.general">[[ranges.general]]</a>

This Clause describes components for dealing with ranges of elements.

The following subclauses describe range and view requirements, and
components for range primitives and range generators as summarized in
[[range.summary]].

**Table: Ranges library summary**

| Subclause           |                  | Header        |
| ------------------- | ---------------- | ------------- |
| [[range.access]]    | Range access     | `<ranges>`    |
| [[range.req]]       | Requirements     |               |
| [[range.utility]]   | Range utilities  |               |
| [[range.factories]] | Range factories  |               |
| [[range.adaptors]]  | Range adaptors   |               |
| [[coro.generator]]  | Range generators | `<generator>` |


## Header `<ranges>` synopsis <a id="ranges.syn">[[ranges.syn]]</a>

``` cpp
#include <compare>              // see [compare.syn]
#include <initializer_list>     // see [initializer.list.syn]
#include <iterator>             // see [iterator.synopsis]

namespace std::ranges {
  inline namespace unspecified {
    // [range.access], range access
    inline constexpr unspecified begin = unspecified;                               // freestanding
    inline constexpr unspecified end = unspecified;                                 // freestanding
    inline constexpr unspecified cbegin = unspecified;                              // freestanding
    inline constexpr unspecified cend = unspecified;                                // freestanding
    inline constexpr unspecified rbegin = unspecified;                              // freestanding
    inline constexpr unspecified rend = unspecified;                                // freestanding
    inline constexpr unspecified crbegin = unspecified;                             // freestanding
    inline constexpr unspecified crend = unspecified;                               // freestanding

    inline constexpr unspecified size = unspecified;                                // freestanding
    inline constexpr unspecified ssize = unspecified;                               // freestanding
    inline constexpr unspecified empty = unspecified;                               // freestanding
    inline constexpr unspecified data = unspecified;                                // freestanding
    inline constexpr unspecified cdata = unspecified;                               // freestanding
  }

  // [range.range], ranges
  template<class T>
    concept range = see below;                                                      // freestanding

  template<class T>
    constexpr bool enable_borrowed_range = false;                                   // freestanding

  template<class T>
    concept borrowed_range = see below;                                             // freestanding

  template<class T>
    using iterator_t = decltype(ranges::begin(declval<T&>()));                      // freestanding
  template<range R>
    using sentinel_t = decltype(ranges::end(declval<R&>()));                        // freestanding
  template<range R>
    using const_iterator_t = const_iterator<iterator_t<R>>;                         // freestanding
  template<range R>
    using const_sentinel_t = const_sentinel<sentinel_t<R>>;                         // freestanding
  template<range R>
    using range_difference_t = iter_difference_t<iterator_t<R>>;                    // freestanding
  template<sized_range R>
    using range_size_t = decltype(ranges::size(declval<R&>()));                     // freestanding
  template<range R>
    using range_value_t = iter_value_t<iterator_t<R>>;                              // freestanding
  template<range R>
    using range_reference_t = iter_reference_t<iterator_t<R>>;                      // freestanding
  template<range R>
    using range_const_reference_t = iter_const_reference_t<iterator_t<R>>;          // freestanding
  template<range R>
    using range_rvalue_reference_t = iter_rvalue_reference_t<iterator_t<R>>;        // freestanding
  template<range R>
    using range_common_reference_t = iter_common_reference_t<iterator_t<R>>;        // freestanding

  // [range.sized], sized ranges
  template<class>
    constexpr bool disable_sized_range = false;                                     // freestanding

  template<class T>
    concept sized_range = see below;                                                // freestanding

  // [range.view], views
  template<class T>
    constexpr bool enable_view = see below;                                         // freestanding

  struct view_base {};                                                              // freestanding

  template<class T>
    concept view = see below;                                                       // freestanding

  // [range.refinements], other range refinements
  template<class R, class T>
    concept output_range = see below;                                               // freestanding

  template<class T>
    concept input_range = see below;                                                // freestanding

  template<class T>
    concept forward_range = see below;                                              // freestanding

  template<class T>
    concept bidirectional_range = see below;                                        // freestanding

  template<class T>
    concept random_access_range = see below;                                        // freestanding

  template<class T>
    concept contiguous_range = see below;                                           // freestanding

  template<class T>
    concept common_range = see below;                                               // freestanding

  template<class T>
    concept viewable_range = see below;                                             // freestanding

  template<class T>
    concept constant_range = see below;                                             // freestanding

  // [view.interface], class template view_interface
  template<class D>
    requires is_class_v<D> && same_as<D, remove_cv_t<D>>
  class view_interface;                                                             // freestanding

  // [range.subrange], sub-ranges
  enum class subrange_kind : bool { unsized, sized };                               // freestanding

  template<input_or_output_iterator I, sentinel_for<I> S = I, subrange_kind K = see below>
    requires (K == subrange_kind::sized || !sized_sentinel_for<S, I>)
  class subrange;                                                                   // freestanding

  template<class I, class S, subrange_kind K>
    constexpr bool enable_borrowed_range<subrange<I, S, K>> = true;                 // freestanding

  template<size_t N, class I, class S, subrange_kind K>
    requires ((N == 0 && copyable<I>) || N == 1)
    constexpr auto get(const subrange<I, S, K>& r);                                 // freestanding

  template<size_t N, class I, class S, subrange_kind K>
    requires (N < 2)
    constexpr auto get(subrange<I, S, K>&& r);                                      // freestanding
}

namespace std {
  using ranges::get;                                                                // freestanding
}

namespace std::ranges {
  // [range.dangling], dangling iterator handling
  struct dangling;                                                                  // freestanding

  // [range.elementsof], class template elements_of
  template<range R, class Allocator = allocator<byte>>
    struct elements_of;

  template<range R>
    using borrowed_iterator_t = see below;                                          // freestanding

  template<range R>
    using borrowed_subrange_t = see below;                                          // freestanding

  // [range.utility.conv], range conversions
  template<class C, input_range R, class... Args> requires (!view<C>)
    constexpr C to(R&& r, Args&&... args);                                          // freestanding
  template<template<class...> class C, input_range R, class... Args>
    constexpr auto to(R&& r, Args&&... args);                                       // freestanding
  template<class C, class... Args> requires (!view<C>)
    constexpr auto to(Args&&... args);                                              // freestanding
  template<template<class...> class C, class... Args>
    constexpr auto to(Args&&... args);                                              // freestanding

  // [range.empty], empty view
  template<class T>
    requires is_object_v<T>
  class empty_view;                                                                 // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<empty_view<T>> = true;                     // freestanding

  namespace views {
    template<class T>
      constexpr empty_view<T> empty{};                                              // freestanding
  }

  // [range.single], single view
  template<move_constructible T>
    requires is_object_v<T>
  class single_view;                                                                // freestanding

  namespace views { inline constexpr unspecified single = unspecified; }            // freestanding

  template<bool Const, class T>
    using maybe-const = conditional_t<Const, const T, T>;   // exposition only

  // [range.iota], iota view
  template<weakly_incrementable W, semiregular Bound = unreachable_sentinel_t>
    requires weakly-equality-comparable-with<W, Bound> && copyable<W>
  class iota_view;                                                                  // freestanding

  template<class W, class Bound>
    constexpr bool enable_borrowed_range<iota_view<W, Bound>> = true;               // freestanding

  namespace views { inline constexpr unspecified iota = unspecified; }              // freestanding

  // [range.repeat], repeat view
  template<move_constructible T, semiregular Bound = unreachable_sentinel_t>
    requires see below
  class repeat_view;                                                                // freestanding

  namespace views { inline constexpr unspecified repeat = unspecified; }            // freestanding

  // [range.istream], istream view
  template<movable Val, class CharT, class Traits = char_traits<CharT>>
    requires see below
  class basic_istream_view;
  template<class Val>
    using istream_view = basic_istream_view<Val, char>;
  template<class Val>
    using wistream_view = basic_istream_view<Val, wchar_t>;

  namespace views { template<class T> constexpr unspecified istream = unspecified; }

  // [range.adaptor.object], range adaptor objects
  template<class D>
    requires is_class_v<D> && same_as<D, remove_cv_t<D>>
  class range_adaptor_closure { };                                                  // freestanding

  // [range.all], all view
  namespace views {
    inline constexpr unspecified all = unspecified;                                 // freestanding

    template<viewable_range R>
      using all_t = decltype(all(declval<R>()));                                    // freestanding
  }

  // [range.ref.view], ref view
  template<range R>
    requires is_object_v<R>
  class ref_view;                                                                   // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<ref_view<T>> = true;                       // freestanding

  // [range.owning.view], owning view
  template<range R>
    requires see below
  class owning_view;                                                                // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<owning_view<T>> =                          // freestanding
      enable_borrowed_range<T>;

  // [range.as.rvalue], as rvalue view
  template<view V>
    requires input_range<V>
  class as_rvalue_view;                                                             // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<as_rvalue_view<T>> =                       // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified as_rvalue = unspecified; }         // freestanding

  // [range.filter], filter view
  template<input_range V, indirect_unary_predicate<iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class filter_view;                                                                // freestanding

  namespace views { inline constexpr unspecified filter = unspecified; }            // freestanding

  // [range.transform], transform view
  template<input_range V, move_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>> &&
             can-reference<invoke_result_t<F&, range_reference_t<V>>>
  class transform_view;                                                             // freestanding

  namespace views { inline constexpr unspecified transform = unspecified; }         // freestanding

  // [range.take], take view
  template<view> class take_view;                                                   // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<take_view<T>> =                            // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified take = unspecified; }              // freestanding

  // [range.take.while], take while view
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
    class take_while_view;                                                          // freestanding

  namespace views { inline constexpr unspecified take_while = unspecified; }        // freestanding

  // [range.drop], drop view
  template<view V>
    class drop_view;                                                                // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<drop_view<T>> =                            // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified drop = unspecified; }              // freestanding

  // [range.drop.while], drop while view
  template<view V, class Pred>
    requires input_range<V> && is_object_v<Pred> &&
             indirect_unary_predicate<const Pred, iterator_t<V>>
    class drop_while_view;                                                          // freestanding

  template<class T, class Pred>
    constexpr bool enable_borrowed_range<drop_while_view<T, Pred>> =                // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified drop_while = unspecified; }        // freestanding

  // [range.join], join view
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>>
  class join_view;                                                                  // freestanding

  namespace views { inline constexpr unspecified join = unspecified; }              // freestanding

  // [range.join.with], join with view
  template<class R, class P>
    concept compatible-joinable-ranges = see below; // exposition only

  template<input_range V, forward_range Pattern>
    requires view<V> && input_range<range_reference_t<V>>
          && view<Pattern>
          && compatible-joinable-ranges<range_reference_t<V>, Pattern>
  class join_with_view;                                                             // freestanding

  namespace views { inline constexpr unspecified join_with = unspecified; }         // freestanding

  // [range.lazy.split], lazy split view
  template<class R>
    concept tiny-range = see below;   // exposition only

  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  class lazy_split_view;                                                            // freestanding

  // [range.split], split view
 template<forward_range V, forward_range Pattern>
   requires view<V> && view<Pattern> &&
            indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to>
  class split_view;                                                                 // freestanding

  namespace views {
    inline constexpr unspecified lazy_split = unspecified;                          // freestanding
    inline constexpr unspecified split = unspecified;                               // freestanding
  }

  // [range.counted], counted view
  namespace views { inline constexpr unspecified counted = unspecified; }           // freestanding

  // [range.common], common view
  template<view V>
    requires (!common_range<V> && copyable<iterator_t<V>>)
  class common_view;                                                                // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<common_view<T>> =                          // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified common = unspecified; }            // freestanding

  // [range.reverse], reverse view
  template<view V>
    requires bidirectional_range<V>
  class reverse_view;                                                               // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<reverse_view<T>> =                         // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified reverse = unspecified; }           // freestanding

  // [range.as.const], as const view
  template<input_range R>
    constexpr auto& possibly-const-range(R& r) {          // exposition only
      if constexpr (constant_range<const R> && !constant_range<R>) {
        return const_cast<const R&>(r);
      } else {
        return r;
      }
    }

  template<view V>
    requires input_range<V>
  class as_const_view;                                                              // freestanding

  template<class T>
    constexpr bool enable_borrowed_range<as_const_view<T>> =                        // freestanding
      enable_borrowed_range<T>;

  namespace views { inline constexpr unspecified as_const = unspecified; }          // freestanding

  // [range.elements], elements view
  template<input_range V, size_t N>
    requires see below
  class elements_view;                                                              // freestanding

  template<class T, size_t N>
    constexpr bool enable_borrowed_range<elements_view<T, N>> =                     // freestanding
      enable_borrowed_range<T>;

  template<class R>
    using keys_view = elements_view<R, 0>;                                          // freestanding
  template<class R>
    using values_view = elements_view<R, 1>;                                        // freestanding

  namespace views {
    template<size_t N>
      constexpr unspecified elements = unspecified;                                 // freestanding
    inline constexpr auto keys = elements<0>;                                       // freestanding
    inline constexpr auto values = elements<1>;                                     // freestanding
  }

  // [range.enumerate], enumerate view
  template<input_range View>
    requires view<View>
  class enumerate_view;                                                             // freestanding

  template<class View>
    constexpr bool enable_borrowed_range<enumerate_view<View>> =                    // freestanding
      enable_borrowed_range<View>;

  namespace views { inline constexpr unspecified enumerate = unspecified; }         // freestanding

  // [range.zip], zip view
  template<input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0)
  class zip_view;                                                                   // freestanding

  template<class... Views>
    constexpr bool enable_borrowed_range<zip_view<Views...>> =                      // freestanding
      (enable_borrowed_range<Views> && ...);

  namespace views { inline constexpr unspecified zip = unspecified; }               // freestanding

  // [range.zip.transform], zip transform view
  template<move_constructible F, input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0) && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<Views>...> &&
             can-reference<invoke_result_t<F&, range_reference_t<Views>...>>
  class zip_transform_view;                                                         // freestanding

  namespace views { inline constexpr unspecified zip_transform = unspecified; }     // freestanding

  // [range.adjacent], adjacent view
  template<forward_range V, size_t N>
    requires view<V> && (N > 0)
  class adjacent_view;                                                              // freestanding

  template<class V, size_t N>
    constexpr bool enable_borrowed_range<adjacent_view<V, N>> =                     // freestanding
      enable_borrowed_range<V>;

  namespace views {
    template<size_t N>
      constexpr unspecified adjacent = unspecified;                                 // freestanding
    inline constexpr auto pairwise = adjacent<2>;                                   // freestanding
  }

  // [range.adjacent.transform], adjacent transform view
  template<forward_range V, move_constructible F, size_t N>
    requires see below
  class adjacent_transform_view;                                                    // freestanding

  namespace views {
    template<size_t N>
      constexpr unspecified adjacent_transform = unspecified;                       // freestanding
    inline constexpr auto pairwise_transform = adjacent_transform<2>;               // freestanding
  }

  // [range.chunk], chunk view
  template<view V>
    requires input_range<V>
  class chunk_view;                                                                 // freestanding

  template<view V>
    requires forward_range<V>
  class chunk_view<V>;                                                              // freestanding

  template<class V>
    constexpr bool enable_borrowed_range<chunk_view<V>> =                           // freestanding
      forward_range<V> && enable_borrowed_range<V>;

  namespace views { inline constexpr unspecified chunk = unspecified; }             // freestanding

  // [range.slide], slide view
  template<forward_range V>
    requires view<V>
  class slide_view;                                                                 // freestanding

  template<class V>
    constexpr bool enable_borrowed_range<slide_view<V>> =
      enable_borrowed_range<V>;                                                     // freestanding

  namespace views { inline constexpr unspecified slide = unspecified; }             // freestanding

  // [range.chunk.by], chunk by view
  template<forward_range V, indirect_binary_predicate<iterator_t<V>, iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class chunk_by_view;                                                              // freestanding

  namespace views { inline constexpr unspecified chunk_by = unspecified; }          // freestanding

  // [range.stride], stride view
  template<input_range V>
    requires view<V>
  class stride_view;                                                                // freestanding

  template<class V>
    constexpr bool enable_borrowed_range<stride_view<V>> =                          // freestanding
      enable_borrowed_range<V>;

  namespace views { inline constexpr unspecified stride = unspecified; }            // freestanding

  // [range.cartesian], cartesian product view
  template<input_range First, forward_range... Vs>
    requires (view<First> && ... && view<Vs>)
  class cartesian_product_view;                                                     // freestanding

  namespace views { inline constexpr unspecified cartesian_product = unspecified; } // freestanding
}

namespace std {
  namespace views = ranges::views;                                                  // freestanding

  template<class T> struct tuple_size;                                              // freestanding
  template<size_t I, class T> struct tuple_element;                                 // freestanding

  template<class I, class S, ranges::subrange_kind K>
  struct tuple_size<ranges::subrange<I, S, K>>                                      // freestanding
    : integral_constant<size_t, 2> {};
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<0, ranges::subrange<I, S, K>> {                              // freestanding
    using type = I;                                                                 // freestanding
  };
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<1, ranges::subrange<I, S, K>> {                              // freestanding
    using type = S;                                                                 // freestanding
  };
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<0, const ranges::subrange<I, S, K>> {                        // freestanding
    using type = I;                                                                 // freestanding
  };
  template<class I, class S, ranges::subrange_kind K>
  struct tuple_element<1, const ranges::subrange<I, S, K>> {                        // freestanding
    using type = S;                                                                 // freestanding
  };

  struct from_range_t { explicit from_range_t() = default; };                       // freestanding
  inline constexpr from_range_t from_range{};                                       // freestanding
}
```

Within this Clause, for an integer-like type `X`
[[iterator.concept.winc]], `make-unsigned-like-t<X>` denotes
`make_unsigned_t<X>` if `X` is an integer type; otherwise, it denotes a
corresponding unspecified unsigned-integer-like type of the same width
as `X`. For an expression `x` of type `X`, `to-unsigned-like(x)` is `x`
explicitly converted to `make-unsigned-like-t<X>`.

Also within this Clause, `make-signed-like-t<X>` for an integer-like
type `X` denotes `make_signed_t<X>` if `X` is an integer type;
otherwise, it denotes a corresponding unspecified signed-integer-like
type of the same width as `X`.

## Range access <a id="range.access">[[range.access]]</a>

### General <a id="range.access.general">[[range.access.general]]</a>

In addition to being available via inclusion of the `<ranges>` header,
the customization point objects in [[range.access]] are available when
`<iterator>` is included.

Within [[range.access]], the *reified object* of a subexpression `E`
denotes

- the same object as `E` if `E` is a glvalue, or
- the result of applying the temporary materialization conversion
  [[conv.rval]] to `E` otherwise.

### `ranges::begin` <a id="range.access.begin">[[range.access.begin]]</a>

The name `ranges::begin` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::begin(E)` is ill-formed.
- Otherwise, if `T` is an array type [[term.array.type]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::begin(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `T` is an array type, `ranges::begin(E)` is
  expression-equivalent to `t + 0`.
- Otherwise, if `auto(t.begin())` is a valid expression whose type
  models `input_or_output_iterator`, `ranges::begin(E)` is
  expression-equivalent to `auto(t.begin())`.
- Otherwise, if `T` is a class or enumeration type and `auto(begin(t))`
  is a valid expression whose type models `input_or_output_iterator`
  where the meaning of `begin` is established as-if by performing
  argument-dependent lookup only [[basic.lookup.argdep]], then
  `ranges::begin(E)` is expression-equivalent to that expression.
- Otherwise, `ranges::begin(E)` is ill-formed.

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::begin(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::begin(E)` is a valid expression, its type
models `input_or_output_iterator`. — *end note*\]

### `ranges::end` <a id="range.access.end">[[range.access.end]]</a>

The name `ranges::end` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::end(E)` is ill-formed.
- Otherwise, if `T` is an array type [[term.array.type]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::end(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `T` is an array of unknown bound, `ranges::end(E)` is
  ill-formed.
- Otherwise, if `T` is an array, `ranges::end(E)` is
  expression-equivalent to `t + extent_v<T>`.
- Otherwise, if `auto(t.end())` is a valid expression whose type models
  `sentinel_for<iterator_t<T>>` then `ranges::end(E)` is
  expression-equivalent to `auto(t.end())`.
- Otherwise, if `T` is a class or enumeration type and `auto(end(t))` is
  a valid expression whose type models `sentinel_for<iterator_t<T>>`
  where the meaning of `end` is established as-if by performing
  argument-dependent lookup only [[basic.lookup.argdep]], then
  `ranges::end(E)` is expression-equivalent to that expression.
- Otherwise, `ranges::end(E)` is ill-formed.

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::end(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::end(E)` is a valid expression, the types
`S` and `I` of `ranges::end(E)` and `ranges::begin(E)` model
`sentinel_for<S, I>`. — *end note*\]

### `ranges::cbegin` <a id="range.access.cbegin">[[range.access.cbegin]]</a>

The name `ranges::cbegin` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E` with type `T`,
let `t` be an lvalue that denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::cbegin(E)` is ill-formed.
- Otherwise, let `U` be `ranges::begin(possibly-const-range(t))`.
  `ranges::cbegin(E)` is expression-equivalent to
  `const_iterator<decltype(U)>(U)`.

\[*Note 1*: Whenever `ranges::cbegin(E)` is a valid expression, its type
models `input_or_output_iterator` and
`constant-iterator`. — *end note*\]

### `ranges::cend` <a id="range.access.cend">[[range.access.cend]]</a>

The name `ranges::cend` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E` with type `T`,
let `t` be an lvalue that denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::cend(E)` is ill-formed.
- Otherwise, let `U` be `ranges::end(possibly-const-range(t))`.
  `ranges::cend(E)` is expression-equivalent to
  `const_sentinel<decltype(U)>(U)`.

\[*Note 1*: Whenever `ranges::cend(E)` is a valid expression, the types
`S` and `I` of the expressions `ranges::cend(E)` and `ranges::cbegin(E)`
model `sentinel_for<S, I>`. If `S` models `input_iterator`, then `S`
also models
\exposconceptx{constant-iterator}{constant-iterator}. — *end note*\]

### `ranges::rbegin` <a id="range.access.rbegin">[[range.access.rbegin]]</a>

The name `ranges::rbegin` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::rbegin(E)` is ill-formed.
- Otherwise, if `T` is an array type [[term.array.type]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::rbegin(E)`
  is ill-formed with no diagnostic required.
- Otherwise, if `auto(t.rbegin())` is a valid expression whose type
  models `input_or_output_iterator`, `ranges::rbegin(E)` is
  expression-equivalent to `auto(t.rbegin())`.
- Otherwise, if `T` is a class or enumeration type and `auto(rbegin(t))`
  is a valid expression whose type models `input_or_output_iterator`
  where the meaning of `rbegin` is established as-if by performing
  argument-dependent lookup only [[basic.lookup.argdep]], then
  `ranges::rbegin(E)` is expression-equivalent to that expression.
- Otherwise, if both `ranges::begin(t)` and `ranges::end(t)` are valid
  expressions of the same type which models `bidirectional_iterator`
  [[iterator.concept.bidir]], `ranges::rbegin(E)` is
  expression-equivalent to `make_reverse_iterator(ranges::end(t))`.
- Otherwise, `ranges::rbegin(E)` is ill-formed.

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::rbegin(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::rbegin(E)` is a valid expression, its type
models `input_or_output_iterator`. — *end note*\]

### `ranges::rend` <a id="range.access.rend">[[range.access.rend]]</a>

The name `ranges::rend` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::rend(E)` is ill-formed.
- Otherwise, if `T` is an array type [[term.array.type]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::rend(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `auto(t.rend())` is a valid expression whose type models
  `sentinel_for<decltype({}ranges::rbegin(E))>` then `ranges::rend(E)`
  is expression-equivalent to `auto(t.rend())`.
- Otherwise, if `T` is a class or enumeration type and `auto(rend(t))`
  is a valid expression whose type models
  `sentinel_for<decltype(ranges::rbegin(E))>` where the meaning of
  `rend` is established as-if by performing argument-dependent lookup
  only [[basic.lookup.argdep]], then `ranges::rend(E)` is
  expression-equivalent to that expression.
- Otherwise, if both `ranges::begin(t)` and `ranges::end(t)` are valid
  expressions of the same type which models `bidirectional_iterator`
  [[iterator.concept.bidir]], then `ranges::rend(E)` is
  expression-equivalent to `make_reverse_iterator(ranges::begin(t))`.
- Otherwise, `ranges::rend(E)` is ill-formed.

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::rend(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::rend(E)` is a valid expression, the types
`S` and `I` of the expressions `ranges::rend(E)` and `ranges::rbegin(E)`
model `sentinel_for<S, I>`. — *end note*\]

### `ranges::crbegin` <a id="range.access.crbegin">[[range.access.crbegin]]</a>

The name `ranges::crbegin` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E` with type `T`,
let `t` be an lvalue that denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::crbegin(E)` is ill-formed.
- Otherwise, let `U` be `ranges::rbegin(possibly-const-range(t))`.
  `ranges::crbegin(E)` is expression-equivalent to
  `const_iterator<decltype(U)>(U)`.

\[*Note 1*: Whenever `ranges::crbegin(E)` is a valid expression, its
type models `input_or_output_iterator` and
`constant-iterator`. — *end note*\]

### `ranges::crend` <a id="range.access.crend">[[range.access.crend]]</a>

The name `ranges::crend` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E` with type `T`,
let `t` be an lvalue that denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::crend(E)` is ill-formed.
- Otherwise, let `U` be `ranges::rend(possibly-const-range(t))`.
  `ranges::crend(E)` is expression-equivalent to
  `const_sentinel<decltype(U)>(U)`.

\[*Note 1*: Whenever `ranges::crend(E)` is a valid expression, the types
`S` and `I` of the expressions `ranges::crend(E)` and
`ranges::crbegin(E)` model `sentinel_for<S, I>`. If `S` models
`input_iterator`, then `S` also models
\exposconceptx{constant-iterator}{constant-iterator}. — *end note*\]

### `ranges::size` <a id="range.prim.size">[[range.prim.size]]</a>

The name `ranges::size` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `T` is an array of unknown bound [[term.array.type]],
  `ranges::size(E)` is ill-formed.
- Otherwise, if `T` is an array type, `ranges::size(E)` is
  expression-equivalent to `auto(extent_v<T>)`.
- Otherwise, if `disable_sized_range<remove_cv_t<T>>` [[range.sized]] is
  `false` and `auto(t.size())` is a valid expression of integer-like
  type [[iterator.concept.winc]], `ranges::size(E)` is
  expression-equivalent to `auto({}t.size())`.
- Otherwise, if `T` is a class or enumeration type,
  `disable_sized_range<remove_cv_t<T>>` is `false` and `auto(size(t))`
  is a valid expression of integer-like type where the meaning of `size`
  is established as-if by performing argument-dependent lookup only
  [[basic.lookup.argdep]], then `ranges::size(E)` is
  expression-equivalent to that expression.
- Otherwise, if `to-unsigned-like(ranges::end(t) - ranges::begin(t))`
  [[ranges.syn]] is a valid expression and the types `I` and `S` of
  `ranges::begin(t)` and `ranges::end(t)` (respectively) model both
  `sized_sentinel_for<S, I>` [[iterator.concept.sizedsentinel]] and
  `forward_iterator<I>`, then `ranges::size(E)` is expression-equivalent
  to `to-unsigned-like(ranges::end(t) - ranges::begin(t))`.
- Otherwise, `ranges::size(E)` is ill-formed.

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::size(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::size(E)` is a valid expression, its type
is integer-like. — *end note*\]

### `ranges::ssize` <a id="range.prim.ssize">[[range.prim.ssize]]</a>

The name `ranges::ssize` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. If `ranges::size(t)` is ill-formed,
`ranges::ssize(E)` is ill-formed. Otherwise let `D` be
`make-signed-like-t<decltype(ranges::{}size(t))>`, or `ptrdiff_t` if it
is wider than that type; `ranges::ssize(E)` is expression-equivalent to
`static_cast<D>(ranges::size(t))`.

### `ranges::empty` <a id="range.prim.empty">[[range.prim.empty]]</a>

The name `ranges::empty` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `T` is an array of unknown bound [[term.array.type]],
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

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::empty(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::empty(E)` is a valid expression, it has
type `bool`. — *end note*\]

### `ranges::data` <a id="range.prim.data">[[range.prim.data]]</a>

The name `ranges::data` denotes a customization point object
[[customization.point.object]].

Given a subexpression `E` with type `T`, let `t` be an lvalue that
denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::data(E)` is ill-formed.
- Otherwise, if `T` is an array type [[term.array.type]] and
  `remove_all_extents_t<T>` is an incomplete type, `ranges::data(E)` is
  ill-formed with no diagnostic required.
- Otherwise, if `auto(t.data())` is a valid expression of pointer to
  object type, `ranges::data(E)` is expression-equivalent to
  `auto(t.data())`.
- Otherwise, if `ranges::begin(t)` is a valid expression whose type
  models `contiguous_iterator`, `ranges::data(E)` is
  expression-equivalent to `to_address(ranges::begin(t))`.
- Otherwise, `ranges::data(E)` is ill-formed.

\[*Note 1*: Diagnosable ill-formed cases above result in substitution
failure when `ranges::data(E)` appears in the immediate context of a
template instantiation. — *end note*\]

\[*Note 2*: Whenever `ranges::data(E)` is a valid expression, it has
pointer to object type. — *end note*\]

### `ranges::cdata` <a id="range.prim.cdata">[[range.prim.cdata]]</a>

``` cpp
template<class T>
constexpr auto as-const-pointer(const T* p) { return p; }   // exposition only
```

The name `ranges::cdata` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E` with type `T`,
let `t` be an lvalue that denotes the reified object for `E`. Then:

- If `E` is an rvalue and `enable_borrowed_range<remove_cv_t<T>>` is
  `false`, `ranges::cdata(E)` is ill-formed.
- Otherwise, `ranges::cdata(E)` is expression-equivalent to
  `as-const-pointer(ranges::data(possibly-const-range(t)))`.

\[*Note 1*: Whenever `ranges::cdata(E)` is a valid expression, it has
pointer to constant object type. — *end note*\]

## Range requirements <a id="range.req">[[range.req]]</a>

### General <a id="range.req.general">[[range.req.general]]</a>

Ranges are an abstraction that allows a C++ program to operate on
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
to provide operations with predictable complexity.

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
      ranges::begin(t);         // sometimes equality-preserving (see below)
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

\[*Note 1*: Equality preservation of both `ranges::begin` and
`ranges::end` enables passing a range whose iterator type models
`forward_iterator` to multiple algorithms and making multiple passes
over the range by repeated calls to `ranges::begin` and `ranges::end`.
Since `ranges::begin` is not required to be equality-preserving when the
return type does not model `forward_iterator`, it is possible for
repeated calls to not return equal values or to not be
well-defined. — *end note*\]

``` cpp
template<class T>
  concept borrowed_range =
    range<T> && (is_lvalue_reference_v<T> || enable_borrowed_range<remove_cvref_t<T>>);
```

Let `U` be `remove_reference_t<T>` if `T` is an rvalue reference type,
and `T` otherwise. Given a variable `u` of type `U`, `T` models
`borrowed_range` only if the validity of iterators obtained from `u` is
not tied to the lifetime of that variable.

\[*Note 2*: Since the validity of iterators is not tied to the lifetime
of a variable whose type models `borrowed_range`, a function with a
parameter of such a type can return iterators obtained from it without
danger of dangling. — *end note*\]

``` cpp
template<class>
  constexpr bool enable_borrowed_range = false;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`enable_borrowed_range` for cv-unqualified program-defined types. Such
specializations shall be usable in constant expressions [[expr.const]]
and have type `const bool`.

\[*Example 1*:

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
    range<T> && requires(T& t) { ranges::size(t); };
```

Given an lvalue `t` of type `remove_reference_t<T>`, `T` models
`sized_range` only if

- `ranges::size(t)` is amortized 𝑂(1), does not modify `t`, and is equal
  to `ranges::distance(ranges::begin(t), ranges::end(t))`, and
- if `iterator_t<T>` models `forward_iterator`, `ranges::size(t)` is
  well-defined regardless of the evaluation of `ranges::begin(t)`.
  \[*Note 1*: `ranges::size(t)` is otherwise not required to be
  well-defined after evaluating `ranges::begin(t)`. For example, it is
  possible for `ranges::size(t)` to be well-defined for a `sized_range`
  whose iterator type does not model `forward_iterator` only if
  evaluated before the first call to `ranges::begin(t)`. — *end note*\]

``` cpp
template<class>
  constexpr bool disable_sized_range = false;
```

*Remarks:* Pursuant to [[namespace.std]], users may specialize
`disable_sized_range` for cv-unqualified program-defined types. Such
specializations shall be usable in constant expressions [[expr.const]]
and have type `const bool`.

\[*Note 1*: `disable_sized_range` allows use of range types with the
library that satisfy but do not in fact model
`sized_range`. — *end note*\]

### Views <a id="range.view">[[range.view]]</a>

The `view` concept specifies the requirements of a `range` type that has
the semantic properties below, which make it suitable for use in
constructing range adaptor pipelines [[range.adaptors]].

``` cpp
template<class T>
  concept view =
    range<T> && movable<T> && enable_view<T>;
```

`T` models `view` only if:

- `T` has 𝑂(1) move construction; and
- move assignment of an object of type `T` is no more complex than
  destruction followed by move construction; and
- if N copies and/or moves are made from an object of type `T` that
  contained M elements, then those N objects have 𝑂(N+M) destruction;
  and
- `copy_constructible<T>` is `false`, or `T` has 𝑂(1) copy construction;
  and
- `copyable<T>` is `false`, or copy assignment of an object of type `T`
  is no more complex than destruction followed by copy construction.

\[*Note 1*: The constraints on copying and moving imply that a
moved-from object of type `T` has 𝑂(1) destruction. — *end note*\]

\[*Example 1*:

Examples of views are:

- A `range` type that wraps a pair of iterators.
- A `range` type that holds its elements by `shared_ptr` and shares
  ownership with all its copies.
- A `range` type that generates its elements on demand.

A container such as `vector<string>` does not meet the semantic
requirements of `view` since copying the container copies all of the
elements, which cannot be done in constant time.

— *end example*\]

Since the difference between `range` and `view` is largely semantic, the
two are differentiated with the help of `enable_view`.

``` cpp
template<class T>
  constexpr bool is-derived-from-view-interface = see belownc;            // exposition only
template<class T>
  constexpr bool enable_view =
    derived_from<T, view_base> || is-derived-from-view-interface<T>;
```

For a type `T`, *`is-derived-from-view-interface`*`<T>` is `true` if and
only if `T` has exactly one public base class `view_interface<U>` for
some type `U` and `T` has no base classes of type `view_interface<V>`
for any other type `V`.

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
customization point object [[range.prim.data]] is usable with the range.

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

\[*Example 1*: The standard containers [[containers]] model
`common_range`. — *end example*\]

``` cpp
template<class T>
  concept common_range =
    range<T> && same_as<iterator_t<T>, sentinel_t<T>>;
```

``` cpp
template<class R>
  constexpr bool is-initializer-list = see below;               // exposition only
```

For a type `R`, *`is-initializer-list`*`<R>` is `true` if and only if
`remove_cvref_t<R>` is a specialization of `initializer_list`.

The `viewable_range` concept specifies the requirements of a `range`
type that can be converted to a view safely.

``` cpp
template<class T>
  concept viewable_range =
    range<T> &&
    ((view<remove_cvref_t<T>> && constructible_from<remove_cvref_t<T>, T>) ||
     (!view<remove_cvref_t<T>> &&
      (is_lvalue_reference_v<T> || (movable<remove_reference_t<T>> && !is-initializer-list<T>))));
```

The `constant_range` concept specifies the requirements of a `range`
type whose elements are not modifiable.

``` cpp
template<class T>
  concept constant_range =
    input_range<T> && constant-iterator<iterator_t<T>>;
```

## Range utilities <a id="range.utility">[[range.utility]]</a>

### General <a id="range.utility.general">[[range.utility.general]]</a>

The components in [[range.utility]] are general utilities for
representing and manipulating ranges.

### Helper concepts <a id="range.utility.helpers">[[range.utility.helpers]]</a>

Many of the types in subclause  [[range.utility]] are specified in terms
of the following exposition-only concepts:

``` cpp
template<class R>
  concept \defexposconceptnc{simple-view} =                                     // exposition only
    view<R> && range<const R> &&
    same_as<iterator_t<R>, iterator_t<const R>> &&
    same_as<sentinel_t<R>, sentinel_t<const R>>;

template<class I>
  concept \defexposconceptnc{has-arrow} =                                       // exposition only
    input_iterator<I> && (is_pointer_v<I> || requires(I i) { i.operator->(); });

template<class T, class U>
  concept \defexposconceptnc{different-from} =                                  // exposition only
    !same_as<remove_cvref_t<T>, remove_cvref_t<U>>;

template<class R>
  concept \defexposconceptnc{range-with-movable-references} =                   // exposition only
    input_range<R> && move_constructible<range_reference_t<R>> &&
    move_constructible<range_rvalue_reference_t<R>>;
```

### View interface <a id="view.interface">[[view.interface]]</a>

#### General <a id="view.interface.general">[[view.interface.general]]</a>

The class template `view_interface` is a helper for defining view-like
types that offer a container-like interface. It is parameterized with
the type that is derived from it.

``` cpp
namespace std::ranges {
  template<class D>
    requires is_class_v<D> && same_as<D, remove_cv_t<D>>
  class view_interface {
  private:
    constexpr D& derived() noexcept {               // exposition only
      return static_cast<D&>(*this);
    }
    constexpr const D& derived() const noexcept {   // exposition only
      return static_cast<const D&>(*this);
    }

  public:
    constexpr bool empty() requires sized_range<D> || forward_range<D> {
      if constexpr (sized_range<D>)
        return ranges::size(derived()) == 0;
      else
        return ranges::begin(derived()) == ranges::end(derived());
    }
    constexpr bool empty() const requires sized_range<const D> || forward_range<const D> {
      if constexpr (sized_range<const D>)
        return ranges::size(derived()) == 0;
      else
        return ranges::begin(derived()) == ranges::end(derived());
    }

    constexpr auto cbegin() requires input_range<D> {
      return ranges::cbegin(derived());
    }
    constexpr auto cbegin() const requires input_range<const D> {
      return ranges::cbegin(derived());
    }
    constexpr auto cend() requires input_range<D> {
      return ranges::cend(derived());
    }
    constexpr auto cend() const requires input_range<const D> {
      return ranges::cend(derived());
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
        return to-unsigned-like(ranges::end(derived()) - ranges::begin(derived()));
      }
    constexpr auto size() const requires forward_range<const D> &&
      sized_sentinel_for<sentinel_t<const D>, iterator_t<const D>> {
        return to-unsigned-like(ranges::end(derived()) - ranges::begin(derived()));
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

*Preconditions:* `!empty()` is `true`.

*Effects:* Equivalent to: `return *ranges::begin(`*`derived`*`());`

``` cpp
constexpr decltype(auto) back() requires bidirectional_range<D> && common_range<D>;
constexpr decltype(auto) back() const
  requires bidirectional_range<const D> && common_range<const D>;
```

*Preconditions:* `!empty()` is `true`.

*Effects:* Equivalent to:
`return *ranges::prev(ranges::end(`*`derived`*`()));`

### Sub-ranges <a id="range.subrange">[[range.subrange]]</a>

#### General <a id="range.subrange.general">[[range.subrange.general]]</a>

The `subrange` class template combines together an iterator and a
sentinel into a single object that models the `view` concept.
Additionally, it models the `sized_range` concept when the final
template parameter is `subrange_kind::sized`.

``` cpp
namespace std::ranges {
  template<class From, class To>
    concept \defexposconceptnc{uses-nonqualification-pointer-conversion} =      // exposition only
      is_pointer_v<From> && is_pointer_v<To> &&
      !convertible_to<remove_pointer_t<From>(*)[], remove_pointer_t<To>(*)[]>;

  template<class From, class To>
    concept \defexposconceptnc{convertible-to-non-slicing} =                    // exposition only
      convertible_to<From, To> &&
      !uses-nonqualification-pointer-conversion<decay_t<From>, decay_t<To>>;

  template<class T, class U, class V>
    concept \defexposconceptnc{pair-like-convertible-from} =                    // exposition only
      !range<T> && !is_reference_v<T> && pair-like<T> &&
      constructible_from<T, U, V> &&
      convertible-to-non-slicing<U, tuple_element_t<0, T>> &&
      convertible_to<V, tuple_element_t<1, T>>;

  template<input_or_output_iterator I, sentinel_for<I> S = I, subrange_kind K =
      sized_sentinel_for<S, I> ? subrange_kind::sized : subrange_kind::unsized>
    requires (K == subrange_kind::sized || !sized_sentinel_for<S, I>)
  class subrange : public view_interface<subrange<I, S, K>> {
  private:
    static constexpr bool StoreSize =                       // exposition only
      K == subrange_kind::sized && !sized_sentinel_for<S, I>;
    I begin_ = I();                                         // exposition only
    S end_ = S();                                           // exposition only
    make-unsigned-like-t<iter_difference_t<I>> size_ = 0;   // exposition only; present only
                                                            // if StoreSize is true
  public:
    subrange() requires default_initializable<I> = default;

    constexpr subrange(convertible-to-non-slicing<I> auto i, S s) requires (!StoreSize);

    constexpr subrange(convertible-to-non-slicing<I> auto i, S s,
                       make-unsigned-like-t<iter_difference_t<I>> n)
      requires (K == subrange_kind::sized);

    template<different-from<subrange> R>
      requires borrowed_range<R> &&
               convertible-to-non-slicing<iterator_t<R>, I> &&
               convertible_to<sentinel_t<R>, S>
    constexpr subrange(R&& r) requires (!StoreSize || sized_range<R>);

    template<borrowed_range R>
      requires convertible-to-non-slicing<iterator_t<R>, I> &&
               convertible_to<sentinel_t<R>, S>
    constexpr subrange(R&& r, make-unsigned-like-t<iter_difference_t<I>> n)
      requires (K == subrange_kind::sized)
        : subrange{ranges::begin(r), ranges::end(r), n} {}

    template<different-from<subrange> PairLike>
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

  template<borrowed_range R>
    subrange(R&&) ->
      subrange<iterator_t<R>, sentinel_t<R>,
               (sized_range<R> || sized_sentinel_for<sentinel_t<R>, iterator_t<R>>)
                 ? subrange_kind::sized : subrange_kind::unsized>;

  template<borrowed_range R>
    subrange(R&&, make-unsigned-like-t<range_difference_t<R>>) ->
      subrange<iterator_t<R>, sentinel_t<R>, subrange_kind::sized>;
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
`n == `*`to-unsigned-like`*`(ranges::distance(i, s))` is `true`.

*Effects:* Initializes *begin\_* with `std::move(i)` and *end\_* with
`s`. If *StoreSize* is `true`, initializes *size\_* with `n`.

\[*Note 1*: Accepting the length of the range and storing it to later
return from `size()` enables `subrange` to model `sized_range` even when
it stores an iterator and sentinel that do not model
`sized_sentinel_for`. — *end note*\]

``` cpp
template<different-from<subrange> R>
  requires borrowed_range<R> &&
           convertible-to-non-slicing<iterator_t<R>, I> &&
           convertible_to<sentinel_t<R>, S>
constexpr subrange(R&& r) requires (!StoreSize || sized_range<R>);
```

*Effects:* Equivalent to:

- If *StoreSize* is `true`,
  `subrange(r, static_cast<decltype(`*`size_`*`)>(ranges::size(r)))`.
- Otherwise, `subrange(ranges::begin(r), ranges::end(r))`.

*PairLike*

``` cpp
template<different-from<subrange> PairLike>
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

``` cpp
if constexpr (bidirectional_iterator<I>) {
  if (n < 0) {
    ranges::advance(begin_, n);
    if constexpr (StoreSize)
      size_ += to-unsigned-like(-n);
    return *this;
  }
}

auto d = n - ranges::advance(begin_, n, end_);
if constexpr (StoreSize)
  size_ -= to-unsigned-like(d);
return *this;
```

``` cpp
template<size_t N, class I, class S, subrange_kind K>
  requires ((N == 0 && copyable<I>) || N == 1)
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

The type `dangling` is used together with the template aliases
`borrowed_iterator_t` and `borrowed_subrange_t`. When an algorithm that
typically returns an iterator into, or a subrange of, a range argument
is called with an rvalue range argument that does not model
`borrowed_range` [[range.range]], the return value possibly refers to a
range whose lifetime has ended. In such cases, the type `dangling` is
returned instead of an iterator or subrange.

``` cpp
namespace std::ranges {
  struct dangling {
    constexpr dangling() noexcept = default;
    constexpr dangling(auto&&...) noexcept {}
  };
}
```

\[*Example 1*:

``` cpp
vector<int> f();
auto result1 = ranges::find(f(), 42);                                   // #1
static_assert(same_as<decltype(result1), ranges::dangling>);
auto vec = f();
auto result2 = ranges::find(vec, 42);                                   // #2
static_assert(same_as<decltype(result2), vector<int>::iterator>);
auto result3 = ranges::find(ranges::subrange{vec}, 42);                 // #3
static_assert(same_as<decltype(result3), vector<int>::iterator>);
```

The call to `ranges::find` at \#1 returns `ranges::dangling` since `f()`
is an rvalue `vector`; it is possible for the `vector` to be destroyed
before a returned iterator is dereferenced. However, the calls at \#2
and \#3 both return iterators since the lvalue `vec` and specializations
of `subrange` model `borrowed_range`.

— *end example*\]

For a type `R` that models `range`:

- if `R` models `borrowed_range`, then `borrowed_iterator_t<R>` denotes
  `iterator_t<R>`, and `borrowed_subrange_t<R>` denotes
  `subrange<iterator_t<R>>`;
- otherwise, both `borrowed_iterator_t<R>` and `borrowed_subrange_t<R>`
  denote `dangling`.

### Class template `elements_of` <a id="range.elementsof">[[range.elementsof]]</a>

Specializations of `elements_of` encapsulate a range and act as a tag in
overload sets to disambiguate when a range should be treated as a
sequence rather than a single value.

\[*Example 1*:

``` cpp
template<bool YieldElements>
generator<any> f(ranges::input_range auto&& r) {
  if constexpr (YieldElements)
    co_yield ranges::elements_of(r);        // yield each element of r
  else
    co_yield r;                             // yield r as a single value
}
```

— *end example*\]

``` cpp
namespace std::ranges {
  template<range R, class Allocator = allocator<byte>>
  struct elements_of {
    [[no_unique_address]] R range;
    [[no_unique_address]] Allocator allocator = Allocator();
  };

  template<class R, class Allocator = allocator<byte>>
    elements_of(R&&, Allocator = Allocator()) -> elements_of<R&&, Allocator>;
}
```

### Range conversions <a id="range.utility.conv">[[range.utility.conv]]</a>

#### General <a id="range.utility.conv.general">[[range.utility.conv.general]]</a>

The range conversion functions construct an object (usually a container)
from a range, by using a constructor taking a range, a `from_range_t`
tagged constructor, or a constructor taking a pair of iterators, or by
inserting each element of the range into the default-constructed object.

`ranges::to` is applied recursively, allowing the conversion of a range
of ranges.

\[*Example 1*:

``` cpp
string_view str = "the quick brown fox";
auto words = views::split(str, ' ') | to<vector<string>>();
// words is vector<string>{"the", "quick", "brown", "fox"}
```

— *end example*\]

Let *reservable-container* be defined as follows:

``` cpp
template<class Container>
constexpr bool reservable-container =          // exposition only
  sized_range<Container> &&
  requires(Container& c, range_size_t<Container> n) {
    c.reserve(n);
    { c.capacity() } -> same_as<decltype(n)>;
    { c.max_size() } -> same_as<decltype(n)>;
  };
```

Let *container-insertable* be defined as follows:

``` cpp
template<class Container, class Ref>
constexpr bool container-insertable =          // exposition only
  requires(Container& c, Ref&& ref) {
    requires (requires { c.push_back(std::forward<Ref>(ref)); } ||
              requires { c.insert(c.end(), std::forward<Ref>(ref)); });
  };
```

Let *container-inserter* be defined as follows:

``` cpp
template<class Ref, class Container>
constexpr auto container-inserter(Container& c) {                // exposition only
  if constexpr (requires { c.push_back(declval<Ref>()); })
    return back_inserter(c);
  else
    return inserter(c, c.end());
}
```

#### `ranges::to` <a id="range.utility.conv.to">[[range.utility.conv.to]]</a>

``` cpp
template<class C, input_range R, class... Args> requires (!view<C>)
  constexpr C to(R&& r, Args&&... args);
```

*Mandates:* `C` is a cv-unqualified class type.

*Returns:* An object of type `C` constructed from the elements of `r` in
the following manner:

- If `C` does not satisfy `input_range` or
  `convertible_to<range_reference_t<R>, range_value_t<C>>` is `true`:
  - If `constructible_from<C, R, Args...>` is `true`:
    ``` cpp
    C(std::forward<R>(r), std::forward<Args>(args)...)
    ```
  - Otherwise, if `constructible_from<C, from_range_t, R, Args...>` is
    `true`:
    ``` cpp
    C(from_range, std::forward<R>(r), std::forward<Args>(args)...)
    ```
  - Otherwise, if
    - `common_range<R>` is `true`,
    - the *qualified-id*
      `iterator_traits<iterator_t<R>>::iterator_category` is valid and
      denotes a type that models `derived_from<input_iterator_tag>`, and
    - `constructible_from<C, iterator_t<R>, sentinel_t<R>, Args...>` is
      `true`:

    ``` cpp
    C(ranges::begin(r), ranges::end(r), std::forward<Args>(args)...)
    ```
  - Otherwise, if
    - `constructible_from<C, Args...>` is `true`, and
    - *`container-insertable`*`<C, range_reference_t<R>>` is `true`:

    ``` cpp
    C c(std::forward<Args>(args)...);
    if constexpr (sized_range<R> && reservable-container<C>)
      c.reserve(static_cast<range_size_t<C>>(ranges::size(r)));
    ranges::copy(r, container-inserter<range_reference_t<R>>(c));
    ```
- Otherwise, if `input_range<range_reference_t<R>>` is `true`:
  ``` cpp
  to<C>(r | views::transform([](auto&& elem) {
    return to<range_value_t<C>>(std::forward<decltype(elem)>(elem));
  }), std::forward<Args>(args)...);
  ```
- Otherwise, the program is ill-formed.

``` cpp
template<template<class...> class C, input_range R, class... Args>
  constexpr auto to(R&& r, Args&&... args);
```

Let *input-iterator* be an exposition-only type:

``` cpp
struct input-iterator {                        // exposition only
  using iterator_category = input_iterator_tag;
  using value_type = range_value_t<R>;
  using difference_type = ptrdiff_t;
  using pointer = add_pointer_t<range_reference_t<R>>;
  using reference = range_reference_t<R>;
  reference operator*() const;
  pointer operator->() const;
  input-iterator& operator++();
  input-iterator operator++(int);
  bool operator==(const input-iterator&) const;
};
```

\[*Note 1*: *input-iterator* meets the syntactic requirements of
*Cpp17InputIterator*. — *end note*\]

Let *`DEDUCE_EXPR`* be defined as follows:

- `C(declval<R>(), declval<Args>()...)` if that is a valid expression,
- otherwise, `C(from_range, declval<R>(), declval<Args>()...)` if that
  is a valid expression,
- otherwise,
  ``` cpp
  C(declval<input-iterator>(), declval<input-iterator>(), declval<Args>()...)
  ```

  if that is a valid expression,
- otherwise, the program is ill-formed.

*Returns:*
`to<decltype(`*`DEDUCE_EXPR`*`)>(std::forward<R>(r), std::forward<Args>(args)...)`.

#### `ranges::to` adaptors <a id="range.utility.conv.adaptors">[[range.utility.conv.adaptors]]</a>

``` cpp
template<class C, class... Args> requires (!view<C>)
  constexpr auto to(Args&&... args);
template<template<class...> class C, class... Args>
  constexpr auto to(Args&&... args);
```

*Mandates:* For the first overload, `C` is a cv-unqualified class type.

*Returns:* A range adaptor closure object [[range.adaptor.object]] `f`
that is a perfect forwarding call
wrapper [[term.perfect.forwarding.call.wrapper]] with the following
properties:

- It has no target object.
- Its bound argument entities `bound_args` consist of objects of types
  `decay_t<Args>...` direct-non-list-initialized with
  `std::forward<Args>(args)...`, respectively.
- Its call pattern is `to<C>(r, bound_args...)`, where `r` is the
  argument used in a function call expression of `f`.

## Range factories <a id="range.factories">[[range.factories]]</a>

### General <a id="range.factories.general">[[range.factories.general]]</a>

Subclause [[range.factories]] defines *range factories*, which are
utilities to create a view.

Range factories are declared in namespace `std::ranges::views`.

### Empty view <a id="range.empty">[[range.empty]]</a>

#### Overview <a id="range.empty.overview">[[range.empty.overview]]</a>

`empty_view` produces a view of no elements of a particular type.

\[*Example 1*:

``` cpp
auto e = views::empty<int>;
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

`single_view` produces a view that contains exactly one element of a
specified value.

The name `views::single` denotes a customization point object
[[customization.point.object]]. Given a subexpression `E`, the
expression `views::single(E)` is expression-equivalent to
`single_view<decay_t<decltype((E))>>(E)`.

\[*Example 1*:

``` cpp
for (int i : views::single(4))
  cout << i;        // prints 4
```

— *end example*\]

#### Class template `single_view` <a id="range.single.view">[[range.single.view]]</a>

``` cpp
namespace std::ranges {
  template<move_constructible T>
    requires is_object_v<T>
  class single_view : public view_interface<single_view<T>> {
  private:
    movable-box<T> value_;              // exposition only{} (see [range.move.wrap])

  public:
    single_view() requires default_initializable<T> = default;
    constexpr explicit single_view(const T& t) requires copy_constructible<T>;
    constexpr explicit single_view(T&& t);
    template<class... Args>
      requires constructible_from<T, Args...>
    constexpr explicit single_view(in_place_t, Args&&... args);

    constexpr T* begin() noexcept;
    constexpr const T* begin() const noexcept;
    constexpr T* end() noexcept;
    constexpr const T* end() const noexcept;
    static constexpr size_t size() noexcept;
    constexpr T* data() noexcept;
    constexpr const T* data() const noexcept;
  };

  template<class T>
    single_view(T) -> single_view<T>;
}
```

``` cpp
constexpr explicit single_view(const T& t) requires copy_constructible<T>;
```

*Effects:* Initializes *value\_* with `t`.

``` cpp
constexpr explicit single_view(T&& t);
```

*Effects:* Initializes *value\_* with `std::move(t)`.

``` cpp
template<class... Args>
  requires constructible_from<T, Args...>
constexpr explicit single_view(in_place_t, Args&&... args);
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
expression-equivalent to `iota_view(E)` and `iota_view(E, F)`,
respectively.

\[*Example 1*:

``` cpp
for (int i : views::iota(1, 10))
  cout << i << ' '; // prints 1 2 3 4 5 6 7 8 9
```

— *end example*\]

#### Class template `iota_view` <a id="range.iota.view">[[range.iota.view]]</a>

``` cpp
namespace std::ranges {
  template<class I>
    concept exposition onlyconceptnc{decrementable} = see belownc;  // exposition only

  template<class I>
    concept exposition onlyconceptnc{advanceable} = see belownc;    // exposition only

  template<weakly_incrementable W, semiregular Bound = unreachable_sentinel_t>
    requires weakly-equality-comparable-with<W, Bound> && copyable<W>
  class iota_view : public view_interface<iota_view<W, Bound>> {
  private:
    // [range.iota.iterator], class iota_view::iterator
    struct iterator;                    // exposition only

    // [range.iota.sentinel], class iota_view::sentinel
    struct sentinel;                    // exposition only

    W value_ = W();                     // exposition only
    Bound bound_ = Bound();             // exposition only

  public:
    iota_view() requires default_initializable<W> = default;
    constexpr explicit iota_view(W value);
    constexpr explicit iota_view(type_identity_t<W> value, type_identity_t<Bound> bound);
    constexpr explicit iota_view(iterator first, see below last);

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
  concept decrementable =               // exposition only
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
  concept advanceable =                 // exposition only
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
is reachable from `value`. When `W` and `Bound` model
`totally_ordered_with`, then `bool(value <= Bound())` is `true`.

*Effects:* Initializes *value\_* with `value`.

``` cpp
constexpr explicit iota_view(type_identity_t<W> value, type_identity_t<Bound> bound);
```

*Preconditions:* `Bound` denotes `unreachable_sentinel_t` or `bound` is
reachable from `value`. When `W` and `Bound` model
`totally_ordered_with`, then `bool(value <= bound)` is `true`.

*Effects:* Initializes *value\_* with `value` and *bound\_* with
`bound`.

``` cpp
constexpr explicit iota_view(iterator first, see below last);
```

*Effects:* Equivalent to:

- If `same_as<W, Bound>` is `true`,
  `iota_view(first.`*`value_`*`, last.`*`value_`*`)`.
- Otherwise, if `Bound` denotes `unreachable_sentinel_t`,
  `iota_view(first.`*`value_`*`, last)`.
- Otherwise, `iota_view(first.`*`value_`*`, last.`*`bound_`*`)`.

*Remarks:* The type of `last` is:

- If `same_as<W, Bound>` is `true`, *iterator*.
- Otherwise, if `Bound` denotes `unreachable_sentinel_t`, `Bound`.
- Otherwise, *sentinel*.

``` cpp
constexpr iterator begin() const;
```

*Effects:* Equivalent to: `return `*`iterator`*`{`*`value_`*`};`

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

*Effects:* Equivalent to: `return `*`iterator`*`{`*`bound_`*`};`

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

*Remarks:* The expression in the *requires-clause* is equivalent to:

``` cpp
(same_as<W, Bound> && advanceable<W>) || (is-integer-like<W> && is-integer-like<Bound>) ||
  sized_sentinel_for<Bound, W>
```

#### Class `iota_view::iterator` <a id="range.iota.iterator">[[range.iota.iterator]]</a>

``` cpp
namespace std::ranges {
  template<weakly_incrementable W, semiregular Bound>
    requires weakly-equality-comparable-with<W, Bound> && copyable<W>
  struct iota_view<W, Bound>::iterator {
  private:
    W value_ = W();             // exposition only

  public:
    using iterator_concept = see below;
    using iterator_category = input_iterator_tag;       // present only if W models incrementable and
                                                        // IOTA-DIFF-T(W) is an integral type
    using value_type = W;
    using difference_type = IOTA-DIFF-T(W);

    iterator() requires default_initializable<W> = default;
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

\[*Note 1*: Overloads for `iter_move` and `iter_swap` are omitted
intentionally. — *end note*\]

``` cpp
constexpr explicit iterator(W value);
```

*Effects:* Initializes *value\_* with `value`.

``` cpp
constexpr W operator*() const noexcept(is_nothrow_copy_constructible_v<W>);
```

*Effects:* Equivalent to: `return `*`value_`*`;`

\[*Note 1*: The `noexcept` clause is needed by the default `iter_move`
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

*Effects:* Equivalent to:

``` cpp
i += n;
return i;
```

``` cpp
friend constexpr iterator operator+(difference_type n, iterator i)
  requires advanceable<W>;
```

*Effects:* Equivalent to: `return i + n;`

``` cpp
friend constexpr iterator operator-(iterator i, difference_type n)
  requires advanceable<W>;
```

*Effects:* Equivalent to:

``` cpp
i -= n;
return i;
```

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
    requires weakly-equality-comparable-with<W, Bound> && copyable<W>
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

### Repeat view <a id="range.repeat">[[range.repeat]]</a>

#### Overview <a id="range.repeat.overview">[[range.repeat.overview]]</a>

`repeat_view` generates a sequence of elements by repeatedly producing
the same value.

The name `views::repeat` denotes a customization point object
[[customization.point.object]]. Given subexpressions `E` and `F`, the
expressions `views::repeat(E)` and `views::repeat(E, F)` are
expression-equivalent to `repeat_view(E)` and `repeat_view(E, F)`,
respectively.

\[*Example 1*:

``` cpp
for (int i : views::repeat(17, 4))
  cout << i << ' ';
// prints 17 17 17 17
```

— *end example*\]

#### Class template `repeat_view` <a id="range.repeat.view">[[range.repeat.view]]</a>

``` cpp
namespace std::ranges {
  template<class T>
    concept \defexposconceptnc{integer-like-with-usable-difference-type} =  // exposition only
      is-signed-integer-like<T> || (is-integer-like<T> && weakly_incrementable<T>);

  template<move_constructible T, semiregular Bound = unreachable_sentinel_t>
    requires (is_object_v<T> && same_as<T, remove_cv_t<T>> &&
              (integer-like-with-usable-difference-type<Bound> ||
               same_as<Bound, unreachable_sentinel_t>))
  class repeat_view : public view_interface<repeat_view<T, Bound>> {
  private:
    // [range.repeat.iterator], class repeat_view::iterator
    struct iterator;                            // exposition only

    movable-box<T> value_;                      // exposition only, see [range.move.wrap]
    Bound bound_ = Bound();                     // exposition only

  public:
    repeat_view() requires default_initializable<T> = default;

    constexpr explicit repeat_view(const T& value, Bound bound = Bound())
      requires copy_constructible<T>;
    constexpr explicit repeat_view(T&& value, Bound bound = Bound());
    template<class... TArgs, class... BoundArgs>
      requires constructible_from<T, TArgs...> &&
               constructible_from<Bound, BoundArgs...>
    constexpr explicit repeat_view(piecewise_construct_t,
      tuple<TArgs...> value_args, tuple<BoundArgs...> bound_args = tuple<>{});

    constexpr iterator begin() const;
    constexpr iterator end() const requires (!same_as<Bound, unreachable_sentinel_t>);
    constexpr unreachable_sentinel_t end() const noexcept;

    constexpr auto size() const requires (!same_as<Bound, unreachable_sentinel_t>);
  };

  template<class T, class Bound>
    repeat_view(T, Bound) -> repeat_view<T, Bound>;
}
```

``` cpp
constexpr explicit repeat_view(const T& value, Bound bound = Bound())
  requires copy_constructible<T>;
```

*Preconditions:* If `Bound` is not `unreachable_sentinel_t`,
`bound` \ge 0.

*Effects:* Initializes *value\_* with `value` and *bound\_* with
`bound`.

``` cpp
constexpr explicit repeat_view(T&& value, Bound bound = Bound());
```

*Preconditions:* If `Bound` is not `unreachable_sentinel_t`,
`bound` \ge 0.

*Effects:* Initializes *value\_* with `std::move(value)` and *bound\_*
with `bound`.

``` cpp
template<class... TArgs, class... BoundArgs>
  requires constructible_from<T, TArgs...> &&
           constructible_from<Bound, BoundArgs...>
constexpr explicit repeat_view(piecewise_construct_t,
  tuple<TArgs...> value_args, tuple<BoundArgs...> bound_args = tuple<>{});
```

*Effects:* Initializes *value\_* with
`make_from_tuple<T>(std::move(value_args))` and initializes\linebreak
*bound\_* with `make_from_tuple<Bound>(std::move(bound_args))`. The
behavior is undefined if `Bound` is not `unreachable_sentinel_t` and
*bound\_* is negative.

``` cpp
constexpr iterator begin() const;
```

*Effects:* Equivalent to:
`return `*`iterator`*`(addressof(*`*`value_`*`));`

``` cpp
constexpr iterator end() const requires (!same_as<Bound, unreachable_sentinel_t>);
```

*Effects:* Equivalent to:
`return `*`iterator`*`(addressof(*`*`value_`*`), `*`bound_`*`);`

``` cpp
constexpr unreachable_sentinel_t end() const noexcept;
```

*Effects:* Equivalent to: `return unreachable_sentinel;`

``` cpp
constexpr auto size() const requires (!same_as<Bound, unreachable_sentinel_t>);
```

*Effects:* Equivalent to: `return `*`to-unsigned-like`*`(`*`bound_`*`);`

#### Class `repeat_view::iterator` <a id="range.repeat.iterator">[[range.repeat.iterator]]</a>

``` cpp
namespace std::ranges {
  template<move_constructible T, semiregular Bound>
    requires (is_object_v<T> && same_as<T, remove_cv_t<T>> &&
              (integer-like-with-usable-difference-type<Bound> ||
               same_as<Bound, unreachable_sentinel_t>))
  class repeat_view<T, Bound>::iterator {
  private:
    using index-type =                          // exposition only
      conditional_t<same_as<Bound, unreachable_sentinel_t>, ptrdiff_t, Bound>;
    const T* value_ = nullptr;                  // exposition only
    index-type current_ = index-type();         // exposition only

    constexpr explicit iterator(const T* value, index-type b = index-type());   // exposition only

  public:
    using iterator_concept = random_access_iterator_tag;
    using iterator_category = random_access_iterator_tag;
    using value_type = T;
    using difference_type = see below;

    iterator() = default;

    constexpr const T& operator*() const noexcept;

    constexpr iterator& operator++();
    constexpr iterator operator++(int);

    constexpr iterator& operator--();
    constexpr iterator operator--(int);

    constexpr iterator& operator+=(difference_type n);
    constexpr iterator& operator-=(difference_type n);
    constexpr const T& operator[](difference_type n) const noexcept;

    friend constexpr bool operator==(const iterator& x, const iterator& y);
    friend constexpr auto operator<=>(const iterator& x, const iterator& y);

    friend constexpr iterator operator+(iterator i, difference_type n);
    friend constexpr iterator operator+(difference_type n, iterator i);

    friend constexpr iterator operator-(iterator i, difference_type n);
    friend constexpr difference_type operator-(const iterator& x, const iterator& y);
  };
}
```

If `is-signed-integer-like<index-type>` is `true`, the member
*typedef-name* `difference_type` denotes *index-type*. Otherwise, it
denotes `IOTA-DIFF-T(index-type)` [[range.iota.view]].

``` cpp
constexpr explicit iterator(const T* value, index-type b = index-type());
```

*Preconditions:* If `Bound` is not `unreachable_sentinel_t`, `b` \ge 0.

*Effects:* Initializes *value\_* with `value` and *current\_* with `b`.

``` cpp
constexpr const T& operator*() const noexcept;
```

*Effects:* Equivalent to: `return *`*`value_`*`;`

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++current_;
return *this;
```

``` cpp
constexpr iterator operator++(int);
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--();
```

*Preconditions:* If `Bound` is not `unreachable_sentinel_t`,
$\textit{current_} > 0$.

*Effects:* Equivalent to:

``` cpp
--current_;
return *this;
```

``` cpp
constexpr iterator operator--(int);
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
constexpr iterator& operator+=(difference_type n);
```

*Preconditions:* If `Bound` is not `unreachable_sentinel_t`,
\textit{current_} + `n` \ge 0.

*Effects:* Equivalent to:

``` cpp
current_ += n;
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type n);
```

*Preconditions:* If `Bound` is not `unreachable_sentinel_t`,
\textit{current_} - `n` \ge 0.

*Effects:* Equivalent to:

``` cpp
current_ -= n;
return *this;
```

``` cpp
constexpr const T& operator[](difference_type n) const noexcept;
```

*Effects:* Equivalent to: `return *(*this + n);`

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`current_`*`;`

``` cpp
friend constexpr auto operator<=>(const iterator& x, const iterator& y);
```

*Effects:* Equivalent to:
`return x.`*`current_`*` <=> y.`*`current_`*`;`

``` cpp
friend constexpr iterator operator+(iterator i, difference_type n);
friend constexpr iterator operator+(difference_type n, iterator i);
```

*Effects:* Equivalent to:

``` cpp
i += n;
return i;
```

``` cpp
friend constexpr iterator operator-(iterator i, difference_type n);
```

*Effects:* Equivalent to:

``` cpp
i -= n;
return i;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y);
```

*Effects:* Equivalent to:

``` cpp
return static_cast<difference_type>(x.current_) - static_cast<difference_type>(y.current_);
```

### Istream view <a id="range.istream">[[range.istream]]</a>

#### Overview <a id="range.istream.overview">[[range.istream.overview]]</a>

`basic_istream_view` models `input_range` and reads (using `operator>>`)
successive elements from its corresponding input stream.

The name `views::istream<T>` denotes a customization point object
[[customization.point.object]]. Given a type `T` and a subexpression `E`
of type `U`, if `U` models
`derived_from<basic_istream<typename U::char_type,
typename U::traits_type>>`, then the expression `views::istream<T>(E)`
is expression-equivalent to
`basic_istream_view<T, typename U::char_type,
typename U::traits_type>(E)`; otherwise, `views::istream<T>(E)` is
ill-formed.

\[*Example 1*:

``` cpp
auto ints = istringstream{"0 1  2   3     4"};
ranges::copy(views::istream<int>(ints), ostream_iterator<int>{cout, "-"});
// prints 0-1-2-3-4-
```

— *end example*\]

#### Class template `basic_istream_view` <a id="range.istream.view">[[range.istream.view]]</a>

``` cpp
namespace std::ranges {
  template<class Val, class CharT, class Traits>
    concept \defexposconceptnc{stream-extractable} =                // exposition only
      requires(basic_istream<CharT, Traits>& is, Val& t) {
         is >> t;
      };

  template<movable Val, class CharT, class Traits = char_traits<CharT>>
    requires default_initializable<Val> &&
             stream-extractable<Val, CharT, Traits>
  class basic_istream_view : public view_interface<basic_istream_view<Val, CharT, Traits>> {
  public:
    constexpr explicit basic_istream_view(basic_istream<CharT, Traits>& stream);

    constexpr auto begin() {
      *stream_ >> value_;
      return iterator{*this};
    }

    constexpr default_sentinel_t end() const noexcept;

  private:
    // [range.istream.iterator], class basic_istream_view::iterator
    struct iterator;                            // exposition only
    basic_istream<CharT, Traits>* stream_;      // exposition only
    Val value_ = Val();                         // exposition only
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

#### Class `basic_istream_view::iterator` <a id="range.istream.iterator">[[range.istream.iterator]]</a>

``` cpp
namespace std::ranges {
  template<movable Val, class CharT, class Traits>
    requires default_initializable<Val> &&
             stream-extractable<Val, CharT, Traits>
  class basic_istream_view<Val, CharT, Traits>::iterator {
  public:
    using iterator_concept = input_iterator_tag;
    using difference_type = ptrdiff_t;
    using value_type = Val;

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
    basic_istream_view* parent_;                                // exposition only
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

*Effects:* Equivalent to:

``` cpp
*parent_->stream_ >> parent_->value_;
return *this;
```

``` cpp
void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
Val& operator*() const;
```

*Effects:* Equivalent to: `return `*`parent_`*`->`*`value_`*`;`

``` cpp
friend bool operator==(const iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to: `return !*x.`*`parent_`*`->`*`stream_`*`;`

## Range adaptors <a id="range.adaptors">[[range.adaptors]]</a>

### General <a id="range.adaptors.general">[[range.adaptors.general]]</a>

Subclause [[range.adaptors]] defines *range adaptors*, which are
utilities that transform a range into a view with custom behaviors.
These adaptors can be chained to create pipelines of range
transformations that evaluate lazily as the resulting view is iterated.

Range adaptors are declared in namespace `std::ranges::views`.

The bitwise operator is overloaded for the purpose of creating adaptor
chain pipelines. The adaptors also support function call syntax with
equivalent semantics.

\[*Example 1*:

``` cpp
vector<int> ints{0,1,2,3,4,5};
auto even = [](int i) { return 0 == i % 2; };
auto square = [](int i) { return i * i; };
for (int i : ints | views::filter(even) | views::transform(square)) {
  cout << i << ' '; // prints 0 4 16
}
assert(ranges::equal(ints | views::filter(even), views::filter(ints, even)));
```

— *end example*\]

### Range adaptor objects <a id="range.adaptor.object">[[range.adaptor.object]]</a>

A *range adaptor closure object* is a unary function object that accepts
a range argument. For a range adaptor closure object `C` and an
expression `R` such that `decltype((R))` models `range`, the following
expressions are equivalent:

``` cpp
C(R)
R | C
```

Given an additional range adaptor closure object `D`, the expression
`C | D` produces another range adaptor closure object `E`. `E` is a
perfect forwarding call wrapper [[term.perfect.forwarding.call.wrapper]]
with the following properties:

- Its target object is an object `d` of type `decay_t<decltype((D))>`
  direct-non-list-initialized with `D`.
- It has one bound argument entity, an object `c` of type
  `decay_t<decltype((C))>` direct-non-list-initialized with `C`.
- Its call pattern is `d(c(arg))`, where `arg` is the argument used in a
  function call expression of `E`.

The expression `C | D` is well-formed if and only if the initializations
of the state entities of `E` are all well-formed.

Given an object `t` of type `T`, where

- `t` is a unary function object that accepts a range argument,
- `T` models `derived_from<range_adaptor_closure<T>>`,
- `T` has no other base classes of type `range_adaptor_closure<U>` for
  any other type `U`, and
- `T` does not model `range`

then the implementation ensures that `t` is a range adaptor closure
object.

The template parameter `D` for `range_adaptor_closure` may be an
incomplete type. If an expression of type cv `D` is used as an operand
to the `|` operator, `D` shall be complete and model
`derived_from<range_adaptor_closure<D>>`. The behavior of an expression
involving an object of type cv `D` as an operand to the `|` operator is
undefined if overload resolution selects a program-defined `operator|`
function.

If an expression of type cv `U` is used as an operand to the `|`
operator, where `U` has a base class of type `range_adaptor_closure<T>`
for some type `T` other than `U`, the behavior is undefined.

The behavior of a program that adds a specialization for
`range_adaptor_closure` is undefined.

A *range adaptor object* is a customization point object
[[customization.point.object]] that accepts a `viewable_range` as its
first argument and returns a view.

If a range adaptor object accepts only one argument, then it is a range
adaptor closure object.

If a range adaptor object `adaptor` accepts more than one argument, then
let `range` be an expression such that `decltype((range))` models
`viewable_range`, let `args...` be arguments such that
`adaptor(range, args...)` is a well-formed expression as specified in
the rest of subclause  [[range.adaptors]], and let `BoundArgs` be a pack
that denotes `decay_t<decltype((args))>...`. The expression
`adaptor(args...)` produces a range adaptor closure object `f` that is a
perfect forwarding call wrapper [[term.perfect.forwarding.call.wrapper]]
with the following properties:

- Its target object is a copy of `adaptor`.
- Its bound argument entities `bound_args` consist of objects of types
  `BoundArgs...` direct-non-list-initialized with
  `std::forward<decltype((args))>(args)...`, respectively.
- Its call pattern is `adaptor(r, bound_args...)`, where `r` is the
  argument used in a function call expression of `f`.

The expression `adaptor(args...)` is well-formed if and only if the
initialization of the bound argument entities of the result, as
specified above, are all well-formed.

### Movable wrapper <a id="range.move.wrap">[[range.move.wrap]]</a>

Many types in this subclause are specified in terms of an
exposition-only class template *movable-box*. `movable-box<T>` behaves
exactly like `optional<T>` with the following differences:

- `movable-box<T>` constrains its type parameter `T` with
  `move_constructible<T> && is_object_v<T>`.
- The default constructor of `movable-box<T>` is equivalent to:
  ``` cpp
  constexpr movable-box() noexcept(is_nothrow_default_constructible_v<T>)
      requires default_initializable<T>
    : movable-box{in_place} {}
  ```
- If `copyable<T>` is not modeled, the copy assignment operator is
  equivalent to:
  ``` cpp
  constexpr movable-box& operator=(const movable-box& that)
    noexcept(is_nothrow_copy_constructible_v<T>)
    requires copy_constructible<T> {
    if (this != addressof(that)) {
      if (that) emplace(*that);
      else reset();
    }
    return *this;
  }
  ```
- If `movable<T>` is not modeled, the move assignment operator is
  equivalent to:
  ``` cpp
  constexpr movable-box& operator=(movable-box&& that)
    noexcept(is_nothrow_move_constructible_v<T>) {
    if (this != addressof(that)) {
      if (that) emplace(std::move(*that));
      else reset();
    }
    return *this;
  }
  ```

*Recommended practice:*

- If `copy_constructible<T>` is `true`, `movable-box<T>` should store
  only a `T` if either `T` models `copyable`, or
  `is_nothrow_move_constructible_v<T> && is_nothrow_copy_constructible_v<T>`
  is `true`.
- Otherwise, `movable-box<T>` should store only a `T` if either `T`
  models `movable` or `is_nothrow_move_constructible_v<T>` is `true`.

### Non-propagating cache <a id="range.nonprop.cache">[[range.nonprop.cache]]</a>

Some types in subclause [[range.adaptors]] are specified in terms of an
exposition-only class template *non-propagating-cache*.
`non-propagating-cache<T>` behaves exactly like `optional<T>` with the
following differences:

- `non-propagating-cache<T>` constrains its type parameter `T` with
  `is_object_v<T>`.
- The copy constructor is equivalent to:
  ``` cpp
  constexpr non-propagating-cache(const non-propagating-cache&) noexcept {}
  ```
- The move constructor is equivalent to:
  ``` cpp
  constexpr non-propagating-cache(non-propagating-cache&& other) noexcept {
    other.reset();
  }
  ```
- The copy assignment operator is equivalent to:
  ``` cpp
  constexpr non-propagating-cache& operator=(const non-propagating-cache& other) noexcept {
    if (addressof(other) != this)
      reset();
    return *this;
  }
  ```
- The move assignment operator is equivalent to:
  ``` cpp
  constexpr non-propagating-cache& operator=(non-propagating-cache&& other) noexcept {
    reset();
    other.reset();
    return *this;
  }
  ```
- `non-propagating-cache<T>` has an additional member function template
  specified as follows:
  ``` cpp
  template<class I>
    constexpr T& emplace-deref(const I& i);    // exposition only
  ```

  *Mandates:* The declaration `T t(*i);` is well-formed for some
  invented variable `t`.
  \[*Note 1*: If `*i` is a prvalue of type cv `T`, there is no
  requirement that it is movable [[dcl.init.general]]. — *end note*\]
  *Effects:* Calls `reset()`. Then direct-non-list-initializes the
  contained value with `*i`.
  *Ensures:* `*this` contains a value.
  *Returns:* A reference to the new contained value.
  *Throws:* Any exception thrown by the initialization of the contained
  value.
  *Remarks:* If an exception is thrown during the initialization of `T`,
  `*this` does not contain a value, and the previous value (if any) has
  been destroyed.

\[*Note 1*: *non-propagating-cache* enables an input view to temporarily
cache values as it is iterated over. — *end note*\]

### Range adaptor helpers <a id="range.adaptor.helpers">[[range.adaptor.helpers]]</a>

``` cpp
namespace std::ranges {
  template<class F, class Tuple>
  constexpr auto tuple-transform(F&& f, Tuple&& t) { // exposition only
    return apply([&]<class... Ts>(Ts&&... elements) {
      return tuple<invoke_result_t<F&, Ts>...>(invoke(f, std::forward<Ts>(elements))...);
    }, std::forward<Tuple>(t));
  }

  template<class F, class Tuple>
  constexpr void tuple-for-each(F&& f, Tuple&& t) { // exposition only
    apply([&]<class... Ts>(Ts&&... elements) {
      (static_cast<void>(invoke(f, std::forward<Ts>(elements))), ...);
    }, std::forward<Tuple>(t));
  }

  template<class T>
  constexpr T& as-lvalue(T&& t) {                   // exposition only
    return static_cast<T&>(t);
  }
}
```

### All view <a id="range.all">[[range.all]]</a>

#### General <a id="range.all.general">[[range.all.general]]</a>

`views::all` returns a view that includes all elements of its range
argument.

The name `views::all` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::all(E)` is expression-equivalent to:

- `decay-copy(E)` if the decayed type of `E` models `view`.
- Otherwise, `ref_view{E}` if that expression is well-formed.
- Otherwise, `owning_view{E}`.

#### Class template `ref_view` <a id="range.ref.view">[[range.ref.view]]</a>

`ref_view` is a view of the elements of some other range.

``` cpp
namespace std::ranges {
  template<range R>
    requires is_object_v<R>
  class ref_view : public view_interface<ref_view<R>> {
  private:
    R* r_;                      // exposition only

  public:
    template<different-from<ref_view> T>
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
template<different-from<ref_view> T>
  requires see below
constexpr ref_view(T&& t);
```

*Effects:* Initializes *r\_* with
`addressof(static_cast<R&>(std::forward<T>(t)))`.

*Remarks:* Let *`FUN`* denote the exposition-only functions

``` cpp
void FUN(R&);
void FUN(R&&) = delete;
```

The expression in the *requires-clause* is equivalent to:

``` cpp
convertible_to<T, R&> && requires { FUN(declval<T>()); }
```

#### Class template `owning_view` <a id="range.owning.view">[[range.owning.view]]</a>

`owning_view` is a move-only view of the elements of some other range.

``` cpp
namespace std::ranges {
  template<range R>
    requires movable<R> && (!is-initializer-list<R>) // see [range.refinements]
  class owning_view : public view_interface<owning_view<R>> {
  private:
    R r_ = R();         // exposition only

  public:
    owning_view() requires default_initializable<R> = default;
    constexpr owning_view(R&& t);

    owning_view(owning_view&&) = default;
    owning_view& operator=(owning_view&&) = default;

    constexpr R& base() & noexcept { return r_; }
    constexpr const R& base() const & noexcept { return r_; }
    constexpr R&& base() && noexcept { return std::move(r_); }
    constexpr const R&& base() const && noexcept { return std::move(r_); }

    constexpr iterator_t<R> begin() { return ranges::begin(r_); }
    constexpr sentinel_t<R> end() { return ranges::end(r_); }

    constexpr auto begin() const requires range<const R>
    { return ranges::begin(r_); }
    constexpr auto end() const requires range<const R>
    { return ranges::end(r_); }

    constexpr bool empty() requires requires { ranges::empty(r_); }
    { return ranges::empty(r_); }
    constexpr bool empty() const requires requires { ranges::empty(r_); }
    { return ranges::empty(r_); }

    constexpr auto size() requires sized_range<R>
    { return ranges::size(r_); }
    constexpr auto size() const requires sized_range<const R>
    { return ranges::size(r_); }

    constexpr auto data() requires contiguous_range<R>
    { return ranges::data(r_); }
    constexpr auto data() const requires contiguous_range<const R>
    { return ranges::data(r_); }
  };
}
```

``` cpp
constexpr owning_view(R&& t);
```

*Effects:* Initializes *r\_* with `std::move(t)`.

### As rvalue view <a id="range.as.rvalue">[[range.as.rvalue]]</a>

#### Overview <a id="range.as.rvalue.overview">[[range.as.rvalue.overview]]</a>

`as_rvalue_view` presents a view of an underlying sequence with the same
behavior as the underlying sequence except that its elements are
rvalues. Some generic algorithms can be called with an `as_rvalue_view`
to replace copying with moving.

The name `views::as_rvalue` denotes a range adaptor object
[[range.adaptor.object]]. Let `E` be an expression and let `T` be
`decltype((E))`. The expression `views::as_rvalue(E)` is
expression-equivalent to:

- `views::all(E)` if
  `same_as<range_rvalue_reference_t<T>, range_reference_t<T>>` is
  `true`.
- Otherwise, `as_rvalue_view(E)`.

\[*Example 1*:

``` cpp
vector<string> words = {"the", "quick", "brown", "fox", "ate", "a", "pterodactyl"};
vector<string> new_words;
ranges::copy(words | views::as_rvalue, back_inserter(new_words));
  // moves each string from words into new_words
```

— *end example*\]

#### Class template `as_rvalue_view` <a id="range.as.rvalue.view">[[range.as.rvalue.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires input_range<V>
  class as_rvalue_view : public view_interface<as_rvalue_view<V>> {
    V base_ = V();      // exposition only

  public:
    as_rvalue_view() requires default_initializable<V> = default;
    constexpr explicit as_rvalue_view(V base);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>)
    { return move_iterator(ranges::begin(base_)); }
    constexpr auto begin() const requires range<const V>
    { return move_iterator(ranges::begin(base_)); }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (common_range<V>) {
        return move_iterator(ranges::end(base_));
      } else {
        return move_sentinel(ranges::end(base_));
      }
    }
    constexpr auto end() const requires range<const V> {
      if constexpr (common_range<const V>) {
        return move_iterator(ranges::end(base_));
      } else {
        return move_sentinel(ranges::end(base_));
      }
    }

    constexpr auto size() requires sized_range<V> { return ranges::size(base_); }
    constexpr auto size() const requires sized_range<const V> { return ranges::size(base_); }
  };

  template<class R>
    as_rvalue_view(R&&) -> as_rvalue_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit as_rvalue_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

### Filter view <a id="range.filter">[[range.filter]]</a>

#### Overview <a id="range.filter.overview">[[range.filter.overview]]</a>

`filter_view` presents a view of the elements of an underlying sequence
that satisfy a predicate.

The name `views::filter` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `P`, the
expression `views::filter(E, P)` is expression-equivalent to
`filter_view(E, P)`.

\[*Example 1*:

``` cpp
vector<int> is{ 0, 1, 2, 3, 4, 5, 6 };
auto evens = views::filter(is, [](int i) { return 0 == i % 2; });
for (int i : evens)
  cout << i << ' '; // prints 0 2 4 6
```

— *end example*\]

#### Class template `filter_view` <a id="range.filter.view">[[range.filter.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, indirect_unary_predicate<iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class filter_view : public view_interface<filter_view<V, Pred>> {
  private:
    V base_ = V();                              // exposition only
    movable-box<Pred> pred_;                    // exposition only

    // [range.filter.iterator], class filter_view::iterator
    class iterator;                             // exposition only

    // [range.filter.sentinel], class filter_view::sentinel
    class sentinel;                             // exposition only

  public:
    filter_view() requires default_initializable<V> && default_initializable<Pred> = default;
    constexpr explicit filter_view(V base, Pred pred);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
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
constexpr explicit filter_view(V base, Pred pred);
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

*Preconditions:* *`pred_`*`.has_value()` is `true`.

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
    using iterator_concept  = see belownc;
    using iterator_category = see belownc;        // not always present
    using value_type        = range_value_t<V>;
    using difference_type   = range_difference_t<V>;

    iterator() requires default_initializable<iterator_t<V>> = default;
    constexpr iterator(filter_view& parent, iterator_t<V> current);

    constexpr const iterator_t<V>& base() const & noexcept;
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

The member *typedef-name* `iterator_category` is defined if and only if
`V` models `forward_range`. In that case, `iterator::iterator_category`
is defined as follows:

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
constexpr const iterator_t<V>& base() const & noexcept;
```

*Effects:* Equivalent to: `return `*`current_`*`;`

``` cpp
constexpr iterator_t<V> base() &&;
```

*Effects:* Equivalent to: `return std::move(`*`current_`*`);`

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

`transform_view` presents a view of an underlying sequence after
applying a transformation function to each element.

The name `views::transform` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::transform(E, F)` is expression-equivalent to
`transform_view(E, F)`.

\[*Example 1*:

``` cpp
vector<int> is{ 0, 1, 2, 3, 4 };
auto squares = views::transform(is, [](int i) { return i * i; });
for (int i : squares)
  cout << i << ' '; // prints 0 1 4 9 16
```

— *end example*\]

#### Class template `transform_view` <a id="range.transform.view">[[range.transform.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, move_constructible F>
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
    movable-box<F> fun_;                        // exposition only

  public:
    transform_view() requires default_initializable<V> && default_initializable<F> = default;
    constexpr explicit transform_view(V base, F fun);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
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
constexpr explicit transform_view(V base, F fun);
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
  template<input_range V, move_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>> &&
             can-reference<invoke_result_t<F&, range_reference_t<V>>>
  template<bool Const>
  class transform_view<V, F>::iterator {
  private:
    using Parent = maybe-const<Const, transform_view>;          // exposition only
    using Base = maybe-const<Const, V>;                         // exposition only
    iterator_t<Base> current_ = iterator_t<Base>();             // exposition only
    Parent* parent_ = nullptr;                                  // exposition only

  public:
    using iterator_concept  = see belownc;
    using iterator_category = see belownc;                        // not always present
    using value_type        =
      remove_cvref_t<invoke_result_t<maybe-const<Const, F>&, range_reference_t<Base>>>;
    using difference_type   = range_difference_t<Base>;

    iterator() requires default_initializable<iterator_t<Base>> = default;
    constexpr iterator(Parent& parent, iterator_t<Base> current);
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr const iterator_t<Base>& base() const & noexcept;
    constexpr iterator_t<Base> base() &&;

    constexpr decltype(auto) operator*() const
      noexcept(noexcept(invoke(*parent_->fun_, *current_))) {
      return invoke(*parent_->fun_, *current_);
    }

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
      requires random_access_range<Base> {
      return invoke(*parent_->fun_, current_[n]);
    }

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
      requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if *Base* models `forward_range`, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

The member *typedef-name* `iterator_category` is defined if and only if
*Base* models `forward_range`. In that case,
`iterator::iterator_category` is defined as follows: Let `C` denote the
type `iterator_traits<iterator_t<Base>>::iterator_category`.

- If
  `is_reference_v<invoke_result_t<maybe-const<Const, F>&, range_reference_t<Base>>>`
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
constexpr const iterator_t<Base>& base() const & noexcept;
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
constexpr void operator++(int);
```

*Effects:* Equivalent to `++`*`current_`*.

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
`return `*`iterator`*`{*i.`*`parent_`*`, i.`*`current_`*` + n};`

``` cpp
friend constexpr iterator operator-(iterator i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return `*`iterator`*`{*i.`*`parent_`*`, i.`*`current_`*` - n};`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`current_`*`;`

#### Class template `transform_view::sentinel` <a id="range.transform.sentinel">[[range.transform.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, move_constructible F>
    requires view<V> && is_object_v<F> &&
             regular_invocable<F&, range_reference_t<V>> &&
             can-reference<invoke_result_t<F&, range_reference_t<V>>>
  template<bool Const>
  class transform_view<V, F>::sentinel {
  private:
    using Parent = maybe-const<Const, transform_view>;  // exposition only
    using Base = maybe-const<Const, V>;                 // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only

  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end);
    constexpr sentinel(sentinel<!Const> i)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    template<bool OtherConst>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const sentinel& y, const iterator<OtherConst>& x);
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
template<bool OtherConst>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const sentinel& y, const iterator<OtherConst>& x);
```

*Effects:* Equivalent to: `return y.`*`end_`*` - x.`*`current_`*`;`

### Take view <a id="range.take">[[range.take]]</a>

#### Overview <a id="range.take.overview">[[range.take.overview]]</a>

`take_view` produces a view of the first N elements from another view,
or all the elements if the adapted view contains fewer than N.

The name `views::take` denotes a range adaptor object
[[range.adaptor.object]]. Let `E` and `F` be expressions, let `T` be
`remove_cvref_t<decltype((E))>`, and let `D` be
`range_difference_t<decltype((E))>`. If `decltype((F))` does not model
`convertible_to<D>`, `views::take(E, F)` is ill-formed. Otherwise, the
expression `views::take(E, F)` is expression-equivalent to:

- If `T` is a specialization of `empty_view` [[range.empty.view]], then
  `((void)F, decay-copy(E))`, except that the evaluations of `E` and `F`
  are indeterminately sequenced.
- Otherwise, if `T` models `random_access_range` and `sized_range` and
  is a specialization of `span` [[views.span]], `basic_string_view`
  [[string.view]], or `subrange` [[range.subrange]], then
  `U(ranges::begin(E),
  ranges::begin(E) + std::min<D>(ranges::distance(E), F))`, except that
  `E` is evaluated only once, where `U` is a type determined as follows:
  - if `T` is a specialization of `span`, then `U` is
    `span<typename T::element_type>`;
  - otherwise, if `T` is a specialization of `basic_string_view`, then
    `U` is `T`;
  - otherwise, `T` is a specialization of `subrange`, and `U` is
    `subrange<iterator_t<T>>`;
- otherwise, if `T` is a specialization of `iota_view`
  [[range.iota.view]] that models `random_access_range` and
  `sized_range`, then `iota_view(*ranges::begin(E),
  *(ranges::begin(E) + std::\linebreak{}min<D>(ranges::distance(E), F)))`,
  except that `E` is evaluated only once.
- Otherwise, if `T` is a specialization of `repeat_view`
  [[range.repeat.view]]:
  - if `T` models `sized_range`, then
    ``` cpp
    views::repeat(*E.value_, std::min<D>(ranges::distance(E), F))
    ```

    except that `E` is evaluated only once;
  - otherwise, `views::repeat(*E.value_, static_cast<D>(F))`.
- Otherwise, `take_view(E, F)`.

\[*Example 1*:

``` cpp
vector<int> is{0,1,2,3,4,5,6,7,8,9};
for (int i : is | views::take(5))
  cout << i << ' '; // prints 0 1 2 3 4
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
    template<bool> class sentinel;                      // exposition only

  public:
    take_view() requires default_initializable<V> = default;
    constexpr explicit take_view(V base, range_difference_t<V> count);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>) {
      if constexpr (sized_range<V>) {
        if constexpr (random_access_range<V>) {
          return ranges::begin(base_);
        } else {
          auto sz = range_difference_t<V>(size());
          return counted_iterator(ranges::begin(base_), sz);
        }
      } else if constexpr (sized_sentinel_for<sentinel_t<V>, iterator_t<V>>) {
        auto it = ranges::begin(base_);
        auto sz = std::min(count_, ranges::end(base_) - it);
        return counted_iterator(std::move(it), sz);
      } else {
        return counted_iterator(ranges::begin(base_), count_);
      }
    }

    constexpr auto begin() const requires range<const V> {
      if constexpr (sized_range<const V>) {
        if constexpr (random_access_range<const V>) {
          return ranges::begin(base_);
        } else {
          auto sz = range_difference_t<const V>(size());
          return counted_iterator(ranges::begin(base_), sz);
        }
      } else if constexpr (sized_sentinel_for<sentinel_t<const V>, iterator_t<const V>>) {
        auto it = ranges::begin(base_);
        auto sz = std::min(count_, ranges::end(base_) - it);
        return counted_iterator(std::move(it), sz);
      } else {
        return counted_iterator(ranges::begin(base_), count_);
      }
    }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (sized_range<V>) {
        if constexpr (random_access_range<V>)
          return ranges::begin(base_) + range_difference_t<V>(size());
        else
          return default_sentinel;
      } else if constexpr (sized_sentinel_for<sentinel_t<V>, iterator_t<V>>) {
        return default_sentinel;
      } else {
        return sentinel<false>{ranges::end(base_)};
      }
    }

    constexpr auto end() const requires range<const V> {
      if constexpr (sized_range<const V>) {
        if constexpr (random_access_range<const V>)
          return ranges::begin(base_) + range_difference_t<const V>(size());
        else
          return default_sentinel;
      } else if constexpr (sized_sentinel_for<sentinel_t<const V>, iterator_t<const V>>) {
        return default_sentinel;
      } else {
        return sentinel<true>{ranges::end(base_)};
      }
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

  template<class R>
    take_view(R&&, range_difference_t<R>)
      -> take_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit take_view(V base, range_difference_t<V> count);
```

*Preconditions:* `count >= 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *count\_*
with `count`.

#### Class template `take_view::sentinel` <a id="range.take.sentinel">[[range.take.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<view V>
  template<bool Const>
  class take_view<V>::sentinel {
  private:
    using Base = maybe-const<Const, V>;                                     // exposition only
    template<bool OtherConst>
      using CI = counted_iterator<iterator_t<maybe-const<OtherConst, V>>>;  // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();                             // exposition only

  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end);
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    friend constexpr bool operator==(const CI<Const>& y, const sentinel& x);

    template<bool OtherConst = !Const>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const CI<OtherConst>& y, const sentinel& x);
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
friend constexpr bool operator==(const CI<Const>& y, const sentinel& x);

template<bool OtherConst = !Const>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const CI<OtherConst>& y, const sentinel& x);
```

*Effects:* Equivalent to:
`return y.count() == 0 || y.base() == x.`*`end_`*`;`

### Take while view <a id="range.take.while">[[range.take.while]]</a>

#### Overview <a id="range.take.while.overview">[[range.take.while.overview]]</a>

Given a unary predicate `pred` and a view `r`, `take_while_view`
produces a view of the range \[`ranges::be``gin(r)`,
`ranges::find_if_not(r, pred)`).

The name `views::take_while` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::take_while(E, F)` is expression-equivalent to
`take_while_view(E, F)`.

\[*Example 1*:

``` cpp
auto input = istringstream{"0 1 2 3 4 5 6 7 8 9"};
auto small = [](const auto x) noexcept { return x < 5; };
auto small_ints = views::istream<int>(input) | views::take_while(small);
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
    movable-box<Pred> pred_;                            // exposition only

  public:
    take_while_view() requires default_initializable<V> && default_initializable<Pred> = default;
    constexpr explicit take_while_view(V base, Pred pred);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr const Pred& pred() const;

    constexpr auto begin() requires (!simple-view<V>)
    { return ranges::begin(base_); }

    constexpr auto begin() const
      requires range<const V> &&
               indirect_unary_predicate<const Pred, iterator_t<const V>>
    { return ranges::begin(base_); }

    constexpr auto end() requires (!simple-view<V>)
    { return sentinel<false>(ranges::end(base_), addressof(*pred_)); }

    constexpr auto end() const
      requires range<const V> &&
               indirect_unary_predicate<const Pred, iterator_t<const V>>
    { return sentinel<true>(ranges::end(base_), addressof(*pred_)); }
  };

  template<class R, class Pred>
    take_while_view(R&&, Pred) -> take_while_view<views::all_t<R>, Pred>;
}
```

``` cpp
constexpr explicit take_while_view(V base, Pred pred);
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
  class take_while_view<V, Pred>::sentinel {
    using Base = maybe-const<Const, V>;                 // exposition only

    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only
    const Pred* pred_ = nullptr;                        // exposition only

  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end, const Pred* pred);
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const { return end_; }

    friend constexpr bool operator==(const iterator_t<Base>& x, const sentinel& y);

    template<bool OtherConst = !Const>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator_t<maybe-const<OtherConst, V>>& x,
                                     const sentinel& y);
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

*Effects:* Initializes *end\_* with `std::move(s.`*`end_`*`)` and
*pred\_* with `s.`*`pred_`*.

``` cpp
friend constexpr bool operator==(const iterator_t<Base>& x, const sentinel& y);

template<bool OtherConst = !Const>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator_t<maybe-const<OtherConst, V>>& x,
                                 const sentinel& y);
```

*Effects:* Equivalent to:
`return y.`*`end_`*` == x || !invoke(*y.`*`pred_`*`, *x);`

### Drop view <a id="range.drop">[[range.drop]]</a>

#### Overview <a id="range.drop.overview">[[range.drop.overview]]</a>

`drop_view` produces a view excluding the first N elements from another
view, or an empty range if the adapted view contains fewer than N
elements.

The name `views::drop` denotes a range adaptor object
[[range.adaptor.object]]. Let `E` and `F` be expressions, let `T` be
`remove_cvref_t<decltype((E))>`, and let `D` be
`range_difference_t<decltype((E))>`. If `decltype((F))` does not model
`convertible_to<D>`, `views::drop(E, F)` is ill-formed. Otherwise, the
expression `views::drop(E, F)` is expression-equivalent to:

- If `T` is a specialization of `empty_view` [[range.empty.view]], then
  `((void)F, decay-copy(E))`, except that the evaluations of `E` and `F`
  are indeterminately sequenced.
- Otherwise, if `T` models `random_access_range` and `sized_range` and
  is
  - a specialization of `span` [[views.span]],
  - a specialization of `basic_string_view` [[string.view]],
  - a specialization of `iota_view` [[range.iota.view]], or
  - a specialization of `subrange` [[range.subrange]] where
    `T::StoreSize` is `false`,

  then
  `U(ranges::begin(E) + std::min<D>(ranges::distance(E), F), ranges::end(E))`,
  except that `E` is evaluated only once, where `U` is
  `span<typename T::element_type>` if `T` is a specialization of `span`
  and `T` otherwise.
- Otherwise, if `T` is a specialization of `subrange` [[range.subrange]]
  that models `random_access_range` and `sized_range`, then
  `T(ranges::begin(E) + std::min<D>(ranges::distance(E), F), ranges::\linebreak{}end(E),
  to-unsigned-like(ranges::distance(E) -
  std::min<D>(ranges::distance(E), F)))`, except that `E` and `F` are
  each evaluated only once.
- Otherwise, if `T` is a specialization of `repeat_view`
  [[range.repeat.view]]:
  - if `T` models `sized_range`, then
    ``` cpp
    views::repeat(*E.value_, ranges::distance(E) - std::min<D>(ranges::distance(E), F))
    ```

    except that `E` is evaluated only once;
  - otherwise, `((void)F, decay-copy(E))`, except that the evaluations
    of `E` and `F` are indeterminately sequenced.
- Otherwise, `drop_view(E, F)`.

\[*Example 1*:

``` cpp
auto ints = views::iota(0) | views::take(10);
for (auto i : ints | views::drop(5)) {
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
    drop_view() requires default_initializable<V> = default;
    constexpr explicit drop_view(V base, range_difference_t<V> count);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin()
      requires (!(simple-view<V> &&
                  random_access_range<const V> && sized_range<const V>));
    constexpr auto begin() const
      requires random_access_range<const V> && sized_range<const V>;

    constexpr auto end() requires (!simple-view<V>)
    { return ranges::end(base_); }

    constexpr auto end() const requires range<const V>
    { return ranges::end(base_); }

    constexpr auto size() requires sized_range<V> {
      const auto s = ranges::size(base_);
      const auto c = static_cast<decltype(s)>(count_);
      return s < c ? 0 : s - c;
    }

    constexpr auto size() const requires sized_range<const V> {
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
constexpr explicit drop_view(V base, range_difference_t<V> count);
```

*Preconditions:* `count >= 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *count\_*
with `count`.

``` cpp
constexpr auto begin()
  requires (!(simple-view<V> &&
              random_access_range<const V> && sized_range<const V>));
constexpr auto begin() const
  requires random_access_range<const V> && sized_range<const V>;
```

*Returns:*
`ranges::next(ranges::begin(`*`base_`*`), `*`count_`*`, ranges::end(`*`base_`*`))`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept when `drop_view` models `forward_range`,
the first overload caches the result within the `drop_view` for use on
subsequent calls.

\[*Note 1*: Without this, applying a `reverse_view` over a `drop_view`
would have quadratic iteration complexity. — *end note*\]

### Drop while view <a id="range.drop.while">[[range.drop.while]]</a>

#### Overview <a id="range.drop.while.overview">[[range.drop.while.overview]]</a>

Given a unary predicate `pred` and a view `r`, `drop_while_view`
produces a view of the range \[`ranges::find_if_not(r, pred)`,
`ranges::end(r)`).

The name `views::drop_while` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::drop_while(E, F)` is expression-equivalent to
`drop_while_view(E, F)`.

\[*Example 1*:

``` cpp
constexpr auto source = "  \t   \t   \t   hello there"sv;
auto is_invisible = [](const auto x) { return x == ' ' || x == '\t'; };
auto skip_ws = views::drop_while(source, is_invisible);
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
    drop_while_view() requires default_initializable<V> && default_initializable<Pred> = default;
    constexpr explicit drop_while_view(V base, Pred pred);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr const Pred& pred() const;

    constexpr auto begin();

    constexpr auto end() { return ranges::end(base_); }

  private:
    V base_ = V();                                      // exposition only
    movable-box<Pred> pred_; \itcorr[-1]                           // exposition only
  };

  template<class R, class Pred>
    drop_while_view(R&&, Pred) -> drop_while_view<views::all_t<R>, Pred>;
}
```

``` cpp
constexpr explicit drop_while_view(V base, Pred pred);
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

*Preconditions:* *`pred_`*`.has_value()` is `true`.

*Returns:* `ranges::find_if_not(`*`base_`*`, cref(*`*`pred_`*`))`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept when `drop_while_view` models
`forward_range`, the first call caches the result within the
`drop_while_view` for use on subsequent calls.

\[*Note 1*: Without this, applying a `reverse_view` over a
`drop_while_view` would have quadratic iteration
complexity. — *end note*\]

### Join view <a id="range.join">[[range.join]]</a>

#### Overview <a id="range.join.overview">[[range.join.overview]]</a>

`join_view` flattens a view of ranges into a view.

The name `views::join` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::join(E)` is expression-equivalent to
`join_view<views::all_t<decltype((E))>>{E}`.

\[*Example 1*:

``` cpp
vector<string> ss{"hello", " ", "world", "!"};
for (char ch : ss | views::join)
  cout << ch;                                   // prints hello world!
```

— *end example*\]

#### Class template `join_view` <a id="range.join.view">[[range.join.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>>
  class join_view : public view_interface<join_view<V>> {
  private:
    using InnerRng = range_reference_t<V>;                  // exposition only

    // [range.join.iterator], class template join_view::iterator
    template<bool Const>
      struct iterator;                                      // exposition only

    // [range.join.sentinel], class template join_view::sentinel
    template<bool Const>
      struct sentinel;                                      // exposition only

    V base_ = V();                                          // exposition only

    non-propagating-cache<iterator_t<V>> outer_;            // exposition only, present only
                                                            // when !forward_range<V>
    non-propagating-cache<remove_cv_t<InnerRng>> inner_;    // exposition only, present only
                                                            // if is_reference_v<InnerRng> is false

  public:
    join_view() requires default_initializable<V> = default;
    constexpr explicit join_view(V base);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() {
      if constexpr (forward_range<V>) {
        constexpr bool use_const = simple-view<V> &&
                                   is_reference_v<InnerRng>;
        return iterator<use_const>{*this, ranges::begin(base_)};
      } else {
        outer_ = ranges::begin(base_);
        return iterator<false>{*this};
      }
    }

    constexpr auto begin() const
      requires forward_range<const V> &&
               is_reference_v<range_reference_t<const V>> &&
               input_range<range_reference_t<const V>>
    { return iterator<true>{*this, ranges::begin(base_)}; }

    constexpr auto end() {
      if constexpr (forward_range<V> &&
                    is_reference_v<InnerRng> && forward_range<InnerRng> &&
                    common_range<V> && common_range<InnerRng>)
        return iterator<simple-view<V>>{*this, ranges::end(base_)};
      else
        return sentinel<simple-view<V>>{*this};
    }

    constexpr auto end() const
      requires forward_range<const V> &&
               is_reference_v<range_reference_t<const V>> &&
               input_range<range_reference_t<const V>> {
      if constexpr (forward_range<range_reference_t<const V>> &&
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
    requires view<V> && input_range<range_reference_t<V>>
  template<bool Const>
  struct join_view<V>::iterator {
  private:
    using Parent    = maybe-const<Const, join_view>;            // exposition only
    using Base      = maybe-const<Const, V>;                    // exposition only
    using OuterIter = iterator_t<Base>;                         // exposition only
    using InnerIter = iterator_t<range_reference_t<Base>>;      // exposition only

    static constexpr bool ref-is-glvalue =                      // exposition only
      is_reference_v<range_reference_t<Base>>;

    OuterIter outer_ = OuterIter();                     // exposition only, present only
                                                        // if Base models forward_range
    optional<InnerIter> inner_;                                 // exposition only
    Parent* parent_  = nullptr;                                 // exposition only

    constexpr void satisfy();                                   // exposition only

    constexpr OuterIter& outer();                               // exposition only
    constexpr const OuterIter& outer() const;                   // exposition only

    constexpr iterator(Parent& parent, OuterIter outer)
      requires forward_range<Base>;                             // exposition only
    constexpr explicit iterator(Parent& parent)
      requires (!forward_range<Base>);                          // exposition only

  public:
    using iterator_concept  = see below;
    using iterator_category = see below;                        // not always present
    using value_type        = range_value_t<range_reference_t<Base>>;
    using difference_type   = see below;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const &&
               convertible_to<iterator_t<V>, OuterIter> &&
               convertible_to<iterator_t<InnerRng>, InnerIter>;

    constexpr decltype(auto) operator*() const { return **inner_; }

    constexpr InnerIter operator->() const
      requires has-arrow<InnerIter> && copyable<InnerIter>;

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
      requires ref-is-glvalue && forward_range<Base> &&
               equality_comparable<iterator_t<range_reference_t<Base>>>;

    friend constexpr decltype(auto) iter_move(const iterator& i)
    noexcept(noexcept(ranges::iter_move(*i.inner_))) {
      return ranges::iter_move(*i.inner_);
    }

    friend constexpr void iter_swap(const iterator& x, const iterator& y)
      noexcept(noexcept(ranges::iter_swap(*x.inner_, *y.inner_)))
      requires indirectly_swappable<InnerIter>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *ref-is-glvalue* is `true`, *Base* models `bidirectional_range`,
  and `range_reference_t<Base>` models both `bidirectional_range` and
  `common_range`, then `iterator_concept` denotes
  `bidirectional_iterator_tag`.
- Otherwise, if *ref-is-glvalue* is `true` and *Base* and
  `range_reference_t<Base>` each model
  \libconceptx{forward_range}{forward_range}, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

The member *typedef-name* `iterator_category` is defined if and only if
*ref-is-glvalue* is `true`, *Base* models `forward_range`, and
`range_reference_t<Base>` models `forward_range`. In that case,
`iterator::iterator_category` is defined as follows:

- Let *OUTERC* denote
  `iterator_traits<iterator_t<Base>>::iterator_category`, and let
  *INNERC* denote
  `iterator_traits<iterator_t<range_reference_t<Base>>>::iterator_category`.
- If *OUTERC* and *INNERC* each model
  `derived_from<bidirectional_iterator_tag>` and
  `range_reference_t<Base>` models `common_range`, `iterator_category`
  denotes `bidirectional_iterator_tag`.
- Otherwise, if *OUTERC* and *INNERC* each model
  `derived_from<forward_iterator_tag>`, `iterator_category` denotes
  `forward_iterator_tag`.
- Otherwise, `iterator_category` denotes `input_iterator_tag`.

`iterator::difference_type` denotes the type:

``` cpp
common_type_t<
  range_difference_t<Base>,
  range_difference_t<range_reference_t<Base>>>
```

`join_view` iterators use the *satisfy* function to skip over empty
inner ranges.

``` cpp
constexpr OuterIter& outer();
constexpr const OuterIter& outer() const;
```

*Returns:* *outer\_* if *Base* models `forward_range`; otherwise,
`*`*`parent_`*`->`*`outer_`*.

``` cpp
constexpr void satisfy();
```

*Effects:* Equivalent to:

``` cpp
auto update_inner = [this](const iterator_t<Base>& x) -> auto&& {
  if constexpr (ref-is-glvalue)     // *x is a reference
    return *x;
  else
    return parent_->inner_.emplace-deref(x);
};

for (; outer() != ranges::end(parent_->base_); ++outer()) {
  auto&& inner = update_inner(outer());
  inner_ = ranges::begin(inner);
  if (*inner_ != ranges::end(inner))
    return;
}
if constexpr (ref-is-glvalue)
  inner_.reset();
```

``` cpp
constexpr iterator(Parent& parent, OuterIter outer)
  requires forward_range<Base>;
```

*Effects:* Initializes *outer\_* with `std::move(outer)` and *parent\_*
with `addressof(parent)`; then calls *`satisfy`*`()`.

``` cpp
constexpr explicit iterator(Parent& parent)
  requires (!forward_range<Base>);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`; then calls
*`satisfy`*`()`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const &&
           convertible_to<iterator_t<V>, OuterIter> &&
           convertible_to<iterator_t<InnerRng>, InnerIter>;
```

*Effects:* Initializes *outer\_* with `std::move(i.`*`outer_`*`)`,
*inner\_* with `std::move(i.`*`inner_`*`)`, and *parent\_* with
`i.`*`parent_`*.

\[*Note 1*: `Const` can only be `true` when *Base* models
`forward_range`. — *end note*\]

``` cpp
constexpr InnerIter operator->() const
  requires has-arrow<InnerIter> && copyable<InnerIter>;
```

*Effects:* Equivalent to: `return *`*`inner_`*`;`

``` cpp
constexpr iterator& operator++();
```

Let *`inner-range`* be:

- If *ref-is-glvalue* is `true`, `*`*`outer`*`()`.
- Otherwise, `*`*`parent_`*`->`*`inner_`*.

*Effects:* Equivalent to:

``` cpp
if (++*inner_ == ranges::end(as-lvalue(inner-range))) {
  ++outer();
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
  inner_ = ranges::end(as-lvalue(*--outer_));
while (*inner_ == ranges::begin(as-lvalue(*outer_)))
  *inner_ = ranges::end(as-lvalue(*--outer_));
--*inner_;
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
  requires ref-is-glvalue && forward_range<Base> &&
           equality_comparable<iterator_t<range_reference_t<Base>>>;
```

*Effects:* Equivalent to:
`return x.`*`outer_`*` == y.`*`outer_`*` && x.`*`inner_`*` == y.`*`inner_`*`;`

``` cpp
friend constexpr void iter_swap(const iterator& x, const iterator& y)
  noexcept(noexcept(ranges::iter_swap(*x.inner_, *y.inner_)))
  requires indirectly_swappable<InnerIter>;
```

*Effects:* Equivalent to:
`return ranges::iter_swap(*x.`*`inner_`*`, *y.`*`inner_`*`);`

#### Class template `join_view::sentinel` <a id="range.join.sentinel">[[range.join.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V> && input_range<range_reference_t<V>>
  template<bool Const>
  struct join_view<V>::sentinel {
  private:
    using Parent = maybe-const<Const, join_view>;       // exposition only
    using Base = maybe-const<Const, V>;                 // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only

  public:
    sentinel() = default;

    constexpr explicit sentinel(Parent& parent);
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    template<bool OtherConst>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
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
template<bool OtherConst>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`outer`*`() == y.`*`end_`*`;`

### Join with view <a id="range.join.with">[[range.join.with]]</a>

#### Overview <a id="range.join.with.overview">[[range.join.with.overview]]</a>

`join_with_view` takes a view and a delimiter, and flattens the view,
inserting every element of the delimiter in between elements of the
view. The delimiter can be a single element or a view of elements.

The name `views::join_with` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::join_with(E, F)` is expression-equivalent to
`join_with_view(E, F)`.

\[*Example 1*:

``` cpp
vector<string> vs = {"the", "quick", "brown", "fox"};
for (char c : vs | views::join_with('-')) {
  cout << c;
}
// The above prints the-quick-brown-fox
```

— *end example*\]

#### Class template `join_with_view` <a id="range.join.with.view">[[range.join.with.view]]</a>

``` cpp
namespace std::ranges {
  template<class R, class P>
  concept compatible-joinable-ranges =            // exposition only
      common_with<range_value_t<R>, range_value_t<P>> &&
      common_reference_with<range_reference_t<R>, range_reference_t<P>> &&
      common_reference_with<range_rvalue_reference_t<R>, range_rvalue_reference_t<P>>;

  template<class R>
  concept bidirectional-common = bidirectional_range<R> && common_range<R>;    // exposition only

  template<input_range V, forward_range Pattern>
    requires view<V> && input_range<range_reference_t<V>>
          && view<Pattern>
          && compatible-joinable-ranges<range_reference_t<V>, Pattern>
  class join_with_view : public view_interface<join_with_view<V, Pattern>> {
    using InnerRng = range_reference_t<V>;                  // exposition only

    V base_ = V();                                          // exposition only
    non-propagating-cache<iterator_t<V>> outer_it_;         // exposition only, present only
                                                            // when !forward_range<V>
    non-propagating-cache<remove_cv_t<InnerRng>> inner_;   // exposition only, present only
                                                            // if is_reference_v<InnerRng> is false
    Pattern pattern_ = Pattern();                           // exposition only

    // [range.join.with.iterator], class template join_with_view::iterator
    template<bool Const> struct iterator;                   // exposition only

    // [range.join.with.sentinel], class template join_with_view::sentinel
    template<bool Const> struct sentinel;                   // exposition only

  public:
    join_with_view()
      requires default_initializable<V> && default_initializable<Pattern> = default;

    constexpr explicit join_with_view(V base, Pattern pattern);

    template<input_range R>
      requires constructible_from<V, views::all_t<R>> &&
               constructible_from<Pattern, single_view<range_value_t<InnerRng>>>
    constexpr explicit join_with_view(R&& r, range_value_t<InnerRng> e);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() {
      if constexpr (forward_range<V>) {
        constexpr bool use_const =
          simple-view<V> && is_reference_v<InnerRng> && simple-view<Pattern>;
        return iterator<use_const>{*this, ranges::begin(base_)};
      }
      else {
        outer_it_ = ranges::begin(base_);
        return iterator<false>{*this};
      }
    }
    constexpr auto begin() const
      requires forward_range<const V> &&
               forward_range<const Pattern> &&
               is_reference_v<range_reference_t<const V>> &&
               input_range<range_reference_t<const V>> {
      return iterator<true>{*this, ranges::begin(base_)};
    }

    constexpr auto end() {
      if constexpr (forward_range<V> &&
                    is_reference_v<InnerRng> && forward_range<InnerRng> &&
                    common_range<V> && common_range<InnerRng>)
        return iterator<simple-view<V> && simple-view<Pattern>>{*this, ranges::end(base_)};
      else
        return sentinel<simple-view<V> && simple-view<Pattern>>{*this};
    }
    constexpr auto end() const
      requires forward_range<const V> && forward_range<const Pattern> &&
               is_reference_v<range_reference_t<const V>> &&
               input_range<range_reference_t<const V>> {
      using InnerConstRng = range_reference_t<const V>;
      if constexpr (forward_range<InnerConstRng> &&
                    common_range<const V> && common_range<InnerConstRng>)
        return iterator<true>{*this, ranges::end(base_)};
      else
        return sentinel<true>{*this};
    }
  };

  template<class R, class P>
    join_with_view(R&&, P&&) -> join_with_view<views::all_t<R>, views::all_t<P>>;

  template<input_range R>
    join_with_view(R&&, range_value_t<range_reference_t<R>>)
      -> join_with_view<views::all_t<R>, single_view<range_value_t<range_reference_t<R>>>>;
}
```

``` cpp
constexpr explicit join_with_view(V base, Pattern pattern);
```

*Effects:* Initializes *base\_* with `std::move(base)` and *pattern\_*
with `std::move(pattern)`.

``` cpp
template<input_range R>
  requires constructible_from<V, views::all_t<R>> &&
           constructible_from<Pattern, single_view<range_value_t<InnerRng>>>
constexpr explicit join_with_view(R&& r, range_value_t<InnerRng> e);
```

*Effects:* Initializes *base\_* with `views::all(std::forward<R>(r))`
and *pattern\_* with `views::sin``gle(std::move(e))`.

#### Class template `join_with_view::iterator` <a id="range.join.with.iterator">[[range.join.with.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && input_range<range_reference_t<V>>
          && view<Pattern> && compatible-joinable-ranges<range_reference_t<V>, Pattern>
  template<bool Const>
  class join_with_view<V, Pattern>::iterator {
    using Parent = maybe-const<Const, join_with_view>;                  // exposition only
    using Base = maybe-const<Const, V>;                                 // exposition only
    using InnerBase = range_reference_t<Base>;                          // exposition only
    using PatternBase = maybe-const<Const, Pattern>;                    // exposition only

    using OuterIter = iterator_t<Base>;                                 // exposition only
    using InnerIter = iterator_t<InnerBase>;                            // exposition only
    using PatternIter = iterator_t<PatternBase>;                        // exposition only

    static constexpr bool ref-is-glvalue = is_reference_v<InnerBase>;   // exposition only

    Parent* parent_ = nullptr;                                          // exposition only
    OuterIter outer_it_ = OuterIter();                          // exposition only, present only
                                                                // if Base models forward_range
    variant<PatternIter, InnerIter> inner_it_;                          // exposition only

    constexpr iterator(Parent& parent, OuterIter outer)
      requires forward_range<Base>;                                     // exposition only
    constexpr explicit iterator(Parent& parent)
      requires (!forward_range<Base>);                                  // exposition only
    constexpr OuterIter& outer();                                       // exposition only
    constexpr const OuterIter& outer() const;                           // exposition only
    constexpr auto& update-inner();                                     // exposition only
    constexpr auto& get-inner();                                        // exposition only
    constexpr void satisfy();                                           // exposition only

  public:
    using iterator_concept = see below;
    using iterator_category = see below;                                // not always present
    using value_type = see below;
    using difference_type = see below;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, OuterIter> &&
               convertible_to<iterator_t<InnerRng>, InnerIter> &&
               convertible_to<iterator_t<Pattern>, PatternIter>;

    constexpr decltype(auto) operator*() const;

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int)
      requires ref-is-glvalue && forward_iterator<OuterIter> &&
               forward_iterator<InnerIter>;

    constexpr iterator& operator--()
      requires ref-is-glvalue && bidirectional_range<Base> &&
               bidirectional-common<InnerBase> && bidirectional-common<PatternBase>;
    constexpr iterator operator--(int)
      requires ref-is-glvalue && bidirectional_range<Base> &&
               bidirectional-common<InnerBase> && bidirectional-common<PatternBase>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires ref-is-glvalue && forward_range<Base> &&
               equality_comparable<InnerIter>;

    friend constexpr decltype(auto) iter_move(const iterator& x) {
      using rvalue_reference = common_reference_t<
        iter_rvalue_reference_t<InnerIter>,
        iter_rvalue_reference_t<PatternIter>>;
      return visit<rvalue_reference>(ranges::iter_move, x.inner_it_);
    }

    friend constexpr void iter_swap(const iterator& x, const iterator& y)
      requires indirectly_swappable<InnerIter, PatternIter> {
      visit(ranges::iter_swap, x.inner_it_, y.inner_it_);
    }
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *ref-is-glvalue* is `true`, *Base* models `bidirectional_range`,
  and *InnerBase* and *PatternBase* each model `bidirectional-common`,
  then `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if *ref-is-glvalue* is `true` and *Base* and *InnerBase*
  each model `forward_range`, then `iterator_concept` denotes
  `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

The member *typedef-name* `iterator_category` is defined if and only if
*ref-is-glvalue* is `true`, and *Base* and *InnerBase* each model
`forward_range`. In that case, `iterator::iterator_category` is defined
as follows:

- Let *OUTERC* denote `iterator_traits<OuterIter>::iterator_category`,
  let *INNERC* denote `iterator_traits<InnerIter>::iterator_category`,
  and let *PATTERNC* denote
  `iterator_-\linebreak traits<PatternIter>::iterator_category`.
- If
  ``` cpp
  is_reference_v<common_reference_t<iter_reference_t<InnerIter>,
                                    iter_reference_t<PatternIter>>>
  ```

  is `false`, `iterator_category` denotes `input_iterator_tag`.
- Otherwise, if *OUTERC*, *INNERC*, and *PATTERNC* each model
  `derived_from<bidirectional_iterator_category>` and *InnerBase* and
  *PatternBase* each model `common_range`, `iterator_category` denotes
  `bidirectional_iterator_tag`.
- Otherwise, if *OUTERC*, *INNERC*, and *PATTERNC* each model
  `derived_from<forward_iterator_tag>`, `iterator_category` denotes
  `forward_iterator_tag`.
- Otherwise, `iterator_category` denotes `input_iterator_tag`.

`iterator::value_type` denotes the type:

``` cpp
common_type_t<iter_value_t<InnerIter>, iter_value_t<PatternIter>>
```

`iterator::difference_type` denotes the type:

``` cpp
common_type_t<
    iter_difference_t<OuterIter>,
    iter_difference_t<InnerIter>,
    iter_difference_t<PatternIter>>
```

``` cpp
constexpr OuterIter& outer();
constexpr const OuterIter& outer() const;
```

*Returns:* *outer_it\_* if *Base* models `forward_range`; otherwise,
`*`*`parent_`*`->`*`outer_it_`*.

``` cpp
constexpr auto& update-inner();
```

*Effects:* Equivalent to:

``` cpp
if constexpr (ref-is-glvalue)
  return as-lvalue(*outer());
else
  return parent_->inner_.emplace-deref(outer());
```

``` cpp
constexpr auto& get-inner();
```

*Effects:* Equivalent to:

``` cpp
if constexpr (ref-is-glvalue)
  return as-lvalue(*outer());
else
  return *parent_->inner_;
```

``` cpp
constexpr void satisfy();
```

*Effects:* Equivalent to:

``` cpp
while (true) {
  if (inner_it_.index() == 0) {
    if (std::get<0>(inner_it_) != ranges::end(parent_->pattern_))
      break;
    inner_it_.emplace<1>(ranges::begin(update-inner()));
  } else {
    if (std::get<1>(inner_it_) != ranges::end(get-inner()))
      break;
    if (++outer() == ranges::end(parent_->base_)) {
      if constexpr (ref-is-glvalue)
        inner_it_.emplace<0>();
      break;
    }
    inner_it_.emplace<0>(ranges::begin(parent_->pattern_));
  }
}
```

\[*Note 1*: `join_with_view` iterators use the *satisfy* function to
skip over empty inner ranges. — *end note*\]

``` cpp
constexpr iterator(Parent& parent, OuterIter outer)
  requires forward_range<Base>;
constexpr explicit iterator(Parent& parent)
  requires (!forward_range<Base>);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`. For the
first overload, also initializes *outer_it\_* with `std::move(outer)`.
Then, equivalent to:

``` cpp
if (outer() != ranges::end(parent_->base_)) {
  inner_it_.emplace<1>(ranges::begin(update-inner()));
  satisfy();
}
```

``` cpp
constexpr iterator(iterator<!Const> i)
    requires Const && convertible_to<iterator_t<V>, OuterIter> &&
             convertible_to<iterator_t<InnerRng>, InnerIter> &&
             convertible_to<iterator_t<Pattern>, PatternIter>;
```

*Effects:* Initializes *outer_it\_* with `std::move(i.`*`outer_it_`*`)`
and *parent\_* with `i.`*`parent_`*. Then, equivalent to:

``` cpp
if (i.inner_it_.index() == 0)
  inner_it_.emplace<0>(std::get<0>(std::move(i.inner_it_)));
else
  inner_it_.emplace<1>(std::get<1>(std::move(i.inner_it_)));
```

\[*Note 2*: `Const` can only be `true` when *Base* models
`forward_range`. — *end note*\]

``` cpp
constexpr decltype(auto) operator*() const;
```

*Effects:* Equivalent to:

``` cpp
using reference =
  common_reference_t<iter_reference_t<InnerIter>, iter_reference_t<PatternIter>>;
return visit([](auto& it) -> reference { return *it; }, inner_it_);
```

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
visit([](auto& it){ ++it; }, inner_it_);
satisfy();
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
constexpr iterator operator++(int)
  requires ref-is-glvalue && forward_iterator<OuterIter> && forward_iterator<InnerIter>;
```

*Effects:* Equivalent to:

``` cpp
iterator tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--()
  requires ref-is-glvalue && bidirectional_range<Base> &&
           bidirectional-common<InnerBase> && bidirectional-common<PatternBase>;
```

*Effects:* Equivalent to:

``` cpp
if (outer_it_ == ranges::end(parent_->base_)) {
  auto&& inner = *--outer_it_;
  inner_it_.emplace<1>(ranges::end(inner));
}

while (true) {
  if (inner_it_.index() == 0) {
    auto& it = std::get<0>(inner_it_);
    if (it == ranges::begin(parent_->pattern_)) {
      auto&& inner = *--outer_it_;
      inner_it_.emplace<1>(ranges::end(inner));
    } else {
      break;
    }
  } else {
    auto& it = std::get<1>(inner_it_);
    auto&& inner = *outer_it_;
    if (it == ranges::begin(inner)) {
      inner_it_.emplace<0>(ranges::end(parent_->pattern_));
    } else {
      break;
    }
  }
}
visit([](auto& it){ --it; }, inner_it_);
return *this;
```

``` cpp
constexpr iterator operator--(int)
  requires ref-is-glvalue && bidirectional_range<Base> &&
           bidirectional-common<InnerBase> && bidirectional-common<PatternBase>;
```

*Effects:* Equivalent to:

``` cpp
iterator tmp = *this;
--*this;
return tmp;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires ref-is-glvalue && forward_range<Base> &&
           equality_comparable<InnerIter>;
```

*Effects:* Equivalent to:

``` cpp
return x.outer_it_ == y.outer_it_ && x.inner_it_ == y.inner_it_;
```

#### Class template `join_with_view::sentinel` <a id="range.join.with.sentinel">[[range.join.with.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && input_range<range_reference_t<V>>
          && view<Pattern> && compatible-joinable-ranges<range_reference_t<V>, Pattern>
  template<bool Const>
  class join_with_view<V, Pattern>::sentinel {
    using Parent = maybe-const<Const, join_with_view>;  // exposition only
    using Base = maybe-const<Const, V>;                 // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only

    constexpr explicit sentinel(Parent& parent);        // exposition only

  public:
    sentinel() = default;
    constexpr sentinel(sentinel<!Const> s)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    template<bool OtherConst>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
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
template<bool OtherConst>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`outer`*`() == y.`*`end_`*`;`

### Lazy split view <a id="range.lazy.split">[[range.lazy.split]]</a>

#### Overview <a id="range.lazy.split.overview">[[range.lazy.split.overview]]</a>

`lazy_split_view` takes a view and a delimiter, and splits the view into
subranges on the delimiter. The delimiter can be a single element or a
view of elements.

The name `views::lazy_split` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::lazy_split(E, F)` is expression-equivalent to
`lazy_split_view(E, F)`.

\[*Example 1*:

``` cpp
string str{"the quick brown fox"};
for (auto word : str | views::lazy_split(' ')) {
  for (char ch : word)
    cout << ch;
  cout << '*';
}
// The above prints the*quick*brown*fox*
```

— *end example*\]

#### Class template `lazy_split_view` <a id="range.lazy.split.view">[[range.lazy.split.view]]</a>

``` cpp
namespace std::ranges {
  template<auto> struct require-constant;                       // exposition only

  template<class R>
  concept \defexposconceptnc{tiny-range} =                                          // exposition only
    sized_range<R> &&
    requires { typename require-constant<remove_reference_t<R>::size()>; } &&
    (remove_reference_t<R>::size() <= 1);

  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  class lazy_split_view : public view_interface<lazy_split_view<V, Pattern>> {
  private:
    V base_ = V();                                              // exposition only
    Pattern pattern_ = Pattern();                               // exposition only

    non-propagating-cache<iterator_t<V>> current_;              // exposition only, present only
                                                                // if forward_range<V> is false

    // [range.lazy.split.outer], class template lazy_split_view::outer-iterator
    template<bool> struct outer-iterator;                       // exposition only

    // [range.lazy.split.inner], class template lazy_split_view::inner-iterator
    template<bool> struct inner-iterator;                       // exposition only

  public:
    lazy_split_view()
      requires default_initializable<V> && default_initializable<Pattern> = default;
    constexpr explicit lazy_split_view(V base, Pattern pattern);

    template<input_range R>
      requires constructible_from<V, views::all_t<R>> &&
               constructible_from<Pattern, single_view<range_value_t<R>>>
    constexpr explicit lazy_split_view(R&& r, range_value_t<R> e);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() {
      if constexpr (forward_range<V>) {
        return outer-iterator<simple-view<V> && simple-view<Pattern>>
          {*this, ranges::begin(base_)};
      } else {
        current_ = ranges::begin(base_);
        return outer-iterator<false>{*this};
      }
    }

    constexpr auto begin() const requires forward_range<V> && forward_range<const V> {
      return outer-iterator<true>{*this, ranges::begin(base_)};
    }

    constexpr auto end() requires forward_range<V> && common_range<V> {
      return outer-iterator<simple-view<V> && simple-view<Pattern>>
        {*this, ranges::end(base_)};
    }

    constexpr auto end() const {
      if constexpr (forward_range<V> && forward_range<const V> && common_range<const V>)
        return outer-iterator<true>{*this, ranges::end(base_)};
      else
        return default_sentinel;
    }
  };

  template<class R, class P>
    lazy_split_view(R&&, P&&) -> lazy_split_view<views::all_t<R>, views::all_t<P>>;

  template<input_range R>
    lazy_split_view(R&&, range_value_t<R>)
      -> lazy_split_view<views::all_t<R>, single_view<range_value_t<R>>>;
}
```

``` cpp
constexpr explicit lazy_split_view(V base, Pattern pattern);
```

*Effects:* Initializes *base\_* with `std::move(base)`, and *pattern\_*
with `std::move(pattern)`.

``` cpp
template<input_range R>
  requires constructible_from<V, views::all_t<R>> &&
           constructible_from<Pattern, single_view<range_value_t<R>>>
constexpr explicit lazy_split_view(R&& r, range_value_t<R> e);
```

*Effects:* Initializes *base\_* with `views::all(std::forward<R>(r))`,
and *pattern\_* with `views::``single(std::move(e))`.

#### Class template `lazy_split_view::outer-iterator` <a id="range.lazy.split.outer">[[range.lazy.split.outer]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  template<bool Const>
  struct lazy_split_view<V, Pattern>::outer-iterator {
  private:
    using Parent = maybe-const<Const, lazy_split_view>;     // exposition only
    using Base = maybe-const<Const, V>;                     // exposition only
    Parent* parent_ = nullptr;                              // exposition only

    iterator_t<Base> current_ = iterator_t<Base>();         // exposition only, present only
                                                            // if V models forward_range

    bool trailing_empty_ = false;                           // exposition only

  public:
    using iterator_concept  =
      conditional_t<forward_range<Base>, forward_iterator_tag, input_iterator_tag>;

    using iterator_category = input_iterator_tag;           // present only if Base
                                                            // models forward_range

    // [range.lazy.split.outer.value], class lazy_split_view::outer-iterator::value_type
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

Many of the specifications in [[range.lazy.split]] refer to the notional
member *current* of *outer-iterator*. *current* is equivalent to
*current\_* if `V` models `forward_range`, and `*parent_->current_`
otherwise.

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
if (current == end) {
  trailing_empty_ = false;
  return *this;
}
const auto [pbegin, pend] = subrange{parent_->pattern_};
if (pbegin == pend) ++current;
else if constexpr (tiny-range<Pattern>) {
  current = ranges::find(std::move(current), end, *pbegin);
  if (current != end) {
    ++current;
    if (current == end)
      trailing_empty_ = true;
  }
}
else {
  do {
    auto [b, p] = ranges::mismatch(current, end, pbegin, pend);
    if (p == pend) {
      current = b;
      if (current == end)
        trailing_empty_ = true;
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

*Effects:* Equivalent to:

``` cpp
return x.current_ == y.current_ && x.trailing_empty_ == y.trailing_empty_;
```

``` cpp
friend constexpr bool operator==(const outer-iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to:

``` cpp
return x.current == ranges::end(x.parent_->base_) && !x.trailing_empty_;
```

#### Class `lazy_split_view::outer-iterator::value_type` <a id="range.lazy.split.outer.value">[[range.lazy.split.outer.value]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  template<bool Const>
  struct lazy_split_view<V, Pattern>::outer-iterator<Const>::value_type
    : view_interface<value_type> {
  private:
    outer-iterator i_ = outer-iterator();               // exposition only

  public:
    value_type() = default;
    constexpr explicit value_type(outer-iterator i);

    constexpr inner-iterator<Const> begin() const;
    constexpr default_sentinel_t end() const noexcept;
  };
}
```

``` cpp
constexpr explicit value_type(outer-iterator i);
```

*Effects:* Initializes *i\_* with `std::move(i)`.

``` cpp
constexpr inner-iterator<Const> begin() const;
```

*Effects:* Equivalent to:
`return `*`inner-iterator`*`<Const>{`*`i_`*`};`

``` cpp
constexpr default_sentinel_t end() const noexcept;
```

*Effects:* Equivalent to: `return default_sentinel;`

#### Class template `lazy_split_view::inner-iterator` <a id="range.lazy.split.inner">[[range.lazy.split.inner]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to> &&
             (forward_range<V> || tiny-range<Pattern>)
  template<bool Const>
  struct lazy_split_view<V, Pattern>::inner-iterator {
  private:
    using Base = maybe-const<Const, V>;                     // exposition only
    outer-iterator<Const> i_ = outer-iterator<Const>();     // exposition only
    bool incremented_ = false;                              // exposition only

  public:
    using iterator_concept  = typename outer-iterator<Const>::iterator_concept;

    using iterator_category = see belownc;                    // present only if Base
                                                            // models forward_range
    using value_type        = range_value_t<Base>;
    using difference_type   = range_difference_t<Base>;

    inner-iterator() = default;
    constexpr explicit inner-iterator(outer-iterator<Const> i);

    constexpr const iterator_t<Base>& base() const & noexcept;
    constexpr iterator_t<Base> base() && requires forward_range<V>;

    constexpr decltype(auto) operator*() const { return *i_.current; }

    constexpr inner-iterator& operator++();
    constexpr decltype(auto) operator++(int) {
      if constexpr (forward_range<Base>) {
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

If *Base* does not model `forward_range` there is no member
`iterator_category`. Otherwise, the *typedef-name* `iterator_category`
denotes:

- `forward_iterator_tag` if
  `iterator_traits<iterator_t<Base>>::iterator_category` models
  `derived_from<forward_iterator_tag>`;
- otherwise, `iterator_traits<iterator_t<Base>>::iterator_category`.

``` cpp
constexpr explicit inner-iterator(outer-iterator<Const> i);
```

*Effects:* Initializes *i\_* with `std::move(i)`.

``` cpp
constexpr const iterator_t<Base>& base() const & noexcept;
```

*Effects:* Equivalent to: `return `*`i_`*`.`*`current`*`;`

``` cpp
constexpr iterator_t<Base> base() && requires forward_range<V>;
```

*Effects:* Equivalent to: `return std::move(`*`i_`*`.`*`current`*`);`

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

### Split view <a id="range.split">[[range.split]]</a>

#### Overview <a id="range.split.overview">[[range.split.overview]]</a>

`split_view` takes a view and a delimiter, and splits the view into
`subrange`s on the delimiter. The delimiter can be a single element or a
view of elements.

The name `views::split` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::split(E, F)` is expression-equivalent to
`split_view(E, F)`.

\[*Example 1*:

``` cpp
string str{"the quick brown fox"};
for (auto word : views::split(str, ' ')) {
  cout << string_view(word) << '*';
}
// The above prints the*quick*brown*fox*
```

— *end example*\]

#### Class template `split_view` <a id="range.split.view">[[range.split.view]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to>
  class split_view : public view_interface<split_view<V, Pattern>> {
  private:
    V base_ = V();                              // exposition only
    Pattern pattern_ = Pattern();               // exposition only

    // [range.split.iterator], class split_view::iterator
    struct iterator;                            // exposition only

    // [range.split.sentinel], class split_view::sentinel
    struct sentinel;                            // exposition only

  public:
    split_view()
      requires default_initializable<V> && default_initializable<Pattern> = default;
    constexpr explicit split_view(V base, Pattern pattern);

    template<forward_range R>
      requires constructible_from<V, views::all_t<R>> &&
               constructible_from<Pattern, single_view<range_value_t<R>>>
    constexpr explicit split_view(R&& r, range_value_t<R> e);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr iterator begin();

    constexpr auto end() {
      if constexpr (common_range<V>) {
        return iterator{*this, ranges::end(base_), {}};
      } else {
        return sentinel{*this};
      }
    }

    constexpr subrange<iterator_t<V>> find-next(iterator_t<V>); // exposition only
  };

  template<class R, class P>
    split_view(R&&, P&&) -> split_view<views::all_t<R>, views::all_t<P>>;

  template<forward_range R>
    split_view(R&&, range_value_t<R>)
      -> split_view<views::all_t<R>, single_view<range_value_t<R>>>;
}
```

``` cpp
constexpr explicit split_view(V base, Pattern pattern);
```

*Effects:* Initializes *base\_* with `std::move(base)`, and *pattern\_*
with `std::move(pattern)`.

``` cpp
template<forward_range R>
  requires constructible_from<V, views::all_t<R>> &&
           constructible_from<Pattern, single_view<range_value_t<R>>>
constexpr explicit split_view(R&& r, range_value_t<R> e);
```

*Effects:* Initializes *base\_* with `views::all(std::forward<R>(r))`,
and *pattern\_* with `views::``single(std::move(e))`.

``` cpp
constexpr iterator begin();
```

*Returns:*
`{*this, ranges::begin(`*`base_`*`), `*`find-next`*`(ranges::begin(`*`base_`*`))}`.

*Remarks:* In order to provide the amortized constant time complexity
required by the `range` concept, this function caches the result within
the `split_view` for use on subsequent calls.

``` cpp
constexpr subrange<iterator_t<V>> find-next(iterator_t<V> it);
```

*Effects:* Equivalent to:

``` cpp
auto [b, e] = ranges::search(subrange(it, ranges::end(base_)), pattern_);
if (b != ranges::end(base_) && ranges::empty(pattern_)) {
  ++b;
  ++e;
}
return {b, e};
```

#### Class `split_view::iterator` <a id="range.split.iterator">[[range.split.iterator]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to>
  class split_view<V, Pattern>::iterator {
  private:
    split_view* parent_ = nullptr;                              // exposition only
    iterator_t<V> cur_ = iterator_t<V>();                       // exposition only
    subrange<iterator_t<V>> next_ = subrange<iterator_t<V>>();  // exposition only
    bool trailing_empty_ = false;                               // exposition only

  public:
    using iterator_concept = forward_iterator_tag;
    using iterator_category = input_iterator_tag;
    using value_type = subrange<iterator_t<V>>;
    using difference_type = range_difference_t<V>;

    iterator() = default;
    constexpr iterator(split_view& parent, iterator_t<V> current, subrange<iterator_t<V>> next);

    constexpr iterator_t<V> base() const;
    constexpr value_type operator*() const;

    constexpr iterator& operator++();
    constexpr iterator operator++(int);

    friend constexpr bool operator==(const iterator& x, const iterator& y);
  };
}
```

``` cpp
constexpr iterator(split_view& parent, iterator_t<V> current, subrange<iterator_t<V>> next);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`, *cur\_* with
`std::move(current)`, and *next\_* with `std::move(next)`.

``` cpp
constexpr iterator_t<V> base() const;
```

*Effects:* Equivalent to `return `*`cur_`*`;`

``` cpp
constexpr value_type operator*() const;
```

*Effects:* Equivalent to `return {`*`cur_`*`, `*`next_`*`.begin()};`

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
cur_ = next_.begin();
if (cur_ != ranges::end(parent_->base_)) {
  cur_ = next_.end();
  if (cur_ == ranges::end(parent_->base_)) {
    trailing_empty_ = true;
    next_ = {cur_, cur_};
  } else {
    next_ = parent_->find-next(cur_);
  }
} else {
  trailing_empty_ = false;
}
return *this;
```

``` cpp
constexpr iterator operator++(int);
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y);
```

*Effects:* Equivalent to:

``` cpp
return x.cur_ == y.cur_ && x.trailing_empty_ == y.trailing_empty_;
```

#### Class `split_view::sentinel` <a id="range.split.sentinel">[[range.split.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, forward_range Pattern>
    requires view<V> && view<Pattern> &&
             indirectly_comparable<iterator_t<V>, iterator_t<Pattern>, ranges::equal_to>
  struct split_view<V, Pattern>::sentinel {
  private:
    sentinel_t<V> end_ = sentinel_t<V>();               // exposition only

  public:
    sentinel() = default;
    constexpr explicit sentinel(split_view& parent);

    friend constexpr bool operator==(const iterator& x, const sentinel& y);
  };
}
```

``` cpp
constexpr explicit sentinel(split_view& parent);
```

*Effects:* Initializes *end\_* with `ranges::end(parent.`*`base_`*`)`.

``` cpp
friend constexpr bool operator==(const iterator& x, const sentinel& y);
```

*Effects:* Equivalent to:
`return x.`*`cur_`*` == y.`*`end_`*` && !x.`*`trailing_empty_`*`;`

### Counted view <a id="range.counted">[[range.counted]]</a>

A counted view presents a view of the elements of the counted range
[[iterator.requirements.general]] `i`+\[0, `n`) for an iterator `i` and
non-negative integer `n`.

The name `views::counted` denotes a customization point object
[[customization.point.object]]. Let `E` and `F` be expressions, let `T`
be `decay_t<decltype((E))>`, and let `D` be `iter_difference_t<T>`. If
`decltype((F))` does not model `convertible_to<D>`,
`views::counted(E, F)` is ill-formed.

\[*Note 1*: This case can result in substitution failure when
`views::counted(E, F)` appears in the immediate context of a template
instantiation. — *end note*\]

Otherwise, `views::counted(E, F)` is expression-equivalent to:

- If `T` models `contiguous_iterator`, then
  `span(to_address(E), static_cast<size_t>(static_-\linebreak{}cast<D>(F)))`.
- Otherwise, if `T` models `random_access_iterator`, then
  `subrange(E, E + static_cast<D>(F))`, except that `E` is evaluated
  only once.
- Otherwise, `subrange(counted_iterator(E, F), default_sentinel)`.

### Common view <a id="range.common">[[range.common]]</a>

#### Overview <a id="range.common.overview">[[range.common.overview]]</a>

`common_view` takes a view which has different types for its iterator
and sentinel and turns it into a view of the same elements with an
iterator and sentinel of the same type.

\[*Note 1*: `common_view` is useful for calling legacy algorithms that
expect a range’s iterator and sentinel types to be the
same. — *end note*\]

The name `views::common` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::common(E)` is expression-equivalent to:

- `views::all(E)`, if `decltype((E))` models `common_range` and
  `views::all(E)` is a well-formed expression.
- Otherwise, `common_view{E}`.

\[*Example 1*:

``` cpp
// Legacy algorithm:
template<class ForwardIterator>
size_t count(ForwardIterator first, ForwardIterator last);

template<forward_range R>
void my_algo(R&& r) {
  auto&& common = views::common(r);
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
    common_view() requires default_initializable<V> = default;

    constexpr explicit common_view(V r);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
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
        return ranges::begin(base_) + ranges::distance(base_);
      else
        return common_iterator<iterator_t<V>, sentinel_t<V>>(ranges::end(base_));
    }

    constexpr auto end() const requires range<const V> {
      if constexpr (random_access_range<const V> && sized_range<const V>)
        return ranges::begin(base_) + ranges::distance(base_);
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

### Reverse view <a id="range.reverse">[[range.reverse]]</a>

#### Overview <a id="range.reverse.overview">[[range.reverse.overview]]</a>

`reverse_view` takes a bidirectional view and produces another view that
iterates the same elements in reverse order.

The name `views::reverse` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E`, the expression
`views::reverse(E)` is expression-equivalent to:

- If the type of `E` is a (possibly cv-qualified) specialization of
  `reverse_view`, equivalent to `E.base()`.
- Otherwise, if the type of `E` is cv
  `subrange<reverse_iterator<I>, reverse_iterator<I>, K>` for some
  iterator type `I` and value `K` of type `subrange_kind`,
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

\[*Example 1*:

``` cpp
vector<int> is {0,1,2,3,4};
for (int i : is | views::reverse)
  cout << i << ' '; // prints 4 3 2 1 0
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
    reverse_view() requires default_initializable<V> = default;

    constexpr explicit reverse_view(V r);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
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
`return make_reverse_iterator(ranges::end(`*`base_`*`));`

``` cpp
constexpr reverse_iterator<iterator_t<V>> end();
constexpr auto end() const requires common_range<const V>;
```

*Effects:* Equivalent to:
`return make_reverse_iterator(ranges::begin(`*`base_`*`));`

### As const view <a id="range.as.const">[[range.as.const]]</a>

#### Overview <a id="range.as.const.overview">[[range.as.const.overview]]</a>

`as_const_view` presents a view of an underlying sequence as constant.
That is, the elements of an `as_const_view` cannot be modified.

The name `views::as_const` denotes a range adaptor object
[[range.adaptor.object]]. Let `E` be an expression, let `T` be
`decltype((E))`, and let `U` be `remove_cvref_t<T>`. The expression
`views::as_const(E)` is expression-equivalent to:

- If `views::all_t<T>` models `constant_range`, then `views::all(E)`.
- Otherwise, if `U` denotes `empty_view<X>` for some type `X`, then
  `auto(views::empty<const X>)`.
- Otherwise, if `U` denotes `span<X, Extent>` for some type `X` and some
  extent `Extent`, then `span<const X, Extent>(E)`.
- Otherwise, if `U` denotes `ref_view<X>` for some type `X` and
  `const X` models `constant_range`, then
  `ref_view(static_cast<const X&>(E.base()))`.
- Otherwise, if `E` is an lvalue, `const U` models `constant_range`, and
  `U` does not model `view`, then `ref_view(static_cast<const U&>(E))`.
- Otherwise, `as_const_view(E)`.

\[*Example 1*:

``` cpp
template<constant_range R>
void cant_touch_this(R&&);

vector<char> hammer = {'m', 'c'};
span<char> beat = hammer;
cant_touch_this(views::as_const(beat));         // will not modify the elements of hammer
```

— *end example*\]

#### Class template `as_const_view` <a id="range.as.const.view">[[range.as.const.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires input_range<V>
  class as_const_view : public view_interface<as_const_view<V>> {
    V base_ = V();      // exposition only

  public:
    as_const_view() requires default_initializable<V> = default;
    constexpr explicit as_const_view(V base);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>) { return ranges::cbegin(base_); }
    constexpr auto begin() const requires range<const V> { return ranges::cbegin(base_); }

    constexpr auto end() requires (!simple-view<V>) { return ranges::cend(base_); }
    constexpr auto end() const requires range<const V> { return ranges::cend(base_); }

    constexpr auto size() requires sized_range<V> { return ranges::size(base_); }
    constexpr auto size() const requires sized_range<const V> { return ranges::size(base_); }
  };

  template<class R>
    as_const_view(R&&) -> as_const_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit as_const_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

### Elements view <a id="range.elements">[[range.elements]]</a>

#### Overview <a id="range.elements.overview">[[range.elements.overview]]</a>

`elements_view` takes a view of tuple-like values and a `size_t`, and
produces a view with a value-type of the Nᵗʰ element of the adapted
view’s value-type.

The name `views::elements<N>` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E` and constant
expression `N`, the expression `views::elements<N>(E)` is
expression-equivalent to
`elements_view<views::all_t<decltype((E))>, N>{E}`.

\[*Example 1*:

``` cpp
auto historical_figures = map{
  pair{"Lovelace"sv, 1815},
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

`keys_view` is an alias for `elements_view<R, 0>`, and is useful for
extracting keys from associative containers.

\[*Example 2*:

``` cpp
auto names = historical_figures | views::keys;
for (auto&& name : names) {
  cout << name << ' ';          // prints Babbage Hamilton Lovelace Turing
}
```

— *end example*\]

`values_view` is an alias for `elements_view<R, 1>`, and is useful for
extracting values from associative containers.

\[*Example 3*:

``` cpp
auto is_even = [](const auto x) { return x % 2 == 0; };
cout << ranges::count_if(historical_figures | views::values, is_even);  // prints 2
```

— *end example*\]

#### Class template `elements_view` <a id="range.elements.view">[[range.elements.view]]</a>

``` cpp
namespace std::ranges {
  template<class T, size_t N>
  concept has-tuple-element =                   // exposition only
    tuple-like<T> && N < tuple_size_v<T>;

  template<class T, size_t N>
  concept returnable-element =                  // exposition only
    is_reference_v<T> || move_constructible<tuple_element_t<N, T>>;

  template<input_range V, size_t N>
    requires view<V> && has-tuple-element<range_value_t<V>, N> &&
             has-tuple-element<remove_reference_t<range_reference_t<V>>, N> &&
             returnable-element<range_reference_t<V>, N>
  class elements_view : public view_interface<elements_view<V, N>> {
  public:
    elements_view() requires default_initializable<V> = default;
    constexpr explicit elements_view(V base);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>)
    { return iterator<false>(ranges::begin(base_)); }

    constexpr auto begin() const requires range<const V>
    { return iterator<true>(ranges::begin(base_)); }

    constexpr auto end() requires (!simple-view<V> && !common_range<V>)
    { return sentinel<false>{ranges::end(base_)}; }

    constexpr auto end() requires (!simple-view<V> && common_range<V>)
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
    template<bool> class iterator;                      // exposition only

    // [range.elements.sentinel], class template elements_view::sentinel
    template<bool> class sentinel;                      // exposition only

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
             has-tuple-element<remove_reference_t<range_reference_t<V>>, N> &&
             returnable-element<range_reference_t<V>, N>
  template<bool Const>
  class elements_view<V, N>::iterator {
    using Base = maybe-const<Const, V>;                 // exposition only

    iterator_t<Base> current_ = iterator_t<Base>();     // exposition only

    static constexpr decltype(auto) get-element(const iterator_t<Base>& i);     // exposition only

  public:
    using iterator_concept = see below;
    using iterator_category = see below;                // not always present
    using value_type = remove_cvref_t<tuple_element_t<N, range_value_t<Base>>>;
    using difference_type = range_difference_t<Base>;

    iterator() requires default_initializable<iterator_t<Base>> = default;
    constexpr explicit iterator(iterator_t<Base> current);
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr const iterator_t<Base>& base() const & noexcept;
    constexpr iterator_t<Base> base() &&;

    constexpr decltype(auto) operator*() const
    { return get-element(current_); }

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<Base>;

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x)
      requires random_access_range<Base>;

    constexpr decltype(auto) operator[](difference_type n) const
      requires random_access_range<Base>
    { return get-element(current_ + n); }

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

    friend constexpr iterator operator+(const iterator& x, difference_type y)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& x, difference_type y)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
  };
}
```

The member *typedef-name* `iterator_concept` is defined as follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if *Base* models `forward_range`, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

The member *typedef-name* `iterator_category` is defined if and only if
*Base* models `forward_range`. In that case, `iterator_category` is
defined as follows: Let `C` denote the type
`iterator_traits<iterator_t<Base>>::iterator_category`.

- If `std::get<N>(*current_)` is an rvalue, `iterator_category` denotes
  `input_iterator_tag`.
- Otherwise, if `C` models `derived_from<random_access_iterator_tag>`,
  `iterator_category` denotes `random_access_iterator_tag`.
- Otherwise, `iterator_category` denotes `C`.

``` cpp
static constexpr decltype(auto) get-element(const iterator_t<Base>& i);
```

*Effects:* Equivalent to:

``` cpp
if constexpr (is_reference_v<range_reference_t<Base>>) {
  return std::get<N>(*i);
} else {
  using E = remove_cv_t<tuple_element_t<N, range_reference_t<Base>>>;
  return static_cast<E>(std::get<N>(*i));
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
constexpr const iterator_t<Base>& base() const & noexcept;
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
constexpr void operator++(int);
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

*Effects:* Equivalent to: `return `*`iterator`*`{x} += y;`

``` cpp
friend constexpr iterator operator+(difference_type x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return y + x;`

``` cpp
friend constexpr iterator operator-(const iterator& x, difference_type y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return `*`iterator`*`{x} -= y;`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`current_`*`;`

#### Class template `elements_view::sentinel` <a id="range.elements.sentinel">[[range.elements.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range V, size_t N>
    requires view<V> && has-tuple-element<range_value_t<V>, N> &&
             has-tuple-element<remove_reference_t<range_reference_t<V>>, N> &&
             returnable-element<range_reference_t<V>, N>
  template<bool Const>
  class elements_view<V, N>::sentinel {
  private:
    using Base = maybe-const<Const, V>;                 // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();         // exposition only

  public:
    sentinel() = default;
    constexpr explicit sentinel(sentinel_t<Base> end);
    constexpr sentinel(sentinel<!Const> other)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    template<bool OtherConst>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const sentinel& x, const iterator<OtherConst>& y);
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
template<bool OtherConst>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const sentinel& x, const iterator<OtherConst>& y);
```

*Effects:* Equivalent to: `return x.`*`end_`*` - y.`*`current_`*`;`

### Enumerate view <a id="range.enumerate">[[range.enumerate]]</a>

#### Overview <a id="range.enumerate.overview">[[range.enumerate.overview]]</a>

`enumerate_view` is a view whose elements represent both the position
and value from a sequence of elements.

The name `views::enumerate` denotes a range adaptor object. Given a
subexpression `E`, the expression `views::enumerate(E)` is
expression-equivalent to
`enumerate_view<views::all_t<decltype((E))>>(E)`.

\[*Example 1*:

``` cpp
vector<int> vec{ 1, 2, 3 };
for (auto [index, value] : views::enumerate(vec))
  cout << index << ":" << value << ' ';         // prints 0:1 1:2 2:3
```

— *end example*\]

#### Class template `enumerate_view` <a id="range.enumerate.view">[[range.enumerate.view]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires range-with-movable-references<V>
  class enumerate_view : public view_interface<enumerate_view<V>> {
    V base_ = V();                                    // exposition only

    // [range.enumerate.iterator], class template enumerate_view::iterator
    template<bool Const>
      class iterator;                                 // exposition only

    // [range.enumerate.sentinel], class template enumerate_view::sentinel
    template<bool Const>
      class sentinel;                                 // exposition only

  public:
    constexpr enumerate_view() requires default_initializable<V> = default;
    constexpr explicit enumerate_view(V base);

    constexpr auto begin() requires (!simple-view<V>)
    { return iterator<false>(ranges::begin(base_), 0); }
    constexpr auto begin() const requires range-with-movable-references<const V>
    { return iterator<true>(ranges::begin(base_), 0); }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (common_range<V> && sized_range<V>)
        return iterator<false>(ranges::end(base_), ranges::distance(base_));
      else
        return sentinel<false>(ranges::end(base_));
    }
    constexpr auto end() const requires range-with-movable-references<const V> {
      if constexpr (common_range<const V> && sized_range<const V>)
        return iterator<true>(ranges::end(base_), ranges::distance(base_));
      else
        return sentinel<true>(ranges::end(base_));
    }

    constexpr auto size() requires sized_range<V>
    { return ranges::size(base_); }
    constexpr auto size() const requires sized_range<const V>
    { return ranges::size(base_); }

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }
  };

  template<class R>
    enumerate_view(R&&) -> enumerate_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit enumerate_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

#### Class template `enumerate_view::iterator` <a id="range.enumerate.iterator">[[range.enumerate.iterator]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires range-with-movable-references<V>
  template<bool Const>
  class enumerate_view<V>::iterator {
    using Base = maybe-const<Const, V>;                         // exposition only

  public:
    using iterator_category = input_iterator_tag;
    using iterator_concept = see below;
    using difference_type = range_difference_t<Base>;
    using value_type = tuple<difference_type, range_value_t<Base>>;

  private:
    using reference-type =                                      // exposition only
      tuple<difference_type, range_reference_t<Base>>;
    iterator_t<Base> current_ = iterator_t<Base>();             // exposition only
    difference_type pos_ = 0;                                   // exposition only

    constexpr explicit
      iterator(iterator_t<Base> current, difference_type pos);  // exposition only

  public:
    iterator() requires default_initializable<iterator_t<Base>> = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr const iterator_t<Base>& base() const & noexcept;
    constexpr iterator_t<Base> base() &&;

    constexpr difference_type index() const noexcept;

    constexpr auto operator*() const {
      return reference-type(pos_, *current_);
    }

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<Base>;

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x)
      requires random_access_range<Base>;

    constexpr auto operator[](difference_type n) const
      requires random_access_range<Base>
    { return reference-type(pos_ + n, current_[n]); }

    friend constexpr bool operator==(const iterator& x, const iterator& y) noexcept;
    friend constexpr strong_ordering operator<=>(const iterator& x, const iterator& y) noexcept;

    friend constexpr iterator operator+(const iterator& x, difference_type y)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& x, difference_type y)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y);

    friend constexpr auto iter_move(const iterator& i)
      noexcept(noexcept(ranges::iter_move(i.current_)) &&
               is_nothrow_move_constructible_v<range_rvalue_reference_t<Base>>) {
      return tuple<difference_type,
                   range_rvalue_reference_t<Base>>(i.pos_, ranges::iter_move(i.current_));
    }
  };
}
```

The member *typedef-name* `iterator::iterator_concept` is defined as
follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if *Base* models `forward_range`, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

``` cpp
constexpr explicit iterator(iterator_t<Base> current, difference_type pos);
```

*Effects:* Initializes *current\_* with `std::move(current)` and *pos\_*
with `pos`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`
and *pos\_* with `i.`*`pos_`*.

``` cpp
constexpr const iterator_t<Base>& base() const & noexcept;
```

*Effects:* Equivalent to: `return `*`current_`*`;`

``` cpp
constexpr iterator_t<Base> base() &&;
```

*Effects:* Equivalent to: `return std::move(`*`current_`*`);`

``` cpp
constexpr difference_type index() const noexcept;
```

*Effects:* Equivalent to: `return `*`pos_`*`;`

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++current_;
++pos_;
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
constexpr iterator operator++(int) requires forward_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto temp = *this;
++*this;
return temp;
```

``` cpp
constexpr iterator& operator--() requires bidirectional_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
--current_;
--pos_;
return *this;
```

``` cpp
constexpr iterator operator--(int) requires bidirectional_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto temp = *this;
--*this;
return temp;
```

``` cpp
constexpr iterator& operator+=(difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
current_ += n;
pos_ += n;
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
current_ -= n;
pos_ -= n;
return *this;
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y) noexcept;
```

*Effects:* Equivalent to: `return x.`*`pos_`*` == y.`*`pos_`*`;`

``` cpp
friend constexpr strong_ordering operator<=>(const iterator& x, const iterator& y) noexcept;
```

*Effects:* Equivalent to: `return x.`*`pos_`*` <=> y.`*`pos_`*`;`

``` cpp
friend constexpr iterator operator+(const iterator& x, difference_type y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto temp = x;
temp += y;
return temp;
```

``` cpp
friend constexpr iterator operator+(difference_type x, const iterator& y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return y + x;`

``` cpp
friend constexpr iterator operator-(const iterator& x, difference_type y)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto temp = x;
temp -= y;
return temp;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y);
```

*Effects:* Equivalent to: `return x.`*`pos_`*` - y.`*`pos_`*`;`

#### Class template `enumerate_view::sentinel` <a id="range.enumerate.sentinel">[[range.enumerate.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires range-with-movable-references<V>
  template<bool Const>
  class enumerate_view<V>::sentinel {
    using Base = maybe-const<Const, V>;                         // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();                 // exposition only
    constexpr explicit sentinel(sentinel_t<Base> end);          // exposition only

  public:
    sentinel() = default;
    constexpr sentinel(sentinel<!Const> other)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr sentinel_t<Base> base() const;

    template<bool OtherConst>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const sentinel& x, const iterator<OtherConst>& y);
  };
}
```

``` cpp
constexpr explicit sentinel(sentinel_t<Base> end);
```

*Effects:* Initializes *end\_* with `std::move(end)`.

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
template<bool OtherConst>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`current_`*` - y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const sentinel& x, const iterator<OtherConst>& y);
```

*Effects:* Equivalent to: `return x.`*`end_`*` - y.`*`current_`*`;`

### Zip view <a id="range.zip">[[range.zip]]</a>

#### Overview <a id="range.zip.overview">[[range.zip.overview]]</a>

`zip_view` takes any number of views and produces a view of tuples of
references to the corresponding elements of the constituent views.

The name `views::zip` denotes a customization point object
[[customization.point.object]]. Given a pack of subexpressions `Es...`,
the expression `views::zip(Es...)` is expression-equivalent to

- `auto(views::empty<tuple<>>)` if `Es` is an empty pack,
- otherwise, `zip_view<views::all_t<decltype((Es))>...>(Es...)`.

\[*Example 1*:

``` cpp
vector v = {1, 2};
list l = {'a', 'b', 'c'};

auto z = views::zip(v, l);
range_reference_t<decltype(z)> f = z.front();   // f is a tuple<int&, char&>
                                                // that refers to the first element of v and l

for (auto&& [x, y] : z) {
  cout << '(' << x << ", " << y << ") ";        // prints (1, a) (2, b)
}
```

— *end example*\]

#### Class template `zip_view` <a id="range.zip.view">[[range.zip.view]]</a>

``` cpp
namespace std::ranges {
  template<class... Rs>
  concept zip-is-common =                             // exposition only
    (sizeof...(Rs) == 1 && (common_range<Rs> && ...)) ||
    (!(bidirectional_range<Rs> && ...) && (common_range<Rs> && ...)) ||
    ((random_access_range<Rs> && ...) && (sized_range<Rs> && ...));

  template<input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0)
  class zip_view : public view_interface<zip_view<Views...>> {
    tuple<Views...> views_;             // exposition only

    // [range.zip.iterator], class template zip_view::iterator
    template<bool> class iterator;      // exposition only

    // [range.zip.sentinel], class template zip_view::sentinel
    template<bool> class sentinel;      // exposition only

  public:
    zip_view() = default;
    constexpr explicit zip_view(Views... views);

    constexpr auto begin() requires (!(simple-view<Views> && ...)) {
      return iterator<false>(tuple-transform(ranges::begin, views_));
    }
    constexpr auto begin() const requires (range<const Views> && ...) {
      return iterator<true>(tuple-transform(ranges::begin, views_));
    }

    constexpr auto end() requires (!(simple-view<Views> && ...)) {
      if constexpr (!zip-is-common<Views...>) {
        return sentinel<false>(tuple-transform(ranges::end, views_));
      } else if constexpr ((random_access_range<Views> && ...)) {
        return begin() + iter_difference_t<iterator<false>>(size());
      } else {
        return iterator<false>(tuple-transform(ranges::end, views_));
      }
    }

    constexpr auto end() const requires (range<const Views> && ...) {
      if constexpr (!zip-is-common<const Views...>) {
        return sentinel<true>(tuple-transform(ranges::end, views_));
      } else if constexpr ((random_access_range<const Views> && ...)) {
        return begin() + iter_difference_t<iterator<true>>(size());
      } else {
        return iterator<true>(tuple-transform(ranges::end, views_));
      }
    }

    constexpr auto size() requires (sized_range<Views> && ...);
    constexpr auto size() const requires (sized_range<const Views> && ...);
  };

  template<class... Rs>
    zip_view(Rs&&...) -> zip_view<views::all_t<Rs>...>;
}
```

Two `zip_view` objects have the same underlying sequence if and only if
the corresponding elements of *views\_* are equal [[concepts.equality]]
and have the same underlying sequence.

\[*Note 1*: In particular, comparison of iterators obtained from
`zip_view` objects that do not have the same underlying sequence is not
required to produce meaningful results
[[iterator.concept.forward]]. — *end note*\]

``` cpp
constexpr explicit zip_view(Views... views);
```

*Effects:* Initializes *views\_* with `std::move(views)...`.

``` cpp
constexpr auto size() requires (sized_range<Views> && ...);
constexpr auto size() const requires (sized_range<const Views> && ...);
```

*Effects:* Equivalent to:

``` cpp
return apply([](auto... sizes) {
  using CT = make-unsigned-like-t<common_type_t<decltype(sizes)...>>;
  return ranges::min({CT(sizes)...});
}, tuple-transform(ranges::size, views_));
```

#### Class template `zip_view::iterator` <a id="range.zip.iterator">[[range.zip.iterator]]</a>

``` cpp
namespace std::ranges {
  template<bool Const, class... Views>
    concept \defexposconceptnc{all-random-access} =                 // exposition only
      (random_access_range<maybe-const<Const, Views>> && ...);
  template<bool Const, class... Views>
    concept \defexposconceptnc{all-bidirectional} =                 // exposition only
      (bidirectional_range<maybe-const<Const, Views>> && ...);
  template<bool Const, class... Views>
    concept \defexposconceptnc{all-forward} =                       // exposition only
      (forward_range<maybe-const<Const, Views>> && ...);

  template<input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0)
  template<bool Const>
  class zip_view<Views...>::iterator {
    tuple<iterator_t<maybe-const<Const, Views>>...> current_;\itcorr[-1]       // exposition only
    constexpr explicit iterator(tuple<iterator_t<maybe-const<Const, Views>>...>);
                                                                            // exposition only
  public:
    using iterator_category = input_iterator_tag;                           // not always present
    using iterator_concept  = see below;
    using value_type = tuple<range_value_t<maybe-const<Const, Views>>...>;
    using difference_type = common_type_t<range_difference_t<maybe-const<Const, Views>>...>;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && (convertible_to<iterator_t<Views>, iterator_t<const Views>> && ...);

    constexpr auto operator*() const;
    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires all-forward<Const, Views...>;

    constexpr iterator& operator--() requires all-bidirectional<Const, Views...>;
    constexpr iterator operator--(int) requires all-bidirectional<Const, Views...>;

    constexpr iterator& operator+=(difference_type x)
      requires all-random-access<Const, Views...>;
    constexpr iterator& operator-=(difference_type x)
      requires all-random-access<Const, Views...>;

    constexpr auto operator[](difference_type n) const
      requires all-random-access<Const, Views...>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires (equality_comparable<iterator_t<maybe-const<Const, Views>>> && ...);

    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires all-random-access<Const, Views...>;

    friend constexpr iterator operator+(const iterator& i, difference_type n)
      requires all-random-access<Const, Views...>;
    friend constexpr iterator operator+(difference_type n, const iterator& i)
      requires all-random-access<Const, Views...>;
    friend constexpr iterator operator-(const iterator& i, difference_type n)
      requires all-random-access<Const, Views...>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires (sized_sentinel_for<iterator_t<maybe-const<Const, Views>>,
                                   iterator_t<maybe-const<Const, Views>>> && ...);

    friend constexpr auto iter_move(const iterator& i) noexcept(see below);

    friend constexpr void iter_swap(const iterator& l, const iterator& r) noexcept(see below)
      requires (indirectly_swappable<iterator_t<maybe-const<Const, Views>>> && ...);
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If `all-random-access<Const, Views...>` is modeled, then
  `iterator_concept` denotes `random_access_iterator_tag`.
- Otherwise, if `all-bidirectional<Const, Views...>` is modeled, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if `all-forward<Const, Views...>` is modeled, then
  `iterator_concept` denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

`iterator::iterator_category` is present if and only if
`all-forward<Const, Views...>` is modeled.

If the invocation of any non-const member function of *iterator* exits
via an exception, the iterator acquires a singular value.

``` cpp
constexpr explicit iterator(tuple<iterator_t<maybe-const<Const, Views>>...> current);
```

*Effects:* Initializes *current\_* with `std::move(current)`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && (convertible_to<iterator_t<Views>, iterator_t<const Views>> && ...);
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`.

``` cpp
constexpr auto operator*() const;
```

*Effects:* Equivalent to:

``` cpp
return tuple-transform([](auto& i) -> decltype(auto) { return *i; }, current_);
```

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
tuple-for-each([](auto& i) { ++i; }, current_);
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
constexpr iterator operator++(int) requires all-forward<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--() requires all-bidirectional<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
tuple-for-each([](auto& i) { --i; }, current_);
return *this;
```

``` cpp
constexpr iterator operator--(int) requires all-bidirectional<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
constexpr iterator& operator+=(difference_type x)
  requires all-random-access<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
tuple-for-each([&]<class I>(I& i) { i += iter_difference_t<I>(x); }, current_);
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires all-random-access<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
tuple-for-each([&]<class I>(I& i) { i -= iter_difference_t<I>(x); }, current_);
return *this;
```

``` cpp
constexpr auto operator[](difference_type n) const
  requires all-random-access<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
return tuple-transform([&]<class I>(I& i) -> decltype(auto) {
  return i[iter_difference_t<I>(n)];
}, current_);
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires (equality_comparable<iterator_t<maybe-const<Const, Views>>> && ...);
```

*Returns:*

- `x.`*`current_`*` == y.`*`current_`* if
  `all-bidirectional<Const, Views...>` is `true`.
- Otherwise, `true` if there exists an integer
  0 ≤ i < `sizeof...(Views)` such that
  `bool(std::get<`i`>(x.`*`current_`*`) == std::get<`i`>(y.`*`current_`*`))`
  is `true`. \[*Note 3*: This allows `zip_view` to model `common_range`
  when all constituent views model `common_range`. — *end note*\]
- Otherwise, `false`.

``` cpp
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires all-random-access<Const, Views...>;
```

*Returns:* `x.`*`current_`*` <=> y.`*`current_`*.

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires all-random-access<Const, Views...>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires all-random-access<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r += n;
return r;
```

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires all-random-access<Const, Views...>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r -= n;
return r;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires (sized_sentinel_for<iterator_t<maybe-const<Const, Views>>,
                               iterator_t<maybe-const<Const, Views>>> && ...);
```

Let *`DIST`*`(`i`)` be
`difference_type(std::get<`i`>(x.`*`current_`*`) - std::get<`i`>(y.`*`current_`*`))`.

*Returns:* The value with the smallest absolute value among
*`DIST`*`(`n`)` for all integers 0 ≤ n < `sizeof...(Views)`.

``` cpp
friend constexpr auto iter_move(const iterator& i) noexcept(see below);
```

*Effects:* Equivalent to:

``` cpp
return tuple-transform(ranges::iter_move, i.current_);
```

*Remarks:* The exception specification is equivalent to:

``` cpp
(noexcept(ranges::iter_move(declval<const iterator_t<maybe-const<Const,
                                                            Views>>&>())) && ...) &&
(is_nothrow_move_constructible_v<range_rvalue_reference_t<maybe-const<Const,
                                                                      Views>>> && ...)
```

``` cpp
friend constexpr void iter_swap(const iterator& l, const iterator& r) noexcept(see below)
  requires (indirectly_swappable<iterator_t<maybe-const<Const, Views>>> && ...);
```

*Effects:* For every integer 0 ≤ i < `sizeof...(Views)`, performs:

``` cpp
ranges::iter_swap(std::get<$i$>(l.current_), std::get<$i$>(r.current_))
```

*Remarks:* The exception specification is equivalent to the logical of
the following expressions:

``` cpp
noexcept(ranges::iter_swap(std::get<$i$>(l.current_), std::get<$i$>(r.current_)))
```

for every integer 0 ≤ i < `sizeof...(Views)`.

#### Class template `zip_view::sentinel` <a id="range.zip.sentinel">[[range.zip.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0)
  template<bool Const>
  class zip_view<Views...>::sentinel {
    tuple<sentinel_t<maybe-const<Const, Views>>...> end_;\itcorr[-1]               // exposition only
    constexpr explicit sentinel(tuple<sentinel_t<maybe-const<Const, Views>>...> end);
                                                                                // exposition only
  public:
    sentinel() = default;
    constexpr sentinel(sentinel<!Const> i)
      requires Const && (convertible_to<sentinel_t<Views>, sentinel_t<const Views>> && ...);

    template<bool OtherConst>
      requires (sentinel_for<sentinel_t<maybe-const<Const, Views>>,
                             iterator_t<maybe-const<OtherConst, Views>>> && ...)
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires (sized_sentinel_for<sentinel_t<maybe-const<Const, Views>>,
                                   iterator_t<maybe-const<OtherConst, Views>>> && ...)
    friend constexpr common_type_t<range_difference_t<maybe-const<OtherConst, Views>>...>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires (sized_sentinel_for<sentinel_t<maybe-const<Const, Views>>,
                                   iterator_t<maybe-const<OtherConst, Views>>> && ...)
    friend constexpr common_type_t<range_difference_t<maybe-const<OtherConst, Views>>...>
      operator-(const sentinel& y, const iterator<OtherConst>& x);
  };
}
```

``` cpp
constexpr explicit sentinel(tuple<sentinel_t<maybe-const<Const, Views>>...> end);
```

*Effects:* Initializes *end\_* with `end`.

``` cpp
constexpr sentinel(sentinel<!Const> i)
  requires Const && (convertible_to<sentinel_t<Views>, sentinel_t<const Views>> && ...);
```

*Effects:* Initializes *end\_* with `std::move(i.`*`end_`*`)`.

``` cpp
template<bool OtherConst>
  requires (sentinel_for<sentinel_t<maybe-const<Const, Views>>,
                         iterator_t<maybe-const<OtherConst, Views>>> && ...)
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Returns:* `true` if there exists an integer 0 ≤ i < `sizeof...(Views)`
such that
`bool(std::get<`i`>(x.`*`current_`*`) == std::get<`i`>(y.`*`end_`*`))`
is `true`. Otherwise, `false`.

``` cpp
template<bool OtherConst>
  requires (sized_sentinel_for<sentinel_t<maybe-const<Const, Views>>,
                               iterator_t<maybe-const<OtherConst, Views>>> && ...)
friend constexpr common_type_t<range_difference_t<maybe-const<OtherConst, Views>>...>
  operator-(const iterator<OtherConst>& x, const sentinel& y);
```

Let `D` be the return type. Let *`DIST`*`(`i`)` be
`D(std::get<`i`>(x.`*`current_`*`) - std::get<`i`>(y.`*`end_`*`))`.

*Returns:* The value with the smallest absolute value among
*`DIST`*`(`n`)` for all integers 0 ≤ n < `sizeof...(Views)`.

``` cpp
template<bool OtherConst>
  requires (sized_sentinel_for<sentinel_t<maybe-const<Const, Views>>,
                               iterator_t<maybe-const<OtherConst, Views>>> && ...)
friend constexpr common_type_t<range_difference_t<maybe-const<OtherConst, Views>>...>
  operator-(const sentinel& y, const iterator<OtherConst>& x);
```

*Effects:* Equivalent to `return -(x - y);`

### Zip transform view <a id="range.zip.transform">[[range.zip.transform]]</a>

#### Overview <a id="range.zip.transform.overview">[[range.zip.transform.overview]]</a>

`zip_transform_view` takes an invocable object and any number of views
and produces a view whose Mᵗʰ element is the result of applying the
invocable object to the Mᵗʰ elements of all views.

The name `views::zip_transform` denotes a customization point object
[[customization.point.object]]. Let `F` be a subexpression, and let
`Es...` be a pack of subexpressions.

- If `Es` is an empty pack, let `FD` be `decay_t<decltype((F))>`.
  - If `move_constructible<FD> &&
    regular_invocable<FD&>` is `false`, or if
    `decay_t<invoke_result_t<FD&>>` is not an object type,
    `views::zip_transform(F, Es...)` is ill-formed.
  - Otherwise, the expression `views::zip_transform(F, Es...)` is
    expression-equivalent to
    ``` cpp
    ((void)F, auto(views::empty<decay_t<invoke_result_t<FD&>>>))
    ```
- Otherwise, the expression `views::zip_transform(F, Es...)` is
  expression-equivalent to `zip_transform_view(F, Es...)`.

\[*Example 1*:

``` cpp
vector v1 = {1, 2};
vector v2 = {4, 5, 6};

for (auto i : views::zip_transform(plus(), v1, v2)) {
  cout << i << ' ';     // prints 5 7
}
```

— *end example*\]

#### Class template `zip_transform_view` <a id="range.zip.transform.view">[[range.zip.transform.view]]</a>

``` cpp
namespace std::ranges {
  template<move_constructible F, input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0) && is_object_v<F> &&
              regular_invocable<F&, range_reference_t<Views>...> &&
              can-reference<invoke_result_t<F&, range_reference_t<Views>...>>
  class zip_transform_view : public view_interface<zip_transform_view<F, Views...>> {
    movable-box<F> fun_;                    // exposition only
    zip_view<Views...> zip_;                // exposition only

    using InnerView = zip_view<Views...>;   // exposition only
    template<bool Const>
      using ziperator = iterator_t<maybe-const<Const, InnerView>>;      // exposition only
    template<bool Const>
      using zentinel = sentinel_t<maybe-const<Const, InnerView>>;       // exposition only

    // [range.zip.transform.iterator], class template zip_transform_view::iterator
    template<bool> class iterator;          // exposition only

    // [range.zip.transform.sentinel], class template zip_transform_view::sentinel
    template<bool> class sentinel;          // exposition only

  public:
    zip_transform_view() = default;

    constexpr explicit zip_transform_view(F fun, Views... views);

    constexpr auto begin() { return iterator<false>(*this, zip_.begin()); }

    constexpr auto begin() const
      requires range<const InnerView> &&
               regular_invocable<const F&, range_reference_t<const Views>...> {
      return iterator<true>(*this, zip_.begin());
    }

    constexpr auto end() {
      if constexpr (common_range<InnerView>) {
        return iterator<false>(*this, zip_.end());
      } else {
        return sentinel<false>(zip_.end());
      }
    }

    constexpr auto end() const
      requires range<const InnerView> &&
               regular_invocable<const F&, range_reference_t<const Views>...> {
      if constexpr (common_range<const InnerView>) {
        return iterator<true>(*this, zip_.end());
      } else {
        return sentinel<true>(zip_.end());
      }
    }

    constexpr auto size() requires sized_range<InnerView> {
      return zip_.size();
    }

    constexpr auto size() const requires sized_range<const InnerView> {
      return zip_.size();
    }
  };

  template<class F, class... Rs>
    zip_transform_view(F, Rs&&...) -> zip_transform_view<F, views::all_t<Rs>...>;
}
```

``` cpp
constexpr explicit zip_transform_view(F fun, Views... views);
```

*Effects:* Initializes *fun\_* with `std::move(fun)` and *zip\_* with
`std::move(views)...`.

#### Class template `zip_transform_view::iterator` <a id="range.zip.transform.iterator">[[range.zip.transform.iterator]]</a>

``` cpp
namespace std::ranges {
  template<move_constructible F, input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0) && is_object_v<F> &&
              regular_invocable<F&, range_reference_t<Views>...> &&
              can-reference<invoke_result_t<F&, range_reference_t<Views>...>>
  template<bool Const>
  class zip_transform_view<F, Views...>::iterator {
    using Parent = maybe-const<Const, zip_transform_view>;      // exposition only
    using Base = maybe-const<Const, InnerView>;                 // exposition only
    Parent* parent_ = nullptr;                                  // exposition only
    ziperator<Const> inner_;\itcorr[-1]                                    // exposition only

    constexpr iterator(Parent& parent, ziperator<Const> inner);   // exposition only

  public:
    using iterator_category = see belownc;                        // not always present
    using iterator_concept  = typename ziperator<Const>::iterator_concept;
    using value_type =
      remove_cvref_t<invoke_result_t<maybe-const<Const, F>&,
                                     range_reference_t<maybe-const<Const, Views>>...>>;
    using difference_type = range_difference_t<Base>;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<ziperator<false>, ziperator<Const>>;

    constexpr decltype(auto) operator*() const noexcept(see below);
    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<Base>;

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x) requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x) requires random_access_range<Base>;

    constexpr decltype(auto) operator[](difference_type n) const
      requires random_access_range<Base>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<ziperator<Const>>;

    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;

    friend constexpr iterator operator+(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, const iterator& i)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<ziperator<Const>, ziperator<Const>>;
  };
}
```

The member *typedef-name* `iterator::iterator_category` is defined if
and only if *Base* models `forward_range`. In that case,
`iterator::iterator_category` is defined as follows:

- If
  ``` cpp
  invoke_result_t<maybe-const<Const, F>&, range_reference_t<maybe-const<Const, Views>>...>
  ```

  is not a reference, `iterator_category` denotes `input_iterator_tag`.
- Otherwise, let `Cs` denote the pack of types
  `iterator_traits<iterator_t<maybe-const<Const, Views>>>::iterator_category...`.
  - If `(derived_from<Cs, random_access_iterator_tag> && ...)` is
    `true`, `iterator_category` denotes `random_access_iterator_tag`.
  - Otherwise, if
    `(derived_from<Cs, bidirectional_iterator_tag> && ...)` is `true`,
    `iterator_category` denotes `bidirectional_iterator_tag`.
  - Otherwise, if `(derived_from<Cs, forward_iterator_tag> && ...)` is
    `true`, `iterator_category` denotes `forward_iterator_tag`.
  - Otherwise, `iterator_category` denotes `input_iterator_tag`.

``` cpp
constexpr iterator(Parent& parent, ziperator<Const> inner);
```

*Effects:* Initializes *parent\_* with `addressof(parent)` and *inner\_*
with `std::move(inner)`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<ziperator<false>, ziperator<Const>>;
```

*Effects:* Initializes *parent\_* with `i.`*`parent_`* and *inner\_*
with `std::move(i.`*`inner_`*`)`.

``` cpp
constexpr decltype(auto) operator*() const noexcept(see below);
```

*Effects:* Equivalent to:

``` cpp
return apply([&](const auto&... iters) -> decltype(auto) {
  return invoke(*parent_->fun_, *iters...);
}, inner_.current_);
```

*Remarks:* Let `Is` be the pack `0, 1, …, ``(sizeof...(Views)-1)`. The
exception specification is equivalent to:
`noexcept(invoke(*`*`parent_`*`->`*`fun_`*`, *std::get<Is>(`*`inner_`*`.`*`current_`*`)...))`.

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++inner_;
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to: `++*this`.

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
--inner_;
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
constexpr iterator& operator+=(difference_type x)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
inner_ += x;
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
inner_ -= x;
return *this;
```

``` cpp
constexpr decltype(auto) operator[](difference_type n) const
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
return apply([&]<class... Is>(const Is&... iters) -> decltype(auto) {
  return invoke(*parent_->fun_, iters[iter_difference_t<Is>(n)]...);
}, inner_.current_);
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires equality_comparable<ziperator<Const>>;
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

Let *op* be the operator.

*Effects:* Equivalent to:
`return x.`*`inner_`*` `*`op`*` y.`*`inner_`*`;`

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return `*`iterator`*`(*i.`*`parent_`*`, i.`*`inner_`*` + n);`

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return `*`iterator`*`(*i.`*`parent_`*`, i.`*`inner_`*` - n);`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<ziperator<Const>, ziperator<Const>>;
```

*Effects:* Equivalent to: `return x.`*`inner_`*` - y.`*`inner_`*`;`

#### Class template `zip_transform_view::sentinel` <a id="range.zip.transform.sentinel">[[range.zip.transform.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<move_constructible F, input_range... Views>
    requires (view<Views> && ...) && (sizeof...(Views) > 0) && is_object_v<F> &&
              regular_invocable<F&, range_reference_t<Views>...> &&
              can-reference<invoke_result_t<F&, range_reference_t<Views>...>>
  template<bool Const>
  class zip_transform_view<F, Views...>::sentinel {
    zentinel<Const> inner_;                                     // exposition only
    constexpr explicit sentinel(zentinel<Const> inner);         // exposition only

  public:
    sentinel() = default;
    constexpr sentinel(sentinel<!Const> i)
      requires Const && convertible_to<zentinel<false>, zentinel<Const>>;

    template<bool OtherConst>
      requires sentinel_for<zentinel<Const>, ziperator<OtherConst>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<zentinel<Const>, ziperator<OtherConst>>
    friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<zentinel<Const>, ziperator<OtherConst>>
    friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
      operator-(const sentinel& x, const iterator<OtherConst>& y);
  };
}
```

``` cpp
constexpr explicit sentinel(zentinel<Const> inner);
```

*Effects:* Initializes *inner\_* with `inner`.

``` cpp
constexpr sentinel(sentinel<!Const> i)
  requires Const && convertible_to<zentinel<false>, zentinel<Const>>;
```

*Effects:* Initializes *inner\_* with `std::move(i.`*`inner_`*`)`.

``` cpp
template<bool OtherConst>
  requires sentinel_for<zentinel<Const>, ziperator<OtherConst>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to: `return x.`*`inner_`*` == y.`*`inner_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<zentinel<Const>, ziperator<OtherConst>>
friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
  operator-(const iterator<OtherConst>& x, const sentinel& y);
template<bool OtherConst>
  requires sized_sentinel_for<zentinel<Const>, ziperator<OtherConst>>
friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
  operator-(const sentinel& x, const iterator<OtherConst>& y);
```

*Effects:* Equivalent to: `return x.`*`inner_`*` - y.`*`inner_`*`;`

### Adjacent view <a id="range.adjacent">[[range.adjacent]]</a>

#### Overview <a id="range.adjacent.overview">[[range.adjacent.overview]]</a>

`adjacent_view` takes a view and produces a view whose Mᵗʰ element is a
tuple of references to the Mᵗʰ through (M + N - 1)ᵗʰ elements of the
original view. If the original view has fewer than N elements, the
resulting view is empty.

The name `views::adjacent<N>` denotes a range adaptor object
[[range.adaptor.object]]. Given a subexpression `E` and a constant
expression `N`, the expression `views::adjacent<N>(E)` is
expression-equivalent to

- `((void)E, auto(views::empty<tuple<>>))` if `N` is equal to `0`,
- otherwise, `adjacent_view<views::all_t<decltype((E))>, N>(E)`.

\[*Example 1*:

``` cpp
vector v = {1, 2, 3, 4};

for (auto i : v | views::adjacent<2>) {
  cout << "(" << std::get<0>(i) << ", " << std::get<1>(i) << ") ";  // prints (1, 2) (2, 3) (3, 4)
}
```

— *end example*\]

Define `REPEAT(T, N)` as a pack of `N` types, each of which denotes the
same type as `T`.

#### Class template `adjacent_view` <a id="range.adjacent.view">[[range.adjacent.view]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, size_t N>
    requires view<V> && (N > 0)
  class adjacent_view : public view_interface<adjacent_view<V, N>> {
    V base_ = V();                      // exposition only

    // [range.adjacent.iterator], class template adjacent_view::iterator
    template<bool> class iterator;      // exposition only

    // [range.adjacent.sentinel], class template adjacent_view::sentinel
    template<bool> class sentinel;      // exposition only

    struct as-sentinel{};               // exposition only

  public:
    adjacent_view() requires default_initializable<V> = default;
    constexpr explicit adjacent_view(V base);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>) {
      return iterator<false>(ranges::begin(base_), ranges::end(base_));
    }

    constexpr auto begin() const requires range<const V> {
      return iterator<true>(ranges::begin(base_), ranges::end(base_));
    }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (common_range<V>) {
        return iterator<false>(as-sentinel{}, ranges::begin(base_), ranges::end(base_));
      } else {
        return sentinel<false>(ranges::end(base_));
      }
    }

    constexpr auto end() const requires range<const V> {
      if constexpr (common_range<const V>) {
        return iterator<true>(as-sentinel{}, ranges::begin(base_), ranges::end(base_));
      } else {
        return sentinel<true>(ranges::end(base_));
      }
    }

    constexpr auto size() requires sized_range<V>;
    constexpr auto size() const requires sized_range<const V>;
  };
}
```

``` cpp
constexpr explicit adjacent_view(V base);
```

*Effects:* Initializes *base\_* with `std::move(base)`.

``` cpp
constexpr auto size() requires sized_range<V>;
constexpr auto size() const requires sized_range<const V>;
```

*Effects:* Equivalent to:

``` cpp
using ST = decltype(ranges::size(base_));
using CT = common_type_t<ST, size_t>;
auto sz = static_cast<CT>(ranges::size(base_));
sz -= std::min<CT>(sz, N - 1);
return static_cast<ST>(sz);
```

#### Class template `adjacent_view::iterator` <a id="range.adjacent.iterator">[[range.adjacent.iterator]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, size_t N>
    requires view<V> && (N > 0)
  template<bool Const>
  class adjacent_view<V, N>::iterator {
    using Base = maybe-const<Const, V>;                                         // exposition only
    array<iterator_t<Base>, N> current_ = array<iterator_t<Base>, N>();         // exposition only
    constexpr iterator(iterator_t<Base> first, sentinel_t<Base> last);          // exposition only
    constexpr iterator(as-sentinel, iterator_t<Base> first, iterator_t<Base> last);
                                                                                // exposition only
  public:
    using iterator_category = input_iterator_tag;
    using iterator_concept  = see below;
    using value_type = tuple<REPEAT(range_value_t<Base>, N)...>;
    using difference_type = range_difference_t<Base>;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr auto operator*() const;
    constexpr iterator& operator++();
    constexpr iterator operator++(int);

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x)
      requires random_access_range<Base>;

    constexpr auto operator[](difference_type n) const
      requires random_access_range<Base>;

    friend constexpr bool operator==(const iterator& x, const iterator& y);
    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator<=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base> &&
               three_way_comparable<iterator_t<Base>>;

    friend constexpr iterator operator+(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, const iterator& i)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;

    friend constexpr auto iter_move(const iterator& i) noexcept(see below);
    friend constexpr void iter_swap(const iterator& l, const iterator& r) noexcept(see below)
      requires indirectly_swappable<iterator_t<Base>>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, `iterator_concept` denotes `forward_iterator_tag`.

If the invocation of any non-const member function of *iterator* exits
via an exception, the *iterator* acquires a singular value.

``` cpp
constexpr iterator(iterator_t<Base> first, sentinel_t<Base> last);
```

*Ensures:* *`current_`*`[0] == first` is `true`, and for every integer
1 ≤ i < `N`,
*`current_`*`[`i`] == ranges::next(`*`current_`*`[`i`-1], 1, last)` is
`true`.

``` cpp
constexpr iterator(as-sentinel, iterator_t<Base> first, iterator_t<Base> last);
```

*Ensures:* If *Base* does not model `bidirectional_range`, each element
of *current\_* is equal to *last*. Otherwise,
*`current_`*`[N-1] == last` is `true`, and for every integer
0 ≤ i < (`N` - 1),
*`current_`*`[`i`] == ranges::prev(`*`current_`*`[`i`+1], 1, first)` is
`true`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;
```

*Effects:* Initializes each element of *current\_* with the
corresponding element of `i.`*`current_`* as an xvalue.

``` cpp
constexpr auto operator*() const;
```

*Effects:* Equivalent to:

``` cpp
return tuple-transform([](auto& i) -> decltype(auto) { return *i; }, current_);
```

``` cpp
constexpr iterator& operator++();
```

*Preconditions:* *`current_`*`.back()` is incrementable.

*Ensures:* Each element of *current\_* is equal to `ranges::next(i)`,
where `i` is the value of that element before the call.

*Returns:* `*this`.

``` cpp
constexpr iterator operator++(int);
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

*Preconditions:* *`current_`*`.front()` is decrementable.

*Ensures:* Each element of *current\_* is equal to `ranges::prev(i)`,
where `i` is the value of that element before the call.

*Returns:* `*this`.

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
constexpr iterator& operator+=(difference_type x)
  requires random_access_range<Base>;
```

*Preconditions:* *`current_`*`.back() + x` has well-defined behavior.

*Ensures:* Each element of *current\_* is equal to `i + x`, where `i` is
the value of that element before the call.

*Returns:* `*this`.

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires random_access_range<Base>;
```

*Preconditions:* *`current_`*`.front() - x` has well-defined behavior.

*Ensures:* Each element of *current\_* is equal to `i - x`, where `i` is
the value of that element before the call.

*Returns:* `*this`.

``` cpp
constexpr auto operator[](difference_type n) const
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
return tuple-transform([&](auto& i) -> decltype(auto) { return i[n]; }, current_);
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y);
```

*Returns:* `x.`*`current_`*`.back() == y.`*`current_`*`.back()`.

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Returns:* `x.`*`current_`*`.back() < y.`*`current_`*`.back()`.

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
  requires random_access_range<Base> &&
           three_way_comparable<iterator_t<Base>>;
```

*Returns:* `x.`*`current_`*`.back() <=> y.`*`current_`*`.back()`.

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r += n;
return r;
```

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r -= n;
return r;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to:
`return x.`*`current_`*`.back() - y.`*`current_`*`.back();`

``` cpp
friend constexpr auto iter_move(const iterator& i) noexcept(see below);
```

*Effects:* Equivalent to:
`return `*`tuple-transform`*`(ranges::iter_move, i.`*`current_`*`);`

*Remarks:* The exception specification is equivalent to:

``` cpp
noexcept(ranges::iter_move(declval<const iterator_t<Base>&>())) &&
is_nothrow_move_constructible_v<range_rvalue_reference_t<Base>>
```

``` cpp
friend constexpr void iter_swap(const iterator& l, const iterator& r) noexcept(see below)
  requires indirectly_swappable<iterator_t<Base>>;
```

*Preconditions:* None of the iterators in `l.`*`current_`* is equal to
an iterator in `r.`*`current_`*.

*Effects:* For every integer 0 ≤ i < `N`, performs
`ranges::iter_swap(l.`*`current_`*`[`i`], r.`*`current_`*`[`i`])`.

*Remarks:* The exception specification is equivalent to:

``` cpp
noexcept(ranges::iter_swap(declval<iterator_t<Base>>(), declval<iterator_t<Base>>()))
```

#### Class template `adjacent_view::sentinel` <a id="range.adjacent.sentinel">[[range.adjacent.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, size_t N>
    requires view<V> && (N > 0)
  template<bool Const>
  class adjacent_view<V, N>::sentinel {
    using Base = maybe-const<Const, V>;                         // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();                 // exposition only
    constexpr explicit sentinel(sentinel_t<Base> end);          // exposition only

  public:
    sentinel() = default;
    constexpr sentinel(sentinel<!Const> i)
      requires Const && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    template<bool OtherConst>
      requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
    friend constexpr range_difference_t<maybe-const<OtherConst, V>>
      operator-(const sentinel& y, const iterator<OtherConst>& x);
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
template<bool OtherConst>
  requires sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to:
`return x.`*`current_`*`.back() == y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to:
`return x.`*`current_`*`.back() - y.`*`end_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<maybe-const<OtherConst, V>>>
friend constexpr range_difference_t<maybe-const<OtherConst, V>>
  operator-(const sentinel& y, const iterator<OtherConst>& x);
```

*Effects:* Equivalent to:
`return y.`*`end_`*` - x.`*`current_`*`.back();`

### Adjacent transform view <a id="range.adjacent.transform">[[range.adjacent.transform]]</a>

#### Overview <a id="range.adjacent.transform.overview">[[range.adjacent.transform.overview]]</a>

`adjacent_transform_view` takes an invocable object and a view and
produces a view whose Mᵗʰ element is the result of applying the
invocable object to the Mᵗʰ through (M + N - 1)ᵗʰ elements of the
original view. If the original view has fewer than N elements, the
resulting view is empty.

The name `views::adjacent_transform<N>` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F` and a
constant expression `N`:

- If `N` is equal to `0`, `views::adjacent_transform<N>(E, F)` is
  expression-equivalent to `((void)E, views::zip_transform(F))`, except
  that the evaluations of `E` and `F` are indeterminately sequenced.
- Otherwise, the expression `views::adjacent_transform<N>(E, F)` is
  expression-equivalent to
  `adjacent_transform_view<views::all_t<decltype((E))>, decay_t<decltype((F))>, N>(E, F)`.

\[*Example 1*:

``` cpp
vector v = {1, 2, 3, 4};

for (auto i : v | views::adjacent_transform<2>(std::multiplies())) {
  cout << i << ' ';     // prints 2 6 12
}
```

— *end example*\]

#### Class template `adjacent_transform_view` <a id="range.adjacent.transform.view">[[range.adjacent.transform.view]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, move_constructible F, size_t N>
    requires view<V> && (N > 0) && is_object_v<F> &&
             regular_invocable<F&, REPEAT(range_reference_t<V>, N)...> &&
             can-reference<invoke_result_t<F&, REPEAT(range_reference_t<V>, N)...>>
  class adjacent_transform_view : public view_interface<adjacent_transform_view<V, F, N>> {
    movable-box<F> fun_;                        // exposition only
    adjacent_view<V, N> inner_;                 // exposition only

    using InnerView = adjacent_view<V, N>;      // exposition only
    template<bool Const>
      using inner-iterator = iterator_t<maybe-const<Const, InnerView>>;         // exposition only
    template<bool Const>
      using inner-sentinel = sentinel_t<maybe-const<Const, InnerView>>;         // exposition only

    // [range.adjacent.transform.iterator], class template adjacent_transform_view::iterator
    template<bool> class iterator;              // exposition only

    // [range.adjacent.transform.sentinel], class template adjacent_transform_view::sentinel
    template<bool> class sentinel;              // exposition only

  public:
    adjacent_transform_view() = default;
    constexpr explicit adjacent_transform_view(V base, F fun);

    constexpr V base() const & requires copy_constructible<InnerView> { return inner_.base(); }
    constexpr V base() && { return std::move(inner_).base(); }

    constexpr auto begin() {
      return iterator<false>(*this, inner_.begin());
    }

    constexpr auto begin() const
      requires range<const InnerView> &&
               regular_invocable<const F&, REPEAT(range_reference_t<const V>, N)...> {
      return iterator<true>(*this, inner_.begin());
    }

    constexpr auto end() {
      if constexpr (common_range<InnerView>) {
        return iterator<false>(*this, inner_.end());
      } else {
        return sentinel<false>(inner_.end());
      }
    }

    constexpr auto end() const
      requires range<const InnerView> &&
               regular_invocable<const F&, REPEAT(range_reference_t<const V>, N)...> {
      if constexpr (common_range<const InnerView>) {
        return iterator<true>(*this, inner_.end());
      } else {
        return sentinel<true>(inner_.end());
      }
    }

    constexpr auto size() requires sized_range<InnerView> {
      return inner_.size();
    }

    constexpr auto size() const requires sized_range<const InnerView> {
      return inner_.size();
    }
  };
}
```

``` cpp
constexpr explicit adjacent_transform_view(V base, F fun);
```

*Effects:* Initializes *fun\_* with `std::move(fun)` and *inner\_* with
`std::move(base)`.

#### Class template `adjacent_transform_view::iterator` <a id="range.adjacent.transform.iterator">[[range.adjacent.transform.iterator]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, move_constructible F, size_t N>
    requires view<V> && (N > 0) && is_object_v<F> &&
             regular_invocable<F&, REPEAT(range_reference_t<V>, N)...> &&
             can-reference<invoke_result_t<F&, REPEAT(range_reference_t<V>, N)...>>
  template<bool Const>
  class adjacent_transform_view<V, F, N>::iterator {
    using Parent = maybe-const<Const, adjacent_transform_view>;         // exposition only
    using Base = maybe-const<Const, V>;                                 // exposition only
    Parent* parent_ = nullptr;                                          // exposition only
    inner-iterator<Const> inner_;                                       // exposition only

    constexpr iterator(Parent& parent, inner-iterator<Const> inner);    // exposition only

  public:
    using iterator_category = see below;
    using iterator_concept  = typename inner-iterator<Const>::iterator_concept;
    using value_type =
      remove_cvref_t<invoke_result_t<maybe-const<Const, F>&,
                                     REPEAT(range_reference_t<Base>, N)...>>;
    using difference_type = range_difference_t<Base>;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<inner-iterator<false>, inner-iterator<Const>>;

    constexpr decltype(auto) operator*() const noexcept(see below);
    constexpr iterator& operator++();
    constexpr iterator operator++(int);
    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;
    constexpr iterator& operator+=(difference_type x) requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x) requires random_access_range<Base>;

    constexpr decltype(auto) operator[](difference_type n) const
      requires random_access_range<Base>;

    friend constexpr bool operator==(const iterator& x, const iterator& y);
    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator<=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base> && three_way_comparable<inner-iterator<Const>>;

    friend constexpr iterator operator+(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, const iterator& i)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<inner-iterator<Const>, inner-iterator<Const>>;
  };
}
```

The member *typedef-name* `iterator::iterator_category` is defined as
follows:

- If `invoke_result_t<maybe-const<Const, F>&,
  REPEAT(range_reference_t<Base>, N)...>` isnot a reference,
  `iterator_category` denotes `input_iterator_tag`.
- Otherwise, let `C` denote the type
  `iterator_traits<iterator_t<Base>>::iterator_category`.
  - If `derived_from<C, random_access_iterator_tag>` is `true`,
    `iterator_category` denotes `random_access_iterator_tag`.
  - Otherwise, if `derived_from<C, bidirectional_iterator_tag>` is
    `true`, `iterator_category` denotes `bidirectional_iterator_tag`.
  - Otherwise, if `derived_from<C, forward_iterator_tag>` is `true`,
    `iterator_category` denotes `forward_iterator_tag`.
  - Otherwise, `iterator_category` denotes `input_iterator_tag`.

``` cpp
constexpr iterator(Parent& parent, inner-iterator<Const> inner);
```

*Effects:* Initializes *parent\_* with `addressof(parent)` and *inner\_*
with `std::move(inner)`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<inner-iterator<false>, inner-iterator<Const>>;
```

*Effects:* Initializes *parent\_* with `i.`*`parent_`* and *inner\_*
with `std::move(i.`*`inner_`*`)`.

``` cpp
constexpr decltype(auto) operator*() const noexcept(see below);
```

*Effects:* Equivalent to:

``` cpp
return apply([&](const auto&... iters) -> decltype(auto) {
  return invoke(*parent_->fun_, *iters...);
}, inner_.current_);
```

*Remarks:* Let `Is` be the pack `0, 1, …, (N-1)`. The exception
specification is equivalent to:

``` cpp
noexcept(invoke(*parent_->fun_, *std::get<Is>(inner_.current_)...))
```

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
++inner_;
return *this;
```

``` cpp
constexpr iterator operator++(int);
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
--inner_;
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
constexpr iterator& operator+=(difference_type x) requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
inner_ += x;
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type x) requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
inner_ -= x;
return *this;
```

``` cpp
constexpr decltype(auto) operator[](difference_type n) const
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
return apply([&](const auto&... iters) -> decltype(auto) {
  return invoke(*parent_->fun_, iters[n]...);
}, inner_.current_);
```

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y);
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
friend constexpr bool operator>(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
friend constexpr bool operator<=(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
friend constexpr bool operator>=(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires random_access_range<Base> && three_way_comparable<inner-iterator<Const>>;
```

Let *op* be the operator.

*Effects:* Equivalent to:
`return x.`*`inner_`*` `*`op`*` y.`*`inner_`*`;`

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return `*`iterator`*`(*i.`*`parent_`*`, i.`*`inner_`*` + n);`

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return `*`iterator`*`(*i.`*`parent_`*`, i.`*`inner_`*` - n);`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<inner-iterator<Const>, inner-iterator<Const>>;
```

*Effects:* Equivalent to: `return x.`*`inner_`*` - y.`*`inner_`*`;`

#### Class template `adjacent_transform_view::sentinel` <a id="range.adjacent.transform.sentinel">[[range.adjacent.transform.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, move_constructible F, size_t N>
    requires view<V> && (N > 0) && is_object_v<F> &&
             regular_invocable<F&, REPEAT(range_reference_t<V>, N)...> &&
             can-reference<invoke_result_t<F&, REPEAT(range_reference_t<V>, N)...>>
  template<bool Const>
  class adjacent_transform_view<V, F, N>::sentinel {
    inner-sentinel<Const> inner_;                               // exposition only
    constexpr explicit sentinel(inner-sentinel<Const> inner);   // exposition only

  public:
    sentinel() = default;
    constexpr sentinel(sentinel<!Const> i)
      requires Const && convertible_to<inner-sentinel<false>, inner-sentinel<Const>>;

    template<bool OtherConst>
      requires sentinel_for<inner-sentinel<Const>, inner-iterator<OtherConst>>
    friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<inner-sentinel<Const>, inner-iterator<OtherConst>>
    friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
      operator-(const iterator<OtherConst>& x, const sentinel& y);

    template<bool OtherConst>
      requires sized_sentinel_for<inner-sentinel<Const>, inner-iterator<OtherConst>>
    friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
      operator-(const sentinel& x, const iterator<OtherConst>& y);
  };
}
```

``` cpp
constexpr explicit sentinel(inner-sentinel<Const> inner);
```

*Effects:* Initializes *inner\_* with `inner`.

``` cpp
constexpr sentinel(sentinel<!Const> i)
  requires Const && convertible_to<inner-sentinel<false>, inner-sentinel<Const>>;
```

*Effects:* Initializes *inner\_* with `std::move(i.`*`inner_`*`)`.

``` cpp
template<bool OtherConst>
  requires sentinel_for<inner-sentinel<Const>, inner-iterator<OtherConst>>
friend constexpr bool operator==(const iterator<OtherConst>& x, const sentinel& y);
```

*Effects:* Equivalent to `return x.`*`inner_`*` == y.`*`inner_`*`;`

``` cpp
template<bool OtherConst>
  requires sized_sentinel_for<inner-sentinel<Const>, inner-iterator<OtherConst>>
friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
  operator-(const iterator<OtherConst>& x, const sentinel& y);

template<bool OtherConst>
  requires sized_sentinel_for<inner-sentinel<Const>, inner-iterator<OtherConst>>
friend constexpr range_difference_t<maybe-const<OtherConst, InnerView>>
  operator-(const sentinel& x, const iterator<OtherConst>& y);
```

*Effects:* Equivalent to `return x.`*`inner_`*` - y.`*`inner_`*`;`

### Chunk view <a id="range.chunk">[[range.chunk]]</a>

#### Overview <a id="range.chunk.overview">[[range.chunk.overview]]</a>

`chunk_view` takes a view and a number N and produces a range of views
that are N-sized non-overlapping successive chunks of the elements of
the original view, in order. The last view in the range can have fewer
than N elements.

The name `views::chunk` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `N`, the
expression `views::chunk(E, N)` is expression-equivalent to
`chunk_view(E, N)`.

\[*Example 1*:

``` cpp
vector v = {1, 2, 3, 4, 5};

for (auto r : v | views::chunk(2)) {
  cout << '[';
  auto sep = "";
  for (auto i : r) {
    cout << sep << i;
    sep = ", ";
  }
  cout << "] ";
}
// The above prints [1, 2] [3, 4] [5]
```

— *end example*\]

#### Class template `chunk_view` for input ranges <a id="range.chunk.view.input">[[range.chunk.view.input]]</a>

``` cpp
namespace std::ranges {
  template<class I>
  constexpr I div-ceil(I num, I denom) {                  // exposition only
    I r = num / denom;
    if (num % denom)
      ++r;
    return r;
  }

  template<view V>
    requires input_range<V>
  class chunk_view : public view_interface<chunk_view<V>> {
    V base_;                                              // exposition only
    range_difference_t<V> n_;                             // exposition only
    range_difference_t<V> remainder_ = 0;                 // exposition only

    non-propagating-cache<iterator_t<V>> current_;       // exposition only

    // [range.chunk.outer.iter], class chunk_view::outer-iterator
    class outer-iterator;                                 // exposition only

    // [range.chunk.inner.iter], class chunk_view::inner-iterator
    class inner-iterator;                                 // exposition only

  public:
    constexpr explicit chunk_view(V base, range_difference_t<V> n);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr outer-iterator begin();
    constexpr default_sentinel_t end() const noexcept;

    constexpr auto size() requires sized_range<V>;
    constexpr auto size() const requires sized_range<const V>;
  };

  template<class R>
    chunk_view(R&&, range_difference_t<R>) -> chunk_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit chunk_view(V base, range_difference_t<V> n);
```

*Preconditions:* `n > 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *n\_* with
`n`.

``` cpp
constexpr outer-iterator begin();
```

*Effects:* Equivalent to:

``` cpp
current_ = ranges::begin(base_);
remainder_ = n_;
return outer-iterator(*this);
```

``` cpp
constexpr default_sentinel_t end() const noexcept;
```

*Returns:* `default_sentinel`.

``` cpp
constexpr auto size() requires sized_range<V>;
constexpr auto size() const requires sized_range<const V>;
```

*Effects:* Equivalent to:

``` cpp
return to-unsigned-like(div-ceil(ranges::distance(base_), n_));
```

#### Class `chunk_view::outer-iterator` <a id="range.chunk.outer.iter">[[range.chunk.outer.iter]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires input_range<V>
  class chunk_view<V>::outer-iterator {
    chunk_view* parent_;                                        // exposition only

    constexpr explicit outer-iterator(chunk_view& parent);      // exposition only

  public:
    using iterator_concept = input_iterator_tag;
    using difference_type  = range_difference_t<V>;

    // [range.chunk.outer.value], class chunk_view::outer-iterator::value_type
    struct value_type;

    outer-iterator(outer-iterator&&) = default;
    outer-iterator& operator=(outer-iterator&&) = default;

    constexpr value_type operator*() const;
    constexpr outer-iterator& operator++();
    constexpr void operator++(int);

    friend constexpr bool operator==(const outer-iterator& x, default_sentinel_t);

    friend constexpr difference_type operator-(default_sentinel_t y, const outer-iterator& x)
      requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
    friend constexpr difference_type operator-(const outer-iterator& x, default_sentinel_t y)
      requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
  };
}
```

``` cpp
constexpr explicit outer-iterator(chunk_view& parent);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`.

``` cpp
constexpr value_type operator*() const;
```

*Preconditions:* `*this == default_sentinel` is `false`.

*Returns:* `value_type(*`*`parent_`*`)`.

``` cpp
constexpr outer-iterator& operator++();
```

*Preconditions:* `*this == default_sentinel` is `false`.

*Effects:* Equivalent to:

``` cpp
ranges::advance(*parent_->current_, parent_->remainder_, ranges::end(parent_->base_));
parent_->remainder_ = parent_->n_;
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
friend constexpr bool operator==(const outer-iterator& x, default_sentinel_t);
```

*Effects:* Equivalent to:

``` cpp
return *x.parent_->current_ == ranges::end(x.parent_->base_) && x.parent_->remainder_ != 0;
```

``` cpp
friend constexpr difference_type operator-(default_sentinel_t y, const outer-iterator& x)
  requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Effects:* Equivalent to:

``` cpp
const auto dist = ranges::end(x.parent_->base_) - *x.parent_->current_;
if (dist < x.parent_->remainder_) {
  return dist == 0 ? 0 : 1;
}
return div-ceil(dist - x.parent_->remainder_, x.parent_->n_) + 1;
```

``` cpp
friend constexpr difference_type operator-(const outer-iterator& x, default_sentinel_t y)
  requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Effects:* Equivalent to: `return -(y - x);`

#### Class `chunk_view::outer-iterator::value_type` <a id="range.chunk.outer.value">[[range.chunk.outer.value]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires input_range<V>
  struct chunk_view<V>::outer-iterator::value_type : view_interface<value_type> {
  private:
    chunk_view* parent_;                                        // exposition only

    constexpr explicit value_type(chunk_view& parent);          // exposition only

  public:
    constexpr inner-iterator begin() const noexcept;
    constexpr default_sentinel_t end() const noexcept;

    constexpr auto size() const
      requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
  };
}
```

``` cpp
constexpr explicit value_type(chunk_view& parent);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`.

``` cpp
constexpr inner-iterator begin() const noexcept;
```

*Returns:* *`inner-iterator`*`(*`*`parent_`*`)`.

``` cpp
constexpr default_sentinel_t end() const noexcept;
```

*Returns:* `default_sentinel`.

``` cpp
constexpr auto size() const
  requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Effects:* Equivalent to:

``` cpp
return to-unsigned-like(ranges::min(parent_->remainder_,
                                ranges::end(parent_->base_) - *parent_->current_));
```

#### Class `chunk_view::inner-iterator` <a id="range.chunk.inner.iter">[[range.chunk.inner.iter]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires input_range<V>
  class chunk_view<V>::inner-iterator {
    chunk_view* parent_;                                                // exposition only

    constexpr explicit inner-iterator(chunk_view& parent) noexcept;     // exposition only

  public:
    using iterator_concept = input_iterator_tag;
    using difference_type = range_difference_t<V>;
    using value_type = range_value_t<V>;

    inner-iterator(inner-iterator&&) = default;
    inner-iterator& operator=(inner-iterator&&) = default;

    constexpr const iterator_t<V>& base() const &;

    constexpr range_reference_t<V> operator*() const;
    constexpr inner-iterator& operator++();
    constexpr void operator++(int);

    friend constexpr bool operator==(const inner-iterator& x, default_sentinel_t);

    friend constexpr difference_type operator-(default_sentinel_t y, const inner-iterator& x)
      requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
    friend constexpr difference_type operator-(const inner-iterator& x, default_sentinel_t y)
      requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;

    friend constexpr range_rvalue_reference_t<V> iter_move(const inner-iterator& i)
      noexcept(noexcept(ranges::iter_move(*i.parent_->current_)));

    friend constexpr void iter_swap(const inner-iterator& x, const inner-iterator& y)
      noexcept(noexcept(ranges::iter_swap(*x.parent_->current_, *y.parent_->current_)))
      requires indirectly_swappable<iterator_t<V>>;
  };
}
```

``` cpp
constexpr explicit inner-iterator(chunk_view& parent) noexcept;
```

*Effects:* Initializes *parent\_* with `addressof(parent)`.

``` cpp
constexpr const iterator_t<V>& base() const &;
```

*Effects:* Equivalent to: `return *`*`parent_`*`->`*`current_`*`;`

``` cpp
constexpr range_reference_t<V> operator*() const;
```

*Preconditions:* `*this == default_sentinel` is `false`.

*Effects:* Equivalent to: `return **`*`parent_`*`->`*`current_`*`;`

``` cpp
constexpr inner-iterator& operator++();
```

*Preconditions:* `*this == default_sentinel` is `false`.

*Effects:* Equivalent to:

``` cpp
++*parent_->current_;
if (*parent_->current_ == ranges::end(parent_->base_))
  parent_->remainder_ = 0;
else
  --parent_->remainder_;
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
friend constexpr bool operator==(const inner-iterator& x, default_sentinel_t);
```

*Returns:* `x.`*`parent_`*`->`*`remainder_`*` == 0`.

``` cpp
friend constexpr difference_type operator-(default_sentinel_t y, const inner-iterator& x)
  requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Effects:* Equivalent to:

``` cpp
return ranges::min(x.parent_->remainder_,
                   ranges::end(x.parent_->base_) - *x.parent_->current_);
```

``` cpp
friend constexpr difference_type operator-(const inner-iterator& x, default_sentinel_t y)
  requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Effects:* Equivalent to: `return -(y - x);`

``` cpp
friend constexpr range_rvalue_reference_t<V> iter_move(const inner-iterator& i)
  noexcept(noexcept(ranges::iter_move(*i.parent_->current_)));
```

*Effects:* Equivalent to:
`return ranges::iter_move(*i.`*`parent_`*`->`*`current_`*`);`

``` cpp
friend constexpr void iter_swap(const inner-iterator& x, const inner-iterator& y)
  noexcept(noexcept(ranges::iter_swap(*x.parent_->current_, *y.parent_->current_)))
  requires indirectly_swappable<iterator_t<V>>;
```

*Effects:* Equivalent to:
`ranges::iter_swap(*x.`*`parent_`*`->`*`current_`*`, *y.`*`parent_`*`->`*`current_`*`);`

#### Class template `chunk_view` for forward ranges <a id="range.chunk.view.fwd">[[range.chunk.view.fwd]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires forward_range<V>
  class chunk_view<V> : public view_interface<chunk_view<V>> {
    V base_;                            // exposition only
    range_difference_t<V> n_;           // exposition only

    // [range.chunk.fwd.iter], class template chunk_view::iterator
    template<bool> class iterator;      // exposition only

  public:
    constexpr explicit chunk_view(V base, range_difference_t<V> n);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin() requires (!simple-view<V>) {
      return iterator<false>(this, ranges::begin(base_));
    }

    constexpr auto begin() const requires forward_range<const V> {
      return iterator<true>(this, ranges::begin(base_));
    }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (common_range<V> && sized_range<V>) {
        auto missing = (n_ - ranges::distance(base_) % n_) % n_;
        return iterator<false>(this, ranges::end(base_), missing);
      } else if constexpr (common_range<V> && !bidirectional_range<V>) {
        return iterator<false>(this, ranges::end(base_));
      } else {
        return default_sentinel;
      }
    }

    constexpr auto end() const requires forward_range<const V> {
      if constexpr (common_range<const V> && sized_range<const V>) {
        auto missing = (n_ - ranges::distance(base_) % n_) % n_;
        return iterator<true>(this, ranges::end(base_), missing);
      } else if constexpr (common_range<const V> && !bidirectional_range<const V>) {
        return iterator<true>(this, ranges::end(base_));
      } else {
        return default_sentinel;
      }
    }

    constexpr auto size() requires sized_range<V>;
    constexpr auto size() const requires sized_range<const V>;
  };
}
```

``` cpp
constexpr explicit chunk_view(V base, range_difference_t<V> n);
```

*Preconditions:* `n > 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *n\_* with
`n`.

``` cpp
constexpr auto size() requires sized_range<V>;
constexpr auto size() const requires sized_range<const V>;
```

*Effects:* Equivalent to:

``` cpp
return to-unsigned-like(div-ceil(ranges::distance(base_), n_));
```

#### Class template `chunk_view::iterator` for forward ranges <a id="range.chunk.fwd.iter">[[range.chunk.fwd.iter]]</a>

``` cpp
namespace std::ranges {
  template<view V>
    requires forward_range<V>
  template<bool Const>
  class chunk_view<V>::iterator {
    using Parent = maybe-const<Const, chunk_view>;                      // exposition only
    using Base = maybe-const<Const, V>;                                 // exposition only

    iterator_t<Base> current_ = iterator_t<Base>();                     // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();                         // exposition only
    range_difference_t<Base> n_ = 0;                                    // exposition only
    range_difference_t<Base> missing_ = 0;                              // exposition only

    constexpr iterator(Parent* parent, iterator_t<Base> current,       // exposition only
                       range_difference_t<Base> missing = 0);

  public:
    using iterator_category = input_iterator_tag;
    using iterator_concept = see below;
    using value_type = decltype(views::take(subrange(current_, end_), n_));
    using difference_type = range_difference_t<Base>;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>
                     && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr iterator_t<Base> base() const;

    constexpr value_type operator*() const;
    constexpr iterator& operator++();
    constexpr iterator operator++(int);

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x)
      requires random_access_range<Base>;

    constexpr value_type operator[](difference_type n) const
      requires random_access_range<Base>;

    friend constexpr bool operator==(const iterator& x, const iterator& y);
    friend constexpr bool operator==(const iterator& x, default_sentinel_t);

    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator<=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base> &&
               three_way_comparable<iterator_t<Base>>;

    friend constexpr iterator operator+(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, const iterator& i)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;

    friend constexpr difference_type operator-(default_sentinel_t y, const iterator& x)
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
    friend constexpr difference_type operator-(const iterator& x, default_sentinel_t y)
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, `iterator_concept` denotes `forward_iterator_tag`.

``` cpp
constexpr iterator(Parent* parent, iterator_t<Base> current,
                   range_difference_t<Base> missing = 0);
```

*Effects:* Initializes *current\_* with `current`, *end\_* with
`ranges::end(parent->`*`base_`*`)`, *n\_* with `parent``->`*`n_`*, and
*missing\_* with `missing`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>
                 && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`,
*end\_* with `std::move(i.`*`end_`*`)`, *n\_* with `i.`*`n_`*, and
*missing\_* with `i.`*`missing_`*.

``` cpp
constexpr iterator_t<Base> base() const;
```

*Returns:* *current\_*.

``` cpp
constexpr value_type operator*() const;
```

*Preconditions:* *`current_`*` != `*`end_`* is `true`.

*Returns:*
`views::take(subrange(`*`current_`*`, `*`end_`*`), `*`n_`*`)`.

``` cpp
constexpr iterator& operator++();
```

*Preconditions:* *`current_`*` != `*`end_`* is `true`.

*Effects:* Equivalent to:

``` cpp
missing_ = ranges::advance(current_, n_, end_);
return *this;
```

``` cpp
constexpr iterator operator++(int);
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
ranges::advance(current_, missing_ - n_);
missing_ = 0;
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
constexpr iterator& operator+=(difference_type x)
  requires random_access_range<Base>;
```

*Preconditions:* If `x` is positive,
`ranges::distance(`*`current_`*`, `*`end_`*`) > `*`n_`*` * (x - 1)` is
`true`.

\[*Note 1*: If `x` is negative, the *Effects* paragraph implies a
precondition. — *end note*\]

*Effects:* Equivalent to:

``` cpp
if (x > 0) {
  ranges::advance(current_, n_ * (x - 1));
  missing_ = ranges::advance(current_, n_, end_);
} else if (x < 0) {
  ranges::advance(current_, n_ * x + missing_);
  missing_ = 0;
}
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return *this += -x;`

``` cpp
constexpr value_type operator[](difference_type n) const
  requires random_access_range<Base>;
```

*Returns:* `*(*this + n)`.

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y);
```

*Returns:* `x.`*`current_`*` == y.`*`current_`*.

``` cpp
friend constexpr bool operator==(const iterator& x, default_sentinel_t);
```

*Returns:* `x.`*`current_`*` == x.`*`end_`*.

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Returns:* `x.`*`current_`*` < y.`*`current_`*.

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
  requires random_access_range<Base> &&
           three_way_comparable<iterator_t<Base>>;
```

*Returns:* `x.`*`current_`*` <=> y.`*`current_`*.

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r += n;
return r;
```

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r -= n;
return r;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
```

*Returns:*
`(x.`*`current_`*` - y.`*`current_`*` + x.`*`missing_`*` - y.`*`missing_`*`) / x.`*`n_`*.

``` cpp
friend constexpr difference_type operator-(default_sentinel_t y, const iterator& x)
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Returns:* *`div-ceil`*`(x.`*`end_`*` - x.`*`current_`*`, x.`*`n_`*`)`.

``` cpp
friend constexpr difference_type operator-(const iterator& x, default_sentinel_t y)
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return -(y - x);`

### Slide view <a id="range.slide">[[range.slide]]</a>

#### Overview <a id="range.slide.overview">[[range.slide.overview]]</a>

`slide_view` takes a view and a number N and produces a view whose Mᵗʰ
element is a view over the Mᵗʰ through (M + N - 1)ᵗʰ elements of the
original view. If the original view has fewer than N elements, the
resulting view is empty.

The name `views::slide` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `N`, the
expression `views::slide(E, N)` is expression-equivalent to
`slide_view(E, N)`.

\[*Example 1*:

``` cpp
vector v = {1, 2, 3, 4};

for (auto i : v | views::slide(2)) {
  cout << '[' << i[0] << ", " << i[1] << "] ";          // prints [1, 2] [2, 3] [3, 4]
}
```

— *end example*\]

#### Class template `slide_view` <a id="range.slide.view">[[range.slide.view]]</a>

``` cpp
namespace std::ranges {
  template<class V>
  concept slide-caches-nothing = random_access_range<V> && sized_range<V>;       // exposition only

  template<class V>
  concept slide-caches-last =                                            // exposition only
    !slide-caches-nothing<V> && bidirectional_range<V> && common_range<V>;

  template<class V>
  concept slide-caches-first =                                           // exposition only
    !slide-caches-nothing<V> && !slide-caches-last<V>;

  template<forward_range V>
    requires view<V>
  class slide_view : public view_interface<slide_view<V>> {
    V base_;                            // exposition only
    range_difference_t<V> n_;           // exposition only

    // [range.slide.iterator], class template slide_view::iterator
    template<bool> class iterator;      // exposition only

    // [range.slide.sentinel], class slide_view::sentinel
    class sentinel;                     // exposition only

  public:
    constexpr explicit slide_view(V base, range_difference_t<V> n);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr auto begin()
      requires (!(simple-view<V> && slide-caches-nothing<const V>));
    constexpr auto begin() const requires slide-caches-nothing<const V>;

    constexpr auto end()
      requires (!(simple-view<V> && slide-caches-nothing<const V>));
    constexpr auto end() const requires slide-caches-nothing<const V>;

    constexpr auto size() requires sized_range<V>;
    constexpr auto size() const requires sized_range<const V>;
  };

  template<class R>
    slide_view(R&&, range_difference_t<R>) -> slide_view<views::all_t<R>>;
}
```

``` cpp
constexpr explicit slide_view(V base, range_difference_t<V> n);
```

*Preconditions:* `n > 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *n\_* with
`n`.

``` cpp
constexpr auto begin()
  requires (!(simple-view<V> && slide-caches-nothing<const V>));
```

*Returns:*

- If `V` models `slide-caches-first`,
  ``` cpp
  iterator<false>(ranges::begin(base_),
                  ranges::next(ranges::begin(base_), n_ - 1, ranges::end(base_)), n_)
  ```
- Otherwise,
  *`iterator`*`<false>(ranges::begin(`*`base_`*`), `*`n_`*`)`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept, this function caches the result within
the `slide_view` for use on subsequent calls when `V` models
`slide-caches-first`.

``` cpp
constexpr auto begin() const requires slide-caches-nothing<const V>;
```

*Returns:* *`iterator`*`<true>(ranges::begin(`*`base_`*`), `*`n_`*`)`.

``` cpp
constexpr auto end()
  requires (!(simple-view<V> && slide-caches-nothing<const V>));
```

*Returns:*

- If `V` models `slide-caches-nothing`,
  ``` cpp
  iterator<false>(ranges::begin(base_) + range_difference_t<V>(size()), n_)
  ```
- Otherwise, if `V` models `slide-caches-last`,
  ``` cpp
  iterator<false>(ranges::prev(ranges::end(base_), n_ - 1, ranges::begin(base_)), n_)
  ```
- Otherwise, if `V` models `common_range`,
  ``` cpp
  iterator<false>(ranges::end(base_), ranges::end(base_), n_)
  ```
- Otherwise, *`sentinel`*`(ranges::end(`*`base_`*`))`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept, this function caches the result within
the `slide_view` for use on subsequent calls when `V` models
`slide-caches-last`.

``` cpp
constexpr auto end() const requires slide-caches-nothing<const V>;
```

*Returns:* `begin() + range_difference_t<const V>(size())`.

``` cpp
constexpr auto size() requires sized_range<V>;
constexpr auto size() const requires sized_range<const V>;
```

*Effects:* Equivalent to:

``` cpp
auto sz = ranges::distance(base_) - n_ + 1;
if (sz < 0) sz = 0;
return to-unsigned-like(sz);
```

#### Class template `slide_view::iterator` <a id="range.slide.iterator">[[range.slide.iterator]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V>
    requires view<V>
  template<bool Const>
  class slide_view<V>::iterator {
    using Base = maybe-const<Const, V>;                 // exposition only
    iterator_t<Base> current_   = iterator_t<Base>();   // exposition only
    iterator_t<Base> last_ele_  = iterator_t<Base>();   // exposition only,
                                               // present only if Base models slide-caches-first
    range_difference_t<Base> n_ = 0;                    // exposition only

    constexpr iterator(iterator_t<Base> current, range_difference_t<Base> n) // exposition only
      requires (!slide-caches-first<Base>);

    constexpr iterator(iterator_t<Base> current, iterator_t<Base> last_ele,  // exposition only
                       range_difference_t<Base> n)
      requires slide-caches-first<Base>;

  public:
    using iterator_category = input_iterator_tag;
    using iterator_concept = see below;
    using value_type = decltype(views::counted(current_, n_));
    using difference_type = range_difference_t<Base>;

    iterator() = default;
    constexpr iterator(iterator<!Const> i)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;

    constexpr auto operator*() const;
    constexpr iterator& operator++();
    constexpr iterator operator++(int);

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type x)
      requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type x)
      requires random_access_range<Base>;

    constexpr auto operator[](difference_type n) const
      requires random_access_range<Base>;

    friend constexpr bool operator==(const iterator& x, const iterator& y);

    friend constexpr bool operator<(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator<=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr bool operator>=(const iterator& x, const iterator& y)
      requires random_access_range<Base>;
    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires random_access_range<Base> &&
               three_way_comparable<iterator_t<Base>>;

    friend constexpr iterator operator+(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, const iterator& i)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& i, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, `iterator_concept` denotes `forward_iterator_tag`.

If the invocation of any non-const member function of *iterator* exits
via an exception, the *iterator* acquires a singular value.

``` cpp
constexpr iterator(iterator_t<Base> current, range_difference_t<Base> n)
  requires (!slide-caches-first<Base>);
```

*Effects:* Initializes *current\_* with `current` and *n\_* with `n`.

``` cpp
constexpr iterator(iterator_t<Base> current, iterator_t<Base> last_ele,
                   range_difference_t<Base> n)
  requires slide-caches-first<Base>;
```

*Effects:* Initializes *current\_* with `current`, *last_ele\_* with
`last_ele`, and *n\_* with `n`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>;
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`
and *n\_* with `i.`*`n_`*.

\[*Note 1*: *`iterator`*`<true>` can only be formed when *Base* models
`slide-caches-nothing`, in which case *last_ele\_* is not
present. — *end note*\]

``` cpp
constexpr auto operator*() const;
```

*Returns:* `views::counted(`*`current_`*`, `*`n_`*`)`.

``` cpp
constexpr iterator& operator++();
```

*Preconditions:* *current\_* and *last_ele\_* (if present) are
incrementable.

*Ensures:* *current\_* and *last_ele\_* (if present) are each equal to
`ranges::next(i)`, where `i` is the value of that data member before the
call.

*Returns:* `*this`.

``` cpp
constexpr iterator operator++(int);
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

*Preconditions:* *current\_* and *last_ele\_* (if present) are
decrementable.

*Ensures:* *current\_* and *last_ele\_* (if present) are each equal to
`ranges::prev(i)`, where `i` is the value of that data member before the
call.

*Returns:* `*this`.

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
constexpr iterator& operator+=(difference_type x)
  requires random_access_range<Base>;
```

*Preconditions:* *`current_`*` + x` and *`last_ele_`*` + x` (if
*last_ele\_* is present) have well-defined behavior.

*Ensures:* *current\_* and *last_ele\_* (if present) are each equal to
`i + x`, where `i` is the value of that data member before the call.

*Returns:* `*this`.

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires random_access_range<Base>;
```

*Preconditions:* *`current_`*` - x` and *`last_ele_`*` - x` (if
*last_ele\_* is present) have well-defined behavior.

*Ensures:* *current\_* and *last_ele\_* (if present) are each equal to
`i - x`, where `i` is the value of that data member before the call.

*Returns:* `*this`.

``` cpp
constexpr auto operator[](difference_type n) const
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:
`return views::counted(`*`current_`*` + n, `*`n_`*`);`

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y);
```

*Returns:* If *last_ele\_* is present,
`x.`*`last_ele_`*` == y.`*`last_ele_`*; otherwise,
`x.`*`current_`*` == y.`*`cur``rent_`*.

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Returns:* `x.`*`current_`*` < y.`*`current_`*.

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
  requires random_access_range<Base> &&
           three_way_comparable<iterator_t<Base>>;
```

*Returns:* `x.`*`current_`*` <=> y.`*`current_`*.

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r += n;
return r;
```

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r -= n;
return r;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
```

*Returns:* If *last_ele\_* is present,
`x.`*`last_ele_`*` - y.`*`last_ele_`*; otherwise,
`x.`*`current_`*` - y.`*`cur``rent_`*.

#### Class `slide_view::sentinel` <a id="range.slide.sentinel">[[range.slide.sentinel]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V>
    requires view<V>
  class slide_view<V>::sentinel {
    sentinel_t<V> end_ = sentinel_t<V>();             // exposition only
    constexpr explicit sentinel(sentinel_t<V> end);   // exposition only

  public:
    sentinel() = default;

    friend constexpr bool operator==(const iterator<false>& x, const sentinel& y);

    friend constexpr range_difference_t<V>
      operator-(const iterator<false>& x, const sentinel& y)
        requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;

    friend constexpr range_difference_t<V>
      operator-(const sentinel& y, const iterator<false>& x)
        requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
  };
}
```

\[*Note 1*: *sentinel* is used only when `slide-caches-first<V>` is
`true`. — *end note*\]

``` cpp
constexpr explicit sentinel(sentinel_t<V> end);
```

*Effects:* Initializes *end\_* with `end`.

``` cpp
friend constexpr bool operator==(const iterator<false>& x, const sentinel& y);
```

*Returns:* `x.`*`last_ele_`*` == y.`*`end_`*.

``` cpp
friend constexpr range_difference_t<V>
  operator-(const iterator<false>& x, const sentinel& y)
    requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Returns:* `x.`*`last_ele_`*` - y.`*`end_`*.

``` cpp
friend constexpr range_difference_t<V>
  operator-(const sentinel& y, const iterator<false>& x)
    requires sized_sentinel_for<sentinel_t<V>, iterator_t<V>>;
```

*Returns:* `y.`*`end_`*` - x.`*`last_ele_`*.

### Chunk by view <a id="range.chunk.by">[[range.chunk.by]]</a>

#### Overview <a id="range.chunk.by.overview">[[range.chunk.by.overview]]</a>

`chunk_by_view` takes a view and a predicate, and splits the view into
`subrange`s between each pair of adjacent elements for which the
predicate returns `false`.

The name `views::chunk_by` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `F`, the
expression `views::chunk_by(E, F)` is expression-equivalent to
`chunk_by_view(E, F)`.

\[*Example 1*:

``` cpp
vector v = {1, 2, 2, 3, 0, 4, 5, 2};

for (auto r : v | views::chunk_by(ranges::less_equal{})) {
  cout << '[';
  auto sep = "";
  for (auto i : r) {
    cout << sep << i;
    sep = ", ";
  }
  cout << "] ";
}
// The above prints [1, 2, 2, 3] [0, 4, 5] [2]
```

— *end example*\]

#### Class template `chunk_by_view` <a id="range.chunk.by.view">[[range.chunk.by.view]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, indirect_binary_predicate<iterator_t<V>, iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class chunk_by_view : public view_interface<chunk_by_view<V, Pred>> {
    V base_ = V();                                          // exposition only
    movable-box<Pred> pred_;                                // exposition only

    // [range.chunk.by.iter], class chunk_by_view::iterator
    class iterator;                                         // exposition only

  public:
    chunk_by_view() requires default_initializable<V> && default_initializable<Pred> = default;
    constexpr explicit chunk_by_view(V base, Pred pred);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr const Pred& pred() const;

    constexpr iterator begin();
    constexpr auto end();

    constexpr iterator_t<V> find-next(iterator_t<V>);       // exposition only
    constexpr iterator_t<V> find-prev(iterator_t<V>)        // exposition only
      requires bidirectional_range<V>;
  };

  template<class R, class Pred>
    chunk_by_view(R&&, Pred) -> chunk_by_view<views::all_t<R>, Pred>;
}
```

``` cpp
constexpr explicit chunk_by_view(V base, Pred pred);
```

*Effects:* Initializes *base\_* with `std::move(base)` and *pred\_* with
`std::move(pred)`.

``` cpp
constexpr const Pred& pred() const;
```

*Effects:* Equivalent to: `return *`*`pred_`*`;`

``` cpp
constexpr iterator begin();
```

*Preconditions:* *`pred_`*`.has_value()` is `true`.

*Returns:*
*`iterator`*`(*this, ranges::begin(`*`base_`*`), `*`find-next`*`(ranges::begin(`*`base_`*`)))`.

*Remarks:* In order to provide the amortized constant-time complexity
required by the `range` concept, this function caches the result within
the `chunk_by_view` for use on subsequent calls.

``` cpp
constexpr auto end();
```

*Effects:* Equivalent to:

``` cpp
if constexpr (common_range<V>) {
  return iterator(*this, ranges::end(base_), ranges::end(base_));
} else {
  return default_sentinel;
}
```

``` cpp
constexpr iterator_t<V> find-next(iterator_t<V> current);
```

*Preconditions:* *`pred_`*`.has_value()` is `true`.

*Returns:*

``` cpp
ranges::next(ranges::adjacent_find(current, ranges::end(base_), not_fn(ref(*pred_))),
             1, ranges::end(base_))
```

``` cpp
constexpr iterator_t<V> find-prev(iterator_t<V> current) requires bidirectional_range<V>;
```

*Preconditions:*

- `current` is not equal to `ranges::begin(`*`base_`*`)`.
- *`pred_`*`.has_value()` is `true`.

*Returns:* An iterator `i` in the range \[`ranges::begin(`*`base_`*`)`,
`current`) such that:

- `ranges::adjacent_find(i, current, not_fn(ref(*`*`pred_`*`)))` is
  equal to `current`; and
- if `i` is not equal to `ranges::begin(`*`base_`*`)`, then
  `bool(invoke(*`*`pred_`*`, *ranges::prev(i), *i))` is `false`.

#### Class `chunk_by_view::iterator` <a id="range.chunk.by.iter">[[range.chunk.by.iter]]</a>

``` cpp
namespace std::ranges {
  template<forward_range V, indirect_binary_predicate<iterator_t<V>, iterator_t<V>> Pred>
    requires view<V> && is_object_v<Pred>
  class chunk_by_view<V, Pred>::iterator {
    chunk_by_view* parent_ = nullptr;                                   // exposition only
    iterator_t<V> current_ = iterator_t<V>();                           // exposition only
    iterator_t<V> next_    = iterator_t<V>();                           // exposition only

    constexpr iterator(chunk_by_view& parent, iterator_t<V> current,    // exposition only
                       iterator_t<V> next);

  public:
    using value_type = subrange<iterator_t<V>>;
    using difference_type  = range_difference_t<V>;
    using iterator_category = input_iterator_tag;
    using iterator_concept = see below;

    iterator() = default;

    constexpr value_type operator*() const;
    constexpr iterator& operator++();
    constexpr iterator operator++(int);

    constexpr iterator& operator--() requires bidirectional_range<V>;
    constexpr iterator operator--(int) requires bidirectional_range<V>;

    friend constexpr bool operator==(const iterator& x, const iterator& y);
    friend constexpr bool operator==(const iterator& x, default_sentinel_t);
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If `V` models `bidirectional_range`, then `iterator_concept` denotes
  `bidirectional_iterator_tag`.
- Otherwise, `iterator_concept` denotes `forward_iterator_tag`.

``` cpp
constexpr iterator(chunk_by_view& parent, iterator_t<V> current, iterator_t<V> next);
```

*Effects:* Initializes *parent\_* with `addressof(parent)`, *current\_*
with `current`, and *next\_* with `next`.

``` cpp
constexpr value_type operator*() const;
```

*Preconditions:* *current\_* is not equal to *next\_*.

*Returns:* `subrange(`*`current_`*`, `*`next_`*`)`.

``` cpp
constexpr iterator& operator++();
```

*Preconditions:* *current\_* is not equal to *next\_*.

*Effects:* Equivalent to:

``` cpp
current_ = next_;
next_ = parent_->find-next(current_);
return *this;
```

``` cpp
constexpr iterator operator++(int);
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
next_ = current_;
current_ = parent_->find-prev(next_);
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
friend constexpr bool operator==(const iterator& x, const iterator& y);
```

*Returns:* `x.`*`current_`*` == y.`*`current_`*.

``` cpp
friend constexpr bool operator==(const iterator& x, default_sentinel_t);
```

*Returns:* `x.`*`current_`*` == x.`*`next_`*.

### Stride view <a id="range.stride">[[range.stride]]</a>

#### Overview <a id="range.stride.overview">[[range.stride.overview]]</a>

`stride_view` presents a view of an underlying sequence, advancing over
n elements at a time, as opposed to the usual single-step succession.

The name `views::stride` denotes a range adaptor object
[[range.adaptor.object]]. Given subexpressions `E` and `N`, the
expression `views::stride(E, N)` is expression-equivalent to
`stride_view(E, N)`.

\[*Example 1*:

``` cpp
auto input = views::iota(0, 12) | views::stride(3);
ranges::copy(input, ostream_iterator<int>(cout, " "));                  // prints 0 3 6 9
ranges::copy(input | views::reverse, ostream_iterator<int>(cout, " ")); // prints 9 6 3 0
```

— *end example*\]

#### Class template `stride_view` <a id="range.stride.view">[[range.stride.view]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V>
  class stride_view : public view_interface<stride_view<V>> {
    V base_;                                    // exposition only
    range_difference_t<V> stride_;              // exposition only
    // [range.stride.iterator], class template stride_view::iterator
    template<bool> class iterator;              // exposition only
  public:
    constexpr explicit stride_view(V base, range_difference_t<V> stride);

    constexpr V base() const & requires copy_constructible<V> { return base_; }
    constexpr V base() && { return std::move(base_); }

    constexpr range_difference_t<V> stride() const noexcept;

    constexpr auto begin() requires (!simple-view<V>) {
      return iterator<false>(this, ranges::begin(base_));
    }

    constexpr auto begin() const requires range<const V> {
      return iterator<true>(this, ranges::begin(base_));
    }

    constexpr auto end() requires (!simple-view<V>) {
      if constexpr (common_range<V> && sized_range<V> && forward_range<V>) {
        auto missing = (stride_ - ranges::distance(base_) % stride_) % stride_;
        return iterator<false>(this, ranges::end(base_), missing);
      } else if constexpr (common_range<V> && !bidirectional_range<V>) {
        return iterator<false>(this, ranges::end(base_));
      } else {
        return default_sentinel;
      }
    }

    constexpr auto end() const requires range<const V> {
      if constexpr (common_range<const V> && sized_range<const V> && forward_range<const V>) {
        auto missing = (stride_ - ranges::distance(base_) % stride_) % stride_;
        return iterator<true>(this, ranges::end(base_), missing);
      } else if constexpr (common_range<const V> && !bidirectional_range<const V>) {
        return iterator<true>(this, ranges::end(base_));
      } else {
        return default_sentinel;
      }
    }

    constexpr auto size() requires sized_range<V>;
    constexpr auto size() const requires sized_range<const V>;
  };

  template<class R>
    stride_view(R&&, range_difference_t<R>) -> stride_view<views::all_t<R>>;
}
```

``` cpp
constexpr stride_view(V base, range_difference_t<V> stride);
```

*Preconditions:* `stride > 0` is `true`.

*Effects:* Initializes *base\_* with `std::move(base)` and *stride\_*
with `stride`.

``` cpp
constexpr range_difference_t<V> stride() const noexcept;
```

*Returns:* *stride\_*.

``` cpp
constexpr auto size() requires sized_range<V>;
constexpr auto size() const requires sized_range<const V>;
```

*Effects:* Equivalent to:

``` cpp
return to-unsigned-like(div-ceil(ranges::distance(base_), stride_));
```

#### Class template `stride_view::iterator` <a id="range.stride.iterator">[[range.stride.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range V>
    requires view<V>
  template<bool Const>
  class stride_view<V>::iterator {
    using Parent = maybe-const<Const, stride_view>;                      // exposition only
    using Base = maybe-const<Const, V>;                                  // exposition only

    iterator_t<Base> current_ = iterator_t<Base>();                      // exposition only
    sentinel_t<Base> end_ = sentinel_t<Base>();                          // exposition only
    range_difference_t<Base> stride_ = 0;                                // exposition only
    range_difference_t<Base> missing_ = 0;                               // exposition only

    constexpr iterator(Parent* parent, iterator_t<Base> current,        // exposition only
                       range_difference_t<Base> missing = 0);
  public:
    using difference_type = range_difference_t<Base>;
    using value_type = range_value_t<Base>;
    using iterator_concept = see below;
    using iterator_category = see below;    // not always present

    iterator() requires default_initializable<iterator_t<Base>> = default;

    constexpr iterator(iterator<!Const> other)
      requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>
                     && convertible_to<sentinel_t<V>, sentinel_t<Base>>;

    constexpr iterator_t<Base> base() &&;
    constexpr const iterator_t<Base>& base() const & noexcept;

    constexpr decltype(auto) operator*() const { return *current_; }

    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<Base>;

    constexpr iterator& operator--() requires bidirectional_range<Base>;
    constexpr iterator operator--(int) requires bidirectional_range<Base>;

    constexpr iterator& operator+=(difference_type n) requires random_access_range<Base>;
    constexpr iterator& operator-=(difference_type n) requires random_access_range<Base>;

    constexpr decltype(auto) operator[](difference_type n) const
      requires random_access_range<Base>
    { return *(*this + n); }

    friend constexpr bool operator==(const iterator& x, default_sentinel_t);

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

    friend constexpr iterator operator+(const iterator& x, difference_type n)
      requires random_access_range<Base>;
    friend constexpr iterator operator+(difference_type n, const iterator& x)
      requires random_access_range<Base>;
    friend constexpr iterator operator-(const iterator& x, difference_type n)
      requires random_access_range<Base>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;

    friend constexpr difference_type operator-(default_sentinel_t y, const iterator& x)
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
    friend constexpr difference_type operator-(const iterator& x, default_sentinel_t y)
      requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;

    friend constexpr range_rvalue_reference_t<Base> iter_move(const iterator& i)
      noexcept(noexcept(ranges::iter_move(i.current_)));

    friend constexpr void iter_swap(const iterator& x, const iterator& y)
      noexcept(noexcept(ranges::iter_swap(x.current_, y.current_)))
      requires indirectly_swappable<iterator_t<Base>>;
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If *Base* models `random_access_range`, then `iterator_concept`
  denotes `random_access_iterator_tag`.
- Otherwise, if *Base* models `bidirectional_range`, then
  `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if *Base* models `forward_range`, then `iterator_concept`
  denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

The member *typedef-name* `iterator_category` is defined if and only if
*Base* models `forward_range`. In that case,
`iterator::iterator_category` is defined as follows:

- Let `C` denote the type
  `iterator_traits<iterator_t<Base>>::iterator_category`.
- If `C` models `derived_from<random_access_iterator_tag>`, then
  `iterator_category` denotes `random_access_iterator_tag`.
- Otherwise, `iterator_category` denotes `C`.

``` cpp
constexpr iterator(Parent* parent, iterator_t<Base> current,
                   range_difference_t<Base> missing = 0);
```

*Effects:* Initializes *current\_* with `std::move(current)`, *end\_*
with `ranges::end(parent->`*`base_`*`)`, *stride\_* with
`parent->`*`stride_`*, and *missing\_* with `missing`.

``` cpp
constexpr iterator(iterator<!Const> i)
  requires Const && convertible_to<iterator_t<V>, iterator_t<Base>>
                 && convertible_to<sentinel_t<V>, sentinel_t<Base>>;
```

*Effects:* Initializes *current\_* with `std::move(i.`*`current_`*`)`,
*end\_* with `std::move(i.`*`end_`*`)`, *stride\_* with `i.`*`stride_`*,
and *missing\_* with `i.`*`missing_`*.

``` cpp
constexpr iterator_t<Base> base() &&;
```

*Returns:* `std::move(`*`current_`*`)`.

``` cpp
constexpr const iterator_t<Base>& base() const & noexcept;
```

*Returns:* *current\_*.

``` cpp
constexpr iterator& operator++();
```

*Preconditions:* *`current_`*` != `*`end_`* is `true`.

*Effects:* Equivalent to:

``` cpp
missing_ = ranges::advance(current_, stride_, end_);
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to: `++*this;`

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
ranges::advance(current_, missing_ - stride_);
missing_ = 0;
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
constexpr iterator& operator+=(difference_type n) requires random_access_range<Base>;
```

*Preconditions:* If `n` is positive,
`ranges::distance(`*`current_`*`, `*`end_`*`) > `*`stride_`*` * (n - 1)`
is `true`.

\[*Note 1*: If `n` is negative, the *Effects* paragraph implies a
precondition. — *end note*\]

*Effects:* Equivalent to:

``` cpp
if (n > 0) {
  ranges::advance(current_, stride_ * (n - 1));
  missing_ = ranges::advance(current_, stride_, end_);
} else if (n < 0) {
  ranges::advance(current_, stride_ * n + missing_);
  missing_ = 0;
}
return *this;
```

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to: `return *this += -x;`

``` cpp
friend constexpr bool operator==(const iterator& x, default_sentinel_t);
```

*Returns:* `x.`*`current_`*` == x.`*`end_`*.

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<iterator_t<Base>>;
```

*Returns:* `x.`*`current_`*` == y.`*`current_`*.

``` cpp
friend constexpr bool operator<(const iterator& x, const iterator& y)
  requires random_access_range<Base>;
```

*Returns:* `x.`*`current_`*` < y.`*`current_`*.

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

*Returns:* `x.`*`current_`*` <=> y.`*`current_`*.

``` cpp
friend constexpr iterator operator+(const iterator& i, difference_type n)
  requires random_access_range<Base>;
friend constexpr iterator operator+(difference_type n, const iterator& i)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r += n;
return r;
```

``` cpp
friend constexpr iterator operator-(const iterator& i, difference_type n)
  requires random_access_range<Base>;
```

*Effects:* Equivalent to:

``` cpp
auto r = i;
r -= n;
return r;
```

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires sized_sentinel_for<iterator_t<Base>, iterator_t<Base>>;
```

*Returns:* Let `N` be `(x.`*`current_`*` - y.`*`current_`*`)`.

- If *Base* models `forward_range`,
  `(N + x.`*`missing_`*` - y.`*`missing_`*`) / x.`*`stride_`*.
- Otherwise, if `N` is negative, `-`*`div-ceil`*`(-N, x.`*`stride_`*`)`.
- Otherwise, *`div-ceil`*`(N, x.`*`stride_`*`)`.

``` cpp
friend constexpr difference_type operator-(default_sentinel_t y, const iterator& x)
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Returns:*
*`div-ceil`*`(x.`*`end_`*` - x.`*`current_`*`, x.`*`stride_`*`)`.

``` cpp
friend constexpr difference_type operator-(const iterator& x, default_sentinel_t y)
  requires sized_sentinel_for<sentinel_t<Base>, iterator_t<Base>>;
```

*Effects:* Equivalent to: `return -(y - x);`

``` cpp
friend constexpr range_rvalue_reference_t<Base> iter_move(const iterator& i)
  noexcept(noexcept(ranges::iter_move(i.current_)));
```

*Effects:* Equivalent to: `return ranges::iter_move(i.`*`current_`*`);`

``` cpp
friend constexpr void iter_swap(const iterator& x, const iterator& y)
  noexcept(noexcept(ranges::iter_swap(x.current_, y.current_)))
  requires indirectly_swappable<iterator_t<Base>>;
```

*Effects:* Equivalent to:
`ranges::iter_swap(x.`*`current_`*`, y.`*`current_`*`);`

### Cartesian product view <a id="range.cartesian">[[range.cartesian]]</a>

#### Overview <a id="range.cartesian.overview">[[range.cartesian.overview]]</a>

`cartesian_product_view` takes any non-zero number of ranges n and
produces a view of tuples calculated by the n-ary cartesian product of
the provided ranges.

The name `views::cartesian_product` denotes a customization point object
[[customization.point.object]]. Given a pack of subexpressions `Es`, the
expression `views::cartesian_product(Es...)` is expression-equivalent to

- `views::single(tuple())` if `Es` is an empty pack,
- otherwise,
  `cartesian_product_view<views::all_t<decltype((Es))>...>(Es...)`.

\[*Example 1*:

``` cpp
vector<int> v { 0, 1, 2 };
for (auto&& [a, b, c] : views::cartesian_product(v, v, v)) {
  cout << a << ' ' << b << ' ' << c << '\n';
}
// The above prints
// 0 0 0
// 0 0 1
// 0 0 2
// 0 1 0
// 0 1 1
// ...
```

— *end example*\]

#### Class template `cartesian_product_view` <a id="range.cartesian.view">[[range.cartesian.view]]</a>

``` cpp
namespace std::ranges {
  template<bool Const, class First, class... Vs>
  concept cartesian-product-is-random-access =          // exposition only
    (random_access_range<maybe-const<Const, First>> && ... &&
      (random_access_range<maybe-const<Const, Vs>>
        && sized_range<maybe-const<Const, Vs>>));

  template<class R>
  concept cartesian-product-common-arg =                // exposition only
    common_range<R> || (sized_range<R> && random_access_range<R>);

  template<bool Const, class First, class... Vs>
  concept cartesian-product-is-bidirectional =          // exposition only
    (bidirectional_range<maybe-const<Const, First>> && ... &&
      (bidirectional_range<maybe-const<Const, Vs>>
        && cartesian-product-common-arg<maybe-const<Const, Vs>>));

  template<class First, class... Vs>
  concept cartesian-product-is-common =                 // exposition only
    cartesian-product-common-arg<First>;

  template<class... Vs>
  concept cartesian-product-is-sized =                  // exposition only
    (sized_range<Vs> && ...);

  template<bool Const, template<class> class FirstSent, class First, class... Vs>
    concept cartesian-is-sized-sentinel =               // exposition only
      (sized_sentinel_for<FirstSent<maybe-const<Const, First>>,
          iterator_t<maybe-const<Const, First>>> && ...
        && (sized_range<maybe-const<Const, Vs>>
          && sized_sentinel_for<iterator_t<maybe-const<Const, Vs>>,
              iterator_t<maybe-const<Const, Vs>>>));

  template<cartesian-product-common-arg R>
  constexpr auto cartesian-common-arg-end(R& r) {       // exposition only
    if constexpr (common_range<R>) {
      return ranges::end(r);
    } else {
      return ranges::begin(r) + ranges::distance(r);
    }
  }

  template<input_range First, forward_range... Vs>
    requires (view<First> && ... && view<Vs>)
  class cartesian_product_view : public view_interface<cartesian_product_view<First, Vs...>> {
  private:
    tuple<First, Vs...> bases_;                 // exposition only
    // [range.cartesian.iterator], class template cartesian_product_view::iterator
    template<bool Const> class iterator;       // exposition only

  public:
    constexpr cartesian_product_view() = default;
    constexpr explicit cartesian_product_view(First first_base, Vs... bases);

    constexpr iterator<false> begin()
      requires (!simple-view<First> || ... || !simple-view<Vs>);
    constexpr iterator<true> begin() const
      requires (range<const First> && ... && range<const Vs>);

    constexpr iterator<false> end()
      requires ((!simple-view<First> || ... || !simple-view<Vs>) &&
        cartesian-product-is-common<First, Vs...>);
    constexpr iterator<true> end() const
      requires cartesian-product-is-common<const First, const Vs...>;
    constexpr default_sentinel_t end() const noexcept;

    constexpr see below size()
      requires cartesian-product-is-sized<First, Vs...>;
    constexpr see below size() const
      requires cartesian-product-is-sized<const First, const Vs...>;
  };

  template<class... Vs>
    cartesian_product_view(Vs&&...) -> cartesian_product_view<views::all_t<Vs>...>;
}
```

``` cpp
constexpr explicit cartesian_product_view(First first_base, Vs... bases);
```

*Effects:* Initializes *bases\_* with
`std::move(first_base), std::move(bases)...`.

``` cpp
constexpr iterator<false> begin()
  requires (!simple-view<First> || ... || !simple-view<Vs>);
```

*Effects:* Equivalent to:

``` cpp
return iterator<false>(*this, tuple-transform(ranges::begin, bases_));
```

``` cpp
constexpr iterator<true> begin() const
  requires (range<const First> && ... && range<const Vs>);
```

*Effects:* Equivalent to:

``` cpp
return iterator<true>(*this, tuple-transform(ranges::begin, bases_));
```

``` cpp
constexpr iterator<false> end()
  requires ((!simple-view<First> || ... || !simple-view<Vs>)
    && cartesian-product-is-common<First, Vs...>);
constexpr iterator<true> end() const
  requires cartesian-product-is-common<const First, const Vs...>;
```

Let:

- *is-const* be `true` for the const-qualified overload, and `false`
  otherwise;
- *is-empty* be `true` if the expression `ranges::empty(rng)` is `true`
  for any `rng` among the underlying ranges except the first one and
  `false` otherwise; and
- *`begin-or-first-end`*`(rng)` be expression-equivalent to
  *`is-empty`*` ? ranges::begin(rng) : `*`cartesian-common-arg-end`*`(rng)`
  if `rng` is the first underlying range and `ranges::begin(rng)`
  otherwise.

*Effects:* Equivalent to:

``` cpp
iterator<is-const> it(*this, tuple-transform(
  [](auto& rng){ return begin-or-first-end(rng); }, bases_));
return it;
```

``` cpp
constexpr default_sentinel_t end() const noexcept;
```

*Returns:* `default_sentinel`.

``` cpp
constexpr see below size()
  requires cartesian-product-is-sized<First, Vs...>;
constexpr see below size() const
  requires cartesian-product-is-sized<const First, const Vs...>;
```

The return type is an *implementation-defined* unsigned-integer-like
type.

*Recommended practice:* The return type should be the smallest
unsigned-integer-like type that is sufficiently wide to store the
product of the maximum sizes of all the underlying ranges, if such a
type exists.

Let p be the product of the sizes of all the ranges in *bases\_*.

*Preconditions:* p can be represented by the return type.

*Returns:* p.

#### Class template `cartesian_product_view::iterator` <a id="range.cartesian.iterator">[[range.cartesian.iterator]]</a>

``` cpp
namespace std::ranges {
  template<input_range First, forward_range... Vs>
    requires (view<First> && ... && view<Vs>)
  template<bool Const>
  class cartesian_product_view<First, Vs...>::iterator {
  public:
    using iterator_category = input_iterator_tag;
    using iterator_concept  = see below;
    using value_type = tuple<range_value_t<maybe-const<Const, First>>,
      range_value_t<maybe-const<Const, Vs>>...>;
    using reference = tuple<range_reference_t<maybe-const<Const, First>>,
      range_reference_t<maybe-const<Const, Vs>>...>;
    using difference_type = see below;

    iterator() = default;

    constexpr iterator(iterator<!Const> i) requires Const &&
      (convertible_to<iterator_t<First>, iterator_t<const First>> &&
        ... && convertible_to<iterator_t<Vs>, iterator_t<const Vs>>);

    constexpr auto operator*() const;
    constexpr iterator& operator++();
    constexpr void operator++(int);
    constexpr iterator operator++(int) requires forward_range<maybe-const<Const, First>>;

    constexpr iterator& operator--()
      requires cartesian-product-is-bidirectional<Const, First, Vs...>;
    constexpr iterator operator--(int)
      requires cartesian-product-is-bidirectional<Const, First, Vs...>;

    constexpr iterator& operator+=(difference_type x)
      requires cartesian-product-is-random-access<Const, First, Vs...>;
    constexpr iterator& operator-=(difference_type x)
      requires cartesian-product-is-random-access<Const, First, Vs...>;

    constexpr reference operator[](difference_type n) const
      requires cartesian-product-is-random-access<Const, First, Vs...>;

    friend constexpr bool operator==(const iterator& x, const iterator& y)
      requires equality_comparable<iterator_t<maybe-const<Const, First>>>;

    friend constexpr bool operator==(const iterator& x, default_sentinel_t);

    friend constexpr auto operator<=>(const iterator& x, const iterator& y)
      requires all-random-access<Const, First, Vs...>;

    friend constexpr iterator operator+(const iterator& x, difference_type y)
      requires cartesian-product-is-random-access<Const, First, Vs...>;
    friend constexpr iterator operator+(difference_type x, const iterator& y)
      requires cartesian-product-is-random-access<Const, First, Vs...>;
    friend constexpr iterator operator-(const iterator& x, difference_type y)
      requires cartesian-product-is-random-access<Const, First, Vs...>;
    friend constexpr difference_type operator-(const iterator& x, const iterator& y)
      requires cartesian-is-sized-sentinel<Const, iterator_t, First, Vs...>;

    friend constexpr difference_type operator-(const iterator& i, default_sentinel_t)
      requires cartesian-is-sized-sentinel<Const, sentinel_t, First, Vs...>;
    friend constexpr difference_type operator-(default_sentinel_t, const iterator& i)
      requires cartesian-is-sized-sentinel<Const, sentinel_t, First, Vs...>;

    friend constexpr auto iter_move(const iterator& i) noexcept(see below);

    friend constexpr void iter_swap(const iterator& l, const iterator& r) noexcept(see below)
      requires (indirectly_swappable<iterator_t<maybe-const<Const, First>>> && ... &&
        indirectly_swappable<iterator_t<maybe-const<Const, Vs>>>);

  private:
    using Parent = maybe-const<Const, cartesian_product_view>;          // exposition only
    Parent* parent_ = nullptr;                                          // exposition only
    tuple<iterator_t<maybe-const<Const, First>>,
      iterator_t<maybe-const<Const, Vs>>...> current_;                  // exposition only

    template<size_t N = sizeof...(Vs)>
      constexpr void next();                                            // exposition only

    template<size_t N = sizeof...(Vs)>
      constexpr void prev();                                            // exposition only

    template<class Tuple>
      constexpr difference_type distance-from(const Tuple& t) const;    // exposition only

    constexpr iterator(Parent& parent, tuple<iterator_t<maybe-const<Const, First>>,
      iterator_t<maybe-const<Const, Vs>>...> current);                  // exposition only
  };
}
```

`iterator::iterator_concept` is defined as follows:

- If `cartesian-product-is-random-access<Const, First, Vs...>` is
  modeled, then `iterator_concept` denotes `random_access_iterator_tag`.
- Otherwise, if
  `cartesian-product-is-bidirectional<Const, First, Vs...>` is modeled,
  then `iterator_concept` denotes `bidirectional_iterator_tag`.
- Otherwise, if `maybe-const<Const, First>` models `forward_range`, then
  `iterator_concept` denotes `forward_iterator_tag`.
- Otherwise, `iterator_concept` denotes `input_iterator_tag`.

`iterator::difference_type` is an *implementation-defined*
signed-integer-like type.

*Recommended practice:* `iterator::difference_type` should be the
smallest signed-integer-like type that is sufficiently wide to store the
product of the maximum sizes of all underlying ranges if such a type
exists.

``` cpp
template<size_t N = sizeof...(Vs)>
  constexpr void next();
```

*Effects:* Equivalent to:

``` cpp
auto& it = std::get<N>(current_);
++it;
if constexpr (N > 0) {
  if (it == ranges::end(std::get<N>(parent_->bases_))) {
    it = ranges::begin(std::get<N>(parent_->bases_));
    next<N - 1>();
  }
}
```

``` cpp
template<size_t N = sizeof...(Vs)>
  constexpr void prev();
```

*Effects:* Equivalent to:

``` cpp
auto& it = std::get<N>(current_);
if constexpr (N > 0) {
  if (it == ranges::begin(std::get<N>(parent_->bases_))) {
    it = cartesian-common-arg-end(std::get<N>(parent_->bases_));
    prev<N - 1>();
  }
}
--it;
```

``` cpp
template<class Tuple>
  constexpr difference_type distance-from(const Tuple& t) const;
```

Let:

- $\textit{scaled-size}(N)$ be the product of
  `static_cast<difference_type>(ranges::size(std::get<`N`>(`*`parent_`*`->`*`bases_`*`)))`
  and $\textit{scaled-size}(N+1)$ if N \le `sizeof...(Vs)`, otherwise
  `static_cast<difference_type>(1)`;
- $\textit{scaled-distance}(N)$ be the product of
  `static_cast<difference_type>(std::get<`N`>(`*`cur``rent_`*`) - std::get<`N`>(t))`
  and $\textit{scaled-size}(N+1)$; and
- *scaled-sum* be the sum of $\textit{scaled-distance}(N)$ for every
  integer 0 \le N \le `sizeof...(Vs)`.

*Preconditions:* *scaled-sum* can be represented by `difference_type`.

*Returns:* *scaled-sum*.

``` cpp
constexpr iterator(Parent& parent, tuple<iterator_t<maybe-const<Const, First>>,
  iterator_t<maybe-const<Const, Vs>>...> current);
```

*Effects:* Initializes *parent\_* with `addressof(parent)` and
*current\_* with `std::move(current)`.

``` cpp
constexpr iterator(iterator<!Const> i) requires Const &&
  (convertible_to<iterator_t<First>, iterator_t<const First>> &&
    ... && convertible_to<iterator_t<Vs>, iterator_t<const Vs>>);
```

*Effects:* Initializes *parent\_* with `i.`*`parent_`* and *current\_*
with `std::move(i.`*`current_`*`)`.

``` cpp
constexpr auto operator*() const;
```

*Effects:* Equivalent to:

``` cpp
return tuple-transform([](auto& i) -> decltype(auto) { return *i; }, current_);
```

``` cpp
constexpr iterator& operator++();
```

*Effects:* Equivalent to:

``` cpp
next();
return *this;
```

``` cpp
constexpr void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
constexpr iterator operator++(int) requires forward_range<maybe-const<Const, First>>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
++*this;
return tmp;
```

``` cpp
constexpr iterator& operator--()
  requires cartesian-product-is-bidirectional<Const, First, Vs...>;
```

*Effects:* Equivalent to:

``` cpp
prev();
return *this;
```

``` cpp
constexpr iterator operator--(int)
  requires cartesian-product-is-bidirectional<Const, First, Vs...>;
```

*Effects:* Equivalent to:

``` cpp
auto tmp = *this;
--*this;
return tmp;
```

``` cpp
constexpr iterator& operator+=(difference_type x)
  requires cartesian-product-is-random-access<Const, First, Vs...>;
```

Let `orig` be the value of `*this` before the call.

Let `ret` be:

- If `x > 0`, the value of `*this` had *next* been called `x` times.
- Otherwise, if `x < 0`, the value of `*this` had *prev* been called
  `-x` times.
- Otherwise, `orig`.

*Preconditions:* `x` is in the range
[`ranges::distance(*this, ranges::begin(*\textit{parent_}))`,
`ranges::distance(*this, ranges::end(*\textit{parent_}))`].

*Effects:* Sets the value of `*this` to `ret`.

*Returns:* `*this`.

*Complexity:* Constant.

``` cpp
constexpr iterator& operator-=(difference_type x)
  requires cartesian-product-is-random-access<Const, First, Vs...>;
```

*Effects:* Equivalent to:

``` cpp
*this += -x;
return *this;
```

``` cpp
constexpr reference operator[](difference_type n) const
  requires cartesian-product-is-random-access<Const, First, Vs...>;
```

*Effects:* Equivalent to: `return *((*this) + n);`

``` cpp
friend constexpr bool operator==(const iterator& x, const iterator& y)
  requires equality_comparable<iterator_t<maybe-const<Const, First>>>;
```

*Effects:* Equivalent to: `return x.`*`current_`*` == y.`*`current_`*`;`

``` cpp
friend constexpr bool operator==(const iterator& x, default_sentinel_t);
```

*Returns:* `true` if
`std::get<`i`>(x.`*`current_`*`) == ranges::end(std::get<`i`>(x.`*`parent_`*`->`*`bases_`*`))`
is `true` for any integer 0 \le i \le `sizeof...(Vs)`; otherwise,
`false`.

``` cpp
friend constexpr auto operator<=>(const iterator& x, const iterator& y)
  requires all-random-access<Const, First, Vs...>;
```

*Effects:* Equivalent to:
`return x.`*`current_`*` <=> y.`*`current_`*`;`

``` cpp
friend constexpr iterator operator+(const iterator& x, difference_type y)
  requires cartesian-product-is-random-access<Const, First, Vs...>;
```

*Effects:* Equivalent to: `return `*`iterator`*`(x) += y;`

``` cpp
friend constexpr iterator operator+(difference_type x, const iterator& y)
  requires cartesian-product-is-random-access<Const, First, Vs...>;
```

*Effects:* Equivalent to: `return y + x;`

``` cpp
friend constexpr iterator operator-(const iterator& x, difference_type y)
  requires cartesian-product-is-random-access<Const, First, Vs...>;
```

*Effects:* Equivalent to: `return `*`iterator`*`(x) -= y;`

``` cpp
friend constexpr difference_type operator-(const iterator& x, const iterator& y)
  requires cartesian-is-sized-sentinel<Const, iterator_t, First, Vs...>;
```

*Effects:* Equivalent to:
`return x.`*`distance-from`*`(y.`*`current_`*`);`

``` cpp
friend constexpr difference_type operator-(const iterator& i, default_sentinel_t)
  requires cartesian-is-sized-sentinel<Const, sentinel_t, First, Vs...>;
```

Let *end-tuple* be an object of a type that is a specialization of
`tuple`, such that:

- `std::get<0>(`*`end-tuple`*`)` has the same value as
  `ranges::end(std::get<0>(i.`*`parent_`*`->`*`ba``ses_`*`))`;
- `std::get<`N`>(`*`end-tuple`*`)` has the same value as
  `ranges::begin(std::get<`N`>(i.`*`parent_`*`->`*`bases_`*`))` for
  every integer 1 \le N \le `sizeof...(Vs)`.

*Effects:* Equivalent to:
`return i.`*`distance-from`*`(`*`end-tuple`*`);`

``` cpp
friend constexpr difference_type operator-(default_sentinel_t s, const iterator& i)
  requires cartesian-is-sized-sentinel<Const, sentinel_t, First, Vs...>;
```

*Effects:* Equivalent to: `return -(i - s);`

``` cpp
friend constexpr auto iter_move(const iterator& i) noexcept(see below);
```

*Effects:* Equivalent to:
`return `*`tuple-transform`*`(ranges::iter_move, i.`*`current_`*`);`

*Remarks:* The exception specification is equivalent to the logical of
the following expressions:

- `noexcept(ranges::iter_move(std::get<`N`>(i.`*`current_`*`)))` for
  every integer0 \le N \le `sizeof...(Vs)`,
- `is_nothrow_move_constructible_v<range_rvalue_reference_t<`*`maybe-const`*`<Const, T>>>`
  for every type `T` in `First, Vs...`.

``` cpp
friend constexpr void iter_swap(const iterator& l, const iterator& r) noexcept(see below)
  requires (indirectly_swappable<iterator_t<maybe-const<Const, First>>> && ... &&
        indirectly_swappable<iterator_t<maybe-const<Const, Vs>>>);
```

*Effects:* For every integer 0 \le i \le `sizeof...(Vs)`, performs:

``` cpp
ranges::iter_swap(std::get<$i$>(l.current_), std::get<$i$>(r.current_))
```

*Remarks:* The exception specification is equivalent to the logical of
the following expressions:

- `noexcept(ranges::iter_swap(std::get<`i`>(l.`*`current_`*`), std::get<`i`>(r.`*`current_`*`)))`
  forevery integer 0 \le i \le `sizeof...(Vs)`.

## Range generators <a id="coro.generator">[[coro.generator]]</a>

### Overview <a id="coroutine.generator.overview">[[coroutine.generator.overview]]</a>

Class template `generator` presents a view of the elements yielded by
the evaluation of a coroutine.

A `generator` generates a sequence of elements by repeatedly resuming
the coroutine from which it was returned. Elements of the sequence are
produced by the coroutine each time a `co_yield` statement is evaluated.
When the `co_yield` statement is of the form `co_yield elements_of(r)`,
each element of the range `r` is successively produced as an element of
the sequence.

\[*Example 1*:

``` cpp
generator<int> ints(int start = 0) {
  while (true)
    co_yield start++;
}

void f() {
  for (auto i : ints() | views::take(3))
    cout << i << ' ';       // prints 0 1 2
}
```

— *end example*\]

### Header `<generator>` synopsis <a id="generator.syn">[[generator.syn]]</a>

``` cpp
namespace std {
  // [coro.generator.class], class template generator
  template<class Ref, class V = void, class Allocator = void>
    class generator;

  namespace pmr {
    template<class R, class V = void>
      using generator = std::generator<R, V, polymorphic_allocator<>>;
  }
}
```

### Class template `generator` <a id="coro.generator.class">[[coro.generator.class]]</a>

``` cpp
namespace std {
  template<class Ref, class V = void, class Allocator = void>
  class generator : public ranges::view_interface<generator<Ref, V, Allocator>> {
  private:
    using value = conditional_t<is_void_v<V>, remove_cvref_t<Ref>, V>;  // exposition only
    using reference = conditional_t<is_void_v<V>, Ref&&, Ref>;          // exposition only

    // [coro.generator.iterator], class generator::iterator
    class iterator;                                                     // exposition only

  public:
    using yielded =
      conditional_t<is_reference_v<reference>, reference, const reference&>;

    // [coro.generator.promise], class generator::promise_type
    class promise_type;

    generator(const generator&) = delete;
    generator(generator&& other) noexcept;

    ~generator();

    generator& operator=(generator other) noexcept;

    iterator begin();
    default_sentinel_t end() const noexcept;

  private:
    coroutine_handle<promise_type> coroutine_ = nullptr;  // exposition only
    unique_ptr<stack<coroutine_handle<>>> active_;        // exposition only
  };
}
```

*Mandates:*

- If `Allocator` is not `void`, `allocator_traits<Allocator>::pointer`
  is a pointer type.
- *value* is a cv-unqualified object type.
- *reference* is either a reference type, or a cv-unqualified object
  type that models `copy_constructible`.
- Let `RRef` denote `remove_reference_t<reference>&&` if *reference* is
  a reference type, and *reference* otherwise. Each of:
  - `common_reference_with<reference&&, value&>`,
  - `common_reference_with<reference&&, RRef&&>`, and
  - `\texttt{common_reference_with}<RRef&&, const \textit{value}&>`

  is modeled.
  \[*Note 4*: These requirements ensure the exposition-only *iterator*
  type can model `indirectly_readable` and thus
  `input_iterator`. — *end note*\]

If `Allocator` is not `void`, it shall meet the *Cpp17Allocator*
requirements.

Specializations of `generator` model `view` and `input_range`.

The behavior of a program that adds a specialization for `generator` is
undefined.

### Members <a id="coro.generator.members">[[coro.generator.members]]</a>

``` cpp
generator(generator&& other) noexcept;
```

*Effects:* Initializes *coroutine\_* with
`exchange(other.`*`coroutine_`*`, {})` and *active\_* with
`exchange(other.active_, nullptr)`.

\[*Note 1*: Iterators previously obtained from `other` are not
invalidated; they become iterators into `*this`. — *end note*\]

``` cpp
~generator();
```

*Effects:* Equivalent to:

``` cpp
if (coroutine_) {
  coroutine_.destroy();
}
```

\[*Note 2*: Ownership of recursively yielded generators is held in
awaitable objects in the coroutine frame of the yielding generator, so
destroying the root generator effectively destroys the entire stack of
yielded generators. — *end note*\]

``` cpp
generator& operator=(generator other) noexcept;
```

*Effects:* Equivalent to:

``` cpp
swap(coroutine_, other.coroutine_);
swap(active_, other.active_);
```

*Returns:* `*this`.

\[*Note 3*: Iterators previously obtained from `other` are not
invalidated; they become iterators into `*this`. — *end note*\]

``` cpp
iterator begin();
```

*Preconditions:* *coroutine\_* refers to a coroutine suspended at its
initial suspend point [[dcl.fct.def.coroutine]].

*Effects:* Pushes *coroutine\_* into `*`*`active_`*, then evaluates
*`coroutine_`*`.resume()`.

*Returns:* An *iterator* object whose member *coroutine\_* refers to the
same coroutine as does *coroutine\_*.

\[*Note 4*: A program that calls `begin` more than once on the same
generator has undefined behavior. — *end note*\]

``` cpp
default_sentinel_t end() const noexcept;
```

*Returns:* `default_sentinel`.

### Class `generator::promise_type` <a id="coro.generator.promise">[[coro.generator.promise]]</a>

``` cpp
namespace std {
  template<class Ref, class V, class Allocator>
  class generator<Ref, V, Allocator>::promise_type {
  public:
    generator get_return_object() noexcept;

    suspend_always initial_suspend() const noexcept { return {}; }
    auto final_suspend() noexcept;

    suspend_always yield_value(yielded val) noexcept;

    auto yield_value(const remove_reference_t<yielded>& lval)
      requires is_rvalue_reference_v<yielded> &&
        constructible_from<remove_cvref_t<yielded>, const remove_reference_t<yielded>&>;

    template<class R2, class V2, class Alloc2, class Unused>
      requires same_as<typename generator<R2, V2, Alloc2>::yielded, yielded>
        auto yield_value(ranges::elements_of<generator<R2, V2, Alloc2>&&, Unused> g) noexcept;

    template<ranges::input_range R, class Alloc>
      requires convertible_to<ranges::range_reference_t<R>, yielded>
        auto yield_value(ranges::elements_of<R, Alloc> r) noexcept;

    void await_transform() = delete;

    void return_void() const noexcept {}
    void unhandled_exception();

    void* operator new(size_t size)
      requires same_as<Allocator, void> || default_initializable<Allocator>;

    template<class Alloc, class... Args>
      requires same_as<Allocator, void> || convertible_to<const Alloc&, Allocator>
        void* operator new(size_t size, allocator_arg_t, const Alloc& alloc, const Args&...);

    template<class This, class Alloc, class... Args>
      requires same_as<Allocator, void> || convertible_to<const Alloc&, Allocator>
        void* operator new(size_t size, const This&, allocator_arg_t, const Alloc& alloc,
                           const Args&...);

    void operator delete(void* pointer, size_t size) noexcept;

  private:
    add_pointer_t<yielded> value_ = nullptr;    // exposition only
    exception_ptr except_;                      // exposition only
  };
}
```

``` cpp
generator get_return_object() noexcept;
```

*Returns:* A `generator` object whose member *coroutine\_* is
`coroutine_handle<promise_type>::from_promise(*this)`, and whose member
*active\_* points to an empty stack.

``` cpp
auto final_suspend() noexcept;
```

*Preconditions:* A handle referring to the coroutine whose promise
object is `*this` is at the top of `*`*`active_`* of some `generator`
object `x`. This function is called by that coroutine upon reaching its
final suspend point [[dcl.fct.def.coroutine]].

*Returns:* An awaitable object of unspecified type [[expr.await]] whose
member functions arrange for the calling coroutine to be suspended, pop
the coroutine handle from the top of `*x.`*`active_`*, and resume
execution of the coroutine referred to by `x.`*`active_`*`->top()` if
`*x.`*`active_`* is not empty. If it is empty, control flow returns to
the current coroutine caller or resumer [[dcl.fct.def.coroutine]].

``` cpp
suspend_always yield_value(yielded val) noexcept;
```

*Effects:* Equivalent to *`value_`*` = addressof(val)`.

*Returns:* `{}`.

``` cpp
auto yield_value(const remove_reference_t<yielded>& lval)
  requires is_rvalue_reference_v<yielded> &&
    constructible_from<remove_cvref_t<yielded>, const remove_reference_t<yielded>&>;
```

*Preconditions:* A handle referring to the coroutine whose promise
object is `*this` is at the top of `*`*`active_`* of some `generator`
object.

*Returns:* An awaitable object of an unspecified type [[expr.await]]
that stores an object of type `remove_cvref_t<yielded>`
direct-non-list-initialized with `lval`, whose member functions arrange
for *value\_* to point to that stored object and then suspend the
coroutine.

*Throws:* Any exception thrown by the initialization of the stored
object.

*Remarks:* A *yield-expression* that calls this function has type
`void`[[expr.yield]].

``` cpp
template<class R2, class V2, class Alloc2, class Unused>
  requires same_as<typename generator<R2, V2, Alloc2>::yielded, yielded>
  auto yield_value(ranges::elements_of<generator<R2, V2, Alloc2>&&, Unused> g) noexcept;
```

*Preconditions:* A handle referring to the coroutine whose promise
object is `*this` is at the top of `*`*`active_`* of some `generator`
object `x`. The coroutine referred to by `g.range.`*`coroutine_`* is
suspended at its initial suspend point.

*Returns:* An awaitable object of an unspecified type [[expr.await]]
into which `g.range` is moved, whose member `await_ready` returns
`false`, whose member `await_suspend` pushes
`g.range.`\textit{coroutine\_} into `*x.`*`active_`* and resumes
execution of the coroutine referred to by `g.range.`*`coroutine_`*, and
whose member `await_resume` evaluates `rethrow_exception(`*`except_`*`)`
if `bool(`*`ex``cept_`*`)` is `true`. If `bool(`*`except_`*`)` is
`false`, the `await_resume` member has no effects.

*Remarks:* A *yield-expression* that calls this function has type
`void`[[expr.yield]].

``` cpp
template<ranges::input_range R, class Alloc>
  requires convertible_to<ranges::range_reference_t<R>, yielded>
  auto yield_value(ranges::elements_of<R, Alloc> r) noexcept;
```

*Effects:* Equivalent to:

``` cpp
auto nested = [](allocator_arg_t, Alloc, ranges::iterator_t<R> i, ranges::sentinel_t<R> s)
  -> generator<yielded, ranges::range_value_t<R>, Alloc> {
    for (; i != s; ++i) {
      co_yield static_cast<yielded>(*i);
    }
  };
return yield_value(ranges::elements_of(nested(
  allocator_arg, r.allocator, ranges::begin(r.range), ranges::end(r.range))));
```

\[*Note 1*: A *yield-expression* that calls this function has type
`void`[[expr.yield]]. — *end note*\]

``` cpp
void unhandled_exception();
```

*Preconditions:* A handle referring to the coroutine whose promise
object is `*this` is at the top of `*`*`active_`* of some `generator`
object `x`.

*Effects:* If the handle referring to the coroutine whose promise object
is `*this` is the sole element of `*x.`*`active_`*, equivalent to
`throw`, otherwise, assigns `current_exception()` to *except\_*.

``` cpp
void* operator new(size_t size)
  requires same_as<Allocator, void> || default_initializable<Allocator>;

template<class Alloc, class... Args>
  requires same_as<Allocator, void> || convertible_to<const Alloc&, Allocator>
  void* operator new(size_t size, allocator_arg_t, const Alloc& alloc, const Args&...);

template<class This, class Alloc, class... Args>
  requires same_as<Allocator, void> || convertible_to<const Alloc&, Allocator>
  void* operator new(size_t size, const This&, allocator_arg_t, const Alloc& alloc,
                     const Args&...);
```

Let `A` be

- `Allocator`, if it is not `void`,
- `Alloc` for the overloads with a template parameter `Alloc`, or
- `allocator<void>` otherwise.

Let `B` be `allocator_traits<A>::template rebind_alloc<U>` where `U` is
an unspecified type whose size and alignment are both
\_\_STDCPP_DEFAULT_NEW_ALIGNMENT\_\_.

*Mandates:* `allocator_traits<B>::pointer` is a pointer type.

*Effects:* Initializes an allocator `b` of type `B` with `A(alloc)`, for
the overloads with a function parameter `alloc`, and with `A()`
otherwise. Uses `b` to allocate storage for the smallest array of `U`
sufficient to provide storage for a coroutine state of size `size`, and
unspecified additional state necessary to ensure that `operator delete`
can later deallocate this memory block with an allocator equal to `b`.

*Returns:* A pointer to the allocated storage.

``` cpp
void operator delete(void* pointer, size_t size) noexcept;
```

*Preconditions:* `pointer` was returned from an invocation of one of the
above overloads of `operator new` with a `size` argument equal to
`size`.

*Effects:* Deallocates the storage pointed to by `pointer` using an
allocator equivalent to that used to allocate it.

### Class `generator::iterator` <a id="coro.generator.iterator">[[coro.generator.iterator]]</a>

``` cpp
namespace std {
  template<class Ref, class V, class Allocator>
  class generator<Ref, V, Allocator>::iterator {
  public:
    using value_type = value;
    using difference_type = ptrdiff_t;

    iterator(iterator&& other) noexcept;
    iterator& operator=(iterator&& other) noexcept;

    reference operator*() const noexcept(is_nothrow_copy_constructible_v<reference>);
    iterator& operator++();
    void operator++(int);

    friend bool operator==(const iterator& i, default_sentinel_t);

  private:
    coroutine_handle<promise_type> coroutine_; // exposition only
  };
}
```

``` cpp
iterator(iterator&& other) noexcept;
```

*Effects:* Initializes *coroutine\_* with
`exchange(other.`*`coroutine_`*`, {})`.

``` cpp
iterator& operator=(iterator&& other) noexcept;
```

*Effects:* Equivalent to
*`coroutine_`*` = exchange(other.`*`coroutine_`*`, {})`.

*Returns:* `*this`.

``` cpp
reference operator*() const noexcept(is_nothrow_copy_constructible_v<reference>);
```

*Preconditions:* For some `generator` object `x`, *coroutine\_* is in
`*x.`*`active_`* and `x.`*`active_`*`->top()` refers to a suspended
coroutine with promise object `p`.

*Effects:* Equivalent to:
`return static_cast<`*`reference`*`>(*p.`*`value_`*`);`

``` cpp
iterator& operator++();
```

*Preconditions:* For some `generator` object `x`, *coroutine\_* is in
`*x.`*`active_`*.

*Effects:* Equivalent to `x.`*`active_`*`->top().resume()`.

*Returns:* `*this`.

``` cpp
void operator++(int);
```

*Effects:* Equivalent to `++*this`.

``` cpp
friend bool operator==(const iterator& i, default_sentinel_t);
```

*Effects:* Equivalent to: `return i.`*`coroutine_`*`.done();`

<!-- Section link definitions -->
[coro.generator]: #coro.generator
[coro.generator.class]: #coro.generator.class
[coro.generator.iterator]: #coro.generator.iterator
[coro.generator.members]: #coro.generator.members
[coro.generator.promise]: #coro.generator.promise
[coroutine.generator.overview]: #coroutine.generator.overview
[generator.syn]: #generator.syn
[range.access]: #range.access
[range.access.begin]: #range.access.begin
[range.access.cbegin]: #range.access.cbegin
[range.access.cend]: #range.access.cend
[range.access.crbegin]: #range.access.crbegin
[range.access.crend]: #range.access.crend
[range.access.end]: #range.access.end
[range.access.general]: #range.access.general
[range.access.rbegin]: #range.access.rbegin
[range.access.rend]: #range.access.rend
[range.adaptor.helpers]: #range.adaptor.helpers
[range.adaptor.object]: #range.adaptor.object
[range.adaptors]: #range.adaptors
[range.adaptors.general]: #range.adaptors.general
[range.adjacent]: #range.adjacent
[range.adjacent.iterator]: #range.adjacent.iterator
[range.adjacent.overview]: #range.adjacent.overview
[range.adjacent.sentinel]: #range.adjacent.sentinel
[range.adjacent.transform]: #range.adjacent.transform
[range.adjacent.transform.iterator]: #range.adjacent.transform.iterator
[range.adjacent.transform.overview]: #range.adjacent.transform.overview
[range.adjacent.transform.sentinel]: #range.adjacent.transform.sentinel
[range.adjacent.transform.view]: #range.adjacent.transform.view
[range.adjacent.view]: #range.adjacent.view
[range.all]: #range.all
[range.all.general]: #range.all.general
[range.as.const]: #range.as.const
[range.as.const.overview]: #range.as.const.overview
[range.as.const.view]: #range.as.const.view
[range.as.rvalue]: #range.as.rvalue
[range.as.rvalue.overview]: #range.as.rvalue.overview
[range.as.rvalue.view]: #range.as.rvalue.view
[range.cartesian]: #range.cartesian
[range.cartesian.iterator]: #range.cartesian.iterator
[range.cartesian.overview]: #range.cartesian.overview
[range.cartesian.view]: #range.cartesian.view
[range.chunk]: #range.chunk
[range.chunk.by]: #range.chunk.by
[range.chunk.by.iter]: #range.chunk.by.iter
[range.chunk.by.overview]: #range.chunk.by.overview
[range.chunk.by.view]: #range.chunk.by.view
[range.chunk.fwd.iter]: #range.chunk.fwd.iter
[range.chunk.inner.iter]: #range.chunk.inner.iter
[range.chunk.outer.iter]: #range.chunk.outer.iter
[range.chunk.outer.value]: #range.chunk.outer.value
[range.chunk.overview]: #range.chunk.overview
[range.chunk.view.fwd]: #range.chunk.view.fwd
[range.chunk.view.input]: #range.chunk.view.input
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
[range.elementsof]: #range.elementsof
[range.empty]: #range.empty
[range.empty.overview]: #range.empty.overview
[range.empty.view]: #range.empty.view
[range.enumerate]: #range.enumerate
[range.enumerate.iterator]: #range.enumerate.iterator
[range.enumerate.overview]: #range.enumerate.overview
[range.enumerate.sentinel]: #range.enumerate.sentinel
[range.enumerate.view]: #range.enumerate.view
[range.factories]: #range.factories
[range.factories.general]: #range.factories.general
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
[range.join.with]: #range.join.with
[range.join.with.iterator]: #range.join.with.iterator
[range.join.with.overview]: #range.join.with.overview
[range.join.with.sentinel]: #range.join.with.sentinel
[range.join.with.view]: #range.join.with.view
[range.lazy.split]: #range.lazy.split
[range.lazy.split.inner]: #range.lazy.split.inner
[range.lazy.split.outer]: #range.lazy.split.outer
[range.lazy.split.outer.value]: #range.lazy.split.outer.value
[range.lazy.split.overview]: #range.lazy.split.overview
[range.lazy.split.view]: #range.lazy.split.view
[range.move.wrap]: #range.move.wrap
[range.nonprop.cache]: #range.nonprop.cache
[range.owning.view]: #range.owning.view
[range.prim.cdata]: #range.prim.cdata
[range.prim.data]: #range.prim.data
[range.prim.empty]: #range.prim.empty
[range.prim.size]: #range.prim.size
[range.prim.ssize]: #range.prim.ssize
[range.range]: #range.range
[range.ref.view]: #range.ref.view
[range.refinements]: #range.refinements
[range.repeat]: #range.repeat
[range.repeat.iterator]: #range.repeat.iterator
[range.repeat.overview]: #range.repeat.overview
[range.repeat.view]: #range.repeat.view
[range.req]: #range.req
[range.req.general]: #range.req.general
[range.reverse]: #range.reverse
[range.reverse.overview]: #range.reverse.overview
[range.reverse.view]: #range.reverse.view
[range.single]: #range.single
[range.single.overview]: #range.single.overview
[range.single.view]: #range.single.view
[range.sized]: #range.sized
[range.slide]: #range.slide
[range.slide.iterator]: #range.slide.iterator
[range.slide.overview]: #range.slide.overview
[range.slide.sentinel]: #range.slide.sentinel
[range.slide.view]: #range.slide.view
[range.split]: #range.split
[range.split.iterator]: #range.split.iterator
[range.split.overview]: #range.split.overview
[range.split.sentinel]: #range.split.sentinel
[range.split.view]: #range.split.view
[range.stride]: #range.stride
[range.stride.iterator]: #range.stride.iterator
[range.stride.overview]: #range.stride.overview
[range.stride.view]: #range.stride.view
[range.subrange]: #range.subrange
[range.subrange.access]: #range.subrange.access
[range.subrange.ctor]: #range.subrange.ctor
[range.subrange.general]: #range.subrange.general
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
[range.utility.conv]: #range.utility.conv
[range.utility.conv.adaptors]: #range.utility.conv.adaptors
[range.utility.conv.general]: #range.utility.conv.general
[range.utility.conv.to]: #range.utility.conv.to
[range.utility.general]: #range.utility.general
[range.utility.helpers]: #range.utility.helpers
[range.view]: #range.view
[range.zip]: #range.zip
[range.zip.iterator]: #range.zip.iterator
[range.zip.overview]: #range.zip.overview
[range.zip.sentinel]: #range.zip.sentinel
[range.zip.transform]: #range.zip.transform
[range.zip.transform.iterator]: #range.zip.transform.iterator
[range.zip.transform.overview]: #range.zip.transform.overview
[range.zip.transform.sentinel]: #range.zip.transform.sentinel
[range.zip.transform.view]: #range.zip.transform.view
[range.zip.view]: #range.zip.view
[ranges]: #ranges
[ranges.general]: #ranges.general
[ranges.syn]: #ranges.syn
[view.interface]: #view.interface
[view.interface.general]: #view.interface.general
[view.interface.members]: #view.interface.members

<!-- Link reference definitions -->
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[concepts.equality]: concepts.md#concepts.equality
[containers]: containers.md#containers
[conv.rval]: expr.md#conv.rval
[customization.point.object]: library.md#customization.point.object
[dcl.fct.def.coroutine]: dcl.md#dcl.fct.def.coroutine
[dcl.init.general]: dcl.md#dcl.init.general
[expr.await]: expr.md#expr.await
[expr.const]: expr.md#expr.const
[expr.yield]: expr.md#expr.yield
[iterator.concept.bidir]: iterators.md#iterator.concept.bidir
[iterator.concept.forward]: iterators.md#iterator.concept.forward
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
[range.lazy.split]: #range.lazy.split
[range.prim.data]: #range.prim.data
[range.range]: #range.range
[range.repeat.view]: #range.repeat.view
[range.sized]: #range.sized
[range.subrange]: #range.subrange
[range.summary]: #range.summary
[range.utility]: #range.utility
[ranges.syn]: #ranges.syn
[string.view]: strings.md#string.view
[term.array.type]: #term.array.type
[term.perfect.forwarding.call.wrapper]: #term.perfect.forwarding.call.wrapper
[views.span]: containers.md#views.span

<!-- Link reference definitions -->
[coro.generator]: #coro.generator
[range.access]: #range.access
[range.adaptors]: #range.adaptors
[range.factories]: #range.factories
[range.req]: #range.req
[range.utility]: #range.utility
