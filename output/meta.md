# Metaprogramming library <a id="meta">[meta]</a>

## General <a id="meta.general">[meta.general]</a>

This Clause describes metaprogramming facilities. These facilities are
summarized in [meta.summary].

**Table: Metaprogramming library summary**

| Subclause |  | Header |
| --- | --- | --- |
| [intseq] | Integer sequences | `<utility>` |
| [type.traits] | Type traits | `<type_traits>` |
| [ratio] | Rational arithmetic | `<ratio>` |

## Compile-time integer sequences <a id="intseq">[intseq]</a>

### In general <a id="intseq.general">[intseq.general]</a>

The library provides a class template that can represent an integer
sequence. When used as an argument to a function template the template
parameter pack defining the sequence can be deduced and used in a pack
expansion.

\[*Note 1*: The `index_sequence` alias template is provided for the
common case of an integer sequence of type `size_t`; see also
[tuple.apply]. — *end note*\]

### Class template `integer_sequence` <a id="intseq.intseq">[intseq.intseq]</a>

``` cpp
namespace std {
  template<class T, T... I> struct integer_sequence {
    using value_type = T;
    static constexpr size_t size() noexcept { return sizeof...(I); }
  };
}
```

`T` is an integer type.

### Alias template `make_integer_sequence` <a id="intseq.make">[intseq.make]</a>

``` cpp
template<class T, T N>
  using make_integer_sequence = integer_sequence<T, see below{}>;
```

***Mandates:***

$\texttt{N} \geq 0$.

The alias template `make_integer_sequence` denotes a specialization of
`integer_sequence` with `N` non-type template arguments. The type
`make_integer_sequence<T, N>` is an alias for the type
`integer_sequence<T, 0, 1, ..., N-1>`.

\[*Note 2*: `make_integer_sequence<int, 0>` is an alias for the type
`integer_sequence<int>`. — *end note*\]

## Metaprogramming and type traits <a id="type.traits">[type.traits]</a>

### General <a id="type.traits.general">[type.traits.general]</a>

Subclause [type.traits] describes components used by C++ programs,
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

All functions specified in [type.traits] are signal-safe
[support.signal].

### Requirements <a id="meta.rqmts">[meta.rqmts]</a>

A describes a property of a type. It shall be a class template that
takes one template type argument and, optionally, additional arguments
that help define the property being described. It shall be
*Cpp17DefaultConstructible*, *Cpp17CopyConstructible*, and publicly and
unambiguously derived, directly or indirectly, from its
*base characteristic*, which is a specialization of the template
`integral_constant` [meta.help], with the arguments to the template
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
`integral_constant` [meta.help], with the arguments to the template
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
specializations for any of the templates specified in [type.traits] is
undefined.

Unless otherwise specified, an incomplete type may be used to
instantiate a template specified in [type.traits]. The behavior of a
program is undefined if:

- an instantiation of a template specified in [type.traits] directly or
  indirectly depends on an incompletely-defined object type `T`, and

- that instantiation could yield a different result were `T`
  hypothetically completed.

### Header `<type_traits>` synopsis <a id="meta.type.synop">[meta.type.synop]</a>

``` cpp
// all freestanding
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
    using \libglobal{remove_const_t}    = typename remove_const<T>::type;
  template<class T>
    using \libglobal{remove_volatile_t} = typename remove_volatile<T>::type;
  template<class T>
    using \libglobal{remove_cv_t}       = typename remove_cv<T>::type;
  template<class T>
    using \libglobal{add_const_t}       = typename add_const<T>::type;
  template<class T>
    using \libglobal{add_volatile_t}    = typename add_volatile<T>::type;
  template<class T>
    using \libglobal{add_cv_t}          = typename add_cv<T>::type;

  // [meta.trans.ref], reference modifications
  template<class T> struct remove_reference;
  template<class T> struct add_lvalue_reference;
  template<class T> struct add_rvalue_reference;

  template<class T>
    using \libglobal{remove_reference_t}     = typename remove_reference<T>::type;
  template<class T>
    using \libglobal{add_lvalue_reference_t} = typename add_lvalue_reference<T>::type;
  template<class T>
    using \libglobal{add_rvalue_reference_t} = typename add_rvalue_reference<T>::type;

  // [meta.trans.sign], sign modifications
  template<class T> struct make_signed;
  template<class T> struct make_unsigned;

  template<class T>
    using \libglobal{make_signed_t}   = typename make_signed<T>::type;
  template<class T>
    using \libglobal{make_unsigned_t} = typename make_unsigned<T>::type;

  // [meta.trans.arr], array modifications
  template<class T> struct remove_extent;
  template<class T> struct remove_all_extents;

  template<class T>
    using \libglobal{remove_extent_t}      = typename remove_extent<T>::type;
  template<class T>
    using \libglobal{remove_all_extents_t} = typename remove_all_extents<T>::type;

  // [meta.trans.ptr], pointer modifications
  template<class T> struct remove_pointer;
  template<class T> struct add_pointer;

  template<class T>
    using \libglobal{remove_pointer_t} = typename remove_pointer<T>::type;
  template<class T>
    using \libglobal{add_pointer_t}    = typename add_pointer<T>::type;

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
  template<class T> struct unwrap_reference;
  template<class T> struct unwrap_ref_decay;

  template<class T>
    using \libglobal{type_identity_t}    = typename type_identity<T>::type;
  template<class T>
    using \libglobal{remove_cvref_t}     = typename remove_cvref<T>::type;
  template<class T>
    using \libglobal{decay_t}            = typename decay<T>::type;
  template<bool B, class T = void>
    using \libglobal{enable_if_t}        = typename enable_if<B, T>::type;
  template<bool B, class T, class F>
    using \libglobal{conditional_t}      = typename conditional<B, T, F>::type;
  template<class... T>
    using \libglobal{common_type_t}      = typename common_type<T...>::type;
  template<class... T>
    using \libglobal{common_reference_t} = typename common_reference<T...>::type;
  template<class T>
    using \libglobal{underlying_type_t}  = typename underlying_type<T>::type;
  template<class Fn, class... ArgTypes>
    using \libglobal{invoke_result_t}    = typename invoke_result<Fn, ArgTypes...>::type;
  template<class T>
    using unwrap_reference_t = typename unwrap_reference<T>::type;
  template<class T>
    using unwrap_ref_decay_t = typename unwrap_ref_decay<T>::type;
  template<class...>
    using \libglobal{void_t}             = void;

  // [meta.logical], logical operator traits
  template<class... B> struct conjunction;
  template<class... B> struct disjunction;
  template<class B> struct negation;

  // [meta.unary.cat], primary type categories
  template<class T>
    constexpr bool \libglobal{is_void_v} = is_void<T>::value;
  template<class T>
    constexpr bool \libglobal{is_null_pointer_v} = is_null_pointer<T>::value;
  template<class T>
    constexpr bool \libglobal{is_integral_v} = is_integral<T>::value;
  template<class T>
    constexpr bool \libglobal{is_floating_point_v} = is_floating_point<T>::value;
  template<class T>
    constexpr bool \libglobal{is_array_v} = is_array<T>::value;
  template<class T>
    constexpr bool \libglobal{is_pointer_v} = is_pointer<T>::value;
  template<class T>
    constexpr bool \libglobal{is_lvalue_reference_v} = is_lvalue_reference<T>::value;
  template<class T>
    constexpr bool \libglobal{is_rvalue_reference_v} = is_rvalue_reference<T>::value;
  template<class T>
    constexpr bool \libglobal{is_member_object_pointer_v} = is_member_object_pointer<T>::value;
  template<class T>
    constexpr bool \libglobal{is_member_function_pointer_v} = is_member_function_pointer<T>::value;
  template<class T>
    constexpr bool \libglobal{is_enum_v} = is_enum<T>::value;
  template<class T>
    constexpr bool \libglobal{is_union_v} = is_union<T>::value;
  template<class T>
    constexpr bool \libglobal{is_class_v} = is_class<T>::value;
  template<class T>
    constexpr bool \libglobal{is_function_v} = is_function<T>::value;

  // [meta.unary.comp], composite type categories
  template<class T>
    constexpr bool \libglobal{is_reference_v} = is_reference<T>::value;
  template<class T>
    constexpr bool \libglobal{is_arithmetic_v} = is_arithmetic<T>::value;
  template<class T>
    constexpr bool \libglobal{is_fundamental_v} = is_fundamental<T>::value;
  template<class T>
    constexpr bool \libglobal{is_object_v} = is_object<T>::value;
  template<class T>
    constexpr bool \libglobal{is_scalar_v} = is_scalar<T>::value;
  template<class T>
    constexpr bool \libglobal{is_compound_v} = is_compound<T>::value;
  template<class T>
    constexpr bool \libglobal{is_member_pointer_v} = is_member_pointer<T>::value;

  // [meta.unary.prop], type properties
  template<class T>
    constexpr bool \libglobal{is_const_v} = is_const<T>::value;
  template<class T>
    constexpr bool \libglobal{is_volatile_v} = is_volatile<T>::value;
  template<class T>
    constexpr bool \libglobal{is_trivial_v} = is_trivial<T>::value;
  template<class T>
    constexpr bool \libglobal{is_trivially_copyable_v} = is_trivially_copyable<T>::value;
  template<class T>
    constexpr bool \libglobal{is_standard_layout_v} = is_standard_layout<T>::value;
  template<class T>
    constexpr bool \libglobal{is_empty_v} = is_empty<T>::value;
  template<class T>
    constexpr bool \libglobal{is_polymorphic_v} = is_polymorphic<T>::value;
  template<class T>
    constexpr bool \libglobal{is_abstract_v} = is_abstract<T>::value;
  template<class T>
    constexpr bool \libglobal{is_final_v} = is_final<T>::value;
  template<class T>
    constexpr bool \libglobal{is_aggregate_v} = is_aggregate<T>::value;
  template<class T>
    constexpr bool \libglobal{is_signed_v} = is_signed<T>::value;
  template<class T>
    constexpr bool \libglobal{is_unsigned_v} = is_unsigned<T>::value;
  template<class T>
    constexpr bool \libglobal{is_bounded_array_v} = is_bounded_array<T>::value;
  template<class T>
    constexpr bool \libglobal{is_unbounded_array_v} = is_unbounded_array<T>::value;
  template<class T>
    constexpr bool \libglobal{is_scoped_enum_v} = is_scoped_enum<T>::value;
  template<class T, class... Args>
    constexpr bool \libglobal{is_constructible_v} = is_constructible<T, Args...>::value;
  template<class T>
    constexpr bool \libglobal{is_default_constructible_v} = is_default_constructible<T>::value;
  template<class T>
    constexpr bool \libglobal{is_copy_constructible_v} = is_copy_constructible<T>::value;
  template<class T>
    constexpr bool \libglobal{is_move_constructible_v} = is_move_constructible<T>::value;
  template<class T, class U>
    constexpr bool \libglobal{is_assignable_v} = is_assignable<T, U>::value;
  template<class T>
    constexpr bool \libglobal{is_copy_assignable_v} = is_copy_assignable<T>::value;
  template<class T>
    constexpr bool \libglobal{is_move_assignable_v} = is_move_assignable<T>::value;
  template<class T, class U>
    constexpr bool \libglobal{is_swappable_with_v} = is_swappable_with<T, U>::value;
  template<class T>
    constexpr bool \libglobal{is_swappable_v} = is_swappable<T>::value;
  template<class T>
    constexpr bool \libglobal{is_destructible_v} = is_destructible<T>::value;
  template<class T, class... Args>
    constexpr bool is_trivially_constructible_v
      = is_trivially_constructible<T, Args...>::value;
  template<class T>
    constexpr bool is_trivially_default_constructible_v
      = is_trivially_default_constructible<T>::value;
  template<class T>
    constexpr bool is_trivially_copy_constructible_v
      = is_trivially_copy_constructible<T>::value;
  template<class T>
    constexpr bool is_trivially_move_constructible_v
      = is_trivially_move_constructible<T>::value;
  template<class T, class U>
    constexpr bool \libglobal{is_trivially_assignable_v} = is_trivially_assignable<T, U>::value;
  template<class T>
    constexpr bool is_trivially_copy_assignable_v
      = is_trivially_copy_assignable<T>::value;
  template<class T>
    constexpr bool is_trivially_move_assignable_v
      = is_trivially_move_assignable<T>::value;
  template<class T>
    constexpr bool \libglobal{is_trivially_destructible_v} = is_trivially_destructible<T>::value;
  template<class T, class... Args>
    constexpr bool is_nothrow_constructible_v
      = is_nothrow_constructible<T, Args...>::value;
  template<class T>
    constexpr bool is_nothrow_default_constructible_v
      = is_nothrow_default_constructible<T>::value;
  template<class T>
    constexpr bool is_nothrow_copy_constructible_v
      = is_nothrow_copy_constructible<T>::value;
  template<class T>
    constexpr bool is_nothrow_move_constructible_v
      = is_nothrow_move_constructible<T>::value;
  template<class T, class U>
    constexpr bool \libglobal{is_nothrow_assignable_v} = is_nothrow_assignable<T, U>::value;
  template<class T>
    constexpr bool \libglobal{is_nothrow_copy_assignable_v} = is_nothrow_copy_assignable<T>::value;
  template<class T>
    constexpr bool \libglobal{is_nothrow_move_assignable_v} = is_nothrow_move_assignable<T>::value;
  template<class T, class U>
    constexpr bool \libglobal{is_nothrow_swappable_with_v} = is_nothrow_swappable_with<T, U>::value;
  template<class T>
    constexpr bool \libglobal{is_nothrow_swappable_v} = is_nothrow_swappable<T>::value;
  template<class T>
    constexpr bool \libglobal{is_nothrow_destructible_v} = is_nothrow_destructible<T>::value;
  template<class T>
    constexpr bool \libglobal{is_implicit_lifetime_v} = is_implicit_lifetime<T>::value;
  template<class T>
    constexpr bool \libglobal{has_virtual_destructor_v} = has_virtual_destructor<T>::value;
  template<class T>
    constexpr bool has_unique_object_representations_v
      = has_unique_object_representations<T>::value;
  template<class T, class U>
    constexpr bool \libglobal{reference_constructs_from_temporary_v}
      = reference_constructs_from_temporary<T, U>::value;
  template<class T, class U>
    constexpr bool \libglobal{reference_converts_from_temporary_v}
      = reference_converts_from_temporary<T, U>::value;

  // [meta.unary.prop.query], type property queries
  template<class T>
    constexpr size_t \libglobal{alignment_of_v} = alignment_of<T>::value;
  template<class T>
    constexpr size_t \libglobal{rank_v} = rank<T>::value;
  template<class T, unsigned I = 0>
    constexpr size_t \libglobal{extent_v} = extent<T, I>::value;

  // [meta.rel], type relations
  template<class T, class U>
    constexpr bool \libglobal{is_same_v} = is_same<T, U>::value;
  template<class Base, class Derived>
    constexpr bool \libglobal{is_base_of_v} = is_base_of<Base, Derived>::value;
  template<class From, class To>
    constexpr bool \libglobal{is_convertible_v} = is_convertible<From, To>::value;
  template<class From, class To>
    constexpr bool \libglobal{is_nothrow_convertible_v} = is_nothrow_convertible<From, To>::value;
  template<class T, class U>
    constexpr bool \libglobal{is_layout_compatible_v} = is_layout_compatible<T, U>::value;
  template<class Base, class Derived>
    constexpr bool is_pointer_interconvertible_base_of_v
      = is_pointer_interconvertible_base_of<Base, Derived>::value;
  template<class Fn, class... ArgTypes>
    constexpr bool \libglobal{is_invocable_v} = is_invocable<Fn, ArgTypes...>::value;
  template<class R, class Fn, class... ArgTypes>
    constexpr bool \libglobal{is_invocable_r_v} = is_invocable_r<R, Fn, ArgTypes...>::value;
  template<class Fn, class... ArgTypes>
    constexpr bool \libglobal{is_nothrow_invocable_v} = is_nothrow_invocable<Fn, ArgTypes...>::value;
  template<class R, class Fn, class... ArgTypes>
    constexpr bool is_nothrow_invocable_r_v
      = is_nothrow_invocable_r<R, Fn, ArgTypes...>::value;

  // [meta.logical], logical operator traits
  template<class... B>
    constexpr bool \libglobal{conjunction_v} = conjunction<B...>::value;
  template<class... B>
    constexpr bool \libglobal{disjunction_v} = disjunction<B...>::value;
  template<class B>
    constexpr bool \libglobal{negation_v} = negation<B>::value;

  // [meta.member], member relationships
  template<class S, class M>
    constexpr bool is_pointer_interconvertible_with_class(M S::*m) noexcept;
  template<class S1, class S2, class M1, class M2>
    constexpr bool is_corresponding_member(M1 S1::*m1, M2 S2::*m2) noexcept;

  // [meta.const.eval], constant evaluation context
  constexpr bool is_constant_evaluated() noexcept;
}
```

### Helper classes <a id="meta.help">[meta.help]</a>

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
and its associated *typedef-name* `true_type` and `false_type` are used
as base classes to define the interface for various type traits.

### Unary type traits <a id="meta.unary">[meta.unary]</a>

#### General <a id="meta.unary.general">[meta.unary.general]</a>

Subclause [meta.unary] contains templates that may be used to query the
properties of a type at compile time.

Each of these templates shall be a *Cpp17UnaryTypeTrait* [meta.rqmts]
with a base characteristic of `true_type` if the corresponding condition
is `true`, otherwise `false_type`.

#### Primary type categories <a id="meta.unary.cat">[meta.unary.cat]</a>

The primary type categories correspond to the descriptions given in
subclause  [basic.types] of the C++ standard.

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

\[*Note 1*: For any given type `T`, exactly one of the primary type
categories has a `value` member that evaluates to `true`. — *end note*\]

#### Composite type traits <a id="meta.unary.comp">[meta.unary.comp]</a>

These templates provide convenient compositions of the primary type
categories, corresponding to the descriptions given in subclause 
[basic.types].

For any given type `T`, the result of applying one of these templates to
`T` and to cv `T` shall yield the same result.

#### Type properties <a id="meta.unary.prop">[meta.unary.prop]</a>

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
trivial [term.trivial.type], [special] function call that is not an
odr-use [term.odr.use] of `declval` in the context of the corresponding
definition notwithstanding the restrictions of  [declval].

For the purpose of defining the templates in this subclause, let
`VAL<T>` for some type `T` be an expression defined as follows:

- If `T` is a reference or function type, `VAL<T>` is an expression with
  the same type and value category as `declval<T>()`.

- Otherwise, `VAL<T>` is a prvalue that initially has type `T`.

  \[*Note 1*: If `T` is cv-qualified, the cv-qualification is subject to
  adjustment [expr.type]. — *end note*\]

\[*Example 1*:

``` cpp
is_const_v<const volatile int>      // true
is_const_v<const int*>              // false
is_const_v<const int&>              // false
is_const_v<int[3]>                  // false
is_const_v<const int[3]>            // true
```

— *end example*\]

\[*Example 2*:

``` cpp
remove_const_t<const volatile int>  // volatile int
remove_const_t<const int* const>    // const int*
remove_const_t<const int&>          // const int\&
remove_const_t<const int[3]>        // int[3]
```

— *end example*\]

\[*Example 3*:

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

\[*Note 2*: These tokens are never interpreted as a function
declaration. — *end note*\]

Access checking is performed as if in a context unrelated to `T` and any
of the `Args`. Only the validity of the immediate context of the
variable initialization is considered.

\[*Note 3*: The evaluation of the initialization can result in side
effects such as the instantiation of class template specializations and
function template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*\]

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

\[*Note 4*: If a type has padding bits, the condition does not hold;
otherwise, the condition holds true for integral types. — *end note*\]

### Type property queries <a id="meta.unary.prop.query">[meta.unary.prop.query]</a>

This subclause contains templates that may be used to query properties
of types at compile time.

Each of these templates shall be a *Cpp17UnaryTypeTrait* [meta.rqmts]
with a base characteristic of `integral_constant<size_t, Value>`.

\[*Example 4*:

``` cpp
// the following assertions hold:
assert(rank_v<int> == 0);
assert(rank_v<int[2]> == 1);
assert(rank_v<int[][4]> == 2);
```

— *end example*\]

\[*Example 5*:

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

— *end example*\]

### Relationships between types <a id="meta.rel">[meta.rel]</a>

This subclause contains templates that may be used to query
relationships between types at compile time.

Each of these templates shall be a *Cpp17BinaryTypeTrait* [meta.rqmts]
with a base characteristic of `true_type` if the corresponding condition
is true, otherwise `false_type`.

For the purpose of defining the templates in this subclause, a function
call expression `declval<T>()` for any type `T` is considered to be a
trivial [term.trivial.type], [special] function call that is not an
odr-use [term.odr.use] of `declval` in the context of the corresponding
definition notwithstanding the restrictions of  [declval].

\[*Example 6*:

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

\[*Note 5*: This requirement gives well-defined results for reference
types, array types, function types, and cv `void`. — *end note*\]

Access checking is performed in a context unrelated to `To` and `From`.
Only the validity of the immediate context of the *expression* of the
`return` statement [stmt.return] (including initialization of the
returned object or reference) is considered.

\[*Note 6*: The initialization can result in side effects such as the
instantiation of class template specializations and function template
specializations, the generation of implicitly-defined functions, and so
on. Such side effects are not in the “immediate context” and can result
in the program being ill-formed. — *end note*\]

### Transformations between types <a id="meta.trans">[meta.trans]</a>

#### General <a id="meta.trans.general">[meta.trans.general]</a>

Each of the templates in [meta.trans] shall be a
*Cpp17TransformationTrait* [meta.rqmts].

#### Const-volatile modifications <a id="meta.trans.cv">[meta.trans.cv]</a>

#### Reference modifications <a id="meta.trans.ref">[meta.trans.ref]</a>

#### Sign modifications <a id="meta.trans.sign">[meta.trans.sign]</a>

#### Array modifications <a id="meta.trans.arr">[meta.trans.arr]</a>

\[*Example 7*:

``` cpp
// the following assertions hold:
assert((is_same_v<remove_extent_t<int>, int>));
assert((is_same_v<remove_extent_t<int[2]>, int>));
assert((is_same_v<remove_extent_t<int[2][3]>, int[3]>));
assert((is_same_v<remove_extent_t<int[][3]>, int[3]>));
```

— *end example*\]

\[*Example 8*:

``` cpp
// the following assertions hold:
assert((is_same_v<remove_all_extents_t<int>, int>));
assert((is_same_v<remove_all_extents_t<int[2]>, int>));
assert((is_same_v<remove_all_extents_t<int[2][3]>, int>));
assert((is_same_v<remove_all_extents_t<int[][3]>, int>));
```

— *end example*\]

#### Pointer modifications <a id="meta.trans.ptr">[meta.trans.ptr]</a>

#### Other transformations <a id="meta.trans.other">[meta.trans.other]</a>

\[*Note 7*: The compilation of the expression can result in side effects
such as the instantiation of class template specializations and function
template specializations, the generation of implicitly-defined
functions, and so on. Such side effects are not in the “immediate
context” and can result in the program being ill-formed. — *end note*\]

In addition to being available via inclusion of the `<type_traits>`
header, the templates `unwrap_reference`, `unwrap_ref_decay`,
`unwrap_reference_t`, and `unwrap_ref_decay_t` are available when the
header `<functional>` [functional.syn] is included.

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
`remove_reference_t<B>`, and let `COMMON-REF(A, B)` be:

- If `A` and `B` are both lvalue reference types, `COMMON-REF(A, B)` is
  `COND-RES(COPYCV(X, Y) &,
      COPYCV(Y, X) &)` if that type exists and is a reference type.

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

Note B: Notwithstanding the provisions of [meta.type.synop], and
pursuant to [namespace.std], a program may specialize
`common_type<T1, T2>` for types `T1` and `T2` such that
`is_same_v<T1, decay_t<T1>>` and `is_same_v<T2, decay_t<T2>>` are each
`true`.

\[*Note 8*: Such specializations are needed when only explicit
conversions are desired between the template arguments. — *end note*\]

Such a specialization need not have a member named `type`, but if it
does, the *qualified-id* `common_type<T1, T2>::type` shall denote a
cv-unqualified non-reference type to which each of the types `T1` and
`T2` is explicitly convertible. Moreover, `common_type_t<T1, T2>` shall
denote the same type, if any, as does `common_type_t<T2, T1>`. No
diagnostic is required for a violation of this Note’s rules.

Note C: For the `common_reference` trait applied to a parameter pack `T`
of types, the member `type` shall be either defined or not present as
follows:

- If `sizeof...(T)` is zero, there shall be no member `type`.

- Otherwise, if `sizeof...(T)` is one, let `T0` denote the sole type in
  the pack `T`. The member typedef `type` shall denote the same type as
  `T0`.

- Otherwise, if `sizeof...(T)` is two, let `T1` and `T2` denote the two
  types in the pack `T`. Then

  - Let `R` be `COMMON-REF(T1, T2)`. If `T1` and `T2` are reference
    types, `R` is well-formed, and
    `is_convertible_v<add_pointer_t<T1>, add_pointer_t<R>> && is_convertible_v<add_poin\linebreak{}ter_t<T2>, add_pointer_t<R>>`
    is `true`, then the member typedef `type` denotes `R`.

  - Otherwise, if
    `basic_common_reference<remove_cvref_t<T1>, remove_cvref_t<T2>,
          XREF(T1), XREF(T2)>::type` is well-formed, then the member
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

Note D: Notwithstanding the provisions of [meta.type.synop], and
pursuant to [namespace.std], a program may partially specialize
`basic_common_reference<T, U, TQual, UQual>` for types `T` and `U` such
that `is_same_v<T, decay_t<T>>` and `is_same_v<U, decay_t<U>>` are each
`true`.

\[*Note 9*: Such specializations can be used to influence the result of
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

\[*Example 9*:

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

### Logical operator traits <a id="meta.logical">[meta.logical]</a>

This subclause describes type traits for applying logical operators to
other type traits.

``` cpp
template<class... B> struct conjunction : see below { };
```

The class template `conjunction` forms the logical conjunction of its
template type arguments.

For a specialization
`conjunction<`$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$`>`, if
there is a template type argument $\texttt{B}_{i}$ for which
`bool(`$\texttt{B}_{i}$`::value)` is `false`, then instantiating
`conjunction<`$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$`>::value`
does not require the instantiation of $\texttt{B}_{j}$`::value` for
j > i.

\[*Note 10*: This is analogous to the short-circuiting behavior of the
built-in operator `&&`. — *end note*\]

Every template type argument for which $\texttt{B}_{i}$`::value` is
instantiated shall be usable as a base class and shall have a member
`value` which is convertible to `bool`, is not hidden, and is
unambiguously available in the type.

The specialization
`conjunction<`$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$`>` has a
public and unambiguous base that is either

- the first type $\texttt{B}_{i}$ in the list
  `true_type, `$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$ for
  which `bool(`$\texttt{B}_{i}$`::value)` is `false`, or

- if there is no such $\texttt{B}_{i}$, the last type in the list.

\[*Note 11*: This means a specialization of `conjunction` does not
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

For a specialization
`disjunction<`$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$`>`, if
there is a template type argument $\texttt{B}_{i}$ for which
`bool(`$\texttt{B}_{i}$`::value)` is `true`, then instantiating
`disjunction<`$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$`>::value`
does not require the instantiation of $\texttt{B}_{j}$`::value` for
j > i.

\[*Note 12*: This is analogous to the short-circuiting behavior of the
built-in operator `||`. — *end note*\]

Every template type argument for which $\texttt{B}_{i}$`::value` is
instantiated shall be usable as a base class and shall have a member
`value` which is convertible to `bool`, is not hidden, and is
unambiguously available in the type.

The specialization
`disjunction<`$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$`>` has a
public and unambiguous base that is either

- the first type $\texttt{B}_{i}$ in the list
  `false_type, `$\texttt{B}_{1}$`, `$\dotsc$`, `$\texttt{B}_{N}$ for
  which `bool(`$\texttt{B}_{i}$`::value)` is `true`, or

- if there is no such $\texttt{B}_{i}$, the last type in the list.

\[*Note 13*: This means a specialization of `disjunction` does not
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

### Member relationships <a id="meta.member">[meta.member]</a>

``` cpp
template<class S, class M>
  constexpr bool is_pointer_interconvertible_with_class(M S::*m) noexcept;
```

***Mandates:***

`S` is a complete type.

***Returns:***

`true` if and only if `S` is a standard-layout type, `M` is an object
type, `m` is not null, and each object `s` of type `S` is
pointer-interconvertible\[basic.compound\] with its subobject `s.*m`.

``` cpp
template<class S1, class S2, class M1, class M2>
  constexpr bool is_corresponding_member(M1 S1::*m1, M2 S2::*m2) noexcept;
```

***Mandates:***

`S1` and `S2` are complete types.

***Returns:***

`true` if and only if `S1` and `S2` are standard-layout
struct\[class.prop\] types, `M1` and `M2` are object types, `m1` and
`m2` are not null, and `m1` and `m2` point to corresponding members of
the common initial sequence\[class.mem\] of `S1` and `S2`.

\[*Note 14*:

The type of a pointer-to-member expression `&C::b` is not always a
pointer to member of `C`, leading to potentially surprising results when
using these functions in conjunction with inheritance.

— *end note*\]

### Constant evaluation context <a id="meta.const.eval">[meta.const.eval]</a>

``` cpp
constexpr bool is_constant_evaluated() noexcept;
```

***Effects:***

Equivalent to:

``` cpp
if consteval {
  return true;
} else {
  return false;
}
```

\[*Example 10*:

    constexpr void f(unsigned char *p, int n) {
      if (std::is_constant_evaluated()) {           // should not be a constexpr if statement
        for (int k = 0; k<n; ++k) p[k] = 0;
      } else {
        memset(p, 0, n);                            // not a core constant expression
      }
    }

— *end example*\]

## Compile-time rational arithmetic <a id="ratio">[ratio]</a>

### In general <a id="ratio.general">[ratio.general]</a>

Subclause  [ratio] describes the ratio library. It provides a class
template `ratio` which exactly represents any finite rational number
with a numerator and denominator representable by compile-time constants
of type `intmax_t`.

Throughout subclause  [ratio], the names of template parameters are used
to express type requirements. If a template parameter is named `R1` or
`R2`, and the template argument is not a specialization of the `ratio`
template, the program is ill-formed.

### Header `<ratio>` synopsis <a id="ratio.syn">[ratio.syn]</a>

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
    constexpr bool \libglobal{ratio_equal_v} = ratio_equal<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool \libglobal{ratio_not_equal_v} = ratio_not_equal<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool \libglobal{ratio_less_v} = ratio_less<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool \libglobal{ratio_less_equal_v} = ratio_less_equal<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool \libglobal{ratio_greater_v} = ratio_greater<R1, R2>::value;
  template<class R1, class R2>
    constexpr bool \libglobal{ratio_greater_equal_v} = ratio_greater_equal<R1, R2>::value;

  // [ratio.si], convenience SI typedefs
  using \libglobal{yocto} = ratio<1, 1'000'000'000'000'000'000'000'000>;  // see below
  using \libglobal{zepto} = ratio<1,     1'000'000'000'000'000'000'000>;  // see below
  using \libglobal{atto}  = ratio<1,         1'000'000'000'000'000'000>;
  using \libglobal{femto} = ratio<1,             1'000'000'000'000'000>;
  using \libglobal{pico}  = ratio<1,                 1'000'000'000'000>;
  using \libglobal{nano}  = ratio<1,                     1'000'000'000>;
  using \libglobal{micro} = ratio<1,                         1'000'000>;
  using \libglobal{milli} = ratio<1,                             1'000>;
  using \libglobal{centi} = ratio<1,                               100>;
  using \libglobal{deci}  = ratio<1,                                10>;
  using \libglobal{deca}  = ratio<                               10, 1>;
  using \libglobal{hecto} = ratio<                              100, 1>;
  using \libglobal{kilo}  = ratio<                            1'000, 1>;
  using \libglobal{mega}  = ratio<                        1'000'000, 1>;
  using \libglobal{giga}  = ratio<                    1'000'000'000, 1>;
  using \libglobal{tera}  = ratio<                1'000'000'000'000, 1>;
  using \libglobal{peta}  = ratio<            1'000'000'000'000'000, 1>;
  using \libglobal{exa}   = ratio<        1'000'000'000'000'000'000, 1>;
  using \libglobal{zetta} = ratio<    1'000'000'000'000'000'000'000, 1>;  // see below
  using \libglobal{yotta} = ratio<1'000'000'000'000'000'000'000'000, 1>;  // see below
}
```

### Class template `ratio` <a id="ratio.ratio">[ratio.ratio]</a>

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

\[*Note 1*: These rules ensure that infinite ratios are avoided and that
for any negative input, there exists a representable value of its
absolute value which is positive. This excludes the most negative
value. — *end note*\]

The static data members `num` and `den` shall have the following values,
where `gcd` represents the greatest common divisor of the absolute
values of `N` and `D`:

- `num` shall have the value
  `$\operatorname{sgn}(\tcode{N})$ * $\operatorname{sgn}(\tcode{D})$ * abs(N) / gcd`.

- `den` shall have the value `abs(D) / gcd`.

### Arithmetic on `ratio}{s` <a id="ratio.arithmetic">[ratio.arithmetic]</a>

Each of the alias templates `ratio_add`, `ratio_subtract`,
`ratio_multiply`, and `ratio_divide` denotes the result of an arithmetic
computation on two `ratio}{s` `R1` and `R2`. With `X` and `Y` computed
(in the absence of arithmetic overflow) as specified by
[ratio.arithmetic], each alias denotes a `ratio<U, V>` such that `U` is
the same as `ratio<X, Y>::num` and `V` is the same as
`ratio<X, Y>::den`.

If it is not possible to represent `U` or `V` with `intmax_t`, the
program is ill-formed. Otherwise, an implementation should yield correct
values of `U` and `V`. If it is not possible to represent `X` or `Y`
with `intmax_t`, the program is ill-formed unless the implementation
yields correct values of `U` and `V`.

**Table: Expressions used to perform ratio arithmetic**

|  |  |  |
| --- | --- | --- |
| `ratio_add<R1, R2>` | `R1::num * R2::den +` | `R1::den * R2::den` |
|  | `R2::num * R1::den` |
| `ratio_subtract<R1, R2>` | `R1::num * R2::den -` | `R1::den * R2::den` |
|  | `R2::num * R1::den` |
| `ratio_multiply<R1, R2>` | `R1::num * R2::num` | `R1::den * R2::den` |
| `ratio_divide<R1, R2>` | `R1::num * R2::den` | `R1::den * R2::num` |
\[*Example 1*:

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

### Comparison of `ratio}{s` <a id="ratio.comparison">[ratio.comparison]</a>

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

### SI types for `ratio` <a id="ratio.si">[ratio.si]</a>

For each of the *typedef-name* `yocto`, `zepto`, `zetta`, and `yotta`,
if both of the constants used in its specification are representable by
`intmax_t`, the typedef is defined; if either of the constants is not
representable by `intmax_t`, the typedef is not defined.

<!-- Link reference definitions -->
[array]: containers.md#array
[basic.compound]: basic.md#basic.compound
[basic.fundamental]: basic.md#basic.fundamental
[basic.type.qualifier]: basic.md#basic.type.qualifier
[basic.types]: basic.md#basic.types
[basic.types.general]: basic.md#basic.types.general
[class.abstract]: class.md#class.abstract
[class.derived]: class.md#class.derived
[class.dtor]: class.md#class.dtor
[class.pre]: class.md#class.pre
[class.temporary]: basic.md#class.temporary
[class.virtual]: class.md#class.virtual
[conv.rank]: basic.md#conv.rank
[dcl.array]: dcl.md#dcl.array
[dcl.enum]: dcl.md#dcl.enum
[dcl.init.aggr]: dcl.md#dcl.init.aggr
[dcl.ref]: dcl.md#dcl.ref
[declval]: #declval
[defns.referenceable]: intro.md#defns.referenceable
[expr.alignof]: expr.md#expr.alignof
[expr.type]: expr.md#expr.type
[expr.unary.noexcept]: expr.md#expr.unary.noexcept
[func.require]: #func.require
[functional.syn]: #functional.syn
[meta.help]: #meta.help
[meta.rqmts]: #meta.rqmts
[meta.summary]: #meta.summary
[meta.trans]: #meta.trans
[meta.type.synop]: #meta.type.synop
[meta.unary]: #meta.unary
[namespace.std]: library.md#namespace.std
[ratio]: #ratio
[ratio.arithmetic]: #ratio.arithmetic
[special]: class.md#special
[stmt.return]: stmt.md#stmt.return
[support.signal]: support.md#support.signal
[swappable.requirements]: library.md#swappable.requirements
[term.layout.compatible.type]: #term.layout.compatible.type
[term.object.type]: #term.object.type
[term.odr.use]: #term.odr.use
[term.scalar.type]: #term.scalar.type
[term.standard.layout.type]: #term.standard.layout.type
[term.trivial.type]: #term.trivial.type
[term.trivially.copyable.type]: #term.trivially.copyable.type
[term.unevaluated.operand]: #term.unevaluated.operand
[tuple.apply]: #tuple.apply
[type.traits]: #type.traits

<!-- Link reference definitions -->
[intseq]: #intseq
[ratio]: #ratio
[type.traits]: #type.traits
