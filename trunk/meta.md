# Metaprogramming library <a id="meta">[[meta]]</a>

## General <a id="meta.general">[[meta.general]]</a>

This Clause describes metaprogramming facilities. These facilities are
summarized in [[meta.summary]].

**Table: Metaprogramming library summary**

| Subclause           |                     | Header          |
| ------------------- | ------------------- | --------------- |
| [[intseq]]          | Integer sequences   | `<utility>`     |
| [[type.traits]]     | Type traits         | `<type_traits>` |
| [[meta.reflection]] | Reflection          | `<meta>`        |
| [[ratio]]           | Rational arithmetic | `<ratio>`       |


## Compile-time integer sequences <a id="intseq">[[intseq]]</a>

### General <a id="intseq.general">[[intseq.general]]</a>

The library provides a class template that can represent an integer
sequence. When used as an argument to a function template the template
parameter pack defining the sequence can be deduced and used in a pack
expansion.

[*Note 1*: The `index_sequence` alias template is provided for the
common case of an integer sequence of type `size_t`; see also
[[tuple.apply]]. — *end note*\]

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
`integer_sequence` with `N` constant template arguments. The type
`make_integer_sequence<T, N>` is an alias for the type
`integer_sequence<T, 0, 1, `…`, N - 1>`.

[*Note 1*: `make_integer_sequence<int, 0>` is an alias for the type
`integer_sequence<int>`. — *end note*\]

## Metaprogramming and type traits <a id="type.traits">[[type.traits]]</a>

### General <a id="type.traits.general">[[type.traits.general]]</a>

Subclause [[type.traits]] describes components used by C++ programs,
particularly in templates, to support the widest possible range of
types, optimize template code usage, detect type related user errors,
and perform type inference and transformation at compile time. It
includes type classification traits, type property inspection traits,
and type transformations. The type classification traits describe a
complete taxonomy of all possible C++ types, and state where in that
taxonomy a given type belongs. The type property inspection traits allow
important characteristics of types or of combinations of types to be
inspected. The type transformations allow certain properties of types to
be manipulated.

All functions specified in [[type.traits]] are signal-safe
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
specializations for any of the templates specified in [[type.traits]] is
undefined.

Unless otherwise specified, an incomplete type may be used to
instantiate a template specified in [[type.traits]]. The behavior of a
program is undefined if

- an instantiation of a template specified in [[type.traits]] directly
  or indirectly depends on an incompletely-defined object type `T`, and
- that instantiation could yield a different result were `T`
  hypothetically completed.

### Header `<type_traits>` synopsis <a id="meta.type.synop">[[meta.type.synop]]</a>

``` cpp
// all freestanding
namespace std {
  // [meta.help], helper class
  template<class T, T v> struct integral_constant;

  template<bool B>
    using bool_constant = integral_constant<bool, B>;
  using true_type  = bool_constant<true>;
  using false_type = bool_constant<false>;

  // [const.wrap.class], class template constant_wrapper
  template<class T>
    struct cw-fixed-value;                                      // exposition only

  template<cw-fixed-value X, class = typename decltype(X)::type>
    struct constant_wrapper;

  template<class T>
    concept \defexposconceptnc{constexpr-param} =                                   // exposition only
      requires { typename constant_wrapper<T::value>; };

  struct cw-operators;                                          // exposition only

  template<cw-fixed-value X>
    constexpr auto cw = constant_wrapper<X>{};

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
  template<class T> struct is_reflection;

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
  template<class T> struct is_trivially_copyable;
  template<class T> struct is_trivially_relocatable;
  template<class T> struct is_replaceable;
  template<class T> struct is_standard_layout;
  template<class T> struct is_empty;
  template<class T> struct is_polymorphic;
  template<class T> struct is_abstract;
  template<class T> struct is_final;
  template<class T> struct is_aggregate;
  template<class T> struct is_consteval_only;

  template<class T> struct is_signed;
  template<class T> struct is_unsigned;
  template<class T> struct is_bounded_array;
  template<class T> struct is_unbounded_array;
  template<class T> struct is_scoped_enum;

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
  template<class T> struct is_nothrow_relocatable;

  template<class T> struct is_implicit_lifetime;

  template<class T> struct has_virtual_destructor;

  template<class T> struct has_unique_object_representations;

  template<class T, class U> struct reference_constructs_from_temporary;
  template<class T, class U> struct reference_converts_from_temporary;

  // [meta.unary.prop.query], type property queries
  template<class T> struct alignment_of;
  template<class T> struct rank;
  template<class T, unsigned I = 0> struct extent;

  // [meta.rel], type relations
  template<class T, class U> struct is_same;
  template<class Base, class Derived> struct is_base_of;
  template<class Base, class Derived> struct is_virtual_base_of;
  template<class From, class To> struct is_convertible;
  template<class From, class To> struct is_nothrow_convertible;
  template<class T, class U> struct is_layout_compatible;
  template<class Base, class Derived> struct is_pointer_interconvertible_base_of;

  template<class Fn, class... ArgTypes> struct is_invocable;
  template<class R, class Fn, class... ArgTypes> struct is_invocable_r;

  template<class Fn, class... ArgTypes> struct is_nothrow_invocable;
  template<class R, class Fn, class... ArgTypes> struct is_nothrow_invocable_r;

  template<class Fn, class Tuple> struct is_applicable;
  template<class Fn, class Tuple> struct is_nothrow_applicable;

  // [meta.trans.cv], const-volatile modifications
  template<class T> struct remove_const;
  template<class T> struct remove_volatile;
  template<class T> struct remove_cv;
  template<class T> struct add_const;
  template<class T> struct add_volatile;
  template<class T> struct add_cv;

  template<class T>
    using remove_const_t    = remove_const<T>::type;
  template<class T>
    using remove_volatile_t = remove_volatile<T>::type;
  template<class T>
    using remove_cv_t       = remove_cv<T>::type;
  template<class T>
    using add_const_t       = add_const<T>::type;
  template<class T>
    using add_volatile_t    = add_volatile<T>::type;
  template<class T>
    using add_cv_t          = add_cv<T>::type;

  // [meta.trans.ref], reference modifications
  template<class T> struct remove_reference;
  template<class T> struct add_lvalue_reference;
  template<class T> struct add_rvalue_reference;

  template<class T>
    using remove_reference_t     = remove_reference<T>::type;
  template<class T>
    using add_lvalue_reference_t = add_lvalue_reference<T>::type;
  template<class T>
    using add_rvalue_reference_t = add_rvalue_reference<T>::type;

  // [meta.trans.sign], sign modifications
  template<class T> struct make_signed;
  template<class T> struct make_unsigned;

  template<class T>
    using make_signed_t   = make_signed<T>::type;
  template<class T>
    using make_unsigned_t = make_unsigned<T>::type;

  // [meta.trans.arr], array modifications
  template<class T> struct remove_extent;
  template<class T> struct remove_all_extents;

  template<class T>
    using remove_extent_t      = remove_extent<T>::type;
  template<class T>
    using remove_all_extents_t = remove_all_extents<T>::type;

  // [meta.trans.ptr], pointer modifications
  template<class T> struct remove_pointer;
  template<class T> struct add_pointer;

  template<class T>
    using remove_pointer_t = remove_pointer<T>::type;
  template<class T>
    using add_pointer_t    = add_pointer<T>::type;

  // [meta.trans.other], other transformations
  template<class T> struct type_identity;
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
  template<class Fn, class Tuple> struct apply_result;
  template<class T> struct unwrap_reference;
  template<class T> struct unwrap_ref_decay;

  template<class T>
    using type_identity_t    = type_identity<T>::type;
  template<class T>
    using remove_cvref_t     = remove_cvref<T>::type;
  template<class T>
    using decay_t            = decay<T>::type;
  template<bool B, class T = void>
    using enable_if_t        = enable_if<B, T>::type;
  template<bool B, class T, class F>
    using conditional_t      = conditional<B, T, F>::type;
  template<class... T>
    using common_type_t      = common_type<T...>::type;
  template<class... T>
    using common_reference_t = common_reference<T...>::type;
  template<class T>
    using underlying_type_t  = underlying_type<T>::type;
  template<class Fn, class... ArgTypes>
    using invoke_result_t    = invoke_result<Fn, ArgTypes...>::type;
  template<class Fn, class Tuple>
    using apply_result_t     = apply_result<Fn, Tuple>::type;
  template<class T>
    using unwrap_reference_t = unwrap_reference<T>::type;
  template<class T>
    using unwrap_ref_decay_t = unwrap_ref_decay<T>::type;
  template<class...>
    using void_t             = void;

  // [meta.logical], logical operator traits
  template<class... B> struct conjunction;
  template<class... B> struct disjunction;
  template<class B> struct negation;

  // [meta.unary.cat], primary type categories
  template<class T>
    constexpr bool is_void_v = is_void<T>::value;
  template<class T>
    constexpr bool is_null_pointer_v = is_null_pointer<T>::value;
  template<class T>
    constexpr bool is_integral_v = is_integral<T>::value;
  template<class T>
    constexpr bool is_floating_point_v = is_floating_point<T>::value;
  template<class T>
    constexpr bool is_array_v = is_array<T>::value;
  template<class T>
    constexpr bool is_pointer_v = is_pointer<T>::value;
  template<class T>
    constexpr bool is_lvalue_reference_v = is_lvalue_reference<T>::value;
  template<class T>
    constexpr bool is_rvalue_reference_v = is_rvalue_reference<T>::value;
  template<class T>
    constexpr bool is_member_object_pointer_v = is_member_object_pointer<T>::value;
  template<class T>
    constexpr bool is_member_function_pointer_v = is_member_function_pointer<T>::value;
  template<class T>
    constexpr bool is_enum_v = is_enum<T>::value;
  template<class T>
    constexpr bool is_union_v = is_union<T>::value;
  template<class T>
    constexpr bool is_class_v = is_class<T>::value;
  template<class T>
    constexpr bool is_function_v = is_function<T>::value;
  template<class T>
    constexpr bool is_reflection_v = is_reflection<T>::value;

  // [meta.unary.comp], composite type categories
  template<class T>
    constexpr bool is_reference_v = is_reference<T>::value;
  template<class T>
    constexpr bool is_arithmetic_v = is_arithmetic<T>::value;
  template<class T>
    constexpr bool is_fundamental_v = is_fundamental<T>::value;
  template<class T>
    constexpr bool is_object_v = is_object<T>::value;
  template<class T>
    constexpr bool is_scalar_v = is_scalar<T>::value;
  template<class T>
    constexpr bool is_compound_v = is_compound<T>::value;
  template<class T>
    constexpr bool is_member_pointer_v = is_member_pointer<T>::value;

  // [meta.unary.prop], type properties
  template<class T>
    constexpr bool is_const_v = is_const<T>::value;
  template<class T>
    constexpr bool is_volatile_v = is_volatile<T>::value;
  template<class T>
    constexpr bool is_trivially_copyable_v = is_trivially_copyable<T>::value;
  template<class T>
    constexpr bool is_trivially_relocatable_v = is_trivially_relocatable<T>::value;
  template<class T>
    constexpr bool is_standard_layout_v = is_standard_layout<T>::value;
  template<class T>
    constexpr bool is_empty_v = is_empty<T>::value;
  template<class T>
    constexpr bool is_polymorphic_v = is_polymorphic<T>::value;
  template<class T>
    constexpr bool is_abstract_v = is_abstract<T>::value;
  template<class T>
    constexpr bool is_final_v = is_final<T>::value;
  template<class T>
    constexpr bool is_aggregate_v = is_aggregate<T>::value;
  template<class T>
    constexpr bool is_consteval_only_v = is_consteval_only<T>::value;
  template<class T>
    constexpr bool is_signed_v = is_signed<T>::value;
  template<class T>
    constexpr bool is_unsigned_v = is_unsigned<T>::value;
  template<class T>
    constexpr bool is_bounded_array_v = is_bounded_array<T>::value;
  template<class T>
    constexpr bool is_unbounded_array_v = is_unbounded_array<T>::value;
  template<class T>
    constexpr bool is_scoped_enum_v = is_scoped_enum<T>::value;
  template<class T, class... Args>
    constexpr bool is_constructible_v = is_constructible<T, Args...>::value;
  template<class T>
    constexpr bool is_default_constructible_v = is_default_constructible<T>::value;
  template<class T>
    constexpr bool is_copy_constructible_v = is_copy_constructible<T>::value;
  template<class T>
    constexpr bool is_move_constructible_v = is_move_constructible<T>::value;
  template<class T, class U>
    constexpr bool is_assignable_v = is_assignable<T, U>::value;
  template<class T>
    constexpr bool is_copy_assignable_v = is_copy_assignable<T>::value;
  template<class T>
    constexpr bool is_move_assignable_v = is_move_assignable<T>::value;
  template<class T, class U>
    constexpr bool is_swappable_with_v = is_swappable_with<T, U>::value;
  template<class T>
    constexpr bool is_swappable_v = is_swappable<T>::value;
  template<class T>
    constexpr bool is_destructible_v = is_destructible<T>::value;
  template<class T, class... Args>
    constexpr bool is_trivially_constructible_v = is_trivially_constructible<T, Args...>::value;
  template<class T>
    constexpr bool is_trivially_default_constructible_v
      = is_trivially_default_constructible<T>::value;
  template<class T>
    constexpr bool is_trivially_copy_constructible_v = is_trivially_copy_constructible<T>::value;
  template<class T>
    constexpr bool is_trivially_move_constructible_v = is_trivially_move_constructible<T>::value;
  template<class T, class U>
    constexpr bool is_trivially_assignable_v = is_trivially_assignable<T, U>::value;
  template<class T>
    constexpr bool is_trivially_copy_assignable_v = is_trivially_copy_assignable<T>::value;
  template<class T>
    constexpr bool is_trivially_move_assignable_v = is_trivially_move_assignable<T>::value;
  template<class T>
    constexpr bool is_trivially_destructible_v = is_trivially_destructible<T>::value;
  template<class T, class... Args>
    constexpr bool is_nothrow_constructible_v = is_nothrow_constructible<T, Args...>::value;
  template<class T>
    constexpr bool is_nothrow_default_constructible_v
      = is_nothrow_default_constructible<T>::value;
  template<class T>
    constexpr bool is_nothrow_copy_constructible_v = is_nothrow_copy_constructible<T>::value;
  template<class T>
    constexpr bool is_nothrow_move_constructible_v = is_nothrow_move_constructible<T>::value;
  template<class T, class U>
    constexpr bool is_nothrow_assignable_v = is_nothrow_assignable<T, U>::value;
  template<class T>
    constexpr bool is_nothrow_copy_assignable_v = is_nothrow_copy_assignable<T>::value;
  template<class T>
    constexpr bool is_nothrow_move_assignable_v = is_nothrow_move_assignable<T>::value;
  template<class T, class U>
    constexpr bool is_nothrow_swappable_with_v = is_nothrow_swappable_with<T, U>::value;
  template<class T>
    constexpr bool is_nothrow_swappable_v = is_nothrow_swappable<T>::value;
  template<class T>
    constexpr bool is_nothrow_destructible_v = is_nothrow_destructible<T>::value;
  template<class T>
    constexpr bool is_nothrow_relocatable_v = is_nothrow_relocatable<T>::value;
  template<class T>
    constexpr bool is_implicit_lifetime_v = is_implicit_lifetime<T>::value;
  template<class T>
    constexpr bool is_replaceable_v = is_replaceable<T>::value;
  template<class T>
    constexpr bool has_virtual_destructor_v = has_virtual_destructor<T>::value;
  template<class T>
    constexpr bool has_unique_object_representations_v
      = has_unique_object_representations<T>::value;
  template<class T, class U>
    constexpr bool reference_constructs_from_temporary_v
      = reference_constructs_from_temporary<T, U>::value;
  template<class T, class U>
    constexpr bool reference_converts_from_temporary_v
      = reference_converts_from_temporary<T, U>::value;

  // [meta.unary.prop.query], type property queries
  template<class T>
    constexpr size_t alignment_of_v = alignment_of<T>::value;
  template<class T>
    constexpr size_t rank_v = rank<T>::value;
  template<class T, unsigned I = 0>
    constexpr size_t extent_v = extent<T, I>::value;

  // [meta.rel], type relations
  template<class T, class U>
    constexpr bool is_same_v = is_same<T, U>::value;
  template<class Base, class Derived>
    constexpr bool is_base_of_v = is_base_of<Base, Derived>::value;
  template<class Base, class Derived>
    constexpr bool is_virtual_base_of_v = is_virtual_base_of<Base, Derived>::value;
  template<class From, class To>
    constexpr bool is_convertible_v = is_convertible<From, To>::value;
  template<class From, class To>
    constexpr bool is_nothrow_convertible_v = is_nothrow_convertible<From, To>::value;
  template<class T, class U>
    constexpr bool is_layout_compatible_v = is_layout_compatible<T, U>::value;
  template<class Base, class Derived>
    constexpr bool is_pointer_interconvertible_base_of_v
      = is_pointer_interconvertible_base_of<Base, Derived>::value;
  template<class Fn, class... ArgTypes>
    constexpr bool is_invocable_v = is_invocable<Fn, ArgTypes...>::value;
  template<class R, class Fn, class... ArgTypes>
    constexpr bool is_invocable_r_v = is_invocable_r<R, Fn, ArgTypes...>::value;
  template<class Fn, class... ArgTypes>
    constexpr bool is_nothrow_invocable_v = is_nothrow_invocable<Fn, ArgTypes...>::value;
  template<class R, class Fn, class... ArgTypes>
    constexpr bool is_nothrow_invocable_r_v = is_nothrow_invocable_r<R, Fn, ArgTypes...>::value;
  template<class Fn, class Tuple>
    constexpr bool is_applicable_v = is_applicable<Fn, Tuple>::value;
  template<class Fn, class Tuple>
    constexpr bool is_nothrow_applicable_v = is_nothrow_applicable<Fn, Tuple>::value;

  // [meta.logical], logical operator traits
  template<class... B>
    constexpr bool conjunction_v = conjunction<B...>::value;
  template<class... B>
    constexpr bool disjunction_v = disjunction<B...>::value;
  template<class B>
    constexpr bool negation_v = negation<B>::value;

  // [meta.member], member relationships
  template<class S, class M>
    constexpr bool is_pointer_interconvertible_with_class(M S::*m) noexcept;
  template<class S1, class S2, class M1, class M2>
    constexpr bool is_corresponding_member(M1 S1::*m1, M2 S2::*m2) noexcept;

  // [meta.const.eval], constant evaluation context
  constexpr bool is_constant_evaluated() noexcept;
  consteval bool is_within_lifetime(const auto*) noexcept;
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

### Class template `constant_wrapper` <a id="const.wrap.class">[[const.wrap.class]]</a>

``` cpp
namespace std {
  template<class T>
  struct cw-fixed-value {                                                         // exposition only
    using type = T;                                                               // exposition only
    constexpr cw-fixed-value(type v) noexcept : data(v) {}
    T data;                                                                       // exposition only
  };

  template<class T, size_t Extent>
  struct cw-fixed-value<T[Extent]> {                                              // exposition only
    using type = T[Extent];                                                       // exposition only
    constexpr cw-fixed-value(T (&arr)[Extent]) noexcept;
    T data[Extent];                                                               // exposition only
  };

  template<class T, size_t Extent>
    cw-fixed-value(T (&)[Extent]) -> cw-fixed-value<T[Extent]>;                   // exposition only

  struct cw-operators {                                                           // exposition only
    // unary operators
    template<constexpr-param T>
      friend constexpr auto operator+(T) noexcept -> constant_wrapper<(+T::value)>
        { return {}; }
    template<constexpr-param T>
      friend constexpr auto operator-(T) noexcept -> constant_wrapper<(-T::value)>
        { return {}; }
    template<constexpr-param T>
      friend constexpr auto operator~(T) noexcept -> constant_wrapper<(~T::value)>
        { return {}; }
    template<constexpr-param T>
      friend constexpr auto operator!(T) noexcept -> constant_wrapper<(!T::value)>
        { return {}; }
    template<constexpr-param T>
      friend constexpr auto operator&(T) noexcept -> constant_wrapper<(&T::value)>
        { return {}; }
    template<constexpr-param T>
      friend constexpr auto operator*(T) noexcept -> constant_wrapper<(*T::value)>
        { return {}; }

    // binary operators
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator+(L, R) noexcept -> constant_wrapper<(L::value + R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator-(L, R) noexcept -> constant_wrapper<(L::value - R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator*(L, R) noexcept -> constant_wrapper<(L::value * R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator/(L, R) noexcept -> constant_wrapper<(L::value / R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator%(L, R) noexcept -> constant_wrapper<(L::value % R::value)>
        { return {}; }

    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator<<(L, R) noexcept -> constant_wrapper<(L::value << R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator>>(L, R) noexcept -> constant_wrapper<(L::value >> R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator&(L, R) noexcept -> constant_wrapper<(L::value & R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator|(L, R) noexcept -> constant_wrapper<(L::value | R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator^(L, R) noexcept -> constant_wrapper<(L::value ^ R::value)>
        { return {}; }

    template<constexpr-param L, constexpr-param R>
      requires (!is_constructible_v<bool, decltype(L::value)> ||
                !is_constructible_v<bool, decltype(R::value)>)
        friend constexpr auto operator&&(L, R) noexcept
          -> constant_wrapper<(L::value && R::value)>
            { return {}; }
    template<constexpr-param L, constexpr-param R>
      requires (!is_constructible_v<bool, decltype(L::value)> ||
                !is_constructible_v<bool, decltype(R::value)>)
        friend constexpr auto operator||(L, R) noexcept
          -> constant_wrapper<(L::value || R::value)>
            { return {}; }

    // comparisons
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator<=>(L, R) noexcept
        -> constant_wrapper<(L::value <=> R::value)>
          { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator<(L, R) noexcept -> constant_wrapper<(L::value < R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator<=(L, R) noexcept -> constant_wrapper<(L::value <= R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator==(L, R) noexcept -> constant_wrapper<(L::value == R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator!=(L, R) noexcept -> constant_wrapper<(L::value != R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator>(L, R) noexcept -> constant_wrapper<(L::value > R::value)>
        { return {}; }
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator>=(L, R) noexcept -> constant_wrapper<(L::value >= R::value)>
        { return {}; }

    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator,(L, R) noexcept = delete;
    template<constexpr-param L, constexpr-param R>
      friend constexpr auto operator->*(L, R) noexcept -> constant_wrapper<L::value->*(R::value)>
        { return {}; }

    // call and index
    template<constexpr-param T, constexpr-param... Args>
      constexpr auto operator()(this T, Args...) noexcept
        requires requires { constant_wrapper<T::value(Args::value...)>(); }
          { return constant_wrapper<T::value(Args::value...)>{}; }
    template<constexpr-param T, constexpr-param... Args>
      constexpr auto operator[](this T, Args...) noexcept
        -> constant_wrapper<(T::value[Args::value...])>
          { return {}; }

    // pseudo-mutators
    template<constexpr-param T>
      constexpr auto operator++(this T) noexcept
        requires requires(T::value_type x) { ++x; }
          { return constant_wrapper<[] { auto c = T::value; return ++c; }()>{}; }
    template<constexpr-param T>
      constexpr auto operator++(this T, int) noexcept
        requires requires(T::value_type x) { x++; }
          { return constant_wrapper<[] { auto c = T::value; return c++; }()>{}; }

    template<constexpr-param T>
      constexpr auto operator--(this T) noexcept
        requires requires(T::value_type x) { --x; }
          { return constant_wrapper<[] { auto c = T::value; return --c; }()>{}; }
    template<constexpr-param T>
      constexpr auto operator--(this T, int) noexcept
        requires requires(T::value_type x) { x--; }
          { return constant_wrapper<[] { auto c = T::value; return c--; }()>{}; }

    template<constexpr-param T, constexpr-param R>
      constexpr auto operator+=(this T, R) noexcept
        requires requires(T::value_type x) { x += R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v += R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator-=(this T, R) noexcept
        requires requires(T::value_type x) { x -= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v -= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator*=(this T, R) noexcept
        requires requires(T::value_type x) { x *= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v *= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator/=(this T, R) noexcept
        requires requires(T::value_type x) { x /= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v /= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator%=(this T, R) noexcept
        requires requires(T::value_type x) { x %= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v %= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator&=(this T, R) noexcept
        requires requires(T::value_type x) { x &= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v &= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator|=(this T, R) noexcept
        requires requires(T::value_type x) { x |= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v |= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator^=(this T, R) noexcept
        requires requires(T::value_type x) { x ^= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v ^= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator<<=(this T, R) noexcept
        requires requires(T::value_type x) { x <<= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v <<= R::value; }()>{}; }
    template<constexpr-param T, constexpr-param R>
      constexpr auto operator>>=(this T, R) noexcept
        requires requires(T::value_type x) { x >>= R::value; }
          { return constant_wrapper<[] { auto v = T::value; return v >>= R::value; }()>{}; }
  };

  template<cw-fixed-value X, class>
  struct constant_wrapper : cw-operators {
    static constexpr const auto & value = X.data;
    using type = constant_wrapper;
    using value_type = decltype(X)::type;

    template<constexpr-param R>
      constexpr auto operator=(R) const noexcept
        requires requires(value_type x) { x = R::value; }
          { return constant_wrapper<[] { auto v = value; return v = R::value; }()>{}; }

    constexpr operator decltype(auto)() const noexcept { return value; }
  };
}
```

The class template `constant_wrapper` aids in metaprogramming by
ensuring that the evaluation of expressions comprised entirely of
`constant_wrapper` are core constant expressions [[expr.const]],
regardless of the context in which they appear. In particular, this
enables use of `constant_wrapper` values that are passed as arguments to
constexpr functions to be used in constant expressions.

[*Note 1*: The unnamed second template parameter to `constant_wrapper`
is present to aid argument-dependent lookup [[basic.lookup.argdep]] in
finding overloads for which `constant_wrapper`’s wrapped value is a
suitable argument, but for which the `constant_wrapper` itself is
not. — *end note*\]

[*Example 1*:

``` cpp
  constexpr auto initial_phase(auto quantity_1, auto quantity_2) {
    return quantity_1 + quantity_2;
  }

  constexpr auto middle_phase(auto tbd) {
    return tbd;
  }

  void final_phase(auto gathered, auto available) {
    if constexpr (gathered == available)
      std::cout << "Profit!\n";
  }

  void impeccable_underground_planning() {
    auto gathered_quantity = middle_phase(initial_phase(std::cw<42>, std::cw<13>));
    static_assert(gathered_quantity == 55);
    auto all_available = std::cw<55>;
    final_phase(gathered_quantity, all_available);
  }

  void deeply_flawed_underground_planning() {
    constexpr auto gathered_quantity = middle_phase(initial_phase(42, 13));
    constexpr auto all_available = 55;
    final_phase(gathered_quantity, all_available);  // error: gathered == available
                                                    // is not a constant expression
  }
```

— *end example*\]

``` cpp
constexpr cw-fixed-value(T (&arr)[Extent]) noexcept;
```

*Effects:* Initialize elements of *data* with corresponding elements of
`arr`.

### Unary type traits <a id="meta.unary">[[meta.unary]]</a>

#### General <a id="meta.unary.general">[[meta.unary.general]]</a>

Subclause [[meta.unary]] contains templates that may be used to query
the properties of a type at compile time.

Each of these templates shall be a *Cpp17UnaryTypeTrait* [[meta.rqmts]]
with a base characteristic of `true_type` if the corresponding condition
is `true`, otherwise `false_type`.

#### Primary type categories <a id="meta.unary.cat">[[meta.unary.cat]]</a>

The primary type categories specified in [[meta.unary.cat]] correspond
to the descriptions given in subclause  [[basic.types]] of the C++
standard.

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

[*Note 1*: For any given type `T`, exactly one of the primary type
categories has a `value` member that evaluates to `true`. — *end note*\]

#### Composite type traits <a id="meta.unary.comp">[[meta.unary.comp]]</a>

The templates specified in [[meta.unary.comp]] provide convenient
compositions of the primary type categories, corresponding to the
descriptions given in subclause  [[basic.types]].

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

#### Type properties <a id="meta.unary.prop">[[meta.unary.prop]]</a>

The templates specified in [[meta.unary.prop]] provide access to some of
the more important properties of types.

It is unspecified whether the library defines any full or partial
specializations of any of these templates.

For all of the class templates `X` declared in this subclause,
instantiating that template with a template-argument that is a class
template specialization may result in the implicit instantiation of the
template argument if and only if the semantics of `X` require that the
argument is a complete type.

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial [[term.trivial.type]], [[special]] function call that is not an
odr-use [[term.odr.use]] of `declval` in the context of the
corresponding definition notwithstanding the restrictions of 
[[declval]].

For the purpose of defining the templates in this subclause, let
`VAL<T>` for some type `T` be an expression defined as follows:

- If `T` is a reference or function type, `VAL<T>` is an expression with
  the same type and value category as `declval<T>()`.
- Otherwise, `VAL<T>` is a prvalue that initially has type `T`.
  \[*Note 1*: If `T` is cv-qualified, the cv-qualification is subject to
  adjustment [[expr.type]]. — *end note*\]

[*Example 1*:

``` cpp
is_const_v<const volatile int>      // true
is_const_v<const int*>              // false
is_const_v<const int&>              // false
is_const_v<int[3]>                  // false
is_const_v<const int[3]>            // true
```

— *end example*\]

[*Example 2*:

``` cpp
remove_const_t<const volatile int>  // volatile int
remove_const_t<const int* const>    // const int*
remove_const_t<const int&>          // const int&
remove_const_t<const int[3]>        // int[3]
```

— *end example*\]

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

— *end example*\]

The predicate condition for a template specialization
`is_constructible<T, Args...>` shall be satisfied if and only if the
following variable definition would be well-formed for some invented
variable `t`:

``` cpp
T t(declval<Args>()...);
```

[*Note 1*: These tokens are never interpreted as a function
declaration. — *end note*\]

Access checking is performed as if in a context unrelated to `T` and any
of the `Args`. Only the validity of the immediate context of the
variable initialization is considered.

[*Note 2*: The evaluation of the initialization can result in side
effects such as the instantiation of class template specializations and
function template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*\]

The predicate condition for a template specialization
`has_unique_object_representations<T>` shall be satisfied if and only if

- `T` is trivially copyable, and
- any two objects of type `T` with the same value have the same object
  representation, where
  - two objects of array or non-union class type are considered to have
    the same value if their respective sequences of direct subobjects
    have the same values, and
  - two objects of union type are considered to have the same value if
    they have the same active member and the corresponding members have
    the same value.

The set of scalar types for which this condition holds is
*implementation-defined*.

[*Note 3*: If a type has padding bits, the condition does not hold;
otherwise, the condition holds true for integral types. — *end note*\]

### Type property queries <a id="meta.unary.prop.query">[[meta.unary.prop.query]]</a>

The templates specified in [[meta.unary.prop.query]] may be used to
query properties of types at compile time.

Each of these templates shall be a *Cpp17UnaryTypeTrait* [[meta.rqmts]]
with a base characteristic of `integral_constant<size_t, Value>`.

[*Example 1*:

``` cpp
// the following assertions hold:
static_assert(rank_v<int> == 0);
static_assert(rank_v<int[2]> == 1);
static_assert(rank_v<int[][4]> == 2);
```

— *end example*\]

[*Example 2*:

``` cpp
// the following assertions hold:
static_assert(extent_v<int> == 0);
static_assert(extent_v<int[2]> == 2);
static_assert(extent_v<int[2][4]> == 2);
static_assert(extent_v<int[][4]> == 0);
static_assert(extent_v<int, 1> == 0);
static_assert(extent_v<int[2], 1> == 0);
static_assert(extent_v<int[2][4], 1> == 4);
static_assert(extent_v<int[][4], 1> == 4);
```

— *end example*\]

### Relationships between types <a id="meta.rel">[[meta.rel]]</a>

The templates specified in [[meta.rel]] may be used to query
relationships between types at compile time.

Each of these templates shall be a *Cpp17BinaryTypeTrait* [[meta.rqmts]]
with a base characteristic of `true_type` if the corresponding condition
is true, otherwise `false_type`.

Let `ELEMS-OF(T)` be the parameter pack `get<N>(declval<T>())`, where
*N* is the pack of `size_t` template arguments of the specialization of
`index_sequence` denoted by
`make_index_sequence<tuple_size_v<remove_reference_t<T>>>`.

[*Note 1*: Virtual base classes that are private, protected, or
ambiguous are, nonetheless, virtual base classes. — *end note*\]

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial [[term.trivial.type]], [[special]] function call that is not an
odr-use [[term.odr.use]] of `declval` in the context of the
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

— *end example*\]

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
types, array types, function types, and cv `void`. — *end note*\]

Access checking is performed in a context unrelated to `To` and `From`.
Only the validity of the immediate context of the *expression* of the
`return` statement [[stmt.return]] (including initialization of the
returned object or reference) is considered.

[*Note 3*: The initialization can result in side effects such as the
instantiation of class template specializations and function template
specializations, the generation of implicitly-defined functions, and so
on. Such side effects are not in the “immediate context” and can result
in the program being ill-formed. — *end note*\]

### Transformations between types <a id="meta.trans">[[meta.trans]]</a>

#### General <a id="meta.trans.general">[[meta.trans.general]]</a>

Each of the templates in [[meta.trans]] shall be a
*Cpp17TransformationTrait* [[meta.rqmts]].

#### Const-volatile modifications <a id="meta.trans.cv">[[meta.trans.cv]]</a>

The templates specified in [[meta.trans.cv]] add or remove
cv-qualifications [[basic.type.qualifier]].

#### Reference modifications <a id="meta.trans.ref">[[meta.trans.ref]]</a>

The templates specified in [[meta.trans.ref]] add or remove references.

#### Sign modifications <a id="meta.trans.sign">[[meta.trans.sign]]</a>

The templates specified in [[meta.trans.sign]] convert an integer type
to its corresponding signed or unsigned type.

#### Array modifications <a id="meta.trans.arr">[[meta.trans.arr]]</a>

The templates specified in [[meta.trans.arr]] modify array types.

[*Example 1*:

``` cpp
// the following assertions hold:
static_assert(is_same_v<remove_extent_t<int>, int>);
static_assert(is_same_v<remove_extent_t<int[2]>, int>);
static_assert(is_same_v<remove_extent_t<int[2][3]>, int[3]>);
static_assert(is_same_v<remove_extent_t<int[][3]>, int[3]>);
```

— *end example*\]

[*Example 2*:

``` cpp
// the following assertions hold:
static_assert(is_same_v<remove_all_extents_t<int>, int>);
static_assert(is_same_v<remove_all_extents_t<int[2]>, int>);
static_assert(is_same_v<remove_all_extents_t<int[2][3]>, int>);
static_assert(is_same_v<remove_all_extents_t<int[][3]>, int>);
```

— *end example*\]

#### Pointer modifications <a id="meta.trans.ptr">[[meta.trans.ptr]]</a>

The templates specified in [[meta.trans.ptr]] add or remove pointers.

#### Other transformations <a id="meta.trans.other">[[meta.trans.other]]</a>

The templates specified in [[meta.trans.other]] perform other
modifications of a type.

[*Note 1*: The compilation of the expression can result in side effects
such as the instantiation of class template specializations and function
template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*\]

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
  `const volatile short`. — *end example*\]
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

For the `common_type` trait applied to a template parameter pack `T` of
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
  - \[*Note 2*: None of the following will apply if there is a
    specialization `common_type<D1, D2>`. — *end note*\]
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

Notwithstanding the provisions of [[meta.rqmts]], and pursuant to
[[namespace.std]], a program may specialize `common_type<T1, T2>` for
types `T1` and `T2` such that `is_same_v<T1, decay_t<T1>>` and
`is_same_v<T2, decay_t<T2>>` are each `true`.

[*Note 2*: Such specializations are needed when only explicit
conversions are desired between the template arguments. — *end note*\]

Such a specialization need not have a member named `type`, but if it
does, the *qualified-id* `common_type<T1, T2>::type` shall denote a
cv-unqualified non-reference type to which each of the types `T1` and
`T2` is explicitly convertible. Moreover, `common_type_t<T1, T2>` shall
denote the same type, if any, as does `common_type_t<T2, T1>`. No
diagnostic is required for a violation of this Note’s rules.

For the `common_reference` trait applied to a parameter pack `T` of
types, the member `type` shall be either defined or not present as
follows:

- If `sizeof...(T)` is zero, there shall be no member `type`.
- Otherwise, if `sizeof...(T)` is one, let `T0` denote the sole type in
  the pack `T`. The member typedef `type` shall denote the same type as
  `T0`.
- Otherwise, if `sizeof...(T)` is two, let `T1` and `T2` denote the two
  types in the pack `T`. Then
  - Let `R` be `COMMON-REF(T1, T2)`. If `T1` and `T2` are reference
    types, `R` is well-formed, and
    `is_convertible_v<add_pointer_t<T1>, add_pointer_t<R>> && is_convertible_v<add_poin{}ter_t<T2>, add_pointer_t<R>>`
    is `true`, then the member typedef `type` denotes `R`.
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

Notwithstanding the provisions of [[meta.rqmts]], and pursuant to
[[namespace.std]], a program may partially specialize
`basic_common_reference<T, U, TQual, UQual>` for types `T` and `U` such
that `is_same_v<T, decay_t<T>>` and `is_same_v<U, decay_t<U>>` are each
`true`.

[*Note 3*: Such specializations can be used to influence the result of
`common_reference`, and are needed when only explicit conversions are
desired between the template arguments. — *end note*\]

Such a specialization need not have a member named `type`, but if it
does, the *qualified-id*
`basic_common_reference<T, U, TQual, UQual>::type` shall denote a type
to which each of the types `TQual<T>` and `UQual<U>` is convertible.
Moreover, `basic_common_reference<T, U, TQual, UQual>::type` shall
denote the same type, if any, as does
`basic_common_reference<U, T, UQual, TQual>::type`. No diagnostic is
required for a violation of these rules.

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

— *end example*\]

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
built-in operator `&&`. — *end note*\]

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
`false_type`. — *end note*\]

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
built-in operator `||`. — *end note*\]

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
`false_type`. — *end note*\]

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
struct [[class.prop]] types, `M1` and `M2` are object types, `m1` and
`m2` are not null, and `m1` and `m2` point to corresponding members of
the common initial sequence [[class.mem]] of `S1` and `S2`.

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
static_assert( !is_pointer_interconvertible_with_class<C, int>( &C::b ) );
  // Forces the use of class C, and the result is false.

static_assert( is_corresponding_member( &C::a, &C::b ) );
  // Succeeds because, despite its appearance, &C::a and &C::b have types
  // ``pointer to member of A of type int'' and
  // ``pointer to member of B of type int'', respectively.
static_assert( !is_corresponding_member<C, C, int, int>( &C::a, &C::b ) );
  // Forces the use of class C, and the result is false.
```

— *end example*\]

— *end note*\]

### Constant evaluation context <a id="meta.const.eval">[[meta.const.eval]]</a>

``` cpp
constexpr bool is_constant_evaluated() noexcept;
```

*Effects:* Equivalent to:

``` cpp
if consteval {
  return true;
} else {
  return false;
}
```

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

— *end example*\]

``` cpp
consteval bool is_within_lifetime(const auto* p) noexcept;
```

*Returns:* `true` if `p` is a pointer to an object that is within its
lifetime [[basic.life]]; otherwise, `false`.

*Remarks:* During the evaluation of an expression `E` as a core constant
expression, a call to this function is ill-formed unless `p` points to
an object that is usable in constant expressions or whose complete
object’s lifetime began within `E`.

[*Example 2*:

``` cpp
struct OptBool {
  union { bool b; char c; };

  // note: this assumes common implementation properties for bool and char:
  // * sizeof(bool) == sizeof(char), and
  // * the value representations for true and false are distinct
  //   from the value representation for 2
  constexpr OptBool() : c(2) { }
  constexpr OptBool(bool b) : b(b) { }

  constexpr auto has_value() const -> bool {
    if consteval {
      return std::is_within_lifetime(&b);       // during constant evaluation, cannot read from c
    } else {
      return c != 2;                            // during runtime, must read from c
    }
  }

  constexpr auto operator*() const -> const bool& {
    return b;
  }
};

constexpr OptBool disengaged;
constexpr OptBool engaged(true);
static_assert(!disengaged.has_value());
static_assert(engaged.has_value());
static_assert(*engaged);
```

— *end example*\]

## Reflection <a id="meta.reflection">[[meta.reflection]]</a>

### Header `<meta>` synopsis <a id="meta.syn">[[meta.syn]]</a>

``` cpp
#include <initializer_list>     // see [initializer.list.syn]

namespace std {
  // [meta.string.literal], checking string literals
  consteval bool is_string_literal(const char* p);
  consteval bool is_string_literal(const wchar_t* p);
  consteval bool is_string_literal(const char8_t* p);
  consteval bool is_string_literal(const char16_t* p);
  consteval bool is_string_literal(const char32_t* p);

  // [meta.define.static], promoting to static storage
  namespace meta {
    template<ranges::input_range R>
      consteval info reflect_constant_string(R&& r);
    template<ranges::input_range R>
      consteval info reflect_constant_array(R&& r);
  }
  template<ranges::input_range R>
    consteval const ranges::range_value_t<R>* define_static_string(R&& r);
  template<ranges::input_range R>
    consteval span<const ranges::range_value_t<R>> define_static_array(R&& r);
  template<class T>
    consteval const remove_cvref_t<T>* define_static_object(T&& r);
}

namespace std::meta {
  using info = decltype(^^::);

  // [meta.reflection.exception], class exception
  class exception;

  // [meta.reflection.operators], operator representations
  enum class operators {
    see below;
  };
  using enum operators;
  consteval operators operator_of(info r);
  consteval string_view symbol_of(operators op);
  consteval u8string_view u8symbol_of(operators op);

  // [meta.reflection.names], reflection names and locations
  consteval bool has_identifier(info r);

  consteval string_view identifier_of(info r);
  consteval u8string_view u8identifier_of(info r);

  consteval string_view display_string_of(info r);
  consteval u8string_view u8display_string_of(info r);

  consteval source_location source_location_of(info r);

  // [meta.reflection.queries], reflection queries
  consteval info type_of(info r);
  consteval info object_of(info r);
  consteval info constant_of(info r);

  consteval bool is_public(info r);
  consteval bool is_protected(info r);
  consteval bool is_private(info r);

  consteval bool is_virtual(info r);
  consteval bool is_pure_virtual(info r);
  consteval bool is_override(info r);
  consteval bool is_final(info r);

  consteval bool is_deleted(info r);
  consteval bool is_defaulted(info r);
  consteval bool is_user_provided(info r);
  consteval bool is_user_declared(info r);
  consteval bool is_explicit(info r);
  consteval bool is_noexcept(info r);

  consteval bool is_bit_field(info r);
  consteval bool is_enumerator(info r);
  consteval bool is_annotation(info r);

  consteval bool is_const(info r);
  consteval bool is_volatile(info r);
  consteval bool is_mutable_member(info r);
  consteval bool is_lvalue_reference_qualified(info r);
  consteval bool is_rvalue_reference_qualified(info r);

  consteval bool has_static_storage_duration(info r);
  consteval bool has_thread_storage_duration(info r);
  consteval bool has_automatic_storage_duration(info r);

  consteval bool has_internal_linkage(info r);
  consteval bool has_module_linkage(info r);
  consteval bool has_external_linkage(info r);
  consteval bool has_c_language_linkage(info r);
  consteval bool has_linkage(info r);

  consteval bool is_complete_type(info r);
  consteval bool is_enumerable_type(info r);

  consteval bool is_variable(info r);
  consteval bool is_type(info r);
  consteval bool is_namespace(info r);
  consteval bool is_type_alias(info r);
  consteval bool is_namespace_alias(info r);

  consteval bool is_function(info r);
  consteval bool is_conversion_function(info r);
  consteval bool is_operator_function(info r);
  consteval bool is_literal_operator(info r);
  consteval bool is_special_member_function(info r);
  consteval bool is_constructor(info r);
  consteval bool is_default_constructor(info r);
  consteval bool is_copy_constructor(info r);
  consteval bool is_move_constructor(info r);
  consteval bool is_assignment(info r);
  consteval bool is_copy_assignment(info r);
  consteval bool is_move_assignment(info r);
  consteval bool is_destructor(info r);

  consteval bool is_function_parameter(info r);
  consteval bool is_explicit_object_parameter(info r);
  consteval bool has_default_argument(info r);
  consteval bool has_ellipsis_parameter(info r);

  consteval bool is_template(info r);
  consteval bool is_function_template(info r);
  consteval bool is_variable_template(info r);
  consteval bool is_class_template(info r);
  consteval bool is_alias_template(info r);
  consteval bool is_conversion_function_template(info r);
  consteval bool is_operator_function_template(info r);
  consteval bool is_literal_operator_template(info r);
  consteval bool is_constructor_template(info r);
  consteval bool is_concept(info r);

  consteval bool is_value(info r);
  consteval bool is_object(info r);

  consteval bool is_structured_binding(info r);

  consteval bool is_class_member(info r);
  consteval bool is_namespace_member(info r);
  consteval bool is_nonstatic_data_member(info r);
  consteval bool is_static_member(info r);
  consteval bool is_base(info r);

  consteval bool has_default_member_initializer(info r);

  consteval bool has_parent(info r);
  consteval info parent_of(info r);

  consteval info dealias(info r);

  consteval bool has_template_arguments(info r);
  consteval info template_of(info r);
  consteval vector<info> template_arguments_of(info r);
  consteval vector<info> parameters_of(info r);
  consteval info variable_of(info r);
  consteval info return_type_of(info r);

  // [meta.reflection.access.context], access control context
  struct access_context;

  // [meta.reflection.access.queries], member accessibility queries
  consteval bool is_accessible(info r, access_context ctx);
  consteval bool has_inaccessible_nonstatic_data_members(info r, access_context ctx);
  consteval bool has_inaccessible_bases(info r, access_context ctx);
  consteval bool has_inaccessible_subobjects(info r, access_context ctx);

  // [meta.reflection.member.queries], reflection member queries
  consteval vector<info> members_of(info r, access_context ctx);
  consteval vector<info> bases_of(info type, access_context ctx);
  consteval vector<info> static_data_members_of(info type, access_context ctx);
  consteval vector<info> nonstatic_data_members_of(info type, access_context ctx);
  consteval vector<info> subobjects_of(info type, access_context ctx);
  consteval vector<info> enumerators_of(info type_enum);

  // [meta.reflection.layout], reflection layout queries
  struct member_offset;
  consteval member_offset offset_of(info r);
  consteval size_t size_of(info r);
  consteval size_t alignment_of(info r);
  consteval size_t bit_size_of(info r);

  // [meta.reflection.annotation], annotation reflection
  consteval vector<info> annotations_of(info item);
  consteval vector<info> annotations_of_with_type(info item, info type);

  // [meta.reflection.extract], value extraction
  template<class T>
    consteval T extract(info);

  // [meta.reflection.substitute], reflection substitution
  template<class R>
    concept reflection_range = see below;

  template<reflection_range R = initializer_list<info>>
    consteval bool can_substitute(info templ, R&& arguments);
  template<reflection_range R = initializer_list<info>>
    consteval info substitute(info templ, R&& arguments);

  // [meta.reflection.result], expression result reflection
  template<class T>
    consteval info reflect_constant(T expr);
  template<class T>
    consteval info reflect_object(T& expr);
  template<class T>
    consteval info reflect_function(T& fn);

  // [meta.reflection.define.aggregate], class definition generation
  struct data_member_options;
  consteval info data_member_spec(info type, data_member_options options);
  consteval bool is_data_member_spec(info r);
  template<reflection_range R = initializer_list<info>>
    consteval info define_aggregate(info type_class, R&&);

  // associated with [meta.unary.cat], primary type categories
  consteval bool is_void_type(info type);
  consteval bool is_null_pointer_type(info type);
  consteval bool is_integral_type(info type);
  consteval bool is_floating_point_type(info type);
  consteval bool is_array_type(info type);
  consteval bool is_pointer_type(info type);
  consteval bool is_lvalue_reference_type(info type);
  consteval bool is_rvalue_reference_type(info type);
  consteval bool is_member_object_pointer_type(info type);
  consteval bool is_member_function_pointer_type(info type);
  consteval bool is_enum_type(info type);
  consteval bool is_union_type(info type);
  consteval bool is_class_type(info type);
  consteval bool is_function_type(info type);
  consteval bool is_reflection_type(info type);

  // associated with [meta.unary.comp], composite type categories
  consteval bool is_reference_type(info type);
  consteval bool is_arithmetic_type(info type);
  consteval bool is_fundamental_type(info type);
  consteval bool is_object_type(info type);
  consteval bool is_scalar_type(info type);
  consteval bool is_compound_type(info type);
  consteval bool is_member_pointer_type(info type);

  // associated with [meta.unary.prop], type properties
  consteval bool is_const_type(info type);
  consteval bool is_volatile_type(info type);
  consteval bool is_trivially_copyable_type(info type);
  consteval bool is_trivially_relocatable_type(info type);
  consteval bool is_replaceable_type(info type);
  consteval bool is_standard_layout_type(info type);
  consteval bool is_empty_type(info type);
  consteval bool is_polymorphic_type(info type);
  consteval bool is_abstract_type(info type);
  consteval bool is_final_type(info type);
  consteval bool is_aggregate_type(info type);
  consteval bool is_consteval_only_type(info type);
  consteval bool is_signed_type(info type);
  consteval bool is_unsigned_type(info type);
  consteval bool is_bounded_array_type(info type);
  consteval bool is_unbounded_array_type(info type);
  consteval bool is_scoped_enum_type(info type);

  template<reflection_range R = initializer_list<info>>
    consteval bool is_constructible_type(info type, R&& type_args);
  consteval bool is_default_constructible_type(info type);
  consteval bool is_copy_constructible_type(info type);
  consteval bool is_move_constructible_type(info type);

  consteval bool is_assignable_type(info type_dst, info type_src);
  consteval bool is_copy_assignable_type(info type);
  consteval bool is_move_assignable_type(info type);

  consteval bool is_swappable_with_type(info type1, info type2);
  consteval bool is_swappable_type(info type);

  consteval bool is_destructible_type(info type);

  template<reflection_range R = initializer_list<info>>
    consteval bool is_trivially_constructible_type(info type, R&& type_args);
  consteval bool is_trivially_default_constructible_type(info type);
  consteval bool is_trivially_copy_constructible_type(info type);
  consteval bool is_trivially_move_constructible_type(info type);

  consteval bool is_trivially_assignable_type(info type_dst, info type_src);
  consteval bool is_trivially_copy_assignable_type(info type);
  consteval bool is_trivially_move_assignable_type(info type);
  consteval bool is_trivially_destructible_type(info type);

  template<reflection_range R = initializer_list<info>>
    consteval bool is_nothrow_constructible_type(info type, R&& type_args);
  consteval bool is_nothrow_default_constructible_type(info type);
  consteval bool is_nothrow_copy_constructible_type(info type);
  consteval bool is_nothrow_move_constructible_type(info type);

  consteval bool is_nothrow_assignable_type(info type_dst, info type_src);
  consteval bool is_nothrow_copy_assignable_type(info type);
  consteval bool is_nothrow_move_assignable_type(info type);

  consteval bool is_nothrow_swappable_with_type(info type1, info type2);
  consteval bool is_nothrow_swappable_type(info type);

  consteval bool is_nothrow_destructible_type(info type);
  consteval bool is_nothrow_relocatable_type(info type);

  consteval bool is_implicit_lifetime_type(info type);

  consteval bool has_virtual_destructor(info type);

  consteval bool has_unique_object_representations(info type);

  consteval bool reference_constructs_from_temporary(info type_dst, info type_src);
  consteval bool reference_converts_from_temporary(info type_dst, info type_src);

  // associated with [meta.unary.prop.query], type property queries
  consteval size_t rank(info type);
  consteval size_t extent(info type, unsigned i = 0);

  // associated with [meta.rel], type relations
  consteval bool is_same_type(info type1, info type2);
  consteval bool is_base_of_type(info type_base, info type_derived);
  consteval bool is_virtual_base_of_type(info type_base, info type_derived);
  consteval bool is_convertible_type(info type_src, info type_dst);
  consteval bool is_nothrow_convertible_type(info type_src, info type_dst);
  consteval bool is_layout_compatible_type(info type1, info type2);
  consteval bool is_pointer_interconvertible_base_of_type(info type_base, info type_derived);

  template<reflection_range R = initializer_list<info>>
    consteval bool is_invocable_type(info type, R&& type_args);
  template<reflection_range R = initializer_list<info>>
    consteval bool is_invocable_r_type(info type_result, info type, R&& type_args);

  template<reflection_range R = initializer_list<info>>
    consteval bool is_nothrow_invocable_type(info type, R&& type_args);
  template<reflection_range R = initializer_list<info>>
    consteval bool is_nothrow_invocable_r_type(info type_result, info type, R&& type_args);

  // associated with [meta.trans.cv], const-volatile modifications
  consteval info remove_const(info type);
  consteval info remove_volatile(info type);
  consteval info remove_cv(info type);
  consteval info add_const(info type);
  consteval info add_volatile(info type);
  consteval info add_cv(info type);

  // associated with [meta.trans.ref], reference modifications
  consteval info remove_reference(info type);
  consteval info add_lvalue_reference(info type);
  consteval info add_rvalue_reference(info type);

  // associated with [meta.trans.sign], sign modifications
  consteval info make_signed(info type);
  consteval info make_unsigned(info type);

  // associated with [meta.trans.arr], array modifications
  consteval info remove_extent(info type);
  consteval info remove_all_extents(info type);

  // associated with [meta.trans.ptr], pointer modifications
  consteval info remove_pointer(info type);
  consteval info add_pointer(info type);

  // associated with [meta.trans.other], other transformations
  consteval info remove_cvref(info type);
  consteval info decay(info type);
  template<reflection_range R = initializer_list<info>>
    consteval info common_type(R&& type_args);
  template<reflection_range R = initializer_list<info>>
    consteval info common_reference(R&& type_args);
  consteval info underlying_type(info type);
  template<reflection_range R = initializer_list<info>>
    consteval info invoke_result(info type, R&& type_args);
  consteval info unwrap_reference(info type);
  consteval info unwrap_ref_decay(info type);

  consteval size_t tuple_size(info type);
  consteval info tuple_element(size_t index, info type);

  consteval size_t variant_size(info type);
  consteval info variant_alternative(size_t index, info type);

  consteval strong_ordering type_order(info type_a, info type_b);
}
```

Unless otherwise specified, each function, and each specialization of
any function template, specified in this header is a designated
addressable function [[namespace.std]].

The behavior of any function specified in namespace `std::meta` is
*implementation-defined* when a reflection of a construct not otherwise
specified by this document is provided as an argument.

[*Note 1*: Values of type `std::meta::info` can represent
implementation-specific constructs [[basic.fundamental]]. — *end note*\]

[*Note 2*:

Many of the functions specified in namespace `std::meta` have semantics
that can be affected by the completeness of class types represented by
reflection values. For such functions, for any reflection `r` such that
`dealias(r)` represents a specialization of a templated class with a
reachable definition, the specialization is implicitly instantiated
[[temp.inst]].

[*Example 1*:

``` cpp
template<class T>
struct X {
  T mem;
};

static_assert(size_of(^^X<int>) == sizeof(int));    // instantiates X<int>
```

— *end example*\]

— *end note*\]

Any function in namespace `std::meta` whose return type is `string_view`
or `u8string_view` returns an object *V* such that `V.data()[V.size()]`
equals `'\0'`.

[*Example 2*:

``` cpp
struct C { };

constexpr string_view sv = identifier_of(^^C);
static_assert(sv == "C");
static_assert(sv.data()[0] == 'C');
static_assert(sv.data()[1] == '{}0');
```

— *end example*\]

For the purpose of exposition, throughout this clause `^^E` is used to
indicate a reflection representing source construct `E`.

### Checking string literals <a id="meta.string.literal">[[meta.string.literal]]</a>

``` cpp
consteval bool is_string_literal(const char* p);
consteval bool is_string_literal(const wchar_t* p);
consteval bool is_string_literal(const char8_t* p);
consteval bool is_string_literal(const char16_t* p);
consteval bool is_string_literal(const char32_t* p);
```

*Returns:*

- If `p` points to an unspecified object [[expr.const]], `false`.
- Otherwise, if `p` points to a subobject of a string literal
  object [[lex.string]], `true`.
- Otherwise, `false`.

### Promoting to static storage <a id="meta.define.static">[[meta.define.static]]</a>

The functions in this subclause promote compile-time storage into static
storage.

``` cpp
template<ranges::input_range R>
  consteval info reflect_constant_string(R&& r);
```

Let `CharT` be `ranges::range_value_t<R>`.

*Mandates:* `CharT` is one of `char`, `wchar_t`, `char8_t`, `char16_t`,
`char32_t`.

Let V be the pack of values of type `CharT` whose elements are the
corresponding elements of `r`, except that if `r` refers to a string
literal object, then V does not include the trailing null terminator of
`r`.

Let P be the template parameter object [[temp.param]] of type
`const CharT[sizeof...(V) + 1]` initialized with `{`V`..., CharT()}`.

*Returns:* .

[*Note 1*: P is a potentially non-unique
object [[intro.object]]. — *end note*\]

``` cpp
template<ranges::input_range R>
  consteval info reflect_constant_array(R&& r);
```

Let `T` be `ranges::range_value_t<R>`.

*Mandates:* `T` is a structural type [[temp.param]],
`is_constructible_v<T, ranges::range_reference_t<R>>` is `true`, and
`is_copy_constructible_v<T>` is `true`.

Let V be the pack of values of type `info` of the same size as `r`,
where the iᵗʰ element is `reflect_constant(``eᵢ``)`, where `eᵢ` is the
iᵗʰ element of `r`.

Let P be

- If `sizeof...(`V`) > 0` is `true`, then the template parameter
  object [[temp.param]] of type `const T[sizeof...(`V`)]` initialized
  with `{[:`V`:]...}`.
- Otherwise, the template parameter object of type `const array<T, 0>`
  initialized with `{}`.

*Returns:* .

*Throws:* `meta::exception` unless `reflect_constant(e)` is a constant
subexpression for every element `e` of `r`.

[*Note 2*: P is a potentially non-unique
object [[intro.object]]. — *end note*\]

``` cpp
template<ranges::input_range R>
  consteval const ranges::range_value_t<R>* define_static_string(R&& r);
```

*Effects:* Equivalent to:

``` cpp
return meta::extract<const ranges::range_value_t<R>*>(meta::reflect_constant_string(r));
```

``` cpp
template<ranges::input_range R>
  consteval span<const ranges::range_value_t<R>> define_static_array(R&& r);
```

*Effects:* Equivalent to:

``` cpp
using T = ranges::range_value_t<R>;
meta::info array = meta::reflect_constant_array(r);
if (meta::is_array_type(meta::type_of(array))) {
  return span<const T>(meta::extract<const T*>(array), meta::extent(meta::type_of(array)));
} else {
  return span<const T>();
}
```

``` cpp
template<class T>
  consteval const remove_cvref_t<T>* define_static_object(T&& t);
```

*Effects:* Equivalent to:

``` cpp
using U = remove_cvref_t<T>;
if constexpr (meta::is_class_type(^^U)) {
  return addressof(meta::extract<const U&>(meta::reflect_constant(std::forward<T>(t))));
} else {
  return define_static_array(span(addressof(t), 1)).data();
}
```

[*Note 3*: For class types, `define_static_object` provides the address
of the template parameter object [[temp.param]] that is
template-argument equivalent to `t`. — *end note*\]

### Class `exception` <a id="meta.reflection.exception">[[meta.reflection.exception]]</a>

``` cpp
namespace std::meta {
  class exception : public std::exception {
  private:
    optional<string> what_;     // exposition only
    u8string u8what_;           // exposition only
    info from_;                 // exposition only
    source_location where_;     // exposition only

  public:
    consteval exception(u8string_view what, info from,
                        source_location where = source_location::current()) noexcept;

    consteval exception(string_view what, info from,
                        source_location where = source_location::current()) noexcept;

    exception(const exception&) = default;
    exception(exception&&) = default;

    exception& operator=(const exception&) = default;
    exception& operator=(exception&&) = default;

    constexpr const char* what() const noexcept override;
    consteval u8string_view u8what() const noexcept;
    consteval info from() const noexcept;
    consteval source_location where() const noexcept;
  };
}
```

Reflection functions throw exceptions of type `meta::exception` to
signal an error. `meta::exception` is a consteval-only type.

``` cpp
consteval exception(u8string_view what, info from,
                    source_location where = source_location::current()) noexcept;
```

*Effects:* Initializes *u8what\_* with `what`, *from\_* with `from`, and
*where\_* with `where`. If `what` can be represented in the ordinary
literal encoding, initializes *what\_* with `what`, transcoded from
UTF-8 to the ordinary literal encoding. Otherwise, *what\_* is
value-initialized.

``` cpp
consteval exception(string_view what, info from,
                    source_location where = source_location::current()) noexcept;
```

`what` designates a sequence of characters that can be encoded in UTF-8.

*Effects:* Initializes *what\_* with `what`, *u8what\_* with `what`
transcoded from the ordinary literal encoding to UTF-8, *from\_* with
`from` and *where\_* with `where`.

``` cpp
constexpr const char* what() const noexcept override;
```

*`what_`*`.has_value()` is `true`.

*Returns:* *`what_`*`->c_str()`.

``` cpp
consteval u8string_view u8what() const noexcept;
```

*Returns:* *u8what\_*.

``` cpp
consteval info from() const noexcept;
```

*Returns:* *from\_*.

``` cpp
consteval source_location where() const noexcept;
```

*Returns:* *where\_*.

### Operator representations <a id="meta.reflection.operators">[[meta.reflection.operators]]</a>

``` cpp
enum class operators {
  see below;
};
using enum operators;
```

The enumeration type `operators` specifies constants used to identify
operators that can be overloaded, with the meanings listed
in  [[meta.reflection.operators]]. The values of the constants are
distinct.

**Table: Enum class `operators`**

| Constant                    | Corresponding *operator-function-id* | Operator symbol name |
| --------------------------- | ------------------------------------ | -------------------- |
| `op_new`                    | `operator new`                       | `new`                |
| `op_delete`                 | `operator delete`                    | `delete`             |
| `op_array_new`              | `operator new[]`                     | `new[]`              |
| `op_array_delete`           | `operator delete[]`                  | `delete[]`           |
| `op_co_await`               | `operator co_await`                  | `co_await`           |
| `op_parentheses`            | `operator()`                         | `()`                 |
| `op_square_brackets`        | `operator[]`                         | `[]`                 |
| `op_arrow`                  | `operator->`                         | `->`                 |
| `op_arrow_star`             | `operator->*`                        | `->*`                |
| `op_tilde`                  | `operator\~`                         | `\~`                 |
| `op_exclamation`            | `operator!`                          | `!`                  |
| `op_plus`                   | `operator+`                          | `+`                  |
| `op_minus`                  | `operator-`                          | `-`                  |
| `op_star`                   | `operator*`                          | `*`                  |
| `op_slash`                  | `operator/`                          | `/`                  |
| `op_percent`                | `operator%`                          | `%`                  |
| `op_caret`                  | `operator^`                          | `^`                  |
| `op_ampersand`              | `operator&`                          | `&`                  |
| `op_equals`                 | `operator=`                          | `=`                  |
| `op_pipe`                   | `operator|`                          | `|`                  |
| `op_plus_equals`            | `operator+=`                         | `+=`                 |
| `op_minus_equals`           | `operator-=`                         | `-=`                 |
| `op_star_equals`            | `operator*=`                         | `*=`                 |
| `op_slash_equals`           | `operator/=`                         | `/=`                 |
| `op_percent_equals`         | `operator%=`                         | `%=`                 |
| `op_caret_equals`           | `operator^=`                         | `^=`                 |
| `op_ampersand_equals`       | `operator&=`                         | `&=`                 |
| `op_pipe_equals`            | `operator|=`                         | `|=`                 |
| `op_equals_equals`          | `operator==`                         | `==`                 |
| `op_exclamation_equals`     | `operator!=`                         | `!=`                 |
| `op_less`                   | `operator<`                          | `<`                  |
| `op_greater`                | `operator>`                          | `>`                  |
| `op_less_equals`            | `operator<=`                         | `<=`                 |
| `op_greater_equals`         | `operator>=`                         | `>=`                 |
| `op_spaceship`              | `operator<=>`                        | `<=>`                |
| `op_ampersand_ampersand`    | `operator&&`                         | `&&`                 |
| `op_pipe_pipe`              | `operator||`                         | `||`                 |
| `op_less_less`              | `operator<<`                         | `<<`                 |
| `op_greater_greater`        | `operator>>`                         | `>>`                 |
| `op_less_less_equals`       | `operator<<=`                        | `<<=`                |
| `op_greater_greater_equals` | `operator>>=`                        | `>>=`                |
| `op_plus_plus`              | `operator++`                         | `++`                 |
| `op_minus_minus`            | `operator--`                         | `--`                 |
| `op_comma`                  | `operator,`                          | `,`                  |

``` cpp
consteval operators operator_of(info r);
```

*Returns:* The value of the enumerator from `operators` whose
corresponding *operator-function-id* is the unqualified name of the
entity represented by `r`.

*Throws:* `meta::exception` unless `r` represents an operator function
or operator function template.

``` cpp
consteval string_view symbol_of(operators op);
consteval u8string_view u8symbol_of(operators op);
```

*Returns:* A `string_view` or `u8string_view` containing the characters
of the operator symbol name corresponding to `op`, respectively encoded
with the ordinary literal encoding or with UTF-8.

*Throws:* `meta::exception` unless the value of `op` corresponds to one
of the enumerators in `operators`.

### Reflection names and locations <a id="meta.reflection.names">[[meta.reflection.names]]</a>

``` cpp
consteval bool has_identifier(info r);
```

*Returns:*

- If `r` represents an entity that has a typedef name for linkage
  purposes [[dcl.typedef]], then `true`.
- Otherwise, if `r` represents an unnamed entity, then `false`.
- Otherwise, if `r` represents a class type, then
  `!has_template_arguments(r)`.
- Otherwise, if `r` represents a function, then `true` if
  `has_template_arguments(r)` is `false` and the function is not a
  constructor, destructor, operator function, or conversion function.
  Otherwise, `false`.
- Otherwise, if `r` represents a template, then `true` if `r` does not
  represent a constructor template, operator function template, or
  conversion function template. Otherwise, `false`.
- Otherwise, if `r` represents the iᵗʰ parameter of a function F that is
  an (implicit or explicit) specialization of a templated function T and
  the iᵗʰ parameter of the instantiated declaration of T whose template
  arguments are those of F would be instantiated from a pack, then
  `false`.
- Otherwise, if `r` represents the parameter P of a function F, then let
  S be the set of declarations, ignoring any explicit instantiations,
  that precede some point in the evaluation context and that declare
  either F or a templated function of which F is a specialization;
  `true` if
  - there is a declaration D in S that introduces a name N for either P
    or the parameter corresponding to P in the templated function that D
    declares and
  - no declaration in S does so using any name other than N.

  Otherwise, `false`.
  \[*Example 2*:
      void fun(int);
      constexpr std::meta::info r = parameters_of(^^fun)[0];
      static_assert(!has_identifier(r));

      void fun(int x);
      static_assert(has_identifier(r));

      void fun(int x);
      static_assert(has_identifier(r));

      void poison() {
        void fun(int y);
      }
      static_assert(!has_identifier(r));

  — *end example*\]
- Otherwise, if `r` represents a variable, then `false` if the
  declaration of that variable was instantiated from a function
  parameter pack. Otherwise, `!has_template_arguments(r)`.
- Otherwise, if `r` represents a structured binding, then `false` if the
  declaration of that structured binding was instantiated from a
  structured binding pack. Otherwise, `true`.
- Otherwise, if `r` represents a type alias, then
  `!has_template_arguments(r)`.
- Otherwise, if `r` represents an enumerator, non-static-data member,
  namespace, or namespace alias, then `true`.
- Otherwise, if `r` represents a direct base class relationship, then
  `has_identifier(type_of(r))`.
- Otherwise, `r` represents a data member description
  (T, N, A, W, *NUA*)[[class.mem.general]]; `true` if N is not $\bot$.
  Otherwise, `false`.

``` cpp
consteval string_view identifier_of(info r);
consteval u8string_view u8identifier_of(info r);
```

Let E be UTF-8 for `u8identifier_of`, and otherwise the ordinary literal
encoding.

*Returns:* An NTMBS, encoded with E, determined as follows:

- If `r` represents an entity with a typedef name for linkage purposes,
  then that name.
- Otherwise, if `r` represents a literal operator or literal operator
  template, then the *ud-suffix* of the operator or operator template.
- Otherwise, if `r` represents the parameter P of a function F, then let
  S be the set of declarations, ignoring any explicit instantiations,
  that precede some point in the evaluation context and that declare
  either F or a templated function of which F is a specialization; the
  name that was introduced by a declaration in S for the parameter
  corresponding to P.
- Otherwise, if `r` represents an entity, then the identifier introduced
  by the declaration of that entity.
- Otherwise, if `r` represents a direct base class relationship, then
  `identifier_of(type_of(r))` or `u8identifier_of(type_of(r))`,
  respectively.
- Otherwise, `r` represents a data member description
  (T, N, A, W, NUA)[[class.mem.general]]; a `string_view` or
  `u8string_view`, respectively, containing the identifier N.

*Throws:* `meta::exception` unless `has_identifier(r)` is `true` and the
identifier that would be returned (see above) is representable by E.

``` cpp
consteval string_view display_string_of(info r);
consteval u8string_view u8display_string_of(info r);
```

*Returns:* An *implementation-defined* `string_view` or `u8string_view`,
respectively.

*Recommended practice:* Where possible, implementations should return a
string suitable for identifying the represented construct.

``` cpp
consteval source_location source_location_of(info r);
```

*Returns:* If `r` represents a value, a type other than a class type or
an enumeration type, the global namespace, or a data member description,
then `source_location{}`. Otherwise, an *implementation-defined*
`source_location` value.

*Recommended practice:* If `r` represents an entity with a definition
that is reachable from the evaluation context, a value corresponding to
a definition should be returned.

### Reflection queries <a id="meta.reflection.queries">[[meta.reflection.queries]]</a>

``` cpp
consteval bool has-type(info r);  // exposition only
```

*Returns:* `true` if `r` represents a value, annotation, object,
variable, function whose type does not contain an undeduced placeholder
type and that is not a constructor or destructor, enumerator, non-static
data member, unnamed bit-field, direct base class relationship, data
member description, or function parameter. Otherwise, `false`.

``` cpp
consteval info type_of(info r);
```

*Returns:*

- If `r` represents the iᵗʰ parameter of a function F, then the iᵗʰ type
  in the parameter-type-list of F[[dcl.fct]].
- Otherwise, if `r` represents a value, object, variable, function,
  non-static data member, or unnamed bit-field, then the type of what is
  represented by `r`.
- Otherwise, if `r` represents an annotation, then
  `type_of(constant_of(r))`.
- Otherwise, if `r` represents an enumerator N of an enumeration E,
  then:
  - If E is defined by a declaration D that precedes a point P in the
    evaluation context and P does not occur within an *enum-specifier*
    of D, then a reflection of E.
  - Otherwise, a reflection of the type of N prior to the closing brace
    of the *enum-specifier* as specified in  [[dcl.enum]].
- Otherwise, if `r` represents a direct base class relationship (D, B),
  then a reflection of B.
- Otherwise, for a data member description
  (T, N, A, W, *NUA*)[[class.mem.general]], a reflection of the type T.

*Throws:* `meta::exception` unless *`has-type`*`(r)` is `true`.

``` cpp
consteval info object_of(info r);
```

*Returns:*

- If `r` represents an object, then `r`.
- Otherwise, if `r` represents a reference, then a reflection of the
  object referred to by that reference.
- Otherwise, `r` represents a variable; a reflection of the object
  declared by that variable.

*Throws:* `meta::exception` unless `r` is a reflection representing
either

- an object with static storage duration [[basic.stc.general]], or
- a variable that either declares or refers to such an object, and if
  that variable is a reference R, then either
  - R is usable in constant expressions [[expr.const]], or
  - the lifetime of R began within the core constant expression
    currently under evaluation.

[*Example 1*:

``` cpp
int x;
int& y = x;

static_assert(^^x != ^^y);                          // OK, r and y are different variables so their
                                                    // reflections compare different
static_assert(object_of(^^x) == object_of(^^y));    // OK, because y is a reference
                                                    // to x, their underlying objects are the same
```

— *end example*\]

``` cpp
consteval info constant_of(info r);
```

Let R be a constant expression of type `info` such that R` == r` is
`true`. If `r` represents an annotation, then let C be its underlying
constant.

*Effects:* Equivalent to:

``` cpp
if constexpr (is_annotation($R$)) {
  return $C$;
} else {
  return reflect_constant([: $R$ :]);
}
```

*Throws:* `meta::exception` unless either `r` represents an annotation
or `[: `R` :]` is a valid *splice-expression*[[expr.prim.splice]].

[*Example 2*:

``` cpp
constexpr int x = 0;
constexpr int y = 0;

static_assert(^^x != ^^y);                      // OK, x and y are different variables,
                                                // so their reflections compare different
static_assert(constant_of(^^x) ==
              constant_of(^^y));                // OK, both constant_of(\reflexpr{x)} and
                                                // constant_of(\reflexpr{y)} represent the value 0
static_assert(constant_of(^^x) ==
              reflect_constant(0));             // OK, likewise

struct S { int m; };
constexpr S s {42};
static_assert(is_object(constant_of(^^s)) &&
              is_object(reflect_object(s)));
static_assert(constant_of(^^s) !=       // OK, template parameter object that is template-argument-
              reflect_object(s));       // equivalent to s is a different object than s
static_assert(constant_of(^^s) ==
              constant_of(reflect_object(s)));  // OK

consteval info fn() {
  constexpr int x = 42;
  return ^^x;
}
constexpr info r = constant_of(fn());           // error: x is outside its lifetime
```

— *end example*\]

``` cpp
consteval bool is_public(info r);
consteval bool is_protected(info r);
consteval bool is_private(info r);
```

*Returns:* `true` if `r` represents either

- a class member or unnamed bit-field that is public, protected, or
  private, respectively, or
- a direct base class relationship (D, B) for which B is, respectively,
  a public, protected, or private base class of D.

Otherwise, `false`.

``` cpp
consteval bool is_virtual(info r);
```

*Returns:* `true` if `r` represents either a virtual member function or
a direct base class relationship (D, B) for which B is a virtual base
class of D. Otherwise, `false`.

``` cpp
consteval bool is_pure_virtual(info r);
consteval bool is_override(info r);
```

*Returns:* `true` if `r` represents a member function that is pure
virtual or overrides another member function, respectively. Otherwise,
`false`.

``` cpp
consteval bool is_final(info r);
```

*Returns:* `true` if `r` represents a final class or a final member
function. Otherwise, `false`.

``` cpp
consteval bool is_deleted(info r);
consteval bool is_defaulted(info r);
```

*Returns:* `true` if `r` represents a function that is a deleted
function [[dcl.fct.def.delete]] or defaulted
function [[dcl.fct.def.default]], respectively. Otherwise, `false`.

``` cpp
consteval bool is_user_provided(info r);
consteval bool is_user_declared(info r);
```

*Returns:* `true` if `r` represents a function that is user-provided or
user-declared [[dcl.fct.def.default]], respectively. Otherwise, `false`.

``` cpp
consteval bool is_explicit(info r);
```

*Returns:* `true` if `r` represents a member function that is declared
explicit. Otherwise, `false`.

[*Note 1*: If `r` represents a member function template that is
declared explicit, `is_explicit(r)` is still `false` because in general,
such queries for templates cannot be answered. — *end note*\]

``` cpp
consteval bool is_noexcept(info r);
```

*Returns:* `true` if `r` represents a `noexcept` function type or a
function with a non-throwing exception specification [[except.spec]].
Otherwise, `false`.

[*Note 2*: If `r` represents a function template that is declared
`noexcept`, `is_noexcept(r)` is still `false` because in general, such
queries for templates cannot be answered. — *end note*\]

``` cpp
consteval bool is_bit_field(info r);
```

*Returns:* `true` if `r` represents a bit-field, or if `r` represents a
data member description (T, N, A, W, *NUA*)[[class.mem.general]] for
which W is not $\bot$. Otherwise, `false`.

``` cpp
consteval bool is_enumerator(info r);
consteval bool is_annotation(info r);
```

*Returns:* `true` if `r` represents an enumerator or annotation,
respectively. Otherwise, `false`.

``` cpp
consteval bool is_const(info r);
consteval bool is_volatile(info r);
```

Let T be `type_of(r)` if *`has-type`*`(r)` is `true`. Otherwise, let T
be `dealias(r)`.

*Returns:* `true` if `T` represents a const or volatile type,
respectively, or a const- or volatile-qualified function type,
respectively. Otherwise, `false`.

``` cpp
consteval bool is_mutable_member(info r);
```

*Returns:* `true` if `r` represents a `mutable` non-static data member.
Otherwise, `false`.

``` cpp
consteval bool is_lvalue_reference_qualified(info r);
consteval bool is_rvalue_reference_qualified(info r);
```

Let T be `type_of(r)` if *`has-type`*`(r)` is `true`. Otherwise, let T
be `dealias(r)`.

*Returns:* `true` if T represents an lvalue- or rvalue-qualified
function type, respectively. Otherwise, `false`.

``` cpp
consteval bool has_static_storage_duration(info r);
consteval bool has_thread_storage_duration(info r);
consteval bool has_automatic_storage_duration(info r);
```

*Returns:* `true` if `r` represents an object or variable that has
static, thread, or automatic storage duration,
respectively [[basic.stc]]. Otherwise, `false`.

[*Note 3*: It is not possible to have a reflection representing an
object or variable having dynamic storage duration. — *end note*\]

``` cpp
consteval bool has_internal_linkage(info r);
consteval bool has_module_linkage(info r);
consteval bool has_external_linkage(info r);
consteval bool has_c_language_linkage(info r);
consteval bool has_linkage(info r);
```

*Returns:* `true` if `r` represents a variable, function, type,
template, or namespace whose name has internal linkage, module linkage,
C language linkage, or any linkage, respectively [[basic.link]].
Otherwise, `false`.

``` cpp
consteval bool is_complete_type(info r);
```

*Returns:* `true` if `is_type(r)` is `true` and there is some point in
the evaluation context from which the type represented by `dealias(r)`
is not an incomplete type [[basic.types]]. Otherwise, `false`.

``` cpp
consteval bool is_enumerable_type(info r);
```

A type T is *enumerable* from a point P if either

- T is a class type complete at point P or
- T is an enumeration type defined by a declaration D such that D is
  reachable from P but P does not occur within an *enum-specifier* of
  D[[dcl.enum]].

*Returns:* `true` if `dealias(r)` represents a type that is enumerable
from some point in the evaluation context. Otherwise, `false`.

[*Example 3*:

``` cpp
class S;
enum class E;
static_assert(!is_enumerable_type(^^S));
static_assert(!is_enumerable_type(^^E));

class S {
  void mfn() {
    static_assert(is_enumerable_type(^^S));
  }
  static_assert(!is_enumerable_type(^^S));
};
static_assert(is_enumerable_type(^^S));

enum class E {
  A = is_enumerable_type(^^E) ? 1 : 2
};
static_assert(is_enumerable_type(^^E));
static_assert(static_cast<int>(E::A) == 2);
```

— *end example*\]

``` cpp
consteval bool is_variable(info r);
```

*Returns:* `true` if `r` represents a variable. Otherwise, `false`.

``` cpp
consteval bool is_type(info r);
consteval bool is_namespace(info r);
```

*Returns:* `true` if `r` represents an entity whose underlying entity is
a type or namespace, respectively. Otherwise, `false`.

``` cpp
consteval bool is_type_alias(info r);
consteval bool is_namespace_alias(info r);
```

*Returns:* `true` if `r` represents a type alias or namespace alias,
respectively. Otherwise, `false`.

[*Note 4*: A specialization of an alias template is a type
alias. — *end note*\]

``` cpp
consteval bool is_function(info r);
```

*Returns:* `true` if `r` represents a function. Otherwise, `false`.

``` cpp
consteval bool is_conversion_function(info r);
consteval bool is_operator_function(info r);
consteval bool is_literal_operator(info r);
```

*Returns:* `true` if `r` represents a function that is a conversion
function [[class.conv.fct]], operator function [[over.oper]], or literal
operator [[over.literal]], respectively. Otherwise, `false`.

``` cpp
consteval bool is_special_member_function(info r);
consteval bool is_constructor(info r);
consteval bool is_default_constructor(info r);
consteval bool is_copy_constructor(info r);
consteval bool is_move_constructor(info r);
consteval bool is_assignment(info r);
consteval bool is_copy_assignment(info r);
consteval bool is_move_assignment(info r);
consteval bool is_destructor(info r);
```

*Returns:* `true` if `r` represents a function that is a special member
function [[special]], a constructor, a default constructor, a copy
constructor, a move constructor, an assignment operator, a copy
assignment operator, a move assignment operator, or a destructor,
respectively. Otherwise, `false`.

``` cpp
consteval bool is_function_parameter(info r);
```

*Returns:* `true` if `r` represents a function parameter. Otherwise,
`false`.

``` cpp
consteval bool is_explicit_object_parameter(info r);
```

*Returns:* `true` if `r` represents a function parameter that is an
explicit object parameter [[dcl.fct]]. Otherwise, `false`.

``` cpp
consteval bool has_default_argument(info r);
```

*Returns:* If `r` represents a parameter P of a function F, then:

- If F is a specialization of a templated function T, then `true` if
  there exists a declaration D of T that precedes some point in the
  evaluation context and D specifies a default argument for the
  parameter of T corresponding to P. Otherwise, `false`.
- Otherwise, if there exists a declaration D of F that precedes some
  point in the evaluation context and D specifies a default argument for
  P, then `true`.

Otherwise, `false`.

``` cpp
consteval bool has_ellipsis_parameter(info r);
```

*Returns:* `true` if `r` represents a function or function type that has
an ellipsis in its parameter-type-list [[dcl.fct]]. Otherwise, `false`.

``` cpp
consteval bool is_template(info r);
```

*Returns:* `true` if `r` represents a function template, class template,
variable template, alias template, or concept. Otherwise, `false`.

[*Note 5*: A template specialization is not a template. For example,
`is_template(``)` is `true` but `is_template(``)` is
`false`. — *end note*\]

``` cpp
consteval bool is_function_template(info r);
consteval bool is_variable_template(info r);
consteval bool is_class_template(info r);
consteval bool is_alias_template(info r);
consteval bool is_conversion_function_template(info r);
consteval bool is_operator_function_template(info r);
consteval bool is_literal_operator_template(info r);
consteval bool is_constructor_template(info r);
consteval bool is_concept(info r);
```

*Returns:* `true` if `r` represents a function template, variable
template, class template, alias template, conversion function template,
operator function template, literal operator template, constructor
template, or concept, respectively. Otherwise, `false`.

``` cpp
consteval bool is_value(info r);
consteval bool is_object(info r);
```

*Returns:* `true` if `r` represents a value or object, respectively.
Otherwise, `false`.

``` cpp
consteval bool is_structured_binding(info r);
```

*Returns:* `true` if `r` represents a structured binding. Otherwise,
`false`.

``` cpp
consteval bool is_class_member(info r);
consteval bool is_namespace_member(info r);
consteval bool is_nonstatic_data_member(info r);
consteval bool is_static_member(info r);
consteval bool is_base(info r);
```

*Returns:* `true` if `r` represents a class member, namespace member,
non-static data member, static member, or direct base class
relationship, respectively. Otherwise, `false`.

``` cpp
consteval bool has_default_member_initializer(info r);
```

*Returns:* `true` if `r` represents a non-static data member that has a
default member initializer. Otherwise, `false`.

``` cpp
consteval bool has_parent(info r);
```

*Returns:*

- If `r` represents the global namespace, then `false`.
- Otherwise, if `r` represents an entity that has C language
  linkage [[dcl.link]], then `false`.
- Otherwise, if `r` represents an entity that has a language linkage
  other than C++ language linkage, then an *implementation-defined*
  value.
- Otherwise, if `r` represents a type that is neither a class nor
  enumeration type, then `false`.
- Otherwise, if `r` represents an entity or direct base class
  relationship, then `true`.
- Otherwise, `false`.

``` cpp
consteval info parent_of(info r);
```

*Returns:*

- If `r` represents a non-static data member that is a direct member of
  an anonymous union, or an unnamed bit-field declared within the
  *member-specification* of such a union, then a reflection representing
  the innermost enclosing anonymous union.
- Otherwise, if `r` represents an enumerator, then a reflection
  representing the corresponding enumeration type.
- Otherwise, if `r` represents a direct base class relationship (D, B),
  then a reflection representing D.
- Otherwise, let E be a class, function, or namespace whose class scope,
  function parameter scope, or namespace scope, respectively, is the
  innermost such scope that either is, or encloses, the target scope of
  a declaration of what is represented by `r`.
  - If E is the function call operator of a closure type for a
    *consteval-block-declaration*[[dcl.pre]], then
    `parent_of(parent_of(``))`. \[*Note 3*: In this case, the first
    `parent_of` will be the closure type, so the second `parent_of` is
    necessary to give the parent of that closure type. — *end note*\]
  - Otherwise, .

*Throws:* `meta::exception` unless `has_parent(r)` is `true`.

[*Example 4*:

``` cpp
struct I { };

struct F : I {
  union {
    int o;
  };

  enum N {
    A
  };
};

constexpr auto ctx = std::meta::access_context::current();

static_assert(parent_of(^^F) == ^^::);
static_assert(parent_of(bases_of(^^F, ctx)[0]) == ^^F);
static_assert(is_union_type(parent_of(^^F::o)));
static_assert(parent_of(^^F::N) == ^^F);
static_assert(parent_of(^^F::A) == ^^F::N);
```

— *end example*\]

``` cpp
consteval info dealias(info r);
```

*Returns:* A reflection representing the underlying entity of what `r`
represents.

*Throws:* `meta::exception` unless `r` represents an entity.

[*Example 5*:

``` cpp
using X = int;
using Y = X;
static_assert(dealias(^^int) == ^^int);
static_assert(dealias(^^X) == ^^int);
static_assert(dealias(^^Y) == ^^int);
```

— *end example*\]

``` cpp
consteval bool has_template_arguments(info r);
```

*Returns:* `true` if `r` represents a specialization of a function
template, variable template, class template, or an alias template.
Otherwise, `false`.

``` cpp
consteval info template_of(info r);
```

*Returns:* A reflection of the template of the specialization
represented by `r`.

*Throws:* `meta::exception` unless `has_template_arguments(r)` is
`true`.

``` cpp
consteval vector<info> template_arguments_of(info r);
```

*Returns:* A `vector` containing reflections of the template arguments
of the template specialization represented by `r`, in the order in which
they appear in the corresponding template argument list. For a given
template argument A, its corresponding reflection R is determined as
follows:

- If A denotes a type or type alias, then R is a reflection representing
  the underlying entity of A. \[*Note 4*: R always represents a type,
  never a type alias. — *end note*\]
- Otherwise, if A denotes a class template, variable template, concept,
  or alias template, then R is a reflection representing A.
- Otherwise, A is a constant template argument [[temp.arg.nontype]]. Let
  P be the corresponding template parameter.
  - If P has reference type, then R is a reflection representing the
    object or function referred to by A.
  - Otherwise, if P has class type, then R represents the corresponding
    template parameter object.
  - Otherwise, R is a reflection representing the value of A.

*Throws:* `meta::exception` unless `has_template_arguments(r)` is
`true`.

[*Example 6*:

``` cpp
template<class T, class U = T> struct Pair { };
template<class T> struct Pair<char, T> { };
template<class T> using PairPtr = Pair<T*>;

static_assert(template_of(^^Pair<int>) == ^^Pair);
static_assert(template_of(^^Pair<char, char>) == ^^Pair);
static_assert(template_arguments_of(^^Pair<int>).size() == 2);
static_assert(template_arguments_of(^^Pair<int>)[0] == ^^int);

static_assert(template_of(^^PairPtr<int>) == ^^PairPtr);
static_assert(template_arguments_of(^^PairPtr<int>).size() == 1);

struct S { };
int i;
template<int, int&, S, template<class> class>
  struct X { };
constexpr auto T = ^^X<1, i, S{}, PairPtr>;
static_assert(is_value(template_arguments_of(T)[0]));
static_assert(is_object(template_arguments_of(T)[1]));
static_assert(is_object(template_arguments_of(T)[2]));
static_assert(template_arguments_of(T)[3] == ^^PairPtr);
```

— *end example*\]

``` cpp
consteval vector<info> parameters_of(info r);
```

*Returns:*

- If `r` represents a function F, then a `vector` containing reflections
  of the parameters of F, in the order in which they appear in a
  declaration of F.
- Otherwise, `r` represents a function type T; a `vector` containing
  reflections of the types in parameter-type-list [[dcl.fct]] of T, in
  the order in which they appear in the parameter-type-list.

*Throws:* `meta::exception` unless `r` represents a function or a
function type.

``` cpp
consteval info variable_of(info r);
```

*Returns:* The reflection of the parameter variable corresponding to
`r`.

*Throws:* `meta::exception` unless

- `r` represents a parameter of a function F and
- there is a point P in the evaluation context for which the innermost
  non-block scope enclosing P is the function parameter
  scope [[basic.scope.param]] associated with F.

``` cpp
consteval info return_type_of(info r);
```

*Returns:* The reflection of the return type of the function or function
type represented by `r`.

*Throws:* `meta::exception` unless either `r` represents a function and
*`has-type`*`(r)` is `true` or `r` represents a function type.

### Access control context <a id="meta.reflection.access.context">[[meta.reflection.access.context]]</a>

The `access_context` class is a non-aggregate type that represents a
namespace, class, or function from which queries pertaining to access
rules may be performed, as well as the designating class
[[class.access.base]], if any.

An `access_context` has an associated scope and designating class.

``` cpp
namespace std::meta {
  struct access_context {
    access_context() = delete;

    consteval info scope() const;
    consteval info designating_class() const;

    static consteval access_context current() noexcept;
    static consteval access_context unprivileged() noexcept;
    static consteval access_context unchecked() noexcept;
    consteval access_context via(info cls) const;
  };
}
```

`access_context` is a structural type. Two values `ac1` and `ac2` of
type `access_context` are template-argument-equivalent [[temp.type]] if
`ac1.scope()` and `ac2.scope()` are template-argument-equivalent and
`ac1.designating_class()` and `ac2.designating_class()` are
template-argument-equivalent.

``` cpp
consteval info scope() const;
consteval info designating_class() const;
```

*Returns:* The `access_context`’s associated scope and designating
class, respectively.

``` cpp
static consteval access_context current() noexcept;
```

Given a program point P, let *`eval-point`*`(`P`)` be the following
program point:

- If a potentially-evaluated subexpression [[intro.execution]] of a
  default member initializer I for a member of class
  C[[class.mem.general]] appears at P, then a point determined as
  follows:
  - If an aggregate initialization is using I, *`eval-point`*`(`Q`)`,
    where Q is the point at which that aggregate initialization appears.
  - Otherwise, if an initialization by an inherited
    constructor [[class.inhctor.init]] is using I, a point whose
    immediate scope is the class scope corresponding to C.
  - Otherwise, a point whose immediate scope is the function parameter
    scope corresponding to the constructor definition that is using I.
- Otherwise, if a potentially-evaluated subexpression of a default
  argument [[dcl.fct.default]] appears at P, *`eval-point`*`(`Q`)`,
  where Q is the point at which the invocation of the
  function [[expr.call]] using that default argument appears.
- Otherwise, if the immediate scope of P is a function parameter scope
  introduced by a declaration D, and P appears either before the locus
  of D or within the trailing *requires-clause* of D, a point whose
  immediate scope is the innermost scope enclosing the locus of D that
  is not a template parameter scope.
- Otherwise, if the immediate scope of P is a function parameter scope
  introduced by a *lambda-expression* L whose *lambda-introducer*
  appears at point Q, and P appears either within the
  *trailing-return-type* or the trailing *requires-clause* of L,
  *`eval-point`*`(`Q`)`.
- Otherwise, if the innermost non-block scope enclosing P is the
  function parameter scope introduced by a
  *consteval-block-declaration*[[dcl.pre]], a point whose immediate
  scope is that inhabited by the outermost *consteval-block-declaration*
  D containing P such that each scope (if any) that intervenes between P
  and the function parameter scope introduced by D is either
  - a block scope or
  - a function parameter scope or lambda scope introduced by a
    *consteval-block-declaration*.
- Otherwise, P.

Given a scope S, let *`ctx-scope`*`(`S`)` be the following scope:

- If S is a class scope or namespace scope, S.
- Otherwise, if S is a function parameter scope introduced by the
  declaration of a function, S.
- Otherwise, if S is a lambda scope introduced by a *lambda-expression*
  L, the function parameter scope corresponding to the call operator of
  the closure type of L.
- Otherwise, *`ctx-scope`*`(`S'`)`, where S' is the parent scope of S.

*Returns:* An `access_context` whose designating class is the null
reflection and whose scope represents the function, class, or namespace
whose corresponding function parameter scope, class scope, or namespace
scope, respectively, is *`ctx-scope`*`(`S`)`, where S is the immediate
scope of *`eval-point`*`(`P`)` and P is the point at which the
invocation of `current` lexically appears.

*Remarks:* `current` is not an addressable function [[namespace.std]].
An invocation of `current` that appears at a program point P is
value-dependent [[temp.dep.constexpr]] if *`eval-point`*`(`P`)` is
enclosed by a scope corresponding to a templated entity.

[*Example 1*:

``` cpp
struct A {
  int a = 0;
  consteval A(int p) : a(p) {}
};
struct B : A {
  using A::A;
  consteval B(int p, int q) : A(p * q) {}
  info s = access_context::current().scope();
};
struct C : B { using B::B; };

struct Agg {
  consteval bool eq(info rhs = access_context::current().scope()) {
    return s == rhs;
  }
  info s = access_context::current().scope();
};

namespace NS {
  static_assert(Agg{}.s == access_context::current().scope());              // OK
  static_assert(Agg{}.eq());                                                // OK
  static_assert(B(1).s == ^^B);                                             // OK
  static_assert(is_constructor(B{1, 2}.s) && parent_of(B{1, 2}.s) == ^^B);  // OK
  static_assert(is_constructor(C{1, 2}.s) && parent_of(C{1, 2}.s) == ^^B);  // OK

  auto fn() -> [:is_namespace(access_context::current().scope()) ? ^^int : ^^bool:];
  static_assert(type_of(^^fn) == ^^auto()->int);                            // OK

  template<auto R>
    struct TCls {
      consteval bool fn()
        requires (is_type(access_context::current().scope())) {
          return true;                  // OK, scope is TCls<R>.
        }
    };
  static_assert(TCls<0>{}.fn());        // OK
}
```

— *end example*\]

``` cpp
static consteval access_context unprivileged() noexcept;
```

*Returns:* An `access_context` whose designating class is the null
reflection and whose scope is the global namespace.

``` cpp
static consteval access_context unchecked() noexcept;
```

*Returns:* An `access_context` whose designating class and scope are
both the null reflection.

``` cpp
consteval access_context via(info cls) const;
```

*Returns:* An `access_context` whose scope is `this->scope()` and whose
designating class is `cls`.

*Throws:* `meta::exception` unless `cls` is either the null reflection
or a reflection of a complete class type.

### Member accessibility queries <a id="meta.reflection.access.queries">[[meta.reflection.access.queries]]</a>

``` cpp
consteval bool is_accessible(info r, access_context ctx);
```

Let *`PARENT-CLS`*`(r)` be:

- If `parent_of(r)` represents a class C, then C.
- Otherwise, *`PARENT-CLS`*`(parent_of(r))`.

Let *`DESIGNATING-CLS`*`(r, ctx)` be:

- If `ctx.designating_class()` represents a class C, then C.
- Otherwise, *`PARENT-CLS`*`(r)`.

*Returns:*

- If `r` represents an unnamed bit-field F, then
  `is_accessible(``r_H``, ctx)`, where `r_H` represents a hypothetical
  non-static data member of the class represented by *`PARENT-CLS`*`(r)`
  with the same access as F. \[*Note 5*: Unnamed bit-fields are treated
  as class members for the purpose of `is_accessible`. — *end note*\]
- Otherwise, if `r` does not represent a class member or a direct base
  class relationship, then `true`.
- Otherwise, if `r` represents
  - a class member that is not a (possibly indirect or variant) member
    of *`DESIGNATING-CLS`*`(r, ctx)` or
  - a direct base class relationship such that `parent_of(r)` does not
    represent *`DESIGNATING-CLS`*`(r, ctx)` or a (direct or indirect)
    base class thereof,

  then `false`.
- Otherwise, if `ctx.scope()` is the null reflection, then `true`.
- Otherwise, letting P be a program point whose immediate scope is the
  function parameter scope, class scope, or namespace scope
  corresponding to the function, class, or namespace represented by
  `ctx.scope()`:
  - If `r` represents a direct base class relationship (D, B), then
    `true` if base class B of *`DESIGNATING-CLS`*`(r, ctx)` is
    accessible at P[[class.access.base]]; otherwise `false`.
  - Otherwise, `r` represents a class member M; `true` if M would be
    accessible at P with the designating class [[class.access.base]] as
    *`DESIGNATING-CLS`*`(r, ctx)` if the effect of any
    *using-declaration*s [[namespace.udecl]] were ignored. Otherwise,
    `false`.

[*Note 1*: The definitions of when a class member or base class is
accessible from a point P do not consider whether a declaration of that
entity is reachable from P. — *end note*\]

*Throws:* `meta::exception` if

- `r` represents a class member for which *`PARENT-CLS`*`(r)` is an
  incomplete class or
- `r` represents a direct base class relationship (D, B) for which D is
  incomplete.

[*Example 1*:

``` cpp
consteval access_context fn() {
  return access_context::current();
}

class Cls {
  int mem;
  friend consteval access_context fn();
public:
  static constexpr auto r = ^^mem;
};

static_assert(is_accessible(Cls::r, fn()));                             // OK
static_assert(!is_accessible(Cls::r, access_context::current()));       // OK
static_assert(is_accessible(Cls::r, access_context::unchecked()));      // OK
```

— *end example*\]

``` cpp
consteval bool has_inaccessible_nonstatic_data_members(info r, access_context ctx);
```

*Returns:* `true` if `is_accessible(`R`, ctx)` is `false` for any R in
`nonstatic_data_members_of(r, access_context::unchecked())`. Otherwise,
`false`.

*Throws:* `meta::exception` unless

- `nonstatic_data_members_of(r, access_context::unchecked())` is a
  constant subexpression and
- `r` does not represent a closure type.

``` cpp
consteval bool has_inaccessible_bases(info r, access_context ctx);
```

*Returns:* `true` if `is_accessible(`R`, ctx)` is `false` for any R in
`bases_of(r, access_context::unchecked())`. Otherwise, `false`.

*Throws:* `meta::exception` unless
`bases_of(r, access_context::unchecked())` is a constant subexpression.

``` cpp
consteval bool has_inaccessible_subobjects(info r, access_context ctx);
```

*Effects:* Equivalent to:

``` cpp
return has_inaccessible_bases(r, ctx) || has_inaccessible_nonstatic_data_members(r, ctx);
```

### Reflection member queries <a id="meta.reflection.member.queries">[[meta.reflection.member.queries]]</a>

``` cpp
consteval vector<info> members_of(info r, access_context ctx);
```

A declaration D *members-of-precedes* a point P if D precedes either P
or the point immediately following the *class-specifier* of the
outermost class for which P is in a complete-class context.

A declaration D of a member M of a class or namespace Q is
*Q-members-of-eligible* if

- the host scope of D[[basic.scope.scope]] is the class scope or
  namespace scope associated with Q,
- D is not a friend declaration,
- M is not a closure type [[expr.prim.lambda.closure]],
- M is not a specialization of a template [[temp.pre]],
- if Q is a class that is not a closure type, then M is a direct member
  of Q[[class.mem.general]] that is not a variant member of a nested
  anonymous union of Q[[class.union.anon]], and
- if Q is a closure type, then M is a function call operator or function
  call operator template.

It is *implementation-defined* whether declarations of other members of
a closure type Q are Q-members-of-eligible.

A member M of a class or namespace Q is *Q-members-of-representable*
from a point P if a Q-members-of-eligible declaration of M
members-of-precedes P, and M is

- a class or enumeration type,
- a type alias,
- a class template, function template, variable template, alias
  template, or concept,
- a variable or reference V for which the type of V does not contain an
  undeduced placeholder type,
- a function F for which
  - the type of F does not contain an undeduced placeholder type,
  - the constraints (if any) of F are satisfied, and
  - if F is a prospective destructor, F is the selected
    destructor [[class.dtor]],
- a non-static data member,
- a namespace, or
- a namespace alias.

[*Note 1*: Examples of direct members that are not
Q-members-of-representable for any entity Q include: unscoped
enumerators [[enum]], partial specializations of
templates [[temp.spec.partial]], and closure
types [[expr.prim.lambda.closure]]. — *end note*\]

*Returns:* A `vector` containing reflections of all members M of the
entity Q represented by `dealias(r)` for which

- M is Q-members-of-representable from some point in the evaluation
  context and
- `is_accessible(``, ctx)` is `true`.

If `dealias(r)` represents a class C, then the `vector` also contains
reflections representing all unnamed bit-fields B whose declarations
inhabit the class scope corresponding to C for which
`is_accessible(``, ctx)` is `true`. Reflections of class members and
unnamed bit-fields that are declared appear in the order in which they
are declared.

[*Note 2*: Base classes are not members. Implicitly-declared special
members appear after any user-declared
members [[special]]. — *end note*\]

*Throws:* `meta::exception` unless `dealias(r)` is a reflection
representing either a class type that is complete from some point in the
evaluation context or a namespace.

[*Example 1*:

``` cpp
// TU1
export module M;
namespace NS {
  export int m;
  static int l;
}
static_assert(members_of(^^NS, access_context::current()).size() == 2);

// TU2
import M;

static_assert(                                                  // NS::l does not precede
  members_of(^^NS, access_context::current()).size() == 1);     // the constant-expressionREF:basic.lookup

class B {};

struct S : B {
private:
  class I;
public:
  int m;
};

static_assert(                                                  // 6 special members,
  members_of(^^S, access_context::current()).size() == 7);      // 1 public member,
                                                                // does not include base

static_assert(                                                  // all of the above,
  members_of(^^S, access_context::unchecked()).size() == 8);    // as well as a reflection
                                                                // representing S::I
```

— *end example*\]

``` cpp
consteval vector<info> bases_of(info type, access_context ctx);
```

*Returns:* Let C be the class represented by `dealias(type)`. A `vector`
containing the reflections of all the direct base class relationships B,
if any, of C such that `is_accessible(``, ctx)` is `true`. The direct
base class relationships appear in the order in which the corresponding
base classes appear in the *base-specifier-list* of C.

*Throws:* `meta::exception` unless `dealias(type)` represents a class
type that is complete from some point in the evaluation context.

``` cpp
consteval vector<info> static_data_members_of(info type, access_context ctx);
```

*Returns:* A `vector` containing each element `e` of
`members_of(type, ctx)` such that `is_variable(e)` is `true`, preserving
their order.

*Throws:* `meta::exception` unless `dealias(type)` represents a class
type that is complete from some point in the evaluation context.

``` cpp
consteval vector<info> nonstatic_data_members_of(info type, access_context ctx);
```

*Returns:* A `vector` containing each element `e` of
`members_of(type, ctx)` such that `is_nonstatic_data_member(e)` is
`true`, preserving their order.

*Throws:* `meta::exception` unless `dealias(type)` represents a class
type that is complete from some point in the evaluation context.

``` cpp
consteval vector<info> subobjects_of(info type, access_context ctx);
```

*Returns:* A `vector` containing each element of `bases_of(type, ctx)`
followed by each element of `nonstatic_data_members_of(type, ctx)`,
preserving their order.

*Throws:* `meta::exception` unless `dealias(type)` represents a class
type that is complete from some point in the evaluation context.

``` cpp
consteval vector<info> enumerators_of(info type_enum);
```

*Returns:* A `vector` containing the reflections of each enumerator of
the enumeration represented by `dealias(type_enum)`, in the order in
which they are declared.

*Throws:* `meta::exception` unless `dealias(type_enum)` represents an
enumeration type, and `is_enumerable_type(type_enum)` is `true`.

### Reflection layout queries <a id="meta.reflection.layout">[[meta.reflection.layout]]</a>

``` cpp
struct member_offset {
  ptrdiff_t bytes;
  ptrdiff_t bits;
  constexpr ptrdiff_t total_bits() const;
  auto operator<=>(const member_offset&) const = default;
};

constexpr ptrdiff_t member_offset::total_bits() const;
```

*Returns:* `bytes * CHAR_BIT + bits`.

``` cpp
consteval member_offset offset_of(info r);
```

Let V be the offset in bits from the beginning of a complete object of
the type represented by `parent_of(r)` to the subobject associated with
the construct represented by `r`.

*Returns:* `{`V` / CHAR_BIT, `V` % CHAR_BIT}`.

*Throws:* `meta::exception` unless `r` represents a non-static data
member, unnamed bit-field, or direct base class relationship (D, B) for
which either B is not a virtual base class or D is not an abstract
class.

``` cpp
consteval size_t size_of(info r);
```

*Returns:* If

- `r` represents a non-static data member of type T or a data member
  description (T, N, A, W, *NUA*) or
- `dealias(r)` represents a type T,

then `sizeof(`T`)` if T is not a reference type and
`size_of(add_pointer(``))` otherwise. Otherwise, `size_of(type_of(r))`.

[*Note 1*: It is possible that while `sizeof(char) == size_of(``)` is
`true`, that `sizeof(char&) == size_of(``&)` is `false`. If `b`
represents a direct base class relationship of an empty base class, then
`size_of(b) > 0` is `true`. — *end note*\]

*Throws:* `meta::exception` unless all of the following conditions are
met:

- `dealias(r)` is a reflection of a type, object, value, variable of
  non-reference type, non-static data member that is not a bit-field,
  direct base class relationship, or data member description
  (T, N, A, W, *NUA*)[[class.mem.general]] where W is $\bot$.
- If `dealias(r)` represents a type, then `is_complete_type(r)` is
  `true`.

``` cpp
consteval size_t alignment_of(info r);
```

*Returns:*

- If `dealias(r)` represents a type T, then
  `alignment_of(add_pointer(r))` if T is a reference type and the
  alignment requirement of T otherwise.
- Otherwise, if `dealias(r)` represents a variable or object, then the
  alignment requirement of the variable or object.
- Otherwise, if `r` represents a direct base class relationship, then
  `alignment_of(type_of(r))`.
- Otherwise, if `r` represents a non-static data member M of a class C,
  then the alignment of the direct member subobject corresponding to M
  of a complete object of type C.
- Otherwise, `r` represents a data member description
  (T, N, A, W, *NUA*)[[class.mem.general]]. If A is not $\bot$, then the
  value A. Otherwise, `alignment_of(``)`.

*Throws:* `meta::exception` unless all of the following conditions are
met:

- `dealias(r)` is a reflection of a type, object, variable of
  non-reference type, non-static data member that is not a bit-field,
  direct base class relationship, or data member description.
- If `dealias(r)` represents a type, then `is_complete_type(r)` is
  `true`.

``` cpp
consteval size_t bit_size_of(info r);
```

*Returns:*

- If `r` represents an unnamed bit-field or a non-static data member
  that is a bit-field with width W, then W.
- Otherwise, if `r` represents a data member description
  (T, N, A, W, *NUA*)[[class.mem.general]] and W is not $\bot$, then W.
- Otherwise, `CHAR_BIT * size_of(r)`.

*Throws:* `meta::exception` unless all of the following conditions are
met:

- `dealias(r)` is a reflection of a type, object, value, variable of
  non-reference type, non-static data member, unnamed bit-field, direct
  base class relationship, or data member description.
- If `dealias(r)` represents a type, then `is_complete_type(r)` is
  `true`.

### Annotation reflection <a id="meta.reflection.annotation">[[meta.reflection.annotation]]</a>

``` cpp
consteval vector<info> annotations_of(info item);
```

Let E be

- the corresponding *base-specifier* if `item` represents a direct base
  class relationship,
- otherwise, the entity represented by `item`.

*Returns:* A `vector` containing all of the reflections R representing
each annotation applying to each declaration of E that precedes either
some point in the evaluation context [[expr.const]] or a point
immediately following the *class-specifier* of the outermost class for
which such a point is in a complete-class context. For any two
reflections R₁ and R₂ in the returned `vector`, if the annotation
represented by R₁ precedes the annotation represented by R₂, then R₁
appears before R₂. If R₁ and R₂ represent annotations from the same
translation unit T, any element in the returned `vector` between R₁ and
R₂ represents an annotation from T.

[*Note 1*: The order in which two annotations appear is otherwise
unspecified. — *end note*\]

*Throws:* `meta::exception` unless `item` represents a type, type alias,
variable, function, namespace, enumerator, direct base class
relationship, or non-static data member.

[*Example 1*:

``` cpp
[[=1]] void f();
[[=2, =3]] void g();
void g [[=4]] ();

static_assert(annotations_of(^^f).size() == 1);
static_assert(annotations_of(^^g).size() == 3);
static_assert([: constant_of(annotations_of(^^g)[0]) :] == 2);
static_assert(extract<int>(annotations_of(^^g)[1]) == 3);
static_assert(extract<int>(annotations_of(^^g)[2]) == 4);

struct Option { bool value; };

struct C {
  [[=Option{true}]] int a;
  [[=Option{false}]] int b;
};

static_assert(extract<Option>(annotations_of(^^C::a)[0]).value);
static_assert(!extract<Option>(annotations_of(^^C::b)[0]).value);

template<class T>
  struct [[=42]] D { };

constexpr std::meta::info a1 = annotations_of(^^D<int>)[0];
constexpr std::meta::info a2 = annotations_of(^^D<char>)[0];
static_assert(a1 != a2);
static_assert(constant_of(a1) == constant_of(a2));

[[=1]] int x, y;
static_assert(annotations_of(^^x)[0] == annotations_of(^^y)[0]);
```

— *end example*\]

``` cpp
consteval vector<info> annotations_of_with_type(info item, info type);
```

*Returns:* A `vector` containing each element `e` of
`annotations_of(item)` where

``` cpp
remove_const(type_of(e)) == remove_const(type)
```

is `true`, preserving their order.

*Throws:* `meta::exception` unless

- `annotations_of(item)` is a constant expression and
- `dealias(type)` represents a type and `is_complete_type(type)` is
  `true`.

### Value extraction <a id="meta.reflection.extract">[[meta.reflection.extract]]</a>

The `extract` function template may be used to extract a value out of a
reflection when its type is known.

The following are defined for exposition only to aid in the
specification of `extract`.

``` cpp
template<class T>
  consteval T extract-ref(info r);      // exposition only
```

[*Note 1*: `T` is a reference type. — *end note*\]

*Returns:* If `r` represents an object O, then a reference to O.
Otherwise, a reference to the object declared, or referred to, by the
variable represented by `r`.

*Throws:* `meta::exception` unless

- `r` represents a variable or object of type `U`,
- `is_convertible_v<remove_reference_t<U>(*)[], remove_reference_t<T>(*)[]>`
  is `true`,and \[*Note 6*: The intent is to allow only qualification
  conversion from `U` to `T`. — *end note*\]
- If `r` represents a variable, then either that variable is usable in
  constant expressions or its lifetime began within the core constant
  expression currently under evaluation.

``` cpp
template<class T>
  consteval T extract-member-or-function(info r);       // exposition only
```

*Returns:*

- If `T` is a pointer type, then a pointer value pointing to the
  function represented by `r`.
- Otherwise, a pointer-to-member value designating the non-static data
  member or function represented by `r`.

*Throws:* `meta::exception` unless

- `r` represents a non-static data member with type `X`, that is not a
  bit-field, that is a direct member of class `C`, `T` and `X C::*` are
  similar types [[conv.qual]], and `is_convertible_v<X C::*, T>` is
  `true`;
- `r` represents an implicit object member function with type `F` or
  `F noexcept` that is a direct member of a class `C`, and `T` is
  `F C::*`; or
- `r` represents a non-member function, static member function, or
  explicit object member function of function type `F` or `F noexcept`,
  and `T` is `F*`.

``` cpp
template<class T>
  consteval T extract-value(info r);    // exposition only
```

Let `U` be the type of the value or object that `r` represents.

*Returns:* `static_cast<T>([:`R`:])`, where R is a constant expression
of type `info` such that R` == r` is `true`.

*Throws:* `meta::exception` unless

- `U` is a pointer type, `T` and `U` are either similar [[conv.qual]] or
  both function pointer types, and `is_convertible_v<U, T>` is `true`,
- `U` is not a pointer type and the cv-unqualified types of `T` and `U`
  are the same,
- `U` is an array type, `T` is a pointer type, and the value `r`
  represents is convertible to `T`, or
- `U` is a closure type, `T` is a function pointer type, and the value
  that `r` represents is convertible to `T`.

``` cpp
template<class T>
  consteval T extract(info r);
```

Let `U` be `remove_cv_t<T>`.

*Effects:* Equivalent to:

``` cpp
if constexpr (is_reference_type(^^T)) {
  return extract-ref<T>(r);
} else if (is_nonstatic_data_member(r) || is_function(r)) {
  return extract-member-or-function<U>(r);
} else {
  return extract-value<U>(constant_of(r));
}
```

### Reflection substitution <a id="meta.reflection.substitute">[[meta.reflection.substitute]]</a>

``` cpp
template<class R>
concept reflection_range =
  ranges::input_range<R> &&
  same_as<ranges::range_value_t<R>, info> &&
  same_as<remove_cvref_t<ranges::range_reference_t<R>>, info>;

template<reflection_range R = initializer_list<info>>
  consteval bool can_substitute(info templ, R&& arguments);
```

Let `Z` be the template represented by `templ` and let `Args...` be a
sequence of prvalue constant expressions that compute the reflections
held by the elements of `arguments`, in order.

*Returns:* `true` if `Z<[:Args:]...>` is a valid
*template-id*[[temp.names]] that does not name a function whose type
contains an undeduced placeholder type. Otherwise, `false`.

*Throws:* `meta::exception` unless `templ` represents a template, and
every reflection in `arguments` represents a construct usable as a
template argument [[temp.arg]].

[*Note 1*: If forming `Z<[:Args:]...>` leads to a failure outside of
the immediate context, the program is ill-formed. — *end note*\]

``` cpp
template<reflection_range R = initializer_list<info>>
  consteval info substitute(info templ, R&& arguments);
```

Let `Z` be the template represented by `templ` and let `Args...` be a
sequence of prvalue constant expressions that compute the reflections
held by the elements of `arguments`, in order.

*Returns:* .

*Throws:* `meta::exception` unless `can_substitute(templ, arguments)` is
`true`.

[*Note 2*: If forming `Z<[:Args:]...>` leads to a failure outside of
the immediate context, the program is ill-formed. — *end note*\]

[*Example 1*:

``` cpp
template<class T>
  auto fn1();

static_assert(!can_substitute(^^fn1, {^^int}));         // OK
constexpr info r1 = substitute(^^fn1, {^^int});         // error: fn1<int> contains an undeduced
                                                        // placeholder type for its return type

template<class T>
  auto fn2() {
    static_assert(^^T != ^^int);    // static assertion failed during instantiation of fn2<int>
    return 0;
  }

constexpr bool r2 = can_substitute(^^fn2, {^^int});     // error: instantiation of body of fn2<int>
                                                        // is needed to deduce return type
```

— *end example*\]

[*Example 2*:

``` cpp
consteval info to_integral_constant(unsigned i) {
  return substitute(^^integral_constant, {^^unsigned, reflect_constant(i)});
}
constexpr info r = to_integral_constant(2);     // OK, r represents the type
                                                // integral_constant<unsigned, 2>
```

— *end example*\]

### Expression result reflection <a id="meta.reflection.result">[[meta.reflection.result]]</a>

``` cpp
template<class T>
  consteval info reflect_constant(T expr);
```

*Mandates:* `is_copy_constructible_v<T>` is `true` and `T` is a
cv-unqualified structural type [[temp.param]] that is not a reference
type.

Let V be:

- if `T` is a class type, then an object that is
  template-argument-equivalent to the value of `expr`;
- otherwise, the value of `expr`.

Let `TCls` be the invented template:

``` cpp
template<T P> struct TCls;
```

*Returns:* `template_arguments_of(``)[0]`.

[*Note 1*: This is a reflection of an object for class types, and a
reflection of a value otherwise. — *end note*\]

*Throws:* `meta::exception` unless the *template-id* `TCls<`V`>` would
be valid.

[*Example 1*:

``` cpp
template<auto D>
  struct A { };

struct N { int x; };
struct K { char const* p; };

constexpr info r1 = reflect_constant(42);
static_assert(is_value(r1));
static_assert(r1 == template_arguments_of(^^A<42>)[0]);

constexpr info r2 = reflect_constant(N{42});
static_assert(is_object(r2));
static_assert(r2 == template_arguments_of(^^A<N{42}>)[0]);

constexpr info r3 = reflect_constant(K{nullptr});   // OK
constexpr info r4 = reflect_constant(K{"ebab"});    // error: constituent pointer
                                                    // points to string literal
```

— *end example*\]

``` cpp
template<class T>
  consteval info reflect_object(T& expr);
```

*Mandates:* `T` is an object type.

*Returns:* A reflection of the object designated by `expr`.

*Throws:* `meta::exception` unless `expr` is suitable for use as a
constant template argument for a constant template parameter of type
`T&`[[temp.arg.nontype]].

``` cpp
template<class T>
  consteval info reflect_function(T& fn);
```

*Mandates:* `T` is a function type.

*Returns:* A reflection of the function designated by `fn`.

*Throws:* `meta::exception` unless `fn` is suitable for use as a
constant template argument for a constant template parameter of type
`T&`[[temp.arg.nontype]].

### Reflection class definition generation <a id="meta.reflection.define.aggregate">[[meta.reflection.define.aggregate]]</a>

``` cpp
namespace std::meta {
  struct data_member_options {
    struct name-type {                          // exposition only
      template<class T>
        requires constructible_from<u8string, T>
        consteval name-type(T&&);

      template<class T>
        requires constructible_from<string, T>
        consteval name-type(T&&);

    private:
      variant<u8string, string> contents;       // exposition only
    };

    optional<name-type> name;
    optional<int> alignment;
    optional<int> bit_width;
    bool no_unique_address = false;
  };
}
```

The classes `data_member_options` and `data_member_options::name-type`
are consteval-only types [[basic.types.general]], and are not structural
types [[temp.param]].

``` cpp
template<class T>
  requires constructible_from<u8string, T>
  consteval name-type(T&& value);
```

*Effects:* Initializes *contents* with
`u8string(std::forward<T>(value))`.

``` cpp
template<class T>
  requires constructible_from<string, T>
  consteval name-type(T&& value);
```

*Effects:* Initializes *contents* with `string(std::forward<T>(value))`.

[*Note 1*:

The class *name-type* allows the function `data_member_spec` to accept
an ordinary string literal (or `string_view`, `string`, etc.) or a UTF-8
string literal (or `u8string_view`, `u8string`, etc.) equally well.

[*Example 1*:

    consteval void fn() {
      data_member_options o1 = {.name = "ordinary_literal_encoding"};
      data_member_options o2 = {.name = u8"utf8_encoding"};
    }

— *end example*\]

— *end note*\]

``` cpp
consteval info data_member_spec(info type, data_member_options options);
```

*Returns:* A reflection of a data member description
(T, N, A, W, *NUA*)[[class.mem.general]] where

- T is the type represented by `dealias(type)`,
- N is either the identifier encoded by `options.name` or $\bot$ if
  `options.name` does not contain a value,
- A is either the alignment value held by `options.alignment` or $\bot$
  if `options.alignment` does not contain a value,
- W is either the value held by `options.bit_width` or $\bot$ if
  `options.bit_width` does not contain a value, and
- *NUA* is the value held by `options.no_unique_address`.

[*Note 2*: The returned reflection value is primarily useful in
conjunction with `define_aggregate`; it can also be queried by certain
other functions in `std::meta` (e.g., `type_of`,
`identifier_of`). — *end note*\]

*Throws:* `meta::exception` unless the following conditions are met:

- `dealias(type)` represents either an object type or a reference type;
- if `options.name` contains a value, then:
  - `holds_alternative<u8string>(options.name->`*`contents`*`)` is
    `true` and `get<u8string>(options.name->`*`contents`*`)` contains a
    valid identifier [[lex.name]] that is not a keyword [[lex.key]] when
    interpreted with UTF-8, or
  - `holds_alternative<string>(options.name->`*`contents`*`)` is `true`
    and `get<string>(options.name->`*`contents`*`)` contains a valid
    identifier [[lex.name]] that is not a keyword [[lex.key]] when
    interpreted with the ordinary literal encoding;

  \[*Note 7*: The name corresponds to the spelling of an
  identifier token after phase 6 of translation@@REF:lex.phases@@.
  Lexical constructs like
  *universal-character-name*s@@REF:lex.universal.char@@ are not
  processed and will cause evaluation to fail. For example,
  `R"(\u03B1)"` is an invalid identifier and is not interpreted as
  `"`α`"`. — *end note*\]
- if `options.name` does not contain a value, then `options.bit_width`
  contains a value;
- if `options.bit_width` contains a value V, then
  - `is_integral_type(type) || is_enum_type(type)` is `true`,
  - `options.alignment` does not contain a value,
  - `options.no_unique_address` is `false`, and
  - if V equals `0`, then `options.name` does not contain a value; and
- if `options.alignment` contains a value, it is an alignment
  value [[basic.align]] not less than `alignment_of(type)`.

``` cpp
consteval bool is_data_member_spec(info r);
```

*Returns:* `true` if `r` represents a data member description.
Otherwise, `false`.

``` cpp
template<reflection_range R = initializer_list<info>>
  consteval info define_aggregate(info class_type, R&& mdescrs);
```

Let C be the class represented by `class_type` and $r_K$ be the Kᵗʰ
reflection value in `mdescrs`. For every $r_K$ in `mdescrs`, let
$(T_K, N_K, A_K, W_K, *NUA*_K)$ be the corresponding data member
description represented by $r_K$.

- C is incomplete from every point in the evaluation context;
  \[*Note 8*: C can be a class template specialization for which there
  is a reachable definition of the class template. In this case, the
  injected declaration is an explicit specialization. — *end note*\]
- `is_data_member_spec(`$r_K$`)` is `true` for every $r_K$;
- `is_complete_type(`$T_K$`)` is `true` for every $r_K$; and
- for every pair $(r_K, r_L)$ where K < L, if $N_K$ is not $\bot$ and
  $N_L$ is not $\bot$, then either:
  - $N_K$` != `$N_L$ is `true` or
  - $N_K$` == u8"_"` is `true`. \[*Note 9*: Every provided identifier is
    unique or `"_"`. — *end note*\]

*Effects:* Produces an injected declaration D[[expr.const]] that defines
C and has properties as follows:

- The target scope of D is the scope to which C
  belongs [[basic.scope.scope]].
- The locus of D follows immediately after the core constant expression
  currently under evaluation.
- The characteristic sequence of D[[expr.const]] is the sequence of
  reflection values $r_K$.
- If C is a specialization of a templated class T, and C is not a local
  class, then D is an explicit specialization of T.
- For each $r_K$, there is a corresponding entity $M_K$ belonging to the
  class scope of D with the following properties:
  - If $N_K$ is $\bot$, $M_K$ is an unnamed bit-field. Otherwise, $M_K$
    is a non-static data member whose name is the identifier determined
    by the character sequence encoded by $N_K$ in UTF-8.
  - The type of $M_K$ is $T_K$.
  - $M_K$ is declared with the attribute `[[no_unique_address]]` if and
    only if *NUA*_K is `true`.
  - If $W_K$ is not $\bot$, $M_K$ is a bit-field whose width is that
    value. Otherwise, $M_K$ is not a bit-field.
  - If $A_K$ is not $\bot$, $M_K$ has the *alignment-specifier*
    `alignas(`$A_K$`)`. Otherwise, $M_K$ has no *alignment-specifier*.
- For every $r_L$ in `mdescrs` such that K < L, the declaration
  corresponding to $r_K$ precedes the declaration corresponding to
  $r_L$.

*Returns:* `class_type`.

### Reflection type traits <a id="meta.reflection.traits">[[meta.reflection.traits]]</a>

This subclause specifies `consteval` functions to query the properties
of types [[meta.unary]], query the relationships between types
[[meta.rel]], or transform types [[meta.trans]], during program
translation. Each `consteval` function declared in this class has an
associated class template declared elsewhere in this document.

Every function and function template declared in this subclause throws
an exception of type `meta::exception` unless the following conditions
are met:

- For every parameter `p` of type `info`, `is_type(p)` is `true`.
- For every parameter `r` whose type is constrained on
  `reflection_range`, `ranges::{}all_of({}r, is_type)` is `true`.

``` cpp
// associated with [meta.unary.cat], primary type categories
consteval bool is_void_type(info type);
consteval bool is_null_pointer_type(info type);
consteval bool is_integral_type(info type);
consteval bool is_floating_point_type(info type);
consteval bool is_array_type(info type);
consteval bool is_pointer_type(info type);
consteval bool is_lvalue_reference_type(info type);
consteval bool is_rvalue_reference_type(info type);
consteval bool is_member_object_pointer_type(info type);
consteval bool is_member_function_pointer_type(info type);
consteval bool is_enum_type(info type);
consteval bool is_union_type(info type);
consteval bool is_class_type(info type);
consteval bool is_function_type(info type);
consteval bool is_reflection_type(info type);

// associated with [meta.unary.comp], composite type categories
consteval bool is_reference_type(info type);
consteval bool is_arithmetic_type(info type);
consteval bool is_fundamental_type(info type);
consteval bool is_object_type(info type);
consteval bool is_scalar_type(info type);
consteval bool is_compound_type(info type);
consteval bool is_member_pointer_type(info type);

// associated with [meta.unary.prop], type properties
consteval bool is_const_type(info type);
consteval bool is_volatile_type(info type);
consteval bool is_trivially_copyable_type(info type);
consteval bool is_trivially_relocatable_type(info type);
consteval bool is_replaceable_type(info type);
consteval bool is_standard_layout_type(info type);
consteval bool is_empty_type(info type);
consteval bool is_polymorphic_type(info type);
consteval bool is_abstract_type(info type);
consteval bool is_final_type(info type);
consteval bool is_aggregate_type(info type);
consteval bool is_consteval_only_type(info type);
consteval bool is_signed_type(info type);
consteval bool is_unsigned_type(info type);
consteval bool is_bounded_array_type(info type);
consteval bool is_unbounded_array_type(info type);
consteval bool is_scoped_enum_type(info type);

template<reflection_range R = initializer_list<info>>
  consteval bool is_constructible_type(info type, R&& type_args);
consteval bool is_default_constructible_type(info type);
consteval bool is_copy_constructible_type(info type);
consteval bool is_move_constructible_type(info type);

consteval bool is_assignable_type(info type_dst, info type_src);
consteval bool is_copy_assignable_type(info type);
consteval bool is_move_assignable_type(info type);

consteval bool is_swappable_with_type(info type1, info type2);
consteval bool is_swappable_type(info type);

consteval bool is_destructible_type(info type);

template<reflection_range R = initializer_list<info>>
  consteval bool is_trivially_constructible_type(info type, R&& type_args);
consteval bool is_trivially_default_constructible_type(info type);
consteval bool is_trivially_copy_constructible_type(info type);
consteval bool is_trivially_move_constructible_type(info type);

consteval bool is_trivially_assignable_type(info type_dst, info type_src);
consteval bool is_trivially_copy_assignable_type(info type);
consteval bool is_trivially_move_assignable_type(info type);
consteval bool is_trivially_destructible_type(info type);

template<reflection_range R = initializer_list<info>>
  consteval bool is_nothrow_constructible_type(info type, R&& type_args);
consteval bool is_nothrow_default_constructible_type(info type);
consteval bool is_nothrow_copy_constructible_type(info type);
consteval bool is_nothrow_move_constructible_type(info type);

consteval bool is_nothrow_assignable_type(info type_dst, info type_src);
consteval bool is_nothrow_copy_assignable_type(info type);
consteval bool is_nothrow_move_assignable_type(info type);

consteval bool is_nothrow_swappable_with_type(info type1, info type2);
consteval bool is_nothrow_swappable_type(info type);

consteval bool is_nothrow_destructible_type(info type);
consteval bool is_nothrow_relocatable_type(info type);

consteval bool is_implicit_lifetime_type(info type);

consteval bool has_virtual_destructor(info type);

consteval bool has_unique_object_representations(info type);

consteval bool reference_constructs_from_temporary(info type_dst, info type_src);
consteval bool reference_converts_from_temporary(info type_dst, info type_src);

// associated with [meta.rel], type relations
consteval bool is_same_type(info type1, info type2);
consteval bool is_base_of_type(info type_base, info type_derived);
consteval bool is_virtual_base_of_type(info type_base, info type_derived);
consteval bool is_convertible_type(info type_src, info type_dst);
consteval bool is_nothrow_convertible_type(info type_src, info type_dst);
consteval bool is_layout_compatible_type(info type1, info type2);
consteval bool is_pointer_interconvertible_base_of_type(info type_base, info type_derived);

template<reflection_range R = initializer_list<info>>
  consteval bool is_invocable_type(info type, R&& type_args);
template<reflection_range R = initializer_list<info>>
  consteval bool is_invocable_r_type(info type_result, info type, R&& type_args);

template<reflection_range R = initializer_list<info>>
  consteval bool is_nothrow_invocable_type(info type, R&& type_args);
template<reflection_range R = initializer_list<info>>
  consteval bool is_nothrow_invocable_r_type(info type_result, info type, R&& type_args);

// associated with [meta.trans.cv], const-volatile modifications
consteval info remove_const(info type);
consteval info remove_volatile(info type);
consteval info remove_cv(info type);
consteval info add_const(info type);
consteval info add_volatile(info type);
consteval info add_cv(info type);

// associated with [meta.trans.ref], reference modifications
consteval info remove_reference(info type);
consteval info add_lvalue_reference(info type);
consteval info add_rvalue_reference(info type);

// associated with [meta.trans.sign], sign modifications
consteval info make_signed(info type);
consteval info make_unsigned(info type);

// associated with [meta.trans.arr], array modifications
consteval info remove_extent(info type);
consteval info remove_all_extents(info type);

// associated with [meta.trans.ptr], pointer modifications
consteval info remove_pointer(info type);
consteval info add_pointer(info type);

// associated with [meta.trans.other], other transformations
consteval info remove_cvref(info type);
consteval info decay(info type);
template<reflection_range R = initializer_list<info>>
  consteval info common_type(R&& type_args);
template<reflection_range R = initializer_list<info>>
  consteval info common_reference(R&& type_args);
consteval info underlying_type(info type);
template<reflection_range R = initializer_list<info>>
  consteval info invoke_result(info type, R&& type_args);
consteval info unwrap_reference(info type);
consteval info unwrap_ref_decay(info type);
```

Each function or function template declared above has the following
behavior based on the signature and return type of that function or
function template.

[*Note 1*: The associated class template need not be
instantiated. — *end note*\]

[*Note 2*: For those functions or function templates which return a
reflection, that reflection always represents a type and never a type
alias. — *end note*\]

[*Note 3*: If `t` is a reflection of the type `int` and `u` is a
reflection of an alias to the type `int`, then `t == u` is `false` but
`is_same_type(t, u)` is `true`. Also, `t == dealias(u)` is
`true`. — *end note*\]

``` cpp
consteval size_t rank(info type);
```

*Returns:* `rank_v<`T`>`, where T is the type represented by
`dealias(type)`.

``` cpp
consteval size_t extent(info type, unsigned i = 0);
```

*Returns:* `extent_v<`T`, `I`>`, where T is the type represented by
`dealias(type)` and I is a constant equal to `i`.

``` cpp
consteval size_t tuple_size(info type);
```

*Returns:* `tuple_size_v<`T`>`, where T is the type represented by
`dealias(type)`.

``` cpp
consteval info tuple_element(size_t index, info type);
```

*Returns:* A reflection representing the type denoted by
`tuple_element_t<`I`, `T`>`, where T is the type represented by
`dealias(type)` and I is a constant equal to `index`.

``` cpp
consteval size_t variant_size(info type);
```

*Returns:* `variant_size_v<`T`>`, where T is the type represented by
`dealias(type)`.

``` cpp
consteval info variant_alternative(size_t index, info type);
```

*Returns:* A reflection representing the type denoted by
`variant_alternative_t<`I`, `T`>`, where T is the type represented by
`dealias(type)` and I is a constant equal to `index`.

``` cpp
consteval strong_ordering type_order(info t1, info t2);
```

*Returns:* `type_order_v<`T₁`, `T₂`>`, where T₁ and T₂ are the types
represented by `dealias(t1)` and `dealias(t2)`, respectively.

## Compile-time rational arithmetic <a id="ratio">[[ratio]]</a>

### General <a id="ratio.general">[[ratio.general]]</a>

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
// all freestanding
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
    constexpr bool ratio_equal_v = ratio_equal<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool ratio_not_equal_v = ratio_not_equal<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool ratio_less_v = ratio_less<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool ratio_less_equal_v = ratio_less_equal<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool ratio_greater_v = ratio_greater<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool ratio_greater_equal_v = ratio_greater_equal<R1, R2>::value;

  // [ratio.si], convenience SI typedefs
  using quecto = ratio<1, 1'000'000'000'000'000'000'000'000'000'000>;     // see below
  using ronto  = ratio<1,     1'000'000'000'000'000'000'000'000'000>;     // see below
  using yocto  = ratio<1,         1'000'000'000'000'000'000'000'000>;     // see below
  using zepto  = ratio<1,             1'000'000'000'000'000'000'000>;     // see below
  using atto   = ratio<1,                 1'000'000'000'000'000'000>;
  using femto  = ratio<1,                     1'000'000'000'000'000>;
  using pico   = ratio<1,                         1'000'000'000'000>;
  using nano   = ratio<1,                             1'000'000'000>;
  using micro  = ratio<1,                                 1'000'000>;
  using milli  = ratio<1,                                     1'000>;
  using centi  = ratio<1,                                       100>;
  using deci   = ratio<1,                                        10>;
  using deca   = ratio<                                       10, 1>;
  using hecto  = ratio<                                      100, 1>;
  using kilo   = ratio<                                    1'000, 1>;
  using mega   = ratio<                                1'000'000, 1>;
  using giga   = ratio<                            1'000'000'000, 1>;
  using tera   = ratio<                        1'000'000'000'000, 1>;
  using peta   = ratio<                    1'000'000'000'000'000, 1>;
  using exa    = ratio<                1'000'000'000'000'000'000, 1>;
  using zetta  = ratio<            1'000'000'000'000'000'000'000, 1>;     // see below
  using yotta  = ratio<        1'000'000'000'000'000'000'000'000, 1>;     // see below
  using ronna  = ratio<    1'000'000'000'000'000'000'000'000'000, 1>;     // see below
  using quetta = ratio<1'000'000'000'000'000'000'000'000'000'000, 1>;     // see below
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
value. — *end note*\]

The static data members `num` and `den` shall have the following values,
where `gcd` represents the greatest common divisor of the absolute
values of `N` and `D`:

- `num` shall have the value
  `\operatorname{sgn}(\tcode{N}) * \operatorname{sgn}(\tcode{D}) * abs(N) / gcd`.
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

— *end example*\]

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

For each of the *typedef-name*s `quecto`, `ronto`, `yocto`, `zepto`,
`zetta`, `yotta`, `ronna`, and `quetta`, if both of the constants used
in its specification are representable by `intmax_t`, the typedef is
defined; if either of the constants is not representable by `intmax_t`,
the typedef is not defined.

<!-- Section link definitions -->
[const.wrap.class]: #const.wrap.class
[intseq]: #intseq
[intseq.general]: #intseq.general
[intseq.intseq]: #intseq.intseq
[intseq.make]: #intseq.make
[meta]: #meta
[meta.const.eval]: #meta.const.eval
[meta.define.static]: #meta.define.static
[meta.general]: #meta.general
[meta.help]: #meta.help
[meta.logical]: #meta.logical
[meta.member]: #meta.member
[meta.reflection]: #meta.reflection
[meta.reflection.access.context]: #meta.reflection.access.context
[meta.reflection.access.queries]: #meta.reflection.access.queries
[meta.reflection.annotation]: #meta.reflection.annotation
[meta.reflection.define.aggregate]: #meta.reflection.define.aggregate
[meta.reflection.exception]: #meta.reflection.exception
[meta.reflection.extract]: #meta.reflection.extract
[meta.reflection.layout]: #meta.reflection.layout
[meta.reflection.member.queries]: #meta.reflection.member.queries
[meta.reflection.names]: #meta.reflection.names
[meta.reflection.operators]: #meta.reflection.operators
[meta.reflection.queries]: #meta.reflection.queries
[meta.reflection.result]: #meta.reflection.result
[meta.reflection.substitute]: #meta.reflection.substitute
[meta.reflection.traits]: #meta.reflection.traits
[meta.rel]: #meta.rel
[meta.rqmts]: #meta.rqmts
[meta.string.literal]: #meta.string.literal
[meta.syn]: #meta.syn
[meta.trans]: #meta.trans
[meta.trans.arr]: #meta.trans.arr
[meta.trans.cv]: #meta.trans.cv
[meta.trans.general]: #meta.trans.general
[meta.trans.other]: #meta.trans.other
[meta.trans.ptr]: #meta.trans.ptr
[meta.trans.ref]: #meta.trans.ref
[meta.trans.sign]: #meta.trans.sign
[meta.type.synop]: #meta.type.synop
[meta.unary]: #meta.unary
[meta.unary.cat]: #meta.unary.cat
[meta.unary.comp]: #meta.unary.comp
[meta.unary.general]: #meta.unary.general
[meta.unary.prop]: #meta.unary.prop
[meta.unary.prop.query]: #meta.unary.prop.query
[ratio]: #ratio
[ratio.arithmetic]: #ratio.arithmetic
[ratio.comparison]: #ratio.comparison
[ratio.general]: #ratio.general
[ratio.ratio]: #ratio.ratio
[ratio.si]: #ratio.si
[ratio.syn]: #ratio.syn
[type.traits]: #type.traits
[type.traits.general]: #type.traits.general

<!-- Link reference definitions -->
[array]: containers.md#array
[basic.align]: basic.md#basic.align
[basic.compound]: basic.md#basic.compound
[basic.fundamental]: basic.md#basic.fundamental
[basic.life]: basic.md#basic.life
[basic.link]: basic.md#basic.link
[basic.lookup.argdep]: basic.md#basic.lookup.argdep
[basic.scope.param]: basic.md#basic.scope.param
[basic.scope.scope]: basic.md#basic.scope.scope
[basic.stc]: basic.md#basic.stc
[basic.stc.general]: basic.md#basic.stc.general
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[basic.types.general]: basic.md#basic.types.general
[class.abstract]: class.md#class.abstract
[class.access.base]: class.md#class.access.base
[class.conv.fct]: class.md#class.conv.fct
[class.dtor]: class.md#class.dtor
[class.inhctor.init]: class.md#class.inhctor.init
[class.mem]: class.md#class.mem
[class.mem.general]: class.md#class.mem.general
[class.pre]: class.md#class.pre
[class.prop]: class.md#class.prop
[class.temporary]: basic.md#class.temporary
[class.union.anon]: class.md#class.union.anon
[class.virtual]: class.md#class.virtual
[conv.qual]: expr.md#conv.qual
[conv.rank]: basic.md#conv.rank
[dcl.array]: dcl.md#dcl.array
[dcl.enum]: dcl.md#dcl.enum
[dcl.fct]: dcl.md#dcl.fct
[dcl.fct.def.default]: dcl.md#dcl.fct.def.default
[dcl.fct.def.delete]: dcl.md#dcl.fct.def.delete
[dcl.fct.default]: dcl.md#dcl.fct.default
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.link]: dcl.md#dcl.link
[dcl.pre]: dcl.md#dcl.pre
[dcl.ref]: dcl.md#dcl.ref
[dcl.typedef]: dcl.md#dcl.typedef
[declval]: utilities.md#declval
[defns.referenceable]: #defns.referenceable
[enum]: dcl.md#enum
[except.spec]: except.md#except.spec
[expr.alignof]: expr.md#expr.alignof
[expr.call]: expr.md#expr.call
[expr.const]: expr.md#expr.const
[expr.prim.lambda.closure]: expr.md#expr.prim.lambda.closure
[expr.prim.splice]: expr.md#expr.prim.splice
[expr.type]: expr.md#expr.type
[expr.unary.noexcept]: expr.md#expr.unary.noexcept
[functional.syn]: utilities.md#functional.syn
[intro.execution]: basic.md#intro.execution
[intro.object]: basic.md#intro.object
[intseq]: #intseq
[lex.key]: lex.md#lex.key
[lex.name]: lex.md#lex.name
[lex.string]: lex.md#lex.string
[meta.help]: #meta.help
[meta.reflection]: #meta.reflection
[meta.reflection.operators]: #meta.reflection.operators
[meta.rel]: #meta.rel
[meta.rqmts]: #meta.rqmts
[meta.summary]: #meta.summary
[meta.trans]: #meta.trans
[meta.trans.arr]: #meta.trans.arr
[meta.trans.cv]: #meta.trans.cv
[meta.trans.other]: #meta.trans.other
[meta.trans.ptr]: #meta.trans.ptr
[meta.trans.ref]: #meta.trans.ref
[meta.trans.sign]: #meta.trans.sign
[meta.unary]: #meta.unary
[meta.unary.cat]: #meta.unary.cat
[meta.unary.comp]: #meta.unary.comp
[meta.unary.prop]: #meta.unary.prop
[meta.unary.prop.query]: #meta.unary.prop.query
[namespace.std]: library.md#namespace.std
[namespace.udecl]: dcl.md#namespace.udecl
[over.literal]: over.md#over.literal
[over.oper]: over.md#over.oper
[ratio]: #ratio
[ratio.arithmetic]: #ratio.arithmetic
[special]: class.md#special
[stmt.return]: stmt.md#stmt.return
[support.signal]: support.md#support.signal
[swappable.requirements]: library.md#swappable.requirements
[temp.arg]: temp.md#temp.arg
[temp.arg.nontype]: temp.md#temp.arg.nontype
[temp.dep.constexpr]: temp.md#temp.dep.constexpr
[temp.inst]: temp.md#temp.inst
[temp.names]: temp.md#temp.names
[temp.param]: temp.md#temp.param
[temp.pre]: temp.md#temp.pre
[temp.spec.partial]: temp.md#temp.spec.partial
[temp.type]: temp.md#temp.type
[term.implicit.lifetime.type]: #term.implicit.lifetime.type
[term.object.type]: #term.object.type
[term.odr.use]: #term.odr.use
[term.scalar.type]: #term.scalar.type
[term.standard.layout.type]: #term.standard.layout.type
[term.trivial.type]: #term.trivial.type
[term.trivially.copyable.type]: #term.trivially.copyable.type
[term.unevaluated.operand]: #term.unevaluated.operand
[tuple.apply]: utilities.md#tuple.apply
[type.traits]: #type.traits
